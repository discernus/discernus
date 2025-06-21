# Onboarding Guide for Platform Developers

Welcome to the Discernus team! This guide provides the "golden path" for a new platform developer to get set up, understand our engineering standards, and make their first contribution to the core application.

---

### **Phase 1: Orientation (The 30-Minute Overview)**

Your goal in this phase is to understand *how* and *why* our system is built the way it is.

1.  **Start at the Documentation Site**: Begin by exploring the [**documentation website**](../README.md) we've set up. It provides the high-level mission and vision. To view the project documentation locally, run the following command from the project root:
    ```bash
    docker-compose up docs
    ```
    You can then access the documentation at [http://localhost:8000](http://localhost:8000). This starts a live-reloading server, and any changes you make to the documentation files will be updated in your browser automatically.

2.  **Review the Project Map**: From the homepage, use the **"Key Documents"** badges to navigate to the **[`Documentation Index`](../docs/DOCUMENTATION_INDEX.md)**. This is your map to the entire project's knowledge base.

3.  **Learn the Rules of the Road**: Read the **[`CONTRIBUTING.md`](../docs/CONTRIBUTING.md)** file. It outlines the fundamental workflow for all contributions.

4.  **Understand Our Architecture**: This is the most critical step for a platform developer. Read the **[`CODE_ORGANIZATION_STANDARDS.md`](../docs/CODE_ORGANIZATION_STANDARDS.md)** to understand the strict separation between `production`, `experimental`, and `deprecated` code. This is the core of our development philosophy.

5.  **Browse the Architecture Diagrams**: Familiarize yourself with the system design by looking through the diagrams in the **[`architecture/`](../docs/platform-development/architecture/)** directory.

---

### **Phase 2: Environment Setup (Getting Hands-On)**

This phase gets the application running on your local machine.

1.  **Follow the Environment Guide**: The **[`DEV_ENVIRONMENT.md`](../docs/platform-development/DEV_ENVIRONMENT.md)** provides the single source of truth for setting up your environment. **The Docker-based setup is strongly recommended.**

2.  **Verify Documentation Access**: Ensure you can access the documentation website at [http://localhost:8000](http://localhost:8000) (started in Phase 1). If you encounter any issues with the Docker setup, refer to the troubleshooting section in the **[`DEV_ENVIRONMENT.md`](../docs/platform-development/DEV_ENVIRONMENT.md)** guide.

3.  **Initialize the Research Workspace**: Even as a platform developer, you need the research workspace for the application to run correctly. After setting up the Docker environment, run this script from the project root:
    ```bash
    python3 scripts/utilities/setup_research_workspace.py
    ```

---

### **Phase 3: Your First Contribution (The "Hello, World" Task)**

Your first task is designed to walk you through our full development and review cycle.

1.  **Find a Task**: Ask the project lead for a "good first issue." This is typically a small, well-defined task like fixing a minor bug, adding a unit test to an existing utility, or creating a new helper function.

2.  **Develop in the Right Place**: If you are adding a new feature, start in the `experimental/prototypes/` directory. If you are fixing a bug in existing `src/` code, you can work on it directly.

3.  **Write and Run Tests**: All code changes require tests. Add a corresponding unit test in the `tests/unit/` directory. Before committing, run the entire test suite to ensure you haven't caused any regressions.
    ```bash
    # Run all tests
    python3 tests/run_tests.py
    ```

4.  **Check Documentation Style**: Run the docstring linter to ensure your code is well-documented.
    ```bash
    # Run the docstring linter
    python3 -m pydocstyle src/
    ```

5.  **Submit a Pull Request**: When you create your Pull Request, you will be greeted by our **PR Template**. Follow the checklist to ensure your contribution is complete and ready for review. This is the final step in our "how we do things here" process. 