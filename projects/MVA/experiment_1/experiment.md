---
name: mva_evidence_test
description: Test that the fixed orchestrator properly enforces framework evidence requirements

framework_file: cff_v4_mva.md
models:
  - openai/gpt-4o
runs_per_model: 1
analysis_variant: fully_normative

# Test with minimal corpus for quick verification
corpus_files:
  - sanitized_speech_a1c5e7d2.md
---

# MVA Evidence Test

This is a minimal test to verify that the fixed orchestrator properly enforces framework evidence requirements.