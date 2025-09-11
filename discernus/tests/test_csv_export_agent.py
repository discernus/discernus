#!/usr/bin/env python3
"""
Unit tests for CSV Export Agent
===============================

Tests the core functionality of the CSV Export Agent,
including CSV generation, evidence linking, and export options.
"""

# Copyright (C) 2025  Discernus Team

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import os
import csv
import json
import tempfile
import unittest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

from discernus.agents.csv_export_agent import (
    CSVExportAgent,
    ExportResult,
    ExportOptions,
    CSVExportError
)


class TestCSVExportAgent:
    """Test cases for CSV Export Agent."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.agent = CSVExportAgent()
        
        # Sample analysis data structure (from gasket integration)
        self.sample_analysis_data = {
            "analysis_metadata": {
                "framework_name": "character_assessment_framework",
                "framework_version": "v7.0",
                "analyst_confidence": 0.85,
                "analysis_notes": "Test analysis"
            },
            "document_analyses": [
                {
                    "document_id": "doc_001",
                    "document_name": "test_document_1.txt",
                    "analysis_scores": {
                        "dignity_score": 0.8,
                        "tribalism_score": 0.6,
                        "dignity_tribalism_tension": 0.2,
                        "truth_score": 0.7,
                        "manipulation_score": 0.5,
                        "justice_score": 0.9,
                        "resentment_score": 0.7,
                        "hope_score": 0.4,
                        "fear_score": 0.3,
                        "civic_character_index": 0.65
                    },
                    "extraction_metadata": {
                        "extraction_time_seconds": 5.2,
                        "tokens_used": 150,
                        "cost_usd": 0.01,
                        "attempts": 1,
                        "gasket_version": "v7.0"
                    }
                },
                {
                    "document_id": "doc_002", 
                    "document_name": "test_document_2.txt",
                    "analysis_scores": {
                        "dignity_score": 0.85,
                        "tribalism_score": 0.2,
                        "dignity_tribalism_tension": 0.65,
                        "truth_score": 0.7,
                        "manipulation_score": 0.1,
                        "justice_score": 0.75,
                        "resentment_score": 0.15,
                        "hope_score": 0.9,
                        "fear_score": 0.05,
                        "civic_character_index": 0.78
                    },
                    "extraction_metadata": {
                        "extraction_time_seconds": 6.1,
                        "tokens_used": 175,
                        "cost_usd": 0.012,
                        "attempts": 1,
                        "gasket_version": "v7.0"
                    }
                }
            ]
        }
        
        # Sample framework config
        self.sample_framework_config = {
            "name": "character_assessment_framework",
            "version": "v7.0",
            "display_name": "Character Assessment Framework v7.0"
        }
        
        # Sample corpus manifest
        self.sample_corpus_manifest = {
            "corpus_name": "test_corpus",
            "corpus_version": "v7.0",
            "document_count": 2
        }
    
    def test_initialization(self):
        """Test agent initialization."""
        agent = CSVExportAgent()
        assert agent.agent_name == "CSVExportAgent"
        assert agent.audit_logger is None
        
        # Test with audit logger
        mock_logger = Mock()
        agent_with_logger = CSVExportAgent(audit_logger=mock_logger)
        assert agent_with_logger.audit_logger == mock_logger
    
    def test_export_options_defaults(self):
        """Test ExportOptions default values."""
        options = ExportOptions()
        assert options.include_calculated_metrics is True
        assert options.evidence_detail_level == "hashes_only"
        assert options.export_format == "standard"
        assert options.custom_column_names is None
        assert options.include_metadata is True
    
    def test_successful_export(self):
        """Test successful CSV export operation."""
        # Mock the artifact client instance
        with patch.object(self.agent, 'artifact_client') as mock_client:
            mock_client.get_artifact.return_value = json.dumps(self.sample_analysis_data).encode('utf-8')
            
            with tempfile.TemporaryDirectory() as temp_dir:
                result = self.agent.export_mid_point_data(
                    scores_hash="test_hash_123",
                    evidence_hash="test_hash_123",
                    framework_config=self.sample_framework_config,
                    corpus_manifest=self.sample_corpus_manifest,
                    export_path=temp_dir
                )
                
                assert result.success is True
                assert result.export_path == temp_dir
                assert len(result.files_created) >= 3  # scores, evidence, metadata
                assert result.total_records == 2
                assert result.error_message is None
                
                # Verify files were created
                expected_files = ['scores.csv', 'evidence.csv', 'metadata.csv']
                for filename in expected_files:
                    filepath = os.path.join(temp_dir, filename)
                    assert os.path.exists(filepath), f"File {filename} was not created"
    
    def test_scores_csv_generation(self):
        """Test scores.csv file generation and content."""
        # Mock the artifact client instance
        with patch.object(self.agent, 'artifact_client') as mock_client:
            mock_client.get_artifact.return_value = json.dumps(self.sample_analysis_data).encode('utf-8')
            
            with tempfile.TemporaryDirectory() as temp_dir:
                result = self.agent.export_mid_point_data(
                    scores_hash="test_hash_123",
                    evidence_hash="test_hash_123",
                    framework_config=self.sample_framework_config,
                    corpus_manifest=self.sample_corpus_manifest,
                    export_path=temp_dir
                )
                
                # Read and verify scores.csv
                scores_file = os.path.join(temp_dir, 'scores.csv')
                with open(scores_file, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    rows = list(reader)
                    
                    assert len(rows) == 2  # Two documents
                    
                    # Check first row
                    row1 = rows[0]
                    assert row1['document_id'] == 'doc_001'
                    assert row1['filename'] == 'test_document_1.txt'
                    assert float(row1['dignity_score']) == 0.8
                    assert float(row1['truth_score']) == 0.7
                    assert 'evidence_hash' in row1
                    
                    # Check second row
                    row2 = rows[1]
                    assert row2['document_id'] == 'doc_002'
                    assert float(row2['dignity_score']) == 0.85
                    assert float(row2['hope_score']) == 0.9
    
    def test_evidence_csv_generation(self):
        """Test evidence.csv file generation and content."""
        # Mock the artifact client instance
        with patch.object(self.agent, 'artifact_client') as mock_client:
            mock_client.get_artifact.return_value = json.dumps(self.sample_analysis_data).encode('utf-8')
            
            with tempfile.TemporaryDirectory() as temp_dir:
                result = self.agent.export_mid_point_data(
                    scores_hash="test_hash_123",
                    evidence_hash="test_hash_123",
                    framework_config=self.sample_framework_config,
                    corpus_manifest=self.sample_corpus_manifest,
                    export_path=temp_dir
                )
                
                # Read and verify evidence.csv
                evidence_file = os.path.join(temp_dir, 'evidence.csv')
                with open(evidence_file, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    rows = list(reader)
                    
                    # Should have evidence rows for each non-null score
                    assert len(rows) > 0
                    
                    # Check first evidence row
                    row1 = rows[0]
                    assert 'document_id' in row1
                    assert 'evidence_hash' in row1
                    assert 'dimension' in row1
                    assert 'score' in row1
    
    def test_metadata_csv_generation(self):
        """Test metadata.csv file generation and content."""
        # Mock the artifact client instance
        with patch.object(self.agent, 'artifact_client') as mock_client:
            mock_client.get_artifact.return_value = json.dumps(self.sample_analysis_data).encode('utf-8')
            
            with tempfile.TemporaryDirectory() as temp_dir:
                result = self.agent.export_mid_point_data(
                    scores_hash="test_hash_123",
                    evidence_hash="test_hash_123",
                    framework_config=self.sample_framework_config,
                    corpus_manifest=self.sample_corpus_manifest,
                    export_path=temp_dir
                )
                
                # Read and verify metadata.csv
                metadata_file = os.path.join(temp_dir, 'metadata.csv')
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    rows = list(reader)
                    
                    assert len(rows) == 2  # Two documents
                    
                    # Check metadata content
                    row1 = rows[0]
                    assert row1['document_id'] == 'doc_001'
                    assert row1['framework_name'] == 'character_assessment_framework'
                    assert row1['framework_version'] == 'v7.0'
                    assert row1['gasket_version'] == 'v7.0'
                    assert 'export_timestamp' in row1
    
    def test_custom_export_options(self):
        """Test export with custom options."""
        options = ExportOptions(
            include_calculated_metrics=False,
            evidence_detail_level="quotes",
            export_format="r_friendly",
            custom_column_names={"document_id": "doc_id", "filename": "file_name"},
            include_metadata=False
        )
        
        assert options.include_calculated_metrics is False
        assert options.evidence_detail_level == "quotes"
        assert options.export_format == "r_friendly"
        assert options.custom_column_names["document_id"] == "doc_id"
        assert options.include_metadata is False
    
    def test_artifact_loading_failure(self):
        """Test handling of artifact loading failures."""
        # Mock the artifact client instance to return None (artifact not found)
        with patch.object(self.agent, 'artifact_client') as mock_client:
            mock_client.get_artifact.return_value = None
            
            with tempfile.TemporaryDirectory() as temp_dir:
                result = self.agent.export_mid_point_data(
                    scores_hash="nonexistent_hash",
                    evidence_hash="nonexistent_hash",
                    framework_config=self.sample_framework_config,
                    corpus_manifest=self.sample_corpus_manifest,
                    export_path=temp_dir
                )
                
                assert result.success is False
                assert "Analysis artifact not found" in result.error_message
                assert result.total_records == 0
    
    def test_evidence_hash_creation(self):
        """Test evidence hash creation for linking."""
        doc_analysis = {
            "document_id": "test_doc",
            "analysis_scores": {"dignity_score": 0.8, "truth_score": 0.7}
        }
        
        hash1 = self.agent._create_evidence_hash(doc_analysis)
        hash2 = self.agent._create_evidence_hash(doc_analysis)
        
        # Hash should be consistent
        assert hash1 == hash2
        assert len(hash1) == 16  # Truncated SHA-256
        assert isinstance(hash1, str)
        
        # Different content should produce different hash
        doc_analysis2 = {
            "document_id": "different_doc",
            "analysis_scores": {"dignity_score": 0.9, "truth_score": 0.8}
        }
        hash3 = self.agent._create_evidence_hash(doc_analysis2)
        assert hash1 != hash3
    
    def test_get_export_stats(self):
        """Test export statistics retrieval."""
        stats = self.agent.get_export_stats()
        
        assert stats["agent_name"] == "CSVExportAgent"
        assert stats["gasket_type"] == "pipeline_to_human"
        assert "csv_generation" in stats["capabilities"]
        assert "evidence_linking" in stats["capabilities"]
        assert "standard" in stats["supported_formats"]
        assert "r_friendly" in stats["supported_formats"]
    
    def test_empty_analysis_data(self):
        """Test handling of empty analysis data."""
        empty_data = {"analysis_metadata": {}, "document_analyses": []}
        
        # Mock the artifact client instance
        with patch.object(self.agent, 'artifact_client') as mock_client:
            mock_client.get_artifact.return_value = json.dumps(empty_data).encode('utf-8')
            
            with tempfile.TemporaryDirectory() as temp_dir:
                result = self.agent.export_mid_point_data(
                    scores_hash="empty_hash",
                    evidence_hash="empty_hash",
                    framework_config=self.sample_framework_config,
                    corpus_manifest=self.sample_corpus_manifest,
                    export_path=temp_dir
                )
                
                assert result.success is False
                assert "No document analyses found" in result.error_message


if __name__ == '__main__':
    unittest.main()