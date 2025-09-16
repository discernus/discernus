# Discernus Methodology: Computational Text Analysis Procedures

**Version**: 1.0  
**Status**: Active Standard  
**Date**: January 2025

---

## Abstract

This document describes the computational methodology implemented by the Discernus platform for systematic text analysis. The methodology consists of a three-stage pipeline: (1) framework-based dimensional analysis with internal ensemble validation, (2) statistical analysis with computational verification, and (3) evidence-integrated synthesis. The approach uses large language models for analytical reasoning while maintaining computational verification of all mathematical operations and complete provenance tracking for reproducibility.

---

## 1. Methodological Framework

### 1.1 Architecture Principles

The Discernus methodology implements a THIN software architecture where:

- **Language Model Intelligence**: Complex analytical reasoning, framework interpretation, and dimensional scoring are handled by large language models
- **Software Infrastructure**: Minimal orchestration, caching, and data management with no embedded analytical logic
- **Component Constraints**: Individual components limited to <150 lines to prevent analytical logic migration from LLMs to code
- **Verification Requirements**: All mathematical operations must be executed as code with full computational provenance

### 1.2 Input Specifications

The methodology requires three specification documents:

**Framework Specification (v10.0)**:
- Natural language description of analytical dimensions
- Scoring criteria and examples for each dimension
- Academic grounding and references
- Machine-readable YAML appendix with dimensional definitions

**Experiment Specification (v10.0)**:
- Research questions and hypotheses
- Statistical analysis plan
- Expected outcomes and deliverables
- Machine-readable YAML appendix with configuration

**Corpus Specification (v8.0.2)**:
- Document manifest with metadata
- File organization and structure
- Speaker attribution and context information
- Machine-readable YAML appendix with document listings

### 1.3 Validation Requirements

**Pre-execution Validation**:
- Specification compliance checking against Discernus standards
- Statistical prerequisites validation (sample size, group balance)
- Framework-corpus coherence assessment
- Issue classification (BLOCKING, QUALITY, SUGGESTION)

**Runtime Validation**:
- Mathematical verification through code execution
- Evidence quality assessment and confidence scoring
- Statistical methodology compliance
- Error handling and fail-fast behavior

**Post-execution Validation**:
- Provenance verification and audit trail completeness
- Output quality assessment against academic standards
- Reproducibility verification
- Peer review readiness evaluation

---

## 2. Processing Pipeline

### 2.1 Pipeline Overview

The methodology implements a three-stage processing pipeline:

```
Stage 1: Analysis → Stage 2: Synthesis → Stage 3: Finalization
```

Each stage produces specific artifacts and maintains complete provenance tracking.

### 2.2 Stage 1: Dimensional Analysis

**Objective**: Apply analytical framework to corpus documents with computational verification.

**Procedure**:

1. **Document Processing**:
   - Load corpus documents according to manifest
   - Validate document structure and metadata
   - Apply security boundary constraints

2. **Framework Application**:
   - Parse framework specification and dimensional definitions
   - Apply dimensional scoring criteria to each document
   - Generate confidence and salience scores for each dimension

3. **Internal Ensemble Analysis**:
   - Execute three independent analytical approaches per document:
     - Evidence-First: Direct textual evidence and explicit statements
     - Context-Weighted: Rhetorical context and structural positioning
     - Pattern-Based: Repetition patterns and strategic emphasis
   - Calculate median scores across approaches for self-consistency

4. **Evidence Extraction**:
   - Extract supporting textual evidence for each dimensional score
   - Link evidence quotes to specific dimensions and confidence levels
   - Validate evidence quality and relevance

5. **Document Markup**:
   - Generate marked-up version of original text with dimensional annotations
   - Insert evidence markers and dimensional tags throughout document
   - Preserve original formatting while adding analytical markup
   - Create searchable and navigable marked-up version

6. **Computational Verification**:
   - Execute all mathematical calculations as code
   - Generate computational work artifacts with full provenance
   - Validate score calculations and derived metrics

**Output Artifacts**:
- Dimensional scores (JSON format)
- Evidence database (JSON format)
- Marked-up document (Markdown format with dimensional annotations)
- Computational work artifacts (Python code)
- Analysis audit trail (structured logs)

### 2.3 Stage 2: Statistical Analysis and Synthesis

**Objective**: Perform statistical analysis and generate evidence-integrated narrative synthesis.

**Procedure**:

1. **Statistical Planning**:
   - Generate statistical analysis plan based on experiment hypotheses
   - Identify appropriate statistical tests and methodologies
   - Plan effect size calculations and confidence intervals
   - Design multiple comparison correction strategies

