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
> We strongly encourage you to use a high-quality LLM chatbot (such as Gemini Pro or Claude Opus) as an authoring partner. Provide the full text of this specification to the chatbot, along with your research ideas, to co-author a draft framework that is likely to pass the automated validation process on the first try.

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

### Section 3.5: Framework Design for Agent Interaction

**(Recommended Best Practices)**

This section provides guidance on designing framework content that works effectively with Discernus agents. Understanding how your framework integrates with the analysis pipeline is essential for reliable, consistent results.

#### **Framework vs. Agent Responsibilities**

**Framework Should Specify:**
- Domain expertise and theoretical grounding
- Analytical dimensions and their definitions  
- Evidence requirements and confidence criteria
- Framework-specific constraints and concept distinctions
- Scholarly context and intellectual methodology

**Framework Should NOT Specify:**
- Technical output formatting (handled by agents)
- Generic analysis procedures (handled by agents)
- System-level validation requirements (handled by platform)
- File handling or data processing instructions (handled by orchestration)

#### **Agent Integration Principles**

**Provide Context, Not Instructions**: Your framework should provide domain knowledge and analytical context that agents can use to adapt their standard procedures.

**Complement Agent Capabilities**: Agents handle technical aspects (formatting, validation, error handling). Focus on intellectual content (theory, definitions, domain expertise).

**Avoid Technical Specifications**: Don't specify output formats, analysis steps, or system behaviors - these are handled by the platform.

**Focus on Domain Expertise**: Establish clear expert personas and theoretical grounding that agents can incorporate into their specialized prompts.

#### **Effective Framework Content Patterns**

**Domain Expertise Definition**:
```
You are an expert [DOMAIN] analyst specializing in [SPECIALTY], 
grounded in [THEORETICAL FOUNDATION]. 
```

**Framework-Specific Guidance**:
```
IMPORTANT DISTINCTIONS: [Include critical concept clarifications]
- [Concept A] measures [specific thing] (distinct from [similar concept])
- Use exact dimension names as specified - do not substitute similar concepts

ANALYTICAL APPROACH: [Your framework's unique methodology]
- [Key theoretical principle 1]  
- [Key analytical insight 2]
```

**Evidence and Confidence Standards**:
```
EVIDENCE REQUIREMENTS: [Framework-specific evidence standards]
- [Type of evidence needed for this domain]
- [Confidence criteria specific to your framework]
```

#### **Advanced Framework Concepts**

**Salience vs. Intensity Distinction** (for frameworks using rhetorical emphasis):
```
SALIENCE ≠ INTENSITY. In your framework documentation, clearly explain:
- Intensity: How strong the concept appears (0.0-1.0)
- Salience: How prominent/emphasized the concept is (0.0-1.0)
- Why this distinction matters for your analytical approach
```

**Framework-Specific Evidence Standards**:
```
Define what constitutes valid evidence for your domain:
- Direct quotations vs. paraphrases
- Contextual requirements for ambiguous references  
- Domain-specific evidence quality criteria
```

**Confidence Calibration Guidelines**:
```
Provide domain-specific confidence criteria:
- What constitutes "clear evidence" in your field
- How uncertainty should be handled
- Field-specific validation approaches
```

#### **LLM Error Prevention Strategies**

**(Critical for Reliable Results)**

**Prevent Anchoring Bias**:
```
AVOID ANCHORING: Don't provide example scores in your descriptions
❌ "Fear (like 0.8 in crisis speeches)"
✅ "Fear: Crisis language and threat perception"
```

**Prevent Concept Conflation**:
```
EXPLICIT DISTINCTIONS: Always clarify similar concepts
✅ "Compersion measures joy from others' success (distinct from compassion)"
✅ "Individual dignity focuses on universal worth (not personal achievement)"
```

**Prevent Scale Drift**:
```
ANCHOR EXPECTATIONS: Provide clear boundary definitions
✅ "0.0 means complete absence, not just low presence"
✅ "1.0 means dominant theme, not just strong presence"
```

**Prevent Evidence Fabrication**:
```
EVIDENCE REQUIREMENTS: Specify exact quotation standards
✅ "Provide exact quotes, not paraphrases"
✅ "If evidence is ambiguous, lower confidence score accordingly"
```

#### **Sequential Analysis Strategies**

**(Highly Recommended for Complex Frameworks)**

For frameworks with multiple dimensions (5+), sequential evaluation significantly improves analysis quality:

**Why Sequential Analysis Works Better**:
- **Reduced Cognitive Load**: LLM can focus on one concept at a time
- **Prevents Cross-Contamination**: No interference between similar dimensions
- **Higher Quality Evidence**: More thorough search for dimension-specific indicators
- **Better Calibration**: Consistent scale interpretation without comparative bias

**Implementation Approaches**:

