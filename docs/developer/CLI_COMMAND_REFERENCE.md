# Discernus CLI Command Reference

**Comprehensive reference for all Discernus CLI commands and options.**

## Global Options

Available on all commands:

| Option | Short | Environment Variable | Description |
|--------|-------|---------------------|-------------|
| `--verbose` | `-v` | `DISCERNUS_VERBOSE` | Enable verbose output with config details |
| `--quiet` | `-q` | `DISCERNUS_QUIET` | Minimal output for scripts and CI |
| `--no-color` | | `DISCERNUS_NO_COLOR` | Disable colored output |
| `--config PATH` | | | Use specific configuration file |
| `--version` | | | Show version and exit |
| `--help` | | | Show help and exit |

## Core Commands

### `discernus run [EXPERIMENT_PATH]`

Execute complete experiment (analysis + synthesis).

**Arguments:**
- `EXPERIMENT_PATH`: Path to experiment directory (default: current directory)

**Options:**
| Option | Environment Variable | Default | Description |
|--------|---------------------|---------|-------------|
| `--dry-run` | `DISCERNUS_DRY_RUN` | `false` | Show what would be done without executing |
| `--analysis-model MODEL` | `DISCERNUS_ANALYSIS_MODEL` | `vertex_ai/gemini-2.5-flash-lite` | LLM model for analysis |
| `--synthesis-model MODEL` | `DISCERNUS_SYNTHESIS_MODEL` | `vertex_ai/gemini-2.5-pro` | LLM model for synthesis |
| `--skip-validation` | `DISCERNUS_SKIP_VALIDATION` | `false` | Skip experiment validation |
| `--analysis-only` | `DISCERNUS_ANALYSIS_ONLY` | `false` | Run analysis only, skip synthesis |
| `--ensemble-runs N` | `DISCERNUS_ENSEMBLE_RUNS` | `1` | Number of ensemble runs |
| `--no-auto-commit` | `DISCERNUS_NO_AUTO_COMMIT` | `false` | Disable automatic Git commit |

**Examples:**
```bash
# Basic execution
discernus run

# With specific models
discernus run --analysis-model vertex_ai/gemini-2.5-pro

# Test run without execution
discernus run --dry-run

# Analysis only for faster iteration
discernus run --analysis-only

# Run from different directory
discernus run /path/to/experiment

# Verbose output with config details
discernus --verbose run --dry-run
```

**Exit Codes:**
- `0`: Success
- `1`: General error
- `3`: Validation failed
- `4`: Infrastructure error

---

### `discernus continue [EXPERIMENT_PATH]`

Intelligently resume experiment from existing artifacts.

**Arguments:**
- `EXPERIMENT_PATH`: Path to experiment directory (default: current directory)

**Options:**
| Option | Environment Variable | Default | Description |
|--------|---------------------|---------|-------------|
| `--synthesis-model MODEL` | `DISCERNUS_SYNTHESIS_MODEL` | `vertex_ai/gemini-2.5-pro` | LLM model for synthesis |
| `--no-auto-commit` | `DISCERNUS_NO_AUTO_COMMIT` | `false` | Disable automatic Git commit |

**Examples:**
```bash
# Resume from cached analysis
discernus continue

# Resume with different synthesis model
discernus continue --synthesis-model vertex_ai/gemini-2.5-flash-lite
```

---

### `discernus list`

List available experiments with status and details.

**No arguments or options.**

**Output:** Professional table showing:
- Status (Valid/Invalid)
- Experiment path
- Experiment name
- Framework used
- Number of corpus files

**Examples:**
```bash
# List all experiments
discernus list

# Quiet listing
discernus --quiet list
```

---

### `discernus status`

Show system status and available commands.

**No arguments or options.**

**Output:** System status tables showing:
- Component status (Local Storage, Git Integration, LLM Gateway)
- Available commands with descriptions

**Examples:**
```bash
# Show system status
discernus status

# Verbose system information
discernus --verbose status
```

---

### `discernus validate [EXPERIMENT_PATH]`

Validate experiment structure and configuration.

**Arguments:**
- `EXPERIMENT_PATH`: Path to experiment directory (default: current directory)

**Options:**
| Option | Description |
|--------|-------------|
| `--skip-coherence` | Skip experiment coherence validation |

**Examples:**
```bash
# Validate current experiment
discernus validate

# Validate specific experiment
discernus validate /path/to/experiment

# Quick structure validation only  
discernus validate --skip-coherence
```

**Exit Codes:**
- `0`: Valid experiment
- `3`: Validation failed

---

### `discernus debug [EXPERIMENT_PATH]`

Interactive debugging mode with detailed agent tracing.

**Arguments:**
- `EXPERIMENT_PATH`: Path to experiment directory (default: current directory)

**Options:**
| Option | Description |
|--------|-------------|
| `--analysis-model MODEL` | LLM model for analysis |
| `--step-by-step` | Enable step-by-step execution |

**Examples:**
```bash
# Interactive debugging
discernus debug

# Debug with specific model
discernus debug --analysis-model vertex_ai/gemini-2.5-pro
```

---

### `discernus artifacts [EXPERIMENT_PATH]`

Show experiment artifacts and available resumption points.

**Arguments:**
- `EXPERIMENT_PATH`: Path to experiment directory (default: current directory)

**Examples:**
```bash
# Show artifacts for current experiment
discernus artifacts

# Show artifacts for specific experiment
discernus artifacts /path/to/experiment
```

---

### `discernus promote [EXPERIMENT_PATH]`

