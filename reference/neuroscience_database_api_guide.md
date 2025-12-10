# Neuroscience Database API Guide
## Architectural Primitives Extraction for Biological Modeling

**Last Updated:** 2025-12-10
**Purpose:** Extract ~200-300 brain regions, ~100-1000 neuron types, canonical circuit motifs (<100), and hierarchical connectivity patterns from major neuroscience databases.

---

## Table of Contents
1. [Allen Brain Atlas](#1-allen-brain-atlas)
2. [NeuroMorpho.org](#2-neuromorphoorg)
3. [Brain Atlases (Glasser, BigBrain, HCP)](#3-brain-atlases)
4. [Cell Ontology (CL)](#4-cell-ontology-cl)
5. [NeuroNames](#5-neuronames)
6. [Canonical Circuit Motifs](#6-canonical-circuit-motifs)
7. [Data Formats Reference](#7-data-formats-reference)
8. [Extraction Strategy Summary](#8-extraction-strategy-summary)

---

## 1. Allen Brain Atlas

### 1.1 Overview
The Allen Institute for Brain Science provides comprehensive access to brain structure, gene expression, cell types, and connectivity data through RESTful APIs and the Allen SDK.

### 1.2 API Endpoints

#### Base API URL
```
http://api.brain-map.org/
```

#### Key Endpoints

**RESTful Model Access (RMA):**
```
http://api.brain-map.org/api/v2/data/[Model].[format]?criteria=[filters]
```

**Structure Graph Download:**
```
http://api.brain-map.org/api/v2/structure_graph_download/[id].[json|xml]
```

Specific atlases:
- Mouse Brain: `http://api.brain-map.org/api/v2/structure_graph_download/1.json`
- Human Brain: `http://api.brain-map.org/api/v2/structure_graph_download/10.json`
- Developing Human: `http://api.brain-map.org/api/v2/structure_graph_download/16.json`

**Cell Types Database:**
```
http://api.brain-map.org/ (accessed via RMA queries)
```

**Mouse Connectivity:**
```
http://api.brain-map.org/ (connectivity-specific queries)
```

### 1.3 Authentication & Access
- **No authentication required** for most API queries
- Free and open access under Allen Institute Terms of Use
- Rate limiting may apply (not explicitly documented)
- AWS credentials required for bulk data downloads via S3

### 1.4 Data Formats & Schemas

**Supported Formats:**
- JSON (primary)
- XML
- CSV
- NRRD (volumetric brain data)
- SWC (morphology reconstructions)
- NWB (Neurodata Without Borders - electrophysiology)

**Key Data Models:**
- Structure
- Ontology
- StructureGraph
- ApiCellTypesSpecimenDetail
- Specimen
- Experiment

### 1.5 Key Entity Types

#### A. Brain Regions & Hierarchies

**Structure Fields:**
- `id`: Unique structure identifier
- `acronym`: Short abbreviation
- `name`: Full anatomical name
- `parent_structure_id`: Hierarchical parent
- `structure_id_path`: Full path from root
- `depth`: Level in hierarchy
- `graph_order`: Traversal order
- `color_hex_triplet`: Visualization color
- `ontology_id`: Associated ontology

**Coverage:**
- Mouse Brain: ~800+ structures (hierarchical)
- Human Brain: ~700+ structures
- Developing Human: ~500+ structures

**Example Query - Get All Brain Structures:**
```bash
curl "http://api.brain-map.org/api/v2/data/Structure/query.json?criteria=[graph_id$eq1]&num_rows=2000"
```

**Example Query - Get Cortical Regions:**
```bash
curl "http://api.brain-map.org/api/v2/data/Structure/query.json?criteria=[graph_id$eq1][name$li'*cortex*']"
```

#### B. Cell Types (Allen Cell Types Database)

**ABC Atlas - Comprehensive Cell Type Taxonomy:**
- **5,322 cell type clusters** (mouse whole brain)
- Organized hierarchically:
  - 34 classes
  - 338 subclasses
  - 1,201 supertypes
  - 5,322 types/clusters
- Cross-species taxonomy: 1,435 clusters

**Cell Type Metadata:**
- Structure (brain region)
- Cortical layer
- Dendrite type (spiny, aspiny, sparsely spiny)
- Apical dendrite status (intact, truncated)
- Morphology classification
- Electrophysiology properties
- Transcriptomic profile
- Neurotransmitter type
- Marker genes
- Transcription factors
- Neuropeptides

**Example Query - Cell Specimens:**
```bash
curl "http://api.brain-map.org/api/v2/data/ApiCellTypesSpecimenDetail/query.json?criteria=[specimen_id$eq464212183]"
```

**Neuron Classification Dimensions:**
1. **By Neurotransmitter:**
   - Glutamatergic (excitatory)
   - GABAergic (inhibitory)
   - Dopaminergic
   - Serotonergic
   - Cholinergic

2. **By Morphology:**
   - Pyramidal neurons
   - Stellate cells
   - Basket cells
   - Chandelier cells
   - Martinotti cells

3. **By Marker Expression:**
   - Parvalbumin (PV)
   - Somatostatin (SST)
   - Vasoactive intestinal peptide (VIP)
   - Calbindin
   - Calretinin

4. **By Electrophysiology:**
   - Fast-spiking
   - Regular-spiking
   - Burst-spiking
   - Low-threshold spiking

#### C. Connectivity Matrices

**Mouse Connectivity Atlas:**
- 213×213 connectivity matrix (Oh et al. 2014)
- Available as CSV downloads
- Ipsilateral and contralateral projections
- Voxel-level projection density grids

**Example Query - Projection Data:**
```bash
curl "http://api.brain-map.org/api/v2/data/StructureUnionize/query.json?criteria=[section_data_set_id$eq181599674]"
```

**Connectivity Data Format (NRRD):**
- 3D projection density grids
- Registered to Common Coordinate Framework (CCF)
- 10, 25, 50, 100 μm resolutions

#### D. Network Modules

**Functional Networks:**
- Default mode network
- Salience network
- Executive control network
- Sensorimotor networks
- Visual processing streams

**Anatomical Circuits:**
- Hippocampal formation
- Basal ganglia loops
- Thalamocortical circuits
- Cerebellar pathways

### 1.6 Allen SDK (Python)

**Installation:**
```bash
pip install allensdk
```

**Example - Download Structure Ontology:**
```python
from allensdk.core.structure_tree import StructureTree
from allensdk.api.queries.ontologies_api import OntologiesApi

oapi = OntologiesApi()
structure_graph = oapi.get_structures_with_sets([1])  # 1 = Mouse Brain Atlas
structure_tree = StructureTree.clean_structures(structure_graph)

# Get all cortical structures
cortical_structures = [s for s in structure_tree.nodes()
                      if 'cortex' in s['name'].lower()]
print(f"Found {len(cortical_structures)} cortical structures")
```

**Example - Cell Types Data:**
```python
from allensdk.core.cell_types_cache import CellTypesCache

ctc = CellTypesCache(manifest_file='cell_types/manifest.json')

# Get all cells
cells = ctc.get_cells()
print(f"Total cells: {len(cells)}")

# Get morphology data
morphology = ctc.get_reconstruction(specimen_id=464212183)

# Get electrophysiology data
ephys_data = ctc.get_ephys_data(specimen_id=464212183)
```

**Example - Mouse Connectivity:**
```python
from allensdk.core.mouse_connectivity_cache import MouseConnectivityCache

mcc = MouseConnectivityCache(manifest_file='connectivity/manifest.json')

# Get structure tree
structure_tree = mcc.get_structure_tree()

# Get projection density for an experiment
pd = mcc.get_projection_density(experiment_id=181599674)

# Get connectivity matrix
connectivity_matrix = mcc.get_structure_unionizes([181599674])
```

### 1.7 Bulk Download Options

**ABC Atlas Data:**
- GitHub repository: Cell type annotations, taxonomy tables
- S3 buckets: Single-cell RNA-seq, spatial transcriptomics
- Access via `AbcProjectCache` Python class

**Cell Types Database:**
- Morphology reconstructions (SWC): Via specimen ID
- Electrophysiology (NWB): Via specimen ID
- Transcriptomics: Via Allen SDK

**Connectivity Data:**
- Structure unionizes CSV: Projection densities by region
- NRRD grid data: 3D volumetric projections
- Full experiment datasets: Via Allen SDK cache

**Documentation Links:**
- Main API: http://help.brain-map.org/display/api
- Cell Types: http://help.brain-map.org/display/celltypes/API
- Mouse Connectivity: http://help.brain-map.org/display/mouseconnectivity/API
- ABC Atlas: https://alleninstitute.github.io/abc_atlas_access/

---

## 2. NeuroMorpho.org

### 2.1 Overview
NeuroMorpho.org is the world's largest centrally curated repository of digitally reconstructed neurons and glia, containing 80,000+ morphologies from diverse species and brain regions.

### 2.2 API Endpoints

#### Base API URL
```
http://neuromorpho.org/api/
```

#### Main Endpoints

**Neuron Information:**
```
http://neuromorpho.org/api/neuron/[operation]/[value]
```

**Neuron Fields:**
```
http://neuromorpho.org/api/neuron/fields
```

**Literature References:**
```
http://neuromorpho.org/api/literature/[operation]/[value]
```

**Morphometry Data:**
```
http://neuromorpho.org/api/morphometry/[neuron_name]
```

### 2.3 Authentication & Access
- **No authentication required**
- Free and open access
- Download rate limits apply (use concurrent downloads responsibly)

### 2.4 Data Formats & Schemas

**Primary Format:**
- **SWC** (Standardized morphology format)
- Original uploaded formats also available
- Metadata in JSON

**SWC Format Specification:**
```
# Sample Structure (7 columns)
ID   Type   X   Y   Z   Radius   Parent
1    1      0   0   0   1.0      -1
2    3      0   5   0   0.5      1
3    3      0   10  0   0.5      2
```

**Type Codes:**
- 0: undefined
- 1: soma
- 2: axon
- 3: basal dendrite
- 4: apical dendrite
- 5-6: custom regions

### 2.5 Key Entity Types

#### A. Neuron Morphologies

**Metadata Fields:**
- Neuron name (unique identifier)
- Cell type
- Brain region
- Species
- Strain
- Age classification
- Gender
- Experimental condition
- Reconstruction method
- Original format
- Upload date
- Archive name

**Coverage by Category:**
- Species: 70+ animal species
- Brain regions: 200+ anatomical areas
- Cell types: 300+ classifications
- Labs: 500+ contributing laboratories

#### B. Morphometric Properties

Quantitative measurements provided for each neuron:

**Soma Metrics:**
- Surface area
- Volume
- Diameter

**Dendritic Metrics:**
- Total length
- Number of branches
- Branch order statistics
- Diameter statistics
- Segment length statistics
- Surface area
- Volume
- Bifurcation angles

**Axonal Metrics:**
- Total length
- Number of branches
- Projection patterns

**Overall Metrics:**
- Width (X extent)
- Height (Y extent)
- Depth (Z extent)
- Euclidean distance metrics

#### C. Circuit Motifs (via Morphology Analysis)

While NeuroMorpho doesn't directly catalog circuit motifs, morphologies enable identification of:

**Connectivity Patterns:**
- Feedforward architectures (pyramidal cell projections)
- Feedback loops (interneuron morphologies)
- Lateral inhibition (basket cell arborizations)

**Dendritic Processing:**
- Dendritic integration zones
- Compartmentalization patterns
- Synaptic targeting domains

### 2.6 Example API Calls

**Get Neuron Information:**
```bash
# Get neuron by name
curl "http://neuromorpho.org/api/neuron/name/cnic_001"

# Get neurons by brain region
curl "http://neuromorpho.org/api/neuron/select?q=brain_region:hippocampus"

# Get neurons by cell type
curl "http://neuromorpho.org/api/neuron/select?q=cell_type:pyramidal"
```

**Get Available Fields:**
```bash
curl "http://neuromorpho.org/api/neuron/fields"
```

**Complex Query (multiple filters):**
```bash
curl "http://neuromorpho.org/api/neuron/select?q=brain_region:neocortex,cell_type:interneuron,species:mouse&size=100"
```

**Download Morphology File:**
```
http://neuromorpho.org/dableFiles/[archive_name]/CNG%20version/[neuron_name].CNG.swc
```

### 2.7 Python Access

**Using neuromorphopy:**
```bash
pip install neuromorphopy
```

```python
from neuromorphopy import NeuroMorpho

# Initialize client
nm = NeuroMorpho()

# Search neurons
results = nm.search(
    brain_region='hippocampus',
    cell_type='pyramidal',
    species='mouse'
)

# Download morphologies
for neuron in results[:10]:
    nm.download(neuron['neuron_name'], output_dir='morphologies/')
```

**Using neuromorphr (R):**
```r
library(neuromorphr)

# Read neuron from NeuroMorpho
neuron <- neuromorpho_read_neurons("cnic_001")

# Search and download
search_results <- neuromorpho_search(brain_region="hippocampus")
```

### 2.8 Bulk Download Options

**Methods:**
1. **Direct FTP Access:**
   - Historical archive downloads
   - Organized by publication/archive

2. **API Batch Downloads:**
   - Use pagination: `?page=0&size=500`
   - Concurrent downloads with rate limiting

3. **Python Package:**
   - `neuromorphopy` supports efficient concurrent downloads
   - Automatic retry and error handling

**Recommended Strategy for Large-Scale Extraction:**
```python
from neuromorphopy import NeuroMorpho
import time

nm = NeuroMorpho()

# Target: 1000 neurons across key regions
target_regions = ['neocortex', 'hippocampus', 'striatum', 'thalamus',
                 'cerebellum', 'brainstem']

for region in target_regions:
    neurons = nm.search(brain_region=region, size=200)
    print(f"{region}: {len(neurons)} neurons available")

    # Download subset
    for neuron in neurons[:50]:
        try:
            nm.download(neuron['neuron_name'], f'data/{region}/')
            time.sleep(0.1)  # Respect rate limits
        except Exception as e:
            print(f"Error: {e}")
```

**Documentation:**
- API Reference: https://neuromorpho.org/apiReference.html
- Main Portal: https://neuromorpho.org/

---

## 3. Brain Atlases

### 3.1 Glasser Atlas (HCP-MMP1.0)

#### Overview
Multi-modal parcellation of human cortex based on Human Connectome Project data, defining 180 areas per hemisphere (360 total cortical areas).

#### Download Sources

**Primary Source - BALSA Database:**
```
https://balsa.wustl.edu/
File ID: nvrZ
```

**Figshare Repository:**
```
https://figshare.com/articles/dataset/2016_Glasser_MMP1_0_Cortical_Atlases/24431146
```

**GitHub (FSL Format):**
```
https://github.com/mbedini/The-HCP-MMP1.0-atlas-in-FSL
File: HCP-Multi-Modal-Parcellation-1.0.xml
```

**Extended Version (HCPex):**
```
https://www.oxcns.org
https://github.com/wayalan/HCPex
Includes: 360 cortical + 66 subcortical areas
```

#### Data Formats
- NIfTI volumetric (MNI152 space)
- GIFTI surface format
- FSL XML label definitions
- FreeSurfer annotation files

#### Key Features
- **180 areas per hemisphere**
- Multimodal boundaries (structure, function, connectivity)
- Standard space projections (MNI152NLin6Asym, MNI152NLin2009cAsym)

#### Example Brain Regions
```
Cortical Areas:
- Primary Visual (V1, V2, V3, V4)
- Motor Cortex (4, 6d, 6mp)
- Prefrontal (8Av, 8BL, 9a, 9p, 10d, 10v, 46)
- Temporal (STSv, TE1a, TE2a, TGd)
- Parietal (7Am, 7Pm, IPS1, LIPv)
- Language (44, 45, 55b, IFSa)
```

### 3.2 BigBrain Atlas

#### Overview
Ultra-high resolution 3D model of a human brain at nearly cellular resolution (20 μm), based on 7,404 histological sections.

#### Access Methods

**Download Portal:**
```
https://bigbrain.loris.ca
```

**EBRAINS Platform:**
```
https://www.ebrains.eu/tools/human-brain-atlas
Interactive: siibra-explorer
API: siibra-api
Python: siibra-python
```

**Primary Website:**
```
https://bigbrainproject.org/maps-and-models.html
```

#### API Access

**siibra-api (HTTP API):**
```
Base URL: https://siibra-api-stable.apps.tc.humanbrainproject.eu/

Example endpoints:
GET /atlases - List available atlases
GET /parcellations - List brain parcellations
GET /regions - Get brain regions
GET /spaces - Get reference spaces
```

**siibra-python:**
```bash
pip install siibra
```

```python
import siibra

# Access BigBrain
atlas = siibra.atlases.MULTILEVEL_HUMAN_ATLAS
bigbrain_space = siibra.spaces.BIGBRAIN

# Get parcellations
parcellation = atlas.get_parcellation('julich 2.9')

# Get regions
regions = parcellation.get_regions()
```

#### Data Formats
- Volume data: NRRD, NIfTI
- Surface meshes: OBJ, VTK
- Histological images: Various resolutions (20μm to 1mm)

#### Resolution Levels
- Full resolution: 20 μm (terabyte-scale)
- Downsampled: 40 μm, 100 μm, 200 μm, 400 μm, 1 mm

#### Key Features
- Cytoarchitectonic boundaries visible
- Subcortical nuclei delineation
- Layer-specific cortical structure
- Integration with Julich-Brain atlas (probabilistic maps)

### 3.3 HCP Connectome

#### Overview
Large-scale structural and functional connectivity datasets from 1200+ subjects, including diffusion MRI tractography and resting-state fMRI.

#### Access Portal
```
https://db.humanconnectome.org/
```

**Requirements:**
- Create free account
- Accept WU-Minn HCP Data Use Terms
- Obtain AWS credentials for bulk downloads

#### API Access

**ConnectomeDB REST API:**
```
Base URL: https://db.humanconnectome.org/
Documentation available after account creation
```

**DataLad (Programmatic Access):**
```bash
# Install DataLad
pip install datalad

# Clone HCP dataset
datalad clone https://github.com/datalad-datasets/human-connectome-project-openaccess

# Get specific files (uses AWS credentials)
datalad get HCP1200/100307/T1w/T1w_acpc_dc.nii.gz
```

#### Available Data Types

**Structural MRI:**
- T1-weighted (0.7mm isotropic)
- T2-weighted
- Cortical surface reconstructions
- Subcortical segmentations

**Diffusion MRI:**
- 3 shells (b=1000, 2000, 3000)
- 270 directions
- Tractography results
- Structural connectivity matrices

**Functional MRI:**
- Resting-state (4 runs × 15 min)
- Task-based (7 tasks)
- Functional connectivity matrices
- Parcellated time series

**Connectivity Matrices:**
- 785 subjects (clean data subset)
- Multiple parcellations available
- Region-average time series
- Structure-function relationships

#### Data Organization

**Subject Directory Structure:**
```
HCP1200/
├── 100307/
│   ├── T1w/
│   │   ├── T1w_acpc_dc.nii.gz
│   │   └── Diffusion/
│   ├── MNINonLinear/
│   │   └── Results/
│   └── analysis/
```

#### Connectivity Matrix Formats
- CSV (region × region)
- MAT (MATLAB)
- HDF5 (Python/PyTorch)
- ConnectomeWorkbench (.conn.nii)

#### Software Tools

**Connectome Workbench:**
```bash
# Command-line tools for visualization and analysis
wb_command -cifti-convert ...
wb_command -cifti-roi ...
```

**Python Access:**
```python
import neurohcp

# Configure AWS credentials
neurohcp.setup_credentials()

# Download data
subjects = neurohcp.get_subjects()
data = neurohcp.get_data(subject='100307', data_type='diffusion')
```

#### Key Network Structures

**Resting-State Networks:**
- Default Mode Network (DMN)
- Dorsal Attention Network (DAN)
- Ventral Attention Network (VAN)
- Frontoparietal Control Network
- Somatomotor Network
- Visual Network
- Auditory Network

**Structural Modules:**
- Association fiber tracts
- Projection pathways
- Commissural connections
- Thalamic connectivity profiles

### 3.4 Unified Brain Atlas Comparisons

| Atlas | Resolution | Areas | Species | Modality | Best For |
|-------|-----------|-------|---------|----------|----------|
| Glasser (HCP-MMP1.0) | 2mm | 360 | Human | Multi-modal | Functional organization |
| BigBrain | 20μm | Variable | Human | Histology | Cytoarchitecture |
| HCP Connectome | 2mm | Variable | Human | MRI | Connectivity |
| Allen Mouse | 10μm | 800+ | Mouse | Multi-modal | Gene expression |
| Julich-Brain | 1mm | 200+ | Human | Histology | Probabilistic maps |

---

## 4. Cell Ontology (CL)

### 4.1 Overview
The Cell Ontology is a standardized vocabulary of cell types across species, with 2,700+ cell type classes organized hierarchically. Critical for neuron type classification and cross-database integration.

### 4.2 API Access

#### Ontology Browsers

**NCBO BioPortal:**
```
Base URL: https://bioportal.bioontology.org/ontologies/CL
API: https://data.bioontology.org/documentation
```

**Ontology Lookup Service (OLS):**
```
Base URL: https://www.ebi.ac.uk/ols/ontologies/cl
API: https://www.ebi.ac.uk/ols/api/ontologies/cl
```

**Ontobee:**
```
Base URL: http://www.ontobee.org/ontology/CL
```

#### GitHub Repository
```
https://github.com/obophenotype/cell-ontology
Direct OBO/OWL downloads
```

### 4.3 Authentication & Access
- **No authentication required**
- Open access under CC BY 4.0
- SPARQL endpoints available for complex queries

### 4.4 Data Formats

**Available Formats:**
- **OWL** (RDF/XML) - Full ontology with logic
- **OBO** - Human-readable text format
- **JSON** (OBOGraphs) - Lightweight JSON representation
- **TTL** (Turtle/RDF)

**Download Links:**
```
OWL: http://purl.obolibrary.org/obo/cl.owl
OBO: http://purl.obolibrary.org/obo/cl.obo
JSON: http://purl.obolibrary.org/obo/cl.json
```

### 4.5 Key Entity Types

#### A. Neuron Classifications

**Primary Neuron Class:**
```
CL:0000540 - neuron
```

**Major Neuron Subclasses:**

**By Neurotransmitter (20+ types):**
```
CL:0000679 - glutamatergic neuron
CL:0000617 - GABAergic neuron
CL:0000700 - dopaminergic neuron
CL:0000850 - serotonergic neuron
CL:0000108 - cholinergic neuron
CL:0000117 - CNS neuron (sensu Vertebrata)
```

**By Morphology (50+ types):**
```
CL:0000598 - pyramidal neuron
CL:0000099 - interneuron
CL:0000210 - photoreceptor cell
CL:0000287 - bipolar neuron
CL:0000104 - multipolar neuron
CL:0000242 - Merkel cell
CL:0000573 - retinal cone cell
CL:0000604 - retinal rod cell
```

**By Location (100+ types):**
```
CL:0000119 - cerebellar Purkinje cell
CL:0000121 - Purkinje cell
CL:2000029 - central nervous system neuron
CL:0000540 - neuron
CL:0011103 - sympathetic neuron
CL:0011104 - parasympathetic neuron
CL:0000107 - autonomic neuron
```

**By Function (30+ types):**
```
CL:0000101 - sensory neuron
CL:0000100 - motor neuron
CL:0000199 - mechanoreceptor cell
CL:0000207 - olfactory receptor cell
```

**Cortical Neuron Specific (40+ types):**
```
CL:0000118 - basket cell
CL:0000120 - granule cell
CL:0000598 - pyramidal neuron
CL:4023041 - L2/3 intratelencephalic projecting glutamatergic neuron
CL:4023042 - L5 extratelencephalic projecting glutamatergic cortical neuron
```

#### B. Glial Cells (50+ types)
```
CL:0000125 - glial cell
CL:0000127 - astrocyte
CL:0000128 - oligodendrocyte
CL:0000129 - microglial cell
CL:0000710 - neurecto-epithelial cell
```

#### C. Hierarchical Relationships

**Relationship Types:**
- `is_a`: Subclass relationship
- `part_of`: Compositional relationship
- `develops_from`: Developmental lineage
- `has_part`: Component relationship
- `capable_of`: Functional capability

**Example Hierarchy:**
```
cell (CL:0000000)
└── native cell (CL:0000003)
    └── neuron (CL:0000540)
        ├── CNS neuron (CL:0000117)
        │   ├── cerebral cortex neuron (CL:0000119)
        │   │   ├── pyramidal neuron (CL:0000598)
        │   │   └── cortical interneuron (CL:0008031)
        │   │       ├── basket cell (CL:0000118)
        │   │       └── chandelier cell (CL:4023083)
        │   └── motor neuron (CL:0000100)
        └── sensory neuron (CL:0000101)
```

### 4.6 API Query Examples

#### BioPortal API

**Get Neuron Class:**
```bash
curl -H "Authorization: apikey YOUR_API_KEY" \
  "http://data.bioontology.org/ontologies/CL/classes/http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FCL_0000540"
```

**Search for Cell Types:**
```bash
curl -H "Authorization: apikey YOUR_API_KEY" \
  "http://data.bioontology.org/search?q=pyramidal+neuron&ontologies=CL"
```

**Get Class Hierarchy:**
```bash
curl -H "Authorization: apikey YOUR_API_KEY" \
  "http://data.bioontology.org/ontologies/CL/classes/http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FCL_0000540/tree"
```

#### OLS API

**Get Neuron Terms:**
```bash
curl "https://www.ebi.ac.uk/ols/api/ontologies/cl/terms?iri=http://purl.obolibrary.org/obo/CL_0000540"
```

**Search Cell Types:**
```bash
curl "https://www.ebi.ac.uk/ols/api/search?q=interneuron&ontology=cl"
```

**Get Children of Neuron:**
```bash
curl "https://www.ebi.ac.uk/ols/api/ontologies/cl/terms/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252FCL_0000540/children"
```

### 4.7 Advanced Tools

#### Ontology Access Kit (OAK)

```bash
pip install oaklib
```

```python
from oaklib import get_adapter

# Load Cell Ontology
cl = get_adapter("sqlite:obo:cl")

# Get all neuron types
neurons = cl.descendants("CL:0000540")  # neuron
print(f"Found {len(list(neurons))} neuron types")

# Get GABAergic neurons
gaba_neurons = cl.descendants("CL:0000617")
for neuron_id in gaba_neurons:
    label = cl.label(neuron_id)
    print(f"{neuron_id}: {label}")
```

#### OnClass (ML Classification)

OnClass uses Cell Ontology graph structure for automatic cell type classification from single-cell data.

```python
import OnClass

# Train classifier with ontology
model = OnClass.OnClassModel(cell_ontology_file='cl.obo')
model.train(expression_data, cell_type_labels)

# Predict cell types (including unseen types)
predictions = model.predict(new_expression_data)
```

### 4.8 Brain Data Standards Ontology (BDSO)

**Extension of CL for neuroscience:**
- Data-driven cell type ontology
- Integrated with Allen Institute cell types
- Marker gene definitions
- Transcriptomic cluster mappings

**Access:**
```
https://github.com/brain-bican/cell-type-ontology
```

### 4.9 Integration with Major Projects

**Projects Using CL:**
- CZ CELLxGENE (cell type annotations)
- Human Cell Atlas
- ENCODE
- BRAIN Initiative Cell Census Network (BICCN)
- Allen Brain Cell Atlas

### 4.10 Extraction Strategy for Neuron Types

**Target: 100-1000 neuron types**

1. **Core Categories (100 types):**
   - Query all direct descendants of CL:0000540 (neuron)
   - Filter for well-characterized types with marker genes

2. **Cortical Detail (200 types):**
   - Extract all cortical neuron subtypes
   - Include layer-specific variants
   - Add projection-defined types

3. **Extended Set (1000 types):**
   - Include regional specializations
   - Add electrophysiological variants
   - Include developmental stages

**Python Extraction Script:**
```python
from oaklib import get_adapter

cl = get_adapter("sqlite:obo:cl")

# Get all neuron descendants
all_neurons = list(cl.descendants("CL:0000540", predicates=["is_a"]))

neuron_data = []
for neuron_id in all_neurons:
    info = {
        'id': neuron_id,
        'label': cl.label(neuron_id),
        'definition': cl.definition(neuron_id),
        'synonyms': list(cl.entity_aliases(neuron_id)),
        'parents': list(cl.parents(neuron_id)),
    }
    neuron_data.append(info)

print(f"Extracted {len(neuron_data)} neuron types")
```

---

## 5. NeuroNames

### 5.1 Overview
NeuroNames is a comprehensive neuroanatomical nomenclature system covering ~3,000 CNS structures across human, macaque, rat, and mouse. Maintained by University of Washington.

### 5.2 Access Methods

#### Primary Portal
```
http://braininfo.org
http://braininfo.rprc.washington.edu/
```

#### Direct Downloads

**NeuroNames Ontology (JSON):**
```
http://braininfo.rprc.washington.edu/Nnont.aspx
Format: JSON
Content: ~3000 structures with nomenclature
```

### 5.3 Authentication & Access
- **No authentication required**
- Free download and use
- Available to hundreds of laboratories worldwide

### 5.4 Data Structure

#### Core Database Tables

**Three Main Tables:**
1. **Names** - Terms in multiple languages
2. **Concepts** - Neuroanatomical structures
3. **Models** - Species-specific implementations

**Coverage:**
- 16,000+ names
- 8 languages
- 2,500+ neuroanatomical concepts
- 4 species models (human, macaque, rat, mouse)

### 5.5 Key Features

#### Multi-lingual Support
- English (primary)
- Latin (classical nomenclature)
- French
- German
- Italian
- Spanish
- Russian
- Chinese

#### Nomenclature Systems Integrated
- Terminologia Anatomica (TA)
- Nomina Anatomica (NA)
- Terminologia Neuroanatomica (TNA)
- Classic neuroscience literature

#### Hierarchical Organization
- Parent-child relationships
- Part-whole hierarchies
- Topological relationships
- Functional groupings

### 5.6 Data Format (JSON)

**Structure Example:**
```json
{
  "id": "549",
  "name": "neocortex",
  "latin": "neocortex",
  "abbreviation": "Ncx",
  "definition": "The most recently evolved part of the cerebral cortex...",
  "synonyms": ["isocortex", "neopallium"],
  "parent_id": "453",
  "species": ["human", "macaque", "rat", "mouse"],
  "level": 5
}
```

### 5.7 Integration with Other Systems

**NeuroLex (NIFSTD):**
- NeuroNames is the basis for brain regions in NeuroLex
- Linked to NIFSTD ontology
- Semantic web integration

**UMLS Integration:**
- NeuroNames is a resource vocabulary in NLM's UMLS
- Concept mapping to medical terminologies
- Cross-reference to MeSH, SNOMED

**BrainInfo Portal:**
- Interactive navigation
- Hierarchical tree browser
- Cross-species comparisons
- Literature links

### 5.8 Key Entity Coverage

#### Major Brain Divisions (~50 structures)
```
- Telencephalon
- Diencephalon
- Mesencephalon
- Metencephalon
- Myelencephalon
```

#### Cortical Regions (~200 structures)
```
- Frontal lobe subdivisions
- Parietal lobe areas
- Temporal lobe regions
- Occipital cortex
- Insular cortex
- Cingulate cortex
- Hippocampal formation
```

#### Subcortical Structures (~150 structures)
```
- Basal ganglia components
- Thalamic nuclei
- Hypothalamic regions
- Amygdala subdivisions
- Brainstem nuclei
- Cerebellar structures
```

#### White Matter Tracts (~100 structures)
```
- Association fibers
- Projection pathways
- Commissural connections
- Cerebellar peduncles
```

#### Functional Systems (~50 groupings)
```
- Motor system components
- Sensory pathways
- Limbic system
- Reticular formation
- Autonomic centers
```

### 5.9 Extraction Strategy

**Python Parsing Example:**
```python
import json
import requests

# Download NeuroNames JSON
url = "http://braininfo.rprc.washington.edu/Nnont.aspx"
response = requests.get(url)
neuronames_data = response.json()

# Parse structures
brain_regions = []
for structure in neuronames_data:
    region = {
        'id': structure['id'],
        'name': structure['name'],
        'abbreviation': structure.get('abbreviation', ''),
        'definition': structure.get('definition', ''),
        'parent_id': structure.get('parent_id'),
        'level': structure.get('level'),
        'synonyms': structure.get('synonyms', [])
    }
    brain_regions.append(region)

print(f"Extracted {len(brain_regions)} brain regions")

# Build hierarchy
def build_hierarchy(regions, parent_id=None):
    hierarchy = []
    for region in regions:
        if region['parent_id'] == parent_id:
            children = build_hierarchy(regions, region['id'])
            if children:
                region['children'] = children
            hierarchy.append(region)
    return hierarchy

hierarchy = build_hierarchy(brain_regions)
```

### 5.10 Controlled Vocabulary Features

**Standard Terms:**
- Official nomenclature for indexing
- Canonical names for search queries
- Stable identifiers for database linking

**Operational Definitions:**
- All structures include definitions
- Boundary specifications
- Landmark descriptions

**Synonym Management:**
- Historical terms preserved
- Alternative nomenclatures listed
- Deprecated terms tracked

---

## 6. Canonical Circuit Motifs

### 6.1 Overview
Recurring patterns of neural connectivity that implement fundamental computational operations. These motifs appear across brain regions and species.

### 6.2 Key Circuit Motifs (<100 patterns)

#### A. Feedforward Motifs

**1. Feedforward Excitation (FFE)**
```
Structure: A → B → C (all excitatory)
Function: Signal amplification, temporal integration
Examples:
- Cortical layer 4 → layer 2/3 → layer 5
- Hippocampal trisynaptic circuit
- Thalamocortical projections
```

**2. Feedforward Inhibition (FFI)**
```
Structure:
  A → B (excitatory)
  A → I → B (via inhibitory interneuron)
Function: Temporal precision, gain control
Examples:
- Sensory cortex L4 → L2/3 with PV interneurons
- Cerebellar granule cell → Purkinje cell
- Hippocampal CA3 → CA1 with basket cells
```

**3. Cascade Motif**
```
Structure: A → B → C → D (unidirectional chain)
Function: Sequential processing, delay lines
Examples:
- Olfactory pathway (ORN → glomerulus → M/T → cortex)
- Retina → LGN → V1 → V2
```

#### B. Feedback Motifs

**4. Recurrent Excitation**
```
Structure: A ↔ B (bidirectional excitatory)
Function: Working memory, sustained activity, amplification
Examples:
- Cortical pyramidal cell networks
- Hippocampal CA3 recurrent collaterals
- PFC delay period activity
```

**5. Feedback Inhibition**
```
Structure: A → B → I → A
Function: Negative feedback, oscillations, gain control
Examples:
- Pyramidal → interneuron → pyramidal loops
- Thalamocortical oscillations
- Striatal medium spiny neurons
```

**6. Recurrent Inhibition**
```
Structure: I ↔ I (interneuron-interneuron)
Function: Disinhibition, gamma oscillations
Examples:
- PV-PV connections (fast synchronization)
- SST-VIP interactions
```

#### C. Lateral Motifs

**7. Lateral Inhibition**
```
Structure: A → I → B (neighbors)
Function: Contrast enhancement, winner-take-all
Examples:
- Retinal amacrine cells
- Cortical basket cells
- Olfactory bulb granule cells
```

**8. Lateral Excitation**
```
Structure: A → B (neighboring similar neurons)
Function: Feature linking, contour integration
Examples:
- Horizontal connections in V1
- Hippocampal place cell ensembles
- Auditory cortex frequency bands
```

#### D. Disinhibitory Motifs

**9. Canonical Disinhibitory Circuit**
```
Structure: VIP → SST → Pyramidal
         (interneuron → interneuron → principal cell)
Function: Flexible gating, attention, learning
Components:
- VIP interneurons (activated by top-down input)
- SST interneurons (target pyramidal dendrites)
- Pyramidal cells (disinhibited for processing)

Examples across brain regions:
- Visual cortex: attentional modulation
- Auditory cortex: sound discrimination
- Prefrontal cortex: working memory gating
- Hippocampus: memory encoding

Properties:
- Fast dynamics (<100ms)
- Pathway-specific control
- Enables supralinear integration
- Supports flexible information routing
```

**10. PV-SST Disinhibition**
```
Structure: PV → SST → Pyramidal dendrites
Function: Input-specific filtering
Examples:
- Sensory cortex: stimulus selectivity
- Motor cortex: movement preparation
```

#### E. Competition Motifs

**11. Winner-Take-All (WTA)**
```
Structure: Multiple units with mutual inhibition
Components:
- Recurrent excitation within units
- Strong lateral inhibition between units
- Optional threshold nonlinearity

Implementation motifs:
a) Direct mutual inhibition: A ↔ I ↔ B
b) Shared inhibitory pool: A → I ← B, I → {A,B}
c) Feedforward + feedback: Combined FFI + FBI

Function: Selection, decision-making, attention
Computational primitives:
1. Mutual inhibition (competition)
2. Self-excitation (commitment)
3. Threshold detection
4. Normalization
5. History dependence
6. Adaptive gain

Examples:
- Basal ganglia action selection
- Cortical attentional selection
- Hippocampal pattern separation
- Olfactory bulb odor discrimination
- Oculomotor system: saccade selection
- Prefrontal cortex: rule selection
```

**12. Normalization**
```
Structure: Input → E, Input → I, I → E (divisive)
Function: Gain control, invariance
Examples:
- V1 contrast normalization
- Grid cell normalization in MEC
- Multisensory integration in SC
```

#### F. Gating Motifs

**13. Thalamic Gate**
```
Structure: Cortex ↔ Thalamus ↔ TRN (thalamic reticular nucleus)
Function: Attention, sleep-wake, sensory filtering
Examples:
- Sensory thalamus → cortex
- Motor thalamus → M1
- Pulvinar → parietal cortex
```

**14. Striatal Gate**
```
Structure: Cortex → Striatum (direct/indirect pathways) → Thalamus
Function: Action selection, motor control
Examples:
- Direct pathway: Go signal
- Indirect pathway: No-go signal
- Hyperdirect pathway: Global pause
```

#### G. Oscillation-Generating Motifs

**15. Pacemaker Circuit**
```
Structure: Reciprocal excitation-inhibition
Function: Rhythmic activity generation
Examples:
- Thalamocortical oscillations (sleep spindles)
- Respiratory rhythm generator
- Locomotor CPGs
```

**16. Gamma Generator**
```
Structure: Pyramidal ↔ PV interneuron loop
Function: 40-80 Hz oscillations, binding
Examples:
- Hippocampal CA3 gamma
- Cortical gamma during attention
- Olfactory bulb gamma
```

**17. Theta Generator**
```
Structure: Medial septum → Hippocampus feedback
Function: 4-8 Hz oscillations, sequence coordination
Examples:
- Hippocampal theta during navigation
- Prefrontal theta during working memory
```

#### H. Integration Motifs

**18. Dendritic Subunit**
```
Structure: Multiple inputs → dendritic branch → soma
Function: Compartmentalized AND/OR operations
Examples:
- Pyramidal cell apical tuft
- Purkinje cell dendritic trees
- Retinal ganglion cell dendrites
```

**19. Coincidence Detector**
```
Structure: Multiple convergent inputs with tight timing
Function: AND operation, temporal binding
Examples:
- MSO neurons (sound localization)
- Hippocampal CA1 pyramidal cells
- Cortical layer 5 pyramidal neurons
```

**20. Integrator**
```
Structure: Recurrent excitation with long time constants
Function: Accumulation, decision variable
Examples:
- Oculomotor integrator
- LIP decision neurons
- Prefrontal working memory
```

#### I. Plasticity Motifs

**21. Spike-Timing-Dependent Plasticity (STDP) Circuit**
```
Structure: Feedforward with temporal correlation detection
Function: Causal learning, sequence learning
Examples:
- Cortical layer 2/3 connections
- Hippocampal CA3-CA1 synapses
```

**22. Heterosynaptic Plasticity**
```
Structure: Multiple pathways converging with neuromodulation
Function: Associative learning, credit assignment
Examples:
- Dopaminergic modulation in striatum
- Noradrenergic modulation in cortex
```

#### J. Specialized Motifs

**23. Central Pattern Generator (CPG)**
```
Structure: Half-center oscillator + coordination layer
Function: Rhythmic motor patterns
Examples:
- Locomotion circuits (spinal cord)
- Respiratory circuits (brainstem)
- Chewing circuits
```

**24. Efference Copy**
```
Structure: Motor command → copy → sensory comparison
Function: Prediction, sensory cancellation
Examples:
- Corollary discharge (eye movements)
- Cerebellum forward models
- Auditory feedback during speech
```

**25. Predictive Coding**
```
Structure: Hierarchical with error feedback
Components:
- Prediction units (feedforward)
- Error units (feedback)
- Update mechanism
Function: Efficient coding, learning
Examples:
- Visual cortical hierarchy
- Auditory cortex speech processing
```

### 6.3 Motif Properties Matrix

| Motif | Timescale | Computation | Key Neurons | Brain Regions |
|-------|-----------|-------------|-------------|---------------|
| FFI | 5-20ms | Temporal precision | PV interneurons | All cortex |
| Disinhibition | 50-200ms | Gating | VIP, SST | Association cortex |
| WTA | 100-500ms | Selection | Pyramidal + basket | PFC, BG, HC |
| Recurrent excitation | 100ms-10s | Memory | Pyramidal | PFC, HC |
| Gamma generator | 12-25ms (40Hz) | Binding | PV interneurons | HC, cortex |
| CPG | 100ms-2s | Rhythm | Multiple | Brainstem, spinal |

### 6.4 Data Sources for Circuit Motifs

**Literature Sources:**
1. **eLife articles:**
   - "Mechanisms of competitive selection" (2019)
   - "A disinhibitory circuit motif" (2018)
   - DOI: 10.7554/eLife.51473

2. **Review Papers:**
   - "Neural circuit motifs in valence processing" (PMC6590698)
   - "Canonical disinhibitory circuits" (Current Opinion Neurobiology)

3. **Databases:**
   - Allen Institute: Circuit tracing datasets
   - NeuroMorpho: Morphological connectivity patterns
   - ModelDB: Computational implementations

**Extraction Strategy:**
```python
# Systematic motif catalog
motif_catalog = {
    'feedforward': ['FFE', 'FFI', 'cascade'],
    'feedback': ['recurrent_exc', 'feedback_inh'],
    'lateral': ['lateral_inh', 'lateral_exc'],
    'disinhibitory': ['VIP-SST-Pyr', 'PV-SST-Pyr'],
    'competition': ['WTA', 'normalization'],
    'gating': ['thalamic', 'striatal'],
    'oscillation': ['pacemaker', 'gamma', 'theta'],
    'integration': ['dendritic', 'coincidence', 'integrator'],
    'plasticity': ['STDP', 'heterosynaptic'],
    'specialized': ['CPG', 'efference_copy', 'predictive_coding']
}

# ~25 main motifs + variants = ~100 total
```

### 6.5 Computational Implementations

**ModelDB Repository:**
```
https://modeldb.science/
Search: "circuit motif", "canonical circuit"
Formats: NEURON, Python, MATLAB
```

**Brian2 Examples:**
```python
from brian2 import *

# Example: Winner-Take-All Network
N = 10  # Number of competing units
tau = 10*ms
Vth = 1.0

# Neurons with self-excitation
neurons = NeuronGroup(N, '''
    dv/dt = (-v + I_ext + I_rec - I_inh)/tau : 1
    I_ext : 1
    I_rec : 1
    I_inh : 1
''', threshold='v > Vth', reset='v = 0')

# Recurrent excitation (within population)
exc_synapses = Synapses(neurons, neurons, 'w : 1', on_pre='I_rec_post += w')
exc_synapses.connect(condition='i == j')  # Self-connection
exc_synapses.w = 0.2

# Lateral inhibition (between populations)
inh_synapses = Synapses(neurons, neurons, 'w : 1', on_pre='I_inh_post += w')
inh_synapses.connect(condition='i != j')
inh_synapses.w = 0.1
```

---

## 7. Data Formats Reference

### 7.1 Neuroanatomical Data Formats

#### SWC (Neuron Morphology)
```
Format: ASCII text, 7 columns
Columns: ID, Type, X, Y, Z, Radius, Parent
Types: 0=undefined, 1=soma, 2=axon, 3=dendrite, 4=apical
Example:
1 1 0.0 0.0 0.0 5.0 -1
2 3 1.0 2.0 0.5 0.8 1
3 3 2.0 4.0 1.0 0.7 2

Tools: NeuroMorpho, NEURON, Allen SDK
```

#### NWB (Neurodata Without Borders)
```
Format: HDF5
Content: Electrophysiology, behavior, stimuli
Standard: Neuroscience community standard
Tools: PyNWB, MatNWB, Allen SDK
```

#### NRRD (Nearly Raw Raster Data)
```
Format: ASCII header + binary data
Content: Volumetric brain images, connectivity grids
Header: Key-value pairs defining dimensions, spacing, encoding
Tools: pynrrd, ITK-SNAP, 3D Slicer
```

### 7.2 Ontology Formats

#### OWL (Web Ontology Language)
```
Format: RDF/XML
Content: Full ontology with logical axioms
Use: Reasoning, SPARQL queries
Tools: Protégé, OWL API, rdflib
```

#### OBO (Open Biological Ontologies)
```
Format: Simple text format
Content: Terms, relationships, definitions
Syntax:
[Term]
id: CL:0000540
name: neuron
def: "An electrically active cell..."
is_a: CL:0000000 ! cell

Tools: OBO-Edit, Onto-Perl, OAK
```

#### JSON (OBOGraphs)
```
Format: JSON
Content: Lightweight ontology representation
Structure:
{
  "graphs": [{
    "nodes": [{"id": "CL:0000540", "lbl": "neuron"}],
    "edges": [{"sub": "CL:0000540", "pred": "is_a", "obj": "CL:0000000"}]
  }]
}

Tools: obographs, JavaScript libraries
```

### 7.3 Connectivity Formats

#### Connectivity Matrix (CSV/MAT)
```
Format: CSV, MATLAB .mat, HDF5
Structure: N×N matrix (regions × regions)
Values: Connection strength, probability, weight
Example:
       V1    V2    V4    MT
V1     0     0.8   0.3   0.5
V2     0.4   0     0.9   0.7
V4     0.2   0.6   0     0.4
MT     0.3   0.5   0.2   0
```

#### CIFTI (Connectivity Informatics Technology Initiative)
```
Format: HDF5-based
Content: Dense/parcellated connectomes
Standard: HCP Connectome Workbench
Extensions: .dconn.nii, .pconn.nii
Tools: Connectome Workbench, CIFTI-MATLAB
```

#### GraphML
```
Format: XML for graphs
Content: Network structure with metadata
Use: Complex network analysis
Tools: NetworkX, igraph, Cytoscape
```

### 7.4 Image Formats

#### NIfTI (Neuroimaging Informatics Technology Initiative)
```
Format: Binary with header
Extensions: .nii, .nii.gz
Content: 3D/4D brain images
Standard: MRI community standard
Tools: FSL, SPM, AFNI, nibabel
```

#### GIFTI (Geometry Format)
```
Format: XML + binary
Content: Surface meshes, surface data
Extensions: .surf.gii, .func.gii
Standard: HCP, FreeSurfer
Tools: Connectome Workbench, FreeSurfer
```

### 7.5 Allen Institute Specific

#### CCF (Common Coordinate Framework)
```
Format: NRRD volumes + annotation
Resolution: 10, 25, 50, 100 μm
Content: Template brain + region labels
Tools: Allen SDK, SimpleITK
```

#### Structure Unionizes (CSV)
```
Format: CSV
Content: Projection statistics by brain region
Columns:
- section_data_set_id
- structure_id
- hemisphere_id
- projection_density
- projection_energy
- projection_intensity
- volume
```

---

## 8. Extraction Strategy Summary

### 8.1 Brain Regions (Target: 200-300)

#### Priority 1: Allen Brain Atlas (150 regions)
```python
from allensdk.core.structure_tree import StructureTree
from allensdk.api.queries.ontologies_api import OntologiesApi

oapi = OntologiesApi()
structures = oapi.get_structures_with_sets([1])  # Mouse
tree = StructureTree.clean_structures(structures)

# Filter for major regions
priority_regions = []
for structure in tree.nodes():
    # Include if:
    # - Level 3-7 (exclude very broad and very specific)
    # - Has significant volume
    # - Well-documented
    if 3 <= structure['depth'] <= 7:
        priority_regions.append({
            'id': structure['id'],
            'name': structure['name'],
            'acronym': structure['acronym'],
            'parent': structure.get('parent_structure_id'),
            'level': structure['depth'],
            'color': structure.get('color_hex_triplet')
        })

# Target distribution:
# - Cortex: 60 regions
# - Subcortical: 40 regions
# - Brainstem: 30 regions
# - Cerebellum: 20 regions
```

#### Priority 2: Glasser Atlas (50 regions)
```
Download HCP-MMP1.0
Extract ROI labels and coordinates
Focus on functionally distinct areas:
- Primary sensory/motor: 15 areas
- Association cortex: 25 areas
- Multimodal hubs: 10 areas
```

#### Priority 3: NeuroNames (100 regions)
```
Download JSON from braininfo.org
Parse hierarchical structure
Cross-reference with Allen Atlas
Include human-specific regions not in mouse
```

### 8.2 Neuron Types (Target: 100-1000)

#### Tier 1: Core Types (100)
**Source: Cell Ontology + Allen ABC Atlas**

```python
from oaklib import get_adapter

cl = get_adapter("sqlite:obo:cl")

# Major categories
categories = {
    'excitatory': ['pyramidal', 'granule', 'spiny stellate'],
    'inhibitory': ['PV', 'SST', 'VIP', 'basket', 'chandelier', 'Martinotti'],
    'modulatory': ['dopaminergic', 'serotonergic', 'cholinergic'],
    'sensory': ['photoreceptor', 'hair cell', 'mechanoreceptor'],
    'motor': ['motor neuron', 'Purkinje cell']
}

core_types = []
for category, types in categories.items():
    for neuron_type in types:
        # Search CL
        results = cl.search(neuron_type)
        # Add regional variants
        # Example: "cortical pyramidal" vs "hippocampal pyramidal"
```

#### Tier 2: Regional Specialization (300)
**Source: Allen ABC Atlas taxonomy**

```
Download taxonomy from ABC Atlas
5,322 clusters → filter to 300 representative types
Selection criteria:
- Well-characterized marker genes
- Clear functional annotations
- Present in multiple datasets
- Cross-species correspondence
```

#### Tier 3: Extended Set (1000)
**Source: Multiple databases integration**

```
Combine:
- Allen ABC: 300 types (as above)
- NeuroMorpho: 300 morphological types
- CL: 200 functionally-defined types
- Literature: 200 specialized types

Deduplication and cross-mapping required
```

### 8.3 Circuit Motifs (Target: <100)

#### Core Motifs (25)
```
1. Feedforward excitation
2. Feedforward inhibition
3. Cascade
4. Recurrent excitation
5. Feedback inhibition
6. Recurrent inhibition
7. Lateral inhibition
8. Lateral excitation
9. Canonical disinhibition (VIP-SST-Pyr)
10. PV-SST disinhibition
11. Winner-take-all
12. Normalization
13. Thalamic gate
14. Striatal gate
15. Pacemaker
16. Gamma generator
17. Theta generator
18. Dendritic subunit
19. Coincidence detector
20. Integrator
21. STDP circuit
22. Heterosynaptic plasticity
23. Central pattern generator
24. Efference copy
25. Predictive coding
```

#### Extended Set (75)
```
Add variants and combinations:
- Regional specializations (cortex vs hippocampus vs cerebellum)
- Laminar variants (L2/3 vs L5 vs L6)
- Temporal variants (fast vs slow)
- Neuromodulated variants
- Developmental stages
- Species differences
```

**Data Sources:**
- Allen Connectivity Atlas: Anatomical connectivity
- ModelDB: Computational implementations
- Literature: eLife, Current Opinion Neurobiology
- Allen Cell Types: Morphological basis for motifs

### 8.4 Connectivity Matrices

#### Allen Mouse Connectivity
```python
from allensdk.core.mouse_connectivity_cache import MouseConnectivityCache

mcc = MouseConnectivityCache()

# Oh et al. 2014 matrix (213×213)
# Download structure unionizes
# Build custom connectivity matrix for selected regions

priority_structures = [
    'VISp', 'VISal', 'VISl', 'VISpl', 'VISpm',  # Visual
    'SSp', 'SSs',  # Somatosensory
    'MOp', 'MOs',  # Motor
    'AUDp', 'AUDpo', 'AUDv',  # Auditory
    'HIP', 'CA1', 'CA3', 'DG',  # Hippocampus
    'TH', 'VPM', 'VPL', 'LGd',  # Thalamus
    'STR', 'CP', 'ACB',  # Striatum
]

# Extract submatrix for these regions
```

#### HCP Connectome
```
Access via db.humanconnectome.org
Download structural connectivity (DTI)
Download functional connectivity (rsfMRI)
Target: 100-400 region parcellation (Glasser or similar)
Format: CSV matrices
```

### 8.5 Network Modules

#### Functional Networks
```
From HCP and literature:
1. Default Mode Network (DMN)
2. Executive Control Network
3. Salience Network
4. Sensorimotor Network
5. Visual Network
6. Auditory Network
7. Dorsal Attention Network
8. Ventral Attention Network
9. Language Network
10. Spatial Navigation Network
```

#### Anatomical Circuits
```
From Allen + literature:
1. Hippocampal formation pathways
2. Basal ganglia loops (motor, cognitive, limbic)
3. Thalamocortical circuits
4. Cortico-striatal-thalamic loops
5. Cerebellar circuits
6. Limbic system
7. Reward circuitry
8. Fear circuitry
```

### 8.6 Implementation Timeline

**Phase 1: Core Structures (Week 1)**
- Allen structure ontology → 150 regions
- Cell Ontology → 100 neuron types
- Literature → 25 core motifs

**Phase 2: Extended Data (Week 2)**
- Glasser + NeuroNames → +100 regions
- Allen ABC Atlas → +300 neuron types
- ModelDB → +25 motif variants

**Phase 3: Connectivity (Week 3)**
- Allen connectivity matrix
- HCP connectivity data
- Network module definitions

**Phase 4: Integration (Week 4)**
- Cross-reference all databases
- Build unified schema
- Validate consistency
- Create extraction tools

### 8.7 Database Schema Design

#### Recommended Structure
```sql
-- Brain Regions
CREATE TABLE brain_regions (
    id VARCHAR PRIMARY KEY,
    name VARCHAR NOT NULL,
    acronym VARCHAR,
    ontology_source VARCHAR,  -- 'Allen', 'NeuroNames', 'Glasser'
    parent_id VARCHAR REFERENCES brain_regions(id),
    level INTEGER,
    functional_system VARCHAR,
    definition TEXT
);

-- Neuron Types
CREATE TABLE neuron_types (
    id VARCHAR PRIMARY KEY,
    name VARCHAR NOT NULL,
    ontology_source VARCHAR,  -- 'CL', 'Allen', 'Custom'
    neurotransmitter VARCHAR,
    morphology_class VARCHAR,
    electrophysiology VARCHAR,
    marker_genes TEXT[],
    parent_type_id VARCHAR REFERENCES neuron_types(id)
);

-- Circuit Motifs
CREATE TABLE circuit_motifs (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    category VARCHAR,  -- 'feedforward', 'feedback', 'lateral', etc.
    components JSONB,  -- {neurons: [...], connections: [...]}
    computation VARCHAR,
    timescale_ms INTEGER,
    brain_regions VARCHAR[],
    references TEXT[]
);

-- Connectivity
CREATE TABLE connectivity (
    source_region_id VARCHAR REFERENCES brain_regions(id),
    target_region_id VARCHAR REFERENCES brain_regions(id),
    connection_strength FLOAT,
    connection_type VARCHAR,
    species VARCHAR,
    data_source VARCHAR,
    PRIMARY KEY (source_region_id, target_region_id)
);

-- Network Modules
CREATE TABLE network_modules (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    module_type VARCHAR,  -- 'functional', 'anatomical'
    regions VARCHAR[] REFERENCES brain_regions(id),
    function TEXT
);
```

### 8.8 Validation Checklist

**Brain Regions:**
- [ ] 200-300 regions extracted
- [ ] Hierarchical relationships preserved
- [ ] Cross-database mapping completed
- [ ] Functional annotations added
- [ ] Spatial coordinates available

**Neuron Types:**
- [ ] 100-1000 types extracted
- [ ] Multiple classification axes covered
- [ ] Marker genes documented
- [ ] Cross-species mappings
- [ ] Morphological data linked

**Circuit Motifs:**
- [ ] <100 motifs cataloged
- [ ] Computational functions defined
- [ ] Component neuron types specified
- [ ] Example implementations available
- [ ] Brain region distributions mapped

**Connectivity:**
- [ ] Connectivity matrices obtained
- [ ] Multiple species/scales covered
- [ ] Structural and functional data
- [ ] Network analysis metrics computed

---

## 9. API Access Code Templates

### 9.1 Complete Extraction Pipeline

```python
"""
Neuroscience Database Extraction Pipeline
Extracts brain regions, neuron types, circuit motifs, and connectivity
"""

import json
import requests
from allensdk.api.queries.ontologies_api import OntologiesApi
from allensdk.core.structure_tree import StructureTree
from allensdk.core.mouse_connectivity_cache import MouseConnectivityCache
from oaklib import get_adapter
import pandas as pd

class NeuroDataExtractor:
    def __init__(self, output_dir='neuroscience_data'):
        self.output_dir = output_dir
        self.data = {
            'brain_regions': [],
            'neuron_types': [],
            'circuit_motifs': [],
            'connectivity': []
        }

    def extract_allen_brain_regions(self, max_regions=150):
        """Extract brain regions from Allen Brain Atlas"""
        print("Extracting Allen Brain Atlas regions...")

        oapi = OntologiesApi()
        structures = oapi.get_structures_with_sets([1])  # Mouse Brain
        tree = StructureTree.clean_structures(structures)

        for structure in tree.nodes():
            if 3 <= structure.get('depth', 0) <= 7:  # Optimal level
                region = {
                    'id': f"ABA:{structure['id']}",
                    'name': structure['name'],
                    'acronym': structure.get('acronym', ''),
                    'source': 'Allen Brain Atlas',
                    'parent_id': f"ABA:{structure.get('parent_structure_id')}" if structure.get('parent_structure_id') else None,
                    'level': structure.get('depth'),
                    'color': structure.get('color_hex_triplet'),
                    'atlas_id': structure.get('atlas_id'),
                    'ontology_id': structure.get('ontology_id')
                }
                self.data['brain_regions'].append(region)

        print(f"Extracted {len(self.data['brain_regions'])} brain regions")
        return self.data['brain_regions'][:max_regions]

    def extract_neuron_types_from_cl(self, max_types=100):
        """Extract neuron types from Cell Ontology"""
        print("Extracting neuron types from Cell Ontology...")

        cl = get_adapter("sqlite:obo:cl")

        # Get all neuron descendants
        neuron_descendants = list(cl.descendants("CL:0000540", predicates=["is_a"]))

        for neuron_id in neuron_descendants[:max_types]:
            neuron_type = {
                'id': neuron_id,
                'name': cl.label(neuron_id),
                'source': 'Cell Ontology',
                'definition': cl.definition(neuron_id),
                'synonyms': list(cl.entity_aliases(neuron_id)),
                'parent_ids': [str(p) for p in cl.parents(neuron_id)]
            }
            self.data['neuron_types'].append(neuron_type)

        print(f"Extracted {len(self.data['neuron_types'])} neuron types")
        return self.data['neuron_types']

    def extract_canonical_motifs(self):
        """Define canonical circuit motifs"""
        print("Cataloging canonical circuit motifs...")

        motifs = [
            {
                'id': 'motif_001',
                'name': 'Feedforward Inhibition',
                'category': 'feedforward',
                'components': {
                    'neurons': ['excitatory input', 'inhibitory interneuron', 'target neuron'],
                    'connections': [
                        {'from': 'input', 'to': 'target', 'type': 'excitatory'},
                        {'from': 'input', 'to': 'interneuron', 'type': 'excitatory'},
                        {'from': 'interneuron', 'to': 'target', 'type': 'inhibitory'}
                    ]
                },
                'computation': 'Temporal precision, gain control',
                'timescale_ms': 10,
                'examples': ['Cortical L4→L2/3', 'Hippocampal CA3→CA1']
            },
            {
                'id': 'motif_002',
                'name': 'Canonical Disinhibition',
                'category': 'disinhibitory',
                'components': {
                    'neurons': ['VIP interneuron', 'SST interneuron', 'Pyramidal cell'],
                    'connections': [
                        {'from': 'VIP', 'to': 'SST', 'type': 'inhibitory'},
                        {'from': 'SST', 'to': 'Pyramidal', 'type': 'inhibitory'},
                        {'from': 'input', 'to': 'Pyramidal', 'type': 'excitatory'}
                    ]
                },
                'computation': 'Flexible gating, attentional modulation',
                'timescale_ms': 100,
                'examples': ['Visual cortex attention', 'PFC working memory']
            },
            {
                'id': 'motif_003',
                'name': 'Winner-Take-All',
                'category': 'competition',
                'components': {
                    'neurons': ['Multiple excitatory units', 'Shared inhibitory pool'],
                    'connections': [
                        {'from': 'unit', 'to': 'self', 'type': 'recurrent_excitatory'},
                        {'from': 'unit', 'to': 'inhibitory_pool', 'type': 'excitatory'},
                        {'from': 'inhibitory_pool', 'to': 'all_units', 'type': 'inhibitory'}
                    ]
                },
                'computation': 'Selection, decision-making',
                'timescale_ms': 200,
                'examples': ['Basal ganglia', 'Cortical attention', 'Olfactory bulb']
            },
            # Add more motifs...
        ]

        self.data['circuit_motifs'] = motifs
        print(f"Cataloged {len(motifs)} circuit motifs")
        return motifs

    def extract_connectivity_matrix(self, regions_subset=None):
        """Extract connectivity matrix from Allen Mouse Connectivity"""
        print("Extracting connectivity matrix...")

        mcc = MouseConnectivityCache(manifest_file='connectivity/manifest.json')

        # Get structure tree
        structure_tree = mcc.get_structure_tree()

        # Define regions of interest
        if regions_subset is None:
            regions_subset = [
                'VISp', 'SSp', 'MOp', 'AUDp',  # Primary sensory/motor
                'HIP', 'CA1', 'CA3', 'DG',  # Hippocampus
                'TH', 'STR', 'CB'  # Subcortical
            ]

        # Get experiments
        experiments = mcc.get_experiments(dataframe=True)

        # Build connectivity matrix
        connectivity = []
        for source_region in regions_subset:
            source_struct = structure_tree.get_structures_by_acronym([source_region])
            if not source_struct:
                continue
            source_id = source_struct[0]['id']

            # Get projections from this region
            region_experiments = experiments[
                experiments['structure_id'] == source_id
            ]

            for _, exp in region_experiments.head(5).iterrows():  # Limit for demo
                unionizes = mcc.get_structure_unionizes([exp['id']])
                for _, row in unionizes.iterrows():
                    target_struct = structure_tree.get_structures_by_id([row['structure_id']])
                    if target_struct:
                        connectivity.append({
                            'source': source_region,
                            'target': target_struct[0].get('acronym', 'Unknown'),
                            'strength': row['projection_density'],
                            'volume': row['volume'],
                            'experiment_id': exp['id']
                        })

        self.data['connectivity'] = connectivity
        print(f"Extracted {len(connectivity)} connectivity measurements")
        return connectivity

    def save_all(self):
        """Save all extracted data"""
        print("Saving data...")

        with open(f'{self.output_dir}/brain_regions.json', 'w') as f:
            json.dump(self.data['brain_regions'], f, indent=2)

        with open(f'{self.output_dir}/neuron_types.json', 'w') as f:
            json.dump(self.data['neuron_types'], f, indent=2)

        with open(f'{self.output_dir}/circuit_motifs.json', 'w') as f:
            json.dump(self.data['circuit_motifs'], f, indent=2)

        pd.DataFrame(self.data['connectivity']).to_csv(
            f'{self.output_dir}/connectivity.csv', index=False
        )

        print(f"Data saved to {self.output_dir}/")

    def generate_report(self):
        """Generate extraction report"""
        report = {
            'brain_regions_count': len(self.data['brain_regions']),
            'neuron_types_count': len(self.data['neuron_types']),
            'circuit_motifs_count': len(self.data['circuit_motifs']),
            'connectivity_measurements': len(self.data['connectivity']),
            'sources': ['Allen Brain Atlas', 'Cell Ontology', 'Literature', 'Allen Connectivity']
        }

        print("\n=== Extraction Report ===")
        for key, value in report.items():
            print(f"{key}: {value}")

        return report

# Usage
if __name__ == '__main__':
    extractor = NeuroDataExtractor()

    # Extract all data types
    extractor.extract_allen_brain_regions(max_regions=200)
    extractor.extract_neuron_types_from_cl(max_types=100)
    extractor.extract_canonical_motifs()
    extractor.extract_connectivity_matrix()

    # Save and report
    extractor.save_all()
    extractor.generate_report()
```

### 9.2 Quick Reference Commands

```bash
# Allen Brain Atlas - Download structure ontology
curl "http://api.brain-map.org/api/v2/structure_graph_download/1.json" > mouse_brain_structures.json

# NeuroMorpho - Get neuron list
curl "http://neuromorpho.org/api/neuron/select?q=species:mouse&size=100" > neurons.json

# Cell Ontology - Download
wget http://purl.obolibrary.org/obo/cl.json

# NeuroNames - Download
wget http://braininfo.rprc.washington.edu/Nnont.aspx -O neuronames.json

# HCP Glasser Atlas - From Figshare
# Visit: https://figshare.com/articles/dataset/2016_Glasser_MMP1_0_Cortical_Atlases/24431146

# BigBrain - Access via EBRAINS
# Portal: https://ebrains.eu/tools/human-brain-atlas
```

---

## 10. References and Documentation

### Primary API Documentation
1. **Allen Brain Atlas API**: http://help.brain-map.org/display/api
2. **NeuroMorpho API**: https://neuromorpho.org/apiReference.html
3. **Cell Ontology**: https://cell-ontology.github.io/
4. **HCP Data Access**: https://db.humanconnectome.org/
5. **EBRAINS siibra-api**: https://siibra-api-stable.apps.tc.humanbrainproject.eu/

### Key Publications
1. Glasser MF et al. (2016) Nature - Multi-modal parcellation
2. Amunts K et al. (2013) Science - BigBrain atlas
3. Oh SW et al. (2014) Nature - Allen Mouse Connectivity
4. Diehl AD et al. (2016) J Biomed Semantics - Cell Ontology
5. Bowden DM & Martin RF (1995) NeuroImage - NeuroNames

### Software Tools
1. **Allen SDK**: https://alleninstitute.github.io/AllenSDK/
2. **siibra-python**: https://github.com/FZJ-INM1-BDA/siibra-python
3. **Ontology Access Kit (OAK)**: https://github.com/INCATools/ontology-access-kit
4. **neuromorphopy**: https://pypi.org/project/neuromorphopy/
5. **Connectome Workbench**: https://www.humanconnectome.org/software/connectome-workbench

---

**Document Status:** Comprehensive v1.0
**Target Achievement:**
- ✓ Brain Regions: 200-300 (achievable)
- ✓ Neuron Types: 100-1000 (achievable)
- ✓ Circuit Motifs: <100 (cataloged 25 core + variants)
- ✓ Connectivity: Multiple matrices available
- ✓ Network Modules: Functional and anatomical defined

**Next Steps:** Run extraction pipeline, validate data, integrate into BioFormulas database.
