# Experiment Report

## Evidence-Backed Hypothesis Testing

### H1: Institutional Cohesion

**Hypothesis**: McCain's institutional concession will demonstrate higher overall cohesion indices (dignity, hope, amity, cohesive goals) reflecting democratic norms of gracious transition

**Conclusion**

Based on the available evidence, the hypothesis is **INCONCLUSIVE** from a quantitative standpoint, but **qualitatively supported** by the textual data. A definitive statistical conclusion cannot be reached as no aggregate numerical data (e.g., mean cohesion scores, frequency distributions) were provided for comparison. However, a qualitative analysis of the classified textual excerpts strongly aligns with the hypothesis that McCain's concession speech would feature prominent themes of democratic cohesion.

The textual evidence from McCain’s 2008 concession speech consistently demonstrates high-confidence classifications in categories central to the hypothesis. The theme of **amity** is explicitly articulated in his unifying statement, "Whatever our differences, we are fellow Americans" [john_mccain_2008_concession.txt, amity, conf: 0.95], which frames the political contest within a superordinate national identity. This contrasts sharply with the oppositional framing found in other political discourse, such as the classification of "enmity" [bernie_sanders_2025_fighting_oligarchy.txt, enmity, conf: 0.90].

Furthermore, McCain’s speech actively confers **dignity** upon his opponent and his supporters, a key norm in a gracious transition. He commends Senator Obama for "inspiring the hopes of so many millions of Americans" [john_mccain_2008_concession.txt, individual_dignity, conf: 0.95] and acknowledges shared beliefs about opportunity while recognizing the "old injustices that once stained our nation's reputation" [john_mccain_2008_concession.txt, individual_dignity, conf: 0.90]. This rhetoric validates the political struggle and victory of the opposing side.

Finally, the speech is anchored by an appeal to **cohesive goals**, directly calling for future collaboration by "offering our next president our good will and earnest effort to find ways to come together, to find the necessary compromises to bridge our differences" [john_mccain_2008_concession.txt, cohesive_goals, conf: 0.95]. This forward-looking statement is foundational to the peaceful transfer of power, framing the post-election period as one of national unity rather than continued partisan conflict.

It is crucial to acknowledge the limitations of this analysis. The conclusion is drawn from a very small sample size of classified excerpts (N=8 unique samples). Without comprehensive statistical evidence comparing the overall distribution of discourse codes across the full texts, we cannot statistically validate the hypothesis. A robust test would require aggregate metrics demonstrating that cohesion indices are significantly more prevalent in McCain's speech than in a comparable corpus of non-concession political speeches. Nonetheless, the available textual samples provide a consistent and compelling qualitative indication that McCain's concession was rhetorically constructed to reinforce the democratic norms of a gracious and cohesive political transition.

### H2: Populist Fragmentation

**Hypothesis**: Sanders' populist critique will show higher fragmentative elements (tribal dominance, enmity) but with strategic contradictions indicating sophisticated rhetorical positioning

### Conclusion: Synthesis of Findings

Based on the provided textual evidence, the hypothesis is **SUPPORTED**, albeit with significant limitations. The analysis indicates that Sanders' discourse contains the predicted combination of highly fragmentative elements and strategically contradictory cohesive frames. However, the absence of statistical evidence and the small sample size prevent a definitive conclusion.

The first component of the hypothesis—that Sanders' populist critique exhibits high fragmentative elements—is substantiated by the textual data. The discourse model identified strong instances of `enmity` and `fragmentative_goals`. For example, the statement, "The rich want to get richer and they don't care who they step on" (Sanders, 2025), was classified as `enmity` with high confidence (0.90). This rhetoric establishes a clear antagonist ("the rich") and attributes malicious intent, a core feature of fragmentative discourse. Similarly, the declaration, "We will not accept an oligarchic form of society" (Sanders, 2025), was coded as `fragmentative_goals` (conf: 0.90), framing the political project as a struggle against a specific societal structure and its proponents, thereby creating a clear in-group/out-group dynamic.

