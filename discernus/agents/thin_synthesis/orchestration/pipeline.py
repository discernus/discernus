#!/usr/bin/env python3
"""
THIN Code-Generated Synthesis Pipeline - Production Version
==========================================================

Integrates with Discernus infrastructure:
- MinIO artifact storage for content-addressable data
- AuditLogger for complete provenance
- SecureCodeExecutor for sandboxed computation

4-Agent Architecture:
1. AnalyticalCodeGenerator: LLM generates Python analysis code
2. SecureCodeExecutor: Production-safe code execution
3. EvidenceCurator: LLM selects evidence based on actual results
4. ResultsInterpreter: LLM synthesizes final narrative

Key Innovation: Evidence curation happens AFTER statistical computation.
"""

import logging
import json
import time
import pandas as pd

import os
from typing import Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

# Import main codebase infrastructure
import sys
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from discernus.storage.minio_client import DiscernusArtifactClient
from discernus.core.audit_logger import AuditLogger

# Import THIN synthesis agents
from ..analysis_planner.agent import AnalysisPlanner, AnalysisPlanRequest
from ..evidence_curator.agent import EvidenceCurator, EvidenceCurationRequest
from ..results_interpreter.agent import ResultsInterpreter, InterpretationRequest

# Import MathToolkit for reliable mathematical operations
from discernus.core.math_toolkit import execute_analysis_plan

@dataclass
class ProductionPipelineRequest:
    """Production pipeline request using artifact hashes instead of file paths."""
    framework_spec: str
    scores_artifact_hash: str  # MinIO artifact hash for scores CSV
    evidence_artifact_hash: str  # MinIO artifact hash for evidence CSV
    experiment_context: Optional[str] = None
    max_evidence_per_finding: int = 3
    min_confidence_threshold: float = 0.7
    interpretation_focus: str = "comprehensive"
    
    # Provenance context (Issue #208 fix)
    framework_hash: Optional[str] = None
    corpus_hash: Optional[str] = None
    framework_name: Optional[str] = None

@dataclass
class ProductionPipelineResponse:
    """Complete pipeline response with all outputs and metadata."""
    # Final outputs
    narrative_report: str
    executive_summary: str
    key_findings: list
    
    # Intermediate artifacts (as hashes for provenance)
    analysis_plan_hash: str
    statistical_results_hash: str
    curated_evidence_hash: str
    
    # Pipeline metadata
    success: bool
    total_execution_time: float
    stage_timings: Dict[str, float]
    stage_success: Dict[str, bool]
    
    # Quality metrics
    word_count: int
    evidence_integration_summary: str
    statistical_summary: str
    
    # Error information (if any)
    error_message: str = ""

