---
version: "7.0"
name: gasket_debug_test
description: Debug test for gasket schema extraction
hypothesis: Test gasket schema conversion
research_questions:
  - "Does gasket schema conversion work?"
hypotheses:
  H1_Test: "Gasket schema should be detected and converted"
success_criteria:
  - "Gasket schema detected successfully"
model:
  analysis: "vertex_ai/gemini-2.5-flash-lite"
  synthesis: "vertex_ai/gemini-2.5-flash-lite"
framework: "framework.md"
corpus_path: "corpus/"
---