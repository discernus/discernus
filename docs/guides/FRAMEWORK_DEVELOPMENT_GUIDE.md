```markdown
# Framework Development Guide: From Theory to Execution

**Version**: 2.0  
**Status**: Active

This guide provides a comprehensive workflow for researchers to translate their theoretical ideas into complete, execution-ready Discernus framework files (`framework.md`). The core principle is to use a powerful LLM (like Claude, Gemini, or ChatGPT) as a **Socratic partner and technical assistant**, allowing you to focus on the scholarship while the LLM handles the technical formatting.

---

## The "Narrative First" Philosophy

Our framework architecture is designed to put your research ideas first. You should **never** start by writing JSON or technical specifications. Instead, you begin by writing a clear, human-readable narrative that explains your framework. The machine-readable configuration is generated from this narrative in a later step.

### Your Goal as a Researcher

1.  **Develop a Clear Theory**: Articulate the core concepts, analytical dimensions, and methodological principles of your framework.
2.  **Explain It in Prose**: Write a high-quality narrative in the main body of your `framework.md`.
3.  **Use an LLM to Generate the Appendix**: Work collaboratively with an LLM to translate your narrative into the specific, machine-readable JSON appendix that the Discernus system requires.

This process ensures that the technical implementation is always driven by, and perfectly aligned with, your scholarly intent.

---

## Step 1: Write Your Narrative

Begin by creating a new `framework.md` file. In this file, start writing. Do not worry about formatting or code yet. Focus on answering these questions in clear prose:

*   **What is the name of your framework?** (e.g., "The Corporate Social Responsibility Framework")
*   **What is its core purpose?** (e.g., "To analyze corporate communications for authentic commitment versus 'greenwashing'.")
*   **What are the analytical dimensions (axes)?** (e.g., "Commitment vs. Compliance," "Transparency vs. Obfuscation.")
*   **How are these dimensions defined?** Provide clear, academic definitions for each one. What does a high score mean? What does a low score mean?
*   **What evidence should be used?** What kind of linguistic or rhetorical patterns should an analyst look for? Provide examples.

Your narrative should be rich enough that another researcher in your field could understand and apply your methodology just by reading it.

### Framework Design Principles

When developing your narrative, follow these core principles:

**Clear Analytical Dimensions**: Design 2-6 dimensions that are clearly distinct and measurable. Avoid overlapping dimensions, vague concepts, or unmeasurable abstractions.

**Measurable Language Indicators**: Specify concrete words, phrases, and patterns that indicate each dimension. Avoid subjective judgments, cultural assumptions, or undefined terms.

**Scalable Scoring Systems**: Use consistent scales that work across different text types. Recommended approaches:
- **Continuous**: 0.0-1.0 for most analytical dimensions
- **Categorical**: Clear categories with distinct criteria
- **Ordinal**: 1-5 or 1-7 with clear level descriptions

**Comprehensive Evidence Requirements**: Ensure multiple types of evidence support each dimension:
- **Lexical**: Specific words and phrases
- **Semantic**: Meaning patterns and concepts
- **Rhetorical**: Argument structures and persuasive techniques
- **Structural**: Text organization and formatting

### Domain-Specific Examples

Before writing your own framework, review these examples across different domains:

#### Academic Research: Literary Analysis Framework

```markdown
# Narrative Complexity Analysis Framework v1.0

## Framework Overview
**Purpose**: Analyze narrative sophistication and literary device usage in fictional works
**Domain**: Literary studies, comparative literature, creative writing analysis
**Scope**: Novels, short stories, poetry, dramatic works
**Analysis Unit**: Full text with paragraph-level granularity

## Theoretical Foundation
Based on narratology theory (Genette, Bal) and contemporary literary criticism, focusing on measurable textual features that correlate with narrative complexity.

## Analytical Dimensions

### Dimension 1: Structural Complexity
**What it measures**: Sophistication of narrative structure and temporal organization
**Scale**: 0.0-1.0 (continuous)
**Evidence types**: Narrative techniques, temporal markers, structural patterns

**Language indicators**:
- Time markers: "meanwhile," "earlier," "years later"
- Perspective shifts: "he thought," "from her perspective"
- Structural transitions: "in another place," "returning to"

**Scoring criteria**:
- **Low (0.0-0.3)**: Linear chronology, single perspective, conventional structure
- **Medium (0.4-0.6)**: Multiple perspectives or non-linear elements, moderate complexity
- **High (0.7-1.0)**: Complex temporal structure, multiple narrative layers, experimental form

