# Discernus MVP – Environment & Bill of Materials v1.0  
*(External Dependencies & Modules to Build)*  

---

## 1 – Target Runtime Environment  

| Layer | Requirement | Version | Notes |
|-------|-------------|---------|-------|
| **OS** | Ubuntu LTS | 22.04 | Any Debian‑compatible distro fine |
| **Python** | CPython | 3.11.* | Use `pyenv` / `asdf` for portability |
| **PostgreSQL** | Server | 15 | JSONB performance improvements |
| **Redis** | In‑memory broker | 7.* | Celery default backend |
| **Node.js** (optional) | Node | 20 | For packaging static Plotly assets |
| **Docker** | Engine | ≥ 24 | Compose spec 3.9 |
| **Git** | SCM | ≥ 2.34 | For worktrees & sparse‑checkout |

Hardware: 4 vCPU, 8 GB RAM handles the 100‑text MVP comfortably.

---

## 2 – Python Package Requirements (lockfile will pin exact builds)  

```text
# Core
openai~=1.24.0
sqlmodel~=0.0.16
psycopg2-binary~=2.9
celery~=5.4
redis~=5.0
pydantic~=2.6
numpy~=1.26
pandas~=2.2
plotly~=5.22
jinja2~=3.1
weasyprint~=62.0

# Validation & schema
jsonschema~=4.21
fastlangid~=1.0  # language guess for Gatekeeper

# Dev / Testing
pytest~=8.2
pytest-asyncio~=0.23
black~=24.4
ruff~=0.4
mypy~=1.10
pre-commit~=3.7
```

All versions will be frozen in `requirements.lock` via `pip-compile` before release.

---

## 3 – System Packages  

```bash
sudo apt update && sudo apt install -y    build-essential libpq-dev libffi-dev libpango-1.0-0    libjpeg-dev libpng-dev libfreetype6-dev libharfbuzz-dev    graphviz
```

(WeasyPrint and Graphviz need their C libraries.)

---

## 4 – Docker Compose Skeleton  

```yaml
version: "3.9"
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: postgres
    volumes: [db_data:/var/lib/postgresql/data]
  redis:
    image: redis:7
  worker:
    build: .
    command: celery -A discernus_worker worker -Q experiments -c 8 --loglevel=info
    env_file: .env
    depends_on: [db, redis]
  api:
    build: .
    command: uvicorn discernus.api:app --host 0.0.0.0 --port 8000
    env_file: .env
    depends_on: [db, redis]
volumes:
  db_data:
```

---

## 5 – Environment Variables  

| Name | Purpose | Example |
|------|---------|---------|
| `OPENAI_API_KEY` | Auth for GPT‑4 | `sk-…` |
| `DATABASE_URL` | SQLModel engine | `postgresql+psycopg2://postgres:postgres@db:5432/postgres` |
| `REDIS_URL` | Celery broker | `redis://redis:6379/0` |
| `DISCERNS_FRAMEWORK_DIR` | Path to YAML frameworks | `/app/frameworks` |
| `REPORT_OUTPUT_DIR` | Where HTML/PDF reports go | `/app/output` |
| `PYTHONUTF8` | Ensure UTF‑8 | `1` |

---

## 6 – Bill of Materials — Modules to Implement  

| # | Module (Python package path) | Responsibility | Est. LOC |
|---|------------------------------|----------------|----------|
| **1** | `discernus.gatekeeper` | Corpus validation, deduplication, insertion | 250 |
| **2** | `discernus.tasks.evaluate_text` | Celery task wrapper for single text + framework | 150 |
| **3** | `discernus.llm.gateway` | Thin wrapper around OpenAI SDK with retry & logging | 120 |
| **4** | `discernus.signature` | Pydantic models + vectorisation utilities | 180 |
| **5** | `discernus.validation` | MFQ correlation, PFT precision/recall | 160 |
| **6** | `discernus.reporting.builder` | Jinja templates, Plotly embed, WeasyPrint PDF | 220 |
| **7** | `discernus.exporter` | Replication ZIP + lockfile generator | 90 |
| **8** | `discernus.cli.run_experiment` | Parse YAML, enqueue Celery batch, watcher loop | 140 |
| **9** | `discernus.db.models` | SQLModel tables & migrations (Alembic) | 110 |
| **10** | `discernus.tests.*` | Pytest suite & fixtures | 300 |

_Total new code ≈ 1 720 lines (+ tests) – well within a six‑week sprint for a small team._

---

## 7 – External Services & Access  

| Service | Usage | Notes |
|---------|-------|-------|
| **OpenAI Chat Completions** | GPT‑4o scoring calls | Apply for research grant credits to cover runs |
| **GitHub Actions** | CI pipeline (pytest + lint) | 2 000 runner‑minutes per month |
| **Docker Hub / GHCR** | Container registry | Push automated images from CI |

---

## 8 – Suggested Pre‑Commit Hooks  

1. **Black** – code style  
2. **Ruff** – lint + import sort  
3. **Mypy** – type checking  
4. **pytest** – fast unit tests  
5. **detect‑secrets** – ensure API keys never committed  

---

## 9 – Risk & Mitigation  

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| OpenAI rate‑limits | Medium | Medium | Batch size = 5, exponential back‑off, cached retries |
| WeasyPrint font errors | Low | Low | Include `fonts/` folder in Docker image |
| Redis persistence loss | Low | Low | Results safely in Postgres after task success |
| Version drift in packages | Medium | Medium | `pip‑compile` lockfile + Dependabot alerts |

---

## 10 – Next Steps  

1. **Approve the dependency list** ➜ freeze `requirements.lock`.  
2. **Set up GitHub Secrets** (`OPENAI_API_KEY`, `DATABASE_URL`).  
3. **Bootstrap Docker Compose** ➜ run `pytest -m smoke`.  
4. **Kick off week‑1 sprint** (Gatekeeper, DB migrations).

---

*Once the scaffolding stands, writing Discernus code is an exercise in connecting typed bricks—not mixing mortar.*  
