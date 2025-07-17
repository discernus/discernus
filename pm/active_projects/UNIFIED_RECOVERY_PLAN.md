# Discernus Recovery & Unification Plan
**Based on Comprehensive Gap Analysis Synthesis**

## Executive Summary

The gap analyses reveal a project with **proven capabilities that have been lost through architectural regression**. This is not a greenfield development challenge but an **archaeological recovery mission** to restore sophisticated multi-agent workflows on a modern THIN foundation.

**Core Finding**: The system once produced publication-quality academic reports with adversarial review, data visualization, and complex statistical modeling. These capabilities were deliberately removed during a "THIN reformation" that solved reliability issues but threw away the orchestration engine.

**Strategic Approach**: Phased recovery using historical artifacts as immutable benchmarks, following a disciplined "golden set" methodology to prevent future regressions.

---

## Phase 0: Establish Ground Truth (Week 1)
*Foundation: Create immutable quality benchmarks*

### 0.1 Golden Set Creation
**Objective**: Establish immutable benchmarks that define "success" for all future development

**Actions**:
- Create `/golden_set` directory structure
- Archive the **MLK vs. Malcolm X analysis** as the qualitative target (sophistication, depth, framework adherence)
- Archive the **Trump study comprehensive report** as the capability target (data ingestion, visualization, multi-format output)
- Document the **vanderveen ThinOrchestrator pattern** as the architectural template
- Archive the **SOAR conversation logs** as the multi-agent workflow template

**Success Criteria**: Every future development decision evaluated against: "Does this move us closer to automatically generating golden set quality?"

---

## Phase 1: Core Engine Recovery (Weeks 2-4)
*Foundation: Fix existing EnsembleOrchestrator and project-based workflow*

**STATUS: ⏳ IN PROGRESS**

This phase is underway. The core architectural refactoring is feature-complete,
but end-to-end validation is pending the completion of the agent refactoring in section 1.2.

### CRITICAL DISCOVERY: ThinOrchestrator Was Deprecated (January 12, 2025)

**STATUS FOR NEXT AGENT**: The original plan assumed ThinOrchestrator needed to be recovered. Investigation revealed it was deprecated because it violated THIN principles. The current EnsembleOrchestrator is the correct THIN approach. Focus on fixing CLI to use existing EnsembleOrchestrator and project-based workflow instead of recreating deprecated components.

**Investigation revealed the ThinOrchestrator was deprecated because it violated THIN principles:**
- **Framework Context Loss**: Framework specifications weren't reaching analysis agents properly
- **LLM Confusion**: Moderator LLMs generated unrelated content instead of following research questions  
- **Over-Complex Architecture**: Too much conversation management logic (996 lines)
- **Unreliable Results**: Multiple test runs failed to produce meaningful analysis

**The EnsembleOrchestrator is the correct THIN approach that replaced it** with simple linear pipeline:
1. ValidationAgent.validate_and_execute_sync() ✅ working
2. EnsembleOrchestrator - spawns analysis agents 
3. SynthesisAgent - aggregates results
4. ModeratorAgent - orchestrates outlier discussions only
5. RefereeAgent - arbitrates disagreements  
6. FinalSynthesisAgent - packages results

### 1.1 Critical Infrastructure Fixes & Architectural Canonization

**STATUS: ⏳ Pending Final Validation**

**Completed Tasks (Feature-Complete):**
1.  **Established Project-Based Workflow**: Canonized the "Project" as the core unit of work. The CLI now accepts a single project path and correctly orchestrates the validation and execution based on the `framework.md`, `experiment.md`, and `corpus/` contained within.
2.  **Created the `ProjectCoherenceAnalyst`**: Replaced the legacy `ValidationAgent` with a new, intelligent agent that performs a holistic analysis of a project's methodological soundness, including model health checks and corpus validation.
3.  **Implemented the "Immutable Session Package"**: The `EnsembleOrchestrator` now creates a complete, self-contained snapshot of all project assets (`framework.md`, `experiment.md`, `corpus/`) for every run, ensuring perfect reproducibility.
4.  **Instituted Asset Fingerprinting**: The `ProjectChronolog` now records the SHA-256 hash of all project assets at the start of each session, creating an unbreakable "barcode" that links the logs to the exact data used.
5.  **Ensured Full Transparency**: The system now logs the specific LLM model used for every conversational turn and centralizes all provider-specific parameter logic in `models.yaml`.
6.  **Delivered Tidy Data**: A new `DataExtractionAgent` automatically parses the conversation logs to produce a clean, analysis-ready `results.csv` file for every run.

### 1.2 Agent Architecture Refactoring

**STATUS: ✅ COMPLETE**

