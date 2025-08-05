#!/usr/bin/env python3
"""
LLM Analyzer - THIN Component
=============================

Handles LLM interaction for analysis.
This component contains the LLM intelligence.
"""

from datetime import datetime, timezone
from typing import Dict, Any, List
from litellm import completion

from .framework_parser import FrameworkConfig
from .document_processor import ProcessedDocument


class LLMAnalyzer:
    """
    Handles LLM interaction for document analysis.
    
    THIN Principle: This component contains the LLM intelligence.
    The orchestrator delegates LLM calls to this specialized component.
    """
    
    def __init__(self, prompt_template: str):
        self.prompt_template = prompt_template
    
    def analyze_documents(self, framework_config: FrameworkConfig, 
                         processed_docs: List[ProcessedDocument],
                         model: str, batch_id: str) -> Dict[str, Any]:
        """
        Perform LLM analysis of documents using framework.
        
        Args:
            framework_config: Parsed framework configuration
            processed_docs: List of processed documents
            model: LLM model to use
            batch_id: Batch identifier for tracking
            
        Returns:
            Analysis result with LLM response and metadata
        """
        start_time = datetime.now(timezone.utc)
        
        # Format documents for prompt
        formatted_docs = self._format_documents_for_prompt(processed_docs)
        
        # Build analysis prompt
        prompt = self._build_analysis_prompt(framework_config, formatted_docs)
        
        # Call LLM with safety settings for political content
        try:
            response = completion(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                safety_settings=[
                    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
                ] if model.startswith("vertex_ai") else None
            )
            
            if not response or not response.choices:
                raise Exception("LLM returned empty response")
            
            result_content = response.choices[0].message.content
            if not result_content or result_content.strip() == "":
                raise Exception("LLM returned empty content")
            
            end_time = datetime.now(timezone.utc)
            duration = (end_time - start_time).total_seconds()
            
            return {
                "batch_id": batch_id,
                "raw_analysis_response": result_content,
                "duration_seconds": duration,
                "mathematical_validation": True,
                "model_used": model,
                "prompt_length": len(prompt),
                "response_length": len(result_content)
            }
            
        except Exception as e:
            raise Exception(f"LLM analysis failed: {str(e)}")
    
    def _format_documents_for_prompt(self, documents: List[ProcessedDocument]) -> str:
        """Format processed documents for LLM prompt."""
        if not documents:
            return "No documents provided."
        
        formatted_docs = []
        for i, doc in enumerate(documents):
            formatted_docs.append(f"Document {i+1} ({doc.filename}):\n{doc.content}")
        
        return "\n\n".join(formatted_docs)
    
    def _build_analysis_prompt(self, framework_config: FrameworkConfig, 
                              formatted_docs: str) -> str:
        """Build the complete analysis prompt for the LLM using framework-defined analysis_prompt."""
        
        # v7.3: Use framework-defined analysis_prompt if available
        analysis_variants = framework_config.raw_config.get("analysis_variants", {})
        default_variant = analysis_variants.get("default", {})
        framework_prompt = default_variant.get("analysis_prompt", "")
        
        if framework_prompt:
            # Use the framework's custom analysis prompt
            return f"""
{framework_prompt}

Documents to analyze:
{formatted_docs}

CRITICAL: Your response MUST include the embedded CSV sections with exact delimiters:
```
<<<DISCERNUS_SCORES_CSV_v1>>>
aid,[framework-defined score columns]
{{artifact_id}},[framework-specific scores]
<<<END_DISCERNUS_SCORES_CSV_v1>>>

<<<DISCERNUS_EVIDENCE_CSV_v1>>>
aid,dimension,[framework-defined evidence columns]
{{artifact_id}},{{dimension_name}},[framework-specific evidence data]
<<<END_DISCERNUS_EVIDENCE_CSV_v1>>>
```
"""
        else:
            # Fallback to generic prompt for legacy frameworks
            dimensions_text = ", ".join(framework_config.dimensions)
            return f"""
        Analyze the following documents using the framework dimensions: {dimensions_text}
        
        Documents:
        {formatted_docs}
        
        Provide analysis with embedded CSV output using the standard Discernus delimiters.
        """