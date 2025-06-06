import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator
import sys
import os
from datetime import datetime

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.api import crud, schemas
from src.models.models import Base, Corpus, Document, Chunk, Job, Task

# --- Database Fixtures for In-Memory Testing ---

@pytest.fixture(scope="module")
def db_engine():
    """Fixture for an in-memory SQLite database engine."""
    return create_engine("sqlite:///:memory:")

@pytest.fixture(scope="module")
def db_session(db_engine):
    """Fixture to create all tables and yield a session factory."""
    Base.metadata.create_all(bind=db_engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
    yield SessionLocal
    Base.metadata.drop_all(bind=db_engine)

@pytest.fixture
def db(db_session) -> Generator:
    """Fixture to get a clean database session for each test."""
    db_conn = db_session()
    try:
        # Clean up tables before each test
        for table in reversed(Base.metadata.sorted_tables):
            db_conn.execute(table.delete())
        db_conn.commit()
        yield db_conn
    finally:
        db_conn.close()

class TestCrudOperations:
    """
    Unit tests for the CRUD operations using an in-memory SQLite database.
    """

    # --- Helper methods ---
    def _create_test_document(self, db, corpus_id, doc_data_override=None):
        """Helper to create a document with default data."""
        defaults = {
            "text_id": "default_doc",
            "title": "Default Document",
            "document_type": "article",
            "author": "Default Author",
            "date": datetime(2023, 1, 1),
            "schema_version": "1.0.0"
        }
        if doc_data_override:
            defaults.update(doc_data_override)
        
        doc_data = schemas.DocumentBase(**defaults)
        return crud.create_document(db, corpus_id=corpus_id, document_data=doc_data)

    def _create_test_chunk(self, db, document_id, chunk_data_override=None):
        """Helper to create a chunk with default data."""
        defaults = {
            "chunk_id": 0,
            "total_chunks": 1,
            "chunk_type": "fixed",
            "chunk_size": 100,
            "document_position": 0.0,
            "word_count": 20,
            "unique_words": 15,
            "word_density": 0.75,
            "chunk_content": "This is a default test chunk content."
        }
        if chunk_data_override:
            defaults.update(chunk_data_override)

        chunk_data = schemas.ChunkBase(**defaults)
        return crud.create_chunk(db, document_id=document_id, chunk_data=chunk_data)


    # --- Corpus CRUD Tests ---
    def test_create_corpus(self, db):
        """Tests the creation of a new corpus."""
        corpus = crud.create_corpus(db, name="Test Corpus", description="A test.")
        
        assert corpus.id is not None
        assert corpus.name == "Test Corpus"
        assert corpus.description == "A test."
        
        # Verify it was committed to the DB
        retrieved = db.query(Corpus).filter(Corpus.id == corpus.id).first()
        assert retrieved is not None

    def test_get_corpus(self, db):
        """Tests retrieving a single corpus by its ID."""
        corpus = crud.create_corpus(db, name="Another Corpus")
        
        retrieved = crud.get_corpus(db, corpus_id=corpus.id)
        assert retrieved is not None
        assert retrieved.id == corpus.id
        assert retrieved.name == "Another Corpus"
        
        # Test getting a non-existent corpus
        assert crud.get_corpus(db, corpus_id=999) is None

    def test_get_corpora(self, db):
        """Tests retrieving a list of all corpora."""
        # Clear table to ensure clean state
        db.query(Corpus).delete()
        db.commit()
        
        crud.create_corpus(db, name="Corpus 1")
        crud.create_corpus(db, name="Corpus 2")
        
        corpora = crud.get_corpora(db)
        assert len(corpora) == 2
        
        # Test with limit
        corpora_limited = crud.get_corpora(db, limit=1)
        assert len(corpora_limited) == 1 

    # --- Document CRUD Tests ---
    def test_create_document(self, db):
        """Tests creating a new document linked to a corpus."""
        corpus = crud.create_corpus(db, name="Doc Corpus")
        doc = self._create_test_document(db, corpus.id, {"text_id": "doc1", "title": "Test Document"})
        
        assert doc.id is not None
        assert doc.corpus_id == corpus.id
        assert doc.text_id == "doc1"
        assert doc.title == "Test Document"
        
        retrieved = db.query(Document).filter(Document.id == doc.id).first()
        assert retrieved is not None

    def test_get_corpus_documents(self, db):
        """Tests retrieving documents for a specific corpus."""
        corpus1 = crud.create_corpus(db, name="Corpus with Docs")
        corpus2 = crud.create_corpus(db, name="Corpus without Docs")
        
        self._create_test_document(db, corpus1.id, {"text_id": "doc1"})
        self._create_test_document(db, corpus1.id, {"text_id": "doc2"})
        
        docs = crud.get_corpus_documents(db, corpus_id=corpus1.id)
        assert len(docs) == 2
        
        no_docs = crud.get_corpus_documents(db, corpus_id=corpus2.id)
        assert len(no_docs) == 0

    def test_get_document_by_text_id(self, db):
        """Tests retrieving a document by its unique text_id."""
        corpus = crud.create_corpus(db, name="Text ID Corpus")
        self._create_test_document(db, corpus.id, {"text_id": "unique_text_id"})
        
        doc = crud.get_document_by_text_id(db, text_id="unique_text_id")
        assert doc is not None
        assert doc.text_id == "unique_text_id"
        
        assert crud.get_document_by_text_id(db, text_id="nonexistent") is None

    # --- Chunk CRUD Tests ---
    def test_create_chunk(self, db):
        """Tests creating a new chunk for a document."""
        corpus = crud.create_corpus(db, name="Chunk Corpus")
        doc = self._create_test_document(db, corpus.id)
        
        chunk = self._create_test_chunk(db, doc.id, {"chunk_id": 0, "total_chunks": 1, "chunk_content": "This is a test chunk."})
        
        assert chunk.id is not None
        assert chunk.document_id == doc.id
        assert chunk.chunk_id == 0
        assert chunk.chunk_content == "This is a test chunk."
        
        retrieved = db.query(Chunk).filter(Chunk.id == chunk.id).first()
        assert retrieved is not None
        
    def test_get_document_chunks(self, db):
        """Tests retrieving all chunks for a specific document."""
        corpus = crud.create_corpus(db, name="Doc Chunk Corpus")
        doc1 = self._create_test_document(db, corpus.id, {"text_id": "doc1"})
        doc2 = self._create_test_document(db, corpus.id, {"text_id": "doc2"})
        
        self._create_test_chunk(db, doc1.id, {"chunk_id": 0, "total_chunks": 2, "chunk_content": "c1"})
        self._create_test_chunk(db, doc1.id, {"chunk_id": 1, "total_chunks": 2, "chunk_content": "c2"})

        chunks = crud.get_document_chunks(db, document_id=doc1.id)
        assert len(chunks) == 2
        
        no_chunks = crud.get_document_chunks(db, document_id=doc2.id)
        assert len(no_chunks) == 0

    def test_get_corpus_chunks(self, db):
        """Tests retrieving all chunks for a whole corpus."""
        corpus = crud.create_corpus(db, name="Corpus Chunk Corpus")
        doc1 = self._create_test_document(db, corpus.id, {"text_id": "doc1"})
        doc2 = self._create_test_document(db, corpus.id, {"text_id": "doc2"})
        
        self._create_test_chunk(db, doc1.id, {"chunk_id": 0, "total_chunks": 1})
        self._create_test_chunk(db, doc2.id, {"chunk_id": 0, "total_chunks": 2})
        self._create_test_chunk(db, doc2.id, {"chunk_id": 1, "total_chunks": 2})
        
        chunks = crud.get_corpus_chunks(db, corpus_id=corpus.id)
        assert len(chunks) == 3

    def test_get_chunk_by_id(self, db):
        """Tests retrieving a single chunk by its primary key ID."""
        corpus = crud.create_corpus(db, name="Chunk ID Corpus")
        doc = self._create_test_document(db, corpus.id)
        chunk = self._create_test_chunk(db, doc.id)
        
        retrieved = crud.get_chunk_by_id(db, chunk_id=chunk.id)
        assert retrieved is not None
        assert retrieved.id == chunk.id
        
        assert crud.get_chunk_by_id(db, chunk_id=999) is None
        
    def test_get_chunks_by_text_ids(self, db):
        """Tests retrieving chunks associated with a list of text_ids."""
        corpus = crud.create_corpus(db, name="Multi-doc Corpus")
        doc1 = self._create_test_document(db, corpus.id, {"text_id": "text1"})
        doc2 = self._create_test_document(db, corpus.id, {"text_id": "text2"})
        doc3 = self._create_test_document(db, corpus.id, {"text_id": "text3"})

        # Doc1 has 2 chunks
        self._create_test_chunk(db, doc1.id, {"chunk_id": 0, "total_chunks": 2})
        self._create_test_chunk(db, doc1.id, {"chunk_id": 1, "total_chunks": 2})
        
        # Doc2 has 1 chunk
        self._create_test_chunk(db, doc2.id, {"chunk_id": 0, "total_chunks": 1})

        # Doc3 has 1 chunk (should not be retrieved)
        self._create_test_chunk(db, doc3.id, {"chunk_id": 0, "total_chunks": 1})

        chunks = crud.get_chunks_by_text_ids(db, text_ids=["text1", "text2"])
        assert len(chunks) == 3

        chunks_one = crud.get_chunks_by_text_ids(db, text_ids=["text1"])
        assert len(chunks_one) == 2

        chunks_none = crud.get_chunks_by_text_ids(db, text_ids=["nonexistent"])
        assert len(chunks_none) == 0

    # --- Job CRUD Tests ---
    def test_create_job(self, db):
        """Tests creating a new job."""
        corpus = crud.create_corpus(db, name="Job Corpus")
        doc = self._create_test_document(db, corpus.id, {"text_id": "job_doc_1"})

        job_data = schemas.JobCreate(
            corpus_id=corpus.id,
            job_name="Test Job",
            text_ids=[doc.text_id],
            frameworks=["moral_rhetorical_posture"],
            models=["gpt-4"],
        )
        
        job = crud.create_job(db, job_data=job_data)
        
        assert job.id is not None
        assert job.corpus_id == corpus.id
        assert job.status == "pending"
        assert job.job_name == "Test Job"
        assert job.text_ids == [doc.text_id]

    def test_get_job(self, db):
        """Tests retrieving a single job."""
        corpus = crud.create_corpus(db, name="Job Corpus")
        doc = self._create_test_document(db, corpus.id, {"text_id": "job_doc_1"})
        job_data = schemas.JobCreate(corpus_id=corpus.id, text_ids=[doc.text_id], frameworks=["civic_virtue"], models=["m1"])
        job = crud.create_job(db, job_data=job_data)

        retrieved = crud.get_job(db, job_id=job.id)
        assert retrieved is not None
        assert retrieved.id == job.id

    def test_get_jobs_with_status_filter(self, db):
        """Tests retrieving jobs with a status filter."""
        corpus = crud.create_corpus(db, name="Job Corpus")
        doc = self._create_test_document(db, corpus.id, {"text_id": "job_doc_1"})
        job_data = schemas.JobCreate(corpus_id=corpus.id, text_ids=[doc.text_id], frameworks=["civic_virtue"], models=["m1"])
        
        job1 = crud.create_job(db, job_data=job_data)
        crud.update_job_status(db, job_id=job1.id, status="running")
        
        crud.create_job(db, job_data=job_data)

        running_jobs = crud.get_jobs(db, status_filter="running")
        assert len(running_jobs) == 1
        assert running_jobs[0].status == "running"

        pending_jobs = crud.get_jobs(db, status_filter="pending")
        assert len(pending_jobs) == 1
        assert pending_jobs[0].status == "pending"

    def test_update_job_status(self, db):
        """Tests updating a job's status."""
        corpus = crud.create_corpus(db, name="Job Corpus")
        doc = self._create_test_document(db, corpus.id, {"text_id": "job_doc_1"})
        job_data = schemas.JobCreate(corpus_id=corpus.id, text_ids=[doc.text_id], frameworks=["civic_virtue"], models=["m1"])
        job = crud.create_job(db, job_data=job_data)
        
        crud.update_job_status(db, job_id=job.id, status="completed", completed_at=datetime.utcnow())
        
        db.refresh(job)
        assert job.status == "completed"
        assert job.completed_at is not None

    # --- Task CRUD Tests ---
    def test_create_task(self, db):
        """Tests creating a new task for a job."""
        corpus = crud.create_corpus(db, name="Task Corpus")
        doc = self._create_test_document(db, corpus.id)
        chunk = self._create_test_chunk(db, doc.id)
        job_data = schemas.JobCreate(corpus_id=corpus.id, text_ids=[doc.text_id], frameworks=["civic_virtue"], models=["m1"])
        job = crud.create_job(db, job_data=job_data)

        task = crud.create_task(db, job_id=job.id, chunk_id=chunk.id, framework="civic_virtue", model="m1", run_number=1)

        assert task.id is not None
        assert task.job_id == job.id
        assert task.chunk_id == chunk.id
        assert task.status == "pending"

    def test_update_task_status(self, db):
        """Tests updating a task's status."""
        corpus = crud.create_corpus(db, name="Task Corpus")
        doc = self._create_test_document(db, corpus.id)
        chunk = self._create_test_chunk(db, doc.id)
        job_data = schemas.JobCreate(corpus_id=corpus.id, text_ids=[doc.text_id], frameworks=["civic_virtue"], models=["m1"])
        job = crud.create_job(db, job_data=job_data)
        task = crud.create_task(db, job_id=job.id, chunk_id=chunk.id, framework="civic_virtue", model="m1", run_number=1)

        crud.update_task_status(db, task_id=task.id, status="completed", result_data={"result": "success"}, api_cost=0.01)
        
        db.refresh(task)
        assert task.status == "completed"
        assert task.result_data == {"result": "success"}
        assert task.api_cost == 0.01

    def test_get_pending_tasks_for_job(self, db):
        """Tests retrieving pending tasks for a job."""
        corpus = crud.create_corpus(db, name="Task Corpus")
        doc = self._create_test_document(db, corpus.id)
        chunk = self._create_test_chunk(db, doc.id)
        job_data = schemas.JobCreate(corpus_id=corpus.id, text_ids=[doc.text_id], frameworks=["civic_virtue"], models=["m1"])
        job = crud.create_job(db, job_data=job_data)
        
        task1 = crud.create_task(db, job_id=job.id, chunk_id=chunk.id, framework="civic_virtue", model="m1", run_number=1)
        task2 = crud.create_task(db, job_id=job.id, chunk_id=chunk.id, framework="civic_virtue", model="m1", run_number=2)
        crud.update_task_status(db, task_id=task2.id, status="completed")

        pending_tasks = crud.get_pending_tasks_for_job(db, job_id=job.id)
        assert len(pending_tasks) == 1
        assert pending_tasks[0].id == task1.id
        assert pending_tasks[0].status == "pending"

    # --- Statistics Tests ---
    def test_get_system_statistics(self, db):
        """Tests retrieving system-wide statistics."""
        # Setup data
        corpus = crud.create_corpus(db, name="Stats Corpus")
        doc = self._create_test_document(db, corpus.id)
        chunk = self._create_test_chunk(db, doc.id)
        job_data = schemas.JobCreate(corpus_id=corpus.id, text_ids=[doc.text_id], frameworks=["civic_virtue"], models=["m1"])
        job = crud.create_job(db, job_data=job_data)
        crud.create_task(db, job_id=job.id, chunk_id=chunk.id, framework="civic_virtue", model="m1", run_number=1)

        # Get stats
        stats = crud.get_system_statistics(db)

        # Assertions
        assert stats.total_corpora == 1
        assert stats.total_documents == 1
        assert stats.total_chunks == 1
        assert stats.total_jobs == 1
        assert stats.total_tasks == 1
        assert stats.system_health == "healthy"