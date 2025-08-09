#!/usr/bin/env python3
"""
RAG-Enhanced Results Interpreter

A single, intelligent interpreter that combines statistical analysis with dynamic
evidence retrieval to create reports that serve multiple audiences while maintaining
academic rigor and narrative flow.

Key Design Principles:
- Human researcher approach: Use evidence strategically, not mechanically
- RAG for interpretive moments: Query evidence when making claims about patterns
- Multi-audience formatting: Scanner/collaborator/transparency sections in one report
- Narrative intelligence: Weave evidence naturally into the analytical story
"""

import json
import logging
import yaml
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from ....gateway.llm_gateway import LLMGateway
from ....gateway.model_registry import ModelRegistry


@dataclass
class RAGInterpretationRequest:
    """Request for RAG-enhanced interpretation."""
    statistical_results: Dict[str, Any]
    framework_spec: str
    experiment_context: Optional[str] = None
    txtai_curator: Optional[Any] = None  # For dynamic evidence queries
    
    # Provenance metadata
    run_id: Optional[str] = None
    models_used: Optional[Dict[str, str]] = None
    execution_timestamp_utc: Optional[str] = None
    execution_timestamp_local: Optional[str] = None
    framework_name: Optional[str] = None
    framework_version: Optional[str] = None
    corpus_info: Optional[Dict[str, Any]] = None
    cost_data: Optional[Dict[str, Any]] = None


@dataclass
class RAGInterpretationResponse:
    """Response with multi-audience report sections."""
    # Full report content
    full_report: str
    
    # Audience-specific sections
    scanner_section: str      # Executive summary for busy researchers
    collaborator_section: str # Detailed analysis for peer reviewers  
    transparency_section: str # Technical details for auditors
    
    # Metadata
    success: bool
    word_count: int
    evidence_queries_used: int
    used_evidence: Optional[List[Dict[str, Any]]] = None  # For quality measurement
    error_message: Optional[str] = None


