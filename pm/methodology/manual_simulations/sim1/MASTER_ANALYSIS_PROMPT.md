# Master Analysis Prompt: Coordinate-Free Populism Validation 

## Mission
You are tasked with executing a complete **coordinate-free populism analysis** on Bolsonaro's July 22, 2018 candidacy announcement speech using the methodologically rigorous framework developed for the coordinate-free populism validation experiment. This analysis will serve as a comprehensive test of the coordinate-free approach against a known populist political text from the Brazilian 2018 election.

## Context & Significance
This is Jair Bolsonaro's formal candidacy announcement for the 2018 Brazilian presidential election, delivered at a PSL party conference. This speech is ideal for testing the coordinate-free populism framework because:
- **Cultural Specificity**: Contains Brazilian political references, coded language, and cultural markers
- **Historical Context**: Delivered during the critical 2018 election period with extensive Operation Car Wash background
- **Populist Candidate**: Bolsonaro is widely recognized as a populist figure, providing a strong test case
- **Methodological Rigor**: Enables validation of framework effectiveness on real political discourse

## Source Material
**File**: `22 de julho - Oficialização da Candidatura à presidência – Conferência PSL.m4a.txt`
**Content**: Complete transcript of Bolsonaro's candidacy announcement speech
**Length**: 1,322 lines of timestamped Portuguese speech transcript
**Context**: PSL party conference, Rio de Janeiro, July 22, 2018

## Execution Instructions

### CRITICAL: Sequential Processing Required
You MUST execute these prompts in exact sequence, as each stage depends on outputs from previous stages. Do NOT execute prompts in parallel - the dependency chain requires sequential processing.

### Stage 1: Discovery Analysis
1. **Read**: `stage_1_discovery.txt` 
2. **Substitute Variables**: Replace `{speech_text}` with the complete content from the speech transcript
3. **Execute**: Run the discovery analysis exactly as specified in the prompt
4. **Save Results**: Create `stage_1_discovery_results.md` with your complete analysis
5. **Preserve Outputs**: You will need these results for Stage 4

### Stage 2A: Populism Assessment
1. **Read**: `stage_2_populism_prompt.txt`
2. **Substitute Variables**: Replace `{speech_text}` with the complete speech transcript
3. **Execute**: Run the populism assessment exactly as specified
4. **Save Results**: Create `stage_2_populism_results.md` with your complete assessment
5. **Preserve Outputs**: You will need these results for Stage 3

### Stage 2B: Pluralism Assessment  
1. **Read**: `stage_2_pluralism_prompt.txt`
2. **Substitute Variables**: Replace `{speech_text}` with the complete speech transcript
3. **Execute**: Run the pluralism assessment exactly as specified
4. **Save Results**: Create `stage_2_pluralism_results.md` with your complete assessment
5. **Preserve Outputs**: You will need these results for Stage 3

### Stage 3: Competitive Analysis
1. **Read**: `stage_3_competitive_analysis.txt`
2. **Substitute Variables**: 
   - Replace `{populism_results}` with your complete Stage 2A output
   - Replace `{pluralism_results}` with your complete Stage 2B output
3. **Execute**: Run the competitive analysis exactly as specified
4. **Save Results**: Create `stage_3_competitive_results.md` with your complete analysis
5. **Preserve Outputs**: You will need these results for Stage 4

### Stage 4: Framework Fit Assessment
1. **Read**: `stage_4_framework_fit.txt`
2. **Substitute Variables**:
   - Replace `{discovery_results}` with your complete Stage 1 output
   - Replace `{framework_results}` with combined outputs from Stages 2A, 2B, and 3
3. **Execute**: Run the framework fit assessment exactly as specified
4. **Save Results**: Create `stage_4_framework_fit_results.md` with your complete assessment

## Quality Standards

### Analytical Rigor
- **Evidence-Based**: Support every assessment with direct quotes from the speech
- **Portuguese Preservation**: Include original Portuguese quotes with English translations
- **Cultural Competency**: Demonstrate understanding of Brazilian political context
- **Methodological Precision**: Follow prompt instructions exactly without deviation

### Brazilian Context Requirements
- **Operation Car Wash**: Recognize anti-corruption themes in context of the major scandal
- **Military References**: Understand 1964-1985 military dictatorship historical context
- **Cultural Markers**: Identify Brazilian-specific populist indicators like "cidadão de bem," "patriotas vs comunistas"
- **Religious Context**: Recognize evangelical Christian political influences
- **Regional Dynamics**: Understand Northeast/South regional political dynamics

