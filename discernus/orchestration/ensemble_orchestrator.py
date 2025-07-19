#!/usr/bin/env python3
"""
🚨 DEPRECATED: EnsembleOrchestrator (July 18, 2025)
===============================================

**DEPRECATION NOTICE**: This EnsembleOrchestrator is deprecated and will be removed in a future version.

**Why Deprecated**: 
- Creates directory structures that violate Research Provenance Guide v3.0
- Superseded by WorkflowOrchestrator which follows proper architectural patterns
- Part of architectural cleanup to prevent confusion between orchestrator types

**Current Replacement**: Use `WorkflowOrchestrator` from `discernus.orchestration.workflow_orchestrator`

**Migration Timeline**: 
- July 18, 2025: All new development should use WorkflowOrchestrator
- Next release: EnsembleOrchestrator will be removed completely

**For Existing Code**: Replace imports:
```python
# OLD (deprecated)
from discernus.orchestration.ensemble_orchestrator import EnsembleOrchestrator

# NEW (correct)  
from discernus.orchestration.workflow_orchestrator import WorkflowOrchestrator
```
===============================================
"""

import sys
import asyncio
import json
import redis
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
import os
import yaml
import re
import importlib
import shutil
import hashlib

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    from discernus.gateway.model_registry import ModelRegistry
    from discernus.gateway.llm_gateway import LLMGateway
    from discernus.core.conversation_logger import ConversationLogger
    from discernus.core.secure_code_executor import SecureCodeExecutor
    from discernus.core.project_chronolog import get_project_chronolog, log_project_event
    # Import DataExtractionAgent only when needed to avoid circular imports
    DEPENDENCIES_AVAILABLE = True
except ImportError as e:
    print(f"EnsembleOrchestrator dependencies not available: {e}")
    DEPENDENCIES_AVAILABLE = False

