#!/usr/bin/env python3
"""
txtai Evidence Curator Agent

This agent uses txtai for fast, accurate evidence retrieval from large evidence pools.
Instead of loading all evidence into LLM context, it provides targeted query-based
retrieval with full provenance preservation.

Key Design Principles:
- Query-based evidence retrieval using txtai semantic search + metadata filtering
- Maintains perfect academic provenance (document_name, dimension, confidence)
- Scales to 300,000+ evidence pieces without context window issues
- Deterministic results for reproducible research
- No evidence hallucination - only returns actual evidence from analysis
"""

import json
import logging
import os
import sys
import tempfile
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from pathlib import Path

# Import txtai for evidence indexing
try:
    from txtai.embeddings import Embeddings
except ImportError:
    raise ImportError("txtai is required. Install with: pip install txtai")

# Import LLM gateway from main codebase
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from discernus.gateway.llm_gateway import LLMGateway
from discernus.gateway.model_registry import ModelRegistry
from discernus.core.audit_logger import AuditLogger
from discernus.core.local_artifact_storage import LocalArtifactStorage


@dataclass
class EvidenceQuery:
    """Structured evidence query."""
    document_name: Optional[str] = None
    dimension: Optional[str] = None
    speaker: Optional[str] = None
    semantic_query: Optional[str] = None
    limit: int = 5


@dataclass
class EvidenceResult:
    """Evidence retrieval result with full provenance."""
    quote_text: str
    document_name: str
    dimension: str
    confidence: float
    score: float  # txtai relevance score
    metadata: Dict[str, Any]


@dataclass
class TxtaiCurationRequest:
    """Request for txtai-based evidence curation."""
    statistical_results: Dict[str, Any]
    evidence_data: bytes  # JSON evidence data
    framework_spec: str
    model: str


@dataclass
class TxtaiCurationResponse:
    """Response from txtai evidence curation."""
    raw_llm_curation: str
    curation_summary: Dict[str, Any]
    success: bool
    error_message: Optional[str] = None
    
    def to_json_serializable(self) -> Dict[str, Any]:
        """Convert response to JSON-serializable format for compatibility."""
        return {
            "raw_llm_curation": self.raw_llm_curation,
            "curation_summary": self.curation_summary,
            "success": self.success,
            "error_message": self.error_message
        }


