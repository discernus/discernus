# Storage Architecture for Modular Moral Gravity Wells

## Overview

The modular architecture supports multiple dipole frameworks and generated prompts. This document outlines the recommended storage structure for maintainability, extensibility, and research reproducibility.

## Recommended Directory Structure

```
moral_gravity_analysis/
├── frameworks/                    # Multiple dipole frameworks
│   ├── moral_foundations/         # Original 5-dipole system
│   │   ├── dipoles.json
│   │   ├── framework.json
│   │   └── README.md
│   ├── political_spectrum/        # Alternative: left-right political analysis
│   │   ├── dipoles.json
│   │   ├── framework.json
│   │   └── README.md
│   └── custom_research/           # User-defined frameworks
│       ├── dipoles.json
│       ├── framework.json
│       └── README.md
├── prompts/                       # Generated prompts by framework and version
│   ├── moral_foundations/
│   │   ├── v2025.01.05/
│   │   │   ├── interactive.txt
│   │   │   ├── batch.txt
│   │   │   └── metadata.json
│   │   └── v2025.01.03/
│   │       ├── interactive.txt
│   │       └── metadata.json
│   └── political_spectrum/
│       └── v2025.01.06/
│           ├── interactive.txt
│           └── metadata.json
├── config/                        # Current active configuration (symlink)
│   ├── dipoles.json -> ../frameworks/moral_foundations/dipoles.json
│   └── framework.json -> ../frameworks/moral_foundations/framework.json
└── model_output/                  # Analysis results (unchanged)
```

## Storage Principles

### 1. **Framework Separation**
- Each complete dipole system gets its own directory under `frameworks/`
- Contains both conceptual (`dipoles.json`) and mathematical (`framework.json`) definitions
- Includes documentation explaining the theoretical basis

### 2. **Version Management**
- Prompts organized by framework and version
- Metadata tracks generation parameters and config versions
- Clear lineage from configuration to generated prompt

### 3. **Active Configuration**
- `config/` directory points to currently active framework via symlinks
- Maintains backward compatibility with existing code
- Easy switching between frameworks

### 4. **Extensibility**
- New frameworks can be added without affecting existing ones
- Researchers can develop custom dipole systems
- Clear separation between core system and research extensions

## Implementation Benefits

### For Researchers
- **Multiple Frameworks**: Compare different moral psychology theories
- **Version Control**: Track evolution of frameworks and prompts
- **Reproducibility**: Clear provenance from theory to analysis
- **Customization**: Develop domain-specific dipole systems

### For Developers
- **Modularity**: Clean separation of concerns
- **Maintainability**: Framework changes don't affect core code
- **Extensibility**: Plugin-like architecture for new frameworks
- **Compatibility**: Existing analyses continue to work

## Migration Strategy

### Phase 1: Reorganize Current System
1. Create `frameworks/moral_foundations/` with current configs
2. Move generated prompts to `prompts/moral_foundations/v2025.01.05/`
3. Create symlinks in `config/` to active framework

### Phase 2: Enable Framework Switching
1. Update `MoralGravityWellsElliptical` to accept framework parameter
2. Add framework selection to command-line tools
3. Update `generate_prompt.py` for multi-framework support

### Phase 3: Research Extensions
1. Develop alternative frameworks (political, cultural, etc.)
2. Create framework validation tools
3. Add comparative analysis capabilities

## Example Framework Definitions

### Alternative Framework: Political Spectrum
```json
// frameworks/political_spectrum/dipoles.json
{
  "version": "2025.01.06",
  "description": "Left-Right Political Analysis Framework",
  "dipoles": [
    {
      "name": "Economic",
      "positive": {"name": "Solidarity", "description": "..."},
      "negative": {"name": "Competition", "description": "..."}
    },
    {
      "name": "Social",
      "positive": {"name": "Equality", "description": "..."},
      "negative": {"name": "Tradition", "description": "..."}
    }
    // ... additional dipoles
  ]
}
```

### Custom Research Framework
```json
// frameworks/environmental_ethics/dipoles.json
{
  "version": "2025.01.06",
  "description": "Environmental Ethics Analysis Framework",
  "dipoles": [
    {
      "name": "Stewardship",
      "positive": {"name": "Sustainability", "description": "..."},
      "negative": {"name": "Exploitation", "description": "..."}
    }
    // ... domain-specific dipoles
  ]
}
```

## Usage Examples

### Switch Active Framework
```bash
# Switch to political spectrum framework
ln -sf ../frameworks/political_spectrum/dipoles.json config/dipoles.json
ln -sf ../frameworks/political_spectrum/framework.json config/framework.json

# Generate new prompt for active framework
python generate_prompt.py --output prompts/political_spectrum/v2025.01.06/
```

### Analyze with Specific Framework
```python
# Use specific framework for analysis
analyzer = MoralGravityWellsElliptical(framework="political_spectrum")
results = analyzer.analyze_text(text)
```

### Compare Frameworks
```python
# Compare same text across different frameworks
moral_results = MoralGravityWellsElliptical(framework="moral_foundations").analyze_text(text)
political_results = MoralGravityWellsElliptical(framework="political_spectrum").analyze_text(text)
```

This architecture provides a solid foundation for research extensibility while maintaining the simplicity and power of the current system.