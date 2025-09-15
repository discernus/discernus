#!/usr/bin/env python3
"""
Enhanced Analysis Agent - Sequential Tool Calling
================================================

Uses three separate LLM calls instead of trying to get all 3 tools in one call.
This approach is more reliable and bulletproof.
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


class EnhancedAnalysisAgentSequentialTools:
    """
    Enhanced Analysis Agent using sequential tool calling approach.
    
    Makes 3 separate LLM calls:
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
        
        # Load prompt templates
        self.scores_prompt = self._load_scores_prompt()
        self.evidence_prompt = self._load_evidence_prompt()
        self.work_prompt = self._load_work_prompt()
        
    def _load_scores_prompt(self) -> str:
        """Load the scores prompt template"""
        return """You are an expert discourse analyst. Analyze the document and score each dimension.

**TASK**: Score each dimension on a 0.0-1.0 scale for intensity, salience, and confidence.

**DIMENSIONS**:
{dimensions}

**DOCUMENT**:
{document_content}

**FRAMEWORK**:
{framework_content}

**INSTRUCTIONS**:
1. Analyze the document using the framework dimensions
2. Score each dimension (raw_score, salience, confidence)
3. Call the record_analysis_scores function with your results

You MUST call the record_analysis_scores function with your dimensional scoring judgments."""

    def _load_evidence_prompt(self) -> str:
        """Load the evidence prompt template"""
        return """You are an expert discourse analyst. Extract evidence quotes for each dimension.

**TASK**: Provide specific textual evidence for each dimension scoring decision.

**DIMENSIONS**:
{dimensions}

**DOCUMENT**:
{document_content}

**FRAMEWORK**:
{framework_content}

**INSTRUCTIONS**:
1. Find specific quotes from the document that support each dimension
2. Provide reasoning for why each quote supports the dimension
3. Call the record_evidence_quotes function with your evidence

You MUST call the record_evidence_quotes function with your evidence quotes and reasoning."""

    def _load_work_prompt(self) -> str:
        """Load the work prompt template"""
        return """You are an expert discourse analyst. Calculate derived metrics using Python code.

**TASK**: Calculate derived metrics using Python code execution.

**DIMENSIONS**:
{dimensions}

**DOCUMENT**:
{document_content}

**FRAMEWORK**:
{framework_content}

**INSTRUCTIONS**:
1. Write Python code to calculate derived metrics
2. Common metrics: overall intensity, rhetorical complexity, confidence-weighted scores
3. Execute the code and get the output
4. Call the record_computational_work function with your code and results

You MUST call the record_computational_work function with your Python code, execution output, and derived metrics."""

    def _extract_dimensions_from_yaml(self, framework_content: str) -> List[str]:
        """Extract dimension names from framework YAML content"""
        dimensions = []
        
        # Simple extraction - look for lines with dimension names
        for line in framework_content.split('\n'):
            line = line.strip()
            if line.startswith('- ') and ':' in line:
                # Extract dimension name
                dimension_name = line.split(':')[0].strip().replace('- ', '')
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
        document: Dict[str, Any], 
        framework_content: str,
        document_id: str = None
    ) -> Dict[str, Any]:
        """
        Analyze a document using the sequential tool calling approach.
        
        Args:
            document_content: The text content to analyze
            framework_content: The framework specification content
            document_id: Unique identifier for the document
            
        Returns:
            Dictionary containing analysis results and artifact IDs
        """
        try:
            # Extract dimensions from framework
            dimensions = self._extract_dimensions_from_yaml(framework_content)
            if not dimensions:
                dimensions = self._get_default_dimensions()
            
            dimensions_text = "\n".join([f"- {dim}: {dim}" for dim in dimensions])
            
            print(f"   📝 Document: {len(document_content)} characters")
            print(f"   📝 Framework: {len(framework_content)} characters")
            print(f"   📝 Dimensions: {len(dimensions)}")
            
            # Call 1: Analysis Scores
            print(f"   🔧 Call 1: Analysis Scores...")
            scores_result = self._call_scores_tool(document_content, framework_content, dimensions_text, document_id)
            
            # Call 2: Evidence Quotes
            print(f"   🔧 Call 2: Evidence Quotes...")
            evidence_result = self._call_evidence_tool(document_content, framework_content, dimensions_text, document_id)
            
            # Call 3: Computational Work
            print(f"   🔧 Call 3: Computational Work...")
            work_result = self._call_work_tool(document_content, framework_content, dimensions_text, document_id)
            
            # Return results
            return {
                "success": True,
                "document_id": document_id,
                "scores_artifact": scores_result,
                "evidence_artifact": evidence_result,
                "work_artifact": work_result,
                "tool_calls_count": 3,
                "usage": {}  # Could aggregate usage from all calls
            }
            
        except Exception as e:
            # Log error
            self.audit_logger.log_agent_event(
                agent_name="EnhancedAnalysisAgentSequentialTools",
                event_type="analysis_error", 
                data={
                    "document_id": document_id,
                    "error": str(e)
                }
            )
            raise
    
    def _call_scores_tool(self, document_content: str, framework_content: str, dimensions_text: str, document_id: str) -> str:
        """Call the scores tool"""
        prompt = self.scores_prompt.format(
            dimensions=dimensions_text,
            document_content=document_content,
            framework_content=framework_content
        )
        
        tools = [{
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
        }]
        
        response, metadata = self.llm_gateway.execute_call_with_tools(
            model=self.model,
            prompt=prompt,
            system_prompt="You are a helpful assistant. You MUST call the record_analysis_scores function.",
            tools=tools,
            force_function_calling=True
        )
        
        if not metadata.get('success') or not metadata.get('tool_calls'):
            raise Exception(f"Scores tool call failed: {metadata.get('error', 'Unknown error')}")
        
        # Process tool call
        tool_call = metadata.get('tool_calls')[0]
        function_args = json.loads(tool_call.function.arguments)
        
        # Save artifact
        return self._save_analysis_artifact(function_args)
    
    def _call_evidence_tool(self, document_content: str, framework_content: str, dimensions_text: str, document_id: str) -> str:
        """Call the evidence tool"""
        prompt = self.evidence_prompt.format(
            dimensions=dimensions_text,
            document_content=document_content,
            framework_content=framework_content
        )
        
        tools = [{
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
        }]
        
        response, metadata = self.llm_gateway.execute_call_with_tools(
            model=self.model,
            prompt=prompt,
            system_prompt="You are a helpful assistant. You MUST call the record_evidence_quotes function.",
            tools=tools,
            force_function_calling=True
        )
        
        if not metadata.get('success') or not metadata.get('tool_calls'):
            raise Exception(f"Evidence tool call failed: {metadata.get('error', 'Unknown error')}")
        
        # Process tool call
        tool_call = metadata.get('tool_calls')[0]
        function_args = json.loads(tool_call.function.arguments)
        
        # Save artifact
        return self._save_evidence_artifact(function_args)
    
    def _call_work_tool(self, document_content: str, framework_content: str, dimensions_text: str, document_id: str) -> str:
        """Call the work tool"""
        prompt = self.work_prompt.format(
            dimensions=dimensions_text,
            document_content=document_content,
            framework_content=framework_content
        )
        
        tools = [{
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
        }]
        
        response, metadata = self.llm_gateway.execute_call_with_tools(
            model=self.model,
            prompt=prompt,
            system_prompt="You are a helpful assistant. You MUST call the record_computational_work function.",
            tools=tools,
            force_function_calling=True
        )
        
        if not metadata.get('success') or not metadata.get('tool_calls'):
            print(f"   ❌ Work tool call failed: {metadata.get('error', 'Unknown error')}")
            print(f"   📊 Metadata: {metadata}")
            raise Exception(f"Work tool call failed: {metadata.get('error', 'Unknown error')}")
        
        # Process tool call
        tool_call = metadata.get('tool_calls')[0]
        function_args = json.loads(tool_call.function.arguments)
        
        # Save artifact
        return self._save_work_artifact(function_args)
    
    def _save_analysis_artifact(self, data: Dict[str, Any]) -> str:
        """Save analysis scores artifact"""
        content = json.dumps(data, indent=2).encode('utf-8')
        return self.storage.put_artifact(content, {"artifact_type": "analysis_scores"})
    
    def _save_evidence_artifact(self, data: Dict[str, Any]) -> str:
        """Save evidence quotes artifact"""
        content = json.dumps(data, indent=2).encode('utf-8')
        return self.storage.put_artifact(content, {"artifact_type": "evidence_quotes"})
    
    def _save_work_artifact(self, data: Dict[str, Any]) -> str:
        """Save computational work artifact"""
        content = json.dumps(data, indent=2).encode('utf-8')
        return self.storage.put_artifact(content, {"artifact_type": "computational_work"})
    
    def analyze_documents(self, corpus_documents: List[Dict[str, Any]], framework_content: str, 
                         experiment_config: Dict[str, Any], model: str = None) -> Dict[str, Any]:
        """
        Compatibility wrapper for the old analyze_documents interface.
        """
        if not corpus_documents:
            return {"analysis_result": None}
        
        # Process the first document (orchestrator processes one at a time)
        document = corpus_documents[0]
        document_content = document.get('content', '')
        document_id = document.get('filename', 'unknown')
        
        # Use the new analyze_document method
        result = self.analyze_document(document_content, framework_content, document_id)
        
        # Convert to old format for compatibility
        # Load the actual artifact data
        scores_data = self._load_artifact_data(result.get("scores_artifact"))
        evidence_data = self._load_artifact_data(result.get("evidence_artifact"))
        work_data = self._load_artifact_data(result.get("work_artifact"))
        
        # Create the old format with raw_analysis_response
        document_analysis = {
            "document_id": document_id,
            "document_name": document_id,
            "dimensional_scores": scores_data.get("scores", {}),
            "evidence": evidence_data.get("evidence", []),
            "computational_work": work_data
        }
        
        analysis_json = {
            "document_analyses": [document_analysis]
        }
        
        raw_response = f"<<<DISCERNUS_ANALYSIS_JSON_v6>>>\n{json.dumps(analysis_json, indent=2)}\n<<<END_DISCERNUS_ANALYSIS_JSON_v6>>>"
        
        return {
            "analysis_result": {
                "result_content": {
                    "scores": scores_data.get("scores", {}),
                    "evidence": evidence_data.get("evidence", []),
                    "work": work_data
                },
                "raw_analysis_response": raw_response,
                "cached": False,
                "success": result.get("success", True)
            }
        }
    
    def _load_artifact_data(self, artifact_id: str) -> Dict[str, Any]:
        """Load artifact data from storage"""
        if not artifact_id:
            return {}
        
        try:
            artifact_bytes = self.storage.get_artifact(artifact_id)
            return json.loads(artifact_bytes.decode('utf-8'))
        except Exception as e:
            print(f"Warning: Could not load artifact {artifact_id}: {e}")
            return {}
