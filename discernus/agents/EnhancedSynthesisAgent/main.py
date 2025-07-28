"""
Enhanced synthesis agent with mathematical spot-checking.

Synthesizes analysis results into comprehensive report.
"""

import base64
import json
from typing import Dict, Any, List, Optional

from litellm import completion

from discernus.core.security_boundary import ExperimentSecurityBoundary
from discernus.core.audit_logger import AuditLogger
from discernus.core.local_artifact_storage import LocalArtifactStorage


class EnhancedSynthesisAgent:
    """
    Enhanced synthesis agent with mathematical spot-checking.
    
    Synthesizes analysis results into comprehensive report.
    """
    
    def __init__(self, security: ExperimentSecurityBoundary, audit: AuditLogger,
                storage: LocalArtifactStorage):
        """
        Initialize synthesis agent.
        
        Args:
            security: Security boundary
            audit: Audit logger
            storage: Artifact storage
        """
        self.security = security
        self.audit = audit
        self.storage = storage
        self.agent_name = "EnhancedSynthesisAgent"
        
        # Load prompt template
        self.prompt_template = """
You are an expert synthesis agent. Your task is to synthesize the following analysis results into a coherent report.

Here are the aggregated scores from all documents:
<<<DISCERNUS_SCORES_CSV_v1>>>
{scores_csv}
<<<END_DISCERNUS_SCORES_CSV_v1>>>

Here is the aggregated evidence from all documents:
<<<DISCERNUS_EVIDENCE_CSV_v1>>>
{evidence_csv}
<<<END_DISCERNUS_EVIDENCE_CSV_v1>>>

Here are the raw analysis results for your reference:
{analysis_results}

Please provide a comprehensive synthesis of these results in markdown format. Your report should:
1. Analyze the overall patterns and trends in the scores
2. Identify key themes and insights from the evidence
3. Highlight any notable correlations or relationships
4. Provide specific examples to support your findings
5. Maintain a neutral, factual tone

**IMPORTANT**:
1. Include mathematical calculations and proofs for all statistical claims
2. Spot-check individual analyses for consistency
3. Report any anomalies or discrepancies found
"""
    
    def synthesize_results(self, scores_hash: str, evidence_hash: str,
                         analysis_results: List[Dict[str, Any]],
                         experiment_config: Dict[str, Any],
                         model: str = "vertex_ai/gemini-2.5-flash") -> Dict[str, Any]:
        """
        Synthesize analysis results.
        
        Args:
            scores_hash: Hash of scores CSV
            evidence_hash: Hash of evidence CSV
            analysis_results: List of analysis results
            experiment_config: Experiment configuration
            model: LLM model to use
            
        Returns:
            Synthesis results
        """
        # Load CSVs
        scores_csv = self.storage.get_artifact(scores_hash).decode()
        evidence_csv = self.storage.get_artifact(evidence_hash).decode()
        
        # Format analysis results
        analysis_text = ""
        for result in analysis_results:
            if "result_hash" in result:
                analysis = self.storage.get_artifact(result["result_hash"]).decode()
                analysis_text += f"\n=== {result['document']} ===\n{analysis}\n"
        
        # Generate prompt
        prompt_text = self.prompt_template.format(
            scores_csv=scores_csv,
            evidence_csv=evidence_csv,
            analysis_results=analysis_text
        )
        
        # Call LLM
        self.audit.log_agent_event(self.agent_name, "llm_call_start", {
            "model": model,
            "prompt_length": len(prompt_text)
        })
        
        response = completion(
            model=model,
            messages=[{"role": "user", "content": prompt_text}],
            temperature=0.0,
            max_tokens=6000
        )
        
        if not response.choices[0].message.content:
            raise ValueError("Empty response from LLM")
        
        result_text = response.choices[0].message.content
        
        # Store synthesis result
        result_hash = self.storage.put_artifact(
            result_text.encode(),
            {"artifact_type": "synthesis_result"}
        )
        
        return {
            "synthesis_report_markdown": result_text,
            "result_hash": result_hash
        } 