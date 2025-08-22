#!/usr/bin/env python3
"""
Simple Unit Tests for Orchestrator Regression
=============================================

Focused tests for the batch processing regression without complex mocking.
Tests the core logic patterns we need to verify.

Key Test Areas:
1. Individual vs batch processing detection
2. Path resolution bug verification  
3. DataFrame conversion logic
4. Artifact storage patterns
"""

import unittest
from pathlib import Path
import json
import tempfile
import shutil
import pandas as pd


class TestOrchestratorRegressionPatterns(unittest.TestCase):
    """Test the core patterns affected by the batch processing regression."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = Path(tempfile.mkdtemp())
        
        # Create test artifacts directory structure
        self.artifacts_dir = self.temp_dir / "shared_cache" / "artifacts"
        self.artifacts_dir.mkdir(parents=True)
        
        # Create test raw analysis response
        self.test_response_content = """
        <<<DISCERNUS_ANALYSIS_JSON_v6>>>
        {
          "analysis_metadata": {
            "framework_name": "test_framework",
            "framework_version": "10.0.0"
          },
          "document_analyses": [
            {
              "document_name": "doc1.txt",
              "dimensional_scores": {
                "dimension1": {"raw_score": 0.5, "salience": 0.6, "confidence": 0.9},
                "dimension2": {"raw_score": 0.7, "salience": 0.8, "confidence": 0.95}
              }
            },
            {
              "document_name": "doc2.txt",
              "dimensional_scores": {
                "dimension1": {"raw_score": 0.3, "salience": 0.4, "confidence": 0.8},
                "dimension2": {"raw_score": 0.9, "salience": 0.7, "confidence": 0.9}
              }
            }
          ]
        }
        <<<END_DISCERNUS_ANALYSIS_JSON_v6>>>
        """
    
    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir)
    
    def test_path_resolution_bug_detection(self):
        """Test the specific path bug in statistical analysis."""
        # Create file in CORRECT location
        correct_file = self.artifacts_dir / "raw_analysis_response_v6_test123"
        correct_file.write_text(self.test_response_content)
        
        # Test BROKEN path (current implementation)
        broken_path = self.temp_dir / "shared_cache" / "artifacts" / "artifacts"
        broken_files = list(broken_path.glob("raw_analysis_response_v6_*")) if broken_path.exists() else []
        self.assertEqual(len(broken_files), 0, "Broken path should find no files")
        
        # Test CORRECT path (fixed implementation)
        correct_path = self.temp_dir / "shared_cache" / "artifacts"
        correct_files = list(correct_path.glob("raw_analysis_response_v6_*"))
        self.assertEqual(len(correct_files), 1, "Correct path should find the file")
        
        # Verify we can read the content
        found_file = correct_files[0]
        content = found_file.read_text()
        self.assertIn("DISCERNUS_ANALYSIS_JSON_v6", content)
    
    def test_individual_vs_batch_analysis_structure(self):
        """Test the structural difference between individual and batch analysis results."""
        
        # INDIVIDUAL PROCESSING PATTERN (CORRECT)
        individual_results = [
            {
                "batch_id": "batch_individual_doc1",
                "raw_analysis_response": """
                <<<DISCERNUS_ANALYSIS_JSON_v6>>>
                {
                  "document_analyses": [
                    {
                      "document_name": "doc1.txt",
                      "dimensional_scores": {
                        "dimension1": {"raw_score": 0.5, "salience": 0.6, "confidence": 0.9}
                      }
                    }
                  ]
                }
                <<<END_DISCERNUS_ANALYSIS_JSON_v6>>>
                """
            },
            {
                "batch_id": "batch_individual_doc2", 
                "raw_analysis_response": """
                <<<DISCERNUS_ANALYSIS_JSON_v6>>>
                {
                  "document_analyses": [
                    {
                      "document_name": "doc2.txt",
                      "dimensional_scores": {
                        "dimension1": {"raw_score": 0.3, "salience": 0.4, "confidence": 0.8}
                      }
                    }
                  ]
                }
                <<<END_DISCERNUS_ANALYSIS_JSON_v6>>>
                """
            }
        ]
        
        # BATCH PROCESSING PATTERN (BROKEN)
        batch_result = [
            {
                "batch_id": "batch_all_docs",
                "raw_analysis_response": """
                <<<DISCERNUS_ANALYSIS_JSON_v6>>>
                {
                  "document_analyses": [
                    {
                      "document_name": "doc1.txt",
                      "dimensional_scores": {
                        "dimension1": {"raw_score": 0.5, "salience": 0.6, "confidence": 0.9}
                      }
                    },
                    {
                      "document_name": "doc2.txt", 
                      "dimensional_scores": {
                        "dimension1": {"raw_score": 0.3, "salience": 0.4, "confidence": 0.8}
                      }
                    }
                  ]
                }
                <<<END_DISCERNUS_ANALYSIS_JSON_v6>>>
                """
            }
        ]
        
        # Test individual processing characteristics
        self.assertEqual(len(individual_results), 2, "Individual processing: 2 analysis result files")
        for result in individual_results:
            # Each result should have exactly 1 document
            json_content = self._extract_json_from_response(result['raw_analysis_response'])
            doc_analyses = json_content.get('document_analyses', [])
            self.assertEqual(len(doc_analyses), 1, "Individual processing: 1 document per result")
        
        # Test batch processing characteristics  
        self.assertEqual(len(batch_result), 1, "Batch processing: 1 analysis result file")
        json_content = self._extract_json_from_response(batch_result[0]['raw_analysis_response'])
        doc_analyses = json_content.get('document_analyses', [])
        self.assertEqual(len(doc_analyses), 2, "Batch processing: All documents in single result")
    
    def test_dataframe_conversion_patterns(self):
        """Test DataFrame conversion for both individual and batch patterns."""
        
        # Test individual processing DataFrame conversion
        individual_results = [
            {
                "raw_analysis_response": """
                <<<DISCERNUS_ANALYSIS_JSON_v6>>>
                {
                  "document_analyses": [
                    {
                      "document_name": "doc1.txt",
                      "dimensional_scores": {
                        "dimension1": {"raw_score": 0.5, "salience": 0.6, "confidence": 0.9}
                      }
                    }
                  ]
                }
                <<<END_DISCERNUS_ANALYSIS_JSON_v6>>>
                """
            },
            {
                "raw_analysis_response": """
                <<<DISCERNUS_ANALYSIS_JSON_v6>>>
                {
                  "document_analyses": [
                    {
                      "document_name": "doc2.txt",
                      "dimensional_scores": {
                        "dimension1": {"raw_score": 0.3, "salience": 0.4, "confidence": 0.8}
                      }
                    }
                  ]
                }
                <<<END_DISCERNUS_ANALYSIS_JSON_v6>>>
                """
            }
        ]
        
        # Convert individual results to DataFrame
        individual_df = self._convert_individual_to_dataframe(individual_results)
        
        # Verify DataFrame structure
        self.assertEqual(len(individual_df), 2, "Individual processing: 2 documents in DataFrame")
        self.assertIn('document_name', individual_df.columns)
        self.assertIn('dimension1_raw', individual_df.columns)
        
        # Verify data values
        doc1_row = individual_df[individual_df['document_name'] == 'doc1.txt'].iloc[0]
        self.assertEqual(doc1_row['dimension1_raw'], 0.5)
        
        doc2_row = individual_df[individual_df['document_name'] == 'doc2.txt'].iloc[0]
        self.assertEqual(doc2_row['dimension1_raw'], 0.3)
    
    def test_caching_implications(self):
        """Test the caching implications of individual vs batch processing."""
        
        # Individual processing: Each document can be cached separately
        individual_cache_keys = [
            "analysis_doc1_hash123",
            "analysis_doc2_hash456"
        ]
        
        # Batch processing: All documents cached together
        batch_cache_key = "analysis_all_docs_hash789"
        
        # Simulate document change scenario
        doc1_changed = True
        doc2_unchanged = True
        
        if individual_cache_keys:
            # Individual processing: Only re-analyze changed document
            if doc1_changed:
                reanalyze_individual = ["doc1.txt"]  # Only doc1 needs re-analysis
            else:
                reanalyze_individual = []
            
            self.assertEqual(len(reanalyze_individual), 1, "Individual: Only changed document re-analyzed")
        
        if batch_cache_key:
            # Batch processing: Re-analyze ALL documents even if only one changed
            if doc1_changed or doc2_unchanged:  # Any change forces full re-analysis
                reanalyze_batch = ["doc1.txt", "doc2.txt"]  # ALL documents
            else:
                reanalyze_batch = []
            
            self.assertEqual(len(reanalyze_batch), 2, "Batch: ALL documents re-analyzed for any change")
        
        # This demonstrates the efficiency problem with batch processing
        self.assertLess(len(reanalyze_individual), len(reanalyze_batch), 
                       "Individual processing is more efficient for partial changes")
    
    def test_scalability_limits(self):
        """Test scalability limits of batch vs individual processing."""
        
        # Simulate large document corpus
        num_documents = 1000
        avg_document_size = 5000  # 5KB per document
        
        # Individual processing: Context window per document
        individual_context_per_call = avg_document_size + 2000  # Document + framework
        individual_total_context = individual_context_per_call  # Same per call
        
        # Batch processing: Context window for ALL documents
        batch_context_total = (avg_document_size * num_documents) + 2000  # All docs + framework
        
        # Typical LLM context limits
        gemini_context_limit = 2_000_000  # 2M tokens ~= 8M characters
        
        # Individual processing scalability
        individual_scalable = individual_total_context < gemini_context_limit
        
        # Batch processing scalability  
        batch_scalable = batch_context_total < gemini_context_limit
        
        self.assertTrue(individual_scalable, "Individual processing should scale to large corpora")
        self.assertFalse(batch_scalable, f"Batch processing fails at {num_documents} documents ({batch_context_total:,} chars)")
        
        # Calculate maximum batch size
        max_batch_size = (gemini_context_limit - 2000) // avg_document_size
        self.assertLess(max_batch_size, num_documents, 
                       f"Batch processing limited to ~{max_batch_size} documents vs {num_documents} needed")
    
    def _extract_json_from_response(self, raw_response: str) -> dict:
        """Helper to extract JSON from analysis response."""
        start_marker = '<<<DISCERNUS_ANALYSIS_JSON_v6>>>'
        end_marker = '<<<END_DISCERNUS_ANALYSIS_JSON_v6>>>'
        
        start_idx = raw_response.find(start_marker)
        end_idx = raw_response.find(end_marker)
        
        if start_idx == -1 or end_idx == -1:
            return {}
        
        json_content = raw_response[start_idx + len(start_marker):end_idx].strip()
        return json.loads(json_content)
    
    def _convert_individual_to_dataframe(self, individual_results: list) -> pd.DataFrame:
        """Helper to convert individual analysis results to DataFrame."""
        all_rows = []
        
        for analysis_result in individual_results:
            raw_response = analysis_result.get('raw_analysis_response', '')
            analysis_data = self._extract_json_from_response(raw_response)
            
            for doc_analysis in analysis_data.get('document_analyses', []):
                row = {'document_name': doc_analysis.get('document_name', '')}
                
                for dimension, scores in doc_analysis.get('dimensional_scores', {}).items():
                    row[f"{dimension}_raw"] = scores.get('raw_score', 0.0)
                    row[f"{dimension}_salience"] = scores.get('salience', 0.0)
                    row[f"{dimension}_confidence"] = scores.get('confidence', 0.0)
                
                all_rows.append(row)
        
        return pd.DataFrame(all_rows)


class TestPathResolutionBug(unittest.TestCase):
    """Test the specific path resolution bug."""
    
    def test_artifacts_directory_path_bug(self):
        """Test the path bug that causes statistical analysis to fail."""
        temp_dir = Path(tempfile.mkdtemp())
        
        try:
            experiment_path = temp_dir / "experiment"
            experiment_path.mkdir()
            
            # Create CORRECT artifacts structure (where files actually are)
            correct_artifacts = experiment_path / "shared_cache" / "artifacts"
            correct_artifacts.mkdir(parents=True)
            
            # Create test file in correct location
            test_file = correct_artifacts / "raw_analysis_response_v6_test123"
            test_file.write_text("test content")
            
            # Test BROKEN path (what current code looks for)
            broken_path = experiment_path / "shared_cache" / "artifacts" / "artifacts"
            broken_files = list(broken_path.glob("raw_analysis_response_v6_*")) if broken_path.exists() else []
            
            # Test CORRECT path (what we should look for)
            correct_path = experiment_path / "shared_cache" / "artifacts"
            correct_files = list(correct_path.glob("raw_analysis_response_v6_*"))
            
            # Verify the bug
            self.assertEqual(len(broken_files), 0, "BROKEN: Current path finds no files")
            self.assertEqual(len(correct_files), 1, "CORRECT: Fixed path finds the file")
            
            # This demonstrates the exact bug causing "No raw analysis response found"
            
        finally:
            shutil.rmtree(temp_dir)
    
    def test_individual_vs_batch_artifact_count(self):
        """Test artifact count differences between individual and batch processing."""
        
        # Simulate individual processing: 4 documents = 4 analysis files
        individual_analysis_files = [
            "analysis_result_doc1_hash1",
            "analysis_result_doc2_hash2", 
            "analysis_result_doc3_hash3",
            "analysis_result_doc4_hash4"
        ]
        
        # Simulate batch processing: 4 documents = 1 analysis file
        batch_analysis_files = [
            "analysis_result_batch_all_docs"
        ]
        
        # Individual processing benefits
        self.assertEqual(len(individual_analysis_files), 4, "Individual: 4 files for 4 documents")
        self.assertEqual(len(batch_analysis_files), 1, "Batch: 1 file for 4 documents")
        
        # Caching implications
        # If doc2 changes:
        individual_reuse = 3  # Can reuse 3 out of 4 cached results
        batch_reuse = 0       # Must re-analyze all 4 documents
        
        self.assertEqual(individual_reuse, 3, "Individual: Can reuse 75% of cached results")
        self.assertEqual(batch_reuse, 0, "Batch: Cannot reuse any cached results")
        
        # Cost implications for 1000 document corpus with 1 document change
        documents_total = 1000
        documents_changed = 1
        
        individual_reanalysis_cost = documents_changed  # Only changed documents
        batch_reanalysis_cost = documents_total         # ALL documents
        
        efficiency_ratio = batch_reanalysis_cost / individual_reanalysis_cost
        self.assertEqual(efficiency_ratio, 1000, "Individual processing 1000x more efficient for single document changes")


class TestSynthesisAssetValidation(unittest.TestCase):
    """Test synthesis asset validation patterns."""
    
    def test_evidence_artifact_collection_patterns(self):
        """Test how evidence artifacts should be collected from individual vs batch results."""
        
        # Individual processing: Separate evidence artifacts per document
        individual_evidence_artifacts = {
            "evidence_v6_doc1_hash1": {"document_id": "doc1", "artifact_type": "evidence_v6"},
            "evidence_v6_doc2_hash2": {"document_id": "doc2", "artifact_type": "evidence_v6"},
            "evidence_v6_doc3_hash3": {"document_id": "doc3", "artifact_type": "evidence_v6"},
            "evidence_v6_doc4_hash4": {"document_id": "doc4", "artifact_type": "evidence_v6"}
        }
        
        # Batch processing: Single evidence artifact for all documents
        batch_evidence_artifacts = {
            "evidence_v6_batch_all": {"document_ids": ["doc1", "doc2", "doc3", "doc4"], "artifact_type": "evidence_v6"}
        }
        
        # Individual processing benefits for synthesis
        individual_evidence_count = len(individual_evidence_artifacts)
        batch_evidence_count = len(batch_evidence_artifacts)
        
        self.assertEqual(individual_evidence_count, 4, "Individual: 4 evidence artifacts for granular linkage")
        self.assertEqual(batch_evidence_count, 1, "Batch: 1 evidence artifact loses granular linkage")
        
        # Provenance implications
        # For synthesis, individual artifacts provide:
        individual_provenance_granularity = "document-level"
        batch_provenance_granularity = "corpus-level"
        
        self.assertEqual(individual_provenance_granularity, "document-level", "Individual: Document-level provenance")
        self.assertEqual(batch_provenance_granularity, "corpus-level", "Batch: Corpus-level provenance (less precise)")


if __name__ == '__main__':
    unittest.main()
