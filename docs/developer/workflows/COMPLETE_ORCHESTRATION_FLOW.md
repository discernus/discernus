# Discernus Complete Orchestration Flow
*Technical Reference - Step-by-Step Asset Production*

---

## Overview

This document provides a complete technical walkthrough of Discernus orchestration, from experiment validation through final report generation. Each stage is detailed with inputs, processing steps, and outputs for full system transparency.

**Architecture**: 4-Stage THIN Pipeline with comprehensive asset tracking

```
Pre-Flight → Analysis → Synthesis → Finalization
Validation     Stage     Stage       Stage
    ↓            ↓         ↓           ↓
Coherence   Raw Scores Statistical Academic
Validation  Evidence   Analysis    Reports
Issues      Metadata   Knowledge   Full Audit
                      Integration  Trail
```

---

## Stage 0: Pre-Flight Validation

**Agent**: `ExperimentCoherenceAgent`  
**Purpose**: Validate experiment setup before expensive LLM operations  
**CLI**: `discernus run` (automatic) or `python scripts/validate_experiment.py`

### Input Assets
- `experiment.md` - Experiment specification
- `framework.md` - Analytical framework definition  
- `corpus/corpus.md` - Corpus manifest with file listings
- `corpus/*.md` - Individual corpus documents

### Processing Steps

#### Step 0.1: Artifact Loading
- **Action**: Load and parse experiment specification files
- **Validation**: File existence, JSON/YAML parsing, basic structure
- **Logging**: `ExperimentCoherenceAgent.loading_artifacts`

#### Step 0.2: Specification Compliance Check
- **Action**: Validate against Discernus Specification v7.3
- **Checks**: Required fields, format compliance, version compatibility
- **Output**: Compliance status per specification section

#### Step 0.3: Statistical Prerequisites Validation
- **Action**: Assess corpus adequacy for statistical analysis
- **Checks**: Minimum document count, dimension coverage, balanced sampling
- **Logic**: Corpus size vs. framework complexity analysis

#### Step 0.4: LLM Coherence Assessment
- **Action**: AI-powered methodology review
- **Model**: `vertex_ai/gemini-2.5-flash-lite` (default)
- **Prompt**: Framework-corpus alignment evaluation
- **Output**: Coherence score and methodological recommendations

#### Step 0.5: Issue Classification & Reporting
- **Action**: Categorize validation findings by severity
- **Categories**:
  - **BLOCKING**: Must fix (prevents execution)
  - **QUALITY**: Should fix (impacts result quality)  
  - **SUGGESTION**: Could improve (optimization)
- **Decision**: BLOCKING issues halt execution

### Output Assets
- **Validation Report**: Structured validation results
- **Issue Manifest**: Categorized problems with fix recommendations
- **Coherence Score**: AI-assessed methodology alignment
- **Execution Decision**: PASS/FAIL with detailed reasoning

### Success Criteria
✅ No BLOCKING issues present  
✅ All required files exist and parse correctly  
✅ Framework-corpus coherence above threshold  

---

## Stage 1: Analysis

**Agent**: `EnhancedAnalysisAgent`  
**Purpose**: Framework-based dimensional scoring with evidence extraction  
**Infrastructure**: Content-addressable storage, security boundaries

### Input Assets
- ✅ Validated experiment specification
- ✅ Framework definition (JSON + natural language)
- ✅ Corpus manifest and documents
- Configuration: analysis model, ensemble settings

### Processing Steps

#### Step 1.1: Security Boundary Setup
- **Action**: Initialize experiment isolation environment
- **Component**: `ExperimentSecurityBoundary`
- **Security**: Prevent path traversal, validate file access
- **Logging**: `CleanAnalysisOrchestrator.security_boundary_initialized`

#### Step 1.2: Corpus Processing
- **Action**: Load and validate corpus documents
- **Processing**: Parse markdown, extract metadata, validate structure
- **Caching**: Content-addressable storage (SHA256 hashing)
- **Output**: `corpus_artifact_hash`

#### Step 1.3: Framework-Based Analysis
- **Action**: Apply dimensional scoring framework to each document
- **Model**: Analysis model (e.g., `vertex_ai/gemini-2.5-pro`)
- **Process**: Document-by-document dimensional scoring
- **Batching**: Configurable batch sizes for efficiency

#### Step 1.4: Evidence Extraction
- **Action**: Extract supporting textual evidence for each score
- **Criteria**: Relevance, confidence, salience scoring
- **Format**: Quote + metadata + dimensional linkage
- **Quality**: Evidence quality assessment and filtering

#### Step 1.5: Artifact Storage
- **Action**: Store analysis results with full provenance
- **Storage**: LocalArtifactStorage with metadata
- **Hashing**: SHA256 content-addressable storage
- **Metadata**: Analysis parameters, model info, timestamps

### Output Assets
- **`scores_artifact_hash`**: Raw dimensional scores with calculation provenance
  - Format: JSON with scores, confidence, metadata per document
  - Schema: `{document_id: {dimension: {score, confidence, reasoning}}}`
