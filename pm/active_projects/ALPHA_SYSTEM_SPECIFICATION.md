# Alpha System Specification v1.0
**Date**: July 25, 2025  
**Status**: Active Specification - Implementation Ready  
**Purpose**: Define unambiguous requirements for first production-ready iteration

---

## 1. SCOPE AND BOUNDARIES

### **What This Alpha System MUST Do**
End-to-end processing of **arbitrary specification-compliant experiments** with:
- **Single-batch corpus size** (fits in one Gemini 2.5 Pro request ~350 documents)
- **No human intervention** once process starts
- **Complete provenance logging** in experiment results package
- **Meaningful per-document analysis** + **human-readable synthesis**

### **What This Alpha System WILL NOT Do**
- Multi-batch processing or statistical run management
- Rate limiting or quota management  
- Advanced error recovery or retry logic
- Statistical optimization or variance analysis
- Complex validation beyond file existence checks

---

## 2. CRITICAL IMPLEMENTATION PRINCIPLE

### **Infrastructure Inventory First**
**MANDATORY FIRST STEP**: Before writing any new code, implementers MUST:

1. **Survey existing infrastructure** - Review `/scripts/router.py`, existing agents in `/discernus/agents/`, Redis streams usage, and MinIO integration patterns
2. **Identify working components** - Determine which orchestration, analysis, and coordination systems already exist and function
3. **Document gaps vs duplication** - Clearly identify what needs to be built NEW vs what can be leveraged/extended
4. **Justify new code** - Any new infrastructure must have explicit justification for why existing systems cannot be extended

**RATIONALE**: Previous implementations ignored existing working infrastructure (router.py, OrchestratorAgent, AnalyseBatchAgent, etc.) and built parallel systems, violating THIN principles and creating unnecessary complexity.

**VALIDATION**: Implementation plan must include inventory of existing systems and explicit gap analysis before proposing new components.

---

## 3. CORE REQUIREMENTS

### **R1: Arbitrary Experiment Processing**
**REQUIREMENT**: System processes any specification-compliant experiment without modification.

**VALIDATION**: Three diverse test experiments (defined in Section 4) must run successfully.

**ANTI-PATTERN**: Hardcoded framework names, corpus structures, or experiment-specific logic.

### **R2: Zero Intervention Execution**
**REQUIREMENT**: Once `discernus run <experiment_path>` is executed, system completes without human interaction.

**VALIDATION**: All three test experiments complete from start to finish without manual steps.

**ANTI-PATTERN**: Manual agent spawning, environment debugging, or result verification steps.

### **R3: Rails Architecture Usage**
**REQUIREMENT**: System uses existing Redis streams, MinIO storage, and agent coordination infrastructure.

**VALIDATION**: No custom execution scripts. All processing via orchestrator agents and task streams.

**ANTI-PATTERN**: Direct agent calls, subprocess execution, or bypassing coordination layer.

### **R4: Complete Provenance Logging**
**REQUIREMENT**: Every system action logged with timestamps, hashes, and full traceability.

**VALIDATION**: Experiment run folder contains complete audit trail readable by external researchers.

**ANTI-PATTERN**: Missing logs, incomplete timestamps, or opaque system actions.

---

## 4. TECHNICAL ARCHITECTURE

### **4.1 Input Validation (Deterministic Only)**
```
APPROVED FOLDER STRUCTURE:
projects/
  <experiment_name>/
    experiment.yaml          # Experiment specification
    framework.md            # Framework specification  
    corpus/                 # Corpus directory
      document1.txt
      document2.txt
      ...
```

**VALIDATION LOGIC**:
1. Parse `experiment.yaml` for declared assets
2. Verify all referenced files exist in approved locations
3. Reject experiments referencing assets outside project folder
4. No LLM validation - pure file system checks

### **4.2 Execution Flow (Non-Blocking Rails)**
```
1. VALIDATION → 2. RUN SETUP → 3. BATCH ANALYSIS → 4. SYNTHESIS → 5. REPORT GENERATION
     ↓              ↓                ↓                 ↓              ↓
  File checks   Run folder     AnalyseBatchAgent  SynthesisAgent  ReportAgent
              + provenance    + Gemini 2.5 Pro   + results      + final report
```

