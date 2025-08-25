# Integrated Provenance, Validation, and Logging Specification

Status: Draft for Review

Purpose: Unify provenance practices (per PROVENANCE_SYSTEM.md), dual-track logging (per DUAL_TRACK_LOGGING_ARCHITECTURE.md), and hash/validation patterns into a thin, practical specification suitable for the current system. This document also proposes acceptance-criteria updates for related backlog items.

---

## Principles

- Content-addressed integrity remains canonical: all artifacts are stored and referenced by SHA-256 (prefix for filenames; full hash in manifests/logs).
- Do not embed validation hashes inside artifacts. Instead, record integrity and minimal validation signals in a run-scoped manifest and provenance logs.
- Favor thin “shape signatures” and invariant checks over deep parsing. Fail fast when preconditions are not met.
- Maintain dual-track logging with minimal, consistent JSONL schemas and stage-boundary events.

---

## Canonical hashing and canonicalization

- Use SHA-256 over canonical JSON bytes for integrity/shape-signature calculations:
  - Serialization: `json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)`
  - Encoding: UTF-8 bytes
  - Hash: `hashlib.sha256(bytes).hexdigest()`
- Never use Python `hash()` for persistence (non-deterministic across processes).

---

## Run Manifest (thin, provenance-oriented)

Each successful run writes a `manifest.json` in the run directory and emits corresponding events to `artifacts.jsonl` and `orchestrator.jsonl`.

Minimum fields (illustrative):

```json
{
  "run_id": "20250804T175152Z",
  "git_commit": "<hash-or-null>",
  "artifacts": [
    {
      "hash": "ecbe79b4",                
      "sha256": "ecbe79b482...full",
      "type": "statistical_results",     
      "size_bytes": 87213,
      "created_at": "2025-01-23T12:34:56Z",
      "dependencies": ["analysis_results_185f5e58", "framework_sha:..."],
      "shape_signature": "sha256:..."
    }
  ],
  "rag_indexes": [
    {
      "name": "fact_checker",
      "config": {"content": true, "model": "txtai/default"},
      "doc_count": 123,
      "evidence_input_hashes": ["35008a8b", "..."],
      "index_build_fingerprint": "sha256:...",
      "created_at": "2025-01-23T12:40:12Z"
    }
  ]
}
```

Notes:
- `shape_signature` is optional and applies to numerical outputs (see below).
- `index_build_fingerprint` is SHA-256 over canonicalized sorted `evidence_input_hashes` plus key config flags (e.g., `{"content": true}`) to serve caching/invalidation.

---

## Shape signatures and invariants (numerical outputs)

Applies to both statistical results and derived metrics.

- Shape signature: SHA-256 of a minimal, canonical summary of the result’s “presence and form,” for example:
  - Sorted top-level keys
  - Required sections present (e.g., correlations, descriptives)
  - Non-empty counts per section
  - Sentinel numeric invariants (e.g., correlations in [-1,1], no NaN/Inf)
- The shape signature is stored in the run manifest for the corresponding artifact and logged in `artifacts.jsonl`.
- Acceptance: Succeeds when invariants hold and signature exists; otherwise fail fast.

Benefits:
- Detects “metadata-only” outputs without deep, brittle parsing.
- Consistent across stats and derived metrics; thin to compute and verify.

---

## RAG index manifest (directory-native)

For every index produced (fact-checker, synthesis), write a minimal manifest and emit an artifacts log record:

Fields:
- `name` (e.g., `fact_checker`, `synthesis_evidence`)
- `config` (must include `{"content": true}`)
- `doc_count` (> 0)
- `evidence_input_hashes` (sorted, unique)
- `index_build_fingerprint` = SHA-256 over canonical JSON of `{ "evidence_input_hashes": [...], "config": {"content": true, ...} }`
- `created_at`

Health checks before use:
- `doc_count > 0`
- sample retrieval returns content (at least 1 success)
- on failure: fail fast and log structured error events

---

## Dual-track logging: minimum JSONL schemas

Emit at stage boundaries and on every artifact write. Keep schemas stable and minimal.

- `orchestrator.jsonl` events (examples):
  - `{"event":"stage_start","stage":"analysis","timestamp":"...","metadata":{...}}`
  - `{"event":"stage_complete","stage":"analysis","timestamp":"...","results":{...}}`
  - `{"event":"pre_synthesis_check_failed","reason":"no_evidence","timestamp":"..."}`

