
# XML Parser for UniProt, InterPro, Reactome
import xml.etree.ElementTree as ET

def parse_uniprot_xml(file_path):
    """Parse UniProt XML files."""
    proteins = []

    tree = ET.parse(file_path)
    root = tree.getroot()

    ns = {'u': 'http://uniprot.org/uniprot'}

    for entry in root.findall('u:entry', ns):
        protein = {
            'id': entry.find('u:accession', ns).text if entry.find('u:accession', ns) is not None else None,
            'name': entry.find('u:name', ns).text if entry.find('u:name', ns) is not None else None,
            'genes': [],
            'features': []
        }

        for gene in entry.findall('.//u:gene', ns):
            if gene.text:
                protein['genes'].append(gene.text)

        for feature in entry.findall('.//u:feature', ns):
            protein['features'].append({
                'type': feature.get('type'),
                'description': feature.get('description')
            })

        proteins.append(protein)

    return proteins
