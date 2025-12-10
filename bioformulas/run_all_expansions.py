#!/usr/bin/env python3
"""
Master runner for all formula expansions.
Executes each module sequentially with logging.
"""

import sys
import logging
from datetime import datetime
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(message)s',
    datefmt='%H:%M:%S'
)
log = logging.getLogger('bioformulas')

def main():
    log.info("=" * 60)
    log.info("BIOFORMULAS MASSIVE EXPANSION")
    log.info("=" * 60)
    log.info(f"Started: {datetime.now().isoformat()}")
    log.info("")

    # Import and run each module
    modules = [
        ("expand_01_ion_channels", "Ion Channels"),
        ("expand_02_metabolism", "Metabolic Pathways"),
        ("expand_03_receptors", "Receptors & Ligand Binding"),
        ("expand_04_signaling", "Cell Signaling Cascades"),
        ("expand_05_neurons", "Neuron Models"),
        ("expand_06_synapses", "Synapses & Plasticity"),
        ("expand_07_cardiac", "Cardiac & Muscle"),
        ("expand_08_networks", "Network Dynamics"),
    ]

    for module_name, desc in modules:
        log.info(f"\n{'#' * 60}")
        log.info(f"# LOADING: {desc}")
        log.info(f"{'#' * 60}\n")

        try:
            module = __import__(module_name)
            module.run()
        except Exception as e:
            log.error(f"ERROR in {module_name}: {e}")
            import traceback
            traceback.print_exc()

    # Final summary
    log.info("\n" + "=" * 60)
    log.info("EXPANSION COMPLETE")
    log.info("=" * 60)

    # Get final counts
    import sqlite3
    conn = sqlite3.connect(Path(__file__).parent / 'bioformulas.db')

    counts = {}
    tables = ['formulas', 'categories', 'sources', 'ion_channels', 'synapses',
              'enzyme_kinetics', 'neuron_models', 'plasticity_rules', 'variables']

    for table in tables:
        try:
            count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            counts[table] = count
        except Exception:
            counts[table] = 0

    log.info("")
    log.info("FINAL DATABASE STATISTICS:")
    log.info("-" * 40)
    log.info(f"  Total formulas:      {counts['formulas']}")
    log.info(f"  Categories:          {counts['categories']}")
    log.info(f"  Sources:             {counts['sources']}")
    log.info(f"  Ion channels:        {counts['ion_channels']}")
    log.info(f"  Synapses:            {counts['synapses']}")
    log.info(f"  Enzyme kinetics:     {counts['enzyme_kinetics']}")
    log.info(f"  Neuron models:       {counts['neuron_models']}")
    log.info(f"  Plasticity rules:    {counts['plasticity_rules']}")
    log.info("-" * 40)

    # Formula type breakdown
    log.info("\nFormulas by type:")
    cursor = conn.execute("""
        SELECT formula_type, COUNT(*) as cnt
        FROM formulas
        GROUP BY formula_type
        ORDER BY cnt DESC
    """)
    for row in cursor.fetchall():
        log.info(f"  {row[0]}: {row[1]}")

    # Domain breakdown
    log.info("\nFormulas by domain:")
    cursor = conn.execute("""
        SELECT domain, COUNT(*) as cnt
        FROM formulas
        WHERE domain IS NOT NULL
        GROUP BY domain
        ORDER BY cnt DESC
        LIMIT 20
    """)
    for row in cursor.fetchall():
        log.info(f"  {row[0]}: {row[1]}")

    conn.close()

    log.info("")
    log.info(f"Finished: {datetime.now().isoformat()}")
    log.info("=" * 60)

if __name__ == "__main__":
    main()
