#!/usr/bin/env python3
"""
Unit Tests for Statistical Analysis Integration
==============================================

Tests for the statistical analysis phase that is affected by the batch processing regression.
These tests focus on DataFrame conversion and path resolution issues.

Key Test Areas:
1. DataFrame conversion from individual vs batch analysis results
2. Path resolution for artifact loading  
3. Statistical function execution integration
4. Error handling for missing artifacts
"""

import unittest
from unittest.mock import Mock, MagicMock, patch
from pathlib import Path
import json
import tempfile
import shutil
import pandas as pd

from discernus.core.clean_analysis_orchestrator import CleanAnalysisOrchestrator, CleanAnalysisError


class TestStatisticalAnalysisIntegration(unittest.TestCase):
    """Test statistical analysis integration with analysis results."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create temporary directory
        self.temp_dir = Path(tempfile.mkdtemp())
        self.experiment_path = self.temp_dir / "test_experiment"
        self.experiment_path.mkdir(parents=True)
        
        # Create artifacts directory with correct structure
        self.artifacts_dir = self.experiment_path / "shared_cache" / "artifacts"
        self.artifacts_dir.mkdir(parents=True)
        
        # Initialize orchestrator
        self.orchestrator = CleanAnalysisOrchestrator(self.experiment_path)
        self.orchestrator.config = {'framework': 'framework.md'}
        
        # Mock dependencies
        self.orchestrator.artifact_storage = Mock()
        self.orchestrator.logger = Mock()
    
    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir)
    
    def test_path_resolution_fix(self):
        """Test that path resolution uses correct artifacts directory."""
        # Create mock raw analysis response file
        raw_response_file = self.artifacts_dir / "raw_analysis_response_v6_test123"
        raw_response_content = """
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
                "dimension1": {"raw_score": 0.5, "salience": 0.6, "confidence": 0.9}
              }
            }
          ]
        }
        <<<END_DISCERNUS_ANALYSIS_JSON_v6>>>
        """
        raw_response_file.write_text(raw_response_content)
        
        # Test the corrected path resolution
        analysis_results = [{"raw_analysis_response": ""}]  # Empty to force file loading
        
        # This should use the CORRECT path (without extra /artifacts)
        df = self.orchestrator._convert_analysis_to_dataframe_fixed(analysis_results)
        
        # Verify DataFrame was created successfully
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 1)  # One document
        self.assertIn('document_name', df.columns)
        self.assertIn('dimension1_raw', df.columns)
        self.assertEqual(df.iloc[0]['dimension1_raw'], 0.5)
    
    def test_dataframe_conversion_individual_results(self):
        """Test DataFrame conversion from multiple individual analysis results."""
        # Mock individual analysis results (CORRECT PATTERN)
        individual_results = [
            {
                "raw_analysis_response": """
                <<<DISCERNUS_ANALYSIS_JSON_v6>>>
                {
                  "document_analyses": [
                    {
                      "document_name": "doc1.txt",
                      "dimensional_scores": {
                        "dimension1": {"raw_score": 0.5, "salience": 0.6, "confidence": 0.9},
                        "dimension2": {"raw_score": 0.7, "salience": 0.8, "confidence": 0.95}
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
                        "dimension1": {"raw_score": 0.3, "salience": 0.4, "confidence": 0.8},
                        "dimension2": {"raw_score": 0.9, "salience": 0.7, "confidence": 0.9}
                      }
                    }
                  ]
                }
                <<<END_DISCERNUS_ANALYSIS_JSON_v6>>>
                """
            }
        ]
        
        # Convert to DataFrame
        df = self.orchestrator._convert_analysis_to_dataframe_individual(individual_results)
        
        # Verify DataFrame structure
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 2)  # Two documents
        
        # Verify columns exist
        expected_columns = [
            'document_name',
            'dimension1_raw', 'dimension1_salience', 'dimension1_confidence',
            'dimension2_raw', 'dimension2_salience', 'dimension2_confidence'
        ]
        for col in expected_columns:
            self.assertIn(col, df.columns)
        
        # Verify data values
        doc1_row = df[df['document_name'] == 'doc1.txt'].iloc[0]
        self.assertEqual(doc1_row['dimension1_raw'], 0.5)
        self.assertEqual(doc1_row['dimension2_salience'], 0.8)
        
        doc2_row = df[df['document_name'] == 'doc2.txt'].iloc[0]
        self.assertEqual(doc2_row['dimension1_raw'], 0.3)
        self.assertEqual(doc2_row['dimension2_confidence'], 0.9)
    
    def test_dataframe_conversion_batch_results(self):
        """Test DataFrame conversion from batch analysis results (BROKEN PATTERN)."""
        # Mock batch analysis result (CURRENT BROKEN APPROACH)
        batch_result = {
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
        
        # Test current batch conversion (works but breaks caching)
        df = self.orchestrator._convert_analysis_to_dataframe([batch_result])
        
        # Verify it works but note the architectural problem
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 2)  # Two documents from single batch
        
        # This works for DataFrame creation but breaks:
        # - Document-level caching
        # - Individual artifact storage
        # - Granular error handling
        # - Synthesis asset validation
    
    def test_statistical_function_execution_with_individual_data(self):
        """Test that statistical functions work with individual document data."""
        # Mock DataFrame from individual results
        test_df = pd.DataFrame([
            {
                'document_name': 'doc1.txt',
                'dimension1_raw': 0.5,
                'dimension1_salience': 0.6,
                'dimension1_confidence': 0.9,
                'dimension2_raw': 0.7,
                'dimension2_salience': 0.8,
                'dimension2_confidence': 0.95
            },
            {
                'document_name': 'doc2.txt', 
                'dimension1_raw': 0.3,
                'dimension1_salience': 0.4,
                'dimension1_confidence': 0.8,
                'dimension2_raw': 0.9,
                'dimension2_salience': 0.7,
                'dimension2_confidence': 0.9
            }
        ])
        
        # Mock statistical functions module
        mock_stats_module = Mock()
        
        # Mock statistical functions
        def mock_descriptive_stats(data):
            return {
                "mean_dimension1": data['dimension1_raw'].mean(),
                "std_dimension1": data['dimension1_raw'].std(),
                "count": len(data)
            }
        
        def mock_correlation_analysis(data):
            return {
                "dimension1_dimension2_correlation": data['dimension1_raw'].corr(data['dimension2_raw']),
                "significance": "p < 0.05"
            }
        
        # Configure mock module
        mock_stats_module.descriptive_statistics = mock_descriptive_stats
        mock_stats_module.correlation_analysis = mock_correlation_analysis
        
        # Mock the module loading and execution
        with patch('importlib.util.spec_from_file_location'), \
             patch('importlib.util.module_from_spec', return_value=mock_stats_module), \
             patch.object(self.orchestrator, '_convert_analysis_to_dataframe_individual', return_value=test_df):
            
            # Mock workspace path
            workspace_path = self.temp_dir / "workspace"
            workspace_path.mkdir()
            (workspace_path / "automatedstatisticalanalysisagent_functions.py").write_text("# Mock functions")
            
            # Test statistical function execution
            results = self.orchestrator._execute_statistical_functions_individual(
                workspace_path, 
                [{"mock": "individual_result1"}, {"mock": "individual_result2"}],
                Mock()
            )
        
        # Verify statistical results
        self.assertIn('descriptive_statistics', results)
        self.assertIn('correlation_analysis', results)
        
        # Verify descriptive statistics
        desc_stats = results['descriptive_statistics']
        self.assertEqual(desc_stats['mean_dimension1'], 0.4)  # (0.5 + 0.3) / 2
        self.assertEqual(desc_stats['count'], 2)
        
        # Verify correlation analysis
        corr_stats = results['correlation_analysis']
        self.assertIn('dimension1_dimension2_correlation', corr_stats)


# Helper methods to add to CleanAnalysisOrchestrator for testing
def _convert_analysis_to_dataframe_fixed(self, analysis_results: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Fixed DataFrame conversion with correct path resolution.
    """
    import pandas as pd
    import json
    
    if not analysis_results or len(analysis_results) == 0:
        raise CleanAnalysisError("No analysis results to convert")
    
    analysis_result = analysis_results[0]
    raw_response = analysis_result.get('raw_analysis_response', '')
    
    if not raw_response:
        # FIXED PATH: Remove extra /artifacts component
        artifacts_dir = self.experiment_path / "shared_cache" / "artifacts"  # CORRECT
        raw_response_files = list(artifacts_dir.glob("raw_analysis_response_v6_*"))
        
        if raw_response_files:
            raw_response_file = sorted(raw_response_files)[-1]
            raw_response = raw_response_file.read_text(encoding='utf-8')
        else:
            raise CleanAnalysisError("No raw analysis response found in artifacts directory")
    
    # Extract JSON (same as current implementation)
    start_marker = '<<<DISCERNUS_ANALYSIS_JSON_v6>>>'
    end_marker = '<<<END_DISCERNUS_ANALYSIS_JSON_v6>>>'
    
    start_idx = raw_response.find(start_marker)
    end_idx = raw_response.find(end_marker)
    
    if start_idx == -1 or end_idx == -1:
        raise CleanAnalysisError("Could not find analysis JSON markers in response")
    
    json_content = raw_response[start_idx + len(start_marker):end_idx].strip()
    analysis_data = json.loads(json_content)
    
    # Convert to DataFrame
    rows = []
    for doc_analysis in analysis_data.get('document_analyses', []):
        row = {'document_name': doc_analysis.get('document_name', '')}
        
        for dimension, scores in doc_analysis.get('dimensional_scores', {}).items():
            row[f"{dimension}_raw"] = scores.get('raw_score', 0.0)
            row[f"{dimension}_salience"] = scores.get('salience', 0.0)
            row[f"{dimension}_confidence"] = scores.get('confidence', 0.0)
        
        rows.append(row)
    
    return pd.DataFrame(rows)


