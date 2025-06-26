# DES Extension — Temporal & Comparative Analysis  
*Date: 2025‑06‑25*

## BLUF  
Fold **temporal** and **comparative** analysis into the unified Discernus Experiment Specification by adding three optional sub‑objects—`temporal`, `comparative`, and `longitudinal`—plus flags in `corpus`, `execution`, and `validation`. These fields let researchers describe time‑sliced corpora, before/after contrasts, author trajectories, and text‑to‑text difference reports without breaking backward compatibility.

---

## Why DES Needs Native Temporal & Comparative Hooks  

1. **Temporal Category Analysis** – track framework scores across time windows.  
2. **Individual Author Evolution** – longitudinal stylometry within a speaker’s corpus.  
3. **Systematic Text Comparison** – generate difference reports between two arbitrary texts.  

Storing these relations explicitly removes guess‑work for the orchestrator, simplifies conversational prompting, and provides a replicable trail for reviewers.

---

## Proposed Additions  

| Section | New Fields | Purpose |
|---------|------------|---------|
| `corpus` | `temporal_partition` with `granularity` & `bins` | Bucket texts by time. |
| `execution` | `analysis_mode: single | temporal | comparative | longitudinal` | Clarifies engine behaviour. |
| `temporal` | `reference_period`, `smoothing`, `significance_tests` | Time‑series knobs. |
| `comparative` | `pairings`, `difference_metric`, `report` | Text‑to‑text differencing. |
| `longitudinal` | `author_field`, `trajectory_metric`, `flag_anomalies` | Track speaker evolution. |
| `validation` | `temporal_stability_threshold`, `difference_effect_size` | Mirrors MFQ thresholds. |
| `output` | Allow `difference_report`, `temporal_plot` formats | Report Builder extras. |

---

## Example Snippet  

```yaml
analysis_mode: temporal
corpus:
  slug: inaugural_addresses_1789-2021@v2
  temporal_partition:
    granularity: year
    bins:
      - {label: pre_1945, start: "1789-03-04", end: "1945-01-19"}
      - {label: post_1945, start: "1945-01-20", end: "2021-01-20"}

temporal:
  reference_period: "1789-03-04/1899-12-31"
  smoothing: rolling_mean
  significance_tests: [Mann-Kendall]

validation:
  temporal_stability_threshold: 0.15
```

---

*Time and comparison become first‑class citizens without shattering the unified spec.*  
