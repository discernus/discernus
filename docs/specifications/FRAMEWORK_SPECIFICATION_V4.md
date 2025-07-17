# Framework Specification (v4.0)

**Version**: 4.0  
**Status**: Active

A Discernus framework is a self-contained `framework.md` file that is both human-readable and machine-parsable. It serves as the single source of truth for a specific analytical methodology.

---

## 1. File Structure

A framework file MUST be a standard Markdown (`.md`) file and MUST contain two distinct sections:

1.  **Human-Readable Prose (Markdown)**: The majority of the document consists of standard Markdown. This section should include the theoretical background, definitions of the analytical anchors, methodological guidance, and anything else a human researcher needs to understand and trust the framework.
2.  **Machine-Readable Configuration (YAML)**: The document MUST contain one and only one fenced YAML code block that begins with the line `# --- Discernus Configuration ---`. This block contains the explicit, structured instructions for the software.

---

## 2. Embedded YAML Schema

The YAML configuration block provides the "API contract" for the Discernus execution engine.

### **Example `framework.md` file:**
````markdown
# My Custom Framework

This framework analyzes text for its emotional content based on the works of...

## Anchors
- **Joy**: Expressions of happiness, delight...
- **Sadness**: Expressions of sorrow, grief...

# --- Discernus Configuration ---
name: my_custom_framework
version: v4.0
# ... rest of YAML config ...
````

### **Schema Details**

```yaml
# --- Discernus Configuration ---

# REQUIRED: Basic metadata
name: unique_framework_name
version: v4.0
display_name: "Human-Readable Framework Name"

# REQUIRED: A dictionary of one or more analysis variants.
# This allows a single framework file to support multiple types of analysis
# (e.g., a simple descriptive run vs. a full normative evaluation).
# A variant named 'default' MUST be present.
analysis_variants:

  # The 'default' variant is run if the experiment does not specify one.
  default:
    description: "The standard analysis for this framework."
    analysis_prompt: |
      You are an expert... This is the prompt for the default analysis.
      The required JSON structure is:
      {{
        "scores": {{ "default_anchor": 0.0 }},
        "evidence": {{ "default_anchor": [] }}
      }}

  # OPTIONAL: Additional, named variants.
  descriptive_only:
    description: "A simplified analysis focusing only on descriptive elements."
    analysis_prompt: |
      You are an expert... This is the prompt for the descriptive-only analysis.
      The required JSON structure is:
      {{
        "scores": {{ "descriptive_anchor": 0.0 }},
        "evidence": {{ "descriptive_anchor": [] }}
      }}

# OPTIONAL: Specification for post-analysis calculations.
# The `CalculationAgent` will only execute a formula if all of its
# input variables (e.g., 'fear_hope_axis') are present in the 'scores'
# object produced by the selected analysis_variant.
calculation_spec:
  cohesion_index: "(0.25 * fear_hope_axis) + (0.20 * envy_compersion_axis)"

```
---

## 3. Usage as a Meta-Prompt

A key design principle of this specification is that the specification document itself can be used as a "meta-prompt." A researcher can paste the content of this document into a general-purpose chatbot and ask it to help them create a new, compliant framework file. This empowers users to create their own tools without needing to be expert YAML programmers. 