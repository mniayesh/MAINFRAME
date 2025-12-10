#!/usr/bin/env python3
"""
PARALLEL BioModels Harvester - Maximum speed extraction.

Uses concurrent processing for:
- Parallel downloads (10x faster)
- Parallel SBML parsing (CPU cores)
- Batch database writes
"""

import requests
import libsbml
import sympy
from pathlib import Path
import logging
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from threading import Lock
import queue
from expand_base import get_conn, add_formula, get_source_id, get_category_id, print_summary, count_formulas

log = logging.getLogger('bioformulas.biomodels_parallel')

BIOMODELS_API = "https://www.ebi.ac.uk/biomodels"
BIOMODELS_SEARCH = f"{BIOMODELS_API}/search"
BIOMODELS_MODEL = f"{BIOMODELS_API}/model/download"


class ParallelBioModelsHarvester:
    """High-speed parallel formula extraction."""

    def __init__(self, conn, output_dir='data/biomodels', max_workers=10):
        self.conn = conn
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.source_id = get_source_id(conn, 'BioModels Database')
        self.max_workers = max_workers
        self.db_lock = Lock()

        self.stats = {
            'models_processed': 0,
            'reactions_found': 0,
            'formulas_extracted': 0,
            'errors': 0,
            'cache_hits': 0
        }

    def mathml_to_latex(self, math_ast):
        """Convert SBML MathML AST to LaTeX."""
        try:
            formula = libsbml.formulaToL3String(math_ast)
            if not formula or formula == 'FLUX_VALUE':
                return None

            try:
                formula_clean = formula.replace('^', '**')
                expr = sympy.sympify(formula_clean)
                latex = sympy.latex(expr)
                return latex
            except:
                return formula
        except Exception as e:
            return None

    def download_model(self, model_id):
        """Download a single model (threaded)."""
        filepath = self.output_dir / f"{model_id}.xml"

        # Check cache first
        if filepath.exists():
            self.stats['cache_hits'] += 1
            return filepath

        try:
            url = f"{BIOMODELS_MODEL}/{model_id}?filename={model_id}_url.xml"
            resp = requests.get(url, timeout=30)
            resp.raise_for_status()
            filepath.write_text(resp.text)
            return filepath
        except Exception as e:
            log.error(f"Download failed for {model_id}: {e}")
            return None

    def parse_model(self, filepath):
        """Parse SBML and extract formulas (can be parallelized)."""
        if not filepath or not filepath.exists():
            return []

        model_id = filepath.stem
        formulas = []

        try:
            reader = libsbml.SBMLReader()
            sbml_doc = reader.readSBML(str(filepath))
            model = sbml_doc.getModel()

            if not model:
                return formulas

            # Extract reactions
            num_reactions = model.getNumReactions()
            self.stats['reactions_found'] += num_reactions

            for i in range(num_reactions):
                reaction = model.getReaction(i)

                try:
                    rxn_id = reaction.getId()
                    rxn_name = reaction.getName() or rxn_id

                    kinetic_law = reaction.getKineticLaw()
                    if not kinetic_law:
                        continue

                    math = kinetic_law.getMath()
                    if not math:
                        continue

                    latex = self.mathml_to_latex(math)
                    if not latex or latex == 'FLUX_VALUE':
                        continue

                    # Get reactants/products
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

                    formulas.append({
                        'name': f"{model_id}: {rxn_name[:100]}",
                        'latex': f"v = {latex}",
                        'description': f"Reaction rate law from BioModels {model_id}: {rxn_name}",
                        'formula_type': 'rate_equation',
                        'domain': 'biochemistry',
                        'model_origin': model_id,
                        'reactants': ', '.join(reactants[:5]),
                        'products': ', '.join(products[:5])
                    })
                except Exception as e:
                    continue

            # Extract rate rules
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
                        continue

            return formulas

        except Exception as e:
            log.error(f"Parse error for {filepath.name}: {e}")
            self.stats['errors'] += 1
            return []

    def save_formulas_batch(self, formulas):
        """Thread-safe batch database write."""
        if not formulas:
            return

        with self.db_lock:
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

                    self.stats['formulas_extracted'] += 1

                except Exception as e:
                    log.warning(f"Save error: {e}")

    def process_model(self, model_id):
        """Download + parse a single model."""
        log.info(f"  Processing {model_id}")

        # Download
        filepath = self.download_model(model_id)
        if not filepath:
            return []

        # Parse
        formulas = self.parse_model(filepath)

        self.stats['models_processed'] += 1

        if formulas:
            log.info(f"  ✓ {model_id}: {len(formulas)} formulas")

        return formulas

    def harvest_parallel(self, model_ids, download_workers=10, parse_workers=4):
        """
        Parallel harvest with separate download/parse pools.

        Args:
            model_ids: List of model IDs to process
            download_workers: Concurrent downloads (I/O bound)
            parse_workers: Concurrent parsers (CPU bound)
        """
        log.info("="*60)
        log.info(f"PARALLEL BioModels Harvester")
        log.info(f"  Download workers: {download_workers}")
        log.info(f"  Parse workers: {parse_workers}")
        log.info(f"  Models to process: {len(model_ids)}")
        log.info("="*60)

        start_count = count_formulas(self.conn)
        start_time = time.time()

        # Stage 1: Parallel downloads
        log.info("\n[STAGE 1] Downloading models in parallel...")
        filepaths = []

        with ThreadPoolExecutor(max_workers=download_workers) as executor:
            future_to_model = {executor.submit(self.download_model, mid): mid for mid in model_ids}

            for future in as_completed(future_to_model):
                model_id = future_to_model[future]
                try:
                    filepath = future.result()
                    if filepath:
                        filepaths.append(filepath)
                except Exception as e:
                    log.error(f"  Error downloading {model_id}: {e}")

        log.info(f"  Downloaded/cached: {len(filepaths)} files")

        # Stage 2: Parallel parsing
        log.info("\n[STAGE 2] Parsing models in parallel...")
        all_formulas = []

        with ThreadPoolExecutor(max_workers=parse_workers) as executor:
            future_to_file = {executor.submit(self.parse_model, fp): fp for fp in filepaths}

            for future in as_completed(future_to_file):
                try:
                    formulas = future.result()
                    if formulas:
                        all_formulas.extend(formulas)

                        # Batch save every 100 formulas
                        if len(all_formulas) >= 100:
                            self.save_formulas_batch(all_formulas)
                            all_formulas = []

                except Exception as e:
                    log.error(f"  Parse error: {e}")

        # Save remaining
        if all_formulas:
            self.save_formulas_batch(all_formulas)

        # Summary
        elapsed = time.time() - start_time

        log.info("\n" + "="*60)
        log.info(f"PARALLEL HARVEST COMPLETE")
        log.info(f"  Time: {elapsed:.1f}s")
        log.info(f"  Models processed: {self.stats['models_processed']}")
        log.info(f"  Cache hits: {self.stats['cache_hits']}")
        log.info(f"  Reactions found: {self.stats['reactions_found']}")
        log.info(f"  Formulas extracted: {self.stats['formulas_extracted']}")
        log.info(f"  Errors: {self.stats['errors']}")
        log.info(f"  Speed: {self.stats['models_processed'] / elapsed:.1f} models/sec")
        log.info(f"  Speed: {self.stats['formulas_extracted'] / elapsed:.1f} formulas/sec")
        log.info("="*60)

        print_summary(self.conn, "BioModels Parallel", start_count)

    def search_kinetic_models(self, max_results=50):
        """Search for kinetic (non-FBA) models."""
        log.info("Searching for kinetic models...")

        all_models = set()

        queries = [
            'kinetic',
            'enzyme kinetics',
            'michaelis',
            'mapk',
            'calcium signaling',
            'glycolysis kinetic',
            'cell cycle'
        ]

        for query in queries:
            try:
                params = {'query': query, 'numResults': 20, 'format': 'json'}
                resp = requests.get(BIOMODELS_SEARCH, params=params, timeout=30)
                resp.raise_for_status()
                data = resp.json()

                models = data.get('models', [])
                for m in models:
                    model_id = m.get('id') or m.get('modelId')
                    if model_id and model_id.startswith('BIOMD'):
                        all_models.add(model_id)

            except Exception as e:
                log.warning(f"Search '{query}' failed: {e}")

        model_list = sorted(list(all_models))[:max_results]
        log.info(f"Found {len(model_list)} unique kinetic models")

        return model_list


def main():
    """Run parallel harvester."""
    import argparse

    parser = argparse.ArgumentParser(description='Parallel BioModels harvester')
    parser.add_argument('--max-models', type=int, default=50,
                        help='Maximum models to harvest')
    parser.add_argument('--download-workers', type=int, default=10,
                        help='Concurrent downloads')
    parser.add_argument('--parse-workers', type=int, default=4,
                        help='Concurrent parsers')

    args = parser.parse_args()

    conn = get_conn()

    try:
        harvester = ParallelBioModelsHarvester(conn, max_workers=args.download_workers)

        # Search for kinetic models
        model_ids = harvester.search_kinetic_models(max_results=args.max_models)

        # Harvest in parallel
        harvester.harvest_parallel(
            model_ids,
            download_workers=args.download_workers,
            parse_workers=args.parse_workers
        )

    finally:
        conn.close()


if __name__ == '__main__':
    main()
