# Protein/Enzyme Database API Access Guide

**Focus**: Extracting family-level patterns, catalytic mechanisms, and modular architectures—NOT individual sequences

**Target Scale**: ~6k EC numbers, protein domain architectures, regulation patterns, catalytic strategies

---

## 1. EC (Enzyme Commission) - BRENDA Database

### Overview
BRENDA (BRaunschweig ENzyme DAtabase) is the world's most comprehensive enzyme database with ~5.8 million data points on 112,288 enzymes from 15,335 organisms, containing 8,226+ unique EC numbers.

### Primary API Endpoints

#### SPARQL Endpoint (Recommended for Semantic Queries)
- **URL**: `https://sparql.dsmz.de/brenda`
- **Format**: SPARQL queries → RDF/JSON/XML
- **Authentication**: None required for public SPARQL endpoint
- **Scale**: 10,798,737 RDF triples

#### SOAP API (Comprehensive Data Access)
- **URL**: `https://www.brenda-enzymes.org/` (SOAP web service)
- **Format**: SOAP/XML
- **Authentication**: **REQUIRED**
  - Email address + SHA256 hashed password
  - Must register at brenda-enzymes.org
- **Coverage**: 50+ data fields, 150+ remote methods

### Data Formats
- **SPARQL**: RDF/Turtle, JSON-LD, XML
- **SOAP**: XML responses
- **Download**: Text files, SBML

### Key Entity Types for Family-Level Extraction

#### 1. **Enzyme Classes (EC Hierarchy)**
- **Entity**: `EnzymeClass` (RDF type in SPARQL)
- 6 major classes, 4-level hierarchy (e.g., EC 3.1.1.34)
- **Fields**: EC number, systematic name, recommended name, reaction, cofactors

#### 2. **Catalytic Mechanisms**
- Covalent catalysis
- Acid-base catalysis
- Metal-aided catalysis
- Integration with M-CSA (Mechanism of Catalyzed Structural Activity) database

#### 3. **Allosteric Regulation**
- **Entities**: `Activator`, `Inhibitor`
- Regulatory cofactors and effectors
- Available through SOAP API data fields

#### 4. **Reaction Mechanisms**
- **Entity**: `Reaction` (RDF type)
- Substrate → Product transformations
- Catalytic strategies as computational operators

#### 5. **Cofactors and Coenzymes**
- **Entity**: `Cofactor`, `Compound`
- Essential for mechanism classification

### Example API Calls

#### SPARQL Example 1: List All EC Classes
```sparql
PREFIX brenda: <http://brenda-enzymes.org/ontology#>

SELECT ?ecNumber ?name
WHERE {
  ?enzyme a brenda:EnzymeClass ;
          brenda:ecNumber ?ecNumber ;
          brenda:recommendedName ?name .
}
LIMIT 6000
```

#### SPARQL Example 2: Get Catalytic Mechanisms by EC Class
```sparql
PREFIX brenda: <http://brenda-enzymes.org/ontology#>

SELECT ?ecNumber ?reaction ?cofactor ?mechanism
WHERE {
  ?enzyme brenda:ecNumber ?ecNumber ;
          brenda:catalyzes ?reaction .
  OPTIONAL { ?enzyme brenda:requiresCofactor ?cofactor }
  OPTIONAL { ?enzyme brenda:catalyticMechanism ?mechanism }
}
```

#### SOAP Example (Python with Zeep)
```python
from zeep import Client
import hashlib

# Authentication
email = "your@email.com"
password = hashlib.sha256("yourpassword".encode()).hexdigest()

wsdl = "https://www.brenda-enzymes.org/soap/brenda_zeep.wsdl"
client = Client(wsdl)

# Get all EC numbers with oxidoreductase mechanism (EC 1.x.x.x)
ec_numbers = client.service.getEcNumber(email, password, "ecNumber=1.*")

# Get catalytic mechanisms for specific EC
mechanisms = client.service.getCatalyticActivity(email, password, "ecNumber=3.4.21.4")
```

