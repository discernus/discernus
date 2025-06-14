# Replicating Analyses from "Narrative Gravity Maps" Paper

This document provides instructions on how to replicate the key analyses presented in the paper "Narrative Gravity Maps: A Quantitative Framework for Discerning the Forces Driving Persuasive Narratives."

## Software Version

The analyses in the paper were generated using version [YOUR_GIT_TAG_OR_COMMIT_HASH_HERE] of this software. You can check out this specific version from the repository to ensure maximum fidelity.

## General Workflow for Replication

For each analysis listed below, you will find:
1.  The specific framework used.
2.  The input text(s) used.
3.  **Crucially, the pre-computed JSON score file(s)** generated from our LLM analysis. Using these files allows you to bypass the LLM step and directly replicate the visualizations and metrics presented in the paper.
4.  Instructions on how to generate the visualization using the provided JSON data.

**Important Note on Model Identification**: When using AI platforms (like Perplexity, Poe, etc.) that utilize underlying models, the JSON output may identify the platform rather than the underlying model. For academic accuracy, you may need to manually update the `model_name` and `model_version` fields to reflect the actual model that performed the analysis (e.g., changing "Perplexity" to "Claude-4.0-Sonnet" if that was the selected underlying model).

## Core Analyses

### 1. Analysis of Nelson Mandela's 1994 Inaugural Address (Figure 1)

*   **Framework:** Civic Virtue Framework
    *   Location: `frameworks/civic_virtue/`
*   **Input Text:** Nelson Mandela's 1994 Inaugural Address
    *   Location: `reference_texts/mandela_1994_inaugural.txt`
*   **Pre-computed LLM Scores:**
    *   File: `model_output/paper_analyses/mandela_1994_inaugural_scores.json`
    *   *(Suggestion: You will need to create this JSON file containing the scores that correspond to your Figure 1)*
*   **Replication using Streamlit App:**
    1.  Launch the Streamlit app: `python launch_app.py`
    2.  Navigate to the "📝 Create Analysis" tab.
    3.  In "Step 2: Input LLM Analysis (JSON)", click "Browse files" and upload `model_output/paper_analyses/mandela_1994_inaugural_scores.json`.
    4.  Click "🎯 Generate Visualization".
    5.  The visualization and metrics corresponding to Figure 1 should be displayed.
*   **Replication using Command Line:**
    ```bash
    python narrative_gravity_elliptical.py model_output/paper_analyses/mandela_1994_inaugural_scores.json --output output_visualizations/mandela_figure_1.png
    ```

### 2. Comparative Analysis: Mandela (1994) vs. Chavez (UN Speech) (Figure 2)

*   **Framework:** Civic Virtue Framework
    *   Location: `frameworks/civic_virtue/`
*   **Input Texts:**
    1.  Nelson Mandela's 1994 Inaugural Address
        *   Location: `reference_texts/mandela_1994_inaugural.txt`
    2.  Hugo Chavez's UN Speech (Please specify which one, e.g., 2006)
        *   Suggestion: Add this text to `reference_texts/chavez_un_2006.txt` (or similar)
*   **Pre-computed LLM Scores:**
    1.  Mandela: `model_output/paper_analyses/mandela_1994_inaugural_scores.json` (as above)
    2.  Chavez: `model_output/paper_analyses/chavez_un_2006_scores.json`
        *   *(Suggestion: You will need to create this JSON file for Chavez's speech corresponding to your Figure 2)*
*   **Replication using Streamlit App:**
    1.  Launch the Streamlit app: `python launch_app.py`
    2.  Navigate to the "🔍 Compare Analysis" tab.
    3.  Ensure "civic_virtue" is the selected framework.
    4.  For "Select first analysis:", choose `mandela_1994_inaugural_scores.json` (you might need to place it directly in `model_output` or adjust paths/upload).
    5.  For "Select second analysis:", choose `chavez_un_2006_scores.json`.
    6.  Click "🔍 Compare Analyses".
    7.  The comparative visualization corresponding to Figure 2 should be displayed.
    *Note: The Streamlit app's file browser for comparison currently looks directly in `model_output/`. You may need to temporarily copy your specific paper JSONs there or adjust this part of the instructions if you keep them in `model_output/paper_analyses/`.*
*   **Replication using Command Line:**
    ```bash
    python narrative_gravity_elliptical.py model_output/paper_analyses/mandela_1994_inaugural_scores.json model_output/paper_analyses/chavez_un_2006_scores.json --output output_visualizations/comparative_figure_2.png
    ```

---

*Further analyses presented in the paper can be documented here following the same format.* 