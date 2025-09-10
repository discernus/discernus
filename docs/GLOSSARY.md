# Discernus Glossary

*Updated August 2025 - Reflects current THIN synthesis pipeline with comprehensive RAG architecture*

## Core Architecture Concepts

### **THIN Architecture**
Software design philosophy where minimal code enables LLM intelligence rather than constraining it. Software provides orchestration, caching, and deterministic operations; LLMs handle reasoning, interpretation, and domain knowledge. Components limited to <150 lines to prevent intelligence creep.

### **Comprehensive RAG (Retrieval-Augmented Generation)**
Modern synthesis paradigm that indexes all experiment data types (corpus, framework, scores, statistics, evidence, metadata) in a unified knowledge graph, enabling cross-domain reasoning and intelligent evidence retrieval.

### **Cross-Domain Reasoning**
Ability to investigate connections between statistical patterns and textual evidence through natural language queries that span multiple data types (e.g., "What evidence supports the correlation between dignity and cohesion scores?").

### **Knowledge Graph**
Unified semantic index of all experiment data types using txtai embeddings, enabling fast (<2s) cross-domain queries with full provenance preservation.

### **Intelligent Retrieval**
LLM-powered adaptive query generation with targeted evidence retrieval based on statistical findings, eliminating context window limitations of massive evidence pools.

## Current Processing Pipeline

### **3-Stage THIN Synthesis Architecture**
Unified pipeline: Analysis → Synthesis → Finalization with comprehensive cross-domain provenance.

### **Analysis Stage**
Enhanced analysis agents with framework-specific prompts and dimensional scoring, producing raw scores and evidence with computational verification.

### **Synthesis Stage**
Statistical analysis and knowledge integration with LLM-powered synthesis, cross-domain reasoning, and evidence retrieval for comprehensive narrative construction.

### **Finalization Stage**
Academic-quality output generation with full cross-domain provenance, computational verification, peer review readiness, and complete artifact organization.

## Research Framework Components

### **Framework Specification**
Natural language analytical approach expressed in markdown with dimensional definitions, evaluation criteria, and academic grounding. Enables any analytical approach expressible in natural language.

### **Experiment Specification**
Research design document defining hypotheses, corpus requirements, analytical methodology, and success criteria. Supports multi-model research designs and comparative evaluation.

### **Corpus Specification**
Text collection manifest with metadata, processing requirements, and quality standards. Handles document collections from dozens to thousands with hash-based anonymization.

### **Dimensional Scores**
Individual analytical judgments (e.g., dignity_score = 0.8) that require textual evidence grounding. Foundation for all statistical analysis and evidence linking.

## Data Types and Artifacts

### **Six Data Type Integration**
Comprehensive knowledge architecture indexes: (1) Corpus Documents - full text with speaker attribution, (2) Framework Specification - analytical methodology, (3) Raw Scores - dimension scores with provenance, (4) Statistical Results - verified mathematical findings, (5) Evidence Quotes - supporting textual evidence, (6) Experiment Metadata - research context and hypotheses.

### **Content-Addressable Storage**
SHA256-based artifact management through LocalArtifactStorage, eliminating redundant computation on identical inputs with immutable, hashed artifacts.

### **Provenance Chain**
Complete audit trail from statistical findings back to source texts through deterministic semantic search and metadata preservation, ensuring peer review readiness.

### **Evidence Linking Scope**
Evidence linking required only for dimensional scores and direct mathematical derivatives. Complex statistical relationships require mathematical transparency rather than evidence linking.

## Technical Infrastructure

### **txtai Knowledge Index**
Comprehensive research knowledge index serving all experiment data types with deterministic, reproducible retrieval across heterogeneous research data types and full provenance preservation.

### **MathToolkit**
Pre-built mathematical functions with provenance metadata for reliable statistical calculations. All operations executed through secure code execution with complete transparency.

### **LocalArtifactStorage**
Content-addressable storage system for artifact management with Git-based provenance and version control, no centralized databases required.

### **LLM Gateway**
Multi-model architecture with Gemini 2.5 series as development defaults, supporting cross-model compatibility validation for ensemble testing and targeted use cases.

