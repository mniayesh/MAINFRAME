"""
Mechanisms Extractors

Extract mechanisms, processes, and pathways from:
- Gene Ontology (GO)
- Reactome
- KEGG

Focus on architectural primitives, not exhaustive data.
"""

import json
import xml.etree.ElementTree as ET
from typing import Dict, List, Any, Optional
from .base import BaseExtractor, retry_with_backoff
import requests


class GOExtractor(BaseExtractor):
    """
    Extract mechanisms and processes from Gene Ontology.

    Focuses on:
    - Biological processes with computational relevance
    - Molecular functions (catalysis, binding, gating)
    - Hierarchical relationships
    """

    def __init__(self, **kwargs):
        """Initialize GO extractor with rate limiting."""
        super().__init__(
            rate_limit_calls=10,  # Conservative limit
            rate_limit_period=1.0,
            **kwargs
        )
        self.base_url = "http://api.geneontology.org/api"

    def extract(
        self,
        aspect: str = None,
        focus_terms: List[str] = None,
        max_terms: int = 500
    ) -> List[Dict[str, Any]]:
        """
        Extract GO terms.

        Args:
            aspect: Filter by aspect ('biological_process', 'molecular_function', 'cellular_component')
            focus_terms: List of specific GO IDs to extract (e.g., ['GO:0006915'])
            max_terms: Maximum number of terms to extract

        Returns:
            List of GO term dictionaries
        """
        self.logger.info("Starting GO extraction...")

        if focus_terms:
            return self._extract_specific_terms(focus_terms)
        else:
            return self._extract_by_aspect(aspect, max_terms)

    def _extract_specific_terms(self, go_ids: List[str]) -> List[Dict[str, Any]]:
        """Extract specific GO terms by ID."""
        results = []

        for go_id in go_ids:
            self.logger.info(f"Extracting {go_id}...")

            try:
                term_data = self.get_term(go_id)
                if term_data:
                    results.append(term_data)
                    self.stats['items_extracted'] += 1

            except Exception as e:
                self.logger.error(f"Error extracting {go_id}: {str(e)}")

        return results

    def _extract_by_aspect(self, aspect: str = None, max_terms: int = 500) -> List[Dict[str, Any]]:
        """
        Extract GO terms by searching and filtering.

        Note: GO API doesn't have a simple 'list all terms' endpoint,
        so we use the bioentity search or download OBO file.
        """
        self.logger.info("Downloading GO OBO file for bulk extraction...")

        # Download OBO file (more efficient than API for bulk extraction)
        obo_url = "http://purl.obolibrary.org/obo/go.obo"

        try:
            response = self.make_request(obo_url, use_cache=True)
            obo_content = response.text

            # Parse OBO file
            terms = self._parse_obo(obo_content, aspect, max_terms)

            self.stats['items_extracted'] = len(terms)
            return terms

        except Exception as e:
            self.logger.error(f"Error downloading OBO file: {str(e)}")
            return []

    def get_term(self, go_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a GO term.

        Args:
            go_id: GO identifier (e.g., 'GO:0006915')

        Returns:
            Dictionary with term information
        """
        url = f"{self.base_url}/bioentity/function/{go_id}"

        try:
            data = self.get_json(url)

            return self._transform_term(data)

        except Exception as e:
            self.logger.error(f"Error fetching {go_id}: {str(e)}")
            return None

    def get_term_relationships(self, go_id: str, relationship_type: str = 'subterms') -> List[Dict[str, Any]]:
        """
        Get hierarchical relationships for a GO term.

        Args:
            go_id: GO identifier
            relationship_type: 'subterms' (children) or 'superterms' (parents)

        Returns:
            List of related terms
        """
        url = f"{self.base_url}/bioentity/function/{go_id}/{relationship_type}"

        try:
            data = self.get_json(url)
            return data.get('associations', [])

        except Exception as e:
            self.logger.error(f"Error fetching relationships for {go_id}: {str(e)}")
            return []

    def _parse_obo(self, obo_content: str, aspect: str = None, max_terms: int = 500) -> List[Dict[str, Any]]:
        """
        Parse OBO format file.

        Args:
            obo_content: OBO file content as string
            aspect: Filter by namespace
            max_terms: Maximum terms to extract

        Returns:
            List of parsed GO terms
        """
        terms = []
        current_term = {}
        in_term = False

        aspect_map = {
            'biological_process': 'biological_process',
            'molecular_function': 'molecular_function',
            'cellular_component': 'cellular_component'
        }

        for line in obo_content.split('\n'):
            line = line.strip()

            if line == '[Term]':
                if current_term:
                    # Check if term matches aspect filter
                    if aspect is None or current_term.get('namespace') == aspect_map.get(aspect):
                        terms.append(self._transform_obo_term(current_term))

                    if len(terms) >= max_terms:
                        break

                current_term = {}
                in_term = True

            elif in_term and line:
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip()

                    if key == 'id':
                        current_term['id'] = value
                    elif key == 'name':
                        current_term['name'] = value
                    elif key == 'namespace':
                        current_term['namespace'] = value
                    elif key == 'def':
                        # Definition is in quotes
                        if '"' in value:
                            current_term['definition'] = value.split('"')[1]
                    elif key == 'is_a':
                        if 'parents' not in current_term:
                            current_term['parents'] = []
                        parent_id = value.split('!')[0].strip()
                        current_term['parents'].append(parent_id)
                    elif key == 'relationship':
                        if 'relationships' not in current_term:
                            current_term['relationships'] = []
                        current_term['relationships'].append(value)

        # Don't forget the last term
        if current_term and (aspect is None or current_term.get('namespace') == aspect_map.get(aspect)):
            if len(terms) < max_terms:
                terms.append(self._transform_obo_term(current_term))

        self.logger.info(f"Parsed {len(terms)} GO terms from OBO file")
        return terms

    def _transform_obo_term(self, obo_term: Dict) -> Dict[str, Any]:
        """Transform OBO term to standard format."""
        # Map namespace to process category
        category_map = {
            'biological_process': 'process',
            'molecular_function': 'mechanism',
            'cellular_component': 'structure'
        }

        return {
            'identifier': obo_term.get('id'),
            'name': obo_term.get('name'),
            'description': obo_term.get('definition', ''),
            'entity_type': category_map.get(obo_term.get('namespace'), 'process'),
            'namespace': obo_term.get('namespace'),
            'parent_terms': obo_term.get('parents', []),
            'relationships': obo_term.get('relationships', []),
            'source_database': 'GO',
            'confidence_score': 0.95,  # GO is highly curated
            'evidence_strength': 'experimental'
        }

    def _transform_term(self, api_data: Dict) -> Dict[str, Any]:
        """Transform API response to standard format."""
        return {
            'identifier': api_data.get('id'),
            'name': api_data.get('label'),
            'description': api_data.get('definition'),
            'entity_type': 'process' if 'process' in api_data.get('category', '') else 'mechanism',
            'source_database': 'GO',
            'confidence_score': 0.95,
            'evidence_strength': 'experimental',
            'metadata': api_data
        }


class ReactomeExtractor(BaseExtractor):
    """
    Extract pathways and reactions from Reactome.

    Focuses on:
    - Signaling pathways
    - Metabolic pathways
    - Regulatory networks
    - Reaction mechanisms
    """

    def __init__(self, **kwargs):
        """Initialize Reactome extractor."""
        super().__init__(
            rate_limit_calls=10,
            rate_limit_period=1.0,
            **kwargs
        )
        self.base_url = "https://reactome.org/ContentService"

    def extract(
        self,
        species: str = '9606',  # Homo sapiens
        top_level_only: bool = False,
        pathway_categories: List[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Extract Reactome pathways.

        Args:
            species: NCBI taxonomy ID (9606 = Homo sapiens)
            top_level_only: Only extract top-level pathways
            pathway_categories: Filter by categories (e.g., ['Signal Transduction'])

        Returns:
            List of pathway dictionaries
        """
        self.logger.info(f"Starting Reactome extraction for species {species}...")

        # Get pathway hierarchy
        pathways = self.get_pathway_hierarchy(species)

        if top_level_only:
            # Filter to only top-level
            pathways = [p for p in pathways if not p.get('hasEvent', [])]

        # Get detailed information for each pathway
        detailed_pathways = []
        for pathway in pathways[:500]:  # Limit to avoid excessive API calls
            pathway_id = pathway.get('stId')
            if pathway_id:
                details = self.get_pathway_details(pathway_id)
                if details:
                    detailed_pathways.append(details)
                    self.stats['items_extracted'] += 1

        return detailed_pathways

    def get_pathway_hierarchy(self, species: str = '9606') -> List[Dict[str, Any]]:
        """
        Get complete pathway hierarchy for a species.

        Args:
            species: NCBI taxonomy ID

        Returns:
            List of pathways in hierarchical structure
        """
        url = f"{self.base_url}/data/eventsHierarchy/{species}"

        try:
            data = self.get_json(url)

            # Flatten hierarchy
            return self._flatten_hierarchy(data)

        except Exception as e:
            self.logger.error(f"Error fetching pathway hierarchy: {str(e)}")
            return []

    def _flatten_hierarchy(self, hierarchy: List[Dict], parent_id: str = None) -> List[Dict]:
        """Recursively flatten pathway hierarchy."""
        flattened = []

        for item in hierarchy:
            pathway = {
                'stId': item.get('stId'),
                'displayName': item.get('displayName'),
                'type': item.get('type'),
                'species': item.get('species', [{}])[0].get('displayName') if item.get('species') else None,
                'parent_id': parent_id
            }
            flattened.append(pathway)

            # Recursively process children
            if 'children' in item:
                flattened.extend(
                    self._flatten_hierarchy(item['children'], item.get('stId'))
                )

        return flattened

    def get_pathway_details(self, pathway_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a pathway.

        Args:
            pathway_id: Reactome stable identifier (e.g., 'R-HSA-69278')

        Returns:
            Dictionary with pathway details
        """
        url = f"{self.base_url}/data/query/{pathway_id}"

        try:
            data = self.get_json(url)

            return self._transform_pathway(data)

        except Exception as e:
            self.logger.error(f"Error fetching pathway {pathway_id}: {str(e)}")
            return None

    def get_pathway_reactions(self, pathway_id: str) -> List[Dict[str, Any]]:
        """Get all reactions in a pathway."""
        url = f"{self.base_url}/data/pathway/{pathway_id}/containedEvents"

        try:
            data = self.get_json(url)
            return data

        except Exception as e:
            self.logger.error(f"Error fetching reactions for {pathway_id}: {str(e)}")
            return []

    def _transform_pathway(self, api_data: Dict) -> Dict[str, Any]:
        """Transform API response to standard format."""
        return {
            'identifier': api_data.get('stId'),
            'name': api_data.get('displayName'),
            'description': api_data.get('summation', [{}])[0].get('text', '') if api_data.get('summation') else '',
            'entity_type': 'pathway',
            'pathway_category': self._infer_category(api_data.get('displayName', '')),
            'source_database': 'Reactome',
            'confidence_score': 0.90,
            'evidence_strength': 'experimental',
            'metadata': {
                'doi': api_data.get('doi'),
                'species': api_data.get('species', [{}])[0].get('displayName'),
                'has_diagram': api_data.get('hasDiagram', False)
            }
        }

    def _infer_category(self, name: str) -> str:
        """Infer pathway category from name."""
        name_lower = name.lower()

        if any(term in name_lower for term in ['signal', 'signaling']):
            return 'signaling'
        elif any(term in name_lower for term in ['metabol', 'glycolysis', 'tca']):
            return 'metabolic'
        elif any(term in name_lower for term in ['transport', 'translocation']):
            return 'transport'
        elif any(term in name_lower for term in ['immune', 'inflammation']):
            return 'immune'
        else:
            return 'other'


class KEGGExtractor(BaseExtractor):
    """
    Extract pathways from KEGG.

    IMPORTANT: KEGG has strict rate limits (3 requests per second).

    Focuses on:
    - Metabolic pathways
    - Signaling pathways
    - Disease pathways
    """

    def __init__(self, **kwargs):
        """Initialize KEGG extractor with strict rate limiting."""
        super().__init__(
            rate_limit_calls=3,  # KEGG limit: 3 per second
            rate_limit_period=1.0,
            **kwargs
        )
        self.base_url = "https://rest.kegg.jp"

    def extract(
        self,
        organism: str = 'hsa',  # Homo sapiens
        pathway_types: List[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Extract KEGG pathways.

        Args:
            organism: KEGG organism code (hsa = human)
            pathway_types: Filter by pathway types

        Returns:
            List of pathway dictionaries
        """
        self.logger.info(f"Starting KEGG extraction for organism {organism}...")

        # Get list of pathways
        pathways = self.list_pathways(organism)

        # Get details for each pathway
        detailed_pathways = []
        for pathway in pathways[:300]:  # Limit due to rate limits
            pathway_id = pathway.get('id')
            if pathway_id:
                details = self.get_pathway_details(pathway_id)
                if details:
                    detailed_pathways.append(details)
                    self.stats['items_extracted'] += 1

        return detailed_pathways

    def list_pathways(self, organism: str = 'hsa') -> List[Dict[str, Any]]:
        """
        List all pathways for an organism.

        Args:
            organism: KEGG organism code

        Returns:
            List of pathway identifiers and names
        """
        url = f"{self.base_url}/list/pathway/{organism}"

        try:
            response = self.make_request(url)
            text = response.text

            pathways = []
            for line in text.strip().split('\n'):
                if '\t' in line:
                    pathway_id, pathway_name = line.split('\t', 1)
                    pathways.append({
                        'id': pathway_id,
                        'name': pathway_name
                    })

            self.logger.info(f"Found {len(pathways)} pathways")
            return pathways

        except Exception as e:
            self.logger.error(f"Error listing pathways: {str(e)}")
            return []

    def get_pathway_details(self, pathway_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a pathway.

        Args:
            pathway_id: KEGG pathway ID (e.g., 'path:hsa00010')

        Returns:
            Dictionary with pathway details
        """
        url = f"{self.base_url}/get/{pathway_id}"

        try:
            response = self.make_request(url)
            text = response.text

            # Parse KEGG flat file format
            parsed = self._parse_kegg_entry(text)

            return self._transform_pathway(parsed)

        except Exception as e:
            self.logger.error(f"Error fetching pathway {pathway_id}: {str(e)}")
            return None

    def _parse_kegg_entry(self, text: str) -> Dict[str, Any]:
        """Parse KEGG flat file format."""
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

    def _transform_pathway(self, parsed_entry: Dict) -> Dict[str, Any]:
        """Transform parsed KEGG entry to standard format."""
        pathway_id = parsed_entry.get('ENTRY', '').split()[0] if parsed_entry.get('ENTRY') else ''

        return {
            'identifier': pathway_id,
            'name': parsed_entry.get('NAME', ''),
            'description': parsed_entry.get('DESCRIPTION', ''),
            'entity_type': 'pathway',
            'pathway_category': self._infer_kegg_category(parsed_entry.get('CLASS', '')),
            'source_database': 'KEGG',
            'confidence_score': 0.85,
            'evidence_strength': 'computational',
            'metadata': {
                'organism': parsed_entry.get('ORGANISM', ''),
                'class': parsed_entry.get('CLASS', ''),
                'pathway_map': parsed_entry.get('PATHWAY_MAP', '')
            }
        }

    def _infer_kegg_category(self, class_info: str) -> str:
        """Infer pathway category from CLASS field."""
        if 'Metabolism' in class_info:
            return 'metabolic'
        elif 'Signal' in class_info:
            return 'signaling'
        elif 'Disease' in class_info:
            return 'disease'
        else:
            return 'other'