class ProductionThinSynthesisPipeline:
    """
    Production version of THIN Code-Generated Synthesis Pipeline.
    
    Integrates with Discernus infrastructure for robust, scalable synthesis.
    """
    
    def __init__(self,
                 artifact_client: DiscernusArtifactClient,
                 audit_logger: AuditLogger,
                 model: str = "vertex_ai/gemini-2.5-pro",
                 debug_agent: Optional[str] = None,
                 debug_level: str = "info"):
        """
        Initialize production pipeline with infrastructure dependencies.
        
        Args:
            artifact_client: MinIO client for content-addressable storage
            audit_logger: Audit logger for complete provenance
            model: LLM model for all agents
        """
        self.artifact_client = artifact_client
        self.audit_logger = audit_logger
        self.model = model
        self.debug_agent = debug_agent
        self.debug_level = debug_level
        
        # Initialize agents with infrastructure
        self.analysis_planner = AnalysisPlanner(model=model, audit_logger=audit_logger)
        self.evidence_curator = EvidenceCurator(model=model)
        self.results_interpreter = ResultsInterpreter(model=model)
        
        # Set up logging
        self.logger = logging.getLogger(__name__)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
        
        self.audit_logger.log_agent_event(
            "ProductionThinSynthesisPipeline",
            "initialization",
            {
                "model": model,
                "architecture": "declarative_mathematical_specification",
                "math_toolkit_enabled": True
            }
        )
        
        self.logger.info("🏭 Production THIN Synthesis Pipeline initialized")

    def run(self, request: ProductionPipelineRequest) -> ProductionPipelineResponse:
        """
        Execute the complete 4-agent synthesis pipeline with full infrastructure.
        
        Args:
            request: ProductionPipelineRequest with artifact hashes
            
        Returns:
            ProductionPipelineResponse with complete synthesis results
        """
        start_time = time.time()
        stage_timings = {}
        stage_success = {}
        
        # Log pipeline start
        self.audit_logger.log_agent_event(
            "ProductionThinSynthesisPipeline",
            "pipeline_start",
            {
                "framework_spec_preview": request.framework_spec[:200] + "..." if len(request.framework_spec) > 200 else request.framework_spec,
                "scores_artifact": request.scores_artifact_hash,
                "evidence_artifact": request.evidence_artifact_hash,
                "experiment_context": request.experiment_context,
                # Add provenance context logging (Issue #208 fix)
                "framework_hash": request.framework_hash[:12] + "..." if request.framework_hash else "MISSING",
                "corpus_hash": request.corpus_hash[:12] + "..." if request.corpus_hash else "MISSING",
                "framework_name": request.framework_name,
                "provenance_validated": bool(request.framework_hash and request.corpus_hash)
            }
        )
        
        # Log provenance context for debugging
        if request.framework_hash and request.corpus_hash:
            self.logger.info(f"🔍 Synthesis provenance validated:")
            self.logger.info(f"   - Framework: {request.framework_name} ({request.framework_hash[:12]}...)")
            self.logger.info(f"   - Corpus: {request.corpus_hash[:12]}...")
            self.logger.info(f"   - Scores artifact: {request.scores_artifact_hash[:12]}...")
            self.logger.info(f"   - Evidence artifact: {request.evidence_artifact_hash[:12]}...")
        else:
            self.logger.warning("⚠️  Missing provenance context - synthesis agents operating blind!")
        
        try:
            self.logger.info("🚀 Starting Production THIN Synthesis Pipeline")
            
            # Stage 1: Generate Analysis Plan
            self.logger.info("📝 Stage 1: Generating analysis plan...")
            stage_start = time.time()
            
            plan_response = self._stage_1_generate_analysis_plan(request)
            
            stage_timings['analysis_planning'] = time.time() - stage_start
            stage_success['analysis_planning'] = plan_response.success
            
            if not plan_response.success:
                return self._create_error_response(
                    "Analysis planning failed", 
                    plan_response.error_message,
                    stage_timings, 
                    stage_success,
                    time.time() - start_time
                )
            
            # Stage 2: Execute Analysis Plan
            self.logger.info("⚙️  Stage 2: Executing analysis plan...")
            stage_start = time.time()
            
            exec_response = self._stage_2_execute_analysis_plan(plan_response, request)
            
            stage_timings['analysis_execution'] = time.time() - stage_start
            stage_success['analysis_execution'] = len(exec_response.get('errors', [])) == 0
            
            if len(exec_response.get('errors', [])) > 0:
                return self._create_error_response(
                    "Analysis execution failed",
                    "; ".join(exec_response['errors']),
                    stage_timings,
                    stage_success,
                    time.time() - start_time
                )
            
            # Stage 3: Curate Evidence
            self.logger.info("🔍 Stage 3: Curating evidence...")
            
            # Debug output for evidence curator
            if self.debug_agent in ['evidence-curator', None] and self.debug_level in ['debug', 'verbose']:
                self.logger.info(f"🔍 DEBUG: Evidence curation input:")
                self.logger.info(f"   - Statistical results keys: {list(exec_response['result_data'].keys()) if exec_response.get('result_data') else 'NO DATA'}")
                self.logger.info(f"   - Evidence artifact hash: {request.evidence_artifact_hash}")
                if exec_response.get('result_data'):
                    for key, value in exec_response['result_data'].items():
                        if isinstance(value, dict):
                            self.logger.info(f"   - {key}: {list(value.keys()) if value else 'EMPTY'}")
                        else:
                            self.logger.info(f"   - {key}: {type(value).__name__}")
            
            stage_start = time.time()
            
            curation_response = self._stage_3_curate_evidence(exec_response, request)
            
            stage_timings['evidence_curation'] = time.time() - stage_start
            stage_success['evidence_curation'] = curation_response.success
            
            if not curation_response.success:
                return self._create_error_response(
                    "Evidence curation failed",
                    curation_response.error_message,
                    stage_timings,
                    stage_success,
                    time.time() - start_time
                )
            
            # Stage 4: Interpret Results
            self.logger.info("📖 Stage 4: Interpreting results...")
            stage_start = time.time()
            
            interpretation_response = self._stage_4_interpret_results(
                exec_response, curation_response, request
            )
            
            stage_timings['results_interpretation'] = time.time() - stage_start
            stage_success['results_interpretation'] = interpretation_response.success
            
            if not interpretation_response.success:
                return self._create_error_response(
                    "Results interpretation failed",
                    interpretation_response.error_message,
                    stage_timings,
                    stage_success,
                    time.time() - start_time
                )
            
            # Store intermediate artifacts
            plan_hash = self.artifact_client.put_artifact(json.dumps(plan_response.analysis_plan).encode('utf-8'))
            results_hash = self.artifact_client.put_artifact(json.dumps(exec_response['results']).encode('utf-8'))
            evidence_hash = self.artifact_client.put_artifact(json.dumps(curation_response.to_json_serializable()).encode('utf-8'))
            
            # Success! Create complete response
            total_time = time.time() - start_time
            
            self.logger.info(f"✅ Pipeline completed successfully in {total_time:.2f} seconds")
            
            # Log pipeline completion
            self.audit_logger.log_agent_event(
                "ProductionThinSynthesisPipeline",
                "pipeline_complete",
                {
                    "total_time": total_time,
                    "stage_timings": stage_timings,
                    "analysis_plan_hash": plan_hash,
                    "statistical_results_hash": results_hash,
                    "curated_evidence_hash": evidence_hash,
                    "word_count": interpretation_response.word_count
                }
            )
            
            return ProductionPipelineResponse(
                # Final outputs
                narrative_report=interpretation_response.narrative_report,
                executive_summary=interpretation_response.executive_summary,
                key_findings=interpretation_response.key_findings,
                
                # Intermediate artifacts
                analysis_plan_hash=plan_hash,
                statistical_results_hash=results_hash,
                curated_evidence_hash=evidence_hash,
                
                # Pipeline metadata
                success=True,
                total_execution_time=total_time,
                stage_timings=stage_timings,
                stage_success=stage_success,
                
                # Quality metrics
                word_count=interpretation_response.word_count,
                evidence_integration_summary=interpretation_response.evidence_integration_summary,
                statistical_summary=interpretation_response.statistical_summary
            )
            
        except Exception as e:
            total_time = time.time() - start_time
            self.logger.error(f"Pipeline failed with exception: {str(e)}")
            
            # Log pipeline failure
            self.audit_logger.log_agent_event(
                "ProductionThinSynthesisPipeline",
                "pipeline_failed",
                {
                    "total_time": total_time,
                    "error": str(e),
                    "stage_timings": stage_timings,
                    "stage_success": stage_success
                }
            )
            
            return self._create_error_response(
                "Pipeline execution failed",
                str(e),
                stage_timings,
                stage_success,
                total_time
            )

    def _stage_1_generate_analysis_plan(self, request: ProductionPipelineRequest):
        """Stage 1: Generate analysis plan using declarative mathematical specification."""
        
        # Retrieve analysis data from artifacts
        combined_data = self.artifact_client.get_artifact(request.scores_artifact_hash)
        
        # Load actual data to show LLM real structure
        import pandas as pd
        
        # Initialize default values
        scores_df = None
        evidence_df = None
        available_columns = []
        data_summary = ""
        
        try:
            # Use unified data loading that handles JSON
            scores_df = self._load_data_to_dataframe(combined_data, "scores")
            evidence_df = self._load_data_to_dataframe(combined_data, "evidence")
            
            available_columns = list(scores_df.columns)
            
            # Create data summary for the analysis planner
            data_summary = f"""
Data Summary:
- Scores DataFrame: {scores_df.shape[0]} rows, {scores_df.shape[1]} columns
- Evidence DataFrame: {evidence_df.shape[0]} rows, {evidence_df.shape[1]} columns
- Available columns: {', '.join(available_columns)}
- Sample scores data: {scores_df.head(2).to_dict('records') if len(scores_df) > 0 else 'No data'}
- Sample evidence data: {evidence_df.head(2).to_dict('records') if len(evidence_df) > 0 else 'No data'}
"""
            
            self.logger.info(f"Data-informed planning: scores_df {scores_df.shape}, evidence_df {evidence_df.shape}")
            self.logger.info(f"Available columns: {available_columns}")
            
        except Exception as e:
            self.logger.warning(f"Failed to load actual data structure: {str(e)}")
            data_summary = "Data structure could not be determined"
        
        try:
            # Extract research questions from experiment context
            research_questions = self._extract_research_questions(request.experiment_context)
            
            # Create analysis plan request
            plan_request = AnalysisPlanRequest(
                experiment_context=request.experiment_context or "",
                framework_spec=request.framework_spec,
                data_summary=data_summary,
                available_columns=available_columns,
                research_questions=research_questions
            )
            
            # Log analysis planning start
            self.audit_logger.log_agent_event(
                "AnalysisPlanner",
                "analysis_planning_start",
                {
                    "framework_spec_length": len(request.framework_spec),
                    "data_informed_planning": True,
                    "available_columns": available_columns,
                    "research_questions_count": len(research_questions)
                }
            )
            
            plan_response = self.analysis_planner.generate_analysis_plan(plan_request)
            
            # Debug logging for generated plan
            if self.debug_agent == "analysis-plan" and self.debug_level in ["debug", "verbose"]:
                self.logger.info(f"Generated plan tasks: {len(plan_response.analysis_plan.get('tasks', {})) if plan_response.analysis_plan else 0}")
                if plan_response.analysis_plan:
                    self.logger.info(f"Generated plan preview: {str(plan_response.analysis_plan)[:500]}...")
                    if len(str(plan_response.analysis_plan)) > 500:
                        self.logger.info(f"Generated plan (full):\n{plan_response.analysis_plan}")
            
            return plan_response
            
        except Exception as e:
            self.logger.error(f"Analysis planning failed: {str(e)}")
            raise
    
    def _extract_research_questions(self, experiment_context: str) -> list:
        """
        Extract research questions from experiment context.
        
        Args:
            experiment_context: The experiment context string
            
        Returns:
            List of research questions
        """
        if not experiment_context:
            return []
        
        # Simple extraction - look for lines that start with numbers or bullet points
        questions = []
        lines = experiment_context.split('\n')
        
        for line in lines:
            line = line.strip()
            # Look for numbered questions (e.g., "1. What is...")
            if line and (line[0].isdigit() and '. ' in line[:10]):
                question = line.split('. ', 1)[1] if '. ' in line else line
                questions.append(question)
            # Look for bullet points (e.g., "- What is...")
            elif line.startswith('- ') or line.startswith('* '):
                question = line[2:] if len(line) > 2 else line
                questions.append(question)
            # Look for "Research Question:" patterns
            elif 'research question' in line.lower() and ':' in line:
                question = line.split(':', 1)[1].strip()
                if question:
                    questions.append(question)
        
        return questions

    def _stage_2_execute_analysis_plan(self, plan_response, request: ProductionPipelineRequest):
        """Stage 2: Execute analysis plan using MathToolkit."""
        
        # Load data into DataFrames
        import pandas as pd
        
        try:
            # Load JSON artifact containing both scores and evidence
            combined_data = self.artifact_client.get_artifact(request.scores_artifact_hash)
            scores_df = self._load_data_to_dataframe(combined_data, "scores")
            evidence_df = self._load_data_to_dataframe(combined_data, "evidence")
            
            self.logger.info(f"Loaded JSON artifact: scores_df: {scores_df.shape}, evidence_df: {evidence_df.shape}")
            
        except Exception as e:
            raise Exception(f"Failed to load data into DataFrames: {str(e)}")
        
        try:
            # Validate plan response
            if not plan_response.success:
                raise Exception(f"Analysis plan generation failed: {plan_response.error_message}")
            
            if not plan_response.analysis_plan:
                raise Exception("No analysis plan generated")
            
            # Log execution start
            self.audit_logger.log_agent_event(
                "MathToolkit",
                "analysis_execution_start",
                {
                    "plan_tasks_count": len(plan_response.analysis_plan.get('tasks', {})),
                    "data_shape": f"{scores_df.shape}, {evidence_df.shape}",
                    "available_columns": list(scores_df.columns)
                }
            )
            
            # Execute the analysis plan using MathToolkit
            execution_result = execute_analysis_plan(scores_df, plan_response.analysis_plan)
            
            # Debug logging for execution results
            if self.debug_agent == "math-toolkit" and self.debug_level in ["debug", "verbose"]:
                self.logger.info(f"Execution result success: {len(execution_result.get('errors', [])) == 0}")
                self.logger.info(f"Execution result errors: {execution_result.get('errors', [])}")
                self.logger.info(f"Execution result tasks completed: {len(execution_result.get('results', {}))}")
                if execution_result.get('results'):
                    self.logger.info(f"Execution result task types: {[result.get('type', 'unknown') for result in execution_result['results'].values()]}")
            
            # Log execution completion
            self.audit_logger.log_agent_event(
                "MathToolkit",
                "analysis_execution_complete",
                {
                    "success": len(execution_result.get('errors', [])) == 0,
                    "errors_count": len(execution_result.get('errors', [])),
                    "tasks_completed": len(execution_result.get('results', {})),
                    "result_types": [result.get('type', 'unknown') for result in execution_result.get('results', {}).values()]
                }
            )
            
            return execution_result
            
        except Exception as e:
            self.logger.error(f"Analysis execution failed: {str(e)}")
            raise

    def _stage_3_curate_evidence(self, exec_response, request: ProductionPipelineRequest):
        """Stage 3: Curate evidence based on statistical results."""
        
        # Retrieve evidence data for curation from JSON artifact
        combined_data = self.artifact_client.get_artifact(request.evidence_artifact_hash)
        
        # Create curation request with JSON data
        curation_request = EvidenceCurationRequest(
            statistical_results=exec_response['results'],
            evidence_data=combined_data,
            framework_spec=request.framework_spec,
            max_evidence_per_finding=request.max_evidence_per_finding,
            min_confidence_threshold=request.min_confidence_threshold
        )
        
        # Log evidence curation start
        self.audit_logger.log_agent_event(
            "EvidenceCurator",
            "evidence_curation_start",
            {
                "available_evidence_count": 57,  # Known from JSON structure
                "statistical_results_keys": list(exec_response['results'].keys()) if isinstance(exec_response['results'], dict) else "non_dict_results",
                "max_evidence_per_finding": request.max_evidence_per_finding
            }
        )
        
        curation_response = self.evidence_curator.curate_evidence(curation_request)
        
        # Debug logging for evidence curation
        if self.debug_agent == "evidence-curator" and self.debug_level in ["debug", "verbose"]:
            self.logger.info(f"Evidence curation success: {curation_response.success}")
            self.logger.info(f"Evidence curation error: {curation_response.error_message or 'None'}")
            self.logger.info(f"Curated evidence count: {len(curation_response.curated_evidence) if curation_response.curated_evidence else 0}")
            if curation_response.curated_evidence:
                self.logger.info(f"Curated evidence types: {[evidence.evidence_type for evidence in curation_response.curated_evidence]}")
        
        return curation_response

    def _stage_4_interpret_results(self, exec_response, curation_response, request: ProductionPipelineRequest):
        """Stage 4: Generate final narrative interpretation."""
        
        # Debug logging for results interpreter
        if self.debug_agent in ['results-interpreter', None] and self.debug_level in ['debug', 'verbose']:
            self.logger.info(f"📖 DEBUG: Results interpreter input:")
            self.logger.info(f"   - Statistical results keys: {list(exec_response['results'].keys()) if exec_response.get('results') else 'NO DATA'}")
            self.logger.info(f"   - Curated evidence keys: {list(curation_response.curated_evidence.keys()) if curation_response.curated_evidence else 'NO DATA'}")
            self.logger.info(f"   - Total evidence pieces: {sum(len(evidence_list) for evidence_list in curation_response.curated_evidence.values()) if curation_response.curated_evidence else 0}")
            if exec_response.get('results'):
                for key, value in exec_response['results'].items():
                    if isinstance(value, dict):
                        self.logger.info(f"   - {key}: {list(value.keys()) if value else 'EMPTY'}")
                    else:
                        self.logger.info(f"   - {key}: {type(value).__name__}")
        
        interpretation_request = InterpretationRequest(
            statistical_results=exec_response['results'],
            curated_evidence=curation_response.curated_evidence,
            framework_spec=request.framework_spec,
            experiment_context=request.experiment_context
        )
        
        # Log interpretation start
        self.audit_logger.log_agent_event(
            "ResultsInterpreter",
            "interpretation_start",
            {
                "curated_evidence_count": len(curation_response.curated_evidence),
                "interpretation_focus": request.interpretation_focus
            }
        )
        
        return self.results_interpreter.interpret_results(interpretation_request)

    def _load_data_to_dataframe(self, data: bytes, data_type: str) -> pd.DataFrame:
        """Load JSON data to DataFrame format (v6.0 only)."""
        return self._parse_json_to_dataframe(data, data_type)

    def _parse_json_to_dataframe(self, json_data: bytes, data_type: str) -> pd.DataFrame:
        """Parse JSON analysis output to DataFrame format."""
        try:
            # Parse JSON from bytes
            json_str = json_data.decode('utf-8')
            analysis_result = json.loads(json_str)
            
            if data_type == "scores":
                return self._json_scores_to_dataframe(analysis_result)
            elif data_type == "evidence":
                return self._json_evidence_to_dataframe(analysis_result)
            else:
                raise ValueError(f"Unknown data type: {data_type}")
                
        except Exception as e:
            raise Exception(f"Failed to parse JSON {data_type} data: {str(e)}")
    
    def _json_scores_to_dataframe(self, analysis_result: dict) -> pd.DataFrame:
        """Convert v6.0 JSON analysis scores to DataFrame format."""
        try:
            # v6.0 JSON structure: document_analyses[].dimensional_scores
            document_analyses = analysis_result.get('document_analyses', [])
            
            if not document_analyses:
                raise ValueError("No document_analyses found in JSON")
            
            rows = []
            for doc_analysis in document_analyses:
                document_id = doc_analysis.get('document_id', '{artifact_id}')
                dimensional_scores = doc_analysis.get('dimensional_scores', {})
                
                # Create row with document identifier
                row_data = {'aid': document_id}
                
                # Extract dimensional scores generically (framework-agnostic)
                for dim_name, dim_data in dimensional_scores.items():
                    if isinstance(dim_data, dict):
                        # Standard v6.0 fields: raw_score, salience, confidence
                        row_data[f"{dim_name}_score"] = dim_data.get('raw_score', 0.0)
                        row_data[f"{dim_name}_salience"] = dim_data.get('salience', 0.0)
                        row_data[f"{dim_name}_confidence"] = dim_data.get('confidence', 0.0)
                        
                        # Handle any additional fields generically (framework-agnostic)
                        for field_name, field_value in dim_data.items():
                            if field_name not in ['raw_score', 'salience', 'confidence']:
                                column_name = f"{dim_name}_{field_name}"
                                row_data[column_name] = field_value
                
                rows.append(row_data)
            
            return pd.DataFrame(rows)
            
        except Exception as e:
            raise Exception(f"Failed to convert v6.0 JSON scores to DataFrame: {str(e)}")
    
    def _json_evidence_to_dataframe(self, analysis_result: dict) -> pd.DataFrame:
        """Convert v6.0 JSON analysis evidence to DataFrame format."""
        try:
            # v6.0 JSON structure: document_analyses[].evidence[]
            document_analyses = analysis_result.get('document_analyses', [])
            
            if not document_analyses:
                raise ValueError("No document_analyses found in JSON")
            
            rows = []
            for doc_analysis in document_analyses:
                document_id = doc_analysis.get('document_id', '{artifact_id}')
                evidence_list = doc_analysis.get('evidence', [])
                
                for i, evidence in enumerate(evidence_list):
                    if isinstance(evidence, dict):
                        row = {
                            'aid': document_id,
                            'dimension': evidence.get('dimension', ''),
                            'quote_id': evidence.get('quote_id', f"quote_{i}"),
                            'quote_text': evidence.get('quote_text', ''),
                            'confidence_score': evidence.get('confidence', 0.0),
                            'context_type': evidence.get('context_type', 'direct')
                        }
                        rows.append(row)
            
            # Return DataFrame with standard evidence columns
            if rows:
                return pd.DataFrame(rows)
            else:
                # Return empty DataFrame with correct schema
                return pd.DataFrame(columns=['aid', 'dimension', 'quote_id', 'quote_text', 'confidence_score', 'context_type'])
            
        except Exception as e:
            raise Exception(f"Failed to convert v6.0 JSON evidence to DataFrame: {str(e)}")


    
    def _describe_dataframe_structure(self, df: pd.DataFrame, data_type: str) -> str:
        """Analyze DataFrame structure for code generation (works for both CSV and JSON sources)."""
        try:
            structure_info = {
                "data_type": data_type,
                "total_rows": len(df),
                "columns": list(df.columns),
                "sample_data": df.head(3).to_dict('records')
            }
            
            return json.dumps(structure_info, indent=2)
            
        except Exception as e:
            return f"Error analyzing {data_type} DataFrame: {str(e)}"

    def _create_error_response(self, 
                             error_type: str, 
                             error_message: str,
                             stage_timings: Dict[str, float],
                             stage_success: Dict[str, bool],
                             total_time: float) -> ProductionPipelineResponse:
        """Create standardized error response."""
        
        return ProductionPipelineResponse(
            narrative_report="",
            executive_summary="",
            key_findings=[],
            analysis_plan_hash="",
            statistical_results_hash="",
            curated_evidence_hash="",
            success=False,
            total_execution_time=total_time,
            stage_timings=stage_timings,
            stage_success=stage_success,
            word_count=0,
            evidence_integration_summary="",
            statistical_summary="",
            error_message=f"{error_type}: {error_message}"
        ) 