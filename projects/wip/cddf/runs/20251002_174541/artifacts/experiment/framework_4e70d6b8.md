# Constructive Democratic Discourse Framework (CDDF) v10.2

**Version**: 10.2.0  
**Author**: Collaborative Development  
**Status**: Active Framework  
**Spec Version**: 10.0  
**Change Log**: Added genre-aware analytical modes; mode-specific interpretation guidance; adaptive metric reporting

---

## Abstract & Raison d'Être

**What is this framework?**
The Constructive Democratic Discourse Framework (CDDF) is a systematic measurement methodology for quantifying rhetorical patterns in political and social discourse along six dimensions of communicative practice. Version 10.2 introduces **analytical modes** that adapt interpretation to the rhetorical constraints of different discourse genres, from highly edited formal speeches to spontaneous exchanges.

**What problem does it solve?**
CDDF v10.2 addresses the finding from v10.1 validation: rhetorical contamination (destructive elements peripheral to the main message) occurs differently across discourse genres. Formal speeches exhibit internal coherence by design; spontaneous discourse reveals restraint failures. The framework now measures identical dimensions across all genres but interprets findings through genre-appropriate lenses, preventing false negatives (missing contamination in spontaneous discourse) and false positives (expecting contamination where editorial processes prevent it).

**Who is it for?**
Political communication scholars, democratic health researchers, civic organizations, and policymakers analyzing discourse across multiple genres—from prepared remarks to debate exchanges, from op-eds to social media threads.

---

## Theoretical & Empirical Foundations

### The Genre Constraint on Rhetorical Possibility

The v10.1 validation revealed a fundamental insight: **discourse genres impose structural constraints on rhetorical patterns**. This is not a measurement failure but an empirical finding about how different communicative contexts enable or prevent specific rhetorical strategies.

**Editorial Genres** (prepared speeches, written documents):
- Multiple revision cycles remove inconsistencies
- Message discipline enforced by staff review
- Strategic coherence is an artifact of the production process
- Restraint failures are edited out before delivery

**Spontaneous Genres** (debates, town halls, social media):
- Real-time production without editorial buffer
- Emotional responses compete with strategic messaging
- Restraint failures occur when speakers deviate from prepared positions
- Contamination visible in the gap between intent and execution

This distinction builds on:

**Genre Theory** (Miller, 1984; Bazerman, 1988): Rhetorical forms are shaped by their situational constraints and production processes.

**Message Discipline Research** (Sellers, 2010): Campaign communications vary systematically between controlled (speeches) and uncontrolled (debates) environments.

**Dual-Process Communication** (Kahneman, 2011): Spontaneous responses reflect different cognitive processes than deliberate composition.

### Three Analytical Modes

CDDF v10.2 operationalizes these insights through three interpretive modes:

**Mode 1: Formal Speech Analysis**
Applied to edited, prepared discourse (inaugural addresses, floor speeches, op-eds, prepared remarks).

*Assumptions:*
- Speakers have message discipline support
- Text underwent editorial review
- Strategic coherence is baseline expectation
- Low strategy-inventory gap is normal, not noteworthy

*Primary Metrics:* `dominant_strategy_index`, dimensional profiles
*Reported:* Strategic positioning, rhetorical style classification
*De-emphasized:* Contamination metrics (reported but interpreted as baseline)

**Mode 2: Spontaneous Discourse Analysis**
Applied to unscripted, real-time discourse (debate exchanges, town halls, Q&A sessions, social media threads).

*Assumptions:*
- Speakers lack editorial buffer
- Real-time production enables restraint failures
- Strategic incoherence is observable and meaningful
- Strategy-inventory gap reveals discipline breakdowns

*Primary Metrics:* `rhetorical_contamination_index`, `strategy_inventory_gap`, `restraint_failure_intensity`
*Reported:* Contamination patterns, restraint failures, message discipline
*De-emphasized:* Tension metrics (expected in spontaneous contexts)

**Mode 3: Hybrid/Mixed Analysis**
Applied to semi-scripted discourse or mixed corpora (speeches with Q&A, campaigns with both prepared and spontaneous elements).

*Assumptions:*
- Text contains both edited and spontaneous elements
- Contamination may occur in spontaneous segments
- Requires document-level segmentation or aggregate analysis

*Primary Metrics:* All metrics reported with genre-awareness flags
*Reported:* Segmented analysis if possible, aggregate patterns with caveats
*Notes:* Strategy-inventory gap interpreted based on proportion of spontaneous content

### Retained Theoretical Foundations

