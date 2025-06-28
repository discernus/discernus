"""
Test all core imports work correctly after reorganization.
This validates that the structure cleanup was successful.
"""

import pytest


def test_api_imports():
    """Test that API components can be imported"""
    from discernus.api.main import app
    assert app is not None


def test_gateway_imports():
    """Test that gateway components can be imported"""
    from discernus.gateway.llm_gateway import get_llm_analysis
    assert get_llm_analysis is not None


def test_engine_imports():
    """Test that engine components can be imported"""
    from discernus.engine.signature_engine import calculate_coordinates
    from discernus.engine.prompt_engine import create_prompt_from_experiment
    
    assert calculate_coordinates is not None
    assert create_prompt_from_experiment is not None


def test_database_imports():
    """Test that database components can be imported"""
    from discernus.database.models import AnalysisJob, AnalysisResult
    from discernus.database.session import get_db
    
    assert AnalysisJob is not None
    assert AnalysisResult is not None
    assert get_db is not None


def test_reporting_imports():
    """Test that reporting components can be imported"""
    from discernus.reporting.report_builder import ReportBuilder
    
    assert ReportBuilder is not None


def test_analysis_imports():
    """Test that analysis components can be imported"""
    from discernus.analysis.statistical_methods import StatisticalMethodRegistry
    
    assert StatisticalMethodRegistry is not None


def test_scripts_imports():
    """Test that scripts can be imported"""
    from scripts.tasks import analyze_text_task
    
    assert analyze_text_task is not None


def test_database_models_instantiation():
    """Test that database models can be instantiated"""
    from discernus.database.models import AnalysisJob, AnalysisResult
    
    # These should not require database connection to instantiate
    job = AnalysisJob()
    result = AnalysisResult()
    
    assert job is not None
    assert result is not None


def test_report_builder_instantiation():
    """Test that report builder can be instantiated"""
    from discernus.reporting.report_builder import ReportBuilder
    
    # This should work without filesystem dependencies
    builder = ReportBuilder(output_dir="/tmp/test_reports")
    assert builder is not None 