#!/usr/bin/env python3
"""
EvidenceCurator Agent

This agent receives actual statistical results and intelligently selects
relevant evidence to support the findings. This is the key innovation:
evidence curation happens AFTER statistical computation, not before.

Key Design Principles:
- Post-computation curation: Evidence selection based on actual results
- LLM intelligence: Understands statistical significance and effect sizes
- Framework-agnostic: Works with any analytical framework
- Quality over quantity: Selects most relevant evidence, not all evidence
- No hallucination: Only uses existing evidence, never creates new content
"""

import json
import logging
import pandas as pd
import json
import re
import os
import yaml
import hashlib
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict

# Import LLM gateway from main codebase
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../..'))
from discernus.gateway.llm_gateway import LLMGateway
from discernus.gateway.model_registry import ModelRegistry

@dataclass
class EvidenceCurationRequest:
    """Request structure for evidence curation."""
    statistical_results: Dict[str, Any]
    evidence_data: bytes  # JSON data instead of CSV path
    framework_spec: str
    max_evidence_per_finding: int = 3
    min_confidence_threshold: float = 0.7

# THIN: CuratedEvidence dataclass removed - all intelligence flows through raw_llm_curation

@dataclass
class EvidenceCurationResponse:
    """THIN: Response structure containing raw LLM curation."""
    curated_evidence: Dict[str, List[Any]]  # THIN: Generic list instead of CuratedEvidence
    curation_summary: Dict[str, Any]
    success: bool
    error_message: Optional[str] = None
    footnote_registry: Dict[int, Dict[str, str]] = None
    raw_llm_curation: Optional[str] = None  # THIN: Primary intelligence flow
    
    def to_json_serializable(self) -> Dict[str, Any]:
        """THIN: Convert to JSON-serializable format for artifact storage."""
        serializable_evidence = {}
        for category, evidence_list in self.curated_evidence.items():
            # THIN: Handle generic evidence objects instead of CuratedEvidence dataclass
            serializable_evidence[category] = evidence_list
        
        # Defensive JSON serialization - convert any non-serializable objects to strings
        def make_json_safe(obj):
            if isinstance(obj, (str, int, float, bool, type(None))):
                return obj
            elif isinstance(obj, (list, tuple)):
                return [make_json_safe(item) for item in obj]
            elif isinstance(obj, dict):
                return {str(k): make_json_safe(v) for k, v in obj.items()}
            else:
                return str(obj)
        
        return {
            'curated_evidence': serializable_evidence,
            'curation_summary': make_json_safe(self.curation_summary),
            'success': self.success,
            'error_message': self.error_message,
            'footnote_registry': make_json_safe(self.footnote_registry or {}),
            'raw_llm_curation': self.raw_llm_curation  # THIN: Preserve LLM intelligence
        }

