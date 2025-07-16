# Stage 6 Universal Template Specification
**Version:** 2.0  
**Date:** January 25, 2025  
**Status:** IMPLEMENTATION SPECIFICATION  
**Replaces:** Deprecated automated generation approach

---

## **Executive Summary**

This document specifies the **universal template architecture** for Stage 6 analysis, defining clean, executable templates that adapt to any Framework Specification v3.2 compliant experiment.

**Core Strategy**: Universal template that intelligently loads experiment data and adapts to framework structure, using standard libraries (NumPy, Matplotlib, Pandas) with transparent, executable code that researchers run naturally.

**Key Principle**: Templates provide excellent starting points that researchers can understand, modify, and extend, rather than automated generation with pre-executed outputs.

---

## **Strategic Framework Portfolio**

### **Framework Selection Criteria**

**Pareto Efficiency Dimensions:**
- **Anchor Complexity**: 3, 4, 5, 10 anchors (covers simple → complex spectrum)
- **Relationship Types**: Competitive, Complementary, Hierarchical, Triangular
- **Domain Coverage**: Political Science, Moral Psychology, Business Ethics, Institutional Analysis
- **Analysis Patterns**: Temporal Evolution, Comparative Studies, Cross-Cultural, Regulatory Compliance

### **The Strategic Five**

#### **1. Tamaki-Fuks Competitive Populism** ✅ *COMPLETED*
- **Anchors**: 3 (Populism, Nationalism, Patriotism)
- **Relationships**: Competitive dynamics with dilution effects
- **Pattern**: Temporal evolution, strategic discourse analysis
- **Domain**: Political campaign analysis, populism research
- **Status**: Production template complete (stage5_to_stage6_sarah_experience.ipynb)

#### **2. Moral Foundations Theory** 🔄 *NEXT PRIORITY*
- **Anchors**: 5 (Care/Harm, Fairness/Cheating, Loyalty/Betrayal, Authority/Subversion, Sanctity/Degradation)
- **Relationships**: Complementary moral psychology
- **Pattern**: Cross-cultural value analysis, moral reasoning
- **Domain**: Moral psychology, cultural studies, value systems
- **Implementation**: Complementary dynamics template

#### **3. Civic Virtue Framework** 🔄 *HIGH COMPLEXITY*
- **Anchors**: 10 (5 virtues + 5 vices in clustered arrangement)
- **Relationships**: Virtue-vice opposition, hierarchical clustering
- **Pattern**: Democratic discourse quality, institutional analysis
- **Domain**: Political communication, civic engagement, institutional health
- **Implementation**: Hierarchical cluster template with arc positioning

#### **4. Political Worldview Triad** 🔄 *COMPARATIVE*
- **Anchors**: 3 (Left, Right, Populist positioning)
- **Relationships**: Triangular positioning space
- **Pattern**: Comparative entity analysis, positioning studies
- **Domain**: Comparative politics, candidate positioning, party analysis
- **Implementation**: Triangular comparative template

#### **5. Business Ethics Framework** 🔄 *REGULATORY*
- **Anchors**: 4 (Stakeholder responsibility, Legal compliance, Environmental stewardship, Ethical leadership)
- **Relationships**: Regulatory compliance dynamics
- **Pattern**: Corporate communication analysis, ESG compliance
- **Domain**: Business communication, corporate ethics, regulatory analysis
- **Implementation**: Compliance tracking template

---

## **Template Pattern Architecture**

### **Pattern Classification System**

```python
TEMPLATE_PATTERNS = {
    'competitive_dynamics': {
        'frameworks': ['tamaki_fuks_competitive_populism'],
        'anchor_range': [3, 4],
        'features': [
            'competitive_dilution_modeling',
            'strategic_temporal_evolution', 
            'campaign_trajectory_analysis',
            'dual_panel_visualization'
        ],
        'visualizations': [
            'coordinate_space_with_competition_lines',
            'competitive_effects_boxplot',
            'temporal_evolution_complex_grid',
            'strategic_trajectory_mapping'
        ]
    },
    
    'complementary_moral': {
        'frameworks': ['moral_foundations_theory'],
        'anchor_range': [5, 6],
        'features': [
            'value_balance_analysis',
            'cross_cultural_comparison',
            'moral_reasoning_patterns',
            'stability_over_time'
        ],
        'visualizations': [
            'moral_foundation_balance_chart',
            'cultural_comparison_radar',
            'temporal_moral_evolution',
            'value_system_heatmap'
        ]
    },
    
    'hierarchical_institutional': {
        'frameworks': ['civic_virtue_framework'],
        'anchor_range': [8, 12],
        'features': [
            'virtue_vice_clustering',
            'institutional_health_metrics',
            'democratic_discourse_quality',
            'complex_relationship_modeling'
        ],
        'visualizations': [
            'clustered_arc_positioning',
            'virtue_vice_opposition_analysis',
            'institutional_health_dashboard',
            'democratic_quality_metrics'
        ]
    },
    
    'triangular_comparative': {
        'frameworks': ['political_worldview_triad'],
        'anchor_range': [3, 3],
        'features': [
            'entity_comparison_analysis',
            'positioning_relative_analysis',
            'competitive_landscape_mapping',
            'movement_tracking'
        ],
        'visualizations': [
            'triangular_positioning_space',
            'comparative_entity_analysis',
            'positioning_shift_tracking',
            'competitive_landscape_overview'
        ]
    },
    
    'regulatory_compliance': {
        'frameworks': ['business_ethics_framework'],
        'anchor_range': [4, 5],
        'features': [
            'compliance_tracking',
            'stakeholder_analysis',
            'risk_assessment_modeling',
            'regulatory_trend_analysis'
        ],
        'visualizations': [
            'compliance_dashboard',
            'stakeholder_impact_analysis',
            'regulatory_risk_heatmap',
            'trend_compliance_tracking'
        ]
    }
}
```

