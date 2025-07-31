---
title: Discernus System Architecture - Technical Specification
---

# Discernus System Architecture (v4.0 - THIN Orchestration)

> **Document Structure**: This document is organized into three distinct sections: (1) **Universal Principles** - immutable architectural foundations, (2) **Current Implementation** - v4.0 architecture as implemented, and (3) **Evolution Roadmap** - planned enhancements and future vision. Each section serves different stakeholders and development phases.

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

# Part I: Universal Principles (Immutable)

These foundational principles are the "constitutional" bedrock of Discernus - they remain constant regardless of implementation maturity or technology evolution:

**1. Day-1 Extensibility Through Specifications**
- Researchers can create unlimited frameworks, experiments, and corpora within specifications
- Any analytical approach expressible in natural language can be implemented
- Diverse methodological approaches and research designs supported
- External prompts allow analytical customization without code changes
- Git-based sharing enables immediate academic collaboration and framework distribution

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
- LLMs must execute code for all mathematical calculations
- Statistical results verified through secure code execution
- No hallucinated statistics - all numbers computed and logged
- Provenance systems detect content tampering and ensure analysis integrity
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
- Use statistical methods to measure variance and determine optimal sample sizes
- Adaptive sampling stops when confidence intervals meet requirements
- Balance statistical confidence with budget through empirical stopping rules
- Always report uncertainty, confidence intervals, and methodological constraints
- Employ multi-run statistical validation for reliability assessment

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

**10. Empirical Model Selection Based on Performance Requirements**
- Context window requirements determined by analysis complexity
- Rate limiting needs based on institutional processing scale
- Accuracy demands: Consistent performance across full context window
- Empirical validation: Models chosen through actual complexity testing
- Cost-performance optimization through systematic evaluation
- Provider reliability considerations for predictable academic pricing

**11. Security and Privacy by Design**
- Corpus anonymization and hash-based identity protection as standard practice
- Process isolation and sandboxing for secure agent execution (implemented upfront)
- Comprehensive audit logging for academic integrity and compliance (implemented upfront)
- API key management and rate limiting to prevent abuse
- Git-based provenance provides tamper-evident audit trails
- **Academic Data Sensitivity**: Text corpora often contain sensitive political, corporate, or personal content requiring proper security controls from day one

**11a. Orchestrator Trust Boundary Model**
- **Trust Layering**: Security architecture distinguishes between trusted infrastructure (orchestrators) and untrusted workloads (agents)
- **Orchestrator Privileges**: Can resolve canonical framework references (`../../frameworks/`) as trusted infrastructure operations
- **Agent Restrictions**: All agent file access constrained to experiment directory via `ExperimentSecurityBoundary`
- **Pre-Injection Security**: Orchestrators pre-resolve external dependencies before agent execution, eliminating agent access to system files
- **Canonical Framework Support**: Enables single-source-of-truth frameworks while maintaining strict agent isolation
- **Audit Compliance**: All framework access (canonical and local) logged with security context for complete provenance

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
- Model selection validated through complexity testing
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

# Part II: Current Implementation (v4.0 Architecture)

This section describes the actual implemented architecture as of 2025-01-30. All features and capabilities described here are operational and tested.

## Current Technology Stack

**Infrastructure**:
- MinIO content-addressable storage for artifact management
- Git-based provenance and version control (no databases)
- Local filesystem or S3-compatible storage backends
- Direct function calls over distributed coordination

**LLM Integration**:
- Primary: Vertex AI Gemini 2.5 Flash ($0.13/$0.38 per 1M tokens)
- Premium: Claude models for synthesis and critique
- Multi-provider gateway via LiteLLM
- Cost-optimized model selection based on empirical testing

**Current Specifications**:
- Framework Specification v6.0 (natural language analytical approaches)
- Experiment Specification v3.0 (multi-model research designs)
- Corpus Specification v3.0 (text collection management)

## Current Processing Pipeline

**Streamlined 3-Stage Architecture**:
1. **Analysis Stage**: Enhanced analysis agents with framework-specific prompts
2. **Synthesis Stage**: Batch processing with mathematical verification
3. **Reporting Stage**: Statistical analysis and academic-quality output

**Perfect Caching**: SHA256-based content-addressable storage eliminates redundant computation on identical inputs

**Security Model**: 
- Orchestrator trust boundary with agent restrictions
- ExperimentSecurityBoundary constrains agent file access
- Audit logging for all operations

---

# Part III: Evolution Roadmap (Future Vision)

This section outlines planned enhancements organized by development timeline. Features here are aspirational and may require architectural changes.

## Near-Term: Foundational Reliability (Next 6 Months)

**Enhanced Prompt Management**:
- Complete externalization of all agent prompts to YAML files
- Version-controlled prompt templates and systematic testing
- Framework-agnostic prompt libraries

**Systematic Evaluation Framework**:
- Automated testing pipeline using promptfoo or similar
- Golden dataset for regression testing
- LLM-as-judge validation for semantic quality
- Continuous integration for prompt changes

**Graceful Error Recovery**:
- Comprehensive fail-fast validation
- Partial artifact preservation on interruption
- Clear error messages with remediation steps
- Retry logic for transient failures

## Medium-Term: Performance Optimization (6-18 Months)

**Intelligent Model Routing**:
- Task complexity classification for optimal model selection
- Cost-performance optimization based on request characteristics
- Fallback chains for reliability

**Enhanced Multi-Agent Patterns**:
- Structured debate between specialized analysis agents
- Red team / blue team validation workflows
- Consensus mechanisms for complex reasoning tasks

**Advanced Caching Strategies**:
- Semantic similarity caching using vector embeddings
- Prompt optimization through retrieval-augmented generation
- Dynamic few-shot example selection

*Note: These features may require revision of the "No Database Policy" to support vector storage.*

## Long-Term: Autonomous Systems (18+ Months)

**Self-Healing Architecture**:
- Dynamic quality monitoring and correction
- Automated prompt optimization based on performance metrics
- Real-time adaptation to model capability changes

**Cost-Performance Frontier**:
- RAG-based dynamic prompt construction
- Context window optimization
- Predictive model selection based on task analysis

**Advanced Academic Features**:
- Automated literature integration
- Citation networks and research lineage tracking
- Collaborative framework development tools

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

*Last updated 2025‑01‑31 - Restructured with clear delineation between Universal Principles, Current Implementation, and Evolution Roadmap*