import pytest
import sys
import os
import json
import logging
from io import StringIO
from datetime import datetime

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.utils.logging_config import MetricsCollector, StructuredLogger, setup_logging, get_logger, ErrorCodes

@pytest.fixture
def metrics_collector():
    """Returns a new instance of MetricsCollector for each test."""
    return MetricsCollector()

@pytest.fixture
def log_capture():
    """
    A fixture that captures logs from a named logger and yields a StringIO stream.
    """
    # Using a dictionary to hold the stream allows it to be accessible inside the factory.
    streams = {}
    
    def factory(logger_name):
        logger = logging.getLogger(logger_name)
        log_stream = StringIO()
        handler = logging.StreamHandler(log_stream)
        
        # Save original state
        original_handlers = logger.handlers[:]
        original_level = logger.level
        
        # Configure for capture
        logger.handlers = [handler]
        logger.setLevel(logging.INFO)
        
        streams[logger_name] = (log_stream, original_handlers, original_level)
        return log_stream

    yield factory
    
    # Teardown: restore original logger state
    for logger_name, (log_stream, original_handlers, original_level) in streams.items():
        logger = logging.getLogger(logger_name)
        logger.handlers = original_handlers
        logger.level = original_level

class TestMetricsCollector:
    """
    Unit tests for the MetricsCollector class.
    """

    def test_initialization(self, metrics_collector):
        """Tests that the collector initializes with zeroed-out metrics."""
        summary = metrics_collector.get_summary()
        assert summary['ingestion']['total_attempts'] == 0
        assert summary['job_processing']['total_jobs'] == 0
        assert summary['api_usage']['total_requests'] == 0
        assert summary['summary']['ingestion_success_rate'] == 0

    def test_record_ingestion_attempt(self, metrics_collector):
        """Tests recording of successful and failed ingestion attempts."""
        metrics_collector.record_ingestion_attempt(success=True, documents=10, chunks=100)
        metrics_collector.record_ingestion_attempt(success=False, validation_errors=5)
        
        summary = metrics_collector.get_summary()
        assert summary['ingestion']['total_attempts'] == 2
        assert summary['ingestion']['successful_corpora'] == 1
        assert summary['ingestion']['failed_corpora'] == 1
        assert summary['ingestion']['documents_processed'] == 10
        assert summary['ingestion']['chunks_created'] == 100
        assert summary['ingestion']['validation_errors'] == 5
        assert summary['summary']['ingestion_success_rate'] == 50.0

    def test_record_job_event(self, metrics_collector):
        """Tests the lifecycle of a job event."""
        metrics_collector.record_job_event("created", job_id=1)
        metrics_collector.record_job_event("completed", job_id=1)
        
        summary = metrics_collector.get_summary()
        assert summary['job_processing']['total_jobs'] == 1
        assert summary['job_processing']['completed_jobs'] == 1
        assert summary['job_processing']['active_jobs'] == 0

    def test_record_task_event(self, metrics_collector):
        """Tests recording various task events."""
        metrics_collector.record_task_event("created", task_id=101)
        metrics_collector.record_task_event("completed", task_id=101, api_cost=0.05)
        metrics_collector.record_task_event("created", task_id=102)
        metrics_collector.record_task_event("failed", task_id=102)
        
        summary = metrics_collector.get_summary()
        assert summary['job_processing']['total_tasks'] == 2
        assert summary['job_processing']['completed_tasks'] == 1
        assert summary['job_processing']['failed_tasks'] == 1
        assert summary['api_usage']['total_cost'] == 0.05

    def test_get_summary_handles_division_by_zero(self, metrics_collector):
        """Ensures summary calculation doesn't fail when counts are zero."""
        summary = metrics_collector.get_summary()
        assert summary['summary']['ingestion_success_rate'] == 0
        assert summary['summary']['job_success_rate'] == 0
        assert summary['summary']['task_success_rate'] == 0
        assert summary['summary']['api_success_rate'] == 0
        assert summary['summary']['average_cost_per_task'] == 0

class TestStructuredLogger:
    """
    Unit tests for the StructuredLogger class.
    """
    
    def test_info_log_structure(self, log_capture):
        """Tests that info logs are correctly formatted as JSON."""
        logger_name = "test_info_logger"
        log_stream = log_capture(logger_name)
        
        logger = get_logger(logger_name)
        logger.info("This is an info message.", extra_data={"user": "test"})
        
        log_output = json.loads(log_stream.getvalue())
        
        assert log_output['level'] == 'INFO'
        assert log_output['message'] == 'This is an info message.'
        assert log_output['extra']['user'] == 'test'

    def test_warning_log_structure(self, log_capture):
        """Tests that warning logs include an error code."""
        logger_name = "test_warning_logger"
        log_stream = log_capture(logger_name)
        
        logger = get_logger(logger_name)
        logger.warning("This is a warning.", error_code=ErrorCodes.API_VALIDATION_ERROR)
        
        log_output = json.loads(log_stream.getvalue())
        
        assert log_output['level'] == 'WARNING'
        assert log_output['error_code'] == ErrorCodes.API_VALIDATION_ERROR

    def test_error_log_with_exception(self, log_capture):
        """Tests that error logs correctly serialize exception information."""
        logger_name = "test_error_logger"
        log_stream = log_capture(logger_name)
        
        logger = get_logger(logger_name)
        try:
            raise ValueError("This is a test exception.")
        except ValueError as e:
            logger.error("An error occurred.", exception=e)
            
        log_output = json.loads(log_stream.getvalue())
        
        assert log_output['level'] == 'ERROR'
        assert "exception" in log_output
        assert log_output['exception']['type'] == 'ValueError'
        assert log_output['exception']['message'] == 'This is a test exception.'
        assert "stack_trace" in log_output['exception'] 