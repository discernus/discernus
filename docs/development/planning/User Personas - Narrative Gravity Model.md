# User Personas - Narrative Gravity Model

#personal/writing/narrativegravity
---

## Persona 1: Dr. Sarah Chen, Validation Researcher  

**Profile**  
• Associate Professor of Political Communication at a mid-tier research university  
• 8 years post-PhD, working toward tenure  

**Background & Context**  
• Specializes in computational political discourse analysis  
• Uses content-analysis and basic sentiment tools  
• Moderate Python comfort (runs scripts, but not a developer)  
• Needs 2–3 publications in 18 months; wary of black-box AI  

**Goals & Motivations**  
1. Co-author a methodologically rigorous paper  
2. Access novel analytical tools for ongoing projects  
3. Train graduate students in reproducible text analysis  

**Pain Points & Frustrations**  
• “How do I know this isn’t just dressed-up sentiment analysis?”  
• Reproducibility anxiety for students  
• Skepticism from tenure reviewers  

**Technical Requirements**  
• Raw results export in CSV/JSON (SPSS/R compatible)  
• Confidence intervals, inter-rater and inter-LLM reliability metrics  
• Detailed methodology documentation  

**User Journey Story**  
Fresh back from a conference, Sarah visits the platform URL. In 2 hours she:  
1. Reads the methodology draft and variance data  
2. Downloads CSV of Trump 2025 vs. Lincoln 1865 analyses  
3. Tests the “Demo Analysis” on Obama’s 2008 speech  
4. Reviews validation-study design (48 h framework separation, randomization)  
5. Screenshots key findings and schedules a lunch to plan a pilot study  

**Success Metrics**  
• Publication in a top-tier journal  
• Framework cited by peers  
• Graduate-student replication of her pilot study  

---

## Persona 2: Marcus Rodriguez, Media Analyst  

**Profile**  
• Senior Political Reporter for a major metropolitan newspaper  
• 15 years covering campaigns, debates, and policy  

**Background & Context**  
• Relies on sentiment trackers and manual fact-checks  
• Low-to-moderate technical comfort (web tools OK; CLI no)  
• Deadlines often require analysis within 2–4 hours  

**Goals & Motivations**  
1. Publish data-backed analysis that stands out  
2. Educate readers on deeper rhetorical patterns  
3. Build a signature analytical brand  

**Pain Points & Frustrations**  
• Speed vs. depth under tight deadlines  
• Explaining AI methods to skeptical editors/readers  
• Need quotes illustrating each score (e.g., “fear-mongering passages”)  

**Technical Requirements**  
• 30 min end-to-end analysis  
• Visualizations and excerpted quotes for each high-score dimension  
• One-click CSV/JSON export, plus plain-English summaries  

**User Journey Story**  
Covering the State of the Union, Marcus:  
1. Pastes transcript into the web UI  
2. Selects three frameworks (CV, MRP, PS) and clicks “Run”  
3. Drafts his article while the 20-min analysis runs  
4. Receives scores + 3–5 exemplary quotes per high-score dimension  
5. Compares results to Obama 2012 and Reagan 1984 via sidebar  
6. Submits his piece with embedded charts and attributions  

**Success Metrics**  
• Article engagement and social-media shares  
• Editor praise for unique analytical depth  
• Other journalists asking for his methodology  

---

## Persona 3: Dr. Elena Vasquez, Framework Developer  

**Profile**  
• PhD in Literature, digital humanities researcher & consultant  
• 5 years in computational text analysis, strong Python skills  

**Background & Context**  
• Analyzes corporate ESG reports, social movements, historical texts  
• Builds NLP pipelines but seeks faster platform foundations  
• Runs a consulting practice for NGOs and think tanks  

**Goals & Motivations**  
1. Extend the core model with domain-specific frameworks  
2. Prove methodological soundness to clients and peers  
3. Contribute extensions to an open repository  

**Pain Points & Frustrations**  
• Reinventing low-level analysis code is time-consuming  
• Validating new frameworks without built-in testing tools  
• Needing transparent access to core algorithms  

**Technical Requirements**  
• JSON schema for defining new gravity wells and weights  
• Access to coordinate-calculation code and prompt templates  
• Test harness for inter-LLM validation on custom corpora  
• API endpoints for programmatic integration  

