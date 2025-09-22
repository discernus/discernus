#!/usr/bin/env python3
"""
V2 Statistical Agent - Atomic Processing Implementation
=====================================================

This agent processes atomic score and derived metrics artifacts from the AnalysisAgent
and performs comprehensive statistical analysis.

THIN Principles:
- Each document's scores are processed individually
- LLM handles all statistical intelligence
- Agent only adapts interfaces, no business logic
- Atomic artifacts for downstream consumption
"""

import json
import logging
import yaml
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional

from discernus.core.security_boundary import ExperimentSecurityBoundary
from discernus.core.audit_logger import AuditLogger
from discernus.core.local_artifact_storage import LocalArtifactStorage
from discernus.core.agent_result import AgentResult
from discernus.core.run_context import RunContext
from discernus.core.standard_agent import StandardAgent
from discernus.gateway.llm_gateway_enhanced import EnhancedLLMGateway
from discernus.gateway.model_registry import get_model_registry


class V2StatisticalAgent(StandardAgent):
    """
    V2 Statistical Agent for atomic processing of score artifacts.
    
    This agent processes individual score and derived metrics artifacts
    from the AnalysisAgent and performs comprehensive statistical analysis.
    """
    
    def __init__(self, 
                 security: ExperimentSecurityBoundary,
                 storage: LocalArtifactStorage,
                 audit: AuditLogger):
        """
        Initialize the V2 Statistical Agent.
        
        Args:
            security: Security boundary for file operations
            storage: Content-addressable artifact storage
            audit: Audit logger for comprehensive event tracking
        """
        super().__init__(security, storage, audit)
        self.agent_name = "V2StatisticalAgent"
        self.logger = logging.getLogger(__name__)
        
        # Initialize LLM gateway
        self.gateway = EnhancedLLMGateway(get_model_registry())
        
        self.logger.info(f"Initialized {self.agent_name}")
    
    def _load_prompt_template(self) -> str:
        """Load the statistical analysis prompt template from YAML file."""
        prompt_path = Path(__file__).parent / "prompt.yaml"
        if not prompt_path.exists():
            error_msg = f"StatisticalAgent prompt file not found at {prompt_path}"
            self.audit.log_agent_event(self.agent_name, "prompt_error", {"error": error_msg})
            raise FileNotFoundError(error_msg)
        
        with open(prompt_path, 'r') as f:
            yaml_content = f.read()
        prompt_data = yaml.safe_load(yaml_content)
        return prompt_data['template']
    
    def get_capabilities(self) -> Dict[str, Any]:
        """
        Get agent capabilities and metadata.
        
        Returns:
            Dictionary describing agent capabilities
        """
        return {
            "agent_name": self.agent_name,
            "agent_type": "V2StatisticalAgent",
            "capabilities": [
                "statistical_analysis",
                "atomic_score_processing"
            ],
            "input_types": ["score_extraction_artifacts", "derived_metrics_artifacts"],
            "output_types": ["statistical_analysis"],
            "models_used": ["vertex_ai/gemini-2.5-pro", "vertex_ai/gemini-2.5-flash-lite"]
        }
    
    def execute(self, run_context: RunContext) -> AgentResult:
        """
        Execute statistical analysis on atomic score artifacts.
        
        Args:
            run_context: Run context containing analysis artifacts and metadata
            
        Returns:
            AgentResult with statistical analysis artifacts
        """
        try:
            self.logger.info("Starting V2 Statistical Agent execution")
            self.audit.log_agent_event(self.agent_name, "execution_started", {
                "run_context_type": type(run_context).__name__
            })
            
            # Validate run context
            if not run_context:
                return AgentResult(
                    success=False,
                    artifacts=[],
                    metadata={"agent_name": self.agent_name, "error": "run_context is required"},
                    error_message="run_context is required"
                )
            
            # THIN: Read framework file directly
            framework_content = self._read_framework_file(run_context.framework_path)
            if not framework_content:
                return AgentResult(
                    success=False,
                    artifacts=[],
                    metadata={"agent_name": self.agent_name, "error": "failed to read framework file"},
                    error_message=f"Failed to read framework file: {run_context.framework_path}"
                )
            
            # Get analysis artifacts (list of artifact hashes)
            analysis_artifacts = run_context.analysis_artifacts
            self.logger.info(f"Received analysis_artifacts: {analysis_artifacts}")
            if not analysis_artifacts:
                return AgentResult(
                    success=False,
                    artifacts=[],
                    metadata={"agent_name": self.agent_name, "error": "analysis_artifacts not found"},
                    error_message="analysis_artifacts not found in RunContext"
                )
            
            # Process atomic score artifacts
            raw_artifacts = self._collect_atomic_scores(analysis_artifacts)
            if not raw_artifacts:
                return AgentResult(
                    success=False,
                    artifacts=[],
                    metadata={"agent_name": self.agent_name, "error": "no artifacts found"},
                    error_message="No artifacts found in analysis artifacts"
                )
            
            # Generate batch ID
            batch_id = f"stats_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"
            
            # Step 1: Statistical Analysis (Python code generation + execution)
            statistical_analysis_content = self._step1_statistical_analysis(framework_content, raw_artifacts, batch_id)
            if not statistical_analysis_content:
                return AgentResult(
                    success=False,
                    artifacts=[],
                    metadata={"agent_name": self.agent_name, "error": "statistical analysis failed"},
                    error_message="Statistical analysis failed"
                )
            
            # Parse the structured response to extract statistical_results
            try:
                structured_data = json.loads(statistical_analysis_content)
                statistical_results = structured_data.get("statistical_results", {})
                self.logger.info(f"Successfully parsed statistical_results with {len(statistical_results)} keys")
            except (json.JSONDecodeError, KeyError) as e:
                self.logger.error(f"Could not parse structured response: {e}")
                self.logger.error(f"Raw content: {statistical_analysis_content[:500]}...")
                # Fallback to storing raw content
                statistical_results = {}
            
            # Store Step 1 artifact in format expected by synthesis agent
            statistical_artifact_data = {
                "analysis_id": f"stats_{batch_id}",
                "step": "statistical_analysis",
                "model_used": "vertex_ai/gemini-2.5-pro",
                "statistical_results": statistical_results,
                "statistical_analysis_content": statistical_analysis_content,  # Keep raw content for debugging
                "documents_processed": len(raw_artifacts),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
            statistical_content_bytes = json.dumps(statistical_artifact_data, indent=2).encode('utf-8')
            statistical_artifact_hash = self.storage.put_artifact(
                statistical_content_bytes,
                {"artifact_type": "statistical_analysis", "batch_id": batch_id}
            )
            
            
            # Create artifacts list with proper hashes
            artifacts = [
                {
                    "type": "statistical_analysis",
                    "content": statistical_artifact_data,
                    "metadata": {
                        "artifact_type": "statistical_analysis",
                        "phase": "statistical",
                        "batch_id": batch_id,
                        "timestamp": datetime.now().isoformat(),
                        "agent_name": self.agent_name,
                        "artifact_hash": statistical_artifact_hash
                    }
                }
            ]
            
            # Update run context with proper artifact hashes
            run_context.statistical_artifacts = [statistical_artifact_hash]
            run_context.statistical_results = statistical_analysis_content  # Pass the raw content to synthesis agent
            
            self.audit.log_agent_event(self.agent_name, "execution_completed", {
                "batch_id": batch_id,
                "artifacts_created": len(artifacts),
                "documents_processed": len(raw_artifacts)
            })
            
            return AgentResult(
                success=True,
                artifacts=artifacts,
                metadata={
                    "agent_name": self.agent_name,
                    "batch_id": batch_id,
                    "documents_processed": len(raw_artifacts),
                    "artifacts_created": len(artifacts)
                }
            )
            
        except Exception as e:
            self.logger.error(f"V2StatisticalAgent execution failed: {e}")
            self.audit.log_agent_event(self.agent_name, "execution_failed", {
                "error": str(e)
            })
            return AgentResult(
                success=False,
                artifacts=[],
                metadata={"agent_name": self.agent_name, "error": str(e)},
                error_message=f"V2StatisticalAgent execution failed: {str(e)}"
            )
    
    def _collect_atomic_scores(self, analysis_artifacts: List[str]) -> List[Dict[str, Any]]:
        """
        Collect raw artifacts for statistical analysis - NO PARSING.
        
        Args:
            analysis_artifacts: List of artifact hashes from analysis phase
            
        Returns:
            List of raw artifact data for LLM processing
        """
        self.logger.info(f"Collecting raw artifacts from {len(analysis_artifacts)} analysis artifacts")
        raw_artifacts = []
        
        for artifact_hash in analysis_artifacts:
            try:
                # Load artifact
                artifact_bytes = self.storage.get_artifact(artifact_hash)
                if not artifact_bytes:
                    self.logger.warning(f"Could not load artifact {artifact_hash}")
                    continue
                
                # Store raw artifact data - let LLM figure out how to use it
                raw_artifacts.append({
                    "artifact_hash": artifact_hash,
                    "raw_content": artifact_bytes.decode('utf-8'),
                    "artifact_type": "analysis_artifact"
                })
                
            except Exception as e:
                self.logger.warning(f"Error loading artifact {artifact_hash}: {e}")
                continue
        
        return raw_artifacts
    
    def _step1_statistical_analysis(self, framework_content: str, raw_artifacts: List[Dict[str, Any]], batch_id: str) -> Optional[str]:
        """
        Step 1: Perform statistical analysis internally using LLM capabilities.
        
        Args:
            framework_content: Framework content for context
            raw_artifacts: List of raw artifact data from analysis phase
            batch_id: Batch identifier
            
        Returns:
            Complete LLM response with statistical results, or None if failed
        """
        try:
            # Load the externalized prompt template
            prompt_template = self._load_prompt_template()
            self.logger.info(f"Loaded prompt template, length: {len(prompt_template)}")
            
            # Prepare the prompt with actual data
            prompt = prompt_template.format(
                framework_content=framework_content,
                experiment_name="mlkmx",
                experiment_description="MLK-MX Civil Rights Discourse Analysis",
                research_questions="How do different rhetorical strategies in civil rights discourse manifest through the Cohesive Flourishing Framework dimensions?",
                experiment_content=framework_content,  # Using framework as experiment content for now
                data_columns="dimensional_scores, derived_metrics, evidence",
                sample_data=json.dumps(raw_artifacts[:2], indent=2) if len(raw_artifacts) >= 2 else json.dumps(raw_artifacts, indent=2),
                corpus_manifest="Two documents: Malcolm X 'The Ballot or the Bullet' and MLK 'Letter from Birmingham Jail'"
            )

            self.audit.log_agent_event(self.agent_name, "step1_started", {
                "batch_id": batch_id,
                "step": "statistical_analysis",
                "model": "vertex_ai/gemini-2.5-pro",
                "artifacts_count": len(raw_artifacts)
            })
            
            # Call LLM
            response = self.gateway.execute_call(
                model="vertex_ai/gemini-2.5-pro",
                prompt=prompt
            )
            
            if isinstance(response, tuple):
                content, metadata = response
            else:
                content = response.get('content', '')
                metadata = response.get('metadata', {})
            
            self.logger.info(f"LLM response length: {len(content)}")
            self.logger.info(f"LLM response preview: {content[:200]}...")
            
            # Parse the LLM response to extract structured JSON format
            if content and content.strip():
                try:
                    # Try to extract JSON from the response
                    # Look for JSON code blocks or direct JSON
                    import re
                    
                    # First try to find JSON code blocks
                    json_match = re.search(r'```json\s*(\{.*?\})\s*```', content, re.DOTALL)
                    if json_match:
                        json_str = json_match.group(1)
                    else:
                        # Try to find JSON without code blocks - be more flexible
                        # Look for JSON that might have leading whitespace or newlines
                        json_match = re.search(r'\s*\{.*\}', content, re.DOTALL)
                        if json_match:
                            json_str = json_match.group(0).strip()
                        else:
                            # Fallback: return raw content
                            self.logger.warning("Could not extract JSON from statistical analysis response")
                            return content.strip()
                    
                    # Debug: Log the extracted JSON string
                    self.logger.info(f"Extracted JSON string: {json_str[:200]}...")
                    
                    # Parse the JSON
                    try:
                        structured_response = json.loads(json_str)
                    except json.JSONDecodeError as json_error:
                        self.logger.error(f"JSON parsing failed: {json_error}")
                        self.logger.error(f"JSON string: {json_str[:500]}...")
                        # Try to fix common JSON issues
                        json_str_fixed = json_str.replace('\n', ' ').replace('\r', ' ')
                        try:
                            structured_response = json.loads(json_str_fixed)
                        except json.JSONDecodeError as second_error:
                            self.logger.error(f"JSON parsing failed even after fixing: {second_error}")
                            self.logger.error(f"Fixed JSON string: {json_str_fixed[:500]}...")
                            # Final fallback: return raw content
                            self.logger.warning("Could not parse JSON even after fixing, returning raw content")
                            return content.strip()
                    
                    self.audit.log_agent_event(self.agent_name, "step1_completed", {
                        "batch_id": batch_id,
                        "step": "statistical_analysis",
                        "response_length": len(content),
                        "structured_format": True
                    })
                    
                    return json.dumps(structured_response, indent=2)
                    
                except json.JSONDecodeError as e:
                    self.logger.warning(f"Could not parse JSON from statistical analysis response: {e}")
                    # Fallback: return raw content
                    return content.strip()
            else:
                self.logger.error("Statistical analysis returned empty response")
                return None
                
        except Exception as e:
            self.logger.error(f"Step 1 failed: {e}")
            return None
    
    
    def _read_framework_file(self, framework_path: str) -> Optional[str]:
        """Read framework content directly from file."""
        try:
            return Path(framework_path).read_text(encoding='utf-8')
        except Exception as e:
            self.logger.error(f"Failed to read framework file {framework_path}: {e}")
            return None