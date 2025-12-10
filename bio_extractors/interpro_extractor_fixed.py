"""
Fixed InterPro Extractor with Pydantic Validation

Fixes the same 'str'.get() error that affected Reactome by validating
API responses before accessing nested fields.
"""

import logging
from typing import Dict, Any, List, Optional, Union
from pydantic import BaseModel, Field, field_validator
from enhanced_base import EnhancedBaseExtractor, console
from rich.panel import Panel

logger = logging.getLogger(__name__)


# ===== Pydantic Models for InterPro API =====

class InterProMetadata(BaseModel):
    """Validated InterPro metadata with flexible field handling"""
    accession: Optional[str] = None
    name: Optional[Union[str, Dict[str, Any]]] = None
    source_database: Optional[str] = None
    type: Optional[str] = None
    go_terms: Optional[List[Dict[str, Any]]] = None

    @field_validator('name', mode='before')
    @classmethod
    def validate_name(cls, v):
        """
        Handle name variations:
        - Can be a string (most common)
        - Can be a dict with 'name' key
        - Can be None
        """
        if v is None:
            return None
        if isinstance(v, str):
            return v
        if isinstance(v, dict):
            # Extract 'name' field from dict
            return v.get('name', str(v))
        return str(v)


class InterProEntry(BaseModel):
    """Validated InterPro entry with flexible metadata handling"""
    metadata: Union[InterProMetadata, Dict[str, Any]]

    @field_validator('metadata', mode='before')
    @classmethod
    def validate_metadata(cls, v):
        """
        Handle metadata variations:
        - Can be a dict (normal case)
        - Can be a string (ERROR CASE - convert to dict)
        - Can be None (ERROR CASE - convert to empty dict)
        """
        if v is None:
            logger.warning("Metadata is None, converting to empty dict")
            return {}

        if isinstance(v, str):
            logger.warning(f"Metadata is string: '{v}', converting to dict")
            return {'name': v}

        if isinstance(v, dict):
            return v

        logger.error(f"Unexpected metadata type: {type(v)}, converting to empty dict")
        return {}


class InterProExtractorFixed(EnhancedBaseExtractor):
    """
    Fixed InterPro extractor with full pydantic validation

    Prevents parser errors by validating all API responses.
    """

    def __init__(self):
        super().__init__(
            base_url="https://www.ebi.ac.uk/interpro/api",
            rate_limit=0,
            max_retries=3,
            timeout=30
        )

    def extract_entries(
        self,
        entry_type: str = "domain",
        max_entries: int = 500,
        page_size: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Extract InterPro entries with validation

        Args:
            entry_type: Type of entry (domain, family, etc.)
            max_entries: Maximum number of entries to extract
            page_size: Number of entries per page

        Returns:
            List of validated entry dictionaries
        """
        logger.info(f"Starting InterPro extraction ({entry_type})...")

        entries = []
        page = 1

        try:
            while len(entries) < max_entries:
                logger.info(f"Fetching page {page}...")

                url = f"{self.base_url}/entry/interpro?type={entry_type}&page_size={page_size}&page={page}"

                try:
                    response = self._make_request(url)
                    data = response.json()

                    # Get results from response
                    results = data.get('results', [])

                    if not results:
                        logger.info("No more results")
                        break

                    logger.info(f"Page {page}: {len(results)} items")

                    # Validate each entry
                    for item in results:
                        try:
                            # Validate with pydantic
                            entry = InterProEntry(**item)

                            # Extract metadata safely
                            metadata = entry.metadata if isinstance(entry.metadata, dict) else entry.metadata.model_dump()

                            # Build validated entry
                            validated_entry = {
                                'identifier': metadata.get('accession', f'unknown_{len(entries)}'),
                                'name': self._extract_name(metadata),
                                'entity_type': 'enzyme' if entry_type == 'domain' else entry_type,
                                'source_database': 'InterPro',
                                'confidence_score': 0.9,
                                'evidence_strength': 'computational',
                                'metadata': {
                                    'type': metadata.get('type', entry_type),
                                    'source_db': metadata.get('source_database', 'InterPro'),
                                    'go_terms': metadata.get('go_terms', [])
                                }
                            }

                            entries.append(validated_entry)

                            if len(entries) >= max_entries:
                                break

                        except Exception as e:
                            logger.warning(f"Skipping invalid entry: {e}")
                            self.stats['validations_failed'] += 1
                            continue

                    page += 1

                except Exception as e:
                    logger.error(f"Error fetching page {page}: {e}")
                    break

            logger.info(f"Retrieved {len(entries)} InterPro entries")

            console.print(Panel(
                f"[bold green]Successfully extracted {len(entries)} entries[/bold green]",
                title="InterPro Extraction Complete",
                border_style="green"
            ))

        except Exception as e:
            logger.error(f"Error during extraction: {e}")
            console.print(Panel(
                f"[bold red]Extraction failed: {e}[/bold red]",
                title="InterPro Extraction Error",
                border_style="red"
            ))

        return entries

    def _extract_name(self, metadata: Dict[str, Any]) -> str:
        """Safely extract name from metadata"""
        name = metadata.get('name', metadata.get('accession', 'Unknown'))

        # If name is still a dict, extract nested name
        if isinstance(name, dict):
            name = name.get('name', name.get('short', str(name)))

        return str(name)


def test_fixed_extractor():
    """Test the fixed extractor"""
    extractor = InterProExtractorFixed()

    # Test extraction
    entries = extractor.extract_entries(entry_type='domain', max_entries=100, page_size=20)

    print(f"\n✓ Extracted {len(entries)} entries")
    print(f"\nSample entries:")
    for entry in entries[:5]:
        print(f"  - {entry['name']} [{entry['identifier']}]")

    # Print statistics
    extractor.print_stats()

    return entries


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    test_fixed_extractor()
