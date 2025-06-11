"""
Manual Development Support Module - Priority 2 Infrastructure

This module provides structured development workflows, session management,
and quality assurance tools for systematic component development.

Components:
- Seed prompt library for standardized development approaches
- Development session management and tracking
- Quality assurance frameworks and validation tools
- Component-specific development protocols
"""

from .seed_prompts import SeedPromptLibrary
from .session_manager import DevelopmentSessionManager  
from .quality_assurance import ComponentQualityValidator

__all__ = [
    'SeedPromptLibrary',
    'DevelopmentSessionManager', 
    'ComponentQualityValidator'
] 