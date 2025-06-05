# User Stories: Narrative Gravity Wells Framework v2.0

These narratives illustrate real-world usage scenarios and help identify workflow improvements.

## Story 1: Testing the 5-Dipole Framework with Custom Persuasive Narratives

**User Profile:** Dr. Sarah Chen, Political Science Professor
**Goal:** Analyze moral appeals in 2024 campaign speeches using the established framework
**Materials:** Collection of recent political speeches (Biden, Trump, RFK Jr.)

### Step-by-Step Workflow

#### Phase 1: Setup and Familiarization
1. **Clone/Download Framework**
   ```bash
   git clone [repository]
   cd moral_gravity_analysis
   pip install -r requirements.txt
   ```

2. **Understand Current Framework**
   - Reads `README.md` for overview
   - Examines `frameworks/moral_foundations/README.md` for theoretical basis
   - Reviews existing analyses in `model_output/` for examples

3. **Verify System Status**
   ```bash
   python framework_manager.py summary
   ```
   - Confirms moral_foundations framework is active
   - Validates framework integrity

#### Phase 2: Prompt Generation and LLM Analysis
4. **Generate Analysis Prompt**
   ```bash
   python generate_prompt.py --output prompts/my_research/campaign_2024.txt
   ```
   **Pain Point:** *Wants to customize prompt for political speeches specifically - needs campaign-focused language cues*

5. **Prepare Text Samples**
   - Manually extracts key speech excerpts (500-1000 words each)
   - **Missing Feature:** *Batch text preparation tool*

6. **LLM Analysis Workflow**
   - Opens ChatGPT/Claude with generated prompt
   - Pastes first speech excerpt
   - Saves JSON response as `biden_state_union_2024.json`
   - Repeats for each speech
   - **Pain Point:** *Manual copy-paste workflow is tedious for large datasets*

#### Phase 3: Visualization and Analysis
7. **Generate Individual Visualizations**
   ```bash
   python narrative_gravity_elliptical.py model_output/biden_state_union_2024.json
python narrative_gravity_elliptical.py model_output/trump_rally_michigan_2024.json
python narrative_gravity_elliptical.py model_output/rfk_announcement_2024.json
   ```

8. **Comparative Analysis**
   ```bash
   python narrative_gravity_elliptical.py \
     model_output/biden_state_union_2024.json \
     model_output/trump_rally_michigan_2024.json \
     model_output/rfk_announcement_2024.json
   ```

9. **Interpretation and Documentation**
   - Analyzes patterns across candidates
   - Documents findings in research paper
   - **Missing Feature:** *Automated report generation with key metrics*

#### Phase 4: Validation and Peer Review
10. **Share Results with Colleagues**
    - **Pain Point:** *No easy way to package analysis for sharing*
    - **Missing Feature:** *Export functionality for academic presentation*

11. **Reproduce Analysis**
    - Colleague attempts to replicate findings
    - **Gap:** *Version tracking could be clearer for reproducibility*

### Identified Needs
- **Campaign-specific prompt templates**
- **Batch text processing tools**  
- **LLM API integration** (reduce manual workflow)
- **Automated report generation**
- **Analysis packaging/export tools**
- **Better reproducibility documentation**

---

## Story 2: Creating a Custom Environmental Ethics Framework

**User Profile:** Dr. Marcus Rodriguez, Environmental Policy Researcher  
**Goal:** Develop framework for analyzing climate policy communications
**Research Question:** How do environmental narratives appeal to different moral foundations?

### Step-by-Step Workflow

#### Phase 1: Conceptual Framework Design
1. **Literature Review and Theory Development**
   - Studies existing environmental ethics literature
   - Identifies 4 key dipoles for environmental discourse:
     - **Stewardship** vs **Exploitation**
     - **Precaution** vs **Progress** 
     - **Collective** vs **Individual**
     - **Intergenerational** vs **Present-focused**

2. **Framework Validation with Experts**
   - Shares conceptual framework with colleagues
   - **Missing Feature:** *Dipole validation checklist/tool*

#### Phase 2: Technical Implementation
3. **Create Framework Directory**
   ```bash
   mkdir -p frameworks/environmental_ethics
   ```

