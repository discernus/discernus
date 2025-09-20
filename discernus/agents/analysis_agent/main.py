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
        """Load the framework-agnostic prompt template."""
        return """You are an expert discourse analyst specializing in systematic content analysis using provided frameworks.

ANALYSIS TASK:
Perform a comprehensive analysis of the provided document(s) using the specified framework. Your analysis must include:

1. **Dimensional Scoring**: Score each framework dimension on a 0-1 scale for:
   - raw_score: Presence/strength of the dimension
   - salience: Emphasis/importance in the discourse
   - confidence: Your confidence in the assessment

2. **Evidence Collection**: Provide 1-2 high-quality quotes per dimension that best exemplify the scoring.

3. **Document Markup**: Provide a marked-up version of the original document with systematic dimensional annotations.

INTERNAL CONSISTENCY APPROACH:
Perform three independent analytical approaches:
- Evidence-First: Start with quotes, then score
- Context-Weighted: Consider broader context and framing
- Pattern-Based: Look for rhetorical patterns and structures

Then aggregate using median for scores and select the most representative evidence.

DOCUMENT MARKUP REQUIREMENT:
In addition to the analysis above, you must also provide a marked-up version of the original document with systematic dimensional annotations.

For the marked_up_document field, you must:
1. Include the COMPLETE original document text
2. Insert dimensional annotations INLINE at the exact locations where relevant phrases occur
3. Use this format: [DIMENSION_NAME: "quoted text from document"]
4. Mark ALL text relevant to each dimension, not just the evidence quotes
5. Preserve the full context and flow of the original document
6. Format the output in MARKDOWN for human readability

This creates a comprehensive markup showing your complete reasoning for each dimensional score, allowing researchers to see exactly how you interpreted the document without losing any context.

Example of inline markup in Markdown:
```markdown
# Document Analysis - Marked Up Text

My fellow Americans, three years ago, we launched the Great American Comeback. Tonight, I stand before you to share the incredible results. [HOMOGENEOUS_PEOPLE_CONSTRUCTION: Jobs are booming, incomes are soaring, poverty is plummeting, crime is falling, confidence is surging, and our country is thriving and highly respected again!] [POPULAR_SOVEREIGNTY_CLAIMS: The agenda I will lay out this evening is not a Republican agenda or a Democrat agenda. It's the agenda of the American people.] [CRISIS_RESTORATION_NARRATIVE: This year, America will recognize two important anniversaries that show us the majesty of America's mission and the power of American pride.]
```

Return the complete marked-up document in Markdown format in the marked_up_document field of your JSON response.

OUTPUT FORMAT:
Return your complete analysis in this exact JSON structure:

{
  "analysis_metadata": {
    "framework_name": "FRAMEWORK_NAME",
    "framework_version": "FRAMEWORK_VERSION",
    "analyst_confidence": 0.95,
    "analysis_notes": "Applied three independent analytical approaches with median aggregation",
    "internal_consistency_approach": "3-run median aggregation"
  },
  "document_analyses": [
    {
      "document_id": "DOCUMENT_ID_PLACEHOLDER",
      "document_name": "DOCUMENT_NAME",
      "dimensional_scores": {
        "DIMENSION_1": {
          "raw_score": 0.8,
          "salience": 0.7,
          "confidence": 0.9
        }
      },
      "evidence_quotes": {
        "DIMENSION_1": [
          "Quote 1 that exemplifies this dimension",
          "Quote 2 that exemplifies this dimension"
        ]
      },
      "marked_up_document": "# Document Analysis - Marked Up Text\\n\\n[Complete document with inline annotations]"
    }
  ]
}

FRAMEWORK:
{framework_content}

DOCUMENTS:
{document_content}

Analyze the provided document(s) using the specified framework and return the complete analysis in the exact JSON format above."""

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
                doc_name = doc.get('name', doc.get('filename', f'document_{doc_index}'))
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
            
            # Compile final results
            final_results = {
                "composite_analysis": composite_result,
                "evidence_extraction": evidence_result,
                "score_extraction": scores_result,
                "derived_metrics": derived_metrics_result,
                "verification": verification_result,
                "markup_extraction": markup_result,
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

    def _prepare_single_document(self, doc: Dict[str, Any], doc_index: int) -> str:
        """Prepare a single document for individual analysis."""
        doc_content = doc.get('content', '')
        doc_name = doc.get('name', doc.get('filename', f'document_{doc_index}'))
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
