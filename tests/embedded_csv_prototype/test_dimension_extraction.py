#!/usr/bin/env python3
"""
Test Framework-Agnostic Dimension Extraction
=========================================

Tests that our dimension extraction and CSV validation works with any v5.0 framework.
"""

import unittest
import json
import re
from pathlib import Path
from discernus.gateway.llm_gateway import LLMGateway
from discernus.gateway.model_registry import ModelRegistry

class TestDimensionExtraction(unittest.TestCase):
    
    def setUp(self):
        # Load a few different v5.0 frameworks for testing
        self.frameworks_dir = Path(__file__).parent.parent.parent / "frameworks"
        self.frameworks = {
            "caf": self.frameworks_dir / "reference/core/caf_v5.0.md",
            "chf": self.frameworks_dir / "reference/core/chf_v5.0.md",
            "ecf": self.frameworks_dir / "reference/core/ecf_v5.0.md"
        }
        
        # Initialize LLM gateway for validation tests
        self.registry = ModelRegistry()
        self.gateway = LLMGateway(self.registry)
    
    def _extract_json_appendix(self, framework_content: str) -> dict:
        """Extract and parse JSON appendix from framework markdown."""
        json_pattern = r"```json\n(.*?)\n```"
        json_match = re.search(json_pattern, framework_content, re.DOTALL)
        if not json_match:
            raise ValueError("No JSON appendix found in framework")
        return json.loads(json_match.group(1))
    
    def _extract_dimensions(self, framework_config: dict) -> list:
        """Extract all dimensions from a framework config."""
        # Get all dimension groups
        dimension_groups = framework_config.get("dimension_groups", {})
        
        # Collect all dimensions from all groups
        all_dimensions = []
        for group_name, dimensions in dimension_groups.items():
            if isinstance(dimensions, list):
                all_dimensions.extend(dimensions)
        
        return all_dimensions
    
    def _validate_csv_structure(self, scores_csv: str, evidence_csv: str, dimensions: list) -> None:
        """Validate that CSV data matches expected structure."""
        # Validate scores CSV
        scores_lines = scores_csv.split('\n')
        self.assertGreater(len(scores_lines), 1, "Scores CSV should have header and data")
        
        scores_header = scores_lines[0].split(',')
        self.assertEqual(scores_header[0], "aid", "First column should be 'aid'")
        
        # Check all dimensions are present in header
        for i, dimension in enumerate(dimensions, 1):
            self.assertEqual(scores_header[i], dimension, 
                           f"Column {i} should be {dimension}")
        
        # Check data row has correct number of columns
        data_row = scores_lines[1].split(',')
        self.assertEqual(len(data_row), len(dimensions) + 1,
                        "Data row should have aid + all dimensions")
        
        # Validate all scores are floats between 0 and 1
        for score in data_row[1:]:
            score_float = float(score)
            self.assertGreaterEqual(score_float, 0.0, "Scores must be >= 0.0")
            self.assertLessEqual(score_float, 1.0, "Scores must be <= 1.0")
        
        # Validate evidence CSV
        evidence_lines = evidence_csv.split('\n')
        self.assertGreater(len(evidence_lines), 1, "Evidence CSV should have header and data")
        
        evidence_header = evidence_lines[0].split(',')
        self.assertEqual(evidence_header, 
                        ["aid", "dimension", "quote_id", "quote_text", "context_type"],
                        "Evidence CSV header mismatch")
        
        # Check that evidence dimensions match framework dimensions
        evidence_dimensions = set()
        for line in evidence_lines[1:]:
            if line.strip():  # Skip empty lines
                parts = line.split(',')
                evidence_dimensions.add(parts[1])  # dimension is second column
        
        for dimension in dimensions:
            self.assertIn(dimension, evidence_dimensions,
                         f"Missing evidence for dimension: {dimension}")
    
    def test_dimension_extraction(self):
        """Test that dimensions are correctly extracted from any v5.0 framework."""
        for framework_name, framework_path in self.frameworks.items():
            with self.subTest(framework=framework_name):
                # Load framework
                with open(framework_path, "r") as f:
                    framework_content = f.read()
                
                # Extract and validate dimensions
                framework_config = self._extract_json_appendix(framework_content)
                dimensions = self._extract_dimensions(framework_config)
                
                # Basic validation
                self.assertGreater(len(dimensions), 0, 
                                 f"No dimensions found in {framework_name}")
                self.assertEqual(len(set(dimensions)), len(dimensions),
                               f"Duplicate dimensions found in {framework_name}")
                
                print(f"✅ {framework_name}: {len(dimensions)} dimensions extracted")
    
    def test_csv_generation(self):
        """Test that CSV generation works with any framework's dimensions."""
        # Use CAF for this test since we know it works
        with open(self.frameworks["caf"], "r") as f:
            framework_content = f.read()
        
        # Get test document
        doc_path = Path(__file__).parent.parent.parent / "projects/simple_test/corpus/document1.txt"
        with open(doc_path, "r") as f:
            document_content = f.read()
        
        # Extract dimensions
        framework_config = self._extract_json_appendix(framework_content)
        dimensions = self._extract_dimensions(framework_config)
        
        # Build the enhanced prompt
        prompt = f'''You are an enhanced computational research analysis agent. Your primary task is to perform systematic analysis that produces **STRUCTURED JSON DATA** with **EMBEDDED CSV SECTIONS** for synthesis scalability.

**CRITICAL OUTPUT REQUIREMENT: Your response must contain BOTH a JSON analysis AND embedded CSV sections using the delimiters specified below.**

**EMBEDDED CSV OUTPUT CONTRACT:**

After your standard JSON analysis, you MUST include these two CSV sections:

1. **SCORES CSV**: Contains all dimension scores for synthesis aggregation
2. **EVIDENCE CSV**: Contains key evidence quotes linked to artifact IDs for cross-referencing

**REQUIRED CSV FORMAT:**

```
<<<DISCERNUS_SCORES_CSV_v1>>>
aid,{",".join(dimensions)}
{{artifact_id}},{",".join("{{" + dim + "_score}}" for dim in dimensions)}
<<<END_DISCERNUS_SCORES_CSV_v1>>>

<<<DISCERNUS_EVIDENCE_CSV_v1>>>
aid,dimension,quote_id,quote_text,context_type
{{artifact_id}},{{dimension_name}},{{quote_number}},{{quote_text}},{{context_type}}
<<<END_DISCERNUS_EVIDENCE_CSV_v1>>>
```

**IMPORTANT**: Replace {{artifact_id}} with "test_doc_001", use actual numeric scores from your analysis, and include 1-2 strongest evidence quotes per dimension.

---

**FRAMEWORK:**
{framework_content}

---

**DOCUMENT TO ANALYZE:**
{document_content}

Begin analysis now. Provide the complete JSON analysis followed by the embedded CSV sections using the exact delimiters specified above.'''

        # Make LLM call
        response, metadata = self.gateway.execute_call(
            model="vertex_ai/gemini-2.5-flash-lite",
            prompt=prompt,
            system_prompt="You are an expert research analysis agent.",
            max_retries=2
        )
        
        print("\n🤖 LLM Response Metadata:")
        print(f"Success: {metadata['success']}")
        print(f"Model: {metadata['model']}")
        print(f"Tokens: {metadata['usage']['total_tokens']}")
        
        if not metadata['success']:
            self.fail(f"LLM call failed: {metadata.get('error', 'Unknown error')}")
        
        # Extract CSV sections
        scores_pattern = r"<<<DISCERNUS_SCORES_CSV_v1>>>(.*?)<<<END_DISCERNUS_SCORES_CSV_v1>>>"
        scores_match = re.search(scores_pattern, response, re.DOTALL)
        scores_csv = scores_match.group(1).strip() if scores_match else ""
        
        evidence_pattern = r"<<<DISCERNUS_EVIDENCE_CSV_v1>>>(.*?)<<<END_DISCERNUS_EVIDENCE_CSV_v1>>>"
        evidence_match = re.search(evidence_pattern, response, re.DOTALL)
        evidence_csv = evidence_match.group(1).strip() if evidence_match else ""
        
        # Validate CSV structure matches framework dimensions
        self._validate_csv_structure(scores_csv, evidence_csv, dimensions)
        
        print("\n✅ CSV validation complete")
        print(f"📊 {len(dimensions)} dimensions validated")
        print(f"📝 Evidence entries validated")

if __name__ == "__main__":
    unittest.main() 