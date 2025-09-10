# Micro Test Corpus

Four short test documents enabling statistical analysis with two sentiment categories.

## Document Overview

- **Positive Test 1 & 2**: Documents with positive sentiment language
- **Negative Test 1 & 2**: Documents with negative sentiment language

These documents are designed to trigger statistical analysis comparing positive vs negative sentiment categories.

---

## Document Manifest

```yaml
name: "Micro Statistical Test Corpus"
version: "1.0"
spec_version: "8.0"
total_documents: 4
date_range: "2024"

documents:
  - filename: "positive_test_1.txt"
    document_id: "pos_test_1"
    metadata:
      type: "test"
      sentiment_category: "positive"
      author: "Test_Author_A"
      year: 2024
  - filename: "positive_test_2.txt"
    document_id: "pos_test_2"
    metadata:
      type: "test"
      sentiment_category: "positive"
      author: "Test_Author_B"
      year: 2024
  - filename: "negative_test_1.txt"
    document_id: "neg_test_1"
    metadata:
      type: "test"
      sentiment_category: "negative"
      author: "Test_Author_C"
      year: 2024
  - filename: "negative_test_2.txt"
    document_id: "neg_test_2"
    metadata:
      type: "test"
      sentiment_category: "negative"
      author: "Test_Author_D"
      year: 2024
```
