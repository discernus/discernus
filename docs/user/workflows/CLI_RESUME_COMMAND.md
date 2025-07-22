# CLI Resume Command Documentation

## Overview

The `discernus resume` command enables resumption of interrupted experiments from saved state files. This feature transforms experiment failures from "lost work" to "resumable progress" - a critical capability for production research workflows.

## Basic Usage

```bash
# Resume with intelligent state analysis (default)
discernus resume ./projects/my_experiment

# Resume with specific options
discernus resume ./projects/my_experiment --state-file state_after_step_2.json
discernus resume ./projects/my_experiment --from-step 3
discernus resume ./projects/my_experiment --dry-run
discernus resume ./projects/my_experiment --list-states

# Intelligent vs Legacy resume modes
discernus resume ./projects/my_experiment --intelligent    # Default: state analysis + validation
discernus resume ./projects/my_experiment --legacy        # Legacy: direct state continuation
```

## Command Options

### `--state-file FILE`
Specify a particular state file to resume from instead of auto-detecting the latest one.

**Example:**
```bash
discernus resume ./projects/my_experiment --state-file results/2025-07-17_21-59-15/state_after_step_1_AnalysisAgent.json
```

### `--from-step INTEGER`
Override auto-detection and resume from a specific step number (1-based).

**Example:**
```bash
discernus resume ./projects/my_experiment --from-step 3
```

### `--dry-run`
Show what would be resumed without executing any workflow steps.

**Example:**
```bash
discernus resume ./projects/my_experiment --dry-run
```

**Output:**
```
🔄 Discernus Experiment Resume
========================================
📂 Using latest state file: results/2025-07-17_21-59-15/state_after_step_1_AnalysisAgent.json
✅ Loaded state file with 16 top-level keys
🎯 Auto-detected resume step: 2

📋 Workflow Status (4 steps total):
   Step 1: AnalysisAgent - ✅ COMPLETED
   Step 2: DataExtractionAgent - 🚀 RESUMING
   Step 3: CalculationAgent - ⏳ PENDING
   Step 4: SynthesisAgent - ⏳ PENDING

🧪 DRY RUN: Would resume from step 2
   No actual execution will occur.
```

### `--list-states`
List all available state files for resumption, sorted by modification time.

**Example:**
```bash
discernus resume ./projects/my_experiment --list-states
```

### `--intelligent` / `--legacy`
Choose between intelligent state analysis (default) or legacy direct resumption.

**Intelligent Resume (Default):**
- State integrity validation
- Workflow change detection since interruption
- Resource availability validation  
- User guidance and multiple resumption options
- Enhanced with Issue #132 smart resumption logic

**Legacy Resume:**
- Direct state file loading and continuation
- Original resume behavior for backwards compatibility

**Examples:**
```bash
# Intelligent resume with full state analysis
discernus resume ./projects/my_experiment --intelligent

# Legacy resume for backwards compatibility  
discernus resume ./projects/my_experiment --legacy
```

**Output:**
```
📁 Scanning for state files in: projects/my_experiment

📋 Found 7 state files:
   1. results/2025-07-18_09-05-44/state_after_step_4_SynthesisAgent.json (2025-07-18 09:52:13)
   2. results/2025-07-18_09-05-44/state_after_step_3_CalculationAgent.json (2025-07-18 09:51:45)
   3. results/2025-07-18_09-05-44/state_after_step_2_DataExtractionAgent.json (2025-07-18 09:49:09)
   4. results/2025-07-17_21-59-15/state_after_step_1_AnalysisAgent.json (2025-07-17 22:35:38)
   ...
```

## Intelligent Resumption Logic (Issue #132)

### Enhanced State Analysis (Default Mode)
The intelligent resume performs comprehensive analysis before resumption:

1. **Enhanced State Discovery**: Scans both `results/` and `experiments/` directory structures
2. **State Integrity Validation**: Verifies state files are complete and consistent  
3. **Workflow Change Detection**: Compares current experiment.md to interrupted session
4. **Resource Validation**: Ensures required models and dependencies are still available
5. **Progress Assessment**: Determines exactly what work has been completed
6. **Resumption Point Analysis**: Identifies the precise resumption point with validation
7. **User Guidance**: Presents clear options and recommendations

### Legacy Auto-Detection (--legacy mode)
The original resume logic for backwards compatibility:

