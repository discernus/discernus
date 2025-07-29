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
import tempfile
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
from discernus.core.secure_code_executor import SecureCodeExecutor
from discernus.core.audit_logger import AuditLogger

# Import THIN synthesis agents
from ..analytical_code_generator.agent import AnalyticalCodeGenerator, CodeGenerationRequest
from ..evidence_curator.agent import EvidenceCurator, EvidenceCurationRequest
from ..results_interpreter.agent import ResultsInterpreter, InterpretationRequest

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

@dataclass
class ProductionPipelineResponse:
    """Complete pipeline response with all outputs and metadata."""
    # Final outputs
    narrative_report: str
    executive_summary: str
    key_findings: list
    
    # Intermediate artifacts (as hashes for provenance)
    generated_code_hash: str
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
                 model: str = "vertex_ai/gemini-2.5-pro"):
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
        
        # Initialize agents with infrastructure
        self.code_generator = AnalyticalCodeGenerator(model=model)
        self.secure_executor = SecureCodeExecutor(
            timeout_seconds=60,
            memory_limit_mb=512,
            enable_data_science=True
        )
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
                "secure_executor_config": {
                    "timeout_seconds": 60,
                    "memory_limit_mb": 512,
                    "data_science_enabled": True
                }
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
                "experiment_context": request.experiment_context
            }
        )
        
        try:
            self.logger.info("🚀 Starting Production THIN Synthesis Pipeline")
            
            # Stage 1: Generate Analysis Code
            self.logger.info("📝 Stage 1: Generating analysis code...")
            stage_start = time.time()
            
            code_response = self._stage_1_generate_code(request)
            
            stage_timings['code_generation'] = time.time() - stage_start
            stage_success['code_generation'] = code_response.success
            
            if not code_response.success:
                return self._create_error_response(
                    "Code generation failed", 
                    code_response.error_message,
                    stage_timings, 
                    stage_success,
                    time.time() - start_time
                )
            
            # Stage 2: Execute Generated Code
            self.logger.info("⚙️  Stage 2: Executing generated code...")
            stage_start = time.time()
            
            exec_response = self._stage_2_execute_code(code_response, request)
            
            stage_timings['code_execution'] = time.time() - stage_start
            stage_success['code_execution'] = exec_response['success']
            
            if not exec_response['success']:
                return self._create_error_response(
                    "Code execution failed",
                    exec_response['error'],
                    stage_timings,
                    stage_success,
                    time.time() - start_time
                )
            
            # Stage 3: Curate Evidence
            self.logger.info("🔍 Stage 3: Curating evidence...")
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
            code_hash = self.artifact_client.put_artifact(code_response.analysis_code.encode('utf-8'))
            results_hash = self.artifact_client.put_artifact(json.dumps(exec_response['result_data']).encode('utf-8'))
            evidence_hash = self.artifact_client.put_artifact(json.dumps(curation_response.curated_evidence).encode('utf-8'))
            
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
                    "generated_code_hash": code_hash,
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
                generated_code_hash=code_hash,
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

    def _stage_1_generate_code(self, request: ProductionPipelineRequest):
        """Stage 1: Generate analysis code using artifacts with actual data structure."""
        
        # Retrieve CSV data from artifacts to analyze structure
        scores_data = self.artifact_client.get_artifact(request.scores_artifact_hash)
        evidence_data = self.artifact_client.get_artifact(request.evidence_artifact_hash)
        
        # Load actual data to show LLM real structure
        import io
        import pandas as pd
        
        try:
            # Load actual DataFrames to understand real structure
            scores_df = pd.read_csv(
                io.BytesIO(scores_data),
                on_bad_lines='skip',
                engine='python', 
                quoting=3
            )
            evidence_df = pd.read_csv(
                io.BytesIO(evidence_data),
                on_bad_lines='skip',
                engine='python',
                quoting=3  
            )
            
            # Create samples for LLM to understand actual structure
            scores_sample = scores_df.head(3).to_dict('records') if len(scores_df) > 0 else []
            evidence_sample = evidence_df.head(5).to_dict('records') if len(evidence_df) > 0 else []
            available_columns = list(scores_df.columns)
            
            self.logger.info(f"Data-informed generation: scores_df {scores_df.shape}, evidence_df {evidence_df.shape}")
            self.logger.info(f"Available columns: {available_columns}")
            
        except Exception as e:
            self.logger.warning(f"Failed to load actual data structure: {str(e)}")
            scores_sample = []
            evidence_sample = []
            available_columns = []
        
        # Write to temporary files for legacy structure analysis
        with tempfile.NamedTemporaryFile(mode='wb', suffix='.csv', delete=False) as scores_temp:
            scores_temp.write(scores_data)
            scores_temp_path = scores_temp.name
            
        with tempfile.NamedTemporaryFile(mode='wb', suffix='.csv', delete=False) as evidence_temp:
            evidence_temp.write(evidence_data)
            evidence_temp_path = evidence_temp.name
        
        try:
            # Analyze CSV structures
            scores_structure = self._describe_csv_structure(scores_temp_path, "scores")
            evidence_structure = self._describe_csv_structure(evidence_temp_path, "evidence")
            
            # Create enhanced code generation request with actual data structure
            code_request = CodeGenerationRequest(
                framework_spec=request.framework_spec,
                scores_csv_structure=scores_structure,
                evidence_csv_structure=evidence_structure,
                experiment_context=request.experiment_context,
                actual_scores_sample=scores_sample,
                actual_evidence_sample=evidence_sample,
                available_columns=available_columns
            )
            
            # Log code generation start
            self.audit_logger.log_agent_event(
                "AnalyticalCodeGenerator",
                "code_generation_start",
                {
                    "framework_spec_length": len(request.framework_spec),
                    "scores_structure": scores_structure,
                    "evidence_structure": evidence_structure,
                    "data_informed_generation": True,
                    "available_columns": available_columns,
                    "scores_sample_size": len(scores_sample),
                    "evidence_sample_size": len(evidence_sample)
                }
            )
            
            return self.code_generator.generate_analysis_code(code_request)
            
        finally:
            # Clean up temporary files
            os.unlink(scores_temp_path)
            os.unlink(evidence_temp_path)

    def _stage_2_execute_code(self, code_response, request: ProductionPipelineRequest):
        """Stage 2: Execute generated code using SecureCodeExecutor with enhanced data injection."""
        
        # Retrieve CSV data from artifacts
        scores_data = self.artifact_client.get_artifact(request.scores_artifact_hash)
        evidence_data = self.artifact_client.get_artifact(request.evidence_artifact_hash)
        
        # Load CSV data directly into DataFrames (eliminates file system access)
        import io
        import pandas as pd
        
        try:
            # Use robust CSV parsing with error handling for malformed data
            scores_df = pd.read_csv(
                io.BytesIO(scores_data), 
                on_bad_lines='skip',  # Skip malformed lines instead of failing
                engine='python',      # More permissive parser
                quoting=3             # Handle quotes properly
            )
            evidence_df = pd.read_csv(
                io.BytesIO(evidence_data),
                on_bad_lines='skip',
                engine='python',
                quoting=3
            )
            
            # Log data shapes for debugging
            self.logger.info(f"Loaded scores_df: {scores_df.shape}, evidence_df: {evidence_df.shape}")
            
        except Exception as e:
            raise Exception(f"Failed to load CSV data into DataFrames: {str(e)}")
        
        # Prepare context with DataFrames instead of file paths
        context = {
            'scores_df': scores_df,
            'evidence_df': evidence_df,
            'pd': pd,  # Ensure pandas is available
            'np': __import__('numpy'),  # Ensure numpy is available
        }
        
        # Generate execution code without file operations
        execution_code = f"""
# DataFrames pre-loaded by pipeline (no file access needed)
# scores_df and evidence_df are available as variables

# Generated analysis code
{code_response.analysis_code}
"""
        
        # Log code execution start
        self.audit_logger.log_agent_event(
            "SecureCodeExecutor",
            "code_execution_start",
            {
                "code_length": len(execution_code),
                "scores_artifact": request.scores_artifact_hash,
                "evidence_artifact": request.evidence_artifact_hash,
                "scores_shape": scores_df.shape,
                "evidence_shape": evidence_df.shape,
                "enhanced_data_injection": True
            }
        )
        
        # Execute using SecureCodeExecutor with DataFrame context
        execution_result = self.secure_executor.execute_code(execution_code, context=context)
        
        # Log execution completion
        self.audit_logger.log_agent_event(
            "SecureCodeExecutor",
            "code_execution_complete",
            {
                "success": execution_result['success'],
                "execution_time": execution_result['execution_time'],
                "memory_used": execution_result.get('memory_used', 0),
                "security_violations": execution_result.get('security_violations', [])
            }
        )
        
        return execution_result

    def _stage_3_curate_evidence(self, exec_response, request: ProductionPipelineRequest):
        """Stage 3: Curate evidence based on statistical results."""
        
        # Retrieve evidence data for curation
        evidence_data = self.artifact_client.get_artifact(request.evidence_artifact_hash)
        
        # Parse evidence CSV for curation
        with tempfile.NamedTemporaryFile(mode='wb', suffix='.csv', delete=False) as evidence_temp:
            evidence_temp.write(evidence_data)
            evidence_csv_path = evidence_temp.name
        
        try:
            # Use robust CSV parsing consistent with Stage 2
            evidence_df = pd.read_csv(
                evidence_csv_path,
                on_bad_lines='skip',  # Skip malformed lines
                engine='python',      # More permissive parser
                quoting=3             # Handle quotes properly
            )
            
            # Create curation request
            curation_request = EvidenceCurationRequest(
                statistical_results=exec_response['result_data'],
                evidence_csv_path=evidence_csv_path,
                framework_spec=request.framework_spec,
                max_evidence_per_finding=request.max_evidence_per_finding,
                min_confidence_threshold=request.min_confidence_threshold
            )
            
            # Log evidence curation start
            self.audit_logger.log_agent_event(
                "EvidenceCurator",
                "evidence_curation_start",
                {
                    "available_evidence_count": len(evidence_df),
                    "statistical_results_keys": list(exec_response['result_data'].keys()) if isinstance(exec_response['result_data'], dict) else "non_dict_results",
                    "max_evidence_per_finding": request.max_evidence_per_finding
                }
            )
            
            return self.evidence_curator.curate_evidence(curation_request)
            
        finally:
            os.unlink(evidence_csv_path)

    def _stage_4_interpret_results(self, exec_response, curation_response, request: ProductionPipelineRequest):
        """Stage 4: Generate final narrative interpretation."""
        
        interpretation_request = InterpretationRequest(
            statistical_results=exec_response['result_data'],
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

    def _describe_csv_structure(self, csv_path: str, data_type: str) -> str:
        """Analyze CSV structure for code generation."""
        try:
            # Use robust CSV parsing consistent with pipeline stages
            df = pd.read_csv(
                csv_path,
                on_bad_lines='skip',  # Skip malformed lines
                engine='python',      # More permissive parser
                quoting=3             # Handle quotes properly
            )
            
            structure_info = {
                "data_type": data_type,
                "total_rows": len(df),
                "columns": list(df.columns),
                "sample_data": df.head(3).to_dict('records')
            }
            
            return json.dumps(structure_info, indent=2)
            
        except Exception as e:
            return f"Error analyzing {data_type} CSV: {str(e)}"

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
            generated_code_hash="",
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