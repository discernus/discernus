# Discernus MVP Technical Requirements Specification v1.1  
*(Merged & Reconciled)*  

---

## 1 – Bottom‑Line‑Up‑Front (BLUF)  
Deliver, within six weeks, a **dual‑framework, single‑provider pipeline** that:  

1. **Scores 100 texts** with two theory frameworks—Moral Foundations Theory (MFT) & Political Framing Theory (PFT).  
2. **Validates** results against gold standards (MFQ correlations ≥ 0.6; PFT F1 ≥ 0.75).  
3. **Persists** every signature plus metadata in Postgres.  
4. **Generates** a self‑contained HTML/PDF report embedding Discernus coordinate visualizations and validation stats.  
5. **Exports** a replication ZIP (corpus + YAML + JSON + report) fit for journal submission.  

Anything **outside** those five bullets is deferred to Phase 2.  

---

## 2 – Scope Summary  

| In‑Scope | Out‑of‑Scope |
|----------|--------------|
| 2 theory frameworks (MFT, PFT) | Additional frameworks or boosters |
| One LLM provider (OpenAI GPT‑4) | Multi‑provider routing |
| Batch size = 100 texts | Cross‑cultural or > 1 k corpora |
| CLI‑driven experiments | Conversational recipe interface |
| Gatekeeper‑validated corpus | Ad‑hoc or unvalidated text ingestion |

---

## 3 – Architecture & Components  

```mermaid
graph TD
  A[Corpus Gatekeeper] -->|Clean texts| B(Celery Queue)
  B --> C[LLM Gateway (OpenAI SDK)]
  C --> D[Signature Engine]
  D --> E[(Postgres)]
  D --> F[Validation Toolkit]
  E --> G[Report Builder]
  F --> G
  G --> H[Replication ZIP]
```

| ID | Component | Purpose | Notes |
|----|-----------|---------|-------|
| **A** | **Corpus Gatekeeper** | Validate schema, deduplicate, store texts | Follows *Corpus Spec v1.0* |
| **B** | **Celery Queue** | Parallel task execution | 8 workers, Redis broker |
| **C** | **LLM Gateway** | Call GPT‑4 with back‑off, cost log | LiteLLM proxy _optional_ |
| **D** | **Signature Engine** | Parse raw LLM JSON ➜ vectors & stats | Pydantic models; NumPy ops |
| **E** | **Persistence Layer** | Store signatures & provenance | `discourse_analyses` JSONB |
| **F** | **Validation Toolkit** | MFQ correlation, frame F1 | Outputs CSV |
| **G** | **Report Builder** | Jinja HTML + Plotly divs ➜ PDF | Uses WeasyPrint for PDF |
| **H** | **Exporter** | Zip corpus + YAML + report | SHA‑256 lockfile inside |

---

## 4 – Functional Requirements  

| Pillar | Must‑Have Capability | Acceptance Test |
|--------|----------------------|-----------------|
| Framework Execution | Parse YAML → prompt → score | 100/100 texts processed for each framework |
| Signature Engine | Produce vectors & stats | 0 parsing errors; columns match framework axes |
| Validation | MFQ *r* ≥ 0.6, PFT F1 ≥ 0.75 | `validation_stats.csv` passes thresholds |
| Persistence | Insert JSONB rows | Row count = 200 |
| Visualization | Radar + anchor plots | `run_id.html` opens & shows both plots |
| Reporting | Create self‑contained HTML/PDF | Report ≤ 5 MB, viewable offline |
| Export | Generate replication ZIP | Zip hash logged; unzip shows all assets |

---

## 5 – Non‑Functional Requirements  

| Attribute | Target |
|-----------|--------|
| Reliability | ≥ 95 % success on CI smoke test |
| Runtime | ≤ 30 min for full batch |
| Cost | ≤ USD 10 per run |
| Transparency | Prompt, model, cost logged per text |
| Reproducibility | Identical inputs → identical DB rows (± 1e‑6) |

---

## 6 – Deliverables & Timeline  

| Week | Deliverable |
|------|-------------|
| 1 | Repo branch scaffold, Gatekeeper prototype, DB migrations |
| 2 | MFT prompt + Signature Engine v0, JSON outputs |
| 3 | PFT prompt, dual‑framework pipeline, DB writes |
| 4 | Report Builder with visualizer integration |
| 5 | Validation toolkit, stats meet thresholds |
| 6 | Replication ZIP, documentation, tag `v0.9.0‑MVP` |

---

## 7 – Dependencies & Interfaces  

* OpenAI Python SDK ≥ 1.3  
* Celery 5 + Redis 7  
* PostgreSQL 15 + SQLModel  
* Plotly 5, WeasyPrint 62  
* JSON Schema validation via *jsonschema* package  
* Corpus Spec v1.0 for input texts  

---

## 8 – Revision Log  

| Version | Date | Editor | Notes |
|---------|------|--------|-------|
| v1.0 | 2025‑06‑24 | ChatGPT | Initial MVP requirements |
| **v1.1** | 2025‑06‑25 | ChatGPT | Added Signature Engine, Report Builder, Corpus Gatekeeper; reconciled scope |

---

*“Insight happens after the numbers.”  This MVP captures numbers you can trust and packages them in stories scholars can read.*  
