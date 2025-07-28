#!/usr/bin/env python3
"""
Test Gauntlet for the Framework-Agile Synthesis Orchestrator
============================================================

This test suite subjects the SynthesisOrchestrator to a series of escalating
challenges to validate its robustness, scalability, and framework-agnostic
design.
"""
import unittest
import json
from pathlib import Path

from discernus.core.synthesis_orchestrator import SynthesisOrchestrator

class TestSynthesisGauntlet(unittest.TestCase):
    """A test suite for the SynthesisOrchestrator."""

    def setUp(self):
        """Set up the test environment before each test."""
        # self.orchestrator = SynthesisOrchestrator() # Remove shared instance
        self.test_data_path = Path("discernus/tests/synthesis_gauntlet/test_data")
        self.artifacts_path = self.test_data_path / "artifacts"
        self.frameworks_path = self.test_data_path / "frameworks"
        
        print("\n--- Starting Test Gauntlet ---")

    def test_hurdle_1_framework_diversity(self):
        """
        Tests the orchestrator against a small, diverse set of synthetic
        frameworks and artifacts.
        """
        print("Hurdle 1: Processing diverse synthetic artifacts...")
        
        orchestrator = SynthesisOrchestrator()
        all_artifact_paths = list(self.artifacts_path.glob("*"))
        
        manifest, quarantined = orchestrator.generate_manifest(
            artifact_paths=all_artifact_paths
        )
        
        # In the new design, it will process all valid artifacts regardless of framework
        # The schema is discovered from the first valid artifact found.
        self.assertEqual(len(manifest), 18, "Should correctly process 10 CFF + 8 PDAF artifacts")
        self.assertEqual(len(quarantined), 2, "Should quarantine only the 2 poison pills")
        
        print("Hurdle 1 Passed: Correctly handled framework diversity and quarantined failures.")

    def test_hurdle_2_production_scale(self):
        """
        Tests the orchestrator against the full set of real-world artifacts
        from the large_batch_test to ensure it can handle production scale.
        """
        print("\nHurdle 2: Processing real production artifacts at scale...")

        # Find the real framework file and all artifact files
        prod_artifacts_path = Path("projects/large_batch_test/shared_cache/artifacts")
        
        # The framework is also an artifact, identified by its hash
        # This hash is stable for the test case.
        prod_framework_path = prod_artifacts_path / "5707a64b536a57f583787976d6870ce3ed0121f143c94e6077735ab4e5b8c082"
        
        # Get all files in the directory except the artifact registry
        all_prod_artifact_paths = [p for p in prod_artifacts_path.glob("*") if p.is_file() and p.name != "artifact_registry.json"]

        orchestrator = SynthesisOrchestrator()
        manifest, quarantined = orchestrator.generate_manifest(
            artifact_paths=all_prod_artifact_paths
        )

        # We expect analysis artifacts to be processed and non-analysis files to be quarantined
        # Production data contains: 46 analysis artifacts + 48 text files + 1 synthesis artifact = 95 total
        self.assertEqual(len(manifest), 46, "Should process all 46 analysis artifacts.")
        self.assertEqual(len(quarantined), 49, "Should quarantine 48 text files + 1 synthesis artifact.")

        print(f"Hurdle 2 Passed: Successfully processed {len(manifest)} production artifacts.")
        print(f"Quarantined {len(quarantined)} non-analysis or malformed files.")


if __name__ == '__main__':
    unittest.main(verbosity=2) 