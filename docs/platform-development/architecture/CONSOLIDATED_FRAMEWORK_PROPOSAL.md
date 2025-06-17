# Consolidated Framework Architecture Proposal

**Problem**: Framework definitions are scattered across multiple files with duplication and inconsistency  
**Solution**: Single-file framework definition with comprehensive structure  
**Date**: December 16, 2025

---

## 🎯 **Problem Statement**

The current framework definition system is **simultaneously too complex and too sparse**:

### **Current Problems**
- **Multi-file complexity**: Each framework requires 3+ files (dipoles.json, framework.json, weights.json)
- **Information duplication**: Well names and weights duplicated across files
- **Inconsistent structure**: Some frameworks have prompt_format.md, others don't
- **Maintenance burden**: Changes require updating multiple files
- **Scattered information**: Related data split across multiple locations
- **Prompt generation complexity**: System must merge information from multiple sources

### **Current File Structure Issues**
```
frameworks/civic_virtue/
├── dipoles.json          (148 lines) - Framework metadata + dipole definitions
├── framework.json        (146 lines) - Coordinate system + well positioning + weights
├── weights.json          (85 lines)  - Duplicate weight info + philosophy
├── README.md             (46 lines)  - Documentation
└── prompt_format.md      (114 lines) - Sometimes present, inconsistent
```

**Total**: 539+ lines across 5 files with significant duplication

---

## 💡 **Proposed Solution: Consolidated Framework Definition**

### **Single-File Structure**
```
frameworks/civic_virtue/
└── framework.json        (All framework information in logical structure)
```

### **Comprehensive Schema**
```json
{
  "framework_meta": {
    "name": "civic_virtue",
    "display_name": "Civic Virtue Framework", 
    "version": "v2025.06.14",
    "description": "Complete framework description",
    "theoretical_foundation": {
      "primary_sources": [...],
      "theoretical_approach": "..."
    }
  },
  
  "coordinate_system": {
    "type": "circle",
    "radius": 1.0,
    "scaling_factor": 0.8
  },
  
  "dipoles": [
    {
      "name": "Identity",
      "description": "Moral worth and group membership dynamics",
      "positive": {
        "name": "Dignity",
        "description": "...",
        "language_cues": [...],
        "angle": 90,
        "weight": 1.0,
        "type": "integrative",
        "tier": "primary"
      },
      "negative": {
        "name": "Tribalism", 
        "description": "...",
        "language_cues": [...],
        "angle": 270,
        "weight": -1.0,
        "type": "disintegrative",
        "tier": "primary"
      }
    }
  ],
  
  "weighting_philosophy": {
    "description": "Three-tier weighting system...",
    "tiers": {
      "primary": {"weight": 1.0, "description": "...", "wells": [...]},
      "secondary": {"weight": 0.8, "description": "...", "wells": [...]},
      "tertiary": {"weight": 0.6, "description": "...", "wells": [...]}
    }
  },
  
  "prompt_configuration": {
    "expert_role": "You are an expert...",
    "analysis_focus": "Evaluate how...",
    "scoring_emphasis": "Focus on...",
    "evidence_requirements": "Provide specific..."
  },
  
  "visualization": {
    "well_type_colors": {"integrative": "#2E7D32", "disintegrative": "#C62828"},
    "supported_types": ["circular", "comparative"]
  },
  
  "metrics": {
    "com": {"name": "Center of Mass", "description": "..."},
    "nps": {"name": "Narrative Polarity Score", "description": "..."}
  },
  
  "compatibility": {
    "prompt_templates": ["hierarchical_v2.1", "standard_v2.0"],
    "weighting_schemes": ["winner_take_most", "proportional"],
    "api_versions": ["v2.0", "v2.1"]
  }
}
```

---

## ✅ **Benefits of Consolidated Approach**

### **1. Simplicity & Maintainability**
- **Single source of truth**: All framework information in one logical structure
- **No duplication**: Well definitions, weights, and metadata unified
- **Easier updates**: Change framework in one place
- **Consistent structure**: Same schema across all frameworks
- **Better version control**: Single file to track changes

### **2. Enhanced Functionality**
- **Framework-specific prompting**: `prompt_configuration` section eliminates template guesswork
- **Complete context**: All related information available simultaneously
- **Self-documenting**: Structure makes relationships clear
- **Validation simplicity**: Single schema to validate against

### **3. Developer Experience**
- **Simpler loading**: One JSON parse operation vs. multiple file loads
- **Fewer errors**: No cross-file reference mismatches
- **Easier testing**: Mock single object vs. multiple file system
- **Better IDE support**: Single file for navigation and editing

### **4. Rich Framework-Specific Prompting**
- **Comprehensive keyword banks**: 5.3x more language cues with categorical organization
- **Rich conceptual descriptions**: 2.8x more detailed well descriptions with theoretical context
- **Framework-specific guidance**: Domain expertise embedded (analytical questions, contextual considerations, common challenges)
- **Separation of concerns**: Framework-specific content separate from general template structure
- **Domain expertise capture**: Framework developers can encode deep domain knowledge into prompting

