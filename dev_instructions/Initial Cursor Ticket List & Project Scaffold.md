# Initial Cursor Ticket List & Project Scaffold

---

## Project Folder Structure

narrative-gravity/ ├── README.md ├── requirements.txt ├── setup.py ├── docker-compose.yml ├── Dockerfile │ ├── schemas/ │ ├── core_schema.json │ ├── cv_extension_schema.json │ ├── mrp_extension_schema.json │ └── ps_extension_schema.json │ ├── corpus/ │ └── golden_set/ # 5–10 annotated sample JSONL files │ ├── src/ │ ├── api/ │ │ ├── **init**.py │ │ ├── health.py # /api/health endpoint │ │ └── corpora.py # corpora and documents/chunks endpoints │ │ └── jobs.py # job creation & status endpoints │ │ │ ├── models/ │ │ ├── **init**.py │ │ ├── corpus.py │ │ ├── document.py │ │ ├── chunk.py │ │ ├── job.py │ │ └── task.py │ │ │ ├── tasks/ │ │ ├── **init**.py │ │ ├── ingestion.py # JSONL ingestion & schema validation │ │ └── processing.py # enqueue & process Hugging Face calls │ │ │ ├── services/ │ │ ├── **init**.py │ │ ├── huggingface_client.py # wrapper, retry, cost-tracking │ │ └── cost_tracker.py # record usage & budgets │ │ │ ├── cli/ │ │ ├── **init**.py │ │ └── generate_jsonl.py # CLI to convert raw texts → JSONL │ │ │ └── utils/ │ ├── **init**.py │ ├── validation.py # JSON Schema loader & validator │ └── chunker.py # fixed, sectional, semantic chunk logic │ └── tests/ ├── test_health.py ├── test_ingestion.py ├── test_chunking.py ├── test_api_corpora.py └── test_job_lifecycle.py

---

## Initial Ticket List

### 1. Project Setup & CI  
- Ticket 1.1: Initialize Git repo, Python virtualenv, install core dependencies (FastAPI/Flask, Celery, Redis client, HF SDK, JSONSchema).  
- Ticket 1.2: Add `docker-compose.yml` for Redis, Celery worker, and API service.  
- Ticket 1.3: Configure CI pipeline (GitHub Actions or similar) to run lint, schema validation, and unit tests on push.

### 2. Schemas & Golden Set  
- Ticket 2.1: Copy core + extension JSON Schemas into `schemas/`.  
- Ticket 2.2: Create 5–10 “golden set” JSONL records in `corpus/golden_set/` for end-to-end tests.  
- Ticket 2.3: Write unit tests to validate these records against the core schema.

### 3. Health & Admin API Skeleton  
- Ticket 3.1: Implement `/api/health` endpoint returning service status.  
- Ticket 3.2: Scaffold corpora endpoints:  
  - `POST /api/corpora/upload`  
  - `GET  /api/corpora`  
- Ticket 3.3: Scaffold job endpoints:  
  - `POST /api/jobs`  
  - `GET  /api/jobs`  
  - `GET  /api/jobs/{job_id}`

### 4. Data Models & Database  
- Ticket 4.1: Define ORM models or SQLAlchemy schemas for Corpus, Document, Chunk, Job, Task.  
- Ticket 4.2: Create migrations or table-creation scripts.  
- Ticket 4.3: Write unit tests for CRUD operations on each model.

### 5. JSONL Ingestion & Validation  
- Ticket 5.1: Implement CLI `generate_jsonl.py` to read raw formats (CSV, Markdown) and emit JSONL chunks.  
- Ticket 5.2: Build ingestion task (`tasks/ingestion.py`) to parse uploaded JSONL, validate against schema, and persist Document & Chunk records.  
- Ticket 5.3: Integrate schema validation library (e.g. `jsonschema`) and report structured errors.

### 6. Chunking Logic  
- Ticket 6.1: Implement `utils/chunker.py` with fixed-size chunking (configurable size & overlap).  
- Ticket 6.2: Add sectional chunking (split on headings/paragraphs).  
- Ticket 6.3: Prototype semantic chunking (e.g. spaCy sentence clusters).  
- Ticket 6.4: Write unit tests verifying chunk counts and metadata.

### 7. Task Queue & Orchestration  
- Ticket 7.1: Configure Celery (or RQ) with Redis as broker.  
- Ticket 7.2: In `tasks/processing.py`, implement the worker routine that reads Task entries, calls Hugging Face, stores raw output.  
- Ticket 7.3: Add retry logic with exponential backoff on transient errors.  
- Ticket 7.4: Persist task state transitions in the database and update Job status accordingly.

### 8. Hugging Face Integration & Cost Tracking  
- Ticket 8.1: Build `services/huggingface_client.py` wrapper with model listing, inference calls, and unified error handling.  
- Ticket 8.2: Implement `services/cost_tracker.py` to record usage and enforce budget thresholds.  
- Ticket 8.3: Write integration tests mocking HF API to verify retry and cost logic.

### 9. Results Analysis Backend  
- Ticket 9.1: After all runs complete, compute variance, confidence intervals, and inter-model agreement in a background job.  
- Ticket 9.2: Store aggregated metrics in a Results table.  
- Ticket 9.3: Expose export endpoints for CSV/JSON replication packages.

### 10. Admin Interface Skeleton  
- Ticket 10.1: Scaffold a minimal frontend app (Streamlit or React) under `src/api/views/`.  
- Ticket 10.2: Implement Corpus Upload form and job-launch UI.  
- Ticket 10.3: Add Dashboard view showing active jobs and cost meter.  
- Ticket 10.4: Wire API calls from frontend to backend endpoints.

### 11. Logging, Monitoring & Health Checks  
- Ticket 11.1: Integrate structured logging (e.g. JSON logs) for ingestion, tasks, and API requests.  
- Ticket 11.2: Implement `/api/health` checks for Redis, DB, and HF connectivity.  
- Ticket 11.3: Add error-reporting hooks (e.g. Sentry or basic email alerts).

---

*With these tickets and the scaffold in place, Cursor can begin implementing Epic 1 right away. Feedback welcome on adjustments before we start coding!*

#personal/writing/narrativegravity