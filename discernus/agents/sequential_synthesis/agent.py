#!/usr/bin/env python3
"""
Sequential Synthesis Agent (v2.0)

Implements the THIN, framework-agnostic, sequential synthesis architecture.
This agent replaces the legacy InvestigativeSynthesisAgent.
"""

import json
import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from pathlib import Path
import yaml

from ...gateway.llm_gateway import LLMGateway
from ...gateway.model_registry import ModelRegistry
from ..comprehensive_knowledge_curator.agent import ComprehensiveKnowledgeCurator, KnowledgeQuery, KnowledgeResult

@dataclass
class SynthesisRequest:
    direct_context: Dict[str, Any]
    rag_curator: ComprehensiveKnowledgeCurator

@dataclass
class SynthesisResponse:
    success: bool
    final_report: str
    provenance_log: List[Dict[str, Any]]
    error_message: Optional[str] = None

class SequentialSynthesisAgent:
    """
    Executes the 5-step sequential synthesis pipeline.
    """
    def __init__(self, model: str, audit_logger=None):
        self.model = model
        self.model_registry = ModelRegistry()
        self.llm_gateway = LLMGateway(self.model_registry)
        self.logger = logging.getLogger(__name__)
        self.audit_logger = audit_logger
        self.prompts = self._load_prompts()
        self.provenance_log = []

    def _load_prompts(self) -> Dict[str, Any]:
        """Load YAML prompts from the 'prompts' directory."""
        prompts_path = Path(__file__).parent / "prompts/synthesis_prompts.yaml"
        with open(prompts_path, 'r') as f:
            return yaml.safe_load(f)

    def synthesize_research(self, request: SynthesisRequest) -> SynthesisResponse:
        """Execute the full 5-step sequential synthesis process."""
        self.provenance_log = []
        try:
            # Step 1: Hypothesis Testing
            hypothesis_queries = self._generate_queries(request, "hypothesis_analysis")
            hypothesis_evidence = self._query_rag(request.rag_curator, hypothesis_queries, ["evidence_quotes", "corpus_text"])
            hypothesis_findings = self._synthesize_step(request, "hypothesis_analysis", hypothesis_evidence)

            # Step 2: Statistical Anomaly Investigation
            anomaly_queries = self._generate_queries(request, "anomaly_investigation")
            anomaly_evidence = self._query_rag(request.rag_curator, anomaly_queries, ["raw_scores", "calculated_metrics", "evidence_quotes"])
            anomaly_findings = self._synthesize_step(request, "anomaly_investigation", anomaly_evidence)

            # Step 3: Cross-Dimensional Pattern Discovery
            pattern_queries = self._generate_queries(request, "pattern_discovery")
            pattern_evidence = self._query_rag(request.rag_curator, pattern_queries, ["calculated_metrics", "evidence_quotes"])
            pattern_findings = self._synthesize_step(request, "pattern_discovery", pattern_evidence)

            # Step 4: Statistical Framework Fit Assessment (with enhanced statistical data)
            framework_fit_assessment = self._synthesize_step(request, "framework_fit_assessment")

            # Step 5: Final Integration
            # Aggregate all retrieved evidence for the final report
            aggregated_evidence = {**hypothesis_evidence, **anomaly_evidence, **pattern_evidence}

            final_report = self._synthesize_step(
                request,
                "final_integration",
                retrieved_evidence=aggregated_evidence,
                previous_findings={
                    "hypothesis_findings": hypothesis_findings,
                    "anomaly_findings": anomaly_findings,
                    "pattern_findings": pattern_findings,
                    "framework_fit_assessment": framework_fit_assessment,
                }
            )

            return SynthesisResponse(
                success=True,
                final_report=final_report,
                provenance_log=self.provenance_log
            )

        except Exception as e:
            self.logger.error(f"Sequential synthesis pipeline failed: {e}", exc_info=True)
            return SynthesisResponse(success=False, final_report="", provenance_log=self.provenance_log, error_message=str(e))

    def _generate_queries(self, request: SynthesisRequest, step_name: str) -> List[str]:
        """Use the LLM to generate targeted RAG queries for a given synthesis step."""
        step_config = self.prompts['step_definitions'][step_name]
        prompt = self._render_prompt("query_generation_template", {
            "direct_context": json.dumps(request.direct_context, indent=2),
            "task_description": step_config['query_generation_task']
        })
        
        response_content, _ = self.llm_gateway.execute_call(model=self.model, prompt=prompt, system_prompt=self.prompts['system_prompts']['query_generator'])
        queries = self._extract_json_list(response_content)
        
        self.provenance_log.append({"step": step_name, "action": "generate_queries", "queries": queries, "llm_response": response_content})
        return queries

    def _query_rag(self, rag_curator: ComprehensiveKnowledgeCurator, queries: List[str], content_types: List[str]) -> Dict[str, List[KnowledgeResult]]:
        """Execute a batch of queries against the RAG index."""
        evidence_map = {}
        for query in queries:
            results = rag_curator.query_knowledge(KnowledgeQuery(semantic_query=query, content_types=content_types, limit=10))
            evidence_map[query] = results
        
        self.provenance_log.append({"step": "query_rag", "queries": queries, "content_types": content_types, "results_count": {q: len(r) for q, r in evidence_map.items()}})
        return evidence_map

    def _synthesize_step(self, request: SynthesisRequest, step_name: str, retrieved_evidence: Optional[Dict] = None, previous_findings: Optional[Dict] = None) -> str:
        """Execute a single synthesis step using the LLM."""
        step_config = self.prompts['step_definitions'][step_name]
        
        # Evidence Budgeting with rich metadata for proper citation
        budgeted_evidence_str = ""
        if retrieved_evidence:
            # Include rich evidence data for proper academic citation
            evidence_with_metadata = {}
            for query, results in retrieved_evidence.items():
                evidence_items = []
                for r in results[:3]:  # Top 3 results per query
                    evidence_item = {
                        "content": r.content,
                        "source_document": r.metadata.get('document_name', 'Unknown'),
                        "speaker": r.metadata.get('speaker', 'Unknown Speaker'),
                        "data_type": r.data_type,
                        "relevance_score": r.relevance_score
                    }
                    evidence_items.append(evidence_item)
                evidence_with_metadata[query] = evidence_items
            budgeted_evidence_str = json.dumps(evidence_with_metadata, indent=2)

        prompt = self._render_prompt("synthesis_step_template", {
            "direct_context": json.dumps(request.direct_context, indent=2),
            "retrieved_evidence": budgeted_evidence_str,
            "previous_findings": json.dumps(previous_findings, indent=2) if previous_findings else "N/A",
            "task_description": step_config['synthesis_task']
        })

        response_content, _ = self.llm_gateway.execute_call(model=self.model, prompt=prompt, system_prompt=self.prompts['system_prompts']['synthesis_researcher'])
        
        self.provenance_log.append({"step": step_name, "action": "synthesize", "llm_response": response_content})
        return response_content

    def _render_prompt(self, template_name: str, context: Dict[str, Any]) -> str:
        """Render a prompt template with the given context."""
        template = self.prompts['prompt_templates'][template_name]
        return template.format(**context)

    def _extract_json_list(self, llm_response: str) -> List[str]:
        """Extract a JSON list from a raw LLM response, handling markdown fences."""
        try:
            # Handle markdown code fences
            if "```json" in llm_response:
                llm_response = llm_response.split("```json")[1].split("```")[0]
            return json.loads(llm_response)
        except (json.JSONDecodeError, IndexError):
            self.logger.warning(f"Failed to parse JSON list from LLM response: {llm_response}")
            return []
