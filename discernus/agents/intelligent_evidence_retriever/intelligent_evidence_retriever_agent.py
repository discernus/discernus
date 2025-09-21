#!/usr/bin/env python3
"""
Intelligent Evidence Retrieval Agent
===================================

This agent replaces RAG-based evidence retrieval with intelligent atomic evidence
processing using strategic curation based on statistical findings.

Architecture:
- Step 0: Evidence Inventory (count artifacts without processing)
- Step 1: Strategic Curation Planning (Gemini Pro + tool calling)
- Steps 2-n: Iterative Evidence Curation (Flash/Pro with session caching)

THIN Principles:
- LLM intelligence for strategic planning and curation
- Software coordination for iteration and caching
- Deterministic handoffs via tool calling
- Direct atomic evidence processing (no RAG)
"""

import json
import logging
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional, Tuple

from discernus.core.security_boundary import ExperimentSecurityBoundary
from discernus.core.audit_logger import AuditLogger
from discernus.core.local_artifact_storage import LocalArtifactStorage
from discernus.core.agent_result import AgentResult
from discernus.core.run_context import RunContext
from discernus.core.standard_agent import StandardAgent
from discernus.gateway.llm_gateway_enhanced import EnhancedLLMGateway
from discernus.gateway.model_registry import get_model_registry


