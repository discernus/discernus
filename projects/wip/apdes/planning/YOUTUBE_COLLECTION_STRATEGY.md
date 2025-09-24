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

### Academic Verification Protocols

#### Full-Length Speech Identification
**Critical Requirement**: Only complete, unedited speeches acceptable for academic analysis

1. **Duration Verification Process**:
   - Cross-reference video duration with official event records
   - Verify against news reports of actual speech length  
   - Check C-SPAN archives for authoritative timing when available
   - Flag any video under expected duration for manual review
   - Document expected vs actual duration discrepancies

2. **Content Completeness Validation**:
   - Verify opening and closing remarks are present and complete
   - Check for continuous speech flow without obvious jump cuts
   - Identify editing artifacts, missing segments, or audio gaps
   - Ensure introduction/conclusion match known speech structure from news reports
   - Flag videos with suspicious transitions or incomplete content

3. **Source Authentication Strategy**:
   - **Tier 1 (Preferred)**: Official government channels (White House, Senate, House, Governor offices)
   - **Tier 2 (Reliable)**: C-SPAN, major established news networks (CNN, Fox, MSNBC, ABC, NBC, CBS)  
   - **Tier 3 (Acceptable)**: Verified political organization channels, campaign accounts
   - **Tier 4 (Avoid)**: User uploads, unverified channels, compilation videos
   - Cross-check multiple sources when official versions unavailable
   - Document source tier and verification confidence

#### Metadata Validation Requirements

**Speaker Authentication**:
- Verify primary speaker identity through visual confirmation in video
- Cross-reference speaker attribution with official event records
- Check speaker name against known aliases or common misspellings
- Flag any uncertainty in speaker identification for manual review
- Document secondary speakers, introducers, or moderators

**Date and Event Accuracy**:
- Confirm video upload date correlates with actual event date (±1 day acceptable for news uploads)
- Verify event date against contemporaneous news coverage
- Cross-reference location and venue details with historical records
- Document timezone considerations for live events
- Flag any temporal discrepancies requiring further investigation

**Contextual Verification**:
- Confirm event type classification (rally, press conference, formal address, debate, interview)
- Verify audience type and size (campaign crowd, congressional session, media briefing)
- Document occasion or trigger for speech (crisis response, routine event, campaign stop)
- Record venue name and geographic location with precision
- Note any special circumstances (emergency address, breaking news context)

### Video Identification Process
1. **Primary Source Search**: 
   - Official government/campaign channels first
   - C-SPAN archive searches for formal events
   - Major news network verified uploads
   
2. **Cross-Reference Validation**: 
   - Compare multiple sources for same event
   - Verify consistent duration across sources  
   - Check metadata alignment between sources
   
3. **Historical Verification**: 
   - Cross-check against newspaper archives (NYT, WaPo, WSJ)
   - Verify against academic databases when available
   - Confirm against presidential libraries/official records
   
4. **Duration Authentication**: 
   - Compare video length with reported speech duration
   - Account for introduction/conclusion time
   - Flag unusual brevity or length for investigation
   
5. **Academic Quality Assessment**: 
   - Ensure transcript quality meets research standards
   - Verify complete content suitable for framework analysis
   - Document confidence level in source reliability

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

#### Length and Completeness Requirements
- **Full-length speeches only**: No clips, excerpts, or highlight reels
- **Minimum duration threshold**: 
  - Formal addresses: 10+ minutes expected
  - Rally speeches: 30+ minutes expected  
  - Press conferences: 15+ minutes expected
  - Campaign speeches: 20+ minutes expected
- **Content integrity**: Complete opening/closing, no obvious edits or cuts
- **Transcript length validation**: Cross-check character count with expected speech length

#### Source Quality Verification
- **Speaker verification**: Visual confirmation of primary speaker throughout video
- **Date accuracy**: Upload date within 48 hours of actual event date
- **Source credibility**: Tier 1-3 sources only (see Authentication Strategy above)
- **Multiple source confirmation**: When possible, verify against 2+ independent uploads

#### Academic Research Standards  
- **Metadata completeness**: Speaker, date, location, event type, duration all documented
- **Contextual accuracy**: Event circumstances and significance verified
- **Transcript quality**: Manual captions preferred; high-confidence auto-captions acceptable
- **Cross-reference capability**: Event linkable to contemporaneous news coverage
- **Replication documentation**: Sufficient detail for other researchers to locate same content

