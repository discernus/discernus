#!/usr/bin/env python3
"""
Unified Synthesis Agent for Discernus v8.1
==========================================

Generates publication-ready research reports using:
- Complete research data (raw scores, derived metrics, statistical results)
- txtai RAG integration for intelligent evidence retrieval
- THIN prompting approach with gemini-2.5-pro for reliability

Replaces the complex 3-agent synthesis model with a single, comprehensive agent.
"""

import json
import tempfile
from pathlib import Path
from typing import Dict, Any, List, Optional

from ...gateway.llm_gateway import LLMGateway
from ...gateway.model_registry import ModelRegistry
# txtai integration temporarily disabled for Phase 3 MVP
from ..prompt_assemblers.synthesis_assembler import SynthesisPromptAssembler
from ..audit_logger import AuditLogger
from txtai.embeddings import Embeddings


class UnifiedSynthesisAgent:
    """
    Single agent for complete research report synthesis.
    
    Uses proven THIN approach with txtai RAG integration for evidence-grounded reporting.
    """
    
    def __init__(self, 
                 model: str = "vertex_ai/gemini-2.5-pro",
                 audit_logger: Optional[AuditLogger] = None,
                 enhanced_mode: bool = True):
        """
        Initialize unified synthesis agent.
        
        Args:
            model: LLM model for synthesis (Pro model for reliability)
            audit_logger: Optional audit logger for provenance
            enhanced_mode: Use enhanced multi-level analysis (CRIT-006)
        """
        self.model = model
        self.llm_gateway = LLMGateway(ModelRegistry())
        self.audit_logger = audit_logger
        self.agent_name = "UnifiedSynthesisAgent"
        self.enhanced_mode = enhanced_mode
        
        # Load enhanced synthesis prompt template
        if enhanced_mode:
            self.enhanced_prompt_template = self._load_enhanced_prompt_template()
        
        if self.audit_logger:
            self.audit_logger.log_agent_event(self.agent_name, "initialization", {
                "model": self.model,
                "enhanced_mode": enhanced_mode,
                "capabilities": ["final_report_generation", "evidence_integration", "statistical_interpretation", "multi_level_analysis"]
            })
    
    def generate_final_report(self,
                            framework_path: Path,
                            experiment_path: Path,
                            research_data_artifact_hash: str,
                            rag_index: Embeddings = None,
                            artifact_storage = None,
                            evidence_artifact_hashes: list = None) -> Dict[str, Any]:
        """
        Generates publication-ready research report using RAG for evidence.

        Args:
            framework_path: Path to the framework file.
            experiment_path: Path to the experiment file.
            research_data_artifact_hash: Hash of the research data artifact.
            rag_index: A queryable txtai Embeddings object for evidence retrieval.
            artifact_storage: The artifact storage instance.

        Returns:
            A dictionary containing the final report.
        """
        if self.audit_logger:
            self.audit_logger.log_agent_event(self.agent_name, "synthesis_start", {
                "framework": str(framework_path),
                "research_data_hash": research_data_artifact_hash,
                "rag_enabled": True
            })
        
        try:
            # Use both evidence sources: direct evidence artifacts AND RAG index
            evidence_context_lines = []
            
            # 1. Get evidence from direct artifact hashes (like deprecated orchestrator)
            if evidence_artifact_hashes and artifact_storage:
                direct_evidence = self._get_all_evidence(evidence_artifact_hashes, artifact_storage)
                for evidence in direct_evidence:
                    quote = evidence.get('quote_text', '')
                    doc_name = evidence.get('document_name', 'Unknown')
                    dimension = evidence.get('dimension', 'Unknown')
                    confidence = evidence.get('confidence', 0.0)
                    
                    if quote:
                        evidence_context_lines.append(
                            f"- **{dimension}** from {doc_name} (confidence: {confidence:.2f}): \"{quote}\""
                        )
            
            # 2. Supplement with RAG index search if available
            if rag_index:
                try:
                    retrieved_evidence = rag_index.search(query="general context", limit=5)
                    
                    # Handle txtai search results which return (id, score) tuples
                    for result in retrieved_evidence:
                        if isinstance(result, tuple) and len(result) >= 2:
                            doc_id, score = result[0], result[1]
                            # Add RAG-retrieved evidence with proper attribution
                            evidence_context_lines.append(f"- RAG evidence from document {doc_id} (relevance: {score:.2f})")
                        elif isinstance(result, dict):
                            # Handle dictionary results (alternative txtai format)
                            quote = result.get('source_quote', result.get('text', 'No content available'))
                            evidence_context_lines.append(f"- RAG: {quote}")
                except Exception as e:
                    # RAG search failed, continue with direct evidence only
                    pass
            
            evidence_context = "\n".join(evidence_context_lines) if evidence_context_lines else "No relevant evidence found."
            
            assembler = SynthesisPromptAssembler()
            synthesis_prompt = assembler.assemble_prompt(
                framework_path=framework_path,
                experiment_path=experiment_path,
                research_data_artifact_hash=research_data_artifact_hash,
                artifact_storage=artifact_storage,
                evidence_artifacts=evidence_artifact_hashes or [] # Use evidence hashes if provided
            )
            
            enhanced_prompt = f"""{synthesis_prompt}

AVAILABLE EVIDENCE (retrieved via RAG):
{evidence_context}

Use this evidence to support your statistical interpretations."""
            
            # The LLM gateway returns a tuple: (final_report, metadata)
            final_report, metadata = self.llm_gateway.execute_call(
                model=self.model,
                prompt=enhanced_prompt,
                temperature=0.1
            )
            
            if self.audit_logger:
                self.audit_logger.log_agent_event(self.agent_name, "synthesis_complete", {
                    "report_length": len(final_report)
                })
            
            return {"final_report": final_report}
                
        except Exception as e:
            if self.audit_logger:
                self.audit_logger.log_error("synthesis_failed", str(e), {"agent": self.agent_name})
            # Re-raise the exception to be handled by the orchestrator
            raise
    
    def _load_enhanced_prompt_template(self) -> Dict[str, Any]:
        """Load enhanced synthesis prompt template."""
        try:
            import yaml
            prompt_file = Path(__file__).parent / "enhanced_synthesis_prompt.yaml"
            with open(prompt_file, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            # Fallback to basic mode if enhanced template not available
            if self.audit_logger:
                self.audit_logger.log_agent_event(self.agent_name, "enhanced_template_load_failed", {
                    "error": str(e),
                    "fallback": "basic_mode"
                })
            return {}
    
    def _generate_enhanced_report(self, framework_path: Path, experiment_path: Path, 
                                research_data_artifact_hash: str, evidence_artifact_hashes: List[str], 
                                artifact_storage) -> str:
        """Generate enhanced multi-level analytical report."""
        
        # 1. Load all required data
        framework_content = framework_path.read_text(encoding='utf-8')
        experiment_content = experiment_path.read_text(encoding='utf-8')
        
        # 2. Get research data
        research_data_bytes = artifact_storage.get_artifact(research_data_artifact_hash)
        research_data = json.loads(research_data_bytes.decode('utf-8'))
        
        # 3. Prepare evidence context
        evidence_context = self._prepare_evidence_context(evidence_artifact_hashes, artifact_storage)
        
        # 4. Create experiment metadata from available information
        experiment_metadata = f"""
        Experiment Path: {experiment_path}
        Framework Path: {framework_path}
        Research Data Available: Yes
        Evidence Artifacts: {len(evidence_artifact_hashes)} available
        """
        
        # 5. Assemble enhanced prompt
        enhanced_prompt = self.enhanced_prompt_template['template'].format(
            experiment_metadata=experiment_metadata,
            framework_content=framework_content,
            experiment_content=experiment_content,
            research_data=json.dumps(research_data, indent=2),
            evidence_context=evidence_context
        )
        
        # 5. Generate report with enhanced prompt
        return self._generate_report_with_llm(enhanced_prompt)
    
    def _generate_report_with_llm(self, prompt: str) -> str:
        """Generate report using LLM with enhanced prompt."""
        try:
            response, metadata = self.llm_gateway.execute_call(
                model=self.model,
                prompt=prompt,
                system_prompt=self.enhanced_prompt_template.get('system_prompt', ''),
                max_tokens=8000,  # Increased for comprehensive reports
                temperature=0.1   # Low temperature for analytical consistency
            )
            
            if self.audit_logger:
                self.audit_logger.log_agent_event(self.agent_name, "enhanced_report_generated", {
                    "tokens_used": metadata.get('usage', {}).get('total_tokens', 0),
                    "model": self.model,
                    "report_length": len(response)
                })
            
            return response
            
        except Exception as e:
            if self.audit_logger:
                self.audit_logger.log_agent_event(self.agent_name, "llm_generation_failed", {
                    "error": str(e)
                })
            raise
    
    def _get_all_evidence(self, evidence_artifact_hashes: List[str], artifact_storage) -> List[Dict[str, Any]]:
        """Retrieve and combine all evidence from artifacts."""
        all_evidence = []
        
        for hash_id in evidence_artifact_hashes:
            try:
                evidence_content = artifact_storage.get_artifact(hash_id)
                evidence_data = json.loads(evidence_content.decode('utf-8'))
                evidence_list = evidence_data.get('evidence_data', [])
                all_evidence.extend(evidence_list)
            except Exception as e:
                if self.audit_logger:
                    self.audit_logger.log_agent_event(self.agent_name, "evidence_retrieval_failed", {
                        "artifact_hash": hash_id,
                        "error": str(e)
                    })
                continue
        
        return all_evidence
    
    def _prepare_evidence_context(self, evidence_artifact_hashes: List[str], artifact_storage) -> str:
        """Prepare comprehensive evidence context with count and direct access."""
        all_evidence = self._get_all_evidence(evidence_artifact_hashes, artifact_storage)
        
        if not all_evidence:
            return "No evidence available for citation."
        
        # Enhanced mode: Provide evidence count AND direct access (superior to RAG queries)
        evidence_lines = [
            f"EVIDENCE DATABASE: {len(all_evidence)} pieces of textual evidence extracted during analysis.",
            f"All evidence is provided below for direct citation - no queries needed.",
            "",
            "CITATION REQUIREMENTS:",
            "- Every major statistical claim MUST be supported by direct quotes from evidence below",
            "- Use format: 'As [Speaker] stated: \"[exact quote]\" (Source: [document_name])'",
            "- Prioritize evidence with confidence scores >0.8",
            "- Integrate statistical findings with textual evidence for coherent narratives",
            "",
            "AVAILABLE EVIDENCE FOR DIRECT CITATION:",
            ""
        ]
        
        for i, evidence in enumerate(all_evidence, 1):
            doc_name = evidence.get('document_name', 'Unknown')
            dimension = evidence.get('dimension', 'Unknown')
            quote = evidence.get('quote_text', '')
            confidence = evidence.get('confidence', 0.0)
            
            evidence_lines.append(f"{i}. **{dimension}** evidence from {doc_name} (confidence: {confidence:.2f}):")
            evidence_lines.append(f"   \"{quote}\"")
            evidence_lines.append("")  # Empty line for readability
        
        return "\n".join(evidence_lines)
    
    def _generate_report_with_evidence_integration(self, synthesis_prompt: str) -> str:
        """Generate final report using LLM with evidence integration instructions."""
        
        # Use THIN approach - natural language prompt with Pro model for reliability
        response_text, metadata = self.llm_gateway.execute_call(
            model=self.model,
            prompt=synthesis_prompt,
            system_prompt="You are an expert computational social science researcher. Generate comprehensive, evidence-based research reports that meet publication standards."
        )
        
        if not metadata.get("success") or not response_text:
            raise ValueError(f"Failed to generate synthesis report: {metadata.get('error')}")
        
        return response_text.strip()
    
    def _validate_report_quality(self, report: str) -> Dict[str, Any]:
        """Validate the quality of the generated report."""
        quality_metrics = {
            "total_length": len(report),
            "has_executive_summary": "## Executive Summary" in report,
            "has_methodology": "## Methodology" in report,
            "has_results": "## Results" in report,
            "has_conclusion": "## Conclusion" in report,
            "citation_count": report.count("(Source:"),
            "quote_count": report.count('As ') + report.count(' stated:'),
            "meets_basic_structure": True
        }
        
        # Check for minimum academic standards
        quality_metrics["meets_basic_structure"] = (
            quality_metrics["has_executive_summary"] and
            quality_metrics["has_methodology"] and 
            quality_metrics["has_results"] and
            quality_metrics["has_conclusion"] and
            quality_metrics["citation_count"] >= 3  # Minimum evidence citations
        )
        
        return quality_metrics
