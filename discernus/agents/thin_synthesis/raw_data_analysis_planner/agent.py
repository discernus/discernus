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
    analysis_plan: Optional[Dict[str, Any]] = None
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
            
            if not response or not response.strip():
                return RawDataAnalysisPlanResponse(success=False, error_message="Empty response from LLM")
            
            # Parse JSON response
            try:
                analysis_plan = json.loads(response)
            except json.JSONDecodeError as e:
                self.logger.error(f"Failed to parse JSON response: {e}")
                return RawDataAnalysisPlanResponse(success=False, error_message=f"Invalid JSON: {str(e)}")
            
            # Basic validation
            if not self._validate_plan_structure(analysis_plan):
                return RawDataAnalysisPlanResponse(success=False, error_message="Invalid plan structure")
            
            self.logger.info(f"Generated raw data plan with {len(analysis_plan.get('tasks', {}))} tasks")
            return RawDataAnalysisPlanResponse(success=True, analysis_plan=analysis_plan)
            
        except Exception as e:
            self.logger.error(f"Raw data planning failed: {str(e)}")
            return RawDataAnalysisPlanResponse(success=False, error_message=str(e))
    
    def _validate_plan_structure(self, plan: Dict[str, Any]) -> bool:
        """Basic validation of plan structure."""
        try:
            required_keys = ["stage", "experiment_summary", "tasks"]
            if not all(key in plan for key in required_keys):
                return False
            if plan["stage"] != "raw_data_collection":
                return False
            if not isinstance(plan.get("tasks"), dict) or len(plan["tasks"]) == 0:
                return False
            return True
        except Exception:
            return False 