#### Pre-Extraction Validation Checklist
- [ ] Video duration matches reported event length (±10%)
- [ ] Complete speech from opening to closing remarks
- [ ] Primary speaker clearly identifiable and verified
- [ ] Event date confirmed through news sources
- [ ] Source meets Tier 1-3 authentication standards
- [ ] No obvious editing artifacts or missing content
- [ ] Transcript/captions available and legible
- [ ] Event context and significance documented

#### Post-Extraction Quality Review
- [ ] Transcript captures complete speech content
- [ ] Speaker attribution accurate throughout
- [ ] No missing segments or garbled text
- [ ] Metadata fields complete and verified
- [ ] File properly organized in era/category structure
- [ ] Cross-reference documentation complete

### Academic Verification Workflow

#### Phase 1: Target Event Research (Before YouTube Search)
1. **Historical Event Documentation**:
   - Identify specific event from news archives, presidential libraries, official records
   - Document expected speech length from contemporaneous reporting
   - Note key themes, quotes, or moments that should appear in complete version
   - Record official venue, date, time, and attendance figures

2. **Multi-Source Cross-Reference**:
   - Check multiple news sources for event coverage and duration
   - Verify against C-SPAN archives when available  
   - Cross-reference with academic databases or government records
   - Document expected speech structure and key content markers

#### Phase 2: YouTube Source Identification  
1. **Systematic Search Strategy**:
   - Search official government/campaign channels first
   - Query major news networks with verified accounts
   - Use specific date ranges and location filters
   - Document all potential sources found

2. **Source Evaluation Matrix**:
   - Rate each source using Tier 1-4 authentication system
   - Compare video durations across sources
   - Check upload dates against event dates  
   - Note any discrepancies or red flags

#### Phase 3: Pre-Extraction Validation
1. **Content Verification**:
   - Watch opening 2-3 minutes to confirm complete speech start
   - Skip to ending to verify complete conclusion present
   - Sample middle sections for continuous flow
   - Check for obvious edits, cuts, or missing segments

2. **Metadata Documentation**:
   - Complete verification checklist for chosen source
   - Document confidence level and any concerns
   - Record alternative sources as backups
   - Note any limitations or caveats

#### Academic Documentation Template

For each collected speech, maintain research record:

```markdown
# [Speaker] [Event Type] - [Date] - [Location]

## Source Information
- **YouTube URL**: [link]
- **Channel**: [channel name]
- **Upload Date**: [date]
- **Source Tier**: [1-4]
- **Alternative Sources**: [list other versions found]

## Event Verification
- **Reported Duration**: [from news sources]
- **Video Duration**: [actual video length]
- **Duration Match**: [Y/N with % variance]
- **News Sources**: [NYT, WaPo, etc. coverage links]
- **Official Records**: [government/library documentation]

## Content Validation
- **Complete Opening**: [Y/N]
- **Complete Conclusion**: [Y/N]  
- **Continuous Flow**: [Y/N]
- **Editing Artifacts**: [None/List any found]
- **Key Moments Present**: [Verify expected quotes/themes]

## Metadata Accuracy
- **Speaker Verified**: [Y/N]
- **Date Verified**: [Y/N]
- **Location Verified**: [Y/N]
- **Event Context**: [Description]
- **APDES Classification**: [Era, category, significance]

## Quality Assessment
- **Academic Suitability**: [High/Medium/Low]
- **Research Confidence**: [0-100%]
- **Extraction Recommend**: [Y/N]
- **Special Notes**: [Any concerns or limitations]
```

### Success Metrics

#### Academic Verification Success Rates
- **Source Authentication**: 100% of extracted speeches from Tier 1-3 sources
- **Duration Verification**: 90%+ of speeches match expected length within ±15%
- **Content Completeness**: 95%+ contain complete opening and closing remarks
- **Metadata Accuracy**: 100% accuracy in speaker, date, location verification
- **Cross-Reference Success**: 90%+ independently confirmed through multiple sources

#### Coverage Quality Standards  
- **Coverage completeness**: All major populist speakers and crisis events represented
- **Temporal accuracy**: Events properly sequenced within eras with verified dates
- **Ideological balance**: Multiple perspectives on each crisis/event captured
- **Full-length requirement**: 100% complete speeches, zero clips or excerpts
- **Research utility**: 95%+ of extractions suitable for academic framework analysis

#### Documentation and Reproducibility
- **Academic documentation**: Complete verification record for each speech
- **Source transparency**: All YouTube URLs and alternative sources documented  
- **Methodology replication**: Sufficient detail for independent researcher validation
- **Quality assurance**: Pre and post-extraction checklists completed for all content

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