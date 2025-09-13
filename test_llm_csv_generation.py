#!/usr/bin/env python3
"""
Test LLM CSV Generation Capability
==================================

Tests the core assumption that LLMs can generate both analysis responses
AND CSV data in a single operation, with the agent saving both to disk.
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


class LLMCSVGenerationTest:
    """Test LLM's ability to generate both analysis and CSV in one operation."""
    
    def __init__(self):
        # Create test environment
        test_dir = Path("/tmp/llm_csv_test")
        test_dir.mkdir(exist_ok=True)
        (test_dir / "experiment.md").write_text("# LLM CSV Generation Test")
        
        security_boundary = ExperimentSecurityBoundary(experiment_path=test_dir)
        self.audit_logger = AuditLogger(security_boundary, test_dir)
        model_registry = ModelRegistry()
        self.llm_gateway = LLMGateway(model_registry)
        
    def test_analysis_with_csv_generation(self) -> bool:
        """Test: LLM generates both analysis response AND CSV data in single operation."""
        print("🧪 Testing LLM analysis + CSV generation...")
        
        # Test data
        test_documents = [
            "This is a positive statement about the topic",
            "This is a negative statement about the topic", 
            "This is a neutral statement about the topic"
        ]
        
        prompt = """You are an analysis agent. Analyze these documents and generate both an analysis report AND CSV data.

**Documents to analyze:**
1. "This is a positive statement about the topic"
2. "This is a negative statement about the topic"
3. "This is a neutral statement about the topic"

**Your Tasks:**
1. Analyze each document for sentiment (score 0.0-1.0)
2. Calculate derived metrics (average, variance, range)
3. Generate a comprehensive analysis report
4. Generate CSV data with the results

**Output Format:**
Please provide your response in this exact format:

## ANALYSIS REPORT
[Your detailed analysis here - include scores, calculations, methodology, etc.]

## CSV DATA
[Your CSV data here - include headers and all the data]

**Important**: 
- Generate BOTH the analysis report AND the CSV data
- Use whatever format feels natural for the analysis
- Use proper CSV format for the data
- Include all necessary information in both sections"""

        try:
            print("   📞 Calling LLM for analysis + CSV generation...")
            response, metadata = self.llm_gateway.execute_call(
                model="vertex_ai/gemini-2.5-flash",
                prompt=prompt,
                temperature=0.1
            )
            
            print(f"   ✅ LLM response received ({len(response)} chars)")
            print(f"   📝 Response preview: {response[:100]}...")
            
            # Save raw response
            raw_file = Path("/tmp/llm_csv_test/raw_analysis.txt")
            raw_file.write_text(response)
            print(f"   💾 Raw response saved to {raw_file}")
            
            # Parse the response to extract CSV data
            csv_data = self._extract_csv_from_response(response)
            if csv_data:
                # Save CSV data
                csv_file = Path("/tmp/llm_csv_test/analysis_data.csv")
                csv_file.write_text(csv_data)
                print(f"   💾 CSV data saved to {csv_file}")
                print(f"   📊 CSV preview: {csv_data[:200]}...")
                
                # Verify CSV format
                if self._validate_csv_format(csv_data):
                    print("   ✅ CSV format validation passed")
                    return True
                else:
                    print("   ❌ CSV format validation failed")
                    return False
            else:
                print("   ❌ No CSV data found in response")
                return False
                
        except Exception as e:
            print(f"   ❌ Analysis + CSV generation failed: {e}")
            return False
    
    def test_statistical_analysis_with_csv(self) -> bool:
        """Test: LLM generates statistical analysis AND statistical CSV in single operation."""
        print("\n🧪 Testing LLM statistical analysis + CSV generation...")
        
        # Mock analysis data (what would come from analysis phase)
        mock_analysis_data = """
## Document Analysis Results

### Document 1: "Positive statement"
- Sentiment Score: 0.8
- Confidence: 0.9

### Document 2: "Negative statement"  
- Sentiment Score: 0.2
- Confidence: 0.85

### Document 3: "Neutral statement"
- Sentiment Score: 0.5
- Confidence: 0.7

### Derived Metrics:
- Average Sentiment: 0.5
- Sentiment Variance: 0.09
- Sentiment Range: 0.6
"""
        
        prompt = f"""You are a statistical analysis agent. Analyze this data and generate both statistical analysis AND CSV data.

**Analysis Data to Process:**
{mock_analysis_data}

**Your Tasks:**
1. Perform statistical analysis on the sentiment scores
2. Calculate additional statistical measures (mean, median, std dev, etc.)
3. Generate a comprehensive statistical report
4. Generate CSV data with all the statistical results

**Output Format:**
Please provide your response in this exact format:

## STATISTICAL ANALYSIS REPORT
[Your detailed statistical analysis here - include calculations, methodology, results, etc.]

## STATISTICAL CSV DATA
[Your CSV data here - include headers and all statistical results]

**Important**: 
- Generate BOTH the statistical analysis AND the CSV data
- Use proper statistical methodology
- Use proper CSV format for the data
- Include all necessary statistical measures"""

        try:
            print("   📞 Calling LLM for statistical analysis + CSV generation...")
            response, metadata = self.llm_gateway.execute_call(
                model="vertex_ai/gemini-2.5-flash",
                prompt=prompt,
                temperature=0.1
            )
            
            print(f"   ✅ LLM response received ({len(response)} chars)")
            print(f"   📝 Response preview: {response[:100]}...")
            
            # Save raw response
            raw_file = Path("/tmp/llm_csv_test/raw_statistical.txt")
            raw_file.write_text(response)
            print(f"   💾 Raw response saved to {raw_file}")
            
            # Parse the response to extract CSV data
            csv_data = self._extract_csv_from_response(response)
            if csv_data:
                # Save CSV data
                csv_file = Path("/tmp/llm_csv_test/statistical_data.csv")
                csv_file.write_text(csv_data)
                print(f"   💾 CSV data saved to {csv_file}")
                print(f"   📊 CSV preview: {csv_data[:200]}...")
                
                # Verify CSV format
                if self._validate_csv_format(csv_data):
                    print("   ✅ CSV format validation passed")
                    return True
                else:
                    print("   ❌ CSV format validation failed")
                    return False
            else:
                print("   ❌ No CSV data found in response")
                return False
                
        except Exception as e:
            print(f"   ❌ Statistical analysis + CSV generation failed: {e}")
            return False
    
    def test_derived_metrics_with_csv(self) -> bool:
        """Test: LLM generates derived metrics calculation AND CSV in single operation."""
        print("\n🧪 Testing LLM derived metrics + CSV generation...")
        
        # Mock dimensional scores (what would come from analysis)
        mock_scores = {
            "document_1": {"tribal_dominance": 0.9, "populist_rhetoric": 0.8, "us_vs_them": 0.7},
            "document_2": {"tribal_dominance": 0.3, "populist_rhetoric": 0.4, "us_vs_them": 0.2},
            "document_3": {"tribal_dominance": 0.6, "populist_rhetoric": 0.5, "us_vs_them": 0.6}
        }
        
        prompt = f"""You are a derived metrics agent. Calculate derived metrics from these dimensional scores and generate both analysis AND CSV data.

**Dimensional Scores:**
{mock_scores}

**Your Tasks:**
1. Calculate derived metrics for each dimension (average, variance, range, etc.)
2. Calculate cross-dimensional metrics (correlations, composite scores, etc.)
3. Generate a comprehensive derived metrics report
4. Generate CSV data with all the derived metrics

**Output Format:**
Please provide your response in this exact format:

## DERIVED METRICS REPORT
[Your detailed derived metrics analysis here - include calculations, methodology, results, etc.]

## DERIVED METRICS CSV DATA
[Your CSV data here - include headers and all derived metrics results]

**Important**: 
- Generate BOTH the derived metrics analysis AND the CSV data
- Use proper mathematical methodology
- Use proper CSV format for the data
- Include all necessary derived metrics"""

        try:
            print("   📞 Calling LLM for derived metrics + CSV generation...")
            response, metadata = self.llm_gateway.execute_call(
                model="vertex_ai/gemini-2.5-flash",
                prompt=prompt,
                temperature=0.1
            )
            
            print(f"   ✅ LLM response received ({len(response)} chars)")
            print(f"   📝 Response preview: {response[:100]}...")
            
            # Save raw response
            raw_file = Path("/tmp/llm_csv_test/raw_derived_metrics.txt")
            raw_file.write_text(response)
            print(f"   💾 Raw response saved to {raw_file}")
            
            # Parse the response to extract CSV data
            csv_data = self._extract_csv_from_response(response)
            if csv_data:
                # Save CSV data
                csv_file = Path("/tmp/llm_csv_test/derived_metrics_data.csv")
                csv_file.write_text(csv_data)
                print(f"   💾 CSV data saved to {csv_file}")
                print(f"   📊 CSV preview: {csv_data[:200]}...")
                
                # Verify CSV format
                if self._validate_csv_format(csv_data):
                    print("   ✅ CSV format validation passed")
                    return True
                else:
                    print("   ❌ CSV format validation failed")
                    return False
            else:
                print("   ❌ No CSV data found in response")
                return False
                
        except Exception as e:
            print(f"   ❌ Derived metrics + CSV generation failed: {e}")
            return False
    
    def _extract_csv_from_response(self, response: str) -> str:
        """Extract CSV data from LLM response."""
        lines = response.split('\n')
        csv_lines = []
        in_csv_section = False
        in_code_block = False
        
        for line in lines:
            if line.strip().startswith('## CSV DATA') or line.strip().startswith('## STATISTICAL CSV DATA') or line.strip().startswith('## DERIVED METRICS CSV DATA'):
                in_csv_section = True
                continue
            elif line.strip().startswith('## '):
                in_csv_section = False
                in_code_block = False
                continue
            elif in_csv_section and line.strip():
                # Handle markdown code blocks
                if line.strip().startswith('```csv') or line.strip().startswith('```'):
                    in_code_block = True
                    continue
                elif line.strip().startswith('```'):
                    in_code_block = False
                    continue
                elif in_code_block or not line.strip().startswith('```'):
                    csv_lines.append(line)
        
        return '\n'.join(csv_lines).strip()
    
    def _validate_csv_format(self, csv_data: str) -> bool:
        """Basic CSV format validation."""
        if not csv_data:
            return False
        
        lines = csv_data.strip().split('\n')
        if len(lines) < 2:  # Need at least header + 1 data row
            return False
        
        # Check that all lines have similar structure (comma-separated)
        for line in lines:
            if line.strip() and ',' not in line:
                return False
        
        return True
    
    def run_all_tests(self) -> bool:
        """Run all LLM CSV generation tests."""
        print("🚀 Starting LLM CSV Generation Tests")
        print("=" * 60)
        
        tests = [
            ("Analysis + CSV Generation", self.test_analysis_with_csv_generation),
            ("Statistical Analysis + CSV", self.test_statistical_analysis_with_csv),
            ("Derived Metrics + CSV", self.test_derived_metrics_with_csv)
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
        print("📊 LLM CSV GENERATION TEST RESULTS")
        print("=" * 60)
        
        passed = sum(1 for _, result in results if result)
        total = len(results)
        
        for test_name, result in results:
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status} {test_name}")
        
        print(f"\nOverall: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 LLM CSV Generation VALIDATED!")
            print("   ✅ LLMs can generate both analysis and CSV in single operation")
            print("   ✅ Agent can save both outputs to disk")
            print("   ✅ CSV format validation works")
            return True
        else:
            print("⚠️  LLM CSV Generation needs refinement")
            return False


if __name__ == "__main__":
    test = LLMCSVGenerationTest()
    success = test.run_all_tests()
    sys.exit(0 if success else 1)
