# Populist Discourse Analysis Framework (PDAF) v9.0

---

## Part 1: The Scholarly Document

### Section 1: Abstract & *Raison d'être*

**What is this framework?**
The Populist Discourse Analysis Framework (PDAF) is a specialized analytical tool designed to identify, measure, and analyze the core rhetorical components of populist political communication.

**What problem does it solve?**
Populism is a notoriously difficult concept to define and measure operationally. The PDAF provides a systematic, evidence-based methodology for quantifying the key dimensions of populist rhetoric in a given text, moving beyond subjective interpretation to a more rigorous, repeatable analysis.

**Who is it for?**
This framework is intended for political scientists, communication researchers, journalists, and civic organizations who need to track and understand the prevalence and nature of populist discourse in speeches, manifestos, social media, and other political texts.

### Section 2: Theoretical & Empirical Foundations

The PDAF is grounded in the ideational approach to populism, most prominently articulated by Cas Mudde and Cristóbal Rovira Kaltwasser. This approach defines populism as a "thin-centered ideology" that posits a fundamental antagonism between a virtuous, unified "people" and a corrupt, self-serving "elite."

-   **Mudde, C. (2004).** "The Populist Zeitgeist". *Government and Opposition, 39*(4), 541-563.
-   **Mudde, C., & Kaltwasser, C. R. (2017).** *Populism: A Very Short Introduction*. Oxford University Press.

The framework operationalizes this core concept by defining three measurable dimensions: **Anti-Elitism**, **People-Centrism**, and **Scapegoating**, which together capture the central antagonistic relationship at the heart of populist discourse.

### Section 3: Analytical Methodology

The PDAF scores each of the three core dimensions independently to capture the unique rhetorical profile of a given text.

-   **Dimensions**:
    -   **Anti-Elitism**: Measures the degree to which the text frames a struggle between "the people" and a corrupt, out-of-touch elite (political, economic, cultural).
    -   **People-Centrism**: Measures the degree to which the text appeals to a unified, virtuous, and sovereign "people" as the sole legitimate source of political power.
    -   **Scapegoating**: Measures the degree to which the text blames a specific out-group (e.g., immigrants, minorities, foreign nations) for the problems faced by "the people," often presented as being in league with the elite.

-   **Derived Metrics**:
    -   **Populism Index**: A composite score calculated as `(anti_elitism + people_centrism + scapegoating) / 3`. This provides a single, overarching measure of the intensity of populist rhetoric in the text. A score above 0.5 is considered indicative of significant populist framing.

### Section 4: Intended Application & Corpus Fit

-   **Target Corpus Description**: The PDAF is designed for the analysis of formal political communication, including but not limited to: political speeches, party manifestos, candidate debates, and official social media pronouncements. It is most effective on texts where a clear political argument is being made.
-   **Known Limitations & Scope**: This framework is not intended for analyzing conversational speech, private correspondence, or texts that lack a persuasive political intent. Its effectiveness may be limited on highly ironic or satirical content. The "Scapegoating" dimension, in particular, requires careful contextual interpretation.
-   **System Validation Note**: Be aware that the Discernus platform will perform automated statistical validation of this framework's fit with your chosen corpus. Applying it to a corpus of, for example, scientific articles would likely result in a validation failure.

---

## Part 2: The Machine-Readable Appendix

```yaml
# --- Start of Machine-Readable Appendix ---

# 5.1: Metadata
metadata:
  framework_name: "populist_discourse_analysis_framework"
  framework_version: "9.0.0"
  author: "Discernus Project"
  spec_version: "10.0"

# 5.2: Analysis Variants
analysis_variants:
  default:
    description: "The standard analytical protocol for identifying and scoring the core dimensions of populist rhetoric."
    analysis_prompt: |
      You are an expert political scientist specializing in the study of populism. Your task is to analyze the provided text using the Populist Discourse Analysis Framework (PDAF). You will score three key dimensions of populist rhetoric: Anti-Elitism, People-Centrism, and Scapegoating.
      For each dimension, you must provide:
      1. A `raw_score` from 0.0 to 1.0, representing the intensity and prevalence of the dimension in the text.
      2. Your `confidence` in that score, from 0.0 to 1.0.
      3. A direct quote from the text as `evidence` that best exemplifies your reasoning.
      Adhere strictly to the definitions and linguistic markers provided for each dimension.

# 5.3: Dimensions
dimensions:
  - name: "anti_elitism"
    description: "Measures rhetoric that frames a struggle between 'the people' and a corrupt, self-serving, and out-of-touch elite."
    markers:
      - "corrupt elite"
      - "political establishment"
      - "mainstream media"
      - "globalists"
      - "out of touch"
      - "betrayed the people"
  - name: "people_centrism"
    description: "Measures rhetoric that appeals to a unified, virtuous, and sovereign 'people' as the sole source of legitimacy."
    markers:
      - "the people"
      - "common sense"
      - "silent majority"
      - "real Americans"
      - "will of the people"
      - "we the people"
  - name: "scapegoating"
    description: "Measures rhetoric that blames a specific out-group for the problems of 'the people'."
    markers:
      - "immigrants are taking"
      - "foreigners are the problem"
      - "[minority group] is to blame"
      - "stabbed in the back"
      - "enemies within"

# 5.4: Derived Metrics
derived_metrics:
  - name: "populism_index"
    description: "A composite index measuring the overall intensity of populist rhetoric. Calculated as the average of the three core dimension scores."
    formula: "(dimensions.anti_elitism.raw_score + dimensions.people_centrism.raw_score + dimensions.scapegoating.raw_score) / 3"

# 5.5: Output Schema
output_schema:
  type: object
  properties:
    dimensional_scores:
      type: object
      properties:
        anti_elitism:
          type: object
          properties:
            raw_score: { type: number, minimum: 0.0, maximum: 1.0 }
            confidence: { type: number, minimum: 0.0, maximum: 1.0 }
            evidence: { type: string }
          required: [ "raw_score", "confidence", "evidence" ]
        people_centrism:
          type: object
          properties:
            raw_score: { type: number, minimum: 0.0, maximum: 1.0 }
            confidence: { type: number, minimum: 0.0, maximum: 1.0 }
            evidence: { type: string }
          required: [ "raw_score", "confidence", "evidence" ]
        scapegoating:
          type: object
          properties:
            raw_score: { type: number, minimum: 0.0, maximum: 1.0 }
            confidence: { type: number, minimum: 0.0, maximum: 1.0 }
            evidence: { type: string }
          required: [ "raw_score", "confidence", "evidence" ]
  required:
    - dimensional_scores

# --- End of Machine-Readable Appendix ---
```
