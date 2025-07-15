# Framework Integration Guide
*Create Analytical Frameworks for Discernus*

This guide shows you how to create analytical frameworks that work seamlessly with Discernus. Whether you're analyzing political discourse, literary texts, corporate communications, or any other domain, this guide provides practical patterns and examples.

## Three Foundational Commitments Integration

Your framework must support Discernus's three foundational commitments:

- **Mathematical Reliability**: Frameworks must enable LLMs to design analysis, secure code to execute calculations, and LLMs to interpret results
- **Cost Transparency**: Frameworks must provide clear guidance for upfront cost estimation and efficient analysis
- **Complete Reproducibility**: Frameworks must enable zero mystery - every analytical step documented for independent replication

## Quick Start: Framework Template

```markdown
# [Your Framework Name] v[Version]

## Framework Overview
**Purpose**: [What this framework analyzes and why]
**Domain**: [Academic research, corporate analysis, journalism, etc.]
**Scope**: [Types of texts this applies to]
**Analysis Unit**: [Sentences, paragraphs, documents, etc.]

## Theoretical Foundation
[Academic or practical basis for your framework]

## Analytical Dimensions

### Dimension 1: [Name]
**What it measures**: [Clear description]
**Scale**: 0.0-1.0 (or categorical, or other scale)
**Evidence types**: Lexical, semantic, rhetorical patterns

**Language indicators**:
- Specific words: [examples]
- Phrases: [examples]
- Semantic patterns: [examples]

**Scoring criteria**:
- **Low (0.0-0.3)**: [Description with examples]
- **Medium (0.4-0.6)**: [Description with examples]  
- **High (0.7-1.0)**: [Description with examples]

### Dimension 2: [Name]
[Same structure as Dimension 1]

## Output Requirements
**Quantitative**: Numerical scores for each dimension
**Qualitative**: Evidence citations and reasoning
**Confidence**: Uncertainty assessment for each score
**Synthesis**: Overall interpretation and conclusions
```

## Domain-Specific Examples

### Academic Research: Literary Analysis Framework

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

## Output Requirements
**Quantitative**: Scores for structural complexity and character development
**Qualitative**: Text evidence with citations, explanation of scoring rationale
**Confidence**: Assessment of analysis certainty based on text clarity
**Synthesis**: Overall evaluation of narrative sophistication
```

### Corporate Communications: Brand Sentiment Framework

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

## Output Requirements
**Quantitative**: Valence and intent scores with confidence intervals
**Qualitative**: Key themes, representative quotes, sentiment trends
**Confidence**: Statistical significance based on sample size
**Synthesis**: Strategic recommendations for brand management
```

### Journalism: Source Credibility Framework

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

## Output Requirements
**Quantitative**: Attribution and evidence quality scores
**Qualitative**: Credibility strengths and weaknesses, improvement recommendations
**Confidence**: Assessment reliability based on content clarity
**Synthesis**: Overall credibility evaluation with specific recommendations
```

### Think Tank Research: Policy Analysis Framework

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

## Output Requirements
**Quantitative**: Resource and alignment scores with uncertainty ranges
**Qualitative**: Implementation challenges, stakeholder analysis, timeline assessment
**Confidence**: Prediction reliability based on policy specificity
**Synthesis**: Feasibility assessment with strategic recommendations
```

## Framework Design Principles

### 1. Clear Analytical Dimensions
**Best Practice**: 2-6 dimensions that are clearly distinct and measurable
**Avoid**: Overlapping dimensions, vague concepts, unmeasurable abstractions

**Example Structure**:
```markdown
### Dimension: [Clear Name]
**What it measures**: [Specific, measurable concept]
**Scale**: [Well-defined scale with anchors]
**Evidence types**: [Specific textual features to look for]
**Language indicators**: [Concrete examples of relevant language]
**Scoring criteria**: [Clear descriptions for each score level]
```

### 2. Measurable Language Indicators
**Best Practice**: Specific words, phrases, and patterns that indicate each dimension
**Avoid**: Subjective judgments, cultural assumptions, undefined terms

**Good Examples**:
- "Statistical terms: 'correlation,' 'significance,' 'confidence interval'"
- "Temporal markers: 'before,' 'after,' 'during,' 'meanwhile'"
- "Certainty language: 'definitely,' 'probably,' 'possibly,' 'uncertain'"

### 3. Scalable Scoring Systems
**Best Practice**: Consistent scales that work across different text types
**Avoid**: Arbitrary scales, inconsistent anchors, unclear boundaries

