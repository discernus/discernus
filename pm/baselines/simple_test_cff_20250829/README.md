# Simple Test CFF Baseline Snapshot - 2025-08-29

## Purpose
Preserved baseline state before implementing 3-run internal self-consistency testing.

## Contents
- **Runs**: 3 baseline runs with different analysis models (Flash Lite, Flash, Pro) + Pro synthesis
- **Shared Cache**: All cached artifacts and functions
- **Experiment Config**: Original experiment.md and framework files
- **Original Prompt**: Using standard EnhancedAnalysisAgent prompt (not 3-run version)

## Baseline Runs
1. **20250829T152852Z**: Flash Lite + Pro synthesis (/bin/zsh.0262, 199,610 tokens)
2. **20250829T153704Z**: Flash + Pro synthesis (/bin/zsh.1773, 230,276 tokens)  
3. **20250829T154643Z**: Pro + Pro synthesis (/bin/zsh.4842, 206,741 tokens)

## Usage
This snapshot preserves the 'before' state for comparison with 3-run variance reduction results.

