# "Phase 0.5" Diagnostic Sprint Plan

**Objective**:
a) Pin down the exact root cause of the Phase 3 orchestration pipeline failure.
b) Gather empirical data to validate whether the architect's proposed "Minimal Fix Path" is sufficient, or if a Supervisor migration is necessary.

**Deliverables**:
1.  **Incident Post-Mortem Report**: A document detailing the timeline, error logs, and Redis state for recent failures.
2.  **Code Audit Findings**: A list of actionable findings from reviewing the orchestration logic.
3.  **Instrumentation & Metrics Report**: Data from instrumented test runs showing agent behavior in real-time.
4.  **End-to-End Diagnostic Test Report**: Results and analysis from a new test harness designed to replicate the failure.
5.  **Recommendation Memo**: A final data-driven recommendation on whether to proceed with the Minimal Fix Path or escalate to a Supervisor-based solution.

---

## Sprint Tasks (1-Week Timeline)

### Day 0: Sanity Check (1-2 Hours)
*   **Objective**: Ensure we aren't about to solve a problem that has already been addressed.
*   **Tasks**:
    1.  **Review Git History**: Check `git log` and `gh pr list` on the `feature/phase-2-validation-fix` branch for recent commits or pending PRs related to orchestration.
    2.  **Code Search**: Briefly search for key function calls (e.g., `_wait_for_task_completion`) to understand usage patterns and identify potential areas of concern.

### Day 1-2: Incident Post-Mortem
*   **Objective**: Reconstruct the failure event to form a root-cause hypothesis.
*   **Tasks**:
    1.  Gather logs from the last 3 failed runs (agent logs, Orchestrator stdout/stderr).
    2.  Dump and analyze the state of Redis `tasks` and `tasks.done` streams at the time of failure.
    3.  Reconstruct the event timeline: which process failed first, with what exit code or exception.
    4.  Formulate a primary hypothesis: was it a zombie subprocess, blocking I/O, Redis deadlock, unhandled exception, etc.?

### Day 2-3: Code Audit
*   **Objective**: Pinpoint specific code-level issues in the orchestration logic.
*   **Tasks**:
    1.  Review `scripts/router.py` for `subprocess.Popen` management issues.
    2.  Audit `OrchestratorAgent` for flawed `_wait_for...` loops, missing timeouts, or incorrect error handling.
    3.  Identify specific code patterns that could be fixed with <200 lines of code (e.g., adding heartbeats, timeouts, robust error handling).

### Day 3-4: Instrumentation & Live Metrics
*   **Objective**: Move from forensics to live observation.
*   **Tasks**:
    1.  Add lightweight "heartbeat" pings from each spawned agent process back to Redis.
    2.  Centralize logging for agent start/stop/crash events, duration, and memory usage.
    3.  Run a controlled "synthetic" experiment (e.g., 3 small documents) and observe the instrumented system in real-time.

### Day 4-5: End-to-End Diagnostic Harness
*   **Objective**: Reliably reproduce the failure under controlled conditions.
*   **Tasks**:
    1.  Build a minimal test harness script (`scripts/diagnostic_harness.py`).
    2.  The harness will enqueue a simple experiment, wait for completion, and assert that synthesis and review tasks were correctly created.
    3.  Run 5-10 trials in parallel to measure success/failure rate, timing, and resource footprints.
    4.  Use the harness to confirm the bottleneck or failure point with hard data.

### Day 5: Minimal Fix Spike & Comparison
*   **Objective**: Test the proposed minimal fix against the baseline failure.
*   **Tasks**:
    1.  Implement a simple, 50-LOC worker-pool to replace the current `subprocess.Popen` logic.
    2.  Rerun the diagnostic harness with the worker-pool implementation.
    3.  Directly compare the success rate and latency metrics against the baseline.

### Day 6: Synthesis & Recommendation
*   **Objective**: Produce the final decision-making document.
*   **Tasks**:
    1.  Synthesize the findings from the Post-Mortem, Audit, Metrics, Harness, and Spike into a concise, 1-page memo.
    2.  Conclude with a clear, data-driven recommendation:
        *   **If success rate ≥ 95% and latency is acceptable**: Proceed with the Minimal Fix Path and defer the Supervisor migration.
        *   **Otherwise**: Justify a lightweight, feature-flagged Supervisor pilot (using static templates and long-lived workers) based on the specific failure mode that the minimal fix could not address.

---

## Definition of Done
*   Incident Post-Mortem document is complete with a root-cause hypothesis.
*   Code Audit checklist is produced with 3-5 actionable findings.
*   Instrumentation metrics dashboard (or log file analysis) is available.
*   Diagnostic Test Report shows success/failure rates, logs, and resource usage.
*   Minimal Fix prototype exists and its comparative results are documented.
*   Final Recommendation Memo is delivered to stakeholders. 