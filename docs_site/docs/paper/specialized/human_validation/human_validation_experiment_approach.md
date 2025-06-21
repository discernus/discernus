## Revised Human Validation Study Plan: Strategic Single-Dipole Validation

### **Executive Summary of Strategic Decisions**

Based on systematic analysis of cognitive load, academic defensibility, and resource optimization, this human validation study employs a **strategic single-dipole approach** focusing on the theoretically most powerful dimension of the Civic Virtue framework. This design maximizes interpretive clarity, minimizes complexity barriers, and provides the strongest foundation for demonstrating computational-human alignment in political discourse analysis.

### **Framework Selection: Single Dipole Civic Virtue (Dignity vs Tribalism)**

**Strategic Rationale:**

- **Theoretical Centrality:** The Identity dipole (Dignity vs Tribalism) represents the Primary Tier (1.0 weighting) in the Civic Virtue framework's theoretical hierarchy, capturing the most psychologically powerful moral-political distinction in virtue ethics approaches to persuasive discourse.
- **Cognitive Optimization:** Single dipole reduces cognitive load by 80% compared to full 5-dipole framework while preserving core theoretical construct validation.
- **Maximum Reliability:** Literature demonstrates that simpler annotation tasks yield higher inter-rater reliability, increasing probability of achieving target ≥0.70 agreement.
- **Clear Success Metrics:** Binary success/failure determination rather than complex multi-dimensional assessment patterns.

**Academic Justification:**
> "To establish proof-of-concept for computational-human alignment in political discourse analysis, we focus validation on the theoretically most powerful dimension of our framework—the Identity dipole (Dignity vs Tribalism)—which represents the primary tier of moral-political distinction in virtue ethics approaches to persuasive discourse. This strategic focus enables rigorous validation of core theoretical constructs while maintaining methodological rigor within resource constraints."

**Implementation Specifications:**

- **Single Question Format:** "On a scale of 1-7, how much does this text emphasize personal dignity and respect (high) vs tribal us-versus-them thinking (low)?"
- **Evidence Requirement:** Annotators highlight 1-2 key passages supporting their scores
- **Simplified Codebook:** 3-5 pages with concrete examples and boundary cases
- **Quality Control:** Single gold standard cases easier to develop and validate


### **Text Selection: Anonymous Political Excerpts Strategy**

**Strategic Rationale:**

- **Bias Elimination:** Anonymous excerpts eliminate the strongest confounding variable (speaker identity bias) while preserving authentic political discourse patterns.
- **Methodological Superiority:** Forces evaluation based on textual content analysis rather than partisan associations, enabling clean assessment of framework validity.
- **Ecological Validity:** Maintains authentic linguistic and rhetorical patterns of political communication while controlling for measurement contamination.

**Corpus Composition (15-20 Texts):**

**Dignity Pole Exemplars (4-5 texts):**

- Excerpts emphasizing unity, individual worth, and respectful disagreement
- Sources: Regional governors' bipartisan initiatives, lesser-known historical unity speeches
- Anonymous excerpts from post-disaster speeches emphasizing community resilience

**Tribalism Pole Exemplars (4-5 texts):**

- Clear us-vs-them rhetoric without policy substance
- Sources: Local political rallies, regional campaign events
- Anonymous excerpts demonstrating pure tribal messaging patterns

**Balanced/Moderate Cases (4-5 texts):**

- Policy-focused content with mixed dignity/tribal elements
- Sources: State legislative debates, regional political forums
- Excerpts showing substantive disagreement without personal attacks

**Edge Cases and Controls (2-3 texts):**

- Pure policy statements (low framework fit controls)
- Ceremonial speeches (neutral content)
- Historical documents testing temporal framework applicability

**Text Preparation Protocol:**

- **Strategic Excerpting:** 400-600 word segments capturing moral positioning without identifying context
- **Metadata Removal:** Strip identifying references (dates, places, specific events)
- **Context Neutralization:** Remove positional identifiers while preserving rhetorical structure
- **Recognition Testing:** Pre-test with political science students to ensure non-recognition

**Academic Justification:**
> "To isolate textual moral content from speaker identity effects, we utilize anonymized excerpts from political discourse by regionally prominent but nationally unknown speakers. This approach preserves the authentic linguistic and rhetorical patterns of political communication while eliminating the strongest potential confounding variable—partisan bias triggered by speaker recognition."

### **Prompting Strategy: Conceptually Equivalent Adaptive Prompts**

**Strategic Rationale:**

- **Methodological Best Practice:** Computational social science literature establishes that task equivalence (not linguistic identity) is the standard for human-LLM validation studies.
- **Evaluator Optimization:** Adapted prompts maximize reliability for each evaluator type by addressing cognitive processing differences.
- **Academic Defensibility:** Systematic adaptation process with empirical validation provides stronger evidence than naive identical prompting.

**LLM Prompt Template:**

```
Role: You are an expert political discourse analyst.
Task: Analyze the following text for Dignity vs. Tribalism positioning.
Scale: Rate on 1-7 scale where 1=Strong Tribalism, 7=Strong Dignity

Definitions:
- Dignity (6-7): Emphasizes individual worth, respectful disagreement, unity across differences
- Tribalism (1-2): Emphasizes us-vs-them divisions, group superiority, exclusionary language
- Mixed/Moderate (3-5): Contains elements of both approaches

Instructions: Provide numerical score and identify 2-3 supporting passages
Format: Score: X/7, Evidence: [specific passages]
```

**Human Annotation Instructions:**