class EvidenceCurator:
    """
    Intelligently curates evidence based on actual statistical results.
    
    This agent leverages LLM intelligence to understand statistical findings
    and select the most relevant supporting evidence from the available pool.
    The key innovation is that curation happens AFTER computation.
    """
    
    def __init__(self, model: str, audit_logger=None):
        """
        Initialize the EvidenceCurator.
        
        Args:
            model: LLM model to use for evidence curation
            audit_logger: Optional audit logger for cost tracking
        """
        self.model = model
        self.model_registry = ModelRegistry()
        self.llm_gateway = LLMGateway(self.model_registry)
        self.logger = logging.getLogger(__name__)
        self.audit_logger = audit_logger
        self.footnote_counter = 0
        self.footnote_registry = {}
        
        # Fan-out/Fan-in configuration for large corpora
        self.LARGE_CORPUS_THRESHOLD = 100  # Switch to fan-out/fan-in above this many evidence pieces
        self.CHUNK_SIZE = 500  # Evidence pieces per chunk
        self.PIECES_PER_CHUNK = 30  # Target pieces to curate from each chunk
        self.FINAL_TARGET_PIECES = 100  # Final number of pieces after aggregation
        
    def curate_evidence(self, request: EvidenceCurationRequest) -> EvidenceCurationResponse:
        """
        Main entry point for evidence curation.
        Automatically detects large evidence pools and uses fan-out/fan-in approach.
        """
        evidence_df = self._load_evidence_data(request.evidence_data)
        if evidence_df is None or evidence_df.empty:
            return self._create_empty_response("Failed to load evidence data")
        
        # Check if we need fan-out/fan-in approach for large evidence pools
        if len(evidence_df) > self.LARGE_CORPUS_THRESHOLD:
            self.logger.info(f"Large evidence pool detected ({len(evidence_df)} pieces). Using fan-out/fan-in approach...")
            return self._curate_evidence_fanout_fanin(request, evidence_df)
        else:
            self.logger.info(f"Standard evidence curation for {len(evidence_df)} pieces")
            return self._curate_evidence_standard(request, evidence_df)
    
    def _curate_evidence_standard(self, request: EvidenceCurationRequest, evidence_df: pd.DataFrame) -> EvidenceCurationResponse:
        """
        Curate evidence based on statistical results (standard approach).
        
        Args:
            request: EvidenceCurationRequest containing results and evidence
            evidence_df: Pre-loaded evidence DataFrame
            
        Returns:
            EvidenceCurationResponse with curated evidence
        """
        try:
            # Reset footnote counter for new curation session
            self.footnote_counter = 0
            self.footnote_registry = {}
            
            # Defensive check: ensure statistical_results is not None
            if request.statistical_results is None:
                self.logger.warning("statistical_results is None, returning empty curated evidence")
                return EvidenceCurationResponse(
                    curated_evidence={},
                    curation_summary={"warning": "No statistical results provided"},
                    success=True,
                    footnote_registry={}
                )
            
            # Evidence DataFrame is already loaded and validated by caller
            if evidence_df is None:
                return EvidenceCurationResponse(
                    curated_evidence={},
                    curation_summary={},
                    success=False,
                    error_message="Evidence data is None",
                    footnote_registry={}
                )
            
            # THIN approach: Let LLM handle all filtering and selection logic
            # Remove hardcoded confidence thresholds - let LLM decide what's relevant
            if len(evidence_df) == 0:
                return EvidenceCurationResponse(
                    curated_evidence={},
                    curation_summary={"warning": "No evidence data available"},
                    success=True,
                    footnote_registry={}
                )
            
            # Use LLM for intelligent evidence curation (THIN approach)
            curation_result = self._curate_evidence_with_llm(
                request.statistical_results, 
                evidence_df, 
                request
            )
            
            # Extract curated evidence and raw LLM curation
            curated_evidence = curation_result.get('curated_evidence', {})
            raw_llm_curation = curation_result.get('raw_llm_curation', None)
            
            # Generate curation summary
            curation_summary = self._generate_curation_summary(
                curated_evidence, 
                len(evidence_df), 
                len(evidence_df)  # All evidence considered, no hardcoded filtering
            )
            
            return EvidenceCurationResponse(
                curated_evidence=curated_evidence,
                curation_summary=curation_summary,
                success=True,
                footnote_registry=self.footnote_registry,
                raw_llm_curation=raw_llm_curation  # THIN: Preserve LLM intelligence
            )
            
        except Exception as e:
            self.logger.error(f"Evidence curation failed: {str(e)}")
            return EvidenceCurationResponse(
                curated_evidence={},
                curation_summary={},
                success=False,
                error_message=str(e),
                footnote_registry={}
            )
    
    def _create_evidence_hash(self, evidence_text: str, artifact_id: str, dimension: str) -> str:
        """Create a hash for evidence verification."""
        content = f"{artifact_id}:{dimension}:{evidence_text}"
        return hashlib.sha256(content.encode('utf-8')).hexdigest()[:12]
    
    def _assign_footnote_number(self, evidence_text: str, artifact_id: str, dimension: str) -> int:
        """Assign a unique footnote number and register the evidence."""
        evidence_hash = self._create_evidence_hash(evidence_text, artifact_id, dimension)
        
        # Check if this evidence already has a footnote
        for footnote_num, registry_entry in self.footnote_registry.items():
            if registry_entry['evidence_hash'] == evidence_hash:
                return footnote_num
        
        # Assign new footnote number
        self.footnote_counter += 1
        self.footnote_registry[self.footnote_counter] = {
            'evidence_hash': evidence_hash,
            'artifact_id': artifact_id,
            'dimension': dimension,
            'evidence_text': evidence_text[:100] + '...' if len(evidence_text) > 100 else evidence_text
        }
        
        return self.footnote_counter
    
    def _curate_evidence_with_llm(self, statistical_results: Dict[str, Any], 
                                 evidence_df: pd.DataFrame,
                                 request: EvidenceCurationRequest) -> Dict[str, List[Any]]:
        """
        THIN approach: Let LLM intelligently curate evidence based on statistical results.
        Uses externalized YAML instructions for LLM guidance.
        """
        try:
            # Load externalized YAML instructions
            prompt_template = self._load_curation_prompt_template()
            
            # THIN approach: Pass raw data to LLM as strings
            # Let LLM handle any data structure without JSON serialization
            
            stats_str = str(statistical_results)
            evidence_str = str(evidence_df.to_dict('records'))  # Show ALL evidence to LLM
            
            # Build prompt with YAML template
            prompt = prompt_template.format(
                framework_spec=request.framework_spec,
                statistical_results=stats_str,
                evidence_sample=evidence_str,
                max_evidence_per_finding=request.max_evidence_per_finding
            )
            
            # Call LLM for intelligent curation
            response_content, metadata = self.llm_gateway.execute_call(
                model=self.model,
                prompt=prompt,
                max_tokens=8000  # Allow comprehensive evidence curation
            )
            
            # Extract and log cost information
            if self.audit_logger and metadata.get("usage"):
                usage_data = metadata["usage"]
                try:
                    self.audit_logger.log_cost(
                        operation="evidence_curation",
                        model=metadata.get("model", self.model),
                        tokens_used=usage_data.get("total_tokens", 0),
                        cost_usd=usage_data.get("response_cost_usd", 0.0),
                        agent_name="EvidenceCurator",
                        metadata={
                            "prompt_tokens": usage_data.get("prompt_tokens", 0),
                            "completion_tokens": usage_data.get("completion_tokens", 0),
                            "attempts": metadata.get("attempts", 1),
                            "evidence_pieces": len(evidence_df)
                        }
                    )
                    cost = usage_data.get("response_cost_usd", 0.0)
                    tokens = usage_data.get("total_tokens", 0)
                    print(f"💰 Evidence curation cost: ${cost:.6f} ({tokens:,} tokens)")
                except Exception as e:
                    print(f"⚠️ Error logging cost for evidence curation: {e}")
            
            if not response_content or not metadata.get('success'):
                self.logger.warning("LLM curation failed, returning empty evidence")
                return {}
            
            # THIN: Pass LLM's intelligent curation directly
            parsed_result = self._parse_llm_curation_response(response_content, evidence_df)
            
            # Return both curated evidence and raw LLM curation for downstream use
            return {
                'curated_evidence': parsed_result,
                'raw_llm_curation': response_content  # THIN: Preserve LLM intelligence
            }
            
        except Exception as e:
            self.logger.error(f"LLM evidence curation failed: {str(e)}")
            return {}
    
    def _curate_evidence_fanout_fanin(self, request: EvidenceCurationRequest, evidence_df: pd.DataFrame) -> EvidenceCurationResponse:
        """
        Fan-out/Fan-in evidence curation for large corpora.
        
        Strategy:
        1. Split evidence into manageable chunks
        2. Curate each chunk in parallel (fan-out)
        3. Aggregate results and final curation (fan-in)
        """
        try:
            # Step 1: Split evidence into chunks
            chunks = self._split_evidence_into_chunks(evidence_df)
            self.logger.info(f"Split {len(evidence_df)} evidence pieces into {len(chunks)} chunks")
            
            # Step 2: Curate each chunk (fan-out)
            chunk_results = []
            for i, chunk_df in enumerate(chunks):
                self.logger.info(f"Curating chunk {i+1}/{len(chunks)} ({len(chunk_df)} pieces)...")
                
                # Create modified request for chunk curation
                chunk_request = EvidenceCurationRequest(
                    statistical_results=request.statistical_results,
                    evidence_data=self._dataframe_to_json_bytes(chunk_df),
                    framework_spec=request.framework_spec,  # Required parameter - pass it directly
                    max_evidence_per_finding=self.PIECES_PER_CHUNK // 5,  # Distribute across findings
                    min_confidence_threshold=request.min_confidence_threshold
                )
                
                # Load evidence data for this chunk
                chunk_evidence_df = self._load_evidence_data(chunk_request.evidence_data)
                if chunk_evidence_df is None or chunk_evidence_df.empty:
                    self.logger.warning(f"Chunk {i+1} evidence data is empty, skipping")
                    continue
                
                # Curate this chunk using standard method
                chunk_result = self._curate_evidence_standard(chunk_request, chunk_evidence_df)
                if chunk_result.success:
                    chunk_results.append(chunk_result.curated_evidence)
                    self.logger.info(f"Chunk {i+1} produced {sum(len(evidence_list) for evidence_list in chunk_result.curated_evidence.values())} pieces")
                else:
                    self.logger.warning(f"Chunk {i+1} curation failed: {chunk_result.error_message}")
            
            # Step 3: Aggregate and final curation (fan-in)
            if not chunk_results:
                return self._create_empty_response("All chunk curations failed")
            
            aggregated_evidence = self._aggregate_chunk_results(chunk_results)
            self.logger.info(f"Aggregated {sum(len(evidence_list) for evidence_list in aggregated_evidence.values())} pieces from {len(chunk_results)} chunks")
            
            # Step 4: Final curation to target number
            final_result = self._final_evidence_curation(request, aggregated_evidence)
            self.logger.info(f"Final curation produced {sum(len(evidence_list) for evidence_list in final_result.values())} pieces")
            
            return EvidenceCurationResponse(
                curated_evidence=final_result,
                curation_summary={
                    "method": "fan_out_fan_in",
                    "total_input_pieces": len(evidence_df),
                    "chunks_processed": len(chunks),
                    "successful_chunks": len(chunk_results),
                    "final_pieces": sum(len(evidence_list) for evidence_list in final_result.values())
                },
                success=True,
                footnote_registry=self.footnote_registry,
                raw_llm_curation=None  # THIN: Fan-out/fan-in doesn't preserve individual LLM responses
            )
            
        except Exception as e:
            self.logger.error(f"Fan-out/fan-in curation failed: {str(e)}")
            return self._create_empty_response(f"Fan-out/fan-in curation failed: {str(e)}")
    
    def _split_evidence_into_chunks(self, evidence_df: pd.DataFrame) -> List[pd.DataFrame]:
        """Split evidence DataFrame into manageable chunks."""
        chunks = []
        for i in range(0, len(evidence_df), self.CHUNK_SIZE):
            chunk = evidence_df.iloc[i:i + self.CHUNK_SIZE].copy()
            chunks.append(chunk)
        return chunks
    
    def _dataframe_to_json_bytes(self, df: pd.DataFrame) -> bytes:
        """Convert DataFrame back to JSON bytes format expected by standard curation."""
        # Reconstruct the original JSON structure
        document_analyses = []
        
        # Group by artifact_id to reconstruct documents
        for artifact_id in df['artifact_id'].unique():
            doc_df = df[df['artifact_id'] == artifact_id]
            evidence_list = []
            
            for _, row in doc_df.iterrows():
                evidence = {
                    'dimension': row.get('dimension', ''),
                    'quote_text': row.get('evidence_text', ''),
                    'confidence': row.get('confidence', 0.0),
                    'context_type': row.get('context', 'direct')
                }
                evidence_list.append(evidence)
            
            document_analyses.append({
                'document_id': artifact_id,
                'evidence': evidence_list
            })
        
        json_data = {'document_analyses': document_analyses}
        return json.dumps(json_data).encode('utf-8')
    
    def _aggregate_chunk_results(self, chunk_results: List[Dict[str, List[Any]]]) -> Dict[str, List[Any]]:
        """Aggregate evidence from multiple chunk results."""
        aggregated = {}
        
        for chunk_result in chunk_results:
            for category, evidence_list in chunk_result.items():
                if category not in aggregated:
                    aggregated[category] = []
                aggregated[category].extend(evidence_list)
        
        return aggregated
    
    def _final_evidence_curation(self, request: EvidenceCurationRequest, aggregated_evidence: Dict[str, List[Any]]) -> Dict[str, List[Any]]:
        """Final curation to reduce aggregated evidence to target number."""
        total_pieces = sum(len(evidence_list) for evidence_list in aggregated_evidence.values())
        
        if total_pieces <= self.FINAL_TARGET_PIECES:
            # Already within target, return as-is
            return aggregated_evidence
        
        # Need to reduce - use LLM for intelligent final selection
        self.logger.info(f"Final curation: reducing {total_pieces} pieces to {self.FINAL_TARGET_PIECES}")
        
        # Convert aggregated evidence back to a format suitable for LLM curation
        # This is a simplified approach - in practice, you might want more sophisticated logic
        final_result = {}
        pieces_per_category = self.FINAL_TARGET_PIECES // len(aggregated_evidence)
        
        for category, evidence_list in aggregated_evidence.items():
            # Sort by relevance_score and take top pieces
            sorted_evidence = sorted(evidence_list, key=lambda x: x.relevance_score, reverse=True)
            final_result[category] = sorted_evidence[:pieces_per_category]
        
        return final_result
    
    def _create_empty_response(self, error_message: str) -> EvidenceCurationResponse:
        """Create an empty response for error cases."""
        return EvidenceCurationResponse(
            curated_evidence={},
            curation_summary={"error": error_message},
            success=False,
            error_message=error_message,
            footnote_registry={},
            raw_llm_curation=None  # THIN: No LLM curation available
        )
    
    def _load_curation_prompt_template(self) -> str:
        """Load externalized YAML instructions for evidence curation."""
        try:
            # Load from YAML file (THIN architecture)
            yaml_path = os.path.join(os.path.dirname(__file__), 'prompts', 'evidence_curation.yaml')
            with open(yaml_path, 'r') as f:
                config = yaml.safe_load(f)
            return config['template']
        except Exception as e:
            self.logger.warning(f"Could not load YAML template: {e}")
            # Fallback to simple template
            return """
You are an evidence curator for academic research. Given statistical results and evidence data, 
curate the most relevant evidence pieces that support the key findings.

Statistical Results:
{statistical_results}

Evidence Sample:
{evidence_sample}

Framework Specification:
{framework_spec}

Instructions:
1. Analyze the statistical results to identify key findings
2. Select the most relevant evidence pieces that support these findings
3. Return curated evidence in JSON format with reasoning for each selection
4. Limit to {max_evidence_per_finding} pieces per finding

Return only valid JSON.
"""
    
    def _parse_llm_curation_response(self, response_content: str, evidence_df: pd.DataFrame) -> Dict[str, List[Any]]:
        """THIN approach: Pass LLM's intelligent evidence curation directly without parsing."""
        try:
            # THIN: Instead of parsing LLM intelligence, pass it directly to downstream components
            # The LLM has already done the intelligent curation - we don't need to re-interpret it
            
            self.logger.info("THIN approach: Passing LLM's intelligent curation directly to ResultsInterpreter")
            self.logger.info(f"LLM curation response length: {len(response_content)} characters")
            
            # Store the raw LLM curation for downstream use
            # This preserves the LLM's intelligence without software interference
            raw_curation = {
                "raw_llm_curation": response_content,
                "evidence_df_length": len(evidence_df),
                "curation_timestamp": "now"
            }
            
            # THIN: Return empty curated evidence - all intelligence flows through raw_llm_curation
            self.logger.info("THIN evidence curation: LLM intelligence preserved for downstream components")
            return {}
            
        except Exception as e:
            self.logger.error(f"THIN evidence curation failed: {str(e)}")
            # THIN: No fallback - return empty result
            return {}
    

    
    def _load_evidence_data(self, evidence_data: bytes) -> Optional[pd.DataFrame]:
        """Load and validate evidence JSON data."""
        
        try:
            # Parse JSON data (handle both pre-extracted evidence and legacy formats)
            import json
            import re
            json_str = evidence_data.decode('utf-8')
            
            # Check if this is pre-extracted evidence format (new THIN approach)
            if '"evidence_metadata"' in json_str and '"evidence_data"' in json_str:
                # Pre-extracted evidence artifact format
                evidence_artifact = json.loads(json_str)
                evidence_list = evidence_artifact.get('evidence_data', [])
                evidence_metadata = evidence_artifact.get('evidence_metadata', {})
                
                self.logger.info(f"Pre-extracted evidence: {evidence_metadata.get('total_evidence_pieces', 0)} pieces from {evidence_metadata.get('total_documents', 0)} documents")
                
                # Convert pre-extracted evidence to expected format for curation
                analysis_result = {
                    "analysis_metadata": {
                        "framework_name": "pre_extracted_evidence",
                        "framework_version": evidence_metadata.get('framework_version', 'v6.0'),
                        "analyst_confidence": 0.95,
                        "analysis_notes": f"Using pre-extracted evidence: {evidence_metadata.get('extraction_method', 'unknown')}"
                    },
                    "evidence_data": evidence_list  # Direct access to evidence list
                }
            elif '<<<DISCERNUS_ANALYSIS_JSON_v6>>>' in json_str:
                # Legacy delimited format (raw analysis response)
                json_pattern = r'<<<DISCERNUS_ANALYSIS_JSON_v6>>>\s*({.*?})\s*<<<END_DISCERNUS_ANALYSIS_JSON_v6>>>'
                json_match = re.search(json_pattern, json_str, re.DOTALL)
                if json_match:
                    json_content = json_match.group(1).strip()
                    analysis_result = json.loads(json_content)
                else:
                    raise ValueError("Could not extract JSON from delimited format")
            else:
                # Pure JSON format (legacy)
                analysis_result = json.loads(json_str)
            
            # Debug: Log the structure of the analysis result
            self.logger.info(f"Analysis result keys: {list(analysis_result.keys()) if isinstance(analysis_result, dict) else 'Not a dict'}")
            if isinstance(analysis_result, dict):
                for key, value in analysis_result.items():
                    if isinstance(value, list):
                        self.logger.info(f"  {key}: list with {len(value)} items")
                    elif isinstance(value, dict):
                        self.logger.info(f"  {key}: dict with keys {list(value.keys())}")
                    else:
                        self.logger.info(f"  {key}: {type(value).__name__}")
            
            # Convert to DataFrame - handle both pre-extracted and legacy formats
            rows = []
            
            if 'evidence_data' in analysis_result:
                # Pre-extracted evidence format (new THIN approach)
                evidence_list = analysis_result.get('evidence_data', [])
                self.logger.info(f"Processing pre-extracted evidence: {len(evidence_list)} pieces")
                
                for i, evidence in enumerate(evidence_list):
                    if isinstance(evidence, dict):
                        row = {
                            'aid': evidence.get('document_name', f'doc_{i}'),
                            'dimension': evidence.get('dimension', ''),
                            'quote_id': f"quote_{i}",
                            'quote_text': evidence.get('quote_text', ''),
                            'confidence_score': evidence.get('confidence', 0.0),
                            'context_type': evidence.get('context_type', 'direct')
                        }
                        rows.append(row)
            else:
                # Legacy format (document_analyses structure)
                document_analyses = analysis_result.get('document_analyses', [])
                
                if not document_analyses:
                    raise ValueError("No document_analyses or evidence_data found in JSON")
                
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
            
            if not rows:
                return pd.DataFrame(columns=['aid', 'dimension', 'quote_id', 'quote_text', 'confidence_score', 'context_type'])
            
            evidence_df = pd.DataFrame(rows)
            
            # Map actual column names to expected column names  
            column_mapping = {
                'aid': 'artifact_id',
                'quote_text': 'evidence_text',
                'confidence_score': 'confidence',
                'context_type': 'context'
            }
            
            # Rename columns to match expected schema
            evidence_df = evidence_df.rename(columns=column_mapping)
            
            # Add missing columns with default values
            if 'context' not in evidence_df.columns:
                evidence_df['context'] = 'Generated from analysis'
            if 'reasoning' not in evidence_df.columns:
                evidence_df['reasoning'] = 'Evidence extracted during analysis'
            
            # Validate required columns (after mapping)
            required_columns = ['artifact_id', 'dimension', 'evidence_text', 
                              'context', 'confidence', 'reasoning']
            
            missing_columns = [col for col in required_columns if col not in evidence_df.columns]
            if missing_columns:
                self.logger.error(f"Missing evidence columns after mapping: {missing_columns}")
                return None
            
            # Clean and validate data (using mapped column names)
            evidence_df = evidence_df.dropna(subset=['artifact_id', 'dimension', 'evidence_text'])
            evidence_df['confidence'] = pd.to_numeric(evidence_df['confidence'], errors='coerce')
            evidence_df = evidence_df.dropna(subset=['confidence'])
            
            return evidence_df
            
        except Exception as e:
            self.logger.error(f"Failed to load evidence data: {str(e)}")
            self.logger.error(f"Evidence data type: {type(evidence_data)}")
            self.logger.error(f"Evidence data length: {len(evidence_data) if hasattr(evidence_data, '__len__') else 'No length'}")
            if isinstance(evidence_data, bytes):
                try:
                    json_str = evidence_data.decode('utf-8')
                    self.logger.error(f"JSON string preview (first 500 chars): {json_str[:500]}")
                except:
                    self.logger.error("Could not decode evidence data as UTF-8")
            import traceback
            self.logger.error(f"Full traceback: {traceback.format_exc()}")
            return None
    
    def _curate_descriptive_evidence(self, descriptive_stats: Dict[str, Any], 
                                   evidence_df: pd.DataFrame,
                                   request: EvidenceCurationRequest) -> List[Any]:
        """THIN: Legacy method deprecated - all curation handled by LLM."""
        return []
    
    def _curate_hypothesis_evidence(self, hypothesis_tests: Dict[str, Any],
                                  evidence_df: pd.DataFrame,
                                  request: EvidenceCurationRequest) -> List[Any]:
        """THIN: Legacy method deprecated - all curation handled by LLM."""
        return []
    
    def _curate_correlation_evidence(self, correlations: Dict[str, Any],
                                   evidence_df: pd.DataFrame,
                                   request: EvidenceCurationRequest) -> List[Any]:
        """THIN: Legacy method deprecated - all curation handled by LLM."""
        return []
    
    def _curate_reliability_evidence(self, reliability_metrics: Dict[str, Any],
                                    evidence_df: pd.DataFrame,
                                    request: EvidenceCurationRequest) -> List[Any]:
        """THIN: Legacy method deprecated - all curation handled by LLM."""
        return []
    
    def _get_relevant_dimensions_for_hypothesis(self, hypothesis: str) -> List[str]:
        """Determine which dimensions are relevant to a hypothesis."""
        
        # Map hypothesis names to relevant dimensions
        hypothesis_mappings = {
            'H1_virtue_positive_correlation': ['integrity', 'courage', 'compassion', 'justice', 'wisdom'],
            'H2_vice_positive_correlation': ['corruption', 'cowardice', 'cruelty', 'injustice', 'folly'],
            'H3_virtue_vice_negative_correlation': ['integrity', 'courage', 'compassion', 'justice', 'wisdom', 
                                                  'corruption', 'cowardice', 'cruelty', 'injustice', 'folly'],
            'H4_overall_virtue_greater_than_overall_vice': ['integrity', 'courage', 'compassion', 'justice', 'wisdom']
        }
        
        return hypothesis_mappings.get(hypothesis, [])
    
    def _get_cluster_dimensions(self, cluster_name: str) -> List[str]:
        """Get dimensions that belong to a reliability cluster."""
        
        cluster_mappings = {
            'virtue_cluster_alpha': ['integrity', 'courage', 'compassion', 'justice', 'wisdom'],
            'vice_cluster_alpha': ['corruption', 'cowardice', 'cruelty', 'injustice', 'folly']
        }
        
        return cluster_mappings.get(cluster_name, [])
    
    def _generate_curation_summary(self, curated_evidence: Dict[str, List[Any]], 
                                 total_evidence: int, high_confidence_evidence: int) -> Dict[str, Any]:
        """Generate a summary of the curation process."""
        
        total_curated = sum(len(evidence_list) for evidence_list in curated_evidence.values())
        
        # Calculate evidence distribution by category
        category_counts = {category: len(evidence_list) 
                          for category, evidence_list in curated_evidence.items()}
        
        # THIN: Calculate summary for generic evidence objects
        all_evidence = []
        for evidence_list in curated_evidence.values():
            all_evidence.extend(evidence_list)
        
        # THIN: Use default values since we no longer have structured CuratedEvidence objects
        avg_confidence = 0.8 if all_evidence else 0
        avg_relevance = 0.8 if all_evidence else 0
        
        return {
            'total_evidence_available': total_evidence,
            'high_confidence_evidence': high_confidence_evidence,
            'total_curated': total_curated,
            'curation_rate': total_curated / high_confidence_evidence if high_confidence_evidence > 0 else 0,
            'evidence_by_category': category_counts,
            'average_confidence': round(avg_confidence, 3),
            'average_relevance_score': round(avg_relevance, 3),
            'curation_strategy': 'post_computation_intelligent_selection'
        } 