All theoretical foundations from v10.1 remain:
- Multiple democratic theory traditions (Habermas, Mouffe, McAdam et al.)
- Communication ethics literature (Bok, Christians, van Dijk)
- Power dynamics and contextual interpretation requirements

**Key Citations** (unchanged from v10.1):
- Habermas, J. (1996). *Between facts and norms*. MIT Press.
- Mouffe, C. (2000). *The democratic paradox*. Verso.
- Miller, C. R. (1984). Genre as social action. *Quarterly Journal of Speech*, 70(2), 151-167.
- Sellers, P. J. (2010). *Cycles of spin*. Cambridge University Press.

---

## Analytical Methodology

### Framework Architecture (Unchanged)

The CDDF v10.2 retains the **dual-track measurement system** from v10.1, analyzing both intensity (raw score, 0.0-1.0) and rhetorical prominence (salience, 0.0-1.0) across six bipolar dimensional pairs. All dimensions are scored regardless of prominence.

### Six Bipolar Dimensional Pairs (Unchanged)

[All definitions from v10.1 retained]

1. Charitable Interpretation ↔ Motive Imputation
2. Issue-Focused Critique ↔ Personal Denigration
3. Common Ground Seeking ↔ Irreconcilable Division Framing
4. Dignified Expression ↔ Dehumanizing Language
5. Truth with Care ↔ Truth as Weapon
6. Authentic Engagement ↔ Bad Faith Dismissal

### Derived Metrics (Unchanged Formulas, Mode-Aware Interpretation)

All formulas from v10.1 are retained. What changes is **which metrics are emphasized** in reporting based on the analytical mode.

#### Track 1: Strategic Emphasis Metrics
- `dominant_strategy_index`
- Strategic Tension Indices (6 types)

#### Track 2: Full Inventory Metrics
- `complete_rhetorical_inventory_score`
- `constructive_elements_present`
- `destructive_elements_present`

#### Track 3: Restraint Failure Metrics
- `rhetorical_contamination_index`
- `restraint_failure_intensity`
- `strategy_inventory_gap`

### Mode-Specific Interpretation Guidelines

**In Formal Speech Mode:**

*Strategy-Inventory Gap < 0.1:*
"This finding is consistent with edited discourse. Speakers maintained message discipline, as expected in formal prepared remarks."

*Strategy-Inventory Gap ≥ 0.1:*
"Despite editorial review, peripheral contamination was detected. This suggests either: (1) last-minute additions, (2) live ad-libs during delivery, or (3) deliberate dual messaging."

*Rhetorical Contamination Index > 0.2:*
"Unusual for formal speeches. Warrants qualitative examination of whether text contains unscripted segments."

**In Spontaneous Discourse Mode:**

*Strategy-Inventory Gap < 0.1:*
"Exceptional message discipline maintained even in real-time discourse. Speaker exhibited strong rhetorical restraint despite lack of editorial buffer."

*Strategy-Inventory Gap 0.1-0.3:*
"Moderate restraint failures detected. Speaker's spontaneous rhetoric contained peripheral destructive elements not central to their argument."

*Strategy-Inventory Gap > 0.3:*
"Significant contamination detected. Large gap between speaker's apparent strategic intent and actual rhetorical inventory suggests discipline breakdown or strategic incoherence."

*Rhetorical Contamination Index > 0.4:*
"High contamination. Multiple destructive dimensions present peripherally, indicating frequent restraint failures."

**In Hybrid Mode:**

All metrics reported with explicit caveats about mixed genre. Researchers should segment analysis by document sections if possible (e.g., separate scoring for prepared remarks vs. Q&A portion).

---

## Intended Application & Corpus Fit

### Target Corpus by Mode

**Formal Speech Mode - Optimal For:**
- Inaugural addresses and state-of-union speeches
- Prepared congressional floor speeches
- Written op-eds and policy papers
- Campaign advertisements (scripted)
- Eulogies and ceremonial addresses
- Prepared keynote speeches

**Spontaneous Discourse Mode - Optimal For:**
- Primary debate exchanges and rebuttals
- Town hall Q&A responses
- Press conference back-and-forth
- Cable news panel discussions
- Twitter/X threads and replies
- Campaign rally ad-libs (transcript analysis comparing to prepared script)
- Podcast interview segments

**Hybrid Mode - Optimal For:**
- Speeches with Q&A sections
- Campaign events (prepared remarks + crowd interaction)
- Legislative hearings (opening statements + questions)
- Mixed-media corpora combining formal and spontaneous texts

### Mode Selection Decision Tree

