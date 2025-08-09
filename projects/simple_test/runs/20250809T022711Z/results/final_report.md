# Experiment Report

## Evidence-Backed Hypothesis Testing

### H1: Institutional Cohesion

**Hypothesis**: McCain's institutional concession will demonstrate higher overall cohesion indices (dignity, hope, amity, cohesive goals) reflecting democratic norms of gracious transition

Based on the evidence provided, the hypothesis is **INCONCLUSIVE**.

A definitive conclusion cannot be reached due to the absence of the necessary statistical evidence. The hypothesis posits that McCain's concession will demonstrate *higher* overall cohesion indices. To validate such a comparative claim, aggregate statistical data—such as mean cohesion scores, standard deviations, and tests of statistical significance (e.g., t-tests or ANOVA)—are required to compare McCain's discourse against a relevant baseline or another discourse type. Without these quantitative measures, it is impossible to statistically confirm that the observed cohesion is significantly "higher."

However, a qualitative analysis of the classified textual evidence provides preliminary, though not definitive, support for the hypothesis. The samples from McCain's 2008 concession speech consistently align with the specified cohesion indices, reflecting norms of a gracious political transition. The discourse is marked by strong expressions of **amity**, as when McCain frames the political contest within a superordinate national identity: "Whatever our differences, we are fellow Americans..." (amity, conf: 0.95). The theme of **dignity** is also prominent, extended both to his opponent and the electorate. McCain commends Senator Obama for "inspiring the hopes of so many millions of Americans," an act he "deeply admire[s]" (individual_dignity, conf: 0.95), and acknowledges a shared belief in American opportunity, despite the painful "memory of old injustices" (individual_dignity, conf: 0.90). Finally, the speech explicitly articulates **cohesive goals**, calling on supporters to offer the victor "good will and earnest effort to find ways to come together...to bridge our differences" (cohesive_goals, conf: 0.95). The high confidence scores associated with these classifications lend weight to their thematic relevance.

Despite these qualitative indicators, the analysis is constrained by two critical limitations. First, as noted, the lack of aggregate statistics prevents a formal test of the hypothesis. Second, the extremely small sample size of eight unique textual excerpts (N=8) is insufficient to support generalizable claims about the entire speech or the genre of institutional concessions. Therefore, while the available textual evidence is thematically consistent with the hypothesis, the lack of quantitative validation renders the finding inconclusive. A robust test would require a full statistical analysis of a larger, more representative corpus.

### H2: Populist Fragmentation

**Hypothesis**: Sanders' populist critique will show higher fragmentative elements (tribal dominance, enmity) but with strategic contradictions indicating sophisticated rhetorical positioning

**Conclusion**

Based on the evidence provided, the hypothesis is **INCONCLUSIVE**. This conclusion is necessitated by the complete absence of statistical evidence (Statistical Evidence: {}) and a critically small textual sample size (N=8 unique excerpts). Without quantitative metrics comparing the frequency and distribution of discourse features across a larger corpus, claims of "higher" levels of fragmentation cannot be substantiated. However, the limited qualitative data does present a pattern that is highly consistent with the hypothesis, warranting further investigation.

The textual evidence offers preliminary support for both components of the hypothesis. First, the populist critique from Sanders clearly exhibits the specified fragmentative elements. His discourse was classified with high confidence as containing `enmity` ("The rich want to get richer and they don't care who they step on," conf: 0.90) and `fragmentative_goals` ("We will not accept an oligarchic form of society," conf: 0.90). These statements construct a clear out-group ("the rich," "oligarchs") and define political objectives in oppositional terms, aligning with the first part of the hypothesis.

Second, the evidence points toward the "strategic contradictions" indicative of sophisticated rhetorical positioning. Alongside the fragmentative rhetoric, Sanders employs cohesive language to foster in-group solidarity. He is shown using `amity` to rally his supporters, urging them to "stand together, are strong, are disciplined" to "create the kind of nation that we deserve" (conf: 0.80). This juxtaposition of defining an external enemy while simultaneously building internal cohesion is the core of the hypothesized strategy. The McCain sample, by contrast, consists exclusively of cohesive elements such as `amity`, `individual_dignity`, and `cohesive_goals`, providing a baseline against which Sanders' mixed rhetoric appears distinct.

