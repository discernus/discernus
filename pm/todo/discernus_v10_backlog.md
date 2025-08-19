# Discernus v10 Backlog

**Date**: 2025-01-19  
**Status**: Major Breakthrough - Enhanced Synthesis Operational  
**Version**: v10.0

## 🏆 Major Achievements Summary

**BREAKTHROUGH**: Enhanced Framework-Agnostic Synthesis Agent (CRIT-006) now operational and producing **academic-quality reports** with 2x+ word count and 3x+ analytical sophistication.

**KEY MILESTONES COMPLETED**:
- ✅ **Enhanced Synthesis**: Multi-level analytical architecture with literature integration
- ✅ **Infrastructure Cleanup**: Clean, framework-agnostic pipeline with deprecated contamination  
- ✅ **Framework Enhancement**: CFF v10.0 with 18 derived metrics and academic depth
- ✅ **Hybrid Design Foundation**: Minimal experiments → comprehensive analysis capability proven

**CURRENT CAPABILITY**: 7-line experiment specification → 3,000-word academic analysis with statistical tables, literature review, and evidence integration.

---

## 🚨 Critical Issues (Publication Blocking)

### Immediate Priority - Platform Robustness

**STATUS UPDATE**: Major breakthrough achieved! CRIT-006 Enhanced Synthesis Agent operational and producing academic-quality reports (2,850-3,060 words vs. previous ~1,500 words). CRIT-007 Infrastructure cleanup completed. Core pipeline now clean and framework-agnostic.

**COMPLETED CRITICAL ITEMS**: CRIT-006 ✅, CRIT-007 ✅, CRIT-008 ✅, CRIT-009 ✅, CRIT-001 ✅, CRIT-002 ✅, CRIT-003 ✅

#### [CRIT-008] Robust Path Resolution and Validation ✅ COMPLETED
- **Description**: ✅ COMPLETED - Fixed "works on my machine" problems with robust filename matching
- **Impact**: ✅ RESOLVED - Experiments now work reliably regardless of filename variations from git merges
- **Critical Issues**: ✅ ALL RESOLVED
  - Fuzzy filename matching implemented (ignores hash suffixes automatically)
  - Corpus file existence validation added before experiment execution
  - Enhanced validation integration with clear logging
  - Supports exact, fuzzy, and extension-flexible matching
- **Results Achieved**:
  - Fuzzy matching: `john_mccain_2008_concession.txt` → `john_mccain_2008_concession_ff9b26f2.txt`
  - Early validation: "STATUS: Corpus files validated" before analysis
  - 4/4 documents processed successfully (vs. 0/4 in broken state)
  - Git merge compatibility restored
- **Status**: ✅ COMPLETED - Robust path resolution operational and tested

#### [CRIT-009] Appropriate Reliability Metrics for Oppositional Frameworks ✅ COMPLETED
- **Description**: ✅ COMPLETED - Replaced Cronbach's Alpha with methodologically sound oppositional construct validation for frameworks with opposing dimensions
- **Impact**: ✅ RESOLVED - System now uses LLM-driven framework classification to apply appropriate validation methods
- **Critical Issues**: ✅ ALL RESOLVED
  - Cronbach's Alpha automatically skipped for oppositional frameworks like CFF
  - Oppositional construct validation implemented (negative correlation checks, discriminant validity)
  - Enhanced synthesis prompt updated to interpret oppositional validation correctly
  - Statistical formatter handles both traditional reliability and oppositional validation
- **Implementation Approach**: 
  - THIN architecture using LLM-driven framework classification instead of hardcoded detection
  - Single prompt determines if framework measures opposing or unidimensional constructs
  - Automatic selection of appropriate validation methodology
- **Results Achieved**:
  - CFF v10.0 correctly classified as oppositional framework
  - Cronbach's Alpha eliminated for opposing constructs
  - Oppositional validation tables generated instead
  - Framework-agnostic approach works with any framework structure
- **Status**: ✅ COMPLETED - Methodologically appropriate metrics implemented with THIN architecture

### Publication Readiness - Source Access

#### [CRIT-001] Missing Corpus Documents in Results ✅ COMPLETED
- **Description**: ✅ COMPLETED - Corpus documents now automatically copied to run results folder
- **Impact**: ✅ RESOLVED - Researchers can access source texts for verification in `runs/[run_id]/results/corpus/`
- **Implementation Details**:
  - Added `_copy_corpus_documents_to_results()` method to ExperimentOrchestrator
  - Creates `results/corpus/` directory with all source documents
  - Handles hash-suffixed filenames with fuzzy matching
  - Copies corpus manifest for metadata reference
  - Graceful error handling - doesn't fail experiment if corpus copying fails
