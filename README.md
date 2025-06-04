# Elliptical Moral Gravity Wells Framework

A quantitative framework for analyzing the moral forces driving political narratives using elliptical geometry and gravity well positioning.

## Overview

The Elliptical Moral Gravity Wells framework positions ten moral "gravity wells" on an elliptical boundary, with integrative wells (Dignity, Truth, Justice, Hope, Pragmatism) in the upper half and disintegrative wells (Tribalism, Manipulation, Resentment, Fantasy, Fear) in the lower half. Political narratives are positioned inside the ellipse based on their gravitational pull from these boundary wells.

## Key Features

### 🎯 **Comprehensive Analysis**
- **10 Moral Dimensions**: Five integrative and five disintegrative gravity wells
- **Elliptical Geometry**: Vertically elongated ellipse emphasizing moral elevation
- **Advanced Metrics**: Moral Elevation, Polarity, Coherence, and Directional Purity scores
- **Visual Positioning**: Narratives plotted based on weighted gravitational forces

### 🔄 **Interactive Workflow** 
- **Multi-file Analysis**: Compare multiple political texts in a single session
- **Progressive Insights**: Each analysis builds on previous ones for comparative understanding
- **LLM Integration**: Works with any AI model (GPT-4, Claude, Gemini, etc.)
- **Smart File Handling**: Automatic downloadable JSON outputs when supported

### 📊 **Professional Visualizations**
- **Enhanced Filename Generation**: Content-aware naming with vendor/model attribution
- **Publication Quality**: High-resolution outputs with proper typography and spacing
- **Comparative Analysis**: Side-by-side visualization of multiple narratives
- **Automatic Summaries**: 500-character analysis summaries with intelligent text fitting

## Quick Start

### Prerequisites
```bash
python 3.8+
matplotlib
numpy
seaborn
```

### Installation
```bash
git clone https://github.com/your-repo/moral-gravity-analysis
cd moral-gravity-analysis
pip install -r requirements.txt
```

### Basic Usage

**Single Analysis:**
```bash
python moral_gravity_elliptical.py path/to/analysis.json
```

**Comparative Analysis:**
```bash
python moral_gravity_elliptical.py analysis1.json analysis2.json analysis3.json
```

## Interactive LLM Analysis

### Using the Interactive Prompt

1. **Copy the prompt** from `reference_prompts/5_dipole_interactive_prompt_v2025.01.03.19.45.txt`
2. **Paste into your preferred LLM** (GPT-4, Claude, Gemini, etc.)
3. **Upload your first political text** when prompted
4. **Receive JSON analysis + commentary**
5. **Continue with additional files** for comparative insights

### Example Workflow
```
You → Paste interactive prompt into ChatGPT
LLM → "Please upload your first political narrative file"
You → Upload speech/manifesto/article
LLM → Provides JSON + detailed analysis + asks for next file
You → Upload second text
LLM → Provides analysis + comparison with first file
...continue building comprehensive analysis
```

## Analysis Framework

### Moral Gravity Wells

**Integrative Wells (Upper Ellipse):**
- **Dignity** (90°): Individual moral worth, universal rights, pluralism
- **Truth** (30°): Intellectual honesty, evidence engagement, transparency
- **Justice** (150°): Impartial fairness, rule-based processes, inclusion
- **Hope** (60°): Grounded optimism, realistic paths forward
- **Pragmatism** (120°): Evidence-based solutions, feasibility focus

**Disintegrative Wells (Lower Ellipse):**
- **Tribalism** (270°): Group dominance, in-group/out-group framing
- **Manipulation** (210°): Information distortion, emotional exploitation
- **Resentment** (330°): Grievance-centered, moral scorekeeping
- **Fantasy** (240°): Denial of trade-offs, utopian promises
- **Fear** (300°): Threat amplification, danger exaggeration

### Calculated Metrics

- **Moral Elevation**: Vertical position normalized by ellipse height (-1.0 to 1.0)
- **Moral Polarity**: Distance from center normalized by ellipse dimensions (0.0 to 1.0)
- **Coherence**: Consistency of gravitational pull direction (0.0 to 1.0)
- **Directional Purity**: Alignment with vertical moral axis (-1.0 to 1.0)

## Example Analyses

The `model_output/` directory contains example analyses across the political spectrum:

### Historical Speeches
- **Nelson Mandela 1994 Inaugural**: Reconciliation and hope-centered
- **Hugo Chávez 2006 UN Speech**: Populist critique with tribalism elements

### Contemporary Political Texts
- **Left Center Positive**: "A Shared Future" - dignity and institutional reform
- **Left Center Negative**: "Redemption Through Reckoning" - grievance-based manifesto
- **Right Center Positive**: "Stewarding Freedom" - conservative renewal vision
- **Right Center Negative**: "Take Back Our Nation" - fear and tribal mobilization

## File Organization

```
moral_gravity_analysis/
├── moral_gravity_elliptical.py      # Main framework
├── reference_prompts/               # Current and historical prompts
│   ├── 5_dipole_interactive_prompt_v2025.01.03.19.45.txt
│   └── older_versions/
├── reference_texts/                 # Example political texts
├── model_output/                    # Generated analyses and visualizations
├── requirements.txt
└── README.md
```

## Filename Convention

All generated files follow the pattern:
```
YYYY_MM_DD_HHMMSS_[vendor]_[model]_[content_identifier].[extension]
```

Examples:
- `2025_06_03_214802_openai_gpt_4_a_shared_future_equity_through_dignity_and_democra.png`
- `2025_06_03_214914_openai_gpt_4_take_back_our_nation_the_time_for_mercy_is_over.json`

## Advanced Features

### Comparative Visualizations
```bash
python moral_gravity_elliptical.py file1.json file2.json
# Generates: timestamp_model_comparative_content1_vs_content2.png
```

### Cross-Model Analysis
The framework supports analyses from multiple AI models:
- OpenAI GPT-4 (`openai_gpt_4`)
- Anthropic Claude (`anthropic_claude_sonnet_4`)
- Google Gemini (`google_gemini_pro`)
- Custom models (automatic detection from metadata)

### Academic Integration
- **Mathematical Foundation**: Based on elliptical geometry and gravitational physics
- **Reproducible Analysis**: Standardized JSON format with version tracking
- **Publication Ready**: High-quality visualizations with proper academic formatting

## Contributing

This framework is designed for academic research into political discourse analysis. Contributions should maintain the mathematical rigor and visualization quality standards.

## License

See LICENSE file for details.

## Citation

If you use this framework in academic work, please cite:
```
Whatcott, J. (2025). Elliptical Moral Gravity Wells Framework v2.0: 
Interactive Analysis of Political Narrative Moral Forces. 
```

## Version History

- **v2.0 (2025.01.03)**: Major enhancement with interactive workflow and advanced features
  - Interactive LLM prompt system for multi-file comparative analysis
  - Enhanced filename generation with content identification and vendor/model attribution
  - Professional visualization system with automatic text fitting
  - Comprehensive comparative analysis capabilities
  - Support for multiple AI models (GPT-4, Claude, Gemini, etc.)
- **v1.0**: Initial elliptical framework with basic analysis capabilities 
