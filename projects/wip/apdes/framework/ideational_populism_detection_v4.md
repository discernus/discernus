# Ideational Populism Detection V4 Framework

## Framework Overview

This framework implements a three-stage analytical approach to populism detection that begins with faithful replication of Vanderveen et al. (2024) methodology, extends their analysis with enhanced dimensionality, and concludes with advanced insights only possible through Discernus's gasket architecture.

**Strategic Purpose**: Academic outreach demonstration showing "embrace and extend" capabilities - validating existing research while demonstrating superior analytical depth.

## Stage 1: Faithful Replication
*"What Vanderveen Did"*

### Core Classification Task
Sentence-level analysis using the ideational approach to populism with three-category classification:

- **POPULIST**: Appeals to "the people" against corrupt elites
- **PLURALIST**: Emphasis on democratic institutions, compromise, inclusion  
- **NEUTRAL**: Neither populist nor pluralist framing

### Analysis Prompt (Stage 1)
```
You are analyzing political speech for populist content using the ideational approach established by Mudde (2004) and operationalized by Vanderveen et al. (2024).

For each sentence, classify as:

POPULIST: Contains references to "the people" or ordinary citizens being betrayed, threatened, or opposed by corrupt elites, establishment figures, or special interests. Look for Manichean (good vs. evil) framing.

PLURALIST: Emphasizes democratic processes, institutional solutions, compromise between different groups, or inclusive governance approaches that acknowledge multiple legitimate interests.

NEUTRAL: Standard political communication without clear populist or pluralist framing - policy details, biographical information, procedural statements, etc.

SENTENCE: "{sentence}"

CLASSIFICATION: [POPULIST/PLURALIST/NEUTRAL]
REASONING: [Brief explanation of classification]
CONFIDENCE: [High/Medium/Low]
```

### Expected Outputs
- Direct comparison with Vanderveen's 84%/89% accuracy benchmarks
- Sentence-level classifications for validation against hand-coded training data
- Replication validation report demonstrating methodological fidelity

## Stage 2: Enhanced Analysis
*"What Vanderveen Should Have Done"*

### Extended Dimensions

#### Populist Intensity Gradients
- **WEAK**: Implicit people/elite distinction without explicit conflict
- **MODERATE**: Clear us-vs-them framing with policy-focused critique
- **STRONG**: Existential threat narrative with system-level condemnation

#### Populist Mechanisms
- **ANTI_ESTABLISHMENT**: Attacks on political institutions, career politicians, "Washington"
- **ANTI_ELITE**: Criticism of economic/cultural elites, experts, media
- **PEOPLE_SOVEREIGNTY**: Appeals to popular will over expert judgment, direct democracy themes

#### Temporal Context Analysis
- **CAMPAIGN_PHASE**: Primary vs. general election populist strategies
- **HISTORICAL_ERA**: Pre-Trump vs. Trump-era vs. post-Trump populism evolution
- **RESPONSE_MODE**: Proactive populist appeals vs. defensive populist reactions

### Analysis Prompt (Stage 2)
```
Building on the basic populist classification, now analyze dimensional characteristics:

SENTENCE: "{sentence}"
BASIC_CLASSIFICATION: {stage_1_result}

If POPULIST, analyze:

INTENSITY: 
- WEAK: Subtle people/elite distinction
- MODERATE: Clear oppositional framing
- STRONG: Existential threat/crisis narrative

MECHANISM:
- ANTI_ESTABLISHMENT: Attacks political institutions/career politicians
- ANTI_ELITE: Criticism of economic/cultural/expert elites  
- PEOPLE_SOVEREIGNTY: Popular will vs. expert/institutional authority

STRATEGIC_CONTEXT:
- TEMPORAL_POSITIONING: Where in speech (opening/climax/conclusion)
- AUDIENCE_TARGETING: Base mobilization vs. persuasion attempt
- DEFENSIVE_VS_PROACTIVE: Responding to attacks vs. initiating populist frame

SPEAKER_CONTEXT: {speaker} in {year} during {document_type}
```

### Expected Outputs
- Multi-dimensional populism profiles by candidate and era
- Intensity tracking across campaign phases and historical periods
- Mechanism analysis showing different types of populist appeals

## Stage 3: Advanced Analytics
*"What Only Discernus Can Do"*

### Salience Weighting Analysis

#### Rhetorical Positioning Factors
- **SPEECH_STRUCTURE**: Opening hooks, climactic moments, closing appeals
- **REPETITION_PATTERNS**: Frequency and variation of populist themes
- **EMOTIONAL_INTENSITY**: Anger, fear, hope, pride markers accompanying populist language
- **EMPHASIS_MARKERS**: Exclamation points, capitalization, "this is important" signals

#### Audience Resonance Indicators
- **APPLAUSE_CUES**: Lines designed to generate crowd response
- **CALL_AND_RESPONSE**: Interactive populist elements
- **MEMORABLE_PHRASES**: Soundbite-ready populist formulations
- **SOCIAL_MEDIA_OPTIMIZED**: Tweet-length populist messages

### Tension Analysis

#### Populist Contradictions
- **ELITE_STATUS_DENIAL**: Wealthy/powerful candidates claiming outsider status
- **INSTITUTIONAL_PARTICIPATION**: Anti-system rhetoric from system insiders
- **PLURALIST_POPULISM**: Democratic populism vs. authoritarian populism tensions

