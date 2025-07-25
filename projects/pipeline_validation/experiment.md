name: "pipeline_validation_experiment"
description: "Canonical experiment to validate the first 3 stages of the pipeline (PreTest → BatchAnalysis → CorpusSynthesis)."
research_question: "Does the simplified 3-stage pipeline produce a valid synthesis from the Constitutional Health Framework analysis?"
frameworks:
  - id: chf_v1.1_ideology_enhanced.md
    sha256: 4fee4d1de6adae3478c913181f871cbeb7be377910b93a792d6803deef9d3070
corpus_path: "corpus/"
statistical_runs: 1
pipeline_stages: ["PreTest", "BatchAnalysis", "CorpusSynthesis"]
stop_after_stage: "CorpusSynthesis"
