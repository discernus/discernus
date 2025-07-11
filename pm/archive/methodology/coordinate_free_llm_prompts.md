# Coordinate-Free Populism Analysis: Enhanced LLM Prompts
# Generated from coordinate_free_populism_validation_experiment.yaml (Enhanced Version)
# 
# This document shows the enhanced prompts optimized for Brazilian political context
# with improved operational definitions, cultural specificity, and structured outputs.
# These prompts incorporate expert assessment feedback for maximum analytical rigor.
#
# Date: 2025-07-02 (Enhanced)
# Source: coordinate_free_populism_validation_experiment.yaml
# Status: Production-ready with Brazilian context optimization

# ================================================================
# ENHANCEMENT SUMMARY
# ================================================================

**Key Improvements Made:**
- **Expert Role Definitions**: Specialized analytical personas for each stage (discourse analyst, political scientist, strategic communication analyst, methodology expert)
- **Brazilian Cultural Context**: Specific linguistic markers and political references
- **Operational Definitions**: Clear criteria for all assessment scales (High/Medium/Low/None)
- **Enhanced Coherency Patterns**: Added "Authoritarian populist" and "Strategic ambiguity" options
- **Structured Output Formats**: Standardized response formats for systematic data extraction
- **Framework Fit Optimization**: Enhanced coverage assessment with 70% threshold guidance
- **Evidence Standards**: Portuguese original + English translation requirements
- **Methodological Precision**: Clear distinctions between populist and related themes
- **Theoretical Grounding**: References to key scholars and Brazilian constitutional framework

# ================================================================
# EXPERIMENT CONTEXT
# ================================================================

**Experiment**: Coordinate-Free vs Coordinate-Based Populism Analysis: Validation Study
**LLM Models**: GPT-4 or Claude-3.5 Sonnet
**Analysis Strategy**: Sequential stage processing with validation checks
**Corpus**: Brazilian political speeches (2018 election period)
**Sample Size**: 40 speeches (20 high-populism, 20 low-populism expected)
**Optimization**: Enhanced for Bolsonaro campaign speech analysis

# ================================================================
# EXPERT ROLE DEFINITIONS
# ================================================================

## Role Definition Strategy
Each analysis stage begins with an expert role definition to prime the LLM with appropriate analytical expertise, theoretical knowledge, and cultural competency. This enhances analytical quality, consistency, and domain-specific knowledge activation.

### Stage 1: Discourse Analysis Expert
**Role**: Expert discourse analyst specializing in Brazilian political communication
**Expertise**: Qualitative analysis methods, Brazilian political culture, 2018 election context, coded language
**Focus**: Systematic theme identification without framework bias

### Stage 2A: Populism Theory Expert  
**Role**: Political scientist with expertise in populism theory and Brazilian democratic discourse
**Expertise**: Ideational theory of populism (Mudde, Hawkins, Urbinati), Brazilian political history
**Focus**: Distinguishing populism from nationalism, authoritarianism, religious conservatism

### Stage 2B: Democratic Pluralism Expert
**Role**: Political scientist with expertise in democratic pluralism theory and Brazilian institutional democracy  
**Expertise**: Democratic pluralism theory (Dahl, Urbinati, Levitsky & Ziblatt), 1988 Brazilian Constitution
**Focus**: Institutional mediation, minority rights, procedural democracy

### Stage 3: Strategic Communication Expert
**Role**: Strategic communication analyst with expertise in Brazilian political discourse
**Expertise**: Competitive rhetorical dynamics, audience segmentation, coded messaging, strategic complexity
**Focus**: Complex strategic patterns, sophisticated vs incoherent messaging

### Stage 4: Methodology Expert
**Role**: Methodology expert in discourse analysis frameworks
**Expertise**: Framework evaluation, bias prevention, adaptive framework selection, analytical limitations
**Focus**: Honest assessment of framework appropriateness and improvement recommendations

