"""
Robust Response Parser for LLM Outputs
=====================================

Multi-strategy parsing system that handles various LLM response formats:
- Clean JSON
- JSON with markdown code blocks 
- JSON followed by commentary (Claude's "Extra data" issue)
- Structured text fallback

This addresses the brittle parsing issues where Claude adds commentary after JSON,
causing "Extra data: line 45 column 1" errors.
"""

import json
import re
import logging
from typing import Dict, Any, List, Callable, Optional

# Configure logging for parser debugging
parser_logger = logging.getLogger("robust_parser")


class RobustResponseParser:
    """
    Model-agnostic response parser with fallback strategies.
    
    Designed to handle the diversity of LLM response formats without
    brittle model-specific workarounds.
    """
    
    def __init__(self, debug_mode: bool = False):
        self.debug_mode = debug_mode
        self.parsing_attempts_log = []
        
    def parse_llm_response(self, content: str, model_name: str) -> Dict[str, Any]:
        """
        Parse LLM response using multiple fallback strategies.
        
        Args:
            content: Raw response content from LLM
            model_name: Name of the model (for logging/debugging)
            
        Returns:
            Parsed response with scores and metadata
            
        Raises:
            ValueError: If all parsing strategies fail
        """
        self.parsing_attempts_log = []
        
        parsing_strategies = [
            self._parse_clean_json,
            self._parse_json_with_markdown_blocks,
            self._parse_json_with_extra_content,
            self._parse_structured_text_fallback
        ]
        
        for i, strategy in enumerate(parsing_strategies):
            try:
                result = strategy(content, model_name)
                if self._validate_parsed_response(result):
                    if self.debug_mode:
                        parser_logger.info(f"✅ Strategy {i+1} ({strategy.__name__}) succeeded for {model_name}")
                    return result
                else:
                    self.parsing_attempts_log.append(f"Strategy {i+1} returned invalid result")
            except Exception as e:
                self.parsing_attempts_log.append(f"Strategy {i+1} ({strategy.__name__}) failed: {str(e)}")
                if self.debug_mode:
                    parser_logger.debug(f"Strategy {i+1} failed for {model_name}: {e}")
                continue
        
        # If we get here, all strategies failed
        error_summary = "; ".join(self.parsing_attempts_log)
        parser_logger.error(f"❌ All parsing strategies failed for {model_name}: {error_summary}")
        raise ValueError(f"All parsing strategies failed for {model_name}: {error_summary}")
    
    def _parse_clean_json(self, content: str, model_name: str) -> Dict[str, Any]:
        """Strategy 1: Parse as clean JSON"""
        return json.loads(content.strip())
    
    def _parse_json_with_markdown_blocks(self, content: str, model_name: str) -> Dict[str, Any]:
        """Strategy 2: Extract JSON from markdown code blocks"""
        # Remove markdown code block wrappers
        cleaned_content = content.strip()
        
        # Handle ```json blocks
        if cleaned_content.startswith('```json'):
            cleaned_content = cleaned_content[7:]  # Remove ```json
        elif cleaned_content.startswith('```'):
            cleaned_content = cleaned_content[3:]   # Remove ```
            
        if cleaned_content.endswith('```'):
            cleaned_content = cleaned_content[:-3]   # Remove trailing ```
            
        return json.loads(cleaned_content.strip())
    
    def _parse_json_with_extra_content(self, content: str, model_name: str) -> Dict[str, Any]:
        """
        Strategy 3: Handle JSON followed by commentary (Claude's issue)
        
        This is the core fix for "Extra data: line 45 column 1" errors.
        Claude often returns valid JSON followed by explanatory text.
        """
        # Find the start of JSON
        json_start = content.find('{')
        if json_start == -1:
            raise ValueError("No JSON start found")
        
        # Find the complete JSON object by tracking braces
        brace_count = 0
        json_end = json_start
        
        for i, char in enumerate(content[json_start:], json_start):
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0:
                    json_end = i + 1
                    break
        
        if brace_count != 0:
            raise ValueError("Incomplete JSON object - unmatched braces")
        
        # Extract just the JSON portion
        clean_json = content[json_start:json_end]
        
        if self.debug_mode:
            extra_content = content[json_end:].strip()
            if extra_content:
                parser_logger.debug(f"Found extra content after JSON for {model_name}: {extra_content[:100]}...")
        
        return json.loads(clean_json)
    
    def _parse_structured_text_fallback(self, content: str, model_name: str) -> Dict[str, Any]:
        """Strategy 4: Extract structured data from text when JSON fails"""
        scores = {}
        
        # Look for score patterns like "Care": 0.8 or Care: 0.8
        score_patterns = [
            r'"(\w+)":\s*([0-9]*\.?[0-9]+)',  # "Care": 0.8
            r'(\w+):\s*([0-9]*\.?[0-9]+)',    # Care: 0.8
            r'(\w+)\s*=\s*([0-9]*\.?[0-9]+)', # Care = 0.8
            r'(\w+)\s*-\s*([0-9]*\.?[0-9]+)', # Care - 0.8
        ]
        
        for pattern in score_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for concept, score_str in matches:
                try:
                    score = float(score_str)
                    # Normalize scores to 0-1 range if needed
                    if score > 1.0 and score <= 10.0:
                        score = score / 10.0
                    elif score > 10.0:
                        score = score / 100.0
                    
                    scores[concept.title()] = round(score, 3)
                except ValueError:
                    continue
        
        if not scores:
            raise ValueError("No structured data found in text")
        
        return {"scores": scores, "parsing_method": "text_fallback"}
    
    def _validate_parsed_response(self, result: Dict[str, Any]) -> bool:
        """
        Validate that the parsed response contains expected structure.
        
        Args:
            result: Parsed response dictionary
            
        Returns:
            True if response appears valid, False otherwise
        """
        # Must be a dictionary
        if not isinstance(result, dict):
            return False
        
        # Must have scores (directly or nested)
        scores = result.get("scores", {})
        if isinstance(result, dict) and not scores:
            # Check if the result itself contains score-like data
            score_like_keys = [k for k, v in result.items() 
                             if isinstance(v, (int, float, dict)) and k not in ["parsing_method"]]
            if score_like_keys:
                scores = {k: v for k, v in result.items() if k in score_like_keys}
                result["scores"] = scores
            else:
                return False
        
        # Scores should be a dictionary
        if not isinstance(scores, dict):
            return False
        
        # Should have at least one score
        if len(scores) == 0:
            return False
        
        # All scores should be numeric and in reasonable range
        for score_name, score_value in scores.items():
            if isinstance(score_value, dict):
                # Handle nested format like {"score": 0.8, "evidence": "..."}
                if "score" in score_value:
                    score_value = score_value["score"]
                else:
                    return False
            
            if not isinstance(score_value, (int, float)):
                return False
            
            if score_value < 0 or score_value > 1.0:
                return False
        
        return True
    
    def get_parsing_log(self) -> List[str]:
        """Get log of parsing attempts for debugging"""
        return self.parsing_attempts_log.copy()


