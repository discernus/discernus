# License Audit Tools Makefile
# Convenient commands for running license audits

.PHONY: help audit quick baseline diff compliance policy clean test

# Default target
help:
	@echo "License Audit Tools for Discernus Project"
	@echo ""
	@echo "Available commands:"
	@echo "  audit      - Run complete license audit"
	@echo "  quick      - Quick license check only"
	@echo "  baseline   - Create new baseline audit"
	@echo "  diff       - Compare against existing baseline"
	@echo "  compliance - Check license compliance only"
	@echo "  policy     - Create example policy file"
	@echo "  clean      - Remove generated reports"
	@echo "  test       - Test all scripts"
	@echo ""
	@echo "Examples:"
	@echo "  make audit              # Full audit with all reports"
	@echo "  make baseline           # Create baseline_audit.json"
	@echo "  make diff               # Compare against baseline"
	@echo "  make compliance         # Policy compliance check"

# Run complete audit
audit:
	@echo "🎯 Running complete license audit..."
	python3 run_audit.py --output-dir audit_results

# Quick license check
quick:
	@echo "🔍 Running quick license check..."
	python3 license_checker.py

# Create baseline audit for future comparisons
baseline:
	@echo "📊 Creating baseline audit..."
	python3 license_checker.py --output-format json --output-file baseline_audit.json
	@echo "✅ Baseline saved to baseline_audit.json"

# Compare against baseline
diff:
	@if [ ! -f baseline_audit.json ]; then \
		echo "❌ No baseline found. Run 'make baseline' first."; \
		exit 1; \
	fi
	@echo "📈 Comparing against baseline..."
	python3 dependency_diff.py baseline_audit.json

# Check compliance against policy
compliance:
	@echo "✅ Checking license compliance..."
	python3 compliance_checker.py

# Create example policy file
policy:
	@echo "📋 Creating example policy file..."
	python3 compliance_checker.py --create-policy
	@echo "✅ Example policy created: license_policy_example.json"

# Clean up generated files
clean:
	@echo "🧹 Cleaning up generated files..."
	rm -rf audit_results/
	rm -f license_policy_example.json
	rm -f *.json *.md *.csv
	@echo "✅ Cleanup complete"

# Test all scripts
test:
	@echo "🧪 Testing all scripts..."
	@echo "Testing license_checker.py..."
	python3 license_checker.py --output-format json > /dev/null && echo "✅ license_checker.py works"
	@echo "Testing compliance_checker.py..."
	python3 compliance_checker.py --create-policy > /dev/null && echo "✅ compliance_checker.py works"
	@echo "Testing run_audit.py..."
	python3 run_audit.py --output-dir test_audit > /dev/null && echo "✅ run_audit.py works"
	@rm -rf test_audit license_policy_example.json
	@echo "✅ All scripts working correctly"

# Run with custom baseline
audit-with-baseline:
	@if [ ! -f baseline_audit.json ]; then \
		echo "❌ No baseline found. Run 'make baseline' first."; \
		exit 1; \
	fi
	@echo "🎯 Running audit with baseline comparison..."
	python3 run_audit.py --baseline baseline_audit.json --output-dir audit_results

# CI/CD friendly compliance check (exits with error code)
ci-compliance:
	@echo "🤖 Running CI compliance check..."
	python3 compliance_checker.py
	@if [ $$? -eq 0 ]; then \
		echo "✅ All licenses compliant - safe to deploy"; \
	else \
		echo "❌ License violations detected - blocking deployment"; \
		exit 1; \
	fi

# Generate quarterly report
quarterly:
	@echo "📅 Generating quarterly license report..."
	@mkdir -p quarterly_reports
	python3 run_audit.py --baseline baseline_audit.json --output-dir quarterly_reports/$(shell date +%Y-%m)
	@echo "✅ Quarterly report generated in quarterly_reports/$(shell date +%Y-%m)/"

# Show current license summary
summary:
	@echo "📊 Current license summary:"
	python3 license_checker.py | head -20 