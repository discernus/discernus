"""
AnalysisPlanner Agent: Generates declarative mathematical analysis plans.

This agent analyzes the experiment, framework, and data to produce a structured
JSON plan specifying which mathematical operations to perform, replacing the
fragile code generation approach.
"""

import json
import logging
import yaml
from typing import Dict, Any, Optional
from dataclasses import dataclass
from pathlib import Path

from discernus.core.audit_logger import AuditLogger


@dataclass
class AnalysisPlanRequest:
    """Request for generating an analysis plan."""
    experiment_context: str
    framework_spec: str
    data_summary: str
    available_columns: list
    research_questions: list
    raw_analysis_data: str = ""  # THIN: Raw analysis data for LLM interpretation


@dataclass
class AnalysisPlanResponse:
    """Response containing the generated analysis plan."""
    success: bool
    analysis_plan: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None


class AnalysisPlanner:
    """
    Agent that generates structured analysis plans instead of arbitrary code.
    
    This agent replaces the AnalyticalCodeGenerator by producing declarative
    JSON specifications of mathematical operations to perform.
    """
    
    def __init__(self, model: str = "vertex_ai/gemini-2.5-pro", audit_logger: Optional[AuditLogger] = None):
        """
        Initialize the AnalysisPlanner.
        
        Args:
            model: LLM model to use for analysis planning
            audit_logger: Optional audit logger for provenance
        """
        self.model = model
        self.audit_logger = audit_logger
        
        # Import LLM gateway from main codebase
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))
        from discernus.gateway.llm_gateway import LLMGateway
        from discernus.gateway.model_registry import ModelRegistry
        
        self.model_registry = ModelRegistry()
        self.llm_gateway = LLMGateway(self.model_registry)
        self.logger = logging.getLogger(__name__)
        
    def generate_analysis_plan(self, request: AnalysisPlanRequest) -> AnalysisPlanResponse:
        """
        Generate a structured analysis plan based on the experiment context.
        
        Args:
            request: AnalysisPlanRequest containing experiment context and data
            
        Returns:
            AnalysisPlanResponse with the generated plan or error details
        """
        try:
            self.logger.info("Generating analysis plan for experiment")
            
            # Log the request for audit purposes
            if self.audit_logger:
                self.audit_logger.log_agent_event(
                    "AnalysisPlanner",
                    "generate_analysis_plan",
                    {
                        "experiment_context_length": len(request.experiment_context),
                        "framework_spec_length": len(request.framework_spec),
                        "data_summary_length": len(request.data_summary),
                        "raw_analysis_data_length": len(request.raw_analysis_data),
                        "research_questions_count": len(request.research_questions),
                        "approach": "thin_raw_data_interpretation"
                    }
                )
            
            # Build the prompt
            prompt = self._build_analysis_plan_prompt(request)
            
            # Generate the analysis plan using enforced JSON mode
            response, metadata = self.llm_gateway.execute_call(
                model=self.model,
                prompt=prompt,
                system_prompt="You are an expert research analyst. Always respond with valid JSON only.",
                response_format={"type": "json_object"},  # Enforce JSON output
                temperature=0.1  # Low temperature for consistent, structured output
            )
            
            if not response or not response.strip():
                return AnalysisPlanResponse(
                    success=False,
                    error_message="Empty response from LLM"
                )
            
            # Parse the JSON response
            try:
                analysis_plan = json.loads(response)
            except json.JSONDecodeError as e:
                self.logger.error(f"Failed to parse JSON response: {e}")
                self.logger.error(f"Raw response: {response}")
                return AnalysisPlanResponse(
                    success=False,
                    error_message=f"Invalid JSON response: {str(e)}"
                )
            
            # Validate the analysis plan structure
            validation_result = self._validate_analysis_plan(analysis_plan)
            if not validation_result["valid"]:
                return AnalysisPlanResponse(
                    success=False,
                    error_message=f"Invalid analysis plan: {validation_result['error']}"
                )
            
            self.logger.info(f"Successfully generated analysis plan with {len(analysis_plan.get('tasks', {}))} tasks")
            
            return AnalysisPlanResponse(
                success=True,
                analysis_plan=analysis_plan
            )
            
        except Exception as e:
            self.logger.error(f"Error generating analysis plan: {str(e)}")
            return AnalysisPlanResponse(
                success=False,
                error_message=f"Analysis plan generation failed: {str(e)}"
            )
    
    def _load_quantitative_grammar(self) -> str:
        """
        Load the quantitative grammar specification.
        
        Returns:
            YAML content as string
        """
        try:
            grammar_path = Path(__file__).parent.parent.parent.parent / "core" / "quantitative_grammar.yaml"
            with open(grammar_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            self.logger.warning(f"Could not load quantitative grammar: {e}")
            return ""
    
    def _build_analysis_plan_prompt(self, request: AnalysisPlanRequest) -> str:
        """
        Build the prompt for generating an analysis plan.
        
        Args:
            request: The analysis plan request
            
        Returns:
            Formatted prompt string
        """
        # Load quantitative grammar for standardized keys
        grammar_spec = self._load_quantitative_grammar()
        
        prompt = f"""
You are an expert research analyst tasked with creating a structured mathematical analysis plan for a political discourse analysis experiment.

## EXPERIMENT CONTEXT
{request.experiment_context}

## FRAMEWORK SPECIFICATION
{request.framework_spec}

## DATA SUMMARY
{request.data_summary}

## RAW ANALYSIS DATA (THIN APPROACH)
{request.raw_analysis_data[:2000]}{"..." if len(request.raw_analysis_data) > 2000 else ""}

## RESEARCH QUESTIONS
{chr(10).join(f"- {q}" for q in request.research_questions)}

## QUANTITATIVE GRAMMAR - STANDARDIZED SEMANTIC KEYS
Use these standardized semantic categories for task names to ensure interface compatibility:

{grammar_spec}

**CRITICAL**: Your task names must use semantic keys from the grammar above (e.g., "descriptive_stats", "correlations", "reliability", "variance_analysis") rather than numbered task names like "01_descriptive_statistics_scores".

## THIN APPROACH: DATA INTERPRETATION
**You are provided with raw analysis data above. Your task is to:**
1. **Interpret the JSON structure** to understand available dimensions and data
2. **Identify available columns** from the raw data structure - look for patterns like:
   - Score columns: `dimension_score`, `dimension_raw_score` (e.g., `dignity_score`, `dignity_raw_score`)
   - Classification columns: `category_classification_classification` (e.g., `era_classification_classification`)
   - Metadata columns: `field_salience`, `field_confidence`, `field_justification`
   
   **CRITICAL**: All column names use UNDERSCORES, never dots. The DataFrame columns will be:
   - `dignity_score`, `dignity_raw_score`, `dignity_salience`, `dignity_confidence`
   - `era_classification_classification`, `ideology_classification_classification`
   - NOT `dignity.score` or `era_classification.classification`
3. **Extract grouping variables** from classification fields:
   - For grouping by era: use `era_classification_classification` column
   - For grouping by ideology: use `ideology_classification_classification` column
   - Do NOT assume simplified column names like `era` or `ideology` exist
4. **Create analysis plan** using ONLY the actual column names you see in the raw data
5. **Use semantic keys** from the quantitative grammar for task names

**CRITICAL**: Your analysis plan must reference the EXACT column names present in the data structure. Do not assume or create simplified column names.

## TASK
Analyze the experiment context, framework, and research questions to create a comprehensive analysis plan. Your plan should specify exactly which mathematical operations to perform to answer the research questions using ONLY the available columns.

## AVAILABLE MATHEMATICAL TOOLS
You have access to these pre-built, tested mathematical functions:

1. **calculate_descriptive_stats**: Calculate mean, std, min, max, median, quartiles, skewness, kurtosis
   - Parameters: columns (list of column names), grouping_variable (optional)

2. **perform_independent_t_test**: Compare two groups on a dependent variable
   - Parameters: grouping_variable, dependent_variable, group1 (optional), group2 (optional)

3. **calculate_pearson_correlation**: Calculate Pearson correlation matrix
   - Parameters: columns (list of column names)

4. **perform_one_way_anova**: Test for differences between multiple groups
   - Parameters: grouping_variable, dependent_variable

5. **calculate_effect_sizes**: Calculate effect sizes (eta-squared) for group differences
   - Parameters: grouping_variable, dependent_variable

**IMPORTANT**: Use these EXACT tool names in your analysis plan. Do not use simplified names like "descriptive_stats" - use the full function name like "calculate_descriptive_stats".

## OUTPUT FORMAT
You must output a valid JSON object with this exact structure:

{{
  "experiment_summary": "Brief description of what this analysis will accomplish",
  "tasks": {{
    "task_name_1": {{
      "tool": "tool_name",
      "parameters": {{
        "param1": "value1",
        "param2": "value2"
      }},
      "purpose": "Why this analysis is needed"
    }},
    "task_name_2": {{
      "tool": "tool_name",
      "parameters": {{
        "param1": "value1"
      }},
      "purpose": "Why this analysis is needed"
    }}
  }}
}}

## REQUIREMENTS
1. Use only the available tools listed above
2. Use actual column names from the available columns list
3. **Use standardized semantic keys from the quantitative grammar** for task names (e.g., "descriptive_stats", "correlations", "reliability")
4. Create a comprehensive plan that addresses all research questions
5. Include descriptive statistics for all relevant variables
6. Include appropriate statistical tests based on the experimental design
7. Ensure all parameter values are valid for the given data structure
8. Output only valid JSON - no markdown formatting, no explanations outside the JSON

Generate your analysis plan now:
"""
        return prompt
    
    def _validate_analysis_plan(self, analysis_plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate the structure and content of an analysis plan.
        
        Args:
            analysis_plan: The analysis plan to validate
            
        Returns:
            Dictionary with validation result
        """
        try:
            # Check required top-level keys
            if "experiment_summary" not in analysis_plan:
                return {"valid": False, "error": "Missing 'experiment_summary'"}
            
            if "tasks" not in analysis_plan:
                return {"valid": False, "error": "Missing 'tasks'"}
            
            # Validate tasks structure
            tasks = analysis_plan["tasks"]
            if not isinstance(tasks, dict):
                return {"valid": False, "error": "'tasks' must be a dictionary"}
            
            if len(tasks) == 0:
                return {"valid": False, "error": "No tasks specified"}
            
            # Validate each task
            available_tools = {
                "calculate_descriptive_stats", "perform_independent_t_test", "calculate_pearson_correlation",
                "perform_one_way_anova", "calculate_effect_sizes"
            }
            
            for task_name, task_config in tasks.items():
                if not isinstance(task_config, dict):
                    return {"valid": False, "error": f"Task '{task_name}' must be a dictionary"}
                
                if "tool" not in task_config:
                    return {"valid": False, "error": f"Task '{task_name}' missing 'tool'"}
                
                if "parameters" not in task_config:
                    return {"valid": False, "error": f"Task '{task_name}' missing 'parameters'"}
                
                if "purpose" not in task_config:
                    return {"valid": False, "error": f"Task '{task_name}' missing 'purpose'"}
                
                tool = task_config["tool"]
                if tool not in available_tools:
                    return {"valid": False, "error": f"Task '{task_name}' uses unknown tool '{tool}'"}
                
                if not isinstance(task_config["parameters"], dict):
                    return {"valid": False, "error": f"Task '{task_name}' parameters must be a dictionary"}
            
            return {"valid": True}
            
        except Exception as e:
            return {"valid": False, "error": f"Validation error: {str(e)}"} 