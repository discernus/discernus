# PoC Pending Tasks

- [x] Implement `discernus results <RUN_ID>` CLI command to fetch and organize results by run ID.
- [x] Add export/import functionality: `discernus run --from-manifest runs/<RUN_ID>/manifest.json`.
- [x] Harden cost guard: abort mid-run in live mode when spending exceeds the cap via Lua script.
- [x] Extend run manifest to capture output artifact hashes and generate a human-readable report.

## Next-Step Wishlist (post-PoC)

- [x] Implement `discernus export <RUN_ID>` CLI command to materialize run directory (`corpus/`, `analysis/`, `synthesis/`, `logs/`, `manifest.json`).
- [ ] Precision-aware normalizer & framework `precision` field.
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

**Status**: Ready for complex academic framework testing with PDAF v1.3

**Context**: The vanderveen_micro project contains a sophisticated 10-anchor Populist Discourse Analysis Framework (PDAF v1.3) and real 2016 US political documents (DOCX/PDF). This is a critical validation test for the THIN architecture's ability to handle complex academic research.

**Completed Setup**:
- [x] Updated experiment YAML to use Gemini models (gemini-2.5-flash default)
- [x] Created academic directory structure: `projects/vanderveen_micro/pdaf_replication/run_001/`

**Validation Tasks**:
- [ ] Run full pipeline test with vanderveen_micro experiment using updated YAML configuration
- [ ] Validate AnalyseChunkAgent with complex PDAF framework (10 analytical anchors, mathematical indices)
- [ ] Test binary processing: large DOCX files (488-499KB) and PDF files (700KB-2.9MB)
- [ ] Validate SynthesisAgent with multi-document populist analysis synthesis
- [ ] Verify framework complexity handling: LLM can parse and apply sophisticated academic frameworks
- [ ] Check synthesis quality: academic-grade multi-document populist analysis report
- [ ] Document results as proof-of-concept milestone for complex academic research capability

**Files Ready**:
- Framework: `projects/vanderveen_micro/framework.md` (PDAF v1.3, 214 lines)
- Experiment: `projects/vanderveen_micro/experiment_binary_test.yaml` (updated with Gemini models)
- Corpus: 7 documents including Trump/Sanders speeches and party platforms
- Target: `projects/vanderveen_micro/pdaf_replication/run_001/` (new academic structure) 