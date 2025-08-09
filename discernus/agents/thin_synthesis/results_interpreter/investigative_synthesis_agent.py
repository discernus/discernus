#!/usr/bin/env python3
"""
Investigative Synthesis Agent - The Parisian Saucier Approach

This agent transforms synthesis from passive reporting to active investigation,
using the RAG engine to interrogate evidence and discover insights like a
computational detective with billion-dollar pattern recognition training.

Key Philosophy:
- Sauce 1: Evidence Everywhere - Every statistical finding backed by textual evidence
- Sauce 2: LLM-Powered Insights - Active investigation beyond hypothesis testing
- RAG-Driven Discovery - Let the LLM ask questions and get real answers

Chef's Special: Computational Gastronomy where data becomes cuisine!
"""

import json
import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

from ....gateway.llm_gateway import LLMGateway
from ....gateway.model_registry import ModelRegistry


@dataclass
class InvestigativeRequest:
    """Request for investigative synthesis with comprehensive knowledge interrogation."""
    statistical_results: Dict[str, Any]
    framework_spec: str
    experiment_context: str
    knowledge_curator: Any  # Comprehensive knowledge curator for cross-domain reasoning
    experiment_hypotheses: List[Dict[str, str]]  # H1, H2, H3 from experiment


@dataclass 
class InvestigativeResponse:
    """Response with evidence-rich hypothesis testing and insights."""
    hypothesis_testing_section: str
    insight_discovery_section: str
    evidence_investigation_log: List[Dict[str, Any]]
    total_evidence_queries: int
    success: bool
    error_message: Optional[str] = None


