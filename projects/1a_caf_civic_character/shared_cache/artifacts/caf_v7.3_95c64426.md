# Civic Analysis Framework (CAF) v7.3

The Civic Analysis Framework provides a systematic approach to evaluating the civic character of political discourse, focusing on the fundamental tensions between competing civic virtues and their strategic deployment in public communication.

## Raison d'Être

Democratic governance depends on civic discourse that embodies fundamental virtues: dignity, truth, justice, hope, and pragmatism. However, political communication often involves strategic tensions where speakers simultaneously appeal to competing virtues and their pathological counterparts. This framework provides a rigorous methodology for evaluating these tensions and assessing the overall civic character of political discourse.

## Research Foundations

This framework is grounded in:
- **Classical Civic Republican Theory**: Sustainable democratic governance requires citizens and leaders who embody civic virtues
- **Virtue Ethics**: Character assessment through demonstrated patterns of moral reasoning
- **Political Communication Theory**: Strategic deployment of appeals in public discourse
- **Tension Mathematics**: Quantitative assessment of competing value systems

## Dimensions and Axes

The framework evaluates political discourse across five bipolar axes that form the foundation of civic character:

### Identity Axis: Dignity ↔ Tribalism
- **Dignity (0.0-1.0)**: Appeals to universal human worth, respect for individuals regardless of group membership, emphasis on shared humanity and individual moral agency
- **Tribalism (0.0-1.0)**: Appeals to group identity, us-vs-them framing, emphasis on group loyalty over universal principles, exclusionary rhetoric

### Truth Axis: Truth ↔ Manipulation  
- **Truth (0.0-1.0)**: Commitment to factual accuracy, acknowledgment of complexity, intellectual honesty, evidence-based reasoning
- **Manipulation (0.0-1.0)**: Strategic distortion of information, emotional manipulation, misleading framing, exploitation of cognitive biases

### Justice Axis: Justice ↔ Resentment
- **Justice (0.0-1.0)**: Concern for fair outcomes, procedural fairness, protection of rights, systemic equity considerations
- **Resentment (0.0-1.0)**: Exploitation of grievances, blame-focused rhetoric, zero-sum framing, victimization narratives

### Emotional Axis: Hope ↔ Fear
- **Hope (0.0-1.0)**: Constructive optimism, positive vision for the future, empowerment rhetoric, possibility-focused language
- **Fear (0.0-1.0)**: Anxiety-inducing rhetoric, threat-focused language, catastrophic framing, security-based appeals

### Reality Axis: Pragmatism ↔ Fantasy
- **Pragmatism (0.0-1.0)**: Realistic problem-solving, acknowledgment of constraints, practical solutions, incremental progress
- **Fantasy (0.0-1.0)**: Unrealistic promises, magical thinking, oversimplified solutions, denial of constraints

## Linguistic Markers

**Critical Note**: These markers represent semantic spaces and conceptual patterns, not keyword lists. Analysts should look for the underlying concepts and meanings expressed through various linguistic forms, not just literal word matches.

### Dignity Markers
Look for dignity concepts such as:
- Universal pronouns: "all people," "every citizen," "human dignity"
- Individual agency: "personal responsibility," "individual choice," "human potential"  
- Inclusive language: "regardless of," "irrespective of," "common humanity"

*Consider related semantic expressions beyond these specific words - focus on the concept of universal human worth and individual moral agency regardless of the exact language used.*

### Tribalism Markers
Look for tribalism concepts such as:
- Group identifiers: "us vs them," "our people," "real Americans"
- Exclusionary language: "outsiders," "enemies within," "not one of us"
- Loyalty tests: "with us or against us," "true believers," "betrayal"

*Consider related semantic expressions - focus on the concept of group loyalty over universal principles and exclusionary rhetoric regardless of specific terminology.*

### Truth Markers
Look for truth-commitment concepts such as:
- Evidence language: "data shows," "research indicates," "facts demonstrate"
- Complexity acknowledgment: "on the other hand," "however," "it's complicated"
- Intellectual humility: "I could be wrong," "more study needed," "uncertain"

*Consider related semantic expressions - focus on commitment to factual accuracy and intellectual honesty regardless of exact phrasing.*

