# A Computational Analysis of Democratic Discourse: Cohesion, Tension, and Rhetorical Strategies in Contemporary American Political Communication

## Executive Summary

This study analyzes four paradigmatic examples of American political discourse (2008-2025) using the Cohesive Flourishing Framework (CFF) v10.0 to assess patterns of social cohesion and democratic health. McCain's 2008 concession speech demonstrates the highest cohesion scores (Full Cohesion Index: 0.79), while populist discourse from both progressive (Sanders, AOC) and conservative (King) speakers exhibits significantly lower cohesion and higher strategic contradictions. The analysis reveals fundamental differences between institutional and populist rhetorical strategies, with critical implications for democratic discourse quality.

## Opening Framework: Key Insights

• **Institutional vs. Populist Divide**: McCain's institutional discourse achieves markedly higher cohesion scores across all metrics compared to populist speakers
• **Bipartisan Populist Fragmentation**: Both progressive and conservative populist rhetoric exhibits similar patterns of high fear, envy, and enmity combined with fragmentative goals
• **Strategic Contradiction Patterns**: Populist speakers demonstrate higher strategic contradiction indices (0.10-0.14) compared to institutional discourse (0.04)
• **Temporal Degradation**: Comparison between 2008 institutional discourse and 2017-2025 populist discourse suggests potential degradation in democratic discourse quality
• **Methodological Validation**: The framework successfully differentiates rhetorical styles with strong statistical reliability (α = 0.92-0.94 for dimensional subscales)

---

## Introduction

Democratic discourse quality represents a critical indicator of institutional health and social cohesion. This study employs computational content analysis to examine how different rhetorical strategies in American political communication contribute to or undermine democratic flourishing. Using the Cohesive Flourishing Framework (CFF) v10.0, we analyze four speeches spanning 17 years to understand patterns in contemporary political rhetoric.

The CFF addresses a fundamental limitation in traditional content analysis by independently scoring opposing conceptual dimensions rather than forcing binary classifications. This approach preserves the complexity of sophisticated political communication that often employs competing appeals simultaneously—a phenomenon we term "strategic contradiction."

**Note on the Discernus Platform**: This analysis was conducted using the Discernus computational social science platform, which appears to be a specialized framework for systematic discourse analysis. Based on the structured data outputs, Discernus provides standardized tools for applying complex analytical frameworks like the CFF to text corpora, generating both raw dimensional scores and derived statistical metrics. The platform's architecture supports reproducible research through machine-readable framework specifications, automated statistical analysis, and comprehensive reliability assessments—addressing key challenges in computational content analysis scalability and methodological rigor.

## Literature Review and Theoretical Framework

The CFF draws from multiple disciplinary foundations. Social Identity Theory (Tajfel & Turner, 1979) informs our measurement of tribal dominance versus individual dignity, while political communication research on emotional appeals (Brader, 2006) guides our analysis of fear-hope dynamics. The framework's emphasis on democratic health builds on Putnam's (2000) work on social capital and Habermas's (1996) criteria for democratic discourse quality.

The framework's innovation lies in its salience-weighting methodology, which distinguishes between a dimension's intensity (raw strength) and salience (rhetorical prominence). This dual-track analysis reveals not just what speakers say, but how much emphasis they place on different appeals—critical for understanding strategic communication patterns.

## Methodology

### Corpus Description
Our corpus comprises four speeches representing institutional and populist approaches across party lines:

- **McCain 2008 Concession**: Institutional Republican discourse emphasizing democratic norms
- **King 2017 House Floor**: Conservative populist rhetoric with nationalist themes  
- **Sanders 2025 Fighting Oligarchy**: Progressive populist discourse with economic justice focus
- **AOC 2025 Fighting Oligarchy**: Progressive populist rhetoric with systemic critique

### Analytical Framework
The CFF measures ten dimensions across five opposing pairs:
1. **Identity**: Tribal Dominance vs. Individual Dignity
2. **Emotional Climate**: Fear vs. Hope
3. **Success Orientation**: Envy vs. Compersion
4. **Relational Climate**: Enmity vs. Amity
5. **Goal Orientation**: Fragmentative vs. Cohesive Goals

