"""
Protein and Enzyme Extractors

Extract protein family and enzyme data from:
- UniProt (protein families, domains, functional annotations)
- InterPro (protein domain architectures)
- BRENDA (enzyme catalytic mechanisms)

Focus on family-level patterns, NOT individual sequences.
"""

import json
import hashlib
from typing import Dict, List, Any, Optional
from zeep import Client
from .base import BaseExtractor


class UniProtExtractor(BaseExtractor):
    """
    Extract protein family data from UniProt.

    Focuses on:
    - Protein families (NOT individual sequences)
    - Functional domains
    - Catalytic mechanisms
    - Family representatives (UniRef)
    """

    def __init__(self, **kwargs):
        """Initialize UniProt extractor."""
        super().__init__(
            rate_limit_calls=10,
            rate_limit_period=1.0,
            **kwargs
        )
        self.base_url = "https://rest.uniprot.org"

    def extract(
        self,
        extraction_type: str = 'families',
        organism: str = '9606',  # Homo sapiens
        max_results: int = 500
    ) -> List[Dict[str, Any]]:
        """
        Extract UniProt data.

        Args:
            extraction_type: 'families', 'domains', or 'catalytic'
            organism: NCBI taxonomy ID
            max_results: Maximum results to extract

        Returns:
            List of extracted entities
        """
        self.logger.info(f"Starting UniProt extraction ({extraction_type})...")

        if extraction_type == 'families':
            return self.extract_protein_families(organism, max_results)
        elif extraction_type == 'domains':
            return self.extract_domains(organism, max_results)
        elif extraction_type == 'catalytic':
            return self.extract_catalytic_activities(organism, max_results)
        else:
            self.logger.warning(f"Unknown extraction type: {extraction_type}")
            return []

    def extract_protein_families(self, organism: str = '9606', limit: int = 500) -> List[Dict[str, Any]]:
        """
        Extract protein family representatives using UniRef.

        Args:
            organism: NCBI taxonomy ID
            limit: Maximum families to extract

        Returns:
            List of protein family dictionaries
        """
        # Use UniRef90 for family representatives (90% identity clustering)
        url = f"{self.base_url}/uniref/search"

        params = {
            'query': f'(taxonomy_id:{organism})',
            'format': 'json',
            'size': min(limit, 500)
        }

        try:
            # Paginate through results
            results = self.paginate(
                url,
                params=params,
                page_param='cursor',
                page_size_param='size',
                page_size=100,
                max_pages=5,
                results_key='results'
            )

            # Transform to standard format
            families = []
            for result in results:
                family = self._transform_uniref_cluster(result)
                families.append(family)
                self.stats['items_extracted'] += 1

            self.logger.info(f"Extracted {len(families)} protein families")
            return families

        except Exception as e:
            self.logger.error(f"Error extracting protein families: {str(e)}")
            return []

    def extract_domains(self, organism: str = '9606', limit: int = 500) -> List[Dict[str, Any]]:
        """
        Extract proteins with specific domain architectures.

        Args:
            organism: NCBI taxonomy ID
            limit: Maximum domains to extract

        Returns:
            List of domain dictionaries
        """
        # Search for proteins with Pfam/InterPro annotations
        url = f"{self.base_url}/uniprotkb/search"

        params = {
            'query': f'(organism_id:{organism}) AND (xref:pfam-*)',
            'format': 'json',
            'fields': 'accession,protein_name,xref_pfam,ft_domain',
            'size': min(limit, 500)
        }

        try:
            data = self.get_json(url, params=params)

            domains = []
            for entry in data.get('results', []):
                # Extract domain information
                domain_data = self._extract_domain_info(entry)
                if domain_data:
                    domains.extend(domain_data)
                    self.stats['items_extracted'] += len(domain_data)

            self.logger.info(f"Extracted {len(domains)} domain architectures")
            return domains

        except Exception as e:
            self.logger.error(f"Error extracting domains: {str(e)}")
            return []

    def extract_catalytic_activities(self, organism: str = '9606', limit: int = 500) -> List[Dict[str, Any]]:
        """
        Extract proteins with catalytic activity annotations.

        Args:
            organism: NCBI taxonomy ID
            limit: Maximum catalytic activities to extract

        Returns:
            List of catalytic activity dictionaries
        """
        url = f"{self.base_url}/uniprotkb/search"

        params = {
            'query': f'(organism_id:{organism}) AND (cc_catalytic_activity:*)',
            'format': 'json',
            'fields': 'accession,protein_name,cc_catalytic_activity,ec',
            'size': min(limit, 500)
        }

        try:
            data = self.get_json(url, params=params)

            activities = []
            for entry in data.get('results', []):
                activity = self._transform_catalytic_activity(entry)
                if activity:
                    activities.append(activity)
                    self.stats['items_extracted'] += 1

            self.logger.info(f"Extracted {len(activities)} catalytic activities")
            return activities

        except Exception as e:
            self.logger.error(f"Error extracting catalytic activities: {str(e)}")
            return []

    def _transform_uniref_cluster(self, cluster: Dict) -> Dict[str, Any]:
        """Transform UniRef cluster to standard format."""
        return {
            'identifier': cluster.get('id'),
            'name': cluster.get('name'),
            'description': cluster.get('representativeMember', {}).get('proteinName', ''),
            'entity_type': 'enzyme',  # Placeholder, refine based on annotation
            'source_database': 'UniProt',
            'confidence_score': 0.85,
            'evidence_strength': 'computational',
            'metadata': {
                'member_count': cluster.get('memberCount'),
                'organism': cluster.get('representativeMember', {}).get('organism', {}).get('scientificName'),
                'common_taxon': cluster.get('commonTaxon', {}).get('scientificName')
            }
        }

    def _extract_domain_info(self, entry: Dict) -> List[Dict[str, Any]]:
        """Extract domain information from UniProt entry."""
        domains = []

        # Extract Pfam domains
        pfam_refs = entry.get('uniProtKBCrossReferences', [])
        for ref in pfam_refs:
            if ref.get('database') == 'Pfam':
                domain = {
                    'identifier': ref.get('id'),
                    'name': ref.get('properties', [{}])[0].get('value', '') if ref.get('properties') else '',
                    'description': f"Pfam domain from {entry.get('primaryAccession')}",
                    'entity_type': 'mechanism',
                    'source_database': 'UniProt',
                    'confidence_score': 0.85,
                    'evidence_strength': 'computational',
                    'metadata': {
                        'protein_accession': entry.get('primaryAccession'),
                        'protein_name': entry.get('proteinDescription', {}).get('recommendedName', {}).get('fullName', {}).get('value')
                    }
                }
                domains.append(domain)

        return domains

    def _transform_catalytic_activity(self, entry: Dict) -> Optional[Dict[str, Any]]:
        """Transform catalytic activity entry to standard format."""
        # Extract EC number if available
        ec_numbers = []
        for comment in entry.get('comments', []):
            if comment.get('commentType') == 'CATALYTIC_ACTIVITY':
                reaction = comment.get('reaction', {})
                ec_number = reaction.get('ecNumber')
                if ec_number:
                    ec_numbers.append(ec_number)

        if not ec_numbers:
            return None

        return {
            'identifier': entry.get('primaryAccession'),
            'name': entry.get('proteinDescription', {}).get('recommendedName', {}).get('fullName', {}).get('value', ''),
            'description': 'Catalytic activity',
            'entity_type': 'enzyme',
            'ec_number': ec_numbers[0] if ec_numbers else None,
            'source_database': 'UniProt',
            'confidence_score': 0.90,
            'evidence_strength': 'experimental',
            'metadata': {
                'all_ec_numbers': ec_numbers
            }
        }


