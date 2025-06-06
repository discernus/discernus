"""
Celery tasks for narrative analysis processing.
Implements the missing Epic 1 requirements: task processing, retry logic, and Hugging Face integration.
"""

import logging
import time
import requests
import os
from typing import Dict, Any, Optional
from datetime import datetime
from celery import current_task
from celery.exceptions import Retry

from ..celery_app import celery_app
from ..models.base import get_db_session
from ..api import crud
from sqlalchemy.orm import Session
from ..api.schemas import TaskStatus

logger = logging.getLogger(__name__)

# Hugging Face API configuration
HF_API_BASE = "https://api-inference.huggingface.co/models"
HF_HEADERS = {
    "Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_KEY', '')}"
}

class TaskExecutionError(Exception):
    """Custom exception for task execution errors."""
    pass

class RetryableError(Exception):
    """Exception for errors that should trigger a retry."""
    pass

@celery_app.task(bind=True, autoretry_for=(RetryableError,), retry_kwargs={'max_retries': 3})
def process_narrative_analysis_task(self, task_id: int) -> Dict[str, Any]:
    """
    Process a single narrative analysis task.
    
    This implements Epic 1 requirements:
    - C. Queue & Orchestration: Actual task processing
    - D. Resumability & Retry Logic: Automatic retry with exponential backoff
    
    Args:
        task_id: Database ID of the task to process
        
    Returns:
        Dict containing analysis results
        
    Raises:
        RetryableError: For transient failures that should be retried
        TaskExecutionError: For permanent failures
    """
    db = get_db_session()
    
    try:
        # Get task from database
        task = crud.get_task(db, task_id)
        if not task:
            raise TaskExecutionError(f"Task {task_id} not found")
        
        logger.info(f"Processing task {task_id}: {task.framework} analysis on chunk {task.chunk_id}")
        
        # Update task status to running
        crud.update_task_status(
            db, 
            task_id, 
            TaskStatus.running,
            api_cost=0.0
        )
        
        # Get the chunk content
        chunk = crud.get_chunk_by_id(db, task.chunk_id)
        if not chunk:
            raise TaskExecutionError(f"Chunk {task.chunk_id} not found")
        
        # Perform the analysis based on framework
        analysis_result = None
        api_cost = 0.0
        
        if task.framework == "civic_virtue":
            analysis_result, api_cost = analyze_civic_virtue(chunk.chunk_content, task.model)
        elif task.framework == "moral_rhetorical_posture":
            analysis_result, api_cost = analyze_moral_rhetorical_posture(chunk.chunk_content, task.model)
        elif task.framework == "political_spectrum":
            analysis_result, api_cost = analyze_political_spectrum(chunk.chunk_content, task.model)
        else:
            raise TaskExecutionError(f"Unknown framework: {task.framework}")
        
        # Store successful result in task and update chunk framework_data
        crud.update_task_status(
            db,
            task_id,
            TaskStatus.completed,
            result_data=analysis_result,
            api_cost=api_cost
        )
        
        # Update chunk's framework_data with analysis results
        _update_chunk_framework_data(db, chunk, task.framework, analysis_result)
        
        logger.info(f"Task {task_id} completed successfully")
        
        # Update job progress
        _update_job_progress(db, task.job_id)
        
        return {
            "task_id": task_id,
            "status": "completed",
            "framework": task.framework,
            "model": task.model,
            "run_number": task.run_number,
            "api_cost": api_cost,
            "result": analysis_result
        }
        
    except RetryableError as e:
        # Handle retryable errors with exponential backoff
        retry_count = self.request.retries
        delay = min(60 * (2 ** retry_count), 300)  # Max 5 minutes
        
        logger.warning(f"Task {task_id} failed (attempt {retry_count + 1}): {e}. Retrying in {delay}s")
        
        # Update task status
        crud.update_task_status(
            db,
            task_id,
            TaskStatus.retrying,
            error_message=str(e)
        )
        
        # Retry with exponential backoff
        raise self.retry(countdown=delay, exc=e)
        
    except TaskExecutionError as e:
        # Handle permanent errors
        logger.error(f"Task {task_id} failed permanently: {e}")
        
        crud.update_task_status(
            db,
            task_id,
            TaskStatus.failed,
            error_message=str(e)
        )
        
        # Update job status if all tasks failed
        if task:
            _update_job_progress(db, task.job_id)
        
        raise e
        
    except Exception as e:
        # Handle unexpected errors
        logger.error(f"Task {task_id} encountered unexpected error: {e}")
        
        crud.update_task_status(
            db,
            task_id,
            TaskStatus.failed,
            error_message=f"Unexpected error: {str(e)}"
        )
        
        raise TaskExecutionError(f"Unexpected error in task {task_id}: {e}")
        
    finally:
        db.close()

def analyze_civic_virtue(text: str, model: str) -> tuple[Dict[str, Any], float]:
    """
    Analyze text for civic virtue using Hugging Face models.
    
    Args:
        text: Text to analyze
        model: Hugging Face model name
        
    Returns:
        Tuple of (analysis_result, api_cost)
    """
    try:
        from .huggingface_client import HuggingFaceClient
        
        client = HuggingFaceClient()
        analysis_result, api_cost = client.analyze_text(text, "civic_virtue", model)
        
        return analysis_result, api_cost
        
    except Exception as e:
        logger.error(f"Civic virtue analysis failed: {e}")
        raise RetryableError(f"Civic virtue analysis failed: {e}")

