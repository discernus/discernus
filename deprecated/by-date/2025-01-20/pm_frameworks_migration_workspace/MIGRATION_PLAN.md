# Framework Migration Plan & Status

**Date**: July 19, 2025  
**Objective**: Migrate all historical frameworks to V4.0 Markdown specification  
**Target**: Framework Specification v4.0 compliance

---

## Migration Status

### ✅ **Completed Migrations**

#### 1. **Cohesive Flourishing Framework (CFF) v4.1** 
- **Status**: ✅ Already V4 compliant
- **Location**: `pm/frameworks/Cohesive Flourishing Framework (CFF) v4.1.md`
- **Quality**: Gold standard example of V4 format

#### 2. **Political Worldview Triad v4.0**
- **Status**: ✅ Migrated from v3.2 YAML
- **Location**: `pm/frameworks/political_worldview_triad_v4.md`
- **Source**: `3_2_spec_frameworks/political_worldview_triad/political_worldview_triad_v3.2.yaml`

#### 3. **Civic Virtue Framework v4.0**
- **Status**: ✅ Migrated from v3.2 YAML  
- **Location**: `pm/frameworks/civic_virtue_v4.md`
- **Source**: `3_2_spec_frameworks/civic_virtue/civic_virtue_v3.2.yaml`

### 🔄 **Remaining Frameworks to Migrate**

#### 4. **Moral Foundations Theory (MFT)**
- **Source**: `3_2_spec_frameworks/moral_foundations_theory/moral_foundations_theory_v3.2.yaml`
- **Target**: `moral_foundations_theory_v4.md`
- **Complexity**: High (6 foundation pairs, rich theoretical content)

#### 5. **Business Ethics Framework**
- **Source**: `3_2_spec_frameworks/business_ethics/business_ethics_v3.2.yaml`
- **Target**: `business_ethics_v4.md`
- **Complexity**: Medium

#### 6. **Political Discourse Framework**
- **Source**: `3_2_spec_frameworks/political_discourse/political_discourse_v3.2.yaml`
- **Target**: `political_discourse_v4.md`
- **Complexity**: Medium

#### 7. **Political Framing Theory**
- **Source**: `3_2_spec_frameworks/political_framing_theory/political_framing_theory_v3.2.yaml`
- **Target**: `political_framing_theory_v4.md`
- **Complexity**: Medium

#### 8. **IDITI Framework**
- **Source**: `3_2_spec_frameworks/iditi/iditi_v3.2.yaml`
- **Target**: `iditi_v4.md`
- **Complexity**: Medium

#### 9. **Populism-Pluralism Framework**
- **Source**: `3_2_spec_frameworks/populism_pluralism/populism_pluralism_v3.2.yaml`
- **Target**: `populism_pluralism_v4.md`
- **Complexity**: Medium

### 📋 **Legacy Frameworks to Review**

#### 10. **CFF v3.1 Enhanced Linguistic Markers**
- **Source**: `cff_3_1_enhanced_linguistic_markers.md`
- **Action**: Assess if content should be merged into CFF v4.1 or archived

#### 11. **CFF v3.1 Production Agent Instructions**
- **Source**: `cff_v3_1_production_agent_instructions.md`
- **Action**: Archive (superseded by CFF v4.1)

#### 12. **PDAF v1.1 Production Agent Instructions**
- **Source**: `pdaf_v1.1_production_agent_instructions.md`
- **Action**: Evaluate for V4 upgrade or archive

#### 13. **Coordinate Free Experiment Schema**
- **Source**: `coordinate_free_experiment_schema_specification.md`
- **Action**: Review relevance to V4 specification

---

## Migration Methodology

### V4.0 Transformation Process

**From**: V3.2 YAML Configuration
```yaml
name: framework_name
description: |
  Complex YAML structure...
anchors:
  anchor_name:
    description: "..."
    language_cues: [...]
```

**To**: V4.0 Markdown + JSON
```markdown
# Framework Name v4.0
Rich human-readable narrative...

<details><summary>Machine-Readable Configuration</summary>
{
  "name": "framework_name",
  "analysis_variants": {...}
}
</details>
```

### Key Transformations

1. **Theoretical Content**: YAML comments → Rich Markdown narrative
2. **Language Cues**: YAML arrays → Natural language prompt instructions  
3. **Configuration**: Complex YAML → Clean JSON appendix
4. **Prompts**: Technical specifications → Conversational expert briefings
5. **Evidence**: Structured requirements → Natural evidence collection

### Quality Standards

- ✅ **Documentation-Execution Coherence**: Methodology matches prompts exactly
- ✅ **Natural Language Prompts**: Expert briefings, not technical specs
- ✅ **Rich Evidence**: Multiple quotations per dimension
- ✅ **Academic Validation**: Complete theoretical grounding
- ✅ **JSON Compliance**: Clean, parseable configuration

---

## Execution Options

### Option 1: Automated Migration
**Command**: 
```bash
cd /Volumes/code/discernus/pm/frameworks
python3 framework_migrator.py
```
**Pros**: Fast, consistent, processes all frameworks
**Cons**: May need manual review and refinement

### Option 2: Manual Migration
**Process**: Individual framework conversion using examples as templates
**Pros**: Higher quality, custom refinement
**Cons**: Time-intensive, requires framework expertise

### Option 3: Hybrid Approach (Recommended)
1. **Auto-migrate** remaining frameworks for structure
2. **Manual review** and enhancement for quality
3. **Validation testing** with sample texts

---

## Quality Assurance Plan

### 1. **Specification Compliance**
- [ ] Human-readable methodology section
- [ ] Machine-readable JSON appendix  
- [ ] Natural language analysis prompts
- [ ] Complete output contract schema

### 2. **Content Preservation**
- [ ] All theoretical content preserved
- [ ] Academic sources maintained
- [ ] Analytical capabilities retained
- [ ] Version history documented

### 3. **Enhancement Opportunities**
- [ ] Improved prompt naturalness
- [ ] Enhanced evidence requirements
- [ ] Clearer methodological explanations
- [ ] Better academic integration

### 4. **Validation Testing**
- [ ] Test each framework with sample texts
- [ ] Verify JSON parsing works correctly
- [ ] Confirm prompt generates expected outputs
- [ ] Validate against V4 specification

---

## Timeline Estimate

**Immediate** (Today):
- ✅ 3 frameworks completed (CFF, Political Worldview Triad, Civic Virtue)

**Next Session** (1-2 hours):
- 🔄 Complete remaining 6 framework migrations
- 📋 Review legacy frameworks for archival decisions

**Quality Assurance** (1 hour):
- 🧪 Test migrated frameworks with sample texts
- 🔍 Review for specification compliance
- 📝 Document migration outcomes

**Total Estimated Effort**: 2-3 hours for complete migration

---

## Success Metrics

1. **Coverage**: All active frameworks migrated to V4.0
2. **Quality**: Full specification compliance
3. **Functionality**: All frameworks generate valid outputs
4. **Documentation**: Complete theoretical preservation
5. **Usability**: Natural language prompts work effectively

---

## Next Actions

**Immediate Priority**:
1. **Complete Migration**: Process remaining 6 frameworks
2. **Quality Review**: Test and refine migrated frameworks  
3. **Archive Legacy**: Move superseded frameworks to archive
4. **Update Documentation**: Ensure all references point to V4 frameworks

**Ready to Execute**: All tools and examples are prepared for immediate migration.
