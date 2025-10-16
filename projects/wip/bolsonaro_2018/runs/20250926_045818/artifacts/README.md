This README provides a comprehensive overview and guide for the `bolsonaro_2018` Discernus research experiment. It is designed to be self-contained, discoverable, and auditable, adhering to academic and professional standards.

---

# Discernus Research Experiment: bolsonaro_2018

## Table of Contents

1.  [Overview](#1-overview)
2.  [Experiment Design & Context](#2-experiment-design--context)
    *   [2.1. Framework Definition](#21-framework-definition)
    *   [2.2. Corpus Definition](#22-corpus-definition)
    *   [2.3. Document Set](#23-document-set)
3.  [Experiment Artifacts](#3-experiment-artifacts)
    *   [3.1. Artifact Inventory Summary](#31-artifact-inventory-summary)
    *   [3.2. Detailed Artifact Descriptions](#32-detailed-artifact-descriptions)
4.  [Directory Structure](#4-directory-structure)
5.  [Provenance & Reproducibility](#5-provenance--reproducibility)
6.  [Usage Instructions for Researchers & Auditors](#6-usage-instructions-for-researchers--auditors)
7.  [Contact & Support](#7-contact--support)

---

## 1. Overview

This document serves as a comprehensive README for the Discernus research experiment titled `bolsonaro_2018`. This experiment was conducted using the Discernus framework, a structured methodology designed for rigorous, auditable analysis of textual corpora, often in contexts requiring evidence extraction, scoring, and synthesis.

The primary objective of this experiment was to apply a defined analytical framework to a specific corpus of documents, generating a series of structured artifacts that capture the entire analytical process from initial document ingestion to final synthesis.

*   **Experiment Name:** `bolsonaro_2018`
*   **Run ID:** `bolsonaro_2018_20250926_005818`
*   **Completion Date:** `2025-09-26T04:58:18.192079+00:00`
*   **Root Directory:** `/Volumes/code/discernus/projects/wip/bolsonaro_2018`

---

## 2. Experiment Design & Context

This section outlines the foundational components that define the scope and methodology of the `bolsonaro_2018` experiment.

### 2.1. Framework Definition

The analytical methodology applied in this experiment is defined by the `framework.md` file. This document specifies the criteria, categories, and rules used for evidence extraction, scoring, and synthesis. It is crucial for understanding the analytical lens through which the corpus was examined.

*   **Reference:** [framework.md](framework.md)

### 2.2. Corpus Definition

The set of documents analyzed in this experiment is derived from the corpus defined in `corpus.md`. This file typically outlines the source, scope, and selection criteria for the documents included in the study.

*   **Reference:** [corpus.md](corpus.md)

### 2.3. Document Set

This experiment processed a total of **12** individual documents. These documents are the primary units of analysis, and all subsequent artifacts are directly or indirectly derived from their content.

---

## 3. Experiment Artifacts

The Discernus framework generates a structured set of artifacts at various stages of the analytical process. These artifacts ensure transparency, auditability, and reproducibility of the research. Each artifact type represents a distinct output or intermediate step in the experiment workflow.

### 3.1. Artifact Inventory Summary

| Artifact Type            | Count | Description                                                                    |
| :----------------------- | :---- | :----------------------------------------------------------------------------- |
| `experiment_spec`        | 1     | Configuration and parameters for the experiment run.                           |
| `framework`              | 1     | The analytical framework definition used for this run.                         |
| `corpus_manifest`        | 1     | Manifest of documents included in the corpus for this run.                     |
| `corpus_document`        | 12    | Raw content of each document in the corpus.                                    |
| `composite_analysis`     | 12    | Aggregated analysis results for each document.                                 |
| `evidence_extraction`    | 12    | Specific evidence extracted from each document according to the framework.     |
| `score_extraction`       | 12    | Scores assigned based on extracted evidence for each document.                 |
| `marked_up_document`     | 12    | Documents with embedded annotations and extracted evidence.                    |
| `statistical_analysis`   | 1     | Aggregate statistical findings across all documents.                           |
| `final_synthesis_report` | 1     | Comprehensive report summarizing the experiment's findings.                    |
| `run_context`            | 1     | Metadata and environmental context of the experiment run.                      |

### 3.2. Detailed Artifact Descriptions

#### `experiment_spec` (1 artifact)
This artifact contains the precise configuration and parameters used to initiate and execute the `bolsonaro_2018` experiment. It captures settings such as input paths, output formats, and any specific flags or options applied during the run. It is critical for understanding the exact setup of the experiment.

#### `framework` (1 artifact)
This artifact is a copy of the `framework.md` file used for this specific experiment run. It defines the analytical model, including categories, criteria, and scoring rubrics, against which the corpus documents were evaluated. It is the blueprint for the analysis.

#### `corpus_manifest` (1 artifact)
This artifact lists all documents included in the `bolsonaro_2018` corpus, typically with their unique identifiers, original source paths, and any relevant metadata. It serves as a definitive index of the documents analyzed. This is a copy of the `corpus.md` file used for this specific experiment run.

#### `corpus_document` (12 artifacts)
These artifacts represent the raw, original content of each document processed in the experiment. Each `corpus_document` corresponds to one of the 12 documents from the corpus, preserved in its original or standardized format. These are the primary inputs to the analytical process.

#### `composite_analysis` (12 artifacts)
For each document, this artifact consolidates all analytical outputs, including extracted evidence, assigned scores, and any other document-specific findings, into a single, structured representation. It provides a holistic view of the analysis for an individual document.

#### `evidence_extraction` (12 artifacts)
These artifacts contain the specific textual segments or data points identified and extracted from each `corpus_document` according to the rules defined in the `framework`. Each extracted piece of evidence is typically linked to a specific criterion or category.

#### `score_extraction` (12 artifacts)
These artifacts record the scores or ratings assigned to each document (or specific aspects within it) based on the `evidence_extraction` and the scoring rubrics defined in the `framework`. They quantify the findings for each document.

#### `marked_up_document` (12 artifacts)
These artifacts are versions of the `corpus_document` with embedded annotations. They visually highlight the extracted evidence and potentially other analytical insights directly within the document's text, making the analysis transparent and easy to review.

#### `statistical_analysis` (1 artifact)
This artifact presents an aggregate statistical summary of the findings across all 12 documents. It includes quantitative metrics, distributions, and potentially visualizations derived from the `score_extraction` and `composite_analysis` artifacts, providing a high-level overview of the experiment's results.

#### `final_synthesis_report` (1 artifact)
This is the culminating report of the `bolsonaro_2018` experiment. It synthesizes the findings from the `statistical_analysis`, `composite_analysis`, and other artifacts into a coherent narrative, drawing conclusions and discussing implications based on the analytical framework.

#### `run_context` (1 artifact)
This artifact captures the complete environmental context in which the experiment was executed. This includes software versions, system configurations, timestamps, and other metadata essential for ensuring the reproducibility and auditability of the experiment. It provides critical provenance information.

---

## 4. Directory Structure

The experiment's root directory (`/Volumes/code/discernus/projects/wip/bolsonaro_2018`) is organized to provide clear access to all generated artifacts and foundational documents.

```
/Volumes/code/discernus/projects/wip/bolsonaro_2018/
├── framework.md                      # The analytical framework definition (original input)
├── corpus.md                         # The corpus manifest definition (original input)
├── README.md                         # This document
├── artifacts/
│   ├── experiment_spec/              # Contains experiment_spec.json
│   ├── framework/                    # Contains framework.json (processed framework artifact)
│   ├── corpus_manifest/              # Contains corpus_manifest.json (processed corpus artifact)
│   ├── corpus_document/              # Contains 12 raw document files (e.g., doc_id_1.txt, doc_id_2.pdf)
│   ├── composite_analysis/           # Contains 12 composite analysis files (e.g., doc_id_1.json)
│   ├── evidence_extraction/          # Contains 12 evidence extraction files (e.g., doc_id_1.json)
│   ├── score_extraction/             # Contains 12 score extraction files (e.g., doc_id_1.json)
│   ├── marked_up_document/           # Contains 12 marked-up document files (e.g., doc_id_1.html or .pdf)
│   ├── statistical_analysis/         # Contains statistical_analysis.json or .csv
│   ├── final_synthesis_report/       # Contains final_synthesis_report.md or .pdf
│   └── run_context/                  # Contains run_context.json
└── logs/                             # (Optional) Directory for experiment logs
```

Each artifact type listed in Section 3.1 typically resides in its own subdirectory under `artifacts/`, named after the artifact type. Individual document-specific artifacts (e.g., `corpus_document`, `composite_analysis`) are named using their unique document identifiers within their respective subdirectories.

---

## 5. Provenance & Reproducibility

The Discernus framework is designed with a strong emphasis on provenance and reproducibility. Every artifact generated in this experiment contributes to a complete audit trail.

*   **Run ID (`bolsonaro_2018_20250926_005818`):** This unique identifier links all artifacts to a specific execution of the experiment.
*   **`run_context` artifact:** This artifact (located in `artifacts/run_context/run_context.json`) provides a snapshot of the execution environment, including software versions, dependencies, and system configuration. This is crucial for replicating the exact conditions of the experiment.
*   **Timestamped Completion:** The `Completion Date` ensures that the exact time of the experiment's conclusion is recorded, aiding in chronological tracking.
*   **Explicit Framework and Corpus:** The `framework.md` and `corpus.md` files (and their artifact copies in `artifacts/framework/` and `artifacts/corpus_manifest/`) explicitly define the inputs and methodology, allowing for independent verification or re-application of the analysis.
*   **Granular Artifacts:** The detailed breakdown into `evidence_extraction`, `score_extraction`, and `composite_analysis` artifacts for each document allows researchers and auditors to trace every step of the analytical process from raw document to final score.

To reproduce this experiment, one would ideally use the Discernus framework with the `experiment_spec` and the original `framework.md` and `corpus.md` files, ensuring the environment matches the specifications in `run_context`.

---

## 6. Usage Instructions for Researchers & Auditors

This section provides guidance on navigating and interpreting the contents of this experiment directory.

1.  **Start with the Overview:** Begin by reviewing this `README.md` file for a high-level understanding of the experiment.
2.  **Examine the Core Definitions:**
    *   **Framework:** Read `framework.md` to understand the analytical criteria and scoring logic.
    *   **Corpus:** Review `corpus.md` to understand the source and selection of documents.
3.  **Review the Final Report:** Access the `final_synthesis_report` artifact (typically in `artifacts/final_synthesis_report/final_synthesis_report.md` or `.pdf`) for the experiment's main conclusions and discussion.
4.  **Inspect Aggregate Statistics:** Consult the `statistical_analysis` artifact (e.g., `artifacts/statistical_analysis/statistical_analysis.json`) for quantitative summaries and overall trends.
5.  **Dive into Individual Document Analysis:**
    *   Navigate to `artifacts/composite_analysis/` to find the comprehensive analysis for each of the 12 documents. These JSON files provide a structured summary.
    *   To see the raw document content, go to `artifacts/corpus_document/`.
    *   To see how evidence was extracted, check `artifacts/evidence_extraction/`.
    *   To understand the scores assigned, review `artifacts/score_extraction/`.
    *   For a visual representation of the analysis directly on the document, examine the `marked_up_document` artifacts (e.g., `artifacts/marked_up_document/doc_id_X.html`).
6.  **Verify Provenance:** Review `artifacts/run_context/run_context.json` to understand the environment and exact parameters of this experiment run.
7.  **Consult `experiment_spec`:** For the precise configuration used to launch this experiment, refer to `artifacts/experiment_spec/experiment_spec.json`.

**Note:** A basic understanding of the Discernus framework and its output formats (primarily JSON for structured data, Markdown/HTML/PDF for reports) is assumed for detailed artifact inspection.

---

## 7. Contact & Support

For questions regarding the Discernus framework or this specific experiment, please refer to the Discernus project documentation or contact the research team responsible for this experiment.

---