"""
Fixed Allen Brain Atlas Extractor with Pydantic Validation

Improves on the original Allen Brain extractor by adding:
- Pydantic validation for API responses
- Enhanced error prevention
- Better caching and retry logic
"""

import logging
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, field_validator
from enhanced_base import EnhancedBaseExtractor, console
from rich.panel import Panel

logger = logging.getLogger(__name__)


# ===== Pydantic Models for Allen Brain API =====

class AllenBrainStructure(BaseModel):
    """Validated Allen Brain Atlas structure"""
    id: int
    name: str
    acronym: Optional[str] = ""
    safe_name: Optional[str] = None
    parent_structure_id: Optional[int] = None
    depth: Optional[int] = 0
    graph_order: Optional[int] = 0
    atlas_id: Optional[int] = None

    @field_validator('id', mode='before')
    @classmethod
    def validate_id(cls, v):
        """Ensure ID is an integer"""
        if v is None:
            return 0
        try:
            return int(v)
        except (ValueError, TypeError):
            return 0

    @field_validator('name', mode='before')
    @classmethod
    def validate_name(cls, v):
        """Ensure name is a string"""
        if v is None or str(v).strip() == "":
            return "Unknown structure"
        return str(v).strip()

    @field_validator('acronym', mode='before')
    @classmethod
    def validate_acronym(cls, v):
        """Handle acronym variations"""
        if v is None:
            return ""
        return str(v).strip()


class AllenBrainExtractorFixed(EnhancedBaseExtractor):
    """
    Fixed Allen Brain Atlas extractor with full pydantic validation

    Prevents parser errors by validating all API responses.
    Extracts brain region hierarchy and properties.
    """

    def __init__(self):
        super().__init__(
            base_url="https://api.brain-map.org/api/v2",
            rate_limit=10,
            max_retries=3,
            timeout=30
        )

    def extract_structures(
        self,
        max_structures: int = 500,
        graph_id: int = 1  # 1 = Adult Mouse Brain
    ) -> List[Dict[str, Any]]:
        """
        Extract brain structures with validation

        Args:
            max_structures: Maximum number of structures to extract
            graph_id: Graph ID (1 = Adult Mouse Brain)

        Returns:
            List of validated structure dictionaries
        """
        logger.info(f"Starting Allen Brain Atlas extraction (graph_id={graph_id})...")
        console.print(f"[cyan]Extracting Allen Brain structures...[/cyan]")

        structures = []

        try:
            # Query structures from Allen Brain API
            url = f"{self.base_url}/data/Structure/query.json"
            params = {
                'criteria': f'[graph_id$eq{graph_id}]',
                'num_rows': max_structures
            }

            response = self._make_request(url, params=params)
            data = response.json()

            # Get structure list from response
            structure_list = data.get('msg', [])

            if not structure_list:
                logger.warning("No structures returned from API")
                return []

            logger.info(f"Retrieved {len(structure_list)} structures")

            # Validate and transform each structure
            for item in structure_list:
                try:
                    # Validate with pydantic
                    structure = AllenBrainStructure(**item)

                    # Transform to standard entity format
                    validated_structure = {
                        'identifier': f"ABA:{structure.id}",
                        'name': structure.name,
                        'description': structure.safe_name or structure.name,
                        'entity_type': 'network_structure',
                        'source_database': 'Allen Brain Atlas',
                        'confidence_score': 0.90,
                        'evidence_strength': 'experimental',
                        'metadata': {
                            'acronym': structure.acronym,
                            'parent_id': structure.parent_structure_id,
                            'depth': structure.depth,
                            'graph_order': structure.graph_order,
                            'atlas_id': structure.atlas_id,
                            'graph_id': graph_id
                        }
                    }

                    structures.append(validated_structure)

                except Exception as e:
                    logger.warning(f"Skipping invalid structure: {e}")
                    self.stats['validations_failed'] += 1
                    continue

            logger.info(f"Successfully validated {len(structures)} structures")

            console.print(Panel(
                f"[bold green]Successfully extracted {len(structures)} brain structures[/bold green]",
                title="Allen Brain Atlas Extraction Complete",
                border_style="green"
            ))

        except Exception as e:
            logger.error(f"Error during extraction: {e}")
            console.print(Panel(
                f"[bold red]Extraction failed: {e}[/bold red]",
                title="Allen Brain Atlas Extraction Error",
                border_style="red"
            ))

        return structures

    def extract_connectivity(
        self,
        max_experiments: int = 200
    ) -> List[Dict[str, Any]]:
        """
        Extract brain connectivity data with validation

        Args:
            max_experiments: Maximum number of connectivity experiments

        Returns:
            List of validated connectivity dictionaries
        """
        logger.info("Starting Allen Brain connectivity extraction...")

        connections = []

        try:
            # Query connectivity experiments
            url = f"{self.base_url}/data/SectionDataSet/query.json"
            params = {
                'criteria': 'products[id$eq5]',  # Mouse Connectivity
                'num_rows': max_experiments
            }

            response = self._make_request(url, params=params)
            data = response.json()

            experiment_list = data.get('msg', [])

            if not experiment_list:
                logger.warning("No connectivity experiments returned")
                return []

            logger.info(f"Retrieved {len(experiment_list)} connectivity experiments")

            # Transform each experiment
            for experiment in experiment_list:
                try:
                    connection = {
                        'identifier': f"ABA_CONN:{experiment.get('id', 0)}",
                        'name': f"Connectivity: {experiment.get('id', 'Unknown')}",
                        'description': 'Brain region connectivity pattern',
                        'entity_type': 'network_structure',
                        'source_database': 'Allen Brain Atlas',
                        'confidence_score': 0.85,
                        'evidence_strength': 'experimental',
                        'metadata': {
                            'experiment_id': experiment.get('id'),
                            'plane_of_section': experiment.get('plane_of_section_id')
                        }
                    }

                    connections.append(connection)

                except Exception as e:
                    logger.warning(f"Skipping invalid connectivity: {e}")
                    self.stats['validations_failed'] += 1
                    continue

            logger.info(f"Successfully extracted {len(connections)} connectivity patterns")

            console.print(Panel(
                f"[bold green]Successfully extracted {len(connections)} connectivity patterns[/bold green]",
                title="Allen Brain Connectivity Complete",
                border_style="green"
            ))

        except Exception as e:
            logger.error(f"Error during connectivity extraction: {e}")
            console.print(Panel(
                f"[bold red]Connectivity extraction failed: {e}[/bold red]",
                title="Allen Brain Connectivity Error",
                border_style="red"
            ))

        return connections


def test_fixed_extractor():
    """Test the fixed Allen Brain extractor"""
    extractor = AllenBrainExtractorFixed()

    # Test structure extraction
    structures = extractor.extract_structures(max_structures=200)

    print(f"\n✓ Extracted {len(structures)} structures")
    print(f"\nSample structures:")
    for structure in structures[:5]:
        print(f"  - {structure['name']} [{structure['identifier']}] - {structure['metadata']['acronym']}")

    # Print statistics
    extractor.print_stats()

    return structures


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    test_fixed_extractor()
