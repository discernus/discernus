#!/usr/bin/env python3
"""
Fact Checker Agent

This agent verifies all factual claims in the draft synthesis report against:
1. Original source documents (via corpus index service)
2. Stored analysis results and derived metrics
3. Evidence database

The agent focuses on data integrity and accurate reporting, not mathematical correctness.
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path

from discernus.gateway.llm_gateway import LLMGateway


class FactCheckerAgent:
    """
    Fact Checker Agent for validating factual claims in synthesis reports.
    
    This agent uses LLM intelligence to:
    1. Identify factual claims that need verification
    2. Validate claims against available resources
    3. Classify issues by type and severity
    4. Generate actionable findings for the revision agent
    """
    
    def __init__(self, gateway=None, audit_logger=None, corpus_index_service=None, 
                 model: str = "vertex_ai/gemini-2.5-pro", artifact_storage=None, working_dir=None):
        """Initialize the Fact Checker Agent."""
        self.model = model
        if gateway:
            self.client = gateway
        else:
            from ...gateway.model_registry import ModelRegistry
            model_registry = ModelRegistry()
            self.client = LLMGateway(model_registry)
        self.audit_logger = audit_logger
        self.corpus_index_service = corpus_index_service
        self.working_dir = working_dir or Path.cwd()
        self.logger = logging.getLogger(__name__)
        
        # Initialize artifact storage
        if artifact_storage:
            self.artifact_storage = artifact_storage
        else:
            # Create a basic artifact storage for this project
            try:
                from ...core.local_artifact_storage import LocalArtifactStorage
                from ...core.security_boundary import ExperimentSecurityBoundary
                
                # Create security boundary for this project
                security_boundary = ExperimentSecurityBoundary(self.working_dir)
                
                # Use shared_cache directory if it exists, otherwise create it
                shared_cache_dir = self.working_dir / "shared_cache"
                if not shared_cache_dir.exists():
                    shared_cache_dir.mkdir(parents=True, exist_ok=True)
                
                # Check if there's an existing artifact registry
                existing_registry = shared_cache_dir / "artifacts" / "artifact_registry.json"
                if existing_registry.exists():
                    # Load the existing registry
                    with open(existing_registry, 'r') as f:
                        existing_registry_data = json.load(f)
                    
                    # Create artifact storage and manually load the existing registry
                    self.artifact_storage = LocalArtifactStorage(
                        security_boundary=security_boundary,
                        run_folder=shared_cache_dir,
                        run_name="fact_checker"
                    )
                    
                    # Manually set the registry to the existing one
                    self.artifact_storage.registry = existing_registry_data
                    self.logger.info(f"Loaded existing artifact registry with {len(existing_registry_data)} artifacts")
                else:
                    # Create new artifact storage
                    self.artifact_storage = LocalArtifactStorage(
                        security_boundary=security_boundary,
                        run_folder=shared_cache_dir,
                        run_name="fact_checker"
                    )
                    self.logger.info(f"Created new artifact storage for: {shared_cache_dir}")
                    
            except Exception as e:
                self.logger.warning(f"Could not initialize artifact storage: {e}")
                self.artifact_storage = None
    
    def run(self) -> Dict[str, Any]:
        """
        Run fact-checking with self-directed data discovery.
        
        This method makes the agent completely autonomous - it discovers and loads
        all the data it needs without external input.
        
        Returns:
            Dictionary containing fact-checking results with status, findings, and summary.
        """
        try:
            self.logger.info("Starting self-directed fact-checking process")
            
            # 1. Discover synthesis report to validate
            synthesis_report = self._discover_synthesis_report()
            if not synthesis_report:
                return {
                    "status": "failed",
                    "error": "No synthesis report found for validation",
                    "findings": [],
                    "summary": "Fact checking failed: no synthesis report available"
                }
            
            # 2. Discover available evidence artifacts
            evidence_data = self._discover_evidence_data()
            
            # 3. Discover framework specification
            framework_spec = self._discover_framework_spec()
            
            # 4. Discover corpus index service with search wrappers
            corpus_index, search_wrappers = self._discover_semantic_index_with_wrapper([
                "corpus_search", "quote_validation", "semantic_search"
            ])
            
            # 5. Discover analysis data for validation
            raw_analysis_data = self._discover_raw_analysis_data()
            derived_metrics_data = self._discover_derived_metrics_data()
            statistical_results_data = self._discover_statistical_results_data()
            
            # 6. Perform fact checking using discovered resources
            fact_check_results = self._run_fact_checking(
                synthesis_report, evidence_data, framework_spec, corpus_index, 
                search_wrappers, raw_analysis_data, derived_metrics_data, statistical_results_data
            )
            
            return fact_check_results
            
        except Exception as e:
            self.logger.error(f"Fact checking failed: {e}")
            return {
                "status": "failed",
                "error": str(e),
                "findings": [],
                "summary": f"Fact checking failed: {e}"
            }
    
    def _discover_synthesis_report(self) -> Optional[Dict[str, Any]]:
        """
        Discover the synthesis report to validate.
        
        Returns:
            Synthesis report content or None if not found
        """
        try:
            # First try to find from artifact storage
            if hasattr(self, 'artifact_storage') and self.artifact_storage:
                # Look for synthesis report artifacts (could be various types)
                synthesis_artifacts = self._discover_artifacts_by_type("synthesis_report")
                if not synthesis_artifacts:
                    # Try alternative artifact types
                    synthesis_artifacts = self._discover_artifacts_by_type("final_report")
                if not synthesis_artifacts:
                    synthesis_artifacts = self._discover_artifacts_by_type("draft_synthesis_report")
                
                if synthesis_artifacts:
                    latest_artifact = synthesis_artifacts[0]  # Could enhance to find most recent
                    return self._load_artifact_content(latest_artifact["hash"])
            
            # Fallback: try to find from common file patterns
            # This would look for files with names like "synthesis_report", "final_report", etc.
            return None
            
        except Exception as e:
            self.logger.warning(f"Failed to discover synthesis report: {e}")
            return None
    
    def _discover_evidence_data(self) -> Optional[Dict[str, Any]]:
        """
        Discover evidence data for fact checking.
        
        Returns:
            Evidence data or None if not found
        """
        try:
            # First try to find from artifact storage
            if hasattr(self, 'artifact_storage') and self.artifact_storage:
                # Look for evidence collection artifacts
                evidence_artifacts = self._discover_artifacts_by_type("evidence_collection")
                if not evidence_artifacts:
                    # Try alternative artifact types
                    evidence_artifacts = self._discover_artifacts_by_type("evidence_retrieval_results")
                if not evidence_artifacts:
                    evidence_artifacts = self._discover_artifacts_by_type("curated_evidence")
                
                if evidence_artifacts:
                    latest_artifact = evidence_artifacts[0]
                    return self._load_artifact_content(latest_artifact["hash"])
            
            # Fallback: try to find from common file patterns
            return None
            
        except Exception as e:
            self.logger.warning(f"Failed to discover evidence data: {e}")
            return None
    
    def _discover_framework_spec(self) -> Optional[Dict[str, Any]]:
        """
        Discover framework specification for context.
        
        Returns:
            Framework specification or None if not found
        """
        try:
            # First try to find from artifact storage
            if hasattr(self, 'artifact_storage') and self.artifact_storage:
                # Look for framework specification artifacts
                framework_artifacts = self._discover_artifacts_by_type("framework_specification")
                if not framework_artifacts:
                    # Try alternative artifact types
                    framework_artifacts = self._discover_artifacts_by_type("framework_spec")
                if not framework_artifacts:
                    framework_artifacts = self._discover_artifacts_by_type("framework_definition")
                
                if framework_artifacts:
                    latest_artifact = framework_artifacts[0]
                    return self._load_artifact_content(latest_artifact["hash"])
            
            # Fallback: try to find from common file patterns
            return None
            
        except Exception as e:
            self.logger.warning(f"Failed to discover framework specification: {e}")
            return None
    
    def _discover_raw_analysis_data(self) -> Optional[Dict[str, Any]]:
        """
        Discover raw analysis data for validation.
        
        Returns:
            Raw analysis data or None if not found
        """
        try:
            # Look for artifacts with type raw_analysis_response_v6
            if hasattr(self, 'artifact_storage') and self.artifact_storage:
                raw_analysis_artifacts = self._discover_artifacts_by_type("raw_analysis_response_v6")
                
                if raw_analysis_artifacts:
                    latest_artifact = raw_analysis_artifacts[0]
                    return self._load_artifact_content(latest_artifact["hash"])
            
            return None
            
        except Exception as e:
            self.logger.warning(f"Failed to discover raw analysis data: {e}")
            return None
    
    def _discover_derived_metrics_data(self) -> Optional[Dict[str, Any]]:
        """
        Discover derived metrics data for validation.
        
        Returns:
            Derived metrics data or None if not found
        """
        try:
            # Look for artifacts with type derived_metrics_results_with_data
            if hasattr(self, 'artifact_storage') and self.artifact_storage:
                derived_metrics_artifacts = self._discover_artifacts_by_type("derived_metrics_results_with_data")
                
                if derived_metrics_artifacts:
                    latest_artifact = derived_metrics_artifacts[0]
                    return self._load_artifact_content(latest_artifact["hash"])
            
            return None
            
        except Exception as e:
            self.logger.warning(f"Failed to discover derived metrics data: {e}")
            return None
    
    def _discover_statistical_results_data(self) -> Optional[Dict[str, Any]]:
        """
        Discover statistical results data for validation.
        
        Returns:
            Statistical results data or None if not found
        """
        try:
            # Look for artifacts with type statistical_results_with_data
            if hasattr(self, 'artifact_storage') and self.artifact_storage:
                statistical_artifacts = self._discover_artifacts_by_type("statistical_results_with_data")
                
                if statistical_artifacts:
                    latest_artifact = statistical_artifacts[0]
                    return self._load_artifact_content(latest_artifact["hash"])
            
            return None
            
        except Exception as e:
            self.logger.warning(f"Failed to discover statistical results data: {e}")
            return None
    
    def _discover_semantic_index_with_wrapper(self, required_properties: List[str]) -> tuple:
        """
        Discover a semantic index and its search wrapper methods.
        
        Args:
            required_properties: List of properties the index must have
            
        Returns:
            Tuple of (index, wrapper_methods)
        """
        # First try to use the corpus index service if it's available
        if hasattr(self, 'corpus_index_service') and self.corpus_index_service:
            # Check if it has the required properties
            if self._index_has_properties(self.corpus_index_service, required_properties):
                # Get wrapper methods from the service
                wrapper_methods = getattr(
                    self.corpus_index_service, 
                    'get_search_wrapper_methods', 
                    self._get_default_corpus_wrappers
                )()
                return self.corpus_index_service, wrapper_methods
        
        # Fallback: try to discover from artifact storage
        if hasattr(self, 'artifact_storage') and self.artifact_storage:
            corpus_artifacts = self._discover_artifacts_by_type("corpus_index")
            if corpus_artifacts:
                # Use the first available corpus index
                latest_artifact = corpus_artifacts[0]  # Could be enhanced to find most recent
                index = self.artifact_storage.get_artifact(latest_artifact["hash"])
                
                if self._index_has_properties(index, required_properties):
                    wrapper_methods = getattr(
                        index, 
                        'get_search_wrapper_methods', 
                        self._get_default_corpus_wrappers
                    )()
                    return index, wrapper_methods
        
        # Final fallback: return default wrappers
        return None, self._get_default_corpus_wrappers()
    
    def _discover_artifacts_by_type(self, artifact_type: str) -> List[Dict[str, Any]]:
        """
        Discover artifacts by type from artifact storage.
        
        Args:
            artifact_type: Type of artifact to discover
            
        Returns:
            List of artifact metadata dictionaries
        """
        if not hasattr(self, 'artifact_storage') or not self.artifact_storage:
            return []
        
        try:
            all_artifacts = self.artifact_storage.list_artifacts()
            # Filter by artifact type and normalize field names for compatibility
            filtered_artifacts = []
            for art in all_artifacts:
                if art.get("metadata", {}).get("artifact_type") == artifact_type:
                    # Normalize to expected format with both 'hash' and 'hash_id' fields
                    normalized_artifact = art.copy()
                    normalized_artifact["hash"] = art.get("hash_id")  # Add 'hash' field for compatibility
                    filtered_artifacts.append(normalized_artifact)
            return filtered_artifacts
        except Exception as e:
            self.logger.warning(f"Failed to discover artifacts of type {artifact_type}: {e}")
            return []
    
    def _index_has_properties(self, index: Any, required_properties: List[str]) -> bool:
        """
        Check if an index has the required properties.
        
        Args:
            index: The index to check
            required_properties: List of properties the index must have
            
        Returns:
            True if index has all required properties, False otherwise
        """
        if not index:
            return False
        
        try:
            # Try to get capabilities from the index
            capabilities = getattr(index, 'get_capabilities', lambda: [])()
            
            # Check if all required properties are in capabilities
            return all(prop in capabilities for prop in required_properties)
        except Exception as e:
            self.logger.warning(f"Failed to check index properties: {e}")
            return False
    
    def _load_artifact_content(self, artifact_hash: str) -> Optional[Dict[str, Any]]:
        """
        Load content from an artifact by hash.
        
        Args:
            artifact_hash: Hash of the artifact to load
            
        Returns:
            Artifact content or None if loading failed
        """
        try:
            if hasattr(self, 'artifact_storage') and self.artifact_storage:
                artifact = self.artifact_storage.get_artifact(artifact_hash)
                if artifact:
                    # Handle bytes content (most common case)
                    if isinstance(artifact, bytes):
                        try:
                            # Try to decode as UTF-8 text
                            content = artifact.decode('utf-8')
                            return {
                                "content": content,
                                "content_type": "text",
                                "size_bytes": len(artifact)
                            }
                        except UnicodeDecodeError:
                            # If it's not text, return as binary
                            return {
                                "content": artifact,
                                "content_type": "binary",
                                "size_bytes": len(artifact)
                            }
                    # Handle string content
                    elif isinstance(artifact, str):
                        return {
                            "content": artifact,
                            "content_type": "text",
                            "size_bytes": len(artifact.encode('utf-8'))
                        }
                    # Handle other types
                    else:
                        return {
                            "content": str(artifact),
                            "content_type": "other",
                            "size_bytes": len(str(artifact).encode('utf-8'))
                        }
            return None
        except Exception as e:
            self.logger.warning(f"Failed to load artifact {artifact_hash}: {e}")
            return None
    
    def _get_default_corpus_wrappers(self) -> Dict[str, Any]:
        """
        Provide default corpus search wrapper methods.
        
        Returns:
            Dictionary of default search wrapper methods
        """
        return {
            "validate_quote": self._default_validate_quote,
            "search_documents": self._default_search_documents,
            "get_context": self._default_get_context
        }
    
    def _default_validate_quote(self, quote: str, document_name: str) -> Dict[str, Any]:
        """Default quote validation method."""
        return {
            "status": "not_implemented",
            "message": "Default quote validation not implemented"
        }
    
    def _default_search_documents(self, query: str) -> List[Dict[str, Any]]:
        """Default document search method."""
        return []
    
    def _default_get_context(self, document_name: str, quote: str) -> Dict[str, Any]:
        """Default context retrieval method."""
        return {
            "status": "not_implemented",
            "message": "Default context retrieval not implemented"
        }
    
    def _run_fact_checking(self, synthesis_report: Dict[str, Any], 
                          evidence_data: Optional[Dict[str, Any]], 
                          framework_spec: Optional[Dict[str, Any]], 
                          corpus_index: Any, 
                          search_wrappers: Dict[str, Any],
                          raw_analysis_data: Optional[Dict[str, Any]],
                          derived_metrics_data: Optional[Dict[str, Any]],
                          statistical_results_data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Run the actual fact checking using discovered resources and LLM.
        
        Args:
            synthesis_report: The synthesis report to validate
            evidence_data: Available evidence data
            framework_spec: Framework specification for context
            corpus_index: Corpus index service for validation
            search_wrappers: Search wrapper methods
            raw_analysis_data: Raw analysis results for validation
            derived_metrics_data: Derived metrics for validation
            statistical_results_data: Statistical results for validation
            
        Returns:
            Fact checking results with findings and summary
        """
        try:
            self.logger.info("Running fact checking with discovered resources using LLM")
            
            # Log resource access events
            self._log_resource_access("synthesis_report", synthesis_report)
            self._log_resource_access("evidence_data", evidence_data)
            self._log_resource_access("framework_spec", framework_spec)
            self._log_resource_access("corpus_index", corpus_index)
            self._log_resource_access("search_wrappers", search_wrappers)
            self._log_resource_access("raw_analysis_data", raw_analysis_data)
            self._log_resource_access("derived_metrics_data", derived_metrics_data)
            self._log_resource_access("statistical_results_data", statistical_results_data)
            
            # Load the prompt template
            prompt_content = self._load_prompt_template()
            if not prompt_content:
                return {
                    "status": "failed",
                    "error": "Failed to load prompt template",
                    "findings": [],
                    "summary": {"total_issues": 0, "critical": 0, "errors": 0, "warnings": 0, "verified_claims": 0}
                }
            
            # Prepare the context for the LLM
            context = self._prepare_fact_checking_context(
                synthesis_report, evidence_data, framework_spec, corpus_index, 
                search_wrappers, raw_analysis_data, derived_metrics_data, statistical_results_data
            )
            
            # Execute fact checking using LLM
            llm_response = self._execute_llm_fact_checking(prompt_content, context)
            
            # Parse the LLM response
            parsed_results = self._parse_llm_fact_checking_response(llm_response)
            
            # Add resource usage information
            parsed_results["resources_used"] = {
                "synthesis_report": bool(synthesis_report),
                "evidence_data": bool(evidence_data),
                "framework_spec": bool(framework_spec),
                "corpus_index": bool(corpus_index),
                "search_wrappers": list(search_wrappers.keys()) if search_wrappers else [],
                "raw_analysis_data": bool(raw_analysis_data),
                "derived_metrics_data": bool(derived_metrics_data),
                "statistical_results_data": bool(statistical_results_data)
            }
            
            return parsed_results
            
        except Exception as e:
            self.logger.error(f"Fact checking execution failed: {e}")
            return {
                "status": "failed",
                "error": str(e),
                "findings": [],
                "summary": {"total_issues": 0, "critical": 0, "errors": 0, "warnings": 0, "verified_claims": 0}
            }
    
    def _load_prompt_template(self) -> Optional[str]:
        """Load the prompt template from the YAML file."""
        try:
            import yaml
            from pathlib import Path
            
            # Get the path to the prompt.yaml file
            current_file = Path(__file__)
            prompt_file = current_file.parent / "prompt.yaml"
            
            if not prompt_file.exists():
                self.logger.error(f"Prompt file not found: {prompt_file}")
                return None
            
            with open(prompt_file, 'r', encoding='utf-8') as f:
                prompt_data = yaml.safe_load(f)
            
            return prompt_data.get('prompt', '')
            
        except Exception as e:
            self.logger.error(f"Failed to load prompt template: {e}")
            return None
    
    def _prepare_fact_checking_context(self, synthesis_report: Dict[str, Any],
                                     evidence_data: Optional[Dict[str, Any]],
                                     framework_spec: Optional[Dict[str, Any]],
                                     corpus_index: Any,
                                     search_wrappers: Dict[str, Any],
                                     raw_analysis_data: Optional[Dict[str, Any]],
                                     derived_metrics_data: Optional[Dict[str, Any]],
                                     statistical_results_data: Optional[Dict[str, Any]]) -> str:
        """Prepare the context information for the LLM with intelligent truncation to prevent token overflow."""
        
        context_parts = []
        
        # Add synthesis report content
        if synthesis_report:
            context_parts.append("## SYNTHESIS REPORT TO VALIDATE")
            if isinstance(synthesis_report, dict) and "content" in synthesis_report:
                context_parts.append(synthesis_report["content"])
            else:
                context_parts.append(str(synthesis_report))
        
        # Add evidence data summary
        if evidence_data:
            context_parts.append("## AVAILABLE EVIDENCE DATA")
            context_parts.append(str(evidence_data))
        
        # Add framework specification
        if framework_spec:
            context_parts.append("## FRAMEWORK SPECIFICATION")
            context_parts.append(str(framework_spec))
        
        # Add raw analysis data (truncated if too large)
        if raw_analysis_data:
            context_parts.append("## RAW ANALYSIS DATA")
            raw_content = str(raw_analysis_data)
            if len(raw_content) > 10000:  # Truncate if > 10KB
                context_parts.append(raw_content[:10000] + "\n[... truncated for token limit ...]")
                self.logger.info(f"Raw analysis data truncated from {len(raw_content)} to 10000 characters")
            else:
                context_parts.append(raw_content)
        
        # Add derived metrics data (intelligently summarized)
        if derived_metrics_data:
            context_parts.append("## DERIVED METRICS DATA (SUMMARY)")
            metrics_summary = self._summarize_metrics_data(derived_metrics_data)
            context_parts.append(metrics_summary)
        
        # Add statistical results data (intelligently summarized)
        if statistical_results_data:
            context_parts.append("## STATISTICAL RESULTS DATA (SUMMARY)")
            stats_summary = self._summarize_statistical_data(statistical_results_data)
            context_parts.append(stats_summary)
        
        # Add corpus index capabilities
        if corpus_index:
            context_parts.append("## CORPUS INDEX CAPABILITIES")
            context_parts.append(f"Index type: {type(corpus_index).__name__}")
            if search_wrappers:
                context_parts.append(f"Available search wrappers: {list(search_wrappers.keys())}")
        
        # Add discovery method information
        context_parts.append("## DISCOVERY METHODS AVAILABLE")
        context_parts.append("""
        You have access to these discovery methods:
        - _discover_synthesis_report() - Returns synthesis report content
        - _discover_evidence_data() - Returns evidence data
        - _discover_framework_spec() - Returns framework specification
        - _discover_semantic_index_with_wrapper() - Returns corpus index and search wrappers
        - _discover_raw_analysis_data() - Returns raw analysis data (raw_analysis_response_v6)
        - _discover_derived_metrics_data() - Returns derived metrics (derived_metrics_results_with_data)
        - _discover_statistical_results_data() - Returns statistical results (statistical_results_with_data)
        
        Use these methods to access the data you need for validation.
        """)
        
        return "\n\n".join(context_parts)
    
    def _summarize_metrics_data(self, metrics_data: Dict[str, Any]) -> str:
        """Summarize derived metrics data for fact checking, extracting key statistics."""
        try:
            import json
            
            # Extract content and parse if needed
            content = metrics_data.get('content', '{}')
            if isinstance(content, str):
                try:
                    parsed_metrics = json.loads(content)
                except json.JSONDecodeError:
                    return f"Derived metrics data available ({len(content)} characters) - parsing failed"
            else:
                parsed_metrics = content
            
            # Extract key summary statistics for fact checking
            summary_parts = []
            
            # Look for dimension scores and statistics
            if 'dimension_scores' in parsed_metrics:
                scores = parsed_metrics['dimension_scores']
                summary_parts.append(f"Dimension scores available for {len(scores)} dimensions")
                
                # Extract key statistics for each dimension
                for dim_name, dim_data in scores.items():
                    if isinstance(dim_data, dict):
                        mean_score = dim_data.get('mean_score', 'N/A')
                        std_dev = dim_data.get('std_dev', 'N/A')
                        summary_parts.append(f"  {dim_name}: mean={mean_score}, std_dev={std_dev}")
            
            # Look for correlation data
            if 'correlations' in parsed_metrics:
                correlations = parsed_metrics['correlations']
                summary_parts.append(f"Correlation data available: {len(correlations)} correlations")
            
            # Look for aggregate statistics
            if 'aggregate_stats' in parsed_metrics:
                stats = parsed_metrics['aggregate_stats']
                summary_parts.append(f"Aggregate statistics: {list(stats.keys())}")
            
            return "\n".join(summary_parts) if summary_parts else "Derived metrics data available (summary extraction failed)"
            
        except Exception as e:
            self.logger.warning(f"Failed to summarize metrics data: {e}")
            return f"Derived metrics data available ({len(str(metrics_data))} characters) - summarization failed"
    
    def _summarize_statistical_data(self, stats_data: Dict[str, Any]) -> str:
        """Summarize statistical results data for fact checking, extracting only key numbers for validation."""
        try:
            import json
            
            # Extract content and parse if needed
            content = stats_data.get('content', '{}')
            if isinstance(content, str):
                try:
                    parsed_stats = json.loads(content)
                except json.JSONDecodeError:
                    return "Statistical data available but unparseable"
            else:
                parsed_stats = content
            
            # Extract ONLY the key statistical values needed for fact checking
            key_stats = []
            
            # Look for individual results - extract only the main metrics
            if 'individual_results' in parsed_stats:
                results = parsed_stats['individual_results']
                key_stats.append(f"Individual results: {len(results)} subjects")
                
                # Extract only the primary cohesion metrics (limit to prevent overflow)
                count = 0
                for subject_name, subject_data in results.items():
                    if count >= 10:  # Limit to first 10 subjects
                        key_stats.append("  ... (additional subjects truncated)")
                        break
                    if isinstance(subject_data, dict):
                        if 'full_cohesion_index' in subject_data:
                            cohesion = subject_data['full_cohesion_index']
                            # Round to 3 decimal places to reduce token usage
                            key_stats.append(f"  {subject_name}: {round(cohesion, 3)}")
                            count += 1
            
            # Look for summary statistics - extract only key values
            if 'summary_statistics' in parsed_stats:
                summary_stats = parsed_stats['summary_statistics']
                key_stats.append("Summary stats:")
                
                # Extract only the most important summary values
                important_keys = ['mean', 'std', 'min', 'max', 'count', 'correlation']
                for key in important_keys:
                    if key in summary_stats:
                        value = summary_stats[key]
                        if isinstance(value, (int, float)):
                            key_stats.append(f"  {key}: {round(value, 3)}")
            
            # Limit total output to prevent token overflow
            result = "\n".join(key_stats[:20])  # Limit to 20 lines max
            if len(key_stats) > 20:
                result += "\n... (additional statistics truncated for token limit)"
            
            return result if key_stats else "Statistical data available (no key metrics found)"
            
        except Exception as e:
            self.logger.warning(f"Failed to summarize statistical data: {e}")
            return "Statistical data available (summarization failed)"
    
    def _execute_llm_fact_checking(self, prompt_content: str, context: str) -> str:
        """Execute fact checking using the LLM."""
        try:
            # Combine prompt and context
            full_prompt = f"{prompt_content}\n\n{context}"
            
            # Call the LLM using the correct gateway interface
            response, metadata = self.client.execute_call(
                model=self.model,
                prompt=full_prompt,
                system_prompt="You are a fact-checking expert. Follow the instructions exactly and return valid JSON. Be concise but thorough - focus on the most critical issues first.",
                temperature=0.1,  # Low temperature for consistent fact checking
                max_tokens=16000  # Increased to allow for comprehensive fact checking results
            )
            
            # Check for empty response - this is critical for fact checking
            if not response or not response.strip():
                self.logger.error(f"LLM returned empty response for fact checking. Metadata: {metadata}")
                raise ValueError("LLM returned empty response - fact checking cannot proceed without validation")
            
            # Log successful response
            self.logger.info(f"LLM fact checking response received: {len(response)} characters")
            
            return response
            
        except Exception as e:
            self.logger.error(f"LLM fact checking failed: {e}")
            raise
    
    def _parse_llm_fact_checking_response(self, llm_response: str) -> Dict[str, Any]:
        """Parse the LLM response into structured results."""
        try:
            # Try to extract JSON from the response
            import json
            import re
            
            # Look for JSON content in the response
            json_match = re.search(r'\{.*\}', llm_response, re.DOTALL)
            if json_match:
                json_content = json_match.group(0)
                parsed = json.loads(json_content)
                
                # Ensure required fields exist
                if "findings" not in parsed:
                    parsed["findings"] = []
                
                # Generate summary if not provided
                if "validation_summary" not in parsed:
                    findings = parsed.get("findings", [])
                    parsed["validation_summary"] = {
                        "total_claims_checked": len(findings),
                        "claims_verified": len([f for f in findings if f.get("severity") == "VERIFIED"]),
                        "issues_found": len(findings),
                        "critical_issues": len([f for f in findings if f.get("severity") == "CRITICAL"]),
                        "data_integrity_score": 1.0 if len(findings) == 0 else 0.5
                    }
                
                return {
                    "status": "completed",
                    "findings": parsed.get("findings", []),
                    "summary": parsed.get("validation_summary", {}),
                    "raw_llm_response": llm_response
                }
            
            # Fallback if JSON parsing fails
            return {
                "status": "completed",
                "findings": [],
                "summary": {"total_issues": 0, "critical": 0, "errors": 0, "warnings": 0, "verified_claims": 0},
                "raw_llm_response": llm_response,
                "parsing_warning": "Failed to parse structured response from LLM"
            }
            
        except Exception as e:
            self.logger.error(f"Failed to parse LLM response: {e}")
            return {
                "status": "completed",
                "findings": [],
                "summary": {"total_issues": 0, "critical": 0, "errors": 0, "warnings": 0, "verified_claims": 0},
                "raw_llm_response": llm_response,
                "parsing_error": str(e)
            }
    
    def _log_resource_access(self, resource_name: str, resource_data: Any) -> None:
        """
        Log when a resource is successfully accessed by the LLM.
        
        Args:
            resource_name: Name of the resource being accessed
            resource_data: The resource data that was accessed
        """
        try:
            if resource_data:
                # Log successful resource access
                print(f"✅ LLM successfully accessed {resource_name}")
                self.logger.info(f"✅ LLM successfully accessed {resource_name}")
                
                # Log additional details based on resource type
                if resource_name == "synthesis_report" and isinstance(resource_data, dict):
                    content_length = len(resource_data.get("content", ""))
                    print(f"   📄 Synthesis report content: {content_length} characters")
                    self.logger.info(f"   📄 Synthesis report content: {content_length} characters")
                elif resource_name == "evidence_data" and isinstance(resource_data, dict):
                    try:
                        import json
                        content = resource_data.get("content", "{}")
                        parsed = json.loads(content)
                        evidence_count = len(parsed.get("evidence_results", []))
                        total_quotes = parsed.get("metadata", {}).get("total_quotes", 0)
                        print(f"   🔍 Evidence data: {evidence_count} evidence results, {total_quotes} total quotes")
                        self.logger.info(f"   🔍 Evidence data: {evidence_count} evidence results, {total_quotes} total quotes")
                    except Exception as e:
                        print(f"   🔍 Evidence data: Error parsing content - {e}")
                        self.logger.warning(f"   🔍 Evidence data: Error parsing content - {e}")
                elif resource_name == "framework_spec" and isinstance(resource_data, dict):
                    content_length = len(resource_data.get("content", ""))
                    print(f"   📋 Framework specification: {content_length} characters")
                    self.logger.info(f"   📋 Framework specification: {content_length} characters")
                elif resource_name == "raw_analysis_data" and isinstance(resource_data, dict):
                    content_length = len(resource_data.get("content", ""))
                    print(f"   📊 Raw analysis data: {content_length} characters")
                    self.logger.info(f"   📊 Raw analysis data: {content_length} characters")
                elif resource_name == "derived_metrics_data" and isinstance(resource_data, dict):
                    content_length = len(resource_data.get("content", ""))
                    print(f"   📈 Derived metrics data: {content_length} characters (will be summarized)")
                    self.logger.info(f"   📈 Derived metrics data: {content_length} characters (will be summarized)")
                elif resource_name == "statistical_results_data" and isinstance(resource_data, dict):
                    content_length = len(resource_data.get("content", ""))
                    print(f"   📉 Statistical results data: {content_length} characters (will be summarized)")
                    self.logger.info(f"   📉 Statistical results data: {content_length} characters (will be summarized)")
                elif resource_name == "corpus_index":
                    print(f"   🔎 Corpus index service: {type(resource_data).__name__}")
                    self.logger.info(f"   🔎 Corpus index service: {type(resource_data).__name__}")
                elif resource_name == "search_wrappers" and isinstance(resource_data, dict):
                    wrapper_count = len(resource_data)
                    print(f"   🛠️ Search wrappers: {wrapper_count} methods available")
                    self.logger.info(f"   🛠️ Search wrappers: {wrapper_count} methods available")
            else:
                # Log missing resource
                print(f"⚠️ LLM could not access {resource_name}: resource not available")
                self.logger.warning(f"⚠️ LLM could not access {resource_name}: resource not available")
                
        except Exception as e:
            print(f"Failed to log resource access for {resource_name}: {e}")
            self.logger.warning(f"Failed to log resource access for {resource_name}: {e}")
