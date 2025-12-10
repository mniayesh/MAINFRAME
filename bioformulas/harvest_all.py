#!/usr/bin/env python3
"""
MASTER FORMULA HARVESTER
========================

Orchestrates extraction from ALL major biological formula databases:
- BioModels (SBML reaction kinetics, ODEs)
- ModelDB (NEURON ion channels, synapses)
- NeuroML (neural mechanisms)
- KEGG (metabolic pathways)
- Reactome (signaling pathways)
- BRENDA (enzyme kinetics)

This script harvests millions of biological equations from public databases
and stores them in a unified, searchable format.
"""

import logging
import argparse
from datetime import datetime
from pathlib import Path

from expand_base import get_conn, count_formulas

# Import all harvesters
from harvest_biomodels import BioModelsHarvester
from harvest_modeldb import ModelDBHarvester
from harvest_neuroml import NeuroMLHarvester
from harvest_kegg import KEGGHarvester
from harvest_reactome import ReactomeHarvester
from harvest_brenda import BRENDAHarvester

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(name)s: %(message)s',
    datefmt='%H:%M:%S'
)
log = logging.getLogger('harvest_all')


class MasterHarvester:
    """Orchestrate all formula harvesting operations."""

    def __init__(self):
        self.conn = get_conn()
        self.start_time = datetime.now()
        self.initial_count = count_formulas(self.conn)

    def harvest_all(self, config=None):
        """
        Run all harvesters.

        Args:
            config: Dict with harvester-specific settings
        """
        if config is None:
            config = self.get_default_config()

        log.info("="*70)
        log.info("MASTER BIOLOGICAL FORMULA HARVESTER")
        log.info("="*70)
        log.info(f"Started: {self.start_time.isoformat()}")
        log.info(f"Initial formula count: {self.initial_count}")
        log.info("="*70)

        results = {}

        # 1. BRENDA - Enzyme mechanisms (fast, no API calls)
        if config.get('brenda', {}).get('enabled', True):
            log.info("\n" + "🧬 "*20)
            log.info("HARVESTING: BRENDA Enzyme Kinetics")
            log.info("🧬 "*20 + "\n")

            try:
                harvester = BRENDAHarvester(self.conn)
                harvester.harvest()
                results['brenda'] = harvester.stats
            except Exception as e:
                log.error(f"BRENDA harvest failed: {e}")
                results['brenda'] = {'error': str(e)}

        # 2. BioModels - SBML models
        if config.get('biomodels', {}).get('enabled', True):
            log.info("\n" + "🔬 "*20)
            log.info("HARVESTING: BioModels Database (SBML)")
            log.info("🔬 "*20 + "\n")

            try:
                harvester = BioModelsHarvester(self.conn)
                cfg = config.get('biomodels', {})
                harvester.harvest(
                    query=cfg.get('query', 'curated'),
                    max_models=cfg.get('max_models', 20),
                    delay=cfg.get('delay', 1.5)
                )
                results['biomodels'] = harvester.stats
            except Exception as e:
                log.error(f"BioModels harvest failed: {e}")
                results['biomodels'] = {'error': str(e)}

        # 3. ModelDB - Computational neuroscience
        if config.get('modeldb', {}).get('enabled', True):
            log.info("\n" + "⚡ "*20)
            log.info("HARVESTING: ModelDB (NEURON models)")
            log.info("⚡ "*20 + "\n")

            try:
                harvester = ModelDBHarvester(self.conn)
                cfg = config.get('modeldb', {})
                harvester.harvest(
                    query=cfg.get('query', 'ion channel'),
                    max_models=cfg.get('max_models', 10),
                    delay=cfg.get('delay', 2.0)
                )
                results['modeldb'] = harvester.stats
            except Exception as e:
                log.error(f"ModelDB harvest failed: {e}")
                results['modeldb'] = {'error': str(e)}

        # 4. KEGG - Metabolic pathways
        if config.get('kegg', {}).get('enabled', True):
            log.info("\n" + "🧪 "*20)
            log.info("HARVESTING: KEGG Pathways")
            log.info("🧪 "*20 + "\n")

            try:
                harvester = KEGGHarvester(self.conn)
                cfg = config.get('kegg', {})
                harvester.harvest(
                    organism=cfg.get('organism', 'hsa'),
                    max_pathways=cfg.get('max_pathways', 5),
                    delay=cfg.get('delay', 1.5)
                )
                results['kegg'] = harvester.stats
            except Exception as e:
                log.error(f"KEGG harvest failed: {e}")
                results['kegg'] = {'error': str(e)}

        # 5. Reactome - Signaling pathways
        if config.get('reactome', {}).get('enabled', True):
            log.info("\n" + "🔗 "*20)
            log.info("HARVESTING: Reactome Pathways")
            log.info("🔗 "*20 + "\n")

            try:
                harvester = ReactomeHarvester(self.conn)
                cfg = config.get('reactome', {})
                harvester.harvest(
                    species=cfg.get('species', 'Homo sapiens'),
                    max_pathways=cfg.get('max_pathways', 5),
                    delay=cfg.get('delay', 1.5)
                )
                results['reactome'] = harvester.stats
            except Exception as e:
                log.error(f"Reactome harvest failed: {e}")
                results['reactome'] = {'error': str(e)}

        # 6. NeuroML - Neural mechanisms
        if config.get('neuroml', {}).get('enabled', False):
            log.info("\n" + "🧠 "*20)
            log.info("HARVESTING: NeuroML")
            log.info("🧠 "*20 + "\n")

            try:
                harvester = NeuroMLHarvester(self.conn)
                # Would need .nml files provided
                log.info("NeuroML: Provide .nml files to process")
                results['neuroml'] = {'status': 'skipped - needs files'}
            except Exception as e:
                log.error(f"NeuroML harvest failed: {e}")
                results['neuroml'] = {'error': str(e)}

        # Final summary
        self.print_final_summary(results)

    def get_default_config(self):
        """Get default harvester configuration."""
        return {
            'brenda': {'enabled': True},
            'biomodels': {'enabled': True, 'query': 'curated', 'max_models': 20, 'delay': 1.5},
            'modeldb': {'enabled': True, 'query': 'ion channel', 'max_models': 10, 'delay': 2.0},
            'kegg': {'enabled': True, 'organism': 'hsa', 'max_pathways': 5, 'delay': 1.5},
            'reactome': {'enabled': True, 'species': 'Homo sapiens', 'max_pathways': 5, 'delay': 1.5},
            'neuroml': {'enabled': False}
        }

    def print_final_summary(self, results):
        """Print comprehensive harvest summary."""
        end_time = datetime.now()
        final_count = count_formulas(self.conn)
        added = final_count - self.initial_count
        duration = (end_time - self.start_time).total_seconds()

        log.info("\n" + "="*70)
        log.info("HARVEST COMPLETE - FINAL SUMMARY")
        log.info("="*70)
        log.info(f"Started:  {self.start_time.isoformat()}")
        log.info(f"Finished: {end_time.isoformat()}")
        log.info(f"Duration: {duration:.1f} seconds")
        log.info("-"*70)
        log.info(f"Initial formulas: {self.initial_count}")
        log.info(f"Final formulas:   {final_count}")
        log.info(f"NEW FORMULAS:     {added}")
        log.info("="*70)

        log.info("\nResults by source:")
        for source, stats in results.items():
            log.info(f"\n{source.upper()}:")
            if isinstance(stats, dict):
                for key, val in stats.items():
                    log.info(f"  {key}: {val}")

        log.info("\n" + "="*70)
        log.info(f"DATABASE NOW CONTAINS {final_count} BIOLOGICAL FORMULAS")
        log.info("="*70)

        # Save summary to file
        summary_file = Path('harvest_summary.txt')
        with open(summary_file, 'w') as f:
            f.write(f"Harvest Summary\n")
            f.write(f"{'='*70}\n")
            f.write(f"Completed: {end_time.isoformat()}\n")
            f.write(f"Duration: {duration:.1f}s\n")
            f.write(f"Formulas added: {added}\n")
            f.write(f"Total formulas: {final_count}\n\n")

            for source, stats in results.items():
                f.write(f"{source}:\n")
                if isinstance(stats, dict):
                    for key, val in stats.items():
                        f.write(f"  {key}: {val}\n")
                f.write("\n")

        log.info(f"\nSummary saved to: {summary_file}")

    def close(self):
        """Close database connection."""
        self.conn.close()


