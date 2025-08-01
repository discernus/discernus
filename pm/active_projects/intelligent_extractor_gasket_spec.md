# Specification: The Intelligent Extractor Gasket (Gasket #2)

## 1. Overview and Purpose

This document provides the technical specification for the "Intelligent Extractor," a critical architectural component designed to create a robust, THIN interface between the non-deterministic Analysis Agent and the deterministic MathToolkit.

This component directly addresses the root cause of the `Data Sparsity` and `JSON parsing failed` warnings observed in recent experiment runs. It also provides the definitive architectural solution for the semantic mapping problem identified in **GitHub Issue #254**.

**Related GitHub Issue:** [#254: SemanticMapperAgent: Address Last Meter Framework Translation Issues](https://github.com/discernus/discernus/issues/254)

## 2. The Problem: Syntactic and Semantic Mismatches

The connection between the Analysis Agent and the MathToolkit currently suffers from two distinct but related problems:

1.  **Syntactic Brittleness (The JSON Parsing Failures):** The current `thin_orchestrator` uses a brittle `regex` and `json.loads()` parser. When the Analysis Agent produces even slightly malformed JSON (e.g., a missing comma), the parser fails, and the analysis is discarded, leading to data sparsity.

2.  **Semantic Mismatch (The Cognitive Bias):** As detailed in Issue #254, the Analysis LLM has a strong cognitive bias towards hierarchical data structures (e.g., `scores.dimensions.populism.score`). However, the downstream MathToolkit requires a flat data structure (e.g., `populism_score`). The current "fixes"—enhanced prompting and defensive code in the MathToolkit—are THICK patches that increase complexity and are not guaranteed to work with future models.

These two problems are symptoms of a single architectural flaw: a lack of a proper gasket to mediate the interface between the LLM world and the deterministic code world.

## 3. The Solution: The Intelligent Extractor & Semantic Mapper Gasket

The Intelligent Extractor Gasket replaces the brittle parser with a flexible, intelligent LLM-based component that solves both problems simultaneously. It acts as both a **robust parser** and a **semantic mapper**.

### 3.1. The Raw Analysis Log as Single Source of Truth

The Analysis Agent will produce a **Raw Analysis Log**—a single, human-readable text block that contains everything:
- The raw scores it assigned
- The direct quotes it selected as evidence  
- The reasoning that connects the evidence to the scores

This Raw Analysis Log becomes the foundational artifact that feeds into **two separate gaskets**, creating parallel streams for scores and evidence.

### 3.2. The Parallel Journey Architecture

From the Raw Analysis Log, two distinct streams emerge:

**The Quantitative Stream (Scores):**
1. Raw Analysis Log → Intelligent Extractor Gasket → MathToolkit → Calculated Metrics

**The Qualitative Stream (Evidence):**  
1. Raw Analysis Log → Evidence Distillation → Synthesis Agent

The Intelligent Extractor is specifically responsible for the **LLM-to-Math boundary** in the quantitative stream.

### 3.3. Progressive Distillation Architecture

If the Intelligent Extractor cannot reliably perform the extraction in a single call, we may need to implement a **progressive distillation architecture**—a series of simpler, sequential LLM calls (gasket assemblies) that break down the complex extraction task into manageable steps.

## 4. Technical Implementation

### 4.1. Framework-Agnostic Design

The Intelligent Extractor must work with **any** framework that complies with the Discernus specifications. It cannot be hardcoded to specific dimension names or scoring schemes.

### 4.2. Orchestrator Modification

The `_combine_analysis_results` method within `discernus/core/thin_orchestrator.py` must be refactored. The existing `regex` and `json.loads()` logic will be removed entirely. A new private method, `_extract_and_map_with_gasket`, will be called for each raw analysis response.

### 4.3. The "Gasket" LLM Call

The `_extract_and_map_with_gasket` method will construct and execute the new LLM call.

**Input:**
1.  The raw text `result_content` from the Analysis Agent (the Raw Analysis Log).
2.  The `gasket_schema` from the framework specification (a simple list of required flat column names).

**Model:** A fast and cheap model should be used, such as `vertex_ai/gemini-2.5-flash`.

**Prompt Template:**

```text
You are a highly efficient and accurate data extraction and semantic mapping bot. Your sole purpose is to extract specific numerical scores from a given text and map them to a flat JSON structure.

From the text provided below, find and extract the numerical scores for the following dimensions:
{target_dimensions}

Map these findings to a simple, flat JSON object using these exact key names:
{target_keys}

The values must be a float between 0.0 and 1.0. If a score cannot be found for a dimension, use `null` as its value.

Return ONLY a single, valid JSON object.

Example Input Text: "...the analysis of dimension A results in a score of 0.85, while dimension B has a raw_score of 0.72..."
Example Output:
{"dimension_a_score": 0.85, "dimension_b_score": 0.72}

Do not include any other text, explanation, or markdown formatting in your response.

---
TEXT TO ANALYZE:
{raw_analysis_response}
---
```

**Output:** A simple, clean, flat JSON string that matches the framework's `gasket_schema`.

### 4.4. Framework Integration

The framework specification (v7.0) will include a new `gasket_schema` section that defines the target flat structure for the Intelligent Extractor:

```yaml
gasket_schema:
  target_keys:
    - "dimension_1_score"
    - "dimension_2_score"
    - "dimension_3_score"
  target_dimensions:
    - "Dimension 1"
    - "Dimension 2" 
    - "Dimension 3"
```

The orchestrator will read this schema from the framework and pass it to the Intelligent Extractor, ensuring the gasket works with any compliant framework.

### 4.5. Separation of Concerns

The Intelligent Extractor is **not** responsible for evidence curation or thematic distillation. Those tasks belong to the Evidence Distillation component in the qualitative stream. The Intelligent Extractor's sole responsibility is extracting numerical scores from the Raw Analysis Log and mapping them to the flat schema required by the MathToolkit.

## 5. Benefits of This Approach

1.  **Solves Syntactic Brittleness:** Eliminates parsing failures by using LLM intelligence to understand and extract data from imperfect text.
2.  **Solves Semantic Mismatch:** Explicitly instructs the LLM to perform the hierarchical-to-flat mapping, directly addressing the core problem of Issue #254.
3.  **Framework Agnostic:** Works with any framework that provides a `gasket_schema`, maintaining the THIN principle of experiment-agnostic infrastructure.
4.  **THIN Architecture:** Removes complex, high-maintenance parsing and translation code from the orchestrator and MathToolkit, replacing it with a simple, self-contained gasket.
5.  **Liberates the Analysis Agent:** The primary analysis agent is no longer burdened with complex formatting and mapping rules, allowing it to focus on its core intellectual mission.
6.  **Clear Separation of Concerns:** The gasket has a single, well-defined responsibility: LLM-to-Math score extraction and mapping.
7.  **Enables Parallel Processing:** The Raw Analysis Log enables both quantitative and qualitative streams to proceed independently and efficiently.
