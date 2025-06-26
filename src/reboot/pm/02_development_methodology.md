# 02: Development Methodology - Question-Driven Prioritization

This document outlines the core development methodology for the Discernus Reboot. Our process is designed to ensure we are always building something useful and that our technical implementation directly serves a clear research need.

## The Core Principle: Answer the Next Question

All development work is anchored around a sequence of "researcher questions." Each question represents a distinct, valuable capability that a researcher would want from the Discernus platform.

This approach provides several key benefits:
- **Clarity of Purpose:** Every development cycle has a clear, non-technical goal.
- **Natural Scoping:** The work required to answer the current question defines the scope of the next release.
- **User-Centricity:** It forces us to think from the researcher's perspective at all times.
- **Incremental Value:** The platform becomes more useful with each question we answer.

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

## Next Up: Multi-LLM Comparison
> *"Do different flagship cloud LLMs produce statistically similar results for a substantive text?"*

- **Status:** Next in the development queue.
- **Required Evolution:**
    - A new endpoint, likely `/compare-models`, that accepts a single text and a list of models to compare.
    - A new report type that visualizes the signatures from multiple models on a single chart.
    - A mechanism to calculate and display statistical similarity (e.g., variance in centroid positions).

## Question Backlog
- Do local models produce statistically similar results to flagship cloud LLMs?
- Do LLMs produce statistically significant runs across multipe runs of the same experiment?
- Ceteris parabis, what's the difference between the way framework A based experiment 1 and framework B based experiment 2 analyzes text A?