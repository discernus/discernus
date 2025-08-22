# Trump Populism Corpus Collection Project

## 🎯 **Project Overview**
This project collects and processes Donald Trump's political discourse across his entire political career for the Discernus experiment. The goal is to achieve comprehensive temporal and geographical coverage to enable longitudinal analysis of his rhetorical evolution.

## 📊 **Current Status: Phase 1 - Strategic 2024 Collection**

### **Progress: 18 of 74 speeches collected (24.3%)**
- **Strategy**: Targeted collection for temporal/geographical balance
- **Target**: ~35-40 speeches total (not bulk processing all 74)
- **Focus**: Key campaign phases and swing states

### **Current Coverage (18 speeches)**
- **June 2024**: 7 speeches (AZ, NV, MI, WI, PA, PA, VA)
- **July 2024**: 3 speeches (MI, NC, MN)  
- **August 2024**: 8 speeches (GA, MT, NC, PA, NC, AZ)

### **Strategic Gaps to Fill**
- **September 2024**: 2-3 speeches (mid-campaign phase)
- **October 2024**: 3-4 speeches (late campaign phase)
- **November 2024**: 2-3 speeches (election week)

## 🗂️ **Project Structure**

```
projects/2d_trump_populism/
├── corpus/
│   ├── 2024_campaign/           # Current collection focus
│   │   ├── primary_campaign/    # Extracted transcripts
│   │   └── 2024_campaign_metadata.json
│   ├── campaign_2015_2016/      # ✅ COMPLETE (~125+ speeches)
│   ├── presidential_2017_2020/  # ✅ BASIC COVERAGE (5 speeches)
│   ├── first_campaign_1988_2000/ # ❌ NOT STARTED (critical baseline)
│   └── post_presidency_2021_2024/ # ❌ NOT STARTED (critical transformation)
├── docs/
│   ├── corpus_collection_status.md  # Detailed status tracking
│   └── cleanup_summary.md           # Project organization summary
└── tests/                           # Test scripts and validation
```

## 🎯 **Strategic Collection Plan**

### **Phase 1: Complete Strategic 2024 Coverage** ⏳ **IN PROGRESS**
- Achieve temporal and geographical balance
- Target ~35-40 total speeches
- Focus on key campaign phases and swing states

### **Phase 2: Add 2000 Campaign Baseline** 📋 **PLANNED**
- Establish pre-populist Trump baseline
- Target 3-5 key speeches from first presidential run
- Essential for transformation analysis

### **Phase 3: Add 2021-2023 Transformation Period** 📋 **PLANNED**
- Document post-January 6 evolution
- Target critical speeches (Jan 6, Jan 9, 2021)
- Sample of 2021-2023 speeches

## 🛠️ **Technical Infrastructure**

### **Transcript Extraction**
- **Primary Method**: OpenAI Whisper (local processing)
- **Fallback Method**: YouTube API (when accessible)
- **Model**: Standardized on "base" model
- **Performance**: ~5 minutes per speech

### **Quality Assurance**
- High-quality transcripts with metadata
- Consistent file naming and organization
- Full provenance tracking
- Robust error handling and fallbacks

## 📈 **Collection Metrics**

- **Total Available**: 74 speeches (2024 campaign)
- **Successfully Processed**: 18 speeches
- **Success Rate**: 100%
- **Processing Time**: ~5 minutes per speech

## 🎯 **Next Actions**

1. **Continue 2024 Strategic Collection**
   - Target September-October-November phases
   - Achieve temporal and geographical balance

2. **Begin 2000 Campaign Research**
   - Identify available 2000 campaign speeches
   - Plan collection strategy for baseline period

3. **Research 2021-2023 Content**
   - Locate January 6 and January 9, 2021 speeches
   - Identify key 2021-2023 speech sources

## 📝 **Key Documents**

- **[Corpus Collection Status](docs/corpus_collection_status.md)** - Detailed progress tracking
- **[Cleanup Summary](docs/cleanup_summary.md)** - Project organization details

---

*Last Updated: August 21, 2025*
*Status: Phase 1 (2024 Strategic Collection) - IN PROGRESS*