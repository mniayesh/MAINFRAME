"""
Biological → Computational Architecture Mapping

Maps extracted biological primitives to computational architecture patterns
and system design principles.
"""

import json
from pathlib import Path
from typing import Dict, List, Tuple


class ComputationalMapper:
    """Map biological primitives to computational architectures"""

    def __init__(self):
        self.results_dir = Path("extraction_results")
        self.cognitive_data = []
        self.brain_structures = []
        self.pathways = []
        self.load_data()

    def load_data(self):
        """Load extracted data"""
        # Load cognitive data
        cog_file = self.results_dir / "CognitiveAtlas_parallel.json"
        if cog_file.exists():
            with open(cog_file) as f:
                self.cognitive_data = json.load(f)

        # Load brain structures
        brain_file = self.results_dir / "AllenBrain_parallel.json"
        if brain_file.exists():
            with open(brain_file) as f:
                self.brain_structures = json.load(f)

        # Load pathways
        kegg_file = self.results_dir / "KEGG_parallel.json"
        if kegg_file.exists():
            with open(kegg_file) as f:
                self.pathways = json.load(f)

    def map_cognitive_to_os(self) -> List[Tuple[str, str, str, float]]:
        """Map cognitive operations to OS-level primitives"""
        mappings = []

        for entity in self.cognitive_data:
            name = entity['name'].lower()
            bio_op = entity['name']
            comp_primitive = None
            fidelity = 0.0

            # Attention → Interrupt handling / Scheduler
            if 'attention' in name:
                comp_primitive = "Interrupt Handler / Process Scheduler"
                fidelity = 0.92
                desc = "Selective filtering and priority management of incoming signals"

            # Memory operations → Memory hierarchy
            elif any(x in name for x in ['memory', 'recall', 'retrieval']):
                comp_primitive = "Memory Hierarchy (Cache/RAM/Disk)"
                fidelity = 0.88
                desc = "Multi-level storage with different access latencies"

            # Learning → Weight updates / Parameter optimization
            elif 'learning' in name or 'encoding' in name:
                comp_primitive = "Gradient Descent / Parameter Update"
                fidelity = 0.85
                desc = "Iterative optimization of system parameters"

            # Reasoning → Logic engine / Inference system
            elif any(x in name for x in ['reasoning', 'inference']):
                comp_primitive = "Inference Engine / Theorem Prover"
                fidelity = 0.82
                desc = "Logical deduction and pattern matching"

            # Adaptation → Adaptive algorithms
            elif 'adaptation' in name or 'adaptive' in name:
                comp_primitive = "Adaptive Algorithm / Online Learning"
                fidelity = 0.87
                desc = "Dynamic parameter adjustment based on feedback"

            # Association → Hash table / Associative memory
            elif 'association' in name or 'associative' in name:
                comp_primitive = "Associative Array / Content-Addressable Memory"
                fidelity = 0.90
                desc = "Key-value lookup and pattern association"

            # Action → Command execution
            elif 'action' in name or 'execution' in name:
                comp_primitive = "Command Executor / Action Dispatcher"
                fidelity = 0.85
                desc = "Execution of commands and motor programs"

            # Default
            else:
                comp_primitive = "General Computation Module"
                fidelity = 0.70
                desc = "Generic computational operation"

            if comp_primitive:
                mappings.append((bio_op, comp_primitive, desc, fidelity))

        return mappings

    def map_structures_to_architecture(self) -> List[Tuple[str, str, str, float]]:
        """Map brain structures to system architectures"""
        mappings = []

        for entity in self.brain_structures:
            name = entity['name'].lower()
            acronym = entity['metadata'].get('acronym', '')
            bio_struct = f"{entity['name']} [{acronym}]"
            arch_pattern = None
            fidelity = 0.0

            # Cortical layers → Hierarchical processing pipeline
            if 'layer' in name and 'cortex' in name:
                arch_pattern = "Hierarchical Processing Pipeline"
                fidelity = 0.89
                desc = "Layered abstraction with feed-forward and feedback"

            # Hippocampus → Content-addressable memory
            elif 'hippocampus' in name or 'ca1' in name or 'ca3' in name:
                arch_pattern = "Content-Addressable Memory / Pattern Completion"
                fidelity = 0.91
                desc = "Sparse distributed memory with pattern completion"

            # Thalamus → Router / Message broker
            elif 'thalamus' in name or 'thalamic' in name:
                arch_pattern = "Router / Message Broker"
                fidelity = 0.88
                desc = "Central relay and routing of information streams"

            # Cerebellum → Error correction / PID controller
            elif 'cerebellum' in name or 'cerebellar' in name:
                arch_pattern = "PID Controller / Error Correction System"
                fidelity = 0.87
                desc = "Predictive error correction and motor control"

            # Fiber tracts → Network interconnects
            elif any(x in name for x in ['fiber', 'tract', 'bundle']):
                arch_pattern = "Network Interconnect / Bus System"
                fidelity = 0.90
                desc = "High-bandwidth communication pathways"

            # Amygdala → Threat detection / Anomaly detector
            elif 'amygdala' in name:
                arch_pattern = "Anomaly Detector / Threat Assessment"
                fidelity = 0.85
                desc = "Real-time threat detection and valence assignment"

            # Cortex general → Processing unit
            elif 'cortex' in name or 'cortical' in name:
                arch_pattern = "Processing Core / Compute Unit"
                fidelity = 0.82
                desc = "General-purpose computational substrate"

            # Default
            else:
                arch_pattern = "Neural Network Module"
                fidelity = 0.75
                desc = "Specialized neural computation unit"

            if arch_pattern:
                mappings.append((bio_struct, arch_pattern, desc, fidelity))

        return mappings

    def map_pathways_to_systems(self) -> List[Tuple[str, str, str, float]]:
        """Map metabolic pathways to system-level patterns"""
        mappings = []

        for entity in self.pathways:
            name = entity['name'].lower()
            bio_pathway = entity['name']
            system_pattern = None
            fidelity = 0.0

            # Signaling → Event-driven architecture
            if 'signal' in name:
                system_pattern = "Event-Driven Architecture / Pub-Sub System"
                fidelity = 0.86
                desc = "Asynchronous message passing and event propagation"

            # Metabolic pathways → Data processing pipeline
            elif any(x in name for x in ['metabol', 'synthesis', 'degradation']):
                system_pattern = "Data Processing Pipeline / ETL System"
                fidelity = 0.84
                desc = "Sequential transformation and processing of inputs"

            # Glycolysis / TCA → Energy management
            elif any(x in name for x in ['glycolysis', 'tca', 'citrate', 'oxidative']):
                system_pattern = "Power Management / Resource Allocation"
                fidelity = 0.88
                desc = "Energy production and resource distribution"

            # Amino acid metabolism → Resource pool management
            elif 'amino acid' in name or 'biosynthesis' in name:
                system_pattern = "Resource Pool / Object Pool Pattern"
                fidelity = 0.82
                desc = "Reusable resource management and allocation"

            # Carbon metabolism → Core processing loop
            elif 'carbon' in name:
                system_pattern = "Core Event Loop / Central Processing"
                fidelity = 0.85
                desc = "Fundamental processing cycle"

            # Transport → Message passing
            elif 'transport' in name:
                system_pattern = "Message Passing Interface / IPC"
                fidelity = 0.87
                desc = "Inter-process communication and data transfer"

            # Default
            else:
                system_pattern = "Processing Subsystem"
                fidelity = 0.70
                desc = "Specialized processing module"

            if system_pattern:
                mappings.append((bio_pathway, system_pattern, desc, fidelity))

        return mappings

    def generate_mapping_report(self) -> str:
        """Generate comprehensive mapping report"""
        report = []
        report.append("=" * 100)
        report.append("BIOLOGICAL → COMPUTATIONAL ARCHITECTURE MAPPING")
        report.append("=" * 100)
        report.append("")

        # Cognitive mappings
        report.append("🧠 COGNITIVE OPERATIONS → OS PRIMITIVES")
        report.append("=" * 100)
        cog_mappings = self.map_cognitive_to_os()
        report.append(f"Total mappings: {len(cog_mappings)}\n")

        for bio, comp, desc, fidelity in sorted(cog_mappings, key=lambda x: -x[3])[:15]:
            report.append(f"  Biological: {bio}")
            report.append(f"  Computational: {comp}")
            report.append(f"  Description: {desc}")
            report.append(f"  Fidelity: {fidelity:.2f}")
            report.append("")

        # Structure mappings
        report.append("=" * 100)
        report.append("🏗️ BRAIN STRUCTURES → SYSTEM ARCHITECTURES")
        report.append("=" * 100)
        struct_mappings = self.map_structures_to_architecture()
        report.append(f"Total mappings: {len(struct_mappings)}\n")

        for bio, arch, desc, fidelity in sorted(struct_mappings, key=lambda x: -x[3])[:15]:
            report.append(f"  Biological: {bio}")
            report.append(f"  Architecture: {arch}")
            report.append(f"  Description: {desc}")
            report.append(f"  Fidelity: {fidelity:.2f}")
            report.append("")

        # Pathway mappings
        report.append("=" * 100)
        report.append("⚡ METABOLIC PATHWAYS → SYSTEM PATTERNS")
        report.append("=" * 100)
        pathway_mappings = self.map_pathways_to_systems()
        report.append(f"Total mappings: {len(pathway_mappings)}\n")

        for bio, pattern, desc, fidelity in sorted(pathway_mappings, key=lambda x: -x[3])[:15]:
            report.append(f"  Biological: {bio}")
            report.append(f"  System Pattern: {pattern}")
            report.append(f"  Description: {desc}")
            report.append(f"  Fidelity: {fidelity:.2f}")
            report.append("")

        # Summary statistics
        report.append("=" * 100)
        report.append("MAPPING STATISTICS")
        report.append("=" * 100)
        avg_cog_fidelity = sum(x[3] for x in cog_mappings) / len(cog_mappings) if cog_mappings else 0
        avg_struct_fidelity = sum(x[3] for x in struct_mappings) / len(struct_mappings) if struct_mappings else 0
        avg_pathway_fidelity = sum(x[3] for x in pathway_mappings) / len(pathway_mappings) if pathway_mappings else 0

        report.append(f"  Cognitive Operations: {len(cog_mappings)} mappings, avg fidelity {avg_cog_fidelity:.3f}")
        report.append(f"  Brain Structures: {len(struct_mappings)} mappings, avg fidelity {avg_struct_fidelity:.3f}")
        report.append(f"  Metabolic Pathways: {len(pathway_mappings)} mappings, avg fidelity {avg_pathway_fidelity:.3f}")
        report.append(f"  Overall: {len(cog_mappings) + len(struct_mappings) + len(pathway_mappings)} total mappings")
        report.append("")

        # Key insights
        report.append("=" * 100)
        report.append("KEY ARCHITECTURAL INSIGHTS")
        report.append("=" * 100)
        report.append("")
        report.append("💡 HIGH-FIDELITY MAPPINGS (>0.90):")
        all_mappings = cog_mappings + struct_mappings + pathway_mappings
        high_fidelity = [m for m in all_mappings if m[3] > 0.90]
        for bio, comp, desc, fidelity in sorted(high_fidelity, key=lambda x: -x[3]):
            report.append(f"  • {bio[:60]:60s} → {comp} (fidelity: {fidelity:.2f})")
        report.append("")

        report.append("🎯 ARCHITECTURAL PATTERNS DISCOVERED:")
        patterns = set(m[1] for m in struct_mappings)
        for pattern in sorted(patterns):
            count = len([m for m in struct_mappings if m[1] == pattern])
            report.append(f"  • {pattern}: {count} biological implementations")
        report.append("")

        report.append("=" * 100)

        return "\n".join(report)


def main():
    """Run mapping analysis"""
    print("\n🔬 Mapping biological primitives to computational architectures...\n")

    mapper = ComputationalMapper()
    report = mapper.generate_mapping_report()

    # Print to console
    print(report)

    # Save to file
    output_file = "extraction_results/COMPUTATIONAL_MAPPING_ANALYSIS.txt"
    with open(output_file, 'w') as f:
        f.write(report)

    print(f"\n✓ Mapping analysis saved to: {output_file}")


if __name__ == '__main__':
    main()
