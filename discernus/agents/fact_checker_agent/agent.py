import json
import yaml
from pathlib import Path
from typing import Dict, Any, List
from ...core.audit_logger import AuditLogger
from ...core.hybrid_corpus_service import HybridCorpusService


class FactCheckerAgent:
    """A multi-stage agent for fact-checking synthesis reports using hybrid (Typesense + BM25) corpus indexing."""

    def __init__(self, gateway, audit_logger: AuditLogger, corpus_index_service: HybridCorpusService = None):
        self.gateway = gateway
        self.audit_logger = audit_logger
        self.corpus_index_service = corpus_index_service
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
        corpus_index_service: HybridCorpusService = None,
    ) -> Dict[str, Any]:
        """
        Executes the fact-checking process against the report using corpus indexing.

        Args:
            report_content: Content of the final report to be validated.
            corpus_index_service: Corpus index service for quote validation.

        Returns:
            A dictionary containing the validation results.
        """
        # Use provided service or fall back to instance service
        index_service = corpus_index_service or self.corpus_index_service
        
        if self.audit_logger:
            self.audit_logger.log_agent_event(
                agent_name="FactCheckerAgent",
                event_type="fact_check_start",
                data={"report_length": len(report_content)}
            )

        all_findings = []
        for check in self.rubric["checks"]:
            findings = self._perform_check(
                check, report_content, index_service
            )
            all_findings.extend(findings)

        summary = self._summarize_findings(all_findings)
        return summary

    def _perform_check(
        self, check: Dict[str, str], report_content: str, corpus_index_service: HybridCorpusService
    ) -> List[Dict[str, str]]:
        """
        Execute a specific validation check using the LLM and corpus indexing.
        
        Returns:
            A finding dictionary if issues are found, None if check passes.
        """
        prompt = self._assemble_prompt(check, report_content, corpus_index_service)

        response, metadata = self.gateway.execute_call(
            model="vertex_ai/gemini-2.5-flash",  # Use Flash for cost-effective fact-checking
            prompt=prompt,
            temperature=0.1  # Low temperature for consistency
        )

        return self._parse_response(response, check)

    def _assemble_prompt(
        self, check: Dict[str, str], report_content: str, corpus_index_service: HybridCorpusService
    ) -> str:
        """Assembles the prompt for a specific fact-checking task using corpus indexing."""
        
        # Get relevant evidence context for this check
        evidence_context = self._get_evidence_context(check, report_content, corpus_index_service)
        
        return f"""
You are a meticulous fact-checker. Your task is to validate a research report based on a specific rubric using the provided corpus indexing system.

# RUBRIC FOR THIS CHECK

- **Check Name:** {check['name']}
- **Severity:** {check['severity']}
- **Description:** {check['description']}
- **Instructions:** {check['instructions']}

# REPORT TO VALIDATE

{report_content}

# CORPUS INDEXING SYSTEM FOR VALIDATION
{evidence_context}

# INSTRUCTIONS

1. Carefully read the report content.
2. Apply the rubric instructions precisely using the corpus indexing system above.
3. If you find issues, respond with:
```json
{{
    "issues_found": true,
    "details": "Specific description of what was found",
    "examples": ["example 1", "example 2"],
    "quote_validation": {{
        "quotes_checked": ["quote1", "quote2"],
        "validation_results": ["valid", "invalid"],
        "drift_analysis": ["exact", "minor_drift", "significant_drift", "hallucination"]
    }}
}}

4. If no issues are found, respond with:
```json
{{
    "issues_found": false,
    "details": "Check passed - no issues detected"
}}
```

Be precise and factual. Only report actual issues, not potential concerns.
"""

    def _get_evidence_context(self, check: Dict[str, str], report_content: str, corpus_index_service: HybridCorpusService) -> str:
        """Get relevant evidence context for a specific check using corpus indexing."""
        check_name = check.get('name', '')
        
        if not corpus_index_service:
            return "⚠️ **CORPUS INDEX STATUS**: No corpus indexing service available. Quote validation will be limited."
        
        # Create check-specific queries to retrieve relevant source materials
        queries = []
        
        if check_name == "Dimension Hallucination":
            queries = [
                "framework dimensions list definition",
                "analytical dimensions framework specification",
                "framework structure axes dimensions"
            ]
        elif check_name == "Evidence Quote Mismatch":
            # Extract quotes from the report to search for
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
        
        # Query the corpus index for relevant context
        source_materials = []
        for query in queries:
            try:
                results = corpus_index_service.search_quotes(query, fuzziness="AUTO", size=3)
                for result in results:
                    if result.get('highlighted_content'):
                        # Format with metadata for context
                        filename = result.get('filename', 'unknown')
                        speaker = result.get('speaker', 'unknown')
                        score = result.get('score', 0.0)
                        content = result.get('highlighted_content', '')
                        source_materials.append(f"[{filename}: {speaker}] (Score: {score:.2f})\n{content}")
                    elif result.get('full_content'):
                        # Fallback to full content if no highlight
                        filename = result.get('filename', 'unknown')
                        speaker = result.get('speaker', 'unknown')
                        content = result.get('full_content', '')[:500]  # Limit length
                        source_materials.append(f"[{filename}: {speaker}]\n{content}")
            except Exception as e:
                continue  # Skip failed queries
        
        if source_materials:
            return "\n\n".join([f"SOURCE {i+1}:\n{material}" for i, material in enumerate(source_materials[:5])])
        else:
            return "No relevant source materials found in corpus index."
    
    def validate_quotes_in_report(self, report_content: str, corpus_index_service: HybridCorpusService) -> Dict[str, Any]:
        """
        Validate all quotes found in the report against the corpus index.
        
        Args:
            report_content: Content of the report to validate
            corpus_index_service: Corpus index service for validation
            
        Returns:
            Dictionary containing quote validation results
        """
        if not corpus_index_service:
            return {"error": "No corpus index service available"}
        
        import re
        
        # Extract quotes from the report
        quotes = re.findall(r'"([^"]{20,100})"', report_content)
        
        if not quotes:
            return {"message": "No quotes found in report", "quotes_checked": 0}
        
        validation_results = []
        total_quotes = len(quotes)
        valid_quotes = 0
        invalid_quotes = 0
        
        for quote in quotes:
            # Validate each quote
            validation = corpus_index_service.validate_quote(quote)
            
            result = {
                "quote": quote[:100] + "..." if len(quote) > 100 else quote,
                "validation": validation,
                "status": "valid" if validation.get("valid", False) else "invalid"
            }
            
            validation_results.append(result)
            
            if validation.get("valid", False):
                valid_quotes += 1
            else:
                invalid_quotes += 1
        
        return {
            "total_quotes": total_quotes,
            "valid_quotes": valid_quotes,
            "invalid_quotes": invalid_quotes,
            "validation_results": validation_results,
            "summary": f"Validated {total_quotes} quotes: {valid_quotes} valid, {invalid_quotes} invalid"
        }

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
                            "examples": result.get('examples', []),
                            "quote_validation": result.get('quote_validation', {})
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