### Filtering Strategies: Family-Level NOT Individual Sequences

1. **Query by EC Hierarchy Level**
   - EC 1.*.*.* (all oxidoreductases) → ~1,000 families
   - EC 3.4.*.* (all peptidases) → ~500 families
   - Avoid querying individual proteins

2. **Filter by Catalytic Strategy**
   - Use SPARQL to group by mechanism type
   - Extract reaction patterns, not protein instances

3. **Aggregate by Cofactor Requirements**
   - Group enzymes by cofactor dependencies (NAD+, FAD, metal ions)
   - Extract catalytic strategies as computational rules

4. **Download Complete EC Hierarchy**
   - Use SPARQL endpoint to get all ~6k EC numbers
   - Parse reaction mechanisms locally

---

## 2. UniProt - Protein Sequences and Annotations

### Overview
UniProt provides comprehensive protein sequence and functional information, including protein families, domains, and functional annotations. Focus on family-level data, NOT 200M+ individual sequences.

### Primary API Endpoints

#### REST API (Recommended)
- **Base URL**: `https://rest.uniprot.org/`
- **Endpoints**:
  - `/uniprotkb/search` - Search with filters
  - `/uniprotkb/stream` - Streaming for large datasets
  - `/uniref/` - UniRef protein clusters (family representatives)
  - `/uniparc/` - UniParc sequence archive
- **Format**: JSON, TSV, FASTA, XML, RDF
- **Authentication**: None required (rate limits apply)

#### SPARQL Endpoint
- **URL**: `https://sparql.uniprot.org/`
- **Format**: SPARQL → RDF/JSON

#### EBI Proteins API
- **Base URL**: `https://www.ebi.ac.uk/proteins/api/`
- **Focus**: Sequence features, domains, annotations

### Data Formats
- JSON (default, recommended)
- TSV (tabular)
- XML
- RDF/Turtle
- FASTA (sequences)

### Key Entity Types for Family-Level Extraction

#### 1. **Protein Families (NOT Individual Sequences)**
- **Query Field**: `family`
- **Cross-reference**: `xref_pfam`, `xref_interpro`
- **Filter Strategy**: Query by Pfam/InterPro accessions

#### 2. **Functional Domains and Motifs**
- **Features**: Active sites, binding sites, regions, domains
- **API**: EBI Proteins API `/features` endpoint

#### 3. **Catalytic Mechanisms**
- **Fields**: `cc_catalytic_activity`, `ft_act_site`
- Active site residues and catalytic mechanisms

#### 4. **Allosteric Regulation**
- **Fields**: `ft_binding`, `ft_region`, `cc_function`
- Regulatory sites and functional annotations

#### 5. **Domain Architectures**
- Positional features: domains, repeats, motifs
- Multi-domain protein organization

### Example API Calls

#### REST Example 1: Get All Proteins with Specific Pfam Domain
```bash
# Query proteins containing Kinase domain (PF00069)
curl "https://rest.uniprot.org/uniprotkb/search?query=xref_pfam:PF00069&format=json&size=500"
```

#### REST Example 2: Get Protein Family Representatives (UniRef90)
```bash
# Get UniRef90 clusters (90% identity representatives)
curl "https://rest.uniprot.org/uniref/search?query=taxonomy_id:9606&format=json&size=500"
```

#### REST Example 3: Filter by Catalytic Activity
```bash
# Get all serine proteases (EC 3.4.21.*) annotations
curl "https://rest.uniprot.org/uniprotkb/search?query=ec:3.4.21.*&fields=accession,protein_name,ec,cc_catalytic_activity&format=tsv"
```

#### REST Example 4: Get Domain Features for Protein Family
```bash
# Get domain architecture for proteins with both Kinase and SH2 domains
curl "https://rest.uniprot.org/uniprotkb/search?query=(xref_pfam:PF00069)+AND+(xref_pfam:PF00017)&fields=accession,protein_name,ft_domain&format=json"
```

