"""
Narrative Gravity Corpus Management System

Enhanced corpus management with stable identifiers, FAIR data principles,
and academic standards compliance.

Core Components:
- CorpusRegistry: Central registry with stable URIs
- CorpusValidator: Validation and integrity checking
- CorpusDiscovery: Search and exploration tools
- CorpusExporter: Academic format exports
"""

from .registry import CorpusRegistry, CorpusDocument
from .validator import CorpusValidator
from .discovery import CorpusDiscovery
from .exporter import CorpusExporter

__all__ = [
    'CorpusRegistry',
    'CorpusDocument', 
    'CorpusValidator',
    'CorpusDiscovery',
    'CorpusExporter'
]

__version__ = '1.0.0' 