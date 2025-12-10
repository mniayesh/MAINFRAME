"""
Biological Database Extraction Framework

A production-ready framework for extracting architectural primitives from biological databases.

Modules:
    base: Base extractor class with rate limiting, caching, and retry logic
    mechanisms_extractors: GO, Reactome, KEGG pathways
    neuroscience_extractors: Allen Brain Atlas, NeuroMorpho, Cell Ontology
    protein_extractors: UniProt, InterPro, BRENDA
    metabolic_extractors: ChEBI, eQuilibrator
    cognitive_extractors: Cognitive Atlas, CogPO via BioPortal

Usage:
    from bio_extractors import MechanismExtractor

    extractor = MechanismExtractor()
    go_terms = extractor.extract_go_mechanisms()
"""

__version__ = "1.0.0"
__author__ = "BioArchitecture Team"

from .base import BaseExtractor, ExtractionError, RateLimitError
from .mechanisms_extractors import GOExtractor, ReactomeExtractor, KEGGExtractor
from .neuroscience_extractors import AllenBrainExtractor, NeuroMorphoExtractor, CellOntologyExtractor
from .protein_extractors import UniProtExtractor, InterProExtractor, BRENDAExtractor
from .metabolic_extractors import ChEBIExtractor, EQuilibratorExtractor
from .cognitive_extractors import CognitiveAtlasExtractor, CogPOExtractor

__all__ = [
    'BaseExtractor',
    'ExtractionError',
    'RateLimitError',
    'GOExtractor',
    'ReactomeExtractor',
    'KEGGExtractor',
    'AllenBrainExtractor',
    'NeuroMorphoExtractor',
    'CellOntologyExtractor',
    'UniProtExtractor',
    'InterProExtractor',
    'BRENDAExtractor',
    'ChEBIExtractor',
    'EQuilibratorExtractor',
    'CognitiveAtlasExtractor',
    'CogPOExtractor',
]
