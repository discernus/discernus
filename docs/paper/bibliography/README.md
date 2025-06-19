# Bibliography - Political Corpora and Corpus Analysis Resources

## Overview

This directory contains bibliographical resources for political text corpora and corpus analysis methodologies relevant to narrative gravity research.

## ⚠️ **AI Citation Safeguards** - **MANDATORY VERIFICATION PROTOCOL**

### 🚨 **Critical Warning**: 
AI assistants frequently generate plausible-sounding but completely **fabricated citations**. This project discovered 3 fake citations that were nearly published.

### 📋 **Verification Requirements**
**ALL citations from AI sources must be verified before inclusion:**

1. **Google Scholar Search** - Exact title + author verification
2. **DOI Verification** - Must resolve to actual paper  
3. **Journal Website Check** - Confirm publication exists
4. **Multiple Source Confirmation** - At least 2 independent verification methods

### 🛠️ **Verification Tools**
- **Quick Check**: `python3 scripts/verify_citations.py --title "Paper Title" --authors "Authors"`
- **Complete Safeguard Guide**: `docs/paper/bibliography/AI_BIBLIOGRAPHY_SAFEGUARDS.md`
- **Verification Tracking**: All citations marked with verification status

### ✅ **Verification Status Legend**
- 🟢 **VERIFIED** - Confirmed through multiple sources + DOI
- 🟡 **MANUAL_CHECK** - Requires human verification  
- 🔴 **AI_HALLUCINATION** - Confirmed fake (do not use)
- ⚪ **UNVERIFIED** - Not yet checked (verify before use)

### 📚 **Current Bibliography Status**
- ✅ `methodology_core_references.bib` - All verified December 2024
- ✅ `political_corpora_resources.bib` - Human curated, no AI input
- 📋 `methodology_paper_references.md` - Verification tracking active

**NEVER directly copy AI-suggested citations into bibliography files.**

## Files in This Directory

### 📚 **[political_corpora_resources.bib](political_corpora_resources.bib)**
**BibTeX bibliography file** containing formal citations for:
- **4 Major Political Text Corpora**: HKBU, German, Spanish, CORPS
- **11 Corpus Analysis Research Papers**: Methodology and application studies
- **4 Infrastructure Resources**: CLARIN, Wikipedia, technical documentation

**Usage**: Import into LaTeX/Markdown documents for formal citations
**Format**: Standard BibTeX format compatible with academic publishing

### 🔬 **[methodology_core_references.bib](methodology_core_references.bib)**
**BibTeX bibliography file** for methodology paper references:
- **Computational Text Analysis**: Grimmer & Stewart, Lucas et al., Hopkins & King
- **Theoretical Frameworks**: Moral Foundations, Framing Theory, Cultural Theory
- **Validation Methods**: Expert consultation, convergent validity, reproducibility
- **Status**: Active collection phase - many references need verification

**Usage**: Core citations for Discernus methodology paper
**Format**: Standard BibTeX with verification status tracking

### 📋 **[methodology_paper_references.md](methodology_paper_references.md)**
**Reference tracking document** for methodology paper bibliography:
- **Citation Status Tracking**: Verified, needs verification, questionable
- **Collection Strategy**: Priority ordering and search procedures  
- **Quality Control**: Verification process and BibTeX standards
- **Integration Plan**: Coordination with existing bibliography files

### 📊 **[corpus_analysis_for_narrative_gravity.md](corpus_analysis_for_narrative_gravity.md)**
**Strategic analysis document** evaluating corpus resources for narrative gravity research:
- **Relevance Rankings**: Star ratings for each corpus (⭐⭐⭐⭐⭐ = highest)
- **Research Applications**: Specific use cases for narrative gravity studies
- **Collaboration Opportunities**: Potential partnerships and data sharing
- **Research Agenda**: Immediate, medium-term, and long-term project roadmap

**Usage**: Strategic planning and grant proposal development
**Format**: Markdown with detailed analysis and recommendations

## Quick Reference: Most Relevant Resources

### 🏆 **Top Priority Corpora**

