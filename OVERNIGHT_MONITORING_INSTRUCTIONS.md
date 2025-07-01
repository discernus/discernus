# 🌙 Overnight Experiment Monitoring Instructions

## Quick Start (Recommended)

```bash
# Make sure you're in the project root directory (/Volumes/dev/discernus)
./run_flagship_monitored.sh
```

## What This Does

The monitoring system will:

✅ **Capture ALL errors** - parsing failures, model failures, API issues  
✅ **Save raw LLM responses** - for debugging format mismatches  
✅ **Continue on failures** - won't stop if one model fails  
✅ **Generate comprehensive reports** - human-readable summaries  
✅ **Log everything** - timestamped logs with full details  

## Output Files You'll Find Tomorrow

### 1. Terminal Output
- `flagship_experiment_output_YYYYMMDD_HHMMSS.log` - Complete terminal output

### 2. Error Analysis Directory  
- `error_logs_YYYYMMDD_HHMMSS/` - Comprehensive error analysis
  - `ERROR_SUMMARY.md` - **READ THIS FIRST** - Human-readable summary
  - `FINAL_ERROR_REPORT.json` - Complete structured error data
  - `experiment_errors.log` - Detailed timestamped log
  - `raw_response_[model]_[#].txt` - Actual LLM responses that failed parsing
  - `parsing_failure_[model]_[#].json` - Detailed parsing failure analysis

### 3. Normal Experiment Results
- `0_workspace/byu_populism_project/experiments/exp_02_flagship_ensemble/results/YYYY-MM-DD_HH-MM-SS/`
  - `stage6_interactive_analysis.ipynb` - Analysis notebook
  - `run_metadata.json` - Experiment metadata

## Tomorrow Morning Debugging Workflow

1. **Check if experiment completed**:
   ```bash
   tail flagship_experiment_output_*.log
   ```

2. **Quick error overview**:
   ```bash
   ls error_logs_*/
   cat error_logs_*/ERROR_SUMMARY.md
   ```

3. **If there were parsing failures**:
   ```bash
   # Look at what models actually returned
   cat error_logs_*/raw_response_*.txt
   ```

4. **If experiment succeeded**:
   ```bash
   # Check the results directory
   ls 0_workspace/byu_populism_project/experiments/exp_02_flagship_ensemble/results/
   ```

## Expected Behavior

### ✅ **Success Case**:
- 6 models complete successfully (GPT-4o, Claude-3.5-Sonnet, Mistral, Gemini, Claude-Haiku, Portuguese-Ollama)
- All models follow JSON format correctly
- Coordinate generation successful (not 0.000, 0.000)
- Stage 6 notebook generated with ensemble analysis

### ⚠️ **Partial Success** (Expected):
- Some models may fail (especially Portuguese Ollama if it's resource-intensive)
- Experiment continues with remaining models
- Error logs capture what went wrong for debugging

### 🚨 **Complete Failure** (Unexpected):
- If ALL models fail, check:
  - API key issues (`ERROR_SUMMARY.md`)
  - Prompt format problems (parsing failures)
  - Infrastructure issues (general errors)

## Manual Alternative

If you prefer to run manually:

```bash
python3 monitored_experiment_runner.py 0_workspace/byu_populism_project/experiments/exp_02_flagship_ensemble/exp_02_flagship_ensemble.yaml
```

## What We Fixed Today

✅ **Prompt Engine Bug** - GPT-4o now receives proper JSON format instructions  
✅ **Parsing Infrastructure** - Robust handling of different response formats  
✅ **Temperature Setting** - Fixed at 0.7 for proper variation  
✅ **Framework Validation** - All v3.2 compliance checks pass  

The infrastructure should be rock-solid now. Any remaining issues will be captured in detail for easy debugging tomorrow.

---

**Sleep well! 😴 The system will handle everything and capture any issues for morning analysis.** 