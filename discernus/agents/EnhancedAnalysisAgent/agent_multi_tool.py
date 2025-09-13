#!/usr/bin/env python3
"""
Enhanced Analysis Agent - Multi-Tool Implementation
==================================================

Implements the simplified multi-tool approach for complex framework analysis.
Uses three focused tools for structured output while leveraging Gemini's full context window.
"""

import json
import hashlib
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

from discernus.core.security_boundary import ExperimentSecurityBoundary
from discernus.core.audit_logger import AuditLogger
from discernus.core.local_artifact_storage import LocalArtifactStorage
from discernus.gateway.llm_gateway_enhanced import EnhancedLLMGateway
from discernus.gateway.model_registry import ModelRegistry


class EnhancedAnalysisAgentMultiTool:
    """
    Enhanced Analysis Agent using simplified multi-tool approach.
    
    Uses three focused tools:
    1. record_analysis_scores - Dimensional scores with confidence/salience
    2. record_evidence_quotes - Evidence quotes and reasoning
    3. record_computational_work - Derived metrics and code execution
    """
    
    def __init__(
        self,
        security_boundary: ExperimentSecurityBoundary,
        audit_logger: AuditLogger,
        storage: LocalArtifactStorage,
        llm_gateway: EnhancedLLMGateway,
        model: str = "vertex_ai/gemini-2.5-pro"
    ):
        self.security_boundary = security_boundary
        self.audit_logger = audit_logger
        self.storage = storage
        self.llm_gateway = llm_gateway
        self.model = model
        
        # Load prompt template
        self.prompt_template = self._load_prompt_template()
        
    def _load_prompt_template(self) -> str:
        """Load the multi-tool prompt template"""
        prompt_path = Path(__file__).parent / "prompt_multi_tool.txt"
        if prompt_path.exists():
            return prompt_path.read_text()
        else:
            # Fallback prompt
            return """
You are an expert discourse analyst. Analyze the document using the provided framework and return structured results using the three provided tools.

**ANALYSIS REQUIREMENTS:**
- Apply the framework's dimensional definitions precisely
- Score each dimension on a 0.0-1.0 scale for intensity, salience, and confidence
- Provide specific textual evidence for each scoring decision

**THREE-PHASE INTERNAL PROCESSING:**
Internally, generate three independent analytical approaches:
1. Evidence-First Analysis: Focus on direct textual evidence and explicit statements
2. Context-Weighted Analysis: Emphasize rhetorical context, structural positioning, and thematic centrality
3. Pattern-Based Analysis: Look for repetition patterns, rhetorical devices, and strategic emphasis

Calculate the MEDIAN score for each dimension across all three approaches.
Select the BEST evidence quote from the three approaches for each dimension.

**OUTPUT REQUIREMENTS:**
Call the three tools in sequence:
1. record_analysis_scores - with your final aggregated scores
2. record_evidence_quotes - with your best evidence selections  
3. record_computational_work - with your derived metrics calculations

**DOCUMENT:**
{document_content}

**FRAMEWORK:**
{framework_content}
"""
    
    def _get_tools_schema(self, framework_content: str = None) -> List[Dict[str, Any]]:
        """Get the three-tool schema for structured output, dynamically generated from framework"""
        
        # Extract dimensions from framework content if provided
        dimensions = self._extract_framework_dimensions(framework_content) if framework_content else self._get_default_dimensions()
        
        # Build dynamic scores properties
        scores_properties = {}
        for dimension in dimensions:
            scores_properties[dimension] = {
                "type": "object",
                "properties": {
                    "raw_score": {"type": "number"},
                    "salience": {"type": "number"},
                    "confidence": {"type": "number"}
                },
                "required": ["raw_score", "salience", "confidence"]
            }
        
        return [
            {
                "type": "function",
                "function": {
                    "name": "record_analysis_scores",
                    "description": "Record dimensional scores with confidence and salience",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "document_id": {"type": "string"},
                            "framework_name": {"type": "string"},
                            "framework_version": {"type": "string"},
                            "scores": {
                                "type": "object",
                                "description": "Dimensional scores as key-value pairs where keys are dimension names and values contain raw_score, salience, and confidence",
                                "properties": scores_properties,
                                "additionalProperties": {
                                    "type": "object",
                                    "properties": {
                                        "raw_score": {"type": "number"},
                                        "salience": {"type": "number"},
                                        "confidence": {"type": "number"}
                                    },
                                    "required": ["raw_score", "salience", "confidence"]
                                }
                            }
                        },
                        "required": ["document_id", "framework_name", "framework_version", "scores"]
                    }
                }
            },
            {
                "type": "function", 
                "function": {
                    "name": "record_evidence_quotes",
                    "description": "Record evidence quotes and reasoning for each dimension",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "document_id": {"type": "string"},
                            "evidence": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "dimension": {"type": "string"},
                                        "quote": {"type": "string"},
                                        "reasoning": {"type": "string"}
                                    },
                                    "required": ["dimension", "quote", "reasoning"]
                                }
                            }
                        },
                        "required": ["document_id", "evidence"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "record_computational_work", 
                    "description": "Record derived metrics calculations and code execution",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "document_id": {"type": "string"},
                            "executed_code": {"type": "string"},
                            "execution_output": {"type": "string"},
                            "derived_metrics": {
                                "type": "object",
                                "additionalProperties": {"type": "number"}
                            }
                        },
                        "required": ["document_id", "executed_code", "execution_output", "derived_metrics"]
                    }
                }
            }
        ]
    
    def _create_analysis_prompt(self, document_content: str, framework_content: str) -> str:
        """Create the analysis prompt with document and framework content"""
        return self.prompt_template.format(
            document_content=document_content,
            framework_content=framework_content
        )
    
    def _save_analysis_artifact(self, scores_data: Dict[str, Any]) -> str:
        """Save analysis scores artifact"""
        # Convert to JSON bytes
        json_data = json.dumps(scores_data, indent=2, sort_keys=True)
        artifact_hash = self.storage.put_artifact(
            content=json_data.encode('utf-8'),
            metadata={
                "artifact_type": "analysis_scores",
                "source_agent": "EnhancedAnalysisAgentMultiTool"
            }
        )
        return artifact_hash
    
    def _save_evidence_artifact(self, evidence_data: Dict[str, Any]) -> str:
        """Save evidence quotes artifact"""
        # Convert to JSON bytes
        json_data = json.dumps(evidence_data, indent=2, sort_keys=True)
        artifact_hash = self.storage.put_artifact(
            content=json_data.encode('utf-8'),
            metadata={
                "artifact_type": "evidence_quotes",
                "source_agent": "EnhancedAnalysisAgentMultiTool"
            }
        )
        return artifact_hash
    
    def _save_work_artifact(self, work_data: Dict[str, Any]) -> str:
        """Save computational work artifact"""
        # Convert to JSON bytes
        json_data = json.dumps(work_data, indent=2, sort_keys=True)
        artifact_hash = self.storage.put_artifact(
            content=json_data.encode('utf-8'),
            metadata={
                "artifact_type": "computational_work",
                "source_agent": "EnhancedAnalysisAgentMultiTool"
            }
        )
        return artifact_hash
    
    def _extract_framework_dimensions(self, framework_content: str) -> List[str]:
        """Extract dimension names from framework content"""
        dimensions = []
        
        # Look for dimension definitions in the framework text
        lines = framework_content.split('\n')
        in_dimensions_section = False
        
        for line in lines:
            line = line.strip()
            
            # Look for dimension section markers
            if any(marker in line.lower() for marker in ['dimensions:', 'dimensions', '**dimensions**']):
                in_dimensions_section = True
                continue
            
            # Look for dimension definitions (lines starting with - or *)
            if in_dimensions_section and (line.startswith('-') or line.startswith('*')):
                # Extract dimension name from line like "- Positive Sentiment (0.0-1.0): ..."
                dimension_text = line.lstrip('-*').strip()
                if '(' in dimension_text:
                    dimension_name = dimension_text.split('(')[0].strip()
                else:
                    dimension_name = dimension_text.split(':')[0].strip()
                
                # Convert to snake_case
                dimension_name = dimension_name.lower().replace(' ', '_').replace('-', '_')
                dimensions.append(dimension_name)
            
            # Stop at next major section
            elif in_dimensions_section and line.startswith('#'):
                break
        
        # If no dimensions found in text, try to extract from YAML
        if not dimensions:
            dimensions = self._extract_dimensions_from_yaml(framework_content)
        
        # Filter out derived metrics and other non-dimension items
        filtered_dimensions = []
        for dim in dimensions:
            # Skip items that are clearly not dimensions
            if any(skip_word in dim.lower() for skip_word in ['derived', 'metrics', 'calculation', 'balance', 'magnitude']):
                continue
            # Only include items that look like dimensions (short, descriptive)
            if len(dim) < 50 and not ':' in dim:
                filtered_dimensions.append(dim)
        
        return filtered_dimensions if filtered_dimensions else self._get_default_dimensions()
    
    def _extract_dimensions_from_yaml(self, framework_content: str) -> List[str]:
        """Extract dimensions from YAML metadata in framework"""
        dimensions = []
        
        # Look for YAML section
        yaml_start = framework_content.find("```yaml")
        yaml_end = framework_content.find("```", yaml_start + 7)
        
        if yaml_start != -1 and yaml_end != -1:
            yaml_content = framework_content[yaml_start+7:yaml_end]
            
            # Simple extraction of dimension names from YAML
            # This is a basic implementation - could be enhanced with proper YAML parsing
            for line in yaml_content.split('\n'):
                line = line.strip()
                if 'dimension' in line.lower() and ':' in line:
                    # Extract dimension name
                    dimension_name = line.split(':')[0].strip()
                    if dimension_name and not dimension_name.startswith('#'):
                        dimensions.append(dimension_name)
        
        return dimensions
    
    def _get_default_dimensions(self) -> List[str]:
        """Get default PDAF dimensions as fallback"""
        return [
            "manichaean_people_elite_framing",
            "crisis_restoration_temporal_narrative", 
            "popular_sovereignty_claims",
            "anti_pluralist_exclusion",
            "elite_conspiracy_systemic_corruption",
            "authenticity_vs_political_class",
            "homogeneous_people_construction",
            "nationalist_exclusion",
            "economic_populist_appeals"
        ]
    
    def analyze_document(
        self, 
        document_content: str, 
        framework_content: str,
        document_id: str = "test_document"
    ) -> Dict[str, Any]:
        """
        Analyze a document using the multi-tool approach.
        
        Args:
            document_content: The text content to analyze
            framework_content: The framework specification content
            document_id: Unique identifier for the document
            
        Returns:
            Dictionary containing analysis results and artifact IDs
        """
        try:
            # Create analysis prompt
            prompt = self._create_analysis_prompt(document_content, framework_content)
            print(f"   📝 Generated prompt length: {len(prompt)} characters")
            print(f"   📝 Framework content preview: {framework_content[:200]}...")
            
            # Get tools schema (dynamically generated from framework)
            tools = self._get_tools_schema(framework_content)
            
            # Log the analysis request
            self.audit_logger.log_agent_event(
                agent_name="EnhancedAnalysisAgentMultiTool",
                event_type="analysis_start",
                data={
                    "document_id": document_id,
                    "document_length": len(document_content),
                    "framework_length": len(framework_content),
                    "model": self.model
                }
            )
            
            # Execute LLM call with tools (force function calling to ensure all tools are used)
            print(f"   🔍 Sending analysis prompt to {self.model}...")
            response, metadata = self.llm_gateway.execute_call_with_tools(
                model=self.model,
                prompt=prompt,
                system_prompt="You are a helpful assistant. You MUST call all three functions in your response. Complete STEP 1, STEP 2, and STEP 3 by calling record_analysis_scores, record_evidence_quotes, and record_computational_work respectively. Do not stop after the first function call.",
                tools=tools,
                force_function_calling=True  # Force the model to make function calls (ANY mode)
            )
            
            # Log the response
            self.audit_logger.log_agent_event(
                agent_name="EnhancedAnalysisAgentMultiTool", 
                event_type="analysis_complete",
                data={
                    "document_id": document_id,
                    "success": metadata.get('success', False),
                    "tool_calls": len(metadata.get('tool_calls', [])),
                    "usage": metadata.get('usage', {})
                }
            )
            
            if not metadata.get('success') or not metadata.get('tool_calls'):
                raise Exception(f"LLM call failed: {metadata.get('error', 'Unknown error')}")
            
            # Process tool calls
            tool_calls = metadata.get('tool_calls') or []
            print(f"   🔧 Processing {len(tool_calls)} tool calls (expected 3)...")
            if len(tool_calls) < 1:
                print(f"   ❌ Expected at least 1 tool call, got {len(tool_calls)}")
                raise Exception(f"Expected at least 1 tool call, got {len(tool_calls)}")

            if len(tool_calls) < 3:
                print(f"   ⚠️  Warning: Expected 3 tool calls, got {len(tool_calls)}")
                print(f"   Continuing with partial results...")
            
            # Extract data from each tool call
            scores_data = None
            evidence_data = None
            work_data = None
            
            for tool_call in tool_calls:
                if hasattr(tool_call, 'function'):
                    function_name = tool_call.function.name
                    print(f"   🔧 Processing tool: {function_name}")
                    arguments = json.loads(tool_call.function.arguments)

                    if function_name == "record_analysis_scores":
                        scores_data = arguments
                        print(f"   ✅ Found analysis scores data")
                        print(f"   📊 Scores object: {arguments.get('scores', {})}")
                    elif function_name == "record_evidence_quotes":
                        evidence_data = arguments
                        print(f"   ✅ Found evidence quotes data")
                    elif function_name == "record_computational_work":
                        work_data = arguments
                        print(f"   ✅ Found computational work data")

            # Check what we have
            missing_tools = []
            if not scores_data:
                missing_tools.append("record_analysis_scores")
            if not evidence_data:
                missing_tools.append("record_evidence_quotes")
            if not work_data:
                missing_tools.append("record_computational_work")

            if missing_tools:
                print(f"   ⚠️  Missing tool calls: {missing_tools}")
                print(f"   Continuing with available data...")

            if not scores_data:
                raise Exception("Missing required analysis scores data")

            if not scores_data.get('scores'):
                print("   ⚠️  Warning: Scores object is empty, but continuing for debugging")
                # For now, allow empty scores to see what the LLM is sending
            
            # Save artifacts (only save what we have)
            scores_artifact_id = self._save_analysis_artifact(scores_data)
            evidence_artifact_id = self._save_evidence_artifact(evidence_data) if evidence_data else None
            work_artifact_id = self._save_work_artifact(work_data) if work_data else None
            
            # Return results
            return {
                "success": True,
                "document_id": document_id,
                "scores_artifact": scores_artifact_id,
                "evidence_artifact": evidence_artifact_id,
                "work_artifact": work_artifact_id,
                "tool_calls_count": len(tool_calls),
                "usage": metadata.get('usage', {})
            }
            
        except Exception as e:
            # Log error
            self.audit_logger.log_agent_event(
                agent_name="EnhancedAnalysisAgentMultiTool",
                event_type="analysis_error", 
                data={
                    "document_id": document_id,
                    "error": str(e)
                }
            )
            raise
