"""
Fixed Reactome Extractor with Pydantic Validation

This fixes the 'str' object has no attribute 'get' error by validating
API responses before accessing nested fields.
"""

import logging
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, field_validator
from enhanced_base import EnhancedBaseExtractor, console
from rich.panel import Panel

logger = logging.getLogger(__name__)


# ===== Pydantic Models for Reactome API =====

class ReactomeSpecies(BaseModel):
    """Validated species object - flexible to handle ID-only responses"""
    dbId: int
    displayName: Optional[str] = "Unknown Species"
    name: Optional[List[str]] = None
    taxId: Optional[str] = None

    @classmethod
    def from_id(cls, species_id: int):
        """Create species from just an ID"""
        return cls(dbId=species_id, displayName=f"Species {species_id}")


class ReactomePathway(BaseModel):
    """Validated pathway object with flexible species handling"""
    dbId: int
    displayName: str
    stId: str
    schemaClass: str
    species: Optional[List[ReactomeSpecies]] = None

    @field_validator('species', mode='before')
    @classmethod
    def validate_species(cls, v):
        """
        Handle species variations:
        - Can be None
        - Can be an integer (species ID)
        - Can be a single dict
        - Can be a list of dicts/ints
        - Can be a string (ERROR CASE - log and convert)
        """
        if v is None:
            return None

        # Integer ID -> convert to species object
        if isinstance(v, int):
            return [{'dbId': v, 'displayName': f"Species {v}"}]

        # ERROR CASE: API returned string
        if isinstance(v, str):
            logger.warning(f"Species returned as string: '{v}'. Converting to None.")
            return None

        # Single dict -> wrap in list
        if isinstance(v, dict):
            return [v]

        # List -> normalize each element
        if isinstance(v, list):
            normalized = []
            for item in v:
                if isinstance(item, int):
                    normalized.append({'dbId': item, 'displayName': f"Species {item}"})
                elif isinstance(item, dict):
                    normalized.append(item)
            return normalized

        # Unexpected type
        logger.error(f"Unexpected species type: {type(v)}. Converting to None.")
        return None


class ReactomeEvent(BaseModel):
    """Validated event (pathway or reaction) hierarchy"""
    dbId: int
    stId: str
    displayName: str
    schemaClass: str
    species: Optional[List[ReactomeSpecies]] = None
    children: Optional[List['ReactomeEvent']] = None

    @field_validator('species', mode='before')
    @classmethod
    def validate_species(cls, v):
        """Same species validation as ReactomePathway"""
        if v is None or isinstance(v, str):
            return None
        if isinstance(v, dict):
            return [v]
        return v if isinstance(v, list) else None

    @field_validator('children', mode='before')
    @classmethod
    def validate_children(cls, v):
        """Handle children variations"""
        if v is None or isinstance(v, str):
            return None
        if isinstance(v, dict):
            return [v]
        return v if isinstance(v, list) else None


# Enable forward references
ReactomeEvent.model_rebuild()


