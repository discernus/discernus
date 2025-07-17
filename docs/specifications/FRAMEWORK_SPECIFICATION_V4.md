# Framework Specification (v4.0)

**Version**: 4.0  
**Status**: Active

A Discernus framework is a self-contained markdown file that embodies the core principles of computational social science research. It serves as both human-readable methodology and machine-executable instructions, ensuring perfect coherence between theory and practice.

---

## Part I: Core Principles

### 1. The THIN Philosophy

**Principle**: LLMs do intelligence, software does infrastructure.

**In Practice**: Your framework documentation should contain rich methodological intelligence that guides human researchers. Your YAML prompts should contain that same intelligence translated into natural conversational instructions for LLMs. The software simply routes these instructions - it contains no analytical intelligence itself.

**Anti-Pattern**: Creating beautiful documentation with simple "return JSON" prompts that ignore the methodology.

### 2. Documentation-Execution Coherence

**Principle**: What you promise in documentation must exactly match what you deliver in execution.

**In Practice**: If your methodology section specifies "minimum 3 pieces of textual evidence per score," your YAML prompt must command the LLM to provide exactly that. If your documentation describes confidence assessments, your prompt must generate them.

**Anti-Pattern**: Comprehensive methodology documentation with prompts that generate only basic numerical scores.

### 3. Human Expert Simulation

**Principle**: Framework prompts should feel like natural conversations with domain experts, not technical API calls.

**In Practice**: Write prompts as if you're briefing a brilliant colleague who shares your methodological perspective. Use natural language, provide context, explain reasoning. Avoid robotic instructions or parameter-heavy specifications.

**Anti-Pattern**: Terse, technical prompts that feel like programming commands rather than scholarly discourse.

### 4. Epistemic Integrity

**Principle**: Every analytical decision must be traceable, auditable, and replicable.

**In Practice**: Your framework must generate sufficient evidence and reasoning to support all conclusions. Scores without evidence are meaningless. Patterns without quotations are unverifiable.

**Anti-Pattern**: Black-box scoring where analysts cannot trace numerical outputs back to textual inputs.

---

## Part II: How Principles Manifest in Practice

### The Coherence Requirement

Your framework exists in two forms that must be perfectly aligned:

1. **Human-Readable Methodology**: Rich scholarly documentation explaining your analytical approach
2. **Machine-Executable Instructions**: Natural language prompts that implement that exact methodology

**Example of Coherence**:
```
Documentation says: "Minimum 3 pieces of textual evidence per score"
Prompt says: "For each score, provide at least 3 direct quotations from the text that support your assessment"
```

**Example of Incoherence** (Common Error):
```
Documentation says: "Minimum 3 pieces of textual evidence per score"  
Prompt says: "Return a JSON object with numerical scores"
```

### The Intelligence Distribution

**What belongs in Documentation**:
- Theoretical foundations
- Methodological principles  
- Interpretive frameworks
- Quality standards
- Examples and edge cases

**What belongs in YAML Prompts**:
- The same intelligence translated into conversational instructions
- Specific output requirements that implement the methodology
- Evidence requirements that ensure auditability
- Reasoning requirements that ensure transparency

### The Natural Language Imperative

LLMs excel at natural conversation, not technical specifications. Your prompts should read like expert briefings:

**Good**: "You are an expert political discourse analyst with deep knowledge of rhetorical strategies. Your task is to analyze this text for patterns of social cohesion using the framework's five-dimensional model..."

**Bad**: "Process input text. Score axes 1-5. Output JSON format with fields: worldview, scores, confidence."

---

## Part III: Technical Implementation

### 1. File Structure

A framework file MUST be a standard Markdown (`.md`) file containing:

1. **Human-Readable Methodology**: Standard Markdown documentation
2. **Machine-Executable Configuration**: Single YAML block beginning with `# --- Discernus Configuration ---`

### 2. LLM Processing Optimization

Structure your `analysis_prompt` using this five-phase approach:

**Phase 1: Cognitive Priming**
```
You are an expert [domain] analyst with expertise in [specific area].
Your perspective is grounded in [theoretical framework].
```

**Phase 2: Framework Methodology**
```
Your task is to analyze the provided text using [framework name].
This framework examines [high-level approach] through [analytical lens].
```

**Phase 3: Operational Definitions**
```
The framework evaluates [number] dimensions:
- [Dimension 1]: [Clear definition with examples]
- [Dimension 2]: [Clear definition with examples]
```

**Phase 4: Scoring Protocol**
```
For each dimension, follow this process:
1. Read the text for [specific patterns]
2. Identify [specific evidence types]
3. Score based on [specific criteria]
4. Provide [specific evidence requirements]
```

