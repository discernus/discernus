#!/usr/bin/env python3
"""
EvidenceCurator Agent - Intelligent Retrieval Architecture
"""
import json
import logging
import pandas as pd
import os
import re
import yaml
import hashlib
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict

# Import LLM gateway from main codebase
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../..'))
from discernus.gateway.llm_gateway import LLMGateway
from discernus.gateway.model_registry import ModelRegistry
from discernus.core.audit_logger import AuditLogger
from discernus.core.parsing_utils import parse_llm_json_response


@dataclass
class EvidenceCurationRequest:
    """Request structure for evidence curation."""
    statistical_results: Dict[str, Any]
    evidence_data: bytes  # JSON data of the entire evidence pool
    framework_spec: str
    scores_data: bytes # Raw scores data to find drivers of variance

@dataclass
class EvidenceCurationResponse:
    """Response structure containing the synthesized evidence narrative."""
    raw_llm_curation: str  # The final synthesized narrative
    curation_summary: Dict[str, Any]
    success: bool
    error_message: Optional[str] = None
    
    def to_json_serializable(self) -> Dict[str, Any]:
        """Convert to JSON-serializable format for artifact storage."""
        return {
            'raw_llm_curation': self.raw_llm_curation,
            'curation_summary': self.curation_summary,
            'success': self.success,
            'error_message': self.error_message
        }