### **Template Selection Logic**

```python
def select_template_pattern(framework_yaml):
    """Auto-select appropriate template pattern based on framework characteristics"""
    
    framework = yaml.safe_load(framework_yaml)
    anchor_count = len(framework.get('anchors', {}))
    
    # Pattern matching logic
    if 'competitive_relationships' in framework:
        if anchor_count <= 4:
            return 'competitive_dynamics'
        else:
            return 'hierarchical_institutional'
    
    elif 'moral_foundations' in framework.get('name', '').lower():
        return 'complementary_moral'
    
    elif 'triad' in framework.get('name', '').lower():
        return 'triangular_comparative'
    
    elif 'business' in framework.get('name', '').lower() or 'ethics' in framework.get('name', '').lower():
        return 'regulatory_compliance'
    
    else:
        # Generic fallback based on anchor count
        if anchor_count <= 4:
            return 'competitive_dynamics'  # Simplest robust template
        elif anchor_count <= 6:
            return 'complementary_moral'
        else:
            return 'hierarchical_institutional'
```

---

## **Technical Implementation Architecture**

### **Template Structure**

```
templates/
├── base/
│   ├── standard_library_foundation.py
│   ├── publication_standards.py
│   ├── coordinate_mathematics.py
│   └── export_utilities.py
├── patterns/
│   ├── competitive_dynamics/
│   │   ├── template.ipynb
│   │   ├── visualization_functions.py
│   │   └── analysis_functions.py
│   ├── complementary_moral/
│   │   ├── template.ipynb
│   │   ├── visualization_functions.py
│   │   └── analysis_functions.py
│   ├── hierarchical_institutional/
│   │   ├── template.ipynb
│   │   ├── visualization_functions.py
│   │   └── analysis_functions.py
│   ├── triangular_comparative/
│   │   ├── template.ipynb
│   │   ├── visualization_functions.py
│   │   └── analysis_functions.py
│   └── regulatory_compliance/
│       ├── template.ipynb
│       ├── visualization_functions.py
│       └── analysis_functions.py
└── generator/
    ├── template_selector.py
    ├── notebook_generator.py
    └── framework_adapter.py
```

### **Universal Template Workflow**

```python
# Simple template copying approach
def setup_stage6_template(experiment_results, framework_path, results_dir):
    """Copy universal template and save experiment data for loading"""
    
    # 1. Copy universal template to results directory
    template_source = "templates/universal_analysis_template.ipynb"
    template_destination = results_dir / "stage6_interactive_analysis.ipynb"
    shutil.copy(template_source, template_destination)
    
    # 2. Save experiment data in standard format for template to load
    experiment_data = {
        'results': experiment_results,
        'framework_path': framework_path,
        'timestamp': datetime.now().isoformat(),
        'job_id': experiment_results.get('job_id')
    }
    
    data_path = results_dir / "experiment_data.json"
    with open(data_path, 'w') as f:
        json.dump(experiment_data, f, indent=2)
    
    # 3. Copy framework YAML for provenance
    framework_dest = results_dir / "framework_definition.yaml"
    shutil.copy(framework_path, framework_dest)
    
    return template_destination

# Template intelligently loads data when user runs cells
# No pre-execution, no base64 garbage, just clean executable code
```

---

## **Academic Validation Strategy**

### **Stakeholder Validation Plan**

**Phase 1: Framework-Specific Validation**
- **Sarah Chen (BYU)**: Tamaki-Fuks + Political Triad templates
- **Moral Psychology Expert**: MFT template review and validation
- **Governance Researcher**: Civic Virtue institutional analysis validation
- **Business Ethics Expert**: Corporate compliance template validation

