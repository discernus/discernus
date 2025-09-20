#!/usr/bin/env python3
"""
Statistical Agent - THIN v2.0 Architecture
==========================================

Performs comprehensive statistical analysis using LLM internal execution 
with minimal tool calling for verification and CSV generation.

Architecture:
- Step 1: Statistical Execution (Pro) - Generate + execute statistical functions
- Step 2: Verification (Lite + tool calling) - Adversarial verification 
- Step 3: CSV Generation (Lite + tool calling) - Transform to researcher format
"""

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional
import yaml

from ...core.security_boundary import ExperimentSecurityBoundary
from ...core.local_artifact_storage import LocalArtifactStorage
from ...core.audit_logger import AuditLogger
from ...core.verbose_tracing import trace_calls, trace_section, trace_data
from ...gateway.llm_gateway_enhanced import EnhancedLLMGateway
from ...gateway.model_registry import get_model_registry


class StatisticalAgent:
    """
    THIN Statistical Agent for comprehensive statistical analysis.
    
    Uses LLM internal execution for statistical planning, analysis, and code generation,
    with minimal tool calling for verification and CSV output.
    """

    def __init__(self, 
                 security: ExperimentSecurityBoundary,
                 storage: LocalArtifactStorage,
                 audit: AuditLogger,
                 experiment_metadata: Optional[Dict[str, Any]] = None):
        """
        Initialize the Statistical Agent.
        
        Args:
            security: Security boundary for file operations
            storage: Content-addressable artifact storage
            audit: Audit logger for comprehensive event tracking
            experiment_metadata: Optional experiment configuration
        """
        self.agent_name = "StatisticalAgent"
        self.security = security
        self.storage = storage
        self.audit = audit
        self.experiment_metadata = experiment_metadata or {}
        
        # Initialize LLM gateway
        self.gateway = EnhancedLLMGateway(get_model_registry())
        
        # Load prompt template
        self.prompt_template = self._load_prompt_template()
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
        
    def _load_prompt_template(self) -> str:
        """Load the statistical analysis prompt template."""
        prompt_path = Path(__file__).parent / "prompt.yaml"
        try:
            with open(prompt_path, 'r') as f:
                yaml_content = yaml.safe_load(f)
                return yaml_content.get('template', '')
        except FileNotFoundError:
            self.logger.error(f"Prompt template not found: {prompt_path}")
            return ""
        except Exception as e:
            self.logger.error(f"Error loading prompt template: {e}")
            return ""

    @trace_calls(include_args=True, include_return=True)
    def analyze_batch(self,
                     framework_content: str,
                     experiment_content: str,
                     corpus_manifest: str,
                     batch_id: str,
                     analysis_artifact_hashes: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Perform comprehensive statistical analysis on a batch of analysis artifacts.
        
        Args:
            framework_content: Full framework markdown content
            experiment_content: Full experiment.md content  
            corpus_manifest: Corpus manifest content
            batch_id: Unique identifier for this batch
            
        Returns:
            Dictionary containing statistical results, verification status, and CSV paths
        """
        
        
        self.audit.log_agent_event(self.agent_name, "batch_analysis_started", {
            "batch_id": batch_id,
            "framework_length": len(framework_content),
            "experiment_length": len(experiment_content)
        })
        
        # Check cache first
        cached_result = self.check_cache(batch_id)
        if cached_result:
            return cached_result
        
        try:
            # Step 1: Statistical Execution (Pro)
            statistical_result = self._step1_statistical_execution(
                framework_content, experiment_content, corpus_manifest, batch_id, analysis_artifact_hashes
            )
            
            # Step 2: Verification (Lite + tool calling)
            verification_result = self._step2_verification(
                statistical_result, batch_id
            )
            
            # Step 3: CSV Generation removed - now handled by AnalysisAgent
            
            # Calculate total costs and performance metrics
            total_cost_info = self._calculate_total_costs(statistical_result, verification_result, {})
            
            # Combine results
            final_result = {
                "batch_id": batch_id,
                "statistical_analysis": statistical_result,
                "verification": verification_result,
                "total_cost_info": total_cost_info,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "agent_name": self.agent_name
            }
            
            self.audit.log_agent_event(self.agent_name, "batch_analysis_completed", {
                "batch_id": batch_id,
                "verification_status": verification_result.get("verification_status", "unknown"),
                "total_cost_info": total_cost_info
            })
            
            # Store result in cache for future use
            cache_hash = self.store_cache(batch_id, final_result)
            
            # Add cache hash to final result for orchestrator
            final_result["cache_hash"] = cache_hash
            
            return final_result
            
        except Exception as e:
            error_msg = f"Statistical analysis failed for batch {batch_id}: {str(e)}"
            self.logger.error(error_msg)
            self.audit.log_agent_event(self.agent_name, "batch_analysis_failed", {
                "batch_id": batch_id,
                "error": str(e)
            })
            raise

    @trace_calls(include_args=True, include_return=True)
    def _step1_statistical_execution(self,
                                   framework_content: str,
                                   experiment_content: str,
                                   corpus_manifest: str,
                                   batch_id: str,
                                   analysis_artifact_hashes: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Step 1: Generate and execute statistical analysis functions using Gemini 2.5 Pro.
        
        Based on the existing AutomatedStatisticalAnalysisAgent approach but with
        LLM internal execution of the generated functions.
        """
        
        with trace_section("Discover analysis artifacts"):
            # Discover and load analysis artifacts from shared cache
            analysis_artifacts = self._discover_analysis_artifacts(batch_id, analysis_artifact_hashes)
            trace_data("analysis_artifacts", f"Found {len(analysis_artifacts)} artifacts: {list(analysis_artifacts.keys())}")
        
        if not analysis_artifacts:
            raise ValueError(f"No analysis artifacts found for batch {batch_id}")
        
        # Prepare prompt using existing statistical analysis template
        prompt = self._prepare_statistical_prompt(
            framework_content, experiment_content, corpus_manifest, analysis_artifacts
        )
        
        self.audit.log_agent_event(self.agent_name, "step1_started", {
            "batch_id": batch_id,
            "step": "statistical_execution",
            "model": "vertex_ai/gemini-2.5-pro",
            "artifacts_count": len(analysis_artifacts)
        })
        
        # Execute with Pro model for complex statistical analysis
        start_time = datetime.now(timezone.utc)
        response = self.gateway.execute_call(
            model="vertex_ai/gemini-2.5-pro",
            prompt=prompt
        )
        end_time = datetime.now(timezone.utc)
        execution_time = (end_time - start_time).total_seconds()
        
        if isinstance(response, tuple):
            content, metadata = response
        else:
            content = response.get('content', '')
            metadata = response.get('metadata', {})
        
        # Extract cost information from metadata
        cost_info = {
            "model": "vertex_ai/gemini-2.5-pro",
            "execution_time_seconds": execution_time,
            "response_cost": metadata.get('response_cost', 0.0),
            "input_tokens": metadata.get('input_tokens', 0),
            "output_tokens": metadata.get('output_tokens', 0),
            "total_tokens": metadata.get('total_tokens', 0),
            "prompt_length": len(prompt),
            "response_length": len(content)
        }
        
        # Save statistical execution result with cost tracking
        statistical_result = {
            "batch_id": batch_id,
            "step": "statistical_execution",
            "model_used": "vertex_ai/gemini-2.5-pro",
            "statistical_functions_and_results": content,
            "analysis_artifacts_processed": len(analysis_artifacts),
            "cost_info": cost_info,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        statistical_hash = self.storage.put_artifact(
            json.dumps(statistical_result, indent=2).encode('utf-8'),
            {"artifact_type": "statistical_analysis", "batch_id": batch_id}
        )
        
        statistical_result['artifact_hash'] = statistical_hash
        
        self.audit.log_agent_event(self.agent_name, "step1_completed", {
            "batch_id": batch_id,
            "step": "statistical_execution",
            "artifact_hash": statistical_hash,
            "response_length": len(content),
            "cost_info": cost_info
        })
        
        return statistical_result

    def _step2_verification(self, 
                          statistical_result: Dict[str, Any], 
                          batch_id: str) -> Dict[str, Any]:
        """
        Step 2: Verify statistical analysis by re-executing functions using Flash Lite.
        
        Similar to the analysis agent's verification step - adversarial checking
        by re-running the generated functions and comparing results.
        """
        
        # Define verification tool
        verification_tools = [
            {
                "name": "verify_statistical_analysis",
                "description": "Verify that the statistical analysis functions and results are correct",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "verified": {
                            "type": "boolean",
                            "description": "Whether the statistical analysis is mathematically correct"
                        }
                    },
                    "required": ["verified"]
                }
            }
        ]
        
        prompt = f"""Re-execute and verify the statistical analysis functions and results:

STATISTICAL FUNCTIONS AND RESULTS:
{statistical_result['statistical_functions_and_results']}

Your task:
1. Extract the Python functions from the statistical analysis
2. Re-execute them with the same data
3. Compare your results with the reported results
4. Call the verify_statistical_analysis tool with your verification result

If the functions execute correctly and produce the same results, call with verified=true.
If there are errors or discrepancies, call with verified=false."""

        self.audit.log_agent_event(self.agent_name, "step2_started", {
            "batch_id": batch_id,
            "step": "verification",
            "model": "vertex_ai/gemini-2.5-flash-lite"
        })

        start_time = datetime.now(timezone.utc)
        response_content, response_metadata = self.gateway.execute_call_with_tools(
            model="vertex_ai/gemini-2.5-flash-lite",
            prompt=prompt,
            tools=verification_tools
        )
        end_time = datetime.now(timezone.utc)
        execution_time = (end_time - start_time).total_seconds()
        
        # Extract cost information from response metadata
        verification_cost_info = {
            "model": "vertex_ai/gemini-2.5-flash-lite",
            "execution_time_seconds": execution_time,
            "prompt_length": len(prompt),
            "response_cost": response_metadata.get('response_cost', 0.0),
            "input_tokens": response_metadata.get('input_tokens', 0),
            "output_tokens": response_metadata.get('output_tokens', 0),
            "total_tokens": response_metadata.get('total_tokens', 0)
        }
        
        # Extract verification result from metadata (tool calls are in metadata)
        verification_status = "unknown"
        tool_calls = response_metadata.get('tool_calls', [])
        if tool_calls:
            for tool_call in tool_calls:
                if hasattr(tool_call, 'function') and tool_call.function.name == "verify_statistical_analysis":
                    try:
                        args = json.loads(tool_call.function.arguments)
                        verification_status = "verified" if args.get("verified", False) else "verification_error"
                    except (json.JSONDecodeError, Exception):
                        verification_status = "verification_error"
        
        verification_result = {
            "batch_id": batch_id,
            "step": "verification",
            "model_used": "vertex_ai/gemini-2.5-flash-lite",
            "verification_status": verification_status,
            "cost_info": verification_cost_info,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        verification_hash = self.storage.put_artifact(
            json.dumps(verification_result, indent=2).encode('utf-8'),
            {"artifact_type": "statistical_verification", "batch_id": batch_id}
        )
        
        verification_result['artifact_hash'] = verification_hash
        
        self.audit.log_agent_event(self.agent_name, "step2_completed", {
            "batch_id": batch_id,
            "step": "verification",
            "verification_status": verification_status,
            "artifact_hash": verification_hash,
            "cost_info": verification_cost_info
        })
        
        return verification_result

    # CSV generation removed - now handled by AnalysisAgent

    def _discover_analysis_artifacts(self, batch_id: str, specific_hashes: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Discover analysis artifacts from shared cache for the given batch.
        
        Args:
            batch_id: Batch identifier for logging
            specific_hashes: If provided, load only these specific artifact hashes.
                           If None, falls back to loading from current analysis session.
        
        Returns:
            Dictionary of artifact_hash -> artifact_data
        """
        artifacts = {}
        
        if specific_hashes:
            # THIN approach: Load only the specific artifacts requested by orchestrator
            self.logger.info(f"Loading {len(specific_hashes)} specific artifacts for batch {batch_id}")
            
            for artifact_hash in specific_hashes:
                try:
                    artifact_content = self.storage.get_artifact(artifact_hash)
                    artifact_data = json.loads(artifact_content.decode('utf-8'))
                    artifacts[artifact_hash] = artifact_data
                except Exception as e:
                    self.logger.warning(f"Could not load specific artifact {artifact_hash}: {e}")
                    continue
            
            self.logger.info(f"Successfully loaded {len(artifacts)} specific artifacts")
            return artifacts
        
        # Fallback: Load from current analysis session (legacy behavior)
        # Guard: Only attempt fallback if storage registry is properly initialized
        if not hasattr(self.storage, 'registry') or not self.storage.registry:
            self.logger.error("Storage registry not initialized. Cannot discover artifacts.")
            return {}
            
        self.logger.warning("No specific artifacts provided, falling back to current session discovery")
        
        analysis_sessions = {}
        for artifact_hash, artifact_info in self.storage.registry.items():
            metadata = artifact_info.get("metadata", {})
            artifact_type = metadata.get("artifact_type", "")
            analysis_id = metadata.get("analysis_id", "")
            
            if artifact_type in ["composite_analysis", "score_extraction", "derived_metrics", "evidence_extraction"] and analysis_id:
                if analysis_id not in analysis_sessions:
                    analysis_sessions[analysis_id] = []
                analysis_sessions[analysis_id].append((artifact_hash, artifact_info))
        
        if not analysis_sessions:
            self.logger.warning(f"No analysis artifacts found for batch {batch_id}")
            return artifacts
        
        # Use the most recent analysis session
        most_recent_analysis_id = max(analysis_sessions.keys())
        self.logger.info(f"Using most recent analysis session: {most_recent_analysis_id}")
        
        for artifact_hash, artifact_info in analysis_sessions[most_recent_analysis_id]:
            try:
                artifact_content = self.storage.get_artifact(artifact_hash)
                artifact_data = json.loads(artifact_content.decode('utf-8'))
                artifacts[artifact_hash] = artifact_data
            except Exception as e:
                self.logger.warning(f"Could not load artifact {artifact_hash}: {e}")
                continue
        
        self.logger.info(f"Successfully loaded {len(artifacts)} artifacts from analysis session {most_recent_analysis_id}")
        return artifacts

    def _prepare_statistical_prompt(self, framework_content: str, experiment_content: str, corpus_manifest: str, artifacts: Dict[str, Any]) -> str:
        """
        Prepare the statistical analysis prompt with framework and artifacts.
        
        Args:
            framework_content: The framework content
            experiment_content: The experiment content
            corpus_manifest: The corpus manifest content
            artifacts: Dictionary of artifact_hash -> artifact_data
            
        Returns:
            Formatted prompt for statistical analysis
        """
        prompt = f"""Perform comprehensive statistical analysis on the provided analysis artifacts.

FRAMEWORK:
{framework_content}

EXPERIMENT:
{experiment_content}

CORPUS MANIFEST:
{corpus_manifest}

ANALYSIS ARTIFACTS:
"""
        
        for artifact_hash, artifact_data in artifacts.items():
            prompt += f"\n--- ARTIFACT {artifact_hash} ---\n"
            prompt += json.dumps(artifact_data, indent=2)
            prompt += "\n\n"
        
        return prompt

    def _calculate_total_costs(self, statistical_result: Dict[str, Any], 
                             verification_result: Dict[str, Any], 
                             csv_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate total costs and performance metrics across all steps.
        
        Args:
            statistical_result: Results from step 1
            verification_result: Results from step 2  
            csv_result: Results from step 3
            
        Returns:
            Dictionary with aggregated cost and performance information
        """
        
        # Extract cost info from each step
        stat_cost = statistical_result.get("cost_info", {})
        verify_cost = verification_result.get("cost_info", {})
        csv_cost = csv_result.get("cost_info", {})
        
        # Calculate totals
        total_cost = (
            stat_cost.get("response_cost", 0.0) +
            verify_cost.get("response_cost", 0.0) +
            csv_cost.get("response_cost", 0.0)
        )
        
        total_execution_time = (
            stat_cost.get("execution_time_seconds", 0.0) +
            verify_cost.get("execution_time_seconds", 0.0) +
            csv_cost.get("execution_time_seconds", 0.0)
        )
        
        total_tokens = (
            stat_cost.get("total_tokens", 0) +
            verify_cost.get("total_tokens", 0) +
            csv_cost.get("total_tokens", 0)
        )
        
        return {
            "total_cost_usd": total_cost,
            "total_execution_time_seconds": total_execution_time,
            "total_tokens": total_tokens,
            "cost_breakdown": {
                "statistical_execution": stat_cost.get("response_cost", 0.0),
                "verification": verify_cost.get("response_cost", 0.0),
                "csv_generation": csv_cost.get("response_cost", 0.0)
            },
            "performance_breakdown": {
                "statistical_execution_time": stat_cost.get("execution_time_seconds", 0.0),
                "verification_time": verify_cost.get("execution_time_seconds", 0.0),
                "csv_generation_time": csv_cost.get("execution_time_seconds", 0.0)
            },
            "models_used": [
                stat_cost.get("model", "unknown"),
                verify_cost.get("model", "unknown"),
                csv_cost.get("model", "unknown")
            ]
        }

    def check_cache(self, batch_id: str) -> Optional[Dict[str, Any]]:
        """
        Check if statistical analysis results are already cached.
        
        Args:
            batch_id: Batch identifier for cache lookup
            
        Returns:
            Cached results if available, None otherwise
        """
        
        # Search through artifact registry for matching statistical analysis
        for artifact_hash, artifact_info in self.storage.registry.items():
            metadata = artifact_info.get("metadata", {})
            
            if (metadata.get("artifact_type") == "statistical_analysis" and
                metadata.get("batch_id") == batch_id):
                
                self.logger.info(f"💾 Cache hit for statistical analysis: {batch_id}")
                
                try:
                    cached_content = self.storage.get_artifact(artifact_hash)
                    cached_result = json.loads(cached_content.decode('utf-8'))
                    
                    self.audit.log_agent_event(self.agent_name, "cache_hit", {
                        "batch_id": batch_id,
                        "cached_artifact_hash": artifact_hash
                    })
                    
                    # Add cached flag to indicate this result came from cache
                    cached_result["cached"] = True
                    return cached_result
                    
                except Exception as e:
                    self.logger.warning(f"⚠️ Cache hit but failed to load content: {e}")
                    continue
        
        # No cache hit
        self.logger.info(f"🔍 No cache hit for {batch_id} - will perform analysis...")
        return None

    def store_cache(self, batch_id: str, result: Dict[str, Any]) -> str:
        """
        Store statistical analysis results in cache.
        
        Args:
            batch_id: Batch identifier
            result: Analysis results to cache
            
        Returns:
            Artifact hash of cached result
        """
        
        cache_metadata = {
            "artifact_type": "statistical_analysis_cache",
            "batch_id": batch_id,
            "cached_at": datetime.now(timezone.utc).isoformat(),
            "agent_name": self.agent_name
        }
        
        cache_hash = self.storage.put_artifact(
            json.dumps(result, indent=2).encode('utf-8'),
            cache_metadata
        )
        
        self.audit.log_agent_event(self.agent_name, "cache_store", {
            "batch_id": batch_id,
            "cache_artifact_hash": cache_hash
        })
        
        return cache_hash