**COORDINATION**: Each stage creates tasks in Redis streams, agents process asynchronously.

### **4.3 Run Folder Structure**
```
projects/<experiment_name>/runs/<timestamp>/
  manifest.json              # Run metadata + hashes
  logs/                      # Complete execution logs
    validation.log
    batch_analysis.log  
    synthesis.log
    report_generation.log
  assets/                    # Hashed experiment inputs
    <framework_hash>.md
    <prompt_hash>.yaml
    <document_hash1>.txt
    <document_hash2>.txt
    ...
  results/                   # Hashed outputs
    batch_analysis/
      <response_hash1>.json
      <response_hash2>.json 
      ...
    synthesis/
      <synthesis_hash>.md
    reports/
      <final_report_hash>.md
```

### **4.4 CLI Specification**
**REQUIREMENT**: All system interaction MUST occur through a standardized CLI.

| Command | Description |
|---|---|
| `discernus run <experiment_path>` | The primary execution command. Initiates the full, end-to-end process: validation, run setup, batch analysis, synthesis, and report generation. This is the only command that executes the pipeline. |
| `discernus validate <experiment_path>` | Performs deterministic file system validation only (per Section 3.1). Checks for correct folder structure and file existence. Provides a quick sanity check before execution. |
| `discernus list` | Scans the `projects/` directory and lists all valid experiment folders it finds, acting as a simple discovery mechanism. |

### **4.5 Configuration Management**
**REQUIREMENT**: All system components MUST be initialized with consistent configuration.

1.  **Centralized `.env` File**: All configuration variables (Redis host, MinIO credentials, API keys) MUST be stored in a single `.env` file at the project root.
2.  **CLI Responsibility**: The `discernus` CLI application is responsible for loading this configuration file upon startup.
3.  **Environment Inheritance**: All spawned agents and sub-processes MUST inherit this consistent environment, ensuring uniform access to infrastructure and services. This directly addresses previous environment and credential-passing failures.

### **4.6 Prompt Management & Provenance**
**REQUIREMENT**: Agent intelligence MUST be externalized, and its state MUST be captured for provenance.

1.  **External Prompts**: All agent prompts MUST be defined in external `prompt.yaml` files located within their respective agent directories (e.g., `discernus/agents/AnalyseBatchAgent/prompt.yaml`).
2.  **"DNA" Provenance**: During the "Run Setup" phase, the system MUST:
    a. Read the exact `prompt.yaml` file for each agent involved in the pipeline.
    b. Save a copy of each prompt file into the run's `assets/` directory.
    c. Record the SHA-256 hash of each saved prompt in the `manifest.json` file.
    
This ensures that the exact "DNA" of every agent at the time of execution is permanently and verifiably stored with the experiment results.

### **4.7 Inter-Agent Task Contracts**
**REQUIREMENT**: Internal coordination messages MUST be simple, deterministic, and contain no business logic. These are internal "order tickets" for the software infrastructure; they are never seen by an LLM.

**Coordination Model**: Each agent, upon successful completion of its task, is responsible for enqueuing the task for the subsequent stage. This creates a THIN, decentralized, and reliable workflow.

**Example Task Contracts (JSON on Redis Stream)**:

*   **Task: `analyse_batch`**
    ```json
    {
      "task_type": "analyse_batch",
      "run_id": "20250726T100000Z",
      "framework_hash": "abc...",
      "corpus_document_hashes": ["def...", "ghi..."],
      "agent_prompt_hash": "jkl..."
    }
    ```
*   **Task: `synthesize_results`**
    ```json
    {
      "task_type": "synthesize_results",
      "run_id": "20250726T100000Z",
      "analysis_result_hashes": ["mno...", "pqr..."],
      "agent_prompt_hash": "stu..."
    }
    ```

### **4.8 Standardized Logging Schema**
**REQUIREMENT**: All log entries MUST be structured for machine-readability and consistent analysis.

