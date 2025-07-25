#!/usr/bin/env python3
"""
LLM Response Parser - Centralized response parsing for THIN compliance
=====================================================================

THIN Principle: Centralize parsing infrastructure to avoid duplication across agents.
However, extensive parsing is often a sign of THICK design - consider whether
parsing is necessary at all.

This module provides utilities for the common case where LLM responses need
to be extracted from markdown code blocks or cleaned up for JSON parsing.
"""

import json
import re
from typing import Dict, Any, Optional, Union

class LLMResponseParser:
    """Centralized parser for LLM responses with common patterns"""
    
    @staticmethod
    def extract_json_from_response(response: str) -> Optional[Dict[str, Any]]:
        """
        Extract JSON from LLM response, handling markdown code blocks.
        
        Args:
            response: Raw LLM response text
            
        Returns:
            Parsed JSON dict or None if parsing fails
        """
        if not response or not response.strip():
            return None
            
        # Extract JSON from markdown code blocks if present
        json_content = LLMResponseParser._extract_from_markdown_blocks(response)
        if not json_content:
            json_content = response.strip()
            
        try:
            return json.loads(json_content)
        except (json.JSONDecodeError, TypeError):
            return None
    
    @staticmethod
    def _extract_from_markdown_blocks(response: str) -> Optional[str]:
        """Extract content from markdown code blocks"""
        # Try JSON blocks first
        json_match = re.search(r'```json\s*\n(.*?)\n```', response, re.DOTALL)
        if json_match:
            return json_match.group(1).strip()
            
        # Try YAML blocks
        yaml_match = re.search(r'```yaml\s*\n(.*?)\n```', response, re.DOTALL)
        if yaml_match:
            return yaml_match.group(1).strip()
            
        # Try generic code blocks
        code_match = re.search(r'```\s*\n(.*?)\n```', response, re.DOTALL)
        if code_match:
            return code_match.group(1).strip()
            
        return None
    
    @staticmethod
    def extract_score_from_analysis(analysis_response: str) -> Optional[float]:
        """
        Extract numerical score from analysis response.
        
        THIN NOTE: This method exists for compatibility with existing statistical
        analysis. Consider whether score extraction is necessary - natural language
        analysis may be more valuable than numerical scores.
        """
        json_data = LLMResponseParser.extract_json_from_response(analysis_response)
        if not json_data:
            return None
            
        # Try various score field names
        score_fields = ['score', 'primary_score', 'overall_score']
        for field in score_fields:
            if field in json_data and isinstance(json_data[field], (int, float)):
                return float(json_data[field])
                
        # Handle nested score structures
        if 'scores' in json_data and isinstance(json_data['scores'], list):
            for score_item in json_data['scores']:
                if isinstance(score_item, dict) and 'score' in score_item:
                    return float(score_item['score'])
                    
        return None

# THIN Warning: Extensive use of this parser may indicate THICK design
# Consider whether structured parsing is necessary or if natural language
# responses would be more appropriate for human consumption 