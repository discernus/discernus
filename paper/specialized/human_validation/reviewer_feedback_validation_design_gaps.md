# Reviewer Feedback: Human Validation Study Design Gaps

**Date:** December 2024  
**Source:** External Reviewer Feedback  
**Status:** Under Consideration  
**Priority:** High - Methodological Rigor  

## Summary

A reviewer identified five critical methodological gaps in our human validation study design that need to be addressed for journal-level acceptance and statistical rigor.

---

## 1. **No mention of inter-rater reliability metric**

### 🔍 Why it matters

If your human raters do not consistently agree on which statement is "closer to" a well (e.g. *Dignity*), then the well's semantic core is unstable—or the raters misunderstood the task. That undermines any comparison between human ratings and LLM-generated scores.

### ✅ What to do

**Add inter-rater reliability (IRR)** as a key outcome metric alongside model-human agreement.

#### Recommended metrics:

* **Fleiss' Kappa**: Use when 3+ raters judge the same set of triplets. Measures agreement beyond chance.
* **Krippendorff's Alpha**: More flexible; handles ordinal and missing data better.
* **Cohen's Kappa**: Only valid if you use 2 raters per item.

#### Example implementation:

For each triplet, ask 5 human raters:

> "Which of the following two statements is *closer to Justice*?"

Then compute IRR on the binary labels they give. If Fleiss' Kappa < 0.4, revisit your well definitions or rater instructions.

---

## 2. **Single-source raters risk**

### 🔍 Why it matters

If all raters share similar cultural, political, or religious priors, they may converge on judgments that an LLM also mimics—giving you a false sense of model-human agreement. This is especially critical since your framework (Civic Virtue) has normative grounding.

### ✅ What to do

**Stratify rater recruitment** by ideological or epistemic tradition.

#### Practical approach:

* **Use screening questions** to classify raters into liberal, communitarian, conservative, or internationalist frames.
* **Balance your panels** so each triplet is rated by a mix of viewpoints.

#### Example:

If a triplet compares:

* "We must protect the weak through shared sacrifice."
* "No one is owed anything; we each rise or fall on merit."

Liberal raters may favor the first as closer to *Dignity*, while libertarian raters might do the opposite. Capturing this divergence is *the point*—not noise.

---

## 3. **No null model baseline**

### 🔍 Why it matters

You need to show that LLMs outperform trivial baselines. Otherwise, any alignment might be due to label bias or dataset skew.

### ✅ What to do

Add at least **two baselines**:

#### (A) **Random vector baseline**

* Assign random 10D vectors to each statement.
* Compute cosine similarity to the well vector.
* Compare rank-order performance to LLM vectors.

#### (B) **Majority sentiment model**

* For each well, use a simplistic rule like: "assign +1 if statement is emotionally positive, −1 if negative."
* This mimics naive sentiment analysis and tests whether your gravity metric adds anything beyond tone.

#### Reporting

* Include these in a comparative ROC-AUC or rank correlation chart.
* If your LLM score doesn't significantly outperform both, it's not learnable or valid.

---

## 4. **Unclear human training protocol**

### 🔍 Why it matters

If humans don't *internalize the well definitions*, their ratings become noise. Especially since your wells are abstract (e.g., *Truth*, *Fantasy*, *Resentment*), raters need a **shared interpretive lens**.

### ✅ What to do

Build a 1–2 page **Rater Primer PDF** with:

1. **Plain-language definition** of each well.
2. **Distinguishing pairs**: e.g., how *Pragmatism* differs from *Fantasy*.
3. **2–3 annotated triplet examples**:

   * Show two statements judged relative to one well.
   * Explain why one is closer than the other.
4. Optional: Add a short quiz (3–5 items) and exclude those who fail it.

#### Bonus

Include links to a short video or audio primer—especially if raters are remote and paid (e.g., via Prolific or Positly).

---

## 5. **Triplet size and statistical power unaddressed**

### 🔍 Why it matters

You need a **minimum number of annotated triplets** to confidently claim that a model is more aligned than chance. Too few → false positives; too many → wasted rater budget.

### ✅ What to do

Run a **power analysis** using expected effect size. You're comparing ranks or match rates, so you can use:

#### A. **Simulation-based power analysis**

Use bootstrapping:

* Simulate N triplets × K raters.
* Sample from plausible agreement rates (e.g. 65% human-model agreement).
* Estimate needed N for p < 0.05 at 80% power.

#### B. **Analytical estimate**

For Kendall's Tau or Spearman's Rho as a performance metric, use G\*Power or Python `statsmodels` to compute needed sample size to detect a medium effect (ρ ≈ 0.3) with α = 0.05 and β = 0.2.

#### Rough estimate

To detect a moderate difference (effect size d ≈ 0.5) with 5 raters per triplet:

* \~100–150 triplets per well should be sufficient.
* \~10 wells = \~1,000–1,500 total comparisons.

You can start with 3 wells to pilot feasibility.

---

## Reviewer's Final Assessment

> These are solvable with modest effort—and fixing them gives your results a shot at **journal acceptance**, not just internal confidence. I can help you draft:
> 
> * A power simulation notebook
> * A rater onboarding packet
> * JSON spec updates to integrate null baselines
> 
> Want to move forward on one of those now?

## Implementation Recommendations

### Phase 1: Pilot Study (Immediate)
**Scope:** Test with 3 wells instead of 10
- **Dignity** vs **Tribalism** (current focus)
- **Truth** vs **Fantasy** 
- **Justice** vs **Resentment**

**Sample size:** 50 triplets × 5 raters = 250 judgments per well
**Budget:** ~$1,500-2,000 for quality raters

### Phase 2: Power Analysis
**Use G*Power or Python to calculate:**
- Target effect size: d = 0.5 (moderate)
- Power: 80% (β = 0.2)
- Alpha: 0.05
- **Result:** ~100-150 triplets per well needed

### Phase 3: Rater Training Protocol
**Create 2-page primer with:**
- Well definitions in plain language
- Distinguishing pairs between similar wells
- 2-3 annotated triplet examples
- Optional qualification quiz

## Next Steps Required

1. **Inter-rater reliability metrics** - Add Fleiss' Kappa calculation
2. **Diversify rater pool** - Recruit across ideological spectrum
3. **Implement null baselines** - Random vector and sentiment baselines
4. **Create rater training** - Comprehensive primer document
5. **Power analysis** - Statistical sample size calculation

## Status: Pending Review and Integration

This feedback needs to be carefully considered and integrated into our validation study design before proceeding with large-scale human validation experiments. 