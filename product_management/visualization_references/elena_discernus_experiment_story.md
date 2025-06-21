# Gravity Wells

---

Elena Verhoeven hunched over her monitor in the faculty lounge at Georgetown’s Department of Communication, the soft hum of her laptop drowned beneath the low tide of summer air conditioning. Her browser window glowed with the Discernus dashboard—version 2.7, running a custom experiment she’d configured at 2 a.m. the night before. The corpus she had fed it was both politically curated and rhetorically volatile: fifty political speeches hand-sorted into folders like `conservative_dignity`, `progressive_tribalism`, and `mixed_controls`.

Her experiment: score every speech using the **Moral Foundations Theory (MFT)** framework—both through four different LLMs and a panel of Mechanical Turk raters—and compare those against the categories she had annotated manually. It was a test of Discernus’s architecture, of the LLMs’ internalized moral lexicons, and of the underlying hypothesis she couldn’t let go of: *the tribal vs dignity axis isn’t about ideology—it’s about moral style.*

---

## Day 1: First Results

At 10:47 a.m., the Discernus job log pinged complete. Elena clicked into the visualization pane.

**First up: the elliptical map for Bernie Sanders, 2025.**  
Claude had scored this one five times. On the ellipse, she saw the familiar poles: Dignity, Justice, Truth, Hope on the upper arc; Fear, Resentment, Manipulation, Tribalism on the lower.

A **blue “Narrative Center” dot** hovered at (–0.02, –0.61). Just south of the ellipse’s equator. Elena frowned—not because it was wrong, but because it confirmed her suspicions. The disintegrative wells were strong: high **Resentment** (0.7), moderate **Fear** (0.5), and a disturbing **Manipulation** score of 0.4. But what stood out was **Tribalism**: 0.8.

The composite summary rendered on the right read:

> “This speech constructs a populist moral architecture emphasizing betrayal by corporate elites, elite oligarchs, and political insiders. It frames unity as conditional upon ideological purity, using strong ‘us-vs-them’ boundaries and rhetorical cleansing of dissent.”

That wasn’t *just* what Sanders said. That was *how* he said it.

---

## Variance and Stability

She toggled to the second dashboard: *variance plots* comparing LLMs. For this speech, GPT-4o had rendered a coherence index of 0.63 and directional purity of 0.91—strong and consistent. But Claude showed **volatility**. Across five runs, its **Hope** score swung between 0.2 and 0.6.

She squinted at the bar graphs. Claude over-weighted the redemptive lines; GPT-4o saw the aggression and judgment. Llama 3? Flat. Dull. An average of 0.33 across all wells, like it didn’t know what a moral vector was.

> “It's not hallucinating,” Elena muttered. “It’s just not *feeling* it.”

---

## Comparison Plot: McCain vs Trump

She loaded two more panels. Both labeled “conservative.” One was McCain’s 2008 concession; the other, Trump’s fictional 2029 second inaugural from her “AI-augmented rhetorical modeling” corpus.

The ellipse told the story at a glance.

- **McCain’s center**: (0.003, 0.45), near Dignity and Hope.  
- **Trump’s center**: (–0.01, –0.62), buried in the disintegrative field.

Where McCain spiked high in **Pragmatism** and **Justice**, Trump shot upward in **Tribalism** (0.9), **Fear** (0.7), and **Fantasy** (0.6). Elena traced the blue dashed lines with her mouse, watching them ripple toward their poles.

Then she flipped to the composite summary:

> “Populist narrative emphasizing American exceptionalism through existential grievance. High tribalism via exclusionary language and cultural signaling. Minimal integrative wells suggest erosion of shared civic identity in favor of loyalty-based legitimacy.”

Elena’s heart sank—and then surged. This wasn’t just about *who said what.* It was how they *constructed legitimacy.*

---

## Day 3: Human vs Model

The Mechanical Turk ratings came in late Wednesday night. Elena fed them into Discernus. Within minutes, she had a comparative heatmap: LLMs vs. Humans across all five moral foundations.

The best aligned? **GPT-4o** on **Care** and **Fairness**, with Pearson r of 0.86 and 0.78, respectively. But **Loyalty** and **Sanctity**? A mess. LLMs over-applied purity metaphors—even to secular progressive speeches.

Elena opened a difference map. The **progressive tribalism** set—speeches by AOC, Kendi, DiAngelo—scored *higher* in Purity and Loyalty with GPT-4 than with humans.

> “It’s detecting moralization where the crowd hears policy,” she whispered.

That, in itself, was a finding.

---

## Night 5: Narrative Trajectories

Elena linked the files chronologically.

- **Obama 2004 → 2009 → 2012**  
- **Bush 1999 → 2001 → 2004**

She plotted their narrative centers on the ellipse, linked with a gray arc.

Obama’s arc curved **upward**: from Pragmatism toward Dignity and Truth. Bush’s stayed mostly flat, centered between Justice and Hope—but his 2004 speech dipped: higher Fear, lower Coherence.

The dashboards called it “a drift toward rhetorical safeguarding.” Elena called it: *post-9/11 trauma in policy clothing.*

---

## Writing It Up

By Sunday, her draft was 4,000 words and growing. She called the framework **Moral Gravity Drift Analysis** and the paper *Rhetorical Signature as Strategic Identity: An Empirical Study of Integrative vs. Disintegrative Moral Framing in U.S. Political Discourse.*

Her final table cross-tabulated:

- **Speech Category** (Dignity, Tribalism, Mixed)
- **Mean Well Score per Moral Pole**
- **Contradiction Index**
- **Human-LLM Alignment Coefficients**
- **Narrative Coherence vs Polarity**

It showed what she needed it to show: that rhetorical worldview **is measurable**, **modelable**, and **predictively coherent**. Not just noise. Not just style. Structure.

---

## Epilogue: The Dashboard Moment

Late Sunday night, she pushed her chair back and watched the **Bush 2001 dashboard replay** on loop.

The Narrative Center glowed softly at the ellipse’s midpoint—just slightly above center. The green bars rose high in **Dignity**, **Truth**, and **Justice**. The red ones—**Fear**, **Resentment**, **Tribalism**—barely flickered.

> *A shared civic myth*, she thought. *Not because it was perfect—but because it was balanced.*

And maybe that was what Discernus had shown her most of all.

You didn’t need a perfect speech.  
You needed one that **knew where its gravity pulled from**.

She clicked **Export** and let the dashboard save itself to posterity.
