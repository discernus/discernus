---
title: Discernus System Architecture - Technical Specification
---

# Discernus System Architecture (THIN Orchestration)

> **Document Structure**: This document is organized into three distinct sections: (1) **Universal Principles** - immutable architectural foundations, (2) **Current Implementation** - operational architecture and capabilities, and (3) **Evolution Roadmap** - planned enhancements and future vision. Each section serves different stakeholders and development phases.

---

## About Discernus

**Discernus** is a computational research platform that amplifies researcher expertise through systematic, reproducible analysis of text corpora. Rather than replacing human judgment, Discernus enables researchers to apply their analytical frameworks at scale while maintaining transparency and academic integrity.

### What Discernus Does

Discernus transforms research capacity without compromising scholarly control:

**Traditional Approach**: 
- Researcher manually codes documents → Individual analysis → Manual synthesis → Subjective aggregation
- Limited scale, inconsistent application, difficult replication

**Discernus Approach**: 
- Researcher designs framework once → Automated consistent application across corpus → LLM-powered synthesis with computational verification → Transparent, statistically validated results
- Institutional scale, improved consistency, enhanced auditability

### Foundational Philosophy

**Human Amplification, Not Replacement**: Researchers retain complete control over analytical approach, interpretation, and synthesis. Discernus provides computational scale and methodological consistency while preserving human expertise and judgment.

**Day-1 Extensibility**: Create unlimited frameworks, experiments, and corpora within specifications. No programming required - analytical approaches expressed in natural language enable immediate research productivity.

**Academic Integrity by Design**: Calculations verified through code execution, decisions logged for audit, provenance maintained for peer review. Statistical results computed rather than hallucinated.

**LLM Consistency Approach**: LLMs can provide more consistent evaluation than human panels in many contexts, representing averaged human perception patterns while reducing fatigue and bias effects.

### Core Capabilities
- **Flexible Analytical Frameworks**: Approaches expressible in natural language (political analysis, discourse analysis, content analysis, literary criticism, etc.)
- **Scalable Text Processing**: Handles document collections from dozens to thousands with hash-based anonymization for sensitive materials
- **Computational Verification**: Statistics computed and verified through code execution
- **Process Transparency**: Audit trails, variance reporting, confidence intervals, methodological constraints
- **Git-based Collaboration**: Framework and experiment sharing enables academic community building

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

**3. Researcher-Centric Information Architecture**
- **Mirror Research Thinking**: System organization reflects how researchers naturally conceptualize and organize their work
- **Cognitive Load Management**: Present the right information at the right time in the right format for clarity
- **Human-Readable Interfaces**: Meaningful names, logical structures, and rich context over cryptic technical identifiers
- **Progressive Disclosure**: Surface relevant details when needed while maintaining clean primary workflows
- **Research Narrative Preservation**: File organization tells the story of the research process and decision-making
- **Balance Rigor with Usability**: Maintain underlying technical precision while providing researcher-friendly abstractions
- **Workflow Integration**: Support natural research patterns rather than forcing adaptation to system constraints

**4. No Black Box - Complete Process Transparency**
- **LLM Reasoning Visibility**: All agent reasoning traces and decision logic captured and accessible
- **Framework Interpretation Transparency**: How natural language analytical frameworks are operationalized and applied to specific texts
- **Computational Process Transparency**: Every mathematical calculation shows its work through executable code
- **Agent Orchestration Transparency**: Why specific agents were invoked, in what order, and with what parameters
- **Synthesis Methodology Transparency**: How conflicting analyses are identified, weighted, and resolved
- **Error Resolution Transparency**: What failed, why it failed, and how the system responded
- **Academic Requirement**: Researchers must be able to understand, validate, and replicate every step of the analytical process
- **Peer Review Enablement**: Complete methodological transparency sufficient for rigorous academic review

**5. Academic Provenance by Design**
- Every decision, artifact, and transformation logged with complete context
- Git-based version control for all research materials and process history
- Audit trails sufficient for peer review and replication
- Tamper-evident chains of analytical custody

**6. Computational Verification ("Show Your Math")**
- LLMs must execute code for all mathematical calculations
- Statistical results verified through secure code execution
- No hallucinated statistics - all numbers computed and logged
- Provenance systems detect content tampering and ensure analysis integrity
- Academic integrity through transparent, auditable computational processes

