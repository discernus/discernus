---
title: Discernus System Architecture - Technical Specification
---

# Discernus System Architecture (v4.0 - THIN Orchestration)

> **Architecture Update**: This document reflects THIN v2.0 approach based on distributed prototype learnings. 
> Core sections (1-4) describe the current direct function call approach. Later sections contain valuable 
> reference content for specifications, development workflows, and operational guidance.

---

## About Discernus

**Discernus** is a computational research platform that amplifies researcher expertise through systematic, reproducible analysis of text corpora. Rather than replacing human judgment, Discernus enables researchers to apply their analytical frameworks at unprecedented scale while maintaining complete transparency and academic integrity.

### What Discernus Does

Discernus transforms research capacity without compromising scholarly control:

**Traditional Approach**: 
- Researcher manually codes documents → Individual analysis → Manual synthesis → Subjective aggregation
- Limited scale, inconsistent application, difficult replication

**Discernus Approach**: 
- Researcher designs framework once → Automated consistent application across corpus → LLM-powered synthesis with computational verification → Transparent, statistically validated results
- Institutional scale, perfect consistency, complete auditability

### Foundational Philosophy

**Human Amplification, Not Replacement**: Researchers retain complete control over analytical approach, interpretation, and synthesis. Discernus provides computational scale and methodological consistency while preserving human expertise and judgment.

**Day-1 Extensibility**: Create unlimited frameworks, experiments, and corpora within specifications. No programming required - analytical approaches expressed in natural language enable immediate research productivity.

**Academic Integrity by Design**: Every calculation verified through code execution, every decision logged for audit, complete provenance for peer review. No hallucinated statistics, no black-box results.

**Empirically Validated Consistency**: LLMs provide more consistent evaluation than human panels at institutional scale, representing global-scale averaging of human perception patterns while eliminating fatigue and bias drift.

### Core Capabilities
- **Unlimited Analytical Frameworks**: Any approach expressible in natural language (political analysis, discourse analysis, content analysis, literary criticism, etc.)
- **Any Text Corpus**: Scales from dozens to thousands of documents with hash-based anonymization for sensitive materials
- **Computational Verification**: All statistics computed and verified - no hallucinated results
- **Complete Transparency**: End-to-end audit trails, variance reporting, confidence intervals, methodological constraints
- **Immediate Collaboration**: Git-based framework and experiment sharing enables academic community building

---

## Fundamental Architectural Principles

These principles guide every design decision in Discernus:

**1. Day-1 Extensibility Through Specifications**
- **Already Extensible**: Researchers can create unlimited frameworks, experiments, and corpora within specifications
- Framework Specification v4.0 enables any analytical approach expressible in natural language
- Experiment Specification v2.0 supports diverse methodological approaches and research designs
- Corpus Specification v2.0 accommodates any text collection with proper preparation
- External YAML prompts allow analytical customization without code changes
- Git-based sharing enables immediate academic collaboration and framework distribution
- *Future: Advanced platform features (core+modules architecture, marketplace, GUI tools) deferred to post-MVP*

**2. Human Intellectual Value Amplification, Not Replacement**
- Real value creation comes from researcher expertise: framework design, corpus curation, experiment methodology
- Discernus amplifies human intuition and domain knowledge rather than substituting for it
- Researchers retain full control over analytical approach, interpretation, and synthesis
- System provides computational scale and consistency while preserving human judgment
- End-to-end transparency enables researchers to audit, validate, and refine their analytical choices
- Post-hoc analysis, synthesis, and scholarly interpretation remain fundamentally human activities
- Technology serves scholarship, not the reverse - researchers drive insights, system provides rigor

**3. Academic Provenance by Design**
- Every decision, artifact, and transformation logged
- Git-based version control for all research materials
- Audit trails sufficient for peer review and replication

**4. Computational Verification ("Show Your Math")**
- LLMs must execute Python code for all mathematical calculations
- Statistical results verified through `SecureCodeExecutor` with resource limits
- No hallucinated statistics - all numbers computed and logged
- Provenance stamps detect content tampering and ensure analysis integrity
- Academic integrity through transparent, auditable computational processes

