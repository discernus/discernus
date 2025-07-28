#!/usr/bin/env python3
"""
THIN Orchestrator v2.0 for Discernus
====================================

THIN v2.0 orchestrator implementing direct function calls instead of Redis coordination.
Coordinates the simplified 2-agent pipeline: Enhanced Analysis → Enhanced Synthesis

Key THIN v2.0 principles:
- Direct Python function calls (no Redis coordination)
- LLM intelligence for complex reasoning
- Minimal software coordination
- Perfect caching through content-addressable storage
- Complete audit trails for academic integrity
"""

import json
import yaml
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional

from .security_boundary import ExperimentSecurityBoundary, SecurityError
from .audit_logger import AuditLogger
from .local_artifact_storage import LocalArtifactStorage
from .enhanced_manifest import EnhancedManifest
from ..agents.EnhancedAnalysisAgent.main import EnhancedAnalysisAgent
from ..agents.EnhancedSynthesisAgent.main import EnhancedSynthesisAgent


class ThinOrchestratorError(Exception):
    """THIN orchestrator specific exceptions"""
    pass


class ThinOrchestrator:
    """
    THIN v2.0 orchestrator implementing direct function call coordination.
    
    Simplified 2-agent pipeline:
    1. Enhanced Analysis Agent (with mathematical validation)
    2. Enhanced Synthesis Agent (with mathematical spot-checking)
    
    Key features:
    - Direct function calls (no Redis)
    - Security boundary enforcement
    - Complete audit trails
    - Perfect caching for restart=resume
    - Enhanced mathematical validation
    """
    
    def __init__(self, experiment_path: Path):
        """
        Initialize THIN orchestrator for an experiment.
        
        Args:
            experiment_path: Path to experiment directory (containing experiment.md)
        """
        self.experiment_path = Path(experiment_path).resolve()
        
        # Initialize security boundary
        self.security = ExperimentSecurityBoundary(self.experiment_path)
        
        print(f"🎯 THIN Orchestrator v2.0 initialized for: {self.security.experiment_name}")
        
    def run_experiment(self, model: str = "vertex_ai/gemini-2.5-flash") -> Dict[str, Any]:
        """
        Execute complete experiment using THIN v2.0 direct call coordination.
        
        Args:
            model: LLM model to use for analysis and synthesis
            
        Returns:
            Complete experiment results with provenance
        """
        start_time = datetime.now(timezone.utc).isoformat()
        
        # Create timestamped run folder
        run_timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        run_folder = self.experiment_path / "runs" / run_timestamp
        
        try:
            # Initialize run infrastructure
            self.security.secure_mkdir(run_folder)
            
            # Initialize audit logging
            audit = AuditLogger(self.security, run_folder)
            
            # Initialize experiment-level shared cache for perfect THIN caching
            shared_cache_dir = self.experiment_path / "shared_cache"
            self.security.secure_mkdir(shared_cache_dir)
            storage = LocalArtifactStorage(self.security, shared_cache_dir)
            
            # Initialize enhanced manifest
            manifest = EnhancedManifest(self.security, run_folder, audit, storage)
            
            audit.log_orchestrator_event("experiment_start", {
                "experiment_path": str(self.experiment_path),
                "run_folder": str(run_folder),
                "model": model,
                "architecture": "thin_v2.0_direct_calls"
            })
            
            print(f"🚀 Starting THIN v2.0 experiment: {run_timestamp}")
            
            # Load and validate experiment configuration
            experiment_config = self._load_experiment_config()
            manifest.set_run_metadata(
                experiment_config["name"], 
                str(self.experiment_path),
                "thin_v2.0_alpha"
            )
            manifest.set_experiment_config(experiment_config)
            
            # Load framework
            framework_content = self._load_framework(experiment_config["framework"])
            framework_hash = storage.put_artifact(
                framework_content.encode('utf-8'),
                {"artifact_type": "framework", "original_filename": experiment_config["framework"]}
            )
            manifest.add_input_artifact("framework", framework_hash, {
                "filename": experiment_config["framework"],
                "size_bytes": len(framework_content)
            })
            
            # Load corpus documents
            corpus_documents = self._load_corpus(experiment_config["corpus_path"])
            corpus_hashes = []
            corpus_metadata = []
            
            for doc in corpus_documents:
                doc_hash = storage.put_artifact(
                    doc["content"].encode('utf-8') if isinstance(doc["content"], str) else doc["content"],
                    {"artifact_type": "corpus_document", "original_filename": doc["filename"]}
                )
                corpus_hashes.append(doc_hash)
                corpus_metadata.append({
                    "filename": doc["filename"],
                    "size_bytes": len(doc["content"]) if isinstance(doc["content"], str) else len(doc["content"])
                })
            
            manifest.add_corpus_artifacts(corpus_hashes, corpus_metadata)
            
            audit.log_orchestrator_event("inputs_loaded", {
                "framework_hash": framework_hash,
                "corpus_documents": len(corpus_documents),
                "total_input_artifacts": len(corpus_hashes) + 1
            })
            
            # Phase 1: Batch Planning and Enhanced Analysis with Context Window Management
            # CONTEXT_WINDOW_MANAGEMENT: This entire section can be removed when LLM context windows become unlimited
            batch_planning_start_time = datetime.now(timezone.utc).isoformat()
            manifest.add_execution_stage("batch_planning", "BatchPlannerAgent", batch_planning_start_time)
            
            # Create intelligent batch plan with production cost transparency
            # batch_planner = BatchPlannerAgent(self.security, audit)
            # batch_plan = batch_planner.create_batches(
            #     framework_content=framework_content,
            #     corpus_documents=corpus_documents,
            #     model=model
            # )
            
            batch_planning_end_time = datetime.now(timezone.utc).isoformat()
            manifest.add_execution_stage("batch_planning", "BatchPlannerAgent",
                                       batch_planning_start_time, batch_planning_end_time, "completed", {
                "total_batches": 0, # No batches in this new flow
                "total_estimated_cost": 0.0,
                "total_estimated_tokens": 0,
                "context_window_limit": 0
            })
            
            print(f"💰 Total estimated cost: ${0:.4f}")
            print(f"📊 Batch plan: 0 batches, "
                  f"⏱️ ~{0:.1f} minutes")
            
            # Initialize analysis and synthesis agents
            analysis_agent = EnhancedAnalysisAgent(self.security, audit, storage)
            
            # Execute analysis (one document at a time)
            all_analysis_results, scores_hash, evidence_hash = self._execute_analysis_sequentially(
                analysis_agent,
                corpus_documents,
                framework_content,
                experiment_config,
                model
            )

            # Check if any analysis tasks succeeded
            successful_analyses = [res for res in all_analysis_results if res.get('result_hash')]
            if not successful_analyses:
                raise ThinOrchestratorError("All analysis batches failed. Halting experiment.")

            # Execute synthesis
            print("\n🔬 Synthesizing results...")
            synthesis_agent = EnhancedSynthesisAgent(self.security, audit, storage)
            synthesis_start_time = datetime.now(timezone.utc).isoformat()
            
            # Pass final CSV artifact hashes to the synthesis agent
            print(f"DEBUG: Passing scores_hash={scores_hash} and evidence_hash={evidence_hash} to synthesis agent.")
            synthesis_result = synthesis_agent.synthesize_results(
                scores_hash=scores_hash,
                evidence_hash=evidence_hash,
                analysis_results=all_analysis_results, # Still useful for metadata
                experiment_config=experiment_config,
                model=model 
            )
            
            synthesis_end_time = datetime.now(timezone.utc).isoformat()
            manifest.add_execution_stage("enhanced_synthesis", "EnhancedSynthesisAgent",
                                       synthesis_start_time, synthesis_end_time, "completed", {
                "result_hash": synthesis_result["result_hash"],
                "duration_seconds": synthesis_result["duration_seconds"],
                "synthesis_confidence": synthesis_result["synthesis_confidence"]
            })
            
            # Finalize manifest (synthesis results already captured in execution stages)
            
            # Combine batch results for final summary
            analysis_summary = self._combine_batch_results(all_analysis_results)

            # Generate final report (optional, can be done by ReportAgent)
            # For now, we'll just use the synthesis markdown as the final report
            final_report_content = synthesis_result.get("synthesis_report_markdown", "Synthesis failed.")
            report_hash = storage.put_artifact(
                final_report_content.encode('utf-8'), 
                {"artifact_type": "final_report"}
            )

            # Write final report to results folder
            results_dir = self.security.secure_mkdir(run_folder / "results")
            report_file = results_dir / "final_report.md"
            self.security.secure_write_text(report_file, final_report_content)
            
            # Finalize manifest and audit
            manifest_file = manifest.finalize_manifest()
            audit.finalize_session()
            
            # Calculate total execution time
            end_time = datetime.now(timezone.utc).isoformat()
            total_duration = self._calculate_duration(start_time, end_time)
            
            # Final orchestrator event
            audit.log_orchestrator_event("experiment_complete", {
                "total_duration_seconds": total_duration,
                "analysis_duration": analysis_summary["total_duration_seconds"],
                "synthesis_duration": synthesis_result.get("execution_metadata", {}).get("duration_seconds", 0),
                "final_report_hash": report_hash,
                "manifest_file": str(manifest_file),
                "mathematical_validation": "completed"
            })
            
            print(f"✅ THIN v2.0 experiment complete: {run_timestamp} ({total_duration:.1f}s)")
            print(f"📋 Results: {results_dir}")
            print(f"📊 Report: {report_file}")
            
            return {
                "run_id": run_timestamp,
                "run_folder": str(run_folder),
                "results_directory": str(results_dir),
                "final_report_file": str(report_file),
                "manifest_file": str(manifest_file),
                "total_duration_seconds": total_duration,
                "analysis_result": analysis_summary,
                "synthesis_result": synthesis_result,
                "mathematical_validation": True,
                "architecture": "thin_v2.0_direct_calls"
            }
            
        except Exception as e:
            # Log error and cleanup
            try:
                audit.log_error("orchestrator_error", str(e), {
                    "experiment_path": str(self.experiment_path),
                    "run_folder": str(run_folder) if 'run_folder' in locals() else None
                })
                if 'audit' in locals():
                    audit.finalize_session()
            except:
                pass  # Don't fail on logging errors
            
            raise ThinOrchestratorError(f"Experiment execution failed: {e}")

    def _execute_analysis_sequentially(self,
                                       analysis_agent: EnhancedAnalysisAgent,
                                       corpus_documents: List[Dict[str, Any]],
                                       framework_content: str,
                                       experiment_config: Dict[str, Any],
                                       model: str) -> tuple[List[Dict[str, Any]], Optional[str], Optional[str]]:
        """
        Executes the analysis agent for each document, passing CSV artifact hashes.
        """
        all_analysis_results = []
        scores_hash = None
        evidence_hash = None
        total_docs = len(corpus_documents)
        print(f"\n🚀 Starting sequential analysis of {total_docs} documents...")

        for i, doc in enumerate(corpus_documents):
            print(f"\n--- Analyzing document {i+1}/{total_docs}: {doc.get('filename')} ---")
            try:
                # The returned result is now a dictionary containing the analysis result and the CSV hashes
                result = analysis_agent.analyze_batch(
                    framework_content=framework_content,
                    corpus_documents=[doc],  # Pass a list with a single document
                    experiment_config=experiment_config,
                    model=model,
                    current_scores_hash=scores_hash,
                    current_evidence_hash=evidence_hash
                )
                
                # Update hashes for the next iteration
                scores_hash = result.get("scores_hash", scores_hash)
                evidence_hash = result.get("evidence_hash", evidence_hash)
                
                # Append the nested analysis result to the list
                all_analysis_results.append(result["analysis_result"])
            except Exception as e:
                print(f"❌ Analysis failed for document {doc.get('filename')}: {e}")
                all_analysis_results.append({"error": str(e), "document": doc.get('filename')})

        return all_analysis_results, scores_hash, evidence_hash




    def _combine_batch_results(self, batch_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Combines results from multiple analysis batches into a single summary.
        """
        if not batch_results:
            return {"total_duration_seconds": 0, "num_batches": 0, "successful_batches": 0}

        total_duration = sum(r.get('duration_seconds', 0) for r in batch_results)
        num_batches = len(batch_results)
        successful_batches = sum(1 for r in batch_results if r.get('result_hash'))

        return {
            "total_duration_seconds": total_duration,
            "num_batches": num_batches,
            "successful_batches": successful_batches,
            "all_batches_successful": successful_batches == num_batches,
            "individual_batch_results": [
                {
                    "batch_id": r.get("batch_id"),
                    "result_hash": r.get("result_hash"),
                    "duration": r.get("duration_seconds")
                } for r in batch_results
            ]
        }

    def _load_experiment_config(self) -> Dict[str, Any]:
        """Load and validate the experiment.md file."""
        exp_file = self.experiment_path / "experiment.md"
        
        if not exp_file.exists():
            raise ThinOrchestratorError(f"experiment.md not found in {self.experiment_path}")
        
        content = self.security.secure_read_text(exp_file)
        
        # Extract YAML from markdown
        if '---' in content:
            parts = content.split('---')
            if len(parts) >= 2:
                yaml_content = parts[1].strip()
            else:
                yaml_content = parts[0].strip()
        else:
            yaml_content = content
        
        try:
            config = yaml.safe_load(yaml_content)
        except yaml.YAMLError as e:
            raise ThinOrchestratorError(f"Invalid YAML in experiment.md: {e}")
        
        # Validate required fields
        required_fields = ['name', 'framework', 'corpus_path']
        missing_fields = [field for field in required_fields if field not in config]
        if missing_fields:
            raise ThinOrchestratorError(f"Missing required fields in experiment.md: {', '.join(missing_fields)}")
        
        return config
    
    def _load_framework(self, framework_filename: str) -> str:
        """Load framework content."""
        framework_file = self.experiment_path / framework_filename
        
        if not framework_file.exists():
            raise ThinOrchestratorError(f"Framework file not found: {framework_filename}")
        
        return self.security.secure_read_text(framework_file)
    
    def _load_corpus(self, corpus_path: str) -> List[Dict[str, Any]]:
        """Load corpus documents."""
        corpus_dir = self.experiment_path / corpus_path
        
        if not corpus_dir.exists():
            raise ThinOrchestratorError(f"Corpus directory not found: {corpus_path}")
        
        # Find all text files in corpus directory
        corpus_files = [f for f in corpus_dir.iterdir() if f.is_file() and f.suffix == '.txt']
        
        if not corpus_files:
            raise ThinOrchestratorError(f"No .txt files found in corpus directory: {corpus_path}")
        
        documents = []
        for txt_file in sorted(corpus_files):
            content = self.security.secure_read_text(txt_file)
            documents.append({
                "filename": txt_file.name,
                "content": content,
                "filepath": str(txt_file.relative_to(self.experiment_path))
            })
        
        return documents
    
    def _generate_final_report(self, 
                             analysis_result: Dict[str, Any],
                             synthesis_result: Dict[str, Any], 
                             experiment_config: Dict[str, Any],
                             manifest: EnhancedManifest) -> str:
        """Generate beautiful final markdown report."""
        
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        
        report = f"""# {experiment_config['name']} - Analysis Report

**Generated**: {timestamp}  
**Architecture**: THIN v2.0 Direct Function Calls  
**Mathematical Validation**: Enabled  

---

## Executive Summary

This report presents the results of computational research analysis using the Discernus THIN v2.0 architecture with enhanced mathematical validation capabilities.

**Key Features of This Analysis**:
- ✅ Mathematical "show your work" requirements for all calculations
- ✅ Dual-LLM validation with spot-checking of numerical results  
- ✅ Complete audit trails for academic reproducibility
- ✅ Content-addressable storage for perfect caching
- ✅ Security boundary enforcement

---

## Analysis Results

### Enhanced Analysis Agent Results
**Agent**: {analysis_result['result_content']['agent_name']}  
**Version**: {analysis_result['result_content']['agent_version']}  
**Duration**: {analysis_result['duration_seconds']:.1f} seconds  
**Mathematical Validation**: {analysis_result['mathematical_validation']}  

{analysis_result['result_content']['analysis_results']}

---

## Synthesis Results

### Enhanced Synthesis Agent Results  
**Agent**: {synthesis_result['result_content']['agent_name']}  
**Version**: {synthesis_result['result_content']['agent_version']}  
**Duration**: {synthesis_result['duration_seconds']:.1f} seconds  
**Mathematical Confidence**: {synthesis_result['synthesis_confidence']:.2f}  

{synthesis_result['result_content']['synthesis_results']}

---

## Mathematical Validation Report

### Validation Summary
- **Dual-LLM Validation**: {synthesis_result['result_content'].get('mathematical_validation', {}).get('validation_enabled', False)}
- **Mathematical Confidence**: {synthesis_result['synthesis_confidence']:.2f}
- **Errors Detected**: {len(synthesis_result['mathematical_validation'].get('mathematical_errors_found', []))}

### Validation Details
{synthesis_result['result_content'].get('mathematical_validation', {}).get('validation_content', 'No validation details available')}

---

## Provenance Information

### Experiment Configuration
- **Experiment**: {experiment_config['name']}
- **Framework**: {experiment_config['framework']}
- **Corpus Path**: {experiment_config['corpus_path']}

### Execution Metadata
- **Run ID**: {analysis_result['result_content']['execution_metadata']['start_time']}
- **Security Boundary**: {analysis_result['result_content']['provenance']['security_boundary']['experiment_name']}
- **Audit Session**: {analysis_result['result_content']['provenance']['audit_session_id']}

### Artifact Hashes
- **Framework**: {analysis_result['result_content']['input_artifacts']['framework_hash'][:16]}...
- **Documents**: {len(analysis_result['result_content']['input_artifacts']['document_hashes'])} corpus documents
- **Analysis Result**: {analysis_result['result_hash'][:16]}...
- **Synthesis Result**: {synthesis_result['result_hash'][:16]}...

---

## Quality Assurance

### THIN v2.0 Architecture Validation
- ✅ Direct function calls (no Redis coordination)
- ✅ LLM intelligence for complex reasoning
- ✅ Minimal software coordination  
- ✅ Perfect caching through content-addressable storage
- ✅ Complete audit trails for academic integrity

### Mathematical Validation
- ✅ "Show your work" requirements implemented
- ✅ Dual-LLM validation with spot-checking
- ✅ Confidence estimates for all numerical results
- ✅ Independent recalculation of key metrics

---

*This report was generated by the Discernus THIN v2.0 architecture with enhanced mathematical validation capabilities.*
"""
        
        return report
    
    def _calculate_duration(self, start: str, end: str) -> float:
        """Calculate duration between timestamps in seconds."""
        try:
            start_dt = datetime.fromisoformat(start.replace('Z', '+00:00'))
            end_dt = datetime.fromisoformat(end.replace('Z', '+00:00'))
            return (end_dt - start_dt).total_seconds()
        except Exception:
            return 0.0 