### Dimension 2: Character Development
**What it measures**: Depth and sophistication of character portrayal
**Scale**: 0.0-1.0 (continuous)
**Evidence types**: Character description, dialogue, internal monologue

**Language indicators**:
- Internal states: "wondered," "felt conflicted," "realized"
- Character growth: "had changed," "no longer believed," "understood now"
- Relationship dynamics: "between them," "her attitude toward," "his perception of"

**Scoring criteria**:
- **Low (0.0-0.3)**: Static characters, minimal development, functional roles
- **Medium (0.4-0.6)**: Some character growth, moderate psychological depth
- **High (0.7-1.0)**: Complex character arcs, psychological nuance, dynamic relationships
```

#### Business Intelligence: Brand Sentiment Framework

```markdown
# Customer Communication Sentiment Analysis Framework v1.0

## Framework Overview
**Purpose**: Analyze customer sentiment and brand perception in communication channels
**Domain**: Corporate communications, brand management, customer service
**Scope**: Customer reviews, social media posts, support tickets, survey responses
**Analysis Unit**: Individual messages or posts

## Theoretical Foundation
Combines sentiment analysis theory with brand perception psychology, focusing on actionable insights for business decision-making.

## Analytical Dimensions

### Dimension 1: Emotional Valence
**What it measures**: Overall positive/negative sentiment toward brand
**Scale**: -1.0 to 1.0 (negative to positive)
**Evidence types**: Evaluative language, emotional expressions, satisfaction indicators

**Language indicators**:
- Positive: "love," "excellent," "exceeded expectations," "recommend"
- Negative: "disappointed," "terrible," "waste of money," "avoid"
- Neutral: "okay," "average," "as expected," "decent"

**Scoring criteria**:
- **Negative (-1.0 to -0.3)**: Clear dissatisfaction, complaints, criticism
- **Neutral (-0.2 to 0.2)**: Balanced or factual comments, mixed opinions
- **Positive (0.3 to 1.0)**: Satisfaction, praise, recommendations

### Dimension 2: Purchase Intent
**What it measures**: Likelihood of future purchase or recommendation
**Scale**: 0.0-1.0 (unlikely to very likely)
**Evidence types**: Behavioral indicators, future-oriented language, recommendation statements

**Language indicators**:
- High intent: "will buy again," "recommend to friends," "my go-to brand"
- Medium intent: "might consider," "depends on," "worth trying"
- Low intent: "never again," "look elsewhere," "not worth it"

**Scoring criteria**:
- **Low (0.0-0.3)**: Unlikely to purchase, negative recommendations
- **Medium (0.4-0.6)**: Neutral or conditional purchase likelihood
- **High (0.7-1.0)**: Strong purchase intent, positive recommendations
```

#### Journalism: Source Credibility Framework

```markdown
# News Source Credibility Assessment Framework v1.0

## Framework Overview
**Purpose**: Evaluate credibility indicators in news sources and media content
**Domain**: Journalism, media studies, fact-checking, editorial review
**Scope**: News articles, press releases, editorial content, opinion pieces
**Analysis Unit**: Individual articles or content pieces

## Theoretical Foundation
Based on journalism ethics and media literacy research, focusing on verifiable credibility indicators rather than subjective bias assessment.

## Analytical Dimensions

### Dimension 1: Source Attribution
**What it measures**: Quality and transparency of source citation
**Scale**: 0.0-1.0 (poor to excellent attribution)
**Evidence types**: Citation patterns, source identification, verification methods

**Language indicators**:
- Strong attribution: "according to [specific official]," "data from [institution]," "confirmed by [authority]"
- Weak attribution: "sources say," "it is believed," "reportedly"
- Anonymous sources: "anonymous official," "source close to," "speaking on condition"

**Scoring criteria**:
- **Low (0.0-0.3)**: Unclear sources, unverified claims, heavy reliance on anonymous sources
- **Medium (0.4-0.6)**: Mixed attribution quality, some verification, moderate transparency
- **High (0.7-1.0)**: Clear source identification, verification methods, transparent attribution

### Dimension 2: Evidence Quality
**What it measures**: Strength and reliability of supporting evidence
**Scale**: 0.0-1.0 (weak to strong evidence)
**Evidence types**: Data citations, expert quotes, documentation references

