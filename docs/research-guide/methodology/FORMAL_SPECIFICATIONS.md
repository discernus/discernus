# Formal Specification System Proposal
## Narrative Gravity Wells Framework Standardization

**Version:** 1.0.0  
**Date:** June 12, 2025  
**Status:** Proposal

---

## 🎯 **Executive Summary**

This proposal establishes formal specifications for three critical components of the Narrative Gravity Wells system:

1. **Framework Specifications** - Standardized structure for moral/political analysis frameworks
2. **Prompt Template Specifications** - Structured templates for LLM analysis instructions  
3. **Weighting Scheme Specifications** - Mathematical methodologies for score aggregation

## 📐 **1. Framework Specification Standard**

### **1.1 Core Framework Schema (v2.0)**

```json
{
  "$schema": "https://narrative-gravity.github.io/schemas/framework-v2.0.json",
  "framework_name": "string (required, snake_case)",
  "display_name": "string (required, human-readable)",
  "version": "string (required, semver: vYYYY.MM.DD)",
  "description": "string (required, academic description)",
  
  "coordinate_system": {
    "type": "circle",
    "radius": 1.0,
    "description": "Circular coordinate system parameters"
  },
  
  "positioning_strategy": {
    "type": "enum[clustered_positioning, even_distribution, custom]",
    "description": "string (positioning rationale)",
    "clusters": {
      "cluster_name": {
        "center_angle": "number (0-360)",
        "span": "number (degrees)",
        "well_types": ["array of well types"],
        "description": "string (cluster purpose)"
      }
    }
  },
  
  "wells": {
    "WellName": {
      "angle": "number (0-360, required)",
      "weight": "number (positive, required)", 
      "type": "string (framework-specific, required)",
      "tier": "enum[primary, secondary, tertiary]",
      "description": "string (academic definition)"
    }
  },
  
  "well_type_colors": {
    "type_name": "#hexcolor"
  },
  
  "theoretical_foundation": {
    "primary_sources": ["array of academic citations"],
    "theoretical_approach": "string (methodology description)",
    "validation_studies": ["array of empirical validation references"]
  },
  
  "metrics": {
    "metric_code": {
      "name": "string (display name)",
      "description": "string (calculation description)",
      "formula": "string (mathematical formula)",
      "interpretation": "string (meaning guidance)"
    }
  },
  
  "compatibility": {
    "prompt_templates": ["array of compatible template IDs"],
    "weighting_schemes": ["array of compatible weighting IDs"],
    "visualization_types": ["array of supported viz types"]
  }
}
```

### **1.2 Framework Validation Rules**

**Structural Validation:**
- ✅ All required fields present
- ✅ Well angles within 0-360° range
- ✅ Well weights are positive numbers
- ✅ Positioning strategy matches well configuration
- ✅ Color codes are valid hex values

**Semantic Validation:**
- ✅ Well names are unique within framework
- ✅ Cluster spans don't exceed 360° total
- ✅ Theoretical foundation includes primary sources
- ✅ Metrics formulas are mathematically valid

**Academic Validation:**
- ✅ Theoretical foundation cites peer-reviewed sources
- ✅ Framework methodology is clearly described
- ✅ Validation studies support framework claims

---

## 📝 **2. Prompt Template Specification Standard**

### **2.1 Structured Prompt Template Schema (v2.1)**

