# Alpha Feature Complete Milestone

**Milestone**: Alpha Feature Complete
**Status**: Active
**Issues**: Open issues related to completing core features for Alpha release

---

## Open Issues

### Implement Resume from Statistical Preparation to Full Synthesis
- **Issue**: #405
- **Labels**: enhancement, orchestration
- **Assignees**: 
- **Created**: 2025-08-11
- **Updated**: 2025-08-11
- **Milestone**: Alpha Feature Complete
- **Description**: Implement Resume from Statistical Preparation to Full Synthesis

**Issue Summary**: Implement the ability to resume from statistical preparation to full synthesis, providing workflow flexibility for researchers who initially chose the offramp but later want complete analysis.

**User Story**: As a researcher, I want to be able to continue from my statistical preparation results to full Discernus synthesis when needed, so that I have maximum flexibility in my research workflow.

**Acceptance Criteria**:
- [ ] `discernus run --resume-from-stats` command functionality
- [ ] Automatic detection of existing statistical preparation artifacts
- [ ] Seamless continuation from statistical prep to synthesis stage
- [ ] Updated manifest.json with resume history and provenance
- [ ] Extended directory structure with synthesis artifacts
- [ ] Preserved statistical preparation results alongside synthesis results

**Technical Tasks**:
- [ ] Implement `--resume-from-stats` CLI option
- [ ] Add resume detection logic in ThinOrchestrator
- [ ] Extend existing directory structure without overwriting
- [ ] Update manifest with resume metadata and timeline
- [ ] Preserve complete audit trail across resume operations

**Definition of Done**:
- [ ] Resume functionality works seamlessly from statistical prep
- [ ] All original statistical prep artifacts preserved
- [ ] Manifest shows complete workflow history
- [ ] Directory structure maintains both statistical prep and synthesis results

**Story Points**: 4
**Epic**: 401

---

### Implement Research Workflow Configuration Profiles
- **Issue**: #404
- **Labels**: enhancement, peer-review, user-experience
- **Assignees**: 
- **Created**: 2025-08-11
- **Updated**: 2025-08-11
- **Milestone**: Alpha Feature Complete
- **Description**: Implement Research Workflow Configuration Profiles

**Issue Summary**: Create configurable research workflow profiles that allow researchers to customize their analysis and synthesis pipelines based on their specific research needs and preferences.

**User Story**: As a researcher, I want to be able to select from predefined workflow profiles or create custom ones, so that I can optimize my research process for different types of analysis.

**Acceptance Criteria**:
- [ ] Predefined workflow profiles (e.g., "Quick Analysis", "Deep Dive", "Peer Review Ready")
- [ ] Custom profile creation and editing capabilities
- [ ] Profile selection via CLI and configuration files
- [ ] Profile validation and error handling
- [ ] Profile sharing and version control

**Technical Tasks**:
- [ ] Design workflow profile schema
- [ ] Implement profile management system
- [ ] Create profile validation logic
- [ ] Add CLI commands for profile operations
- [ ] Implement profile persistence and sharing

**Definition of Done**:
- [ ] Researchers can select and customize workflow profiles
- [ ] Profiles are validated and error-free
- [ ] Profile system integrates with existing CLI
- [ ] Documentation covers all profile features

**Story Points**: 6
**Epic**: 401

---

### Implement Evidence-Integrated CSV Export for Statistical Analysis
- **Issue**: #403
- **Labels**: enhancement, statistical-methodology
- **Assignees**: 
- **Created**: 2025-08-11
- **Updated**: 2025-08-11
- **Milestone**: Alpha Feature Complete
- **Description**: Implement Evidence-Integrated CSV Export for Statistical Analysis

**Issue Summary**: Enhance the CSV export functionality to include evidence integration, allowing researchers to export statistical results with linked evidence for comprehensive analysis and reporting.

**User Story**: As a researcher, I want to export my statistical analysis results with integrated evidence, so that I can maintain the connection between data and supporting evidence in external tools.

**Acceptance Criteria**:
- [ ] CSV export includes evidence columns
- [ ] Evidence properly linked to statistical results
- [ ] Export format is compatible with external analysis tools
- [ ] Evidence metadata preserved in export
- [ ] Export performance optimized for large datasets

