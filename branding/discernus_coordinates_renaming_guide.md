
# Discernus Rebranding Guide – Coordinates-Based Language

**Version:** v1.0  
**Purpose:** Replace metaphor-heavy language (e.g., “wells”, “gravity”, “pull”) with precise, cross-domain terminology centered on “Discernus Coordinates.”

---

## 🔁 Core Concept: What’s Changing?

| Old Language             | New Language                     | Rationale                                         |
|--------------------------|----------------------------------|--------------------------------------------------|
| Gravity Well             | Discernus Coordinate Plane        | Domain-neutral; supports geometric reasoning     |
| Well (e.g. “Fear well”)  | Axis Coordinate (e.g. “Fear axis”) | Technical, scalable, not metaphor-dependent      |
| Narrative Center         | Discernus Center                  | Suggests vector average, cross-framework aligned |
| Pull / Draw              | Coordinate Magnitude              | Abstracts emotional bias as scalar intensity     |
| Axis Polarity            | Coordinate Polarity               | Implies formal system of signed direction        |
| Rhetorical Field         | Discernus Map                     | Branded + general-purpose                        |
| Positive / Negative Wells| Integrative / Disintegrative Coordinates | Keeps theory-mapped terminology                  |

---

## 🧱 Structural Changes to Implement

### 1. YAML Framework Definitions
- Replace: `well_name`, `gravity`, `pull`, etc.  
- With: `coordinate_name`, `coordinate_score`, `discernus_center`

**Before:**
```yaml
wells:
  - name: tribalism
    polarity: negative
    magnitude: 0.8
```

**After:**
```yaml
coordinates:
  - name: tribalism
    polarity: disintegrative
    score: 0.8
```

---

### 2. Scoring Output Schema
Use the following format in JSON or CSV outputs:

```json
"discernus_coordinates": {
  "care": 0.62,
  "loyalty": -0.45,
  "authority": 0.20
},
"discernus_center": {
  "x": -0.13,
  "y": 0.74
},
"coherence_index": 0.91,
"contradiction_index": 0.27
```

---

### 3. Visualizations

| Old Label                | New Label                        |
|--------------------------|----------------------------------|
| “Gravity Map”            | “Discernus Coordinate Map”       |
| “Narrative Pull”         | “Coordinate Distribution”        |
| “Moral Well Heatmap”     | “Coordinate Intensity Heatmap”   |
| “Contradiction Arc”      | “Coordinate Conflict Ribbon”     |
| “Model Overlay Wells”    | “Multi-Agent Coordinate Plot”    |

---

### 4. Prompt Language

**Old:**  
“Evaluate which rhetorical wells the text is drawn toward.”  
**New:**  
“Score the text across Discernus Coordinate dimensions, identifying which axis coordinates have the greatest magnitude.”

---

### 5. Dashboard Components

| Component                | Rename To                         |
|--------------------------|-----------------------------------|
| “Narrative Gravity”      | “Discernus Center”                |
| “Moral Pulls”            | “High-Scoring Coordinates”        |
| “Rhetorical Strength”    | “Coordinate Intensity”            |
| “Pull Strength Map”      | “Coordinate Field”                |
| “Emotional Signature”    | “Discernus Coordinate Signature”  |

---

## ✅ Summary

This renaming system ensures:
- Consistency across front-end, backend, and exports
- Domain neutrality and cross-disciplinary applicability
- Support for formal modeling and scalable analytics

All public and internal assets should begin migrating to the **Discernus Coordinates** language standard as of version `v2.1`.

---

*Generated based on current Discernus framework specs, visualization designs, and reviewer feedback targeting metaphor minimization and theory-generalized clarity.*


---

## 🧩 Coordinate System Specification (Addendum)

### 📌 What Are Discernus Coordinates?

**Discernus Coordinates** refer to a structured set of scalar scores—each corresponding to an axis in a theory-aligned interpretive space (e.g., moral foundations, rhetorical frames, civic values). These coordinates represent the rhetorical orientation of a document, utterance, or agent along each dimension.

### 📐 Types of Coordinate Planes

Each framework in Discernus defines a unique coordinate space:
- **Moral Foundations Theory (MFT)** → 5D: Care, Fairness, Loyalty, Authority, Sanctity  
- **Entman Framing Functions** → 4D: Problem, Cause, Moral Evaluation, Remedy  
- **Lakoff Family Models** → Multi-dipole cluster  
- **Populism vs. Pluralism** → 1D axis

Coordinate values range from –1.0 to +1.0 unless otherwise specified.

### 🧱 Coordinate Score Structures

- **Atomic Coordinates**: Individual axis scores (e.g., `"loyalty": 0.72`)
- **Coordinate Clusters**: Groupings (e.g., “disintegrative composite” = sum of Tribalism, Fear, Resentment)
- **Discernus Center**: Vector average of coordinate scores, projected on visual map

### 📊 Agreement + Stability Metrics

| Metric                     | Description                                                             |
|----------------------------|-------------------------------------------------------------------------|
| **CAI** (Coordinate Agreement Index) | r between human scores and model predictions across axes         |
| **CVI** (Coordinate Variance Index)  | Std. dev. across multiple runs of same model                     |
| **CCS** (Coordinate Contradiction Score) | Conflict magnitude between opposing axes (e.g., empathy vs cruelty) |

Use these consistently in both diagnostics and visual export summaries.

---

## 🖼 Coordinate Visualizations (Standard Reference)

- **Coordinate Plane**: Visual field (e.g., ellipse or radar chart)
- **Narrative Center**: Weighted centroid of all coordinates
- **Axis Rays**: Labeled score lines
- **Contradiction Arcs**: Highlighted if CCS > 0.5