**Completed Tasks:**
1.  **Created `TrueValidationAgent`**: A new, specialized agent now performs deep, rubric-based methodological validation of the `framework.md` and `experiment.md` files.
2.  **Integrated `ExecutionPlannerAgent`**: The existing `ExecutionPlannerAgent` is now correctly integrated into the validation workflow, responsible for generating a detailed, machine-readable run plan.
3.  **Refactored `ProjectCoherenceAnalyst`**: This agent now acts as a meta-orchestrator for the pre-execution phase, first calling the `TrueValidationAgent` for methodological validation and then, upon success, calling the `ExecutionPlannerAgent` for technical planning.
4.  **Updated Agent Registry**: The new `TrueValidationAgent` is fully registered and discoverable.

---

## Phase 2: Capability Recovery (Weeks 5-8)
*Foundation: Restore sophisticated multi-agent workflows*

**Status: ✅ Partially Complete** - The core sequential academic workflow has been successfully restored and implemented in the `WorkflowOrchestrator`, fulfilling a major objective of this phase. The remaining tasks involve more advanced, non-linear conversational patterns.

### 2.1 Multi-Agent Conversation Protocols

**Priority Tasks**:
1. **Implement agent-to-agent communication** protocols from SOAR conversation logs
2. **Restore moderator/referee/arbitration system** for outlier detection and resolution
3. **Implement final synthesis agent** for publication-ready reports with methodology sections
4. **Add state management** for multi-turn conversations and context accumulation

### 2.2 Advanced Orchestration Recovery

**Priority Tasks**:
1. **Support dynamic workflow sequences** (Analysis → Stats → Interpretation → Review → Synthesis)
2. **Implement review-and-revise loops** with feedback incorporation
3. **Restore real-time Redis event streaming** for comprehensive provenance
4. **Validate recovered workflows** against historical SOAR conversation logs

---

## Phase 3: Data & Statistical Infrastructure (Weeks 9-11)
*Foundation: Restore data ingestion and mathematical reliability*

### 3.1 Data Ingestion Recovery

**Priority Tasks**:
1. **Restore PDF text extraction** capability from Trump study evidence
2. **Restore DOCX text extraction** capability from Trump study evidence
3. **Create robust corpus versioning** and management system
4. **Validate data ingestion** against Trump study corpus requirements

### 3.2 Statistical Analysis Recovery

**Priority Tasks**:
1. **Fix StatisticalAnalysisAgent** to handle consistent JSON inputs and produce valid Cronbach's alpha
2. **Restore CFF Cohesion Index calculation** from Trump study
3. **Restore data visualization capabilities** (HTML charts, timeline graphics)
4. **Validate all statistical calculations** against golden set benchmarks

---

## Phase 4: Product Shell & User Experience (Weeks 12-14)
*Foundation: Build polished user-facing features*

### 4.1 CLI Refinement

**Priority Tasks**:
1. **Implement cost estimation** feature promised in documentation
2. **Create user-friendly CLI experience** with natural language queries and streamlined commands
3. **Implement interactive validation resolution** for experiment issues
4. **Create comprehensive help system** and command documentation

### 4.2 Multi-Format Output System

**Priority Tasks**:
1. **Restore multi-format report generation** (comprehensive, blog post, reflection)
2. **Create export system** for charts, data, and reports in multiple formats
3. **Validate output quality** against Trump study comprehensive report
4. **Validate entire system** against all golden set benchmarks

---

## Risk Mitigation & Quality Assurance

### Critical Success Factors

1. **Framework Agnosticism Enforcement**
   - Automated tests prevent framework-specific assumptions in core software
   - All framework intelligence must reside in framework files, not code
   - Code review process specifically checks for THIN compliance

2. **Regression Prevention**
   - Golden set validation in CI/CD pipeline
   - Automated smoke tests against historical artifacts
   - Comprehensive logging and provenance tracking

3. **Integration Discipline**
   - Single source of truth for all configuration parsing
   - Deterministic control flow (no LLM-driven branching)
   - Modular capability recovery as optional workflow steps

### Quality Gates

**Phase 1 Gate**: System can execute the `vanderveen` test project directory through the main CLI using the existing EnsembleOrchestrator (after fixing the broken ThinOrchestrator imports), successfully loading the separate framework and experiment files.
**Phase 2 Gate**: System can produce structured adversarial review matching SOAR logs
**Phase 3 Gate**: System can ingest Trump study corpus and generate valid statistics
**Phase 4 Gate**: System can automatically generate analysis matching MLK vs. Malcolm quality

---

## Historical Evidence Base

### Proven Capabilities (From Archaeological Analysis)

1. **Multi-Agent Adversarial Review** (SOAR conversation logs)
   - Sequential agent spawning with specialized instructions
   - Moderator/referee arbitration system
   - Structured debate with evidence-based resolution
   - 17-minute sophisticated analysis sessions

2. **Academic-Quality Output** (Trump study artifacts)
   - 1,252-line comprehensive analysis reports
   - Data visualization (HTML charts, timeline graphics)
   - Multi-format output (blog posts, reflections, reports)
   - CFF Cohesion Index calculations with temporal evolution tracking