---

## 🎯 **Flexible Framework Architecture: Beyond Dipoles**

The consolidated framework approach supports **multiple conceptual models** including both traditional dipole-based frameworks and independent wells approaches:

### **Framework Model Flexibility**

**Dipole-Based Frameworks** (Current Standard):
- Organized as positive/negative pairs (e.g., Dignity vs. Tribalism)
- Wells positioned as opposites around circle
- Center of mass calculated from dipole forces
- Suitable for moral/virtue frameworks with clear opposites

**Independent Wells Frameworks** (New Capability):
- Wells positioned independently around circle
- Each well represents competing theory, not opposite pair
- Center of mass calculated from independent gravitational forces  
- Suitable for tripartite models or competing worldviews

**Example: Three Wells Political Discourse Framework**
Based on the Three Gravitational Wells model, positioning:
- Intersectionality Theory (0°)
- Tribal Domination Theory (120°) 
- Pluralist Individual Dignity Theory (240°)

These represent independent competing worldviews, not opposite pairs, requiring different mathematical treatment and prompt approaches.

**Clustered Dipole Frameworks** (Advanced Feature):
- Dipoles clustered within defined arcs of the circle
- Flexible cluster definitions with custom arc ranges
- Domain-specific groupings (e.g., stakeholder relations 15°-75°, operational integrity 120°-210°)
- Cluster-aware calculations and domain-specific metrics
- Support for asymmetric positioning and variable cluster sizes

### **Two-Dimensional Prompting Architecture**

The consolidated framework approach perfectly supports the crucial distinction between **framework-specific content** and **general template structure**:

### **Dimension 1: Framework-Specific Rich Content**
- **Rich dipole descriptions**: Deep conceptual explanations with theoretical context
- **Comprehensive keyword banks**: Organized by categories (direct appeals, bridging language, etc.)
- **Domain expertise guidance**: Framework-specific analytical questions and considerations
- **Conceptual breadth mapping**: Core concepts and recognition patterns for each well
- **Theoretical grounding**: Academic sources and domain-specific reasoning

**Example - Enhanced Dignity Well:**
- **Basic description**: 144 characters
- **Rich description**: 410 characters (2.8x more detailed)
- **Language cues**: 32 total across 4 categories (5.3x more comprehensive)
- **Domain guidance**: 5 analytical questions, 4 contextual considerations, 5 common challenges

### **Dimension 2: General Template Structure**
- **Expert role definition**: Cross-framework analyst positioning
- **Scoring requirements**: Universal 0.0-1.0 scale with evidence requirements
- **JSON response format**: Consistent structure across all frameworks
- **Analysis methodology**: General approach to evidence gathering and reasoning
- **Response formatting**: Standard metadata, wells array, metrics structure

### **Benefits of Separation**
✅ **Framework developers** can focus on domain expertise without worrying about prompt engineering  
✅ **Template developers** can improve general prompting without domain-specific knowledge  
✅ **More accurate analysis** through rich, domain-specific content  
✅ **Maintainable templates** through consistent cross-framework structure  
✅ **Scalable system** supporting any number of specialized frameworks  

---

## 🔄 **Migration Strategy**

### **Phase 1: Proof of Concept** ✅ Complete
- [x] Create consolidated structure for `civic_virtue`
- [x] Build demonstration loader and prompt generator
- [x] Validate prompt generation quality
- [x] Document benefits and approach

### **Phase 2: Gradual Migration**
1. **Update FrameworkManager** to support both old and new formats
2. **Migrate one framework at a time** (civic_virtue, political_spectrum, etc.)
3. **Add validation** to ensure consolidated definitions are complete
4. **Update PromptTemplateManager** to use consolidated information

### **Phase 3: Full Transition**
1. **Update all existing frameworks** to consolidated format
2. **Remove legacy multi-file support** after validation
3. **Update documentation** and guides
4. **Clean up deprecated files**

### **Backward Compatibility**
```python
def load_framework(self, framework_name: str) -> Dict[str, Any]:
    """Load framework with backward compatibility"""
    consolidated_file = f"frameworks/{framework_name}/framework.json"
    
    if os.path.exists(consolidated_file):
        # New consolidated format
        with open(consolidated_file, 'r') as f:
            return json.load(f)
    else:
        # Legacy multi-file format
        return self._load_legacy_framework(framework_name)
```

---

## 📊 **Comparison: Before vs. After**

### **Current Multi-File Approach**
```python
# Load 3+ separate files
dipoles = load_json("frameworks/civic_virtue/dipoles.json")      # 148 lines
framework = load_json("frameworks/civic_virtue/framework.json")  # 146 lines  
weights = load_json("frameworks/civic_virtue/weights.json")      # 85 lines

# Cross-reference and merge data
wells = extract_wells_from_dipoles(dipoles)
well_weights = weights["well_weights"]  
coordinate_system = framework["coordinate_system"]

# Build prompt from scattered information
prompt = build_prompt(dipoles, framework, weights, custom_templates)
```

