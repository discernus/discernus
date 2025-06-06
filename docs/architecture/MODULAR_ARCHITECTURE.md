# Narrative Gravity Wells Modular Architecture v2.0 - Technical Documentation

This document provides technical implementation details for the modular architecture introduced in v2.0.

## Technical Architecture

### Class Structure Changes

#### `NarrativeGravityWellsElliptical` Enhancements

**New Constructor Parameters:**
```python
def __init__(self, config_dir="config"):
    """
    Initialize with modular configuration loading.
    
    Args:
        config_dir (str): Directory containing dipoles.json and framework.json
                         Defaults to "config" for backward compatibility
    """
```

**Configuration Loading:**
```python
def load_configuration(self, config_dir):
    """Load dipoles and framework from JSON files with fallback to defaults."""
    dipoles_file = Path(config_dir) / "dipoles.json"
    framework_file = Path(config_dir) / "framework.json"
    
    if dipoles_file.exists() and framework_file.exists():
        # Load modular configuration
        self.dipoles_data = self._load_dipoles(dipoles_file)
        self.framework_data = self._load_framework(framework_file)
        self.well_definitions = self._build_well_definitions()
        print(f"✅ Loaded framework v{self.framework_data['version']} from {framework_file}")
    else:
        # Fallback to hardcoded defaults
        self._load_default_configuration()
        print("⚠️  Using default configuration (config files not found)")
```

**Backward Compatibility Methods:**
```python
def normalize_analysis_data(self, data):
    """Convert old JSON format to new format for processing."""
    if "wells" in data and "scores" not in data:
        # Old format: {"wells": [{"name": "Dignity", "score": 1.0}]}
        scores = {well["name"]: well["score"] for well in data["wells"]}
        data["scores"] = scores
        
    # Ensure all wells have scores (fill missing with 0.0)
    for well_name in self.well_definitions:
        if well_name not in data["scores"]:
            data["scores"][well_name] = 0.0
            
    return data
```

### JSON Format Specification

#### New Minimal Format
```json
{
  "metadata": {
    "title": "Analysis Title",
    "model": "gpt-4",
            "prompt_version": "2025.06.04",
        "dipoles_version": "2025.06.04",
        "framework_version": "2025.06.04"
  },
  "scores": {
    "Dignity": 1.0,
    "Truth": 0.8,
    "Hope": 0.6,
    "Justice": 0.7,
    "Pragmatism": 0.4,
    "Tribalism": 0.2,
    "Manipulation": 0.1,
    "Resentment": 0.3,
    "Fear": 0.2,
    "Fantasy": 0.1
  }
}
```

#### Legacy Format (Deprecated but Supported)
```json
{
  "metadata": {...},
  "wells": [
    {"name": "Dignity", "score": 1.0, "angle": 90, "weight": 1.0},
    {"name": "Truth", "score": 0.8, "angle": 45, "weight": 0.8}
  ],
  "com": {"x": 0.1, "y": 0.2},
  "mps": 0.25,
  "dps": 0.85
}
```

### Configuration File Schemas

#### `dipoles.json` Schema
```json
{
  "type": "object",
  "required": ["version", "description", "dipoles"],
  "properties": {
    "version": {"type": "string"},
    "description": {"type": "string"},
    "dipoles": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["name", "description", "positive", "negative"],
        "properties": {
          "name": {"type": "string"},
          "description": {"type": "string"},
          "positive": {
            "type": "object",
            "required": ["name", "description", "language_cues"],
            "properties": {
              "name": {"type": "string"},
              "description": {"type": "string"},
              "language_cues": {
                "type": "array",
                "items": {"type": "string"}
              }
            }
          },
          "negative": {
            "type": "object",
            "required": ["name", "description", "language_cues"],
            "properties": {
              "name": {"type": "string"},
              "description": {"type": "string"},
              "language_cues": {
                "type": "array",
                "items": {"type": "string"}
              }
            }
          }
        }
      }
    }
  }
}
```

#### `framework.json` Schema
```json
{
  "type": "object",
  "required": ["version", "description", "wells"],
  "properties": {
    "version": {"type": "string"},
    "description": {"type": "string"},
    "ellipse": {
      "type": "object",
      "properties": {
        "semi_major_axis": {"type": "number"},
        "semi_minor_axis": {"type": "number"},
        "orientation": {"type": "string", "enum": ["vertical", "horizontal"]}
      }
    },
    "wells": {
      "type": "object",
      "patternProperties": {
        "^[A-Za-z]+$": {
          "type": "object",
          "required": ["angle", "weight", "type"],
          "properties": {
            "angle": {"type": "number", "minimum": 0, "maximum": 360},
            "weight": {"type": "number"},
            "type": {"type": "string", "enum": ["integrative", "disintegrative"]},
            "tier": {"type": "string", "enum": ["primary", "secondary", "tertiary"]}
          }
        }
      }
    },
    "scaling_factor": {"type": "number"}
  }
}
```

### Prompt Generation Algorithm