#### Python Example Using Requests
```python
import requests

# Search for protein families with specific domain
url = "https://rest.uniprot.org/uniprotkb/search"
params = {
    "query": "xref_pfam:PF00069",  # Kinase domain
    "fields": "accession,protein_name,ft_domain,cc_function,xref_pfam",
    "format": "json",
    "size": 500
}

response = requests.get(url, params=params)
data = response.json()

# Extract domain architectures
for entry in data['results']:
    print(f"{entry['primaryAccession']}: {entry.get('features', [])}")
```

### Filtering Strategies: Families NOT Sequences

1. **Use UniRef Clusters (Family Representatives)**
   - UniRef100: Identical sequences → single representative
   - UniRef90: 90% identity clusters → ~10x reduction
   - UniRef50: 50% identity clusters → ~100x reduction
   - **Endpoint**: `/uniref/search?query=identity:0.9`

2. **Query by Protein Family Cross-References**
   ```
   xref_pfam:PF00001         # Specific Pfam family
   xref_interpro:IPR000001   # Specific InterPro entry
   xref_panther:PTHR10000    # PANTHER family
   ```

3. **Filter by Functional Annotation, NOT Sequence**
   ```
   cc_function:kinase        # Functional annotation
   ec:2.7.*.*                # All kinases by EC number
   ft_act_site:*             # Has annotated active site
   ```

4. **Extract Domain Architectures**
   - Query: `(xref_pfam:PF00001)+AND+(xref_pfam:PF00002)`
   - Returns proteins with specific domain combinations
   - Identifies modular architectures

5. **Use return_fields Parameter**
   ```
   fields=accession,protein_name,ft_domain,xref_pfam,cc_catalytic_activity
   ```
   - Avoid downloading full sequences
   - Get only family/domain annotations

6. **Taxonomic Filtering for Model Organisms**
   ```
   taxonomy_id:9606          # Human only
   taxonomy_id:2759          # Eukaryotes
   reviewed:true             # Swiss-Prot (curated only)
   ```

---

## 3. InterPro - Protein Families, Domains, and Motifs

### Overview
InterPro is an integrated database of protein families, domains, and functional sites, combining signatures from 13 member databases (including Pfam, SMART, PROSITE, etc.). **Ideal for domain architecture analysis.**

### Primary API Endpoints

#### REST API
- **Base URL**: `https://www.ebi.ac.uk/interpro/api/`
- **Main Endpoints**:
  - `/entry` - InterPro entries (families, domains, motifs)
  - `/protein` - Protein matches
  - `/structure` - 3D structures
  - `/taxonomy` - Taxonomic distribution
  - `/proteome` - Proteome coverage
  - `/set` - Entry sets (e.g., domain architectures)
- **Format**: JSON (default)
- **Authentication**: None required

#### GitHub API Documentation
- **Repo**: https://github.com/ProteinsWebTeam/interpro7-api
- **Docs**: https://github.com/ProteinsWebTeam/interpro7-api/blob/master/docs/README.md

### Data Formats
- JSON (default, structured metadata)
- TSV (via script generator)
- FASTA (sequence export)

### Key Entity Types for Family-Level Extraction

#### 1. **Protein Families**
- **Type**: `family` entries
- Homologous proteins with shared ancestry
- **Example**: IPR036859 (Immunoglobulin-like domain)

#### 2. **Functional Domains**
- **Type**: `domain` entries
- Distinct structural/functional units
- Modular components of multi-domain proteins
- **Example**: IPR000719 (Protein kinase domain)

#### 3. **Motifs and Sites**
- **Types**: `site`, `conserved_site`, `active_site`, `binding_site`
- Short conserved sequences
- **Example**: IPR017441 (Protein kinase, ATP binding site)

