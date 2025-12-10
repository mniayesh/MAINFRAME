"""
Fixed KEGG Extractor with Pydantic Validation

Improves on the original KEGG extractor by adding:
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


# ===== Pydantic Models for KEGG API =====

class KEGGPathwayListEntry(BaseModel):
    """Validated KEGG pathway list entry"""
    id: str
    name: str

    @field_validator('id', mode='before')
    @classmethod
    def validate_id(cls, v):
        """Ensure ID is a string"""
        if v is None:
            return "unknown"
        return str(v).strip()

    @field_validator('name', mode='before')
    @classmethod
    def validate_name(cls, v):
        """Ensure name is a string"""
        if v is None:
            return "Unknown pathway"
        return str(v).strip()


class KEGGPathway(BaseModel):
    """Validated KEGG pathway with flexible field handling"""
    identifier: str
    name: str
    description: Optional[str] = ""
    pathway_class: Optional[str] = None
    organism: Optional[str] = None
    disease: Optional[str] = None
    genes: Optional[List[str]] = []
    compounds: Optional[List[str]] = []

    @field_validator('identifier', mode='before')
    @classmethod
    def validate_identifier(cls, v):
        if v is None or str(v).strip() == "":
            return "unknown"
        return str(v).strip()

    @field_validator('name', mode='before')
    @classmethod
    def validate_name(cls, v):
        if v is None or str(v).strip() == "":
            return "Unknown pathway"
        return str(v).strip()

    @field_validator('genes', mode='before')
    @classmethod
    def validate_genes(cls, v):
        """Convert gene list to array"""
        if v is None:
            return []
        if isinstance(v, list):
            return v
        if isinstance(v, str):
            # Parse from KEGG format
            return [g.strip() for g in v.split('\n') if g.strip()]
        return []


class KEGGExtractorFixed(EnhancedBaseExtractor):
    """
    Fixed KEGG extractor with full pydantic validation

    Prevents parser errors by validating all API responses.
    Maintains strict rate limiting (3 requests/second).
    """

    def __init__(self):
        super().__init__(
            base_url="https://rest.kegg.jp",
            rate_limit=3,  # KEGG strict limit: 3 req/sec
            max_retries=3,
            timeout=30
        )

    def extract_pathways(
        self,
        organism: str = 'hsa',
        max_pathways: int = 500
    ) -> List[Dict[str, Any]]:
        """
        Extract KEGG pathways with validation

        Args:
            organism: KEGG organism code (hsa = human)
            max_pathways: Maximum number of pathways to extract

        Returns:
            List of validated pathway dictionaries
        """
        logger.info(f"Starting KEGG extraction for organism {organism}...")
        console.print(f"[cyan]Extracting KEGG pathways for {organism}...[/cyan]")

        pathways = []

        try:
            # Step 1: List all pathways
            pathway_list = self._list_pathways(organism)
            logger.info(f"Found {len(pathway_list)} pathways in KEGG")

            # Step 2: Get details for each pathway (limited by max_pathways)
            for i, pathway_entry in enumerate(pathway_list[:max_pathways]):
                if i % 50 == 0:
                    console.print(f"[cyan]Progress: {i}/{min(len(pathway_list), max_pathways)}[/cyan]")

                try:
                    pathway_id = pathway_entry.id
                    details = self._get_pathway_details(pathway_id)

                    if details:
                        pathways.append(details)

                except Exception as e:
                    logger.warning(f"Skipping pathway {pathway_entry.id}: {e}")
                    self.stats['validations_failed'] += 1
                    continue

            logger.info(f"Successfully extracted {len(pathways)} KEGG pathways")

            console.print(Panel(
                f"[bold green]Successfully extracted {len(pathways)} pathways[/bold green]",
                title="KEGG Extraction Complete",
                border_style="green"
            ))

        except Exception as e:
            logger.error(f"Error during extraction: {e}")
            console.print(Panel(
                f"[bold red]Extraction failed: {e}[/bold red]",
                title="KEGG Extraction Error",
                border_style="red"
            ))

        return pathways

    def _list_pathways(self, organism: str = 'hsa') -> List[KEGGPathwayListEntry]:
        """
        List all pathways for an organism with validation

        Args:
            organism: KEGG organism code

        Returns:
            List of validated pathway list entries
        """
        url = f"{self.base_url}/list/pathway/{organism}"

        try:
            response = self._make_request(url)
            text = response.text

            pathways = []
            for line in text.strip().split('\n'):
                if '\t' in line:
                    pathway_id, pathway_name = line.split('\t', 1)

                    # Validate with pydantic
                    try:
                        entry = KEGGPathwayListEntry(
                            id=pathway_id.strip(),
                            name=pathway_name.strip()
                        )
                        pathways.append(entry)
                    except Exception as e:
                        logger.warning(f"Invalid pathway entry: {e}")
                        self.stats['validations_failed'] += 1
                        continue

            logger.info(f"Listed {len(pathways)} pathways")
            return pathways

        except Exception as e:
            logger.error(f"Error listing pathways: {e}")
            self.stats['errors'] += 1
            return []

    def _get_pathway_details(self, pathway_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a pathway with validation

        Args:
            pathway_id: KEGG pathway ID (e.g., 'path:hsa00010')

        Returns:
            Validated pathway dictionary
        """
        url = f"{self.base_url}/get/{pathway_id}"

        try:
            response = self._make_request(url)
            text = response.text

            # Parse KEGG flat file format
            parsed = self._parse_kegg_entry(text)

            # Validate with pydantic
            pathway = KEGGPathway(
                identifier=parsed.get('ENTRY', '').split()[0] if parsed.get('ENTRY') else pathway_id,
                name=parsed.get('NAME', 'Unknown'),
                description=parsed.get('DESCRIPTION', ''),
                pathway_class=parsed.get('CLASS', None),
                organism=parsed.get('ORGANISM', None),
                disease=parsed.get('DISEASE', None),
                genes=self._parse_gene_list(parsed.get('GENE', '')),
                compounds=self._parse_compound_list(parsed.get('COMPOUND', ''))
            )

            # Transform to standard entity format
            return {
                'identifier': pathway.identifier,
                'name': pathway.name,
                'description': pathway.description,
                'entity_type': 'pathway',
                'source_database': 'KEGG',
                'confidence_score': 0.9,
                'evidence_strength': 'curated',
                'metadata': {
                    'pathway_class': pathway.pathway_class,
                    'organism': pathway.organism,
                    'disease': pathway.disease,
                    'gene_count': len(pathway.genes) if pathway.genes else 0,
                    'compound_count': len(pathway.compounds) if pathway.compounds else 0
                }
            }

        except Exception as e:
            logger.error(f"Error fetching pathway {pathway_id}: {e}")
            self.stats['errors'] += 1
            return None

    def _parse_kegg_entry(self, text: str) -> Dict[str, Any]:
        """Parse KEGG flat file format"""
        entry = {}
        current_key = None
        current_value = []

        for line in text.split('\n'):
            if line.startswith(' '):
                # Continuation of previous field
                current_value.append(line.strip())
            else:
                # New field
                if current_key:
                    entry[current_key] = '\n'.join(current_value)

                if line.strip():
                    parts = line.split(None, 1)
                    if len(parts) == 2:
                        current_key = parts[0]
                        current_value = [parts[1]]
                    else:
                        current_key = parts[0]
                        current_value = []

        # Don't forget last field
        if current_key:
            entry[current_key] = '\n'.join(current_value)

        return entry

    def _parse_gene_list(self, gene_text: str) -> List[str]:
        """Parse KEGG gene list"""
        if not gene_text:
            return []

        genes = []
        for line in gene_text.split('\n'):
            if line.strip():
                # Gene format: "1234 gene_name; description"
                parts = line.strip().split(None, 1)
                if parts:
                    genes.append(parts[0])

        return genes

    def _parse_compound_list(self, compound_text: str) -> List[str]:
        """Parse KEGG compound list"""
        if not compound_text:
            return []

        compounds = []
        for line in compound_text.split('\n'):
            if line.strip():
                # Compound format: "C00001 compound_name"
                parts = line.strip().split(None, 1)
                if parts:
                    compounds.append(parts[0])

        return compounds


def test_fixed_extractor():
    """Test the fixed KEGG extractor"""
    extractor = KEGGExtractorFixed()

    # Test extraction
    pathways = extractor.extract_pathways(organism='hsa', max_pathways=100)

    print(f"\n✓ Extracted {len(pathways)} pathways")
    print(f"\nSample pathways:")
    for pathway in pathways[:5]:
        print(f"  - {pathway['name']} [{pathway['identifier']}]")

    # Print statistics
    extractor.print_stats()

    return pathways


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    test_fixed_extractor()
