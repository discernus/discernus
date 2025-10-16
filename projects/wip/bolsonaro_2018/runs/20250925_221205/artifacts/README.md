# README: Discernus Experiment - bolsonaro_2018

## Table of Contents
1.  [Experiment Overview](#1-experiment-overview)
2.  [Purpose and Scope](#2-purpose-and-scope)
3.  [Experiment Details](#3-experiment-details)
4.  [Core Components](#4-core-components)
    *   [4.1. Analytical Framework](#41-analytical-framework)
    *   [4.2. Corpus](#42-corpus)
5.  [Artifact Inventory and Descriptions](#5-artifact-inventory-and-descriptions)
    *   [5.1. `experiment_spec`](#51-experiment_spec)
    *   [5.2. `framework`](#52-framework)
    *   [5.3. `corpus_manifest`](#53-corpus_manifest)
    *   [5.4. `corpus_document`](#54-corpus_document)
    *   [5.5. `composite_analysis`](#55-composite_analysis)
    *   [5.6. `evidence_extraction`](#56-evidence_extraction)
    *   [5.7. `score_extraction`](#57-score_extraction)
    *   [5.8. `marked_up_document`](#58-marked_up_document)
    *   [5.9. `statistical_analysis`](#59-statistical_analysis)
    *   [5.10. `final_synthesis_report`](#510-final_synthesis_report)
    *   [5.11. `run_context`](#511-run_context)
6.  [Directory Structure](#6-directory-structure)
7.  [Provenance and Reproducibility](#7-provenance-and-reproducibility)
8.  [Usage Instructions for Researchers and Auditors](#8-usage-instructions-for-researchers-and-auditors)
9.  [Contact and Support](#9-contact-and-support)

---

## 1. Experiment Overview

This document serves as a comprehensive README for the Discernus research experiment named `bolsonaro_2018`. It provides a detailed overview of the experiment's components, generated artifacts, directory structure, and guidance for researchers and auditors seeking to understand, verify, or reproduce the findings.

The experiment systematically applied a defined analytical framework to a specific corpus of documents, generating a rich set of intermediate and final artifacts.

## 2. Purpose and Scope

The `bolsonaro_2018` experiment aimed to [**Insert specific research question or objective here, e.g., "analyze the framing of political discourse surrounding Jair Bolsonaro during the 2018 Brazilian presidential election."**]. This README facilitates the discoverability and interpretability of all generated data and reports, ensuring transparency and adherence to research best practices.

## 3. Experiment Details

*   **Experiment Name:** `bolsonaro_2018`
*   **Run ID:** `bolsonaro_2018_20250925_181205`
*   **Completion Date:** `2025-09-25T22:12:05.274689+00:00`
*   **Root Directory:** `/Volumes/code/discernus/projects/wip/bolsonaro_2018`
*   **Number of Documents Processed:** 12

## 4. Core Components

The experiment's foundation rests upon two primary components: the analytical framework and the corpus.

### 4.1. Analytical Framework

The analytical framework defines the methodology, rules, criteria, and scoring mechanisms used to analyze the corpus documents. It is crucial for understanding how evidence was extracted and interpreted.

*   **File:** `framework.md`
*   **Description:** This Markdown file details the specific Discernus framework applied in this experiment. It outlines the analytical categories, definitions, and any specific instructions for evidence extraction and scoring.

### 4.2. Corpus

The corpus comprises the collection of source materials subjected to analysis.

*   **File:** `corpus.md`
*   **Description:** This Markdown file provides an overview of the corpus, including its scope, selection criteria, and any general characteristics of the documents included.

## 5. Artifact Inventory and Descriptions

This section details each type of artifact generated during the `bolsonaro_2018` experiment, along with its purpose and quantity.

### 5.1. `experiment_spec` (1 artifact)
*   **Description:** Contains the initial specifications and configuration parameters that defined how the experiment was set up and executed. This artifact is critical for understanding the experiment's design choices.

### 5.2. `framework` (1 artifact)
*   **Description:** The complete analytical framework used for the experiment. This is the definitive version of the methodology applied, detailing categories, indicators, and scoring rubrics. (See also [4.1. Analytical Framework](#41-analytical-framework)).

### 5.3. `corpus_manifest` (1 artifact)
*   **Description:** A comprehensive list or manifest of all documents included in the corpus, often including metadata such as document IDs, titles, sources, and original URLs. It serves as an index for the `corpus_document` artifacts.

### 5.4. `corpus_document` (12 artifacts)
*   **Description:** The raw, original source documents that constitute the corpus. Each artifact represents a single document that was subjected to analysis. These are the primary data inputs for the experiment.

### 5.5. `composite_analysis` (12 artifacts)
*   **Description:** For each `corpus_document`, this artifact provides a consolidated view of all analytical findings. It aggregates extracted evidence, scores, and potentially other document-specific insights into a single, structured output.

### 5.6. `evidence_extraction` (12 artifacts)
*   **Description:** Contains the specific textual snippets or data points extracted from each `corpus_document` that serve as direct evidence for the analytical categories defined in the `framework`. Each artifact corresponds to the evidence extracted from one document.

### 5.7. `score_extraction` (12 artifacts)
*   **Description:** Records the scores assigned to each `corpus_document` based on the extracted evidence and the rules specified in the `framework`. These scores quantify the presence or absence, or intensity, of specific analytical indicators.

### 5.8. `marked_up_document` (12 artifacts)
*   **Description:** Versions of the `corpus_document` with annotations, highlights, or other markings indicating where evidence was found, what categories it relates to, or specific analytical observations. These are invaluable for direct verification.

### 5.9. `statistical_analysis` (1 artifact)
*   **Description:** The aggregated statistical findings across the entire corpus. This artifact presents quantitative summaries, trends, and patterns derived from the `score_extraction` data, often including charts, graphs, and statistical tests.

### 5.10. `final_synthesis_report` (1 artifact)
*   **Description:** The primary output report of the experiment, summarizing the overall findings, conclusions, and interpretations. It synthesizes insights from the `statistical_analysis` and provides a narrative explanation of the experiment's results.

### 5.11. `run_context` (1 artifact)
*   **Description:** Captures the environmental and execution details of the experiment run. This includes software versions, system configurations, timestamps, and any other parameters relevant to the experiment's execution, crucial for reproducibility.

## 6. Directory Structure

The experiment's artifacts are organized within the root directory `/Volumes/code/discernus/projects/wip/bolsonaro_2018`. While the exact subdirectory names might vary based on the Discernus implementation, a typical structure would be:

```
bolsonaro_2018/
├── README.md                     # This file
├── framework.md                  # Overview of the analytical framework
├── corpus.md                     # Overview of the corpus
├── artifacts/
│   ├── experiment_spec/          # Contains the experiment specification file
│   │   └── bolsonaro_2018_spec.json
│   ├── framework/                # Contains the detailed framework file
│   │   └── framework_definition.json
│   ├── corpus_manifest/          # Contains the manifest of all corpus documents
│   │   └── corpus_manifest.json
│   ├── corpus_document/          # Individual source documents (e.g., PDFs, text files)
│   │   ├── doc_001.pdf
│   │   ├── doc_002.txt
│   │   └── ... (12 documents)
│   ├── composite_analysis/       # Aggregated analysis results per document
│   │   ├── doc_001_composite.json
│   │   └── ... (12 files)
│   ├── evidence_extraction/      # Extracted evidence snippets per document
│   │   ├── doc_001_evidence.json
│   │   └── ... (12 files)
│   ├── score_extraction/         # Scores assigned per document
│   │   ├── doc_001_scores.json
│   │   └── ... (12 files)
│   ├── marked_up_document/       # Documents with annotations
│   │   ├── doc_001_marked_up.pdf
│   │   └── ... (12 files)
│   ├── statistical_analysis/     # Overall statistical findings
│   │   └── statistical_report.json
│   ├── final_synthesis_report/   # The main synthesis report
│   │   └── final_synthesis.pdf
│   └── run_context/              # Details about the experiment run environment
│       └── run_context.json
```

## 7. Provenance and Reproducibility

This experiment is designed with reproducibility and auditability in mind:

*   **Run ID (`bolsonaro_2018_20250925_181205`):** A unique identifier for this specific execution of the experiment.
*   **Completion Date (`2025-09-25T22:12:05.274689+00:00`):** Provides a precise timestamp of when the experiment concluded.
*   **`framework` artifact:** The definitive methodological blueprint. Any re-run using this framework on the same corpus should yield comparable results.
*   **`corpus_manifest` and `corpus_document` artifacts:** Ensure that the exact input data used for the experiment is preserved and identifiable.
*   **`run_context` artifact:** Captures the computational environment, including software versions and system details, which are crucial for replicating the exact conditions of the original run.

Researchers and auditors can trace the entire analytical process from the raw documents (`corpus_document`) through evidence extraction (`evidence_extraction`), scoring (`score_extraction`), and aggregation (`composite_analysis`), up to the final reports (`statistical_analysis`, `final_synthesis_report`).

## 8. Usage Instructions for Researchers and Auditors

To effectively navigate and understand this experiment's output:

1.  **Start with the `final_synthesis_report`:** This PDF or Markdown file provides the high-level conclusions and narrative of the experiment.
2.  **Review `statistical_analysis`:** For quantitative insights and aggregated data, consult the statistical report.
3.  **Examine `framework.md` and the `framework` artifact:** To understand the methodology applied, including definitions, categories, and scoring rules.
4.  **Consult `corpus.md` and `corpus_manifest`:** To understand the source materials and their characteristics.
5.  **Drill down into individual documents:**
    *   Locate specific `corpus_document` files to view the original content.
    *   Refer to `marked_up_document` to see how evidence was identified and annotated within the original text.
    *   Review `evidence_extraction` and `score_extraction` for detailed, document-specific findings.
    *   The `composite_analysis` artifact provides a convenient summary for each document.
6.  **Verify Provenance:** Use the `run_context` artifact to understand the environment in which the experiment was conducted, aiding in reproducibility efforts.
7.  **Tools:** Standard text editors, JSON viewers, and PDF readers will be sufficient to inspect most artifacts.

## 9. Contact and Support

For questions, clarifications, or further information regarding the `bolsonaro_2018` Discernus experiment, please contact [**Insert Contact Information Here, e.g., "the Discernus Research Team" or "researcher@example.com"**].