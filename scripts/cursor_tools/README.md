# Cursor Tools

This directory contains specialized tools designed to support Cursor AI agent development and resolve common environment issues that agents encounter.

## Tools

### `check_environment.py`
**Purpose**: Verify development environment setup for Cursor agents  
**Usage**: `python3 scripts/cursor_tools/check_environment.py`  
**Features**:
- Python command confusion detection (python vs python3)
- macOS-specific environment validation
- Package availability checking
- Common agent confusion pattern detection
- Development environment diagnostics

**Integration**: ✅ **ACTIVELY USED** in Makefile (`make check`)

### `safe_python.sh`
**Purpose**: Safe Python command wrapper for Cursor agents  
**Usage**: `./scripts/cursor_tools/safe_python.sh <command> [args...]`  
**Features**:
- Handles python vs python3 confusion
- macOS environment issue resolution
- Safe command execution with proper error handling
- Colored output for better visibility
- Agent-friendly command patterns

**Integration**: ✅ **ACTIVELY USED** in Makefile (`make run-safe`, `make debug-safe`)

### `prevent_nested_repos.py`
**Purpose**: Prevent and detect nested Git repositories that break provenance  
**Usage**: `python3 scripts/cursor_tools/prevent_nested_repos.py [options]`  
**Features**:
- Nested repository detection and cleanup
- Provenance system protection
- Automated scanning and reporting
- Integration with Git workflows
- Research integrity preservation

### `python_wrapper.py`
**Purpose**: Python execution wrapper with enhanced error handling  
**Usage**: `python3 scripts/cursor_tools/python_wrapper.py <script> [args...]`  
**Features**:
- Enhanced error reporting for agent debugging
- Environment validation before execution
- Standardized output formatting
- Integration with Cursor agent workflows

## Common Agent Issues Addressed

### 1. Python Command Confusion
**Problem**: Agents often confuse `python` vs `python3` commands  
**Solution**: `safe_python.sh` and `check_environment.py` detect and resolve this

### 2. macOS Environment Issues  
**Problem**: macOS has complex Python environment setup (Homebrew, system, user)  
**Solution**: Environment checking and safe execution wrappers

### 3. Nested Repository Problems
**Problem**: Agents accidentally create nested Git repos, breaking provenance  
**Solution**: `prevent_nested_repos.py` detects and prevents this critical issue

### 4. Package Availability
**Problem**: Agents assume packages are available without checking  
**Solution**: Environment validation before execution

## Integration Status

✅ **ACTIVELY INTEGRATED** - These tools are core to the Discernus development workflow:

- **Makefile Integration**: `check_environment.py` and `safe_python.sh` are used in standard make targets
- **Development Workflow**: Essential for reliable agent operation
- **Quality Assurance**: Prevent common development environment issues

## Use Cases

1. **Agent Development**: Ensure reliable execution environment for Cursor agents
2. **Environment Setup**: Validate and configure development environments  
3. **Debugging**: Diagnose and resolve common agent execution issues
4. **Quality Assurance**: Prevent environment-related failures in research workflows

## Makefile Integration

```makefile
check:  ## Check environment setup (run this first!)
	@python3 scripts/cursor_tools/check_environment.py

run-safe:  ## Run experiment with safe Python wrapper
	@./scripts/cursor_tools/safe_python.sh -m discernus.cli run $(EXPERIMENT)
```

## Output Examples

### Environment Check Success
```
🔍 Checking development environment...
✅ Python 3.13.5 detected
✅ Using Homebrew Python (macOS standard)  
✅ All required packages available
✅ Environment ready for Cursor agents
```

### Environment Issues Detected
```
⚠️  'python' command exists - use 'python3' instead
⚠️  Missing package: youtube-transcript-api
❌ Nested repository detected: projects/experiment/.git
```

## Dependencies

- Standard Python libraries (sys, os, subprocess, pathlib)
- Git (for repository management)
- Bash shell (for shell scripts)
- No external Python packages required

## Design Philosophy

These tools follow the **"Magical Incantation"** principle from the Discernus project:
- Prevent costly agent confusion cycles
- Provide immediate orientation and problem resolution
- Enable reliable, repeatable development workflows
- Minimize time spent on environment issues vs. actual research work
