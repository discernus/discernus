
# Discernus Architectural Review Charter Prompt

**Bottom-Line‑Up‑Front:**  
Feed Claude‑4‑Sonnet a *charter‑style* prompt that spells out **why** you’re doing the review, **what** success looks like, **where** the code lives, and **how** you want the findings structured.

---

## Opening Framework – Prompt Anatomy

| Section | Purpose |
|---------|---------|
| **Role & Perspective** | Tell Claude to think like a principal software architect coaching a product‑oriented PM. |
| **Mission Objectives** | Enumerate the architectural qualities you care about: modularity, extensibility, reproducibility, testability, DX. |
| **Context Payload** | Brief project description, repo path(s), any prior design docs. |
| **Guiding Questions** | Seed Claude with the angles you most need insight on (plugin seams, config strategy, data lineage, etc.). |
| **Deliverables & Format** | Bullet issues → severity/impact, quick‑wins vs long‑horizon, diagram suggestions, and a concise executive summary. |
| **Tone & Interaction Rules** | “Explain like I’m developer‑adjacent, challenge assumptions, ask clarifying questions first.” |

---

## Copy‑Ready Prompt

```text
You are a principal software architect brought in to perform a *first-pass architectural review* of the Discernus codebase.

Project snapshot
----------------
• **Mission**: Discernus is an open-source “operating system for reproducible discourse science.”  
  –  Hosts multiple analytical frameworks (e.g., civic-virtue scoring, narrative gravity)  
  –  Orchestrates human + AI evaluators, ensures transparent provenance, supports plugin expansion  
• **Tech stack**: Python ≥3.10, mixed NLP / LLM pipelines, PostgreSQL, Redis, FastAPI.  
• **Repo root**: `/workspace/discernus` (Cursor has indexed it; feel free to grep).  
• **High-level directory map** (subject to change):  
  ```
  discernus/
      core/          # business logic + workflow engine
      ingest/        # corpus parsers & validators
      models/        # ML & LLM wrappers
      plugins/       # optional extensions (planned)
      interface/     # CLI + REST gateway
      config/        # Hydra/Pydantic configs
      tests/
  ```

Review charter
--------------
1. **Modularity & Separation of Concerns**  
   –  Are layers (ingest → core → interface) cleanly isolated?  
   –  Where is coupling or cross-import bleed-through?  

2. **Extensibility / Plugin Architecture**  
   –  Evaluate current `plugins/` scaffold and propose hook points (entry_points, pluggy, etc.).  
   –  Recommend patterns for external researchers to add frameworks without touching core.  

3. **Reproducibility & Config Management**  
   –  How to guarantee deterministic runs (configs, dataset hashes, model versioning)?  
   –  Assess viability of Hydra + Pydantic vs alternatives.  

4. **Testing, Typing, and CI/CD**  
   –  Coverage gaps, type-safety, mutation risks, fixture strategy.  
   –  Pre-commit + GitHub Actions hygiene.  

5. **Data Lineage & Provenance**  
   –  Traceability of corpus → annotation → score → report.  
   –  Storage design (DB vs object store vs DVC).  

6. **Risk & Debt Hotspots**  
   –  Identify proto-antipatterns (global state, God objects, silent mutations).  
   –  Rank by severity: *critical, high, moderate, informational*.  

Output requirements
-------------------
• Begin with a **one-page executive summary** in plain language a PM can brief to leadership.  
• Follow with **detailed findings**: each issue ⇒ impact, evidence path/file, and recommended fix.  
• **Quick-wins list** (≤2 weeks effort) vs **Long-horizon refactors**.  
• Inline code snippets or directory diffs as needed (≤20 lines each).  
• Close with a **revised high-level diagram** (ASCII OK) showing desired layering & dataflow.

Interaction guidelines
----------------------
• Ask any clarifying questions **before** diving into analysis if critical info is missing.  
• Cite specific files/lines when flagging issues so devs can jump straight in.  
• Use bullet points; avoid fluff. Think “architect’s field report.”  
```

---

## How to Use It

1. **Open a fresh chat** with *claude‑4‑sonnet* (MAX mode **ON**).  
2. Paste the entire block above.  
3. Provide answers to any clarifying questions Claude asks, or simply say “Proceed.”  
4. Iterate as needed until the architectural audit meets your needs.

---

**Takeaway:** A well‑scoped charter prompt turns Claude into an extension of your product‑architect brain—surfacing hidden coupling, proposing plug‑in seams, and packaging the review in PM‑friendly language.