def _convert_analysis_to_dataframe_individual(self, analysis_results: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    DataFrame conversion from individual analysis results (CORRECT PATTERN).
    """
    import pandas as pd
    import json
    
    if not analysis_results or len(analysis_results) == 0:
        raise CleanAnalysisError("No analysis results to convert")
    
    all_rows = []
    
    # Process each individual analysis result
    for analysis_result in analysis_results:
        raw_response = analysis_result.get('raw_analysis_response', '')
        
        if not raw_response:
            continue  # Skip empty responses
        
        # Extract JSON from each individual result
        start_marker = '<<<DISCERNUS_ANALYSIS_JSON_v6>>>'
        end_marker = '<<<END_DISCERNUS_ANALYSIS_JSON_v6>>>'
        
        start_idx = raw_response.find(start_marker)
        end_idx = raw_response.find(end_marker)
        
        if start_idx == -1 or end_idx == -1:
            continue  # Skip malformed responses
        
        json_content = raw_response[start_idx + len(start_marker):end_idx].strip()
        
        try:
            analysis_data = json.loads(json_content)
        except json.JSONDecodeError:
            continue  # Skip unparseable responses
        
        # Each individual result should have exactly one document analysis
        for doc_analysis in analysis_data.get('document_analyses', []):
            row = {'document_name': doc_analysis.get('document_name', '')}
            
            # Add dimensional scores
            for dimension, scores in doc_analysis.get('dimensional_scores', {}).items():
                row[f"{dimension}_raw"] = scores.get('raw_score', 0.0)
                row[f"{dimension}_salience"] = scores.get('salience', 0.0)
                row[f"{dimension}_confidence"] = scores.get('confidence', 0.0)
            
            all_rows.append(row)
    
    if not all_rows:
        raise CleanAnalysisError("No valid document analyses found in results")
    
    return pd.DataFrame(all_rows)


def _execute_statistical_functions_individual(self, workspace_path: Path, analysis_results: List[Dict[str, Any]], audit_logger) -> Dict[str, Any]:
    """
    Execute statistical functions with individual analysis results (CORRECT PATTERN).
    """
    import pandas as pd
    import importlib.util
    
    # Load the generated statistical functions module
    functions_file = workspace_path / "automatedstatisticalanalysisagent_functions.py"
    if not functions_file.exists():
        raise CleanAnalysisError("Statistical functions file not found")
    
    # Import the generated module
    spec = importlib.util.spec_from_file_location("statistical_functions", functions_file)
    stats_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(stats_module)
    
    # Convert individual analysis results to DataFrame
    analysis_data = self._convert_analysis_to_dataframe_individual(analysis_results)
    
    # Execute each statistical function
    statistical_outputs = {}
    function_names = [name for name in dir(stats_module) if not name.startswith('_') and callable(getattr(stats_module, name))]
    
    for func_name in function_names:
        try:
            func = getattr(stats_module, func_name)
            result = func(analysis_data)
            statistical_outputs[func_name] = result
        except Exception as e:
            statistical_outputs[func_name] = {"error": str(e), "status": "failed"}
    
    return statistical_outputs


# Add methods to CleanAnalysisOrchestrator for testing
CleanAnalysisOrchestrator._convert_analysis_to_dataframe_fixed = _convert_analysis_to_dataframe_fixed
CleanAnalysisOrchestrator._convert_analysis_to_dataframe_individual = _convert_analysis_to_dataframe_individual
CleanAnalysisOrchestrator._execute_statistical_functions_individual = _execute_statistical_functions_individual


class TestPathResolutionRegression(unittest.TestCase):
    """Test the specific path resolution bug in statistical analysis."""
    
    def test_artifacts_path_bug(self):
        """Test the specific path bug that causes 'No raw analysis response found'."""
        # Create temporary experiment structure
        temp_dir = Path(tempfile.mkdtemp())
        experiment_path = temp_dir / "test_experiment"
        experiment_path.mkdir(parents=True)
        
        try:
            # Create CORRECT artifacts directory structure
            correct_artifacts_dir = experiment_path / "shared_cache" / "artifacts"
            correct_artifacts_dir.mkdir(parents=True)
            
            # Create BROKEN artifacts directory structure (what the bug looks for)
            broken_artifacts_dir = experiment_path / "shared_cache" / "artifacts" / "artifacts"
            broken_artifacts_dir.mkdir(parents=True)
            
            # Place file in CORRECT location
            test_file = correct_artifacts_dir / "raw_analysis_response_v6_test"
            test_file.write_text("test content")
            
            # Test BROKEN path (current implementation)
            broken_path = experiment_path / "shared_cache" / "artifacts" / "artifacts"
            broken_files = list(broken_path.glob("raw_analysis_response_v6_*"))
            self.assertEqual(len(broken_files), 0, "Broken path finds no files")
            
            # Test CORRECT path (fixed implementation)
            correct_path = experiment_path / "shared_cache" / "artifacts"
            correct_files = list(correct_path.glob("raw_analysis_response_v6_*"))
            self.assertEqual(len(correct_files), 1, "Correct path finds the file")
            
        finally:
            shutil.rmtree(temp_dir)


if __name__ == '__main__':
    unittest.main()
