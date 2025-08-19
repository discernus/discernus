# Discernus v10 Backlog

**Date**: 2025-08-19  
**Status**: Active Development  
**Version**: v10.0

---

## 🚨 Critical Issues (Publication Blocking)

### High Priority - Must Fix Before Release

#### [CRIT-001] Missing Corpus Documents in Results
- **Description**: Corpus documents not included in run results folder
- **Impact**: Researchers cannot access source texts for verification
- **Acceptance Criteria**: All source texts available in `runs/[run_id]/results/`
- **Effort**: Medium
- **Dependencies**: None

#### [CRIT-002] Evidence Database Not Accessible
- **Description**: Evidence database exists in shared_cache but not in results
- **Impact**: Cannot verify specific quotes and evidence cited in final report
- **Acceptance Criteria**: Evidence database accessible in results folder
- **Effort**: Low
- **Dependencies**: CRIT-001

#### [CRIT-003] Source Metadata Missing
- **Description**: No source document metadata (dates, contexts, speaker backgrounds)
- **Impact**: Cannot verify temporal or contextual accuracy of analysis
- **Acceptance Criteria**: Source metadata included in results
- **Effort**: Medium
- **Dependencies**: CRIT-001

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

#### [CRIT-006] Synthesis Agent Framework-Awareness Gap
- **Description**: Synthesis agent ignores sophisticated framework capabilities, producing generic reports despite rich data
- **Impact**: Enhanced frameworks provide no benefit in final reports, wasting analytical sophistication
- **Acceptance Criteria**: Synthesis agent uses framework-specific guidance to leverage enhanced metrics and capabilities
- **Effort**: High
- **Dependencies**: None
- **Observed**: Enhanced CFF v10.0 with salience analysis, tension indices, and cohesion calculations completely ignored in final report
- **Priority**: CRITICAL - Blocks value realization from framework enhancements

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

## 🎯 Sprint Planning

### Sprint 1: Critical Issues (Publication Readiness)
- [ ] CRIT-001: Missing Corpus Documents in Results
- [ ] CRIT-002: Evidence Database Not Accessible
- [ ] CRIT-003: Source Metadata Missing
- [ ] CRIT-004: Quote Verification Impossible

### Sprint 2: Complete Reproducibility
- [ ] CRIT-005: Incomplete Reproducibility
- [ ] TECH-003: Error Handling & Resilience

### Sprint 3: Quality & Validation
- [ ] QUAL-001: Automated Quality Checks
- [ ] QUAL-002: Statistical Validation
- [ ] QUAL-003: Evidence Quality Assessment

### Sprint 4: Technical Improvements
- [ ] TECH-001: Framework Specification Enhancement
- [ ] TECH-002: Model Selection Optimization

---

## 📈 Success Metrics

### Publication Readiness
- [ ] All source texts accessible in results
- [ ] Evidence database fully accessible
- [ ] Complete source metadata available
- [ ] All quotes verifiable
- [ ] End-to-end reproducibility achieved

### Quality Standards
- [ ] Automated quality validation implemented
- [ ] Statistical validation automated
- [ ] Evidence quality assessment functional

### Performance Targets
- [ ] Support for 100+ document corpora
- [ ] Intelligent caching implemented
- [ ] Parallel processing where applicable

---

## 🔄 Backlog Maintenance

- **Review Frequency**: Weekly
- **Priority Updates**: As issues are resolved
- **New Items**: Add as discovered during development
- **Completion Criteria**: All acceptance criteria met and tested
