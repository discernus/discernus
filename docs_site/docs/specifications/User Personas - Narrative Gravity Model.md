# User Personas - Discernus Platform

#discernus #personas #mvp-strategy
---

## MVP Priority Classification

### 🎯 **MVP Critical (Phase 1)**
- **Persona 1**: Dr. Sarah Chen, Validation Researcher
- **Persona 4**: Independent Research Author (Platform Developer)
- **Persona 6**: Dr. Jonathan Haidt, Framework Originator (NEW)

### 📊 **Phase 2: Expert Consultation**
- **Persona 3**: Dr. Elena Vasquez, Framework Developer

### 🌐 **Phase 3: General Platform**
- **Persona 2**: Marcus Rodriguez, Media Analyst
- **Persona 5**: Jessica Park, Casual User

---

## Persona 1: Dr. Sarah Chen, Validation Researcher [MVP CRITICAL]

**Profile**  
• Associate Professor of Political Communication at a mid-tier research university  
• 8 years post-PhD, working toward tenure  

**Background & Context**  
• Specializes in computational political discourse analysis  
• Uses content-analysis and basic sentiment tools  
• Moderate Python comfort (runs scripts, but not a developer)  
• Needs 2–3 publications in 18 months; wary of black-box AI  
• **MVP Context**: Ideal collaborator for Moral Foundations Theory validation studies

**Goals & Motivations**  
1. Co-author a methodologically rigorous paper using established frameworks
2. Access validated analytical tools (MFT, Political Framing Theory) for ongoing projects  
3. Train graduate students in reproducible text analysis with proven frameworks

**Pain Points & Frustrations**  
• "How do I know this isn't just dressed-up sentiment analysis?"  
• Need validation against established measures (MFQ-30, framing studies)
• Reproducibility anxiety for students  
• Skepticism from tenure reviewers about novel computational methods

**Technical Requirements**  
• **Validation Evidence**: Correlation with MFQ-30, inter-rater reliability with expert human coding
• Raw results export in CSV/JSON (SPSS/R compatible)  
• Confidence intervals, inter-rater and inter-LLM reliability metrics  
• Detailed methodology documentation referencing established literature

**User Journey Story**  
Fresh back from a conference, Sarah visits the Discernus platform. In 2 hours she:  
1. Reads the MFT implementation methodology and validation against MFQ-30 (r=0.83)
2. Downloads CSV of Trump 2024 vs. Obama 2008 MFT analyses with confidence intervals
3. Tests the "Demo Analysis" on Biden's 2021 inaugural using Moral Foundations Theory
4. Reviews validation study design (expert consultation with Haidt lab, cross-LLM reliability)
5. Screenshots key findings showing 0.91 inter-LLM correlation and schedules lunch to plan collaboration

**Success Metrics**  
• Publication in computational social science journal featuring Discernus methodology
• Framework validation cited by peers  
• Graduate-student replication of MFT studies using Discernus

---

## Persona 2: Marcus Rodriguez, Media Analyst [PHASE 3]

**Profile**  
• Senior Political Reporter for a major metropolitan newspaper  
• 15 years covering campaigns, debates, and policy  

**Background & Context**  
• Relies on sentiment trackers and manual fact-checks  
• Low-to-moderate technical comfort (web tools OK; CLI no)  
• Deadlines often require analysis within 2–4 hours  
• **Note**: General platform user, not MVP priority

**Goals & Motivations**  
1. Publish data-backed analysis using established academic frameworks
2. Educate readers on deeper rhetorical patterns (MFT, framing analysis)
3. Build a signature analytical brand  

**Pain Points & Frustrations**  
• Speed vs. depth under tight deadlines  
• Explaining computational methods to skeptical editors/readers  
• Need quotes illustrating each framework dimension (e.g., "care/harm passages")

**Technical Requirements**  
• 30 min end-to-end analysis using established frameworks
• Visualizations and excerpted quotes for each framework dimension
• One-click CSV/JSON export, plus plain-English summaries  

**User Journey Story**  
Covering the State of the Union, Marcus:  
1. Pastes transcript into the web UI  
2. Selects Moral Foundations Theory and Political Framing Theory frameworks
3. Drafts his article while the 20-min analysis runs  
4. Receives MFT scores + 3–5 exemplary quotes per foundation dimension
5. Compares framing results to previous presidential addresses via historical database
6. Submits piece with embedded charts showing care/harm vs. authority/loyalty patterns

**Success Metrics**  
• Article engagement and social-media shares  
• Editor praise for unique analytical depth grounded in academic frameworks
• Other journalists requesting access to established framework analysis

---

## Persona 3: Dr. Elena Vasquez, Framework Developer [PHASE 2]

**Profile**  
• PhD in Literature, digital humanities researcher & consultant  
• 5 years in computational text analysis, strong Python skills  

**Background & Context**  
• Analyzes corporate ESG reports, social movements, historical texts  
• Builds NLP pipelines but seeks faster platform foundations  
• Runs a consulting practice for NGOs and think tanks  
• **MVP Context**: Potential contributor after platform validates established frameworks

