# Democratic Discourse Corpus

Four paradigmatic examples of American political communication spanning institutional and populist approaches to democratic discourse. Selected to represent key temporal moments and rhetorical styles in contemporary American democracy.

The corpus includes concession speeches, floor speeches, and policy statements that demonstrate different approaches to democratic engagement and public persuasion across a 17-year temporal span (2008-2025).

## Document Overview

-   **McCain 2008**: Institutional democratic discourse emphasizing unity and norms
-   **King 2017**: Conservative populist discourse with nationalist themes
-   **Sanders 2025**: Progressive populist rhetoric with economic justice themes
-   **AOC 2025**: Progressive populist discourse with systemic critique

---

## Document Manifest

```yaml
name: "Democratic Discourse Corpus"
version: "8.0"
spec_version: "8.0"
total_documents: 4
date_range: "2008-2025"

documents:
  - filename: "john_mccain_2008_concession.txt"
    document_id: "mccain_2008_concession"
    metadata:
      speaker: "John McCain"
      year: 2008
      party: "Republican"
      style: "institutional"
  - filename: "steve_king_2017_house_floor.txt"
    document_id: "king_2017_house_floor"
    metadata:
      speaker: "Steve King"
      year: 2017
      party: "Republican"
      style: "populist_conservative"
  - filename: "bernie_sanders_2025_fighting_oligarchy.txt"
    document_id: "sanders_2025_oligarchy"
    metadata:
      speaker: "Bernie Sanders"
      year: 2025
      party: "Independent"
      style: "populist_progressive"
  - filename: "alexandria_ocasio_cortez_2025_fighting_oligarchy.txt"
    document_id: "aoc_2025_oligarchy"
    metadata:
      speaker: "Alexandria Ocasio-Cortez"
      year: 2025
      party: "Democratic"
      style: "populist_progressive"
```
