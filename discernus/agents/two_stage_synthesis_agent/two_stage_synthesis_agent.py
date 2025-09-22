#!/usr/bin/env python3
"""
Two-Stage Synthesis Agent for Discernus
=======================================

Implements two-stage synthesis to prevent hallucination and ensure data-driven reports:

Stage 1: Data-Driven Analysis
- Input: Statistical results, experiment metadata, framework
- Process: Generate coherent analysis anchored in statistical findings
- Output: Complete research report without evidence quotes
- Goal: Establish all analytical claims based solely on data

Stage 2: Evidence Integration  
- Input: Stage 1 report + curated evidence from IntelligentEvidenceRetrievalAgent
- Process: Enhance report with supporting quotes, create evidence appendix
- Output: Final report with integrated evidence and complete audit trail
- Goal: Support existing claims with evidence, no new analytical claims

Anti-Hallucination Architecture:
- Stage separation prevents evidence from influencing analytical conclusions
- Stage 2 is strictly additive (quotes + appendix), no new analysis
- All claims must originate from Stage 1 statistical analysis
- Evidence serves only to illustrate pre-established findings
"""

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional

from discernus.core.standard_agent import StandardAgent
from discernus.core.agent_result import AgentResult
from discernus.core.run_context import RunContext
from discernus.core.security_boundary import ExperimentSecurityBoundary
from discernus.core.local_artifact_storage import LocalArtifactStorage
from discernus.core.audit_logger import AuditLogger
from discernus.gateway.llm_gateway_enhanced import EnhancedLLMGateway
from discernus.gateway.model_registry import ModelRegistry
import yaml


