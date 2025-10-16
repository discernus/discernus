# Discernus Research Experiment: `bolsonaro_2018`

## Table of Contents

1.  [Experiment Overview](#1-experiment-overview)
2.  [Experiment Details](#2-experiment-details)
3.  [Artifact Inventory and Descriptions](#3-artifact-inventory-and-descriptions)
    *   [Core Experiment Definitions](#31-core-experiment-definitions)
    *   [Corpus and Document Artifacts](#32-corpus-and-document-artifacts)
    *   [Analysis and Extraction Artifacts](#33-analysis-and-extraction-artifacts)
    *   [Summary and Reporting Artifacts](#34-summary-and-reporting-artifacts)
    *   [Contextual Artifacts](#35-contextual-artifacts)
4.  [Directory Structure](#4-directory-structure)
5.  [Provenance Information](#5-provenance-information)
6.  [Usage for Researchers and Auditors](#6-usage-for-researchers-and-auditors)
    *   [Navigating the Experiment](#61-navigating-the-experiment)
    *   [Understanding the Analysis](#62-understanding-the-analysis)
    *   [Reproducibility and Extension](#63-reproducibility-and-extension)
7.  [Contact and Support](#7-contact-and-support)

---

## 1. Experiment Overview

This document serves as a comprehensive README file for the Discernus research experiment named `bolsonaro_2018`. It provides a detailed overview of the experiment's purpose, structure, generated artifacts, and guidance for researchers and auditors seeking to understand, verify, or extend its findings.

The experiment was conducted using the Discernus framework, a structured methodology for systematic analysis of textual corpora. This particular run focuses on a corpus of 12 documents, likely related to the 2018 political landscape involving Jair Bolsonaro, as indicated by the experiment's name.

---

## 2. Experiment Details

*   **Experiment Name:** `bolsonaro_2018`
*   **Discernus Framework Definition:** The analytical framework used for this experiment is detailed in [framework.md](framework.md). This document outlines the specific criteria, categories, and methodologies applied during the analysis.
*   **Corpus Definition:** The source and selection criteria for the documents analyzed in this experiment are described in [corpus.md](corpus.md).
*   **Number of Documents Analyzed:** 12
*   **Unique Run Identifier (Run ID):** `bolsonaro_2018_20250926_000043`
*   **Completion Date:** `2025-09-26T04:00:43.889741+00:00`
*   **Experiment Directory Path:** `/Volumes/code/discernus/projects/wip/bolsonaro_2018`

---

## 3. Artifact Inventory and Descriptions

This section details each type of artifact generated during the `bolsonaro_2018` experiment run, explaining its purpose and content. The quantities listed indicate the number of files or records of that artifact type.

### 3.1. Core Experiment Definitions

*   **`experiment_spec`** (1 artifact)
    *   **Description:** This artifact contains the complete specification of the experiment, including its configuration parameters, objectives, and any specific instructions or settings that guided the Discernus run. It acts as the blueprint for the entire experiment.

### 3.2. Corpus and Document Artifacts

*   **`framework`** (1 artifact)
    *   **Description:** This artifact is a copy of the Discernus framework definition (`framework.md`) used for this specific experiment run. It defines the analytical schema, categories, and rules applied to the corpus.
*   **`corpus_manifest`** (1 artifact)
    *   **Description:** This artifact provides a comprehensive manifest of all documents included in the `bolsonaro_2018` corpus. It typically lists document identifiers, original source paths, and potentially metadata such as publication date, author, or URL.
*   **`corpus_document`** (12 artifacts)
    *   **Description:** These artifacts represent the raw or pre-processed textual content of each of the 12 documents analyzed in the experiment. Each file corresponds to one document from the corpus.

### 3.3. Analysis and Extraction Artifacts

*   **`composite_analysis`** (12 artifacts)
    *   **Description:** For each document, this artifact consolidates the results of various analytical steps performed by the Discernus framework. It provides a structured, comprehensive view of the document's analysis, often including aggregated scores, extracted entities, and relationships.
*   **`evidence_extraction`** (12 artifacts)
    *   **Description:** These artifacts contain specific textual segments or data points extracted from each document that were identified as evidence according to the Discernus framework's criteria. Each extraction is typically linked to a specific analytical category or claim.
*   **`score_extraction`** (12 artifacts)
    *   **Description:** These artifacts record the quantitative scores or ratings assigned to various aspects, claims, or categories within each document, based on the rules defined in the Discernus framework. These scores contribute to the overall evaluation of the document.
*   **`marked_up_document`** (12 artifacts)
    *   **Description:** These artifacts are versions of the original `corpus_document` files, but with annotations, highlights, or other markup directly embedded. This markup visually indicates the locations of extracted evidence, scored sections, or other analytical findings within the text.

### 3.4. Summary and Reporting Artifacts

*   **`statistical_analysis`** (1 artifact)
    *   **Description:** This artifact presents an aggregated statistical summary and analysis across all 12 documents in the corpus. It may include distributions of scores, frequencies of extracted evidence types, correlations, and other quantitative insights derived from the entire experiment.
*   **`final_synthesis_report`** (1 artifact)
    *   **Description:** This is the conclusive report of the `bolsonaro_2018` experiment. It synthesizes the findings from the `composite_analysis` and `statistical_analysis` artifacts, providing interpretations, conclusions, and potentially recommendations based on the experiment's objectives.

### 3.5. Contextual Artifacts

*   **`run_context`** (1 artifact)
    *   **Description:** This artifact captures the environmental details, software versions, system configurations, and any other relevant contextual information present at the time the experiment was executed. This is crucial for ensuring reproducibility and debugging.

---

## 4. Directory Structure

The experiment's directory (`/Volumes/code/discernus/projects/wip/bolsonaro_2018`) is organized to ensure all artifacts are logically grouped and easily discoverable. The typical structure is as follows:

```
bolsonaro_2018/
├── README.md                 <- This file
├── framework.md              <- Discernus framework definition
├── corpus.md                 <- Corpus definition and selection criteria
├── artifacts/                <- Directory containing all generated artifacts
│   ├── experiment_spec/      <- Contains the experiment specification
│   │   └── bolsonaro_2018_spec.json  (example filename)
│   ├── corpus_manifest/      <- Contains the manifest of all corpus documents
│   │   └── corpus_manifest.json
│   ├── corpus_document/      <- Contains the 12 raw corpus documents
│   │   ├── doc_001.txt
│   │   └── ... (10 more files)
│   │   └── doc_012.txt
│   ├── composite_analysis/   <- Contains the composite analysis for each document
│   │   ├── doc_001_composite.json
│   │   └── ... (10 more files)
│   │   └── doc_012_composite.json
│   ├── evidence_extraction/  <- Contains extracted evidence for each document
│   │   ├── doc_001_evidence.json
│   │   └── ... (10 more files)
│   │   └── doc_012_evidence.json
│   ├── score_extraction/     <- Contains extracted scores for each document
│   │   ├── doc_001_scores.json
│   │   └── ... (10 more files)
│   │   └── doc_012_scores.json
│   ├── marked_up_document/   <- Contains marked-up versions of each document
│   │   ├── doc_001_markedup.html (or .txt)
│   │   └── ... (10 more files)
│   │   └── doc_012_markedup.html (or .txt)
│   ├── statistical_analysis/ <- Contains the overall statistical analysis
│   │   └── statistical_report.json
│   ├── final_synthesis_report/ <- Contains the final synthesis report
│   │   └── synthesis_report.pdf (or .md, .json)
│   └── run_context/          <- Contains the run context information
│       └── run_context.json
└── logs/                     <- Optional: Directory for execution logs
    └── run_log_20250926.txt
```

---

## 5. Provenance Information

This experiment was executed under the following specific conditions, ensuring traceability and aiding in reproducibility:

*   **Run ID:** `bolsonaro_2018_20250926_000043`
*   **Completion Timestamp:** `2025-09-26T04:00:43.889741+00:00` (UTC)
*   **Execution Environment:** The experiment was run within the directory `/Volumes/code/discernus/projects/wip/bolsonaro_2018`. Detailed environment specifics (e.g., Discernus version, operating system, dependencies) are recorded in the `run_context` artifact.
*   **Framework Version:** The specific version of the Discernus framework used is implicitly captured within the `run_context` artifact and explicitly defined by the `framework.md` file.

This provenance information is critical for auditing the experiment, verifying its results, and understanding the conditions under which the analysis was performed.

---

## 6. Usage for Researchers and Auditors

This section provides guidance on how to effectively navigate and utilize the artifacts generated by the `bolsonaro_2018` experiment.

### 6.1. Navigating the Experiment

*   **Start with the `final_synthesis_report`:** For a high-level understanding of the experiment's findings and conclusions, begin by reviewing the `final_synthesis_report` artifact.
*   **Review `experiment_spec`, `framework.md`, and `corpus.md`:** To understand the methodology, analytical criteria, and data sources, consult these foundational documents.
*   **Explore `statistical_analysis`:** For quantitative summaries and trends across the entire corpus, examine the `statistical_analysis` artifact.
*   **Dive into individual documents:** To understand the analysis of a specific document, locate its corresponding `corpus_document`, `composite_analysis`, `evidence_extraction`, `score_extraction`, and `marked_up_document` artifacts within their respective subdirectories.

### 6.2. Understanding the Analysis

*   **`composite_analysis`:** These files provide a structured, machine-readable breakdown of all analytical outputs for a given document. They are ideal for programmatic access and detailed review.
*   **`evidence_extraction` and `score_extraction`:** These artifacts isolate the specific data points and quantitative assessments, allowing for focused examination of how conclusions were reached.
*   **`marked_up_document`:** These files offer a human-readable, visual representation of the analysis directly on the source text, making it easy to see what parts of the document contributed to specific findings.

### 6.3. Reproducibility and Extension

*   **Reproducibility:** The `experiment_spec` and `run_context` artifacts contain the necessary information to re-run the experiment, provided the Discernus framework and its dependencies are correctly configured. Researchers can use this to verify results or test modifications.
*   **Extension:** This experiment serves as a baseline. Researchers can extend this work by:
    *   Modifying the `framework.md` to explore different analytical dimensions.
    *   Expanding the `corpus.md` to include more documents.
    *   Developing new analysis modules within the Discernus framework and applying them to this corpus.

---

## 7. Contact and Support

For questions regarding the Discernus framework or this specific experiment, please refer to the Discernus project documentation or contact the research team responsible for this experiment via the primary project communication channels.