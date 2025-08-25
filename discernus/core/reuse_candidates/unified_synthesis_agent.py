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
    
    def __init__(
        self,
        model: str,
        audit_logger: Optional[AuditLogger] = None,
        rag_index: Optional[Embeddings] = None,
        enhanced_mode: bool = True,
    ):
        """
        Initialize the agent.

        Args:
            model: The language model to use for synthesis.
            audit_logger: An optional audit logger instance.
            rag_index: An optional pre-built txtai RAG index for evidence retrieval.
            enhanced_mode: Whether to use the enhanced prompt template.
        """
        self.model = model
        self.audit_logger = audit_logger
        self.agent_name = "UnifiedSynthesisAgent"
        self.llm_gateway = LLMGateway(ModelRegistry())
        self.rag_index = rag_index  # Store the RAG index
        self.enhanced_mode = enhanced_mode
        self.prompt_template = (
            self._load_enhanced_prompt_template()
            if enhanced_mode
            else self._load_basic_prompt_template()
        )

    def generate_final_report(
        self,
        framework_path: Path,
        experiment_path: Path,
        research_data_artifact_hash: str,
        artifact_storage,
    ) -> Dict[str, Any]:
        """
        Generate the final academic report.
        This method now assumes the RAG index is available via self.rag_index
        and uses it to perform targeted evidence retrieval.
        """
        if self.audit_logger:
            self.audit_logger.log_agent_event(
                self.agent_name,
                "synthesis_start",
                {
                    "framework": str(framework_path),
                    "research_data_hash": research_data_artifact_hash,
                    "rag_enabled": self.rag_index is not None,
                },
            )

        try:
            # 1. Assemble the base prompt WITHOUT the evidence database.
            # The evidence will be injected Just-In-Time by this agent.
            assembler = SynthesisPromptAssembler()
            base_prompt = assembler.assemble_prompt(
                framework_path=framework_path,
                experiment_path=experiment_path,
                research_data_artifact_hash=research_data_artifact_hash,
                artifact_storage=artifact_storage,
                evidence_artifacts=[],  # Evidence is handled by RAG, not the assembler
            )

            # 2. Extract statistical findings from the research data to use as RAG queries.
            research_data = json.loads(
                artifact_storage.get_artifact(research_data_artifact_hash).decode("utf-8")
            )
            statistical_findings = self._extract_findings_for_rag(
                research_data.get("statistical_results", {})
            )

            # 3. Use the RAG index to find evidence for each finding.
            evidence_context = self._retrieve_and_format_evidence(statistical_findings)

            # 4. Construct the final, enhanced prompt with the retrieved evidence.
            final_prompt = f"""{base_prompt}

# AVAILABLE EVIDENCE (retrieved via targeted RAG queries):
{evidence_context}

Use the evidence above to support your statistical interpretations and generate the final report."""

            # 5. Execute the LLM call.
            final_report, metadata = self.llm_gateway.execute_call(
                model=self.model, prompt=final_prompt, temperature=0.1
            )

            if self.audit_logger:
                self.audit_logger.log_agent_event(
                    self.agent_name, "synthesis_complete", {"report_length": len(final_report)}
                )

            return {"final_report": final_report}

        except Exception as e:
            if self.audit_logger:
                self.audit_logger.log_error(
                    "synthesis_failed", str(e), {"agent": self.agent_name}
                )
            raise

    def _extract_findings_for_rag(self, statistical_results: Dict[str, Any]) -> List[str]:
        """Extract key statistical findings to use as RAG queries."""
        findings = []
        
        # Extract correlations from the actual structure: statistical_data.calculate_correlation_matrix
        statistical_data = statistical_results.get("statistical_data", {})
        correlation_matrix = statistical_data.get("calculate_correlation_matrix", {})
        
        # Generate queries for strong correlations (|r| > 0.7)
        for var1, correlations in correlation_matrix.items():
            if isinstance(correlations, dict):
                for var2, correlation in correlations.items():
                    if (isinstance(correlation, (int, float)) and 
                        var1 != var2 and 
                        abs(correlation) > 0.7):
                        # Create readable variable names
                        var1_clean = var1.replace('_raw', '').replace('_', ' ').title()
                        var2_clean = var2.replace('_raw', '').replace('_', ' ').title()
                        findings.append(f"{var1_clean} {var2_clean} correlation")
                        
        # Add queries for key derived metrics
        derived_metrics = statistical_data.get("summarize_corpus_metrics", {})
        if derived_metrics:
            findings.extend([
                "full cohesion index analysis",
                "strategic contradiction patterns",
                "tension indices interpretation",
                "cohesive fragmentative dimensions"
            ])
        
        # Ensure we have some queries even if correlations are missing
        if not findings:
            findings = [
                "framework dimensions analysis",
                "statistical results interpretation", 
                "corpus analysis findings"
            ]
            
        return findings[:10]  # Limit to avoid too many queries

    def _retrieve_and_format_evidence(self, queries: List[str]) -> str:
        """Use the RAG index to retrieve and format evidence for the given queries."""
        if not self.rag_index or not queries:
            return "No relevant evidence found."

        all_evidence_lines = []
        for query in queries:
            all_evidence_lines.append(f"\n## Evidence related to: '{query}'")
            try:
                search_results = self.rag_index.search(query, limit=3)
                if not search_results:
                    all_evidence_lines.append("- No direct evidence found in the database.")
                    continue

                for result in search_results:
                    # result is a dict {'id': ..., 'text': ..., 'score': ...}
                    quote = result.get("text", "Content not available")
                    score = result.get("score", 0.0)
                    # Attempt to parse the JSON content of the quote to get metadata
                    try:
                        evidence_data = json.loads(quote)
                        doc_name = evidence_data.get("document_name", "Unknown")
                        dimension = evidence_data.get("dimension", "Unknown")
                        actual_quote = evidence_data.get("quote_text", quote)
                        line = f"- From '{doc_name}' ({dimension}): \"{actual_quote}\" (Relevance: {score:.2f})"
                        all_evidence_lines.append(line)
                    except json.JSONDecodeError:
                        # If it's not JSON, it's just plain text, use it directly
                        all_evidence_lines.append(f"- \"{quote}\" (Relevance: {score:.2f})")

            except Exception as e:
                all_evidence_lines.append(f"- Error during RAG search for this query: {e}")
        
        return "\n".join(all_evidence_lines)

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
                # Use quiet=True to suppress verbose logging during bulk evidence retrieval
                evidence_content = artifact_storage.get_artifact(hash_id, quiet=True)
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
