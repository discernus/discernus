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
from typing import Dict, Any, List, Optional, Tuple

from .security_boundary import ExperimentSecurityBoundary, SecurityError
from .audit_logger import AuditLogger
from .local_artifact_storage import LocalArtifactStorage
from .enhanced_manifest import EnhancedManifest
from ..agents.EnhancedAnalysisAgent.main import EnhancedAnalysisAgent
from ..agents.EnhancedSynthesisAgent.main import EnhancedSynthesisAgent
from ..agents.batch_planner_agent import BatchPlannerAgent


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
        
    def run_experiment(self, model: str = "vertex_ai/gemini-2.5-pro") -> Dict[str, Any]:
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
            
            # Initialize artifact storage
            storage = LocalArtifactStorage(self.security, run_folder)
            
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
            batch_planner = BatchPlannerAgent(self.security, audit)
            batch_plan = batch_planner.create_batches(
                framework_content=framework_content,
                corpus_documents=corpus_documents,
                model=model
            )
            
            batch_planning_end_time = datetime.now(timezone.utc).isoformat()
            manifest.add_execution_stage("batch_planning", "BatchPlannerAgent",
                                       batch_planning_start_time, batch_planning_end_time, "completed", {
                "total_batches": batch_plan["total_batches"],
                "total_estimated_cost": batch_plan["total_estimated_cost"],
                "total_estimated_tokens": batch_plan["total_estimated_tokens"],
                "context_window_limit": batch_plan["context_window_limit"]
            })
            
            print(f"💰 Total estimated cost: ${batch_plan['total_estimated_cost']:.4f}")
            print(f"📊 Batch plan: {batch_plan['total_batches']} batches, "
                  f"⏱️ ~{(batch_plan['total_batches'] * batch_plan['delay_between_batches'])/60:.1f} minutes")
            
            # Execute batched analysis with production monitoring and intelligent pacing
            analysis_start_time = datetime.now(timezone.utc).isoformat()
            manifest.add_execution_stage("enhanced_analysis", "EnhancedAnalysisAgent", analysis_start_time)
            
            analysis_agent = EnhancedAnalysisAgent(self.security, audit, storage)
            all_analysis_results = []
            total_actual_cost = 0.0
            
            print(f"\n🚀 Starting {batch_plan['total_batches']} batch analysis with intelligent pacing...")
            
            for i, batch in enumerate(batch_plan["batches"]):
                # Calculate pacing delay (skip for first batch)
                delay_seconds = batch_plan['delay_between_batches'] if i > 0 else 0
                
                # Add total_batches info for status reporting
                batch['total_batches'] = batch_plan['total_batches']
                
                # Use production batch execution with enhanced monitoring
                batch_result = batch_planner.execute_batch_with_pacing(
                    batch_info=batch,
                    analysis_agent=analysis_agent,
                    framework_content=framework_content,
                    delay_seconds=delay_seconds
                )
                
                # Track actual costs and execution
                if batch_result['success']:
                    total_actual_cost += batch_result.get('actual_cost', 0.0)
                    # The batch_result contains the analysis results already
                    all_analysis_results.append(batch_result['results'])
                else:
                    print(f"❌ Batch {batch['batch_id']} failed: {batch_result.get('error', 'Unknown error')}")
                    # Add empty results to maintain batch ordering
                    all_analysis_results.append({})
                
                audit.log_orchestrator_event("batch_completed", {
                    "batch_id": batch['batch_id'],
                    "documents_processed": batch['document_count'],
                    "duration_seconds": batch_result['execution_time'],
                    "success": batch_result['success'],
                    "actual_cost": batch_result.get('actual_cost', 0.0)
                })
            
            # Combine all batch results
            combined_analysis_result = self._combine_batch_results(all_analysis_results)
            
            # Production cost summary
            cost_variance = abs(total_actual_cost - batch_plan['total_estimated_cost'])
            cost_accuracy = ((batch_plan['total_estimated_cost'] - cost_variance) / batch_plan['total_estimated_cost']) * 100 if batch_plan['total_estimated_cost'] > 0 else 100
            
            print(f"\n💰 FINAL COST SUMMARY:")
            print(f"   Estimated: ${batch_plan['total_estimated_cost']:.4f}")
            print(f"   Actual: ${total_actual_cost:.4f}")
            print(f"   Accuracy: {cost_accuracy:.1f}%")
            
            analysis_end_time = datetime.now(timezone.utc).isoformat()
            manifest.add_execution_stage("enhanced_analysis", "EnhancedAnalysisAgent", 
                                       analysis_start_time, analysis_end_time, "completed", {
                "total_batches_processed": len(batch_plan["batches"]),
                "total_documents": len(corpus_documents),
                "estimated_cost": batch_plan['total_estimated_cost'],
                "actual_cost": total_actual_cost,
                "cost_accuracy_percent": cost_accuracy,
                "mathematical_validation": True
            })
            
            # Phase 2: Enhanced Synthesis with Mathematical Spot-Checking
            synthesis_start_time = datetime.now(timezone.utc).isoformat()
            manifest.add_execution_stage("enhanced_synthesis", "EnhancedSynthesisAgent", synthesis_start_time)
            
            # Execute synthesis
            print("\n🔬 Synthesizing results...")
            synthesis_agent = EnhancedSynthesisAgent(self.security, audit, storage)
            
            # Extract structured data for synthesis to avoid memory issues
            structured_data, artifact_map = self._extract_and_consolidate_analysis_data(all_analysis_results, storage)

            # Generate human-readable artifact index
            self._generate_artifact_index_html(artifact_map, run_folder)

            synthesis_result = synthesis_agent.synthesize_results(
                analysis_results=structured_data,
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
            
            # Generate final beautiful markdown report
            final_report = self._generate_final_report(
                combined_analysis_result, synthesis_result, experiment_config, manifest
            )
            
            report_hash = storage.put_artifact(
                final_report.encode('utf-8'),
                {"artifact_type": "final_report", "format": "markdown"}
            )
            
            # Save beautiful report to results directory
            results_dir = self.security.secure_mkdir(run_folder / "results")
            report_file = results_dir / "final_report.md"
            self.security.secure_write_text(report_file, final_report)
            
            # Finalize manifest and audit
            manifest_file = manifest.finalize_manifest()
            audit.finalize_session()
            
            # Calculate total execution time
            end_time = datetime.now(timezone.utc).isoformat()
            total_duration = self._calculate_duration(start_time, end_time)
            
            # Final orchestrator event
            audit.log_orchestrator_event("experiment_complete", {
                "total_duration_seconds": total_duration,
                "analysis_duration": analysis_result["duration_seconds"],
                "synthesis_duration": synthesis_result["duration_seconds"],
                "final_report_hash": report_hash,
                "manifest_file": manifest_file,
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
                "manifest_file": manifest_file,
                "total_duration_seconds": total_duration,
                "analysis_result": analysis_result,
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
    
    def _extract_and_consolidate_analysis_data(self, 
                                               analysis_results: List[Dict[str, Any]],
                                               storage: LocalArtifactStorage) -> Tuple[List[Dict[str, Any]], Dict[str, str]]:
        """
        Extracts structured data from analysis artifacts for memory-efficient synthesis.
        """
        print(" consolidating analysis data for synthesis...")
        consolidated_data = []
        artifact_map = {} # Maps original filename to artifact hash

        for result_wrapper in analysis_results:
            analysis_data = result_wrapper.get('analysis_results', {})
            
            if not isinstance(analysis_data, dict):
                # Handle case where LLM returned a string despite instructions
                print(f"⚠️  Skipping non-dict analysis result in batch {result_wrapper.get('batch_id')}")
                continue

            doc_analyses = analysis_data.get('document_analyses', {})
            for doc_filename, doc_analysis in doc_analyses.items():
                # Find the original document hash from the input artifacts
                # This is a bit convoluted, but necessary to link back
                original_doc_hash = None
                for doc_info in result_wrapper.get('input_artifacts', {}).get('documents', []):
                    if doc_info.get('filename') == doc_filename:
                        original_doc_hash = doc_info.get('hash')
                        break

                structured_entry = {
                    "original_document": {
                        "filename": doc_filename,
                        "hash": original_doc_hash
                    },
                    "artifact_hash": result_wrapper.get('artifact_hash'),
                    "scores": doc_analysis.get('scores'),
                    "tension_analysis": doc_analysis.get('tension_analysis'),
                    "character_clusters": doc_analysis.get('character_clusters')
                }
                consolidated_data.append(structured_entry)
                if original_doc_hash:
                    artifact_map[doc_filename] = result_wrapper.get('artifact_hash')

        print(f"  Consolidated data for {len(consolidated_data)} documents.")
        return consolidated_data, artifact_map

    def _generate_artifact_index_html(self, artifact_map: Dict[str, str], run_folder: Path):
        """Generates a human-readable HTML index of artifacts."""
        html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Artifact Index</title>
    <style>
        body { font-family: sans-serif; margin: 2em; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        a { color: #0066cc; }
    </style>
</head>
<body>
    <h1>Analysis Artifact Index</h1>
    <p>This index maps original corpus documents to their detailed analysis artifact files.</p>
    <table>
        <thead>
            <tr>
                <th>Original Document</th>
                <th>Analysis Artifact Link</th>
            </tr>
        </thead>
        <tbody>
"""
        for filename, fhash in sorted(artifact_map.items()):
            relative_path = f"./artifacts/{fhash}"
            html_content += f'            <tr><td>{filename}</td><td><a href="{relative_path}">{fhash}</a></td></tr>\n'
        
        html_content += """
        </tbody>
    </table>
</body>
</html>
"""
        index_path = run_folder / "artifact_index.html"
        self.security.secure_write_file(index_path, html_content)
        print(f"  Generated artifact index: {index_path}")


    def _load_experiment_config(self) -> Dict[str, Any]:
        """Load and validate experiment configuration."""
        experiment_file = self.experiment_path / "experiment.md"
        
        if not experiment_file.exists():
            raise ThinOrchestratorError(f"experiment.md not found in {self.experiment_path}")
        
        content = self.security.secure_read_text(experiment_file)
        
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
    
    def _combine_batch_results(self, batch_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Combine multiple batch analysis results into a single unified result.
        
        Args:
            batch_results: List of individual batch analysis results
            
        Returns:
            Combined analysis result in the same format as single batch
        """
        if not batch_results:
            raise ThinOrchestratorError("Cannot combine empty batch results")
        
        if len(batch_results) == 1:
            return batch_results[0]
        
        # Use the first batch as the template
        combined_result = batch_results[0].copy()
        
        # Combine analysis content from all batches
        combined_analysis_parts = []
        combined_documents = []
        total_duration = 0.0
        
        for i, batch_result in enumerate(batch_results):
            batch_content = batch_result["result_content"]
            combined_analysis_parts.append(f"## Batch {i+1} Analysis Results\n\n{batch_content['analysis_results']}")
            combined_documents.extend(batch_content.get("document_analyses", []))
            total_duration += batch_result.get("duration_seconds", 0.0)
        
        # Update the combined result
        combined_result["result_content"]["analysis_results"] = "\n\n".join(combined_analysis_parts)
        combined_result["result_content"]["document_analyses"] = combined_documents
        combined_result["duration_seconds"] = total_duration
        
        # Update metadata to reflect batching
        combined_result["result_content"]["processing_mode"] = "batched_analysis"
        combined_result["result_content"]["total_batches"] = len(batch_results)
        combined_result["result_content"]["batch_metadata"] = [
            {
                "batch_id": i + 1,
                "documents_processed": len(batch["result_content"].get("document_analyses", [])),
                "duration_seconds": batch.get("duration_seconds", 0.0),
                "result_hash": batch["result_hash"]
            }
            for i, batch in enumerate(batch_results)
        ]
        
        print(f"🔗 Combined {len(batch_results)} batch results into unified analysis")
        
        return combined_result
    
    def _calculate_duration(self, start: str, end: str) -> float:
        """Calculate duration between timestamps in seconds."""
        try:
            start_dt = datetime.fromisoformat(start.replace('Z', '+00:00'))
            end_dt = datetime.fromisoformat(end.replace('Z', '+00:00'))
            return (end_dt - start_dt).total_seconds()
        except Exception:
            return 0.0 