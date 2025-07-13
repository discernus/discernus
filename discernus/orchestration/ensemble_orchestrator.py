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

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    from discernus.core.thin_litellm_client import ThinLiteLLMClient
    from discernus.gateway.litellm_client import LiteLLMClient  # Add our improved client
    from discernus.core.conversation_logger import ConversationLogger
    DEPENDENCIES_AVAILABLE = True
except ImportError as e:
    print(f"EnsembleOrchestrator dependencies not available: {e}")
    DEPENDENCIES_AVAILABLE = False

class LiteLLMClientAdapter:
    """Adapter to make LiteLLMClient compatible with EnsembleOrchestrator's expected interface"""
    
    def __init__(self):
        self.client = LiteLLMClient()
    
    def call_llm(self, prompt: str, role: str) -> str:
        """Adapt LiteLLMClient.analyze_text to the call_llm interface"""
        # Create a minimal experiment definition for the analyze_text method
        experiment_def = {
            "framework": {"name": "ensemble_framework"},
            "research_question": f"Ensemble analysis task: {role}"
        }
        
        # Use a fast, cost-effective model for analysis tasks
        model_name = "vertex_ai/gemini-2.5-flash"  # Fast and cheap
        
        try:
            # Call our improved client with parameter manager
            result, cost = self.client.analyze_text(prompt, experiment_def, model_name)
            
            # Extract the text response
            if isinstance(result, dict) and 'raw_response' in result:
                return result['raw_response']
            elif isinstance(result, str):
                return result
            else:
                print(f"⚠️ Unexpected result type from LiteLLMClient: {type(result)}")
                return str(result) if result else ""
                
        except Exception as e:
            print(f"⚠️ LiteLLMClientAdapter error: {e}")
            # Fallback to empty string rather than None to avoid issues
            return ""

