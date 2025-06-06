# Narrative Gravity Maps - Changelog

## [v2025.06.04] - 2025-06-06

### Major Features Added

#### 🚀 Universal Multi-Run Dashboard System
- **NEW**: `create_generic_multi_run_dashboard.py` - Fully generalized multi-run analysis dashboard
- **Auto-Detection**: Automatically extracts speaker, year, framework from filenames using regex patterns
- **Framework Agnostic**: Works with any framework structure (civic virtue, custom, unknown)
- **Parameter Override**: Manual parameters can override auto-detection when needed
- **Statistical Rigor**: Maintains all variance analysis, confidence intervals, and visualization quality

#### 🔍 Smart Auto-Detection Features
- **Filename Parsing**: Recognizes common patterns like `speaker_year_framework_timestamp.json`
- **Framework Detection**: Auto-detects civic virtue or provides generic integrative/disintegrative categorization
- **Metadata Extraction**: Pulls run count, model info, dates, job IDs with graceful fallbacks
- **Error Handling**: Robust fallbacks for missing or malformed data

#### 📊 Enhanced LLM Integration
- **Generic Prompting**: Framework-agnostic composite summary generation
- **Variance Analysis**: Pure statistical analysis with technical focus
- **Dynamic Templates**: No hardcoded speaker or framework references

### Technical Improvements

#### 🏗️ Architecture Generalization
- **Parameter-Driven Design**: Transformed hardcoded Obama-specific system to universal tool
- **Function Signature**: `create_dashboard(results_file, speaker=None, year=None, speech_type=None, framework=None)`
- **Backwards Compatibility**: Works with all existing JSON file formats and naming conventions

#### 📁 Project Organization
- **Archive Structure**: Moved development versions to `archive/development_versions/`
- **Documentation**: Added comprehensive guides in `docs/generalization/`
- **Test Outputs**: Organized development visualizations in `archive/test_outputs/`

### Files Added

1. **`create_generic_multi_run_dashboard.py`** - Main generalized dashboard system (674 lines)
2. **`test_auto_detection.py`** - Auto-detection capability demonstration (113 lines)
3. **`docs/generalization/GENERIC_DASHBOARD_USAGE.md`** - Comprehensive usage documentation (204 lines)
4. **`docs/generalization/GENERALIZATION_SUMMARY.md`** - Technical transformation details (216 lines)
5. **`CHANGELOG.md`** - This file documenting changes

### Files Moved to Archive

#### Development Versions (`archive/development_versions/`)
- `create_obama_elliptical_dashboard_v4.py` through `v8.py` (5 versions)
- `create_obama_elliptical_enhanced_v2.py` and `v3.py`
- `create_obama_elliptical_viz.py`
- `generate_obama_summary.py`
- `parse_obama_results.py`
- `test_multi_run_obama.py`

#### Test Outputs (`archive/test_outputs/`)
- `obama_dashboard_v*.png` (multiple versions)
- `obama_elliptical_enhanced*.png` (multiple versions)

### Documentation Updates

#### README.md Enhancements
- **NEW Section**: Multi-Run Analysis Dashboard System with usage examples
- **Quick Start**: Added command-line and programmatic usage examples
- **Feature Overview**: Comprehensive description of auto-detection capabilities

#### PROJECT_STRUCTURE.md Updates
- **Archive Organization**: Documented new archive structure
- **Core Components**: Added generalized dashboard and test files
- **Documentation Structure**: Added generalization documentation section

### Migration Path

#### For Existing Users
1. **Immediate Compatibility**: Use new system with existing files
   ```bash
   python create_generic_multi_run_dashboard.py obama_multi_run_civic_virtue_20250606_142731.json
   ```

2. **Enhanced Usage**: Add parameters for better control
   ```bash
   python create_generic_multi_run_dashboard.py results.json --speaker "Lincoln" --year "1863"
   ```

3. **New Workflows**: Apply to any speaker/framework
   ```bash
   python create_generic_multi_run_dashboard.py new_analysis.json
   ```

### Success Criteria Met

✅ **Dynamic Input Handling** - Auto-detects run count, framework, metadata  
✅ **Flexible Title Generation** - Dynamic speaker/year/framework extraction  
✅ **Framework Agnostic Design** - Works with any framework structure  
✅ **LLM Prompt Generalization** - No hardcoded references, fully generic  
✅ **Technical Architecture** - Parameter-driven with auto-extraction logic  
✅ **Quality Preservation** - Maintains all visual and statistical rigor  
✅ **Backwards Compatibility** - Works with existing files and formats  

### Impact

**Before**: Hardcoded system limited to Obama civic virtue analysis  
**After**: Universal tool for multi-run narrative gravity analysis across any domain, speaker, or framework

The transformation maintains 100% of the original quality while providing maximum flexibility and minimal configuration requirements.

---

## Previous Versions

### [v2025.01.05] - Framework Modularization
- Modular architecture with multiple framework support
- Automated prompt generation system
- Framework switching capabilities

### [v1.0] - Initial Release
- Obama-specific civic virtue analysis
- Basic elliptical visualization
- Single-run analysis capability 