In summary, while the qualitative excerpts align perfectly with the hypothesized rhetorical structure—demonstrating both fragmentation and strategic cohesive appeals in Sanders' discourse—the conclusion must remain inconclusive. The fundamental limitations of a non-existent statistical framework and a sample size insufficient for generalization make it impossible to validate the hypothesis rigorously. A larger, statistically representative corpus would be required to determine if these observed patterns are significant and characteristic of Sanders' broader populist discourse compared to other political actors.

### H3: Democratic Patterns

**Hypothesis**: The two discourse types will exhibit distinct social cohesion signatures corresponding to institutional versus populist democratic approaches

Based on the evidence provided, the hypothesis that the two discourse types will exhibit distinct social cohesion signatures corresponding to institutional versus populist democratic approaches is **INCONCLUSIVE**, though the qualitative data offers preliminary support. The absence of statistical evidence makes it impossible to validate the observed qualitative patterns rigorously.

The analysis of the textual evidence reveals two divergent rhetorical signatures. The institutional discourse, exemplified by John McCain's 2008 concession speech, is characterized by a high frequency of markers associated with social cohesion and deference to democratic norms. This is evident in repeated expressions of `amity` that emphasize a superordinate national identity over partisan division: "Whatever our differences, we are fellow Americans, and please believe me when I say no association has ever meant more to me than that" (john_mccain_2008_concession.txt, amity, conf: 0.95). This unifying theme is reinforced by a stated commitment to `cohesive_goals`, such as the call to "find the necessary compromises to bridge our differences" (john_mccain_2008_concession.txt, cohesive_goals, conf: 0.95). Furthermore, this discourse type consistently affirms the value of political opponents and the citizenry through expressions of `compassion` and `individual_dignity`, as when McCain commends his opponent's ability to inspire "so many millions of Americans" (john_mccain_2008_concession.txt, individual_dignity, conf: 0.95). This signature aligns with an institutional approach that seeks to reinforce the legitimacy of the political system and ensure stability.

Conversely, the populist discourse, represented by Bernie Sanders' speech on fighting oligarchy, displays a signature of social polarization. This approach constructs a conflictual social dynamic by defining a virtuous in-group ("we") against a corrupt out-group. This is most clearly demonstrated through the classification of `enmity`, which frames the political contest as a moral struggle: "The rich want to get richer and they don't care who they step on" (bernie_sanders_2025_fighting_oligarchy.txt, enmity, conf: 0.90). This antagonistic framing is complemented by `fragmentative_goals` that reject existing societal structures rather than seeking compromise within them: "We will not accept an oligarchic form of society" (bernie_sanders_2025_fighting_oligarchy.txt, fragmentative_goals, conf: 0.90). While an instance of `amity` is present in Sanders' discourse, it functions to solidify the in-group for the purpose of this conflict—"if we stand together...we can create the kind of nation that we deserve" (bernie_sanders_2025_fighting_oligarchy.txt, amity, conf: 0.80)—rather than to bridge societal divides.

In conclusion, the qualitative evidence strongly suggests that the institutional and populist discourses utilize distinct social cohesion strategies as hypothesized. However, this conclusion remains tentative due to critical limitations. Most significantly, no statistical evidence was provided to determine the frequency, distribution, or significance of these coded features across the two corpora. Without quantitative data (e.g., chi-square tests of code frequencies), it is impossible to ascertain whether these observed differences are statistically significant or merely anecdotal. Furthermore, the small sample size (N=8) drawn from only two texts limits the generalizability of these findings. Therefore, while the textual analysis provides a compelling narrative in favor of the hypothesis, the lack of statistical validation renders the hypothesis empirically **INCONCLUSIVE**.


## Beyond the Hypotheses: Computational Insights

*Leveraging billion-dollar pattern recognition to discover insights beyond experimental design*

### Insight 1: The Inversion of the Historical Superlative

