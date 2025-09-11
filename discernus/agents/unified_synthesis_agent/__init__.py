"""
Unified Synthesis Agent for Discernus v10
=========================================

Generates publication-ready research reports using:
- Complete research data (raw scores, derived metrics, statistical results)
- Curated evidence from EvidenceRetriever
- THIN prompting approach with gemini-2.5-pro for reliability

Pure synthesis agent - no external lookups or RAG queries.
"""

# Copyright (C) 2025  Discernus Team

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


from .agent import UnifiedSynthesisAgent

__all__ = ['UnifiedSynthesisAgent']