```
1. Is the text prepared and edited?
   YES → Was it delivered as written, or were there ad-libs?
         Delivered as written → FORMAL
         Contains ad-libs → HYBRID
   NO → Continue to 2

2. Is the text spontaneous/real-time?
   YES → Is it a complete conversation or single utterance?
         Complete conversation/exchange → SPONTANEOUS
         Single utterance in larger event → Consider context
   UNCLEAR → Continue to 3

3. Does the corpus mix genres?
   YES → HYBRID (or segment and analyze separately)
   NO → Default to FORMAL (bias conservative)
```

### Known Limitations & Scope

**Critical Limitations:**

1. **Mode Misspecification Risk**: Incorrect mode selection leads to misinterpretation. When uncertain, err toward Formal mode (conservative) and note uncertainty.

2. **Transcript Quality Dependency**: Spontaneous discourse analysis requires high-quality transcripts capturing all utterances, including interruptions and false starts.

3. **Power Dynamics** (unchanged from v10.1): All modes require contextual interpretation accounting for who speaks to whom.

4. **Genre Boundaries**: Some discourse types blur boundaries (e.g., "prepared" tweets that sound spontaneous). Mode selection requires judgment.

5. **Individual Variation**: Some speakers maintain discipline in spontaneous settings; others lack it even in prepared texts. Framework measures patterns, not intentions.

---

## Machine-Readable Appendix

