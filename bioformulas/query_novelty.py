#!/usr/bin/env python3
"""
Query NOVELTY.db - Database of novel AI architectures derived from biology

Usage:
    python3 query_novelty.py list
    python3 query_novelty.py search "MAPK"
    python3 query_novelty.py show 11
    python3 query_novelty.py stats
"""

import sqlite3
import sys

def connect():
    return sqlite3.connect('NOVELTY.db')

def list_all():
    """List all architectures"""
    conn = connect()
    cur = conn.cursor()
    cur.execute('SELECT id, name, description FROM novel_architectures ORDER BY id')

    print("="*80)
    print("NOVEL AI ARCHITECTURES - FULL CATALOG")
    print("="*80)
    print()

    for id, name, desc in cur.fetchall():
        print(f"{id:2d}. {name}")
        print(f"    {desc[:120]}...")
        print()

    conn.close()

def search(keyword):
    """Search architectures by keyword"""
    conn = connect()
    cur = conn.cursor()

    cur.execute('''
        SELECT id, name, description, use_in_nature
        FROM novel_architectures
        WHERE name LIKE ? OR description LIKE ? OR use_in_nature LIKE ? OR source LIKE ?
        ORDER BY id
    ''', (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'))

    results = cur.fetchall()

    print("="*80)
    print(f"SEARCH RESULTS FOR: '{keyword}' ({len(results)} found)")
    print("="*80)
    print()

    if not results:
        print("No matches found.")
        return

    for id, name, desc, nature in results:
        print(f"{id:2d}. {name}")
        print(f"    Description: {desc[:100]}...")
        print(f"    In Nature: {nature[:100]}...")
        print()

    conn.close()

def show(arch_id):
    """Show full details of an architecture"""
    conn = connect()
    cur = conn.cursor()

    cur.execute('''
        SELECT name, description, use_in_nature, architecture, source, created_date
        FROM novel_architectures
        WHERE id = ?
    ''', (arch_id,))

    result = cur.fetchone()

    if not result:
        print(f"Architecture ID {arch_id} not found.")
        return

    name, desc, nature, arch, source, date = result

    print("="*80)
    print(f"ARCHITECTURE #{arch_id}: {name}")
    print("="*80)
    print()
    print(f"DESCRIPTION:")
    print(f"  {desc}")
    print()
    print(f"USE IN NATURE:")
    print(f"  {nature}")
    print()
    print(f"SOURCE:")
    print(f"  {source}")
    print()
    print(f"ARCHITECTURE:")
    print("-"*80)
    print(arch)
    print("-"*80)
    print()
    print(f"Created: {date}")
    print()

    conn.close()

def stats():
    """Show database statistics"""
    conn = connect()
    cur = conn.cursor()

    cur.execute('SELECT COUNT(*) FROM novel_architectures')
    total = cur.fetchone()[0]

    # Count by category (based on name)
    categories = {
        'Metabolic': 0,
        'Activation': 0,
        'Learning': 0,
        'Oscillatory': 0,
        'Amplification': 0,
        'Routing': 0,
        'Energy': 0,
        'Other': 0
    }

    cur.execute('SELECT name FROM novel_architectures')
    for (name,) in cur.fetchall():
        if 'Metabolic' in name:
            categories['Metabolic'] += 1
        elif 'Activation' in name:
            categories['Activation'] += 1
        elif 'Learning' in name or 'STDP' in name or 'BCM' in name or 'Oja' in name:
            categories['Learning'] += 1
        elif 'Oscillatory' in name or 'Kuramoto' in name or 'FitzHugh' in name or 'Van der Pol' in name:
            categories['Oscillatory'] += 1
        elif 'Amplif' in name or 'MAPK' in name:
            categories['Amplification'] += 1
        elif 'Router' in name or 'Routing' in name:
            categories['Routing'] += 1
        elif 'Energy' in name or 'ATP' in name:
            categories['Energy'] += 1
        else:
            categories['Other'] += 1

    print("="*80)
    print("NOVELTY.db STATISTICS")
    print("="*80)
    print()
    print(f"Total Architectures: {total}")
    print()
    print("By Category:")
    for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
        if count > 0:
            print(f"  {cat:20s}: {count:2d}")
    print()

    # Top sources
    cur.execute('''
        SELECT source, COUNT(*) as cnt
        FROM novel_architectures
        GROUP BY source
        ORDER BY cnt DESC
        LIMIT 5
    ''')

    print("Top Sources:")
    for source, count in cur.fetchall():
        print(f"  [{count}] {source[:60]}...")
    print()

    conn.close()

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    command = sys.argv[1]

    if command == 'list':
        list_all()
    elif command == 'search' and len(sys.argv) > 2:
        search(sys.argv[2])
    elif command == 'show' and len(sys.argv) > 2:
        show(int(sys.argv[2]))
    elif command == 'stats':
        stats()
    else:
        print(__doc__)

if __name__ == '__main__':
    main()
