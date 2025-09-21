# DEPRECATED: Unified Synthesis Agent

**Status**: DEPRECATED as of 2025-01-21

**Reason**: This agent was never integrated into the CLI and caused confusion during development. The active synthesis agent is `two_stage_synthesis_agent`.

**Active Agent**: Use `discernus/agents/two_stage_synthesis_agent/` instead.

**Migration**: All synthesis functionality has been consolidated into the TwoStageSynthesisAgent, which is properly integrated with the CLI and orchestration system.

**Files in this directory**:
- `v2_unified_synthesis_agent.py` - Deprecated implementation
- `prompt.yaml` - Deprecated prompt template
- `__init__.py` - Deprecated module init

**Do not use this agent in new code or experiments.**
