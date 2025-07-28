import unittest
import pandas as pd
from pathlib import Path
from io import StringIO
import re
import tempfile
import os

# Reusing the validated extraction logic
def extract_embedded_csv(analysis_response: str, artifact_id: str) -> tuple[str, str]:
    scores_pattern = r"<<<DISCERNUS_SCORES_CSV_v1>>>(.*?)<<<END_DISCERNUS_SCORES_CSV_v1>>>"
    scores_match = re.search(scores_pattern, analysis_response, re.DOTALL)
    scores_csv = scores_match.group(1).strip() if scores_match else ""
    
    evidence_pattern = r"<<<DISCERNUS_EVIDENCE_CSV_v1>>>(.*?)<<<END_DISCERNUS_EVIDENCE_CSV_v1>>>"
    evidence_match = re.search(evidence_pattern, analysis_response, re.DOTALL)
    evidence_csv = evidence_match.group(1).strip() if evidence_match else ""
    
    scores_csv = scores_csv.replace("{artifact_id}", artifact_id)
    evidence_csv = evidence_csv.replace("{artifact_id}", artifact_id)
    
    return scores_csv, evidence_csv

class TestStreamingCsvAggregation(unittest.TestCase):
    def setUp(self):
        self.synthetic_responses_dir = Path(__file__).parent / "synthetic_framework_responses"
        self.temp_dir = tempfile.TemporaryDirectory()
        self.scores_path = Path(self.temp_dir.name) / "scores.csv"
        self.evidence_path = Path(self.temp_dir.name) / "evidence.csv"

    def tearDown(self):
        self.temp_dir.cleanup()

    def _append_to_csv(self, file_path: Path, csv_data: str):
        """Appends a CSV string to a file, handling headers correctly."""
        if not csv_data:
            return
        
        data_df = pd.read_csv(StringIO(csv_data))
        
        # If file doesn't exist, write with header. Otherwise, append without.
        if not file_path.exists():
            data_df.to_csv(file_path, index=False)
        else:
            # Important: When appending, we need to align columns.
            # We can do this by reading the existing file and concatenating.
            # This is a bit more than a simple append, but necessary for schema changes.
            existing_df = pd.read_csv(file_path)
            combined_df = pd.concat([existing_df, data_df], ignore_index=True)
            combined_df.to_csv(file_path, index=False)


    def test_streaming_aggregation(self):
        """
        Validates a streaming approach where CSV data from different frameworks
        is incrementally appended to files on disk.
        """
        # --- Step 1: Process the first artifact (CAF) ---
        caf_response_path = self.synthetic_responses_dir / "caf_response.txt"
        with open(caf_response_path, "r") as f:
            caf_response = f.read()
        caf_scores_csv, caf_evidence_csv = extract_embedded_csv(caf_response, "caf_artifact_123")
        
        self._append_to_csv(self.scores_path, caf_scores_csv)
        self._append_to_csv(self.evidence_path, caf_evidence_csv)

        # --- Step 2: Process the second artifact (BEF) ---
        bef_response_path = self.synthetic_responses_dir / "bef_response.txt"
        with open(bef_response_path, "r") as f:
            bef_response = f.read()
        bef_scores_csv, bef_evidence_csv = extract_embedded_csv(bef_response, "bef_artifact_456")

        self._append_to_csv(self.scores_path, bef_scores_csv)
        self._append_to_csv(self.evidence_path, bef_evidence_csv)
        
        # --- Step 3: Validate the final aggregated files ---
        self.assertTrue(self.scores_path.exists())
        self.assertTrue(self.evidence_path.exists())

        # Validate final scores CSV
        final_scores_df = pd.read_csv(self.scores_path)
        self.assertEqual(len(final_scores_df), 2)
        
        caf_row = final_scores_df[final_scores_df['aid'] == 'caf_artifact_123']
        self.assertEqual(caf_row['dignity'].iloc[0], 0.8)
        self.assertTrue(pd.isna(caf_row['transparency'].iloc[0]))

        bef_row = final_scores_df[final_scores_df['aid'] == 'bef_artifact_456']
        self.assertEqual(bef_row['transparency'].iloc[0], 0.9)
        self.assertTrue(pd.isna(bef_row['dignity'].iloc[0]))
        
        print("\nValidated final aggregated scores file from streaming process:")
        print(final_scores_df.to_string())

        # Validate final evidence CSV
        final_evidence_df = pd.read_csv(self.evidence_path)
        self.assertEqual(len(final_evidence_df), 4)
        self.assertEqual(len(final_evidence_df[final_evidence_df['aid'] == 'caf_artifact_123']), 2)
        self.assertEqual(len(final_evidence_df[final_evidence_df['aid'] == 'bef_artifact_456']), 2)
        print("\nValidated final aggregated evidence file from streaming process:")
        print(final_evidence_df.to_string())


if __name__ == "__main__":
    unittest.main() 