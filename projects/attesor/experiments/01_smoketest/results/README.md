# Smoketest Results Structure

This directory contains validation results for orchestrator functionality testing.

## Expected Files

### 1. `orchestrator_validation.md`
**Purpose**: Human-readable validation of THIN orchestrator changes
**Content**:
- Workflow selection verification (RAW_AGGREGATION chosen)
- Agent spawning confirmation (no synthesis agents)
- Execution time and cost tracking
- Success/failure status with specific details

### 2. `raw_analysis_scores.json`
**Purpose**: Raw PDAF anchor scores for validation
**Content**:
```json
{
  "speech_1": {
    "model": "claude-3.5-sonnet",
    "condition": "sanitized_english",
    "pdaf_scores": {
      "anchor_1_people_elite": 1.2,
      "anchor_2_crisis_urgency": 0.8,
      // ... all 10 anchors
    }
  }
}
```

### 3. `system_logs.jsonl`
**Purpose**: Technical logs for debugging (minimal, focused)
**Content**: Only essential system events, not full conversation

### 4. `validation_report.md`
**Purpose**: Go/no-go decision for proceeding to pilot
**Content**:
- ✅ Orchestrator correctly chose RAW_AGGREGATION
- ✅ No synthesis agents spawned
- ✅ Clean PDAF scores collected
- ✅ Ready for pilot experiment

## Success Criteria

**Infrastructure Validation**:
- [ ] Orchestrator reads experiment requirements correctly
- [ ] RAW_AGGREGATION workflow selected (not ADVERSARIAL_SYNTHESIS)
- [ ] Only analysis agents spawned (no synthesis/moderation/referee)
- [ ] Clean PDAF anchor scores collected
- [ ] Execution completed in < 10 minutes
- [ ] Cost < $1.00

**Decision Point**: If all criteria met → proceed to pilot. If any fail → debug orchestrator before continuing. 