#!/usr/bin/env python3
"""
Example Usage of Biological Database Extraction Framework

This script demonstrates various ways to use the extraction framework,
from simple single-database extraction to complex multi-database orchestration.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from bio_extractors import (
    GOExtractor,
    ReactomeExtractor,
    KEGGExtractor,
    AllenBrainExtractor,
    ChEBIExtractor,
    CognitiveAtlasExtractor
)


def example_1_simple_extraction():
    """Example 1: Simple single-database extraction."""
    print("\n" + "="*80)
    print("EXAMPLE 1: Simple GO Extraction")
    print("="*80)

    # Create extractor and extract GO terms
    with GOExtractor() as extractor:
        # Extract first 50 biological process terms
        go_terms = extractor.extract(
            aspect='biological_process',
            max_terms=50
        )

        print(f"\nExtracted {len(go_terms)} GO terms")

        # Show first 3 terms
        for term in go_terms[:3]:
            print(f"\n  ID: {term['identifier']}")
            print(f"  Name: {term['name']}")
            print(f"  Type: {term['entity_type']}")

        # Print extraction statistics
        extractor.print_stats()


def example_2_with_filters():
    """Example 2: Extraction with specific filters."""
    print("\n" + "="*80)
    print("EXAMPLE 2: Reactome with Filters")
    print("="*80)

    with ReactomeExtractor() as extractor:
        # Extract only human signaling pathways
        pathways = extractor.extract(
            species='9606',  # Homo sapiens
            top_level_only=False
        )

        # Filter for signaling pathways
        signaling = [
            p for p in pathways
            if 'signal' in p.get('name', '').lower()
        ]

        print(f"\nTotal pathways: {len(pathways)}")
        print(f"Signaling pathways: {len(signaling)}")

        # Show examples
        for pathway in signaling[:3]:
            print(f"\n  {pathway['name']}")
            print(f"  Category: {pathway.get('pathway_category', 'N/A')}")


def example_3_rate_limited_extraction():
    """Example 3: Rate-limited extraction (KEGG)."""
    print("\n" + "="*80)
    print("EXAMPLE 3: KEGG (Rate Limited)")
    print("="*80)

    with KEGGExtractor() as extractor:
        # KEGG automatically enforces 3 requests/second limit
        print("\nKEGG extractor automatically rate-limits to 3 requests/second")

        # Extract human pathways
        pathways = extractor.extract(
            organism='hsa',  # Homo sapiens
        )

        print(f"\nExtracted {len(pathways)} KEGG pathways")

        # Show pathway categories
        categories = {}
        for pathway in pathways:
            cat = pathway.get('pathway_category', 'unknown')
            categories[cat] = categories.get(cat, 0) + 1

        print("\nPathway categories:")
        for category, count in sorted(categories.items(), key=lambda x: -x[1]):
            print(f"  {category:15s}: {count}")


def example_4_neuroscience_extraction():
    """Example 4: Neuroscience database extraction."""
    print("\n" + "="*80)
    print("EXAMPLE 4: Allen Brain Atlas")
    print("="*80)

    with AllenBrainExtractor() as extractor:
        # Extract brain structure hierarchy
        structures = extractor.extract(
            data_type='structure',
            species='mouse'
        )

        print(f"\nExtracted {len(structures)} brain structures")

        # Show hierarchical structure
        print("\nBrain regions (first 5):")
        for structure in structures[:5]:
            print(f"\n  {structure['name']}")
            print(f"  Location: {structure.get('anatomical_location', 'N/A')}")
            print(f"  ID: {structure['identifier']}")


def example_5_metabolic_extraction():
    """Example 5: Metabolic database extraction."""
    print("\n" + "="*80)
    print("EXAMPLE 5: ChEBI Biological Roles")
    print("="*80)

    with ChEBIExtractor() as extractor:
        # Extract biological role classifications
        roles = extractor.extract(
            extraction_type='roles',
            max_entities=30
        )

        print(f"\nExtracted {len(roles)} biological roles")

        # Show role types
        for role in roles[:5]:
            print(f"\n  {role['name']}")
            print(f"  ID: {role['identifier']}")
            print(f"  Class: {role.get('mechanism_class', 'N/A')}")


def example_6_cognitive_extraction():
    """Example 6: Cognitive database extraction."""
    print("\n" + "="*80)
    print("EXAMPLE 6: Cognitive Atlas")
    print("="*80)

    with CognitiveAtlasExtractor() as extractor:
        # Extract cognitive concepts
        concepts = extractor.extract(
            extraction_type='concepts',
            max_items=30
        )

        print(f"\nExtracted {len(concepts)} cognitive concepts")

        # Show cognitive operations
        print("\nCognitive concepts (first 5):")
        for concept in concepts[:5]:
            print(f"\n  {concept['name']}")
            print(f"  Operation: {concept.get('operation_type', 'N/A')}")


def example_7_save_results():
    """Example 7: Saving extraction results."""
    print("\n" + "="*80)
    print("EXAMPLE 7: Save Results to Files")
    print("="*80)

    with GOExtractor() as extractor:
        # Extract GO terms
        terms = extractor.extract(max_terms=50)

        # Save to JSON
        output_dir = Path('example_results')
        output_dir.mkdir(exist_ok=True)

        output_file = output_dir / 'go_terms_example.json'
        extractor.save_to_json(terms, str(output_file))

        print(f"\nSaved {len(terms)} terms to {output_file}")


def example_8_parallel_extraction():
    """Example 8: Parallel extraction from multiple databases."""
    print("\n" + "="*80)
    print("EXAMPLE 8: Parallel Extraction")
    print("="*80)

    from concurrent.futures import ThreadPoolExecutor, as_completed

    def extract_go():
        with GOExtractor() as extractor:
            return extractor.extract(max_terms=30)

    def extract_reactome():
        with ReactomeExtractor() as extractor:
            return extractor.extract()[:30]

    def extract_cognitive():
        with CognitiveAtlasExtractor() as extractor:
            return extractor.extract(max_items=30)

    # Extract in parallel
    results = {}
    tasks = {
        'GO': extract_go,
        'Reactome': extract_reactome,
        'CognitiveAtlas': extract_cognitive
    }

    print("\nExtracting from 3 databases in parallel...")

    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {
            executor.submit(task): name
            for name, task in tasks.items()
        }

        for future in as_completed(futures):
            db_name = futures[future]
            try:
                result = future.result()
                results[db_name] = result
                print(f"  ✓ {db_name}: {len(result)} items")
            except Exception as e:
                print(f"  ✗ {db_name}: {str(e)}")

    total_items = sum(len(items) for items in results.values())
    print(f"\nTotal items extracted: {total_items}")


def example_9_caching_demonstration():
    """Example 9: Demonstrate caching mechanism."""
    print("\n" + "="*80)
    print("EXAMPLE 9: Caching Demonstration")
    print("="*80)

    import time

    with GOExtractor() as extractor:
        # First extraction (cache miss)
        print("\n1st extraction (cache MISS):")
        start = time.time()
        terms1 = extractor.extract(max_terms=50)
        duration1 = time.time() - start
        print(f"  Duration: {duration1:.2f}s")
        print(f"  Items: {len(terms1)}")

        # Second extraction (cache hit)
        print("\n2nd extraction (cache HIT):")
        start = time.time()
        terms2 = extractor.extract(max_terms=50)
        duration2 = time.time() - start
        print(f"  Duration: {duration2:.2f}s")
        print(f"  Items: {len(terms2)}")

        # Show speedup
        speedup = duration1 / max(duration2, 0.001)
        print(f"\nSpeedup: {speedup:.1f}x faster")

        # Show cache statistics
        stats = extractor.get_stats()
        print(f"\nCache hit rate: {stats['cache_hit_rate_percent']:.1f}%")


def main():
    """Run all examples."""
    print("\n" + "="*80)
    print("BIOLOGICAL DATABASE EXTRACTION FRAMEWORK")
    print("Example Usage Demonstrations")
    print("="*80)

    examples = [
        ("Simple Extraction", example_1_simple_extraction),
        ("Filtered Extraction", example_2_with_filters),
        ("Rate Limited (KEGG)", example_3_rate_limited_extraction),
        ("Neuroscience", example_4_neuroscience_extraction),
        ("Metabolic", example_5_metabolic_extraction),
        ("Cognitive", example_6_cognitive_extraction),
        ("Save Results", example_7_save_results),
        ("Parallel Extraction", example_8_parallel_extraction),
        ("Caching Demo", example_9_caching_demonstration),
    ]

    # Run specific example or all
    import sys
    if len(sys.argv) > 1:
        try:
            example_num = int(sys.argv[1])
            if 1 <= example_num <= len(examples):
                name, func = examples[example_num - 1]
                print(f"\nRunning Example {example_num}: {name}")
                func()
            else:
                print(f"Invalid example number. Choose 1-{len(examples)}")
        except ValueError:
            print("Usage: python example_usage.py [example_number]")
    else:
        # Run all examples
        for i, (name, func) in enumerate(examples, 1):
            try:
                func()
            except Exception as e:
                print(f"\nExample {i} failed: {str(e)}")

    print("\n" + "="*80)
    print("Examples completed!")
    print("="*80 + "\n")


if __name__ == '__main__':
    main()
