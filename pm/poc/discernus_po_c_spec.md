# Discernus Thin‑Orchestration PoC – Implementation Brief

## 1 · Objective

Stand up a **minimal, reproducible pipeline** that demonstrates the *THIN* architecture:

- **No bespoke parsers** for frameworks or outputs.
- **Artefact‑oriented caching** so finished LLM calls are never repeated.
- **Abort / resume** and **cost‑guard** controls proven in practice.

The PoC targets a 10‑document sample corpus and a single uploaded framework (CAF\_v4.3) running on one LiteLLM model.

---

## 2 · Core Concepts (Glossary)

| Term                  | Plain‑English meaning                                                                        |
| --------------------- | -------------------------------------------------------------------------------------------- |
| **Redis Stream**      | A shared append‑only task list.                                                              |
| **MinIO**             | Local S3‑compatible object store for artefacts.                                              |
| **Artefact**          | Any file (JSON, Parquet, prompt) saved by SHA‑256.                                           |
| **Router**            | 150‑line Python service that moves tasks between Redis streams—nothing else.                 |
| **Agent**             | Stateless container whose entrypoint is *“read task → call LLM with prompt → write result.”* |
| **OrchestratorAgent** | The *only* reasoning component; decides which tasks to queue next.                           |

---

## 3 · PoC Scope & Non‑Goals

### In‑Scope

1. Skeleton Router (Redis Streams).
2. Local MinIO + tiny CLI (`put|get|lookup`).
3. Two agents: **AnalyseChunkAgent** & **OrchestratorAgent**.
4. Artefact hashing + cache check.
5. Pause / resume via Redis `run_status`.
6. Live vs dev mode cost guard (Lua script).

### Out‑of‑Scope (for now)

- ValidationAgent, non‑deterministic averaging, composite synthesis, PostHocMathAgent.
- Multi‑framework support beyond CAF\_v4.3.

### 3.5 · Agent Registry

All agent implementations are externalized and discoverable through a registry pattern:

- **`agents/AnalyseChunkAgent/`** - Document analysis with framework application
- **`agents/OrchestratorAgent/`** - Task planning and dependency management  
- **`agents/SynthesisAgent/`** - Multi-analysis aggregation and report generation
- **`agents/SecuritySentinelAgent/`** - Runtime security monitoring (post-PoC)

Each agent directory contains:
- `main.py` - Agent entrypoint and execution logic
- `prompt.yaml` - External prompt template with framework-agnostic instructions
- `Dockerfile` - Containerized execution environment

### 3.6 · Model Registry

We maintain a **Model Registry** in `models/registry.yaml` (with optional overrides in `models/provider_defaults.yaml`) that drives which LLMs are available and how they're pinned.

**File: `models/provider_defaults.yaml`**
```yaml
vertex_ai:
  forbidden_params:
    - max_tokens
  required_params:
    safety_settings:
      - category: HARM_CATEGORY_HARASSMENT
        threshold: BLOCK_NONE
      - category: HARM_CATEGORY_HATE_SPEECH
        threshold: BLOCK_NONE
      - category: HARM_CATEGORY_SEXUALLY_EXPLICIT
        threshold: BLOCK_NONE
      - category: HARM_CATEGORY_DANGEROUS_CONTENT
        threshold: BLOCK_NONE
  timeout: 180
openai:
  forbidden_params:
    - max_tokens
  requires_pre_moderation: true
  timeout: 120
# etc…

openai/gpt-4o:
  provider: openai
  performance_tier: top-tier
  context_window: 128000
  costs:
    input_per_million_tokens: 2.5
    output_per_million_tokens: 10.0
  utility_tier: 4
  task_suitability:
    - synthesis
    - code_interpreter
  tpm: 300000
  rpm: 5000
  optimal_batch_size: 6
  last_updated: '2025-07-21'
  review_by: '2026-01-17'
anthropic/claude-3-5-sonnet-20240620:
  provider: anthropic
  performance_tier: top-tier
  # …and so on, matching your prior registry format
```

---

## 4 · Architecture Overview

```mermaid
graph TD
  subgraph Router
    R[Redis Streams]
  end
  O[OrchestratorAgent] -->|publish AnalyseChunk| R
  R --> AC[AnalyseChunkAgent]
  AC -->|.done| R
  R -->|events| O
  subgraph Artefact Store
    M[MinIO /artefacts]
  end
  AC -->|PUT JSON| M
  O -->|PUT logs| M
```

