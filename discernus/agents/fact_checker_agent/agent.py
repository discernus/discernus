import json
import yaml
import re
from pathlib import Path
from typing import Dict, Any, List, Optional
from ...core.audit_logger import AuditLogger
from ...core.hybrid_corpus_service import HybridCorpusService


class FactCheckerAgent:
    """A focused agent for fact-checking synthesis reports using quote validation and statistical verification."""

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
        assets: Dict[str, Any],
        corpus_index_service: HybridCorpusService = None,
    ) -> Dict[str, Any]:
        """
        Executes the fact-checking process against the report using targeted validation.

        Args:
            report_content: Content of the draft report to be validated.
            assets: Dictionary containing all synthesis assets for validation.
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
        
        # Execute each validation check
        for check in self.rubric["checks"]:
            findings = self._perform_check(check, report_content, assets, index_service)
            all_findings.extend(findings)

        summary = self._summarize_findings(all_findings)
        return summary

    def _perform_check(
        self, check: Dict[str, str], report_content: str, assets: Dict[str, Any], 
        corpus_index_service: HybridCorpusService
    ) -> List[Dict[str, Any]]:
        """
        Execute a specific validation check.
        
        Returns:
            A list of finding dictionaries if issues are found, empty list if check passes.
        """
        check_name = check.get('name', '')
        
        if check_name == "Quote Validation":
            return self._validate_quotes(report_content, corpus_index_service)
        elif check_name == "Statistical Verification":
            return self._verify_statistics(report_content, assets)
        elif check_name == "Framework Compliance":
            return self._verify_framework_compliance(report_content, assets)
        elif check_name == "Evidence Attribution":
            return self._verify_evidence_attribution(report_content)
        else:
            return [{"error": f"Unknown check type: {check_name}"}]

    def _validate_quotes(self, report_content: str, corpus_index_service: HybridCorpusService) -> List[Dict[str, Any]]:
        """
        Validate all quotes found in the report against the corpus index.
        
        Args:
            report_content: Content of the report to validate
            corpus_index_service: Corpus index service for validation
            
        Returns:
            List of finding dictionaries
        """
        if not corpus_index_service:
            return [{"error": "No corpus index service available for quote validation."}]
        
        # Extract quotes using multiple patterns
        quotes = []
        
        # Pattern 1: Standard quotes
        quotes.extend(re.findall(r'"([^"]{20,100})"', report_content))
        
        # Pattern 2: Italicized quotes (markdown)
        quotes.extend(re.findall(r'\*([^*]{20,100})\*', report_content))
        
        # Pattern 3: Bold quotes (markdown)
        quotes.extend(re.findall(r'\*\*([^*]{20,100})\*\*', report_content))
        
        # Pattern 4: Single quotes
        quotes.extend(re.findall(r"'([^']{20,100})'", report_content))
        
        # Remove duplicates and filter by length
        unique_quotes = list(set([q.strip() for q in quotes if len(q.strip()) >= 20]))
        
        if not unique_quotes:
            return []
        
        findings = []
        for quote in unique_quotes:
            try:
                # Validate each quote using the hybrid search
                validation = corpus_index_service.validate_quote(quote)
                
                # Only report significant issues
                drift_level = validation.get('drift_level', 'unknown')
                if drift_level in ['significant_drift', 'major_drift', 'hallucination']:
                    finding = {
                        "check_name": "Quote Validation",
                        "severity": "WARNING",
                        "description": f"Quote has {drift_level} from original source",
                        "details": f"Quote: '{quote[:100]}{'...' if len(quote) > 100 else ''}'",
                        "examples": [quote],
                        "quote_validation": {
                            "quote": quote,
                            "drift_level": drift_level,
                            "score": validation.get('score', 0),
                            "best_match": validation.get('best_match', {}),
                            "canonical_text": validation.get('canonical_text', '')
                        }
                    }
                    findings.append(finding)
                    
            except Exception as e:
                # Log validation errors but continue
                finding = {
                    "check_name": "Quote Validation",
                    "severity": "ERROR",
                    "description": "Quote validation failed due to error",
                    "details": f"Error validating quote: {str(e)}",
                    "examples": [quote],
                    "quote_validation": {"error": str(e)}
                }
                findings.append(finding)
        
        return findings

    def _verify_statistics(self, report_content: str, assets: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Verify statistical claims in the report against provided assets.
        
        Args:
            report_content: Content of the report to validate
            assets: Dictionary containing all synthesis assets
            
        Returns:
            List of finding dictionaries
        """
        findings = []
        
        # Extract numerical claims from the report
        # Pattern: numbers with decimal points, percentages, correlations
        numerical_patterns = [
            r'(\d+\.\d+)',  # Decimal numbers
            r'(\d+)%',      # Percentages
            r'r\s*=\s*([+-]?\d+\.\d+)',  # Correlation coefficients
            r'mean\s*=\s*([+-]?\d+\.\d+)',  # Means
            r'std\s*=\s*([+-]?\d+\.\d+)',   # Standard deviations
        ]
        
        for pattern in numerical_patterns:
            matches = re.findall(pattern, report_content, re.IGNORECASE)
            for match in matches:
                try:
                    value = float(match)
                    
                    # Check for unrealistic values
                    if pattern == r'(\d+)%' and value == 100:
                        findings.append({
                            "check_name": "Statistical Verification",
                            "severity": "WARNING",
                            "description": "Report claims 100% value, which may be unrealistic",
                            "details": f"Found 100% claim in report. This may be an exaggeration or missing context.",
                            "examples": [f"{value}%"],
                            "quote_validation": {}
                        })
                    
                    # Check for correlation coefficients outside valid range
                    elif 'r' in pattern and (value < -1 or value > 1):
                        findings.append({
                            "check_name": "Statistical Verification",
                            "severity": "CRITICAL",
                            "description": "Invalid correlation coefficient value",
                            "details": f"Correlation coefficient r={value} is outside valid range [-1, 1]",
                            "examples": [f"r={value}"],
                            "quote_validation": {}
                        })
                        
                except ValueError:
                    continue
        
        # Check for vague statistical claims without specific numbers
        vague_claims = [
            r'significant\s+(?:increase|decrease|difference)',
            r'high\s+(?:correlation|accuracy|precision)',
            r'strong\s+(?:relationship|association|effect)',
            r'proven\s+(?:beyond\s+)?doubt',
            r'demonstrates\s+conclusively'
        ]
        
        for pattern in vague_claims:
            if re.search(pattern, report_content, re.IGNORECASE):
                findings.append({
                    "check_name": "Statistical Verification",
                    "severity": "WARNING",
                    "description": "Vague statistical claim without specific data",
                    "details": f"Report contains vague claim matching pattern: '{pattern}'",
                    "examples": [],
                    "quote_validation": {}
                })
        
        return findings

    def _verify_framework_compliance(self, report_content: str, assets: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Verify that the report adheres to the specified framework.
        
        Args:
            report_content: Content of the report to validate
            assets: Dictionary containing all synthesis assets
            
        Returns:
            List of finding dictionaries
        """
        findings = []
        
        # Example: Check for "framework dimensions" in the report
        if re.search(r"framework dimensions", report_content, re.IGNORECASE):
            findings.append({
                "check_name": "Framework Compliance",
                "severity": "WARNING",
                "description": "Report mentions framework dimensions, but no specific framework is provided.",
                "details": "The report mentions framework dimensions, but no specific framework name or definition is provided. This might be a dimension hallucination.",
                "examples": [],
                "quote_validation": {}
            })
        
        # Example: Check for "analytical dimensions" in the report
        if re.search(r"analytical dimensions", report_content, re.IGNORECASE):
            findings.append({
                "check_name": "Framework Compliance",
                "severity": "WARNING",
                "description": "Report mentions analytical dimensions, but no specific framework is provided.",
                "details": "The report mentions analytical dimensions, but no specific framework name or definition is provided. This might be a dimension hallucination.",
                "examples": [],
                "quote_validation": {}
            })
        
        return findings

    def _verify_evidence_attribution(self, report_content: str) -> List[Dict[str, Any]]:
        """
        Verify that evidence is properly attributed in the report.
        
        Args:
            report_content: Content of the report to validate
            
        Returns:
            List of finding dictionaries
        """
        findings = []
        
        # Example: Check for "According to [Source]" or "Based on [Source]"
        if re.search(r"According to \[.*?\]", report_content, re.IGNORECASE) or re.search(r"Based on \[.*?\]", report_content, re.IGNORECASE):
            findings.append({
                "check_name": "Evidence Attribution",
                "severity": "WARNING",
                "description": "Report uses attribution phrases without specific sources.",
                "details": "The report uses phrases like 'According to [Source]' or 'Based on [Source]' without providing a specific source. This makes it difficult to verify the evidence.",
                "examples": [],
                "quote_validation": {}
            })
        
        return findings

    def _summarize_findings(self, findings: List[Dict[str, Any]]) -> Dict[str, Any]:
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