**Technical Tasks**:
- [ ] Extend CSV export schema to include evidence
- [ ] Implement evidence linking logic
- [ ] Optimize export performance
- [ ] Add export format validation
- [ ] Create export documentation

**Definition of Done**:
- [ ] CSV exports include evidence integration
- [ ] Export performance meets requirements
- [ ] Format is compatible with external tools
- [ ] Documentation covers export features

**Story Points**: 5
**Epic**: 401

---

### Implement Statistical Preparation Stage and CSV Export System
- **Issue**: #402
- **Labels**: enhancement, orchestration
- **Assignees**: 
- **Created**: 2025-08-11
- **Updated**: 2025-08-11
- **Milestone**: Alpha Feature Complete
- **Description**: Implement Statistical Preparation Stage and CSV Export System

**Issue Summary**: Implement the core infrastructure for statistical preparation mode, including the orchestration stage, derived metrics calculation, and CSV export system.

**User Story**: As a researcher, I want to run `discernus run --statistical-prep` and receive analysis-ready CSV datasets so that I can perform statistical analysis using my preferred tools.

**Acceptance Criteria**:
- [ ] Add `--statistical-prep` CLI flag to ThinOrchestrator
- [ ] Implement derived metrics calculation using existing MathToolkit
- [ ] Create CSV export with raw scores, derived metrics, and evidence quotes
- [ ] Generate variable codebook with column definitions
- [ ] Store statistical preparation artifacts with content-addressable hashing
- [ ] Update manifest.json to track statistical preparation stage
- [ ] Maintain complete provenance chain for resume capability

**Technical Tasks**:
- [ ] Extend `ThinOrchestrator.run_experiment()` with `statistical_prep_only` parameter
- [ ] Create `_calculate_derived_metrics()` method using framework calculation specs
- [ ] Implement `_export_statistical_preparation_package()` for CSV generation
- [ ] Add `statistical_preparation` stage to EnhancedManifest
- [ ] Update ProvenanceOrganizer for statistical prep artifacts

**Definition of Done**:
- [ ] Statistical preparation mode produces complete CSV datasets
- [ ] All artifacts stored with SHA-256 hashing for provenance
- [ ] Manifest tracking works correctly
- [ ] Unit tests pass for new functionality

**Story Points**: 8
**Epic**: 401

---

### Epic: Sequential Synthesis Agent Architecture v2.0
- **Issue**: #354
- **Labels**: enhancement, epic
- **Assignees**: 
- **Created**: 2025-08-08
- **Updated**: 2025-08-09
- **Milestone**: Alpha Feature Complete
- **Description**: Epic: Sequential Synthesis Agent Architecture v2.0

**Full Description**:
# Epic #354: Sequential Synthesis Agent Architecture v2.0

**Date**: January 9, 2025  
**Status**: 🔄 **REFACTORED** - Sequential Synthesis Agent Architecture  
**Strategic Objective**: Replace experiment-specific InvestigativeSynthesisAgent with framework-agnostic sequential synthesis following proven CFF analysis patterns

## 🎯 Strategic Focus: Sequential Synthesis Agent v2.0

**Core Mission**: Transform synthesis pipeline from brittle, experiment-specific hardcoding to a robust, framework-agnostic sequential synthesis agent that follows THIN principles and scales to thousands of documents.

**Technical Foundation**: Implement clean data separation (Context vs Lookup), sequential prompting with externalized YAML, and intelligent RAG utilization that eliminates framework pollution while maintaining academic rigor.

## 🏗️ Architectural Vision

### **Clean Data Separation Architecture**
Transform from conflated data flow to clean separation:

```python
# Current: Everything mixed in RAG
rag_index.add(framework_definitions + evidence_quotes + scores + corpus)
# Result: Framework pollution dominates search results

# New: Context vs Lookup Separation  
direct_context = {
    'experiment': hypotheses_and_research_questions,
    'framework': methodology_and_dimensions, 
    'corpus': document_manifest_and_speakers,
    'statistics': verified_statistical_tables_from_mathtoolkit
}

rag_lookup = {
    'evidence_quotes': textual_evidence_with_speaker_attribution,
    'corpus_text': chunked_paragraphs_for_quote_extraction,
    'raw_scores': queryable_dimension_scores,
    'calculated_metrics': queryable_derived_indices
}
```

