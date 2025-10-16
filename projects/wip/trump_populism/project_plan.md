# Trump Populism Research Project - Master Plan

## 🎯 Research Objective
**How Trump's populist rhetorical strategies evolve across political contexts (1988-2025)** using PDAF v10.0 framework.

## 📊 Current Status (STRATEGIC PIVOT TO PHASE 1)
- **Phase 1 Focus**: Replication of Van der Veen et al. (2024) presidential study
- **Data Source**: Existing corpus in `/pm/paper_replication_experiment_vandelveen/`
- **Framework**: PDAF v10.0 ready for immediate validation
- **Readiness**: 80% - focused execution with existing data
- **STRATEGIC ADVANTAGE**: Concrete results before massive expansion

## 🚨 ADVERSARIAL REVIEW FINDINGS

### **Critical Coverage Gaps**
1. **Presidential Governance Content**: Missing complete SOTU series, foreign policy, crisis response
2. **Business Era Content**: 1980s-2000s business interviews, books, corporate rhetoric
3. **Direct Communication**: Social media, press conferences, unfiltered Q&A
4. **Institutional Context**: Congressional addresses, policy implementation rhetoric
5. **Strategic Evolution Tracking**: Cannot analyze populist adaptation to power

### **PDAF v10.0 Compliance Issues**
- **Strategic Tension Analysis**: Mathematically valid but substantively misleading
- **Context Blindness**: Cannot distinguish campaign vs. governance populism
- **Temporal Gaps**: Missing evolutionary baselines for authentic change measurement

## 📁 REVISED TARGET STRUCTURE

```
corpus/
├── analysis_ready/              # Current: 109 docs | Target: 200+ docs
│   ├── 01_campaign_2015_2016/      # 35 docs ✅
│   ├── 02_presidential_2017_2020/  # 12 docs → Target: 40+ docs
│   │   ├── governance_core/          # SOTU, Inaugural ✅
│   │   ├── foreign_policy/           # NEW: NATO, Middle East, China
│   │   ├── crisis_response/          # NEW: COVID, Jan 6, impeachment
│   │   ├── domestic_policy/          # NEW: Infrastructure, economy
│   │   └── institutional/            # NEW: Congressional addresses
│   ├── 03_post_presidency_2021_2023/ # 23 docs → Target: 35+ docs
│   ├── 04_2024_campaign/            # 35 docs ✅
│   └── 05_baseline_1988_2000/       # 6 docs → Target: 30+ docs
│       ├── business_era/             # NEW: 1980s-2000s content
│       ├── early_political/          # NEW: Reform Party, 2000 run
│       └── media_appearances/        # NEW: Interviews, TV appearances
├── expansion_targets/            # NEW: Systematic gap-filling
│   ├── presidential_governance/     # SOTU 2017, foreign policy addresses
│   ├── business_rhetoric/           # Art of the Deal, corporate speeches
│   ├── direct_communication/        # Twitter/X, press conferences
│   ├── institutional_context/       # Cabinet meetings, policy announcements
│   └── strategic_evolution/         # Crisis responses, adaptation patterns
├── archive/                       # Original files preserved
├── baseline_2017_2020/            # Enhanced governance content
└── metadata/                      # Unified corpus tracking
```

## 🚀 REVISED EXECUTION ROADMAP

### **Phase 1A**: Foundation Assessment (Complete ✅)
- Adversarial review completed
- Coverage gaps identified
- Methodological risks documented

### **Phase 1B**: Corpus Expansion with Centralized Tools (Priority Focus)

#### **Automated Pipeline Available**: `/scripts/expansion_pipeline.py`
```bash
# Run specific expansion phase
python scripts/expansion_pipeline.py --phase presidential --week 1
python scripts/expansion_pipeline.py --phase business --week 2

# Generate progress reports
python scripts/expansion_pipeline.py --generate-report
python scripts/expansion_pipeline.py --validate-all
```

#### **Week-by-Week Breakdown**
- **Week 1**: Presidential governance content (SOTU 2017, foreign policy)
  - **Tools**: `youtube_transcript_extractor.py`, `html_transcript_extractor.py`
  - **Resources**: `/corpus/political/us/` for existing presidential content
  - **Methods**: Leverage existing political corpus + targeted gap filling
  - **Command**: `python scripts/expansion_pipeline.py --phase presidential --week 1`