#### Template Structure
```python
def generate_prompt(dipoles_data, framework_data, interactive=True):
    """Generate LLM prompt from configuration data."""
    
    # Extract dipole information
    dipoles = []
    for dipole in dipoles_data['dipoles']:
        positive = dipole['positive']
        negative = dipole['negative']
        
        dipoles.append({
            'name': dipole['name'],
            'positive_name': positive['name'],
            'positive_desc': positive['description'],
            'positive_cues': positive['language_cues'],
            'negative_name': negative['name'],
            'negative_desc': negative['description'],
            'negative_cues': negative['language_cues']
        })
    
    # Build prompt template
    if interactive:
        template = INTERACTIVE_TEMPLATE
    else:
        template = SIMPLE_TEMPLATE
        
    return template.format(
        dipoles=dipoles,
        version=dipoles_data['version'],
        framework_version=framework_data['version']
    )
```

### Metric Calculation

#### Runtime Calculation from Scores
```python
def calculate_metrics(self, scores):
    """Calculate metrics from well scores and framework configuration."""
    
    # Get well positions and weights from framework
    positions = []
    weighted_forces = []
    
    for well_name, score in scores.items():
        if well_name in self.well_definitions:
            well = self.well_definitions[well_name]
            angle_rad = math.radians(well['angle'])
            weight = well['weight']
            
            # Calculate position on ellipse
            x, y = self._ellipse_position(angle_rad)
            positions.append((x, y, score * weight))
            
            # Calculate weighted force vector
            force_x = x * score * weight
            force_y = y * score * weight
            weighted_forces.append((force_x, force_y))
    
    # Calculate center of mass
    total_weight = sum(abs(pos[2]) for pos in positions)
    if total_weight > 0:
        com_x = sum(pos[0] * abs(pos[2]) for pos in positions) / total_weight
        com_y = sum(pos[1] * abs(pos[2]) for pos in positions) / total_weight
    else:
        com_x = com_y = 0.0
    
    # Calculate derived metrics
    moral_polarity_score = math.sqrt(com_x**2 + com_y**2)
    directional_purity_score = com_y  # Vertical component
    
    return {
        'com': {'x': com_x, 'y': com_y},
        'mps': moral_polarity_score,
        'dps': directional_purity_score
    }
```

### Framework Validation

#### Consistency Checks
```python
def validate_framework_consistency(dipoles_data, framework_data):
    """Validate that dipoles and framework definitions are consistent."""
    
    # Extract well names from dipoles
    dipole_wells = set()
    for dipole in dipoles_data['dipoles']:
        dipole_wells.add(dipole['positive']['name'])
        dipole_wells.add(dipole['negative']['name'])
    
    # Extract well names from framework
    framework_wells = set(framework_data['wells'].keys())
    
    # Check consistency
    missing_in_framework = dipole_wells - framework_wells
    extra_in_framework = framework_wells - dipole_wells
    
    if missing_in_framework or extra_in_framework:
        raise ValueError(f"Inconsistent well definitions: "
                        f"Missing: {missing_in_framework}, "
                        f"Extra: {extra_in_framework}")
    
    # Validate weights and angles
    for well_name, well_config in framework_data['wells'].items():
        if not 0 <= well_config['angle'] < 360:
            raise ValueError(f"Invalid angle for {well_name}: {well_config['angle']}")
        
        if well_config['type'] == 'integrative' and well_config['weight'] < 0:
            raise ValueError(f"Integrative well {well_name} has negative weight")
        
        if well_config['type'] == 'disintegrative' and well_config['weight'] > 0:
            raise ValueError(f"Disintegrative well {well_name} has positive weight")
    
    return True
```

### Performance Optimizations

#### Configuration Caching
```python
class NarrativeGravityWellsElliptical:
    def __init__(self, config_dir="config"):
        self._config_cache = {}
        self._config_dir = config_dir
        self.load_configuration(config_dir)
    
    def load_configuration(self, config_dir):
        """Load configuration with caching."""
        cache_key = str(Path(config_dir).resolve())
        
        if cache_key in self._config_cache:
            cached = self._config_cache[cache_key]
            self.dipoles_data = cached['dipoles']
            self.framework_data = cached['framework']
            self.well_definitions = cached['wells']
            return
        
        # Load and cache configuration
        # ... loading logic ...
        
        self._config_cache[cache_key] = {
            'dipoles': self.dipoles_data,
            'framework': self.framework_data,
            'wells': self.well_definitions
        }
```

### Migration Utilities

#### JSON Format Transformer
```python
def transform_legacy_to_new_format(legacy_json_path, output_path):
    """Transform legacy JSON files to new minimal format."""
    
    with open(legacy_json_path) as f:
        data = json.load(f)
    
    # Extract scores from wells array
    scores = {}
    if 'wells' in data:
        for well in data['wells']:
            scores[well['name']] = well['score']
    
    # Create new format
    new_data = {
        'metadata': data.get('metadata', {}),
        'scores': scores
    }
    
    # Add version information
    new_data['metadata']['format_version'] = '2.0'
    new_data['metadata']['migrated_from'] = 'legacy'
    
    with open(output_path, 'w') as f:
        json.dump(new_data, f, indent=2)
```

## Error Handling

### Configuration Loading Errors
- Missing config files → Fall back to defaults
- Invalid JSON → Detailed parsing error
- Schema validation failure → Specific field errors
- Inconsistent wells → List missing/extra wells

### Runtime Errors
- Unknown wells in analysis data → Warning + default angle
- Missing scores → Fill with 0.0
- Invalid metric calculations → Use fallback values

### Framework Validation Errors
- Structural validation via JSON schema
- Semantic validation for well consistency
- Mathematical validation for angles and weights

This technical documentation should be sufficient for developers working with the modular architecture while avoiding duplication with the user-facing README.md. 