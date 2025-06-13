#Prompt Engineering Strategy - Hierarchical Theme Detection

11 June 2025

## Situation Analysis: Current State Assessment

### **Current Prompt Architecture**

The existing Civic Virtue Framework prompt instructs LLMs to "assess each well independently on a 0.0-1.0 scale based on conceptual strength," focusing on "how strongly each orientation shapes the narrative's structure." This approach treats all wells as potentially relevant and allows for distributed scoring across multiple dimensions.

### **Observed Failure Patterns**

**Flat Score Distributions**: Real-world narratives consistently produce moderate scores (0.3-0.7) across multiple wells rather than sharp hierarchical distinctions. Trump's Joint Session Address exemplifies this: dominant themes (Tribalism 0.8, Fantasy 0.8) coexist with substantial scores for competing wells (Hope 0.52, Justice 0.38).

**Synthetic Validation Failures**: Even engineered texts designed for maximum extremity (synthetic positive/negative narratives) fail to produce truly polarized scores. The "perfect positive" synthetic achieved Dignity 0.7, Truth 0.9, Justice 0.8 rather than approaching 1.0, while disintegrative wells scored 0.1-0.2 rather than true zeros.

**Missing Hierarchy Signal**: Current prompts provide no mechanism for LLMs to express that one theme overwhelmingly dominates while others are peripheral noise. The scoring treats a narrative driven 80% by Tribalism identically to one where Tribalism is merely present alongside other themes.

### **Root Cause Analysis**

**Prompt Psychology**: LLMs trained on balanced, nuanced human feedback tend toward moderate, "reasonable" responses unless explicitly forced toward extremes. The current prompt rewards comprehensive analysis over hierarchical clarity.

**Conceptual vs. Relative Assessment**: Asking "how present is this theme?" yields different responses than "what are the top driving forces and how do they rank?" The former allows for multiple moderate scores; the latter demands hierarchical thinking.

**Evidence Requirements**: Current prompts don't require textual evidence for scores, allowing LLMs to rely on impressionistic rather than grounded assessment.

## Strategic Redesign Framework

### **Core Principle Shift: From Presence to Dominance**

Transform the analytical task from "detect all themes" to "identify the hierarchy of driving forces." This fundamental reframing should produce sharper, more defensible results.

### **Three-Stage Prompt Architecture**

**Stage 1: Thematic Ranking**

- Require identification of top 2-3 dominant wells
- Force rank ordering with explicit justification
- Establish that only truly central themes qualify for "dominant" status

**Stage 2: Relative Weighting**

- Assign percentage weights to dominant themes (must sum to 80-100%)
- Remaining wells receive residual weighting (0-20% total)
- Create mathematical forcing function for hierarchy

**Stage 3: Evidence Grounding**

- Mandate specific text excerpts for all wells scoring >0.3
- Require explanation of why minor themes are truly minor
- Build accountability for scoring decisions


### **Specific Prompt Template**

```
**TASK: Hierarchical Thematic Analysis**

**STAGE 1 - IDENTIFY DOMINANT THEMES**
After reading this narrative, identify the 2-3 themes that most fundamentally shape its moral architecture. These should be forces that, if removed, would fundamentally alter the narrative's character.

Rank your selections 1-3 and provide one-sentence justification for each.

**STAGE 2 - ASSIGN RELATIVE WEIGHTS**
Distribute 100 percentage points across ALL ten wells, with the following constraints:
- Your top-ranked theme must receive 40-60% 
- Your second-ranked theme must receive 20-40%
- Your third-ranked theme (if any) must receive 10-30%
- All remaining wells must receive 0-5% unless you can provide strong textual evidence

**STAGE 3 - EVIDENCE AND SCORING**
For each well receiving >5% weight:
- Provide specific text excerpt (5-20 words) demonstrating its presence
- Convert percentage weight to 0.0-1.0 score using: Score = (Weight% ÷ 60) capped at 1.0
- For wells receiving ≤5% weight, assign scores 0.0-0.2 based on minimal presence

**QUALITY CONTROLS**
- If no theme achieves >40% weight, this narrative may not fit the Civic Virtue framework
- If you cannot find strong textual evidence for a well, it should score <0.2
- Dominant themes should be visually obvious to any reader of this text
```


### **Validation Against Synthetic Benchmarks**

**Perfect Positive Synthetic**: Should yield Dignity 90%+, all disintegrative wells 0-2%
**Perfect Negative Synthetic**: Should yield Tribalism 90%+, all integrative wells 0-2%
**Balanced Historical Speech**: Should distribute weight across 4-5 wells, no single well >40%

## Implementation Gameplan

### **Week 1: Prompt Development and Initial Testing**

**Days 1-2: Template Refinement**

- Draft 3-4 variant prompt templates using the hierarchical approach
- Test against current synthetic validation set
- Identify which template produces sharpest hierarchical distinctions

**Days 3-4: Cross-Model Validation**

- Run best template against Claude 3.5, GPT-4, and Gemini
- Document cross-model consistency in hierarchical rankings
- Identify systematic biases or failure modes per model

**Days 5-7: Iterative Refinement**

- Adjust template based on observed patterns
- Focus on cases where hierarchy isn't clearly emerging
- Establish final template for broader testing


### **Week 2: Systematic Validation**

**Days 1-3: Golden Set Analysis**

- Apply refined prompt to full 30-text validation corpus
- Calculate percentage of narratives achieving clear hierarchical dominance (target: 80%+)
- Document cases where framework fit appears poor

**Days 4-5: Statistical Benchmarking**

- Compare new vs. old prompt outputs on identical texts
- Measure increase in score variance and hierarchical clarity
- Validate that extreme cases now produce extreme scores

**Days 6-7: Cross-Framework Testing**

- Apply hierarchical prompting to Fukuyama Identity framework
- Confirm approach generalizes beyond Civic Virtue wells
- Document any framework-specific adjustments needed


### **Week 3: Quality Assurance and Documentation**

**Days 1-3: Reliability Testing**

- 10-run consistency testing on 10 diverse narratives
- Coefficient of variation analysis for multi-run stability
- Document any remaining inconsistency patterns

**Days 4-5: Edge Case Validation**

- Test boundary conditions: very short texts, non-English translations, ambiguous cases
- Establish clear guidance for when framework doesn't apply
- Create "poor fit" detection criteria

**Days 6-7: Documentation and Handoff**

- Complete technical documentation of prompt evolution
- Create training materials for human annotators
- Prepare for visualization mathematics integration


### **Success Criteria and Exit Conditions**

**Primary Success Metrics**:

- Synthetic extremes achieve 90%+ single-well dominance
- Real-world narratives show clear 2-3 theme hierarchy in 80%+ of cases
- Cross-model consistency (Spearman's ρ > 0.85) for hierarchical rankings
- Multi-run reliability (CV < 0.1) for dominant theme identification

**Secondary Validation Targets**:

- Framework fit detection identifies obvious mismatches
- Evidence excerpts provide clear textual grounding
- Relative weights align with human intuitive assessment

**Exit Criteria for Moving to Human Validation**:

- All primary success metrics achieved
- Technical documentation complete
- Prompt template locked for stability
- Integration ready for visualization mathematics track