3. **Framework-Agnostic Architecture** (vanderveen tests - BROKEN)
   - Reference implementations import deprecated ThinOrchestrator (need to fix to use EnsembleOrchestrator)
   - SimpleOverwatch drift detection and prevention patterns
   - Robust, testable execution path concepts
   - Perfect structured JSON output requirements

4. **Manual Analysis Target** (CFF 3.1 studies)
   - MLK vs. Malcolm X comparative analysis
   - Multi-dimensional weighted scoring
   - Historical contextualization
   - Precise numerical analysis with detailed justification

### The Great Regression Timeline

1.  **"SOAR v1" & "DCS Era" (The Golden Age)**: Hyper-sophisticated but complex systems (conversational multi-agent and database-driven coordinate system).
2.  **The "Great Regression"**: These complex systems were deliberately abandoned due to reliability, validity, and architectural rigidity issues.
3.  **The "THIN Reformation"**: A superior, file-based architecture (`ThinOrchestrator` handling separate framework/experiment files) was developed in tests but never fully integrated.
4.  **Current State**: Fragmented components with a broken CLI and a missing, coherent orchestration strategy.

---

## Expected Outcomes

### Immediate Benefits (Phase 1)
- Elimination of "process hallucination" and framework adherence failures
- Reliable structured outputs from any analytical framework
- Unified, maintainable orchestration architecture

### Medium-term Benefits (Phase 2-3)
- Restoration of sophisticated multi-agent adversarial workflows
- Academic-quality analysis and reporting capabilities
- Robust data ingestion and statistical analysis

### Long-term Benefits (Phase 4)
- Polished researcher-grade user experience
- Publication-ready automated analysis matching manual expert quality
- Scalable platform supporting any analytical framework

---

## Implementation Guidelines

### Development Discipline
- **Golden Set Methodology**: All development evaluated against historical quality benchmarks.
- **Incremental Recovery**: Capabilities restored one at a time with verification at each step.
- **THIN Compliance & Coordinate-Free Philosophy**: Automated tests prevent framework-specific assumptions and mathematical reductionism.
- **Archaeological Approach**: Learn from past failures (the brittleness of the DCS) to avoid repeating architectural mistakes.

### Technical Principles
- **Framework Agnosticism**: Zero hardcoded assumptions about framework structure. The orchestrator must be able to process any valid framework file.
- **Mathematical Reliability**: All calculations performed by SecureCodeExecutor.
- **Key Architectural Pattern: "Show Your Work"**: To ensure both mathematical reliability and THIN principles, the primary method for extracting structured data (like numerical scores) from LLM analysis will be the "Show Your Work" pattern. This involves prompting the analysis agent to use its own internal code interpreter to derive a numerical result. The agent must then return both the code it wrote and the result it got. The orchestrator's job is to verify this calculation using its own `SecureCodeExecutor`, not to parse natural language. This eliminates interpretation ambiguity, maximizes provenance, and leverages the advanced capabilities of modern LLMs.
- **Deterministic Control Flow**: No LLM-driven branching for core workflows.
- **Single Source of Truth**: The framework and experiment files are the separate, unambiguous sources of truth for their respective domains.

---

## Conclusion

This is not a speculative development plan but an **evidence-based recovery mission**. Every capability we need to build has been proven to work in our own historical artifacts. The path forward is clear: establish immutable quality benchmarks, fix the existing EnsembleOrchestrator to support project-based workflows, restore sophisticated multi-agent workflows, and wrap it all in a polished user experience.

The golden set methodology ensures we never again lose capabilities through undisciplined refactoring. By treating our best historical outputs as the specification, we can build with confidence toward a concrete, achievable target that represents genuine academic and strategic value.

---

## Appendix: Key Artifacts Referenced

### Quality Benchmarks
- `projects/cff_3_1_studies/mlk_malcolm_cff_comparison.md` - Manual analysis quality target
- `projects/cff_3_0_trump_study/results/comprehensive_trump_cff_analysis_report.md` - Capability benchmark
- `projects/cff_3_0_trump_study/results/trump_cohesion_timeline.html` - Visualization benchmark

### Architectural Templates  
- `reference_implementations/cff_v2_system_test/run_thin_framework_test.py` - BROKEN (imports deprecated ThinOrchestrator)
- `discernus/orchestration/ensemble_orchestrator.py` - Current working THIN orchestrator
- `projects/soar_2_pdaf_poc/results/PDAF_BLIND_EXPERIMENT_CONVERSATION_LOG_20250712.jsonl` - Multi-agent workflow

### Historical Evidence
- `projects/soar_2_pdaf_poc/blind/results/2025-07-12_16-05-00/final_report.md` - Academic synthesis example
- `projects/attesor/experiments/01_smoketest/results/` - Current system failures
- `discernus/orchestration/workflow_orchestrator.py` - Current infrastructure foundation 