# System Health Test Suite

## Overview

This directory contains self-contained system health validation tests for the Discernus platform. These tests verify that core system components work correctly without depending on external research workspaces or framework templates.

## Directory Structure

```
tests/system_health/
├── README.md                           # This documentation
├── test_system_health.py              # Main system health validation script
├── frameworks/                        # Dedicated test frameworks
│   └── moral_foundations_theory/      # Test framework for MFT validation
│       └── moral_foundations_theory_framework.yaml
├── test_experiments/                  # Dedicated test experiments
│   └── system_health_test.yaml        # Basic system health experiment
└── results/                           # Test result storage
    ├── latest.json                    # Latest test results (JSON)
    ├── system_health_YYYYMMDD_HHMMSS.json # Timestamped detailed results
    └── summary_YYYYMMDD_HHMMSS.txt    # Human-readable summaries
```

## Purpose

The system health tests are designed to validate:

1. **Core Imports** - All critical system components can be imported
2. **Coordinate System** - Enhanced coordinate algorithms work correctly
3. **QA System** - Quality assurance system initializes and functions
4. **Framework Loading** - Framework manager can load YAML frameworks
5. **Experiment Definition** - Experiment definitions can be parsed and validated
6. **End-to-End Experiment Execution** - Complete experiment pipeline with 9-dimensional validation

## 🎯 9-Dimensional Experiment Validation Framework

The end-to-end test validates that the system can deliver truly successful experiments according to your comprehensive framework:

### **✅ All 9 Dimensions Validated**

1. **Design Validation** - Experiment definition YAML loads and validates
2. **Dependency Validation** - All experiment components (frameworks, engines, QA) initialize
3. **Execution Integrity** - Complete analysis pipeline executes successfully
4. **Data Persistence** - Results stored and retrievable from database/files
5. **Asset Management** - Reports, visualizations, and academic packages generated
6. **Reproducibility** - Results stored for immediate use and future reproduction
7. **Scientific Validity** - QA system validates results meet confidence thresholds
8. **Design Alignment** - Results appropriate to experiment design and expectations
9. **Research Value** - Complete workflow delivers actionable insights to researchers

## Design Principles

### Self-Contained Testing
- **No external dependencies** on research workspaces or template archives
- **Dedicated test assets** that are purpose-built for validation
- **Consistent test environment** that doesn't change with research work

### Clear Separation of Concerns
- **`framework_templates/`** = Archive of "original DNA" framework templates (not for testing)
- **`research_workspaces/`** = Active research frameworks and experiments (not for testing)
- **`tests/system_health/`** = Dedicated system validation assets (for testing only)

## Usage

Run the system health validation:

```bash
# From project root
python tests/system_health/test_system_health.py

# Or from the test directory
cd tests/system_health
python test_system_health.py

# Disable result storage (console output only)
python tests/system_health/test_system_health.py --no-save

# Include real LLM integration test (costs money!)
python tests/system_health/test_system_health.py --include-real-llm

# Fast CI/CD mode: no storage, mock-only
python tests/system_health/test_system_health.py --no-save
```

## Result Storage

Test results are automatically saved to `tests/system_health/results/` in multiple formats:

### 1. **JSON Results** (Machine-readable)
- **`latest.json`** - Always contains the most recent test results
- **`system_health_YYYYMMDD_HHMMSS.json`** - Timestamped detailed results

**JSON Structure:**
```json
{
  "summary": {
    "total_tests": 5,
    "passed_tests": 5,
    "success_rate": 100.0,
    "overall_status": "HEALTHY",
    "duration_seconds": 0.46,
    "start_time": "2025-06-23T07:37:26.742221"
  },
  "tests": [
    {
      "test_name": "Core Imports",
      "passed": true,
      "details": { "coordinate_engine": "success" },
      "error": null
    }
  ],
  "metadata": {
    "test_suite_version": "1.0.0",
    "python_version": "3.9.6",
    "platform": "darwin"
  }
}
```

### 2. **Text Summaries** (Human-readable)
- **`summary_YYYYMMDD_HHMMSS.txt`** - Human-readable test reports

**Text Format:**
```
🏥 DISCERNUS SYSTEM HEALTH VALIDATION
==================================================
Run Time: 2025-06-23 07:37:26
Duration: 0.46 seconds
Status: HEALTHY
Tests: 5/5 passed (100.0%)

✅ PASS Core Imports
   coordinate_engine: success
   qa_system: success
   framework_manager: success
```