def analyze_moral_rhetorical_posture(text: str, model: str) -> tuple[Dict[str, Any], float]:
    """
    Analyze text for moral rhetorical posture using Hugging Face models.
    
    Args:
        text: Text to analyze
        model: Hugging Face model name
        
    Returns:
        Tuple of (analysis_result, api_cost)
    """
    try:
        from .huggingface_client import HuggingFaceClient
        
        client = HuggingFaceClient()
        analysis_result, api_cost = client.analyze_text(text, "moral_rhetorical_posture", model)
        
        return analysis_result, api_cost
        
    except Exception as e:
        logger.error(f"Moral rhetorical posture analysis failed: {e}")
        raise RetryableError(f"Moral rhetorical posture analysis failed: {e}")

def analyze_political_spectrum(text: str, model: str) -> tuple[Dict[str, Any], float]:
    """
    Analyze text for political spectrum positioning using Hugging Face models.
    
    Args:
        text: Text to analyze
        model: Hugging Face model name
        
    Returns:
        Tuple of (analysis_result, api_cost)
    """
    try:
        from .huggingface_client import HuggingFaceClient
        
        client = HuggingFaceClient()
        analysis_result, api_cost = client.analyze_text(text, "political_spectrum", model)
        
        return analysis_result, api_cost
        
    except Exception as e:
        logger.error(f"Political spectrum analysis failed: {e}")
        raise RetryableError(f"Political spectrum analysis failed: {e}")

def call_huggingface_api(model: str, text: str, task_type: str = "text-classification") -> Dict[str, Any]:
    """
    Call Hugging Face Inference API with retry logic.
    
    Args:
        model: Hugging Face model name
        text: Text to analyze
        task_type: Type of analysis task
        
    Returns:
        API response data
        
    Raises:
        RetryableError: For retryable API errors
        TaskExecutionError: For permanent API errors
    """
    import os
    
    url = f"{HF_API_BASE}/{model}"
    headers = {
        "Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_KEY', '')}"
    }
    
    payload = {"inputs": text}
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        # Handle rate limiting
        if response.status_code == 429:
            retry_after = int(response.headers.get('Retry-After', 60))
            logger.warning(f"Rate limited by Hugging Face API. Retrying after {retry_after}s")
            raise RetryableError(f"Rate limited. Retry after {retry_after}s")
        
        # Handle server errors (retryable)
        if response.status_code >= 500:
            raise RetryableError(f"Hugging Face API server error: {response.status_code}")
        
        # Handle client errors (non-retryable)
        if response.status_code >= 400:
            raise TaskExecutionError(f"Hugging Face API client error: {response.status_code} - {response.text}")
        
        response.raise_for_status()
        return response.json()
        
    except requests.RequestException as e:
        logger.error(f"Hugging Face API request failed: {e}")
        raise RetryableError(f"API request failed: {e}")

def _extract_score(api_response: Dict[str, Any], label: str) -> float:
    """Extract score for a specific label from API response."""
    # Placeholder implementation - adjust based on actual API response format
    if isinstance(api_response, list) and api_response:
        for item in api_response:
            if isinstance(item, dict) and item.get('label', '').lower() == label.lower():
                return float(item.get('score', 0.0))
    return 0.0

def estimate_api_cost(text: str, model: str) -> float:
    """Estimate API cost based on text length and model."""
    # Rough estimation - adjust based on actual pricing
    base_cost = 0.001  # $0.001 per request
    length_multiplier = len(text) / 1000  # Additional cost per 1K characters
    return base_cost + (length_multiplier * 0.0001)

def _update_chunk_framework_data(db: Session, chunk, framework: str, analysis_result: Dict[str, Any]) -> None:
    """Update chunk's framework_data with analysis results."""
    try:
        # Get current framework_data or initialize
        current_framework_data = chunk.framework_data or {}
        
        # Ensure analysis_results section exists
        if 'analysis_results' not in current_framework_data:
            current_framework_data['analysis_results'] = {}
        
        # Store framework-specific results
        current_framework_data['analysis_results'][framework] = analysis_result
        
        # Update chunk in database
        chunk.framework_data = current_framework_data
        db.commit()
        
        logger.info(f"Updated framework_data for chunk {chunk.id} with {framework} results")
        
    except Exception as e:
        logger.error(f"Failed to update chunk framework_data: {e}")
        db.rollback()


def _update_job_progress(db, job_id: int):
    """Update job progress and status based on task completion."""
    # Update task counts
    crud.update_job_task_counts(db, job_id)
    
    # Get updated job
    job = crud.get_job(db, job_id)
    if not job:
        return
    
    # Check if job is complete
    if job.completed_tasks + job.failed_tasks >= job.total_tasks:
        if job.failed_tasks == job.total_tasks:
            # All tasks failed
            crud.update_job_status(db, job_id, "failed", completed_at=datetime.utcnow())
        elif job.failed_tasks > 0:
            # Some tasks failed, but some succeeded
            crud.update_job_status(db, job_id, "completed", completed_at=datetime.utcnow())
        else:
            # All tasks succeeded
            crud.update_job_status(db, job_id, "completed", completed_at=datetime.utcnow())
    
    logger.info(f"Job {job_id} progress: {job.completed_tasks}/{job.total_tasks} completed, {job.failed_tasks} failed") 