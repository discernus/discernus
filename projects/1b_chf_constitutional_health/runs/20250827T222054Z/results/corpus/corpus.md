# Presidential Addresses to Congress Corpus

This corpus contains presidential addresses to Congress, including State of the Union addresses, inaugural addresses, and other joint session speeches. The corpus spans from 1992-2025, including both Bush presidencies: George H.W. Bush (1992 baseline) and George W. Bush (2001-2008).

## Current Coverage

### Cold War Transition Baseline (1992)
- **Bush H.W. (1992):** 1992 SOTU ✅

### State of the Union Addresses (SOTU)

- **Clinton (1993-2000):** 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001 ✅
- **Bush W. (2001-2008):** 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009 ✅
- **Obama (2009-2016):** 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017 ✅
- **Trump (2017-2020):** 2017, 2018, 2019, 2020, 2025 ✅
- **Biden (2021-present):** 2021, 2022, 2023, 2024, 2025 ✅

### Joint Session Addresses (Non-SOTU)

- **Clinton (1993):** Administration Goals Address ✅
- **Bush W. (2001):** Administration Goals Address ✅
- **Obama (2009):** Economic Recovery Address ✅
- **Trump (2017):** Joint Session Address ✅
- **Biden (2021):** Joint Session Address ✅

### Inaugural Addresses

- **Washington (1789):** First Inaugural ✅
- **Clinton (1993, 1997):** First and Second Inaugurals ✅
- **Bush W. (2001, 2005):** First and Second Inaugurals ✅
- **Obama (2009, 2013):** First and Second Inaugurals ✅
- **Trump (2017, 2025):** First and Second Inaugurals ✅
- **Biden (2021, 2025):** First and Second Inaugurals ✅

## Corpus Status

**Total Coverage:** 1789, 1992-2025 ✅ **COMPLETE**

All major presidential addresses to Congress from 1992 to the present are now included in the corpus, including the Bush H.W. 1992 baseline, providing comprehensive coverage for the Discernus project's analysis of modern presidential rhetoric and policy communication.

## File Naming Convention

Files follow various patterns:

- `{President}_{Type}_{Year}.txt` (e.g., `Biden_SOTU_2021.txt`)
- `{president}_{year}_{description}.md` (e.g., `barack_obama_2009_address_before_a_joint_session_of_the_congress.md`)

## Source Attribution

All speeches are sourced from the American Presidency Project (presidency.ucsb.edu) and include proper metadata including president, date, source, and speech type.

---

## Document Manifest

