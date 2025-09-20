#!/usr/bin/env python3
"""
Analysis Agent - THIN v2.0 Architecture
=======================================

Production analysis agent with 6-step THIN approach featuring inline markup,
comprehensive logging, and full orchestrator compatibility.

This agent is completely experiment-agnostic and can handle any framework
without modification.
"""

import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional
import yaml

from discernus.core.security_boundary import ExperimentSecurityBoundary
from discernus.core.audit_logger import AuditLogger
from discernus.core.local_artifact_storage import LocalArtifactStorage
from discernus.gateway.llm_gateway_enhanced import EnhancedLLMGateway


class AnalysisAgentError(Exception):
    """Analysis agent specific exceptions"""
    pass


class AnalysisAgent:
    """Production analysis agent with 6-step THIN approach and inline markup."""

    def __init__(self,
                 security_boundary: ExperimentSecurityBoundary,
                 audit_logger: AuditLogger,
                 artifact_storage: LocalArtifactStorage):
        self.security = security_boundary
        self.audit = audit_logger
        self.storage = artifact_storage
        self.agent_name = "AnalysisAgent"
        self.gateway = EnhancedLLMGateway(self.audit)
        self.prompt_template = self._load_prompt_template()

        self.audit.log_agent_event(self.agent_name, "initialization", {
            "security_boundary": self.security.get_boundary_info(),
            "capabilities": [
                "composite_analysis_with_markup", 
                "evidence_extraction", 
                "score_extraction", 
                "derived_metrics", 
                "verification", 
                "markup_extraction"
            ]
        })

    def _load_prompt_template(self) -> str:
        """Load the framework-agnostic prompt template from the YAML file."""
        prompt_path = Path(__file__).parent / "prompt.yaml"
        if not prompt_path.exists():
            error_msg = f"AnalysisAgent prompt file not found at {prompt_path}"
            self.audit.log_agent_event(self.agent_name, "prompt_error", {"error": error_msg})
            raise FileNotFoundError(error_msg)
        
        with open(prompt_path, 'r') as f:
            yaml_content = f.read()
        prompt_data = yaml.safe_load(yaml_content)
        return prompt_data['template']

    def analyze_documents(self, 
                         framework_content: str, 
                         documents: List[Dict[str, Any]], 
                         experiment_metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Analyze documents using the 6-step THIN approach.
        
        Args:
            framework_content: Raw framework file content
            documents: List of document dictionaries with 'content', 'name', etc.
            experiment_metadata: Optional experiment metadata
            
        Returns:
            Dictionary containing all analysis results and artifacts
        """
        analysis_id = self._generate_analysis_id()
        
        self.audit.log_agent_event(self.agent_name, "analysis_started", {
            "analysis_id": analysis_id,
            "document_count": len(documents),
            "framework_provided": bool(framework_content),
            "experiment_metadata": experiment_metadata
        })

        try:
            # Process documents individually for integrity and scalability
            all_composite_results = []
            all_evidence_results = []
            all_scores_results = []
            all_derived_metrics_results = []
            all_verification_results = []
            all_markup_results = []

            for doc_index, doc in enumerate(documents):
                doc_name = doc.get('id', doc.get('name', doc.get('filename', f'document_{doc_index}')))
                self.audit.log_agent_event(self.agent_name, "document_analysis_started", {
                    "analysis_id": analysis_id,
                    "document_index": doc_index,
                    "document_name": doc_name,
                    "total_documents": len(documents)
                })

                # Step 1: Enhanced Composite Analysis (individual document)
                composite_result = self._step1_enhanced_composite_analysis_single(
                    framework_content, doc, doc_index, analysis_id
                )
                all_composite_results.append(composite_result)
            
            # Step 2: Evidence Extraction
            evidence_result = self._step2_evidence_extraction(composite_result, analysis_id)
            all_evidence_results.append(evidence_result)
            
            # Step 3: Score Extraction
            scores_result = self._step3_score_extraction(composite_result, analysis_id)
            all_scores_results.append(scores_result)
            
            # Step 4: Derived Metrics Generation
            derived_metrics_result = self._step4_derived_metrics_generation_single(
                framework_content, scores_result, doc_index, analysis_id
            )
            all_derived_metrics_results.append(derived_metrics_result)
            
            # Step 5: Verification
            verification_result = self._step5_verification_single(
                framework_content, derived_metrics_result, scores_result, doc_index, analysis_id
            )
            all_verification_results.append(verification_result)
            
            # Step 6: Markup Extraction
            markup_result = self._step6_markup_extraction(composite_result, analysis_id)
            all_markup_results.append(markup_result)

            self.audit.log_agent_event(self.agent_name, "document_analysis_completed", {
                "analysis_id": analysis_id,
                "document_index": doc_index,
                "document_name": doc_name,
                "total_documents": len(documents)
            })

            # Aggregate results from all documents
            composite_result = self._aggregate_composite_results(all_composite_results, analysis_id)
            evidence_result = self._aggregate_evidence_results(all_evidence_results, analysis_id)
            scores_result = self._aggregate_scores_results(all_scores_results, analysis_id)
            derived_metrics_result = self._aggregate_derived_metrics_results(all_derived_metrics_results, analysis_id)
            verification_result = self._aggregate_verification_results(all_verification_results, analysis_id)
            markup_result = self._aggregate_markup_results(all_markup_results, analysis_id)
            
            # Step 7: CSV Generation (for statistical offramp)
            csv_result = self._step7_csv_generation(
                framework_content, all_scores_results, all_evidence_results, 
                all_derived_metrics_results, analysis_id
            )
            
            # Compile final results
            final_results = {
                "composite_analysis": composite_result,
                "evidence_extraction": evidence_result,
                "score_extraction": scores_result,
                "derived_metrics": derived_metrics_result,
                "verification": verification_result,
                "markup_extraction": markup_result,
                "csv_generation": csv_result,
                "analysis_metadata": {
                    "analysis_id": analysis_id,
                    "agent_name": self.agent_name,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "document_count": len(documents),
                    "framework_provided": bool(framework_content)
                }
            }
            
            # Generate content-addressable hash for the entire result
            result_json = json.dumps(final_results, sort_keys=True)
            result_hash = self._generate_content_hash(result_json)
            final_results["result_hash"] = result_hash
            
            self.audit.log_agent_event(self.agent_name, "analysis_completed", {
                "analysis_id": analysis_id,
                "result_hash": result_hash,
                "verification_status": verification_result.get("verification_status", "unknown")
            })
            
            return final_results
            
        except Exception as e:
            self.audit.log_agent_event(self.agent_name, "analysis_failed", {
                "analysis_id": analysis_id,
                "error": str(e),
                "error_type": type(e).__name__
            })
            raise AnalysisAgentError(f"Analysis failed: {str(e)}") from e

    def _step1_enhanced_composite_analysis_single(self,
                                         framework_content: str, 
                                                document: Dict[str, Any],
                                                doc_index: int,
                                         analysis_id: str) -> Dict[str, Any]:
        """Step 1: Enhanced composite analysis for a single document."""
        doc_name = document.get('name', document.get('filename', f'document_{doc_index}'))
        
        # Prepare single document for prompt
        document_content = self._prepare_single_document(document, doc_index)
        
        # Create the analysis prompt for single document
        prompt = self.prompt_template.replace('{framework_content}', framework_content).replace('{document_content}', document_content).replace('{analysis_id}', f"{analysis_id}_doc_{doc_index}").replace('{num_documents}', "1")
        
        self.audit.log_agent_event(self.agent_name, "step1_started_single", {
            "analysis_id": analysis_id,
            "step": "enhanced_composite_analysis_generation",
            "model": "vertex_ai/gemini-2.5-flash",
            "document_index": doc_index,
            "document_name": doc_name
        })
        
        # Execute LLM call for single document
        response = self.gateway.execute_call(
            model="vertex_ai/gemini-2.5-flash",
            prompt=prompt
        )
        
        # Extract content from response
        if isinstance(response, tuple):
            content, metadata = response
        else:
            content = response.get('content', '')
            metadata = response.get('metadata', {})
        
        # If content is empty, try to get it from the raw response
        if not content and hasattr(response, 'choices'):
            content = response.choices[0].message.content
        
        # Generate document hash for provenance
        document_hash = self._generate_content_hash(document.get('content', ''))
        
        # Save composite result to artifacts
        composite_data = {
            "analysis_id": analysis_id,
            "step": "enhanced_composite_analysis_generation",
            "model_used": "vertex_ai/gemini-2.5-flash",
            "raw_analysis_response": content,
            "document_hash": document_hash,
            "document_index": doc_index,
            "document_name": doc_name,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        composite_hash = self.storage.put_artifact(
            json.dumps(composite_data, indent=2).encode('utf-8'),
            {"artifact_type": "composite_analysis", "analysis_id": analysis_id, "document_index": doc_index}
        )
        
        composite_data['artifact_hash'] = composite_hash
        
        self.audit.log_agent_event(self.agent_name, "step1_completed_single", {
            "analysis_id": analysis_id,
            "step": "enhanced_composite_analysis_generation",
            "artifact_hash": composite_hash,
            "document_index": doc_index,
            "document_name": doc_name,
            "response_length": len(content)
        })
        
        return composite_data

    def _step4_derived_metrics_generation_single(self,
                                               framework_content: str,
                                               scores_result: Dict[str, Any],
                                               doc_index: int,
                                               analysis_id: str) -> Dict[str, Any]:
        """Step 4: Generate derived metrics for a single document."""
        doc_name = scores_result.get('document_name', f'document_{doc_index}')

        prompt = f"""Based on this framework and the dimensional scores for a single document, generate and execute code to calculate derived metrics:

FRAMEWORK:
{framework_content}

SCORES FOR DOCUMENT: {doc_name}
{scores_result['scores_extraction']}

Generate Python code to calculate derived metrics and execute it internally. Return both the code and the results."""

        self.audit.log_agent_event(self.agent_name, "step4_started_single", {
            "analysis_id": analysis_id,
            "step": "derived_metrics_generation",
            "model": "vertex_ai/gemini-2.5-flash-lite",
            "document_index": doc_index,
            "document_name": doc_name
        })

        response = self.gateway.execute_call(
            model="vertex_ai/gemini-2.5-flash-lite",
            prompt=prompt
        )

        if isinstance(response, tuple):
            content, metadata = response
        else:
            content = response.get('content', '')
            metadata = response.get('metadata', {})

        # If content is empty, try to get it from the raw response
        if not content and hasattr(response, 'choices'):
            content = response.choices[0].message.content

        # Save derived metrics result to artifacts
        derived_metrics_data = {
            "analysis_id": analysis_id,
            "step": "derived_metrics_generation",
            "model_used": "vertex_ai/gemini-2.5-flash-lite",
            "raw_metrics_response": content,
            "document_index": doc_index,
            "document_name": doc_name,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

        derived_metrics_hash = self.storage.put_artifact(
            json.dumps(derived_metrics_data, indent=2).encode('utf-8'),
            {"artifact_type": "derived_metrics", "analysis_id": analysis_id, "document_index": doc_index}
        )

        derived_metrics_data['artifact_hash'] = derived_metrics_hash

        self.audit.log_agent_event(self.agent_name, "step4_completed_single", {
            "analysis_id": analysis_id,
            "step": "derived_metrics_generation",
            "artifact_hash": derived_metrics_hash,
            "document_index": doc_index,
            "document_name": doc_name,
            "response_length": len(content)
        })

        return derived_metrics_data

    def _step5_verification_single(self,
                                 framework_content: str,
                                 derived_metrics_result: Dict[str, Any],
                                 scores_result: Dict[str, Any],
                                 doc_index: int,
                                 analysis_id: str) -> Dict[str, Any]:
        """Step 5: Verify derived metrics for a single document."""
        doc_name = derived_metrics_result.get('document_name', f'document_{doc_index}')

        prompt = f"""Verify the derived metrics calculations for this single document against the framework:

FRAMEWORK:
{framework_content}

DERIVED METRICS:
{derived_metrics_result['raw_metrics_response']}

Verify that the calculations are correct and the metrics are properly derived from the dimensional scores."""

        self.audit.log_agent_event(self.agent_name, "step5_started_single", {
            "analysis_id": analysis_id,
            "step": "verification",
            "model": "vertex_ai/gemini-2.5-flash",
            "document_index": doc_index,
            "document_name": doc_name
        })

        response = self.gateway.execute_call(
            model="vertex_ai/gemini-2.5-flash",
            prompt=prompt
        )

        if isinstance(response, tuple):
            content, metadata = response
        else:
            content = response.get('content', '')
            metadata = response.get('metadata', {})

        # If content is empty, try to get it from the raw response
        if not content and hasattr(response, 'choices'):
            content = response.choices[0].message.content

        # Save verification result to artifacts
        verification_data = {
            "analysis_id": analysis_id,
            "step": "verification",
            "model_used": "vertex_ai/gemini-2.5-flash",
            "raw_verification_response": content,
            "document_index": doc_index,
            "document_name": doc_name,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

        verification_hash = self.storage.put_artifact(
            json.dumps(verification_data, indent=2).encode('utf-8'),
            {"artifact_type": "verification", "analysis_id": analysis_id, "document_index": doc_index}
        )

        verification_data['artifact_hash'] = verification_hash

        self.audit.log_agent_event(self.agent_name, "step5_completed_single", {
            "analysis_id": analysis_id,
            "step": "verification",
            "artifact_hash": verification_hash,
            "document_index": doc_index,
            "document_name": doc_name,
            "response_length": len(content)
        })

        return verification_data

    def _aggregate_composite_results(self, all_results: List[Dict[str, Any]], analysis_id: str) -> Dict[str, Any]:
        """Aggregate composite results from all documents."""
        # For now, return the last result as a placeholder
        # In a full implementation, this would merge all document analyses
        return all_results[-1] if all_results else {}

    def _aggregate_evidence_results(self, all_results: List[Dict[str, Any]], analysis_id: str) -> Dict[str, Any]:
        """Aggregate evidence results from all documents."""
        # For now, return the last result as a placeholder
        return all_results[-1] if all_results else {}

    def _aggregate_scores_results(self, all_results: List[Dict[str, Any]], analysis_id: str) -> Dict[str, Any]:
        """Aggregate score results from all documents."""
        # For now, return the last result as a placeholder
        return all_results[-1] if all_results else {}

    def _aggregate_derived_metrics_results(self, all_results: List[Dict[str, Any]], analysis_id: str) -> Dict[str, Any]:
        """Aggregate derived metrics results from all documents."""
        # For now, return the last result as a placeholder
        return all_results[-1] if all_results else {}

    def _aggregate_verification_results(self, all_results: List[Dict[str, Any]], analysis_id: str) -> Dict[str, Any]:
        """Aggregate verification results from all documents."""
        # For now, return the last result as a placeholder
        return all_results[-1] if all_results else {}

    def _aggregate_markup_results(self, all_results: List[Dict[str, Any]], analysis_id: str) -> Dict[str, Any]:
        """Aggregate markup results from all documents."""
        # For now, return the last result as a placeholder
        return all_results[-1] if all_results else {}

    def _step2_evidence_extraction(self, composite_result: Dict[str, Any], analysis_id: str) -> Dict[str, Any]:
        """Step 2: Extract evidence from composite result using Flash Lite."""
        
        prompt = f"""Extract the evidence section from this analysis result:

{composite_result['raw_analysis_response']}

Return the evidence data in whatever format you think is most useful for the next step."""

        self.audit.log_agent_event(self.agent_name, "step2_started", {
            "analysis_id": analysis_id,
            "step": "evidence_extraction",
            "model": "vertex_ai/gemini-2.5-flash-lite"
        })

        response = self.gateway.execute_call(
            model="vertex_ai/gemini-2.5-flash-lite",
            prompt=prompt
        )
        
        if isinstance(response, tuple):
            content, metadata = response
        else:
            content = response.get('content', '')
            metadata = response.get('metadata', {})
        
        # Save evidence result - no parsing, just store what the LLM produced
        evidence_result = {
            "analysis_id": analysis_id,
            "step": "evidence_extraction",
            "model_used": "vertex_ai/gemini-2.5-flash-lite",
            "evidence_extraction": content,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        evidence_hash = self.storage.put_artifact(
            json.dumps(evidence_result, indent=2).encode('utf-8'),
            {"artifact_type": "evidence_extraction", "analysis_id": analysis_id}
        )
        
        evidence_result['artifact_hash'] = evidence_hash
        
        self.audit.log_agent_event(self.agent_name, "step2_completed", {
            "analysis_id": analysis_id,
            "step": "evidence_extraction",
            "artifact_hash": evidence_hash,
            "response_length": len(content)
        })
        
        return evidence_result

    def _step3_score_extraction(self, composite_result: Dict[str, Any], analysis_id: str) -> Dict[str, Any]:
        """Step 3: Extract scores from composite result using Flash Lite."""
        
        prompt = f"""Extract the dimensional scores from this analysis result:

{composite_result['raw_analysis_response']}

Return the scores data in whatever format you think is most useful for the next step."""

        self.audit.log_agent_event(self.agent_name, "step3_started", {
            "analysis_id": analysis_id,
            "step": "score_extraction",
            "model": "vertex_ai/gemini-2.5-flash-lite"
        })

        response = self.gateway.execute_call(
            model="vertex_ai/gemini-2.5-flash-lite",
            prompt=prompt
        )
        
        if isinstance(response, tuple):
            content, metadata = response
        else:
            content = response.get('content', '')
            metadata = response.get('metadata', {})
        
        # Save scores result - no parsing, just store what the LLM produced
        scores_result = {
            "analysis_id": analysis_id,
            "step": "score_extraction",
            "model_used": "vertex_ai/gemini-2.5-flash-lite",
            "scores_extraction": content,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        scores_hash = self.storage.put_artifact(
            json.dumps(scores_result, indent=2).encode('utf-8'),
            {"artifact_type": "score_extraction", "analysis_id": analysis_id}
        )
        
        scores_result['artifact_hash'] = scores_hash
        
        self.audit.log_agent_event(self.agent_name, "step3_completed", {
            "analysis_id": analysis_id,
            "step": "score_extraction",
            "artifact_hash": scores_hash,
            "response_length": len(content)
        })
        
        return scores_result

    def _step4_derived_metrics_generation(self, 
                                        framework_content: str, 
                                        scores_result: Dict[str, Any], 
                                        analysis_id: str) -> Dict[str, Any]:
        """Step 4: Generate derived metrics using Flash Lite."""
        
        prompt = f"""Based on this framework and the dimensional scores, generate and execute code to calculate derived metrics:

FRAMEWORK:
{framework_content}

SCORES:
{scores_result['scores_extraction']}

Generate Python code to calculate derived metrics and execute it internally. Return both the code and the results."""

        self.audit.log_agent_event(self.agent_name, "step4_started", {
            "analysis_id": analysis_id,
            "step": "derived_metrics_generation",
            "model": "vertex_ai/gemini-2.5-flash-lite"
        })

        response = self.gateway.execute_call(
            model="vertex_ai/gemini-2.5-flash-lite",
            prompt=prompt
        )
        
        if isinstance(response, tuple):
            content, metadata = response
        else:
            content = response.get('content', '')
            metadata = response.get('metadata', {})
        
        # Save derived metrics result - no parsing, just store what the LLM produced
        derived_metrics_result = {
            "analysis_id": analysis_id,
            "step": "derived_metrics_generation",
            "model_used": "vertex_ai/gemini-2.5-flash-lite",
            "derived_metrics": content,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        derived_metrics_hash = self.storage.put_artifact(
            json.dumps(derived_metrics_result, indent=2).encode('utf-8'),
            {"artifact_type": "derived_metrics", "analysis_id": analysis_id}
        )
        
        derived_metrics_result['artifact_hash'] = derived_metrics_hash
        
        self.audit.log_agent_event(self.agent_name, "step4_completed", {
            "analysis_id": analysis_id,
            "step": "derived_metrics_generation",
            "artifact_hash": derived_metrics_hash,
            "response_length": len(content)
        })
        
        return derived_metrics_result

    def _step5_verification(self, 
                          framework_content: str, 
                          derived_metrics_result: Dict[str, Any], 
                          scores_result: Dict[str, Any], 
                          analysis_id: str) -> Dict[str, Any]:
        """Step 5: Verify derived metrics using tool calling."""
        
        # Define verification tool
        verification_tools = [
            {
                "name": "verify_math",
                "description": "Verify that the derived metrics calculations are correct",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "verified": {
                            "type": "boolean",
                            "description": "Whether the mathematical calculations are correct"
                        }
                    },
                    "required": ["verified"]
                }
            }
        ]
        
        prompt = f"""Verify that the derived metrics calculations are correct:

FRAMEWORK:
{framework_content}

SCORES:
{scores_result['scores_extraction']}

DERIVED METRICS:
{derived_metrics_result['derived_metrics']}

Review the calculations and call the verify_math tool with your verification result."""

        self.audit.log_agent_event(self.agent_name, "step5_started", {
            "analysis_id": analysis_id,
            "step": "verification",
            "model": "vertex_ai/gemini-2.5-flash-lite"
        })

        response = self.gateway.execute_call_with_tools(
            model="vertex_ai/gemini-2.5-flash-lite",
            prompt=prompt,
            tools=verification_tools
        )
        
        # Extract verification result
        verification_status = "unknown"
        if hasattr(response, 'choices') and response.choices:
            tool_calls = response.choices[0].message.tool_calls
            if tool_calls:
                for tool_call in tool_calls:
                    if tool_call.function.name == "verify_math":
                        try:
                            args = json.loads(tool_call.function.arguments)
                            verification_status = "verified" if args.get("verified", False) else "verification_error"
                        except json.JSONDecodeError:
                            verification_status = "verification_error"
        
        verification_result = {
            "analysis_id": analysis_id,
            "step": "verification",
            "model_used": "vertex_ai/gemini-2.5-flash-lite",
            "verification_status": verification_status,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        verification_hash = self.storage.put_artifact(
            json.dumps(verification_result, indent=2).encode('utf-8'),
            {"artifact_type": "verification", "analysis_id": analysis_id}
        )
        
        verification_result['artifact_hash'] = verification_hash
        
        self.audit.log_agent_event(self.agent_name, "step5_completed", {
            "analysis_id": analysis_id,
            "step": "verification",
            "artifact_hash": verification_hash,
            "verification_status": verification_status
        })
        
        return verification_result

    def _step6_markup_extraction(self, composite_result: Dict[str, Any], analysis_id: str) -> Dict[str, Any]:
        """Step 6: Extract marked-up document from composite result."""
        
        prompt = f"""Extract the marked-up document from this analysis result and format it as Markdown for human readability:

{composite_result['raw_analysis_response']}

Return the marked-up document in Markdown format with:
1. A clear header (e.g., "# Document Analysis - Marked Up Text")
2. The complete original document text with inline dimensional annotations
3. Use the format: [DIMENSION_NAME: "quoted text from document"]
4. Preserve all original formatting and context
5. Make it readable for human researchers

Format as Markdown, not JSON."""

        self.audit.log_agent_event(self.agent_name, "step6_started", {
            "analysis_id": analysis_id,
            "step": "markup_extraction",
            "model": "vertex_ai/gemini-2.5-flash-lite"
        })

        response = self.gateway.execute_call(
            model="vertex_ai/gemini-2.5-flash-lite",
            prompt=prompt
        )
        
        if isinstance(response, tuple):
            content, metadata = response
        else:
            content = response.get('content', '')
            metadata = response.get('metadata', {})
        
        # Save markup result
        markup_result = {
            "analysis_id": analysis_id,
            "step": "markup_extraction",
            "model_used": "vertex_ai/gemini-2.5-flash-lite",
            "marked_up_document": content,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        markup_hash = self.storage.put_artifact(
            content.encode('utf-8'),
            {"artifact_type": "marked_up_document", "analysis_id": analysis_id, "format": "markdown"}
        )
        
        markup_result['artifact_hash'] = markup_hash
        
        self.audit.log_agent_event(self.agent_name, "step6_completed", {
            "analysis_id": analysis_id,
            "step": "markup_extraction",
            "artifact_hash": markup_hash,
            "response_length": len(content)
        })
        
        return markup_result

    def _prepare_documents(self, documents: List[Dict[str, Any]]) -> str:
        """Prepare documents for the analysis prompt.

        This method now processes documents individually for integrity and scalability.
        Each document gets its own analysis call to prevent concept blending.
        """
        # For individual document processing, we return a placeholder
        # The actual document content is processed individually in the main analysis loop
        return f"Individual document analysis mode: {len(documents)} documents to process"

    def _step7_csv_generation(self, 
                             framework_content: str,
                             all_scores_results: List[Dict[str, Any]], 
                             all_evidence_results: List[Dict[str, Any]], 
                             all_derived_metrics_results: List[Dict[str, Any]], 
                             analysis_id: str) -> Dict[str, Any]:
        """Step 7: Generate CSV files for researchers using the sophisticated StatisticalAgent approach."""
        
        # Define CSV generation tool
        csv_tools = [
            {
                "name": "generate_csv_file",
                "description": "Generate a CSV file with the specified content",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "filename": {
                            "type": "string",
                            "description": "Name of the CSV file (e.g., 'scores.csv')"
                        },
                        "csv_content": {
                            "type": "string",
                            "description": "Complete CSV content with headers and data"
                        }
                    },
                    "required": ["filename", "csv_content"]
                }
            }
        ]
        
        # Discover analysis artifacts for CSV generation (like the old StatisticalAgent)
        analysis_artifacts = self._discover_analysis_artifacts_for_csv(analysis_id)
        
        # Prepare artifact content for CSV generation
        artifacts_content = ""
        for artifact_hash, artifact_data in analysis_artifacts.items():
            artifacts_content += f"\n--- ARTIFACT {artifact_hash} ---\n"
            artifacts_content += json.dumps(artifact_data, indent=2)
        
        prompt = f"""Transform the analysis artifacts into CSV files for researchers:

FRAMEWORK:
{framework_content}

ANALYSIS ARTIFACTS:
{artifacts_content}

Your task is to create comprehensive CSV files for statistical analysis. Follow these steps:

STEP 1: Extract all dimensional scores
- Find all dimensional scores from score_extraction artifacts
- Use the framework content above to identify what dimensions should be present
- Include document_id, document_name, dimension, raw_score, salience, confidence for each score

STEP 2: Extract all derived metrics
- Find all derived metrics from derived_metrics artifacts
- Use the framework content above to identify what derived metrics should be present
- Include document_id, document_name, dimension, raw_score, salience, confidence for each derived metric
- Use the dimension name as the dimension field

STEP 3: Extract all evidence quotes
- Find all evidence quotes from evidence_extraction artifacts
- Include document_id, document_name, dimension, quote_text, confidence for each quote

ANALYSIS ARTIFACTS REFERENCE:
The analysis artifacts include these specific types:
- composite_analysis: Contains the raw analysis results for each document
- score_extraction: Contains dimensional scores
- derived_metrics: Contains calculated metrics
- evidence_extraction: Contains evidence quotes and reasoning for each dimension

STEP 4: Create scores.csv
- Combine ALL dimensional scores AND derived metrics into one CSV
- Required columns: document_id, document_name, dimension, raw_score, salience, confidence
- Ensure every document has entries for both dimensional scores and derived metrics

STEP 5: Create evidence.csv
- Include all evidence quotes with proper attribution
- Required columns: document_id, document_name, dimension, quote_text, confidence

STEP 6: Verify completeness
- Check that scores.csv contains BOTH dimensional scores AND derived metrics
- Verify that data for every document appears in both CSV files
- Ensure all data from the analysis artifacts is included

Use the generate_csv_file tool for each CSV file. Ensure proper CSV formatting with:
- Headers in the first row
- Comma-separated values
- Quoted strings if they contain commas
- Standard format compatible with statistical software"""

        self.audit.log_agent_event(self.agent_name, "step7_started", {
            "analysis_id": analysis_id,
            "step": "csv_generation",
            "model": "vertex_ai/gemini-2.5-flash",
            "documents_count": len(all_scores_results)
        })

        start_time = datetime.now(timezone.utc)
        response_content, response_metadata = self.gateway.execute_call_with_tools(
            model="vertex_ai/gemini-2.5-flash",
            prompt=prompt,
            system_prompt="You are a data processing assistant. You MUST use the generate_csv_file tool to create CSV files from the analysis data. Generate separate CSV files for scores and evidence as instructed.",
            tools=csv_tools,
            force_function_calling=True
        )
        end_time = datetime.now(timezone.utc)
        execution_time = (end_time - start_time).total_seconds()
        
        # Extract cost information
        csv_cost_info = {
            "model": "vertex_ai/gemini-2.5-flash",
            "execution_time_seconds": execution_time,
            "prompt_length": len(prompt),
            "documents_processed": len(all_scores_results),
            "response_cost": response_metadata.get('response_cost', 0.0),
            "input_tokens": response_metadata.get('input_tokens', 0),
            "output_tokens": response_metadata.get('output_tokens', 0),
            "total_tokens": response_metadata.get('total_tokens', 0)
        }
        
        # Parse tool calls to extract CSV files
        csv_files = []
        
        # Debug: Log the response structure
        self.audit.log_agent_event(self.agent_name, "csv_debug_response", {
            "response_type": str(type(response_content)),
            "has_choices": hasattr(response_content, 'choices'),
            "choices_count": len(response_content.choices) if hasattr(response_content, 'choices') else 0
        })
        
        if hasattr(response_content, 'choices'):
            for i, choice in enumerate(response_content.choices):
                choice_info = {
                    "choice_index": i,
                    "choice_type": str(type(choice)),
                    "has_message": hasattr(choice, 'message'),
                    "has_tool_calls": False
                }
                
                if hasattr(choice, 'message'):
                    choice_info["message_type"] = str(type(choice.message))
                    if hasattr(choice.message, 'tool_calls'):
                        choice_info["has_tool_calls"] = True
                        choice_info["tool_calls_count"] = len(choice.message.tool_calls)
                
                self.audit.log_agent_event(self.agent_name, "csv_debug_choice", choice_info)
        
        if hasattr(response_content, 'choices') and response_content.choices:
            for choice in response_content.choices:
                if hasattr(choice, 'message') and hasattr(choice.message, 'tool_calls'):
                    for tool_call in choice.message.tool_calls:
                        if hasattr(tool_call, 'function') and tool_call.function.name == "generate_csv_file":
                            try:
                                args = json.loads(tool_call.function.arguments)
                                filename = args.get('filename')
                                csv_content = args.get('csv_content')
                                
                                if filename and csv_content:
                                    # Write CSV file to results directory
                                    csv_path = self._write_csv_file(filename, csv_content, analysis_id)
                                    csv_files.append({
                                        "filename": filename,
                                        "path": str(csv_path),
                                        "size": len(csv_content)
                                    })
                            except Exception as e:
                                self.audit.log_agent_event(self.agent_name, "csv_tool_call_error", {
                                    "error": str(e),
                                    "tool_call": str(tool_call)
                                })
        
        # Save CSV generation result
        csv_result = {
            "analysis_id": analysis_id,
            "step": "csv_generation",
            "model_used": "vertex_ai/gemini-2.5-flash",
            "csv_files": csv_files,
            "cost_info": csv_cost_info,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        csv_hash = self.storage.put_artifact(
            json.dumps(csv_result, indent=2).encode('utf-8'),
            {"artifact_type": "csv_generation", "analysis_id": analysis_id}
        )
        
        csv_result['artifact_hash'] = csv_hash
        
        self.audit.log_agent_event(self.agent_name, "step7_completed", {
            "analysis_id": analysis_id,
            "step": "csv_generation",
            "csv_files_created": len(csv_files),
            "artifact_hash": csv_hash,
            "execution_time": execution_time
        })
        
        return csv_result

    def _write_csv_file(self, filename: str, csv_content: str, analysis_id: str) -> Path:
        """Write CSV content to the appropriate experiment results directory."""
        
        # Determine output directory - use the current run directory
        experiment_path = Path(self.security.experiment_root)
        runs_dir = experiment_path / "runs"
        
        # Find the most recent run directory (the current one)
        run_dirs = [d for d in runs_dir.iterdir() if d.is_dir()]
        if not run_dirs:
            # Fallback: create a new run directory
            run_id = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
            current_run_dir = runs_dir / run_id
        else:
            # Use the most recent run directory
            current_run_dir = max(run_dirs, key=lambda d: d.stat().st_mtime)
        
        results_dir = current_run_dir / "results"
        
        # Ensure directory exists
        results_dir.mkdir(parents=True, exist_ok=True)
        
        # Write CSV file to results directory
        csv_path = results_dir / filename
        
        with open(csv_path, 'w', encoding='utf-8') as f:
            f.write(csv_content)
        
        self.audit.log_agent_event(self.agent_name, "csv_file_written", {
            "csv_path": str(csv_path),
            "filename": filename,
            "size": len(csv_content),
            "run_directory": str(current_run_dir)
        })
        return csv_path

    def _discover_analysis_artifacts_for_csv(self, analysis_id: str) -> Dict[str, Any]:
        """
        Discover analysis artifacts for CSV generation using the StatisticalAgent approach.
        
        Args:
            analysis_id: Analysis identifier to find artifacts for
            
        Returns:
            Dictionary of artifact_hash -> artifact_data
        """
        artifacts = {}
        
        # Guard: Only attempt if storage registry is properly initialized
        if not hasattr(self.storage, 'registry') or not self.storage.registry:
            self.audit.log_agent_event(self.agent_name, "csv_artifact_discovery_error", {
                "error": "Storage registry not initialized",
                "analysis_id": analysis_id
            })
            return {}
        
        # Find artifacts for this analysis session
        for artifact_hash, artifact_info in self.storage.registry.items():
            metadata = artifact_info.get("metadata", {})
            artifact_type = metadata.get("artifact_type", "")
            artifact_analysis_id = metadata.get("analysis_id", "")
            
            # Include all relevant artifact types for CSV generation
            if (artifact_type in ["composite_analysis", "score_extraction", "derived_metrics", "evidence_extraction"] 
                and artifact_analysis_id == analysis_id):
                try:
                    artifact_content = self.storage.get_artifact(artifact_hash)
                    artifact_data = json.loads(artifact_content.decode('utf-8'))
                    artifacts[artifact_hash] = artifact_data
                except Exception as e:
                    self.audit.log_agent_event(self.agent_name, "csv_artifact_load_error", {
                        "error": str(e),
                        "artifact_hash": artifact_hash,
                        "analysis_id": analysis_id
                    })
                    continue
        
        # Get unique artifact types
        artifact_types = set()
        for artifact_data in artifacts.values():
            if isinstance(artifact_data, dict):
                artifact_types.add(artifact_data.get("step", "unknown"))
            else:
                artifact_types.add("unknown")
        
        self.audit.log_agent_event(self.agent_name, "csv_artifact_discovery", {
            "analysis_id": analysis_id,
            "artifacts_found": len(artifacts),
            "artifact_types": list(artifact_types)
        })
        
        return artifacts

    def _prepare_single_document(self, doc: Dict[str, Any], doc_index: int) -> str:
        """Prepare a single document for individual analysis."""
        doc_content = doc.get('content', '')
        doc_name = doc.get('id', doc.get('name', doc.get('filename', f'document_{doc_index}')))
        doc_hash = self._generate_content_hash(doc_content)
            
        document_content = f"--- Document {doc_index+1}: {doc_name} ---\n"
        document_content += f"Hash: {doc_hash}\n"
        document_content += f"Content:\n{doc_content}\n"
        
        return document_content

    def _generate_analysis_id(self) -> str:
        """Generate a unique analysis ID."""
        timestamp = datetime.now(timezone.utc).isoformat()
        return f"analysis_{hashlib.md5(timestamp.encode()).hexdigest()[:8]}"

    def _generate_content_hash(self, content: str) -> str:
        """Generate a content hash for the given content."""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()[:16]
