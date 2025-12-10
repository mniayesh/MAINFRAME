#!/usr/bin/env python3
"""
Complete BioModels Harvester - Systematically harvest ALL curated models.

Instead of searching (which returns limited results), this script:
1. Generates sequential model IDs: BIOMD0000000001 -> BIOMD0000001000
2. Downloads in parallel (skips 400 errors gracefully)
3. Extracts all formulas from successful downloads
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from harvest_biomodels_parallel import ParallelBioModelsHarvester, get_conn
import logging

log = logging.getLogger('bioformulas.complete')


def generate_biomd_ids(start=1, end=1000):
    """Generate sequential BioModels IDs."""
    for i in range(start, end + 1):
        yield f"BIOMD{i:010d}"


def main():
    """Harvest all curated BioModels systematically."""
    import argparse

    parser = argparse.ArgumentParser(description='Complete BioModels systematic harvest')
    parser.add_argument('--start', type=int, default=1,
                        help='Starting model number (default: 1)')
    parser.add_argument('--end', type=int, default=1000,
                        help='Ending model number (default: 1000)')
    parser.add_argument('--batch-size', type=int, default=100,
                        help='Models per batch (default: 100)')
    parser.add_argument('--download-workers', type=int, default=20,
                        help='Concurrent downloads')
    parser.add_argument('--parse-workers', type=int, default=8,
                        help='Concurrent parsers')

    args = parser.parse_args()

    conn = get_conn()

    try:
        harvester = ParallelBioModelsHarvester(conn, max_workers=args.download_workers)

        # Generate all model IDs in range
        all_model_ids = list(generate_biomd_ids(args.start, args.end))

        log.info("="*60)
        log.info(f"COMPLETE BioModels Harvest")
        log.info(f"  Model range: {all_model_ids[0]} to {all_model_ids[-1]}")
        log.info(f"  Total models to attempt: {len(all_model_ids)}")
        log.info(f"  Batch size: {args.batch_size}")
        log.info("="*60)

        # Process in batches to avoid memory issues
        for batch_start in range(0, len(all_model_ids), args.batch_size):
            batch_end = min(batch_start + args.batch_size, len(all_model_ids))
            batch = all_model_ids[batch_start:batch_end]

            batch_num = (batch_start // args.batch_size) + 1
            total_batches = (len(all_model_ids) + args.batch_size - 1) // args.batch_size

            log.info(f"\n{'='*60}")
            log.info(f"BATCH {batch_num}/{total_batches}: {batch[0]} to {batch[-1]}")
            log.info(f"{'='*60}")

            # Harvest batch in parallel
            harvester.harvest_parallel(
                batch,
                download_workers=args.download_workers,
                parse_workers=args.parse_workers
            )

            log.info(f"✓ Batch {batch_num}/{total_batches} complete")

        log.info("\n" + "="*60)
        log.info("COMPLETE HARVEST FINISHED")
        log.info("="*60)

    finally:
        conn.close()


if __name__ == '__main__':
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] %(message)s',
        datefmt='%H:%M:%S'
    )

    main()