class InterProExtractor(BaseExtractor):
    """
    Extract protein domain and family data from InterPro.

    Focuses on:
    - Protein domain families
    - Domain architectures
    - Functional sites
    """

    def __init__(self, **kwargs):
        """Initialize InterPro extractor."""
        super().__init__(
            rate_limit_calls=10,
            rate_limit_period=1.0,
            **kwargs
        )
        self.base_url = "https://www.ebi.ac.uk/interpro/api"

    def extract(
        self,
        entry_type: str = 'domain',
        max_entries: int = 500
    ) -> List[Dict[str, Any]]:
        """
        Extract InterPro entries.

        Args:
            entry_type: Type of entry ('domain', 'family', 'site')
            max_entries: Maximum entries to extract

        Returns:
            List of InterPro entry dictionaries
        """
        self.logger.info(f"Starting InterPro extraction ({entry_type})...")

        entries = self.get_entries(entry_type=entry_type, limit=max_entries)

        # Transform to standard format
        transformed = []
        for entry in entries:
            transformed_entry = self._transform_entry(entry)
            transformed.append(transformed_entry)
            self.stats['items_extracted'] += 1

        return transformed

    def get_entries(self, entry_type: str = 'domain', limit: int = 500) -> List[Dict[str, Any]]:
        """
        Get InterPro entries of a specific type.

        Args:
            entry_type: Type of entry
            limit: Maximum entries to retrieve

        Returns:
            List of entries
        """
        url = f"{self.base_url}/entry/interpro"

        params = {
            'type': entry_type,
            'page_size': 100
        }

        try:
            # Use pagination
            entries = self.paginate(
                url,
                params=params,
                page_param='page',
                page_size_param='page_size',
                page_size=100,
                max_pages=min(5, limit // 100 + 1),
                results_key='results'
            )

            self.logger.info(f"Retrieved {len(entries)} InterPro entries")
            return entries[:limit]

        except Exception as e:
            self.logger.error(f"Error getting InterPro entries: {str(e)}")
            return []

    def get_entry_details(self, interpro_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about an InterPro entry.

        Args:
            interpro_id: InterPro identifier (e.g., 'IPR000001')

        Returns:
            Entry details
        """
        url = f"{self.base_url}/entry/interpro/{interpro_id}"

        try:
            data = self.get_json(url)
            return data

        except Exception as e:
            self.logger.error(f"Error getting entry details: {str(e)}")
            return None

    def _transform_entry(self, entry: Dict) -> Dict[str, Any]:
        """Transform InterPro entry to standard format."""
        metadata = entry.get('metadata', {})

        return {
            'identifier': metadata.get('accession'),
            'name': metadata.get('name', {}).get('name', ''),
            'description': metadata.get('description', [''])[0] if metadata.get('description') else '',
            'entity_type': 'mechanism',
            'mechanism_class': metadata.get('type'),
            'source_database': 'InterPro',
            'confidence_score': 0.90,
            'evidence_strength': 'computational',
            'metadata': {
                'type': metadata.get('type'),
                'member_databases': metadata.get('member_databases'),
                'go_terms': metadata.get('go_terms', [])
            }
        }


class BRENDAExtractor(BaseExtractor):
    """
    Extract enzyme catalytic mechanisms from BRENDA.

    IMPORTANT: Requires authentication (email + hashed password).

    Focuses on:
    - EC hierarchy and classification
    - Catalytic mechanisms
    - Cofactor requirements
    - Reaction mechanisms
    """

    def __init__(self, email: str = None, password: str = None, **kwargs):
        """
        Initialize BRENDA extractor.

        Args:
            email: BRENDA account email
            password: BRENDA account password (will be hashed)
        """
        super().__init__(
            rate_limit_calls=5,  # Conservative for SOAP API
            rate_limit_period=1.0,
            **kwargs
        )

        self.email = email
        if password:
            self.password_hash = hashlib.sha256(password.encode()).hexdigest()
        else:
            self.password_hash = None

        # SOAP client initialization
        self.wsdl_url = "https://www.brenda-enzymes.org/soap/brenda_zeep.wsdl"
        self.client = None

        if email and password:
            try:
                self.client = Client(self.wsdl_url)
                self.logger.info("BRENDA SOAP client initialized")
            except Exception as e:
                self.logger.error(f"Error initializing BRENDA client: {str(e)}")

    def extract(
        self,
        ec_class: str = None,
        max_enzymes: int = 500
    ) -> List[Dict[str, Any]]:
        """
        Extract enzyme data from BRENDA.

        Args:
            ec_class: EC class filter (e.g., '1.*.*.*' for oxidoreductases)
            max_enzymes: Maximum enzymes to extract

        Returns:
            List of enzyme dictionaries
        """
        if not self.client:
            self.logger.error("BRENDA client not initialized. Provide email and password.")
            return []

        self.logger.info(f"Starting BRENDA extraction (EC class: {ec_class or 'all'})...")

        # Get EC numbers
        ec_numbers = self.get_ec_numbers(ec_class)

        # Get details for each EC number
        enzymes = []
        for ec_number in ec_numbers[:max_enzymes]:
            enzyme_data = self.get_enzyme_details(ec_number)
            if enzyme_data:
                enzymes.append(enzyme_data)
                self.stats['items_extracted'] += 1

        return enzymes

    def get_ec_numbers(self, ec_class: str = None) -> List[str]:
        """
        Get list of EC numbers.

        Args:
            ec_class: EC class filter (e.g., '1.*.*.*')

        Returns:
            List of EC numbers
        """
        if not self.client:
            return []

        try:
            # Build query
            query = f"ecNumber={ec_class}" if ec_class else "ecNumber=*"

            # Call SOAP method
            result = self.client.service.getEcNumber(self.email, self.password_hash, query)

            # Parse result (format: "EC:1.1.1.1\nEC:1.1.1.2\n...")
            ec_numbers = []
            for line in result.split('\n'):
                if line.startswith('EC:'):
                    ec_numbers.append(line.replace('EC:', '').strip())

            self.logger.info(f"Found {len(ec_numbers)} EC numbers")
            return ec_numbers

        except Exception as e:
            self.logger.error(f"Error getting EC numbers: {str(e)}")
            return []

    def get_enzyme_details(self, ec_number: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about an enzyme.

        Args:
            ec_number: EC number (e.g., '1.1.1.1')

        Returns:
            Enzyme details dictionary
        """
        if not self.client:
            return None

        try:
            # Get enzyme information
            query = f"ecNumber={ec_number}"

            # Get recommended name
            name_result = self.client.service.getRecommendedName(
                self.email, self.password_hash, query
            )

            # Get systematic name
            systematic_result = self.client.service.getSystematicName(
                self.email, self.password_hash, query
            )

            # Get reaction
            reaction_result = self.client.service.getReaction(
                self.email, self.password_hash, query
            )

            # Get cofactors
            cofactor_result = self.client.service.getCofactor(
                self.email, self.password_hash, query
            )

            return self._transform_enzyme(
                ec_number,
                name_result,
                systematic_result,
                reaction_result,
                cofactor_result
            )

        except Exception as e:
            self.logger.error(f"Error getting enzyme details for {ec_number}: {str(e)}")
            return None

    def _transform_enzyme(
        self,
        ec_number: str,
        name: str,
        systematic_name: str,
        reaction: str,
        cofactors: str
    ) -> Dict[str, Any]:
        """Transform BRENDA enzyme data to standard format."""
        # Parse names
        recommended_name = self._parse_brenda_result(name)
        systematic = self._parse_brenda_result(systematic_name)
        reaction_text = self._parse_brenda_result(reaction)
        cofactor_list = self._parse_brenda_result(cofactors)

        return {
            'identifier': f"EC:{ec_number}",
            'name': recommended_name or systematic or f"Enzyme {ec_number}",
            'description': reaction_text or '',
            'entity_type': 'enzyme',
            'ec_number': ec_number,
            'catalytic_mechanism': self._infer_mechanism_from_ec(ec_number),
            'source_database': 'BRENDA',
            'confidence_score': 0.90,
            'evidence_strength': 'experimental',
            'metadata': {
                'systematic_name': systematic,
                'cofactors': cofactor_list,
                'ec_class': ec_number.split('.')[0] if '.' in ec_number else None
            }
        }

    def _parse_brenda_result(self, result: str) -> Optional[str]:
        """Parse BRENDA SOAP result string."""
        if not result or result.strip() == '':
            return None

        # BRENDA results are in format: "field#value#...\n"
        lines = result.split('\n')
        values = []

        for line in lines:
            if '#' in line:
                parts = line.split('#')
                if len(parts) >= 2:
                    values.append(parts[1])

        return values[0] if values else None

    def _infer_mechanism_from_ec(self, ec_number: str) -> str:
        """Infer catalytic mechanism from EC class."""
        if not ec_number:
            return 'unknown'

        ec_class = ec_number.split('.')[0] if '.' in ec_number else ec_number

        mechanism_map = {
            '1': 'oxidoreductase',
            '2': 'transferase',
            '3': 'hydrolase',
            '4': 'lyase',
            '5': 'isomerase',
            '6': 'ligase',
            '7': 'translocase'
        }

        return mechanism_map.get(ec_class, 'unknown')
