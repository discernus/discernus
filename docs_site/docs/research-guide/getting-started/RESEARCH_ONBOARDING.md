# Onboarding Guide for Researchers

Welcome to the Discernus project! This guide provides the "golden path" for a new researcher to get set up, understand our research workflow, and run their first experiment.

---

### **Phase 1: Orientation (The 10-Minute Overview)**

Your goal in this phase is to quickly get the "lay of the land" without being overwhelmed by technical details.

1.  **Start at the Documentation Site**: Begin by exploring the [**documentation website**](../../README.md). It provides the high-level mission and vision of the project.

2.  **Consult the Project Map**: From the homepage, use the **"Key Documents"** badges to navigate to the **[`Documentation Index`](../../docs/DOCUMENTATION_INDEX.md)**. This is your map to all project documentation. Spend a few minutes here to see what's available.

3.  **Learn the Rules of the Road**: The final orientation step is to read the **[`CONTRIBUTING.md`](../../docs/CONTRIBUTING.md)**. This gives you a high-level overview of our development philosophy before you create your first experiment.

---

### **Phase 2: Environment Setup (Getting Hands-On)**

This phase gets the platform running on your local machine so you can start your research.

1.  **Follow the Environment Guide**: The **[`DEV_ENVIRONMENT.md`](../../docs/platform-development/DEV_ENVIRONMENT.md)** provides the single source of truth for setting up your environment. **The Docker-based setup is strongly recommended.**

2.  **View the Documentation Website**: To view the project documentation locally, run the following command from the project root. This starts a live-reloading server, and any changes you make to the documentation files will be updated in your browser automatically.
    ```bash
    docker-compose up docs
    ```
    You can then access the documentation at [http://localhost:8000](http://localhost:8000).

3.  **Initialize Your Research Workspace**: The `research_workspaces` directory is where you will do all of your work. After setting up the Docker environment, run this script from the project root to create the necessary folder structure:
    ```bash
    python3 scripts/utilities/setup_research_workspace.py
    ```

---

### **Phase 3: Your First Contribution (The "Hello, World" Task)**

Your first task is to create a simple experiment to learn the end-to-end workflow.

1.  **Create a Test Experiment**: In your new `research_workspaces/june_2025_research_dev_workspace/experiments/` directory, create a new YAML file (e.g., `my_first_experiment.yaml`). You can use the example in the main project `README.md` as a starting point.

2.  **Update the Workspace Index**: After creating your experiment file, run the automated indexer script from the project root. This will automatically add your new experiment to the `README.md` in your workspace.
    ```bash
    python3 scripts/utilities/update_research_workspace_index.py
    ```
    This gives you immediate feedback that the system recognizes your work.

3.  **Run Your Experiment**: Use the `comprehensive_experiment_orchestrator.py` script to run your experiment.
    ```bash
    # From within the Docker container
    python scripts/applications/comprehensive_experiment_orchestrator.py research_workspaces/june_2025_research_dev_workspace/experiments/my_first_experiment.yaml
    ```

4.  **Submit a Pull Request**: To share your work, create a Pull Request. You will be greeted by our **PR Template**, which will guide you through the process of adding your experiment to the project.

---

**Congratulations! You have now completed the basic research workflow. You are ready to explore the existing frameworks and design your own experiments.** 