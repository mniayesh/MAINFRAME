# Metabolic Database API Access Guide
## Extracting Principles and Patterns from Metabolic Databases

**Focus**: This guide prioritizes extracting PRINCIPLES, PATTERNS, and REGULATORY MECHANISMS over exhaustive molecule lists.

---

## Table of Contents
1. [HMDB - Human Metabolome Database](#1-hmdb---human-metabolome-database)
2. [ChEBI - Chemical Entities of Biological Interest](#2-chebi---chemical-entities-of-biological-interest)
3. [KEGG - Kyoto Encyclopedia of Genes and Genomes](#3-kegg---kyoto-encyclopedia-of-genes-and-genomes)
4. [Reactome - Pathway Database](#4-reactome---pathway-database)
5. [MetaCyc - Metabolic Pathways Database](#5-metacyc---metabolic-pathways-database)
6. [eQuilibrator - Thermodynamics Database](#6-equilibrator---thermodynamics-database)
7. [Pattern Extraction Strategies](#pattern-extraction-strategies)

---

## 1. HMDB - Human Metabolome Database
**Scale**: ~220,000+ metabolites

### API Access
- **Primary Endpoint**: Contact-based access (NOT publicly documented)
- **Web Interface**: https://hmdb.ca/
- **Downloads Page**: https://hmdb.ca/downloads

### Authentication & Access
- **API Access**: Requires direct contact with HMDB team
  - Academic/Research: eponine@ualberta.ca or samackay@ualberta.ca
  - Commercial: samackay@ualberta.ca
- **Web Access**: Free, no authentication required
- **Rate Limits**: Not publicly documented (API access only)

### Data Formats
- **XML**: `hmdb_metabolites.xml` (complete database dump)
- **SDF**: Chemical structures for all compounds
- **JSON**: Metabolite data
- **CSV/TXT**: Tabular data exports
- **SMILES, InChI, InChIKey**: Chemical structure formats

### Key Entity Types

#### Metabolites
- Chemical structures (SMILES, InChI, SDF, MOL, PDB)
- Biological roles and functions
- Pathway memberships
- Concentration ranges in biological fluids
- Disease associations

#### Pathways
- Metabolite pathway memberships
- Pathway maps (limited compared to KEGG/Reactome)
- Metabolite relationships within pathways

#### Data NOT Available
- ❌ Detailed reaction stoichiometry
- ❌ Thermodynamic parameters (ΔG, equilibrium constants)
- ❌ Flux constraints
- ❌ Explicit feedback loop annotations
- ❌ Rate-limiting step annotations

### Download Strategy (Avoiding 220k Individual Queries)

```bash
# Download complete XML database dump
wget https://hmdb.ca/system/downloads/current/hmdb_metabolites.zip

# Download structure files
wget https://hmdb.ca/system/downloads/current/structures.zip

# Parse XML for pathway-level patterns
# Focus on pathway membership, not individual metabolites
```

### Pattern Extraction Strategy

**1. Pathway-Centric Analysis**
```python
# Pseudocode for extracting pathway patterns
import xml.etree.ElementTree as ET

def extract_pathway_patterns(hmdb_xml):
    pathways = {}

    for metabolite in parse_xml(hmdb_xml):
        for pathway in metabolite.pathways:
            if pathway not in pathways:
                pathways[pathway] = {
                    'metabolites': [],
                    'roles': set(),
                    'diseases': set()
                }
            pathways[pathway]['metabolites'].append(metabolite.id)
            pathways[pathway]['roles'].add(metabolite.role)
            pathways[pathway]['diseases'].update(metabolite.diseases)

    return pathways
```

**2. Focus Areas for HMDB**
- Metabolite concentration ranges (homeostatic set points)
- Disease-metabolite associations (dysregulation patterns)
- Metabolite pathway memberships (network topology)
- Biological roles (functional classification)

**3. HMDB's Strengths**
- ✅ Comprehensive metabolite catalog
- ✅ Disease associations
- ✅ Concentration data (biofluid levels)
- ✅ Chemical structure data

**4. HMDB's Limitations**
- ⚠️ Limited mechanistic detail
- ⚠️ No thermodynamics
- ⚠️ No flux data
- ⚠️ Basic pathway information

---

## 2. ChEBI - Chemical Entities of Biological Interest
**Scale**: ~50,000+ biologically relevant small molecules

### API Access
- **Primary REST API**: https://www.ebi.ac.uk/chebi/backend/api/docs/
- **SOAP Web Services**: http://www.ebi.ac.uk/webservices/chebi/2.0/webservice?wsdl
- **libChEBI API**: Python/Java/MATLAB libraries (https://github.com/libChEBI)
- **SPARQL Endpoint**: http://chebi.bio2rdf.org/sparql
- **Ontology Lookup Service**: https://www.ebi.ac.uk/ols4/ontologies/chebi

### Authentication & Rate Limits
- **Authentication**: None required (free public access)
- **Rate Limits**: Not explicitly documented, but reasonable use expected
- **License**: Open, free for all users

### Data Formats
- **JSON**: REST API responses
- **XML**: SOAP responses, downloadable dumps
- **RDF/OWL**: Ontology format, SPARQL queries
- **SDF/MOL**: Chemical structures
- **Flat Files**: Monthly downloads from ftp://ftp.ebi.ac.uk/pub/databases/chebi/

### Key Entity Types

#### Chemical Entities
- Chemical structures and formulas
- Synonyms and names
- Database cross-references (KEGG, HMDB, PubChem, etc.)
- Ontology classifications

#### Biological Roles Ontology
- **Metabolic role classification**
  - Cofactor, coenzyme
  - Substrate, product
  - Inhibitor, activator
  - Metabolite types (primary, secondary)
  - Signaling molecules

#### Ontology Hierarchy
- Parent-child relationships
- "has role" relationships
- "is a" classifications
- Chemical structure relationships

### API Examples

#### SOAP Web Services (Most Comprehensive)

```python
# Using Python's zeep library for SOAP
from zeep import Client

wsdl = 'http://www.ebi.ac.uk/webservices/chebi/2.0/webservice?wsdl'
client = Client(wsdl=wsdl)

# Get complete entity with all relationships
entity = client.service.getCompleteEntity('CHEBI:15422')  # ATP

# Get ontology parents (includes role classifications)
parents = client.service.getOntologyParents('CHEBI:15422')

# Get all children with specific role
# Relationship types: "has role", "is a", "is conjugate base of", etc.
children = client.service.getAllOntologyChildrenInPath(
    chebiId='CHEBI:24432',  # biological role
    relationshipType='has role',
    onlyWithChemicalStructure=False
)

# Get entities by biological role
# Example: Find all cofactors
cofactors = client.service.getAllOntologyChildrenInPath(
    chebiId='CHEBI:23357',  # cofactor
    relationshipType='is a',
    onlyWithChemicalStructure=True
)
```

#### libChEBI (Python) - File-Based Access

```python
# Install: pip install libChEBIpy
from libchebipy import ChebiEntity

# Get entity and traverse ontology
entity = ChebiEntity('CHEBI:15422')  # ATP

print(f"Name: {entity.get_name()}")
print(f"Formula: {entity.get_formula()}")
print(f"SMILES: {entity.get_smiles()}")

# Get biological roles
for relation in entity.get_outgoings():
    if relation.get_type() == 'has role':
        role = relation.get_target_chebi_id()
        print(f"Role: {ChebiEntity(role).get_name()}")

# Get parent/child relationships
parents = entity.get_parents()
children = entity.get_children()
```

#### REST API (ChEBI 2.0)

```bash
# Base URL: https://www.ebi.ac.uk/chebi/backend/api/

# Search for entity
curl -X GET "https://www.ebi.ac.uk/chebi/backend/api/search/ATP"

# Get entity by ID
curl -X GET "https://www.ebi.ac.uk/chebi/backend/api/entity/CHEBI:15422"
```

### Pattern Extraction Strategy

**1. Role-Based Pattern Mining**
```python
def extract_metabolic_roles(chebi_id='CHEBI:24432'):  # biological role
    """
    Extract all metabolic roles and their members
    Instead of getting all 50k molecules, focus on role hierarchy
    """
    client = Client(wsdl)

    # Get all role types
    role_hierarchy = {}
    roles = client.service.getAllOntologyChildrenInPath(
        chebiId=chebi_id,
        relationshipType='is a',
        onlyWithChemicalStructure=False
    )

    for role in roles:
        # For each role, get representative members (sample, not all)
        members = client.service.getAllOntologyChildrenInPath(
            chebiId=role.chebiId,
            relationshipType='has role',
            onlyWithChemicalStructure=True
        )

        role_hierarchy[role.chebiName] = {
            'role_id': role.chebiId,
            'member_count': len(members),
            'sample_members': members[:10]  # Sample only
        }

    return role_hierarchy
```

**2. Cofactor and Coenzyme Networks**
```python
# ChEBI IDs for key metabolic role categories
METABOLIC_ROLES = {
    'cofactor': 'CHEBI:23357',
    'coenzyme': 'CHEBI:23354',
    'enzyme inhibitor': 'CHEBI:23924',
    'enzyme activator': 'CHEBI:23834',
    'substrate': 'CHEBI:78675',
    'metabolite': 'CHEBI:25212',
    'signaling molecule': 'CHEBI:62488',
}

def get_functional_categories():
    """Get functional groupings, not individual molecules"""
    functional_map = {}

    for role_name, role_id in METABOLIC_ROLES.items():
        entities = get_entities_with_role(role_id)

        # Group by chemical class, not individual molecules
        functional_map[role_name] = {
            'count': len(entities),
            'chemical_classes': group_by_parent_class(entities),
            'cross_pathway_roles': find_multi_pathway_roles(entities)
        }

    return functional_map
```

**3. ChEBI's Strengths for Pattern Extraction**
- ✅ Hierarchical role classification (avoids exhaustive enumeration)
- ✅ Biological function ontology
- ✅ Chemical class relationships
- ✅ Cross-database linking (KEGG, HMDB, etc.)

**4. Focus on Principles, Not Lists**
- Query by **role hierarchy** (cofactors, inhibitors, activators)
- Extract **functional classes** (energy carriers, signaling molecules)
- Map **cross-pathway metabolites** (metabolites appearing in multiple pathways)
- Identify **regulatory molecules** (allosteric regulators, feedback inhibitors)

---

## 3. KEGG - Kyoto Encyclopedia of Genes and Genomes
**Scale**: 18,000+ compounds, 12,000+ reactions, 500+ pathways

### API Access
- **Primary Endpoint**: https://rest.kegg.jp/
- **API Documentation**: https://www.kegg.jp/kegg/rest/keggapi.html
- **Web Interface**: https://www.kegg.jp/

### Authentication & Rate Limits
- **Authentication**: None required for academic use (honor system)
- **Rate Limits**: **Maximum 3 requests per second** (strictly enforced)
  - Exceeding this limit results in IP blocking
- **License**:
  - Academic: Free at https://rest.kegg.jp/
  - Commercial: Requires paid subscription at https://kegg.net/

### Data Formats
- **Flat Text**: Default response format (parseable)
- **JSON**: Available for some endpoints
- **KGML (XML)**: Pathway maps with graphical and semantic information
- **MOL**: Chemical structures
- **Image**: PNG pathway diagrams

### Key Entity Types

#### Compounds (C-numbers)
- Chemical structures
- Molecular formulas
- Exact mass
- Pathway memberships
- Reaction participation

#### Reactions (R-numbers)
- **Stoichiometric equations**
- Reversibility annotations
- Enzyme associations (EC numbers)
- RClass (reaction class) - structural transformation patterns
- Pathway memberships

#### Pathways
- **Metabolic pathway maps**
- Pathway topology (graph structure)
- Reaction sequences
- Regulatory annotations (limited)
- Module definitions (functional units)

#### Modules (M-numbers)
- **Functional units** of metabolic pathways
- Molecular complexes
- **Pathway modules** (multi-step reaction sequences)
- Enzyme modules
- **Essential for extracting principles!**

#### Reaction Classes (RCLASS)
- **Chemical transformation patterns**
- Substrate-product pair classifications
- RDM (Reaction Direction Match) patterns
- **Key for understanding reaction mechanisms**

### API Examples

#### Basic Operations

```bash
# Get compound information
curl "https://rest.kegg.jp/get/cpd:C00002"  # ATP

# Get reaction equation with stoichiometry
curl "https://rest.kegg.jp/get/rn:R00086"

# Get pathway map
curl "https://rest.kegg.jp/get/path:map00010"  # Glycolysis

# Get module (functional unit)
curl "https://rest.kegg.jp/get/md:M00001"  # Glycolysis core module

# Find pathways containing a compound
curl "https://rest.kegg.jp/link/pathway/cpd:C00002"  # All pathways with ATP

# Find reactions in a pathway
curl "https://rest.kegg.jp/link/reaction/path:map00010"

# Get KGML (pathway topology XML)
curl "https://rest.kegg.jp/get/hsa00010/kgml"
```

#### Pattern-Focused Queries

```bash
# List ALL pathways (to get overview, not details)
curl "https://rest.kegg.jp/list/pathway"

# List ALL modules (functional units - THIS IS KEY!)
curl "https://rest.kegg.jp/list/module"

# Get module definition (shows reaction logic)
curl "https://rest.kegg.jp/get/md:M00001"
# Returns: logical expression of enzymes/reactions
# Example: (K00844,K12407,K00845,K00886,K08074,K00918) (K01810,K06859,K13810,K15916)

# Find all RCLASSes (reaction patterns, not individual reactions)
curl "https://rest.kegg.jp/list/rclass"

# Get reaction class definition
curl "https://rest.kegg.jp/get/rc:RC00001"
```

#### Advanced Pattern Mining

```python
import requests
import time

BASE_URL = "https://rest.kegg.jp"
RATE_LIMIT = 0.34  # Seconds between requests (3 per second max)

def kegg_get(endpoint):
    """Rate-limited KEGG API call"""
    time.sleep(RATE_LIMIT)
    response = requests.get(f"{BASE_URL}/{endpoint}")
    return response.text

# 1. Get all pathway modules (functional units)
modules = kegg_get("list/module")
pathway_modules = [m for m in modules.split('\n') if 'M000' in m]

# 2. Extract module composition (multi-step processes)
module_definitions = {}
for module_line in pathway_modules[:50]:  # Sample, not all
    module_id = module_line.split('\t')[0]
    module_def = kegg_get(f"get/{module_id}")

    # Parse module definition for:
    # - Reaction steps
    # - Essential enzymes
    # - Alternative routes
    module_definitions[module_id] = parse_module(module_def)

# 3. Get pathway topology (graph structure)
pathway_kgml = kegg_get("get/hsa00010/kgml")  # Glycolysis
topology = parse_kgml_topology(pathway_kgml)

# 4. Extract reaction stoichiometry
reaction_data = kegg_get("get/rn:R00086")
stoichiometry = parse_reaction_equation(reaction_data)
```

### Extracting Principles from KEGG

#### 1. Pathway Modules (Not Individual Reactions)

```python
def extract_pathway_principles():
    """
    Focus on MODULES, not all 12,000 reactions
    Modules = multi-step functional units
    """

    # Module types to focus on:
    module_categories = {
        'pathway_modules': 'M00001-M00999',     # Core metabolic pathways
        'structural_complexes': 'M01000-M01999', # Protein complexes
        'functional_sets': 'M02000-M02999',      # Functional gene sets
        'signature_modules': 'M03000-M03999'     # Pathway signatures
    }

    # Extract principles:
    principles = {}

    for category, range_pattern in module_categories.items():
        modules_in_category = get_modules_by_range(range_pattern)

        principles[category] = {
            'core_modules': identify_core_modules(modules_in_category),
            'alternative_routes': find_alternative_pathways(modules_in_category),
            'essential_steps': extract_essential_reactions(modules_in_category),
            'regulatory_points': identify_regulation_points(modules_in_category)
        }

    return principles
```

#### 2. Reaction Classes (Chemical Transformation Patterns)

```python
def extract_reaction_patterns():
    """
    Use RCLASS to get reaction TYPES, not individual reactions
    RClass = chemical transformation patterns (e.g., phosphorylation)
    """

    # Get all reaction classes
    rclasses = kegg_get("list/rclass")

    # Group by transformation type
    transformation_patterns = {
        'phosphoryl_transfer': [],
        'oxidation_reduction': [],
        'group_transfer': [],
        'hydrolysis': [],
        'isomerization': [],
        'condensation': []
    }

    for rclass in rclasses:
        rclass_id = rclass.split('\t')[0]
        rclass_data = kegg_get(f"get/{rclass_id}")

        # Classify transformation pattern
        pattern_type = classify_transformation(rclass_data)
        transformation_patterns[pattern_type].append({
            'rclass_id': rclass_id,
            'substrate_pattern': extract_substrate_pattern(rclass_data),
            'product_pattern': extract_product_pattern(rclass_data)
        })

    return transformation_patterns
```

#### 3. Energy Coupling and ATP Dependency

```python
def identify_energy_coupling_patterns():
    """
    Find reactions coupled to ATP hydrolysis or other energy sources
    """

    # Key energy molecules
    energy_compounds = {
        'ATP': 'C00002',
        'GTP': 'C00044',
        'NADH': 'C00004',
        'NADPH': 'C00005',
        'FADH2': 'C01352'
    }

    energy_coupled_reactions = {}

    for energy_name, compound_id in energy_compounds.items():
        # Find all reactions involving this energy carrier
        reactions = kegg_get(f"link/reaction/cpd:{compound_id}")

        # Classify as energy-consuming or energy-producing
        for reaction in reactions.split('\n'):
            if reaction:
                rn_id = reaction.split('\t')[1]
                rn_data = kegg_get(f"get/{rn_id}")

                direction = classify_energy_direction(rn_data, compound_id)

                if energy_name not in energy_coupled_reactions:
                    energy_coupled_reactions[energy_name] = {
                        'producing': [],
                        'consuming': []
                    }

                energy_coupled_reactions[energy_name][direction].append(rn_id)

    return energy_coupled_reactions
```

#### 4. Pathway Topology and Branching Points

```python
def extract_pathway_topology(pathway_id='path:map00010'):
    """
    Parse KGML to extract pathway structure
    Identify: branching points, convergence points, cycles
    """

    kgml = kegg_get(f"get/{pathway_id}/kgml")

    # Parse KGML XML
    from xml.etree import ElementTree as ET
    root = ET.fromstring(kgml)

    # Build graph
    graph = {
        'nodes': {},  # Compounds and reactions
        'edges': [],  # Substrate-product relationships
        'branching_points': [],
        'convergence_points': [],
        'cycles': []
    }

    # Extract entries (compounds, reactions)
    for entry in root.findall('entry'):
        entry_id = entry.get('id')
        entry_type = entry.get('type')
        entry_name = entry.get('name')

        graph['nodes'][entry_id] = {
            'type': entry_type,
            'name': entry_name,
            'graphics': entry.find('graphics').attrib if entry.find('graphics') is not None else {}
        }

    # Extract relationships
    for relation in root.findall('relation'):
        entry1 = relation.get('entry1')
        entry2 = relation.get('entry2')
        rel_type = relation.get('type')

        graph['edges'].append({
            'from': entry1,
            'to': entry2,
            'type': rel_type
        })

    # Extract reactions (substrate -> product flow)
    for reaction in root.findall('reaction'):
        reaction_id = reaction.get('id')
        reaction_name = reaction.get('name')

        substrates = [s.get('id') for s in reaction.findall('substrate')]
        products = [p.get('id') for p in reaction.findall('product')]

        # Identify branching (1 substrate -> multiple products)
        if len(products) > 1:
            graph['branching_points'].append({
                'reaction': reaction_name,
                'substrate': substrates,
                'products': products
            })

        # Identify convergence (multiple substrates -> 1 product)
        if len(substrates) > 1:
            graph['convergence_points'].append({
                'reaction': reaction_name,
                'substrates': substrates,
                'product': products
            })

    # Detect cycles (feedback loops)
    graph['cycles'] = detect_cycles(graph['edges'])

    return graph
```

### KEGG Data Coverage

#### Available ✅
- Stoichiometric equations
- Reaction reversibility
- Pathway topology (graph structure)
- Enzyme associations
- Compound relationships
- Module definitions (functional units)
- Reaction class patterns
- Pathway maps with spatial layout

#### NOT Available ❌
- Thermodynamic parameters (ΔG, K_eq)
- Flux constraints or flux data
- Explicit feedback inhibition annotations
- Rate constants (k_cat, K_m)
- Quantitative regulation parameters

### Strategy Summary: KEGG

**DO:**
- ✅ Query by **modules** (functional units), not individual reactions
- ✅ Use **RClass** for reaction patterns
- ✅ Extract **pathway topology** from KGML
- ✅ Focus on **multi-step processes**
- ✅ Identify **energy coupling patterns** (ATP, NADH, etc.)
- ✅ Map **branching and convergence points**

**DON'T:**
- ❌ Download all 18,000 compounds individually
- ❌ Query every reaction separately
- ❌ Exceed 3 requests/second
- ❌ Expect thermodynamic data

---

## 4. Reactome - Pathway Database
**Scale**: 2,500+ pathways, 14,000+ reactions (human focus)

### API Access
- **Primary Endpoint**: https://reactome.org/ContentService/
- **Analysis Service**: https://reactome.org/AnalysisService/
- **API Documentation**: https://reactome.org/ContentService/ (Swagger/OpenAPI)
- **Python Client**: reactome2py (https://github.com/reactome/reactome2py)

### Authentication & Rate Limits
- **Authentication**: None required (free public access)
- **Rate Limits**: Not explicitly documented
  - Fair use policy applies
  - For heavy usage, consider local installation
- **License**: Creative Commons (CC BY 4.0)

### Data Formats
- **JSON**: Primary format for all REST endpoints
- **XML**: Available for some data types
- **SBML**: Systems Biology Markup Language (pathway models)
- **BioPAX**: Biological Pathway Exchange format
- **Plain Text**: Some simple queries
- **Images**: Pathway diagrams (PNG, SVG)

### Key Entity Types

#### Events (Core Abstraction)
- **Pathways**: Collections of reactions
- **Reactions**: Individual biochemical transformations
- **Event Hierarchy**: Nested pathway structure (pathways contain pathways)

#### Physical Entities
- **Simple Entities**: Small molecules, metabolites
- **Complexes**: Protein-protein, protein-metabolite complexes
- **Sets**: Groups of functionally equivalent entities
- **Polymers**: DNA, RNA, proteins

#### Regulation
- **Positive Regulation**: Activators, catalysts
- **Negative Regulation**: Inhibitors, feedback inhibition
- **Requirements**: Essential cofactors, conditions

#### Topology & Structure
- **Compartments**: Cellular locations (cytosol, mitochondria, etc.)
- **Preceding Events**: Temporal and logical dependencies
- **Followed By Events**: Downstream consequences
- **Pathway Diagram**: Spatial layout information

### API Examples

#### Basic Queries

```bash
# Get pathway hierarchy for a species
curl "https://reactome.org/ContentService/data/eventsHierarchy/HSA"  # Human

# Get specific pathway details
curl "https://reactome.org/ContentService/data/query/R-HSA-70326"  # Glucose metabolism

# Get all reactions in a pathway
curl "https://reactome.org/ContentService/data/pathway/R-HSA-70326/containedEvents"

# Get entities participating in a reaction
curl "https://reactome.org/ContentService/data/query/R-HSA-71403"  # Specific reaction

# Get regulation information
curl "https://reactome.org/ContentService/data/query/R-HSA-71403/regulatedBy"

# Get pathway diagram
curl "https://reactome.org/ContentService/data/pathway/R-HSA-70326/containedEvents"
```

#### Pattern-Focused Queries

```python
import requests

BASE_URL = "https://reactome.org/ContentService/data"

# 1. Get complete pathway hierarchy (topology)
def get_pathway_hierarchy(species='HSA'):
    """
    Get entire pathway tree structure
    This shows how pathways nest within each other
    """
    url = f"{BASE_URL}/eventsHierarchy/{species}"
    response = requests.get(url)
    return response.json()

# 2. Get pathway details with regulation
def get_pathway_with_regulation(pathway_id='R-HSA-70326'):
    """
    Get pathway including regulatory relationships
    """
    # Get basic pathway info
    pathway = requests.get(f"{BASE_URL}/query/{pathway_id}").json()

    # Get contained events
    events = requests.get(f"{BASE_URL}/pathway/{pathway_id}/containedEvents").json()

    # For each event, get regulation
    regulation_map = {}
    for event in events:
        event_id = event['stId']

        # Get regulators
        try:
            regulators = requests.get(f"{BASE_URL}/query/{event_id}/regulatedBy").json()
            regulation_map[event_id] = regulators
        except:
            regulation_map[event_id] = None

    return {
        'pathway': pathway,
        'events': events,
        'regulation': regulation_map
    }

# 3. Extract feedback loops
def find_feedback_patterns(pathway_id):
    """
    Identify potential feedback loops in pathway
    Look for products that regulate earlier steps
    """
    pathway_data = get_pathway_with_regulation(pathway_id)

    feedback_loops = []

    # Build dependency graph
    event_graph = {}
    for event in pathway_data['events']:
        event_id = event['stId']

        # Get preceding and following events
        preceding = event.get('precedingEvent', [])

        # Check if this event regulates any preceding event
        if pathway_data['regulation'].get(event_id):
            for regulator in pathway_data['regulation'][event_id]:
                if regulator.get('regulator'):
                    regulator_id = regulator['regulator']['stId']

                    # Check if regulator is in preceding events
                    if any(p['stId'] == regulator_id for p in preceding):
                        feedback_loops.append({
                            'regulated_event': event_id,
                            'regulator': regulator_id,
                            'regulation_type': regulator.get('regulationType')
                        })

    return feedback_loops

# 4. Extract multi-stage reaction chains
def extract_reaction_chains(pathway_id):
    """
    Find linear sequences of reactions (metabolic chains)
    """
    events = requests.get(f"{BASE_URL}/pathway/{pathway_id}/containedEvents").json()

    chains = []
    current_chain = []

    for event in events:
        if event.get('eventType') == 'Reaction':
            # Check if this continues the current chain
            if current_chain:
                last_event = current_chain[-1]
                # If input of current matches output of last
                if shares_entity(last_event['output'], event['input']):
                    current_chain.append(event)
                else:
                    # Chain broken, start new one
                    if len(current_chain) > 1:
                        chains.append(current_chain)
                    current_chain = [event]
            else:
                current_chain = [event]

    # Add final chain
    if len(current_chain) > 1:
        chains.append(current_chain)

    return chains

# 5. Get compartment-based organization
def analyze_compartmentalization(pathway_id):
    """
    Analyze how pathway is distributed across cellular compartments
    Identify transport steps between compartments
    """
    events = requests.get(f"{BASE_URL}/pathway/{pathway_id}/containedEvents").json()

    compartment_map = {}
    transport_steps = []

    for event in events:
        # Get compartments of inputs and outputs
        input_compartments = get_compartments(event.get('input', []))
        output_compartments = get_compartments(event.get('output', []))

        # If compartments differ, this is a transport step
        if input_compartments != output_compartments:
            transport_steps.append({
                'event': event['stId'],
                'from': input_compartments,
                'to': output_compartments
            })

        # Map events to compartments
        for comp in input_compartments | output_compartments:
            if comp not in compartment_map:
                compartment_map[comp] = []
            compartment_map[comp].append(event['stId'])

    return {
        'compartment_distribution': compartment_map,
        'transport_steps': transport_steps
    }
```

#### Advanced Pattern Mining

```python
# 6. Identify rate-limiting steps (heuristic)
def identify_potential_rate_limiting_steps(pathway_id):
    """
    Heuristic identification of rate-limiting steps based on:
    - Irreversible reactions
    - Highly regulated reactions
    - Committed steps (after branching points)
    """
    pathway_data = get_pathway_with_regulation(pathway_id)

    potential_rate_limiting = []

    for event in pathway_data['events']:
        score = 0
        reasons = []

        # Check for regulation (regulated steps often rate-limiting)
        if pathway_data['regulation'].get(event['stId']):
            regulators = pathway_data['regulation'][event['stId']]
            score += len(regulators) * 2
            reasons.append(f"Regulated by {len(regulators)} factors")

        # Check if irreversible (from event properties)
        if not event.get('reversibleReaction', True):
            score += 3
            reasons.append("Irreversible")

        # Check if it's an early committed step
        if is_committed_step(event, pathway_data):
            score += 2
            reasons.append("Committed step")

        # Check for energy coupling (ATP, GTP consumption)
        if uses_energy_currency(event):
            score += 1
            reasons.append("Energy-consuming")

        if score >= 3:
            potential_rate_limiting.append({
                'event': event['stId'],
                'score': score,
                'reasons': reasons
            })

    return sorted(potential_rate_limiting, key=lambda x: x['score'], reverse=True)

# 7. Extract homeostatic regulation mechanisms
def extract_homeostatic_patterns(pathway_id):
    """
    Find regulatory patterns that maintain homeostasis:
    - Negative feedback loops
    - Product inhibition
    - Allosteric regulation
    - Competitive inhibition
    """
    pathway_data = get_pathway_with_regulation(pathway_id)

    homeostatic_mechanisms = {
        'negative_feedback': [],
        'product_inhibition': [],
        'positive_regulation': [],
        'competitive_inhibition': []
    }

    for event_id, regulators in pathway_data['regulation'].items():
        if not regulators:
            continue

        for reg in regulators:
            reg_type = reg.get('regulationType', '').lower()
            regulator_entity = reg.get('regulator', {})

            # Classify regulation type
            if 'negative' in reg_type or 'inhibit' in reg_type:
                # Check if product inhibits its own production (feedback)
                if is_product_of_pathway(regulator_entity, event_id, pathway_data):
                    homeostatic_mechanisms['negative_feedback'].append({
                        'event': event_id,
                        'regulator': regulator_entity.get('stId'),
                        'mechanism': 'Product feedback inhibition'
                    })
                else:
                    homeostatic_mechanisms['product_inhibition'].append({
                        'event': event_id,
                        'regulator': regulator_entity.get('stId')
                    })

            elif 'positive' in reg_type or 'activat' in reg_type:
                homeostatic_mechanisms['positive_regulation'].append({
                    'event': event_id,
                    'regulator': regulator_entity.get('stId')
                })

    return homeostatic_mechanisms

# 8. Export to network format for analysis
def export_pathway_network(pathway_id, format='networkx'):
    """
    Convert pathway to network graph for analysis
    Enables: cycle detection, bottleneck analysis, path finding
    """
    import networkx as nx

    pathway_data = get_pathway_with_regulation(pathway_id)

    # Create directed graph
    G = nx.DiGraph()

    # Add nodes (events)
    for event in pathway_data['events']:
        G.add_node(event['stId'], **event)

    # Add edges (precedingEvent relationships)
    for event in pathway_data['events']:
        for preceding in event.get('precedingEvent', []):
            G.add_edge(preceding['stId'], event['stId'])

    # Add regulation edges (different color/style)
    for event_id, regulators in pathway_data['regulation'].items():
        if regulators:
            for reg in regulators:
                regulator_id = reg.get('regulator', {}).get('stId')
                if regulator_id:
                    G.add_edge(
                        regulator_id,
                        event_id,
                        edge_type='regulation',
                        regulation_type=reg.get('regulationType')
                    )

    # Analyze network properties
    network_properties = {
        'num_nodes': G.number_of_nodes(),
        'num_edges': G.number_of_edges(),
        'cycles': list(nx.simple_cycles(G)),
        'longest_path': nx.dag_longest_path(G) if nx.is_directed_acyclic_graph(G) else None,
        'branching_points': [n for n in G.nodes() if G.out_degree(n) > 1],
        'convergence_points': [n for n in G.nodes() if G.in_degree(n) > 1]
    }

    return G, network_properties
```

### Reactome's Strengths for Pattern Extraction

#### Available ✅
- **Pathway hierarchy** (nested structure)
- **Regulation annotations** (positive/negative, activation/inhibition)
- **Event relationships** (preceding/following)
- **Compartmentalization** (subcellular location)
- **Stoichiometry** (reaction equations)
- **Pathway diagrams** (spatial layout)
- **Cross-references** (UniProt, ChEBI, etc.)

#### NOT Available ❌
- Thermodynamic parameters (ΔG)
- Flux data or constraints
- Quantitative kinetics (k_cat, K_m)
- Explicit rate-limiting step annotations

### Strategy Summary: Reactome

**DO:**
- ✅ Use **pathway hierarchy** to understand organization
- ✅ Extract **regulation relationships** (feedback loops)
- ✅ Analyze **event dependencies** (preceding/following)
- ✅ Map **compartment transitions** (transport steps)
- ✅ Build **network graphs** for topology analysis
- ✅ Focus on **human pathways** (best curated)

**DON'T:**
- ❌ Query individual metabolites (focus on pathways)
- ❌ Expect thermodynamic or flux data
- ❌ Ignore the event hierarchy (key organizing principle)

---

## 5. MetaCyc - Metabolic Pathways Database
**Scale**: 3,150+ pathways, 19,000+ reactions, 19,000+ metabolites (all domains of life)

### API Access
- **Primary Endpoint**: BioCyc Web Services (https://biocyc.org/web-services.shtml)
- **SmartTables**: https://metacyc.org/smarttables (collections of objects)
- **SPARQL Endpoint**: Available for BioCyc databases
- **Pathway Tools API**: For programmatic access (requires installation)

### Authentication & Rate Limits
- **Authentication**: Requires subscription for API access
  - **MetaCyc**: Paid subscription required (as of Jan 1, 2024)
  - **EcoCyc**: Free access to data
- **Rate Limits**: Not publicly documented (reasonable use expected)
- **License**:
  - Academic: Paid subscription required for MetaCyc
  - Commercial: Commercial license required
  - Teaching: Free access available

### Subscription Requirements
⚠️ **Important**: As of January 2024, MetaCyc transitioned to a paid subscription model. NIH funding ended, requiring user subscriptions for access.

- **Contact**: BioCyc Support for pricing
- **Free Alternative**: EcoCyc (E. coli specific) remains free

### Data Formats
- **XML (ptools-xml)**: Primary format for pathway/reaction/compound objects
- **JSON**: Available for web services
- **Column-delimited**: Tabular format
- **SBML**: Systems Biology Markup Language
- **BioPAX**: Biological Pathway Exchange
- **SmartTable**: Interactive tables with filtering/sorting

### Key Entity Types

#### Pathways
- **Metabolic pathways** (primary and secondary metabolism)
- **Superpathways** (multi-pathway processes)
- **Pathway variants** (organism-specific versions)
- **Regulatory information** (activators, inhibitors)
- **Expected taxonomic range**

#### Reactions
- **Stoichiometric equations**
- **EC numbers** (Enzyme Commission classification)
- **Gibbs free energy of formation** (ΔG°')
- **Reversibility**
- **Spontaneity**
- **Enzyme properties**:
  - K_m values (substrate affinity)
  - k_cat values (turnover number)
  - Cofactor requirements
  - Activators and inhibitors

#### Compounds
- **Chemical structures** (SMILES, InChI, MOL)
- **Gibbs free energy of formation** (ΔG_f°)
- **pK_a values**
- **Cellular concentrations**
- **Roles in pathways**

#### Enzymes & Proteins
- **Subunit composition**
- **Cofactor requirements**
- **Substrate specificity**
- **Kinetic parameters**
- **Regulation** (allosteric, competitive, non-competitive)

### API Examples

#### Web Services API

```python
import requests
import xml.etree.ElementTree as ET

# Note: Requires subscription and authentication
# Authentication details not publicly documented

BASE_URL = "https://websvc.biocyc.org"

# 1. Get pathway in XML format
def get_pathway_xml(pathway_id, db='META'):
    """
    Retrieve pathway object in ptools-xml format
    db = 'META' for MetaCyc, 'ECO' for EcoCyc
    """
    url = f"{BASE_URL}/getxml?{db}:{pathway_id}"
    # Add authentication headers (subscription required)
    headers = {'Authorization': 'Bearer YOUR_API_KEY'}  # Example

    response = requests.get(url, headers=headers)
    return ET.fromstring(response.text)

# 2. Query using BioVelo query language
def query_biocyc(query, db='META'):
    """
    Example queries:
    - Find all reactions with ATP as substrate
    - Find all pathways in glycolysis category
    """
    url = f"{BASE_URL}/query?{db}&query={query}"
    response = requests.get(url, headers=auth_headers)
    return response.json()

# 3. Get reaction with thermodynamics
def get_reaction_with_thermodynamics(reaction_id, db='META'):
    """
    Retrieve reaction including ΔG values
    """
    url = f"{BASE_URL}/getxml?{db}:{reaction_id}"
    response = requests.get(url, headers=auth_headers)
    reaction_xml = ET.fromstring(response.text)

    # Parse thermodynamic data
    thermodynamics = {
        'gibbs_0': None,  # Standard Gibbs free energy
        'reversible': None,
        'spontaneous': None
    }

    for child in reaction_xml:
        if child.tag == 'gibbs-0':
            thermodynamics['gibbs_0'] = float(child.text)
        elif child.tag == 'reaction-direction':
            thermodynamics['reversible'] = (child.text == 'REVERSIBLE')
        elif child.tag == 'spontaneous':
            thermodynamics['spontaneous'] = (child.text == 'true')

    return thermodynamics

# 4. Get SmartTable data
def get_smarttable(smarttable_id):
    """
    Access pre-defined SmartTable collections
    Example: All pathways, all cofactors, etc.
    """
    url = f"https://metacyc.org/smarttable/{smarttable_id}"
    # SmartTables can be exported as CSV, JSON
    response = requests.get(url)
    return response.text
```

#### SmartTables (Web Interface)

SmartTables are powerful for extracting pattern-level data:

```python
# Available SmartTables (examples):
SMARTTABLES = {
    'all_pathways': ':ALL-PATHWAYS',
    'all_reactions': ':ALL-REACTIONS',
    'all_enzymes': ':ALL-ENZYMES',
    'all_cofactors': ':ALL-COFACTORS',
    'all_transport': ':ALL-TRANSPORT',
}

# Access via web interface:
# https://biocyc.org/smarttable/META/:ALL-PATHWAYS
# - Can filter, sort, export
# - Avoids downloading entire database
```

#### Pathway Tools API (Local Installation)

```python
# If you have Pathway Tools installed locally
# Python API for accessing local database

from ptools import Pathway, Reaction, Compound

# Get pathway and its regulation
pathway = Pathway('GLYCOLYSIS')

# Get regulatory information
regulators = pathway.get_regulators()
for reg in regulators:
    print(f"Regulated by: {reg.name}")
    print(f"Type: {reg.regulation_type}")  # activation, inhibition

# Get all reactions in pathway
reactions = pathway.get_reactions()
for rxn in reactions:
    # Get thermodynamics
    gibbs = rxn.get_gibbs_free_energy()
    print(f"ΔG°': {gibbs} kJ/mol")

    # Get kinetics
    enzymes = rxn.get_enzymes()
    for enz in enzymes:
        km = enz.get_km_values()
        kcat = enz.get_kcat_values()
        print(f"K_m: {km}, k_cat: {kcat}")
```

### Pattern Extraction from MetaCyc

#### 1. Thermodynamic Feasibility Analysis

```python
def analyze_pathway_thermodynamics(pathway_id):
    """
    Extract thermodynamic feasibility of pathway
    Identify energetically unfavorable steps requiring coupling
    """
    pathway = get_pathway_xml(pathway_id)
    reactions = pathway.findall('.//Reaction')

    thermodynamic_profile = {
        'favorable_steps': [],      # ΔG < 0
        'unfavorable_steps': [],    # ΔG > 0
        'near_equilibrium': [],     # ΔG ≈ 0
        'energy_coupling_required': []
    }

    for rxn in reactions:
        rxn_id = rxn.get('ID')
        gibbs = get_gibbs_energy(rxn)

        if gibbs is None:
            continue

        if gibbs < -5:  # Significantly negative (kJ/mol)
            thermodynamic_profile['favorable_steps'].append({
                'reaction': rxn_id,
                'gibbs': gibbs,
                'potential_regulation_point': True
            })
        elif gibbs > 5:  # Significantly positive
            thermodynamic_profile['unfavorable_steps'].append({
                'reaction': rxn_id,
                'gibbs': gibbs
            })

            # Check if coupled to ATP hydrolysis
            if is_atp_coupled(rxn):
                thermodynamic_profile['energy_coupling_required'].append({
                    'reaction': rxn_id,
                    'gibbs': gibbs,
                    'coupling': 'ATP'
                })
        else:  # Near equilibrium
            thermodynamic_profile['near_equilibrium'].append({
                'reaction': rxn_id,
                'gibbs': gibbs,
                'likely_reversible': True
            })

    return thermodynamic_profile

# 2. Regulatory Network Extraction
def extract_regulation_network(pathway_id):
    """
    Build regulatory network from pathway
    Focus on feedback and feedforward patterns
    """
    pathway = get_pathway_xml(pathway_id)

    regulation_network = {
        'feedback_inhibition': [],
        'feedback_activation': [],
        'feedforward_activation': [],
        'allosteric_regulation': [],
        'competitive_inhibition': []
    }

    reactions = pathway.findall('.//Reaction')

    for rxn in reactions:
        # Get regulatory information
        regulators = rxn.findall('.//Regulator')

        for reg in regulators:
            regulator_compound = reg.get('compound-id')
            regulation_type = reg.get('type')  # activation, inhibition
            mechanism = reg.get('mechanism')  # allosteric, competitive, etc.

            # Determine if feedback or feedforward
            if is_downstream_product(regulator_compound, rxn, pathway):
                # This is feedback regulation
                if regulation_type == 'inhibition':
                    regulation_network['feedback_inhibition'].append({
                        'reaction': rxn.get('ID'),
                        'regulator': regulator_compound,
                        'mechanism': mechanism
                    })
                elif regulation_type == 'activation':
                    regulation_network['feedback_activation'].append({
                        'reaction': rxn.get('ID'),
                        'regulator': regulator_compound,
                        'mechanism': mechanism
                    })
            else:
                # Feedforward regulation
                if regulation_type == 'activation':
                    regulation_network['feedforward_activation'].append({
                        'reaction': rxn.get('ID'),
                        'regulator': regulator_compound,
                        'mechanism': mechanism
                    })

            # Classify by mechanism
            if mechanism == 'allosteric':
                regulation_network['allosteric_regulation'].append({
                    'reaction': rxn.get('ID'),
                    'regulator': regulator_compound,
                    'type': regulation_type
                })
            elif mechanism == 'competitive':
                regulation_network['competitive_inhibition'].append({
                    'reaction': rxn.get('ID'),
                    'regulator': regulator_compound
                })

    return regulation_network

# 3. Cofactor Dependency Analysis
def analyze_cofactor_dependencies(pathway_id):
    """
    Identify cofactor requirements and recycling patterns
    """
    pathway = get_pathway_xml(pathway_id)
    reactions = pathway.findall('.//Reaction')

    cofactor_usage = {
        'NAD+/NADH': {'oxidizing': [], 'reducing': []},
        'NADP+/NADPH': {'oxidizing': [], 'reducing': []},
        'ATP/ADP': {'consuming': [], 'producing': []},
        'FAD/FADH2': {'oxidizing': [], 'reducing': []},
        'CoA': {'required': []},
    }

    for rxn in reactions:
        # Check substrates and products for cofactors
        substrates = rxn.findall('.//Substrate')
        products = rxn.findall('.//Product')

        # NAD+/NADH cycling
        if has_compound(substrates, 'NAD+') and has_compound(products, 'NADH'):
            cofactor_usage['NAD+/NADH']['reducing'].append(rxn.get('ID'))
        elif has_compound(substrates, 'NADH') and has_compound(products, 'NAD+'):
            cofactor_usage['NAD+/NADH']['oxidizing'].append(rxn.get('ID'))

        # NADP+/NADPH cycling
        if has_compound(substrates, 'NADP+') and has_compound(products, 'NADPH'):
            cofactor_usage['NADP+/NADPH']['reducing'].append(rxn.get('ID'))
        elif has_compound(substrates, 'NADPH') and has_compound(products, 'NADP+'):
            cofactor_usage['NADP+/NADPH']['oxidizing'].append(rxn.get('ID'))

        # ATP cycling
        if has_compound(substrates, 'ATP') and has_compound(products, 'ADP'):
            cofactor_usage['ATP/ADP']['consuming'].append(rxn.get('ID'))
        elif has_compound(substrates, 'ADP') and has_compound(products, 'ATP'):
            cofactor_usage['ATP/ADP']['producing'].append(rxn.get('ID'))

    # Calculate net cofactor balance
    net_balance = {}
    for cofactor, usage in cofactor_usage.items():
        if isinstance(usage, dict):
            net_balance[cofactor] = {
                'net_production': len(usage.get('producing', [])) - len(usage.get('consuming', [])),
                'requires_recycling': True if len(usage.get('consuming', [])) > 0 else False
            }

    return cofactor_usage, net_balance

# 4. Multi-stage Reaction Chain Analysis
def extract_reaction_chains(pathway_id):
    """
    Identify linear sequences and parallel branches
    """
    pathway = get_pathway_xml(pathway_id)
    reactions = pathway.findall('.//Reaction')

    # Build substrate-product graph
    graph = {}
    for rxn in reactions:
        rxn_id = rxn.get('ID')
        substrates = [s.get('compound-id') for s in rxn.findall('.//Substrate')]
        products = [p.get('compound-id') for p in rxn.findall('.//Product')]

        graph[rxn_id] = {
            'substrates': substrates,
            'products': products
        }

    # Find linear chains
    chains = []
    current_chain = []

    # Start from initial substrate
    for rxn_id, data in graph.items():
        # Check if substrate is not a product of any other reaction (start of chain)
        is_initial = all(
            sub not in other_data['products']
            for sub in data['substrates']
            for other_id, other_data in graph.items()
            if other_id != rxn_id
        )

        if is_initial:
            chain = trace_chain(rxn_id, graph)
            chains.append(chain)

    # Identify branching points
    branching_points = []
    for compound in get_all_compounds(graph):
        producers = [rid for rid, data in graph.items() if compound in data['products']]
        consumers = [rid for rid, data in graph.items() if compound in data['substrates']]

        if len(consumers) > 1:
            branching_points.append({
                'compound': compound,
                'branches': consumers
            })

    return {
        'chains': chains,
        'branching_points': branching_points,
        'longest_chain': max(chains, key=len) if chains else None
    }
```

### MetaCyc's Unique Strengths

#### Available ✅ (Unique Among These Databases)
- **Gibbs free energy values** (ΔG°')
- **Kinetic parameters** (K_m, k_cat, V_max)
- **Enzyme regulation details** (allosteric, competitive, non-competitive)
- **Cofactor requirements**
- **Activators and inhibitors**
- **Pathway variants** across organisms
- **Quantitative data** for modeling

#### Also Available ✅
- Stoichiometric equations
- Reaction directionality
- Pathway hierarchy
- Enzyme properties
- Taxonomic distribution

#### Limitations ❌
- **Requires paid subscription** (as of 2024)
- Flux data not included
- Not all reactions have thermodynamic data

### Strategy Summary: MetaCyc

**DO:**
- ✅ Use **SmartTables** to browse categories (avoid individual queries)
- ✅ Extract **thermodynamic data** for pathway feasibility
- ✅ Analyze **regulatory networks** (best annotation available)
- ✅ Focus on **cofactor dependencies**
- ✅ Identify **energy coupling mechanisms**
- ✅ Compare **pathway variants** across organisms

**DON'T:**
- ❌ Query all 19,000 metabolites individually
- ❌ Ignore thermodynamic constraints
- ❌ Forget subscription is required for access

---

## 6. eQuilibrator - Thermodynamics Database
**Specialized database for biochemical thermodynamics**

### API Access
- **Web Interface**: https://equilibrator.weizmann.ac.il/
- **Python API**: `equilibrator-api` (pip install equilibrator-api)
- **Documentation**: https://equilibrator.readthedocs.io/
- **GitHub**: https://github.com/eladnoor/equilibrator-api

### Authentication & Rate Limits
- **Authentication**: None required
- **Rate Limits**: Not specified for API
  - Web interface: reasonable use
  - Python package: no limits (runs locally)
- **License**: Open source, free for all uses

### Data Formats
- **Python Objects**: Primary interface via equilibrator-api
- **JSON**: Can export calculations
- **CSV**: For batch results
- **Downloadable Data**: All thermodynamic source data freely available

### Key Capabilities

#### Thermodynamic Properties
- **Standard Gibbs Free Energy** (ΔG°')
- **Physiological Gibbs Free Energy** (ΔG')
  - Adjusted for pH, ionic strength, temperature
  - Adjusted for metabolite concentrations
- **Equilibrium Constants** (K_eq)
- **Reaction Feasibility** analysis

#### Metabolite Coverage
- Integration with **MetaNetX** (comprehensive metabolite database)
- Cross-references to:
  - KEGG compounds
  - BiGG models
  - ModelSEED
  - ChEBI

### Python API Examples

```python
# Install: pip install equilibrator-api
from equilibrator_api import ComponentContribution, Reaction, Q_

# Initialize the calculator
cc = ComponentContribution()

# 1. Calculate ΔG for a reaction
# Example: ATP hydrolysis
rxn = Reaction.parse_formula("ATP + H2O = ADP + phosphate")

# Standard conditions (pH 7, ionic strength 0.1M, 25°C)
dG0_prime = cc.standard_dg_prime(rxn)
print(f"ΔG°' = {dG0_prime}")  # Returns energy with units

# 2. Physiological conditions
# Adjust for actual cellular concentrations
dG_prime = cc.physiological_dg_prime(
    rxn,
    p_h=Q_(7.4),  # Physiological pH
    ionic_strength=Q_(0.25, "M"),  # Typical cellular ionic strength
    temperature=Q_(37, "degC"),  # Body temperature
    concentrations={
        "ATP": Q_(3, "mM"),
        "ADP": Q_(0.5, "mM"),
        "phosphate": Q_(10, "mM")
    }
)
print(f"ΔG' = {dG_prime}")

# 3. Batch calculation for pathway
pathway_reactions = [
    "glucose + ATP = glucose-6-phosphate + ADP",
    "glucose-6-phosphate = fructose-6-phosphate",
    "fructose-6-phosphate + ATP = fructose-1,6-bisphosphate + ADP",
    # ... more reactions
]

pathway_energetics = []
for rxn_str in pathway_reactions:
    rxn = Reaction.parse_formula(rxn_str)
    dG = cc.standard_dg_prime(rxn)
    pathway_energetics.append({
        'reaction': rxn_str,
        'dG0_prime': float(dG.magnitude),
        'spontaneous': float(dG.magnitude) < 0
    })

# 4. Calculate overall pathway ΔG
total_dG = sum(r['dG0_prime'] for r in pathway_energetics)
print(f"Total pathway ΔG°' = {total_dG} kJ/mol")

# 5. Find equilibrium constant
K_eq = cc.equilibrium_constant(rxn)
print(f"K_eq = {K_eq}")

# 6. Reverse reaction feasibility
reverse_rxn = Reaction.parse_formula("ADP + phosphate = ATP + H2O")
dG_reverse = cc.standard_dg_prime(reverse_rxn)
print(f"Reverse ΔG°' = {dG_reverse}")
# Should be negative of forward reaction
```

### Pattern Extraction with eQuilibrator

```python
# 1. Identify thermodynamically unfavorable steps
def find_unfavorable_steps(pathway_reactions):
    """
    Find reactions requiring energy coupling
    """
    cc = ComponentContribution()

    unfavorable = []
    for rxn_str in pathway_reactions:
        rxn = Reaction.parse_formula(rxn_str)
        dG = cc.standard_dg_prime(rxn)

        if dG.magnitude > 0:  # Unfavorable
            unfavorable.append({
                'reaction': rxn_str,
                'dG0_prime': dG.magnitude,
                'requires_coupling': dG.magnitude > 5  # Threshold
            })

    return unfavorable

# 2. Analyze energy coupling strategies
def analyze_energy_coupling(main_reaction, coupling_reaction):
    """
    Calculate if coupling makes reaction favorable
    Example: Glucose phosphorylation coupled to ATP hydrolysis
    """
    cc = ComponentContribution()

    main_rxn = Reaction.parse_formula(main_reaction)
    coupling_rxn = Reaction.parse_formula(coupling_reaction)

    # Individual reactions
    dG_main = cc.standard_dg_prime(main_rxn)
    dG_coupling = cc.standard_dg_prime(coupling_rxn)

    # Combined reaction (sum)
    combined_formula = combine_reactions(main_reaction, coupling_reaction)
    combined_rxn = Reaction.parse_formula(combined_formula)
    dG_combined = cc.standard_dg_prime(combined_rxn)

    return {
        'main_dG': dG_main.magnitude,
        'coupling_dG': dG_coupling.magnitude,
        'combined_dG': dG_combined.magnitude,
        'coupling_effective': dG_combined.magnitude < 0
    }

# 3. Pathway directionality analysis
def analyze_pathway_directionality(pathway_reactions, concentrations=None):
    """
    Determine which direction pathway will proceed
    Based on thermodynamics and concentrations
    """
    cc = ComponentContribution()

    # Standard conditions
    forward_feasible = []
    reverse_feasible = []
    near_equilibrium = []

    for rxn_str in pathway_reactions:
        rxn = Reaction.parse_formula(rxn_str)

        if concentrations:
            dG = cc.physiological_dg_prime(rxn, concentrations=concentrations)
        else:
            dG = cc.standard_dg_prime(rxn)

        dG_val = dG.magnitude

        if dG_val < -5:
            forward_feasible.append(rxn_str)
        elif dG_val > 5:
            reverse_feasible.append(rxn_str)
        else:
            near_equilibrium.append(rxn_str)

    return {
        'forward_driven': forward_feasible,
        'reverse_driven': reverse_feasible,
        'reversible': near_equilibrium
    }

# 4. Identify regulatory leverage points
def identify_thermodynamic_control_points(pathway_reactions):
    """
    Find reactions with large negative ΔG (irreversible, regulatory)
    These are often rate-limiting and regulated
    """
    cc = ComponentContribution()

    control_points = []

    for rxn_str in pathway_reactions:
        rxn = Reaction.parse_formula(rxn_str)
        dG = cc.standard_dg_prime(rxn)

        # Large negative ΔG = irreversible, committed step
        if dG.magnitude < -20:  # Highly exergonic
            control_points.append({
                'reaction': rxn_str,
                'dG0_prime': dG.magnitude,
                'likely_regulated': True,
                'irreversible': True
            })

    return sorted(control_points, key=lambda x: x['dG0_prime'])
```

### Integration with Other Databases

```python
# Combine KEGG pathway with eQuilibrator thermodynamics

def enrich_kegg_pathway_with_thermodynamics(pathway_id='path:map00010'):
    """
    Get KEGG pathway and add thermodynamic data from eQuilibrator
    """
    import requests
    from equilibrator_api import ComponentContribution, Reaction

    cc = ComponentContribution()

    # Get reactions from KEGG
    kegg_reactions = get_kegg_pathway_reactions(pathway_id)

    enriched_pathway = []

    for kegg_rxn in kegg_reactions:
        # Convert KEGG reaction equation to eQuilibrator format
        equilibrator_formula = convert_kegg_to_equilibrator(kegg_rxn['equation'])

        try:
            rxn = Reaction.parse_formula(equilibrator_formula)
            dG = cc.standard_dg_prime(rxn)
            K_eq = cc.equilibrium_constant(rxn)

            enriched_pathway.append({
                'kegg_id': kegg_rxn['id'],
                'equation': kegg_rxn['equation'],
                'dG0_prime': float(dG.magnitude),
                'K_eq': float(K_eq.magnitude),
                'spontaneous': float(dG.magnitude) < 0,
                'enzyme': kegg_rxn.get('enzyme'),
                'pathway': pathway_id
            })
        except Exception as e:
            # Some reactions may not be calculable
            enriched_pathway.append({
                'kegg_id': kegg_rxn['id'],
                'equation': kegg_rxn['equation'],
                'dG0_prime': None,
                'error': str(e)
            })

    return enriched_pathway
```

### eQuilibrator's Strengths

#### Available ✅
- **Most comprehensive thermodynamic data** for biochemistry
- **Adjustable conditions** (pH, ionic strength, temperature, concentrations)
- **Uncertainty estimates** for predictions
- **Component Contribution method** (group contribution + data)
- **Free and open source**

#### Use Cases ✅
- Pathway feasibility analysis
- Energy coupling identification
- Metabolic flux analysis (constraint-based modeling)
- Identifying regulatory control points
- Reaction directionality prediction

### Strategy Summary: eQuilibrator

**DO:**
- ✅ Use for **thermodynamic feasibility** of pathways
- ✅ **Adjust for physiological conditions** (not just standard)
- ✅ Identify **energy coupling requirements**
- ✅ Find **thermodynamically irreversible steps** (regulatory points)
- ✅ **Combine with KEGG/Reactome** for complete picture

**DON'T:**
- ❌ Use for reaction kinetics (rates, K_m, etc.)
- ❌ Expect data for all possible reactions
- ❌ Ignore uncertainty estimates

---

## Pattern Extraction Strategies

### Overall Approach: Principles Over Lists

**The Goal**: Extract **RULES** and **PATTERNS**, not exhaustive catalogs.

### 1. Hierarchical Querying Strategy

Instead of querying 220,000 metabolites, query by **functional categories**:

```python
# BAD: Query all metabolites
for metabolite_id in range(1, 220000):  # ❌ Don't do this!
    get_metabolite_details(metabolite_id)

# GOOD: Query by category
categories = [
    'energy_carriers',      # ATP, GTP, NADH, FADH2
    'cofactors',           # Vitamins, metal ions
    'signaling_molecules', # cAMP, Ca2+, hormones
    'central_metabolites', # Glycolysis, TCA intermediates
    'feedback_regulators'  # Allosteric inhibitors/activators
]

for category in categories:
    category_members = get_metabolites_by_role(category)
    analyze_category_patterns(category_members)
```

### 2. Module and Pathway-Centric Analysis

Focus on **functional units**, not individual components:

```python
# Hierarchy of analysis:
# 1. Pathways (e.g., Glycolysis)
#    └─ 2. Modules (e.g., Glucose activation)
#          └─ 3. Reactions (e.g., Hexokinase)
#                └─ 4. Metabolites (e.g., Glucose, ATP)

def extract_pathway_principles(database='KEGG'):
    """
    Top-down approach: Pathways → Modules → Reactions
    """

    # Level 1: Get pathway categories
    pathway_categories = {
        'carbohydrate_metabolism': [],
        'amino_acid_metabolism': [],
        'lipid_metabolism': [],
        'nucleotide_metabolism': [],
        'energy_metabolism': []
    }

    # Level 2: For each category, get modules
    for category, pathways in pathway_categories.items():
        modules = get_modules_for_pathways(pathways)

        # Level 3: Analyze module patterns
        patterns = {
            'committed_steps': [],
            'regulation_points': [],
            'energy_coupling': [],
            'cofactor_usage': [],
            'feedback_loops': []
        }

        for module in modules:
            patterns['committed_steps'].extend(
                identify_committed_steps(module)
            )
            patterns['regulation_points'].extend(
                identify_regulation_points(module)
            )
            # ... etc

        # Level 4: Extract principles
        principles = extract_principles_from_patterns(patterns)
```

### 3. Cross-Database Integration

Combine strengths of multiple databases:

```python
def integrated_pathway_analysis(pathway_name='Glycolysis'):
    """
    Use multiple databases for complementary information
    """

    analysis = {}

    # 1. KEGG: Pathway topology and modules
    analysis['topology'] = {
        'graph': get_kegg_pathway_graph(pathway_name),
        'modules': get_kegg_modules(pathway_name),
        'reaction_classes': get_kegg_rclass_patterns(pathway_name)
    }

    # 2. Reactome: Regulation and compartmentalization
    analysis['regulation'] = {
        'feedback_loops': get_reactome_feedback_loops(pathway_name),
        'activation': get_reactome_activators(pathway_name),
        'inhibition': get_reactome_inhibitors(pathway_name),
        'compartments': get_reactome_compartments(pathway_name)
    }

    # 3. eQuilibrator: Thermodynamics
    analysis['thermodynamics'] = {
        'reaction_energies': get_equilibrator_dG_values(pathway_name),
        'unfavorable_steps': identify_unfavorable_steps(pathway_name),
        'energy_coupling': identify_atp_coupled_steps(pathway_name)
    }

    # 4. MetaCyc: Detailed regulation and kinetics
    analysis['kinetics'] = {
        'km_values': get_metacyc_km_values(pathway_name),
        'allosteric_regulation': get_metacyc_allosteric_sites(pathway_name),
        'cofactors': get_metacyc_cofactor_requirements(pathway_name)
    }

    # 5. ChEBI: Functional classification of metabolites
    analysis['metabolite_roles'] = {
        'cofactors': get_chebi_cofactors_in_pathway(pathway_name),
        'intermediates': get_chebi_pathway_intermediates(pathway_name),
        'regulators': get_chebi_regulatory_molecules(pathway_name)
    }

    # Synthesize principles
    principles = synthesize_principles(analysis)

    return principles

def synthesize_principles(analysis):
    """
    Extract high-level principles from integrated data
    """
    principles = {
        'flow_control': [],
        'energy_management': [],
        'homeostatic_regulation': [],
        'network_topology': [],
        'multi_stage_coordination': []
    }

    # Flow control principles
    # - Identify rate-limiting steps (thermodynamics + regulation)
    rate_limiting = []
    for rxn in analysis['thermodynamics']['reaction_energies']:
        if rxn['dG'] < -20:  # Highly irreversible
            if rxn['id'] in analysis['regulation']['inhibition']:
                rate_limiting.append({
                    'reaction': rxn['id'],
                    'principle': 'Irreversible + regulated = rate-limiting',
                    'evidence': {
                        'thermodynamic': rxn['dG'],
                        'regulatory': analysis['regulation']['inhibition'][rxn['id']]
                    }
                })
    principles['flow_control'] = rate_limiting

    # Energy management principles
    # - ATP coupling for unfavorable reactions
    energy_coupling = []
    for rxn in analysis['thermodynamics']['unfavorable_steps']:
        if rxn in analysis['thermodynamics']['energy_coupling']:
            energy_coupling.append({
                'reaction': rxn,
                'principle': 'Unfavorable reactions coupled to ATP hydrolysis',
                'dG_uncoupled': rxn['dG'],
                'dG_coupled': rxn['dG_coupled']
            })
    principles['energy_management'] = energy_coupling

    # Homeostatic regulation principles
    # - Feedback inhibition by end products
    feedback_patterns = []
    for loop in analysis['regulation']['feedback_loops']:
        if loop['type'] == 'negative':
            feedback_patterns.append({
                'principle': 'End-product feedback inhibition',
                'pathway': loop['pathway'],
                'regulated_step': loop['target'],
                'regulator': loop['source'],
                'mechanism': analysis['kinetics']['allosteric_regulation'].get(loop['target'])
            })
    principles['homeostatic_regulation'] = feedback_patterns

    # Network topology principles
    # - Branching points for metabolite distribution
    branching = analysis['topology']['graph']['branching_points']
    principles['network_topology'] = [
        {
            'principle': 'Branching points distribute flux to multiple pathways',
            'locations': branching,
            'regulation': [
                analysis['regulation'].get(b) for b in branching
            ]
        }
    ]

    # Multi-stage coordination
    # - Cofactor recycling across reactions
    cofactor_patterns = []
    for cofactor, usage in analysis['kinetics']['cofactors'].items():
        if usage['consuming'] and usage['producing']:
            cofactor_patterns.append({
                'principle': 'Cofactor recycling maintains redox balance',
                'cofactor': cofactor,
                'consumers': usage['consuming'],
                'producers': usage['producing'],
                'net_balance': len(usage['producing']) - len(usage['consuming'])
            })
    principles['multi_stage_coordination'] = cofactor_patterns

    return principles
```

### 4. Pattern Templates

Define reusable patterns to search for:

```python
METABOLIC_PATTERNS = {
    'feedback_inhibition': {
        'description': 'End product inhibits early committed step',
        'components': {
            'pathway': 'linear or branched',
            'regulated_enzyme': 'early in pathway',
            'inhibitor': 'end product',
            'mechanism': 'allosteric'
        },
        'search_strategy': {
            'kegg': 'Find pathways with branching',
            'reactome': 'Get regulation relationships',
            'metacyc': 'Confirm allosteric mechanism',
            'chebi': 'Verify inhibitor is product'
        }
    },

    'substrate_channeling': {
        'description': 'Intermediates passed directly between enzymes',
        'components': {
            'enzyme_complex': 'multi-enzyme complex',
            'intermediates': 'unstable or toxic',
            'compartment': 'localized'
        },
        'search_strategy': {
            'reactome': 'Find enzyme complexes',
            'metacyc': 'Get subunit composition',
            'kegg': 'Check pathway topology'
        }
    },

    'energy_coupling': {
        'description': 'Unfavorable reaction driven by favorable one',
        'components': {
            'unfavorable_rxn': 'ΔG > 0',
            'favorable_rxn': 'ATP → ADP + Pi',
            'coupled_mechanism': 'shared intermediate or complex'
        },
        'search_strategy': {
            'equilibrator': 'Calculate ΔG values',
            'kegg': 'Find reactions with ATP',
            'metacyc': 'Verify coupling mechanism'
        }
    },

    'futile_cycle_prevention': {
        'description': 'Prevent simultaneous forward and reverse pathways',
        'components': {
            'forward_pathway': 'e.g., glycolysis',
            'reverse_pathway': 'e.g., gluconeogenesis',
            'regulation': 'reciprocal regulation'
        },
        'search_strategy': {
            'kegg': 'Find paired pathways',
            'reactome': 'Get regulation relationships',
            'metacyc': 'Verify reciprocal inhibition'
        }
    },

    'committed_step': {
        'description': 'First irreversible reaction in pathway',
        'components': {
            'position': 'early in pathway',
            'thermodynamics': 'ΔG << 0',
            'regulation': 'highly regulated',
            'uniqueness': 'product specific to this pathway'
        },
        'search_strategy': {
            'equilibrator': 'Find highly negative ΔG',
            'kegg': 'Check pathway position',
            'reactome': 'Verify high regulation',
            'metacyc': 'Check product usage'
        }
    }
}

def search_for_pattern(pattern_name, target_pathway=None):
    """
    Search across databases for specific metabolic pattern
    """
    pattern = METABOLIC_PATTERNS[pattern_name]

    results = {
        'pattern': pattern_name,
        'instances': []
    }

    # Execute search strategy
    for database, query_description in pattern['search_strategy'].items():
        if database == 'kegg':
            kegg_results = execute_kegg_pattern_search(pattern, target_pathway)
            results['instances'].extend(kegg_results)

        elif database == 'reactome':
            reactome_results = execute_reactome_pattern_search(pattern, target_pathway)
            results['instances'].extend(reactome_results)

        elif database == 'equilibrator':
            thermo_results = execute_thermodynamic_pattern_search(pattern, target_pathway)
            results['instances'].extend(thermo_results)

        elif database == 'metacyc':
            metacyc_results = execute_metacyc_pattern_search(pattern, target_pathway)
            results['instances'].extend(metacyc_results)

    # Filter for complete matches (have all required components)
    complete_instances = [
        inst for inst in results['instances']
        if all(comp in inst for comp in pattern['components'].keys())
    ]

    return complete_instances
```

### 5. Summary Statistics Instead of Exhaustive Lists

```python
def pathway_summary_statistics(pathway_id):
    """
    Get statistical summary instead of complete data
    """
    summary = {
        'pathway_id': pathway_id,
        'total_reactions': 0,
        'total_metabolites': 0,

        # Thermodynamic summary
        'thermodynamics': {
            'favorable_reactions': 0,
            'unfavorable_reactions': 0,
            'near_equilibrium': 0,
            'mean_dG': 0,
            'std_dG': 0
        },

        # Topology summary
        'topology': {
            'linear_segments': 0,
            'branching_points': 0,
            'convergence_points': 0,
            'cycles': 0,
            'longest_chain': 0
        },

        # Regulation summary
        'regulation': {
            'regulated_steps': 0,
            'feedback_loops': 0,
            'feedforward_loops': 0,
            'allosteric_sites': 0
        },

        # Energy summary
        'energy': {
            'atp_consuming': 0,
            'atp_producing': 0,
            'net_atp': 0,
            'nadh_producing': 0,
            'nadh_consuming': 0,
            'net_nadh': 0
        },

        # Functional classification
        'metabolite_roles': {
            'cofactors': [],  # Just list types, not all instances
            'intermediates': 0,  # Count
            'branch_points': [],
            'regulatory_molecules': []
        }
    }

    # Populate summary (implementation details omitted)
    # ...

    return summary
```

---

## Key Principles to Extract

### 1. Flow Rules and Constraint Networks

**What to extract:**
- Stoichiometric constraints (mass balance)
- Thermodynamic feasibility (ΔG constraints)
- Cofactor availability (NAD+/NADH, ATP/ADP ratios)
- Compartmentalization (transport constraints)

**Where to find:**
- **KEGG**: Reaction stoichiometry, modules
- **Reactome**: Compartment information
- **eQuilibrator**: Thermodynamic constraints
- **MetaCyc**: Complete stoichiometry with cofactors

### 2. Feedback Inhibition Patterns

**What to extract:**
- End-product inhibition of committed steps
- Negative feedback loops
- Allosteric regulation sites
- Competitive inhibition

**Where to find:**
- **MetaCyc**: Most detailed (allosteric mechanisms, K_i values)
- **Reactome**: Regulation relationships
- **KEGG**: Limited (pathway maps show some regulation)

### 3. Rate-Limiting Steps

**What to extract:**
- Irreversible reactions (ΔG << 0)
- Highly regulated enzymes
- Committed steps (first irreversible after branch point)
- Slow enzymes (low k_cat or high K_m)

**Where to find:**
- **eQuilibrator**: Thermodynamic irreversibility
- **Reactome**: Regulation intensity
- **MetaCyc**: Kinetic parameters
- **KEGG**: Pathway position (modules)

### 4. Energy Coupling Principles

**What to extract:**
- ATP-driven unfavorable reactions
- Proton gradient coupling
- Redox coupling (NADH/NADPH)
- Group transfer reactions

**Where to find:**
- **eQuilibrator**: Calculate coupled ΔG
- **KEGG**: Identify ATP-coupled reactions
- **MetaCyc**: Mechanism of coupling
- **Reactome**: Complex formation

### 5. Homeostatic Regulation Mechanisms

**What to extract:**
- Set points (normal metabolite concentrations)
- Feedback loops (negative and positive)
- Feedforward activation
- Reciprocal regulation (futile cycle prevention)

**Where to find:**
- **HMDB**: Normal concentration ranges
- **MetaCyc**: Detailed regulation mechanisms
- **Reactome**: Regulatory network topology
- **KEGG**: Pathway-level regulation

### 6. Multi-Stage Reaction Chains

**What to extract:**
- Linear sequences (metabolic chains)
- Enzyme complexes (substrate channeling)
- Cofactor recycling patterns
- Coordinated regulation of chain

**Where to find:**
- **KEGG**: Modules (multi-step units)
- **Reactome**: Event sequences, complexes
- **MetaCyc**: Enzyme complexes, subunit composition
- **ChEBI**: Cofactor classification

---

## Quick Reference Table

| Database | Best For | Authentication | Rate Limit | Thermodynamics | Regulation | Cost |
|----------|----------|----------------|------------|----------------|------------|------|
| **HMDB** | Metabolite catalog, concentrations | Contact-based | Unknown | ❌ No | ❌ Limited | Free (web) |
| **ChEBI** | Functional roles, ontology | None | Reasonable use | ❌ No | ⚠️ Some | Free |
| **KEGG** | Pathway topology, modules | None (academic) | 3/second | ❌ No | ⚠️ Some | Free (academic) |
| **Reactome** | Regulation, compartments | None | Reasonable use | ❌ No | ✅ Yes | Free |
| **MetaCyc** | Kinetics, detailed regulation | Subscription | Reasonable use | ✅ Yes (ΔG) | ✅ Yes | **Paid** |
| **eQuilibrator** | Thermodynamics | None | None (local API) | ✅ Yes | ❌ No | Free |

---

## Recommended Workflow

### For Extracting Pathway Principles

1. **Start with KEGG**:
   - Get pathway overview and modules
   - Identify core reactions and topology
   - Find energy-coupled reactions (ATP, NADH)

2. **Add Thermodynamics with eQuilibrator**:
   - Calculate ΔG for each reaction
   - Identify irreversible steps (potential regulation points)
   - Find unfavorable steps requiring coupling

3. **Enrich with Reactome**:
   - Get regulation relationships
   - Find feedback loops
   - Identify compartmentalization

4. **Detail with MetaCyc** (if subscription available):
   - Get kinetic parameters
   - Confirm allosteric mechanisms
   - Get cofactor requirements

5. **Classify with ChEBI**:
   - Categorize metabolites by role
   - Identify cofactors vs. intermediates
   - Find regulatory molecules

6. **Contextualize with HMDB**:
   - Get normal concentration ranges
   - Link to disease states
   - Understand clinical relevance

### For Each Database, Focus On:

**Avoid**: Downloading all metabolites/reactions
**Instead**: Query by:
- Pathway membership
- Functional category (cofactors, regulators)
- Reaction class (phosphorylation, oxidation)
- Module (multi-step functional unit)
- Regulation type (feedback, allosteric)

---

## Example Code: Complete Integration

```python
#!/usr/bin/env python3
"""
Complete example: Extract principles from glycolysis
Integrates multiple databases to find patterns
"""

import requests
import time
from equilibrator_api import ComponentContribution, Reaction, Q_

class MetabolicPatternExtractor:
    """
    Extract metabolic principles from multiple databases
    """

    def __init__(self):
        self.kegg_base = "https://rest.kegg.jp"
        self.reactome_base = "https://reactome.org/ContentService/data"
        self.cc = ComponentContribution()
        self.rate_limit = 0.34  # KEGG rate limit

    def analyze_pathway(self, pathway_name="Glycolysis"):
        """
        Complete pathway analysis
        """
        print(f"Analyzing {pathway_name}...")

        results = {
            'pathway': pathway_name,
            'principles': {}
        }

        # 1. KEGG: Get topology and reactions
        print("  [1/5] Extracting topology from KEGG...")
        kegg_data = self.get_kegg_pathway_data('map00010')  # Glycolysis
        results['topology'] = kegg_data

        # 2. eQuilibrator: Calculate thermodynamics
        print("  [2/5] Calculating thermodynamics...")
        thermodynamics = self.calculate_pathway_thermodynamics(
            kegg_data['reactions']
        )
        results['thermodynamics'] = thermodynamics

        # 3. Identify rate-limiting steps
        print("  [3/5] Identifying rate-limiting steps...")
        rate_limiting = self.identify_rate_limiting_steps(
            kegg_data,
            thermodynamics
        )
        results['principles']['rate_limiting_steps'] = rate_limiting

        # 4. Find feedback patterns
        print("  [4/5] Finding feedback patterns...")
        feedback = self.find_feedback_patterns(kegg_data)
        results['principles']['feedback_inhibition'] = feedback

        # 5. Analyze energy coupling
        print("  [5/5] Analyzing energy coupling...")
        energy = self.analyze_energy_coupling(kegg_data, thermodynamics)
        results['principles']['energy_coupling'] = energy

        print(f"✓ Analysis complete!")
        return results

    def get_kegg_pathway_data(self, pathway_id):
        """Get pathway from KEGG"""
        time.sleep(self.rate_limit)

        # Get pathway info
        pathway_info = requests.get(
            f"{self.kegg_base}/get/{pathway_id}"
        ).text

        # Get reactions in pathway
        time.sleep(self.rate_limit)
        reactions_response = requests.get(
            f"{self.kegg_base}/link/reaction/{pathway_id}"
        ).text

        reaction_ids = [
            line.split('\t')[1]
            for line in reactions_response.split('\n')
            if line
        ]

        # Get reaction details
        reactions = []
        for rn_id in reaction_ids[:10]:  # Sample for demo
            time.sleep(self.rate_limit)
            rn_data = requests.get(
                f"{self.kegg_base}/get/{rn_id}"
            ).text

            reactions.append({
                'id': rn_id,
                'data': rn_data
            })

        return {
            'pathway_id': pathway_id,
            'pathway_info': pathway_info,
            'reactions': reactions
        }

    def calculate_pathway_thermodynamics(self, reactions):
        """Calculate ΔG for each reaction"""
        thermodynamics = []

        for rxn_data in reactions:
            # Parse reaction equation
            equation = self.parse_kegg_equation(rxn_data['data'])

            if equation:
                try:
                    rxn = Reaction.parse_formula(equation)
                    dG = self.cc.standard_dg_prime(rxn)

                    thermodynamics.append({
                        'reaction_id': rxn_data['id'],
                        'equation': equation,
                        'dG0_prime': float(dG.magnitude),
                        'spontaneous': float(dG.magnitude) < 0,
                        'irreversible': float(dG.magnitude) < -20
                    })
                except:
                    thermodynamics.append({
                        'reaction_id': rxn_data['id'],
                        'equation': equation,
                        'dG0_prime': None,
                        'error': 'Calculation failed'
                    })

        return thermodynamics

    def identify_rate_limiting_steps(self, kegg_data, thermodynamics):
        """
        Heuristic for rate-limiting steps:
        - Highly negative ΔG (irreversible)
        - Uses ATP (energy investment)
        - Early in pathway
        """
        rate_limiting = []

        for i, thermo in enumerate(thermodynamics):
            if thermo.get('dG0_prime') and thermo['dG0_prime'] < -20:
                rate_limiting.append({
                    'reaction': thermo['reaction_id'],
                    'dG': thermo['dG0_prime'],
                    'position': f"Step {i+1}",
                    'reason': 'Highly irreversible',
                    'likely_regulated': True
                })

        return rate_limiting

    def find_feedback_patterns(self, kegg_data):
        """
        Identify potential feedback loops
        (Simplified - real implementation would parse pathway topology)
        """
        # This would require graph analysis of KGML
        # Placeholder for demonstration
        return {
            'note': 'Feedback loop detection requires KGML parsing',
            'known_feedback': [
                {
                    'pathway': 'Glycolysis',
                    'pattern': 'ATP inhibits phosphofructokinase',
                    'type': 'Product inhibition'
                },
                {
                    'pathway': 'Glycolysis',
                    'pattern': 'AMP activates phosphofructokinase',
                    'type': 'Energy sensing'
                }
            ]
        }

    def analyze_energy_coupling(self, kegg_data, thermodynamics):
        """Find ATP-coupled reactions"""
        atp_coupled = []

        for rxn_data in kegg_data['reactions']:
            equation = self.parse_kegg_equation(rxn_data['data'])

            if equation and 'ATP' in equation:
                # Find corresponding thermodynamics
                thermo = next(
                    (t for t in thermodynamics
                     if t['reaction_id'] == rxn_data['id']),
                    None
                )

                atp_coupled.append({
                    'reaction': rxn_data['id'],
                    'equation': equation,
                    'dG': thermo.get('dG0_prime') if thermo else None,
                    'principle': 'Energy investment via ATP'
                })

        return atp_coupled

    def parse_kegg_equation(self, kegg_text):
        """Extract reaction equation from KEGG data"""
        for line in kegg_text.split('\n'):
            if line.startswith('EQUATION'):
                equation = line.replace('EQUATION', '').strip()
                return equation
        return None

    def print_results(self, results):
        """Pretty print results"""
        print("\n" + "="*60)
        print(f"METABOLIC PRINCIPLES: {results['pathway']}")
        print("="*60)

        print("\n1. RATE-LIMITING STEPS")
        print("-" * 60)
        for step in results['principles']['rate_limiting_steps']:
            print(f"  • {step['reaction']}")
            print(f"    ΔG°' = {step['dG']:.1f} kJ/mol")
            print(f"    {step['reason']}")
            print()

        print("\n2. ENERGY COUPLING")
        print("-" * 60)
        for coupling in results['principles']['energy_coupling']:
            print(f"  • {coupling['reaction']}")
            print(f"    {coupling['equation']}")
            print(f"    {coupling['principle']}")
            print()

        print("\n3. FEEDBACK PATTERNS")
        print("-" * 60)
        for pattern in results['principles']['feedback_inhibition']['known_feedback']:
            print(f"  • {pattern['pattern']}")
            print(f"    Type: {pattern['type']}")
            print()

# Usage
if __name__ == "__main__":
    extractor = MetabolicPatternExtractor()
    results = extractor.analyze_pathway("Glycolysis")
    extractor.print_results(results)
```

---

## Conclusion

This guide provides API access methods and strategies for extracting **PRINCIPLES and PATTERNS** from metabolic databases, avoiding exhaustive data downloads of hundreds of thousands of metabolites.

### Key Takeaways:

1. **Query by hierarchy**: Use functional categories, pathways, and modules instead of individual metabolites
2. **Integrate databases**: Combine strengths (KEGG topology + eQuilibrator thermodynamics + Reactome regulation)
3. **Focus on patterns**: Look for feedback loops, energy coupling, rate-limiting steps
4. **Use specialized tools**: eQuilibrator for thermodynamics, ChEBI for roles, KEGG for topology
5. **Extract principles**: Flow rules, constraints, regulation mechanisms, not exhaustive lists

### Database Selection Guide:

- **Free thermodynamics**: eQuilibrator (best choice)
- **Free pathway topology**: KEGG (academic only)
- **Free regulation**: Reactome
- **Detailed kinetics**: MetaCyc (requires subscription)
- **Metabolite classification**: ChEBI (free, ontology-based)
- **Clinical context**: HMDB (free web access)

---

## Sources

- [HMDB API](https://hmdb.ca/simple/api)
- [HMDB Downloads](https://www.hmdb.ca/downloads)
- [ChEBI Web Services](https://www.ebi.ac.uk/chebi/webServices.do)
- [ChEBI 2.0 API Documentation](https://www.ebi.ac.uk/chebi/backend/api/docs/)
- [libChEBI API](https://jcheminf.biomedcentral.com/articles/10.1186/s13321-016-0123-9)
- [KEGG API Manual](https://www.kegg.jp/kegg/rest/keggapi.html)
- [KEGG MODULE Database](https://www.genome.jp/kegg/module.html)
- [KEGG REACTION Database](https://www.genome.jp/kegg/reaction/)
- [Reactome Content Service](https://reactome.org/dev/content-service)
- [Reactome ContentService API](https://reactome.org/ContentService/)
- [BioCyc Web Services](https://biocyc.org/web-services.shtml)
- [MetaCyc SmartTables](https://metacyc.org/smarttables)
- [MetaCyc User Guide](https://metacyc.org/MetaCycUserGuide.shtml)
- [eQuilibrator](https://equilibrator.weizmann.ac.il/)
- [eQuilibrator 3.0 Documentation](https://pmc.ncbi.nlm.nih.gov/articles/PMC8728285/)
- [eQuilibrator API Tutorial](https://equilibrator.readthedocs.io/en/latest/tutorial.html)
