# System Health Test Assets

## Overview

This directory contains **test assets** used by the production orchestrator when running system health validation. The standalone test system has been **deprecated** and replaced with integrated system health mode in the production orchestrator.

## 🔄 Migration Status: COMPLETE

- ❌ **Old**: Standalone `test_system_health.py` (deprecated)
- ✅ **New**: `scripts/system_health_check.sh` (uses production orchestrator)

## Directory Structure

```
tests/system_health/
├── README.md                           # This documentation
├── frameworks/                        # Test framework assets
│   └── moral_foundations_theory/      # MFT test framework
│       └── moral_foundations_theory_framework.yaml
├── test_experiments/                  # Test experiment definitions
│   └── system_health_test.yaml        # System health validation experiment
└── results/                           # Test result storage
    ├── latest.json                    # Latest test results
    └── system_health_*.json           # Timestamped results
```

## Purpose

This directory provides **dedicated test assets** for system health validation that are:
- **Self-contained** - No dependencies on research workspaces
- **Stable** - Won't change with research work
- **Production-integrated** - Used by the actual production orchestrator

## Current Usage

### 🏥 System Health Checks (Recommended)
```bash
# Basic health check
scripts/system_health_check.sh

# CI/CD mode
scripts/system_health_check.sh ci

# Pre-release validation  
scripts/system_health_check.sh release
```

### 🔧 Direct Orchestrator Usage
```bash
# Direct production orchestrator with system health mode
python3 scripts/applications/comprehensive_experiment_orchestrator.py \
  tests/system_health/test_experiments/system_health_test.yaml \
  --system-health-mode
```

## Asset Details

### Test Framework
- **Location**: `frameworks/moral_foundations_theory/moral_foundations_theory_framework.yaml`
- **Purpose**: Provides stable MFT framework for testing coordinate calculations
- **Referenced by**: Production orchestrator when `--system-health-mode` is enabled

### Test Experiment
- **Location**: `test_experiments/system_health_test.yaml`
- **Purpose**: Defines system health validation experiment specification
- **Features**: Mock LLM analysis, zero API costs, comprehensive validation

### Results Storage
- **Location**: `results/`
- **Format**: JSON results with detailed validation tracking
- **Latest**: Always available at `results/latest.json`

## Integration Points

The production orchestrator automatically:
1. **Switches framework base directory** to `tests/system_health` in system health mode
2. **Uses mock LLM client** to avoid API costs
3. **Validates all 9 dimensions** of experiment execution
4. **Saves results** to this directory's results folder

## Maintenance

### When to Update
- **Framework structure changes**: Update test framework YAML
- **Experiment specification changes**: Update system health experiment
- **New validation requirements**: Modify experiment success criteria

### Files NOT to Modify
- Don't add production frameworks here (use `framework_templates/` instead)
- Don't add research experiments here (use `research_workspaces/` instead)
- Don't modify production orchestrator references to this directory

## CI/CD Integration

```yaml
# GitHub Actions example
- name: System Health Check
  run: scripts/system_health_check.sh ci
  
- name: Check Health Status
  run: |
    if [[ "$(cat tests/system_health/results/latest.json | jq -r '.summary.overall_status')" != "HEALTHY" ]]; then
      exit 1
    fi
```

---

**📚 For complete system health documentation, see**: [PRODUCTION_ORCHESTRATOR_SYSTEM_HEALTH_ENHANCEMENT_PLAN.md](../../PRODUCTION_ORCHESTRATOR_SYSTEM_HEALTH_ENHANCEMENT_PLAN.md) 