**5. LLM Consistency Superiority Over Human Evaluation Panels**
- **Fundamental Assumption**: Properly managed LLMs are more consistently perceptive than human evaluator panels
- LLMs represent global-scale averaging of human perception patterns across training data
- Individual humans may be more perceptive, but panels suffer from inconsistency, fatigue, and bias drift
- LLM evaluation provides speed and precision impossible with human panels at institutional scale
- Consistency enables reliable cross-document, cross-time, and cross-researcher comparisons
- Statistical validation (variance measurement, confidence intervals) quantifies this consistency advantage
- This assumption justifies computational methodology over traditional human coding approaches

**6. Variance-Aware Adaptive Processing with Transparency**
- Accept LLM response variance as natural and expected phenomenon (not a bug to fix)
- **Synthetic Calibration**: Generate representative text from corpus using Gemini 2.5 Flash for variance measurement
- **Coefficient of Variation**: Measure CV = σ/μ from pilot runs to determine optimal sample sizes
- **Sequential Probability Ratio Testing (SPRT)**: Adaptive sampling stops when confidence intervals meet requirements
- **Minimum Sample Size Calculation**: n = (z × CV / E)² where z=1.96 (95% confidence), E=desired margin
- **Cost-Constrained Optimization**: Balance statistical confidence with budget through empirical stopping rules
- **Transparency Requirement**: Always report uncertainty, confidence intervals, CV, and methodological constraints
- **Multi-Run Statistical Validation**: Cronbach's alpha, ANOVA, inter-run reliability, and convergence analysis

**7. Reliability Over Flexibility**
- Single, predictable pipeline over infinite customization options
- Boring, bulletproof behavior over theoretical capability
- "It works every time" trumps "it can do anything"
- **Direct function calls over distributed coordination** - proven through prototype experience

**8. Resource-Conscious Cost Management**
- Empirical cost-performance optimization through model selection and batching
- Variance-driven adaptive sampling minimizes unnecessary LLM calls
- Perfect caching eliminates redundant computation on re-runs
- Transparent cost reporting enables institutional budget planning
- *Note: Advanced cost controls and budgeting tools deferred to post-MVP phase*

**9. Specialized Agent Interaction Over Monolithic Analysis**
- Task-specific agents outperform single-LLM approaches (empirically validated)
- Controlled agent conversations through structured protocols and handoffs
- Natural language communication between agents (no complex JSON parsing)
- Sequential validation gauntlet: TrueValidation → ProjectCoherence → StatisticalPlanning → ModelHealth
- Adversarial review protocols: IdeologicalReviewer ↔ StatisticalReviewer → ModeratorSynthesis
- Agent specialization: AnalysisBatch → CorpusSynthesis → Review → Moderation pipeline

**10. Opinionated Model Selection Based on Performance Requirements**
- Context window requirements: 2M+ tokens for multi-framework batch analysis
- Rate limiting needs: 800+ RPM for institutional-scale processing
- Accuracy demands: Consistent performance across full context window
- Empirical validation: Models chosen through actual complexity testing (CHF failure)
- Cost-performance optimization: Gemini 2.5 Pro selected over alternatives
- Provider reliability: Vertex AI chosen for predictable academic pricing

**11. Security and Privacy by Design**
- Corpus anonymization and hash-based identity protection as standard practice
- Secure code execution environments with resource limits for computational verification
- API key management and rate limiting to prevent abuse
- Git-based provenance provides tamper-evident audit trails
- *Note: Full security architecture deferred to post-MVP phase*

**12. Graceful Degradation and Error Recovery**
- Fail-fast validation prevents expensive downstream failures
- Partial artifact preservation on timeout or interruption
- Clear error messages with actionable remediation steps
- System continues processing remaining batches when individual items fail
- *Note: Advanced resilience patterns and retry logic deferred to post-MVP phase*

**13. Intelligence in Prompts, Not Software**
- LLMs handle reasoning, interpretation, and domain knowledge
- Software provides coordination, storage, and deterministic operations only
- Components limited to <150 lines to prevent intelligence creep

**14. Externalized Intelligence, Internalized Coordination**
- Agent prompts live in external YAML files (intelligence belongs outside code)
- Agent discovery uses hardcoded mappings (coordination stays predictable)
- Researchers modify prompts, not coordination logic
- Balances THIN principles with Radical Simplification reliability

