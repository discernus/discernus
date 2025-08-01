#!/usr/bin/env python3
"""
Intelligent Extractor Agent - Gasket #2
=======================================

Converts Raw Analysis Log to flat JSON structure using LLM intelligence.
Replaces brittle regex/json parsing with semantic LLM-based extraction.

This agent solves the core "Data Sparsity" problem by creating a robust
interface between non-deterministic Analysis Agent output and deterministic
MathToolkit processing.

Key Features:
- Framework-agnostic design using gasket_schema
- Semantic mapping from hierarchical to flat structures  
- Robust error handling and retry logic
- Fast extraction using Gemini 2.5 Flash
- THIN architecture with single responsibility
"""

import json
import logging
import time
import yaml
import os
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from datetime import datetime

from discernus.gateway.llm_gateway import LLMGateway
from discernus.gateway.model_registry import ModelRegistry
from discernus.core.audit_logger import AuditLogger


@dataclass
class ExtractionResult:
    """Result of intelligent extraction with metadata."""
    success: bool
    extracted_scores: Dict[str, Optional[float]]
    extraction_time_seconds: float
    tokens_used: int
    cost_usd: float
    attempts: int
    error_message: Optional[str] = None
    raw_llm_response: Optional[str] = None


class IntelligentExtractorError(Exception):
    """Intelligent Extractor specific exceptions."""
    pass


