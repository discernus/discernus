# Framework Specification (v4.0)

**Version**: 4.0  
**Status**: Active

A Discernus framework is a self-contained markdown file that embodies the core principles of computational social science research. It serves as both human-readable methodology and machine-executable instructions, ensuring perfect coherence between theory and practice.

---

## Terminology Glossary

To ensure consistency across all frameworks, these terms have specific meanings:

**Framework**: The complete analytical system including theory, methodology, and implementation (e.g., Cohesive Flourishing Framework)

**Domain**: Major conceptual area within a framework that groups related dimensions (e.g., "Emotional Climate Domain", "Stakeholder Relations Domain")

**Dimension**: Individual measurable element that receives a 0.0-1.0 score (e.g., Fear, Hope, Customer Service, Employee Development). This is the primary term for scoreable elements.

**Axis**: Bipolar continuum between opposing concepts, used only when true bipolar relationships exist (e.g., Populism ↔ Pluralism axis in orthogonal frameworks)

**Analysis Variant**: Different analytical approaches within the same framework (e.g., "default" for complete analysis, "descriptive_only" for simplified scoring)

---

## Framework Size and Performance Guidelines

### Character Limit Policy

**Maximum Framework Size**: 15,000 characters (15KB)

**Rationale**: Framework size directly impacts processing efficiency and analysis quality. Oversized frameworks create unnecessarily verbose analysis outputs that reduce synthesis efficiency without improving analytical rigor.

**Validation**: The system enforces this limit during experiment ingest. Frameworks exceeding 15KB will be rejected with specific guidance on reduction strategies.

### Evidence Optimization Notice

**System Behavior**: The analysis agent is optimized for synthesis efficiency and will automatically limit evidence to the strongest 1-2 quotes per dimension, regardless of framework requests for more extensive evidence collection.

**Framework Authors**: Design your evidence requirements around **quality over quantity**. Focus prompts on identifying the most demonstrative evidence rather than comprehensive evidence collection.

### Character Reduction Strategies

To maintain analytical depth within the 15KB limit:

**1. Streamline Linguistic Cues**
- Use concise dimension definitions (2-3 sentences maximum)
- Eliminate redundant explanatory text
- Focus on distinctive characteristics rather than comprehensive descriptions

**2. Optimize Prompt Structure**
- Combine related instructions into single paragraphs
- Use bullet points instead of verbose explanations
- Eliminate repetitive phrasing across dimensions

**3. Consolidate Examples**
- Provide 1-2 high-quality examples rather than multiple variations
- Focus on edge cases that clarify boundaries
- Remove obvious or intuitive examples

**4. Efficient Scoring Guidelines**
- Use standardized intensity/salience language across dimensions
- Avoid repeating general scoring principles for each dimension
- Reference common scoring criteria once at the framework level

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

### 5. Synthesis Efficiency

**Principle**: Framework design must balance analytical rigor with synthesis efficiency.

**In Practice**: Design evidence requirements that focus on the strongest, most demonstrative quotes rather than comprehensive evidence collection. The system will automatically optimize evidence volume for synthesis efficiency while maintaining analytical integrity.  

**Anti-Pattern**: Requesting extensive evidence collection that produces unnecessarily verbose outputs without improving analytical quality.

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

A framework file MUST be a standard Markdown (`.md`) file containing two distinct sections:

1.  **The Narrative (Human-Focused)**: The main body of the file. This section uses standard Markdown to explain the framework's theory, objectives, methodology, and references in clear, human-readable prose. It is the conceptual heart of the document.
2.  **The Appendix (Machine-Focused)**: A single, collapsible appendix at the end of the file that contains a single, unambiguous JSON object. This JSON block is the **single source of truth for execution** and MUST be the only machine-parsable configuration in the file.

### 2. The JSON Appendix: The Single Source of Truth

The appendix MUST begin with `<details><summary>Machine-Readable Configuration</summary>` and end with `</details>`. It MUST contain a single JSON code block that defines the execution contract.

#### Required JSON Schema

```json
{
  "name": "unique_framework_name",
  "version": "v4.0",
  "display_name": "Human-Readable Framework Name",
  "analysis_variants": {
    "default": {
      "description": "Complete implementation of the framework methodology",
      "analysis_prompt": "Your five-phase prompt that implements ALL methodology requirements from your documentation, including evidence requirements, confidence assessments, and reasoning explanations."
    },
    "descriptive_only": {
      "description": "Simplified version focusing on descriptive elements",
      "analysis_prompt": "Simplified prompt that still maintains coherence with your methodology."
    }
  },
  "calculation_spec": {
    "composite_score": "(0.25 * dimension_1) + (0.75 * dimension_2)"
  },
  "output_contract": {
    "schema": {
      "worldview": "string",
      "scores": "object",
      "evidence": "object",
      "confidence": "object",
      "reasoning": "object"
    },
    "instructions": "IMPORTANT: Your response MUST be a single, valid JSON object and nothing else. Do not include any text, explanations, or markdown code fences before or after the JSON object."
  }
}
```

**Component Explanations**:
*   **`name`, `version`, `display_name`**: Basic metadata for identification.
*   **`analysis_variants`**: A dictionary of prompts. A `default` key is required. This allows a single framework to support multiple analysis types.
*   **`calculation_spec`**: (Optional) A dictionary of formulas for the `CalculationAgent` to execute on the `scores` data.
*   **`output_contract`**: (Required) A formal definition of the expected JSON output from the `AnalysisAgent`'s LLM call.
    *   **`schema`**: Defines the required top-level keys and their expected data types.
    *   **`instructions`**: Provides a boilerplate instruction that MUST be appended to every `analysis_prompt` to ensure reliable, clean JSON output.

### 3. LLM Processing Optimization

When constructing your `analysis_prompt`, follow this five-phase approach, and remember to append the `output_contract.instructions` at the very end.

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
Return a single JSON object that conforms to the schema defined in the output_contract.
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

**The "Evidence Maximalism" Trap**:
- Requests for extensive evidence collection per dimension
- Verbose prompts that produce unnecessarily long responses
- **Result**: Analysis bloat that reduces synthesis efficiency without improving quality

**The "Character Bloat" Trap**:
- Overly detailed dimension definitions with redundant explanations
- Repetitive instructions across framework sections
- **Result**: Frameworks exceeding 15KB limit, rejected during ingest validation

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
ensuring the final output contains a valid JSON appendix with a clear 
output_contract.
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