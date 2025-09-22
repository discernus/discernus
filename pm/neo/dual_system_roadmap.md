# Framework Analysis Platform: Dual-System Architecture Roadmap

## Executive Summary

This document outlines a two-system architecture for framework-based document analysis and research synthesis, designed to serve computational social scientists and discourse researchers. The architecture separates core analysis infrastructure from exploratory research capabilities, enabling independent development, deployment, and usage patterns.

## System Overview

### System 1: Document Analysis Management Application
**Core Infrastructure for Systematic Framework Analysis**

### System 2: Conversational Research Synthesis Application  
**Intelligent Research Assistant Built on System 1 Foundation**

---

## System 1: Document Analysis Management Application

### Reason for Existence

System 1 addresses the fundamental challenge of applying analytical frameworks to document corpora systematically and reliably. Current approaches to discourse analysis suffer from:

- **Inconsistent application** of analytical frameworks across documents
- **Poor replicability** due to subjective interpretation variations  
- **Limited scalability** for large document collections
- **Fragmented storage** of analysis results and evidence
- **Lack of standardization** across research projects

System 1 provides standardized infrastructure for framework-based analysis with computational rigor and export capabilities for downstream statistical analysis.

### Theory of Operation

**Framework-Centric Architecture**: The system treats analytical frameworks as first-class entities with explicit specifications, versions, and computational procedures. Frameworks define:
- Dimensional measurement procedures
- Derived metric calculations  
- Output schemas and validation rules
- Evidence collection requirements

**Separation of Analysis and Interpretation**: System 1 focuses purely on measurement - applying frameworks to generate empirical data about discourse patterns. Interpretation and statistical analysis occur in downstream tools or System 2.

**Audit Trail Completeness**: Every analysis generates complete computational trails including raw scores, derived metrics, evidence quotes, marked-up documents, and calculation code for independent verification.

### User Flows

#### Primary Flow: Document Analysis Execution
1. **Corpus Management**: Import documents with rich metadata (author, date, type, context)
2. **Framework Selection**: Choose analytical framework and version from available options
3. **Analysis Execution**: System applies framework to selected documents using LLM analysis agents
4. **Result Storage**: Dimensional scores, derived metrics, evidence, and markup stored in database
5. **Quality Verification**: Review confidence scores, evidence quality, calculation audits
6. **Export Generation**: Extract analysis results in formats suitable for statistical software

#### Secondary Flow: Framework Management
1. **Framework Import**: Load new analytical frameworks with complete specifications
2. **Version Control**: Manage framework versions and track changes
3. **Validation**: Test framework application on sample documents
4. **Documentation**: Maintain framework metadata and usage guidelines

### Technical Stack

**Database**: PostgreSQL with JSONB support
- Relational structure for core entities (documents, analyses, frameworks)
- JSONB storage for framework-specific derived metrics
- Materialized views for entity inventory and summary statistics
- Full-text search capabilities for evidence quotes

**Application Framework**: Python
- FastAPI for API endpoints and web interface
- SQLAlchemy for database operations and migrations  
- Pandas for data manipulation and export generation
- Direct LLM API integration (OpenAI/Anthropic) without abstraction layers

**Analysis Engine**: 
- Structured prompt templates for framework application
- Multi-perspective consistency checking (evidence-first, context-weighted, pattern-based)
- Automatic confidence calculation and quality assessment
- Derived metric computation with audit trail generation

### Key Architectural Design Principles

#### Single Workstation Architecture
- **Rationale**: Eliminates multi-user coordination complexity while maintaining full functionality
- **Benefits**: No resource contention, simpler deployment, full researcher control
- **Export Strategy**: Comprehensive data export enables collaboration through shared datasets

#### Framework Agnosticism  
- **Rationale**: Cannot anticipate all future analytical frameworks or research directions
- **Implementation**: Flexible schema accommodates varying framework requirements
- **Extension**: New frameworks integrate without system modification

#### Computational Transparency
- **Rationale**: Academic research requires reproducible, auditable methods
- **Implementation**: Complete calculation trails, version tracking, evidence preservation
- **Verification**: Independent replication possible through exported code and data

