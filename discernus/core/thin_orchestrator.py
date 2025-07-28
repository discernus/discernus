#!/usr/bin/env python3
"""
THIN Orchestrator v2.0
=====================

Implements THIN principles:
- Direct function calls (no Redis)
- Perfect caching
- Minimal coordination logic
- Let LLMs be LLMs
"""

import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

from discernus.core.security_boundary import ExperimentSecurityBoundary, SecurityError
from discernus.core.audit_logger import AuditLogger
from discernus.core.local_artifact_storage import LocalArtifactStorage
from discernus.agents.EnhancedAnalysisAgent.main import EnhancedAnalysisAgent
from discernus.agents.EnhancedSynthesisAgent.main import EnhancedSynthesisAgent
from discernus.core.enhanced_manifest import EnhancedManifest


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

    def _chunk_documents(self, documents: List[Dict[str, Any]], chunk_size: int = 5) -> List[List[Dict[str, Any]]]:
        """
        Split documents into chunks for processing.
        
        Args:
            documents: List of document dictionaries
            chunk_size: Number of documents per chunk
            
        Returns:
            List of document chunks
        """
        return [documents[i:i + chunk_size] for i in range(0, len(documents), chunk_size)]

    def _execute_analysis_sequentially(self,
                                   analysis_agent: EnhancedAnalysisAgent,
                                   corpus_documents: List[Dict[str, Any]],
                                   framework_content: str,
                                   experiment_config: Dict[str, Any],
                                   model: str) -> tuple[List[Dict[str, Any]], Optional[str], Optional[str]]:
        """
        Executes the analysis agent for documents in chunks, passing CSV artifact hashes.
        
        Note: This method processes documents in chunks. API-level batching is handled by LiteLLM.
        """
        all_analysis_results = []
        scores_hash = None
        evidence_hash = None
        total_docs = len(corpus_documents)
        
        # Split documents into chunks
        chunk_size = 5  # Process 5 documents at a time
        chunks = self._chunk_documents(corpus_documents, chunk_size)
        total_chunks = len(chunks)
        
        print(f"\n🚀 Starting analysis of {total_docs} documents in {total_chunks} chunks...")
        
        for chunk_idx, chunk in enumerate(chunks, 1):
            chunk_docs = len(chunk)
            print(f"\n=== Processing chunk {chunk_idx}/{total_chunks} ({chunk_docs} documents) ===")
            
            for i, doc in enumerate(chunk):
                doc_num = (chunk_idx - 1) * chunk_size + i + 1
                print(f"\n--- Analyzing document {doc_num}/{total_docs}: {doc.get('filename')} ---")
                try:
                    # Process one document at a time
                    result = analysis_agent.analyze_documents(
                        framework_content=framework_content,
                        corpus_documents=[doc],  # Single document list
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
            
            print(f"\n✅ Completed chunk {chunk_idx}/{total_chunks}")
            print(f"   Progress: {len(all_analysis_results)}/{total_docs} documents processed")

        return all_analysis_results, scores_hash, evidence_hash

    def run_experiment(self, model: str = "vertex_ai/gemini-2.5-flash", synthesis_only: bool = False) -> Dict[str, Any]:
        """
        Run experiment with enhanced agents and mathematical validation.
        
        Args:
            model: LLM model to use
            synthesis_only: If True, skip analysis and run synthesis on existing CSVs
            
        Returns:
            Experiment results with mathematical validation
        """
        # Create run directory with timestamp
        run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        run_dir = self.experiment_path / "runs" / run_id
        run_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize logging and storage
        audit = AuditLogger(run_dir / "logs")
        storage = LocalArtifactStorage(run_dir / "artifacts")
        
        # Load experiment config
        experiment_config = self._load_experiment_config()
        
        # Create manifest
        manifest = EnhancedManifest(run_dir / "manifest.json")
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
        
        if synthesis_only:
            # Find latest CSVs in shared cache
            shared_cache = self.experiment_path / "shared_cache" / "artifacts"
            if not shared_cache.exists():
                raise ThinOrchestratorError("No shared cache found for synthesis-only mode")
            
            # Load artifact registry
            registry_path = shared_cache / "artifact_registry.json"
            if not registry_path.exists():
                raise ThinOrchestratorError("No artifact registry found in shared cache")
            
            with open(registry_path) as f:
                registry = json.load(f)
            
            # Find latest CSV artifacts
            scores_hash = None
            evidence_hash = None
            
            for artifact_hash, info in registry.items():
                if info.get("metadata", {}).get("artifact_type") == "intermediate_scores.csv":
                    scores_hash = artifact_hash
                elif info.get("metadata", {}).get("artifact_type") == "intermediate_evidence.csv":
                    evidence_hash = artifact_hash
            
            if not scores_hash or not evidence_hash:
                raise ThinOrchestratorError("Could not find required CSV artifacts in shared cache")
            
            # Run synthesis only
            synthesis_agent = EnhancedSynthesisAgent(self.security, audit, storage)
            synthesis_result = synthesis_agent.synthesize_results(
                scores_hash=scores_hash,
                evidence_hash=evidence_hash,
                analysis_results=[],  # No analysis results in synthesis-only mode
                experiment_config=experiment_config,
                model=model
            )
            
            if not synthesis_result or not isinstance(synthesis_result, dict):
                raise ThinOrchestratorError(f"Invalid synthesis result format: {type(synthesis_result)}")
            
            if "synthesis_report_markdown" not in synthesis_result:
                raise ThinOrchestratorError("Missing synthesis_report_markdown in result")
            
            # Save final report
            results_dir = run_dir / "results"
            results_dir.mkdir(exist_ok=True)
            
            with open(results_dir / "final_report.md", "w") as f:
                f.write(synthesis_result["synthesis_report_markdown"])
            
            return synthesis_result
        
        # Initialize analysis and synthesis agents
        analysis_agent = EnhancedAnalysisAgent(self.security, audit, storage)
        
        # Execute analysis (in chunks)
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
        
        synthesis_result = synthesis_agent.synthesize_results(
            scores_hash=scores_hash,
            evidence_hash=evidence_hash,
            analysis_results=all_analysis_results,
            experiment_config=experiment_config,
            model=model
        )
        
        synthesis_end_time = datetime.now(timezone.utc).isoformat()
        
        # Save final report
        results_dir = run_dir / "results"
        results_dir.mkdir(exist_ok=True)
        
        with open(results_dir / "final_report.md", "w") as f:
            f.write(synthesis_result["synthesis_report_markdown"])
        
        # Update manifest
        manifest.add_output_artifact(
            "synthesis_result",
            synthesis_result["result_hash"],
            {
                "filename": "final_report.md",
                "size_bytes": len(synthesis_result["synthesis_report_markdown"])
            }
        )
        
        manifest.add_execution_stage(
            "synthesis",
            synthesis_start_time,
            synthesis_end_time,
            "completed",
            {
                "model": model,
                "result_hash": synthesis_result["result_hash"]
            }
        )
        
        manifest.finalize()
        
        return synthesis_result

    def _load_experiment_config(self) -> Dict[str, Any]:
        """Load experiment configuration."""
        experiment_path = self.experiment_path / "experiment.md"
        if not experiment_path.exists():
            raise ThinOrchestratorError(f"Experiment file not found: {experiment_path}")
        
        experiment_content = self.security.secure_read_text(experiment_path)
        
        # Parse experiment config from markdown
        config = {
            "name": None,
            "framework": None,
            "corpus_path": None,
            "description": None
        }
        
        for line in experiment_content.split("\n"):
            line = line.strip()
            if line.startswith("- Framework:"):
                config["framework"] = line.split(":")[1].strip()
            elif line.startswith("- Corpus:"):
                config["corpus_path"] = line.split(":")[1].strip()
            elif line.startswith("- Name:"):
                config["name"] = line.split(":")[1].strip()
            elif line.startswith("## Description"):
                config["description"] = line.split("## Description")[1].strip()
        
        if not all([config["name"], config["framework"], config["corpus_path"]]):
            raise ThinOrchestratorError("Invalid experiment config - missing required fields")
        
        return config

    def _load_framework(self, framework_path: str) -> str:
        """Load framework content."""
        framework_file = self.experiment_path / framework_path
        if not framework_file.exists():
            raise ThinOrchestratorError(f"Framework file not found: {framework_path}")
        
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