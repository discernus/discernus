#!/usr/bin/env python3
"""
Corpus Tools Package

This package provides tools for corpus management, including transcript extraction,
text processing, and corpus validation utilities.
"""

# Import new durable infrastructure
from .transcript_extractor import TranscriptExtractor
from .extraction_result import (
    ExtractionResult, VideoInfo, QualityMetrics,
    ExtractionError, YouTubeAPIError, WhisperError, NetworkError, ContentUnavailableError
)

__all__ = [
    'TranscriptExtractor', 
    'ExtractionResult',
    'VideoInfo',
    'QualityMetrics',
    'ExtractionError',
    'YouTubeAPIError',
    'WhisperError',
    'NetworkError',
    'ContentUnavailableError'
]

__version__ = "2.0.0"
