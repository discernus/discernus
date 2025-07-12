# DEPRECATION NOTICE: Complex Orchestrator

**Date Deprecated**: January 12, 2025  
**Reason**: Replaced with simple ensemble execution path

## Why This Code Was Deprecated

The `orchestrator.py` in this directory implemented a complex conversation-based orchestration system that had fundamental issues:

1. **Framework Context Loss**: Framework specifications weren't reaching analysis agents properly
2. **LLM Confusion**: Moderator LLMs generated unrelated content instead of following research questions
3. **Over-Complex Architecture**: Violated THIN principles with too much conversation management logic
4. **Unreliable Results**: Multiple test runs failed to produce meaningful analysis

## What Replaced It

**New Simple Ensemble Execution Path**:
1. `ValidationAgent.validate_and_execute_sync()` - validates compatibility (✅ working)
2. `EnsembleOrchestrator` - spawns analysis agents (one per corpus text)
3. `SynthesisAgent` - aggregates results and notes outliers
4. `ModeratorAgent` - orchestrates discussion about outliers only
5. `RefereeAgent` - arbitrates disagreements
6. `FinalSynthesisAgent` - packages results for persistence

## Architecture Philosophy Change

**Old Approach** (Deprecated): Complex conversation orchestration with multiple turns
**New Approach**: Simple linear pipeline with targeted interactions only when needed

This aligns with SOAR v2.0 Developer Briefing Phase 1 priorities and THIN architecture principles.

## Files in This Directory

- `orchestrator.py` - The deprecated complex orchestrator (996 lines)
- This deprecation notice

**Do not use this code.** It has been superseded by the simple ensemble approach. 