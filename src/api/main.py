"""
FastAPI application for Narrative Gravity Analysis.
Implements Epic 1: Corpus & Job Management Backend API endpoints.
"""

from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import logging
from datetime import datetime

from ..models.base import get_db
from . import schemas, crud, services
from .auth import get_current_user  # For future authentication

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Narrative Gravity Analysis API",
    description="Epic 1: Corpus & Job Management Backend for consequential narratives analysis",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Add CORS middleware for web interface integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],  # Streamlit default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/api/health")
async def health_check(db: Session = Depends(get_db)):
    """Health check endpoint to verify API and database connectivity."""
    try:
        # Test database connection
        from sqlalchemy import text
        db.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "database": "connected",
            "version": "1.0.0"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service unhealthy"
        )

# Corpus Management Endpoints

@app.post("/api/corpora/upload", response_model=schemas.CorpusResponse)
async def upload_corpus(
    file: UploadFile = File(...),
    name: Optional[str] = None,
    description: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Upload and ingest a JSONL corpus file.
    Validates each record against core schema and creates corpus + documents + chunks.
    """
    try:
        if not file.filename.endswith('.jsonl'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File must be a .jsonl file"
            )
        
        # Read and parse JSONL file
        content = await file.read()
        corpus_name = name or file.filename.replace('.jsonl', '')
        
        # Use the ingestion service to process the file
        corpus = await services.ingest_jsonl_corpus(
            content=content,
            name=corpus_name,
            description=description,
            db=db
        )
        
        logger.info(f"Successfully ingested corpus: {corpus.name} with {corpus.record_count} records")
        return corpus
        
    except Exception as e:
        logger.error(f"Corpus upload failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Upload failed: {str(e)}"
        )

@app.get("/api/corpora", response_model=List[schemas.CorpusResponse])
async def list_corpora(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all uploaded corpora with metadata."""
    corpora = crud.get_corpora(db, skip=skip, limit=limit)
    return corpora

@app.get("/api/corpora/{corpus_id}/documents", response_model=List[schemas.DocumentResponse])
async def list_corpus_documents(
    corpus_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List documents in a specific corpus with metadata."""
    documents = crud.get_corpus_documents(db, corpus_id=corpus_id, skip=skip, limit=limit)
    if not documents:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Corpus not found or has no documents"
        )
    return documents

@app.get("/api/corpora/{corpus_id}/chunks", response_model=List[schemas.ChunkResponse])
async def list_corpus_chunks(
    corpus_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List chunks in a specific corpus with metadata."""
    chunks = crud.get_corpus_chunks(db, corpus_id=corpus_id, skip=skip, limit=limit)
    if not chunks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Corpus not found or has no chunks"
        )
    return chunks

# Job Management Endpoints

@app.post("/api/jobs", response_model=schemas.JobResponse)
async def create_job(
    job_request: schemas.JobCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new processing job for selected texts, frameworks, and models.
    Enqueues tasks for batch processing.
    """
    try:
        job = await services.create_processing_job(
            job_request=job_request,
            db=db
        )
        
        logger.info(f"Created job {job.id} with {job.total_tasks} tasks")
        return job
        
    except Exception as e:
        logger.error(f"Job creation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Job creation failed: {str(e)}"
        )

@app.get("/api/jobs", response_model=List[schemas.JobResponse])
async def list_jobs(
    skip: int = 0,
    limit: int = 100,
    status_filter: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List processing jobs with optional status filtering."""
    jobs = crud.get_jobs(db, skip=skip, limit=limit, status_filter=status_filter)
    return jobs

@app.get("/api/jobs/{job_id}", response_model=schemas.JobDetailResponse)
async def get_job_detail(
    job_id: int,
    db: Session = Depends(get_db)
):
    """Get detailed job information including task status breakdown."""
    job_detail = crud.get_job_with_tasks(db, job_id=job_id)
    if not job_detail:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    return job_detail

@app.post("/api/jobs/{job_id}/resume")
async def resume_job(
    job_id: int,
    db: Session = Depends(get_db)
):
    """Resume a failed or cancelled job from the last successful checkpoint."""
    try:
        result = await services.resume_job(job_id=job_id, db=db)
        return {"message": f"Job {job_id} resumed", "tasks_requeued": result}
    except Exception as e:
        logger.error(f"Job resume failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Resume failed: {str(e)}"
        )

# Task Status Endpoints

@app.get("/api/tasks/{task_id}", response_model=schemas.TaskResponse)
async def get_task_detail(
    task_id: int,
    db: Session = Depends(get_db)
):
    """Get detailed information about a specific task."""
    task = crud.get_task(db, task_id=task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task

# Administrative Endpoints

@app.get("/api/stats", response_model=schemas.SystemStats)
async def get_system_stats(db: Session = Depends(get_db)):
    """Get system-wide statistics for monitoring."""
    stats = crud.get_system_statistics(db)
    return stats

@app.get("/api/metrics")
async def get_system_metrics():
    """Get detailed system metrics including success rates and costs."""
    from ..utils.logging_config import metrics_collector
    return metrics_collector.get_summary()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 