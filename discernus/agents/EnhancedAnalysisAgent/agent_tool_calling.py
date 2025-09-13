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
from .cache import AnalysisCache
from .prompt_builder import create_analysis_prompt


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
        prompt_path = Path(__file__).parent / "prompt_tool_calling.txt"
        if not prompt_path.exists():
            raise FileNotFoundError("Could not find prompt_tool_calling.txt for EnhancedAnalysisAgent")
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
        
        # Define the tool schema
        tools = [{
            "type": "function",
            "function": {
                "name": "record_analysis_with_work",
                "description": "Record analysis results with computational work",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "document_id": {"type": "string"},
                        "document_hash": {"type": "string"},
                        "framework_name": {"type": "string"},
                        "framework_version": {"type": "string"},
                        "analysis_payload": {
                            "type": "object",
                            "properties": {
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
                                },
                                "derived_metrics": {
                                    "type": "object",
                                    "additionalProperties": {"type": "number"}
                                },
                                "evidence": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "dimension": {"type": "string"},
                                            "quote": {"type": "string"},
                                            "source": {"type": "string"},
                                            "offset": {"type": "integer"}
                                        },
                                        "required": ["dimension", "quote"]
                                    }
                                }
                            },
                            "required": ["scores", "derived_metrics", "evidence"]
                        },
                        "executed_code": {"type": "string"},
                        "execution_output": {"type": "string"}
                    },
                    "required": ["document_id", "document_hash", "framework_name", "framework_version",
                                "analysis_payload", "executed_code", "execution_output"]
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
            raise Exception("No tool calls found in LLM response")
        
        # Process the first tool call (should be record_analysis_with_work)
        tool_call = tool_calls[0]
        if tool_call.get('function', {}).get('name') != 'record_analysis_with_work':
            raise Exception(f"Expected record_analysis_with_work tool call, got: {tool_call.get('function', {}).get('name')}")
        
        # Parse the tool call arguments
        function_args = json.loads(tool_call['function']['arguments'])
        
        # Save artifacts using the structured data (no parsing needed!)
        analysis_artifact = self._save_analysis_artifact(function_args)
        work_artifact = self._save_work_artifact(function_args)
        
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
        # Encode document content
        content_bytes = document.get('content', '').encode('utf-8')
        content_b64 = base64.b64encode(content_bytes).decode('utf-8')
        
        # Encode framework
        framework_json = json.dumps(framework, indent=2)
        framework_b64 = base64.b64encode(framework_json.encode('utf-8')).decode('utf-8')
        
        # Create documents list
        documents = [{
            'index': 1,
            'hash': hashlib.sha256(content_bytes).hexdigest(),
            'content': content_b64,
            'filename': document.get('filename', document.get('id', 'document'))
        }]
        
        # Use the existing prompt builder but with tool calling template
        return create_analysis_prompt(
            self.prompt_template,
            f"analysis_{document.get('id', 'unknown')}",
            framework_b64,
            documents
        )
    
    def _save_analysis_artifact(self, function_args: Dict[str, Any]) -> str:
        """Save the analysis results as a clean artifact"""
        analysis_data = {
            "document_id": function_args["document_id"],
            "document_hash": function_args["document_hash"],
            "framework_name": function_args["framework_name"],
            "framework_version": function_args["framework_version"],
            "scores": function_args["analysis_payload"]["scores"],
            "derived_metrics": function_args["analysis_payload"]["derived_metrics"],
            "evidence": function_args["analysis_payload"]["evidence"],
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        content = json.dumps(analysis_data, indent=2).encode('utf-8')
        return self.storage.put_artifact(content, {
            "artifact_type": "analysis",
            "document_id": function_args["document_id"],
            "framework": function_args["framework_name"]
        })
    
    def _save_work_artifact(self, function_args: Dict[str, Any]) -> str:
        """Save the computational work as a separate artifact"""
        work_data = {
            "document_id": function_args["document_id"],
            "executed_code": function_args["executed_code"],
            "execution_output": function_args["execution_output"],
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        content = json.dumps(work_data, indent=2).encode('utf-8')
        return self.storage.put_artifact(content, {
            "artifact_type": "work",
            "document_id": function_args["document_id"],
            "framework": function_args["framework_name"]
        })
