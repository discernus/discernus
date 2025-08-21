# Discernus Development Makefile
# Standardizes common operations - no venv needed!

.PHONY: help check test install deps harness clean start-infra stop-infra safe-python

help:  ## Show this help message
	@echo "Discernus Development Commands"
	@echo "============================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

check:  ## Check environment setup (run this first!)
	@echo "🔍 Checking development environment..."
	@python3 scripts/check_environment.py

safe-python:  ## Use safe Python wrapper (recommended for agents)
	@echo "🛡️  Using safe Python wrapper..."
	@./scripts/safe_python.sh



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

validate-framework:  ## Validate a framework against current specification
	@if [ -z "$(FRAMEWORK)" ]; then echo "❌ Usage: make validate-framework FRAMEWORK=path/to/framework.md"; exit 1; fi
	@echo "🔍 Validating framework: $(FRAMEWORK)"
	@python3 scripts/framework_validation/framework_validator.py $(FRAMEWORK)

enhanced-validate-framework:  ## Enhanced validation with academic grounding
	@if [ -z "$(FRAMEWORK)" ]; then echo "❌ Usage: make enhanced-validate-framework FRAMEWORK=path/to/framework.md"; exit 1; fi
	@echo "🔍 Enhanced validation with academic grounding: $(FRAMEWORK)"
	@python3 scripts/framework_researcher/enhanced_framework_validator.py $(FRAMEWORK)

enhanced-validate-framework-verbose:  ## Enhanced validation with detailed transparency
	@if [ -z "$(FRAMEWORK)" ]; then echo "❌ Usage: make enhanced-validate-framework-verbose FRAMEWORK=path/to/framework.md"; exit 1; fi
	@echo "🔍 Enhanced validation with full transparency: $(FRAMEWORK)"
	@python3 scripts/framework_researcher/enhanced_framework_validator.py $(FRAMEWORK) --verbose

enhanced-validate-framework-research:  ## Enhanced validation with research directions generation
	@if [ -z "$(FRAMEWORK)" ]; then echo "❌ Usage: make enhanced-validate-framework-research FRAMEWORK=path/to/framework.md"; exit 1; fi
	@echo "🔍 Enhanced validation with research directions: $(FRAMEWORK)"
	@python3 scripts/framework_researcher/enhanced_framework_validator.py $(FRAMEWORK) --research-directions

enhanced-validate-framework-full:  ## Enhanced validation with research directions and verbose mode
	@if [ -z "$(FRAMEWORK)" ]; then echo "❌ Usage: make enhanced-validate-framework-full FRAMEWORK=path/to/framework.md"; exit 1; fi
	@echo "🔍 Enhanced validation with research directions and full transparency: $(FRAMEWORK)"
	@python3 scripts/framework_researcher/enhanced_framework_validator.py $(FRAMEWORK) --research-directions --verbose

enhanced-validate-framework-librarian:  ## Enhanced validation with research directions and librarian research initiation
	@if [ -z "$(FRAMEWORK)" ]; then echo "❌ Usage: make enhanced-validate-framework-librarian FRAMEWORK=path/to/framework.md"; exit 1; fi
	@echo "🔍 Enhanced validation with research directions and librarian research: $(FRAMEWORK)"
	@python3 scripts/framework_researcher/enhanced_framework_validator.py $(FRAMEWORK) --research-directions --initiate-research

harness-list:  ## List available models
	@python3 scripts/prompt_engineering_harness.py --list-models

harness-simple:  ## Test simple prompt (requires MODEL and PROMPT vars)
	@python3 scripts/prompt_engineering_harness.py --model "$(MODEL)" --prompt "$(PROMPT)"

harness-file:  ## Test prompt from file (requires MODEL and FILE vars)
	@python3 scripts/prompt_engineering_harness.py --model "$(MODEL)" --prompt-file "$(FILE)"

run:  ## Run experiment (requires EXPERIMENT var, e.g. make run EXPERIMENT=projects/simple_test)
	@if [ -z "$(EXPERIMENT)" ]; then echo "❌ Usage: make run EXPERIMENT=projects/your_experiment"; exit 1; fi
	@echo "🚀 Running experiment: $(EXPERIMENT)"
	@discernus run $(EXPERIMENT)

run-safe:  ## Run experiment with safe Python wrapper (recommended for agents)
	@if [ -z "$(EXPERIMENT)" ]; then echo "❌ Usage: make run-safe EXPERIMENT=projects/your_experiment"; exit 1; fi
	@echo "🛡️  Running experiment with safe wrapper: $(EXPERIMENT)"
	@./scripts/safe_python.sh -m discernus.cli run $(EXPERIMENT)

continue:  ## Continue experiment from artifacts (requires EXPERIMENT var)
	@if [ -z "$(EXPERIMENT)" ]; then echo "❌ Usage: make continue EXPERIMENT=projects/your_experiment"; exit 1; fi
	@echo "🔄 Continuing experiment: $(EXPERIMENT)"
	@discernus continue $(EXPERIMENT)

continue-safe:  ## Continue experiment with safe Python wrapper
	@if [ -z "$(EXPERIMENT)" ]; then echo "❌ Usage: make continue-safe EXPERIMENT=projects/your_experiment"; exit 1; fi
	@echo "🛡️  Continuing experiment with safe wrapper: $(EXPERIMENT)"
	@./scripts/safe_python.sh -m discernus.cli continue $(EXPERIMENT)

debug:  ## Debug experiment (requires EXPERIMENT var)
	@if [ -z "$(EXPERIMENT)" ]; then echo "❌ Usage: make debug EXPERIMENT=projects/your_experiment"; exit 1; fi
	@echo "🐛 Debugging experiment: $(EXPERIMENT)"
	@discernus debug $(EXPERIMENT) --verbose

debug-safe:  ## Debug experiment with safe Python wrapper
	@if [ -z "$(EXPERIMENT)" ]; then echo "❌ Usage: make debug-safe EXPERIMENT=projects/your_experiment"; exit 1; fi
	@echo "🛡️  Debugging experiment with safe wrapper: $(EXPERIMENT)"
	@./scripts/safe_python.sh -m discernus.cli debug $(EXPERIMENT) --verbose

list:  ## List available experiments
	@echo "📋 Listing experiments..."
	@discernus list

list-safe:  ## List experiments with safe Python wrapper
	@echo "🛡️  Listing experiments with safe wrapper..."
	@./scripts/safe_python.sh -m discernus.cli list

clean:  ## Clean up temporary files
	@echo "🧹 Cleaning temporary files..."
	@./scripts/cleanup_python_cache.sh
	@find . -name ".DS_Store" -delete
	@echo "✅ Cleanup complete!"

clean-all:  ## Comprehensive cleanup (cache, artifacts, logs)
	@echo "🧹 Comprehensive cleanup..."
	@./scripts/cleanup_python_cache.sh
	@find . -name ".DS_Store" -delete
	@find . -name "*.log" -path "*/deprecated/*" -delete
	@echo "✅ Comprehensive cleanup complete!"
	@echo "✅ Cleanup complete!" 