# Discernus CLI Quick Reference

**Professional computational social science research platform with modern CLI conventions.**

## Essential Commands

```bash
# Run complete experiment (analysis + synthesis)
discernus run

# List available experiments  
discernus list

# Show system status
discernus status

# Create configuration file
discernus config init
```

## Global Options

```bash
# Available on all commands
--verbose, -v     # Show detailed output and config info
--quiet, -q       # Minimal output for scripts/CI
--no-color        # Disable colored output
--config PATH     # Use specific config file
--version         # Show version and exit
```

## Configuration Hierarchy

**Priority Order**: CLI arguments > Environment variables > Config file > Defaults

```bash
# 1. CLI arguments (highest priority)
discernus run --analysis-model vertex_ai/gemini-2.5-pro

# 2. Environment variables
export DISCERNUS_ANALYSIS_MODEL=vertex_ai/gemini-2.5-pro
discernus run

# 3. Config file (.discernus.yaml)
analysis_model: vertex_ai/gemini-2.5-pro

# 4. Built-in defaults (lowest priority)
```

## Quick Start Workflow

```bash
# 1. Navigate to your experiment directory
cd my-research-project

# 2. Create default config (optional)
discernus config init

# 3. List available experiments
discernus list

# 4. Run experiment with verbose output
discernus --verbose run

# 5. Check results
ls runs/*/results/
```

## Common Usage Patterns

### Development & Testing
```bash
# Test experiment structure without execution
discernus run --dry-run

# Skip validation for faster iteration
discernus run --skip-validation

# Analysis only (no synthesis)
discernus run --analysis-only

# Quiet output for scripts
discernus --quiet run
```

### Model Selection
```bash
# Use different models
discernus run --analysis-model vertex_ai/gemini-2.5-flash-lite \
              --synthesis-model vertex_ai/gemini-2.5-pro

# Via environment variables
export DISCERNUS_ANALYSIS_MODEL=vertex_ai/gemini-2.5-flash-lite
export DISCERNUS_SYNTHESIS_MODEL=vertex_ai/gemini-2.5-pro
discernus run
```

### Configuration Management
```bash
# Show current configuration
discernus config show

# Validate config file
discernus config validate

# Create config in specific location
discernus config init ~/.config/discernus/config.yaml
```

### Experiment Management
```bash
# Resume from existing artifacts
discernus continue

# Interactive debugging
discernus debug

# Validate experiment structure
discernus validate

# Promote workbench files
discernus promote
```

## Environment Variables

| Variable | Purpose | Example |
|----------|---------|---------|
| `DISCERNUS_ANALYSIS_MODEL` | Default analysis model | `vertex_ai/gemini-2.5-flash-lite` |
| `DISCERNUS_SYNTHESIS_MODEL` | Default synthesis model | `vertex_ai/gemini-2.5-pro` |
| `DISCERNUS_AUTO_COMMIT` | Auto-commit successful runs | `true` / `false` |
| `DISCERNUS_SKIP_VALIDATION` | Skip experiment validation | `true` / `false` |
| `DISCERNUS_VERBOSE` | Enable verbose output | `true` / `false` |
| `DISCERNUS_QUIET` | Enable quiet output | `true` / `false` |
| `DISCERNUS_NO_COLOR` | Disable colored output | `true` / `false` |

## Exit Codes

| Code | Meaning | Example |
|------|---------|---------|
| 0 | Success | Experiment completed successfully |
| 1 | General error | Unexpected runtime error |
| 2 | Invalid usage | Wrong command line arguments |
| 3 | Validation failed | Missing experiment.md or invalid structure |
| 4 | Infrastructure error | External service unavailable |
| 5 | File error | Config file not found, permission denied |
| 6 | Configuration error | Invalid YAML syntax in config file |

## Directory Structure

Discernus follows standard conventions:

```
my-research-project/
├── .discernus.yaml          # Optional config file
├── experiment.md            # Experiment definition
├── framework.md             # Analysis framework (or path to framework)
├── corpus/                  # Text files to analyze
│   ├── document1.txt
│   └── document2.txt
├── runs/                    # Execution results
│   └── 20240101T120000Z/    # Timestamped run directory
└── shared_cache/            # Cached artifacts for reuse
```

## Professional Features

### Rich Terminal Interface
- **Structured tables** for experiment listings and status
- **Progress indicators** for long-running operations  
- **Professional formatting** with consistent colors and icons
- **Responsive layout** that adapts to terminal width

### Smart Configuration
- **Automatic discovery** of config files in current/parent/home directories
- **XDG Base Directory** specification compliance
- **Validation** with helpful error messages
- **Hierarchical overrides** for flexible workflows

### Research-Focused Design
- **Current directory defaults** - just `cd` to your experiment and run
- **Provenance tracking** with automatic Git commits
- **Cost transparency** with token usage and cost reporting
- **Academic standards** with comprehensive audit trails

## Next Steps

- **Detailed Command Guide**: See `CLI_COMMAND_REFERENCE.md` for complete option documentation
- **Configuration Guide**: See `CLI_CONFIGURATION_GUIDE.md` for advanced config management
- **Best Practices**: See `CLI_BEST_PRACTICES.md` for optimization tips and troubleshooting

---

*For issues or questions, see the [troubleshooting guide](../troubleshooting/TROUBLESHOOTING_GUIDE.md) or [create an issue](https://github.com/discernus/discernus/issues).*