- **Results Achieved**:
  - All 4 corpus documents copied successfully in test
  - Corpus manifest (corpus.md) copied for reference
  - Source documents accessible with original manifest filenames
  - Enables full quote verification and replication
- **Status**: ✅ COMPLETED - Source texts now accessible in results for verification

#### [CRIT-002] Evidence Database Not Accessible ✅ COMPLETED
- **Description**: ✅ COMPLETED - Evidence database now automatically aggregated and copied to results folder
- **Impact**: ✅ RESOLVED - Researchers can verify specific quotes and evidence cited in final report via `runs/[run_id]/results/evidence/`
- **Implementation Details**:
  - Added `_copy_evidence_database_to_results()` method to ExperimentOrchestrator
  - Aggregates all evidence artifacts from shared_cache into comprehensive database
  - Creates `results/evidence/` directory with consolidated evidence files
  - Generates both JSON and CSV formats for different analysis needs
  - Includes metadata about extraction methods, documents analyzed, and collection timing
- **Results Achieved**:
  - 446 evidence pieces aggregated from 40 files in test
  - Evidence database JSON with complete metadata and provenance
  - Evidence database CSV for easy analysis (446 rows)
  - All quotes traceable to specific documents and dimensions
  - Full quote verification now possible for peer review
- **Status**: ✅ COMPLETED - Evidence database accessible in results for quote verification

#### [CRIT-003] Source Metadata Missing ✅ COMPLETED
- **Description**: ✅ COMPLETED - Source document metadata now automatically extracted and copied to results folder
- **Impact**: ✅ RESOLVED - Researchers can verify temporal and contextual accuracy of analysis via `runs/[run_id]/results/metadata/`
- **Implementation Details**:
  - Added `_copy_source_metadata_to_results()` method to ExperimentOrchestrator
  - Extracts all metadata from corpus manifest (speaker, year, party, style, etc.)
  - Creates `results/metadata/` directory with comprehensive metadata files
  - Generates both JSON and CSV formats for different analysis needs
  - Includes summary statistics about corpus composition and metadata fields
  - Copies original corpus manifest for reference
- **Results Achieved**:
  - 4 documents with complete metadata extracted in test
  - Metadata fields: speaker, year, party, style
  - Speakers: Alexandria Ocasio-Cortez, Bernie Sanders, John McCain, Steve King
  - Years: 2008, 2017, 2025 (temporal span coverage)
  - Parties: Democratic, Independent, Republican (political diversity)
  - Full contextual verification now possible for peer review
- **Status**: ✅ COMPLETED - Source metadata accessible in results for temporal and contextual verification

#### [CRIT-004] Quote Verification Impossible
- **Description**: Final report references evidence but source texts unavailable
- **Impact**: Reviewers cannot verify quoted evidence is real
- **Acceptance Criteria**: All quotes traceable to source texts
- **Effort**: Low
- **Dependencies**: CRIT-001, CRIT-002

#### [CRIT-005] Incomplete Reproducibility
- **Description**: Mathematical calculations reproducible, textual analysis not
- **Impact**: Other researchers cannot replicate text analysis
- **Acceptance Criteria**: Complete end-to-end reproducibility including source access
- **Effort**: High
- **Dependencies**: CRIT-001, CRIT-002, CRIT-003

---

## 🔧 Technical Debt & Improvements

### Medium Priority - Should Fix Soon

#### [TECH-001] Framework Specification Enhancement
- **Description**: Framework specification enhanced with LLM optimization, sequential analysis, and comprehensive guidance
- **Impact**: Significantly improved framework quality and LLM reliability
- **Acceptance Criteria**: ✅ COMPLETED - Enhanced specification with prompting strategies, academic depth, and clear guidance
- **Effort**: High
- **Dependencies**: None
- **Status**: ✅ COMPLETED

#### [TECH-004] Framework Library Compliance Update
- **Description**: All existing frameworks need updating to comply with enhanced v10.0 specification
- **Impact**: Inconsistent framework quality across the platform, reduced LLM reliability for non-compliant frameworks
- **Acceptance Criteria**: All frameworks in reference library updated with LLM optimization features (examples, anti-examples, scoring calibration, sequential variants)
- **Effort**: High
- **Dependencies**: TECH-001 (completed)
- **Affected Frameworks**: PDAF, other reference frameworks, seed frameworks
- **Priority**: High - Required for platform consistency