2. **Statistical Execution**:
   - Execute hypothesis testing using LLM-generated code
   - Perform effect size calculations and confidence intervals
   - Apply multiple comparison corrections where appropriate
   - Generate statistical visualizations and summaries

3. **Statistical Verification**:
   - Verify statistical calculations through independent code execution
   - Validate statistical assumptions and methodology compliance
   - Check for computational errors and edge cases
   - Confirm reproducibility of statistical results

4. **Evidence Curation**:
   - Retrieve supporting evidence for statistical findings
   - Validate evidence attribution and source accuracy
   - Organize evidence by statistical significance and relevance

5. **Knowledge Integration**:
   - Build comprehensive corpus index for cross-domain queries
   - Integrate statistical results with textual evidence
   - Validate consistency between quantitative and qualitative findings

6. **Narrative Synthesis**:
   - Generate comprehensive research report using statistical results
   - Integrate evidence quotes with proper attribution
   - Apply academic formatting and methodology documentation
   - Include limitations and methodological considerations

**Output Artifacts**:
- Statistical analysis results (JSON format)
- Curated evidence database (JSON format)
- Research synthesis report (Markdown format)
- Synthesis audit trail (structured logs)

### 2.4 Stage 3: Finalization and Export

**Objective**: Generate publication-ready outputs with complete provenance documentation.

**Procedure**:

1. **Data Export**:
   - Export all scores to CSV format with metadata
   - Export evidence database to CSV format with attribution
   - Export statistical results to CSV format for external replication
   - Generate summary statistics and visualizations
   - Create replication-ready datasets for external software

2. **Provenance Documentation**:
   - Consolidate all audit trails and processing logs
   - Generate complete experiment provenance documentation
   - Create reproducibility package with all inputs and outputs
   - Validate artifact integrity and completeness

3. **Publication Preparation**:
   - Format research report for academic publication
   - Include complete methodology and limitations sections
   - Generate executive summary and key findings
   - Prepare supplementary materials and data files

**Output Artifacts**:
- Publication-ready research report (Markdown format)
- Complete data exports (CSV format)
- Statistical replication datasets (CSV format)
- Marked-up documents with evidence annotations (Markdown format)
- Provenance documentation (structured format)
- Reproducibility package (Git repository)

---

## 3. Technical Implementation

### 3.1 System Components

**Orchestrator**: `CleanAnalysisOrchestrator`
- Implements 12-phase pipeline with fail-fast behavior
- Manages security boundaries and experiment isolation
- Coordinates agent execution and artifact management
- Maintains comprehensive audit logging

**Analysis Agent**: `EnhancedAnalysisAgent`
- Implements multi-tool calling architecture for structured output
- Executes internal ensemble analysis with 3-run median aggregation
- Performs mathematical verification through code execution
- Maintains framework-agnostic dimensional scoring

**Synthesis Agent**: `UnifiedSynthesisAgent`
- Generates statistical analysis through LLM code execution
- Integrates curated evidence with proper attribution
- Produces academic-quality research reports
- Maintains evidence integration and citation standards

**Supporting Infrastructure**:
- `LocalArtifactStorage`: Content-addressable storage with Git integration
- `RAGIndexManager`: Knowledge retrieval and cross-domain queries
- `AuditLogger`: Complete provenance tracking and logging
- `SecurityBoundary`: Experiment isolation and access control

### 3.2 Data Management

**Input Data Types**:
1. Corpus documents with speaker attribution and context
2. Framework specifications with dimensional definitions
3. Experiment configurations with statistical plans
4. Document metadata and analytical context
5. Statistical results and computed metrics
6. Evidence artifacts and supporting materials

**Storage Architecture**:
- Content-addressable storage using SHA256 hashing
- Git-based version control for all artifacts
- Structured JSON format for all data exchanges
- Complete provenance tracking for all transformations

**Caching Strategy**:
- Unified cache management with intelligent invalidation
- Content-based cache keys for deterministic behavior
- Performance optimization through batch processing
- Cost management through token usage tracking

---

## 4. Quality Assurance Procedures

### 4.1 Pre-Execution Validation

**Specification Compliance**:
- Validate framework specification against v10.0 standard
- Validate experiment specification against v10.0 standard
- Validate corpus specification against v8.0.2 standard
- Check file existence and accessibility

**Statistical Prerequisites**:
- Verify minimum sample size requirements
- Validate group balance for comparative analysis
- Check statistical power considerations
- Assess framework-corpus coherence

**Issue Classification**:
- **BLOCKING**: Prevents execution, must be resolved
- **QUALITY**: Impacts result quality, should be addressed
- **SUGGESTION**: Optimization opportunity, optional

### 4.2 Runtime Validation

