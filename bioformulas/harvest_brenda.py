#!/usr/bin/env python3
"""
Harvest formulas from BRENDA (enzyme kinetics database).
BRENDA: https://www.brenda-enzymes.org/

Note: BRENDA requires authentication. This harvester extracts from public data.
"""

import requests
from pathlib import Path
import logging
import re
from expand_base import get_conn, add_formula, get_source_id, get_category_id
from expand_base import add_enzyme, print_summary, count_formulas

log = logging.getLogger('bioformulas.brenda')

# Common enzyme mechanisms and their formulas
ENZYME_MECHANISMS = {
    'michaelis_menten': {
        'name': 'Michaelis-Menten',
        'latex': r'v = \frac{V_{max} [S]}{K_m + [S]}',
        'description': 'Standard Michaelis-Menten enzyme kinetics',
        'type': 'rate_equation'
    },
    'competitive_inhibition': {
        'name': 'Competitive Inhibition',
        'latex': r'v = \frac{V_{max} [S]}{K_m(1 + [I]/K_i) + [S]}',
        'description': 'Enzyme kinetics with competitive inhibitor',
        'type': 'rate_equation'
    },
    'non_competitive_inhibition': {
        'name': 'Non-Competitive Inhibition',
        'latex': r'v = \frac{V_{max} [S]}{(K_m + [S])(1 + [I]/K_i)}',
        'description': 'Enzyme kinetics with non-competitive inhibitor',
        'type': 'rate_equation'
    },
    'uncompetitive_inhibition': {
        'name': 'Uncompetitive Inhibition',
        'latex': r'v = \frac{V_{max} [S]}{K_m + [S](1 + [I]/K_i)}',
        'description': 'Enzyme kinetics with uncompetitive inhibitor',
        'type': 'rate_equation'
    },
    'substrate_inhibition': {
        'name': 'Substrate Inhibition',
        'latex': r'v = \frac{V_{max} [S]}{K_m + [S] + [S]^2/K_{si}}',
        'description': 'Enzyme inhibited by excess substrate',
        'type': 'rate_equation'
    },
    'hill_equation': {
        'name': 'Hill Equation',
        'latex': r'v = \frac{V_{max} [S]^n}{K_{0.5}^n + [S]^n}',
        'description': 'Cooperative enzyme kinetics (Hill equation)',
        'type': 'rate_equation'
    },
    'bi_bi_ordered': {
        'name': 'Bi-Bi Ordered Sequential',
        'latex': r'v = \frac{V_{max} [A][B]}{K_{iA}K_B + K_B[A] + K_A[B] + [A][B]}',
        'description': 'Two-substrate ordered mechanism',
        'type': 'rate_equation'
    },
    'bi_bi_random': {
        'name': 'Bi-Bi Random Sequential',
        'latex': r'v = \frac{V_{max} [A][B]}{K_{iA}K_B + K_A[B] + K_B[A] + [A][B]}',
        'description': 'Two-substrate random binding',
        'type': 'rate_equation'
    },
    'ping_pong': {
        'name': 'Ping-Pong Bi-Bi',
        'latex': r'v = \frac{V_{max} [A][B]}{K_A[B] + K_B[A] + [A][B]}',
        'description': 'Ping-pong mechanism',
        'type': 'rate_equation'
    },
    'allosteric_activation': {
        'name': 'Allosteric Activation',
        'latex': r'v = \frac{V_{max} [S]}{K_m + [S]} \cdot \frac{1 + ([A]/K_a)^n}{1 + ([A]/K_a)^n + (K_m/[S])}',
        'description': 'Enzyme with allosteric activator',
        'type': 'rate_equation'
    },
    'product_inhibition': {
        'name': 'Product Inhibition',
        'latex': r'v = \frac{V_{max} [S]}{K_m(1 + [P]/K_p) + [S]}',
        'description': 'Inhibition by reaction product',
        'type': 'rate_equation'
    },
    'partial_competitive': {
        'name': 'Partial Competitive Inhibition',
        'latex': r'v = \frac{V_{max} [S]}{K_m(1 + [I]/K_i) + [S](1 + [I]/(\alpha K_i))}',
        'description': 'Mixed competitive/non-competitive inhibition',
        'type': 'rate_equation'
    }
}


class BRENDAHarvester:
    """Extract enzyme kinetic formulas."""

    def __init__(self, conn, output_dir='data/brenda'):
        self.conn = conn
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Add BRENDA as source
        cursor = conn.execute("SELECT source_id FROM sources WHERE name = 'BRENDA Database'")
        row = cursor.fetchone()
        if row:
            self.source_id = row[0]
        else:
            conn.execute("""
                INSERT INTO sources (name, url, description)
                VALUES ('BRENDA Database', 'https://www.brenda-enzymes.org/',
                        'Comprehensive enzyme information system')
            """)
            conn.commit()
            self.source_id = get_source_id(conn, 'BRENDA Database')

        self.stats = {'mechanisms_added': 0, 'formulas': 0}

    def add_enzyme_mechanisms(self):
        """Add all standard enzyme kinetic mechanisms to database."""
        log.info("Adding enzyme kinetic mechanisms from BRENDA knowledge base")

        cat_id = get_category_id(self.conn, 'Enzyme Kinetics')
        if not cat_id:
            cat_id = get_category_id(self.conn, 'Biochemistry')

        for mech_id, mech in ENZYME_MECHANISMS.items():
            try:
                add_formula(
                    self.conn,
                    name=f"BRENDA: {mech['name']}",
                    latex=mech['latex'],
                    desc=mech['description'],
                    ftype=mech['type'],
                    cat_id=cat_id,
                    src_id=self.source_id,
                    domain='enzyme-kinetics',
                    model_origin='brenda-mechanisms'
                )

                self.stats['mechanisms_added'] += 1
                self.stats['formulas'] += 1

            except Exception as e:
                log.warning(f"  Error adding {mech['name']}: {e}")

    def harvest(self):
        """Harvest BRENDA formulas."""
        log.info("="*60)
        log.info("BRENDA Harvester Starting")
        log.info("="*60)

        start_count = count_formulas(self.conn)

        # Add standard mechanisms
        self.add_enzyme_mechanisms()

        log.info("="*60)
        log.info(f"BRENDA Harvest Complete")
        log.info(f"  Enzyme mechanisms: {self.stats['mechanisms_added']}")
        log.info(f"  Formulas: {self.stats['formulas']}")
        log.info("="*60)

        print_summary(self.conn, "BRENDA", start_count)


def main():
    """Run BRENDA harvester."""
    conn = get_conn()

    try:
        harvester = BRENDAHarvester(conn)
        harvester.harvest()

    finally:
        conn.close()


if __name__ == '__main__':
    main()
