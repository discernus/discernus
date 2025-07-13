# Experiment: Single-LLM Bias Isolation Pilot
## Test Bias Detection Protocol Before Multi-LLM Study

**Date**: January 13, 2025  
**Framework**: PDAF v1.1 (Sanitized)  
**Analysis Type**: Bias isolation validation  
**Expected Duration**: 30-45 minutes  
**Purpose**: Validate bias detection methodology with single model

---

## Objective

Test the complete bias isolation protocol with one LLM:
1. Validate speaker identity bias exists (original vs sanitized)
2. Test cross-linguistic mitigation (sanitized vs Esperanto)
3. Confirm raw score collection works correctly
4. Validate statistical analysis pipeline

---

## Methodology

**Single-Model Design**:
- **Corpus**: 4 speeches (Romney, McCain, Lewis, Booker)
- **Models**: Claude 3.5 Sonnet only 
- **Conditions**: All 3 corpus conditions (original, sanitized English, Esperanto)
- **Workflow**: RAW_AGGREGATION (bias isolation protocol)

**Configuration**:
```yaml
remove_synthesis: true  # CRITICAL: Bias isolation protocol
models: ["claude-3.5-sonnet"]
corpus_conditions: ["original", "sanitized_english", "sanitized_esperanto"]
```

**Analysis Pipeline**:
1. **Bias Detection**: Compare original vs sanitized English scores
2. **Cross-Linguistic Test**: Compare sanitized English vs Esperanto scores
3. **Statistical Validation**: Calculate bias magnitude and correlation
4. **Methodology Validation**: Confirm protocol works before full study

---

## Expected Outcomes

**Bias Detection Hypothesis**:
- Original condition: Scores influenced by speaker identity
- Sanitized condition: Reduced identity bias
- Esperanto condition: Further bias reduction with maintained validity

**Success Criteria**:
- Detectable score differences between original and sanitized conditions
- High correlation between sanitized English and Esperanto (r > 0.8)
- Clean raw score collection without synthesis contamination
- Statistical pipeline generates meaningful bias measurements

---

## Implementation Notes

**Setup Commands**:
```bash
# Create pilot corpus
mkdir -p experiments/02_single_llm_pilot/corpus/{original,sanitized_english,sanitized_esperanto}

# Copy 4 speeches across conditions
cp corpus/original/mitt_romney_2020_impeachment.txt experiments/02_single_llm_pilot/corpus/original/
cp corpus/original/john_mccain_2008_concession.txt experiments/02_single_llm_pilot/corpus/original/
cp corpus/original/john_lewis_1963_march_on_washington.txt experiments/02_single_llm_pilot/corpus/original/
cp corpus/original/cory_booker_2018_first_step_act.txt experiments/02_single_llm_pilot/corpus/original/

# Copy sanitized versions
cp corpus/sanitized_english/sanitized_speech_f9b8c2d7.md experiments/02_single_llm_pilot/corpus/sanitized_english/
cp corpus/sanitized_english/sanitized_speech_a1c5e7d2.md experiments/02_single_llm_pilot/corpus/sanitized_english/
cp corpus/sanitized_english/sanitized_speech_c6d4a3e8.md experiments/02_single_llm_pilot/corpus/sanitized_english/
cp corpus/sanitized_english/sanitized_speech_b3f7d2a6.md experiments/02_single_llm_pilot/corpus/sanitized_english/

# Copy Esperanto versions
cp corpus/sanitized_esperanto/9c759f7025a4_esperanto.txt experiments/02_single_llm_pilot/corpus/sanitized_esperanto/
cp corpus/sanitized_esperanto/c7cc43197100_esperanto.txt experiments/02_single_llm_pilot/corpus/sanitized_esperanto/
cp corpus/sanitized_esperanto/6a2ff5ec9d0a_esperanto.txt experiments/02_single_llm_pilot/corpus/sanitized_esperanto/
cp corpus/sanitized_esperanto/cccec508db40_esperanto.txt experiments/02_single_llm_pilot/corpus/sanitized_esperanto/
```

**Analysis**: 4 speeches × 3 conditions × 1 model = 12 analyses (~$2-3 cost, 30-45 minutes)

This pilot validates the complete bias isolation methodology before committing to the full 864-analysis study. 