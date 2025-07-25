# Van der Veen 2019 Replication - Micro Experiment

## Overview

**Micro-scale replication** of Van der Veen 2019 populist language classification using **PDAF v1.3 Tension Enhanced** framework. This experiment tests whether enhanced populist analysis can replicate academic findings while revealing strategic patterns invisible to original methodology.

## Original Study

**Paper**: Van der Veen 2019 - "Classifying populist language in American presidential politics"  
**Source**: `../vanderveen/paper_source_materials/Classifying_populist_language_in_American_presiden.rtf`  
**Focus**: Computational classification of populist language in 2016 presidential candidate speeches

## Methodological Enhancement

**Original Method**: Van der Veen classification approach  
**Enhanced Method**: PDAF v1.3 Tension Enhanced with:
- **Strategic tension quantification** (Democratic-Authoritarian, Internal-External, Crisis-Elite)
- **Populist Strategic Contradiction Index (PSCI)** measurement
- **Cross-ideological coherence analysis** across Republican/Democratic populist patterns
- **Salience-weighted analysis** for strategic priority identification

## Balanced Micro Corpus (7 documents)

### Republican Assets (3)
1. **`us.2016.Trump.Announcement.6-16.docx`** - Trump announcement speech (key populist moment)
2. **`us.2016.Trump.7-21.docx`** - Trump mid-campaign speech (RNC period)
3. **`us.2016.Cruz.Announcement.3-23.docx`** - Cruz announcement (alternative Republican populist variant)

### Democratic Assets (2)  
4. **`us.2016.Sanders.Announcement.5-26.docx`** - Sanders announcement (key left-populist moment)
5. **`us.2016.Sanders.3-15.docx`** - Sanders mid-campaign speech

### Institutional Comparison (2)
6. **`us.2016.RepublicanPartyPlatform.pdf`** - Official Republican institutional language
7. **`us.2016.DemocraticPartyPlatform.pdf`** - Official Democratic institutional language

## Research Questions

### Primary Replication Question
**Can PDAF v1.3 tension-enhanced analysis replicate Van der Veen 2019 populist classification findings?**

### Methodological Extension Questions
1. **What strategic tension patterns emerge in 2016 populist discourse?**
2. **How do Republican vs Democratic populist strategies differ in coherence?** 
3. **Do candidate speeches vs party platforms show different populist strategic patterns?**
4. **What populist insights are revealed through tension analysis unavailable to original method?**

## Expected Findings

### Replication Expectations
- **Trump speeches**: High populist intensity with strategic tensions (Democratic-Authoritarian conflicts)
- **Sanders speeches**: Moderate-to-high populist intensity with different strategic patterns  
- **Cruz speech**: Moderate populist intensity with ideological variant patterns
- **Party platforms**: Lower populist intensity with institutional language patterns

### Extension Expectations  
- **Strategic tension quantification** revealing populist messaging coherence differences
- **Cross-candidate comparison** of populist strategic architecture
- **Enhanced understanding** of 2016 populist communication patterns

## Execution

### Framework
**File**: `framework.md` (PDAF v1.3 Tension Enhanced)

### Experiment Specification  
**File**: `experiment.md` (Complete workflow and success criteria)

### Run Command
```bash
# From project root
python3 discernus_cli.py execute projects/vanderveen_micro
```

## Academic Value

### Replication Contribution
- **Methodological validation** of computational populist analysis
- **Cross-framework comparison** between approaches
- **Reproducible analysis** of 2016 populist discourse

### Extension Contribution
- **Strategic tension mathematics** applied to populist studies
- **Cross-ideological coherence analysis** using quantitative methods
- **Enhanced populist communication theory** through computational analysis

---

**Status**: Ready for execution  
**Framework**: PDAF v1.3 Tension Enhanced  
**Corpus**: 7 balanced documents (3 Republican, 2 Democratic, 2 institutional)  
**Expected Duration**: 30-45 minutes for complete analysis 