import pytest
import os
from unittest.mock import patch
from celery import Celery

# Add the project root to the Python path
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

@patch.dict(os.environ, {"REDIS_URL": "redis://test-redis:6379/0"})
def test_celery_app_creation():
    """
    Tests that the Celery app is created with the correct configuration.
    """
    from celery_app import celery_app
    
    assert isinstance(celery_app, Celery)
    assert celery_app.main == "narrative_gravity_analysis"
    assert celery_app.conf.broker_url == "redis://test-redis:6379/0"
    assert celery_app.conf.result_backend == "redis://test-redis:6379/0"
    assert "src.tasks.analysis_tasks" in celery_app.conf.include 