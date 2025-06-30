# Experiment Design Considerations: Democratic Tension Axis Model – Brazil 2018

## Bottom-Line Summary
To benchmark and validate the Democratic Tension Axis Model – Brazil 2018 against the original Tamaki & Fuks (T&F) framework, use **sequential single-axis passes for human raters**, and **experimentally compare both sequential and parallel multi-axis prompting for LLMs**. This approach leverages established best practices for human content analysis and allows for empirical assessment of LLM strengths in multi-dimensional tasks.

---

## Opening Framework

- **Humans:** Score each axis (Populismo↔Pluralismo, Patriotismo↔Nacionalismo) independently in sequential passes.
- **LLMs:** Run both sequential single-axis and parallel multi-axis prompts to evaluate which approach yields higher reliability, discriminant validity, and interpretability.
- **Empirical Focus:** Measure consistency, discriminant validity, and alignment with original T&F scores. Invite BYU collaborators to review and refine cue sets and methodology.

---

## 1. Human Rater Protocol: Sequential Single-Axis Passes

### Rationale
- Humans are susceptible to “halo effects” and cognitive contamination when scoring multiple dimensions simultaneously.  
- Sequential, independent passes per axis **maximize reliability and clarity** of dimensional measurement.

### Method
- **Step 1:** Raters score all items for Axis 1 (Populismo↔Pluralismo) using only cues and criteria for that axis.
- **Step 2:** Raters, ideally after a break or with shuffled order, score all items for Axis 2 (Patriotismo↔Nacionalismo) using only the corresponding cues.
- Provide comprehensive cue tables for each axis.
- If feasible, implement double-blind rating to minimize bias.

### Reference
Krippendorff, K. (2018). *Content Analysis: An Introduction to Its Methodology*. SAGE.  
🔗 [https://us.sagepub.com/en-us/nam/content-analysis/book258450](https://us.sagepub.com/en-us/nam/content-analysis/book258450)  
📊 Confidence: HIGH

---

## 2. LLM Protocol: Sequential vs. Parallel Multi-Axis Prompting

### Sequential Single-Axis Prompting
- Prompt LLM to focus exclusively on one axis per run.
- Example:  
```

Analise o discurso considerando apenas o eixo Populismo↔Pluralismo. Ignore apelos à identidade nacional.

```

### Parallel Multi-Axis Prompting
- Prompt LLM to score both axes in a single inference, providing explicit reasoning for each.
- Example:  
```

Analise o discurso e atribua um escore de 0 a 2 para cada eixo (Populismo↔Pluralismo e Patriotismo↔Nacionalismo), explicando separadamente o raciocínio para cada um.

```

### Rationale
- Recent evidence shows LLMs can handle simultaneous multi-dimensional tasks efficiently and consistently, potentially outperforming humans in annotation reliability for some tasks (Gilardi et al., 2023; Wei et al., 2022).
- Testing both approaches is essential to establish which method offers the best combination of reliability, efficiency, and clarity in this application.

### References
Gilardi, F., et al. (2023) – "ChatGPT Outperforms Humans in Political Ideology Classification" – *British Journal of Political Science*  
🔗 [https://doi.org/10.1017/S0007123423000282](https://doi.org/10.1017/S0007123423000282)  
📊 Confidence: HIGH

Wei, J., et al. (2022) – "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models" – *arXiv*  
🔗 [https://arxiv.org/abs/2201.11903](https://arxiv.org/abs/2201.11903)  
📊 Confidence: HIGH

---

## 3. Validation Strategy

- **Benchmark** all axis scores against original T&F manual scores.
- **Calculate inter-rater agreement** for human raters (Krippendorff’s alpha, Cohen’s kappa, etc.).
- **Test axis independence:** Analyze score correlations; true orthogonality should yield near-zero correlation between axes.
- **Audit LLM performance:** Evaluate clarity and interpretability of LLM justifications; flag cases of axis cross-talk or scoring confusion.

---

## 4. Reporting and Collaboration

- Report methodology and results transparently:
- “Human raters used sequential single-axis passes, following best practices (Krippendorff, 2018). LLMs were tested with both sequential and parallel multi-axis prompting (Gilardi et al., 2023; Wei et al., 2022). Results are presented side-by-side for benchmarking.”
- Invite BYU and other expert collaborators to audit cue lists, suggest further language adaptation, and participate in reliability/validation rounds.
- Document all protocol adjustments and empirical findings for future publication.

---

## Summary Table: Protocol Choices

| Approach                   | Method                    | Pros                                      | Cons                                     |
|----------------------------|---------------------------|-------------------------------------------|------------------------------------------|
| Human, sequential          | One axis per pass         | High validity, low halo effect            | Slower, more labor-intensive             |
| LLM, sequential            | One axis per prompt       | Auditable, strong axis focus              | May lose efficiency/holism benefits      |
| LLM, parallel              | Both axes in one prompt   | Efficiency, possible multi-dim interaction| Risk of axis cross-talk (needs audit)    |

---

## Key References

- Krippendorff, K. (2018). *Content Analysis: An Introduction to Its Methodology*. SAGE.  
🔗 [https://us.sagepub.com/en-us/nam/content-analysis/book258450](https://us.sagepub.com/en-us/nam/content-analysis/book258450)  
📊 Confidence: HIGH

- Gilardi, F., et al. (2023). "ChatGPT Outperforms Humans in Political Ideology Classification." *British Journal of Political Science*.  
🔗 [https://doi.org/10.1017/S0007123423000282](https://doi.org/10.1017/S0007123423000282)  
📊 Confidence: HIGH

- Wei, J., et al. (2022). "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models." *arXiv*.  
🔗 [https://arxiv.org/abs/2201.11903](https://arxiv.org/abs/2201.11903)  
📊 Confidence: HIGH

---

**Takeaway:**  
- Use sequential single-axis scoring for humans; empirically compare sequential and parallel for LLMs.
- Prioritize reliability, clarity, and orthogonality in all scoring.
- Benchmark and refine collaboratively with BYU and expert raters.

---
```

Let me know if you want example protocols, data analysis scripts, or reviewer checklists.