**Mathematical Verification**:
- Execute all calculations as executable code
- Validate computational work artifacts
- Verify score calculations and derived metrics
- Check statistical methodology compliance

**Evidence Quality**:
- Assess evidence relevance and confidence
- Validate evidence attribution and source accuracy
- Check evidence-dimensional linkage
- Verify evidence quality thresholds

**Error Handling**:
- Implement fail-fast behavior for critical errors
- Log all errors with complete context
- Provide detailed error reporting and recovery guidance
- Maintain system stability during processing

### 4.3 Post-Execution Validation

**Provenance Verification**:
- Validate complete audit trail integrity
- Check artifact completeness and accessibility
- Verify Git integration and version control
- Confirm reproducibility package completeness

**Output Quality**:
- Assess academic standards compliance
- Validate statistical methodology and reporting
- Check evidence integration and citation quality
- Verify publication readiness

**Reproducibility Testing**:
- Validate complete experiment replication capability
- Test artifact integrity and accessibility
- Verify specification compliance and execution
- Confirm output consistency and quality

---

## 5. Statistical Methodology

### 5.1 Analysis Procedures

**Dimensional Scoring**:
- Apply framework dimensions to each document
- Generate confidence and salience scores
- Execute internal ensemble analysis (3-run median)
- Validate score calculations through code execution

**Statistical Planning**:
- Generate statistical analysis plan based on experiment hypotheses
- Identify appropriate statistical tests and methodologies
- Plan effect size calculations and confidence intervals
- Design multiple comparison correction strategies

**Statistical Execution**:
- Execute hypothesis testing using appropriate methods
- Calculate effect sizes and confidence intervals
- Apply multiple comparison corrections where needed
- Generate statistical visualizations and summaries

**Statistical Verification**:
- Verify statistical calculations through independent code execution
- Validate statistical assumptions and methodology compliance
- Check for computational errors and edge cases
- Confirm reproducibility of statistical results

**Evidence Integration**:
- Link statistical findings to textual evidence
- Validate evidence attribution and source accuracy
- Organize evidence by statistical significance
- Ensure proper citation and attribution standards

### 5.2 Computational Verification

**Code Execution**:
- All mathematical operations executed as Python code
- Statistical calculations verified through computational execution
- Generated code includes full provenance and documentation
- Results validated against expected statistical properties

**Quality Control**:
- Implement confidence scoring for all calculations
- Validate statistical assumptions and methodology
- Check for computational errors and edge cases
- Ensure reproducibility and consistency

---

## 6. Output Specifications

### 6.1 Data Formats

**Dimensional Scores**: JSON format with document-level scores, confidence, and metadata
**Evidence Database**: JSON format with quotes, attribution, and dimensional linkage
**Marked-up Documents**: Markdown format with dimensional annotations and evidence markers
**Statistical Results**: JSON format with test results, effect sizes, and methodology
**Statistical Replication Data**: CSV format with raw data for external software replication
**Research Report**: Markdown format with academic structure and formatting

### 6.2 Provenance Documentation

**Audit Trails**: Structured logs of all processing steps and decisions
**Artifact Tracking**: Complete inventory of all inputs, outputs, and intermediate files
**Version Control**: Git-based tracking of all changes and modifications
**Reproducibility Package**: Complete experiment package for replication

### 6.3 Publication Standards

**Academic Formatting**: Proper methodology, results, and discussion sections
**Evidence Integration**: All claims supported by textual evidence and statistical results
**Methodology Documentation**: Complete description of analytical procedures
**Limitations and Considerations**: Transparent reporting of methodological constraints

---

## 7. Implementation Requirements

### 7.1 System Requirements

**Software Dependencies**: Python 3.13+, required packages as specified in requirements.txt
**Storage Requirements**: Sufficient disk space for corpus, artifacts, and Git repository
**Computational Resources**: Adequate memory and processing power for LLM operations
**Network Access**: Internet connectivity for LLM API access

### 7.2 Configuration Requirements

**Model Configuration**: Specify analysis and synthesis models
**Security Settings**: Configure security boundaries and access controls
**Caching Configuration**: Set up content-addressable storage and cache management
**Logging Configuration**: Configure audit logging and provenance tracking

### 7.3 Validation Requirements

**Pre-execution Checks**: Validate all specifications and prerequisites
**Runtime Monitoring**: Monitor processing progress and error conditions
**Post-execution Verification**: Validate outputs and provenance completeness
**Quality Assurance**: Ensure academic standards and reproducibility

---

*This methodology document describes the computational procedures implemented by the Discernus platform for systematic text analysis. For technical implementation details, see the System Architecture documentation. For usage instructions, see the User Guide and CLI Reference.*
