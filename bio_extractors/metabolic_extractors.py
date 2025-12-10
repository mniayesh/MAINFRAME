"""
Metabolic Database Extractors

Extract metabolic principles and patterns from:
- ChEBI (chemical entities and biological roles)
- eQuilibrator (thermodynamic parameters)

Focus on patterns and regulatory mechanisms, NOT exhaustive molecule lists.
"""

import json
from typing import Dict, List, Any, Optional
from zeep import Client
from .base import BaseExtractor


class ChEBIExtractor(BaseExtractor):
    """
    Extract chemical entities and biological roles from ChEBI.

    Focuses on:
    - Biological role classifications
    - Cofactors and coenzymes
    - Metabolite classes
    - Chemical ontology patterns
    """

    def __init__(self, **kwargs):
        """Initialize ChEBI extractor."""
        super().__init__(
            rate_limit_calls=10,
            rate_limit_period=1.0,
            **kwargs
        )
        self.rest_base_url = "https://www.ebi.ac.uk/chebi/backend/api"
        self.wsdl_url = "http://www.ebi.ac.uk/webservices/chebi/2.0/webservice?wsdl"
        self.soap_client = None

    def _init_soap_client(self):
        """Initialize SOAP client lazily."""
        if not self.soap_client:
            try:
                self.soap_client = Client(self.wsdl_url)
                self.logger.info("ChEBI SOAP client initialized")
            except Exception as e:
                self.logger.error(f"Error initializing SOAP client: {str(e)}")

    def extract(
        self,
        extraction_type: str = 'roles',
        parent_id: str = None,
        max_entities: int = 500
    ) -> List[Dict[str, Any]]:
        """
        Extract ChEBI data.

        Args:
            extraction_type: 'roles' (biological roles), 'cofactors', 'metabolites'
            parent_id: Parent ChEBI ID for ontology traversal
            max_entities: Maximum entities to extract

        Returns:
            List of chemical entity dictionaries
        """
        self.logger.info(f"Starting ChEBI extraction ({extraction_type})...")

        if extraction_type == 'roles':
            return self.extract_biological_roles(max_entities)
        elif extraction_type == 'cofactors':
            return self.extract_cofactors(max_entities)
        elif extraction_type == 'metabolites':
            return self.extract_metabolite_classes(max_entities)
        else:
            self.logger.warning(f"Unknown extraction type: {extraction_type}")
            return []

    def extract_biological_roles(self, limit: int = 500) -> List[Dict[str, Any]]:
        """
        Extract biological role classifications.

        Returns:
            List of biological role entities
        """
        self._init_soap_client()
        if not self.soap_client:
            return []

        # Get all children of "biological role" (CHEBI:24432)
        parent_chebi_id = 'CHEBI:24432'

        try:
            # Get ontology children
            children = self.soap_client.service.getAllOntologyChildrenInPath(
                chebiId=parent_chebi_id,
                relationshipType='is a',
                onlyWithChemicalStructure=False
            )

            roles = []
            for child in children[:limit]:
                role_data = self._transform_role(child)
                roles.append(role_data)
                self.stats['items_extracted'] += 1

            self.logger.info(f"Extracted {len(roles)} biological roles")
            return roles

        except Exception as e:
            self.logger.error(f"Error extracting biological roles: {str(e)}")
            return []

    def extract_cofactors(self, limit: int = 500) -> List[Dict[str, Any]]:
        """
        Extract cofactor and coenzyme entities.

        Returns:
            List of cofactor entities
        """
        self._init_soap_client()
        if not self.soap_client:
            return []

        # Get all children of "cofactor" (CHEBI:23357)
        parent_chebi_id = 'CHEBI:23357'

        try:
            children = self.soap_client.service.getAllOntologyChildrenInPath(
                chebiId=parent_chebi_id,
                relationshipType='is a',
                onlyWithChemicalStructure=True  # Only with structures
            )

            cofactors = []
            for child in children[:limit]:
                # Get complete entity for more details
                entity = self.get_complete_entity(child.chebiId)
                if entity:
                    cofactor_data = self._transform_cofactor(entity)
                    cofactors.append(cofactor_data)
                    self.stats['items_extracted'] += 1

            self.logger.info(f"Extracted {len(cofactors)} cofactors")
            return cofactors

        except Exception as e:
            self.logger.error(f"Error extracting cofactors: {str(e)}")
            return []

    def extract_metabolite_classes(self, limit: int = 500) -> List[Dict[str, Any]]:
        """
        Extract metabolite classifications.

        Returns:
            List of metabolite class entities
        """
        # Use REST API to search for metabolite classes
        url = f"{self.rest_base_url}/data/search"

        params = {
            'query': 'metabolite',
            'max_results': limit
        }

        try:
            data = self.get_json(url, params=params)

            metabolites = []
            for item in data.get('entities', [])[:limit]:
                metabolite = self._transform_metabolite(item)
                metabolites.append(metabolite)
                self.stats['items_extracted'] += 1

            self.logger.info(f"Extracted {len(metabolites)} metabolite classes")
            return metabolites

        except Exception as e:
            self.logger.error(f"Error extracting metabolite classes: {str(e)}")
            return []

    def get_complete_entity(self, chebi_id: str) -> Optional[Dict]:
        """
        Get complete entity information.

        Args:
            chebi_id: ChEBI identifier

        Returns:
            Complete entity data
        """
        self._init_soap_client()
        if not self.soap_client:
            return None

        try:
            entity = self.soap_client.service.getCompleteEntity(chebi_id)
            return entity

        except Exception as e:
            self.logger.error(f"Error getting complete entity {chebi_id}: {str(e)}")
            return None

    def _transform_role(self, role_data) -> Dict[str, Any]:
        """Transform biological role to standard format."""
        return {
            'identifier': role_data.chebiId,
            'name': role_data.chebiName,
            'description': f"Biological role classification: {role_data.chebiName}",
            'entity_type': 'mechanism',  # Roles are computational mechanisms
            'mechanism_class': 'biological_role',
            'source_database': 'ChEBI',
            'confidence_score': 0.90,
            'evidence_strength': 'experimental',
            'metadata': {
                'type': role_data.type if hasattr(role_data, 'type') else None,
                'status': role_data.status if hasattr(role_data, 'status') else None
            }
        }

    def _transform_cofactor(self, entity) -> Dict[str, Any]:
        """Transform cofactor entity to standard format."""
        return {
            'identifier': entity.chebiId,
            'name': entity.chebiAsciiName,
            'description': entity.definition or '',
            'entity_type': 'mechanism',
            'mechanism_class': 'cofactor',
            'source_database': 'ChEBI',
            'confidence_score': 0.90,
            'evidence_strength': 'experimental',
            'metadata': {
                'formula': entity.Formulae[0] if entity.Formulae else None,
                'charge': entity.charge,
                'mass': entity.mass,
                'smiles': entity.smiles,
                'inchi': entity.inchi
            }
        }

    def _transform_metabolite(self, item: Dict) -> Dict[str, Any]:
        """Transform metabolite data to standard format."""
        return {
            'identifier': item.get('id'),
            'name': item.get('name'),
            'description': item.get('definition', ''),
            'entity_type': 'process',  # Metabolites participate in processes
            'process_category': 'metabolic',
            'source_database': 'ChEBI',
            'confidence_score': 0.85,
            'evidence_strength': 'computational',
            'metadata': item
        }