### 3. **Accessing Results**

**Latest Results (JSON):**
```bash
# View latest test status
cat tests/system_health/results/latest.json | jq '.summary.overall_status'

# Check specific test details
cat tests/system_health/results/latest.json | jq '.tests[] | select(.test_name=="Framework Loading")'
```

**Historical Results:**
```bash
# List all test runs
ls tests/system_health/results/system_health_*.json

# View specific run
cat tests/system_health/results/system_health_20250623_073726.json
```

Expected output:
```
🏥 DISCERNUS SYSTEM HEALTH VALIDATION
==================================================
🧪 Testing Core System Imports...
✅ DiscernusCoordinateEngine import successful
✅ LLMQualityAssuranceSystem import successful
✅ FrameworkManager import successful

🎯 Testing Enhanced Coordinate System...
✅ Coordinate engine initialization successful
✅ Coordinate calculation working: (0.581, 0.252), distance: 0.633
✅ Dominance amplification working
✅ Adaptive scaling working: 0.910

🛡️ Testing QA System...
✅ QA system initialization successful
✅ QA system basic functionality available

🏗️ Testing Framework Loading...
✅ Test framework loading successful
✅ Framework has 6 anchors (anchors terminology)

📋 Testing Experiment Definition...
✅ Test experiment definition loading successful
✅ Experiment definition structure valid
✅ Experiment: System_Health_Test
✅ Description: Basic system health validation test - validates core...
✅ Has 3 success criteria defined
✅ Component types: frameworks, models
✅ Experiment correctly references test framework

🎪 Testing End-to-End Experiment Execution...
✅ Design validation: Experiment definition loaded
✅ Dependency validation: All components loaded successfully
🎭 Using mock LLM for analysis...
✅ Execution integrity: Full pipeline executed successfully
✅ Data persistence: Results saved successfully
✅ Asset management: Report generated successfully
✅ Reproducibility: Results successfully stored and retrieved
✅ Scientific validity: QA confidence threshold met
✅ Design alignment: Results match expected moral foundation activations
✅ Research value: Complete workflow delivers actionable insights
🎉 End-to-end experiment execution: ALL 9 DIMENSIONS VALIDATED

==================================================
🏆 VALIDATION SUMMARY: 6/6 tests passed
🎉 System is healthy and ready for experiments!
```

## Maintenance Notes

### Adding New Tests
1. Add test functions to `test_system_health.py`
2. Update the `tests` list in `run_comprehensive_validation()`
3. Add any required test assets to the appropriate subdirectories

### Framework Updates
If core framework structure changes:
1. Update `frameworks/moral_foundations_theory/` with new structure
2. Update validation logic in `test_framework_loading()`
3. Ensure test experiment still references correct framework path

### Integration with CI/CD
This test suite should be run as part of:
- Pre-commit hooks
- CI/CD pipeline validation
- Development environment setup verification
- Release candidate validation

**CI/CD Integration Examples:**

```yaml
# GitHub Actions example
- name: System Health Check
  run: |
    python tests/system_health/test_system_health.py
    # Upload results as artifacts
    echo "HEALTH_STATUS=$(cat tests/system_health/results/latest.json | jq -r '.summary.overall_status')" >> $GITHUB_ENV

# Jenkins pipeline example
stage('Health Check') {
    steps {
        sh 'python tests/system_health/test_system_health.py'
        archiveArtifacts artifacts: 'tests/system_health/results/*.json'
        script {
            def healthStatus = readJSON file: 'tests/system_health/results/latest.json'
            if (healthStatus.summary.overall_status != 'HEALTHY') {
                error "System health check failed: ${healthStatus.summary.overall_status}"
            }
        }
    }
}
```

**Monitoring Integration:**
```bash
# Automated monitoring script
#!/bin/bash
python tests/system_health/test_system_health.py
STATUS=$(cat tests/system_health/results/latest.json | jq -r '.summary.overall_status')
if [ "$STATUS" != "HEALTHY" ]; then
    # Send alert to monitoring system
    curl -X POST "https://monitoring.example.com/alert" \
         -d "status=$STATUS&component=discernus-system-health"
fi
```

The self-contained nature ensures consistent results across all environments. 