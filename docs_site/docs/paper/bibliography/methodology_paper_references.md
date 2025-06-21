# Methodology Paper Bibliography Tracker

**File**: `discernus_methodology_paper_v1.md`  
**Created**: June 2025  
**Status**: Active collection phase

## Reference Collection Strategy

### 📋 **Citations Added to Draft**

| Citation | Status | Priority | Notes |
|----------|--------|----------|-------|
| Grimmer & Stewart, 2013 | 🟡 VERIFY | HIGH | Classic computational text analysis survey |
| Benoit et al., 2018 | 🟡 VERIFY | HIGH | Quanteda and text analysis methods |
| Denny & Spirling, 2018 | 🟡 VERIFY | HIGH | Text as data methodology |
| Rodriguez et al., 2021 | 🔴 CHECK | LOW | May be placeholder - verify existence |
| King, 1995 | 🟡 VERIFY | LOW | Replication in political science (superseded by newer refs) |
| Freese & Peterson, 2017 | 🟡 VERIFY | MED | Replication in social science |
| **Boyd & Holtzman, 2024** | 🔴 NOT FOUND | **HIGH** | **Reproducibility crisis - NEEDS VERIFICATION** |
| **Denny et al., 2023** | 🔴 NOT FOUND | **HIGH** | **Recent reproducibility - NEEDS VERIFICATION** |
| **van Atteveldt et al., 2023** | 🔴 NOT FOUND | **HIGH** | **Comp comm science review - NEEDS VERIFICATION** |
| **Chase, 2023** | 🟢 VERIFIED | **MED** | **Harrison Chase/LangChain - extensively documented** |
| **Liu et al., 2023** | 🟡 VERIFY | **MED** | **LlamaIndex - current LLM data integration** |
| Hopkins & King, 2010 | 🟡 VERIFY | HIGH | Validation methods |
| Mohammad & Turney, 2013 | 🟡 VERIFY | MED | Sentiment analysis/NLP methods |
| Sagi & Dehghani, 2014 | 🟡 VERIFY | HIGH | Moral foundations computational work |
| Bird et al., 2009 | 🟢 KNOWN | LOW | NLTK Natural Language Processing book |
| Manning et al., 2014 | 🟡 VERIFY | LOW | Stanford NLP group work |
| Lucas et al., 2015 | 🟡 VERIFY | HIGH | Computer-assisted text analysis |
| Monroe et al., 2008 | 🟡 VERIFY | MED | Topic models/political science |
| Laver et al., 2003 | 🟡 VERIFY | MED | Automated content analysis |
| Haidt et al., 2009 | 🟡 VERIFY | HIGH | Original MFT paper |
| Graham et al., 2013 | 🟡 VERIFY | HIGH | MFT empirical validation |
| Entman, 1993 | 🟡 VERIFY | HIGH | Original framing theory paper |
| Lakoff, 2002 | 🟡 VERIFY | HIGH | Cognitive linguistics/political framing |
| Douglas & Wildavsky, 1982 | 🟡 VERIFY | HIGH | Original cultural theory |
| Kahan et al., 2012 | 🟡 VERIFY | HIGH | Cultural cognition research |

### 🎯 **Priority Collection Order**

#### **HIGH Priority** (Core theoretical/methodological)
1. **Boyd & Holtzman, 2024** - Reproducibility crisis in computational social science **[NEW - CRITICAL]**
2. **Denny et al., 2023** - Recent reproducibility in computational social science **[NEW - CRITICAL]**  
3. **van Atteveldt et al., 2023** - Computational communication science review **[NEW - CRITICAL]**
4. **Grimmer & Stewart, 2013** - Foundational text analysis survey
5. **Haidt et al., 2009** - Original Moral Foundations Theory  
6. **Graham et al., 2013** - MFT empirical validation
7. **Entman, 1993** - Original framing theory
8. **Lakoff, 2002** - Political framing/cognitive linguistics
9. **Douglas & Wildavsky, 1982** - Original cultural theory
10. **Kahan et al., 2012** - Cultural cognition measurement
11. **Hopkins & King, 2010** - Validation methodology
12. **Lucas et al., 2015** - Computer-assisted text analysis
13. **Sagi & Dehghani, 2014** - MFT computational implementation

