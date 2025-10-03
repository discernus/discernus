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

**Advanced Markers Structure** (Recommended Best Practice):

While the specification shows simple string lists for markers, an enhanced object structure provides superior context for LLM agents:

```yaml
markers:
  positive_examples:
    - phrase: "corrupt elite"
      explanation: "explicit moral corruption claims against elites"
    - phrase: "rigged system"  
      explanation: "systemic corruption language"
  negative_examples:
    - phrase: "disagreement"
      explanation: "policy differences without moral dichotomy"
  boundary_cases:
    - phrase: "out of touch"
      explanation: "depends on whether it implies moral corruption vs. disconnect"
```

This richer format significantly improves agent accuracy by providing detailed context for each example. Framework authors are encouraged to use this enhanced structure when developing complex analytical frameworks.

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

#### **Derived Metrics Best Practices**

**(Recommended for Robust Frameworks)**

When creating derived metrics that involve division or complex calculations, follow these defensive programming practices:

**Division-by-Zero Prevention**:
```yaml
# Add small constant to prevent division by zero
formula: "(numerator) / (denominator + 0.001)"
```

**Salience-Weighted Calculations**:
```yaml
# Safe salience weighting with defensive constant
formula: "(dim_a.raw_score * dim_a.salience + dim_b.raw_score * dim_b.salience) / (dim_a.salience + dim_b.salience + 0.001)"
```

**Tension Metrics** (for measuring strategic contradictions):
```yaml
# Measures tension between competing dimensions
formula: "min(dim_a.raw_score, dim_b.raw_score) * abs(dim_a.salience - dim_b.salience)"
```

**Advanced Statistical Functions**:
```yaml
# Standard deviation calculation using numpy
formula: "np.std([dim_a.salience, dim_b.salience, dim_c.salience])"
# Correlation using scipy
formula: "scipy.stats.pearsonr(dim_a.raw_score, dim_b.raw_score)[0]"
```

**Note**: The Discernus formula engine supports all functions from the available libraries (numpy, pandas, scipy, sklearn, statistics, math, etc.). Framework authors can use any mathematical or statistical function these libraries provide without needing to implement basic operations.

These practices ensure numerical stability and prevent execution failures in edge cases where salience values might sum to zero.

### Section 4: Intended Application & Corpus Fit

**(Required)**

This section defines the proper scope and application of your framework, which is critical for ensuring valid results.

-   **Target Corpus Description**: Describe the ideal corpus for your framework. Be specific about the genre (e.g., "parliamentary debates"), time period (e.g., "21st-century speeches"), or linguistic style (e.g., "formal, prepared remarks") it is designed to analyze.
-   **Known Limitations & Scope**: Discuss the boundaries of your framework. Where might it be misapplied? What kinds of texts would it be unsuitable for? What are the potential pitfalls in interpreting its results?

### Section 4.5: Framework Fit Assessment

**(Required)**

This section defines how to assess whether your framework is working as intended across the corpus. Framework fit is a critical validity measure that determines whether your analytical dimensions are functioning properly and providing meaningful insights.

-   **Framework Fit Definition**: Clearly explain what constitutes good framework fit for your specific framework. This should be grounded in your theoretical foundations and analytical methodology.
-   **Fit Assessment Criteria**: Specify the statistical and analytical criteria that indicate good framework performance. Consider:
    - **Dimensional Distinctiveness**: Are your dimensions measuring different concepts? (Low inter-correlation within conceptual clusters)
    - **Bipolar Validity**: Do opposing dimensions show strong negative correlations as theorized?
    - **Theoretical Coherence**: Do the observed dimensional relationships match your framework's predictions?
    - **Discriminatory Power**: Can your framework distinguish between different types of content as intended?
-   **Fit Score Calculation**: Provide specific statistical formulas for calculating framework fit score (0.0-1.0 scale). This should be implementable by the Statistical Agent using corpus-wide dimensional data.
-   **Interpretation Guidelines**: Explain what different fit score ranges mean for interpreting your results:
    - **0.8-1.0**: Excellent fit - framework is working as intended
    - **0.6-0.8**: Good fit - minor adjustments may be needed
    - **0.4-0.6**: Moderate fit - some dimensions may need refinement
    - **0.2-0.4**: Poor fit - significant framework issues
    - **0.0-0.2**: Very poor fit - framework may be misapplied