# ================================================================
# STAGE 1: DISCOVERY ANALYSIS PROMPT
# ================================================================

## Stage 1 Prompt Template
```
You are an expert discourse analyst specializing in Brazilian political communication with deep expertise in qualitative analysis methods. You have extensive knowledge of Brazilian political culture, the historical context of the 2018 presidential election, and systematic approaches to identifying rhetorical themes without imposing preconceived analytical frameworks. Your expertise includes understanding coded language, cultural references, and the complex dynamics of Brazilian democratic discourse.

Analyze this Brazilian political speech from the 2018 presidential election without using any predefined categories.

TEXT: {speech_text}

Questions:
1. What are the 3-5 main themes in this speech?

2. How does this speech approach democratic governance?

3. What values are prioritized or emphasized?

4. What model of governance does this speech seem to prefer?

5. How do the main themes relate to each other?

Provide specific evidence from the text for each assessment.
```

## Stage 1 Output Validation Criteria
- Themes are specific and evidence-based
- Governance approach is clearly characterized  
- Value priorities are supported by textual evidence

# ================================================================
# STAGE 2: ANCHOR ASSESSMENT PROMPTS
# ================================================================

## Stage 2A: Populism Assessment Prompt Template
```
You are a political scientist with expertise in populism theory and Brazilian democratic discourse. Your specialization includes the ideational theory of populism (Mudde, Hawkins, Urbinati), Brazilian political history, and the specific cultural and linguistic manifestations of populist rhetoric in Brazilian electoral politics. You understand how populism differs from related phenomena like nationalism, authoritarianism, and religious conservatism, and you're expert in identifying populist themes within the complex context of Brazilian political competition.

Based on this Brazilian political speech from the 2018 presidential election, assess populist themes:

TEXT: {speech_text}

Populism Assessment:
1. PRESENCE: Are populist themes present? (Yes/No/Unclear)
   - Look for: anti-elite rhetoric, people-centric claims, us-vs-them framing

2. SALIENCE: How central are populist themes? (High/Medium/Low/None)
   - Consider: prominence, repetition, emphasis in speech structure

3. EVIDENCE: What specific language supports your assessment?
   - Quote exact phrases and provide context

4. INTENSITY: How strongly emphasized? (Strong/Moderate/Weak/None)
   - Assess: emotional language, rhetorical devices, conviction level

5. CONSISTENCY: Are themes consistently applied? (Consistent/Mixed/Inconsistent)
   - Check: throughout speech, contradictory elements, thematic coherence

6. CONFIDENCE: How confident are you in this assessment? (High/Medium/Low)
   - Consider: clarity of evidence, ambiguity, interpretive uncertainty
```

## Stage 2B: Pluralism Assessment Prompt Template
```
You are a political scientist with expertise in democratic pluralism theory and Brazilian institutional democracy. Your specialization includes democratic pluralism theory (Dahl, Urbinati, Levitsky & Ziblatt), Brazilian constitutional democracy, and the institutional framework established by the 1988 Constitution. You understand how pluralist principles manifest in Brazilian political discourse, including institutional mediation, minority rights protection, and procedural democracy. You're expert in identifying pluralist themes and distinguishing them from related concepts like moderate conservatism or procedural legalism.

Based on this Brazilian political speech from the 2018 presidential election, assess pluralist themes:

TEXT: {speech_text}

Pluralism Assessment:
1. PRESENCE: Are pluralist themes present? (Yes/No/Unclear)
   - Look for: institutional respect, minority rights, procedural democracy

2. SALIENCE: How central are pluralist themes? (High/Medium/Low/None)
   - Consider: prominence, repetition, emphasis in speech structure

3. EVIDENCE: What specific language supports your assessment?
   - Quote exact phrases and provide context

4. INTENSITY: How strongly emphasized? (Strong/Moderate/Weak/None)
   - Assess: commitment level, rhetorical emphasis, detailed elaboration

5. CONSISTENCY: Are themes consistently applied? (Consistent/Mixed/Inconsistent)
   - Check: throughout speech, contradictory elements, thematic coherence

6. CONFIDENCE: How confident are you in this assessment? (High/Medium/Low)
   - Consider: clarity of evidence, ambiguity, interpretive uncertainty
```

