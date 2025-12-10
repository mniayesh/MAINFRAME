"""
Extract and organize metabolic efficiency formulas from the bioformulas database.

This script extracts key formulas related to:
- ATP production/consumption
- Enzyme kinetics
- Metabolic pathways
- Resource allocation

Database: /home/user/MAINFRAME/bioformulas/bioformulas.db
"""

import sqlite3
import json
from typing import List, Dict, Tuple
from pathlib import Path


class MetabolicFormulaExtractor:
    """Extract metabolic efficiency formulas from bioformulas database."""

    def __init__(self, db_path: str = "/home/user/MAINFRAME/bioformulas/bioformulas.db"):
        self.db_path = db_path
        self.conn = None

    def connect(self):
        """Connect to database."""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row

    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()

    def extract_atp_formulas(self) -> List[Dict]:
        """Extract ATP production and consumption formulas."""
        cursor = self.conn.cursor()

        query = """
        SELECT formula_id, name, description, latex, symbolic, python_code,
               domain, model_origin
        FROM formulas
        WHERE (name LIKE '%ATP%' OR description LIKE '%ATP%')
          AND (description LIKE '%production%' OR description LIKE '%consumption%'
               OR description LIKE '%synthesis%' OR description LIKE '%hydrolysis%')
        LIMIT 30;
        """

        cursor.execute(query)
        results = []

        for row in cursor.fetchall():
            results.append({
                'id': row['formula_id'],
                'name': row['name'],
                'description': row['description'],
                'latex': row['latex'],
                'symbolic': row['symbolic'],
                'python': row['python_code'],
                'domain': row['domain'],
                'origin': row['model_origin']
            })

        return results

    def extract_enzyme_kinetics(self) -> List[Dict]:
        """Extract enzyme kinetics formulas."""
        cursor = self.conn.cursor()

        query = """
        SELECT formula_id, name, description, latex, symbolic, python_code, domain
        FROM formulas
        WHERE category_id = 11
        ORDER BY formula_id
        LIMIT 50;
        """

        cursor.execute(query)
        results = []

        for row in cursor.fetchall():
            results.append({
                'id': row['formula_id'],
                'name': row['name'],
                'description': row['description'],
                'latex': row['latex'],
                'symbolic': row['symbolic'],
                'python': row['python_code'],
                'domain': row['domain']
            })

        return results

    def extract_glycolysis_formulas(self) -> List[Dict]:
        """Extract glycolysis pathway formulas."""
        cursor = self.conn.cursor()

        query = """
        SELECT formula_id, name, description, latex, symbolic, python_code, domain
        FROM formulas
        WHERE category_id = 16
        ORDER BY formula_id;
        """

        cursor.execute(query)
        results = []

        for row in cursor.fetchall():
            results.append({
                'id': row['formula_id'],
                'name': row['name'],
                'description': row['description'],
                'latex': row['latex'],
                'symbolic': row['symbolic'],
                'python': row['python_code'],
                'domain': row['domain']
            })

        return results

    def extract_oxidative_phosphorylation(self) -> List[Dict]:
        """Extract oxidative phosphorylation formulas."""
        cursor = self.conn.cursor()

        query = """
        SELECT formula_id, name, description, latex, symbolic, python_code, domain
        FROM formulas
        WHERE category_id = 18
        ORDER BY formula_id;
        """

        cursor.execute(query)
        results = []

        for row in cursor.fetchall():
            results.append({
                'id': row['formula_id'],
                'name': row['name'],
                'description': row['description'],
                'latex': row['latex'],
                'symbolic': row['symbolic'],
                'python': row['python_code'],
                'domain': row['domain']
            })

        return results

    def extract_enzyme_data(self) -> List[Dict]:
        """Extract enzyme kinetics data from enzyme_kinetics table."""
        cursor = self.conn.cursor()

        query = """
        SELECT kinetics_id, enzyme_name, kinetics_type, km, vmax, kcat,
               hill_coefficient, substrate, product
        FROM enzyme_kinetics
        ORDER BY kinetics_id;
        """

        cursor.execute(query)
        results = []

        for row in cursor.fetchall():
            enzyme_data = {
                'id': row['kinetics_id'],
                'enzyme': row['enzyme_name'],
                'type': row['kinetics_type'],
                'km': row['km'],
                'vmax': row['vmax'],
                'kcat': row['kcat'],
                'hill_coefficient': row['hill_coefficient'],
                'substrate': row['substrate'],
                'product': row['product']
            }

            # Calculate catalytic efficiency if data available
            if row['kcat'] and row['km']:
                enzyme_data['catalytic_efficiency'] = row['kcat'] / row['km']

            results.append(enzyme_data)

        return results

    def extract_resource_allocation(self) -> List[Dict]:
        """Extract resource allocation and constraint formulas."""
        cursor = self.conn.cursor()

        query = """
        SELECT formula_id, name, description, latex, symbolic, python_code, domain
        FROM formulas
        WHERE (description LIKE '%allocation%' OR description LIKE '%constraint%'
               OR description LIKE '%capacity%' OR description LIKE '%saturation%'
               OR description LIKE '%resource%')
          AND (domain LIKE '%biochem%' OR domain LIKE '%metabolism%')
        LIMIT 30;
        """

        cursor.execute(query)
        results = []

        for row in cursor.fetchall():
            results.append({
                'id': row['formula_id'],
                'name': row['name'],
                'description': row['description'],
                'latex': row['latex'],
                'symbolic': row['symbolic'],
                'python': row['python_code'],
                'domain': row['domain']
            })

        return results

    def export_to_json(self, output_dir: str = "/home/user/MAINFRAME/bioformulas"):
        """Export all extracted formulas to JSON files."""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        # Extract all categories
        extractions = {
            'atp_formulas': self.extract_atp_formulas(),
            'enzyme_kinetics': self.extract_enzyme_kinetics(),
            'glycolysis': self.extract_glycolysis_formulas(),
            'oxidative_phosphorylation': self.extract_oxidative_phosphorylation(),
            'enzyme_data': self.extract_enzyme_data(),
            'resource_allocation': self.extract_resource_allocation()
        }

        # Save each category
        for category, data in extractions.items():
            output_file = output_path / f"{category}.json"
            with open(output_file, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"Exported {len(data)} entries to {output_file}")

        # Create summary
        summary = {
            'database': self.db_path,
            'extraction_date': '2025-12-10',
            'categories': {
                category: len(data)
                for category, data in extractions.items()
            }
        }

        summary_file = output_path / "extraction_summary.json"
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        print(f"\nSummary saved to {summary_file}")

        return extractions

    def print_key_formulas(self):
        """Print key formulas for quick reference."""
        print("="*80)
        print("KEY METABOLIC EFFICIENCY FORMULAS")
        print("="*80)

        # 1. Michaelis-Menten
        print("\n1. MICHAELIS-MENTEN KINETICS (Formula ID: 35)")
        print("-" * 80)
        print("Formula: v = (V_max * [S]) / (K_m + [S])")
        print("Description: Classic enzyme saturation kinetics")
        print("Application: Capacity saturation in neural networks")

        # 2. Competitive Inhibition
        print("\n2. COMPETITIVE INHIBITION (Formula ID: 38)")
        print("-" * 80)
        print("Formula: v = (V_max * [S]) / (K_m * (1 + [I]/K_i) + [S])")
        print("Description: Multiple substrates compete for enzyme active site")
        print("Application: Attention mechanism, resource competition")

        # 3. Hill Equation
        print("\n3. HILL EQUATION - COOPERATIVITY (Formula ID: 41)")
        print("-" * 80)
        print("Formula: v = (V_max * [S]^n) / (K_0.5^n + [S]^n)")
        print("Description: Cooperative binding, n>1 creates sharp threshold")
        print("Application: Gating mechanisms, sharp decision boundaries")

        # 4. Substrate Inhibition
        print("\n4. SUBSTRATE INHIBITION (Formula ID: 42)")
        print("-" * 80)
        print("Formula: v = (V_max * [S]) / (K_m + [S] + [S]^2/K_si)")
        print("Description: Excess substrate inhibits enzyme")
        print("Application: Prevent overconfident predictions, regularization")

        # 5. PFK1 Allosteric Regulation
        print("\n5. PFK1 ALLOSTERIC REGULATION (Formula ID: 202)")
        print("-" * 80)
        print("Formula: v = V_max * f(F6P, ATP, AMP)")
        print("  - ATP inhibition (high energy state)")
        print("  - AMP activation (low energy state)")
        print("  - F6P cooperativity (substrate availability)")
        print("Application: Multi-signal integration, adaptive learning rates")

        # 6. ATP Synthase
        print("\n6. ATP SYNTHASE (Formula ID: 217)")
        print("-" * 80)
        print("Formula: v = k_f*[ADP][Pi]*exp(n*F*ΔΨ/RT) - k_r*[ATP]")
        print("Description: Chemiosmotic coupling, proton gradient drives ATP synthesis")
        print("Application: Gradient-driven optimization, energy-efficient computation")

        print("\n" + "="*80)


def main():
    """Main extraction and export function."""
    print("METABOLIC FORMULA EXTRACTION")
    print("="*80)

    extractor = MetabolicFormulaExtractor()

    try:
        extractor.connect()
        print("Connected to database: /home/user/MAINFRAME/bioformulas/bioformulas.db\n")

        # Print key formulas
        extractor.print_key_formulas()

        # Export to JSON
        print("\nEXPORTING TO JSON FILES")
        print("="*80)
        extractions = extractor.export_to_json()

        # Print statistics
        print("\nEXTRACTION STATISTICS")
        print("="*80)
        for category, data in extractions.items():
            print(f"{category:30s}: {len(data):4d} entries")

        print("\n" + "="*80)
        print("Extraction complete!")
        print("="*80)

    finally:
        extractor.close()


if __name__ == '__main__':
    main()
