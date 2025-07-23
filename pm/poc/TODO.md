# PoC Pending Tasks

- [x] Implement `discernus results <RUN_ID>` CLI command to fetch and organize results by run ID.
- [x] Add export/import functionality: `discernus run --from-manifest runs/<RUN_ID>/manifest.json`.
- [x] Harden cost guard: abort mid-run in live mode when spending exceeds the cap via Lua script.
- [x] Extend run manifest to capture output artifact hashes and generate a human-readable report.
- [x] **COMPLETED 2025-07-23**: Audit all PoC code (including agents) for THIN violations the form of parsing LLM responses

## CRITICAL Discovery: MockRedisClient Gap (2025-07-23)

**Issue**: TaskListExecutorAgent validation revealed that LLM generates mock Redis client instead of using real connection:
- ✅ **LLM correctly interprets** raw task lists (1455 characters successfully parsed)
- ✅ **LLM generates correct Python code** for task enqueueing
- ❌ **LLM creates MockRedisClient** instead of using real Redis connection
- ❌ **Tasks never actually enqueued** - only printed to console

**Root Cause**: TaskListExecutorAgent prompt lacks proper context injection for real Redis client
**Impact**: Pipeline validation complete through task interpretation, but execution bridge missing
**Priority**: HIGH - blocks end-to-end completion

## Next-Step Wishlist (post-PoC)

- [x] Implement `discernus export <RUN_ID>` CLI command to materialize run directory (`corpus/`, `analysis/`, `synthesis/`, `logs/`, `manifest.json`).
- [ ] **URGENT**: Fix TaskListExecutorAgent to execute LLM-generated code with real Redis client instead of mock
- [ ] Precision-aware normalizer & framework `precision` field.
- [ ] Review the PoC code for model, framework, experiment and corpus agnosticism - should not have these hard coded
- [ ] Support `non_deterministic` averaging and `runs_per_chunk`.
- [ ] Build ValidationAgent for custom schema validation.
- [ ] Build PostHocMathAgent for retro metrics analysis.
- [ ] Composite framework synthesis combining multiple analyses.
- [ ] Complete Security package: static policy enforcement in router and deploy SecuritySentinelAgent. 

## Tasks to support Project/Experiment/Run hierarchy

- [ ] Enhance `run` command: accept `--project <PROJECT>` and `--experiment <EXPERIMENT>` options and derive run path accordingly.
- [ ] Update `ArtifactManifestWriter` to write manifests under `projects/<PROJECT>/<EXPERIMENT>/<RUN_ID>/` instead of `runs/`.
- [ ] Modify CLI commands (`pause`, `resume`, `results`) to locate and operate on manifests using the new hierarchical path.
- [ ] Deprecate or alias the old `runs/` directory support for backward compatibility.
- [ ] Update integration tests and docs to use the new directory structure patterns.

## Vanderveen Micro Project Validation

**Status**: THIN Architecture Validated - Execution Bridge Missing

**Major Progress (2025-07-23)**:
- [x] **THIN Pipeline Validation Complete**: OrchestratorAgent → PlanExecutorAgent → TaskListExecutorAgent all working
- [x] **Binary File Processing Validated**: DOCX/PDF files (500KB+) successfully stored in MinIO with SHA256 hashing
- [x] **Framework Agnostic Confirmed**: PDAF v1.3 (complex 10-anchor framework) processed without parsing
- [x] **LLM Interpretation Verified**: Raw 1455-character task lists correctly interpreted by Gemini 2.5 Flash
- [x] **Orchestration Loop Fixed**: Cleared 15 duplicate experiment requests, system no longer loops

**Architecture Validation Results**:
✅ **Content-addressable storage** - Binary files stored/retrieved by SHA256 hash  
✅ **Framework agnostic processing** - No hardcoded PDAF assumptions in infrastructure  
✅ **Raw blob handoffs** - No parsing violations between agents  
✅ **LLM intelligence handling complexity** - 10-anchor framework with mathematical indices processed  

**Critical Gap Identified**:
❌ **Code execution bridge missing** - LLM generates correct task enqueueing code but executes mock instead of real Redis

**Validation Tasks**:
- [x] Run full pipeline test with vanderveen_micro experiment using updated YAML configuration
- [x] Validate AnalyseChunkAgent architecture (THIN compliance confirmed)
- [x] Test binary processing: large DOCX files (488-499KB) and PDF files (700KB-2.9MB)
- [x] Test TaskListExecutorAgent with complex PDAF framework interpretation
- [x] Verify framework complexity handling: LLM successfully parsed and interpreted sophisticated academic frameworks
- [ ] **BLOCKED**: Complete end-to-end analysis (requires TaskListExecutorAgent code execution fix)
- [ ] **BLOCKED**: Validate SynthesisAgent with multi-document analysis synthesis 
- [ ] **BLOCKED**: Check synthesis quality: academic-grade multi-document populist analysis report

**Files Ready**:
- Framework: `projects/vanderveen_micro/framework.md` (PDAF v1.3, 214 lines) ✅ **VALIDATED**
- Experiment: `projects/vanderveen_micro/experiment_binary_test.yaml` (updated with Gemini models) ✅ **VALIDATED**
- Corpus: 7 documents including Trump/Sanders speeches and party platforms ✅ **VALIDATED** 
- Target: `projects/vanderveen_micro/pdaf_replication/run_001/` (new academic structure) ⏳ **READY**

**Next Agent Priority**: Fix TaskListExecutorAgent MockRedisClient issue to complete end-to-end validation 