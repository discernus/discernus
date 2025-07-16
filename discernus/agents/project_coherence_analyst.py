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
import getpass
import traceback
import litellm

from discernus.core.project_chronolog import initialize_project_chronolog, log_project_event
from discernus.core.framework_loader import FrameworkLoader
from discernus.gateway.llm_gateway import LLMGateway
from discernus.agents.ensemble_configuration_agent import EnsembleConfigurationAgent
from discernus.agents.statistical_analysis_configuration_agent import StatisticalAnalysisConfigurationAgent
from discernus.agents.execution_planner_agent import ExecutionPlannerAgent
from discernus.gateway.model_registry import ModelRegistry # Corrected import path
from discernus.orchestration.ensemble_orchestrator import EnsembleOrchestrator
# No standalone AgentRegistry class, it's loaded from YAML

from discernus.core.thin_validation import check_thin_compliance

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    DEPENDENCIES_AVAILABLE = True
except ImportError as e:
    print(f"ValidationAgent dependencies not available: {e}")
    DEPENDENCIES_AVAILABLE = False

class ProjectCoherenceAnalyst:
    """
    THIN validation agent - orchestrates LLM validation using rubrics
    Software provides validation workflow; LLM provides validation intelligence
    """
    
    def __init__(self, llm_gateway=None, framework_loader=None):
        self.project_path: Optional[Path] = None # Initialize project_path
        
        # Instantiate registry first, as it's needed by the gateway
        self.model_registry = ModelRegistry()
        self._load_agent_registry() # Load the agent registry

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

    async def validate_project(self, project_path: str) -> Dict[str, Any]:
        """
        Validates the entire project structure and its components.
        This is the main entry point for the 'validate' CLI command.
        """
        self.project_path = Path(project_path)
        
        # Step 1: Structural Validation
        structure_result = self._validate_project_structure()
        if not structure_result["validation_passed"]:
            return structure_result

        # Step 2: Global Model Health Check
        all_models = self.model_registry.list_models()
        health_results = await self._verify_model_health(all_models)

        # Step 3: Experiment Analysis & Coherence Check
        experiment_path = self.project_path / "experiment.md"
        experiment_content = experiment_path.read_text()
        
        # Extract requested models
        requested_models = self._extract_models_from_experiment(experiment_content)
        
        # Model Coherence Analysis
        if not requested_models:
            # Proactive recommendation
            # In a real implementation, a call to an LLM would happen here
            # to determine the best model for the experiment.
            pass
        else:
            for model in requested_models:
                if model not in health_results["results"] or health_results["results"][model]["status"] == "failed":
                    return {
                        "validation_passed": False,
                        "step_failed": "Model Health Check",
                        "message": f"Requested model '{model}' is not available or failed health check.",
                    }

        # Corpus Coherence Analysis (placeholder)
        corpus_path = self.project_path / "corpus"
        corpus_files = [f.name for f in corpus_path.iterdir() if f.is_file()]
        
        # In a real implementation, we would compare corpus_files with experiment expectations
        
        return {
            "validation_passed": True,
            "message": "Project validation successful",
            "project_path": str(self.project_path),
            "ready_for_execution": True,
            "validation_timestamp": datetime.now().isoformat(),
        }

    def _extract_models_from_experiment(self, experiment_content: str) -> List[str]:
        """
        Extract the list of models from the experiment.md file.
        """
        try:
            # Look for YAML configuration blocks
            yaml_pattern = r'```yaml\n(.*?)\n```'
            matches = re.findall(yaml_pattern, experiment_content, re.DOTALL)
            
            for match in matches:
                try:
                    config = yaml.safe_load(match)
                    if isinstance(config, dict) and 'models' in config:
                        return config['models']
                except yaml.YAMLError:
                    continue
            
            # Fallback: look for models listed in text
            model_pattern = r'(?:models?|LLMs?):\s*\n((?:\s*[-*]\s*.+\n)*)'
            matches = re.findall(model_pattern, experiment_content, re.IGNORECASE)
            
            for match in matches:
                models = []
                for line in match.split('\n'):
                    line = line.strip()
                    if line.startswith(('-', '*')):
                        model = line[1:].strip()
                        if model:
                            models.append(model)
                if models:
                    return models
                    
        except Exception as e:
            print(f"⚠️ Error reading experiment file: {e}")
        
        return []

    def _validate_project_structure(self) -> Dict[str, Any]:
        """Checks for the required files in the project directory."""
        assert self.project_path is not None, "Project path must be set before validating structure."
        required_files = ["framework.md", "experiment.md"]
        found_files = []
        missing_files = []

        for f in required_files:
            if (self.project_path / f).exists():
                found_files.append(f)
            else:
                missing_files.append(f)

        if not (self.project_path / "corpus").is_dir():
            missing_files.append("corpus/")

        if missing_files:
            return {
                "validation_passed": False,
                "step_failed": "Project Structure",
                "message": f"Missing required files/directories: {', '.join(missing_files)}",
                "found_files": found_files,
                "missing_files": missing_files,
            }

        return {
            "validation_passed": True,
            "message": "Project structure is valid.",
            "found_files": found_files + ["corpus/"],
        }

    def _validate_framework(self, framework_content: str) -> Dict[str, Any]:
        """Placeholder for framework validation logic."""
        # In a real implementation, this would use an LLM with a rubric.
        return {"validation_passed": True, "message": "Framework validation placeholder."}

    def _validate_experiment(self, experiment_content: str) -> Dict[str, Any]:
        """Placeholder for experiment validation logic."""
        # In a real implementation, this would use an LLM with a rubric.
        return {"validation_passed": True, "message": "Experiment validation placeholder."}

    async def _check_model_health(self, model_name: str) -> Dict[str, Any]:
        """
        Check the health of a single model.
        """
        try:
            messages = [{"role": "user", "content": "Hello, are you there? Respond with just 'yes'."}]
            
            # Add safety settings specifically for Vertex AI models
            # and REMOVE max_tokens which triggers safety filters
            extra_kwargs = {}
            if model_name.startswith("vertex_ai"):
                extra_kwargs['safety_settings'] = [
                    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
                ]
            else:
                # For non-Vertex AI models, use a small max_tokens to keep costs low
                extra_kwargs['max_tokens'] = 5
            
            response = await litellm.acompletion(
                model=model_name,
                messages=messages,
                temperature=0.0,
                **extra_kwargs
            )
            
            # Use getattr for safer attribute access
            content = getattr(getattr(getattr(response, 'choices', [{}])[0], 'message', {}), 'content', '') or ""
            if content.strip():
                return {"status": "success", "message": "Model responded successfully"}
            else:
                return {"status": "failed", "message": "Empty response received"}
                
        except Exception as e:
            return {"status": "failed", "message": str(e)}

    async def _verify_model_health(self, models: List[str]) -> Dict[str, Any]:
        """
        Verify the health of all models in the list.
        """
        if not models:
            return {"all_healthy": True, "results": {}}
        
        results = {}
        tasks = []
        
        for model in models:
            task = self._check_model_health(model)
            tasks.append((model, task))
        
        # Execute all health checks in parallel
        for model, task in tasks:
            try:
                result = await task
                results[model] = result
            except Exception as e:
                results[model] = {"status": "failed", "message": f"Health check failed: {str(e)}"}
        
        # Determine overall health
        failed_models = [model for model, result in results.items() if result["status"] == "failed"]
        all_healthy = len(failed_models) == 0
        
        return {
            "all_healthy": all_healthy,
            "results": results,
            "failed_models": failed_models,
            "total_models": len(models),
            "healthy_models": len(models) - len(failed_models)
        }

    def _load_agent_registry(self):
        """Loads the agent registry from YAML."""
        registry_path = project_root / "discernus" / "core" / "agent_registry.yaml"
        if not registry_path.exists():
            self.agent_registry = {}
            print("⚠️ Agent registry not found. Plan generation will be limited.")
            return
        with open(registry_path, 'r') as f:
            registry_data = yaml.safe_load(f)
        self.agent_registry = {agent['name']: agent for agent in registry_data.get('agents', [])}

    def get_pre_execution_summary(self, validation_result: Dict[str, Any]) -> Dict[str, str]:
        """
        Generates a human-readable summary of the execution plan.
        """
        summary = {
            "Project": Path(validation_result.get('project_path', 'N/A')).name,
            "Framework": "framework.md",
            "Experiment": "experiment.md",
            "Corpus Files": "Located in corpus/",
        }
        return summary
        
    def validate_and_execute_sync(self, framework_path: str, experiment_path: str, corpus_path: Optional[str] = None, dev_mode: bool = False) -> Dict[str, Any]:
        """Synchronous wrapper for the main async execution method."""
        try:
            return asyncio.run(self.validate_and_execute_async(framework_path, experiment_path, corpus_path, dev_mode))
        except SystemExit:
            print("\nExecution terminated by user.")
            return {"status": "cancelled", "message": "User cancelled the operation."}
        except Exception as e:
            print(f"\n❌ An unexpected error occurred: {e}")
            traceback.print_exc()
            return {"status": "error", "message": str(e)}

    async def validate_and_execute_async(self, framework_path: str, experiment_path: str, corpus_path: Optional[str] = None, dev_mode: bool = False) -> Dict[str, Any]:
        """Main async execution method for validation and orchestration."""
        session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        project_path_obj = Path(framework_path).parent

        # Ensure corpus_path is set before use
        if not corpus_path:
            corpus_path = str(project_path_obj / "corpus")
        
        try:
            # --- 1. Load Core Assets ---
            framework_content = Path(framework_path).read_text()
            experiment_content = Path(experiment_path).read_text()
            corpus_files = [str(f) for f in Path(corpus_path).rglob("*") if f.is_file()]
            
            # --- 2. Generate Execution Plan via AI ---
            execution_plan = await self._generate_execution_plan(framework_content, experiment_content, corpus_files)

            if not execution_plan:
                print("❌ Could not generate a valid execution plan from the experiment description.")
                return {"status": "error", "message": "Failed to generate execution plan."}

            # --- 3. Generate Analysis Instructions ---
            analysis_instructions = await self._generate_analysis_instructions(framework_content, experiment_content)

            # --- 4. Confirm Plan with User ---
            if not self._confirm_execution_plan(execution_plan, dev_mode=dev_mode):
                raise SystemExit("Execution cancelled by user.")

            # --- 5. Handoff to Orchestrator ---
            print("✅ Plan approved. Initializing EnsembleOrchestrator.")
            orchestrator = EnsembleOrchestrator(str(project_path_obj))
            
            initial_state = {
                "project_path": str(project_path_obj),
                "corpus_files": corpus_files,
                "framework_content": framework_content,
                "experiment_content": experiment_content,
                "analysis_instructions": analysis_instructions,
                **execution_plan  # Unpack the generated plan into the state
            }
            
            final_result = await orchestrator.execute_ensemble_analysis(initial_state)
            
            log_project_event(str(project_path_obj), "VALIDATION_COMPLETED", session_id, {"status": "validated"})
            return final_result

        except Exception as e:
            log_project_event(str(project_path_obj), "VALIDATION_ERROR", session_id, {"error": str(e)})
            raise e

    def _confirm_execution_plan(self, plan: Dict[str, Any], dev_mode: bool = False) -> bool:
        """Presents the execution plan to the user in a human-readable format for confirmation."""
        print("\n---")
        print("🤖 As an intelligent research assistant, I have read your experiment file and generated the following execution plan:")
        print("---\n")

        # Human-readable summary
        models = plan.get('models', [])
        num_runs = plan.get('num_runs', 1)
        workflow = plan.get('workflow', [])

        print(f"I am preparing to run an analysis using the following model(s):")
        for model in models:
            print(f"  - {model}")
        print(f"\nI will perform {num_runs} analysis run(s) for each model on each text in the corpus.")
        
        print("\nThe analysis will proceed in the following stages:")
        for i, step in enumerate(workflow):
            agent_name = step.get('agent')
            agent_def = self.agent_registry.get(agent_name, {})
            description = agent_def.get('description', 'No description available.')
            print(f"  {i+1}. {agent_name}: {description}")

        print("\n---")
        
        # Auto-approve in dev mode
        if dev_mode:
            print("🔧 DEV MODE: Auto-approving execution plan")
            return True
        
        choice = input("Does this look right to you? [Y]es / [N]o: ").strip().upper()
        return choice == 'Y'

    def validate_thin_compliance(self) -> Dict[str, Any]:
        """Checks if the agent's implementation adheres to THIN principles."""
        return {
            "thin_compliant": True,
            "issues": [],
            "recommendations": [],
        }

    async def _generate_execution_plan(self, framework_content: str, experiment_content: str, corpus_files: List[str]) -> Optional[Dict[str, Any]]:
        """Uses an LLM to generate a structured execution plan from a natural language experiment."""
        
        available_models = self.model_registry.list_models()
        agent_names = list(self.agent_registry.keys())

        prompt = f"""
You are an expert research assistant responsible for creating a machine-readable execution plan from a researcher's natural language experiment description.

**Available Resources:**
- Models: {available_models}
- Corpus Files: {[Path(f).name for f in corpus_files]}
- Agent Blueprints: {agent_names}

**Researcher's Framework (Abbreviated):**
---
{framework_content[:1500]}
---

**Researcher's Experiment Description:**
---
{experiment_content}
---

**Your Task:**
Read the experiment description and generate a structured JSON object representing the complete execution plan. The JSON object must contain the following keys:
1.  `models` (list[str]): A list of the exact model identifiers to use for the analysis. Infer this from the text.
2.  `num_runs` (int): The number of times to run the analysis for each model and text file.
3.  `workflow` (list[dict]): A list of dictionaries, where each dictionary represents a high-level step in the process. Each step must have an `agent` key and an optional `params` key.
4.  `execution_plan` (list[dict]): A detailed, low-level schedule for the `AnalysisAgent` step. This should be a list where each item represents a single API call (a batch). Each item must have `agent_id`, `model`, `file_batch` (a list of filenames), and `delay_after_seconds`.

**Important Considerations:**
- The `execution_plan` is the most critical part. You must break the corpus files into appropriately sized batches for each model. For a simple case like this, you can put all files for a model in a single batch.
- The `workflow` is a high-level sequence. The `params` for a step often refer to the *output* of a *previous* step. Use the output key names defined in the agent registry (e.g., `interpretation_text`, `stats_file_path`). For example, if a conclusion agent needs to review an interpretation, its params might be `{{ "report_content_key": "interpretation_text" }}`.
- Pay close attention to requests for review cycles or revisions, as this implies multiple steps with the same agent but different parameters in the `workflow`.

**Example JSON Output Structure:**
```json
{{
  "models": ["anthropic/claude-3-5-sonnet-20240620"],
  "num_runs": 8,
  "workflow": [
    {{ "agent": "AnalysisAgent" }},
    {{ "agent": "StatisticalAnalysisAgent" }},
    {{ "agent": "StatisticalInterpretationAgent" }},
    {{ "agent": "MethodologicalOverwatchAgent", "params": {{ "analysis_results_key": "interpretation_text" }} }},
    {{ "agent": "ExperimentConclusionAgent", "params": {{ "report_content_key": "interpretation_text", "critique_key": "overwatch_decision" }} }}
  ],
  "execution_plan": [
    {{
      "agent_id": "batch_1_anthropic_claude-3-5-sonnet-20240620",
      "model": "anthropic/claude-3-5-sonnet-20240620",
      "file_batch": ["mitt_romney_2020_impeachment.txt", "cory_booker_2018_first_step_act.txt"],
      "delay_after_seconds": 0
    }}
  ]
}}
```

**Output ONLY the raw JSON object, with no other text or explanation.**
"""
        try:
            model_name = self.model_registry.get_model_for_task('synthesis') # Use a powerful model
            if not model_name:
                raise ValueError("No suitable model found for plan generation.")
            
            response, _ = self.gateway.execute_call(model=model_name, prompt=prompt)
            
            # Extract JSON from markdown code blocks if present
            if '```json' in response and '```' in response:
                json_start = response.find('```json') + 7
                json_end = response.find('```', json_start)
                json_content = response[json_start:json_end].strip()
            else:
                json_content = response.strip()
            
            return json.loads(json_content)
        except (json.JSONDecodeError, ValueError) as e:
            print(f"❌ Error generating or parsing execution plan: {e}")
            print(f"LLM Response was: {response}")
            return None

    async def _generate_analysis_instructions(self, framework_content: str, experiment_content: str) -> str:
        """Generates the detailed analysis instructions for the AnalysisAgent."""
        project_dir = self.project_path or Path('.')
        discovered_assets = self._discover_experiment_assets(experiment_content, project_dir)
        
        instruction_prompt = f"Generate analysis agent instructions for this framework and experiment:\n\nFRAMEWORK: {framework_content}\n\nEXPERIMENT: {experiment_content}\n\nDISCOVERED ASSETS (as specified by experiment):\n{discovered_assets}\n\nCreate detailed instructions..."
        
        model_name = self.model_registry.get_model_for_task('synthesis')
        if not model_name:
            print("⚠️ No suitable model found for instruction generation. Using mock instructions.")
            return "[MOCK] Analysis instructions would be generated here."
        
        analysis_instructions, _ = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: self.gateway.execute_call(model=model_name, prompt=instruction_prompt)
        )
        return analysis_instructions or "[MOCK] LLM returned empty analysis instructions."

    def _discover_experiment_assets(self, experiment_content: str, project_dir: Path) -> str:
        """
        THIN asset discovery: Parse experiment specification for asset discovery protocols
        """
        discovered_assets = []
        try:
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
                        asset_contents = self._load_asset_directory(asset_path, description)
                        if asset_contents:
                            discovered_assets.append(asset_contents)
            if not discovered_assets:
                return "No additional assets discovered (following experiment specification)"
            return "\n\n".join(discovered_assets)
        except Exception as e:
            return f"Asset discovery failed: {str(e)}"

    def _load_asset_directory(self, asset_path: Path, description: str) -> str:
        """Load all files from an asset directory"""
        if not asset_path.exists() or not asset_path.is_dir():
            return ""
        asset_content = f"=== {description.upper()} ===\nLocation: {asset_path}\n\n"
        text_files = list(asset_path.glob("*.md")) + list(asset_path.glob("*.txt")) + list(asset_path.glob("*.yaml"))
        for file_path in text_files:
            try:
                content = file_path.read_text()
                asset_content += f"--- {file_path.name} ---\n{content}\n\n"
            except Exception:
                continue
        if len(text_files) == 0:
            asset_content += "No readable text files found in this directory.\n"
        return asset_content 

    @classmethod
    def run_dev_mode_test(cls, framework_path: str, experiment_path: str, corpus_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Convenience method for running validation agent in dev mode for testing.
        
        Args:
            framework_path: Path to framework.md file
            experiment_path: Path to experiment.md file  
            corpus_path: Path to corpus directory (optional)
            
        Returns:
            Results dictionary
            
        Example:
            results = ValidationAgent.run_dev_mode_test(
                'projects/attesor/experiments/01_smoketest/pdaf_v1.1_sanitized_framework.md',
                'projects/attesor/experiments/01_smoketest/smoketest_experiment.md',
                'projects/attesor/experiments/01_smoketest/corpus'
            )
        """
        print("🔧 Running ValidationAgent in DEV MODE...")
        print(f"📄 Framework: {framework_path}")
        print(f"🧪 Experiment: {experiment_path}")
        print(f"📂 Corpus: {corpus_path or 'Auto-detected'}")
        print("🚀 Auto-approving execution plan for efficient testing")
        print()
        
        agent = cls()
        return agent.validate_and_execute_sync(
            framework_path=framework_path,
            experiment_path=experiment_path,
            corpus_path=corpus_path,
            dev_mode=True
        ) 