**15. Empirical Technology Choices**
- Decisions based on actual testing, not theoretical optimization
- Gemini 2.5 Pro chosen over Flash due to CHF complexity test failure
- Cost optimization secondary to reliability validation

**16. Linear Progression with Perfect Caching**
- Fixed 5-stage pipeline with deterministic progression
- Cache hits eliminate redundant computation entirely
- Predictable resource usage and timing

**17. Artifact-Oriented State Management**
- All data flows through immutable, hashed artifacts in MinIO
- No mutable state in agents or orchestrator
- Perfect reproducibility through artifact chains

**18. Fail-Fast Input Validation**
- Strict contracts enforced at system boundaries
- Clear error messages over expensive debugging cycles
- "Garbage in, clear error out"

---

### The THIN vs THICK Philosophy

**Discernus embodies THIN software architecture principles**:

**THIN Architecture** (Discernus):
- **LLM Intelligence**: Complex reasoning, format detection, framework application handled by language models
- **Software Infrastructure**: Minimal routing, caching, orchestration - no business logic
- **Principle**: "Make it easier to do the right thing and harder to do the wrong thing"
- **Result**: Framework/experiment/corpus agnostic system that adapts to researcher needs

**THICK Architecture** (Traditional Systems):
- **Software Intelligence**: Complex parsing, format-specific processors, hardcoded business rules
- **LLM Usage**: Limited to simple tasks, constrained by software assumptions
- **Problem**: Brittle, framework-specific, requires engineering for each new research approach
- **Result**: Researchers constrained by what software developers anticipated

---

## 1 · Current Implementation Objective

Implement a **reliable, THIN pipeline** based on distributed prototype learnings:

- **Direct function calls** for orchestration - no Redis coordination complexity
- **Multi-stage processing proven effective**: BatchAnalysis → Synthesis → Report produces quality results
- **Artifact-oriented storage** for provenance - MinIO content-addressable storage works well
- **LLM intelligence validated** - agents produce quality academic output when properly coordinated

**Key Learning**: Complex distributed coordination creates reliability problems. The THIN approach uses direct Python function calls while preserving proven agent intelligence and multi-stage processing benefits.

---

## 2 · Core Concepts (Glossary)

| Term | Plain‑English meaning |
| ---- | --------------------- |
| **Redis Stream** | Append‑only log used for firehose logging (not critical path after simplification). |
| **Task Queue (list)** | Redis list used for deterministic completion signalling (no consumer group races). |
| **MinIO** | Local S3‑compatible object store for artefacts. |
| **Artefact** | Any file (JSON, Parquet, prompt) saved by SHA‑256. |
| **Router** | ~150 lines: spawns workers / loads registry; *no business logic*. |
| **Agent** | Stateless worker: *read task → call LLM with prompt → write result*. |
| **OrchestratorAgent** | LLM that plans execution for a fixed 5‑stage pipeline. |

---

## 3 · Architecture Overview (THIN Orchestration)

**THIN v2.0 Core Principle**: Direct function calls, not distributed coordination.

```python
class ThinOrchestrator:
    def run_experiment(self, experiment_path: Path) -> ExperimentResult:
        # 1. Validation
        experiment = self.validate_experiment(experiment_path)
        run_id = self.create_run_folder(experiment)
        
        # 2. Direct agent calls - no Redis coordination
        batch_result = self.batch_agent.analyze(experiment.corpus, experiment.framework)
        synthesis_result = self.synthesis_agent.synthesize([batch_result], experiment.framework)
        final_report = self.report_agent.generate(synthesis_result, experiment.metadata)
        
        # 3. Save results - MinIO for provenance, filesystem for CLI
        self.save_results(run_id, batch_result, synthesis_result, final_report)
        return ExperimentResult(run_id, final_report)
```

**Data Flow**:
```
Input: experiment.yaml + framework.md + corpus/
  ↓ (direct function call)
BatchAnalysis: documents → structured analysis results
  ↓ (direct function call)  
Synthesis: analysis results → statistical aggregation
  ↓ (direct function call)
Report: synthesis results → academic report
  ↓ (direct file write)
Output: results in both filesystem and MinIO
```

---

## 4 · THIN Orchestration Implementation

> **Goal:** Preserve proven agent intelligence while eliminating distributed coordination complexity.

