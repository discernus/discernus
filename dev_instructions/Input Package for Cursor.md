# Input Package for Cursor

Below is the project scaffold, JSON Schema files, “golden set” test data, and a prioritized ticket list (including testing & monitoring tasks).

---

## 1. Project Scaffold & Folder Structure

narrative-gravity/ ├── README.md ├── requirements.txt ├── setup.py ├── docker-compose.yml ├── Dockerfile │ ├── schemas/ │ ├── core_schema.json │ ├── cv_extension_schema.json │ ├── mrp_extension_schema.json │ └── ps_extension_schema.json │ ├── corpus/ │ └── golden_set/ # 5–10 annotated sample JSONL files │ ├── src/ │ ├── api/ │ │ ├── **init**.py │ │ ├── health.py # /api/health endpoint │ │ └── corpora.py # corpora endpoints │ │ └── jobs.py # job endpoints │ │ │ ├── models/ │ │ ├── corpus.py │ │ ├── document.py │ │ ├── chunk.py │ │ ├── job.py │ │ └── task.py │ │ │ ├── tasks/ │ │ ├── ingestion.py # JSONL ingestion & schema validation │ │ └── processing.py # enqueue & process Hugging Face calls │ │ │ ├── services/ │ │ ├── huggingface_client.py # HF wrapper, retry, cost-tracking │ │ └── cost_tracker.py # record usage & budgets │ │ │ ├── cli/ │ │ └── generate_jsonl.py # CLI to convert raw texts → JSONL │ │ │ └── utils/ │ ├── validation.py # JSON Schema loader & validator │ └── chunker.py # fixed, sectional, semantic chunk logic │ └── tests/ ├── test_health.py ├── test_ingestion.py ├── test_chunking.py ├── test_api_corpora.py └── test_job_lifecycle.py

---

## 2. JSON Schema Files

Place your versioned JSON Schemas in `schemas/`:

- **core_schema.json** – Document‐level + chunk‐level core fields  
- **cv_extension_schema.json** – Civic Virtue framework extensions  
- **mrp_extension_schema.json** – Moral‐Rhetorical Posture framework extensions  
- **ps_extension_schema.json** – Political Spectrum framework extensions  

Ensure each schema has a `"schema_version"` field and clear `required` definitions.

---

## 3. “Golden Set” Test Data

In `corpus/golden_set/`, include 5–10 JSONL files—each a small, fully annotated example covering different genres (speech, op‐ed, ad script). These will drive your end‐to‐end CI tests (ingest → chunk → job → results).

---

## 4. Initial Ticket List

1. **Project Setup & CI**  
   - Initialize repo, virtualenv, core deps (FastAPI, Celery, Redis, HF SDK, JSONSchema).  
   - Add Docker Compose services (API, Redis, worker).  
   - Configure CI (schema checks, unit tests, golden‐set pipeline).

2. **Schemas & Golden Set**  
   - Copy schemas to `schemas/`.  
   - Add golden‐set JSONL in `corpus/golden_set/`.  
   - Write tests to validate these records against core_schema.json.

3. **Health & Monitoring**  
   - Implement `/api/health` verifying DB, Redis, HF connectivity.  
   - Add baseline performance & cost benchmark test on golden‐set.  
   - Configure alert hooks (email or CI failure) on health/checks failures.

4. **Corpus & Job Management API**  
   - `POST /api/corpora/upload` (JSONL ingestion + schema validation).  
   - `GET /api/corpora`, `GET /api/corpora/{id}/documents`, `GET /api/corpora/{id}/chunks`.  
   - `POST /api/jobs`, `GET /api/jobs`, `GET /api/jobs/{job_id}`.

5. **Data Models & Database**  
   - Define PostgreSQL tables (Corpus, Document, Chunk, Job, Task) with JSONB columns for metadata.  
   - Configure Alembic migrations.  
   - Write CRUD unit tests.

6. **Ingestion & Chunking**  
   - CLI: `generate_jsonl.py` for raw→JSONL conversion.  
   - `tasks/ingestion.py` to parse JSONL, validate schema, persist records.  
   - `utils/chunker.py` for fixed, sectional, semantic chunking.  
   - Tests: verify chunk counts, metadata fields.

7. **Task Queue & Orchestration**  
   - Configure Celery + Redis broker.  
   - `tasks/processing.py`: enqueue `(chunk × framework × model × run)` tasks.  
   - Retry logic with exponential backoff; record retries & failures.

8. **Hugging Face Integration & Cost Tracking**  
   - `services/huggingface_client.py`: unified model calls via HF Inference API.  
   - `services/cost_tracker.py`: record usage, enforce $2 500 budget.  
   - Mock HF in tests to verify retry & cost logic.

9. **Results Analysis Backend**  
   - Compute variance, confidence intervals, inter-model agreement after runs.  
   - Store aggregated metrics; expose CSV/JSON export endpoints.  
   - Tests: verify statistical computations on golden‐set.

10. **Admin Interface Skeleton**  
- Scaffold minimal Streamlit/React UI under `src/api/views/`.  
- Corpus upload form, job-launcher, dashboard with cost meter.  
- Wire up to backend endpoints; basic styling.

11. **Testing & Failure‐Mode Definitions**  
- CI tests for schema compliance, chunk counts, job→task linkage.  
- Define and test failure modes (e.g., mark repeatedly failing chunks, skip rest).  
- Performance & cost assertions on small sample to prevent runaway API calls.

---

#personal/writing/narrativegravity