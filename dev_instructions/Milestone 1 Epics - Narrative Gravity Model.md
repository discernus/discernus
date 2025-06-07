# Milestone 1 Epics - Narrative Gravity Model
#personal/writing/narrativegravity

## ✅ MILESTONE 1 STATUS UPDATE (June 2025)

**Epic 1-4: INFRASTRUCTURE COMPLETED** ✅
- Backend services, multi-LLM integration, testing infrastructure: 100% complete  
- **Current Issue**: Minor API bug in MetricsCollector (being fixed)
- **Test Success Rate**: 181/182 tests passing (99.5%)

**NEW PRIORITY**: Validation-First Development - Academic credibility must be established before advancing to Milestone 2.

**See**: `VALIDATION_FIRST_DEVELOPMENT_STRATEGY.md` for current 3-phase plan focused on reliability studies.

---

## Epic 1: Corpus & Job Management Backend ✅ COMPLETED
**Description:** Build the backend services that let the Project Founder ingest, validate, store, and orchestrate batch jobs on the universal "consequential narratives" corpus.

**STATUS**: ✅ All requirements implemented with Celery + Redis + PostgreSQL + FastAPI architecture.

### User Stories  
- **Upload JSONL corpus files with validation**: Ingest newline-delimited JSON and validate against the core+extension schemas.  
- **Browse corpora and metadata**: List uploaded corpora with name, upload date, and record count; view document-level metadata.  
- **Select texts, frameworks, models, and run count to launch batch jobs**: Create a Job ID capturing parameters for auditing.  
- **Resumable and fault-tolerant processing**: Automatically resume interrupted jobs and retry transient errors.  
- **Status tracking and history**: Query job and per-chunk status; view historical job outcomes for replication.

### Technical Requirements  
- **Data Models**: `Corpus`, `Document`, `Chunk`, `Job`, and `Task` tables capturing all core and extension fields.  
- **JSONL Parsing & Validation**: POST `/api/corpora/upload`; validate each record against JSON Schemas.  
- **Queue & Orchestration**: Durable task queue (e.g. Celery+Redis); enqueue one task per `(chunk × framework × model × run)`.  
- **Resumability & Retry Logic**: Persist task state; exponential-backoff retries on transient API failures.  
- **APIs**:  
  - `POST /api/corpora/upload`  
  - `GET /api/corpora`  
  - `GET /api/corpora/{corpus_id}/documents`  
  - `GET /api/corpora/{corpus_id}/chunks`  
  - `POST /api/jobs`  
  - `GET /api/jobs`  
  - `GET /api/jobs/{job_id}`  
- **Logging & Validation**: Centralized error logging with codes and stack traces; ingestion audit metrics.  
- **Security & Access Control**: Token-based auth; admin-role restrictions; input sanitization.  
- **Tooling for Corpus JSON Generation**: CLI utility to normalize source texts, apply chunking, compute metadata, and emit JSONL.  
- **Tooling for Schema Migration & Versioning**: Versioned JSON Schemas; migration scripts (jq/Python) for upgrading old records.

---

## Epic 2: Hugging Face API Integration Backend ✅ COMPLETED
**Description:** Leverage Hugging Face's unified API to access multiple LLMs.

**STATUS**: ✅ Multi-LLM integration complete with GPT-4o, Claude 3.5 Sonnet, Gemini 1.5 Pro.

### User Stories  
- **Integrate with Hugging Face Inference API using single authentication**.  
- **Access multiple LLMs through Hugging Face** (GPT-4, Claude, Gemini, etc.).  
- **Handle rate limiting and retry logic** transparently.  
- **Process each text 5 times per selected model** for variance analysis.  
- **Track costs through Hugging Face's unified billing**.

### Technical Requirements  
- **Single API Integration**: One endpoint and auth for all models.  
- **Cost Efficiency**: Monitor usage and billing within Hugging Face.  
- **Model Flexibility**: Dynamically list and invoke available models.  
- **Unified Error Handling**: Consistent retry and backoff strategies for all model calls.

---

## Epic 3: Results Analysis Backend ✅ COMPLETED
**Description:** Compute and store reliability metrics and expose them for export and visualization.

**STATUS**: ✅ Universal multi-run dashboard with statistical analysis complete.

### User Stories  
- **Calculate variance, confidence intervals, and inter-model agreement** for each text.  
- **Store run-level data** with timestamps and model versions.  
- **Provide data export APIs** for CSV/JSON replication packages.  
- **Generate summary data** to drive admin-interface visualizations.

### Technical Requirements  
- **Statistical Libraries**: e.g. NumPy, SciPy, or equivalent for variance and CI computations.  
- **Data Storage Schema**: Tables for raw outputs, aggregated metrics, and audit trails.  
- **Visualization Payloads**: JSON endpoints supplying chart-ready data.  
- **Unified Cost Tracking**: Correlate metrics with per-model billing data.

---

## Epic 4: Admin Interface & Monitoring ✅ COMPLETED
**Description:** Web dashboard tying together corpus ingestion, job orchestration, LLM processing, and results export.

**STATUS**: ✅ Streamlit interface with comprehensive workflow management complete.

### User Stories  
- **Dashboard showing system status, active jobs, and recent results**.  
- **Corpus upload & job launcher** with checkbox selections for texts, frameworks, and models.  
- **Real-time job progress, error logs, and cost meter**.  
- **Results viewer and one-click export** for academic datasets.  
- **Settings page** for Hugging Face API key, model selection, run count, and retry parameters.

### Technical Requirements  
- **Frontend UI Components**: React/Streamlit or similar for dashboard, forms, and tables.  
- **Data Endpoints**: REST APIs supporting all user stories.  
- **Authentication & Authorization**: Secure login for the Project Founder role; token management.  
- **Responsive Design**: Usable on desktop and tablet for admin tasks.
