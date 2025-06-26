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
- **Capabilities:** Analysis of a single text against a self-contained experiment file, producing a shareable HTML visualization.

### Question #2: Comparative Analysis (Next Up)
> *"I have the signature for Text A. Now, how does it compare directly to Text B using the same framework?"*

- **Status:** Next in the development queue.
- **Required Evolution:**
    - A mechanism to handle state (i.e., remembering the first analysis).
    - An API endpoint that can accept two texts for comparison.
    - Integration with the visualizer's built-in comparison modes.
    - *This will likely drive the introduction of a simple persistence layer (e.g., an in-memory cache or a simple database table).*

### Question #3: Group-Level Analysis (Future)
> *"How does the average moral signature of this group of texts compare to the average signature of this other group?"*

- **Status:** Post-comparative analysis.
- **Required Evolution:**
    - A robust corpus ingestion system to handle collections of texts.
    - An asynchronous task queue (`Celery`) to process batches of texts without blocking the UI.
    - A full database (`PostgreSQL`) to store all results for aggregation.
    - The ability to calculate and visualize a `centroid` for a group of signatures. 



##Question Backlog
- What's the distance between the centroids of text A and text B?
- What's the distance between the average centroid position of text group and text group B?
- What the average variance of LLM A and LLM B