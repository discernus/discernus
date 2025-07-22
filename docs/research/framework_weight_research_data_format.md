# Framework Weight Research Data Format
## Systematic Literature Validity Assessment Protocol

**Purpose**: Enable systematic falsification of the hypothesis that sufficient literature consensus exists for framework static weights.

**Storage Location**: `docs/research/framework_weight_validation/`

**Critical Requirement**: All research findings must be stored in structured format enabling meta-analysis and falsification.

---

## Data Structure Specification

### Per Research Question Format

Each research question generates a standardized JSON research report:

```json
{
  "research_question_id": "A1_relational_dynamics",
  "question": "What does peer-reviewed research say about the relative impact of hostile vs. cooperative discourse on community social cohesion?",
  "framework_target": "CFF v4.2 Amity-Enmity weight (0.40)",
  "discernus_librarian_session": {
    "session_id": "discernus_librarian_2025_01_20_A1",
    "timestamp": "2025-01-20T15:30:00Z", 
    "model_used": "vertex_ai/gemini-2.5-flash",
    "search_apis": ["semantic_scholar", "crossref", "google_scholar"],
    "search_terms": ["hostile discourse", "cooperative communication", "social cohesion"]
  },
  "literature_corpus": {
    "papers_found": 23,
    "papers_analyzed": 15,
    "excluded_papers": 8,
    "exclusion_reasons": ["not_peer_reviewed", "insufficient_relevance", "no_quantitative_data"]
  },
  "research_findings": {
    "consensus_strength": "weak", // strong | moderate | weak | absent
    "effect_sizes_available": true,
    "sample_sizes_adequate": false,
    "replication_evidence": "limited",
    "direct_weight_guidance": false,
    "research_quality_score": 6.2, // 0-10 scale
    "key_findings": [
      "Cooperative discourse increases social capital (Cohen's d = 0.34, n=1200, p<0.01)",
      "Hostile discourse correlates with reduced civic engagement (r = -0.28, mixed evidence)",
      "No studies directly compare 0.40 vs alternative weightings"
    ]
  },
  "falsification_assessment": {
    "literature_consensus_exists": false,
    "evidence_quality": "provisional", // established | provisional | speculative | unknown
    "weight_validity_classification": "🟠 Speculative",
    "research_gaps": [
      "No studies specifically test discourse-cohesion weight ratios",
      "Limited experimental evidence on causation",  
      "Insufficient cross-cultural validation"
    ],
    "recommendation": "Current 0.40 weight lacks empirical support. Recommend provisional classification pending additional research."
  },
  "confidence_metrics": {
    "search_completeness": 0.85,
    "quality_assessment_confidence": 0.78,
    "synthesis_confidence": 0.72,
    "discernus_librarian_reliability": 0.80
  }
}
```

---

## Falsification Criteria Framework

### **Dual Hypotheses to Test**
**Social Health Hypothesis**: *"There exists sufficient literature consensus to justify Social Health weight assignments (normative analysis) in framework triple weighting systems."*

**Strategic Effectiveness Hypothesis**: *"There exists sufficient literature consensus to justify Strategic Effectiveness weight assignments (pragmatic analysis) in framework triple weighting systems."*

**Ethical Tension Hypothesis**: *"Strategic Effectiveness optimal weights conflict with Social Health optimal weights, creating ethical tensions between political success and social wellbeing."*

### **Literature Consensus Classification**

**🟢 ESTABLISHED** (High Confidence):
- 5+ high-quality peer-reviewed studies
- Consistent findings across multiple methodologies  
- Large sample sizes (>1000 total participants)
- Effect sizes documented with confidence intervals
- Replication across different populations/contexts

**🟡 PROVISIONAL** (Medium Confidence):
- 2-4 peer-reviewed studies supporting claim
- Some methodological variation but consistent direction
- Moderate sample sizes (100-1000 total participants)
- Some effect sizes available, limited replication
- Theoretical foundation with partial empirical support

**🟠 SPECULATIVE** (Low Confidence):
- 1-2 studies or primarily theoretical reasoning
- Limited empirical support or mixed findings
- Small sample sizes (<100) or convenience samples
- No effect sizes or weight-specific guidance
- Theoretical appeal but insufficient validation

**🔴 UNKNOWN** (No Research Basis):
- No relevant studies found
- Research exists but on different constructs
- Weight assignments appear convenience-based
- No theoretical or empirical justification
- Pure assumption or convention

### **Falsification Thresholds**

**Social Health Research Domain**:
- **SUPPORTED** if ≥60% of Social Health weights achieve 🟢 or 🟡 status
- **FALSIFIED** if <40% achieve 🟢 or 🟡 status  
- **MIXED EVIDENCE** if 40-60% achieve sufficient support

