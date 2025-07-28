---
title: Discernus System Architecture - Technical Specification
---

# Discernus System Architecture (v4.0 - THIN Orchestration)

> **Architectural Vision**: This document outlines the durable architectural vision and the non-negotiable principles for the Discernus platform. It is the "constitution" that guides our technical decisions. For the specifics of the current reference implementation, including code examples and technology choices, please see the `THIN_V2_IMPLEMENTATION_PLAN.md`.

---

## About Discernus

**Discernus** is a computational research platform that amplifies researcher expertise through systematic, reproducible analysis of text corpora. Rather than replacing human judgment, Discernus enables researchers to apply their analytical frameworks at unprecedented scale while maintaining complete transparency and academic integrity.

### What Discernus Does

Discernus transforms research capacity without compromising scholarly control:

**Traditional Approach**: 
- Researcher manually codes documents → Individual analysis → Manual synthesis → Subjective aggregation
- Limited scale, inconsistent application, difficult replication

**Discernus Approach**: 
- Researcher designs framework once → Automated consistent application across corpus → LLM-powered synthesis with computational verification → Transparent, statistically validated results
- Institutional scale, perfect consistency, complete auditability

### Foundational Philosophy

**Human Amplification, Not Replacement**: Researchers retain complete control over analytical approach, interpretation, and synthesis. Discernus provides computational scale and methodological consistency while preserving human expertise and judgment.

**Day-1 Extensibility**: Create unlimited frameworks, experiments, and corpora within specifications. No programming required - analytical approaches expressed in natural language enable immediate research productivity.

**Academic Integrity by Design**: Every calculation verified through code execution, every decision logged for audit, complete provenance for peer review. No hallucinated statistics, no black-box results.

**Empirically Validated Consistency**: LLMs provide more consistent evaluation than human panels at institutional scale, representing global-scale averaging of human perception patterns while eliminating fatigue and bias drift.

### Core Capabilities
- **Unlimited Analytical Frameworks**: Any approach expressible in natural language (political analysis, discourse analysis, content analysis, literary criticism, etc.)
- **Any Text Corpus**: Scales from dozens to thousands of documents with hash-based anonymization for sensitive materials
- **Computational Verification**: All statistics computed and verified - no hallucinated results
- **Complete Transparency**: End-to-end audit trails, variance reporting, confidence intervals, methodological constraints
- **Immediate Collaboration**: Git-based framework and experiment sharing enables academic community building

---

## Fundamental Architectural Principles

These principles guide every design decision in Discernus:

**1. Day-1 Extensibility Through Specifications**
- **Already Extensible**: Researchers can create unlimited frameworks, experiments, and corpora within specifications
- Framework Specification v4.0 enables any analytical approach expressible in natural language
- Experiment Specification v2.0 supports diverse methodological approaches and research designs
- Corpus Specification v2.0 accommodates any text collection with proper preparation
- External YAML prompts allow analytical customization without code changes
- Git-based sharing enables immediate academic collaboration and framework distribution
- *Future: Advanced platform features (core+modules architecture, marketplace, GUI tools) deferred to post-MVP*

**2. Human Intellectual Value Amplification, Not Replacement**
- Real value creation comes from researcher expertise: framework design, corpus curation, experiment methodology
- Discernus amplifies human intuition and domain knowledge rather than substituting for it
- Researchers retain full control over analytical approach, interpretation, and synthesis
- System provides computational scale and consistency while preserving human judgment
- End-to-end transparency enables researchers to audit, validate, and refine their analytical choices
- Post-hoc analysis, synthesis, and scholarly interpretation remain fundamentally human activities
- Technology serves scholarship, not the reverse - researchers drive insights, system provides rigor

**3. Academic Provenance by Design**
- Every decision, artifact, and transformation logged
- Git-based version control for all research materials
- Audit trails sufficient for peer review and replication

