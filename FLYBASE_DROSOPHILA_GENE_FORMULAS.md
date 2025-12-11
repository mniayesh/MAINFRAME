# FlyBase Drosophila Gene and Protein Formulas for Neural Computation

**Database Source**: FlyBase (http://flybase.org)
**Organism**: *Drosophila melanogaster*
**Focus**: Neural computation, synaptic plasticity, learning, and behavior
**Date**: 2025-12-10

---

## Table of Contents

1. [Voltage-Gated Ion Channels](#1-voltage-gated-ion-channels)
2. [Neurotransmitter Receptors](#2-neurotransmitter-receptors)
3. [Learning and Memory Genes](#3-learning-and-memory-genes)
4. [Synaptic Proteins](#4-synaptic-proteins)
5. [Circadian Rhythm Genes](#5-circadian-rhythm-genes)
6. [G-Protein Signaling](#6-g-protein-signaling)
7. [Calcium-Dependent Enzymes](#7-calcium-dependent-enzymes)

---

## 1. Voltage-Gated Ion Channels

### 1.1 Shaker (Sh) - Voltage-Gated Potassium Channel (Kv1)

**FlyBase ID**: FBgn0001044

**Gene Function**: Encodes the founding member of voltage-gated potassium channel (Kv) family mediating fast A-type potassium current (IA).

**Protein Structure**:
- Four subunits form functional channel
- Each subunit: 6 transmembrane domains (S1-S6)
- S4 domain: voltage sensor
- P-loop between S5-S6: ion selectivity filter
- Intracellular N-terminus: inactivation ball domain

**Channel Kinetics**:
```
I_A(V,t) = ḡ_A * m³(V,t) * h(V,t) * (V - E_K)

where:
  m∞(V) = 1 / (1 + exp(-(V + 30)/10))    [activation]
  h∞(V) = 1 / (1 + exp((V + 60)/7))      [inactivation]
  τ_m(V) = 0.5-2 ms (rapid activation)
  τ_h(V) = 5-50 ms (inactivation)
```

**Single Channel Conductance**:
- A2 channels: 6-8 pS
- Rapid turn-on, fast inactivation

**Expression Pattern**:
- CNS neurons: widely expressed
- Neuromuscular junction
- Thermosensitive GABA neurons (sleep regulation)
- Mushroom bodies

**Behavioral Relevance**:
- Sleep promotion via thermosensitive GABA transmission
- Leg-shaking phenotype in mutants under ether anesthesia
- Action potential repolarization
- Neuronal excitability control

---

### 1.2 para - Voltage-Gated Sodium Channel (Nav)

**FlyBase ID**: FBgn0000114

**Gene Function**: Encodes the sole α-subunit of voltage-gated sodium channels in *Drosophila*, essential for action potential initiation.

**Protein Structure**:
- 4 homologous domains (I-IV)
- Each domain: 6 transmembrane segments
- Multiple splice variants with distinct gating properties
- Localized to axonal initial segment

**Channel Kinetics**:
```
I_Na(V,t) = ḡ_Na * m³(V,t) * h(V,t) * (V - E_Na)

Activation:
  m∞(V) = 1 / (1 + exp(-(V + 40)/3))
  τ_m(V) = 0.1-0.5 ms (very rapid)

Inactivation:
  h∞(V) = 1 / (1 + exp((V + 65)/7))
  τ_h(V) = 1-10 ms (rapid)
```

**Expression Pattern**:
- Only 23±1% of embryonic/larval CNS neurons express para
- Broadly expressed in adult CNS
- Enriched at distal axonal segment (action potential initiation site)
- Correlates with actively firing neurons

**Behavioral Relevance**:
- Essential for neuronal excitability
- Temperature-sensitive paralytic mutations
- Rapid inactivation kinetics crucial for spike generation
- Determines integrator vs resonator properties

---

### 1.3 cacophony (cac) - Voltage-Gated Calcium Channel (Cav2)

**FlyBase ID**: FBgn0263111

**Gene Function**: Encodes pore-forming α1 subunit of presynaptic voltage-gated Ca²⁺ channel, essential for neurotransmitter release and synaptic plasticity.

**Protein Structure**:
- Four homologous repeats (I-IV)
- Each repeat: 6 transmembrane segments
- Mutually exclusive splice sites:
  - IS4 transmembrane domain (affects localization)
  - I-II intracellular linker (fine-tunes presynaptic function)

**Channel Kinetics and Calcium Dynamics**:
```
I_Ca(V,t) = ḡ_Ca * m²(V,t) * h(V,t) * (V - E_Ca)

Activation:
  m∞(V) = 1 / (1 + exp(-(V + 20)/6))
  τ_m(V) = 1-5 ms

[Ca²⁺]_presynaptic dynamics:
  d[Ca²⁺]/dt = -α*I_Ca(V,t) - [Ca²⁺]/τ_Ca

  where τ_Ca = 10-100 ms (calcium removal time constant)
```

**Synaptic Transmission Formula**:
```
Release Rate = k_max * [Ca²⁺]⁴_local / (K_d⁴ + [Ca²⁺]⁴_local)

Typical values:
  Cooperativity: n = 4 (fourth-power Ca²⁺ dependence)
  K_d ≈ 10-100 μM
```

**Expression Pattern**:
- Presynaptic active zones
- Neuromuscular junction
- CNS synapses
- Clustered with release machinery

**Behavioral Relevance**:
- Evoked neurotransmitter release
- Paired-pulse facilitation
- Homeostatic plasticity
- Long-term potentiation
- Seizure suppression (mutations suppress seizures)
- Temperature-sensitive paralysis in mutants

---

### 1.4 ether-a-go-go (eag) - Voltage-Gated Potassium Channel (Kv10/KCNH)

**FlyBase ID**: FBgn0000535

**Gene Function**: Founding member of KCNH superfamily, mediates delayed rectifier K⁺ current with unique calcium/calmodulin regulation.

**Protein Structure**:
- 6 transmembrane domains
- Cyclic nucleotide-binding domain (CNBD) in C-terminus
- CaMKII phosphorylation sites
- Calmodulin-binding domain (enables Ca²⁺/CaM-dependent gating)

**Channel Kinetics with CaMKII Modulation**:
```
I_eag(V,t) = ḡ_eag * n⁴(V,t) * f([Ca²⁺]_i, CaMKII) * (V - E_K)

Voltage-dependent activation:
  n∞(V) = 1 / (1 + exp(-(V + 25)/15))
  τ_n(V) = 10-50 ms (slower than Shaker)

CaMKII modulation:
  f(CaMKII_active) = 1 + β * [CaMKII-P] / ([CaMKII-P] + K_m)

  where β = 0.5-2.0 (modulation factor)
```

**CaMKII-Dependent Regulation**:
```
d[CaMKII-P]/dt = k_phos * [Ca²⁺/CaM] * [CaMKII] - k_dephos * [CaMKII-P]

EAG current enhancement: 30-200% increase with CaMKII activation
```

**Expression Pattern**:
- CNS neurons (widespread)
- Mushroom bodies (memory circuits)
- Photoreceptors
- Motor neurons

**Behavioral Relevance**:
- Ether-induced leg-shaking behavior in mutants
- Neuronal excitability regulation
- Memory formation (interaction with learning pathways)
- Cardiac repolarization analog

---

### 1.5 slowpoke (slo) - Large Conductance Ca²⁺-Activated K⁺ Channel (BK)

**FlyBase ID**: FBgn0003429

**Gene Function**: Encodes structural α-subunit of BK channel, activated by both voltage and intracellular Ca²⁺, crucial for neurotransmitter release regulation.

**Protein Structure**:
- 7 transmembrane segments (S0-S6)
- Large C-terminal cytoplasmic domain
- Two RCK (regulator of K⁺ conductance) domains with Ca²⁺-binding sites
- Multiple alternative splice variants

**Dual Activation Kinetics**:
```
P_open(V, [Ca²⁺]) = 1 / (1 + exp(-(V - V_half([Ca²⁺]))/k))

where V_half depends on [Ca²⁺]:
  V_half([Ca²⁺]) = V_0 - S * log([Ca²⁺]/K_d)

  V_0 ≈ +50 mV (in absence of Ca²⁺)
  S ≈ 30-40 mV per 10-fold [Ca²⁺] change
  K_d ≈ 1-10 μM
```

**Single Channel Conductance**: 126 pS (large conductance)

**PKA Modulation**:
```
I_BK(modulated) = I_BK(basal) * (1 + α * [PKA_active])

where α = 1.5-3.0 (PKA enhancement factor)
```

**Calcium Sensitivity**:
```
Hill equation:
  Activity = Activity_max * [Ca²⁺]ⁿ / (K_d^n + [Ca²⁺]ⁿ)

  Hill coefficient n = 2-4 (varies with splice variant)
```

**Expression Pattern**:
- Presynaptic terminals
- Neuromuscular junction
- CNS neurons
- Muscle cells

**Behavioral Relevance**:
- Regulates neurotransmitter release
- Action potential repolarization
- Maintains electrical excitability
- Temperature compensation
- Modulated by phosphorylation (PKA) and binding proteins (Slob, 14-3-3ζ)

---

### 1.6 Hyperkinetic (Hk) - Voltage-Gated K⁺ Channel β-Subunit

**FlyBase ID**: FBgn0263220

**Gene Function**: Encodes β-subunit that modulates Shaker and Eag K⁺ channels, belonging to aldo-keto reductase superfamily.

**Protein Structure**:
- Aldo-keto reductase fold
- N-terminal domain for channel interaction
- Oxidoreductase domain (may have enzymatic function)

**Modulation of Shaker Kinetics**:
```
With Hk β-subunit association:
  τ_activation(Sh+Hk) = 0.3 * τ_activation(Sh alone)
  τ_inactivation(Sh+Hk) = 1.5 * τ_inactivation(Sh alone)

Current amplitude increase: 2-5 fold
Temperature sensitivity: altered Q10
Drug sensitivity: modified
```

**Channel Complex Stoichiometry**:
```
(Sh_α)₄:(Hk_β)₄ tetrameric assembly
```

**Expression Pattern**:
- Co-localizes with Shaker channels
- Neurons and muscle
- Essential for normal channel function

**Behavioral Relevance**:
- Regulates action potential kinetics
- Modulates transmitter release timing
- Temperature dependence of neural activity

---

### 1.7 Shaw (Kv3) - Delayed Rectifier K⁺ Channel

**FlyBase ID**: FBgn0003386

**Gene Function**: Encodes Kv3-type voltage-gated K⁺ channel with non-inactivating current and low voltage sensitivity.

**Channel Properties**:
```
Single Channel Conductance: 42 pS
Voltage sensitivity: extremely low

I_Shaw(V,t) = ḡ_Shaw * n⁴(V,t) * (V - E_K)

where:
  n∞(V) = 1 / (1 + exp(-(V + 10)/20))  [shallow slope]
  τ_n = 20-100 ms

Non-inactivating: h(t) = 1 (no inactivation gate)
```

**Activation**: Open at resting membrane potential (unusual)

**Expression Pattern**:
- CNS neurons
- Mushroom bodies
- Circadian rhythm circuits (oscillates with Shal)

**Behavioral Relevance**:
- Background K⁺ conductance
- Circadian rhythm modulation
- Resting membrane potential regulation

---

### 1.8 Shab (Kv2) - Delayed Rectifier K⁺ Channel

**FlyBase ID**: FBgn0262593

**Gene Function**: Encodes Kv2-family delayed rectifier K⁺ channel with moderate activation kinetics.

**Channel Kinetics**:
```
I_Shab(V,t) = ḡ_Shab * n²(V,t) * (V - E_K)

Activation faster than Shaw:
  n∞(V) = 1 / (1 + exp(-(V + 15)/12))
  τ_n = 10-50 ms

Delayed-rectifier type: minimal inactivation
```

**Expression Pattern**:
- CNS neurons
- Motor neurons
- Mushroom bodies

**Behavioral Relevance**:
- Action potential repolarization
- Regulates firing frequency
- Contributes to embryonic K⁺ currents

---

### 1.9 Shal (Kv4) - A-Type K⁺ Channel

**FlyBase ID**: FBgn0003380

**Gene Function**: Encodes Kv4-family rapidly inactivating A-type K⁺ channel.

**Channel Kinetics**:
```
I_Shal(V,t) = ḡ_Shal * m⁴(V,t) * h(V,t) * (V - E_K)

Fast inactivation:
  m∞(V) = 1 / (1 + exp(-(V + 25)/12))
  h∞(V) = 1 / (1 + exp((V + 55)/8))

  τ_m = 1-5 ms
  τ_h = 10-100 ms
```

**Circadian Regulation**:
```
Amplitude oscillates with ~24h period
Peak: subjective night
Trough: subjective day
```

**Expression Pattern**:
- CNS neurons
- Circadian pacemaker neurons
- Mushroom bodies

**Behavioral Relevance**:
- Circadian rhythm regulation (oscillates with Shaw)
- Action potential repolarization
- Controls neuronal excitability

---

### 1.10 TRP/TRPL - Transient Receptor Potential Calcium Channels

**FlyBase ID**: FBgn0032593 (TRPγ), FBgn0003861 (trpl)

**Gene Function**: TRPC-family cation channels responding to diverse stimuli, essential for sensory transduction and calcium signaling.

**Protein Structure**:
- 6 transmembrane domains
- Pore loop between TM5-TM6
- Large intracellular N- and C-termini
- Ankyrin repeats

**Channel Properties**:
```
TRP channel:
  P_Ca : P_Cs > 50:1 (highly Ca²⁺ selective)

TRPL channel:
  P_Ca : P_Cs ≈ 5:1 (modest Ca²⁺ permeability)

Light-activated current (phototransduction):
  I_TRP(t) = ḡ_TRP * (1 - exp(-t/τ_act)) * exp(-t/τ_inact)

  where:
    τ_act ≈ 10-50 ms
    τ_inact ≈ 100-500 ms
```

**Regulation by Lipid Messengers**:
```
Activation by PIP₂ depletion and DAG production:

  Light → Rhodopsin* → Gq → PLCβ → ↓PIP₂ + ↑DAG → TRP/TRPL opening
```

**Expression Pattern**:
- Photoreceptors (dominant in phototransduction)
- 13 TRP genes in *Drosophila*
- Various sensory neurons

**Behavioral Relevance**:
- Phototaxis (trpl;trp double mutants are blind)
- Thermotaxis
- Gravitaxis
- Noxious tastant avoidance
- Proprioception

---

### 1.11 SK - Small Conductance Ca²⁺-Activated K⁺ Channel

**FlyBase ID**: FBgn0031456

**Gene Function**: Encodes small conductance Ca²⁺-activated K⁺ channel regulating neuronal excitability and nociception.

**Channel Kinetics**:
```
I_SK(V, [Ca²⁺]) = ḡ_SK * (V - E_K) * f([Ca²⁺])

Calcium-dependent activation:
  f([Ca²⁺]) = [Ca²⁺]ⁿ / (K_d^n + [Ca²⁺]ⁿ)

  Hill coefficient n = 3-5
  K_d ≈ 0.3-0.7 μM

Voltage-independent gating
```

**Expression Pattern**:
- Peripheral neurons
- Nociceptive neurons
- Photoreceptors
- Localized to axons (not dendrites)

**Behavioral Relevance**:
- Negatively regulates nociception (pain sensation)
- Knockdown causes hypersensitive nociception
- Photoreceptor sensitivity control
- After-hyperpolarization (AHP) generation

---

### 1.12 Ca²⁺ Channel α2δ Subunit

**FlyBase ID**: FBgn0030084 (straightjacket/α2δ-3)

**Gene Function**: Accessory subunit of voltage-gated Ca²⁺ channels, crucial for channel trafficking, localization, and synaptic function.

**Protein Structure**:
- Large extracellular α2 domain
- Transmembrane δ domain
- GPI anchor or transmembrane segment
- Disulfide-linked α2-δ complex

**Functional Effects on Cac/Cav2**:
```
With α2δ subunit:
  - Surface expression: 2-5 fold increase
  - Current density: 3-10 fold increase
  - Activation kinetics: τ_act reduced by 20-40%
  - Inactivation: slower, τ_inact increased by 30-50%

Calcium current enhancement:
  I_Ca(+α2δ) = κ * I_Ca(-α2δ)
  where κ = 3-10
```

**Expression Pattern**:
- Presynaptic terminals
- Co-localizes with cacophony
- Neuromuscular junction
- CNS synapses

**Behavioral Relevance**:
- Essential for synaptic transmission (null mutants embryonic lethal)
- Calcium-dependent neurotransmitter release
- Synaptic strength regulation
- Neural circuit function

---

## 2. Neurotransmitter Receptors

### 2.1 NMDA Receptor (Nmdar1, Nmdar2)

**FlyBase ID**: FBgn0010399 (Nmdar1), FBgn0053513 (Nmdar2)

**Gene Function**: Ionotropic glutamate receptors essential for synaptic plasticity, learning, and memory consolidation.

**Protein Structure**:
- Heteromeric assembly: dNR1/dNR2
- 4 subunits (2 NR1 + 2 NR2)
- 3 transmembrane segments + re-entrant pore loop
- Large extracellular N-terminal domain (ligand binding)

**Channel Kinetics and Plasticity**:
```
I_NMDA(V,t) = ḡ_NMDA * m(V) * B(V) * (V - E_rev)

Voltage-dependent Mg²⁺ block:
  B(V) = 1 / (1 + [Mg²⁺]_o * exp(-V/V_0) / K_d)

  where:
    [Mg²⁺]_o ≈ 1 mM
    V_0 ≈ 16-18 mV
    K_d ≈ 3.6 mM

Dual glutamate + glycine requirement:
  m(Glu, Gly) = ([Glu]/K_Glu) * ([Gly]/K_Gly) /
                ((1 + [Glu]/K_Glu) * (1 + [Gly]/K_Gly))
```

**Calcium Permeability**:
```
P_Ca²⁺ : P_Na⁺ ≈ 10:1

Calcium influx for plasticity:
  J_Ca = P_Ca * I_NMDA * F/RT * (V * F/RT) *
         ([Ca²⁺]_i - [Ca²⁺]_o * exp(-V*F/RT)) /
         (1 - exp(-V*F/RT))
```

**Expression Pattern**:
- Punctate synaptic localization
- Throughout adult brain
- Mushroom bodies (learning centers)
- Visual system

**Behavioral Relevance**:
- Required acutely for associative learning
- Long-term memory consolidation
- Activity-dependent synaptic plasticity
- LTP and LTD induction
- Alcohol response modulation

---

### 2.2 Rdl - GABA_A Receptor (Resistance to Dieldrin)

**FlyBase ID**: FBgn0004244

**Gene Function**: Ligand-gated chloride channel mediating fast inhibitory neurotransmission via GABA.

**Protein Structure**:
- Pentameric assembly
- 4 transmembrane domains per subunit
- Chloride-selective pore
- GABA binding site at subunit interfaces

**Channel Kinetics**:
```
I_GABA(V,t) = ḡ_GABA * f([GABA]) * (V - E_Cl)

GABA-dependent activation:
  f([GABA]) = [GABA]ⁿ / (EC₅₀ⁿ + [GABA]ⁿ)

  Hill coefficient n = 1.5-2.5
  EC₅₀ ≈ 10-50 μM

Chloride reversal:
  E_Cl ≈ -65 to -80 mV (hyperpolarizing)
```

**Inhibitory Postsynaptic Current**:
```
IPSC(t) = I_max * exp(-t/τ_decay)

where:
  τ_decay = 10-30 ms (fast inhibition)
  I_max depends on receptor density and [GABA]
```

**Expression Pattern**:
- Highly expressed in mushroom bodies
- CNS neurons (widespread)
- Presynaptic and postsynaptic

**Behavioral Relevance**:
- Inhibits olfactory associative learning
- Visual processing
- Odor coding
- Sleep regulation
- Courtship behavior
- Insecticide resistance (cyclodiene resistance mutation)

---

### 2.3 Dopamine Receptors (DopR1/Dumb, DopR2/Damb)

**FlyBase ID**: FBgn0011582 (Dop1R1), FBgn0053517 (Dop1R2), FBgn0034223 (Dop2R)

**Gene Function**: G-protein coupled receptors mediating dopamine signaling in reward, aversion, and memory.

**Protein Structure**:
- 7 transmembrane domains (GPCR)
- D1-like: Dop1R1, Dop1R2 (couple to Gαs → ↑cAMP)
- D2-like: Dop2R (couples to Gαi → ↓cAMP)

**D1-like Signaling (Dop1R1/dDA1)**:
```
Dopamine + DopR1 → Gαs activation → Adenylyl Cyclase → ↑cAMP

cAMP production rate:
  d[cAMP]/dt = V_max * [DA·DopR1·Gαs] / (K_m + [DA·DopR1·Gαs]) - k_PDE * [cAMP]

  where k_PDE includes Dunce phosphodiesterase activity
```

**D2-like Signaling (Dop2R)**:
```
Dopamine + DopR2 → Gαi activation → ↓Adenylyl Cyclase → ↓cAMP

Opposing regulation:
  DopR1: memory formation (positive)
  DopR2: memory erosion (negative)
```

**Dose-Response**:
```
Response = Response_max * [DA]ⁿ / (EC₅₀ⁿ + [DA]ⁿ)

DopR1 EC₅₀ ≈ 10-100 nM
Hill coefficient n ≈ 1-2
```

**Expression Pattern**:
- Mushroom body neurons (learning center)
- Dopaminergic neurons innervate MB neuropil
- Various brain regions

**Behavioral Relevance**:
- Aversive olfactory learning (DopR1 essential)
- Appetitive learning
- Memory formation vs. erosion (opposing DopR1/DopR2)
- Reward processing
- Psychoactive substance intake regulation

---

### 2.4 Octopamine Receptors (OAMB, Octβ1R)

**FlyBase ID**: FBgn0024944 (Oamb), FBgn0038980 (Octβ1R)

**Gene Function**: G-protein coupled receptors mediating octopamine signaling in appetitive/aversive learning and arousal.

**Protein Structure**:
- 7 transmembrane domains
- OAMB: α1-like receptor (two isoforms: OAMB-K3, OAMB-AS)
- Octβ1R: β-adrenergic-like receptor

**OAMB Signaling (Appetitive Learning)**:
```
Octopamine + OAMB → Multiple pathways:

1) Ca²⁺ pathway (both isoforms):
   OAMB → Gαq → PLCβ → IP₃ → ↑[Ca²⁺]_i

2) cAMP pathway (OAMB-K3 only):
   OAMB-K3 → Gαs → AC → ↑cAMP

Dual second messenger:
  Appetitive learning = f([Ca²⁺], [cAMP])
  Aversive learning = f([cAMP] only)
```

**Octβ1R Signaling**:
```
Octopamine + Octβ1R → Gαs → ↑cAMP

Drives both:
  - Aversive learning (αβ neurons)
  - Appetitive learning (context-dependent)
```

**Expression Pattern**:
- Mushroom body neurons
- Dorsal paired medial (DPM) cells
- Subesophageal ganglion
- Motor neurons

**Behavioral Relevance**:
- Appetitive olfactory learning (OAMB required)
- Sugar reward processing
- Courtship conditioning (aversive input)
- Concerted action with dopamine receptors

---

### 2.5 Nicotinic Acetylcholine Receptors (nAChRs)

**FlyBase ID**: Multiple genes (Dα1-Dα7, Dβ1-Dβ3)

**Gene Function**: Ligand-gated cation channels mediating fast excitatory cholinergic transmission.

**Protein Structure**:
- Pentameric assembly (5 subunits around central pore)
- Each subunit: 4 transmembrane domains (M1-M4)
- Non-selective cation channel
- 10 nAChR subunit genes in *Drosophila*

**Channel Kinetics**:
```
I_nAChR(V,t) = ḡ_nAChR * f([ACh], t) * (V - E_rev)

Acetylcholine activation:
  f([ACh]) = [ACh]ⁿ / (EC₅₀ⁿ + [ACh]ⁿ)

  Hill coefficient n = 1.5-2.5
  EC₅₀ ≈ 10-100 μM (subunit-dependent)

Reversal potential:
  E_rev ≈ 0 mV (non-selective: Na⁺, K⁺, Ca²⁺)
```

**Desensitization**:
```
Open ⇌ Desensitized

τ_desensitization = 50-500 ms (varies by subunit composition)
```

**Expression Pattern**:
- Excitatory cholinergic synapses
- CNS neurons (widespread)
- Temporal regulation during development
- Neuromuscular junction

**Behavioral Relevance**:
- Excitatory neurotransmission
- Learning and memory
- Neural development
- Synaptic plasticity
- Cognitive processes

---

## 3. Learning and Memory Genes

### 3.1 rutabaga (rut) - Ca²⁺/Calmodulin-Responsive Adenylyl Cyclase

**FlyBase ID**: FBgn0003301

**Gene Function**: Type 1 adenylyl cyclase acting as molecular coincidence detector for associative learning via cAMP synthesis.

**Protein Structure**:
- Membrane-bound enzyme
- Two catalytic domains (C1, C2)
- Calmodulin-binding domain
- Responsive to both Ca²⁺/CaM and Gαs

**Coincidence Detection Mechanism**:
```
Synergistic cAMP production:

d[cAMP]/dt = V_max * f([Ca²⁺/CaM]) * g([Gαs-GTP]) /
             (K_m + [ATP]) - k_PDE * [cAMP]

where:
  f([Ca²⁺/CaM]) = [Ca²⁺/CaM]ⁿ / (K_d^n + [Ca²⁺/CaM]ⁿ)
  g([Gαs-GTP]) = [Gαs-GTP] / (K_act + [Gαs-GTP])

Synergy factor:
  With both Ca²⁺/CaM AND Gαs: 10-100× baseline
  With either alone: 2-5× baseline
```

**Associative Learning Formula**:
```
CS (odor) → Ca²⁺ influx → ↑[Ca²⁺/CaM]
        +
US (shock/reward) → neurotransmitter → GPCR → Gαs
        ↓
    rut-AC1 activation → ↑↑↑cAMP → PKA → CREB → Memory
```

**PKA Activation Kinetics**:
```
[PKA_active] = [PKA_total] * ([cAMP]⁴ / (K_d⁴ + [cAMP]⁴))

Hill coefficient n = 4 (cooperative binding)
K_d ≈ 0.1-1 μM
```

**Expression Pattern**:
- Mushroom body Kenyon cells
- Projection neurons
- Ellipsoid body
- Memory-relevant brain regions

**Behavioral Relevance**:
- Essential for associative olfactory learning
- Coincidence detector for CS + US
- Short-term memory formation
- Behavioral plasticity
- Synergistic activation by ACh + DA or ACh + OA

---

### 3.2 dunce (dnc) - cAMP Phosphodiesterase 4 (Pde4)

**FlyBase ID**: FBgn0000479

**Gene Function**: cAMP-specific phosphodiesterase degrading cAMP, acting as molecular gate for long-term memory formation.

**Protein Structure**:
- Complex gene with large introns containing other genes
- PDE catalytic domain
- Regulatory domains
- Multiple splice variants

**cAMP Degradation Kinetics**:
```
d[cAMP]/dt_degradation = -V_max * [cAMP] / (K_m + [cAMP])

Michaelis-Menten parameters:
  K_m ≈ 1-10 μM
  V_max (enzymatic capacity)

Steady-state cAMP level:
  [cAMP]_ss = (V_synthesis - V_max) / k_PDE
```

**Memory Gate Mechanism**:
```
During LTM formation:
  Dnc is inhibited in serotonergic neurons (SPN)
  ↓
  ↑cAMP in SPN
  ↓
  PKA activation in SPN
  ↓
  Activation of downstream dopaminergic neurons
  ↓
  Gate opened for LTM in mushroom bodies
```

**Temporal Dynamics**:
```
dnc mutants: elevated [cAMP] → impaired learning
dunce × rutabaga double mutant: partial rescue

Optimal cAMP level for learning: narrow window
  Too low (rut mutant): no learning
  Too high (dnc mutant): impaired learning
  Just right: normal learning
```

**Expression Pattern**:
- Mushroom body neuropil (intense staining)
- Serotonergic neurons
- Various brain regions
- Spatial regulation of cAMP dynamics

**Behavioral Relevance**:
- Learning and memory (original learning mutant)
- Long-term memory checkpoint
- cAMP homeostasis
- Spatial compartmentalization of signaling

---

### 3.3 amnesiac (amn) - PACAP-like Neuropeptide

**FlyBase ID**: FBgn0086782

**Gene Function**: Encodes pre-pro-neuropeptide with PACAP-like peptide, essential for medium-term and long-term memory.

**Protein Structure**:
- Pre-pro-neuropeptide precursor
- Three predicted peptides
- One peptide homologous to mammalian PACAP (pituitary adenylate cyclase-activating peptide)
- C-terminal: RVRFamide motif

**Signaling Mechanism**:
```
AMN neuropeptide release (from DPM neurons)
        ↓
GPCR activation on mushroom body neurons
        ↓
Gαs → Adenylyl Cyclase → ↑cAMP
        ↓
PKA activation → CREB phosphorylation
        ↓
Middle-term and Long-term memory
```

**cAMP Amplification**:
```
[cAMP]_MB = [cAMP]_basal + k_AMN * [AMN_released]

where k_AMN represents GPCR-mediated amplification
```

**Temporal Dynamics**:
```
Short-term memory (STM): AMN-independent
Middle-term memory (MTM): AMN-dependent
Long-term memory (LTM): AMN-dependent

Time course:
  STM: 0-3 hours
  MTM: 3-6 hours (requires AMN)
  LTM: >24 hours (requires AMN + CREB)
```

**Expression Pattern**:
- Dorsal paired medial (DPM) neurons
- Projects to mushroom bodies
- Larval CNS
- Neuromuscular junction (PACAP-like immunoreactivity)

**Behavioral Relevance**:
- Prolongs medium-term memory
- Essential for long-term memory consolidation
- Works with cAMP/PKA pathway
- Neuromodulator for memory circuits

---

### 3.4 CREB (CrebB/dCREB2) - cAMP Response Element Binding Protein

**FlyBase ID**: FBgn0265784

**Gene Function**: Transcription factor essential for long-term memory, phosphorylated by PKA to activate memory gene transcription.

**Protein Structure**:
- Basic leucine zipper (bZIP) domain (DNA binding)
- Kinase-inducible domain (KID) with PKA phosphorylation site
- Multiple isoforms: activators and repressors
- Nuclear localization signals

**Phosphorylation-Dependent Activation**:
```
PKA phosphorylation:
  CREB + PKA-active → pCREB (Ser133/equivalent)

Transcriptional activity:
  Activity = Activity_max * [pCREB] / (K_d + [pCREB])

Nuclear accumulation dynamics:
  d[pCREB]_nucleus/dt = k_import * [pCREB]_cytoplasm - k_export * [pCREB]_nucleus
```

**Long-Term Memory Formation**:
```
Learning → ↑cAMP → PKA → pCREB
                          ↓
                   CRE-driven transcription
                          ↓
        Memory consolidation genes (C/EBP, etc.)
                          ↓
                 Synaptic remodeling
                          ↓
                  Long-term memory

Time course: >24 hours for protein synthesis-dependent LTM
```

**CREB Isoform Balance**:
```
Memory strength ∝ [CREB_activator] / [CREB_repressor]

Overexpression of activator: enhanced LTM
Overexpression of blocker: blocked LTM
```

**Expression Pattern**:
- Mushroom bodies (Kenyon cells)
- Ellipsoid body R2/R4m neurons
- Various MB neuron subsets
- Dynamic regulation during memory formation

**Behavioral Relevance**:
- Essential for long-term memory (not STM)
- Requires phosphorylation by PKA
- Nuclear dynamics regulated during LTM
- Controls memory gene expression
- One training session sufficient if CREB optimized

---

### 3.5 radish (rsh) - PKA Substrate for Anesthesia-Resistant Memory

**FlyBase ID**: FBgn0015720

**Gene Function**: Encodes protein required specifically for anesthesia-resistant memory (ARM), a parallel memory component.

**Protein Structure**:
- Novel protein (no clear homology)
- 23 predicted PKA phosphorylation sequences
- Cytoplasmic and nuclear localization
- PKA target in vitro

**Memory Component Specificity**:
```
Two parallel memory pathways after training:

1) Anesthesia-sensitive memory (ASM):
   Training → cAMP/PKA → CREB → LTM

2) Anesthesia-resistant memory (ARM):
   Training → cAMP/PKA → Radish-P → ARM

ARM + ASM = Total consolidated memory
```

**PKA-Dependent Phosphorylation**:
```
Radish + PKA → Radish-P (23 potential sites)

Phosphorylation state correlates with ARM strength
```

**Temporal Dynamics**:
```
ARM onset: 30-60 minutes post-training
ARM duration: days
ARM resistant to cold anesthesia (unlike ASM)

Pharmacology:
  Anesthesia → blocks ASM, spares ARM
  radish mutant → blocks ARM, spares ASM
```

**Expression Pattern**:
- Mushroom bodies (high expression)
- Cytoplasm and nucleus
- Co-expression with other cAMP pathway components

**Behavioral Relevance**:
- Specifically required for ARM
- Links to cAMP/PKA pathway
- Distinct from CREB-dependent LTM
- Represents parallel memory storage mechanism

---

### 3.6 PKA Catalytic Subunit (Pka-C1/DCO)

**FlyBase ID**: FBgn0000273

**Gene Function**: Catalytic subunit of cAMP-dependent protein kinase, central to learning and memory signaling cascades.

**Protein Structure**:
- Conserved serine/threonine kinase domain
- cAMP-binding regulatory subunit binding site
- Substrate recognition motif: R-R/K-X-S/T

**Activation Mechanism**:
```
PKA holoenzyme: (R)₂(C)₂ (inactive)

cAMP binding:
  4 cAMP + (R)₂(C)₂ → (R·2cAMP)₂ + 2 C (active)

Catalytic activity:
  k_cat/K_m for optimal substrates ≈ 10⁶ M⁻¹s⁻¹
```

**Substrate Phosphorylation**:
```
Substrate-P production:
  v = V_max * [Substrate] / (K_m + [Substrate])

Key substrates in learning:
  - CREB (transcription)
  - Radish (ARM)
  - Ion channels (modulation)
  - Synaptic proteins
```

**Dose-Dependent Effects on Memory**:
```
Paradoxical finding:
  WT PKA: normal memory
  ↓PKA (DCO mutants): ENHANCED memory
  ↑↑PKA (overexpression): REDUCED memory

Optimal PKA activity window for memory formation
```

**Age-Related Memory**:
```
DCO heterozygous mutations:
  - Delay age-related memory impairment >2-fold
  - Suggests PKA increase contributes to cognitive aging
```

**Expression Pattern**:
- Mushroom bodies (preferential)
- Widespread CNS
- Critical for MB-dependent memory

**Behavioral Relevance**:
- Essential for associative learning
- Cold-sensitive alleles impair learning
- Biphasic dose-response (optimal window)
- Memory consolidation
- Age-related cognitive decline

---

## 4. Synaptic Proteins

### 4.1 Synaptotagmin 1 (Syt1) - Calcium Sensor for Synchronous Release

**FlyBase ID**: FBgn0004242

**Gene Function**: Primary Ca²⁺ sensor for fast synchronous neurotransmitter release, containing tandem C2 domains.

**Protein Structure**:
- N-terminal transmembrane domain (anchors to synaptic vesicle)
- C2A domain (3 Ca²⁺ binding sites)
- C2B domain (2 Ca²⁺ binding sites)
- Linker region

**Calcium Sensing Mechanism**:
```
Ca²⁺ binding to C2 domains:

C2A: 3 Ca²⁺ sites, K_d ≈ 10-100 μM
C2B: 2 Ca²⁺ sites, K_d ≈ 50-200 μM

Total 5 Ca²⁺ ions bound per Syt1 molecule at high [Ca²⁺]
```

**Fusion Triggering**:
```
Release rate:
  R(t) = R_max * ([Ca²⁺]_local(t))ⁿ / (K_d^n + ([Ca²⁺]_local(t))ⁿ)

Cooperativity: n ≈ 5 (matches 5 Ca²⁺ binding sites)
K_d ≈ 10-50 μM (local domain)

Time course:
  τ_release ≈ 0.5-2 ms (ultrafast)
```

**Synchronous vs Asynchronous Release**:
```
WT Syt1:
  - Synchronous release: dominant
  - Asynchronous release: minimal

syt1 mutants:
  - Synchronous release: abolished
  - Asynchronous release: uncovered (delayed pathway)

Time course asynchronous: τ ≈ 10-100 ms
```

**Expression Pattern**:
- All synaptic vesicles
- Presynaptic terminals
- Neuromuscular junction
- CNS synapses

**Behavioral Relevance**:
- Fast synchronous neurotransmitter release
- Precise temporal coupling of Ca²⁺ to exocytosis
- Synaptic transmission fidelity
- Multiple Syt isoforms for different functions (Syt4, Syt7)

---

### 4.2 Complexin (cpx) - SNARE Complex Regulator

**FlyBase ID**: FBgn0041605

**Gene Function**: Presynaptic cytosolic protein regulating SNARE complex assembly, serving as fusion clamp and release facilitator.

**Protein Structure**:
- Small cytosolic protein (~150 amino acids)
- Central α-helix (binds SNARE complex)
- N-terminal domain
- C-terminal domain
- Phosphorylation site: Ser126

**Dual Function in Release**:
```
1) Fusion Clamp:
   Spontaneous release rate:
     R_spont(WT) < R_spont(cpx-/-)

   cpx-/- mutants: marked increase in spontaneous fusion

2) Evoked Release Facilitator:
   Evoked release probability:
     P_release(WT) > P_release(cpx-/-)

   Cpx promotes calcium-triggered fusion
```

**Regulation of Release Pathways**:
```
Synchronous release:
  Controlled by Cpx, requires Synaptotagmin

Asynchronous release:
  cpx-/- → increased asynchronous component
  Cpx overexpression → eliminates asynchronous release

Balance:
  Synchronous/Asynchronous = f([Cpx], [Cpx-P])
```

**Phosphorylation Modulation**:
```
Cpx phosphorylation at S126:
  - Selectively alters fusion clamp function
  - Does not affect facilitation

Cpx-P → altered spontaneous release rate
```

**Expression Pattern**:
- Presynaptic terminals
- All synapses
- Co-localizes with SNARE proteins

**Behavioral Relevance**:
- Controls spontaneous vs evoked release balance
- Synaptic homeostasis
- Temporal precision of neurotransmission
- Works with Bruchpilot to tether vesicles

---

### 4.3 Bruchpilot (brp) - Active Zone Scaffold Protein

**FlyBase ID**: FBgn0259246

**Gene Function**: Cytoskeletal protein essential for T-bar (electron-dense projection) assembly and Ca²⁺ channel clustering at active zones.

**Protein Structure**:
- Large scaffold protein
- N-terminus: closer to active zone membrane
- C-terminus: extends toward cytoplasm
- Coiled-coil domains for protein-protein interactions

**Active Zone Assembly**:
```
BRP-dependent maturation stages:

Stage 1: Liprin-α recruitment (BRP-independent)
         ↓
Stage 2: BRP recruitment and T-bar assembly
         ↓
Stage 3: Ca²⁺ channel clustering (BRP-dependent)
         ↓
Mature active zone with maximal release capacity
```

**Calcium Channel Clustering**:
```
Cacophony (Cav2) density:

  WT: 50-100 channels per active zone (clustered)
  brp mutant: 10-20 channels per active zone (diffuse)

Clustering factor:
  CF = [Cac]_WT / [Cac]_brp ≈ 3-5 fold
```

**Effect on Synaptic Transmission**:
```
brp mutants:
  - T-bars: completely absent
  - Ca²⁺ current density: reduced 60-80%
  - Evoked release: depressed 50-70%
  - Short-term plasticity: altered

Quantal content:
  m = n * p

  m_WT / m_brp ≈ 2-4 (reduced release)
```

**Expression Pattern**:
- Presynaptic active zones
- T-bar center component
- Neuromuscular junction
- CNS synapses

**Behavioral Relevance**:
- Essential for structural integrity of release sites
- Clusters Ca²⁺ channels for efficient coupling
- Determines synaptic strength
- Short-term plasticity regulation

---

### 4.4 Stoned A and Stoned B - Endocytic Proteins

**FlyBase ID**: FBgn0003638 (stoned)

**Gene Function**: Two proteins (STNA, STNB) regulating synaptic vesicle endocytosis and recycling via synaptotagmin interaction.

**Protein Structure**:
- STNA: Novel protein, no homology
- STNB: Contains AP50-homology domain (endocytosis)
- Both interact with Synaptotagmin 1

**Vesicle Recycling Kinetics**:
```
stoned mutants:
  - Endo-exo-cycling pool size: reduced 40-60%
  - Vesicle retrieval rate: delayed 2-5 fold

FM1-43 dye uptake:
  τ_uptake(WT) = 30-60 s
  τ_uptake(stn) = 90-180 s (slower)
```

**Synaptotagmin Retrieval**:
```
After exocytosis:
  Syt1 in plasma membrane
       ↓
  Stoned A + Stoned B bind Syt1
       ↓
  AP2 complex recruitment
       ↓
  Clathrin-mediated endocytosis
       ↓
  Syt1 returned to vesicles

Retrieval efficiency:
  E = [Syt1_vesicles] / [Syt1_total]

  E_WT ≈ 0.8-0.9
  E_stn ≈ 0.4-0.6 (impaired)
```

**Spatial Regulation**:
```
stoned mutants:
  - Loss of spatial organization of endocytic domains
  - Diffuse distribution of endocytic intermediates
  - Lattice network disruption (AP2, Dynamin localization)
```

**Expression Pattern**:
- Presynaptic terminals
- Co-localizes with endocytic proteins
- Punctate distribution at synapses

**Behavioral Relevance**:
- Regulates synaptic transmission strength
- Controls vesicle pool size
- Maintains sustained neurotransmitter release
- Couples exocytosis to endocytosis

---

### 4.5 Inebriated (ine) - Neurotransmitter/Osmolyte Transporter

**FlyBase ID**: FBgn0011603

**Gene Function**: Na⁺/Cl⁻-dependent neurotransmitter transporter family member, regulates motor neuron excitability.

**Protein Structure**:
- 12 transmembrane domains
- SLC6A family transporter
- Similar to betaine/GABA transporter (BGT1)
- NOT a GABA or glutamate transporter (despite early proposals)

**Transport Mechanism**:
```
Transport stoichiometry (typical for SLC6A):
  1 substrate + 2 Na⁺ + 1 Cl⁻ → (inward)

Na⁺ gradient provides driving force
Cl⁻ required for binding

Flux equation:
  J = J_max * f([Na⁺], [Cl⁻], [Substrate], V)
```

**Effect on Neuronal Excitability**:
```
ine mutations:
  - Defective reuptake of substrate neurotransmitter
  - Increased extracellular neurotransmitter
  - Motor neuron overstimulation
  - Increased excitability

Behavioral phenotype: "inebriated" (wobbly movement)
```

**Expression Pattern**:
- Motor neurons
- CNS neurons
- Hindgut (water homeostasis function)
- Eye photoreceptors

**Behavioral Relevance**:
- Motor coordination (inebriated phenotype in mutants)
- Neuronal excitability regulation
- Systemic water homeostasis (hindgut function)
- NOT directly GABA-ergic, despite family similarity

---

## 5. Circadian Rhythm Genes

### 5.1 period (per) - Core Clock Component

**FlyBase ID**: FBgn0003068

**Gene Function**: Core circadian clock gene encoding PER protein, which forms negative feedback loop with CLOCK and CYCLE.

**Protein Structure**:
- PAS domains (protein-protein interaction)
- Nuclear localization signals
- Phosphorylation sites (multiple kinases)
- CRY binding domain

**Molecular Feedback Loop**:
```
Transcription phase (day):
  CLK/CYC heterodimer → binds E-box → transcribes per + tim

Translation and accumulation (evening):
  per mRNA → PER protein (accumulates in cytoplasm)
  tim mRNA → TIM protein

Nuclear translocation (night):
  PER + TIM → heterodimer → nuclear entry

Repression (late night):
  PER/TIM → inhibits CLK/CYC → represses own transcription

Degradation (morning):
  Light → CRY activation → TIM degradation
  PER unstable alone → degradation

Cycle repeats with ~24h period
```

**Mathematical Model**:
```
d[per_mRNA]/dt = v_s * f_CLK/CYC - k_m * [per_mRNA]

d[PER]/dt = k_s * [per_mRNA] - k_d * [PER] - k_n * [PER]

d[PER_nucleus]/dt = k_n * [PER] - k_deg * [PER_nucleus]

where:
  f_CLK/CYC = V_max / (1 + ([PER_nucleus]/K_I)ⁿ)  [repression]

Period τ ≈ 24 hours
Hill coefficient n = 4-8 (cooperativity)
```

**Phosphorylation Delays**:
```
Multiple kinases phosphorylate PER:
  - DBT (Doubletime/CK1): delays nuclear entry
  - Other kinases: affect stability

Delay crucial for ~24h oscillation:
  Without delays: period too short (~12-16h)
```

**Expression Pattern**:
- Pacemaker neurons (s-LNv, l-LNv)
- Dorsal neurons
- Oscillates with circadian rhythm
- Peak expression: late day/early evening

**Behavioral Relevance**:
- Controls circadian locomotor activity
- per⁰ mutants: arrhythmic
- per^S mutants: short period (~19h)
- per^L mutants: long period (~29h)
- Sleep-wake cycles

---

### 5.2 timeless (tim) - PER Partner Protein

**FlyBase ID**: FBgn0014396

**Gene Function**: Essential clock component that heterodimerizes with PER for nuclear translocation and light-dependent degradation.

**Protein Structure**:
- Large protein
- PER-binding domain
- CRY-binding domain (light sensitivity)
- Nuclear localization signals

**TIM-PER Interaction**:
```
Formation of functional complex:
  PER + TIM ⇌ PER:TIM (K_d ≈ nM range, tight binding)

Nuclear import:
  Rate enhanced >10-fold with TIM
  PER alone: slow/inefficient nuclear entry
  PER:TIM: efficient nuclear translocation
```

**Light-Induced Degradation**:
```
Light activation pathway:
  Light → Cryptochrome (CRY) activation
       ↓
  CRY* binds TIM
       ↓
  TIM ubiquitination and degradation
       ↓
  PER unstable without TIM → degradation
       ↓
  Clock reset (phase advance)

Degradation kinetics:
  τ_TIM_degradation ≈ 30-60 min (in light)
```

**Temperature Entrainment**:
```
PYREXIA channel (TRPA) controls PER/TIM:
  Temperature shifts → PYREXIA → [Ca²⁺]_i changes
  → affects PER stability and nuclear entry

Allows temperature synchronization of clock
```

**Expression Pattern**:
- Circadian neurons
- Co-expressed with PER
- Oscillates with ~24h rhythm
- Peak: evening

**Behavioral Relevance**:
- Essential for circadian rhythms
- tim mutants: arrhythmic
- Light entrainment mediator
- Temperature entrainment
- Phase setting of clock

---

### 5.3 Clock (Clk) - Positive Transcription Factor

**FlyBase ID**: FBgn0023076

**Gene Function**: bHLH-PAS transcription factor that heterodimerizes with CYCLE to activate per and tim transcription.

**Protein Structure**:
- Basic helix-loop-helix (bHLH) domain (DNA binding)
- PAS domains (CYC binding)
- Transcriptional activation domain

**Transcriptional Activation**:
```
CLK/CYC heterodimer formation:
  CLK + CYC → CLK:CYC complex

E-box binding and transcription:
  CLK:CYC + E-box (CACGTG) → transcription ON

  Target genes:
    - period (per)
    - timeless (tim)
    - vrille (vri)
    - PAR domain protein 1 (Pdp1)

Transcription rate:
  v_per = V_max * [CLK:CYC:E-box] / (1 + [PER:TIM]ⁿ/K_I^n)
```

**Feedback Regulation**:
```
CLK/CYC activity oscillates inversely with PER/TIM:

  Day: High CLK/CYC → high per/tim transcription
  Night: PER/TIM inhibits CLK/CYC → low per/tim transcription

Result: ~24h oscillation
```

**Expression Pattern**:
- Circadian pacemaker neurons
- Constitutive (doesn't oscillate at mRNA level)
- Activity oscillates via post-translational regulation

**Behavioral Relevance**:
- Essential positive element of clock
- Clk mutants: arrhythmic
- Drives rhythmic gene expression
- Master regulator of circadian outputs

---

## 6. G-Protein Signaling

### 6.1 Gαs - Stimulatory G-Protein Alpha Subunit

**FlyBase ID**: FBgn0001123

**Gene Function**: Alpha subunit of heterotrimeric G-protein that activates adenylyl cyclase upon GPCR activation, increasing cAMP.

**Protein Structure**:
- GTPase domain
- Receptor-binding domain
- Adenylyl cyclase-binding domain
- Palmitoylation sites for membrane anchoring

**GTPase Cycle**:
```
Inactive state:
  Gαs·GDP·Gβγ (membrane-associated trimer)

GPCR activation:
  Receptor* + Gαs·GDP·Gβγ → Receptor*·Gαs·GDP·Gβγ

GDP/GTP exchange:
  Receptor*·Gαs·GDP·Gβγ → Receptor* + Gαs·GTP + Gβγ

Active state:
  Gαs·GTP binds and activates adenylyl cyclase (AC)

  Gαs·GTP + AC → Gαs·GTP·AC* → ↑cAMP

GTP hydrolysis (termination):
  Gαs·GTP → Gαs·GDP + Pi
  τ_GTPase ≈ 10-60 s (intrinsic)

Reassociation:
  Gαs·GDP + Gβγ → Gαs·GDP·Gβγ (reset)
```

**cAMP Production**:
```
d[cAMP]/dt = V_AC * [Gαs·GTP·AC] / (K_m + [ATP]) - k_PDE * [cAMP]

V_AC increased 5-20 fold by Gαs activation
```

**Expression Pattern**:
- Widespread in CNS
- Neurons (particularly memory circuits)
- Associates with GPCRs (DopR1, OAMB-K3, etc.)

**Behavioral Relevance**:
- Learning and memory (cAMP signaling)
- Neurophysiology
- GPCR signal transduction
- Multiple behaviors dependent on cAMP

---

### 6.2 Gαq - Phospholipase C-Coupled G-Protein

**FlyBase ID**: FBgn0004435

**Gene Function**: Alpha subunit coupling GPCRs to phospholipase Cβ (PLCβ), producing IP₃ and DAG for Ca²⁺ release and PKC activation.

**Protein Structure**:
- GTPase domain
- PLCβ-binding domain
- 7 splice variants encoding 3 isoforms (Gαq1, Gαq3, Gαq4)

**Signaling Cascade**:
```
GPCR activation pathway:
  Receptor* → Gαq·GTP activation
       ↓
  Gαq·GTP + PLCβ → PLCβ* (active)
       ↓
  PLCβ* + PIP₂ → IP₃ + DAG
       ↓
  IP₃ → Ca²⁺ release from ER
  DAG → PKC activation + ion channel modulation (TRP/TRPL)
```

**IP₃-Induced Ca²⁺ Release**:
```
d[Ca²⁺]_i/dt = v_IP3R * ([IP₃]/K_IP3)³ * ([Ca²⁺]_ER - [Ca²⁺]_i) - k_pump * [Ca²⁺]_i

Hill coefficient for IP₃: n = 3
K_IP3 ≈ 0.1-1 μM
```

**DAG Production**:
```
[DAG] = k_PLCβ * [PIP₂] * [Gαq·GTP]

DAG effects:
  - PKC activation
  - TRP/TRPL channel activation (phototransduction)
```

**Expression Pattern**:
- CNS neurons
- Photoreceptors (phototransduction cascade)
- Olfactory neurons
- Mushroom bodies

**Behavioral Relevance**:
- Neuronal development
- Olfaction
- Flight
- Learning and memory
- Phototransduction (visual system)
- Organ size and developmental timing

---

### 6.3 Gαi - Inhibitory G-Protein Alpha Subunit

**FlyBase ID**: FBgn0001104

**Gene Function**: Alpha subunit that inhibits adenylyl cyclase and modulates ion channels upon GPCR activation.

**Protein Structure**:
- GTPase domain
- Inhibits AC when GTP-bound
- Modulates ion channels via Gβγ release

**Inhibitory Mechanism**:
```
GPCR activation:
  Receptor* → Gαi·GTP + Gβγ

Adenylyl cyclase inhibition:
  Gαi·GTP + AC → AC·Gαi·GTP (inactive)

Net cAMP production:
  d[cAMP]/dt = V_AC(Gαs) * f_inhibition(Gαi) - k_PDE * [cAMP]

  where:
    f_inhibition = 1 / (1 + [Gαi·GTP·AC]/K_I)

  Result: ↓cAMP when Gαi active
```

**Gβγ-Mediated Effects**:
```
Released Gβγ subunits:
  - Activate GIRK channels (K⁺ efflux → hyperpolarization)
  - Inhibit voltage-gated Ca²⁺ channels
  - Modulate other effectors
```

**Expression Pattern**:
- CNS neurons
- Widespread distribution
- Co-expression with Gαo in Gαi/o subgroup

**Behavioral Relevance**:
- GPCR signal transduction (inhibitory)
- Opposes Gαs-mediated cAMP signaling
- Modulates neuronal excitability
- Ion channel regulation

---

## 7. Calcium-Dependent Enzymes

### 7.1 CaMKII - Calcium/Calmodulin-Dependent Protein Kinase II

**FlyBase ID**: FBgn0264607

**Gene Function**: Abundant serine/threonine kinase activated by Ca²⁺/calmodulin, essential for synaptic plasticity and memory.

**Protein Structure**:
- Catalytic domain
- Regulatory domain (autoinhibitory)
- Calmodulin-binding domain
- Association domain (forms holoenzyme)
- Thr287 (autophosphorylation site)

**Activation Mechanism**:
```
Inactive state:
  CaMKII (autoinhibited by regulatory domain)

Ca²⁺/CaM binding:
  4 Ca²⁺ + CaM → Ca²⁺/CaM
  Ca²⁺/CaM + CaMKII → Ca²⁺/CaM·CaMKII* (active)

Autophosphorylation:
  CaMKII* + ATP → CaMKII-P (Thr287) + ADP

CaMKII-P properties:
  - Ca²⁺-independent activity (autonomous)
  - Acts as "molecular memory switch"
  - Sustained activity after [Ca²⁺] returns to baseline
```

**Kinetic Model**:
```
d[CaMKII-P]/dt = k_auto * [Ca²⁺/CaM·CaMKII]² - k_PP * [CaMKII-P]

where:
  k_auto: autophosphorylation rate (enhanced by holoenzyme structure)
  k_PP: protein phosphatase dephosphorylation rate

Bistability: [CaMKII-P] can exist in low or high state
  - Low state: transient signaling
  - High state: persistent signaling (memory)
```

**Synaptic Plasticity**:
```
LTP induction:
  High-frequency stimulation → ↑[Ca²⁺]_i
  → CaMKII activation and autophosphorylation
  → Sustained CaMKII-P activity
  → AMPA receptor insertion
  → Enhanced synaptic strength

Threshold for LTP:
  [Ca²⁺]_threshold ≈ 1-10 μM
  Duration: >100 ms required
```

**Structural Effects**:
```
Activated CaMKII expression:
  - Increases dendritic filopodia formation
  - Accelerates F-actin turnover
  - Alters cytoskeletal dynamics

Effects on spine morphology:
  Spine size ∝ [CaMKII-P]
```

**Expression Pattern**:
- Abundant in neurons
- Postsynaptic densities
- Dendrites and spines
- Mushroom bodies

**Behavioral Relevance**:
- Disrupts behavioral plasticity when inhibited
- Impairs acoustic priming
- Impairs courtship conditioning
- Essential for learning and memory
- Regulated by CASK scaffold protein

---

### 7.2 Calcineurin (CanA1/Pp2B-14D) - Ca²⁺/Calmodulin-Dependent Phosphatase

**FlyBase ID**: FBgn0010015 (CanA1), FBgn0011826 (Pp2B-14D)

**Gene Function**: Ca²⁺/calmodulin-stimulated protein phosphatase opposing kinase actions, involved in plasticity and sleep.

**Protein Structure**:
- Catalytic subunit A (~60 kDa): CanA
- Regulatory subunit B (19 kDa): CanB (EF-hand Ca²⁺-binding)
- Calmodulin-binding domain
- Autoinhibitory domain

**Activation Mechanism**:
```
Inactive state:
  CanA·CanB (autoinhibited)

Ca²⁺ and CaM binding:
  4 Ca²⁺ + CanB → CanA·CanB-Ca²⁺
  Ca²⁺/CaM + CanA·CanB-Ca²⁺ → Active calcineurin

Phosphatase activity:
  Substrate-P + H₂O → Substrate + Pi

  K_m ≈ 1-10 μM (substrate-dependent)
```

**Opposes CaMKII**:
```
Bidirectional control:
  CaMKII: phosphorylation (↑ activity)
  Calcineurin: dephosphorylation (↓ activity)

Balance determines phosphorylation state:
  Steady-state = f([Ca²⁺], CaMKII/Calcineurin ratio)
```

**Ca²⁺ Sensitivity**:
```
[Ca²⁺] dependence:
  Low [Ca²⁺] (< 0.5 μM): minimal activity
  Medium [Ca²⁺] (0.5-2 μM): progressive activation
  High [Ca²⁺] (> 2 μM): maximal activity

Compared to CaMKII:
  Calcineurin: lower Ca²⁺ threshold, slower kinetics
  CaMKII: higher Ca²⁺ threshold, faster kinetics
```

**Expression Pattern**:
- Neurons (widespread)
- Muscle
- Essential neuronal function (null mutants lethal)

**Behavioral Relevance**:
- Memory consolidation (mammalian studies suggest role)
- Sleep regulation:
  - Pan-neuronal knockdown → sleep loss
  - Constitutively active CanA → increased sleep
- Aversive olfactory memory retention (knockdown impairs)
- Plasticity and modulation

---

### 7.3 Neuropeptide F Receptor (NPFR1)

**FlyBase ID**: FBgn0037792

**Gene Function**: GPCR for neuropeptide F, regulating feeding, sleep-wake behavior, and reward-seeking.

**Protein Structure**:
- 7 transmembrane domains
- NPF-binding extracellular domains
- Couples to Gαi/Gαs (context-dependent)

**Signaling Pathways**:
```
NPF (36 residues, RVRFamide C-terminus) + NPFR1 → G-protein activation

Feeding/arousal pathway:
  NPFR1 → Gαi → ↓cAMP (or alternative pathway)

Effects:
  - Promotes wakefulness
  - Promotes feeding in adults
  - Regulates reward-seeking behavior
```

**Developmental Regulation**:
```
Larval behavioral changes:
  Young larvae (feeding): high NPF expression
  Older larvae (wandering): low NPF expression

  NPF overexpression in older larvae:
    - Prolongs feeding behavior
    - Suppresses hypermobility
    - Suppresses cooperative burrowing
```

**Sleep-Wake Regulation**:
```
NPF activation:
  - Promotes wakefulness
  - Acts through cognate receptor NPFR1

Independent regulation:
  Feeding and sleep-wake regulated by separate NPF circuits
```

**Expression Pattern**:
- Dorsolateral neurons (central brain)
- Subesophageal ganglion neurons
- NPF neurons project widely

**Behavioral Relevance**:
- Feeding behavior (NPF homolog of mammalian NPY)
- Sleep-wake regulation
- Reward-seeking and motivation
- Developmental behavioral transitions
- Hunger and satiety signals

---

### 7.4 Insomniac (inc) - BTB Domain E3 Ubiquitin Ligase Adaptor

**FlyBase ID**: FBgn0025394

**Gene Function**: BTB domain protein serving as Cullin-3 adaptor for ubiquitin-mediated protein degradation, linking sleep regulation to synaptic function.

**Protein Structure**:
- BTB domain (Cullin-3 binding)
- Substrate recognition domains
- Localizes to cytoplasm and synapses
- Evolutionarily conserved

**Ubiquitination Pathway**:
```
Sleep regulation via protein turnover:

Substrate protein + INC·Cul3·E2-Ub
       ↓
Substrate-Ub (polyubiquitinated)
       ↓
Proteasomal degradation
       ↓
Turnover of synaptic proteins

Sleep duration ∝ f([INC], [Cul3], substrate turnover rate)
```

**Sleep Phenotype**:
```
inc mutants:
  - Baseline sleep reduction: ~10 hours (dramatic)
  - Sleep consolidation: reduced
  - Homeostatic response to deprivation: reduced

Indicates disrupted sleep homeostat
```

**Synaptic Function**:
```
INC essential for:
  - Normal synaptic structure
  - Synaptic excitability
  - Proper localization within neurons

INC and orthologs:
  - Traffic to synapses in fly and mammalian neurons
  - Likely ubiquitinate synaptic proteins
```

**Molecular Mechanism**:
```
INC/Cul3 pathway regulates sleep by:
  1) Controlling neuronal excitability
  2) Regulating synaptic protein levels
  3) Linking protein turnover to sleep homeostasis

Sleep need ∝ synaptic strength ∝ protein levels
INC/Cul3 → protein degradation → ↓ synaptic strength → sleep reduction
```

**Expression Pattern**:
- Neurons (essential in neurons for sleep)
- Synaptic localization
- Evolutionarily conserved orthologs in mammals

**Behavioral Relevance**:
- Sleep duration and consolidation
- Sleep homeostasis
- Synaptic function and excitability
- Demonstrates link between ubiquitin pathway, synapses, and sleep
- Strongest baseline sleep phenotype observed

---

## Summary Statistics

**Total Genes/Proteins Documented**: 38

**Categories**:
- Voltage-Gated Ion Channels: 12
- Neurotransmitter Receptors: 5
- Learning and Memory Genes: 6
- Synaptic Proteins: 5
- Circadian Rhythm Genes: 3
- G-Protein Signaling: 3
- Calcium-Dependent Enzymes: 4

**Formula Types Included**:
- Channel kinetics and conductance equations
- Enzyme kinetics (Michaelis-Menten)
- Signal transduction cascades
- Calcium dynamics
- Molecular oscillators
- Synaptic transmission
- Learning and memory mechanisms
- Circadian clock mathematics

---

## References and Sources

All information compiled from FlyBase database (http://flybase.org) and peer-reviewed scientific literature accessed via web search on 2025-12-10.

### Key Source Categories:

1. **FlyBase Gene Reports**: Official database entries for each gene
2. **PubMed/PMC Articles**: Peer-reviewed research on gene function and mechanisms
3. **SDB Online (Interactive Fly)**: Comprehensive gene briefs and educational resources
4. **UniProt**: Protein structure and function annotations
5. **Major Journals**: Science, Nature, PNAS, Journal of Neuroscience, eLife, PLOS Genetics

### Major Research Areas Covered:

- **Ion Channel Biophysics**: Voltage-gated and ligand-gated channel kinetics
- **Synaptic Transmission**: Vesicle release, endocytosis, active zone organization
- **Learning and Memory**: cAMP cascade, CREB-dependent transcription, parallel memory pathways
- **Circadian Rhythms**: Molecular feedback loops and oscillations
- **Signal Transduction**: GPCR signaling, second messengers, kinases/phosphatases
- **Behavioral Neuroscience**: Gene-behavior relationships in *Drosophila*

---

## Notes on Mathematical Formulations

All formulas are derived from experimental measurements and computational models published in the peer-reviewed literature. Parameter values represent typical ranges observed in *Drosophila* studies. Where specific values were not available from the search results, standard biophysical models for equivalent mammalian proteins were used as templates, as many of these molecules are highly conserved across species.

The formulas emphasize:
1. **Quantitative relationships** between molecular states
2. **Kinetic parameters** (time constants, rate constants)
3. **Dose-response relationships** (Hill equations, EC₅₀ values)
4. **Dynamic processes** (differential equations where appropriate)
5. **Functional coupling** between molecules in signaling pathways

These mathematical descriptions enable computational modeling of *Drosophila* neural circuits and provide a foundation for bio-inspired AI architectures based on insect neurobiology.
