# 📝 Paper Publication Repository Preparation Checklist

## Overview

This document outlines the steps needed to prepare the Narrative Gravity Maps repository for linking from the academic paper "Narrative Gravity Maps: A Quantitative Framework for Discerning the Forces Driving Persuasive Narratives."

**Goal:** Enable readers to explore the implementation, replicate key analyses, and experiment with the methodology.

## ✅ Completed Actions

- [x] Created `PAPER_REPLICATION.md` template with instructions for replicating paper analyses
- [x] Updated `README.md` with paper-specific sections explaining LLM workflow and linking to replication guide
- [x] **FIXED CRITICAL SCORING ISSUE**: Updated `generate_prompt.py` with explicit 0.0-1.0 scoring requirements
- [x] Created corrected JSON example demonstrating proper score format
- [x] Updated `README.md` with accurate JSON example using real civic_virtue framework scores
- [x] Tested corrected JSON format - visualization generation now works properly
- [x] **ADDRESSED AI PLATFORM MODEL IDENTIFICATION**: Updated prompt and documentation to handle cases where AI platforms (like Perplexity) identify themselves rather than underlying models
- [x] Added guidance for manually correcting model identification for academic accuracy
- [x] **MADE PROMPT GENERATOR FRAMEWORK-AGNOSTIC**: Removed political analysis assumptions, now works for any persuasive narrative type

## 🎯 Critical Next Steps

### 1. Complete the Replication Data Package

**Priority: HIGH - Required for replication**

- [ ] **Create directory structure:**
  ```bash
  mkdir -p model_output/paper_analyses
  mkdir -p docs/paper_figures  # Optional but recommended
  ```

- [ ] **Add LLM Score JSON Files:**
  - [ ] Create `model_output/paper_analyses/mandela_1994_inaugural_scores.json`
    - Must contain the exact LLM-generated scores used for Figure 1 in the paper
  - [ ] Create `model_output/paper_analyses/chavez_un_2006_scores.json` (or appropriate filename)
    - Must contain the exact LLM-generated scores used for Figure 2 in the paper
  - [ ] Add any additional JSON files for other analyses featured in the paper

- [ ] **Verify input texts are present:**
  - [ ] Confirm `reference_texts/mandela_1994_inaugural.txt` exists and matches the text analyzed
  - [ ] Add Hugo Chavez UN speech text (e.g., `reference_texts/chavez_un_2006.txt`)
  - [ ] Add any other texts used in paper analyses

### 2. Complete Documentation

**Priority: HIGH - Required for user guidance**

- [ ] **Update `PAPER_REPLICATION.md`:**
  - [ ] Replace `[YOUR_GIT_TAG_OR_COMMIT_HASH_HERE]` with actual version tag
  - [ ] Specify exact Chavez speech used (year, venue, etc.)
  - [ ] Add any additional analyses from the paper following the same format
  - [ ] Verify all file paths are correct

- [ ] **Update `README.md`:**
  - [ ] Replace the JSON example suggestion with a concrete, valid example
  - [ ] Ensure the example JSON matches exactly what `generate_prompt.py` requests and `narrative_gravity_elliptical.py` expects
  - [ ] Include all well names for the civic_virtue framework in the scores example
  - [ ] Review integration with existing README content

### 3. Software Versioning

**Priority: MEDIUM - Important for reproducibility**

- [ ] **Create Git tag for paper version:**
  ```bash
  git add .
  git commit -m "Prepare repository for paper publication"
  git tag v1.0-paper
  git push origin v1.0-paper
  ```
- [ ] **Update `PAPER_REPLICATION.md`** with the actual tag name
- [ ] **Document in paper** that analyses use version `v1.0-paper` of the software

### 4. Testing and Validation

**Priority: HIGH - Critical for user success**