#### Export-First Design
- **Rationale**: Researchers need flexibility to use specialized statistical tools
- **Formats**: CSV, JSON, R, Stata, Python-native formats
- **Completeness**: Full analysis context preserved in exports

---

## System 2: Conversational Research Synthesis Application

### Reason for Existence

System 2 addresses the research discovery and synthesis challenge that emerges once substantial analysis data accumulates. Researchers face:

- **Analysis paralysis** when confronting large datasets with multiple comparison possibilities
- **Missed opportunities** for novel research directions using available data
- **Manual statistical execution** requiring significant technical expertise
- **Interpretation challenges** connecting statistical results to theoretical frameworks
- **Feasibility assessment** difficulties determining what research questions are answerable

System 2 provides intelligent research assistance that understands available data and guides researchers through systematic exploration and analysis.

### Theory of Operation

**Entity Inventory Context Loading**: Rather than comprehensive relationship graphs, the system loads lightweight entity inventories (available authors, frameworks, temporal coverage, document types) that provide LLMs with queryable context without computational overhead.

**Iterative Research Workflow**: The system supports natural research progression:
1. **Inventory**: "What do I have of this type?"
2. **Feasibility**: "Can I answer this question with available data?" 
3. **Refinement**: "What if I constrained the scope this way?"
4. **Execution**: "Run the analysis with proper statistical rigor"

**Statistical Method Selection**: The system selects appropriate statistical procedures based on data characteristics, research questions, and established methodological standards.

**Interpretive Synthesis**: Results are contextualized within theoretical frameworks and research literature to generate actionable insights.

### User Flows

#### Primary Flow: Conversational Research Exploration
1. **Context Loading**: System prepares entity inventory from System 1 database
2. **Research Question**: Researcher poses natural language research question
3. **Feasibility Assessment**: System evaluates data availability and statistical power
4. **Method Recommendation**: Suggests appropriate analytical approaches and potential constraints  
5. **Analysis Execution**: Performs statistical analysis with proper methodological rigor
6. **Report Generation**: Creates interpreted results with statistical evidence and theoretical context
7. **Follow-up Exploration**: Enables iterative refinement and additional questions

#### Secondary Flow: Statistical Analysis Management
1. **Analysis History**: Track completed statistical analyses and research questions
2. **Result Storage**: Persist statistical results, methods, and interpretations
3. **Comparison Studies**: Build on previous analyses for longitudinal research
4. **Export Integration**: Combine with System 1 exports for comprehensive datasets

### Technical Stack

**Foundation**: Built on System 1 database and Python infrastructure

**Statistical Analysis**: 
- SciPy/StatsModels for statistical procedures
- Pandas for data manipulation and aggregation
- Matplotlib/Seaborn for visualization recommendations
- Custom statistical reporting with effect sizes and interpretation

**Conversational Interface**:
- Direct LLM API integration with structured prompts
- Entity inventory context loading (50-100K tokens)
- Tool calling for database queries and statistical procedures
- Natural language result interpretation and report generation

**Analysis Storage**:
- Extended database schema for statistical analysis results
- Research question tracking and similarity detection
- Method documentation and replication procedures
- Report versioning and export capabilities

### Key Architectural Design Principles

#### Lightweight Context Loading
- **Rationale**: Comprehensive relationship graphs create maintenance overhead without proportional benefits
- **Implementation**: Materialized views provide entity summaries refreshed periodically
- **Scalability**: Entity inventory context scales to large corpora without performance degradation

#### Methodological Rigor
- **Rationale**: Academic research requires proper statistical procedures and effect size reporting
- **Implementation**: Automated assumption checking, multiple comparison corrections, confidence intervals
- **Transparency**: Complete methodological documentation and replication procedures

#### Iterative Refinement Support
- **Rationale**: Researchers naturally refine questions based on data availability and initial results
- **Implementation**: Conversational interface supports scope adjustment and alternative approaches
- **Memory**: Analysis history informs suggestions and prevents redundant work

#### Human-AI Collaboration
- **Rationale**: Researchers bring domain expertise and interpretive judgment that AI cannot replace
- **Implementation**: System provides computational power and methodological rigor while preserving researcher control over questions and interpretation
- **Boundaries**: Clear separation between statistical execution and theoretical interpretation

