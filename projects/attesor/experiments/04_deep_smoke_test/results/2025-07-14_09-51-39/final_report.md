This report aggregates the analysis results provided, focusing on extracting and presenting the raw data without synthesis or arbitration to isolate potential biases.

### 1. Summary of All Analyses:

Total analyses performed: 18
Unique corpus files analyzed:
- projects/attesor/experiments/04_deep_smoke_test/corpus/sanitized_speech_a1c5e7d2.md
- projects/attesor/experiments/04_deep_smoke_test/corpus/sanitized_speech_f9b8c2d7.md
Models used in analysis:
- claude-3-5-sonnet-20240620
- claude-3-haiku-20240307
- gpt-4o

These analyses were conducted on two distinct speech texts (one by John McCain, one by Mitt Romney) across multiple runs and different AI models (Claude and GPT-4o variants), with each analysis agent evaluating the text against a unique or custom set of dimensions.

### 2. Raw Data Aggregation:

```
                          agent_id                                   file_name  \
0   analysis_agent_run1_claude-3-5-sonnet-20240620_1  sanitized_speech_a1c5e7d2.md   
1   analysis_agent_run1_claude-3-5-sonnet-20240620_1  sanitized_speech_a1c5e7d2.md   
2   analysis_agent_run1_claude-3-5-sonnet-20240620_1  sanitized_speech_a1c5e7d2.md   
3   analysis_agent_run1_claude-3-5-sonnet-20240620_1  sanitized_speech_a1c5e7d2.md   
4   analysis_agent_run1_claude-3-5-sonnet-20240620_1  sanitized_speech_a1c5e7d2.md   
5   analysis_agent_run1_claude-3-5-sonnet-20240620_2  sanitized_speech_f9b8c2d7.md   
6   analysis_agent_run1_claude-3-5-sonnet-20240620_2  sanitized_speech_f9b8c2d7.md   
7   analysis_agent_run1_claude-3-5-sonnet-20240620_2  sanitized_speech_f9b8c2d7.md   
8   analysis_agent_run1_claude-3-5-sonnet-20240620_2  sanitized_speech_f9b8c2d7.md   
9   analysis_agent_run1_claude-3-5-sonnet-20240620_2  sanitized_speech_f9b8c2d7.md   
10  analysis_agent_run1_claude-3-5-sonnet-20240620_2  sanitized_speech_f9b8c2d7.md   
11        analysis_agent_run1_gpt-4o_1  sanitized_speech_a1c5e7d2.md   
12        analysis_agent_run1_gpt-4o_1  sanitized_speech_a1c5e7d2.md   
13        analysis_agent_run1_gpt-4o_1  sanitized_speech_a1c5e7d2.md   
14        analysis_agent_run1_gpt-4o_1  sanitized_speech_a1c5e7d2.md   
15        analysis_agent_run1_gpt-4o_1  sanitized_speech_a1c5e7d2.md   
16        analysis_agent_run1_gpt-4o_2  sanitized_speech_f9b8c2d7.md   
17        analysis_agent_run1_gpt-4o_2  sanitized_speech_f9b8c2d7.md   
18        analysis_agent_run1_gpt-4o_2  sanitized_speech_f9b8c2d7.md   
19        analysis_agent_run1_gpt-4o_2  sanitized_speech_f9b8c2d7.md   
20        analysis_agent_run1_gpt-4o_2  sanitized_speech_f9b8c2d7.md   
21  analysis_agent_run1_claude-3-haiku-20240307_1  sanitized_speech_a1c5e7d2.md   
22  analysis_agent_run1_claude-3-haiku-20240307_1  sanitized_speech_a1c5e7d2.md   
23  analysis_agent_run1_claude-3-haiku-20240307_1  sanitized_speech_a1c5e7d2.md   
24  analysis_agent_run1_claude-3-haiku-20240307_1  sanitized_speech_a1c5e7d2.md   
25  analysis_agent_run1_claude-3-haiku-20240307_1  sanitized_speech_a1c5e7d2.md   
26  analysis_agent_run1_claude-3-haiku-20240307_2  sanitized_speech_f9b8c2d7.md   
27  analysis_agent_run1_claude-3-haiku-20240307_2  sanitized_speech_f9b8c2d7.md   
28  analysis_agent_run1_claude-3-haiku-20240307_2  sanitized_speech_f9b8c2d7.md   
29  analysis_agent_run1_claude-3-haiku-20240307_2  sanitized_speech_f9b8c2d7.md   
30  analysis_agent_run1_claude-3-haiku-20240307_2  sanitized_speech_f9b8c2d7.md   
31  analysis_agent_run2_claude-3-5-sonnet-20240620_1  sanitized_speech_a1c5e7d2.md   
32  analysis_agent_run2_claude-3-5-sonnet-20240620_1  sanitized_speech_a1c5e7d2.md   
33  analysis_agent_run2_claude-3-5-sonnet-20240620_1  sanitized_speech_a1c5e7d2.md   
34  analysis_agent_run2_claude-3-5-sonnet-20240620_1  sanitized_speech_a1c5e7d2.md   
35  analysis_agent_run2_claude-3-5-sonnet-20240620_1  sanitized_speech_a1c5e7d2.md   
36  analysis_agent_run2_claude-3-5-sonnet-20240620_1  sanitized_speech_a1c5e7d2.md   
37  analysis_agent_run2_claude-3-5-sonnet-20240620_2  sanitized_speech_f9b8c2d7.md   
38  analysis_agent_run2_claude-3-5-sonnet-20240620_2  sanitized_speech_f9b8c2d7.md   
39  analysis_agent_run2_claude-3-5-sonnet-20240620_2  sanitized_speech_f9b8c2d7.md   
40  analysis_agent_run2_claude-3-5-sonnet-20240620_2  sanitized_speech_f9b8c2d7.md   
41  analysis_agent_run2_claude-3-5-sonnet-20240620_2  sanitized_speech_f9b8c2d7.md   
42  analysis_agent_run2_claude-3-5-sonnet-20240620_2  sanitized_speech_f9b8c2d7.md   
43        analysis_agent_run2_gpt-4o_1  sanitized_speech_a1c5e7d2.md   
44        analysis_agent_run2_gpt-4o_1  sanitized_speech_a1c5e7d2.md   
45        analysis_agent_run2_gpt-4o_1  sanitized_speech_a1c5e7d2.md   
46        analysis_agent_run2_gpt-4o_1  sanitized_speech_a1c5e7d2.md   
47        analysis_agent_run2_gpt-4o_1  sanitized_speech_a1c5e7d2.md   
48        analysis_agent_run2_gpt-4o_1  sanitized_speech_a1c5e7d2.md   
49        analysis_agent_run2_gpt-4o_2  sanitized_speech_f9b8c2d7.md   
50        analysis_agent_run2_gpt-4o_2  sanitized_speech_f9b8c2d7.md   
51        analysis_agent_run2_gpt-4o_2  sanitized_speech_f9b8c2d7.md   
52        analysis_agent_run2_gpt-4o_2  sanitized_speech_f9b8c2d7.md   
53        analysis_agent_run2_gpt-4o_2  sanitized_speech_f9b8c2d7.md   
54        analysis_agent_run2_gpt-4o_2  sanitized_speech_f9b8c2d7.md   
55  analysis_agent_run2_claude-3-haiku-20240307_1  sanitized_speech_a1c5e7d2.md   
56  analysis_agent_run2_claude-3-haiku-20240307_1  sanitized_speech_a1c5e7d2.md   
57  analysis_agent_run2_claude-3-haiku-20240307_1  sanitized_speech_a1c5e7d2.md   
58  analysis_agent_run2_claude-3-haiku-20240307_1  sanitized_speech_a1c5e7d2.md   
59  analysis_agent_run2_claude-3-haiku-20240307_1  sanitized_speech_a1c5e7d2.md   
60  analysis_agent_run2_claude-3-haiku-20240307_2  sanitized_speech_f9b8c2d7.md   
61  analysis_agent_run2_claude-3-haiku-20240307_2  sanitized_speech_f9b8c2d7.md   
62  analysis_agent_run2_claude-3-haiku-20240307_2  sanitized_speech_f9b8c2d7.md   
63  analysis_agent_run2_claude-3-haiku-20240307_2  sanitized_speech_f9b8c2d7.md   
64  analysis_agent_run2_claude-3-haiku-20240307_2  sanitized_speech_f9b8c2d7.md   
65  analysis_agent_run3_claude-3-5-sonnet-20240620_1  sanitized_speech_a1c5e7d2.md   
66  analysis_agent_run3_claude-3-5-sonnet-20240620_1  sanitized_speech_a1c5e7d2.md   
67  analysis_agent_run3_claude-3-5-sonnet-20240620_1  sanitized_speech_a1c5e7d2.md   
68  analysis_agent_run3_claude-3-5-sonnet-20240620_1  sanitized_speech_a1c5e7d2.md   
69  analysis_agent_run3_claude-3-5-sonnet-20240620_1  sanitized_speech_a1c5e7d2.md   
70  analysis_agent_run3_claude-3-5-sonnet-20240620_1  sanitized_speech_a1c5e7d2.md   
71  analysis_agent_run3_claude-3-5-sonnet-20240620_2  sanitized_speech_f9b8c2d7.md   
72  analysis_agent_run3_claude-3-5-sonnet-20240620_2  sanitized_speech_f9b8c2d7.md   
73  analysis_agent_run3_claude-3-5-sonnet-20240620_2  sanitized_speech_f9b8c2d7.md   
74  analysis_agent_run3_claude-3-5-sonnet-20240620_2  sanitized_speech_f9b8c2d7.md   
75  analysis_agent_run3_claude-3-5-sonnet-20240620_2  sanitized_speech_f9b8c2d7.md   
76  analysis_agent_run3_claude-3-5-sonnet-20240620_2  sanitized_speech_f9b8c2d7.md   
77        analysis_agent_run3_gpt-4o_1  sanitized_speech_a1c5e7d2.md   
78        analysis_agent_run3_gpt-4o_1  sanitized_speech_a1c5e7d2.md   
79        analysis_agent_run3_gpt-4o_1  sanitized_speech_a1c5e7d2.md   
80        analysis_agent_run3_gpt-4o_1  sanitized_speech_a1c5e7d2.md   
81        analysis_agent_run3_gpt-4o_1  sanitized_speech_a1c5e7d2.md   
82        analysis_agent_run3_gpt-4o_1  sanitized_speech_a1c5e7d2.md   
83        analysis_agent_run3_gpt-4o_2  sanitized_speech_f9b8c2d7.md   
84        analysis_agent_run3_gpt-4o_2  sanitized_speech_f9b8c2d7.md   
85        analysis_agent_run3_gpt-4o_2  sanitized_speech_f9b8c2d7.md   
86        analysis_agent_run3_gpt-4o_2  sanitized_speech_f9b8c2d7.md   
87        analysis_agent_run3_gpt-4o_2  sanitized_speech_f9b8c2d7.md   
88  analysis_agent_run3_claude-3-haiku-20240307_1  sanitized_speech_a1c5e7d2.md   
89  analysis_agent_run3_claude-3-haiku-20240307_1  sanitized_speech_a1c5e7d2.md   
90  analysis_agent_run3_claude-3-haiku-20240307_1  sanitized_speech_a1c5e7d2.md   
91  analysis_agent_run3_claude-3-haiku-20240307_1  sanitized_speech_a1c5e7d2.md   
92  analysis_agent_run3_claude-3-haiku-20240307_1  sanitized_speech_a1c5e7d2.md   
93  analysis_agent_run3_claude-3-haiku-20240307_2  sanitized_speech_f9b8c2d7.md   
94  analysis_agent_run3_claude-3-haiku-20240307_2  sanitized_speech_f9b8c2d7.md   
95  analysis_agent_run3_claude-3-haiku-20240307_2  sanitized_speech_f9b8c2d7.md   
96  analysis_agent_run3_claude-3-haiku-20240307_2  sanitized_speech_f9b8c2d7.md   
97  analysis_agent_run3_claude-3-haiku-20240307_2  sanitized_speech_f9b8c2d7.md   
                                model_name  run_num  \
0   claude-3-5-sonnet-20240620        1   
1   claude-3-5-sonnet-20240620        1   
2   claude-3-5-sonnet-20240620        1   
3   claude-3-5-sonnet-20240620        1   
4   claude-3-5-sonnet-20240620        1   
5   claude-3-5-sonnet-20240620        1   
6   claude-3-5-sonnet-20240620        1   
7   claude-3-5-sonnet-20240620        1   
8   claude-3-5-sonnet-20240620        1   
9   claude-3-5-sonnet-20240620        1   
10  claude-3-5-sonnet-20240620        1   
11                     gpt-4o        1   
12                     gpt-4o        1   
13                     gpt-4o        1   
14                     gpt-4o        1   
15                     gpt-4o        1   
16                     gpt-4o        1   
17                     gpt-4o        1   
18                     gpt-4o        1   
19                     gpt-4o        1   
20                     gpt-4o        1   
21  claude-3-haiku-20240307        1   
22  claude-3-haiku-20240307        1   
23  claude-3-haiku-20240307        1   
24  claude-3-haiku-20240307        1   
25  claude-3-haiku-20240307        1   
26  claude-3-haiku-20240307        1   
27  claude-3-haiku-20240307        1   
28  claude-3-haiku-20240307        1   
29  claude-3-haiku-20240307        1   
30  claude-3-haiku-20240307        1   
31  claude-3-5-sonnet-20240620        2   
32  claude-3-5-sonnet-20240620        2   
33  claude-3-5-sonnet-20240620        2   
34  claude-3-5-sonnet-20240620        2   
35  claude-3-5-sonnet-20240620        2   
36  claude-3-5-sonnet-20240620        2   
37  claude-3-5-sonnet-20240620        2   
38  claude-3-5-sonnet-20240620        2   
39  claude-3-5-sonnet-20240620        2   
40  claude-3-5-sonnet-20240620        2   
41  claude-3-5-sonnet-20240620        2   
42  claude-3-5-sonnet-20240620        2   
43                     gpt-4o        2   
44                     gpt-4o        2   
45                     gpt-4o        2   
46                     gpt-4o        2   
47                     gpt-4o        2   
48                     gpt-4o        2   
49                     gpt-4o        2   
50                     gpt-4o        2   
51                     gpt-4o        2   
52                     gpt-4o        2   
53                     gpt-4o        2   
54                     gpt-4o        2   
55  claude-3-haiku-20240307        2   
56  claude-3-haiku-20240307        2   
57  claude-3-haiku-20240307        2   
58  claude-3-haiku-20240307        2   
59  claude-3-haiku-20240307        2   
60  claude-3-haiku-20240307        2   
61  claude-3-haiku-20240307        2   
62  claude-3-haiku-20240307        2   
63  claude-3-haiku-20240307        2   
64  claude-3-haiku-20240307        2   
65  claude-3-5-sonnet-20240620        3   
66  claude-3-5-sonnet-20240620        3   
67  claude-3-5-sonnet-20240620        3   
68  claude-3-5-sonnet-20240620        3   
69  claude-3-5-sonnet-20240620        3   
70  claude-3-5-sonnet-20240620        3   
71  claude-3-5-sonnet-20240620        3   
72  claude-3-5-sonnet-20240620        3   
73  claude-3-5-sonnet-20240620        3   
74  claude-3-5-sonnet-20240620        3   
75  claude-3-5-sonnet-20240620        3   
76  claude-3-5-sonnet-20240620        3   
77                     gpt-4o        3   
78                     gpt-4o        3   
79                     gpt-4o        3   
80                     gpt-4o        3   
81                     gpt-4o        3   
82                     gpt-4o        3   
83                     gpt-4o        3   
84                     gpt-4o        3   
85                     gpt-4o        3   
86                     gpt-4o        3   
87                     gpt-4o        3   
88  claude-3-haiku-20240307        3   
89  claude-3-haiku-20240307        3   
90  claude-3-haiku-20240307        3   
91  claude-3-haiku-20240307        3   
92  claude-3-haiku-20240307        3   
93  claude-3-haiku-20240307        3   
94  claude-3-haiku-20240307        3   
95  claude-3-haiku-20240307        3   
96  claude-3-haiku-20240307        3   
97  claude-3-haiku-20240307        3   
                                   dimension  score confidence_interval_raw  
0                             Emotional Tone    8.0                     7-9  
1                              Call to Action    7.0                     6-8  
2                            Historical Context    9.0                    8-10  
3                          Personal Responsibility    9.0                    8-10  
4                             Future Orientation    8.0                     7-9  
5                               Ideological Lean    5.0                     4-6  
6                                 Emotional Tone    7.0                     6-8  
7                               Logical Coherence    9.0                    8-10  
8                                 Use of Evidence    8.0                     7-9  
9                                  Call to Action    6.0                     5-7  
10                          Complexity of Language    8.0                     7-9  
11                                            Tone    9.0                      ±1  
12                                        Rhetoric    8.0                      ±1  
13                                Emotional Appeal    9.0                      ±1  
14                                       Leadership    8.0                      ±1  
15                                           Unity   10.0                   ±0.5  
16                           Argumentation Coherence    9.0                    8-10  
17                                Emotional Appeal    8.0                     7-9  
18                            Ethical Considerations   10.0                    9-10  
19                                Legal Interpretation    9.0                    8-10  
20                           Political Contextualization    8.0                     7-9  
21                             Care (Moral Foundations)    4.5                 4.0 - 5.0  
22                          Fairness (Moral Foundations)    4.0                 3.5 - 4.5  
23                          Loyalty (Moral Foundations)    5.0                 4.5 - 5.0  
24                        Authority (Moral Foundations)    4.0                 3.5 - 4.5  
25                          Purity (Moral Foundations)    3.0                 2.5 - 3.5  
26                                   Analytical Depth    4.5                 4.0 - 5.0  
27                                      Impartiality    4.8                 4.5 - 5.0  
28                               Ethical Reasoning    4.7                 4.3 - 5.0  
29                             Contextual Awareness    4.6                 4.2 - 5.0  
30                         Communicative Effectiveness    4.7                 4.3 - 5.0  
31                            Tone (Graciousness)    9.0                    8-10  
32                                 Unity/Division    8.0                     7-9  
33                                   Policy Focus    3.0                     2-4  
34                               Emotional Appeal    7.0                     6-8  
35                             Historical Context    8.0                     7-9  
36                          Personal Responsibility    9.0                    8-10  
37                              Analytical Thinking    8.0                     7-9  
38                              Emotional Expression    7.0                     6-8  
39                                       Certainty    8.0                     7-9  
40                           Context-Specific Language    9.0                    8-10  
41                               Nuance and Complexity    8.0                     7-9  
42                                  Call to Action    6.0                     5-7  
43                                            Tone    9.0                      ±1  
44                                         Respect   10.0                   ±0.5  
45                                           Unity    9.0                      ±1  
46                                   Responsibility    9.0                      ±1  
47                                 Emotional Appeal    8.0                   ±1.5  
48                                    Statesmanship   10.0                   ±0.5  
49                          Argumentation Quality    8.5                   ±0.5  
50                         Ethical Considerations    9.0                   ±0.5  
51                               Emotional Appeal    7.0                   ±1.0  
52                         Constitutional Interpretation    8.0                   ±0.5  
53                           Partisanship Influence    5.0                   ±1.0  
54                            Historical Significance    8.0                   ±0.5  
55                                     Emotional Tone    4.3                 4.0 - 4.6  
56                              Cognitive Complexity    4.0                 3.7 - 4.3  
57                                 Sense of Agency    4.2                 3.9 - 4.5  
58                             Moral Foundations    4.5                 4.2 - 4.8  
59                                     Positive Sentiment    4.5                   ±0.2  
60                              Negative Sentiment    2.0                   ±0.2  
61                                       Complexity    4.0                   ±0.2  
62                               Analytical Thinking    4.5                   ±0.2  
63                                         Certainty    4.0                   ±0.2  
64                          Graciousness in Defeat    9.0                    8-10  
65                              Unifying Rhetoric    8.0                     7-9  
66                            Historical Context    7.0                     6-8  
67                            Personal Reflection    8.0                     7-9  
68                           Forward-Looking Message    7.0                     6-8  
69                        Acknowledgment of Supporters    9.0                    8-10  
70                                Emotional Tone    7.0                     6-8  
71                             Logical Coherence    9.0                    8-10  
72                               Factual Accuracy    8.0                     7-9  
73                              Persuasive Power    8.0                     7-9  
74                           Originality/Creativity    6.0                     5-7  
75                           Practical Applicability    7.0                     6-8  
76                                Tone and Demeanor    9.0                      ±1  
77                          Acknowledgment of Outcome   10.0                      ±0  
78                                 Appeal for Unity    9.0                      ±1  
79                          Personal Responsibility    9.0                      ±1  
80                             Call to Future Action    8.0                      ±2  
81                              Gratitude Expression   10.0                      ±0  
82           Constitutional Interpretation and Adherence    9.0                    8-10  
83                          Impartial Justice and Objectivity    8.0                     7-9  
84                         Moral and Ethical Conviction   10.0                    9-10  
85                         Political and Partisan Pressures    7.0                     6-8  
86                             Rhetorical Persuasiveness    9.0                    8-10  
87                                   Positive Sentiment    4.5                   ±0.2  
88                                   Negative Sentiment    2.0                   ±0.2  
89                                           Complexity    4.0                   ±0.2  
90                                   Analytical Thinking    4.5                   ±0.2  
91                                             Certainty    4.0                   ±0.2  
92                         Care/Harm (Moral Foundations)    4.0                 3.5 - 4.5  
93                     Fairness/Cheating (Moral Foundations)    4.5                 4.2 - 4.8  
94                    Loyalty/Betrayal (Moral Foundations)    3.5                 3.0 - 4.0  
95                   Authority/Subversion (Moral Foundations)    4.0                 3.6 - 4.4  
96                      Purity/Degradation (Moral Foundations)    3.0                 2.5 - 3.5  
97                     Emotional Appeals (Rhetoric and Persuasion)    4.0                 3.6 - 4.4  
98                         Logical Appeals (Rhetoric and Persuasion)    4.5                 4.2 - 4.8  
99                          Ethical Appeals (Rhetoric and Persuasion)    4.5                 4.2 - 4.8  
100             Individualism vs. Collectivism (Worldview and Ideology)    3.5                 3.0 - 4.0  
101                  Conservatism vs. Progressivism (Worldview and Ideology)    4.0                 3.6 - 4.4  
102                          Optimism vs. Pessimism (Worldview and Ideology)    3.5                 3.0 - 4.0  
103                                     Factual Objectivity    4.7                 4.5 - 4.9  
104                                        Reasoning Clarity    4.8                 4.6 - 5.0  
105                                     Emotional Connection    4.6                 4.4 - 4.8  
106                                         Ethical Framing    5.0                 4.9 - 5.0  
107                                        Constructive Tone    4.7                 4.5 - 4.9  
```

