# Populist Discourse Analysis Framework (PDAF) v10.0.0

---

## Part 1: The Scholarly Document

### Section 1: Abstract & *Raison d'être*

**What is this framework?**
The Populist Discourse Analysis Framework (PDAF) is a comprehensive analytical tool designed to identify, measure, and analyze the core rhetorical components of populist political communication through advanced strategic tension analysis and salience-weighted measurement.

**What problem does it solve?**
Populism has emerged as one of the most consequential political phenomena of the 21st century, reshaping democratic politics across the globe from Brexit to Trump, from Bolsonaro to Modi. Yet despite its profound impact, the systematic measurement of populist discourse remains fragmented and inconsistent across academic disciplines. Traditional populism analysis suffers from three fundamental limitations: ideological bias (focusing only on right-wing or left-wing variants), binary classification (populist vs. non-populist), and static measurement (ignoring rhetorical emphasis patterns). 

The PDAF addresses this critical gap by providing the first comprehensive, cross-ideological framework for quantifying populist rhetorical patterns through innovative **populist strategic tension analysis** that captures the sophisticated ways speakers deploy populist appeals with varying emphasis and internal contradictions.

**Who is it for?**
This framework is intended for political scientists, communication researchers, journalists, and civic organizations who need to track and understand the prevalence, nature, and strategic coherence of populist discourse in speeches, manifestos, social media, and other political texts.

### Section 2: Theoretical & Empirical Foundations

The PDAF builds on foundational populism research (Mudde, 2004; Müller, 2016), political communication theory (Moffitt, 2016), and democratic theory (Urbinati, 2019). Each analytical dimension is grounded in comparative populism studies and cross-national empirical research on populist discourse patterns.

**Theoretical Innovation: Cross-Ideological Populist Strategic Tension Analysis**

Traditional populism measurement treats populist appeals as ideologically neutral phenomena (Mudde, 2004) but fails to capture the strategic sophistication of populist communication. Recent research demonstrates that populist leaders often employ contradictory appeals within single speeches—what scholars term "populist strategic contradictions" (Hawkins et al., 2019; Rooduijn et al., 2019).

The PDAF's tension analysis addresses this gap by measuring not just the presence of populist appeals, but their strategic deployment patterns and internal contradictions. This innovation enables researchers to distinguish between coherent populist messaging and strategic overreach that may confuse audiences or undermine populist effectiveness.

**Key Citations**:
- **Foundational Populism Theory**: Mudde, C. (2004). The populist zeitgeist. *Government and Opposition*, 39(4), 541-563.
- **Comparative Populism Studies**: Hawkins, K. A., Carlin, R. E., Littvay, L., & Kaltwasser, C. R. (Eds.). (2019). *The Ideational Approach to Populism*. London: Routledge.
- **Political Communication Theory**: Moffitt, B. (2016). *The Global Rise of Populism*. Stanford University Press.
- **Democratic Theory**: Urbinati, N. (2019). *Me the People: How Populism Transforms Democracy*. Cambridge, MA: Harvard University Press.

### Section 3: Analytical Methodology

The PDAF employs a multi-layered analytical approach with **nine core dimensions** organized into three theoretically grounded categories, plus advanced **salience-weighted analysis** and **populist strategic tension mathematics**.

**Core Innovation**: PDAF introduces cross-ideological populist measurement with salience-weighted tension analysis, enabling researchers to distinguish between coherent populist strategies and strategic overreach where speakers attempt contradictory populist appeals simultaneously.

**Dimensions**: The framework evaluates populist discourse across nine dimensions organized into three categories, employing a standard 0.0-1.0 scale for consistent measurement across the Discernus platform:

**Primary Populist Core Anchors** (Based on Mudde's minimal definition and Müller's anti-pluralist theory):
1. **Manichaean People-Elite Framing** (0.0-1.0): Moral dichotomy between pure, virtuous people and corrupt, self-serving elites
2. **Crisis-Restoration Temporal Narrative** (0.0-1.0): Decline-crisis-redemption temporal structuring where current crisis stems from elite betrayal
3. **Popular Sovereignty Claims** (0.0-1.0): Direct people's will as ultimate political authority, bypassing representative institutions
4. **Anti-Pluralist Exclusion** (0.0-1.0): Rejection of legitimate opposition and institutional constraints on popular will

**Populist Mechanism Anchors** (Grounded in mobilization and representation theories):
5. **Elite Conspiracy/Systemic Corruption** (0.0-1.0): Elite coordination against people's interests through hidden networks or institutional capture
6. **Authenticity vs. Political Class** (0.0-1.0): Genuine representation versus professional politician artifice
7. **Homogeneous People Construction** (0.0-1.0): Unified people identity transcending internal divisions of class, region, or interest

**Boundary Distinction Anchors** (Based on exclusion mechanisms and boundary-drawing research):
8. **Nationalist Exclusion** (0.0-1.0): Cultural/ethnic homogeneity and external threat emphasis that defines populist community boundaries
9. **Economic Populist Appeals** (0.0-1.0): Populist economic discourse regardless of ideological direction

**Advanced Analytical Features**:
- **Salience-Weighted Analysis**: Captures not just populist intensity but rhetorical emphasis patterns (0.0-1.0 salience scoring)
- **Populist Strategic Tension Mathematics**: Quantifies contradictory populist appeals using the formula: `Tension = min(Anchor_A_score, Anchor_B_score) × |Anchor_A_salience - Anchor_B_salience|`
- **Populist Strategic Contradiction Index (PSCI)**: Overall measure of strategic coherence vs. contradiction across tension pairs. The PSCI is calculated directly from base dimensions to ensure numerical stability and avoid dependency chaining between derived metrics. This robust implementation provides the same mathematical result as averaging the three tension metrics but with enhanced computational reliability.

**Salience-Weighted Indices**: These metrics account for both the intensity and rhetorical prominence of populist dimensions:

