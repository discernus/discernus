# Discernus CLI Configuration Guide

**Comprehensive guide to configuration files, environment variables, and settings hierarchy.**

## Configuration Overview

Discernus uses a hierarchical configuration system that follows modern CLI tool conventions:

**Priority Order (highest to lowest):**
1. **CLI arguments** - Direct command-line options
2. **Environment variables** - `DISCERNUS_*` variables  
3. **Configuration files** - YAML files with settings
4. **Built-in defaults** - Sensible defaults for all options

## Configuration Files

### File Discovery

Discernus automatically searches for configuration files in this order:

1. **Current directory**: `.discernus.yaml`, `discernus.yaml`
2. **Parent directories**: Walk up to project root (looks for `.git` or `pyproject.toml`)
3. **Home directory**: `~/.discernus.yaml`, `~/discernus.yaml`
4. **XDG config directory**: `~/.config/discernus/config.yaml`

### File Format

Configuration files use YAML format with clear sections:

```yaml
# Discernus Configuration
# This file configures default settings for the Discernus CLI
# All settings can be overridden by environment variables (DISCERNUS_*)
# or CLI arguments

# Model Configuration
analysis_model: vertex_ai/gemini-2.5-flash-lite
synthesis_model: vertex_ai/gemini-2.5-pro

# Execution Options
auto_commit: true
skip_validation: false
ensemble_runs: 1

# Output Options
verbose: false
quiet: false
no_color: false
progress: true

# Advanced Options
dry_run: false
force: false
```

### Creating Configuration Files

#### Quick Setup
```bash
# Create default config in current directory
discernus config init

# Create config in specific location
discernus config init ~/.config/discernus/config.yaml

# Overwrite existing config
discernus config init --force
```

#### Manual Creation
Create `.discernus.yaml` in your project root:

```yaml
# Project-specific configuration
analysis_model: vertex_ai/gemini-2.5-pro
synthesis_model: vertex_ai/gemini-2.5-pro
auto_commit: true
skip_validation: false
verbose: true
```

### Configuration Validation

```bash
# Validate current config file
discernus config validate

# Validate specific config file  
discernus config validate /path/to/config.yaml

# Show current configuration
discernus config show
```

## Environment Variables

### Variable Naming Convention

All environment variables use the `DISCERNUS_` prefix with uppercase names:

| Configuration Key | Environment Variable | Type | Description |
|------------------|---------------------|------|-------------|
| `analysis_model` | `DISCERNUS_ANALYSIS_MODEL` | string | Default analysis model |
| `synthesis_model` | `DISCERNUS_SYNTHESIS_MODEL` | string | Default synthesis model |
| `auto_commit` | `DISCERNUS_AUTO_COMMIT` | boolean | Auto-commit successful runs |
| `skip_validation` | `DISCERNUS_SKIP_VALIDATION` | boolean | Skip experiment validation |
| `ensemble_runs` | `DISCERNUS_ENSEMBLE_RUNS` | integer | Number of ensemble runs |
| `verbose` | `DISCERNUS_VERBOSE` | boolean | Enable verbose output |
| `quiet` | `DISCERNUS_QUIET` | boolean | Enable quiet output |
| `no_color` | `DISCERNUS_NO_COLOR` | boolean | Disable colored output |
| `progress` | `DISCERNUS_PROGRESS` | boolean | Show progress indicators |
| `dry_run` | `DISCERNUS_DRY_RUN` | boolean | Enable dry-run mode |
| `force` | `DISCERNUS_FORCE` | boolean | Force operations |

### Boolean Values

Environment variables accept these boolean values:
- **True**: `true`, `True`, `TRUE`, `1`, `yes`, `Yes`, `YES`
- **False**: `false`, `False`, `FALSE`, `0`, `no`, `No`, `NO`

### Usage Examples

#### Development Environment
```bash
# .env file for development
export DISCERNUS_ANALYSIS_MODEL=vertex_ai/gemini-2.5-flash-lite
export DISCERNUS_SYNTHESIS_MODEL=vertex_ai/gemini-2.5-flash-lite
export DISCERNUS_VERBOSE=true
export DISCERNUS_AUTO_COMMIT=false
```