```
You will read political texts and evaluate them on how much they emphasize 
personal dignity and respect versus tribal us-versus-them thinking.

Please rate each text on a scale of 1-7:
- 1-2: Strongly emphasizes tribal divisions, us-vs-them language
- 3-4: Moderately tribal with some dignity elements  
- 5-6: Moderately emphasizes dignity with some tribal elements
- 7: Strongly emphasizes personal dignity, respect, unity

For each rating, please highlight 1-2 key passages that support your decision.

Take your time to read carefully and consider the overall moral approach of the text.
```

**Equivalence Validation Protocol:**

- **Pilot Testing:** Both prompt versions tested on 5 control texts to ensure comparable score distributions
- **Statistical Validation:** Correlation analysis confirming equivalent results on validation texts
- **Documentation:** Systematic record of adaptation rationale and empirical validation

**Academic Justification:**
> "To optimize reliability and validity for each evaluator type while maintaining task equivalence, we adapted prompt formulations following established practices in computational social science validation. LLM prompts utilize structured templates optimized for computational processing, while human annotation instructions employ conversational language with contextual examples. Both versions maintain identical analytical frameworks, scoring scales, and evaluation criteria, with equivalence validated through pilot testing and statistical comparison of score distributions."

### **Statistical Analysis Plan and Success Criteria**

**Primary Hypotheses:**

- **H1 (Inter-Rater Reliability):** Human annotators will achieve ≥0.70 agreement on Dignity vs Tribalism scoring
- **H2 (Human-LLM Alignment):** Human and LLM scores will show ≥0.80 correlation for single dipole validation
- **H3 (Framework Fit Validation):** High-fit texts will show better human-LLM agreement than low-fit controls

**Statistical Validation:**

- **Inter-Rater Reliability:** Intraclass correlation coefficient (ICC) for human-human agreement
- **Human-LLM Correlation:** Pearson correlation with confidence intervals
- **Score Distribution Analysis:** Range utilization and boundary case performance
- **Evidence Quality Assessment:** Thematic analysis of supporting passages

**Success Criteria:**

- **Minimum Acceptable:** ICC ≥ 0.70, Human-LLM r ≥ 0.70
- **Target Performance:** ICC ≥ 0.80, Human-LLM r ≥ 0.80
- **Excellence Threshold:** ICC ≥ 0.85, Human-LLM r ≥ 0.85


### **Resource Allocation and Timeline**

**Phase 1: Materials Development (Week 1)**

- Finalize 15-20 text corpus with anonymization
- Complete simplified codebook and training materials
- Develop gold standard cases and attention checks

**Phase 2: Platform Setup and Pilot (Week 2)**

- CloudResearch/MTurk account configuration
- Pilot study with 5 texts × 5 annotators
- Prompt refinement based on pilot feedback

**Phase 3: Main Study Execution (Week 3)**

- Launch full study: 20 texts × 4 annotators = 80 HITs
- Real-time quality monitoring and anomaly detection
- Cost management within \$400 budget allocation

**Phase 4: Analysis and Documentation (Week 4)**

- Statistical analysis and validation testing
- Academic documentation and replication package
- Results interpretation and next-phase planning

**Budget Allocation:**

- **Annotation Payments:** \$150 (80 HITs × \$1.50 + platform fees)
- **Platform Fees:** \$50 (CloudResearch/MTurk charges)
- **Contingency Reserve:** \$200 (additional validation if needed)


### **Academic Documentation and Replication**

**Methodological Transparency:**

- Complete documentation of text selection and anonymization process
- Systematic record of prompt adaptation rationale and validation
- Full statistical analysis plan with pre-registered hypotheses

**Replication Package:**

- Anonymized text corpus with metadata
- Both LLM and human prompt versions
- Complete annotation codebook and training materials
- Statistical analysis scripts and validation procedures

**Publication Strategy:**
> "This validation establishes a methodological template for computational-human alignment testing in political discourse analysis, demonstrating how systematic validation can build confidence in computational approaches through strategic focus on theoretically central constructs. Having established alignment for the most psychologically powerful moral-political distinction, future research can systematically extend validation to additional dimensions, building a comprehensive empirical foundation for multi-dimensional computational analysis."

---

## Summary: Strategic Excellence Through Methodological Focus

This revised human validation plan transforms resource constraints into strategic advantages through:

- **Theoretical Focus:** Single dipole approach concentrates validation resources on the most theoretically powerful construct
- **Bias Control:** Anonymous text strategy eliminates confounding variables while maintaining ecological validity
- **Methodological Sophistication:** Adapted prompting approach reflects computational social science best practices
- **Academic Credibility:** Systematic documentation and pre-registration demonstrate methodological rigor
- **Foundation Building:** Success provides clear pathway for extending validation to additional dimensions

The plan positions your research as methodologically sophisticated rather than resource-constrained, providing a strong foundation for academic publication and future research expansion.

<div style="text-align: center">⁂</div>

[^1]: Phase-Entry-Criteria_-Human-Validation-Studies.md

[^2]: narrative_gravity_maps_v1.3.0.md

[^3]: CHANGELOG.md

[^4]: CloudResearch-MTurk-Validation-Study_-Complete-G.md

[^5]: EXPERIMENTAL_DESIGN_FRAMEWORK.md

[^6]: DAILY_TODO_2025_06_13.md

[^7]: PAPER_CHANGELOG.md

[^8]: Human_Thematic_Perception_and_Computational_Replication_A_Literature_Review.md