### Manipulation Markers
Look for manipulation concepts such as:
- Emotional triggers: "outrageous," "shocking," "unbelievable"
- False dichotomies: "only two choices," "either/or," "no middle ground"
- Cognitive bias exploitation: "everyone knows," "obviously," "common sense"

*Consider related semantic expressions - focus on strategic information distortion and emotional manipulation regardless of specific techniques used.*

### Justice Markers
Look for justice concepts such as:
- Fairness language: "equal treatment," "level playing field," "due process"
- Rights protection: "constitutional rights," "civil liberties," "equal protection"
- Systemic thinking: "structural issues," "institutional reform," "systemic change"

*Consider related semantic expressions - focus on concern for fair outcomes and rights protection regardless of exact legal or political terminology.*

### Resentment Markers
Look for resentment concepts such as:
- Grievance language: "they took from us," "we've been wronged," "victims of"
- Blame attribution: "it's their fault," "they caused this," "responsible for our problems"
- Zero-sum framing: "their gain is our loss," "finite resources," "winner takes all"

*Consider related semantic expressions - focus on exploitation of grievances and blame-focused rhetoric regardless of specific targets or language.*

### Hope Markers
Look for hope concepts such as:
- Possibility language: "we can," "together we will," "bright future"
- Empowerment rhetoric: "in our hands," "we have the power," "make it happen"
- Constructive vision: "building," "creating," "improving"

*Consider related semantic expressions - focus on constructive optimism and positive future vision regardless of specific aspirational language used.*

### Fear Markers
Look for fear concepts such as:
- Threat language: "danger," "crisis," "under attack"
- Catastrophic framing: "disaster," "collapse," "end of"
- Security appeals: "protect ourselves," "defend against," "safety first"

*Consider related semantic expressions - focus on anxiety-inducing rhetoric and threat-focused language regardless of specific fears or threats mentioned.*

### Pragmatism Markers
Look for pragmatism concepts such as:
- Constraint acknowledgment: "within our means," "realistic goals," "step by step"
- Problem-solving focus: "practical solutions," "what works," "evidence-based"
- Incremental progress: "gradual improvement," "building on," "next steps"

*Consider related semantic expressions - focus on realistic problem-solving and constraint acknowledgment regardless of specific policy areas or approaches.*

### Fantasy Markers
Look for fantasy concepts such as:
- Magical thinking: "easy solutions," "simple fix," "overnight change"
- Unrealistic promises: "eliminate all," "perfect world," "no more"
- Constraint denial: "money is no object," "unlimited resources," "anything is possible"

*Consider related semantic expressions - focus on unrealistic promises and constraint denial regardless of specific policy areas or promises made.*

## Analysis Methodology

The framework employs sequential chain-of-thought analysis, examining each dimension group independently before integration. This approach improves analytical consistency and evidence quality by focusing attention on specific patterns before synthesis.

## Weighting Scheme

**Dynamic Salience Weighting**: Each dimension receives a salience weight (0.0-1.0) based on its centrality to the specific text being analyzed. This allows the framework to adapt to different types of political discourse while maintaining analytical rigor.

## Calculated Metrics

### Tension Scores
- **Dignity-Tribalism Tension**: (dignity_score + (1 - tribalism_score)) / 2
- **Truth-Manipulation Tension**: (truth_score + (1 - manipulation_score)) / 2  
- **Justice-Resentment Tension**: (justice_score + (1 - resentment_score)) / 2
- **Hope-Fear Tension**: (hope_score + (1 - fear_score)) / 2
- **Pragmatism-Fantasy Tension**: (pragmatism_score + (1 - fantasy_score)) / 2

### Composite Indices
- **Civic Character Index**: Average of all tension scores
- **Salience-Weighted Civic Character Index**: Tension scores weighted by dimension salience
- **Virtue Index**: Average of positive dimension scores (dignity, truth, justice, hope, pragmatism)
- **Pathology Index**: Average of negative dimension scores (tribalism, manipulation, resentment, fear, fantasy)

## Pattern Classifications

