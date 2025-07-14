#!/usr/bin/env python3
"""
Simple Ensemble Orchestrator - THIN pipeline execution
======================================================

THIN Principle: Simple linear pipeline with LLM intelligence at each step.
No complex conversation management - just validated assets -> ensemble analysis -> synthesis.

Pipeline:
1. Receive validated assets from ValidationAgent
2. Spawn analysis agents (one per corpus text)
3. Synthesis agent aggregates results and notes outliers
4. Moderator agent organizes discussion about outliers only (if needed)
5. Referee agent arbitrates disagreements (if needed)
6. Final synthesis agent packages results for persistence
"""

import sys
import asyncio
import json
import redis
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
import os # Added for os.urandom
import yaml
import re

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    from discernus.gateway.model_registry import ModelRegistry
    from discernus.gateway.llm_gateway import LLMGateway
    from discernus.core.conversation_logger import ConversationLogger
    from discernus.core.secure_code_executor import SecureCodeExecutor
    from discernus.agents.statistical_analysis_configuration_agent import StatisticalAnalysisConfigurationAgent
    from discernus.agents.statistical_interpretation_agent import StatisticalInterpretationAgent
    from discernus.agents.experiment_conclusion_agent import ExperimentConclusionAgent
    from discernus.agents.methodological_overwatch_agent import MethodologicalOverwatchAgent
    DEPENDENCIES_AVAILABLE = True
except ImportError as e:
    print(f"EnsembleOrchestrator dependencies not available: {e}")
    DEPENDENCIES_AVAILABLE = False

