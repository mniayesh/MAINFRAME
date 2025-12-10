
# SDF (Structural Data Format) Parser for ChEBI/PubChem
def parse_sdf(file_path, max_compounds=None):
    """Parse chemical structure files (ChEBI, PubChem)."""
    compounds = []
    current_compound = {'structure_lines': []}
    count = 0

    with open(file_path) as f:
        for line in f:
            if line.strip() == '$$$$':
                if current_compound['structure_lines']:
                    compounds.append(current_compound)
                    count += 1
                    if max_compounds and count >= max_compounds:
                        break
                current_compound = {'structure_lines': []}
            else:
                current_compound['structure_lines'].append(line)

    return compounds