#### 4. **Domain Architectures**
- **Endpoint**: `/entry/{db}/{acc}/domain_architecture/`
- Modular organization of domains
- Protein architecture patterns

#### 5. **Homologous Superfamilies**
- **Type**: `homologous_superfamily`
- Evolutionarily related protein structures
- **Example**: IPR011009 (Protein kinase-like domain)

### Example API Calls

#### Example 1: Get All InterPro Entries of Type "Domain"
```bash
curl "https://www.ebi.ac.uk/interpro/api/entry/interpro?type=domain&page_size=200"
```

#### Example 2: Get Specific InterPro Entry Metadata
```bash
# Kinase domain (IPR000719)
curl "https://www.ebi.ac.uk/interpro/api/entry/interpro/IPR000719"
```

Response includes:
- Accession, name, type
- Member database signatures (Pfam, SMART, etc.)
- GO terms, pathways
- Taxonomic distribution

#### Example 3: Get Domain Architectures for Pfam Family
```bash
# Get all domain architectures containing Pfam Kinase domain
curl "https://www.ebi.ac.uk/interpro/api/entry/pfam/PF00069/domain_architecture/"
```

Returns:
- Domain architecture IDs
- Domain composition (ordered list)
- Protein counts for each architecture

#### Example 4: Get All Pfam Families via InterPro
```bash
curl "https://www.ebi.ac.uk/interpro/api/entry/pfam?page_size=200"
```