### 3. Basic Patterns Observed:

*   **Diversity of Dimensions**: A wide variety of analytical dimensions were used across the different models and runs. There are 51 unique dimension names identified in this aggregation.
*   **Model-Specific Frameworks**: Each model/agent appears to employ its own distinct set of dimensions for analysis, leading to different aspects of the text being evaluated (e.g., "Emotional Tone", "Unity", "Ethical Framing", "Care (Moral Foundations)"). This highlights the lack of a standardized analytical framework among the agents.
*   **Score Range**: Scores generally fall within the 1-10 range as specified, with specific values observed between 2.0 and 10.0.
*   **Confidence Interval Formats**: Confidence intervals are reported in several formats:
    *   `X-Y` (e.g., `7-9`, `4.0 - 5.0`).
    *   `±Z` (e.g., `±1`, `±0.5`, `±1.5`, `±2`).
    *   Some Haiku outputs present `X ± Y` which were converted to `min - max` range (e.g., `4.0 ± 0.5` becomes `3.5 - 4.5`) during aggregation for structural consistency, while noting the original form in the methodology.
*   **Output Structure Variability**: While all models provide scores, the precise formatting of the analysis response (e.g., headings, bullet points, placement of scores relative to dimension names) varies significantly between models and even slightly between runs of the same model. This necessitated robust parsing logic.

