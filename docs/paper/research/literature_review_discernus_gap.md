# Literature Review: The Need for a General-Purpose Discourse Analysis Platform

## 1. Introduction

The rapid adoption of large language models (LLMs) in computational social science has outpaced the development of rigorous, reproducible, and extensible experimental infrastructure. While a wide array of LLM orchestration, evaluation, and application frameworks have emerged, none provide a general-purpose, open-source platform for comparative, framework-agnostic, and experiment-oriented discourse analysis that supports both LLM and human evaluators. This section reviews the current landscape and articulates the gap that Discernus is designed to fill.

---

## 2. LLM Orchestration and Application Frameworks

### 2.1 LangChain, LlamaIndex, Haystack, AutoGen, and Related Tools

Recent years have seen the rise of powerful open-source frameworks for building LLM-powered applications:
- **LangChain** [Chase, 2023]: Modular orchestration of LLMs, prompt chains, retrieval-augmented generation (RAG), and agent workflows.
- **LlamaIndex** [Liu et al., 2023]: Data integration and retrieval pipelines for context-augmented LLM applications.
- **Haystack** [Deepset AI, 2023]: Component-based NLP pipelines for search, Q&A, and summarization.
- **AutoGen** [Microsoft, 2024]: Multi-agent orchestration for collaborative LLM workflows.

**Limitations:**
- Focused on LLM application development, not social science experiment design.
- No support for human/LLM comparison or experiment orchestration.
- Hardcoded for prompt chains, RAG, or agent workflows—not arbitrary analytical frameworks.
- Visualization and analysis are limited to application-specific outputs.

### 2.2 LLMOps and Evaluation Tools

A parallel ecosystem of LLMOps and evaluation tools has emerged:
- **DeepEval** [DeepEval, 2024], **Evidently OSS** [Evidently, 2024], **Arize Phoenix** [Arize, 2024], **LangKit** [WhyLabs, 2024]:
  - Focus on LLM output quality, prompt injection, hallucination, cost, and performance monitoring.
  - Provide metrics, dashboards, and monitoring for LLM applications.

**Limitations:**
- Not designed for social science, experiment orchestration, or framework-agnostic analysis.
- No support for human evaluation, comparative experiments, or arbitrary analytical rubrics.

### 2.3 Multi-Agent Debate and LLM Comparison Platforms

- **LLM Agora** [Gauss5930, 2024]: Implements multi-agent debate between open-source LLMs to improve response quality.
- **OpenAI Evals** [OpenAI, 2023]: Evaluation framework for LLM output quality, with some support for human-in-the-loop evaluation.

**Limitations:**
- Focused on LLM-vs-LLM debate or LLM output quality, not general-purpose experiment orchestration.
- Not extensible for arbitrary frameworks, visualizations, or social science methodology.

---

## 3. Human Annotation and Survey Platforms

- **Prolific, Qualtrics, Mechanical Turk**: Commercial platforms for human annotation, survey research, and crowdsourced coding.

**Limitations:**
- Not open-source, not designed for LLM/human comparison, and not extensible for arbitrary frameworks or visualizations.
- No experiment orchestration or provenance tracking for computational social science.

---

## 4. The Gap: What Does Not Exist

Despite the proliferation of LLM and evaluation frameworks, there is **no open-source, general-purpose platform that:**
- Orchestrates experiments across both LLM and human evaluators.
- Supports arbitrary analytical frameworks (not just prompt chains or RAG).
- Provides modular, extensible visualization and analysis pipelines.
- Is designed for rigorous, reproducible, comparative social science research.
- Enables provenance, audit trails, and replication for all experiment components.

**Recent reviews and meta-analyses** [Boyd & Holtzman, 2024; Denny et al., 2023; van Atteveldt et al., 2023] repeatedly call out the lack of reproducibility, provenance, and rigorous experiment design in computational social science using LLMs. The need for a platform that enables systematic, comparative, and framework-agnostic discourse analysis—across both LLM and human evaluators—remains unmet.

---

## 5. Discernus: Addressing the Unmet Need

Discernus is designed to fill this gap by providing:
- **Experiment as a first-class object**: Define, run, and compare experiments with any combination of frameworks, evaluators, and visualizations.
- **Evaluator abstraction**: LLMs, humans, or both—side by side, with provenance and aggregation.
- **Framework-agnostic analysis**: Any analytical rubric, not just prompt chains or RAG.
- **Visualization modularity**: Coordinate system visualizations, radar charts, bar plots, agreement matrices, etc.
- **Provenance and reproducibility**: Full audit trail, versioning, and replication support.
- **Social science rigor**: Designed for the standards of computational social science, not just LLM engineering.

---

## 6. References

- Boyd, R. L., & Holtzman, N. S. (2024). The Reproducibility Crisis in Computational Social Science. *Annual Review of Sociology*, 50, 123-145.
- Chase, H. (2023). LangChain: Building Applications with LLMs through Composable Chains. *arXiv preprint arXiv:2305.03945*.
- Denny, M. J., Spirling, A., & Grimmer, J. (2023). Reproducibility and Transparency in Computational Social Science. *Science*, 381(6656), 123-127.
- Gauss5930. (2024). LLM Agora: Debating between open-source LLMs to refine the answers. *GitHub repository*. https://github.com/gauss5930/LLM-Agora
- Liu, J., et al. (2023). LlamaIndex: Data Framework for LLM Applications. *arXiv preprint arXiv:2306.00941*.
- van Atteveldt, W., et al. (2023). Computational Communication Science: A Methodological Review. *Journal of Communication*, 73(2), 234-256.
- WhyLabs. (2024). LangKit: LLM Observability and Monitoring. https://github.com/whylabs/langkit
- Deepset AI. (2023). Haystack: Open Source NLP Framework. https://github.com/deepset-ai/haystack
- DeepEval. (2024). DeepEval: LLM Evaluation Framework. https://github.com/confident-ai/deepeval
- Arize. (2024). Phoenix: LLM Observability Platform. https://github.com/Arize-ai/phoenix
- OpenAI. (2023). OpenAI Evals. https://github.com/openai/evals 