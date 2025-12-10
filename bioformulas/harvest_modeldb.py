#!/usr/bin/env python3
"""
Harvest formulas from ModelDB (computational neuroscience).
ModelDB: https://modeldb.science/

Extracts equations from:
- NEURON .mod files (ion channels, synapses)
- NeuroML files
- Model metadata
"""

import requests
import re
from pathlib import Path
import logging
import time
from bs4 import BeautifulSoup
from expand_base import get_conn, add_formula, get_source_id, get_category_id
from expand_base import add_ion_channel, add_synapse, add_neuron, print_summary, count_formulas

log = logging.getLogger('bioformulas.modeldb')

MODELDB_BASE = "https://modeldb.science"
MODELDB_API = f"{MODELDB_BASE}/api/v1"


class MODFileParser:
    """Parse NEURON .mod files to extract equations."""

    def __init__(self):
        self.equations = []

    def parse_derivative_block(self, text):
        """Extract ODEs from DERIVATIVE block."""
        equations = []

        # Find DERIVATIVE blocks
        deriv_pattern = r'DERIVATIVE\s+(\w+)\s*\{([^}]+)\}'
        for match in re.finditer(deriv_pattern, text, re.DOTALL):
            block_name = match.group(1)
            block_content = match.group(2)

            # Find all prime (derivative) assignments
            # Example: m' = (minf - m)/mtau
            prime_pattern = r"(\w+)'\s*=\s*([^;\n]+)"
            for var_match in re.finditer(prime_pattern, block_content):
                var = var_match.group(1)
                expr = var_match.group(2).strip()

                equations.append({
                    'variable': var,
                    'expression': expr,
                    'block': block_name,
                    'type': 'ODE'
                })

        return equations

    def parse_kinetic_block(self, text):
        """Extract kinetic (Markov) equations from KINETIC block."""
        equations = []

        kinetic_pattern = r'KINETIC\s+(\w+)\s*\{([^}]+)\}'
        for match in re.finditer(kinetic_pattern, text, re.DOTALL):
            block_name = match.group(1)
            block_content = match.group(2)

            # Find transition rates: ~ alpha <-> beta
            transition_pattern = r'~\s*([^<\->]+)\s*<->\s*([^;\n]+)'
            for trans in re.finditer(transition_pattern, block_content):
                states = trans.group(1).strip()
                rates = trans.group(2).strip()

                equations.append({
                    'states': states,
                    'rates': rates,
                    'block': block_name,
                    'type': 'kinetic'
                })

        return equations

    def parse_procedure(self, text, proc_name):
        """Extract rate functions from PROCEDURE blocks."""
        equations = []

        proc_pattern = rf'PROCEDURE\s+{proc_name}\s*\([^)]*\)\s*\{{([^}}]+)\}}'
        match = re.search(proc_pattern, text, re.DOTALL)
        if not match:
            return equations

        content = match.group(1)

        # Find assignments
        assign_pattern = r'(\w+)\s*=\s*([^;\n]+)'
        for assign in re.finditer(assign_pattern, content):
            var = assign.group(1)
            expr = assign.group(2).strip()

            equations.append({
                'variable': var,
                'expression': expr,
                'procedure': proc_name,
                'type': 'rate_function'
            })

        return equations

    def extract_metadata(self, text):
        """Extract metadata from comments."""
        metadata = {
            'title': None,
            'channel_type': None,
            'ions': [],
            'range_vars': [],
            'global_vars': []
        }

        # TITLE
        title_match = re.search(r'TITLE\s+(.+)', text)
        if title_match:
            metadata['title'] = title_match.group(1).strip()

        # USEION
        for ion_match in re.finditer(r'USEION\s+(\w+)', text):
            metadata['ions'].append(ion_match.group(1))

        # RANGE
        range_match = re.search(r'RANGE\s+([^\n]+)', text)
        if range_match:
            metadata['range_vars'] = [v.strip() for v in range_match.group(1).split(',')]

        # GLOBAL
        global_match = re.search(r'GLOBAL\s+([^\n]+)', text)
        if global_match:
            metadata['global_vars'] = [v.strip() for v in global_match.group(1).split(',')]

        return metadata

    def parse(self, mod_text, filename='unknown'):
        """Parse a .mod file and extract all equations."""
        result = {
            'filename': filename,
            'metadata': self.extract_metadata(mod_text),
            'odes': self.parse_derivative_block(mod_text),
            'kinetics': self.parse_kinetic_block(mod_text),
            'rates': []
        }

        # Common rate function names
        for proc in ['rates', 'rate', 'trates', 'vtrap']:
            result['rates'].extend(self.parse_procedure(mod_text, proc))

        return result