Analysis reveals a functional inversion of the historical superlative ("ever") as a rhetorical device. While both speakers anchor their arguments in a historical context, the purpose of this framing has shifted from unifying through a shared past to dividing through an unprecedented present. This pattern suggests a change not just in political tone, but in the fundamental use of history to construct political reality.

John McCain, in a moment of de-escalation, uses the device to frame unity as a personal, historical peak. His statement, "no association has **ever** meant more to me than that," positions the identity of "fellow Americans" as the ultimate, time-tested value, superseding the conflict of the moment. Conversely, Bernie Sanders, in a call to action, uses the same device to frame a national crisis. His claim of "more concentration of ownership... than we have **ever** had in the history of this country" weaponizes history to establish the present as a unique, dangerous breaking point that demands confrontation. The rhetorical tool is identical, but its function has inverted: from a mechanism for reconciliation to a catalyst for mobilization.

### Insight 2: Co-opting Resentment for Cohesive Manipulation

System analysis reveals a non-obvious pattern where the speaker employing overtly cohesive rhetoric, John McCain, also utilizes a sophisticated form of manipulation by co-opting the language of resentment. While Bernie Sanders' use of resentment is direct and fragmentative ("We will not accept an oligarchic form of society"), McCain's is more subtle. He strategically acknowledges the foundations of resentment to neutralize them within a broader, unifying message.

This tactic is evident when McCain references past grievances, noting that "the memory of them [old injustices] still had the power to wound." He is not stoking resentment but validating its source. Similarly, he acknowledges a sense of political alienation by referencing "millions of Americans who had once wrongly believed that they had little at stake or little influence." By embedding these acknowledgments of past pain and powerlessness within messages tagged as `hope` and `cohesive_goals`, McCain reframes these potentially divisive feelings as overcome obstacles. This rhetorical maneuver manipulates the emotional landscape, using the memory of resentment as a tool to build consensus rather than to fragment it.

### Insight 3: Thematic Convergence as a Marker of Authentic Concession

The evidence reveals that speaker authenticity, particularly in a high-stakes context like a political concession, is signaled not by the mere presence of positive themes, but by their **conceptual convergence** within single, pivotal statements. The system detected that one core idea in McCain's speech was simultaneously and with high confidence classified under three distinct, high-level concepts: `hope`, `individual_dignity`, and `compassion`. This thematic density points to a moment of profound rhetorical and emotional sincerity.

The key utterance, "...that he managed to do so by inspiring the hopes of so many millions of Americans who had once wrongly believed that they had little at stake," serves as the nexus for this pattern. It is flagged for both `hope` and `individual_dignity` (conf: 0.95), while a slightly longer version containing this clause is flagged for `compassion` (conf: 0.95). This is not a simple list of virtues. Instead, McCain achieves authenticity by reframing his opponent's victory through the lens of his own deeply held values. He explicitly connects his worldview to his opponent's by stating, "I've always believed that America offers opportunities to all... Senator Obama believes that too." By framing Obama's success as a validation of a shared American ideal, McCain concedes the election without compromising his own principles, thereby projecting an authenticity that resonates more deeply than simple praise.

### Insight 4: From Healing Historical Wounds to Prosecuting a Present-Day War

The evidence reveals a significant evolution in how societal divisions are framed in civic discourse. The locus of conflict has shifted from being a *historical wound* requiring collective healing to a *present-day structural war* requiring active combat. This is a more nuanced pattern than a simple increase in negative sentiment.

In 2008, John McCain's concession speech framed America's core challenge as overcoming the "memory" of "old injustices." While acknowledging these memories "still had the power to wound," the framing is retrospective. His rhetoric seeks national cohesion by finding common ground with his opponent ("Senator Obama believes that too"), positioning the struggle as a shared journey away from a stained past toward a more perfect union. The division is a ghost to be exorcised collectively.

By contrast, the 2025-era discourse articulated by Bernie Sanders defines the central conflict as an immediate, ongoing, and structural one. The problem is not a memory but a present reality: "Today you have more concentration of ownership... than we have ever had." The language shifts from healing to fighting, explicitly identifying a contemporary antagonist ("The rich want to get richer") and a system to be defeated ("We will not accept an oligarchic form of society"). The discourse is no longer about binding up the nation's old wounds, but about mobilizing one part of the nation to fight a battle against another, here and now.

