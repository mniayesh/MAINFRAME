#!/usr/bin/env python3
"""
BioModels harvester V2 - Using libsbml for proper SBML parsing.

This version uses the official libsbml library to properly parse SBML models
and extract reaction kinetics with full MathML support.
"""

import requests
import libsbml
import sympy
from pathlib import Path
import logging
import time
from expand_base import get_conn, add_formula, get_source_id, get_category_id, print_summary, count_formulas

log = logging.getLogger('bioformulas.biomodels_v2')

BIOMODELS_API = "https://www.ebi.ac.uk/biomodels"
BIOMODELS_SEARCH = f"{BIOMODELS_API}/search"
BIOMODELS_MODEL = f"{BIOMODELS_API}/model/download"


class BioModelsHarvesterV2:
    """Extract formulas from BioModels using libsbml."""

    def __init__(self, conn, output_dir='data/biomodels'):
        self.conn = conn
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.source_id = get_source_id(conn, 'BioModels Database')
        self.stats = {
            'models_processed': 0,
            'reactions_found': 0,
            'formulas_extracted': 0,
            'errors': 0
        }

    def mathml_to_latex(self, math_ast):
        """Convert SBML MathML AST to LaTeX using libsbml."""
        try:
            # Get formula string from AST
            formula = libsbml.formulaToL3String(math_ast)

            if not formula or formula == 'FLUX_VALUE':
                return None

            # Convert to sympy and then to LaTeX
            try:
                # Clean up the formula
                formula_clean = formula.replace('^', '**')

                # Parse as sympy expression
                expr = sympy.sympify(formula_clean)
                latex = sympy.latex(expr)

                return latex
            except Exception:
                # Fallback: return the formula string as-is
                return formula

        except Exception as e:
            log.debug(f"    MathML conversion failed: {e}")
            return None

    def extract_reactions(self, sbml_doc, model_id):
        """Extract reactions from SBML document using libsbml."""
        formulas = []

        model = sbml_doc.getModel()
        if not model:
            log.warning(f"  No model found in {model_id}")
            return formulas

        num_reactions = model.getNumReactions()
        log.info(f"  Found {num_reactions} reactions in model")
        self.stats['reactions_found'] += num_reactions

        for i in range(num_reactions):
            reaction = model.getReaction(i)

            try:
                rxn_id = reaction.getId()
                rxn_name = reaction.getName() or rxn_id

                # Get kinetic law
                kinetic_law = reaction.getKineticLaw()
                if not kinetic_law:
                    continue

                # Get math
                math = kinetic_law.getMath()
                if not math:
                    continue

                # Convert to LaTeX
                latex = self.mathml_to_latex(math)
                if not latex or latex == 'FLUX_VALUE':
                    continue

                # Get reactants and products
                reactants = []
                for j in range(reaction.getNumReactants()):
                    reactant = reaction.getReactant(j)
                    species = model.getSpecies(reactant.getSpecies())
                    if species:
                        reactants.append(species.getName() or species.getId())

                products = []
                for j in range(reaction.getNumProducts()):
                    product = reaction.getProduct(j)
                    species = model.getSpecies(product.getSpecies())
                    if species:
                        products.append(species.getName() or species.getId())

                # Create formula
                formulas.append({
                    'name': f"{model_id}: {rxn_name[:100]}",
                    'latex': f"v = {latex}",
                    'description': f"Reaction rate law from BioModels {model_id}: {rxn_name}",
                    'formula_type': 'rate_equation',
                    'domain': 'biochemistry',
                    'model_origin': model_id,
                    'reaction_id': rxn_id,
                    'reactants': ', '.join(reactants[:5]),  # Limit to 5
                    'products': ', '.join(products[:5])
                })

            except Exception as e:
                log.debug(f"    Error parsing reaction {i}: {e}")
                continue

        return formulas

    def extract_rate_rules(self, sbml_doc, model_id):
        """Extract ODE rate rules from SBML document."""
        formulas = []

        model = sbml_doc.getModel()
        if not model:
            return formulas

        num_rules = model.getNumRules()

        for i in range(num_rules):
            rule = model.getRule(i)

            if rule.getTypeCode() == libsbml.SBML_RATE_RULE:
                try:
                    variable = rule.getVariable()
                    math = rule.getMath()

                    if math:
                        latex = self.mathml_to_latex(math)
                        if latex:
                            formulas.append({
                                'name': f"{model_id}: d{variable}/dt",
                                'latex': f"\\frac{{d[{variable}]}}{{dt}} = {latex}",
                                'description': f"ODE rate rule from BioModels {model_id}",
                                'formula_type': 'ODE',
                                'domain': 'systems-biology',
                                'model_origin': model_id
                            })
                except Exception as e:
                    log.debug(f"    Error parsing rate rule {i}: {e}")
                    continue

        return formulas

    def process_model(self, model_id):
        """Download and extract formulas from a BioModels model."""
        log.info(f"Processing model: {model_id}")

        try:
            # Check if already downloaded
            filepath = self.output_dir / f"{model_id}.xml"

            if not filepath.exists():
                # Download
                url = f"{BIOMODELS_MODEL}/{model_id}?filename={model_id}_url.xml"
                resp = requests.get(url, timeout=30)
                resp.raise_for_status()
                filepath.write_text(resp.text)
                log.info(f"  Downloaded {model_id}")
            else:
                log.info(f"  Using cached {model_id}")

            # Parse with libsbml
            reader = libsbml.SBMLReader()
            sbml_doc = reader.readSBML(str(filepath))

            if sbml_doc.getNumErrors() > 0:
                log.warning(f"  SBML has {sbml_doc.getNumErrors()} errors")

            # Extract formulas
            formulas = []
            formulas.extend(self.extract_reactions(sbml_doc, model_id))
            formulas.extend(self.extract_rate_rules(sbml_doc, model_id))

            log.info(f"  ✓ Extracted {len(formulas)} formulas from {model_id}")

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
                    name=f['name'][:200],
                    latex=f['latex'],
                    desc=f['description'],
                    ftype=f['formula_type'],
                    cat_id=cat_id,
                    src_id=self.source_id,
                    domain=f.get('domain'),
                    model_origin=f.get('model_origin')
                )

            except Exception as e:
                log.warning(f"  Error saving formula: {e}")

    def harvest(self, model_ids=None, max_models=10, delay=1.0):
        """
        Harvest formulas from BioModels.

        Args:
            model_ids: List of specific model IDs to process (or None to search)
            max_models: Maximum models to process
            delay: Delay between downloads
        """
        log.info("="*60)
        log.info("BioModels Harvester V2 (libsbml)")
        log.info("="*60)

        start_count = count_formulas(self.conn)

        # Use provided model IDs or search
        if not model_ids:
            # Search for models
            log.info("Searching for curated models...")
            try:
                params = {'query': 'curated', 'numResults': max_models, 'format': 'json'}
                resp = requests.get(BIOMODELS_SEARCH, params=params, timeout=30)
                resp.raise_for_status()
                data = resp.json()
                models = data.get('models', [])
                model_ids = [m.get('id') or m.get('modelId') for m in models[:max_models]]
                model_ids = [m for m in model_ids if m]
            except Exception as e:
                log.error(f"Search failed: {e}")
                return

        log.info(f"Processing {len(model_ids)} models...")

        all_formulas = []
        for i, model_id in enumerate(model_ids, 1):
            log.info(f"[{i}/{len(model_ids)}] {model_id}")

            formulas = self.process_model(model_id)
            all_formulas.extend(formulas)

            # Save periodically
            if len(all_formulas) >= 100:
                self.save_formulas(all_formulas)
                all_formulas = []

            time.sleep(delay)

        # Save remaining
        if all_formulas:
            self.save_formulas(all_formulas)

        # Summary
        log.info("="*60)
        log.info(f"BioModels V2 Harvest Complete")
        log.info(f"  Models processed: {self.stats['models_processed']}")
        log.info(f"  Reactions found: {self.stats['reactions_found']}")
        log.info(f"  Formulas extracted: {self.stats['formulas_extracted']}")
        log.info(f"  Errors: {self.stats['errors']}")
        log.info("="*60)

        print_summary(self.conn, "BioModels V2", start_count)


def main():
    """Run BioModels V2 harvester on cached files."""
    conn = get_conn()

    try:
        harvester = BioModelsHarvesterV2(conn)

        # Process the 5 files we already downloaded
        cached_models = [
            'MODEL1409240004',
            'MODEL1509220029',
            'MODEL1509220030',
            'MODEL1509220031',
            'MODEL1509220032'
        ]

        log.info("Processing cached BioModels files with libsbml...")
        harvester.harvest(model_ids=cached_models, delay=0.1)

    finally:
        conn.close()


if __name__ == '__main__':
    main()