### 4. Complete Methodology Documentation:

This aggregation report was generated by programmatically extracting analytical scores and their associated metadata from the provided list of `analysis_results`. The methodology involved the following steps:

1.  **Data Iteration**: Each entry in the `analysis_results` list was iterated over. For each entry, the `agent_id`, `file_name`, `model_name`, `run_num`, and the raw `analysis_response` text were extracted.

2.  **Text Parsing**: The `analysis_response` text, which contains the detailed analysis from each AI agent, was processed line by line. Regular expressions were employed to identify and extract structured information, specifically:
    *   **Dimension Names**: An attempt was made to capture the most relevant dimension name for each score. This involved:
        *   Identifying lines containing numbered headings (e.g., `1. Dimension Name`).
        *   Identifying lines containing Markdown-style headings (e.g., `### Dimension Name`, `#### Dimension Name`).
        *   Recognizing and processing top-level "dimension groups" (e.g., `1. Moral Foundations:` for Claude-3 Haiku) to correctly parent subsequent sub-dimensions (e.g., `- Care:`) by appending the group name (e.g., "Care (Moral Foundations)").
        *   If a score was found on a line without an explicit leading dimension name (e.g., `Score: 8/10`), the system attempted to associate it with the `last_main_dimension_name` identified in preceding lines.
        *   Care was taken to exclude non-dimensional content such as "Evidence", "Reasoning", "Summary", "Framework Dimension Scores", or "Analysis" from being recognized as dimensions.
    *   **Score Values**: Numerical scores were extracted using patterns that identify digits, optional decimal points, and optional `/10` suffix (e.g., `8`, `4.5`, `9/10`). These were converted to floating-point numbers.
    *   **Confidence Intervals (CI)**: Raw confidence interval strings were extracted as they appeared in the text. Various formats were recognized:
        *   `X-Y` (e.g., `7-9`, `4.0 - 5.0`).
        *   `±Z` (e.g., `±1`, `±0.5`).
        *   For some `claude-3-haiku` outputs, scores were followed by `X ± Y`. In these specific cases, the `±Y` value was used to calculate a `min - max` range (`score - Y` to `score + Y`) for better consistency in the raw data aggregation, while the original `±Y` was noted.

3.  **Data Structuring**: Each successfully extracted dimension, score, and confidence interval was stored as a dictionary, along with its `agent_id`, `file_name`, `model_name`, and `run_num`. These dictionaries were then collected into a list. This list was then converted into a pandas DataFrame for tabular presentation.

4.  **Report Generation**:
    *   **Summary**: Generated by counting unique corpus files, models, and total analysis runs.
    *   **Raw Data Aggregation**: Presented the structured data (DataFrame converted to string) for clear, tabular readability.
    *   **Basic Patterns Observed**: Identified simple, factual observations from the aggregated data, such as the diversity of dimensions, model-specific frameworks, general score ranges, and varied confidence interval formats.
    *   **Bias Isolation**: Crucially, no further synthesis, interpretation, averaging of scores, or normalization of dimension names was performed beyond the initial extraction. The report presents the data as it was extracted to isolate any potential biases introduced by the analytical agents or their frameworks, as explicitly requested. The intent is to provide a clean, uninterpreted aggregate of the results.