1.  **Format**: Logs MUST be written in JSONL format (one JSON object per line).
2.  **Standard Fields**: Every log entry MUST contain the following fields: `timestamp` (ISO 8601), `run_id`, `agent_name`, `stage`, `log_level` (`INFO`, `WARN`, `ERROR`), and `message`.

### **4.9 BaseAgent Abstraction & Error Reporting**
**REQUIREMENT**: Agent boilerplate MUST be abstracted to enforce consistency and THIN principles.

1.  **`BaseAgent` Class**: All agents MUST inherit from a common `discernus.core.BaseAgent` abstract class.
2.  **Boilerplate Responsibility**: This base class will handle non-negotiable infrastructure tasks:
    *   Loading configuration from the environment.
    *   Initializing connections to Redis and MinIO.
    *   Setting up the standardized JSONL logger.
    *   Implementing a consistent `report_fatal_error` method.
3.  **THIN Focus**: This abstraction allows the agent-specific code to be purely focused on its core task: preparing a prompt, calling an LLM, and saving the resulting artifact.

---

## 5. TEST EXPERIMENTS

### **5.1 Three Diverse Experiments (To Be Built)**

**Experiment A: Political Rhetoric Analysis**
- **Framework**: Civic Virtue Framework (CFF) variant
- **Corpus**: 15-20 diverse political speeches
- **Expected Output**: Constitutional health scores per document

**Experiment B: Corporate Communications Analysis** 
- **Framework**: Business Ethics Framework variant
- **Corpus**: 15-20 corporate earnings calls/statements
- **Expected Output**: Ethical positioning analysis per document

**Experiment C: Academic Discourse Analysis**
- **Framework**: Temporal Relevance Framework variant  
- **Corpus**: 15-20 academic papers (abstracts/conclusions)
- **Expected Output**: Temporal relevance scores per document

### **5.2 Specification Compliance Validation**
**PROCESS**: Use `prompt_engineering_harness.py` to validate each experiment package:

```bash
# Test each experiment for specification compliance
python3 scripts/prompt_engineering_harness.py \
  --model "anthropic/claude-3-5-sonnet-20240620" \
  --experiment "projects/political_rhetoric_analysis" \
  --prompt-file "validation_prompts/specification_compliance.txt"
```

**SUCCESS CRITERIA**: Claude responds "Yes, these documents comply with their specifications and are coherent as a set."

**FAILURE ACTION**: Fix specifications until validation passes for all three experiments.

---

## 6. SYSTEM INTERFACE

### **6.1 Command Line Interface**
```bash
# Primary execution command
discernus run projects/<experiment_name>

# Validation only (no execution)
discernus validate projects/<experiment_name>

# List all experiments
discernus list

# Show run status
discernus status projects/<experiment_name>/runs/<timestamp>
```

### **6.2 Output Contracts**

**Per-Document Analysis Format**:
```json
{
  "document_id": "<hash>",
  "document_name": "original_filename.txt", 
  "framework_analysis": {
    "dimension_1": {"score": 0.75, "evidence": "..."},
    "dimension_2": {"score": 0.32, "evidence": "..."}
  },
  "processing_metadata": {
    "timestamp": "2025-07-25T14:30:00Z",
    "model": "vertex_ai/gemini-2.5-pro",
    "tokens_used": 2450
  }
}
```

**Human-Readable Synthesis Format**:
```markdown
# Experiment Results: <experiment_name>

## Executive Summary
[2-3 paragraph overview of key findings]

## Methodology 
[Framework applied, corpus characteristics, processing details]

## Detailed Findings
[Per-dimension analysis with supporting evidence]

## Appendix
- Run ID: <timestamp>
- Framework Hash: <hash>
- Corpus Hash: <hash>
- Processing Time: <duration>
```

---

## 7. SUCCESS CRITERIA

### **7.1 Core Acceptance Tests**
- [ ] **Test A**: Political Rhetoric experiment completes end-to-end without intervention
- [ ] **Test B**: Corporate Communications experiment completes end-to-end without intervention  
- [ ] **Test C**: Academic Discourse experiment completes end-to-end without intervention
- [ ] **Architecture**: All processing uses Redis/MinIO rails (no custom scripts)
- [ ] **Provenance**: Complete audit trail in each run folder
- [ ] **Outputs**: Human-readable results that make intuitive sense