The second component of the hypothesis—the presence of strategic contradictions indicating sophisticated rhetorical positioning—is also supported. Alongside the divisive frames, Sanders employs language of `amity`. The call to action, "if we stand together, are strong, are disciplined, are smart...we can create the kind of nation that we deserve" (Sanders, 2025), was classified as `amity` (conf: 0.80). The juxtaposition of this cohesive, aspirational language with the aforementioned enmity-laden rhetoric is the central contradiction. This allows the speaker to mobilize a base through a narrative of conflict while simultaneously framing the ultimate objective in unifying and positive terms, a hallmark of sophisticated populist strategy. This pattern is distinct from the uniformly cohesive rhetoric found in the control sample from McCain, which consistently features themes of `amity`, `individual_dignity`, and `cohesive_goals` (McCain, 2008).

**Limitations:**
This conclusion must be interpreted with caution due to two primary limitations. First, the statistical evidence was not provided. Without quantitative data on the relative frequency of these discourse frames across a larger corpus, we cannot validate the "higher" prevalence of fragmentation or assess the statistical significance of the observed contradictions. Second, the textual sample size is extremely small (N=8 unique excerpts), which severely limits the generalizability of these findings. While the qualitative evidence aligns perfectly with the hypothesis, a robust and defensible conclusion would require a large-scale computational analysis across a comprehensive dataset.

### H3: Democratic Patterns

**Hypothesis**: The two discourse types will exhibit distinct social cohesion signatures corresponding to institutional versus populist democratic approaches

Based on the provided evidence, the following conclusion can be drawn:

**Conclusion: Hypothesis Supported**

The analysis of the provided textual evidence **SUPPORTS** the hypothesis that institutional and populist discourse types exhibit distinct social cohesion signatures. The institutional discourse, represented by John McCain's 2008 concession speech, is characterized by rhetoric aimed at national unity, procedural legitimacy, and bridging divides. In contrast, the populist discourse, exemplified by Bernie Sanders' 2025 speech on fighting oligarchy, constructs social cohesion by mobilizing an in-group against a perceived antagonistic out-group.

The institutional signature is clearly visible in the excerpts from McCain's speech, which are consistently classified with pro-social, unifying codes. The discourse emphasizes a superordinate national identity that transcends political differences, as seen in the repeated expression of `amity`: "Whatever our differences, we are fellow Americans" (john_mccain_2008_concession.txt). This is reinforced by the articulation of `cohesive_goals`, such as the call to "find ways to come together... to bridge our differences" (john_mccain_2008_concession.txt). Furthermore, this discourse type validates the democratic process and the dignity of all participants, including political opponents, through expressions of `compassion` and respect for `individual_dignity` (john_mccain_2008_concession.txt). This rhetorical pattern functions to repair societal divisions and reinforce the stability of the political system.

Conversely, the populist signature evident in Sanders' speech builds cohesion through a different mechanism: demarcation and opposition. The primary tool is the creation of an out-group, coded as `enmity`: "The rich want to get richer and they don't care who they step on" (bernie_sanders_2025_fighting_oligarchy.txt). This antagonism directly informs the movement's objectives, which are framed as `fragmentative_goals` in opposition to the established order: "We will not accept an oligarchic form of society" (bernie_sanders_2025_fighting_oligarchy.txt). While this discourse also contains expressions of `amity`—"if we stand together... we can create the kind of nation that we deserve" (bernie_sanders_2025_fighting_oligarchy.txt)—this solidarity is conditional and directed toward the in-group ("we") in its struggle against the out-group ("oligarchy," "Trumpism"). This contrasts sharply with the universal, unconditional `amity` expressed in the institutional example.

**Limitations**

It is imperative to acknowledge the limitations of this analysis. The conclusion is based on a qualitative assessment of a small sample of ten textual excerpts from only two speeches. No quantitative statistical evidence was provided (Statistical Evidence: {}), which prevents an analysis of the relative frequency or statistical significance of these cohesion signatures across the entirety of the discourses. Therefore, while the available evidence provides a clear, illustrative distinction that supports the hypothesis, these findings cannot be generalized without a larger, more systematically sampled dataset and accompanying statistical analysis.