**Recommended Scales**:
- **Continuous**: 0.0-1.0 for most analytical dimensions
- **Categorical**: Clear categories with distinct criteria
- **Ordinal**: 1-5 or 1-7 with clear level descriptions

### 4. Comprehensive Evidence Requirements
**Best Practice**: Multiple types of evidence support each dimension
**Avoid**: Single indicators, brittle detection methods

**Evidence Types**:
- **Lexical**: Specific words and phrases
- **Semantic**: Meaning patterns and concepts
- **Rhetorical**: Argument structures and persuasive techniques
- **Structural**: Text organization and formatting

## Technical Implementation

### Mathematical Reliability Integration
Your framework must support the hybrid intelligence pattern:

```markdown
## Calculation Instructions
**LLM Design Phase**: Apply framework to text using natural language reasoning
**Secure Code Execution**: Calculate statistics, confidence intervals, correlations
**LLM Interpretation Phase**: Translate numerical results into actionable insights

**Example Code Block**:
```python
# LLM will generate analysis code like this:
import numpy as np
import pandas as pd

# Process dimension scores
scores = [0.7, 0.8, 0.6, 0.9, 0.5]  # From framework analysis
mean_score = np.mean(scores)
std_dev = np.std(scores)
confidence_interval = np.percentile(scores, [25, 75])

# Store results for LLM interpretation
result_data = {
    'mean_score': mean_score,
    'std_dev': std_dev,
    'confidence_interval': confidence_interval,
    'sample_size': len(scores)
}
```

### Cost Transparency Requirements
Your framework must enable accurate cost estimation:

```markdown
## Cost Estimation Factors
**Token Complexity**: Estimated tokens per text based on analysis depth
**Model Requirements**: Specify minimum model capabilities needed
**Batch Processing**: Guidance for efficient corpus processing
**Quality Thresholds**: Trade-offs between cost and analysis quality

**Example Estimation**:
- Simple framework: ~500 tokens per text
- Complex framework: ~1500 tokens per text
- Statistical analysis: ~200 tokens per corpus
- Interpretation: ~300 tokens per result set
```

### Complete Reproducibility Standards
Your framework must enable independent replication:

```markdown
## Reproducibility Requirements
**Version Control**: Framework version and change history
**Decision Criteria**: Explicit rules for all analytical decisions
**Edge Cases**: Guidance for ambiguous or difficult texts
**Validation Data**: Example analyses with expected results

**Example Validation**:
```markdown
### Test Case 1: [Description]
**Input Text**: [Sample text]
**Expected Dimension 1 Score**: 0.7 (± 0.1)
**Expected Dimension 2 Score**: 0.4 (± 0.1)
**Rationale**: [Explanation of scoring reasoning]
```

## Framework Validation Process

### Self-Validation Checklist
Before submitting your framework, verify:

- [ ] **Clear purpose and scope** defined
- [ ] **2-6 analytical dimensions** with distinct concepts
- [ ] **Measurable language indicators** for each dimension
- [ ] **Consistent scoring criteria** across dimensions
- [ ] **Multiple evidence types** per dimension
- [ ] **Practical application examples** included
- [ ] **Calculation instructions** for mathematical reliability
- [ ] **Cost estimation guidance** provided
- [ ] **Reproducibility standards** met

### Automated Validation
Discernus validates your framework automatically:

```bash
# Framework validation command
python3 -c "
from discernus.agents.validation_agent import ValidationAgent
agent = ValidationAgent()
result = agent.validate_framework_only('path/to/your/framework.md')
print(f'Validation result: {result[\"status\"]}')
print(f'Completeness: {result[\"completeness_percentage\"]}%')
if result['issues']:
    print('Issues to address:')
    for issue in result['issues']:
        print(f'- {issue}')
"
```

### Common Validation Issues

**Framework Too Vague**:
```markdown
# BAD: Vague dimension
### Dimension: Quality
**What it measures**: How good the text is
**Scale**: Low to High
```

```markdown
# GOOD: Specific dimension
### Dimension: Argument Strength
**What it measures**: Logical coherence and evidence quality in persuasive arguments
**Scale**: 0.0-1.0 (weak to strong argumentation)
**Evidence types**: Logical connectors, evidence citations, reasoning patterns
```

**Missing Language Indicators**:
```markdown
# BAD: No specific indicators
**Language indicators**: Look for positive and negative words
```