### **7.2 Robustness Tests**
- [ ] **Invalid Experiment**: System gracefully rejects malformed experiment with clear error
- [ ] **Missing Assets**: System detects and reports missing corpus files
- [ ] **Path Traversal**: System rejects experiments referencing files outside project folder
- [ ] **Concurrent Runs**: System handles multiple experiment runs simultaneously

### **7.3 Quality Gates**
- [ ] **No Hardcoding**: System works with unseen experiment types
- [ ] **Complete Logging**: External researcher can understand full process from logs
- [ ] **Readable Results**: Non-technical user can understand experiment outcomes

---

## 8. ANTI-PATTERNS (FORBIDDEN)

### **❌ What NOT to Build**
1. **Custom execution scripts** that bypass orchestration layer
2. **Hardcoded framework logic** specific to test experiments  
3. **Manual intervention points** requiring user debugging
4. **Incomplete logging** missing timestamps or provenance hashes
5. **Opaque processing** where system actions aren't auditable
6. **Test-only functionality** that doesn't generalize to new experiments

### **❌ Implementation Smells**
- If you're manually spawning agents → use Rails coordination
- If you're hardcoding experiment names → build generic processing
- If you need manual intervention → fix the automation
- If logging is incomplete → capture everything with timestamps
- If it only works with test data → build for arbitrary inputs

---

## 9. EXTRA CREDIT FEATURES

### **9.1 Runtime Dashboard**
**CLI Interface**: Real-time progress display during execution
```
🔄 Discernus Alpha - Experiment: political_rhetoric_analysis
┌─────────────────────────────────────────────────────────┐
│ ✅ Validation Complete        (2s)                      │
│ ✅ Run Setup Complete         (1s)                      │  
│ 🔄 Batch Analysis Running     (Est: 4m 30s remaining)   │
│ ⏳ Synthesis Pending                                    │
│ ⏳ Report Generation Pending                            │
└─────────────────────────────────────────────────────────┘
```

### **9.2 Agent-Scriptable Mode**
**Shell Environment**: Cursor agents can inspect and control system state
```bash
# Agent-friendly status output
discernus status projects/test_experiment --format=json
discernus logs projects/test_experiment/runs/latest --tail
discernus debug projects/test_experiment --show-redis-state
```

---

## 10. IMPLEMENTATION PHASES

### **Phase 1: Test Asset Creation (2-3 days)**
1. Build three diverse experiment packages
2. Validate compliance using prompt engineering harness
3. Refine specifications until all experiments pass validation

### **Phase 2: Core System Implementation (3-4 days)**
1. Build CLI interface (`run`, `validate`, `list`) with validation logic.
2. Implement `BaseAgent` abstraction and standardized logging.
3. Implement run folder creation and full provenance logging (including prompt "DNA").
4. Connect to existing Rails coordination using defined Inter-Agent Task Contracts.
5. Implement `AnalyseBatchAgent`, `SynthesisAgent`, `ReportAgent`.

### **Phase 3: Integration Testing (1-2 days)**
1. Run all three test experiments end-to-end via `discernus run`.
2. Verify complete provenance logging
3. Validate human-readable outputs
4. Fix any automation gaps

### **Phase 4: Extra Credit (Optional)**
1. Runtime dashboard implementation
2. Agent-scriptable mode
3. Performance optimization

---

## 11. DEFINITION OF DONE

**The Alpha System is complete when:**

1. **All three test experiments** run successfully from `discernus run` command
2. **Zero human intervention** required once execution starts
3. **Complete provenance logging** captured in run folders
4. **Human-readable results** produced for each experiment
5. **Architecture compliance** - uses Rails, no custom scripts
6. **Arbitrary experiment capability** - works with unseen spec-compliant inputs

**Acceptance Test**: A new Cursor agent can run any of the three test experiments successfully without guidance beyond this specification document.

---

**This specification eliminates ambiguity about what constitutes a "real system" versus a demo. Future agents must build to these exact requirements.** 