---

## Integration Architecture

### Data Flow Between Systems
1. **System 1** generates framework analysis results and maintains entity inventory
2. **System 2** accesses System 1 data read-only for statistical analysis
3. **System 2** stores statistical analysis results in separate schema
4. **Export capabilities** provide unified datasets combining both systems' outputs

### API Boundaries
- **System 1**: RESTful API for document management, framework application, analysis results
- **System 2**: Extends System 1 API with statistical analysis endpoints and conversational interface
- **Clear separation**: System 2 never modifies System 1 core data (documents, frameworks, analyses)

### Deployment Flexibility
- **Independent deployment**: System 1 can operate without System 2
- **Incremental adoption**: Researchers can start with System 1, add System 2 later
- **Resource isolation**: Statistical analysis compute separate from document analysis compute

---

## Development Roadmap

### Phase 1: System 1 Core (Months 1-6)
1. **Database schema** and migration system
2. **Framework specification** format and validation
3. **Document ingestion** with metadata support
4. **Analysis execution engine** with LLM integration
5. **Basic export capabilities** (CSV, JSON)
6. **Web interface** for analysis management

### Phase 2: System 1 Enhancement (Months 4-8) 
1. **Advanced export formats** (R, Stata, Python)
2. **Materialized views** for entity inventory
3. **Calculation auditing** and verification tools
4. **Framework version management**
5. **Analysis quality assessment** and confidence metrics
6. **Documentation system** and user guides

### Phase 3: System 2 Foundation (Months 6-10)
1. **Entity inventory** context loading system
2. **Conversational interface** with LLM integration
3. **Statistical analysis engine** with common procedures
4. **Basic report generation** with interpretation
5. **Analysis history** tracking and storage

### Phase 4: System 2 Enhancement (Months 8-12)
1. **Advanced statistical procedures** and effect size calculations
2. **Methodological validation** and assumption checking
3. **Research question similarity** detection and recommendations
4. **Comprehensive report generation** with visualizations
5. **Integration testing** and performance optimization

### Phase 5: Production Readiness (Months 10-14)
1. **Performance optimization** and scaling considerations
2. **Comprehensive testing** and validation procedures
3. **Documentation completion** and user training materials
4. **Deployment automation** and monitoring systems
5. **User feedback integration** and feature refinement

---

## Success Metrics

### System 1 Success Indicators
- **Analysis consistency**: Low variance in repeated framework applications
- **Processing throughput**: Documents analyzed per day/researcher
- **Export adoption**: Percentage of researchers using export capabilities
- **Framework expansion**: Number of frameworks successfully integrated

### System 2 Success Indicators
- **Research velocity**: Time from question to statistical results
- **Method appropriateness**: Correct statistical procedure selection rate
- **Result reliability**: Replication success rate for generated analyses
- **User satisfaction**: Researcher adoption and continued usage patterns

### Combined System Success
- **Research output quality**: Publications enabled by platform usage
- **Methodological advancement**: Novel analytical approaches developed
- **Community adoption**: Growth in active researcher user base
- **Academic impact**: Citations and integration with broader research infrastructure

---

## Risk Mitigation

### Technical Risks
- **LLM API reliability**: Implement fallback procedures and error handling
- **Database performance**: Query optimization and indexing strategies
- **Framework complexity**: Validation procedures and error detection
- **Statistical accuracy**: Comprehensive testing against established methods

### User Adoption Risks  
- **Learning curve**: Extensive documentation and training materials
- **Workflow integration**: Export capabilities and tool compatibility
- **Research validity**: Transparent methodology and audit trails
- **Community acceptance**: Academic validation and peer review processes

### Scalability Risks
- **Data growth**: Database optimization and archival strategies  
- **Computational load**: Resource monitoring and capacity planning
- **Framework proliferation**: Management and version control procedures
- **User growth**: Performance testing and infrastructure scaling

This roadmap provides a systematic approach to building robust infrastructure for framework-based discourse analysis while maintaining the flexibility and rigor required for academic research applications.