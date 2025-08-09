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
        Main investigative synthesis - the chef's tasting menu approach.
        
        Amuse-bouche: Parse hypotheses and prepare investigation plan
        Premier plat: Active hypothesis testing with evidence interrogation  
        Plat principal: Statistical anomaly investigation and pattern discovery
        Dessert: Insight synthesis and unexpected pattern revelation
        """
        try:
            self.investigation_log = []
            
            # Amuse-bouche: Extract experiment hypotheses from context
            hypotheses = self._extract_hypotheses_from_context(request.experiment_context)
            self.logger.info(f"🔍 Chef's menu: Testing {len(hypotheses)} hypotheses with active RAG investigation")
            
            # Premier plat: Hypothesis testing with comprehensive knowledge interrogation
            hypothesis_section = self._investigate_hypotheses(
                hypotheses, 
                request.statistical_results, 
                request.knowledge_curator
            )
            
            # Plat principal: Statistical anomaly investigation with cross-domain reasoning
            insight_section = self._discover_insights(
                request.statistical_results,
                request.knowledge_curator,
                request.framework_spec
            )
            
            return InvestigativeResponse(
                hypothesis_testing_section=hypothesis_section,
                insight_discovery_section=insight_section,
                evidence_investigation_log=self.investigation_log,
                total_evidence_queries=len(self.investigation_log),
                success=True
            )
            
        except Exception as e:
            self.logger.error(f"🔥 Kitchen fire! Investigation failed: {e}")
            return InvestigativeResponse(
                hypothesis_testing_section="",
                insight_discovery_section="",
                evidence_investigation_log=[],
                total_evidence_queries=0,
                success=False,
                error_message=str(e)
            )
    
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
    
    def _investigate_hypotheses(self, hypotheses: List[Dict[str, str]], 
                               statistical_results: Dict[str, Any], 
                               knowledge_curator) -> str:
        """
        Active hypothesis testing - the chef interrogates each hypothesis with evidence.
        
        For each hypothesis:
        1. Identify relevant statistical findings
        2. Query RAG engine for supporting/contradicting evidence  
        3. Synthesize evidence-backed conclusion
        """
        
        if not hypotheses:
            return "## Hypothesis Testing\n\nNo structured hypotheses found in experiment design."
        
        sections = ["## Evidence-Backed Hypothesis Testing\n"]
        
        for hypothesis in hypotheses:
            self.logger.info(f"🔍 Investigating {hypothesis['id']}: {hypothesis['name']}")
            
            # Design investigation queries based on hypothesis
            investigation_queries = self._design_investigation_queries(hypothesis)
            
            # Interrogate the comprehensive knowledge graph
            evidence_findings = []
            for query in investigation_queries:
                knowledge_results = self._interrogate_knowledge(knowledge_curator, query, hypothesis['id'])
                if knowledge_results:
                    evidence_findings.extend(knowledge_results)
            
            # Find relevant statistical results
            statistical_support = self._find_statistical_support(hypothesis, statistical_results)
            
            # Synthesize hypothesis conclusion
            hypothesis_conclusion = self._synthesize_hypothesis_conclusion(
                hypothesis, statistical_support, evidence_findings
            )
            
            sections.append(f"### {hypothesis['id']}: {hypothesis['name']}\n")
            sections.append(f"**Hypothesis**: {hypothesis['statement']}\n")
            sections.append(hypothesis_conclusion)
            sections.append("")
        
        return "\n".join(sections)
    
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
        relevant_stats = {}
        
        # Extract relevant statistical findings based on hypothesis type
        for result_key, result_data in statistical_results.items():
            if not isinstance(result_data, dict):
                continue
                
            if 'speaker_differentiation' in hypothesis_key:
                if 'descriptive_stats' in result_key or 'variance' in result_key.lower():
                    relevant_stats[result_key] = result_data
            elif 'character_signatures' in hypothesis_key:
                if 'correlation' in result_key.lower() or 'derived_metrics' in result_key:
                    relevant_stats[result_key] = result_data
            elif 'coherence' in hypothesis_key:
                if 'civic_character_index' in str(result_data) or 'coherence' in result_key.lower():
                    relevant_stats[result_key] = result_data
        
        return relevant_stats
    
    def _synthesize_hypothesis_conclusion(self, hypothesis: Dict[str, str], 
                                        statistical_support: Dict[str, Any],
                                        evidence_findings: List[Any]) -> str:
        """Synthesize evidence-backed conclusion for each hypothesis."""
        
        # Create synthesis prompt for LLM
        synthesis_prompt = f"""
You are a computational discourse analyst synthesizing findings for hypothesis testing.

HYPOTHESIS: {hypothesis['statement']}

STATISTICAL EVIDENCE:
{json.dumps(statistical_support, indent=2)}

TEXTUAL EVIDENCE:
{self._format_evidence_for_synthesis(evidence_findings)}

TASK: Write a rigorous academic conclusion that:
1. States whether the hypothesis is SUPPORTED, NOT SUPPORTED, or INCONCLUSIVE
2. Cites specific statistical findings with numbers
3. Integrates textual evidence with speaker attribution
4. Explains the reasoning clearly
5. Acknowledges limitations (N=8 sample size)

Format as academic prose with inline evidence citations.
"""

        try:
            content, meta = self.llm_gateway.execute_call(
                model=self.model,
                system_prompt="You are a rigorous academic researcher synthesizing computational discourse analysis.",
                prompt=synthesis_prompt,
                temperature=0.1
            )
            
            return content or "Synthesis failed - unable to generate conclusion."
            
        except Exception as e:
            self.logger.error(f"Hypothesis synthesis failed: {e}")
            return f"**Analysis Error**: Unable to synthesize conclusion for {hypothesis['id']}"
    
    def _discover_insights(self, statistical_results: Dict[str, Any], 
                          knowledge_curator, framework_spec: str) -> str:
        """
        Sauce 2: LLM-powered insight discovery beyond hypothesis testing.
        
        Let the billion-dollar training find obvious patterns that humans might miss.
        """
        
        self.logger.info("🧠 Activating billion-dollar pattern recognition for insight discovery...")
        
        # Design exploratory investigation queries
        exploratory_queries = [
            "What temporal patterns exist across speakers from different eras?",
            "Which speakers combine manipulation and resentment tactics?", 
            "How do salience patterns reveal speaker authenticity?",
            "What evidence shows the evolution of civic discourse over time?",
            "Which statistical anomalies have clear textual explanations?",
            "What unexpected correlations emerge from the evidence patterns?"
        ]
        
        insights = []
        
        for query in exploratory_queries:
            # Interrogate comprehensive knowledge for each exploratory question
            evidence = self._interrogate_knowledge(knowledge_curator, query, "INSIGHT")
            
            if evidence:
                # Let LLM discover patterns
                insight = self._generate_insight_from_evidence(query, evidence, statistical_results)
                if insight:
                    insights.append(insight)
        
        # Compile insights section
        if insights:
            insight_section = ["## Beyond the Hypotheses: Computational Insights\n"]
            insight_section.append("*Leveraging billion-dollar pattern recognition to discover insights beyond experimental design*\n")
            
            for i, insight in enumerate(insights, 1):
                insight_section.append(f"### Insight {i}: {insight['title']}\n")
                insight_section.append(insight['content'])
                insight_section.append("")
            
            return "\n".join(insight_section)
        else:
            return "## Computational Insights\n\nNo significant patterns discovered beyond hypothesis testing."
    
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
