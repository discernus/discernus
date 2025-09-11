#!/usr/bin/env python3
"""
Framework Parser - THIN Component
=================================

Extracts dimensions and configuration from framework markdown files.
Pure software component - no LLM intelligence.
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


import json
import re
from typing import Dict, Any, List
from dataclasses import dataclass


@dataclass
class FrameworkConfig:
    """Parsed framework configuration."""
    dimensions: List[str]
    dimension_groups: Dict[str, List[str]]
    raw_config: Dict[str, Any]
    framework_hash: str


class FrameworkParser:
    """
    Parses framework markdown files to extract dimensions and configuration.
    
    THIN Principle: Pure software component with no LLM intelligence.
    Handles the mechanical task of parsing JSON from markdown.
    """
    
    def parse_framework(self, framework_content: str, framework_hash: str) -> FrameworkConfig:
        """
        Extract framework configuration from markdown content.
        
        Args:
            framework_content: Raw framework markdown content
            framework_hash: Hash of the framework content for tracking
            
        Returns:
            FrameworkConfig with parsed dimensions and metadata
        """
        # Extract JSON appendix from framework
        json_pattern = r"```json\n(.*?)\n```"
        json_match = re.search(json_pattern, framework_content, re.DOTALL)
        if not json_match:
            raise ValueError("No JSON appendix found in framework")
        
        try:
            framework_config = json.loads(json_match.group(1))
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in framework appendix: {e}")
        
        # Extract all dimensions from dimension groups (framework-agnostic)
        all_dimensions = []
        dimension_groups = framework_config.get("dimension_groups", {})
        
        for group_name, dimensions in dimension_groups.items():
            if isinstance(dimensions, list):
                all_dimensions.extend(dimensions)
            else:
                # Log warning but continue - don't fail on malformed groups
                print(f"Warning: Dimension group '{group_name}' is not a list, skipping")
        
        if not all_dimensions:
            raise ValueError("No dimensions found in framework dimension_groups")
        
        return FrameworkConfig(
            dimensions=all_dimensions,
            dimension_groups=dimension_groups,
            raw_config=framework_config,
            framework_hash=framework_hash
        )