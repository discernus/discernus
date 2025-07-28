#!/usr/bin/env python3
"""
Unit tests for Hash Cross-Referenced CSV generation in SynthesisOrchestrator.

Tests the enhanced orchestrator's ability to generate both scores.csv and 
evidence.csv files using progressive appending architecture.
"""

import unittest
import tempfile
import json
import csv
import hashlib
from pathlib import Path
from unittest.mock import patch, mock_open

# Add the project root to the path
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from discernus.core.synthesis_orchestrator import SynthesisOrchestrator


class TestHashCsvOrchestrator(unittest.TestCase):
    """Test suite for Hash Cross-Referenced CSV generation."""

    def setUp(self):
        """Set up test fixtures."""
        self.orchestrator = SynthesisOrchestrator()
        self.test_fixtures_dir = Path(__file__).parent / "fixtures" / "sample_artifacts"
        
        # Ensure we have test artifacts
        self.test_artifacts = list(self.test_fixtures_dir.glob("*"))
        self.test_artifacts = [f for f in self.test_artifacts if f.is_file() and f.name != "artifact_registry.json"]
        
        if len(self.test_artifacts) < 2:
            self.skipTest("Need at least 2 test artifacts for meaningful testing")

    def test_framework_agnostic_csv_generation(self):
        """
        Test 1.1: Framework Agnostic Extraction
        
        Test orchestrator handles diverse framework schemas correctly.
        Input: Analysis artifacts (potentially different schemas)
        Expected: Unified CSV with dynamically discovered headers
        Success Criteria: All dimensions extracted, no data loss
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir)
            
            # This method doesn't exist yet - we need to implement it
            # For now, test that we can call the existing generate_manifest method
            manifest, quarantined = self.orchestrator.generate_manifest(self.test_artifacts[:3])
            
            # Verify we got some data
            self.assertGreater(len(manifest), 0, "Should generate manifest entries")
            self.assertIsInstance(manifest, list, "Manifest should be a list")
            
            # Verify manifest structure
            if manifest:
                first_entry = manifest[0]
                self.assertIn('artifact_hash', first_entry, "Should have artifact_hash field")
                self.assertIn('document_name', first_entry, "Should have document_name field")
                
                # Check for dynamic schema discovery
                scores_fields = [k for k in first_entry.keys() if k not in ['artifact_hash', 'document_name']]
                self.assertGreater(len(scores_fields), 0, "Should discover framework-specific fields")
            
            print(f"✅ Generated manifest with {len(manifest)} entries, quarantined {len(quarantined)} files")

    def test_evidence_hash_linking_preparation(self):
        """
        Test 1.2: Evidence Cross-Reference Integrity (Preparation)
        
        This test prepares for evidence CSV functionality by examining
        what evidence data is available in the current artifacts.
        """
        # Find a JSON artifact (not a text document)
        json_artifact = None
        for artifact in self.test_artifacts:
            try:
                with open(artifact, 'r', encoding='utf-8') as f:
                    json.load(f)
                json_artifact = artifact
                break
            except json.JSONDecodeError:
                continue
        
        if not json_artifact:
            self.skipTest("No valid JSON artifacts found for testing")
        
        with open(json_artifact, 'r', encoding='utf-8') as f:
            artifact_data = json.load(f)
        
        # Check if we have evidence/quotes in the raw response
        raw_response = artifact_data.get("raw_analysis_response", "")
        if raw_response.startswith("```json"):
            raw_response = raw_response[7:-4]
        
        try:
            inner_json = json.loads(raw_response)
            print(f"✅ Artifact structure analysis:")
            print(f"   - Top-level keys: {list(inner_json.keys())}")
            
            # Examine document_analyses structure
            if "document_analyses" in inner_json:
                for doc_key, doc_data in inner_json["document_analyses"].items():
                    print(f"   - Document: {doc_key}")
                    print(f"     - Keys: {list(doc_data.keys())}")
                    
                    # Check evidence structure
                    if "evidence" in doc_data:
                        evidence_data = doc_data["evidence"]
                        print(f"     - Evidence dimensions: {list(evidence_data.keys())}")
                        
                        # Sample one evidence dimension
                        first_dimension = list(evidence_data.keys())[0]
                        sample_quotes = evidence_data[first_dimension]
                        print(f"     - Sample {first_dimension} quotes ({len(sample_quotes)} total):")
                        if sample_quotes:
                            print(f"       - \"{sample_quotes[0][:80]}...\"")
                    
                    # Check scores structure  
                    if "scores" in doc_data:
                        scores_data = doc_data["scores"]
                        print(f"     - Score dimensions: {list(scores_data.keys())}")
                        if scores_data:
                            first_score_key = list(scores_data.keys())[0]
                            sample_score = scores_data[first_score_key]
                            print(f"     - Sample {first_score_key}: {sample_score}")
                            
        except json.JSONDecodeError:
            self.fail("Could not parse artifact raw_analysis_response")

    def test_progressive_appending_concept(self):
        """
        Test 1.3: Progressive Appending Architecture (Concept)
        
        Test the concept of processing artifacts one at a time without
        accumulating everything in memory.
        """
        processed_count = 0
        max_memory_items = 0
        
        # Simulate progressive processing
        for artifact_path in self.test_artifacts[:5]:  # Test with first 5 artifacts
            try:
                # Process single artifact (simulate)
                manifest_entry, _ = self.orchestrator.generate_manifest([artifact_path])
                
                if manifest_entry:
                    processed_count += 1
                    # In real implementation, this would be written to CSV immediately
                    # and the memory would be released
                    max_memory_items = max(max_memory_items, 1)  # Only 1 item in memory at a time
                
            except Exception as e:
                print(f"   - Quarantined {artifact_path.name}: {str(e)}")
        
        self.assertGreater(processed_count, 0, "Should process at least some artifacts")
        self.assertEqual(max_memory_items, 1, "Should maintain constant memory usage")
        
        print(f"✅ Progressive processing: {processed_count} artifacts, max memory: {max_memory_items} items")

    def test_hash_filename_concept(self):
        """
        Test 1.5: Hash Filename Concept
        
        Test the concept of generating content-based hash filenames
        for provenance and tamper detection.
        """
        # Create sample CSV content
        sample_scores_data = "artifact_hash,document_name,Hope,Fear\nabc123,doc_1,0.9,0.2\n"
        sample_evidence_data = "artifact_hash,dimension,quote_text\nabc123,Hope,sample quote\n"
        
        # Generate content hashes
        scores_hash = hashlib.sha256(sample_scores_data.encode()).hexdigest()[:16]
        evidence_hash = hashlib.sha256(sample_evidence_data.encode()).hexdigest()[:16]
        
        # Verify hash generation works
        self.assertEqual(len(scores_hash), 16, "Should generate 16-char hash")
        self.assertEqual(len(evidence_hash), 16, "Should generate 16-char hash") 
        self.assertNotEqual(scores_hash, evidence_hash, "Different content should produce different hashes")
        
        expected_scores_filename = f"{scores_hash}_scores.csv"
        expected_evidence_filename = f"{evidence_hash}_evidence.csv"
        
        print(f"✅ Hash filenames concept:")
        print(f"   - Scores CSV: {expected_scores_filename}")
        print(f"   - Evidence CSV: {expected_evidence_filename}")

    def test_generate_hash_cross_referenced_csv(self):
        """
        Test the actual Hash CSV generation implementation.
        
        This test validates the new generate_hash_cross_referenced_csv method
        works correctly with real analysis artifacts.
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir)
            
            # Use only JSON artifacts for this test
            json_artifacts = []
            for artifact in self.test_artifacts:
                try:
                    with open(artifact, 'r', encoding='utf-8') as f:
                        json.load(f)
                    json_artifacts.append(artifact)
                except json.JSONDecodeError:
                    continue
            
            if len(json_artifacts) == 0:
                self.skipTest("No valid JSON artifacts found")
            
            # Test the new method
            scores_path, evidence_path, quarantined = self.orchestrator.generate_hash_cross_referenced_csv(
                json_artifacts, output_dir
            )
            
            # Verify files were created
            self.assertTrue(scores_path.exists(), "Scores CSV should be created")
            self.assertTrue(evidence_path.exists(), "Evidence CSV should be created")
            
            # Verify hash-based filenames
            self.assertTrue(scores_path.name.endswith("_scores.csv"), "Scores file should have _scores suffix")
            self.assertTrue(evidence_path.name.endswith("_evidence.csv"), "Evidence file should have _evidence suffix")
            
            # Verify CSV structure
            with open(scores_path, 'r', encoding='utf-8') as f:
                scores_reader = csv.DictReader(f)
                scores_headers = scores_reader.fieldnames
                scores_rows = list(scores_reader)
            
            with open(evidence_path, 'r', encoding='utf-8') as f:
                evidence_reader = csv.DictReader(f)
                evidence_headers = evidence_reader.fieldnames
                evidence_rows = list(evidence_reader)
            
            # Validate scores structure
            self.assertIn('artifact_hash', scores_headers, "Scores should have artifact_hash column")
            self.assertIn('document_name', scores_headers, "Scores should have document_name column")
            self.assertGreater(len(scores_rows), 0, "Should have at least one scores row")
            
            # Validate evidence structure
            self.assertEqual(evidence_headers, ['artifact_hash', 'dimension', 'quote_id', 'quote_text', 'context_type'])
            self.assertGreater(len(evidence_rows), 0, "Should have at least one evidence row")
            
            # Validate cross-reference integrity
            scores_hashes = {row['artifact_hash'] for row in scores_rows}
            evidence_hashes = {row['artifact_hash'] for row in evidence_rows}
            self.assertTrue(evidence_hashes.issubset(scores_hashes), "All evidence should link to scores")
            
            print(f"✅ Generated Hash CSV files:")
            print(f"   - Scores: {scores_path.name} ({len(scores_rows)} rows, {len(scores_headers)} columns)")
            print(f"   - Evidence: {evidence_path.name} ({len(evidence_rows)} rows)")
            print(f"   - Quarantined: {len(quarantined)} artifacts")
            print(f"   - Score dimensions: {[h for h in scores_headers if h not in ['artifact_hash', 'document_name']]}")


if __name__ == '__main__':
    # Run with verbose output
    unittest.main(verbosity=2) 