#### **MEDIUM Priority** (Supporting methodology)
- King, 1995 - Replication standards
- Freese & Peterson, 2017 - Reproducibility
- Monroe et al., 2008 - Topic modeling
- Laver et al., 2003 - Automated content analysis
- Mohammad & Turney, 2013 - NLP methods

#### **MEDIUM Priority** (Current LLM Infrastructure) **[NEW CATEGORY]**
- **Chase, 2023** - LangChain orchestration framework  
- **Liu et al., 2023** - LlamaIndex data integration
- OpenAI, 2023 - OpenAI Evals framework
- DeepEval, 2024 - LLM evaluation tools
- Arize, 2024 - Phoenix LLM observability

#### **LOW Priority** (Technical/well-known)
- Bird et al., 2009 - NLTK book (widely available)
- Manning et al., 2014 - Stanford NLP (multiple papers)
- Rodriguez et al., 2021 - Verify if real citation
- King, 1995 - Replication standards (superseded by newer references)

## Collection Tasks

### ✅ **Immediate Actions** (This week)
- [ ] Search Google Scholar for HIGH priority references
- [ ] Check university library access for paywalled articles  
- [ ] Verify questionable citations (Rodriguez et al., 2021)
- [ ] Create BibTeX entries for confirmed references

### 📚 **Search Strategies**

#### **For Core Theory Papers**
- **MFT**: Search "Haidt moral foundations theory" + year
- **Framing**: Search "Entman framing theory 1993"  
- **Cultural Theory**: Search "Douglas Wildavsky cultural theory risk"

#### **For Methodology Papers**
- **Text Analysis**: Search "Grimmer Stewart computational text analysis"
- **Validation**: Search "Hopkins King validation computational"

#### **For Recent Work** 
- Search author names in Google Scholar
- Check recent citations of core papers
- Look for review articles in computational social science

### 🔍 **Verification Process**

1. **Google Scholar search** - Verify title, authors, year
2. **CrossRef/DOI lookup** - Get complete bibliographic info
3. **University access check** - Ensure we can access full text
4. **Abstract review** - Confirm relevance to our arguments
5. **BibTeX creation** - Standard academic format

### 📝 **BibTeX File Strategy**

Create separate `.bib` files:
- `methodology_core_references.bib` - Essential citations for paper
- `framework_specific_references.bib` - MFT, Framing, Cultural Theory literature  
- `computational_methods_references.bib` - Technical/methodological papers

## Integration with Existing Bibliography

### **Current Files**
- `political_corpora_resources.bib` - Corpus and data resources
- `corpus_analysis_for_narrative_gravity.md` - Strategic analysis

### **New Organization**
```
docs/paper/bibliography/
├── political_corpora_resources.bib      # Existing corpus resources
├── methodology_core_references.bib      # New: Core methodology citations  
├── framework_specific_references.bib    # New: Theoretical framework papers
├── computational_methods_references.bib # New: Technical/CS methods
└── README.md                           # Updated to include all files
```

## Quality Control

### **Before Adding to .bib File**
- [ ] Verify complete bibliographic information
- [ ] Check for DOI/URL availability  
- [ ] Confirm spelling of authors/titles
- [ ] Standardize journal name formatting
- [ ] Add abstract/keywords if available

### **Citation Style Standards**
- Use consistent BibTeX entry types
- Include DOI when available
- Add URLs for web resources
- Include page numbers for journal articles
- Standard abbreviations for journal names

## Important Discovery: Literature Review Gap Analysis

### 🔍 **Found Existing Research** 
The file `docs/paper/research/literature_review_discernus_gap.md` contains a **more current and targeted literature review** that positions Discernus specifically within the LLM-era computational social science landscape.

