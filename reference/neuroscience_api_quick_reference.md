# Neuroscience Database API - Quick Reference
**Fast access commands for architectural primitive extraction**

## Essential API Endpoints

### Allen Brain Atlas
```bash
# Mouse brain structures (800+ regions)
curl "http://api.brain-map.org/api/v2/structure_graph_download/1.json" > allen_mouse.json

# Human brain structures (700+ regions)
curl "http://api.brain-map.org/api/v2/structure_graph_download/10.json" > allen_human.json

# Search structures
curl "http://api.brain-map.org/api/v2/data/Structure/query.json?criteria=[name$li'*cortex*']"

# Cell types query
curl "http://api.brain-map.org/api/v2/data/ApiCellTypesSpecimenDetail/query.json"
```

**Allen SDK (Python):**
```python
from allensdk.core.structure_tree import StructureTree
from allensdk.api.queries.ontologies_api import OntologiesApi

oapi = OntologiesApi()
structures = oapi.get_structures_with_sets([1])
tree = StructureTree.clean_structures(structures)
```

### NeuroMorpho.org
```bash
# Search neurons by region
curl "http://neuromorpho.org/api/neuron/select?q=brain_region:hippocampus&size=100"

# Search by cell type
curl "http://neuromorpho.org/api/neuron/select?q=cell_type:pyramidal&size=50"

# Get neuron info
curl "http://neuromorpho.org/api/neuron/name/cnic_001"
```

**Python:**
```python
from neuromorphopy import NeuroMorpho
nm = NeuroMorpho()
results = nm.search(brain_region='hippocampus', species='mouse')
```

### Cell Ontology
```bash
# Download full ontology
wget http://purl.obolibrary.org/obo/cl.json
wget http://purl.obolibrary.org/obo/cl.owl
wget http://purl.obolibrary.org/obo/cl.obo

# OLS API - Search neurons
curl "https://www.ebi.ac.uk/ols/api/search?q=neuron&ontology=cl"

# Get neuron class
curl "https://www.ebi.ac.uk/ols/api/ontologies/cl/terms?iri=http://purl.obolibrary.org/obo/CL_0000540"
```

**Python:**
```python
from oaklib import get_adapter
cl = get_adapter("sqlite:obo:cl")
neurons = list(cl.descendants("CL:0000540"))  # All neuron types
```

### NeuroNames
```bash
# Download complete nomenclature (3000+ structures)
wget http://braininfo.rprc.washington.edu/Nnont.aspx -O neuronames.json
```

### Brain Atlases

**Glasser Atlas (HCP-MMP1.0):**
- BALSA: https://balsa.wustl.edu/ (File ID: nvrZ)
- Figshare: https://figshare.com/articles/dataset/2016_Glasser_MMP1_0_Cortical_Atlases/24431146
- GitHub: https://github.com/mbedini/The-HCP-MMP1.0-atlas-in-FSL

**BigBrain:**
- Download: https://bigbrain.loris.ca
- API: https://siibra-api-stable.apps.tc.humanbrainproject.eu/

**HCP Connectome:**
- Portal: https://db.humanconnectome.org/ (requires free account)
- GitHub DataLad: https://github.com/datalad-datasets/human-connectome-project-openaccess

## Target Extraction Numbers

| Data Type | Target | Primary Source | Format |
|-----------|--------|----------------|---------|
| Brain Regions | 200-300 | Allen + Glasser + NeuroNames | JSON |
| Neuron Types | 100-1000 | Cell Ontology + Allen ABC | JSON/OBO |
| Circuit Motifs | <100 | Literature + ModelDB | Custom JSON |
| Connectivity | N×N matrices | Allen Connectivity + HCP | CSV/NRRD |

## One-Line Installation Commands

```bash
# Python packages
pip install allensdk neuromorphopy oaklib pandas numpy

# For HCP data
pip install neurohcp datalad

# For image processing
pip install nibabel pynrrd SimpleITK
```

## Quick Extraction Script

