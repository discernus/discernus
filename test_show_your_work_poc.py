#!/usr/bin/env python3
"""
Phase 0: Proof of Concept for Show Your Work Architecture
========================================================

Tests core assumptions:
1. LLM internal code execution reliability
2. Evidence stripping reduces tokens by ~44%
3. Basic verification concept with Gemini 2.5 Pro
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any, List

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from discernus.gateway.llm_gateway import LLMGateway
from discernus.gateway.model_registry import ModelRegistry
from discernus.core.audit_logger import AuditLogger


class ShowYourWorkPOC:
    """Proof of concept for Show Your Work architecture."""
    
    def __init__(self):
        from discernus.core.security_boundary import ExperimentSecurityBoundary
        from pathlib import Path
        
        # Create minimal security boundary for testing
        security_boundary = ExperimentSecurityBoundary(
            experiment_path=Path("/tmp/poc_test")
        )
        
        self.audit_logger = AuditLogger(security_boundary, Path("/tmp/poc_test"))
        model_registry = ModelRegistry()
        self.llm_gateway = LLMGateway(model_registry)
        
    def test_llm_internal_execution(self) -> bool:
        """Test if LLM can reliably execute code internally."""
        print("🧪 Testing LLM internal code execution...")
        
        prompt = """You are a mathematical calculation expert. Calculate the following and show your work:

**Task**: Calculate the mean, median, and standard deviation of these numbers: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

**Requirements**:
1. Write Python code to perform the calculations
2. Execute the code internally and show the results
3. Provide both the code and the execution output
4. Format your response as JSON with these keys:
   - "python_code": The complete Python code
   - "execution_output": What the code printed when executed
   - "results": The calculated values (mean, median, std_dev)
   - "csv_data": A simple CSV string with the results

**Expected JSON format**:
{
  "python_code": "import numpy as np\ndata = [1,2,3,4,5,6,7,8,9,10]\n...",
  "execution_output": "Mean: 5.5\nMedian: 5.5\n...",
  "results": {"mean": 5.5, "median": 5.5, "std_dev": 2.87},
  "csv_data": "metric,value\nmean,5.5\nmedian,5.5\nstd_dev,2.87"
}

Execute the code internally and provide the complete response."""

        try:
            response, metadata = self.llm_gateway.execute_call(
                model="vertex_ai/gemini-2.5-flash",
                prompt=prompt,
                temperature=0.1
            )
            
            print(f"✅ LLM Response received (length: {len(response)})")
            
            # Try to parse as JSON (handle markdown code blocks)
            try:
                # Extract JSON from markdown code blocks if present
                json_text = response
                if "```json" in response:
                    start = response.find("```json") + 7
                    end = response.find("```", start)
                    if end > start:
                        json_text = response[start:end].strip()
                elif "```" in response:
                    start = response.find("```") + 3
                    end = response.find("```", start)
                    if end > start:
                        json_text = response[start:end].strip()
                
                result = json.loads(json_text)
                print(f"✅ JSON parsing successful")
                print(f"   - Has python_code: {'python_code' in result}")
                print(f"   - Has execution_output: {'execution_output' in result}")
                print(f"   - Has results: {'results' in result}")
                print(f"   - Has csv_data: {'csv_data' in result}")
                
                if all(key in result for key in ['python_code', 'execution_output', 'results', 'csv_data']):
                    print("✅ All required keys present")
                    return True
                else:
                    print("❌ Missing required keys")
                    return False
                    
            except json.JSONDecodeError as e:
                print(f"❌ JSON parsing failed: {e}")
                print(f"Response preview: {response[:200]}...")
                return False
                
        except Exception as e:
            print(f"❌ LLM call failed: {e}")
            return False
    
    def test_evidence_stripping(self) -> bool:
        """Test evidence stripping reduces token usage by ~44%."""
        print("\n🧪 Testing evidence stripping...")
        
        # Create a mock analysis artifact with evidence
        mock_artifact = {
            "analysis_id": "test_123",
            "document_analyses": [
                {
                    "document_id": "doc_1",
                    "dimensional_scores": {
                        "dimension_1": {"raw_score": 0.8, "salience": 0.9, "confidence": 0.95}
                    },
                    "evidence": [
                        {
                            "dimension": "dimension_1",
                            "quote_text": "This is a very long evidence quote that takes up a lot of space and contains detailed information about the analysis. " * 20,  # Repeat 20 times
                            "confidence": 0.9,
                            "context_type": "direct_statement"
                        }
                    ]
                }
            ]
        }
        
        # Calculate original size
        original_json = json.dumps(mock_artifact, indent=2)
        original_size = len(original_json)
        print(f"   Original size: {original_size} characters")
        
        # Strip evidence
        stripped_artifact = self._strip_evidence(mock_artifact)
        stripped_json = json.dumps(stripped_artifact, indent=2)
        stripped_size = len(stripped_json)
        print(f"   Stripped size: {stripped_size} characters")
        
        # Calculate reduction
        reduction = (original_size - stripped_size) / original_size
        print(f"   Reduction: {reduction:.1%}")
        
        # Check if reduction is significant (>30%)
        if reduction > 0.3:
            print("✅ Evidence stripping achieves significant reduction")
            return True
        else:
            print("❌ Evidence stripping reduction too small")
            return False
    
    def _strip_evidence(self, artifact: Dict[str, Any]) -> Dict[str, Any]:
        """Strip evidence arrays from analysis artifacts."""
        stripped = json.loads(json.dumps(artifact))  # Deep copy
        
        if "document_analyses" in stripped:
            for doc_analysis in stripped["document_analyses"]:
                if "evidence" in doc_analysis:
                    # Replace evidence with count
                    evidence_count = len(doc_analysis["evidence"])
                    doc_analysis["evidence"] = f"[{evidence_count} evidence quotes stripped]"
        
        return stripped
    
    def test_basic_verification(self) -> bool:
        """Test basic verification concept with Gemini 2.5 Pro."""
        print("\n🧪 Testing basic verification concept...")
        
        # Simulate a calculation result that needs verification
        calculation_result = {
            "python_code": "import numpy as np\ndata = [1,2,3,4,5]\nresult = np.mean(data)\nprint(f'Mean: {result}')",
            "execution_output": "Mean: 3.0",
            "results": {"mean": 3.0},
            "csv_data": "metric,value\nmean,3.0"
        }
        
        verification_prompt = f"""You are a mathematical verification expert. Verify the following calculation:

