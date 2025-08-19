# Framework Specification (v10.0)

**Version**: 10.0  
**Status**: Active Standard  
**Replaces**: v9.0

---

## Introduction: The Framework as an Intellectual Artifact

In the Discernus ecosystem, a **Framework** is the intellectual heart of an analysis. It is the canvas on which a researcher sketches their unique intellectual contributions and ideas. It serves as a self-contained, human- and machine-readable document that defines a specific analytical lens through which to interpret a text-based corpus. It translates a complex research question or theory into a set of measurable, evidence-based dimensions.

A framework is both a complete scholarly artifact for human understanding and a fully functional set of computational instructions for the Discernus automated agents. This specification is designed to be a rich, flexible, and robust guide to help you create frameworks of the highest possible quality.

### The Framework Lifecycle: Authoring, Validation, and Execution

To ensure the integrity of all research conducted on the platform, every framework follows a clear lifecycle:

1.  **Authoring**: The researcher, guided by this specification, creates a framework as a `.md` file.
2.  **Validation**: When an experiment is submitted, the Discernus system performs a rigorous automated validation of the framework. This process checks for **structural coherence** and **compliance with this specification**. Frameworks that fail this basic validation will not be executed. The analytical fit between the framework and the corpus is assessed later, during the statistical analysis of the results.
3.  **Execution**: Once validated, the framework's machine-readable appendix is used by the AI agents to conduct a faithful and repeatable analysis of the corpus.

> **Pro Tip for Authors**
> We strongly encourage you to use a high-quality LLM chatbot (such as Gemini 2.5 Pro or Claude 3 Opus) as an authoring partner. Provide the full text of this `v10.0` specification to the chatbot, along with your research ideas, to co-author a draft framework that is likely to pass the automated validation process on the first try.

---

## Part 1: The Scholarly Document (The Human-Readable Narrative)

This part of the framework is written in standard Markdown. It is designed to be read and understood by other researchers, providing the full context, theory, and methodology of your analytical approach.

### Section 1: Abstract & *Raison d'être*

**(Required)**

This is the high-level summary of your framework. It must clearly and concisely answer three questions:

1.  **What is this framework?** (e.g., "A framework for measuring the prevalence of populist rhetoric in political speeches.")
2.  **What problem does it solve?** (e.g., "It provides a quantifiable, evidence-based method for tracking rhetorical trends that are otherwise difficult to assess systematically.")
3.  **Who is it for?** (e.g., "Political scientists, journalists, and civic organizations.")

### Section 2: Theoretical & Empirical Foundations

**(Required)**

This section provides the intellectual and scholarly grounding for your framework. It is crucial for establishing the credibility and validity of your approach.

-   **Literature Review**: Briefly discuss the existing research your framework builds upon.
-   **Core Theories**: Explain the core academic or theoretical concepts that inform your analytical dimensions.
-   **Citations**: You **must** include citations to academic literature, prior research, or other relevant sources to support your claims.

### Section 3: Analytical Methodology

**(Required)**

This is the "how-to" of your framework, explaining the mechanics of your analysis in detail.

-   **Dimensions**: For each analytical dimension, provide a clear and unambiguous definition. Explain what it is intended to measure and why it is important.
-   **Derived & Composite Metrics**: If your framework includes calculated metrics, explain the formula and the rationale behind it. Discuss any weighting schemes, normalization strategies, or validation methods used.
-   **Advanced Concepts (Optional)**: If your framework uses sophisticated techniques (e.g., measuring rhetorical salience, strategic tension, etc.), you must provide a thorough explanation of the concept and its implementation here.

### Section 4: Intended Application & Corpus Fit

**(Required)**

This section defines the proper scope and application of your framework, which is critical for ensuring valid results.

-   **Target Corpus Description**: Describe the ideal corpus for your framework. Be specific about the genre (e.g., "parliamentary debates"), time period (e.g., "21st-century speeches"), or linguistic style (e.g., "formal, prepared remarks") it is designed to analyze.
-   **Known Limitations & Scope**: Discuss the boundaries of your framework. Where might it be misapplied? What kinds of texts would it be unsuitable for? What are the potential pitfalls in interpreting its results?
-   **System Validation Note**: Be aware that the Discernus platform will perform a post-hoc statistical analysis of your framework's fit with your chosen corpus based on the variance in the results. This analysis, which occurs at the end of the experiment, is a key measure of your research design's validity. A low framework-corpus fit score may indicate that the framework was misapplied and could impact the interpretation of the results.

---

## Part 2: The Machine-Readable Appendix

This part of the framework must be a single, valid YAML block placed at the very end of the document. It contains the precise, structured instructions that the Discernus AI agents will use to execute the analysis.

### Section 5: Configuration Appendix

**(Required)**

The appendix must be a single YAML code block.

```yaml
# --- Start of Machine-Readable Appendix ---

# 5.1: Metadata (Required)
metadata:
  framework_name: "your_framework_name"
  framework_version: "1.0.0"
  author: "Your Name or Organization"
  spec_version: "10.0"

# 5.2: Analysis Variants (At least one required)
analysis_variants:
  default:
    description: "The standard analytical protocol for this framework."
    analysis_prompt: |
      You are an expert analyst. Your persona, instructions, and the full
      methodology of the analysis go here. This prompt should contain
      everything the AI needs to know to perform the analysis faithfully.

# 5.3: Dimensions (At least one required)
dimensions:
  - name: "example_dimension_1"
    description: "A clear, concise description of what this dimension measures."
    markers:
      - "linguistic marker 1"
      - "semantic concept 2"
      - "example phrase 3"

# 5.4: Derived Metrics (Optional)
derived_metrics:
  - name: "example_derived_metric"
    description: "A clear description of what this metric calculates."
    formula: "dimensions.example_dimension_1.raw_score * 2"

# 5.5: Output Schema (Required)
# Note: This schema should be authored in YAML for readability.
# The Discernus system will automatically convert it to a strict
# JSON Schema for validation and execution.
output_schema:
  type: object
  properties:
    dimensional_scores:
      type: object
      properties:
        example_dimension_1:
          type: object
          properties:
            raw_score: { type: number, minimum: 0.0, maximum: 1.0 }
            confidence: { type: number, minimum: 0.0, maximum: 1.0 }
            evidence: { type: string }
  required:
    - dimensional_scores

# --- End of Machine-Readable Appendix ---
```