1. **State File Discovery**: Scans the project's `results/` directory for state files
2. **Latest Selection**: Chooses the most recently modified state file if none specified
3. **Step Detection**: Extracts the completed step number from the filename pattern `state_after_step_N_AgentName.json`
4. **Resume Point**: Automatically resumes from the next step after the completed one

## Framework Agnostic

The resume command works with **any compliant framework**:
- ✅ CFF (Cohesive Flourishing Framework)
- ✅ PDAF (Political Discourse Analysis Framework)
- ✅ Custom frameworks following Framework Specification v4.0
- ✅ Any experiment with workflow steps defined

## Error Handling

The command provides comprehensive error handling and user guidance:

### No State Files Found
```bash
❌ No state files found for resumption.
💡 Run 'discernus resume PROJECT_PATH --list-states' to see available state files.
```

### Invalid State File
```bash
❌ Failed to load state file: [error details]
```

### Invalid Resume Step
```bash
❌ Invalid resume step: 5. Must be between 1 and 4
```

### Missing Agent in Workflow
```bash
❌ Step 2 failed: Step 2 is missing the 'agent' key.
```

## Safety Features

### Confirmation Prompts
```bash
📋 Workflow Status (4 steps total):
   Step 1: AnalysisAgent - ✅ COMPLETED
   Step 2: DataExtractionAgent - 🚀 RESUMING
   Step 3: CalculationAgent - ⏳ PENDING
   Step 4: SynthesisAgent - ⏳ PENDING

🚀 Resume experiment from step 2? [y/N]: 
```

### Git Rollback Support
If resumption fails, you can rollback using git:
```bash
git restore .
```

## Integration with Existing Workflows

The resume command integrates seamlessly with existing Discernus workflows:

1. **State File Compatibility**: Uses the same state files generated by `discernus execute`
2. **Orchestrator Integration**: Uses the same `WorkflowOrchestrator` for consistent execution
3. **Logging Integration**: Maintains the same logging and chronolog patterns
4. **Framework Loading**: Uses the same framework loading mechanisms

## Common Use Cases

### Development & Testing
```bash
# Quick validation without execution
discernus resume ./my_experiment --dry-run

# Resume from specific step for testing
discernus resume ./my_experiment --from-step 3
```

### Production Research
```bash
# Resume from latest failure point
discernus resume ./my_experiment

# Resume from specific known good state
discernus resume ./my_experiment --state-file results/session_xyz/state_after_step_2.json
```

### Debugging & Analysis
```bash
# List all available resume points
discernus resume ./my_experiment --list-states

# Resume from earlier step to re-run problematic phase
discernus resume ./my_experiment --from-step 1
```

## Technical Implementation

### Architecture
- **Framework-Agnostic**: Works with any compliant experiment structure
- **State File Validation**: Comprehensive JSON loading and validation
- **Workflow Integration**: Full integration with existing `WorkflowOrchestrator`
- **THIN Principles**: Follows THIN architecture with minimal software intelligence

### State File Format
The resume command works with standard state files containing:
- `workflow`: Array of workflow step definitions
- `framework`: Complete framework specification
- `experiment`: Experiment configuration
- `corpus`: Corpus metadata and files
- Additional workflow state data

### Resume Point Detection
```python
# Filename pattern: state_after_step_N_AgentName.json
match = re.search(r'state_after_step_(\d+)_', filename)
if match:
    completed_step = int(match.group(1))
    return completed_step + 1  # Resume from next step
```

## Future Enhancements

### Phase 2: Fault Tolerance Infrastructure
- Incremental state persistence (save after each LLM call)
- Never lose more than 1 LLM call's worth of work
- Progressive checkpoints during workflow execution

### Phase 3: Advanced Resume Features
- Resume from specific LLM call number
- Parallel workflow resumption
- Cross-session resume capability
- Resume with different parameters (model, runs, etc.)

### Phase 4: Integration Enhancements
- Resume from CLI `execute` command failures
- Integration with fault tolerance monitoring
- Resume suggestions in error messages

## Success Stories

### MVA Experiment 3 Recovery
The CLI resume command was successfully validated by recovering MVA Experiment 3:
- **Failure Point**: DataExtractionAgent schema transformation issues
- **Recovery**: Resumed from `state_after_step_1_AnalysisAgent.json`
- **Result**: Successfully completed all 4 workflow steps
- **Output**: Generated `mva_results.csv` and `final_mva_report.md`
- **Data**: Processed 94 CFF analyses with 46/47 successful extractions

This real-world validation proves the resume command works in production scenarios and can recover valuable research work from infrastructure failures. 