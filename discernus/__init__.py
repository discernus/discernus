"""
Discernus - Computational Social Science Research Platform
=========================================================

A THIN architecture platform for systematic discourse analysis using LLMs.

Main Components:
- CLI: Command-line interface for experiment execution
- Agents: THIN analysis agents with YAML prompts (direct function calls)  
- Core: Utilities for provenance, validation, and execution
- Gateway: LLM provider abstraction layer

Copyright (C) 2025  Discernus Team

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

__version__ = "0.2.0"
__author__ = "Discernus Team"

# Import key components for easy access (only if they exist)
try:
    from discernus.gateway.llm_gateway import LLMGateway
    _has_llm_gateway = True
except ImportError:
    _has_llm_gateway = False

try:
    from discernus.core.provenance_stamp import create_provenance_stamp
    _has_provenance = True
except ImportError:
    _has_provenance = False

__all__ = []
if _has_llm_gateway:
    __all__.append("LLMGateway")
if _has_provenance:
    __all__.append("create_provenance_stamp") 