class EQuilibratorExtractor(BaseExtractor):
    """
    Extract thermodynamic parameters from eQuilibrator.

    Focuses on:
    - Gibbs free energy (ΔG) values
    - Reaction thermodynamics
    - pH and ionic strength dependencies
    - Equilibrium constants
    """

    def __init__(self, **kwargs):
        """Initialize eQuilibrator extractor."""
        super().__init__(
            rate_limit_calls=5,  # Conservative for computational API
            rate_limit_period=1.0,
            **kwargs
        )
        self.base_url = "https://equilibrator.weizmann.ac.il/api"

    def extract(
        self,
        reaction_ids: List[str] = None,
        compound_ids: List[str] = None,
        max_entries: int = 500
    ) -> List[Dict[str, Any]]:
        """
        Extract thermodynamic data.

        Args:
            reaction_ids: List of reaction identifiers to extract
            compound_ids: List of compound identifiers
            max_entries: Maximum entries to extract

        Returns:
            List of thermodynamic parameter dictionaries
        """
        self.logger.info("Starting eQuilibrator extraction...")

        results = []

        # Extract reactions
        if reaction_ids:
            for reaction_id in reaction_ids[:max_entries]:
                reaction_data = self.get_reaction_thermodynamics(reaction_id)
                if reaction_data:
                    results.append(reaction_data)
                    self.stats['items_extracted'] += 1

        # Extract compounds
        if compound_ids:
            for compound_id in compound_ids[:max_entries]:
                compound_data = self.get_compound_thermodynamics(compound_id)
                if compound_data:
                    results.append(compound_data)
                    self.stats['items_extracted'] += 1

        return results

    def get_reaction_thermodynamics(self, reaction_id: str) -> Optional[Dict[str, Any]]:
        """
        Get thermodynamic parameters for a reaction.

        Args:
            reaction_id: Reaction identifier

        Returns:
            Thermodynamic parameters
        """
        # Note: eQuilibrator API may require authentication or have specific endpoints
        # This is a placeholder implementation - adjust based on actual API
        url = f"{self.base_url}/reaction/{reaction_id}"

        try:
            data = self.get_json(url)

            return self._transform_reaction_thermodynamics(data)

        except Exception as e:
            self.logger.error(f"Error getting reaction thermodynamics: {str(e)}")
            return None

    def get_compound_thermodynamics(self, compound_id: str) -> Optional[Dict[str, Any]]:
        """
        Get thermodynamic parameters for a compound.

        Args:
            compound_id: Compound identifier

        Returns:
            Thermodynamic parameters
        """
        url = f"{self.base_url}/compound/{compound_id}"

        try:
            data = self.get_json(url)

            return self._transform_compound_thermodynamics(data)

        except Exception as e:
            self.logger.error(f"Error getting compound thermodynamics: {str(e)}")
            return None

    def _transform_reaction_thermodynamics(self, data: Dict) -> Dict[str, Any]:
        """Transform reaction thermodynamics to standard format."""
        return {
            'identifier': data.get('id'),
            'name': data.get('name', 'Thermodynamic reaction'),
            'description': data.get('equation', ''),
            'entity_type': 'process',
            'process_category': 'metabolic',
            'source_database': 'eQuilibrator',
            'confidence_score': 0.80,
            'evidence_strength': 'computational',
            'metadata': {
                'delta_g': data.get('dG'),
                'delta_g_prime': data.get('dG_prime'),
                'ph': data.get('pH'),
                'ionic_strength': data.get('ionic_strength'),
                'temperature': data.get('temperature')
            }
        }

    def _transform_compound_thermodynamics(self, data: Dict) -> Dict[str, Any]:
        """Transform compound thermodynamics to standard format."""
        return {
            'identifier': data.get('id'),
            'name': data.get('name'),
            'description': f"Thermodynamic properties of {data.get('name')}",
            'entity_type': 'constraint',  # Thermodynamic constraints
            'constraint_type': 'thermodynamic',
            'source_database': 'eQuilibrator',
            'confidence_score': 0.80,
            'evidence_strength': 'computational',
            'metadata': {
                'formation_energy': data.get('formation_energy'),
                'ph': data.get('pH'),
                'ionic_strength': data.get('ionic_strength')
            }
        }