---

## 5 · Implementation Phases & Estimates

| #     | Deliverable                      | Timebox (hrs) | Key Tasks                                                                                                                                                     |
| ----- | -------------------------------- | ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **1** | **Skeleton Router**              | 2             | • Set up Redis Streams `tasks` / `tasks.done`.• Consumer group example.                                                                                       |
| **2** | **Artefact Registry CLI**        | 2             | • MinIO docker‑compose.• CLI commands: `put`, `get`, `lookup`.                                                                                                |
| **3** | **Agents & Prompts**             | 4             | • Externalise prompts to `agents/*/prompt.yaml`.• AnalyseChunkAgent splits corpus, calls LiteLLM proxy, emits `{output_uri, sha256, prompt_hash, chunk_id}` to Redis metadata.• OrchestratorAgent hard‑codes simple linear pipeline.• Create `agents/SynthesisAgent/prompt_v1.yaml` + container stub in docker-compose.yml |
| **4** | **Cache & Resume**               | 2             | • SHA‑256 before enqueue.• Redis key `run:{id}:status` (RUNNING/PAUSED).                                                                                      |
| **5** | **Cost Guard** (optional in PoC) | 2             | • Pre‑run cost estimate via LiteLLM `/pricing`.• Lua script aborts run if `spent > cap` in live mode.                                                         |

*Total*: **12 hrs dev time**.

---

## 5.1 · Critical Implementation Notes

**AnalyseChunkAgent Response Schema**: Phase 3 → Phase 4 handoff requires AnalyseChunkAgent to emit structured metadata for cache detection. In `agents/AnalyseChunkAgent/prompt_v1.yaml`:

```yaml
# Response format requirement:
"Respond with JSON: {output_uri, sha256, prompt_hash, chunk_id}."
```

This ensures Phase 4 cache logic can immediately detect existing artifacts without additional Redis queries.

---

## 5.5 · Implementation FAQs (decisions)

| Question from Cursor             | Decision for PoC                                                                                                                                                                   | Rationale                                                                                    |
| -------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| **LiteLLM proxy setup**          | *Integrate with the existing proxy* we already run. No infra spin‑up.                                                                                                              | Keeps PoC surface minimal; in production users will point to their own.                      |
| **Cache‑hit strategy**           | **Dependency‑aware artefact check**: For each *(chunk, framework\_hash)* ensure analysis JSON exists before enqueue.                                                               | Guarantees we skip only what is truly complete; avoids false positives when corpora overlap. |
| **Artefact manifest format**     | **JSON** file (`runs/<run_id>/manifest.json`) containing: `{sha256, uri, parent_sha256, task_type, timestamp, prompt_hash}`. *Optional Markdown* summary auto‑generated from JSON. | JSON is machine‑diffable; Markdown is human‑readable.                                        |
| **File reconstruction / naming** | Preserve **original filename** & MIME in manifest; retrieval still by SHA hash.                                                                                                    | Aids human traceability without weakening immutability guarantees.                           |
| **Next blocker to tackle first** | 1. `SynthesisAgent` ➜ run completion2. PEL reclaim on resume3. Live‑mode cost guard end‑to‑end test4. JSON manifest writer                                                         | Unblocks cache hit demo, then reliability, then safety.                                      |

---

## 6 · Acceptance Criteria

1. **Run Success**: `discernus run experiment.yaml --mode live` completes, producing analysis JSON artefacts and a run log in MinIO.
2. **Pause / Resume**: While RUNNING, `discernus pause <run_id>` pauses; `discernus resume <run_id>` completes without duplicate LLM calls. Verified by filtering proxy logs for AnalyseChunkAgent calls: zero calls on second run.
3. **Cache Hit**: Re‑running the identical experiment makes **zero** LLM calls.
4. **Cost Prompt** (live mode): CLI displays estimated \$ cost and requires `y/N` confirmation.
5. **Dev Mode**: `--mode dev` auto‑confirms and bypasses cost guard.

---

## 7 · Example Commands

```bash
# Start infra
$ docker compose up -d redis minio

# Put sample corpus & framework
$ discernus artefact put data/corpus/sample1.txt
$ discernus artefact put frameworks/CAF_v4.3.md

# Run experiment (live)
$ discernus run experiments/caf_sample.yaml --mode live

# Pause mid‑run
$ discernus pause RUN123
# Resume
$ discernus resume RUN123

# Re‑run (should hit cache)
$ discernus run experiments/caf_sample.yaml --mode live

# After run
$ discernus manifest RUN123 > runs/RUN123/manifest.json
```

