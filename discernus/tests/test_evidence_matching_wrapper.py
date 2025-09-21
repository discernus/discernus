#!/usr/bin/env python3
"""
Unit Tests for EvidenceMatchingWrapper

Follows Test-Driven Development (TDD) methodology.
Tests Phase 1: Foundation functionality including basic txtai integration,
evidence index building, and basic search functionality.
Tests Phase 2: LLM Query Generation functionality.
"""

import unittest
import tempfile
import shutil
import json
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

from discernus.core.deprecated.evidence_matching_wrapper import EvidenceMatchingWrapper
from discernus.core.local_artifact_storage import LocalArtifactStorage
from discernus.core.security_boundary import ExperimentSecurityBoundary
from discernus.core.audit_logger import AuditLogger


class TestEvidenceMatchingWrapper(unittest.TestCase):
    """Test suite for the EvidenceMatchingWrapper."""

    def setUp(self):
        """Set up a temporary directory for artifacts."""
        self.test_dir = Path(tempfile.mkdtemp())
        
        # Create experiment structure
        (self.test_dir / "experiment.md").touch()
        self.run_folder = self.test_dir / "runs" / "test_run"
        self.run_folder.mkdir(parents=True, exist_ok=True)
        
        # Initialize infrastructure
        self.security_boundary = ExperimentSecurityBoundary(self.test_dir)
        self.artifact_storage = LocalArtifactStorage(
            security_boundary=self.security_boundary,
            run_folder=self.run_folder
        )
        self.audit_logger = AuditLogger(
            security_boundary=self.security_boundary,
            run_folder=self.run_folder
        )
        
        # Sample evidence data
        self.sample_evidence = {
            "evidence_data": [
                {
                    "quote_text": "The quick brown fox jumps over the lazy dog.",
                    "document_name": "test_doc1.txt",
                    "dimension": "test_dimension",
                    "confidence": 0.9,
                    "extraction_method": "analysis_time_extraction_v1.0",
                    "source_type": "analysis_response"
                },
                {
                    "quote_text": "A journey of a thousand miles begins with a single step.",
                    "document_name": "test_doc2.txt",
                    "dimension": "wisdom",
                    "confidence": 0.8,
                    "extraction_method": "analysis_time_extraction_v1.0",
                    "source_type": "analysis_response"
                },
                {
                    "quote_text": "Brevity is the soul of wit.",
                    "document_name": "test_doc3.txt",
                    "dimension": "wisdom",
                    "confidence": 0.95,
                    "extraction_method": "analysis_time_extraction_v1.0",
                    "source_type": "analysis_response"
                }
            ]
        }
        
        # Store sample evidence as artifact
        self.evidence_hash = self.artifact_storage.put_artifact(
            json.dumps(self.sample_evidence).encode('utf-8'),
            {"artifact_type": "evidence_database"}
        )
        
        # Initialize wrapper
        self.wrapper = EvidenceMatchingWrapper(
            model="test_model",
            artifact_storage=self.artifact_storage,
            audit_logger=self.audit_logger
        )

    def tearDown(self):
        """Clean up the temporary directory."""
        shutil.rmtree(self.test_dir)

    def test_initialization(self):
        """Test that the wrapper initializes correctly."""
        self.assertEqual(self.wrapper.model, "test_model")
        self.assertEqual(self.wrapper.artifact_storage, self.artifact_storage)
        self.assertEqual(self.wrapper.audit_logger, self.audit_logger)
        self.assertIsNone(self.wrapper.index)
        self.assertEqual(len(self.wrapper.evidence_data), 0)
        self.assertEqual(len(self.wrapper.evidence_metadata), 0)

    def test_build_index_success(self):
        """Test successful index building from evidence artifacts."""
        # Build index
        success = self.wrapper.build_index([self.evidence_hash])
        
        # Verify success
        self.assertTrue(success)
        self.assertIsNotNone(self.wrapper.index)
        self.assertEqual(len(self.wrapper.evidence_data), 3)
        self.assertEqual(self.wrapper.evidence_metadata['total_evidence_pieces'], 3)
        self.assertEqual(self.wrapper.evidence_metadata['total_artifacts_processed'], 1)

    def test_build_index_no_artifacts(self):
        """Test index building with no artifacts."""
        success = self.wrapper.build_index([])
        self.assertFalse(success)
        self.assertIsNone(self.wrapper.index)

    def test_build_index_invalid_artifact(self):
        """Test index building with invalid artifact content."""
        # Create invalid evidence artifact
        invalid_evidence = {"invalid": "structure"}
        invalid_hash = self.artifact_storage.put_artifact(
            json.dumps(invalid_evidence).encode('utf-8'),
            {"artifact_type": "evidence_database"}
        )
        
        success = self.wrapper.build_index([invalid_hash])
        self.assertFalse(success)

    def test_build_index_mixed_artifacts(self):
        """Test index building with some valid and some invalid artifacts."""
        # Create another valid evidence artifact
        additional_evidence = {
            "evidence_data": [
                {
                    "quote_text": "Additional wisdom quote.",
                    "document_name": "test_doc4.txt",
                    "dimension": "wisdom",
                    "confidence": 0.85,
                    "extraction_method": "analysis_time_extraction_v1.0",
                    "source_type": "analysis_response"
                }
            ]
        }
        additional_hash = self.artifact_storage.put_artifact(
            json.dumps(additional_evidence).encode('utf-8'),
            {"artifact_type": "evidence_database"}
        )
        
        # Build index with both valid artifacts
        success = self.wrapper.build_index([self.evidence_hash, additional_hash])
        
        self.assertTrue(success)
        self.assertEqual(len(self.wrapper.evidence_data), 4)

    def test_search_evidence_no_index(self):
        """Test evidence search when no index is built."""
        results = self.wrapper.search_evidence("test query")
        self.assertEqual(len(results), 0)

    def test_search_evidence_basic(self):
        """Test basic evidence search functionality."""
        # Build index first
        self.wrapper.build_index([self.evidence_hash])
        
        # Search for evidence
        results = self.wrapper.search_evidence("fox")
        
        # Should find the fox quote
        self.assertGreater(len(results), 0)
        fox_found = any("fox" in result["quote_text"].lower() for result in results)
        self.assertTrue(fox_found)

    def test_search_evidence_with_filters(self):
        """Test evidence search with metadata filters."""
        # Build index first
        self.wrapper.build_index([self.evidence_hash])
        
        # Search with dimension filter
        results = self.wrapper.search_evidence("wisdom", filters={"dimension": "wisdom"})
        
        # Should only return wisdom dimension evidence
        self.assertGreater(len(results), 0)
        for result in results:
            self.assertEqual(result["dimension"], "wisdom")

    def test_search_evidence_confidence_filter(self):
        """Test evidence search with confidence filters."""
        # Build index first
        self.wrapper.build_index([self.evidence_hash])
        
        # Search with confidence filter
        results = self.wrapper.search_evidence("test", filters={"confidence_min": 0.9})
        
        # Should only return high confidence evidence
        self.assertGreater(len(results), 0)
        for result in results:
            self.assertGreaterEqual(result["confidence"], 0.9)

    def test_get_evidence_by_metadata(self):
        """Test metadata-based evidence retrieval."""
        # Build index first
        self.wrapper.build_index([self.evidence_hash])
        
        # Get evidence by dimension
        results = self.wrapper.get_evidence_by_metadata({"dimension": "wisdom"})
        
        # Should return wisdom dimension evidence
        self.assertEqual(len(results), 2)
        for result in results:
            self.assertEqual(result["dimension"], "wisdom")

    def test_get_evidence_by_metadata_no_filters(self):
        """Test metadata-based evidence retrieval without filters."""
        # Build index first
        self.wrapper.build_index([self.evidence_hash])
        
        # Get evidence without filters
        results = self.wrapper.get_evidence_by_metadata({})
        
        # Should return all evidence
        self.assertEqual(len(results), 3)

    def test_get_evidence_by_metadata_confidence_range(self):
        """Test metadata-based evidence retrieval with confidence range."""
        # Build index first
        self.wrapper.build_index([self.evidence_hash])
        
        # Get evidence with confidence range
        results = self.wrapper.get_evidence_by_metadata({
            "confidence_min": 0.85,
            "confidence_max": 0.95
        })
        
        # Should return evidence in confidence range
        self.assertGreater(len(results), 0)
        for result in results:
            self.assertGreaterEqual(result["confidence"], 0.85)
            self.assertLessEqual(result["confidence"], 0.95)

    def test_get_index_status(self):
        """Test index status reporting."""
        # Check status before building index
        status = self.wrapper.get_index_status()
        self.assertFalse(status["index_built"])
        self.assertEqual(status["evidence_count"], 0)
        
        # Build index
        self.wrapper.build_index([self.evidence_hash])
        
        # Check status after building index
        status = self.wrapper.get_index_status()
        self.assertTrue(status["index_built"])
        self.assertEqual(status["evidence_count"], 3)
        self.assertEqual(status["model"], "test_model")

    def test_filter_matching(self):
        """Test filter matching logic."""
        # Build index first
        self.wrapper.build_index([self.evidence_hash])
        
        # Test various filter combinations
        test_cases = [
            ({"dimension": "wisdom"}, 2),  # Should find 2 wisdom quotes
            ({"dimension": "test_dimension"}, 1),  # Should find 1 test dimension quote
            ({"document_name": "test_doc1.txt"}, 1),  # Should find 1 document
            ({"confidence_min": 0.9}, 2),  # Should find 2 high confidence quotes (0.9, 0.95)
            ({"confidence_max": 0.85}, 1),  # Should find 1 low confidence quote (0.8 only)
            ({"dimension": "wisdom", "confidence_min": 0.9}, 1),  # Combined filters
        ]
        
        for filters, expected_count in test_cases:
            with self.subTest(filters=filters):
                results = self.wrapper.get_evidence_by_metadata(filters)
                self.assertEqual(len(results), expected_count)

    def test_search_result_formatting(self):
        """Test that search results are properly formatted."""
        # Build index first
        self.wrapper.build_index([self.evidence_hash])
        
        # Search for evidence
        results = self.wrapper.search_evidence("test")
        
        # Verify result format
        for result in results:
            self.assertIn("quote_text", result)
            self.assertIn("document_name", result)
            self.assertIn("dimension", result)
            self.assertIn("confidence", result)
            self.assertIn("relevance_score", result)
            self.assertIn("metadata", result)
            
            # Verify data types
            self.assertIsInstance(result["quote_text"], str)
            self.assertIsInstance(result["document_name"], str)
            self.assertIsInstance(result["dimension"], str)
            self.assertIsInstance(result["confidence"], (int, float))
            self.assertIsInstance(result["relevance_score"], (int, float))
            self.assertIsInstance(result["metadata"], dict)

    def test_error_handling_invalid_artifact(self):
        """Test error handling when artifacts can't be loaded."""
        # Create a corrupted artifact
        corrupted_hash = self.artifact_storage.put_artifact(
            b"invalid json content",
            {"artifact_type": "evidence_database"}
        )
        
        # Should handle gracefully
        success = self.wrapper.build_index([corrupted_hash])
        self.assertFalse(success)

    def test_error_handling_search_failure(self):
        """Test error handling when search fails."""
        # Build index first
        self.wrapper.build_index([self.evidence_hash])
        
        # Mock search failure
        with patch.object(self.wrapper.index, 'search', side_effect=Exception("Search failed")):
            results = self.wrapper.search_evidence("test")
            self.assertEqual(len(results), 0)

    def test_evidence_without_quotes(self):
        """Test handling of evidence without quote text."""
        evidence_no_quotes = {
            "evidence_data": [
                {
                    "quote_text": "",  # Empty quote
                    "document_name": "test_doc5.txt",
                    "dimension": "test",
                    "confidence": 0.8,
                    "extraction_method": "analysis_time_extraction_v1.0",
                    "source_type": "analysis_response"
                },
                {
                    "quote_text": None,  # None quote
                    "document_name": "test_doc6.txt",
                    "dimension": "test",
                    "confidence": 0.8,
                    "extraction_method": "analysis_time_extraction_v1.0",
                    "source_type": "analysis_response"
                }
            ]
        }
        
        no_quotes_hash = self.artifact_storage.put_artifact(
            json.dumps(evidence_no_quotes).encode('utf-8'),
            {"artifact_type": "evidence_database"}
        )
        
        # Build index - should skip evidence without quotes
        success = self.wrapper.build_index([no_quotes_hash])
        
        # Should fail when there are no valid evidence pieces
        self.assertFalse(success)
        self.assertEqual(len(self.wrapper.evidence_data), 0)  # No valid evidence

    # Phase 2: LLM Query Generation Tests
    def test_generate_search_queries_with_llm(self):
        """Test LLM-based search query generation."""
        # Mock LLM gateway
        mock_llm = Mock()
        mock_llm.execute_call.return_value = ("- wisdom quotes\n- philosophical insights\n- life lessons\n- moral guidance\n- ethical principles", {})
        self.wrapper.llm_gateway = mock_llm
        
        findings = [
            "The majority of respondents (65%) believe wisdom comes from experience",
            "Only 23% of participants consider formal education as the primary source of wisdom"
        ]
        
        queries = self.wrapper.generate_search_queries(findings, max_queries=3)
        
        # Should generate 3 queries
        self.assertEqual(len(queries), 3)
        self.assertIn("wisdom quotes", queries)
        self.assertIn("philosophical insights", queries)
        self.assertIn("life lessons", queries)
        
        # Verify LLM was called correctly
        mock_llm.execute_call.assert_called_once()
        call_args = mock_llm.execute_call.call_args
        self.assertIn("wisdom comes from experience", call_args[1]['prompt'])
        self.assertIn("formal education", call_args[1]['prompt'])
    
    def test_generate_search_queries_fallback(self):
        """Test fallback query generation when LLM is unavailable."""
        # No LLM gateway
        self.wrapper.llm_gateway = None
        
        findings = [
            "The majority of respondents believe wisdom comes from experience",
            "Only 23% of participants consider formal education as primary"
        ]
        
        queries = self.wrapper.generate_search_queries(findings, max_queries=3)
        
        # Should generate fallback queries
        self.assertEqual(len(queries), 3)
        # Should contain key terms from findings
        self.assertTrue(any("wisdom" in q.lower() for q in queries))
        self.assertTrue(any("experience" in q.lower() for q in queries))
    
    def test_generate_search_queries_empty_findings(self):
        """Test query generation with empty findings."""
        queries = self.wrapper.generate_search_queries([], max_queries=5)
        self.assertEqual(queries, [])
    
    def test_generate_search_queries_llm_failure(self):
        """Test fallback when LLM query generation fails."""
        # Mock LLM that raises an exception
        mock_llm = Mock()
        mock_llm.execute_call.side_effect = Exception("LLM service unavailable")
        self.wrapper.llm_gateway = mock_llm
        
        findings = ["The majority of respondents believe wisdom comes from experience"]
        
        queries = self.wrapper.generate_search_queries(findings, max_queries=3)
        
        # Should fall back to rule-based generation
        self.assertEqual(len(queries), 3)
        self.assertTrue(any("wisdom" in q.lower() for q in queries))
    
    def test_parse_generated_queries(self):
        """Test parsing of LLM-generated query responses."""
        response = "- wisdom quotes\n- philosophical insights\n- life lessons\n- moral guidance"
        queries = self.wrapper._parse_generated_queries(response)
        
        expected = ["wisdom quotes", "philosophical insights", "life lessons", "moral guidance"]
        self.assertEqual(queries, expected)
    
    def test_parse_generated_queries_mixed_format(self):
        """Test parsing of queries with mixed formatting."""
        response = "- wisdom quotes\nphilosophical insights\n- life lessons\nmoral guidance"
        queries = self.wrapper._parse_generated_queries(response)
        
        expected = ["wisdom quotes", "philosophical insights", "life lessons", "moral guidance"]
        self.assertEqual(queries, expected)
    
    def test_fallback_query_generation(self):
        """Test rule-based fallback query generation."""
        findings = [
            "The majority of respondents believe wisdom comes from experience",
            "Only 23% of participants consider formal education as primary"
        ]
        
        queries = self.wrapper._generate_fallback_queries(findings, max_queries=3)
        
        self.assertEqual(len(queries), 3)
        # Should contain key terms from findings
        self.assertTrue(any("wisdom" in q.lower() for q in queries))
        self.assertTrue(any("experience" in q.lower() for q in queries))
    
    def test_search_evidence_with_auto_queries(self):
        """Test automatic evidence search using generated queries."""
        # Build index first
        self.wrapper.build_index([self.evidence_hash])
        
        # Mock LLM gateway for query generation
        mock_llm = Mock()
        mock_llm.execute_call.return_value = ("- wisdom\n- philosophy\n- life lessons", {})
        self.wrapper.llm_gateway = mock_llm
        
        findings = [
            "The majority of respondents believe wisdom comes from experience",
            "Only 23% of participants consider formal education as primary"
        ]
        
        results = self.wrapper.search_evidence_with_auto_queries(
            findings, 
            max_queries=3, 
            results_per_query=2
        )
        
        # Should return evidence from multiple queries
        self.assertGreater(len(results), 0)
        # Should have unique quotes
        quotes = [r.get('quote_text', '') for r in results]
        self.assertEqual(len(quotes), len(set(quotes)))
    
    def test_search_evidence_with_auto_queries_no_index(self):
        """Test auto-query search when no index is available."""
        # Mock LLM gateway
        mock_llm = Mock()
        mock_llm.execute_call.return_value = ("- wisdom\n- philosophy", {})
        self.wrapper.llm_gateway = mock_llm
        
        findings = ["The majority of respondents believe wisdom comes from experience"]
        
        results = self.wrapper.search_evidence_with_auto_queries(findings)
        
        # Should return empty results when no index
        self.assertEqual(results, [])
    
    def test_search_evidence_with_auto_queries_fallback(self):
        """Test auto-query search with fallback query generation."""
        # Build index first
        self.wrapper.build_index([self.evidence_hash])
        
        # No LLM gateway - should use fallback
        self.wrapper.llm_gateway = None
        
        findings = [
            "The majority of respondents believe wisdom comes from experience",
            "Only 23% of participants consider formal education as primary"
        ]
        
        results = self.wrapper.search_evidence_with_auto_queries(
            findings, 
            max_queries=3, 
            results_per_query=2
        )
        
        # Should still return results using fallback queries
        self.assertGreater(len(results), 0)


if __name__ == "__main__":
    unittest.main()
