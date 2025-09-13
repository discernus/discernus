#!/usr/bin/env python3
"""
Zero Parsing Test for Show Your Work Architecture
================================================

Tests the core principle: LLMs do all processing internally, we just pass raw responses
between agents without any parsing, opening, or processing.
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from discernus.gateway.llm_gateway import LLMGateway
from discernus.gateway.model_registry import ModelRegistry
from discernus.core.audit_logger import AuditLogger
from discernus.core.security_boundary import ExperimentSecurityBoundary


class ZeroParsingTest:
    """Test zero parsing approach - raw LLM responses passed between agents."""
    
    def __init__(self):
        # Create test environment
        test_dir = Path("/tmp/zero_parsing_test")
        test_dir.mkdir(exist_ok=True)
        (test_dir / "experiment.md").write_text("# Zero Parsing Test")
        
        security_boundary = ExperimentSecurityBoundary(experiment_path=test_dir)
        self.audit_logger = AuditLogger(security_boundary, test_dir)
        model_registry = ModelRegistry()
        self.llm_gateway = LLMGateway(model_registry)
        
    def test_raw_response_flow(self) -> bool:
        """Test: Primary LLM generates response, we save it raw, verification LLM processes it raw."""
        print("🧪 Testing zero parsing flow...")
        
        # STEP 1: Primary LLM generates analysis with derived metrics
        print("   Step 1: Primary LLM generates analysis...")
        primary_prompt = """You are an analysis agent. Analyze this data and calculate derived metrics.

**Data to analyze:**
- Document 1: "This is a positive statement about the topic"
- Document 2: "This is a negative statement about the topic" 
- Document 3: "This is a neutral statement about the topic"

**Tasks:**
1. Score each document on sentiment (0.0-1.0)
2. Calculate derived metrics: average sentiment, sentiment variance
3. Execute the calculations internally
4. Return your response in whatever format you think is best

