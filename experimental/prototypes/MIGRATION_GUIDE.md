# Migration Guide: Narrative Gravity → Discernus Coordinate System

**Version**: Migration to Cartographic Terminology  
**Date**: User Request - Terminology Update  
**Status**: ⚠️ **DEPRECATION NOTICE**

## 🚨 Deprecation Notice

The `NarrativeGravityVisualizationEngine` and related "Narrative Gravity" terminology is being deprecated in favor of the new `DiscernusVisualizationEngine` with cartographic vocabulary. This migration preserves all valuable architectural patterns while implementing the updated terminology from the glossary.

## 📋 What's Being Migrated

### **✅ Preserved Architecture**
- **Theme System** - Excellent design, just terminology updates
- **Multi-format Export** - HTML, PNG, SVG, PDF capabilities remain
- **Mathematical Algorithms** - Positioning calculations preserved
- **Multiple Visualization Types** - Single, comparative, dashboard patterns
- **Centralized Engine Pattern** - Core architecture maintained

### **🔄 Terminology Updates**

| Old Term | New Term | Usage |
|----------|----------|-------|
| `NarrativeGravityVisualizationEngine` | `DiscernusVisualizationEngine` | Main class |
| `wells` | `anchors` | Fixed reference points |
| `dipoles` | `axes` | Paired anchor dimensions |
| `narrative_scores` | `axis_scores` / `anchor_scores` | Score parameters |
| `narrative_position` | `centroid` | Calculated position |
| `well_colors` | `anchor_colors` | Theme color mapping |
| `calculate_narrative_position()` | `calculate_centroid()` | Method names |
| "Narrative Gravity Maps" | "Discernus Coordinate System (DCS)" | System branding |

## 🔧 Migration Instructions

### **Step 1: Update Imports**

```python
# OLD (Deprecated)
from src.visualization.engine import NarrativeGravityVisualizationEngine

# NEW (Recommended)
from experimental.prototypes.discernus_visualization_engine import DiscernusVisualizationEngine
```

### **Step 2: Update Method Calls**

```python
# OLD: Wells and narrative terminology
engine.create_single_analysis(
    wells=well_definitions,
    narrative_scores=scores,
    narrative_label="Narrative Position"
)

# NEW: Anchors and centroid terminology  
engine.create_single_analysis(
    anchors=anchor_definitions,
    axis_scores=scores,  # or anchor_scores for ASFa frameworks
    centroid_label="Centroid"
)
```

### **Step 3: Update Data Structures**

```python
# OLD: Well-based configuration
wells = {
    'Hope': {'angle': 0, 'type': 'integrative', 'weight': 1.0},
    'Fear': {'angle': 180, 'type': 'disintegrative', 'weight': 0.6}
}

# NEW: Anchor-based configuration (same structure, new terminology)
anchors = {
    'Hope': {'angle': 0, 'type': 'integrative', 'weight': 1.0},
    'Fear': {'angle': 180, 'type': 'disintegrative', 'weight': 0.6}
}
```

### **Step 4: Update Theme References**

```python
# OLD: well_colors property
theme.well_colors

# NEW: anchor_colors property
theme.anchor_colors
```

## 🧪 Testing Your Migration

Use the **Visualization Iteration Lab** for rapid testing:

```python
from experimental.prototypes.visualization_iteration_lab import VisualizationIterationLab

# Initialize lab
lab = VisualizationIterationLab()

# Test themes across your data
lab.rapid_theme_comparison('your_anchor_set', 'your_signature')

# Test mathematical approaches
lab.mathematical_approach_testing()

# Interactive development
lab.hot_reload_development_session()
```

## 📊 Framework Type Considerations

### **Axis-Set Frameworks (ASFx)**
- Use `axis_scores` parameter
- Anchors come in opposing pairs forming axes
- Examples: Civic Virtue, Moral Foundations Theory

```python
engine.create_single_analysis(
    anchors=asfx_anchors,
    axis_scores=axis_signature,  # Scores along axes
    title="ASFx Framework Analysis"
)
```

### **Anchor-Set Frameworks (ASFa)**
- Use `anchor_scores` parameter  
- Anchors are independent (no opposing pairs)
- Examples: Three Theories framework

```python
engine.create_single_analysis(
    anchors=asfa_anchors,
    anchor_scores=anchor_signature,  # Scores toward individual anchors
    title="ASFa Framework Analysis"
)
```

## 🎯 Benefits of Migration

### **Academic Credibility**
- Cartographic terminology is empirically grounded
- Eliminates confusing physics metaphors
- Clear to interdisciplinary readers

### **Framework Flexibility**  
- Handles both ASFx (paired) and ASFa (independent) frameworks
- No longer assumes exactly two poles per dimension
- Extensible to new framework types

### **Visualization Clarity**
- Geometry-agnostic data layer
- Role-based naming (anchor, axis, centroid)
- Scalable to future visualization types

## 🔄 Backward Compatibility

During the transition period:

1. **Old system remains functional** for existing code
2. **Gradual migration recommended** - migrate components one at a time
3. **Iteration lab provides testing** for migration validation
4. **Production integration planned** after experimental validation

## 📝 Migration Checklist

- [ ] Update import statements
- [ ] Replace method calls with new terminology
- [ ] Update data structure variable names  
- [ ] Test with Visualization Iteration Lab
- [ ] Verify theme compatibility
- [ ] Test mathematical approaches
- [ ] Validate production data formats
- [ ] Update documentation and comments

## 🎨 Rapid Iteration Workflow

For visualization development with the new system:

1. **Use the Iteration Lab** for instant feedback
2. **Test across all themes** with one command
3. **Compare mathematical approaches** side-by-side  
4. **Hot-reload modules** for development speed
5. **Export for production** when ready

## 🔮 Next Steps

1. **Complete experimental validation** using the iteration lab
2. **Update theme system** with new terminology
3. **Migrate VisualizationGenerator** wrapper
4. **Update orchestrator integration**
5. **Deprecate old systems** after full migration

---

**Questions?** The new system preserves all the solid architectural patterns while implementing the cleaner cartographic terminology. Use the iteration lab for rapid testing and development! 