# Product Enhancement Case: Integrating BERTopic into Discernus for Semantic Corpus Management

---

## 🧭 Executive Summary (Bottom Line)

Discernus aims to make discourse science reproducible by orchestrating human and AI evaluation across structured analytical frameworks. Yet today, its ingestion layer lacks a semantic substrate—there is no system-level awareness of what topics texts are about. As a result, sampling is blind, prompting is brittle, and rater calibration lacks topical grounding.

**BERTopic** offers a lightweight but powerful enhancement: by integrating topic modeling into ingestion, we give Discernus the ability to *cluster, query, and reason over discourse thematically*. This scaffolds higher-order features—prompt routing, contrastive triplet sampling, bias audits—with minimal disruption to existing infrastructure.

---

## 🧩 Current State of Infrastructure

| Layer | Current Behavior | Limitation |
|-------|------------------|------------|
| Ingestion | Validate → Hash → Store → Register | No semantic indexing |
| Corpus Storage | Filesystem + DB registry | Unqueryable by content |
| Experimentation | Pull text → Prompt → Score | No topic-awareness in selection |
| Framework Alignment | Hard-coded by prompt | No thematic routing |

---

## 🌐 BERTopic Integration: Product Vision

**What it adds:** A semantic layer on top of ingestion that attaches topic metadata to each document, enabling downstream components to reason about *what kind of text they are handling*.

**What it enables:**
- Topically-aware LLM prompts
- Intelligent sampling for contrastive evaluations
- Rater stratification and thematic balance
- Corpus coverage visualization

---

## 🛣️ Phased Implementation Plan

### **Phase 1: Passive Enrichment (MVP)**

- Add `bertopic_enricher.py` to ingestion pipeline
- Generate and store: topic ID, label, confidence, top keywords
- Sidecar JSON or new DB column per doc

**Output Example:**
```json
{
  "topic_id": 12,
  "topic_label": "Populist resentment",
  "confidence": 0.89,
  "keywords": ["elite", "people", "corruption", "media"]
}
```

**Impact:** No change to rest of system, but metadata is now queryable and auditable.

#### Phase 1 Prototype (`bertopic_enricher.py`)
```python
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
import json
import os
from typing import List

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
topic_model = BERTopic(embedding_model=embedding_model)

def enrich_with_topics(documents: List[str], doc_ids: List[str], output_dir: str):
    topics, probs = topic_model.fit_transform(documents)
    topic_info = topic_model.get_topic_info()

    os.makedirs(output_dir, exist_ok=True)

    for doc, doc_id, topic, prob in zip(documents, doc_ids, topics, probs):
        if topic == -1:
            continue  # Skip outliers

        topic_keywords = topic_model.get_topic(topic)
        enrichment = {
            "topic_id": topic,
            "topic_label": topic_info.loc[topic_info.Topic == topic, "Name"].values[0],
            "confidence": float(prob),
            "keywords": [kw for kw, _ in topic_keywords]
        }
        with open(os.path.join(output_dir, f"{doc_id}_topic.json"), "w") as f:
            json.dump(enrichment, f, indent=2)
```

---

### **Phase 2: Prompt Routing & Triplet Sampling**

- Use topic metadata to:
  - Route documents to framework-appropriate prompts
  - Build contrastive triplets across or within topic boundaries
- Add topic-level filters in experiment orchestrator

---

### **Phase 3: Rater Assignment + Corpus Audits**

- Group raters by ideological profile → assign topic-balanced sets
- Visualize corpus coverage across topics
- Detect thematic gaps or overweights in datasets

---

## 📊 Pros and Cons

| Pros | Cons |
|------|------|
| ✦ Semantic understanding of documents | ⚠ BERTopic models are corpus-dependent; topics shift over time |
| ✦ Better LLM prompt relevance | ⚠ Topic boundaries not always interpretable by humans |
| ✦ More meaningful triplets | ⚠ Adds memory/compute load at ingestion |
| ✦ Rater balancing and coverage analysis | ⚠ Introduces additional layer of metadata to maintain |
| ✦ Easy to plug into current pipeline | ⚠ Requires monitoring topic coherence periodically |

---

## 🔥 Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| **Topic instability over time** | Freeze BERTopic model per versioned corpus snapshot |
| **Poor clustering on small corpora** | Use MiniLM embeddings + tune HDBSCAN params |
| **Loss of interpretability** | Use manual topic labeling or auto-label fallback |
| **Ingestion slowdowns** | Batch process enrichment asynchronously post-validation |

---

## 🧠 Strategic Payoff

- **Immediate**: Rich metadata enables better sampling, prompting, and documentation.
- **Mid-term**: Paves way for automated framework alignment and blind spot detection.
- **Long-term**: Positions Discernus as a *semantic operating system* for human-AI discourse analysis.

---

## ✅ Recommendation

Proceed with **Phase 1 MVP**: Passive metadata enrichment using BERTopic. Minimal infrastructure change, high insight yield. Evaluate impact on prompt selection and triplet quality, then plan Phase 2 based on operational feedback.