```python
#!/usr/bin/env python3
"""Quick extraction of neuroscience architectural primitives"""

import json
from allensdk.api.queries.ontologies_api import OntologiesApi
from allensdk.core.structure_tree import StructureTree
from oaklib import get_adapter

# 1. Brain Regions (Allen)
print("Extracting brain regions...")
oapi = OntologiesApi()
structures = oapi.get_structures_with_sets([1])
tree = StructureTree.clean_structures(structures)
regions = [s for s in tree.nodes() if 3 <= s.get('depth', 0) <= 7]
print(f"Found {len(regions)} brain regions")
with open('brain_regions.json', 'w') as f:
    json.dump(regions, f, indent=2)

# 2. Neuron Types (Cell Ontology)
print("Extracting neuron types...")
cl = get_adapter("sqlite:obo:cl")
neurons = list(cl.descendants("CL:0000540"))
neuron_data = [{
    'id': n,
    'name': cl.label(n),
    'definition': cl.definition(n)
} for n in neurons]
print(f"Found {len(neuron_data)} neuron types")
with open('neuron_types.json', 'w') as f:
    json.dump(neuron_data, f, indent=2)

# 3. Circuit Motifs (Literature-based catalog)
motifs = [
    {'name': 'Feedforward Inhibition', 'category': 'feedforward'},
    {'name': 'Canonical Disinhibition', 'category': 'disinhibitory'},
    {'name': 'Winner-Take-All', 'category': 'competition'},
    {'name': 'Recurrent Excitation', 'category': 'feedback'},
    {'name': 'Lateral Inhibition', 'category': 'lateral'},
    # ... add more
]
print(f"Cataloged {len(motifs)} circuit motifs")
with open('circuit_motifs.json', 'w') as f:
    json.dump(motifs, f, indent=2)

print("\nExtraction complete!")
print(f"- {len(regions)} brain regions")
print(f"- {len(neuron_data)} neuron types")
print(f"- {len(motifs)} circuit motifs")
```

## Data Format Cheat Sheet

| Format | Extension | Used For | Read With |
|--------|-----------|----------|-----------|
| SWC | .swc | Neuron morphology | NEURON, Allen SDK |
| NWB | .nwb | Electrophysiology | pynwb |
| NRRD | .nrrd | Brain volumes | pynrrd |
| OWL | .owl | Ontologies (full) | owlready2 |
| OBO | .obo | Ontologies (simple) | oaklib |
| JSON | .json | General data | json, pandas |
| NIfTI | .nii.gz | MRI images | nibabel |
| GIFTI | .gii | Surface data | nibabel |

## Key Neuron Type IDs (Cell Ontology)

```
CL:0000540 - neuron (root)
CL:0000679 - glutamatergic neuron
CL:0000617 - GABAergic neuron
CL:0000700 - dopaminergic neuron
CL:0000850 - serotonergic neuron
CL:0000108 - cholinergic neuron
CL:0000598 - pyramidal neuron
CL:0000099 - interneuron
CL:0000118 - basket cell
CL:0000119 - cerebellar Purkinje cell
CL:0000100 - motor neuron
CL:0000101 - sensory neuron
```

## Essential Circuit Motifs (Top 10)

1. **Feedforward Inhibition (FFI)** - Timing precision
2. **Canonical Disinhibition (VIP→SST→Pyr)** - Gating
3. **Winner-Take-All** - Selection/decision
4. **Recurrent Excitation** - Working memory
5. **Lateral Inhibition** - Contrast enhancement
6. **Feedback Inhibition** - Gain control
7. **Gamma Generator (Pyr↔PV)** - Synchronization
8. **Coincidence Detector** - Temporal binding
9. **Normalization** - Invariance
10. **Thalamic Gate** - Attentional filtering

## Priority Brain Regions (Top 50)

### Cortical (25)
```
Visual: V1, V2, V4, MT, MST
Motor: M1, PMC, SMA, PMd, PMv
Prefrontal: dlPFC, vmPFC, OFC, ACC, FEF
Temporal: A1, IT, STG, MTG, parahippocampal
Parietal: S1, S2, PPC, IPS, SPL
```

### Subcortical (15)
```
Thalamus: LGN, MGN, VPL, VPM, MD, Pulvinar
Basal Ganglia: Striatum, GPe, GPi, STN, SNc, SNr
Hippocampus: CA1, CA3, DG
```

### Other (10)
```
Cerebellum, Amygdala, Hypothalamus, Superior Colliculus,
Inferior Colliculus, PAG, LC, VTA, Raphe, Substantia Nigra
```

## Connectivity Matrix Sources

1. **Allen Mouse Connectivity**: 213×213 regions, voxel-level projection data
2. **HCP Structural**: ~360 regions (Glasser), DTI tractography
3. **HCP Functional**: ~360 regions, resting-state fMRI correlations

## Common Issues & Solutions

**Issue**: Allen SDK downloads are slow
**Solution**: Use caching, specify manifest_file location

**Issue**: Cell Ontology download fails
**Solution**: Use OAK: `runoak -i sqlite:obo:cl info CL:0000540`

**Issue**: HCP requires authentication
**Solution**: Create free account at db.humanconnectome.org

**Issue**: NeuroMorpho rate limiting
**Solution**: Add delays between requests (0.1-1 second)

## Next Steps

1. Run extraction script above
2. Load data into BioFormulas database
3. Build cross-reference mappings
4. Create hierarchical indices
5. Implement query interface

## Resources

- Full Guide: `/home/user/MAINFRAME/docs/neuroscience_database_api_guide.md`
- Allen Institute: https://alleninstitute.org/
- NeuroMorpho: https://neuromorpho.org/
- Cell Ontology: https://cell-ontology.github.io/
- HCP: https://www.humanconnectome.org/
- EBRAINS: https://ebrains.eu/
