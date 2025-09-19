#!/usr/bin/env python3
"""
V2 EvidenceRetriever Agent
==========================

A V2-compliant agent that retrieves evidence quotes to support statistical findings.
This agent follows the V2 StandardAgent interface and consolidates all RAG logic.
"""

import json
import logging
import re
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

from ...core.standard_agent import StandardAgent
from ...core.agent_base_classes import ToolCallingAgent
from ...core.agent_result import AgentResult
from ...core.run_context import RunContext
from ...core.agent_config import AgentConfig
from ...core.evidence_matching_wrapper import EvidenceMatchingWrapper
from ...core.local_artifact_storage import LocalArtifactStorage
from ...core.security_boundary import ExperimentSecurityBoundary
from ...core.audit_logger import AuditLogger
from ...gateway.llm_gateway import LLMGateway
from ...gateway.model_registry import get_model_registry


class V2EvidenceRetrieverAgent(ToolCallingAgent):
    """
    V2-compliant agent responsible for retrieving evidence quotes to support statistical findings.
    
    This agent consolidates all RAG logic and follows the V2 StandardAgent interface.
    It uses RunContext for data handoffs and AgentConfig for configuration.
    """
    
    def __init__(self, 
                 security: ExperimentSecurityBoundary,
                 storage: LocalArtifactStorage,
                 audit: AuditLogger,
                 config: Optional[AgentConfig] = None):
        """
        Initialize the V2 EvidenceRetrieverAgent.
        
        Args:
            security: Security boundary for the experiment
            storage: Artifact storage for persistence
            audit: Audit logger for provenance tracking
            config: Agent configuration
        """
        super().__init__(security, storage, audit, config)
        
        self.agent_name = "V2EvidenceRetriever"
        self.logger = logging.getLogger(__name__)
        
        # Initialize LLM gateway
        self.llm_gateway = LLMGateway(get_model_registry())
        
        # Evidence wrapper for semantic search
        self.evidence_wrapper = None
        
        # RAG index for evidence retrieval
        self.rag_index = None
    
    def execute(self, **kwargs) -> AgentResult:
        """
        Execute evidence retrieval using V2 interface.
        
        Args:
            **kwargs: Execution parameters including RunContext
            
        Returns:
            AgentResult with evidence retrieval results
        """
        try:
            self.log_execution_start(**kwargs)
            
            # Extract RunContext from kwargs
            run_context = kwargs.get('run_context')
            if not run_context:
                raise ValueError("run_context is required")
            
            if not isinstance(run_context, RunContext):
                raise ValueError("run_context must be a RunContext instance")
            
            # Update phase
            run_context.update_phase("evidence_retrieval")
            
            # Get required data from RunContext
            framework_path = run_context.framework_path
            statistical_results = run_context.statistical_results
            analysis_artifacts = run_context.analysis_artifacts
            
            if not framework_path:
                raise ValueError("framework_path not found in RunContext")
            if not statistical_results:
                raise ValueError("statistical_results not found in RunContext")
            if not analysis_artifacts:
                raise ValueError("analysis_artifacts not found in RunContext")
            
            # Step 1: Load framework specification
            self.logger.info("Step 1: Loading framework specification...")
            framework_spec = self._load_framework_from_path(framework_path)
            
            # Step 2: Find evidence artifacts from analysis artifacts
            self.logger.info("Step 2: Finding evidence artifacts from analysis artifacts...")
            evidence_artifact_hashes = self._find_evidence_artifacts_from_analysis(analysis_artifacts)
            
            # Step 3: Build evidence wrapper
            self.logger.info("Step 3: Building evidence wrapper...")
            self.evidence_wrapper = self._build_evidence_wrapper(evidence_artifact_hashes)
            if not self.evidence_wrapper:
                raise RuntimeError("Failed to build evidence wrapper")
            
            # Step 4: Use LLM to identify key findings and retrieve evidence
            self.logger.info("Step 4: Using LLM to identify findings and retrieve evidence...")
            evidence_results = self._llm_driven_evidence_retrieval(framework_spec, statistical_results)
            
            # Step 5: Store evidence results
            self.logger.info("Step 5: Storing evidence results...")
            framework_hash = self._calculate_framework_hash(framework_path)
            evidence_artifact_hash = self._store_evidence_results(evidence_results, framework_hash)
            
            # Update RunContext with results
            run_context.evidence = {
                "evidence_results": evidence_results,
                "evidence_quotes_found": sum(len(result['quotes']) for result in evidence_results),
                "framework": framework_spec.get('name', 'Unknown')
            }
            run_context.add_artifact("evidence", evidence_artifact_hash, evidence_artifact_hash)
            
            # Log success
            self.audit.log_agent_event("evidence_retrieval_complete", {
                "framework": framework_spec.get('name', 'Unknown'),
                "evidence_quotes_found": sum(len(result['quotes']) for result in evidence_results),
                "evidence_artifact_hash": evidence_artifact_hash
            })
            
            # Create result
            result = AgentResult(
                success=True,
                artifacts=[evidence_artifact_hash],
                metadata={
                    "framework": framework_spec.get('name', 'Unknown'),
                    "evidence_quotes_found": sum(len(result['quotes']) for result in evidence_results),
                    "findings_processed": len(evidence_results)
                }
            )
            
            self.log_execution_complete(result)
            return result
            
        except Exception as e:
            self.logger.error(f"Evidence retrieval failed: {e}")
            self.log_execution_error(e)
            
            return AgentResult(
                success=False,
                artifacts=[],
                metadata={},
                error_message=str(e)
            )
    
    def get_capabilities(self) -> List[str]:
        """Get agent capabilities"""
        return [
            "evidence_retrieval",
            "rag_search",
            "semantic_search",
            "framework_agnostic_analysis",
            "tool_calling",
            "structured_output"
        ]
    
    def get_required_inputs(self) -> List[str]:
        """Get required input parameters"""
        return ["run_context"]
    
    def get_optional_inputs(self) -> List[str]:
        """Get optional input parameters"""
        return []
    
    def _load_framework_from_path(self, framework_path: str) -> Dict[str, Any]:
        """Load framework specification from file path."""
        try:
            framework_file = Path(framework_path)
            if not framework_file.exists():
                raise ValueError(f"Framework file not found: {framework_path}")
            
            with open(framework_file, 'r', encoding='utf-8') as f:
                if framework_path.endswith('.yaml') or framework_path.endswith('.yml'):
                    import yaml
                    return yaml.safe_load(f)
                else:
                    return json.load(f)
                    
        except Exception as e:
            self.logger.error(f"Failed to load framework from path: {e}")
            raise
    
    def _find_evidence_artifacts_from_analysis(self, analysis_artifacts: List[str]) -> List[str]:
        """Find evidence artifacts from analysis artifacts."""
        try:
            evidence_hashes = []
            
            for artifact_hash in analysis_artifacts:
                try:
                    artifact_content = self.storage.get_artifact(artifact_hash)
                    if not artifact_content:
                        continue
                    
                    artifact_data = json.loads(artifact_content.decode('utf-8'))
                    
                    # Look for evidence artifacts in the analysis results
                    if isinstance(artifact_data, dict):
                        # Check for evidence_artifacts field
                        if 'evidence_artifacts' in artifact_data:
                            evidence_hashes.extend(artifact_data['evidence_artifacts'])
                        
                        # Check for evidence_artifact_hashes field
                        if 'evidence_artifact_hashes' in artifact_data:
                            evidence_hashes.extend(artifact_data['evidence_artifact_hashes'])
                        
                        # Check for evidence_data field
                        if 'evidence_data' in artifact_data:
                            evidence_hashes.append(artifact_hash)
                            
                except Exception as e:
                    self.logger.warning(f"Failed to process analysis artifact {artifact_hash}: {e}")
                    continue
            
            self.logger.info(f"Found {len(evidence_hashes)} evidence artifacts from analysis")
            return evidence_hashes
            
        except Exception as e:
            self.logger.error(f"Failed to find evidence artifacts: {e}")
            raise
    
    def _build_evidence_wrapper(self, evidence_artifact_hashes: List[str]) -> Optional[EvidenceMatchingWrapper]:
        """Build the evidence wrapper from artifact hashes."""
        try:
            wrapper = EvidenceMatchingWrapper(
                model=self.config.model if self.config else "vertex_ai/gemini-2.5-flash",
                artifact_storage=self.storage,
                audit_logger=self.audit
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
            # Extract key findings from statistical results
            findings = self._extract_key_findings(statistical_results)
            
            if not findings:
                self.logger.warning("No key findings identified from statistical results")
                return []
            
            evidence_results = []
            
            for finding in findings:
                try:
                    # Generate evidence queries for this finding
                    queries = self._generate_evidence_queries(finding, framework_spec)
                    
                    # Retrieve evidence for each query
                    finding_evidence = []
                    for query in queries:
                        evidence = self._retrieve_evidence_for_query(query)
                        finding_evidence.extend(evidence)
                    
                    # Deduplicate and rank evidence
                    finding_evidence = self._deduplicate_and_rank_evidence(finding_evidence)
                    
                    evidence_results.append({
                        "finding": finding,
                        "queries": queries,
                        "quotes": finding_evidence
                    })
                    
                except Exception as e:
                    self.logger.warning(f"Failed to process finding: {e}")
                    continue
            
            return evidence_results
            
        except Exception as e:
            self.logger.error(f"Failed to retrieve evidence: {e}")
            raise
    
    def _extract_key_findings(self, statistical_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract key findings from statistical results."""
        try:
            findings = []
            
            # Look for common statistical result patterns
            if 'findings' in statistical_results:
                findings.extend(statistical_results['findings'])
            
            if 'key_findings' in statistical_results:
                findings.extend(statistical_results['key_findings'])
            
            if 'results' in statistical_results:
                results = statistical_results['results']
                if isinstance(results, list):
                    findings.extend(results)
                elif isinstance(results, dict):
                    for key, value in results.items():
                        if isinstance(value, dict) and 'significance' in value:
                            findings.append({
                                "dimension": key,
                                "significance": value['significance'],
                                "description": value.get('description', '')
                            })
            
            return findings
            
        except Exception as e:
            self.logger.error(f"Failed to extract key findings: {e}")
            return []
    
    def _generate_evidence_queries(self, finding: Dict[str, Any], framework_spec: Dict[str, Any]) -> List[str]:
        """Generate evidence queries for a finding."""
        try:
            # Create a prompt for query generation
            prompt = f"""
            Based on this statistical finding and framework, generate 2-3 specific evidence queries:
            
            Finding: {finding}
            Framework: {framework_spec.get('name', 'Unknown')}
            
            Generate queries that would help find evidence to support or refute this finding.
            Focus on specific, searchable terms related to the finding.
            """
            
            # Use LLM to generate queries
            response = self.llm_gateway.call_llm(
                model=self.config.model if self.config else "vertex_ai/gemini-2.5-flash",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1
            )
            
            # Parse response to extract queries
            queries = []
            lines = response.split('\n')
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#') and not line.startswith('-'):
                    # Clean up the query
                    query = re.sub(r'^\d+\.\s*', '', line)
                    if query:
                        queries.append(query)
            
            return queries[:3]  # Limit to 3 queries
            
        except Exception as e:
            self.logger.error(f"Failed to generate evidence queries: {e}")
            return [str(finding.get('description', 'statistical finding'))]
    
    def _retrieve_evidence_for_query(self, query: str) -> List[Dict[str, Any]]:
        """Retrieve evidence for a specific query."""
        try:
            if not self.evidence_wrapper:
                return []
            
            # Use the evidence wrapper to search
            results = self.evidence_wrapper.search_evidence(query, limit=5)
            
            # Format results
            evidence = []
            for result in results:
                evidence.append({
                    "quote_text": result.get('quote_text', ''),
                    "document_name": result.get('document_name', 'unknown'),
                    "relevance_score": result.get('relevance_score', 0.0),
                    "metadata": result.get('metadata', {})
                })
            
            return evidence
            
        except Exception as e:
            self.logger.error(f"Failed to retrieve evidence for query '{query}': {e}")
            return []
    
    def _deduplicate_and_rank_evidence(self, evidence: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Deduplicate and rank evidence by relevance."""
        try:
            # Remove duplicates based on quote text
            seen_quotes = set()
            unique_evidence = []
            
            for item in evidence:
                quote_text = item.get('quote_text', '')
                if quote_text and quote_text not in seen_quotes:
                    seen_quotes.add(quote_text)
                    unique_evidence.append(item)
            
            # Sort by relevance score
            unique_evidence.sort(key=lambda x: x.get('relevance_score', 0.0), reverse=True)
            
            return unique_evidence[:10]  # Limit to top 10
            
        except Exception as e:
            self.logger.error(f"Failed to deduplicate and rank evidence: {e}")
            return evidence
    
    def _store_evidence_results(self, evidence_results: List[Dict[str, Any]], framework_hash: str) -> str:
        """Store evidence results in artifact storage."""
        try:
            evidence_data = {
                "evidence_data": evidence_results,
                "framework_hash": framework_hash,
                "timestamp": datetime.now().isoformat(),
                "agent": self.agent_name,
                "total_quotes": sum(len(result['quotes']) for result in evidence_results)
            }
            
            # Store as artifact
            artifact_id = f"evidence_v2_{int(datetime.now().timestamp())}"
            self.storage.store_artifact(artifact_id, json.dumps(evidence_data, indent=2))
            
            return artifact_id
            
        except Exception as e:
            self.logger.error(f"Failed to store evidence results: {e}")
            raise
    
    def _calculate_framework_hash(self, framework_path: str) -> str:
        """Calculate hash for framework file."""
        try:
            import hashlib
            
            with open(framework_path, 'rb') as f:
                content = f.read()
                return hashlib.sha256(content).hexdigest()
                
        except Exception as e:
            self.logger.error(f"Failed to calculate framework hash: {e}")
            return "unknown"
