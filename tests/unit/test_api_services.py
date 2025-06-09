import pytest
import asyncio
from unittest.mock import patch, MagicMock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator
import sys
import os
import json
from datetime import datetime

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.narrative_gravity.api import services, crud, schemas
from src.narrative_gravity.models.models import Base, Corpus, Document, Chunk, Job, Task
from src.narrative_gravity.api.services import IngestionError, ValidationError

# --- Database Fixtures for In-Memory Testing (similar to test_crud) ---

@pytest.fixture(scope="module")
def db_engine():
    return create_engine("sqlite:///:memory:")

@pytest.fixture(scope="module")
def db_session(db_engine):
    Base.metadata.create_all(bind=db_engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
    yield SessionLocal
    Base.metadata.drop_all(bind=db_engine)

@pytest.fixture
def db(db_session) -> Generator:
    db_conn = db_session()
    try:
        for table in reversed(Base.metadata.sorted_tables):
            db_conn.execute(table.delete())
        db_conn.commit()
        yield db_conn
    finally:
        db_conn.close()

# --- Test Data Helpers ---
def create_valid_jsonl(docs=1, chunks_per_doc=1) -> bytes:
    lines = []
    for i in range(docs):
        for j in range(chunks_per_doc):
            record = {
                "document": {
                    "text_id": f"doc_{i+1}",
                    "title": f"Document {i+1}",
                    "document_type": "article",
                    "author": "Test Author",
                    "date": datetime(2023, 1, 1).isoformat(),
                    "schema_version": "1.0.0"
                },
                "chunk_id": j,
                "total_chunks": chunks_per_doc,
                "chunk_type": "fixed",
                "chunk_size": 50,
                "document_position": j / chunks_per_doc,
                "word_count": 10,
                "unique_words": 10,
                "word_density": 1.0,
                "chunk_content": f"This is chunk {j+1} of doc {i+1}."
            }
            lines.append(json.dumps(record))
    return "\n".join(lines).encode('utf-8')

class TestApiServices:
    """Unit tests for API service layer functions."""

    @pytest.mark.asyncio
    async def test_ingest_jsonl_corpus_success(self, db):
        """Tests successful ingestion of a valid JSONL file."""
        jsonl_content = create_valid_jsonl(docs=2, chunks_per_doc=3)
        
        corpus = await services.ingest_jsonl_corpus(
            content=jsonl_content,
            name="Test Corpus",
            description="A test.",
            uploader_id=None,
            db=db
        )
        
        assert corpus is not None
        assert corpus.name == "Test Corpus"
        
        db_corpus = crud.get_corpus(db, corpus.id)
        assert db_corpus.record_count == 6 # 2 docs * 3 chunks
        
        docs = crud.get_corpus_documents(db, corpus_id=corpus.id)
        assert len(docs) == 2
        
        chunks = crud.get_corpus_chunks(db, corpus_id=corpus.id)
        assert len(chunks) == 6
        
    @pytest.mark.asyncio
    async def test_ingest_jsonl_corpus_invalid_json(self, db):
        """Tests ingestion with invalid JSON content."""
        invalid_content = b'{"a": 1}\nthis is not json\n{"b": 2}'
        
        corpus = await services.ingest_jsonl_corpus(
            content=invalid_content,
            name="Invalid Corpus",
            description=None,
            uploader_id=None,
            db=db
        )

        # The service should still create a corpus but log errors.
        assert corpus is not None
        # Check that only the valid lines were processed
        assert crud.get_corpus(db, corpus.id).record_count == 0
        
    @pytest.mark.asyncio
    async def test_ingest_jsonl_corpus_schema_validation_error(self, db):
        """Tests ingestion with data that fails schema validation."""
        # Missing required 'document' field
        invalid_record = json.dumps({"chunk_id": 0}).encode('utf-8')
        
        corpus = await services.ingest_jsonl_corpus(
            content=invalid_record,
            name="Invalid Schema Corpus",
            description=None,
            uploader_id=None,
            db=db
        )
        
        # Corpus is created, but no records are ingested.
        assert corpus is not None
        assert crud.get_corpus(db, corpus.id).record_count == 0

    @pytest.mark.asyncio
    async def test_ingest_jsonl_empty_file_fails(self, db):
        """Tests that an empty or whitespace-only file raises an error."""
        with pytest.raises(IngestionError, match="Empty file"):
            await services.ingest_jsonl_corpus(b'', "Empty", None, None, db)
            
        with pytest.raises(IngestionError, match="Empty file"):
            await services.ingest_jsonl_corpus(b' \n \t \n ', "Whitespace", None, None, db)

    @pytest.mark.asyncio
    @patch('src.narrative_gravity.api.services.analysis_tasks.process_narrative_analysis_task.delay')
    async def test_create_processing_job_success(self, mock_delay, db):
        """Tests successful creation of a processing job."""
        # 1. Setup
        corpus = crud.create_corpus(db, name="Job Corpus")
        doc = Document(corpus_id=corpus.id, text_id="doc1", title="D1", document_type="article", author="A1", date=datetime.now(), schema_version="1.0.0")
        db.add(doc)
        db.commit()
        chunk1 = Chunk(document_id=doc.id, chunk_id=0, total_chunks=1, chunk_type="fixed", chunk_size=10, document_position=0, word_count=2, unique_words=2, word_density=1, chunk_content="c1")
        db.add(chunk1)
        db.commit()

        job_request = schemas.JobCreate(
            corpus_id=corpus.id,
            job_name="My Test Job",
            text_ids=["doc1"],
            frameworks=["civic_virtue", "moral_rhetorical_posture"],
            models=["gpt-4"],
            run_count=2
        )

        # 2. Execute
        job = await services.create_processing_job(job_request, creator_id=1, db=db)

        # 3. Assert
        assert job is not None
        assert job.job_name == "My Test Job"
        assert job.status == "pending"
        
        db.refresh(job)
        assert job.total_tasks == 4 # 1 chunk * 2 frameworks * 1 model * 2 runs
        assert job.completed_tasks == 0
        
        tasks = db.query(Task).filter(Task.job_id == job.id).all()
        assert len(tasks) == 4
        
        # Check that Celery task was called for each created task
        assert mock_delay.call_count == 4
        mock_delay.assert_any_call(tasks[0].id)

    @pytest.mark.asyncio
    async def test_create_processing_job_no_chunks_fails(self, db):
        """Tests that job creation fails if no chunks are found."""
        corpus = crud.create_corpus(db, name="Job Corpus")
        job_request = schemas.JobCreate(
            corpus_id=corpus.id,
            text_ids=["nonexistent_doc"],
            frameworks=["civic_virtue"],
            models=["gpt-4"]
        )
        
        with pytest.raises(ValueError, match="No chunks found"):
            await services.create_processing_job(job_request, creator_id=1, db=db)
            
    @pytest.mark.asyncio
    @patch('src.narrative_gravity.api.services.analysis_tasks.process_narrative_analysis_task.delay')
    async def test_resume_job_success(self, mock_delay, db):
        """Tests resuming a failed job."""
        # 1. Setup: Create a failed job with one failed and one pending task
        corpus = crud.create_corpus(db, name="Resume Corpus")
        doc = Document(corpus_id=corpus.id, text_id="doc1", title="D1", document_type="article", author="A1", date=datetime.now(), schema_version="1.0.0")
        db.add(doc)
        db.commit()
        chunk = Chunk(document_id=doc.id, chunk_id=0, total_chunks=1, chunk_type="fixed", chunk_size=10, document_position=0, word_count=2, unique_words=2, word_density=1, chunk_content="c1")
        db.add(chunk)
        job = Job(corpus_id=corpus.id, status="failed", text_ids=["doc1"], frameworks=["civic_virtue"], models=["gpt-4"])
        db.add(job)
        db.commit()
        task1 = Task(job_id=job.id, chunk_id=chunk.id, status="failed", framework="civic_virtue", model="gpt-4", run_number=1)
        task2 = Task(job_id=job.id, chunk_id=chunk.id, status="pending", framework="civic_virtue", model="gpt-4", run_number=2)
        db.add_all([task1, task2])
        db.commit()

        # 2. Execute
        requeued_count = await services.resume_job(job.id, db)

        # 3. Assert
        assert requeued_count == 2
        db.refresh(job)
        assert job.status == "running"
        
        db.refresh(task1)
        assert task1.status == "pending" # Failed task is reset to pending
        
        assert mock_delay.call_count == 2
        mock_delay.assert_any_call(task1.id)
        mock_delay.assert_any_call(task2.id)

    def test_estimate_job_cost(self):
        """Tests the cost estimation logic."""
        cost = services.estimate_job_cost(
            chunk_count=100,
            frameworks=["f1", "f2"],
            models=["m1", "m2", "m3"],
            run_count=5
        )
        # 100 * 2 * 3 * 5 * 0.01 = 30.0
        assert cost == 30.0
        
    def test_validate_framework_compatibility(self):
        """Tests the framework compatibility validator."""
        # Test case with missing framework data
        errors = services.validate_framework_compatibility("civic_virtue", {})
        assert len(errors) > 0
        assert "missing" in errors[0]

        # Test with valid data for civic_virtue
        valid_data = {"framework_data": {"civic_virtue": {}}}
        errors = services.validate_framework_compatibility("civic_virtue", valid_data)
        assert len(errors) == 0
        
        # Test with an unknown framework
        errors = services.validate_framework_compatibility("unknown_framework", {})
        assert len(errors) > 0
        assert "Unknown framework" in errors[0] 