- `agents.jsonl` events (examples):
  - `{"agent":"EnhancedAnalysisAgent","event":"llm_call","input":{"...": "..."},"output_meta":{"tokens":123},"timestamp":"..."}`

- `artifacts.jsonl` events (examples):
  - `{"event":"artifact_created","type":"statistical_results","sha256":"...","shape_signature":"sha256:...","timestamp":"..."}`
  - `{"event":"rag_index_built","name":"fact_checker","fingerprint":"sha256:...","doc_count":123,"timestamp":"..."}`

- `system.jsonl` events (examples):
  - `{"event":"security_boundary_enforced","agent":"...","path":"...","timestamp":"..."}`

Git auto-commit:
- Record `git_commit` (hash or null) in the run manifest and emit a `system.jsonl` event with status.

---

## Pre-synthesis preflight (fail-fast)

Before synthesis begins, verify and log:

1. Statistical results
   - present, non-empty; invariants pass; shape signature recorded
2. Derived metrics
   - present if required; non-empty; invariants pass; shape signature recorded
3. Evidence availability
   - `evidence_count > 0` OR explicit “no-evidence” path with logged rationale
4. RAG index
   - manifest exists, `doc_count > 0`, sample retrieval returns content
5. Framework & corpus
   - SHA-256 recorded in manifest; files exist and parse; minimal structure checks

On any failure: emit `pre_synthesis_check_failed` and terminate the run with a clear error.

---

## Documentation alignment and hygiene

- PROVENANCE_SYSTEM.md refers to `scripts/validate_run_integrity.py`. If the actual path is `scripts/auditing/validate_run_integrity.py`, either add a wrapper at the documented path or update references consistently.
- Ensure all four JSONL streams are actually emitted with the minimal fields above. Stage-boundary events are mandatory.

---

## Backlog acceptance criteria updates (proposed)

1) Fix derived metrics and statistical analysis validation gap (hash-based validation)

- Replace embedded `validation_hash` concept with:
  - `shape_signature` (SHA-256 over canonical minimal summary) recorded in run manifest
  - invariant checks (no NaN/Inf; correlations within [-1,1]; expected sections non-empty)
  - fail-fast on missing/invalid results
- Use `hashlib.sha256(canonical_json)` only (no Python `hash()`).
- Emit `artifact_created` with `shape_signature` to `artifacts.jsonl`.

2) [CACHE-002] Reimplement RAG index caching for new architecture

- Require a per-index manifest with `config`, `doc_count`, `evidence_input_hashes`, and `index_build_fingerprint`.
- Cache keys derive from `index_build_fingerprint`.
- Invalidate cache when `evidence_input_hashes` or `config` change.
- Health checks (doc_count > 0, sample retrieval returns content) are mandatory; fail-fast on failure.

3) [CLI-007] Implement CLI Logging & Provenance

- Ensure dual-track JSONL emission with minimal schemas at stage boundaries.
- Write `manifest.json` with artifact entries (hash, type, size, deps) and optional `shape_signature` for numerical outputs.
- Record Git auto-commit outcome in manifest and `system.jsonl`.

4) [PROVENANCE-001] Phase 1: Foundation – Basic academic provenance

- Implement run manifest and thin symlink organization as already documented.
- Provide `scripts/validate_run_integrity.py` (or a compatible wrapper) that validates:
  - manifest structure
  - artifact hashes vs filenames (prefix vs full SHA-256)
  - symlink integrity
  - provenance chain consistency (deps present)
  - optional Git history check

---

## Testing strategy (thin)

- Unit tests
  - shape signature generation for typical stats/derived metrics objects
  - RAG index `index_build_fingerprint` stability (order-insensitive inputs)
  - pre-synthesis preflight invariants (positive/negative cases)

- Integration tests
  - run through analysis → stats/derived → RAG build → preflight → synthesis
  - assert JSONL events present; manifest populated; fail-fast behavior on injected faults

---

## Definition of Done

- Run manifest is written with artifact entries, optional `shape_signature` for numerical outputs, and RAG index manifests.
- Dual-track logs emit the minimum events and fields at stage boundaries.
- Pre-synthesis preflight enforces the checks above and fails fast on violations.
- Cache keys for RAG indexes use `index_build_fingerprint` and invalidate correctly.
- Validation script verifies hashes, symlinks, and manifest consistency.

---

## Out of scope (for now)

- Merkle trees for RAG directories
- Heavy per-document hashing inside hot paths (we rely on content-addressed storage at write time)
- Blockchain anchoring


