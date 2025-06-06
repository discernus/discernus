#!/usr/bin/env python3
"""
Start Celery worker for narrative analysis task processing.
Part of Epic 1: Queue & Orchestration implementation.
"""

import os
import sys
from src.celery_app import celery_app

def start_worker():
    """Start the Celery worker with appropriate configuration."""
    print("🔄 Starting Narrative Gravity Analysis Celery Worker")
    print("=" * 55)
    print("Worker will process narrative analysis tasks")
    print("Press Ctrl+C to stop")
    print("=" * 55)
    
    # Start worker with appropriate options for development
    celery_app.worker_main([
        'worker',
        '--loglevel=info',
        '--pool=solo',  # Required for macOS development
        '--concurrency=2',
        '--queues=analysis,celery',  # Process both analysis and default queues
    ])

if __name__ == "__main__":
    try:
        start_worker()
    except KeyboardInterrupt:
        print("\n👋 Celery worker stopped")
        sys.exit(0) 