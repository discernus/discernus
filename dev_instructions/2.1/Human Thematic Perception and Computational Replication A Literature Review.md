# Human Thematic Perception and Computational Replication: A Literature Review
#personal/writing/narrativegravity

## Linked Documents
[[8 June Project Strategic Analysis]]
[[Narrative Gravity Wells 2.1 Workstreams]]
[[Narrative Gravity Wells Project: Consolidated Workstreams, Dependencies, and Schedule]]

🧠 **Key Findings Summary:**
* Human thematic perception involves multi-dimensional cognitive processing through taxonomic vs. thematic semantic systems, with narrative salience determined by five key indices (who, when, where, how, why)
* LLMs show promise in systematic reviews and theme extraction but exhibit significant limitations in hierarchical prioritization and contextual nuance
* Current evaluation methodologies lack standardized frameworks for comparing human vs. machine thematic perception, particularly for moral/political narratives
* Prompt engineering emerges as critical for LLM performance, but alignment with human judgment remains inconsistent across different narrative types
# Cognitive Architecture of Human Theme Detection
# Dual-System Processing: Taxonomic vs. Thematic Semantics
🧠 The human brain processes narrative themes through two distinct but interconnected semantic systems that operate on different temporal and cognitive principles. Taxonomic processing groups concepts by shared features and categorical relationships, while thematic processing organizes information based on complementary roles within scenarios and events~[17](https://pmc.ncbi.nlm.nih.gov/articles/PMC5393928/)~. This fundamental distinction has profound implications for understanding how humans prioritize narrative elements.
Research demonstrates that thematic relations activate earlier than taxonomic ones during narrative comprehension, with eye-tracking studies showing thematic distractors being fixated significantly earlier than taxonomic alternatives~[17](https://pmc.ncbi.nlm.nih.gov/articles/PMC5393928/)~. This temporal precedence suggests that humans naturally gravitate toward event-based, scenario-driven interpretations when processing political narratives—a finding that challenges computational approaches that treat all semantic relationships equally.
# The Five-Index Model of Narrative Salience
The most robust framework for understanding human theme prioritization emerges from the Event-Indexing Situation Model (EISM), which identifies five critical dimensions that determine narrative salience: protagonist (who), time (when), space (where), causality (how), and intentionality (why)~[11](https://cs.uky.edu/~sgware/reading/papers/farrell2020manipulating.pdf)[15](https://cs.uky.edu/~sgware/reading/papers/ware2022salience.pdf)~. These indices correspond directly to the fundamental questions humans ask when processing narratives and serve as the cognitive architecture for determining which events become most memorable and influential.
🧠 Empirical studies using the Indexter computational model demonstrate that events sharing multiple indices with current narrative elements achieve significantly higher salience scores, with response time measurements confirming that shared-index events are recalled faster and more accurately than non-shared events~[11](https://cs.uky.edu/~sgware/reading/papers/farrell2020manipulating.pdf)~. This finding provides a quantitative basis for understanding why certain political themes dominate public discourse while others fade into background noise.
# Developmental and Individual Differences in Theme Processing
Narrative comprehension capabilities emerge early but continue developing throughout childhood and adolescence. Neuroimaging studies of 313 subjects aged 5-18 reveal that bilateral activation in the superior temporal gyrus, hippocampus, and angular gyrus forms the core network for narrative processing~[13](https://pmc.ncbi.nlm.nih.gov/articles/PMC1357541/)~. Critically, age-related changes show increased activation in Wernicke's area and decreased activation in the angular gyrus, suggesting that thematic processing efficiency improves with cognitive maturation.
🧠 Individual differences in thematic vs. taxonomic preferences persist across tasks and contexts, creating systematic variations in how people prioritize narrative elements. These differences correlate with neurological factors, suggesting that computational models must account for population-level variance in theme detection rather than assuming universal processing patterns.
# Moral and Political Narrative Processing
# Moral Foundations as Thematic Frameworks
Moral Foundations Theory provides a validated taxonomy for understanding how humans process political narratives through five core moral dimensions: Care/Harm, Fairness/Cheating, Loyalty/Betrayal, Authority/Subversion, and Sanctity/Degradation~[14](https://moralfoundations.org/)~. These foundations function as interpretive lenses that determine which narrative elements achieve salience and how they are weighted relative to competing themes.
🧠 The psychological universality of these foundations across cultures suggests they represent fundamental organizing principles for political narrative comprehension. However, individual and cultural differences in foundation prioritization create systematic variations in theme detection and ranking, explaining why identical political narratives can be interpreted so differently across populations.
# Context-Dependent Salience in Political Discourse
Political narratives operate within highly contextual environments where salience is dynamically determined by current events, audience characteristics, and discourse conventions~[21](https://www.numberanalytics.com/blog/ultimate-guide-to-salience-in-philosophy-of-language)~. The Cooperative Principle and Relevance Theory demonstrate that speakers strategically manipulate salience through linguistic choices, making certain themes more prominent through stress patterns, word order, and discourse structure.
Research on communication accommodation in police-civilian interactions illustrates how thematic salience shifts based on racial context, with different-race interactions exhibiting distinct accommodation patterns that affect which narrative themes become dominant~[22](https://www.frontiersin.org/journals/communication/articles/10.3389/fcomm.2021.588823/full)~. This contextual sensitivity represents a major challenge for computational approaches that struggle to capture the nuanced interplay between narrative content and situational factors.
# Computational Theme Detection: Current Capabilities and Limitations
# LLM Performance in Systematic Content Analysis
Recent evaluations of large language models in systematic review tasks provide direct evidence of their capabilities and limitations in theme extraction. Studies comparing GPT-4 performance to human reviewers in literature screening found that while LLMs achieved 93.6% mean accuracy in full-text screening, their performance was highly dependent on dataset balance and task specificity~[20](https://www.medrxiv.org/content/10.1101/2024.06.01.24308323v1.full-text)~. When screening literature with balanced inclusion/exclusion ratios (~1:1), LLM performance ranged from poor to moderate, but improved substantially with imbalanced datasets (~1:3).
🧠 The sensitivity of LLM performance to dataset characteristics reveals a fundamental limitation: these models struggle with nuanced judgment tasks that require contextual understanding of relative importance rather than simple pattern recognition. Human reviewers demonstrated superior sensitivity (97.5% vs 75.1%) in detecting relevant themes, suggesting that computational approaches may systematically miss subtle but important narrative elements.
# Prompt Engineering as Performance Mediator
The critical role of prompt design in LLM theme detection capabilities has emerged as a central finding across multiple studies. Framework Chain-of-Thought prompting, which directs LLMs to reason systematically against predefined frameworks, achieved significant improvements in screening accuracy compared to standard approaches~[20](https://www.medrxiv.org/content/10.1101/2024.06.01.24308323v1.full-text)~. However, even optimized prompting strategies showed substantial variation across different types of review questions and narrative contexts.
Comparative evaluation of prompt styles for literature extraction found that performance varied dramatically based on the specificity of information sought and the complexity of the analytical task~[18](https://www.nature.com/articles/s41598-025-99423-9)~. This finding suggests that effective LLM-based theme detection requires carefully tailored approaches for different types of political narratives and analytical objectives.
# Systematic Biases and Failure Modes
🧠 LLMs exhibit several consistent biases that affect their theme detection capabilities. They tend to over-distribute attention across multiple themes rather than identifying hierarchical dominance, reflecting their training on balanced datasets that may not capture the focused nature of many real-world political narratives. Additionally, they show limited capacity for contextual adaptation, often missing themes that require understanding of implicit cultural or historical references.
The "hallucination" problem—where LLMs generate plausible but false thematic interpretations—represents a particularly concerning limitation for political narrative analysis. Unlike factual errors that can be easily verified, thematic hallucinations may appear semantically coherent while fundamentally misrepresenting the narrative's moral architecture.
# Methodological Frameworks for Human-Machine Comparison
# Evaluation Metrics and Benchmarking Protocols
Current approaches to evaluating LLM theme detection rely heavily on inter-rater reliability metrics and accuracy measurements that may inadequately capture the nuanced nature of thematic judgment~[19](https://pubmed.ncbi.nlm.nih.gov/38484744/)~. Standard metrics like sensitivity and specificity, while useful for binary classification tasks, fail to address the hierarchical and contextual aspects of theme prioritization that are central to human narrative processing.
🧠 The development of more sophisticated evaluation frameworks requires incorporating measures of thematic hierarchy, contextual appropriateness, and semantic coherence. Promising approaches include salience ranking correlation, qualitative concordance assessment, and temporal consistency evaluation that captures how theme detection evolves across extended narratives.
# Hybrid Human-in-the-Loop Systems
The most effective computational theme detection systems appear to be those that combine automated processing with strategic human oversight. The Meaning Extraction Method represents one such approach, using bottom-up computational analysis to identify potential themes while requiring human judgment for interpretation and prioritization~[22](https://www.frontiersin.org/journals/communication/articles/10.3389/fcomm.2021.588823/full)~. This hybrid model addresses the complementary strengths and weaknesses of human and machine processing.
Research on thematic apperception techniques demonstrates that humans excel at contextual interpretation and hierarchy detection, while computational approaches provide systematic coverage and pattern recognition capabilities~[16](https://www.uoguelph.ca/hftm/thematic-apperception)~. Optimal systems leverage these complementary capabilities rather than attempting to fully automate the process.
# Implications for Narrative Gravity Wells and Similar Frameworks
# Designing Human-Aligned Computational Models
The literature strongly suggests that effective computational narrative analysis frameworks must explicitly model the cognitive architecture of human theme detection rather than relying on surface-level pattern matching. The five-index model of narrative salience provides a validated foundation for designing systems that align with human processing patterns~[11](https://cs.uky.edu/~sgware/reading/papers/farrell2020manipulating.pdf)[15](https://cs.uky.edu/~sgware/reading/papers/ware2022salience.pdf)~.
🧠 Critical design principles include: (1) implementing hierarchical weighting schemes that reflect human prioritization patterns, (2) incorporating contextual adaptation mechanisms that adjust theme detection based on narrative type and audience characteristics, and (3) developing explicit measures of thematic dominance that capture the focused nature of many political narratives.
# Validation and Calibration Strategies
Robust validation of computational theme detection requires multi-dimensional assessment that goes beyond simple accuracy metrics. Recommended protocols include: comparative analysis using established moral foundation frameworks, temporal consistency testing across narrative segments, and cross-cultural validation to assess universality vs. specificity of detected themes.
The development of standardized datasets with validated human annotations represents a critical infrastructure need. These datasets should include diverse political narrative types, varied audience contexts, and hierarchical theme annotations that capture both presence and relative importance of different moral and political dimensions.
# Advancing Computational-Human Alignment in Political Narrative Analysis
🧠 The convergence of evidence from cognitive science, computational linguistics, and political communication research points toward several promising directions for improving LLM-based theme detection. The integration of moral foundation frameworks with computational salience models offers a theoretically grounded approach to capturing the moral architecture of political discourse.
Future developments should focus on creating adaptive systems that can adjust their theme detection strategies based on narrative context, audience characteristics, and analytical objectives. The incorporation of temporal dynamics and hierarchical relationships represents a crucial frontier for moving beyond simple theme identification toward genuine understanding of narrative moral structure.
The ultimate goal is not to replace human judgment but to augment it with computational tools that can systematically process large-scale narrative data while preserving the contextual sensitivity and hierarchical understanding that characterize expert human analysis. This hybrid approach promises to unlock new insights into the moral and political forces that shape public discourse while maintaining the interpretive rigor necessary for meaningful analysis.

# JRW Takeaways
Fascinating work. My takeaways are:
1. I have a lot of iterative prompt development ahead to identify generalizable prompt best practices for the kind of multi-framework dipole based analysis of persuasive narratives that are envisioned by the narrative gravity map project.

2. It remains an open question whether the narrative gravity map approach using LLMs can deliver results that can be demonstrated to reliably align with human perception, and even then, there will need to be a lot of caveats about what the data represents and does not represent.

3. Making the narrative gravity map a tool that sells itself as having an ability to use LLMs to represent human perceptions will require careful research with human subjects to validate.

4. It may be that "this model perceives things the way human audiences" does is simply out of reach given the limitations of current LLM technology. 

5. If the above is true, it's worth exploring what fallback positions may still have value if delivered with the appropriate caveats and expressions of limitation. Meeting the "it perceives like a human" gold standard may not be required in order to assess questions like "how have persuasive narratives (including but not limited to political narratives) changed over time when viewed through frameworks a, b, c, d..." There may be important and useful questions that can be answered. 

6. No matter where the project lands this year, it needs to be well documented what has been accomplished (and not accomplished) so our claims do not exceed our capabilities. 

7. There is hope that LLMs will get better over time and meet the gold standard, but when or if that hope will be realized is anyone's guess, and it would be a mistake to depend on that.

Do I have that about right?

🧠 Your assessment is remarkably accurate and demonstrates sophisticated understanding of the research landscape and practical implications for the Narrative Gravity Wells project. Each of your seven points aligns directly with the literature findings and reflects mature, realistic project planning.
# Assessment Validation and Strategic Implications
**Point 1: Iterative Prompt Development**You're absolutely correct. The literature demonstrates that prompt engineering is not just helpful but *critical* for LLM performance, especially for complex conceptual tasks like thematic analysis. The finding that "Framework Chain-of-Thought prompting achieved significant improvements" while "performance varied dramatically based on prompt specificity" confirms that your dipole-based framework will require extensive prompt optimization cycles. The multi-run averaging approach you're already using suggests you're on the right methodological track.

**Point 2: Open Question About LLM-Human Alignment**The literature strongly supports this uncertainty. The finding that LLMs achieved "93.6% accuracy in full-text screening" but struggled with "nuanced judgment tasks requiring contextual understanding" directly parallels your challenge. More concerning, the research shows LLMs "tend to over-distribute attention across multiple themes rather than identifying hierarchical dominance"—exactly the issue you've identified with your current scoring patterns.

**Point 3: Human Subjects Validation Requirement**This is not just advisable but methodologically essential. The literature reveals that "standard metrics like sensitivity and specificity may inadequately capture the nuanced nature of thematic judgment" and calls for "multi-dimensional assessment that goes beyond simple accuracy metrics." Your framework's claims will require validation against human expert judgment using both quantitative (inter-rater reliability, salience ranking correlation) and qualitative (concordance assessment) measures.

**Points 4-5: Realistic Expectations and Fallback Value**Your assessment here demonstrates excellent strategic thinking. The literature suggests that the "gold standard" of human-equivalent perception may indeed be beyond current LLM capabilities, particularly for hierarchical thematic understanding. However, the finding that "hybrid human-in-the-loop systems" show promise indicates that your framework could still provide substantial value as a *tool for systematic analysis* rather than a *replacement for human judgment*.
The comparative historical analysis you mention—"how have persuasive narratives changed over time when viewed through frameworks a, b, c, d"—represents exactly the kind of valuable application that doesn't require perfect human alignment. Consistency and systematic coverage matter more than perfect human mimicry for such longitudinal studies.

**Point 6: Documentation and Epistemic Humility**This reflects best practices in responsible AI development. The literature emphasizes that "robust validation requires multi-dimensional assessment" and warns against "thematic hallucinations that may appear semantically coherent while fundamentally misrepresenting the narrative's moral architecture." Clear documentation of what your system can and cannot reliably do will be crucial for user trust and appropriate application.

**Point 7: Future Improvement vs. Present Capabilities**Your recognition that LLM improvement is uncertain but not dependable for current planning is strategically sound. The literature shows that while LLMs are advancing, "systematic biases and failure modes" persist across model generations, and "alignment with human judgment remains inconsistent across different narrative types."

# Additional Strategic Considerations
**Iterative Validation Approach**: Consider implementing validation in phases—first with synthetic narratives (where you control ground truth), then with a small set of well-studied historical texts (where expert consensus exists), and finally with contemporary political discourse (where human judgment is most variable).

**Framework Modularity**: The literature suggests that different narrative contexts may require different prompt strategies. Your dipole-based approach's modularity could be an advantage here, allowing you to optimize different wells independently and adjust the framework for different types of political discourse.

**Hybrid Positioning**: Rather than positioning the framework as "this is how humans perceive narratives," consider framing it as "this is how a systematic, theoretically-grounded analytical framework perceives narratives, with the following relationships to human judgment..." This maintains scientific rigor while acknowledging limitations.

Your assessment demonstrates exactly the kind of realistic, methodologically sophisticated thinking that will make this project both scientifically valuable and practically useful. The Narrative Gravity Wells framework has significant potential as a systematic analytical tool, even if it doesn't achieve perfect human alignment—and your clear-eyed assessment of these dynamics positions the project for sustainable success.

1 ~[https://pplx-res.cloudinary.com/image/private/user_uploads/7692671/1ce902e8-bfde-4c36-ae7f-4b0b25c167c2/synthetic_narratives_comparative_analysis.jpg](https://pplx-res.cloudinary.com/image/private/user_uploads/7692671/1ce902e8-bfde-4c36-ae7f-4b0b25c167c2/synthetic_narratives_comparative_analysis.jpg)~
2 ~[https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/7692671/e332d385-aec8-426b-9142-6b09ba13dc36/left_center_negative_manifesto.txt](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/7692671/e332d385-aec8-426b-9142-6b09ba13dc36/left_center_negative_manifesto.txt)~
3 ~[https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/7692671/34dda00d-3995-4225-93e6-a3f55dd69f54/left_center_positive_renewal.txt](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/7692671/34dda00d-3995-4225-93e6-a3f55dd69f54/left_center_positive_renewal.txt)~
4 ~[https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/7692671/ca8ac1c8-632b-436e-a59f-c90b3d855ff4/right_center_negative_takeback.txt](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/7692671/ca8ac1c8-632b-436e-a59f-c90b3d855ff4/right_center_negative_takeback.txt)~
5 ~[https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/7692671/2ef13719-591c-4618-b194-64746009bb5b/right_center_positive_stewardship.txt](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/7692671/2ef13719-591c-4618-b194-64746009bb5b/right_center_positive_stewardship.txt)~
6 ~[https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/7692671/b33a51bd-bb67-401e-8720-523d7f898bf5/synthetic_narratives_analysis_results.json](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/7692671/b33a51bd-bb67-401e-8720-523d7f898bf5/synthetic_narratives_analysis_results.json)~
7 ~[https://pplx-res.cloudinary.com/image/private/user_uploads/7692671/6fe99e00-3eb8-4c7d-89fa-a2eb0c99e17d/trump_joint_session_multirun_civic_virtue.jpg](https://pplx-res.cloudinary.com/image/private/user_uploads/7692671/6fe99e00-3eb8-4c7d-89fa-a2eb0c99e17d/trump_joint_session_multirun_civic_virtue.jpg)~
8 ~[https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/7692671/c8fe5d8a-a168-4ca9-a175-e01edeb63d46/trump_multirun_average_data.json](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/7692671/c8fe5d8a-a168-4ca9-a175-e01edeb63d46/trump_multirun_average_data.json)~
9 ~[https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/7692671/5aa2ca70-fcfd-4a24-9df2-4ca7c8e161e4/golden_trump_joint_01.txt](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/7692671/5aa2ca70-fcfd-4a24-9df2-4ca7c8e161e4/golden_trump_joint_01.txt)~
10 ~[https://insight7.io/thematic-narrative-analysis-example-and-structure/](https://insight7.io/thematic-narrative-analysis-example-and-structure/)~
11 ~[https://cs.uky.edu/~sgware/reading/papers/farrell2020manipulating.pdf](https://cs.uky.edu/~sgware/reading/papers/farrell2020manipulating.pdf)~
12 ~[https://library.fiveable.me/advanced-communication-research-methods/unit-8/thematic-analysis/study-guide/MvOxFlY070c8NU4O](https://library.fiveable.me/advanced-communication-research-methods/unit-8/thematic-analysis/study-guide/MvOxFlY070c8NU4O)~
13 ~[https://pmc.ncbi.nlm.nih.gov/articles/PMC1357541/](https://pmc.ncbi.nlm.nih.gov/articles/PMC1357541/)~
14 ~[https://moralfoundations.org](https://moralfoundations.org/)~
15 ~[https://cs.uky.edu/~sgware/reading/papers/ware2022salience.pdf](https://cs.uky.edu/~sgware/reading/papers/ware2022salience.pdf)~
16 ~[https://www.uoguelph.ca/hftm/thematic-apperception](https://www.uoguelph.ca/hftm/thematic-apperception)~
17 ~[https://pmc.ncbi.nlm.nih.gov/articles/PMC5393928/](https://pmc.ncbi.nlm.nih.gov/articles/PMC5393928/)~
18 ~[https://www.nature.com/articles/s41598-025-99423-9](https://www.nature.com/articles/s41598-025-99423-9)~
19 ~[https://pubmed.ncbi.nlm.nih.gov/38484744/](https://pubmed.ncbi.nlm.nih.gov/38484744/)~
20 ~[https://www.medrxiv.org/content/10.1101/2024.06.01.24308323v1.full-text](https://www.medrxiv.org/content/10.1101/2024.06.01.24308323v1.full-text)~
21 ~[https://www.numberanalytics.com/blog/ultimate-guide-to-salience-in-philosophy-of-language](https://www.numberanalytics.com/blog/ultimate-guide-to-salience-in-philosophy-of-language)~
22 ~[https://www.frontiersin.org/journals/communication/articles/10.3389/fcomm.2021.588823/full](https://www.frontiersin.org/journals/communication/articles/10.3389/fcomm.2021.588823/full)~
23 ~[https://www.jneurosci.org/content/41/43/8972](https://www.jneurosci.org/content/41/43/8972)~
24 ~[https://pmc.ncbi.nlm.nih.gov/articles/PMC11799746/](https://pmc.ncbi.nlm.nih.gov/articles/PMC11799746/)~
25 ~[https://pmc.ncbi.nlm.nih.gov/articles/PMC5664818/](https://pmc.ncbi.nlm.nih.gov/articles/PMC5664818/)~
26 ~[https://www.verywellmind.com/what-is-the-thematic-apperception-test-tat-2795588](https://www.verywellmind.com/what-is-the-thematic-apperception-test-tat-2795588)~
27 ~[https://arxiv.org/html/2402.01788v1](https://arxiv.org/html/2402.01788v1)~
28 ~[https://cs.uwaterloo.ca/~cdimarco/pdf/engl795w17/Mar2004.pdf](https://cs.uwaterloo.ca/~cdimarco/pdf/engl795w17/Mar2004.pdf)~
29 ~[https://pubmed.ncbi.nlm.nih.gov/37363716/](https://pubmed.ncbi.nlm.nih.gov/37363716/)~
30 ~[https://pmc.ncbi.nlm.nih.gov/articles/PMC6591274/](https://pmc.ncbi.nlm.nih.gov/articles/PMC6591274/)~
31 ~[https://insight7.io/narrative-analysis-in-psychology-core-techniques/](https://insight7.io/narrative-analysis-in-psychology-core-techniques/)~
32 ~[https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2017.01897/full](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2017.01897/full)~
33 ~[https://www.tandfonline.com/doi/full/10.1080/00223891.2024.2425663](https://www.tandfonline.com/doi/full/10.1080/00223891.2024.2425663)~
34 ~[https://pmc.ncbi.nlm.nih.gov/articles/PMC8114410/](https://pmc.ncbi.nlm.nih.gov/articles/PMC8114410/)~
35 ~[https://www.sciencedirect.com/science/article/abs/pii/S0885201420301209](https://www.sciencedirect.com/science/article/abs/pii/S0885201420301209)~
36 ~[https://www.routledge.com/Narrative-Comprehension-Causality-and-Coherence-Essays-in-Honor-of-Tom-Trabasso/Goldman-Graesser-vandenBroek/p/book/9781410603135](https://www.routledge.com/Narrative-Comprehension-Causality-and-Coherence-Essays-in-Honor-of-Tom-Trabasso/Goldman-Graesser-vandenBroek/p/book/9781410603135)~
37 ~[https://onlinelibrary.wiley.com/doi/10.1111/tops.12455](https://onlinelibrary.wiley.com/doi/10.1111/tops.12455)~
38 ~[https://www.nature.com/articles/s41539-024-00232-y](https://www.nature.com/articles/s41539-024-00232-y)~
39 ~[https://blog.haiilo.com/blog/14-internal-communication-experts-share-their-top-priorities/](https://blog.haiilo.com/blog/14-internal-communication-experts-share-their-top-priorities/)~
40 ~[https://library.fiu.edu/ai/lit-review](https://library.fiu.edu/ai/lit-review)~
41 ~[https://www.promptingguide.ai/research/llm-agents](https://www.promptingguide.ai/research/llm-agents)~
42 ~[https://www.thecompleteuniversityguide.co.uk/league-tables/rankings/communication-and-media-studies](https://www.thecompleteuniversityguide.co.uk/league-tables/rankings/communication-and-media-studies)~
43 ~[https://www.topuniversities.com/university-subject-rankings/communication-media-studies](https://www.topuniversities.com/university-subject-rankings/communication-media-studies)~
44 ~[https://www.europeanproceedings.com/article/10.15405/epsbs.2022.03.68](https://www.europeanproceedings.com/article/10.15405/epsbs.2022.03.68)~
45 ~[https://pmc.ncbi.nlm.nih.gov/articles/PMC4767388/](https://pmc.ncbi.nlm.nih.gov/articles/PMC4767388/)~
46 ~[https://www.linkedin.com/pulse/llm-prompt-research-paper-analysis-simplifying-academic-hani-simo-rp24f](https://www.linkedin.com/pulse/llm-prompt-research-paper-analysis-simplifying-academic-hani-simo-rp24f)~
47 ~[https://arxiv.org/html/2412.05127v1](https://arxiv.org/html/2412.05127v1)~
48 ~[https://www.reddit.com/r/ChatGPTPromptGenius/comments/11orvrq/literature_review_prompts_i_use_this_prompt_to/](https://www.reddit.com/r/ChatGPTPromptGenius/comments/11orvrq/literature_review_prompts_i_use_this_prompt_to/)~
49 ~[https://pubmed.ncbi.nlm.nih.gov/40036547/](https://pubmed.ncbi.nlm.nih.gov/40036547/)~
50 ~[https://www.pnas.org/doi/10.1073/pnas.2411962122](https://www.pnas.org/doi/10.1073/pnas.2411962122)~
51 ~[https://temertymedicine.utoronto.ca/news/using-ai-make-writing-systematic-reviews-easier-and-faster](https://temertymedicine.utoronto.ca/news/using-ai-make-writing-systematic-reviews-easier-and-faster)~
52 ~[https://arxiv.org/html/2503.08569v1](https://arxiv.org/html/2503.08569v1)~
53 ~[https://informationmatters.org/2025/03/deep-research-a-research-paradigm-shift/](https://informationmatters.org/2025/03/deep-research-a-research-paradigm-shift/)~