**7. LLM Consistency Superiority Over Human Evaluation Panels**
- **Fundamental Assumption**: Properly managed LLMs are more consistently perceptive than human evaluator panels
- LLMs represent global-scale averaging of human perception patterns across training data
- Individual humans may be more perceptive, but panels suffer from inconsistency, fatigue, and bias drift
- LLM evaluation provides speed and precision impossible with human panels at institutional scale
- Consistency enables reliable cross-document, cross-time, and cross-researcher comparisons
- Statistical validation (variance measurement, confidence intervals) quantifies this consistency advantage
- This assumption justifies computational methodology over traditional human coding approaches

**8. Variance-Aware Adaptive Processing with Transparency**
- Accept LLM response variance as natural and expected phenomenon (not a bug to fix)
- Use statistical methods to measure variance and determine optimal sample sizes
- Adaptive sampling stops when confidence intervals meet requirements
- Balance statistical confidence with budget through empirical stopping rules
- Always report uncertainty, confidence intervals, and methodological constraints
- Employ multi-run statistical validation for reliability assessment

**9. Reliability Over Flexibility**
- Single, predictable pipeline over infinite customization options
- Boring, bulletproof behavior over theoretical capability
- "It works every time" trumps "it can do anything"
- **Direct function calls over distributed coordination** - proven through prototype experience

**10. Resource-Conscious Cost Management**
- Empirical cost-performance optimization through model selection and batching
- Variance-driven adaptive sampling reduces unnecessary LLM calls
- Caching eliminates redundant computation on re-runs
- Transparent cost reporting enables institutional budget planning

**11. Specialized Agent Processing Over Monolithic Analysis**
- Task-specific agents outperform single-LLM approaches (empirically validated)
- Streamlined pipeline: BatchAnalysis → Synthesis → Report with comprehensive provenance
- Natural language communication between stages (no complex JSON parsing)
- Agent specialization: focused analysis agents with clear input/output contracts
- Comprehensive reporting with proper provenance asset management

**12. Empirical Model Selection Based on Performance Requirements**
- Context window requirements determined by analysis complexity
- Rate limiting needs based on institutional processing scale
- Accuracy demands: Consistent performance across full context window
- Empirical validation: Models chosen through actual complexity testing
- Cost-performance optimization through systematic evaluation
- Provider reliability considerations for predictable academic pricing

**13. Security and Privacy by Design**
- Corpus anonymization and hash-based identity protection as standard practice
- Process isolation and sandboxing for secure agent execution (implemented upfront)
- Comprehensive audit logging for academic integrity and compliance (implemented upfront)
- API key management and rate limiting to prevent abuse
- Git-based provenance provides tamper-evident audit trails
- **Academic Data Sensitivity**: Text corpora often contain sensitive political, corporate, or personal content requiring proper security controls from day one

**13a. Orchestrator Trust Boundary Model**
- **Trust Layering**: Security architecture distinguishes between trusted infrastructure (orchestrators) and untrusted workloads (agents)
- **Orchestrator Privileges**: Can resolve canonical framework references (`../../frameworks/`) as trusted infrastructure operations
- **Agent Restrictions**: All agent file access constrained to experiment directory via `ExperimentSecurityBoundary`
- **Pre-Injection Security**: Orchestrators pre-resolve external dependencies before agent execution, eliminating agent access to system files
- **Canonical Framework Support**: Enables single-source-of-truth frameworks while maintaining strict agent isolation
- **Audit Compliance**: All framework access (canonical and local) logged with security context for complete provenance

**14. Graceful Degradation and Error Recovery**
- Fail-fast validation prevents expensive downstream failures
- Partial artifact preservation on timeout or interruption
- Clear error messages with actionable remediation steps
- System continues processing remaining batches when individual items fail

**15. Intelligence in Prompts, Not Software**
- LLMs handle reasoning, interpretation, and domain knowledge
- Software provides coordination, storage, and deterministic operations only
- Components limited to <150 lines to prevent intelligence creep

**16. Externalized Intelligence, Internalized Coordination**
- Agent prompts live in external YAML files (intelligence belongs outside code)
- Agent discovery via file-based scanning (THIN principle: simple filesystem patterns over hardcoded logic)
- Researchers modify prompts, not coordination logic
- Balances THIN principles with Radical Simplification reliability

