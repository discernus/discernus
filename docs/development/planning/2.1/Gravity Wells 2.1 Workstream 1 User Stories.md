# Gravity Wells 2.1 Workstream 1 User Stories
**Key Architectural Insights:**
* Your current system already has robust backend infrastructure (Epic 1-4 complete) with multi-LLM integration and statistical analysis capabilities
* The challenge is creating a **research workbench** that maintains experimental rigor while enabling rapid iteration
* You need **experiment versioning** that tracks the combined prompt-scoring-framework evolution as unified hypotheses

⠀Epic: Integrated Prompt-Scoring Research Workbench
**As a** narrative framework researcher, **I want** a React application that treats prompt engineering and scoring methodology as a unified experimental system with rigorous version control and comparative analysis capabilities, **so that** I can systematically test hypotheses about thematic hierarchy detection while maintaining research reproducibility and avoiding the chaos of scattered files.
# Enhanced User Stories for Integrated Development
**1. Unified Experiment Design Interface**
* **User Story:** As a researcher, I want to design experiments that combine specific prompt template versions, framework configurations, and scoring algorithm variants as single testable hypotheses, so that I can systematically evaluate whether changes improve thematic hierarchy detection.
* **Acceptance Criteria:**
  * Interface presents "Experiment Designer" that bundles prompt template + framework version + scoring parameters as a single experimental condition
  * Users can create "Hypothesis Sets" comparing multiple experimental conditions (e.g., "Hierarchical Prompting v1.2 + Winner-Take-Most Scoring" vs. "Standard Prompting v2.1 + Linear Scoring")
  * Each experiment automatically generates unique identifiers and metadata tracking
  * Experiments can be saved as templates for replication with different text sets
  * The system prevents execution of incomplete experimental designs

⠀**2. Research-Grade Version Control and Provenance**
* **User Story:** As a framework developer, I want comprehensive version tracking that captures the complete experimental context—prompt evolution, framework changes, scoring algorithm modifications, and LLM model versions—so that I can reproduce any analysis and understand what drove performance changes.
* **Acceptance Criteria:**
  * Every analysis result includes complete provenance: prompt template hash, framework version, scoring algorithm version, LLM model and version, timestamp
  * "Experiment Lineage" view shows how prompt and scoring changes evolved together over time
  * Users can "fork" successful experimental conditions to create new variants
  * Rollback capability allows reverting to any previous experimental state
  * Export functionality generates complete replication packages with all versioned components

⠀**3. Systematic Comparative Analysis Dashboard**
* **User Story:** As a researcher, I want to compare experimental results across multiple dimensions—prompt versions, scoring approaches, text types, and LLM models—with statistical rigor, so that I can identify which changes actually improve thematic hierarchy detection.
* **Acceptance Criteria:**
  * Side-by-side comparison view supports up to 4 experimental conditions simultaneously
  * Statistical comparison tools show significance tests for score distributions and hierarchy sharpness metrics
  * "Hierarchy Sharpness" metrics automatically calculated (e.g., coefficient of variation across wells, dominance ratios)
  * Visual comparison shows both raw scores and derived metrics (narrative position, polarity, purity)
  * Results can be filtered by text characteristics (synthetic vs. real-world, political vs. non-political)

⠀**4. Hypothesis-Driven Text Management**
* **User Story:** As a prompt engineer, I want to organize texts into research-relevant categories (validation sets, edge cases, framework fit tests) with the ability to rapidly test experimental conditions against specific text types, so that I can systematically evaluate prompt performance across different narrative characteristics.
* **Acceptance Criteria:**
  * Text library organized by research purpose: "Golden Standard" (known ground truth), "Edge Cases" (challenging scenarios), "Framework Fit Tests" (potential mismatches)
  * Batch testing interface allows running experimental conditions against predefined text sets
  * "Synthetic Text Generator" for creating controlled test cases with known thematic properties
  * Text metadata includes difficulty ratings, expected dominant themes, and framework fit assessments
  * Quick-add functionality for capturing interesting real-world examples during research

⠀**5. Integrated Scoring Algorithm Laboratory**
* **User Story:** As a framework developer, I want to experiment with different scoring approaches (linear averaging, winner-take-most, hierarchical weighting, nonlinear transforms) within the same interface where I'm testing prompts, so that I can evaluate how prompt changes and scoring changes interact to affect thematic hierarchy detection.
* **Acceptance Criteria:**
  * "Scoring Lab" interface allows real-time modification of scoring algorithms with immediate visualization updates
  * Predefined scoring templates: "Linear Average," "Winner-Take-Most," "Exponential Weighting," "Hierarchical Dominance"
  * Custom scoring function editor with validation and testing capabilities
  * A/B testing interface compares scoring approaches on identical prompt-text combinations
  * Mathematical visualization shows how different scoring approaches affect narrative positioning

⠀**6. Research Documentation and Insight Capture**
* **User Story:** As a researcher, I want to capture insights, hypotheses, and observations directly within the experimental interface with automatic linking to specific experimental conditions, so that I can maintain research continuity and build institutional knowledge about what works.
* **Acceptance Criteria:**
  * "Research Notes" system allows tagging observations to specific experiments, prompt versions, or text analyses
  * Hypothesis tracking: state predictions, link to experimental tests, record outcomes
  * "Insight Dashboard" aggregates patterns across experiments (e.g., "Hierarchical prompts consistently improve dominance detection")
  * Automated research summaries highlight significant findings and suggest next experiments
  * Export capability generates research reports with embedded experimental evidence

⠀Technical Architecture for Research Rigor
**Experiment Database Schema:**

### python
### class Experiment:
    id: UUID
    name: str
    hypothesis: str
    prompt_template_version: str
    framework_version: str
    scoring_algorithm_version: str
    created_at: datetime
    status: ExperimentStatus

### class ExperimentRun:
    id: UUID
    experiment_id: UUID
    text_id: UUID
    llm_model: str
    llm_version: str
    raw_scores: Dict[str, float]
    calculated_metrics: Dict[str, float]
    execution_time: datetime
    
### class ExperimentComparison:
    id: UUID
    experiment_ids: List[UUID]
    comparison_metrics: Dict[str, float]
    statistical_tests: Dict[str, float]
    researcher_notes: str
**Research Workflow Integration:**
* Connect to your existing FastAPI backend for LLM orchestration
* Leverage your current multi-run statistical analysis capabilities
* Extend your framework switching system to support experimental conditions
* Build on your existing visualization engine for comparative displays

⠀**Quality Assurance Features:**
* Automated validation that experimental conditions are properly specified
* Statistical power analysis to ensure adequate sample sizes
* Drift detection to identify when LLM model updates affect consistency
* Replication verification that ensures experiments can be reproduced

⠀This approach transforms the React app from a simple prompt editor into a **research workbench** that maintains experimental rigor while enabling the rapid iteration you need. The key insight is treating each combination of prompt + framework + scoring approach as a testable hypothesis rather than separate components, which aligns with your recognition that these elements are fundamentally interdependent. The interface becomes your **research laboratory** rather than just a development tool, ensuring that insights are captured, experiments are reproducible, and progress is systematic rather than chaotic.

#personal/writing/narrativegravity