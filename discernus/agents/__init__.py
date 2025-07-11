#!/usr/bin/env python3
"""
Discernus Agents Package
========================

SOAR agents for Simple Atomic Orchestration Research.
Following THIN principles - agents defined by text prompts, not code.
"""

# Version info
__version__ = "1.0.0"

# Import key agents
from .validation_agent import ValidationAgent

__all__ = ['ValidationAgent'] 