class EnsembleOrchestrator:
    """
    THIN ensemble orchestrator - simple linear pipeline execution
    """
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.results_path = self.project_path / "results"
        self.results_path.mkdir(exist_ok=True)
        
        # Core components with improved LLM client
        if not DEPENDENCIES_AVAILABLE:
            raise ImportError("EnsembleOrchestrator dependencies not available. Please check your environment.")
            
        try:
            # Use our new, clean components
            self.model_registry = ModelRegistry()
            self.gateway = LLMGateway(self.model_registry) # Pass registry to gateway
            self.statistical_config_agent = StatisticalAnalysisConfigurationAgent()
            print("✅ EnsembleOrchestrator using ModelRegistry, LLMGateway, and StatisticalAnalysisConfigurationAgent")
        except Exception as e:
            print(f"❌ EnsembleOrchestrator: Failed to initialize gateway components: {e}")
            raise e
            
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
        self.logger = None  # Will be initialized per session
        
        # Session state
        self.session_id = None
        self.analysis_results = []
        self.analysis_matrix = {}
        self.synthesis_result = None
        self.outliers = []
        self.statistical_plan = None
        
    def _parse_experiment_config(self, validation_results: Dict[str, Any]) -> Dict[str, Any]:
        """Parse YAML config block from experiment.md"""
        
        # Default configuration
        default_config = {
            'models': ['vertex_ai/gemini-2.5-flash'],
            'remove_synthesis': False,
            'batch_size': 1,
            'num_runs': 1
        }
        
        # CRITICAL FIX: Read directly from experiment.md file to get latest configuration
        # This ensures we get the configuration after any health check adjustments
        experiment_file = self.project_path / "experiment.md"
        
        if not experiment_file.exists():
            print(f"⚠️  Experiment file not found: {experiment_file}")
            return default_config
            
        try:
            experiment_definition = experiment_file.read_text()
            
            # Extract YAML block from markdown
            yaml_match = re.search(r'```yaml\n(.*?)```', experiment_definition, re.DOTALL)
            if not yaml_match:
                print(f"⚠️  No YAML configuration found in experiment.md")
                return default_config
                
            yaml_content = yaml_match.group(1)
            config = yaml.safe_load(yaml_content)
            
            # Merge with defaults
            default_config.update(config)
            print(f"✅ Parsed experiment config: {default_config}")
            return default_config
            
        except Exception as e:
            print(f"⚠️  Could not parse experiment YAML, using defaults. Error: {e}")
            return default_config

    async def execute_ensemble_analysis(self, validation_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        THIN Principle: LLM decides research workflow based on experiment requirements
        """
        try:
            # Initialize session
            self._init_session_logging()

            # Step 1: Validate statistical analysis plan BEFORE running analysis
            experiment_path = self.project_path / "experiment.md"
            self.statistical_plan = self.statistical_config_agent.generate_statistical_plan(str(experiment_path))
            self._log_system_event("STATISTICAL_PLAN_GENERATED", self.statistical_plan)

            if self.statistical_plan.get("validation_status") != "complete":
                raise ValueError(f"Statistical plan validation failed: {self.statistical_plan.get('notes', 'No notes provided.')}")

            # Parse experiment configuration from YAML
            experiment_config = self._parse_experiment_config(validation_results)
            
            self._log_system_event("ENSEMBLE_STARTED", {
                "corpus_file_count": len(validation_results.get('corpus_files', [])),
                "session_id": self.session_id,
                "experiment_config": experiment_config
            })
            
            # Step 1: Execute the analysis - use spawn_analysis_agents for multiple runs and statistical analysis
            # This ensures proper analysis_matrix population for Cronbach's Alpha and other statistical tests
            await self._spawn_analysis_agents(validation_results, experiment_config)
            
            # Step 2: MID-FLIGHT OVERWATCH CHECKPOINT
            overwatch_agent = MethodologicalOverwatchAgent()
            # The analysis_results list is now clean and contains no exceptions
            overwatch_decision = overwatch_agent.review_analysis_results(self.analysis_results)
            self._log_system_event("OVERWATCH_AGENT_REVIEW", overwatch_decision)

            if overwatch_decision.get("decision") == "TERMINATE":
                raise SystemExit(f"METHODOLOGICAL OVERWATCH: Execution terminated. Reason: {overwatch_decision.get('reason')}")

            # Step 3: Ask LLM what to do next based on experiment requirements
            coordination_prompt = f"""
            Analysis complete. Here are the analysis results:
            {json.dumps(self.analysis_results, indent=2)}
            
            And here are the experiment requirements:
            {validation_results.get('experiment', {}).get('definition', 'No experiment definition provided')}
            
            Experiment Configuration:
            {json.dumps(experiment_config, indent=2)}

            Based on all the information above (the analysis results, the experiment requirements, and the specific YAML configuration), what should happen next?
            Options:
            - If experiment requires synthesis/moderation/referee: respond "ADVERSARIAL_SYNTHESIS"
            - If experiment requires bias isolation (e.g., remove_synthesis: true): respond "RAW_AGGREGATION" 
            - If you need more information: respond "NEED_MORE_INFO"
            
            Respond with just the action name.
            """
            
            model_name = self.model_registry.get_model_for_task('coordination')
            if not model_name:
                print("⚠️ No suitable model found for coordination, using default.")
                model_name = 'vertex_ai/gemini-1.5-flash-latest' # A reasonable default
            next_action = await self._call_llm_async(coordination_prompt, "coordination_llm", model_name)
            
            # Step 4: Execute whatever the LLM decided (THIN: dumb execution)
            if "RAW_AGGREGATION" in next_action.upper():
                final_results = await self._simple_aggregation()
            elif "ADVERSARIAL_SYNTHESIS" in next_action.upper():
                final_results = await self._adversarial_workflow()
            else:
                # Default to simple aggregation if unclear
                final_results = await self._simple_aggregation()

            # Step 5: Run statistical analysis based on the validated plan
            stats_results_path = await self._run_statistical_analysis(self.statistical_plan)

            # Step 6: Interpret statistical results and append to the report
            if final_results.get("report_path") and stats_results_path:
                await self._interpret_and_append_stats(final_results["report_path"], stats_results_path)

                # Step 7: Perform the final methodological audit and append it
                await self._perform_final_audit(final_results["report_path"], stats_results_path)

            self._log_system_event("ENSEMBLE_COMPLETED", {
                "session_id": self.session_id,
                "final_status": "success",
                "workflow_used": next_action
            })
            
            return {
                "status": "success",
                "session_id": self.session_id,
                "results": final_results,
                "workflow": next_action
            }
            
        except Exception as e:
            self._log_system_event("ENSEMBLE_ERROR", {
                "session_id": self.session_id,
                "error": str(e)
            })
            return {
                "status": "error",
                "session_id": self.session_id,
                "message": f"Ensemble analysis failed: {str(e)}"
            }

    async def _execute_planned_analysis(self, schedule: List[Dict[str, Any]]):
        """
        Executes a pre-computed analysis plan from the ExecutionPlannerAgent.
        This is a THIN method that simply iterates through a schedule.
        """
        if not schedule:
            raise ValueError("Execution plan schedule is empty. Cannot proceed.")

        all_results = []
        for i, step in enumerate(schedule):
            self._log_system_event("EXECUTING_PLAN_STEP", {
                "step": i + 1,
                "total_steps": len(schedule),
                "agent_id": step.get('agent_id'),
                "model": step.get('model'),
                "batch_size": len(step.get('file_batch', [])),
            })
            
            try:
                response = await self._call_llm_async(step['prompt'], step['agent_id'], step['model'])
                # Here we would need to parse the single response to get individual results for each file in the batch.
                # For now, we'll store the raw batch response.
                all_results.append({
                    "agent_id": step.get('agent_id'),
                    "model_name": step.get('model'),
                    "analysis_response": response,
                    "file_batch": step.get('file_batch')
                })
            except Exception as e:
                all_results.append(e) # Store exception to be filtered later

            # Honor the calculated delay to respect rate limits
            if step.get('delay_after_seconds', 0) > 0:
                await asyncio.sleep(step['delay_after_seconds'])

        # Filter out exceptions, similar to the old method
        successful_results = [r for r in all_results if not isinstance(r, Exception)]
        self.analysis_results = successful_results

    async def _perform_final_audit(self, report_path: str, stats_path: str):
        """Spawns the conclusion agent to perform a final audit and appends it."""
        self._log_system_event("FINAL_AUDIT_STARTED", {
            "project_path": str(self.project_path),
            "report_path": report_path,
        })
        try:
            conclusion_agent = ExperimentConclusionAgent()
            audit_text = conclusion_agent.generate_final_audit(
                project_path=str(self.project_path),
                report_file_path=report_path,
                stats_file_path=stats_path
            )

            # Append the audit to the final report
            with open(report_path, "a") as f:
                f.write("\n\n" + audit_text)

            self._log_system_event("FINAL_AUDIT_COMPLETED", {
                "report_path": report_path,
                "audit_length": len(audit_text)
            })
        except Exception as e:
            self._log_system_event("FINAL_AUDIT_FAILED", {"error": str(e)})

    async def _interpret_and_append_stats(self, report_path: str, stats_path: str):
        """Spawns an agent to interpret stats and appends them to the final report."""
        self._log_system_event("STATISTICAL_INTERPRETATION_STARTED", {
            "report_path": report_path,
            "stats_path": stats_path
        })

        try:
            interpretation_agent = StatisticalInterpretationAgent()
            interpretation_text = interpretation_agent.interpret_statistical_results(
                stats_file_path=stats_path,
                report_file_path=report_path
            )

            # Append the interpretation to the final report
            with open(report_path, "a") as f:
                f.write("\n\n" + interpretation_text)
            
            self._log_system_event("STATISTICAL_INTERPRETATION_COMPLETED", {
                "report_path": report_path,
                "interpretation_length": len(interpretation_text)
            })
        except Exception as e:
            self._log_system_event("STATISTICAL_INTERPRETATION_FAILED", {
                "error": str(e)
            })

    async def _spawn_analysis_agents(self, validation_results: Dict[str, Any], experiment_config: Dict[str, Any]):
        """THIN: Let LLM validate inputs and decide analysis approach"""
        
        validation_prompt = f"""
        You are the input validation agent. Assess these validation results:
        
        {json.dumps(validation_results, indent=2)}
        
        Questions:
        1. Are the inputs sufficient to proceed with analysis?
        2. How many analysis agents should be spawned?
        3. What should each agent analyze?
        
        If inputs are sufficient, respond with: "PROCEED_WITH_ANALYSIS"
        If not, respond with: "INSUFFICIENT_INPUTS" followed by what's missing.
        """
        
        model_name = self.model_registry.get_model_for_task('validation')
        if not model_name:
            print("⚠️ No suitable model found for input validation, using default.")
            model_name = 'vertex_ai/gemini-1.5-flash-latest' # A reasonable default
        validation_decision = await self._call_llm_async(validation_prompt, "input_validation_agent", model_name)
        
        if "INSUFFICIENT_INPUTS" in validation_decision.upper():
            raise ValueError(f"LLM input validation failed: {validation_decision}")
        
        corpus_files = validation_results.get('corpus_files', [])
        analysis_instructions = validation_results.get('analysis_agent_instructions', '')
        models = experiment_config.get('models', ['vertex_ai/gemini-2.5-flash'])
        
        self._log_system_event("ANALYSIS_AGENTS_SPAWNING", {
            "agent_count": len(corpus_files) * len(models),
            "models": models,
            "instructions_preview": analysis_instructions[:200] + "..." if len(analysis_instructions) > 200 else analysis_instructions
        })
        
        # Process each corpus file with its own analysis agent for each model
        analysis_tasks = []
        num_runs = experiment_config.get('num_runs', 1)
        for run in range(num_runs):
            for model_name in models:
                for i, corpus_file in enumerate(corpus_files):
                    agent_id = f"analysis_agent_run{run+1}_{model_name.replace('/', '_')}_{i+1}"
                    task = self._run_analysis_agent(agent_id, corpus_file, analysis_instructions, model_name, run + 1)
                    analysis_tasks.append(task)
        
        # THIN: Let LLM decide execution strategy
        execution_prompt = f"""
        You are the execution strategy agent. Decide how to run {len(analysis_tasks)} analysis tasks:
        
        Options:
        - "SEQUENTIAL": Run one at a time (safer, slower)
        - "PARALLEL": Run all at once (faster, more resource intensive)
        
        Consider system load and task complexity. Respond with just the strategy name.
        """
        
        model_name = self.model_registry.get_model_for_task('coordination')
        if not model_name:
            print("⚠️ No suitable model found for execution strategy, using default.")
            model_name = 'vertex_ai/gemini-1.5-flash-latest' # A reasonable default
        execution_strategy = await self._call_llm_async(execution_prompt, "execution_strategy_agent", model_name)
        
        if "SEQUENTIAL" in execution_strategy.upper():
            print("🔧 LLM chose SEQUENTIAL execution")
            raw_results = []
            for i, task in enumerate(analysis_tasks):
                result = await task
                raw_results.append(result)
        else:
            print("🔧 LLM chose PARALLEL execution")
            import asyncio
            raw_results = await asyncio.gather(*analysis_tasks, return_exceptions=True)
        
        # --- Single, Early Filtering of Exceptions ---
        successful_results: List[Dict[str, Any]] = []
        failed_count = 0
        
        for i, result in enumerate(raw_results):
            if isinstance(result, Exception):
                failed_count += 1
                self._log_system_event("ANALYSIS_AGENT_ERROR", {
                    "agent_id": f"analysis_agent_{i+1}",
                    "error": str(result)
                })
            else:
                # result is guaranteed to be Dict[str, Any] here - explicit cast for type checker
                typed_result: Dict[str, Any] = result  # type: ignore
                successful_results.append(typed_result)

        # Overwrite self.analysis_results with the clean, typed list
        self.analysis_results = successful_results

        # Only ask about failure handling if there were actual failures and we have some successes
        if failed_count > 0 and self.analysis_results:
            results_prompt = f"""
            You are the results processing agent. Process these analysis results:
            
            There are {failed_count} failed analyses and {len(self.analysis_results)} successful analyses. What should we do?
            - "FILTER": Continue with the {len(self.analysis_results)} successful results
            - "ABORT": Stop processing due to the failures
            
            Respond with just the action name.
            """
            
            model_name = self.model_registry.get_model_for_task('coordination')
            if not model_name:
                print("⚠️ No suitable model found for results processing, using default.")
                model_name = 'vertex_ai/gemini-1.5-flash-latest'
            results_decision = await self._call_llm_async(results_prompt, "results_processing_agent", model_name)
            
            if "ABORT" in results_decision.upper():
                raise RuntimeError(f"LLM decided to abort due to {failed_count} failed analyses")
        
        # Populate the analysis matrix from the now-clean results
        for result in self.analysis_results:
            file_name = result.get("file_name")
            model_name = result.get("model_name")
            run_num = result.get("run_num")
            if file_name and model_name:
                if file_name not in self.analysis_matrix:
                    self.analysis_matrix[file_name] = {}
                if model_name not in self.analysis_matrix[file_name]:
                    self.analysis_matrix[file_name][model_name] = {}
                self.analysis_matrix[file_name][model_name][run_num] = result

        self._log_system_event("ANALYSIS_AGENTS_COMPLETED", {
            "successful_count": len(self.analysis_results),
            "failed_count": failed_count,
            "analysis_matrix": self.analysis_matrix
        })
    
    async def _run_statistical_analysis(self, statistical_plan: Dict[str, Any]) -> Optional[str]:
        """Run statistical analysis and return the path to the results file."""
        
        self._log_system_event("STATISTICAL_ANALYSIS_STARTED", {
            "session_id": self.session_id,
            "statistical_plan": statistical_plan
        })

        # Prepare data for statistical analysis
        statistical_data = self._prepare_statistical_data()

        # Generate Python code for statistical analysis based on the plan
        required_tests = [test['test_name'] for test in statistical_plan.get('required_tests', [])]
        
        code_generation_prompt = f"""
        You are a data science expert. Generate Python code to perform the following statistical analyses on the provided data: {', '.join(required_tests)}

        The data is in a dictionary named 'statistical_data':
        {json.dumps(statistical_data, indent=2)}

        The data is a dictionary where the keys are text filenames and the values are dictionaries
        where the keys are model names and the values are lists of analysis results for each run.

        Your task is to generate Python code to perform the requested tests and store the results in a dictionary named 'statistical_results'.
        The code should use the pandas and scipy libraries.
        """

        model_name = self.model_registry.get_model_for_task('code_generation')
        if not model_name:
            print("⚠️ No suitable model found for code generation, using default.")
            model_name = 'vertex_ai/gemini-1.5-pro-latest' # A powerful model for code
        statistical_code = await self._call_llm_async(code_generation_prompt, "statistical_code_generator", model_name)

        # Execute the statistical analysis code
        executor = SecureCodeExecutor()
        execution_result = executor.execute_code(statistical_code, {'statistical_data': statistical_data})

        # Save the statistical analysis results
        if execution_result['success']:
            results_file = self.session_results_path / "statistical_analysis_results.json"
            results_file.write_text(json.dumps(execution_result['result_data'], indent=2))
            
            self._log_system_event("STATISTICAL_ANALYSIS_COMPLETED", {
                "session_id": self.session_id,
                "results_file": str(results_file)
            })
            return str(results_file)
        else:
            self._log_system_event("STATISTICAL_ANALYSIS_FAILED", {
                "session_id": self.session_id,
                "error": execution_result['error']
            })
        return None

    def _prepare_statistical_data(self):
        """Prepare the analysis matrix for statistical analysis."""
        statistical_data = {}
        for text, models in self.analysis_matrix.items():
            statistical_data[text] = {}
            for model, runs in models.items():
                statistical_data[text][model] = []
                for run, result in runs.items():
                    # Assuming the analysis_response is a JSON string with a 'score' field
                    try:
                        analysis_data = json.loads(result['analysis_response'])
                        statistical_data[text][model].append(analysis_data.get('score'))
                    except (json.JSONDecodeError, KeyError):
                        # Handle cases where the score is not available or the response is not a valid JSON
                        statistical_data[text][model].append(None)
        return statistical_data

    async def _run_analysis_agent(self, agent_id: str, corpus_file: str, instructions: str, model_name: str, run_num: int) -> Dict[str, Any]:
        """Run a single analysis agent on one corpus text"""
        
        self._log_system_event("AGENT_SPAWNED", {
            "agent_id": agent_id,
            "agent_type": "analysis_agent",
            "corpus_file": Path(corpus_file).name,
            "model_name": model_name,
            "run_num": run_num
        })
        
        # Read the corpus text
        corpus_text = Path(corpus_file).read_text()
        
        # Create analysis prompt
        analysis_prompt = f"""You are {agent_id}, a framework analysis specialist.

ANALYSIS INSTRUCTIONS:
{instructions}

TEXT TO ANALYZE:
File: {Path(corpus_file).name}
Content:
{corpus_text}

TASK: Apply the framework systematically to this text. Provide structured output with:
1. Framework dimension scores (with confidence intervals)
2. Specific textual evidence for each score
3. Systematic reasoning for your analysis

Be precise and cite specific text passages to support your scores."""

        # Call LLM - The model_name for the core analysis is passed in from the experiment config
        response = await self._call_llm_async(analysis_prompt, agent_id, model_name)
        
        self._log_system_event("AGENT_COMPLETED", {
            "agent_id": agent_id,
            "agent_type": "analysis_agent",
            "response_length": len(response) if response else 0
        })
        
        return {
            "agent_id": agent_id,
            "corpus_file": corpus_file,
            "analysis_response": response,
            "file_name": Path(corpus_file).name,
            "model_name": model_name,
            "run_num": run_num
        }
    
    async def _run_synthesis_agent(self):
        """Synthesis agent aggregates results and identifies outliers"""
        
        self._log_system_event("AGENT_SPAWNED", {
            "agent_id": "synthesis_agent",
            "agent_type": "synthesis_agent",
            "input_count": len(self.analysis_results)
        })
        
        # THIN: Let LLM handle result formatting instead of assuming structure
        formatting_prompt = f"""
        You are the results formatting agent. Format these analysis results for synthesis:
        
        Raw results: {self.analysis_results}
        
        Convert to human-readable format for synthesis. Handle any errors gracefully.
        """
        
        model_name = self.model_registry.get_model_for_task('synthesis')
        if not model_name:
            print("⚠️ No suitable model found for formatting, using default.")
            model_name = 'vertex_ai/gemini-1.5-flash-latest' # A reasonable default
        formatted_results = await self._call_llm_async(formatting_prompt, "results_formatting_agent", model_name)
        
        synthesis_prompt = f"""You are the synthesis_agent. Your job is to:

1. Aggregate the analysis results from {len(self.analysis_results)} analysis agents
2. Identify patterns and trends across texts
3. Note any significant outliers or disagreements
4. Provide preliminary synthesis

ANALYSIS RESULTS TO SYNTHESIZE:
{formatted_results}

TASK: 
1. Create aggregate statistics and patterns
2. Identify outliers (texts or scores that deviate significantly)
3. Note areas of uncertainty or disagreement
4. Provide preliminary conclusions

FORMAT YOUR RESPONSE AS:
AGGREGATE PATTERNS: [summary of overall patterns]
OUTLIERS DETECTED: [list any significant outliers with reasons]
PRELIMINARY CONCLUSIONS: [initial synthesis]
CONFIDENCE LEVEL: [your confidence in these results]"""

        model_name = self.model_registry.get_model_for_task('synthesis')
        if not model_name:
            print("⚠️ No suitable model found for synthesis, using default.")
            model_name = 'vertex_ai/gemini-1.5-flash-latest' # A reasonable default
        self.synthesis_result = await self._call_llm_async(synthesis_prompt, "synthesis_agent", model_name)
        
        # Extract outliers for potential discussion
        if "OUTLIERS DETECTED:" in self.synthesis_result:
            outlier_section = self.synthesis_result.split("OUTLIERS DETECTED:")[1].split("PRELIMINARY CONCLUSIONS:")[0]
            if "None" not in outlier_section and len(outlier_section.strip()) > 10:
                self.outliers = [outlier_section.strip()]
        
        self._log_system_event("AGENT_COMPLETED", {
            "agent_id": "synthesis_agent",
            "agent_type": "synthesis_agent",
            "outliers_found": len(self.outliers)
        })
    
    async def _handle_outliers(self):
        """THIN: Let LLM decide if outliers need handling"""
        
        outlier_assessment_prompt = f"""
        You are the outlier assessment agent. Review the current outlier situation:
        
        Current outliers identified: {getattr(self, 'outliers', [])}
        
        Do these outliers require discussion and resolution?
        - If YES: respond "HANDLE_OUTLIERS" 
        - If NO: respond "SKIP_OUTLIERS"
        
        Respond with just the action name.
        """
        
        model_name = self.model_registry.get_model_for_task('coordination')
        if not model_name:
            print("⚠️ No suitable model found for outlier assessment, using default.")
            model_name = 'vertex_ai/gemini-1.5-flash-latest' # A reasonable default
        outlier_decision = await self._call_llm_async(outlier_assessment_prompt, "outlier_assessment_agent", model_name)
        
        if "HANDLE_OUTLIERS" in outlier_decision.upper():
            self._log_system_event("OUTLIER_DISCUSSION_STARTED", {
                "outlier_count": len(getattr(self, 'outliers', []))
            })
            
            # Moderator agent organizes discussion about outliers
            await self._run_moderator_agent()
            
            # Referee agent arbitrates if there are still disagreements
            await self._run_referee_agent()
            
            self._log_system_event("OUTLIER_DISCUSSION_COMPLETED", {
                "resolution_method": "moderator_referee_arbitration"
            })
        else:
            self._log_system_event("OUTLIER_DISCUSSION_SKIPPED", {
                "reason": "LLM determined outliers do not need discussion"
            })
    
    async def _run_moderator_agent(self):
        """Moderator agent organizes focused discussion about outliers only"""
        
        self._log_system_event("AGENT_SPAWNED", {
            "agent_id": "moderator_agent",
            "agent_type": "moderator_agent",
            "focus": "outlier_discussion"
        })
        
        moderator_prompt = f"""You are the moderator_agent. Focus ONLY on outliers that need discussion.

SYNTHESIS RESULT:
{self.synthesis_result}

OUTLIERS TO DISCUSS:
{chr(10).join(self.outliers)}

TASK: Organize a structured discussion about these outliers:
1. Why might these outliers exist?
2. Are they methodological issues or genuine findings?
3. What additional evidence would help resolve them?
4. Should any scores be reconsidered?

Provide focused recommendations for outlier resolution."""

        model_name = self.model_registry.get_model_for_task('synthesis')
        if not model_name:
            print("⚠️ No suitable model found for moderator, using default.")
            model_name = 'vertex_ai/gemini-1.5-flash-latest' # A reasonable default
        moderator_response = await self._call_llm_async(moderator_prompt, "moderator_agent", model_name)
        
        self._log_system_event("AGENT_COMPLETED", {
            "agent_id": "moderator_agent",
            "agent_type": "moderator_agent",
            "recommendations_length": len(moderator_response) if moderator_response else 0
        })
        
        # Store moderator recommendations
        self.moderator_recommendations = moderator_response
    
    async def _run_referee_agent(self):
        """Referee agent arbitrates final decisions about outliers"""
        
        self._log_system_event("AGENT_SPAWNED", {
            "agent_id": "referee_agent",
            "agent_type": "referee_agent",
            "arbitration_scope": "outlier_resolution"
        })
        
        referee_prompt = f"""You are the referee_agent. Make final arbitration decisions.

ORIGINAL SYNTHESIS:
{self.synthesis_result}

MODERATOR RECOMMENDATIONS:
{getattr(self, 'moderator_recommendations', 'No moderator recommendations available')}

TASK: Make final decisions about outliers:
1. Which outliers are legitimate findings vs. methodological issues?
2. What are the final recommended scores/interpretations?
3. What confidence level should be assigned to final results?

Provide clear, evidence-based arbitration decisions."""

        model_name = self.model_registry.get_model_for_task('synthesis')
        if not model_name:
            print("⚠️ No suitable model found for referee, using default.")
            model_name = 'vertex_ai/gemini-1.5-flash-latest' # A reasonable default
        referee_decision = await self._call_llm_async(referee_prompt, "referee_agent", model_name)
        
        self._log_system_event("AGENT_COMPLETED", {
            "agent_id": "referee_agent",
            "agent_type": "referee_agent",
            "arbitration_complete": True
        })
        
        # Store referee decision
        self.referee_decision = referee_decision
    
    async def _final_synthesis(self) -> Dict[str, Any]:
        """Final synthesis agent packages results for persistence"""
        
        self._log_system_event("AGENT_SPAWNED", {
            "agent_id": "final_synthesis_agent",
            "agent_type": "final_synthesis_agent",
            "packaging_results": True
        })
        
        # Determine what synthesis to use
        if hasattr(self, 'referee_decision') and self.referee_decision:
            final_synthesis_input = self.referee_decision
            synthesis_type = "referee_arbitrated"
        elif self.synthesis_result:
            final_synthesis_input = self.synthesis_result
            synthesis_type = "standard_synthesis"
        else:
            final_synthesis_input = "No synthesis available"
            synthesis_type = "fallback"
        
        final_prompt = f"""You are the final_synthesis_agent. Package the complete analysis for academic use.

ANALYSIS INPUT TYPE: {synthesis_type}

FINAL SYNTHESIS INPUT:
{final_synthesis_input}

TASK: Create publication-ready final report including:
1. Executive summary of findings
2. Methodology summary
3. Key results with confidence levels
4. Limitations and caveats
5. Recommendations for future research

Format as structured academic output suitable for peer review."""

        model_name = self.model_registry.get_model_for_task('synthesis')
        if not model_name:
            print("⚠️ No suitable model found for final synthesis, using default.")
            model_name = 'vertex_ai/gemini-1.5-flash-latest' # A reasonable default
        final_report = await self._call_llm_async(final_prompt, "final_synthesis_agent", model_name)
        
        # Save results to project
        final_report_path = await self._save_results_to_project(final_report)
        
        self._log_system_event("AGENT_COMPLETED", {
            "agent_id": "final_synthesis_agent",
            "agent_type": "final_synthesis_agent",
            "results_saved": True
        })
        
        return {
            "final_report": final_report,
            "analysis_count": len(self.analysis_results),
            "outliers_handled": len(self.outliers),
            "synthesis_type": synthesis_type,
            "session_id": self.session_id,
            "report_path": final_report_path
        }
    
    async def _simple_aggregation(self) -> Dict[str, Any]:
        """THIN: Simple aggregation without adversarial synthesis"""
        
        final_report_prompt = f"""
        Create a simple aggregation report from these analysis results:
        
        {json.dumps(self.analysis_results, indent=2)}
        
        Provide:
        1. Summary of all analyses
        2. Raw data aggregation  
        3. Basic patterns observed
        4. Complete methodology documentation
        
        No synthesis or arbitration - just clean aggregation for bias isolation.
        """
        
        model_name = self.model_registry.get_model_for_task('synthesis')
        if not model_name:
            print("⚠️ No suitable model found for aggregation, using default.")
            model_name = 'vertex_ai/gemini-1.5-flash-latest' # A reasonable default
        final_report = await self._call_llm_async(final_report_prompt, "aggregation_agent", model_name)
        report_path = await self._save_results_to_project(final_report)
        
        return {
            "type": "simple_aggregation",
            "report": final_report,
            "report_path": report_path,
            "raw_analyses": self.analysis_results
        }
    
    async def _adversarial_workflow(self) -> Dict[str, Any]:
        """THIN: Original adversarial workflow when experiment requires it"""
        
        # Run synthesis agent
        await self._run_synthesis_agent()
        
        # Ask LLM if outliers need handling
        if hasattr(self, 'synthesis_result'):
            outlier_prompt = f"""
            Synthesis complete: {self.synthesis_result}
            
            Do any outliers need discussion? Respond "YES" or "NO".
            """
            
            model_name = self.model_registry.get_model_for_task('coordination')
            if not model_name:
                print("⚠️ No suitable model found for outlier coordination, using default.")
                model_name = 'vertex_ai/gemini-1.5-flash-latest' # A reasonable default
            needs_outlier_discussion = await self._call_llm_async(outlier_prompt, "outlier_coordinator", model_name)
            
            if "YES" in needs_outlier_discussion.upper():
                await self._handle_outliers()
        
        # Final synthesis
        final_results = await self._final_synthesis()
        
        return final_results
    
    async def _save_results_to_project(self, final_report: str) -> Optional[str]:
        """Save results back to the project directory and return the report path."""
        
        # Use the session-specific results path
        results_dir = self.session_results_path
        results_dir.mkdir(exist_ok=True)
        
        # Save final report
        report_path = results_dir / "final_report.md"
        report_path.write_text(final_report)
        
        # Save session metadata
        metadata = {
            "session_id": self.session_id,
            "timestamp": results_dir.name,
            "analysis_count": len(self.analysis_results),
            "outliers_handled": len(self.outliers),
            "project_path": str(self.project_path)
        }
        (results_dir / "session_metadata.json").write_text(json.dumps(metadata, indent=2))
        
        # Create run-specific chronolog for academic integrity and statistical analysis
        files_saved = ["final_report.md", "session_metadata.json"]
        
        # Only create chronolog if we have a valid session_id
        if self.session_id:
            try:
                from discernus.core.project_chronolog import get_project_chronolog
                chronolog = get_project_chronolog(str(self.project_path))
                
                chronolog_result = chronolog.create_run_chronolog(
                    session_id=self.session_id,
                    results_directory=str(results_dir)
                )
                
                if chronolog_result.get('created', False):
                    run_log_path = chronolog_result['run_chronolog_file']
                    files_saved.append(Path(run_log_path).name)
                    print(f"📝 Run chronolog created: {run_log_path}")
                    
                    # Merge the run log into the main project chronolog
                    print(f"Merging run log into master project chronolog...")
                    chronolog.merge_run_log(run_log_path)
                    
                    # Log timing statistics for academic analysis
                    run_stats = chronolog_result.get('run_statistics', {})
                    if run_stats.get('status') == 'statistics_calculated':
                        print(f"⏱️  Analysis duration: {run_stats.get('analysis_duration_seconds', 'N/A')} seconds")
                        print(f"📈 Events per minute: {run_stats.get('events_per_minute', 'N/A'):.2f}")
                        
            except Exception as e:
                print(f"⚠️ Failed to create run chronolog: {e}")
        else:
            print("⚠️ No session_id available, skipping run chronolog creation")
        
        self._log_system_event("RESULTS_SAVED", {
            "results_directory": str(results_dir),
            "files_saved": files_saved
        })
        return str(report_path)
    
    def _init_session_logging(self):
        """Initialize conversation logging for this session"""
        # Generate session ID with timestamp
        timestamp = datetime.now()
        self.session_id = f"session_{timestamp.strftime('%Y%m%d_%H%M%S')}"
        self.conversation_id = f"conversation_{timestamp.strftime('%Y%m%d_%H%M%S')}_{os.urandom(4).hex()}"
        
        # Log session start to project chronolog
        try:
            from discernus.core.project_chronolog import log_project_event
            log_project_event(
                str(self.project_path),
                "ENSEMBLE_SESSION_STARTED",
                self.session_id,
                {
                    "conversation_id": self.conversation_id,
                    "project_path": str(self.project_path)
                }
            )
        except Exception as e:
            print(f"⚠️ Failed to log to project chronolog: {e}")
        
        # Initialize conversation logger if dependencies available
        if DEPENDENCIES_AVAILABLE:
            try:
                self.logger = ConversationLogger(str(self.project_path))
                print(f"✅ Redis event capture ACTIVATED for conversation: {self.conversation_id}")
            except Exception as e:
                print(f"⚠️ Conversation logging failed: {e}")
                self.logger = None
        else:
            self.logger = None

        # Create timestamped results directory
        timestamp_str = timestamp.strftime('%Y-%m-%d_%H-%M-%S')
        self.session_results_path = self.results_path / timestamp_str
        self.session_results_path.mkdir(exist_ok=True)
        
        # Get model information for provenance
        model_info = self._get_model_provenance()
        
        # Save session metadata with model provenance
        metadata = {
            "session_id": self.session_id,
            "conversation_id": self.conversation_id,
            "timestamp": timestamp_str,
            "analysis_count": 0,
            "outliers_handled": 0,
            "project_path": str(self.project_path),
            "model_provenance": model_info
        }
        
        metadata_path = self.session_results_path / "session_metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)

    def _get_model_provenance(self) -> Dict[str, Any]:
        """Extract model information for research provenance"""
        try:
            if not self.model_registry:
                raise ValueError("ModelRegistry not initialized")
            
            # Get all available models from the registry
            available_models = self.model_registry.list_models()
            
            return {
                "available_models": available_models,
                "capture_method": "model_registry_query",
                "capture_timestamp": datetime.now().isoformat(),
                "notes": f"Registry loaded from {self.model_registry.config_path}"
            }
        except Exception as e:
            return {
                "available_models": "error",
                "capture_method": "exception",
                "capture_timestamp": datetime.now().isoformat(),
                "notes": f"Error capturing model info: {str(e)}"
            }
    
    def _log_system_event(self, event_type: str, event_data: Dict[str, Any]):
        """Log system events to Redis and conversation log"""
        
        # Publish to Redis
        redis_event = {
            "timestamp": datetime.utcnow().isoformat(),
            "session_id": self.session_id,
            "event_type": event_type,
            "event_data": event_data
        }
        
        try:
            self.redis_client.publish("soar.ensemble.event", json.dumps(redis_event))
        except:
            pass  # Redis optional for functionality
        
        # Log to conversation logger if available
        if self.logger:
            self.logger.log_llm_message(
                conversation_id=self.conversation_id or self.session_id or "unknown",
                speaker="system",
                message=f"{event_type}: {event_data}",
                metadata={
                    "type": "ensemble_event",
                    "event_type": event_type,
                    "session_id": self.session_id
                }
            )
    
    async def _call_llm_async(self, prompt: str, agent_id: str, model_name: str) -> str:
        """Call LLM asynchronously with proper logging"""
        
        if not self.gateway:
            print(f"🔴 DEBUG: No LLM gateway available for {agent_id}")
            return f"[MOCK RESPONSE] {agent_id} would analyze: {prompt[:100]}..."
        
        try:
            # The model_name parameter is now passed in from the calling method
            print(f"🟡 DEBUG: Starting LLM call for {agent_id} with model {model_name}")
            
            if self.logger:
                self.logger.log_llm_message(
                    conversation_id=self.conversation_id or self.session_id or "unknown",
                    speaker=agent_id,
                    message=prompt,
                    metadata={"type": "llm_request", "agent_id": agent_id, "session_id": self.session_id, "model_name": model_name}
                )
            
            # Make the LLM call
            content, metadata = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.gateway.execute_call(model=model_name, prompt=prompt)
            )
            
            print(f"🟢 DEBUG: Got response for {agent_id}, length: {len(content) if content else 'None'}")
            
            if self.logger:
                self.logger.log_llm_message(
                    conversation_id=self.conversation_id or self.session_id or "unknown",
                    speaker=agent_id,
                    message=content,
                    metadata={"type": "llm_response", "agent_id": agent_id, "session_id": self.session_id, **metadata}
                )
            
            return content
            
        except Exception as e:
            error_msg = f"LLM call failed for {agent_id}: {str(e)}"
            print(f"🔴 DEBUG: Exception in LLM call for {agent_id}: {str(e)}")
            
            if self.logger:
                self.logger.log_llm_message(
                    conversation_id=self.conversation_id or self.session_id or "unknown",
                    speaker="system",
                    message=error_msg,
                    metadata={"type": "llm_error", "agent_id": agent_id, "session_id": self.session_id, "model_name": model_name}
                )
            
            return f"[ERROR] {error_msg}"