### **Proposed Consolidated Approach**  
```python
# Load single comprehensive file
framework = load_json("frameworks/civic_virtue/framework.json")

# All information immediately available
dipoles = framework["dipoles"]
weights = framework["weighting_philosophy"] 
prompt_config = framework["prompt_configuration"]
coordinate_system = framework["coordinate_system"]

# Direct prompt generation
prompt = generate_prompt_from_framework(framework, text)
```

**Reduction**: From 379+ lines across 3+ files to single logical structure

---

## 🧪 **Validation Results**

The proof-of-concept demonstrates:

### **Successful Prompt Generation**
- ✅ **4,176 character prompt** generated from consolidated definition
- ✅ **All framework wells** properly included (10 wells from 5 dipoles)
- ✅ **Scoring guidelines** integrated from weighting philosophy
- ✅ **Expert role** and analysis focus from prompt configuration
- ✅ **Evidence requirements** explicitly stated
- ✅ **JSON format** automatically derived from dipole structure

### **Code Simplification**
- ✅ **Single load operation** vs. multiple file coordination
- ✅ **No cross-referencing** needed between files
- ✅ **Logical information hierarchy** easy to navigate
- ✅ **Framework-specific prompt configuration** eliminates guesswork

### **Content Richness Improvements**
- ✅ **Language cues**: 5.3x more comprehensive (32 vs 6 total)
- ✅ **Descriptive content**: 2.8x more detailed (410 vs 144 characters)
- ✅ **Categorical organization**: 4 language cue categories vs flat list
- ✅ **Domain expertise**: 14 pieces of framework-specific guidance
- ✅ **Theoretical grounding**: Explicit academic sources and reasoning
- ✅ **Recognition patterns**: 6 concrete patterns for identifying each well

### **Architectural Flexibility Achievements**
- ✅ **Multiple framework models**: Both dipole-based and independent wells supported
- ✅ **Three Wells Model compatibility**: Direct support for tripartite political discourse analysis
- ✅ **Calculation method specification**: Framework-specific mathematical approaches
- ✅ **Gravitational metaphor support**: Independent wells as competing theories vs. opposing forces
- ✅ **Prompt adaptation**: Framework-aware prompt generation for different conceptual models

### **Advanced Clustering Capabilities**
- ✅ **Flexible arc positioning**: Custom arc ranges (e.g., 15°-75°) vs. symmetric positioning
- ✅ **Domain-specific clustering**: Business ethics example with stakeholder/operational/strategic domains
- ✅ **Variable cluster parameters**: Different spans, dipole counts, and positioning methods per cluster
- ✅ **Cluster-aware calculations**: Domain weighting and cluster coherence metrics
- ✅ **Asymmetric framework design**: Support for frameworks focused on specific conceptual regions
- ✅ **Overlap control**: Configurable cluster separation and boundary management

---

## 📋 **Implementation Checklist**

### **Framework Definition Tasks**
- [ ] Create consolidated schema specification
- [ ] Migrate `civic_virtue` framework (proof-of-concept ✅)
- [ ] Migrate `political_spectrum` framework  
- [ ] Migrate `moral_rhetorical_posture` framework
- [ ] Migrate `fukuyama_identity` framework
- [ ] Migrate `mft_persuasive_force` framework
- [ ] Migrate `iditi` framework

### **Code Integration Tasks**
- [ ] Update FrameworkManager with backward compatibility
- [ ] Update PromptTemplateManager to use prompt_configuration
- [ ] Add validation for consolidated framework files
- [ ] Update framework loading tests
- [ ] Update API endpoints using frameworks

### **Documentation Tasks**
- [ ] Update framework development guides
- [ ] Create migration guide for existing frameworks
- [ ] Update API documentation
- [ ] Add consolidated schema to project specs

### **Cleanup Tasks**
- [ ] Remove deprecated multi-file loaders
- [ ] Clean up legacy framework files
- [ ] Update CHANGELOG with architectural improvement
- [ ] Archive old examples and documentation

---

## 🎯 **Conclusion**

The consolidated framework approach addresses the core problem: **information scattered across multiple files creates unnecessary complexity while making framework-specific customization difficult**.

The single-file approach provides:
- **Complete framework definition** in logical structure
- **Framework-specific prompt configuration** eliminating template guesswork  
- **Simplified maintenance** and development workflow
- **Better consistency** across all frameworks
- **Enhanced functionality** through comprehensive metadata

This architectural improvement will make framework development, maintenance, and usage significantly more straightforward while enabling better customization and consistency.

**Recommendation**: Proceed with gradual migration starting with proof-of-concept validation and framework-by-framework conversion. 