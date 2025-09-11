
Copyright (C) 2025  Discernus Team

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

import unittest
import json
from pathlib import Path
import sys
import os

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from discernus.agents.thin_synthesis.orchestration.pipeline import ProductionThinSynthesisPipeline, ProductionPipelineRequest
from discernus.core.local_artifact_storage import LocalArtifactStorage
from discernus.core.audit_logger import AuditLogger
from .generate_data import generate_synthetic_corpus, generate_synthetic_analysis_output

class TestLargeScaleSynthesis(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Generate synthetic data once for all tests."""
        cls.test_dir = Path(__file__).parent
        os.makedirs(cls.test_dir / "artifacts", exist_ok=True)
        
        cls.corpus = generate_synthetic_corpus(num_documents=500)
        cls.scores_artifact_content, cls.evidence_artifact_content = generate_synthetic_analysis_output(cls.corpus)

        # Initialize infrastructure
        from discernus.core.security_boundary import ExperimentSecurityBoundary
        # Create a dummy security boundary for the test
        cls.security_boundary = ExperimentSecurityBoundary(cls.test_dir)
        cls.artifact_storage = LocalArtifactStorage(
            security_boundary=cls.security_boundary,
            run_folder=cls.test_dir
        )
        cls.audit_logger = AuditLogger(
            security_boundary=cls.security_boundary,
            run_folder=cls.test_dir
        )
        
        # Store artifacts
        cls.scores_hash = cls.artifact_storage.put_artifact(json.dumps(cls.scores_artifact_content).encode('utf-8'))
        cls.evidence_hash = cls.artifact_storage.put_artifact(json.dumps(cls.evidence_artifact_content).encode('utf-8'))

    def test_end_to_end_large_scale_synthesis(self):
        """
        Validates the full synthesis pipeline with a 500-document synthetic corpus.
        This test is the Definition of Done for the Intelligent Evidence Retrieval epic.
        """
        pipeline = ProductionThinSynthesisPipeline(
            artifact_client=self.artifact_storage,
            audit_logger=self.audit_logger,
            model="vertex_ai/gemini-2.5-flash" 
        )

        framework_spec = """
        # Framework: Synthetic Populism Analysis
        This framework analyzes text for populist and integrity rhetoric.
        """

        request = ProductionPipelineRequest(
            framework_spec=framework_spec,
            scores_artifact_hash=self.scores_hash,
            evidence_artifact_hash=self.evidence_hash,
            experiment_context="A large-scale test of the synthesis pipeline."
        )

        # Execute the pipeline
        response = pipeline.run(request)

        # 1. Assert successful completion
        self.assertTrue(response.success, f"Pipeline failed with message: {response.error_message}")
        
        # 2. Assert that a raw curation artifact was generated
        self.assertIsNotNone(response.curated_evidence_hash)
        curation_artifact_content = self.artifact_storage.get_artifact(response.curated_evidence_hash).decode('utf-8')
        curation_data = json.loads(curation_artifact_content)
        raw_curation = curation_data.get("raw_llm_curation")
        
        self.assertIsNotNone(raw_curation)
        self.assertGreater(len(raw_curation), 10, "The curation should contain some content")
        
        # Check that curation summary indicates some findings were processed
        curation_summary = curation_data.get("curation_summary", {})
        findings_summarized = curation_summary.get("findings_summarized", 0)
        self.assertGreater(findings_summarized, 0, "At least one finding should have been summarized")

        # 3. Assert that the final report was generated successfully
        self.assertIsNotNone(response.narrative_report)
        self.assertGreater(len(response.narrative_report), 100)
        
        print("\n--- Large Scale Synthesis Test Passed ---")
        print(f"Final Narrative Report Preview:\n{response.narrative_report[:500]}...")
        print("\n--- Raw LLM Curation Preview ---")
        print(f"{raw_curation[:1000]}...")


if __name__ == "__main__":
    unittest.main()