### **Sequential Synthesis Pipeline**
Replace single-call optimization fallacy with focused sequential steps:

```yaml
# Step 1: Hypothesis Testing Investigation
# Step 2: Statistical Anomaly Investigation  
# Step 3: Cross-Dimensional Pattern Discovery
# Step 4: Statistical Framework Fit Assessment (Tiered)
# Step 5: Final Integration & Report Synthesis
```

### **Framework-Agnostic Query Generation**
Eliminate hardcoded experiment assumptions:

```python
# Current Anti-Pattern: Experiment-specific hardcoding
"McCain quote showing institutional dignity"
"Sanders quote expressing tribal dominance"

# New: Statistical-driven query generation
"Speaker with highest {dimension} score evidence"
"Evidence for statistical outlier: F-statistic {value}"
"Quote demonstrating {pattern} from statistical analysis"
```

## 📋 Epic Requirements Matrix

### **PHASE 1: Clean RAG Architecture & Data Separation (Week 1)**

#### Content-Type Filtering & Framework Pollution Elimination
- **REQ-CF-001**: Implement txtai content_type filtering using `where` clauses
- **REQ-CF-002**: Separate framework definitions from evidence index
- **REQ-CF-003**: Implement content weighting (evidence > corpus > metrics)
- **REQ-CF-004**: Add hybrid search (BM25 + embeddings) for precision
- **REQ-CF-005**: Eliminate framework pollution in search results

#### Statistical Table Contracts & MathToolkit Integration  
- **REQ-ST-001**: Design LLM-optimized JSON statistical output format
- **REQ-ST-002**: Implement ANOVA summary tables for direct LLM consumption
- **REQ-ST-003**: Add reliability summary tables with interpretation
- **REQ-ST-004**: Create descriptive statistics tables for Bronze Standard
- **REQ-ST-005**: Eliminate pandas/numpy objects in synthesis pipeline

#### Evidence Budgeting & Selection Policy
- **REQ-EB-001**: Implement token-budget based evidence selection
- **REQ-EB-002**: Add MMR (Maximal Marginal Relevance) for diversity
- **REQ-EB-003**: Implement evidence deduplication by hash
- **REQ-EB-004**: Replace arbitrary limits with intelligent selection
- **REQ-EB-005**: Ensure speaker and topic diversity in evidence

### **PHASE 2: Sequential Synthesis Agent Implementation (Week 2)**

#### Externalized YAML Prompting Framework
- **REQ-YP-001**: Create synthesis_prompts.yaml with all templates
- **REQ-YP-002**: Implement Evidence-First synthesis constraint in prompts
- **REQ-YP-003**: Add No-LM-Math constraint enforcement in prompts  
- **REQ-YP-004**: Design step-specific task descriptions and examples
- **REQ-YP-005**: Enable easy prompt iteration without code changes

#### Framework-Agnostic Sequential Pipeline
- **REQ-SP-001**: Implement 5-step sequential synthesis process
- **REQ-SP-002**: Add statistical-driven query generation (no hardcoding)
- **REQ-SP-003**: Implement focused cognitive load per step
- **REQ-SP-004**: Add cross-step information flow and integration
- **REQ-SP-005**: Ensure framework and experiment agnosticity

#### Statistical Framework Fit Assessment (Tiered Approach)
- **REQ-FF-001**: Implement Gold Standard (ANOVA + Reliability) assessment
- **REQ-FF-002**: Implement Silver Standard (Reliability only) assessment
- **REQ-FF-003**: Implement Bronze Standard (Descriptive stats) assessment
- **REQ-FF-004**: Add automatic tier selection based on available data
- **REQ-FF-005**: Generate quantitative framework fit conclusions

### **PHASE 3: Integration, Validation & Provenance (Week 3)**

#### Provenance & Audit Logging
- **REQ-AL-001**: Log every prompt, model ID, and temperature setting
- **REQ-AL-002**: Log all RAG queries with results and relevance scores
- **REQ-AL-003**: Create chain-of-custody linking claims to evidence
- **REQ-AL-004**: Add References appendix with complete provenance
- **REQ-AL-005**: Implement append-only audit logging for reproducibility

