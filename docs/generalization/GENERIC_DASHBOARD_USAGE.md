# Generic Multi-Run Narrative Gravity Analysis Dashboard

A fully generalized version of the multi-run visualization system that can work with any speaker, framework, and text type.

## Overview

This system takes a hardcoded, Obama-specific dashboard and transforms it into a flexible, parameter-driven tool that can analyze any multi-run narrative gravity analysis results.

## Key Features

### 1. **Dynamic Input Handling**
- Works with any multi-run JSON file structure
- Auto-detects run count (not limited to 5 runs)
- Handles any framework (not just civic virtue)
- Extracts speaker/source and year from filename or accepts as parameters

### 2. **Flexible Title Generation**
- **Before**: "Obama 2009 Inaugural Speech - Multi-Run Civic Virtue Analysis Dashboard"
- **After**: "[Speaker] [Year] [Speech/Text Type] - Multi-Run [Framework] Analysis Dashboard"
- Auto-parses from filename or accepts manual parameters

### 3. **Framework Agnostic Design**
- Auto-detects framework structure from JSON data
- Works with any framework's well structure
- Dynamic well categorization (integrative vs disintegrative)
- Gracefully handles unknown frameworks

### 4. **LLM Prompt Generalization**
- Generic prompting for any speech/framework combination
- Framework-agnostic statistical analysis prompts
- No hardcoded references to specific speakers or content

## Function Signature

```python
create_dashboard(results_file, speaker=None, year=None, speech_type=None, framework=None)
```

### Parameters
- `results_file` (required): Path to multi-run results JSON file
- `speaker` (optional): Speaker name (auto-detected from filename if not provided)
- `year` (optional): Year of speech (auto-detected from filename if not provided)  
- `speech_type` (optional): Type of speech/text (defaults to "Speech")
- `framework` (optional): Analysis framework (auto-detected from data if not provided)

## Usage Examples

### 1. Basic Usage (Full Auto-Detection)
```bash
python create_generic_multi_run_dashboard.py results.json
```
The system will automatically extract all metadata from the filename and data structure.

### 2. With Manual Parameters
```bash
python create_generic_multi_run_dashboard.py results.json \
  --speaker "Lincoln" \
  --year "1863" \
  --speech-type "Address" \
  --framework "Civic Virtue"
```

### 3. Partial Override
```bash
python create_generic_multi_run_dashboard.py trump_2017_rally_populist_framework.json \
  --speech-type "Rally Speech"
```
Will auto-detect Trump, 2017, and populist framework, but use "Rally Speech" as the type.

### 4. Custom Output Location
```bash
python create_generic_multi_run_dashboard.py results.json \
  --output "custom_dashboard.png"
```

## Auto-Detection Logic

### Filename Parsing Patterns
The system recognizes these common filename patterns:

1. `speaker_year_framework_timestamp.json`
   - Example: `trump_2017_populist_20250606_142731.json`
   - Extracts: Speaker=Trump, Year=2017, Framework=Populist

2. `speaker_multi_run_framework_timestamp.json`
   - Example: `biden_multi_run_civic_virtue_20250606_142731.json`
   - Extracts: Speaker=Biden, Framework=Civic Virtue

3. `speaker_framework_year.json`
   - Example: `churchill_wartime_rhetoric_1940.json`
   - Extracts: Speaker=Churchill, Framework=Wartime Rhetoric, Year=1940

### Framework Detection
The system automatically detects framework types:

1. **Civic Virtue Framework**: Auto-detected if wells include Dignity, Truth, Hope, Justice, Pragmatism, Tribalism, Manipulation, Fantasy, Resentment, Fear
2. **Unknown Frameworks**: Automatically categorizes first half of wells as integrative, second half as disintegrative
3. **Custom Categories**: Can be extended to recognize other framework patterns

## Preserved Features

### Visual Layout
- Same GridSpec structure with 7 rows and proper spacing
- Elliptical map with narrative center variance display  
- Bar chart with confidence intervals and value labels
- Color-coded panels (blue/darkred borders)
- Forensic footer with complete traceability data

### Statistical Analysis
- Variance calculation across all runs
- Confidence interval computation
- Narrative center coordinate variance
- Category-specific variance comparisons

### LLM Integration
- Composite summary generation (2-3 sentences)
- Pure variance analysis (100 words, technical focus)
- Score-variance relationship discussion
- Framework-agnostic prompting

## Output Structure

The generated dashboard maintains the same professional layout as the original:

```
┌─────────────────────────────────────────────────────────────────┐
│                    [Speaker] [Year] [Type] - Multi-Run         │
│                    [Framework] Analysis Dashboard              │
├─────────────────────┬───────────────────────────────────────────┤
│                     │                                           │
│   Framework Map     │         Bar Chart with                   │
│   (Elliptical)      │      Confidence Intervals                │
│   Mean Scores       │                                           │
│                     │                                           │
├─────────────────────┼───────────────────────────────────────────┤
│   COMPOSITE         │       VARIANCE ANALYSIS                  │
│   SUMMARY           │                                           │
│   (LLM Generated)   │       (LLM Generated)                    │
├─────────────────────┴───────────────────────────────────────────┤
│ Files: xxx.json | Model: xxx | Runs: N | Date: xxx | Job: xxx  │
└─────────────────────────────────────────────────────────────────┘
```

## Technical Architecture

### Core Functions
- `parse_filename_metadata()`: Extracts metadata from filenames
- `detect_framework_structure()`: Auto-detects framework from score data
- `load_and_process_data()`: Loads and processes multi-run results
- `generate_composite_summary()`: Creates framework-agnostic summary
- `generate_variance_analysis()`: Creates statistical variance analysis
- `create_dashboard()`: Main dashboard generation function

### Backward Compatibility
The system maintains full backward compatibility with existing JSON file formats and naming conventions.

## Error Handling

- Graceful fallbacks for missing metadata
- Default values for unknown parameters  
- Clear error messages for file issues
- Framework auto-detection for unknown structures

## Integration

Can be easily integrated into existing workflows:

```python
from create_generic_multi_run_dashboard import create_dashboard

# Generate dashboard programmatically
fig = create_dashboard("my_results.json", speaker="Kennedy", year="1961")
if fig:
    fig.savefig("kennedy_dashboard.png", dpi=300, bbox_inches='tight')
```

## Success Criteria Met

✅ Works with any multi-run JSON file structure  
✅ Automatically adapts to different frameworks  
✅ Generates appropriate titles and forensic data  
✅ Maintains visual quality and statistical rigor  
✅ Requires minimal manual configuration  
✅ Preserves all refined features from the original  

## Migration from Specific Versions

To migrate from speaker-specific versions:

1. Replace hardcoded function calls:
   ```python
   # Old
   from create_obama_elliptical_dashboard_v8 import main
   main()
   
   # New  
   from create_generic_multi_run_dashboard import create_dashboard
   create_dashboard("results.json")
   ```

2. Update file naming conventions to leverage auto-detection
3. Test with existing data to verify compatibility

The generalized system provides the same quality output with maximum flexibility and minimal configuration. 