# Methodology: The Discernus Analysis Agent

This document details the internal methodology of the Discernus Analysis Agent. It is intended for researchers who wish to understand not just *what* the agent does, but *how* it performs its analysis and *why* it is designed the way it is. The principles outlined below have been developed and refined through extensive testing to ensure the production of stable, reliable, and conceptually sound analytical results.

## 1. Core Principle: One Document, One LLM Call

The single most important principle governing the analysis process is that **each document in a corpus is processed in a separate, independent call to the language model.**

Early versions of the agent attempted to analyze an entire corpus in a single batch call to the LLM. This approach was found to be fundamentally unreliable. When multiple documents are presented in a single context window, the model can suffer from "concept blending," where the rhetorical features of one document bleed into the analysis of another. This leads to inaccurate scores and invalidates the results.

By enforcing a strict "one document, one call" policy, we ensure analytical integrity. The analysis for each document is completely sandboxed, free from the influence of other texts in the corpus.

## 2. Model Configuration for Analytical Reliability

Achieving reliable and replicable results from a Large Language Model requires a configuration that prioritizes deterministic output over creativity. Our methodology is built on two key configuration principles:

### 2.1. Low Temperature for High Consistency

The `temperature` parameter, which controls the randomness of the model's output, is the most critical setting for analytical tasks. The Analysis Agent uses a **low temperature setting (typically between 0.0 and 0.2)** for all analytical calls.

- **High Temperature (`> 0.7`)**: Useful for creative tasks like brainstorming or writing stories, but disastrous for analysis. It produces high variance and increases the likelihood that the model will fail to adhere to the required structured data format (e.g., JSON).
- **Low Temperature (`< 0.2`)**: Constrains the model to its most probable, and therefore most stable and consistent, outputs. This is essential for ensuring that repeated analyses of the same text yield similar results. Our internal testing has shown this to be the single most important factor in eliminating catastrophic model failures and reducing scoring variance.

### 2.2. Matching Model Capability to Framework and Prompt Complexity

It is important to understand that the final prompt sent to the language model is a composite artifact, constructed at runtime. The agent dynamically combines the **analytical framework** (e.g., `cff_v10.md`) with its own internal **prompt template** (`prompt.yaml`). The framework provides the specific dimensions, definitions, and examples for the analysis, while the template provides the instructions, output schema, and methodological constraints (like the 3-shot median technique). The combined complexity of these two components determines the overall task complexity.

The system supports multiple models (e.g., Gemini Flash for speed, Gemini Pro for capability). Our methodology dictates that the complexity of the analytical task must match the capability of the model.

- **Simple Frameworks and Prompts (e.g., Single-Pass Analysis)**: These are suitable for efficient, cost-effective models like Gemini Flash.
- **Complex Prompts (e.g., Multi-Step Internal Analysis)**: These require more capable (and more expensive) models like Gemini Pro to be executed reliably. Our testing has shown that sending a highly complex prompt to a less capable model is a primary cause of structured output failures.

## 3. The 3-Shot Median Aggregation Technique

For high-stakes analysis, the agent employs a "3-shot median aggregation" prompt. This is a robustness mechanism designed to mitigate the impact of a single flawed analytical perspective from the LLM.

The process is as follows:

1. The prompt instructs the model to perform **three independent internal analyses** of the same text, each from a slightly different conceptual perspective ("Evidence-First", "Context-Weighted", "Pattern-Based").
2. This generates three internal scores for each dimension.
3. The agent is instructed to report the **median** of these three scores as the final `raw_score`.

The primary benefit of this technique is **outlier resistance**. If two perspectives produce scores of 0.2 and 0.3, but a third produces a wildly divergent score of 0.9, the median (0.3) provides a much more stable result than the average (0.47).

## 4. The Objective Confidence Score

A limitation of using the median is that it discards information about the degree of agreement between the three internal analyses. A set of scores like (0.4, 0.5, 0.6) and (0.1, 0.5, 0.9) both produce a median of 0.5, but the second set indicates far greater analytical uncertainty.

To resolve this, the agent redefines the `confidence` score as an **objective measure of analytical consistency.** The prompt instructs the model to calculate it using a simple formula:

**`confidence = 1 - (maximum_internal_raw_score - minimum_internal_raw_score)`**