**Example Framework Fit Definition**:
```
FRAMEWORK FIT ASSESSMENT for [Your Framework Name]:

Good framework fit is indicated by:
1. Dimensional Distinctiveness: Constructive dimensions show moderate positive correlations (0.3-0.7) with each other, destructive dimensions show moderate positive correlations (0.3-0.7) with each other
2. Bipolar Validity: Opposing dimensions show strong negative correlations (-0.6 to -0.9)
3. Theoretical Coherence: Observed patterns match framework predictions for [specific theoretical claims]
4. Discriminatory Power: Framework can distinguish between [specific content types] with effect sizes > 0.5

FIT SCORE CALCULATION:
framework_fit_score = (dimensional_distinctiveness + bipolar_validity + theoretical_coherence + discriminatory_power) / 4

Where:
- dimensional_distinctiveness = average correlation within constructive cluster + average correlation within destructive cluster
- bipolar_validity = average absolute correlation between opposing dimension pairs
- theoretical_coherence = [framework-specific coherence measure]
- discriminatory_power = [framework-specific discrimination measure]
```

---

## Part 2: The Machine-Readable Appendix

This part of the framework must be a single, valid YAML block placed at the very end of the document. It contains the precise, structured instructions that the Discernus AI agents will use to execute the analysis.

### Formula Engine Capabilities

The Discernus secure execution environment provides access to a comprehensive suite of Python libraries for derived metrics calculations. Framework authors can use any function from the available libraries in their derived metrics formulas.

**Available Library Categories:**
- **Core Data Science**: Mathematical operations, arrays, statistical functions, data manipulation
- **Advanced Statistics**: Hypothesis testing, effect sizes, post-hoc corrections, power analysis
- **Machine Learning**: Algorithms and utilities for pattern recognition and analysis
- **Text Analysis**: Natural language processing, sentiment analysis, pattern matching
- **Mathematical Functions**: Standard mathematical operations, random number generation
- **General Utilities**: Data handling, date/time operations, advanced data structures

**Reference the Complete Library List:**
See the [Core Capabilities Registry](../../discernus/core/presets/core_capabilities.yaml) for the complete list of available libraries and their specific functions. The registry is maintained by the platform and may be updated to include additional libraries as they become available.

**Important Notes:**
- Framework authors can use any function from these libraries in their derived metrics formulas
- The LLM will automatically select appropriate functions based on the required calculations
- All functions are executed in a secure, sandboxed environment with resource limits
- No file I/O, network access, or system operations are permitted

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
  - name: "example_ratio_metric"
    description: "Example of a ratio metric with defensive programming against division by zero."
    formula: "(dimensions.example_dimension_1.raw_score * dimensions.example_dimension_1.salience) / (dimensions.example_dimension_1.salience + 0.001)"

# 5.5: Framework Fit Score (Required)
# Define how to calculate framework fit score for statistical validation
framework_fit_score:
  description: "Assessment of how well the framework applies to the corpus as a whole"
  calculation_method: "Statistical analysis of dimensional relationships and theoretical coherence"
  components:
    - name: "dimensional_distinctiveness"
      description: "Measures whether dimensions within clusters are appropriately correlated"
      formula: "average_correlation_within_constructive_cluster + average_correlation_within_destructive_cluster"
    - name: "bipolar_validity" 
      description: "Measures strength of opposing relationships between dimension pairs"
      formula: "average_absolute_correlation_between_opposing_pairs"
    - name: "theoretical_coherence"
      description: "Measures how well observed patterns match framework predictions"
      formula: "[framework-specific coherence calculation]"
    - name: "discriminatory_power"
      description: "Measures framework's ability to distinguish between content types"
      formula: "[framework-specific discrimination calculation]"
  final_formula: "(dimensional_distinctiveness + bipolar_validity + theoretical_coherence + discriminatory_power) / 4"
  interpretation:
    excellent: "0.8-1.0: Framework working as intended"
    good: "0.6-0.8: Minor adjustments may be needed"
    moderate: "0.4-0.6: Some dimensions may need refinement"
    poor: "0.2-0.4: Significant framework issues"
    very_poor: "0.0-0.2: Framework may be misapplied"

# 5.6: Output Schema (Required)
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