## Beyond the Hypotheses: Computational Insights

*Leveraging billion-dollar pattern recognition to discover insights beyond experimental design*

### Insight 1: The Superlative Shift: From Unifying Emotion to Systemic Crisis

A subtle but significant pattern emerges in how speakers from different eras use historical superlatives to frame the present moment. Both John McCain in 2008 and Bernie Sanders in the modern era employ the same rhetorical device—claiming the present is a unique peak in history—but for diametrically opposed purposes. This reveals a shift in the function of political framing, from invoking shared identity to highlighting systemic conflict.

McCain, in a moment of political concession, uses a superlative to express a peak of unifying, personal emotion: "no association has ever meant more to me than that [of being fellow Americans]." Here, the "ever" serves to elevate a shared, positive identity above political differences, fostering amity. In contrast, Sanders uses the identical structure to declare a peak of negative, systemic crisis: "more concentration of ownership in America than we have ever had." For Sanders, the "ever" serves to quantify an unprecedented economic threat, defining a tribal conflict between oligarchs and citizens. The same linguistic tool used to express the ultimate unifying value in one era is repurposed in another to define the ultimate divisive problem.

### Insight 2: Rhetorical Divergence: Acknowledging Grievance vs. Targeting Resentment

The evidence does not reveal a speaker combining manipulation and resentment. Instead, it uncovers a more nuanced, non-obvious pattern: a fundamental divergence between a speaker who acknowledges the *source* of resentment to build cohesion, and another who defines a *target* for resentment to create fragmentation. The tactics appear to be mutually exclusive strategies for mobilizing support.

John McCain, in his concession, employs a strategy of absorptive cohesion. He explicitly recognizes a historical grievance with the potential to cause division, stating that "the memory of [old injustices] still had the power to wound." However, he immediately neutralizes this by framing it as a shared challenge he and his opponent both recognize. This tactic acknowledges the legitimacy of the grievance while simultaneously folding it into a unifying, forward-looking narrative of `cohesive_goals`. In contrast, Bernie Sanders' rhetoric, classified as `fragmentative_goals`, isolates a specific antagonist: "We will not accept an oligarchic form of society." This approach does not seek to absorb or reframe grievance but to channel it, creating a clear in-group/out-group dynamic essential for resentment-based mobilization. The insight is not that a speaker combines these tactics, but that they represent two opposing poles for handling societal discontent.

### Insight 3: Rhetorical Fusion as a Marker of Authenticity

The evidence reveals that speaker authenticity is not merely conveyed by the presence of salient themes, but by their *rhetorical fusion* within a single, complex thought. The system's repeated, high-confidence identification of multiple distinct concepts—`hope`, `individual_dignity`, and `compassion`—within the exact same sentence is the key pattern. This indicates the speaker is not simply listing values, but weaving them into an integrated, nuanced statement that is difficult to fabricate.

For instance, McCain's statement, "But that he managed to do so by inspiring the hopes of so many millions of Americans who had once wrongly believed that they had little at stake...is something I deeply admire and commend him for achieving," is simultaneously tagged for all three concepts. He doesn't state them separately. Instead, his personal `compassion` ("I deeply admire") is presented as a direct result of his opponent's success in restoring `hope` and `individual_dignity` to citizens. This fusion of personal admiration with a rival's specific, positive impact on the electorate creates a powerful and authentic expression of respect, moving beyond political platitudes to a genuine acknowledgment of a shared democratic ideal.

### Insight 4: From Shared Wounds to Active Enemies: The Shifting Locus of Political Problems

The evidence reveals a fundamental evolution in civic discourse, not just in tone, but in the conceptual framing of societal problems. The locus of conflict appears to have shifted from healing shared historical wounds to fighting an active, malevolent class enemy. This pattern suggests the nature of the perceived adversary has been redefined over time, moving from a political rival to a moral foe.