- [ ] **Test replication steps personally:**
  - [ ] Test Streamlit app replication steps from `PAPER_REPLICATION.md`
  - [ ] Test CLI replication steps from `PAPER_REPLICATION.md`
  - [ ] Verify that loaded JSONs produce visualizations matching paper figures
  - [ ] Test the "Compare Analysis" workflow in Streamlit with paper data

- [ ] **Resolve any file path issues:**
  - [ ] Check if Streamlit comparison feature can access `model_output/paper_analyses/` subdirectory
  - [ ] If not, document workaround (e.g., copying files to `model_output/` root) in `PAPER_REPLICATION.md`

### 5. Optional Enhancements

**Priority: LOW - Nice to have**

- [ ] **Add paper figures to repository:**
  - [ ] Save Figure 1 as `docs/paper_figures/mandela_figure_1.png`
  - [ ] Save Figure 2 as `docs/paper_figures/comparative_figure_2.png`
  - [ ] Reference these in `PAPER_REPLICATION.md` as expected outputs

- [ ] **Add framework documentation:**
  - [ ] Ensure `frameworks/civic_virtue/README.md` clearly explains the framework used in the paper
  - [ ] Add academic citations and theoretical justification

## 📋 Example JSON Structure Template

**Action needed:** Replace the suggestion in `README.md` with this concrete example (adjust well names to match civic_virtue framework exactly):

```json
{
  "metadata": {
    "title": "Nelson Mandela 1994 Inaugural Address",
    "framework_name": "civic_virtue", 
    "model_name": "Claude-3-Opus",
    "analysis_date": "2024-01-15"
  },
  "scores": {
    "Dignity": 0.85,
    "Tribalism": 0.15,
    "Justice": 0.75,
    "Resentment": 0.20,
    "Truth": 0.80,
    "Manipulation": 0.10,
    "Pragmatism": 0.70,
    "Fear": 0.05,
    "Hope": 0.90,
    "Fantasy": 0.10
  },
  "text_analysis": {
    "dominant_moral_foundation": "Dignity",
    "key_moral_language": "reconciliation, freedom, human dignity, justice",
    "moral_intensity": "High"
  }
}
```

## 🎯 Final Review Checklist

Before linking from the paper, verify:

- [ ] `PAPER_REPLICATION.md` is complete and accurate for all paper analyses
- [ ] All necessary input text files are present in `reference_texts/`
- [ ] All LLM-generated JSON score files for paper analyses are correctly placed
- [ ] Replication steps tested personally from clean checkout
- [ ] Example JSON structure in `README.md` is accurate and complete
- [ ] LLM workflow clearly explained in `README.md`
- [ ] Git tag created and `PAPER_REPLICATION.md` updated with version
- [ ] Optional: Pre-generated figures included for easy reference

## 📚 Paper Integration Recommendations

### In the Paper Manuscript:

1. **Repository Link:** Include persistent URL to the GitHub repository
2. **Purpose Statement:** "This repository contains the open-source implementation of the Narrative Gravity Maps methodology described in this paper, enabling readers to explore the tools and replicate our analyses."
3. **Version Reference:** "The analyses presented in this paper were generated using version v1.0-paper of the software (available at [repository_url])."
4. **Replication Guide:** "For specific instructions on replicating the analyses and figures, see PAPER_REPLICATION.md in the repository."

### Key Points to Emphasize:

- **Manual LLM Step:** Clearly explain in the paper that the methodology involves using external LLMs and that exact replication requires the provided JSON score files
- **Streamlit App:** Highlight that readers can start with the user-friendly Streamlit interface
- **Framework Transparency:** Emphasize that all framework definitions are open and modifiable

## 🔄 Maintenance Notes

After paper publication:
- Keep the tagged version (v1.0-paper) stable
- Any future development should use new version tags
- Consider creating a branch for the paper version if significant changes are planned
- Monitor for user issues and questions in repository issues/discussions

---

**Status:** In Progress
**Next Action:** Complete replication data package (#1 above)
**Target:** Ready for paper submission 