1. **CORPS** (⭐⭐⭐⭐⭐) - Political speeches with audience reactions
   - Perfect for validating narrative gravity through audience response
   - Contact: FBK HLT-NLP team

2. **HKBU Corpus** (⭐⭐⭐⭐) - Multi-language political speeches
   - Ideal for cross-cultural framework validation
   - Access: [digital.lib.hkbu.edu.hk/corpus](https://digital.lib.hkbu.edu.hk/corpus)

3. **German Political Corpus** (⭐⭐⭐⭐) - 11M words, linguistically processed
   - Large-scale analysis and non-Anglo validation
   - Access: [Sketch Engine](https://sketchengine.eu/german-political-speeches-corpus)

### 📖 **Essential Methodology Papers**

- **Partington (2012)**: "Corpus Analysis of Political Language" - Foundation methods
- **Guerini et al. (2013)**: CORPS methodology - Audience reaction annotation
- **Climate Change Study**: Keyword analysis and semantic tagging techniques

## Research Integration Strategy

### **Immediate Actions** (Next 3 months)
1. Contact CORPS team for audience reaction correlation study
2. Access HKBU corpus for cross-cultural pilot analysis
3. Download German corpus sample for framework testing

### **Citation Strategy**
- Use `political_corpora_resources.bib` for formal academic citations
- Reference methodology papers to position narrative gravity within corpus linguistics
- Emphasize complementary value rather than replacement of existing approaches

### **Collaboration Opportunities**
- **Technical**: Share intelligent corpus ingestion methods
- **Data**: Contribute narrative gravity annotations to existing corpora
- **Research**: Joint studies on audience reaction prediction

## Usage Instructions

### **For LaTeX Documents**
```latex
\bibliography{paper/bibliography/political_corpora_resources}
\cite{guerini_corps_2013}  % CORPS methodology
\cite{hkbu_political_speeches_corpus}  % Cross-cultural validation
```

### **For Grant Proposals**
- Reference strategic analysis for research agenda and collaboration plans
- Cite established corpus resources to demonstrate field integration
- Highlight technical innovations in corpus management

### **For Methodology Sections**
- Position narrative gravity within established corpus linguistics tradition
- Reference Partington (2012) for methodological foundation
- Cite specific corpora used for validation studies

## Bibliography Workflow for Methodology Paper

### 🔍 **Reference Verification Process**
1. **Search Google Scholar** for complete bibliographic information
2. **Check CrossRef/DOI** for accurate metadata  
3. **Verify university access** to ensure full-text availability
4. **Review abstract** to confirm relevance to methodology arguments
5. **Create complete BibTeX entry** with DOI, page numbers, etc.
6. **Remove verification status** once confirmed

### ⚡ **Quick Verification Commands**
For efficient reference collection, use these search patterns:
```bash
# High priority searches
"Grimmer Stewart text as data computational text analysis"
"Haidt moral foundations theory psychology"  
"Entman framing toward clarification fractured paradigm"
"Hopkins King automated nonparametric content analysis"
```

### 📝 **BibTeX Quality Standards**
- Include DOI when available: `doi = {10.1000/example}`
- Add page numbers for articles: `pages = {123--145}`
- Use standard journal abbreviations
- Include URL for web resources
- Add volume/number for journal articles

### 🎯 **Current Priority Tasks**
1. **THIS WEEK**: Verify 5 HIGH priority references
2. **NEXT WEEK**: Complete MFT/Framing/Cultural Theory core papers
3. **MONTH 1**: Full bibliography verification complete
4. **ONGOING**: Add new references as paper develops

## Future Additions

This bibliography will be updated with:
- **Additional corpus discoveries** from literature review
- **Collaboration correspondence** and partnership agreements  
- **Publication citations** as papers are accepted and published
- **Technical documentation** for corpus integration methods
- **Methodology paper references** as verification progresses
- **Framework-specific literature** for detailed implementations

---

*Last updated: June 2025*
*Source: Web search of political corpus resources + methodology paper drafting*
*Next review: After methodology paper bibliography verification* 