def main():
    """Run master harvester."""
    parser = argparse.ArgumentParser(description='Harvest biological formulas from all databases')

    parser.add_argument('--sources', nargs='+',
                        choices=['brenda', 'biomodels', 'modeldb', 'kegg', 'reactome', 'neuroml'],
                        help='Specific sources to harvest (default: all except neuroml)')

    parser.add_argument('--max-models', type=int, default=20,
                        help='Max models per source (default: 20)')

    parser.add_argument('--fast', action='store_true',
                        help='Fast mode: fewer models, shorter delays')

    args = parser.parse_args()

    # Build config
    config = {}

    if args.fast:
        # Fast mode: minimal extraction for testing
        config = {
            'brenda': {'enabled': True},
            'biomodels': {'enabled': True, 'max_models': 5, 'delay': 0.5},
            'modeldb': {'enabled': True, 'max_models': 3, 'delay': 1.0},
            'kegg': {'enabled': True, 'max_pathways': 2, 'delay': 0.5},
            'reactome': {'enabled': True, 'max_pathways': 2, 'delay': 0.5},
            'neuroml': {'enabled': False}
        }
    else:
        # Use defaults
        config = None

    # If specific sources requested, disable others
    if args.sources:
        if config is None:
            config = {}
        for source in ['brenda', 'biomodels', 'modeldb', 'kegg', 'reactome', 'neuroml']:
            if source not in config:
                config[source] = {}
            config[source]['enabled'] = source in args.sources

    # Run harvest
    harvester = MasterHarvester()

    try:
        harvester.harvest_all(config)
    finally:
        harvester.close()


if __name__ == '__main__':
    main()
