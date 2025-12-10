#!/usr/bin/env python3
"""
Query script for Layer 0-2 formulas in bioformulas database.
Demonstrates how to retrieve and use the mathematical formulations.
"""

import sqlite3
from pathlib import Path
from tabulate import tabulate

DB_PATH = Path(__file__).parent / 'bioformulas.db'

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def query_layer_formulas(layer_num):
    """Query all formulas for a specific layer."""
    conn = get_connection()

    results = conn.execute("""
        SELECT
            f.name,
            f.latex,
            f.formula_type,
            f.description,
            f.python_code,
            f.publication_year,
            f.publication_doi
        FROM formulas f
        JOIN categories c ON f.category_id = c.category_id
        WHERE c.name LIKE ?
        ORDER BY f.formula_id
    """, (f'Layer {layer_num}%',)).fetchall()

    conn.close()
    return results

def print_formula_details(formula):
    """Pretty print a formula with all details."""
    print("=" * 80)
    print(f"Name: {formula['name']}")
    print(f"Type: {formula['formula_type']}")
    if formula['publication_year']:
        print(f"Year: {formula['publication_year']}")
    if formula['publication_doi']:
        print(f"DOI: {formula['publication_doi']}")
    print("-" * 80)
    print(f"LaTeX:\n  {formula['latex']}")
    print("-" * 80)
    print(f"Description:\n  {formula['description']}")
    if formula['python_code']:
        print("-" * 80)
        print("Python Implementation:")
        print(formula['python_code'])
    print("=" * 80)
    print()

def search_formulas(search_term):
    """Full-text search across formulas."""
    conn = get_connection()

    results = conn.execute("""
        SELECT
            f.name,
            f.latex,
            f.description,
            c.name as category
        FROM formulas f
        JOIN categories c ON f.category_id = c.category_id
        WHERE f.name LIKE ? OR f.description LIKE ?
        ORDER BY f.name
    """, (f'%{search_term}%', f'%{search_term}%')).fetchall()

    conn.close()
    return results

def get_formula_by_name(name):
    """Retrieve specific formula by name."""
    conn = get_connection()

    result = conn.execute("""
        SELECT
            f.*,
            c.name as category_name
        FROM formulas f
        JOIN categories c ON f.category_id = c.category_id
        WHERE f.name = ?
    """, (name,)).fetchone()

    conn.close()
    return result

def main():
    print("BioAI Layers 0-2 Formula Database Query Tool")
    print("=" * 80)

    # Summary by layer
    print("\nFORMULA COUNTS BY LAYER:")
    print("-" * 80)
    for layer in [0, 1, 2]:
        formulas = query_layer_formulas(layer)
        print(f"Layer {layer}: {len(formulas)} formulas")

    # Display all Layer 0 formulas
    print("\n\nLAYER 0: PHYSICAL SUBSTRATE FORMULAS")
    print("=" * 80)
    layer0_formulas = query_layer_formulas(0)

    table_data = []
    for f in layer0_formulas:
        table_data.append([
            f['name'],
            f['formula_type'],
            f['latex'][:50] + '...' if len(f['latex']) > 50 else f['latex']
        ])

    print(tabulate(table_data, headers=['Name', 'Type', 'LaTeX (truncated)'], tablefmt='grid'))

    # Show detailed example: Langevin equation
    print("\n\nDETAILED EXAMPLE: Langevin Equation (Overdamped)")
    langevin = get_formula_by_name("Langevin Equation (Overdamped)")
    if langevin:
        print_formula_details(langevin)

    # Display all Layer 2 formulas
    print("\nLAYER 2: MORPHOGENESIS FORMULAS")
    print("=" * 80)
    layer2_formulas = query_layer_formulas(2)

    table_data = []
    for f in layer2_formulas:
        table_data.append([
            f['name'],
            f['formula_type'],
            f['description'][:60] + '...' if len(f['description']) > 60 else f['description']
        ])

    print(tabulate(table_data, headers=['Name', 'Type', 'Description'], tablefmt='grid'))

    # Search example
    print("\n\nSEARCH EXAMPLE: 'diffusion'")
    print("=" * 80)
    search_results = search_formulas('diffusion')

    table_data = []
    for r in search_results[:10]:  # Show first 10 results
        table_data.append([
            r['category'],
            r['name'],
            r['description'][:50] + '...' if len(r['description']) > 50 else r['description']
        ])

    print(tabulate(table_data, headers=['Category', 'Name', 'Description'], tablefmt='grid'))
    print(f"\nTotal matches: {len(search_results)}")

    # Show detailed example: Gray-Scott
    print("\n\nDETAILED EXAMPLE: Gray-Scott Model")
    gray_scott = get_formula_by_name("Gray-Scott Model")
    if gray_scott:
        print_formula_details(gray_scott)

if __name__ == '__main__':
    main()