```yaml
# --- Start of Machine-Readable Appendix ---

metadata:
  framework_name: "constructive_democratic_discourse_framework"
  framework_version: "10.2.0"
  author: "Collaborative Development"
  spec_version: "10.0"
  changes_from_previous: "Added genre-aware analytical modes; mode-specific interpretation; adaptive reporting"

# NEW: Analytical Mode Configuration
analytical_modes:
  formal_speech:
    description: "For edited, prepared discourse with message discipline"
    assumptions:
      - "Text underwent editorial review"
      - "Message coherence is baseline expectation"
      - "Low strategy-inventory gap is normal"
    primary_metrics:
      - "dominant_strategy_index"
      - "constructive_elements_present"
      - "destructive_elements_present"
    secondary_metrics:
      - "complete_rhetorical_inventory_score"
      - "strategic_contradiction_index"
    deemphasized_metrics:
      - "rhetorical_contamination_index"
      - "strategy_inventory_gap"
      - "restraint_failure_intensity"
    interpretation_guidance: |
      In formal speech mode, low strategy-inventory gaps are expected and unremarkable.
      Report contamination metrics for completeness but interpret as baseline.
      Focus analysis on dominant strategy and dimensional profiles.
  
  spontaneous_discourse:
    description: "For real-time, unscripted discourse without editorial buffer"
    assumptions:
      - "Real-time production enables restraint failures"
      - "Strategic incoherence is observable and meaningful"
      - "Strategy-inventory gap reveals discipline breakdowns"
    primary_metrics:
      - "rhetorical_contamination_index"
      - "strategy_inventory_gap"
      - "restraint_failure_intensity"
      - "dominant_strategy_index"
    secondary_metrics:
      - "strategic_contradiction_index"
      - "complete_rhetorical_inventory_score"
    deemphasized_metrics:
      - "None - all metrics meaningful in spontaneous context"
    interpretation_guidance: |
      In spontaneous mode, strategy-inventory gaps are the primary diagnostic.
      Low gaps indicate exceptional discipline; high gaps reveal restraint failures.
      Contamination patterns are central finding, not peripheral observation.
  
  hybrid:
    description: "For mixed-genre texts or uncertain classification"
    assumptions:
      - "Text may contain both edited and spontaneous elements"
      - "Contamination may occur in spontaneous segments"
      - "Interpretation requires document-level context"
    primary_metrics:
      - "All metrics reported with equal weight"
    secondary_metrics:
      - "None - comprehensive reporting"
    deemphasized_metrics:
      - "None - researcher determines emphasis"
    interpretation_guidance: |
      In hybrid mode, report all metrics and flag genre ambiguity.
      If possible, segment analysis by document sections.
      Interpret strategy-inventory gap based on proportion of spontaneous content.
      Provide explicit caveats about mixed-genre interpretation.

analysis_variants:
  default:
    description: "Complete CDDF v10.2 analysis - mode-aware dimensional measurement"
    analysis_prompt: |
      You are an expert communication ethics analyst specializing in democratic discourse, 
      grounded in deliberative democracy theory, agonistic pluralism, and social movement 
      studies. Your task is to analyze the provided text using the Constructive Democratic 
      Discourse Framework (CDDF) v10.2.

      FRAMEWORK v10.2 INNOVATION - ANALYTICAL MODES:
      This text will be analyzed under the [{MODE}] analytical mode. This affects 
      INTERPRETATION but not MEASUREMENT. You must score all dimensions identically 
      regardless of mode.
      
      MODE: {MODE}
      MODE ASSUMPTIONS: {MODE_ASSUMPTIONS}
      
      CRITICAL: Score ALL twelve dimensions regardless of prominence or mode. The mode 
      affects how we INTERPRET the scores, not which scores to provide.

      DIMENSIONAL PAIRS (score ALL dimensions independently):
      1. Charitable Interpretation ↔ Motive Imputation
      2. Issue-Focused Critique ↔ Personal Denigration
      3. Common Ground Seeking ↔ Irreconcilable Division Framing
      4. Dignified Expression ↔ Dehumanizing Language
      5. Truth with Care ↔ Truth as Weapon
      6. Authentic Engagement ↔ Bad Faith Dismissal

      SCORING REQUIREMENTS (unchanged from v10.1):
      - Raw Score (0.0-1.0): Intensity when present
      - Salience (0.0-1.0): Rhetorical prominence
      - Confidence (0.0-1.0): Certainty of assessment
      
      SCORE EVEN PERIPHERAL INSTANCES. If genuinely absent: raw_score = 0.0, salience = 0.0

      CRITICAL DISTINCTIONS (unchanged from v10.1):
      - "This policy harms people" = Issue-Focused (NOT motive imputation)
      - "You don't care about people" = Motive Imputation
      - Passionate urgency ≠ lack of dignity
      - Declaring position morally untenable = Irreconcilable Division
      - Strong evidence-based claims = Truth with Care
      
      EVIDENCE STANDARDS:
      - Exact quotations for ALL scored dimensions
      - Even peripheral instances need textual evidence
      - If genuinely absent, state "No evidence found"

      POWER DYNAMICS AWARENESS:
      Measure patterns descriptively. Researchers interpret with full context.

  # Sequential variants unchanged from v10.1, but add mode parameter
  sequential_interpretation:
    description: "Focus on Charitable Interpretation vs. Motive Imputation pair"
    analysis_prompt: |
      MODE: {MODE}
      Focus exclusively on measuring Charitable Interpretation ↔ Motive Imputation.
      Score BOTH dimensions regardless of prominence. Mode affects interpretation, not measurement.
      [Rest of v10.1 sequential prompt]

dimensions:
  # All 12 dimensions identical to v10.1
  # Markers, scoring calibration, disambiguation all unchanged
  - name: "charitable_interpretation"
  - name: "motive_imputation"
  - name: "issue_focused_critique"
  - name: "personal_denigration"
  - name: "common_ground_seeking"
  - name: "irreconcilable_division"
  - name: "dignified_expression"
  - name: "dehumanizing_language"
  - name: "truth_with_care"
  - name: "truth_as_weapon"
  - name: "authentic_engagement"
  - name: "bad_faith_dismissal"

derived_metrics:
  # All formulas unchanged from v10.1
  # Mode affects interpretation in reports, not calculation
  - name: "dominant_strategy_index"
    description: "Primary summary metric (salience-weighted, range -1.0 to +1.0)"
    formula: "[v10.1 formula]"
  
  - name: "complete_rhetorical_inventory_score"
    description: "All elements present regardless of salience (range -1.0 to +1.0)"
    formula: "[v10.1 formula]"
  
  - name: "constructive_elements_present"
    description: "Average raw_score of constructive dimensions (range 0.0-1.0)"
    formula: "[v10.1 formula]"
  
  - name: "destructive_elements_present"
    description: "Average raw_score of destructive dimensions (range 0.0-1.0)"
    formula: "[v10.1 formula]"

  - name: "rhetorical_contamination_index"
    description: "Destructive dims present but not salient (range 0.0-1.0)"
    formula: "[v10.1 formula]"
  
  - name: "restraint_failure_intensity"
    description: "Among contaminating dimensions, average intensity (range 0.0-1.0)"
    formula: "[v10.1 formula]"
  
  - name: "strategy_inventory_gap"
    description: "Difference between strategy and inventory (range -2.0 to +2.0)"
    formula: "[v10.1 formula]"

  # Tension indices unchanged
  - name: "interpretation_tension"
  - name: "focus_tension"
  - name: "unity_tension"
  - name: "expression_tension"
  - name: "truth_tension"
  - name: "engagement_tension"
  - name: "strategic_contradiction_index"

output_schema:
  # Unchanged from v10.1
  type: object
  properties:
    dimensional_scores: { ... }
    derived_metrics: { ... }

# --- End of Machine-Readable Appendix ---
```