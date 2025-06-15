# Experiment Plan: IDITI Framework Validation

*   **Experiment ID**: `iditi_framework_validation_20250614_213725`
*   **Date**: 2025-06-14
*   **Status**: Planning

## 1. Research Question

Does the `iditi` framework accurately classify texts that have been pre-labeled as appealing to "Dignity" versus "Tribalism"?

**Hypothesis**: Texts from the `*_dignity` folders in the validation set will score high on the "Dignity" well and low on "Tribalism." Conversely, texts from the `*_tribalism` folders will show the opposite pattern. Texts from `controls` and `mixed` folders are expected to have more balanced or neutral scores.

## 2. Experimental Design (Single-Factor Validation)

This experiment is a single-factor validation study based on the principles in `EXPERIMENTAL_DESIGN_FRAMEWORK.md`.

*   **Dimension 1: TEXTS (Fixed)**
    *   **Corpus**: All texts within the subdirectories of `corpus/validation_set/`.
    *   **Source Categories**: `conservative_dignity`, `progressive_dignity`, `conservative_tribalism`, `progressive_tribalism`, `mixed`, and `controls`.

*   **Dimension 2: FRAMEWORKS (Fixed)**
    *   **Framework**: `iditi`

*   **Dimension 3: PROMPT TEMPLATES (Fixed)**
    *   **Prompt**: `hierarchical_v2.1`

*   **Dimension 4: WEIGHTING SCHEMES (Fixed)**
    *   **Scheme**: `winner_take_most`

*   **Dimension 5: EVALUATORS (Fixed for Initial Run)**
    *   **Initial Evaluator**: A high-capability LLM (e.g., GPT-4).

## 3. Methodology

1.  **Corpus Ingestion**: Process all text files from the specified `validation_set` subdirectories, retaining their source folder as a ground-truth label.
2.  **Execution**: Run the texts through the narrative gravity analysis pipeline using a dedicated Python script.
3.  **Validation**: Compare the output scores ("Dignity" vs. "Tribalism") against the ground-truth labels.
4.  **Visualization**: Generate visualizations (e.g., a scatter plot or box plots) that group the results by the source folder to visually assess the framework's classification accuracy.

## 4. Results and Artifacts

*   **Results Directory**: All outputs will be stored in `experiment_reports/iditi_framework_validation_20250614_213725/`.
*   **Analysis Script**: A Python script will be created in `examples/experiments/iditi_validation_study/`.
*   **Outputs**:
    *   Raw JSONL analysis results with ground-truth labels.
    *   Aggregated CSV file of scores, including ground-truth labels.
    *   Validation report with accuracy metrics.
    *   Comparative visualizations.

## 5. Next Steps

1.  Create the analysis script.
2.  Create the results directory.
3.  Run the experiment.
4.  Analyze and visualize the results to validate the framework. 