# Framework Development Guide
*How to Create LLM-Optimized Frameworks v3.2*

## 🚀 **Quick Start: The Easy Way**

### **Step 1: Copy the Template**
```bash
cp 1_docs/frameworks/FRAMEWORK_TEMPLATE_v3.2.yaml my_new_framework.yaml
```

### **Step 2: Choose Your Language Template**
- **Brazilian Portuguese texts** → Use Template A (already active)
- **English texts** → Comment out Template A, uncomment Template B
- **Other languages** → Adapt Template B with your target language

### **Step 3: Fill in the Blanks**
Replace every `[PLACEHOLDER]` with your framework details:

```yaml
name: [your_framework_name]           # → populism_analysis
display_name: "[Your Framework]"      # → "Populism Analysis Framework"
[THEORETICAL_DOMAIN]                  # → teoria populista
[METHODOLOGY_NAME]                    # → metodologia de Mudde (2004)
```

### **Step 4: Define Your Anchors**
```yaml
components:
  populism:                          # Your anchor name
    component_id: populism           # Same as anchor name
    description: "Anti-elite rhetoric..." # What this represents
    angle: 90                        # Position on circle (0-359°)
    language_cues:                   # Specific phrases to look for
      - "elite corrupta"
      - "o povo"
      - "nós contra eles"
```

### **Step 5: Validate Your Framework**
```bash
python3 scripts/validate_framework_prompting.py my_new_framework.yaml
```

## ✅ **What Makes This Easy**

### **Built-in Best Practices**
The template automatically includes:
- ✅ **LLM-optimized prompting structure** (5-phase cognitive flow)
- ✅ **Language consistency** (no mid-prompt language switching)
- ✅ **Forward reference safety** (no references to undefined elements)
- ✅ **Complete JSON examples** (shows exactly what LLMs should output)
- ✅ **v3.2 compliance** (all required sections included)

### **Clear Guidance**
- **Placeholders** show exactly what to fill in
- **Examples** demonstrate the expected format
- **Comments** explain the purpose of each section
- **Validation script** catches common mistakes

### **Language Templates**
Pre-built templates for:
- **Brazilian Portuguese Political Discourse** (Template A)
- **English Academic Analysis** (Template B)
- Easy to adapt for other languages

## 🧠 **Understanding LLM-Optimized Prompting**

### **The Five-Phase Architecture**
The template follows a cognitive flow that LLMs process optimally:

```yaml
# PHASE 1: Who are you? (Cognitive priming)
role_definition: |
  Você é um especialista em...

# PHASE 2: What approach? (Methodology)  
framework_summary_instructions: |
  Use o [FRAMEWORK] com...

# PHASE 3: What components? (Framework structure)
components: {...}
axes: {...}

# PHASE 4: How to analyze? (Detailed instructions)
analysis_methodology: |
  Para populismo: Procure por...

# PHASE 5: What output? (JSON format)
json_format_instructions: |
  Retorne um objeto JSON...
```

### **Why This Works Better**
- **Sequential Processing**: Information builds logically
- **No Context Switching**: Consistent language and cognitive frame
- **Clear Task Definition**: LLM knows exactly what to do
- **Specific Guidance**: Removes ambiguity about analysis approach

## 🎯 **Framework Quality Checklist**

Before finalizing your framework, check:

### **✅ Language Consistency**
- [ ] All prompting elements use the same language
- [ ] Language matches your target text corpus
- [ ] No English/Portuguese mixing within prompts
- [ ] Cultural context appropriate (e.g., Brazilian vs European Portuguese)

### **✅ Component Quality**
- [ ] Each anchor has specific, actionable `language_cues`
- [ ] Descriptions explain theoretical meaning clearly
- [ ] Angles are distributed around the circle (avoid clustering)
- [ ] Core indicators help distinguish between anchors

### **✅ Prompting Excellence**
- [ ] Role definition focuses on domain expertise (not technical details)
- [ ] Analysis instructions reference framework components correctly
- [ ] Complete JSON examples provided
- [ ] Scoring scale clearly defined (0.0-1.0 with explanations)

### **✅ Academic Rigor**
- [ ] Primary sources cited in `theoretical_foundation`
- [ ] Clear theoretical approach explanation
- [ ] Proper citation format included
- [ ] Framework limitations documented

## 🚨 **Common Mistakes to Avoid**

### **❌ Language Inconsistency**
```yaml
# WRONG
role_definition: |
  You are an expert...          # English
analysis_methodology: |
  Procure por retórica...       # Portuguese
```

### **❌ Forward References**
```yaml
# WRONG
role_definition: |
  Use the language_cues defined below...
# Problem: language_cues not defined yet
```

### **❌ Vague Language Cues**
```yaml
# WRONG
language_cues:
  - "politics"        # Too vague
  - "government"      # Too general

# RIGHT  
language_cues:
  - "elite corrupta"  # Specific phrase
  - "nós contra eles" # Clear indicator
```

### **❌ Technical Role Definition**
```yaml
# WRONG
role_definition: |
  Score each anchor using the angle positions and JSON format...

# RIGHT
role_definition: |
  Você é um especialista em análise de discurso político...
```

## 📚 **Examples and References**

### **Working Examples**
- `democratic_tension_axis_model_brazil_2018.yaml` - Brazilian political discourse
- `civic_virtue_v3.2.yaml` - English political analysis
- `moral_foundations_theory_v3.2.yaml` - Academic psychological framework

### **Documentation**
- **Framework Specification v3.2**: Complete technical specification
- **LLM-Optimized Prompting Architecture**: Detailed cognitive flow explanation
- **Validation Script**: `scripts/validate_framework_prompting.py`

### **Getting Help**
If your framework validation fails:
1. **Check the error messages** - they point to specific issues
2. **Compare with working examples** - see how similar frameworks are structured
3. **Focus on language consistency** - most issues are language mixing
4. **Validate component references** - ensure all referenced elements exist

## 🎉 **Success Metrics**

Your framework is ready when:
- ✅ **Validation script passes** with no errors
- ✅ **Language consistency** throughout all elements
- ✅ **Complete examples** show expected output clearly
- ✅ **Specific language cues** for your domain/corpus
- ✅ **Academic citations** support theoretical foundation

Following this guide ensures your framework will produce consistent, high-quality analysis results with any LLM! 