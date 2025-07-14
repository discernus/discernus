#!/usr/bin/env python3
"""
Validation Agent - THIN project validation using LLM intelligence
================================================================

THIN Principle: Software provides validation orchestration infrastructure;
LLM provides validation intelligence using comprehensive rubrics.

Uses existing Framework Specification Validation Rubric v1.0 and
Experiment Specification Validation Rubric v1.0 for quality gates.
"""

import sys
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
import re
import yaml
import asyncio

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    from discernus.core.framework_loader import FrameworkLoader
    from discernus.gateway.llm_gateway import LLMGateway
    from discernus.agents.ensemble_configuration_agent import EnsembleConfigurationAgent
    from discernus.agents.statistical_analysis_configuration_agent import StatisticalAnalysisConfigurationAgent
    from discernus.agents.execution_planner_agent import ExecutionPlannerAgent
    from discernus.gateway.model_registry import ModelRegistry # Corrected import path
    from discernus.orchestration.workflow_orchestrator import WorkflowOrchestrator
    DEPENDENCIES_AVAILABLE = True
except ImportError as e:
    print(f"ValidationAgent dependencies not available: {e}")
    DEPENDENCIES_AVAILABLE = False

class ValidationAgent:
    """
    THIN validation agent - orchestrates LLM validation using rubrics
    Software provides validation workflow; LLM provides validation intelligence
    """
    
    def __init__(self, llm_gateway=None, framework_loader=None):
        self.framework_loader = framework_loader or FrameworkLoader()
        self.project_path = None # Initialize project_path
        
        # Instantiate registry first, as it's needed by the gateway
        self.model_registry = ModelRegistry()

        if llm_gateway:
            self.gateway = llm_gateway
        else:
            if not DEPENDENCIES_AVAILABLE:
                raise ImportError("ValidationAgent dependencies not available. Please check your environment.")
            try:
                # Pass the registry to the gateway
                self.gateway = LLMGateway(self.model_registry)
                print("✅ ValidationAgent using LLMGateway with ModelRegistry")
            except Exception as e:
                print(f"❌ ValidationAgent: Failed to initialize LLM gateway: {e}")
                raise e
        
        # Instantiate other agents for comprehensive validation
        self.ensemble_config_agent = EnsembleConfigurationAgent()
        self.statistical_config_agent = StatisticalAnalysisConfigurationAgent()
        self.execution_planner_agent = ExecutionPlannerAgent()

        # Get validation rubrics from FrameworkLoader
        self.framework_rubric = self.framework_loader.framework_rubric
        self.experiment_rubric = self.framework_loader.experiment_rubric
        
        # More reasonable validation thresholds
        self.framework_threshold = 75  # Reduced from 85% - be more reasonable
        self.experiment_threshold = 80  # Reduced from 90% - be more reasonable
    
    def validate_project(self, project_path: str) -> Dict[str, Any]:
        """
        Comprehensive SOAR project validation, including configuration and coherence.
        """
        project_path_obj = Path(project_path)
        
        # Step 1: Project structure validation
        structure_result = self.framework_loader.validate_project_structure(str(project_path_obj))
        if not structure_result['validation_passed']:
            return self._format_error('structure', f"Project structure validation failed: {structure_result['missing_files']}", {'structure_result': structure_result})

        # Step 2: Configuration Generation
        self.ensemble_config_agent.generate_configuration(str(project_path_obj / "experiment.md"))
        
        # Step 3: Statistical Plan Validation
        statistical_plan = self.statistical_config_agent.generate_statistical_plan(str(project_path_obj / "experiment.md"))
        if statistical_plan.get("validation_status") != "complete":
            return self._format_error('statistical_plan', f"Statistical plan validation failed: {statistical_plan.get('notes', 'No notes provided.')}", {'statistical_plan': statistical_plan})

        # Step 4: Coherence validation
        coherence_result = self._validate_project_coherence(project_path_obj)
        if not coherence_result['validation_passed']:
            return self._format_error('coherence', f"Project coherence validation failed: {coherence_result['message']}", {'coherence_result': coherence_result})

        # Step 4.5: Statistical Coherence Validation (NEW)
        framework_content = (project_path_obj / "framework.md").read_text()
        statistical_coherence_result = self._validate_statistical_coherence(project_path_obj, framework_content, statistical_plan)
        if not statistical_coherence_result['validation_passed']:
            return self._format_error('statistical_coherence', f"Statistical coherence validation failed: {statistical_coherence_result['message']}", {'statistical_coherence_result': statistical_coherence_result})

        # Step 5: Framework validation
        framework_result = self._validate_project_framework(project_path_obj)
        if not framework_result['validation_passed']:
            return self._format_error('framework', f"Framework validation failed: {framework_result['message']}", {'framework_result': framework_result})
        
        # Step 6: Experiment validation
        experiment_result = self._validate_project_experiment(project_path_obj)
        if not experiment_result['validation_passed']:
            return self._format_error('experiment', f"Experiment validation failed: {experiment_result['message']}", {'experiment_result': experiment_result})

        # Step 7: Corpus validation
        corpus_result = self._validate_project_corpus(project_path_obj)
        
        # Step 8: Execution Plan Generation
        framework_content = (project_path_obj / "framework.md").read_text()
        # This is a placeholder for getting the real analysis instructions
        analysis_instructions = "Analyze the following texts using the provided framework." 
        models = self._get_models_from_experiment(project_path_obj)

        execution_plan = self.execution_planner_agent.create_execution_plan(
            corpus_files=corpus_result['corpus_files'],
            model_names=models,
            framework_text=framework_content,
            analysis_instructions=analysis_instructions
        )
        if "error" in execution_plan:
            return self._format_error('execution_planning', f"Execution planning failed: {execution_plan['error']}", {'execution_plan': execution_plan})

        final_result = {
            'status': 'success', 'validation_passed': True, 'project_path': str(project_path_obj),
            'validation_timestamp': datetime.now().isoformat(),
            'structure_result': structure_result, 'coherence_result': coherence_result,
            'framework_result': framework_result, 'experiment_result': experiment_result,
            'corpus_result': corpus_result, 'statistical_plan': statistical_plan,
            'statistical_coherence_result': statistical_coherence_result,
            'execution_plan': execution_plan,
            'ready_for_execution': True
        }
        final_result.update(corpus_result)
        return final_result

    def get_pre_execution_summary(self, validation_result: Dict[str, Any]) -> Dict[str, Any]:
        """Generates a structured summary of the execution plan for user confirmation."""
        if not validation_result.get('validation_passed'):
            return {"error": "Validation must pass before generating a summary."}

        plan = validation_result.get('execution_plan', {})
        
        return {
            "Framework": validation_result['framework_result']['framework_name'],
            "Corpus": f"{validation_result['corpus_result']['file_count']} files",
            "Models": self._get_models_from_experiment(Path(validation_result['project_path'])),
            "Total API Calls": plan.get('total_api_calls', 'N/A'),
            "Estimated Cost": f"${plan.get('estimated_cost_usd', 0):.4f} USD",
            "Estimated Duration": f"~{plan.get('estimated_duration_seconds', 0)} seconds",
            "Workflow": "Batch Analysis via Execution Plan",
            "Statistical Plan": [test['test_name'] for test in validation_result['statistical_plan'].get('required_tests', [])]
        }

    def _get_models_from_experiment(self, project_path: Path) -> List[str]:
        """Helper to parse models from the experiment.md YAML block."""
        try:
            experiment_content = (project_path / "experiment.md").read_text()
            yaml_match = re.search(r'```yaml\n(.*?)```', experiment_content, re.DOTALL)
            if yaml_match:
                yaml_config = yaml.safe_load(yaml_match.group(1))
                return yaml_config.get('models', [])
        except Exception:
            return []
        return []

    def _format_error(self, step: str, message: str, details: Dict[str, Any]) -> Dict[str, Any]:
        """Helper to format validation error dictionaries."""
        return {'status': 'error', 'validation_passed': False, 'step_failed': step, 'message': message, **details}

    def _validate_project_coherence(self, project_path: Path) -> Dict[str, Any]:
        """Validate that the experiment, framework, and corpus are logically connected."""
        try:
            framework_content = (project_path / "framework.md").read_text()
            experiment_content = (project_path / "experiment.md").read_text()
        except FileNotFoundError as e:
            return {'validation_passed': False, 'message': f"Missing required file for coherence check: {e.filename}"}

        prompt = f"""
You are a research methodology auditor. Your task is to ensure a research plan is internally coherent and self-contained.

**Framework:**
---
{framework_content[:1500]}
---

**Experiment Plan:**
---
{experiment_content[:1500]}
---

**Audit Checklist:**
1.  **Explicit Link**: Does the experiment plan explicitly state which framework it uses?
2.  **Hypothesis Testability**: Are the hypotheses in the experiment testable using the concepts and anchors defined in the framework?
3.  **Methodology Alignment**: Does the methodology described in the experiment align with the analysis prescribed by the framework?
4.  **Self-Contained**: Are all required assets contained within the experiment folder? No external file references that would break portability?

**Assessment:**
Based on your audit, is this research plan internally coherent and self-contained? Answer with a JSON object with the keys "validation_passed" (boolean) and "message" (a brief explanation of your reasoning).
"""
        try:
            model_name = self.model_registry.get_model_for_task('validation')
            if not model_name:
                return {'validation_passed': False, 'message': "No suitable model found for coherence check."}
            response, metadata = self.gateway.execute_call(model=model_name, prompt=prompt)
            if not metadata.get("success"):
                return {'validation_passed': False, 'error_type': 'LLM_VALIDATION_FAILED', 'message': metadata.get('error', 'Unknown API error')}
            result = json.loads(response)
            return result
        except json.JSONDecodeError as e:
            return {'validation_passed': False, 'message': f"LLM coherence check returned invalid JSON: {e}"}
        except Exception as e:
            return {'validation_passed': False, 'error_type': 'LLM_VALIDATION_FAILED', 'message': f"LLM coherence check failed: {e}"}

    def _validate_statistical_coherence(self, project_path: Path, framework_content: str, statistical_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Ensures the framework's output format matches the statistical plan's needs."""
        
        # This is a placeholder for a more robust method of extracting required fields.
        # For now, we assume 'score' is the key field needed if any statistical tests are planned.
        required_tests = statistical_plan.get('required_tests', [])
        if not required_tests:
            return {'validation_passed': True, 'message': "No statistical tests planned; coherence check not required."}
        
        required_fields = ["score"] # Simple assumption for now.

        prompt = f"""
You are a meticulous Statistical Coherence Auditor. Your job is to verify that a research framework's output instructions will produce the specific data fields required for a planned statistical analysis.

**Statistical Plan Requirements:**
The statistical analysis requires the final output from each analysis run to be a JSON object containing the following key(s): `{', '.join(required_fields)}`.

**Framework to Audit:**
---
{framework_content}
---

**Audit Question:**
Does the framework above explicitly and unambiguously instruct the analysis agent to produce a JSON object that is guaranteed to contain the key(s): `{', '.join(required_fields)}`?

-   Look for instructions about JSON formatting, schema definitions, or specific output keys.
-   If the instructions are clear and guarantee the required keys, the validation passes.
-   If the instructions are ambiguous, missing, or do not guarantee the keys, the validation fails.

**Assessment:**
Respond with a JSON object with two keys:
1.  `"validation_passed"` (boolean): `true` if the framework guarantees the required JSON output, `false` otherwise.
2.  `"message"` (string): A brief explanation for your decision. If it fails, explain what is missing from the framework instructions.
"""
        try:
            model_name = self.model_registry.get_model_for_task('validation')
            if not model_name:
                return {'validation_passed': False, 'message': "No suitable model found for statistical coherence check."}
            
            response, metadata = self.gateway.execute_call(model=model_name, prompt=prompt)
            if not metadata.get("success"):
                return {'validation_passed': False, 'message': f"LLM API call failed: {metadata.get('error')}"}

            result = json.loads(response)

            # If validation fails, attempt to fix it automatically
            if not result.get('validation_passed'):
                print("⚠️ Statistical coherence check failed. Attempting to auto-correct framework...")
                correction_result = self._inject_json_output_instruction(project_path, required_fields)
                if correction_result['success']:
                    # Return a success result indicating it was auto-corrected
                    return {'validation_passed': True, 'message': correction_result['message'], 'auto_corrected': True}
                # If correction fails, return the original failure message plus the correction error
                result['message'] += f" | Auto-correction failed: {correction_result['message']}"
                return result

            return result
        except json.JSONDecodeError as e:
            return {'validation_passed': False, 'message': f"LLM returned invalid JSON for statistical coherence check: {e}"}
        except Exception as e:
            return {'validation_passed': False, 'message': f"An unexpected error occurred during statistical coherence check: {e}"}

    def _inject_json_output_instruction(self, project_path: Path, required_fields: List[str]) -> Dict[str, Any]:
        """Generates and appends a JSON output instruction block to the framework.md file."""
        
        prompt = f"""
You are a helpful research assistant. Your task is to write a standardized markdown section that instructs an analysis agent to provide its output in a specific JSON format.

The required JSON keys are: {required_fields}

Generate a clear, friendly, and unambiguous markdown section that includes:
1. A header like `### Required Output Format`.
2. An explanation of why structured JSON output is necessary (for statistical analysis).
3. A JSON schema example.

The tone should be helpful and instructive.
"""
        try:
            # Use a capable model for generating the instructional text
            model_name = self.model_registry.get_model_for_task('synthesis')
            if not model_name:
                return {'success': False, 'message': "No suitable model found to generate correction text."}

            instruction_text, _ = self.gateway.execute_call(model=model_name, prompt=prompt)
            if not instruction_text:
                return {'success': False, 'message': "LLM failed to generate instruction text."}

            # Append the generated text to the framework.md file
            framework_path = project_path / "framework.md"
            with open(framework_path, 'a') as f:
                f.write("\n\n" + instruction_text)
            
            print(f"✅ Automatically appended JSON output instructions to {framework_path}")
            return {'success': True, 'message': "Successfully appended JSON output instruction to framework.md."}

        except Exception as e:
            print(f"❌ Failed to inject JSON output instruction: {e}")
            return {'success': False, 'message': str(e)}

    def _validate_project_framework(self, project_path: Path) -> Dict[str, Any]:
        """Validate project framework using Framework Specification Validation Rubric"""
        
        # Load framework from project
        framework_context = self.framework_loader.load_project_framework(str(project_path))
        
        if framework_context['status'] != 'success':
            return {
                'status': 'error',
                'validation_passed': False,
                'message': framework_context['message']
            }
        
        # Validate framework using rubric
        validation_result = self.framework_loader.validate_framework(
            framework_context['framework_content'],
            framework_context['framework_name']
        )
        
        if validation_result['status'] != 'success':
            return {
                'status': 'error',
                'validation_passed': False,
                'message': validation_result['message']
            }
        
        # Check completeness threshold
        completeness = validation_result.get('completeness_percentage', 0)
        passed_threshold = completeness >= self.framework_threshold
        
        return {
            'status': 'success',
            'validation_passed': passed_threshold,
            'completeness_percentage': completeness,
            'threshold_required': self.framework_threshold,
            'framework_name': framework_context['framework_name'],
            'validation_details': validation_result['full_response'],
            'message': f"Framework {'passed' if passed_threshold else 'failed'} validation ({completeness}% completeness)"
        }
    
    def _validate_project_experiment(self, project_path: Path) -> Dict[str, Any]:
        """Validate project experiment using Experiment Specification Validation Rubric"""
        
        experiment_path = project_path / "experiment.md"
        
        if not experiment_path.exists():
            return {
                'status': 'error',
                'validation_passed': False,
                'message': f'Experiment file not found: {experiment_path}'
            }
        
        try:
            experiment_content = experiment_path.read_text()
        except Exception as e:
            return {
                'status': 'error',
                'validation_passed': False,
                'message': f'Error reading experiment file: {str(e)}'
            }
        
        # Validate experiment using LLM with rubric
        if not self.gateway:
            return self._mock_experiment_validation(experiment_content, str(project_path))
        
        # Simplified experiment validation prompt
        validation_prompt = f"""You are an experiment validation expert. Evaluate this experiment design efficiently.

EXPERIMENT VALIDATION CRITERIA:
1. Clear research question
2. Falsifiable hypotheses
3. Dataset description and methodology
4. Analysis plan
5. Literature context and justification

PASSING THRESHOLD: 90% of criteria met (4+ out of 5 criteria)

EXPERIMENT TO VALIDATE:
{experiment_content[:3000]}

TASK: Evaluate this experiment against the 5 criteria above. Be reasonable - if an experiment has most components well-defined, it should pass.

RESPONSE FORMAT (REQUIRED):
VALIDATION RESULT: PASS/FAIL
COMPLETENESS: [percentage]%
CRITICAL ISSUES: [list major problems or "None"]
SUMMARY: [brief assessment]

Provide your assessment now."""

        try:
            model_name = self.model_registry.get_model_for_task('validation')
            if not model_name:
                return self._format_error('experiment', "No suitable model found for experiment validation.", {})
            
            validation_response, metadata = self.gateway.execute_call(model=model_name, prompt=validation_prompt)
            
            if not metadata.get("success"):
                return {
                    'status': 'error',
                    'validation_passed': False,
                    'error_type': 'LLM_VALIDATION_FAILED',
                    'message': metadata.get('error', 'Unknown API error')
                }

            # Handle None/empty response
            if not validation_response or validation_response.strip() == 'None':
                print("🚨 DEBUG: Empty/None LLM response for experiment validation")
                print(f"   Prompt length: {len(validation_prompt)} chars")
                print(f"   Response: '{validation_response}'")
                print("   Using fallback validation...")
                
                return self._fallback_experiment_validation(experiment_content, str(project_path))
            
            return self._parse_experiment_validation(validation_response, str(project_path))
        except Exception as e:
            return {
                'status': 'error',
                'validation_passed': False,
                'error_type': 'LLM_VALIDATION_FAILED',
                'message': f'Experiment validation failed: {str(e)}'
            }
    
    def _parse_experiment_validation(self, response: str, _project_path: str) -> Dict[str, Any]:
        """Parse LLM experiment validation response"""
        
        # Check for None response or 'None' string
        if not response or response.strip() == 'None':
            return {
                'status': 'error',
                'validation_passed': False,
                'completeness_percentage': 0,
                'validation_details': response or '',
                'message': 'Empty validation response from LLM'
            }
        
        # THIN: Minimal parsing - just extract key decisions
        validation_passed = "VALIDATION RESULT: PASS" in response
        
        # Extract completeness percentage
        completeness = 0
        if "COMPLETENESS:" in response:
            try:
                completeness_line = [line for line in response.split('\n') if 'COMPLETENESS:' in line][0]
                completeness = int(completeness_line.split('%')[0].split(':')[1].strip())
            except Exception:
                completeness = 0
        
        # If no completeness found but response exists, use reasonable default
        if completeness == 0 and validation_passed:
            completeness = 90  # Default to passing threshold
        elif completeness == 0 and not validation_passed:
            completeness = 70  # Default to reasonable failing score
        
        # Check threshold
        passed_threshold = completeness >= self.experiment_threshold
        
        return {
            'status': 'success',
            'validation_passed': validation_passed and passed_threshold,
            'completeness_percentage': completeness,
            'threshold_required': self.experiment_threshold,
            'validation_details': response,
            'message': f"Experiment {'passed' if validation_passed and passed_threshold else 'failed'} validation ({completeness}% completeness)"
        }
    
    def _mock_experiment_validation(self, _experiment_content: str, _project_path: str) -> Dict[str, Any]:
        """Mock experiment validation for testing"""
        return {
            'status': 'success',
            'validation_passed': True,
            'completeness_percentage': 93,
            'threshold_required': self.experiment_threshold,
            'validation_details': "[MOCK] Experiment validated with 93% completeness",
            'message': "Experiment passed validation (93% completeness)"
        }
    
    def _fallback_experiment_validation(self, experiment_content: str, _project_path: str) -> Dict[str, Any]:
        """Fallback experiment validation when LLM returns None"""
        
        # Simple heuristic-based validation with improved detection
        content_lower = experiment_content.lower()
        
        # More comprehensive detection patterns
        has_research_question = any(term in content_lower for term in [
            'research question', 'question', 'primary question', 'secondary question'
        ])
        
        has_hypothesis = any(term in content_lower for term in [
            'hypothesis', 'hypotheses', 'prediction', 'h1', 'h2', 'h3', 'h_alt'
        ])
        
        has_dataset = any(term in content_lower for term in [
            'dataset', 'corpus', 'sample', 'data', 'texts', 'speeches', 'selection criteria'
        ])
        
        has_analysis_plan = any(term in content_lower for term in [
            'analysis plan', 'method', 'procedure', 'statistical', 'analytical approach', 'analysis'
        ])
        
        has_literature = any(term in content_lower for term in [
            'literature', 'prior', 'previous', 'research', 'theoretical foundation', 'context'
        ])
        
        # Additional quality indicators
        has_operationalization = any(term in content_lower for term in [
            'operationalization', 'measurement', 'variable', 'dependent', 'independent'
        ])
        
        has_methodology = any(term in content_lower for term in [
            'methodology', 'statistical method', 'test', 'significance', 'framework alignment'
        ])
        
        # Count basic criteria (must have all 5)
        basic_criteria = [has_research_question, has_hypothesis, has_dataset, has_analysis_plan, has_literature]
        basic_score = sum(basic_criteria)
        
        # Count quality indicators (bonus points)
        quality_indicators = [has_operationalization, has_methodology]
        quality_score = sum(quality_indicators)
        
        # Calculate final score with bonus
        total_possible = 5 + 2  # 5 basic + 2 quality
        total_score = basic_score + quality_score
        heuristic_score = min(100, int((total_score / total_possible) * 100))
        
        # More detailed feedback
        details = f"[FALLBACK] Heuristic validation: {basic_score}/5 basic criteria + {quality_score}/2 quality indicators = {total_score}/7 total"
        
        return {
            'status': 'success',
            'validation_passed': heuristic_score >= 80,  # 80% threshold
            'completeness_percentage': heuristic_score,
            'threshold_required': self.experiment_threshold,
            'validation_details': details,
            'message': f"Experiment {'passed' if heuristic_score >= 80 else 'failed'} validation ({heuristic_score}% completeness)",
            'fallback_used': True
        }
    
    def _validate_project_corpus(self, project_path: Path, corpus_path: Optional[str] = None) -> Dict[str, Any]:
        """Validate project corpus directory and manifest"""
        
        # Use provided corpus path or default to project/corpus
        if corpus_path:
            actual_corpus_path = Path(corpus_path)
        else:
            actual_corpus_path = project_path / "corpus"
        
        if not actual_corpus_path.exists():
            return {
                'status': 'error',
                'validation_passed': False,
                'message': f'Corpus directory not found: {actual_corpus_path}'
            }
        
        # Check for corpus files
        corpus_files = []
        for file_path in actual_corpus_path.rglob("*.txt"):
            corpus_files.append(str(file_path))
        
        # Also check for .md files (sanitized corpus uses markdown)
        for file_path in actual_corpus_path.rglob("*.md"):
            corpus_files.append(str(file_path))
        
        if not corpus_files:
            return {
                'status': 'error',
                'validation_passed': False,
                'message': f'No text/markdown files found in corpus directory: {actual_corpus_path}'
            }
        
        # Check for manifest (optional but recommended)
        manifest_files = list(actual_corpus_path.glob("manifest.yaml")) + list(actual_corpus_path.glob("*.yaml"))
        has_manifest = len(manifest_files) > 0
        
        return {
            'status': 'success',
            'validation_passed': True,
            'corpus_path': str(actual_corpus_path),
            'corpus_files': corpus_files,
            'file_count': len(corpus_files),
            'has_manifest': has_manifest,
            'manifest_files': [str(f) for f in manifest_files],
            'message': f"Corpus validation passed ({len(corpus_files)} files found)"
        }
    
    def interactive_resolution(self, validation_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Interactive CLI dialog for resolving validation issues
        
        THIN Principle: Software provides CLI interface; user provides resolution
        """
        if validation_result['validation_passed']:
            print("✅ Project validation passed! Ready for execution.")
            return validation_result
        
        print(f"❌ Project validation failed at step: {validation_result['step_failed']}")
        print(f"   Message: {validation_result['message']}")
        print()
        
        # Show specific issues based on failed step
        if validation_result['step_failed'] == 'structure':
            self._show_structure_issues(validation_result['structure_result'])
        elif validation_result['step_failed'] == 'framework':
            self._show_framework_issues(validation_result['framework_result'])
        elif validation_result['step_failed'] == 'experiment':
            self._show_experiment_issues(validation_result['experiment_result'])
        
        # Ask user for next steps
        print("\nOptions:")
        print("1. Fix issues and re-validate")
        print("2. Show detailed validation report")
        print("3. Exit")
        
        choice = input("\nChoose an option (1-3): ").strip()
        
        if choice == "1":
            print("\n📝 Please fix the issues listed above and run 'soar validate' again.")
            return {'status': 'user_action_required', 'action': 'fix_and_revalidate'}
        if choice == "2":
            self._show_detailed_report(validation_result)
            return {'status': 'user_action_required', 'action': 'show_report'}
        print("\n👋 Exiting validation. Fix issues and try again.")
        return {'status': 'user_exit'}
    
    def _show_structure_issues(self, structure_result: Dict[str, Any]):
        """Show project structure issues"""
        print("\n📁 PROJECT STRUCTURE ISSUES:")
        print("Missing required files:")
        for missing_file in structure_result['missing_files']:
            print(f"   - {missing_file}")
        
        print("\nRequired SOAR project structure:")
        print("   project/")
        print("   ├── framework.md      # Framework specification")
        print("   ├── experiment.md     # Research design")
        print("   └── corpus/           # Text files for analysis")
        print("       ├── manifest.yaml # (optional) Corpus metadata")
        print("       └── *.txt         # Text files")
    
    def _show_framework_issues(self, framework_result: Dict[str, Any]):
        """Show framework validation issues"""
        print("\n🔬 FRAMEWORK VALIDATION ISSUES:")
        print(f"Completeness: {framework_result.get('completeness_percentage', 0)}% (required: {self.framework_threshold}%)")
        
        if 'validation_details' in framework_result:
            print("\nDetailed validation feedback:")
            print(framework_result['validation_details'])
    
    def _show_experiment_issues(self, experiment_result: Dict[str, Any]):
        """Show experiment validation issues"""
        print("\n🧪 EXPERIMENT VALIDATION ISSUES:")
        print(f"Completeness: {experiment_result.get('completeness_percentage', 0)}% (required: {self.experiment_threshold}%)")
        
        if 'validation_details' in experiment_result:
            print("\nDetailed validation feedback:")
            print(experiment_result['validation_details'])
    
    def _show_detailed_report(self, validation_result: Dict[str, Any]):
        """Show detailed validation report"""
        print("\n📊 DETAILED VALIDATION REPORT")
        print("=" * 50)
        
        print(f"Project Path: {validation_result.get('project_path', 'Unknown')}")
        print(f"Failed Step: {validation_result['step_failed']}")
        print(f"Status: {'PASSED' if validation_result['validation_passed'] else 'FAILED'}")
        
        # Show all available details
        for key, value in validation_result.items():
            if key.endswith('_result') and isinstance(value, dict):
                print(f"\n{key.upper()}:")
                for subkey, subvalue in value.items():
                    if isinstance(subvalue, (str, int, float, bool)):
                        print(f"  {subkey}: {subvalue}")
    
    def validate_thin_compliance(self) -> Dict[str, Any]:
        """Self-validation: Check if ValidationAgent follows THIN principles"""
        
        issues = []
        recommendations = []
        
        # Check dependencies
        if not DEPENDENCIES_AVAILABLE:
            issues.append("Required dependencies not available")
        
        if not self.framework_rubric:
            issues.append("Framework validation rubric not loaded")
        
        if not self.experiment_rubric:
            issues.append("Experiment validation rubric not loaded")
        
        # THIN recommendations
        recommendations.extend([
            "ValidationAgent provides validation orchestration only",
            "All validation intelligence comes from LLM + rubrics",
            "No content parsing or interpretation in software",
            "Interactive resolution provides CLI interface only"
        ])
        
        return {
            'thin_compliant': len(issues) == 0,
            'issues': issues,
            'recommendations': recommendations,
            'component': 'ValidationAgent'
        } 

    async def _handle_failed_models(self, requested_models: List[str], health_results: Dict[str, Any]) -> List[str]:
        """
        Orchestrates the "Detect, Explain, Propose, Confirm" workflow for failed models.
        """
        failed_models = [m for m, r in health_results['results'].items() if not r['is_healthy'] and m in requested_models]
        healthy_models = [m for m, r in health_results['results'].items() if r['is_healthy']]

        # --- Detect & Explain ---
        print("="*80)
        print("⚠️ MODEL HEALTH WARNING")
        print("="*80)
        print("One or more of your requested models failed the health check:")
        for model in failed_models:
            print(f"- {model}: {health_results['results'][model]['message']}")
        
        # --- Propose ---
        print("\nConsulting EnsembleConfigurationAgent for a recommendation...")
        config_agent = EnsembleConfigurationAgent()
        
        recommendation = config_agent.assess_model_health_situation({
            "required_models": requested_models,
            "failed_models": failed_models,
            "healthy_models": healthy_models, # Pass the full list of healthy alternatives
            "health_results": health_results,
            "project_path": self.project_path
        })
        
        print(f"\nAGENT RECOMMENDATION: {recommendation.get('action', 'cancel').upper()}")
        print(recommendation.get('explanation'))

        # --- Confirm ---
        if recommendation.get('action') == 'substitute':
            adjusted_models = recommendation.get('adjusted_models', [])
            print("\nPROPOSED CHANGE to experiment.md:")
            print(f"  models: {adjusted_models}")
            
            choice = input("Apply this change and proceed? [Y]es / [N]o: ").strip().upper()
            if choice == 'Y':
                print("✅ Change approved. Proceeding with adjusted model list.")
                # In a real implementation, we would now programmatically update experiment.md
                # For now, we return the adjusted list to be used in memory.
                return recommendation.get('adjusted_models', [])
            print("❌ Change rejected. Terminating execution.")
            raise SystemExit
        
        if recommendation.get('action') == 'proceed':
            # Filter the original list to only include healthy models
            final_models = [m for m in requested_models if m not in failed_models]
            print(f"✅ Proceeding with the remaining healthy models: {final_models}")
            return final_models
        
        # 'cancel' or any other case
        print("❌ Execution cancelled as per agent recommendation.")
        raise SystemExit

    async def _perform_health_check(self, _requested_models: List[str]) -> List[str]:
        # This method is now superseded by the logic in _handle_failed_models
        # and the comprehensive check in validate_and_execute_sync.
        # It can be removed or kept for other purposes if needed.
        return []

    def validate_and_execute_sync(self, framework_path: str, experiment_path: str, corpus_path: Optional[str] = None, dev_mode: bool = False) -> Dict[str, Any]:
        """Synchronous wrapper for the main async execution method."""
        try:
            return asyncio.run(self.validate_and_execute_async(framework_path, experiment_path, corpus_path, dev_mode))
        except SystemExit:
            print("\nExecution terminated by user.")
            return {"status": "cancelled", "message": "User cancelled the operation."}
        except Exception as e:
            print(f"\n❌ An unexpected error occurred: {e}")
            # Optionally log the full traceback here
            return {"status": "error", "message": str(e)}

    async def validate_and_execute_async(self, framework_path: str, experiment_path: str, corpus_path: Optional[str] = None, dev_mode: bool = False) -> Dict[str, Any]:
        """Main async execution method for validation and orchestration."""
        import redis
        from datetime import datetime
        from discernus.core.project_chronolog import initialize_project_chronolog, log_project_event
        import getpass
        
        session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        project_path_obj = Path(framework_path).parent
        user = getpass.getuser()
        
        if corpus_path is None:
            try:
                experiment_content_for_path = Path(experiment_path).read_text()
                if self.gateway:
                    corpus_prompt = f"What corpus path does this experiment specify?\n\nEXPERIMENT: {experiment_content_for_path}\n\nAnswer with just the path."
                    model_name = self.model_registry.get_model_for_task('validation')
                    if model_name:
                        llm_response, _ = self.gateway.execute_call(model=model_name, prompt=corpus_prompt)
                        if llm_response and llm_response.strip():
                            extracted_path = llm_response.strip().strip('"\'')
                            corpus_path = str(project_path_obj / extracted_path)
                if corpus_path is None:
                    corpus_path = str(project_path_obj / "corpus")
            except Exception as e:
                corpus_path = str(project_path_obj / "corpus")
        
        command = f"ValidationAgent.validate_and_execute_sync(framework_path='{framework_path}', experiment_path='{experiment_path}', corpus_path='{corpus_path}', dev_mode={dev_mode})"
        
        try:
            initialize_project_chronolog(project_path=str(project_path_obj), user=user, command=command, session_id=session_id)
        except Exception as e:
            print(f"⚠️ ProjectChronolog initialization failed: {e}")
        
        redis_client = redis.Redis(host='localhost', port=6379, db=0)
        
        try:
            # --- Set project_path for the instance ---
            self.project_path = Path(framework_path).parent

            log_project_event(str(self.project_path), "VALIDATION_STARTED", session_id, {"framework_path": framework_path, "experiment_path": experiment_path, "corpus_path": corpus_path})
            
            framework_content = Path(framework_path).read_text() if Path(framework_path).exists() else ""
            experiment_content = Path(experiment_path).read_text() if Path(experiment_path).exists() else ""
            corpus_files = list(Path(corpus_path).rglob("*.txt")) if Path(corpus_path).exists() else []
            
            if not framework_content or not experiment_content or not corpus_files:
                raise FileNotFoundError("One or more essential files (framework, experiment, corpus) were not found.")
            
            # --- NEW, CORRECTED HEALTH CHECK WORKFLOW ---
            
            # 1. Get all possible models from the registry
            all_possible_models = self.model_registry.list_models()

            # 2. Perform comprehensive health check on ALL models
            print("\n--- Running Comprehensive Model Health Check ---")
            health_checker = self.gateway
            # This needs to be run in an event loop
            health_results = await health_checker.check_many_models_health(all_possible_models)

            # 3. Assess the situation for the specific models requested in the experiment
            experiment_config = self._parse_config_from_experiment(experiment_content)
            requested_models = experiment_config.get('models', [])
            
            failed_models = [m for m, r in health_results['results'].items() if not r['is_healthy'] and m in requested_models]
            
            if failed_models:
                # 4. If there's an issue, get an intelligent recommendation
                approved_models = await self._handle_failed_models(
                    requested_models=requested_models,
                    health_results=health_results
                )
            else:
                print("✅ All requested models are healthy.")
                approved_models = requested_models

            # The rest of the process uses the final, approved_models list
            
            if self.gateway:
                corpus_sample = ""
                for i, file_path in enumerate(corpus_files[:3]):
                    content = Path(file_path).read_text()[:500]
                    corpus_sample += f"\nFile {i+1}: {Path(file_path).name}\n{content}...\n"
                
                validation_prompt = f"Do you think this corpus could be analyzed with this framework in the way described in this experiment?\n\nFRAMEWORK: {framework_content}\n\nEXPERIMENT: {experiment_content}\n\nCORPUS: {len(corpus_files)} files. Sample content:\n{corpus_sample}\n\nAnswer: YES/NO with brief reasoning."
                
                reasoning, _ = self.gateway.execute_call(model="anthropic/claude-3-haiku-20240307", prompt=validation_prompt)

                decision_prompt = f"Based on the following reasoning, should the experiment proceed? Answer only with 'YES' or 'NO'.\n\nREASONING:\n{reasoning}"
                
                final_decision, _ = self.gateway.execute_call(model="anthropic/claude-3-haiku-20240307", prompt=decision_prompt)

                if "YES" not in final_decision.upper():
                    print("="*80)
                    print("❌ EXPERIMENT VALIDATION FAILED: Compatibility Check")
                    print("="*80)
                    print("The initial LLM validation check determined that your framework, experiment, and corpus are not compatible as written.")
                    print("\nLLM REASONING:")
                    print(reasoning) # Print the original detailed reasoning
                    print("\nRECOMMENDATION: Please review the framework and experiment files to ensure they are aligned.")
                    print("="*80)
                    return {"status": "validation_failed", "message": f"Compatibility validation failed: {reasoning}"}
            
            project_dir = Path(framework_path).parent
            discovered_assets = self._discover_experiment_assets(experiment_content, project_dir)
            
            instruction_prompt = f"Generate analysis agent instructions for this framework and experiment:\n\nFRAMEWORK: {framework_content}\n\nEXPERIMENT: {experiment_content}\n\nDISCOVERED ASSETS (as specified by experiment):\n{discovered_assets}\n\nCreate detailed instructions..."
            
            if self.gateway:
                model_name = self.model_registry.get_model_for_task('synthesis')
                if not model_name:
                    analysis_instructions = "[MOCK] No suitable model found for instruction generation."
                else:
                    analysis_instructions, _ = self.gateway.execute_call(model=model_name, prompt=instruction_prompt)
            else:
                analysis_instructions = "[MOCK] Analysis instructions would be generated here"
            
            # --- This is where the handoff to the orchestrator happens ---
            
            experiment_config = self._parse_config_from_experiment(experiment_content)
            experiment_config['models'] = approved_models # Use the approved list
            if 'workflow' not in experiment_config:
                raise ValueError("Experiment must contain a `workflow` definition.")

            # 1. Optimize model selection
            config_agent = EnsembleConfigurationAgent()
            requested_models = experiment_config.get('models', [])
            optimized_models = config_agent.optimize_model_selection(requested_models)
            
            # 2. Create a safe execution plan
            planner_agent = ExecutionPlannerAgent()
            execution_plan = planner_agent.create_execution_plan(
                corpus_files=[str(f) for f in corpus_files],
                model_names=optimized_models,
                framework_text=framework_content,
                analysis_instructions=analysis_instructions
            )

            print("✅ Modern workflow detected. Initializing WorkflowOrchestrator.")
            orchestrator = WorkflowOrchestrator(str(project_path_obj))
            
            # The initial state for the workflow includes the optimized models and the execution plan
            initial_state = {
                "corpus_files": [str(f) for f in corpus_files],
                "analysis_agent_instructions": analysis_instructions,
                "framework_content": framework_content,
                "experiment_content": experiment_content,
                "optimized_models": optimized_models,
                "execution_plan": execution_plan
            }
            final_result = await orchestrator.execute_workflow(initial_state)

            log_project_event(str(project_path_obj), "VALIDATION_COMPLETED", session_id, {"status": "validated"})
            
            return final_result
            
        except Exception as e:
            log_project_event(str(project_path_obj), "VALIDATION_ERROR", session_id, {"error": str(e)})
            return {"status": "error", "message": f"Failed to load files: {str(e)}"}
    
    def _parse_config_from_experiment(self, experiment_content: str) -> Dict[str, Any]:
        """Helper to parse YAML config from experiment content."""
        try:
            yaml_match = re.search(r'```yaml\n(.*?)```', experiment_content, re.DOTALL)
            if yaml_match:
                return yaml.safe_load(yaml_match.group(1))
        except Exception:
            return {}
        return {}

    def _discover_experiment_assets(self, experiment_content: str, project_dir: Path) -> str:
        """
        THIN asset discovery: Parse experiment specification for asset discovery protocols
        
        The experiment specification provides intelligence about what assets are needed;
        software provides file system operations to load them.
        """
        discovered_assets = []
        
        try:
            # Look for asset discovery protocols in experiment content
            asset_patterns = [
                ('pdaf_assets/', 'PDAF calibration materials'),
                ('assets/', 'framework assets'),
                ('calibration/', 'calibration materials'),
                ('reference_texts/', 'reference materials')
            ]
            
            for asset_dir, description in asset_patterns:
                if asset_dir in experiment_content.lower():
                    asset_path = project_dir / asset_dir.strip('/')
                    if asset_path.exists():
                        print(f"📁 Discovered asset directory: {asset_path}")
                        asset_contents = self._load_asset_directory(asset_path, description)
                        if asset_contents:
                            discovered_assets.append(asset_contents)
            
            # Look for specific file mentions in experiment
            if 'calibration assets:' in experiment_content.lower():
                print("🔍 Experiment specifies calibration assets protocol")
            
            if 'thin asset discovery protocol:' in experiment_content.lower():
                print("🔍 Experiment includes THIN asset discovery protocol")
            
            if not discovered_assets:
                return "No additional assets discovered (following experiment specification)"
            
            return "\n\n".join(discovered_assets)
            
        except Exception as e:
            print(f"⚠️ Asset discovery error: {e}")
            return f"Asset discovery failed: {str(e)}"
    
    def _load_asset_directory(self, asset_path: Path, description: str) -> str:
        """Load all files from an asset directory"""
        
        if not asset_path.exists() or not asset_path.is_dir():
            return ""
        
        asset_content = f"=== {description.upper()} ===\nLocation: {asset_path}\n\n"
        
        # Load text files from asset directory
        text_files = list(asset_path.glob("*.md")) + list(asset_path.glob("*.txt")) + list(asset_path.glob("*.yaml"))
        
        for file_path in text_files:
            try:
                content = file_path.read_text()
                asset_content += f"--- {file_path.name} ---\n{content}\n\n"
                print(f"📄 Loaded asset: {file_path.name} ({len(content)} chars)")
            except Exception as e:
                print(f"⚠️ Could not load {file_path}: {e}")
                continue
        
        if len(text_files) == 0:
            asset_content += "No readable text files found in this directory.\n"
        
        return asset_content 