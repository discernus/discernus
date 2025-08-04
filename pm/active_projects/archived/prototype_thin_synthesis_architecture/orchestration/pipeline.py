#!/usr/bin/env python3
"""
THIN Code-Generated Synthesis Pipeline

This orchestrates the 4-agent architecture that solves the fundamental 
scalability limitations of monolithic LLM synthesis:

1. AnalyticalCodeGenerator: LLM generates Python analysis code
2. CodeExecutor: Executes code deterministically 
3. EvidenceCurator: LLM selects evidence based on actual results
4. ResultsInterpreter: LLM synthesizes final narrative

Key Innovation: Evidence curation happens AFTER statistical computation,
enabling intelligent, data-driven evidence selection.
"""

import logging
import json
import time
from typing import Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime

# Import all the agents
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from agents.analytical_code_generator import AnalyticalCodeGenerator
from agents.analytical_code_generator.agent import CodeGenerationRequest
from agents.code_executor import CodeExecutor
from agents.code_executor.executor import CodeExecutionRequest
from agents.evidence_curator import EvidenceCurator
from agents.evidence_curator.agent import EvidenceCurationRequest
from agents.results_interpreter import ResultsInterpreter
from agents.results_interpreter.agent import InterpretationRequest

@dataclass
class PipelineRequest:
    """Request structure for the complete pipeline."""
    framework_spec: str
    scores_csv_path: str
    evidence_csv_path: str
    experiment_context: Optional[str] = None
    max_evidence_per_finding: int = 3
    min_confidence_threshold: float = 0.7
    interpretation_focus: str = "comprehensive"

@dataclass
class PipelineResponse:
    """Response structure containing complete synthesis results."""
    # Final outputs
    narrative_report: str
    executive_summary: str
    key_findings: list
    
    # Intermediate results for debugging/analysis
    generated_code: str
    statistical_results: Dict[str, Any]
    curated_evidence: Dict[str, Any]
    
    # Pipeline metadata
    success: bool
    total_execution_time: float
    stage_timings: Dict[str, float]
    stage_success: Dict[str, bool]
    
    # Quality metrics
    word_count: int
    evidence_integration_summary: Dict[str, Any]
    statistical_summary: Dict[str, Any]
    
    # Optional error message (must be last due to default value)
    error_message: Optional[str] = None