**Language indicators**:
- Strong evidence: "data shows," "research indicates," "documented in," "verified by"
- Moderate evidence: "suggests," "appears to," "may indicate," "some evidence"
- Weak evidence: "allegedly," "rumored," "believed to be," "unconfirmed"

**Scoring criteria**:
- **Low (0.0-0.3)**: Unsupported claims, weak evidence, speculation
- **Medium (0.4-0.6)**: Some supporting evidence, moderate verification
- **High (0.7-1.0)**: Strong documentary evidence, expert verification, data support
```

#### Policy Research: Implementation Feasibility Framework

```markdown
# Policy Implementation Feasibility Framework v1.0

## Framework Overview
**Purpose**: Assess policy proposals for practical implementation challenges and opportunities
**Domain**: Policy research, government analysis, institutional planning
**Scope**: Legislative proposals, policy briefs, regulatory documents, implementation plans
**Analysis Unit**: Policy documents or document sections

## Theoretical Foundation
Based on implementation science and policy analysis theory, focusing on predictive indicators of policy success or failure.

## Analytical Dimensions

### Dimension 1: Resource Requirements
**What it measures**: Financial, human, and institutional resources needed
**Scale**: 1-5 (minimal to extensive resources)
**Evidence types**: Budget references, staffing implications, infrastructure needs

**Language indicators**:
- High requirements: "significant investment," "additional staffing," "new infrastructure"
- Medium requirements: "moderate funding," "existing resources," "some training"
- Low requirements: "minimal cost," "current capacity," "no additional"

**Scoring criteria**:
- **Low (1-2)**: Minimal additional resources, uses existing capacity
- **Medium (3)**: Moderate resource requirements, some new investment
- **High (4-5)**: Extensive resources, significant infrastructure changes

### Dimension 2: Stakeholder Alignment
**What it measures**: Degree of stakeholder support and resistance
**Scale**: 0.0-1.0 (high resistance to strong support)
**Evidence types**: Stakeholder references, coalition building, opposition indicators

**Language indicators**:
- Strong support: "broad consensus," "stakeholder agreement," "coalition backing"
- Mixed support: "some opposition," "divided opinions," "requires negotiation"
- Strong opposition: "significant resistance," "widespread objection," "contentious"

**Scoring criteria**:
- **Low (0.0-0.3)**: Strong stakeholder resistance, limited support
- **Medium (0.4-0.6)**: Mixed stakeholder reactions, moderate support
- **High (0.7-1.0)**: Strong stakeholder alignment, broad support
```

### Multi-Scale Analysis Support

Consider how your framework applies across different text levels:

**Document Level**: Overall themes and patterns across the entire text
**Paragraph Level**: Specific arguments and evidence within sections
**Sentence Level**: Linguistic features and sentiment in individual statements
**Phrase Level**: Specific terminology and conceptual markers

Your framework should specify which level(s) of analysis are most appropriate for each dimension.

---

## Step 2: Use an LLM to Generate the JSON Appendix

Now, you will use this narrative to create the machine-readable appendix through collaborative dialogue with an LLM.

### 2.1. The Meta-Prompt

Open your preferred LLM chatbot (Claude, Gemini, ChatGPT, etc.) and use the following "meta-prompt." A meta-prompt is a prompt that tells the LLM how to behave and what its role is.

**The Framework Generation Meta-Prompt:**

```
You are a specialist in computational social science and an expert in the Discernus research platform. Your task is to help me create a machine-readable JSON configuration for a new analytical framework I have designed.

First, I will provide you with the Discernus Framework Specification (v4.0). This document defines the exact JSON structure you must produce.

Second, I will provide you with the narrative of my new framework, which explains its theory and methodology.