---

## 8 · Experiment Export & Directory Structure

After a successful run, a single CLI command recreates the familiar, self-contained experiment folder for archiving and replication:

```bash
$ discernus export <RUN_ID> --out-dir runs/<RUN_ID>
```

This produces:

```
runs/<RUN_ID>/
├─ corpus/               ← all original input files (e.g., *.txt, frameworks/*.md)
├─ analysis/             ← one JSON per chunk named <chunk_id>.<framework_hash>.json
├─ synthesis/            ← <RUN_ID>.json (the merged report)
├─ logs/                 ← router.log, lite_llm_proxy.log, agent logs
└─ manifest.json         ← full provenance chain & metadata
```

- **manifest.json** is both human- and machine-readable, listing each artefact URI, its SHA-256 hash, parent links, task\_type, and timestamp.
- The entire `runs/<RUN_ID>/` folder can be zipped, stored in DVC or Git, and handed off for audit or replication.
- To resume or replay an exported run exactly, users point the CLI at `runs/<RUN_ID>/manifest.json`:
  ```bash
  $ discernus run --from-manifest runs/<RUN_ID>/manifest.json
  ```

---

## 9 · Security Hardening – Guarding the Orchestrator Attack Surface

> **Threat model**: A compromised prompt or malicious framework convinces the **OrchestratorAgent** to enqueue tasks that exfiltrate secrets, invoke shell commands, or leak private data to remote endpoints.

### 9.1 Static policy gate (router‑side, deterministic)

| Check                      | Enforcement                                                                      | Failure action                |
| -------------------------- | -------------------------------------------------------------------------------- | ----------------------------- |
| **Task type allow‑list**   | Router rejects any message whose `type` ∉ {analyse, synth, math, pause, resume} | Drop + log ERR\_INVALID\_TYPE |
| **URI scheme & path**      | Must match regex `^s3://discernus-artifacts/(corpus\|frameworks\|runs)/`        | Drop + log ERR\_BAD\_URI      |
| **Model allow‑list**       | Must be in `models/registry.yaml` (gpt‑4o-mini, llama3‑70b‑instruct, …)         | Drop + log ERR\_BAD\_MODEL    |
| **SHA256 length**          | Exactly 64 hex chars                                                            | Drop                          |
| **Max tasks per run**      | Config param (e.g., 1 000)                                                      | Abort run when exceeded       |

### 9.2 Runtime sentinel agent (cheap LLM watchdog)

- `SecuritySentinelAgent` subscribes to `tasks` and **mirrors** each message through an “adversarial lens”:
  - Quickly inspects for `.env`, PEM blocks, or URLs outside approved domains.
  - Flagged tasks are moved to `tasks.quarantine`; Orchestrator is notified.

### 9.3 Sandboxing & least privilege

| Component             | Execution profile                                                                                | Limits                                                        |
| --------------------- | ------------------------------------------------------------------------------------------------ | ------------------------------------------------------------- |
| **Agent containers**  | Docker with `--network none` (egress blocked) unless task type requires external call (LiteLLM). | Read‑only mount of `/corpus`, temp scratch dir wiped on exit. |
| **OrchestratorAgent** | Same container stack; *no* OS shell allowed.                                                     | Only IPC is Redis.                                            |

### 9.4 Prompt integrity

1. **Hash pinning** – Every prompt file hash is included in the task metadata; Router validates it matches what is in Git.
2. **Immutable system preamble** – Prefix each prompt with a non‑editable UUID line. If payload lacks the preamble → reject.

### 9.5 Secrets scanning before artefact upload

- `registry_cli.py put` runs a regex + entropy scan (<30 LOC) to refuse uploading `.env`, SSH keys, or AWS creds.
- Block any file whose name matches `/.env($|[._-])/` (covers .env, .env.local, .env_dev, .env-prod, etc.)

---

## 10 · Next‑Step Wishlist (post‑PoC)

1. Precision‑aware normaliser & framework `precision` field.
2. `non_deterministic` averaging and `runs_per_chunk`.
3. ValidationAgent for custom schemas.
4. PostHocMathAgent for retro metrics.
5. Composite framework synthesis.
6. **Security package above once PoC stabilises.**

---

*Last updated 2025‑07‑22 by Jeff*