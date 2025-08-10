# Infrastructure Reliability Report
Generated: 2025-08-10 17:53:39 UTC
Project: simple_test

## Overall Health
- Success Rate: 64.6%
- Total Experiments: 82
- Total Failures: 29
- Reliability Trend: Degrading

## 🚨 Critical Components (< 50% success rate)

- **dimension_validation**: 0.0% success (2/2 failures)
- **statistical_validation**: 0.0% success (2/2 failures)

## ⚠️ Warning Components (< 80% success rate)

- **experiment_execution**: 51.9% success (0/52 failures)

## ✅ Healthy Components (≥ 80% success rate)

- **SequentialSynthesisAgent**: 100.0% success (26 executions)

## 🔍 Common Failure Patterns

- `statistical_validation:` (1 occurrences)

## 📊 Detailed Component Metrics

### SequentialSynthesisAgent
- Executions: 26 total, 26 successful, 0 failed
- Success Rate: 100.0%
- Average Duration: N/A
- Last Execution: 2025-08-10T00:42:45.625439+00:00

### dimension_validation
- Executions: 2 total, 0 successful, 2 failed
- Success Rate: 0.0%
- Average Duration: N/A
- Last Execution: 2025-08-10T10:57:46.111423+00:00

### experiment_execution
- Executions: 52 total, 27 successful, 0 failed
- Success Rate: 51.9%
- Average Duration: N/A
- Last Execution: 2025-08-10T11:53:50.069198+00:00

### statistical_validation
- Executions: 2 total, 0 successful, 2 failed
- Success Rate: 0.0%
- Average Duration: N/A
- Last Execution: 2025-08-10T11:54:01.817765+00:00

**Recent Error Patterns:**
- `statistical_validation:`