**Goals & Motivations**  
1. Extend Discernus with domain-specific frameworks after core validation complete
2. Prove methodological soundness to clients using established framework validation
3. Contribute framework extensions to validated repository  

**Pain Points & Frustrations**  
• Need confidence that platform methodology is academically sound before building on it
• Reinventing low-level analysis code is time-consuming  
• Validating new frameworks without built-in testing infrastructure
• Needing transparent access to core algorithms  

**Technical Requirements**  
• Evidence of validation against established measures (MFT, framing theory, cultural theory)
• JSON schema for defining new frameworks following established patterns
• Access to coordinate-calculation code and validated prompt templates  
• Test harness for inter-LLM validation on custom corpora following Discernus protocols

**User Journey Story**  
Elena needs to analyze corporate sustainability reports after Discernus validates core frameworks:  
1. Reviews published validation studies showing MFT correlation with MFQ-30 (r=0.83)
2. Clones repo and reviews validated framework JSON schemas (MFT, Political Framing)
3. Designs "Corporate Environmental Commitment" framework following validated patterns
4. Uses established CLI validation tools to test on sustainability report corpus
5. Runs multi-LLM validation following Discernus protocols with confidence intervals
6. Publishes framework extension with validation evidence and wins consulting contract

**Success Metrics**  
• Adoption of her framework by other researchers building on Discernus validation
• Citations in academic and industry reports referencing Discernus methodology
• Increased consulting revenue from validated analysis services  

---

## Persona 4: Independent Research Author [MVP CRITICAL]

**Profile**  
• Non-developer, non-academic independent researcher  
• Focus on establishing Discernus as validated computational methodology for academic publication
• Limited technical background but strong conceptual and analytical thinking

**Background & Context**  
• Working independently outside traditional academic or corporate structures
• Relies on AI-assisted development tools (Cursor) for technical implementation
• Strong interest in computational social science methodology and framework validation
• Operating on validation budget (~$2,500) for MFT correlation studies

**Goals & Motivations**  
1. **Primary Goal**: Establish Discernus credibility through rigorous validation against established measures
2. Complete peer-reviewed academic paper on computational framework comparison methodology
3. Build validated research infrastructure that generates reproducible, statistically sound results
4. Secure expert endorsement from framework originators (Haidt lab, political communication scholars)

**Pain Points & Frustrations**  
• **Validation pressure**: Ensuring methodology meets academic standards for established frameworks
• **Expert consultation**: Need approval from framework originators without institutional affiliation
• **Technical dependency**: Relying on AI assistance while maintaining research integrity
• **Publication standards**: Meeting computational social science validation requirements
• **Resource constraints**: Limited budget for comprehensive validation studies

**Technical Requirements**  
• **Validation Infrastructure**: Correlation studies with MFQ-30, expert human coding comparison
• **Expert Consultation Tools**: Framework implementation review and approval workflows
• **Statistical Analysis**: Inter-rater reliability, cross-LLM consistency, confidence intervals
• **Academic Output**: Publication-ready methodology documentation and replication packages
• **Database Management**: Systematic storage of validation results and expert feedback

**User Journey Story: MFT Validation Study**  

**Phase 1: Expert Consultation Setup**  
1. **Framework Implementation**: Implements Moral Foundations Theory using validated MFT lexicons and MFQ-30 operational definitions
2. **Expert Outreach**: Contacts Haidt lab requesting implementation review and validation consultation
3. **Implementation Review**: Submits detailed framework operationalization for expert evaluation
4. **Feedback Integration**: Incorporates expert suggestions on lexical markers and scoring protocols

**Phase 2: Validation Study Design**  
5. **Study Protocol**: Designs MFT validation study comparing Discernus outputs to MFQ-30 responses (n=500)
6. **Cross-LLM Testing**: Configures multi-model validation (GPT-4, Claude, Gemini) with 3 runs each
7. **Human Comparison**: Sets up expert human coding subset for inter-rater reliability assessment
8. **Statistical Planning**: Defines success criteria (r>0.8 with MFQ, inter-LLM correlation >0.9)

**Phase 3: Validation Execution & Analysis**  
9. **Data Collection**: Executes validation study with systematic randomization and quality controls
10. **Statistical Analysis**: Analyzes correlation results, confidence intervals, and reliability metrics
11. **Expert Review**: Submits validation results to Haidt lab for final approval
12. **Academic Documentation**: Prepares methodology section with validation evidence and expert endorsement

**Success Metrics**  
• **Validation Success**: Achieve r>0.8 correlation with MFQ-30 across all foundation dimensions
• **Expert Endorsement**: Formal approval from Jonathan Haidt and collaborators
• **Publication**: Acceptance in computational social science journal
• **Academic Impact**: Citations by independent researchers using validated methodology
• **Community Adoption**: Platform usage by computational social science researchers

---

## Persona 5: Jessica Park, Casual User [PHASE 3]

**Profile**  
• Public-policy graduate student and engaged citizen  
• Active on social media, volunteers in local campaigns  

