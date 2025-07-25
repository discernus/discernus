# Experiment: Attesor Orchestrator Smoke Test
## Validate THIN Orchestrator Changes Before Full Study

**Date**: January 13, 2025  
**Framework**: PDAF v1.1 (Sanitized)  
**Analysis Type**: Minimal system validation  
**Expected Duration**: 5-10 minutes  
**Purpose**: Validate THIN orchestrator changes work correctly

---

## Objective

Test that the newly THIN-compliant orchestrator can:
1. Read experiment requirements correctly
2. Choose RAW_AGGREGATION workflow (no synthesis)
3. Process a small corpus without bias isolation failure
4. Generate clean output for validation

---

## Methodology

**Minimal Test Design**:
- **Corpus**: 2 speeches only (Romney, McCain - both sanitized)
- **Models**: Multi-model test (Claude 3.5 Sonnet + Gemini 2.5 Flash)
- **Condition**: Sanitized English only (no bias testing)
- **Workflow**: RAW_AGGREGATION (no adversarial synthesis)

**Success Criteria**:
- Orchestrator correctly chooses RAW_AGGREGATION workflow
- No synthesis/moderation/referee agents spawned
- Clean anchor scores without synthesis contamination
- Complete analysis in under 10 minutes

---

## Multi-Model Configuration

Test multi-model execution capabilities:

```yaml
models:
  - anthropic/claude-3-5-sonnet-20240620
  - vertex_ai/gemini-2.5-flash
num_runs: 1
remove_synthesis: true
```

---

## Expected Outputs

**Validation Targets**:
1. **Workflow Selection**: Logs show "RAW_AGGREGATION" chosen
2. **Agent Spawning**: Only analysis agents, no synthesis agents
3. **Score Collection**: Raw PDAF anchor scores collected
4. **Multi-Model Execution**: Both models process corpus successfully

This smoke test validates the orchestrator changes are working correctly before running the full 864-analysis Attesor study.

---

## Implementation Notes

**Quick Setup**:
```bash
# Copy minimal corpus
cp corpus/sanitized_english/sanitized_speech_f9b8c2d7.md experiments/01_smoketest/corpus/
cp corpus/sanitized_english/sanitized_speech_a1c5e7d2.md experiments/01_smoketest/corpus/

# Copy framework
cp pdaf_v1.1_sanitized_framework.md experiments/01_smoketest/

# Run validation
python3 -c "from discernus.agents.validation_agent import ValidationAgent; ValidationAgent().validate_and_execute_sync('experiments/01_smoketest/pdaf_v1.1_sanitized_framework.md', 'experiments/01_smoketest/smoketest_experiment.md', 'experiments/01_smoketest/corpus')"
```

**Failure Modes to Watch For**:
- Orchestrator chooses ADVERSARIAL_SYNTHESIS (would indicate experiment parsing failure)
- Synthesis agents spawn despite remove_synthesis: true
- Analysis takes longer than expected (would indicate infrastructure issues)

This minimal test validates infrastructure before the full study commitment. 