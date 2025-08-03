# Issue Triage Analysis & Migration Plan
*Comprehensive review of 88 open issues across 8 milestones*

## Triage Summary

**Total Issues Analyzed**: 88 issues across 8 milestones
**Migration Strategy**: Consolidate to 2 active milestones + 1 research milestone

### **Alpha v1.0: Gasket Architecture** *(25 issues)*

#### **CRITICAL → Alpha Foundation (Immediate)**
- **#258**: PDAF Framework: PSCI Calculation Dependency Error *(blocks framework testing)*
- **#257**: PDAF Framework: Missing Temporal Column Extraction *(blocks framework testing)*
- **#256**: PDAF Framework: Categorical Column Naming Mismatch *(blocks framework testing)*

#### **IMPORTANT → Alpha Comprehensive**
- **#273**: Enforce Manifest-Directory Consistency in Corpus Validation
- **#259**: EPIC: Gasket Architecture Implementation *(consolidate with existing work)*
- **#191**: EPIC: Researcher User Experience & Workflow Optimization
- **#184**: Comprehensive Codebase Architecture Compliance Audit
- **#183**: Update Architecture Specification with THIN Best Practices

#### **SECURITY CRITICAL → Alpha Foundation**
- **#137**: SECURITY: Implement ProjectSecurityBoundary core infrastructure *(marked Ready)*

#### **SECURITY IMPORTANT → Alpha Comprehensive**
- **#190**: EPIC: Security & Compliance Audit *(already updated with provenance scenarios)*
- **#144**: EPIC: Workflow Security Architecture Implementation
- **#142**: SECURITY: Migrate remaining file-accessing agents to SecureAgent
- **#141**: SECURITY: Comprehensive security testing framework
- **#140**: SECURITY: Migrate AnalysisAgent to SecureAgent architecture
- **#139**: SECURITY: Add CLI-level security validation for experiment files
- **#138**: SECURITY: Create SecureAgent base class for agent boundary enforcement
- **#143**: SECURITY: Runtime security monitoring and alerting

#### **DEFER → Research & Future Work**
- **#189**: EPIC: Release Engineering & Deployment Pipeline
- **#182**: EPIC: Architecture Compliance Review and Validation
- **#156**: Document CLI interface and options
- **#147**: Add comprehensive cost tracking and reporting
- **#58**: Prepare project for public open source release
- **#57**: Establish contributor guidelines and IP policy
- **#54**: Research and select appropriate open source license
- **#53**: Open Source Licensing Epic

---

### **Alpha v1.1: Performance & UX** *(21 issues)*

#### **CRITICAL → Alpha Foundation**
- **#291**: Default Ensemble Validation: Empirical Model Selection Strategy *(performance blocker)*

#### **IMPORTANT → Alpha Comprehensive**
- **#253**: THICK Violation: ResultsInterpreter Over-Parses LLM Reports *(architecture quality)*
- **#252**: THICK Violation: Evidence Curator Parses LLM Intelligence *(architecture quality)*
- **#251**: Enhancement: Add LLM Response Caching to Synthesis Pipeline
- **#250**: Production Pipeline Parameter Audit
- **#249**: Create Unified Results Dashboard for Researcher-Centric Information Architecture
- **#236**: Update specifications to prevent leading-the-witness bias
- **#194**: EPIC: Developer Velocity & Debugging Infrastructure
- **#198**: Implement smart mock detection for LLM calls
- **#197**: Add context window early warning system
- **#196**: Implement real-time progress streaming for pipeline visibility

#### **DEFER → Research & Future Work**
- **#201**: EPIC: Industry Standard Component Integration (THIN-Compliant)
- **#206**: Integrate httpx for modern HTTP client capabilities
- **#205**: Integrate RQ (Redis Queue) for simplified task orchestration
- **#204**: Integrate Structlog for THIN-compliant structured logging
- **#203**: Integrate Rich CLI for professional terminal interface
- **#202**: Integrate Pydantic Settings for THIN-compliant configuration management
- **#185**: Engage External Architecture Reviewers
- **#127**: Review and enhance MVP testing strategy before release
- **#56**: Create LICENSE file and implement across project
- **#55**: Audit dependencies for license compatibility

---

### **Alpha v1.2: Integration & Testing** *(6 issues)*

#### **IMPORTANT → Alpha Comprehensive**
- **#212**: Create comprehensive features inventory and documentation for alpha release
- **#188**: EPIC: Quality Assurance & Testing Framework
- **#173**: Phase 3: Quality Validation and Comparative Evaluation
- **#172**: Phase 2: Framework Generalizability Testing