**4. Computational Verification ("Show Your Math")**
- LLMs must execute Python code for all mathematical calculations
- Statistical results verified through `SecureCodeExecutor` with resource limits
- No hallucinated statistics - all numbers computed and logged
- Provenance stamps detect content tampering and ensure analysis integrity
- Academic integrity through transparent, auditable computational processes

**5. LLM Consistency Superiority Over Human Evaluation Panels**
- **Fundamental Assumption**: Properly managed LLMs are more consistently perceptive than human evaluator panels
- LLMs represent global-scale averaging of human perception patterns across training data
- Individual humans may be more perceptive, but panels suffer from inconsistency, fatigue, and bias drift
- LLM evaluation provides speed and precision impossible with human panels at institutional scale
- Consistency enables reliable cross-document, cross-time, and cross-researcher comparisons
- Statistical validation (variance measurement, confidence intervals) quantifies this consistency advantage
- This assumption justifies computational methodology over traditional human coding approaches

**6. Variance-Aware Adaptive Processing with Transparency**
- Accept LLM response variance as natural and expected phenomenon (not a bug to fix)
- **Synthetic Calibration**: Generate representative text from corpus using Gemini 2.5 Flash for variance measurement
- **Coefficient of Variation**: Measure CV = σ/μ from pilot runs to determine optimal sample sizes
- **Sequential Probability Ratio Testing (SPRT)**: Adaptive sampling stops when confidence intervals meet requirements
- **Minimum Sample Size Calculation**: n = (z × CV / E)² where z=1.96 (95% confidence), E=desired margin
- **Cost-Constrained Optimization**: Balance statistical confidence with budget through empirical stopping rules
- **Transparency Requirement**: Always report uncertainty, confidence intervals, CV, and methodological constraints
- **Multi-Run Statistical Validation**: Cronbach's alpha, ANOVA, inter-run reliability, and convergence analysis

**7. Reliability Over Flexibility**
- Single, predictable pipeline over infinite customization options
- Boring, bulletproof behavior over theoretical capability
- "It works every time" trumps "it can do anything"
- **Direct function calls over distributed coordination** - proven through prototype experience

**8. Resource-Conscious Cost Management**
- Empirical cost-performance optimization through model selection and batching
- Variance-driven adaptive sampling minimizes unnecessary LLM calls
- Perfect caching eliminates redundant computation on re-runs
- Transparent cost reporting enables institutional budget planning
- *Note: Advanced cost controls and budgeting tools deferred to post-MVP phase*

**9. Specialized Agent Processing Over Monolithic Analysis**
- Task-specific agents outperform single-LLM approaches (empirically validated)
- Streamlined pipeline: BatchAnalysis → Synthesis → Report with comprehensive provenance
- Natural language communication between stages (no complex JSON parsing)
- Agent specialization: focused analysis agents with clear input/output contracts
- Comprehensive reporting with proper provenance asset management

**10. Opinionated Model Selection Based on Performance Requirements**
- Context window requirements: 2M+ tokens for multi-framework batch analysis
- Rate limiting needs: 800+ RPM for institutional-scale processing
- Accuracy demands: Consistent performance across full context window
- Empirical validation: Models chosen through actual complexity testing (CHF failure)
- Cost-performance optimization: Gemini 2.5 Pro selected over alternatives
- Provider reliability: Vertex AI chosen for predictable academic pricing

**11. Security and Privacy by Design**
- Corpus anonymization and hash-based identity protection as standard practice
- Process isolation and sandboxing for secure agent execution (implemented upfront)
- Comprehensive audit logging for academic integrity and compliance (implemented upfront)
- API key management and rate limiting to prevent abuse
- Git-based provenance provides tamper-evident audit trails
- **Academic Data Sensitivity**: Text corpora often contain sensitive political, corporate, or personal content requiring proper security controls from day one

**12. Graceful Degradation and Error Recovery**
- Fail-fast validation prevents expensive downstream failures
- Partial artifact preservation on timeout or interruption
- Clear error messages with actionable remediation steps
- System continues processing remaining batches when individual items fail
- *Note: Advanced resilience patterns and retry logic deferred to post-MVP phase*