**User Journey Story**  
Elena needs to analyze corporate sustainability reports:  
1. Clones repo and reviews core JSON Schemas  
2. Designs “Environmental Commitment” framework (action vs. gesture, accountability vs. primacy, etc.)  
3. Uses CLI tool to convert 50 reports into JSONL with semantic chunking  
4. Runs multi-LLM validation via Hugging Face integration  
5. Refines weights based on variance results  
6. Publishes her framework extension and wins a new consulting contract  

**Success Metrics**  
• Adoption of her framework by other researchers  
• Citations in academic and industry reports  
• Increased consulting revenue from proprietary analysis services  

---

## Persona 4: You, Independent Research Author

**Profile**  
• Non-developer, non-academic independent researcher  
• Focus on getting a rigorous academic paper published on narrative analysis methodology
• Limited technical background but strong conceptual and analytical thinking

**Background & Context**  
• Working independently outside traditional academic or corporate structures
• Relies on AI-assisted development tools (Cursor) for technical implementation
• Strong interest in political discourse analysis and moral framework development
• Operating on limited budget for validation phase (~$2,500)

**Goals & Motivations**  
1. **Primary Goal**: Complete and publish a peer-reviewed academic paper on Narrative Gravity Maps methodology
2. Establish credibility for the framework through rigorous validation studies  
3. Build a research tool that can generate reproducible, statistically sound results
4. Protect intellectual property while enabling appropriate academic collaboration

**Pain Points & Frustrations**  
• **Paper draft management**: Need to track versions and ensure latest draft is always accessible
• **Validation anxiety**: Ensuring the methodology meets academic publication standards without formal institutional support
• **Technical dependency**: Relying on AI assistance for implementation while maintaining research integrity
• **Time pressure**: Balancing thorough validation with publication timeline goals
• **Peer review concerns**: Anticipating skepticism about AI-assisted research from traditional academics

**Technical Requirements**  
• **Paper management system**: Version control and backup for research drafts  
• **Validation tools**: Statistical analysis capabilities for inter-rater reliability, LLM consistency testing
• **Data export**: Academic-format outputs (CSV, JSON) compatible with statistical software
• **Reproducibility package**: Complete methodology documentation and replication materials
• **Admin interface**: Simple UI for managing validation studies without coding

**User Journey Story: LLM Validation Experimentation Cycle**  

**Phase 1: Experiment Design**  
The Independent Researcher starts a new validation study by opening the research workbench. Today's goal: test whether the Civic Virtue Framework shows consistent cross-LLM results on presidential inaugural addresses.

1. **Text Corpus Assembly**: Selects 12 presidential inaugural addresses spanning 1861-2021, entering rich metadata for each (speaker, date, historical context, audience, word count). Notes that Lincoln's 1865 address was delivered to a war-weary nation while Biden's 2021 was to a deeply polarized electorate.

2. **Framework Configuration**: Creates three framework variants to test sensitivity:
   - Standard Civic Virtue (current weights: Identity 1.0, Principles 0.8, Moderators 0.6)
   - Equal-weighted version (all dipoles weighted 1.0) 
   - Enhanced-pragmatism version (pragmatism weight increased to 0.8)

3. **Prompt Template Iteration**: Tests three prompt approaches:
   - Standard template with explicit 0-1 scoring requirements
   - Enhanced template with historical context instructions
   - Minimal template to test baseline LLM interpretation

4. **LLM Configuration**: Selects GPT-4, Claude-3-Sonnet, and Mistral-Large with 3 runs each for statistical reliability (27 total analyses per framework-prompt combination).

**Phase 2: Experiment Execution & Monitoring**  
5. **Batch Execution**: Launches the experiment suite (324 total LLM calls) with randomized execution order. Monitors real-time progress, cost tracking ($23.45 estimated), and preliminary fit assessments.

6. **Framework Fit Alerts**: Receives notification that Shakespeare's Sonnet 18 (test case) shows poor framework fit (0.23 score) with explanation: "Political discourse analysis framework not appropriate for romantic poetry." Confirms the fit detection system is working.

7. **Early Results Review**: After 45 minutes, reviews interim results showing Lincoln 1865 achieving 0.94 cross-LLM correlation on dignity scores, with supporting passages properly identified: "With malice toward none, with charity for all..."