### Insight 5: Emotional Granularity Reveals Rhetorical Structure

A non-obvious insight emerges from the system's ability to differentiate between the labels `enmity` and `envy` with high confidence within the same political text. A simple statistical summary might aggregate these into a single "negative sentiment" score, obscuring a sophisticated rhetorical strategy. The data reveals that generalized hostility (`enmity`) is constructed and then justified through a specific, material grievance classified as `envy`.

The Sanders text first establishes a clear antagonist through broad, hostile statements like, "The rich want to get richer and they don't care who they step on" and "The worst and most dangerous addiction we have is the greed of the oligarchs." These are correctly identified as `enmity`. However, the system's classification of "There has been a $75 trillion transfer of wealth from the bottom 90% to the top 1%" as `envy` is the crucial anomaly. This specific data point provides the *causal justification* for the enmity. It reframes the conflict not as simple dislike, but as a righteous response to a quantifiable loss. This two-step emotional structure—stoking hostility and then grounding it in a perceived injustice of possession—is a pattern invisible to statistical tools that lack this emotional granularity. The stark contrast with the direct, uncomplicated `amity` in McCain's speech ("we are fellow Americans") further highlights the complexity of this layered negative appeal.

### Insight 6: Identity Forged by Internal vs. External Threats

An unexpected correlation emerges between the *target* of a speaker's rhetoric and the type of collective identity they construct. The evidence reveals two distinct, opposing models for defining the political "we": one forged by identifying an internal enemy, and another by appealing to a shared identity that transcends internal conflict.

The discourse of Bernie Sanders exemplifies the first model. His rhetoric systematically constructs an internal enemy—the "oligarchs"—by attributing malicious intent (`enmity`: "The rich want to get richer and they don't care who they step on") and invoking existential threats (`fear`: "They are prepared to destroy Social Security..."). This antagonistic framing serves a specific purpose: to create a collective identity based on opposition to this internal foe. The resulting political goal is explicitly divisive, or `fragmentative`, aiming to "not accept an oligarchic form of society." Here, the "we" is defined by who "we" are fighting against inside our own nation.

In stark contrast, John McCain's discourse models a unified identity by framing disunity itself as the primary threat. Even in the context of a major political loss, his language of `amity` ("Whatever our differences, we are fellow Americans...") elevates a shared national identity above partisan conflict. While Sanders' rhetoric fragments the polity to mobilize one group against another, McCain's seeks to cohere it by appealing to a superordinate identity. The core insight is that political identity is not a static concept; it is actively constructed by framing the primary threat as either an enemy within the gates or the collapse of the walls themselves.


## Technical Transparency
**Investigation Log**: 15 evidence queries performed
**Models Used**: Synthesis: vertex_ai/gemini-2.5-pro
**Evidence Interrogation**: Active RAG-powered investigation


---

## Research Transparency: Computational Cost Analysis

### Cost Summary
**Total Cost**: $0.1146 USD  
**Total Tokens**: 39,691  
**Run Timestamp**: 20250809T022711Z  

### Cost Breakdown by Operation
- **Raw Data Analysis Planning**: $0.0475 USD (18,130 tokens, 1 calls, $0.0475 avg/call)
- **Derived Metrics Analysis Planning**: $0.0672 USD (21,561 tokens, 1 calls, $0.0672 avg/call)

### Cost Breakdown by Model
- **vertex_ai/gemini-2.5-pro**: $0.1146 USD (39,691 tokens, 2 calls)

### Cost Breakdown by Agent
- **RawDataAnalysisPlanner**: $0.0475 USD (18,130 tokens, 1 calls)
- **DerivedMetricsAnalysisPlanner**: $0.0672 USD (21,561 tokens, 1 calls)

### Methodology Note
This research was conducted using the Discernus computational research platform, ensuring complete transparency in computational costs. All LLM interactions are logged with exact token counts and costs for reproducibility and academic integrity.

**Cost Calculation**: Based on provider pricing at time of execution  
**Token Counting**: Exact tokens reported by LLM providers  
**Audit Trail**: Complete logs available in experiment run directory  
