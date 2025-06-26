# DES Roadmap — Five Next‑Obvious Research Axes  
*Date: 2025‑06‑25*

## Opening Framework — Five “Next Obvious” Dimensions  

| Dimension | What It Captures | Why It Matters | Minimal DES Hooks |
|-----------|------------------|----------------|-------------------|
| **Cohort / Stratified Analysis** | Group‑wise contrasts by metadata (party, gender, medium, geography) | Enables moderator tests without re‑uploading corpora | `corpus.strata` & `analysis_mode: stratified` |
| **Cross‑Lingual Translation Layer** | Same framework across languages | Tests cultural generalisability | `execution.translation` block |
| **Prompt / Hyper‑Parameter Sweep** | Systematically vary temperature, prompt style, few‑shot examples | Quantifies robustness | `experiment_matrix.parameter_grid` |
| **Model Ensemble / Benchmark** | Multiple LLMs on identical texts | Inter‑model convergence & cost trade‑offs | `models:` list with per‑model cost caps |
| **Human‑in‑the‑Loop Adjudication** | Manual rating checkpoints | High‑stakes qualitative coding; IRB compliance | `review:` block (stage, sample_rate, role) |

### Implementation Guidance  

* Optional sub‑objects; absence leaves MVP unchanged.  
* Shared cost guardrails via `execution.cost_cap_usd`.  
* Report Builder adds ridge plots, agreement heatmaps, moderator tables.  

---

*Anticipating these axes now prevents painful schema migrations later.*  
