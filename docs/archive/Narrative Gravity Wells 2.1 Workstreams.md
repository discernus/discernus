# Narrative Gravity Wells 2.1 Workstreams
#personal/writing/narrativegravity

## Linked Documents
[[Human Thematic Perception and Computational Replication: A Literature Review]]
[[8 June Project Strategic Analysis]]
[[Narrative Gravity Wells Project: Consolidated Workstreams, Dependencies, and Schedule]]

## Workstream 1: React Frontend Research Workbench 
**Status: ✅ COMPLETED** (as of 2025-01-06)
**Deliverable**: Production-ready React application with TypeScript, modern UI, and comprehensive testing.

### Completed Features:
- ✅ Four-panel tabbed interface (Experiment Designer, Prompt Editor, Analysis Results, Comparison Dashboard)
- ✅ Unified experiment design workflow with configuration dropdowns
- ✅ State management using Zustand with comprehensive stores
- ✅ Modern React 18 + TypeScript + Vite + Tailwind CSS stack
- ✅ Comprehensive test suite with all tests passing
- ✅ Zero TypeScript errors, stable builds
- ✅ Debug console and development tools
- ✅ Responsive design and modern UX

**Deliverable Status**: Complete and ready for backend integration

---

## Workstream 2: Backend API Integration 
**Status: ⚠️ IN PROGRESS** (High Priority)
**Deliverable**: FastAPI endpoints that connect the frontend to the existing analysis engine

### Immediate Tasks:
- 🔴 Create missing API endpoints (`/api/experiments`, `/api/runs`, configuration endpoints)
- 🔴 Connect frontend apiClient.ts to real backend endpoints  
- 🔴 Implement experiment execution engine integration
- 🔴 Populate database with prompt templates, frameworks, and scoring algorithms
- 🔴 Test end-to-end experiment creation and execution workflow

**Current Gap**: Frontend expects API endpoints that don't exist yet. This is the critical blocker for a fully functional v2.1 system.

---

## Workstream 3: Database Schema Enhancement
**Status: ✅ COMPLETED** (as of 2025-01-06)
**Deliverable**: PostgreSQL schema supporting unified experiments and hierarchical results

### Completed Features:
- ✅ New `experiments` table for unified experiment design
- ✅ New `runs` table for hierarchical analysis results
- ✅ Enhanced existing job/task tables with v2.1 features
- ✅ Proper foreign key relationships and constraints
- ✅ Alembic migrations created and ready to deploy
- ✅ Models updated in `src/narrative_gravity/models/`

**Deliverable Status**: Complete and ready for use

---

## Workstream 4: Enhanced Analysis Features
**Status: 🟡 PLANNED** (Medium Priority)
**Deliverable**: Advanced analysis capabilities and improved user experience

### Planned Features:
- 🟡 Real-time analysis progress tracking
- 🟡 Advanced result filtering and comparison tools
- 🟡 Experiment versioning and cloning
- 🟡 Export functionality for academic formats
- 🟡 Enhanced error handling and user feedback

**Dependencies**: Requires completion of Workstream 2 (Backend API Integration)

---

## Current Status Summary (2025-01-06)

### ✅ **Ready for Production:**
- Frontend React application (fully functional standalone)
- Database schema (migrations ready)
- Development environment and testing infrastructure

### 🔴 **Critical Path (Blocks v2.1 Release):**
- Backend API integration between frontend and existing analysis engine
- Missing API endpoints for experiments, runs, and configuration data

### 🎯 **Next Priority:**
Focus entirely on **Workstream 2 (Backend API Integration)** - this is the only remaining blocker for a fully functional v2.1 Phase 1 Research Workbench.

**Estimated Timeline**: 1-2 weeks to complete critical API integration, then 2-3 weeks for enhanced features.

# Work Stream 1: Prompt Engineering and Scoring Framework Refinement
**Objective:** Evolve your LLM prompts and scoring logic so that thematic dominance and relative weighting are surfaced reliably.
1 Define revised prompt templates that require the model to
	* identify and rank the top 2–3 driving wells
	* assign each a true relative weight (e.g., percentage or ratio)
	* provide evidence excerpts for each ranked well
