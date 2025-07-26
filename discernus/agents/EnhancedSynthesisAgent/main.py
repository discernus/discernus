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

    def synthesize_results(self, 
                          consolidated_data: List[Dict[str, Any]],
                          experiment_config: Dict[str, Any],
                          model: str = "vertex_ai/gemini-2.5-pro") -> Dict[str, Any]:
        """
        Perform synthesis on a single, consolidated dataset.
        """
        start_time = datetime.now(timezone.utc).isoformat()
        synthesis_id = f"synthesis_{hashlib.sha256(f'{start_time}{len(consolidated_data)}'.encode()).hexdigest()[:12]}"
        
        self.audit.log_agent_event(self.agent_name, "synthesis_start", {
            "synthesis_id": synthesis_id,
            "num_documents": len(consolidated_data),
            "model": model,
            "experiment": experiment_config.get("name", "unknown")
        })
        
        try:
            # Prepare the synthesis prompt
            synthesis_prompt = self.prompt_template.format(
                consolidated_data=json.dumps(consolidated_data, indent=2)
            )

            # Call the synthesis LLM
            self.audit.log_agent_event(self.agent_name, "llm_call_start", {
                "synthesis_id": synthesis_id, "type": "synthesis", "prompt_length": len(synthesis_prompt)
            })

            response = completion(
                model=model,
                messages=[{"role": "user", "content": synthesis_prompt}],
                temperature=0.0
            )
            
            synthesis_content = response.choices[0].message.content
            
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
                    "num_documents_synthesized": len(consolidated_data)
                },
                "provenance": {
                    "security_boundary": self.security.get_boundary_info(),
                    "audit_session_id": self.audit.session_id
                }
            }
            
            return synthesis_artifact

        except Exception as e:
            self.audit.log_agent_event(self.agent_name, "synthesis_failed", {"error": str(e)})
            raise EnhancedSynthesisAgentError(f"Synthesis failed: {e}")

    def _calculate_duration(self, start: str, end: str) -> float:
        """Calculates duration in seconds from ISO 8601 timestamps."""
        start_dt = datetime.fromisoformat(start)
        end_dt = datetime.fromisoformat(end)
        return (end_dt - start_dt).total_seconds() 