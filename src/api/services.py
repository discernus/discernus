"""
Business logic services for Narrative Gravity Analysis.
Implements JSONL ingestion, job orchestration, and task management for Epic 1.
"""

import json
import jsonschema
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from datetime import datetime
import logging

from . import crud, schemas
from ..models.models import Corpus, Job, Task

logger = logging.getLogger(__name__)

class ValidationError(Exception):
    """Custom exception for validation errors."""
    def __init__(self, line_number: int, errors: List[str], raw_content: str = None):
        self.line_number = line_number
        self.errors = errors
        self.raw_content = raw_content
        super().__init__(f"Validation error at line {line_number}: {', '.join(errors)}")

class IngestionError(Exception):
    """Custom exception for ingestion errors."""
    pass

async def ingest_jsonl_corpus(
    content: bytes,
    name: str,
    description: Optional[str],
    db: Session
) -> Corpus:
    """
    Ingest a JSONL corpus file with full validation.
    Creates corpus, documents, and chunks from validated JSONL records.
    """
    try:
        # Decode content
        text_content = content.decode('utf-8')
        lines = text_content.strip().split('\n')
        
        if not lines or not lines[0].strip():
            raise IngestionError("Empty file or no valid JSON lines found")
        
        # Create corpus first
        corpus = crud.create_corpus(db, name=name, description=description)
        logger.info(f"Created corpus {corpus.id}: {name}")
        
        # Track documents to avoid duplicates
        processed_documents = {}
        validation_errors = []
        total_chunks = 0
        
        # Process each line
        for line_num, line in enumerate(lines, 1):
            if not line.strip():
                continue
                
            try:
                # Parse JSON
                record_data = json.loads(line)
                
                # Validate against schema
                try:
                    record = schemas.JSONLRecord.parse_obj(record_data)
                except Exception as e:
                    validation_errors.append(
                        schemas.ValidationErrorResponse(
                            line_number=line_num,
                            error_type="schema_validation",
                            field_errors={"validation": [str(e)]},
                            raw_content=line[:200] + "..." if len(line) > 200 else line
                        )
                    )
                    continue
                
                # Create or get document
                text_id = record.document.text_id
                if text_id not in processed_documents:
                    # Check if document already exists
                    existing_doc = crud.get_document_by_text_id(db, text_id)
                    if existing_doc:
                        logger.warning(f"Document {text_id} already exists, skipping")
                        continue
                    
                    # Create new document
                    document = crud.create_document(
                        db=db,
                        corpus_id=corpus.id,
                        document_data=record.document
                    )
                    processed_documents[text_id] = document
                    logger.debug(f"Created document {text_id}")
                else:
                    document = processed_documents[text_id]
                
                # Create chunk
                chunk = crud.create_chunk(
                    db=db,
                    document_id=document.id,
                    chunk_data=record
                )
                total_chunks += 1
                logger.debug(f"Created chunk {chunk.chunk_id} for document {text_id}")
                
            except json.JSONDecodeError as e:
                validation_errors.append(
                    schemas.ValidationErrorResponse(
                        line_number=line_num,
                        error_type="json_parse",
                        field_errors={"json": [f"Invalid JSON: {str(e)}"]},
                        raw_content=line[:200] + "..." if len(line) > 200 else line
                    )
                )
                continue
            except Exception as e:
                logger.error(f"Unexpected error processing line {line_num}: {e}")
                validation_errors.append(
                    schemas.ValidationErrorResponse(
                        line_number=line_num,
                        error_type="processing_error",
                        field_errors={"processing": [str(e)]},
                        raw_content=line[:200] + "..." if len(line) > 200 else line
                    )
                )
                continue
        
        # Update corpus record count
        crud.update_corpus_record_count(db, corpus.id, total_chunks)
        
        # If we have validation errors, include them in response
        if validation_errors:
            logger.warning(f"Corpus {name} ingested with {len(validation_errors)} validation errors")
            # For now, we'll continue with successful records
            # In production, you might want to implement stricter validation
        
        logger.info(f"Successfully ingested corpus {name}: {len(processed_documents)} documents, {total_chunks} chunks")
        return corpus
        
    except Exception as e:
        logger.error(f"Corpus ingestion failed: {e}")
        # Clean up corpus if created
        if 'corpus' in locals():
            try:
                db.delete(corpus)
                db.commit()
            except Exception:
                pass
        raise IngestionError(f"Ingestion failed: {str(e)}")

async def create_processing_job(
    job_request: schemas.JobCreate,
    db: Session
) -> Job:
    """
    Create a processing job and enqueue tasks for all chunk/framework/model/run combinations.
    """
    try:
        # Validate corpus exists
        corpus = crud.get_corpus(db, job_request.corpus_id)
        if not corpus:
            raise ValueError(f"Corpus {job_request.corpus_id} not found")
        
        # Get chunks for specified text_ids
        chunks = crud.get_chunks_by_text_ids(db, job_request.text_ids)
        if not chunks:
            raise ValueError(f"No chunks found for text_ids: {job_request.text_ids}")
        
        # Create job
        job = crud.create_job(db, job_request)
        logger.info(f"Created job {job.id} for corpus {corpus.name}")
        
        # Calculate total tasks
        total_tasks = len(chunks) * len(job_request.frameworks) * len(job_request.models) * job_request.run_count
        
        # Create tasks for each combination
        task_count = 0
        for chunk in chunks:
            for framework in job_request.frameworks:
                for model in job_request.models:
                    for run_number in range(1, job_request.run_count + 1):
                        task = crud.create_task(
                            db=db,
                            job_id=job.id,
                            chunk_id=chunk.id,
                            framework=framework,
                            model=model,
                            run_number=run_number
                        )
                        task_count += 1
                        
                        # TODO: Enqueue task for Celery processing
                        # await enqueue_analysis_task(task.id)
        
        # Update job with task count
        crud.update_job_task_counts(db, job.id)
        
        logger.info(f"Created {task_count} tasks for job {job.id}")
        return job
        
    except Exception as e:
        logger.error(f"Job creation failed: {e}")
        raise e

