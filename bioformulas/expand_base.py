#!/usr/bin/env python3
"""Base module for formula expansion - shared utilities and logging."""

import sqlite3
import logging
from pathlib import Path
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(message)s',
    datefmt='%H:%M:%S'
)
log = logging.getLogger('bioformulas')

DB_PATH = Path(__file__).parent / 'bioformulas.db'

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_source_id(conn, name):
    row = conn.execute("SELECT source_id FROM sources WHERE name = ?", (name,)).fetchone()
    return row[0] if row else None

def get_category_id(conn, name):
    row = conn.execute("SELECT category_id FROM categories WHERE name = ?", (name,)).fetchone()
    return row[0] if row else None

def add_category(conn, name, parent_name=None, description=None):
    parent_id = get_category_id(conn, parent_name) if parent_name else None
    conn.execute("""
        INSERT OR IGNORE INTO categories (name, parent_category_id, description)
        VALUES (?, ?, ?)
    """, (name, parent_id, description))
    conn.commit()
    return get_category_id(conn, name)

def add_formula(conn, name, latex, desc, ftype, cat_id, src_id, **kw):
    cur = conn.execute("""
        INSERT INTO formulas (name, latex, description, formula_type, category_id, source_id,
                              mathml, symbolic, python_code, domain, model_origin,
                              publication_doi, publication_year)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, latex, desc, ftype, cat_id, src_id,
          kw.get('mathml'), kw.get('symbolic'), kw.get('python_code'),
          kw.get('domain'), kw.get('model_origin'),
          kw.get('doi'), kw.get('year')))
    conn.commit()
    fid = cur.lastrowid
    log.info(f"➕ [{ftype}] {name}")
    return fid

def add_ion_channel(conn, fid, ch_type, gating, ngates=1, act=None, inact=None, erev=None, gmax=None):
    conn.execute("""
        INSERT INTO ion_channels (formula_id, channel_type, gating_type, num_gates,
                                  activation_var, inactivation_var, reversal_potential, max_conductance)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (fid, ch_type, gating, ngates, act, inact, erev, gmax))
    conn.commit()
    log.info(f"   ⚡ {ch_type}")

def add_synapse(conn, fid, syn_type, plast=None, trans=None, tau_r=None, tau_d=None, erev=None):
    conn.execute("""
        INSERT INTO synapses (formula_id, synapse_type, plasticity_type, transmission_type,
                              time_constant_rise, time_constant_decay, reversal_potential)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (fid, syn_type, plast, trans, tau_r, tau_d, erev))
    conn.commit()
    log.info(f"   🔗 {syn_type}")

def add_enzyme(conn, fid, name, ktype, sub=None, prod=None, km=None, vmax=None, kcat=None, ki=None, hill=None):
    conn.execute("""
        INSERT INTO enzyme_kinetics (formula_id, enzyme_name, kinetics_type, substrate, product,
                                     km, vmax, kcat, ki, hill_coefficient)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (fid, name, ktype, sub, prod, km, vmax, kcat, ki, hill))
    conn.commit()
    log.info(f"   🧬 {name}")

def add_neuron(conn, fid, mtype, ncomp=1, thresh=None, rest=None, cap=None, res=None, refr=None):
    conn.execute("""
        INSERT INTO neuron_models (formula_id, model_type, num_compartments,
                                   threshold_mv, resting_potential_mv, membrane_capacitance,
                                   membrane_resistance, refractory_period_ms)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (fid, mtype, ncomp, thresh, rest, cap, res, refr))
    conn.commit()
    log.info(f"   🧠 {mtype}")

def add_plasticity(conn, fid, rtype, tw_pre=None, tw_post=None, lr=None, wdep=None, ca_dep=False):
    conn.execute("""
        INSERT INTO plasticity_rules (formula_id, rule_type, time_window_pre, time_window_post,
                                      learning_rate, weight_dependence, calcium_dependent)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (fid, rtype, tw_pre, tw_post, lr, wdep, ca_dep))
    conn.commit()
    log.info(f"   📈 {rtype}")

def count_formulas(conn):
    return conn.execute("SELECT COUNT(*) FROM formulas").fetchone()[0]

def print_summary(conn, module_name, start_count):
    end_count = count_formulas(conn)
    added = end_count - start_count
    log.info(f"{'='*50}")
    log.info(f"{module_name}: Added {added} formulas (Total: {end_count})")
    log.info(f"{'='*50}")
