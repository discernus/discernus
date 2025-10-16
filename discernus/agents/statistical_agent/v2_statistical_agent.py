#!/usr/bin/env python3
"""
V2 Statistical Agent - Atomic Processing Implementation
=====================================================

This agent processes atomic score and derived metrics artifacts from the AnalysisAgent
and performs comprehensive statistical analysis.

THIN Principles:
- Each document's scores are processed individually
- LLM handles all statistical intelligence
- Agent only adapts interfaces, no business logic
- Atomic artifacts for downstream consumption
"""

import json
import logging
import yaml
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional

from discernus.core.security_boundary import ExperimentSecurityBoundary
from discernus.core.audit_logger import AuditLogger
from discernus.core.local_artifact_storage import LocalArtifactStorage
from discernus.core.agent_result import AgentResult
from discernus.core.run_context import RunContext
from discernus.core.standard_agent import StandardAgent
from discernus.gateway.llm_gateway_enhanced import EnhancedLLMGateway
from discernus.gateway.model_registry import get_model_registry


class V2StatisticalAgent(StandardAgent):
    """
    V2 Statistical Agent for atomic processing of score artifacts.
    
    This agent processes individual score and derived metrics artifacts
    from the AnalysisAgent and performs comprehensive statistical analysis.
    """
    
    def __init__(self, 
                 security: ExperimentSecurityBoundary,
                 storage: LocalArtifactStorage,
                 audit: AuditLogger):
        """
        Initialize the V2 Statistical Agent.
        
        Args:
            security: Security boundary for file operations
            storage: Content-addressable artifact storage
            audit: Audit logger for comprehensive event tracking
        """
        super().__init__(security, storage, audit)
        self.agent_name = "V2StatisticalAgent"
        self.logger = logging.getLogger(__name__)
        
        # Initialize LLM gateway
        self.gateway = EnhancedLLMGateway(get_model_registry())
        
        self.logger.info(f"Initialized {self.agent_name}")
    
    def _load_prompt_template(self) -> str:
        """Load the statistical analysis prompt template from YAML file."""
        prompt_path = Path(__file__).parent / "prompt.yaml"
        if not prompt_path.exists():
            error_msg = f"StatisticalAgent prompt file not found at {prompt_path}"
            self.audit.log_agent_event(self.agent_name, "prompt_error", {"error": error_msg})
            raise FileNotFoundError(error_msg)
        
        with open(prompt_path, 'r') as f:
            yaml_content = f.read()
        prompt_data = yaml.safe_load(yaml_content)
        return prompt_data['template']
    
    def get_capabilities(self) -> Dict[str, Any]:
        """
        Get agent capabilities and metadata.
        
        Returns:
            Dictionary describing agent capabilities
        """
        return {
            "agent_name": self.agent_name,
            "agent_type": "V2StatisticalAgent",
            "capabilities": [
                "statistical_analysis",
                "atomic_score_processing"
            ],
            "input_types": ["score_extraction_artifacts"],
            "output_types": ["statistical_analysis"],
            "models_used": ["vertex_ai/gemini-2.5-flash-lite", "vertex_ai/gemini-2.5-pro"]
        }
    
    def _validate_inputs(self, run_context: RunContext) -> bool:
        """Strict contract enforcement: ALL required input assets must be present or fail hard."""
        
        # Required Asset 1: Score extraction artifacts (primary data source)
        score_artifacts = self.storage.find_artifacts_by_metadata(artifact_type="score_extraction")
        if score_artifacts is None:
            self.logger.error("CRITICAL: find_artifacts_by_metadata returned None for score_extraction")
            return False
        if not score_artifacts:
            self.logger.error("CONTRACT VIOLATION: No score_extraction artifacts found via CAS discovery")
            return False
        self.logger.info(f"✓ Score extraction: Found {len(score_artifacts)} artifacts")
        
        # Score extraction is now handled directly in composite analysis
        # No separate score extraction validation needed
        
        # Required Asset 3: Framework artifacts
        framework_artifacts = self.storage.find_artifacts_by_metadata(artifact_type="framework")
        if framework_artifacts is None:
            self.logger.error("CRITICAL: find_artifacts_by_metadata returned None for framework")
            return False
        if not framework_artifacts:
            self.logger.error("CONTRACT VIOLATION: No framework artifacts found via CAS discovery")
            return False
        self.logger.info(f"✓ Framework: Found {len(framework_artifacts)} artifacts")
        
        # Required Asset 4: Corpus manifest artifacts
        corpus_manifest_artifacts = self.storage.find_artifacts_by_metadata(artifact_type="corpus_manifest")
        if corpus_manifest_artifacts is None:
            self.logger.error("CRITICAL: find_artifacts_by_metadata returned None for corpus_manifest")
            return False
        if not corpus_manifest_artifacts:
            self.logger.error("CONTRACT VIOLATION: No corpus_manifest artifacts found via CAS discovery")
            return False
        self.logger.info(f"✓ Corpus manifest: Found {len(corpus_manifest_artifacts)} artifacts")
        
        # Required Asset 5: Corpus document artifacts
        corpus_document_artifacts = self.storage.find_artifacts_by_metadata(artifact_type="corpus_document")
        if corpus_document_artifacts is None:
            self.logger.error("CRITICAL: find_artifacts_by_metadata returned None for corpus_document")
            return False
        if not corpus_document_artifacts:
            self.logger.error("CONTRACT VIOLATION: No corpus_document artifacts found via CAS discovery")
            return False
        self.logger.info(f"✓ Corpus documents: Found {len(corpus_document_artifacts)} documents")
        
        self.logger.info("CONTRACT FULFILLED: All required input assets present - proceeding with statistical analysis")
        return True
    
    def execute(self, run_context: RunContext) -> AgentResult:
        """
        Execute statistical analysis on atomic score artifacts.
        
        Args:
            run_context: Run context containing analysis artifacts and metadata
            
        Returns:
            AgentResult with statistical analysis artifacts
        """
        try:
            # Validate inputs - strict contract enforcement
            if not self._validate_inputs(run_context):
                return AgentResult(
                    success=False,
                    artifacts=[],
                    metadata={"agent_name": self.agent_name, "error": "Input validation failed"},
                    error_message="Required inputs missing for statistical analysis"
                )
            
            # Pure CAS architecture - no run_context storage needed
            
            self.logger.info("Starting V2 Statistical Agent execution")
            self.audit.log_agent_event(self.agent_name, "execution_started", {
                "run_context_type": type(run_context).__name__
            })
            
            # Validate run context
            if not run_context:
                return AgentResult(
                    success=False,
                    artifacts=[],
                    metadata={"agent_name": self.agent_name, "error": "run_context is required"},
                    error_message="run_context is required"
                )
            
            # REMOVED: Framework file reading - now handled by CAS discovery in _step1_statistical_analysis
            
            # STEP 1: CAS-native discovery of score_extraction artifacts for pandas processing
            score_artifacts = self.storage.find_artifacts_by_metadata(artifact_type="score_extraction")
            
            # Defensive programming: Handle None return from storage
            if score_artifacts is None:
                self.logger.error("CRITICAL: find_artifacts_by_metadata returned None for score_extraction")
                return AgentResult(
                    success=False,
                    artifacts=[],
                    metadata={"agent_name": self.agent_name, "error": "storage_returned_none"},
                    error_message="Storage system returned None instead of score_extraction artifact list"
                )
            
            if not score_artifacts:
                self.logger.error("CONTRACT VIOLATION: No score_extraction artifacts found via CAS discovery")
                return AgentResult(
                    success=False,
                    artifacts=[],
                    metadata={"agent_name": self.agent_name, "error": "no_score_extraction_artifacts"},
                    error_message="No score_extraction artifacts found - cannot proceed with statistical analysis"
                )
            
            self.logger.info(f"Discovered {len(score_artifacts)} score_extraction artifacts via CAS")
            
            # STEP 1: Generate baseline statistics using pandas (deterministic, no hallucination risk)
            baseline_stats_result = self._step1_generate_baseline_statistics(score_artifacts, run_context)
            if not baseline_stats_result.success:
                return baseline_stats_result
            
            # STEP 2: Score extraction is now handled directly in composite analysis
            # No separate score extraction processing needed
            
            # Generate batch ID
            batch_id = f"stats_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"
            
            # Define model to use for statistical analysis
            model_used = "vertex_ai/gemini-2.5-flash-lite"
            
            # STEP 2: Enhanced Statistical Analysis with baseline statistics + LLM intelligence
            # Get the baseline statistics artifact from Step 1
            baseline_artifacts = self.storage.find_artifacts_by_metadata(
                artifact_type="baseline_statistics"
            )
            
            if not baseline_artifacts:
                self.logger.error("No baseline statistics artifact found from Step 1")
                return AgentResult(
                    success=False,
                    artifacts=[],
                    metadata={"agent_name": self.agent_name, "error": "no_baseline_stats"},
                    error_message="No baseline statistics found - Step 1 may have failed"
                )
            
            # Get the baseline statistics content
            baseline_stats_content = self.storage.get_artifact(baseline_artifacts[0]).decode('utf-8')
            baseline_stats_data = json.loads(baseline_stats_content)
            
            # Step 2: Enhanced Statistical Analysis with baseline + LLM
            statistical_analysis_content = self._step2_enhanced_statistical_analysis(
                baseline_stats_data, batch_id, run_context
            )
            if not statistical_analysis_content:
                return AgentResult(
                    success=False,
                    artifacts=[],
                    metadata={"agent_name": self.agent_name, "error": "enhanced statistical analysis failed"},
                    error_message="Enhanced statistical analysis failed"
                )
            
            # THIN: Store raw LLM response directly, no parsing
            statistical_artifact_data = {
                "analysis_id": f"stats_{batch_id}",
                "step": "statistical_analysis",
                "model_used": model_used,
                "statistical_analysis": statistical_analysis_content.strip(),  # Ensure leading/trailing whitespace is removed
                "documents_processed": len(score_artifacts),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            statistical_content_bytes = json.dumps(statistical_artifact_data, indent=2).encode('utf-8')
            statistical_artifact_hash = self.storage.put_artifact(
                statistical_content_bytes,
                {"artifact_type": "statistical_analysis", "batch_id": batch_id}
            )
            # REMOVED: run_context.statistical_artifacts - replaced with CAS discovery
            run_context.statistical_results = statistical_analysis_content.strip()  # THIN: Raw LLM response
            
            
            # Create artifacts list with proper hashes
            artifacts = [
                {
                    "type": "statistical_analysis",
                    "content": statistical_artifact_data,
                    "metadata": {
                        "artifact_type": "statistical_analysis",
                        "phase": "statistical",
                        "batch_id": batch_id,
                        "timestamp": datetime.now().isoformat(),
                        "agent_name": self.agent_name,
                        "artifact_hash": statistical_artifact_hash
                    }
                }
            ]
            
            self.audit.log_agent_event(self.agent_name, "execution_completed", {
                "batch_id": batch_id,
                "artifacts_created": len(artifacts),
                "documents_processed": len(score_artifacts)
            })
            
            return AgentResult(
                success=True,
                artifacts=artifacts,
                metadata={
                    "agent_name": self.agent_name,
                    "batch_id": batch_id,
                    "documents_processed": len(score_artifacts),
                    "artifacts_created": len(artifacts)
                }
            )
            
        except Exception as e:
            self.logger.error(f"V2StatisticalAgent execution failed: {e}")
            self.audit.log_agent_event(self.agent_name, "execution_failed", {
                "error": str(e)
            })
            return AgentResult(
                success=False,
                artifacts=[],
                metadata={"agent_name": self.agent_name, "error": str(e)},
                error_message=f"V2StatisticalAgent execution failed: {str(e)}"
            )
    
    
    def _step1_generate_baseline_statistics(self, score_artifacts: List[Dict[str, Any]], run_context: RunContext) -> AgentResult:
        """
        STEP 1: Generate baseline statistics using pandas processing of score_extraction artifacts.
        
        This step eliminates hallucination risk for basic statistical calculations by using
        deterministic pandas operations on the structured data from score extraction.
        
        Args:
            score_artifacts: List of score_extraction artifacts from CAS discovery
            run_context: Current run context for artifact creation
            
        Returns:
            AgentResult with baseline statistics artifact
        """
        try:
            # Import the score extraction processor and experiment parameters
            from discernus.core.composite_analysis_processor import ScoreExtractionProcessor
            from discernus.core.experiment_parameters import parse_experiment_parameters
            
            # Load experiment parameters
            experiment_path = Path(run_context.experiment_dir)
            experiment_params = parse_experiment_parameters(experiment_path)
            
            # Convert CAS artifact hashes to file paths for processor
            artifact_paths = []
            for artifact_hash in score_artifacts:
                try:
                    # Get human filename from registry
                    human_filename = self.storage.registry[artifact_hash].get("human_filename", artifact_hash)
                    
                    # Construct full path (score_extraction artifacts are in analysis subdirectory)
                    artifact_path = self.storage.artifacts_dir / "analysis" / human_filename
                    
                    if artifact_path.exists():
                        artifact_paths.append(artifact_path)
                    else:
                        self.logger.warning(f"Score extraction artifact file not found: {artifact_path}")
                        
                except KeyError:
                    self.logger.warning(f"Artifact hash not found in registry: {artifact_hash}")
                except Exception as e:
                    self.logger.warning(f"Error processing artifact hash {artifact_hash}: {e}")
            
            if not artifact_paths:
                self.logger.error("No valid score extraction artifact paths found")
                return AgentResult(
                    success=False,
                    artifacts=[],
                    metadata={"agent_name": self.agent_name, "error": "no_valid_artifacts"},
                    error_message="No valid score extraction artifacts found for processing"
                )
            
            # Process score extractions to generate baseline statistics with experiment parameters
            processor = ScoreExtractionProcessor(experiment_params)
            baseline_statistics = processor.process_score_extractions(artifact_paths)
            
            # Create CAS artifact for baseline statistics
            baseline_artifact_data = {
                "analysis_id": f"baseline_stats_{self.storage.run_name}",
                "step": "baseline_statistics",
                "processor_type": "score_extraction_pandas",
                "processor_version": "1.0.0",
                "baseline_statistics": baseline_statistics,
                "artifacts_processed": len(artifact_paths),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
            # Store as CAS artifact
            baseline_artifact_content = json.dumps(baseline_artifact_data, indent=2, default=str)
            baseline_artifact_hash = self.storage.put_artifact(
                baseline_artifact_content.encode('utf-8'),
                {
                    "artifact_type": "baseline_statistics",
                    "step": "baseline_statistics", 
                    "agent_name": self.agent_name,
                    "run_name": self.storage.run_name,
                    "processor_type": "composite_analysis_pandas"
                }
            )
            
            self.logger.info(f"Generated baseline statistics artifact: {baseline_artifact_hash}")
            
            # Log successful baseline statistics generation
            self.audit.log_agent_event(
                agent_name=self.agent_name,
                event_type="baseline_statistics_generated",
                data={
                    "artifact_hash": baseline_artifact_hash,
                    "score_artifacts_processed": len(artifact_paths),
                    "document_count": baseline_statistics.get('processing_metadata', {}).get('document_count', 0),
                    "framework": baseline_statistics.get('processing_metadata', {}).get('framework_metadata', {}).get('framework_name', 'unknown')
                }
            )
            
            return AgentResult(
                success=True,
                artifacts=[{
                    "hash": baseline_artifact_hash,
                    "type": "baseline_statistics",
                    "metadata": {
                        "step": "baseline_statistics",
                        "processor_type": "score_extraction_pandas",
                        "documents_processed": baseline_statistics.get('processing_metadata', {}).get('document_count', 0)
                    }
                }],
                metadata={
                    "agent_name": self.agent_name,
                    "step": "baseline_statistics",
                    "baseline_artifact_hash": baseline_artifact_hash
                }
            )
            
        except Exception as e:
            self.logger.error(f"Failed to generate baseline statistics: {str(e)}")
            return AgentResult(
                success=False,
                artifacts=[],
                metadata={"agent_name": self.agent_name, "error": "baseline_generation_failed"},
                error_message=f"Baseline statistics generation failed: {str(e)}"
            )
    
    def _step2_enhanced_statistical_analysis(self, baseline_stats_data: Dict[str, Any], batch_id: str, run_context: RunContext) -> Optional[str]:
        """
        STEP 2: Enhanced statistical analysis using baseline statistics + LLM intelligence.
        
        This step takes the reliable baseline statistics from Step 1 and uses LLM intelligence
        to perform experiment-specific analysis, hypothesis testing, and interpretation.
        
        Args:
            baseline_stats_data: Baseline statistics from pandas processing (Step 1)
            batch_id: Batch identifier
            
        Returns:
            Complete LLM response with enhanced statistical results, or None if failed
        """
        try:
            # Load the externalized prompt template
            prompt_template = self._load_prompt_template()
            self.logger.info(f"Loaded prompt template, length: {len(prompt_template)}")
            
            # Load experiment parameters for reliability filtering context
            from discernus.core.experiment_parameters import parse_experiment_parameters
            experiment_path = Path(run_context.experiment_dir)
            experiment_params = parse_experiment_parameters(experiment_path)
            
            # CAS Discovery: Get source materials via artifact discovery
            
            # Get framework from CAS discovery
            framework_artifacts = self.storage.find_artifacts_by_metadata(artifact_type="framework")
            if framework_artifacts is None:
                self.logger.error("CRITICAL: find_artifacts_by_metadata returned None for framework")
                raise ValueError("Storage system returned None for framework artifacts")
            if not framework_artifacts:
                raise ValueError("No framework artifacts found via CAS discovery")
            framework_content = self.storage.get_artifact(framework_artifacts[0]).decode('utf-8')
            
            # Get corpus manifest from CAS discovery
            corpus_manifest_artifacts = self.storage.find_artifacts_by_metadata(artifact_type="corpus_manifest")
            if corpus_manifest_artifacts is None:
                self.logger.error("CRITICAL: find_artifacts_by_metadata returned None for corpus_manifest")
                raise ValueError("Storage system returned None for corpus manifest artifacts")
            if not corpus_manifest_artifacts:
                raise ValueError("No corpus_manifest artifacts found via CAS discovery")
            corpus_manifest_content = self.storage.get_artifact(corpus_manifest_artifacts[0]).decode('utf-8')
            
            # Get experiment content from CAS discovery
            experiment_artifacts = self.storage.find_artifacts_by_metadata(artifact_type="experiment_spec")
            if experiment_artifacts is None:
                self.logger.error("CRITICAL: find_artifacts_by_metadata returned None for experiment_spec")
                raise ValueError("Storage system returned None for experiment spec artifacts")
            if not experiment_artifacts:
                raise ValueError("No experiment_spec artifacts found via CAS discovery")
            experiment_content = self.storage.get_artifact(experiment_artifacts[0]).decode('utf-8')
            
            # Extract experiment metadata from the actual experiment content
            experiment_id = 'unknown'
            experiment_description = 'Statistical analysis of unknown experiment'
            research_questions = 'How do patterns manifest through the framework dimensions?'
            
            # Try to extract real metadata from experiment content
            try:
                import re
                # Extract experiment name from title or abstract
                title_match = re.search(r'^#\s+(.+)$', experiment_content, re.MULTILINE)
                if title_match:
                    experiment_id = title_match.group(1).strip()
                
                # Extract description from abstract section
                abstract_match = re.search(r'## Abstract\s*\n(.*?)(?=\n##|\Z)', experiment_content, re.DOTALL)
                if abstract_match:
                    abstract_text = abstract_match.group(1).strip()
                    # Use first sentence or first 200 chars as description
                    sentences = abstract_text.split('.')
                    if sentences:
                        experiment_description = sentences[0].strip() + '.'
                        if len(experiment_description) > 200:
                            experiment_description = experiment_description[:200] + '...'
                
                # Extract research questions
                questions_match = re.search(r'## Research Questions\s*\n(.*?)(?=\n##|\Z)', experiment_content, re.DOTALL)
                if questions_match:
                    research_questions = questions_match.group(1).strip()
                    
            except Exception as e:
                self.logger.warning(f"Could not extract experiment metadata: {e}")
                # Keep defaults
            
            # STEP 2 ENHANCEMENT: Include baseline statistics from pandas processing
            baseline_stats_json = json.dumps(baseline_stats_data.get('baseline_statistics', {}), indent=2, default=str)
            
            # Raw artifact data is now handled directly in composite analysis
            # No separate raw artifact processing needed
            
            # NO TRUNCATION: All content is sacred intellectual assets
            
            # Create reliability filtering context from experiment parameters
            rf_params = experiment_params.reliability_filtering
            
            if rf_params is not None and rf_params.is_filtering_enabled():
                reliability_filtering_context = f"""
  **RELIABILITY FILTERING: ENABLED**
  
  The experiment explicitly specified the following reliability filtering parameters:
  - **salience_threshold**: {rf_params.salience_threshold} (minimum salience for inclusion)
  - **confidence_threshold**: {rf_params.confidence_threshold} (minimum confidence for inclusion)  
  - **reliability_threshold**: {rf_params.reliability_threshold} (minimum reliability for inclusion)
  - **reliability_calculation**: {rf_params.reliability_calculation} (method for calculating reliability)
  
  Based on these parameters, dimensions are categorized as:
  - **included_high_reliability**: Dimensions with high reliability (≥ 0.7)
  - **included_medium_reliability**: Dimensions with moderate reliability (0.4 ≤ reliability < 0.7)
  - **excluded_low_salience**: Dimensions with low salience (< {rf_params.salience_threshold}) - excluded from analysis
  - **borderline_excluded**: Dimensions with low reliability (0.25 ≤ reliability < 0.4)
  - **clearly_excluded**: Dimensions with very low reliability (< 0.25)
                """
            else:
                reliability_filtering_context = """
  **RELIABILITY FILTERING: DISABLED**
  
  The experiment did NOT specify reliability filtering parameters.
  As a result, ALL dimensions from ALL documents are included in the statistical analysis (no filtering applied).
  This means the sample includes all scored dimensions regardless of salience, confidence, or reliability values.
                """
            
            # Prepare the enhanced prompt with baseline statistics + real extracted metadata
            prompt = prompt_template.format(
                framework_content=framework_content,
                experiment_name=experiment_id,
                experiment_description=experiment_description,
                research_questions=research_questions,
                experiment_content=experiment_content,
                sample_data="",  # Sample data now handled in composite analysis
                corpus_manifest=corpus_manifest_content,
                baseline_statistics=baseline_stats_json,
                reliability_filtering_context=reliability_filtering_context
            )
            
            # Debug prompt construction
            self.logger.info(f"Prompt length: {len(prompt)} characters")
            # Raw data block no longer needed
            self.logger.info(f"Framework content length: {len(framework_content)} characters")
            self.logger.info(f"Corpus manifest length: {len(corpus_manifest_content)} characters")

            # Raw artifacts validation no longer needed
            
            self.audit.log_agent_event(self.agent_name, "step1_started", {
                "batch_id": batch_id,
                "step": "statistical_analysis",
                "model": "vertex_ai/gemini-2.5-flash-lite",
                "artifacts_count": 0
            })
            
            # Call LLM with Flash-Lite and reasoning=1 for pure statistical calculation
            model_used = "vertex_ai/gemini-2.5-flash-lite"
            response = self.gateway.execute_call(
                model=model_used,
                prompt=prompt,
                reasoning=1
            )
            
            # Debug LLM response
            self.logger.info(f"LLM response type: {type(response)}")
            self.logger.info(f"LLM response: {response}")
            
            if isinstance(response, tuple):
                content, metadata = response
                self.logger.info(f"Tuple response - content type: {type(content)}, metadata type: {type(metadata)}")
            else:
                content = response.get('content', '')
                metadata = response.get('metadata', {})
                self.logger.info(f"Dict response - content type: {type(content)}, metadata type: {type(metadata)}")
            
            # Log LLM interaction with cost data
            if metadata and 'usage' in metadata:
                usage_data = metadata['usage']
                self.audit.log_llm_interaction(
                    model=model_used,
                    prompt=prompt,
                    response=content,
                    agent_name=self.agent_name,
                    interaction_type="statistical_analysis",
                    metadata={
                        "prompt_tokens": usage_data.get('prompt_tokens', 0),
                        "completion_tokens": usage_data.get('completion_tokens', 0),
                        "total_tokens": usage_data.get('total_tokens', 0),
                        "response_cost_usd": usage_data.get('response_cost_usd', 0.0),
                        "step": "statistical_analysis",
                        "batch_id": batch_id,
                        "artifacts_count": 0
                    }
                )
            
            # Defensive programming: Handle None values
            if content is None:
                self.logger.error("CRITICAL: content is None from LLM response")
                raise ValueError("LLM response content is None")
            
            self.logger.info(f"LLM response length: {len(content)}")
            self.logger.info(f"LLM response preview: {content[:200]}...")
            
            # THIN: Return raw LLM response directly, no parsing
            if content and content.strip():
                self.audit.log_agent_event(self.agent_name, "step1_completed", {
                    "batch_id": batch_id,
                    "step": "statistical_analysis",
                    "response_length": len(content)
                })
                return content.strip()
            else:
                self.logger.error("Statistical analysis returned empty response")
                return None
                
        except Exception as e:
            self.logger.error(f"Step 1 failed: {e}")
            return None
    
    
    # REMOVED: _read_framework_file - replaced with CAS discovery in _step1_statistical_analysis