class EnsembleOrchestrator:
    """
    THIN ensemble orchestrator - simple linear pipeline execution
    """
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.results_path = self.project_path / "results"
        self.results_path.mkdir(exist_ok=True)
        
        # Core components with improved LLM client
        if DEPENDENCIES_AVAILABLE:
            try:
                # Use our improved LiteLLMClient with parameter manager
                self.llm_client = LiteLLMClientAdapter()
                print("✅ EnsembleOrchestrator using improved LiteLLMClient with parameter manager")
            except:
                try:
                    # Fallback to original client if needed
                    self.llm_client = ThinLiteLLMClient()
                    print("⚠️ EnsembleOrchestrator falling back to ThinLiteLLMClient")
                except:
                    self.llm_client = None
                    print("❌ EnsembleOrchestrator: No LLM client available")
        else:
            self.llm_client = None
            
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
        self.logger = None  # Will be initialized per session
        
        # Session state
        self.session_id = None
        self.analysis_results = []
        self.synthesis_result = None
        self.outliers = []
        
    async def execute_ensemble_analysis(self, validation_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        THIN Principle: LLM decides research workflow based on experiment requirements
        """
        try:
            # Initialize session
            self._init_session_logging()
            
            self._log_system_event("ENSEMBLE_STARTED", {
                "corpus_file_count": len(validation_results.get('corpus_files', [])),
                "session_id": self.session_id
            })
            
            # Step 1: Spawn analysis agents (one per corpus text)
            await self._spawn_analysis_agents(validation_results)
            
            # Step 2: Ask LLM what to do next based on experiment requirements
            coordination_prompt = f"""
            Analysis complete. Here are the analysis results:
            {json.dumps(self.analysis_results, indent=2)}
            
            And here are the experiment requirements:
            {validation_results.get('experiment', {}).get('definition', 'No experiment definition provided')}
            
            Based on the experiment requirements, what should happen next?
            Options:
            - If experiment requires synthesis/moderation/referee: respond "ADVERSARIAL_SYNTHESIS"
            - If experiment requires bias isolation (like Attesor study): respond "RAW_AGGREGATION" 
            - If you need more information: respond "NEED_MORE_INFO"
            
            Respond with just the action name.
            """
            
            next_action = await self._call_llm_async(coordination_prompt, "coordination_llm")
            
            # Step 3: Execute whatever the LLM decided (THIN: dumb execution)
            if "RAW_AGGREGATION" in next_action.upper():
                final_results = await self._simple_aggregation()
            elif "ADVERSARIAL_SYNTHESIS" in next_action.upper():
                final_results = await self._adversarial_workflow()
            else:
                # Default to simple aggregation if unclear
                final_results = await self._simple_aggregation()
            
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
    
    async def _spawn_analysis_agents(self, validation_results: Dict[str, Any]):
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
        
        validation_decision = await self._call_llm_async(validation_prompt, "input_validation_agent")
        
        if "INSUFFICIENT_INPUTS" in validation_decision.upper():
            raise ValueError(f"LLM input validation failed: {validation_decision}")
        
        corpus_files = validation_results.get('corpus_files', [])
        analysis_instructions = validation_results.get('analysis_agent_instructions', '')
        
        self._log_system_event("ANALYSIS_AGENTS_SPAWNING", {
            "agent_count": len(corpus_files),
            "instructions_preview": analysis_instructions[:200] + "..." if len(analysis_instructions) > 200 else analysis_instructions
        })
        
        # Process each corpus file with its own analysis agent
        analysis_tasks = []
        for i, corpus_file in enumerate(corpus_files):
            agent_id = f"analysis_agent_{i+1}"
            task = self._run_analysis_agent(agent_id, corpus_file, analysis_instructions)
            analysis_tasks.append(task)
        
        # THIN: Let LLM decide execution strategy
        execution_prompt = f"""
        You are the execution strategy agent. Decide how to run {len(analysis_tasks)} analysis tasks:
        
        Options:
        - "SEQUENTIAL": Run one at a time (safer, slower)
        - "PARALLEL": Run all at once (faster, more resource intensive)
        
        Consider system load and task complexity. Respond with just the strategy name.
        """
        
        execution_strategy = await self._call_llm_async(execution_prompt, "execution_strategy_agent")
        
        if "SEQUENTIAL" in execution_strategy.upper():
            print("🔧 LLM chose SEQUENTIAL execution")
            self.analysis_results = []
            for i, task in enumerate(analysis_tasks):
                result = await task
                self.analysis_results.append(result)
        else:
            print("🔧 LLM chose PARALLEL execution")
            import asyncio
            self.analysis_results = await asyncio.gather(*analysis_tasks, return_exceptions=True)
        
        # THIN: Let LLM decide how to handle results
        result_types = []
        for r in self.analysis_results:
            if isinstance(r, Exception):
                result_types.append(f"Exception: {type(r).__name__}")
            else:
                result_types.append("Success")
        
        results_prompt = f"""
        You are the results processing agent. Process these analysis results:
        
        Results: {result_types}
        
        Should failed results be:
        - "RETRY": Attempt to retry failed analyses
        - "FILTER": Remove failed results and continue
        - "ABORT": Stop processing due to failures
        
        Respond with just the action name.
        """
        
        results_decision = await self._call_llm_async(results_prompt, "results_processing_agent")
        
        if "ABORT" in results_decision.upper():
            failed_count = sum(1 for r in self.analysis_results if isinstance(r, Exception))
            raise RuntimeError(f"LLM decided to abort due to {failed_count} failed analyses")
        
        # Filter successful results (for now, RETRY logic can be added later)
        successful_results = []
        for i, result in enumerate(self.analysis_results):
            if isinstance(result, Exception):
                self._log_system_event("ANALYSIS_AGENT_ERROR", {
                    "agent_id": f"analysis_agent_{i+1}",
                    "error": str(result)
                })
            else:
                successful_results.append(result)
        
        self.analysis_results = successful_results
        
        self._log_system_event("ANALYSIS_AGENTS_COMPLETED", {
            "successful_count": len(successful_results),
            "failed_count": len(corpus_files) - len(successful_results)
        })
    
    async def _run_analysis_agent(self, agent_id: str, corpus_file: str, instructions: str) -> Dict[str, Any]:
        """Run a single analysis agent on one corpus text"""
        
        self._log_system_event("AGENT_SPAWNED", {
            "agent_id": agent_id,
            "agent_type": "analysis_agent",
            "corpus_file": Path(corpus_file).name
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

        # Call LLM
        response = await self._call_llm_async(analysis_prompt, agent_id)
        
        self._log_system_event("AGENT_COMPLETED", {
            "agent_id": agent_id,
            "agent_type": "analysis_agent",
            "response_length": len(response) if response else 0
        })
        
        return {
            "agent_id": agent_id,
            "corpus_file": corpus_file,
            "analysis_response": response,
            "file_name": Path(corpus_file).name
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
        
        formatted_results = await self._call_llm_async(formatting_prompt, "results_formatting_agent")
        
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

        self.synthesis_result = await self._call_llm_async(synthesis_prompt, "synthesis_agent")
        
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
        
        outlier_decision = await self._call_llm_async(outlier_assessment_prompt, "outlier_assessment_agent")
        
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

        moderator_response = await self._call_llm_async(moderator_prompt, "moderator_agent")
        
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

        referee_decision = await self._call_llm_async(referee_prompt, "referee_agent")
        
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

        final_report = await self._call_llm_async(final_prompt, "final_synthesis_agent")
        
        # Save results to project
        await self._save_results_to_project(final_report)
        
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
            "session_id": self.session_id
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
        
        final_report = await self._call_llm_async(final_report_prompt, "aggregation_agent")
        await self._save_results_to_project(final_report)
        
        return {
            "type": "simple_aggregation",
            "report": final_report,
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
            
            needs_outlier_discussion = await self._call_llm_async(outlier_prompt, "outlier_coordinator")
            
            if "YES" in needs_outlier_discussion.upper():
                await self._handle_outliers()
        
        # Final synthesis
        final_results = await self._final_synthesis()
        
        return final_results
    
    async def _save_results_to_project(self, final_report: str):
        """Save results back to the project directory"""
        
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        results_dir = self.results_path / f"{timestamp}"
        results_dir.mkdir(exist_ok=True)
        
        # Save final report
        (results_dir / "final_report.md").write_text(final_report)
        
        # Save session metadata
        metadata = {
            "session_id": self.session_id,
            "timestamp": timestamp,
            "analysis_count": len(self.analysis_results),
            "outliers_handled": len(self.outliers),
            "project_path": str(self.project_path)
        }
        (results_dir / "session_metadata.json").write_text(json.dumps(metadata, indent=2))
        
        self._log_system_event("RESULTS_SAVED", {
            "results_directory": str(results_dir),
            "files_saved": ["final_report.md", "session_metadata.json"]
        })
    
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
            # For now, capture the known default model from code inspection
            # This can be enhanced later to dynamically extract from LLM client
            default_model = "vertex_ai/gemini-2.5-flash"  # Current default from code inspection
            
            return {
                "primary_model": default_model,
                "model_family": "gemini",
                "model_version": "2.5-flash",
                "provider": "vertex_ai",
                "capture_method": "code_inspection",
                "capture_timestamp": datetime.now().isoformat(),
                "notes": "Model captured from EnsembleOrchestrator default configuration - based on LiteLLMClientAdapter line 54"
            }
        except Exception as e:
            return {
                "primary_model": "error",
                "model_family": "error",
                "model_version": "error", 
                "provider": "error",
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
    
    async def _call_llm_async(self, prompt: str, agent_id: str) -> str:
        """Call LLM asynchronously with proper logging"""
        
        if not self.llm_client:
            print(f"🔴 DEBUG: No LLM client available for {agent_id}")
            return f"[MOCK RESPONSE] {agent_id} would analyze: {prompt[:100]}..."
        
        try:
            # Debug logging
            print(f"🟡 DEBUG: Starting LLM call for {agent_id}")
            print(f"🟡 DEBUG: Prompt length: {len(prompt)}")
            print(f"🟡 DEBUG: LLM client type: {type(self.llm_client)}")
            
            # Log the call
            if self.logger:
                self.logger.log_llm_message(
                    conversation_id=self.conversation_id or self.session_id or "unknown",
                    speaker=agent_id,
                    message=prompt,
                    metadata={
                        "type": "llm_request",
                        "agent_id": agent_id,
                        "session_id": self.session_id
                    }
                )
            
            # Make the LLM call (wrap sync call for async context)
            import asyncio
            if self.llm_client and hasattr(self.llm_client, 'call_llm'):
                print(f"🟡 DEBUG: Calling LLM via async executor for {agent_id}")
                response = await asyncio.get_event_loop().run_in_executor(
                    None, 
                    lambda: self.llm_client.call_llm(prompt, agent_id)
                )
                print(f"🟢 DEBUG: Got response for {agent_id}, length: {len(response) if response else 'None'}")
                print(f"🟢 DEBUG: Response preview: {str(response)[:200] if response else 'None'}")
            else:
                print(f"🔴 DEBUG: LLM client missing call_llm method for {agent_id}")
                response = f"[ERROR] LLM client missing call_llm method"
            
            # Handle None response
            if response is None:
                print(f"🔴 DEBUG: Got None response for {agent_id}")
                response = f"[EMPTY RESPONSE] {agent_id} returned None"
            
            # Log the response
            if self.logger:
                self.logger.log_llm_message(
                    conversation_id=self.conversation_id or self.session_id or "unknown",
                    speaker=agent_id,
                    message=response,
                    metadata={
                        "type": "llm_response",
                        "agent_id": agent_id,
                        "session_id": self.session_id
                    }
                )
            
            return response
            
        except Exception as e:
            error_msg = f"LLM call failed for {agent_id}: {str(e)}"
            print(f"🔴 DEBUG: Exception in LLM call for {agent_id}: {str(e)}")
            
            if self.logger:
                self.logger.log_llm_message(
                    conversation_id=self.conversation_id or self.session_id or "unknown",
                    speaker="system",
                    message=error_msg,
                    metadata={
                        "type": "llm_error",
                        "agent_id": agent_id,
                        "session_id": self.session_id
                    }
                )
            
            return f"[ERROR] {error_msg}" 