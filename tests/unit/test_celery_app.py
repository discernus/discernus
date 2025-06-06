import pytest
import os
from unittest.mock import patch
from celery import Celery

# Add the project root to the Python path
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

def test_celery_app_creation():
    """
    Tests that the Celery app is created with the correct configuration.
    """
    with patch.dict(os.environ, {"REDIS_URL": "redis://test-redis:6379/0"}, clear=False):
        # Import inside the context to ensure env vars are picked up
        import importlib
        import sys
        
        # Clear the module cache to force reimport with new env vars
        if 'src.celery_app' in sys.modules:
            del sys.modules['src.celery_app']
        if 'celery_app' in sys.modules:
            del sys.modules['celery_app']
            
        from src.celery_app import celery_app
        
        assert isinstance(celery_app, Celery)
        assert celery_app.main == "narrative_gravity_analysis"
        assert celery_app.conf.broker_url == "redis://test-redis:6379/0"
        assert celery_app.conf.result_backend == "redis://test-redis:6379/0"
        assert "src.tasks.analysis_tasks" in celery_app.conf.include 