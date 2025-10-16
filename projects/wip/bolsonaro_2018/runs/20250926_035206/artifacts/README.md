# Discernus Research Experiment: `bolsonaro_2018`

## Table of Contents

1.  [Overview](#1-overview)
2.  [Experiment Details](#2-experiment-details)
3.  [Artifact Inventory & Description](#3-artifact-inventory--description)
    *   [experiment_spec](#experimentspec)
    *   [framework](#framework)
    *   [corpus_manifest](#corpus_manifest)
    *   [corpus_document](#corpus_document)
    *   [composite_analysis](#composite_analysis)
    *   [evidence_extraction](#evidence_extraction)
    *   [score_extraction](#score_extraction)
    *   [marked_up_document](#marked_up_document)
    *   [statistical_analysis](#statistical_analysis)
    *   [final_synthesis_report](#final_synthesis_report)
    *   [run_context](#run_context)
4.  [Directory Structure](#4-directory-structure)
5.  [Provenance Information](#5-provenance-information)
6.  [Usage for Researchers and Auditors](#6-usage-for-researchers-and-auditors)
7.  [Contact](#7-contact)

---

## 1. Overview

This README provides a comprehensive guide to the `bolsonaro_2018` Discernus research experiment. It details the experiment's purpose, methodology, and the complete set of generated artifacts, ensuring discoverability, reproducibility, and auditability.

*   **Experiment Name:** `bolsonaro_2018`
*   **Run ID:** `bolsonaro_2018_20250925_235206`
*   **Completion Date:** `2025-09-26T03:52:06.506453+00:00`
*   **Project Directory:** `/Volumes/code/discernus/projects/wip/bolsonaro_2018`
*   **Purpose:** This experiment likely investigates aspects related to Jair Bolsonaro's 2018 presidential campaign or related discourse, utilizing the Discernus framework for structured analysis of a defined corpus of documents. The specific research questions and analytical lens are detailed within the `experiment_spec` and `framework` artifacts.

## 2. Experiment Details

This section outlines the core components that define the `bolsonaro_2018` experiment.

*   **Analytical Framework:** The experiment was conducted using the Discernus framework defined in `framework.md`. This document outlines the analytical categories, coding scheme, and methodological principles applied.
*   **Corpus Definition:** The set of documents analyzed is described in `corpus.md`. This file provides context for the selection criteria and scope of the corpus.
*   **Number of Documents Analyzed:** 12

## 3. Artifact Inventory & Description

This experiment produced a total of 69 artifacts, categorized by type. Each artifact type plays a crucial role in the Discernus methodology, from defining the experiment to presenting the final findings. The artifacts are stored within the `artifacts/` subdirectory, typically organized into subfolders corresponding to their type.

---

### `experiment_spec`

*   **Count:** 1 artifact
*   **Description:** This artifact contains the formal specification of the experiment. It details the research questions, hypotheses, analytical objectives, and any specific parameters or configurations used during the experiment's execution. It serves as the blueprint for the entire research process.
*   **Typical Format:** JSON or YAML.
*   **Location:** `artifacts/experiment_spec/`

### `framework`

*   **Count:** 1 artifact
*   **Description:** This artifact is a copy of the analytical framework (`framework.md`) used for the experiment. It defines the structured approach to analysis, including categories, indicators, and scoring rubrics. It is critical for understanding the methodology applied.
*   **Typical Format:** Markdown (`.md`).
*   **Location:** `artifacts/framework/`

### `corpus_manifest`

*   **Count:** 1 artifact
*   **Description:** A comprehensive manifest listing all documents included in the corpus. For each document, it typically includes metadata such as its unique identifier, original filename, source URL (if applicable), and any other relevant contextual information.
*   **Typical Format:** JSON or CSV.
*   **Location:** `artifacts/corpus_manifest/`

### `corpus_document`

*   **Count:** 12 artifacts
*   **Description:** These are the raw, original source documents that constitute the corpus for this experiment. Each document is preserved in its original or a standardized format to ensure fidelity to the source material.
*   **Typical Format:** PDF, HTML, TXT, DOCX, etc.
*   **Location:** `artifacts/corpus_document/`

### `composite_analysis`

*   **Count:** 12 artifacts
*   **Description:** For each document in the corpus, this artifact provides a consolidated view of its analysis. It aggregates the extracted evidence, assigned scores, and any document-specific summary or qualitative observations, offering a complete analytical record for that document.
*   **Typical Format:** JSON or Markdown.
*   **Location:** `artifacts/composite_analysis/`

### `evidence_extraction`

*   **Count:** 12 artifacts
*   **Description:** These artifacts contain the specific textual segments or data points extracted from each document that serve as direct evidence for the analytical categories defined in the framework. Each piece of evidence is typically linked to its source location within the document.
*   **Typical Format:** JSON (structured data with text, location, and category).
*   **Location:** `artifacts/evidence_extraction/`

### `score_extraction`

*   **Count:** 12 artifacts
*   **Description:** For each document, this artifact records the scores assigned based on the extracted evidence and the criteria outlined in the analytical framework. Scores quantify the presence or absence, intensity, or other characteristics of the analytical categories.
*   **Typical Format:** JSON or CSV.
*   **Location:** `artifacts/score_extraction/`

### `marked_up_document`

*   **Count:** 12 artifacts
*   **Description:** These are versions of the original `corpus_document` with the extracted evidence and associated scores visually highlighted or annotated. This artifact provides a direct, auditable link between the raw text and its analysis, facilitating verification.
*   **Typical Format:** Annotated PDF, HTML with embedded highlights/tooltips.
*   **Location:** `artifacts/marked_up_document/`

### `statistical_analysis`

*   **Count:** 1 artifact
*   **Description:** This artifact presents the quantitative analysis performed across the entire corpus. It includes aggregated scores, statistical summaries, trends, and potentially visualizations derived from the `score_extraction` artifacts.
*   **Typical Format:** Markdown report, CSV, JSON, or statistical software output.
*   **Location:** `artifacts/statistical_analysis/`

### `final_synthesis_report`

*   **Count:** 1 artifact
*   **Description:** The culminating report of the experiment. It synthesizes the findings from the `statistical_analysis` and qualitative observations, discusses the implications, answers the research questions, and presents the overall conclusions of the study.
*   **Typical Format:** Markdown report or PDF.
*   **Location:** `artifacts/final_synthesis_report/`

### `run_context`

*   **Count:** 1 artifact
*   **Description:** This artifact captures the environment and parameters under which the experiment was executed. It includes details such as software versions, timestamps, user information, and system configurations, essential for ensuring the reproducibility and auditability of the experiment.
*   **Typical Format:** JSON or YAML.
*   **Location:** `artifacts/run_context/`

---

## 4. Directory Structure

The experiment's output is organized within the main project directory `/Volumes/code/discernus/projects/wip/bolsonaro_2018` as follows:

```
bolsonaro_2018/
├── README.md                                 <-- This file
├── framework.md                              <-- The analytical framework document
├── corpus.md                                 <-- The corpus definition document
└── artifacts/                                <-- Main directory for all generated artifacts
    ├── composite_analysis/                   <-- Contains 12 composite analysis files (one per document)
    ├── corpus_document/                      <-- Contains 12 raw corpus documents
    ├── corpus_manifest/                      <-- Contains 1 corpus manifest file
    ├── evidence_extraction/                  <-- Contains 12 evidence extraction files (one per document)
    ├── experiment_spec/                      <-- Contains 1 experiment specification file
    ├── final_synthesis_report/               <-- Contains 1 final synthesis report
    ├── framework/                            <-- Contains 1 copy of the framework.md
    ├── marked_up_document/                   <-- Contains 12 marked-up documents (one per document)
    ├── run_context/                          <-- Contains 1 run context file
    ├── score_extraction/                     <-- Contains 12 score extraction files (one per document)
    └── statistical_analysis/                 <-- Contains 1 statistical analysis report
```

## 5. Provenance Information

The integrity and traceability of this experiment are paramount. The following artifacts provide key provenance information:

*   **`experiment_spec`**: Defines *what* the experiment was designed to achieve and *how* it was intended to be executed.
*   **`run_context`**: Records the *exact conditions* under which the experiment was run, including timestamps, software versions, and system details. This is crucial for reproducibility.
*   **`framework.md` (and `artifacts/framework/`)**: Documents the *methodology* and analytical categories applied.
*   **`corpus.md` (and `artifacts/corpus_manifest/`)**: Specifies the *data sources* and their selection criteria.

Together, these artifacts allow researchers and auditors to fully understand the origin, execution, and analytical basis of the `bolsonaro_2018` experiment.

## 6. Usage for Researchers and Auditors

This section provides guidance on how to navigate and utilize the experiment's artifacts.

1.  **Understand the Experiment's Goals:**
    *   Begin by reviewing `artifacts/experiment_spec/` to grasp the research questions and objectives.
    *   Read `framework.md` (or `artifacts/framework/`) to understand the analytical methodology.

2.  **Review the Corpus:**
    *   Consult `corpus.md` and `artifacts/corpus_manifest/` to see the list of analyzed documents and their metadata.
    *   Access the raw documents in `artifacts/corpus_document/` for direct inspection.

3.  **Examine Individual Document Analyses:**
    *   For a comprehensive view of a single document's analysis, refer to its corresponding file in `artifacts/composite_analysis/`.
    *   To see the specific evidence extracted, check `artifacts/evidence_extraction/`.
    *   To review the scores assigned, look into `artifacts/score_extraction/`.
    *   For a visual representation of the analysis directly on the source text, examine the `artifacts/marked_up_document/` files.

4.  **Analyze Aggregate Findings:**
    *   The quantitative results and statistical summaries are available in `artifacts/statistical_analysis/`.
    *   The primary conclusions, discussions, and answers to research questions are presented in the `artifacts/final_synthesis_report/`.

5.  **Verify Reproducibility and Auditability:**
    *   The `artifacts/run_context/` file provides the technical details of the experiment's execution environment, essential for auditing and attempting to reproduce the results.

## 7. Contact

For questions or further information regarding this Discernus experiment, please refer to the project documentation or contact the research team responsible for its execution.