**17. Empirical Technology Choices**
- Decisions based on actual testing, not theoretical optimization
- Model selection validated through complexity testing
- Cost optimization secondary to reliability validation

**18. Linear Progression with Caching**
- Streamlined 3-stage pipeline with deterministic progression
- Cache hits eliminate redundant computation
- Predictable resource usage and timing

**19. Artifact-Oriented State Management**
- All data flows through immutable, hashed artifacts in content-addressable storage
- No mutable state in agents or orchestrator
- Reproducibility through artifact chains

**20. Fail-Fast Input Validation**
- Strict contracts enforced at system boundaries
- Clear error messages over expensive debugging cycles
- "Garbage in, clear error out"

**21. Decentralized Architecture Policy - Independence Over Infrastructure**
- **No Required Centralized Infrastructure**: Researchers work independently on their own machines without requiring shared servers or databases
- **Academic Transparency**: All research data stored as flat files (CSV/JSON) that are transparent to auditors and replication researchers
- **Distributed Collaboration**: Git-based collaboration without centralized infrastructure dependencies
- **Project Isolation**: Individual experiments remain self-contained and portable
- **Replication Ready**: Complete research packages as Git repositories with flat file data
- **Tool Agnostic**: CSV/JSON outputs work with any analysis tool (Excel, R, Python, etc.)
- **Optional Local Databases**: Embedded databases (SQLite, vector stores) permitted for performance optimization if they don't require centralized infrastructure
- **Hash Cross Referenced CSV**: When relational data is needed, use CSV files with shared artifact keys
- GitHub serves as the collaboration layer - no proprietary formats or database dumps

---

# Part II: Current Implementation 

This section describes the implemented architecture and operational capabilities.

## Current Technology Stack

**Infrastructure**:
- MinIO content-addressable storage for artifact management
- Git-based provenance and version control (no centralized databases required)
- Local filesystem or S3-compatible storage backends
- Direct function calls over distributed coordination
- Optional local embedded databases (SQLite) for performance optimization

**LLM Integration**:
- Inherently multi-model architecture with defaults to current Gemini series models during development
- Multi-provider gateway supporting various LLM providers
- Cost-performance optimization through empirical model selection
- Specialized model usage for different analytical tasks

**Specification System**:
- Framework specifications enable natural language analytical approaches
- Experiment specifications support multi-model research designs  
- Corpus specifications provide text collection management

## Current Processing Pipeline

**Streamlined 3-Stage Architecture**:
1. **Analysis Stage**: Enhanced analysis agents with framework-specific prompts
2. **Synthesis Stage**: Batch processing with mathematical verification
3. **Reporting Stage**: Statistical analysis and academic-quality output

**Content-Addressable Caching**: SHA256-based storage eliminates redundant computation on identical inputs

**Security Model**: 
- Orchestrator trust boundary with agent restrictions
- ExperimentSecurityBoundary constrains agent file access
- Comprehensive audit logging for all operations

**Transparency Approach**:
- LLM reasoning traces captured in artifacts where possible
- Framework interpretation steps logged for review
- Agent orchestration decisions recorded for audit
- Mathematical calculations executed and verified through code
- Continuous improvement toward complete process transparency

---

# Part III: Evolution Roadmap (Future Vision)

This section outlines planned enhancements organized by development timeline. Features here are aspirational and may require architectural changes.

## Near-Term: Foundational Reliability (Next 6 Months)

**Enhanced Prompt Management**:
- Complete externalization of all agent prompts to YAML files
- Version-controlled prompt templates and systematic testing
- Framework-agnostic prompt libraries

**Enhanced Transparency Infrastructure**:
- Structured reasoning trace capture and visualization
- Interactive transparency browsers for process exploration
- Framework interpretation workflow documentation
- Decision audit trails with searchable metadata

**Researcher-Centric Information Architecture**:
- Human-readable file naming and organization systems
- Rich metadata and context preservation
- Progressive disclosure interfaces for complex data
- Research narrative preservation in file structures

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
- Semantic similarity caching using local vector embeddings (embedded SQLite with vector extensions)
- Prompt optimization through retrieval-augmented generation
- Dynamic few-shot example selection
- Local vector stores for framework similarity matching

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

*Last updated 2025‑01‑31 - Cleaned up version numbers, specific claims, and marketing language while maintaining clear architectural guidance*