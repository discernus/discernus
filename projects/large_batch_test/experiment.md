---
name: "large_batch_test"
description: "Large batch test experiment to evaluate LiteLLM's built-in retry mechanisms with 429 errors"
framework: "framework.md"
corpus_path: "corpus/"
---

# Large Batch Test Experiment

This experiment tests how the system handles larger document batches and evaluates LiteLLM's built-in retry mechanisms for handling Vertex AI 429 errors under Dynamic Shared Quota (DSQ). 