# ================================================================
# STAGE 3: COMPETITIVE ANALYSIS PROMPT
# ================================================================

## Stage 3 Prompt Template
```
You are a strategic communication analyst with expertise in Brazilian political discourse and competitive rhetorical dynamics. Your specialization includes understanding how competing democratic theories interact in practice, identifying sophisticated rhetorical strategies including audience segmentation and coded messaging, and analyzing the complex strategic patterns that emerge in Brazilian electoral competition. You're expert in recognizing when apparent contradictions reflect strategic sophistication vs genuine incoherence, and you understand the historical and cultural factors that shape Brazilian political strategy.

Analyze how populist and pluralist themes interact in this Brazilian political speech:

POPULISM ASSESSMENT: {populism_results}
PLURALISM ASSESSMENT: {pluralism_results}

Competitive Analysis:
1. OPPOSITION: Do populist and pluralist themes directly compete?
   - Identify specific areas of tension or contradiction

2. COEXISTENCE: Are there areas where both themes coexist?
   - Note compatibility or complementary elements

3. DOMINANCE: Which theme is more prominent and in what contexts?
   - Assess relative emphasis and strategic positioning

4. COHERENCY PATTERN: Which pattern best describes this speech?
   - Focused populist: High populism, low pluralism
   - Focused pluralist: High pluralism, low pluralism  
   - Democratic tension: Moderate both with clear tension
   - Incoherent mixture: High both, potentially contradictory

5. STRATEGIC ASSESSMENT: What rhetorical strategy does this represent?
   - Focused messaging, coalition building, or audience segmentation?
```

# ================================================================
# STAGE 4: FRAMEWORK FIT ASSESSMENT PROMPT
# ================================================================

## Stage 4 Prompt Template
```
You are a methodology expert in discourse analysis frameworks with deep expertise in evaluating when analytical frameworks are well-suited vs poorly suited to specific texts. Your specialization includes understanding framework bias, tunnel vision, and the importance of adaptive framework selection in preventing analytical distortion. You're expert in honest assessment of analytical limitations, identifying when frameworks impose artificial categories on rhetorical reality, and providing constructive recommendations for framework improvement or alternative approaches. Your expertise includes Brazilian political discourse and the specific challenges of analyzing complex multi-audience political communication.

Assess how well the populism/pluralism framework captures this Brazilian political speech:

DISCOVERY RESULTS: {discovery_results}
FRAMEWORK RESULTS: {framework_results}

Framework Fit Assessment:
1. COVERAGE: How much of what matters in this speech is captured by populism/pluralism analysis? (%)

2. GAPS: What important themes are not captured by this framework?
   - List specific themes from discovery that don't fit

3. RELEVANCE: How relevant are populism/pluralism concepts to this speech?
   - Excellent/Good/Fair/Poor relevance rating

4. ALIGNMENT: Do discovery themes align with framework results?
   - Strong/Moderate/Weak/No alignment

5. EXPLANATORY POWER: Does populism/pluralism analysis explain observed patterns?
   - High/Medium/Low explanatory power

6. CONFIDENCE: How confident are you in the framework applicability?
   - High/Medium/Low confidence with reasoning
```

# ================================================================
# VARIABLE SUBSTITUTION REFERENCE
# ================================================================

## Variables Used in Prompts:

### {speech_text}
- **Content**: Full text of the Brazilian political speech being analyzed
- **Usage**: Stages 1, 2A, 2B
- **Format**: Plain text, minimum 500 words per experiment specification

### {populism_results}
- **Content**: Complete output from Stage 2A populism assessment
- **Usage**: Stage 3 competitive analysis
- **Format**: Structured assessment with all 6 evaluation criteria (presence, salience, evidence, intensity, consistency, confidence)

