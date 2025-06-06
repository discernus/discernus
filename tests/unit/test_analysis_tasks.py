import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime

# Add the project root to the Python path
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.tasks import analysis_tasks
from src.api.schemas import TaskStatus
from src.models.models import Task, Chunk

class TestAnalysisTasks:
    """Unit tests for Celery analysis tasks."""

    @pytest.fixture
    def mock_db_session(self):
        """Fixture for a mocked database session."""
        return MagicMock()

    @patch('src.tasks.analysis_tasks.analyze_political_spectrum')
    @patch('src.tasks.analysis_tasks.analyze_moral_rhetorical_posture')
    @patch('src.tasks.analysis_tasks.analyze_civic_virtue')
    @patch('src.tasks.analysis_tasks._update_job_progress')
    @patch('src.tasks.analysis_tasks._update_chunk_framework_data')
    @patch('src.tasks.analysis_tasks.crud')
    @patch('src.tasks.analysis_tasks.get_db_session')
    def test_process_task_success(
        self, mock_get_db, mock_crud, mock_update_chunk, 
        mock_update_job, mock_analyze_cv, mock_analyze_mrp, mock_analyze_ps, mock_db_session
    ):
        """Tests the successful processing of a single task for each framework."""
        mock_get_db.return_value = mock_db_session
        
        # Test Civic Virtue
        task_cv = Task(id=1, job_id=1, chunk_id=1, framework="civic_virtue", model="gpt-4", status="pending")
        chunk = Chunk(id=1, chunk_content="CV test")
        mock_crud.get_task.return_value = task_cv
        mock_crud.get_chunk_by_id.return_value = chunk
        mock_analyze_cv.return_value = ({"cv_result": "ok"}, 0.01)
        
        analysis_tasks.process_narrative_analysis_task(1)
        mock_analyze_cv.assert_called_once_with("CV test", "gpt-4")

        # Test Moral Rhetorical Posture
        task_mrp = Task(id=2, job_id=1, chunk_id=1, framework="moral_rhetorical_posture", model="gpt-4", status="pending")
        mock_crud.get_task.return_value = task_mrp
        mock_analyze_mrp.return_value = ({"mrp_result": "ok"}, 0.02)
        
        analysis_tasks.process_narrative_analysis_task(2)
        mock_analyze_mrp.assert_called_once_with("CV test", "gpt-4")

        # Test Political Spectrum
        task_ps = Task(id=3, job_id=1, chunk_id=1, framework="political_spectrum", model="gpt-4", status="pending")
        mock_crud.get_task.return_value = task_ps
        mock_analyze_ps.return_value = ({"ps_result": "ok"}, 0.03)
        
        analysis_tasks.process_narrative_analysis_task.run(3)
        mock_analyze_ps.assert_called_once_with("CV test", "gpt-4")
        
    @patch('src.tasks.analysis_tasks.crud')
    @patch('src.tasks.analysis_tasks.get_db_session')
    def test_process_task_not_found(self, mock_get_db, mock_crud, mock_db_session):
        """Tests that a TaskExecutionError is raised if the task is not found."""
        mock_get_db.return_value = mock_db_session
        mock_crud.get_task.return_value = None
        
        task_instance = analysis_tasks.process_narrative_analysis_task
        
        with pytest.raises(analysis_tasks.TaskExecutionError, match="Task 99 not found"):
            task_instance.run(99)
            
    @patch('src.tasks.analysis_tasks._update_job_progress')
    @patch('src.tasks.analysis_tasks.crud')
    @patch('src.tasks.analysis_tasks.get_db_session')
    def test_process_task_unknown_framework(self, mock_get_db, mock_crud, mock_update_job, mock_db_session):
        """Tests that a TaskExecutionError is raised for an unknown framework."""
        mock_get_db.return_value = mock_db_session
        task = Task(id=1, job_id=1, framework="unknown")
        mock_crud.get_task.return_value = task
        mock_crud.get_chunk_by_id.return_value = Chunk(id=1, chunk_content="")
        
        task_instance = analysis_tasks.process_narrative_analysis_task
        
        with pytest.raises(analysis_tasks.TaskExecutionError, match="Unknown framework: unknown"):
            task_instance.run(1) 