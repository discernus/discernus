# Discernus: AI Model Analysis Platform

Clean, production-ready implementation of the Discernus platform for analyzing and comparing AI model outputs across moral, political, and psychological frameworks.

## Quick Start

1. **Setup Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Configure Database**:
   ```bash
   cp .env.example .env
   # Edit .env with your database and API credentials
   alembic upgrade head
   ```

3. **Start API Server**:
   ```bash
   python3 -m uvicorn reboot.api.main:app --host 0.0.0.0 --port 8000 --reload
   ```

4. **Run Analysis**:
   ```bash
   python3 reboot/experiments/run_experiment.py reboot/experiments/flagship_model_statistical_comparison.yaml
   ```

## Core Features

- **Multi-Model Comparison**: Compare GPT-4, Claude, and other LLMs
- **Statistical Analysis**: Rigorous correlation and significance testing  
- **Beautiful Reports**: Interactive visualizations with circular coordinate systems
- **Robust Parsing**: Handles various LLM response formats
- **Database Persistence**: PostgreSQL with Alembic migrations

## Architecture

- `reboot/api/` - FastAPI web server
- `reboot/analysis/` - Statistical methods and comparison logic
- `reboot/database/` - SQLAlchemy models and migrations
- `reboot/engine/` - Core analysis engine
- `reboot/gateway/` - LLM API clients  
- `reboot/reporting/` - Visualization and report generation

Built for production research use.
