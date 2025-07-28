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
[CSV header with aid as first column, followed by framework-defined columns]
[CSV data with {artifact_id} as aid value, followed by framework-specific scores]
<<<END_DISCERNUS_SCORES_CSV_v1>>>

<<<DISCERNUS_EVIDENCE_CSV_v1>>>
[CSV header with aid as first column, followed by framework-defined columns]
[CSV data with {artifact_id} as aid value, followed by framework-specific evidence]
<<<END_DISCERNUS_EVIDENCE_CSV_v1>>>
```

**IMPORTANT**: 
1. Replace {artifact_id} with the document's hash
2. The 'aid' column MUST be first in both CSVs
3. Follow the framework's structure for all other columns
4. Include mathematical calculations and proofs for all scores
5. Provide evidence to support your analysis

**Framework (base64 encoded):**
{framework}

**Document (base64 encoded):**
{document}

Analyze the document using the framework and output your results in the required format.
Include your mathematical reasoning and calculations for each score.
"""
    
    def analyze_document(self, framework_content: str, document: Dict[str, Any],
                         experiment_config: Dict[str, Any], model: str = "vertex_ai/gemini-2.5-flash") -> Dict[str, Any]:
        """
        Analyze a single document using the framework.
        Each document is processed independently with no shared context.
        """
        # Encode inputs as base64 to prevent parsing
        framework_b64 = base64.b64encode(framework_content.encode()).decode()
        document_b64 = base64.b64encode(document["content"].encode()).decode()

        # Create prompt for this document only
        prompt_text = self.prompt_template.format(
            framework=framework_b64,
            document=document_b64,
            artifact_id=document["hash"]
        )

        # Call LLM with single document
        print(f"\n📄 Analyzing document: {document.get('filename', 'unknown')}")
        print(f"🔑 Document hash: {document['hash']}")

        response = completion(
            model=model,
            messages=[{"role": "user", "content": prompt_text}],
            temperature=0.0
        )

        if not response or not response.choices or not response.choices[0].message.content:
            raise ValueError(f"Empty response from LLM for document: {document.get('filename')}")

        return {
            "document": document.get("filename"),
            "hash": document["hash"],
            "analysis": response.choices[0].message.content
        }

    def analyze_corpus(self, framework_content: str, corpus_documents: List[Dict[str, Any]],
                      experiment_config: Dict[str, Any], model: str = "vertex_ai/gemini-2.5-flash") -> List[Dict[str, Any]]:
        """
        Analyze each document in the corpus independently.
        No context is shared between documents.
        """
        results = []
        total_docs = len(corpus_documents)

        print(f"\n🚀 Starting analysis of {total_docs} documents...")

        for i, document in enumerate(corpus_documents, 1):
            try:
                print(f"\n--- Document {i}/{total_docs} ---")
                result = self.analyze_document(
                    framework_content=framework_content,
                    document=document,
                    experiment_config=experiment_config,
                    model=model
                )
                results.append(result)
                print(f"✅ Analysis complete for: {document.get('filename')}")

            except Exception as e:
                print(f"❌ Analysis failed for document {document.get('filename')}: {str(e)}")
                results.append({
                    "document": document.get("filename"),
                    "hash": document.get("hash"),
                    "error": str(e)
                })

        return results 