Promote workbench files to operational status.

**Arguments:**
- `EXPERIMENT_PATH`: Path to experiment directory (default: current directory)

**Options:**
| Option | Description |
|--------|-------------|
| `--force` | Force promotion even with conflicts |

**Examples:**
```bash
# Promote workbench files
discernus promote

# Force promotion
discernus promote --force
```

## Configuration Commands

### `discernus config`

Manage Discernus configuration files and settings.

#### `discernus config show`

Display current configuration values and sources.

**Output:** Professional tables showing:
- Configuration file location
- All configuration values with sources (Config/Env/Default)

**Examples:**
```bash
# Show current configuration
discernus config show

# Show config with verbose details
discernus --verbose config show
```

#### `discernus config init [CONFIG_PATH]`

Create a default configuration file.

**Arguments:**
- `CONFIG_PATH`: Path for config file (default: `.discernus.yaml`)

**Options:**
| Option | Description |
|--------|-------------|
| `--force` | Overwrite existing config file |

**Examples:**
```bash
# Create default config in current directory
discernus config init

# Create config in specific location
discernus config init ~/.config/discernus/config.yaml

# Overwrite existing config
discernus config init --force
```

**Exit Codes:**
- `0`: Success
- `5`: File already exists (without --force)

#### `discernus config validate [CONFIG_PATH]`

Validate configuration file syntax and values.

**Arguments:**
- `CONFIG_PATH`: Path to config file (default: auto-discover)

**Examples:**
```bash
# Validate current config file
discernus config validate

# Validate specific config file
discernus config validate /path/to/config.yaml
```

**Exit Codes:**
- `0`: Valid configuration
- `5`: File not found
- `6`: Configuration error

## Advanced Commands

### `discernus workflow`

Chain multiple operations together.

**Examples:**
```bash
# Validate then run
discernus workflow validate run

# Complex workflow
discernus workflow validate run continue
```

### `discernus visualize-provenance [EXPERIMENT_PATH]`

Generate provenance visualization for an experiment.

**Arguments:**
- `EXPERIMENT_PATH`: Path to experiment directory (default: current directory)

**Examples:**
```bash
# Visualize current experiment provenance
discernus visualize-provenance

# Visualize specific experiment
discernus visualize-provenance /path/to/experiment
```

## Legacy Commands

### `discernus start`
**Status:** Removed - no infrastructure services required

### `discernus stop`  
**Status:** Removed - no infrastructure services required

## Model Options

### Available Models

**Analysis Models** (fast, cost-effective):
- `vertex_ai/gemini-2.5-flash-lite` (default)
- `vertex_ai/gemini-2.5-flash`

**Synthesis Models** (high-quality, comprehensive):
- `vertex_ai/gemini-2.5-pro` (default)
- `vertex_ai/gemini-2.5-flash`

### Model Selection Guidelines

**For Analysis:**
- Use `flash-lite` for development and testing
- Use `flash` for production analysis
- Use `pro` for complex analytical frameworks

**For Synthesis:**
- Use `pro` for final reports and publications
- Use `flash` for draft synthesis and iteration

**Cost Optimization:**
- Development: `flash-lite` for both analysis and synthesis
- Production: `flash-lite` analysis + `pro` synthesis
- High-quality: `pro` for both (highest cost, best quality)

## Error Handling

### Exit Codes Reference

| Code | Category | Description | Common Causes |
|------|----------|-------------|---------------|
| 0 | Success | Operation completed successfully | - |
| 1 | General Error | Unexpected runtime error | Network issues, LLM failures |
| 2 | Invalid Usage | Wrong command line arguments | Typos, missing required args |
| 3 | Validation Failed | Experiment structure invalid | Missing files, invalid format |
| 4 | Infrastructure Error | External service unavailable | API limits, network failures |
| 5 | File Error | File system operation failed | File not found, permissions |
| 6 | Configuration Error | Config file invalid | YAML syntax, invalid values |

### Common Error Scenarios

**Exit Code 3 - Validation Failed:**
```bash
$ discernus run
❌ Missing experiment.md in .
Error: Experiment structure validation failed
# Exit code: 3
```

**Exit Code 5 - File Error:**
```bash
$ discernus config validate nonexistent.yaml
❌ Config file not found: nonexistent.yaml
Error: Config file not found: nonexistent.yaml  
# Exit code: 5
```

**Exit Code 6 - Configuration Error:**
```bash
$ discernus config validate invalid.yaml
❌ Config validation failed: Invalid YAML syntax
Error: Config validation failed: Invalid YAML syntax
# Exit code: 6
```

## Shell Integration

### Command Completion

Future versions will support shell completion:

```bash
# Bash
eval "$(_DISCERNUS_COMPLETE=bash_source discernus)"

# Zsh  
eval "$(_DISCERNUS_COMPLETE=zsh_source discernus)"

# Fish
eval "$(_DISCERNUS_COMPLETE=fish_source discernus)"
```

### Scripting Best Practices

```bash
#!/bin/bash
# Example CI/CD script

set -e  # Exit on any error

# Run with quiet output and check exit code
if discernus --quiet run --dry-run; then
    echo "✅ Experiment validation passed"
    discernus --quiet run
else
    echo "❌ Experiment validation failed (exit code: $?)"
    exit 1
fi
```

---

*For quick reference, see [CLI_QUICK_REFERENCE.md](CLI_QUICK_REFERENCE.md). For configuration details, see [CLI_CONFIGURATION_GUIDE.md](CLI_CONFIGURATION_GUIDE.md).*