```markdown
# GOOD: Specific indicators
**Language indicators**:
- Positive evaluation: "excellent," "outstanding," "superior," "impressive"
- Negative evaluation: "poor," "inadequate," "disappointing," "substandard"
- Comparative language: "better than," "worse than," "compared to," "in contrast"
```

**Unclear Scoring Criteria**:
```markdown
# BAD: Vague criteria
- Low: Not very good
- High: Really good
```

```markdown
# GOOD: Clear criteria
- **Low (0.0-0.3)**: Minimal evidence cited, logical gaps present, unsupported claims
- **Medium (0.4-0.6)**: Some evidence provided, mostly logical, few unsupported claims
- **High (0.7-1.0)**: Strong evidence throughout, logical consistency, well-supported claims
```

## Advanced Framework Features

### Multi-Scale Analysis
Support analysis at different text levels:

```markdown
## Multi-Scale Analysis Support
**Document Level**: Overall themes and patterns
**Paragraph Level**: Specific arguments and evidence
**Sentence Level**: Linguistic features and sentiment
**Phrase Level**: Specific terminology and concepts
```

### Temporal Analysis
Enable tracking changes over time:

```markdown
## Temporal Analysis Capabilities
**Time Period Segmentation**: Analyze texts by date ranges
**Trend Detection**: Identify patterns over time
**Change Point Analysis**: Detect significant shifts
**Longitudinal Comparison**: Compare same sources across time
```

### Comparative Analysis
Support comparison across different text types:

```markdown
## Comparative Analysis Features
**Cross-Source Comparison**: Compare different authors, publications, organizations
**Cross-Genre Analysis**: Apply same framework to different text types
**Cross-Cultural Application**: Adapt framework for different cultural contexts
**Cross-Linguistic Support**: Guidelines for translation and adaptation
```

## Framework Publishing and Sharing

### Documentation Standards
Complete framework documentation includes:

```markdown
## Framework Package Contents
├── framework.md                 # Main framework specification
├── validation_examples.md       # Test cases and expected results
├── implementation_guide.md      # Practical application instructions
├── theoretical_background.md    # Academic foundation and citations
├── cost_analysis.md            # Resource requirements and estimation
└── version_history.md          # Change log and updates
```

### Version Control
Maintain clear version history:

```markdown
## Version History
### v1.2 (2025-01-15)
- Added dimension 3: Stakeholder Analysis
- Refined scoring criteria for dimensions 1-2
- Updated language indicators based on pilot testing

### v1.1 (2025-01-10)
- Fixed scoring consistency issues
- Added more specific language indicators
- Improved reproducibility documentation

### v1.0 (2025-01-05)
- Initial framework release
- Two-dimensional analysis: Resource Requirements and Stakeholder Alignment
- Pilot tested on 50 policy documents
```

### Community Contributions
Guidelines for framework improvement:

```markdown
## Community Contribution Guidelines
**Bug Reports**: Issues with framework application or unclear guidance
**Enhancement Requests**: Suggestions for additional dimensions or improvements
**Validation Results**: Share results from applying framework to new domains
**Adaptation Guidelines**: How to modify framework for specific use cases

**Contribution Process**:
1. Test framework on your domain/corpus
2. Document issues or improvements needed
3. Submit detailed feedback with examples
4. Collaborate on framework updates
5. Validate improvements with test cases
```

## Getting Started

### 1. Choose Your Domain
Identify the specific area you want to analyze:
- Academic research questions
- Business intelligence needs
- Journalistic analysis requirements
- Policy evaluation criteria

### 2. Define Your Dimensions
Start with 2-3 clear, measurable concepts:
- What specific aspects matter in your domain?
- How can they be measured objectively?
- What evidence would support each measurement?

### 3. Create Language Indicators
Develop specific examples of relevant language:
- Collect sample texts from your domain
- Identify patterns that indicate each dimension
- Create comprehensive lists of indicators

### 4. Test and Validate
Apply your framework to sample texts:
- Verify that scoring criteria work consistently
- Check that language indicators are comprehensive
- Ensure reproducibility across different users

### 5. Integrate with Discernus
Validate your framework for platform compatibility:
- Run automated validation checks
- Test cost estimation accuracy
- Verify reproducibility standards

**Success Indicator**: Your framework should enable researchers to say "This analysis approach makes sense and I can replicate it" - amplifying human analytical intelligence through computational assistance.

---

*This guide enables creation of frameworks that support Discernus's three foundational commitments: Mathematical Reliability, Cost Transparency, and Complete Reproducibility. The result is domain-neutral analytical capabilities that serve researchers, analysts, and organizations across disciplines.* 