### 4.1 Three-Stage Pipeline (Proven Effective)
```
BatchAnalysis → Synthesis → Report
```
**Validated through distributed prototype**: This pipeline produces quality academic output. Direct function calls eliminate coordination complexity while preserving the proven multi-stage processing benefits.

### 4.2 Direct Function Call Coordination
**THIN v2.0 Approach**: Standard Python patterns replace distributed complexity.

```python
def run_experiment(self, experiment):
    # Standard exception handling, no Redis coordination
    try:
        batch_result = self.batch_agent.analyze(experiment)
        synthesis_result = self.synthesis_agent.synthesize([batch_result])
        final_report = self.report_agent.generate(synthesis_result)
        return final_report
    except Exception as e:
        # Standard Python stack traces show exactly where failure occurred
        self.logger.error(f"Pipeline failed: {e}")
        raise
```

### 4.3 Strict Input Specifications (v3 / v5)
All inputs validated **before** first LLM call.

**Experiment v3** (YAML excerpt):
```yaml
name: "phase3_chf_constitutional_debate"
corpus_path: projects/exp1/corpus/
frameworks: [CAF_v4.3.md, CHF_v1.1.md, ECF_v1.0.md]
statistical_runs: 3   # optional override
```
Constraints: `max_documents`, `max_frameworks_per_run`, **no** `custom_workflow` / `parallel_processing` fields.

**Framework v5**: Markdown file with embedded JSON block declaring `output_contract` (schema) + optional `precision`. Enforced via deterministic validator post‑analysis.

**Corpus v3**: Directory with `manifest.json` listing file names & metadata. System does **no discovery** outside manifest. Binary‑first principle: all files base64 encoded for LLM.

### 4.4 Batch Planner & PreTest
`PreTestAgent` samples corpus to estimate variance & token footprint → returns `recommended_runs_per_batch`.
`BatchPlanner` (inside Orchestrator) uses model registry fields:
- `optimal_batch_tokens` (≈ 70% of context window)
- `max_documents_per_batch`

Generates batch tasks: `{batch_id, text_uris[], framework_hashes[], runs=recommended}`.

### 4.5 AnalyseBatchAgent (Layer 1)
Processes multiple documents + frameworks in one call.
Output schema (per run):
```json
{
  "batch_id": "B01",
  "run_index": 1,
  "framework_scores": {"CAF": {...}, "CHF": {...}},
  "per_doc_notes": {...},
  "batch_summary": "Structured qualitative summary"
}
```
Artefact naming: `analysis/B01.caf<hash>-chf<hash>.run1.json`.

### 4.6 Layered Synthesis & Review

| Layer | Agent(s) | Purpose | Model class |
| ----- | -------- | ------- | ----------- |
| 1 In‑Batch | AnalyseBatchAgent | Raw scores + per‑batch summary | Gemini 2.5 Pro |
| 2 Corpus | CorpusSynthesisAgent | Deterministic aggregation/statistics | Gemini 2.5 Pro |
| 3 Review | 2× ReviewerAgent + ModeratorAgent | Adversarial critique → reconciled narrative | Gemini 2.5 Pro |

`debate/<RUN_ID>.html` captures transcript for audit.

### 4.7 Model Registry
`models/registry.yaml` + `models/provider_defaults.yaml` supply pricing, context windows, and batching parameters.

Example entry:
```yaml
vertex_ai/gemini-2.5-pro:
  provider: vertex_ai
  context_window: 8000000
  costs: {input_per_million_tokens: 1.25, output_per_million_tokens: 5.00}
  task_suitability: [batch_analysis, multi_framework_synthesis, review]
  optimal_batch_tokens: 5600000
  max_documents_per_batch: 300
  last_updated: '2025-07-24'
```

**Note**: Standardized on Gemini 2.5 Pro after Flash reliability failure on CHF complexity test (2025-07-24).

### 4.8 Metrics
Logged per run into `manifest.json`:
- `run_success`: boolean
- `cache_hit_ratio` (re‑run) = skipped_batches / total_batches
- `mean_stage_latency`
- `cost_usd`

### 4.9 Acceptance Criteria
1. **Full Pipeline:** PreTest → BatchAnalysis (≥1 batch) → CorpusSynthesis → Review → Moderation produces artefacts:
   - `analysis/*.json` with `batch_summary`
   - `synthesis/<RUN>.json`
   - `debate/<RUN>.html`
