
# TSV/CSV Parser
import csv

def parse_tsv(file_path, delimiter='\t'):
    """Parse tab/comma-separated value files."""
    rows = []
    with open(file_path) as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        rows = list(reader)
    return rows
