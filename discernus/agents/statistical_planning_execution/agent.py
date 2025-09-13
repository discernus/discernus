#!/usr/bin/env python3
"""
Statistical Planning + Execution Agent
======================================

This agent performs batch statistical analysis on verified analysis artifacts
using tool calling for structured output.
"""

import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional

from discernus.core.security_boundary import ExperimentSecurityBoundary
from discernus.core.audit_logger import AuditLogger
from discernus.core.local_artifact_storage import LocalArtifactStorage
from discernus.gateway.llm_gateway_enhanced import EnhancedLLMGateway
from discernus.gateway.model_registry import ModelRegistry


class StatisticalPlanningExecutionAgent:
    """Statistical Planning + Execution Agent using tool calling for batch processing"""

    def __init__(self,
                 security_boundary: ExperimentSecurityBoundary,
                 audit_logger: AuditLogger,
                 artifact_storage: LocalArtifactStorage):
        self.security = security_boundary
        self.audit = audit_logger
        self.storage = artifact_storage
        self.agent_name = "StatisticalPlanningExecutionAgent"
        
        # Initialize enhanced LLM gateway
        self.llm_gateway = EnhancedLLMGateway(ModelRegistry())
        
        self.audit.log_agent_event(self.agent_name, "initialization", {
            "security_boundary": self.security.get_boundary_info(),
            "capabilities": ["batch_statistical_analysis", "tool_calling", "structured_output"]
        })

    def analyze_batch(self, 
                     analysis_artifact_ids: List[str], 
                     hypotheses: Dict[str, Any],
                     model: str = "vertex_ai/gemini-2.5-flash") -> Dict[str, Any]:
        """Perform batch statistical analysis on verified analysis artifacts"""
        
        start_time = datetime.now(timezone.utc).isoformat()
        
        # Load all analysis artifacts
        analysis_data = []
        for artifact_id in analysis_artifact_ids:
            artifact_content = self.storage.get_artifact(artifact_id)
            if not artifact_content:
                raise ValueError(f"Could not load analysis artifact: {artifact_id}")
            
            analysis_content = json.loads(artifact_content.decode('utf-8'))
            analysis_data.append(analysis_content)
        
        self.audit.log_agent_event(self.agent_name, "batch_analysis_start", {
            "model": model,
            "num_artifacts": len(analysis_artifact_ids),
            "hypotheses": list(hypotheses.keys()) if hypotheses else []
        })
        
        # Create statistical analysis prompt
        prompt = self._create_statistical_prompt(analysis_data, hypotheses)
        
        # Define the tool schema
        tools = [{
            "type": "function",
            "function": {
                "name": "record_statistical_results",
                "description": "Record statistical analysis results and computational work",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "statistics_payload": {
                            "type": "object",
                            "properties": {
                                "tests": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "name": {"type": "string"},
                                            "parameters": {"type": "object"},
                                            "metrics": {"type": "object"}
                                        },
                                        "required": ["name", "metrics"]
                                    }
                                },
                                "aggregated_rows": {
                                    "type": "array",
                                    "items": {"type": "object"}
                                }
                            },
                            "required": ["tests", "aggregated_rows"]
                        },
                        "executed_code": {"type": "string"},
                        "execution_output": {"type": "string"}
                    },
                    "required": ["statistics_payload", "executed_code", "execution_output"]
                }
            }
        }]
        
        # Execute LLM call with tools
        system_prompt = "You are a statistical analysis expert. Analyze the provided data using appropriate statistical tests and call the record_statistical_results tool with your results and the code you executed."
        
        response_content, metadata = self.llm_gateway.execute_call_with_tools(
            model=model,
            prompt=prompt,
            system_prompt=system_prompt,
            tools=tools,
            context=f"Statistical analysis of {len(analysis_data)} documents"
        )
        
        if not metadata.get('success'):
            raise Exception(f"Statistical analysis LLM call failed: {metadata.get('error', 'Unknown error')}")
        
        # Extract tool calls from response
        tool_calls = metadata.get('tool_calls', [])
        if not tool_calls:
            raise Exception("No tool calls found in statistical analysis response")
        
        # Process the first tool call (should be record_statistical_results)
        tool_call = tool_calls[0]
        if tool_call.get('function', {}).get('name') != 'record_statistical_results':
            raise Exception(f"Expected record_statistical_results tool call, got: {tool_call.get('function', {}).get('name')}")
        
        # Parse the tool call arguments
        function_args = json.loads(tool_call['function']['arguments'])
        
        # Save artifacts using the structured data
        statistics_artifact = self._save_statistics_artifact(function_args)
        work_artifact = self._save_statistical_work_artifact(function_args)
        csv_artifact = self._save_statistical_csv_artifact(function_args)
        
        self.audit.log_agent_event(self.agent_name, "batch_analysis_complete", {
            "statistics_artifact": statistics_artifact,
            "work_artifact": work_artifact,
            "csv_artifact": csv_artifact,
            "usage": metadata.get('usage', {})
        })
        
        return {
            "statistics_artifact": statistics_artifact,
            "work_artifact": work_artifact,
            "csv_artifact": csv_artifact,
            "metadata": metadata
        }
    
    def _create_statistical_prompt(self, analysis_data: List[Dict[str, Any]], 
                                  hypotheses: Dict[str, Any]) -> str:
        """Create the statistical analysis prompt for the LLM"""
        
        # Extract numerical data for statistical analysis
        numerical_data = []
        for i, analysis in enumerate(analysis_data):
            row = {
                "document_id": analysis.get('document_id', f'doc_{i}'),
                "framework": analysis.get('framework_name', 'unknown'),
                "scores": analysis.get('scores', {}),
                "derived_metrics": analysis.get('derived_metrics', {})
            }
            numerical_data.append(row)
        
        return f"""
Perform comprehensive statistical analysis on the following dataset of document analyses.

DATASET:
{json.dumps(numerical_data, indent=2)}

HYPOTHESES TO TEST:
{json.dumps(hypotheses, indent=2)}

STATISTICAL ANALYSIS REQUIREMENTS:
1. Generate appropriate statistical tests based on the data and hypotheses
2. Calculate descriptive statistics for all dimensions and derived metrics
3. Perform hypothesis testing (t-tests, ANOVA, correlation analysis, etc.)
4. Generate aggregated data rows for CSV export
5. Use Python with numpy, pandas, scipy.stats, and pingouin libraries
6. Execute your analysis code internally
7. Call the record_statistical_results tool with your results

COMMON STATISTICAL TESTS TO CONSIDER:
- Descriptive statistics (mean, median, std, min, max)
- Correlation analysis between dimensions
- ANOVA for comparing groups
- T-tests for pairwise comparisons
- Reliability analysis (Cronbach's alpha)
- Effect size calculations

Ensure your analysis is appropriate for the data type and research questions.
"""
    
    def _save_statistics_artifact(self, function_args: Dict[str, Any]) -> str:
        """Save the statistical results as a clean artifact"""
        statistics_data = {
            "tests": function_args["statistics_payload"]["tests"],
            "aggregated_rows": function_args["statistics_payload"]["aggregated_rows"],
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        content = json.dumps(statistics_data, indent=2).encode('utf-8')
        return self.storage.put_artifact(content, {
            "artifact_type": "statistics",
            "analysis_type": "batch_statistical_analysis"
        })
    
    def _save_statistical_work_artifact(self, function_args: Dict[str, Any]) -> str:
        """Save the statistical computational work as a separate artifact"""
        work_data = {
            "executed_code": function_args["executed_code"],
            "execution_output": function_args["execution_output"],
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        content = json.dumps(work_data, indent=2).encode('utf-8')
        return self.storage.put_artifact(content, {
            "artifact_type": "statistical_work",
            "analysis_type": "batch_statistical_analysis"
        })
    
    def _save_statistical_csv_artifact(self, function_args: Dict[str, Any]) -> str:
        """Save the statistical CSV data as a separate artifact"""
        # Convert aggregated rows to CSV format
        aggregated_rows = function_args["statistics_payload"]["aggregated_rows"]
        
        if not aggregated_rows:
            csv_content = "No data available\n"
        else:
            # Convert to CSV format
            import csv
            import io
            
            output = io.StringIO()
            fieldnames = aggregated_rows[0].keys()
            writer = csv.DictWriter(output, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(aggregated_rows)
            csv_content = output.getvalue()
        
        content = csv_content.encode('utf-8')
        return self.storage.put_artifact(content, {
            "artifact_type": "statistical_csv",
            "analysis_type": "batch_statistical_analysis"
        })