class ParsingDebugger:
    """Utility class for debugging parsing issues"""
    
    @staticmethod
    def analyze_claude_response(response: str) -> Dict[str, Any]:
        """Analyze a Claude response to understand its structure"""
        analysis = {
            "total_length": len(response),
            "starts_with_json": response.strip().startswith('{'),
            "ends_with_json": response.strip().endswith('}'),
            "brace_analysis": ParsingDebugger._analyze_braces(response),
            "has_markdown_blocks": "```" in response,
            "potential_json_start": response.find('{'),
            "potential_json_end": response.rfind('}'),
        }
        
        # Try to identify where extra content starts
        if analysis["potential_json_end"] != -1:
            json_end = analysis["potential_json_end"] + 1
            extra_content = response[json_end:].strip()
            analysis["extra_content_length"] = len(extra_content)
            analysis["extra_content_preview"] = extra_content[:200] if extra_content else None
        
        return analysis
    
    @staticmethod
    def _analyze_braces(text: str) -> Dict[str, Any]:
        """Analyze brace structure in text"""
        open_braces = text.count('{')
        close_braces = text.count('}')
        
        return {
            "open_braces": open_braces,
            "close_braces": close_braces,
            "balanced": open_braces == close_braces,
            "brace_difference": open_braces - close_braces
        }


# Main parser instance for use throughout the application
default_parser = RobustResponseParser(debug_mode=False)


def parse_llm_response(content: str, model_name: str = "unknown") -> Dict[str, Any]:
    """
    Convenience function for parsing LLM responses.
    
    Args:
        content: Raw response content from LLM
        model_name: Name of the model (for logging)
        
    Returns:
        Parsed response dictionary
    """
    return default_parser.parse_llm_response(content, model_name)


def debug_claude_response(response: str) -> Dict[str, Any]:
    """
    Convenience function for debugging Claude responses.
    
    Args:
        response: Raw Claude response
        
    Returns:
        Analysis of the response structure
    """
    return ParsingDebugger.analyze_claude_response(response) 