class IntelligentEvidenceRetrievalAgent(StandardAgent):
    """
    Intelligent Evidence Retrieval Agent with strategic curation.
    
    This agent processes atomic evidence artifacts and uses statistical findings
    to strategically curate the most relevant evidence quotes through intelligent
    iteration and dynamic model selection.
    """
    
    def __init__(self, 
                 security: ExperimentSecurityBoundary,
                 storage: LocalArtifactStorage,
                 audit: AuditLogger,
                 config: Optional[Dict[str, Any]] = None):
        """
        Initialize the Intelligent Evidence Retrieval Agent.
        
        Args:
            security: Security boundary for file operations
            storage: Content-addressable artifact storage
            audit: Audit logger for comprehensive event tracking
            config: Optional agent configuration
        """
        super().__init__(security, storage, audit, config)
        self.agent_name = "IntelligentEvidenceRetrievalAgent"
        self.logger = logging.getLogger(__name__)
        
        # Initialize Enhanced LLM Gateway for tool calling
        model_registry = get_model_registry()
        self.llm_gateway = EnhancedLLMGateway(model_registry)
        
        # Configuration constants
        self.FLASH_HIGH_CONFIDENCE_THRESHOLD = 400  # documents
        self.FLASH_SIZE_LIMIT = 3.0  # MB
        
        self.logger.info(f"Initialized {self.agent_name}")

    def get_capabilities(self) -> List[str]:
        """Return the capabilities of this intelligent evidence retrieval agent."""
        return [
            "intelligent_evidence_curation",
            "strategic_planning", 
            "atomic_evidence_processing",
            "statistical_mapping",
            "dynamic_model_selection",
            "session_caching",
            "tool_calling",
            "structured_output"
        ]

    def execute(self, run_context: RunContext, **kwargs) -> AgentResult:
        """
        Execute intelligent evidence retrieval using strategic curation.
        
        Args:
            run_context: The RunContext object containing all experiment data
            **kwargs: Additional execution parameters
            
        Returns:
            AgentResult with curated evidence mapped to statistical conclusions
        """
        try:
            self.logger.info("IntelligentEvidenceRetrievalAgent starting execution")
            self.log_execution_start(run_context=run_context, **kwargs)

            # Step 0: Evidence Inventory
            self.logger.info("Step 0: Counting evidence artifacts...")
            evidence_count, evidence_size_mb = self.count_evidence_artifacts(run_context)
            self.logger.info(f"Found {evidence_count} evidence artifacts (~{evidence_size_mb:.1f}MB)")
            
            if evidence_count == 0:
                self.logger.warning("No evidence artifacts found")
                return AgentResult(
                    success=False,
                    artifacts=[],
                    metadata={"agent_name": self.agent_name, "error": "No evidence artifacts found"},
                    error_message="No evidence artifacts found in analysis results"
                )

            # Step 1: Strategic Curation Planning
            self.logger.info("Step 1: Generating strategic curation plan...")
            curation_plan = self.generate_curation_plan(run_context, evidence_count, evidence_size_mb)
            self.logger.info(f"Generated plan: {curation_plan['strategy']} with {len(curation_plan['iterations'])} iterations")
            
            # Dynamic Model Selection
            execution_model = self.select_execution_model(evidence_count, evidence_size_mb)
            self.logger.info(f"Selected execution model: {execution_model}")
            
            # Steps 2-n: Iterative Evidence Curation
            curated_results = []
            cache_session = None
            
            for i, iteration in enumerate(curation_plan['iterations']):
                self.logger.info(f"Executing iteration {i+1}/{len(curation_plan['iterations'])}: {iteration['focus_area']}")
                
                if execution_model == "gemini-2.5-pro":
                    # Use session caching for Pro
                    if not cache_session:
                        cache_session = self.create_cached_session(run_context)
                    results = self.execute_iteration_with_cache(cache_session, iteration)
                else:
                    # Flash: direct processing
                    results = self.execute_iteration_direct(run_context, iteration)
                
                # Store curated results
                artifact_hash = self.store_curated_artifact(results, iteration['focus_area'])
                curated_results.append(artifact_hash)
                self.logger.info(f"Stored curated evidence artifact: {artifact_hash}")
            
            # Create final result
            result = AgentResult(
                success=True,
                artifacts=curated_results,
                metadata={
                    "agent_name": self.agent_name,
                    "evidence_count": evidence_count,
                    "evidence_size_mb": evidence_size_mb,
                    "execution_model": execution_model,
                    "iterations_completed": len(curated_results),
                    "curation_strategy": curation_plan['strategy']
                }
            )
            
            self.log_execution_complete(result)
            return result
            
        except Exception as e:
            self.logger.error(f"Intelligent evidence retrieval failed: {str(e)}")
            return AgentResult(
                success=False,
                artifacts=[],
                metadata={"agent_name": self.agent_name, "error": str(e)},
                error_message=str(e)
            )

    def count_evidence_artifacts(self, run_context: RunContext) -> Tuple[int, float]:
        """
        Count evidence artifacts and estimate total size without processing them.
        
        Args:
            run_context: The RunContext containing analysis artifacts
            
        Returns:
            Tuple of (evidence_count, estimated_size_mb)
        """
        evidence_artifacts = []
        total_size = 0
        
        for artifact_hash in run_context.analysis_artifacts:
            if self.is_evidence_artifact(artifact_hash):
                evidence_artifacts.append(artifact_hash)
                # Estimate size (will be more accurate after we implement size checking)
                total_size += 6000  # ~6KB per evidence artifact for clean extraction
        
        evidence_count = len(evidence_artifacts)
        evidence_size_mb = total_size / (1024 * 1024)  # Convert to MB
        
        return evidence_count, evidence_size_mb

    def is_evidence_artifact(self, artifact_hash: str) -> bool:
        """
        Check if an artifact is an evidence extraction artifact.
        
        Args:
            artifact_hash: Hash of the artifact to check
            
        Returns:
            True if this is an evidence artifact
        """
        try:
            artifact_bytes = self.storage.get_artifact(artifact_hash)
            if not artifact_bytes:
                return False
            
            artifact_data = json.loads(artifact_bytes.decode('utf-8'))
            return artifact_data.get("step") == "evidence_extraction"
            
        except Exception:
            return False

    def generate_curation_plan(self, run_context: RunContext, evidence_count: int, evidence_size_mb: float) -> Dict[str, Any]:
        """
        Generate strategic curation plan using Gemini Pro with tool calling.
        
        Args:
            run_context: The RunContext containing experiment data
            evidence_count: Number of evidence artifacts
            evidence_size_mb: Total size of evidence in MB
            
        Returns:
            Structured curation plan
        """
        # Define the curation planning tool
        curation_tool = {
            "name": "generate_curation_plan",
            "description": "Generate a strategic plan for evidence curation based on statistical findings and evidence volume",
            "parameters": {
                "type": "object",
                "properties": {
                    "strategy": {
                        "type": "string",
                        "enum": ["single_pass", "multi_iteration"],
                        "description": "Overall curation strategy based on evidence volume"
                    },
                    "iterations": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "focus_area": {"type": "string", "description": "Statistical focus for this iteration"},
                                "statistical_targets": {"type": "array", "items": {"type": "string"}},
                                "evidence_subset": {"type": "string", "description": "Which evidence to process"},
                                "expected_quotes": {"type": "integer", "description": "Expected number of quotes to find"}
                            },
                            "required": ["focus_area", "statistical_targets", "evidence_subset", "expected_quotes"]
                        }
                    },
                    "execution_model": {
                        "type": "string", 
                        "enum": ["flash", "pro"],
                        "description": "Recommended model for execution"
                    },
                    "estimated_total_quotes": {"type": "integer", "description": "Total quotes expected across all iterations"}
                },
                "required": ["strategy", "iterations", "execution_model", "estimated_total_quotes"]
            }
        }
        
        # Create planning prompt
        planning_prompt = f"""
You are planning evidence curation for a discourse analysis experiment.

EXPERIMENT CONTEXT:
- Framework: {run_context.metadata.get('framework_name', 'Unknown')}
- Corpus Size: {len(run_context.metadata.get('corpus_documents', []))} documents
- Evidence Artifacts: {evidence_count} (~{evidence_size_mb:.1f}MB)

STATISTICAL RESULTS SUMMARY:
{json.dumps(run_context.statistical_results, indent=2, default=str)[:2000]}...

TASK: Generate a strategic curation plan that:
1. Identifies key statistical findings that need evidence support
2. Plans iterations to focus on specific statistical patterns
3. Balances thoroughness with efficiency
4. Recommends appropriate execution model

Consider:
- Small corpus (≤400 docs): Single pass with Flash
- Large corpus (>400 docs): Multi-iteration with Pro
- Focus each iteration on specific statistical findings
- Aim for 50-200 high-quality quotes per iteration
"""

        try:
            # Execute tool call for planning
            response, metadata = self.llm_gateway.execute_call_with_tools(
                model="vertex_ai/gemini-2.5-pro",
                prompt=planning_prompt,
                tools=[curation_tool],
                tool_choice={"name": "generate_curation_plan"},
                temperature=0.1
            )
            
            # Parse tool call response
            if metadata.get('tool_calls'):
                tool_call = metadata['tool_calls'][0]
                if tool_call['name'] == 'generate_curation_plan':
                    return tool_call['arguments']
            
            # Fallback if tool calling fails
            self.logger.warning("Tool calling failed, using fallback planning")
            return self.create_fallback_plan(evidence_count, evidence_size_mb)
            
        except Exception as e:
            self.logger.error(f"Curation planning failed: {e}")
            return self.create_fallback_plan(evidence_count, evidence_size_mb)

    def create_fallback_plan(self, evidence_count: int, evidence_size_mb: float) -> Dict[str, Any]:
        """Create a simple fallback curation plan."""
        if evidence_count <= self.FLASH_HIGH_CONFIDENCE_THRESHOLD:
            return {
                "strategy": "single_pass",
                "iterations": [{
                    "focus_area": "comprehensive_evidence_curation",
                    "statistical_targets": ["all_significant_findings"],
                    "evidence_subset": "all_evidence",
                    "expected_quotes": 100
                }],
                "execution_model": "flash",
                "estimated_total_quotes": 100
            }
        else:
            return {
                "strategy": "multi_iteration", 
                "iterations": [
                    {
                        "focus_area": "primary_statistical_findings",
                        "statistical_targets": ["correlations", "significant_differences"],
                        "evidence_subset": "all_evidence",
                        "expected_quotes": 150
                    },
                    {
                        "focus_area": "secondary_patterns",
                        "statistical_targets": ["outliers", "trends"],
                        "evidence_subset": "all_evidence", 
                        "expected_quotes": 100
                    }
                ],
                "execution_model": "pro",
                "estimated_total_quotes": 250
            }

    def select_execution_model(self, evidence_count: int, evidence_size_mb: float) -> str:
        """
        Select optimal execution model based on evidence volume.
        
        Args:
            evidence_count: Number of evidence artifacts
            evidence_size_mb: Total evidence size in MB
            
        Returns:
            Model name ("gemini-2.5-flash" or "gemini-2.5-pro")
        """
        if evidence_count <= self.FLASH_HIGH_CONFIDENCE_THRESHOLD and evidence_size_mb <= self.FLASH_SIZE_LIMIT:
            return "gemini-2.5-flash"
        else:
            return "gemini-2.5-pro"

    def create_cached_session(self, run_context: RunContext) -> Any:
        """
        Create cached session for Pro model to avoid re-upload costs.
        
        Args:
            run_context: The RunContext containing evidence artifacts
            
        Returns:
            Cached session object
        """
        # TODO: Implement session caching when available
        self.logger.info("Session caching not yet implemented, using direct calls")
        return None

    def execute_iteration_with_cache(self, cache_session: Any, iteration: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute curation iteration using cached session.
        
        Args:
            cache_session: Cached session object
            iteration: Iteration configuration
            
        Returns:
            Curated evidence results
        """
        # TODO: Implement cached execution
        self.logger.info(f"Executing cached iteration: {iteration['focus_area']}")
        return {"quotes": [], "focus_area": iteration['focus_area']}

    def execute_iteration_direct(self, run_context: RunContext, iteration: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute curation iteration with direct model calls.
        
        Args:
            run_context: The RunContext containing evidence artifacts
            iteration: Iteration configuration
            
        Returns:
            Curated evidence results
        """
        # TODO: Implement direct execution
        self.logger.info(f"Executing direct iteration: {iteration['focus_area']}")
        return {"quotes": [], "focus_area": iteration['focus_area']}

    def store_curated_artifact(self, results: Dict[str, Any], focus_area: str) -> str:
        """
        Store curated evidence results as content-addressable artifact.
        
        Args:
            results: Curated evidence results
            focus_area: Focus area for this curation
            
        Returns:
            Artifact hash
        """
        artifact_data = {
            "agent_name": self.agent_name,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "focus_area": focus_area,
            "curated_evidence": results
        }
        
        artifact_bytes = json.dumps(artifact_data, indent=2).encode('utf-8')
        return self.storage.store_artifact(artifact_bytes)
