# Development Environment Setup

This guide provides instructions for setting up a consistent and effective development environment for the Discernus project.

---

## 1. Local Python Environment (Traditional Setup)

### Quick Setup Commands

```bash
# 1. Activate virtual environment (run from project root)
source venv/bin/activate

# 2. Set up shell environment variables (for imports)
source scripts/setup_dev_env.sh

# 3. Verify imports work
python3 -c "from src.coordinate_engine import CoordinateEngine; print('✅ Imports working!')"
```

### IDE Configuration

#### VS Code Setup
Add to `.vscode/settings.json`:
```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.envFile": "${workspaceFolder}/.env",
    "python.analysis.extraPaths": [
        "${workspaceFolder}/src"
    ]
}
```

#### PyCharm Setup
1.  **File → Settings → Project → Python Interpreter**
2.  Select the virtual environment: `./venv/bin/python`
3.  **File → Settings → Project → Project Structure**
4.  Mark `src/` directory as "Sources Root"

---

## 2. Docker-Based Environment (Recommended)

Using Docker is the recommended approach for development. It ensures a consistent, isolated, and reproducible environment that matches production.

### Prerequisites
- Docker Desktop installed and running.

### Setup and Usage

```bash
# 1. Build the Docker image from the project root
docker build -t discernus .

# 2. Start the services (application and database) in the background
docker-compose up -d

# 3. Set up the database schema inside the container (run once)
docker-compose exec app python launch.py --setup-db
```

### Common Docker Operations

-   **Run a command inside the container:**
    ```bash
    docker-compose exec app <your_command>
    # Example: run tests
    docker-compose exec app python -m pytest
    ```

-   **Access a shell inside the running container:**
    ```bash
    docker-compose exec app /bin/bash
    ```

-   **View logs for all services:**
    ```bash
    docker-compose logs -f
    ```

-   **Stop and remove all services:**
    ```bash
    docker-compose down
    ```

### Docker Troubleshooting

-   **`Permission denied` when running Docker commands?**
    -   Ensure your user is part of the `docker` group (`sudo usermod -aG docker $USER`), or run commands with `sudo`.

-   **Port conflicts?**
    -   If another service is using the PostgreSQL port (5432), you can change the port mapping in `docker-compose.yml`.

-   **Changes to `requirements.txt` or `Dockerfile`?**
    -   You must rebuild the image to include the changes: `docker-compose build`.

---

## 3. Common Issues

-   **Import failures (in local setup)?** → Ensure you have run `source scripts/setup_dev_env.sh`.
-   **Command not found: `python`?** → The standard is `python3`.
-   **Database connection errors?** → Verify the database service is running (via `docker-compose ps`) and that the connection details in your configuration are correct.

---

## 4. Setting Up the Research Workspace

The `research_workspaces` directory is essential for development, as it holds the frameworks, experiments, and other assets the application loads at runtime. This directory is intentionally not committed to the repository to keep research data separate from the application's source code.

For a new developer, this directory will be empty. To create the standard, required folder structure, run the following command from the project root:

```bash
python3 scripts/utilities/setup_research_workspace.py
```

This script will create all the necessary subdirectories (`experiments/`, `frameworks/`, etc.) so you can begin development immediately.

---

**For complete development environment guidance, see `.cursorrules`** 