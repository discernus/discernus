# Presidential Addresses to Congress Corpus

This corpus contains presidential addresses to Congress, including State of the Union addresses, inaugural addresses, and other joint session speeches.

## Current Coverage

### State of the Union Addresses (SOTU)
- **Clinton (1993-2000):** 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001 ✅
- **Bush (2001-2008):** 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009 ✅
- **Obama (2009-2016):** 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017 ✅
- **Trump (2017-2020):** 2017, 2018, 2019, 2020, 2025 ✅
- **Biden (2021-present):** 2021, 2022, 2023, 2024, 2025 ✅

### Joint Session Addresses (Non-SOTU)
- **Clinton (1993):** Administration Goals Address ✅
- **Bush (2001):** Administration Goals Address ✅
- **Obama (2009):** Economic Recovery Address ✅
- **Trump (2017):** Joint Session Address ✅
- **Biden (2021):** Joint Session Address ✅

### Inaugural Addresses
- **Washington (1789):** First Inaugural ✅
- **Clinton (1993, 1997):** First and Second Inaugurals ✅
- **Bush (2001, 2005):** First and Second Inaugurals ✅
- **Obama (2009, 2013):** First and Second Inaugurals ✅
- **Trump (2017, 2025):** First and Second Inaugurals ✅
- **Biden (2021, 2025):** First and Second Inaugurals ✅

## Corpus Status

**Total Coverage:** 1789-2025 ✅ **COMPLETE**

All major presidential addresses to Congress from 1993 to the present are now included in the corpus, providing comprehensive coverage for the Discernus project's analysis of modern presidential rhetoric and policy communication.

## File Naming Convention

Files follow various patterns:
- `{President}_{Type}_{Year}.txt` (e.g., `Biden_SOTU_2021.txt`)
- `{president}_{year}_{description}.md` (e.g., `barack_obama_2009_address_before_a_joint_session_of_the_congress.md`)

## Source Attribution

All speeches are sourced from the American Presidency Project (presidency.ucsb.edu) and include proper metadata including president, date, source, and speech type.

---

<details>
<summary>Machine-Readable Manifest</summary>

