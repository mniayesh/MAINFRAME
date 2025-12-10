#!/usr/bin/env python3
"""
Parallel Database Extraction with Error Prevention

Runs multiple database extractors in parallel to maximize throughput.
Uses fixed extractors (Reactome, InterPro) plus working originals.
"""

import logging
import json
import sys
import time
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, Any, List, Tuple

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Import fixed extractors
from reactome_extractor_fixed import ReactomeExtractorFixed
from interpro_extractor_fixed import InterProExtractorFixed
from kegg_extractor_fixed import KEGGExtractorFixed
from allen_brain_extractor_fixed import AllenBrainExtractorFixed
from cognitive_atlas_extractor_fixed import CognitiveAtlasExtractorFixed

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeRemainingColumn
from rich.live import Live
from rich.layout import Layout

console = Console()
logging.basicConfig(level=logging.WARNING, format='%(levelname)s:%(name)s:%(message)s')


class ParallelExtractor:
    """Orchestrates parallel extraction from multiple databases"""

    def __init__(self, max_workers: int = 5):
        self.max_workers = max_workers
        self.results = {}
        self.start_time = None
        self.end_time = None

    def extract_reactome(self) -> Tuple[str, Dict[str, Any]]:
        """Extract Reactome pathways (FIXED)"""
        try:
            console.print("[cyan]Starting Reactome extraction...[/cyan]")
            extractor = ReactomeExtractorFixed()
            pathways = extractor.extract_pathways(max_pathways=200, top_level_only=False)

            return 'Reactome', {
                'status': 'success',
                'count': len(pathways),
                'data': pathways[:100],  # Sample
                'was_fixed': True,
                'stats': extractor.get_stats()
            }
        except Exception as e:
            logging.error(f"Reactome error: {e}")
            return 'Reactome', {'status': 'failed', 'error': str(e), 'was_fixed': True}

    def extract_interpro(self) -> Tuple[str, Dict[str, Any]]:
        """Extract InterPro entries (FIXED)"""
        try:
            console.print("[cyan]Starting InterPro extraction...[/cyan]")
            extractor = InterProExtractorFixed()
            entries = extractor.extract_entries(entry_type='domain', max_entries=200)

            return 'InterPro', {
                'status': 'success',
                'count': len(entries),
                'data': entries[:50],  # Sample
                'was_fixed': True,
                'stats': extractor.get_stats()
            }
        except Exception as e:
            logging.error(f"InterPro error: {e}")
            return 'InterPro', {'status': 'failed', 'error': str(e), 'was_fixed': True}

    def extract_kegg(self) -> Tuple[str, Dict[str, Any]]:
        """Extract KEGG pathways (FIXED)"""
        try:
            console.print("[cyan]Starting KEGG extraction...[/cyan]")
            extractor = KEGGExtractorFixed()
            pathways = extractor.extract_pathways(organism='hsa', max_pathways=200)

            return 'KEGG', {
                'status': 'success',
                'count': len(pathways),
                'data': pathways[:50],  # Sample
                'was_fixed': True,
                'stats': extractor.get_stats()
            }
        except Exception as e:
            logging.error(f"KEGG error: {e}")
            return 'KEGG', {'status': 'failed', 'error': str(e), 'was_fixed': True}

    def extract_allen_brain(self) -> Tuple[str, Dict[str, Any]]:
        """Extract Allen Brain structures (FIXED)"""
        try:
            console.print("[cyan]Starting Allen Brain extraction...[/cyan]")
            extractor = AllenBrainExtractorFixed()
            structures = extractor.extract_structures(max_structures=300)

            return 'AllenBrain', {
                'status': 'success',
                'count': len(structures),
                'data': structures[:50],  # Sample
                'was_fixed': True,
                'stats': extractor.get_stats()
            }
        except Exception as e:
            logging.error(f"Allen Brain error: {e}")
            return 'AllenBrain', {'status': 'failed', 'error': str(e), 'was_fixed': True}

    def extract_cognitive_atlas(self) -> Tuple[str, Dict[str, Any]]:
        """Extract Cognitive Atlas concepts (FIXED)"""
        try:
            console.print("[cyan]Starting Cognitive Atlas extraction...[/cyan]")
            extractor = CognitiveAtlasExtractorFixed()
            concepts = extractor.extract_concepts(max_concepts=300)

            return 'CognitiveAtlas', {
                'status': 'success',
                'count': len(concepts),
                'data': concepts[:50],  # Sample
                'was_fixed': True,
                'stats': extractor.get_stats()
            }
        except Exception as e:
            logging.error(f"Cognitive Atlas error: {e}")
            return 'CognitiveAtlas', {'status': 'failed', 'error': str(e), 'was_fixed': True}

    def run_parallel(self) -> Dict[str, Dict[str, Any]]:
        """Run all extractors in parallel"""

        console.print(Panel(
            "[bold cyan]PARALLEL DATABASE EXTRACTION[/bold cyan]\n"
            f"Running {self.max_workers} extractors concurrently\n"
            "Using error-prevention infrastructure",
            title="Biological Database Extraction",
            border_style="cyan"
        ))

        self.start_time = time.time()

        # Define extraction tasks
        tasks = [
            ('Reactome', self.extract_reactome),
            ('InterPro', self.extract_interpro),
            ('KEGG', self.extract_kegg),
            ('AllenBrain', self.extract_allen_brain),
            ('CognitiveAtlas', self.extract_cognitive_atlas),
        ]

        results = {}
        completed = 0
        total = len(tasks)

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn(),
            console=console
        ) as progress:

            overall_task = progress.add_task(
                "[cyan]Overall Progress",
                total=total
            )

            # Run extractions in parallel
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                # Submit all tasks
                future_to_name = {
                    executor.submit(task_fn): name
                    for name, task_fn in tasks
                }

                # Collect results as they complete
                for future in as_completed(future_to_name):
                    name = future_to_name[future]

                    try:
                        db_name, result = future.result()
                        results[db_name] = result

                        status = "✓" if result['status'] == 'success' else "✗"
                        count = result.get('count', 0)

                        console.print(
                            f"{status} [bold]{db_name}[/bold]: {count} entities"
                        )

                    except Exception as e:
                        console.print(f"[red]✗ {name}: {e}[/red]")
                        results[name] = {'status': 'failed', 'error': str(e)}

                    completed += 1
                    progress.update(overall_task, completed=completed)

        self.end_time = time.time()
        self.results = results

        return results

    def print_summary(self):
        """Print extraction summary with rich formatting"""

        duration = self.end_time - self.start_time if self.end_time else 0

        # Calculate totals
        total_dbs = len(self.results)
        successful = sum(1 for r in self.results.values() if r['status'] == 'success')
        total_entities = sum(r.get('count', 0) for r in self.results.values())
        fixed_dbs = sum(1 for r in self.results.values() if r.get('was_fixed', False) and r['status'] == 'success')

        # Create summary table
        console.print("\n")
        table = Table(show_header=True, header_style="bold magenta", title="Extraction Results")
        table.add_column("Database", style="cyan", width=20)
        table.add_column("Status", width=12)
        table.add_column("Entities", justify="right", width=10)
        table.add_column("Fixed?", width=10)
        table.add_column("Cache Hit Rate", width=15)

        for db_name, result in sorted(self.results.items()):
            if result['status'] == 'success':
                status = "[green]✓ Success[/green]"
                count = str(result.get('count', 0))
                fixed = "[yellow]Yes[/yellow]" if result.get('was_fixed', False) else "No"

                # Get cache stats if available
                stats = result.get('stats', {})
                cache_rate = stats.get('cache_hit_rate', 'N/A')

            else:
                status = "[red]✗ Failed[/red]"
                count = "0"
                fixed = "[yellow]Yes[/yellow]" if result.get('was_fixed', False) else "No"
                cache_rate = "N/A"

            table.add_row(db_name, status, count, fixed, cache_rate)

        console.print(table)

        # Print summary panel
        console.print("\n")
        console.print(Panel(
            f"[bold]Total Databases:[/bold] {total_dbs}\n"
            f"[bold]Successful:[/bold] {successful}\n"
            f"[bold]Success Rate:[/bold] {successful/total_dbs*100:.1f}%\n"
            f"[bold]Total Entities:[/bold] {total_entities:,}\n"
            f"[bold]Fixed Databases:[/bold] {fixed_dbs}\n"
            f"[bold]Duration:[/bold] {duration:.1f}s\n"
            f"[bold]Throughput:[/bold] {total_entities/duration if duration > 0 else 0:.1f} entities/sec",
            title="[bold green]Parallel Extraction Summary",
            border_style="green"
        ))

    def save_results(self, output_dir: Path = Path('extraction_results')):
        """Save extraction results to files"""

        output_dir.mkdir(exist_ok=True)

        # Save overall report
        report = {
            'timestamp': datetime.now().isoformat(),
            'duration_seconds': self.end_time - self.start_time if self.end_time else 0,
            'results': {
                db: {k: v for k, v in result.items() if k != 'data'}  # Exclude full data
                for db, result in self.results.items()
            },
            'summary': {
                'total_databases': len(self.results),
                'successful': sum(1 for r in self.results.values() if r['status'] == 'success'),
                'total_entities': sum(r.get('count', 0) for r in self.results.values()),
                'fixed_databases': sum(1 for r in self.results.values() if r.get('was_fixed', False) and r['status'] == 'success')
            }
        }

        report_file = output_dir / 'parallel_extraction_report.json'
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)

        console.print(f"\n[green]✓ Report saved to: {report_file}[/green]")

        # Save individual database results
        for db_name, result in self.results.items():
            if result['status'] == 'success' and 'data' in result:
                db_file = output_dir / f'{db_name}_parallel.json'
                with open(db_file, 'w') as f:
                    json.dump(result['data'], f, indent=2)
                console.print(f"[green]✓ {db_name} data saved to: {db_file}[/green]")


def main():
    """Main execution function"""

    extractor = ParallelExtractor(max_workers=5)

    # Run parallel extraction
    results = extractor.run_parallel()

    # Print summary
    extractor.print_summary()

    # Save results
    extractor.save_results()

    return results


if __name__ == '__main__':
    try:
        results = main()
    except KeyboardInterrupt:
        console.print("\n[yellow]Extraction interrupted by user[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")
        import traceback
        traceback.print_exc()