#### Production Environment
```bash
# Production settings
export DISCERNUS_ANALYSIS_MODEL=vertex_ai/gemini-2.5-flash
export DISCERNUS_SYNTHESIS_MODEL=vertex_ai/gemini-2.5-pro
export DISCERNUS_VERBOSE=false
export DISCERNUS_AUTO_COMMIT=true
```

#### CI/CD Environment
```bash
# GitHub Actions / CI settings
export DISCERNUS_QUIET=true
export DISCERNUS_NO_COLOR=true
export DISCERNUS_AUTO_COMMIT=false
export DISCERNUS_DRY_RUN=true  # For validation runs
```

## Configuration Hierarchy Examples

### Example 1: CLI Override

**Config file** (`.discernus.yaml`):
```yaml
analysis_model: vertex_ai/gemini-2.5-flash-lite
synthesis_model: vertex_ai/gemini-2.5-pro
```

**Environment variable**:
```bash
export DISCERNUS_ANALYSIS_MODEL=vertex_ai/gemini-2.5-flash
```

**CLI command**:
```bash
discernus run --analysis-model vertex_ai/gemini-2.5-pro
```

**Result**: Uses `vertex_ai/gemini-2.5-pro` (CLI argument wins)

### Example 2: Environment Override

**Config file** (`.discernus.yaml`):
```yaml
analysis_model: vertex_ai/gemini-2.5-flash-lite
auto_commit: true
```

**Environment variables**:
```bash
export DISCERNUS_ANALYSIS_MODEL=vertex_ai/gemini-2.5-pro
export DISCERNUS_AUTO_COMMIT=false
```

**CLI command**:
```bash
discernus run  # No model specified
```

**Result**: 
- Uses `vertex_ai/gemini-2.5-pro` (env var overrides config)
- Uses `auto_commit: false` (env var overrides config)

### Example 3: Config File Default

**Config file** (`.discernus.yaml`):
```yaml
analysis_model: vertex_ai/gemini-2.5-pro
synthesis_model: vertex_ai/gemini-2.5-flash
verbose: true
```

**CLI command**:
```bash
discernus run  # No overrides
```

**Result**: Uses all settings from config file

## Advanced Configuration Patterns

### Project-Specific Configuration

Create `.discernus.yaml` in each research project:

```yaml
# Project: Political Discourse Analysis
analysis_model: vertex_ai/gemini-2.5-pro  # High-quality analysis needed
synthesis_model: vertex_ai/gemini-2.5-pro # Publication-quality synthesis
auto_commit: true                          # Track all changes
verbose: true                              # Detailed logging
ensemble_runs: 3                           # Multiple runs for reliability
```

### User-Wide Configuration

Create `~/.config/discernus/config.yaml` for personal defaults:

```yaml
# Personal defaults across all projects
analysis_model: vertex_ai/gemini-2.5-flash-lite  # Cost-effective
synthesis_model: vertex_ai/gemini-2.5-pro        # Quality synthesis
auto_commit: true                                 # Always track results
verbose: false                                    # Clean output
no_color: false                                   # Colored output enabled
```

### Environment-Specific Configuration

#### Development
```yaml
# .discernus.dev.yaml
analysis_model: vertex_ai/gemini-2.5-flash-lite
synthesis_model: vertex_ai/gemini-2.5-flash-lite
dry_run: true
verbose: true
auto_commit: false
```

#### Production
```yaml
# .discernus.prod.yaml
analysis_model: vertex_ai/gemini-2.5-flash
synthesis_model: vertex_ai/gemini-2.5-pro
dry_run: false
verbose: false
auto_commit: true
ensemble_runs: 3
```

Use with:
```bash
# Development
discernus --config .discernus.dev.yaml run

# Production
discernus --config .discernus.prod.yaml run
```

### Team Configuration

For research teams, create a shared configuration:

```yaml
# team-config.yaml - Shared team settings
analysis_model: vertex_ai/gemini-2.5-flash
synthesis_model: vertex_ai/gemini-2.5-pro
auto_commit: true
skip_validation: false
ensemble_runs: 3

# Standardized output settings
verbose: false
quiet: false
progress: true
```

Team members can use:
```bash
# Use team config with personal overrides
DISCERNUS_VERBOSE=true discernus --config team-config.yaml run
```

