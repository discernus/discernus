# DCS Research Workflow Specification v1.0
**Version:** 1.0  
**Date:** January 27, 2025  
**Author:** Jeffrey Whatcott  
**Status:** FOUNDATIONAL REFERENCE  
**Scope:** Complete research lifecycle specification for DCS-based discourse analysis

---

## Executive Summary

The DCS Research Workflow establishes the complete research lifecycle for computational discourse analysis, from initial theoretical development through academic publication. This specification defines **six distinct workflow stages** with environment-specific optimization, ensuring seamless progression from exploratory framework development to production-grade academic research.

**Core Principle**: Each research stage has an **optimal environment** based on the primary cognitive task, with clear handoff protocols between stages and robust version control throughout the entire lifecycle.

---

## 1. Complete Research Lifecycle Overview

### 1.1 Six-Stage Research Workflow

```
Framework Development → Prototype Testing → Experiment Design → 
Corpus Preparation → Analysis Execution → Results Interpretation
```

**Stage 1: Framework Development** (IDE-Optimized)
- **Primary Task**: Theoretical conceptualization and framework architecture
- **Environment**: IDE (VS Code, PyCharm) with YAML editing and validation
- **Output**: Framework Specification v3.2 compliant YAML files
- **Duration**: Days to weeks of iterative theoretical work

**Stage 2: Prototype Testing** (Chatbot-Optimized)  
- **Primary Task**: Rapid directional validation and framework refinement
- **Environment**: Consumer chatbots (ChatGPT, Claude) for quick sanity checks
- **Output**: Qualitative feedback on framework coherence and text matching
- **Duration**: Hours to days of exploratory testing

**Stage 3: Experiment Design** (IDE-Optimized)
- **Primary Task**: Systematic methodology construction and validation protocol
- **Environment**: IDE for experiment YAML creation and parameter specification
- **Output**: Complete experiment specification with embedded or referenced frameworks
- **Duration**: Days of methodological planning

**Stage 4: Corpus Preparation** (CLI-Optimized)
- **Primary Task**: Data ingestion, preprocessing, and quality validation
- **Environment**: Command line tools for batch processing and data pipeline execution
- **Output**: Clean, validated corpus with metadata and provenance tracking
- **Duration**: Hours to days depending on corpus complexity

**Stage 5: Analysis Execution** (CLI-Optimized)
- **Primary Task**: Computational analysis at scale with quality monitoring
- **Environment**: Command line orchestration for production-grade batch processing  
- **Output**: Complete analysis results with statistical validation and quality metrics
- **Duration**: Minutes to hours depending on corpus size and framework complexity

**Stage 6: Results Interpretation** (Jupyter-Optimized)
- **Primary Task**: Interactive exploration, visualization, and narrative construction
- **Environment**: Jupyter notebooks for analysis, visualization, and academic deliverable creation
- **Output**: Publication-ready analyses, figures, tables, and academic narratives
- **Duration**: Days to weeks of analytical exploration and interpretation

---

## 2. Environment Integration & Tool Selection

### 2.1 Framework Development vs Experiment Design

**The Two-Mode Architecture Solution**:

**Development Mode (Framework Embedded in Experiment)**:
- Framework and experiment evolve together in single YAML file
- Perfect for "3am lab cranking" rapid iteration
- Joint versioning and atomic changes
- Natural for theoretical development workflow

**Publication Mode (Framework Referenced by Experiment)**:
- Mature frameworks extracted to standalone files
- Experiment references framework by registry key
- Clean separation for academic rigor and reusability
- Framework can be used across multiple experiments

### 2.2 Cross-Environment Data Flow

**IDE → Chatbot**: Framework YAML copied for rapid validation
**Chatbot → IDE**: Refinement insights integrated into framework
**IDE → CLI**: Experiment YAML drives corpus preparation and analysis
**CLI → Jupyter**: Results imported as DataFrames for exploration
**Jupyter → Publication**: Academic deliverables exported in standard formats

---

## 3. BYU Collaboration Implementation

### 3.1 Phase-Specific Workflow Mapping

**BYU Phase 1: Methodological Validation**
- **Framework Development (IDE)**: Populism/Pluralism enhancement with Tamaki & Fuks insights
- **Experiment Design (IDE)**: Four-condition comparative methodology
- **Analysis Execution (CLI)**: Batch processing across conditions
- **Results Interpretation (Jupyter)**: Interactive validation notebook

**BYU Phase 2: Academic Integration**
- **Corpus Preparation (CLI)**: Global Populism Database scaling
- **Results Interpretation (Jupyter)**: Graduate student tutorial templates
- **Publication Pipeline**: Academic workflow integration

### 3.2 Deliverable Environment Specifications

All BYU deliverables follow **Jupyter Native Integration Heuristics**:
1. **Data Fluidity**: Results exportable to Pandas DataFrames
2. **Standard Library Integration**: Built on matplotlib/seaborn/plotly
3. **Pedagogical Clarity**: Markdown narrative with code explanation
4. **Self-Containment**: "Run All Cells" executes without errors
5. **Modularity**: Functions copyable and hackable for researcher needs

---

## 4. Quality Gates & Handoff Protocols

### 4.1 Stage Progression Requirements

**Framework Development → Prototype Testing**:
- Framework Specification v3.2 compliance validated
- Theoretical coherence documented
- Academic citations complete

**Prototype Testing → Experiment Design**:
- Directional accuracy confirmed across test cases
- Edge cases identified and documented
- Framework refinements integrated

**Experiment Design → Corpus Preparation**:
- Complete experiment specification with methodology
- Statistical validation approach defined
- Academic rigor standards satisfied

**Corpus Preparation → Analysis Execution**:
- Corpus quality metrics meet specifications
- Metadata completeness validated
- Analysis pipeline configured

**Analysis Execution → Results Interpretation**:
- Error-free execution with quality monitoring
- Statistical validation successful
- Results formatted for Jupyter integration

### 4.2 Version Control Integration

**Repository Structure**:
```
discernus/
├── frameworks/              # Framework development outputs
├── experiments/             # Experiment design specifications  
├── corpus/                  # Corpus preparation results
├── results/                 # Analysis execution outputs
├── analysis/                # Jupyter interpretation notebooks
└── scripts/                 # CLI automation tools
```

---

## 5. Success Metrics & Validation

### 5.1 Workflow Effectiveness Criteria

**Development Velocity**: Framework → Publication cycle time optimization
**Academic Quality**: Peer review standards satisfaction across all stages
**Collaboration Support**: Multi-researcher workflow seamless operation
**Reproducibility**: Independent replication success rate
**Scalability**: Performance across prototype → production scale transitions

### 5.2 BYU-Specific Success Validation

**Sarah Chen Evaluation Criteria**:
- Jupyter Native Integration: 4/5 heuristics satisfied minimum
- BYU Replication Accuracy: r > 0.80 correlation with manual coding
- Academic Defensibility: Methodology suitable for publication
- Graduate Student Usability: <2 hour learning curve
- Strategic Partnership Value: Novel research capabilities enabled

---

**Workflow Status:** FOUNDATIONAL SPECIFICATION v1.0  
**Cross-References:** Framework Specification v3.2, BYU Methodological Validation Protocol, BYU Strategic Engagement Plan 