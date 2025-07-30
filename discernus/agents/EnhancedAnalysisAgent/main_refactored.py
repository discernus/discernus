#!/usr/bin/env python3
"""
Enhanced Analysis Agent v2.0 - THIN Refactored
===============================================

Refactored version complying with THIN 150-line limit.
Orchestrates specialized components instead of doing everything in one class.

THIN Architecture:
- FrameworkParser: Extracts dimensions from framework markdown
- AnalysisCacheManager: Handles perfect caching of analysis results
- DocumentProcessor: Prepares documents for analysis
- CSVHandler: Extracts and persists CSV data from LLM responses
- Main class: Thin orchestration layer only
"""

import hashlib
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from litellm import completion

from discernus.core.security_boundary import ExperimentSecurityBoundary
from discernus.core.audit_logger import AuditLogger
from discernus.core.local_artifact_storage import LocalArtifactStorage

from .framework_parser import FrameworkParser
from .analysis_cache import AnalysisCacheManager
from .document_processor import DocumentProcessor
from .csv_handler import CSVHandler
from .llm_analyzer import LLMAnalyzer


class EnhancedAnalysisAgentError(Exception):
    """Enhanced analysis agent specific exceptions"""
    pass


class EnhancedAnalysisAgent:
    """
    THIN Enhanced Analysis Agent - Orchestration Layer Only
    
    Coordinates specialized components:
    - Framework parsing (FrameworkParser)
    - Cache management (AnalysisCacheManager) 
    - Document processing (DocumentProcessor)
    - CSV handling (CSVHandler)
    - LLM interaction (this class)
    """
    
    def __init__(self, security: ExperimentSecurityBoundary, audit: AuditLogger, 
                 storage: LocalArtifactStorage):
        self.security = security
        self.audit = audit
        self.storage = storage
        self.agent_name = "EnhancedAnalysisAgent"
        self.agent_version = "2.0.0_thin_refactored"
        
        # Initialize THIN components
        self.framework_parser = FrameworkParser()
        self.cache_manager = AnalysisCacheManager(storage, audit)
        self.document_processor = DocumentProcessor(storage)
        
        # Load prompt template and initialize LLM analyzer
        prompt_template = self._load_prompt_template()
        self.llm_analyzer = LLMAnalyzer(prompt_template)
    
    def _load_prompt_template(self) -> str:
        """Load the enhanced prompt template from YAML."""
        prompt_file = self.security.experiment_path / "prompts" / "enhanced_analysis_prompt.yaml"
        if prompt_file.exists():
            import yaml
            with open(prompt_file) as f:
                config = yaml.safe_load(f)
                return config.get('template', 'Default template not found')
        return "Enhanced analysis prompt template not found"
    
    def analyze_batch(self, framework_content: str, corpus_documents: List[Dict[str, Any]], 
                     experiment_config: Dict[str, Any], model: str = "vertex_ai/gemini-2.5-flash",
                     current_scores_hash: Optional[str] = None, 
                     current_evidence_hash: Optional[str] = None) -> Dict[str, Any]:
        """
        Orchestrate batch analysis using THIN components.
        
        THIN Principle: This method is now just orchestration.
        All complex logic is delegated to specialized components.
        """
        start_time = datetime.now(timezone.utc).isoformat()
        
        # Calculate provenance hashes
        framework_hash = hashlib.sha256(framework_content.encode('utf-8')).hexdigest()
        corpus_content = ''.join([doc.get('filename', '') + str(doc.get('content', '')) 
                                 for doc in corpus_documents])
        corpus_hash = hashlib.sha256(corpus_content.encode('utf-8')).hexdigest()
        
        # Create provenance metadata for all components
        provenance_metadata = {
            "framework_hash": framework_hash,
            "corpus_hash": corpus_hash,
            "analysis_model": model,
            "analysis_timestamp": start_time,
            "agent_name": self.agent_name
        }
        
        # Generate batch ID for caching
        batch_id = self.cache_manager.generate_batch_id(framework_content, corpus_documents)
        
        self.audit.log_agent_event(self.agent_name, "batch_analysis_start", {
            "batch_id": batch_id,
            "num_documents": len(corpus_documents),
            "model": model,
            "experiment": experiment_config.get("name", "unknown")
        })
        
        try:
            # Check cache first
            cache_result = self.cache_manager.check_cache(batch_id, self.agent_name)
            if cache_result.hit:
                csv_handler = CSVHandler(self.storage, {})
                return self.cache_manager.handle_cache_hit(
                    cache_result, csv_handler, current_scores_hash, current_evidence_hash, batch_id)
            
            # Parse framework
            framework_config = self.framework_parser.parse_framework(framework_content, framework_hash)
            
            # Process documents
            processed_docs, document_hashes = self.document_processor.process_documents(
                corpus_documents, batch_id)
            
            # Perform LLM analysis
            analysis_result = self.llm_analyzer.analyze_documents(
                framework_config, processed_docs, model, batch_id)
            
            # Handle CSV extraction and persistence
            csv_handler = CSVHandler(self.storage, provenance_metadata)
            new_scores_hash, new_evidence_hash = csv_handler.extract_and_persist_csvs(
                analysis_result['raw_analysis_response'], 
                document_hashes[0] if document_hashes else "unknown_artifact",
                current_scores_hash, current_evidence_hash)
            
            return {
                "analysis_result": analysis_result,
                "scores_hash": new_scores_hash,
                "evidence_hash": new_evidence_hash
            }
            
        except Exception as e:
            self.audit.log_agent_event(self.agent_name, "analysis_error", {
                "batch_id": batch_id,
                "error": str(e)
            })
            raise EnhancedAnalysisAgentError(f"Analysis failed: {e}")
    

    
