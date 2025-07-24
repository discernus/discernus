# Incident Post-Mortem: Phase 3 Orchestration Failure

**Date**: July 24, 2025
**Status**: Complete

## 1. Executive Summary

The Phase 3 orchestration pipeline failure, where `CorpusSynthesisAgent` tasks are not created, is not caused by a random process crash or infrastructure instability. The root cause is a **predictable architectural gap** in the `OrchestratorAgent`'s coordination logic.

The agent was designed to handle a simple, linear "fire-and-wait-for-one" task sequence. The introduction of parallel `AnalyseBatchAgent` tasks in commit `a79a4e79` was not accompanied by an upgrade to the orchestrator's waiting logic. It correctly "fans out" multiple analysis tasks but has no mechanism to "fan in" their results to trigger the next stage.

The `phase3_test_runner.py` script contains more advanced coordination logic (`_wait_for_task_completion_by_type`) than the production orchestrator, confirming this architectural deficiency.

## 2. Incident Timeline & Analysis

| Timestamp | Event | Analysis |
| :--- | :--- | :--- |
| T+0s | `OrchestratorAgent` receives experiment request. | Process starts as expected. |
| T+5s | `OrchestratorAgent` enqueues `pre_test` task. | Correctly initiates the first step. |
| T+45s | `PreTestAgent` completes. `OrchestratorAgent` receives completion from `tasks.done` stream via `_wait_for_task_completion`. | The "wait-for-one" logic works as designed. |
| T+50s | `OrchestratorAgent` enqueues two `analyse_batch` tasks. | The "fan-out" logic from commit `a79a4e79` executes correctly. |
| T+51s | `OrchestratorAgent`'s `orchestrate_experiment` function completes its sequence and returns to the main listening loop. | **This is the point of failure.** The agent considers its job done and does not wait for the `analyse_batch` tasks it just created. |
| T+5m | Both `AnalyseBatchAgent` processes complete and write their success messages to the `tasks.done` stream. | The analysis layer works perfectly. |
| T+5m to ∞ | No `corpus_synthesis` task is ever created. | The `OrchestratorAgent` is idle, listening for new experiments, and is not aware that the batch results are ready for synthesis. |

## 3. Root Cause Determination

*   **Primary Cause**: Logic deficiency in `OrchestratorAgent`. The agent lacks the state management required to track the completion of a group of dynamically spawned tasks. It correctly implements a 1-to-1 task dependency (`pre_test`) but fails at the 1-to-many dependency (`analyse_batch`).

*   **Contributing Factor**: Divergence between test harness logic and production agent logic. The test runner (`phase3_test_runner.py`) has custom, more sophisticated waiting logic that is not present in the agent itself, masking the production deficit.

## 4. Validation of Architect's Recommendation

This diagnosis **strongly supports** the external architect's recommendation to focus on a "Minimal Fix Path" before considering a full Supervisor migration. The problem is not `subprocess.Popen` reliability; it is a straightforward logic bug in our Python application.

A simple, in-process worker pool or even an enhanced waiting loop within the existing `OrchestratorAgent` would directly address this failure mode without the operational overhead of Supervisor.

## 5. Next Steps

1.  **Proceed to "Minimal Fix Spike"**: Immediately prototype an enhanced waiting mechanism within the `OrchestratorAgent` to handle the fan-in logic.
2.  **Harmonize Logic**: Ensure that any production waiting logic is canonical and that test harnesses use the production logic, not their own custom implementations.
3.  **Defer Supervisor Decision**: Postpone any decision on Supervisor until after the minimal fix has been implemented and tested. The data from this incident does not support the need for an external process manager at this time. 