#### [TECH-002] Model Selection Optimization
- **Description**: Currently hardcoded to Pro model for all operations
- **Impact**: May not be cost-optimal for all use cases
- **Acceptance Criteria**: Configurable model selection based on task requirements
- **Effort**: Medium
- **Dependencies**: None

#### [TECH-003] Error Handling & Resilience
- **Description**: Limited error handling for LLM failures
- **Impact**: Pipeline may fail silently or produce incomplete results
- **Acceptance Criteria**: Comprehensive error handling with graceful degradation
- **Effort**: Medium
- **Dependencies**: None

#### [TECH-005] Complex Framework Performance Optimization
- **Description**: Enhanced frameworks with 18 derived metrics cause significant processing delays
- **Impact**: Long experiment runtimes may affect user experience and research velocity
- **Acceptance Criteria**: Optimize derived metrics generation for complex frameworks
- **Effort**: Medium
- **Dependencies**: None
- **Observed**: Enhanced CFF v10.0 with 18 metrics vs. previous 6 metrics shows processing delays

#### [TECH-006] Enhanced Experiment Provenance Metadata
- **Description**: Add comprehensive model and system information to experiment metadata for full reproducibility
- **Impact**: Current reports lack essential provenance data (analysis model, synthesis model, framework version, git commit) making full replication difficult
- **Acceptance Criteria**:
  - Capture analysis model used (e.g., "vertex_ai/gemini-2.5-flash")
  - Capture synthesis model used (e.g., "vertex_ai/gemini-2.5-pro") 
  - Extract framework name and version from framework content
  - Include git commit hash for repository state
  - Add system information (Python version, key dependencies)
  - Update experiment_summary.json and complete_research_data.json schemas
- **Effort**: Medium
- **Dependencies**: None
- **Priority**: MEDIUM - Improves academic reproducibility and research integrity

#### [ARCH-001] Multi-Agent Progressive Synthesis Architecture (Phase 2)
- **Description**: Implement 4-stage multi-agent synthesis pipeline for comprehensive discovery capabilities beyond single-agent limitations
- **Impact**: Enables full hybrid experimental design paradigm with systematic pattern discovery, computational analysis, and cross-validation
- **Acceptance Criteria**: 
  - Stage 1: Parallel specialized agents (Statistical Enhancement, Evidence Analysis, Pattern Recognition)
  - Stage 2: Sequential advanced synthesis (Cross-Dimensional Network Analysis, Anomaly Detection, Archetype Validation)
  - Stage 3: Integration agents (Insight Synthesis, Methodological Assessment)
  - Stage 4: Communication agents (Academic Report Generation, Executive Intelligence)
  - Computational service integration for mathematical operations with full provenance
  - Multi-agent cross-validation and uncertainty quantification
- **Effort**: Very High
- **Dependencies**: CRIT-006 (Enhanced Single-Agent Synthesis)
- **Capabilities**: Advanced mathematical operations, systematic evidence validation, multi-perspective analysis
- **Expected Outcome**: Claude-level analytical sophistication through systematic agent collaboration
- **Priority**: HIGH - Enables complete hybrid experimental design vision
- **Implementation Strategy**: Progressive enhancement building on Phase 1 single-agent foundation

#### [CRIT-009] Appropriate Reliability Metrics for Oppositional Frameworks
- **Description**: Replace Cronbach's Alpha with methodologically sound alternatives for frameworks that intentionally measure opposing constructs
- **Impact**: Current Cronbach's Alpha calculations are misleading for oppositional frameworks like CFF; negative alphas are expected and validate design rather than indicating failure
- **Critical Issues**:
  - Cronbach's Alpha assumes unidimensional constructs but CFF measures oppositional pairs
  - Negative alphas are incorrectly interpreted as reliability failures
  - Traditional psychometric reliability metrics don't apply to oppositional construct frameworks
  - Creates confusing "fancy metrics with no real relevance" in current reports
- **Acceptance Criteria**:
  - Remove Cronbach's Alpha from current statistical analysis pipeline
  - Implement oppositional construct validation (negative correlation checks)
  - Add test-retest reliability for measurement stability
  - Add discriminant validity tests (opposing archetypes should differ significantly)
  - Add convergent validity tests (similar archetypes should cluster)
  - Reserve Cronbach's Alpha for ensemble inter-model reliability testing only
- **Effort**: Medium
- **Dependencies**: None
- **Priority**: CRITICAL - Eliminates methodologically inappropriate metrics
- **Observed**: Enhanced synthesis correctly interprets negative alphas as validation, but metric shouldn't be calculated for oppositional constructs

