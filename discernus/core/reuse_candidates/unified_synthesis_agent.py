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
                            evidence_artifact_hashes: List[str],
                            artifact_storage) -> Dict[str, Any]:
        """
        Generate complete, publication-ready research report.
        
        Args:
            framework_path: Path to framework specification
            experiment_path: Path to experiment specification  
            research_data_artifact_hash: Hash of complete research data
            evidence_artifact_hashes: List of evidence artifact hashes
            artifact_storage: Storage instance for artifact retrieval
            
        Returns:
            Dictionary containing final report and metadata
        """
        if self.audit_logger:
            self.audit_logger.log_agent_event(self.agent_name, "synthesis_start", {
                "framework": str(framework_path),
                "experiment": str(experiment_path),
                "evidence_artifacts": len(evidence_artifact_hashes)
            })
        
        try:
            # Choose synthesis approach based on mode
            if self.enhanced_mode:
                # Enhanced multi-level analysis approach
                final_report = self._generate_enhanced_report(
                    framework_path, experiment_path, research_data_artifact_hash, 
                    evidence_artifact_hashes, artifact_storage
                )
            else:
                # Legacy synthesis approach
                assembler = SynthesisPromptAssembler()
                synthesis_prompt = assembler.assemble_prompt(
                    framework_path=framework_path,
                    experiment_path=experiment_path,
                    research_data_artifact_hash=research_data_artifact_hash,
                    artifact_storage=artifact_storage,
                    evidence_artifacts=evidence_artifact_hashes
                )
                
                evidence_context = self._prepare_evidence_context(evidence_artifact_hashes, artifact_storage)
                enhanced_prompt = f"""{synthesis_prompt}

AVAILABLE EVIDENCE FOR CITATION:
{evidence_context}

Use this evidence to support your statistical interpretations. Quote directly from the evidence above with proper attribution."""
                
                final_report = self._generate_report_with_evidence_integration(enhanced_prompt)
            
            # 4. Validate report quality
            quality_metrics = self._validate_report_quality(final_report)
            
            if self.audit_logger:
                self.audit_logger.log_agent_event(self.agent_name, "synthesis_complete", {
                    "report_length": len(final_report),
                    "quality_metrics": quality_metrics
                })
            
            return {
                "final_report": final_report,
                "quality_metrics": quality_metrics,
                "model_used": self.model,
                "evidence_pieces_indexed": len(self._get_all_evidence(evidence_artifact_hashes, artifact_storage))
            }
            
        except Exception as e:
            if self.audit_logger:
                self.audit_logger.log_agent_event(self.agent_name, "synthesis_failed", {
                    "error": str(e)
                })
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
        
        # 4. Assemble enhanced prompt
        enhanced_prompt = self.enhanced_prompt_template['template'].format(
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
        """Prepare evidence context for direct embedding in synthesis prompt."""
        all_evidence = self._get_all_evidence(evidence_artifact_hashes, artifact_storage)
        
        if not all_evidence:
            return "No evidence available for citation."
        
        evidence_lines = []
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
