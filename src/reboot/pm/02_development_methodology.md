# 02: Development Methodology - Question-Driven Prioritization

This document outlines the core development methodology for the Discernus Reboot. Our process is designed to ensure we are always building something useful and that our technical implementation directly serves a clear research need.

## The Core Principle: Answer the Next Question

All development work is anchored around a sequence of "researcher questions." Each question represents a distinct, valuable capability that a researcher would want from the Discernus platform. As we do build solutions to answer the questions, we always take a step back to make sure that what we build and configure consitutes scalable platform infrastructure that can help answer all future similar questions, not just temporary scripting to get an answer to a narrowly scoped question as fast as possible.

This approach provides several key benefits:
- **Clarity of Purpose:** Every development cycle has a clear, non-technical goal.
- **Natural Scoping:** The work required to answer the current question defines the scope of the next release.
- **User-Centricity:** It forces us to think from the researcher's perspective at all times.
- **Incremental Value:** The platform becomes more useful with each question we answer.

As we build out the platform to answering plausible user questions, we will inevitably encounter concerns about project hygiene, development velocity, scalability, security, and documentation. We look for opportunities to address these problems at the right time, but we are careful not to jump too far ahead of present concerns. This requires careful consideration and planning, but that's what we're paid to do, so we strive to do it well.

## The Development Sequence

Our development is prioritized along the following sequence of questions:

### Question #1: The MVP (Complete)
> *"What is the moral signature of this single piece of text according to a specific framework, and what does that look like geometrically?"*

- **Status:** Implemented and delivered.
- **Capabilities:** Analysis of a single text against a self-contained experiment file, producing a shareable HTML visualization via the `/analyze` endpoint.

### Question #2: Comparative Analysis (Complete)
> *"I have the signature for Text A. Now, how does it compare directly to Text B using the same framework?"*

- **Status:** Complete.
- **Capabilities:** Direct comparison of two texts via the `/compare` endpoint, producing a unified visual report showing both signatures.

### Question #3: Group-Level Analysis (Complete)
> *"How does the average moral signature of this group of texts compare to the average signature of this other group?"*

- **Status:** Complete.
- **Capabilities:** 
    - Asynchronous batch analysis of text corpora via `/analyze-corpus`.
    - Comparison of job-based results via `/compare-groups`.
    - High-performance, direct comparison of text groups via `/compare-groups-direct`.
    - Calculates and visualizes the `centroid` for each group.
- **Note:** The current implementation uses a temporary file-based result store. This can be upgraded to a persistent `PostgreSQL` database in a future iteration.

### Question #4: Distance Metrics (Complete)
> *"What's the distance between the centroids of text A and text B?"*
> *"What's the distance between the average centroid position of text group A and text group B?"*

- **Status:** Complete.
- **Capabilities:**
    - The `Signature Engine` now includes a `calculate_distance` function.
    - The `/compare` endpoint response and report now include the distance between the two text centroids.
    - The `/compare-groups` and `/compare-groups-direct` endpoints and reports now include the distance between the two group centroids.

### Question #5: Statistical Comparison Infrastructure (Complete)
> *"Do different flagship cloud LLMs produce statistically similar results for a substantive text?"*

- **Status:** Complete.
- **Capabilities:**
    - ✅ **Multi-Model Analysis Pipeline**: Generic `/compare-statistical` endpoint handles multi-model, multi-framework, and multi-run comparisons.
    - ✅ **Advanced Statistical Methods**: Pluggable statistical method registry with geometric similarity and dimensional correlation analyzers.
    - ✅ **Production Database Schema**: Advanced V2 database schema with `AnalysisJobV2`, `AnalysisResultV2`, and `StatisticalComparison` tables.
    - ✅ **Concurrent Execution**: Parallel LLM analysis execution with comprehensive database persistence.
    - ✅ **Statistical Metrics**: Real-time calculation of mean distances, correlation matrices, and significance tests.
    - ✅ **Validated Results**: Successfully demonstrated with gpt-4o-mini vs gpt-3.5-turbo showing 0.0546 distance and 0.94 correlation.
    - 🔧 **Visual Reports**: Report generation infrastructure added, minor template rendering issue under investigation.

## Next Up: Extended Statistical Comparisons
> *"Do local models produce statistically similar results to flagship cloud LLMs?"*
> *"Do LLMs produce consistent results across multiple runs of the same experiment?"*

- **Status:** Next in the development queue.
- **Required Evolution:**
    - Extension of the statistical comparison framework to support local model integration.
    - Multi-run consistency analysis with temporal statistical methods.
    - Framework-to-framework comparison capabilities.

## Question Backlog
- Ceteris paribus, what's the difference between the way framework A based experiment 1 and framework B based experiment 2 analyzes text A?
- How do different prompt templates affect the statistical consistency of results within the same framework?
- What is the optimal sample size for detecting statistically significant differences between model behaviors?