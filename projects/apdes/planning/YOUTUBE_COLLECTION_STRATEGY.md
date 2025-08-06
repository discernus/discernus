# APDES YouTube Collection Strategy

## Overview
Systematic video speech collection to fill Era 2.5-4 gaps (2017-2024) using the validated YouTube transcript extractor.

## Collection Priorities

### Era 2.5: Populist Governance Transition (2017-2019)
**Target: 12-15 videos**

#### Trump Rally Circuit (6-8 rallies)
- **Cincinnati Rally** (August 2017) - First post-inaugural populist rally
- **Phoenix Rally** (August 2017) - Charlottesville response and media attacks  
- **Huntington WV Rally** (August 2017) - Economic populism messaging
- **Pensacola Rally** (December 2017) - Moore endorsement and establishment attacks
- **Nashville Rally** (May 2018) - Immigration and wall messaging
- **Duluth Rally** (June 2018) - Trade war justification
- **Tampa Rally** (July 2018) - Media antagonism peak
- **Charleston WV Rally** (August 2018) - Coal populism and energy

#### Major Policy Populist Speeches (4-5 speeches)
- **Immigration Executive Orders** (January 2017) - Early populist implementation
- **Trade War Announcement** (March 2018) - Economic populist justification  
- **UN General Assembly** (September 2018) - America First foreign policy
- **Border Wall Emergency** (February 2019) - Constitutional populism test
- **Syria/Afghanistan Withdrawal** (December 2018/2019) - Anti-elite foreign policy

#### Institutional Conflict Speeches (2-3 speeches)
- **Mueller Investigation Response** (2018) - Deep state populism  
- **Government Shutdown Justification** (December 2018) - Elite obstruction
- **Fire Rosenstein/Sessions** speeches - DOJ populist conflict

### Era 3: Institutional Crisis (2020-2021)  
**Target: 15-18 videos**

#### BLM Crisis Responses (4-5 videos)
- **Trump BLM Response** (May/June 2020) - Law and order populism
- **AOC BLM Address** - Progressive populist response  
- **Biden BLM Speech** - Mainstream Democratic response
- **DeSantis BLM Position** - State-level populist response
- **Pelosi Congressional Response** - Elite institutional response

#### COVID Populist Messaging (4-5 videos)
- **Trump COVID Relief Opposition** - Elite obstruction claims
- **DeSantis Anti-Lockdown** speeches - State populism vs federal health
- **Tucker Carlson COVID** segments - Media populist messaging
- **Bernie Sanders COVID Relief** - Economic populist approach  
- **Trump Vaccine/Therapeutics** - Medical establishment conflicts

#### January 6th Critical Collection (6-8 videos)
- **January 6th Rally Speech** - Pre-Capitol march content ✅ COLLECTED
- **Trump Post-January 6th** response video (January 7th)
- **Pence January 6th Response** - Constitutional vs populist tension
- **McConnell January 6th Floor Speech** - Establishment response
- **AOC January 6th Response** - Progressive institutional defense
- **Biden January 6th Anniversary** speeches (2022-2024)
- **Tucker Carlson January 6th** coverage - Media populist reframing
- **Josh Hawley January 6th** justification - Senatorial populism

### Era 4: Populist Consolidation (2024)
**Target: 12-15 videos**

#### Trump Comeback Campaign (5-6 videos)
- **Trump Campaign Launch** (November 2022) - Comeback narrative
- **New Hampshire Primary** speech (January 2024)
- **Super Tuesday Victory** speech (March 2024)  
- **Trump VP Announcement** speech (July 2024)
- **Republican Convention** acceptance speech (July 2024)
- **Post-Election Victory** speech (November 2024)

#### Harris Emergency Campaign (3-4 videos)
- **Harris Campaign Launch** (July 2024) - Post-Biden emergency pivot
- **Democratic Convention** acceptance speech (August 2024)
- **Harris Debate Performance** key moments (September 2024)
- **Harris Concession Speech** (November 2024) - Democratic reckoning

#### Gubernatorial Populism (3-4 videos)  
- **DeSantis Presidential Launch** (May 2023) - Alternative populist vision
- **Vivek Ramaswamy Campaign** speeches - Young populist approach
- **Glenn Youngkin Education** speeches - Suburban populist messaging  
- **Ron DeSantis Disney/Woke** conflict speeches - Cultural populism

#### Crisis Response Evolution (1-2 videos)
- **Biden Democracy Speech** (September 2022) - Anti-populist institutional defense
- **Trump Legal Response** speeches - Weaponization populism

## Collection Methodology

### Video Identification Process
1. **Search Strategy**: Use combination of official channels, major news networks, verified political accounts
2. **Date Verification**: Cross-reference with historical records and news coverage
3. **Content Validation**: Ensure speeches are complete, not edited clips or commentary
4. **Quality Check**: Verify captions/transcripts are available before extraction

