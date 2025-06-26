# Discernus Corpus Specification v1.0

## 1 – Purpose  
Defines a portable, machine‑verifiable format for textual corpora used in Discernus experiments.  
The goal is **reproducibility**: any researcher should ingest the corpus, re‑run the experiment, and obtain identical text identifiers and metadata.

---

## 2 – Container Formats  

| Variant | Description | When to Use |
|---------|-------------|-------------|
| **JSONL** | One JSON object per line in a single file (e.g. `corpus.jsonl`). | Medium to large corpora (10 – 100 000 docs). |
| **Directory** | Each document in its own folder: `text.txt` + `meta.json`. | When raw text is > 32 KB or binary assets (images, PDFs) accompany the text. |
| **Parquet** | Columnar storage, schema identical to JSON object. | Very large corpora (> 1 M docs) or Spark/Ray processing. |

All three share the *same field schema* below.

---

## 3 – Field Schema  

| Field | Type | Required | Constraints | Example |
|-------|------|----------|-------------|---------|
| `text_id` | `string` (slug) | ✔ | unique across corpus; `^[a-z0-9_\-]+$` | `"gettysburg_1863"` |
| `text` | `string` | ✔ | UTF‑8; `len(text.split())` 20 – 20 000 | *(full speech text)* |
| `title` | `string` | ✔ | ≤ 300 chars | `"Gettysburg Address"` |
| `language` | `string` (ISO‑639‑1) | ✔ | exactly 2 chars | `"en"` |
| `source` | `string` | ✔ | free text | `"Library of Congress"` |
| `license` | `string` | ✔ | SPDX identifier or URL | `"CC‑BY‑4.0"` |
| `author` | `string` | ✖ | — | `"Abraham Lincoln"` |
| `date` | `string` (YYYY‑MM‑DD) | ✖ | ISO‑8601 | `"1863-11-19"` |
| `url` | `string` | ✖ | valid URL | `"https://loc.gov/item/27286423"` |
| `tags` | `array[string]` | ✖ | ≤ 20 elements | `["civil_war","speech"]` |
| `notes` | `string` | ✖ | Markdown allowed | `"Original punctuation preserved."` |

---

## 4 – Validation Rules  

1. **Uniqueness** – `text_id` must be unique; duplicates hard‑fail.  
2. **Length Bounds** – Text shorter than 20 words or longer than 20 000 words is rejected.  
3. **Encoding** – File must be valid UTF‑8; no BOM.  
4. **Language** – `language` must be ISO‑639‑1; Gatekeeper verifies with fastlang‑id.  
5. **License Safety** – Only SPDX licenses on the approved whitelist (`CC‑*`, `MIT`, `Public‑Domain`) or a resolvable URL.  
6. **Optional SHA‑256** – If a `sha256` field exists, Gatekeeper re‑computes and matches digest.

---

## 5 – JSON Schema (excerpt)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "required": ["text_id", "text", "title", "language", "source", "license"],
  "properties": {
    "text_id": { "type": "string", "pattern": "^[a-z0-9_\-]+$" },
    "text": { "type": "string", "minLength": 1 },
    "title": { "type": "string", "maxLength": 300 },
    "language": { "type": "string", "pattern": "^[a-z]{2}$" },
    "source": { "type": "string" },
    "license": { "type": "string" },
    "author": { "type": "string" },
    "date": { "type": "string", "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}$" },
    "url": { "type": "string", "format": "uri" },
    "tags": {
      "type": "array",
      "items": { "type": "string" },
      "maxItems": 20
    },
    "notes": { "type": "string" }
  },
  "additionalProperties": false
}
```

Save the schema as `corpus_schema_v1.json` beside the corpus.

---

## 6 – Example (JSONL line)

```json
{
  "text_id": "gettysburg_1863",
  "text": "Four score and seven years ago...",
  "title": "Gettysburg Address",
  "language": "en",
  "source": "Library of Congress",
  "license": "Public-Domain",
  "author": "Abraham Lincoln",
  "date": "1863-11-19",
  "url": "https://loc.gov/item/27286423",
  "tags": ["civil_war", "speech"]
}
```

---

## 7 – Integration Points  

- **Corpus Gatekeeper** reads any of the accepted container formats, validates against the JSON Schema, runs dedupe hashing, then inserts rows into the `texts` table.  
- The `Experiment` YAML references corpora by *slug* (e.g., `"corpus: civil_war_speeches_v1"`).  
- Each experiment’s lockfile stores the corpus slug + SHA‑256 of the source file/directory to guarantee immutability.

---

## 8 – Versioning & Changelog  

- `v1.0` (2025‑06‑25) — initial release for MVP.  
- Breaking changes increment the **major** version; non‑breaking additions bump the **minor**.

---

## 9 – License  

The corpus spec itself is released under **CC‑BY‑4.0**.  You are free to use, remix, and extend it with attribution.

