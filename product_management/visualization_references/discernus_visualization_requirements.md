
# Discernus Visualization System Requirements

**Version:** v0.9  
**Author:** Discernus Systems Team  
**Last Updated:** 2025-06-20  
**Scope:** Requirements and design intent for the Discernus visualization subsystem, based on the rhetorical worldview scoring architecture, LLM benchmarking experiments, and end-user narrative diagnostics.

---

## 🎯 Purpose

The Discernus visualization system transforms structured scoring outputs (e.g., dipole scores, function wells, coherence indices) into **interpretable, theory-aligned, and insight-rich graphics** for both researchers and civic users. It bridges human judgment and model inference through rhetorical transparency.

---

## ❓ Key Questions Visualizations Should Answer

### 1. What worldview is being communicated?
- **Visual Type**: Elliptical worldview map or dipole slider
- **Purpose**: Show whether a speaker leans populist, pluralist, tribalist, integrative, etc.

### 2. Which moral/emotional forces dominate the speech?
- **Visual Type**: Gravity well ellipse with poles (e.g., Truth, Dignity, Resentment, Fear)
- **Purpose**: Visualize magnitude and direction of rhetorical emphasis

### 3. Is the speech integrative or disintegrative?
- **Visual Type**: Split bar chart (green for integrative, red for disintegrative)
- **Purpose**: Show positive vs negative moral alignment

### 4. How stable or consistent is the model output?
- **Visual Type**: Error bar plots across runs
- **Purpose**: Track variance; diagnose hallucination or stochastic noise

### 5. How do LLMs compare to human raters?
- **Visual Type**: Heatmaps, scatterplots, correlation matrices
- **Purpose**: Quantify alignment by foundation across sources

### 6. How does worldview shift over time or across speakers?
- **Visual Type**: Trajectory map (linked narrative centers), time series plots
- **Purpose**: Show rhetorical drift or strategic reframing

### 7. Are rhetorical contradictions present?
- **Visual Type**: Contradiction flags, bidirectional barplots
- **Purpose**: Alert users to tension within worldviews

---

## 🧱 Visualization Types and Function

| Type                            | Required? | Description                                                  |
|---------------------------------|-----------|--------------------------------------------------------------|
| Elliptical Gravity Well Map     | ✅         | Shows rhetorical pull toward/away from core civic virtues    |
| Integrative vs Disintegrative Bars | ✅     | Contrasts moral uplift vs tribal/resentful content           |
| Narrative Center Coordinate     | ✅         | Summarizes rhetorical balance and coherence                  |
| Model Variance Chart            | ✅         | Error bars across 5+ model runs                              |
| Multi-Model Overlay Map         | ⚠️         | Compare model outputs on same moral field                    |
| Rater vs Model Heatmap          | ✅         | Scores compared across dimensions and agents                 |
| Temporal Drift Tracker          | ⚠️         | Sequence of narrative centers for same speaker or corpus     |
| Contradiction Index Display     | ✅         | Visual flag + value for worldview inconsistency              |

---

## 📌 Minimum Viable Visualizations (Baseline for Research Use)

| Component                          | Why Required?                                               |
|-----------------------------------|-------------------------------------------------------------|
| Gravity Well Ellipse              | Core worldview diagnostic                                   |
| Integrative/Disintegrative Bar    | Core virtue–vice orientation measure                        |
| Narrative Center Dot              | Rhetorical coherence summary                                |
| Variance/Error Bars               | Model trust + validation signal                             |
| Correlation Plot (Model vs Human) | Critical for LLM validation studies                         |
| Downloadable Summary Card         | Needed for reporting and publication snapshots              |

---

## ✨ Surprisingly Delightful Visualizations

| Component                          | Delight Factor                                              |
|-----------------------------------|-------------------------------------------------------------|
| Multi-Model Sonar Overlay         | Visually intuitive multi-agent comparison                   |
| Narrative Trajectory Animation    | Animates worldview shift across time/speeches               |
| Contradiction Arc Ribbon          | Shows worldview tension overlaid on ellipse                 |
| Ellipse Heat Cloud                | Aggregated moral “weather” for campaigns or timeframes      |
| Interactive Explorer              | Clickable poles, hoverable quotes, time slider              |
| Auto-generated Composite Reports  | Multi-speech dashboards in one frame                        |

---

## 📐 Design Guidelines

- **Coordinate Consistency**: All gravity well ellipses should share fixed pole positions.
- **Color Logic**: Green = Integrative; Red = Disintegrative; Blue = Model scoring; Orange = Center
- **Label Discipline**: Every axis and label should trace directly to framework theory (e.g., MFT, Civic Virtue)
- **Responsiveness**: Visuals must be embeddable in web, printable in PDF
- **Data Provenance**: Tooltip or metadata should trace score to source/model/run

---

## 📤 Output Format Requirements

- **SVG + PNG** for visuals
- **JSON + CSV** for raw scores and metrics
- **Markdown Summary Cards** for publication artifacts
- **HTML Dashboard (optional)** for real-time or longitudinal corpora

---

## 🧪 Integration Tests to Pass

- ✅ All well poles render correctly and in stable coordinates  
- ✅ Scores match input data (cross-verified from CSV to visual)  
- ✅ Hover reveals correct label, score, variance  
- ✅ Contradiction index flags render when > 0.5  
- ✅ Export includes both visuals and metrics bundle

---

## 🧠 Summary

The Discernus visualization system must convert abstract rhetorical theory into **immediate, interpretable, empirically useful diagnostics**. It serves both researchers running validation pipelines and civic users auditing political speech. Its success will rest not on flashy graphics—but on the **clarity, coherence, and trustworthiness** of what it shows about rhetorical worldview structure.

