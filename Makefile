# Discernus Development Makefile
# Standardizes common operations - no venv needed!

.PHONY: help check test install deps harness clean start-infra stop-infra

help:  ## Show this help message
	@echo "Discernus Development Commands"
	@echo "============================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

check:  ## Check environment setup (run this first!)
	@echo "🔍 Checking development environment..."
	@python3 scripts/check_environment.py

start-infra:  ## Start all infrastructure services (MinIO, Redis)
	@echo "🚀 Starting infrastructure services..."
	@./scripts/start_infrastructure.sh

stop-infra:  ## Stop all infrastructure services
	@echo "🛑 Stopping infrastructure services..."
	@pkill -f "minio server" || true
	@pkill redis-server || true
	@echo "✅ Infrastructure stopped"

test:  ## Run the test suite
	@echo "🧪 Running tests..."
	@python3 discernus/tests/quick_test.py

install:  ## Set up the development environment
	@echo "🚀 Setting up development environment..."
	@python3 -m pip install --user --break-system-packages -r requirements.txt
	@echo "✅ Environment ready! Run 'make check' to verify."

deps:  ## Install/update dependencies
	@echo "📦 Installing dependencies..."
	@python3 -m pip install --user --break-system-packages -r requirements.txt
	@echo "✅ Dependencies updated!"

harness:  ## Show prompt harness usage examples
	@echo "🎯 Prompt Engineering Harness Examples:"
	@echo "  List models:    make harness-list"
	@echo "  Test simple:    make harness-simple MODEL=<model> PROMPT=<prompt>"
	@echo "  Test file:      make harness-file MODEL=<model> FILE=<file>"

harness-list:  ## List available models
	@python3 scripts/prompt_engineering_harness.py --list-models

harness-simple:  ## Test simple prompt (requires MODEL and PROMPT vars)
	@python3 scripts/prompt_engineering_harness.py --model "$(MODEL)" --prompt "$(PROMPT)"

harness-file:  ## Test prompt from file (requires MODEL and FILE vars)
	@python3 scripts/prompt_engineering_harness.py --model "$(MODEL)" --prompt-file "$(FILE)"

run:  ## Run experiment (requires EXPERIMENT var, e.g. make run EXPERIMENT=projects/simple_test)
	@if [ -z "$(EXPERIMENT)" ]; then echo "❌ Usage: make run EXPERIMENT=projects/your_experiment"; exit 1; fi
	@echo "🚀 Running experiment: $(EXPERIMENT)"
	@python3 -m discernus.cli run $(EXPERIMENT)

continue:  ## Continue experiment from artifacts (requires EXPERIMENT var)
	@if [ -z "$(EXPERIMENT)" ]; then echo "❌ Usage: make continue EXPERIMENT=projects/your_experiment"; exit 1; fi
	@echo "🔄 Continuing experiment: $(EXPERIMENT)"
	@python3 -m discernus.cli continue $(EXPERIMENT)

debug:  ## Debug experiment (requires EXPERIMENT var)
	@if [ -z "$(EXPERIMENT)" ]; then echo "❌ Usage: make debug EXPERIMENT=projects/your_experiment"; exit 1; fi
	@echo "🐛 Debugging experiment: $(EXPERIMENT)"
	@python3 -m discernus.cli debug $(EXPERIMENT) --verbose

clean:  ## Clean up temporary files
	@echo "🧹 Cleaning temporary files..."
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -name ".DS_Store" -delete
	@echo "✅ Cleanup complete!" 