#### [CRIT-008] Robust Path Resolution and Validation
- **Description**: Fix "works on my machine" problems caused by brittle filename matching between corpus manifests and actual files
- **Impact**: Experiments fail when corpus files have different names than manifest expects; git merges break existing experiments
- **Critical Issues**:
  - Corpus manifest expects exact filenames but git brings hash-suffixed files
  - No validation that corpus files actually exist before running
  - Absolute path dependencies create portability problems
  - Validation system doesn't catch manifest-file mismatches
- **Acceptance Criteria**:
  - Implement fuzzy filename matching (ignore hash suffixes)
  - Add corpus file existence validation before experiment execution
  - Enhance experiment coherence validation to catch path issues
  - Support both exact and approximate filename matching
- **Effort**: Medium
- **Dependencies**: None
- **Priority**: CRITICAL - Prevents "works on my machine" failures
- **Observed**: simple_test broke after git merge due to filename suffix mismatches

#### [CRIT-007] Infrastructure Cruft Cleanup and Deprecation ✅ COMPLETED
- **Description**: ✅ COMPLETED - Surgical cleanup of contaminated/unused components
- **Impact**: ✅ RESOLVED - Clean infrastructure with single active orchestrator, framework agnosticism restored
- **Critical Issues**: ✅ ALL RESOLVED
  - notebook_generator_agent: Deprecated (moved to deprecated/)
  - automated_derived_metrics: Validated as clean and framework-agnostic
  - csv_export_agent: Fixed simple_test path hardcoding
  - Multiple orchestrators: ThinOrchestrator and V8Orchestrator deprecated
- **Results Achieved**:
  - Single active orchestrator (ExperimentOrchestrator) with clean architecture
  - 13 active agents identified and validated
  - 8 contaminated/unused components deprecated
  - Framework and experiment agnosticism restored
  - Reference patterns preserved for future multi-agent architecture
- **Status**: ✅ COMPLETED - Clean foundation established

#### [CRIT-006] Enhanced Framework-Agnostic Synthesis Agent (Phase 1) ✅ COMPLETED
- **Description**: ✅ COMPLETED - Enhanced synthesis agent with comprehensive analytical architecture while preserving framework agnosticism
- **Impact**: ✅ RESOLVED - Enhanced frameworks now provide significant benefit; reports have academic depth and multi-level insights
- **Acceptance Criteria**: ✅ ALL MET
  - Framework-agnostic synthesis prompt working with any compliant framework ✅
  - Multi-level analytical architecture (5 levels: Basic → Advanced → Cross-dimensional → Temporal → Meta-analysis) ✅
  - Comprehensive statistical utilization with confidence analysis, tension patterns, derived metrics ✅
  - Enhanced evidence integration with systematic quote validation ✅
  - Academic-quality output approaching iterative human-AI collaboration results ✅
  - Integration with existing single-agent pipeline architecture ✅
- **Results Achieved**: 
  - 2,850-3,060 word comprehensive reports (vs. ~1,500 word originals)
  - Academic structure with literature review, statistical tables, evidence integration
  - Multi-level analytical progression implemented
  - Framework agnosticism preserved and validated
- **Status**: ✅ COMPLETED - Enhanced synthesis agent operational and producing academic-quality reports

---

## 📊 Quality & Validation

### Medium Priority - Should Implement

#### [QUAL-001] Automated Quality Checks
- **Description**: No automated validation of output quality
- **Impact**: May produce low-quality results without detection
- **Acceptance Criteria**: Automated quality validation at each pipeline stage
- **Effort**: High
- **Dependencies**: TECH-003

#### [QUAL-002] Statistical Validation
- **Description**: Limited validation of statistical analysis results
- **Impact**: May produce statistically invalid conclusions
- **Acceptance Criteria**: Automated statistical validation and sanity checks
- **Effort**: Medium
- **Dependencies**: TECH-003

#### [QUAL-003] Evidence Quality Assessment
- **Description**: No assessment of evidence quality or relevance
- **Impact**: May cite weak or irrelevant evidence
- **Acceptance Criteria**: Evidence quality scoring and filtering
- **Effort**: High
- **Dependencies**: CRIT-002

---

## 🚀 Performance & Scalability

### Low Priority - Nice to Have

#### [PERF-001] Large Corpus Optimization
- **Description**: Current pipeline designed for small corpora (4-20 documents)
- **Impact**: May not scale to research-grade corpora (1000+ documents)
- **Acceptance Criteria**: Efficient processing of large corpora
- **Effort**: High
- **Dependencies**: TECH-003, QUAL-001

