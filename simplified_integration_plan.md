# THIN Synthesis Architecture: Pre-Alpha Integration Plan

## Current Reality Check
- This is **pre-alpha development**, not production
- We can move aggressively without extensive migration planning
- The "production" system is really just the current development codebase
- Users are developers/researchers, not production customers

## Simplified Integration Approach

### Phase 1: Close Prototype Issues ✅
- Issues #167-171: Mark as complete (prototype validated)
- Issue #166: Update to "Phase 1 Complete, Phase 2 Ready"
- Issue #165: Close as superseded

### Phase 2: Direct Integration (2-3 weeks)
**Goal**: Move working prototype into main codebase

#### Issue #175: Replace Legacy Synthesis with THIN Architecture
**Scope**: Direct replacement, not parallel implementation
- Move 4-agent pipeline from prototype to `discernus/agents/`
- Update ThinOrchestrator to use THIN synthesis by default
- Replace EnhancedSynthesisAgent with ThinSynthesisPipeline
- Use existing SecureCodeExecutor (enhance if needed)
- Use existing MinIO artifact system

#### Issue #176: Infrastructure Integration
**Scope**: Use existing infrastructure, don't rebuild
- Integrate with existing LocalArtifactStorage/MinIO
- Use existing AuditLogger for experiment provenance
- Use existing SecurityBoundary for experiment isolation
- External YAML prompts (following existing patterns)

#### Issue #177: Validation and Testing
**Scope**: Ensure it works with existing experiments
- Test with existing framework types (CAF, PDAF, CFF)
- Run on existing experiment projects
- Fix any integration issues that arise
- Update CLI if needed (minimal changes)

## What This Actually Looks Like

### Week 1: Move Components
- Copy prototype agents to `discernus/agents/thin_synthesis/`
- Update imports and dependencies
- Integrate with existing LLM gateway
- Basic integration testing

### Week 2: Infrastructure Integration  
- Replace temporary files with artifact storage
- Integrate with existing orchestration
- Update CLI to use new synthesis
- Test with real experiments

### Week 3: Validation and Cleanup
- Test across different frameworks
- Fix any issues found
- Clean up prototype directory
- Update documentation

## Success Criteria
- THIN synthesis works as drop-in replacement for legacy synthesis
- Existing experiments run successfully with new architecture
- Performance meets or exceeds legacy approach
- Token truncation issues resolved

## Pre-Alpha Benefits
- **Move fast**: No backward compatibility constraints
- **Break things**: If something doesn't work, fix it directly
- **Simple testing**: Just run existing experiments
- **Direct feedback**: Users are developers who can adapt

This is a **3-week integration project**, not a 12-week enterprise migration.