- **`evidence_artifact_hash`**: Supporting evidence quotes with linkage
  - Format: JSON with evidence quotes, sources, dimensional connections
  - Schema: `{evidence_id: {quote, source, dimensions, confidence, salience}}`
- **`corpus_artifact_hash`**: Processed corpus with metadata
  - Format: JSON with document content, metadata, processing info
- **Analysis Audit Trail**: Complete provenance log
- **Performance Metrics**: Cost, token usage, processing time

### Success Criteria
✅ All corpus documents successfully analyzed  
✅ Dimensional scores within expected ranges  
✅ Evidence extraction quality above threshold  
✅ Artifacts stored with complete provenance  

---

## Stage 2: Synthesis

**Agent**: `ProductionThinSynthesisPipeline` → `SequentialSynthesisAgent`  
**Purpose**: Statistical analysis + narrative synthesis with RAG integration  
**Architecture**: 5-step sequential synthesis with comprehensive knowledge RAG

### Input Assets
- ✅ `scores_artifact_hash` (from Analysis)
- ✅ `evidence_artifact_hash` (from Analysis)  
- ✅ `corpus_artifact_hash` (from Analysis)
- ✅ Framework specification
- ✅ Experiment context
- Configuration: synthesis model, statistical parameters

### Processing Steps