2. **Cache Hit:** Re‑running identical experiment triggers zero Layer‑1 calls (verified via LiteLLM logs).
3. **Cost Guard:** Live mode prompts for confirmation using batch token estimates.
4. **Variance‑Driven Runs:** PreTestAgent sets `runs_per_batch`; system executes that many replicate analyses.
5. **Review Integrity:** Moderator output cites batch summaries and statistics (traceable).
6. **Metrics:** `cache_hit_ratio == 1.0` on second run; success rate ≥95% across test suite.

---

## 5 · Example Commands
```bash
# Start infrastructure
$ docker compose up -d redis minio

# Run experiment with hardcoded 5-stage pipeline
$ python3 scripts/phase3_test_runner.py --test full_pipeline

# Monitor system status
$ python3 scripts/debug_monitor.py

# Check Redis task queues
$ redis-cli xlen orchestrator.tasks
$ redis-cli xlen tasks
```

---

## 6 · Experiment Export & Directory Structure
```
projects/<PROJECT>/<EXPERIMENT>/<RUN_ID>/
├─ corpus/            # original input files
├─ analysis/          # batch JSON artefacts
├─ synthesis/         # <RUN_ID>.json corpus statistics
├─ debate/            # review transcript (html + json)
├─ framework/         # copies of framework files
├─ logs/              # router / agent / proxy logs
├─ manifest.json      # machine provenance (hashes, metrics)
└─ manifest.md        # human summary
```

---

## 7 · Security Controls

### 7.1 Enabled Now
- **Hash Pinning**: All framework/corpus artifacts validated by SHA-256
- **Secrets Scanning**: CLI rejects files matching `/.env($|[._-])/` patterns  
- **Path Validation**: Corpus paths restricted to project boundaries
- **Task Type Validation**: Router enforces allowed task types from agent registry

### 7.2 Deferred (Post-Production)
- **Sandboxing**: Agent containers with `--network none`
- **Sentinel Agent**: Advanced prompt injection detection
- **Audit Logging**: Comprehensive security event logging

---

## 8 · Radical Simplification Constraints

The architecture enforces strict constraints to ensure reliability:

### 8.1 Single Pipeline Path
- **Fixed 5-Stage Sequence**: PreTest → BatchAnalysis → CorpusSynthesis → Review → Moderation
- **No Custom Workflows**: System rejects experiments with `custom_workflow` or `parallel_processing` fields
- **Linear Progression**: Each stage completes before next stage begins
- **Predictable Behavior**: Users know exactly what will happen for any valid experiment

### 8.2 Model Standardization  
- **Single Model**: All stages use `vertex_ai/gemini-2.5-pro` for reliability
- **No Model Selection**: System does not support model choice per stage
- **Proven Reliability**: Model selection based on empirical testing, not cost optimization

### 8.3 Input Contract Enforcement
- **Hash-Required Frameworks**: All frameworks must include valid SHA-256 hashes
- **Manifest-Based Corpus**: Corpus directories require explicit `manifest.json`
- **Specification Compliance**: Bouncer validates against strict Pydantic schemas
- **No Legacy Support**: System rejects v2 specifications with clear upgrade guidance

### 8.4 Architectural Principles
- **THIN Components**: All software components limited to <150 lines
- **No Business Logic**: Intelligence resides in LLM prompts, not software
- **Stateless Agents**: Agents read task → call LLM → write result
- **Artifact-Oriented**: All state persisted as SHA-256 addressable artifacts

---

## 9 · Development Workflow

### 9.1 Local Development Setup
**Docker Infrastructure**:
```bash
# Start development infrastructure
$ docker compose up -d redis minio

# Verify services
$ docker compose ps
$ redis-cli ping  # Should return PONG
$ curl http://localhost:9000  # MinIO console
```

**Virtual Environment**:
```bash
# Activate project environment
$ source venv/bin/activate

# Install development dependencies
$ pip install -r requirements-dev.txt  # TODO: Create dev requirements
```

### 9.2 Agent Testing Harness
**Individual Agent Testing**:
```bash
# Test single agent without full pipeline
$ python3 scripts/test_agent.py --agent PreTestAgent --input test_corpus/

# Mock LLM responses for fast iteration
$ python3 scripts/test_agent.py --agent AnalyseBatchAgent --mock-responses
```