#### Integration Testing & Validation
- **REQ-IT-001**: Test with existing CAF/CHF/ECF experiments
- **REQ-IT-002**: Validate framework agnosticity across different frameworks
- **REQ-IT-003**: Test scalability from 10 to 2000+ documents
- **REQ-IT-004**: Ensure academic quality maintenance at scale
- **REQ-IT-005**: Validate THIN compliance across all components

## 🗺️ Implementation Roadmap

### **Phase 1: Clean RAG Architecture** *(Week 1)*
- [ ] **Issue #361**: Comprehensive Knowledge RAG Implementation
  - Modify `ComprehensiveKnowledgeCurator` for content-type filtering
  - Separate framework definitions from evidence index  
  - Implement evidence-focused indexing with proper weighting
  - Test query effectiveness with new architecture
- [ ] **Issue #362**: LLM-Powered Query Intelligence & Cross-Domain Reasoning
  - Implement txtai `where` clause filtering by content_type
  - Add hybrid search (BM25 + embeddings) for retrieval precision
  - Validate framework pollution elimination

### **Phase 2: Sequential Synthesis Agent** *(Week 2)*
- [ ] **Issue #XXX**: Create New Sequential Synthesis Agent
  - Replace current `InvestigativeSynthesisAgent` with `SequentialSynthesisAgent`
  - Implement externalized YAML prompt templates (`synthesis_prompts.yaml`)
  - Build query generation based on statistical patterns
  - Test with existing simple_test experiment
- [ ] **Issue #XXX**: Implement Sequential Processing Pipeline
  - Step 1: Hypothesis Testing Investigation
  - Step 2: Statistical Anomaly Investigation  
  - Step 3: Cross-Dimensional Pattern Discovery
  - Step 4: Statistical Framework Fit Assessment (Tiered)
  - Step 5: Final Integration & Report Synthesis

### **Phase 3: MathToolkit Integration** *(Week 3)*
- [ ] **Issue #XXX**: LLM-Optimized Statistical Output Format
  - Add LLM-optimized formatting to MathToolkit statistical outputs
  - Create standardized JSON tables for direct LLM consumption
  - Implement provenance-linked statistical tables
  - Test end-to-end pipeline with clean data flow
- [ ] **Issue #XXX**: Statistical Results Formatter
  - Convert raw pandas/numpy objects to LLM-friendly tables
  - Add interpretation summaries and key findings extraction
  - Validate academic report quality with new format

### **Phase 4: Production Integration** *(Week 4)*
- [ ] **Issue #366**: Refactor ProductionThinSynthesisPipeline for Sequential RAG Integration
  - Integrate new `SequentialSynthesisAgent` with existing pipeline
  - Update orchestration for clean context vs lookup data separation
  - Maintain backward compatibility during transition
- [ ] **Issue #367**: Integration Testing for Sequential Synthesis Architecture
  - Test with existing CAF/CHF/ECF experiments
  - Validate cross-domain reasoning accuracy
  - Performance testing with larger corpora (100/500/2000+ documents)
- [ ] **Issue #363**: Research Platform Scalability & Modern Architecture Validation
  - Comprehensive performance validation at scale
  - Documentation of architectural advances
  - Production readiness assessment

## ✅ Success Criteria

**Epic #354 COMPLETE when ALL criteria met:**

1. ✅ **Clean Data Separation**: Context (<100KB) flows directly to LLM; lookup data via RAG
2. ✅ **Framework Pollution Eliminated**: txtai queries filtered by content_type, no framework definitions in evidence results  
3. ✅ **Framework Agnostic**: Zero hardcoded assumptions about experiments, speakers, or corpora
4. ✅ **Sequential Pipeline**: 5-step process with externalized YAML prompts operational
5. ✅ **Statistical Integration**: MathToolkit produces LLM-optimized JSON tables
6. ✅ **Framework Fit Assessment**: Tiered approach (Gold/Silver/Bronze) implemented and tested
7. ✅ **Evidence-First Synthesis**: Every claim backed by statistical result + textual quote
8. ✅ **Provenance Chain**: Complete traceability from claims to statistical tables and evidence quotes
9. ✅ **Scalability**: Tested and validated from 10 to 2000+ documents
10. ✅ **THIN Compliance**: LLM intelligence drives all reasoning; minimal software coordination

