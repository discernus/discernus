#!/usr/bin/env python3
"""
V2 Evidence Retriever Agent - Simplified Version

Eliminates fragile parsing by using LLM intelligence to identify key findings.
This addresses the regression introduced during V2 refactoring where parsing
became brittle and maintenance-heavy.

THIN PRINCIPLE: Let the LLM figure out what's interesting instead of trying
to parse specific keys that may change between statistical agent versions.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from discernus.core.standard_agent import StandardAgent
from discernus.core.run_context import RunContext
from discernus.core.agent_result import AgentResult
from discernus.core.security_boundary import ExperimentSecurityBoundary
from discernus.core.local_artifact_storage import LocalArtifactStorage
from discernus.core.audit_logger import AuditLogger
from discernus.gateway.llm_gateway import LLMGateway
from discernus.gateway.model_registry import ModelRegistry
from discernus.core.rag_index_manager import RAGIndexManager


class V2EvidenceRetrieverAgent(StandardAgent):
    """
    Simplified V2 evidence retrieval agent that uses LLM intelligence
    instead of fragile parsing to identify key findings.
    """

    def __init__(self, 
                 security: ExperimentSecurityBoundary,
                 storage: LocalArtifactStorage,
                 audit: AuditLogger,
                 config: Optional[Dict[str, Any]] = None):
        """Initialize the simplified evidence retrieval agent."""
        super().__init__(security, storage, audit, config)
        self.agent_name = "V2EvidenceRetrieverAgent"
        self.logger = logging.getLogger(__name__)

        # Initialize LLM gateway
        model_registry = ModelRegistry()
        self.llm_gateway = LLMGateway(model_registry)

        # RAG Index Manager for evidence retrieval
        self.rag_manager = RAGIndexManager(storage, audit, security)
        
        self.logger.info(f"Initialized {self.agent_name}")

    def get_capabilities(self) -> List[str]:
        """Return the capabilities of this evidence retrieval agent."""
        return [
            "evidence_retrieval",
            "rag_search", 
            "semantic_search",
            "framework_agnostic_analysis",
            "tool_calling",
            "structured_output"
        ]

    def execute(self, run_context: RunContext, **kwargs) -> AgentResult:
        """
        Execute evidence retrieval using V2 interface.
        
        Args:
            run_context: The RunContext object
            **kwargs: Additional execution parameters
            
        Returns:
            AgentResult with evidence retrieval results
        """
        try:
            self.logger.info("V2EvidenceRetrieverAgentSimplified starting execution")
            self.log_execution_start(run_context=run_context, **kwargs)

            # 1. Validate inputs from RunContext
            self.logger.info("Starting evidence retrieval validation...")
            framework_content, statistical_results, corpus_documents = self._validate_and_extract_inputs(run_context)
            self.logger.info("Evidence retrieval validation completed successfully")

            # 2. Build or load a cached RAG index from the corpus documents
            index_cache_key = self.rag_manager.get_corpus_cache_key(corpus_documents)
            if not self.rag_manager.is_index_cached(index_cache_key):
                self.logger.info(f"Building new RAG index with cache key: {index_cache_key}")
                self.rag_manager.build_index_from_corpus(corpus_documents, index_cache_key)
            else:
                self.logger.info(f"Loading cached RAG index with cache key: {index_cache_key}")
                self.rag_manager.load_index(index_cache_key)

            # 3. Use LLM to identify key statistical findings that require evidence
            self.logger.info("Extracting key findings from statistical results...")
            key_findings = self._extract_key_findings(statistical_results)
            self.logger.info(f"Found {len(key_findings)} key findings")
            
            if not key_findings:
                self.logger.warning("No key statistical findings were identified by the LLM. Cannot proceed with evidence retrieval.")
                return AgentResult(
                    success=False,
                    artifacts=[],
                    metadata={"agent_name": self.agent_name, "error": "No key statistical findings identified"},
                    error_message="No key statistical findings were identified by the LLM. Cannot proceed with evidence retrieval."
                )

            # 4. Retrieve evidence for each finding using RAG
            self.logger.info("Retrieving evidence for key findings...")
            evidence_results = self._llm_driven_evidence_retrieval(framework_content, statistical_results)
            
            # 5. Store evidence results
            artifact_hash = self._store_evidence_results(evidence_results, run_context)
            
            # 6. Log completion and return success
            result = AgentResult(
                success=True,
                artifacts=[artifact_hash],
                metadata={
                    "agent_name": self.agent_name,
                    "findings_processed": len(key_findings),
                    "evidence_quotes_found": sum(len(er.get('quotes', [])) for er in evidence_results),
                    "evidence_artifact_hash": artifact_hash
                }
            )
            self.log_execution_complete(result)
            return result

        except Exception as e:
            self.logger.error(f"Evidence retrieval failed: {str(e)}")
            return AgentResult(
                success=False,
                artifacts=[],
                metadata={"agent_name": self.agent_name, "error": str(e)},
                error_message=str(e)
            )

    def _validate_and_extract_inputs(self, run_context: RunContext) -> tuple:
        """Validate RunContext and extract required data."""
        if not run_context:
            raise ValueError("RunContext is required.")

        # Required metadata fields
        framework_content = run_context.metadata.get("framework_content")
        if not framework_content:
            raise ValueError("RunContext metadata is missing required field: framework_content")

        corpus_documents = run_context.metadata.get("corpus_documents")
        if not corpus_documents:
            raise ValueError("RunContext metadata is missing required field: corpus_documents")

        # Statistical results from previous phase
        statistical_results = run_context.statistical_results
        if not statistical_results:
            raise ValueError("RunContext is missing required field: statistical_results")

        return framework_content, statistical_results, corpus_documents

    def _extract_key_findings(self, statistical_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extract key findings from statistical results using LLM intelligence.
        
        THIN PRINCIPLE: Let the LLM figure out what's interesting instead of fragile parsing.
        This eliminates the maintenance burden of keeping up with changing output formats.
        """
        try:
            # Use LLM to identify key findings from the full statistical results
            # This is more robust than trying to parse specific keys that may change
            prompt = f"""
You are analyzing statistical results from a discourse analysis experiment. 
Identify the most important and interesting findings that would benefit from textual evidence support.

STATISTICAL RESULTS:
{json.dumps(statistical_results, indent=2, default=str)}

Please identify 5-10 key findings that are:
1. Statistically significant or noteworthy
2. Would benefit from textual evidence to support the claims
3. Most important for understanding the research question

Return your response as a JSON array of findings, each with this structure:
{{
  "finding": "Clear description of the statistical finding",
  "dimension": "The specific metric or dimension being analyzed", 
  "type": "descriptive|comparative|correlation|other",
  "significance": "Why this finding is important",
  "evidence_queries": ["query1", "query2", "query3"]
}}

Focus on the most impactful findings that would benefit from textual evidence.
"""
            
            response, metadata = self.llm_gateway.execute_call(
                model="vertex_ai/gemini-2.5-flash-lite",
                prompt=prompt,
                system_prompt="You are a helpful assistant analyzing statistical results.",
                temperature=0.1
            )
            
            # Parse the LLM response
            try:
                # Extract JSON from response
                if '```json' in response:
                    start_idx = response.find('```json') + 7
                    end_idx = response.rfind('```')
                    if end_idx > start_idx:
                        json_str = response[start_idx:end_idx].strip()
                    else:
                        json_str = response
                else:
                    json_str = response
                
                findings = json.loads(json_str)
                if isinstance(findings, list):
                    self.logger.info(f"LLM identified {len(findings)} key findings")
                    return findings
                else:
                    self.logger.warning(f"LLM returned non-list findings: {type(findings)}")
                    return []
                    
            except (json.JSONDecodeError, KeyError) as e:
                self.logger.error(f"Failed to parse LLM findings response: {e}")
                return []
            
        except Exception as e:
            self.logger.error(f"Failed to extract key findings: {e}")
            return []

    def _llm_driven_evidence_retrieval(self, framework_spec: Dict[str, Any], statistical_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Retrieve evidence using iterative LLM-driven curation approach."""
        try:
            # Create evidence retrieval prompt
            prompt = self._create_evidence_retrieval_prompt(framework_spec, statistical_results)
            
            # Get LLM response
            response, metadata = self.llm_gateway.execute_call(
                model="vertex_ai/gemini-2.5-flash",
                prompt=prompt,
                system_prompt="You are a helpful assistant for evidence retrieval.",
                temperature=0.1
            )
            
            # Parse response
            evidence_plan = self._parse_llm_response(response)
            
            # Execute iterative evidence curation
            evidence_results = []
            for finding in evidence_plan.get('key_findings', []):
                finding_description = finding.get('finding', '')
                initial_queries = finding.get('queries', [])
                
                # Use iterative curation to find the best quotes
                curated_quotes = self._iterative_quote_curation(
                    finding_description, 
                    initial_queries,
                    max_iterations=3,
                    max_quotes_per_finding=5
                )
                
                evidence_results.append({
                    "finding": finding_description,
                    "dimension": finding.get('dimension', ''),
                    "quotes": curated_quotes
                })
            
            return evidence_results
            
        except Exception as e:
            self.logger.error(f"Failed to retrieve evidence: {e}")
            raise

    def _iterative_quote_curation(self, finding_description: str, initial_queries: List[str], 
                                 max_iterations: int = 3, max_quotes_per_finding: int = 5) -> List[Dict[str, Any]]:
        """
        Iteratively curate the best quotes for a finding using LLM intelligence.
        
        This allows the LLM to:
        1. Start with broad searches to get many candidates
        2. Review and select the best quotes
        3. Refine queries if needed to find better evidence
        4. Stop when satisfied or hit limits
        """
        all_candidates = []
        seen_quotes = set()
        current_queries = initial_queries.copy()
        
        for iteration in range(max_iterations):
            self.logger.info(f"Evidence curation iteration {iteration + 1}/{max_iterations} for finding: {finding_description[:50]}...")
            
            # Search for new candidates with current queries
            new_candidates = []
            for query in current_queries:
                search_results = self.rag_manager.search(query, top_k=5)  # Get more candidates
                for result in search_results:
                    quote_text = result.get('text', '')
                    if quote_text and quote_text not in seen_quotes:
                        seen_quotes.add(quote_text)
                        new_candidates.append({
                            "text": quote_text,
                            "relevance_score": result.get('score', 0.0),
                            "query": query,
                            "iteration": iteration + 1
                        })
            
            all_candidates.extend(new_candidates)
            
            # If we have enough candidates, let LLM curate them
            if len(all_candidates) >= max_quotes_per_finding or iteration == max_iterations - 1:
                curated_quotes = self._llm_curate_quotes(
                    finding_description, 
                    all_candidates, 
                    max_quotes_per_finding
                )
                
                if curated_quotes:
                    self.logger.info(f"Found {len(curated_quotes)} curated quotes for finding")
                    return curated_quotes
                elif iteration < max_iterations - 1:
                    # LLM wasn't satisfied, try refined queries
                    current_queries = self._generate_refined_queries(finding_description, all_candidates)
                    if not current_queries:
                        break
                else:
                    # Last iteration, return best candidates by score
                    return sorted(all_candidates, key=lambda x: x['relevance_score'], reverse=True)[:max_quotes_per_finding]
        
        # Fallback: return best candidates by relevance score
        return sorted(all_candidates, key=lambda x: x['relevance_score'], reverse=True)[:max_quotes_per_finding]

    def _llm_curate_quotes(self, finding_description: str, candidates: List[Dict[str, Any]], 
                          max_quotes: int) -> List[Dict[str, Any]]:
        """Use LLM to curate the best quotes from candidates."""
        if not candidates:
            return []
        
        # Create curation prompt
        candidates_text = "\n".join([
            f"{i+1}. Score: {c['relevance_score']:.3f} | Query: {c['query']} | Text: {c['text'][:200]}..."
            for i, c in enumerate(candidates[:20])  # Limit to top 20 for prompt efficiency
        ])
        
        prompt = f"""
You are curating evidence quotes for this statistical finding:

FINDING: {finding_description}

CANDIDATE QUOTES:
{candidates_text}

Select the BEST {max_quotes} quotes that most strongly support this finding. Consider:
- Relevance to the finding
- Clarity and impact of the quote
- Uniqueness (avoid similar quotes)
- Quality of evidence

Return ONLY the numbers of the selected quotes (e.g., "1, 3, 7, 12, 15").
If no quotes are suitable, return "NONE".
"""
        
        try:
            response, _ = self.llm_gateway.execute_call(
                model="vertex_ai/gemini-2.5-flash",
                prompt=prompt,
                system_prompt="You are a helpful assistant for evidence curation.",
                temperature=0.1
            )
            
            # Parse selected quote indices
            if "NONE" in response.upper():
                return []
            
            selected_indices = []
            for part in response.split(','):
                try:
                    idx = int(part.strip()) - 1  # Convert to 0-based index
                    if 0 <= idx < len(candidates):
                        selected_indices.append(idx)
                except ValueError:
                    continue
            
            # Return selected quotes
            selected_quotes = [candidates[i] for i in selected_indices if i < len(candidates)]
            return selected_quotes[:max_quotes]
            
        except Exception as e:
            self.logger.error(f"Failed to curate quotes: {e}")
            return []

    def _generate_refined_queries(self, finding_description: str, candidates: List[Dict[str, Any]]) -> List[str]:
        """Generate refined search queries based on what we've found so far."""
        if not candidates:
            return []
        
        # Analyze what we've found to generate better queries
        prompt = f"""
FINDING: {finding_description}

CURRENT CANDIDATES FOUND: {len(candidates)}
Top candidates by score:
{chr(10).join([f"- {c['text'][:100]}... (score: {c['relevance_score']:.3f})" for c in sorted(candidates, key=lambda x: x['relevance_score'], reverse=True)[:5]])}

Generate 2-3 refined search queries that might find BETTER evidence for this finding.
Focus on different angles or more specific terms that might yield stronger quotes.

Return only the queries, one per line.
"""
        
        try:
            response, _ = self.llm_gateway.execute_call(
                model="vertex_ai/gemini-2.5-flash",
                prompt=prompt,
                system_prompt="You are a helpful assistant for query refinement.",
                temperature=0.3
            )
            
            # Parse queries from response
            queries = [line.strip() for line in response.split('\n') if line.strip()]
            return queries[:3]  # Limit to 3 refined queries
            
        except Exception as e:
            self.logger.error(f"Failed to generate refined queries: {e}")
            return []

    def _create_evidence_retrieval_prompt(self, framework_spec: Dict[str, Any], statistical_results: Dict[str, Any]) -> str:
        """Create prompt for evidence retrieval."""
        json_safe_statistical_results = self._convert_tuple_keys(statistical_results)
        
        prompt = f"""
Hi. Here is a framework and statistical results of scoring data based on that framework.

## FRAMEWORK SPECIFICATION
{json.dumps(framework_spec, indent=2)}

## STATISTICAL RESULTS
{json.dumps(json_safe_statistical_results, indent=2)}

Your job is to query this RAG index to curate evidence quotes that correspond to the statistical findings.

## PRIORITIZATION GUIDELINES
- Focus on the MOST SIGNIFICANT statistical patterns (strongest correlations, highest variance, most extreme scores)
- Prioritize findings that would benefit most from textual evidence support
- Avoid minor correlations or statistical noise
- Aim for quality over quantity

## YOUR DELIVERABLE
Provide a structured plan for evidence retrieval that includes:

1. **Top 10-15 Key Findings** - The most important statistical patterns requiring evidence
2. **Evidence Queries** - Specific search terms for each finding (2-3 queries per finding)
3. **Quality Criteria** - How to filter and rank evidence quotes
4. **Expected Output** - Target 20-30 high-quality quotes total, not hundreds

## FRAMEWORK CONTEXT
Use the framework specification to understand what dimensions and metrics are being analyzed.
Generate queries that make sense within the framework's analytical approach.

## RESPONSE FORMAT
You must wrap your response in the following delimiters:

<<<DISCERNUS_EVIDENCE_PLAN>>>
{{
  "key_findings": [
    {{
      "finding": "Description of the statistical finding",
      "queries": ["query1", "query2", "query3"]
    }}
  ],
  "quality_criteria": {{
    "min_relevance": 0.5,
    "max_quotes_per_finding": 3
  }},
  "target_total_quotes": 25
}}
<<<END_DISCERNUS_EVIDENCE_PLAN>>>

IMPORTANT: Your response must be valid JSON and must be wrapped in the exact delimiters shown above.
"""
        return prompt

    def _parse_llm_response(self, response: str) -> Dict[str, Any]:
        """Parse LLM response to extract evidence plan."""
        try:
            # Extract content between delimiters
            start_marker = "<<<DISCERNUS_EVIDENCE_PLAN>>>"
            end_marker = "<<<END_DISCERNUS_EVIDENCE_PLAN>>>"
            
            start_idx = response.find(start_marker)
            end_idx = response.find(end_marker)
            
            if start_idx == -1 or end_idx == -1:
                raise ValueError("Response missing required delimiters")
            
            json_str = response[start_idx + len(start_marker):end_idx].strip()
            return json.loads(json_str)
            
        except (json.JSONDecodeError, ValueError) as e:
            self.logger.error(f"Failed to parse LLM response: {e}")
            return {"key_findings": []}

    def _convert_tuple_keys(self, obj: Any) -> Any:
        """Convert tuple keys to strings for JSON serialization."""
        if isinstance(obj, dict):
            return {str(k): self._convert_tuple_keys(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._convert_tuple_keys(item) for item in obj]
        else:
            return obj

    def _store_evidence_results(self, evidence_results: List[Dict[str, Any]], run_context: RunContext) -> str:
        """Store evidence results and return artifact hash."""
        try:
            # Create evidence results artifact
            evidence_artifact = {
                "agent_name": self.agent_name,
                "timestamp": run_context.last_updated.isoformat() if run_context.last_updated else datetime.now().isoformat(),
                "experiment_id": run_context.experiment_id,
                "evidence_results": evidence_results,
                "total_findings": len(evidence_results),
                "total_quotes": sum(len(er.get('quotes', [])) for er in evidence_results)
            }
            
            # Store artifact
            artifact_hash = self.storage.store_artifact(
                content=evidence_artifact,
                artifact_type="evidence_retrieval_results",
                experiment_id=run_context.experiment_id
            )
            
            self.logger.info(f"Stored evidence results with hash: {artifact_hash}")
            return artifact_hash
            
        except Exception as e:
            self.logger.error(f"Failed to store evidence results: {e}")
            raise