Your job is to read both documents carefully and then generate a single, valid JSON object that correctly implements my narrative according to the strict requirements of the specification. You must ask me clarifying questions if my narrative is ambiguous or incomplete to ensure the final JSON is perfect.
```

### 2.2. The Collaborative Process

1.  **Provide the Specification**: Copy the entire content of the Framework Specification and paste it into the chat. The LLM now knows the rules.
2.  **Provide Your Narrative**: Copy the narrative you wrote in Step 1 and paste it into the chat. The LLM now knows your intent.
3.  **Iterate and Refine**: The LLM will now likely ask you clarifying questions.
    *   "Your 'Transparency' dimension is well-defined, but what specific linguistic markers should I include in the prompt for it?"
    *   "You've mentioned a 'Greenwashing Index.' Could you provide the exact formula for the `calculation_spec`?"
    *   "The specification requires an `output_contract`. What specific keys and data types should the final JSON contain?"

    Work with the LLM to answer these questions. This collaborative process ensures that your theoretical ideas are translated into precise, executable instructions.

4.  **Receive the Final JSON**: Once the LLM has all the information it needs, it will generate the complete JSON appendix for you.

### 2.3. Validation Through Dialogue

During your LLM dialogue, test your framework with validation cases to ensure quality and consistency:

**Validation Questions to Ask Your LLM**:
- "Here's a sample text from my domain. What scores would this framework produce and why?"
- "What evidence would support a high score on Dimension 1 versus a low score?"
- "How would this framework handle edge cases or ambiguous texts in my domain?"
- "Can you generate a few test cases with expected results for validation?"

**Quality Assurance Dialogue**:
Use your LLM conversation to verify:
- [ ] Each dimension has clear, distinct conceptual boundaries
- [ ] Language indicators are comprehensive and specific to your domain
- [ ] Scoring criteria are consistent and applicable across different texts
- [ ] Evidence requirements are realistic and achievable
- [ ] The framework captures the theoretical concepts you intended

**Common Clarification Areas**:
- **Scoring Scale Boundaries**: "When exactly does a score move from 0.4 to 0.5?"
- **Evidence Prioritization**: "Which types of evidence are most important when they conflict?"
- **Edge Case Handling**: "What happens when a text shows mixed or contradictory signals?"
- **Domain Specificity**: "How should this framework adapt to different sub-domains?"

### 2.4. ⚠️ CRITICAL: Output Contract Schema Requirements

**🚨 The `output_contract.schema` is NOT optional for production use:**

```json
{
  "output_contract": {
    "schema": {
      "worldview": "string",
      "sentiment_score": "number",
      "toxicity_level": "number", 
      "readability_index": "number",
      "evidence_quotes": "array",
      "confidence_rating": "number"
    }
  }
}
```

**Why Schema Is Critical:**
- **Framework Agnostic Processing**: Without schema, your framework gets CFF-style field names as fallback
- **Exact Field Names**: The system generates exactly the field names you specify
- **Data Type Preservation**: Ensures strings, numbers, arrays, and objects are handled correctly
- **Downstream Compatibility**: CalculationAgent and SynthesisAgent rely on predictable field names

**✅ Framework Naming Freedom:**
- Use ANY field names you want: `"sentiment_score"`, `"toxicity_level"`, `"readability_index"`
- The system adapts to YOUR naming conventions
- No hardcoded assumptions about field meanings

**✅ Supported Data Types:**
- `"string"`: Text values like worldview classifications
- `"number"`: Numeric scores, confidence ratings, indices
- `"array"`: Evidence quotes, supporting examples, keyword lists
- `"object"`: Nested data structures for complex frameworks

**❌ What Happens Without Schema:**
```json
// Your framework produces: {"sentiment_analysis": {"positive": 0.8}}
// Without schema: Gets transformed to "tribal_dominance_score" (CFF fallback)
// With schema: Gets transformed to "sentiment_score" (your specification)
```

**🎯 Best Practice:**
Always include a complete schema that matches your analysis prompt's expected output. Every field your LLM generates should be defined in the schema.

---

## Framework Quality Standards

### Evidence Collection Standards

Your framework should specify multiple types of evidence to ensure robust analysis:

**Evidence Type Categories**:
- **Lexical**: Specific words and phrases that directly indicate dimensional concepts
- **Semantic**: Meaning patterns and conceptual relationships that suggest dimensional presence
- **Rhetorical**: Argument structures, persuasive techniques, and discourse strategies
- **Structural**: Text organization, formatting, and architectural elements

**Evidence Quality Guidelines**:
- **Specific Examples**: Provide concrete examples rather than abstract categories
- **Contextual Sensitivity**: Consider how evidence might vary across different text types
- **Cultural Adaptation**: Account for how evidence might differ across cultural contexts
- **Temporal Stability**: Ensure evidence indicators remain valid over time

### Test Case Development

Create validation examples with your LLM to ensure framework reliability:

**Test Case Template**:
```markdown
### Test Case 1: [Descriptive Name]
**Domain Context**: [Specific area or type of text]
**Input Text**: [Sample text from your domain]
**Expected Dimensional Scores**: 
- Dimension 1: [Score] (Confidence: [Level])
- Dimension 2: [Score] (Confidence: [Level])
**Evidence Summary**: [Key evidence supporting each score]
**Edge Cases**: [How framework handles ambiguous elements]
**Rationale**: [Explanation of scoring reasoning]
```

**Validation Categories**:
- **Typical Cases**: Standard examples that clearly demonstrate each dimension
- **Edge Cases**: Ambiguous or boundary examples that test framework limits
- **Conflicting Evidence**: Texts with mixed signals across dimensions
- **Domain Variations**: Examples from different sub-areas within your domain

### Reproducibility Standards

Ensure your framework enables independent replication:

**Documentation Requirements**:
- **Decision Criteria**: Explicit rules for all analytical decisions
- **Boundary Conditions**: Clear guidance for ambiguous or difficult texts
- **Confidence Assessment**: Standards for evaluating certainty in scores
- **Quality Thresholds**: Minimum evidence requirements for reliable analysis

**Consistency Checks**:
- **Inter-rater Reliability**: Framework should produce similar results across different analysts
- **Temporal Stability**: Results should be consistent when applied to the same text over time
- **Domain Transferability**: Clear guidance on how framework applies to related domains
- **Scale Reliability**: Scoring criteria should work consistently across different text lengths

---

## Step 3: Assemble Your Framework File

You are now ready to assemble the final `framework.md`.

1.  **Paste Your Narrative**: The main body of the file is the narrative you wrote in Step 1.
2.  **Create the Appendix**: At the very end of the file, add the collapsible appendix structure:
    ```markdown
    <details>
    <summary>Machine-Readable Configuration</summary>
    
    </details>
    ```
3.  **Paste the JSON**: Inside the `<details>` block, create a JSON code block and paste the final JSON object you generated with the LLM in Step 2.

    ```markdown
    <details>
    <summary>Machine-Readable Configuration</summary>
    
    ```json
    {
      "name": "your_framework_name",
      "version": "1.0",
      ...
    }
    ```
    
    </details>
    ```

### You're Done!

You have now created a complete, self-contained, and execution-ready Discernus framework. It contains both the rich scholarly context needed for human understanding and the precise, machine-readable instructions needed for reliable automated analysis.

---

## Advanced Framework Features

### Temporal Analysis Capabilities

Enable tracking changes over time by designing your framework to support:

**Time Period Segmentation**: Analyze texts by date ranges to identify trends
**Change Point Detection**: Identify significant shifts in dimensional patterns
**Longitudinal Comparison**: Compare same sources across different time periods
**Trend Analysis**: Track gradual changes in dimensional emphasis over time

**Implementation Approach**: Include temporal markers in your language indicators and design scoring criteria that can detect change over time.

### Comparative Analysis Support

Design your framework to support comparison across different contexts:

**Cross-Source Comparison**: Compare different authors, publications, or organizations
**Cross-Genre Analysis**: Apply same framework to different text types within your domain
**Cross-Cultural Application**: Adapt framework for different cultural contexts
**Cross-Linguistic Support**: Guidelines for translation and adaptation

**Implementation Approach**: Ensure your dimensional definitions and evidence criteria are robust enough to work across different comparative contexts.

### Multi-Dimensional Integration

Consider how your dimensions interact and influence each other:

**Dimensional Correlation**: Expect and account for relationships between dimensions
**Composite Scoring**: Develop methods for combining dimensional scores meaningfully
**Pattern Recognition**: Identify common combinations of dimensional scores
**Emergent Properties**: Recognize when dimensional combinations create new analytical insights

**Implementation Approach**: Work with your LLM to develop calculation specifications that capture these interactions appropriately.

---

## Framework Maintenance and Evolution

### Version Control Best Practices

Maintain clear documentation of framework changes:

```markdown
## Version History
### v1.2 (2025-01-15)
- Added dimension 3: Stakeholder Analysis
- Refined scoring criteria for dimensions 1-2 based on validation testing
- Updated language indicators based on pilot study results
- Improved reproducibility documentation

