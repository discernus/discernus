# Discernus Terminology Refactor & Platform‑Extensibility Implementation Plan  
*Version 1.0 — 2025-06-22*

---

## Table of Contents  
1. Objectives  
2. High‑Level Timeline (12 Weeks)  
3. Detailed Task Matrix  
4. Technical Specifications  
5. CI/CD & Quality Gates  
6. Risk Register & Mitigations  
7. Acceptance Criteria  
8. Next Steps

---

## 1 · Objectives  

| ID | Goal | Success Metric |
|----|------|---------------|
| OBJ‑1 | Replace all legacy gravity terminology with new cartographic vocabulary. | `grep -R "(well|dipole|gravity)" src/` returns **0** hits (except in deprecated alias file). |
| OBJ‑2 | Decouple visualization from core API (data‑only payloads). | Any chart can be removed without breaking `/coordinates` responses. |
| OBJ‑3 | Ship extensible visualization adapters (Radar, UMAP, Parallel Coordinates). | New adapter registers via plugin interface & renders within 200 ms for 10 k docs. |
| OBJ‑4 | Maintain backward compatibility for three months. | Legacy endpoints return HTTP 299 Deprecation headers but still function. |

---

## 2 · High‑Level Timeline (12 Weeks)  

| Phase | Weeks | Milestone |
|-------|-------|-----------|
| 1 · Code Terminology Refactor | 1–3 | Unit tests pass with new classes (`Anchor`, `Axis`, …) |
| 2 · API & Schema Update | 4–6 | `/v2` API live with data‑only payloads |
| 3 · Visualization Adapter Layer | 4–8 (overlap) | Adapter SDK + Radar/UMAP/Parallel prototypes |
| 4 · Plugin & Export System | 7–10 | CSV/Arrow export + Plugin registry |
| 5 · Docs & Deprecation Window | 9–11 | Developer guide, migration FAQ, changelog |
| 6 · UAT & Launch | 12 | Academic beta testers sign off |

---

## 3 · Detailed Task Matrix  

| # | Task | Owner | Dependencies | DoD |
|---|------|-------|--------------|-----|
| 1 | **Rename Classes & Variables** (`Well` → `Anchor`, `Dipole` → `Axis`) | Core Dev | None | All tests green |
| 2 | Add *deprecated.py* with alias classes emitting warnings | Core Dev | 1 | Import works; warning logged |
| 3 | Update YAML keys (`well_id` → `anchor_id`) via migration script | Data Eng | 1 | Script idempotent |
| 4 | Introduce **terminology‑lint** pre‑commit hook | DevOps | 1 | Blocks forbidden strings |
| 5 | Split API: `/frameworks`, `/coordinates` | API Lead | 1 | Swagger updated |
| 6 | Add HTTP 299 headers to legacy endpoints | API Lead | 5 | Manual cURL verified |
| 7 | Draft Adapter interface `render(data, config) -> HTML` | Frontend | 5 | Radar adapter passes tests |
| 8 | Implement **UMAP** server‑side cache | ML Eng | 5 | 10 k docs < 1 s |
| 9 | Build **Parallel Coordinates** adapter in React | Frontend | 7 | Renders dataset sample |
|10 | Create **plugin registry** (YAML manifest + dynamic import) | Frontend | 7 | Loads sample plugin |
|11 | Export endpoints: `/export/csv`, `/export/arrow` | API Lead | 5 | File downloads succeed |
|12 | Update docs site & examples | Tech Writer | 1,5,7 | PR merged |
|13 | Run UAT with grad students (n=5) | PM | 7,9,11 | Feedback logged |
|14 | Final polish & 1.0 tag | PM | All | Git tag, release notes |

---

## 4 · Technical Specifications  

### 4.1 Data Schema v2  
```jsonc
// signature.json
{
  "doc_id": "...",
  "framework_id": "civic_virtue_v2",
  "signature_type": "axis",          // or "anchor"
  "vector": [{"anchor_id": "care", "value": 0.78}, ...],
  "centroid": false
}
```
- **Centroids** flagged via `centroid: true` with identical vector field.  
- Use **parquet** for internal storage; JSON for API.

### 4.2 Adapter SDK (TypeScript)  
```ts
export interface DiscernusAdapter {
  id: string;
  label: string;
  render: (data: SignatureSet, config: AdapterConfig) => Promise<HTMLElement>;
}
```
Adapters injected via dynamic `import()` from a `plugins/` folder defined in `discernus.config.js`.

### 4.3 Pre‑Commit Terminology Lint  
```bash
forbidden='well|dipole|gravity'
git diff --cached -G"$forbidden" --name-only |   xargs grep -nE "$forbidden" && exit 1
```

---

## 5 · CI/CD & Quality Gates  

| Gate | Tool | Threshold |
|------|------|-----------|
| Unit coverage | pytest‑cov | ≥ 90 % |
| Performance | Locust | 95th %ile API < 300 ms |
| ESLint/Black | Lint stage | 0 errors |
| Terminology Lint | Custom | 0 hits |
| Vulnerability Scan | Snyk | No high severity |

---

## 6 · Risk Register  

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Legacy scripts break on rename | Med | High | Deprecation aliases + release notes |
| Visualization perf for 100 k docs | Med | Med | Server‑side aggregation + WebGL adapter |
| Plugin security | Low | High | Sandbox iframe + allowlist |
| Scope creep | Med | Med | Freeze spec after Week 4 |

---

## 7 · Acceptance Criteria  
1. Running `discernus migrate --check` returns **0** deprecated keys.  
2. `/coordinates` returns identical numeric results for v1 and v2 endpoints.  
3. Docs site search for “well” or “dipole” shows only historical references.  
4. External plugin renders without modifying core code.  
5. Beta testers complete scripted tasks in < 15 min, SUS ≥ 80.

---

## 8 · Next Steps (Week 0)  
- **Kick‑off meeting** — walk through this plan, assign owners.  
- **Branch protection** — require terminology‑lint status check.  
- **Create GitHub Projects board** with tasks #1‑14.  
- **Schedule weekly review**; adjust scope only via Change Control Form.

---

*Prepared June 22, 2025.*  