### **Security Boundary**
Orchestrator trust boundary model distinguishing between trusted infrastructure (orchestrators) and untrusted workloads (agents) with ExperimentSecurityBoundary constraining agent file access.

## Agent Architecture

### **Enhanced Analysis Agents**
Framework-specific agents that apply analytical approaches at scale with dimensional scoring, evidence extraction, and computational verification.

### **RAGIndexManager**
Component that creates unified knowledge graphs indexing all experiment data types for cross-domain reasoning and intelligent synthesis.

### **RAGEnhancedResultsInterpreter**
Intelligent synthesis agent using comprehensive knowledge retrieval for evidence-grounded narrative construction with full provenance.

### **Agent Specialization**
Task-specific agents with clear input/output contracts, natural language communication between stages, and cross-domain knowledge integration.

### **Current Package Structure**
- `discernus/core/`: Core production services (MathToolkit, LocalArtifactStorage)
- `discernus/gateway/`: LLM API management and model registry
- `discernus/agents/`: Specialized analysis and synthesis agents
- `discernus/agents/thin_synthesis/`: 3-stage THIN synthesis pipeline
- `discernus/agents/comprehensive_knowledge_curator/`: RAG knowledge indexing
- `discernus/tests/`: Comprehensive test suite with integration testing
- `docs/architecture/`: System architecture and provenance documentation

### **Research Artifacts**
- `projects/`: Individual experiments with project/experiment/run structure
- `frameworks/`: Framework specifications (reference, seed, community)
- `corpus/`: Text collections and corpus manifests
- `pm/`: Product management and specification documents

## Quality and Validation

### **Computational Verification**
All mathematical calculations executed through secure code with complete transparency. No hallucinated statistics - all numbers computed and logged with provenance.

### **Academic Provenance**
Every decision, artifact, and transformation logged with complete context. Git-based version control and tamper-evident chains of analytical custody.

### **Evidence-Grounded Synthesis**
Zero hallucination synthesis through deterministic evidence retrieval and computational verification, maintaining causal chains between statistical findings and textual evidence.

### **Variance-Aware Processing**
Statistical methods to measure LLM response variance, adaptive sampling with confidence intervals, and multi-run validation for reliability assessment.

### **Cross-Model Validation**
Multi-model architecture supporting ensemble testing and targeted use cases while maintaining Gemini 2.5 series as development defaults.

## Modern AI Systems Patterns

### **RAG-First Design**
Retrieval-Augmented Generation as primary synthesis paradigm, moving beyond simple evidence-only approaches to comprehensive knowledge retrieval.

### **LLM Query Intelligence**
Language models generate and refine queries adaptively based on statistical context and research hypotheses, enabling sophisticated cross-domain investigation.

### **Semantic Search Integration**
Vector embeddings and semantic search as core infrastructure for research artifact discovery, with hash-based persistent caching.

### **Adaptive Query Refinement**
LLM-powered query optimization improving retrieval quality iteratively based on result relevance and completeness.

## Development and Extension

### **THIN Compliance**
Adherence to THIN architecture principles: minimal code, maximum LLM intelligence, externalized prompts in YAML files, no complex parsing.

### **Framework Agnostic**
System adapts to any analytical approach expressible in natural language through specification-driven design and externalized intelligence.

### **Empirical Technology Choices**
Decisions based on actual testing rather than theoretical optimization, with model selection validated through complexity testing.

### **Day-1 Extensibility**
Create unlimited frameworks, experiments, and corpora within specifications without programming, enabling immediate research productivity.

---

*This glossary maintains consistent terminology across the Discernus project and reflects the current THIN synthesis architecture with comprehensive RAG capabilities.*

## Related Documentation

- **`CURSOR_AGENT_QUICK_START.md`** - 30-second orientation for new Cursor agents
- **`architecture/DISCERNUS_SYSTEM_ARCHITECTURE.md`** - Complete technical architecture specification
- **`architecture/PROVENANCE_SYSTEM.md`** - Academic provenance and audit trail documentation
- **`developer/CLI_COMMAND_REFERENCE.md`** - Complete CLI usage guide
- **`specifications/`** - Framework, Experiment, and Corpus specification documentation 