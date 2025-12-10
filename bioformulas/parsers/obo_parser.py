
# OBO (Ontology Language) Parser
import re
from pathlib import Path

def parse_obo(file_path):
    """Parse Gene Ontology or similar OBO files."""
    terms = []
    current_term = {}

    with open(file_path) as f:
        for line in f:
            line = line.strip()

            if line == '[Term]':
                if current_term:
                    terms.append(current_term)
                current_term = {}
            elif line.startswith('id:'):
                current_term['id'] = line.split(':', 1)[1].strip()
            elif line.startswith('name:'):
                current_term['name'] = line.split(':', 1)[1].strip()
            elif line.startswith('def:'):
                current_term['definition'] = line.split(':', 1)[1].strip()
            elif line.startswith('relationship:'):
                if 'relationships' not in current_term:
                    current_term['relationships'] = []
                current_term['relationships'].append(line.split(':', 1)[1].strip())

    if current_term:
        terms.append(current_term)

    return terms