class EvidenceCurator:
    """
    Selects and synthesizes evidence using an Intelligent Retrieval architecture.
    """
    
    def __init__(self, model: str, audit_logger=None):
        self.model = model
        self.model_registry = ModelRegistry()
        self.llm_gateway = LLMGateway(self.model_registry)
        self.logger = logging.getLogger(__name__)
        self.audit_logger = audit_logger
        self.agent_name = "EvidenceCurator"

        if self.audit_logger:
            self.audit_logger.log_agent_event(self.agent_name, "initialization", {"model": self.model})

    def curate_evidence(self, request: EvidenceCurationRequest, intelligent_index_data: bytes = None) -> EvidenceCurationResponse:
        """
        Main entry point for Two-Stage RAG Intelligent Retrieval.
        
        Stage 1: Use intelligent index to identify candidate evidence IDs
        Stage 2: Use full evidence text to synthesize narrative
        """
        if self.audit_logger:
            self.audit_logger.log_agent_event(self.agent_name, "curation_start", {"model": self.model})
        try:
            if intelligent_index_data is None:
                return self._create_error_response("Intelligent index data is required for RAG-based curation")
            
            # Load the intelligent index
            index_lines = intelligent_index_data.decode('utf-8').strip().split('\n')
            index_entries = [json.loads(line) for line in index_lines if line.strip()]
            
            # Load full evidence for Stage 2
            evidence_df = self._load_evidence_data(request.evidence_data)
            if evidence_df is None:
                return self._create_error_response("Failed to load evidence data")

            synthesized_narratives = []

            # Iterate through both stages of statistical results
            all_results = {
                **request.statistical_results.get("stage_1_raw_data", {}).get("results", {}),
                **request.statistical_results.get("stage_2_derived_metrics", {}).get("results", {})
            }

            for task_name, task_result in all_results.items():
                if "provenance" not in task_result:
                    self.logger.warning(f"Skipping task '{task_name}' due to missing provenance information.")
                    continue

                # Stage 1: Retrieve candidate evidence IDs using the intelligent index
                candidate_ids = self._stage_1_retrieve_candidates(task_name, task_result, index_entries)
                
                if not candidate_ids:
                    self.logger.info(f"No candidate evidence found for task '{task_name}'.")
                    continue
                
                # Stage 2: Synthesize narrative using full evidence text
                narrative = self._stage_2_synthesize_narrative(task_name, task_result, candidate_ids, evidence_df, request.framework_spec)
                
                if narrative:
                    synthesized_narratives.append(narrative)

            final_curation = "\n\n".join(synthesized_narratives)
            
            if self.audit_logger:
                self.audit_logger.log_agent_event(self.agent_name, "curation_success", {"narratives_synthesized": len(synthesized_narratives)})
            return EvidenceCurationResponse(
                raw_llm_curation=final_curation,
                curation_summary={"findings_summarized": len(synthesized_narratives)},
                success=True
            )
            
        except Exception as e:
            self.logger.error(f"Evidence curation failed: {str(e)}")
            if self.audit_logger:
                self.audit_logger.log_error("curation_failed", str(e), {"agent": self.agent_name})
            return self._create_error_response(str(e))
    
    def _load_evidence_data(self, evidence_data: bytes) -> Optional[pd.DataFrame]:
        """Load and validate evidence JSON data."""
        try:
            json_str = evidence_data.decode('utf-8')
            analysis_result = self._parse_json_robust(json_str)

            rows = []
            if 'evidence_data' in analysis_result:
                evidence_list = analysis_result.get('evidence_data', [])
                for i, evidence in enumerate(evidence_list):
                    if isinstance(evidence, dict):
                        rows.append({
                            'aid': evidence.get('document_name', f'doc_{i}'),
                            'dimension': evidence.get('dimension', ''),
                            'quote_text': evidence.get('quote_text', ''),
                            'confidence_score': evidence.get('confidence', 0.0),
                        })
            elif 'document_analyses' in analysis_result:
                for doc_analysis in analysis_result.get('document_analyses', []):
                    document_id = doc_analysis.get('document_id', '{artifact_id}')
                    for i, evidence in enumerate(doc_analysis.get('evidence', [])):
                        if isinstance(evidence, dict):
                            rows.append({
                                'aid': document_id,
                                'dimension': evidence.get('dimension', ''),
                                'quote_text': evidence.get('quote_text', ''),
                                'confidence_score': evidence.get('confidence', 0.0),
                            })
            if not rows:
                return pd.DataFrame()

            return pd.DataFrame(rows)

        except Exception as e:
            self.logger.error(f"Failed to load evidence data: {str(e)}")
            return None

    def _load_scores_data(self, scores_data: bytes) -> Optional[pd.DataFrame]:
        """Loads the scores data from the raw artifact bytes."""
        try:
            from discernus.core.math_toolkit import _json_scores_to_dataframe_thin
            scores_json = json.loads(scores_data.decode('utf-8'))
            return _json_scores_to_dataframe_thin(scores_json)
        except Exception as e:
            self.logger.error(f"Failed to load scores data: {e}")
            return None
    
    def _stage_1_retrieve_candidates(self, task_name: str, task_result: Dict[str, Any], index_entries: List[Dict]) -> List[str]:
        """
        Stage 1: Use LLM to identify candidate evidence IDs from the intelligent index.
        """
        finding_type = task_result.get("type", "unknown")
        provenance = task_result.get("provenance", {})
        
        # Determine the relevant dimension(s) from provenance
        input_columns = provenance.get("input_columns", [])
        relevant_dimensions = []
        for col in input_columns:
            if col.endswith("_score"):
                dimension = col.replace("_score", "")
                relevant_dimensions.append(dimension)
        
        if not relevant_dimensions:
            return []
        
        # Filter index entries to relevant dimensions first (simple optimization)
        relevant_entries = [entry for entry in index_entries if entry.get("dim") in relevant_dimensions]
        
        if not relevant_entries:
            return []
        
        # Prepare the index for LLM consumption
        index_text = "\n".join([json.dumps(entry) for entry in relevant_entries])
        
        # Create the Stage 1 prompt
        prompt = f"""You are a research assistant performing evidence retrieval. 

TASK: A statistical analysis found the following result:
- Task: {task_name}
- Type: {finding_type}
- Dimensions: {', '.join(relevant_dimensions)}

EVIDENCE INDEX: Here is an index of available evidence summaries:
{index_text}

INSTRUCTIONS: Review the evidence summaries and keywords. Identify the top 5 most relevant pieces of evidence that would best explain or support this statistical finding. 

Respond with a JSON array of evidence IDs only:
["id1", "id2", "id3", "id4", "id5"]
"""
        
        try:
            response_content, _ = self.llm_gateway.execute_call(
                model=self.model,
                prompt=prompt,
                max_tokens=200,
                json_mode=True
            )
            
            if self.audit_logger:
                self.audit_logger.log_llm_interaction(
                    model=self.model, prompt=prompt, response=response_content,
                    agent_name=self.agent_name, metadata={"operation": "stage_1_retrieval"}
                )
            candidate_ids = json.loads(response_content)
            if isinstance(candidate_ids, list):
                return candidate_ids[:5]  # Limit to top 5
            else:
                return []
                
        except Exception as e:
            self.logger.error(f"Stage 1 retrieval failed for task '{task_name}': {e}")
            if self.audit_logger:
                self.audit_logger.log_error("stage_1_retrieval_failed", str(e), {"agent": self.agent_name})
            return []

    def _retrieve_for_descriptive_stats(self, provenance: Dict[str, Any], evidence_df: pd.DataFrame, scores_df: pd.DataFrame) -> pd.DataFrame:
        """
        Retrieval strategy for descriptive statistics. Finds the drivers of variance.
        """
        if not provenance.get("input_columns"):
            return pd.DataFrame()
            
        # Find the first dimension column that ends with _score
        input_columns = provenance.get("input_columns", [])
        dimension = None
        for col in input_columns:
            if col.endswith("_score"):
                dimension = col
                break
                
        if not dimension:
            return pd.DataFrame()

        # Handle small N: if less than 6 docs, use all of them.
        if len(scores_df) < 6:
            doc_ids = scores_df['aid'].unique().tolist()
        else:
            top_docs = scores_df.nlargest(3, dimension)
            bottom_docs = scores_df.nsmallest(3, dimension)
            high_variance_docs = pd.concat([top_docs, bottom_docs])
            doc_ids = high_variance_docs['aid'].unique().tolist()

        dimension_name_only = dimension.replace("_score", "")
        retrieved = evidence_df[
            (evidence_df['aid'].isin(doc_ids)) &
            (evidence_df['dimension'] == dimension_name_only)
        ]
        return retrieved

    def _stage_2_synthesize_narrative(self, task_name: str, task_result: Dict[str, Any], candidate_ids: List[str], evidence_df: pd.DataFrame, framework_spec: str) -> str:
        """
        Stage 2: Use LLM to synthesize narrative from full evidence text of candidates.
        """
        # Retrieve full evidence text for the candidate IDs
        # We need to map the candidate IDs back to the original evidence
        # The candidate IDs are based on the row hash, so we need to recreate them
        candidate_evidence = []
        
        for _, row in evidence_df.iterrows():
            # Recreate the ID using the same logic as the indexer
            row_id = f"evd_{hashlib.sha1(str(row).encode()).hexdigest()[:10]}"
            if row_id in candidate_ids:
                candidate_evidence.append({
                    'document_id': row['aid'],  # Use 'aid' which maps to document_name
                    'dimension': row['dimension'],
                    'quote_text': row['quote_text'],
                    'reasoning': row.get('reasoning', '')
                })
        
        if not candidate_evidence:
            return ""
        
        # Create the Stage 2 prompt with full evidence text
        finding_summary = f"Task: {task_name}\nType: {task_result.get('type', 'unknown')}\nResult: {json.dumps(task_result.get('results', {}), indent=2)}"
        evidence_text = "\n\n".join([
            f"Document: {ev['document_id']}\nDimension: {ev['dimension']}\nQuote: \"{ev['quote_text']}\"\nReasoning: {ev['reasoning']}"
            for ev in candidate_evidence
        ])
        
        prompt = f"""You are a research assistant synthesizing evidence for a computational social science report.

STATISTICAL FINDING:
{finding_summary}

RETRIEVED EVIDENCE (programmatically identified as most relevant):
{evidence_text}

FRAMEWORK CONTEXT:
{framework_spec[:1000]}

TASK: Write a 2-3 paragraph narrative that establishes the CAUSAL LINK between this evidence and the statistical finding. Explain WHY this evidence led to the statistical result, using direct quotes and specific references to the framework's analytical dimensions.

Your narrative should:
1. Explicitly connect the evidence to the statistical finding
2. Use direct quotes from the evidence
3. Reference the framework's theoretical foundation
4. Explain the causal mechanism behind the result

NARRATIVE:
"""
        
        try:
            response_content, metadata = self.llm_gateway.execute_call(
                model=self.model,
                prompt=prompt
            )
            if self.audit_logger:
                self.audit_logger.log_llm_interaction(
                    model=self.model, prompt=prompt, response=response_content,
                    agent_name=self.agent_name, metadata={"operation": "stage_2_synthesis"}
                )
            if response_content:
                return response_content
            else:
                reason = metadata.get('finish_reason', 'Unknown reason') if metadata else 'No metadata available'
                self.logger.warning(f"Empty synthesis for task '{task_name}'. Reason: {reason}")
                return f"// No synthesis could be generated for {task_name}. Reason: {reason}"
        except Exception as e:
            self.logger.error(f"Stage 2 synthesis failed for task '{task_name}': {e}")
            if self.audit_logger:
                self.audit_logger.log_error("stage_2_synthesis_failed", str(e), {"agent": self.agent_name})
            return f"// Error during synthesis for {task_name}: {e}"

    def _create_error_response(self, error_message: str) -> EvidenceCurationResponse:
        return EvidenceCurationResponse(
            raw_llm_curation="",
            curation_summary={"error": error_message},
            success=False,
            error_message=error_message
        )

    def _parse_json_robust(self, json_str: str) -> Dict[str, Any]:
        """
        BUG #326 THIN FIX: Use LLM intelligence to handle malformed JSON instead of complex parsing.
        """
        try:
            return parse_llm_json_response(
                response=json_str,
                llm_gateway=self.llm_gateway,
                model=self.model,
                audit_logger=self.audit_logger
            )
        except (json.JSONDecodeError, ValueError) as e:
            self.logger.error(f"Robust JSON parsing failed after all fallbacks: {e}")
            return {}