### Civic Character Profiles
- **High Civic Character** (≥0.75): Consistent virtue appeals with minimal pathological elements
- **Mixed Character** (0.50-0.74): Balance of virtue and pathology with strategic tensions
- **Low Civic Character** (0.25-0.49): Predominantly pathological appeals with limited virtue
- **Pathological Discourse** (<0.25): Systematic virtue deficits across multiple dimensions

### Strategic Patterns
- **Virtue Signaling** (High virtue scores, low salience): Superficial virtue appeals without substantive commitment
- **Strategic Pathology** (High pathology scores, high salience): Deliberate deployment of divisive rhetoric
- **Authentic Virtue** (High virtue scores, high salience): Genuine commitment to civic ideals
- **Incoherent Messaging** (High variance across dimensions): Inconsistent value appeals

## Reliability and Validity

### Inter-Rater Reliability
Framework designed for high consistency across analysts through:
- Clear operational definitions for each dimension
- Specific linguistic markers and examples
- Sequential analysis methodology
- Explicit confidence reporting requirements

### Construct Validity
Dimensions grounded in established political theory and validated through:
- Classical civic republican literature
- Contemporary political communication research
- Empirical testing across diverse political texts
- Expert review and refinement

## Considerations on Bias

### Potential Sources
- **Ideological Bias**: Analysts' political preferences may influence virtue/pathology assessments
- **Cultural Bias**: Framework developed within Western democratic context
- **Temporal Bias**: Contemporary political norms may not apply to historical texts
- **Selection Bias**: Text sampling may not represent full spectrum of political discourse

### Mitigation Strategies
- **Multi-Analyst Review**: Independent analysis by multiple trained assessors
- **Blind Analysis**: Analysts unaware of speaker identity during assessment
- **Cross-Cultural Validation**: Testing framework across different political systems
- **Longitudinal Consistency**: Regular recalibration using benchmark texts

## Analytical Layers

### Layer 1: Surface Features
Direct textual evidence of virtue/pathology markers through linguistic analysis

### Layer 2: Strategic Intent
Assessment of deliberate rhetorical choices and their civic implications

### Layer 3: Systemic Impact
Evaluation of discourse's contribution to democratic health and civic culture

## Inter-Framework Relationships

**CAF** serves as the foundational civic assessment within the Triadic Architecture:
- **With CHF**: CAF assesses civic virtue while CHF evaluates character heuristics and decision-making patterns
- **With ECF**: CAF focuses on explicit civic appeals while ECF analyzes emotional climate and affective dimensions
- **Synthesis Approach**: Human-led integration of complementary analytical perspectives for comprehensive assessment

<details>
<summary>Machine-Readable Configuration</summary>