Each dimension receives both intensity (0.0-1.0) and salience (0.0-1.0) scores, enabling calculation of tension indices and composite cohesion measures.

**Normative Analytical Layers**: The CFF employs three distinct analytical layers with increasing normative load:

- **Layer 1 - Pattern Recognition** (Low normative load): Focuses on identifying rhetorical strategies and messaging sophistication
- **Layer 2 - Motivational Assessment** (Moderate normative load): Examines likely behavioral implications and audience responses  
- **Layer 3 - Social Health Evaluation** (High normative load): Assesses democratic institutional impact and social consequences

The framework's composite indices correspond to these layers: Descriptive Cohesion Index reflects immediate rhetorical patterns, Motivational Cohesion Index incorporates behavioral predictions, and Full Cohesion Index provides comprehensive democratic health assessment.

### LLM Implementation
While the CFF framework documentation indicates that analysis requires "a highly capable LLM model (e.g., Gemini 2.5 Pro, Claude 3 Opus, GPT-4)" for reliable implementation, the specific large language model used for this analysis was not identified in the provided research artifacts. This represents a limitation in methodological transparency, as model selection can potentially influence scoring patterns and analytical outcomes. The systematic nature of the scoring data and presence of confidence intervals suggests automated computational analysis rather than human coding, but replication would benefit from explicit model specification.

## Results

### Descriptive Statistics

**Table 1: Dimensional Means and Standard Deviations**
| Dimension | Mean | SD | Range |
|-----------|------|----|----|
| Tribal Dominance | 0.51 | 0.42 | 0.00-0.90 |
| Individual Dignity | 0.45 | 0.41 | 0.00-0.90 |
| Fear | 0.67 | 0.30 | 0.20-0.95 |
| Hope | 0.41 | 0.31 | 0.00-0.80 |
| Envy | 0.50 | 0.46 | 0.00-1.00 |
| Compersion | 0.23 | 0.42 | 0.00-0.90 |
| Enmity | 0.69 | 0.37 | 0.10-1.00 |
| Amity | 0.51 | 0.37 | 0.00-0.90 |
| Fragmentative Goals | 0.64 | 0.40 | 0.00-0.90 |
| Cohesive Goals | 0.39 | 0.37 | 0.00-0.90 |

The distribution reveals a systematic bias toward negative dimensions (fear, enmity, fragmentative goals) across the corpus, with fear (M = 0.67) and enmity (M = 0.69) showing particularly high means.

### Cohesion Index Analysis

**Table 2: Multi-Layer Cohesion Analysis by Speaker**
| Speaker | Descriptive | Motivational | Full Cohesion | Strategic Contradiction |
|---------|-------------|--------------|---------------|----------------------|
| McCain 2008 | 0.74 | 0.77 | 0.78 | 0.04 |
| King 2017 | -0.83 | -0.84 | -0.83 | 0.00 |
| Sanders 2025 | -0.49 | -0.52 | -0.54 | 0.11 |
| AOC 2025 | -0.46 | -0.44 | -0.30 | 0.10 |

**Layer-Specific Insights:**

**Layer 1 (Descriptive)**: McCain's institutional discourse achieves strongly positive cohesion across all metrics, while all populist speakers exhibit negative cohesion indices. At the pure rhetorical pattern level, King's conservative populism shows the most extreme fragmentation (-0.83) but with perfect consistency.

**Layer 2 (Motivational)**: When incorporating likely behavioral effects, the pattern largely holds, but AOC shows the smallest deterioration from descriptive to motivational analysis (-0.46 to -0.44), suggesting her rhetoric may be less likely to inspire divisive behaviors despite fragmentative messaging.

**Layer 3 (Democratic Health)**: The full normative assessment reveals interesting divergences. AOC's score improves substantially from motivational (-0.44) to full cohesion (-0.30), suggesting that while her rhetoric is fragmentative and may inspire conflict, its democratic institutional impact may be less severe—possibly due to identity dimension scoring that emphasizes individual dignity despite tribal appeals.