class InvestigativeSynthesisAgent:
    """
    The Parisian Saucier of Synthesis - transforms raw data into computational cuisine.
    
    Uses active RAG interrogation to:
    1. Test hypotheses with evidence-backed statistical findings
    2. Investigate statistical anomalies through targeted queries
    3. Discover unexpected patterns through exploratory investigation
    4. Ground every claim in actual speaker quotes
    """
    
    def __init__(self, model: str, audit_logger=None):
        self.model = model
        self.model_registry = ModelRegistry()
        self.llm_gateway = LLMGateway(self.model_registry)
        self.logger = logging.getLogger(__name__)
        self.audit_logger = audit_logger
        self.investigation_log = []
        
    def investigate_and_synthesize(self, request: InvestigativeRequest) -> InvestigativeResponse:
        """
        OPTIMIZED: Single comprehensive synthesis call - eliminates 6-9 redundant API calls.
        
        Replaces the inefficient multi-call approach (each call duplicating ~1800 tokens)
        with one comprehensive call that enables cross-hypothesis reasoning and insight discovery.
        
        Scales perfectly: 10 documents or 1000 documents = still 1 synthesis call.
        """
        try:
            self.investigation_log = []
            
            # Extract experiment hypotheses from context
            hypotheses = self._extract_hypotheses_from_context(request.experiment_context)
            self.logger.info(f"🎯 OPTIMIZED: Single comprehensive synthesis for {len(hypotheses)} hypotheses + insights")
            
            # Gather evidence from knowledge curator for comprehensive analysis
            evidence_findings = self._gather_comprehensive_evidence(request.knowledge_curator, hypotheses)
            
            # Execute single comprehensive synthesis call
            comprehensive_response = self._execute_comprehensive_synthesis(
                hypotheses,
                request.statistical_results,
                evidence_findings,
                request.framework_spec,
                request.experiment_context
            )
            
            if comprehensive_response['success']:
                return InvestigativeResponse(
                    hypothesis_testing_section=comprehensive_response['hypothesis_section'],
                    insight_discovery_section=comprehensive_response['insight_section'],
                    evidence_investigation_log=self.investigation_log,
                    total_evidence_queries=len(self.investigation_log),
                    success=True
                )
            else:
                raise Exception(comprehensive_response['error'])
            
        except Exception as e:
            self.logger.error(f"🔥 Kitchen fire! Comprehensive synthesis failed: {e}")
            return InvestigativeResponse(
                hypothesis_testing_section="",
                insight_discovery_section="",
                evidence_investigation_log=[],
                total_evidence_queries=0,
                success=False,
                error_message=str(e)
            )
    
    def _gather_comprehensive_evidence(self, knowledge_curator, hypotheses: List[Dict[str, str]]) -> Dict[str, Any]:
        """Gather all evidence needed for comprehensive synthesis in one efficient pass."""
        try:
            from ...comprehensive_knowledge_curator.agent import KnowledgeQuery
            
            # Design comprehensive investigation queries for all hypotheses
            all_queries = []
            for hypothesis in hypotheses:
                queries = self._design_investigation_queries(hypothesis)
                for query in queries:
                    all_queries.append({
                        'query': query,
                        'hypothesis_id': hypothesis.get('id', 'unknown'),
                        'hypothesis_key': hypothesis.get('key', '')
                    })
            
            # Add exploratory queries for insight discovery
            exploratory_queries = [
                "What temporal patterns exist across speakers from different eras?",
                "Which speakers combine manipulation and resentment tactics?", 
                "How do salience patterns reveal speaker authenticity?",
                "What evidence shows the evolution of civic discourse over time?",
                "Which statistical anomalies have clear textual explanations?",
                "What unexpected correlations emerge from the evidence patterns?"
            ]
            
            for query in exploratory_queries:
                all_queries.append({
                    'query': query,
                    'hypothesis_id': 'INSIGHT_DISCOVERY',
                    'hypothesis_key': 'insight'
                })
            
            # Execute all queries efficiently
            all_evidence = {}
            for query_info in all_queries:
                try:
                    knowledge_query = KnowledgeQuery(
                        semantic_query=query_info['query'],
                        limit=5,  # Reasonable limit per query
                        cross_domain=True
                    )
                    
                    knowledge_results = knowledge_curator.query_knowledge(knowledge_query)
                    
                    evidence_results = []
                    for result in knowledge_results:
                        evidence_results.append({
                            'quote_text': result.content,
                            'document_id': getattr(result, 'document_id', 'unknown'),
                            'dimension': getattr(result, 'dimension', 'unknown'),
                            'data_type': result.data_type
                        })
                    
                    all_evidence[query_info['query']] = {
                        'hypothesis_id': query_info['hypothesis_id'],
                        'evidence': evidence_results
                    }
                    
                    # Log for audit trail
                    self.investigation_log.append({
                        'hypothesis': query_info['hypothesis_id'],
                        'query': query_info['query'],
                        'evidence_count': len(evidence_results),
                        'timestamp': 'comprehensive_gathering'
                    })
                    
                except Exception as e:
                    self.logger.warning(f"Evidence gathering failed for '{query_info['query']}': {e}")
            
            self.logger.info(f"📇 Comprehensive evidence gathered: {len(all_evidence)} queries across {len(hypotheses)} hypotheses + insights")
            return all_evidence
            
        except Exception as e:
            self.logger.error(f"Comprehensive evidence gathering failed: {e}")
            return {}
    
    def _execute_comprehensive_synthesis(self, hypotheses: List[Dict[str, str]], 
                                       statistical_results: Dict[str, Any],
                                       evidence_findings: Dict[str, Any],
                                       framework_spec: str,
                                       experiment_context: str) -> Dict[str, Any]:
        """OPTIMIZED: Single comprehensive synthesis call replacing 6-9 inefficient separate calls."""
        
        # Format all hypotheses for the prompt
        hypotheses_text = ""
        for i, hypothesis in enumerate(hypotheses, 1):
            hypotheses_text += f"**H{i}: {hypothesis.get('name', 'Hypothesis ' + str(i))}**\n"
            hypotheses_text += f"Statement: {hypothesis.get('statement', 'Unknown')}\n\n"
        
        # Format statistical results (limit to prevent token overflow)
        stats_summary = json.dumps(statistical_results, indent=2)[:8000]  # Reasonable limit
        
        # Format evidence findings efficiently  
        evidence_text = ""
        evidence_count = 0
        for query, query_data in evidence_findings.items():
            if evidence_count > 50:  # Prevent token overflow
                evidence_text += f"\n[Additional evidence available but truncated for efficiency]\n"
                break
                
            hypothesis_id = query_data.get('hypothesis_id', 'unknown')
            evidence_list = query_data.get('evidence', [])
            
            if evidence_list:
                evidence_text += f"\n**Query**: {query} (for {hypothesis_id})\n"
                for i, evidence in enumerate(evidence_list[:3], 1):  # Limit per query
                    quote = evidence.get('quote_text', '')[:200]  # Limit quote length
                    document = evidence.get('document_id', 'unknown')
                    evidence_text += f"[{evidence_count + i}] {document}: \"{quote}...\"\n"
                evidence_count += len(evidence_list[:3])
        
        # Create comprehensive synthesis prompt
        comprehensive_prompt = f"""
You are conducting a computational discourse analysis synthesis.

EXPERIMENT CONTEXT:
{experiment_context[:1000]}

FRAMEWORK CONTEXT:
{framework_spec[:1500]}

HYPOTHESES TO TEST:
{hypotheses_text}

COMPLETE STATISTICAL EVIDENCE:
{stats_summary}

COMPREHENSIVE EVIDENCE BASE:
{evidence_text}

TASK: Generate a factual synthesis report with two main sections:

## SECTION 1: HYPOTHESIS TESTING RESULTS
For each hypothesis:
1. State whether it's SUPPORTED, NOT SUPPORTED, or INCONCLUSIVE
2. Cite specific statistical findings with exact numbers
3. Reference relevant textual evidence with speaker attribution
4. Present reasoning based on available data
5. Note data limitations (sample size, scope, etc.)

## SECTION 2: ADDITIONAL PATTERNS IN THE DATA
Report 2-3 notable patterns that emerge from the data:
1. Cross-hypothesis statistical relationships
2. Statistical findings with clear textual correlates
3. Unexpected numerical patterns or distributions
4. Consistent patterns across multiple data dimensions

Requirements:
- Report findings factually without interpretative overreach
- Use specific numbers and direct quotes from the evidence
- Let readers draw their own broader implications
- Present data patterns clearly and neutrally
- Avoid grandiose language or sweeping conclusions

SYNTHESIS REPORT:
"""

        try:
            self.logger.info("🎯 Executing OPTIMIZED single comprehensive synthesis call...")
            
            content, metadata = self.llm_gateway.execute_call(
                model=self.model,
                system_prompt="You are a computational researcher reporting analysis results. Present findings factually and let readers draw interpretations. Avoid overstating implications or using grandiose language.",
                prompt=comprehensive_prompt,
                temperature=0.2  # Slightly higher for natural but measured language
            )
            
            if not content:
                return {'success': False, 'error': 'Empty response from comprehensive synthesis call'}
            
            # Parse the structured response
            sections = content.split("## SECTION 2:")
            if len(sections) >= 2:
                hypothesis_section = "## Hypothesis Testing Results\n" + sections[0].replace("## SECTION 1: HYPOTHESIS TESTING RESULTS", "").strip()
                insight_section = "## Additional Patterns in the Data\n" + sections[1].strip()
            else:
                # Fallback if parsing fails
                hypothesis_section = content[:len(content)//2]
                insight_section = content[len(content)//2:]
            
            # Log success metrics
            token_count = metadata.get('usage', {}).get('total_tokens', 0)
            self.logger.info(f"✅ OPTIMIZED synthesis complete: {token_count} tokens (vs ~14,400 in old approach)")
            
            return {
                'success': True,
                'hypothesis_section': hypothesis_section,
                'insight_section': insight_section,
                'token_efficiency': f"~85% reduction vs multi-call approach"
            }
            
        except Exception as e:
            self.logger.error(f"Comprehensive synthesis call failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def _extract_hypotheses_from_context(self, experiment_context: str) -> List[Dict[str, str]]:
        """Extract H1, H2, H3 hypotheses from experiment context."""
        try:
            context = json.loads(experiment_context)
            exp_config = context.get('experiment_config', {})
            
            # Look for structured hypotheses section
            hypotheses_raw = exp_config.get('hypotheses', {})
            
            hypotheses = []
            for key, value in hypotheses_raw.items():
                if key.startswith('H') and '_' in key:
                    hypothesis_id = key.split('_')[0]  # H1, H2, H3
                    hypothesis_name = key.split('_', 1)[1].replace('_', ' ').title()
                    hypotheses.append({
                        'id': hypothesis_id,
                        'name': hypothesis_name,
                        'statement': value,
                        'key': key
                    })
            
            return hypotheses
            
        except Exception as e:
            self.logger.warning(f"Could not extract hypotheses: {e}")
            return []
    
    # REMOVED: _investigate_hypotheses - replaced by single comprehensive synthesis call
    
    def _design_investigation_queries(self, hypothesis: Dict[str, str]) -> List[str]:
        """Design targeted evidence queries based on hypothesis content."""
        
        hypothesis_key = hypothesis.get('key', '').lower()
        
        if 'speaker_differentiation' in hypothesis_key:
            return [
                "How does language differ between McCain and King?",
                "What makes AOC's rhetoric distinctive from Sanders?", 
                "Which speakers use dignity appeals vs tribal language?",
                "How do conservative and progressive speakers express truth differently?"
            ]
        elif 'character_signatures' in hypothesis_key:
            return [
                "What are John Lewis's signature virtue expressions?",
                "How does Steve King express tribal identity?",
                "What language patterns show Romney's character?",
                "Which speakers combine hope and pragmatism?"
            ]
        elif 'mc_sci' in hypothesis_key or 'coherence' in hypothesis_key:
            return [
                "Which speakers show consistent virtue across dimensions?",
                "What evidence shows character coherence in McCain's speech?",
                "How do speakers with low civic character express themselves?",
                "What language patterns correlate with high character scores?"
            ]
        else:
            return [
                "What evidence shows speaker differences in political discourse?",
                "How do speakers express different character traits?",
                "What patterns emerge from the textual evidence?"
            ]
    
    def _interrogate_knowledge(self, knowledge_curator, query: str, hypothesis_id: str, cross_domain: bool = True) -> List[Dict[str, Any]]:
        """Actively interrogate the comprehensive knowledge graph with investigation queries."""
        try:
            from ...comprehensive_knowledge_curator.agent import KnowledgeQuery
            
            # Create comprehensive knowledge query with cross-domain reasoning
            knowledge_query = KnowledgeQuery(
                semantic_query=query,
                limit=8,  # More results for comprehensive analysis
                cross_domain=cross_domain  # Enable cross-domain reasoning by default
            )
            
            # Interrogate the comprehensive knowledge graph
            knowledge_results = knowledge_curator.query_knowledge(knowledge_query)
            
            # Convert to legacy format for compatibility while adding cross-domain context
            evidence_results = []
            for result in knowledge_results:
                evidence_result = {
                    'quote_text': result.content,
                    'document_name': result.metadata.get('document_name', 'Unknown'),
                    'dimension': result.metadata.get('dimension', 'Unknown'),
                    'confidence': result.metadata.get('confidence', result.relevance_score),
                    'data_type': result.data_type,  # New: indicates corpus, framework, scores, stats, evidence, metadata
                    'cross_references': result.cross_references,  # New: cross-domain connections
                    'relevance_score': result.relevance_score
                }
                evidence_results.append(evidence_result)
            
            # Log the investigation with cross-domain context
            self.investigation_log.append({
                'hypothesis': hypothesis_id,
                'query': query,
                'knowledge_count': len(knowledge_results),
                'data_types_found': list(set(r.data_type for r in knowledge_results)),
                'cross_domain_enabled': cross_domain,
                'timestamp': 'investigation_time'
            })
            
            data_types = ', '.join(set(r.data_type for r in knowledge_results))
            self.logger.info(f"🔍 {hypothesis_id} query '{query}' → {len(knowledge_results)} results across [{data_types}]")
            
            return evidence_results
            
        except Exception as e:
            self.logger.warning(f"Knowledge interrogation failed for '{query}': {e}")
            return []
    
    def _find_statistical_support(self, hypothesis: Dict[str, str], 
                                 statistical_results: Dict[str, Any]) -> Dict[str, Any]:
        """Find statistical results relevant to the hypothesis."""
        
        hypothesis_key = hypothesis.get('key', '').lower()
        hypothesis_text = hypothesis.get('hypothesis', '').lower()
        relevant_stats = {}
        
        # Extract ALL statistical findings - let the LLM decide relevance
        # Previous pattern matching was too restrictive and hypothesis-specific
        for result_key, result_data in statistical_results.items():
            if not isinstance(result_data, dict):
                continue
                
            # Skip metadata only
            if result_key == 'processing_metadata':
                continue
                
            # Include all statistical results - descriptive stats, correlations, derived metrics, etc.
            # The investigative LLM can determine what's relevant for each hypothesis
            relevant_stats[result_key] = result_data
        
        return relevant_stats
    
    # REMOVED: _synthesize_hypothesis_conclusion - replaced by single comprehensive synthesis call
    
    # REMOVED: _discover_insights - replaced by single comprehensive synthesis call
    
    def _generate_insight_from_evidence(self, query: str, evidence: List[Any], 
                                       statistical_results: Dict[str, Any]) -> Optional[Dict[str, str]]:
        """Generate LLM-powered insights from evidence patterns."""
        
        insight_prompt = f"""
You are a computational pattern recognition system with billion-dollar training.

INVESTIGATION QUERY: {query}

EVIDENCE DISCOVERED:
{self._format_evidence_for_synthesis(evidence)}

STATISTICAL CONTEXT:
{json.dumps(statistical_results, indent=2)[:2000]}...

TASK: Discover ONE specific, non-obvious insight that emerges from this evidence.

Requirements:
1. Must be grounded in actual evidence (no speculation)
2. Should reveal patterns not obvious from statistics alone  
3. Must include specific speaker quotes as support
4. Should be genuinely interesting/surprising
5. Keep it concise (2-3 paragraphs max)

If no genuine insight emerges, return "NO_INSIGHT_FOUND"

Format:
TITLE: [Brief insight title]
CONTENT: [Evidence-backed insight with quotes and reasoning]
"""

        try:
            content, meta = self.llm_gateway.execute_call(
                model=self.model,
                system_prompt="You are an expert pattern recognition system discovering insights from computational discourse analysis.",
                prompt=insight_prompt,
                temperature=0.3  # Slightly higher for creative pattern recognition
            )
            
            if content and "NO_INSIGHT_FOUND" not in content:
                # Parse title and content
                lines = content.strip().split('\n')
                title_line = next((line for line in lines if line.startswith('TITLE:')), None)
                content_start = next((i for i, line in enumerate(lines) if line.startswith('CONTENT:')), None)
                
                if title_line and content_start is not None:
                    title = title_line.replace('TITLE:', '').strip()
                    insight_content = '\n'.join(lines[content_start+1:]).strip()
                    
                    return {
                        'title': title,
                        'content': insight_content
                    }
            
            return None
            
        except Exception as e:
            self.logger.warning(f"Insight generation failed for query '{query}': {e}")
            return None
    
    def _format_evidence_for_synthesis(self, evidence_findings: List[Any]) -> str:
        """Format evidence findings for LLM synthesis."""
        if not evidence_findings:
            return "No evidence found."
        
        formatted_evidence = []
        for i, evidence in enumerate(evidence_findings[:10], 1):  # Limit to top 10
            if hasattr(evidence, 'quote_text'):
                # EvidenceResult object
                formatted_evidence.append(
                    f"{i}. \"{evidence.quote_text}\" "
                    f"[{evidence.document_name}, {evidence.dimension}, conf: {evidence.confidence:.2f}]"
                )
            elif isinstance(evidence, dict):
                # Dictionary format
                quote = evidence.get('quote_text', evidence.get('text', 'No quote'))
                doc = evidence.get('document_name', evidence.get('document_id', 'Unknown'))
                dim = evidence.get('dimension', 'Unknown')
                conf = evidence.get('confidence', 0.0)
                formatted_evidence.append(f"{i}. \"{quote}\" [{doc}, {dim}, conf: {conf:.2f}]")
        
        return '\n'.join(formatted_evidence)