- **Salience-Weighted Core Populism Index**: `(Manichaean × Salience + Crisis-Restoration × Salience + Popular Sovereignty × Salience + Anti-Pluralist × Salience) / (Total Salience + 0.001)`
- **Salience-Weighted Populism Mechanisms Index**: `(Elite Conspiracy × Salience + Authenticity × Salience + Homogeneous People × Salience) / (Total Salience + 0.001)`
- **Salience-Weighted Boundary Distinctions Index**: `(Nationalist Exclusion × Salience + Economic Populist × Salience) / (Total Salience + 0.001)`
- **Salience-Weighted Overall Populism Index**: `(All Dimensions × Salience) / (Total Salience + 0.001)`

**Note**: The `+ 0.001` term prevents division-by-zero errors in cases where total salience might be zero, ensuring numerical stability.

- **Standard 0.0-1.0 Scale**: Provides consistent measurement compatible with the Discernus platform

**Scoring Calibration Guidelines**:

The PDAF employs a 0.0-1.0 scale for raw scores and 0.0-1.0 for salience and confidence. For detailed, dimension-specific scoring calibration that provides precise guidance for each dimension, refer to the machine-readable appendix in Section 5.3, which contains comprehensive calibration examples for all nine dimensions.

**Examples and Anti-Examples**:

**Manichaean People-Elite Framing**:
- ✅ **Positive**: "The corrupt political establishment has betrayed the American people" - explicit moral dichotomy between virtuous people and corrupt elites
- ❌ **Negative**: "Some politicians are dishonest" - generic criticism without elite framing or moral dichotomy
- ⚠️ **Boundary**: "The ruling class" - context-dependent for corruption vs. leadership distinction

**Crisis-Restoration Narrative**:
- ✅ **Positive**: "We face a national emergency that requires immediate action" - crisis language with urgency and restoration promise
- ❌ **Negative**: "We have challenges to address" - problems without crisis framing or restoration narrative
- ⚠️ **Boundary**: "This is a serious issue" - depends on urgency and restoration promises for full crisis-restoration structure

**Popular Sovereignty Claims**:
- ✅ **Positive**: "The people's will must prevail over institutional obstacles" - direct popular authority as ultimate political source
- ❌ **Negative**: "Democracy is important" - institutional focus without direct popular authority claims
- ⚠️ **Boundary**: "The people have spoken" - depends on context for sovereignty vs. electoral results interpretation

**Anti-Pluralist Exclusion**:
- ✅ **Positive**: "The opposition are enemies of the people" - explicit opposition rejection and legitimacy denial
- ❌ **Negative**: "We disagree with their policies" - policy disagreement without opposition rejection
- ⚠️ **Boundary**: "Strong opposition" - depends on whether it implies rejection vs. recognition of legitimate opposition

**Elite Conspiracy/Systemic Corruption**:
- ✅ **Positive**: "The elites are secretly coordinating against us" - explicit conspiracy claims and systemic corruption emphasis
- ❌ **Negative**: "Some politicians are corrupt" - individual corruption without coordination claims
- ⚠️ **Boundary**: "Systemic problems" - depends on whether it implies coordination vs. dysfunction

**Authenticity vs. Political Class**:
- ✅ **Positive**: "I'm not a politician, I'm a real person" - authenticity claims vs. political class positioning
- ❌ **Negative**: "I have experience in government" - professional qualification without anti-establishment positioning
- ⚠️ **Boundary**: "New to politics" - depends on whether it implies authenticity vs. inexperience

**Homogeneous People Construction**:
- ✅ **Positive**: "We are one people, united and indivisible" - explicit unity construction and homogeneity emphasis
- ❌ **Negative**: "Our community has diverse views" - group acknowledgment without unity claims
- ⚠️ **Boundary**: "Together" - depends on whether it implies unity vs. cooperation

**Nationalist Exclusion**:
- ✅ **Positive**: "Our culture is under threat from foreign influences" - cultural exclusion claims and external threat emphasis
- ❌ **Negative**: "We're proud of our heritage" - pride without exclusion or threat framing
- ⚠️ **Boundary**: "Our heritage" - depends on whether it implies exclusion vs. celebration

**Economic Populist Appeals**:
- ✅ **Positive**: "The economic elite has rigged the system against us" - economic elite framing with populist economic rhetoric
- ❌ **Negative**: "Economic growth is important" - performance focus without populist appeals
- ⚠️ **Boundary**: "Economic reform" - depends on whether it implies populist vs. technocratic approach

**Note**: For comprehensive, dimension-specific scoring calibration with precise examples for each dimension, refer to the machine-readable appendix in Section 5.3, which contains the definitive calibration guidelines used by the analysis agents.

### Section 4: Intended Application & Corpus Fit

**Target Corpus Description**: The PDAF is designed for the analysis of formal political communication, including but not limited to: political speeches, party manifestos, candidate debates, and official social media pronouncements. It is most effective on texts where a clear political argument is being made.

**Known Limitations & Scope**: This framework is not intended for analyzing conversational speech, private correspondence, or texts that lack a persuasive political intent. Its effectiveness may be limited on highly ironic or satirical content. The framework requires careful contextual interpretation, particularly for boundary distinction anchors.

**System Validation Note**: Be aware that the Discernus platform will perform automated statistical validation of this framework's fit with your chosen corpus. Applying it to a corpus of, for example, scientific articles would likely result in a validation failure.

---

## Part 2: The Machine-Readable Appendix

