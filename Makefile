# Discernus Development Makefile
# Local development workflow commands

.PHONY: help setup test experiment database clean health

help: ## Show this help message
	@echo "🖥️  Discernus Local Development Commands"
	@echo "======================================="
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "💡 All commands run in your local Python environment"
	@echo "⚠️  Make sure to activate your virtual environment first!"

setup: ## Set up local development environment
	@echo "🔧 Setting up local development environment..."
	@if [ ! -d "venv" ]; then python3 -m venv venv; fi
	@echo "📦 Installing dependencies..."
	@. venv/bin/activate && pip install -r requirements.txt
	@if [ ! -f ".env" ]; then cp env.example .env; echo "📝 Created .env file from template - please edit with your settings"; fi
	@echo "✅ Setup complete! Don't forget to activate your venv: source venv/bin/activate"

test: ## Run database and environment validation
	python3 check_database.py

experiment: ## Run experiment orchestrator (provide EXPERIMENT_FILE=path)
	@if [ -z "$(EXPERIMENT_FILE)" ]; then \
		echo "Error: EXPERIMENT_FILE not specified"; \
		echo "Usage: make experiment EXPERIMENT_FILE=path/to/experiment.yaml"; \
		echo "Example: make experiment EXPERIMENT_FILE=experiments/my_experiment.yaml"; \
		exit 1; \
	fi
	python3 scripts/applications/comprehensive_experiment_orchestrator.py $(EXPERIMENT_FILE)

health: ## Run system health check
	python3 scripts/applications/comprehensive_experiment_orchestrator.py --system-health-mode

database: ## Access PostgreSQL database shell (local)
	psql -h localhost -U postgres -d discernus

clean: ## Clean up local cache and temporary files
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete
	rm -rf .pytest_cache/
	@echo "🧹 Cleaned up local cache files"

# Helpful environment checks
venv-check:
	@if [ -z "$$VIRTUAL_ENV" ]; then \
		echo "⚠️  Virtual environment not activated!"; \
		echo "💡 Run: source venv/bin/activate"; \
		exit 1; \
	fi 