### 🎯 **Key Insights from Existing Literature Review**
1. **Better Positioning**: Focuses on LLM/human evaluation gap rather than general text analysis
2. **More Current References**: 2023-2024 papers on reproducibility crisis  
3. **Specific Technical Context**: LangChain, LlamaIndex, LLMOps tools
4. **Stronger Gap Argument**: "No platform exists that..." - very compelling

### 📈 **Impact on Methodology Paper**
- **UPGRADE**: Replace older reproducibility references (King 1995) with current ones (Boyd & Holtzman 2024, Denny et al. 2023)
- **STRENGTHEN**: Add "current tools and limitations" section using LLM infrastructure references
- **REFINE**: Position methodology contribution more specifically as filling LLM-era gap

### 🔄 **Next Action Items**
1. **PRIORITY SHIFT**: Focus first on NEW HIGH priority references from literature review
2. **METHODOLOGY PAPER UPDATE**: Incorporate LLM-era positioning and current references
3. **VERIFY**: New references are more critical than some original ones

## 🔍 **VERIFICATION RESULTS** (Updated)

### **Search Results from Web Verification:**

#### **✅ VERIFIED RECENT REFERENCES - Legitimate Alternatives Found**
- **Breznau et al., 2025** - "The reliability of replications: a study in computational reproductions" - **VERIFIED: Royal Society Open Science** ✅ **ADDED TO BIB**
- **Mattsson, 2024** - "Computational social science with confidence" - **VERIFIED: EPJ Data Science** ✅ **ADDED TO BIB**
- **Xu et al., 2024** - "AI for social science and social science of AI: A Survey" - **VERIFIED: Information Processing & Management** ✅ **ADDED TO BIB**

#### **✅ NEW VERIFIED REFERENCES FROM CHATGPT TESTS (2025-01-23)**
- **Schoch et al., 2024** - "Computational reproducibility in computational social science" - **VERIFIED: EPJ Data Science** ✅ **ADDED TO BIB**
- **Bleier, 2025** - "What is Computational Reproducibility?" - **VERIFIED: GESIS Guide** ✅ **ADDED TO BIB**  
- **Marcoci et al., 2025** - "Predicting the replicability of social and behavioural science claims in COVID-19 preprints" - **VERIFIED: Nature Human Behaviour** ✅ **ADDED TO BIB**

#### **✅ VERIFIED - Extensively Documented**
- **Chase, 2023** - Harrison Chase/LangChain orchestration framework (multiple sources, interviews, documentation)

### **✅ SUCCESSFUL VERIFICATION - Real Recent References Found:**

**BREAKTHROUGH**: Found excellent legitimate alternatives to replace hallucinated citations:

1. **Breznau et al., 2025** - "The reliability of replications: a study in computational reproductions"
   - **Journal**: Royal Society Open Science  
   - **Significance**: Major empirical study with 85 research teams testing computational reproducibility
   - **Perfect fit**: Directly addresses reproducibility challenges in computational methods

2. **Mattsson, 2024** - "Computational social science with confidence"  
   - **Journal**: EPJ Data Science
   - **Significance**: Commentary on methodological validation and research infrastructure needs
   - **Relevance**: Discusses maturation of CSS field and institutional requirements

3. **Xu et al., 2024** - "AI for social science and social science of AI: A Survey"
   - **Journal**: Information Processing and Management  
   - **Significance**: Comprehensive survey of AI-social science intersection
   - **Value**: Current perspective on LLM applications in social science

### **📚 BIBLIOGRAPHY STATUS UPDATE:**
- ✅ **Replaced hallucinations**: 3 fake citations → 3 verified recent papers
- ✅ **Enhanced quality**: Found higher-quality, more recent references than original hallucinations
- ✅ **Verified authenticity**: All citations confirmed through web search and journal verification

---

**Next Steps**: 
1. **IMMEDIATE**: Mine references from key PDFs (Bleier 2025, Schoch et al. 2024)
2. **CHECK**: Conference proceedings, preprints, working papers for missing citations
3. **FALLBACK**: Use alternative verified recent references on reproducibility in computational social science
4. Create comprehensive methodology bibliography with verified references only

---

## 📚 **REFERENCE MINING FROM KEY PAPERS** 

