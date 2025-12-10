#!/usr/bin/env python3
"""
Extract biological learning rules from bioformulas database.

This script extracts the actual mathematical formulas that biology uses for learning,
including STDP, BCM, calcium-dependent plasticity, and Hebbian variants.
"""

import sqlite3
import json
from dataclasses import dataclass, asdict
from typing import List, Optional, Dict
from pathlib import Path


@dataclass
class LearningRule:
    """Biological learning rule with all metadata."""
    formula_id: int
    name: str
    rule_type: str
    description: str
    latex: Optional[str]
    symbolic: Optional[str]
    python_code: Optional[str]
    formula_type: str
    domain: str

    # Plasticity parameters
    time_window_pre: Optional[float]
    time_window_post: Optional[float]
    learning_rate: Optional[float]
    weight_dependence: Optional[str]
    calcium_dependent: bool

    # Additional parameters
    parameters: List[Dict] = None

    def __post_init__(self):
        if self.parameters is None:
            self.parameters = []

    def to_dict(self):
        """Convert to dictionary for JSON serialization."""
        return asdict(self)

    def __str__(self):
        """Readable string representation."""
        s = f"\n{'='*80}\n"
        s += f"LEARNING RULE: {self.name}\n"
        s += f"Type: {self.rule_type}\n"
        s += f"Domain: {self.domain}\n"
        s += f"{'='*80}\n\n"

        s += f"Description:\n{self.description}\n\n"

        if self.latex:
            s += f"LaTeX Formula:\n{self.latex}\n\n"

        if self.symbolic:
            s += f"Symbolic Form:\n{self.symbolic}\n\n"

        if self.python_code:
            s += f"Python Implementation:\n{self.python_code}\n\n"

        s += f"Parameters:\n"
        s += f"  - Learning rate: {self.learning_rate}\n"
        s += f"  - Time window (pre): {self.time_window_pre} ms\n"
        s += f"  - Time window (post): {self.time_window_post} ms\n"
        s += f"  - Weight dependence: {self.weight_dependence}\n"
        s += f"  - Calcium dependent: {self.calcium_dependent}\n"

        if self.parameters:
            s += f"\nFormula Parameters:\n"
            for p in self.parameters:
                s += f"  - {p['symbol']}: {p['name']}\n"
                if p['value']:
                    s += f"    = {p['value']} {p['unit'] or ''}\n"

        return s


class LearningRuleExtractor:
    """Extract learning rules from bioformulas database."""

    def __init__(self, db_path: str):
        self.db_path = Path(db_path)
        if not self.db_path.exists():
            raise FileNotFoundError(f"Database not found: {db_path}")

        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

    def get_all_plasticity_rules(self) -> List[LearningRule]:
        """Extract all plasticity rules from database."""
        cursor = self.conn.cursor()

        query = """
        SELECT
            f.formula_id,
            f.name,
            f.description,
            f.latex,
            f.symbolic,
            f.python_code,
            f.formula_type,
            f.domain,
            pr.rule_type,
            pr.time_window_pre,
            pr.time_window_post,
            pr.learning_rate,
            pr.weight_dependence,
            pr.calcium_dependent
        FROM formulas f
        INNER JOIN plasticity_rules pr ON f.formula_id = pr.formula_id
        ORDER BY pr.rule_type
        """

        cursor.execute(query)
        results = cursor.fetchall()

        learning_rules = []
        for row in results:
            # Get parameters for this formula
            cursor.execute("""
                SELECT symbol, name, value, unit, notes
                FROM parameters
                WHERE formula_id = ?
            """, (row['formula_id'],))
            params = cursor.fetchall()

            param_list = [dict(p) for p in params]

            rule = LearningRule(
                formula_id=row['formula_id'],
                name=row['name'],
                rule_type=row['rule_type'],
                description=row['description'],
                latex=row['latex'],
                symbolic=row['symbolic'],
                python_code=row['python_code'],
                formula_type=row['formula_type'],
                domain=row['domain'],
                time_window_pre=row['time_window_pre'],
                time_window_post=row['time_window_post'],
                learning_rate=row['learning_rate'],
                weight_dependence=row['weight_dependence'],
                calcium_dependent=bool(row['calcium_dependent']),
                parameters=param_list
            )
            learning_rules.append(rule)

        return learning_rules

    def get_stdp_rules(self) -> List[LearningRule]:
        """Get only STDP-related rules."""
        all_rules = self.get_all_plasticity_rules()
        return [r for r in all_rules if 'STDP' in r.rule_type]

    def get_calcium_rules(self) -> List[LearningRule]:
        """Get calcium-dependent learning rules."""
        all_rules = self.get_all_plasticity_rules()
        return [r for r in all_rules if r.calcium_dependent or 'calcium' in r.rule_type.lower()]

    def get_hebbian_rules(self) -> List[LearningRule]:
        """Get Hebbian learning variants."""
        all_rules = self.get_all_plasticity_rules()
        return [r for r in all_rules if 'Oja' in r.rule_type or 'BCM' in r.rule_type]

    def search_formulas(self, search_term: str, domain: str = None) -> List[Dict]:
        """Search for formulas by keyword."""
        cursor = self.conn.cursor()

        if domain:
            query = """
            SELECT name, description, latex, symbolic, domain
            FROM formulas
            WHERE (name LIKE ? OR description LIKE ?)
            AND domain = ?
            LIMIT 20
            """
            cursor.execute(query, (f'%{search_term}%', f'%{search_term}%', domain))
        else:
            query = """
            SELECT name, description, latex, symbolic, domain
            FROM formulas
            WHERE name LIKE ? OR description LIKE ?
            LIMIT 20
            """
            cursor.execute(query, (f'%{search_term}%', f'%{search_term}%'))

        return [dict(row) for row in cursor.fetchall()]

    def export_to_json(self, output_file: str):
        """Export all learning rules to JSON."""
        rules = self.get_all_plasticity_rules()
        rules_dict = [r.to_dict() for r in rules]

        with open(output_file, 'w') as f:
            json.dump(rules_dict, f, indent=2)

        print(f"Exported {len(rules)} learning rules to {output_file}")

    def get_statistics(self) -> Dict:
        """Get database statistics."""
        cursor = self.conn.cursor()

        stats = {}

        cursor.execute("SELECT COUNT(*) FROM formulas")
        stats['total_formulas'] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM plasticity_rules")
        stats['plasticity_rules'] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM synapses")
        stats['synapse_models'] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM neuron_models")
        stats['neuron_models'] = cursor.fetchone()[0]

        cursor.execute("SELECT DISTINCT domain FROM formulas")
        stats['domains'] = [row[0] for row in cursor.fetchall()]

        cursor.execute("SELECT DISTINCT rule_type FROM plasticity_rules WHERE rule_type IS NOT NULL")
        stats['rule_types'] = [row[0] for row in cursor.fetchall()]

        return stats


