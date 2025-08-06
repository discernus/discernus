# Issue #338: APDES Era 2.5 Collection - Populist Governance Transition (2017-2019)

## Overview
Collect all Era 2.5 documents (Populist Governance Transition 2017-2019) using all available extraction methods: YouTube API, Whisper transcription, stealth scraping, and official sources.

## Target Corpus Group: Era 2.5 - Populist Governance Transition

### Collection Targets (24-30 documents)

#### Trump Rally Circuit (6-8 rallies)
**Collection Methods**: YouTube API + Whisper fallback, official transcripts
- Cincinnati Rally (August 2017) - First post-inaugural populist rally
- Phoenix Rally (August 2017) - Charlottesville response and media attacks
- Huntington WV Rally (August 2017) - Economic populism messaging
- Pensacola Rally (December 2017) - Moore endorsement and establishment attacks
- Nashville Rally (May 2018) - Immigration and wall messaging
- Duluth Rally (June 2018) - Trade war justification
- Tampa Rally (July 2018) - Media antagonism peak
- Charleston WV Rally (August 2018) - Coal populism and energy

#### Major Policy Populist Speeches (4-5 speeches)
**Collection Methods**: Stealth scraping (White House), official transcripts
- Immigration Executive Orders (January 2017) - Early populist implementation
- Trade War Announcement (March 2018) - Economic populist justification
- UN General Assembly (September 2018) - America First foreign policy
- Border Wall Emergency (February 2019) - Constitutional populism test
- Syria/Afghanistan Withdrawal (December 2018/2019) - Anti-elite foreign policy

#### Institutional Conflict Speeches (2-3 speeches)
**Collection Methods**: Stealth scraping (Congress), official transcripts
- Mueller Investigation Response (2018) - Deep state populism
- Government Shutdown Justification (December 2018) - Elite obstruction
- Fire Rosenstein/Sessions speeches - DOJ populist conflict

#### State-Level Populist Responses (4-5 speeches)
**Collection Methods**: YouTube API, stealth scraping (state government)
- DeSantis early governance speeches (Florida populism)
- Abbott border populism evolution (Texas)
- Noem cultural populist messaging (South Dakota)
- Whitmer institutional response to populist challenges (Michigan)

#### Media and Commentary (4-5 speeches)
**Collection Methods**: YouTube API, stealth scraping (news sources)
- Tucker Carlson segments on populist governance
- Sean Hannity populist messaging analysis
- Fox News populist commentary segments
- Conservative media populist framing

## Implementation Requirements

### Multi-Method Collection Strategy
**Primary Methods**
- **YouTube API**: Fastest method for video content with existing transcripts
- **Whisper Transcription**: High-quality fallback for any audio/video content
- **Stealth Scraping**: Bypass restrictions on government and news websites
- **Official Transcripts**: Direct access to official speech repositories

**Method Selection Logic**
- Try YouTube API first for video content
- Fall back to Whisper for incomplete or low-quality transcripts
- Use stealth scraping for government websites and restricted sources
- Cross-reference with official transcripts when available

### Quality Assurance Protocols
**Academic Verification**
- Full-length speech identification and verification
- Cross-reference video duration with official event records
- Verify against news reports of actual speech length
- Check C-SPAN archives for authoritative timing when available

**Content Quality Assessment**
- Transcript completeness verification
- Speaker identification and attribution
- Temporal context and event metadata
- Academic standards compliance

### Metadata Requirements
**Standard APDES Metadata**
- Speaker identification and party affiliation
- Event date and location
- Speech type and context (rally, policy, institutional)
- Temporal era classification (Era 2.5)
- Collection method and confidence score
- Academic verification status

**Era-Specific Metadata**
- Populist governance context indicators
- Policy implementation vs. campaign messaging
- Institutional conflict markers
- State vs. federal populist dynamics

## Success Criteria
- [ ] Complete collection of 24-30 Era 2.5 documents
- [ ] All documents pass academic verification protocols
- [ ] Comprehensive metadata and provenance tracking maintained
- [ ] Integration with APDES corpus structure and manifest system
- [ ] Quality assurance validation for academic analysis readiness
- [ ] Multi-method collection approach successfully implemented

## Dependencies
- Enhanced transcript extractor from d41dea73 commit
- Stealth transcript scraper from d41dea73 commit
- Academic verification protocols from planning documents
- Integration with APDES corpus manifest system

## Estimated Effort
- **Collection Phase**: 6-8 hours systematic multi-method collection
- **Verification Phase**: 3-4 hours quality assurance
- **Integration Phase**: 2-3 hours corpus integration
- **Total**: 11-15 hours for complete Era 2.5 collection

## Related Issues
- Epic #274: APDES - American Populist Discourse Evolution Study
- Issue #339: APDES Era 3 Collection - Institutional Crisis (2020-2021)
- Issue #340: APDES Era 4 Collection - Populist Consolidation (2024)
- Issue #341: APDES Corpus Metadata Refinement and Integration 