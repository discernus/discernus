# 04: Futures & Roadmap for the Discernus Platform

This document outlines the planned evolution of the Discernus platform, guided by our question-driven development methodology. Each phase builds upon the last, incrementally adding value and technical sophistication.

## Guiding Principles
- **Evolve, Don't "Big Bang":** We will not attempt to build the entire system at once. Features will be added as they are required to answer the next researcher question.
- **Introduce Complexity Only When Necessary:** Powerful technologies like `PostgreSQL` and `Celery` are part of the long-term vision, but they will only be implemented when the scale of the user's question demands them.
- **Preserve the Core IP:** The unique geometric visualization and the academic rigor of the frameworks remain the project's core assets. All architectural choices are in service of making this IP more accessible and powerful.

## Phase 2: Comparative Analysis

- **Driving Question:** *"I have the signature for Text A. Now, how does it compare directly to Text B using the same framework?"*
- **User Value:** Moves from single-point analysis to comparative insight, which is fundamental to research.
- **Technical Evolution:**
    - **State Management:** The application will need to "remember" the first analysis to compare it with the second. This is the first step toward a true persistence layer.
    - **Initial Persistence:** Implement a simple persistence strategy. This could start as an in-memory cache for a user session and evolve to a `SQLite` database, proving the database model before moving to PostgreSQL.
    - **API Enhancement:** Create a new `/compare` endpoint or enhance the `/analyze` endpoint to handle multiple texts.
    - **Visualization:** Leverage the existing comparison modes of the refactored `RebootPlotlyCircularVisualizer`.

## Phase 3: Group-Level Analysis & Batch Processing

- **Driving Question:** *"How does the average moral signature of this group of texts compare to the average signature of this other group?"*
- **User Value:** Enables true quantitative and qualitative analysis across corpora, unlocking the ability to publish findings.
- **Technical Evolution:**
    - **Full Database Implementation:** Migrate from SQLite to **PostgreSQL**. The schema will store all runs, signatures, centroids, and experiment metadata, becoming the single source of truth.
    - **Asynchronous Task Queue:** Implement **Celery** and **Redis**. Analyzing a whole corpus is a long-running task. Moving this work to a background task queue is essential for a responsive user experience. The API will now submit a batch job and return a job ID, with another endpoint to poll for results.
    - **Corpus Management:** Introduce a more formal system for managing and referencing collections of texts.

## Phase 4: Full Academic & Conversational Platform

- **Driving Question:** *"Let's design a new experiment, run it against these three corpora, and get a publication-ready replication package. And I'd like to do this via chat."*
- **User Value:** The platform becomes a full-fledged research assistant, capable of handling complex, multi-stage experiments from design to publication.
- **Technical Evolution:**
    - **Conversational UI:** Build a true chat interface on top of the robust backend API.
    - **DES Evolution:** Evolve the simple experiment file into the full `Discernus Experiment Specification (DES)`, allowing for complex experimental designs (multiple models, frameworks, etc.).
    - **User Accounts & Provenance:** Implement user accounts and permissions to manage access to experiments and results.
    - **Replication Package Exporter:** Create a module that can bundle all the data, code, and results for a given experiment into a shareable, reproducible package.

This phased approach allows us to deliver value at every step while building steadily towards the ambitious and powerful vision laid out in the original reboot documents. 