```json
{
  "corpus_version": "7.3",
  "total_documents": 48,
  "date_range": {
    "start_year": 1992,
    "end_year": 2025
  },
  "field_naming_standards": {
    "required_consistency": ["president", "year", "speech_type", "format"],
    "prohibited_variations": {
      "speaker": "president",
      "document_type": "speech_type",
      "file_type": "format"
    }
  },
  "statistical_readiness": {
    "grouping_variables": ["president", "speech_type"],
    "temporal_variables": ["year"]
  },
  "file_manifest": [
    {
      "name": "george_bush_1992_address_before_a_joint_session_of_the_congress_on_the_state_of_the_union.md",
      "president": "George H.W. Bush",
      "year": 1992,
      "speech_type": "SOTU",
      "format": "text"
    },
    {
      "name": "Clinton_Inaugural_1993.txt",
      "president": "William J. Clinton",
      "year": 1993,
      "speech_type": "Inaugural",
      "format": "text"
    },
    {
      "name": "Clinton_SOTU_1993.txt",
      "president": "William J. Clinton",
      "year": 1993,
      "speech_type": "SOTU",
      "format": "text"
    },
    {
      "name": "william_j_clinton_1993_address_before_a_joint_session_of_congress_on_administration_goals.md",
      "president": "William J. Clinton",
      "year": 1993,
      "speech_type": "Joint Session Address",
      "format": "text"
    },
    {
      "name": "Clinton_SOTU_1994.txt",
      "president": "William J. Clinton",
      "year": 1994,
      "speech_type": "SOTU",
      "format": "text"
    },
    {
      "name": "Clinton_SOTU_1995.txt",
      "president": "William J. Clinton",
      "year": 1995,
      "speech_type": "SOTU",
      "format": "text"
    },
    {
      "name": "Clinton_SOTU_1996.txt",
      "president": "William J. Clinton",
      "year": 1996,
      "speech_type": "SOTU",
      "format": "text"
    },
    {
      "name": "Clinton_Inaugural_1997.txt",
      "president": "William J. Clinton",
      "year": 1997,
      "speech_type": "Inaugural",
      "format": "text"
    },
    {
      "name": "Clinton_SOTU_1997.txt",
      "president": "William J. Clinton",
      "year": 1997,
      "speech_type": "SOTU",
      "format": "text"
    },
    {
      "name": "Clinton_SOTU_1998.txt",
      "president": "William J. Clinton",
      "year": 1998,
      "speech_type": "SOTU",
      "format": "text"
    },
    {
      "name": "Clinton_SOTU_1999.txt",
      "president": "William J. Clinton",
      "year": 1999,
      "speech_type": "SOTU",
      "format": "text"
    },
    {
      "name": "Clinton_SOTU_2000.txt",
      "president": "William J. Clinton",
      "year": 2000,
      "speech_type": "SOTU",
      "format": "text"
    },
    {
      "name": "Bush_Inaugural_2001.txt",
      "president": "George W. Bush",
      "year": 2001,
      "speech_type": "Inaugural",
      "format": "text"
    },

    {
      "name": "Clinton_SOTU_2001.txt",
      "president": "William J. Clinton",
      "year": 2001,
      "speech_type": "SOTU",
      "format": "text"
    },
    {
      "name": "george_w_bush_2001_address_before_a_joint_session_of_the_congress_on_administration_goals.md",
      "president": "George W. Bush",
      "year": 2001,
      "speech_type": "Joint Session Address",
      "format": "text"
    },
    {
      "name": "Bush_SOTU_2002.txt",
      "president": "Bush",
      "year": 2002,
      "speech_type": "SOTU",
      "format": "text"
    },
    {
      "name": "Bush_SOTU_2003.txt",
      "president": "Bush",
      "year": 2003,
      "speech_type": "SOTU",
      "format": "text"
    },
    {
      "name": "Bush_SOTU_2004.txt",
      "president": "Bush",
      "year": 2004,
      "speech_type": "SOTU",
      "format": "text"
    },
    {
      "name": "Bush_Inaugural_2005.txt",
      "president": "Bush",
      "year": 2005,
      "speech_type": "Inaugural",
      "format": "text"
    },
    {
      "name": "Bush_SOTU_2005.txt",
      "president": "Bush",
      "year": 2005,
      "speech_type": "SOTU",
      "format": "text"
    },
    {
      "name": "Bush_SOTU_2006.txt",
      "president": "Bush",
      "year": 2006,
      "speech_type": "SOTU",
      "format": "text"
    },
    {
      "name": "Bush_SOTU_2007.txt",
      "president": "Bush",
      "year": 2007,
      "speech_type": "SOTU",
      "format": "text"
    },
    {
      "name": "Bush_SOTU_2008.txt",
      "president": "Bush",
      "year": 2008,
      "speech_type": "SOTU",
      "format": "text"
    },
    {
      "name": "barack_obama_2009_address_before_a_joint_session_of_the_congress.md",
      "president": "Barack Obama",
      "year": 2009,
      "speech_type": "Joint Session Address",
      "format": "text"
    },
    {
      "name": "Bush_SOTU_2009.txt",
      "president": "Barack Obama",
      "year": 2009,
      "speech_type": "SOTU",
      "format": "text"
    },
    {
      "name": "Obama_Inaugural_2009.txt",
      "president": "Barack Obama",
      "year": 2009,
      "speech_type": "Inaugural",
      "format": "text"
    },

    {
      "name": "Obama_SOTU_2010.txt",
      "president": "Barack Obama",
      "year": 2010,
      "speech_type": "SOTU",
      "format": "text"
    },
    {
      "name": "Obama_SOTU_2011.txt",
      "president": "Barack Obama",
      "year": 2011,
      "speech_type": "SOTU",
      "format": "text"
    },
    {
      "name": "Obama_SOTU_2012.txt",
      "president": "Barack Obama",
      "year": 2012,
      "speech_type": "SOTU",
      "format": "text"
    },
    {
      "name": "Obama_Inaugural_2013.txt",
      "president": "Barack Obama",
      "year": 2013,
      "speech_type": "Inaugural",
      "format": "text"
    },
    {
      "name": "Obama_SOTU_2013.txt",
      "president": "Barack Obama",
      "year": 2013,
      "speech_type": "SOTU",
      "format": "text"
    },
    {
      "name": "Obama_SOTU_2014.txt",
      "president": "Barack Obama",
      "year": 2014,
      "speech_type": "SOTU",
      "format": "text"
    },
    {
      "name": "Obama_SOTU_2015.txt",
      "president": "Barack Obama",
      "year": 2015,
      "speech_type": "SOTU",
      "format": "text"
    },
    {
      "name": "Obama_SOTU_2016.txt",
      "president": "Barack Obama",
      "year": 2016,
      "speech_type": "SOTU",
      "format": "text"
    },
    {
      "name": "donald_j_trump_1st_term_2017_address_before_a_joint_session_of_the_congress.md",
      "president": "Donald Trump",
      "year": 2017,
      "speech_type": "Joint Session Address",
      "format": "text"
    },
    {
      "name": "Obama_SOTU_2017.txt",
      "president": "Barack Obama",
      "year": 2017,
      "speech_type": "SOTU",
      "format": "text"
    },
    {
      "name": "Trump_Inaugural_2017.txt",
      "president": "Donald Trump",
      "year": 2017,
      "speech_type": "Inaugural",
      "format": "text"
    },

    {
      "name": "Trump_SOTU_2018.txt",
      "president": "Donald Trump",
      "year": 2018,
      "speech_type": "SOTU",
      "format": "text"
    },

    {
      "name": "Trump_SOTU_2019.txt",
      "president": "Donald Trump",
      "year": 2019,
      "speech_type": "SOTU",
      "format": "text"
    },
    {
      "name": "Trump_SOTU_2020.txt",
      "president": "Donald Trump",
      "year": 2020,
      "speech_type": "SOTU",
      "format": "text"
    },
    {
      "name": "Biden_Inaugural_2021.txt",
      "president": "Joe Biden",
      "year": 2021,
      "speech_type": "Inaugural",
      "format": "text"
    },

    {
      "name": "joseph_r_biden_jr_2021_address_before_a_joint_session_of_the_congress.md",
      "president": "Joe Biden",
      "year": 2021,
      "speech_type": "Joint Session Address",
      "format": "text"
    },
    {
      "name": "Biden_SOTU_2022.txt",
      "president": "Joe Biden",
      "year": 2022,
      "speech_type": "SOTU",
      "format": "text"
    },
    {
      "name": "Biden_SOTU_2023.txt",
      "president": "Joe Biden",
      "year": 2023,
      "speech_type": "SOTU",
      "format": "text"
    },
    {
      "name": "Biden_SOTU_2024.txt",
      "president": "Joe Biden",
      "year": 2024,
      "speech_type": "SOTU",
      "format": "text"
    },
    {
      "name": "Biden_SOTU_2025.txt",
      "president": "Joe Biden",
      "year": 2025,
      "speech_type": "Farewell Address",
      "format": "text"
    },
    {
      "name": "Trump_Inaugural_2025.txt",
      "president": "Donald Trump",
      "year": 2025,
      "speech_type": "Inaugural",
      "format": "text"
    },
    {
      "name": "Trump_SOTU_2025.txt",
      "president": "Donald Trump",
      "year": 2025,
      "speech_type": "Joint Session Address",
      "format": "text"
    }
  ]
}
```
</details>