```yaml
# --- Start of Machine-Readable Appendix ---

# 5.1: Metadata
metadata:
  framework_name: "populist_discourse_analysis_framework"
  framework_version: "10.0.0"
  author: "Discernus Project"
  spec_version: "10.0"

# 5.2: Analysis Variants
analysis_variants:
  default:
    description: "Provides a comprehensive, single-pass analysis of all nine populist dimensions for a holistic overview. This variant is ideal for initial exploration and overall assessment. For highest quality results with focused attention on specific dimension groups, use the sequential analysis variants below."
    analysis_prompt: |
      You are an expert populist discourse analyst with deep understanding of populist rhetorical strategies across different political contexts. Your task is to analyze the provided text using the Populist Discourse Analysis Framework (PDAF) v10.0, which measures populist discourse patterns through nine core anchors with enhanced metadata reporting and strategic tension analysis.

      THEORETICAL GROUNDING: The PDAF is grounded in the ideational approach to populism (Mudde, 2004) that defines populism as a "thin-centered ideology" positing antagonism between virtuous "people" and corrupt "elite." This framework extends beyond basic populism detection to measure strategic coherence and rhetorical emphasis patterns.

      ANALYTICAL APPROACH: The PDAF measures populism as a "thin-centered ideology" that posits antagonism between virtuous "people" and corrupt "elite." Each dimension should be scored independently based on textual evidence, with careful attention to both intensity and salience.

      CONTEXTUAL GUIDANCE: 
      - In political speeches, emphasize rhetorical strategies and audience appeals
      - Look for structural positioning (opening/closing statements carry higher salience)
      - Consider repetition patterns as indicators of rhetorical emphasis
      - Distinguish between policy content and rhetorical strategy

      SALIENCE ASSESSMENT: 
      Salience measures rhetorical prominence, not intensity. Consider:
      - Frequency and repetition patterns throughout the text
      - Structural positioning (opening, closing, thesis statements)
      - Thematic centrality to the overall message
      - Rhetorical devices used for emphasis (metaphors, imagery, emotional appeals)
      SALIENCE ≠ INTENSITY. A dimension can have high intensity (e.g., 0.9) but low salience (e.g., 0.2) if it's just a passing mention, or moderate intensity (e.g., 0.5) but high salience (e.g., 0.9) if it is the central theme of the text.

      For each of the nine dimensions, provide:
      - **Score (0.0-1.0)**: Based on strength of evidence in the text
      - **Salience (0.0-1.0)**: How central is this dimension to this specific text?
      - **Confidence (0.0-1.0)**: How certain are you in this assessment?
      - **Evidence**: Direct quote supporting your assessment

      Your analysis should focus on evaluating each dimension according to the PDAF methodology, providing clear reasoning for scores, salience, and confidence assessments, and identifying key textual evidence that supports your dimensional assessments.
      
      **Note**: For highest quality results with focused attention on specific dimension groups, use the sequential analysis variants below.



  # Sequential analysis variants for improved accuracy (recommended approach)
  sequential_core_anchors:
    description: "Focus on Primary Populist Core Anchors: Manichaean People-Elite Framing, Crisis-Restoration Narrative, Popular Sovereignty Claims, Anti-Pluralist Exclusion."
    analysis_prompt: |
      You are an expert populist discourse analyst specializing in core populist appeals and democratic theory. Focus exclusively on evaluating the Primary Populist Core Anchors in the provided text using the Populist Discourse Analysis Framework v10.0.

      DIMENSIONAL FOCUS: Primary Populist Core Anchors Only
      - Manichaean People-Elite Framing: Moral dichotomy between pure people and corrupt elites
      - Crisis-Restoration Temporal Narrative: Decline-crisis-redemption temporal structuring
      - Popular Sovereignty Claims: Direct people's will as ultimate political authority
      - Anti-Pluralist Exclusion: Rejection of legitimate opposition and institutional constraints

      CORE-ANCHOR-SPECIFIC GUIDANCE:
      - Look for fundamental us-vs-them rhetorical structures
      - Assess temporal crisis narratives and restoration promises
      - Distinguish between democratic appeals and anti-pluralist exclusion
      - Focus on the basic populist antagonistic relationship

      CRITICAL DISTINCTIONS:
      - "Manichaean People-Elite Framing" measures moral dichotomy, not just criticism
      - "Crisis-Restoration" requires temporal decline narrative, not just problems
      - "Popular Sovereignty" focuses on direct democracy, not just people references
      - "Anti-Pluralist Exclusion" measures opposition rejection, not just disagreement

      Provide raw_score (0.0-1.0), salience (0.0-1.0), evidence, and confidence (0.0-1.0) for ALL FOUR dimensions.

  sequential_mechanism_anchors:
    description: "Focus on Populist Mechanism Anchors: Elite Conspiracy/Systemic Corruption, Authenticity vs. Political Class, Homogeneous People Construction."
    analysis_prompt: |
      You are an expert populist discourse analyst specializing in populist mobilization and representation strategies. Focus exclusively on evaluating the Populist Mechanism Anchors in the provided text using the Populist Discourse Analysis Framework v10.0.

      DIMENSIONAL FOCUS: Populist Mechanism Anchors Only
      - Elite Conspiracy/Systemic Corruption: Elite coordination against people's interests
      - Authenticity vs. Political Class: Genuine representation vs. professional politician artifice
      - Homogeneous People Construction: Unified people identity transcending internal divisions

      MECHANISM-SPECIFIC GUIDANCE:
      - Look for conspiracy theories and systemic corruption claims
      - Assess authenticity claims and anti-establishment positioning
      - Distinguish between group loyalty and homogeneous people construction
      - Focus on mobilization mechanisms rather than policy positions

      CRITICAL DISTINCTIONS:
      - "Elite Conspiracy" requires coordination claims, not just criticism
      - "Authenticity" measures anti-establishment positioning, not just honesty
      - "Homogeneous People" requires unity construction, not just group references

      Provide raw_score (0.0-1.0), salience (0.0-1.0), evidence, and confidence (0.0-1.0) for ALL THREE dimensions.

  sequential_boundary_anchors:
    description: "Focus on Boundary Distinction Anchors: Nationalist Exclusion, Economic Populist Appeals."
    analysis_prompt: |
      You are an expert populist discourse analyst specializing in populist boundary-drawing and economic rhetoric. Focus exclusively on evaluating the Boundary Distinction Anchors in the provided text using the Populist Discourse Analysis Framework v10.0.

      DIMENSIONAL FOCUS: Boundary Distinction Anchors Only
      - Nationalist Exclusion: Cultural/ethnic homogeneity and external threat emphasis
      - Economic Populist Appeals: Populist economic discourse regardless of ideological direction

      BOUNDARY-SPECIFIC GUIDANCE:
      - Look for cultural/ethnic boundary-drawing and external threat language
      - Assess economic grievance framing and populist economic appeals
      - Distinguish between policy positions and populist economic rhetoric
      - Focus on boundary mechanisms rather than specific policy content

      CRITICAL DISTINCTIONS:
      - "Nationalist Exclusion" requires boundary-drawing, not just patriotism
      - "Economic Populist Appeals" measures populist framing, not just economic policy

      Provide raw_score (0.0-1.0), salience (0.0-1.0), evidence, and confidence (0.0-1.0) for BOTH dimensions.

# 5.3: Dimensions
dimensions:
  - name: "manichaean_people_elite_framing"
    description: "Moral dichotomy between pure, virtuous people and corrupt, self-serving elites."
    markers:
      positive_examples:
        - phrase: "collective ownership claims vs. elite capture patterns"
          explanation: "Rhetorical structures that position political systems/resources as rightfully belonging to 'all people' while being wrongfully controlled by small elite groups"
        - phrase: "elite power center identification"
          explanation: "Specific naming of institutional centers (financial, political, media) as antagonistic to popular interests rather than neutral policy actors"
        - phrase: "moral corruption attributions"
          explanation: "Direct assignment of moral corruption rather than policy disagreement or competence issues"
        - phrase: "people virtue construction"
          explanation: "Characterization of ordinary citizens/voters as inherently virtuous, honest, or morally superior"
        - phrase: "binary opposition framing"
          explanation: "Clear dichotomous positioning with no middle ground between people and elite camps"
        - phrase: "systemic manipulation claims"
          explanation: "Assertions that entire systems are deliberately structured to benefit elites at popular expense"
        - phrase: "establishment as corruption metaphor"
          explanation: "Metaphorical language that equates political institutions with moral decay or contamination"
      negative_examples:
        - phrase: "policy-focused critiques without moral framing"
          explanation: "Technical or procedural criticism that addresses specific policies or behaviors without invoking broader moral conflicts between groups"
        - phrase: "institutional disagreement without delegitimization"
          explanation: "Opposition expressed through legitimate political channels without questioning the moral standing of opponents"
        - phrase: "competence-based criticism"
          explanation: "Performance evaluation that focuses on effectiveness rather than moral character or systemic corruption"
      boundary_cases:
        - phrase: "out of touch"
          explanation: "depends on whether it implies moral corruption vs. disconnect"
    scoring_calibration:
      maximum: "0.9-1.0: Maximum moral dichotomy, overwhelming us-vs-them rhetoric, explicit corruption claims"
      high: "0.7-0.8: Strong moral dichotomy, clear us-vs-them rhetoric, explicit corruption claims"
      medium: "0.5-0.6: Moderate people-elite framing, some moral contrast, implied corruption"
      weak: "0.3-0.4: Weak people-elite hints, minimal moral dichotomy"
      minimal: "0.1-0.2: Very weak moral hints, barely detectable opposition"
      absent: "0.0: No people-elite moral dichotomy or corruption claims"
    disambiguation:
      overlap_with_anti_pluralist: "Both dimensions can be present; score each independently based on textual evidence"

  - name: "crisis_restoration_narrative"
    description: "Decline-crisis-redemption temporal structuring where current crisis stems from elite betrayal."
    markers:
      positive_examples:
        - phrase: "decline-from-past-greatness narrative structure"
          explanation: "Temporal framing that positions current conditions as deteriorated from a superior historical state, establishing foundational crisis premise"
        - phrase: "restoration promise rhetoric"
          explanation: "Forward-looking claims that explicitly or implicitly promise return to previous superior state, completing the decline-crisis-redemption arc"
        - phrase: "critical juncture framing"
          explanation: "Present moment characterized as decisive crossroads requiring urgent action to prevent catastrophe or enable restoration"
        - phrase: "crisis urgency markers"
          explanation: "Language intensity indicators that elevate normal problems to existential threat levels requiring immediate response"
        - phrase: "catastrophe threshold language"
          explanation: "Positioning current situation at or near point of irreversible disaster, maximizing urgency for corrective action"
        - phrase: "breaking point terminology"
          explanation: "Indicators that current conditions have reached unsustainable crisis threshold requiring dramatic intervention"
        - phrase: "recovery and reclamation rhetoric"
          explanation: "Language patterns that frame political action as retrieving or restoring something previously possessed but lost"
      negative_examples:
        - phrase: "continuous improvement framing"
          explanation: "Positioning issues as ongoing work or development rather than crisis requiring urgent restoration to previous state"
        - phrase: "difficulty without crisis escalation"
          explanation: "Acknowledgment of problems that maintains proportional response rather than elevating to existential threat level"
        - phrase: "issue-based problem-solving"
          explanation: "Specific problem identification without temporal decline narrative or restoration promises"
      boundary_cases:
        - phrase: "serious issue"
          explanation: "depends on urgency and crisis framing"
    scoring_calibration:
      maximum: "0.9-1.0: Maximum crisis narrative, overwhelming decline-restoration structure, urgent restoration promises"
      high: "0.7-0.8: Strong crisis narrative, clear decline-restoration structure, urgent restoration promises"
      medium: "0.5-0.6: Moderate crisis language, some decline narrative, restoration hints"
      weak: "0.3-0.4: Weak crisis hints, minimal decline-restoration structure"
      minimal: "0.1-0.2: Very weak crisis hints, barely detectable decline-restoration"
      absent: "0.0: No crisis narrative, decline language, or restoration promises"
    disambiguation:
      vs_elite_conspiracy: "Crisis-restoration focuses on temporal narrative; elite conspiracy focuses on causal attribution"

  - name: "popular_sovereignty_claims"
    description: "Direct people's will as ultimate political authority, bypassing representative institutions."
    markers:
      positive_examples:
        - phrase: "unmediated popular authority claims"
          explanation: "Positioning expressed popular will as ultimate political authority requiring immediate compliance without institutional mediation"
        - phrase: "institutional bypass rhetoric"
          explanation: "Language advocating circumvention of representative institutions in favor of direct popular decision-making"
        - phrase: "popular will primacy assertions"
          explanation: "Rhetorical elevation of popular preferences above institutional processes, competing interests, or constitutional constraints"
        - phrase: "direct democracy invocations"
          explanation: "Appeals to immediate popular decision-making that bypass representative democratic structures"
        - phrase: "majoritarianism without constraints"
          explanation: "Popular decision-making claims that reject institutional limits on majority power"
        - phrase: "institution-bypassing formulations"
          explanation: "Rhetorical patterns that advocate going around established democratic procedures to reach 'the people' directly"
        - phrase: "popular decision supremacy rhetoric"
          explanation: "Language positioning popular choice as final authority that cannot be legitimately questioned or constrained"
      negative_examples:
        - phrase: "institutional cooperation emphasis"
          explanation: "Rhetorical focus on working within established democratic structures and procedures rather than bypassing them"
        - phrase: "representative democracy framing"
          explanation: "Language supporting institutional mediation and representative structures without direct popular authority claims"
        - phrase: "constitutional process respect"
          explanation: "Acknowledgment of institutional constraints and procedural requirements rather than popular will supremacy"
      boundary_cases:
        - phrase: "people's choice"
          explanation: "depends on whether it implies direct vs. representative democracy"
    scoring_calibration:
      maximum: "0.9-1.0: Maximum popular sovereignty claims, overwhelming direct democracy language, institution bypassing"
      high: "0.7-0.8: Strong popular sovereignty claims, clear direct democracy language, institution bypassing"
      medium: "0.5-0.6: Moderate popular authority, some direct democracy, limited institution bypassing"
      weak: "0.3-0.4: Weak popular sovereignty hints, minimal direct democracy language"
      minimal: "0.1-0.2: Very weak popular sovereignty hints, barely detectable direct democracy"
      absent: "0.0: No popular sovereignty claims, direct democracy language, or institution bypassing"
    disambiguation:
      vs_anti_pluralist: "Popular sovereignty focuses on direct democracy; anti-pluralist focuses on opposition rejection"

  - name: "anti_pluralist_exclusion"
    description: "Rejection of legitimate opposition and institutional constraints on popular will."
    markers:
      positive_examples:
        - phrase: "opposition legitimacy denial"
          explanation: "Rhetorical rejection of political opponents' right to participate in democratic discourse by questioning their basic legitimacy"
        - phrase: "compromise rejection through demonization"
          explanation: "Refusal to engage institutional norms of negotiation by characterizing opponents as existential threats rather than legitimate disagreement"
        - phrase: "identity-based political exclusion"
          explanation: "Delegitimization of opposition through claims they don't belong to authentic political community based on cultural/national identity"
        - phrase: "existential threat characterization"
          explanation: "Framing political opponents as fundamental dangers to the nation/people rather than legitimate policy alternatives"
        - phrase: "legitimacy denial rhetoric"
          explanation: "Language patterns that question opponents' right to political participation rather than just disagreeing with positions"
        - phrase: "opponent demonization strategies"
          explanation: "Rhetorical patterns that characterize political opposition as evil, traitorous, or fundamentally un-American/anti-popular"
        - phrase: "institutional constraint rejection"
          explanation: "Refusal to accept democratic norms of compromise, negotiation, or power-sharing that limit winner authority"
        - phrase: "zero-sum victory rhetoric"
          explanation: "Language positioning electoral success as mandate for total exclusion of opposition voices from legitimate political influence"
      negative_examples:
        - phrase: "respectful disagreement with legitimacy affirmation"
          explanation: "Opposition framing that explicitly acknowledges opponents' right to participate in democratic process while disagreeing with positions"
        - phrase: "policy-focused opposition"
          explanation: "Disagreement centered on specific policies or approaches without questioning opponents' fundamental right to hold different views"
        - phrase: "institutional resistance without delegitimization"
          explanation: "Opposition expressed through legitimate democratic channels without challenging opponents' basic political standing"
      boundary_cases:
        - phrase: "strong opposition"
          explanation: "depends on whether it implies rejection vs. recognition"
    scoring_calibration:
      maximum: "0.9-1.0: Maximum opposition rejection, overwhelming legitimacy denial, exclusionary language"
      high: "0.7-0.8: Strong opposition rejection, clear legitimacy denial, exclusionary language"
      medium: "0.5-0.6: Moderate opposition rejection, some legitimacy denial, limited exclusion"
      weak: "0.3-0.4: Weak opposition rejection hints, minimal exclusionary language"
      minimal: "0.1-0.2: Very weak opposition rejection hints, barely detectable exclusion"
      absent: "0.0: No opposition rejection, legitimacy denial, or exclusionary language"
    disambiguation:
      vs_popular_sovereignty: "Anti-pluralist focuses on opposition rejection; popular sovereignty focuses on direct democracy"

  - name: "elite_conspiracy_systemic_corruption"
    description: "Elite coordination against people's interests through hidden networks or institutional capture."
    markers:
      positive_examples:
        - phrase: "hidden elite coordination claims"
          explanation: "Assertions that political outcomes result from secret coordination among elite actors rather than transparent democratic processes"
        - phrase: "institutional systematic deception"
          explanation: "Characterization of key institutions (media, government, etc.) as deliberately misleading public as part of coordinated elite strategy"
        - phrase: "elite exploitation conspiracy rhetoric"
          explanation: "Direct accusations of coordinated elite exploitation of vulnerable populations for personal/group gain rather than individual misconduct"
        - phrase: "explicit coordination conspiracy claims"
          explanation: "Direct assertions of secret elite cooperation and coordination against public interest"
        - phrase: "systemic manipulation assertions"
          explanation: "Claims that entire political/economic systems are deliberately structured by elite coordination to disadvantage ordinary people"
        - phrase: "hidden network operation rhetoric"
          explanation: "Language suggesting secret elite networks operating behind public view to control political/economic outcomes"
        - phrase: "establishment coordination accusations"
          explanation: "Claims that establishment institutions work together in coordinated fashion against popular interests"
        - phrase: "shadow power structure assertions"
          explanation: "References to hidden elite power structures that secretly control visible political institutions"
      negative_examples:
        - phrase: "individual misconduct accusations"
          explanation: "Criticism focused on specific individuals' unethical behavior without suggesting broader coordinated conspiracy or systemic elite coordination"
        - phrase: "isolated corruption claims"
          explanation: "References to corruption that treat it as individual moral failing rather than evidence of broader elite coordination patterns"
        - phrase: "competence-based institutional criticism"
          explanation: "Criticism of institutional performance that focuses on effectiveness or incompetence rather than coordinated conspiracy"
      boundary_cases:
        - phrase: "systemic problems"
          explanation: "depends on whether it implies coordination vs. dysfunction"
    scoring_calibration:
      high: "0.8-1.0: Strong conspiracy claims, clear systemic corruption, hidden coordination language"
      medium: "0.5-0.7: Moderate conspiracy hints, some systemic corruption, limited coordination claims"
      low: "0.1-0.4: Weak conspiracy hints, minimal systemic corruption language"
      absent: "0.0: No conspiracy claims, systemic corruption, or coordination language"
    disambiguation:
      vs_manichaean: "Elite conspiracy focuses on coordination; manichaean focuses on moral dichotomy"
      vs_crisis_restoration: "Elite conspiracy focuses on causal attribution; crisis-restoration focuses on temporal narrative structure"

  - name: "authenticity_vs_political_class"
    description: "Genuine representation versus professional politician artifice."
    markers:
      positive_examples:
        - phrase: "anti-political class identity claims"
          explanation: "Explicit positioning of speaker identity in opposition to professional political class membership through authenticity contrasts"
        - phrase: "authenticity-as-opposition rhetoric"
          explanation: "Framing personal authenticity as inherent contrast with professional political class, implying their dishonesty or artifice"
        - phrase: "insider-outsider authenticity distinctions"
          explanation: "Rhetorical construction of authentic popular identity versus inauthentic political establishment based on genuine experience"
        - phrase: "ordinary person positioning"
          explanation: "Self-characterization emphasizing common citizenship rather than professional political credentials or experience"
        - phrase: "anti-establishment identity construction"
          explanation: "Speaker positioning that explicitly rejects or opposes identification with professional political class"
        - phrase: "outsider status claims"
          explanation: "Rhetorical emphasis on speaker's position outside professional political networks or establishment structures"
        - phrase: "genuine representation assertions"
          explanation: "Claims that speaker provides authentic representation in contrast to artificial or self-interested political professionals"
        - phrase: "common citizen identification"
          explanation: "Speaker positioning that emphasizes shared identity with ordinary voters rather than political elite status"
      negative_examples:
        - phrase: "professional credential emphasis"
          explanation: "Rhetorical focus on qualifications, experience, and competence rather than authenticity-based opposition to political class"
        - phrase: "institutional experience valorization"
          explanation: "Positive framing of professional political experience without anti-establishment positioning or authenticity claims"
        - phrase: "competence-based qualifications"
          explanation: "Appeals based on capability and expertise rather than authentic identity opposition to professional political class"
      boundary_cases:
        - phrase: "new to politics"
          explanation: "depends on whether it implies authenticity vs. inexperience"
    scoring_calibration:
      high: "0.8-1.0: Strong authenticity claims, clear anti-political class positioning, outsider identity"
      medium: "0.5-0.7: Moderate authenticity, some anti-establishment, limited outsider claims"
      low: "0.1-0.4: Weak authenticity hints, minimal anti-political class language"
      absent: "0.0: No authenticity claims, anti-establishment positioning, or outsider identity"
    disambiguation:
      vs_elite_conspiracy: "Authenticity focuses on personal identity; elite conspiracy focuses on coordination claims"
      vs_manichaean: "Authenticity focuses on personal positioning; manichaean focuses on moral dichotomy between groups"

  - name: "homogeneous_people_construction"
    description: "Unified people identity transcending internal divisions of class, region, or interest."
    markers:
      positive_examples:
        - phrase: "unified virtuous people construction"
          explanation: "Rhetorical positioning of 'the people' as single, morally superior entity with shared destiny and collective agency transcending internal differences"
        - phrase: "explicit unity assertions"
          explanation: "Direct claims about fundamental unity of popular identity that erases or transcends class, regional, or interest divisions"
        - phrase: "homogeneous identity rhetoric"
          explanation: "Language patterns that construct single, undifferentiated popular identity rather than acknowledging diverse constituencies"
        - phrase: "division-transcending unity claims"
          explanation: "Rhetorical emphasis on essential popular unity that rises above or eliminates internal differences and conflicts"
        - phrase: "shared identity construction"
          explanation: "Language creating common popular identity that binds diverse groups into single unified entity with shared interests"
        - phrase: "national homogeneity assertions"
          explanation: "Claims about unified national character that transcends internal divisions of class, region, ethnicity, or political affiliation"
      negative_examples:
        - phrase: "coalition-building across differences"
          explanation: "Unity appeals that explicitly acknowledge different groups and seek cooperation while maintaining their distinct identities rather than homogeneous fusion"
        - phrase: "group identification without unity construction"
          explanation: "References to communities or constituencies that acknowledge collective identity without claiming transcendent homogeneous unity"
        - phrase: "legal/civic status references"
          explanation: "Language focusing on shared civic or legal standing without constructing unified popular identity that transcends internal differences"
      boundary_cases:
        - phrase: "together"
          explanation: "depends on whether it implies unity vs. cooperation"
    scoring_calibration:
      high: "0.8-1.0: Strong unity construction, clear homogeneous identity, division transcendence"
      medium: "0.5-0.7: Moderate unity, some homogeneous identity, limited division transcendence"
      low: "0.1-0.4: Weak unity hints, minimal homogeneous identity language"
      absent: "0.0: No unity construction, homogeneous identity, or division transcendence"
    disambiguation:
      vs_nationalist_exclusion: "Homogeneous people focuses on internal unity; nationalist exclusion focuses on external boundaries"

  - name: "nationalist_exclusion"
    description: "Cultural/ethnic homogeneity and external threat emphasis that defines populist community boundaries."
    markers:
      positive_examples:
        - phrase: "external group threat characterization"
          explanation: "Rhetorical construction of outside groups as inherent dangers to national community based on essential cultural/ethnic characteristics rather than specific behaviors"
        - phrase: "cultural identity under siege framing"
          explanation: "Language positioning national/cultural identity as threatened by external forces requiring defensive exclusion to preserve homogeneous character"
        - phrase: "authentic membership through cultural criteria"
          explanation: "Definitions of legitimate national belonging that use cultural homogeneity as exclusionary criterion, implicitly delegitimizing cultural others"
        - phrase: "homogeneous cultural assertions"
          explanation: "Claims about shared cultural identity that define national community through exclusion of culturally different groups"
        - phrase: "external threat emphasis"
          explanation: "Rhetorical focus on dangers from outside groups that threaten internal cultural/national homogeneity"
        - phrase: "cultural invasion rhetoric"
          explanation: "Language characterizing cultural diversity or external influence as aggressive threat to essential national character"
        - phrase: "traditionalism as boundary marker"
          explanation: "Use of traditional values discourse to establish cultural boundaries that exclude non-conforming groups from legitimate membership"
        - phrase: "exclusive national identity construction"
          explanation: "Formation of national identity through emphasis on cultural/ethnic homogeneity that inherently excludes diverse populations"
      negative_examples:
        - phrase: "diversity celebration rhetoric"
          explanation: "Language that celebrates cultural diversity and inclusion as national strength rather than emphasizing homogeneity or external cultural threats"
        - phrase: "inclusive patriotism"
          explanation: "Love of country expressions that do not depend on cultural exclusion or external threat emphasis for national identity"
        - phrase: "pride without exclusionary boundary-drawing"
          explanation: "National pride expressions that do not require cultural homogeneity or external group exclusion to define legitimate membership"
      boundary_cases:
        - phrase: "our heritage"
          explanation: "depends on whether it implies exclusion vs. celebration"
    scoring_calibration:
      high: "0.8-1.0: Strong cultural exclusion, clear external threats, homogeneous identity emphasis"
      medium: "0.5-0.7: Moderate cultural exclusion, some external threats, limited homogeneity"
      low: "0.1-0.4: Weak cultural exclusion hints, minimal external threat language"
      absent: "0.0: No cultural exclusion, external threats, or homogeneous identity emphasis"
    disambiguation:
      vs_homogeneous_people: "Nationalist exclusion focuses on external boundaries; homogeneous people focuses on internal unity"

  - name: "economic_populist_appeals"
    description: "Populist economic discourse regardless of ideological direction—from redistributive left populism to protectionist right populism."
    markers:
      positive_examples:
        - phrase: "economic elite vs. working people framing"
          explanation: "Left-populist rhetorical structure contrasting concentrated economic power against ordinary workers with systemic disadvantage claims"
        - phrase: "elite economic interests vs. popular interests opposition"
          explanation: "Populist economic framing that positions financial/corporate elite interests as fundamentally opposed to broader popular economic welfare"
        - phrase: "nationalist economic priority rhetoric"
          explanation: "Right-populist economic appeals prioritizing national economic interests against internationalist or globalist elite economic arrangements"
        - phrase: "economic elite identification"
          explanation: "Specific characterization of concentrated economic power holders as distinct class opposed to popular economic interests"
        - phrase: "economic system manipulation claims"
          explanation: "Assertions that economic systems are structured or manipulated to benefit elite interests at expense of popular economic welfare"
        - phrase: "economic elite betrayal rhetoric"
          explanation: "Language characterizing economic outcomes as result of elite abandonment or betrayal of popular economic interests"
        - phrase: "populist economic justice appeals"
          explanation: "Economic reform rhetoric framed through people-versus-elite moral framework rather than technocratic policy analysis"
        - phrase: "economic fairness through elite opposition"
          explanation: "Economic fairness discourse that frames solutions through opposition to economic elite power rather than systemic reform"
      negative_examples:
        - phrase: "technocratic economic policy emphasis"
          explanation: "Economic discourse emphasizing expertise, evidence, and objective analysis rather than populist people-versus-elite framing structures"
        - phrase: "policy-focused economic discussion"
          explanation: "Economic policy discourse that focuses on specific mechanisms and outcomes without populist elite-opposition rhetoric"
        - phrase: "performance-based economic appeals"
          explanation: "Economic discourse emphasizing growth, effectiveness, and outcomes without framing through populist elite-popular conflict structures"
      boundary_cases:
        - phrase: "economic reform"
          explanation: "depends on whether it implies populist vs. technocratic approach"
    scoring_calibration:
      high: "0.8-1.0: Strong economic populist appeals, clear economic elite framing, economic corruption claims"
      medium: "0.5-0.7: Moderate economic populism, some economic elite framing, limited corruption claims"
      low: "0.1-0.4: Weak economic populist hints, minimal economic elite language"
      absent: "0.0: No economic populist appeals, economic elite framing, or economic corruption claims"
    disambiguation:
      vs_elite_conspiracy: "Economic populist focuses on economic domain; elite conspiracy focuses on coordination claims"
      vs_manichaean: "Economic populist focuses on economic elite framing; manichaean focuses on moral dichotomy regardless of domain"

# 5.4: Derived Metrics
derived_metrics:
  # Basic tension indices (measure rhetorical contradictions)
  - name: "democratic_authoritarian_tension"
    description: "Measures the strategic tension between claims of direct popular will and the rejection of legitimate opposition, quantifying the classic populist contradiction of invoking democratic authority while undermining pluralist norms."
    formula: "min(dimensions.popular_sovereignty_claims.raw_score, dimensions.anti_pluralist_exclusion.raw_score) * abs(dimensions.popular_sovereignty_claims.salience - dimensions.anti_pluralist_exclusion.salience)"
  - name: "internal_external_focus_tension"
    description: "Measures the strategic tension between constructing internal people unity and emphasizing external cultural threats, capturing the populist balance between cohesion-building and boundary-drawing rhetoric."
    formula: "min(dimensions.homogeneous_people_construction.raw_score, dimensions.nationalist_exclusion.raw_score) * abs(dimensions.homogeneous_people_construction.salience - dimensions.nationalist_exclusion.salience)"
  - name: "crisis_elite_attribution_tension"
    description: "Measures the strategic tension between temporal crisis narratives and elite conspiracy claims, quantifying how populist speakers balance decline-restoration framing with causal attribution to elite coordination."
    formula: "min(dimensions.crisis_restoration_narrative.raw_score, dimensions.elite_conspiracy_systemic_corruption.raw_score) * abs(dimensions.crisis_restoration_narrative.salience - dimensions.elite_conspiracy_systemic_corruption.salience)"
  
  # Strategic coherence index (calculated directly from base dimensions to avoid dependency chaining)
  - name: "populist_strategic_contradiction_index"
    description: "Overall measure of populist strategic coherence vs. contradiction, calculated as the average of the three core tension scores to assess whether a speaker employs contradictory populist appeals simultaneously."
    formula: "(min(dimensions.popular_sovereignty_claims.raw_score, dimensions.anti_pluralist_exclusion.raw_score) * abs(dimensions.popular_sovereignty_claims.salience - dimensions.anti_pluralist_exclusion.salience) + min(dimensions.homogeneous_people_construction.raw_score, dimensions.nationalist_exclusion.raw_score) * abs(dimensions.homogeneous_people_construction.salience - dimensions.nationalist_exclusion.salience) + min(dimensions.crisis_restoration_narrative.raw_score, dimensions.elite_conspiracy_systemic_corruption.raw_score) * abs(dimensions.crisis_restoration_narrative.salience - dimensions.elite_conspiracy_systemic_corruption.salience)) / 3"
  
  # Salience-weighted populist indices
  - name: "salience_weighted_core_populism_index"
    description: "Salience-weighted measure of core populist appeals, emphasizing rhetorically prominent dimensions to capture not just populist intensity but strategic emphasis patterns in the Primary Populist Core Anchors."
    formula: "(dimensions.manichaean_people_elite_framing.raw_score * dimensions.manichaean_people_elite_framing.salience + dimensions.crisis_restoration_narrative.raw_score * dimensions.crisis_restoration_narrative.salience + dimensions.popular_sovereignty_claims.raw_score * dimensions.popular_sovereignty_claims.salience + dimensions.anti_pluralist_exclusion.raw_score * dimensions.anti_pluralist_exclusion.salience) / (dimensions.manichaean_people_elite_framing.salience + dimensions.crisis_restoration_narrative.salience + dimensions.popular_sovereignty_claims.salience + dimensions.anti_pluralist_exclusion.salience + 0.001)"
  - name: "salience_weighted_populism_mechanisms_index"
    description: "Salience-weighted measure of populist mobilization mechanisms, capturing how speakers emphasize different populist mobilization strategies including conspiracy claims, authenticity positioning, and people unity construction."
    formula: "(dimensions.elite_conspiracy_systemic_corruption.raw_score * dimensions.elite_conspiracy_systemic_corruption.salience + dimensions.authenticity_vs_political_class.raw_score * dimensions.authenticity_vs_political_class.salience + dimensions.homogeneous_people_construction.raw_score * dimensions.homogeneous_people_construction.salience) / (dimensions.elite_conspiracy_systemic_corruption.salience + dimensions.authenticity_vs_political_class.salience + dimensions.homogeneous_people_construction.salience + 0.001)"
  - name: "salience_weighted_boundary_distinctions_index"
    description: "Salience-weighted measure of populist boundary-drawing mechanisms, capturing how speakers emphasize cultural exclusion and economic populist appeals to define in-group and out-group boundaries."
    formula: "(dimensions.nationalist_exclusion.raw_score * dimensions.nationalist_exclusion.salience + dimensions.economic_populist_appeals.raw_score * dimensions.economic_populist_appeals.salience) / (dimensions.nationalist_exclusion.salience + dimensions.economic_populist_appeals.salience + 0.001)"
  - name: "salience_weighted_overall_populism_index"
    description: "Comprehensive salience-weighted populist measure across all nine dimensions, providing an overall assessment of populist discourse that accounts for both intensity and rhetorical emphasis patterns."
    formula: "(dimensions.manichaean_people_elite_framing.raw_score * dimensions.manichaean_people_elite_framing.salience + dimensions.crisis_restoration_narrative.raw_score * dimensions.crisis_restoration_narrative.salience + dimensions.popular_sovereignty_claims.raw_score * dimensions.popular_sovereignty_claims.salience + dimensions.anti_pluralist_exclusion.raw_score * dimensions.anti_pluralist_exclusion.salience + dimensions.elite_conspiracy_systemic_corruption.raw_score * dimensions.elite_conspiracy_systemic_corruption.salience + dimensions.authenticity_vs_political_class.raw_score * dimensions.authenticity_vs_political_class.salience + dimensions.homogeneous_people_construction.raw_score * dimensions.homogeneous_people_construction.salience + dimensions.nationalist_exclusion.raw_score * dimensions.nationalist_exclusion.salience + dimensions.economic_populist_appeals.raw_score * dimensions.economic_populist_appeals.salience) / (dimensions.manichaean_people_elite_framing.salience + dimensions.crisis_restoration_narrative.salience + dimensions.popular_sovereignty_claims.salience + dimensions.anti_pluralist_exclusion.salience + dimensions.elite_conspiracy_systemic_corruption.salience + dimensions.authenticity_vs_political_class.salience + dimensions.homogeneous_people_construction.salience + dimensions.nationalist_exclusion.salience + dimensions.economic_populist_appeals.salience + 0.001)"

# 5.5: Output Schema
output_schema:
  type: object
  properties:
    dimensional_scores:
      type: object
      properties:
        manichaean_people_elite_framing: { $ref: "#/definitions/score_object" }
        crisis_restoration_narrative: { $ref: "#/definitions/score_object" }
        popular_sovereignty_claims: { $ref: "#/definitions/score_object" }
        anti_pluralist_exclusion: { $ref: "#/definitions/score_object" }
        elite_conspiracy_systemic_corruption: { $ref: "#/definitions/score_object" }
        authenticity_vs_political_class: { $ref: "#/definitions/score_object" }
        homogeneous_people_construction: { $ref: "#/definitions/score_object" }
        nationalist_exclusion: { $ref: "#/definitions/score_object" }
        economic_populist_appeals: { $ref: "#/definitions/score_object" }
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
