import json
from pathlib import Path
from typing import Dict, Any, List

class FactCheckerAgent:
    """
    An agent that validates the factual accuracy of a synthesis report
    against a set of source artifacts using a rubric-driven approach.
    """

    def __init__(self, llm_gateway):
        self.rubric = self._load_rubric()
        self.llm_gateway = llm_gateway

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

    def validate_report(self, report_path: Path, rag_index) -> Dict[str, Any]:
        """
        Executes the fact-checking process against the report.

        Args:
            report_path: Path to the final_report.md to be validated.
            rag_index: A pre-built RAG index containing all necessary source artifacts.

        Returns:
            A dictionary containing the validation results.
        """
        report_content = report_path.read_text(encoding='utf-8')
        validation_results = []

        for check in self.rubric.get('checks', []):
            check_name = check.get('name')
            description = check.get('description')
            instructions = check.get('instructions')
            severity = check.get('severity')
            
            try:
                # Execute the specific check
                finding = self._execute_check(check_name, description, instructions, severity, report_content, rag_index)
                if finding:
                    validation_results.append(finding)
            except Exception as e:
                # Log check failure but continue with other checks
                validation_results.append({
                    "check_name": check_name,
                    "severity": "ERROR",
                    "description": f"Check execution failed: {str(e)}",
                    "details": None
                })

        # Determine status based on validation results
        critical_failures = [f for f in validation_results if f.get('severity') == 'CRITICAL']
        errors = [f for f in validation_results if f.get('severity') == 'ERROR']
        
        if critical_failures or errors:
            status = "failed"
        else:
            status = "success"
        
        return {
            "status": status,
            "findings": validation_results,
            "summary": {
                "total_checks": len(self.rubric.get('checks', [])),
                "critical_failures": len(critical_failures),
                "errors": len(errors),
                "warnings": len([f for f in validation_results if f.get('severity') == 'WARNING'])
            }
        }
    
    def _execute_check(self, check_name: str, description: str, instructions: str, severity: str, report_content: str, rag_index) -> Dict[str, Any]:
        """
        Execute a specific validation check using the LLM.
        
        Returns:
            A finding dictionary if issues are found, None if check passes.
        """
        # Get relevant source materials from RAG index for this check
        try:
            source_context = self._get_source_context_for_check(check_name, report_content, rag_index)
        except RuntimeError as e:
            # RAG index failure is a critical infrastructure issue
            return {
                "check_name": check_name,
                "severity": "CRITICAL",
                "description": f"Check cannot execute due to RAG index failure: {str(e)}",
                "details": "This validation check cannot proceed because the system cannot access required source materials. This indicates a critical infrastructure failure that must be resolved before validation can continue.",
                "examples": []
            }
        
        # Create a focused prompt for this specific check
        check_prompt = f"""You are a fact-checking agent validating an academic research report.

**CHECK: {check_name}**
**SEVERITY: {severity}**
**DESCRIPTION: {description}**

**INSTRUCTIONS:**
{instructions}

**REPORT TO VALIDATE:**
{report_content[:5000]}  # Truncate for context window

**SOURCE MATERIALS FOR VALIDATION:**
{source_context}

**TASK:**
Execute the validation check described above using the provided source materials. If you find issues, respond with:
```json
{{
    "issues_found": true,
    "details": "Specific description of what was found",
    "examples": ["example 1", "example 2"]
}}
```

If no issues are found, respond with:
```json
{{
    "issues_found": false,
    "details": "Check passed - no issues detected"
}}
```

Be precise and factual. Only report actual issues, not potential concerns.
"""

        try:
            # Use the LLM gateway to execute the check
            response, metadata = self.llm_gateway.execute_call(
                model="vertex_ai/gemini-2.5-flash",  # Use Flash for cost efficiency
                prompt=check_prompt,
                temperature=0.1  # Low temperature for consistency
            )
            
            # Parse the response
            import json
            import re
            
            # Extract JSON from response
            json_match = re.search(r'```json\s*(.*?)\s*```', response, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group(1))
                
                if result.get('issues_found'):
                    return {
                        "check_name": check_name,
                        "severity": severity,
                        "description": description,
                        "details": result.get('details'),
                        "examples": result.get('examples', [])
                    }
            
            # No issues found or couldn't parse response
            return None
            
        except Exception as e:
            # Return error finding
            return {
                "check_name": check_name,
                "severity": "ERROR",
                "description": f"Check execution failed: {str(e)}",
                "details": None
            }
    
    def _get_source_context_for_check(self, check_name: str, report_content: str, rag_index) -> str:
        """
        Get relevant source context from the RAG index for a specific check.
        
        Returns:
            Formatted string containing relevant source materials for validation.
        """
        try:
            if not rag_index:
                return "No source materials available for validation."
            
            # Create check-specific queries to retrieve relevant source materials
            queries = []
            
            if check_name == "Dimension Hallucination":
                queries = [
                    "framework dimensions list definition",
                    "analytical dimensions framework specification",
                    "cohesive flourishing framework dimensions"
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
            for i, query in enumerate(queries):
                try:
                    # Use the RAG index's search method (assuming it has one)
                    if hasattr(rag_index, 'search'):
                        print(f"🔍 Fact-checker query {i+1}: '{query}'")
                        results = rag_index.search(query, limit=3)
                        print(f"🔍 Query returned {len(results)} results")
                        
                        for j, result in enumerate(results):
                            # txtai returns (id, score) tuples, so we need to get content from stored documents
                            if isinstance(result, tuple) and len(result) == 2:
                                doc_id, score = result
                                # Get document content from the stored documents
                                if hasattr(rag_index, 'documents') and rag_index.documents:
                                    try:
                                        doc_data = rag_index.documents[doc_id]
                                        content = doc_data.get('text', '')  # No longer truncating
                                        source_materials.append(content)
                                        print(f"🔍 Result {j+1}: {len(content)} chars")
                                    except (IndexError, KeyError) as e:
                                        print(f"⚠️ Could not retrieve document {doc_id}: {e}")
                                        continue
                                else:
                                    print(f"⚠️ RAG index has no stored documents")
                                    continue
                            elif isinstance(result, dict) and 'content' in result:
                                content = result['content']  # No longer truncating
                                source_materials.append(content)
                                print(f"🔍 Result {j+1}: {len(content)} chars")
                            elif isinstance(result, str):
                                content = result  # No longer truncating
                                source_materials.append(content)
                                print(f"🔍 Result {j+1}: {len(content)} chars")
                    else:
                        print(f"⚠️ RAG index has no search method")
                except Exception as e:
                    print(f"❌ Query failed: {e}")
                    continue  # Skip failed queries
            
            if source_materials:
                return "\n\n".join([f"SOURCE {i+1}:\n{material}" for i, material in enumerate(source_materials[:5])])
            else:
                # This is a critical infrastructure failure - raise an exception to be caught by the calling method
                raise RuntimeError("Source materials could not be retrieved from the RAG index. This indicates a critical infrastructure failure that prevents validation from proceeding.")
                
        except Exception as e:
            # Re-raise as RuntimeError to be caught by the calling method
            raise RuntimeError(f"Critical RAG index failure: {str(e)}")
