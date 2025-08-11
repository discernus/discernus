# Infrastructure Reliability Report
Generated: 2025-08-11 12:44:20 UTC
Project: simple_test

## Overall Health
- Success Rate: 27.0%
- Total Experiments: 74
- Total Failures: 54
- Reliability Trend: Degrading

## 🚨 Critical Components (< 50% success rate)

- **experiment_execution**: 29.6% success (0/27 failures)
- **dimension_validation**: 0.0% success (12/12 failures)
- **statistical_validation**: 0.0% success (23/23 failures)

## ✅ Healthy Components (≥ 80% success rate)

- **SequentialSynthesisAgent**: 100.0% success (12 executions)

## 🔍 Common Failure Patterns

- `statistical_validation:` (1 occurrences)

## 📊 Detailed Component Metrics

### SequentialSynthesisAgent
- Executions: 12 total, 12 successful, 0 failed
- Success Rate: 100.0%
- Average Duration: N/A
- Last Execution: 2025-08-11T11:56:48.935401+00:00

### dimension_validation
- Executions: 12 total, 0 successful, 12 failed
- Success Rate: 0.0%
- Average Duration: N/A
- Last Execution: 2025-08-11T01:41:46.226103+00:00

### experiment_execution
- Executions: 27 total, 8 successful, 0 failed
- Success Rate: 29.6%
- Average Duration: N/A
- Last Execution: 2025-08-11T02:55:05.499719+00:00

### statistical_validation
- Executions: 23 total, 0 successful, 23 failed
- Success Rate: 0.0%
- Average Duration: N/A
- Last Execution: 2025-08-11T02:56:49.153256+00:00

**Recent Error Patterns:**
- `statistical_validation:`
