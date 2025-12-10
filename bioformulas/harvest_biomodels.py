#!/usr/bin/env python3
"""
Harvest formulas from BioModels Database via SBML files.
BioModels: https://www.ebi.ac.uk/biomodels/
"""

import requests
import xml.etree.ElementTree as ET
from pathlib import Path
import logging
import time
from expand_base import get_conn, add_formula, get_source_id, get_category_id, add_enzyme, print_summary, count_formulas

log = logging.getLogger('bioformulas.biomodels')

# BioModels REST API
BIOMODELS_API = "https://www.ebi.ac.uk/biomodels"
BIOMODELS_SEARCH = f"{BIOMODELS_API}/search"
BIOMODELS_MODEL = f"{BIOMODELS_API}/model/download"

# SBML namespaces
SBML_NS = {
    'sbml': 'http://www.sbml.org/sbml/level2/version4',
    'sbml3': 'http://www.sbml.org/sbml/level3/version1/core',
    'mathml': 'http://www.w3.org/1998/Math/MathML'
}

class BioModelsHarvester:
    """Extract formulas from BioModels SBML files."""

    def __init__(self, conn, output_dir='data/biomodels'):
        self.conn = conn
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.source_id = get_source_id(conn, 'BioModels Database')
        self.stats = {'models_processed': 0, 'formulas_extracted': 0, 'errors': 0}

    def search_models(self, query='*', max_results=100):
        """Search BioModels database."""
        log.info(f"Searching BioModels: query='{query}', max={max_results}")

        try:
            params = {
                'query': query,
                'numResults': max_results,
                'format': 'json'
            }
            resp = requests.get(BIOMODELS_SEARCH, params=params, timeout=30)
            resp.raise_for_status()
            data = resp.json()

            models = data.get('models', [])
            log.info(f"Found {len(models)} models")
            return models

        except Exception as e:
            log.error(f"Search failed: {e}")
            return []

    def download_sbml(self, model_id):
        """Download SBML file for a model."""
        try:
            url = f"{BIOMODELS_MODEL}/{model_id}?filename={model_id}_url.xml"
            resp = requests.get(url, timeout=30)
            resp.raise_for_status()

            # Save locally
            filepath = self.output_dir / f"{model_id}.xml"
            filepath.write_text(resp.text)

            log.info(f"  Downloaded {model_id}")
            return filepath

        except Exception as e:
            log.error(f"  Download failed for {model_id}: {e}")
            return None

    def parse_mathml(self, math_element):
        """Convert MathML to LaTeX (simplified)."""
        # This is a simplified converter - real MathML->LaTeX needs more work
        try:
            if math_element is None:
                return None

            # Extract text content
            text = ''.join(math_element.itertext())
            return text.strip() if text.strip() else None
        except:
            return None

    def extract_reactions(self, root, model_id):
        """Extract reaction rate laws from SBML."""
        formulas = []

        # Try both SBML level 2 and 3 namespaces
        for ns_key in ['sbml', 'sbml3']:
            reactions = root.findall(f'.//{{{SBML_NS[ns_key]}}}reaction')

            for reaction in reactions:
                try:
                    rxn_id = reaction.get('id', 'unknown')
                    rxn_name = reaction.get('name', rxn_id)

                    # Get kinetic law
                    kinetic_law = reaction.find(f'{{{SBML_NS[ns_key]}}}kineticLaw')
                    if kinetic_law is None:
                        continue

                    # Extract MathML
                    math = kinetic_law.find('.//{http://www.w3.org/1998/Math/MathML}math')
                    if math is not None:
                        # Get reactants and products
                        reactants = [r.get('species', '') for r in reaction.findall(f'.//{{{SBML_NS[ns_key]}}}reactant')]
                        products = [p.get('species', '') for p in reaction.findall(f'.//{{{SBML_NS[ns_key]}}}product')]

                        formula_text = self.parse_mathml(math) or rxn_id

                        formulas.append({
                            'name': f"{model_id}: {rxn_name}",
                            'latex': formula_text,
                            'description': f"Reaction rate law from BioModels {model_id}",
                            'formula_type': 'rate_equation',
                            'domain': 'biochemistry',
                            'model_origin': model_id,
                            'mathml': ET.tostring(math, encoding='unicode') if math is not None else None,
                            'reactants': ','.join(reactants),
                            'products': ','.join(products)
                        })

                except Exception as e:
                    log.warning(f"    Error parsing reaction {rxn_id}: {e}")
                    continue

        return formulas

    def extract_odes(self, root, model_id):
        """Extract ODE rate rules from SBML."""
        formulas = []

        for ns_key in ['sbml', 'sbml3']:
            # Rate rules
            rate_rules = root.findall(f'.//{{{SBML_NS[ns_key]}}}rateRule')

            for rule in rate_rules:
                try:
                    variable = rule.get('variable', 'unknown')
                    math = rule.find('.//{http://www.w3.org/1998/Math/MathML}math')

                    if math is not None:
                        formula_text = self.parse_mathml(math) or variable

                        formulas.append({
                            'name': f"{model_id}: d{variable}/dt",
                            'latex': f"\\frac{{d[{variable}]}}{{dt}} = {formula_text}",
                            'description': f"ODE rate rule from BioModels {model_id}",
                            'formula_type': 'ODE',
                            'domain': 'systems-biology',
                            'model_origin': model_id
                        })

                except Exception as e:
                    log.warning(f"    Error parsing rate rule: {e}")
                    continue

        return formulas

    def process_model(self, model_id):
        """Download and extract all formulas from a model."""
        log.info(f"Processing model: {model_id}")

        try:
            # Download SBML
            filepath = self.download_sbml(model_id)
            if not filepath or not filepath.exists():
                self.stats['errors'] += 1
                return []

            # Parse XML
            tree = ET.parse(filepath)
            root = tree.getroot()

            # Extract formulas
            formulas = []
            formulas.extend(self.extract_reactions(root, model_id))
            formulas.extend(self.extract_odes(root, model_id))

            log.info(f"  Extracted {len(formulas)} formulas from {model_id}")
            self.stats['models_processed'] += 1
            self.stats['formulas_extracted'] += len(formulas)

            return formulas

        except Exception as e:
            log.error(f"  Error processing {model_id}: {e}")
            self.stats['errors'] += 1
            return []

    def save_formulas(self, formulas):
        """Save extracted formulas to database."""
        for f in formulas:
            try:
                # Determine category
                cat_id = None
                if 'enzyme' in f.get('name', '').lower():
                    cat_id = get_category_id(self.conn, 'Enzyme Kinetics')
                elif f['formula_type'] == 'ODE':
                    cat_id = get_category_id(self.conn, 'Systems Biology')
                else:
                    cat_id = get_category_id(self.conn, 'Metabolic Pathways')

                if not cat_id:
                    cat_id = get_category_id(self.conn, 'Biochemistry')

                # Add formula
                add_formula(
                    self.conn,
                    name=f['name'],
                    latex=f['latex'],
                    desc=f['description'],
                    ftype=f['formula_type'],
                    cat_id=cat_id,
                    src_id=self.source_id,
                    mathml=f.get('mathml'),
                    domain=f.get('domain'),
                    model_origin=f.get('model_origin')
                )

            except Exception as e:
                log.warning(f"  Error saving formula '{f['name']}': {e}")

    def harvest(self, query='curated', max_models=50, delay=1.0):
        """
        Main harvesting workflow.

        Args:
            query: Search query ('curated', 'metabolism', 'signaling', etc.)
            max_models: Maximum number of models to process
            delay: Delay between requests (seconds)
        """
        log.info("="*60)
        log.info("BioModels Harvester Starting")
        log.info("="*60)

        start_count = count_formulas(self.conn)

        # Search for models
        models = self.search_models(query, max_models)

        # Process each model
        all_formulas = []
        for i, model_info in enumerate(models[:max_models], 1):
            model_id = model_info.get('id') or model_info.get('modelId')
            if not model_id:
                continue

            log.info(f"[{i}/{len(models)}] {model_id}")
            formulas = self.process_model(model_id)
            all_formulas.extend(formulas)

            # Save periodically
            if len(all_formulas) >= 100:
                self.save_formulas(all_formulas)
                all_formulas = []

            # Rate limiting
            time.sleep(delay)

        # Save remaining
        if all_formulas:
            self.save_formulas(all_formulas)

        # Summary
        log.info("="*60)
        log.info(f"BioModels Harvest Complete")
        log.info(f"  Models processed: {self.stats['models_processed']}")
        log.info(f"  Formulas extracted: {self.stats['formulas_extracted']}")
        log.info(f"  Errors: {self.stats['errors']}")
        log.info("="*60)

        print_summary(self.conn, "BioModels", start_count)


def main():
    """Run BioModels harvester."""
    conn = get_conn()

    try:
        harvester = BioModelsHarvester(conn)

        # Harvest curated models
        harvester.harvest(query='curated', max_models=20, delay=1.5)

    finally:
        conn.close()


if __name__ == '__main__':
    main()
