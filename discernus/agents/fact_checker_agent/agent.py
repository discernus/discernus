import json
import yaml
from pathlib import Path
from typing import Dict, Any, List
from ...core.audit_logger import AuditLogger


class FactCheckerAgent:
    """A multi-stage agent for fact-checking synthesis reports."""

    def __init__(self, gateway, audit_logger: AuditLogger):
        self.gateway = gateway
        self.audit_logger = audit_logger
        self.rubric = self._load_rubric()

    def _load_rubric(self) -> Dict[str, Any]:
        """Loads the validation rubric from the agent's directory."""
        import yaml
        import os
        agent_dir = os.path.dirname(__file__)
        rubric_path = os.path.join(agent_dir, 'rubric.yaml')
        if not os.path.exists(rubric_path):
            raise FileNotFoundError(f"Rubric file not found: {rubric_path}")
        with open(rubric_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def check(
        self,
        report_content: str,
        evidence_index: Any,
    ) -> Dict[str, Any]:
        """
        Executes the fact-checking process against the report.

        Args:
            report_path: Path to the final_report.md to be validated.
            rag_index: A pre-built RAG index containing all necessary source artifacts.

        Returns:
            A dictionary containing the validation results.
        """
        if self.audit_logger:
            self.audit_logger.log_agent_event(
                agent_name="FactCheckerAgent",
                event_type="fact_check_start",
                data={"report_length": len(report_content)}
            )

        all_findings = []
        for check in self.rubric["checks"]:
            findings = self._perform_check(
                check, report_content, evidence_index
            )
            all_findings.extend(findings)

        summary = self._summarize_findings(all_findings)
        return summary

    def _perform_check(
        self, check: Dict[str, str], report_content: str, evidence_index: Any
    ) -> List[Dict[str, str]]:
        """
        Execute a specific validation check using the LLM.
        
        Returns:
            A finding dictionary if issues are found, None if check passes.
        """
        prompt = self._assemble_prompt(check, report_content, evidence_index)

        response, metadata = self.gateway.execute_call(
            model="vertex_ai/gemini-2.5-flash",  # Use Flash for cost-effective fact-checking
            prompt=prompt,
            temperature=0.1  # Low temperature for consistency
        )

        return self._parse_response(response, check)

    def _assemble_prompt(
        self, check: Dict[str, str], report_content: str, evidence_index: Any
    ) -> str:
        """Assembles the prompt for a specific fact-checking task."""
        
        # Get relevant evidence from the RAG index for this check
        evidence_context = self._get_evidence_context(check, report_content, evidence_index)
        
        return f"""
You are a meticulous fact-checker. Your task is to validate a research report based on a specific rubric using the provided evidence database.

# RUBRIC FOR THIS CHECK

- **Check Name:** {check['name']}
- **Severity:** {check['severity']}
- **Description:** {check['description']}
- **Instructions:** {check['instructions']}

# REPORT TO VALIDATE

{report_content}

# EVIDENCE DATABASE FOR VALIDATION

{evidence_context}

# INSTRUCTIONS

1. Carefully read the report content.
2. Apply the rubric instructions precisely using the evidence database above.
3. If you find issues, respond with:
```json
{{
    "issues_found": true,
    "details": "Specific description of what was found",
    "examples": ["example 1", "example 2"]
}}
```

4. If no issues are found, respond with:
```json
{{
    "issues_found": false,
    "details": "Check passed - no issues detected"
}}
```

Be precise and factual. Only report actual issues, not potential concerns.
"""

    def _get_evidence_context(self, check: Dict[str, str], report_content: str, evidence_index: Any) -> str:
        """Get relevant evidence context for a specific check."""
        check_name = check.get('name', '')
        
        # Create check-specific queries to retrieve relevant source materials
        queries = []
        
        if check_name == "Dimension Hallucination":
            queries = [
                "framework dimensions list definition",
                "analytical dimensions framework specification",
                "framework structure axes dimensions"
            ]
        elif check_name == "Evidence Quote Mismatch":
            # Extract some quotes from the report to search for
            import re
            quotes = re.findall(r'"([^"]{20,100})"', report_content)
            queries = quotes[:5] if quotes else ["evidence quotes textual content"]
        elif check_name == "Statistic Mismatch":
            queries = [
                "statistical results numerical values",
                "correlation coefficients means standard deviation",
                "statistical analysis results data"
            ]
        elif check_name == "Grandiose Claim":
            queries = [
                "breakthrough unprecedented first ever",
                "major achievement significant discovery",
                "proves beyond doubt demonstrates conclusively"
            ]
        else:
            queries = ["validation source materials"]
        
        # Query the RAG index for relevant context
        source_materials = []
        for query in queries:
            try:
                results = self._query_evidence(query, evidence_index)
                for result in results:
                    if 'content' in result:
                        # Format with metadata for context
                        metadata = result.get('metadata', {})
                        source_type = metadata.get('source_type', 'unknown')
                        filename = metadata.get('filename', 'unknown')
                        content = result['content'][:2000]  # Limit length
                        source_materials.append(f"[{source_type}: {filename}]\n{content}")
                    elif 'error' in result:
                        source_materials.append(f"ERROR: {result['error']}")
            except Exception as e:
                continue  # Skip failed queries
        
        if source_materials:
            return "\n\n".join([f"SOURCE {i+1}:\n{material}" for i, material in enumerate(source_materials[:5])])
        else:
            return "No relevant source materials found in evidence database."

    def _query_evidence(self, query: str, evidence_index: Any) -> List[Dict[str, Any]]:
        """
        Get relevant source context from the RAG index for a specific check.
        
        Returns:
            List of document dictionaries with content and metadata.
        """
        try:
            if not evidence_index:
                return [{"error": "No evidence index available for query."}]
            
            # Use the RAG index's search method to get (id, score) tuples
            search_results = evidence_index.search(query, limit=3)
            
            if not search_results:
                return [{"error": "No results found for query."}]
            
            # Extract actual document content using the stored documents
            documents = []
            for doc_id, score in search_results:
                if hasattr(evidence_index, 'documents') and evidence_index.documents:
                    # Find the document by ID in the stored documents
                    for doc in evidence_index.documents:
                        if doc['id'] == doc_id:
                            documents.append({
                                "content": doc['text'],
                                "metadata": doc.get('metadata', {}),
                                "score": score
                            })
                            break
                else:
                    documents.append({"error": f"Document {doc_id} not found in stored documents"})
            
            return documents if documents else [{"error": "No document content could be retrieved"}]
                
        except Exception as e:
            return [{"error": f"Query failed: {e}"}]

    def _parse_response(
        self, response: str, check: Dict[str, str]
    ) -> List[Dict[str, str]]:
        """
        Parse the LLM response to extract findings.
        """
        import json
        import re
        
        # Extract JSON from response
        json_match = re.search(r'```json\s*(.*?)\s*```', response, re.DOTALL)
        if json_match:
            try:
                result = json.loads(json_match.group(1))
                
                if result.get('issues_found'):
                    return [
                        {
                            "check_name": check['name'],
                            "severity": check['severity'],
                            "description": check['description'],
                            "details": result.get('details'),
                            "examples": result.get('examples', [])
                        }
                    ]
            
            except json.JSONDecodeError:
                return [{"error": "Could not decode JSON response."}]
        
        # No issues found or couldn't parse response
        return []

    def _summarize_findings(self, findings: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Summarize the validation findings.
        """
        summary = {
            "status": "completed",
            "findings": findings,  # Include the actual findings
            "validation_results": {
                "total_checks": len(self.rubric.get('checks', [])),
                "critical_failures": 0,
                "errors": 0,
                "warnings": 0
            }
        }
        
        # Count findings by severity
        for finding in findings:
            if finding.get('severity') == 'CRITICAL':
                summary['validation_results']['critical_failures'] += 1
            elif finding.get('severity') == 'ERROR':
                summary['validation_results']['errors'] += 1
            elif finding.get('severity') == 'WARNING':
                summary['validation_results']['warnings'] += 1
        
        return summary
