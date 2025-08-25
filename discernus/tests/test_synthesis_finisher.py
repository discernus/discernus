import unittest
from pathlib import Path
import tempfile
import shutil
import json

from discernus.core.synthesis_finisher import SynthesisFinisher
from discernus.core.local_artifact_storage import LocalArtifactStorage
from discernus.core.security_boundary import ExperimentSecurityBoundary


class TestSynthesisFinisher(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.experiment_path = self.test_dir / "project"
        self.experiment_path.mkdir()
        (self.experiment_path / "experiment.md").touch()

        self.security_boundary = ExperimentSecurityBoundary(
            experiment_path=self.experiment_path
        )
        self.run_folder = self.experiment_path / "runs" / "test_run"
        self.run_folder.mkdir(parents=True)
        self.artifact_storage = LocalArtifactStorage(
            run_folder=self.run_folder, security_boundary=self.security_boundary
        )

        self.statistical_results = {
            "correlation_matrix": {
                "correlations": {
                    "fear_raw_vs_hope_raw": -0.8343240438156556,
                    "envy_raw_vs_compersion_raw": -0.9428090415820634,
                }
            },
            "descriptive_statistics": {
                "john_mccain_2008_concession.txt": {
                    "full_cohesion_index": 0.7844645260526821
                },
                "steve_king_2017_house_floor.txt": {
                    "full_cohesion_index": -0.7271074755737331
                },
            },
        }

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_finalize_report_with_valid_placeholders(self):
        draft_report = """
        The analysis revealed several key findings.
        The correlation between fear and hope was {corr(fear_raw, hope_raw)}.
        For John McCain, the Full Cohesion Index was {desc(john_mccain_2008_concession.txt, full_cohesion_index)}.
        Meanwhile, the correlation between envy and compersion stood at {corr(envy_raw, compersion_raw)}, and Steve King's
        cohesion index was {desc(steve_king_2017_house_floor.txt, full_cohesion_index)}.
        """

        finisher = SynthesisFinisher(self.statistical_results)
        final_report = finisher.finalize_report(draft_report)

        # Check that placeholders were resolved with APA-style rounding (2 decimal places)
        self.assertIn("-0.83", final_report)  # Was -0.8343240438156556
        self.assertIn("0.78", final_report)   # Was 0.7844645260526821
        self.assertIn("-0.94", final_report)  # Was -0.9428090415820634
        self.assertIn("-0.73", final_report)  # Was -0.7271074755737331

        self.assertNotIn("{corr(fear_raw, hope_raw)}", final_report)
        self.assertNotIn("{desc(john_mccain_2008_concession.txt, full_cohesion_index)}", final_report)

    def test_finalize_report_with_missing_placeholders(self):
        draft_report = """
        This report has a placeholder for a value not in the data: {corr(nonexistent_a, nonexistent_b)}.
        It also has a valid one: {corr(fear_raw, hope_raw)}.
        """
        finisher = SynthesisFinisher(self.statistical_results)
        final_report = finisher.finalize_report(draft_report)

        self.assertIn("[VALUE_NOT_FOUND:corr(nonexistent_a,nonexistent_b)]", final_report)
        self.assertIn("-0.83", final_report)  # APA-rounded from -0.8343240438156556

    def test_finalize_report_with_malformed_placeholders(self):
        draft_report = "This contains a {{malformed_placeholder}} and an {{unclosed."
        finisher = SynthesisFinisher(self.statistical_results)
        final_report = finisher.finalize_report(draft_report)

        self.assertEqual(draft_report, final_report)

    def test_finalize_report_empty_report(self):
        draft_report = ""
        finisher = SynthesisFinisher(self.statistical_results)
        final_report = finisher.finalize_report(draft_report)
        self.assertEqual("", final_report)

    def test_finalize_report_no_placeholders(self):
        draft_report = "This is a final report with no placeholders to be replaced."
        finisher = SynthesisFinisher(self.statistical_results)
        final_report = finisher.finalize_report(draft_report)
        self.assertEqual(draft_report, final_report)

if __name__ == "__main__":
    unittest.main()
