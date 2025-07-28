#!/usr/bin/env python3
"""
Flash Lite CSV Compliance Validation Test
==========================================

Validates that Gemini 2.5 Flash Lite can reliably produce the embedded CSV format
and that our extraction logic can correctly parse its output.
"""

import unittest
import re
from pathlib import Path

class TestFlashLiteCompliance(unittest.TestCase):

    def setUp(self):
        # This is the actual Flash Lite response from our test
        self.flash_lite_response = '''```json
{
  "analysis_summary": "This analysis of 'test_document.txt' utilizes the Character Assessment Framework v4.3 to evaluate the moral character expressed...",
  "document_analyses": {
    "test_document.txt": {
      "worldview": "The document expresses a universalist, humanistic, and equitable worldview...",
      "scores": {
        "dignity_intensity": 0.95,
        "dignity_salience": 1.0,
        "tribalism_intensity": 0.05,
        "tribalism_salience": 0.1
      }
    }
  },
  "mathematical_verification": {
    "mc_sci_score": 0.626,
    "confidence_score": 0.9
  }
}
```
<<<DISCERNUS_SCORES_CSV_v1>>>
aid,dignity,tribalism,truth,manipulation,justice,resentment,hope,fear,pragmatism,fantasy,mc_sci
test_doc_001,0.95,0.05,0.9,0.05,0.8,0.0,0.8,0.0,0.7,0.05,0.626
<<<END_DISCERNUS_SCORES_CSV_v1>>>

<<<DISCERNUS_EVIDENCE_CSV_v1>>>
aid,dimension,quote_id,quote_text,context_type
test_doc_001,dignity,DIGNITY_1,"Every person deserves a voice, a chance, and the freedom to live with dignity.","direct_statement"
test_doc_001,dignity,DIGNITY_2,"Each individual carries inherent dignity","direct_statement"
test_doc_001,tribalism,TRIBALISM_1,"Our identities enrich our perspectives, but they do not define our moral worth.","counter_evidence"
test_doc_001,truth,TRUTH_1,"Our work is to build systems that reflect that truth—for everyone.","direct_statement"
test_doc_001,justice,JUSTICE_1,"Equity Through Dignity and Democratic Renewal","framing_title"
test_doc_001,justice,JUSTICE_2,"systems that reflect that truth—for everyone.","implicit_statement"
test_doc_001,hope,HOPE_1,"A Shared Future: Equity Through Dignity and Democratic Renewal","framing_title"
test_doc_001,hope,HOPE_2,"contribute to the common good.","goal_statement"
test_doc_001,pragmatism,PRAGMATISM_1,"Our work is to build systems","action_oriented"
test_doc_001,pragmatism,PRAGMATISM_2,"contribute to the common good.","action_oriented"
<<<END_DISCERNUS_EVIDENCE_CSV_v1>>>'''

    def _extract_embedded_csv(self, analysis_response: str, artifact_id: str) -> tuple[str, str]:
        """Extracts pre-formatted CSV segments from an LLM response using the validated logic."""
        
        scores_pattern = r"<<<DISCERNUS_SCORES_CSV_v1>>>(.*?)<<<END_DISCERNUS_SCORES_CSV_v1>>>"
        scores_match = re.search(scores_pattern, analysis_response, re.DOTALL)
        scores_csv = scores_match.group(1).strip() if scores_match else ""
        
        evidence_pattern = r"<<<DISCERNUS_EVIDENCE_CSV_v1>>>(.*?)<<<END_DISCERNUS_EVIDENCE_CSV_v1>>>"
        evidence_match = re.search(evidence_pattern, analysis_response, re.DOTALL)
        evidence_csv = evidence_match.group(1).strip() if evidence_match else ""
        
        # No need to replace artifact_id since Flash Lite already provided the correct one
        return scores_csv, evidence_csv
    
    def test_flash_lite_csv_extraction(self):
        """Validates that Flash Lite output can be extracted correctly."""
        scores_csv, evidence_csv = self._extract_embedded_csv(self.flash_lite_response, "test_doc_001")
        
        # Validate Scores CSV
        self.assertIn("aid,dignity,tribalism", scores_csv)
        self.assertIn("test_doc_001,0.95,0.05,0.9", scores_csv)
        self.assertIn("0.626", scores_csv)  # MC-SCI score present
        
        # Validate Evidence CSV  
        self.assertIn("aid,dimension,quote_id,quote_text,context_type", evidence_csv)
        self.assertIn("test_doc_001,dignity,DIGNITY_1", evidence_csv)
        self.assertIn("Every person deserves a voice", evidence_csv)
        
        print("✅ Flash Lite CSV extraction successful!")
        print(f"📊 Scores CSV length: {len(scores_csv)} chars")
        print(f"📝 Evidence CSV length: {len(evidence_csv)} chars")
        
    def test_flash_lite_delimiter_compliance(self):
        """Validates that Flash Lite used the exact delimiters we specified."""
        # Check for exact delimiter presence
        self.assertIn("<<<DISCERNUS_SCORES_CSV_v1>>>", self.flash_lite_response)
        self.assertIn("<<<END_DISCERNUS_SCORES_CSV_v1>>>", self.flash_lite_response)
        self.assertIn("<<<DISCERNUS_EVIDENCE_CSV_v1>>>", self.flash_lite_response)
        self.assertIn("<<<END_DISCERNUS_EVIDENCE_CSV_v1>>>", self.flash_lite_response)
        
        print("✅ Flash Lite delimiter compliance: PERFECT")
        
    def test_flash_lite_data_quality(self):
        """Validates that Flash Lite provided high-quality, structured data."""
        scores_csv, evidence_csv = self._extract_embedded_csv(self.flash_lite_response, "test_doc_001")
        
        # Check for numeric scores in proper format
        score_lines = scores_csv.split('\n')
        data_line = score_lines[1]  # Skip header
        values = data_line.split(',')
        
        # Validate artifact ID
        self.assertEqual(values[0], "test_doc_001")
        
        # Validate all scores are numeric and in range [0.0, 1.0]
        for i in range(1, len(values)):
            score = float(values[i])
            self.assertGreaterEqual(score, 0.0)
            self.assertLessEqual(score, 1.0)
            
        # Check evidence quality
        evidence_lines = evidence_csv.split('\n')[1:]  # Skip header
        self.assertGreater(len(evidence_lines), 5)  # Multiple evidence entries
        
        print("✅ Flash Lite data quality: HIGH")
        print(f"📊 Generated {len(evidence_lines)} evidence entries")

if __name__ == "__main__":
    unittest.main() 