2 Prototype and test these prompts on a representative set of synthetic narratives to confirm they produce sharply distinguished well weights.
3 Integrate a nonlinear weighting mechanism (e.g., exponential weighting or winner-take-most logic) into the score-to-position calculation.
4 Run multi-model comparisons (Claude 3.5, GPT-4) on the same texts to assess stability and choose the optimal LLM or ensemble approach.
5 Iterate prompt wording and scoring code based on quantitative divergence from your expected dominance hierarchies.

# ⠀Work Stream 2: Human–Machine Alignment and Validation
**Objective:** Benchmark LLM-derived theme weights and scores against human judgments to establish reliability and identify gaps.
1 Assemble a diverse pool of expert annotators and define a coding scheme that captures both absolute well presence and relative dominance.
2 Develop a test dataset of real-world political narratives (including Trump's address, historical speeches) and synthetic extremes.
3 Conduct blind annotation rounds, capturing inter-rater reliability (e.g., Cohen's κ) on well scores and weighted salience rankings.
4 Compare human annotations to LLM outputs using salience ranking correlation (e.g., Spearman's ρ) and highlight systematic mismatches.
5 Refine prompts or scoring logic to address the largest misalignments, then re-validate on a fresh sample to measure improvement.

# ⠀Work Stream 3: Visualization Strategy Enhancement
**Objective:** Create visual encodings that accurately reflect both absolute scores and relative dominance, eliminating compression of extremes.
1 Prototype adaptive-scaling plots where the ellipse boundary dynamically expands or nonlinear transforms exaggerate differences near poles.
2 Implement "edge snapping" for narratives with a single dominant well (e.g., relative weight >80%).
3 Develop complementary visual elements—radial distance bars, vector thickness proportional to relative weight, and color gradients indicating dominance tiers.
4 Conduct user testing (experts and lay audiences) to compare interpretability across visual variants.
5 Standardize the visualization library, documenting recommended default settings and user-adjustable parameters.

# ⠀Work Stream 4: Documentation, Transparency, and Ethical Guardrails
**Objective:** Ensure all capabilities, limitations, and validation outcomes are clearly documented for users and stakeholders.
1 Draft a comprehensive technical white paper that describes
	* prompt evolution history and scoring algorithms
	* validation methodology and human–machine alignment metrics
	* visualization design rationale and user feedback results
2 Produce an executive-level summary of do's and don'ts for interpreting Narrative Gravity Maps.
3 Create machine-readable metadata standards for each analysis run (e.g., prompt version, model version, fit scores).
4 Publish open-source reference implementations and annotated example notebooks.
5 Establish a versioning and change-log process to track framework updates and maintain epistemic transparency.

# ⠀Work Stream 5: Framework Fit Detection and Modular Extension
**Objective:** Build mechanisms for the system to self-identify when the existing wells fail to capture a narrative's driving themes and to suggest extensions.
1 Enable the LLM to output a "framework fit" score or flag when dominant themes fall outside the ten wells.
2 Collect and analyze low-fit cases to identify common missing dimensions (e.g., ecological, technological optimism).
3 Define a process for proposing new wells or subdimensions, including literature-backed conceptual definitions and mapping rules.
4 Pilot the extended dipole sets on held-out narratives and evaluate whether fit scores improve without diluting core dipoles.
5 Integrate fit-detection feedback into the user interface, guiding analysts on when to customize the framework.

# ⠀Work Stream 6: Data Infrastructure and Automation
**Objective:** Streamline the end-to-end analysis pipeline for scalability, reproducibility, and continuous validation.
1 Build a standardized ingestion and preprocessing system for narrative texts, ensuring consistent formatting and metadata capture.
2 Containerize prompt–model invocation and analysis scripts, parameterized by framework version and LLM choice.
3 Automate multi-run batching, result aggregation, and metric computation (e.g., elevation, polarity, coherence).
4 Develop dashboards that track model performance over time and flag drift in scoring distributions or fit scores.
5 Schedule periodic revalidation workflows that rerun key test cases whenever prompts or models are updated.

⠀By advancing these six concurrent work streams—with carefully sequenced tasks—you will systematically refine your narrative scoring, ensure human-aligned validity, optimize communication of results, and maintain rigorous documentation and adaptability.