def main():
    """Main function demonstrating usage."""
    db_path = "/home/user/MAINFRAME/bioformulas/bioformulas.db"

    print("="*80)
    print("BIOLOGICAL LEARNING RULES EXTRACTOR")
    print("="*80)
    print()

    with LearningRuleExtractor(db_path) as extractor:
        # Get statistics
        stats = extractor.get_statistics()
        print("Database Statistics:")
        print(f"  Total formulas: {stats['total_formulas']:,}")
        print(f"  Plasticity rules: {stats['plasticity_rules']}")
        print(f"  Synapse models: {stats['synapse_models']}")
        print(f"  Neuron models: {stats['neuron_models']}")
        print(f"  Rule types: {', '.join(stats['rule_types'])}")
        print()

        # Extract all learning rules
        print("Extracting all learning rules...")
        all_rules = extractor.get_all_plasticity_rules()
        print(f"Found {len(all_rules)} learning rules\n")

        # Print each rule
        for rule in all_rules:
            print(rule)

        # Export to JSON
        output_file = "/home/user/MAINFRAME/bioformulas/learning_rules.json"
        extractor.export_to_json(output_file)

        # Get specific categories
        print("\n" + "="*80)
        print("CATEGORIZED LEARNING RULES")
        print("="*80)

        stdp_rules = extractor.get_stdp_rules()
        print(f"\nSTDP Rules: {len(stdp_rules)}")
        for rule in stdp_rules:
            print(f"  - {rule.name} ({rule.rule_type})")

        calcium_rules = extractor.get_calcium_rules()
        print(f"\nCalcium-dependent Rules: {len(calcium_rules)}")
        for rule in calcium_rules:
            print(f"  - {rule.name}")

        hebbian_rules = extractor.get_hebbian_rules()
        print(f"\nHebbian Variants: {len(hebbian_rules)}")
        for rule in hebbian_rules:
            print(f"  - {rule.name} ({rule.rule_type})")

        # Search for related formulas
        print("\n" + "="*80)
        print("RELATED FORMULAS")
        print("="*80)

        ltp_formulas = extractor.search_formulas("LTP")
        print(f"\nLTP-related formulas: {len(ltp_formulas)}")

        nmda_formulas = extractor.search_formulas("NMDA", domain="synaptic-transmission")
        print(f"NMDA receptor formulas: {len(nmda_formulas)}")
        for formula in nmda_formulas[:5]:
            print(f"  - {formula['name']}")


if __name__ == "__main__":
    main()