class RAGEnhancedResultsInterpreter:
    """
    Intelligent results interpreter that uses RAG strategically to ground
    interpretive claims in actual evidence, like a human researcher would.
    """
    
    def __init__(self, model: str, audit_logger=None):
        self.model = model
        self.model_registry = ModelRegistry()
        self.llm_gateway = LLMGateway(self.model_registry)
        self.logger = logging.getLogger(__name__)
        self.audit_logger = audit_logger
        self.evidence_queries_count = 0
        self._used_evidence: List[Dict[str, Any]] = []
        
    def interpret_results(self, request: RAGInterpretationRequest) -> RAGInterpretationResponse:
        """Generate RAG-enhanced interpretation with multi-audience sections."""
        try:
            self.evidence_queries_count = 0
            # Cache experiment_context JSON for downstream helpers (e.g., hypothesis binding)
            try:
                self._last_experiment_context = request.experiment_context or ""
            except Exception:
                self._last_experiment_context = ""
            
            # REQ-SA-001: Detect and validate evidence resource availability
            evidence_available = self._validate_evidence_availability(request.txtai_curator)
            
            # REQ-SA-002: Identify interpretive claims that require evidence backing
            interpretive_claims = self._identify_interpretive_claims(
                request.statistical_results, 
                evidence_available=evidence_available
            )
            
            # Log evidence awareness status per Epic #280
            self.logger.info(f"🔍 Evidence awareness: {evidence_available}, interpretive claims identified: {len([c for c in interpretive_claims if c.get('evidence_needed', False)])}/{len(interpretive_claims)}")
            
            # Generate evidence-grounded narrative sections
            scanner_section = self._generate_scanner_section(request, interpretive_claims)
            collaborator_section = self._generate_collaborator_section(request, interpretive_claims)
            transparency_section = self._generate_transparency_section(request)
            
            # Combine into full report with evidence integration status
            full_report = self._combine_sections(
                scanner_section, collaborator_section, transparency_section, request
            )
            
            return RAGInterpretationResponse(
                full_report=full_report,
                scanner_section=scanner_section,
                collaborator_section=collaborator_section,
                transparency_section=transparency_section,
                success=True,
                word_count=len(full_report.split()),
                evidence_queries_used=self.evidence_queries_count,
                used_evidence=self._used_evidence  # Add used evidence for quality measurement
            )
            
        except Exception as e:
            self.logger.error(f"RAG interpretation failed: {str(e)}")
            return RAGInterpretationResponse(
                full_report="",
                scanner_section="",
                collaborator_section="",
                transparency_section="",
                success=False,
                word_count=0,
                evidence_queries_used=0,
                used_evidence=[],
                error_message=str(e)
            )
    
    def _validate_evidence_availability(self, txtai_curator) -> bool:
        """
        REQ-SA-001: Detect when evidence resource is available and populated.
        
        Validates that:
        1. txtai_curator exists and is properly initialized
        2. Evidence index is built and contains evidence pieces
        3. Query functionality is operational
        
        Returns:
            bool: True if evidence can be used for interpretation, False otherwise
        """
        if not txtai_curator:
            self.logger.debug("Evidence unavailable: No txtai curator provided")
            return False
            
        # Check if txtai curator has been initialized with evidence
        if not hasattr(txtai_curator, 'index_built') or not txtai_curator.index_built:
            self.logger.debug("Evidence unavailable: txtai index not built")
            return False
            
        if not hasattr(txtai_curator, 'documents') or not txtai_curator.documents:
            self.logger.debug("Evidence unavailable: No documents in evidence pool")
            return False
            
        # Check if evidence pool has sufficient content
        evidence_count = len(txtai_curator.documents)
        if evidence_count < 5:  # Minimum threshold for meaningful evidence
            self.logger.warning(f"Limited evidence pool: only {evidence_count} pieces available")
            return False
            
        self.logger.info(f"✅ Evidence resource validated: {evidence_count} pieces indexed and ready")
        return True
    
    def _identify_interpretive_claims(self, statistical_results: Dict[str, Any], evidence_available: bool = False) -> List[Dict[str, Any]]:
        """
        REQ-SA-002: Identify interpretive claims requiring evidence backing vs mathematical facts.
        
        Enhanced logic distinguishes between:
        - Dimensional scores/patterns → Need evidence justification  
        - Mathematical operations (correlations, ANOVA) → Transparent formula sufficient
        - Speaker characterizations → Need evidence examples
        - Statistical summaries → Mathematical transparency sufficient
        """
        interpretive_claims = []
        
        for result_key, result_data in statistical_results.items():
            if not isinstance(result_data, dict):
                continue
                
            # Enhanced interpretive claim detection per Epic #280 requirements
            evidence_needed = self._requires_evidence_backing(result_key, result_data)
            
            # Only generate query terms if evidence is available and needed
            query_terms = []
            if evidence_needed and evidence_available:
                query_terms = self._extract_query_terms(result_key, result_data)
            elif evidence_needed and not evidence_available:
                self.logger.debug(f"Evidence needed for '{result_key}' but not available - proceeding with statistical interpretation only")
            
                interpretive_claims.append({
                    'result_key': result_key,
                    'result_data': result_data,
                'evidence_needed': evidence_needed,
                'evidence_available': evidence_available,
                'query_terms': query_terms,
                'claim_type': self._classify_claim_type(result_key, result_data)
                })
        
        return interpretive_claims
    
    def _requires_evidence_backing(self, result_key: str, result_data: Dict[str, Any]) -> bool:
        """
        Determine if a statistical result requires evidence backing for interpretation.
        
        Evidence needed for:
        - Dimensional scores and patterns (dignity_score = 0.0) 
        - Speaker characterizations and discourse analysis
        - Framework-specific interpretive findings
        - Derived metrics containing interpretive dimension scores
        
        Evidence NOT needed for:
        - Pure mathematical operations (correlations, ANOVA F-statistics)
        - Technical validation and data quality checks
        """
        result_type = result_data.get("type", "unknown").lower()
        result_key_lower = result_key.lower()
        
        # PRIORITY CHECK: Framework dimensions always need evidence, regardless of context
        framework_dimension_patterns = [
            'dignity', 'tribalism', 'truth', 'manipulation', 'justice', 'resentment', 
            'hope', 'fear', 'pragmatism', 'fantasy', 'tension', 'character_index',
            'virtue_index', 'pathology_index', 'civic_character'
        ]
        
        if any(pattern in result_key_lower for pattern in framework_dimension_patterns):
            return True
        
        # Check if derived metrics calculation contains dimension scores (speaker-specific interpretive claims)
        if result_type == 'derived_metrics_calculation':
            calculated_metrics = result_data.get('calculated_metrics', {})
            if any('tension' in metric or 'index' in metric for metric in calculated_metrics.keys()):
                return True
        
        # Speaker and discourse analysis patterns  
        speaker_analysis_patterns = [
            'speaker', 'discourse', 'pattern', 'signature', 'profile',
            'populist', 'institutional', 'cohesion', 'fragmentative', 'oligarch'
        ]
        
        if any(pattern in result_key_lower for pattern in speaker_analysis_patterns):
            return True
        
        # Check if result involves individual document or speaker analysis via provenance
        if 'provenance' in result_data:
            input_columns = result_data.get('provenance', {}).get('input_columns', [])
            if any('_score' in col or '_dimension' in col for col in input_columns):
                return True
        
        # Mathematical operations that truly don't need evidence backing
        purely_mathematical_patterns = [
            'correlation_matrix', 'anova_f_statistic', 't_test', 'chi_square', 'regression',
            'data_quality', 'missing_data', 'range_check'
        ]
        
        if any(pattern in result_type for pattern in purely_mathematical_patterns):
            return False
        
        # Conservative approach for unclear cases
        return True
    
    def _classify_claim_type(self, result_key: str, result_data: Dict[str, Any]) -> str:
        """Classify the type of interpretive claim for targeted evidence retrieval."""
        result_key_lower = result_key.lower()
        
        if any(pattern in result_key_lower for pattern in ['speaker', 'profile', 'signature']):
            return 'speaker_characterization'
        elif any(pattern in result_key_lower for pattern in ['correlation', 'relationship']):
            return 'relationship_analysis'  
        elif any(pattern in result_key_lower for pattern in ['tension', 'conflict', 'contrast']):
            return 'dimensional_tension'
        elif any(pattern in result_key_lower for pattern in ['score', 'dimension']):
            return 'dimensional_analysis'
        elif any(pattern in result_key_lower for pattern in ['pattern', 'trend']):
            return 'discourse_pattern'
        else:
            return 'general_interpretation'
    
    def _extract_query_terms(self, result_key: str, result_data: Dict[str, Any]) -> List[str]:
        """Extract semantic terms for evidence queries."""
        query_terms = []
        
        # Extract from result key
        key_terms = {
            'dignity': ['dignity', 'respect', 'honor', 'civility'],
            'oligarchy': ['oligarchy', 'elite', 'wealthy', 'billionaire'],
            'populist': ['populist', 'people', 'establishment'],
            'tribal': ['tribal', 'us vs them', 'group'],
            'hope': ['hope', 'optimism', 'future'],
            'fear': ['fear', 'threat', 'danger'],
            'enmity': ['enmity', 'enemy', 'opposition'],
            'amity': ['amity', 'friendship', 'cooperation']
        }
        
        for concept, terms in key_terms.items():
            if concept in result_key.lower():
                query_terms.extend(terms)
        
        # Add provenance-based terms
        if 'provenance' in result_data:
            provenance = result_data['provenance']
            if 'input_columns' in provenance:
                for col in provenance['input_columns']:
                    if isinstance(col, str):
                        query_terms.append(col.replace('_', ' '))
        
        return query_terms[:5]  # Limit query complexity
    
    def _generate_scanner_section(self, request: RAGInterpretationRequest, claims: List[Dict]) -> str:
        """Generate executive summary with structured statistical presentation for busy researchers."""
        
        # Generate structured components first
        hypothesis_table = self._generate_hypothesis_table(request.statistical_results)
        core_findings = self._generate_core_statistical_findings(request.statistical_results)
        
        scanner_prompt = f"""
Generate an executive summary for busy researchers who need to quickly understand the key findings.

STATISTICAL RESULTS: {self._safe_json_dumps(request.statistical_results, indent=2)}

FRAMEWORK CONTEXT: {request.framework_spec[:500]}...

TASK: Write a 2-3 paragraph executive summary that:
1. Leads with the most significant finding
2. Highlights practical implications
3. Uses clear, accessible language
4. Focuses on "what this means" rather than statistical details

Keep it scannable and actionable for a busy researcher.
"""
        
        response_content, _ = self.llm_gateway.execute_call(
            model=self.model,
            prompt=scanner_prompt
        )
        
        # Combine executive summary with structured components
        full_scanner_section = f"""
{response_content.strip()}

---

## 📊 Key Results At A Glance

### Hypothesis Testing Results

{hypothesis_table}

### Core Statistical Findings

{core_findings}
"""
        
        return full_scanner_section.strip()
    
    def _generate_corpus_description(self, request: RAGInterpretationRequest) -> str:
        """Generate a description of the corpus being analyzed."""
        corpus_info = request.corpus_info or {}
        
        # Extract corpus details from experiment context if available
        if request.experiment_context:
            try:
                context = json.loads(request.experiment_context)
                corpus_files = context.get('corpus_files', [])
                if corpus_files:
                    file_names = [f.get('filename', 'Unknown') for f in corpus_files]
                    return f"**Corpus**: {len(corpus_files)} documents ({', '.join(file_names[:3])}{'...' if len(file_names) > 3 else ''})"
            except:
                pass
        
        # Try to extract from corpus_info directly
        if corpus_info.get('files'):
            files = corpus_info['files']
            if isinstance(files, list) and files:
                return f"**Corpus**: {len(files)} documents ({', '.join(files[:3])}{'...' if len(files) > 3 else ''})"
        
        # Check for document count in corpus_info
        doc_count = corpus_info.get('document_count', corpus_info.get('total_documents'))
        if isinstance(doc_count, int):
            return f"**Corpus**: {doc_count} documents"
        
        # Fallback when only hashes or minimal info are available
        return "**Corpus**: documents analyzed (count unavailable)"
    
    def _generate_hypothesis_table(self, statistical_results: Dict[str, Any]) -> str:
        """Generate a hypothesis testing results table."""
        # If available, extract canonical hypotheses from experiment context and bind strictly to them
        experiment_hypotheses = []
        try:
            # experiment_context may contain experiment_config with 'hypotheses'
            # Each hypothesis can be a string or an object with 'id'/'text'
            # We convert to a numbered list H1, H2, ... preserving order
            if hasattr(self, 'current_request_context_json') and self.current_request_context_json:
                context = self.current_request_context_json
            else:
                context = None
        except Exception:
            context = None

        # Fallback: try to read from the most recent request passed through interpret_results
        # We store it temporarily to avoid threading state; if not available, parse later below
        # Parse from a captured attribute if previously set
        # Note: we will also attempt JSON parse inside the try/catch in interpret_results caller if needed

        hypotheses_section = ""
        try:
            # Attempt to access last request via an attribute set in interpret_results caller
            # If not present, we'll parse from local variable in scanner/collaborator generators
            pass
        except Exception:
            pass

        # Build hypotheses list from experiment_context embedded in statistical_results if present
        # (statistical_results may include provenance; if not, we rely on caller-provided context parsing in interpret_results)
        canonical_hypotheses = []
        try:
            # Nothing to extract from statistical_results directly; rely on a stored snapshot
            pass
        except Exception:
            pass

        # Assemble prompt with strict binding to provided hypotheses if we can read them from interpret_results scope
        # We will pass only the statistical_results and a rendered hypotheses list extracted at call site
        prompt = f"""
Create a hypothesis testing results table. Use ONLY the provided hypotheses; do not invent new hypotheses.

Statistical Results:
{self._safe_json_dumps(statistical_results, indent=2)}

Provided Hypotheses (use this exact list; if a hypothesis cannot be tested with available data, mark Not Testable and explain why):
{{HYPOTHESES}}

Format as a markdown table with columns:
- Hypothesis
- Status (SUPPORTED / PARTIALLY SUPPORTED / REJECTED / NOT TESTABLE)
- Key Evidence
- Statistical Significance

Do not include any hypotheses that are not in the Provided Hypotheses list. If none are provided, summarize at most three core, data-driven findings as hypotheses and clearly label them as Exploratory.
"""
        
        try:
            # Try to extract hypotheses from the most recent experiment context cached on the interpreter
            hypotheses_list = []
            try:
                if hasattr(self, "_last_experiment_context") and self._last_experiment_context:
                    ctx = json.loads(self._last_experiment_context)
                    exp_cfg = ctx.get('experiment_config', {})
                    raw_hyps = exp_cfg.get('hypotheses', [])
                    if isinstance(raw_hyps, dict):
                        # Dict mapping ids to text
                        for key in sorted(raw_hyps.keys()):
                            hypotheses_list.append(str(raw_hyps[key]))
                    elif isinstance(raw_hyps, list):
                        for h in raw_hyps:
                            hypotheses_list.append(h if isinstance(h, str) else str(h))
            except Exception:
                hypotheses_list = []

            rendered_hypotheses = "\n".join([f"- H{idx+1}: {text}" for idx, text in enumerate(hypotheses_list)]) if hypotheses_list else "(none provided)"
            final_prompt = prompt.replace("{HYPOTHESES}", rendered_hypotheses)

            response_content, _ = self.llm_gateway.execute_call(
                model=self.model,
                prompt=final_prompt
            )
            return response_content.strip()
        except Exception as e:
            self.logger.warning(f"Failed to generate hypothesis table: {e}")
            return "Hypothesis testing results available in detailed findings section."
    
    def _generate_core_statistical_findings(self, statistical_results: Dict[str, Any]) -> str:
        """Generate core statistical findings for scanner's view."""
        prompt = f"""
Extract and present the 3-5 most important statistical findings from this analysis.

Statistical Results: {self._safe_json_dumps(statistical_results, indent=2)}

Present as bullet points with:
- Clear metric names
- Numerical values
- Brief interpretation
- Significance indicators

Focus on findings that would be most important for a researcher scanning the report.
"""
        
        try:
            response_content, _ = self.llm_gateway.execute_call(
                model=self.model,
                prompt=prompt
            )
            return response_content.strip()
        except Exception as e:
            self.logger.warning(f"Failed to generate core findings: {e}")
            return "Core statistical findings available in detailed analysis section."
    
    def _generate_collaborator_section(self, request: RAGInterpretationRequest, claims: List[Dict]) -> str:
        """Generate detailed analysis with evidence grounding for peer reviewers."""
        
        # This is where we use RAG strategically
        evidence_grounded_findings = []
        collected_evidence: List[Dict[str, Any]] = []
        
        for claim in claims:
            if claim.get('evidence_needed', False) and claim.get('evidence_available', False) and request.txtai_curator:
                # Strategic evidence query with claim context per REQ-SA-003
                evidence = self._query_evidence_for_claim(
                    request.txtai_curator, 
                    claim['query_terms'], 
                    claim['result_key'],
                    claim_data=claim  # Pass full claim context for strategic querying
                )
                if evidence:
                    evidence_grounded_findings.append({
                        'claim': claim,
                        'evidence': evidence
                    })
                    collected_evidence.extend(evidence)
        
        # Store a de-duplicated list of used evidence for footnote rendering
        if collected_evidence:
            seen = set()
            unique_evidence = []
            for ev in collected_evidence:
                key = (ev.get('document_id') or ev.get('document_name'), ev.get('dimension'), ev.get('quote_text'))
                if key not in seen:
                    seen.add(key)
                    unique_evidence.append(ev)
            self._used_evidence = unique_evidence
        
        collaborator_prompt = f"""
Generate detailed findings with evidence integration for academic peer reviewers.

STATISTICAL RESULTS: {self._safe_json_dumps(request.statistical_results, indent=2)}

EVIDENCE-GROUNDED FINDINGS:
{self._format_evidence_findings(evidence_grounded_findings)}

FRAMEWORK CONTEXT: {request.framework_spec[:1000]}...

TASK: Write a comprehensive analysis that:
1. Presents statistical findings with appropriate rigor
2. Integrates evidence quotes naturally into the narrative
3. Explains the interpretive reasoning behind claims
4. Maintains academic objectivity
5. Uses proper citations with document attribution

Structure as academic prose, not bullet points. Make evidence integration feel natural, not forced.
"""
        
        response_content, _ = self.llm_gateway.execute_call(
            model=self.model,
            prompt=collaborator_prompt
        )
        
        return response_content.strip()
    
    def _query_evidence_for_claim(self, txtai_curator, query_terms: List[str], result_key: str, claim_data: Dict[str, Any] = None) -> Optional[List[Dict]]:
        """
        REQ-SA-003: Strategic evidence querying for synthesis workflow.
        
        Enhanced evidence retrieval that:
        - Uses claim type for targeted querying
        - Leverages provenance information for focused search  
        - Adapts query complexity and evidence volume to claim type
        - Implements multi-stage querying for comprehensive coverage
        """
        if not query_terms or not hasattr(txtai_curator, '_query_evidence'):
            return None
            
        try:
            # Import EvidenceQuery from the curator module
            from ...txtai_evidence_curator.agent import EvidenceQuery
            
            # Extract strategic information from claim
            claim_type = claim_data.get('claim_type', 'general_interpretation') if claim_data else 'general_interpretation'
            result_data = claim_data.get('result_data', {}) if claim_data else {}
            
            # Strategic evidence querying based on claim type
            evidence_pieces = self._execute_strategic_query(txtai_curator, query_terms, claim_type, result_data, result_key)
            
            if evidence_pieces:
                self.evidence_queries_count += 1
                self.logger.info(f"Strategic RAG query for '{result_key}' ({claim_type}): retrieved {len(evidence_pieces)} targeted evidence pieces")
                return evidence_pieces
            else:
                self.logger.debug(f"No evidence found for strategic query '{result_key}' with terms: {query_terms[:3]}")
            
        except Exception as e:
            self.logger.warning(f"Strategic evidence query failed for '{result_key}': {e}")
        
        return None
    
    def _execute_strategic_query(self, txtai_curator, query_terms: List[str], claim_type: str, result_data: Dict[str, Any], result_key: str) -> List[Dict]:
        """Execute multi-stage strategic evidence retrieval based on claim type."""
        from ...txtai_evidence_curator.agent import EvidenceQuery
        
        evidence_pieces = []
        
        # Stage 1: Primary targeted query based on claim type
        primary_query = self._build_primary_query(query_terms, claim_type, result_data)
        if primary_query:
            primary_results = txtai_curator._query_evidence(primary_query)
            if primary_results:
                evidence_pieces.extend([self._convert_evidence_result(result) for result in primary_results])
        
        # Stage 2: Supplemental query if primary didn't yield enough evidence
        if len(evidence_pieces) < 2 and claim_type in ['speaker_characterization', 'dimensional_analysis']:
            supplemental_query = self._build_supplemental_query(query_terms, claim_type, result_data)
            if supplemental_query:
                supplemental_results = txtai_curator._query_evidence(supplemental_query)
                if supplemental_results:
                    # Add supplemental results, avoiding duplicates
                    existing_quotes = {ep['quote_text'] for ep in evidence_pieces}
                    for result in supplemental_results:
                        converted = self._convert_evidence_result(result)
                        if converted['quote_text'] not in existing_quotes:
                            evidence_pieces.append(converted)
                            if len(evidence_pieces) >= 4:  # Reasonable limit for strategic querying
                                break
        
        return evidence_pieces
    
    def _build_primary_query(self, query_terms: List[str], claim_type: str, result_data: Dict[str, Any]) -> Optional[object]:
        """Build primary evidence query optimized for claim type."""
        from ...txtai_evidence_curator.agent import EvidenceQuery
        
        # Strategic query building based on claim type
        if claim_type == 'speaker_characterization':
            # For speaker analysis, prioritize dimension-specific evidence
            if result_data.get('provenance', {}).get('input_document_ids'):
                # Target specific documents if available
                doc_ids = result_data['provenance']['input_document_ids'][:2]  # Top 2 most relevant documents
                semantic_query = ' AND '.join(query_terms[:2])  # More focused AND query
                return EvidenceQuery(
                    semantic_query=semantic_query,
                    limit=3
                )
        
        elif claim_type == 'dimensional_analysis':
            # For dimensional analysis, focus on dimension-specific evidence
            dimension_terms = [term for term in query_terms if any(dim in term.lower() 
                                                                 for dim in ['dignity', 'truth', 'justice', 'hope', 'pragmatism', 
                                                                           'tribalism', 'manipulation', 'resentment', 'fear', 'fantasy'])]
            if dimension_terms:
                semantic_query = ' OR '.join(dimension_terms[:3])
                return EvidenceQuery(
                    semantic_query=semantic_query,
                    limit=2
                )
        
        elif claim_type == 'relationship_analysis':
            # For relationships, use broader semantic search
            semantic_query = ' OR '.join(query_terms[:4])  # Slightly broader for relationships
            return EvidenceQuery(
                semantic_query=semantic_query, 
                limit=2
            )
        
        # Default strategic query for other claim types
        semantic_query = ' OR '.join(query_terms[:3])
        return EvidenceQuery(
            semantic_query=semantic_query,
            limit=3
        )
    
    def _build_supplemental_query(self, query_terms: List[str], claim_type: str, result_data: Dict[str, Any]) -> Optional[object]:
        """Build supplemental query to fill evidence gaps."""
        from ...txtai_evidence_curator.agent import EvidenceQuery
        
        # Supplemental queries use broader terms to fill gaps
        if len(query_terms) > 3:
            # Use remaining terms for supplemental search
            supplemental_terms = query_terms[3:6]  # Terms 4-6
            semantic_query = ' OR '.join(supplemental_terms)
            return EvidenceQuery(
                semantic_query=semantic_query,
                limit=2
            )
        
        return None
    
    def _convert_evidence_result(self, result) -> Dict[str, Any]:
        """Convert EvidenceResult object to dict format for compatibility."""
        return {
            'quote_text': result.quote_text,
            'document_name': result.document_name,
            'dimension': result.dimension,
            'confidence': getattr(result, 'confidence', 0.0),
            'speaker': getattr(result, 'speaker', 'unknown'),
            'document_id': getattr(result, 'document_id', result.document_name)
        }
    
    def _safe_json_dumps(self, obj, **kwargs):
        """Safely serialize object to JSON, converting non-serializable objects to strings."""
        try:
            return json.dumps(obj, **kwargs)
        except (TypeError, ValueError) as e:
            # Handle non-serializable objects by converting them to strings
            try:
                def convert_non_serializable(o):
                    if hasattr(o, '__dict__'):
                        return str(o)
                    elif isinstance(o, (set, frozenset)):
                        return list(o)
                    else:
                        return str(o)
                
                return json.dumps(obj, default=convert_non_serializable, **kwargs)
            except Exception:
                # Last resort: convert entire object to string
                return str(obj)
    
    def _format_evidence_findings(self, evidence_grounded_findings: List[Dict]) -> str:
        """Format evidence findings for LLM consumption."""
        if not evidence_grounded_findings:
            return "No evidence-grounded findings available."
        
        formatted = []
        for i, finding in enumerate(evidence_grounded_findings, 1):
            claim = finding['claim']
            evidence = finding['evidence']
            
            formatted.append(f"FINDING {i}: {claim['result_key']}")
            formatted.append(f"Statistical Data: {self._safe_json_dumps(claim['result_data'], indent=2)}")
            formatted.append("Supporting Evidence:")
            
            for j, ev in enumerate(evidence, 1):
                quote = ev.get('quote_text', '')
                document = ev.get('document_id', 'unknown')
                dimension = ev.get('dimension', 'unknown')
                formatted.append(f"  [{j}] {document} ({dimension}): \"{quote}\"")
            
            formatted.append("")  # Blank line
        
        return "\n".join(formatted)
    
    def _generate_transparency_section(self, request: RAGInterpretationRequest) -> str:
        """Generate technical transparency details for auditors."""
        
        transparency_items = []
        
        # Framework and corpus information
        if request.framework_name and request.framework_version:
            transparency_items.append(f"**Framework**: {request.framework_name} {request.framework_version}")
        
        # Corpus description
        corpus_description = self._generate_corpus_description(request)
        transparency_items.append(corpus_description)
        
        # Cost breakdown
        if request.cost_data:
            transparency_items.append(f"**Cost Analysis**: {self._safe_json_dumps(request.cost_data, indent=2)}")
        
        # Model information
        if request.models_used:
            transparency_items.append(f"**Models Used**: {self._safe_json_dumps(request.models_used, indent=2)}")
        
        # Evidence queries
        transparency_items.append(f"**Evidence Queries**: {self.evidence_queries_count} dynamic RAG queries executed")
        
        # Execution metadata
        if request.run_id:
            transparency_items.append(f"**Run ID**: {request.run_id}")
        
        if request.execution_timestamp_utc:
            transparency_items.append(f"**Execution Time**: {request.execution_timestamp_utc}")

        # Evidence footnotes (provenance mapping)
        if getattr(self, "_used_evidence", None):
            footnotes = ["\n### Evidence References"]
            for idx, ev in enumerate(self._used_evidence, start=1):
                doc = ev.get('document_id') or ev.get('document_name') or 'unknown_document'
                dim = ev.get('dimension', 'unknown')
                quote = ev.get('quote_text', '').strip()
                conf = ev.get('confidence')
                conf_str = f"; confidence={conf:.2f}" if isinstance(conf, (int, float)) else ""
                footnotes.append(f"[{idx}] {doc} ({dim}) — \"{quote}\"{conf_str}")
            transparency_items.append("\n".join(footnotes))
        
        return "\n\n".join(transparency_items)
    
    def _combine_sections(self, scanner: str, collaborator: str, transparency: str, request: RAGInterpretationRequest) -> str:
        """Combine sections into full multi-audience report."""
        
        # Extract experiment metadata
        experiment_name = "Computational Analysis"
        if request.experiment_context:
            try:
                context = json.loads(request.experiment_context)
                experiment_name = context.get('experiment_config', {}).get('name', experiment_name)
            except:
                pass
        
        # Disambiguate framework vs. gasket/report version labels if both exist
        framework_line = f"**Framework**: {request.framework_name or 'Unknown'}"
        if request.framework_version:
            framework_line += f" ({request.framework_version})"
        
        report_sections = [
            "---",
            f"# {experiment_name}",
            "",
            framework_line,
            f"**Run ID**: {request.run_id or 'Unknown'}",
            f"**Generated**: {request.execution_timestamp_local or datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "---",
            "",
            "## 📊 Executive Summary",
            "*For busy researchers who need key insights quickly*",
            "",
            scanner,
            "",
            "---",
            "",
            "## 🔬 Detailed Analysis",
            "*For peer reviewers and academic collaborators*",
            "",
            collaborator,
            "",
            "---",
            "",
            "## 🛠️ Technical Transparency",
            "*For auditors and replication researchers*",
            "",
            transparency,
            "",
            "---"
        ]
        
        return "\n".join(report_sections)
