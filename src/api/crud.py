"""
CRUD operations for Narrative Gravity Analysis database.
Implements database queries for Epic 1 corpus and job management.
"""

from sqlalchemy.orm import Session, selectinload
from sqlalchemy import and_, func, text
from typing import List, Optional, Dict, Any
from datetime import datetime

from ..models.models import Corpus, Document, Chunk, Job, Task
from . import schemas

# Corpus CRUD operations

def get_corpora(db: Session, skip: int = 0, limit: int = 100) -> List[Corpus]:
    """Get list of all corpora with pagination."""
    return db.query(Corpus).offset(skip).limit(limit).all()

def get_corpus(db: Session, corpus_id: int) -> Optional[Corpus]:
    """Get a specific corpus by ID."""
    return db.query(Corpus).filter(Corpus.id == corpus_id).first()

def create_corpus(db: Session, name: str, description: Optional[str] = None) -> Corpus:
    """Create a new corpus."""
    corpus = Corpus(
        name=name,
        description=description,
        record_count=0  # Will be updated as documents are added
    )
    db.add(corpus)
    db.commit()
    db.refresh(corpus)
    return corpus

def update_corpus_record_count(db: Session, corpus_id: int, count: int) -> None:
    """Update the record count for a corpus."""
    db.query(Corpus).filter(Corpus.id == corpus_id).update({"record_count": count})
    db.commit()

# Document CRUD operations

