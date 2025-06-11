# Plan: CLI Interfaces Solidification (v2.1)

## 🎯 Objective
Develop and refine command-line interface (CLI) tools to provide a robust, user-friendly, and efficient way for academic reviewers and researchers (including non-developers) to interact with the Narrative Gravity Wells platform. This includes simplifying common workflows, enabling batch processing, and ensuring clear feedback.

## 🚀 Key Tasks

### 1. **Identify and Prioritize Core CLI Workflows**
- **1.1. User Story Mapping:** Based on the primary research objectives (iterative experimentation, validation, comparative analysis), identify the most critical tasks that users would perform via CLI.
    - *Examples:* Running single-text analysis, running batch analysis on a corpus, managing framework configurations, setting up/checking the database, exporting results.
- **1.2. Prioritization:** Prioritize CLI commands based on frequency of use and impact on research velocity.

### 2. **Develop/Refine CLI Commands**
- **2.1. Consistent Naming & Structure:** Establish a consistent naming convention and argument structure for all CLI commands to enhance usability.
    - *Action:* Review `launch.py` and scripts in `scripts/` for existing patterns.
- **2.2. Robust Error Handling:** Implement comprehensive error handling and provide clear, actionable error messages for all CLI commands.
    - *Action:* Ensure errors point to relevant documentation or troubleshooting steps.
- **2.3. Progress Indicators & Logging:** For long-running tasks (e.g., batch analysis), implement progress indicators and detailed logging to the console.
- **2.4. Batch Processing Capabilities:** Enhance existing or create new CLI commands to support batch processing of texts, frameworks, and experiments.
    - *Action:* Ensure input/output formats are clear and consistent (e.g., support for CSV/JSONL for bulk operations).

### 3. **Integrate with Core Backend Functionality**
- **3.1. API Client Integration:** Ensure CLI commands leverage the existing FastAPI backend and analysis engine for consistent behavior with the UI.
    - *Action:* Review `src/narrative_gravity/cli/` for existing CLI entry points.
- **3.2. Configuration Management:** Enable CLI commands to easily select and manage framework configurations and prompt templates (e.g., by name or version).

### 4. **Documentation and Examples**
- **4.1. CLI Usage Guides:** Create dedicated documentation for each primary CLI command, including examples and explanations of arguments.
    - *Action:* Consider adding a `docs/cli/` directory for this purpose, or integrating into existing user guides.
- **4.2. Example Scripts:** Provide simple, runnable example scripts demonstrating common CLI workflows for academic users (e.g., in `examples/` directory).

## 🛠️ Tools & Commands
- `python launch.py --help` (to review existing flags)
- `python scripts/<script_name>.py --help`
- `argparse` (Python module for command-line argument parsing)
- `click` or `Typer` (consider for more advanced CLI development if needed)

## ✅ Validation Criteria
- [ ] All critical research workflows can be executed via CLI.
- [ ] CLI commands have consistent naming and argument structures.
- [ ] Error messages are clear, user-friendly, and provide actionable guidance.
- [ ] Long-running CLI tasks display progress and comprehensive logs.
- [ ] Batch processing functionality is robust and well-documented.
- [ ] CLI commands correctly interact with the database and analysis engine.
- [ ] Comprehensive documentation and runnable examples for all key CLI operations are available. 