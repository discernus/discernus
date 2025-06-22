# Discernus Terminology Strategy & Lexicon  
*Version 1.0 — 2025-06-22*

---

## Bottom‑Line‑Up‑Front  
Discernus is abandoning the pseudo‑physics “Narrative Gravity” metaphor in favor of a cartographic vocabulary that is (1) empirically grounded, (2) extensible to new frameworks, and (3) clear to interdisciplinary readers. The new language distinguishes **anchors** (fixed perimeter references), **axes** (anchor pairs), and **signatures** (per‑document vectors), so every plotted object carries a name that reflects **function, not geometry**.

---

## 1. Why We’re Changing the Language  

| Driver | Pain Point in Old Terms | Solution in New Terms |
|--------|------------------------|-----------------------|
| **Academic Credibility** | “Gravity wells” implied unverifiable forces. | Neutral cartographic references. |
| **Framework Diversity** | “Dipole” presumes exactly two poles. | *Axis‑Set* vs *Anchor‑Set* frameworks. |
| **Visualization Flexibility** | Ellipse math hard‑wired to charts. | Geometry‑agnostic data layer. |
| **Onboarding Clarity** | Users confused “well” vs “point”. | Role‑based nouns (anchor, axis, centroid). |

The rename is therefore **collective**—retiring the entire physics metaphor—and **individual**—each legacy object gets a clear successor term.

---

## 2. Terminology‑Assignment Principles  

1. **Role over Shape** Names describe what the object *does* in analysis, not how it looks.  
2. **Mutual Exclusivity** No two roles share a noun; no noun covers multiple roles.  
3. **Scalability** New frameworks must inherit names without inventing exceptions.  
4. **Metaphor Discipline** One metaphor at a time—cartography. Avoid optics, physics, or medicine.  
5. **Reader Empathy** Favor textbook words (centroid) over jargon (center‑of‑mass) whenever tied.  

---

## 3. Glossary  

| Term | Definition | Example Sentence |
|------|------------|------------------|
| **Anchor** | A fixed reference point on the unit circle’s perimeter representing a semantic extreme (e.g., *Populism*). | “The speech leans 0.72 toward the Populism **anchor**.” |
| **Axis** | A dimension formed by two opposing anchors. | “The *Populism–Pluralism* **axis** captures attitudes toward collective sovereignty.” |
| **Axis Set** | The complete collection of axes defined by an Axis‑Set Framework. | “Civic Virtue’s **axis set** contains five moral dimensions.” |
| **Anchor Cluster** | Two or more anchors intentionally placed within a shared arc to amplify a direction. | “Virtue‑related anchors form an **anchor cluster** in the upper quadrant.” |
| **Axis Signature** | A radar polygon showing a document’s scores along every axis. | “Figure 2 overlays the **axis signature** of right‑wing outlets.” |
| **Anchor Signature** | A radar polygon showing scores toward independent anchors (no opposing poles). | “Thunberg’s UN speech has a strong **anchor signature** toward Intersectionality.” |
| **Centroid** | The arithmetic mean of several signatures, summarizing a corpus or cluster. | “Over eight months, the campaign’s **centroid** drifted 15° toward Pluralism.” |
| **Weighting Scheme / Axis Salience** | Scalars that modulate each axis when computing distances or centroids. | “We applied a 1.5 **salience** to the Morality axis.” |
| **Axis‑Set Framework (ASFx)** | A framework comprising paired anchors that form axes (e.g., Civic Virtue). | “Civic Virtue is implemented as an **Axis‑Set Framework**.” |
| **Anchor‑Set Framework (ASFa)** | A framework comprising independent anchors with no opposing poles (e.g., Three Theories). | “Three Theories is modeled as an **Anchor‑Set Framework**.” |
| **Discernus Coordinate System (DCS)** | The shared geometric space in which all anchors, signatures, and centroids are plotted. | “All frameworks ultimately project into the **DCS**.” |
| **Framework** | A theory‑driven scoring schema (YAML + prompts) that outputs anchor or axis scores. | “Users can upload a new **framework** via the API.” |

---

## 4. Example Sentences in Context  

1. *“Applying the Civic Virtue **Axis‑Set Framework**, we generated an **axis signature** for each speech and observed that the month‑end **centroid** now sits closer to the Integrative **anchor cluster**.”*  
2. *“Because Three Theories is an **Anchor‑Set Framework**, its **anchor signature** has no opposing poles; nevertheless, its **centroid** plots seamlessly in the **DCS**.”*  
3. *“Increasing the **salience** of the Pluralism **anchor** by 0.25 moved the debate’s **centroid** twelve degrees counter‑clockwise.”*  

---

## 5. Multi‑Paragraph Writing Sample  

> **Paragraph 1 – Orientation**  
> Discernus maps narratives the way cartographers map terrain. At the edge of every map lie **anchors**—fixed semantic landmarks such as *Populism* or *Pluralism*. Two opposing anchors form an **axis**, and a framework’s full **axis set** establishes the coordinate grid on which texts are plotted.
>
> **Paragraph 2 – Plotting Documents**  
> Each document receives an **axis signature**, a multi‑spoke polygon that stretches toward anchors in proportion to the evaluator’s scores. Signatures from dozens of speeches coalesce into a luminous field whose geometric center—the **centroid**—tells the story of a movement’s average position.
>
> **Paragraph 3 – Handling Independent Anchors**  
> Not every framework is bipolar. In the **Three Theories Anchor‑Set Framework**, the anchors stand alone like solitary beacons. Documents therefore receive an **anchor signature**, reaching toward *Intersectionality*, *Tribal Domination*, and *Pluralist Dignity* without implying a missing opposite. Yet these signatures plot in the same **Discernus Coordinate System**, preserving cross‑framework comparability.
>
> **Paragraph 4 – Modulating Meaning**  
> Discernus lets researchers adjust **axis salience** to spotlight what matters. Boosting the Moral Foundations axis by 50 % in the Civic Virtue study shifted the cluster’s **centroid** closer to the Integrative **anchor cluster**, revealing how value‑laden rhetoric drives ideological drift.
>
> **Paragraph 5 – Looking Forward**  
> Tomorrow’s scholars may demand UMAP scatterplots or dendrograms instead of radar charts. Because Discernus stores **axis signatures** and **centroids** as plain vectors inside the DCS, any visualization is just an adapter away. The map’s legend stays stable even as the canvas evolves.

---

## 6. Applying the Principles to Future Terms  
1. **Detect the Role** Ask first: what analytic function does the object serve?  
2. **Check for Exclusivity** Ensure the role isn’t already named.  
3. **Align with Metaphor** If the role lives on the map, use cartographic language; if not, pick a new unambiguous metaphor.  
4. **Stress‑Test for Scalability** Can the term handle edge cases such as multi‑pole designs or higher‑dimensional embeddings?  
5. **Document Immediately** Update this lexicon and add a linter rule before the term enters production code.

---

*Prepared June 22, 2025.*  