#### [PERF-002] Caching Strategy
- **Description**: Basic caching may not be optimal for repeated analysis
- **Impact**: Unnecessary recomputation of similar analyses
- **Acceptance Criteria**: Intelligent caching strategy for analysis results
- **Effort**: Medium
- **Dependencies**: None

#### [PERF-003] Parallel Processing
- **Description**: Sequential processing of documents
- **Impact**: Slow processing for large corpora
- **Acceptance Criteria**: Parallel document processing where possible
- **Effort**: High
- **Dependencies**: TECH-003

---

## 📚 Documentation & User Experience

### Low Priority - Nice to Have

#### [DOC-001] User Guide
- **Description**: Limited documentation for researchers
- **Impact**: Researchers may struggle to use the platform effectively
- **Acceptance Criteria**: Comprehensive user guide with examples
- **Effort**: Medium
- **Dependencies**: None

#### [DOC-002] API Documentation
- **Description**: No API documentation for programmatic access
- **Impact**: Developers cannot integrate with the platform
- **Acceptance Criteria**: Complete API documentation with examples
- **Effort**: High
- **Dependencies**: None

#### [DOC-003] Best Practices Guide
- **Description**: No guidance on best practices for research design
- **Impact**: Researchers may design suboptimal experiments
- **Acceptance Criteria**: Best practices guide for research design
- **Effort**: Medium
- **Dependencies**: DOC-001

---

## 🎯 Updated Sprint Planning (Post-CRIT-006/007 Success)

### Sprint 1: Platform Robustness ✅ COMPLETED
- [x] CRIT-008: Robust Path Resolution and Validation ✅
- [x] CRIT-009: Appropriate Reliability Metrics ✅
- [ ] TECH-003: Error Handling & Resilience

### Sprint 2: Publication Readiness (Source Access) - 75% COMPLETE
- [x] CRIT-001: Missing Corpus Documents in Results ✅
- [x] CRIT-002: Evidence Database Not Accessible ✅  
- [x] CRIT-003: Source Metadata Missing ✅
- [ ] CRIT-004: Quote Verification Impossible

### Sprint 3: Complete Reproducibility
- [ ] CRIT-005: Incomplete Reproducibility
- [ ] QUAL-002: Statistical Validation

### Sprint 4: Advanced Architecture (Future)
- [ ] ARCH-001: Multi-Agent Progressive Synthesis Architecture (Phase 2)
- [ ] TECH-002: Model Selection Optimization
- [ ] QUAL-001: Automated Quality Checks

### Completed Major Milestones ✅
- [x] CRIT-006: Enhanced Framework-Agnostic Synthesis Agent ✅
- [x] CRIT-007: Infrastructure Cruft Cleanup ✅
- [x] CRIT-008: Robust Path Resolution and Validation ✅  
- [x] TECH-001: Framework Specification Enhancement ✅

---

## 📈 Success Metrics

### Enhanced Synthesis Achievement ✅
- [x] **Academic-quality reports**: 2,850-3,060 words vs. previous ~1,500 words ✅
- [x] **Multi-level analysis**: 5-level analytical architecture implemented ✅
- [x] **Literature integration**: Proper academic citations and theoretical grounding ✅
- [x] **Statistical sophistication**: Correlation analysis, significance testing, effect sizes ✅
- [x] **Evidence integration**: Systematic quote attribution with source identification ✅
- [x] **Framework agnosticism**: Works with any compliant framework ✅

### Infrastructure Robustness ✅
- [x] **Clean architecture**: Single active orchestrator, deprecated contaminated components ✅
- [x] **Framework agnosticism**: No CFF-specific hardcoding in active pipeline ✅
- [x] **Experiment agnosticism**: No simple_test dependencies in active components ✅
- [x] **13 active agents**: Clear component inventory and responsibilities ✅

### Publication Readiness (In Progress)
- [ ] All source texts accessible in results
- [ ] Evidence database fully accessible
- [ ] Complete source metadata available
- [ ] All quotes verifiable
- [ ] End-to-end reproducibility achieved

### Platform Reliability ✅
- [x] **Robust path resolution**: Fuzzy filename matching with hash suffix tolerance ✅
- [ ] Appropriate reliability metrics for oppositional frameworks  
- [ ] Comprehensive error handling and resilience

---

## 🔄 Backlog Maintenance

- **Review Frequency**: Weekly
- **Priority Updates**: As issues are resolved
- **New Items**: Add as discovered during development
- **Completion Criteria**: All acceptance criteria met and tested