## 🔗 Dependencies & Child Issues

**Core Architecture Issues:**
- Issue #XXX: RAG Content-Type Filtering & Framework Pollution Elimination
- Issue #XXX: MathToolkit LLM-Optimized Output Formatting
- Issue #XXX: Sequential Synthesis Agent Implementation (YAML-based)
- Issue #XXX: Statistical Framework Fit Assessment (Tiered Approach)
- Issue #XXX: Evidence Budgeting & MMR Selection Policy
- Issue #XXX: Framework-Agnostic Query Generation System
- Issue #XXX: Comprehensive Provenance & Audit Logging System
- Issue #XXX: Integration Testing for Sequential Synthesis Architecture
- Issue #XXX: Performance & Scalability Validation (10-2000+ documents)

**Prerequisites:**
- MathToolkit with verified calculations (already implemented)
- LocalArtifactStorage with content-addressable artifacts (already implemented)
- ComprehensiveKnowledgeCurator foundation (needs enhancement)

**Related Epics:**
- Epic #365: Academic Quality & Standards Implementation (quality validation)

## 🧪 Validation Experiments

**Test 1**: Simple_test experiment with sequential synthesis (framework agnosticity)  
**Test 2**: CAF experiment validation (existing framework compatibility)
**Test 3**: Framework pollution elimination verification (search result quality)
**Test 4**: Statistical framework fit assessment (tiered approach validation)
**Test 5**: Scalability testing (10/100/1000/2000+ document performance)
**Test 6**: Cross-framework validation (CHF/ECF compatibility)

## 📊 Technical Architecture Metrics

**Sequential Synthesis Benchmarks:**
- Framework agnosticity: Zero hardcoded experiment assumptions
- Data separation: Clean context vs lookup architecture operational  
- RAG precision: >80% relevant evidence (no framework pollution)
- Statistical integration: JSON tables replace pandas/numpy objects
- Framework fit: Quantitative assessment in every synthesis report
- Provenance coverage: 100% of claims traceable to sources
- Scalability: <2s queries maintained at 2000+ document scale
- THIN compliance: LLM intelligence over software coordination

---

**Strategic Impact**: This epic transforms Discernus synthesis from a brittle, experiment-specific tool to a robust, framework-agnostic sequential synthesis agent that follows THIN principles, eliminates architectural anti-patterns, and scales to enterprise research requirements while maintaining rigorous academic standards.

---

### Epic: Advanced CLI Workflows - Command Chaining & Workbench Integration
- **Issue**: #307
- **Labels**: epic
- **Assignees**: 
- **Created**: 2025-08-05
- **Updated**: 2025-08-06
- **Milestone**: Alpha Feature Complete
- **Description**: Epic: Advanced CLI Workflows - Command Chaining & Workbench Integration

**Full Description**:
## Summary

Enable advanced research workflow patterns through command chaining and seamless workbench-to-operational promotion.

## Scope: Research Workflow Optimization

This epic focuses on streamlining common research patterns and eliminating workflow friction.

## Issues Included

### 🎯 Command Chaining Infrastructure  
- **#278** - CLI Enhancement: Command Chaining and User Experience Improvements
  - Fix existing `discernus workflow` command parsing issues
  - Enable patterns: `discernus workflow promote run experiment`
  - Streamlined research iteration cycles
  - **Status**: Infrastructure exists, needs Click parsing fixes

### 🎯 Workbench Integration
- **#275** - Epic: Researcher Workbench Workflow Enhancement  
  - Complete `discernus promote run` integration
  - Archive workbench files during promotion
  - Execute operational experiment seamlessly
  - **Status**: Mostly implemented, needs integration completion

## Current State ✅

**Existing Infrastructure**:
- ✅ `discernus workflow` command exists with chaining logic
- ✅ `discernus promote` command functional with cleanup
- ✅ Individual commands work correctly
- ✅ Error handling and early exit on failures

