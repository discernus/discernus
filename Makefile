# Discernus Development Makefile
# Enforces Docker-first development (Rule 0)

.PHONY: help start stop test experiment database shell clean

help: ## Show this help message
	@echo "🐳 Discernus Docker-First Development Commands"
	@echo "=============================================="
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "⚠️  NEVER run Python commands directly on host system!"
	@echo "✅ Always use these Docker commands instead."

start: ## Start the containerized environment
	docker-compose up -d
	@echo "✅ Environment started. Use 'make test' to validate."

stop: ## Stop the containerized environment
	docker-compose down

test: ## Run database and environment validation
	docker-compose exec app python3 check_database.py

experiment: ## Run experiment orchestrator (provide EXPERIMENT_FILE=path)
	@if [ -z "$(EXPERIMENT_FILE)" ]; then \
		echo "❌ Must provide EXPERIMENT_FILE=path"; \
		echo "Example: make experiment EXPERIMENT_FILE=experiments/my_experiment.json"; \
		exit 1; \
	fi
	docker-compose exec app python3 scripts/applications/comprehensive_experiment_orchestrator.py $(EXPERIMENT_FILE)

database: ## Access PostgreSQL database shell
	docker-compose exec db psql -U postgres -d discernus

shell: ## Access application container shell
	docker-compose exec app /bin/bash

logs: ## View application logs
	docker-compose logs -f app

clean: ## Clean up containers and volumes
	docker-compose down -v
	docker system prune -f

# Prevent accidental host usage
python3:
	@echo "❌ BLOCKED: Direct python3 usage violates Rule 0"
	@echo "✅ Use: make shell"
	@exit 1

psql:
	@echo "❌ BLOCKED: Direct psql usage violates Rule 0"  
	@echo "✅ Use: make database"
	@exit 1 