class TwoStageSynthesisAgent(StandardAgent):
    """
    Two-stage synthesis agent that prevents hallucination through architectural separation.
    
    The agent ensures all analytical claims originate from statistical data before any
    evidence integration, maintaining strict separation between analysis and illustration.
    """
    
    def __init__(self, 
                 security: ExperimentSecurityBoundary,
                 storage: LocalArtifactStorage,
                 audit: AuditLogger,
                 config: Optional[Dict[str, Any]] = None):
        """
        Initialize the TwoStageSynthesisAgent.
        
        Args:
            security: Security boundary for experiment access
            storage: Artifact storage interface
            audit: Audit logging interface
            config: Optional agent configuration
        """
        super().__init__(security, storage, audit, config)
        self.agent_name = "TwoStageSynthesisAgent"
        self.logger = logging.getLogger(__name__)
        
        # Initialize enhanced LLM gateway for tool calling
        model_registry = ModelRegistry()
        self.llm_gateway = EnhancedLLMGateway(model_registry)
        
        # Stage configuration
        self.stage1_model = "vertex_ai/gemini-2.5-pro"  # Pro for analytical depth
        self.stage2_model = "vertex_ai/gemini-2.5-flash"  # Flash for evidence integration
        
        # Load externalized prompts
        self.stage1_prompt = self._load_prompt_template("stage1_prompt.yaml")
        self.stage2_prompt = self._load_prompt_template("stage2_prompt.yaml")
        
        self.logger.info(f"Initialized {self.agent_name} with two-stage architecture and externalized prompts")
    
    def _load_prompt_template(self, filename: str) -> str:
        """Load a prompt template from the YAML file."""
        prompt_path = Path(__file__).parent / filename
        if not prompt_path.exists():
            error_msg = f"TwoStageSynthesisAgent prompt file not found at {prompt_path}"
            self.audit.log_agent_event(self.agent_name, "prompt_error", {"error": error_msg})
            raise FileNotFoundError(error_msg)
        
        with open(prompt_path, 'r') as f:
            yaml_content = f.read()
        prompt_data = yaml.safe_load(yaml_content)
        return prompt_data['template']
    
    def get_capabilities(self) -> List[str]:
        """Return list of agent capabilities."""
        return [
            "two_stage_synthesis",
            "anti_hallucination_architecture", 
            "data_driven_analysis",
            "evidence_integration",
            "evidence_appendix_generation",
            "analytical_claim_validation",
            "statistical_anchoring",
            "externalized_prompts",
            "tool_calling"
        ]
    
    def execute(self, run_context: RunContext, **kwargs) -> AgentResult:
        """
        Execute two-stage synthesis process.
        
        Args:
            run_context: The RunContext containing all experiment data
            **kwargs: Additional execution parameters
            
        Returns:
            AgentResult with final synthesis report and evidence appendix
        """
        try:
            self.logger.info("TwoStageSynthesisAgent starting two-stage execution")
            self.log_execution_start(**kwargs)
            
            # Validate inputs
            if not self._validate_inputs(run_context):
                return AgentResult(
                    success=False,
                    artifacts=[],
                    metadata={"agent_name": self.agent_name, "error": "Input validation failed"},
                    error_message="Required inputs missing for synthesis"
                )
            
            # Stage 1: Data-Driven Analysis (no evidence)
            self.logger.info("Stage 1: Generating data-driven analysis...")
            stage1_report = self._execute_stage1_analysis(run_context)
            
            if not stage1_report:
                return AgentResult(
                    success=False,
                    artifacts=[],
                    metadata={"agent_name": self.agent_name, "error": "Stage 1 analysis failed"},
                    error_message="Failed to generate data-driven analysis"
                )
            
            # Store Stage 1 report
            stage1_artifact = self._store_stage1_report(stage1_report)
            
            # Stage 2: Evidence Integration
            self.logger.info("Stage 2: Integrating curated evidence...")
            final_report = self._execute_stage2_integration(run_context, stage1_report)
            
            if not final_report:
                return AgentResult(
                    success=False,
                    artifacts=[stage1_artifact],
                    metadata={"agent_name": self.agent_name, "error": "Stage 2 integration failed"},
                    error_message="Failed to integrate evidence into report"
                )
            
            # Store final report with evidence
            final_artifact = self._store_final_report(final_report)
            
            # Create evidence appendix
            appendix_artifact = self._create_evidence_appendix(run_context, final_report)
            
            artifacts = [stage1_artifact, final_artifact]
            if appendix_artifact:
                artifacts.append(appendix_artifact)
            
            self.logger.info(f"Two-stage synthesis completed: {len(artifacts)} artifacts created")
            
            return AgentResult(
                success=True,
                artifacts=artifacts,
                metadata={
                    "agent_name": self.agent_name,
                    "stage1_model": self.stage1_model,
                    "stage2_model": self.stage2_model,
                    "synthesis_method": "two_stage_anti_hallucination",
                    "evidence_integration": True,
                    "appendix_created": appendix_artifact is not None
                }
            )
            
        except Exception as e:
            self.logger.error(f"Two-stage synthesis failed: {e}")
            return AgentResult(
                success=False,
                artifacts=[],
                metadata={"agent_name": self.agent_name, "error": str(e)},
                error_message=f"Two-stage synthesis failed: {e}"
            )
    
    def _validate_inputs(self, run_context: RunContext) -> bool:
        """Validate that required inputs are available for synthesis."""
        # Trust upstream agents - just check existence, not content quality
        if not hasattr(run_context, 'statistical_results') or not run_context.statistical_results:
            self.logger.error("No statistical results found in run_context")
            return False
        
        if not run_context.experiment_id:
            self.logger.error("No experiment_id found in run_context")
            return False
        
        if not run_context.framework_path:
            self.logger.error("No framework_path found in run_context")
            return False
        
        self.logger.info("Input validation passed: statistical results, experiment metadata, and framework available")
        return True
    
    def _execute_stage1_analysis(self, run_context: RunContext) -> Optional[str]:
        """
        Execute Stage 1: Data-driven analysis without evidence quotes.
        
        Args:
            run_context: The RunContext containing statistical results
            
        Returns:
            Stage 1 report text or None if failed
        """
        try:
            self.logger.info("Starting Stage 1: Framework-driven data analysis")
            
            # Prepare the context for Stage 1 analysis
            stage1_context = self._prepare_stage1_context(run_context)
            
            # Create the Stage 1 prompt with all necessary data
            stage1_prompt = self._create_stage1_prompt(stage1_context)
            
            # Execute Stage 1 analysis with Gemini Pro
            self.logger.info(f"Executing Stage 1 analysis with {self.stage1_model}")
            
            response_tuple = self.llm_gateway.execute_call(
                model=self.stage1_model,
                prompt=stage1_prompt,
                temperature=0.3,  # Lower temperature for analytical consistency
                max_tokens=8000   # Sufficient for comprehensive analysis
            )
            
            # Extract content from tuple response
            response, metadata = response_tuple
            
            if not response or not response.strip():
                self.logger.error("Stage 1 analysis returned empty response")
                return None
            
            self.logger.info(f"Stage 1 analysis completed: {len(response)} characters")
            
            # Log successful execution
            self.audit.log_agent_event(
                self.agent_name, 
                "stage1_completed",
                {
                    "model_used": self.stage1_model,
                    "response_length": len(response),
                    "temperature": 0.3
                }
            )
            
            return response
            
        except Exception as e:
            self.logger.error(f"Stage 1 analysis failed: {e}")
            self.audit.log_agent_event(
                self.agent_name,
                "stage1_failed", 
                {"error": str(e)}
            )
            return None
    
    def _execute_stage2_integration(self, run_context: RunContext, stage1_report: str) -> Optional[str]:
        """
        Execute Stage 2: Evidence integration with curated quotes.
        
        Args:
            run_context: The RunContext containing curated evidence
            stage1_report: The Stage 1 report to enhance with evidence
            
        Returns:
            Final report with integrated evidence or None if failed
        """
        try:
            self.logger.info("Starting Stage 2: Evidence integration")
            
            # Prepare curated evidence from the IntelligentEvidenceRetrievalAgent
            curated_evidence = self._prepare_curated_evidence(run_context)
            
            if not curated_evidence:
                self.logger.warning("No curated evidence found - generating Stage 2 report with explanatory note")
                
                # Create a Stage 2 report that explicitly states no evidence was integrated
                timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
                no_evidence_report = f"""---
agent: {self.agent_name}
stage: stage2_no_evidence_integrated
timestamp: {timestamp}
model_used: {self.stage2_model}
evidence_included: false
synthesis_method: two_stage_fallback
---

# Research Synthesis Report

**Note on Evidence Integration:** No curated evidence was provided for this synthesis run. The following analysis is the complete data-driven report from Stage 1. No textual evidence has been integrated into this version of the report.

---

{stage1_report}
"""
                return no_evidence_report
            
            # Create the Stage 2 prompt with Stage 1 report and evidence
            stage2_prompt = self._create_stage2_prompt(stage1_report, curated_evidence)
            
            # Execute Stage 2 integration with Gemini Flash
            self.logger.info(f"Executing Stage 2 integration with {self.stage2_model}")
            
            response_tuple = self.llm_gateway.execute_call(
                model=self.stage2_model,
                prompt=stage2_prompt,
                temperature=0.2,  # Lower temperature for precise integration
                max_tokens=10000  # More tokens for enhanced report
            )
            
            # Extract content from tuple response
            response, metadata = response_tuple
            
            if not response or not response.strip():
                self.logger.error("Stage 2 integration returned empty response")
                return stage1_report  # Fallback to Stage 1 report
            
            self.logger.info(f"Stage 2 integration completed: {len(response)} characters")
            
            # Log successful execution
            self.audit.log_agent_event(
                self.agent_name,
                "stage2_completed",
                {
                    "model_used": self.stage2_model,
                    "response_length": len(response),
                    "evidence_count": len(curated_evidence),
                    "temperature": 0.2
                }
            )
            
            return response
            
        except Exception as e:
            self.logger.error(f"Stage 2 integration failed: {e}")
            self.audit.log_agent_event(
                self.agent_name,
                "stage2_failed",
                {"error": str(e)}
            )
            # Return Stage 1 report as fallback
            return stage1_report
    
    def _store_stage1_report(self, report: str) -> str:
        """Store Stage 1 report as artifact."""
        artifact_data = {
            "agent_name": self.agent_name,
            "stage": "stage1_data_driven_analysis",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "model_used": self.stage1_model,
            "report_content": report,
            "evidence_included": False,
            "synthesis_method": "data_driven_only"
        }
        
        return self.storage.store_artifact(
            content=artifact_data,
            artifact_type="stage1_synthesis_report",
            experiment_id="stage1_analysis"
        )
    
    def _store_final_report(self, report: str) -> str:
        """Store final report as raw markdown content."""
        # Add metadata header to the markdown content itself
        timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
        markdown_content = f"""---
agent: {self.agent_name}
stage: stage2_evidence_integrated
timestamp: {timestamp}
model_used: {self.stage2_model}
evidence_included: true
synthesis_method: two_stage_with_evidence
---

{report}"""
        
        return self.storage.store_artifact(
            content=markdown_content,
            artifact_type="final_synthesis_report",
            experiment_id="final_report"
        )
    
    def _prepare_stage1_context(self, run_context: RunContext) -> Dict[str, Any]:
        """Prepare all necessary context data for Stage 1 analysis."""
        try:
            # Load framework content
            framework_content = ""
            if run_context.framework_path:
                framework_path = Path(run_context.framework_path)
                if framework_path.exists():
                    framework_content = framework_path.read_text(encoding='utf-8')
            
            # Load experiment content
            experiment_content = ""
            experiment_path = Path(run_context.experiment_id) / "experiment.md"
            if experiment_path.exists():
                experiment_content = experiment_path.read_text(encoding='utf-8')
            
            # Load corpus manifest
            corpus_manifest = ""
            if run_context.corpus_path:
                corpus_path = Path(run_context.corpus_path)
                if corpus_path.exists():
                    corpus_manifest = corpus_path.read_text(encoding='utf-8')
            
            return {
                "framework_content": framework_content,
                "experiment_content": experiment_content,
                "corpus_manifest": corpus_manifest,
                "statistical_results": run_context.statistical_results or {},
                "experiment_id": run_context.experiment_id,
                "metadata": run_context.metadata or {}
            }
            
        except Exception as e:
            self.logger.error(f"Failed to prepare Stage 1 context: {e}")
            return {}
    
    def _create_stage1_prompt(self, context: Dict[str, Any]) -> str:
        """Create the complete Stage 1 prompt with all context data."""
        
        # Format statistical results for the prompt
        statistical_summary = self._format_statistical_results(context.get("statistical_results", {}))
        
        # Create the complete prompt by combining template with context
        prompt = f"""{self.stage1_prompt}

**FRAMEWORK SPECIFICATION:**
{context.get('framework_content', 'Framework content not available')}

**EXPERIMENT CONFIGURATION:**
{context.get('experiment_content', 'Experiment content not available')}

**CORPUS MANIFEST:**
{context.get('corpus_manifest', 'Corpus manifest not available')}

**STATISTICAL ANALYSIS RESULTS:**
{statistical_summary}

**EXPERIMENT METADATA:**
Experiment ID: {context.get('experiment_id', 'Unknown')}
Analysis Completed: {context.get('metadata', {}).get('analysis_completed', 'Unknown')}

Please generate a comprehensive framework-driven analysis report following the Stage 1 protocol outlined above."""

        return prompt
    
    def _format_statistical_results(self, statistical_results: Dict[str, Any]) -> str:
        """Format statistical results for inclusion in the Stage 1 prompt."""
        if not statistical_results:
            return "No statistical results available"
        
        try:
            # Format the key sections from the enhanced statistical agent output
            formatted_sections = []
            
            # Execution results
            if "execution_results" in statistical_results:
                formatted_sections.append("## Statistical Analysis Results")
                execution_results = statistical_results["execution_results"]
                
                for analysis_type, results in execution_results.items():
                    if results:
                        formatted_sections.append(f"### {analysis_type.replace('_', ' ').title()}")
                        formatted_sections.append(f"```json\n{json.dumps(results, indent=2)}\n```")
            
            # Framework performance assessment (from enhanced statistical agent)
            if "framework_performance_assessment" in statistical_results:
                formatted_sections.append("## Framework Performance Assessment")
                fpa = statistical_results["framework_performance_assessment"]
                formatted_sections.append(f"```json\n{json.dumps(fpa, indent=2)}\n```")
            
            # Sample size assessment
            if "sample_size_assessment" in statistical_results:
                formatted_sections.append("## Sample Size Assessment")
                ssa = statistical_results["sample_size_assessment"]
                formatted_sections.append(f"```json\n{json.dumps(ssa, indent=2)}\n```")
            
            # Synthesis intelligence (from enhanced statistical agent)
            if "synthesis_intelligence" in statistical_results:
                formatted_sections.append("## Synthesis Intelligence")
                si = statistical_results["synthesis_intelligence"]
                formatted_sections.append(f"```json\n{json.dumps(si, indent=2)}\n```")
            
            return "\n\n".join(formatted_sections) if formatted_sections else "Statistical results format not recognized"
            
        except Exception as e:
            self.logger.error(f"Failed to format statistical results: {e}")
            return f"Error formatting statistical results: {str(e)}"
    
    def _prepare_curated_evidence(self, run_context: RunContext) -> List[Dict[str, Any]]:
        """Prepare curated evidence from IntelligentEvidenceRetrievalAgent artifacts."""
        try:
            curated_evidence = []
            
            # Look for curated evidence artifacts from IntelligentEvidenceRetrievalAgent
            if hasattr(run_context, 'evidence_artifacts') and run_context.evidence_artifacts:
                for artifact_hash in run_context.evidence_artifacts:
                    try:
                        # Load the artifact
                        artifact_bytes = self.storage.get_artifact(artifact_hash)
                        artifact_data = json.loads(artifact_bytes.decode('utf-8'))
                        
                        # Check if this is a curated evidence artifact
                        if (isinstance(artifact_data, dict) and 
                            artifact_data.get('artifact_type') == 'curated_evidence'):
                            
                            evidence_content = artifact_data.get('content', {})
                            if isinstance(evidence_content, dict) and 'quotes' in evidence_content:
                                curated_evidence.extend(evidence_content['quotes'])
                                
                    except Exception as e:
                        self.logger.warning(f"Failed to load evidence artifact {artifact_hash}: {e}")
                        continue
            
            self.logger.info(f"Prepared {len(curated_evidence)} curated evidence quotes")
            return curated_evidence
            
        except Exception as e:
            self.logger.error(f"Failed to prepare curated evidence: {e}")
            return []
    
    def _create_stage2_prompt(self, stage1_report: str, curated_evidence: List[Dict[str, Any]]) -> str:
        """Create the complete Stage 2 prompt with Stage 1 report and evidence."""
        
        # Format evidence for the prompt
        evidence_summary = self._format_curated_evidence(curated_evidence)
        
        # Create the complete Stage 2 prompt
        prompt = f"""{self.stage2_prompt}

**STAGE 1 REPORT TO ENHANCE:**
{stage1_report}

**CURATED EVIDENCE FOR INTEGRATION:**
{evidence_summary}

Please enhance the Stage 1 report by strategically integrating the curated evidence quotes throughout the document, following the Stage 2 protocol outlined above. Preserve all analytical claims and conclusions from Stage 1 while bringing them to life with supporting evidence."""

        return prompt
    
    def _format_curated_evidence(self, curated_evidence: List[Dict[str, Any]]) -> str:
        """Format curated evidence for inclusion in the Stage 2 prompt."""
        if not curated_evidence:
            return "No curated evidence available"
        
        try:
            formatted_quotes = []
            
            for i, quote_data in enumerate(curated_evidence, 1):
                quote_text = quote_data.get('text', 'No text available')
                document_source = quote_data.get('document_index', 'Unknown source')
                relevance = quote_data.get('relevance', 'Not specified')
                strength = quote_data.get('strength_rating', 'Not rated')
                
                formatted_quote = f"""**Quote {i}:**
Text: "{quote_text}"
Source: {document_source}
Relevance: {relevance}
Strength: {strength}
"""
                formatted_quotes.append(formatted_quote)
            
            return "\n".join(formatted_quotes)
            
        except Exception as e:
            self.logger.error(f"Failed to format curated evidence: {e}")
            return f"Error formatting evidence: {str(e)}"
    
    def _create_evidence_appendix(self, run_context: RunContext, final_report: str) -> Optional[str]:
        """Create evidence appendix organized by statistical conclusion."""
        try:
            self.logger.info("Creating evidence appendix")
            
            # Get curated evidence
            curated_evidence = self._prepare_curated_evidence(run_context)
            
            if not curated_evidence:
                self.logger.info("No curated evidence for appendix")
                return None
            
            # Create appendix content
            appendix_content = self._format_evidence_appendix(curated_evidence)
            
            # Store as artifact
            artifact_data = {
                "agent_name": self.agent_name,
                "stage": "evidence_appendix",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "appendix_content": appendix_content,
                "evidence_count": len(curated_evidence),
                "synthesis_method": "two_stage_with_appendix"
            }
            
            appendix_hash = self.storage.store_artifact(
                content=artifact_data,
                artifact_type="evidence_appendix",
                experiment_id="evidence_appendix"
            )
            
            self.logger.info(f"Evidence appendix created with {len(curated_evidence)} quotes")
            return appendix_hash
            
        except Exception as e:
            self.logger.error(f"Failed to create evidence appendix: {e}")
            return None
    
    def _format_evidence_appendix(self, curated_evidence: List[Dict[str, Any]]) -> str:
        """Format evidence appendix with complete attribution and organization."""
        
        appendix_sections = [
            "# Evidence Appendix",
            "",
            "This appendix contains all evidence quotes used in the synthesis report, organized for complete audit trail and reproducibility.",
            "",
            "## Complete Evidence Inventory",
            ""
        ]
        
        # Group evidence by source document if possible
        evidence_by_source = {}
        for quote_data in curated_evidence:
            source = quote_data.get('document_index', 'Unknown Source')
            if source not in evidence_by_source:
                evidence_by_source[source] = []
            evidence_by_source[source].append(quote_data)
        
        # Format by source
        for source, quotes in evidence_by_source.items():
            appendix_sections.append(f"### {source}")
            appendix_sections.append("")
            
            for i, quote_data in enumerate(quotes, 1):
                quote_text = quote_data.get('text', 'No text available')
                relevance = quote_data.get('relevance', 'Not specified')
                strength = quote_data.get('strength_rating', 'Not rated')
                
                appendix_sections.extend([
                    f"**Quote {i}:**",
                    f'"{quote_text}"',
                    f"- **Relevance:** {relevance}",
                    f"- **Strength Rating:** {strength}",
                    ""
                ])
        
        # Add summary statistics
        appendix_sections.extend([
            "## Evidence Summary",
            f"- **Total Quotes:** {len(curated_evidence)}",
            f"- **Source Documents:** {len(evidence_by_source)}",
            f"- **Generated:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}",
            ""
        ])
        
        return "\n".join(appendix_sections)