- **Week 2**: Business era content (1980s-2000s interviews, books)
  - **Tools**: `query_corpus.py`, `enhanced_transcript_extractor.py`
  - **Resources**: `/corpus/business/` for corporate communications baseline
  - **Methods**: Cross-reference business corpus + media archives
  - **Command**: `python scripts/expansion_pipeline.py --phase business --week 2`

- **Week 3**: Direct communication (social media, press conferences)
  - **Tools**: `batch_post_presidency_extractor.py`, `validate_corpus.py`
  - **Resources**: `/corpus/tools/` extraction pipeline for systematic collection
  - **Methods**: Automated collection with quality assurance pipeline
  - **Command**: `python scripts/expansion_pipeline.py --phase direct --week 3`

- **Week 4**: Institutional context (Congressional addresses, hearings)
  - **Tools**: `generate_indexes.py`, `standardize_metadata.py`
  - **Resources**: `/corpus/political/us/` congressional records
  - **Methods**: Search existing corpora + targeted supplementation
  - **Command**: `python scripts/expansion_pipeline.py --phase institutional --week 4`

### **Phase 1C**: Quality Validation (Post-Expansion)
- Content authenticity verification
- Temporal balance assessment
- PDAF dimension coverage validation
- Strategic tension analysis readiness

### **Phase 2**: Analysis Execution (Only After Expansion)
- Phased PDAF v10.0 analysis
- Strategic tension mathematics validation
- Longitudinal evolution tracking
- Comparative context analysis

### **Phase 3**: Results Integration
- Synthesis report generation
- Methodological limitations disclosure
- Research implications articulation

## ✅ REVISED SUCCESS CRITERIA

### **Minimum Viable Corpus (Pre-Analysis)**
- **Presidential Governance**: 25+ documents (vs. current 12)
- **Business Era Content**: 15+ documents (vs. current 6)
- **Institutional Context**: 20+ documents (vs. current 3)
- **Direct Communication**: 15+ documents (vs. current 0)
- **Total Target**: 180+ documents across balanced phases

### **PDAF v10.0 Compliance**
- **Strategic Tension Validity**: Mathematically sound AND substantively meaningful
- **Context Representation**: Campaign vs. governance populism distinguishable
- **Temporal Evolution**: Authentic change measurement possible
- **Methodological Transparency**: Coverage limitations explicitly documented

### **Research Integrity**
- **Balanced Analysis Corpus**: No phase >40% of total content
- **Provenance Tracking**: All content sources verified and documented
- **Adversarial Review Response**: Critical gaps addressed or justified
- **Peer Review Ready**: Methodological concerns preemptively addressed

## ⚠️ EXECUTION BLOCKERS

### **Pre-Analysis Requirements**
- Presidential governance content expansion (Priority 1)
- Business era baseline establishment (Priority 2)
- Institutional context representation (Priority 3)
- Direct communication inclusion (Priority 4)

### **Quality Gates**
- **Gate 1**: 150+ documents with governance representation
- **Gate 2**: PDAF dimension coverage validation
- **Gate 3**: Strategic tension analysis readiness
- **Gate 4**: Adversarial review concerns addressed

## 🎯 EXPANSION STRATEGY

### **Immediate Priorities (Next 2 Weeks)**
1. **Complete State of the Union Series** (2017-2021)
2. **Major Foreign Policy Addresses** (NATO, Middle East, China)
3. **Crisis Response Communication** (COVID, January 6, impeachment)
4. **Economic Policy Rhetoric** (tax reform, trade deals)

### **Medium-term Goals (Weeks 3-4)**
1. **Business Era Content** (1980s-2000s interviews, books)
2. **Social Media Integration** (key tweet threads, Truth Social)
3. **Debate Transcripts** (primary and general election)
4. **Press Conference Content** (unfiltered Q&A)

### **Long-term Enhancement (Post-Analysis)**
1. **Cabinet Meeting Rhetoric** (policy implementation)
2. **Congressional Hearing Responses** (Supreme Court nominations)
3. **Private Communication** (where ethically appropriate)
4. **International Summit Addresses** (G7, bilateral meetings)

---

**STATUS**: **EXPANSION REQUIRED** - Analysis execution blocked until coverage gaps addressed
**NEXT STEP**: Begin systematic corpus expansion following prioritized roadmap
