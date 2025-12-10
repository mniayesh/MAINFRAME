"""
Neuroscience Extractors

Extract neuroscience data from:
- Allen Brain Atlas (brain regions, connectivity, gene expression)
- NeuroMorpho (neuronal morphologies and cell types)
- Cell Ontology (cell type classifications)

Focus on architectural patterns and cell type templates.
"""

import json
import requests
from typing import Dict, List, Any, Optional
from .base import BaseExtractor


class AllenBrainExtractor(BaseExtractor):
    """
    Extract brain architecture data from Allen Brain Atlas.

    Focuses on:
    - Brain region hierarchy
    - Connectivity patterns
    - Cell type definitions
    - Network structures
    """

    def __init__(self, **kwargs):
        """Initialize Allen Brain Atlas extractor."""
        super().__init__(
            rate_limit_calls=10,
            rate_limit_period=1.0,
            **kwargs
        )
        self.base_url = "https://api.brain-map.org/api/v2"

    def extract(
        self,
        data_type: str = 'structure',
        species: str = 'mouse'
    ) -> List[Dict[str, Any]]:
        """
        Extract Allen Brain Atlas data.

        Args:
            data_type: Type of data ('structure', 'connectivity', 'expression')
            species: Species ('mouse', 'human')

        Returns:
            List of extracted entities
        """
        self.logger.info(f"Starting Allen Brain Atlas extraction ({data_type})...")

        if data_type == 'structure':
            return self.extract_brain_structures()
        elif data_type == 'connectivity':
            return self.extract_connectivity()
        else:
            self.logger.warning(f"Unknown data type: {data_type}")
            return []

    def extract_brain_structures(self) -> List[Dict[str, Any]]:
        """
        Extract brain region hierarchy and properties.

        Returns:
            List of brain structure dictionaries
        """
        # Get structure ontology
        url = f"{self.base_url}/data/Structure/query.json"
        params = {
            'criteria': '[graph_id$eq1]',  # Adult Mouse Brain
            'num_rows': 2000
        }

        try:
            data = self.get_json(url, params=params)

            structures = []
            for structure in data.get('msg', []):
                transformed = self._transform_structure(structure)
                structures.append(transformed)
                self.stats['items_extracted'] += 1

            self.logger.info(f"Extracted {len(structures)} brain structures")
            return structures

        except Exception as e:
            self.logger.error(f"Error extracting brain structures: {str(e)}")
            return []

    def extract_connectivity(self) -> List[Dict[str, Any]]:
        """
        Extract brain connectivity data.

        Returns:
            List of connectivity patterns
        """
        # Get projection experiments
        url = f"{self.base_url}/data/SectionDataSet/query.json"
        params = {
            'criteria': 'products[id$eq5]',  # Mouse Connectivity
            'num_rows': 500
        }

        try:
            data = self.get_json(url, params=params)

            connections = []
            for experiment in data.get('msg', []):
                # Extract projection information
                connection = self._transform_connectivity(experiment)
                if connection:
                    connections.append(connection)
                    self.stats['items_extracted'] += 1

            self.logger.info(f"Extracted {len(connections)} connectivity patterns")
            return connections

        except Exception as e:
            self.logger.error(f"Error extracting connectivity: {str(e)}")
            return []

    def _transform_structure(self, structure: Dict) -> Dict[str, Any]:
        """Transform brain structure to standard format."""
        return {
            'identifier': f"ABA:{structure.get('id')}",
            'name': structure.get('name'),
            'description': structure.get('safe_name'),
            'entity_type': 'network_structure',
            'anatomical_location': structure.get('name'),
            'source_database': 'Allen Brain Atlas',
            'confidence_score': 0.90,
            'evidence_strength': 'experimental',
            'metadata': {
                'acronym': structure.get('acronym'),
                'parent_id': structure.get('parent_structure_id'),
                'depth': structure.get('depth'),
                'graph_order': structure.get('graph_order'),
                'atlas_id': structure.get('atlas_id')
            }
        }

    def _transform_connectivity(self, experiment: Dict) -> Optional[Dict[str, Any]]:
        """Transform connectivity experiment to standard format."""
        return {
            'identifier': f"ABA_CONN:{experiment.get('id')}",
            'name': f"Connectivity: {experiment.get('id')}",
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


class NeuroMorphoExtractor(BaseExtractor):
    """
    Extract neuronal morphology data from NeuroMorpho.

    Focuses on:
    - Cell type morphological classes
    - Neuron architectures
    - Dendritic and axonal patterns
    """

    def __init__(self, **kwargs):
        """Initialize NeuroMorpho extractor."""
        super().__init__(
            rate_limit_calls=10,
            rate_limit_period=1.0,
            **kwargs
        )
        self.base_url = "http://neuromorpho.org/api"

    def extract(
        self,
        cell_types: List[str] = None,
        brain_regions: List[str] = None,
        max_neurons: int = 500
    ) -> List[Dict[str, Any]]:
        """
        Extract neuronal morphology data.

        Args:
            cell_types: Filter by cell types (e.g., ['pyramidal', 'interneuron'])
            brain_regions: Filter by brain regions
            max_neurons: Maximum number of neurons to extract

        Returns:
            List of neuron dictionaries
        """
        self.logger.info("Starting NeuroMorpho extraction...")

        # Get neuron metadata
        neurons = self.get_neuron_list(
            cell_types=cell_types,
            brain_regions=brain_regions,
            limit=max_neurons
        )

        # Transform to standard format
        transformed = []
        for neuron in neurons:
            transformed_neuron = self._transform_neuron(neuron)
            transformed.append(transformed_neuron)
            self.stats['items_extracted'] += 1

        return transformed

    def get_neuron_list(
        self,
        cell_types: List[str] = None,
        brain_regions: List[str] = None,
        limit: int = 500
    ) -> List[Dict[str, Any]]:
        """
        Get list of neurons with filters.

        Args:
            cell_types: Filter by cell types
            brain_regions: Filter by brain regions
            limit: Maximum neurons to retrieve

        Returns:
            List of neuron metadata
        """
        url = f"{self.base_url}/neuron/select"

        params = {
            'size': min(limit, 500),  # API limit
            'page': 0
        }

        # Add filters if specified
        if cell_types:
            params['q'] = f"cell_type:{','.join(cell_types)}"
        if brain_regions:
            params['fq'] = f"brain_region:{','.join(brain_regions)}"

        try:
            data = self.get_json(url, params=params)

            # Handle pagination
            neurons = data.get('_embedded', {}).get('neuronResources', [])

            self.logger.info(f"Retrieved {len(neurons)} neurons")
            return neurons

        except Exception as e:
            self.logger.error(f"Error getting neuron list: {str(e)}")
            return []

    def get_cell_types(self) -> List[str]:
        """Get list of all cell types in database."""
        url = f"{self.base_url}/neuron/fields/cell_type"

        try:
            data = self.get_json(url)
            cell_types = data.get('Cell Type', [])
            self.logger.info(f"Found {len(cell_types)} cell types")
            return cell_types

        except Exception as e:
            self.logger.error(f"Error getting cell types: {str(e)}")
            return []

    def _transform_neuron(self, neuron: Dict) -> Dict[str, Any]:
        """Transform neuron data to standard format."""
        return {
            'identifier': f"NMO:{neuron.get('neuron_name')}",
            'name': neuron.get('neuron_name'),
            'description': f"{neuron.get('cell_type')} neuron from {neuron.get('brain_region')}",
            'entity_type': 'cell_type',
            'morphology_class': neuron.get('cell_type'),
            'tissue_origin': neuron.get('brain_region'),
            'source_database': 'NeuroMorpho',
            'confidence_score': 0.85,
            'evidence_strength': 'experimental',
            'metadata': {
                'species': neuron.get('species'),
                'age_classification': neuron.get('age_classification'),
                'protocol': neuron.get('protocol'),
                'archive': neuron.get('archive')
            }
        }


class CellOntologyExtractor(BaseExtractor):
    """
    Extract cell type classifications from Cell Ontology.

    Focuses on:
    - Cell type hierarchies
    - Cell type definitions
    - Marker genes
    - Functional roles
    """

    def __init__(self, **kwargs):
        """Initialize Cell Ontology extractor."""
        super().__init__(
            rate_limit_calls=10,
            rate_limit_period=1.0,
            **kwargs
        )
        # Using OLS (Ontology Lookup Service) for Cell Ontology
        self.base_url = "https://www.ebi.ac.uk/ols4/api"
        self.ontology = "cl"  # Cell Ontology

    def extract(
        self,
        cell_type_filter: str = None,
        max_terms: int = 500
    ) -> List[Dict[str, Any]]:
        """
        Extract cell type definitions.

        Args:
            cell_type_filter: Filter by cell type (e.g., 'neuron')
            max_terms: Maximum number of terms to extract

        Returns:
            List of cell type dictionaries
        """
        self.logger.info("Starting Cell Ontology extraction...")

        if cell_type_filter:
            terms = self.search_terms(cell_type_filter, max_terms)
        else:
            terms = self.get_all_terms(max_terms)

        # Transform to standard format
        transformed = []
        for term in terms:
            transformed_term = self._transform_term(term)
            transformed.append(transformed_term)
            self.stats['items_extracted'] += 1

        return transformed

    def search_terms(self, query: str, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Search for cell type terms.

        Args:
            query: Search query
            limit: Maximum results

        Returns:
            List of matching terms
        """
        url = f"{self.base_url}/search"

        params = {
            'q': query,
            'ontology': self.ontology,
            'rows': limit,
            'exact': False
        }

        try:
            data = self.get_json(url, params=params)

            terms = data.get('response', {}).get('docs', [])
            self.logger.info(f"Found {len(terms)} matching terms")

            return terms

        except Exception as e:
            self.logger.error(f"Error searching terms: {str(e)}")
            return []

    def get_all_terms(self, limit: int = 500) -> List[Dict[str, Any]]:
        """
        Get all cell type terms.

        Args:
            limit: Maximum terms to retrieve

        Returns:
            List of all terms
        """
        url = f"{self.base_url}/ontologies/{self.ontology}/terms"

        params = {
            'size': min(limit, 500)
        }

        try:
            # Use pagination
            terms = self.paginate(
                url,
                params=params,
                page_param='page',
                page_size_param='size',
                page_size=100,
                max_pages=5,
                results_key='_embedded.terms'
            )

            self.logger.info(f"Retrieved {len(terms)} terms")
            return terms

        except Exception as e:
            self.logger.error(f"Error getting all terms: {str(e)}")
            return []

    def get_term_details(self, term_iri: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a term.

        Args:
            term_iri: Term IRI (URL-encoded)

        Returns:
            Term details
        """
        url = f"{self.base_url}/ontologies/{self.ontology}/terms"

        params = {
            'iri': term_iri
        }

        try:
            data = self.get_json(url, params=params)
            return data

        except Exception as e:
            self.logger.error(f"Error getting term details: {str(e)}")
            return None

    def _transform_term(self, term: Dict) -> Dict[str, Any]:
        """Transform Cell Ontology term to standard format."""
        # Extract cell type from label
        label = term.get('label', '')
        description = term.get('description', [''])[0] if isinstance(term.get('description'), list) else term.get('description', '')

        return {
            'identifier': term.get('obo_id') or term.get('short_form'),
            'name': label,
            'description': description,
            'entity_type': 'cell_type',
            'morphology_class': self._infer_morphology_class(label),
            'source_database': 'Cell Ontology',
            'confidence_score': 0.90,
            'evidence_strength': 'experimental',
            'metadata': {
                'iri': term.get('iri'),
                'synonyms': term.get('synonym', []),
                'is_defining_ontology': term.get('is_defining_ontology', False)
            }
        }

    def _infer_morphology_class(self, label: str) -> str:
        """Infer morphology class from cell type label."""
        label_lower = label.lower()

        morphology_keywords = {
            'pyramidal': 'pyramidal',
            'stellate': 'stellate',
            'granule': 'granule',
            'purkinje': 'purkinje',
            'interneuron': 'interneuron',
            'astrocyte': 'astrocyte',
            'oligodendrocyte': 'oligodendrocyte',
            'microglia': 'microglia'
        }

        for keyword, morphology in morphology_keywords.items():
            if keyword in label_lower:
                return morphology

        return 'other'
