# Discernus Post‑Run Analytics & Visualisation Guidance v0.1
*Date: 2025-06-25*

---

## 1 – Philosophy  

- **Reproducibility floor, exploratory ceiling.** Every run ships with an auto‑generated notebook covering descriptive stats and “canonical” plots; researchers can layer richer analysis later.  
- **Loose coupling.** DES focuses on data generation. Analytics live in companion artifacts.  
- **Declarative when helpful, code when necessary.** Simple aggregations fit a YAML recipe DSL; advanced work sits in notebooks.

---

## 2 – Baseline Auto‑Notebook (always generated)  

| Section | Content |
|---------|---------|
| Metadata | run_id, DES hash, evaluator summary |
| Descriptives | text count, token stats, axis means ± SD |
| Framework Plots | MFT radar, PFT anchor map, etc. |
| Validation Tables | MFQ correlations, F1, p‑values |
| Cost & Latency | tokens, dollars, elapsed time |

---

## 3 – Optional Analysis Recipe (AR)  

```yaml
meta:
  title: Party‑split temporal drift
  based_on_run: run_2025_07_13T10_22Z

pipeline:
  - op: filter
    where: speaker_party in ["Democrat", "Republican"]
  - op: groupby
    by: [speaker_party, year]
    agg: mean
  - op: stats
    test: MannKendall
    field: care_harm
  - op: export_plot
    type: line
    x: year
    y: care_harm
    facet: speaker_party
```

Supported ops (MVP): **filter**, **groupby**, **stats**, **export_plot**.

---

## 4 – Optional Visualisation Recipe (VR)  

Vega‑Lite / Plotly JSON referencing dataset columns.

```json
{
  "title": "Axis mean heatmap",
  "data": "analysis_output.csv",
  "mark": "rect",
  "encoding": {
    "x": {"field": "axis", "type": "ordinal"},
    "y": {"field": "year", "type": "ordinal"},
    "color": {"field": "mean", "type": "quantitative"}
  }
}
```

---

## 5 – Storage & Provenance  

Recipes live in `analysis_recipes/` or `vis_recipes/` directories; SHA‑256 logged in the run lockfile if referenced.

---

## 6 – Fallback “Notebook‑Only” Workflow  

When no recipes are supplied, researchers edit the auto‑notebook directly—maximum flexibility, replication still possible with data + notebook.

---

*Lock the data; recipe the insight; sketch the story.*
