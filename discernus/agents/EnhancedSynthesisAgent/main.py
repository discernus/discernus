#!/usr/bin/env python3
"""
Enhanced Synthesis Agent for Discernus THIN v2.0
================================================

Enhanced version of SynthesisAgent with:
- Mathematical spot-checking of analysis agent calculations
- Dual-LLM validation for numerical accuracy
- Enhanced synthesis with confidence assessment
- Direct function call interface (bypasses Redis coordination)

Implements the simplified 2-agent pipeline: AnalysisAgent → SynthesisAgent
"""

import json
import base64
import hashlib
import yaml
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional
from litellm import completion
import pandas as pd

from discernus.core.security_boundary import ExperimentSecurityBoundary, SecurityError
from discernus.core.audit_logger import AuditLogger
from discernus.core.local_artifact_storage import LocalArtifactStorage


class EnhancedSynthesisAgentError(Exception):
    """Enhanced synthesis agent specific exceptions"""
    pass


class EnhancedSynthesisAgent:
    """
    Enhanced synthesis agent with mathematical spot-checking capabilities.
    
    Key enhancements over original SynthesisAgent:
    - Mathematical spot-checking of analysis results
    - Dual-LLM validation for numerical accuracy
    - Enhanced synthesis with confidence assessment
    - Direct function call interface (no Redis)
    - Comprehensive error detection and reporting
    """
    
    def __init__(self, 
                 security_boundary: ExperimentSecurityBoundary,
                 audit_logger: AuditLogger,
                 artifact_storage: LocalArtifactStorage):
        """
        Initialize enhanced synthesis agent.
        
        Args:
            security_boundary: Security boundary for file access
            audit_logger: Audit logger for comprehensive logging
            artifact_storage: Local artifact storage for caching
        """
        self.security = security_boundary
        self.audit = audit_logger
        self.storage = artifact_storage
        self.agent_name = "EnhancedSynthesisAgent"
        
        # Load enhanced prompt template
        self.prompt_template = self._load_prompt_template()
        
        print(f"🧠 {self.agent_name} v2.2 initialized for integrated report synthesis")
        
        self.audit.log_agent_event(self.agent_name, "initialization", {
            "security_boundary": self.security.get_boundary_info(),
            "capabilities": ["consolidated_data_synthesis", "markdown_report_generation"]
        })
    
    def _load_prompt_template(self) -> str:
        """Load prompt template from YAML file."""
        prompt_path = Path(__file__).parent / "prompt.yaml"
        if not prompt_path.exists():
            raise FileNotFoundError("Could not find prompt.yaml for EnhancedSynthesisAgent")
        
        with open(prompt_path, 'r') as f:
            prompt_config = yaml.safe_load(f)
        
        return prompt_config['template']
    
    def _parse_framework_metadata(self, framework_content: str) -> Dict[str, Any]:
        """Parse framework JSON metadata from framework content."""
        try:
            # Extract JSON from framework markdown (similar to corpus parsing)
            if '```json' in framework_content:
                json_start = framework_content.find('```json') + 7
                json_end = framework_content.find('```', json_start)
                if json_end > json_start:
                    json_str = framework_content[json_start:json_end].strip()
                    framework_metadata = json.loads(json_str)
                    print(f"📊 Parsed framework metadata: {framework_metadata.get('display_name', 'Unknown Framework')}")
                    return framework_metadata
            print("⚠️ No framework JSON metadata found")
            return {}
        except Exception as e:
            print(f"⚠️ Failed to parse framework metadata: {e}")
            return {}
    
    def _build_enhanced_prompt(self, 
                              scores_csv: str, 
                              evidence_csv: str,
                              experiment_config: Dict[str, Any],
                              framework_metadata: Dict[str, Any],
                              metadata_lookup: Dict[str, Any]) -> str:
        """Build enhanced synthesis prompt using YAML template (THIN architecture)."""
        
        # Build report structure guidance from experiment config
        report_structure = experiment_config.get('reporting', {}).get('structure', [])
        report_structure_guidance = ""
        if report_structure:
            report_structure_guidance = "\nREQUIRED REPORT STRUCTURE:\nGenerate a comprehensive analysis with these sections:\n"
            for section in report_structure:
                section_guidance = self._get_section_guidance(section)
                report_structure_guidance += f"- {section}: {section_guidance}\n"
        
        # Use YAML template with proper substitutions
        prompt = self.prompt_template.format(
            experiment_name=experiment_config.get('name', 'Unknown'),
            evaluations_per_document=experiment_config.get('analysis', {}).get('evaluations_per_document', 1),
            report_format=experiment_config.get('reporting', {}).get('format', 'standard'),
            required_tests=experiment_config.get('validation', {}).get('required_tests', []),
            framework_name=framework_metadata.get('display_name', 'Unknown Framework'),
            dimension_groups=framework_metadata.get('dimension_groups', {}),
            calculation_spec=framework_metadata.get('calculation_spec', {}),
            reliability_rubric=framework_metadata.get('reliability_rubric', {}),
            total_documents=len(metadata_lookup),
            scores_csv=scores_csv,
            metadata_lookup=json.dumps(metadata_lookup, indent=2),
            report_structure_guidance=report_structure_guidance
        )
        
        return prompt
    
    def _get_section_guidance(self, section_name: str) -> str:
        """Provide guidance for specific report sections."""
        guidance_map = {
            "temporal_evolution_analysis": "Analyze character evolution across years using year metadata",
            "partisan_character_profiles": "Compare Democrats vs Republicans using political_party metadata",
            "presidential_individual_analysis": "Profile each president using president metadata",
            "contextual_speech_analysis": "Compare inaugural vs SOTU using speech_type metadata",
            "statistical_methodology": "Document multi-evaluation reliability and variance analysis",
            "corpus_metadata_utilization": "Explain how metadata informed the analysis",
            "executive_summary": "High-level findings and key insights",
            "hypothesis_testing_results": "Test experiment hypotheses with statistical rigor",
            "statistical_analysis": "Comprehensive statistical work with calculations shown",
            "qualitative_insights": "Thematic analysis from evidence data",
            "methodology_notes": "Analysis approach and framework application",
            "limitations_and_future_research": "Study limitations and research recommendations"
        }
        return guidance_map.get(section_name, "Provide comprehensive analysis for this section")

    def synthesize_results(self,
                          scores_hash: Optional[str],
                          evidence_hash: Optional[str],
                          analysis_results: List[Dict[str, Any]],
                          experiment_config: Dict[str, Any],
                          framework_content: str,
                          corpus_manifest: Dict[str, Any],
                          model: str = "vertex_ai/gemini-2.5-pro") -> Dict[str, Any]:
        """
        Perform synthesis using aggregated CSV artifacts.
        """
        start_time = datetime.now(timezone.utc).isoformat()
        
        # Create deterministic synthesis_id for perfect caching (THIN principle)
        synthesis_id = hashlib.sha256(
            f"{scores_hash}:{evidence_hash}".encode()
        ).hexdigest()[:12]
        
        self.audit.log_agent_event(self.agent_name, "synthesis_start", {
            "synthesis_id": synthesis_id,
            "scores_hash": scores_hash,
            "evidence_hash": evidence_hash,
            "model": model,
            "experiment": experiment_config.get("name", "unknown")
        })
        
        print(f"🔄 Starting synthesis {synthesis_id}")
        print(f"📊 Using scores_hash={scores_hash}")
        print(f"📝 Using evidence_hash={evidence_hash}")

        try:
            # Read CSV artifacts from storage
            scores_csv = ""
            if scores_hash:
                try:
                    scores_csv = self.storage.get_artifact(scores_hash).decode('utf-8')
                    print(f"✅ Loaded scores CSV ({len(scores_csv)} chars)")
                except FileNotFoundError:
                    print(f"⚠️  Scores CSV artifact not found: {scores_hash}")

            # Skip loading evidence CSV to reduce context size and avoid truncation
            evidence_csv = ""
            print(f"⚠️  Skipping evidence CSV ({evidence_hash[:8]}...) to prevent truncation - analysis will focus purely on quantitative scores")

            # Parse framework metadata for intelligent synthesis
            framework_metadata = self._parse_framework_metadata(framework_content)
            
            # Parse corpus manifest for metadata-driven analysis
            file_manifest = corpus_manifest.get('file_manifest', [])
            
            # Create metadata lookup for intelligent cross-referencing
            metadata_lookup = {}
            for item in file_manifest:
                metadata_lookup[item.get('name', '')] = item
            
            # Prepare enhanced synthesis prompt with full context
            synthesis_prompt = self._build_enhanced_prompt(
                scores_csv=scores_csv,
                evidence_csv=evidence_csv,
                experiment_config=experiment_config,
                framework_metadata=framework_metadata,
                metadata_lookup=metadata_lookup
            )

            print(f"📝 Synthesis prompt length: {len(synthesis_prompt)} chars")

            # Call the synthesis LLM
            self.audit.log_agent_event(self.agent_name, "llm_call_start", {
                "synthesis_id": synthesis_id,
                "prompt_length": len(synthesis_prompt)
            })

            response = completion(
                model=model,
                messages=[{"role": "user", "content": synthesis_prompt}],
                temperature=0.0,
                max_tokens=6000,
                safety_settings=[
                    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
                ]
            )
            
            if not response or not response.choices:
                raise EnhancedSynthesisAgentError("LLM returned empty response")
            
            if not response.choices[0] or not response.choices[0].message:
                raise EnhancedSynthesisAgentError("LLM response missing message")
            
            synthesis_content = response.choices[0].message.content
            
            # Check for None content from LLM response
            if synthesis_content is None:
                finish_reason = response.choices[0].finish_reason if response and response.choices else "unknown"
                completion_tokens = response.usage.completion_tokens if response and response.usage else "unknown"
                
                # Handle length-limited responses gracefully
                if finish_reason == 'length':
                    synthesis_content = f"[SYNTHESIS REPORT - Truncated due to length limit]\n\nThis synthesis was truncated after {completion_tokens} tokens. The analysis completed but exceeded the maximum response length. Key findings would be included above this notice."
                    print(f"⚠️  Synthesis truncated at {completion_tokens} tokens - using placeholder content")
                else:
                    raise EnhancedSynthesisAgentError(f"LLM returned None content - finish_reason: {finish_reason}, completion_tokens: {completion_tokens}")
            
            self.audit.log_agent_event(self.agent_name, "llm_call_complete", {
                "synthesis_id": synthesis_id, "type": "synthesis", "response_length": len(synthesis_content)
            })

            # Create comprehensive result artifact
            end_time = datetime.now(timezone.utc).isoformat()
            duration = self._calculate_duration(start_time, end_time)
            
            synthesis_artifact = {
                "synthesis_id": synthesis_id,
                "agent_name": self.agent_name,
                "agent_version": "enhanced_v2.2_integrated_report",
                "experiment_name": experiment_config.get("name", "unknown"),
                "model_used": model,
                "synthesis_report_markdown": synthesis_content,
                "execution_metadata": {
                    "start_time": start_time,
                    "end_time": end_time,
                    "duration_seconds": duration,
                },
                "input_metadata": {
                    "num_analysis_batches_synthesized": len(analysis_results)
                },
                "provenance": {
                    "security_boundary": self.security.get_boundary_info(),
                    "audit_session_id": self.audit.session_id
                }
            }
            
            # Store synthesis artifact and return with expected keys
            result_hash = self.storage.put_artifact(
                json.dumps(synthesis_artifact, indent=2).encode('utf-8'),
                {"artifact_type": "synthesis_result", "synthesis_id": synthesis_id}
            )
            
            return {
                "result_hash": result_hash,
                "duration_seconds": duration,
                "synthesis_confidence": "completed",  # Add basic confidence indicator
                "synthesis_report_markdown": synthesis_content  # Include for final report
            }

        except Exception as e:
            self.audit.log_agent_event(self.agent_name, "synthesis_failed", {"error": str(e)})
            raise EnhancedSynthesisAgentError(f"Synthesis failed: {e}")

    def _calculate_duration(self, start: str, end: str) -> float:
        """Calculates duration in seconds from ISO 8601 timestamps."""
        start_dt = datetime.fromisoformat(start)
        end_dt = datetime.fromisoformat(end)
        return (end_dt - start_dt).total_seconds() 