**13. Intelligence in Prompts, Not Software**
- LLMs handle reasoning, interpretation, and domain knowledge
- Software provides coordination, storage, and deterministic operations only
- Components limited to <150 lines to prevent intelligence creep

**14. Externalized Intelligence, Internalized Coordination**
- Agent prompts live in external YAML files (intelligence belongs outside code)
- Agent discovery via file-based scanning (THIN principle: simple filesystem patterns over hardcoded logic)
- Researchers modify prompts, not coordination logic
- Balances THIN principles with Radical Simplification reliability

**15. Empirical Technology Choices**
- Decisions based on actual testing, not theoretical optimization
- Gemini 2.5 Pro chosen over Flash due to CHF complexity test failure
- Cost optimization secondary to reliability validation

**16. Linear Progression with Perfect Caching**
- Streamlined 3-stage pipeline with deterministic progression
- Cache hits eliminate redundant computation entirely
- Predictable resource usage and timing

**17. Artifact-Oriented State Management**
- All data flows through immutable, hashed artifacts in MinIO
- No mutable state in agents or orchestrator
- Perfect reproducibility through artifact chains

**18. Fail-Fast Input Validation**
- Strict contracts enforced at system boundaries
- Clear error messages over expensive debugging cycles
- "Garbage in, clear error out"

**19. No Database Policy - Git as Persistence Layer**
- **Academic Transparency**: Databases are opaque to auditors and replication researchers
- **Distributed Collaboration**: Flat files enable researcher collaboration without centralized infrastructure
- **Project Isolation**: Individual experiments remain self-contained and portable
- **Replication Ready**: Complete research packages as Git repositories with flat file data
- **Tool Agnostic**: CSV/JSON files work with any analysis tool (Excel, R, Python, etc.)
- GitHub serves as the persistence and collaboration layer for all research materials
- When relational data is needed, use Hash Cross Referenced CSV files with shared artifact keys
- *Future: Discernus Enterprise may offer optional database integration for institutional deployments*

---

## 5 · Architectural Pillars for a Durable LLM System

> This section documents the core architectural principles and industry best practices that guide the development of the Discernus platform. These pillars represent a tiered roadmap, moving from a reliable foundation to a cutting-edge, state-of-the-art system. They are the "constitution" for our technical decisions—ideals we aspire to, even if we are still in the process of implementing them fully.

### Foundational Pillars (The Non-Negotiable Bedrock)

These are the absolute requirements for a reliable, production-ready system.

**Pillar 1: Prompt Management**
- **Principle**: Prompts are code and must be treated as such. They are version-controlled, templated, and strictly separated from application logic.
- **Implementation**: All agent intelligence is defined in external `.yaml` files, enabling versioning, testing, and modification without code changes.

**Pillar 2: Research-Grade Data Assets**
- **Principle**: Generate data artifacts that serve both computational processing and researcher analysis workflows through pure THIN architecture - LLM intelligence with software coordination only.
- **Implementation**: LLMs perform all framework calculations directly and show their mathematical work. Multi-document synthesis achieved through intelligent batch processing: (1) Enhanced analysis agents perform calculations and generate mathematical verification, (2) Batch synthesis agents extract calculated results into research CSV format, (3) Rollup synthesis consolidates multiple CSV batches if needed, (4) Final synthesis provides statistical analysis and interpretation. No parsing pipelines, no transformation logic - pure LLM intelligence with programmatic verification of mathematical accuracy. This approach maintains complete framework agnosticism while providing researcher-ready CSV assets.

**Pillar 3: Systematic Evaluation ("Evals")**
- **Principle**: You cannot improve what you cannot measure. Every critical prompt and model combination must be subject to a suite of automated tests to prevent quality regressions.
- **Implementation**: We use an evaluation pipeline (e.g., using `promptfoo`) to test our agents against a "golden set" of documents. These "Evals" assert not just the structural validity of the output (is it valid JSON?), but also the semantic quality of the reasoning, often using a more powerful LLM as an impartial "judge."

