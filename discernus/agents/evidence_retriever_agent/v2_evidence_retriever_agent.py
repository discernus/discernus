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
from ...core.rag_index_manager import RAGIndexManager


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

        # RAG Index Manager for evidence retrieval
        self.rag_manager = RAGIndexManager(storage, audit, security)
    
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
            self.logger.info("V2EvidenceRetrieverAgent starting execution")
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
            print(f"DEBUG: _extract_key_findings returned: {key_findings}")
            print(f"DEBUG: key_findings length: {len(key_findings)}")
            print(f"DEBUG: key_findings boolean: {bool(key_findings)}")
            self.logger.info(f"Found {len(key_findings)} key findings")
            if not key_findings:
                print("DEBUG: About to return failure due to no key findings")
                error_msg = "No key statistical findings were identified by the LLM. Cannot proceed with evidence retrieval."
                self.logger.error(error_msg)
                print(f"DEBUG: Returning failure with error: {error_msg}")
                return AgentResult(
                    success=False,
                    artifacts=[],
                    metadata={"error": error_msg},
                    error_message=error_msg
                )

            # 4. For each finding, generate queries and retrieve evidence from the RAG index
            evidence_results = []
            for finding in key_findings:
                # Generate queries for this finding
                queries = self._generate_evidence_queries(finding, framework_content)
                for query in queries:
                    evidence = self._retrieve_evidence_for_query(query)
                    evidence_results.extend(evidence)

            # 5. Store the final evidence artifact
            evidence_artifact_hash = self._store_evidence_results(evidence_results, index_cache_key)

            # 6. Update RunContext and return result
            run_context.evidence = evidence_results
            run_context.add_artifact("evidence", evidence_artifact_hash, evidence_artifact_hash)

            result = AgentResult(
                success=True,
                artifacts=[evidence_artifact_hash],
                metadata={
                    "quotes_found": sum(len(e.get("quotes", [])) for e in evidence_results),
                    "findings_processed": len(evidence_results)
                }
            )
            self.log_execution_complete(result)
            return result

        except Exception as e:
            self.logger.error(f"Evidence retrieval failed: {e}", exc_info=True)
            self.log_execution_error(e)
            return AgentResult(success=False, artifacts=[], metadata={}, error_message=str(e))

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

    def _validate_and_extract_inputs(self, run_context: RunContext):
        """Validates required inputs are in the RunContext and returns them."""
        if not run_context:
            raise ValueError("run_context is required")

        framework_content = run_context.metadata.get("framework_content")
        if not framework_content:
            raise ValueError("framework_content not found in RunContext")

        statistical_results = run_context.statistical_results
        if not statistical_results:
            raise ValueError("statistical_results not found in RunContext")

        corpus_documents = run_context.metadata.get("corpus_documents")
        if not corpus_documents:
            raise ValueError("corpus_documents not found in RunContext")
            
        return framework_content, statistical_results, corpus_documents

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
            
            # Debug logging
            print(f"DEBUG: Statistical results keys: {list(statistical_results.keys())}")
            print(f"DEBUG: Statistical results type: {type(statistical_results)}")
            
            # Add detailed debug logging to understand the structure
            import json
            try:
                print(f"DEBUG: Full statistical results: {json.dumps(statistical_results, indent=2, default=str)}")
            except Exception as e:
                print(f"DEBUG: Could not serialize statistical results: {e}")
                print(f"DEBUG: Statistical results repr: {repr(statistical_results)}")
            
            # Look for statistical analysis results in the V2 format
            if 'statistical_functions_and_results' in statistical_results:
                # The statistical results are stored as a JSON string in the statistical_functions_and_results field
                import json
                try:
                    # Extract JSON from the markdown code block
                    json_str = statistical_results['statistical_functions_and_results']
                    if '```json' in json_str:
                        # Find the start and end of the JSON block
                        start_idx = json_str.find('```json') + 7
                        end_idx = json_str.rfind('```')
                        if end_idx > start_idx:
                            json_str = json_str[start_idx:end_idx].strip()
                    analysis = json.loads(json_str)
                    if 'execution_results' in analysis:
                        results = analysis['execution_results']
                    else:
                        results = {}
                except (json.JSONDecodeError, KeyError, IndexError) as e:
                    self.logger.error(f"Failed to parse statistical_functions_and_results: {e}")
                    results = {}
            elif 'statistical_analysis' in statistical_results:
                analysis = statistical_results['statistical_analysis']
                if 'execution_results' in analysis:
                    results = analysis['execution_results']
                else:
                    results = {}
            else:
                results = {}
            
            # Debug: Log the parsed results structure
            print(f"DEBUG: Parsed results keys: {list(results.keys()) if results else 'No results'}")
            if 'group_comparisons' in results:
                print(f"DEBUG: Group comparisons structure: {json.dumps(results['group_comparisons'], indent=2, default=str)}")
            
            print(f"DEBUG: About to check for findings. Current findings count: {len(findings)}")
            
            # Extract findings from group comparison
            if 'group_comparisons' in results and results['group_comparisons']:
                # New format: group_comparisons is a dict of comparisons
                group_comps = results['group_comparisons']
                for comparison_name, comparison_data in group_comps.items():
                    if isinstance(comparison_data, dict) and 'mean_difference' in comparison_data:
                        mean_diff = comparison_data['mean_difference']
                        # Handle both old format (dict with 'value') and new format (direct numeric value)
                        if isinstance(mean_diff, dict) and 'value' in mean_diff:
                            diff_value = mean_diff['value']
                        elif isinstance(mean_diff, (int, float)):
                            diff_value = mean_diff
                        else:
                            continue  # Skip if format is unrecognized
                        
                        findings.append({
                            "dimension": comparison_data.get('dependent_variable', comparison_name),
                            "type": "group_comparison",
                            "description": f"Group comparison shows {comparison_data.get('dependent_variable', comparison_name)} difference: {diff_value:.3f}",
                            "raw_data": comparison_data
                        })
            elif 'group_comparison' in results and results['group_comparison']:
                print(f"DEBUG: Found group_comparison (singular)")
                group_comp = results['group_comparison']
                print(f"DEBUG: Group comparison keys: {list(group_comp.keys())}")
                # Check for mean_differences (plural) first, then mean_difference (singular)
                if 'mean_differences' in group_comp:
                    print(f"DEBUG: Using mean_differences (plural) path")
                    for dimension, difference in group_comp['mean_differences'].items():
                        findings.append({
                            "dimension": dimension,
                            "type": "group_comparison",
                            "description": f"Group comparison shows {dimension} difference: {difference:.3f}",
                            "raw_data": {"mean_difference": difference}
                        })
                else:
                    print(f"DEBUG: Using fallback path for individual dimensions")
                    # Fallback to old format
                    for dimension, stats in group_comp.items():
                        print(f"DEBUG: Processing dimension {dimension} with stats type {type(stats)}")
                        if isinstance(stats, dict) and 'mean_difference' in stats:
                            print(f"DEBUG: Found mean_difference in {dimension}: {stats['mean_difference']}")
                            findings.append({
                                "dimension": dimension,
                                "type": "group_comparison",
                                "description": f"Group comparison shows {dimension} difference: {stats['mean_difference']:.3f}",
                                "raw_data": stats
                            })
            elif 'additional_analyses' in results and results['additional_analyses']:
                additional = results['additional_analyses']
                if 'group_differences' in additional and additional['group_differences']:
                    group_comp = additional['group_differences']
                    for dimension, stats in group_comp.items():
                        if isinstance(stats, dict) and 'mean_difference' in stats:
                            findings.append({
                                "dimension": dimension,
                                "type": "group_comparison",
                                "description": f"Group comparison shows {dimension} difference: {stats['mean_difference']:.3f}",
                                "raw_data": stats
                            })
                elif 'group_comparison' in additional and additional['group_comparison']:
                    group_comp = additional['group_comparison']
                    for dimension, stats in group_comp.items():
                        if isinstance(stats, dict) and 'mean_difference' in stats:
                            findings.append({
                                "dimension": dimension,
                                "type": "group_comparison",
                                "description": f"Group comparison shows {dimension} difference: {stats['mean_difference']:.3f}",
                                "raw_data": stats
                            })
            
            # Extract findings from descriptive statistics
            if 'descriptive_statistics' in results and results['descriptive_statistics']:
                desc_stats = results['descriptive_statistics']
                # Check for overall_statistics (plural) first, then overall (singular)
                if 'overall_statistics' in desc_stats:
                    overall = desc_stats['overall_statistics']
                    for dimension, stats in overall.items():
                        if isinstance(stats, dict) and 'mean' in stats:
                            findings.append({
                                "dimension": dimension,
                                "type": "descriptive",
                                "description": f"Overall {dimension} mean: {stats['mean']:.3f}",
                                "raw_data": stats
                            })
                elif 'overall' in desc_stats:
                    overall = desc_stats['overall']
                    for dimension, stats in overall.items():
                        if isinstance(stats, dict) and 'mean' in stats:
                            findings.append({
                                "dimension": dimension,
                                "type": "descriptive",
                                "description": f"Overall {dimension} mean: {stats['mean']:.3f}",
                                "raw_data": stats
                            })
            
            # Extract findings from correlation analysis
            if 'correlation_analysis' in results and results['correlation_analysis']:
                corr_analysis = results['correlation_analysis']
                if 'correlation_coefficient' in corr_analysis:
                    findings.append({
                        "dimension": "correlation",
                        "type": "correlation_analysis",
                        "description": f"Correlation coefficient: {corr_analysis['correlation_coefficient']:.3f}",
                        "raw_data": corr_analysis
                    })
                elif 'correlation_matrix' in corr_analysis and corr_analysis['correlation_matrix']:
                    findings.append({
                        "dimension": "correlation",
                        "type": "correlation_analysis",
                        "description": f"Correlation analysis completed",
                        "raw_data": corr_analysis['correlation_matrix']
                    })
            
            # Fallback: Look for common statistical result patterns
            if not findings:
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
            
            self.logger.info(f"Extracted {len(findings)} key findings from statistical results")
            return findings
            
        except Exception as e:
            self.logger.error(f"Failed to extract key findings: {e}")
            return []
    
    def _generate_evidence_queries(self, finding: Dict[str, Any], framework_content: str) -> List[str]:
        """Generate evidence queries for a finding."""
        try:
            # Debug logging to understand the data types
            self.logger.debug(f"Finding type: {type(finding)}, Framework content type: {type(framework_content)}")
            
            # Ensure finding is serializable
            try:
                finding_json = json.dumps(finding, indent=2)
            except (TypeError, ValueError) as e:
                self.logger.warning(f"Finding not JSON serializable: {e}. Using string representation.")
                finding_json = str(finding)
            
            # Create a prompt for query generation
            prompt = f"""
            Based on this statistical finding and framework, generate 2-3 specific evidence queries:
            
            Finding: {finding_json}
            Framework Description: {framework_content[:1000]}
            
            Generate queries that would help find textual evidence in a corpus to support or refute this finding.
            Focus on specific, searchable terms, phrases, or concepts related to the finding.
            Return a JSON list of strings. Example: ["query 1", "query 2"]
            """
            
            # Use LLM to generate queries
            response = self.llm_gateway.execute_call(
                model=self.config.model if self.config else "vertex_ai/gemini-2.5-flash",
                prompt=prompt,
                temperature=0.1
            )

            # Handle tuple response from LLM gateway
            if isinstance(response, tuple):
                content, metadata = response
            else:
                content = response.get('content', '') if isinstance(response, dict) else str(response)

            # Debug logging for response handling
            self.logger.debug(f"Response type: {type(response)}, Content type: {type(content)}")
            
            # Ensure content is a string
            if not isinstance(content, str):
                self.logger.warning(f"Content is not a string: {type(content)}. Converting to string.")
                content = str(content)

            # Parse response to extract queries
            try:
                # Find the JSON list in the response
                json_match = re.search(r'\[.*\]', content, re.DOTALL)
                if json_match:
                    queries = json.loads(json_match.group())
                    return queries[:3]
            except json.JSONDecodeError:
                self.logger.warning(f"Could not decode JSON from LLM response for query generation: {content}")

            # Fallback for non-JSON responses
            queries = []
            lines = content.split('\n')
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#') and not line.startswith('-'):
                    # Clean up the query
                    query = re.sub(r'^\d+\.\s*', '', line)
                    if query:
                        queries.append(query)
            
            return queries[:3]  # Limit to 3 queries
            
        except Exception as e:
            self.logger.error(f"Failed to generate evidence queries: {e}", exc_info=True)
            # Provide a safe fallback
            if isinstance(finding, dict):
                return [str(finding.get('description', 'statistical finding'))]
            else:
                return [str(finding)]
    
    def _retrieve_evidence_for_query(self, query: str) -> List[Dict[str, Any]]:
        """Retrieve evidence for a specific query."""
        try:
            if not self.rag_manager: # Changed from evidence_wrapper to rag_manager
                return []
            
            # Use the evidence wrapper to search
            results = self.rag_manager.search(query, top_k=5) # Changed from evidence_wrapper to rag_manager
            
            # Format results
            evidence = []
            for result in results:
                evidence.append({
                    "text": result.get('text', ''), # Changed from quote_text to text
                    "document_name": result.get('document_name', 'unknown'),
                    "score": result.get('score', 0.0), # Changed from relevance_score to score
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
                quote_text = item.get('text', '') # Changed from quote_text to text
                if quote_text and quote_text not in seen_quotes:
                    seen_quotes.add(quote_text)
                    unique_evidence.append(item)
            
            # Sort by relevance score
            unique_evidence.sort(key=lambda x: x.get('score', 0.0), reverse=True) # Changed from relevance_score to score
            
            return unique_evidence[:10]  # Limit to top 10
            
        except Exception as e:
            self.logger.error(f"Failed to deduplicate and rank evidence: {e}")
            return evidence
    
    def _store_evidence_results(self, evidence_results: List[Dict[str, Any]], cache_key: str) -> str:
        """Store evidence results in artifact storage."""
        try:
            evidence_data = {
                "evidence_data": evidence_results,
                "rag_cache_key": cache_key,
                "timestamp": datetime.now().isoformat(),
                "agent": self.agent_name,
                "total_quotes": sum(len(e.get("quotes", [])) for e in evidence_results)
            }
            
            # Store as artifact
            artifact_id = f"evidence_v2_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            artifact_hash = self.storage.put_artifact(
                json.dumps(evidence_data, indent=2).encode('utf-8'),
                {"artifact_type": "evidence_retrieval", "artifact_id": artifact_id}
            )
            
            return artifact_hash
            
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