## Configuration Best Practices

### 1. Layered Configuration Strategy

```
├── ~/.config/discernus/config.yaml    # Personal defaults
├── project/.discernus.yaml             # Project-specific settings  
├── DISCERNUS_* environment variables   # Environment overrides
└── CLI arguments                       # Command-specific overrides
```

### 2. Model Selection Strategy

**Development Phase:**
```yaml
analysis_model: vertex_ai/gemini-2.5-flash-lite  # Fast, cheap
synthesis_model: vertex_ai/gemini-2.5-flash-lite # Fast iteration
```

**Testing Phase:**
```yaml
analysis_model: vertex_ai/gemini-2.5-flash       # Production quality
synthesis_model: vertex_ai/gemini-2.5-flash      # Good quality
```

**Publication Phase:**
```yaml
analysis_model: vertex_ai/gemini-2.5-pro         # Highest quality
synthesis_model: vertex_ai/gemini-2.5-pro        # Publication ready
```

### 3. Output Configuration

**Interactive Use:**
```yaml
verbose: false    # Clean output
quiet: false      # Normal verbosity
no_color: false   # Colored output
progress: true    # Show progress bars
```

**CI/CD Use:**
```yaml
verbose: false    # Minimal output
quiet: true       # Script-friendly
no_color: true    # No ANSI colors
progress: false   # No progress bars
```

**Debugging:**
```yaml
verbose: true     # Show all details
quiet: false      # Full output
no_color: false   # Colored for readability
progress: true    # Show progress
```

### 4. Git Integration

**Research Projects:**
```yaml
auto_commit: true     # Track all results
```

**Development:**
```yaml
auto_commit: false    # Manual control
```

**CI/CD:**
```yaml
auto_commit: false    # Don't commit in CI
```

## Troubleshooting Configuration

### Check Current Configuration

```bash
# Show all configuration sources and values
discernus config show

# Show with verbose details
discernus --verbose config show
```

### Validate Configuration

```bash
# Validate current config
discernus config validate

# Validate specific config file
discernus config validate /path/to/config.yaml
```

### Debug Configuration Issues

```bash
# Show verbose output to see config loading
discernus --verbose run --dry-run

# Check environment variables
env | grep DISCERNUS_

# Test configuration hierarchy
discernus --verbose config show
```

### Common Configuration Errors

#### Invalid YAML Syntax
```bash
$ discernus config validate
❌ Config validation failed: Invalid YAML syntax at line 5
Error: Config validation failed
# Exit code: 6
```

**Solution**: Check YAML indentation and syntax

#### Unknown Configuration Keys
```bash
$ discernus config validate
✅ Config file is valid: .discernus.yaml
⚠️  Unknown configuration keys (will be ignored): analysys_model
```

**Solution**: Fix typo in configuration key

#### File Not Found
```bash
$ discernus --config missing.yaml run
❌ Config file not found: missing.yaml
Error: Config file not found
# Exit code: 5
```

**Solution**: Check file path and permissions

## Migration Guide

### From v1.x Configuration

If you have old configuration files, migrate to the new format:

**Old format** (not supported):
```yaml
models:
  analysis: vertex_ai/gemini-2.5-flash-lite
  synthesis: vertex_ai/gemini-2.5-pro
options:
  auto_commit: true
```

**New format**:
```yaml
analysis_model: vertex_ai/gemini-2.5-flash-lite
synthesis_model: vertex_ai/gemini-2.5-pro
auto_commit: true
```

### Environment Variable Changes

**Old variables** (not supported):
```bash
DISCERNUS_MODEL_ANALYSIS=vertex_ai/gemini-2.5-flash-lite
DISCERNUS_MODEL_SYNTHESIS=vertex_ai/gemini-2.5-pro
```

**New variables**:
```bash
DISCERNUS_ANALYSIS_MODEL=vertex_ai/gemini-2.5-flash-lite
DISCERNUS_SYNTHESIS_MODEL=vertex_ai/gemini-2.5-pro
```

---

*For command reference, see [CLI_COMMAND_REFERENCE.md](CLI_COMMAND_REFERENCE.md). For best practices, see [CLI_BEST_PRACTICES.md](CLI_BEST_PRACTICES.md).*