class TxtaiEvidenceCurator:
    """
    Evidence curator using txtai for scalable, accurate evidence retrieval.
    
    This agent indexes evidence once, then provides fast query-based retrieval
    for synthesis agents. Maintains perfect academic provenance while scaling
    to massive evidence pools.
    """
    
    def __init__(self, model: str, artifact_storage: LocalArtifactStorage, audit_logger=None):
        """
        Initialize the txtai Evidence Curator.
        
        Args:
            model: LLM model for synthesis (queries are deterministic)
            audit_logger: Optional audit logger for cost tracking
        """
        self.model = model
        self.model_registry = ModelRegistry()
        self.llm_gateway = LLMGateway(self.model_registry)
        self.logger = logging.getLogger(__name__)
        self.audit_logger = audit_logger
        self.agent_name = "TxtaiEvidenceCurator"

        # txtai embeddings instance (initialized when needed)
        self.embeddings = None
        self.index_built = False
        self.documents = []  # Store documents for retrieval

        if self.audit_logger:
            self.audit_logger.log_agent_event(self.agent_name, "initialization", {"model": self.model})

    def curate_evidence(self, request: TxtaiCurationRequest) -> TxtaiCurationResponse:
        """
        Main entry point for txtai-based evidence curation.
        
        Process:
        1. Build txtai index from evidence data (if not already built)
        2. For each statistical finding, query for relevant evidence
        3. Synthesize narrative using retrieved evidence
        """
        if self.audit_logger:
            self.audit_logger.log_agent_event(self.agent_name, "curation_start", {"model": self.model})
        try:
            # Load and index evidence
            if not self.index_built:
                success = self._build_evidence_index(request.evidence_data)
                if not success:
                    return self._create_error_response("Failed to build evidence index")
            
            # Process statistical results and generate evidence-based narratives using batch processing
            # Process both raw data and derived metrics results
            all_results = {}
            if "stage_1_raw_data" in request.statistical_results:
                all_results.update(request.statistical_results["stage_1_raw_data"].get("results", {}))
            if "stage_2_derived_metrics" in request.statistical_results:
                all_results.update(request.statistical_results["stage_2_derived_metrics"].get("results", {}))
            
            # Filter tasks that need evidence linking according to Epic 280 design
            valid_tasks = {}
            for task_name, task_result in all_results.items():
                if "provenance" not in task_result:
                    self.logger.warning(f"Skipping task '{task_name}' - no provenance information")
                    continue
                
                # Apply Epic 280 selective evidence linking criteria
                if self._task_needs_evidence_linking(task_name, task_result):
                    valid_tasks[task_name] = task_result
                else:
                    self.logger.debug(f"Skipping task '{task_name}' - mathematical operation, needs transparency not evidence")
            
            self.logger.info(f"Evidence linking applied to {len(valid_tasks)}/{len(all_results)} tasks (Epic 280 selective criteria)")
            
            # Use batch processing to generate all narratives in a single LLM call
            final_curation = self._batch_generate_evidence_narratives(valid_tasks, request.framework_spec)
            
            if self.audit_logger:
                self.audit_logger.log_agent_event(self.agent_name, "curation_success", {"tasks_processed": len(valid_tasks)})
            return TxtaiCurationResponse(
                raw_llm_curation=final_curation,
                curation_summary={
                    "findings_synthesized": len(valid_tasks),
                    "evidence_queries_executed": len(valid_tasks),
                    "indexing_method": "txtai_semantic_search_batch"
                },
                success=True
            )
            
        except Exception as e:
            self.logger.error(f"txtai evidence curation failed: {str(e)}")
            if self.audit_logger:
                self.audit_logger.log_error("curation_failed", str(e), {"agent": self.agent_name})
            return self._create_error_response(str(e))
    
    def _task_needs_evidence_linking(self, task_name: str, task_result: Dict[str, Any]) -> bool:
        """
        Determine if a statistical task needs evidence linking according to Epic 280 design.
        
        Epic 280 Criteria:
        ✅ Dimensional scores (dignity_score = 0.0) → Need evidence justification
        ✅ Axis calculations (dignity-tribalism tension) → Need component evidence  
        ❌ Correlations (r=0.912) → Mathematical relationship, no evidence needed
        ❌ Composite indices → Transparent formula + component evidence sufficient
        ❌ Data validation → Technical operations
        ❌ Statistical tests → Mathematical operations
        """
        task_type = task_result.get("type", "unknown")
        
        # Tasks that need evidence linking (Epic 280)
        evidence_needed_patterns = [
            # Dimensional score calculations and validations
            "dimensional_score",
            "dimension_score", 
            "axis_calculation",
            "tension_calculation",
            # Individual metric calculations that represent analytical judgments
            "individual_metric"
        ]
        
        # Tasks that do NOT need evidence linking (Epic 280)
        mathematical_only_patterns = [
            # Statistical operations
            "one_way_anova",
            "correlation", 
            "t_test",
            "chi_square",
            "regression",
            # Data validation and technical operations
            "metric_validation",
            "missing_data_check",
            "range_check",
            "data_quality",
            # Composite calculations (formula transparency sufficient)
            "derived_metrics_calculation",
            "summary_statistics",
            "descriptive_stats",
            # Aggregation operations
            "group_by",
            "aggregation"
        ]
        
        # Check if task type indicates mathematical-only operation
        for pattern in mathematical_only_patterns:
            if pattern in task_type.lower() or pattern in task_name.lower():
                return False
        
        # Check if task type indicates evidence-needed operation
        for pattern in evidence_needed_patterns:
            if pattern in task_type.lower() or pattern in task_name.lower():
                return True
        
        # Default: Conservative approach - include evidence for unclear cases
        # This ensures we don't miss important analytical judgments
        self.logger.debug(f"Task '{task_name}' (type: {task_type}) defaulting to evidence linking")
        return True

    def _build_evidence_index(self, evidence_data: bytes) -> bool:
        """
        Build txtai index from evidence data.
        
        Args:
            evidence_data: JSON evidence data from analysis
            
        Returns:
            True if indexing succeeded, False otherwise
        """
        if self.audit_logger:
            self.audit_logger.log_agent_event(self.agent_name, "indexing_start", {"evidence_count": len(json.loads(evidence_data.decode('utf-8')).get('evidence_data', []))})
        try:
            # Parse evidence data
            evidence_json = json.loads(evidence_data.decode('utf-8'))
            evidence_list = evidence_json.get('evidence_data', [])
            
            if not evidence_list:
                self.logger.warning("No evidence data found for indexing")
                return False
            
            # Initialize txtai embeddings
            self.embeddings = Embeddings()
            
            # Prepare documents for indexing
            documents = []
            for i, evidence in enumerate(evidence_list):
                # Create searchable text combining metadata and content
                search_text = f"{evidence.get('document_name', '')} {evidence.get('dimension', '')} evidence: {evidence.get('quote_text', '')}"
                
                doc = {
                    "id": i,
                    "text": search_text,
                    "document_name": evidence.get('document_name', ''),
                    "dimension": evidence.get('dimension', ''),
                    "quote_text": evidence.get('quote_text', ''),
                    "confidence": evidence.get('confidence', 0.0),
                    "context_type": evidence.get('context_type', ''),
                    "extraction_method": evidence.get('extraction_method', '')
                }
                documents.append(doc)
            
            # Store documents for retrieval
            self.documents = documents
            
            # Build the index
            self.embeddings.index(documents)
            self.index_built = True
            
            self.logger.info(f"Built txtai index with {len(documents)} evidence pieces")
            if self.audit_logger:
                self.audit_logger.log_agent_event(self.agent_name, "indexing_complete", {"indexed_docs": len(documents)})

            # Debug: Log sample of indexed documents
            sample_docs = documents[:3] if len(documents) >= 3 else documents
            for i, doc in enumerate(sample_docs):
                self.logger.info(f"Sample doc {i}: {doc.get('document_name', 'N/A')} - {doc.get('dimension', 'N/A')} - {doc.get('quote_text', '')[:50]}...")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to build evidence index: {str(e)}")
            if self.audit_logger:
                self.audit_logger.log_error("indexing_failed", str(e), {"agent": self.agent_name})
            return False
    
    def _batch_generate_evidence_narratives(self, valid_tasks: Dict[str, Dict[str, Any]], framework_spec: str) -> str:
        """
        Generate evidence-based narratives for all statistical tasks in a single LLM call.
        
        Args:
            valid_tasks: Dictionary of task_name -> task_result for all valid tasks
            framework_spec: Framework specification for context
            
        Returns:
            Combined evidence narratives for all tasks
        """
        if not valid_tasks:
            return ""
        
        try:
            # Collect evidence for all tasks
            all_task_evidence = {}
            if self.audit_logger:
                self.audit_logger.log_agent_event(self.agent_name, "batch_synthesis_start", {"task_count": len(valid_tasks)})

            for task_name, task_result in valid_tasks.items():
                # Extract provenance information
                provenance = task_result.get("provenance", {})
                input_document_ids = provenance.get("input_document_ids", [])
                input_columns = provenance.get("input_columns", [])
                
                # Determine relevant dimension(s) from input columns
                relevant_dimensions = []
                for col in input_columns:
                    if col.endswith("_score"):
                        dimension = col.replace("_score", "")
                        relevant_dimensions.append(dimension)
                
                if not relevant_dimensions:
                    self.logger.debug(f"No dimensional scores found for task '{task_name}'")
                    continue
                
                # Query for evidence from contributing documents and dimensions
                evidence_pieces = []
                for document_id in input_document_ids[:4]:  # Limit to top 4 contributing documents
                    for dimension in relevant_dimensions[:2]:  # Limit to top 2 dimensions
                        query = EvidenceQuery(
                            document_name=document_id,
                            dimension=dimension,
                            limit=2
                        )
                        results = self._query_evidence(query)
                        evidence_pieces.extend(results)
                
                # Store evidence for this task
                all_task_evidence[task_name] = {
                    "task_result": task_result,
                    "evidence_pieces": evidence_pieces
                }
            
            # Create batch synthesis prompt
            batch_prompt = self._create_batch_synthesis_prompt(all_task_evidence, framework_spec)
            
            # Execute batch synthesis
            response_content, metadata = self.llm_gateway.execute_call(
                model=self.model,
                prompt=batch_prompt
            )

            if self.audit_logger:
                self.audit_logger.log_llm_interaction(
                    model=self.model, prompt=batch_prompt, response=response_content,
                    agent_name=self.agent_name, metadata={"operation": "batch_synthesis"}
                )

            if response_content:
                self.logger.info(f"Batch evidence synthesis successful: processed {len(valid_tasks)} tasks in 1 LLM call")
                return response_content.strip()
            else:
                reason = metadata.get('finish_reason', 'Unknown reason') if metadata else 'No metadata available'
                self.logger.warning(f"Batch synthesis failed: {reason}. Using fallback individual processing.")
                return self._fallback_individual_synthesis(valid_tasks, framework_spec)
                
        except Exception as e:
            self.logger.error(f"Batch evidence synthesis failed: {str(e)}. Using fallback individual processing.")
            if self.audit_logger:
                self.audit_logger.log_error("batch_synthesis_failed", str(e), {"agent": self.agent_name})
            return self._fallback_individual_synthesis(valid_tasks, framework_spec)
    
    def _create_batch_synthesis_prompt(self, all_task_evidence: Dict[str, Dict], framework_spec: str) -> str:
        """Create a comprehensive prompt for batch evidence synthesis."""
        
        task_sections = []
        for task_name, task_data in all_task_evidence.items():
            task_result = task_data["task_result"]
            evidence_pieces = task_data["evidence_pieces"]
            
            if not evidence_pieces:
                continue
                
            # Prepare evidence text for this task
            evidence_text = "\n".join([
                f"  - Document: {ev.document_name}, Dimension: {ev.dimension}, Quote: \"{ev.quote_text}\", Confidence: {ev.confidence}"
                for ev in evidence_pieces
            ])
            
            # Prepare statistical finding summary
            finding_type = task_result.get("type", "unknown")
            finding_summary = f"Type: {finding_type}, Results: {json.dumps(task_result.get('results', {}), indent=2)}"
            
            task_section = f"""
TASK: {task_name}
STATISTICAL FINDING:
{finding_summary}

RETRIEVED EVIDENCE:
{evidence_text}
"""
            task_sections.append(task_section)
        
        batch_prompt = f"""You are a research assistant synthesizing evidence for a computational social science report. Your task is to create evidence-based narratives for multiple statistical findings simultaneously.

FRAMEWORK CONTEXT:
{framework_spec[:1000]}

STATISTICAL FINDINGS AND EVIDENCE:
{''.join(task_sections)}

TASK: For each statistical finding above, write a 2-3 paragraph narrative that establishes the connection between the evidence and the statistical result. Each narrative should:

1. Connect the evidence to the statistical finding
2. Use direct quotes from the evidence  
3. Reference the framework's theoretical foundation
4. Maintain academic tone and precision

Format your response as separate sections for each task, clearly labeled with the task name as a header.

EVIDENCE NARRATIVES:
"""
        return batch_prompt
    
    def _fallback_individual_synthesis(self, valid_tasks: Dict[str, Dict[str, Any]], framework_spec: str) -> str:
        """Fallback to individual synthesis if batch processing fails."""
        self.logger.warning("Using fallback individual synthesis - this will make multiple LLM calls")
        
        narratives = []
        for task_name, task_result in valid_tasks.items():
            narrative = self._generate_evidence_narrative(task_name, task_result, framework_spec)
            if narrative:
                narratives.append(narrative)
        
        return "\n\n".join(narratives)

    def _generate_evidence_narrative(self, task_name: str, task_result: Dict[str, Any], framework_spec: str) -> str:
        """
        Generate evidence-based narrative for a statistical finding.
        
        Args:
            task_name: Name of the statistical task
            task_result: Results from the statistical analysis
            framework_spec: Framework specification for context
            
        Returns:
            Evidence-based narrative or empty string if no evidence found
        """
        try:
            # Extract provenance information
            provenance = task_result.get("provenance", {})
            input_document_ids = provenance.get("input_document_ids", [])
            input_columns = provenance.get("input_columns", [])
            
            # Determine relevant dimension(s) from input columns
            relevant_dimensions = []
            for col in input_columns:
                if col.endswith("_score"):
                    dimension = col.replace("_score", "")
                    relevant_dimensions.append(dimension)
            
            if not relevant_dimensions:
                self.logger.debug(f"No dimensional scores found for task '{task_name}'")
                return ""
            
            # Query for evidence from contributing documents and dimensions
            evidence_pieces = []
            for document_id in input_document_ids[:4]:  # Limit to top 4 contributing documents
                for dimension in relevant_dimensions[:2]:  # Limit to top 2 dimensions
                    query = EvidenceQuery(
                        document_name=document_id,
                        dimension=dimension,
                        limit=2
                    )
                    results = self._query_evidence(query)
                    evidence_pieces.extend(results)
            
            if not evidence_pieces:
                self.logger.warning(f"No evidence found for task '{task_name}' - checked {len(input_document_ids)} docs x {len(relevant_dimensions)} dimensions")
                self.logger.warning(f"Documents: {input_document_ids}")
                self.logger.warning(f"Dimensions: {relevant_dimensions}")
                return ""
            
            # Synthesize narrative using retrieved evidence
            return self._synthesize_evidence_narrative(
                task_name, task_result, evidence_pieces, framework_spec
            )
            
        except Exception as e:
            self.logger.error(f"Failed to generate narrative for task '{task_name}': {str(e)}")
            return ""
    
    def _query_evidence(self, query: EvidenceQuery) -> List[EvidenceResult]:
        """
        Query txtai index for evidence matching the specified criteria.
        
        Args:
            query: Structured evidence query
            
        Returns:
            List of matching evidence results with full provenance
        """
        if not self.embeddings or not self.index_built:
            self.logger.warning("Evidence index not built - cannot query")
            return []
        
        try:
            # Build search query
            search_terms = []
            if query.document_name:
                search_terms.append(query.document_name)
            if query.dimension:
                search_terms.append(query.dimension)
            if query.semantic_query:
                search_terms.append(query.semantic_query)
            
            if not search_terms:
                self.logger.warning("Empty query - no search terms provided")
                return []
            
            search_text = " ".join(search_terms)
            
            # Execute txtai search - returns list of (id, score) tuples
            search_results = self.embeddings.search(search_text, query.limit)
            
            # Convert to EvidenceResult objects
            evidence_results = []
            for result in search_results:
                try:
                    # txtai returns (id, score) tuples
                    if isinstance(result, tuple) and len(result) == 2:
                        doc_id, score = result
                        # Get the document data by ID from our stored documents
                        doc_data = self.documents[doc_id]
                    elif isinstance(result, dict):
                        # Direct document result (less common)
                        doc_data = result
                        score = 1.0
                    else:
                        # Unknown format, skip
                        self.logger.warning(f"Unknown txtai result format: {type(result)}")
                        continue
                        
                except (IndexError, KeyError, TypeError) as e:
                    self.logger.warning(f"Failed to retrieve document for result {result}: {e}")
                    continue
                
                # Filter by metadata if specified
                if query.document_name and doc_data.get("document_name") != query.document_name:
                    continue
                if query.dimension and doc_data.get("dimension") != query.dimension:
                    continue
                
                evidence_results.append(EvidenceResult(
                    quote_text=doc_data.get("quote_text", ""),
                    document_name=doc_data.get("document_name", ""),
                    dimension=doc_data.get("dimension", ""),
                    confidence=doc_data.get("confidence", 0.0),
                    score=score,
                    metadata={
                        "context_type": doc_data.get("context_type", ""),
                        "extraction_method": doc_data.get("extraction_method", "")
                    }
                ))
            
            return evidence_results
            
        except Exception as e:
            self.logger.error(f"Evidence query failed: {str(e)}")
            return []
    
    def _synthesize_evidence_narrative(self, task_name: str, task_result: Dict[str, Any], 
                                     evidence_pieces: List[EvidenceResult], framework_spec: str) -> str:
        """
        Use LLM to synthesize evidence into coherent narrative.
        
        Args:
            task_name: Statistical task name
            task_result: Statistical results
            evidence_pieces: Retrieved evidence pieces
            framework_spec: Framework specification
            
        Returns:
            Synthesized narrative
        """
        if not evidence_pieces:
            return ""
        
        try:
            # Prepare evidence text for LLM
            evidence_text = "\n\n".join([
                f"Document: {ev.document_name}\nDimension: {ev.dimension}\nQuote: \"{ev.quote_text}\"\nConfidence: {ev.confidence}"
                for ev in evidence_pieces
            ])
            
            # Prepare statistical finding summary
            finding_type = task_result.get("type", "unknown")
            finding_summary = f"Task: {task_name}\nType: {finding_type}\nResults: {json.dumps(task_result.get('results', {}), indent=2)}"
            
            # Create synthesis prompt
            prompt = f"""You are a research assistant synthesizing evidence for a computational social science report.

STATISTICAL FINDING:
{finding_summary}

RETRIEVED EVIDENCE (programmatically identified as most relevant):
{evidence_text}

FRAMEWORK CONTEXT:
{framework_spec[:1000]}

TASK: Write a 2-3 paragraph narrative that establishes the connection between this evidence and the statistical finding. Explain how this evidence supports or illustrates the statistical result, using direct quotes and specific references to the framework's analytical dimensions.

Your narrative should:
1. Connect the evidence to the statistical finding
2. Use direct quotes from the evidence
3. Reference the framework's theoretical foundation
4. Maintain academic tone and precision

NARRATIVE:
"""
            
            # Generate synthesis
            response_content, metadata = self.llm_gateway.execute_call(
                model=self.model,
                prompt=prompt
            )
            
            if self.audit_logger:
                self.audit_logger.log_llm_interaction(
                    model=self.model, prompt=prompt, response=response_content,
                    agent_name=self.agent_name, metadata={"operation": "synthesis"}
                )

            if response_content:
                return response_content.strip()
            else:
                reason = metadata.get('finish_reason', 'Unknown reason') if metadata else 'No metadata available'
                self.logger.warning(f"Empty synthesis for task '{task_name}'. Reason: {reason}")
                return f"// No synthesis generated for {task_name}. Reason: {reason}"
                
        except Exception as e:
            self.logger.error(f"Evidence synthesis failed for task '{task_name}': {str(e)}")
            return f"// Error during synthesis for {task_name}: {str(e)}"
    
    def _create_error_response(self, error_message: str) -> TxtaiCurationResponse:
        """Create error response."""
        return TxtaiCurationResponse(
            raw_llm_curation="",
            curation_summary={"error": error_message},
            success=False,
            error_message=error_message
        )

    def build_and_load_index(self, evidence_artifact_hashes: List[str], artifact_storage: LocalArtifactStorage) -> Optional[Embeddings]:
        """
        Builds and loads a txtai index from a list of evidence artifacts.

        Args:
            evidence_artifact_hashes: A list of hashes for the evidence artifacts.
            artifact_storage: The artifact storage system to retrieve evidence.

        Returns:
            A queryable txtai Embeddings object, or None if indexing fails.
        """
        self.logger.info(f"Building RAG index from {len(evidence_artifact_hashes)} evidence artifacts...")
        if not evidence_artifact_hashes:
            self.logger.warning("No evidence artifacts provided for RAG indexing.")
            return None

        try:
            # 1. Prepare documents for indexing
            documents_to_index = []
            doc_id = 0
            all_evidence = self._get_all_evidence(evidence_artifact_hashes, artifact_storage)

            for evidence in all_evidence:
                quote_text = evidence.get('quote_text', '')
                doc_name = evidence.get('document_name', '')
                dimension = evidence.get('dimension', '')
                
                searchable_text = f"Evidence from {doc_name} for {dimension}: {quote_text}"
                
                documents_to_index.append({
                    "id": doc_id,
                    "text": searchable_text,
                    "source_quote": quote_text,
                    "metadata": evidence
                })
                doc_id += 1

            if not documents_to_index:
                self.logger.warning("No valid evidence content found to index.")
                return None

            # 2. Build and return the txtai index
            embeddings = Embeddings()
            embeddings.index(documents_to_index)
            self.index_built = True
            self.logger.info(f"✅ Successfully built RAG index with {len(documents_to_index)} documents.")
            return embeddings

        except Exception as e:
            self.logger.error(f"❌ Failed to build RAG index: {str(e)}")
            if self.audit_logger:
                self.audit_logger.log_error("rag_index_build_failed", str(e), {"agent": self.agent_name})
            return None

    def _get_all_evidence(self, evidence_artifact_hashes: List[str], artifact_storage: LocalArtifactStorage) -> List[Dict[str, Any]]:
        """
        Retrieves and consolidates all evidence from a list of artifact hashes.

        Args:
            evidence_artifact_hashes: A list of hashes for the evidence artifacts.
            artifact_storage: The artifact storage system to retrieve evidence.

        Returns:
            A single list containing all evidence items from all artifacts.
        """
        all_evidence = []
        for artifact_hash in evidence_artifact_hashes:
            try:
                evidence_data = artifact_storage.get_artifact(artifact_hash)
                if evidence_data:
                    evidence_json = json.loads(evidence_data.decode('utf-8'))
                    all_evidence.extend(evidence_json.get('evidence_data', []))
            except Exception as e:
                self.logger.warning(f"Could not process evidence artifact {artifact_hash}: {e}")
        return all_evidence

    def _load_prompt_template(self) -> str:
        """Loads the prompt template for evidence synthesis."""
        # This method is not used in the current code, but is part of the new_code.
        # It would typically load a prompt file or define it directly.
        return """You are a research assistant synthesizing evidence for a computational social science report.

STATISTICAL FINDING:
{finding_summary}

RETRIEVED EVIDENCE (programmatically identified as most relevant):
{evidence_text}

FRAMEWORK CONTEXT:
{framework_spec[:1000]}

TASK: Write a 2-3 paragraph narrative that establishes the connection between this evidence and the statistical finding. Explain how this evidence supports or illustrates the statistical result, using direct quotes and specific references to the framework's analytical dimensions.

Your narrative should:
1. Connect the evidence to the statistical finding
2. Use direct quotes from the evidence
3. Reference the framework's theoretical foundation
4. Maintain academic tone and precision

NARRATIVE:
"""


# Convenience function for backward compatibility
def create_txtai_evidence_curator(model: str, audit_logger=None) -> TxtaiEvidenceCurator:
    """Factory function for creating txtai evidence curator."""
    return TxtaiEvidenceCurator(model=model, audit_logger=audit_logger)
