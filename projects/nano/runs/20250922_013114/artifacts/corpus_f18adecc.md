# Nano Test Corpus

Two short test documents for basic pipeline validation.

## Document Overview

- **Positive Test**: Document with positive sentiment language
- **Negative Test**: Document with negative sentiment language

---

## Document Manifest

```yaml
name: "Nano Test Corpus"
version: "1.0"
spec_version: "8.0.2"
total_documents: 2
date_range: "2024"

documents:
  - filename: "corpus/positive_test.txt"
    document_id: "pos_test"
    metadata:
      type: "test"
      sentiment: "positive"
  - filename: "corpus/negative_test.txt"
    document_id: "neg_test"
    metadata:
      type: "test"
      sentiment: "negative"
```