**Phase 2: Cross-Framework Validation**
- **Template Pattern Consistency**: Ensure similar quality across all patterns
- **Academic Publication Standards**: Verify Nature journal compliance
- **Reproducibility Testing**: Independent replication validation
- **User Experience Testing**: Graduate student usability assessment

### **Quality Metrics**

**Technical Validation:**
- ✅ Template generates error-free notebooks for all 5 frameworks
- ✅ Visualizations meet academic publication standards (300 DPI, proper fonts)
- ✅ Export functionality works across all formats (EPS, PDF, PNG, SVG)
- ✅ Mathematical operations transparent and auditable

**Academic Validation:**
- ✅ Framework-specific insights align with theoretical expectations
- ✅ Statistical analyses appropriate for each framework type
- ✅ Narrative and interpretation quality suitable for publication
- ✅ Peer reviewer acceptance for methodology transparency

**User Experience Validation:**
- ✅ "Run All Cells" executes without errors
- ✅ Generated insights immediately useful for research
- ✅ Customization points clear and accessible
- ✅ Publication workflow seamless

---

## **GPL Defense Strategy**

### **Extensibility Framework**

**When researchers request Framework #6:**

```
"We've shipped with the 5 most important theoretical frameworks covering 90% 
of computational discourse research. These templates represent thousands of 
hours of academic-quality development and validation.

The entire system is GPL-licensed. The architecture is designed for extension:

1. Fork the repository
2. Add your framework to the portfolio
3. Choose the closest template pattern or create a new one
4. Validate against our academic standards
5. Submit a pull request with documentation

Want custom features? Build them.
Want support? Sponsor the project.
Want complaining? There's Reddit."
```

**Technical Extension Points:**
- Framework portfolio easily extensible
- Template pattern system supports new patterns
- All visualization components modular and reusable
- Academic validation process documented and replicable

---

## **Implementation Timeline**

### **Week 1-2: Pattern Generalization**
- Extract reusable components from Tamaki-Fuks template
- Create base template infrastructure
- Develop template selection logic

### **Week 3-4: MFT Template Development**
- Build complementary moral psychology template
- Validate with moral psychology expert
- Integrate with template selection system

### **Week 5-6: Civic Virtue Template Development**
- Build hierarchical institutional template (most complex)
- Handle 10-anchor clustered visualization
- Validate with governance researcher

### **Week 7-8: Remaining Templates**
- Political Worldview Triad (triangular comparative)
- Business Ethics Framework (regulatory compliance)
- Cross-template consistency validation

### **Week 9-10: Integration & Testing**
- Full integration with `run_experiment.py`
- End-to-end testing with all 5 frameworks
- Academic stakeholder final validation
- Documentation and deployment

---

## **Success Metrics & Acceptance Criteria**

### **Technical Success**
- [ ] All 5 framework templates generate error-free notebooks
- [ ] Template selection logic 100% accurate for target frameworks
- [ ] Publication exports meet academic standards across all patterns
- [ ] Integration with `run_experiment.py` seamless

### **Academic Success**
- [ ] Each template validated by domain expert
- [ ] Generated analyses suitable for peer-reviewed publication
- [ ] Methodology transparent and reproducible
- [ ] Statistical approaches appropriate for each framework type

### **Platform Success**
- [ ] GPL extensibility framework documented and validated
- [ ] Template pattern system supports new framework addition
- [ ] Research value covers 90% of computational discourse research needs
- [ ] User experience meets graduate student usability standards

---

**Status:** UPDATED FOR UNIVERSAL TEMPLATE APPROACH  
**Architecture Change:** Moved from automated generation to clean, executable templates
**Next Steps:** Implement universal template that adapts to any spec-validated experiment

## **Strategic Architecture Change**

**Previous Approach (DEPRECATED):** Complex automated generation with pre-executed cells
**New Approach (APPROVED):** Universal template with intelligent data loading

**Key Benefits:**
- ✅ **Academic Trust**: Transparent, executable code researchers can understand
- ✅ **Maintainable**: Single template instead of complex generation system  
- ✅ **Flexible**: Researchers can adapt templates for their specific needs
- ✅ **Reliable**: Standard library foundation eliminates custom bugs

**Cross-References:** 
- [DCS Research Workflow Specification v1.0](../1_docs/specs/DCS_Research_Workflow_Specification_1_0.md)
- [Discernus Experiment System Specification v3.2.0](../1_docs/specs/Discernus_Experiment_System_Specification_v3.2.0.md)
- [Sarah Experience Notebook](../../examples/notebooks/stage5_to_stage6_sarah_experience.ipynb) (Reference implementation) 