**Approach 1: Dimensional Pairs**
```yaml
analysis_variants:
  sequential_identity:
    description: "Focus on identity dimensions only."
    analysis_prompt: |
      Focus exclusively on: [Dimension A] vs [Dimension B]
      [Detailed prompt for just this opposing pair]
  
  sequential_emotional:
    description: "Focus on emotional dimensions only."
    analysis_prompt: |
      Focus exclusively on: [Dimension C] vs [Dimension D]
      [Detailed prompt for just this opposing pair]
```

**Approach 2: Single Dimension Focus**
```yaml
analysis_variants:
  single_dimension_fear:
    description: "Evaluate fear dimension only."
    analysis_prompt: |
      Evaluate only the fear dimension (0.0-1.0)
      [Comprehensive prompt for single dimension]
```

**Orchestration Strategy**: Use multiple analysis passes, then combine results for complete framework evaluation.

#### **Common Framework Design Pitfalls**

**Pitfall 1: Technical Overspecification**
- ❌ Specifying output formats, file handling, or system procedures
- ✅ Focusing on domain knowledge, theoretical grounding, and analytical concepts

**Pitfall 2: Generic Analysis Instructions**
- ❌ "Step 1: Read the text, Step 2: Identify themes..."
- ✅ Domain-specific guidance that complements agent procedures

**Pitfall 3: Conflated Concepts Without Distinction**
- ❌ Using similar concepts interchangeably
- ✅ Clear distinctions between related concepts (e.g., "compersion vs compassion")

**Pitfall 4: Insufficient Domain Context**
- ❌ "Analyze the data"
- ✅ Rich theoretical context that helps agents understand the analytical approach

#### **Scoring Calibration Guidelines**

**(Critical for LLM Consistency)**

Provide specific calibration guidance for your 0.0-1.0 scales to ensure consistent LLM interpretation:

**Calibration Template**:
```
SCORING CALIBRATION for [DIMENSION_NAME]:
- 0.9-1.0: [What constitutes maximum intensity in your domain]
- 0.7-0.8: [Strong but not overwhelming presence] 
- 0.5-0.6: [Moderate, balanced presence]
- 0.3-0.4: [Weak but detectable presence]
- 0.1-0.2: [Minimal, barely present]
- 0.0: [Complete absence]
```

**Example for Political Discourse**:
```
SCORING CALIBRATION for Fear Dimension:
- 0.9-1.0: Existential crisis language, imminent catastrophe, survival threats
- 0.7-0.8: Serious concern, significant risk, urgent problems requiring action
- 0.5-0.6: Moderate worry, potential problems, cautionary language
- 0.3-0.4: Minor concerns, brief mentions of risk, subtle anxiety
- 0.1-0.2: Occasional uncertainty, mild caution, background worry
- 0.0: No fear language, threat perception, or crisis indicators
```

#### **Examples and Anti-Examples**

**(Essential for LLM Accuracy)**

For each dimension, provide concrete examples to prevent misinterpretation:

**Example Template**:
```
[DIMENSION_NAME] Indicators:
✅ POSITIVE EXAMPLES: 
- "[Specific phrase 1]" - [why this qualifies]
- "[Specific phrase 2]" - [why this qualifies]
- "[Specific phrase 3]" - [why this qualifies]

❌ NEGATIVE EXAMPLES (might be confused but don't qualify):
- "[Similar phrase 1]" - [why this doesn't qualify]
- "[Similar phrase 2]" - [why this doesn't qualify]

⚠️ BOUNDARY CASES:
- "[Ambiguous phrase]" - [how to resolve this ambiguity]
```

#### **Concept Disambiguation Strategies**

**(Critical for Complex Frameworks)**

When dimensions might overlap or conflict, provide clear resolution strategies:

**Disambiguation Template**:
```
CONCEPT OVERLAP RESOLUTION:
When [Concept A] and [Concept B] appear together:
- Priority Rule: [Which takes precedence and why]
- Context Clues: [How to use surrounding text to resolve]
- Boundary Criteria: [Specific criteria for edge cases]

CONFLICTING INDICATORS:
When text contains both positive and negative indicators:
- Scoring Strategy: [How to handle mixed signals]
- Evidence Priority: [Which evidence to emphasize]
- Confidence Adjustment: [How to reflect uncertainty]
```

#### **Framework Testing & Validation**

**Before Finalizing Your Framework**:
1. **Test with sample texts** - Ensure your dimensional definitions work in practice
2. **Check conceptual clarity** - Verify that distinctions between similar concepts are clear
3. **Validate scoring calibration** - Confirm LLMs interpret your scales consistently
4. **Test disambiguation strategies** - Verify boundary cases are handled correctly
5. **Review agent compatibility** - Ensure your framework content complements rather than conflicts with agent procedures

