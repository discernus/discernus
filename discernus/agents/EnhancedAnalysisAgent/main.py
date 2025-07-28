"""
Enhanced analysis agent with mathematical validation.

Analyzes documents using framework and outputs results with embedded CSV sections.
"""

import base64
import json
from typing import Dict, Any, List, Optional

from litellm import completion

from discernus.core.security_boundary import ExperimentSecurityBoundary
from discernus.core.audit_logger import AuditLogger
from discernus.core.local_artifact_storage import LocalArtifactStorage


class EnhancedAnalysisAgent:
    """
    Enhanced analysis agent with mathematical validation.
    
    Analyzes documents using framework and outputs results with embedded CSV sections.
    """
    
    def __init__(self, security: ExperimentSecurityBoundary, audit: AuditLogger,
                storage: LocalArtifactStorage):
        """
        Initialize analysis agent.
        
        Args:
            security: Security boundary
            audit: Audit logger
            storage: Artifact storage
        """
        self.security = security
        self.audit = audit
        self.storage = storage
        self.agent_name = "EnhancedAnalysisAgent"
        
        # Load prompt template
        self.prompt_template = """
You are an enhanced computational research analysis agent. Your task is to analyze a document using a provided framework and output your analysis in a format that includes embedded CSV sections.

**CRITICAL: Your response MUST include these two CSV sections with the exact delimiters shown:**

```
<<<DISCERNUS_SCORES_CSV_v1>>>
aid,[framework-defined score columns]
{artifact_id},[framework-specific scores]
<<<END_DISCERNUS_SCORES_CSV_v1>>>

<<<DISCERNUS_EVIDENCE_CSV_v1>>>
aid,dimension,[framework-defined evidence columns]
{artifact_id},{dimension_name},[framework-specific evidence data]
<<<END_DISCERNUS_EVIDENCE_CSV_v1>>>
```

**IMPORTANT**: 
1. Replace {artifact_id} with the document's hash
2. The 'aid' column MUST be first in both CSVs
3. The 'dimension' column MUST be second in the evidence CSV
4. Include mathematical calculations and proofs for all scores

**Framework (base64 encoded):**
{framework}

**Document (base64 encoded):**
{document}

Analyze the document using the framework and output your results in the required format.
"""
    
    def analyze_documents(self, framework_content: str, corpus_documents: List[Dict[str, Any]],
                       experiment_config: Dict[str, Any], model: str = "vertex_ai/gemini-2.5-flash",
                       current_scores_hash: Optional[str] = None,
                       current_evidence_hash: Optional[str] = None) -> Dict[str, Any]:
        """
        Analyze documents using framework.
        
        Args:
            framework_content: Raw framework content
            corpus_documents: List of document dictionaries
            experiment_config: Experiment configuration
            model: LLM model to use
            current_scores_hash: Current scores CSV hash
            current_evidence_hash: Current evidence CSV hash
            
        Returns:
            Analysis results with CSV hashes
        """
        # Base64 encode framework
        framework_b64 = base64.b64encode(framework_content.encode()).decode()
        
        # Process one document at a time
        document = corpus_documents[0]  # Single document list
        document_b64 = base64.b64encode(document["content"].encode()).decode()
        
        # Generate prompt
        prompt_text = self.prompt_template.format(
            framework=f"=== FRAMEWORK (base64 encoded) ===\n{framework_b64}\n",
            document=f"=== DOCUMENT (base64 encoded) ===\n{document_b64}\n",
            artifact_id=document["hash"]
        )
        
        # Call LLM
        self.audit.log_agent_event(self.agent_name, "llm_call_start", {
            "document": document["filename"],
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
        
        # Extract CSV sections
        scores_csv = self._extract_csv_section(result_text, "DISCERNUS_SCORES_CSV_v1")
        evidence_csv = self._extract_csv_section(result_text, "DISCERNUS_EVIDENCE_CSV_v1")
        
        # Store CSVs
        scores_hash = self.storage.put_artifact(
            scores_csv.encode(),
            {"artifact_type": "intermediate_scores.csv"}
        )
        evidence_hash = self.storage.put_artifact(
            evidence_csv.encode(),
            {"artifact_type": "intermediate_evidence.csv"}
        )
        
        # Store full analysis
        analysis_hash = self.storage.put_artifact(
            result_text.encode(),
            {"artifact_type": "analysis_result"}
        )
        
        return {
            "scores_hash": scores_hash,
            "evidence_hash": evidence_hash,
            "analysis_result": {
                "document": document["filename"],
                "result_hash": analysis_hash
            }
        }
    
    def _extract_csv_section(self, text: str, section_name: str) -> str:
        """
        Extract CSV section from text.
        
        Args:
            text: Text containing CSV section
            section_name: Name of CSV section
            
        Returns:
            CSV content
            
        Raises:
            ValueError: If CSV section not found
        """
        start_marker = f"<<<{section_name}>>>"
        end_marker = f"<<<END_{section_name}>>>"
        
        start_idx = text.find(start_marker)
        end_idx = text.find(end_marker)
        
        if start_idx == -1 or end_idx == -1:
            raise ValueError(f"CSV section {section_name} not found")
        
        csv_content = text[start_idx + len(start_marker):end_idx].strip()
        return csv_content 