#!/usr/bin/env python3
"""
Test Current Framework with CSV Embedding
=======================================

Tests that our current framework can generate embedded CSV sections using
the proven prompt pattern from the prototype.
"""

import unittest
import re
from pathlib import Path
import json
from discernus.gateway.llm_gateway import LLMGateway
from discernus.gateway.model_registry import ModelRegistry

class TestCurrentFrameworkCSV(unittest.TestCase):
    
    def setUp(self):
        # Load the framework and document from the simple_test project
        self.framework_path = Path(__file__).parent.parent.parent / "projects/simple_test/framework.md"
        self.document_path = Path(__file__).parent.parent.parent / "projects/simple_test/corpus/document1.txt"
        
        with open(self.framework_path, "r") as f:
            self.framework = f.read()
            
        with open(self.document_path, "r") as f:
            self.document = f.read()
            
        # Extract the JSON appendix from the framework
        json_pattern = r"```json\n(.*?)\n```"
        json_match = re.search(json_pattern, self.framework, re.DOTALL)
        if not json_match:
            raise ValueError("No JSON appendix found in framework")
        self.framework_config = json.loads(json_match.group(1))
        
        # Get all dimensions from virtues and vices
        self.all_dimensions = (
            self.framework_config["dimension_groups"]["virtues"] +
            self.framework_config["dimension_groups"]["vices"]
        )
        
        # Build the enhanced prompt that worked in the prototype
        self.enhanced_prompt = f'''You are an enhanced computational research analysis agent. Your primary task is to perform systematic analysis that produces **STRUCTURED JSON DATA** with **EMBEDDED CSV SECTIONS** for synthesis scalability.

**CRITICAL OUTPUT REQUIREMENT: Your response must contain BOTH a JSON analysis AND embedded CSV sections using the delimiters specified below.**

**EMBEDDED CSV OUTPUT CONTRACT:**

After your standard JSON analysis, you MUST include these two CSV sections:

1. **SCORES CSV**: Contains all dimension scores for synthesis aggregation
2. **EVIDENCE CSV**: Contains key evidence quotes linked to artifact IDs for cross-referencing

**REQUIRED CSV FORMAT:**

```
<<<DISCERNUS_SCORES_CSV_v1>>>
aid,{",".join(self.all_dimensions)}
{{artifact_id}},{",".join("{{" + dim + "_score}}" for dim in self.all_dimensions)}
<<<END_DISCERNUS_SCORES_CSV_v1>>>

<<<DISCERNUS_EVIDENCE_CSV_v1>>>
aid,dimension,quote_id,quote_text,context_type
{{artifact_id}},{{dimension_name}},{{quote_number}},{{quote_text}},{{context_type}}
<<<END_DISCERNUS_EVIDENCE_CSV_v1>>>
```

**IMPORTANT**: Replace {{artifact_id}} with "document1", use actual numeric scores from your analysis, and include 1-2 strongest evidence quotes per dimension.

---

**FRAMEWORK INSTRUCTIONS:**
{self.framework}

---

**DOCUMENT TO ANALYZE:**
{self.document}

Begin enhanced analysis now. Provide the complete JSON analysis followed by the embedded CSV sections using the exact delimiters specified above.'''

        # Initialize the LLM gateway
        self.registry = ModelRegistry()
        self.gateway = LLMGateway(self.registry)

    def _extract_embedded_csv(self, analysis_response: str, artifact_id: str) -> tuple[str, str]:
        """Extracts pre-formatted CSV segments from an LLM response."""
        
        scores_pattern = r"<<<DISCERNUS_SCORES_CSV_v1>>>(.*?)<<<END_DISCERNUS_SCORES_CSV_v1>>>"
        scores_match = re.search(scores_pattern, analysis_response, re.DOTALL)
        scores_csv = scores_match.group(1).strip() if scores_match else ""
        
        evidence_pattern = r"<<<DISCERNUS_EVIDENCE_CSV_v1>>>(.*?)<<<END_DISCERNUS_EVIDENCE_CSV_v1>>>"
        evidence_match = re.search(evidence_pattern, analysis_response, re.DOTALL)
        evidence_csv = evidence_match.group(1).strip() if evidence_match else ""
        
        return scores_csv, evidence_csv
    
    def test_framework_csv_generation(self):
        """Tests that our framework can generate properly delimited CSV sections."""
        # First validate the prompt structure
        self.assertIn("CRITICAL OUTPUT REQUIREMENT", self.enhanced_prompt)
        self.assertIn("<<<DISCERNUS_SCORES_CSV_v1>>>", self.enhanced_prompt)
        self.assertIn("<<<DISCERNUS_EVIDENCE_CSV_v1>>>", self.enhanced_prompt)
        
        # Check that we included all dimensions from the framework
        for dimension in self.all_dimensions:
            self.assertIn(dimension, self.enhanced_prompt)
            
        print("✅ Enhanced prompt structure validated")
        print(f"📊 Framework dimensions included: {len(self.all_dimensions)}")
        
        # Make the actual LLM call
        response, metadata = self.gateway.execute_call(
            model="vertex_ai/gemini-2.5-flash-lite",
            prompt=self.enhanced_prompt,
            system_prompt="You are an expert research analysis agent.",
            max_retries=2
        )
        
        print("\n🤖 LLM Response Metadata:")
        print(f"Success: {metadata['success']}")
        print(f"Model: {metadata['model']}")
        print(f"Tokens: {metadata['usage']['total_tokens']}")
        
        if not metadata['success']:
            self.fail(f"LLM call failed: {metadata.get('error', 'Unknown error')}")
            
        # Extract and validate the CSV sections
        scores_csv, evidence_csv = self._extract_embedded_csv(response, "document1")
        
        # Validate that we got CSV data
        self.assertTrue(scores_csv, "No scores CSV found in response")
        self.assertTrue(evidence_csv, "No evidence CSV found in response")
        
        print("\n📊 CSV Sections Found:")
        print(f"Scores CSV length: {len(scores_csv)} chars")
        print(f"Evidence CSV length: {len(evidence_csv)} chars")
        
        # Print the actual CSV data
        print("\n📊 Scores CSV:")
        print(scores_csv)
        print("\n📝 Evidence CSV (first 500 chars):")
        print(evidence_csv[:500])
        
        # Validate CSV structure
        scores_lines = scores_csv.split('\n')
        self.assertGreater(len(scores_lines), 1, "Scores CSV should have header and data")
        
        evidence_lines = evidence_csv.split('\n')
        self.assertGreater(len(evidence_lines), 1, "Evidence CSV should have header and data")
        
        # Validate scores CSV header matches our dimensions
        scores_header = scores_lines[0].split(',')
        self.assertEqual(scores_header[0], "aid", "First column should be 'aid'")
        for i, dimension in enumerate(self.all_dimensions, 1):
            self.assertEqual(scores_header[i], dimension, f"Column {i} should be {dimension}")
            
        # Validate evidence CSV structure
        evidence_header = evidence_lines[0].split(',')
        self.assertEqual(evidence_header, ["aid", "dimension", "quote_id", "quote_text", "context_type"],
                        "Evidence CSV header mismatch")
        
        print("\n✅ CSV structure validation complete")
        
if __name__ == "__main__":
    unittest.main() 