# CAF Civic Character Political Speeches Corpus

A diverse collection of eight political speeches spanning different eras, political orientations, and rhetorical styles, selected to test the Civic Analysis Framework's ability to detect meaningful differences in character patterns between individual speakers.

The corpus includes speeches from across the political spectrum, representing different approaches to democratic engagement, public persuasion, and civic discourse. These speeches demonstrate varying levels of civic virtue and vice, making them ideal for testing the CAF's dimensional analysis capabilities.

## Document Overview

- **John Lewis 1963**: Civil rights era speech emphasizing dignity and justice
- **John McCain 2008**: Institutional democratic discourse emphasizing unity and norms
- **Steve King 2017**: Conservative populist discourse with nationalist themes
- **Cory Booker 2018**: Progressive institutional discourse on criminal justice reform
- **Mitt Romney 2020**: Institutional discourse on constitutional principles
- **JD Vance 2022**: Conservative populist discourse with nationalist themes
- **Bernie Sanders 2025**: Progressive populist rhetoric with economic justice themes
- **Alexandria Ocasio-Cortez 2025**: Progressive populist discourse with systemic critique

---

## Document Manifest

```yaml
name: "CAF Civic Character Political Speeches Corpus"
version: "10.0"
total_documents: 8
date_range: "1963-2025"
description: "Diverse political speeches for testing CAF dimensional analysis"

groupings:
  speaker_type:
    institutional:
      - "institutional"
      - "institutional_progressive"
    populist:
      - "populist_conservative"
      - "populist_progressive"
    civil_rights:
      - "civil_rights"

documents:
  - document_id: "john_lewis_1963_march"
    filename: "john_lewis_1963_march_on_washington_ab348df3.txt"
    speaker: "John Lewis"
    year: 1963
    party: "Democratic"
    style: "civil_rights"
    type: "protest_speech"
    context: "March on Washington for Jobs and Freedom"
  
  - document_id: "john_mccain_2008_concession"
    filename: "john_mccain_2008_concession_ff9b26f2.txt"
    speaker: "John McCain"
    year: 2008
    party: "Republican"
    style: "institutional"
    type: "concession_speech"
    context: "2008 presidential election concession"
  
  - document_id: "steve_king_2017_immigration"
    filename: "steve_king_2017_house_floor_738780d9.txt"
    speaker: "Steve King"
    year: 2017
    party: "Republican"
    style: "populist_conservative"
    type: "floor_speech"
    context: "House floor speech on immigration"
  
  - document_id: "cory_booker_2018_first_step"
    filename: "cory_booker_2018_first_step_act_0c32812a.txt"
    speaker: "Cory Booker"
    year: 2018
    party: "Democratic"
    style: "institutional_progressive"
    type: "policy_speech"
    context: "First Step Act criminal justice reform"
  
  - document_id: "mitt_romney_2020_impeachment"
    filename: "mitt_romney_2020_impeachment_9ebec73f.txt"
    speaker: "Mitt Romney"
    year: 2020
    party: "Republican"
    style: "institutional"
    type: "impeachment_speech"
    context: "Trump impeachment trial speech"
  
  - document_id: "jd_vance_2022_natcon"
    filename: "jd_vance_2022_natcon_conference_516a3c9c.txt"
    speaker: "JD Vance"
    year: 2022
    party: "Republican"
    style: "populist_conservative"
    type: "conference_speech"
    context: "National Conservatism Conference"
  
  - document_id: "bernie_sanders_2025_oligarchy"
    filename: "bernie_sanders_2025_fighting_oligarchy_261b893a.txt"
    speaker: "Bernie Sanders"
    year: 2025
    party: "Independent"
    style: "populist_progressive"
    type: "policy_statement"
    context: "Economic justice and oligarchy critique"
  
  - document_id: "aoc_2025_oligarchy"
    filename: "alexandria_ocasio_cortez_2025_fighting_oligarchy_1121e4ae.txt"
    speaker: "Alexandria Ocasio-Cortez"
    year: 2025
    party: "Democratic"
    style: "populist_progressive"
    type: "policy_statement"
    context: "Economic justice and oligarchy critique"
```
