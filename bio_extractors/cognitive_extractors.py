"""
Cognitive Ontology Extractors

Extract cognitive and mental process definitions from:
- Cognitive Atlas (cognitive concepts and tasks)
- CogPO (Cognitive Paradigm Ontology via BioPortal)
- MFO (Mental Functioning Ontology via BioPortal)

Focus on computational/architectural representations of cognitive functions.
"""

import json
from typing import Dict, List, Any, Optional
from .base import BaseExtractor


class CognitiveAtlasExtractor(BaseExtractor):
    """
    Extract cognitive concepts and tasks from Cognitive Atlas.

    Focuses on:
    - Cognitive concepts (mental processes)
    - Task ontology
    - Concept relationships
    - Computational paradigms
    """

    def __init__(self, **kwargs):
        """Initialize Cognitive Atlas extractor."""
        super().__init__(
            rate_limit_calls=10,
            rate_limit_period=1.0,
            **kwargs
        )
        self.base_url = "https://www.cognitiveatlas.org/api/v-alpha"

    def extract(
        self,
        extraction_type: str = 'concepts',
        max_items: int = 500
    ) -> List[Dict[str, Any]]:
        """
        Extract Cognitive Atlas data.

        Args:
            extraction_type: 'concepts', 'tasks', or 'disorders'
            max_items: Maximum items to extract

        Returns:
            List of cognitive entity dictionaries
        """
        self.logger.info(f"Starting Cognitive Atlas extraction ({extraction_type})...")

        if extraction_type == 'concepts':
            return self.extract_concepts(max_items)
        elif extraction_type == 'tasks':
            return self.extract_tasks(max_items)
        elif extraction_type == 'disorders':
            return self.extract_disorders(max_items)
        else:
            self.logger.warning(f"Unknown extraction type: {extraction_type}")
            return []

    def extract_concepts(self, limit: int = 500) -> List[Dict[str, Any]]:
        """
        Extract cognitive concepts.

        Returns:
            List of concept dictionaries
        """
        url = f"{self.base_url}/concept"

        try:
            data = self.get_json(url)

            concepts = []
            for concept in data[:limit]:
                transformed = self._transform_concept(concept)
                concepts.append(transformed)
                self.stats['items_extracted'] += 1

            self.logger.info(f"Extracted {len(concepts)} cognitive concepts")
            return concepts

        except Exception as e:
            self.logger.error(f"Error extracting concepts: {str(e)}")
            return []

    def extract_tasks(self, limit: int = 500) -> List[Dict[str, Any]]:
        """
        Extract cognitive tasks.

        Returns:
            List of task dictionaries
        """
        url = f"{self.base_url}/task"

        try:
            data = self.get_json(url)

            tasks = []
            for task in data[:limit]:
                transformed = self._transform_task(task)
                tasks.append(transformed)
                self.stats['items_extracted'] += 1

            self.logger.info(f"Extracted {len(tasks)} cognitive tasks")
            return tasks

        except Exception as e:
            self.logger.error(f"Error extracting tasks: {str(e)}")
            return []

    def extract_disorders(self, limit: int = 500) -> List[Dict[str, Any]]:
        """
        Extract cognitive disorders.

        Returns:
            List of disorder dictionaries
        """
        url = f"{self.base_url}/disorder"

        try:
            data = self.get_json(url)

            disorders = []
            for disorder in data[:limit]:
                transformed = self._transform_disorder(disorder)
                disorders.append(transformed)
                self.stats['items_extracted'] += 1

            self.logger.info(f"Extracted {len(disorders)} disorders")
            return disorders

        except Exception as e:
            self.logger.error(f"Error extracting disorders: {str(e)}")
            return []

    def get_concept_details(self, concept_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a concept.

        Args:
            concept_id: Concept identifier

        Returns:
            Concept details
        """
        url = f"{self.base_url}/concept/id/{concept_id}"

        try:
            data = self.get_json(url)
            return data

        except Exception as e:
            self.logger.error(f"Error getting concept details: {str(e)}")
            return None

    def _transform_concept(self, concept: Dict) -> Dict[str, Any]:
        """Transform cognitive concept to standard format."""
        return {
            'identifier': f"COGAT:{concept.get('id')}",
            'name': concept.get('name'),
            'description': concept.get('definition', ''),
            'entity_type': 'computation',  # Cognitive processes are computations
            'operation_type': self._infer_operation_type(concept.get('name', '')),
            'source_database': 'Cognitive Atlas',
            'confidence_score': 0.85,
            'evidence_strength': 'computational',
            'metadata': {
                'alias': concept.get('alias'),
                'event_stamp': concept.get('event_stamp')
            }
        }

    def _transform_task(self, task: Dict) -> Dict[str, Any]:
        """Transform cognitive task to standard format."""
        return {
            'identifier': f"COGAT_TASK:{task.get('id')}",
            'name': task.get('name'),
            'description': task.get('definition', ''),
            'entity_type': 'process',  # Tasks are processes
            'process_category': 'cognitive',
            'source_database': 'Cognitive Atlas',
            'confidence_score': 0.80,
            'evidence_strength': 'computational',
            'metadata': task
        }

    def _transform_disorder(self, disorder: Dict) -> Dict[str, Any]:
        """Transform disorder to standard format."""
        return {
            'identifier': f"COGAT_DISORDER:{disorder.get('id')}",
            'name': disorder.get('name'),
            'description': disorder.get('definition', ''),
            'entity_type': 'constraint',  # Disorders represent violated constraints
            'constraint_type': 'cognitive',
            'source_database': 'Cognitive Atlas',
            'confidence_score': 0.85,
            'evidence_strength': 'experimental',
            'metadata': disorder
        }

    def _infer_operation_type(self, name: str) -> str:
        """Infer cognitive operation type from name."""
        name_lower = name.lower()

        operation_keywords = {
            'memory': 'memory_operation',
            'attention': 'attention_control',
            'decision': 'decision_making',
            'learning': 'learning',
            'perception': 'perception',
            'motor': 'motor_control',
            'language': 'language_processing',
            'reasoning': 'reasoning',
            'emotion': 'emotion_processing'
        }

        for keyword, operation in operation_keywords.items():
            if keyword in name_lower:
                return operation

        return 'cognitive_operation'


class CogPOExtractor(BaseExtractor):
    """
    Extract Cognitive Paradigm Ontology terms via BioPortal.

    Focuses on:
    - Experimental paradigms
    - Cognitive task structures
    - Measurement approaches
    """

    def __init__(self, api_key: str = None, **kwargs):
        """
        Initialize CogPO extractor.

        Args:
            api_key: BioPortal API key (get from https://bioportal.bioontology.org/account)
        """
        super().__init__(
            rate_limit_calls=5,  # Conservative for BioPortal
            rate_limit_period=1.0,
            **kwargs
        )
        self.base_url = "https://data.bioontology.org"
        self.api_key = api_key
        self.ontology_acronym = "COGPO"

    def extract(self, max_terms: int = 500) -> List[Dict[str, Any]]:
        """
        Extract CogPO terms.

        Args:
            max_terms: Maximum terms to extract

        Returns:
            List of CogPO term dictionaries
        """
        if not self.api_key:
            self.logger.error("BioPortal API key required. Get one at https://bioportal.bioontology.org/account")
            return []

        self.logger.info("Starting CogPO extraction via BioPortal...")

        terms = self.get_ontology_terms(max_terms)

        # Transform to standard format
        transformed = []
        for term in terms:
            transformed_term = self._transform_term(term)
            transformed.append(transformed_term)
            self.stats['items_extracted'] += 1

        return transformed

    def get_ontology_terms(self, limit: int = 500) -> List[Dict[str, Any]]:
        """
        Get all terms from CogPO ontology.

        Args:
            limit: Maximum terms to retrieve

        Returns:
            List of terms
        """
        url = f"{self.base_url}/ontologies/{self.ontology_acronym}/classes"

        params = {
            'apikey': self.api_key,
            'pagesize': 100
        }

        # Add API key to session headers
        self.session.headers.update({'Authorization': f'apikey token={self.api_key}'})

        try:
            # Paginate through results
            terms = self.paginate(
                url,
                params=params,
                page_param='page',
                page_size_param='pagesize',
                page_size=100,
                max_pages=min(5, limit // 100 + 1),
                results_key='collection'
            )

            self.logger.info(f"Retrieved {len(terms)} CogPO terms")
            return terms[:limit]

        except Exception as e:
            self.logger.error(f"Error getting CogPO terms: {str(e)}")
            return []

    def get_term_details(self, term_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a term.

        Args:
            term_id: Term identifier

        Returns:
            Term details
        """
        url = f"{self.base_url}/ontologies/{self.ontology_acronym}/classes/{term_id}"

        params = {
            'apikey': self.api_key
        }

        try:
            data = self.get_json(url, params=params)
            return data

        except Exception as e:
            self.logger.error(f"Error getting term details: {str(e)}")
            return None

    def _transform_term(self, term: Dict) -> Dict[str, Any]:
        """Transform CogPO term to standard format."""
        return {
            'identifier': term.get('@id'),
            'name': term.get('prefLabel'),
            'description': term.get('definition', [''])[0] if isinstance(term.get('definition'), list) else term.get('definition', ''),
            'entity_type': 'computation',
            'operation_type': 'cognitive_paradigm',
            'source_database': 'CogPO',
            'confidence_score': 0.85,
            'evidence_strength': 'computational',
            'metadata': {
                'synonyms': term.get('synonym', []),
                'notation': term.get('notation')
            }
        }


class MFOExtractor(BaseExtractor):
    """
    Extract Mental Functioning Ontology terms via BioPortal.

    Focuses on:
    - Mental states
    - Cognitive functions
    - Mental processes
    """

    def __init__(self, api_key: str = None, **kwargs):
        """
        Initialize MFO extractor.

        Args:
            api_key: BioPortal API key
        """
        super().__init__(
            rate_limit_calls=5,
            rate_limit_period=1.0,
            **kwargs
        )
        self.base_url = "https://data.bioontology.org"
        self.api_key = api_key
        self.ontology_acronym = "MF"  # Mental Functioning Ontology

    def extract(self, max_terms: int = 500) -> List[Dict[str, Any]]:
        """
        Extract MFO terms.

        Args:
            max_terms: Maximum terms to extract

        Returns:
            List of MFO term dictionaries
        """
        if not self.api_key:
            self.logger.error("BioPortal API key required")
            return []

        self.logger.info("Starting MFO extraction via BioPortal...")

        terms = self.get_ontology_terms(max_terms)

        # Transform to standard format
        transformed = []
        for term in terms:
            transformed_term = self._transform_term(term)
            transformed.append(transformed_term)
            self.stats['items_extracted'] += 1

        return transformed

    def get_ontology_terms(self, limit: int = 500) -> List[Dict[str, Any]]:
        """Get all terms from MFO ontology."""
        url = f"{self.base_url}/ontologies/{self.ontology_acronym}/classes"

        params = {
            'apikey': self.api_key,
            'pagesize': 100
        }

        self.session.headers.update({'Authorization': f'apikey token={self.api_key}'})

        try:
            terms = self.paginate(
                url,
                params=params,
                page_param='page',
                page_size_param='pagesize',
                page_size=100,
                max_pages=min(5, limit // 100 + 1),
                results_key='collection'
            )

            self.logger.info(f"Retrieved {len(terms)} MFO terms")
            return terms[:limit]

        except Exception as e:
            self.logger.error(f"Error getting MFO terms: {str(e)}")
            return []

    def _transform_term(self, term: Dict) -> Dict[str, Any]:
        """Transform MFO term to standard format."""
        return {
            'identifier': term.get('@id'),
            'name': term.get('prefLabel'),
            'description': term.get('definition', [''])[0] if isinstance(term.get('definition'), list) else term.get('definition', ''),
            'entity_type': 'representation',  # Mental states are representations
            'encoding_type': 'cognitive_state',
            'source_database': 'MFO',
            'confidence_score': 0.80,
            'evidence_strength': 'computational',
            'metadata': {
                'synonyms': term.get('synonym', []),
                'notation': term.get('notation')
            }
        }
