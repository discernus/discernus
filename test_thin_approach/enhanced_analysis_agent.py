#!/usr/bin/env python3
"""
Enhanced Analysis Agent with Integrated Document Markup
======================================================

Extends the THIN 5-step approach to include document markup in the composite analysis step,
then extracts the markup as a separate provenance artifact.
"""

import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List

from discernus.core.security_boundary import ExperimentSecurityBoundary
from discernus.core.audit_logger import AuditLogger
from discernus.core.local_artifact_storage import LocalArtifactStorage
from discernus.gateway.llm_gateway_enhanced import EnhancedLLMGateway
from tmp.AnalysisAgent.prompt_builder import create_analysis_prompt


class EnhancedAnalysisAgent:
    """Enhanced analysis agent with integrated document markup capability."""

    def __init__(self,
                 security_boundary: ExperimentSecurityBoundary,
                 audit_logger: AuditLogger,
                 artifact_storage: LocalArtifactStorage):
        self.security = security_boundary
        self.audit = audit_logger
        self.storage = artifact_storage
        self.agent_name = "EnhancedAnalysisAgent"
        self.gateway = EnhancedLLMGateway(self.audit)
        self.prompt_template = self._load_prompt_template()

        self.audit.log_agent_event(self.agent_name, "initialization", {
            "security_boundary": self.security.get_boundary_info(),
            "capabilities": ["composite_analysis_with_markup", "evidence_extraction", "score_extraction", "derived_metrics", "verification", "markup_extraction"]
        })

    def _load_original_prompt_template(self) -> str:
        """Load the original prompt template from the AnalysisAgent."""
        # This should match the original prompt template from tmp/AnalysisAgent/prompt_3run.yaml
        return """You are an expert political discourse analyst specializing in populist rhetoric analysis using the Populist Discourse Analysis Framework (PDAF) v10.0.2.

ANALYSIS TASK:
Perform a comprehensive analysis of the provided document(s) using the PDAF framework. Your analysis must include:

1. **Dimensional Scoring**: Score each of the 9 PDAF dimensions on a 0-1 scale for:
   - raw_score: Presence/strength of the dimension
   - salience: Emphasis/importance in the discourse
   - confidence: Your confidence in the assessment

2. **Evidence Collection**: Provide 1-2 high-quality quotes per dimension that best exemplify the scoring.

INTERNAL CONSISTENCY APPROACH:
Perform three independent analytical approaches:
- Evidence-First: Start with quotes, then score
- Context-Weighted: Consider broader context and framing
- Pattern-Based: Look for rhetorical patterns and structures

Then aggregate using median for scores and select the most representative evidence.

OUTPUT FORMAT:
Return your complete analysis in this exact JSON structure:

{
  "analysis_metadata": {
    "framework_name": "populist_discourse_analysis_framework",
    "framework_version": "10.0.2",
    "analyst_confidence": 0.95,
    "analysis_notes": "Applied three independent analytical approaches with median aggregation",
    "internal_consistency_approach": "3-run median aggregation"
  },
  "document_analyses": [
    {
      "document_id": "DOCUMENT_ID_PLACEHOLDER",
      "document_name": "DOCUMENT_NAME",
      "dimensional_scores": {
        "manichaean_people_elite_framing": {
          "raw_score": 0.8,
          "salience": 0.7,
          "confidence": 0.9
        },
        "crisis_restoration_narrative": {
          "raw_score": 0.9,
          "salience": 0.8,
          "confidence": 0.9
        },
        "popular_sovereignty_claims": {
          "raw_score": 0.7,
          "salience": 0.6,
          "confidence": 0.8
        },
        "anti_pluralist_exclusion": {
          "raw_score": 0.7,
          "salience": 0.6,
          "confidence": 0.8
        },
        "elite_conspiracy_systemic_corruption": {
          "raw_score": 0.6,
          "salience": 0.5,
          "confidence": 0.8
        },
        "authenticity_vs_political_class": {
          "raw_score": 0.8,
          "salience": 0.7,
          "confidence": 0.9
        },
        "homogeneous_people_construction": {
          "raw_score": 0.8,
          "salience": 0.7,
          "confidence": 0.9
        },
        "nationalist_exclusion": {
          "raw_score": 0.7,
          "salience": 0.6,
          "confidence": 0.8
        },
        "economic_populist_appeals": {
          "raw_score": 0.9,
          "salience": 0.8,
          "confidence": 0.9
        }
      },
      "evidence": [
        {
          "dimension": "manichaean_people_elite_framing",
          "quote_text": "Exact quote from document",
          "confidence": 0.9,
          "context_type": "direct_statement"
        }
      ]
    }
  ]
}

CRITICAL REQUIREMENTS:
- Use exact dimension names from the framework
- Ensure all 9 dimensions are scored
- Provide high-quality evidence quotes
- Maintain academic rigor and transparency"""

    def _load_prompt_template(self) -> str:
        """Load the enhanced prompt template with markup instructions."""
        return """You are an expert political discourse analyst specializing in populist rhetoric analysis using the Populist Discourse Analysis Framework (PDAF) v10.0.2.

ANALYSIS TASK:
Perform a comprehensive analysis of the provided document(s) using the PDAF framework. Your analysis must include:

1. **Dimensional Scoring**: Score each of the 9 PDAF dimensions on a 0-1 scale for:
   - raw_score: Presence/strength of the dimension
   - salience: Emphasis/importance in the discourse
   - confidence: Your confidence in the assessment

2. **Evidence Collection**: Provide 1-2 high-quality quotes per dimension that best exemplify the scoring.

3. **Document Markup**: Systematically annotate the original document with dimensional markers using this format:
   [DIMENSION_NAME: "quoted text from document"]
   
   Mark ALL text relevant to each dimension, not just the evidence quotes. This creates a comprehensive markup showing your complete reasoning.

INTERNAL CONSISTENCY APPROACH:
Perform three independent analytical approaches:
- Evidence-First: Start with quotes, then score
- Context-Weighted: Consider broader context and framing
- Pattern-Based: Look for rhetorical patterns and structures

Then aggregate using median for scores and select the most representative evidence.

OUTPUT FORMAT:
Return your complete analysis in this exact JSON structure:

{
  "analysis_metadata": {
    "framework_name": "populist_discourse_analysis_framework",
    "framework_version": "10.0.2",
    "analyst_confidence": 0.95,
    "analysis_notes": "Applied three independent analytical approaches with median aggregation and comprehensive document markup",
    "internal_consistency_approach": "3-run median aggregation with markup"
  },
  "document_analyses": [
    {
      "document_id": "DOCUMENT_ID_PLACEHOLDER",
      "document_name": "DOCUMENT_NAME",
      "dimensional_scores": {
        "manichaean_people_elite_framing": {
          "raw_score": 0.8,
          "salience": 0.7,
          "confidence": 0.9
        },
        "crisis_restoration_narrative": {
          "raw_score": 0.9,
          "salience": 0.8,
          "confidence": 0.9
        },
        "popular_sovereignty_claims": {
          "raw_score": 0.7,
          "salience": 0.6,
          "confidence": 0.8
        },
        "anti_pluralist_exclusion": {
          "raw_score": 0.7,
          "salience": 0.6,
          "confidence": 0.8
        },
        "elite_conspiracy_systemic_corruption": {
          "raw_score": 0.6,
          "salience": 0.5,
          "confidence": 0.8
        },
        "authenticity_vs_political_class": {
          "raw_score": 0.8,
          "salience": 0.7,
          "confidence": 0.9
        },
        "homogeneous_people_construction": {
          "raw_score": 0.8,
          "salience": 0.7,
          "confidence": 0.9
        },
        "nationalist_exclusion": {
          "raw_score": 0.7,
          "salience": 0.6,
          "confidence": 0.8
        },
        "economic_populist_appeals": {
          "raw_score": 0.9,
          "salience": 0.8,
          "confidence": 0.9
        }
      },
      "evidence": [
        {
          "dimension": "manichaean_people_elite_framing",
          "quote_text": "Exact quote from document",
          "confidence": 0.9,
          "context_type": "direct_statement"
        }
      ],
      "marked_up_document": "The complete original document with systematic dimensional markup using [DIMENSION_NAME: \"quoted text\"] format throughout"
    }
  ]
}

CRITICAL REQUIREMENTS:
- Mark up ALL relevant text, not just evidence quotes
- Use exact dimension names from the framework
- Ensure markup covers the complete reasoning for each score
- Maintain academic rigor and transparency
- Provide comprehensive provenance for all assessments"""

    def run_enhanced_analysis(self, framework_content: str, corpus_documents: List[Dict[str, Any]], 
                             experiment_config: Dict[str, Any], model: str = "vertex_ai/gemini-2.5-flash") -> Dict[str, Any]:
        """Run the enhanced 6-step analysis with integrated markup."""
        
        analysis_id = f"enhanced_analysis_{hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8]}"
        
        print("=== Enhanced Analysis Agent ===")
        print("6-Step THIN Approach with Integrated Markup:")
        print("1. Enhanced Composite Analysis with Markup (Flash)")
        print("2. Evidence Extraction (Flash Lite)")
        print("3. Score Extraction (Flash Lite)")
        print("4. Derived Metrics Generation (Flash Lite)")
        print("5. Verification (Flash Lite)")
        print("6. Markup Extraction (Flash Lite)")
        print()
        
        results = {}
        
        # Step 1: Enhanced Composite Analysis with Markup (Flash)
        print("Step 1: Enhanced Composite Analysis with Markup using Flash...")
        composite_result = self._step1_enhanced_composite_analysis(
            framework_content, corpus_documents, experiment_config, model, analysis_id
        )
        results['composite_analysis'] = composite_result
        
        # Step 2: Evidence Extraction (Flash Lite)
        print("Step 2: Evidence Extraction with Flash Lite...")
        evidence_result = self._step2_evidence_extraction(composite_result, analysis_id)
        results['evidence_extraction'] = evidence_result
        
        # Step 3: Score Extraction (Flash Lite)
        print("Step 3: Score Extraction with Flash Lite...")
        scores_result = self._step3_score_extraction(composite_result, analysis_id)
        results['score_extraction'] = scores_result
        
        # Step 4: Derived Metrics Generation (Flash Lite)
        print("Step 4: Derived Metrics Generation with Flash Lite...")
        metrics_result = self._step4_derived_metrics_generation(
            framework_content, scores_result, analysis_id
        )
        results['derived_metrics'] = metrics_result
        
        # Step 5: Verification (Flash Lite)
        print("Step 5: Verification with Flash Lite...")
        verification_result = self._step5_verification(
            framework_content, scores_result, metrics_result, analysis_id
        )
        results['verification'] = verification_result
        
        # Step 6: Markup Extraction (Flash Lite)
        print("Step 6: Markup Extraction with Flash Lite...")
        markup_result = self._step6_markup_extraction(composite_result, analysis_id)
        results['markup_extraction'] = markup_result
        
        # Save complete results
        results['analysis_metadata'] = {
            'analysis_id': analysis_id,
            'start_time': composite_result['timestamp'],
            'end_time': datetime.now(timezone.utc).isoformat(),
            'agent_name': self.agent_name
        }
        
        # Calculate result hash
        result_content = json.dumps(results, indent=2, sort_keys=True)
        result_hash = hashlib.sha256(result_content.encode()).hexdigest()
        results['result_hash'] = result_hash
        
        return results

    def _step1_enhanced_composite_analysis(self, framework_content: str, corpus_documents: List[Dict[str, Any]], 
                                          experiment_config: Dict[str, Any], model: str, analysis_id: str) -> Dict[str, Any]:
        """Step 1: Enhanced composite analysis with integrated document markup using Flash."""
        
        # Prepare documents
        documents, document_hashes = self._prepare_documents(corpus_documents, analysis_id)
        
        # Create enhanced prompt with markup instructions
        # Use the original prompt template but add markup instructions
        original_prompt_template = self._load_original_prompt_template()
        prompt_text = create_analysis_prompt(original_prompt_template, analysis_id, framework_content, documents)
        
        # Add markup instructions to the prompt
        markup_instructions = """

IMPORTANT: In addition to the analysis above, you must also provide a marked-up version of the original document with systematic dimensional annotations.

For the marked_up_document field, systematically annotate the original document text with dimensional markers using this format:
[DIMENSION_NAME: "quoted text from document"]

Mark ALL text relevant to each dimension, not just the evidence quotes. This creates a comprehensive markup showing your complete reasoning for each dimensional score.

Example:
[MANICHAEAN_PEOPLE_ELITE: "No issue better illustrates the divide between America's working class and America's political class than illegal immigration."]

[CRISIS_RESTORATION: "Over the last 2 years, my administration has moved with urgency and historic speed to confront problems neglected by leaders of both parties over many decades."]

Include the complete marked-up document in the marked_up_document field of your JSON response."""
        
        prompt_text += markup_instructions
        
        # Execute LLM call
        response = self.gateway.execute_call(
            model=model,
            prompt=prompt_text
        )
        
        # Handle response - get the actual content
        if isinstance(response, tuple):
            content, metadata = response
        else:
            content = response.get('content', '')
            metadata = response.get('metadata', {})
        
        # If content is empty, try to get it from the raw response
        if not content and hasattr(response, 'choices'):
            content = response.choices[0].message.content
        
        # Save composite result to artifacts
        composite_data = {
            "analysis_id": analysis_id,
            "step": "enhanced_composite_analysis_generation",
            "model_used": model,
            "raw_analysis_response": content,
            "document_hashes": document_hashes,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        composite_hash = self.storage.put_artifact(
            json.dumps(composite_data, indent=2).encode('utf-8'),
            {"artifact_type": "enhanced_composite_analysis", "analysis_id": analysis_id}
        )
        
        composite_data['artifact_hash'] = composite_hash
        return composite_data

    def _step2_evidence_extraction(self, composite_result: Dict[str, Any], analysis_id: str) -> Dict[str, Any]:
        """Step 2: Extract evidence from composite result using Flash Lite."""
        
        prompt = f"""Extract the evidence section from this analysis result:

{composite_result['raw_analysis_response']}

Return the evidence data in whatever format you think is most useful for the next step."""

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
        return evidence_result

    def _step3_score_extraction(self, composite_result: Dict[str, Any], analysis_id: str) -> Dict[str, Any]:
        """Step 3: Extract scores from composite result using Flash Lite."""
        
        prompt = f"""Extract the dimensional scores from this analysis result:

{composite_result['raw_analysis_response']}

Return the scores data in whatever format you think is most useful for calculating derived metrics."""

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
        return scores_result

    def _step4_derived_metrics_generation(self, framework_content: str, scores_result: Dict[str, Any], analysis_id: str) -> Dict[str, Any]:
        """Step 4: Generate derived metrics using Flash Lite."""
        
        prompt = f"""Calculate derived metrics for this populist discourse analysis.

FRAMEWORK:
{framework_content[:2000]}...

DIMENSIONAL SCORES:
{scores_result['scores_extraction']}

Calculate the derived metrics and return whatever format you think is most useful for verification."""

        response = self.gateway.execute_call(
            model="vertex_ai/gemini-2.5-flash-lite",
            prompt=prompt
        )
        
        if isinstance(response, tuple):
            content, metadata = response
        else:
            content = response.get('content', '')
            metadata = response.get('metadata', {})
        
        # Save metrics result - no parsing, just store what the LLM produced
        metrics_result = {
            "analysis_id": analysis_id,
            "step": "derived_metrics_generation",
            "model_used": "vertex_ai/gemini-2.5-flash-lite",
            "derived_metrics": content,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        metrics_hash = self.storage.put_artifact(
            json.dumps(metrics_result, indent=2).encode('utf-8'),
            {"artifact_type": "derived_metrics", "analysis_id": analysis_id}
        )
        
        metrics_result['artifact_hash'] = metrics_hash
        return metrics_result

    def _step5_verification(self, framework_content: str, scores_result: Dict[str, Any], metrics_result: Dict[str, Any], analysis_id: str) -> Dict[str, Any]:
        """Step 5: Verify derived metrics calculation using Flash Lite with tool calling."""
        
        # Define verification tool schema
        verification_tools = [
            {
                "name": "return_verification_result",
                "description": "Return the verification result (thumbs up or thumbs down)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "verified": {
                            "type": "boolean",
                            "description": "True if the math is correct, False if not"
                        }
                    },
                    "required": ["verified"]
                }
            }
        ]
        
        prompt = f"""Verify the math in this derived metrics calculation.

DIMENSIONAL SCORES:
{scores_result['scores_extraction']}

DERIVED METRICS:
{metrics_result['derived_metrics']}

Do the math internally - recalculate the derived metrics using the dimensional scores and compare with the provided results. Then use the return_verification_result tool to return true if the math is correct, false if not."""

        response = self.gateway.execute_call_with_tools(
            model="vertex_ai/gemini-2.5-flash-lite",
            prompt=prompt,
            tools=verification_tools
        )
        
        if isinstance(response, tuple):
            content, metadata = response
        else:
            content = response.get('content', '')
            metadata = response.get('metadata', {})
        
        # Extract tool call result
        verified = False  # Default
        
        if metadata.get('tool_calls') and len(metadata['tool_calls']) > 0:
            tool_call = metadata['tool_calls'][0]
            if tool_call.get('function', {}).get('name') == 'return_verification_result':
                try:
                    args = json.loads(tool_call['function']['arguments'])
                    verified = args.get('verified', False)
                except:
                    verified = False
        
        # Save verification result
        verification_result = {
            "analysis_id": analysis_id,
            "step": "verification",
            "model_used": "vertex_ai/gemini-2.5-flash-lite",
            "verified": verified,
            "raw_response": content,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        verification_hash = self.storage.put_artifact(
            json.dumps(verification_result, indent=2).encode('utf-8'),
            {"artifact_type": "verification", "analysis_id": analysis_id}
        )
        
        verification_result['artifact_hash'] = verification_hash
        return verification_result

    def _step6_markup_extraction(self, composite_result: Dict[str, Any], analysis_id: str) -> Dict[str, Any]:
        """Step 6: Extract marked-up document from composite result using Flash Lite."""
        
        prompt = f"""Extract the marked-up document from this analysis result:

{composite_result['raw_analysis_response']}

Return the marked-up document with dimensional annotations in whatever format you think is most useful for provenance and verification."""

        response = self.gateway.execute_call(
            model="vertex_ai/gemini-2.5-flash-lite",
            prompt=prompt
        )
        
        if isinstance(response, tuple):
            content, metadata = response
        else:
            content = response.get('content', '')
            metadata = response.get('metadata', {})
        
        # Save markup result - no parsing, just store what the LLM produced
        markup_result = {
            "analysis_id": analysis_id,
            "step": "markup_extraction",
            "model_used": "vertex_ai/gemini-2.5-flash-lite",
            "marked_up_document": content,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        markup_hash = self.storage.put_artifact(
            json.dumps(markup_result, indent=2).encode('utf-8'),
            {"artifact_type": "markup_extraction", "analysis_id": analysis_id}
        )
        
        markup_result['artifact_hash'] = markup_hash
        return markup_result

    def _prepare_documents(self, corpus_documents: List[Dict[str, Any]], analysis_id: str) -> tuple[List[Dict[str, Any]], List[str]]:
        """Prepares documents for analysis and returns them along with their hashes."""
        documents, document_hashes = [], []
        for i, doc in enumerate(corpus_documents):
            doc_content = doc.get('content', '')
            doc_hash = hashlib.sha256(doc_content.encode()).hexdigest()
            document_hashes.append(doc_hash)
            
            documents.append({
                'index': i,
                'filename': doc.get('name', f'document_{i}'),
                'hash': doc_hash,
                'content': doc_content
            })
        
        return documents, document_hashes