**Strategic Effectiveness Research Domain**:
- **SUPPORTED** if ≥60% of Strategic Effectiveness weights achieve 🟢 or 🟡 status
- **FALSIFIED** if <40% achieve 🟢 or 🟡 status
- **MIXED EVIDENCE** if 40-60% achieve sufficient support

**Ethical Tension Analysis**:
- **HIGH CONFLICT** if Social Health and Strategic Effectiveness recommend opposite weight patterns (e.g., Hope vs Fear emphasis)
- **MODERATE CONFLICT** if weight recommendations differ significantly but same direction
- **LOW CONFLICT** if weight patterns align but with different magnitudes
- **NO CONFLICT** if both domains recommend similar weight patterns

---

## Meta-Analysis Protocol

### **Cross-Framework Validity Assessment**

After completing all research questions, aggregate analysis examining:

1. **Framework Validity Patterns**: Which frameworks have strongest research foundations?
2. **Dimension Type Patterns**: Which types of dimensions (emotional, relational, identity) have best research support?
3. **Weight Assignment Patterns**: Are equal weights vs. hierarchical weights vs. specific ratios better supported?
4. **Research Gap Patterns**: What systematic research needs emerge?

### **Dual-Domain Systematic Comparison Matrix**

**Social Health Research Domain**:
```
Framework | Dimensions | 🟢 Established | 🟡 Provisional | 🟠 Speculative | 🔴 Unknown | Classification
CFF v4.2  |     5      |       ?        |       ?        |       ?        |      ?     | TBD
ECF v1.0  |     6      |       ?        |       ?        |       ?        |      ?     | TBD  
CAF v4.1  |    10      |       ?        |       ?        |       ?        |      ?     | TBD
CHF v1.0  |     3      |       ?        |       ?        |       ?        |      ?     | TBD
```

**Strategic Effectiveness Research Domain**:
```
Framework | Dimensions | 🟢 Established | 🟡 Provisional | 🟠 Speculative | 🔴 Unknown | Classification
CFF v4.2  |     5      |       ?        |       ?        |       ?        |      ?     | TBD
ECF v1.0  |     6      |       ?        |       ?        |       ?        |      ?     | TBD  
CAF v4.1  |    10      |       ?        |       ?        |       ?        |      ?     | TBD
CHF v1.0  |     3      |       ?        |       ?        |       ?        |      ?     | TBD
```

**Ethical Tension Assessment Matrix**:
```
Framework | Dimension Pairs | Social Health Weight | Strategic Effectiveness Weight | Conflict Level | Ethical Impact
CFF v4.2  | Hope-Fear       | 0.25 (Hope emphasis) | 0.40 (Fear emphasis)          | HIGH          | Strategy vs Wellbeing
CFF v4.2  | Amity-Enmity    | 0.35 (Amity emphasis)| 0.30 (Enmity emphasis)        | HIGH          | Unity vs Mobilization
ECF v1.0  | Fear-Hope       | TBD                  | TBD                           | TBD           | TBD
```

---

## Implementation Notes

### **File Organization**
```
docs/research/framework_weight_validation/
├── research_questions/
│   ├── social_health/                    # Issues #91-95: Normative research
│   │   ├── A1_relational_dynamics.json
│   │   ├── A2_emotional_climate.json
│   │   ├── A3_identity_foundation.json
│   │   ├── B1_constitutional_health.json
│   │   └── D1_measurement_methodology.json
│   ├── strategic_effectiveness/          # Issues #97-99: Pragmatic research
│   │   ├── SE1_campaign_effectiveness.json
│   │   ├── SE2_political_mobilization.json
│   │   └── SE3_populist_success_patterns.json
│   └── comparative_analysis/
│       └── ethical_tension_assessment.json
├── discernus_librarian_sessions/
│   ├── social_health/
│   │   ├── session_A1_20250120/
│   │   └── session_A2_20250121/
│   └── strategic_effectiveness/
│       ├── session_SE1_20250120/
│       └── session_SE2_20250121/
├── meta_analysis/
│   ├── social_health_falsification_summary.json
│   ├── strategic_effectiveness_falsification_summary.json
│   ├── ethical_tension_analysis.json
│   └── triple_weighting_framework_validation.json
└── README.md (this file)
```

### **Quality Assurance**
- Each research question requires independent DiscernusLibrarian session
- Cross-validation through different search strategies  
- Explicit confidence intervals and uncertainty quantification
- Complete citation and methodology transparency

**Strategic Value**: This systematic approach enables definitive falsification of literature consensus assumptions while identifying specific research needs for strengthening framework validity. 