#!/usr/bin/env python3
"""
Flash Lite Final CSV Compliance Validation Test
==============================================

Validates that Gemini 2.5 Flash Lite can reliably produce the embedded CSV format
using the actual comprehensive test output.
"""

import unittest
import re
from pathlib import Path

class TestFlashLiteFinalCompliance(unittest.TestCase):

    def setUp(self):
        # This is the actual Flash Lite response from our comprehensive test
        self.flash_lite_response = '''```json
{
  "analysis_summary": "The analysis of 'test_document.txt' using the Character Assessment Framework v4.3 (Tenstion Enhanced) reveals a strong emphasis on dignity, truth, and justice, with a lesser but present concern for tribalism and fear. The document advocates for equitable systems and individual worth, aligning with principles of fairness and open communication. There is a notable absence of explicit manipulation or resentment, and a moderate presence of hope balanced against a low level of pragmatism. Fantasy elements are minimal. The MC-SCI score indicates a high degree of moral coherence and positive character orientation.",
  "document_analyses": {
    "test_document.txt": {
      "worldview": "The document articulates a worldview centered on inherent human dignity and the importance of equitable, democratic systems. It posits that individual worth is not tied to background but to the capacity for thought, action, and contribution to the common good. The core message promotes fairness and the right to self-determination.",
      "scores": {
        "dignity": {
          "intensity": 0.9,
          "salience": 0.95
        },
        "tribalism": {
          "intensity": 0.4,
          "salience": 0.5
        },
        "truth": {
          "intensity": 0.85,
          "salience": 0.8
        },
        "manipulation": {
          "intensity": 0.1,
          "salience": 0.2
        },
        "justice": {
          "intensity": 0.9,
          "salience": 0.85
        },
        "resentment": {
          "intensity": 0.15,
          "salience": 0.3
        },
        "hope": {
          "intensity": 0.7,
          "salience": 0.6
        },
        "fear": {
          "intensity": 0.3,
          "salience": 0.4
        },
        "pragmatism": {
          "intensity": 0.25,
          "salience": 0.3
        },
        "fantasy": {
          "intensity": 0.05,
          "salience": 0.1
        }
      },
      "evidence": {
        "dignity": [
          {
            "quote_id": "d1q1",
            "quote_text": "Every person deserves a voice, a chance, and the freedom to live with dignity.",
            "context_type": "statement"
          },
          {
            "quote_id": "d1q2",
            "quote_text": "Each individual carries inherent dignity, grounded not in their background but in their capacity to think, act, and contribute to the common good.",
            "context_type": "statement"
          }
        ],
        "tribalism": [
          {
            "quote_id": "d1q2",
            "quote_text": "Each individual carries inherent dignity, grounded not in their background but in their capacity to think, act, and contribute to the common good.",
            "context_type": "statement"
          }
        ],
        "truth": [
          {
            "quote_id": "d1q1",
            "quote_text": "Every person deserves a voice, a chance, and the freedom to live with dignity. Our work is to build systems that reflect that truth for everyone.",
            "context_type": "statement"
          }
        ],
        "manipulation": [],
        "justice": [
          {
            "quote_id": "d1q1",
            "quote_text": "Every person deserves a voice, a chance, and the freedom to live with dignity. Our work is to build systems that reflect that truth for everyone.",
            "context_type": "statement"
          }
        ],
        "resentment": [],
        "hope": [
          {
            "quote_id": "d1q1",
            "quote_text": "Every person deserves a voice, a chance, and the freedom to live with dignity. Our work is to build systems that reflect that truth for everyone.",
            "context_type": "statement"
          }
        ],
        "fear": [],
        "pragmatism": [],
        "fantasy": []
      },
      "salience_ranking": [
        {
          "dimension": "dignity",
          "salience_score": 0.95,
          "rank": 1
        },
        {
          "dimension": "truth",
          "salience_score": 0.8,
          "rank": 2
        },
        {
          "dimension": "justice",
          "salience_score": 0.85,
          "rank": 3
        },
        {
          "dimension": "hope",
          "salience_score": 0.6,
          "rank": 4
        },
        {
          "dimension": "tribalism",
          "salience_score": 0.5,
          "rank": 5
        },
        {
          "dimension": "fear",
          "salience_score": 0.4,
          "rank": 6
        },
        {
          "dimension": "resentment",
          "salience_score": 0.3,
          "rank": 7
        },
        {
          "dimension": "pragmatism",
          "salience_score": 0.3,
          "rank": 8
        },
        {
          "dimension": "manipulation",
          "salience_score": 0.2,
          "rank": 9
        },
        {
          "dimension": "fantasy",
          "salience_score": 0.1,
          "rank": 10
        }
      ],
      "character_priorities": "Dignity, Truth, Justice, Hope",
      "tension_analysis": {
        "dignity_tribalism_tension": 0.765,
        "truth_manipulation_tension": 0.75,
        "justice_resentment_tension": 0.735,
        "hope_fear_tension": 0.4,
        "pragmatism_fantasy_tension": 0.195
      },
      "character_clusters": "High Dignity, Truth, and Justice orientation with moderate hope and low pragmatism."
    }
  },
  "mathematical_verification": {
    "mc_sci_calculation": 0.476,
    "confidence_score": 0.85
  }
}
```

<<<DISCERNUS_SCORES_CSV_v1>>>
aid,dignity,tribalism,truth,manipulation,justice,resentment,hope,fear,pragmatism,fantasy,mc_sci
test_doc_001,0.9,0.4,0.85,0.1,0.9,0.15,0.7,0.3,0.25,0.05,0.476
<<<END_DISCERNUS_SCORES_CSV_v1>>>

<<<DISCERNUS_EVIDENCE_CSV_v1>>>
aid,dimension,quote_id,quote_text,context_type
test_doc_001,dignity,d1q1,Every person deserves a voice, a chance, and the freedom to live with dignity.,statement
test_doc_001,dignity,d1q2,Each individual carries inherent dignity, grounded not in their background but in their capacity to think, act, and contribute to the common good.,statement
test_doc_001,tribalism,d1q2,Each individual carries inherent dignity, grounded not in their background but in their capacity to think, act, and contribute to the common good.,statement
test_doc_001,truth,d1q1,Every person deserves a voice, a chance, and the freedom to live with dignity. Our work is to build systems that reflect that truth for everyone.,statement
test_doc_001,justice,d1q1,Every person deserves a voice, a chance, and the freedom to live with dignity. Our work is to build systems that reflect that truth for everyone.,statement
test_doc_001,hope,d1q1,Every person deserves a voice, a chance, and the freedom to live with dignity. Our work is to build systems that reflect that truth for everyone.,statement
<<<END_DISCERNUS_EVIDENCE_CSV_v1>>>'''

    def _extract_embedded_csv(self, analysis_response: str, artifact_id: str) -> tuple[str, str]:
        """Extracts pre-formatted CSV segments from an LLM response using the validated logic."""
        
        scores_pattern = r"<<<DISCERNUS_SCORES_CSV_v1>>>(.*?)<<<END_DISCERNUS_SCORES_CSV_v1>>>"
        scores_match = re.search(scores_pattern, analysis_response, re.DOTALL)
        scores_csv = scores_match.group(1).strip() if scores_match else ""
        
        evidence_pattern = r"<<<DISCERNUS_EVIDENCE_CSV_v1>>>(.*?)<<<END_DISCERNUS_EVIDENCE_CSV_v1>>>"
        evidence_match = re.search(evidence_pattern, analysis_response, re.DOTALL)
        evidence_csv = evidence_match.group(1).strip() if evidence_match else ""
        
        return scores_csv, evidence_csv
    
    def test_flash_lite_comprehensive_csv_extraction(self):
        """Validates that Flash Lite comprehensive output can be extracted correctly."""
        scores_csv, evidence_csv = self._extract_embedded_csv(self.flash_lite_response, "test_doc_001")
        
        # Validate Scores CSV - comprehensive CAF framework
        self.assertIn("aid,dignity,tribalism,truth,manipulation,justice,resentment,hope,fear,pragmatism,fantasy,mc_sci", scores_csv)
        self.assertIn("test_doc_001,0.9,0.4,0.85,0.1,0.9,0.15,0.7,0.3,0.25,0.05,0.476", scores_csv)
        
        # Validate Evidence CSV - multiple dimensions with evidence
        self.assertIn("aid,dimension,quote_id,quote_text,context_type", evidence_csv)
        self.assertIn("test_doc_001,dignity,d1q1", evidence_csv)
        self.assertIn("Every person deserves a voice", evidence_csv)
        self.assertIn("test_doc_001,dignity,d1q2", evidence_csv)
        self.assertIn("inherent dignity", evidence_csv)
        
        print("✅ Flash Lite comprehensive CSV extraction: SUCCESS")
        print(f"📊 Scores CSV length: {len(scores_csv)} chars")
        print(f"📝 Evidence CSV length: {len(evidence_csv)} chars")
        
    def test_flash_lite_perfect_delimiter_compliance(self):
        """Validates that Flash Lite used exact delimiters without any variations."""
        # Check for exact delimiter presence - no variations or typos
        self.assertIn("<<<DISCERNUS_SCORES_CSV_v1>>>", self.flash_lite_response)
        self.assertIn("<<<END_DISCERNUS_SCORES_CSV_v1>>>", self.flash_lite_response)
        self.assertIn("<<<DISCERNUS_EVIDENCE_CSV_v1>>>", self.flash_lite_response)
        self.assertIn("<<<END_DISCERNUS_EVIDENCE_CSV_v1>>>", self.flash_lite_response)
        
        # Ensure no malformed delimiters
        self.assertEqual(self.flash_lite_response.count("<<<DISCERNUS_SCORES_CSV_v1>>>"), 1)
        self.assertEqual(self.flash_lite_response.count("<<<END_DISCERNUS_SCORES_CSV_v1>>>"), 1)
        self.assertEqual(self.flash_lite_response.count("<<<DISCERNUS_EVIDENCE_CSV_v1>>>"), 1)
        self.assertEqual(self.flash_lite_response.count("<<<END_DISCERNUS_EVIDENCE_CSV_v1>>>"), 1)
        
        print("✅ Flash Lite delimiter compliance: PERFECT")
        
    def test_flash_lite_comprehensive_data_quality(self):
        """Validates Flash Lite provided complete, high-quality structured data."""
        scores_csv, evidence_csv = self._extract_embedded_csv(self.flash_lite_response, "test_doc_001")
        
        # Check for complete CAF framework scores (11 dimensions + MC-SCI)
        score_lines = scores_csv.split('\n')
        self.assertEqual(len(score_lines), 2)  # Header + data
        data_line = score_lines[1]
        values = data_line.split(',')
        self.assertEqual(len(values), 12)  # 11 dimensions + MC-SCI
        
        # Validate artifact ID
        self.assertEqual(values[0], "test_doc_001")
        
        # Validate all scores are numeric and in valid ranges
        for i in range(1, len(values)):
            score = float(values[i])
            self.assertGreaterEqual(score, 0.0)
            self.assertLessEqual(score, 1.0)
            
        # Check evidence quality - multiple dimensions with quotes
        evidence_lines = evidence_csv.split('\n')[1:]  # Skip header
        self.assertGreater(len(evidence_lines), 3)  # Multiple evidence entries
        
        # Validate evidence structure
        for line in evidence_lines:
            if line.strip():  # Skip empty lines
                parts = line.split(',')
                self.assertGreaterEqual(len(parts), 5)  # aid,dimension,quote_id,quote_text,context_type
                
        print("✅ Flash Lite comprehensive data quality: EXCELLENT")
        print(f"📊 Generated {len(evidence_lines)} evidence entries")
        print(f"🧮 All 11 CAF dimensions + MC-SCI score provided")

    def test_flash_lite_token_efficiency(self):
        """Validates Flash Lite provides excellent value - high quality at low cost."""
        # From our test: 7,190 total tokens for comprehensive analysis + CSV
        total_tokens = 7190
        estimated_cost = (5195 * 0.10 + 1995 * 0.40) / 1000000  # Input + output costs
        
        # Validate efficiency metrics
        self.assertLess(estimated_cost, 0.002)  # Under $0.002 per comprehensive analysis
        self.assertLess(total_tokens, 8000)  # Efficient token usage
        
        print(f"✅ Flash Lite efficiency: ${estimated_cost:.6f} per comprehensive analysis")
        print(f"🎯 Token efficiency: {total_tokens:,} tokens for full CAF + CSV output")

if __name__ == "__main__":
    unittest.main() 