class IntelligentExtractorAgent:
    """
    Intelligent Extractor Agent - Gasket #2 for LLM-to-Math boundary.
    
    Converts Raw Analysis Logs to flat JSON structures using LLM intelligence,
    replacing brittle parsing with semantic extraction.
    """
    
    def __init__(self, 
                 model: str = "vertex_ai/gemini-2.5-flash",
                 audit_logger: Optional[AuditLogger] = None,
                 max_retries: int = 3,
                 timeout_seconds: int = 30):
        """
        Initialize Intelligent Extractor Agent.
        
        Args:
            model: LLM model for extraction (fast model recommended)
            audit_logger: Optional audit logger for provenance
            max_retries: Maximum retry attempts for failed extractions
            timeout_seconds: Timeout for individual extraction calls
        """
        self.model = model
        self.agent_name = "IntelligentExtractorAgent"
        self.audit_logger = audit_logger
        self.max_retries = max_retries
        self.timeout_seconds = timeout_seconds
        
        # Initialize LLM gateway
        model_registry = ModelRegistry()
        self.llm_gateway = LLMGateway(model_registry)
        
        # Set up logging
        self.logger = logging.getLogger(__name__)
        
        # Load externalized prompt template
        self.prompt_template = self._load_prompt_template()
        
        # Log initialization
        if self.audit_logger:
            self.audit_logger.log_agent_event(
                self.agent_name,
                "initialization",
                {
                    "model": model,
                    "architecture": "intelligent_extractor_gasket",
                    "capabilities": ["semantic_extraction", "hierarchical_to_flat_mapping", "robust_parsing"],
                    "max_retries": max_retries,
                    "timeout_seconds": timeout_seconds,
                    "prompt_externalized": True
                }
            )
    
    def extract_scores_from_raw_analysis(
        self, 
        raw_analysis_text: str, 
        gasket_schema: Dict[str, List[str]]
    ) -> ExtractionResult:
        """
        Extract and map scores from Raw Analysis Log using LLM intelligence.
        
        This is the core method that replaces brittle JSON parsing with
        semantic LLM-based extraction.
        
        Args:
            raw_analysis_text: The Raw Analysis Log from Analysis Agent
            gasket_schema: Framework gasket_schema with target_keys and target_dimensions
            
        Returns:
            ExtractionResult with extracted scores and metadata
        """
        start_time = time.time()
        
        # Validate inputs
        if not raw_analysis_text or not raw_analysis_text.strip():
            return ExtractionResult(
                success=False,
                extracted_scores={},
                extraction_time_seconds=0.0,
                tokens_used=0,
                cost_usd=0.0,
                attempts=0,
                error_message="Empty or invalid raw analysis text"
            )
        
        if not gasket_schema or 'target_keys' not in gasket_schema or 'target_dimensions' not in gasket_schema:
            return ExtractionResult(
                success=False,
                extracted_scores={},
                extraction_time_seconds=0.0,
                tokens_used=0,
                cost_usd=0.0,
                attempts=0,
                error_message="Invalid gasket_schema: missing target_keys or target_dimensions"
            )
        
        # Log extraction start
        if self.audit_logger:
            self.audit_logger.log_agent_event(
                self.agent_name,
                "extraction_start",
                {
                    "raw_analysis_length": len(raw_analysis_text),
                    "target_keys_count": len(gasket_schema['target_keys']),
                    "target_dimensions_count": len(gasket_schema['target_dimensions'])
                }
            )
        
        # Attempt extraction with retries
        for attempt in range(1, self.max_retries + 1):
            try:
                # Create extraction prompt
                extraction_prompt = self._create_extraction_prompt(
                    raw_analysis_text, gasket_schema
                )
                
                # Execute LLM call
                response, metadata = self.llm_gateway.execute_call(
                    model=self.model,
                    prompt=extraction_prompt,
                    system_prompt="You are a highly efficient and accurate data extraction and semantic mapping bot.",
                    timeout=self.timeout_seconds
                )
                
                # Parse extracted scores
                extracted_scores = self._parse_extraction_response(
                    response, gasket_schema['target_keys']
                )
                
                # Calculate metrics
                extraction_time = time.time() - start_time
                tokens_used = metadata.get('total_tokens', 0)
                cost_usd = metadata.get('cost', 0.0)
                
                # Log successful extraction
                if self.audit_logger:
                    self.audit_logger.log_agent_event(
                        self.agent_name,
                        "extraction_success",
                        {
                            "attempt": attempt,
                            "extraction_time_seconds": extraction_time,
                            "tokens_used": tokens_used,
                            "cost_usd": cost_usd,
                            "extracted_keys_count": len([k for k, v in extracted_scores.items() if v is not None])
                        }
                    )
                
                return ExtractionResult(
                    success=True,
                    extracted_scores=extracted_scores,
                    extraction_time_seconds=extraction_time,
                    tokens_used=tokens_used,
                    cost_usd=cost_usd,
                    attempts=attempt,
                    raw_llm_response=response
                )
                
            except Exception as e:
                self.logger.warning(f"Extraction attempt {attempt} failed: {str(e)}")
                
                if attempt == self.max_retries:
                    # Final attempt failed
                    extraction_time = time.time() - start_time
                    
                    if self.audit_logger:
                        self.audit_logger.log_agent_event(
                            self.agent_name,
                            "extraction_failure",
                            {
                                "attempts": attempt,
                                "error": str(e),
                                "error_type": type(e).__name__,
                                "extraction_time_seconds": extraction_time
                            }
                        )
                    
                    return ExtractionResult(
                        success=False,
                        extracted_scores={},
                        extraction_time_seconds=extraction_time,
                        tokens_used=0,
                        cost_usd=0.0,
                        attempts=attempt,
                        error_message=str(e)
                    )
                
                # Wait before retry
                time.sleep(min(2 ** attempt, 10))  # Exponential backoff, max 10s
    
    def _load_prompt_template(self) -> str:
        """
        Load external YAML prompt template following THIN architecture.
        
        Returns:
            Loaded prompt template string
        """
        # Find prompt.yaml in agent directory
        agent_dir = os.path.dirname(__file__)
        prompt_path = os.path.join(agent_dir, 'prompt.yaml')
        
        if not os.path.exists(prompt_path):
            raise FileNotFoundError(f"Prompt file not found: {prompt_path}")
        
        # Load prompt template
        with open(prompt_path, 'r') as f:
            prompt_content = f.read()
            prompt_data = yaml.safe_load(prompt_content)
        
        if 'template' not in prompt_data:
            raise ValueError(f"Prompt file missing 'template' key: {prompt_path}")
        
        return prompt_data['template']
    
    def _create_extraction_prompt(
        self, 
        raw_analysis_text: str, 
        gasket_schema: Dict[str, List[str]]
    ) -> str:
        """
        Create framework-agnostic extraction prompt using externalized template.
        
        Args:
            raw_analysis_text: Raw Analysis Log to extract from
            gasket_schema: Framework gasket schema
            
        Returns:
            Formatted extraction prompt
        """
        target_dimensions = gasket_schema['target_dimensions']
        target_keys = gasket_schema['target_keys']
        
        # Format dimensions and keys for prompt
        dimensions_text = "\n".join(f"- {dim}" for dim in target_dimensions)
        keys_text = "\n".join(f"- {key}" for key in target_keys)
        
        # Create example mapping
        example_mapping = {}
        for i, key in enumerate(target_keys[:2]):  # Show first 2 as example
            example_mapping[key] = round(0.75 + (i * 0.1), 2)
        example_json = json.dumps(example_mapping)
        
        # Use externalized template
        return self.prompt_template.format(
            dimensions_text=dimensions_text,
            keys_text=keys_text,
            example_json=example_json,
            raw_analysis_text=raw_analysis_text
        )
    
    def _parse_extraction_response(
        self, 
        response: str, 
        target_keys: List[str]
    ) -> Dict[str, Optional[float]]:
        """
        Parse LLM extraction response into structured scores.
        
        Args:
            response: Raw LLM response
            target_keys: Expected keys from gasket schema
            
        Returns:
            Dictionary mapping target keys to extracted scores
        """
        # Initialize result with all keys as None
        extracted_scores = {key: None for key in target_keys}
        
        try:
            # Clean response - remove any markdown formatting
            cleaned_response = response.strip()
            if cleaned_response.startswith('```json'):
                cleaned_response = cleaned_response[7:]
            if cleaned_response.endswith('```'):
                cleaned_response = cleaned_response[:-3]
            cleaned_response = cleaned_response.strip()
            
            # Parse JSON
            parsed_data = json.loads(cleaned_response)
            
            # Extract scores for target keys
            for key in target_keys:
                if key in parsed_data:
                    value = parsed_data[key]
                    if value is not None:
                        # Validate score range
                        if isinstance(value, (int, float)) and 0.0 <= value <= 1.0:
                            extracted_scores[key] = float(value)
                        else:
                            self.logger.warning(f"Invalid score for {key}: {value} (must be 0.0-1.0)")
            
            return extracted_scores
            
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse extraction response as JSON: {e}")
            self.logger.error(f"Response was: {response[:200]}...")
            raise IntelligentExtractorError(f"Invalid JSON response from LLM: {e}")
        
        except Exception as e:
            self.logger.error(f"Unexpected error parsing extraction response: {e}")
            raise IntelligentExtractorError(f"Failed to parse extraction response: {e}")
    
    def get_extraction_stats(self) -> Dict[str, Any]:
        """
        Get extraction statistics for monitoring and optimization.
        
        Returns:
            Dictionary with extraction performance metrics
        """
        return {
            "agent_name": self.agent_name,
            "model": self.model,
            "max_retries": self.max_retries,
            "timeout_seconds": self.timeout_seconds,
            "capabilities": ["semantic_extraction", "hierarchical_to_flat_mapping", "robust_parsing"]
        }