```json
{
  "$schema": "https://narrative-gravity.github.io/schemas/prompt-template-v2.1.json",
  "template_id": "string (required, unique)",
  "name": "string (required, human-readable)",
  "version": "string (required, semver)",
  "template_type": "enum[standard, hierarchical, comparative]",
  "description": "string (purpose and methodology)",
  
  "components": {
    "header": {
      "order": 1,
      "required": true,
      "content": "string (version identification)"
    },
    "role_definition": {
      "order": 2, 
      "required": true,
      "content": "string (expert role specification)"
    },
    "scoring_requirements": {
      "order": 3,
      "required": true,
      "content": "string (mandatory 0.0-1.0 scale)"
    },
    "analysis_methodology": {
      "order": 4,
      "required": true,
      "content": "string (analytical approach)"
    },
    "framework_wells": {
      "order": 5,
      "required": true,
      "content": "string (framework-specific wells)",
      "dynamic": true,
      "source": "framework_config"
    },
    "hierarchical_requirements": {
      "order": 6,
      "required": "conditional (if template_type == hierarchical)",
      "content": "string (dominance ranking instructions)"
    },
    "response_format": {
      "order": 7,
      "required": true,
      "content": "string (JSON structure specification)"
    },
    "quality_standards": {
      "order": 8,
      "required": true,
      "content": "string (evidence and reproducibility requirements)"
    }
  },
  
  "framework_compatibility": ["array of framework names"],
  "model_compatibility": ["array of LLM model names"],
  
  "validation_criteria": {
    "output_format_compliance": "boolean",
    "instruction_clarity": "number (1-5 scale)",
    "evidence_requirements": "boolean",
    "reproducibility_score": "number (CV target)"
  },
  
  "performance_targets": {
    "coefficient_of_variation": "number (< 0.20)",
    "hierarchical_clarity": "number (1-5 scale)",
    "framework_fit_accuracy": "number (0.0-1.0)",
    "instruction_following_rate": "number (0.0-1.0)"
  }
}
```

### **2.2 Prompt Template Validation Rules**

**Structural Validation:**
- ✅ All required components present in correct order
- ✅ Component content meets minimum length requirements
- ✅ JSON response format is syntactically valid
- ✅ Framework compatibility declarations are valid

**Content Validation:**
- ✅ Scoring requirements specify 0.0-1.0 scale
- ✅ Role definition establishes expert authority
- ✅ Analysis methodology provides clear guidance
- ✅ Quality standards require evidence and justification

**Performance Validation:**
- ✅ Template achieves CV < 0.20 in testing
- ✅ Output format compliance > 95%
- ✅ Hierarchical clarity meets threshold
- ✅ Cross-model consistency validated

---

## ⚖️ **3. Weighting Scheme Specification Standard**

### **3.1 Weighting Methodology Schema (v1.0)**

```json
{
  "$schema": "https://narrative-gravity.github.io/schemas/weighting-scheme-v1.0.json",
  "scheme_id": "string (required, unique)",
  "name": "string (required, human-readable)",
  "version": "string (required, semver)",
  "algorithm_type": "enum[winner_take_most, proportional, threshold_based, custom]",
  "description": "string (methodology description)",
  
  "mathematical_foundation": {
    "primary_formula": "string (LaTeX or ASCII math)",
    "parameter_definitions": {
      "parameter_name": {
        "symbol": "string (mathematical symbol)",
        "description": "string (parameter meaning)",
        "valid_range": "string (min-max values)",
        "default_value": "number"
      }
    },
    "normalization_method": "string (how scores are normalized)",
    "edge_case_handling": "string (zero scores, ties, etc.)"
  },
  
  "algorithm_parameters": {
    "dominance_threshold": "number (0.0-1.0)",
    "secondary_weight_factor": "number",
    "minimum_score_threshold": "number",
    "tie_breaking_method": "enum[random, alphabetical, score_based]"
  },
  
  "framework_compatibility": ["array of framework names"],
  "prompt_compatibility": ["array of prompt template types"],
  
  "validation_requirements": {
    "mathematical_properties": {
      "sum_to_one": "boolean (weights sum to 1.0)",
      "non_negative": "boolean (all weights >= 0)",
      "monotonic": "boolean (higher scores → higher weights)",
      "scale_invariant": "boolean (proportional scaling preserved)"
    },
    "empirical_validation": {
      "test_scenarios": ["array of test case descriptions"],
      "expected_behaviors": ["array of behavioral requirements"],
      "performance_metrics": ["array of evaluation criteria"]
    }
  },
  
  "implementation": {
    "python_class": "string (class name)",
    "dependencies": ["array of required packages"],
    "computational_complexity": "string (Big O notation)",
    "memory_requirements": "string (space complexity)"
  }
}
```