### Output Format Standards
- **Structured Responses**: Follow the exact output formats specified in each prompt
- **Evidence Tags**: Use [EVIDENCE: "quote"] format for all textual support
- **Confidence Ratings**: Provide honest assessment of analytical certainty
- **Markdown Format**: Save all results as properly formatted markdown files

## Expected Outcomes

### Discovery Analysis (Stage 1)
You should identify themes related to:
- Anti-establishment sentiment
- Military/security themes  
- Religious/traditional values
- Economic nationalism
- Anti-corruption messaging
- Democratic governance approach

### Populism Assessment (Stage 2A)
You should find:
- **High Presence**: Clear populist themes throughout
- **High Salience**: Populist messaging as central to speech structure
- **Cultural Evidence**: Brazilian-specific populist markers
- **Strong Intensity**: Emotional populist appeals
- **High Confidence**: Clear textual evidence for populist classification

### Pluralism Assessment (Stage 2B)
You should find:
- **Lower Presence**: Limited institutional democratic themes
- **Mixed Evidence**: Some constitutional references but potentially strategic
- **Moderate-Low Confidence**: Ambiguous institutional commitment

### Competitive Analysis (Stage 3)
You should identify:
- **Coherency Pattern**: Likely "Authoritarian populist" or "Focused populist"
- **Strategic Assessment**: Possibly "Focused messaging" or "Dog whistle strategy"
- **Dominance**: Populist themes dominating over pluralist themes

### Framework Fit Assessment (Stage 4)
You should find:
- **High Coverage**: 80%+ of speech themes captured by populism/pluralism framework
- **Strong Relevance**: Populism concepts highly relevant to this discourse
- **Strong Alignment**: Discovery themes should align well with framework results
- **High Confidence**: Framework clearly appropriate for this speech type

## Validation Criteria

### Methodological Success
- [ ] All 5 prompts executed in correct sequence
- [ ] Variable substitutions performed accurately  
- [ ] Brazilian cultural context demonstrated throughout
- [ ] Evidence-based assessments with direct quotes
- [ ] Structured output formats followed exactly

### Analytical Success
- [ ] Populist themes correctly identified and characterized
- [ ] Brazilian-specific markers recognized (Operation Car Wash, military references, etc.)
- [ ] Competitive dynamics between populism/pluralism analyzed
- [ ] Framework appropriateness accurately assessed
- [ ] Confidence ratings calibrated appropriately

### Framework Validation Success
- [ ] Coordinate-free approach provides detailed anchor assessments
- [ ] Discovery-first analysis captures themes framework-first might miss
- [ ] Framework fit assessment accurately identifies high appropriateness
- [ ] Multi-stage analysis preserves analytical detail without mathematical constraints

## Research Significance

This analysis will serve as:
1. **Proof of Concept**: Demonstrates coordinate-free framework effectiveness
2. **Methodological Validation**: Tests framework on real populist discourse
3. **Cultural Validation**: Validates Brazilian-specific contextual enhancements
4. **Academic Demonstration**: Shows rigor exceeding traditional approaches

## Final Deliverables

Upon completion, the sim1 folder should contain:
- `stage_1_discovery_results.md` - Complete discovery analysis
- `stage_2_populism_results.md` - Complete populism assessment  
- `stage_2_pluralism_results.md` - Complete pluralism assessment
- `stage_3_competitive_results.md` - Complete competitive analysis
- `stage_4_framework_fit_results.md` - Complete framework fit assessment

## Success Indication

If the coordinate-free framework is working correctly, you should produce:
- **Rich, detailed analysis** that captures nuanced themes without mathematical constraints
- **High framework fit** demonstrating the populism/pluralism framework is appropriate for this speech
- **Brazilian cultural competency** showing the contextual enhancements work effectively
- **Clear evidence base** supporting all assessments with specific textual examples

Execute this analysis with the rigor and systematic approach that the coordinate-free populism validation experiment demands. This is a test of both the framework's analytical capabilities and your ability to apply sophisticated discourse analysis methodology to real political communication.

---

**Begin your analysis now. Execute each stage in sequence and save your results as specified.** 