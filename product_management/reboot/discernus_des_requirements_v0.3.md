# Discernus Experiment Specification – **Detailed Requirements Draft v0.3**
*(Scope & Field‑Level Guidance for the Unified “DES” File)*  
*Date: 2025‑06‑25*

---

## 1 – Purpose & Goals  
- **Single‑source‑of‑truth**: capture every input *visible to the LLM* plus execution settings and provenance in **one YAML/JSON file** (`*.des.yaml`).  
- **Machine‑verifiable**: conforms to a top‑level JSON Schema with modular `$defs` but *no implicit defaults*.  
- **Human‑readable**: clear field names, canonical ordering, and rich inline comments (YAML) so researchers can open, edit, and diff in a text editor.  
- **Composable**: sub‑objects may be **inlined** or **referenced** by slug @ version (e.g., `mft@v1.0`).  
- **Deterministic execution**: a cryptographic `lock` section pins content hashes, guaranteeing replication.  

---

## 2 – Top‑Level Document Layout  

```yaml
experiment_meta:      # Administrative metadata
framework:            # Theory axes & anchors
prompt_template:      # LLM prompt scaffolding
weighting_scheme:     # (optional) numeric weights
corpus:               # Input text collection
execution:            # Model + runtime knobs
output:               # Report & export formats
validation:           # Desired eval metrics
lock:                 # SHA‑256 digests (auto)
```

---

## 3 – Field‑by‑Field Requirements  

### 3.1 `experiment_meta` (object)  
| Field | Type | Required | Constraints | Example |
|-------|------|----------|-------------|---------|
| title | string | ✔ | ≤ 140 chars | "MFT vs PFT on US Inaugurals" |
| description | string | ✔ | ≤ 1 000 chars | Free‑text Markdown |
| authors | array<string> | ✔ | 1 – 10 items | ["J. Doe"] |
| date_created | string | ✔ | ISO 8601 date | "2025‑07‑01" |
| des_version | string | ✔ | vMAJOR.MINOR | "v1.0" |
| license | string | ✖ | SPDX id | "CC‑BY‑4.0" |
| tags | array<string> | ✖ | ≤ 20 items | ["validation", "speech"] |

### 3.2 `framework` (object or slug)  
If slug syntax `id@version` is used, engine fetches canonical file and fills `lock`.  
Inline object must satisfy legacy Framework Specification v3.1 with additions:  
- `schema_version` moved under framework.  
- Optional `default_weighting_scheme`.  
- Required cross‑checks: axis labels unique ≤ 32 chars; ≥ 1 anchor per axis.

### 3.3 `prompt_template` (object or slug)  
Mandatory fields when inlined:  

| Field | Type | Constraints |
|-------|------|-------------|
| base_prompt | string | must include `{text}` placeholder once |
| input_format | enum | direct_analysis / hierarchical / multi_turn |
| temperature | number | 0 – 2 |
| max_tokens | integer | 1 – 8192 |
| stop | array<string> | ≤ 4 items |
| tooling_instructions | string | optional system message |

### 3.4 `weighting_scheme` (object or slug)  
Each axis present in framework must appear in `weights`.  
```yaml
weighting_scheme:
  name: balanced_pairs
  weights:
    care: 1.0
    fairness: 1.0
    loyalty: 1.0
    authority: 1.0
    sanctity: 1.0
```
Rules: all weights ≥ 0; homogeneous type; sum not forced to 1.

### 3.5 `corpus` (object)  
Modes: slug reference, manifest of file paths, or embedded texts.  
Exactly one of `slug | manifest | texts` required.

### 3.6 `execution` (object)  
Fields: model (✔), batch_size (✔), retry_policy, cost_cap_usd, queue.

### 3.7 `output` (object)  
Fields: html_report (default true), pdf_report, raw_json, csv_summary, storage (enum: local/supabase/s3).

### 3.8 `validation` (object)  
Optional thresholds (e.g., mft_correlation_threshold).

### 3.9 `lock` (object)  
Auto‑populated with SHA‑256 digests, git commit, timestamp.

---

## 4 – Referencing & Inlining Rules  

| Scenario | YAML Pattern | Engine Behaviour |
|----------|--------------|------------------|
| Use stable public | framework: mft@v1.0 | fetch & hash |
| Override temp | prompt_template:
  base: direct_analysis@v2025.06.19
  temperature: 0.3 | patch override |
| Local draft | full object inline | tag `local` if version missing |

---

## 5 – Validation Workflow  

1. JSON Schema validation  
2. Cross‑field axis ↔ weights alignment  
3. Integrity checks on slug fetches  
4. Lockfile write & final re‑validation  

---

## 6 – Reserved Keywords & Versioning  

- Reserved top‑levels: experiment_meta, lock  
- No custom key may start with `_discernus_`  
- Breaking spec updates bump major version.

---

## 7 – Examples & Templates  

Two starter files will ship in `examples/`  
- Minimal inline stub  
- Slug‑based study with overrides

---

## 8 – Migration Guide  

`des migrate old/` bundles legacy YAML quartet into unified DES, adds lock.

---

*This requirement sheet provides the detail your collaborator needs to formalise the JSON Schema and author canonical templates.*  
