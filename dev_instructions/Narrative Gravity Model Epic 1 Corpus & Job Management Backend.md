# Narrative Gravity Model Epic 1: Corpus & Job Management Backend
#personal/writing/narrativegravity

## ✅ STATUS: COMPLETED (January 2025)
**Epic 1 has been successfully implemented with full backend infrastructure, multi-LLM integration, and golden set corpus.**

**Next Phase**: Validation-First Development - See `VALIDATION_FIRST_DEVELOPMENT_STRATEGY.md` for current priorities.

---

## Overview  
Build the backend services that let the Project Founder ingest, validate, store, and orchestrate batch jobs on the universal "consequential narratives" corpus. All functionality is exposed via APIs that the Admin Interface (Epic 4) will call.

**✅ IMPLEMENTATION STATUS:**
- Backend Infrastructure: Complete (Celery + Redis + PostgreSQL + FastAPI)
- Multi-LLM Integration: Complete (GPT-4o, Claude 3.5 Sonnet, Gemini 1.5 Pro)
- Golden Set Corpus: Complete (17 curated texts)
- Universal Multi-Run Dashboard: Complete with auto-detection
- Framework Support: Complete (Civic Virtue, Political Spectrum, Moral Foundations)

---

## Data Format & Schema

### 1. Universal Core Schema  
Every narrative—speech, op-ed, article, ad script, pamphlet, web page, social media post—must conform to this core document+chunk schema.  

#### Document‐Level Fields (in each JSON record under `document`)  
- `text_id` (string, required): Unique identifier  
- `title` (string, required)  
- `document_type` (string, required): one of `speech`, `op_ed`, `article`, `tv_ad_script`, `pamphlet`, `web_page`, `social_media`, `other`  
- `author` (string, required)  
- `date` (string, required, ISO 8601)  
- `publication` (string, optional)  
- `medium` (string, optional): e.g. `print`, `online`, `TV`, `radio`  
- `campaign_name` (string, optional)  
- `audience_size` (integer, optional)  
- `source_url` (string, optional)  
- `schema_version` (string, required): core schema version  
- `metadata` (object, optional): arbitrary extra fields  

#### Chunk‐Level Fields (each JSON record extends `document` with these)  
- `chunk_id` (integer, required): zero‐based index  
- `total_chunks` (integer, required)  
- `chunk_type` (string, required): `fixed`, `sectional`, or `semantic`  
- `chunk_size` (integer, required): characters in this chunk  
- `chunk_overlap` (integer, optional): chars overlapping previous chunk  
- `document_position` (float, required): 0.0–1.0 normalized start  
- `word_count` (integer, required)  
- `unique_words` (integer, required)  
- `word_density` (float, required): unique_words ÷ word_count  
- `chunk_content` (string, required)  
- `framework_data` (object, optional): extension fields per framework

### 2. Framework‐Specific Extensions  
Frameworks may define additional fields in `framework_data` but do **not** alter core ingestion. Example extension schemas:  
- **Civic Virtue:** definitions of gravity‐well weights  
- **Moral-Rhetorical Posture:** dipole marker lists  
- **Political Spectrum:** ideological lexicon mappings  

### 3. Chunking Specification  
- **Fixed‐size:** e.g. 5 000 chars + 10% overlap  
- **Sectional:** split on headings/paragraphs (Markdown, HTML, LaTeX)  
- **Semantic:** NLP‐driven (spaCy sentence clusters, recursive heuristics)  
Tool must preserve semantic coherence and record chunk metadata.

### 4. Schema Evolution  
- Store JSON Schema files (core + each extension) in repo with version tags  
- Include `schema_version` in records  
- Provide migration scripts (jq/Python) for upgrading old records  
- Maintain a small "golden set" of test records for regression checks

---

## User Stories

1. **JSONL Ingestion**  
   - As the Project Founder, I want to upload a newline-delimited JSON file so the system can ingest multiple document+chunk records at once.  
   - As the Project Founder, I want immediate validation feedback (schema errors, missing fields) so I can correct and re-upload.

2. **Corpus Browsing & Metadata**  
   - As the Project Founder, I want to list all corpora (name, upload date, record count) so I can choose which to process.  
   - As the Project Founder, I want to view document-level metadata for each text so I can confirm my selections.

3. **Job Queuing & Parameters**  
   - As the Project Founder, I want to select corpora or individual `text_id`s, choose frameworks, pick Hugging Face models, and set `run_count` so I can launch batch jobs.  
   - As the Project Founder, I want each job to have a unique Job ID capturing parameters for later auditing.

4. **Resumable & Fault‐Tolerant Processing**  
   - As the Project Founder, I want jobs to resume from the last successful chunk if interrupted so I don't lose progress.  
   - As the Project Founder, I want failed tasks retried automatically up to a configurable limit so transient API errors don't require manual fixes.

5. **Status Tracking & History**  
   - As the Project Founder, I want to query job status (`pending`, `running`, `completed`, `failed`) so I can monitor progress.  
   - As the Project Founder, I want per-chunk status (e.g. "chunk 3 of 5 runs done") to diagnose bottlenecks.  
   - As the Project Founder, I want a history of past jobs with timestamps and outcomes for audit and replication.

---

## Technical Requirements