This formula converts the range of the three internal scores into a normalized, inverse measure of variance.

- A `confidence` of **1.0** means all three perspectives produced the exact same score (zero variance).
- A `confidence` of **0.1** means the internal scores were highly divergent (e.g., 0.0, 0.5, and 0.9).

This "hack" transforms the confidence score from a subjective guess into a transparent, data-rich signal of the model's internal consistency for each specific dimension, recapturing the information that would otherwise be lost by the median.

## 5. Grounding Analysis in Evidence

To ensure the agent's analysis is not an opaque "black box," the system prompt enforces two additional requirements that anchor its scoring in direct textual evidence. These outputs make the agent's reasoning transparent and fully auditable by a human researcher.

### 5.1. Evidence Collection

For every dimension it scores, the agent is required to extract **1-2 high-quality quotes** from the source text that best exemplify its reasoning for the score. This provides a direct, qualitative check on the quantitative score. A researcher can immediately see *why* the agent assigned a high score for a given dimension by reviewing the evidence it selected.

### 5.2. Full-Text Document Markup

In addition to the summary quotes, the agent must produce a **marked-up version of the complete source document**. In this version, every phrase or sentence relevant to a dimension is annotated inline.

This provides a comprehensive, fine-grained view of the agent's interpretation. It allows a researcher to see not just the "best" examples, but the totality of the evidence the agent considered, all within the original context of the document. This is a powerful tool for auditing the agent's analysis and understanding its interpretation of nuanced text.

## 6. Outputs for Independent Research

To facilitate transparency and enable researchers to perform their own independent statistical analysis, the Analysis Agent produces two primary structured data outputs. These files are saved as CSVs in the `artifacts` directory for each experiment run, allowing for easy ingestion into external statistical software (e.g., R, SPSS, Python/pandas).

### 6.1. `scores.csv`

This file contains a comprehensive record of all quantitative scores for each document in the corpus. Each row represents a document and includes columns for:
- Raw scores for each framework dimension.
- Salience and confidence scores for each dimension.
- Any derived metrics calculated from the raw scores.

### 6.2. `evidence.csv`

This file contains a complete collection of all evidence quotes extracted by the agent during its analysis. Each row includes:
- The document ID from which the quote was taken.
- The dimension the quote is associated with.
- The full text of the evidence quote.

These two files provide researchers with the complete, disaggregated data necessary to replicate the system's findings, perform their own statistical tests, or conduct deeper qualitative analysis on the evidence.

### 6.3. Raw Provenance Artifacts

For complete traceability and replication, the agent also saves the raw, unprocessed outputs from its analysis. These artifacts provide a complete provenance trail, allowing a researcher to trace the data from the initial LLM response through to the final CSVs. They are also saved in the `artifacts` directory.

-   **`composite_analysis_*.json`**: This is the raw JSON payload returned directly by the language model. It contains the complete, unprocessed analysis, including the scores, evidence, and full marked-up document for each text.
-   **`marked_up_document_*.md`**: For convenience, the full marked-up document is also saved as a separate Markdown file, allowing for easy review outside of the main JSON structure.

These raw artifacts are the ground truth of the analysis. A researcher can use them to independently verify that the data was extracted and processed correctly into the final `scores.csv` and `evidence.csv` files.

## 7. Iterative Framework Refinement

The final pillar of the methodology is the principle of iterative conceptual refinement. The analytical frameworks (e.g., `cff_v10.md`) are not static documents; they are treated as an active part of the research process.

When variance is observed in a specific dimension even after technical variables have been controlled for, it is treated as a signal that the framework's definition for that dimension may be ambiguous. The solution is to refine the framework itself.

Our investigation into the `Amity` and `Enmity` dimensions of the CFF serves as a case study. The initial definitions were too vague to handle complex texts that blended criticism with calls for reconciliation. To resolve this, the framework was updated with:

- **More Precise Descriptions**: Distinguishing between criticism of *systems* and hostility toward *people*.
- **Explicit Disambiguation Rules**: Providing guidance on how to score texts that describe a hostile present while calling for a cooperative future.
- **Targeted Examples**: Adding new boundary cases to better illustrate these nuances for the model.

This feedback loop—whereby scoring instability informs conceptual refinement—is a core part of the methodology for achieving high-precision, high-reliability analysis.
