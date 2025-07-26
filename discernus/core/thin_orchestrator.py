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
import pandas as pd
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

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
            synthesis_agent = EnhancedSynthesisAgent(self.security, audit, storage)
            
            # Execute analysis (one document at a time)
            analysis_start_time = datetime.now(timezone.utc).isoformat()
            all_analysis_results = self._execute_analysis_sequentially(
                analysis_agent,
                corpus_documents,
                framework_content,
                experiment_config,
                model
            )
            print("DEBUG: Raw all_analysis_results from sequential execution:")
            # Safe debug output that handles DataFrames
            for i, result in enumerate(all_analysis_results):
                print(f"  Result {i}:")
                print(f"    Success: {result.get('success', False)}")
                print(f"    Batch ID: {result.get('batch_id', 'unknown')}")
                if 'csv_dataframe' in result:
                    df = result['csv_dataframe']
                    print(f"    CSV Shape: {df.shape}")
                    print(f"    CSV Columns: {list(df.columns)}")
                else:
                    print(f"    Result Keys: {list(result.keys())}")
            manifest.add_execution_stage(
                stage_name="enhanced_analysis", 
                agent_name="EnhancedAnalysisAgent_CSV",
                start_time=analysis_start_time,
                end_time=datetime.now(timezone.utc).isoformat(),
                status="completed",
                metadata={"num_documents": len(corpus_documents)}
            )
            
            # Consolidate analysis data for synthesis
            print("\n🔬 Synthesizing results...")
            synthesis_start_time = datetime.now(timezone.utc).isoformat()
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
            
            # Finalize manifest
            manifest.set_synthesis_results(synthesis_result)
            
            # Combine batch results for final summary
            analysis_summary = self._combine_batch_results(all_analysis_results)

            # Generate comprehensive final report with both analysis and synthesis results
            final_report_content = self._generate_final_report(
                analysis_summary, synthesis_result, experiment_config, manifest
            )
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
                "analysis_duration": analysis_summary.get("total_duration_seconds", 0),
                "synthesis_duration": synthesis_result.get("duration_seconds", 0),
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
                                       model: str) -> List[Dict[str, Any]]:
        """
        Executes the CSV-based analysis agent for all documents at once.
        """
        print(f"\n=== CSV-Based Analysis ===")
        print(f"Documents to analyze: {len(corpus_documents)}")
        
        # Use the new CSV method that processes all documents at once
        result = analysis_agent.analyze_documents_csv(
            framework_content=framework_content,
            corpus_documents=corpus_documents,
            experiment_config=experiment_config,
            model=model
        )
        
        # Return in the expected format for compatibility
        if result['success']:
            print(f"✅ CSV analysis completed successfully")
            print(f"   Generated CSV: {result['csv_dataframe'].shape[0]} rows")
            return [result]  # Wrap in list for backward compatibility
        else:
            print(f"❌ CSV analysis failed: {result.get('error', 'Unknown error')}")
            return []

    def _extract_and_consolidate_analysis_data(self, 
                                               analysis_results: List[Dict[str, Any]],
                                               storage: LocalArtifactStorage) -> Tuple[List[Dict[str, Any]], Dict[str, str]]:
        """
        Extracts CSV data from analysis results for synthesis.
        
        Updated for CSV-based architecture - much simpler than complex nested structures.
        """
        print("🔄 Consolidating CSV analysis data for synthesis...")
        
        if not analysis_results:
            print("⚠️  No analysis results to consolidate")
            return [], {}
        
        # Get the CSV data from the first (and only) result
        csv_result = analysis_results[0]
        
        if not csv_result.get('success', False):
            print("⚠️  Analysis failed - no data to consolidate")
            return [], {}
        
        csv_dataframe = csv_result['csv_dataframe']
        batch_id = csv_result['batch_id']
        
        # Convert CSV DataFrame to synthesis-friendly format
        consolidated_data = []
        artifact_map = {}
        
        # Group by document for synthesis
        unique_documents = csv_dataframe['document_id'].unique()
        
        for doc_id in unique_documents:
            doc_rows = csv_dataframe[csv_dataframe['document_id'] == doc_id]
            
            # Create structured entry compatible with synthesis agent
            doc_scores = {}
            doc_evidence = {}
            
            for _, row in doc_rows.iterrows():
                dimension = row['framework_dimension']
                doc_scores[dimension] = {
                    'intensity': row['intensity_score'],
                    'salience': row['salience_score'],
                    'confidence': row['confidence']
                }
                
                if row['evidence_quote']:
                    doc_evidence[dimension] = [row['evidence_quote']]
            
            structured_entry = {
                "original_document": {
                    "filename": doc_id,
                    "hash": f"csv_{batch_id}_{doc_id}"[:12]  # Generate simple hash
                },
                "artifact_hash": f"csv_{batch_id}",
                "scores": doc_scores,
                "evidence": doc_evidence,
                "csv_data": doc_rows.to_dict('records'),  # Include raw CSV data
                "reasoning": doc_rows.iloc[0]['reasoning_snippet'] if len(doc_rows) > 0 else ""
            }
            
            consolidated_data.append(structured_entry)
            artifact_map[doc_id] = f"csv_{batch_id}"
        
        print(f"✅ Consolidated CSV data for {len(consolidated_data)} documents")
        print(f"   Total CSV rows: {len(csv_dataframe)}")
        print(f"   Framework dimensions: {len(csv_dataframe['framework_dimension'].unique())}")
        
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


    def _combine_batch_results(self, batch_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Combines results from analysis batches into a single summary.
        
        Updated for CSV-based architecture.
        """
        if not batch_results:
            return {"total_duration_seconds": 0, "num_batches": 0, "successful_batches": 0}

        # Handle CSV result format
        total_duration = 0
        num_batches = len(batch_results)
        successful_batches = 0
        
        for result in batch_results:
            # CSV results have different structure
            if result.get('success', False):
                successful_batches += 1
                # Calculate duration if available
                if 'json_artifact' in result:
                    exec_info = result['json_artifact'].get('execution_info', {})
                    start_time = exec_info.get('start_time')
                    end_time = exec_info.get('end_time')
                    if start_time and end_time:
                        try:
                            from datetime import datetime
                            start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
                            end_dt = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
                            total_duration += (end_dt - start_dt).total_seconds()
                        except:
                            pass

        return {
            "total_duration_seconds": total_duration,
            "num_batches": num_batches,
            "successful_batches": successful_batches,
            "all_batches_successful": successful_batches == num_batches,
            "csv_analysis_summary": {
                "total_csv_rows": sum(r.get('csv_dataframe', pd.DataFrame()).shape[0] 
                                    for r in batch_results if 'csv_dataframe' in r),
                "total_documents": len(set(
                    doc_id for r in batch_results if 'csv_dataframe' in r
                    for doc_id in r['csv_dataframe']['document_id'].unique()
                )) if batch_results and 'csv_dataframe' in batch_results[0] else 0,
                "framework_dimensions": len(set(
                    dim for r in batch_results if 'csv_dataframe' in r  
                    for dim in r['csv_dataframe']['framework_dimension'].unique()
                )) if batch_results and 'csv_dataframe' in batch_results[0] else 0
            }
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
        """Generate simple final markdown report for CSV architecture."""
        
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        
        # Get basic stats safely
        batch_id = analysis_result.get('batch_id', 'Unknown')
        csv_rows = 0
        analysis_success = analysis_result.get('success', False)
        
        if 'csv_dataframe' in analysis_result and hasattr(analysis_result['csv_dataframe'], 'shape'):
            csv_rows = analysis_result['csv_dataframe'].shape[0]
        
        # Get synthesis info safely
        synthesis_agent = synthesis_result.get('agent_name', 'EnhancedSynthesisAgent')
        synthesis_duration = synthesis_result.get('duration_seconds', 0.0)
        synthesis_confidence = synthesis_result.get('synthesis_confidence', 0.0)
        synthesis_markdown = synthesis_result.get('synthesis_report_markdown', 'Synthesis completed successfully.')
        
        # Get experiment info safely
        exp_name = experiment_config.get('name', 'Unknown')
        exp_framework = experiment_config.get('framework', 'Unknown')
        exp_corpus = experiment_config.get('corpus_path', 'Unknown')
        
        report = f"""# {exp_name} - CSV Analysis Report

**Generated**: {timestamp}  
**Architecture**: THIN v2.0 CSV-Based Analysis  

---

## Analysis Results

### CSV Analysis Summary
**Agent**: EnhancedAnalysisAgent_CSV  
**Batch ID**: {batch_id}  
**CSV Rows Generated**: {csv_rows}  
**Analysis Status**: {'SUCCESS' if analysis_success else 'FAILED'}

*Complete CSV data available for researcher download and statistical analysis.*

---

## Synthesis Results

**Agent**: {synthesis_agent}  
**Duration**: {synthesis_duration:.1f} seconds  
**Confidence**: {synthesis_confidence:.2f}

{synthesis_markdown}

---

## Experiment Configuration

- **Experiment**: {exp_name}
- **Framework**: {exp_framework}
- **Corpus Path**: {exp_corpus}

**Report Generation Complete**: {timestamp}
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