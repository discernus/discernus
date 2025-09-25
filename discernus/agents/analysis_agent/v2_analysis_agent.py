#!/usr/bin/env python3
"""
V2 Analysis Agent - Atomic Processing Implementation
==================================================

This agent processes documents atomically - each document gets its own artifacts
for all 6 analysis steps. This prevents token limit issues and ensures proper
atomic processing.

THIN Principles:
- Each document processed individually through all 6 steps
- No batch processing that could hit token limits
- Clean separation of concerns
- Atomic artifacts for downstream consumption
"""

import json
import logging
import yaml
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional

from discernus.core.security_boundary import ExperimentSecurityBoundary
from discernus.core.audit_logger import AuditLogger
from discernus.core.local_artifact_storage import LocalArtifactStorage
from discernus.core.agent_result import AgentResult
from discernus.core.run_context import RunContext
from discernus.core.standard_agent import StandardAgent
from discernus.core.unified_logger import get_unified_logger
from discernus.gateway.llm_gateway import LLMGateway
from discernus.gateway.model_registry import get_model_registry


class V2AnalysisAgent(StandardAgent):
    """
    V2 Analysis Agent with atomic document processing.
    
    This agent processes each document individually through 4 analysis steps:
    1. Composite Analysis
    2. Evidence Extraction  
    3. Score Extraction
    4. Markup Extraction
    
    Each document gets its own set of artifacts, preventing token limit issues.
    """
    
    def __init__(self, 
                 security: ExperimentSecurityBoundary,
                 storage: LocalArtifactStorage,
                 audit: AuditLogger):
        """
        Initialize the V2 Analysis Agent.
        
        Args:
            security: Security boundary for file operations
            storage: Content-addressable artifact storage
            audit: Audit logger for comprehensive event tracking
        """
        super().__init__(security, storage, audit)
        self.agent_name = "V2AnalysisAgent"
        
        # Initialize LLM gateway
        model_registry = get_model_registry()
        self.gateway = LLMGateway(model_registry)
        
        # Initialize unified logger
        self.unified_logger = get_unified_logger()
        
        # Load YAML prompt template
        self.prompt_template = self._load_prompt_template()
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
        
        # Log initialization
        self.audit.log_agent_event(self.agent_name, "initialization", {
            "agent_type": "V2AnalysisAgent",
            "config_keys": []
        })

    def _load_prompt_template(self) -> str:
        """Load the framework-agnostic prompt template from the YAML file."""
        prompt_path = Path(__file__).parent / "prompt2.yaml"
        if not prompt_path.exists():
            error_msg = f"V2AnalysisAgent prompt file not found at {prompt_path}"
            self.audit.log_agent_event(self.agent_name, "prompt_error", {"error": error_msg})
            raise FileNotFoundError(error_msg)
        
        with open(prompt_path, 'r') as f:
            yaml_content = f.read()
        prompt_data = yaml.safe_load(yaml_content)
        return prompt_data['template']

    def get_capabilities(self) -> List[str]:
        """Return agent capabilities."""
        return [
            "composite_analysis_with_markup",
            "evidence_extraction", 
            "score_extraction",
            "derived_metrics",
            "verification",
            "markup_extraction"
        ]

    def _validate_inputs(self, run_context: RunContext) -> bool:
        """Strict contract enforcement: ALL required input assets must be present or fail hard."""
        
        # Required Asset 1: Framework hash
        framework_hash = run_context.metadata.get("framework_hash")
        if not framework_hash:
            self.logger.error("CONTRACT VIOLATION: No framework_hash found in run_context metadata")
            return False
        self.logger.info(f"✓ Framework: Found hash {framework_hash[:8]}")
        
        # Required Asset 2: Corpus manifest hash
        corpus_manifest_hash = run_context.metadata.get("corpus_manifest_hash")
        if not corpus_manifest_hash:
            self.logger.error("CONTRACT VIOLATION: No corpus_manifest_hash found in run_context metadata")
            return False
        self.logger.info(f"✓ Corpus manifest: Found hash {corpus_manifest_hash[:8]}")
        
        # Required Asset 3: Corpus document hashes
        corpus_document_hashes = run_context.metadata.get("corpus_document_hashes", [])
        if not corpus_document_hashes:
            self.logger.error("CONTRACT VIOLATION: No corpus_document_hashes found in run_context metadata")
            return False
        self.logger.info(f"✓ Corpus documents: Found {len(corpus_document_hashes)} documents")
        
        self.logger.info("CONTRACT FULFILLED: All required input assets present - proceeding with analysis")
        return True

    def execute(self, run_context: RunContext = None, **kwargs) -> AgentResult:
        """
        Execute atomic document analysis.
        
        Args:
            run_context: Run context with experiment data
            **kwargs: Additional arguments
            
        Returns:
            AgentResult with analysis artifacts
        """
        try:
            # Validate inputs - strict contract enforcement
            if not self._validate_inputs(run_context):
                return AgentResult(
                    success=False,
                    artifacts=[],
                    metadata={"agent_name": self.agent_name, "error": "Input validation failed"},
                    error_message="Required inputs missing for analysis"
                )
            
            # Get framework content via CAS
            framework_hash = run_context.metadata.get("framework_hash")
            framework_content = self.storage.get_artifact(framework_hash).decode('utf-8')
            
            corpus_documents = self._read_corpus_documents_via_cas(run_context)

            if not corpus_documents:
                return AgentResult(
                    success=False,
                    error_message="Failed to read corpus documents via CAS discovery",
                    artifacts=[],
                    metadata={"agent_name": self.agent_name}
                )

            # Generate batch ID for this analysis
            batch_id = f"v2_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

            # Process documents atomically - each document gets its own artifacts
            self.logger.info(f"Starting atomic document processing for batch {batch_id}")
            documents = corpus_documents
            all_artifacts = []
            
            # Show total document count
            self.unified_logger.info(f"📊 Running atomic document analysis... ({len(documents)} documents)")
            
            for doc_index, doc in enumerate(documents):
                doc_name = doc.get('id', doc.get('name', doc.get('filename', f'document_{doc_index}')))
                self.logger.info(f"Processing document {doc_index}: {doc_name}")
                
                # Show document progress
                self.unified_logger.progress(f"Analyzing document {doc_index + 1}/{len(documents)}: {doc_name}")
                
                # Process this document atomically through all 6 steps
                doc_artifacts = self._process_document_atomically(
                    framework_content, doc, doc_index, batch_id
                )
                all_artifacts.extend(doc_artifacts)
            
            # REMOVED: Artifact filtering - agents now use CAS discovery with proper metadata labels
            # Each artifact is correctly labeled during put_artifact() with appropriate artifact_type
            run_context.analysis_results = {
                "documents_processed": len(documents),
                "processing_mode": "atomic",
                "batch_id": batch_id
            }

            self.logger.info(f"Total artifacts created: {len(all_artifacts)} - agents will use CAS discovery")

            # Analysis completed successfully
            self.unified_logger.success(f"🎉 Atomic document analysis completed - {len(documents)} documents processed")
            
            # Return results from atomic processing
            return AgentResult(
                success=True,
                artifacts=all_artifacts,
                metadata={
                    "batch_id": batch_id,
                    "documents_processed": len(documents),
                    "agent_name": self.agent_name,
                    "processing_mode": "atomic"
                }
            )
                
        except Exception as e:
            self.logger.error(f"V2AnalysisAgent execution failed: {e}")
            self.audit.log_agent_event(self.agent_name, "analysis_failed", {
                "error": str(e),
                "error_type": type(e).__name__
            })
            
            return AgentResult(
                success=False,
                artifacts=[],
                metadata={"agent_name": self.agent_name},
                error_message=f"V2AnalysisAgent execution failed: {str(e)}"
            )

    def _process_document_atomically(self, 
                                   framework_content: str, 
                                   doc: Dict[str, Any], 
                                   doc_index: int, 
                                   batch_id: str) -> List[Dict[str, Any]]:
        """
        Process a single document through 4 analysis steps atomically.
        
        Args:
            framework_content: Framework content for analysis
            doc: Document to process
            doc_index: Index of document in corpus
            batch_id: Batch identifier
        
        Returns:
            List of artifacts created for this document
        """
        artifacts = []
        
        try:
            # Step 1: Composite Analysis
            self.unified_logger.progress(f"  Step 1/4: Composite analysis for document {doc_index + 1}")
            composite_result = self._step1_composite_analysis(framework_content, doc, doc_index, batch_id)
            if not composite_result:
                raise ValueError(f"Composite analysis failed for document {doc_index + 1}")
            artifacts.append(composite_result)
            
            # Step 2: Evidence Extraction
            self.unified_logger.progress(f"  Step 2/4: Evidence extraction for document {doc_index + 1}")
            evidence_result = self._step2_evidence_extraction(composite_result, doc, doc_index, batch_id)
            if evidence_result:
                artifacts.append(evidence_result)
            
            # Step 3: Score Extraction
            self.unified_logger.progress(f"  Step 3/4: Score extraction for document {doc_index + 1}")
            scores_result = self._step3_score_extraction(composite_result, doc, doc_index, batch_id)
            if scores_result:
                artifacts.append(scores_result)
            
            # Step 4: Markup Extraction
            self.unified_logger.progress(f"  Step 4/4: Markup extraction for document {doc_index + 1}")
            markup_result = self._step4_markup_extraction(composite_result, doc, doc_index, batch_id)
            if markup_result:
                artifacts.append(markup_result)
            
            # Document completed successfully
            self.unified_logger.success(f"✅ Document {doc_index + 1} analysis completed")
                
        except Exception as e:
            self.logger.error(f"Atomic processing failed for document {doc_index}: {e}")
            self.audit.log_agent_event(self.agent_name, "atomic_processing_failed", {
                "document_index": doc_index,
                "error": str(e)
            })
        
        return artifacts

    def _build_human_context_from_cas(self, analysis_phase: str, doc: Dict[str, Any], doc_index: int) -> Dict[str, str]:
        """
        Build human context for artifact naming by discovering run context from CAS.
        
        Args:
            analysis_phase: The analysis phase (e.g., "composite_analysis", "markup_extraction")
            doc: Document metadata
            doc_index: Document index
            
        Returns:
            Dictionary with human-readable context for artifact naming
        """
        try:
            # Discover run context from CAS
            run_context_artifacts = self.storage.find_artifacts_by_metadata(artifact_type="run_context")
            
            if run_context_artifacts and len(run_context_artifacts) > 0:
                # Get the most recent run context
                run_context_artifact = run_context_artifacts[0]
                self.logger.debug(f"Run context artifact type: {type(run_context_artifact)}, content: {run_context_artifact}")
                
                # Handle both dict and string formats
                if isinstance(run_context_artifact, dict):
                    artifact_hash = run_context_artifact.get('hash', run_context_artifact)
                else:
                    artifact_hash = run_context_artifact
                    
                run_context_content = self.storage.get_artifact(artifact_hash)
                
                if run_context_content:
                    try:
                        import json
                        run_context_data = json.loads(run_context_content.decode('utf-8'))
                        experiment_name = run_context_data.get('experiment_name', 'unknown_experiment')
                    except (json.JSONDecodeError, KeyError, TypeError) as e:
                        self.logger.warning(f"Could not parse run context data: {e}")
                        experiment_name = 'unknown_experiment'
                else:
                    experiment_name = 'unknown_experiment'
            else:
                experiment_name = 'unknown_experiment'
            
            # Build human context - use actual filename from document metadata
            source_document_name = doc.get('filename', f'document_{doc_index}')
            # Clean the filename for use in artifact names
            if source_document_name:
                # Remove extension and clean for filename use
                import os
                clean_name = os.path.splitext(source_document_name)[0]
                source_document_name = clean_name
            
            return {
                "source_document_name": source_document_name,
                "experiment_name": experiment_name,
                "analysis_phase": analysis_phase
            }
            
        except Exception as e:
            self.logger.warning(f"Could not build human context from CAS: {e}")
            # Fallback to basic context
            return {
                "source_document_name": doc.get('filename', f'document_{doc_index}'),
                "experiment_name": 'unknown_experiment',
                "analysis_phase": analysis_phase
            }

    def _step1_composite_analysis(self, framework_content: str, doc: Dict[str, Any], doc_index: int, batch_id: str) -> Optional[Dict[str, Any]]:
        """Step 1: Composite Analysis for a single document."""
        try:
            # Create analysis prompt using YAML template with defensive programming
            document_content = doc.get('content', '')
            
            # Defensive programming: Handle None values
            if framework_content is None:
                framework_content = 'No framework content available'
            if document_content is None:
                document_content = 'No document content available'
            
            # NO TRUNCATION: Both frameworks and documents are sacred intellectual assets
            
            prompt = self.prompt_template.replace('{framework_content}', framework_content).replace('{document_content}', document_content)

            # Call LLM
            response = self.gateway.execute_call(
                model="vertex_ai/gemini-2.5-flash",
                prompt=prompt
            )
            
            if isinstance(response, tuple):
                content, metadata = response
            else:
                content = response.get('content', '')
                metadata = response.get('metadata', {})
            
            # FAIL HARD: Check if LLM response is valid
            if content is None or content.strip() == '':
                self.logger.error(f"CRITICAL: Composite analysis failed for document {doc_index} - LLM returned empty response")
                self.logger.error(f"Response type: {type(response)}, Content: {content}")
                self.logger.error(f"Metadata: {metadata}")
                self.logger.error(f"Prompt length: {len(prompt)} characters")
                raise ValueError(f"Composite analysis failed: LLM returned empty response for document {doc_index}")
            
            # Log LLM interaction with cost data
            if metadata and 'usage' in metadata:
                usage_data = metadata['usage']
                self.audit.log_llm_interaction(
                    model="vertex_ai/gemini-2.5-flash",
                    prompt=prompt,
                    response=content,
                    agent_name=self.agent_name,
                    interaction_type="composite_analysis",
                    metadata={
                        "prompt_tokens": usage_data.get('prompt_tokens', 0),
                        "completion_tokens": usage_data.get('completion_tokens', 0),
                        "total_tokens": usage_data.get('total_tokens', 0),
                        "response_cost_usd": usage_data.get('response_cost_usd', 0.0),
                        "step": "composite_analysis",
                        "document_index": doc_index
                    }
                )
            
            # Create artifact
            artifact_data = {
                "analysis_id": f"analysis_{batch_id}_{doc_index}",
                "step": "composite_analysis",
                "model_used": "vertex_ai/gemini-2.5-flash",
                "raw_analysis_response": content,
                "document_index": doc_index,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
            # Store artifact
            content_bytes = json.dumps(artifact_data, indent=2).encode('utf-8')
            
            # Enhanced naming with human context from CAS
            human_context = self._build_human_context_from_cas("composite_analysis", doc, doc_index)
            
            artifact_hash = self.storage.put_artifact(
                content_bytes,
                {"artifact_type": "composite_analysis", "document_index": doc_index},
                human_context
            )
            
            return {
                "type": "composite_analysis",
                "content": artifact_data,
                "metadata": {
                    "artifact_type": "composite_analysis",
                    "phase": "analysis",
                    "batch_id": batch_id,
                    "document_index": doc_index,
                    "timestamp": datetime.now().isoformat(),
                    "agent_name": self.agent_name,
                    "artifact_hash": artifact_hash
                }
            }
            
        except Exception as e:
            self.logger.error(f"Step 1 failed for document {doc_index}: {e}")
            return None

    def _step2_evidence_extraction(self, composite_result: Dict[str, Any], doc: Dict[str, Any], doc_index: int, batch_id: str) -> Optional[Dict[str, Any]]:
        """Step 2: Extract evidence from composite result."""
        try:
            if not composite_result or 'content' not in composite_result:
                return None
                
            raw_response = composite_result['content'].get('raw_analysis_response', '')
            
            # Defensive programming: Handle None values
            if raw_response is None:
                raw_response = 'No analysis result available'
            
            prompt = f"""You are extracting ALL evidence quotes from a discourse analysis. 

ANALYSIS RESULT:
{raw_response}

TASK: Extract ALL evidence quotes from the analysis result. Do NOT curate or select - extract every single quote that appears in the evidence_quotes sections.

REQUIREMENTS:
- Extract EVERY quote from ALL dimensional evidence_quotes sections
- Do NOT curate, select, or filter quotes
- Include ALL quotes regardless of quality or redundancy
- Count the total number of quotes in the composite analysis
- Count the total number of quotes in your output
- Ensure the counts match exactly
- Format as a simple JSON array of strings

OUTPUT FORMAT:
["quote1", "quote2", "quote3", ...]

Return ONLY the JSON array, no other text."""

            # Call LLM
            response = self.gateway.execute_call(
                model="vertex_ai/gemini-2.5-flash-lite",
                prompt=prompt
            )
            
            if isinstance(response, tuple):
                content, metadata = response
            else:
                content = response.get('content', '')
                metadata = response.get('metadata', {})
            
            # Log LLM interaction with cost data
            if metadata and 'usage' in metadata:
                usage_data = metadata['usage']
                self.audit.log_llm_interaction(
                    model="vertex_ai/gemini-2.5-flash-lite",
                    prompt=prompt,
                    response=content,
                    agent_name=self.agent_name,
                    interaction_type="evidence_extraction",
                    metadata={
                        "prompt_tokens": usage_data.get('prompt_tokens', 0),
                        "completion_tokens": usage_data.get('completion_tokens', 0),
                        "total_tokens": usage_data.get('total_tokens', 0),
                        "response_cost_usd": usage_data.get('response_cost_usd', 0.0),
                        "step": "evidence_extraction",
                        "document_index": doc_index
                    }
                )
            
            # THIN: Store LLM response as-is, no validation
            
            # Create artifact
            artifact_data = {
                "analysis_id": f"analysis_{batch_id}_{doc_index}",
                "step": "evidence_extraction",
                "model_used": "vertex_ai/gemini-2.5-flash-lite",
                "evidence_extraction": content,
                "document_index": doc_index,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
            # Store artifact with human context
            content_bytes = json.dumps(artifact_data, indent=2).encode('utf-8')
            human_context = self._build_human_context_from_cas("evidence_extraction", doc, doc_index)
            artifact_hash = self.storage.put_artifact(
                content_bytes,
                {"artifact_type": "evidence_extraction", "document_index": doc_index},
                human_context
            )
            
            return {
                "type": "evidence_extraction",
                "content": artifact_data,
                "metadata": {
                    "artifact_type": "evidence_extraction",
                    "phase": "analysis",
                    "batch_id": batch_id,
                    "document_index": doc_index,
                    "timestamp": datetime.now().isoformat(),
                    "agent_name": self.agent_name,
                    "artifact_hash": artifact_hash
                }
            }
            
        except Exception as e:
            self.logger.error(f"Step 2 failed for document {doc_index}: {e}")
            return None

    def _step3_score_extraction(self, composite_result: Dict[str, Any], doc: Dict[str, Any], doc_index: int, batch_id: str) -> Optional[Dict[str, Any]]:
        """Step 3: Extract scores from composite result."""
        try:
            if not composite_result or 'content' not in composite_result:
                return None
                
            raw_response = composite_result['content'].get('raw_analysis_response', '')
            
            # Defensive programming: Handle None values
            if raw_response is None:
                raw_response = 'No analysis result available'
            
            prompt = f"""Extract the dimensional scores AND derived metrics from this analysis result, preserving ALL computational variables:

{raw_response}

EXTRACTION REQUIREMENTS:
- Extract raw_score, salience, and confidence for each dimension
- Extract ALL derived metrics (tension indices, cohesion components, cohesion indices)
- Preserve the complete data structure from the analysis
- Do not strip away any computational variables

OUTPUT FORMAT:
Return a JSON object with two main sections:
{{
  "dimensional_scores": {{
  "dimension_name": {{
    "raw_score": 0.8,
    "salience": 0.7,
    "confidence": 0.9
    }}
  }},
  "derived_metrics": {{
    "identity_tension": 0.07,
    "emotional_tension": 0.0,
    "strategic_contradiction_index": 0.042,
    "descriptive_cohesion_index": -0.220,
    "motivational_cohesion_index": -0.131,
    "full_cohesion_index": -0.136
  }}
}}

Extract both dimensional scores AND derived metrics preserving all computational variables."""

            # Call LLM
            response = self.gateway.execute_call(
                model="vertex_ai/gemini-2.5-flash-lite",
                prompt=prompt
            )
            
            if isinstance(response, tuple):
                content, metadata = response
            else:
                content = response.get('content', '')
                metadata = response.get('metadata', {})
            
            # Log LLM interaction with cost data
            if metadata and 'usage' in metadata:
                usage_data = metadata['usage']
                self.audit.log_llm_interaction(
                    model="vertex_ai/gemini-2.5-flash-lite",
                    prompt=prompt,
                    response=content,
                    agent_name=self.agent_name,
                    interaction_type="score_extraction",
                    metadata={
                        "prompt_tokens": usage_data.get('prompt_tokens', 0),
                        "completion_tokens": usage_data.get('completion_tokens', 0),
                        "total_tokens": usage_data.get('total_tokens', 0),
                        "response_cost_usd": usage_data.get('response_cost_usd', 0.0),
                        "step": "score_extraction",
                        "document_index": doc_index
                    }
                )
            
            # Create artifact
            artifact_data = {
                "analysis_id": f"analysis_{batch_id}_{doc_index}",
                "step": "score_extraction",
                "model_used": "vertex_ai/gemini-2.5-flash-lite",
                "score_extraction": content,
                "document_index": doc_index,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
            # Store artifact with human context
            content_bytes = json.dumps(artifact_data, indent=2).encode('utf-8')
            human_context = self._build_human_context_from_cas("score_extraction", doc, doc_index)
            artifact_hash = self.storage.put_artifact(
                content_bytes,
                {"artifact_type": "score_extraction", "document_index": doc_index},
                human_context
            )
            
            return {
                "type": "score_extraction",
                "content": artifact_data,
                "metadata": {
                    "artifact_type": "score_extraction",
                    "phase": "analysis",
                    "batch_id": batch_id,
                    "document_index": doc_index,
                    "timestamp": datetime.now().isoformat(),
                    "agent_name": self.agent_name,
                    "artifact_hash": artifact_hash
                }
            }
            
        except Exception as e:
            self.logger.error(f"Step 3 failed for document {doc_index}: {e}")
            return None


    
    def _framework_defines_derived_metrics(self, framework_content: str) -> bool:
        """
        Check if the framework defines derived metrics using LLM intelligence.
        
        Returns True if the framework defines derived metrics, False otherwise.
        """
        try:
            prompt = f"""
            Examine this framework and determine if it defines any derived metrics.
            
            Framework content:
            {framework_content}
            
            Look for:
            - Derived metrics definitions
            - Calculated metrics
            - Composite metrics
            - Any metrics that are computed from other metrics
            
            Respond with only "YES" if derived metrics are defined, or "NO" if not.
            """
            
            response, metadata = self.gateway.execute_call(
                model="vertex_ai/gemini-2.5-flash",
                prompt=prompt,
                system_prompt="You are a framework analysis expert. Answer only YES or NO.",
                max_retries=1
            )
            
            if metadata.get("success") and response:
                return response.strip().upper() == "YES"
            
            # If check fails, assume derived metrics exist to be safe
            return True
            
        except Exception as e:
            self.logger.warning(f"Failed to check for derived metrics: {e}")
            # If check fails, assume derived metrics exist to be safe
            return True
    

    def _step4_markup_extraction(self, composite_result: Dict[str, Any], doc: Dict[str, Any], doc_index: int, batch_id: str) -> Optional[Dict[str, Any]]:
        """Step 4: Extract markup from composite result."""
        try:
            if not composite_result or 'content' not in composite_result:
                return None
                
            raw_response = composite_result['content'].get('raw_analysis_response', '')
            
            # Defensive programming: Handle None values
            if raw_response is None:
                raw_response = 'No analysis result available'
            
            prompt = f"""Extract the marked-up document from this analysis result:

{raw_response}

Return the marked-up document in markdown format."""

            # Call LLM
            response = self.gateway.execute_call(
                model="vertex_ai/gemini-2.5-flash-lite",
                prompt=prompt
            )
            
            if isinstance(response, tuple):
                content, metadata = response
            else:
                content = response.get('content', '')
                metadata = response.get('metadata', {})
            
            # Log LLM interaction with cost data
            if metadata and 'usage' in metadata:
                usage_data = metadata['usage']
                self.audit.log_llm_interaction(
                    model="vertex_ai/gemini-2.5-flash-lite",
                    prompt=prompt,
                    response=content,
                    agent_name=self.agent_name,
                    interaction_type="markup_extraction",
                    metadata={
                        "prompt_tokens": usage_data.get('prompt_tokens', 0),
                        "completion_tokens": usage_data.get('completion_tokens', 0),
                        "total_tokens": usage_data.get('total_tokens', 0),
                        "response_cost_usd": usage_data.get('response_cost_usd', 0.0),
                        "step": "markup_extraction",
                        "document_index": doc_index
                    }
                )
            
            # Create markdown content with metadata header
            timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
            markdown_content = f"""---
analysis_id: analysis_{batch_id}_{doc_index}
step: markup_extraction
model_used: vertex_ai/gemini-2.5-flash-lite
document_index: {doc_index}
timestamp: {timestamp}
---

{content}"""
            
            # Store as markdown content
            content_bytes = markdown_content.encode('utf-8')
            
            # Enhanced naming with human context from CAS
            human_context = self._build_human_context_from_cas("markup_extraction", doc, doc_index)
            
            artifact_hash = self.storage.put_artifact(
                content_bytes,
                {"artifact_type": "marked_up_document", "document_index": doc_index},
                human_context
            )
            
            return {
                "type": "marked_up_document",
                "content": markdown_content,
                "metadata": {
                    "artifact_type": "marked_up_document",
                    "phase": "analysis",
                    "batch_id": batch_id,
                    "document_index": doc_index,
                    "timestamp": datetime.now().isoformat(),
                    "agent_name": self.agent_name,
                    "artifact_hash": artifact_hash
                }
            }
            
        except Exception as e:
            self.logger.error(f"Step 4 failed for document {doc_index}: {e}")
            return None
    
    def _read_framework_file(self, framework_path: str) -> Optional[str]:
        """Read framework content directly from file."""
        try:
            return Path(framework_path).read_text(encoding='utf-8')
        except Exception as e:
            self.logger.error(f"Failed to read framework file {framework_path}: {e}")
            return None
    
    def _read_corpus_documents_via_cas(self, run_context: RunContext) -> List[Dict[str, str]]:
        """Read corpus documents using CAS discovery."""
        try:
            # CAS Discovery: Get corpus document hashes from run_context metadata
            corpus_document_hashes = run_context.metadata.get("corpus_document_hashes", [])
            if not corpus_document_hashes:
                self.logger.error("No corpus document hashes found in run_context metadata")
                return []
            
            documents = []
            for doc_hash in corpus_document_hashes:
                try:
                    # Get document content from CAS
                    doc_content = self.storage.get_artifact(doc_hash).decode('utf-8')
                    
                    # Get document metadata from CAS registry
                    doc_metadata = self.storage.get_artifact_metadata(doc_hash)
                    document_id = doc_metadata.get("document_id", doc_hash[:8])
                    filename = doc_metadata.get("filename", f"document_{document_id}")
                    
                    documents.append({
                        "id": document_id,
                        "filename": filename,  # Include filename for human-readable naming
                        "content": doc_content,
                    })
                except Exception as e:
                    self.logger.warning(f"Failed to load document {doc_hash}: {e}")
            
            self.logger.info(f"Loaded {len(documents)} corpus documents via CAS discovery")
            return documents
            
        except Exception as e:
            self.logger.error(f"Failed to read corpus documents via CAS: {e}")
            return []

