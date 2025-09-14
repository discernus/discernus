#!/usr/bin/env python3
"""
Extended Analysis Agent for Show Your Work Architecture

Implements 5-step THIN approach:
1. Composite Analysis Generation (Flash) - Original 3-shot median aggregation
2. Evidence Extraction (Flash Lite) - Extract evidence from composite result
3. Score Extraction (Flash Lite) - Extract scores from composite result  
4. Derived Metrics Generation (Flash Lite) - Calculate derived metrics from scores
5. Verification (Flash Lite) - Verify derived metrics calculation
"""

import json
import base64
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional

from discernus.core.security_boundary import ExperimentSecurityBoundary
from discernus.core.audit_logger import AuditLogger
from discernus.core.local_artifact_storage import LocalArtifactStorage
from discernus.gateway.llm_gateway_enhanced import EnhancedLLMGateway
from discernus.gateway.model_registry import ModelRegistry

from .cache import AnalysisCache
from .prompt_builder import create_analysis_prompt


class ExtendedAnalysisAgent:
    """Extended analysis agent implementing Show Your Work architecture."""

    def __init__(self,
                 security_boundary: ExperimentSecurityBoundary,
                 audit_logger: AuditLogger,
                 artifact_storage: LocalArtifactStorage):
        self.security = security_boundary
        self.audit = audit_logger
        self.storage = artifact_storage
        self.agent_name = "ExtendedAnalysisAgent"
        self.gateway = EnhancedLLMGateway(ModelRegistry())
        
        # Load the original 3-shot prompt template
        self.prompt_template = self._load_prompt_template()
        self.cache = AnalysisCache(self.storage, self.audit, self.agent_name)

        self.audit.log_agent_event(self.agent_name, "initialization", {
            "security_boundary": self.security.get_boundary_info(),
            "capabilities": ["composite_analysis", "evidence_extraction", "score_extraction", "derived_metrics", "verification"]
        })

    def _load_prompt_template(self) -> str:
        """Load the original 3-shot prompt template."""
        prompt_path = Path(__file__).parent / "prompt.txt"
        if not prompt_path.exists():
            raise FileNotFoundError("Could not find prompt.txt for ExtendedAnalysisAgent")
        with open(prompt_path, 'r') as f:
            return f.read()

    def analyze_documents_extended(self,
                                 framework_content: str,
                                 corpus_documents: List[Dict[str, Any]],
                                 experiment_config: Dict[str, Any],
                                 model: str = "vertex_ai/gemini-2.5-flash") -> Dict[str, Any]:
        """Performs extended 5-step analysis."""
        
        start_time = datetime.now(timezone.utc).isoformat()
        analysis_id = f"extended_analysis_{hashlib.sha256(f'{framework_content}{len(corpus_documents)}{model}'.encode()).hexdigest()[:12]}"
        
        self.audit.log_agent_event(self.agent_name, "extended_analysis_start", {
            "analysis_id": analysis_id, "num_documents": len(corpus_documents), "model": model
        })

        results = {}
        
        # Step 1: Composite Analysis Generation (Flash)
        print("Step 1: Composite Analysis Generation with Flash...")
        composite_result = self._step1_composite_analysis(
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
        
        # Save complete results
        results['analysis_metadata'] = {
            'analysis_id': analysis_id,
            'start_time': start_time,
            'end_time': datetime.now(timezone.utc).isoformat(),
            'agent_name': self.agent_name
        }
        
        # Save to artifacts
        result_hash = self.storage.put_artifact(
            json.dumps(results, indent=2).encode('utf-8'),
            {"artifact_type": "extended_analysis_result", "analysis_id": analysis_id}
        )
        results['result_hash'] = result_hash
        
        return results

    def _step1_composite_analysis(self, framework_content: str, corpus_documents: List[Dict[str, Any]], 
                                 experiment_config: Dict[str, Any], model: str, analysis_id: str) -> Dict[str, Any]:
        """Step 1: Original 3-shot median aggregation analysis using Flash."""
        
        # Prepare documents
        documents, document_hashes = self._prepare_documents(corpus_documents, analysis_id)
        
        # Create prompt using original 3-shot approach
        prompt_text = create_analysis_prompt(self.prompt_template, analysis_id, framework_content, documents)
        
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
            "step": "composite_analysis_generation",
            "model_used": model,
            "raw_analysis_response": content,
            "document_hashes": document_hashes,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        composite_hash = self.storage.put_artifact(
            json.dumps(composite_data, indent=2).encode('utf-8'),
            {"artifact_type": "composite_analysis", "analysis_id": analysis_id}
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
                    import json
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

    def _extract_derived_metrics_from_framework(self, framework_content: str) -> List[Dict[str, Any]]:
        """Extract derived metrics definitions from framework content."""
        # This is a simplified extraction - in practice you'd parse the YAML properly
        derived_metrics = [
            {
                "name": "democratic_authoritarian_tension",
                "description": "Tension between democratic and authoritarian appeals",
                "formula": "min(dimensions.popular_sovereignty_claims.raw_score, dimensions.anti_pluralist_exclusion.raw_score) * abs(dimensions.popular_sovereignty_claims.salience - dimensions.anti_pluralist_exclusion.salience)"
            },
            {
                "name": "internal_external_focus_tension", 
                "description": "Tension between internal and external focus",
                "formula": "min(dimensions.homogeneous_people_construction.raw_score, dimensions.nationalist_exclusion.raw_score) * abs(dimensions.homogeneous_people_construction.salience - dimensions.nationalist_exclusion.salience)"
            },
            {
                "name": "crisis_elite_attribution_tension",
                "description": "Tension between crisis and elite attribution",
                "formula": "min(dimensions.crisis_restoration_narrative.raw_score, dimensions.elite_conspiracy_systemic_corruption.raw_score) * abs(dimensions.crisis_restoration_narrative.salience - dimensions.elite_conspiracy_systemic_corruption.salience)"
            },
            {
                "name": "populist_strategic_contradiction_index",
                "description": "Overall strategic contradiction measure",
                "formula": "(democratic_authoritarian_tension + internal_external_focus_tension + crisis_elite_attribution_tension) / 3"
            },
            {
                "name": "salience_weighted_core_populism_index",
                "description": "Core populism dimensions weighted by salience",
                "formula": "(dimensions.manichaean_people_elite_framing.raw_score * dimensions.manichaean_people_elite_framing.salience + dimensions.crisis_restoration_narrative.raw_score * dimensions.crisis_restoration_narrative.salience + dimensions.popular_sovereignty_claims.raw_score * dimensions.popular_sovereignty_claims.salience + dimensions.anti_pluralist_exclusion.raw_score * dimensions.anti_pluralist_exclusion.salience) / (dimensions.manichaean_people_elite_framing.salience + dimensions.crisis_restoration_narrative.salience + dimensions.popular_sovereignty_claims.salience + dimensions.anti_pluralist_exclusion.salience + 0.001)"
            },
            {
                "name": "salience_weighted_populism_mechanisms_index",
                "description": "Populism mechanisms weighted by salience",
                "formula": "(dimensions.elite_conspiracy_systemic_corruption.raw_score * dimensions.elite_conspiracy_systemic_corruption.salience + dimensions.authenticity_vs_political_class.raw_score * dimensions.authenticity_vs_political_class.salience + dimensions.homogeneous_people_construction.raw_score * dimensions.homogeneous_people_construction.salience) / (dimensions.elite_conspiracy_systemic_corruption.salience + dimensions.authenticity_vs_political_class.salience + dimensions.homogeneous_people_construction.salience + 0.001)"
            },
            {
                "name": "salience_weighted_boundary_distinctions_index",
                "description": "Boundary distinctions weighted by salience",
                "formula": "(dimensions.nationalist_exclusion.raw_score * dimensions.nationalist_exclusion.salience + dimensions.economic_populist_appeals.raw_score * dimensions.economic_populist_appeals.salience) / (dimensions.nationalist_exclusion.salience + dimensions.economic_populist_appeals.salience + 0.001)"
            },
            {
                "name": "salience_weighted_overall_populism_index",
                "description": "Overall populism measure weighted by salience",
                "formula": "(dimensions.manichaean_people_elite_framing.raw_score * dimensions.manichaean_people_elite_framing.salience + dimensions.crisis_restoration_narrative.raw_score * dimensions.crisis_restoration_narrative.salience + dimensions.popular_sovereignty_claims.raw_score * dimensions.popular_sovereignty_claims.salience + dimensions.anti_pluralist_exclusion.raw_score * dimensions.anti_pluralist_exclusion.salience + dimensions.elite_conspiracy_systemic_corruption.raw_score * dimensions.elite_conspiracy_systemic_corruption.salience + dimensions.authenticity_vs_political_class.raw_score * dimensions.authenticity_vs_political_class.salience + dimensions.homogeneous_people_construction.raw_score * dimensions.homogeneous_people_construction.salience + dimensions.nationalist_exclusion.raw_score * dimensions.nationalist_exclusion.salience + dimensions.economic_populist_appeals.raw_score * dimensions.economic_populist_appeals.salience) / (dimensions.manichaean_people_elite_framing.salience + dimensions.crisis_restoration_narrative.salience + dimensions.popular_sovereignty_claims.salience + dimensions.anti_pluralist_exclusion.salience + dimensions.elite_conspiracy_systemic_corruption.salience + dimensions.authenticity_vs_political_class.salience + dimensions.homogeneous_people_construction.salience + dimensions.nationalist_exclusion.salience + dimensions.economic_populist_appeals.salience + 0.001)"
            }
        ]
        return derived_metrics

    def _prepare_documents(self, corpus_documents: List[Dict[str, Any]], analysis_id: str) -> tuple[List[Dict[str, Any]], List[str]]:
        """Prepares documents for analysis and returns them along with their hashes."""
        documents, document_hashes = [], []
        for i, doc in enumerate(corpus_documents):
            content_bytes = doc['content'] if isinstance(doc.get('content'), bytes) else str(doc.get('content', '')).encode('utf-8')
            doc_hash = self.storage.put_artifact(content_bytes, {
                "artifact_type": "corpus_document", "original_filename": doc.get('filename', f'doc_{i+1}'), "analysis_id": analysis_id
            })
            documents.append({
                'index': i + 1, 'hash': doc_hash, 'content': base64.b64encode(content_bytes).decode('utf-8'),
                'filename': doc.get('filename', f'doc_{i+1}')
            })
            document_hashes.append(doc_hash)
        return documents, document_hashes