**Phase 3: Deep Analysis & Evidence Building**  
8. **Consensus Analysis**: Examines cross-LLM correlation matrices showing overall 0.91 agreement across models, with dignity and justice dimensions most consistent (0.94+ correlation) and pragmatism showing more variance (0.87 correlation).

9. **Evidence Exploration**: Drills down into individual analyses, reviewing LLM explanations for scoring decisions. Notes that all three models consistently identify Lincoln's "bind up the nation's wounds" as high-dignity rhetoric, with coherent supporting explanations.

10. **Metadata Pattern Analysis**: Discovers that post-1960 speeches show systematically higher tribalism scores (0.34 avg vs 0.12 for pre-1960), with statistical significance (p=0.003). Documents this as a potential historical trend worthy of academic investigation.

11. **Framework Sensitivity Testing**: Compares results across the three framework weight configurations, finding that core positioning remains stable (position variance <0.05) but narrative elevation shows meaningful differences when pragmatism is weighted higher.

**Phase 4: Validation Evidence Synthesis**  
12. **Confidence Assessment**: Reviews the evidence portfolio: 91% cross-LLM correlation, stable framework positioning, coherent evidence passages, and systematic metadata patterns. Feels confident enough to draft methodology claims for the academic paper.

13. **Academic Export**: Generates publication-ready CSV files with all raw scores, correlation matrices, and supporting passage evidence. Exports R-compatible statistical analysis scripts showing significance tests and confidence intervals.

14. **Documentation Update**: Updates the paper's methodology section with new statistical findings, including tables of inter-LLM reliability and framework fit assessments. Adds footnote about historical tribalism trends as supporting evidence for framework validity.

15. **Experimental Archive**: Saves the complete experiment configuration and results as "Presidential_Inaugural_Validation_v1.0" for future replication and extension studies.

**Evening Reflection**: Reviews the day's evidence generation, noting that systematic validation through the workbench produced far more rigorous results than manual testing. Plans tomorrow's experiment: testing framework performance on synthetic narratives with known moral characteristics as additional validation evidence.

**Success Metrics**  
• **Primary**: Successful submission and acceptance of peer-reviewed paper
• **Secondary**: Framework citations by independent researchers  
• **Validation**: Statistical reliability metrics meet academic standards (>0.90 correlation)
• **Impact**: Recognition in computational social science and political analysis communities
• **Sustainability**: Framework adoption enables ongoing research collaboration opportunities  

---

## Persona 5: Jessica Park, Casual User  

**Profile**  
• Public-policy graduate student and engaged citizen  
• Active on social media, volunteers in local campaigns  

**Background & Context**  
• Consumes multiple news sources and podcasts  
• High consumer-tech comfort; low domain expertise  
• Limited time—seeks quick, trustworthy insights  

**Goals & Motivations**  
1. Understand why rhetoric feels persuasive or manipulative  
2. Make informed voting decisions and discuss politics confidently  
3. Share credible analysis with friends and family  

**Pain Points & Frustrations**  
• Overwhelmed by complex political messaging  
• Unsure how to separate partisan spin from substantive argument  
• Intimidated by academic jargon and statistical output  

**Technical Requirements**  
• Mobile-friendly web UI with one-click “Analyze”  
• Results in plain English, 1–2 min turnaround  
• Charts with embedded excerpt quotes for context  
• One-click social-media sharing of analysis  

**User Journey Story**  
After seeing a journalist’s tweet, Jessica:  
1. Clicks link, pastes a recent campaign-ad transcript  
2. Waits 90 sec for CV/MRP/PS scores + 3 fear-related quotes  
3. “So that’s why it felt manipulative!” she thinks  
4. Shares a screenshot on Instagram Stories with a brief caption  
5. At her next volunteer meeting, she walks peers through the tool  

**Success Metrics**  
• Weekly return visits and shared analyses  
• Friends and family use her insights in discussions  
• Increased confidence in identifying manipulative rhetoric  

---

*These personas guide the design and prioritization of our Milestone 1 infrastructure—and set the stage for Milestones 2 and 3, where academic replication, public-facing tools, and broader adoption come into play.*  