### {pluralism_results}
- **Content**: Complete output from Stage 2B pluralism assessment  
- **Usage**: Stage 3 competitive analysis
- **Format**: Structured assessment with all 6 evaluation criteria (presence, salience, evidence, intensity, consistency, confidence)

### {discovery_results}
- **Content**: Complete output from Stage 1 discovery analysis
- **Usage**: Stage 4 framework fit assessment
- **Format**: Answers to all 5 discovery questions (themes, governance approach, values, governance model, thematic relationships)

### {framework_results}
- **Content**: Combined results from Stages 2A, 2B, and 3
- **Usage**: Stage 4 framework fit assessment
- **Format**: Complete populism assessment + pluralism assessment + competitive analysis

# ================================================================
# PROMPT EXECUTION SEQUENCE
# ================================================================

## Automated Execution Flow:

1. **Stage 1 Execution**
   - Send Stage 1 prompt with {speech_text} substituted
   - Validate output against Stage 1 criteria
   - Store results as {discovery_results}

2. **Stage 2A Execution** 
   - Send Stage 2A prompt with same {speech_text}
   - Validate populism assessment completeness
   - Store results as {populism_results}

3. **Stage 2B Execution**
   - Send Stage 2B prompt with same {speech_text}
   - Validate pluralism assessment completeness
   - Store results as {pluralism_results}

4. **Stage 3 Execution**
   - Send Stage 3 prompt with {populism_results} and {pluralism_results} substituted
   - Validate competitive analysis completeness
   - Combine with Stage 2 results to create {framework_results}

5. **Stage 4 Execution**
   - Send Stage 4 prompt with {discovery_results} and {framework_results} substituted
   - Validate framework fit assessment completeness
   - Store final comprehensive analysis

# ================================================================
# IMPLEMENTATION NOTES
# ================================================================

## Prompt Construction Rules:
- Remove all inline comments (lines starting with #) from prompts
- Preserve exact formatting including line breaks and indentation
- Substitute variables with actual content as specified
- Include all numbered questions and bullet points exactly as written
- Maintain parenthetical response format specifications (e.g., "Yes/No/Unclear")

## Quality Control:
- Each stage must complete successfully before proceeding to next stage
- All structured response formats must be validated against specification
- Evidence requirements must be enforced (specific quotes and context)
- Confidence ratings must be included in all assessments

## Expected Output Format:
- Stage 1: Narrative responses to 5 discovery questions with textual evidence
- Stage 2A/2B: Structured 6-point assessments (presence, salience, evidence, intensity, consistency, confidence)
- Stage 3: 5-point competitive analysis with coherency pattern classification
- Stage 4: 6-point framework fit assessment with percentage coverage estimate

## Corpus Application:
- These prompts will be applied to 40 Brazilian political speeches
- Same prompt sequence executed for each speech
- Results aggregated for comparative analysis with coordinate-based approaches
- Framework fit assessments used for adaptive framework selection validation

# ================================================================
# EXPERIMENTAL VALIDATION
# ================================================================

## Validation Criteria:
- **Internal Consistency**: Stage results align with each other
- **Evidence Quality**: All assessments supported by specific textual evidence  
- **Response Completeness**: All required elements present in structured format
- **Confidence Calibration**: Confidence ratings align with assessment quality

## Success Metrics:
- Discovery analysis identifies themes missed by framework-first approaches
- Framework fit assessment accurately predicts populism relevance
- Competitive analysis reveals strategic messaging patterns
- Coordinate-free approach demonstrates superior analytical distinctiveness

---

**Note**: This document represents the complete enhanced LLM prompt specification for the coordinate-free populism validation experiment, including expert role definitions for optimal analytical performance. All prompts now begin with specialized analytical personas to prime LLM expertise and cultural competency. Software systems should construct prompts exactly as specified, including role definitions, to ensure experimental replicability and methodological rigor. 