4. **Define Conceptual Framework**
   - Creates `frameworks/environmental_ethics/dipoles.json`
   - **Pain Point:** *No template or schema validation during creation*
   - **Workflow Gap:** *Must manually ensure all required fields present*

5. **Define Mathematical Framework**  
   - Creates `frameworks/environmental_ethics/framework.json`
   - **Challenge:** *Choosing optimal well angles and weights without guidance*
   - **Missing Feature:** *Visual framework designer tool*

6. **Framework Validation**
   ```bash
   python framework_manager.py validate environmental_ethics
   ```
   - **Good:** *Catches structural issues early*

#### Phase 3: Testing and Refinement
7. **Activate New Framework**
   ```bash
   python framework_manager.py switch environmental_ethics
   ```

8. **Generate Initial Prompt**
   ```bash
   python generate_prompt.py --output prompts/environmental_ethics/v1.0/interactive.txt
   ```

9. **Test with Sample Texts**
   - Analyzes sample environmental texts
   - **Discovery:** *Some language cues too narrow, others too broad*
   - **Iteration Need:** *Framework refinement based on initial results*

10. **Refine Framework**
    - Updates `dipoles.json` with better language cues
    - Adjusts weights in `framework.json` based on test results
    - **Pain Point:** *No systematic approach to weight optimization*

#### Phase 4: Comparative Validation
11. **Compare Against Moral Foundations**
    ```bash
    # Analyze same text with both frameworks
    python framework_manager.py switch moral_foundations
    python narrative_gravity_elliptical.py climate_speech.json --output moral_foundations_result.png
    
    python framework_manager.py switch environmental_ethics  
    python narrative_gravity_elliptical.py climate_speech.json --output environmental_ethics_result.png
    ```
    **Missing Feature:** *Side-by-side framework comparison tool*

12. **Statistical Validation**
    - Tests framework on corpus of environmental texts
    - **Gap:** *No built-in statistical analysis tools*
    - **Need:** *Reliability and validity metrics*

#### Phase 5: Documentation and Sharing
13. **Document Framework**
    - Creates `frameworks/environmental_ethics/README.md`
    - **Template Missing:** *No standard framework documentation template*

14. **Prepare for Publication**
    - **Missing Feature:** *Academic citation format generator*
    - **Gap:** *No systematic methodology documentation*

15. **Share with Research Community**
    - **Pain Point:** *No central framework repository or sharing mechanism*

### Identified Needs
- **Framework creation wizard/template**
- **Visual framework designer** (drag-and-drop well positioning)
- **Weight optimization tools** (data-driven suggestions)
- **Side-by-side framework comparison visualization**
- **Statistical validation suite** (reliability, validity tests)
- **Framework documentation templates**
- **Academic export functionality** (citations, methodology)
- **Framework sharing/repository system**
- **Automated A/B testing** for framework variations

---

## Cross-Cutting Feature Needs

### Workflow Improvements
1. **LLM API Integration**
   - Direct integration with OpenAI, Anthropic, Google APIs
   - Batch processing capabilities
   - Cost estimation and tracking

2. **Data Management**
   - Text corpus organization tools
   - Analysis result database
   - Version control for frameworks

3. **Visualization Enhancements**
   - Interactive web visualizations
   - Animated framework comparisons
   - Customizable chart themes

4. **Collaboration Features**
   - Framework sharing mechanisms
   - Peer review workflows
   - Multi-user analysis projects

5. **Academic Integration**
   - Citation generation
   - Statistical analysis suite
   - Publication-ready exports
   - Reproducibility packages

### Next Priority Features
Based on these user stories, the highest-impact additions would be:

1. **Framework Creation Wizard** - Streamline custom framework development
2. **LLM API Integration** - Eliminate manual copy-paste workflows  
3. **Comparative Analysis Tools** - Side-by-side framework visualization
4. **Statistical Validation Suite** - Academic rigor for framework development
5. **Academic Export Tools** - Publication and sharing functionality

These user stories reveal that while the technical foundation is solid, significant workflow automation and academic integration features would dramatically improve researcher experience and adoption. 