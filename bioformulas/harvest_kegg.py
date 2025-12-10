#!/usr/bin/env python3
"""
Harvest formulas from KEGG (Kyoto Encyclopedia of Genes and Genomes).
KEGG: https://www.genome.jp/kegg/

Converts pathway reactions into ODEs and rate equations.
"""

import requests
import re
from pathlib import Path
import logging
import time
from expand_base import get_conn, add_formula, get_source_id, get_category_id
from expand_base import add_enzyme, print_summary, count_formulas

log = logging.getLogger('bioformulas.kegg')

KEGG_API = "https://rest.kegg.jp"


class KEGGHarvester:
    """Extract formulas from KEGG pathways and reactions."""

    def __init__(self, conn, output_dir='data/kegg'):
        self.conn = conn
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Add KEGG as a source if not exists
        cursor = conn.execute("SELECT source_id FROM sources WHERE name = 'KEGG Database'")
        row = cursor.fetchone()
        if row:
            self.source_id = row[0]
        else:
            conn.execute("""
                INSERT INTO sources (name, url, description)
                VALUES ('KEGG Database', 'https://www.genome.jp/kegg/',
                        'Kyoto Encyclopedia of Genes and Genomes - metabolic pathways')
            """)
            conn.commit()
            self.source_id = get_source_id(conn, 'KEGG Database')

        self.stats = {'pathways': 0, 'reactions': 0, 'formulas': 0, 'errors': 0}

    def get_pathway_list(self, organism='hsa'):
        """Get list of pathways."""
        log.info(f"Fetching KEGG pathways for {organism}")

        try:
            url = f"{KEGG_API}/list/pathway/{organism}"
            resp = requests.get(url, timeout=30)
            resp.raise_for_status()

            pathways = []
            for line in resp.text.strip().split('\n'):
                if '\t' in line:
                    path_id, name = line.split('\t', 1)
                    pathways.append({'id': path_id, 'name': name})

            log.info(f"Found {len(pathways)} pathways")
            return pathways

        except Exception as e:
            log.error(f"Failed to fetch pathways: {e}")
            return []

    def get_reaction(self, reaction_id):
        """Get reaction details."""
        try:
            url = f"{KEGG_API}/get/{reaction_id}"
            resp = requests.get(url, timeout=30)
            resp.raise_for_status()

            return self.parse_reaction(resp.text, reaction_id)

        except Exception as e:
            log.warning(f"  Failed to get reaction {reaction_id}: {e}")
            return None

    def parse_reaction(self, text, reaction_id):
        """Parse KEGG reaction text."""
        reaction = {'id': reaction_id, 'name': None, 'equation': None,
                    'enzyme': None, 'reactants': [], 'products': []}

        for line in text.split('\n'):
            if line.startswith('NAME'):
                reaction['name'] = line.split(None, 1)[1] if len(line.split(None, 1)) > 1 else None

            elif line.startswith('DEFINITION'):
                # Extract reaction equation
                eq = line.split(None, 1)[1] if len(line.split(None, 1)) > 1 else None
                reaction['equation'] = eq

                # Parse reactants and products
                if eq and '<=>' in eq:
                    left, right = eq.split('<=>', 1)
                    reaction['reactants'] = [c.strip() for c in left.split('+')]
                    reaction['products'] = [c.strip() for c in right.split('+')]

            elif line.startswith('ENZYME'):
                reaction['enzyme'] = line.split(None, 1)[1] if len(line.split(None, 1)) > 1 else None

        return reaction

    def reaction_to_ode(self, reaction):
        """Convert KEGG reaction to ODE."""
        formulas = []

        if not reaction or not reaction.get('equation'):
            return formulas

        rxn_id = reaction['id']
        name = reaction.get('name', rxn_id)

        # Create mass action ODE for each product
        for product in reaction['products']:
            # Clean compound name
            prod_clean = re.sub(r'\d+\s*', '', product).strip()  # Remove stoichiometry
            prod_var = re.sub(r'[^a-zA-Z0-9_]', '_', prod_clean)

            # Simplified mass action rate law
            reactant_terms = []
            for reactant in reaction['reactants']:
                react_clean = re.sub(r'\d+\s*', '', reactant).strip()
                react_var = re.sub(r'[^a-zA-Z0-9_]', '_', react_clean)
                reactant_terms.append(f"[{react_var}]")

            if reactant_terms:
                rate_expr = f"k_{{f}} {' '.join(reactant_terms)}"
            else:
                rate_expr = f"k_{{f}}"

            formulas.append({
                'name': f"KEGG {rxn_id}: Production of {prod_clean}",
                'latex': f"\\frac{{d[{prod_var}]}}{{dt}} = {rate_expr}",
                'description': f"ODE from KEGG reaction {rxn_id}: {name}",
                'formula_type': 'ODE',
                'domain': 'metabolism',
                'model_origin': rxn_id,
                'python_code': f"d{prod_var}_dt = k_f * {' * '.join(reactant_terms)}" if reactant_terms else f"d{prod_var}_dt = k_f"
            })

        # Also create rate equation
        if reaction['reactants']:
            reactant_str = ' + '.join(reaction['reactants'])
            product_str = ' + '.join(reaction['products'])

            formulas.append({
                'name': f"KEGG {rxn_id}: {name}",
                'latex': f"v = k_{{f}} {' '.join([f'[{r}]' for r in reaction['reactants']])}",
                'description': f"Reaction rate from KEGG {rxn_id}",
                'formula_type': 'rate_equation',
                'domain': 'metabolism',
                'model_origin': rxn_id,
                'reaction_equation': f"{reactant_str} <=> {product_str}"
            })

        return formulas

    def get_all_reactions(self, limit=None):
        """Get all reactions from KEGG."""
        try:
            url = f"{KEGG_API}/list/reaction"
            resp = requests.get(url, timeout=30)
            resp.raise_for_status()

            reactions = []
            for line in resp.text.strip().split('\n'):
                if '\t' in line:
                    rxn_id, description = line.split('\t', 1)
                    # Extract equation from description (after semicolon)
                    equation = None
                    if ';' in description:
                        parts = description.split(';', 1)
                        if len(parts) > 1:
                            equation = parts[1].strip()

                    reactions.append({
                        'id': rxn_id,
                        'description': description,
                        'equation': equation
                    })

                    if limit and len(reactions) >= limit:
                        break

            return reactions

        except Exception as e:
            log.error(f"Failed to get reactions: {e}")
            return []

    def save_formulas(self, formulas):
        """Save formulas to database."""
        for f in formulas:
            try:
                cat_id = get_category_id(self.conn, 'Metabolic Pathways')
                if not cat_id:
                    cat_id = get_category_id(self.conn, 'Biochemistry')

                add_formula(
                    self.conn,
                    name=f['name'][:200],
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

    def harvest(self, max_reactions=None, delay=0.3, fetch_details=True):
        """
        Harvest KEGG formulas.

        Args:
            max_reactions: Maximum reactions to process (None = all)
            delay: Delay between API calls
            fetch_details: Whether to fetch full reaction details (slower but more complete)
        """
        log.info("="*60)
        log.info("KEGG Harvester Starting")
        log.info("="*60)

        start_count = count_formulas(self.conn)

        # Get all reactions
        log.info("Fetching reaction list...")
        reactions = self.get_all_reactions(limit=max_reactions)
        log.info(f"Found {len(reactions)} reactions to process")

        all_formulas = []
        processed_reactions = set()

        for i, rxn_info in enumerate(reactions, 1):
            rxn_id = rxn_info['id']

            if rxn_id in processed_reactions:
                continue

            if i % 100 == 0:
                log.info(f"Progress: {i}/{len(reactions)} reactions processed")

            # Option 1: Use equation from list (faster)
            if not fetch_details and rxn_info.get('equation'):
                reaction = {
                    'id': rxn_id,
                    'name': rxn_info['description'].split(';')[0].strip(),
                    'equation': rxn_info['equation'],
                    'enzyme': None,
                    'reactants': [],
                    'products': []
                }

                # Parse equation
                if '<=>' in rxn_info['equation']:
                    left, right = rxn_info['equation'].split('<=>', 1)
                    reaction['reactants'] = [c.strip() for c in left.split('+')]
                    reaction['products'] = [c.strip() for c in right.split('+')]

            # Option 2: Fetch full details (slower but complete)
            else:
                reaction = self.get_reaction(rxn_id)

            if reaction and (reaction.get('equation') or reaction.get('reactants')):
                formulas = self.reaction_to_ode(reaction)
                all_formulas.extend(formulas)
                processed_reactions.add(rxn_id)
                self.stats['reactions'] += 1

            # Save periodically
            if len(all_formulas) >= 100:
                self.save_formulas(all_formulas)
                self.stats['formulas'] += len(all_formulas)
                log.info(f"  Saved {self.stats['formulas']} formulas so far...")
                all_formulas = []

            if fetch_details and i % 10 == 0:
                time.sleep(delay)  # Rate limit for API calls

        # Save remaining
        if all_formulas:
            self.save_formulas(all_formulas)
            self.stats['formulas'] += len(all_formulas)

        log.info("="*60)
        log.info(f"KEGG Harvest Complete")
        log.info(f"  Reactions: {self.stats['reactions']}")
        log.info(f"  Formulas: {self.stats['formulas']}")
        log.info("="*60)

        print_summary(self.conn, "KEGG", start_count)


def main():
    """Run KEGG harvester."""
    conn = get_conn()

    try:
        harvester = KEGGHarvester(conn)

        # Harvest all KEGG reactions (fast mode using list equations)
        # For full details including enzyme info, set fetch_details=True
        harvester.harvest(max_reactions=None, delay=0.3, fetch_details=False)

    finally:
        conn.close()


if __name__ == '__main__':
    main()
