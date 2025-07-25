# Discernus Development Makefile
# Standardizes common operations to prevent venv confusion

.PHONY: help check test install deps harness clean

help:  ## Show this help message
	@echo "Discernus Development Commands"
	@echo "============================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-12s\033[0m %s\n", $$1, $$2}'

check:  ## Check environment setup (run this first!)
	@echo "🔍 Checking development environment..."
	@source venv/bin/activate && python3 scripts/check_environment.py

test:  ## Run the test suite
	@echo "🧪 Running tests..."
	@source venv/bin/activate && python3 discernus/tests/quick_test.py

install:  ## Set up the development environment
	@echo "🚀 Setting up development environment..."
	@python3 -m venv venv
	@source venv/bin/activate && pip install --upgrade pip
	@source venv/bin/activate && pip install -r requirements.txt
	@echo "✅ Environment ready! Run 'make check' to verify."

deps:  ## Install/update dependencies
	@echo "📦 Installing dependencies..."
	@source venv/bin/activate && pip install -r requirements.txt
	@echo "✅ Dependencies updated!"

harness:  ## Show prompt harness usage examples
	@echo "🎯 Prompt Engineering Harness Examples:"
	@echo "  List models:    make harness-list"
	@echo "  Test simple:    make harness-simple MODEL=<model> PROMPT=<prompt>"
	@echo "  Test file:      make harness-file MODEL=<model> FILE=<file>"

harness-list:  ## List available models
	@source venv/bin/activate && python3 scripts/prompt_engineering_harness.py --list-models

harness-simple:  ## Test simple prompt (requires MODEL and PROMPT vars)
	@source venv/bin/activate && python3 scripts/prompt_engineering_harness.py --model "$(MODEL)" --prompt "$(PROMPT)"

harness-file:  ## Test prompt from file (requires MODEL and FILE vars)
	@source venv/bin/activate && python3 scripts/prompt_engineering_harness.py --model "$(MODEL)" --prompt-file "$(FILE)"

clean:  ## Clean up temporary files
	@echo "🧹 Cleaning temporary files..."
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -name ".DS_Store" -delete
	@echo "✅ Cleanup complete!"

# Safety check - prevent running without activated venv
guard-%:
	@if [ -z "$(VIRTUAL_ENV)" ]; then echo "❌ Virtual environment not activated! Run 'source venv/bin/activate' first"; exit 1; fi 