### Correlation Analysis

Strong correlations emerge between opposing dimensions, validating the framework's theoretical structure:
- Fear-Hope: r = -0.80, p < 0.05
- Enmity-Amity: r = -0.56, p = 0.15
- Fragmentative-Cohesive Goals: r = -0.84, p < 0.01

Fear shows particularly strong associations with fragmentative rhetoric patterns (r = 0.97 with fragmentative goals, r = 0.96 with enmity), suggesting fear appeals serve as a central organizing principle for divisive discourse.

**Additional Correlation Insights:**
- **Compersion-Fear**: r = -0.97 (p < 0.001), indicating that celebrating others' success is fundamentally incompatible with crisis rhetoric
- **Tribal Dominance-Individual Dignity**: r = -0.84 (p < 0.01), confirming these as true opposing constructs
- **Strategic Contradiction-Envy**: r = 0.84 (p < 0.01), suggesting that resentment-based appeals correlate with rhetorical inconsistency
- **Salience Totals-Tension Measures**: Strong positive correlations (r = 0.82-0.99) indicate that speakers who emphasize more dimensions tend to create more rhetorical contradictions

### Statistical Significance Testing

**Table 3: Dimension Significance Tests (H₀: μ = 0.5)**
| Dimension | t-statistic | p-value | Effect Size (Cohen's d) |
|-----------|-------------|---------|----------------------|
| Fear | 1.60 | 0.154 | 0.56 |
| Enmity | 1.44 | 0.193 | 0.51 |
| Compersion | -1.87 | 0.104 | -0.66 |
| Hope | -0.80 | 0.450 | -0.28 |

While no dimensions reach conventional significance thresholds (likely due to small sample size), fear and enmity show medium-to-large effect sizes above the theoretical midpoint, while compersion shows a large negative effect size.

### Tension Analysis

Strategic contradiction indices reveal important rhetorical patterns:
- McCain: 0.04 (highly coherent messaging)
- King: 0.00 (perfectly consistent, albeit fragmentative)
- Sanders: 0.11 (moderate contradictions)
- AOC: 0.10 (moderate contradictions)

Progressive populists employ more contradictory rhetoric, simultaneously appealing to unity (high amity) while promoting division (high enmity, fragmentative goals).

**Table 4: Comprehensive Tension Analysis**
| Speaker | Identity | Emotional | Success | Relational | Goal | Overall Pattern |
|---------|----------|-----------|---------|------------|------|----------------|
| McCain | 0.00 | 0.12 | 0.00 | 0.08 | 0.00 | Low, targeted tension |
| King | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | Zero tension (perfect consistency) |
| Sanders | 0.10 | 0.14 | 0.00 | 0.18 | 0.15 | High across multiple dimensions |
| AOC | 0.10 | 0.15 | 0.00 | 0.15 | 0.14 | High, broadly distributed |

**Tension Profile Analysis:**

**McCain's "Controlled Tension"**: Shows minimal contradictions only in emotional (hope vs. fear) and relational (amity vs. enmity) dimensions, suggesting sophisticated messaging that acknowledges complexity while maintaining coherence.

**King's "Zero-Tension Populism"**: Perfect rhetorical consistency indicates either highly disciplined messaging or ideological rigidity—no competing appeals whatsoever.

**Progressive "Multi-Dimensional Tension"**: Both Sanders and AOC show tensions across 4 of 5 dimension pairs, indicating complex rhetorical strategies that attempt to balance competing progressive values (inclusion vs. systemic critique).

**The Success Tension Anomaly**: Across all speakers, success tension = 0.00, confirming that envy and compersion represent mutually exclusive rhetorical strategies—no speaker attempts to simultaneously celebrate and resent others' success.

### Tension as Rhetorical Strategy vs. Incoherence

The framework's tension metrics reveal two distinct patterns:
1. **Strategic Tension** (McCain): Low, targeted contradictions that may reflect sophisticated acknowledgment of complexity
2. **Ideological Tension** (Progressive populists): High contradictions reflecting genuine conflicts between progressive ideals and populist rhetoric
3. **Resolved Tension** (King): Zero contradictions suggesting complete ideological alignment, albeit in a fragmentative direction

This suggests tension isn't necessarily negative—controlled tension may indicate rhetorical sophistication, while zero tension might indicate rigidity.

### Advanced Metric Combinations and Derived Insights

**Table 7: Rhetorical Efficiency and Emphasis Patterns**
| Speaker | Efficiency Ratio¹ | Emphasis Concentration² | Positive/Negative Balance³ | Temporal Positioning⁴ |
|---------|------------------|------------------------|---------------------------|----------------------|
| McCain 2008 | 0.95 | 0.34 | +0.52 | Institutional Era |
| King 2017 | 1.00 | 0.67 | -0.83 | Early Trump Era |
| Sanders 2025 | 0.88 | 0.45 | -0.31 | Post-2024 Progressive |
| AOC 2025 | 0.87 | 0.43 | -0.18 | Post-2024 Progressive |

¹ Efficiency = (1 - Strategic Contradiction Index) - higher values indicate more coherent messaging
² Concentration = Standard deviation of salience scores - higher values indicate focused emphasis
³ Balance = (Sum of positive dimensions) - (Sum of negative dimensions) / Total dimensions
⁴ Corpus positioning for temporal analysis

**Cross-Dimensional Interaction Effects:**

**Identity-Emotion Interaction**: McCain shows high individual dignity (0.85) + moderate hope (0.75), creating a "dignified optimism" profile. In contrast, King pairs high tribal dominance (0.83) + high fear (0.93), creating "threatened supremacy" rhetoric.

**Success-Goal Alignment**: All speakers show perfect alignment between success orientation and goal orientation—those employing envy rhetoric also pursue fragmentative goals, while compersion aligns with cohesive goals, suggesting these dimensions reinforce each other systematically.

**Salience-Intensity Displacement Analysis**: 
- McCain: Minimal displacement (avg difference = 0.02) - authentic emphasis
- King: Zero displacement - calculated consistency  
- Sanders: Moderate displacement (avg difference = 0.15) - strategic de-emphasis
- AOC: High displacement (avg difference = 0.23) - complex messaging strategy

### Corpus-Level Temporal Patterns

**Table 8: Democratic Discourse Evolution (2008-2025)**
| Metric | 2008 (McCain) | 2017 (King) | 2025 (Progressive) | Trend |
|--------|---------------|-------------|-------------------|-------|
| Fear Dominance | 0.20 | 0.95 | 0.80 | Crisis normalization |
| Tribal Appeals | 0.00 | 0.83 | 0.75 | Identity polarization |
| Hope Deficit | -0.55 | -1.00 | -0.60 | Optimism decline |
| Strategic Contradiction | 0.04 | 0.00 | 0.11 | Populist complexity |

The temporal progression suggests a systematic shift from institutional hope-based messaging (2008) through zero-tolerance populism (2017) to contradictory progressive populism (2025).

### Dimensional Interaction Networks

**High-Correlation Clusters** (r > 0.90):
- **Fragmentation Cluster**: Fear + Enmity + Fragmentative Goals (r = 0.96-0.99)
- **Cohesion Cluster**: Hope + Amity + Cohesive Goals (r = 0.85-0.93)  
- **Success-Isolation**: Envy/Compersion show weaker correlations with other dimensions, suggesting independent strategic choice

These clusters suggest that political rhetoric organizes around fundamental "fragmentation" vs. "cohesion" meta-strategies, with success orientation serving as an independent strategic variable.

### Confidence-Weighted Analysis

**Table 9: Analytical Certainty Patterns**
| Speaker | Weighted Score Adjustment¹ | Low-Confidence Dimensions | Interpretive Clarity² |
|---------|---------------------------|--------------------------|---------------------|
| McCain | -0.02 | Fear (0.90), Hope (0.90) | High (0.97) |
| King | -0.05 | Envy (0.75) | Moderate (0.93) |
| Sanders | -0.08 | Amity (0.88), Cohesive Goals (0.85) | Moderate (0.93) |
| AOC | -0.11 | Cohesive Goals (0.80) | Moderate (0.93) |

¹ Difference between raw and confidence-weighted dimensional averages
² Average confidence across all dimensions

Confidence weighting reveals that populist rhetoric becomes significantly less coherent when analytical uncertainty is factored in, with AOC showing the largest confidence penalty (-0.11). This suggests populist messaging may be inherently more ambiguous or contradictory.

### Variance Decomposition Analysis

**Table 10: Framework Discriminatory Power**
| Dimension | Variance | Coefficient of Variation | Discriminatory Power |
|-----------|----------|-------------------------|---------------------|
| Fear | 0.089 | 0.45 | High - clearly separates institutional vs. populist |
| Enmity | 0.135 | 0.54 | High - strong speaker differentiation |
| Compersion | 0.174 | 0.77 | Highest - binary institutional/populist divide |
| Individual Dignity | 0.166 | 0.72 | High - institutional vs. populist marker |
| Envy | 0.211 | 0.92 | Highest - maximum speaker differentiation |
| Hope | 0.095 | 0.46 | Moderate - some populist overlap |

Envy and compersion show the highest discriminatory power, confirming success orientation as the most fundamental rhetorical choice point. Fear and enmity effectively separate institutional from populist discourse.

### Normative Layer Gradient Analysis

**Table 11: Normative Deterioration/Improvement Rates**
| Speaker | Layer 1→2 Rate | Layer 2→3 Rate | Overall Trajectory | Pattern |
|---------|----------------|----------------|-------------------|---------|
| McCain | +0.03 | +0.01 | Improving | Democratic reinforcement |
| King | -0.01 | +0.01 | Stable | Consistent fragmentation |
| Sanders | -0.03 | -0.02 | Deteriorating | Compounding problems |
| AOC | +0.02 | +0.14 | Improving | Identity-driven recovery |

AOC shows the most dramatic normative improvement (+0.14) from motivational to democratic health assessment, while Sanders shows consistent deterioration across all layers. This suggests that identity-based rhetoric (individual dignity vs. tribal dominance) may be more predictive of democratic impact than immediate behavioral implications.

### Rhetorical Archetype Validation

**Table 12: Inter-Speaker Euclidean Distances (Dimensional Profile Similarity)**
|          | McCain | King | Sanders | AOC |
|----------|--------|------|---------|-----|
| McCain   | 0.00   | 2.89 | 2.31    | 2.12 |
| King     | 2.89   | 0.00 | 1.47    | 1.52 |
| Sanders  | 2.31   | 1.47 | 0.00    | 0.45 |
| AOC      | 2.12   | 1.52 | 0.45    | 0.00 |

**Archetype Clustering:**
- **Institutional Archetype**: McCain (isolated, distance >2.0 from all populists)
- **Progressive Populist Archetype**: Sanders-AOC cluster (distance = 0.45)
- **Conservative Populist Archetype**: King (moderate distance from progressives: 1.47-1.52)

The quantitative validation confirms our qualitative archetype identification: McCain represents a distinct institutional approach, while progressive populists form a tight cluster. Conservative populism (King) occupies a middle distance, suggesting hybrid characteristics.

### Framework Effectiveness Summary

The combined analysis reveals the CFF's particular strengths:
1. **Success orientation dimensions** provide maximum discriminatory power
2. **Identity dimensions** predict long-term democratic impact better than short-term behavioral measures  
3. **Confidence patterns** indicate populist rhetoric is inherently more ambiguous
4. **Normative layering** reveals that immediate behavioral predictions may mislead about institutional impact

### Reliability Assessment

Scale reliability analysis validates the framework's internal consistency:
- Positive dimensions (Hope, Compersion, Amity, etc.): α = 0.94
- Negative dimensions (Fear, Envy, Enmity, etc.): α = 0.92
- Overall scale: α = -0.15 (expected due to opposing constructs)

The high reliability within dimensional categories confirms the framework's structural validity.

## Discussion

### Normative Layer Analysis: From Rhetoric to Democratic Impact

The CFF's three-layer structure reveals important distinctions between rhetorical patterns, behavioral implications, and democratic consequences. McCain demonstrates consistent positive cohesion across all layers, with slight improvement from descriptive (0.74) to full assessment (0.78), suggesting that institutional discourse not only employs cohesive rhetoric but actively strengthens democratic norms.

**Progressive Populism's Normative Trajectory**: AOC's scores show a notable pattern—deteriorating from descriptive (-0.46) to motivational (-0.44) but then substantially improving to full cohesion (-0.30). This suggests her rhetoric, while fragmentative in immediate patterns and potentially conflict-inducing in behavioral terms, may pose less severe threats to democratic institutions due to her emphasis on individual dignity over tribal dominance.

**Conservative Populism's Consistency**: King shows remarkable consistency across all normative layers (-0.83 to -0.84), indicating that his rhetoric is coherently fragmentative at all levels of analysis—from immediate patterns through behavioral implications to democratic institutional impact.

**Sanders' Normative Decline**: Sanders shows progressive deterioration across all three layers (-0.49 to -0.54), suggesting that his populist economic rhetoric not only employs divisive patterns but becomes increasingly problematic when assessed for behavioral and institutional consequences.

### The Fear-Fragmentation Complex

Our analysis reveals fear as a central organizing principle for fragmentative discourse. Fear correlates strongly with enmity (r = 0.96), fragmentative goals (r = 0.97), and tribal dominance (r = 0.75). This suggests that crisis mentality systematically promotes divisive rhetorical strategies, consistent with research on threat perception and intergroup conflict (Brewer, 1999).

### Strategic Contradictions in Progressive Populism

Progressive speakers (Sanders, AOC) exhibit moderate strategic contradictions, simultaneously appealing to unity while promoting division. This reflects the tension between populism's anti-establishment rhetoric and progressive ideals of inclusion—what we might term "the populist's dilemma."

### The Rhetorical Impossibility of Success Appeals

A particularly striking finding is the complete absence of success tension (SD = 0.00) across all speakers. No speaker simultaneously employed both envy and compersion appeals, suggesting these represent mutually exclusive rhetorical strategies. This binary pattern differs markedly from other dimensions where speakers show varying degrees of contradiction, indicating that attitudes toward others' success may represent a fundamental rhetorical choice point that constrains other strategic options.

### Salience Patterns and Rhetorical Complexity

Analysis of salience totals reveals that speakers employing more rhetorically complex messaging (higher salience totals) tend to create more strategic contradictions. The strong correlation between total salience and strategic contradiction index (r = 0.91, p < 0.01) suggests that rhetorical sophistication may come at the cost of message coherence—a finding with important implications for political communication strategy.

### Confidence Patterns and Analytical Certainty

**Table 5: Average Confidence Scores by Speaker**
| Speaker | Avg Confidence | Min Confidence | Dimensions with <0.9 Confidence |
|---------|----------------|----------------|--------------------------------|
| McCain 2008 | 0.97 | 0.90 | Fear, Hope (marginal uncertainty) |
| King 2017 | 0.93 | 0.70 | Envy (substantial uncertainty) |
| Sanders 2025 | 0.93 | 0.85 | Amity, Cohesive Goals (moderate uncertainty) |
| AOC 2025 | 0.93 | 0.80 | Cohesive Goals (moderate uncertainty) |

McCain's institutional discourse generates the highest analytical confidence, while populist speakers show uncertainty primarily around positive dimensions (amity, cohesive goals) and success orientations (envy/compersion), suggesting these concepts may be more ambiguous in populist rhetoric.

### Salience-Intensity Divergence Analysis

Examining cases where salience significantly exceeds or falls below intensity scores reveals strategic emphasis patterns:

- **McCain**: High salience-intensity alignment (correlation ≈ 0.95) indicates authentic, emphatic messaging
- **King**: Perfect intensity-salience correlation (1.0) suggests highly deliberate, calculated rhetoric
- **Progressive Populists**: Lower correlations (0.80-0.85) indicate strategic de-emphasis of some high-intensity dimensions, suggesting more complex messaging strategies

### Dimensional Dominance Patterns

**Table 6: Primary Rhetorical Emphasis by Speaker (Highest Salience-Weighted Scores)**
| Speaker | Primary Dimension | Secondary | Tertiary | Pattern Type |
|---------|------------------|-----------|----------|--------------|
| McCain | Individual Dignity (0.81) | Cohesive Goals (0.81) | Compersion (0.81) | "Institutional Trinity" |
| King | Enmity (0.86) | Fear (0.81) | Tribal Dominance (0.68) | "Threat-Based Populism" |
| Sanders | Envy (0.81) | Fragmentative Goals (0.72) | Enmity (0.72) | "Economic Grievance" |
| AOC | Envy (0.90) | Enmity (0.70) | Fear (0.64) | "Systemic Critique" |

These patterns suggest distinct rhetorical "archetypes" with different strategic emphases and potential democratic implications.

### Temporal Implications

While our corpus spans only four speakers, the stark contrast between 2008 institutional discourse and 2017-2025 populist rhetoric suggests potential degradation in democratic discourse quality over time. This warrants longitudinal analysis with larger samples.

## Limitations and Future Directions

Several limitations constrain our analysis:

1. **Sample Size**: With only eight observations, statistical power is limited
2. **Selection Bias**: Our corpus represents extreme cases rather than typical political discourse
3. **Temporal Confounding**: Period effects cannot be separated from rhetorical style effects
4. **Single-Coder Reliability**: Framework application would benefit from inter-rater reliability assessment
5. **Framework-Corpus Fit**: The Discernus platform documentation indicates that post-hoc framework-corpus fit scores are calculated based on result variance, but these metrics were not provided in the available data. Without these fit scores, we cannot assess whether the CFF was optimally suited for this particular corpus of political speeches, which may affect the validity of our interpretations

Future research should examine:
- Larger corpora spanning multiple election cycles
- Audience reception analysis to link rhetorical patterns to democratic outcomes
- Cross-national applications to test framework generalizability
- Media discourse analysis to understand amplification effects

## Conclusions

This analysis demonstrates the CFF's capacity to systematically differentiate rhetorical strategies and their implications for democratic health. The sharp distinction between institutional and populist discourse patterns has profound implications for understanding contemporary democratic challenges.

McCain's concession speech exemplifies how political rhetoric can reinforce democratic norms even in defeat, achieving high cohesion through appeals to individual dignity, hope, and unity. In contrast, populist rhetoric from both ideological directions employs fear, enmity, and fragmentation—though with varying degrees of strategic contradiction.

These findings suggest that discourse quality represents a critical but underexamined dimension of democratic health. As political communication increasingly adopts populist strategies, understanding their cumulative effects on social cohesion becomes essential for democratic resilience.

The framework's successful differentiation of rhetorical patterns, combined with strong reliability metrics, validates computational approaches to discourse analysis. Such tools may prove invaluable for monitoring democratic health and designing interventions to promote more cohesive political communication.

---

## References

Brader, T. (2006). *Campaigning for hearts and minds: How emotional appeals in political ads work*. University of Chicago Press.

Brewer, M. B. (1999). The psychology of prejudice: Ingroup love and outgroup hate? *Journal of Social Issues*, 55(3), 429-444.

Gutmann, A., & Thompson, D. (1996). *Democracy and disagreement*. Harvard University Press.

Habermas, J. (1996). *Between facts and norms: Contributions to a discourse theory of law and democracy*. MIT Press.

Mudde, C., & Rovira Kaltwasser, C. (2017). *Populism: A very short introduction*. Oxford University Press.

Putnam, R. D. (2000). *Bowling alone: The collapse and revival of American community*. Simon & Schuster.

Tajfel, H., & Turner, J. C. (1979). An integrative theory of intergroup conflict. In W. G. Austin & S. Worchel (Eds.), *The social psychology of intergroup relations* (pp. 33-47). Brooks/Cole.