Returns ~19,632 Pfam families with:
- Pfam accession (PF#####)
- Family name
- Integrated InterPro ID

#### Example 5: Search Entries by Name
```bash
curl "https://www.ebi.ac.uk/interpro/api/entry/all?search=kinase&type=domain"
```

#### Example 6: Get Domain Architecture with Specific Domains
```bash
# Proteins with both SH2 and Kinase domains
curl "https://www.ebi.ac.uk/interpro/api/entry/interpro?ida_search=IPR000719,IPR000980"
```

#### Python Example: Extract Domain Architectures
```python
import requests

# Get domain architectures for multi-domain proteins
url = "https://www.ebi.ac.uk/interpro/api/entry/pfam/PF00069/domain_architecture/"
response = requests.get(url)
data = response.json()

# Parse domain architectures
for arch in data['results']:
    domains = arch['ida']  # Ordered list of domain accessions
    count = arch['counts']['proteins']
    print(f"Architecture: {' + '.join(domains)}, Proteins: {count}")
```

### Filtering Strategies: Modular Patterns NOT Sequences

#### 1. **Query by Entry Type**
```
/entry/interpro?type=domain          # Domains only (~5,000)
/entry/interpro?type=family          # Families only (~15,000)
/entry/interpro?type=conserved_site  # Catalytic/binding sites
```

#### 2. **Use Member Database Filtering**
```
/entry/pfam/           # Pfam families only (~19,632)
/entry/smart/          # SMART domains
/entry/prosite/        # PROSITE patterns
/entry/panther/        # PANTHER families
```

#### 3. **Domain Architecture Search (IDA)**
- **Parameter**: `ida_search`
- Finds proteins with specific domain combinations
- **Example**: `ida_search=IPR000719,IPR000980` (SH2 + Kinase)
- **Exclude domains**: `ida_ignore=IPR000001`

#### 4. **Filter by Protein Count Threshold**
- Focus on architectures with ≥10 proteins
- Excludes rare/singleton architectures
- Extract via `/domain_architecture/` endpoint, filter by `counts.proteins`

#### 5. **Taxonomic Filtering**
```
/entry/interpro/IPR000719/taxonomy/uniprot/2759  # Eukaryotes only
```

#### 6. **Get Representative Structures**
```
/entry/interpro/IPR000719/structure/  # PDB structures for this domain
```

#### 7. **Extract GO Terms and Pathways**
```json
{
  "metadata": {
    "go_terms": [...],  // Molecular function, biological process
    "pathways": [...]   // MetaCyc, Reactome, KEGG
  }
}
```

---

## 4. Pfam - Protein Family Classifications

### Overview
Pfam database of protein families is now **hosted by InterPro** (as of 2021+). Contains 19,632+ protein families based on seed alignments and HMMs. Access via InterPro API.

### Primary API Endpoints

#### InterPro REST API (Pfam Integration)
- **Base URL**: `https://www.ebi.ac.uk/interpro/api/entry/pfam/`
- **Format**: JSON
- **Authentication**: None required

#### Official Pfam Documentation
- **Docs**: https://pfam-docs.readthedocs.io/en/latest/api.html

### Data Formats
- JSON (metadata, annotations)
- Stockholm format (alignments, via download)
- HMM profiles (via download)

### Key Entity Types for Family-Level Extraction

#### 1. **Protein Families**
- **Pfam-A**: 19,632+ curated families
- Each family: Pfam accession (PF#####), name, description
- Seed alignment, HMM profile

#### 2. **Clans (Superfamilies)**
- **Clan**: Group of related families
- Shared evolutionary origin
- **Example**: CL0016 (Protein kinase-like superfamily)

#### 3. **Domain Architectures**
- Multi-domain protein organization
- Accessible via `/domain_architecture/` endpoint

#### 4. **Functional Classification**
- GO terms, EC numbers
- Catalytic residues, binding sites

### Example API Calls

#### Example 1: List All Pfam Families
```bash
curl "https://www.ebi.ac.uk/interpro/api/entry/pfam?page_size=200"
```

Returns:
```json
{
  "count": 19632,
  "results": [
    {
      "metadata": {
        "accession": "PF00001",
        "name": "7tm_1",
        "type": "family",
        "source_database": "pfam",
        "integrated": "IPR000276"
      }
    }
  ]
}
```

#### Example 2: Get Specific Pfam Family Details
```bash
curl "https://www.ebi.ac.uk/interpro/api/entry/pfam/PF00069"
```

Returns:
- Family name: "Protein kinase domain"
- InterPro integration: IPR000719
- Member count, taxonomic distribution
- GO terms, EC numbers

#### Example 3: Get Domain Architectures for Pfam Family
```bash
curl "https://www.ebi.ac.uk/interpro/api/entry/pfam/PF00069/domain_architecture/"
```

Returns all multi-domain architectures containing PF00069 (Kinase).

#### Example 4: Search Pfam Families by Name
```bash
curl "https://www.ebi.ac.uk/interpro/api/entry/pfam?search=kinase"
```

#### Example 5: Get Pfam Clan Information
```bash
# Get all families in Kinase clan
curl "https://www.ebi.ac.uk/interpro/api/set/pfam/CL0016"
```

#### Python Example: Extract Catalytic Domains
```python
import requests

# Get all Pfam families with EC numbers (enzymes)
url = "https://www.ebi.ac.uk/interpro/api/entry/pfam"
params = {"page_size": 200}

response = requests.get(url, params=params)
data = response.json()

enzyme_families = []
for entry in data['results']:
    metadata = entry['metadata']
    if 'ec' in metadata:
        enzyme_families.append({
            'pfam_id': metadata['accession'],
            'name': metadata['name'],
            'ec_numbers': metadata['ec']
        })

print(f"Found {len(enzyme_families)} enzyme families")
```

### Filtering Strategies: Family-Level Patterns

#### 1. **Query by Pfam Accession Range**
- PF00001-PF19632 (all families)
- Use pagination: `page_size=200`

#### 2. **Filter by Type**
```
type=family          # Pfam-A families only
type=domain          # If integrated into InterPro as domain
```

#### 3. **Use Clan Groupings**
- Get all families in a clan (superfamily)
- `/set/pfam/CL#####`
- Reduces redundancy, groups by evolutionary relationship

#### 4. **Filter by Functional Annotation**
- Search for families with GO terms: `go_terms`
- Filter by EC number: `ec`
- Catalytic families only

#### 5. **Domain Architecture Analysis**
- Focus on multi-domain proteins
- Extract modular combinations
- `/domain_architecture/` endpoint → filter by protein count

#### 6. **Taxonomic Scope**
```
/entry/pfam/PF00069/taxonomy/  # Taxonomic distribution
```
- Focus on widely distributed families (>100 species)

---

## 5. IUPHAR - Guide to Pharmacology (Receptors, Channels, Transporters)

### Overview
IUPHAR/BPS Guide to PHARMACOLOGY provides expert-curated data on drug targets including GPCRs, ion channels, nuclear receptors, enzymes, transporters. **Organized by family classification.**

### Primary API Endpoints

#### REST Web Services
- **Base URL**: `https://www.guidetopharmacology.org/services/`
- **Format**: JSON
- **Authentication**: None required

#### Web Services Documentation
- **URL**: https://www.guidetopharmacology.org/webServices.jsp

### Data Formats
- JSON (default)
- XML (available for some endpoints)

### Key Entity Types for Family-Level Extraction

#### 1. **Target Families**
- GPCRs (G protein-coupled receptors)
- Ion channels (voltage-gated, ligand-gated)
- Nuclear receptors
- Enzymes (kinases, proteases, etc.)
- Transporters (SLC, ABC families)
- Catalytic receptors

#### 2. **Receptor/Channel Types**
- **GPCRs**: Class A, B, C, F (organized by family)
- **Ion Channels**: Voltage-gated (Na+, K+, Ca2+, Cl-), ligand-gated (nAChR, GABA, glutamate)
- **Transporters**: SLC superfamily, ABC transporters

#### 3. **Gating Mechanisms**
- Voltage-dependent activation
- Ligand-dependent activation
- Mechanosensitive gating
- Temperature-sensitive (TRP channels)

#### 4. **Allosteric Regulation**
- Allosteric modulators (PAMs, NAMs)
- Regulatory binding sites
- G protein coupling patterns

#### 5. **Pharmacological Properties**
- Endogenous ligands
- Agonists, antagonists, modulators
- Binding affinity data (pKi, pKd, pIC50)

### Example API Calls

#### Example 1: Get All Target Families
```bash
curl "https://www.guidetopharmacology.org/services/families"
```

Returns list of target families with:
- Family ID, name, type
- Parent family (hierarchical)
- Target count

#### Example 2: Get All Targets in a Family
```bash
# Get all GPCRs (family ID = 1)
curl "https://www.guidetopharmacology.org/services/families/1/targets"
```

#### Example 3: Get Specific Target Details
```bash
# Get target ID 290 (5-HT2A receptor)
curl "https://www.guidetopharmacology.org/services/targets/290"
```

Returns:
- Target name, family, type
- Gene name, UniProt ID
- Subunit composition
- Gating mechanism
- Endogenous ligands

#### Example 4: Get Ligand Interactions for Target
```bash
# Get interactions for target 290 with pKi values
curl "https://www.guidetopharmacology.org/services/targets/290/interactions?affinityType=pKi&species=Human"
```

Parameters:
- `affinityType`: pKi, pKd, pIC50, pEC50
- `species`: Human, Rat, Mouse
- Returns binding affinity data

#### Example 5: Get All Voltage-Gated Ion Channels
```bash
# Family ID 78 = Voltage-gated ion channels
curl "https://www.guidetopharmacology.org/services/families/78/targets"
```

#### Example 6: Get GPCR Families Hierarchically
```bash
curl "https://www.guidetopharmacology.org/services/families?type=GPCR"
```

#### Python Example: Extract Receptor Family Architecture
```python
import requests

# Get all GPCRs organized by subfamily
base_url = "https://www.guidetopharmacology.org/services"

# Get GPCR family tree
families_response = requests.get(f"{base_url}/families")
families = families_response.json()

gpcr_families = [f for f in families if f.get('type') == 'GPCR']

for family in gpcr_families:
    family_id = family['familyId']
    family_name = family['name']

    # Get targets in this family
    targets_response = requests.get(f"{base_url}/families/{family_id}/targets")
    targets = targets_response.json()

    print(f"\n{family_name} ({len(targets)} targets)")
    for target in targets[:5]:  # First 5 examples
        print(f"  - {target['name']} (Gene: {target.get('geneSymbol', 'N/A')})")
```

### Filtering Strategies: Family-Level NOT Individual Proteins

#### 1. **Query by Target Family Type**
```
/services/families?type=GPCR           # All GPCR families
/services/families?type=IC             # All ion channels
/services/families?type=NHR            # Nuclear hormone receptors
/services/families?type=Transporter    # All transporters
/services/families?type=Enzyme         # Enzyme targets
```

#### 2. **Hierarchical Family Navigation**
- Parent families → subfamilies → individual targets
- Example: GPCRs → Class A → Aminergic → Serotonin → 5-HT subtypes

#### 3. **Filter Targets by Functional Properties**
- Gating mechanism (voltage, ligand, mechanical)
- G protein coupling (Gs, Gi, Gq)
- Ion selectivity (Na+, K+, Ca2+, Cl-)

#### 4. **Extract Pharmacological Rules**
- Common binding sites across family
- Conserved gating residues
- Allosteric modulator patterns

#### 5. **Use Gene Symbol Mapping**
- Map to UniProt for cross-database integration
- Example: `/services/targets/{id}` returns `uniprotId`

#### 6. **Focus on Curated Target Families**
- Exclude orphan receptors (unknown ligands)
- Filter by clinical relevance (has approved drugs)

#### 7. **Download Bulk Data**
- Full database downloads available at:
  https://www.guidetopharmacology.org/download.jsp
- CSV/TSV formats for local processing

---

## Summary: Extraction Strategy for Computational Biology

### Recommended Workflow

1. **EC Numbers & Catalytic Mechanisms** (~6k classes)
   - **Source**: BRENDA SPARQL endpoint
   - **Extract**: EC hierarchy, reaction mechanisms, cofactors
   - **Strategy**: SPARQL query for all EnzymeClass entities
   - **Output**: Catalytic strategies as computational operators

2. **Protein Domain Architectures** (modular patterns)
   - **Source**: InterPro API `/domain_architecture/` endpoint
   - **Extract**: Multi-domain combinations, domain order
   - **Strategy**: Query by domain type, filter by protein count ≥10
   - **Output**: Modularity rules (domain X + domain Y → function Z)

3. **Protein Families** (~20k Pfam families)
   - **Source**: InterPro API `/entry/pfam/`
   - **Extract**: Family HMMs, functional annotations, GO terms
   - **Strategy**: Iterate through Pfam accessions, extract metadata
   - **Output**: Family-level functional signatures

4. **Allosteric Regulation Patterns**
   - **Source**: BRENDA SOAP API (Activator/Inhibitor entities)
   - **Extract**: Regulatory cofactors, effector binding sites
   - **Strategy**: Query by enzyme class, extract allosteric modulators
   - **Output**: Regulation rules (effector → conformational change)

5. **Gating Mechanisms** (channels/receptors)
   - **Source**: IUPHAR API `/services/targets/`
   - **Extract**: Gating mechanisms, ion selectivity, modulation
   - **Strategy**: Filter by ion channel families, extract gating properties
   - **Output**: Gating logic (voltage → open/closed states)

6. **Catalytic Residues & Active Sites**
   - **Source**: UniProt API + InterPro conserved sites
   - **Extract**: Active site motifs, catalytic triads, metal binding
   - **Strategy**: Query `ft_act_site`, `ft_binding` features
   - **Output**: Catalytic strategies as amino acid patterns

### Key Principles

- **Avoid Individual Sequences**: Use family accessions, EC numbers, UniRef clusters
- **Focus on Patterns**: Domain architectures, catalytic mechanisms, regulation rules
- **Leverage Cross-References**: Map between databases (Pfam ↔ InterPro ↔ UniProt)
- **Hierarchical Queries**: Start broad (EC 3.*), narrow down (EC 3.4.21.*)
- **Batch Extraction**: Use API pagination, SPARQL queries, bulk downloads

### Data Integration Points

| Database | Primary Key | Cross-Reference To |
|----------|-------------|-------------------|
| BRENDA   | EC Number   | UniProt (DR field), MetaCyc |
| UniProt  | Accession   | Pfam (xref_pfam), InterPro, EC |
| InterPro | IPR ID      | Pfam, UniProt, PDB, GO |
| Pfam     | PF ID       | InterPro (integrated), UniProt |
| IUPHAR   | Target ID   | UniProt (uniprotId), Gene Symbol |

---

## Sources

### EC/BRENDA
- [BRENDA Enzyme Database](https://www.brenda-enzymes.org/)
- [BRENDA in 2026 - NAR](https://academic.oup.com/nar/advance-article/doi/10.1093/nar/gkaf1113/8315798)
- [BRENDA SOAP Access Help](https://www.brenda-enzymes.org/soap.php)
- [Expasy ENZYME Database](https://enzyme.expasy.org/)
- [ENZYME FTP Download](https://ftp.expasy.org/databases/enzyme/)

### UniProt
- [UniProt Website API Documentation](https://www.uniprot.org/api-documentation/uniprotkb)
- [UniProt website API - NAR 2025](https://academic.oup.com/nar/advance-article/doi/10.1093/nar/gkaf394/8126256)
- [UniProt Programmatic Access](https://www.uniprot.org/help/programmatic_access)
- [UniProt Query Fields](https://www.uniprot.org/help/query-fields)
- [EBI Proteins API](https://www.ebi.ac.uk/proteins/api/doc/)

### InterPro
- [InterPro API](https://www.ebi.ac.uk/interpro/api/)
- [InterPro API GitHub Documentation](https://github.com/ProteinsWebTeam/interpro7-api/blob/master/docs/README.md)
- [InterPro protein families database - NAR 2021](https://academic.oup.com/nar/article/49/D1/D344/5958491)
- [InterPro in 2025 - NAR](https://academic.oup.com/nar/article/53/D1/D444/7905301)
- [InterPro Domain Architecture Tool](https://www.ebi.ac.uk/interpro/search/ida/)

### Pfam
- [Pfam is now hosted by InterPro](http://pfam.xfam.org/)
- [Querying Pfam using InterPro API - Pfam Docs](https://pfam-docs.readthedocs.io/en/latest/api.html)
- [Pfam protein families database - NAR 2021](https://academic.oup.com/nar/article/49/D1/D412/5943818)
- [Pfam embracing AI/ML - NAR 2025](https://academic.oup.com/nar/article/53/D1/D523/7900195)

### IUPHAR
- [IUPHAR/BPS Guide to PHARMACOLOGY](https://www.guidetopharmacology.org/)
- [IUPHAR Web Services](https://www.guidetopharmacology.org/webServices.jsp)
- [IUPHAR/BPS Guide to PHARMACOLOGY in 2024 - NAR](https://academic.oup.com/nar/article/52/D1/D1438/7332061)
- [IUPHAR Targets Page](https://www.guidetopharmacology.org/targets.jsp)
- [IUPHAR GPCR Families](https://www.guidetopharmacology.org/GRAC/ReceptorFamiliesForward?type=GPCR)

---

**Document Version**: 1.0
**Last Updated**: 2025-12-10
**Focus**: Family-level patterns, mechanisms, and modular architectures for computational biology