### **3.2 Weighting Scheme Validation Rules**

**Mathematical Validation:**
- ✅ Formula is mathematically sound
- ✅ Parameters have valid ranges and defaults
- ✅ Edge cases are properly handled
- ✅ Normalization preserves meaningful relationships

**Empirical Validation:**
- ✅ Test scenarios cover expected use cases
- ✅ Algorithm behaves predictably in edge cases
- ✅ Performance meets computational requirements
- ✅ Results align with theoretical expectations

**Implementation Validation:**
- ✅ Code implements specification exactly
- ✅ Dependencies are minimal and stable
- ✅ Performance meets scalability requirements
- ✅ Error handling is comprehensive

---

## 🔧 **4. Implementation Strategy**

### **Phase 1: Schema Development (2 weeks)**
- Create JSON schemas for all three specifications
- Implement validation libraries
- Create CLI validation tools
- Establish testing frameworks

### **Phase 2: Migration & Validation (2 weeks)**
- Migrate existing frameworks to new schema
- Validate all current prompt templates
- Document existing weighting schemes
- Create compatibility matrices

### **Phase 3: Tooling & Automation (2 weeks)**
- Build specification editors (web UI)
- Implement automated validation pipelines
- Create specification generators
- Establish version control workflows

### **Phase 4: Documentation & Training (1 week)**
- Write comprehensive specification guides
- Create validation examples
- Document best practices
- Train team on new standards

---

## 📊 **5. Quality Assurance Framework**

### **Automated Validation Pipeline**
```bash
# Framework validation
narrative-gravity validate framework civic_virtue/framework.json

# Prompt template validation  
narrative-gravity validate prompt templates/hierarchical_v2.1.json

# Weighting scheme validation
narrative-gravity validate weighting schemes/winner_take_most_v3.json

# Cross-component compatibility
narrative-gravity validate compatibility --framework civic_virtue --prompt hierarchical_v2.1 --weighting winner_take_most_v3
```

### **Continuous Integration Checks**
- ✅ Schema validation on all commits
- ✅ Performance regression testing
- ✅ Cross-component compatibility verification
- ✅ Academic citation validation

### **Quality Metrics Dashboard**
- Framework compliance scores
- Prompt template performance metrics
- Weighting scheme mathematical properties
- Cross-component compatibility matrix

---

## 🎯 **6. Benefits & Impact**

### **Immediate Benefits**
- **Consistency**: Standardized structure across all components
- **Validation**: Automated quality assurance and error detection
- **Interoperability**: Clear compatibility requirements
- **Documentation**: Self-documenting specifications

### **Long-term Impact**
- **Scalability**: Easy addition of new frameworks/templates
- **Collaboration**: Clear standards for external contributors
- **Research**: Reproducible and comparable methodologies
- **Maintenance**: Reduced technical debt and easier updates

### **Academic Rigor**
- **Peer Review**: Specifications support academic validation
- **Reproducibility**: Clear methodology documentation
- **Extensibility**: Framework for future research directions
- **Standardization**: Industry-standard approach to narrative analysis

---

## 📋 **7. Next Steps**

1. **Review & Approval**: Team review of specification proposal
2. **Schema Development**: Create formal JSON schemas
3. **Validation Tools**: Build CLI and web validation tools
4. **Migration Planning**: Strategy for existing component migration
5. **Implementation Timeline**: Detailed project plan with milestones

This formal specification system will establish Narrative Gravity Wells as a rigorous, standardized framework for computational narrative analysis while maintaining the flexibility needed for ongoing research and development. 