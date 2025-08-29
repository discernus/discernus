# Populist Discourse Analysis Corpus: Presidential Speeches 2017-2025

This corpus contains presidential speeches designed for temporal analysis of populist discourse patterns using the Populist Discourse Analysis Framework (PDAF) v10.0. The corpus spans 8 years of presidential rhetoric (2017-2025) and includes speeches representing different contexts and time periods, enabling comprehensive analysis of populist discourse evolution and contextual variation.

## Corpus Design

The corpus employs a temporal design with:
- **6 Presidential Speeches**: Spanning 2017-2025
- **3 Speech Types**: Inaugural Address, State of the Union, Joint Session Address
- **3 Time Periods**: Early (2017), Mid (2018-2020), Recent (2025)
- **Total Documents**: 6 speeches enabling temporal pattern analysis

## Document Overview

### Early Presidential Period (2017)
- **Inaugural Address (2017-01-20)**: Foundational presidential rhetoric establishing populist themes
- **Joint Session Address (2017-02-28)**: Early policy vision and legislative agenda

### Mid-Presidential Period (2018-2020)
- **State of the Union 2018 (2018-01-30)**: Annual presidential communication and policy priorities
- **State of the Union 2019 (2019-02-05)**: Annual presidential communication and policy priorities
- **State of the Union 2020 (2020-02-04)**: Annual presidential communication and policy priorities

### Recent Presidential Period (2025)
- **State of the Union 2025 (2025-03-04)**: Recent presidential communication and current priorities

## Temporal Balance

This design enables sophisticated temporal analysis:
- **Early vs. Mid vs. Recent**: Tests for systematic changes in populist discourse over time
- **Speech Type Comparison**: Tests for differences between inaugural, SOTU, and joint session contexts
- **Evolutionary Patterns**: Captures potential changes in populist rhetoric across presidential tenure

## Populist Discourse Dimensions

The corpus is designed to capture variation across nine populist anchor dimensions:

### Core Dimensions
1. **Manichaean People-Elite Framing**: Clear distinction between "the people" and "the elite"
2. **Anti-Establishment Rhetoric**: Criticism of political and institutional establishment

### Mechanism Dimensions
3. **Crisis Narratives**: Framing of urgent threats requiring immediate action
4. **Mobilization Appeals**: Calls for popular action and engagement
5. **Simplification**: Reduction of complex issues to simple dichotomies

### Boundary Dimensions
6. **Exclusionary Populism**: Defining who belongs to "the people"
7. **Elite Conspiracy Theories**: Systemic corruption and elite manipulation
8. **Nationalist Appeals**: Emphasis on national identity and sovereignty
9. **Anti-Intellectualism**: Distrust of expert knowledge and institutions

## Strategic Tension Analysis

The corpus enables analysis of the Populist Strategic Contradiction Index (PSCI):
- **Coherence Measurement**: How well populist dimensions align strategically
- **Temporal Evolution**: Whether strategic coherence changes over time
- **Context Variation**: Whether different speech types show different coherence patterns

## Source Attribution

All speeches are sourced from official presidential communications including:
- Presidential inaugural addresses
- Annual State of the Union addresses
- Joint session addresses to Congress
- Official White House transcripts

---

## Document Manifest

```yaml
name: "Populist Discourse Analysis Corpus: Presidential Speeches 2017-2025"
version: "10.0"
total_documents: 6
date_range: "2017-2025"
speech_types: ["inaugural", "state_of_union", "joint_session"]

documents:
  - filename: "Trump_Inaugural_2017.txt"
    speaker: "Donald J. Trump"
    year: 2017
    month: 1
    day: 20
    speech_type: "inaugural_address"
    period: "early"
    context: "foundational_presidential_rhetoric"
    
  - filename: "trump_sotu_2017.txt"
    speaker: "Donald J. Trump"
    year: 2017
    month: 2
    day: 28
    speech_type: "joint_session_address"
    period: "early"
    context: "early_policy_vision"
    
  - filename: "Trump_SOTU_2018.txt"
    speaker: "Donald J. Trump"
    year: 2018
    month: 1
    day: 30
    speech_type: "state_of_union"
    period: "mid"
    context: "annual_presidential_communication"
    
  - filename: "Trump_SOTU_2019.txt"
    speaker: "Donald J. Trump"
    year: 2019
    month: 2
    day: 5
    speech_type: "state_of_union"
    period: "mid"
    context: "annual_presidential_communication"
    
  - filename: "Trump_SOTU_2020.txt"
    speaker: "Donald J. Trump"
    year: 2020
    month: 2
    day: 4
    speech_type: "state_of_union"
    period: "mid"
    context: "annual_presidential_communication"
    
  - filename: "Trump_SOTU_2025.txt"
    speaker: "Donald J. Trump"
    year: 2025
    month: 3
    day: 4
    speech_type: "state_of_union"
    period: "recent"
    context: "recent_presidential_communication"
```

