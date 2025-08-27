# Emotional Climate Factorial Analysis Corpus

This corpus contains political speeches designed for a 2×3 factorial analysis examining emotional climate patterns across ideology and era factors. The corpus spans 60 years of American political discourse (1963-2025) and includes speeches from prominent political figures representing conservative and progressive ideologies across three distinct political eras.

## Corpus Design

The corpus employs a balanced factorial design with:
- **2 Ideological Groups**: Conservative vs Progressive
- **3 Political Eras**: Civil Rights (1963), Institutional (2008-2020), Populist (2017-2025)
- **Total Documents**: 8 speeches (4 Conservative, 4 Progressive)

## Document Overview

### Civil Rights Era (1963)
- **Progressive**: John Lewis - March on Washington speech

### Institutional Era (2008-2020)
- **Conservative**: John McCain - 2008 Presidential concession speech
- **Conservative**: Mitt Romney - 2020 Senate floor speech on impeachment vote
- **Progressive**: Cory Booker - 2018 Senate floor speech supporting First Step Act

### Populist Era (2017-2025)
- **Progressive**: Bernie Sanders - 2025 Senate floor speech criticizing oligarchic power
- **Progressive**: Alexandria Ocasio-Cortez - 2025 House floor speech on oligarchy
- **Conservative**: JD Vance - 2022 National Conservatism Conference keynote
- **Conservative**: Steve King - 2017 House floor speech on immigration

## Factorial Balance

This design enables sophisticated emotional climate interaction analysis:
- **Ideology × Era Interaction**: Tests whether emotional climate patterns vary systematically across the interaction of ideological affiliation and historical era
- **Main Effects**: Tests for ideological and temporal effects on emotional climate dimensions
- **Statistical Power**: Balanced design maximizes statistical power for detecting interaction effects

## Emotional Climate Dimensions

The corpus is designed to capture variation across six emotional climate dimensions:
1. **Fear/Hope Axis**: Crisis/threat vs. optimism/aspiration
2. **Enmity/Amity Axis**: Opposition/conflict vs. cooperation/unity
3. **Envy/Compersion Axis**: Resentment/comparison vs. shared joy/satisfaction

## Source Attribution

All speeches are sourced from public political discourse including:
- Congressional floor speeches
- Presidential campaign addresses
- Political conference keynotes
- Civil rights movement speeches

---

## Document Manifest

```yaml
name: "Emotional Climate Factorial Analysis Corpus"
version: "10.0"
total_documents: 8
date_range: "1963-2025"
factorial_design: "2×3 (Ideology × Era)"

documents:
  - filename: "john_lewis_1963_march_on_washington.txt"
    speaker: "John Lewis"
    year: 1963
    ideology: "progressive"
    era: "civil_rights"
    speech_type: "civil_rights_address"
    
  - filename: "john_mccain_2008_concession.txt"
    speaker: "John McCain"
    year: 2008
    ideology: "conservative"
    era: "institutional"
    speech_type: "concession_speech"
    
  - filename: "mitt_romney_2020_impeachment.txt"
    speaker: "Mitt Romney"
    year: 2020
    ideology: "conservative"
    era: "institutional"
    speech_type: "senate_floor_speech"
    
  - filename: "cory_booker_2018_first_step_act.txt"
    speaker: "Cory Booker"
    year: 2018
    ideology: "progressive"
    era: "institutional"
    speech_type: "senate_floor_speech"
    
  - filename: "bernie_sanders_2025_fighting_oligarchy.txt"
    speaker: "Bernie Sanders"
    year: 2025
    ideology: "progressive"
    era: "populist"
    speech_type: "senate_floor_speech"
    
  - filename: "alexandria_ocasio_cortez_2025_fighting_oligarchy.txt"
    speaker: "Alexandria Ocasio-Cortez"
    year: 2025
    ideology: "progressive"
    era: "populist"
    speech_type: "house_floor_speech"
    
  - filename: "jd_vance_2022_natcon_conference.txt"
    speaker: "JD Vance"
    year: 2022
    ideology: "conservative"
    era: "populist"
    speech_type: "conference_keynote"
    
  - filename: "steve_king_2017_house_floor.txt"
    speaker: "Steve King"
    year: 2017
    ideology: "conservative"
    era: "populist"
    speech_type: "house_floor_speech"
```

