#!/usr/bin/env python3
"""
Biological Database Extraction Orchestrator

Coordinates extraction from all biological databases in dependency order,
with parallel extraction where possible, and generates comprehensive reports.

Usage:
    python extract_all.py --config config/extraction_config.yaml
    python extract_all.py --databases GO,Reactome --output results/
    python extract_all.py --dry-run  # Preview what will be extracted
"""

import argparse
import json
import yaml
import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
import sqlite3

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from bio_extractors import (
    GOExtractor, ReactomeExtractor, KEGGExtractor,
    AllenBrainExtractor, NeuroMorphoExtractor, CellOntologyExtractor,
    UniProtExtractor, InterProExtractor, BRENDAExtractor,
    ChEBIExtractor, EQuilibratorExtractor,
    CognitiveAtlasExtractor, CogPOExtractor, MFOExtractor
)
from bio_architecture_db_utils import BioArchDB


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('extraction.log')
    ]
)
logger = logging.getLogger(__name__)


class ExtractionOrchestrator:
    """
    Orchestrates extraction from multiple biological databases.

    Features:
    - Dependency-aware extraction order
    - Parallel extraction where possible
    - Progress tracking
    - Error recovery
    - Comprehensive reporting
    """

    def __init__(self, config_path: str = None):
        """
        Initialize orchestrator.

        Args:
            config_path: Path to YAML configuration file
        """
        self.config = self._load_config(config_path)
        self.results = {}
        self.errors = {}
        self.stats = {
            'total_items': 0,
            'total_errors': 0,
            'databases_processed': 0,
            'start_time': None,
            'end_time': None
        }

    def _load_config(self, config_path: str = None) -> Dict:
        """Load configuration from YAML file."""
        if config_path and Path(config_path).exists():
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            logger.info(f"Loaded configuration from {config_path}")
            return config
        else:
            # Default configuration
            logger.warning("Using default configuration")
            return self._get_default_config()

    def _get_default_config(self) -> Dict:
        """Get default configuration."""
        return {
            'output': {
                'directory': 'extraction_results',
                'format': 'json',
                'save_to_db': True,
                'db_path': 'bio_architecture.db'
            },
            'extraction': {
                'max_items_per_database': 500,
                'parallel': True,
                'max_workers': 4
            },
            'cache': {
                'enabled': True,
                'directory': '.cache',
                'ttl_minutes': 15
            },
            'databases': {
                'GO': {'enabled': True, 'priority': 1},
                'Reactome': {'enabled': True, 'priority': 1},
                'KEGG': {'enabled': True, 'priority': 1},
                'AllenBrain': {'enabled': True, 'priority': 2},
                'NeuroMorpho': {'enabled': True, 'priority': 2},
                'CellOntology': {'enabled': True, 'priority': 2},
                'UniProt': {'enabled': True, 'priority': 3},
                'InterPro': {'enabled': True, 'priority': 3},
                'BRENDA': {'enabled': False, 'priority': 3},  # Requires auth
                'ChEBI': {'enabled': True, 'priority': 4},
                'eQuilibrator': {'enabled': False, 'priority': 4},  # May require auth
                'CognitiveAtlas': {'enabled': True, 'priority': 5},
                'CogPO': {'enabled': False, 'priority': 5},  # Requires API key
                'MFO': {'enabled': False, 'priority': 5}  # Requires API key
            }
        }

    def extract_all(
        self,
        databases: List[str] = None,
        parallel: bool = True,
        dry_run: bool = False
    ) -> Dict[str, Any]:
        """
        Extract from all enabled databases.

        Args:
            databases: List of specific databases to extract (None = all enabled)
            parallel: Whether to extract in parallel
            dry_run: If True, only preview what will be extracted

        Returns:
            Dictionary of extraction results
        """
        self.stats['start_time'] = datetime.now()

        logger.info("="*80)
        logger.info("BIOLOGICAL DATABASE EXTRACTION STARTING")
        logger.info("="*80)

        # Get list of databases to extract
        databases_to_extract = self._get_extraction_order(databases)

        if dry_run:
            logger.info("\n=== DRY RUN MODE ===")
            logger.info(f"Would extract from {len(databases_to_extract)} databases:")
            for db_name, priority in databases_to_extract:
                logger.info(f"  - {db_name} (Priority {priority})")
            return {}

        # Group by priority for parallel execution
        priority_groups = self._group_by_priority(databases_to_extract)

        # Extract each priority group
        for priority, db_names in sorted(priority_groups.items()):
            logger.info(f"\n{'='*80}")
            logger.info(f"EXTRACTING PRIORITY {priority} DATABASES")
            logger.info(f"{'='*80}")

            if parallel and len(db_names) > 1:
                self._extract_parallel(db_names)
            else:
                self._extract_sequential(db_names)

        self.stats['end_time'] = datetime.now()
        self.stats['duration_seconds'] = (
            self.stats['end_time'] - self.stats['start_time']
        ).total_seconds()

        return self.results

    def _get_extraction_order(self, databases: List[str] = None) -> List[tuple]:
        """
        Get list of databases to extract in priority order.

        Args:
            databases: Optional filter for specific databases

        Returns:
            List of (database_name, priority) tuples
        """
        db_config = self.config['databases']

        extraction_list = []
        for db_name, db_info in db_config.items():
            # Filter by enabled and requested databases
            if not db_info.get('enabled', False):
                continue

            if databases and db_name not in databases:
                continue

            extraction_list.append((db_name, db_info.get('priority', 999)))

        # Sort by priority (lower priority = extracted first)
        extraction_list.sort(key=lambda x: x[1])

        return extraction_list

    def _group_by_priority(self, databases: List[tuple]) -> Dict[int, List[str]]:
        """Group databases by priority level."""
        groups = {}
        for db_name, priority in databases:
            if priority not in groups:
                groups[priority] = []
            groups[priority].append(db_name)

        return groups

    def _extract_parallel(self, db_names: List[str]):
        """Extract from multiple databases in parallel."""
        max_workers = self.config['extraction'].get('max_workers', 4)

        logger.info(f"Extracting from {len(db_names)} databases in parallel "
                   f"(max {max_workers} workers)...")

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit extraction tasks
            futures = {
                executor.submit(self._extract_single, db_name): db_name
                for db_name in db_names
            }

            # Process completed tasks
            for future in as_completed(futures):
                db_name = futures[future]
                try:
                    result = future.result()
                    logger.info(f"{db_name} extraction completed")
                except Exception as e:
                    logger.error(f"{db_name} extraction failed: {str(e)}")
                    self.errors[db_name] = str(e)
                    self.stats['total_errors'] += 1

    def _extract_sequential(self, db_names: List[str]):
        """Extract from databases sequentially."""
        logger.info(f"Extracting from {len(db_names)} databases sequentially...")

        for db_name in db_names:
            try:
                self._extract_single(db_name)
                logger.info(f"{db_name} extraction completed")
            except Exception as e:
                logger.error(f"{db_name} extraction failed: {str(e)}")
                self.errors[db_name] = str(e)
                self.stats['total_errors'] += 1

    def _extract_single(self, db_name: str) -> List[Dict]:
        """
        Extract from a single database.

        Args:
            db_name: Database name

        Returns:
            List of extracted items
        """
        logger.info(f"\n--- Extracting from {db_name} ---")

        # Get extractor
        extractor = self._get_extractor(db_name)
        if not extractor:
            raise ValueError(f"Unknown database: {db_name}")

        # Extract
        max_items = self.config['extraction'].get('max_items_per_database', 500)

        try:
            with extractor:
                results = extractor.extract()

                # Limit results
                results = results[:max_items]

                # Store results
                self.results[db_name] = results
                self.stats['total_items'] += len(results)
                self.stats['databases_processed'] += 1

                # Save to file
                self._save_results(db_name, results)

                # Print stats
                extractor.print_stats()

                return results

        except Exception as e:
            logger.error(f"Error during extraction: {str(e)}")
            raise

    def _get_extractor(self, db_name: str):
        """Get extractor instance for a database."""
        cache_config = self.config.get('cache', {})

        extractors = {
            'GO': lambda: GOExtractor(
                cache_dir=cache_config.get('directory', '.cache'),
                cache_ttl_minutes=cache_config.get('ttl_minutes', 15)
            ),
            'Reactome': lambda: ReactomeExtractor(
                cache_dir=cache_config.get('directory', '.cache')
            ),
            'KEGG': lambda: KEGGExtractor(
                cache_dir=cache_config.get('directory', '.cache')
            ),
            'AllenBrain': lambda: AllenBrainExtractor(
                cache_dir=cache_config.get('directory', '.cache')
            ),
            'NeuroMorpho': lambda: NeuroMorphoExtractor(
                cache_dir=cache_config.get('directory', '.cache')
            ),
            'CellOntology': lambda: CellOntologyExtractor(
                cache_dir=cache_config.get('directory', '.cache')
            ),
            'UniProt': lambda: UniProtExtractor(
                cache_dir=cache_config.get('directory', '.cache')
            ),
            'InterPro': lambda: InterProExtractor(
                cache_dir=cache_config.get('directory', '.cache')
            ),
            'BRENDA': lambda: BRENDAExtractor(
                email=self.config.get('credentials', {}).get('brenda_email'),
                password=self.config.get('credentials', {}).get('brenda_password'),
                cache_dir=cache_config.get('directory', '.cache')
            ),
            'ChEBI': lambda: ChEBIExtractor(
                cache_dir=cache_config.get('directory', '.cache')
            ),
            'eQuilibrator': lambda: EQuilibratorExtractor(
                cache_dir=cache_config.get('directory', '.cache')
            ),
            'CognitiveAtlas': lambda: CognitiveAtlasExtractor(
                cache_dir=cache_config.get('directory', '.cache')
            ),
            'CogPO': lambda: CogPOExtractor(
                api_key=self.config.get('credentials', {}).get('bioportal_api_key'),
                cache_dir=cache_config.get('directory', '.cache')
            ),
            'MFO': lambda: MFOExtractor(
                api_key=self.config.get('credentials', {}).get('bioportal_api_key'),
                cache_dir=cache_config.get('directory', '.cache')
            )
        }

        return extractors.get(db_name, lambda: None)()

    def _save_results(self, db_name: str, results: List[Dict]):
        """Save extraction results to file."""
        output_dir = Path(self.config['output']['directory'])
        output_dir.mkdir(parents=True, exist_ok=True)

        # Save as JSON
        output_file = output_dir / f"{db_name}_extracted.json"

        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)

        logger.info(f"Saved {len(results)} items to {output_file}")

    def save_to_database(self, db_path: str = None):
        """
        Save extracted data to SQLite database.

        Args:
            db_path: Path to database file
        """
        if not db_path:
            db_path = self.config['output'].get('db_path', 'bio_architecture.db')

        logger.info(f"\n{'='*80}")
        logger.info(f"SAVING TO DATABASE: {db_path}")
        logger.info(f"{'='*80}")

        db = BioArchDB(db_path)

        total_inserted = 0

        for db_name, items in self.results.items():
            logger.info(f"\nInserting {len(items)} items from {db_name}...")

            for item in items:
                try:
                    # Determine entity type
                    entity_type = item.get('entity_type', 'process')

                    # Create entity
                    entity_id = db.create_entity(
                        entity_type=entity_type,
                        identifier=item.get('identifier'),
                        name=item.get('name'),
                        description=item.get('description'),
                        mathematical_formulation=item.get('mathematical_formulation'),
                        confidence_score=item.get('confidence_score', 0.8),
                        evidence_strength=item.get('evidence_strength', 'inferred'),
                        source_database=item.get('source_database', db_name),
                        complexity_level=item.get('complexity_level'),
                        common_name=item.get('common_name')
                    )

                    total_inserted += 1

                except Exception as e:
                    logger.error(f"Error inserting item: {str(e)}")

        db.close()

        logger.info(f"\nSuccessfully inserted {total_inserted} entities into database")

    def generate_report(self, output_file: str = None) -> Dict[str, Any]:
        """
        Generate comprehensive extraction report.

        Args:
            output_file: Optional file to save report

        Returns:
            Report dictionary
        """
        report = {
            'extraction_summary': {
                'total_databases': len(self.results),
                'total_items_extracted': self.stats['total_items'],
                'total_errors': self.stats['total_errors'],
                'start_time': self.stats['start_time'].isoformat(),
                'end_time': self.stats['end_time'].isoformat(),
                'duration_seconds': self.stats['duration_seconds']
            },
            'database_breakdown': {},
            'errors': self.errors,
            'entity_type_counts': {}
        }

        # Database breakdown
        for db_name, items in self.results.items():
            report['database_breakdown'][db_name] = {
                'item_count': len(items),
                'entity_types': self._count_entity_types(items)
            }

        # Overall entity type counts
        all_items = []
        for items in self.results.values():
            all_items.extend(items)

        report['entity_type_counts'] = self._count_entity_types(all_items)

        # Save report
        if output_file:
            with open(output_file, 'w') as f:
                json.dump(report, f, indent=2, default=str)
            logger.info(f"\nReport saved to {output_file}")

        return report

    def _count_entity_types(self, items: List[Dict]) -> Dict[str, int]:
        """Count items by entity type."""
        counts = {}
        for item in items:
            entity_type = item.get('entity_type', 'unknown')
            counts[entity_type] = counts.get(entity_type, 0) + 1

        return counts

    def print_report(self):
        """Print formatted extraction report."""
        report = self.generate_report()

        print("\n" + "="*80)
        print("EXTRACTION REPORT")
        print("="*80)

        summary = report['extraction_summary']
        print(f"\nTotal Databases Processed: {summary['total_databases']}")
        print(f"Total Items Extracted:     {summary['total_items_extracted']}")
        print(f"Total Errors:              {summary['total_errors']}")
        print(f"Duration:                  {summary['duration_seconds']:.2f} seconds")

        print("\n" + "-"*80)
        print("DATABASE BREAKDOWN")
        print("-"*80)

        for db_name, info in report['database_breakdown'].items():
            print(f"\n{db_name}:")
            print(f"  Items:        {info['item_count']}")
            print(f"  Entity Types:")
            for entity_type, count in info['entity_types'].items():
                print(f"    - {entity_type}: {count}")

        print("\n" + "-"*80)
        print("OVERALL ENTITY TYPE DISTRIBUTION")
        print("-"*80)

        for entity_type, count in sorted(report['entity_type_counts'].items(), key=lambda x: -x[1]):
            print(f"  {entity_type:20s}: {count:6d}")

        if report['errors']:
            print("\n" + "-"*80)
            print("ERRORS")
            print("-"*80)
            for db_name, error in report['errors'].items():
                print(f"\n{db_name}: {error}")

        print("\n" + "="*80)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Extract biological architectural primitives from multiple databases'
    )

    parser.add_argument(
        '--config',
        type=str,
        default='config/extraction_config.yaml',
        help='Path to configuration file'
    )

    parser.add_argument(
        '--databases',
        type=str,
        help='Comma-separated list of databases to extract (default: all enabled)'
    )

    parser.add_argument(
        '--output',
        type=str,
        help='Output directory for results'
    )

    parser.add_argument(
        '--db-path',
        type=str,
        help='Path to SQLite database for storage'
    )

    parser.add_argument(
        '--parallel',
        action='store_true',
        default=True,
        help='Extract databases in parallel (default: True)'
    )

    parser.add_argument(
        '--no-parallel',
        action='store_true',
        help='Disable parallel extraction'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview extraction plan without executing'
    )

    parser.add_argument(
        '--skip-db-save',
        action='store_true',
        help='Skip saving to database'
    )

    args = parser.parse_args()

    # Initialize orchestrator
    config_path = args.config if Path(args.config).exists() else None
    orchestrator = ExtractionOrchestrator(config_path)

    # Override config with command-line arguments
    if args.output:
        orchestrator.config['output']['directory'] = args.output

    if args.db_path:
        orchestrator.config['output']['db_path'] = args.db_path

    # Parse database list
    databases = None
    if args.databases:
        databases = [db.strip() for db in args.databases.split(',')]

    # Run extraction
    parallel = args.parallel and not args.no_parallel

    try:
        orchestrator.extract_all(
            databases=databases,
            parallel=parallel,
            dry_run=args.dry_run
        )

        if not args.dry_run:
            # Save to database unless skipped
            if not args.skip_db_save and orchestrator.config['output'].get('save_to_db', True):
                orchestrator.save_to_database()

            # Generate and print report
            output_dir = Path(orchestrator.config['output']['directory'])
            report_file = output_dir / 'extraction_report.json'
            orchestrator.generate_report(str(report_file))
            orchestrator.print_report()

            logger.info("\n✓ Extraction completed successfully!")

    except KeyboardInterrupt:
        logger.warning("\n\nExtraction interrupted by user")
        sys.exit(1)

    except Exception as e:
        logger.error(f"\n\nExtraction failed: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
