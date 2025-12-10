"""
Analyze Extracted Biological Data for Computational Primitives

Identifies architectural patterns, computational operations, and
system primitives from the extracted biological database entities.
"""

import json
from collections import defaultdict, Counter
from pathlib import Path
from typing import Dict, List, Any
import re


class BiologicalDataAnalyzer:
    """Analyze extracted biological data for computational patterns"""

    def __init__(self, results_dir: str = "extraction_results"):
        self.results_dir = Path(results_dir)
        self.data = {}
        self.load_all_data()

    def load_all_data(self):
        """Load all parallel extraction results"""
        json_files = list(self.results_dir.glob("*_parallel.json"))

        for file in json_files:
            db_name = file.stem.replace("_parallel", "")
            try:
                with open(file, 'r') as f:
                    content = f.read().strip()
                    if content and content != "[]":
                        self.data[db_name] = json.loads(content)
                        print(f"✓ Loaded {len(self.data[db_name])} entities from {db_name}")
                    else:
                        self.data[db_name] = []
                        print(f"✗ No data in {db_name}")
            except Exception as e:
                print(f"✗ Error loading {db_name}: {e}")
                self.data[db_name] = []

    def analyze_entity_types(self) -> Dict[str, int]:
        """Count entity types across all databases"""
        type_counts = Counter()

        for db_name, entities in self.data.items():
            for entity in entities:
                entity_type = entity.get('entity_type', 'unknown')
                type_counts[entity_type] += 1

        return dict(type_counts)

    def identify_computational_primitives(self) -> Dict[str, List[str]]:
        """Identify computational operations from cognitive data"""
        primitives = defaultdict(list)

        if 'CognitiveAtlas' in self.data:
            for entity in self.data['CognitiveAtlas']:
                name = entity.get('name', '').lower()
                operation_type = entity['metadata'].get('operation_type', 'unknown')

                # Categorize by computational pattern
                if any(x in name for x in ['memory', 'working', 'recall', 'retrieval']):
                    primitives['memory_operations'].append(entity['name'])
                elif any(x in name for x in ['attention', 'focus', 'selective']):
                    primitives['attention_control'].append(entity['name'])
                elif any(x in name for x in ['decision', 'choice', 'selection']):
                    primitives['decision_making'].append(entity['name'])
                elif any(x in name for x in ['learning', 'acquisition', 'encoding']):
                    primitives['learning_mechanisms'].append(entity['name'])
                elif any(x in name for x in ['reasoning', 'inference', 'logic']):
                    primitives['reasoning_systems'].append(entity['name'])
                elif any(x in name for x in ['motor', 'movement', 'execution']):
                    primitives['motor_control'].append(entity['name'])
                elif any(x in name for x in ['perception', 'sensory', 'detection']):
                    primitives['perception_systems'].append(entity['name'])
                elif any(x in name for x in ['language', 'speech', 'linguistic']):
                    primitives['language_processing'].append(entity['name'])
                else:
                    primitives['other_operations'].append(entity['name'])

        return dict(primitives)

    def identify_network_architectures(self) -> Dict[str, List[str]]:
        """Identify network structures from Allen Brain data"""
        architectures = defaultdict(list)

        if 'AllenBrain' in self.data:
            for entity in self.data['AllenBrain']:
                name = entity.get('name', '').lower()
                acronym = entity['metadata'].get('acronym', '')

                # Categorize by system
                if any(x in name for x in ['cortex', 'cortical', 'layer']):
                    architectures['cortical_structures'].append(f"{entity['name']} [{acronym}]")
                elif any(x in name for x in ['hippocampus', 'hippocampal']):
                    architectures['hippocampal_system'].append(f"{entity['name']} [{acronym}]")
                elif any(x in name for x in ['thalamus', 'thalamic']):
                    architectures['thalamic_system'].append(f"{entity['name']} [{acronym}]")
                elif any(x in name for x in ['hypothalamus', 'hypothalamic']):
                    architectures['hypothalamic_system'].append(f"{entity['name']} [{acronym}]")
                elif any(x in name for x in ['cerebellum', 'cerebellar']):
                    architectures['cerebellar_system'].append(f"{entity['name']} [{acronym}]")
                elif any(x in name for x in ['striatum', 'striatal', 'basal ganglia']):
                    architectures['basal_ganglia'].append(f"{entity['name']} [{acronym}]")
                elif any(x in name for x in ['amygdala', 'amygdalar']):
                    architectures['amygdala_system'].append(f"{entity['name']} [{acronym}]")
                elif any(x in name for x in ['fiber', 'tract', 'pathway', 'bundle']):
                    architectures['connectivity_pathways'].append(f"{entity['name']} [{acronym}]")
                else:
                    architectures['other_structures'].append(f"{entity['name']} [{acronym}]")

        return dict(architectures)

    def identify_metabolic_patterns(self) -> Dict[str, List[str]]:
        """Identify metabolic pathway patterns from KEGG"""
        patterns = defaultdict(list)

        if 'KEGG' in self.data:
            for entity in self.data['KEGG']:
                name = entity.get('name', '').lower()

                # Categorize metabolic pathways
                if any(x in name for x in ['signal', 'signaling']):
                    patterns['signaling_pathways'].append(entity['name'])
                elif any(x in name for x in ['metabol', 'synthesis', 'degradation']):
                    patterns['metabolic_pathways'].append(entity['name'])
                elif any(x in name for x in ['cancer', 'disease', 'infection']):
                    patterns['disease_pathways'].append(entity['name'])
                elif any(x in name for x in ['transport', 'secretion', 'trafficking']):
                    patterns['transport_systems'].append(entity['name'])
                elif any(x in name for x in ['immune', 'inflammatory']):
                    patterns['immune_pathways'].append(entity['name'])
                elif any(x in name for x in ['neuro', 'synaptic']):
                    patterns['neuro_pathways'].append(entity['name'])
                else:
                    patterns['other_pathways'].append(entity['name'])

        return dict(patterns)

    def generate_summary_report(self) -> str:
        """Generate comprehensive analysis report"""
        report = []
        report.append("=" * 80)
        report.append("BIOLOGICAL DATABASE EXTRACTION ANALYSIS")
        report.append("=" * 80)
        report.append("")

        # Overall statistics
        total_entities = sum(len(entities) for entities in self.data.values())
        report.append(f"📊 Total Entities Extracted: {total_entities}")
        report.append(f"📦 Databases: {len(self.data)}")
        report.append("")

        # Per-database breakdown
        report.append("=" * 80)
        report.append("DATABASE BREAKDOWN")
        report.append("=" * 80)
        for db_name, entities in sorted(self.data.items()):
            report.append(f"  {db_name:20s} : {len(entities):4d} entities")
        report.append("")

        # Entity types
        report.append("=" * 80)
        report.append("ENTITY TYPES")
        report.append("=" * 80)
        entity_types = self.analyze_entity_types()
        for entity_type, count in sorted(entity_types.items(), key=lambda x: -x[1]):
            report.append(f"  {entity_type:20s} : {count:4d}")
        report.append("")

        # Computational primitives
        report.append("=" * 80)
        report.append("COMPUTATIONAL PRIMITIVES (Cognitive Atlas)")
        report.append("=" * 80)
        primitives = self.identify_computational_primitives()
        for category, operations in sorted(primitives.items()):
            report.append(f"\n  {category.upper().replace('_', ' ')} ({len(operations)} operations):")
            for op in sorted(operations)[:10]:  # Show first 10
                report.append(f"    - {op}")
            if len(operations) > 10:
                report.append(f"    ... and {len(operations) - 10} more")
        report.append("")

        # Network architectures
        report.append("=" * 80)
        report.append("NETWORK ARCHITECTURES (Allen Brain Atlas)")
        report.append("=" * 80)
        architectures = self.identify_network_architectures()
        for system, structures in sorted(architectures.items()):
            report.append(f"\n  {system.upper().replace('_', ' ')} ({len(structures)} structures):")
            for struct in sorted(structures)[:8]:  # Show first 8
                report.append(f"    - {struct}")
            if len(structures) > 8:
                report.append(f"    ... and {len(structures) - 8} more")
        report.append("")

        # Metabolic patterns
        report.append("=" * 80)
        report.append("METABOLIC PATTERNS (KEGG)")
        report.append("=" * 80)
        patterns = self.identify_metabolic_patterns()
        for category, pathways in sorted(patterns.items()):
            report.append(f"\n  {category.upper().replace('_', ' ')} ({len(pathways)} pathways):")
            for pathway in sorted(pathways)[:8]:  # Show first 8
                report.append(f"    - {pathway}")
            if len(pathways) > 8:
                report.append(f"    ... and {len(pathways) - 8} more")
        report.append("")

        # Key insights
        report.append("=" * 80)
        report.append("KEY COMPUTATIONAL INSIGHTS")
        report.append("=" * 80)
        report.append("")
        report.append("🧠 COGNITIVE OPERATIONS IDENTIFIED:")
        report.append(f"   - {len(primitives.get('memory_operations', []))} memory primitives")
        report.append(f"   - {len(primitives.get('attention_control', []))} attention mechanisms")
        report.append(f"   - {len(primitives.get('decision_making', []))} decision systems")
        report.append(f"   - {len(primitives.get('learning_mechanisms', []))} learning operations")
        report.append(f"   - {len(primitives.get('reasoning_systems', []))} reasoning primitives")
        report.append("")
        report.append("🏗️ ARCHITECTURAL STRUCTURES IDENTIFIED:")
        report.append(f"   - {len(architectures.get('cortical_structures', []))} cortical regions")
        report.append(f"   - {len(architectures.get('hippocampal_system', []))} hippocampal structures")
        report.append(f"   - {len(architectures.get('connectivity_pathways', []))} connectivity pathways")
        report.append(f"   - {len(architectures.get('basal_ganglia', []))} basal ganglia components")
        report.append("")
        report.append("⚡ METABOLIC SYSTEMS IDENTIFIED:")
        report.append(f"   - {len(patterns.get('signaling_pathways', []))} signaling pathways")
        report.append(f"   - {len(patterns.get('metabolic_pathways', []))} metabolic networks")
        report.append(f"   - {len(patterns.get('neuro_pathways', []))} neuro-specific pathways")
        report.append("")
        report.append("=" * 80)

        return "\n".join(report)


def main():
    """Run analysis and generate report"""
    print("\n🔬 Analyzing extracted biological data...\n")

    analyzer = BiologicalDataAnalyzer()
    report = analyzer.generate_summary_report()

    # Print to console
    print(report)

    # Save to file
    output_file = "extraction_results/ANALYSIS_REPORT.txt"
    with open(output_file, 'w') as f:
        f.write(report)

    print(f"\n✓ Analysis saved to: {output_file}")


if __name__ == '__main__':
    main()
