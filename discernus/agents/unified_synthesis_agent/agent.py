#!/usr/bin/env python3
"""
Unified Synthesis Agent for Discernus v10
=========================================

Generates publication-ready research reports using:
- Complete research data (raw scores, derived metrics, statistical results)
- Curated evidence from EvidenceRetriever
- THIN prompting approach with gemini-2.5-pro for reliability

Pure synthesis agent - no external lookups or RAG queries.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional

from ...gateway.llm_gateway_enhanced import EnhancedLLMGateway
from ...gateway.model_registry import ModelRegistry
from ...core.audit_logger import AuditLogger
import yaml


class UnifiedSynthesisAgent:
    """
    Pure synthesis agent for research report generation.
    
    Uses proven THIN approach with curated evidence for evidence-grounded reporting.
    No external lookups or RAG queries - pure synthesis of provided assets.
    """
    
    def __init__(
        self,
        model: str,
        audit_logger: Optional[AuditLogger] = None,
        enhanced_mode: bool = True,
    ):
        """
        Initialize the agent.

        Args:
            model: The language model to use for synthesis.
            audit_logger: An optional audit logger instance.
            enhanced_mode: Whether to use the enhanced prompt template.
        """
        self.model = model
        self.audit_logger = audit_logger
        self.agent_name = "UnifiedSynthesisAgent"
        self.llm_gateway = EnhancedLLMGateway(ModelRegistry())
        self.enhanced_mode = enhanced_mode
        # Model tracking for provenance
        self.analysis_model = None
        self.synthesis_model = model  # This is the synthesis model
        self.prompt_template = (
            self._load_enhanced_prompt_template()
            if enhanced_mode
            else self._load_basic_prompt_template()
        )

    def generate_final_report(
        self,
        assets: Dict[str, Any],
        artifact_storage,
    ) -> Dict[str, Any]:
        """
        Generate the final academic report using static assets only.
        
        Args:
            assets: Dictionary containing all required assets:
                - framework_path: Path to framework specification
                - experiment_path: Path to experiment specification  
                - research_data_artifact_hash: Hash of research data artifact
                - evidence_retrieval_results_hash: Hash of curated evidence (optional)
            artifact_storage: Storage system for retrieving artifacts
            
        Returns:
            Dictionary containing the generated report
        """
        if self.audit_logger:
            self.audit_logger.log_agent_event(
                self.agent_name,
                "synthesis_start",
                {
                    "framework": str(assets.get('framework_path', '')),
                    "experiment": str(assets.get('experiment_path', '')),
                    "research_data_hash": assets.get('research_data_artifact_hash', ''),
                    "evidence_retrieval_hash": assets.get('evidence_retrieval_results_hash', ''),
                },
            )

        try:
            # 1. Load all content directly (THIN approach - no complex parsing)
            framework_content = Path(assets['framework_path']).read_text(encoding='utf-8')
            experiment_content = Path(assets['experiment_path']).read_text(encoding='utf-8')
            
            # 2. Load research data from artifact (THIN approach - direct Python repr)
            research_data_content = artifact_storage.get_artifact(assets['research_data_artifact_hash'])
            research_data_str = research_data_content.decode('utf-8')
            
            # Handle transition from JSON to Python repr format
            try:
                # Try JSON first (current format)
                research_data = json.loads(research_data_str)
            except json.JSONDecodeError:
                # Fallback to Python repr (old format during transition)
                # Preprocess nan values before eval
                research_data_str = research_data_str.replace('nan', 'float("nan")')
                research_data = eval(research_data_str)
            
            # Convert tuple keys to strings for safe repr() serialization
            def convert_tuple_keys_for_repr(obj):
                """Convert tuple keys to strings for safe repr() serialization."""
                if isinstance(obj, dict):
                    converted = {}
                    for k, v in obj.items():
                        if isinstance(k, tuple):
                            converted_key = str(k)
                        else:
                            converted_key = k
                        converted[converted_key] = convert_tuple_keys_for_repr(v)
                    return converted
                elif isinstance(obj, list):
                    return [convert_tuple_keys_for_repr(item) for item in obj]
                elif isinstance(obj, tuple):
                    return tuple(convert_tuple_keys_for_repr(item) for item in obj)
                else:
                    return obj
            
            # Convert tuple keys before calling repr() - apply to entire research_data
            safe_research_data = convert_tuple_keys_for_repr(research_data)
            research_data_repr = repr(safe_research_data)
            
            # 3. Load evidence if available
            evidence_hash = assets.get('evidence_retrieval_results_hash')
            if evidence_hash:
                evidence_content = artifact_storage.get_artifact(evidence_hash)
                evidence_str = evidence_content.decode('utf-8')
                
                # Handle transition from JSON to Python repr format
                try:
                    # Try JSON first (current format)
                    evidence_data = json.loads(evidence_str)
                except json.JSONDecodeError:
                    # Fallback to Python repr (old format during transition)
                    # Preprocess nan values before eval
                    evidence_str = evidence_str.replace('nan', 'float("nan")')
                    evidence_data = eval(evidence_str)
                
                evidence_context = repr(evidence_data)
            else:
                evidence_context = "No curated evidence was available for this synthesis run."
            
            # 4. Load corpus manifest (simple file read)
            corpus_path = Path(assets['experiment_path']).parent / "corpus.md"
            corpus_manifest = corpus_path.read_text(encoding='utf-8') if corpus_path.exists() else "Corpus manifest not available"
            
            # 5. Assemble experiment metadata with model information
            run_id = assets.get('run_id', 'Unknown')
            
            # Extract cost information if available
            costs = assets.get('costs', {})
            total_cost = costs.get('total_cost_usd', 0.0)
            cost_info = f"Total Cost: ${total_cost:.4f} USD" if total_cost > 0 else "Total Cost: Not available"
            
            experiment_metadata = f"""
            Experiment: {Path(assets['experiment_path']).parent.name}
            Run ID: {run_id}
            Framework: {Path(assets['framework_path']).name}
            Analysis Model: {getattr(self, 'analysis_model', 'Unknown')}
            Synthesis Model: {getattr(self, 'synthesis_model', 'Unknown')}
            Document Count: {len(research_data.get('documents', []))}
            {cost_info}
            """

            # 6. Assemble prompt using template (no complex assembler needed)
            base_prompt = self.prompt_template['template'].format(
                experiment_metadata=experiment_metadata,
                framework_content=framework_content,
                experiment_content=experiment_content,
                corpus_manifest=corpus_manifest,
                research_data=f"Complete Statistical Results:\n{research_data_repr}",
                evidence_context=evidence_context
            )

            # 6. Execute the LLM call
            final_report, metadata = self.llm_gateway.execute_call(
                model=self.model, prompt=base_prompt, temperature=0.2, context="Generating comprehensive research report"
            )

            # Log cost information to audit logger
            if self.audit_logger and metadata.get("usage"):
                usage_data = metadata["usage"]
                try:
                    self.audit_logger.log_cost(
                        operation="synthesis_report_generation",
                        model=metadata.get("model", self.model),
                        tokens_used=usage_data.get("total_tokens", 0),
                        cost_usd=usage_data.get("response_cost_usd", 0.0),
                        agent_name=self.agent_name,
                        metadata={
                            "prompt_tokens": usage_data.get("prompt_tokens", 0),
                            "completion_tokens": usage_data.get("completion_tokens", 0),
                            "attempts": metadata.get("attempts", 1),
                            "report_length": len(final_report)
                        }
                    )
                except Exception as e:
                    if hasattr(self, 'logger'):
                        self.logger.error(f"Error logging cost for synthesis: {e}")

            if self.audit_logger:
                self.audit_logger.log_agent_event(
                    self.agent_name, "synthesis_complete", {"report_length": len(final_report)}
                )

            return {"final_report": final_report, "llm_metadata": metadata}

        except Exception as e:
            if self.audit_logger:
                self.audit_logger.log_error(
                    "synthesis_failed", str(e), {"agent": self.agent_name}
                )
            raise

    # RAG-related methods removed - no longer needed for pure synthesis

    # RAG evidence retrieval removed - no longer needed for pure synthesis

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
            prompt_file = Path(__file__).parent / "prompt.yaml"
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
    
    # Enhanced report generation removed - simplified to use SynthesisPromptAssembler
    
    def _generate_report_with_llm(self, prompt: str) -> str:
        """Generate report using LLM with enhanced prompt."""
        try:
            response, metadata = self.llm_gateway.execute_call(
                model=self.model,
                prompt=prompt,
                system_prompt=self.enhanced_prompt_template.get('system_prompt', ''),
                temperature=0.2   # Low temperature for analytical consistency
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
    
    # RAG evidence retrieval removed - no longer needed for pure synthesis
    
    # RAG result formatting removed - no longer needed for pure synthesis
    
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
    
    # Evidence integration method removed - simplified to use main generation method
    
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