class EnsembleOrchestrator:
    """
    THIN ensemble orchestrator with agent registry integration
    """
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.results_path = self.project_path / "results"
        self.results_path.mkdir(exist_ok=True)
        
        # Core components with registry system
        if not DEPENDENCIES_AVAILABLE:
            raise ImportError("EnsembleOrchestrator dependencies not available. Please check your environment.")
            
        try:
            self.model_registry = ModelRegistry()
            self.gateway = LLMGateway(self.model_registry)
            self._load_agent_registry()
            print("✅ EnsembleOrchestrator using Agent Registry, ModelRegistry, and LLMGateway")
        except Exception as e:
            print(f"❌ EnsembleOrchestrator: Failed to initialize components: {e}")
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
        self.session_results_path = None
        self.conversation_id = None
        
    def _load_agent_registry(self):
        """Load agent registry from YAML file"""
        registry_path = project_root / "discernus" / "core" / "agent_registry.yaml"
        if not registry_path.exists():
            raise FileNotFoundError(f"Agent registry not found at: {registry_path}")
        with open(registry_path, 'r') as f:
            registry_data = yaml.safe_load(f)
        self.agent_registry = {agent['name']: agent for agent in registry_data['agents']}
        print("✅ Agent Registry loaded successfully")

    def _create_agent_instance(self, agent_def: Dict[str, Any]) -> Any:
        """Dynamically create an agent instance from registry definition"""
        module_path = agent_def['module']
        class_name = agent_def['class']
        
        # Special case: if it's this orchestrator itself, return self
        if class_name == 'EnsembleOrchestrator':
            return self
            
        module = importlib.import_module(module_path)
        agent_class = getattr(module, class_name)
        return agent_class()
        
    async def _execute_agent(self, agent_name: str, **kwargs) -> Any:
        """Execute an agent using the registry system"""
        agent_def = self.agent_registry.get(agent_name)
        if not agent_def:
            raise ValueError(f"Agent '{agent_name}' not found in registry")
            
        agent_instance = self._create_agent_instance(agent_def)
        execution_method = getattr(agent_instance, agent_def['execution_method'])
        
        if asyncio.iscoroutinefunction(execution_method):
            return await execution_method(**kwargs)
        else:
            return execution_method(**kwargs)
            


    def _init_session_logging(self):
        """Initialize session logging and chronolog"""
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_results_path = self.results_path / f"{self.session_id}"
        self.session_results_path.mkdir(exist_ok=True)

        # Create the Immutable Session Package
        try:
            snapshot_path = self.session_results_path / "project_snapshot"
            snapshot_path.mkdir(exist_ok=True)
            
            # Copy framework and experiment using actual file paths
            if hasattr(self, 'specifications') and self.specifications:
                framework_path = Path(self.specifications['framework']['_metadata']['file_path'])
                experiment_path = Path(self.specifications['experiment']['_metadata']['file_path'])
                
                shutil.copy(framework_path, snapshot_path / framework_path.name)
                shutil.copy(experiment_path, snapshot_path / experiment_path.name)
                
                # Copy corpus
                corpus_path = Path(self.specifications['corpus']['metadata']['corpus_path'])
                corpus_snapshot_path = snapshot_path / "corpus"
                shutil.copytree(corpus_path, corpus_snapshot_path)
            else:
                # Fallback to old behavior if specifications not available
                shutil.copy(self.project_path / "framework.md", snapshot_path)
                shutil.copy(self.project_path / "experiment.md", snapshot_path)
                corpus_snapshot_path = snapshot_path / "corpus"
                shutil.copytree(self.project_path / "corpus", corpus_snapshot_path)
            
            print(f"✅ Created immutable session package at: {snapshot_path}")
            
        except Exception as e:
            print(f"⚠️ Failed to create immutable session package: {e}")
        
        # --- Asset Fingerprinting ---
        asset_fingerprints = {}
        try:
            # Hash framework and experiment using actual file paths
            if hasattr(self, 'specifications') and self.specifications:
                framework_path = Path(self.specifications['framework']['_metadata']['file_path'])
                experiment_path = Path(self.specifications['experiment']['_metadata']['file_path'])
                
                asset_fingerprints[framework_path.name] = self._hash_file(framework_path)
                asset_fingerprints[experiment_path.name] = self._hash_file(experiment_path)
            else:
                # Fallback to old behavior if specifications not available
                framework_path = self.project_path / "framework.md"
                experiment_path = self.project_path / "experiment.md"
                
                asset_fingerprints['framework.md'] = self._hash_file(framework_path)
                asset_fingerprints['experiment.md'] = self._hash_file(experiment_path)
            
            # Hash corpus
            corpus_path = self.project_path / "corpus"
            for corpus_file in corpus_path.rglob('*'):
                if corpus_file.is_file():
                    relative_path = corpus_file.relative_to(self.project_path)
                    asset_fingerprints[str(relative_path)] = self._hash_file(corpus_file)
            
            print("✅ Calculated asset fingerprints (barcodes)")

        except Exception as e:
            print(f"⚠️ Failed to calculate asset fingerprints: {e}")


        # Initialize conversation logger
        self.logger = ConversationLogger(
            project_root=str(self.project_path),
            custom_conversations_dir=str(self.session_results_path)
        )
        self.conversation_id = self.logger.start_conversation(
            speech_text="", # Not relevant for the main log
            research_question="", # Not relevant for the main log
            participants=[] # Dynamically added
        )
        
        # Initialize project chronolog
        log_project_event(str(self.project_path), "SESSION_STARTED", self.session_id, {
            "session_id": self.session_id,
            "session_path": str(self.session_results_path),
            "asset_fingerprints": asset_fingerprints,
        })

    def _hash_file(self, file_path: Path) -> str:
        """Calculates the SHA-256 hash of a file's content."""
        h = hashlib.sha256()
        with open(file_path, 'rb') as f:
            while True:
                data = f.read(65536)  # Read in 64k chunks
                if not data:
                    break
                h.update(data)
        return h.hexdigest()

    def _log_system_event(self, event_type: str, data: Dict[str, Any]):
        """Log system events to chronolog only"""
        # Log to project chronolog (session_id is guaranteed to be string after _init_session_logging)
        if self.session_id:
            log_project_event(str(self.project_path), event_type, self.session_id, data)

    async def _call_llm_async(self, prompt: str, agent_id: str, model_name: str) -> str:
        """Call LLM via gateway with proper logging"""
        self._log_system_event("LLM_CALL_STARTED", {
            "agent_id": agent_id,
            "model_name": model_name,
            "prompt_length": len(prompt)
        })
        
        try:
            response, metadata = self.gateway.execute_call(model_name, prompt)
            
            self._log_system_event("LLM_CALL_COMPLETED", {
                "agent_id": agent_id,
                "model_name": model_name,
                "response_length": len(response),
                "metadata": metadata
            })
            
            return response
            
        except Exception as e:
            self._log_system_event("LLM_CALL_FAILED", {
                "agent_id": agent_id,
                "model_name": model_name,
                "error": str(e)
            })
            raise e

    async def execute_ensemble_analysis(self, specifications: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main execution method - uses Agent Registry with new specification format
        """
        try:
            # Store specifications for use in other methods
            self.specifications = specifications
            
            # Initialize session
            self._init_session_logging()

            # Extract configuration from specifications
            framework = specifications['framework']
            experiment = specifications['experiment']
            corpus = specifications['corpus']
            
            # Get analysis prompt from framework variant
            analysis_variant = experiment.get('analysis_variant', 'default')
            if analysis_variant not in framework['analysis_variants']:
                available_variants = list(framework['analysis_variants'].keys())
                # Use the first available variant if default not found
                analysis_variant = available_variants[0] if available_variants else 'default'
            
            analysis_prompt = framework['analysis_variants'][analysis_variant]['analysis_prompt']
            
            # Extract experiment configuration
            experiment_config = {
                'models': experiment['models'],
                'runs_per_model': experiment.get('runs_per_model', 1),
                'analysis_variant': analysis_variant,
                'framework_name': framework['name'],
                'framework_version': framework['version']
            }
            
            self._log_system_event("ENSEMBLE_STARTED", {
                "corpus_file_count": len(corpus['files']),
                "session_id": self.session_id,
                "experiment_config": experiment_config,
                "framework_name": framework['name'],
                "analysis_variant": analysis_variant
            })
            
            # Step 1: Generate statistical analysis plan using registry (if experiment has statistical_plan)
            if 'statistical_plan' in experiment:
                # Use the experiment file path for the statistical analysis configuration
                experiment_path = experiment['_metadata']['file_path']
                workflow_state = {
                    'experiment_md_path': experiment_path
                }
                step_config = {}
                
                self.statistical_plan = await self._execute_agent(
                    "StatisticalAnalysisConfigurationAgent",
                    workflow_state=workflow_state,
                    step_config=step_config
                )
                
                self._log_system_event("STATISTICAL_PLAN_GENERATED", self.statistical_plan)

                if self.statistical_plan.get("validation_status") != "complete":
                    raise ValueError(f"Statistical plan validation failed: {self.statistical_plan.get('notes', 'No notes provided.')}")
            
            # Step 2: Execute analysis using registry-based AnalysisAgent
            await self._spawn_analysis_agents(specifications, experiment_config, analysis_prompt)
            
            # Step 3: Methodological overwatch using registry
            overwatch_decision = await self._execute_agent(
                "MethodologicalOverwatchAgent",
                workflow_state={"analysis_results": self.analysis_results},
                step_config={}
            )
            
            self._log_system_event("OVERWATCH_AGENT_REVIEW", overwatch_decision)

            if overwatch_decision.get("decision") == "TERMINATE":
                raise SystemExit(f"METHODOLOGICAL OVERWATCH: Execution terminated. Reason: {overwatch_decision.get('reason')}")

            # Step 4: Determine workflow using LLM
            coordination_prompt = f"""
            Analysis complete. Here are the analysis results:
            {json.dumps(self.analysis_results, indent=2)}
            
            And here are the experiment requirements:
            {specifications['experiment'].get('name', 'No experiment name')} - {specifications['experiment'].get('description', 'No experiment description')}
            
            Experiment Configuration:
            {json.dumps(experiment_config, indent=2)}

            Based on all the information above, what should happen next?
            Options:
            - If experiment requires synthesis/moderation/referee: respond "ADVERSARIAL_SYNTHESIS"
            - If experiment requires bias isolation (e.g., remove_synthesis: true): respond "RAW_AGGREGATION" 
            - If you need more information: respond "NEED_MORE_INFO"
            
            Respond with just the action name.
            """
            
            model_name = self.model_registry.get_model_for_task('coordination')
            if not model_name:
                model_name = 'vertex_ai/gemini-1.5-flash-latest'
                
            next_action = await self._call_llm_async(coordination_prompt, "coordination_llm", model_name)
            
            # Step 5: Execute workflow decision
            if "RAW_AGGREGATION" in next_action.upper():
                final_results = await self._simple_aggregation()
            elif "ADVERSARIAL_SYNTHESIS" in next_action.upper():
                final_results = await self._adversarial_workflow()
            else:
                final_results = await self._simple_aggregation()

            # Step 6: Statistical analysis using registry
            stats_results_path = await self._execute_agent(
                "StatisticalAnalysisAgent",
                workflow_state={
                    "analysis_results": self.analysis_results,
                    "session_results_path": str(self.session_results_path)
                },
                step_config={}
            )

            # Step 7: Generate the final comprehensive report
            if not self.session_results_path:
                raise ValueError("Session results path not initialized before report generation.")
            
            final_results = await self._generate_final_report(
                stats_results_path=stats_results_path,
                session_results_path=self.session_results_path
            )

            # Step 9: Tidy Data Extraction
            self._log_system_event("DATA_EXTRACTION_STARTED", {"session_id": self.session_id})
            if self.logger and self.conversation_id and self.session_results_path:
                conversation_log_path = self.session_results_path / f"{self.conversation_id}.jsonl"
                if conversation_log_path.exists():
                    await self._execute_agent(
                        "DataExtractionAgent",
                        conversation_log_path=str(conversation_log_path),
                        output_csv_path=str(self.session_results_path / "results.csv"),
                        framework_content=specifications['framework']['_metadata']['full_content']
                    )
                    self._log_system_event("DATA_EXTRACTION_COMPLETED", {"session_id": self.session_id})
                else:
                    self._log_system_event("DATA_EXTRACTION_SKIPPED", {"reason": "Conversation log not found."})


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

    async def _generate_final_report(self, stats_results_path: str, session_results_path: Path) -> Dict[str, Any]:
        """
        Orchestrates the creation of the final, high-quality analysis report
        by spawning the specialized ReportGeneratorAgent.
        """
        self._log_system_event("FINAL_REPORT_GENERATION_STARTED", {"session_id": self.session_id})

        try:
            # Legacy report generation - simplified for migration away from EnsembleOrchestrator
            # TODO: Remove this when EnsembleOrchestrator is fully deprecated
            
            # These paths now point to the immutable snapshot for true provenance
            snapshot_path = session_results_path / "project_snapshot"
            experiment_spec_path = snapshot_path / self.specifications['experiment']['_metadata']['file_path'].name
            framework_spec_path = snapshot_path / self.specifications['framework']['_metadata']['file_path'].name

            # Simple placeholder report content since report_generator_agent is deprecated
            report_content = f"""# Analysis Report

## Experiment Overview
- Experiment: {experiment_spec_path.name}
- Framework: {framework_spec_path.name}
- Session ID: {self.session_id}

## Results
Statistical results available at: {stats_results_path}

*Note: This is a simplified report generated by the legacy EnsembleOrchestrator. For full reporting capabilities, use the WorkflowOrchestrator.*
"""

            report_path = session_results_path / "comprehensive_analysis_report.md"
            report_path.write_text(report_content)

            self._log_system_event("FINAL_REPORT_GENERATION_COMPLETED", {"report_path": str(report_path)})

            return {
                "report_path": str(report_path),
                "session_id": self.session_id,
                "status": "success"
            }
        except Exception as e:
            self._log_system_event("FINAL_REPORT_GENERATION_FAILED", {"error": str(e)})
            # Fallback to simple report on error
            return await self._simple_aggregation()


    async def _spawn_analysis_agents(self, specifications: Dict[str, Any], experiment_config: Dict[str, Any], analysis_prompt: str):
        """Spawn analysis agents using registry system with new specification format"""
        
        # Get corpus files from specifications
        corpus_files = []
        for filename, file_data in specifications['corpus']['files'].items():
            corpus_files.append(file_data['path'])
        
        analysis_instructions = analysis_prompt
        models = experiment_config.get('models', ['vertex_ai/gemini-2.5-flash'])
        num_runs = experiment_config.get('runs_per_model', 1)
        
        self._log_system_event("ANALYSIS_AGENTS_SPAWNING", {
            "agent_count": len(corpus_files) * len(models) * num_runs,
            "models": models,
            "num_runs": num_runs,
            "instructions_preview": analysis_instructions[:200] + "..." if len(analysis_instructions) > 200 else analysis_instructions
        })
        
        # Create analysis tasks
        analysis_tasks = []
        for run in range(num_runs):
            for model_name in models:
                for i, corpus_file in enumerate(corpus_files):
                    # corpus_file already contains the full absolute path
                    corpus_file_path = corpus_file
                    
                    agent_id = f"analysis_agent_run{run+1}_{model_name.replace('/', '_')}_{i+1}"
                    task = self._run_analysis_agent(
                        agent_id=agent_id,
                        corpus_file=corpus_file_path,
                        instructions=analysis_instructions,
                        model_name=model_name,
                        run_num=run + 1
                    )
                    analysis_tasks.append(task)
        
        # Execute tasks in parallel
        print(f"🔧 Executing {len(analysis_tasks)} analysis tasks in parallel")
        raw_results = await asyncio.gather(*analysis_tasks, return_exceptions=True)
        
        # Filter exceptions
        successful_results: List[Dict[str, Any]] = []
        failed_count = 0
        
        for i, result in enumerate(raw_results):
            if isinstance(result, Exception):
                failed_count += 1
                self._log_system_event("ANALYSIS_AGENT_ERROR", {
                    "agent_id": f"analysis_agent_{i+1}",
                    "error": str(result)
                })
            elif isinstance(result, dict):
                successful_results.append(result)

        self.analysis_results = successful_results
        
        print(f"INFO: Analysis complete. {len(successful_results)} successful, {failed_count} failed.")
        
        if failed_count > 0 and len(successful_results) > 0:
            results_prompt = f"""
            Analysis results processing. There are {failed_count} failed analyses and {len(successful_results)} successful analyses.
            
            Options:
            - "FILTER": Continue with the {len(successful_results)} successful results
            - "ABORT": Stop processing due to the failures
            
            What should we do? Respond with just the action name.
            """
            
            model_name = self.model_registry.get_model_for_task('coordination')
            if not model_name:
                model_name = 'vertex_ai/gemini-1.5-flash-latest'
                
            processing_decision = await self._call_llm_async(results_prompt, "results_processing_agent", model_name)
            
            if "ABORT" in processing_decision.upper():
                raise ValueError(f"Results processing aborted due to {failed_count} failures")

    async def _run_analysis_agent(self, agent_id: str, corpus_file: str, instructions: str, model_name: str, run_num: int) -> Dict[str, Any]:
        """Run a single analysis agent on one corpus text using the framework's direct prompt."""
        
        self._log_system_event("ANALYSIS_AGENT_SPAWNED", {
            "agent_id": agent_id,
            "corpus_file": Path(corpus_file).name,
            "model_name": model_name,
            "run_num": run_num
        })
        
        corpus_text = Path(corpus_file).read_text()
        
        # Use the framework's analysis prompt directly with the corpus text
        analysis_prompt = f"""{instructions}

TEXT TO ANALYZE:
---
{corpus_text}
---

Apply the framework systematically to this text and return the JSON object as specified above."""

        # Use the specified model from the experiment configuration
        raw_response = await self._call_llm_async(analysis_prompt, agent_id, model_name)
        
        # Parse the response - handle markdown fences and extract JSON
        try:
            # Find and extract JSON block from the response
            clean_response = raw_response.strip()
            
            # Look for JSON block markers
            json_start = -1
            json_end = -1
            
            # Try to find ```json markers
            if '```json' in clean_response:
                json_start = clean_response.find('```json') + 7
                json_end = clean_response.find('```', json_start)
            # Try to find ``` markers 
            elif '```' in clean_response:
                json_start = clean_response.find('```') + 3
                json_end = clean_response.find('```', json_start)
            # Try to find JSON by looking for opening brace
            elif '{' in clean_response:
                json_start = clean_response.find('{')
                json_end = clean_response.rfind('}') + 1
            
            if json_start != -1 and json_end != -1:
                clean_response = clean_response[json_start:json_end].strip()
            
            parsed_response = json.loads(clean_response)
            
            # Extract the analysis text - could be in different fields depending on framework
            analysis_text = parsed_response.get("analysis_text", "")
            if not analysis_text:
                # Try other common fields
                analysis_text = parsed_response.get("reasoning", "")
                if not analysis_text:
                    analysis_text = str(parsed_response)  # Use the whole response as fallback
            
            # Create a comprehensive analysis response that includes all the rich data
            comprehensive_analysis = f"Raw LLM Response:\n{raw_response}\n\nParsed JSON:\n{json.dumps(parsed_response, indent=2)}"
            
        except json.JSONDecodeError as e:
            self._log_system_event("JSON_DECODE_ERROR", {"agent_id": agent_id, "raw_response": raw_response, "error": str(e)})
            analysis_text = f"LLM RESPONSE WAS NOT VALID JSON. Raw response: {raw_response}"
            comprehensive_analysis = analysis_text
            parsed_response = {}

        # Log the analysis
        if self.logger and self.conversation_id:
            self.logger.log_llm_message(
                conversation_id=self.conversation_id,
                speaker=agent_id,
                message=comprehensive_analysis,
                metadata={"type": "llm_analysis_text", "parsed_json": parsed_response}
            )

        return {
            "agent_id": agent_id,
            "corpus_file": corpus_file,
            "analysis_response": comprehensive_analysis,
            "parsed_json": parsed_response,
            "file_name": Path(corpus_file).name,
            "model_name": model_name,
            "run_num": run_num
        }

    async def _simple_aggregation(self) -> Dict[str, Any]:
        """Simple aggregation of results - FALLBACK ONLY"""
        
        # Create simple report
        report_content = f"""# Analysis Results Report

## Session Information
- Session ID: {self.session_id}
- Results Path: {self.session_results_path}
- Analysis Count: {len(self.analysis_results)}

## Analysis Results
"""
        
        for result in self.analysis_results:
            report_content += f"""
### {result['agent_id']}
- File: {result['file_name']}
- Model: {result['model_name']}
- Run: {result['run_num']}

Response:
{result['analysis_response']}

---
"""
        
        # Save report
        if self.session_results_path is None:
            raise ValueError("Session results path not initialized")
        report_path = self.session_results_path / "analysis_report.md"
        report_path.write_text(report_content)
        
        return {
            "report_path": str(report_path),
            "session_id": self.session_id,
            "analysis_count": len(self.analysis_results)
        }

    async def _adversarial_workflow(self) -> Dict[str, Any]:
        """Adversarial synthesis workflow"""
        # This needs a more complex implementation, for now, we'll just aggregate
        return await self._simple_aggregation() 