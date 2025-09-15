#!/usr/bin/env python3
"""
Statistical Agent - THIN v2.0 Architecture
==========================================

Performs comprehensive statistical analysis using LLM internal execution 
with minimal tool calling for verification and CSV generation.

Architecture:
- Step 1: Statistical Execution (Pro) - Generate + execute statistical functions
- Step 2: Verification (Lite + tool calling) - Adversarial verification 
- Step 3: CSV Generation (Lite + tool calling) - Transform to researcher format
"""

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional
import yaml

from ...core.security_boundary import ExperimentSecurityBoundary
from ...core.local_artifact_storage import LocalArtifactStorage
from ...core.audit_logger import AuditLogger
from ...gateway.llm_gateway_enhanced import EnhancedLLMGateway
from ...gateway.model_registry import get_model_registry


class StatisticalAgent:
    """
    THIN Statistical Agent for comprehensive statistical analysis.
    
    Uses LLM internal execution for statistical planning, analysis, and code generation,
    with minimal tool calling for verification and CSV output.
    """

    def __init__(self, 
                 security: ExperimentSecurityBoundary,
                 storage: LocalArtifactStorage,
                 audit: AuditLogger,
                 experiment_metadata: Optional[Dict[str, Any]] = None):
        """
        Initialize the Statistical Agent.
        
        Args:
            security: Security boundary for file operations
            storage: Content-addressable artifact storage
            audit: Audit logger for comprehensive event tracking
            experiment_metadata: Optional experiment configuration
        """
        self.agent_name = "StatisticalAgent"
        self.security = security
        self.storage = storage
        self.audit = audit
        self.experiment_metadata = experiment_metadata or {}
        
        # Initialize LLM gateway
        self.gateway = EnhancedLLMGateway(get_model_registry())
        
        # Load prompt template
        self.prompt_template = self._load_prompt_template()
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
        
    def _load_prompt_template(self) -> str:
        """Load the statistical analysis prompt template."""
        prompt_path = Path(__file__).parent / "prompt.yaml"
        try:
            with open(prompt_path, 'r') as f:
                yaml_content = yaml.safe_load(f)
                return yaml_content.get('template', '')
        except FileNotFoundError:
            self.logger.error(f"Prompt template not found: {prompt_path}")
            return ""
        except Exception as e:
            self.logger.error(f"Error loading prompt template: {e}")
            return ""

    def analyze_batch(self,
                     framework_content: str,
                     experiment_content: str,
                     corpus_manifest: str,
                     batch_id: str) -> Dict[str, Any]:
        """
        Perform comprehensive statistical analysis on a batch of analysis artifacts.
        
        Args:
            framework_content: Full framework markdown content
            experiment_content: Full experiment.md content  
            corpus_manifest: Corpus manifest content
            batch_id: Unique identifier for this batch
            
        Returns:
            Dictionary containing statistical results, verification status, and CSV paths
        """
        
        self.audit.log_agent_event(self.agent_name, "batch_analysis_started", {
            "batch_id": batch_id,
            "framework_length": len(framework_content),
            "experiment_length": len(experiment_content)
        })
        
        # Check cache first
        cached_result = self.check_cache(batch_id)
        if cached_result:
            return cached_result
        
        try:
            # Step 1: Statistical Execution (Pro)
            statistical_result = self._step1_statistical_execution(
                framework_content, experiment_content, corpus_manifest, batch_id
            )
            
            # Step 2: Verification (Lite + tool calling)
            verification_result = self._step2_verification(
                statistical_result, batch_id
            )
            
            # Step 3: CSV Generation (Lite + tool calling)
            csv_result = self._step3_csv_generation(
                batch_id
            )
            
            # Calculate total costs and performance metrics
            total_cost_info = self._calculate_total_costs(statistical_result, verification_result, csv_result)
            
            # Combine results
            final_result = {
                "batch_id": batch_id,
                "statistical_analysis": statistical_result,
                "verification": verification_result,
                "csv_generation": csv_result,
                "total_cost_info": total_cost_info,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "agent_name": self.agent_name
            }
            
            self.audit.log_agent_event(self.agent_name, "batch_analysis_completed", {
                "batch_id": batch_id,
                "verification_status": verification_result.get("verification_status", "unknown"),
                "csv_files_created": len(csv_result.get("csv_files", [])),
                "total_cost_info": total_cost_info
            })
            
            # Store result in cache for future use
            self.store_cache(batch_id, final_result)
            
            return final_result
            
        except Exception as e:
            error_msg = f"Statistical analysis failed for batch {batch_id}: {str(e)}"
            self.logger.error(error_msg)
            self.audit.log_agent_event(self.agent_name, "batch_analysis_failed", {
                "batch_id": batch_id,
                "error": str(e)
            })
            raise

    def _step1_statistical_execution(self,
                                   framework_content: str,
                                   experiment_content: str,
                                   corpus_manifest: str,
                                   batch_id: str) -> Dict[str, Any]:
        """
        Step 1: Generate and execute statistical analysis functions using Gemini 2.5 Pro.
        
        Based on the existing AutomatedStatisticalAnalysisAgent approach but with
        LLM internal execution of the generated functions.
        """
        
        # Discover and load analysis artifacts from shared cache
        analysis_artifacts = self._discover_analysis_artifacts(batch_id)
        
        if not analysis_artifacts:
            raise ValueError(f"No analysis artifacts found for batch {batch_id}")
        
        # Prepare prompt using existing statistical analysis template
        prompt = self._prepare_statistical_prompt(
            framework_content, experiment_content, corpus_manifest, analysis_artifacts
        )
        
        self.audit.log_agent_event(self.agent_name, "step1_started", {
            "batch_id": batch_id,
            "step": "statistical_execution",
            "model": "vertex_ai/gemini-2.5-pro",
            "artifacts_count": len(analysis_artifacts)
        })
        
        # Execute with Pro model for complex statistical analysis
        start_time = datetime.now(timezone.utc)
        response = self.gateway.execute_call(
            model="vertex_ai/gemini-2.5-pro",
            prompt=prompt
        )
        end_time = datetime.now(timezone.utc)
        execution_time = (end_time - start_time).total_seconds()
        
        if isinstance(response, tuple):
            content, metadata = response
        else:
            content = response.get('content', '')
            metadata = response.get('metadata', {})
        
        # Extract cost information from metadata
        cost_info = {
            "model": "vertex_ai/gemini-2.5-pro",
            "execution_time_seconds": execution_time,
            "response_cost": metadata.get('response_cost', 0.0),
            "input_tokens": metadata.get('input_tokens', 0),
            "output_tokens": metadata.get('output_tokens', 0),
            "total_tokens": metadata.get('total_tokens', 0),
            "prompt_length": len(prompt),
            "response_length": len(content)
        }
        
        # Save statistical execution result with cost tracking
        statistical_result = {
            "batch_id": batch_id,
            "step": "statistical_execution",
            "model_used": "vertex_ai/gemini-2.5-pro",
            "statistical_functions_and_results": content,
            "analysis_artifacts_processed": len(analysis_artifacts),
            "cost_info": cost_info,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        statistical_hash = self.storage.put_artifact(
            json.dumps(statistical_result, indent=2).encode('utf-8'),
            {"artifact_type": "statistical_analysis", "batch_id": batch_id}
        )
        
        statistical_result['artifact_hash'] = statistical_hash
        
        self.audit.log_agent_event(self.agent_name, "step1_completed", {
            "batch_id": batch_id,
            "step": "statistical_execution",
            "artifact_hash": statistical_hash,
            "response_length": len(content),
            "cost_info": cost_info
        })
        
        return statistical_result

    def _step2_verification(self, 
                          statistical_result: Dict[str, Any], 
                          batch_id: str) -> Dict[str, Any]:
        """
        Step 2: Verify statistical analysis by re-executing functions using Flash Lite.
        
        Similar to the analysis agent's verification step - adversarial checking
        by re-running the generated functions and comparing results.
        """
        
        # Define verification tool
        verification_tools = [
            {
                "name": "verify_statistical_analysis",
                "description": "Verify that the statistical analysis functions and results are correct",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "verified": {
                            "type": "boolean",
                            "description": "Whether the statistical analysis is mathematically correct"
                        }
                    },
                    "required": ["verified"]
                }
            }
        ]
        
        prompt = f"""Re-execute and verify the statistical analysis functions and results:

STATISTICAL FUNCTIONS AND RESULTS:
{statistical_result['statistical_functions_and_results']}

Your task:
1. Extract the Python functions from the statistical analysis
2. Re-execute them with the same data
3. Compare your results with the reported results
4. Call the verify_statistical_analysis tool with your verification result

If the functions execute correctly and produce the same results, call with verified=true.
If there are errors or discrepancies, call with verified=false."""

        self.audit.log_agent_event(self.agent_name, "step2_started", {
            "batch_id": batch_id,
            "step": "verification",
            "model": "vertex_ai/gemini-2.5-flash-lite"
        })

        start_time = datetime.now(timezone.utc)
        response_content, response_metadata = self.gateway.execute_call_with_tools(
            model="vertex_ai/gemini-2.5-flash-lite",
            prompt=prompt,
            tools=verification_tools
        )
        end_time = datetime.now(timezone.utc)
        execution_time = (end_time - start_time).total_seconds()
        
        # Extract cost information from response metadata
        verification_cost_info = {
            "model": "vertex_ai/gemini-2.5-flash-lite",
            "execution_time_seconds": execution_time,
            "prompt_length": len(prompt),
            "response_cost": response_metadata.get('response_cost', 0.0),
            "input_tokens": response_metadata.get('input_tokens', 0),
            "output_tokens": response_metadata.get('output_tokens', 0),
            "total_tokens": response_metadata.get('total_tokens', 0)
        }
        
        # Extract verification result from metadata (tool calls are in metadata)
        verification_status = "unknown"
        tool_calls = response_metadata.get('tool_calls', [])
        if tool_calls:
            for tool_call in tool_calls:
                if hasattr(tool_call, 'function') and tool_call.function.name == "verify_statistical_analysis":
                    try:
                        args = json.loads(tool_call.function.arguments)
                        verification_status = "verified" if args.get("verified", False) else "verification_error"
                    except (json.JSONDecodeError, Exception):
                        verification_status = "verification_error"
        
        verification_result = {
            "batch_id": batch_id,
            "step": "verification",
            "model_used": "vertex_ai/gemini-2.5-flash-lite",
            "verification_status": verification_status,
            "cost_info": verification_cost_info,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        verification_hash = self.storage.put_artifact(
            json.dumps(verification_result, indent=2).encode('utf-8'),
            {"artifact_type": "statistical_verification", "batch_id": batch_id}
        )
        
        verification_result['artifact_hash'] = verification_hash
        
        self.audit.log_agent_event(self.agent_name, "step2_completed", {
            "batch_id": batch_id,
            "step": "verification",
            "verification_status": verification_status,
            "artifact_hash": verification_hash,
            "cost_info": verification_cost_info
        })
        
        return verification_result

    def _step3_csv_generation(self, batch_id: str) -> Dict[str, Any]:
        """
        Step 3: Generate CSV files for researchers using Flash Lite.
        
        Loads raw score and derived metrics artifacts and transforms them into
        R/STATA/pandas-compatible CSV format.
        """
        
        # Define CSV generation tool
        csv_tools = [
            {
                "name": "generate_csv_file",
                "description": "Generate a CSV file with the specified content",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "filename": {
                            "type": "string",
                            "description": "Name of the CSV file (e.g., 'scores.csv')"
                        },
                        "csv_content": {
                            "type": "string",
                            "description": "Complete CSV content with headers and data"
                        }
                    },
                    "required": ["filename", "csv_content"]
                }
            }
        ]
        
        # Discover analysis artifacts for CSV generation
        analysis_artifacts = self._discover_analysis_artifacts(batch_id)
        
        # Prepare artifact content for CSV generation
        artifacts_content = ""
        for artifact_hash, artifact_data in analysis_artifacts.items():
            artifacts_content += f"\n--- ARTIFACT {artifact_hash} ---\n"
            artifacts_content += json.dumps(artifact_data, indent=2)
        
        prompt = f"""Transform the analysis artifacts into CSV files for researchers:

ANALYSIS ARTIFACTS:
{artifacts_content}

Your task:
1. Extract scores, evidence, and metadata from all analysis artifacts
2. Generate standard CSV files that work with R, STATA, and pandas
3. Create separate CSV files for different data types:
   - scores.csv: Dimensional scores with raw_score, salience, confidence
   - evidence.csv: Evidence quotes with dimensions and metadata
   - metadata.csv: Document metadata and analysis information

Use the generate_csv_file tool for each CSV file. Ensure proper CSV formatting with:
- Headers in the first row
- Comma-separated values
- Quoted strings if they contain commas
- Standard format compatible with statistical software"""

        self.audit.log_agent_event(self.agent_name, "step3_started", {
            "batch_id": batch_id,
            "step": "csv_generation",
            "model": "vertex_ai/gemini-2.5-flash-lite",
            "artifacts_count": len(analysis_artifacts)
        })

        start_time = datetime.now(timezone.utc)
        response_content, response_metadata = self.gateway.execute_call_with_tools(
            model="vertex_ai/gemini-2.5-flash-lite",
            prompt=prompt,
            tools=csv_tools
        )
        end_time = datetime.now(timezone.utc)
        execution_time = (end_time - start_time).total_seconds()
        
        # Extract cost information from response metadata
        csv_cost_info = {
            "model": "vertex_ai/gemini-2.5-flash-lite",
            "execution_time_seconds": execution_time,
            "prompt_length": len(prompt),
            "artifacts_processed": len(analysis_artifacts),
            "response_cost": response_metadata.get('response_cost', 0.0),
            "input_tokens": response_metadata.get('input_tokens', 0),
            "output_tokens": response_metadata.get('output_tokens', 0),
            "total_tokens": response_metadata.get('total_tokens', 0)
        }
        
        # Extract CSV generation results from metadata
        csv_files = []
        tool_calls = response_metadata.get('tool_calls', [])
        if tool_calls:
            for tool_call in tool_calls:
                if hasattr(tool_call, 'function') and tool_call.function.name == "generate_csv_file":
                    try:
                        args = json.loads(tool_call.function.arguments)
                        filename = args.get("filename", "unknown.csv")
                        csv_content = args.get("csv_content", "")
                        
                        # Write CSV file to experiment data directory
                        csv_path = self._write_csv_file(filename, csv_content, batch_id)
                        csv_files.append({
                            "filename": filename,
                            "path": str(csv_path),
                            "size": len(csv_content)
                        })
                    except (json.JSONDecodeError, Exception) as e:
                        self.logger.error(f"Error processing CSV generation: {e}")
        
        csv_result = {
            "batch_id": batch_id,
            "step": "csv_generation",
            "model_used": "vertex_ai/gemini-2.5-flash-lite",
            "csv_files": csv_files,
            "cost_info": csv_cost_info,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        csv_hash = self.storage.put_artifact(
            json.dumps(csv_result, indent=2).encode('utf-8'),
            {"artifact_type": "csv_generation", "batch_id": batch_id}
        )
        
        csv_result['artifact_hash'] = csv_hash
        
        self.audit.log_agent_event(self.agent_name, "step3_completed", {
            "batch_id": batch_id,
            "step": "csv_generation",
            "csv_files_created": len(csv_files),
            "artifact_hash": csv_hash,
            "cost_info": csv_cost_info
        })
        
        return csv_result

    def _discover_analysis_artifacts(self, batch_id: str) -> Dict[str, Any]:
        """
        Discover analysis artifacts from shared cache for the given batch.
        
        Looks for score_extraction and derived_metrics artifacts that match
        the batch or experiment.
        """
        artifacts = {}
        
        # Search through artifact registry for analysis artifacts
        for artifact_hash, artifact_info in self.storage.registry.items():
            metadata = artifact_info.get("metadata", {})
            artifact_type = metadata.get("artifact_type", "")
            
            # Look for score and derived metrics artifacts
            if artifact_type in ["score_extraction", "derived_metrics"]:
                try:
                    artifact_content = self.storage.get_artifact(artifact_hash)
                    artifact_data = json.loads(artifact_content.decode('utf-8'))
                    artifacts[artifact_hash] = artifact_data
                except Exception as e:
                    self.logger.warning(f"Could not load artifact {artifact_hash}: {e}")
                    continue
        
        self.logger.info(f"Discovered {len(artifacts)} analysis artifacts for batch {batch_id}")
        return artifacts

    def _prepare_statistical_prompt(self,
                                  framework_content: str,
                                  experiment_content: str,
                                  corpus_manifest: str,
                                  analysis_artifacts: Dict[str, Any]) -> str:
        """
        Prepare the statistical analysis prompt using the template.
        
        Adapts the existing AutomatedStatisticalAnalysisAgent prompt for
        the new THIN approach with LLM internal execution.
        """
        
        # Extract experiment metadata
        experiment_name = self.experiment_metadata.get('name', 'Unknown Experiment')
        experiment_description = self.experiment_metadata.get('description', 'No description available')
        
        # Prepare analysis data summary for prompt
        sample_data = ""
        data_columns = ""
        
        if analysis_artifacts:
            # Create a structured summary of the analysis data
            data_summary = {
                "total_artifacts": len(analysis_artifacts),
                "artifact_types": {},
                "sample_structure": {}
            }
            
            # Analyze artifact structure
            for artifact_hash, artifact_data in analysis_artifacts.items():
                artifact_type = artifact_data.get('step', 'unknown')
                if artifact_type not in data_summary["artifact_types"]:
                    data_summary["artifact_types"][artifact_type] = 0
                data_summary["artifact_types"][artifact_type] += 1
                
                # Extract sample structure from score_extraction artifacts
                if artifact_type == "score_extraction" and "scores_extraction" in artifact_data:
                    scores_data = artifact_data["scores_extraction"]
                    if isinstance(scores_data, str):
                        # Try to extract JSON from the string
                        try:
                            import re
                            json_match = re.search(r'\{.*\}', scores_data, re.DOTALL)
                            if json_match:
                                scores_json = json.loads(json_match.group())
                                if isinstance(scores_json, dict):
                                    data_summary["sample_structure"] = {
                                        "dimensions": list(scores_json.keys()),
                                        "score_fields": ["raw_score", "salience", "confidence"] if scores_json else []
                                    }
                        except (json.JSONDecodeError, AttributeError):
                            pass
            
            sample_data = json.dumps(data_summary, indent=2)
            data_columns = "Analysis artifacts contain: score_extraction (dimensional scores), derived_metrics (calculated metrics), analysis_metadata (document info)"
        
        # Use the prompt template with placeholders (using replace to avoid KeyError from JSON braces)
        prompt = self.prompt_template
        prompt = prompt.replace('{framework_content}', framework_content)
        prompt = prompt.replace('{experiment_name}', experiment_name)
        prompt = prompt.replace('{experiment_description}', experiment_description)
        prompt = prompt.replace('{research_questions}', "See experiment content for detailed research questions and hypotheses")
        prompt = prompt.replace('{experiment_content}', experiment_content)
        prompt = prompt.replace('{data_columns}', data_columns)
        prompt = prompt.replace('{sample_data}', sample_data)
        prompt = prompt.replace('{corpus_manifest}', corpus_manifest)
        
        # Add analysis artifacts content
        prompt += f"\n\n**ANALYSIS ARTIFACTS:**\n"
        prompt += f"You have {len(analysis_artifacts)} analysis artifacts to process:\n\n"
        
        for artifact_hash, artifact_data in analysis_artifacts.items():
            prompt += f"--- ARTIFACT {artifact_hash} ---\n"
            prompt += f"Type: {artifact_data.get('step', 'unknown')}\n"
            prompt += f"Analysis ID: {artifact_data.get('analysis_id', 'unknown')}\n"
            prompt += json.dumps(artifact_data, indent=2)
            prompt += "\n\n"
        
        return prompt

    def _write_csv_file(self, filename: str, csv_content: str, batch_id: str) -> Path:
        """
        Write CSV content to the appropriate experiment data directory.
        
        Args:
            filename: Name of the CSV file
            csv_content: CSV content to write
            batch_id: Batch identifier for organization
            
        Returns:
            Path to the written CSV file
        """
        
        # Determine output directory - use experiment's data directory
        experiment_path = Path(self.security.experiment_root)
        
        # Look for existing run directories or create a new one
        runs_dir = experiment_path / "runs"
        if runs_dir.exists():
            # Find the most recent run directory
            run_dirs = [d for d in runs_dir.iterdir() if d.is_dir()]
            if run_dirs:
                latest_run = max(run_dirs, key=lambda x: x.stat().st_mtime)
                data_dir = latest_run / "data"
            else:
                # Create new run directory
                run_id = datetime.now().strftime("%Y%m%dT%H%M%SZ")
                data_dir = runs_dir / run_id / "data"
        else:
            # Create runs structure
            run_id = datetime.now().strftime("%Y%m%dT%H%M%SZ")
            data_dir = runs_dir / run_id / "data"
        
        # Ensure data directory exists
        data_dir.mkdir(parents=True, exist_ok=True)
        
        # Write CSV file
        csv_path = data_dir / filename
        with open(csv_path, 'w', encoding='utf-8') as f:
            f.write(csv_content)
        
        self.logger.info(f"Wrote CSV file: {csv_path}")
        return csv_path

    def generate_functions(self, workspace_path: Path, pre_assembled_prompt: str = None) -> Dict[str, Any]:
        """
        Compatibility method for orchestrator integration.
        
        This method provides the same interface as AutomatedStatisticalAnalysisAgent
        but uses the new THIN approach with LLM internal execution.
        
        Args:
            workspace_path: Path to workspace directory (for compatibility)
            pre_assembled_prompt: Pre-assembled prompt content (if provided)
            
        Returns:
            Dictionary with success status and results
        """
        
        try:
            # If pre-assembled prompt is provided, extract components from it
            if pre_assembled_prompt:
                framework_content, experiment_content, corpus_manifest = self._extract_from_assembled_prompt(pre_assembled_prompt)
            else:
                # Load components from workspace
                framework_content = self._load_framework_from_workspace(workspace_path)
                experiment_content = self._load_experiment_from_workspace(workspace_path)
                corpus_manifest = self._load_corpus_manifest_from_workspace(workspace_path)
            
            # Generate batch ID for this statistical analysis
            batch_id = f"stats_{datetime.now().strftime('%Y%m%dT%H%M%SZ')}"
            
            # Run the full 3-step analysis
            result = self.analyze_batch(
                framework_content=framework_content,
                experiment_content=experiment_content,
                corpus_manifest=corpus_manifest,
                batch_id=batch_id
            )
            
            # Return in format expected by orchestrator
            return {
                "success": True,
                "batch_id": batch_id,
                "statistical_analysis": result["statistical_analysis"],
                "verification_status": result["verification"]["verification_status"],
                "csv_files": result["csv_generation"]["csv_files"],
                "workspace_path": str(workspace_path)
            }
            
        except Exception as e:
            self.logger.error(f"Statistical analysis failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "batch_id": None
            }

    def _extract_from_assembled_prompt(self, prompt: str) -> tuple:
        """
        Extract framework, experiment, and corpus content from assembled prompt.
        
        Args:
            prompt: Pre-assembled prompt string
            
        Returns:
            Tuple of (framework_content, experiment_content, corpus_manifest)
        """
        
        # Simple extraction based on prompt structure
        # This is a fallback - ideally the orchestrator should pass components directly
        
        framework_content = ""
        experiment_content = ""
        corpus_manifest = ""
        
        # Try to extract sections from the prompt
        lines = prompt.split('\n')
        current_section = None
        
        for line in lines:
            if "**FRAMEWORK SPECIFICATION:**" in line:
                current_section = "framework"
                continue
            elif "**FULL EXPERIMENT CONTENT:**" in line:
                current_section = "experiment"
                continue
            elif "**CORPUS MANIFEST:**" in line:
                current_section = "corpus"
                continue
            elif line.startswith("**") and line.endswith(":**"):
                current_section = None
                continue
                
            if current_section == "framework":
                framework_content += line + "\n"
            elif current_section == "experiment":
                experiment_content += line + "\n"
            elif current_section == "corpus":
                corpus_manifest += line + "\n"
        
        return framework_content.strip(), experiment_content.strip(), corpus_manifest.strip()

    def _load_framework_from_workspace(self, workspace_path: Path) -> str:
        """Load framework content from workspace."""
        framework_file = workspace_path / "framework_content.md"
        if framework_file.exists():
            return framework_file.read_text(encoding='utf-8')
        return ""

    def _load_experiment_from_workspace(self, workspace_path: Path) -> str:
        """Load experiment content from workspace."""
        experiment_file = workspace_path / "experiment_spec.json"
        if experiment_file.exists():
            return experiment_file.read_text(encoding='utf-8')
        return ""

    def _load_corpus_manifest_from_workspace(self, workspace_path: Path) -> str:
        """Load corpus manifest from workspace."""
        # Look for corpus manifest in various possible locations
        possible_files = [
            workspace_path / "corpus_manifest.md",
            workspace_path / "corpus.md",
            workspace_path / "corpus_manifest.json"
        ]
        
        for corpus_file in possible_files:
            if corpus_file.exists():
                return corpus_file.read_text(encoding='utf-8')
        
        return ""

    def _calculate_total_costs(self, statistical_result: Dict[str, Any], 
                             verification_result: Dict[str, Any], 
                             csv_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate total costs and performance metrics across all steps.
        
        Args:
            statistical_result: Results from step 1
            verification_result: Results from step 2  
            csv_result: Results from step 3
            
        Returns:
            Dictionary with aggregated cost and performance information
        """
        
        # Extract cost info from each step
        stat_cost = statistical_result.get("cost_info", {})
        verify_cost = verification_result.get("cost_info", {})
        csv_cost = csv_result.get("cost_info", {})
        
        # Calculate totals
        total_cost = (
            stat_cost.get("response_cost", 0.0) +
            verify_cost.get("response_cost", 0.0) +
            csv_cost.get("response_cost", 0.0)
        )
        
        total_execution_time = (
            stat_cost.get("execution_time_seconds", 0.0) +
            verify_cost.get("execution_time_seconds", 0.0) +
            csv_cost.get("execution_time_seconds", 0.0)
        )
        
        total_tokens = (
            stat_cost.get("total_tokens", 0) +
            verify_cost.get("total_tokens", 0) +
            csv_cost.get("total_tokens", 0)
        )
        
        return {
            "total_cost_usd": total_cost,
            "total_execution_time_seconds": total_execution_time,
            "total_tokens": total_tokens,
            "cost_breakdown": {
                "statistical_execution": stat_cost.get("response_cost", 0.0),
                "verification": verify_cost.get("response_cost", 0.0),
                "csv_generation": csv_cost.get("response_cost", 0.0)
            },
            "performance_breakdown": {
                "statistical_execution_time": stat_cost.get("execution_time_seconds", 0.0),
                "verification_time": verify_cost.get("execution_time_seconds", 0.0),
                "csv_generation_time": csv_cost.get("execution_time_seconds", 0.0)
            },
            "models_used": [
                stat_cost.get("model", "unknown"),
                verify_cost.get("model", "unknown"),
                csv_cost.get("model", "unknown")
            ]
        }

    def check_cache(self, batch_id: str) -> Optional[Dict[str, Any]]:
        """
        Check if statistical analysis results are already cached.
        
        Args:
            batch_id: Batch identifier for cache lookup
            
        Returns:
            Cached results if available, None otherwise
        """
        
        # Search through artifact registry for matching statistical analysis
        for artifact_hash, artifact_info in self.storage.registry.items():
            metadata = artifact_info.get("metadata", {})
            
            if (metadata.get("artifact_type") == "statistical_analysis" and
                metadata.get("batch_id") == batch_id):
                
                self.logger.info(f"💾 Cache hit for statistical analysis: {batch_id}")
                
                try:
                    cached_content = self.storage.get_artifact(artifact_hash)
                    cached_result = json.loads(cached_content.decode('utf-8'))
                    
                    self.audit.log_agent_event(self.agent_name, "cache_hit", {
                        "batch_id": batch_id,
                        "cached_artifact_hash": artifact_hash
                    })
                    
                    # Add cached flag to indicate this result came from cache
                    cached_result["cached"] = True
                    return cached_result
                    
                except Exception as e:
                    self.logger.warning(f"⚠️ Cache hit but failed to load content: {e}")
                    continue
        
        # No cache hit
        self.logger.info(f"🔍 No cache hit for {batch_id} - will perform analysis...")
        return None

    def store_cache(self, batch_id: str, result: Dict[str, Any]) -> str:
        """
        Store statistical analysis results in cache.
        
        Args:
            batch_id: Batch identifier
            result: Analysis results to cache
            
        Returns:
            Artifact hash of cached result
        """
        
        cache_metadata = {
            "artifact_type": "statistical_analysis_cache",
            "batch_id": batch_id,
            "cached_at": datetime.now(timezone.utc).isoformat(),
            "agent_name": self.agent_name
        }
        
        cache_hash = self.storage.put_artifact(
            json.dumps(result, indent=2).encode('utf-8'),
            cache_metadata
        )
        
        self.audit.log_agent_event(self.agent_name, "cache_store", {
            "batch_id": batch_id,
            "cache_artifact_hash": cache_hash
        })
        
        return cache_hash
