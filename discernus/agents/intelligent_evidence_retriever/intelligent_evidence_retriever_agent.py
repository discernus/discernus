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
        
        # Load externalized prompts
        self.planning_prompt = self._load_prompt_template("planning_prompt.yaml")
        self.curation_prompt = self._load_prompt_template("curation_prompt.yaml")
        self.cached_curation_prompt = self._load_prompt_template("cached_curation_prompt.yaml")
        
        self.logger.info(f"Initialized {self.agent_name} with externalized prompts")

    def _load_prompt_template(self, filename: str) -> str:
        """Load a prompt template from the YAML file."""
        try:
            from pathlib import Path
            import yaml
            
            prompt_path = Path(__file__).parent / filename
            if not prompt_path.exists():
                self.logger.error(f"Prompt template not found: {prompt_path}")
                return f"ERROR: Prompt template {filename} not found"
            
            with open(prompt_path, 'r', encoding='utf-8') as f:
                prompt_data = yaml.safe_load(f)
            
            if not isinstance(prompt_data, dict) or 'template' not in prompt_data:
                self.logger.error(f"Invalid prompt template format in {filename}")
                return f"ERROR: Invalid prompt template format in {filename}"
            
            return prompt_data['template']
            
        except Exception as e:
            self.logger.error(f"Failed to load prompt template {filename}: {e}")
            return f"ERROR: Failed to load prompt template {filename}: {str(e)}"

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
            self.log_execution_start(**kwargs)

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
            
            # Dynamic Model Selection (respects Gemini Pro's strategic recommendation)
            execution_model = self.select_execution_model(evidence_count, evidence_size_mb, curation_plan)
            self.logger.info(f"Selected execution model: {execution_model}")
            
            # Validate plan-model consistency
            plan_model = curation_plan.get('execution_model', 'unknown')
            expected_model = "gemini-2.5-flash" if plan_model == 'flash' else "gemini-2.5-pro" if plan_model == 'pro' else 'unknown'
            if expected_model != 'unknown' and execution_model != expected_model:
                self.logger.warning(f"Model selection mismatch: plan recommends {plan_model}, selected {execution_model}")
            else:
                self.logger.info(f"Model selection consistent with strategic plan: {plan_model} → {execution_model}")
            
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
        CAS-native discovery and counting of evidence extraction artifacts.
        THIN: No parsing, just count and size estimation.
        
        Args:
            run_context: The RunContext (not used for CAS discovery)
            
        Returns:
            Tuple of (evidence_count, estimated_size_mb)
        """
        # CAS discovery: Find evidence_extraction artifacts
        evidence_artifacts = self.storage.find_artifacts_by_metadata(
            artifact_type="evidence_extraction"
        )
        
        if not evidence_artifacts:
            self.logger.warning("No evidence_extraction artifacts found via CAS discovery")
            return 0, 0.0
        
        # Calculate total size
        total_size = 0
        for artifact_hash in evidence_artifacts:
            try:
                artifact_bytes = self.storage.get_artifact(artifact_hash)
                if artifact_bytes:
                    total_size += len(artifact_bytes)
                    self.logger.debug(f"Evidence artifact {artifact_hash}: {len(artifact_bytes)} bytes")
            except Exception as e:
                self.logger.warning(f"Could not get size for artifact {artifact_hash}: {e}")
                # Fallback to estimated size
                total_size += 1200  # ~1.2KB based on observations
        
        evidence_count = len(evidence_artifacts)
        evidence_size_mb = total_size / (1024 * 1024)  # Convert to MB
        
        self.logger.info(f"CAS Evidence inventory: {evidence_count} artifacts, {total_size} bytes ({evidence_size_mb:.2f} MB)")
        
        # Store evidence artifact hashes for later use
        self._evidence_artifact_hashes = evidence_artifacts
        
        return evidence_count, evidence_size_mb

    # REMOVED: is_evidence_artifact() - CAS discovery eliminates need for parsing-based identification

    def get_evidence_artifact_details(self, run_context: RunContext) -> List[Dict[str, Any]]:
        """
        Get structured evidence artifact details for orchestration logic.
        NOTE: This returns structured data for software coordination, not LLM processing.
        
        Args:
            run_context: The RunContext (not used for CAS discovery)
            
        Returns:
            List of evidence artifact details for orchestration
        """
        evidence_details = []
        
        if not hasattr(self, '_evidence_artifact_hashes'):
            # If inventory hasn't been run, run it now
            self.count_evidence_artifacts(run_context)
        
        for artifact_hash in self._evidence_artifact_hashes:
            try:
                artifact_bytes = self.storage.get_artifact(artifact_hash)
                if artifact_bytes:
                    # Parse for orchestration logic (not LLM processing)
                    artifact_data = json.loads(artifact_bytes.decode('utf-8'))
                    
                    # Extract key information for planning
                    details = {
                        "hash": artifact_hash,
                        "size_bytes": len(artifact_bytes),
                        "document_index": artifact_data.get("document_index"),
                        "model_used": artifact_data.get("model_used"),
                        "timestamp": artifact_data.get("timestamp"),
                        "analysis_id": artifact_data.get("analysis_id"),
                        "quote_count": 0  # Simplified - let LLM count quotes during processing
                    }
                    
                    evidence_details.append(details)
                    
            except Exception as e:
                self.logger.warning(f"Could not get details for evidence artifact {artifact_hash}: {e}")
        
        self.logger.info(f"Evidence details: {len(evidence_details)} artifacts for orchestration")
        return evidence_details

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
                        "description": "Overall curation strategy: single_pass for small corpora, multi_iteration for large"
                    },
                    "rationale": {
                        "type": "string",
                        "description": "Strategic reasoning for the chosen approach and iteration design"
                    },
                    "iterations": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "iteration_name": {"type": "string", "description": "Descriptive name for this iteration"},
                                "focus_area": {"type": "string", "description": "Primary statistical focus for this iteration"},
                                "statistical_targets": {
                                    "type": "array", 
                                    "items": {"type": "string"},
                                    "description": "Specific statistical findings to find evidence for"
                                },
                                "evidence_subset": {
                                    "type": "string", 
                                    "enum": ["all_evidence", "high_scoring_docs", "outlier_docs", "specific_documents"],
                                    "description": "Which evidence artifacts to process in this iteration"
                                },
                                "curation_instructions": {
                                    "type": "string",
                                    "description": "Detailed instructions for evidence selection in this iteration"
                                },
                                "expected_quotes": {
                                    "type": "integer", 
                                    "minimum": 10,
                                    "maximum": 200,
                                    "description": "Expected number of high-quality quotes to curate"
                                },
                                "priority": {
                                    "type": "string",
                                    "enum": ["high", "medium", "low"],
                                    "description": "Priority level for this iteration"
                                }
                            },
                            "required": ["iteration_name", "focus_area", "statistical_targets", "evidence_subset", "curation_instructions", "expected_quotes", "priority"]
                        }
                    },
                    "execution_model": {
                        "type": "string", 
                        "enum": ["flash", "pro"],
                        "description": "Recommended model: flash for ≤400 docs, pro for >400 docs"
                    },
                    "estimated_total_quotes": {
                        "type": "integer",
                        "minimum": 20,
                        "maximum": 1000,
                        "description": "Total quotes expected across all iterations"
                    },
                    "cost_estimate": {
                        "type": "string",
                        "enum": ["low", "medium", "high"],
                        "description": "Expected cost level for this curation plan"
                    }
                },
                "required": ["strategy", "rationale", "iterations", "execution_model", "estimated_total_quotes", "cost_estimate"]
            }
        }
        
        # Get evidence details for better planning
        evidence_details = self.get_evidence_artifact_details(run_context)
        total_quotes = sum(d['quote_count'] for d in evidence_details)
        
        # Create comprehensive planning prompt using external template
        planning_prompt = self.planning_prompt.format(
            framework_name=run_context.metadata.get('framework_name', 'Unknown Framework'),
            corpus_size=len(run_context.metadata.get('corpus_documents', [])),
            evidence_count=evidence_count,
            evidence_size_mb=f"{evidence_size_mb:.3f}",
            total_quotes=total_quotes,
            statistical_results=json.dumps(run_context.statistical_results, indent=2, default=str)[:3000],
            evidence_inventory=json.dumps([{
                'document_index': d['document_index'],
                'quote_count': d['quote_count'],
                'size_bytes': d['size_bytes']
            } for d in evidence_details], indent=2)
        )

        try:
            # Let Gemini Pro do all the strategic thinking - no fallback
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
                if hasattr(tool_call, 'function') and tool_call.function.name == 'generate_curation_plan':
                    plan = json.loads(tool_call.function.arguments)
                    self.logger.info(f"Gemini Pro strategic plan: {plan['strategy']} with {len(plan['iterations'])} iterations")
                    return plan
            
            # If Gemini Pro fails to plan, that's a real error
            raise RuntimeError("Gemini Pro failed to generate strategic curation plan")
            
        except Exception as e:
            self.logger.error(f"Strategic planning failed: {e}")
            raise  # Don't mask LLM failures with fallbacks


    def select_execution_model(self, evidence_count: int, evidence_size_mb: float, 
                             curation_plan: Optional[Dict[str, Any]] = None) -> str:
        """
        Select optimal execution model based on evidence volume and curation strategy.
        
        Args:
            evidence_count: Number of evidence artifacts
            evidence_size_mb: Total evidence size in MB
            curation_plan: Optional curation plan from Gemini Pro strategic planning
            
        Returns:
            Model name ("gemini-2.5-flash" or "gemini-2.5-pro")
        """
        # If we have a strategic plan from Gemini Pro, respect its recommendation
        if curation_plan and 'execution_model' in curation_plan:
            recommended_model = curation_plan['execution_model']
            if recommended_model == 'flash':
                selected_model = "gemini-2.5-flash"
            elif recommended_model == 'pro':
                selected_model = "gemini-2.5-pro"
            else:
                # Fallback to size-based selection if plan has invalid model
                selected_model = self._select_model_by_size(evidence_count, evidence_size_mb)
            
            self.logger.info(f"Using Gemini Pro recommended model: {selected_model}")
            return selected_model
        
        # Default size-based selection when no plan available
        return self._select_model_by_size(evidence_count, evidence_size_mb)
    
    def _select_model_by_size(self, evidence_count: int, evidence_size_mb: float) -> str:
        """Size-based model selection fallback."""
        if evidence_count <= self.FLASH_HIGH_CONFIDENCE_THRESHOLD and evidence_size_mb <= self.FLASH_SIZE_LIMIT:
            self.logger.info(f"Selected Flash for small corpus: {evidence_count} docs, {evidence_size_mb:.2f}MB")
            return "gemini-2.5-flash"
        else:
            self.logger.info(f"Selected Pro for large corpus: {evidence_count} docs, {evidence_size_mb:.2f}MB")
            return "gemini-2.5-pro"

    def create_cached_session(self, run_context: RunContext) -> Dict[str, Any]:
        """
        Create cached session for Pro model with ALL evidence loaded.
        
        Args:
            run_context: The RunContext containing evidence artifacts
            
        Returns:
            Session context with all evidence loaded
        """
        self.logger.info("Creating cached session with ALL evidence artifacts...")
        
        # Get all evidence artifacts
        if not hasattr(self, '_evidence_artifact_hashes'):
            self.count_evidence_artifacts(run_context)
        
        # Load all evidence content into session context
        session_evidence = []
        total_evidence_chars = 0
        
        for artifact_hash in self._evidence_artifact_hashes:
            try:
                artifact_bytes = self.storage.get_artifact(artifact_hash)
                if artifact_bytes:
                    artifact_data = json.loads(artifact_bytes.decode('utf-8'))
                    
                    evidence_entry = {
                        "document_index": artifact_data.get("document_index"),
                        "evidence_content": artifact_data.get("evidence_extraction", ""),
                        "artifact_hash": artifact_hash,
                        "analysis_metadata": {
                            "model_used": artifact_data.get("model_used"),
                            "timestamp": artifact_data.get("timestamp"),
                            "analysis_id": artifact_data.get("analysis_id")
                        }
                    }
                    
                    session_evidence.append(evidence_entry)
                    total_evidence_chars += len(evidence_entry["evidence_content"])
                    
            except Exception as e:
                self.logger.warning(f"Could not load evidence artifact {artifact_hash}: {e}")
        
        # Create session context
        session_context = {
            "evidence_artifacts": session_evidence,
            "total_evidence_count": len(session_evidence),
            "total_evidence_chars": total_evidence_chars,
            "statistical_context": run_context.statistical_results,
            "experiment_metadata": {
                "experiment_id": run_context.experiment_id,
                "framework_path": str(run_context.framework_path),
                "corpus_path": str(run_context.corpus_path)
            },
            "session_created": datetime.now(timezone.utc).isoformat()
        }
        
        self.logger.info(f"Created cached session: {len(session_evidence)} evidence artifacts, {total_evidence_chars:,} total characters")
        
        return session_context

    def execute_iteration_with_cache(self, cache_session: Dict[str, Any], iteration: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute curation iteration using cached session with ALL evidence.
        
        Args:
            cache_session: Cached session context with all evidence loaded
            iteration: Iteration configuration from strategic plan
            
        Returns:
            Curated evidence results
        """
        self.logger.info(f"Executing cached iteration: {iteration.get('iteration_name', iteration['focus_area'])}")
        
        # Create comprehensive prompt with ALL evidence in context
        cached_prompt = self._create_cached_curation_prompt(cache_session, iteration)
        
        try:
            # Execute Pro curation with full evidence context
            response, metadata = self.llm_gateway.execute_call(
                model="vertex_ai/gemini-2.5-pro",
                prompt=cached_prompt,
                temperature=0.1
            )
            
            # Store raw LLM curation response (THIN: no parsing)
            evidence_count = cache_session["total_evidence_count"]
            evidence_chars = cache_session["total_evidence_chars"]
            
            self.logger.info(f"Cached iteration completed: raw curation response from {evidence_count} artifacts ({evidence_chars:,} chars)")
            
            return {
                "raw_curation_response": response,
                "focus_area": iteration['focus_area'],
                "iteration_name": iteration.get('iteration_name', iteration['focus_area']),
                "evidence_processed": evidence_count,
                "evidence_chars_processed": evidence_chars,
                "model_used": "gemini-2.5-pro",
                "execution_method": "cached_session",
                "statistical_targets": iteration.get('statistical_targets', []),
                "curation_instructions": iteration.get('curation_instructions', ''),
                "priority": iteration.get('priority', 'medium')
            }
            
        except Exception as e:
            self.logger.error(f"Cached iteration failed: {e}")
            return {"raw_curation_response": "", "focus_area": iteration['focus_area'], "error": str(e)}

    def execute_iteration_direct(self, run_context: RunContext, iteration: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute curation iteration with direct model calls.
        
        Args:
            run_context: The RunContext containing evidence artifacts
            iteration: Iteration configuration
            
        Returns:
            Curated evidence results
        """
        self.logger.info(f"Executing direct iteration: {iteration.get('iteration_name', iteration['focus_area'])}")
        
        # Get evidence artifacts for this iteration
        evidence_artifacts = self._get_evidence_for_iteration(run_context, iteration)
        
        if not evidence_artifacts:
            self.logger.warning(f"No evidence artifacts found for iteration: {iteration['focus_area']}")
            return {"raw_curation_response": "", "focus_area": iteration['focus_area'], "evidence_processed": 0}
        
        # Create curation prompt for this iteration
        curation_prompt = self._create_curation_prompt(run_context, iteration, evidence_artifacts)
        
        try:
            # Execute Flash curation
            response, metadata = self.llm_gateway.execute_call(
                model="vertex_ai/gemini-2.5-flash",
                prompt=curation_prompt,
                temperature=0.1
            )
            
            # Store raw LLM curation response (THIN: no parsing)
            self.logger.info(f"Direct iteration completed: raw curation response from {len(evidence_artifacts)} artifacts")
            
            return {
                "raw_curation_response": response,
                "focus_area": iteration['focus_area'],
                "iteration_name": iteration.get('iteration_name', iteration['focus_area']),
                "evidence_processed": len(evidence_artifacts),
                "model_used": "gemini-2.5-flash",
                "statistical_targets": iteration.get('statistical_targets', []),
                "curation_instructions": iteration.get('curation_instructions', ''),
                "priority": iteration.get('priority', 'medium')
            }
            
        except Exception as e:
            self.logger.error(f"Direct iteration failed: {e}")
            return {"raw_curation_response": "", "focus_area": iteration['focus_area'], "error": str(e)}

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
        
        return self.storage.store_artifact(
            content=artifact_data,
            artifact_type="curated_evidence",
            experiment_id=focus_area
        )

    def _get_evidence_for_iteration(self, run_context: RunContext, iteration: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Get evidence artifacts relevant to this iteration.
        
        Args:
            run_context: The RunContext containing evidence artifacts
            iteration: Iteration configuration
            
        Returns:
            List of evidence artifact data for processing
        """
        evidence_subset = iteration.get('evidence_subset', 'all_evidence')
        evidence_artifacts = []
        
        # Get all evidence artifacts first
        if not hasattr(self, '_evidence_artifact_hashes'):
            self.count_evidence_artifacts(run_context)
        
        for artifact_hash in self._evidence_artifact_hashes:
            try:
                artifact_bytes = self.storage.get_artifact(artifact_hash)
                if artifact_bytes:
                    artifact_data = json.loads(artifact_bytes.decode('utf-8'))
                    
                    # Apply evidence subset filtering
                    if self._should_include_evidence(artifact_data, evidence_subset, run_context):
                        evidence_artifacts.append({
                            "hash": artifact_hash,
                            "data": artifact_data,
                            "document_index": artifact_data.get("document_index"),
                            "evidence_content": artifact_data.get("evidence_extraction", "")
                        })
                        
            except Exception as e:
                self.logger.warning(f"Could not load evidence artifact {artifact_hash}: {e}")
        
        self.logger.info(f"Selected {len(evidence_artifacts)} evidence artifacts for iteration (subset: {evidence_subset})")
        return evidence_artifacts

    def _should_include_evidence(self, artifact_data: Dict[str, Any], evidence_subset: str, run_context: RunContext) -> bool:
        """Determine if evidence artifact should be included in this iteration."""
        if evidence_subset == 'all_evidence':
            return True
        elif evidence_subset == 'high_scoring_docs':
            # TODO: Implement high-scoring document filtering based on statistical results
            return True  # For now, include all
        elif evidence_subset == 'outlier_docs':
            # TODO: Implement outlier document filtering based on statistical results
            return True  # For now, include all
        elif evidence_subset == 'specific_documents':
            # TODO: Implement specific document filtering based on iteration config
            return True  # For now, include all
        else:
            return True

    def _create_curation_prompt(self, run_context: RunContext, iteration: Dict[str, Any], 
                              evidence_artifacts: List[Dict[str, Any]]) -> str:
        """
        Create curation prompt for this iteration.
        
        Args:
            run_context: The RunContext containing experiment data
            iteration: Iteration configuration
            evidence_artifacts: Evidence artifacts to process
            
        Returns:
            Formatted curation prompt
        """
        # Get statistical context
        statistical_context = json.dumps(run_context.statistical_results, indent=2, default=str)[:2000]
        
        # Prepare evidence content
        evidence_content = ""
        for i, artifact in enumerate(evidence_artifacts[:10]):  # Limit to 10 artifacts for token management
            doc_index = artifact.get('document_index', i)
            evidence_text = artifact.get('evidence_content', '')
            evidence_content += f"\n--- DOCUMENT {doc_index} EVIDENCE ---\n{evidence_text}\n"
        
        if len(evidence_artifacts) > 10:
            evidence_content += f"\n[... and {len(evidence_artifacts) - 10} more documents ...]"
        
        # Create comprehensive curation prompt using external template
        prompt = self.curation_prompt.format(
            focus_area=iteration['focus_area'],
            curation_instructions=iteration.get('curation_instructions', 'Select the most compelling quotes that support the statistical findings.'),
            statistical_targets=json.dumps(iteration.get('statistical_targets', []), indent=2),
            statistical_context=statistical_context,
            evidence_content=evidence_content,
            expected_quotes=iteration.get('expected_quotes', 50)
        )
        
        return prompt


    def _create_cached_curation_prompt(self, cache_session: Dict[str, Any], iteration: Dict[str, Any]) -> str:
        """
        Create curation prompt with ALL evidence from cached session.
        
        Args:
            cache_session: Session context with all evidence loaded
            iteration: Iteration configuration from strategic plan
            
        Returns:
            Comprehensive prompt with full evidence context
        """
        # Get statistical context from session
        statistical_context = json.dumps(cache_session["statistical_context"], indent=2, default=str)[:3000]
        
        # Include ALL evidence artifacts (no arbitrary limits)
        evidence_content = ""
        evidence_artifacts = cache_session["evidence_artifacts"]
        
        for evidence_entry in evidence_artifacts:
            doc_index = evidence_entry.get('document_index', 'unknown')
            evidence_text = evidence_entry.get('evidence_content', '')
            evidence_content += f"\n--- DOCUMENT {doc_index} EVIDENCE ---\n{evidence_text}\n"
        
        total_chars = cache_session["total_evidence_chars"]
        total_count = cache_session["total_evidence_count"]
        
        # Create comprehensive cached prompt using external template
        prompt = self.cached_curation_prompt.format(
            total_count=total_count,
            total_chars=f"{total_chars:,}",
            session_created=cache_session.get('session_created', 'unknown'),
            focus_area=iteration['focus_area'],
            iteration_name=iteration.get('iteration_name', 'unnamed'),
            curation_instructions=iteration.get('curation_instructions', 'Select the most compelling quotes that support the statistical findings.'),
            statistical_targets=json.dumps(iteration.get('statistical_targets', []), indent=2),
            statistical_context=statistical_context,
            evidence_content=evidence_content,
            expected_quotes=iteration.get('expected_quotes', 50),
            statistical_targets_list=', '.join(iteration.get('statistical_targets', []))
        )
        
        return prompt
