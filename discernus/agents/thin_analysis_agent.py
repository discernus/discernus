#!/usr/bin/env python3
"""
THIN Analysis Agent - Natural Language Analysis without Parsing
===============================================================

THIN Principle: LLM provides intelligence in natural language that humans can read directly.
No parsing required - software just saves and loads text files.

This demonstrates the THIN approach where:
1. LLM returns natural language analysis (human-readable)
2. Software just saves the text (no parsing)
3. Statistical analysis is done by another LLM reading the natural language
4. No JSON structure dependencies or parsing failures
"""

import sys
from pathlib import Path
from typing import Dict, Any

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    from discernus.gateway.llm_gateway import LLMGateway
    from discernus.gateway.model_registry import ModelRegistry
    DEPENDENCIES_AVAILABLE = True
except ImportError as e:
    print(f"ThinAnalysisAgent dependencies not available: {e}")
    DEPENDENCIES_AVAILABLE = False

class ThinAnalysisAgent:
    """
    THIN Analysis Agent - returns natural language analysis without structured parsing
    """
    
    def __init__(self):
        if not DEPENDENCIES_AVAILABLE:
            raise ImportError("Could not import required dependencies")
        self.model_registry = ModelRegistry()
        self.gateway = LLMGateway(self.model_registry)
    
    def analyze_text(self, framework_content: str, text_content: str, file_name: str) -> str:
        """
        Perform framework analysis returning natural language (THIN approach)
        
        Args:
            framework_content: The analytical framework
            text_content: The text to analyze
            file_name: Name of the file being analyzed
            
        Returns:
            Natural language analysis (no parsing required)
        """
        
        prompt = f"""You are a framework analysis specialist. Your task is to analyze the given text using the provided framework and return a natural language analysis that humans can read directly.

FRAMEWORK:
{framework_content}

TEXT TO ANALYZE:
File: {file_name}
{text_content}

INSTRUCTIONS:
Provide a thorough analysis in natural language that includes:
1. Overall assessment with approximate numerical score (if relevant)
2. Specific textual evidence supporting your analysis
3. Clear reasoning connecting the evidence to the framework
4. Any notable patterns or insights

Write your analysis in clear, readable prose that a human researcher could use directly in their work. Do NOT return JSON or structured data - return natural language that tells the story of your analysis.

Begin your analysis:"""

        model_name = self.model_registry.get_model_for_task('analysis')
        if not model_name:
            model_name = "anthropic/claude-3-5-sonnet-20240620"
        
        try:
            response, _ = self.gateway.execute_call(model=model_name, prompt=prompt)
            return response if response else "Analysis failed: Empty response from model"
        except Exception as e:
            return f"Analysis failed: {str(e)}"

# Example of THIN approach - no parsing needed, just natural language
class ThinStatisticalAnalysisAgent:
    """
    THIN Statistical Analysis - LLM reads natural language analyses and generates statistical interpretation
    """
    
    def __init__(self):
        if not DEPENDENCIES_AVAILABLE:
            raise ImportError("Could not import required dependencies")
        self.model_registry = ModelRegistry()
        self.gateway = LLMGateway(self.model_registry)
    
    def analyze_results(self, analysis_results: list) -> str:
        """
        Perform statistical analysis by reading natural language analyses (THIN approach)
        
        Args:
            analysis_results: List of natural language analyses
            
        Returns:
            Statistical interpretation in natural language
        """
        
        # Combine all analyses into one text block
        combined_analyses = "\n\n---\n\n".join([
            f"Analysis {i+1}:\n{result.get('analysis_response', '')}" 
            for i, result in enumerate(analysis_results)
        ])
        
        prompt = f"""You are a statistical analysis expert. You have been given multiple natural language analyses from different models and runs. Your task is to provide a statistical interpretation of these analyses.

ANALYSES TO EXAMINE:
{combined_analyses}

INSTRUCTIONS:
Read through all the analyses and provide a statistical interpretation that includes:
1. Overall patterns and consistency across analyses
2. Range of assessments and any notable variations
3. Reliability assessment (how consistent are the analyses?)
4. Key themes that emerge across multiple analyses
5. Any statistical insights about the distribution of findings

Write your statistical interpretation in clear, natural language that researchers can use directly. Focus on what the pattern of analyses tells us about the reliability and validity of the findings.

Begin your statistical interpretation:"""

        model_name = self.model_registry.get_model_for_task('synthesis')
        if not model_name:
            model_name = "anthropic/claude-3-5-sonnet-20240620"
        
        try:
            response, _ = self.gateway.execute_call(model=model_name, prompt=prompt)
            return response if response else "Statistical analysis failed: Empty response from model"
        except Exception as e:
            return f"Statistical analysis failed: {str(e)}"

# THIN Benefits:
# 1. No parsing failures - natural language doesn't break
# 2. Human readable results - can be used directly in research
# 3. Flexible analysis - LLMs can express nuanced insights
# 4. Robust - no JSON structure dependencies
# 5. True THIN - software is just infrastructure, LLMs provide intelligence 