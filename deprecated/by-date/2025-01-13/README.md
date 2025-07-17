# Deprecated Test Files - January 13, 2025

These test files were deprecated during the transition from the old conversation-based architecture to the new `WorkflowOrchestrator` + Agent Registry system.

## Deprecated Files

### `complete_conversation_test.py`
**Reason**: Uses deprecated `SessionManager`, `MessageRouter`, and `ThinConversationLogger` infrastructure that predates the WorkflowOrchestrator system.

**Replacement**: Use `end_to_end_workflow_test.py` which tests the current WorkflowOrchestrator system.

### `end_to_end_test.py`
**Reason**: Uses deprecated conversation-based infrastructure instead of the agent workflow system.

**Replacement**: Use `end_to_end_workflow_test.py` for integration testing.

### `mvp_test.py`
**Reason**: Tests ultra-thin infrastructure components that are no longer part of the current architecture.

**Replacement**: Use `comprehensive_test_suite.py` for comprehensive framework testing.

### `simple_test.py`
**Reason**: Tests deprecated infrastructure components without LLM dependencies.

**Replacement**: Use `agent_isolation_test_framework.py` for mock-based testing.

## Current Test Architecture

The current system uses:
- `WorkflowOrchestrator` - Main orchestration system
- Agent Registry (`agent_registry.yaml`) - Dynamic agent loading
- `MockLLMGateway` - For testing without API costs
- Framework-agnostic design - Works with any compliant framework

## Migration Notes

If you need to reference the old test logic:
1. The old conversation-based system used `SessionManager` for session management
2. `MessageRouter` handled LLM communication
3. `ThinConversationLogger` managed conversation logging
4. `agent_roles.py` contained hardcoded expert roles (now in agent registry)

The new system eliminates these components in favor of:
- Direct agent execution via registry
- Workflow-based orchestration
- Framework-agnostic data handling
- Comprehensive mock testing infrastructure

## Date Deprecated
January 13, 2025

## Context
Part of systematic cleanup after implementing framework-agnostic architecture and comprehensive test suite upgrade.