async def resume_job(job_id: int, db: Session) -> int:
    """
    Resume a failed job by re-queueing failed and pending tasks.
    """
    try:
        job = crud.get_job(db, job_id)
        if not job:
            raise ValueError(f"Job {job_id} not found")
        
        if job.status not in ["failed", "cancelled"]:
            raise ValueError(f"Job {job_id} cannot be resumed (status: {job.status})")
        
        # Get failed and pending tasks
        failed_tasks = crud.get_failed_tasks_for_job(db, job_id)
        pending_tasks = crud.get_pending_tasks_for_job(db, job_id)
        
        tasks_to_resume = failed_tasks + pending_tasks
        
        if not tasks_to_resume:
            logger.info(f"No tasks to resume for job {job_id}")
            return 0
        
        # Reset task statuses and re-queue
        requeued_count = 0
        for task in tasks_to_resume:
            # Reset failed tasks to pending
            if task.status == "failed":
                crud.update_task_status(db, task.id, "pending")
            
            # TODO: Re-enqueue task for Celery processing
            # await enqueue_analysis_task(task.id)
            requeued_count += 1
        
        # Update job status
        crud.update_job_status(db, job_id, "running", started_at=datetime.utcnow())
        
        logger.info(f"Resumed job {job_id}: {requeued_count} tasks requeued")
        return requeued_count
        
    except Exception as e:
        logger.error(f"Job resume failed: {e}")
        raise e

# Schema validation utilities

def load_core_schema() -> Dict[str, Any]:
    """Load the core JSON schema for validation."""
    # TODO: Load from schemas/core_schema_v1.0.0.json
    # For now, return a basic schema structure
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "required": [
            "document", "chunk_id", "total_chunks", "chunk_type", 
            "chunk_size", "document_position", "word_count", 
            "unique_words", "word_density", "chunk_content"
        ],
        "properties": {
            "document": {
                "type": "object",
                "required": ["text_id", "title", "document_type", "author", "date", "schema_version"],
                "properties": {
                    "text_id": {"type": "string"},
                    "title": {"type": "string"},
                    "document_type": {"type": "string"},
                    "author": {"type": "string"},
                    "date": {"type": "string", "format": "date-time"},
                    "schema_version": {"type": "string", "pattern": "^\\d+\\.\\d+\\.\\d+$"}
                }
            },
            "chunk_id": {"type": "integer", "minimum": 0},
            "total_chunks": {"type": "integer", "minimum": 1},
            "chunk_type": {"type": "string", "enum": ["fixed", "sectional", "semantic"]},
            "chunk_size": {"type": "integer", "minimum": 1},
            "document_position": {"type": "number", "minimum": 0.0, "maximum": 1.0},
            "word_count": {"type": "integer", "minimum": 0},
            "unique_words": {"type": "integer", "minimum": 0},
            "word_density": {"type": "number", "minimum": 0.0, "maximum": 1.0},
            "chunk_content": {"type": "string", "minLength": 1},
            "framework_data": {"type": "object"}
        }
    }

def validate_jsonl_record(record: Dict[str, Any], schema: Dict[str, Any]) -> List[str]:
    """
    Validate a single JSONL record against the schema.
    Returns list of validation errors.
    """
    try:
        jsonschema.validate(record, schema)
        return []
    except jsonschema.ValidationError as e:
        return [str(e)]
    except Exception as e:
        return [f"Validation error: {str(e)}"]

# Cost estimation utilities

def estimate_job_cost(
    chunk_count: int,
    frameworks: List[str],
    models: List[str],
    run_count: int
) -> float:
    """
    Estimate the cost of a processing job based on task count and model pricing.
    """
    # TODO: Implement actual cost calculation based on Hugging Face pricing
    # For now, use placeholder values
    
    base_cost_per_task = 0.01  # $0.01 per task as estimate
    total_tasks = chunk_count * len(frameworks) * len(models) * run_count
    
    # Apply model-specific multipliers
    model_multipliers = {
        "gpt-4": 2.0,
        "claude-3": 1.5,
        "gemini-pro": 1.0,
        "default": 1.0
    }
    
    total_cost = 0.0
    for model in models:
        multiplier = model_multipliers.get(model, model_multipliers["default"])
        model_cost = (total_tasks / len(models)) * base_cost_per_task * multiplier
        total_cost += model_cost
    
    return round(total_cost, 2)

# Framework validation

def validate_framework_compatibility(
    framework: str,
    chunk_data: Dict[str, Any]
) -> List[str]:
    """
    Validate that chunk data is compatible with the specified framework.
    """
    errors = []
    
    if framework == "civic_virtue":
        # Check for civic virtue specific requirements
        framework_data = chunk_data.get("framework_data", {})
        if "civic_virtue" not in framework_data:
            errors.append("civic_virtue framework data missing")
    
    elif framework == "moral_rhetorical_posture":
        # Check for MRP specific requirements
        framework_data = chunk_data.get("framework_data", {})
        if "moral_rhetorical_posture" not in framework_data:
            errors.append("moral_rhetorical_posture framework data missing")
    
    elif framework == "political_spectrum":
        # Check for political spectrum specific requirements
        framework_data = chunk_data.get("framework_data", {})
        if "political_spectrum" not in framework_data:
            errors.append("political_spectrum framework data missing")
    
    else:
        errors.append(f"Unknown framework: {framework}")
    
    return errors 