
# JSON Parser for modern databases
import json

def parse_json_catalog(file_path):
    """Parse JSON catalog files."""
    with open(file_path) as f:
        data = json.load(f)
    return data if isinstance(data, list) else [data]
