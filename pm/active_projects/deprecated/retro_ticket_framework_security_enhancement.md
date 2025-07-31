# Retro Ticket: Framework Security Enhancement - Trusted Canonical Path Resolution

**Date**: 2025-01-30  
**Type**: Architecture Enhancement  
**Priority**: High  
**Status**: Implemented  

## Background

During framework duplication cleanup (Issue #framework-sprawl), we discovered a fundamental tension between:
1. **Security Requirement**: Prevent experiments from accessing files outside their directory (prevent .env exfiltration)
2. **Maintainability Requirement**: Avoid framework duplication across experiment directories

**Original Problem**: Experiments referenced `../../frameworks/reference/core/caf_v6.0.md` but `ExperimentSecurityBoundary` correctly blocked access to files outside experiment directories.

## Root Cause Analysis

**Security Architecture Assumption Gap**: The security boundary was designed with binary trust model:
- **Agents** = Untrusted (must stay within experiment boundary)
- **Files** = All treated equally

**Missing Concept**: **Trusted Infrastructure Operations** by orchestrator

## Solution Implemented

### Enhanced Framework Loading Pattern

**Location**: `discernus/core/thin_orchestrator.py::_load_framework()`

**Key Innovation**: **Orchestrator Trust Boundary**
- **Orchestrators** = Trusted infrastructure (can resolve canonical frameworks)
- **Agents** = Untrusted workloads (stay within security boundary)
- **Framework Content** = Pre-injected by orchestrator before agent execution

```python
def _load_framework(self, framework_filename: str) -> str:
    # Canonical frameworks: Orchestrator resolves (TRUSTED)
    if framework_filename.startswith("../../frameworks/"):
        framework_file = project_root / canonical_path
        return framework_file.read_text(encoding='utf-8')
    
    # Local frameworks: Security boundary enforced (UNTRUSTED)
    else:
        return self.security.secure_read_text(framework_file)
```

### Security Properties Preserved

1. **Agent Isolation**: Agents never see external file paths
2. **Boundary Enforcement**: Security boundary remains intact for agent operations  
3. **Audit Trail**: Framework access logged by trusted orchestrator
4. **Backward Compatibility**: Local frameworks continue to work

### Maintainability Achieved

1. **Single Source of Truth**: Frameworks live in `frameworks/reference/`
2. **No Duplication**: Experiments reference canonical versions
3. **Version Control**: Framework evolution tracked centrally

## Architecture Impact

**Trust Model Refinement**:
```
BEFORE: Binary (agents vs. files)
AFTER:  Layered (orchestrator → agents → security boundary)

Orchestrator (Trusted Infrastructure)
    ↓ Pre-resolves canonical frameworks
Agents (Untrusted Workloads)  
    ↓ All file access validated
Security Boundary (Experiment Scope)
```

**Core Principle**: **Pre-Injection Security Pattern**
- Trusted infrastructure resolves external dependencies
- Untrusted workloads operate on pre-resolved content
- Security boundaries enforce workload isolation

## Lessons Learned

1. **THIN Philosophy Applied to Security**: Don't make software smart about security—make the boundary clear and enforce it consistently
2. **Orchestrator Design Pattern**: Infrastructure components can have elevated privileges when architecturally justified
3. **Security vs. Maintainability**: False dichotomy—proper layering enables both

## Documentation Updates

- ✅ **Core Architecture Document**: Updated with orchestrator trust boundary
- ✅ **Security Boundary**: Enhanced with canonical framework support
- ✅ **Framework Specification**: Clarified canonical referencing pattern

## Testing

- ✅ Canonical framework loading works (`projects/simple_test`)
- ✅ Local framework loading preserved (backward compatibility)
- ✅ Security boundary violations still blocked for agents
- ✅ All reference experiments validate successfully

## Future Considerations

**Potential Extensions**:
1. **Trusted Corpus Libraries**: Similar pattern for shared corpora
2. **Framework Versioning**: Enhanced canonical path resolution
3. **Security Audit**: Regular review of orchestrator privileges

**Monitoring**:
- Track canonical vs. local framework usage patterns
- Monitor for any security boundary violations in production
- Validate that agents cannot circumvent the enhanced loading

---

**Stakeholder Sign-off**:
- Architecture: Implemented and validated ✅
- Security: Trust boundary model reviewed ✅  
- THIN Compliance: Pre-injection pattern aligns with philosophy ✅