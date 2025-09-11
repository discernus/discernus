#!/usr/bin/env python3
"""
Discernus Agents - THIN v2.0 Architecture
=========================================

THIN v2.0 compliant agents with minimal intelligence and LLM-driven processing.
"""

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


# THIN v2.0 Active Agents
from .EnhancedAnalysisAgent.main import EnhancedAnalysisAgent
from .automated_derived_metrics import AutomatedDerivedMetricsAgent

__all__ = [
    "EnhancedAnalysisAgent",
    "AutomatedDerivedMetricsAgent",
] 