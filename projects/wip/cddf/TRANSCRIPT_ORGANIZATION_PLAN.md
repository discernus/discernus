# CDDF v10.2 Transcript Organization Plan

**Date**: 2025-10-01  
**Status**: Ready for Implementation

## 🎯 Key Issues Identified

### 1. **Multi-Speaker Military Addresses**
- **File**: `Full speeches： Trump, Hegseth address military leaders at rare meeting in Quantico.txt`
- **Issue**: Contains both Pete Hegseth (Secretary of War) and Donald Trump (President) speaking at same event
- **Solution**: Split into separate documents by speaker

### 2. **Multi-Speaker Debates**
- **Files**: 
  - `Full Debate： Harris vs. Trump in 2024 ABC News Presidential Debate ｜ WSJ.txt`
  - `FULL SHOW - Presidential GOP Republican Prime Time Debate Part 1 - Presidential Election 2016.txt`
  - `NBC News-YouTube Democratic Debate (Full).txt`
- **Issue**: Cannot associate single document with single speaker
- **Solution**: Create separate documents for each speaker's contributions

## 📋 Organization Strategy

### **Mode 1: Formal Speech Analysis (12/12) ✅**
*No changes needed - all single-speaker formal addresses*

### **Mode 2: Spontaneous Discourse Analysis (Target: 10 documents)**

#### **Current Status: 4/10 documents**
- ✅ `twitter_thread_ericgarland_2019.txt` (Single speaker)
- ✅ `reddit_hegseth_speech_discussion.txt` (Community discourse)
- ✅ `reddit_democrats_moderate_discussion.txt` (Community discourse)

#### **New Documents to Create (6 documents):**

**From Military Address Event:**
- `hegseth_military_address_2024.txt` (Pete Hegseth speech only)
- `trump_military_address_2024.txt` (Donald Trump speech only)

**From 2024 Presidential Debate:**
- `harris_2024_debate_responses.txt` (Kamala Harris contributions only)
- `trump_2024_debate_responses.txt` (Donald Trump contributions only)

**From 2016 GOP Primary Debate:**
- `trump_2016_primary_debate_responses.txt` (Donald Trump contributions only)

**From Democratic Debate:**
- `clinton_2016_primary_debate_responses.txt` (Hillary Clinton contributions only)

### **Mode 3: Hybrid/Mixed Analysis (Target: 6 documents)**

#### **Current Status: 6/6 documents ✅**
- ✅ `sanders_2016_announcement.docx`
- ✅ `trump_2016_announcement.docx`
- ✅ `FULL Hillary Clinton MSNBC Democratic Town Hall In Philadelphia April 25th 2016 HD.txt`
- ✅ `CNN Presidential Town Hall with Joe Biden - (2021-07-21) FULL.txt`
- ✅ `FULL Donald Trump Town Hall Event VIRGINIA BEACH, VIRGINIA 9⧸6⧸16 - FNN.txt`
- ✅ `FULL TOWN HALL： JD Vance Takes Questions From PA Voters At Event With Tulsi Gabbard.txt`

## 🛠️ Implementation Steps

### **Step 1: Split Military Addresses**
1. Extract Hegseth speech (0:02 - 45:06)
2. Extract Trump speech (45:11 - end)
3. Create separate files with proper metadata

### **Step 2: Extract Debate Contributions**
1. **2024 Harris vs Trump Debate**: Extract individual responses
2. **2016 GOP Primary Debate**: Extract Trump responses
3. **Democratic Debate**: Extract Clinton responses

### **Step 3: Update Corpus Manifest**
1. Add new documents to Mode 2 section
2. Update document counts
3. Add metadata for each new document

## 📊 Expected Final Corpus

**Total Documents**: 28/28 (100% complete)
- **Mode 1 (Formal)**: 12/12 (100%) ✅
- **Mode 2 (Spontaneous)**: 10/10 (100%) ✅
- **Mode 3 (Hybrid)**: 6/6 (100%) ✅

## 🎯 CDDF v10.2 Analysis Benefits

### **Mode 2 Validation**:
- **Individual Spontaneous Speeches**: Hegseth, Trump military addresses
- **Debate Contributions**: Real-time political discourse under pressure
- **Social Media Discourse**: Twitter threads, Reddit discussions

### **Mode 3 Validation**:
- **Town Halls**: Q&A format with prepared and spontaneous elements
- **Campaign Announcements**: Mixed prepared/spontaneous content

## 🚀 Next Steps

1. **Split military addresses** into separate speaker files
2. **Extract debate contributions** by speaker
3. **Update corpus manifest** with new documents
4. **Run CDDF v10.2 analysis** on complete corpus

This organization will provide the perfect testbed for CDDF v10.2's genre-aware analytical modes!
