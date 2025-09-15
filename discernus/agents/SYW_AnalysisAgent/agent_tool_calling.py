#!/usr/bin/env python3
"""
Enhanced Analysis Agent with Tool Calling Support
================================================

This agent implements the "Show Your Work" architecture using structured
output via tool calling instead of text parsing.
"""

import json
import base64
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional

from discernus.core.security_boundary import ExperimentSecurityBoundary
from discernus.core.audit_logger import AuditLogger
from discernus.core.local_artifact_storage import LocalArtifactStorage
from discernus.gateway.llm_gateway_enhanced import EnhancedLLMGateway
from discernus.gateway.model_registry import ModelRegistry
# Cache functionality moved to archive - using direct storage for now
# Prompt builder moved to archive - using direct template loading


class EnhancedAnalysisAgentToolCalling:
    """Enhanced Analysis Agent using tool calling for structured output"""

    def __init__(self,
                 security_boundary: ExperimentSecurityBoundary,
                 audit_logger: AuditLogger,
                 artifact_storage: LocalArtifactStorage):
        self.security = security_boundary
        self.audit = audit_logger
        self.storage = artifact_storage
        self.agent_name = "EnhancedAnalysisAgentToolCalling"
        self.prompt_template = self._load_prompt_template()
        self.cache = AnalysisCache(self.storage, self.audit, self.agent_name)
        
        # Initialize enhanced LLM gateway
        self.llm_gateway = EnhancedLLMGateway(ModelRegistry())
        
        self.audit.log_agent_event(self.agent_name, "initialization", {
            "security_boundary": self.security.get_boundary_info(),
            "capabilities": ["tool_calling", "derived_metrics", "structured_output"]
        })

    def _load_prompt_template(self) -> str:
        """Load tool calling prompt template."""
        prompt_path = Path(__file__).parent / "prompt_tool_calling_ultra_simple.txt"
        if not prompt_path.exists():
            raise FileNotFoundError("Could not find prompt_tool_calling_ultra_simple.txt for EnhancedAnalysisAgent")
        with open(prompt_path, 'r') as f:
            return f.read()

    def analyze_document(self,
                        document: Dict[str, Any],
                        framework: Dict[str, Any],
                        model: str = "vertex_ai/gemini-2.5-flash") -> Dict[str, Any]:
        """Analyze a single document using tool calling approach"""
        
        start_time = datetime.now(timezone.utc).isoformat()
        document_id = document.get('id', f"doc_{hashlib.md5(str(document).encode()).hexdigest()[:8]}")
        
        # Create analysis prompt
        prompt = self._create_analysis_prompt(document, framework)
        
        # Define the tool schema - minimal for Gemini 2.5 Pro compatibility
        tools = [{
            "type": "function",
            "function": {
                "name": "record_analysis",
                "description": "Record analysis results",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "document_id": {"type": "string"},
                        "populism_score": {"type": "number"},
                        "authoritarianism_score": {"type": "number"},
                        "evidence": {"type": "string"},
                        "code": {"type": "string"},
                        "output": {"type": "string"}
                    },
                    "required": ["document_id", "populism_score", "authoritarianism_score", "evidence", "code", "output"]
                }
            }
        }]
        
        # Execute LLM call with tools
        system_prompt = "You are an expert discourse analyst. Analyze the document using the framework and call the record_analysis_with_work tool with your results and the code you executed."
        
        self.audit.log_agent_event(self.agent_name, "llm_call_start", {
            "model": model,
            "document_id": document_id
        })
        
        response_content, metadata = self.llm_gateway.execute_call_with_tools(
            model=model,
            prompt=prompt,
            system_prompt=system_prompt,
            tools=tools,
            context=f"Analyzing document {document_id}"
        )
        
        if not metadata.get('success'):
            raise Exception(f"LLM call failed: {metadata.get('error', 'Unknown error')}")
        
        # Extract tool calls from response
        tool_calls = metadata.get('tool_calls', [])
        if not tool_calls:
            print(f"DEBUG: LLM response metadata: {metadata}")
            print(f"DEBUG: LLM response content: {response_content[:500]}...")
            print(f"DEBUG: Tool calls type: {type(tool_calls)}")
            print(f"DEBUG: Tool calls value: {tool_calls}")
            raise Exception("No tool calls found in LLM response")
        
        # Process the first tool call (should be record_analysis_with_work)
        tool_call = tool_calls[0]
        
        # Handle both dict format and ChatCompletionMessageToolCall format
        if hasattr(tool_call, 'function'):
            # ChatCompletionMessageToolCall format
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
        else:
            # Dict format
            function_name = tool_call.get('function', {}).get('name')
            function_args = json.loads(tool_call['function']['arguments'])
        
        if function_name != 'record_analysis':
            raise Exception(f"Expected record_analysis tool call, got: {function_name}")
        
        # Save artifacts using the structured data (no parsing needed!)
        analysis_artifact = self._save_analysis_artifact_simplified(function_args)
        work_artifact = self._save_work_artifact_simplified(function_args)
        
        self.audit.log_agent_event(self.agent_name, "analysis_complete", {
            "document_id": function_args["document_id"],
            "analysis_artifact": analysis_artifact,
            "work_artifact": work_artifact,
            "usage": metadata.get('usage', {})
        })
        
        return {
            "document_id": function_args["document_id"],
            "analysis_artifact": analysis_artifact,
            "work_artifact": work_artifact,
            "metadata": metadata
        }
    
    def _create_analysis_prompt(self, document: Dict[str, Any], framework: Dict[str, Any]) -> str:
        """Create the analysis prompt for the LLM"""
        template = self._load_prompt_template()
        
        return template.format(
            document_content=document.get('content', '')
        )
    
    def _save_analysis_artifact_simplified(self, function_args: Dict[str, Any]) -> str:
        """Save the analysis results as a clean artifact (minimal schema)"""
        analysis_data = {
            "document_id": function_args["document_id"],
            "scores": {
                "populism": {
                    "raw_score": function_args["populism_score"],
                    "salience": 1.0,
                    "confidence": 0.9
                },
                "authoritarianism": {
                    "raw_score": function_args["authoritarianism_score"],
                    "salience": 1.0,
                    "confidence": 0.9
                }
            },
            "evidence": [{
                "dimension": "populism",
                "quote": function_args["evidence"],
                "reasoning": "Analysis evidence"
            }],
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        content = json.dumps(analysis_data, indent=2).encode('utf-8')
        return self.storage.put_artifact(content, {"artifact_type": "analysis"})
    
    def _save_work_artifact_simplified(self, function_args: Dict[str, Any]) -> str:
        """Save the computational work as a separate artifact (minimal schema)"""
        work_data = {
            "document_id": function_args["document_id"],
            "executed_code": function_args["code"],
            "execution_output": function_args["output"],
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        content = json.dumps(work_data, indent=2).encode('utf-8')
        return self.storage.put_artifact(content, {"artifact_type": "work"})
