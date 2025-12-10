#!/usr/bin/env python3
"""
Harvest formulas from NeuroML database.
NeuroML: https://neuroml.org/
Open Source Brain: https://www.opensourcebrain.org/
"""

import requests
import xml.etree.ElementTree as ET
from pathlib import Path
import logging
import time
from expand_base import get_conn, add_formula, get_source_id, get_category_id
from expand_base import add_ion_channel, add_synapse, print_summary, count_formulas

log = logging.getLogger('bioformulas.neuroml')

# NeuroML namespaces
NML_NS = {
    'nml': 'http://www.neuroml.org/schema/neuroml2',
    'nml1': 'http://morphml.org/neuroml/schema'
}

OSB_API = "https://www.opensourcebrain.org/projects.json"


class NeuroMLHarvester:
    """Extract formulas from NeuroML files."""

    def __init__(self, conn, output_dir='data/neuroml'):
        self.conn = conn
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.source_id = get_source_id(conn, 'NeuroML')
        self.stats = {'models_processed': 0, 'formulas_extracted': 0, 'errors': 0}

    def parse_hh_channel(self, channel_elem, model_id):
        """Parse Hodgkin-Huxley style ion channel."""
        formulas = []

        try:
            chan_id = channel_elem.get('id', 'unknown')
            ion_type = channel_elem.get('species', 'unknown')

            # Gate dynamics
            for gate in channel_elem.findall('.//nml:gate', NML_NS):
                gate_id = gate.get('id', 'unknown')
                power = gate.get('instances', '1')

                # Forward/reverse rates
                fwd_rate = gate.find('.//nml:forwardRate', NML_NS)
                rev_rate = gate.find('.//nml:reverseRate', NML_NS)

                if fwd_rate is not None:
                    rate_expr = self.extract_rate_expression(fwd_rate)
                    if rate_expr:
                        formulas.append({
                            'name': f"{model_id}: {chan_id} {gate_id} forward rate",
                            'latex': f"\\alpha_{{{gate_id}}} = {rate_expr}",
                            'description': f"{chan_id} gate {gate_id} forward rate",
                            'formula_type': 'rate_equation',
                            'domain': 'ion-channels',
                            'model_origin': model_id
                        })

                if rev_rate is not None:
                    rate_expr = self.extract_rate_expression(rev_rate)
                    if rate_expr:
                        formulas.append({
                            'name': f"{model_id}: {chan_id} {gate_id} reverse rate",
                            'latex': f"\\beta_{{{gate_id}}} = {rate_expr}",
                            'description': f"{chan_id} gate {gate_id} reverse rate",
                            'formula_type': 'rate_equation',
                            'domain': 'ion-channels',
                            'model_origin': model_id
                        })

                # Gate ODE
                formulas.append({
                    'name': f"{model_id}: {chan_id} {gate_id} dynamics",
                    'latex': f"\\frac{{d{gate_id}}}{{dt}} = \\alpha_{{{gate_id}}}(V)(1-{gate_id}) - \\beta_{{{gate_id}}}(V){gate_id}",
                    'description': f"{chan_id} gating variable {gate_id}",
                    'formula_type': 'ODE',
                    'domain': 'ion-channels',
                    'model_origin': model_id
                })

        except Exception as e:
            log.warning(f"  Error parsing HH channel: {e}")

        return formulas

    def extract_rate_expression(self, rate_elem):
        """Extract rate expression from NeuroML rate element."""
        # HHExpLinearRate, HHExpRate, HHSigmoidRate, etc.
        rate_type = rate_elem.get('type', '')

        if 'ExpLinear' in rate_type:
            rate = rate_elem.get('rate')
            midpoint = rate_elem.get('midpoint')
            scale = rate_elem.get('scale')
            return f"\\frac{{{rate}(V-{midpoint})}}{{{scale}(1-\\exp(-(V-{midpoint})/{scale}))}}"

        elif 'Exp' in rate_type:
            rate = rate_elem.get('rate')
            midpoint = rate_elem.get('midpoint')
            scale = rate_elem.get('scale')
            return f"{rate} \\exp((V-{midpoint})/{scale})"

        elif 'Sigmoid' in rate_type:
            rate = rate_elem.get('rate')
            midpoint = rate_elem.get('midpoint')
            scale = rate_elem.get('scale')
            return f"\\frac{{{rate}}}{{1 + \\exp(-(V-{midpoint})/{scale})}}"

        return "unknown"

    def parse_synapse(self, syn_elem, model_id):
        """Parse synapse model."""
        formulas = []

        try:
            syn_id = syn_elem.get('id', 'unknown')
            tau_decay = syn_elem.get('tauDecay')
            tau_rise = syn_elem.get('tauRise')
            erev = syn_elem.get('erev')

            if tau_decay:
                formulas.append({
                    'name': f"{model_id}: {syn_id} synapse",
                    'latex': f"I = g_{{max}} s (V - E_{{rev}}), \\quad \\tau_{{decay}}={tau_decay}",
                    'description': f"Synaptic current from {syn_id}",
                    'formula_type': 'current_equation',
                    'domain': 'synapses',
                    'model_origin': model_id
                })

        except Exception as e:
            log.warning(f"  Error parsing synapse: {e}")

        return formulas

    def process_neuroml_file(self, filepath, model_id):
        """Parse a NeuroML file."""
        formulas = []

        try:
            tree = ET.parse(filepath)
            root = tree.getroot()

            # Ion channels
            for channel in root.findall('.//nml:ionChannelHH', NML_NS):
                formulas.extend(self.parse_hh_channel(channel, model_id))

            # Synapses
            for syn in root.findall('.//nml:expTwoSynapse', NML_NS):
                formulas.extend(self.parse_synapse(syn, model_id))

            for syn in root.findall('.//nml:expOneSynapse', NML_NS):
                formulas.extend(self.parse_synapse(syn, model_id))

        except Exception as e:
            log.error(f"  Error parsing NeuroML: {e}")

        return formulas

    def save_formulas(self, formulas):
        """Save formulas to database."""
        for f in formulas:
            try:
                cat_id = None
                if 'ion' in f.get('domain', ''):
                    cat_id = get_category_id(self.conn, 'Ion Channels')
                elif 'synap' in f.get('domain', ''):
                    cat_id = get_category_id(self.conn, 'Synaptic Transmission')

                if not cat_id:
                    cat_id = get_category_id(self.conn, 'Neuroscience')

                add_formula(
                    self.conn,
                    name=f['name'],
                    latex=f['latex'],
                    desc=f['description'],
                    ftype=f['formula_type'],
                    cat_id=cat_id,
                    src_id=self.source_id,
                    domain=f.get('domain'),
                    model_origin=f.get('model_origin')
                )

            except Exception as e:
                log.warning(f"  Error saving formula: {e}")

    def harvest(self, sample_files=None):
        """
        Harvest NeuroML formulas.

        Args:
            sample_files: List of local .nml files to process
        """
        log.info("="*60)
        log.info("NeuroML Harvester Starting")
        log.info("="*60)

        start_count = count_formulas(self.conn)

        # For now, process sample files
        # TODO: Add OSB API integration to download models

        if sample_files:
            all_formulas = []
            for filepath in sample_files:
                log.info(f"Processing {filepath}")
                formulas = self.process_neuroml_file(filepath, Path(filepath).stem)
                all_formulas.extend(formulas)

            self.save_formulas(all_formulas)
            self.stats['formulas_extracted'] = len(all_formulas)

        log.info("="*60)
        log.info(f"NeuroML Harvest Complete")
        log.info(f"  Formulas extracted: {self.stats['formulas_extracted']}")
        log.info("="*60)

        print_summary(self.conn, "NeuroML", start_count)


def main():
    """Run NeuroML harvester."""
    conn = get_conn()

    try:
        harvester = NeuroMLHarvester(conn)
        # To use: provide paths to .nml files
        # harvester.harvest(sample_files=['example.nml'])
        log.info("NeuroML harvester ready. Provide .nml files to process.")

    finally:
        conn.close()


if __name__ == '__main__':
    main()
