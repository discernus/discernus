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
                # Get actual size of artifact
                try:
                    artifact_bytes = self.storage.get_artifact(artifact_hash)
                    if artifact_bytes:
                        total_size += len(artifact_bytes)
                        self.logger.debug(f"Evidence artifact {artifact_hash}: {len(artifact_bytes)} bytes")
                except Exception as e:
                    self.logger.warning(f"Could not get size for artifact {artifact_hash}: {e}")
                    # Fallback to estimated size for clean evidence artifacts
                    total_size += 1200  # ~1.2KB based on nano experiment observations
        
        evidence_count = len(evidence_artifacts)
        evidence_size_mb = total_size / (1024 * 1024)  # Convert to MB
        
        self.logger.info(f"Evidence inventory: {evidence_count} artifacts, {total_size} bytes ({evidence_size_mb:.2f} MB)")
        
        # Store evidence artifact hashes for later use
        self._evidence_artifact_hashes = evidence_artifacts
        
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
            
            # Try to parse as JSON
            artifact_data = json.loads(artifact_bytes.decode('utf-8'))
            
            # Check if this is an evidence extraction step
            step = artifact_data.get("step")
            if step == "evidence_extraction":
                return True
            
            # Also check for evidence_extraction field (additional validation)
            if "evidence_extraction" in artifact_data:
                return True
                
            return False
            
        except (json.JSONDecodeError, UnicodeDecodeError, KeyError) as e:
            self.logger.debug(f"Could not parse artifact {artifact_hash} as evidence: {e}")
            return False
        except Exception as e:
            self.logger.warning(f"Unexpected error checking artifact {artifact_hash}: {e}")
            return False

    def get_evidence_artifact_details(self, run_context: RunContext) -> List[Dict[str, Any]]:
        """
        Get detailed information about evidence artifacts for planning purposes.
        
        Args:
            run_context: The RunContext containing analysis artifacts
            
        Returns:
            List of evidence artifact details
        """
        evidence_details = []
        
        if not hasattr(self, '_evidence_artifact_hashes'):
            # If inventory hasn't been run, run it now
            self.count_evidence_artifacts(run_context)
        
        for artifact_hash in self._evidence_artifact_hashes:
            try:
                artifact_bytes = self.storage.get_artifact(artifact_hash)
                if artifact_bytes:
                    artifact_data = json.loads(artifact_bytes.decode('utf-8'))
                    
                    # Extract key information for planning
                    details = {
                        "hash": artifact_hash,
                        "size_bytes": len(artifact_bytes),
                        "document_index": artifact_data.get("document_index"),
                        "model_used": artifact_data.get("model_used"),
                        "timestamp": artifact_data.get("timestamp"),
                        "analysis_id": artifact_data.get("analysis_id")
                    }
                    
                    # Count quotes in evidence extraction
                    evidence_content = artifact_data.get("evidence_extraction", "")
                    quote_count = 0
                    if "```json" in evidence_content:
                        try:
                            # Extract JSON from markdown code block
                            json_start = evidence_content.find("```json") + 7
                            json_end = evidence_content.find("```", json_start)
                            if json_end > json_start:
                                quotes_json = evidence_content[json_start:json_end].strip()
                                quotes = json.loads(quotes_json)
                                quote_count = len(quotes) if isinstance(quotes, list) else 0
                        except (json.JSONDecodeError, ValueError):
                            self.logger.debug(f"Could not parse quotes from artifact {artifact_hash}")
                    
                    details["quote_count"] = quote_count
                    evidence_details.append(details)
                    
            except Exception as e:
                self.logger.warning(f"Could not get details for evidence artifact {artifact_hash}: {e}")
        
        self.logger.info(f"Evidence details: {len(evidence_details)} artifacts with {sum(d['quote_count'] for d in evidence_details)} total quotes")
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
        
        # Create comprehensive planning prompt
        planning_prompt = f"""
You are an expert evidence curation strategist for discourse analysis experiments.

EXPERIMENT CONTEXT:
- Framework: {run_context.metadata.get('framework_name', 'Unknown Framework')}
- Corpus Size: {len(run_context.metadata.get('corpus_documents', []))} documents
- Evidence Artifacts: {evidence_count} artifacts (~{evidence_size_mb:.3f}MB)
- Total Available Quotes: {total_quotes}

STATISTICAL RESULTS ANALYSIS:
{json.dumps(run_context.statistical_results, indent=2, default=str)[:3000]}

EVIDENCE INVENTORY:
{json.dumps([{{
    'document_index': d['document_index'],
    'quote_count': d['quote_count'],
    'size_bytes': d['size_bytes']
}} for d in evidence_details], indent=2)}

STRATEGIC PLANNING TASK:
Generate an intelligent curation plan that maximizes evidence quality while optimizing cost and processing time.

PLANNING GUIDELINES:
1. SMALL CORPUS (≤400 docs, ≤3MB): Single comprehensive pass with Flash
2. LARGE CORPUS (>400 docs, >3MB): Multi-iteration strategy with Pro + caching
3. Focus iterations on distinct statistical patterns (correlations, outliers, trends)
4. Target 50-200 high-quality quotes per iteration
5. Ensure complete coverage of significant statistical findings
6. Consider cross-document pattern analysis for complex findings

STATISTICAL FOCUS AREAS TO CONSIDER:
- Strong correlations and anti-correlations
- Significant differences between groups/conditions
- Outlier documents with extreme scores
- Temporal or sequential patterns
- Interaction effects between dimensions
- Derived metrics validation needs

Generate a plan that balances thoroughness with efficiency.
"""

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
                if tool_call['name'] == 'generate_curation_plan':
                    plan = tool_call['arguments']
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
        self.logger.info(f"Executing direct iteration: {iteration.get('iteration_name', iteration['focus_area'])}")
        
        # Get evidence artifacts for this iteration
        evidence_artifacts = self._get_evidence_for_iteration(run_context, iteration)
        
        if not evidence_artifacts:
            self.logger.warning(f"No evidence artifacts found for iteration: {iteration['focus_area']}")
            return {"quotes": [], "focus_area": iteration['focus_area'], "evidence_processed": 0}
        
        # Create curation prompt for this iteration
        curation_prompt = self._create_curation_prompt(run_context, iteration, evidence_artifacts)
        
        try:
            # Execute Flash curation
            response, metadata = self.llm_gateway.execute_call(
                model="vertex_ai/gemini-2.5-flash",
                prompt=curation_prompt,
                temperature=0.1
            )
            
            # Parse curated quotes from response
            curated_quotes = self._parse_curated_quotes(response, iteration)
            
            self.logger.info(f"Direct iteration completed: {len(curated_quotes)} quotes curated from {len(evidence_artifacts)} artifacts")
            
            return {
                "quotes": curated_quotes,
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
            return {"quotes": [], "focus_area": iteration['focus_area'], "error": str(e)}

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
        
        # Create comprehensive curation prompt
        prompt = f"""
You are an expert evidence curator for discourse analysis research.

ITERATION FOCUS: {iteration['focus_area']}
CURATION INSTRUCTIONS: {iteration.get('curation_instructions', 'Select the most compelling quotes that support the statistical findings.')}

STATISTICAL TARGETS FOR THIS ITERATION:
{json.dumps(iteration.get('statistical_targets', []), indent=2)}

STATISTICAL CONTEXT:
{statistical_context}

EVIDENCE TO CURATE:
{evidence_content}

TASK: Select the {iteration.get('expected_quotes', 50)} most compelling quotes that:
1. Directly support the statistical findings for this iteration's focus area
2. Are clear, specific, and representative examples
3. Demonstrate the patterns identified in the statistical analysis
4. Provide strong evidence for the research conclusions

OUTPUT FORMAT:
For each selected quote, provide:
- Document index
- Exact quote text
- Statistical relevance (which finding it supports)
- Strength rating (1-5, where 5 is strongest evidence)

Focus on quality over quantity. Select quotes that would convince a skeptical peer reviewer.
"""
        
        return prompt

    def _parse_curated_quotes(self, response: str, iteration: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Parse curated quotes from LLM response.
        
        Args:
            response: LLM response containing curated quotes
            iteration: Iteration configuration for context
            
        Returns:
            List of parsed quote objects
        """
        quotes = []
        
        try:
            # Simple parsing - look for structured patterns in the response
            lines = response.split('\n')
            current_quote = {}
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                    
                # Look for document index patterns
                if line.startswith('Document') and ':' in line:
                    if current_quote:
                        quotes.append(current_quote)
                    current_quote = {"document_index": line.split(':')[0].replace('Document', '').strip()}
                
                # Look for quote text patterns
                elif line.startswith('"') and line.endswith('"'):
                    current_quote["quote_text"] = line.strip('"')
                
                # Look for relevance patterns
                elif 'relevance' in line.lower() or 'supports' in line.lower():
                    current_quote["statistical_relevance"] = line
                
                # Look for strength ratings
                elif 'strength' in line.lower() or 'rating' in line.lower():
                    # Extract numeric rating
                    import re
                    rating_match = re.search(r'(\d+)', line)
                    if rating_match:
                        current_quote["strength_rating"] = int(rating_match.group(1))
            
            # Add final quote if exists
            if current_quote:
                quotes.append(current_quote)
            
            # Add iteration metadata to each quote
            for quote in quotes:
                quote["iteration_focus"] = iteration['focus_area']
                quote["statistical_targets"] = iteration.get('statistical_targets', [])
                quote["curation_timestamp"] = datetime.now(timezone.utc).isoformat()
            
            self.logger.info(f"Parsed {len(quotes)} quotes from curation response")
            
        except Exception as e:
            self.logger.error(f"Failed to parse curated quotes: {e}")
            # Return a basic structure if parsing fails
            quotes = [{
                "quote_text": "Parsing failed - raw response available",
                "raw_response": response[:500],
                "iteration_focus": iteration['focus_area'],
                "error": str(e)
            }]
        
        return quotes