```json
{
  "name": "civic_analysis_framework",
  "version": "v7.3",
  "display_name": "Civic Analysis Framework (CAF) v7.3",
  "analysis_variants": {
    "default": {
      "description": "Sequential civic character analysis with chain-of-thought methodology",
      "analysis_prompt": "You are an expert political discourse analyst specializing in civic character assessment. Analyze this text through focused sequential steps, examining each dimension group independently before integration.\n\nSTEP 1 - IDENTITY AXIS ANALYSIS\nFocus ONLY on dignity vs. tribalism patterns (ignore other dimensions for now):\n- Look for dignity patterns: universal pronouns (\"all people,\" \"every citizen\"), individual agency language (\"personal responsibility,\" \"human potential\"), inclusive framing (\"regardless of,\" \"common humanity\") - Note: These are semantic concepts, look for the underlying meaning of universal human worth, not just these exact words\n- Look for tribalism patterns: group identifiers (\"us vs them,\" \"our people\"), exclusionary language (\"outsiders,\" \"enemies within\"), loyalty tests (\"with us or against us\") - Note: These are semantic concepts, look for the underlying meaning of group loyalty over universal principles, not just these exact words\n- Score dignity dimension (0.0-1.0) with specific textual evidence\n- Score tribalism dimension (0.0-1.0) with specific textual evidence\n- Assess salience (0.0-1.0): How central are identity appeals to the overall message?\n- State confidence (0.0-1.0): How certain are you in this assessment?\nShow your analytical work and evidence before proceeding.\n\nSTEP 2 - TRUTH AXIS ANALYSIS\nNow focus ONLY on truth vs. manipulation patterns:\n- Look for truth patterns: evidence language (\"data shows,\" \"research indicates\"), complexity acknowledgment (\"however,\" \"it's complicated\"), intellectual humility (\"I could be wrong\") - Note: These are semantic concepts, look for commitment to factual accuracy and intellectual honesty, not just these exact phrases\n- Look for manipulation patterns: emotional triggers (\"outrageous,\" \"shocking\"), false dichotomies (\"only two choices\"), cognitive bias exploitation (\"everyone knows,\" \"obviously\") - Note: These are semantic concepts, look for strategic information distortion and emotional manipulation, not just these exact techniques\n- Score truth dimension (0.0-1.0) with specific textual evidence\n- Score manipulation dimension (0.0-1.0) with specific textual evidence\n- Assess salience (0.0-1.0): How central are truth/manipulation patterns to the message?\n- State confidence (0.0-1.0): How certain are you in this assessment?\nShow your analytical work and evidence before proceeding.\n\nSTEP 3 - JUSTICE AXIS ANALYSIS\nNow focus ONLY on justice vs. resentment patterns:\n- Look for justice patterns: fairness language (\"equal treatment,\" \"level playing field\"), rights protection (\"constitutional rights,\" \"due process\"), systemic thinking (\"structural issues,\" \"institutional reform\") - Note: These are semantic concepts, look for concern for fair outcomes and rights protection, not just these exact terms\n- Look for resentment patterns: grievance language (\"they took from us,\" \"we've been wronged\"), blame attribution (\"it's their fault\"), zero-sum framing (\"their gain is our loss\") - Note: These are semantic concepts, look for exploitation of grievances and blame-focused rhetoric, not just these exact phrases\n- Score justice dimension (0.0-1.0) with specific textual evidence\n- Score resentment dimension (0.0-1.0) with specific textual evidence\n- Assess salience (0.0-1.0): How central are justice/resentment patterns to the message?\n- State confidence (0.0-1.0): How certain are you in this assessment?\nShow your analytical work and evidence before proceeding.\n\nSTEP 4 - EMOTIONAL AXIS ANALYSIS\nNow focus ONLY on hope vs. fear patterns:\n- Look for hope patterns: possibility language (\"we can,\" \"together we will\"), empowerment rhetoric (\"in our hands,\" \"we have the power\"), constructive vision (\"building,\" \"creating\") - Note: These are semantic concepts, look for constructive optimism and positive future vision, not just these exact expressions\n- Look for fear patterns: threat language (\"danger,\" \"crisis,\" \"under attack\"), catastrophic framing (\"disaster,\" \"collapse\"), security appeals (\"protect ourselves,\" \"defend against\") - Note: These are semantic concepts, look for anxiety-inducing rhetoric and threat-focused language, not just these exact terms\n- Score hope dimension (0.0-1.0) with specific textual evidence\n- Score fear dimension (0.0-1.0) with specific textual evidence\n- Assess salience (0.0-1.0): How central are emotional appeals to the message?\n- State confidence (0.0-1.0): How certain are you in this assessment?\nShow your analytical work and evidence before proceeding.\n\nSTEP 5 - REALITY AXIS ANALYSIS\nNow focus ONLY on pragmatism vs. fantasy patterns:\n- Look for pragmatism patterns: constraint acknowledgment (\"within our means,\" \"realistic goals\"), problem-solving focus (\"practical solutions,\" \"what works\"), incremental progress (\"step by step,\" \"gradual improvement\") - Note: These are semantic concepts, look for realistic problem-solving and constraint acknowledgment, not just these exact approaches\n- Look for fantasy patterns: magical thinking (\"easy solutions,\" \"simple fix\"), unrealistic promises (\"eliminate all,\" \"perfect world\"), constraint denial (\"money is no object,\" \"unlimited resources\") - Note: These are semantic concepts, look for unrealistic promises and constraint denial, not just these exact claims\n- Score pragmatism dimension (0.0-1.0) with specific textual evidence\n- Score fantasy dimension (0.0-1.0) with specific textual evidence\n- Assess salience (0.0-1.0): How central are reality-based vs. fantasy appeals to the message?\n- State confidence (0.0-1.0): How certain are you in this assessment?\nShow your analytical work and evidence before proceeding.\n\nFINAL STEP - INTEGRATION AND VALIDATION\nReview your step-by-step analysis:\n- Check for scoring consistency across all dimension groups\n- Validate that evidence quality meets academic standards\n- Identify strategic tensions between competing virtues (e.g., high dignity + high tribalism)\n- Confirm confidence levels are appropriately calibrated\n- Calculate tension scores and civic character indices\n- Apply pattern classifications based on overall profile\n\nProvide your final structured analysis following this format:\n\n**CIVIC CHARACTER ASSESSMENT**\n\n**Identity Axis**: [dignity score]/[tribalism score] (salience: [score], confidence: [score])\n**Truth Axis**: [truth score]/[manipulation score] (salience: [score], confidence: [score])  \n**Justice Axis**: [justice score]/[resentment score] (salience: [score], confidence: [score])\n**Emotional Axis**: [hope score]/[fear score] (salience: [score], confidence: [score])\n**Reality Axis**: [pragmatism score]/[fantasy score] (salience: [score], confidence: [score])\n\n**Calculated Metrics**:\n- Civic Character Index: [calculated score]\n- Salience-Weighted Index: [calculated score]\n- Pattern Classification: [classification]\n\n**Key Insights**: [Summary of strategic tensions, dominant patterns, and civic implications]"
    }
  },
  "dimension_groups": {
    "identity_axis": ["dignity", "tribalism"],
    "truth_axis": ["truth", "manipulation"],
    "justice_axis": ["justice", "resentment"],
    "emotional_axis": ["hope", "fear"],
    "reality_axis": ["pragmatism", "fantasy"]
  },
  "static_weights": {
    "dignity": 0.20,
    "tribalism": 0.20,
    "truth": 0.20,
    "manipulation": 0.20,
    "justice": 0.20,
    "resentment": 0.20,
    "hope": 0.10,
    "fear": 0.10,
    "pragmatism": 0.15,
    "fantasy": 0.15
  },
  "calculation_spec": {
    "formulas": {
      "dignity_tribalism_tension": "(dignity_score + (1 - tribalism_score)) / 2",
      "truth_manipulation_tension": "(truth_score + (1 - manipulation_score)) / 2",
      "justice_resentment_tension": "(justice_score + (1 - resentment_score)) / 2",
      "hope_fear_tension": "(hope_score + (1 - fear_score)) / 2",
      "pragmatism_fantasy_tension": "(pragmatism_score + (1 - fantasy_score)) / 2",
      "civic_character_index": "(dignity_tribalism_tension + truth_manipulation_tension + justice_resentment_tension + hope_fear_tension + pragmatism_fantasy_tension) / 5",
      "salience_weighted_civic_character_index": "(dignity_tribalism_tension * dignity_salience + truth_manipulation_tension * truth_salience + justice_resentment_tension * justice_salience + hope_fear_tension * hope_salience + pragmatism_fantasy_tension * pragmatism_salience) / (dignity_salience + truth_salience + justice_salience + hope_salience + pragmatism_salience)",
      "virtue_index": "(dignity_score + truth_score + justice_score + hope_score + pragmatism_score) / 5",
      "pathology_index": "(tribalism_score + manipulation_score + resentment_score + fear_score + fantasy_score) / 5"
    },
    "pattern_classifications": {
      "civic_character_profile": {
        "high_civic_character": {"threshold": ">=0.75", "description": "Consistent virtue appeals with minimal pathological elements"},
        "mixed_character": {"threshold": "0.50-0.74", "description": "Balance of virtue and pathology with strategic tensions"},
        "low_civic_character": {"threshold": "0.25-0.49", "description": "Predominantly pathological appeals with limited virtue"},
        "pathological_discourse": {"threshold": "<0.25", "description": "Systematic virtue deficits across multiple dimensions"}
      },
      "strategic_patterns": {
        "virtue_signaling": {"condition": "virtue_index > 0.7 AND avg_virtue_salience < 0.4", "description": "Superficial virtue appeals without substantive commitment"},
        "strategic_pathology": {"condition": "pathology_index > 0.7 AND avg_pathology_salience > 0.6", "description": "Deliberate deployment of divisive rhetoric"},
        "authentic_virtue": {"condition": "virtue_index > 0.7 AND avg_virtue_salience > 0.6", "description": "Genuine commitment to civic ideals"},
        "incoherent_messaging": {"condition": "dimension_variance > 0.3", "description": "Inconsistent value appeals across dimensions"}
      }
    }
  },
  "reporting_metadata": {
    "framework_summary": "Systematic assessment of civic character through virtue-pathology tensions",
    "primary_dimensions": ["dignity", "truth", "justice", "hope", "pragmatism"],
    "key_metrics": ["civic_character_index", "virtue_index", "pathology_index"],
    "bias_considerations": "Framework may reflect Western democratic values; requires multi-analyst validation",
    "reliability_notes": "Designed for high inter-rater consistency through sequential methodology"
  },
  "output_contract": {
    "raw_analysis_log_structure": {
      "step_1_identity": "Dignity vs. tribalism analysis with scores, salience, confidence, and evidence",
      "step_2_truth": "Truth vs. manipulation analysis with scores, salience, confidence, and evidence", 
      "step_3_justice": "Justice vs. resentment analysis with scores, salience, confidence, and evidence",
      "step_4_emotional": "Hope vs. fear analysis with scores, salience, confidence, and evidence",
      "step_5_reality": "Pragmatism vs. fantasy analysis with scores, salience, confidence, and evidence",
      "final_integration": "Calculated metrics, pattern classifications, and civic character assessment"
    },
    "instructions": "Follow the sequential analysis format exactly. Each step must include specific textual evidence, numerical scores (0.0-1.0), salience assessment, and confidence rating. Final integration must calculate all tension scores and apply pattern classifications."
  },
  "gasket_schema": {
    "version": "7.3",
    "extraction_method": "intelligent_extractor",
    "target_keys": [
      "dignity_score", "tribalism_score", "dignity_salience", "tribalism_salience", "dignity_confidence", "tribalism_confidence",
      "truth_score", "manipulation_score", "truth_salience", "manipulation_salience", "truth_confidence", "manipulation_confidence",
      "justice_score", "resentment_score", "justice_salience", "resentment_salience", "justice_confidence", "resentment_confidence",
      "hope_score", "fear_score", "hope_salience", "fear_salience", "hope_confidence", "fear_confidence",
      "pragmatism_score", "fantasy_score", "pragmatism_salience", "fantasy_salience", "pragmatism_confidence", "fantasy_confidence"
    ],
    "extraction_patterns": {
      "dignity_score": ["dignity.*?score.*?([0-9]\\.[0-9])", "dignity.*?([0-9]\\.[0-9])", "dignity\\s*:\\s*([0-9]\\.[0-9])"],
      "tribalism_score": ["tribalism.*?score.*?([0-9]\\.[0-9])", "tribalism.*?([0-9]\\.[0-9])", "tribalism\\s*:\\s*([0-9]\\.[0-9])"],
      "dignity_salience": ["dignity.*?salience.*?([0-9]\\.[0-9])", "salience.*?([0-9]\\.[0-9]).*?dignity"],
      "tribalism_salience": ["tribalism.*?salience.*?([0-9]\\.[0-9])", "salience.*?([0-9]\\.[0-9]).*?tribalism"],
      "dignity_confidence": ["dignity.*?confidence.*?([0-9]\\.[0-9])", "confidence.*?([0-9]\\.[0-9]).*?dignity"],
      "tribalism_confidence": ["tribalism.*?confidence.*?([0-9]\\.[0-9])", "confidence.*?([0-9]\\.[0-9]).*?tribalism"]
    },
    "validation_rules": {
      "required_fields": ["dignity_score", "tribalism_score", "truth_score", "manipulation_score", "justice_score", "resentment_score", "hope_score", "fear_score", "pragmatism_score", "fantasy_score"],
      "score_ranges": {"min": 0.0, "max": 1.0},
      "metadata_ranges": {
        "salience": {"min": 0.0, "max": 1.0},
        "confidence": {"min": 0.0, "max": 1.0}
      },
      "fallback_strategy": "use_default_values"
    }
  }
}
```

</details>