# Discernus Experiment: `bolsonaro_2018`

## Table of Contents

1.  [Introduction](#1-introduction)
2.  [Experiment Overview](#2-experiment-overview)
3.  [Methodological Framework and Corpus](#3-methodological-framework-and-corpus)
4.  [Artifact Inventory and Description](#4-artifact-inventory-and-description)
    *   [Core Experiment Definitions](#core-experiment-definitions)
    *   [Corpus Management](#corpus-management)
    *   [Document-Level Analysis Outputs](#document-level-analysis-outputs)
    *   [Aggregated and Final Outputs](#aggregated-and-final-outputs)
    *   [Provenance and Validation](#provenance-and-validation)
5.  [Directory Structure](#5-directory-structure)
6.  [Provenance and Reproducibility](#6-provenance-and-reproducibility)
7.  [Usage for Researchers and Auditors](#7-usage-for-researchers-and-auditors)
8.  [Contact Information](#8-contact-information)

---

## 1. Introduction

This README file provides a comprehensive guide to the `bolsonaro_2018` Discernus research experiment. It serves as a central point of reference for understanding the experiment's scope, methodology, outputs, and structure. Designed for researchers, auditors, and anyone interested in reviewing the findings or replicating the analysis, this document details each component generated during the experiment run.

The Discernus framework facilitates rigorous, transparent, and reproducible qualitative and quantitative analysis of textual corpora. This experiment applies the Discernus methodology to a specific set of documents related to the `bolsonaro_2018` context.

## 2. Experiment Overview

*   **Experiment Name:** `bolsonaro_2018`
*   **Run ID:** `bolsonaro_2018_20250925_191039`
*   **Completion Date:** `2025-09-25T23:10:39.703066+00:00`
*   **Base Directory:** `/Volumes/code/discernus/projects/wip/bolsonaro_2018`
*   **Number of Documents Analyzed:** 12

This experiment involved the systematic analysis of 12 documents using a predefined methodological framework to extract evidence, assign scores, and synthesize findings.

## 3. Methodological Framework and Corpus

The foundation of this experiment lies in its explicitly defined framework and corpus.

*   **Framework Used:** The analytical methodology, criteria, and scoring rubrics applied in this experiment are detailed in:
    [framework.md](framework.md)
    This document outlines the theoretical and practical approach taken for evidence extraction and scoring.

*   **Corpus Definition:** The set of documents selected for analysis is defined and described in:
    [corpus.md](corpus.md)
    This file provides metadata and context for the 12 documents included in the study.

## 4. Artifact Inventory and Description

The following artifacts were generated during the `bolsonaro_2018` experiment run. Each artifact type plays a specific role in the Discernus methodology, contributing to the transparency and verifiability of the research process.

### Core Experiment Definitions

*   **`experiment_spec` (1 artifact)**
    *   **Description:** This artifact contains the formal specification of the experiment, including its objectives, parameters, and configuration settings. It acts as the blueprint for the entire analysis, ensuring that the experiment was executed according to a predefined plan.
    *   **Purpose:** Essential for understanding the experiment's design and for future replication.
    *   **Location:** Typically found at the root of the experiment directory.

### Corpus Management

*   **`corpus_manifest` (1 artifact)**
    *   **Description:** A comprehensive list of all documents included in the corpus, often accompanied by relevant metadata such as source, date, and unique identifiers.
    *   **Purpose:** Provides an auditable record of the exact documents analyzed, facilitating corpus verification.
    *   **Location:** Typically found at the root of the experiment directory.

*   **`corpus_document` (12 artifacts)**
    *   **Description:** These are the raw, original documents that constitute the corpus for this experiment. They are the primary data source upon which all analysis is performed.
    *   **Purpose:** To provide direct access to the source material for verification and contextual understanding.
    *   **Location:** Usually stored in a dedicated `corpus/` subdirectory.

### Document-Level Analysis Outputs

These artifacts represent the granular results of the analysis for each individual document.

*   **`evidence_extraction` (12 artifacts)**
    *   **Description:** For each document, this artifact contains the specific textual excerpts or data points identified and extracted as evidence relevant to the analytical framework.
    *   **Purpose:** To show precisely *what* information from the original document was considered pertinent for analysis and scoring.
    *   **Location:** Typically found in an `evidence_extraction/` subdirectory, with one file per document.

*   **`score_extraction` (12 artifacts)**
    *   **Description:** This artifact details the scores assigned to specific criteria for each document, based on the extracted evidence. Scores can be numerical, categorical, or qualitative.
    *   **Purpose:** To record the direct analytical judgments made for each criterion per document, providing the basis for aggregation.
    *   **Location:** Typically found in a `score_extraction/` subdirectory, with one file per document.

*   **`composite_analysis` (12 artifacts)**
    *   **Description:** A comprehensive analytical output for each document, combining the extracted evidence, assigned scores, and initial interpretations. This artifact provides a holistic view of the analysis for a single document.
    *   **Purpose:** To offer a complete, auditable record of the analysis performed on each individual document. This is often the most useful artifact for reviewing specific document analyses.
    *   **Location:** Typically found in a `composite_analysis/` subdirectory, with one file per document.

*   **`marked_up_document` (12 artifacts)**
    *   **Description:** Versions of the original `corpus_document` with annotations, highlights, or other visual markings indicating the locations of extracted evidence or points of analytical interest.
    *   **Purpose:** To visually link the analytical findings directly back to the source text, enhancing transparency and ease of verification.
    *   **Location:** Typically found in a `marked_up_document/` subdirectory, with one file per document.

### Aggregated and Final Outputs

These artifacts synthesize the document-level analyses into broader findings and reports.

*   **`statistical_analysis` (1 artifact)**
    *   **Description:** This artifact presents the aggregated quantitative analysis across all documents. It includes statistical summaries, distributions, correlations, and other quantitative insights derived from the `score_extraction` artifacts.
    *   **Purpose:** To identify overarching trends, patterns, and significant findings from the entire corpus.
    *   **Location:** Typically found at the root or in an `analysis/` subdirectory.

*   **`final_synthesis_report` (1 artifact)**
    *   **Description:** The primary output of the experiment, this report synthesizes all findings, conclusions, and implications. It integrates insights from both the qualitative (composite analysis) and quantitative (statistical analysis) aspects of the study.
    *   **Purpose:** To present the main research outcomes and conclusions in a coherent, narrative format. This is often the starting point for understanding the experiment's results.
    *   **Location:** Typically found at the root or in a `reports/` subdirectory.

### Provenance and Validation

*   **`validation_report` (1 artifact)**
    *   **Description:** A report detailing the validation steps performed during or after the experiment. This can include data integrity checks, consistency checks, inter-rater reliability assessments (if applicable), and other quality assurance measures.
    *   **Purpose:** To demonstrate the robustness and reliability of the experiment's data and analysis.
    *   **Location:** Typically found at the root or in a `reports/` subdirectory.

*   **`run_context` (1 artifact)**
    *   **Description:** This artifact captures the environment in which the experiment was executed, including software versions, system configurations, and other contextual information.
    *   **Purpose:** Crucial for ensuring the reproducibility of the experiment by documenting the exact conditions under which it was run.
    *   **Location:** Typically found at the root of the experiment directory.

## 5. Directory Structure

The experiment's directory (`/Volumes/code/discernus/projects/wip/bolsonaro_2018`) is organized to reflect the Discernus workflow and facilitate easy navigation. While the exact structure may vary slightly, a typical arrangement is as follows:

```
bolsonaro_2018/
├── experiment_spec.<ext>               # Experiment definition
├── framework.md                        # Methodological framework
├── corpus.md                           # Corpus definition
├── corpus_manifest.<ext>               # List of corpus documents
├── final_synthesis_report.<ext>        # Main findings report
├── statistical_analysis.<ext>          # Aggregated statistical results
├── validation_report.<ext>             # Validation and QA report
├── run_context.<ext>                   # Environment and provenance details
├── corpus/
│   ├── document_1.<ext>                # Original corpus documents
│   ├── document_2.<ext>
│   └── ... (12 documents)
├── evidence_extraction/
│   ├── document_1.<ext>                # Extracted evidence per document
│   ├── document_2.<ext>
│   └── ... (12 artifacts)
├── score_extraction/
│   ├── document_1.<ext>                # Assigned scores per document
│   ├── document_2.<ext>
│   └── ... (12 artifacts)
├── composite_analysis/
│   ├── document_1.<ext>                # Comprehensive analysis per document
│   ├── document_2.<ext>
│   └── ... (12 artifacts)
└── marked_up_document/
    ├── document_1.<ext>                # Annotated documents
    ├── document_2.<ext>
    └── ... (12 artifacts)
```
*(Note: `<ext>` denotes the specific file extension, which may vary based on the Discernus implementation, e.g., `.json`, `.yaml`, `.csv`, `.pdf`, `.html`)*

## 6. Provenance and Reproducibility

The Discernus framework places a strong emphasis on provenance and reproducibility. This experiment captures several key artifacts to ensure that the entire analysis process is transparent and verifiable:

*   **`Run ID` and `Completion Date`**: Unique identifiers and timestamps for this specific execution.
*   **`experiment_spec`**: Documents the exact parameters and design choices.
*   **`framework.md`**: Provides the detailed methodological guidelines.
*   **`corpus.md` and `corpus_manifest`**: Precisely define the input data.
*   **`run_context`**: Records the computational environment, enabling others to recreate the setup.
*   **All intermediate artifacts**: Each step from `corpus_document` to `final_synthesis_report` is documented, allowing for a full audit trail.

Researchers and auditors can trace every finding back to its source evidence and the analytical steps taken, fostering trust and enabling independent verification.

## 7. Usage for Researchers and Auditors

To effectively navigate and understand this experiment's outputs:

1.  **Start with the `final_synthesis_report`**: This document provides the high-level conclusions and key findings.
2.  **Review `statistical_analysis`**: For quantitative insights and aggregated data.
3.  **Examine `framework.md` and `experiment_spec`**: To understand the methodology and design choices that underpin the analysis.
4.  **Verify the Corpus**: Consult `corpus.md` and `corpus_manifest` to confirm the documents included. Access the raw `corpus_document` files in the `corpus/` directory.
5.  **Deep Dive into Individual Documents**:
    *   For a comprehensive view of a single document's analysis, refer to its corresponding file in `composite_analysis/`.
    *   To see the specific evidence extracted, check `evidence_extraction/`.
    *   To review the scores assigned, look at `score_extraction/`.
    *   For visual verification of evidence within the original text, consult the `marked_up_document/` files.
6.  **Audit for Reproducibility**: Use the `run_context` artifact to understand the environment in which the experiment was conducted, aiding in potential replication efforts.
7.  **Check Validation**: Review the `validation_report` for information on quality assurance and data integrity.

## 8. Contact Information

For questions regarding this Discernus experiment or its outputs, please refer to the project documentation or contact the research team.

---