### v1.1 (2025-01-10)
- Fixed scoring consistency issues identified in peer review
- Added more specific language indicators for edge cases
- Improved clarity of evidence requirements
- Enhanced test case documentation

### v1.0 (2025-01-05)
- Initial framework release
- Two-dimensional analysis: Resource Requirements and Stakeholder Alignment
- Pilot tested on 50 policy documents
- Validation results: 85% inter-rater reliability
```

### Continuous Improvement Process

**Regular Validation**: Periodically test your framework on new texts to ensure continued reliability
**User Feedback**: Collect feedback from other researchers who apply your framework
**Domain Evolution**: Update language indicators and evidence criteria as your domain evolves
**Technical Updates**: Maintain compatibility with evolving Discernus specifications

### Community Contribution

**Sharing Best Practices**: Document lessons learned and share with the research community
**Collaborative Development**: Work with other researchers to improve and extend your framework
**Cross-Domain Adaptation**: Help others adapt your framework to related domains
**Methodological Innovation**: Contribute to advancing computational social science methodology

---

## Troubleshooting Common Issues

### Framework Too Vague

**Problem**: Dimensions are unclear or unmeasurable
```markdown
# BAD: Vague dimension
### Dimension: Quality
**What it measures**: How good the text is
**Scale**: Low to High
```

**Solution**: Provide specific, measurable concepts
```markdown
# GOOD: Specific dimension
### Dimension: Argument Strength
**What it measures**: Logical coherence and evidence quality in persuasive arguments
**Scale**: 0.0-1.0 (weak to strong argumentation)
**Evidence types**: Logical connectors, evidence citations, reasoning patterns
```

### Missing Language Indicators

**Problem**: No specific examples of relevant language
```markdown
# BAD: No specific indicators
**Language indicators**: Look for positive and negative words
```

**Solution**: Provide concrete examples
```markdown
# GOOD: Specific indicators
**Language indicators**:
- Positive evaluation: "excellent," "outstanding," "superior," "impressive"
- Negative evaluation: "poor," "inadequate," "disappointing," "substandard"
- Comparative language: "better than," "worse than," "compared to," "in contrast"
```

### Unclear Scoring Criteria

**Problem**: Vague scoring boundaries
```markdown
# BAD: Vague criteria
- Low: Not very good
- High: Really good
```

**Solution**: Clear, specific criteria
```markdown
# GOOD: Clear criteria
- **Low (0.0-0.3)**: Minimal evidence cited, logical gaps present, unsupported claims
- **Medium (0.4-0.6)**: Some evidence provided, mostly logical, few unsupported claims
- **High (0.7-1.0)**: Strong evidence throughout, logical consistency, well-supported claims
```

### Inconsistent Evidence Requirements

**Problem**: Different standards for different dimensions
**Solution**: Establish consistent evidence requirements across all dimensions, adjusting only for dimension-specific needs

### Overlapping Dimensions

**Problem**: Dimensions measure similar concepts
**Solution**: Clearly differentiate dimensions and test for independence through validation cases

---

## Getting Started Checklist

### Before You Begin
- [ ] Identify your specific domain and research questions
- [ ] Review existing frameworks in your field for gaps and opportunities
- [ ] Collect sample texts that represent your domain
- [ ] Clarify your theoretical foundation and analytical goals

### During Development
- [ ] Write clear narrative explaining your framework
- [ ] Define 2-6 distinct, measurable dimensions
- [ ] Provide specific language indicators for each dimension
- [ ] Create comprehensive test cases for validation
- [ ] Use LLM dialogue to refine and improve framework

### Before Deployment
- [ ] Test framework on diverse sample texts
- [ ] Verify reproducibility across different analysts
- [ ] Document edge cases and boundary conditions
- [ ] Establish quality standards and confidence thresholds
- [ ] Create user documentation and examples

### After Implementation
- [ ] Monitor framework performance on new texts
- [ ] Collect user feedback and identify improvement opportunities
- [ ] Update language indicators and evidence criteria as needed
- [ ] Maintain version control and change documentation
- [ ] Contribute to community knowledge and best practices

---

## Conclusion

This comprehensive guide enables you to create analytical frameworks that amplify human intelligence through computational assistance. By following the narrative-first philosophy and using LLM collaboration, you can develop sophisticated analytical tools that maintain scholarly rigor while enabling large-scale analysis.

**Success Indicator**: Your framework should enable researchers to say "This analysis approach makes sense, captures important insights, and I can replicate it" - creating reliable, valid, and useful research instruments for computational social science.

The goal is not to replace human analytical judgment but to systematize and scale it, making sophisticated analysis accessible to researchers across disciplines while maintaining the highest standards of scholarly rigor.

---

*This guide supports the creation of frameworks that enable mathematical reliability, cost transparency, and complete reproducibility - the three foundational commitments of computational social science research.*