**Important**: Return your response in whatever format you prefer. Don't worry about specific JSON schemas or delimiters. Just provide the analysis and calculations in whatever format feels natural to you."""

        try:
            primary_response, primary_metadata = self.llm_gateway.execute_call(
                model="vertex_ai/gemini-2.5-flash",
                prompt=primary_prompt,
                temperature=0.1
            )
            
            print(f"   ✅ Primary LLM response received ({len(primary_response)} chars)")
            print(f"   📝 Response preview: {primary_response[:100]}...")
            
            # STEP 2: Save raw response to disk (no parsing, no processing)
            print("   Step 2: Saving raw response to disk...")
            raw_file = Path("/tmp/zero_parsing_test/primary_response.txt")
            raw_file.write_text(primary_response)
            print(f"   ✅ Raw response saved to {raw_file}")
            
            # STEP 3: Verification LLM reads raw response and verifies it
            print("   Step 3: Verification LLM processes raw response...")
            verification_prompt = f"""You are a verification agent. I'm giving you a raw response from another LLM agent. Please verify the analysis and calculations.

**Raw Response from Primary Agent:**
{primary_response}

**Your Task:**
1. Read and understand the analysis provided
2. Verify any calculations or metrics mentioned
3. Execute the calculations yourself internally
4. Compare your results with the primary agent's results
5. Provide your verification assessment

**Important**: Just provide your verification in whatever format feels natural to you. Don't worry about specific schemas."""

            verification_response, verification_metadata = self.llm_gateway.execute_call(
                model="vertex_ai/gemini-2.5-flash", 
                prompt=verification_prompt,
                temperature=0.1
            )
            
            print(f"   ✅ Verification response received ({len(verification_response)} chars)")
            print(f"   📝 Verification preview: {verification_response[:100]}...")
            
            # STEP 4: Save verification response raw (no parsing)
            print("   Step 4: Saving raw verification response...")
            verification_file = Path("/tmp/zero_parsing_test/verification_response.txt")
            verification_file.write_text(verification_response)
            print(f"   ✅ Raw verification saved to {verification_file}")
            
            # STEP 5: Final synthesis LLM processes both raw responses
            print("   Step 5: Synthesis LLM processes both raw responses...")
            synthesis_prompt = f"""You are a synthesis agent. I'm giving you two raw responses from other agents. Please synthesize them into a final report.

**Raw Primary Analysis:**
{primary_response}

**Raw Verification Response:**
{verification_response}

**Your Task:**
1. Read both responses (in whatever format they're in)
2. Extract the key findings from the primary analysis
3. Extract the verification assessment
4. Synthesize into a final report
5. Provide your synthesis in whatever format feels natural

**Important**: Just provide your synthesis in whatever format feels natural to you."""

            synthesis_response, synthesis_metadata = self.llm_gateway.execute_call(
                model="vertex_ai/gemini-2.5-flash",
                prompt=synthesis_prompt, 
                temperature=0.1
            )
            
            print(f"   ✅ Synthesis response received ({len(synthesis_response)} chars)")
            print(f"   📝 Synthesis preview: {synthesis_response[:100]}...")
            
            # STEP 6: Save final synthesis raw
            print("   Step 6: Saving raw synthesis response...")
            synthesis_file = Path("/tmp/zero_parsing_test/synthesis_response.txt")
            synthesis_file.write_text(synthesis_response)
            print(f"   ✅ Raw synthesis saved to {synthesis_file}")
            
            # Verify all files exist and have content
            files = [raw_file, verification_file, synthesis_file]
            all_exist = all(f.exists() and f.stat().st_size > 0 for f in files)
            
            if all_exist:
                print("   ✅ All raw responses saved successfully")
                print("   📊 File sizes:")
                for f in files:
                    print(f"      {f.name}: {f.stat().st_size} bytes")
                return True
            else:
                print("   ❌ Some files missing or empty")
                return False
                
        except Exception as e:
            print(f"   ❌ Zero parsing flow failed: {e}")
            return False
    
    def test_no_json_parsing(self) -> bool:
        """Test: We never parse JSON, just pass raw responses around."""
        print("\n🧪 Testing no JSON parsing...")
        
        # Create a mock "analysis" that's not JSON
        mock_analysis = """ANALYSIS REPORT
================

Document Analysis:
- Doc 1: Sentiment score = 0.8 (positive)
- Doc 2: Sentiment score = 0.2 (negative) 
- Doc 3: Sentiment score = 0.5 (neutral)

Derived Metrics:
- Average sentiment: 0.5
- Sentiment variance: 0.09
- Sentiment range: 0.6

Python code used:
```python
import numpy as np
scores = [0.8, 0.2, 0.5]
avg = np.mean(scores)
var = np.var(scores)
print(f"Average: {avg}, Variance: {var}")
```

This analysis was generated using internal code execution.
The results are mathematically sound."""

        print("   📝 Mock analysis created (not JSON format)")
        
        # Save it raw
        raw_file = Path("/tmp/zero_parsing_test/mock_analysis.txt")
        raw_file.write_text(mock_analysis)
        print(f"   ✅ Raw analysis saved to {raw_file}")
        
        # Verification LLM processes it without knowing the format
        verification_prompt = f"""You are a verification agent. Here's a raw analysis response from another agent. Please verify it.

**Raw Analysis Response:**
{mock_analysis}

**Your Task:**
1. Read and understand this analysis (whatever format it's in)
2. Verify the calculations mentioned
3. Execute the calculations yourself
4. Provide your verification assessment

**Important**: Don't worry about the format - just verify the content."""

        try:
            verification_response, _ = self.llm_gateway.execute_call(
                model="vertex_ai/gemini-2.5-flash",
                prompt=verification_prompt,
                temperature=0.1
            )
            
            print(f"   ✅ Verification processed raw response ({len(verification_response)} chars)")
            print(f"   📝 Verification preview: {verification_response[:100]}...")
            
            # Save verification raw
            verification_file = Path("/tmp/zero_parsing_test/mock_verification.txt")
            verification_file.write_text(verification_response)
            print(f"   ✅ Raw verification saved to {verification_file}")
            
            return True
            
        except Exception as e:
            print(f"   ❌ No JSON parsing test failed: {e}")
            return False
    
    def test_entropy_resilience(self) -> bool:
        """Test: System works regardless of LLM response format variations."""
        print("\n🧪 Testing entropy resilience...")
        
        # Test with different response formats
        test_cases = [
            "Simple text response",
            "```json\n{\"result\": \"value\"}\n```",
            "**Markdown** with *formatting*",
            "Plain text with numbers: 1, 2, 3",
            "Mixed format with code:\n```python\nprint('hello')\n```\nAnd text after"
        ]
        
        success_count = 0
        
        for i, test_format in enumerate(test_cases):
            print(f"   Test case {i+1}: {test_format[:30]}...")
            
            # Save raw format
            test_file = Path(f"/tmp/zero_parsing_test/entropy_test_{i}.txt")
            test_file.write_text(test_format)
            
            # Verification LLM processes it
            verification_prompt = f"""You are a verification agent. Here's a raw response from another agent. Please process it and provide verification.

**Raw Response:**
{test_format}

**Your Task:**
1. Read this response (whatever format it's in)
2. Understand what it contains
3. Provide verification assessment
4. Don't worry about parsing specific formats - just process the content

**Important**: Just provide your verification in whatever format feels natural."""

            try:
                verification_response, _ = self.llm_gateway.execute_call(
                    model="vertex_ai/gemini-2.5-flash",
                    prompt=verification_prompt,
                    temperature=0.1
                )
                
                # Save verification
                verification_file = Path(f"/tmp/zero_parsing_test/entropy_verification_{i}.txt")
                verification_file.write_text(verification_response)
                
                print(f"      ✅ Processed successfully")
                success_count += 1
                
            except Exception as e:
                print(f"      ❌ Failed: {e}")
        
        print(f"   📊 Entropy resilience: {success_count}/{len(test_cases)} cases passed")
        return success_count == len(test_cases)
    
    def run_all_tests(self) -> bool:
        """Run all zero parsing tests."""
        print("🚀 Starting Zero Parsing Architecture Tests")
        print("=" * 60)
        
        tests = [
            ("Raw Response Flow", self.test_raw_response_flow),
            ("No JSON Parsing", self.test_no_json_parsing), 
            ("Entropy Resilience", self.test_entropy_resilience)
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
        print("\n" + "=" * 60)
        print("📊 ZERO PARSING TEST RESULTS")
        print("=" * 60)
        
        passed = sum(1 for _, result in results if result)
        total = len(results)
        
        for test_name, result in results:
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status} {test_name}")
        
        print(f"\nOverall: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 Zero Parsing Architecture VALIDATED!")
            print("   ✅ No parsing needed - LLMs handle everything")
            print("   ✅ Raw responses passed between agents")
            print("   ✅ System resilient to LLM entropy")
            return True
        else:
            print("⚠️  Zero Parsing Architecture needs refinement")
            return False


if __name__ == "__main__":
    test = ZeroParsingTest()
    success = test.run_all_tests()
    sys.exit(0 if success else 1)
