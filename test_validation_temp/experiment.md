---
name: "validation_test"
description: "Testing v7.3 validation"
framework: "../frameworks/seed/temporal/prm_v7.3.md"
corpus: "corpus/"
hypotheses:
  H1_Test: "This should fail v7.3 validation due to v7.1 framework reference"
analysis:
  variant: "default"
  models:
    - "vertex_ai/gemini-2.5-flash-lite"
synthesis:
  model: "vertex_ai/gemini-2.5-flash-lite"
expected_outcomes:
  - "Validation failure"
---

# Validation Test

This experiment should fail validation because it references a v7.1 framework.