#### Step 2.1: Statistical Analysis (MathToolkit)
- **Action**: Compute verified statistical results from raw scores
- **Components**: 
  - Descriptive statistics (means, std dev, distributions)
  - Reliability analysis (Cronbach's alpha, inter-rater reliability)
  - Correlation matrices and factor analysis
  - ANOVA and significance testing
- **Validation**: Mathematical verification, no hallucinated statistics
- **Output**: `statistical_results_hash`

#### Step 2.2: Statistical Health Validation
- **Action**: Assess statistical validity and reliability
- **Checks**: Sample size adequacy, distribution normality, reliability thresholds
- **Decision**: PASS/WARN/FAIL with recommended actions
- **Logging**: Statistical health assessment results

#### Step 2.3: RAG Index Building
- **Agent**: `ComprehensiveKnowledgeCurator`
- **Technology**: txtai semantic embeddings
- **Data Sources**: Evidence quotes, raw scores, calculated metrics, corpus text
- **Index Structure**: Unified knowledge graph with cross-domain search
- **Metadata**: Content type, source artifact, dimensional linkage

#### Step 2.4: Sequential Synthesis (5 Steps)

##### Step 2.4.1: Hypothesis Testing
- **Action**: Generate RAG queries for hypothesis evaluation
- **Query Types**: Evidence quotes, corpus text alignment
- **LLM Task**: Evaluate experimental hypotheses against evidence
- **Output**: Hypothesis testing findings

##### Step 2.4.2: Statistical Anomaly Investigation  
- **Action**: Identify and investigate statistical outliers/patterns
- **Query Types**: Raw scores, calculated metrics, evidence quotes
- **LLM Task**: Explain statistical anomalies with supporting evidence
- **Output**: Anomaly investigation findings

##### Step 2.4.3: Cross-Dimensional Pattern Discovery
- **Action**: Discover patterns across analytical dimensions
- **Query Types**: Calculated metrics, evidence quotes
- **LLM Task**: Identify cross-dimensional relationships and themes
- **Output**: Pattern discovery findings

##### Step 2.4.4: Statistical Framework Fit Assessment
- **Action**: Evaluate how well data fits the analytical framework
- **Input**: Direct statistical context (no RAG queries)
- **LLM Task**: Assess framework validity and limitations
- **Output**: Framework fit assessment

##### Step 2.4.5: Final Integration
- **Action**: Synthesize all findings into comprehensive narrative
- **Input**: All previous findings + aggregated RAG evidence
- **LLM Task**: Create coherent academic narrative with proper citations
- **Output**: Final synthesis report

#### Step 2.5: Academic Report Generation
- **Component**: `ThreePartReportGenerator`
- **Structure**: 
  - **Part I**: Executive Summary & Key Findings
  - **Part II**: Detailed Analysis & Evidence
  - **Part III**: Statistical Appendix & Methodology
- **Features**: Proper citations, cost transparency, provenance metadata
- **Output**: `final_report_hash`

### Output Assets
- **`statistical_results_hash`**: Verified mathematical analysis
  - Content: Descriptive stats, reliability measures, correlations, ANOVA
  - Format: JSON with computational verification
- **`final_report_hash`**: Three-part academic report
  - Content: Executive summary, detailed analysis, statistical appendix
  - Format: Markdown with proper academic structure
- **RAG Index**: Persistent txtai knowledge graph
  - Content: Searchable evidence, scores, metrics, corpus
  - Technology: txtai embeddings with metadata filtering
- **Synthesis Provenance Log**: Complete RAG query and synthesis audit trail
- **Cost Metadata**: Token usage, model costs, processing time per step

### Success Criteria
✅ Statistical analysis mathematically verified  
✅ All 5 synthesis steps completed successfully  
✅ RAG queries return relevant evidence  
✅ Final report meets academic standards  
✅ Complete provenance maintained  

---

## Stage 3: Finalization

**Agent**: `CleanAnalysisOrchestrator` + `CSVExportAgent` + `ProvenanceOrganizer`  
**Purpose**: Export research-ready artifacts with complete audit trail  
**Output**: Publication-ready research package

### Input Assets
- ✅ All synthesis outputs (`statistical_results_hash`, `final_report_hash`)
- ✅ All analysis outputs (`scores_artifact_hash`, `evidence_artifact_hash`)
- ✅ Complete audit trail from all stages
- ✅ Session cost and performance data

### Processing Steps

#### Step 3.1: CSV Export Generation
- **Agent**: `CSVExportAgent`
- **Action**: Convert all JSON artifacts to researcher-friendly CSV format
- **Exports**:
  - `scores.csv`: Raw dimensional scores with metadata
  - `evidence.csv`: Evidence quotes with source attribution  
  - `statistics.csv`: Statistical results and calculations
  - `corpus_metadata.csv`: Document metadata and processing info
- **Features**: Proper escaping, UTF-8 encoding, academic citation format

#### Step 3.2: Cost Transparency Integration
- **Action**: Add comprehensive cost reporting to final report
- **Data**: Token usage by model, cost by agent, total session cost
- **Format**: Structured cost appendix for research transparency
- **Purpose**: Enable cost-aware research methodology decisions

#### Step 3.3: Provenance Organization
- **Agent**: `ProvenanceOrganizer`  
- **Action**: Structure all artifacts for academic review and replication
- **Organization**: 
  - `/results/` - Final outputs (report, CSVs)
  - `/artifacts/` - Intermediate processing artifacts
  - `/audit/` - Complete provenance and audit logs
  - `/cache/` - Content-addressable artifact cache
- **Metadata**: Artifact relationships, dependency graphs, processing lineage

#### Step 3.4: Manifest Finalization
- **Component**: `EnhancedManifest`
- **Action**: Complete execution record with all stage metadata
- **Content**: 
  - Execution stages with timestamps
  - Agent versions and configurations  
  - Input/output artifact hashes
  - Performance and cost metrics
  - Error handling and recovery actions

#### Step 3.5: Git Provenance Commit
- **Action**: Commit complete run to version control
- **Purpose**: Enable exact replication and peer review
- **Content**: All results, artifacts, audit trails
- **Message**: Structured commit with run metadata
- **Branch**: Experiment branch for organized research workflow

### Output Assets
- **`final_report.md`**: Complete three-part academic report
- **`scores.csv`**: Raw dimensional scores (researcher-friendly)
- **`evidence.csv`**: Supporting evidence with citations
- **`statistics.csv`**: Statistical analysis results  
- **`corpus_metadata.csv`**: Document processing metadata
- **`manifest.json`**: Complete execution record
- **`audit_trail.json`**: Full provenance and cost data
- **Git Commit**: Versioned research package for replication

### Success Criteria
✅ All CSV exports generated successfully  
✅ Provenance organization completed  
✅ Manifest finalized with complete metadata  
✅ Git commit successful with proper message  
✅ Research package ready for peer review  

---

## Asset Flow Summary

### Content-Addressable Storage
All intermediate artifacts use SHA256 hashing for:
- **Deduplication**: Identical inputs produce identical outputs
- **Caching**: Expensive operations cached automatically  
- **Provenance**: Complete lineage tracking
- **Verification**: Integrity checking and validation

### Asset Dependencies
```
experiment.md + framework.md + corpus/ 
    ↓ (Validation)
validation_report + coherence_score
    ↓ (Analysis) 
scores_artifact_hash + evidence_artifact_hash + corpus_artifact_hash
    ↓ (Synthesis)
statistical_results_hash + final_report_hash + rag_index
    ↓ (Finalization)
final_report.md + *.csv + manifest.json + audit_trail.json + git_commit
```

### Research Package Output
The final research package includes:
- **Publication-Ready Report**: Three-part academic structure
- **Raw Data**: CSV exports for independent analysis
- **Statistical Verification**: Computational audit trail  
- **Complete Provenance**: Full replication capability
- **Cost Transparency**: Research methodology cost assessment
- **Peer Review Ready**: Structured for academic evaluation

---

## Error Handling & Recovery

### Stage-Level Recovery
- **Validation Failures**: Detailed issue reports with fix recommendations
- **Analysis Failures**: Batch-level retry with partial success handling
- **Synthesis Failures**: Step-level recovery with checkpoint restoration
- **Finalization Failures**: Asset-level retry with integrity checking

### Audit Trail Preservation
- All errors logged with full context
- Recovery actions recorded in provenance
- Cost tracking continues through error states
- Partial results preserved for analysis

### Resume Capability
- Content-addressable storage enables exact resume
- Manifest-based state recovery
- Skip completed stages automatically
- Preserve all provenance through resume operations

---

*Document Version: 1.0*  
*Last Updated: August 2025*  
*Architecture: THIN v2.0*