def get_corpus_documents(
    db: Session, 
    corpus_id: int, 
    skip: int = 0, 
    limit: int = 100
) -> List[Document]:
    """Get documents for a specific corpus."""
    return (
        db.query(Document)
        .filter(Document.corpus_id == corpus_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_document_by_text_id(db: Session, text_id: str) -> Optional[Document]:
    """Get a document by its text_id."""
    return db.query(Document).filter(Document.text_id == text_id).first()

def create_document(
    db: Session,
    corpus_id: int,
    document_data: schemas.DocumentBase
) -> Document:
    """Create a new document."""
    document = Document(
        corpus_id=corpus_id,
        text_id=document_data.text_id,
        title=document_data.title,
        document_type=document_data.document_type,
        author=document_data.author,
        date=document_data.date,
        publication=document_data.publication,
        medium=document_data.medium,
        campaign_name=document_data.campaign_name,
        audience_size=document_data.audience_size,
        source_url=document_data.source_url,
        schema_version=document_data.schema_version,
        document_metadata=document_data.document_metadata
    )
    db.add(document)
    db.commit()
    db.refresh(document)
    return document

# Chunk CRUD operations

def get_corpus_chunks(
    db: Session,
    corpus_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[Chunk]:
    """Get chunks for a specific corpus."""
    return (
        db.query(Chunk)
        .join(Document)
        .filter(Document.corpus_id == corpus_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_document_chunks(db: Session, document_id: int) -> List[Chunk]:
    """Get all chunks for a specific document."""
    return (
        db.query(Chunk)
        .filter(Chunk.document_id == document_id)
        .order_by(Chunk.chunk_id)
        .all()
    )

def create_chunk(
    db: Session,
    document_id: int,
    chunk_data: schemas.ChunkBase
) -> Chunk:
    """Create a new chunk."""
    chunk = Chunk(
        document_id=document_id,
        chunk_id=chunk_data.chunk_id,
        total_chunks=chunk_data.total_chunks,
        chunk_type=chunk_data.chunk_type,
        chunk_size=chunk_data.chunk_size,
        chunk_overlap=chunk_data.chunk_overlap,
        document_position=chunk_data.document_position,
        word_count=chunk_data.word_count,
        unique_words=chunk_data.unique_words,
        word_density=chunk_data.word_density,
        chunk_content=chunk_data.chunk_content,
        framework_data=chunk_data.framework_data
    )
    db.add(chunk)
    db.commit()
    db.refresh(chunk)
    return chunk

def get_chunks_by_text_ids(db: Session, text_ids: List[str]) -> List[Chunk]:
    """Get all chunks for documents with specified text_ids."""
    return (
        db.query(Chunk)
        .join(Document)
        .filter(Document.text_id.in_(text_ids))
        .all()
    )

# Job CRUD operations

def get_jobs(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    status_filter: Optional[str] = None
) -> List[Job]:
    """Get list of jobs with optional status filtering."""
    query = db.query(Job)
    if status_filter:
        query = query.filter(Job.status == status_filter)
    return query.offset(skip).limit(limit).all()

def get_job(db: Session, job_id: int) -> Optional[Job]:
    """Get a specific job by ID."""
    return db.query(Job).filter(Job.id == job_id).first()

def create_job(db: Session, job_data: schemas.JobCreate) -> Job:
    """Create a new job."""
    job = Job(
        corpus_id=job_data.corpus_id,
        job_name=job_data.job_name,
        text_ids=job_data.text_ids,
        frameworks=job_data.frameworks,
        models=job_data.models,
        run_count=job_data.run_count,
        job_config=job_data.job_config,
        status="pending"
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return job

def update_job_status(
    db: Session,
    job_id: int,
    status: str,
    started_at: Optional[datetime] = None,
    completed_at: Optional[datetime] = None
) -> None:
    """Update job status and timestamps."""
    update_data = {"status": status}
    if started_at:
        update_data["started_at"] = started_at
    if completed_at:
        update_data["completed_at"] = completed_at
    
    db.query(Job).filter(Job.id == job_id).update(update_data)
    db.commit()

def update_job_task_counts(db: Session, job_id: int) -> None:
    """Update job task completion counts based on current task statuses."""
    # Get task counts by status
    task_counts = (
        db.query(Task.status, func.count(Task.id))
        .filter(Task.job_id == job_id)
        .group_by(Task.status)
        .all()
    )
    
    completed_tasks = 0
    failed_tasks = 0
    total_tasks = 0
    
    for status, count in task_counts:
        total_tasks += count
        if status == "completed":
            completed_tasks = count
        elif status == "failed":
            failed_tasks = count
    
    # Update job record
    db.query(Job).filter(Job.id == job_id).update({
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "failed_tasks": failed_tasks
    })
    db.commit()

def get_job_with_tasks(db: Session, job_id: int) -> Optional[Dict[str, Any]]:
    """Get job with detailed task information."""
    job = (
        db.query(Job)
        .options(selectinload(Job.tasks))
        .filter(Job.id == job_id)
        .first()
    )
    
    if not job:
        return None
    
    # Calculate task status counts
    task_status_counts = {}
    for task in job.tasks:
        status = task.status
        task_status_counts[status] = task_status_counts.get(status, 0) + 1
    
    # Calculate progress percentage
    progress_percentage = 0.0
    if job.total_tasks > 0:
        progress_percentage = (job.completed_tasks / job.total_tasks) * 100
    
    return {
        **job.__dict__,
        "tasks": job.tasks,
        "task_status_counts": task_status_counts,
        "progress_percentage": progress_percentage
    }

# Task CRUD operations

def get_task(db: Session, task_id: int) -> Optional[Task]:
    """Get a specific task by ID."""
    return db.query(Task).filter(Task.id == task_id).first()

def create_task(
    db: Session,
    job_id: int,
    chunk_id: int,
    framework: str,
    model: str,
    run_number: int
) -> Task:
    """Create a new task."""
    task = Task(
        job_id=job_id,
        chunk_id=chunk_id,
        framework=framework,
        model=model,
        run_number=run_number,
        status="pending"
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def update_task_status(
    db: Session,
    task_id: int,
    status: str,
    result_data: Optional[Dict[str, Any]] = None,
    error_message: Optional[str] = None,
    api_cost: Optional[float] = None
) -> None:
    """Update task status and results."""
    update_data = {
        "status": status,
        "updated_at": datetime.utcnow()
    }
    
    if status == "running":
        update_data["started_at"] = datetime.utcnow()
    elif status in ["completed", "failed"]:
        update_data["finished_at"] = datetime.utcnow()
    
    if result_data:
        update_data["result_data"] = result_data
    
    if error_message:
        update_data["last_error"] = error_message
        # Increment error count
        task = db.query(Task).filter(Task.id == task_id).first()
        if task:
            update_data["error_count"] = task.error_count + 1
    
    if api_cost:
        update_data["api_cost"] = api_cost
    
    db.query(Task).filter(Task.id == task_id).update(update_data)
    db.commit()

def get_failed_tasks_for_job(db: Session, job_id: int) -> List[Task]:
    """Get all failed tasks for a job (for resuming)."""
    return (
        db.query(Task)
        .filter(and_(Task.job_id == job_id, Task.status == "failed"))
        .all()
    )

def get_pending_tasks_for_job(db: Session, job_id: int) -> List[Task]:
    """Get all pending tasks for a job."""
    return (
        db.query(Task)
        .filter(and_(Task.job_id == job_id, Task.status == "pending"))
        .all()
    )

# System statistics

def get_system_statistics(db: Session) -> schemas.SystemStats:
    """Get system-wide statistics for monitoring."""
    # Get basic counts
    total_corpora = db.query(func.count(Corpus.id)).scalar()
    total_documents = db.query(func.count(Document.id)).scalar()
    total_chunks = db.query(func.count(Chunk.id)).scalar()
    total_jobs = db.query(func.count(Job.id)).scalar()
    
    # Get job status counts
    active_jobs = db.query(func.count(Job.id)).filter(
        Job.status.in_(["pending", "running"])
    ).scalar()
    
    failed_jobs = db.query(func.count(Job.id)).filter(
        Job.status == "failed"
    ).scalar()
    
    # Get task counts
    total_tasks = db.query(func.count(Task.id)).scalar()
    completed_tasks = db.query(func.count(Task.id)).filter(
        Task.status == "completed"
    ).scalar()
    failed_tasks = db.query(func.count(Task.id)).filter(
        Task.status == "failed"
    ).scalar()
    
    # Database size (PostgreSQL specific)
    try:
        db_size_result = db.execute(
            text("SELECT pg_database_size(current_database()) / 1024.0 / 1024.0 as size_mb")
        )
        database_size_mb = db_size_result.fetchone()[0]
    except Exception:
        database_size_mb = None
    
    # Determine system health
    system_health = "healthy"
    if failed_jobs > total_jobs * 0.1:  # More than 10% jobs failed
        system_health = "degraded"
    if active_jobs == 0 and total_jobs > 0:
        system_health = "idle"
    
    return schemas.SystemStats(
        total_corpora=total_corpora,
        total_documents=total_documents,
        total_chunks=total_chunks,
        total_jobs=total_jobs,
        active_jobs=active_jobs,
        failed_jobs=failed_jobs,
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        failed_tasks=failed_tasks,
        system_health=system_health,
        database_size_mb=database_size_mb
    ) 