### A. Data Models & Storage  
- **Corpus**: `id`, `name`, `upload_timestamp`, `record_count`, `uploader_id`  
- **Document**: `id`, `corpus_id`, `text_id`, `title`, `document_type`, `author`, `date`, `publication`, `medium`, `campaign_name`, `audience_size`, `source_url`, `schema_version`, `metadata JSON`  
- **Chunk**: `id`, `document_id`, `chunk_id`, `total_chunks`, `chunk_type`, `chunk_size`, `chunk_overlap`, `document_position`, `word_count`, `unique_words`, `word_density`, `chunk_content`, `framework_data JSON`  
- **Job**: `id`, `corpus_id`, `text_ids[]`, `frameworks[]`, `models[]`, `run_count`, `status`, `created_at`, `updated_at`  
- **Task**: `id`, `job_id`, `chunk_id`, `framework`, `model`, `run_number`, `status`, `attempts`, `last_error`, `started_at`, `finished_at`

### B. JSONL Parsing & Validation  
- Accept ingestion via `POST /api/corpora/upload` (multipart/form-data or direct JSONL)  
- Validate each line against the core JSON Schema; if a framework is selected, also validate against the extension schema  
- Return a structured error report with line numbers and schema violations  

### C. Queue & Orchestration  
- Use a durable task queue (e.g. Celery + Redis/RabbitMQ)  
- On job creation, enqueue one Task per `(chunk_id × framework × model × run_number)`  
- Task workers call the Hugging Face Inference API, store raw responses in a Results table  

### D. Resumability & Retry Logic  
- Persist task state to database on success/failure  
- Automatic retry on transient errors (HTTP 5xx, timeouts) with exponential backoff  
- Configurable max retries per task  

### E. APIs  
- **POST** `/api/corpora/upload` → ingest JSONL corpus  
- **GET**  `/api/corpora` → list corpora  
- **GET**  `/api/corpora/{corpus_id}/documents` → list documents+metadata  
- **GET**  `/api/corpora/{corpus_id}/chunks` → list chunk metadata  
- **POST** `/api/jobs` → launch processing job  
- **GET**  `/api/jobs` → list jobs  
- **GET**  `/api/jobs/{job_id}` → job + task status  

### F. Validation & Logging  
- Centralized logging for ingestion, orchestration, and task execution  
- Structured logs capturing error codes, stack traces, and API error details  
- Summary metrics: total tasks, successes, failures, retries  

### G. Security & Access Control  
- Token‐based authentication for all endpoints  
- Role‐based checks: only the Project Founder (admin role) may upload corpora or start jobs  
- Input sanitization to prevent injection attacks  

### H. Tooling for Corpus JSON Generation

To ensure all narratives conform to the core+extension schema, provide automated tooling that:

- **Generates JSON Schema Skeletons**  
  Use a schema‐generation tool to create draft JSON Schemas from example records, then refine with descriptions and `required` flags for each field[1].  
- **Creates JSON Lines Corpus Files**  
  Implement a command‐line utility (e.g. Python script or Node.js CLI) that:  
  - Reads source transcripts (CSV, Markdown, plain text) and front‐matter metadata  
  - Validates and normalizes fields against the core JSON Schema  
  - Applies the chunking algorithm (fixed, sectional, semantic) and computes chunk‐level metadata  
  - Emits well‐formed JSON Lines files, one chunk record per line, for ingestion  

### I. Tooling for Schema Migration & Versioning

To gracefully evolve schemas and migrate existing corpora:

- **Versioned Schemas Repository**  
  Maintain semantically versioned JSON Schema files in Git using a tool like `jsonschema-tools` to materialize each new version as a static file[4].  
- **Automated Migration Scripts**  
  Provide migration scripts (e.g., `jq`, `fx`, or Python) that transform old records to the latest schema version when a `schema_version` mismatch is detected[2].  
- **Schema Version Check & Upgrade**  
  On ingestion, detect `schema_version`; if outdated, prompt or automatically run the appropriate migration pipeline to upgrade data before validation.  
- **Compatibility Strategies**  
  Follow additive‐only changes for backward compatibility and deprecate fields rather than remove them; document migration paths in a central registry[3].  

### J. Testing & Monitoring Requirements

To ensure validation infrastructure is robust, observable, and ready for rigorous academic use
* **Golden-Set End-to-End Tests**Maintain 5–10 fully annotated JSONL records ("golden set") and include CI tests that ingest → chunk → enqueue → process → export results to verify the entire pipeline works on known data.
* **Automated Validation Tests** [1](https://www.getambassador.io/blog/complete-roadmap-effective-api-testing)In CI, run schema-compliance checks, verify chunk counts match **total_chunks**, and assert job→task linkage integrity (every task corresponds to a chunk × model run).
* **Failure-Mode Definitions** [2](https://docs.mulesoft.com/mule-runtime/latest/batch-error-handling-faq)Define how the system behaves when a chunk errors repeatedly beyond retry limits (e.g., mark as "failed", notify admin, skip remaining runs) and include tests for each scenario.
* **Baseline Performance & Cost Benchmarks** [1](https://www.getambassador.io/blog/complete-roadmap-effective-api-testing)On a small sample corpus, measure end-to-end latency and API call counts to establish performance baselines and cost per run, then assert against budget thresholds in CI.
* **Health Check Endpoint** [4](https://thinhdanggroup.github.io/health-check-api/)Implement and monitor **/api/health** that verifies connectivity to Redis, DB, and Hugging Face; include automated uptime alerts to ensure early detection of service degradation.
