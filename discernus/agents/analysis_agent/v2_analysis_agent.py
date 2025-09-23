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
            # THIN: Read framework and corpus files directly
            framework_content = self._read_framework_file(run_context.framework_path)
            corpus_documents = self._read_corpus_documents(run_context.corpus_path)

            if not framework_content:
                return AgentResult(
                    success=False,
                    error_message=f"Failed to read framework file: {run_context.framework_path}",
                    metadata={"agent_name": self.agent_name}
                )

            if not corpus_documents:
                return AgentResult(
                    success=False,
                    error_message=f"Failed to read corpus documents from: {run_context.corpus_path}", 
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
            if composite_result:
                artifacts.append(composite_result)
            
            # Step 2: Evidence Extraction
            self.unified_logger.progress(f"  Step 2/4: Evidence extraction for document {doc_index + 1}")
            evidence_result = self._step2_evidence_extraction(composite_result, doc_index, batch_id)
            if evidence_result:
                artifacts.append(evidence_result)
            
            # Step 3: Score Extraction
            self.unified_logger.progress(f"  Step 3/4: Score extraction for document {doc_index + 1}")
            scores_result = self._step3_score_extraction(composite_result, doc_index, batch_id)
            if scores_result:
                artifacts.append(scores_result)
            
            # Step 4: Markup Extraction
            self.unified_logger.progress(f"  Step 4/4: Markup extraction for document {doc_index + 1}")
            markup_result = self._step4_markup_extraction(composite_result, doc_index, batch_id)
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

    def _step1_composite_analysis(self, framework_content: str, doc: Dict[str, Any], doc_index: int, batch_id: str) -> Optional[Dict[str, Any]]:
        """Step 1: Composite Analysis for a single document."""
        try:
            # Create analysis prompt using YAML template
            document_content = doc.get('content', '')
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
            artifact_hash = self.storage.put_artifact(
                content_bytes,
                {"artifact_type": "composite_analysis", "document_index": doc_index}
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

    def _step2_evidence_extraction(self, composite_result: Dict[str, Any], doc_index: int, batch_id: str) -> Optional[Dict[str, Any]]:
        """Step 2: Extract evidence from composite result."""
        try:
            if not composite_result or 'content' not in composite_result:
                return None
                
            raw_response = composite_result['content'].get('raw_analysis_response', '')
            
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
            
            # Store artifact
            content_bytes = json.dumps(artifact_data, indent=2).encode('utf-8')
            artifact_hash = self.storage.put_artifact(
                content_bytes,
                {"artifact_type": "evidence_extraction", "document_index": doc_index}
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

    def _step3_score_extraction(self, composite_result: Dict[str, Any], doc_index: int, batch_id: str) -> Optional[Dict[str, Any]]:
        """Step 3: Extract scores from composite result."""
        try:
            if not composite_result or 'content' not in composite_result:
                return None
                
            raw_response = composite_result['content'].get('raw_analysis_response', '')
            
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
            
            # Create artifact
            artifact_data = {
                "analysis_id": f"analysis_{batch_id}_{doc_index}",
                "step": "score_extraction",
                "model_used": "vertex_ai/gemini-2.5-flash-lite",
                "score_extraction": content,
                "document_index": doc_index,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
            # Store artifact
            content_bytes = json.dumps(artifact_data, indent=2).encode('utf-8')
            artifact_hash = self.storage.put_artifact(
                content_bytes,
                {"artifact_type": "score_extraction", "document_index": doc_index}
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
    

    def _step4_markup_extraction(self, composite_result: Dict[str, Any], doc_index: int, batch_id: str) -> Optional[Dict[str, Any]]:
        """Step 4: Extract markup from composite result."""
        try:
            if not composite_result or 'content' not in composite_result:
                return None
                
            raw_response = composite_result['content'].get('raw_analysis_response', '')
            
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
            artifact_hash = self.storage.put_artifact(
                content_bytes,
                {"artifact_type": "marked_up_document", "document_index": doc_index}
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
    
    def _read_corpus_documents(self, corpus_path: str) -> List[Dict[str, str]]:
        """Read corpus documents directly from manifest file."""
        try:
            import yaml
            import re
            
            corpus_manifest_path = Path(corpus_path)
            if not corpus_manifest_path.exists():
                self.logger.error(f"Corpus manifest not found: {corpus_path}")
                return []
            
            manifest_text = corpus_manifest_path.read_text(encoding='utf-8')
            
            # Extract YAML block from markdown
            yaml_match = re.search(r"```yaml\n(.*?)```", manifest_text, re.DOTALL)
            if not yaml_match:
                yaml_content = manifest_text
            else:
                yaml_content = yaml_match.group(1)

            manifest = yaml.safe_load(yaml_content)
            
            documents = []
            corpus_dir = corpus_manifest_path.parent / 'corpus'
            
            for doc_info in manifest.get('documents', []):
                doc_path = corpus_dir / doc_info['filename']
                if doc_path.exists():
                    content = doc_path.read_text(encoding='utf-8')
                    documents.append({
                        "id": doc_info.get('document_id', doc_info['filename']),
                        "content": content,
                    })
                else:
                    self.logger.warning(f"Document file not found: {doc_path}")
            
            return documents
        except Exception as e:
            self.logger.error(f"Failed to read corpus documents from {corpus_path}: {e}")
            return []

