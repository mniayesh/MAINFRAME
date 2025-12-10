#!/usr/bin/env python3
"""
Harvest formulas from Reactome (biological pathway database).
Reactome: https://reactome.org/

Extracts pathway reactions and regulatory relationships.
"""

import requests
import json
from pathlib import Path
import logging
import time
from expand_base import get_conn, add_formula, get_source_id, get_category_id, print_summary, count_formulas

log = logging.getLogger('bioformulas.reactome')

REACTOME_API = "https://reactome.org/ContentService"


class ReactomeHarvester:
    """Extract formulas from Reactome pathways."""

    def __init__(self, conn, output_dir='data/reactome'):
        self.conn = conn
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Add Reactome as a source if not exists
        cursor = conn.execute("SELECT source_id FROM sources WHERE name = 'Reactome Database'")
        row = cursor.fetchone()
        if row:
            self.source_id = row[0]
        else:
            conn.execute("""
                INSERT INTO sources (name, url, description)
                VALUES ('Reactome Database', 'https://reactome.org/',
                        'Pathway database of biological reactions')
            """)
            conn.commit()
            self.source_id = get_source_id(conn, 'Reactome Database')

        self.stats = {'pathways': 0, 'reactions': 0, 'formulas': 0, 'errors': 0}

    def get_top_pathways(self, species='Homo sapiens', max_results=20):
        """Get top-level pathways."""
        log.info(f"Fetching Reactome pathways for {species}")

        try:
            url = f"{REACTOME_API}/data/pathways/top/{species}"
            resp = requests.get(url, timeout=30)
            resp.raise_for_status()

            pathways = resp.json()
            log.info(f"Found {len(pathways)} top pathways")
            return pathways[:max_results]

        except Exception as e:
            log.error(f"Failed to fetch pathways: {e}")
            return []

    def get_pathway_reactions(self, pathway_id):
        """Get reactions in a pathway."""
        try:
            url = f"{REACTOME_API}/data/pathway/{pathway_id}/containedEvents"
            resp = requests.get(url, timeout=30)
            resp.raise_for_status()

            events = resp.json()
            reactions = [e for e in events if e.get('schemaClass') == 'Reaction']
            return reactions

        except Exception as e:
            log.warning(f"  Failed to get reactions for {pathway_id}: {e}")
            return []

    def reaction_to_formula(self, reaction):
        """Convert Reactome reaction to formula."""
        formulas = []

        try:
            rxn_id = reaction.get('stId', 'unknown')
            name = reaction.get('displayName', rxn_id)

            # Get inputs and outputs
            inputs = reaction.get('input', [])
            outputs = reaction.get('output', [])

            if not inputs or not outputs:
                return formulas

            # Create mass action rate equation
            input_names = [inp.get('displayName', 'unknown') for inp in inputs]
            output_names = [out.get('displayName', 'unknown') for out in outputs]

            input_vars = ' '.join([f"[{n}]" for n in input_names])
            output_vars = ' + '.join(output_names)

            # Rate equation
            formulas.append({
                'name': f"Reactome {rxn_id}: {name}",
                'latex': f"v = k {input_vars}",
                'description': f"Reaction rate from Reactome: {name}",
                'formula_type': 'rate_equation',
                'domain': 'cell-signaling',
                'model_origin': rxn_id
            })

            # ODE for first output
            if output_names:
                out_var = output_names[0].replace(' ', '_').replace('-', '_')
                formulas.append({
                    'name': f"Reactome {rxn_id}: d{out_var}/dt",
                    'latex': f"\\frac{{d[{out_var}]}}{{dt}} = k {input_vars}",
                    'description': f"Production of {output_names[0]} from Reactome {rxn_id}",
                    'formula_type': 'ODE',
                    'domain': 'cell-signaling',
                    'model_origin': rxn_id
                })

        except Exception as e:
            log.warning(f"  Error converting reaction: {e}")

        return formulas

    def save_formulas(self, formulas):
        """Save formulas to database."""
        for f in formulas:
            try:
                cat_id = get_category_id(self.conn, 'Cell Signaling')
                if not cat_id:
                    cat_id = get_category_id(self.conn, 'Systems Biology')

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

    def harvest(self, species='Homo sapiens', max_pathways=10, delay=1.0):
        """
        Harvest Reactome formulas.

        Args:
            species: Species name
            max_pathways: Maximum pathways to process
            delay: Delay between API calls
        """
        log.info("="*60)
        log.info("Reactome Harvester Starting")
        log.info("="*60)

        start_count = count_formulas(self.conn)

        # Get pathways
        pathways = self.get_top_pathways(species, max_pathways)

        all_formulas = []

        for i, pathway in enumerate(pathways, 1):
            path_id = pathway.get('stId', 'unknown')
            path_name = pathway.get('displayName', path_id)

            log.info(f"[{i}/{len(pathways)}] {path_id}: {path_name}")

            # Get reactions
            reactions = self.get_pathway_reactions(path_id)
            log.info(f"  Found {len(reactions)} reactions")

            for reaction in reactions:
                formulas = self.reaction_to_formula(reaction)
                all_formulas.extend(formulas)
                self.stats['reactions'] += 1

            self.stats['pathways'] += 1

            # Save periodically
            if len(all_formulas) >= 50:
                self.save_formulas(all_formulas)
                self.stats['formulas'] += len(all_formulas)
                all_formulas = []

            time.sleep(delay)

        # Save remaining
        if all_formulas:
            self.save_formulas(all_formulas)
            self.stats['formulas'] += len(all_formulas)

        log.info("="*60)
        log.info(f"Reactome Harvest Complete")
        log.info(f"  Pathways: {self.stats['pathways']}")
        log.info(f"  Reactions: {self.stats['reactions']}")
        log.info(f"  Formulas: {self.stats['formulas']}")
        log.info("="*60)

        print_summary(self.conn, "Reactome", start_count)


def main():
    """Run Reactome harvester."""
    conn = get_conn()

    try:
        harvester = ReactomeHarvester(conn)
        harvester.harvest(species='Homo sapiens', max_pathways=5, delay=1.5)

    finally:
        conn.close()


if __name__ == '__main__':
    main()