#### Rhetorical Complexity
- **CODE_SWITCHING**: Populist appeals to base, pluralist language to moderates
- **TEMPORAL_EVOLUTION**: Populist intensity changes within single speech
- **AUDIENCE_ADAPTATION**: Different populist frames for different constituencies

### Systemic Pattern Recognition

#### Cross-Candidate Analysis
- **POPULIST_CONTAGION**: How Trump's populism influences other Republican candidates
- **PARTY_DIFFERENTIATION**: Republican vs. Democratic populist strategies and evolution
- **TEMPORAL_DIFFUSION**: Spread of populist frames across political spectrum over time

#### Linguistic Innovation Tracking
- **VOCABULARY_EVOLUTION**: New terms entering populist lexicon ("deep state," "fake news")
- **FRAME_ADAPTATION**: How populist arguments evolve in response to events
- **STRATEGIC_LEARNING**: Candidates adapting populist approaches based on effectiveness

### Analysis Prompt (Stage 3)
```
Advanced populism analysis incorporating salience weighting and tension detection:

SENTENCE: "{sentence}"
PRIOR_ANALYSIS: {stage_1_and_2_results}
SPEECH_CONTEXT: Position {sentence_position} of {total_sentences} in {document_type}
SPEAKER_PROFILE: {speaker} - {ideology} - {character_profile}
TEMPORAL_CONTEXT: {year} - Era: {historical_era}

SALIENCE_ANALYSIS:
1. RHETORICAL_WEIGHT: How prominent is this populist element?
   - STRUCTURAL_POSITION: Opening/climax/conclusion vs. buried
   - REPETITION_STATUS: Novel theme vs. reinforced pattern
   - EMOTIONAL_CHARGE: High/medium/low intensity markers

2. AUDIENCE_TARGETING: Who is this populist appeal designed for?
   - BASE_MOBILIZATION: Energizing committed supporters
   - PERSUASION_ATTEMPT: Converting moderate/undecided voters
   - OPPOSITION_RESPONSE: Defensive populist positioning

TENSION_ANALYSIS:
1. CONTRADICTION_DETECTION: Does this create logical tensions?
   - ELITE_STATUS_CONTRADICTION: Powerful figure claiming outsider status
   - INSTITUTIONAL_CONTRADICTION: System participant attacking system
   - TEMPORAL_CONTRADICTION: Position changes over time

2. COMPLEXITY_PATTERNS: How sophisticated is the populist strategy?
   - AUDIENCE_SEGMENTATION: Different messages to different groups
   - CONTEXTUAL_ADAPTATION: Situation-specific populist framing
   - STRATEGIC_EVOLUTION: Learning and adaptation over time

SYSTEMIC_SIGNIFICANCE: How does this fit broader populist evolution patterns?
```

### Expected Outputs
- Salience-weighted populism scores showing relative importance of populist elements
- Tension maps revealing contradictions and strategic complexity
- Systemic pattern analysis showing populist evolution across candidates and time periods
- Innovation tracking documenting emergence of new populist language and strategies

## Framework Configuration

### Input Processing
```yaml
sentence_segmentation: true
context_preservation: true
metadata_integration:
  - speaker_profile
  - temporal_context  
  - document_type
  - ideological_baseline
  - character_profile
```

### Output Structure
```yaml
stage_1_replication:
  classification: [POPULIST|PLURALIST|NEUTRAL]
  confidence: [HIGH|MEDIUM|LOW]
  reasoning: string
  
stage_2_enhancement:
  intensity: [WEAK|MODERATE|STRONG]
  mechanism: [ANTI_ESTABLISHMENT|ANTI_ELITE|PEOPLE_SOVEREIGNTY]
  strategic_context: object
  
stage_3_advanced:
  salience_weight: float
  tension_indicators: array
  systemic_patterns: object
```

## Validation Strategy

### Stage 1 Validation
- Direct accuracy comparison with Vanderveen's published results (84%/89% benchmarks)
- Cross-validation against hand-coded training sentences from BYU dataset
- Inter-rater reliability testing using multiple framework runs

### Stage 2 Validation  
- Expert review of dimensional classifications
- Temporal consistency checking across candidate evolution
- Cross-candidate pattern validation

### Stage 3 Validation
- Salience weighting correlation with speech emphasis markers
- Tension analysis validation against known candidate contradictions
- Systemic pattern verification against political science literature

## Academic Presentation Strategy

**Phase 1**: "We faithfully replicated your methodology and achieved comparable accuracy, validating the robustness of the ideational approach."

**Phase 2**: "We extended your analysis to reveal that populism operates through distinct mechanisms with varying intensity across campaign contexts."

**Phase 3**: "We discovered previously invisible patterns in populist salience and strategic complexity that transform our understanding of populist communication."

This progression demonstrates:
1. **Academic credibility** through methodological validation
2. **Analytical superiority** through enhanced dimensionality  
3. **Unique insights** only possible with Discernus's advanced capabilities

---

*Framework developed for academic outreach demonstration showing "embrace and extend" capabilities with Vanderveen et al. (2024) populism classification research.*