### State-of-the-Art Pillars (Production-Grade Performance & Reasoning)

These enhancements move the system from merely reliable to highly performant and efficient.

**Pillar 4: The Router (For Cost, Speed, and Capability)**
- **Principle**: No single LLM is best for every task. A sophisticated system routes tasks to the optimal model based on the task's complexity, cost, and speed requirements.
- **Implementation**: An LLM-based **Router** acts as a dispatcher. A small, fast model first classifies an incoming task (e.g., "simple data extraction" vs. "complex reasoning") and then routes it to the appropriate "expert" model (e.g., `Claude Haiku` for the simple task, `Gemini 2.5 Pro` for the complex one).

**Pillar 5: Structured Caching (For Speed and Cost Savings)**
- **Principle**: Identical inputs should yield identical outputs, and a computation should only be paid for once.
- **Implementation**: A **Semantic Cache** is used. Before making an LLM call, the system converts the prompt into a vector embedding and checks a vector database for a semantically similar, previously executed request. If a match is found, the cached result is returned instantly, saving both time and money. `LiteLLM` provides built-in support for this pattern.

**Pillar 6: Multi-Agent Collaboration (For Complex Reasoning)**
- **Principle**: Advanced reasoning emerges from a structured debate between multiple, specialized "expert" agents.
- **Implementation**: Complex analysis is broken down into a multi-agent workflow (e.g., using `LangGraph`). An `Analyst Agent` provides an initial analysis, a `Red Team Agent` critiques it, and a `Synthesis Agent` acts as a final arbiter to produce a more robust and balanced conclusion. The software's role is simply to orchestrate the flow of messages between these intelligent agents.

### Bleeding-Edge Pillars (Aspirational, Future-Facing Goals)

These patterns represent the next generation of LLM systems, focused on self-correction and extreme efficiency.

**Pillar 7: The "Self-Healing" System (Dynamic Fallbacks & Correctness)**
- **Principle**: A truly resilient system anticipates and dynamically corrects its own errors and quality degradations in real-time.
- **Implementation**: A **"Guardrails" Loop** is used. After an agent produces its output, a separate, fast, and cheap **Guardrails Agent** validates the output against a dynamic rubric. If the output fails validation, the system automatically re-runs the original agent with the corrective feedback from the Guardrails Agent, creating a self-healing loop. `Guardrails AI` is an open-source library for this pattern.

**Pillar 8: The Cost-Performance Frontier (RAG-based Prompt Optimization)**
- **Principle**: The cost and latency of an LLM call are dominated by prompt size. A cutting-edge system actively minimizes its prompt size before every call.
- **Implementation**: A **Retrieval-Augmented Generation (RAG)** pipeline is used to create dynamic "few-shot" prompts. Instead of sending the entire analytical framework, the system uses a vector database to retrieve only the most semantically relevant sections of the framework and a few "golden" examples of similar analyses. This creates a much smaller, more targeted, and often higher-quality prompt, dramatically reducing cost and latency. `LlamaIndex` and `LangChain` are standard tools for this.

---

### The THIN vs THICK Philosophy

**Discernus embodies THIN software architecture principles**:

**THIN Architecture** (Discernus):
- **LLM Intelligence**: Complex reasoning, format detection, framework application handled by language models
- **Software Infrastructure**: Minimal routing, caching, orchestration - no business logic
- **Principle**: "Make it easier to do the right thing and harder to do the wrong thing"
- **Result**: Framework/experiment/corpus agnostic system that adapts to researcher needs

**THICK Architecture** (Traditional Systems):
- **Software Intelligence**: Complex parsing, format-specific processors, hardcoded business rules
- **LLM Usage**: Limited to simple tasks, constrained by software assumptions
- **Problem**: Brittle, framework-specific, requires engineering for each new research approach
- **Result**: Researchers constrained by what software developers anticipated

---

*Last updated 2025‑07‑26 - Architectural Vision & Principles*