This shift is starkly illustrated by comparing the two speakers. In 2008, John McCain framed national challenges as a collective burden, acknowledging that while he and his opponent shared core beliefs, the "memory of [old injustices] still had the power to wound." The problem is a shared, historical pain point within a unified nation. By contrast, the 2025 discourse frames the problem as a present-day enemy with malicious intent. Bernie Sanders targets a specific group—"The rich"—and claims "they don't care who they step on." The goal is no longer healing a wound but defeating an active antagonist to prevent an "oligarchic form of society." The adversary has evolved from a political opponent within a shared system to a corrupt class that must be vanquished.

### Insight 5: Enmity Targets Action, Amity Targets Identity

The evidence reveals an asymmetric pattern in how high-confidence `enmity` and `amity` are rhetorically constructed. The system's `enmity` classifications are triggered not just by negative sentiment, but by the specific framing of an out-group's malevolent *actions* and *character flaws*. The antagonist is defined by what they do. For example, the "oligarchs" are characterized by their "greed" and their willingness to "step on" others, creating a tangible, active enemy.

In contrast, the high-confidence `amity` classification is achieved by appealing to a shared, abstract *identity* that transcends conflict. John McCain's statement, "Whatever our differences, we are fellow Americans," generates amity by invoking a state of *being* rather than a set of positive actions. The insight is that political enmity is constructed around what a group *does*, while political amity is constructed around what a group *is*. This distinction explains the statistical confidence: defining an enemy by their actions is a clear rhetorical signal, just as appealing to a foundational shared identity is a clear signal for unity.

### Insight 6: The Antagonist as a Unifying Construct

An unexpected pattern emerges when contrasting the function of the "enemy" in different political discourses. The evidence suggests that enmity-driven rhetoric, far from being purely divisive, can serve as a primary tool for in-group unification. Bernie Sanders' discourse constructs a political reality that *requires* a clearly defined antagonist to cohere. The "we" is defined by its opposition to "they." This is evident when the "greed of the oligarchs" is framed as an active, malevolent force "prepared to destroy Social Security," creating a clear threat that binds a collective who "will not accept an oligarchic form of society." The enemy is the central organizing principle.

This contrasts sharply with John McCain's rhetoric, which attempts unification by dissolving conflict into a pre-existing, abstract identity. By stating, "Whatever our differences, we are fellow Americans," McCain invokes a shared identity that supersedes any specific antagonist. The unifying principle is internal and historical, not external and oppositional. The surprising insight is not simply that one speaker uses enmity and another uses amity, but that for one, the enemy is a necessary structural component for creating a unified "we," while for the other, the absence of a defined enemy is the entire point.


## Technical Transparency
**Investigation Log**: 15 evidence queries performed
**Models Used**: Synthesis: vertex_ai/gemini-2.5-pro
**Evidence Interrogation**: Active RAG-powered investigation


---

## Research Transparency: Computational Cost Analysis

### Cost Summary
**Total Cost**: $0.1046 USD  
**Total Tokens**: 38,235  
**Run Timestamp**: 20250809T022141Z  

### Cost Breakdown by Operation
- **Raw Data Analysis Planning**: $0.0499 USD (17,929 tokens, 1 calls, $0.0499 avg/call)
- **Derived Metrics Analysis Planning**: $0.0546 USD (20,306 tokens, 1 calls, $0.0546 avg/call)

### Cost Breakdown by Model
- **vertex_ai/gemini-2.5-pro**: $0.1046 USD (38,235 tokens, 2 calls)

### Cost Breakdown by Agent
- **RawDataAnalysisPlanner**: $0.0499 USD (17,929 tokens, 1 calls)
- **DerivedMetricsAnalysisPlanner**: $0.0546 USD (20,306 tokens, 1 calls)

### Methodology Note
This research was conducted using the Discernus computational research platform, ensuring complete transparency in computational costs. All LLM interactions are logged with exact token counts and costs for reproducibility and academic integrity.

**Cost Calculation**: Based on provider pricing at time of execution  
**Token Counting**: Exact tokens reported by LLM providers  
**Audit Trail**: Complete logs available in experiment run directory  
