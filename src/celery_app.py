"""
Celery application configuration for Narrative Gravity Analysis.
Handles background processing of narrative analysis tasks.
"""

from celery import Celery
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create Celery app
celery_app = Celery(
    "narrative_gravity_analysis",
    broker=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    backend=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    include=["src.tasks.analysis_tasks"]
)

# Celery configuration
celery_app.conf.update(
    # Task settings
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    
    # Worker settings
    worker_pool="solo",  # Use solo pool for development on macOS
    worker_concurrency=2,
    worker_prefetch_multiplier=1,
    
    # Task execution settings
    task_soft_time_limit=300,  # 5 minutes soft limit
    task_time_limit=600,       # 10 minutes hard limit
    task_acks_late=True,
    worker_disable_rate_limits=True,
    
    # Retry settings
    task_default_retry_delay=60,    # 1 minute base delay
    task_max_retries=3,
    task_reject_on_worker_lost=True,
    
    # Result settings
    result_expires=3600,  # 1 hour
    result_backend_always_retry=True,
    
    # Monitoring
    worker_send_task_events=True,
    task_send_sent_event=True,
)

# Task routing (if needed for multiple queues later)
celery_app.conf.task_routes = {
    "src.tasks.analysis_tasks.*": {"queue": "analysis"},
}

if __name__ == "__main__":
    celery_app.start() 