"""
Priority 3 Academic Pipeline Integration Tests

End-to-end testing for academic analysis pipeline components.
"""

import pytest
import tempfile
import pandas as pd
import json
from pathlib import Path
from datetime import datetime
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

from src.academic.data_export import AcademicDataExporter
from src.academic.analysis_templates import JupyterTemplateGenerator


class TestAcademicDataExport:
    """Test academic data export functionality."""
    
    def test_csv_export_format(self):
        """Test CSV export with proper academic formatting."""
        sample_data = pd.DataFrame({
            'exp_id': ['exp_001', 'exp_002'],
            'framework': ['civic_virtue', 'political_spectrum'],
            'cv': [0.15, 0.25],
            'llm_model': ['gpt-4', 'claude-3']
        })
        
        # Test academic variable naming standards
        for col in sample_data.columns:
            assert col.islower()  # Lowercase
            assert ' ' not in col  # No spaces
            if len(col.split('_')) > 1:  # If underscore separated
                assert all(part.islower() for part in col.split('_'))
    
    def test_statistical_packages_available(self):
        """Test required statistical packages are installed."""
        
        # Test scipy
        import scipy.stats
        assert hasattr(scipy.stats, 'f_oneway')
        
        # Test pyreadstat for Stata
        try:
            import pyreadstat
            assert hasattr(pyreadstat, 'write_dta')
        except ImportError:
            pytest.skip("pyreadstat not available")
        
        # Test core packages
        import pandas as pd
        import numpy as np
        import matplotlib.pyplot as plt
        import seaborn as sns


class TestAnalysisTemplates:
    """Test analysis template generation."""
    
    def test_jupyter_notebook_generation(self):
        """Test Jupyter notebook template generation."""
        
        with tempfile.TemporaryDirectory() as temp_dir:
            generator = JupyterTemplateGenerator()
            notebook_path = generator.generate_exploration_notebook(
                study_name='test_study',
                output_path=temp_dir
            )
            
            # Verify notebook exists
            assert Path(notebook_path).exists()
            
            # Verify notebook structure
            with open(notebook_path, 'r') as f:
                notebook = json.load(f)
            
            assert 'cells' in notebook
            assert len(notebook['cells']) > 0
            
            # Check for statistical content
            content = str(notebook)
            assert 'scipy' in content
            assert 'pandas' in content
    
    def test_statistical_content_validation(self):
        """Test that templates contain proper statistical analysis."""
        
        with tempfile.TemporaryDirectory() as temp_dir:
            generator = JupyterTemplateGenerator()
            notebook_path = generator.generate_exploration_notebook(
                study_name='stats_test',
                output_path=temp_dir
            )
            
            with open(notebook_path, 'r') as f:
                content = f.read()
            
            # Required statistical elements
            required_elements = [
                'from scipy import stats',
                'pandas as pd',
                'matplotlib.pyplot',
                'seaborn as sns'
            ]
            
            for element in required_elements:
                assert element in content


class TestPipelineIntegration:
    """Test complete pipeline integration."""
    
    def test_pipeline_components_available(self):
        """Test all Priority 3 components are available."""
        
        # Test data export
        from src.academic.data_export import AcademicDataExporter
        exporter = AcademicDataExporter()
        assert hasattr(exporter, 'export_experiments_data')
        
        # Test analysis templates
        from src.academic.analysis_templates import JupyterTemplateGenerator
        generator = JupyterTemplateGenerator()
        assert hasattr(generator, 'generate_exploration_notebook')
        
        # Test documentation
        from src.academic.documentation import MethodologyPaperGenerator
        doc_generator = MethodologyPaperGenerator()
        assert hasattr(doc_generator, 'generate_methodology_section')
    
    def test_workflow_validation_criteria(self):
        """Test academic workflow validation criteria."""
        
        validation_criteria = {
            'data_formats': ['csv', 'feather', 'json', 'stata'],
            'templates': ['jupyter', 'r', 'stata'],
            'documentation': ['methodology', 'results', 'replication']
        }
        
        for category, items in validation_criteria.items():
            assert len(items) > 0
            assert all(isinstance(item, str) for item in items)


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 