**Phase 5: Output Specification**
```
Return a single JSON object with:
- [Field 1]: [Specific requirements]
- [Field 2]: [Specific requirements]
- evidence: [Specific format for quotations and reasoning]
```

### 3. Required YAML Schema

```yaml
# --- Discernus Configuration ---

# REQUIRED: Basic metadata
name: unique_framework_name
version: v4.0
display_name: "Human-Readable Framework Name"

# REQUIRED: Analysis variants implementing your methodology
analysis_variants:
  
  default:
    description: "Complete implementation of the framework methodology"
    analysis_prompt: |
      [Your five-phase prompt that implements ALL methodology requirements
       from your documentation, including evidence requirements, confidence 
       assessments, and reasoning explanations]

  # OPTIONAL: Additional variants for specific use cases
  descriptive_only:
    description: "Simplified version focusing on descriptive elements"
    analysis_prompt: |
      [Simplified prompt that still maintains coherence with your methodology]

# OPTIONAL: Post-analysis calculations
calculation_spec:
  composite_score: "(0.25 * dimension_1) + (0.75 * dimension_2)"
```

### 4. Evidence Requirements Integration

**CRITICAL**: If your methodology specifies evidence requirements, your prompt must generate them:

```yaml
analysis_prompt: |
  You are an expert analyst...
  
  For each score, you must provide:
  - At least 3 direct quotations supporting your assessment
  - Confidence rating (0.0-1.0) based on evidence strength
  - Evidence type classification (lexical/semantic/rhetorical)
  - Brief reasoning connecting evidence to score
  
  Return JSON with:
  {
    "scores": {"dimension_1": 0.5, "dimension_2": -0.3},
    "evidence": {
      "dimension_1": ["quote1", "quote2", "quote3"],
      "dimension_2": ["quote4", "quote5", "quote6"]
    },
    "confidence": {"dimension_1": 0.8, "dimension_2": 0.6},
    "reasoning": {"dimension_1": "explanation...", "dimension_2": "explanation..."}
  }
```

---

## Part IV: Quality Assurance

### Self-Validation Checklist

Before deploying your framework, verify:

**Coherence Check**:
- [ ] Every methodology requirement appears in YAML prompts
- [ ] Evidence standards are enforced in execution
- [ ] Documentation promises match prompt deliverables

**Intelligence Check**:
- [ ] Prompts feel like expert briefings, not technical specs
- [ ] Sufficient context provided for reliable LLM performance
- [ ] Natural language throughout, minimal technical jargon

**Completeness Check**:
- [ ] All data needed for subsequent analysis is generated
- [ ] Categorical variables for statistical grouping included
- [ ] Sufficient evidence for auditability and replication

### Common Failure Patterns

**The "Beautiful Documentation" Trap**:
- Rich methodology documentation
- Simple "return JSON" prompts
- **Result**: Scores without evidence, claims without support

**The "Technical Specification" Trap**:
- Robotic, parameter-heavy prompts
- Feels like programming API documentation
- **Result**: Inconsistent LLM performance, unnatural outputs

**The "Incomplete Intelligence" Trap**:
- Prompts missing key methodological requirements
- Generates data insufficient for planned analyses
- **Result**: Failed experiments, incomplete research

---

## Part V: Meta-Prompt Usage

This specification document serves as a meta-prompt. Researchers can:

1. Paste this entire document into Claude or other LLMs
2. Provide their research goals and methodological approach
3. Ask the LLM to help create a compliant framework file
4. Verify the result implements all principles correctly

**Example Meta-Prompt**:
```
I need to create a Discernus framework for analyzing political speeches 
for authoritarian vs democratic discourse markers. Please help me create 
a framework file that follows the Framework Specification v4.0 principles, 
ensuring perfect coherence between documentation and execution.
```

---

## Part VI: Evolution and Maintenance

### Version Control
- Framework files should include clear version numbers
- Changes should be documented and backward-compatible when possible
- Deprecated frameworks should be archived with clear migration paths

### Community Standards
- Frameworks should be peer-reviewable and methodologically sound
- Clear documentation enables replication and extension
- Shared frameworks advance the field's collective knowledge

### Quality Improvement
- Regular testing ensures frameworks perform as documented
- Community feedback improves methodological rigor
- Continuous refinement maintains cutting-edge capabilities

---

## Conclusion

The Framework Specification v4.0 embodies Discernus's core philosophy: intelligent researchers using intelligent tools to produce intelligent research. By maintaining perfect coherence between documentation and execution, frameworks become reliable, auditable, and scientifically sound.

Your framework is not just a configuration file - it's a scholarly contribution that advances computational social science. Build it with the same rigor you would apply to any academic work, ensuring that theory and practice are perfectly aligned.

**Remember**: Great frameworks make great research possible. Incoherent frameworks make great research impossible. 