**Prompt Iteration Workflow**:
- Agent prompts stored in `agents/<AgentName>/prompt.yaml`
- Modify prompt → Test with harness → Validate output schema
- Version control tracks prompt evolution

### 9.3 Debugging Individual Stages
**Stage Isolation**:
```bash
# Run only specific pipeline stage
$ python3 scripts/debug_stage.py --stage BatchAnalysis --run-id RUN_001

# Inspect stage artifacts
$ python3 scripts/inspect_artifacts.py --stage CorpusSynthesis --run-id RUN_001
```

**Development Mode**:
- `DEV_MODE=true` enables verbose logging and artifact inspection
- Stages can be run independently with cached inputs
- Mock data generators for consistent testing

*TODO: Implement agent testing harness and stage isolation tools*

---

## 10 · Operational Monitoring

### 10.1 Health Checks
**Infrastructure Health**:
```python
# Health check endpoints
def check_redis_health() -> bool:
    """Verify Redis connectivity and basic operations"""
    # TODO: Implement Redis ping, memory usage, queue depths

def check_minio_health() -> bool:
    """Verify MinIO connectivity and storage"""
    # TODO: Implement MinIO connectivity, bucket access, storage usage

def check_llm_health() -> bool:
    """Verify LLM provider connectivity and quotas"""
    # TODO: Implement Vertex AI health check, quota monitoring
```

### 10.2 Queue Monitoring
**Queue Depth Alerting**:
- Monitor `orchestrator.tasks` stream length
- Alert when queue depth > 100 tasks (indicates processing bottleneck)
- Track average task processing time per agent type

**Performance Baselines**:
- Stage completion times: PreTest ~30s, BatchAnalysis ~5min, Synthesis ~2min
- Queue processing rate: ~10 tasks/minute under normal load
- Memory usage: <2GB RSS per agent process

### 10.3 Cost Tracking Integration
**Real-time Cost Monitoring**:
```bash
# Current experiment cost tracking
$ python3 scripts/cost_monitor.py --run-id RUN_001

# Daily cost summary
$ python3 scripts/cost_monitor.py --daily-summary
```

**Budget Integration**:
- Cost estimates before pipeline execution
- Real-time spend tracking during execution
- Budget alerts when approaching limits

*TODO: Implement comprehensive monitoring infrastructure*

---

## 11 · Error Recovery Patterns

### 11.1 Partial Batch Failure Handling
**Batch-Level Resilience**:
- Individual document failures don't abort entire batch
- Failed documents logged with error details
- Partial batch results preserved and marked as incomplete
- Option to retry failed documents only

**Recovery Strategy**:
```python
class BatchRecovery:
    def handle_partial_failure(self, batch_id: str, failed_docs: List[str]):
        """Preserve successful analyses, retry failures"""
        # TODO: Implement selective retry logic
        pass
```

### 11.2 LLM Rate Limit Backoff
**Adaptive Rate Limiting**:
- Exponential backoff: 1s, 2s, 4s, 8s, 16s, 32s maximum
- Provider-specific rate limit detection
- Automatic retry with backoff for transient failures
- Queue prioritization during rate limit periods

### 11.3 Infrastructure Connection Recovery
**Redis Disconnection Handling**:
- Connection pooling with automatic reconnection
- Task persistence during brief disconnections
- Graceful degradation: log to local files if Redis unavailable

**MinIO Connection Recovery**:
- Retry artifact storage with exponential backoff
- Local caching during MinIO unavailability
- Automatic sync when connection restored

*TODO: Implement robust error recovery mechanisms*

---

## 12 · Corpus Preparation Tools

### 12.1 Manifest Generation
**Automatic Manifest Creation**:
```bash
# Generate manifest.json from directory
$ python3 scripts/generate_manifest.py --corpus-dir projects/exp1/corpus/

# Validate existing manifest
$ python3 scripts/validate_manifest.py --corpus-dir projects/exp1/corpus/
```

**Manifest Schema Validation**:
```json
{
  "version": "3.0",
  "total_documents": 42,
  "documents": [
    {
      "filename": "doc001.txt",
      "sha256": "a1b2c3...",
      "size_bytes": 2048,
      "encoding": "utf-8"
    }
  ],
  "created": "2025-07-24T15:30:00Z"
}
```

