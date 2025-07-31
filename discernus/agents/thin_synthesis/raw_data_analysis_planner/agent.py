"""
Raw Data Analysis Planner Agent

This agent generates analysis plans focused on collecting raw data only.
It follows the THIN principle by letting LLMs interpret framework requirements
and generate plans without parsing or custom data structures.
"""

import json
import logging
import yaml
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any, Optional, List

from discernus.gateway.llm_gateway import LLMGateway
from discernus.gateway.model_registry import ModelRegistry
from discernus.core.audit_logger import AuditLogger


@dataclass
class RawDataAnalysisPlanRequest:
    """Request for generating a raw data analysis plan."""
    experiment_context: str
    framework_spec: str
    corpus_manifest: str
    research_questions: List[str]


@dataclass
class RawDataAnalysisPlanResponse:
    """Response containing the generated raw data analysis plan."""
    success: bool
    analysis_plan: Optional[Dict[str, Any]] = None  # Deprecated: Use raw_llm_response
    raw_llm_response: Optional[str] = None  # THIN: Raw LLM response
    error_message: Optional[str] = None


class RawDataAnalysisPlanner:
    """Agent that generates structured analysis plans for raw data collection only."""
    
    def __init__(self, model: str = "vertex_ai/gemini-2.5-pro", audit_logger: Optional[AuditLogger] = None):
        self.model = model
        self.audit_logger = audit_logger
        self.model_registry = ModelRegistry()
        self.llm_gateway = LLMGateway(self.model_registry)
        self.logger = logging.getLogger(__name__)
        self._load_prompt()
        
    def _load_prompt(self):
        """Load the prompt template from YAML file."""
        prompt_path = Path(__file__).parent / "prompts" / "raw_data_planning.yaml"
        with open(prompt_path, 'r') as f:
            self.prompt_config = yaml.safe_load(f)
        
    def generate_raw_data_plan(self, request: RawDataAnalysisPlanRequest) -> RawDataAnalysisPlanResponse:
        """Generate a structured analysis plan for raw data collection only."""
        try:
            self.logger.info("Generating raw data analysis plan")
            
            if self.audit_logger:
                self.audit_logger.log_agent_event(
                    "RawDataAnalysisPlanner",
                    "generate_raw_data_plan",
                    {
                        "experiment_context_length": len(request.experiment_context),
                        "framework_spec_length": len(request.framework_spec),
                        "research_questions_count": len(request.research_questions),
                        "approach": "thin_raw_data_planning"
                    }
                )
            
            # Build prompt from template
            prompt = self.prompt_config["user_prompt_template"].format(
                experiment_context=request.experiment_context,
                framework_spec=request.framework_spec,
                corpus_manifest=request.corpus_manifest,
                research_questions="\n".join(f"- {q}" for q in request.research_questions)
            )
            
            # Generate plan using LLM
            response, metadata = self.llm_gateway.execute_call(
                model=self.model,
                prompt=prompt,
                system_prompt=self.prompt_config["system_prompt"],
                response_format=self.prompt_config["parameters"]["response_format"],
                temperature=self.prompt_config["parameters"]["temperature"]
            )
            
            # Extract and log cost information
            if self.audit_logger and metadata.get("usage"):
                usage_data = metadata["usage"]
                try:
                    self.audit_logger.log_cost(
                        operation="raw_data_analysis_planning",
                        model=metadata.get("model", self.model),
                        tokens_used=usage_data.get("total_tokens", 0),
                        cost_usd=usage_data.get("response_cost_usd", 0.0),
                        agent_name="RawDataAnalysisPlanner",
                        metadata={
                            "prompt_tokens": usage_data.get("prompt_tokens", 0),
                            "completion_tokens": usage_data.get("completion_tokens", 0),
                            "attempts": metadata.get("attempts", 1)
                        }
                    )
                    cost = usage_data.get("response_cost_usd", 0.0)
                    tokens = usage_data.get("total_tokens", 0)
                    print(f"💰 Raw data planning cost: ${cost:.6f} ({tokens:,} tokens)")
                except Exception as e:
                    print(f"⚠️ Error logging cost for raw data planning: {e}")
            
            if not response or not response.strip():
                return RawDataAnalysisPlanResponse(success=False, error_message="Empty response from LLM")
            
            # THIN approach: Pass raw LLM response, let downstream components handle parsing
            self.logger.info(f"Generated raw data plan ({len(response)} chars) - THIN approach")
            return RawDataAnalysisPlanResponse(success=True, raw_llm_response=response)
            
        except Exception as e:
            self.logger.error(f"Raw data planning failed: {str(e)}")
            return RawDataAnalysisPlanResponse(success=False, error_message=str(e))
    
    # REMOVED: _validate_plan_structure - THICK software validation of LLM intelligence
    # THIN principle: Trust LLM to generate valid plans, handle errors gracefully downstream 