**Quality Indicators for LLM-Optimized Frameworks**:
- **Scoring Consistency**: Clear calibration produces consistent results across similar texts
- **Conceptual Precision**: Examples and anti-examples prevent misinterpretation
- **Disambiguation Clarity**: Overlap and conflict resolution strategies work reliably
- **Evidence Grounding**: Specific guidance produces high-quality textual evidence

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
# Provide domain expertise and theoretical context for agents
analysis_variants:
  default:
    description: "The standard analytical protocol for this framework."
    analysis_prompt: |
      You are an expert [YOUR_DOMAIN] analyst specializing in [YOUR_SPECIALTY], 
      grounded in [YOUR_THEORETICAL_FOUNDATION]. Your task is to analyze the 
      provided text using the [YOUR_FRAMEWORK_NAME].

      FRAMEWORK METHODOLOGY:
      [Brief description of your analytical approach and theoretical foundation]

      DIMENSIONAL ANALYSIS:
      You must evaluate [N] dimensions across [N] opposing pairs:
      - [Dimension Pair 1]: [Description and theoretical significance]
      - [Dimension Pair 2]: [Description and theoretical significance]

      IMPORTANT DISTINCTIONS: [Critical concept clarifications]
      - [Concept A] measures [specific thing] (distinct from [similar concept])
      - Use exact dimension names as specified - do not substitute similar concepts

      EVIDENCE STANDARDS: [Framework-specific requirements]
      - [Type of evidence needed for this domain]
      - [Quality criteria for textual support]

      ANALYTICAL APPROACH: [Your framework's unique methodology]
      - [Key theoretical principle that guides analysis]
      - [Specific analytical insights relevant to your domain]

      CONTEXTUAL GUIDANCE: [Corpus-specific analysis considerations]
      - [How your framework applies to the target corpus type]
      - [What to emphasize in this specific context]
      - [Common patterns or challenges in this domain]

  # Recommended: Sequential analysis variants for complex frameworks (5+ dimensions)
  sequential_pair_1:
    description: "Focus on [Dimension Pair 1] for detailed analysis."
    analysis_prompt: |
      You are an expert [DOMAIN] analyst. Focus exclusively on evaluating 
      [Dimension A] vs [Dimension B] in the provided text.
      
      [Include specific guidance, examples, and calibration for just these dimensions]
      
  sequential_pair_2:
    description: "Focus on [Dimension Pair 2] for detailed analysis."
    analysis_prompt: |
      You are an expert [DOMAIN] analyst. Focus exclusively on evaluating
      [Dimension C] vs [Dimension D] in the provided text.
      
      [Include specific guidance, examples, and calibration for just these dimensions]
      
  # Optional: Additional variants for different research contexts
  # descriptive_only:
  #   description: "Simplified version for basic pattern recognition."
  #   analysis_prompt: |
  #     [Domain expertise with simplified analytical requirements]

# 5.3: Dimensions (At least one required)
# Include comprehensive guidance for reliable LLM analysis
dimensions:
  - name: "example_dimension_1"
    description: "A clear, concise description of what this dimension measures."
    markers:
      positive_examples:
        - "specific phrase that clearly indicates this dimension"
        - "another unambiguous indicator"
        - "contextual pattern that qualifies"
      negative_examples:
        - "similar phrase that doesn't qualify - explanation why"
        - "potentially confusing term - why it's different"
      boundary_cases:
        - "ambiguous phrase - resolution strategy"
    scoring_calibration:
      high: "0.7-1.0: [What constitutes strong presence]"
      medium: "0.4-0.6: [What constitutes moderate presence]" 
      low: "0.1-0.3: [What constitutes weak presence]"
      absent: "0.0: [What constitutes complete absence]"
  - name: "example_dimension_2"
    description: "Description of the second dimension (often opposing the first)."
    markers:
      positive_examples:
        - "contrasting linguistic patterns"
        - "opposite semantic indicators"
      negative_examples:
        - "phrases that might be confused with dimension_1"
      boundary_cases:
        - "overlapping concepts - disambiguation strategy"
    disambiguation:
      overlap_with_dimension_1: "When both appear, prioritize [X] based on [criteria]"
      conflict_resolution: "When indicators conflict, use [strategy]"

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
        example_dimension_1: { $ref: "#/definitions/score_object" }
        example_dimension_2: { $ref: "#/definitions/score_object" }
        # Add all your dimensions here
  required: [ "dimensional_scores" ]
  definitions:
    score_object:
      type: object
      properties:
        raw_score: { type: number, minimum: 0.0, maximum: 1.0 }
        salience: { type: number, minimum: 0.0, maximum: 1.0 }
        confidence: { type: number, minimum: 0.0, maximum: 1.0 }
        evidence: { type: string }
      required: [ "raw_score", "salience", "confidence", "evidence" ]

# --- End of Machine-Readable Appendix ---
```