**Working Patterns**:
```bash
# These work today
discernus workflow promote run projects/experiment --cleanup
discernus workflow validate run projects/experiment  
discernus workflow promote validate run projects/experiment
```

## Desired State 🎯

**Enhanced Patterns**:
```bash
# Streamlined research workflows
discernus promote run experiment    # Direct promote → run
discernus validate run experiment   # Validate → run  
discernus iterate experiment        # Promote → run (research iteration)
discernus deploy experiment         # Promote → validate → run (full deployment)
```

**Workbench Integration**:
- `discernus promote run` archives workbench files and executes operational experiment
- Seamless transition from iteration to execution
- Automatic file management during promotion

## Technical Implementation

### Phase 1: Fix Command Chaining Issues
- **Problem**: Click argument parsing with `nargs=-1` before final argument
- **Solution**: Debug and fix parsing, or implement alternative syntax
- **Current Workaround**: `discernus workflow` command works

### Phase 2: Direct Command Integration  
- Enable `discernus promote run` as direct command (not just via workflow)
- Integrate promotion logic directly into run command
- Add option parsing for combined operations

### Phase 3: Workbench Archive Integration
- Complete workbench → operational file management
- Ensure `promote run` archives workbench files before execution
- Test end-to-end workflow patterns

## Research Impact

**Current Pain Points**:
- Researchers must remember multiple command sequences
- Manual coordination of promote → run cycles
- Verbose workflow command syntax

**Expected Benefits**:
- Faster research iteration: `promote run` in one command
- Reduced cognitive load for common patterns
- Natural workflow matching research thinking
- Automatic file management during transitions

## Success Criteria

### Command Chaining
- [ ] `discernus promote run experiment` works as direct command
- [ ] `discernus workflow` parsing issues resolved
- [ ] Options properly inherit between chained commands
- [ ] Error handling with early exit on failures

### Workbench Integration  
- [ ] `promote run` archives workbench files automatically
- [ ] Seamless transition from workbench to operational execution
- [ ] File management tested end-to-end
- [ ] Integration with existing promote cleanup logic

### User Experience
- [ ] Natural command patterns for research workflows
- [ ] Dry-run support shows complete workflow plan
- [ ] Clear error messages for workflow failures
- [ ] Documentation updated with workflow examples

## Implementation Priority

**Phase 1**: Fix existing workflow command parsing
**Phase 2**: Implement direct `promote run` command  
**Phase 3**: Complete workbench archive integration
**Phase 4**: Add convenience commands (`iterate`, `deploy`)

## Dependencies

