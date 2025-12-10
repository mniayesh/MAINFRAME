#!/usr/bin/env python3
"""
Load extracted biological data into the bio_architecture database.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from bio_architecture_db_utils import BioArchDB


def load_extraction_results():
    """Load all extraction results into the database."""

    # Initialize database
    db = BioArchDB('bio_architecture.db')

    # Load extracted data files
    extraction_files = {
        'KEGG': 'extraction_results/KEGG_extracted.json',
        'AllenBrain': 'extraction_results/AllenBrain_extracted.json',
        'CognitiveAtlas': 'extraction_results/CognitiveAtlas_extracted.json',
    }

    entities_to_insert = []

    for source, filepath in extraction_files.items():
        try:
            with open(filepath) as f:
                data = json.load(f)

            print(f'\nProcessing {len(data)} items from {source}...')

            for item in data:
                # Extract fields with fallbacks
                entity = {
                    'entity_type': item.get('entity_type', 'unknown'),
                    'name': item.get('name', 'Unnamed'),
                    'description': item.get('description', item.get('definition', '')),
                    'source_database': item.get('source_database', source),
                    'identifier': item.get('identifier', item.get('id', '')),
                    'confidence_score': item.get('confidence_score', 0.8),
                    'evidence_strength': item.get('evidence_strength', 'computational')
                }

                entities_to_insert.append(entity)

        except FileNotFoundError:
            print(f'  ⚠ File not found: {filepath}')
        except Exception as e:
            print(f'  ⚠ Error processing {source}: {e}')

    # Bulk insert
    if entities_to_insert:
        print(f'\n📥 Inserting {len(entities_to_insert)} entities into database...')
        try:
            db.bulk_import_entities(entities_to_insert)
            print(f'✓ Successfully inserted {len(entities_to_insert)} entities')
        except Exception as e:
            print(f'✗ Error during bulk insert: {e}')

    # Print statistics
    print('\n' + '='*80)
    print('DATABASE STATISTICS')
    print('='*80)
    db.print_statistics()

    db.close()


if __name__ == '__main__':
    load_extraction_results()