### **✅ Available PDFs for Reference Extraction**

#### **1. Bleier (2025) - "What is Computational Reproducibility?" GESIS Guide**
- **File**: `tmp/02_Bleier_computational_reproducibility.pdf`
- **Status**: ✅ **AVAILABLE FOR MINING**
- **Value**: Practical guide with extensive references to reproducibility tools and methods
- **Expected**: Recent papers on reproducibility protocols, computational infrastructure, validation tools

#### **2. Schoch et al. (2024/2023) - "Computational Reproducibility in Computational Social Science"** 
- **File**: `tmp/2307.01918v4.pdf` (arXiv version)
- **Status**: ✅ **AVAILABLE FOR MINING**  
- **Note**: Same paper as already in bibliography, but PDF allows reference extraction
- **Value**: Comprehensive survey with detailed bibliography on computational social science
- **Expected**: Key papers on reproducibility frameworks, external dependencies, tier systems

### **🎯 Mining Strategy**

#### **Priority 1: Recent Reproducibility References**
- Look for 2020-2025 papers on computational reproducibility
- Focus on social science/computational social science specific papers
- Extract tool and framework references (Docker, containers, package management)

#### **Priority 2: Methodological Infrastructure Papers**
- Papers on research infrastructure for computational work
- References to validation frameworks and quality assurance
- Survey papers on computational methods in social science

#### **Priority 3: Tool and Platform References**
- Technical papers on reproducibility tools mentioned in these guides
- Platform papers that support computational reproducibility
- Workflow management and orchestration frameworks

### **🔍 Action Items**

**Immediate:**
1. ✅ **Extract reference lists** from both PDFs ✅ **COMPLETED**
2. ✅ **Cross-reference** with existing bibliography to avoid duplicates ✅ **COMPLETED**
3. ✅ **Prioritize** new references not already in our collection ✅ **COMPLETED**
4. ✅ **Verify** high-priority references through web search ✅ **COMPLETED**

**Follow-up:**
- ✅ **Add verified references to `methodology_core_references.bib`** ✅ **COMPLETED - 6 NEW PAPERS ADDED**
- ✅ **Update tracking status for newly added papers** ✅ **COMPLETED**
- Identify any additional papers that need similar reference mining

---

## 🎯 **REFERENCE MINING RESULTS - SUCCESS!**

### **✅ Added 6 High-Value References from PDF Mining:**

#### **From Bleier (2025) GESIS Guide:**
1. **Camerer et al., 2018** - "Evaluating the replicability of social science experiments in Nature and Science" 
   - **Nature Human Behaviour** - Major replication study with 62% success rate
2. **Hardwicke et al., 2020** - "An empirical assessment of transparency and reproducibility in social sciences"
   - **Royal Society Open Science** - Systematic documentation of low sharing rates
3. **Chan et al., 2024** - "What makes computational communication science (ir)reproducible?"
   - **Computational Communication Research** - Recent barriers study
4. **Breuer & Haim, 2024** - "Are we replicating yet? Reproduction and replication in communication research"
   - **Media and Communication** - Communication field assessment

#### **From Schoch et al. (2023/2024) Paper:**
5. **Nosek et al., 2022** - "Replicability, robustness, and reproducibility in psychological science"
   - **Annual Review of Psychology** - Comprehensive conceptual review
6. **Munafò et al., 2017** - "A manifesto for reproducible science"
   - **Nature Human Behaviour** - Influential call to action

### **📊 Bibliography Enhancement Summary:**
- **Started with**: 9 verified papers
- **Added from mining**: 6 high-value papers  
- **Total now**: **15 verified, high-quality recent references**
- **Coverage**: Psychology, communication, social science, computational methods
- **Time span**: 2017-2025 (excellent recency)

### **💎 Value Added:**
- **Foundational studies**: Camerer, Munafò landmark papers
- **Recent assessments**: Chan, Breuer & Haim 2024 studies  
- **Systematic reviews**: Nosek, Hardwicke comprehensive analyses
- **Cross-disciplinary**: Psychology, communication, social science coverage 