### 12.2 Corpus Validation Tools
**Structure Validation**:
- Verify all files in manifest exist and match hashes
- Check encoding consistency across documents
- Validate file size constraints (max 50KB per document)
- Detect and report binary files requiring base64 encoding

**Size Estimation**:
```bash
# Estimate processing cost before run
$ python3 scripts/estimate_corpus_cost.py --corpus-dir projects/exp1/corpus/ --frameworks 3
# Output: ~$45.20 for 3 runs, ~180 minutes processing time
```

### 12.3 Format Conversion Helpers
**Document Processing**:
- PDF to text conversion with page preservation
- DOCX to plain text with metadata extraction
- HTML to text with structure preservation
- Base64 encoding for binary documents

*TODO: Implement corpus preparation toolkit*

---

## 13 · Framework Development Support

### 13.1 Framework Validation Tools
**Pre-run Validation**:
```bash
# Validate framework before expensive processing
$ python3 scripts/validate_framework.py --framework caf_v4.3.md

# Test framework output contract
$ python3 scripts/test_framework_contract.py --framework caf_v4.3.md --sample-text sample.txt
```

**Framework Linting**:
- Check for required sections (anchors, scoring rubrics, output contracts)
- Validate JSON schema in output contracts
- Detect common framework specification errors
- Suggest improvements based on best practices

### 13.2 Example Frameworks
**Reference Implementations**:
- `frameworks/examples/simple_sentiment.md` - Basic binary classification
- `frameworks/examples/multi_dimensional.md` - Complex analytical framework
- `frameworks/examples/comparative.md` - Framework for document comparison

**Framework Templates**:
- Scaffold new frameworks with proper structure
- Include output contract templates
- Provide scoring rubric examples

### 13.3 Framework Testing Methodology
**Systematic Testing**:
1. **Unit Testing**: Single document analysis validation
2. **Consistency Testing**: Same document, multiple runs
3. **Edge Case Testing**: Unusual document formats and content
4. **Performance Testing**: Token usage and processing time

**Output Contract Validation**:
```python
def validate_framework_output(framework_result: dict, expected_schema: dict) -> bool:
    """Ensure framework produces specification-compliant output"""
    # TODO: Implement schema validation with detailed error reporting
    pass
```

*TODO: Implement framework development support tools*

---

## 14 · Implementation Dependencies

### 14.1 Staged Implementation Approach
**Agent Discovery Migration Strategy**:
- **Phase A (Current)**: Maintain hardcoded `AGENT_SCRIPTS` mapping for pipeline completion reliability
- **Phase B (Refactoring)**: Migrate to `agents/<AgentName>/config.json` discovery pattern
- **Justification**: "Reliability > Flexibility" during critical implementation phase
- **Target**: Router discovers agents by scanning `agents/*/config.json` (~50 lines implementation)

**Prompt Storage Specification**:
- **Location**: `agents/<AgentName>/prompt.yaml`
- **Format**: YAML with versioning and metadata
- **Loading**: Agents load prompts at initialization, cache in memory

### 14.2 Complete Dependency Specification
**Core Python Dependencies**:
```txt
# requirements.txt additions
pandas>=2.0.0          # Statistical calculations in CorpusSynthesis
numpy>=1.24.0          # Numerical operations
scipy>=1.10.0          # Advanced statistics
jinja2>=3.1.0          # HTML template generation for Review stage
pydantic>=2.0.0        # Input validation and schemas
```

**Development Dependencies**:
```txt
# requirements-dev.txt (new file)
pytest>=7.0.0          # Testing framework
pytest-mock>=3.10.0    # Mock LLM responses
black>=23.0.0          # Code formatting
mypy>=1.0.0            # Type checking
```

### 14.3 HTML Generation System
**Template Structure**:
```
templates/
├── debate_transcript.html     # Review stage conversation
├── synthesis_report.html      # CorpusSynthesis output
└── base.html                  # Common layout
```

**Template Engine**:
- Jinja2 templates for consistent HTML generation
- CSS embedded for self-contained artifacts
- Mobile-responsive design for review accessibility

*TODO: Create HTML templates and integrate with Review/Moderation stages*

---

*Last updated 2025‑07‑24 - Aligned with Implementation Plan V4 + External Review Feedback*