#### **DEFER → Research & Future Work**
- **#148**: Analysis of missing documents and error patterns in large batch test
- **#145**: Experiment failed due to out-of-memory error processing large LLM response

---

### **Alpha v1.3: Academic Foundation & Release Readiness** *(10 issues)*

#### **ALL → Alpha Comprehensive** *(Perfect Fit)*
- **#292**: EPIC: Research Integrity & Provenance Architecture Enhancement *(already moved)*
- **#284**: Sprint 6.4: Implement Score Validation Pipeline
- **#283**: Sprint 6.3: Improve Evidence Confidence Calibration
- **#282**: Sprint 6.2: Implement Automatic Grounding Evidence Generation
- **#281**: Sprint 6.1: Enhance Analysis Prompts for Score-Evidence Linking
- **#280**: Epic: Three-Track Evidence Architecture for Academic Validation
- **#278**: CLI Enhancement: Command Chaining and User Experience Improvements
- **#277**: Design and Implement Experiment Specification v7.1 with Root-Level Corpus Manifest
- **#62**: Create comprehensive security and privacy policy
- **#61**: Implement comprehensive code quality automation

## Migration Execution Plan

### **Phase 1: Critical Issues → Alpha Foundation** *(4 issues)*
```bash
# Framework blockers
gh issue edit 258 --milestone "Alpha Foundation (Immediate)"
gh issue edit 257 --milestone "Alpha Foundation (Immediate)" 
gh issue edit 256 --milestone "Alpha Foundation (Immediate)"

# Security critical
gh issue edit 137 --milestone "Alpha Foundation (Immediate)"

# Performance blocker  
gh issue edit 291 --milestone "Alpha Foundation (Immediate)"
```

### **Phase 2: Important Issues → Alpha Comprehensive** *(33 issues)*
```bash
# Gasket Architecture & UX
gh issue edit 273 --milestone "Alpha Comprehensive (Academic Gold Standard)"
gh issue edit 259 --milestone "Alpha Comprehensive (Academic Gold Standard)"
gh issue edit 191 --milestone "Alpha Comprehensive (Academic Gold Standard)"
# ... [continue for all 33 important issues]
```

### **Phase 3: Research Issues → Future Work** *(18 issues)*
```bash
# Defer to post-alpha
gh issue edit 189 --milestone "Research & Future Work"
gh issue edit 182 --milestone "Research & Future Work"
# ... [continue for all 18 research issues]
```

### **Phase 4: Close Deprecated Milestones**
```bash
# Close old milestone structure
gh api repos/discernus/discernus/milestones/4 --method PATCH --field state=closed
gh api repos/discernus/discernus/milestones/5 --method PATCH --field state=closed
gh api repos/discernus/discernus/milestones/6 --method PATCH --field state=closed
gh api repos/discernus/discernus/milestones/9 --method PATCH --field state=closed
gh api repos/discernus/discernus/milestones/8 --method PATCH --field state=closed
```

## Final Milestone Distribution

### **Alpha Foundation (Immediate)** - *9 issues*
- 4 existing provenance fixes (#293-296)
- 3 framework blockers (#256-258)
- 1 security critical (#137)
- 1 performance blocker (#291)

### **Alpha Comprehensive (Academic Gold Standard)** - *40 issues*
- 7 existing quality improvements (#297-302, #285)
- 33 migrated important issues
- Focus: Academic collaboration readiness

### **Research & Future Work** - *28 issues*
- 10 existing research issues
- 18 migrated future work issues
- Focus: Post-alpha enhancements

### **CLOSED/DEPRECATED** - *11 issues*
- Issues that are obsolete or superseded
- Old milestone structure artifacts

## Quality Gates

### **Migration Success Criteria**
- [ ] All 88 issues reviewed and categorized
- [ ] Critical path issues (9) in Alpha Foundation
- [ ] Academic quality issues (40) in Alpha Comprehensive  
- [ ] Future work (28) properly deferred
- [ ] Old milestones (5) closed and archived
- [ ] No orphaned or miscategorized issues

### **Development Readiness**
- [ ] Clear priority sequence established
- [ ] Blocking dependencies resolved
- [ ] Academic focus maintained throughout
- [ ] Provenance crisis issues ready for immediate execution

---

**Next Action**: Execute Phase 1 migration of critical issues to Alpha Foundation milestone.