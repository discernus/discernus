# Cursor Development Prompt for Workstream 1 React Application

## Primary Development Objective
Build a React research workbench that treats prompt engineering and scoring methodology as unified experimental hypotheses, enabling systematic iteration while maintaining research reproducibility.
## Core Application Architecture
**Unified Experiment Design Interface**: Create a React component that bundles prompt template versions, framework configurations, and scoring algorithm variants as single testable hypotheses. The interface should present an "Experiment Designer" where users can create "Hypothesis Sets" comparing multiple experimental conditions (e.g., "Hierarchical Prompting v1.2 + Winner-Take-Most Scoring" vs. "Standard Prompting v2.1 + Linear Scoring").
**Dual-Layer Prompt Editor**: Implement a split-editor interface separating general-purpose prompt templates from framework-specific dipole definitions. Include a "Preview Combined Prompt" function that shows the final merged prompt sent to the LLM, with validation ensuring all template variables have corresponding framework content.
**Research-Grade Version Control**: Every analysis result must include complete provenance—prompt template hash, framework version, scoring algorithm version, LLM model and version, timestamp. Implement an "Experiment Lineage" view showing how prompt and scoring changes evolved together over time.
## Technical Implementation Specifications
**Backend Integration**: Connect to existing FastAPI endpoints (/api/corpora, /api/jobs, /api/results) while respecting the modular architecture. Use the established data models (Corpus, Document, Chunk, Job, Task) that support experimental tracking.
**State Management**: Use Zustand for managing complex experimental state—tracking prompt versions, framework configurations, and analysis results. Implement optimistic updates for rapid iteration while maintaining data consistency.
**Component Structure**:
* Experiment Designer for hypothesis creation
* Split-pane prompt editor with live preview
* Comparative analysis dashboard supporting up to 4 experimental conditions
* Results pinning system for side-by-side comparison
* Version control interface with semantic versioning display

⠀Key User Workflows to Implement
**Experiment Creation Workflow**: User selects prompt template version → chooses framework version → configures scoring parameters → selects test texts → creates named experiment with unique identifier.
**Rapid Iteration Cycle**: Edit prompt in left pane → see framework content in right pane → preview combined prompt → run single-text analysis → view JSON scores and qualitative commentary → pin results for comparison → iterate.
**Comparative Analysis**: Pin multiple analysis results → view side-by-side with statistical comparison tools → highlight differences in numerical scores → filter by text characteristics or experimental conditions.
## Critical Technical Requirements
**Data Schema Integration**: Implement experiment versioning that tracks the combined prompt-scoring-framework evolution as unified hypotheses. Each experiment should generate unique identifiers with complete metadata tracking.
**Statistical Analysis**: Integrate hierarchy sharpness metrics (coefficient of variation across wells, dominance ratios) and comparative analysis tools showing significance tests for score distributions.
**Visualization Components**: Start with simple bar charts separating integrative (positive) and disintegrative (negative) dipole scores, color-coded for quick visual distinction, with metadata showing all version information.
## Development Priorities
**Phase 1**: Build the unified experiment design interface and dual-layer prompt editor with backend integration for single-text analysis.
**Phase 2**: Implement version control, result pinning, and comparative analysis dashboard.
**Phase 3**: Add statistical analysis tools, batch testing capabilities, and performance monitoring.
The application should transform your manual research process into a systematic research laboratory that maintains experimental rigor while enabling the rapid iteration necessary for integrated prompt-scoring development. Focus on treating each combination of prompt + framework + scoring approach as a testable hypothesis rather than separate components.
Use Shadcn/ui components for professional appearance, implement TypeScript throughout for type safety with your FastAPI backend, and ensure the interface supports the academic validation requirements outlined in your validation-first development strategy.

Unified experiment design interface treating prompt-scoring as integrated hypotheses
* **Research-grade version control** capturing complete experimental provenance
* **Systematic comparative analysis** with statistical rigor for validation
* **Hypothesis-driven text management** organized by research purpose
* **Integrated scoring algorithm laboratory** for real-time methodology testing

#personal/writing/narrativegravity