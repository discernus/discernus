import re
import unittest
from pathlib import Path

class TestCsvExtraction(unittest.TestCase):
    def setUp(self):
        self.prototype_dir = Path(__file__).parent
        self.synthetic_responses_dir = self.prototype_dir / "synthetic_framework_responses"

    def _extract_embedded_csv(self, analysis_response: str, artifact_id: str) -> tuple[str, str]:
        """Extracts pre-formatted CSV segments from an LLM response."""
        
        scores_pattern = r"<<<DISCERNUS_SCORES_CSV_v1>>>(.*?)<<<END_DISCERNUS_SCORES_CSV_v1>>>"
        scores_match = re.search(scores_pattern, analysis_response, re.DOTALL)
        scores_csv = scores_match.group(1).strip() if scores_match else ""
        
        evidence_pattern = r"<<<DISCERNUS_EVIDENCE_CSV_v1>>>(.*?)<<<END_DISCERNUS_EVIDENCE_CSV_v1>>>"
        evidence_match = re.search(evidence_pattern, analysis_response, re.DOTALL)
        evidence_csv = evidence_match.group(1).strip() if evidence_match else ""
        
        # Replace placeholder with actual artifact ID
        scores_csv = scores_csv.replace("{artifact_id}", artifact_id)
        evidence_csv = evidence_csv.replace("{artifact_id}", artifact_id)
        
        return scores_csv, evidence_csv

    def test_extracts_from_caf_response(self):
        """Ensures CSV segments are correctly extracted from a CAF-style response."""
        caf_response_path = self.synthetic_responses_dir / "caf_response.txt"
        with open(caf_response_path, "r") as f:
            caf_response = f.read()

        artifact_id = "caf_artifact_123"
        scores_csv, evidence_csv = self._extract_embedded_csv(caf_response, artifact_id)

        # Verify Scores CSV
        self.assertIn("aid,dignity,tribalism", scores_csv)
        self.assertIn(f"{artifact_id},0.8,0.2", scores_csv)
        self.assertNotIn("{artifact_id}", scores_csv)

        # Verify Evidence CSV
        self.assertIn("aid,dimension,quote_id,quote_text,context_type", evidence_csv)
        self.assertIn(f"{artifact_id},dignity,1,", evidence_csv)
        self.assertNotIn("{artifact_id}", evidence_csv)

    def test_extracts_from_bef_response(self):
        """Ensures the same logic works for a different framework schema (BEF)."""
        bef_response_path = self.synthetic_responses_dir / "bef_response.txt"
        with open(bef_response_path, "r") as f:
            bef_response = f.read()

        artifact_id = "bef_artifact_456"
        scores_csv, evidence_csv = self._extract_embedded_csv(bef_response, artifact_id)

        # Verify Scores CSV - note the different column names
        self.assertIn("aid,transparency,accountability", scores_csv)
        self.assertIn(f"{artifact_id},0.9,0.75", scores_csv)
        self.assertNotIn("{artifact_id}", scores_csv)

        # Verify Evidence CSV
        self.assertIn("aid,dimension,quote_id,quote_text,context_type", evidence_csv)
        self.assertIn(f"{artifact_id},transparency,1,", evidence_csv)
        self.assertNotIn("{artifact_id}", evidence_csv)

    def test_handles_missing_sections_gracefully(self):
        """Ensures that if a section is missing, it returns an empty string."""
        response_missing_evidence = """
        <<<DISCERNUS_SCORES_CSV_v1>>>
        aid,score1
        {artifact_id},0.5
        <<<END_DISCERNUS_SCORES_CSV_v1>>>
        """
        artifact_id = "missing_sections_789"
        scores_csv, evidence_csv = self._extract_embedded_csv(response_missing_evidence, artifact_id)

        self.assertIn(f"{artifact_id},0.5", scores_csv)
        self.assertEqual(evidence_csv, "")

if __name__ == "__main__":
    unittest.main() 