### Extraction Workflow
```bash
# Era 2.5 Collection
python3 scripts/youtube_transcript_extractor.py "RALLY_URL" -o projects/apdes/corpus/era_25_governance/trump_rallies/
python3 scripts/youtube_transcript_extractor.py "POLICY_URL" -o projects/apdes/corpus/era_25_governance/policy_speeches/
python3 scripts/youtube_transcript_extractor.py "CONFLICT_URL" -o projects/apdes/corpus/era_25_governance/institutional_conflict/

# Era 3 Collection  
python3 scripts/youtube_transcript_extractor.py "BLM_URL" -o projects/apdes/corpus/era_3_crisis/blm_responses/
python3 scripts/youtube_transcript_extractor.py "COVID_URL" -o projects/apdes/corpus/era_3_crisis/covid_populism/
python3 scripts/youtube_transcript_extractor.py "JAN6_URL" -o projects/apdes/corpus/era_3_crisis/january_6th/

# Era 4 Collection
python3 scripts/youtube_transcript_extractor.py "TRUMP24_URL" -o projects/apdes/corpus/era_4_consolidation/trump_comeback/
python3 scripts/youtube_transcript_extractor.py "HARRIS24_URL" -o projects/apdes/corpus/era_4_consolidation/harris_campaign/  
python3 scripts/youtube_transcript_extractor.py "GOV_URL" -o projects/apdes/corpus/era_4_consolidation/gubernatorial/
```

### Quality Control Standards
- **Minimum length**: 500 characters (exclude brief clips)
- **Speaker verification**: Confirm primary speaker attribution
- **Date accuracy**: Validate upload date matches event date  
- **Content completeness**: Ensure full speeches, not excerpts
- **Transcript quality**: Prefer manual captions over auto-generated when available

### Success Metrics
- **Coverage completeness**: All major populist speakers and crisis events represented
- **Temporal accuracy**: Events properly sequenced within eras  
- **Ideological balance**: Multiple perspectives on each crisis/event captured
- **Quality threshold**: 90%+ of extractions produce usable research content

## Integration with APDES Corpus

### File Organization
```
projects/apdes/corpus/
├── era_25_governance/          # 2017-2019 Trump governance
│   ├── trump_rallies/         # Rally circuit populist messaging ✅ STARTED
│   ├── policy_speeches/       # Major populist policy announcements  
│   └── institutional_conflict/ # Deep state/DOJ/Mueller conflicts
├── era_3_crisis/              # 2020-2021 institutional crisis
│   ├── blm_responses/         # BLM crisis populist responses
│   ├── covid_populism/        # COVID anti-elite messaging
│   └── january_6th/           # January 6th speeches and responses ✅ STARTED
└── era_4_consolidation/       # 2024 populist consolidation  
    ├── trump_comeback/        # Trump 2024 campaign speeches
    ├── harris_campaign/       # Harris emergency campaign
    └── gubernatorial/         # State-level populist messaging
```

### Metadata Enhancement
Each extracted video will include:
- **APDES era classification**: Era 2.5, 3, or 4
- **Crisis context tags**: BLM, COVID, January 6th, Election
- **Speaker ideological positioning**: Populist direction and intensity
- **Event significance**: Major vs minor speech classification
- **Cross-reference data**: Relation to other corpus documents

## Research Value

### Analytical Opportunities
1. **Populist Evolution Tracking**: Discourse development across 2017-2024
2. **Crisis Response Patterns**: How populist messaging adapts to institutional crises
3. **Cross-Platform Consistency**: YouTube vs traditional media populist messaging
4. **Audience Engagement Metrics**: View counts and engagement as populist appeal indicators

### Framework Application
All collected videos will be analyzed using:
- **Ideational Populism Detection V4**: Core populist classification
- **Cohesive Flourishing Framework V7**: Democratic health impact
- **Political Discourse Analysis Framework V7**: Rhetorical strategy analysis
- **Core Assessment Framework V7**: Multi-dimensional discourse analysis

## Implementation Timeline

### Phase 1: Era 3 Critical Collection (Week 1-2)
Focus on January 6th and COVID crisis responses - highest research priority

### Phase 2: Era 2.5 Systematic Collection (Week 3-4)  
Trump rally circuit and major policy speeches - populist governance foundation

### Phase 3: Era 4 Campaign Collection (Week 5-6)
2024 election cycle materials - populist consolidation evidence  

### Phase 4: Quality Review and Integration (Week 7)
Metadata enhancement, corpus integration, and analytical preparation

## Success Indicators

By completion, APDES will have:
- **40+ YouTube-sourced speeches** spanning 2017-2024
- **Complete crisis coverage** for BLM, COVID, January 6th events  
- **Multi-perspective analysis** of each major populist moment
- **Robust temporal sequencing** showing populist discourse evolution
- **Research-quality corpus** ready for comprehensive framework analysis

This systematic collection will transform APDES from a 2016 replication study into the most comprehensive longitudinal populist discourse analysis available in the academic literature.