class ThinSynthesisPipeline:
    """
    Orchestrates the 4-agent THIN Code-Generated Synthesis Architecture.
    
    This pipeline represents a breakthrough in synthesis scalability by:
    1. Using LLMs for intelligence (code generation, evidence curation, interpretation)
    2. Using deterministic software for computation (statistical analysis)
    3. Enabling post-computation evidence curation based on actual results
    4. Avoiding token limits through focused, sequential processing
    """
    
    def __init__(self, 
                 code_model: str = "vertex_ai/gemini-2.5-flash",
                 interpretation_model: str = "vertex_ai/gemini-2.5-pro"):
        """
        Initialize the pipeline with the 4 agents.
        
        Args:
            code_model: Model for code generation and evidence curation
            interpretation_model: Model for final interpretation (Pro for quality)
        """
        self.code_generator = AnalyticalCodeGenerator(model=code_model)
        self.code_executor = CodeExecutor()
        self.evidence_curator = EvidenceCurator(model=code_model)
        self.results_interpreter = ResultsInterpreter(model=interpretation_model)
        
        self.logger = logging.getLogger(__name__)
        
    def run(self, request: PipelineRequest) -> PipelineResponse:
        """
        Execute the complete 4-agent synthesis pipeline.
        
        Args:
            request: PipelineRequest with framework and data specifications
            
        Returns:
            PipelineResponse with complete synthesis results
        """
        start_time = time.time()
        stage_timings = {}
        stage_success = {}
        
        try:
            self.logger.info("🚀 Starting THIN Code-Generated Synthesis Pipeline")
            
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
            stage_success['code_execution'] = exec_response.success
            
            if not exec_response.success:
                return self._create_error_response(
                    "Code execution failed",
                    exec_response.error_message,
                    stage_timings,
                    stage_success,
                    time.time() - start_time,
                    generated_code=code_response.analysis_code
                )
            
            # Stage 3: Curate Evidence (KEY INNOVATION: Post-computation)
            self.logger.info("🎯 Stage 3: Curating evidence based on statistical results...")
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
                    time.time() - start_time,
                    generated_code=code_response.analysis_code,
                    statistical_results=exec_response.results
                )
            
            # Stage 4: Generate Final Narrative
            self.logger.info("📖 Stage 4: Generating final narrative synthesis...")
            stage_start = time.time()
            
            interpretation_response = self._stage_4_interpret_results(
                exec_response, curation_response, request
            )
            
            stage_timings['narrative_synthesis'] = time.time() - stage_start
            stage_success['narrative_synthesis'] = interpretation_response.success
            
            if not interpretation_response.success:
                return self._create_error_response(
                    "Narrative synthesis failed",
                    interpretation_response.error_message,
                    stage_timings,
                    stage_success,
                    time.time() - start_time,
                    generated_code=code_response.analysis_code,
                    statistical_results=exec_response.results,
                    curated_evidence=curation_response.curated_evidence
                )
            
            # Success! Create complete response
            total_time = time.time() - start_time
            
            self.logger.info(f"✅ Pipeline completed successfully in {total_time:.2f} seconds")
            
            return PipelineResponse(
                # Final outputs
                narrative_report=interpretation_response.narrative_report,
                executive_summary=interpretation_response.executive_summary,
                key_findings=interpretation_response.key_findings,
                
                # Intermediate results
                generated_code=code_response.analysis_code,
                statistical_results=exec_response.results,
                curated_evidence=curation_response.curated_evidence,
                
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
            
            return self._create_error_response(
                "Pipeline execution failed",
                str(e),
                stage_timings,
                stage_success,
                total_time
            )
    
    def _stage_1_generate_code(self, request: PipelineRequest):
        """Stage 1: Generate analysis code using AnalyticalCodeGenerator."""
        
        # Prepare data structure descriptions
        scores_structure = self._describe_csv_structure(request.scores_csv_path, "scores")
        evidence_structure = self._describe_csv_structure(request.evidence_csv_path, "evidence")
        
        # Create code generation request
        code_request = CodeGenerationRequest(
            framework_spec=request.framework_spec,
            scores_csv_structure=scores_structure,
            evidence_csv_structure=evidence_structure,
            experiment_context=request.experiment_context
        )
        
        # Generate the code
        return self.code_generator.generate_analysis_code(code_request)
    
    def _stage_2_execute_code(self, code_response, request: PipelineRequest):
        """Stage 2: Execute generated code using CodeExecutor."""
        
        # Create execution request
        exec_request = CodeExecutionRequest(
            analysis_code=code_response.analysis_code,
            scores_csv_path=request.scores_csv_path,
            evidence_csv_path=request.evidence_csv_path,
            timeout_seconds=300
        )
        
        # Execute the code
        return self.code_executor.execute_code(exec_request)
    
    def _stage_3_curate_evidence(self, exec_response, request: PipelineRequest):
        """Stage 3: Curate evidence using EvidenceCurator (KEY INNOVATION)."""
        
        # Create curation request with ACTUAL statistical results
        curation_request = EvidenceCurationRequest(
            statistical_results=exec_response.results,
            evidence_csv_path=request.evidence_csv_path,
            framework_spec=request.framework_spec,
            max_evidence_per_finding=request.max_evidence_per_finding,
            min_confidence_threshold=request.min_confidence_threshold
        )
        
        # Curate evidence based on statistical findings
        return self.evidence_curator.curate_evidence(curation_request)
    
    def _stage_4_interpret_results(self, exec_response, curation_response, request: PipelineRequest):
        """Stage 4: Generate final narrative using ResultsInterpreter."""
        
        # Create interpretation request
        interpretation_request = InterpretationRequest(
            statistical_results=exec_response.results,
            curated_evidence=curation_response.curated_evidence,
            framework_spec=request.framework_spec,
            experiment_context=request.experiment_context,
            interpretation_focus=request.interpretation_focus
        )
        
        # Generate final narrative
        return self.results_interpreter.interpret_results(interpretation_request)
    
    def _describe_csv_structure(self, csv_path: str, csv_type: str) -> str:
        """Generate a description of CSV structure for the code generator."""
        
        try:
            import pandas as pd
            df = pd.read_csv(csv_path)
            
            description = f"{csv_type.upper()} CSV STRUCTURE:\n\n"
            description += f"Columns ({len(df.columns)}):\n"
            
            for col in df.columns:
                dtype = str(df[col].dtype)
                sample_val = df[col].iloc[0] if len(df) > 0 else "N/A"
                description += f"- {col}: {dtype} (sample: {sample_val})\n"
            
            description += f"\nRows: {len(df)}\n"
            description += f"Missing values: {df.isnull().sum().sum()}\n"
            
            return description
            
        except Exception as e:
            self.logger.warning(f"Could not describe {csv_type} CSV structure: {str(e)}")
            return f"{csv_type.upper()} CSV: Structure could not be determined"
    
    def _create_error_response(self, error_type: str, error_message: str,
                             stage_timings: Dict[str, float], 
                             stage_success: Dict[str, bool],
                             total_time: float,
                             generated_code: str = "",
                             statistical_results: Dict[str, Any] = None,
                             curated_evidence: Dict[str, Any] = None) -> PipelineResponse:
        """Create an error response with available partial results."""
        
        return PipelineResponse(
            # Final outputs (empty on error)
            narrative_report="",
            executive_summary="",
            key_findings=[],
            
            # Intermediate results (may be partial)
            generated_code=generated_code,
            statistical_results=statistical_results or {},
            curated_evidence=curated_evidence or {},
            
            # Pipeline metadata
            success=False,
            total_execution_time=total_time,
            stage_timings=stage_timings,
            stage_success=stage_success,
            error_message=f"{error_type}: {error_message}",
            
            # Quality metrics (empty on error)
            word_count=0,
            evidence_integration_summary={},
            statistical_summary={}
        )
    
    def run_quick_summary(self, request: PipelineRequest) -> str:
        """
        Run pipeline and return just the executive summary for quick insights.
        
        This is useful for rapid iteration and testing.
        """
        
        try:
            # Run stages 1-3 to get statistical results and evidence
            code_response = self._stage_1_generate_code(request)
            if not code_response.success:
                return f"Quick summary failed: {code_response.error_message}"
            
            exec_response = self._stage_2_execute_code(code_response, request)
            if not exec_response.success:
                return f"Quick summary failed: {exec_response.error_message}"
            
            curation_response = self._stage_3_curate_evidence(exec_response, request)
            if not curation_response.success:
                return f"Quick summary failed: {curation_response.error_message}"
            
            # Generate just executive summary
            interpretation_request = InterpretationRequest(
                statistical_results=exec_response.results,
                curated_evidence=curation_response.curated_evidence,
                framework_spec=request.framework_spec,
                experiment_context=request.experiment_context
            )
            
            return self.results_interpreter.generate_executive_summary_only(interpretation_request)
            
        except Exception as e:
            return f"Quick summary failed: {str(e)}"
    
    def get_pipeline_status(self) -> Dict[str, Any]:
        """Get status information about the pipeline components."""
        
        return {
            'pipeline_name': 'THIN Code-Generated Synthesis Architecture',
            'version': '1.0.0-prototype',
            'components': {
                'analytical_code_generator': {
                    'model': self.code_generator.model,
                    'status': 'ready'
                },
                'code_executor': {
                    'max_memory_mb': self.code_executor.max_memory_mb,
                    'status': 'ready'
                },
                'evidence_curator': {
                    'model': self.evidence_curator.model,
                    'status': 'ready'
                },
                'results_interpreter': {
                    'model': self.results_interpreter.model,
                    'status': 'ready'
                }
            },
            'key_innovation': 'post_computation_evidence_curation',
            'architecture_type': 'THIN (Thick LLM + Thin Software)',
            'scalability_approach': 'sequential_focused_processing'
        } 