class ModelDBHarvester:
    """Harvest formulas from ModelDB."""

    def __init__(self, conn, output_dir='data/modeldb'):
        self.conn = conn
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.source_id = get_source_id(conn, 'ModelDB')
        self.parser = MODFileParser()
        self.stats = {'models_processed': 0, 'mod_files': 0, 'formulas_extracted': 0, 'errors': 0}

    def search_models(self, query='ion channel', max_results=50):
        """Search ModelDB for models."""
        log.info(f"Searching ModelDB: '{query}'")

        try:
            # ModelDB search page
            search_url = f"{MODELDB_BASE}/ModelList"
            params = {'id': 0, 'celType': query}

            resp = requests.get(search_url, params=params, timeout=30)
            resp.raise_for_status()

            soup = BeautifulSoup(resp.text, 'html.parser')

            # Extract model IDs from links
            model_ids = []
            for link in soup.find_all('a', href=True):
                href = link['href']
                if '/ShowModel' in href or '/model=' in href:
                    # Extract model ID
                    match = re.search(r'model=(\d+)', href)
                    if match:
                        model_ids.append(match.group(1))

            model_ids = list(set(model_ids))[:max_results]
            log.info(f"Found {len(model_ids)} models")
            return model_ids

        except Exception as e:
            log.error(f"Search failed: {e}")
            return []

    def download_model_files(self, model_id):
        """Download model archive and extract .mod files."""
        try:
            # Download model zip
            download_url = f"{MODELDB_BASE}/{model_id}?tab=2"  # Files tab
            resp = requests.get(download_url, timeout=30)
            resp.raise_for_status()

            soup = BeautifulSoup(resp.text, 'html.parser')

            # Find .mod file links
            mod_files = []
            for link in soup.find_all('a', href=True):
                href = link['href']
                if href.endswith('.mod'):
                    mod_url = MODELDB_BASE + href if not href.startswith('http') else href
                    mod_files.append({
                        'url': mod_url,
                        'filename': Path(href).name
                    })

            log.info(f"  Found {len(mod_files)} .mod files")
            return mod_files

        except Exception as e:
            log.error(f"  Download failed: {e}")
            return []

    def download_mod_file(self, url, filename):
        """Download a single .mod file."""
        try:
            resp = requests.get(url, timeout=30)
            resp.raise_for_status()

            # Save locally
            filepath = self.output_dir / filename
            filepath.write_text(resp.text)

            return resp.text

        except Exception as e:
            log.warning(f"    Failed to download {filename}: {e}")
            return None

    def convert_to_formula(self, eq, metadata, model_id):
        """Convert parsed equation to formula dict."""
        if eq['type'] == 'ODE':
            var = eq['variable']
            expr = eq['expression']

            return {
                'name': f"{model_id}: d{var}/dt ({metadata.get('title', 'Unknown')})",
                'latex': f"\\frac{{d{var}}}{{dt}} = {expr}",
                'description': f"ODE from ModelDB {model_id} ({metadata.get('title', '')})",
                'formula_type': 'ODE',
                'domain': 'electrophysiology',
                'model_origin': model_id,
                'python_code': f"d{var}_dt = {expr}"
            }

        elif eq['type'] == 'rate_function':
            var = eq['variable']
            expr = eq['expression']

            return {
                'name': f"{model_id}: {var} ({metadata.get('title', 'Unknown')})",
                'latex': f"{var} = {expr}",
                'description': f"Rate function from ModelDB {model_id}",
                'formula_type': 'rate_equation',
                'domain': 'electrophysiology',
                'model_origin': model_id,
                'python_code': f"{var} = {expr}"
            }

        elif eq['type'] == 'kinetic':
            return {
                'name': f"{model_id}: Kinetic scheme ({metadata.get('title', 'Unknown')})",
                'latex': f"{eq['states']} \\leftrightarrow {eq['rates']}",
                'description': f"Markov kinetic scheme from ModelDB {model_id}",
                'formula_type': 'kinetic',
                'domain': 'ion-channels',
                'model_origin': model_id
            }

        return None

    def save_formulas(self, formulas):
        """Save formulas to database."""
        for f in formulas:
            try:
                # Determine category
                cat_id = None
                domain = f.get('domain', '')

                if 'ion' in domain or 'channel' in f.get('name', '').lower():
                    cat_id = get_category_id(self.conn, 'Ion Channels')
                elif 'synap' in f.get('name', '').lower():
                    cat_id = get_category_id(self.conn, 'Synaptic Transmission')
                elif f['formula_type'] == 'ODE':
                    cat_id = get_category_id(self.conn, 'Neuron Models')

                if not cat_id:
                    cat_id = get_category_id(self.conn, 'Neuroscience')

                # Add formula
                add_formula(
                    self.conn,
                    name=f['name'][:200],  # Limit length
                    latex=f['latex'],
                    desc=f['description'],
                    ftype=f['formula_type'],
                    cat_id=cat_id,
                    src_id=self.source_id,
                    python_code=f.get('python_code'),
                    domain=f.get('domain'),
                    model_origin=f.get('model_origin')
                )

            except Exception as e:
                log.warning(f"  Error saving formula: {e}")

    def process_model(self, model_id):
        """Process a single ModelDB model."""
        log.info(f"Processing ModelDB model: {model_id}")

        try:
            # Download .mod files
            mod_files = self.download_model_files(model_id)
            if not mod_files:
                return []

            all_formulas = []

            for mod_file in mod_files:
                log.info(f"  Parsing {mod_file['filename']}")

                # Download content
                content = self.download_mod_file(mod_file['url'], mod_file['filename'])
                if not content:
                    continue

                # Parse
                result = self.parser.parse(content, mod_file['filename'])

                # Convert to formulas
                for eq in result['odes']:
                    formula = self.convert_to_formula(eq, result['metadata'], model_id)
                    if formula:
                        all_formulas.append(formula)

                for eq in result['rates']:
                    formula = self.convert_to_formula(eq, result['metadata'], model_id)
                    if formula:
                        all_formulas.append(formula)

                for eq in result['kinetics']:
                    formula = self.convert_to_formula(eq, result['metadata'], model_id)
                    if formula:
                        all_formulas.append(formula)

                self.stats['mod_files'] += 1

            log.info(f"  Extracted {len(all_formulas)} formulas from {model_id}")
            self.stats['models_processed'] += 1
            self.stats['formulas_extracted'] += len(all_formulas)

            return all_formulas

        except Exception as e:
            log.error(f"  Error processing {model_id}: {e}")
            self.stats['errors'] += 1
            return []

    def harvest(self, query='ion channel', max_models=20, delay=2.0):
        """Main harvest workflow."""
        log.info("="*60)
        log.info("ModelDB Harvester Starting")
        log.info("="*60)

        start_count = count_formulas(self.conn)

        # Search for models
        model_ids = self.search_models(query, max_models)

        # Process each model
        all_formulas = []
        for i, model_id in enumerate(model_ids, 1):
            log.info(f"[{i}/{len(model_ids)}] Model {model_id}")

            formulas = self.process_model(model_id)
            all_formulas.extend(formulas)

            # Save periodically
            if len(all_formulas) >= 50:
                self.save_formulas(all_formulas)
                all_formulas = []

            # Rate limiting
            time.sleep(delay)

        # Save remaining
        if all_formulas:
            self.save_formulas(all_formulas)

        # Summary
        log.info("="*60)
        log.info(f"ModelDB Harvest Complete")
        log.info(f"  Models processed: {self.stats['models_processed']}")
        log.info(f"  .mod files parsed: {self.stats['mod_files']}")
        log.info(f"  Formulas extracted: {self.stats['formulas_extracted']}")
        log.info(f"  Errors: {self.stats['errors']}")
        log.info("="*60)

        print_summary(self.conn, "ModelDB", start_count)


def main():
    """Run ModelDB harvester."""
    conn = get_conn()

    try:
        harvester = ModelDBHarvester(conn)

        # Harvest ion channel models
        harvester.harvest(query='ion channel', max_models=10, delay=2.0)

    finally:
        conn.close()


if __name__ == '__main__':
    main()
