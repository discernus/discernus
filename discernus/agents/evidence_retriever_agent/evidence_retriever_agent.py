#!/usr/bin/env python3
"""
EvidenceRetriever Agent

A simple, focused agent that:
1. Loads framework specification and statistical results
2. Uses LLM to intelligently identify key findings and generate evidence queries
3. Retrieves relevant evidence quotes using EvidenceMatchingWrapper
4. Stores evidence in a structured, content-addressable file

This agent follows the THIN principle - one job, clear responsibility.
"""

import json
import logging
import re
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

from ...core.evidence_matching_wrapper import EvidenceMatchingWrapper
from ...core.local_artifact_storage import LocalArtifactStorage
from ...core.security_boundary import ExperimentSecurityBoundary
from ...core.audit_logger import AuditLogger
from ...gateway.llm_gateway import LLMGateway
from ...gateway.model_registry import get_model_registry


class EvidenceRetrieverAgent:
    """
    Agent responsible for retrieving evidence quotes to support statistical findings.
    
    This agent works independently to gather evidence, making it available
    for other agents (like synthesis) to consume.
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.agent_name = "EvidenceRetriever"
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.experiment_path = Path(config.get('experiment_path', '.'))
        self.run_id = config.get('run_id', 'default_run')
        self.security_boundary = ExperimentSecurityBoundary(self.experiment_path)
        # Use shared artifact storage if provided, otherwise create new instance
        if 'artifact_storage' in config:
            self.artifact_storage = config['artifact_storage']
            self.logger.info("Using shared artifact storage instance")
        else:
            # Use the existing shared cache artifacts directory
            self.artifact_storage = LocalArtifactStorage(self.security_boundary, self.experiment_path / "shared_cache")
            self.logger.info("Created new artifact storage instance")
        self.llm_gateway = LLMGateway(get_model_registry())
        self.audit_logger = AuditLogger(self.security_boundary, self.experiment_path / "session" / self.run_id)
        
        # Evidence wrapper for semantic search
        self.evidence_wrapper = None
        
    def run(self, **kwargs) -> Dict[str, Any]:
        """
        Main execution method for evidence retrieval.
        
        Args:
            framework_hash: Hash of framework specification artifact
            statistical_results_hash: Hash of statistical results artifact
            evidence_artifact_hashes: List of evidence artifact hashes
            
        Returns:
            Dictionary containing evidence retrieval results and artifact hash
        """
        try:
            self.logger.info("Starting evidence retrieval process...")
            
            # Extract parameters
            framework_hash = kwargs.get('framework_hash')
            statistical_results_hash = kwargs.get('statistical_results_hash')
            evidence_artifact_hashes = kwargs.get('evidence_artifact_hashes', [])
            
            if not framework_hash:
                raise ValueError("framework_hash is required")
            if not statistical_results_hash:
                raise ValueError("statistical_results_hash is required")
            if not evidence_artifact_hashes:
                raise ValueError("evidence_artifact_hashes list is required")
            
            # Step 1: Load framework and statistical results
            self.logger.info("Step 1: Loading framework and statistical results...")
            try:
                framework_spec = self._load_framework_specification(framework_hash)
                statistical_results = self._load_statistical_results(statistical_results_hash)
                self.logger.info("Successfully loaded framework and statistical results")
            except Exception as e:
                self.logger.error(f"Failed to load framework or statistical results: {e}")
                self.logger.info("Falling back to basic evidence retrieval due to artifact loading failure")
                # Still need to build evidence wrapper for fallback
                self.evidence_wrapper = self._build_evidence_wrapper(evidence_artifact_hashes)
                if not self.evidence_wrapper:
                    raise RuntimeError("Failed to build evidence wrapper")
                # Fall back to basic evidence retrieval
                evidence_results = self._fallback_evidence_retrieval({})
                evidence_artifact_hash = self._store_evidence_results(evidence_results, statistical_results_hash)
                return {
                    "status": "success_fallback",
                    "framework": "unknown_due_to_loading_failure",
                    "evidence_quotes_found": sum(len(result['quotes']) for result in evidence_results),
                    "evidence_artifact_hash": evidence_artifact_hash,
                    "evidence_results": evidence_results
                }
            
            # Step 2: Build evidence wrapper
            self.logger.info("Step 2: Building evidence wrapper...")
            self.evidence_wrapper = self._build_evidence_wrapper(evidence_artifact_hashes)
            
            if not self.evidence_wrapper:
                raise RuntimeError("Failed to build evidence wrapper")
            
            # Step 3: Use LLM to identify key findings and retrieve evidence
            self.logger.info("Step 3: Using LLM to identify findings and retrieve evidence...")
            evidence_results = self._llm_driven_evidence_retrieval(framework_spec, statistical_results)
            
            # Step 4: Store evidence results
            self.logger.info("Step 4: Storing evidence results...")
            evidence_artifact_hash = self._store_evidence_results(evidence_results, statistical_results_hash)
            
            # Log success
            if self.audit_logger:
                self.audit_logger.log_agent_event(
                    self.agent_name,
                    "evidence_retrieval_complete",
                    {
                        "framework": framework_spec.get('name', 'Unknown'),
                        "evidence_quotes_found": sum(len(result['quotes']) for result in evidence_results),
                        "evidence_artifact_hash": evidence_artifact_hash
                    }
                )
            
            return {
                "status": "success",
                "framework": framework_spec.get('name', 'Unknown'),
                "evidence_quotes_found": sum(len(result['quotes']) for result in evidence_results),
                "evidence_artifact_hash": evidence_artifact_hash,
                "evidence_results": evidence_results
            }
            
        except Exception as e:
            self.logger.error(f"Evidence retrieval failed: {e}")
            if self.audit_logger:
                self.audit_logger.log_error(
                    "evidence_retrieval_failed",
                    str(e),
                    {"agent": self.agent_name}
                )
            raise
    
    def _load_framework_specification(self, framework_hash: str) -> Dict[str, Any]:
        """Load framework specification from artifact storage."""
        try:
            content = self.artifact_storage.get_artifact(framework_hash)
            if not content:
                raise ValueError(f"Framework specification artifact not found: {framework_hash}")
            
            return json.loads(content.decode('utf-8'))
            
        except Exception as e:
            self.logger.error(f"Failed to load framework specification: {e}")
            raise
    
    def _load_statistical_results(self, statistical_results_hash: str) -> Dict[str, Any]:
        """Load statistical results from artifact storage."""
        try:
            content = self.artifact_storage.get_artifact(statistical_results_hash)
            if not content:
                raise ValueError(f"Statistical results artifact not found: {statistical_results_hash}")
            
            return json.loads(content.decode('utf-8'))
            
        except Exception as e:
            self.logger.error(f"Failed to load statistical results: {e}")
            raise
    
    def _build_evidence_wrapper(self, evidence_artifact_hashes: List[str]) -> Optional[EvidenceMatchingWrapper]:
        """Build the evidence wrapper from artifact hashes."""
        try:
            wrapper = EvidenceMatchingWrapper(
                model="vertex_ai/gemini-2.5-flash",
                artifact_storage=self.artifact_storage,
                audit_logger=self.audit_logger
            )
            
            # Build the index
            success = wrapper.build_index(evidence_artifact_hashes)
            if not success:
                self.logger.error("Failed to build evidence index")
                return None
            
            self.logger.info(f"Successfully built evidence wrapper with {len(wrapper.evidence_data)} evidence pieces")
            return wrapper
            
        except Exception as e:
            self.logger.error(f"Failed to build evidence wrapper: {e}")
            return None
    
    def _llm_driven_evidence_retrieval(self, framework_spec: Dict[str, Any], statistical_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Use LLM to intelligently identify key findings and retrieve relevant evidence.
        
        This method uses natural language prompts to make the agent framework-agnostic.
        """
        try:
            # Create the natural language prompt for the LLM
            prompt = self._create_evidence_retrieval_prompt(framework_spec, statistical_results)
            
            # Get LLM response for evidence retrieval strategy
            response, metadata = self.llm_gateway.execute_call(
                model="vertex_ai/gemini-2.5-flash",
                prompt=prompt,
                system_prompt="You are an expert research analyst specializing in evidence curation and statistical interpretation."
            )
            
            # Parse the LLM response to get evidence retrieval plan
            evidence_plan = self._parse_llm_response(response)
            
            # Execute the evidence retrieval plan
            evidence_results = self._execute_evidence_plan(evidence_plan)
            
            return evidence_results
            
        except Exception as e:
            self.logger.error(f"LLM-driven evidence retrieval failed: {e}")
            # Fallback to basic evidence retrieval
            return self._fallback_evidence_retrieval(statistical_results)
    
    def _create_evidence_retrieval_prompt(self, framework_spec: Dict[str, Any], statistical_results: Dict[str, Any]) -> str:
        """Create natural language prompt for evidence retrieval."""
        
        prompt = f"""
Hi. Here is a framework and statistical results of scoring data based on that framework.

## FRAMEWORK SPECIFICATION
{json.dumps(framework_spec, indent=2)}

## STATISTICAL RESULTS
{json.dumps(statistical_results, indent=2)}

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
        """
        Parse LLM response to extract the evidence retrieval plan.
        
        The method looks for content wrapped in proprietary delimiters and parses it as JSON.
        """
        try:
            # Use regex to find content between proprietary delimiters
            start_marker = '<<<DISCERNUS_EVIDENCE_PLAN>>>'
            end_marker = '<<<END_DISCERNUS_EVIDENCE_PLAN>>>'
            
            start_idx = response.find(start_marker)
            end_idx = response.find(end_marker)
            
            if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
                # Extract content between delimiters
                start_content = start_idx + len(start_marker)
                json_string = response[start_content:end_idx].strip()
                
                # Parse the JSON content
                plan = json.loads(json_string)
                self.logger.info(f"Successfully parsed evidence retrieval plan with {len(plan.get('key_findings', []))} findings.")
                return plan
            else:
                self.logger.warning("No proprietary delimiters found in LLM response. Could not parse plan.")
                self.logger.debug(f"Response content: {response[:500]}...")
                # Fallback if no delimiters are found
                return self._create_fallback_plan()

        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to decode JSON from LLM response: {e}")
            self.logger.debug(f"LLM Response Content: {response}")
            return self._create_fallback_plan()
        except Exception as e:
            self.logger.warning(f"An unexpected error occurred while parsing LLM response, using fallback: {e}")
            return self._create_fallback_plan()
    
    def _execute_evidence_plan(self, evidence_plan: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Execute the evidence retrieval plan by querying the RAG wrapper.
        
        This method iterates through each finding in the plan, runs the associated
        queries, and aggregates the retrieved evidence.
        """
        if not self.evidence_wrapper:
            self.logger.error("Evidence wrapper is not initialized. Cannot execute plan.")
            return []
            
        if not isinstance(evidence_plan, dict) or 'key_findings' not in evidence_plan:
            self.logger.warning("Invalid or empty evidence plan provided. Using fallback.")
            return self._fallback_evidence_retrieval({})

        key_findings = evidence_plan.get('key_findings', [])
        if not key_findings:
            self.logger.warning("No key findings in evidence plan. Using fallback.")
            return self._fallback_evidence_retrieval({})

        self.logger.info(f"Executing evidence retrieval plan with {len(key_findings)} findings.")
        
        all_results = []
        
        for finding_item in key_findings:
            finding_description = finding_item.get("finding")
            queries = finding_item.get("queries", [])
            
            if not finding_description or not queries:
                self.logger.warning(f"Skipping invalid finding item: {finding_item}")
                continue

            self.logger.debug(f"Processing finding: '{finding_description}' with queries: {queries}")
            
            # Use a set to store unique quotes for this finding
            unique_quotes_for_finding = {}

            for query in queries:
                try:
                    # Search for evidence with a reasonable limit per query
                    quotes = self.evidence_wrapper.search_evidence(query, limit=3)
                    for quote in quotes:
                        # Use quote_text as the key to ensure uniqueness
                        unique_quotes_for_finding[quote.get('quote_text')] = quote
                except Exception as e:
                    self.logger.error(f"Failed to execute query '{query}' for finding '{finding_description}': {e}")
            
            if unique_quotes_for_finding:
                # Sort the collected quotes by relevance score, descending
                sorted_quotes = sorted(list(unique_quotes_for_finding.values()), 
                                       key=lambda x: x.get('relevance_score', 0.0), 
                                       reverse=True)
                
                all_results.append({
                    "finding": {"type": "llm_generated", "description": finding_description},
                    "queries_used": queries,
                    "quotes": sorted_quotes,
                    "total_quotes_found": len(sorted_quotes)
                })

        self.logger.info(f"Evidence plan execution complete. Found evidence for {len(all_results)} findings.")
        return all_results
    
    def _fallback_evidence_retrieval(self, statistical_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Fallback evidence retrieval when LLM approach fails."""
        try:
            # Basic evidence retrieval for key statistical patterns
            basic_queries = [
                "correlation analysis",
                "statistical patterns", 
                "framework analysis",
                "evidence examples",
                "key findings"
            ]
            
            evidence_results = []
            for query in basic_queries:
                quotes = self.evidence_wrapper.search_evidence(query, limit=2)
                if quotes:
                    evidence_results.append({
                        "finding": {"type": "fallback", "description": f"Evidence for {query}"},
                        "queries_used": [query],
                        "quotes": quotes,
                        "total_quotes_found": len(quotes)
                    })
            
            return evidence_results[:10]  # Limit to 10 findings
            
        except Exception as e:
            self.logger.error(f"Fallback evidence retrieval failed: {e}")
            return []
    
    def _create_fallback_plan(self) -> Dict[str, Any]:
        """Create a basic fallback evidence retrieval plan."""
        return {
            "key_findings": [],
            "evidence_queries": ["correlation", "pattern", "analysis"],
            "quality_criteria": {"min_relevance": 0.5},
            "target_quotes": 20
        }
    
    def _store_evidence_results(self, evidence_results: List[Dict[str, Any]], 
                               statistical_results_hash: str) -> str:
        """Store evidence results in a content-addressable file."""
        try:
            # Create evidence artifact
            evidence_artifact = {
                "metadata": {
                    "agent": self.agent_name,
                    "timestamp": datetime.utcnow().isoformat(),
                    "statistical_results_hash": statistical_results_hash,
                    "total_findings": len(evidence_results),
                    "total_quotes": sum(len(result['quotes']) for result in evidence_results)
                },
                "evidence_results": evidence_results
            }
            
            # Convert to JSON and store
            content = json.dumps(evidence_artifact, indent=2).encode('utf-8')
            metadata = {
                "artifact_type": "evidence_retrieval_results",
                "agent": self.agent_name,
                "type": "evidence_retrieval"
            }
            artifact_hash = self.artifact_storage.put_artifact(content, metadata)
            
            self.logger.info(f"Stored evidence results with hash: {artifact_hash}")
            return artifact_hash
            
        except Exception as e:
            self.logger.error(f"Failed to store evidence results: {e}")
            raise