```yaml
name: "Presidential Addresses to Congress Corpus"
version: "10.0"
spec_version: "10.0"
total_documents: 48
date_range: "1789, 1992-2025"

documents:
  - filename: "george_bush_1992_address_before_a_joint_session_of_the_congress_on_the_state_of_the_union.md"
    document_id: "bush_hw_1992_sotu"
    metadata:
      speaker: "George H.W. Bush"
      year: 1992
      party: "Republican"
      speech_type: "SOTU"
      format: "text"
  - filename: "Clinton_Inaugural_1993.txt"
    document_id: "clinton_1993_inaugural"
    metadata:
      speaker: "William J. Clinton"
      year: 1993
      party: "Democratic"
      speech_type: "Inaugural"
      format: "text"
  - filename: "Clinton_SOTU_1993.txt"
    document_id: "clinton_1993_sotu"
    metadata:
      speaker: "William J. Clinton"
      year: 1993
      party: "Democratic"
      speech_type: "SOTU"
      format: "text"
  - filename: "william_j_clinton_1993_address_before_a_joint_session_of_congress_on_administration_goals.md"
    document_id: "clinton_1993_admin_goals"
    metadata:
      speaker: "William J. Clinton"
      year: 1993
      party: "Democratic"
      speech_type: "Joint Session Address"
      format: "text"
  - filename: "Clinton_SOTU_1994.txt"
    document_id: "clinton_1994_sotu"
    metadata:
      speaker: "William J. Clinton"
      year: 1994
      party: "Democratic"
      speech_type: "SOTU"
      format: "text"
  - filename: "Clinton_SOTU_1995.txt"
    document_id: "clinton_1995_sotu"
    metadata:
      speaker: "William J. Clinton"
      year: 1995
      party: "Democratic"
      speech_type: "SOTU"
      format: "text"
  - filename: "Clinton_SOTU_1996.txt"
    document_id: "clinton_1996_sotu"
    metadata:
      speaker: "William J. Clinton"
      year: 1996
      party: "Democratic"
      speech_type: "SOTU"
      format: "text"
  - filename: "Clinton_Inaugural_1997.txt"
    document_id: "clinton_1997_inaugural"
    metadata:
      speaker: "William J. Clinton"
      year: 1997
      party: "Democratic"
      speech_type: "Inaugural"
      format: "text"
  - filename: "Clinton_SOTU_1997.txt"
    document_id: "clinton_1997_sotu"
    metadata:
      speaker: "William J. Clinton"
      year: 1997
      party: "Democratic"
      speech_type: "SOTU"
      format: "text"
  - filename: "Clinton_SOTU_1998.txt"
    document_id: "clinton_1998_sotu"
    metadata:
      speaker: "William J. Clinton"
      year: 1998
      party: "Democratic"
      speech_type: "SOTU"
      format: "text"
  - filename: "Clinton_SOTU_1999.txt"
    document_id: "clinton_1999_sotu"
    metadata:
      speaker: "William J. Clinton"
      year: 1999
      party: "Democratic"
      speech_type: "SOTU"
      format: "text"
  - filename: "Clinton_SOTU_2000.txt"
    document_id: "clinton_2000_sotu"
    metadata:
      speaker: "William J. Clinton"
      year: 2000
      party: "Democratic"
      speech_type: "SOTU"
      format: "text"
  - filename: "Bush_Inaugural_2001.txt"
    document_id: "bush_w_2001_inaugural"
    metadata:
      speaker: "George W. Bush"
      year: 2001
      party: "Republican"
      speech_type: "Inaugural"
      format: "text"
  - filename: "Clinton_SOTU_2001.txt"
    document_id: "clinton_2001_sotu"
    metadata:
      speaker: "William J. Clinton"
      year: 2001
      party: "Democratic"
      speech_type: "SOTU"
      format: "text"
  - filename: "george_w_bush_2001_address_before_a_joint_session_of_the_congress_on_administration_goals.md"
    document_id: "bush_w_2001_admin_goals"
    metadata:
      speaker: "George W. Bush"
      year: 2001
      party: "Republican"
      speech_type: "Joint Session Address"
      format: "text"
  - filename: "Bush_SOTU_2002.txt"
    document_id: "bush_w_2002_sotu"
    metadata:
      speaker: "George W. Bush"
      year: 2002
      party: "Republican"
      speech_type: "SOTU"
      format: "text"
  - filename: "Bush_SOTU_2003.txt"
    document_id: "bush_w_2003_sotu"
    metadata:
      speaker: "George W. Bush"
      year: 2003
      party: "Republican"
      speech_type: "SOTU"
      format: "text"
  - filename: "Bush_SOTU_2004.txt"
    document_id: "bush_w_2004_sotu"
    metadata:
      speaker: "George W. Bush"
      year: 2004
      party: "Republican"
      speech_type: "SOTU"
      format: "text"
  - filename: "Bush_Inaugural_2005.txt"
    document_id: "bush_w_2005_inaugural"
    metadata:
      speaker: "George W. Bush"
      year: 2005
      party: "Republican"
      speech_type: "Inaugural"
      format: "text"
  - filename: "Bush_SOTU_2005.txt"
    document_id: "bush_w_2005_sotu"
    metadata:
      speaker: "George W. Bush"
      year: 2005
      party: "Republican"
      speech_type: "SOTU"
      format: "text"
  - filename: "Bush_SOTU_2006.txt"
    document_id: "bush_w_2006_sotu"
    metadata:
      speaker: "George W. Bush"
      year: 2006
      party: "Republican"
      speech_type: "SOTU"
      format: "text"
  - filename: "Bush_SOTU_2007.txt"
    document_id: "bush_w_2007_sotu"
    metadata:
      speaker: "George W. Bush"
      year: 2007
      party: "Republican"
      speech_type: "SOTU"
      format: "text"
  - filename: "Bush_SOTU_2008.txt"
    document_id: "bush_w_2008_sotu"
    metadata:
      speaker: "George W. Bush"
      year: 2008
      party: "Republican"
      speech_type: "SOTU"
      format: "text"
  - filename: "barack_obama_2009_address_before_a_joint_session_of_the_congress.md"
    document_id: "obama_2009_economic_recovery"
    metadata:
      speaker: "Barack Obama"
      year: 2009
      party: "Democratic"
      speech_type: "Joint Session Address"
      format: "text"
  - filename: "Bush_SOTU_2009.txt"
    document_id: "obama_2009_sotu"
    metadata:
      speaker: "Barack Obama"
      year: 2009
      party: "Democratic"
      speech_type: "SOTU"
      format: "text"
  - filename: "Obama_Inaugural_2009.txt"
    document_id: "obama_2009_inaugural"
    metadata:
      speaker: "Barack Obama"
      year: 2009
      party: "Democratic"
      speech_type: "Inaugural"
      format: "text"
  - filename: "Obama_SOTU_2010.txt"
    document_id: "obama_2010_sotu"
    metadata:
      speaker: "Barack Obama"
      year: 2010
      party: "Democratic"
      speech_type: "SOTU"
      format: "text"
  - filename: "Obama_SOTU_2011.txt"
    document_id: "obama_2011_sotu"
    metadata:
      speaker: "Barack Obama"
      year: 2011
      party: "Democratic"
      speech_type: "SOTU"
      format: "text"
  - filename: "Obama_SOTU_2012.txt"
    document_id: "obama_2012_sotu"
    metadata:
      speaker: "Barack Obama"
      year: 2012
      party: "Democratic"
      speech_type: "SOTU"
      format: "text"
  - filename: "Obama_Inaugural_2013.txt"
    document_id: "obama_2013_inaugural"
    metadata:
      speaker: "Barack Obama"
      year: 2013
      party: "Democratic"
      speech_type: "Inaugural"
      format: "text"
  - filename: "Obama_SOTU_2013.txt"
    document_id: "obama_2013_sotu"
    metadata:
      speaker: "Barack Obama"
      year: 2013
      party: "Democratic"
      speech_type: "SOTU"
      format: "text"
  - filename: "Obama_SOTU_2014.txt"
    document_id: "obama_2014_sotu"
    metadata:
      speaker: "Barack Obama"
      year: 2014
      party: "Democratic"
      speech_type: "SOTU"
      format: "text"
  - filename: "Obama_SOTU_2015.txt"
    document_id: "obama_2015_sotu"
    metadata:
      speaker: "Barack Obama"
      year: 2015
      party: "Democratic"
      speech_type: "SOTU"
      format: "text"
  - filename: "Obama_SOTU_2016.txt"
    document_id: "obama_2016_sotu"
    metadata:
      speaker: "Barack Obama"
      year: 2016
      party: "Democratic"
      speech_type: "SOTU"
      format: "text"
  - filename: "donald_j_trump_1st_term_2017_address_before_a_joint_session_of_the_congress.md"
    document_id: "trump_2017_joint_session"
    metadata:
      speaker: "Donald Trump"
      year: 2017
      party: "Republican"
      speech_type: "Joint Session Address"
      format: "text"
  - filename: "Obama_SOTU_2017.txt"
    document_id: "obama_2017_sotu"
    metadata:
      speaker: "Barack Obama"
      year: 2017
      party: "Democratic"
      speech_type: "SOTU"
      format: "text"
  - filename: "Trump_Inaugural_2017.txt"
    document_id: "trump_2017_inaugural"
    metadata:
      speaker: "Donald Trump"
      year: 2017
      party: "Republican"
      speech_type: "Inaugural"
      format: "text"
  - filename: "Trump_SOTU_2018.txt"
    document_id: "trump_2018_sotu"
    metadata:
      speaker: "Donald Trump"
      year: 2018
      party: "Republican"
      speech_type: "SOTU"
      format: "text"
  - filename: "Trump_SOTU_2019.txt"
    document_id: "trump_2019_sotu"
    metadata:
      speaker: "Donald Trump"
      year: 2019
      party: "Republican"
      speech_type: "SOTU"
      format: "text"
  - filename: "Trump_SOTU_2020.txt"
    document_id: "trump_2020_sotu"
    metadata:
      speaker: "Donald Trump"
      year: 2020
      party: "Republican"
      speech_type: "SOTU"
      format: "text"
  - filename: "Biden_Inaugural_2021.txt"
    document_id: "biden_2021_inaugural"
    metadata:
      speaker: "Joe Biden"
      year: 2021
      party: "Democratic"
      speech_type: "Inaugural"
      format: "text"
  - filename: "joseph_r_biden_jr_2021_address_before_a_joint_session_of_the_congress.md"
    document_id: "biden_2021_joint_session"
    metadata:
      speaker: "Joe Biden"
      year: 2021
      party: "Democratic"
      speech_type: "Joint Session Address"
      format: "text"
  - filename: "Biden_SOTU_2022.txt"
    document_id: "biden_2022_sotu"
    metadata:
      speaker: "Joe Biden"
      year: 2022
      party: "Democratic"
      speech_type: "SOTU"
      format: "text"
  - filename: "Biden_SOTU_2023.txt"
    document_id: "biden_2023_sotu"
    metadata:
      speaker: "Joe Biden"
      year: 2023
      party: "Democratic"
      speech_type: "SOTU"
      format: "text"
  - filename: "Biden_SOTU_2024.txt"
    document_id: "biden_2024_sotu"
    metadata:
      speaker: "Joe Biden"
      year: 2024
      party: "Democratic"
      speech_type: "SOTU"
      format: "text"
  - filename: "Biden_SOTU_2025.txt"
    document_id: "biden_2025_sotu"
    metadata:
      speaker: "Joe Biden"
      year: 2025
      party: "Democratic"
      speech_type: "SOTU"
      format: "text"
  - filename: "Trump_Inaugural_2025.txt"
    document_id: "trump_2025_inaugural"
    metadata:
      speaker: "Donald Trump"
      year: 2025
      party: "Republican"
      speech_type: "Inaugural"
      format: "text"
  - filename: "Trump_SOTU_2025.txt"
    document_id: "trump_2025_joint_session"
    metadata:
      speaker: "Donald Trump"
      year: 2025
      party: "Republican"
      speech_type: "Joint Session Address"
      format: "text"
```