- CLI Fundamentals Epic (#306) for professional interface
- Existing promote and run commands (already functional)
- Workbench promotion logic (mostly complete per user feedback)

## User Impact

**High**: Eliminates workflow friction for active researchers
**Medium**: Streamlines common research iteration patterns
**Low**: Nice workflow sugar for power users

This epic transforms Discernus from individual commands to integrated research workflows.

---

### Epic: CLI Fundamentals - Professional Interface & Standards
- **Issue**: #306
- **Labels**: epic
- **Assignees**: 
- **Created**: 2025-08-05
- **Updated**: 2025-08-06
- **Milestone**: Alpha Feature Complete
- **Description**: Epic: CLI Fundamentals - Professional Interface & Standards

**Full Description**:
## Summary

Transform Discernus CLI from basic tool to professional research interface with modern standards and documentation.

## Scope: Core Usability & Professional Polish

This epic focuses on essential CLI improvements that researchers expect from modern command-line tools.

## Issues Included

### ✅ Recently Completed
- Current directory defaults (all commands now default to `.`)
- Version flag (`discernus --version`)
- Consistent help text across commands

### 🎯 Phase 1: Professional Interface (High Impact, Low Effort)
- **#203** - Integrate Rich CLI for professional terminal interface
  - Progress bars for long operations
  - Structured tables for experiment listings  
  - Professional error formatting
  - **Effort**: 2-3 hours, **Impact**: High visual improvement

### 🎯 Phase 2: Modern CLI Standards (High Priority)
- **#305** - CLI Enhancement: Missing Standard Conventions
  - Config file support (`.discernus.yaml`)
  - Environment variable support (`DISCERNUS_*`)
  - Global verbose/quiet flags (`-v`, `-q`)
  - Better exit codes (semantic meanings)
  - Shell completion
  - **Effort**: Medium, **Impact**: Core usability

### 🎯 Phase 3: Documentation (Alpha Release Requirement)
- **#156** - Document CLI interface and options
  - Complete command reference
  - Best practices guide
  - Usage examples and patterns
  - **Effort**: Medium, **Impact**: Required for Alpha

## Success Criteria

### Professional Interface
- [ ] Progress bars during experiment execution
- [ ] Structured table display for `discernus list`
- [ ] Enhanced error messages with formatting
- [ ] Zero breaking changes to existing interface

### Modern Standards
- [ ] Config file support working (`.discernus.yaml`)
- [ ] Environment variables working (`DISCERNUS_ANALYSIS_MODEL`)
- [ ] Verbose/quiet flags functional across all commands
- [ ] Shell completion installable and working
- [ ] Semantic exit codes implemented

### Documentation
- [ ] Complete CLI reference documentation
- [ ] Best practices guide for researchers
- [ ] Integration with existing docs structure
- [ ] Usage examples for all commands and options

## Implementation Priority

**Immediate (Next Sprint)**:
1. #203 (Rich CLI) - Quick win, immediate visual impact
2. #305 Phase 1 (Config files) - Highest user value

**Alpha Release**:
3. #156 (Documentation) - Required for release
4. #305 Phase 2 (Shell completion, exit codes) - Polish

## User Impact

**High Impact**: Professional interface creates immediate confidence in the tool
**Core Usability**: Config files eliminate repetitive typing for researchers
**Alpha Readiness**: Documentation enables external researchers to adopt the tool

## Technical Notes

- Rich library integrates cleanly with existing Click framework
- Click supports config files and environment variables natively
- Shell completion requires installation scripts but Click generates them
- All changes maintain backward compatibility

This epic establishes Discernus CLI as a professional research tool that meets modern expectations.

---

### Epic: Three-Track Evidence Architecture for Academic Validation
- **Issue**: #280
- **Labels**: enhancement, epic
- **Assignees**: 
- **Created**: 2025-08-03
- **Updated**: 2025-08-08
- **Milestone**: Alpha Feature Complete
- **Description**: Epic: Three-Track Evidence Architecture for Academic Validation

**Full Description**:
# Epic #280: Three-Track Evidence Architecture - COMPREHENSIVE ROADMAP

## 🚨 CRITICAL STATUS UPDATE

**Current Reality Check**: Evidence infrastructure is 30% implemented with significant architectural gaps identified. Requires systematic completion with clear requirements and milestones.

## 🎯 STRATEGIC OBJECTIVE

Create durable evidence integration infrastructure that scales from 8 to 2000+ documents while maintaining academic integrity and producing reports infused with provenance-linked evidence.

## 📋 EVIDENCE INTEGRATION REQUIREMENTS MATRIX

### **PHASE 1: Foundation Layer (Epic #280 Core)**

#### Evidence Infrastructure Requirements
- **REQ-EI-001**: Accept evidence data from analysis agents in structured JSON format
- **REQ-EI-002**: Maintain complete provenance chain (document_id → dimension → quote_text → confidence → context)
- **REQ-EI-003**: Build txtai semantic search index with metadata filtering capabilities
- **REQ-EI-004**: Support relevance-ranked evidence retrieval with full provenance metadata
- **REQ-EI-005**: Integrate with artifact storage system for reproducible evidence pools

#### Synthesis Agent Integration Requirements  
- **REQ-SA-001**: Detect and utilize available evidence resources automatically
- **REQ-SA-002**: Identify interpretive claims requiring evidence backing vs mathematical facts
- **REQ-SA-003**: Execute strategic evidence queries when making analytical claims
- **REQ-SA-004**: Integrate retrieved evidence naturally into narrative flow (not appendix-style)
- **REQ-SA-005**: Generate proper footnote citations linking to provenance chains

### **PHASE 2: Output Standards (Dependent Issue #281)**

#### Academic Output Requirements
- **REQ-OF-001**: Generate numbered footnotes for all evidence citations [1], [2], etc.
- **REQ-OF-002**: Create "Evidence Provenance" section with complete audit trails  
- **REQ-OF-003**: Format provenance: `[1] steve_king_2017.txt → manipulation dimension → confidence=0.9`
- **REQ-OF-004**: Enable traceability from any claim back to source document
- **REQ-OF-005**: Integrate evidence across scanner/collaborator/transparency sections consistently

### **PHASE 3: Quality & Scale (Dependent Issue #282)**

#### Quality Assurance Requirements
- **REQ-QA-001**: Measure evidence utilization rate (pieces used / pieces available)
- **REQ-QA-002**: Track interpretive claim coverage (claims backed / total claims)  
- **REQ-QA-003**: Ensure no evidence hallucination (only use retrieved evidence)
- **REQ-QA-004**: Validate evidence-claim alignment through confidence scoring

#### Scalability Requirements  
- **REQ-SC-001**: Handle 2000+ documents without synthesis quality degradation
- **REQ-SC-002**: Complete evidence indexing in <5 minutes for large corpora
- **REQ-SC-003**: Execute evidence queries in <2 seconds per query
- **REQ-SC-004**: Maintain synthesis generation time <10 minutes regardless of evidence pool size

## 🗺️ IMPLEMENTATION ROADMAP

### **Milestone 1.1: Evidence Infrastructure Core** *(Current Sprint)*
- [ ] Remove redundant Stage 3 txtai curator (architectural cleanup)
- [ ] Enhance Stage 5 RAG interpreter with evidence awareness protocols (REQ-SA-001, REQ-SA-002)
- [ ] Implement strategic evidence querying in synthesis workflow (REQ-SA-003)
- [ ] Validate evidence integration with 8-document CAF experiment

### **Milestone 1.2: Basic Evidence Integration** *(Next Sprint)*  
- [ ] Implement evidence-infused narrative generation (REQ-SA-004)
- [ ] Create footnote generation system (REQ-OF-001)
- [ ] Build provenance tracking infrastructure (REQ-EI-002, REQ-OF-002)
- [ ] Test with 25-document corpus expansion

### **Milestone 1.3: Production Quality** *(Final Sprint)*
- [ ] Complete multi-audience evidence integration (REQ-OF-005)
- [ ] Implement quality assurance metrics (REQ-QA-001, REQ-QA-002)
- [ ] Validate scalability requirements (REQ-SC-001 through REQ-SC-004)
- [ ] Stress test with 100+ document corpus

## ✅ EPIC SUCCESS CRITERIA

**Epic #280 COMPLETE when ALL criteria met:**

1. ✅ **Evidence Integration**: Simple test experiment generates report with evidence-backed interpretive claims and proper footnotes
2. ✅ **Provenance Integrity**: Complete audit trail from every claim to source document with confidence metadata  
3. ✅ **Quality Score**: Evidence integration quality >80% (coverage + accuracy + relevance)
4. ✅ **Scalability Proof**: System handles 100+ document corpus without quality degradation
5. ✅ **Academic Standards**: No evidence hallucination, proper attribution, reproducible citations

## 🔗 DEPENDENT ISSUES

**Child Issue #281**: Academic Output Standards Implementation  
**Child Issue #282**: Quality Assurance & Scalability Validation  
**Child Issue #283**: Evidence Integration Testing & Validation

## 🚨 CRITICAL PATH DEPENDENCIES

- **Prerequisite**: Framework Migration v7.3 completion (Epic #316)
- **Blocker**: Current architectural confusion between Stage 3 and Stage 5 evidence handling
- **Risk**: Without systematic approach, will continue tactical bug-fixing cycle

## 🧪 VALIDATION EXPERIMENTS

**Test 1**: 8-document CAF experiment (evidence integration proof of concept)  
**Test 2**: 50-document corpus expansion (medium-scale validation)
**Test 3**: 200-document stress test (scalability validation)  
**Test 4**: Cross-framework evidence reuse (durability validation)

---

**Next Action**: Implement Milestone 1.1 with systematic progress tracking and clear success criteria for each requirement.

---
