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
        evidence_retrieval_results_hash: str = None,
    ) -> Dict[str, Any]:
        """
        Generate the final academic report.
        This method now reads curated evidence directly from EvidenceRetriever output
        instead of using RAG index queries.
        """
        if self.audit_logger:
            self.audit_logger.log_agent_event(
                self.agent_name,
                "synthesis_start",
                {
                    "framework": str(framework_path),
                    "research_data_hash": research_data_artifact_hash,
                    "evidence_retrieval_hash": evidence_retrieval_results_hash,
                },
            )

        try:
            # 1. Assemble the base prompt with framework, experiment, and research data
            assembler = SynthesisPromptAssembler()
            base_prompt = assembler.assemble_prompt(
                framework_path=framework_path,
                experiment_path=experiment_path,
                research_data_artifact_hash=research_data_artifact_hash,
                artifact_storage=artifact_storage,
                evidence_artifacts=[],  # Evidence will be added separately
            )

            # 2. Load and prepare curated evidence from EvidenceRetriever
            evidence_context = self._prepare_evidence_context_from_curated_evidence(
                evidence_retrieval_results_hash, artifact_storage
            )

            # 3. Construct the final, enhanced prompt with the curated evidence
            final_prompt = f"""{base_prompt}

# EVIDENCE INTEGRATION REQUIREMENTS

## CURATED EVIDENCE FOR SYNTHESIS
{evidence_context}

## CRITICAL REQUIREMENTS FOR EVIDENCE INTEGRATION
- Every major statistical claim MUST be supported by evidence from the curated evidence above
- Use the exact format: 'As [Speaker] stated: \"[exact quote]\" (Source: [document_name])'
- Include speaker identification and source document for every quote
- Weave evidence quotes naturally into your analysis, not as separate citations
- If no evidence was found for a finding, explicitly state: "No supporting textual evidence was found for this statistical pattern"
- Do NOT proceed to report writing until you have examined the evidence above

## SYNTHESIS INSTRUCTIONS
Generate your comprehensive academic report following the structure specified in the prompt above, ensuring all claims are evidence-backed using the curated evidence provided."""

            # 4. Execute the LLM call
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
                # Check if we're using our EvidenceMatchingWrapper
                if hasattr(self.rag_index, 'search_evidence'):
                    # Use our wrapper's intelligent search method
                    search_results = self.rag_index.search_evidence(query, limit=3)
                    if not search_results:
                        all_evidence_lines.append("- No direct evidence found in the database.")
                        continue

                    for result in search_results:
                        quote_text = result.get('quote_text', 'Content not available')
                        doc_name = result.get('document_name', 'Unknown')
                        dimension = result.get('dimension', 'Unknown')
                        relevance_score = result.get('relevance_score', 0.0)
                        
                        if quote_text and quote_text.strip():
                            line = f"- From '{doc_name}' ({dimension}): \"{quote_text}\" (Relevance: {relevance_score:.2f})"
                            all_evidence_lines.append(line)
                        else:
                            all_evidence_lines.append(f"- From '{doc_name}' ({dimension}): No quote text available")
                
                else:
                    # Fallback to standard txtai interface
                    search_results = self.rag_index.search(query, limit=3)
                    if not search_results:
                        all_evidence_lines.append("- No direct evidence found in the database.")
                        continue

                    # Get documents if available
                    documents = getattr(self.rag_index, 'documents', [])
                    
                    for result in search_results:
                        if isinstance(result, tuple) and len(result) == 2:
                            # txtai format: (doc_id, score)
                            doc_id, score = result
                            if documents and 0 <= doc_id < len(documents):
                                doc = documents[doc_id]
                                quote = doc.get("text", "Content not available")
                                metadata = doc.get("metadata", {})
                                doc_name = metadata.get("document_name", "Unknown")
                                dimension = metadata.get("dimension", "Unknown")
                                line = f"- From '{doc_name}' ({dimension}): \"{quote}\" (Relevance: {score:.2f})"
                                all_evidence_lines.append(line)
                            else:
                                all_evidence_lines.append(f"- Document {doc_id}: Content not available (Relevance: {score:.2f})")
                        else:
                            # Assume dict format
                            quote = result.get("text", "Content not available")
                            score = result.get("score", 0.0)
                            all_evidence_lines.append(f"- \"{quote}\" (Relevance: {score:.2f})")

            except Exception as e:
                all_evidence_lines.append(f"- Error during RAG search for this query: {e}")
        
        return "\n".join(all_evidence_lines)

    def _load_basic_prompt_template(self) -> Dict[str, Any]:
        """Load basic synthesis prompt template."""
        return {
            "system": "You are an expert academic synthesis agent.",
            "user": "Generate a comprehensive synthesis report."
        }
    
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
    
    def _get_evidence_through_rag(self, query: str, rag_index: Any) -> List[Dict[str, Any]]:
        """Get evidence ONLY through RAG - no direct access allowed."""
        if not rag_index:
            raise ValueError("RAG index required for evidence retrieval - no direct evidence access allowed")
        
        try:
            # Use RAG to find evidence
            search_results = rag_index.search(query, limit=5)
            return self._format_rag_results(search_results)
        except Exception as e:
            if self.audit_logger:
                self.audit_logger.log_agent_event(self.agent_name, "rag_evidence_retrieval_failed", {
                    "query": query,
                    "error": str(e)
                })
            return []
    
    def _format_rag_results(self, search_results: List) -> List[Dict[str, Any]]:
        """Format RAG search results into evidence format."""
        formatted_results = []
        
        for result in search_results:
            try:
                if isinstance(result, tuple) and len(result) == 2:
                    doc_id, score = result
                elif isinstance(result, dict):
                    doc_id = result.get('id', result.get('document', 0))
                    score = result.get('score', 0.0)
                else:
                    doc_id = result
                    score = 0.0
                
                # Get document content through RAG interface
                if hasattr(self.rag_index, 'documents') and self.rag_index.documents:
                    if isinstance(doc_id, int) and 0 <= doc_id < len(self.rag_index.documents):
                        doc = self.rag_index.documents[doc_id]
                        formatted_results.append({
                            "quote_text": doc.get('text', ''),
                            "document_name": doc.get('metadata', {}).get('document_name', 'Unknown'),
                            "dimension": doc.get('metadata', {}).get('dimension', 'Unknown'),
                            "confidence": doc.get('metadata', {}).get('confidence', 0.0),
                            "relevance_score": score
                        })
                else:
                    # txtai returns content directly in search results
                    if hasattr(result, 'get'):
                        formatted_results.append({
                            "quote_text": result.get('text', ''),
                            "document_name": result.get('metadata', {}).get('document_name', 'Unknown') if result.get('metadata') else 'Unknown',
                            "dimension": result.get('metadata', {}).get('dimension', 'Unknown') if result.get('metadata') else 'Unknown',
                            "confidence": result.get('metadata', {}).get('confidence', 0.0) if result.get('metadata') else 0.0,
                            "relevance_score": score
                        })
            except Exception as e:
                if self.audit_logger:
                    self.audit_logger.log_agent_event(self.agent_name, "rag_result_formatting_failed", {
                        "result": str(result),
                        "error": str(e)
                    })
                continue
        
        return formatted_results
    
    def _prepare_evidence_context_from_curated_evidence(self, evidence_retrieval_results_hash: str, artifact_storage) -> str:
        """Prepare evidence context from curated evidence file produced by EvidenceRetriever."""
        if not evidence_retrieval_results_hash:
            return "⚠️ **EVIDENCE STATUS**: No evidence retrieval results available. Proceed with synthesis using only statistical data."
        
        try:
            # Load the curated evidence from EvidenceRetriever
            evidence_content = artifact_storage.get_artifact(evidence_retrieval_results_hash)
            if not evidence_content:
                return "⚠️ **EVIDENCE STATUS**: Evidence retrieval results not found. Proceed with synthesis using only statistical data."
            
            evidence_data = json.loads(evidence_content.decode('utf-8'))
            
            # Extract evidence results
            evidence_results = evidence_data.get('evidence_results', [])
            total_quotes = evidence_data.get('metadata', {}).get('total_quotes', 0)
            
            if not evidence_results or total_quotes == 0:
                return "⚠️ **EVIDENCE STATUS**: No evidence quotes found in retrieval results. Proceed with synthesis using only statistical data."
            
            # Build evidence context
            evidence_lines = [
                "🔍 **CURATED EVIDENCE AVAILABLE FOR SYNTHESIS**",
                f"EvidenceRetriever found {total_quotes} relevant quotes across {len(evidence_results)} statistical findings.",
                "",
                "📋 **EVIDENCE CITATION REQUIREMENTS**:",
                "- Every major statistical claim MUST be supported by evidence from the curated evidence below",
                "- Use format: 'As [Speaker] stated: \"[exact quote]\" (Source: [document_name])'",
                "- Include speaker identification and source document for every quote",
                "- Weave evidence quotes naturally into your analysis, not as separate citations",
                "- If no evidence was found for a finding, explicitly state this limitation",
                ""
            ]
            
            # Add curated evidence for each finding
            for i, finding_result in enumerate(evidence_results[:5]):  # Limit to first 5 findings
                finding_desc = finding_result.get('finding', {}).get('description', f'Finding {i+1}')
                quotes = finding_result.get('quotes', [])
                
                evidence_lines.append(f"🔍 **Finding {i+1}: {finding_desc}**")
                if quotes:
                    evidence_lines.append(f"✅ Evidence found: {len(quotes)} pieces")
                    for j, quote in enumerate(quotes[:3]):  # Top 3 quotes per finding
                        quote_text = quote.get('quote_text', 'No quote')
                        if quote_text and quote_text.strip():
                            # Truncate long quotes for readability
                            display_quote = quote_text[:200] + ('...' if len(quote_text) > 200 else '')
                            evidence_lines.append(f"  📝 Quote {j+1}: \"{display_quote}\"")
                            evidence_lines.append(f"     Source: {quote.get('document_name', 'Unknown')} | Dimension: {quote.get('dimension', 'Unknown')} | Confidence: {quote.get('confidence', 0.0):.2f}")
                        else:
                            evidence_lines.append(f"  ⚠️ Quote {j+1}: No quote text available")
                    evidence_lines.append("")
                else:
                    evidence_lines.append(f"❌ No evidence found for this finding")
                    evidence_lines.append("")
            
            # Add summary and instructions
            evidence_lines.append(f"📈 **EVIDENCE SUMMARY**: {total_quotes} total evidence pieces available for synthesis")
            evidence_lines.append("")
            evidence_lines.append("🎯 **CRITICAL REQUIREMENTS FOR SYNTHESIS**:")
            evidence_lines.append("1. **Mandatory Evidence Integration**: Every major statistical claim MUST cite evidence from above")
            evidence_lines.append("2. **Proper Attribution**: Use exact format: 'As [Speaker] stated: \"[quote]\" (Source: [document_name])'")
            evidence_lines.append("3. **Substantial Quotes**: Include full sentences, not fragments")
            evidence_lines.append("4. **Quality Check**: Every Results paragraph should contain at least one direct quote")
            evidence_lines.append("5. **Transparency**: If evidence is weak, acknowledge it but still cite it")
            evidence_lines.append("")
            evidence_lines.append("🚀 **PROCEED TO SYNTHESIS**: Use the curated evidence above to ground your statistical interpretations in textual reality.")
            
            return "\n".join(evidence_lines)
            
        except Exception as e:
            if self.audit_logger:
                self.audit_logger.log_agent_event(self.agent_name, "evidence_context_preparation_failed", {
                    "error": str(e),
                    "evidence_hash": evidence_retrieval_results_hash
                })
            return f"⚠️ **EVIDENCE STATUS**: Error loading evidence retrieval results: {str(e)}. Proceed with synthesis using only statistical data."
    
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