**Background & Context**  
• Consumes multiple news sources and podcasts  
• High consumer-tech comfort; low domain expertise  
• Limited time—seeks quick, trustworthy insights  
• **Note**: Consumer user, not relevant for MVP validation phase

**Goals & Motivations**  
1. Understand political rhetoric through established academic frameworks
2. Make informed voting decisions using validated analytical tools
3. Share credible analysis grounded in academic research with friends and family  

**Pain Points & Frustrations**  
• Overwhelmed by complex political messaging  
• Unsure how to separate partisan spin from substantive argument  
• Need simple explanations of academic framework results

**Technical Requirements**  
• Mobile-friendly web UI with validated framework options (MFT, Political Framing)
• Results in plain English explaining framework dimensions, 1–2 min turnaround  
• Charts with embedded excerpt quotes showing framework evidence
• Attribution to academic sources and validation studies

**User Journey Story**  
After learning about MFT from a psychology podcast, Jessica:  
1. Clicks Discernus link, pastes a recent campaign speech transcript
2. Selects "Moral Foundations Theory" based on podcast discussion
3. Waits 90 sec for MFT scores + supporting quotes for each foundation
4. "Now I understand the care/harm vs. loyalty/betrayal distinction!" she thinks
5. Shares screenshot with caption referencing Haidt's research validation
6. At volunteer meeting, explains how MFT analysis reveals campaign messaging strategies

**Success Metrics**  
• Weekly return visits using validated frameworks
• Friends and family adoption of academic framework concepts
• Increased sophistication in political discourse analysis using established theory

---

## Persona 6: Dr. Jonathan Haidt, Framework Originator [MVP CRITICAL - NEW]

**Profile**  
• Thomas Cooley Professor of Ethical Leadership at NYU Stern School of Business
• Originator of Moral Foundations Theory with 15+ years of validation research
• Co-founder of Heterodox Academy, author of "The Righteous Mind"

**Background & Context**  
• Leading expert in moral psychology and political psychology
• Extensive experience with MFT validation across cultures and contexts
• Committed to rigorous methodology and replication in social science
• **MVP Context**: Essential for MFT implementation validation and credibility

**Goals & Motivations**  
1. Ensure accurate computational implementation of Moral Foundations Theory
2. Advance rigorous methodology in computational social science
3. Facilitate broader adoption of validated MFT analysis tools
4. Maintain theoretical integrity while enabling technological innovation

**Pain Points & Frustrations**  
• Computational implementations often misrepresent or oversimplify MFT
• Need systematic validation against established MFT measures (MFQ-30)
• Concern about "black box" AI approaches lacking theoretical grounding
• Limited time for extensive consultation on every computational project

**Technical Requirements**  
• **Implementation Review**: Detailed documentation of MFT operationalization in computational form
• **Validation Evidence**: Statistical correlation with MFQ-30 and other established MFT measures  
• **Methodology Transparency**: Clear explanation of prompt templates, scoring algorithms, and aggregation methods
• **Expert Approval Process**: Efficient workflow for reviewing and endorsing implementation quality
• **Ongoing Collaboration**: Framework for continued consultation and refinement

**User Journey Story: MFT Implementation Review**  

**Phase 1: Initial Implementation Assessment**  
1. **Technical Review**: Examines Discernus MFT implementation documentation including lexical markers, prompt templates, and scoring protocols
2. **Validation Design**: Reviews proposed correlation study design comparing Discernus outputs to MFQ-30 responses
3. **Methodology Feedback**: Provides detailed feedback on implementation accuracy and suggests refinements
4. **Pilot Testing**: Reviews preliminary validation results on small sample (n=50) before full study

**Phase 2: Validation Study Oversight**  
5. **Study Approval**: Approves final validation study protocol (n=500) after incorporating feedback
6. **Results Review**: Analyzes correlation results (r=0.83 overall, ranging 0.78-0.89 across foundations)
7. **Statistical Assessment**: Evaluates inter-LLM reliability (r=0.91) and confidence intervals
8. **Boundary Testing**: Reviews performance on edge cases and diverse text types

**Phase 3: Academic Endorsement**  
9. **Final Approval**: Provides formal endorsement of Discernus MFT implementation following successful validation
10. **Methodology Paper**: Co-authors or reviews academic paper describing computational MFT methodology
11. **Community Recommendation**: Recommends Discernus to colleagues and graduate students for MFT research
12. **Ongoing Consultation**: Establishes framework for continued collaboration on MFT refinements

**Success Metrics**  
• **Implementation Quality**: Discernus MFT achieves >0.8 correlation with MFQ-30 across all foundations
• **Methodological Rigor**: Validation study meets standards for computational social science publication
• **Academic Impact**: Endorsed implementation enables new research using computational MFT analysis
• **Community Adoption**: Other MFT researchers adopt validated Discernus implementation
• **Theoretical Integrity**: Computational implementation maintains fidelity to original MFT framework

---

*These personas guide the development of Discernus with clear MVP priorities: establishing credibility through rigorous validation of established academic frameworks (MFT, Political Framing Theory, Cultural Theory) before expanding to general-purpose discourse analysis capabilities.*