class ReactomeExtractorFixed(EnhancedBaseExtractor):
    """
    Fixed Reactome extractor with full pydantic validation

    Prevents parser errors by validating all API responses before field access.
    """

    def __init__(self):
        super().__init__(
            base_url="https://reactome.org/ContentService",
            rate_limit=0,  # No rate limit for Reactome
            max_retries=3,
            timeout=30
        )
        self.species_id = "9606"  # Human

    def extract_pathways(
        self,
        max_pathways: int = 500,
        top_level_only: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Extract Reactome pathways with validation

        Args:
            max_pathways: Maximum number of pathways to extract
            top_level_only: If True, only get top-level pathways

        Returns:
            List of validated pathway dictionaries
        """
        logger.info(f"Starting Reactome extraction for species {self.species_id}...")

        pathways = []

        try:
            if top_level_only:
                pathways = self._extract_top_level_pathways()
            else:
                pathways = self._extract_all_pathways()

            # Limit results
            pathways = pathways[:max_pathways]

            console.print(Panel(
                f"[bold green]Successfully extracted {len(pathways)} pathways[/bold green]",
                title="Reactome Extraction Complete",
                border_style="green"
            ))

        except Exception as e:
            logger.error(f"Error during extraction: {e}")
            console.print(Panel(
                f"[bold red]Extraction failed: {e}[/bold red]",
                title="Reactome Extraction Error",
                border_style="red"
            ))

        return pathways

    def _extract_top_level_pathways(self) -> List[Dict[str, Any]]:
        """Extract top-level pathways (safe, validated)"""
        url = f"{self.base_url}/data/pathways/top/{self.species_id}"

        logger.info(f"Fetching top-level pathways from: {url}")

        try:
            response = self._make_request(url)
            data = response.json()

            # Validate each pathway
            validated_pathways = []

            for item in data:
                try:
                    # Validate with pydantic
                    pathway = ReactomePathway(**item)

                    # Convert to dict and extract relevant fields
                    validated_pathways.append({
                        'identifier': pathway.stId,
                        'name': pathway.displayName,
                        'database_id': pathway.dbId,
                        'entity_type': 'pathway',
                        'source_database': 'Reactome',
                        'confidence_score': 0.9,
                        'evidence_strength': 'expert_curated',
                        'metadata': {
                            'schema_class': pathway.schemaClass,
                            'species': [s.displayName for s in pathway.species] if pathway.species else []
                        }
                    })

                except Exception as e:
                    logger.warning(f"Skipping invalid pathway: {e}")
                    self.stats['validations_failed'] += 1
                    continue

            logger.info(f"Validated {len(validated_pathways)}/{len(data)} pathways")
            return validated_pathways

        except Exception as e:
            logger.error(f"Error fetching top-level pathways: {e}")
            raise

    def _extract_all_pathways(self) -> List[Dict[str, Any]]:
        """Extract all pathways using hierarchy (safe, validated)"""
        url = f"{self.base_url}/data/eventsHierarchy/HSA"

        logger.info(f"Fetching pathway hierarchy from: {url}")

        try:
            response = self._make_request(url)
            data = response.json()

            # Flatten hierarchy with validation
            pathways = []

            def traverse(events: List[Dict[str, Any]]):
                """Recursively traverse hierarchy with validation"""
                for item in events:
                    try:
                        # Validate event
                        event = ReactomeEvent(**item)

                        # Only include pathways (not reactions)
                        if event.schemaClass == 'Pathway':
                            pathways.append({
                                'identifier': event.stId,
                                'name': event.displayName,
                                'database_id': event.dbId,
                                'entity_type': 'pathway',
                                'source_database': 'Reactome',
                                'confidence_score': 0.9,
                                'evidence_strength': 'expert_curated',
                                'metadata': {
                                    'schema_class': event.schemaClass,
                                    'species': [s.displayName for s in event.species] if event.species else []
                                }
                            })

                        # Traverse children
                        if event.children:
                            traverse([c.model_dump() for c in event.children])

                    except Exception as e:
                        logger.warning(f"Skipping invalid event: {e}")
                        self.stats['validations_failed'] += 1
                        continue

            traverse(data)
            logger.info(f"Extracted {len(pathways)} pathways from hierarchy")
            return pathways

        except Exception as e:
            logger.error(f"Error fetching pathway hierarchy: {e}")
            raise


def test_fixed_extractor():
    """Test the fixed extractor"""
    extractor = ReactomeExtractorFixed()

    # Test top-level extraction
    pathways = extractor.extract_pathways(max_pathways=50, top_level_only=True)

    print(f"\n✓ Extracted {len(pathways)} pathways")
    print(f"\nSample pathways:")
    for pathway in pathways[:3]:
        print(f"  - {pathway['name']} [{pathway['identifier']}]")

    # Print statistics
    extractor.print_stats()

    return pathways


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    test_fixed_extractor()