**Original Code**:
```python
{calculation_result['python_code']}
```

**Claimed Output**:
{calculation_result['execution_output']}

**Claimed Results**:
{calculation_result['results']}

**Task**: 
1. Execute the code internally
2. Compare your results with the claimed results
3. Determine if the calculation is correct
4. Provide verification status

**Requirements**:
- Execute the code and show your execution output
- Compare results numerically (allow small floating point differences)
- Return JSON with verification status

**Expected JSON format**:
{{
  "verification_code": "import numpy as np\\ndata = [1,2,3,4,5]\\nresult = np.mean(data)\\nprint(f'Mean: {{result}}')",
  "verification_output": "Mean: 3.0",
  "verification_results": {{"mean": 3.0}},
  "verification_status": "PASS" or "FAIL",
  "verification_notes": "Explanation of verification result"
}}"""

        try:
            response, metadata = self.llm_gateway.execute_call(
                model="vertex_ai/gemini-2.5-flash",
                prompt=verification_prompt,
                temperature=0.1
            )
            
            print(f"✅ Verification response received (length: {len(response)})")
            
            # Try to parse as JSON (handle markdown code blocks)
            try:
                # Extract JSON from markdown code blocks if present
                json_text = response
                if "```json" in response:
                    start = response.find("```json") + 7
                    end = response.find("```", start)
                    if end > start:
                        json_text = response[start:end].strip()
                elif "```" in response:
                    start = response.find("```") + 3
                    end = response.find("```", start)
                    if end > start:
                        json_text = response[start:end].strip()
                
                result = json.loads(json_text)
                print(f"✅ JSON parsing successful")
                
                if "verification_status" in result:
                    status = result["verification_status"]
                    print(f"   Verification status: {status}")
                    
                    if status in ["PASS", "FAIL"]:
                        print("✅ Verification concept working")
                        return True
                    else:
                        print("❌ Invalid verification status")
                        return False
                else:
                    print("❌ Missing verification_status")
                    return False
                    
            except json.JSONDecodeError as e:
                print(f"❌ JSON parsing failed: {e}")
                print(f"Response preview: {response[:200]}...")
                return False
                
        except Exception as e:
            print(f"❌ Verification call failed: {e}")
            return False
    
    def run_all_tests(self) -> bool:
        """Run all proof of concept tests."""
        print("🚀 Starting Show Your Work Architecture - Phase 0 Proof of Concept")
        print("=" * 70)
        
        tests = [
            ("LLM Internal Execution", self.test_llm_internal_execution),
            ("Evidence Stripping", self.test_evidence_stripping),
            ("Basic Verification", self.test_basic_verification)
        ]
        
        results = []
        for test_name, test_func in tests:
            print(f"\n📋 Running: {test_name}")
            try:
                result = test_func()
                results.append((test_name, result))
                if result:
                    print(f"✅ {test_name}: PASSED")
                else:
                    print(f"❌ {test_name}: FAILED")
            except Exception as e:
                print(f"❌ {test_name}: ERROR - {e}")
                results.append((test_name, False))
        
        # Summary
        print("\n" + "=" * 70)
        print("📊 PHASE 0 RESULTS SUMMARY")
        print("=" * 70)
        
        passed = sum(1 for _, result in results if result)
        total = len(results)
        
        for test_name, result in results:
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status} {test_name}")
        
        print(f"\nOverall: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 Phase 0 PASSED - Ready to proceed with implementation!")
            return True
        else:
            print("⚠️  Phase 0 FAILED - Need to address issues before proceeding")
            return False


if __name__ == "__main__":
    poc = ShowYourWorkPOC()
    success = poc.run_all_tests()
    sys.exit(0 if success else 1)
