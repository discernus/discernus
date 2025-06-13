# End-to-End Pipeline Troubleshooting Guide
*Generated: 2025-06-13T07:21:56.105130*

## Executive Summary

**Pipeline Success Rate**: 0.0% (0/10 tests passed)

**Manual Interventions Required**: 20 (2.0 per test)

**Zero-Intervention Goal Met**: ❌ NO

## Gap Analysis Summary

- **Critical Gaps**: 0 (require immediate attention)
- **Error Gaps**: 10 (prevent functionality)  
- **Warning Gaps**: 10 (suboptimal behavior)
- **Info Gaps**: 142 (informational)

## Critical Issues Requiring Resolution

### DatabaseStorage

⚠️ **WARNING**: Real database storage failed: (psycopg2.errors.NotNullViolation) null value in column "selected_models" of relation "experiment" violates not-null constraint
DETAIL:  Failing row contains (17, null, Pipeline Test - civic_virtue, null, End-to-end pipeline validation test, null, hierarchical_v1, civic_virtue, standard, single_model, null, draft, 0, 0, null, unpublished, [], 2025-06-13 07:21:15.868597, 2025-06-13 07:21:15.868597, null, null, null).

[SQL: INSERT INTO experiment (creator_id, name, hypothesis, description, research_context, prompt_template_id, framework_config_id, scoring_algorithm_id, analysis_mode, status, total_runs, successful_runs, research_notes, publication_status, tags, created_at, updated_at) VALUES (%(creator_id)s, %(name)s, %(hypothesis)s, %(description)s, %(research_context)s, %(prompt_template_id)s, %(framework_config_id)s, %(scoring_algorithm_id)s, %(analysis_mode)s, %(status)s, %(total_runs)s, %(successful_runs)s, %(research_notes)s, %(publication_status)s, %(tags)s::JSON, now(), now()) RETURNING experiment.id, experiment.created_at, experiment.updated_at]
[parameters: {'creator_id': None, 'name': 'Pipeline Test - civic_virtue', 'hypothesis': None, 'description': 'End-to-end pipeline validation test', 'research_context': None, 'prompt_template_id': 'hierarchical_v1', 'framework_config_id': 'civic_virtue', 'scoring_algorithm_id': 'standard', 'analysis_mode': 'single_model', 'status': 'draft', 'total_runs': 0, 'successful_runs': 0, 'research_notes': None, 'publication_status': 'unpublished', 'tags': '[]'}]
(Background on this error at: https://sqlalche.me/e/20/gkpj), using mock storage
   *Manual Intervention Required*: Yes

⚠️ **WARNING**: Real database storage failed: (psycopg2.errors.NotNullViolation) null value in column "selected_models" of relation "experiment" violates not-null constraint
DETAIL:  Failing row contains (18, null, Pipeline Test - civic_virtue, null, End-to-end pipeline validation test, null, hierarchical_v1, civic_virtue, standard, single_model, null, draft, 0, 0, null, unpublished, [], 2025-06-13 07:21:28.304149, 2025-06-13 07:21:28.304149, null, null, null).

[SQL: INSERT INTO experiment (creator_id, name, hypothesis, description, research_context, prompt_template_id, framework_config_id, scoring_algorithm_id, analysis_mode, status, total_runs, successful_runs, research_notes, publication_status, tags, created_at, updated_at) VALUES (%(creator_id)s, %(name)s, %(hypothesis)s, %(description)s, %(research_context)s, %(prompt_template_id)s, %(framework_config_id)s, %(scoring_algorithm_id)s, %(analysis_mode)s, %(status)s, %(total_runs)s, %(successful_runs)s, %(research_notes)s, %(publication_status)s, %(tags)s::JSON, now(), now()) RETURNING experiment.id, experiment.created_at, experiment.updated_at]
[parameters: {'creator_id': None, 'name': 'Pipeline Test - civic_virtue', 'hypothesis': None, 'description': 'End-to-end pipeline validation test', 'research_context': None, 'prompt_template_id': 'hierarchical_v1', 'framework_config_id': 'civic_virtue', 'scoring_algorithm_id': 'standard', 'analysis_mode': 'single_model', 'status': 'draft', 'total_runs': 0, 'successful_runs': 0, 'research_notes': None, 'publication_status': 'unpublished', 'tags': '[]'}]
(Background on this error at: https://sqlalche.me/e/20/gkpj), using mock storage
   *Manual Intervention Required*: Yes

⚠️ **WARNING**: Real database storage failed: (psycopg2.errors.NotNullViolation) null value in column "selected_models" of relation "experiment" violates not-null constraint
DETAIL:  Failing row contains (19, null, Pipeline Test - political_spectrum, null, End-to-end pipeline validation test, null, hierarchical_v1, political_spectrum, standard, single_model, null, draft, 0, 0, null, unpublished, [], 2025-06-13 07:21:31.122068, 2025-06-13 07:21:31.122068, null, null, null).

[SQL: INSERT INTO experiment (creator_id, name, hypothesis, description, research_context, prompt_template_id, framework_config_id, scoring_algorithm_id, analysis_mode, status, total_runs, successful_runs, research_notes, publication_status, tags, created_at, updated_at) VALUES (%(creator_id)s, %(name)s, %(hypothesis)s, %(description)s, %(research_context)s, %(prompt_template_id)s, %(framework_config_id)s, %(scoring_algorithm_id)s, %(analysis_mode)s, %(status)s, %(total_runs)s, %(successful_runs)s, %(research_notes)s, %(publication_status)s, %(tags)s::JSON, now(), now()) RETURNING experiment.id, experiment.created_at, experiment.updated_at]
[parameters: {'creator_id': None, 'name': 'Pipeline Test - political_spectrum', 'hypothesis': None, 'description': 'End-to-end pipeline validation test', 'research_context': None, 'prompt_template_id': 'hierarchical_v1', 'framework_config_id': 'political_spectrum', 'scoring_algorithm_id': 'standard', 'analysis_mode': 'single_model', 'status': 'draft', 'total_runs': 0, 'successful_runs': 0, 'research_notes': None, 'publication_status': 'unpublished', 'tags': '[]'}]
(Background on this error at: https://sqlalche.me/e/20/gkpj), using mock storage
   *Manual Intervention Required*: Yes

⚠️ **WARNING**: Real database storage failed: (psycopg2.errors.NotNullViolation) null value in column "selected_models" of relation "experiment" violates not-null constraint
DETAIL:  Failing row contains (20, null, Pipeline Test - political_spectrum, null, End-to-end pipeline validation test, null, hierarchical_v1, political_spectrum, standard, single_model, null, draft, 0, 0, null, unpublished, [], 2025-06-13 07:21:34.942091, 2025-06-13 07:21:34.942091, null, null, null).

[SQL: INSERT INTO experiment (creator_id, name, hypothesis, description, research_context, prompt_template_id, framework_config_id, scoring_algorithm_id, analysis_mode, status, total_runs, successful_runs, research_notes, publication_status, tags, created_at, updated_at) VALUES (%(creator_id)s, %(name)s, %(hypothesis)s, %(description)s, %(research_context)s, %(prompt_template_id)s, %(framework_config_id)s, %(scoring_algorithm_id)s, %(analysis_mode)s, %(status)s, %(total_runs)s, %(successful_runs)s, %(research_notes)s, %(publication_status)s, %(tags)s::JSON, now(), now()) RETURNING experiment.id, experiment.created_at, experiment.updated_at]
[parameters: {'creator_id': None, 'name': 'Pipeline Test - political_spectrum', 'hypothesis': None, 'description': 'End-to-end pipeline validation test', 'research_context': None, 'prompt_template_id': 'hierarchical_v1', 'framework_config_id': 'political_spectrum', 'scoring_algorithm_id': 'standard', 'analysis_mode': 'single_model', 'status': 'draft', 'total_runs': 0, 'successful_runs': 0, 'research_notes': None, 'publication_status': 'unpublished', 'tags': '[]'}]
(Background on this error at: https://sqlalche.me/e/20/gkpj), using mock storage
   *Manual Intervention Required*: Yes

⚠️ **WARNING**: Real database storage failed: (psycopg2.errors.NotNullViolation) null value in column "selected_models" of relation "experiment" violates not-null constraint
DETAIL:  Failing row contains (21, null, Pipeline Test - fukuyama_identity, null, End-to-end pipeline validation test, null, hierarchical_v1, fukuyama_identity, standard, single_model, null, draft, 0, 0, null, unpublished, [], 2025-06-13 07:21:37.742698, 2025-06-13 07:21:37.742698, null, null, null).

[SQL: INSERT INTO experiment (creator_id, name, hypothesis, description, research_context, prompt_template_id, framework_config_id, scoring_algorithm_id, analysis_mode, status, total_runs, successful_runs, research_notes, publication_status, tags, created_at, updated_at) VALUES (%(creator_id)s, %(name)s, %(hypothesis)s, %(description)s, %(research_context)s, %(prompt_template_id)s, %(framework_config_id)s, %(scoring_algorithm_id)s, %(analysis_mode)s, %(status)s, %(total_runs)s, %(successful_runs)s, %(research_notes)s, %(publication_status)s, %(tags)s::JSON, now(), now()) RETURNING experiment.id, experiment.created_at, experiment.updated_at]
[parameters: {'creator_id': None, 'name': 'Pipeline Test - fukuyama_identity', 'hypothesis': None, 'description': 'End-to-end pipeline validation test', 'research_context': None, 'prompt_template_id': 'hierarchical_v1', 'framework_config_id': 'fukuyama_identity', 'scoring_algorithm_id': 'standard', 'analysis_mode': 'single_model', 'status': 'draft', 'total_runs': 0, 'successful_runs': 0, 'research_notes': None, 'publication_status': 'unpublished', 'tags': '[]'}]
(Background on this error at: https://sqlalche.me/e/20/gkpj), using mock storage
   *Manual Intervention Required*: Yes

⚠️ **WARNING**: Real database storage failed: (psycopg2.errors.NotNullViolation) null value in column "selected_models" of relation "experiment" violates not-null constraint
DETAIL:  Failing row contains (22, null, Pipeline Test - fukuyama_identity, null, End-to-end pipeline validation test, null, hierarchical_v1, fukuyama_identity, standard, single_model, null, draft, 0, 0, null, unpublished, [], 2025-06-13 07:21:40.678315, 2025-06-13 07:21:40.678315, null, null, null).

[SQL: INSERT INTO experiment (creator_id, name, hypothesis, description, research_context, prompt_template_id, framework_config_id, scoring_algorithm_id, analysis_mode, status, total_runs, successful_runs, research_notes, publication_status, tags, created_at, updated_at) VALUES (%(creator_id)s, %(name)s, %(hypothesis)s, %(description)s, %(research_context)s, %(prompt_template_id)s, %(framework_config_id)s, %(scoring_algorithm_id)s, %(analysis_mode)s, %(status)s, %(total_runs)s, %(successful_runs)s, %(research_notes)s, %(publication_status)s, %(tags)s::JSON, now(), now()) RETURNING experiment.id, experiment.created_at, experiment.updated_at]
[parameters: {'creator_id': None, 'name': 'Pipeline Test - fukuyama_identity', 'hypothesis': None, 'description': 'End-to-end pipeline validation test', 'research_context': None, 'prompt_template_id': 'hierarchical_v1', 'framework_config_id': 'fukuyama_identity', 'scoring_algorithm_id': 'standard', 'analysis_mode': 'single_model', 'status': 'draft', 'total_runs': 0, 'successful_runs': 0, 'research_notes': None, 'publication_status': 'unpublished', 'tags': '[]'}]
(Background on this error at: https://sqlalche.me/e/20/gkpj), using mock storage
   *Manual Intervention Required*: Yes

⚠️ **WARNING**: Real database storage failed: (psycopg2.errors.NotNullViolation) null value in column "selected_models" of relation "experiment" violates not-null constraint
DETAIL:  Failing row contains (23, null, Pipeline Test - mft_persuasive_force, null, End-to-end pipeline validation test, null, hierarchical_v1, mft_persuasive_force, standard, single_model, null, draft, 0, 0, null, unpublished, [], 2025-06-13 07:21:43.377962, 2025-06-13 07:21:43.377962, null, null, null).

[SQL: INSERT INTO experiment (creator_id, name, hypothesis, description, research_context, prompt_template_id, framework_config_id, scoring_algorithm_id, analysis_mode, status, total_runs, successful_runs, research_notes, publication_status, tags, created_at, updated_at) VALUES (%(creator_id)s, %(name)s, %(hypothesis)s, %(description)s, %(research_context)s, %(prompt_template_id)s, %(framework_config_id)s, %(scoring_algorithm_id)s, %(analysis_mode)s, %(status)s, %(total_runs)s, %(successful_runs)s, %(research_notes)s, %(publication_status)s, %(tags)s::JSON, now(), now()) RETURNING experiment.id, experiment.created_at, experiment.updated_at]
[parameters: {'creator_id': None, 'name': 'Pipeline Test - mft_persuasive_force', 'hypothesis': None, 'description': 'End-to-end pipeline validation test', 'research_context': None, 'prompt_template_id': 'hierarchical_v1', 'framework_config_id': 'mft_persuasive_force', 'scoring_algorithm_id': 'standard', 'analysis_mode': 'single_model', 'status': 'draft', 'total_runs': 0, 'successful_runs': 0, 'research_notes': None, 'publication_status': 'unpublished', 'tags': '[]'}]
(Background on this error at: https://sqlalche.me/e/20/gkpj), using mock storage
   *Manual Intervention Required*: Yes

⚠️ **WARNING**: Real database storage failed: (psycopg2.errors.NotNullViolation) null value in column "selected_models" of relation "experiment" violates not-null constraint
DETAIL:  Failing row contains (24, null, Pipeline Test - mft_persuasive_force, null, End-to-end pipeline validation test, null, hierarchical_v1, mft_persuasive_force, standard, single_model, null, draft, 0, 0, null, unpublished, [], 2025-06-13 07:21:47.091195, 2025-06-13 07:21:47.091195, null, null, null).

[SQL: INSERT INTO experiment (creator_id, name, hypothesis, description, research_context, prompt_template_id, framework_config_id, scoring_algorithm_id, analysis_mode, status, total_runs, successful_runs, research_notes, publication_status, tags, created_at, updated_at) VALUES (%(creator_id)s, %(name)s, %(hypothesis)s, %(description)s, %(research_context)s, %(prompt_template_id)s, %(framework_config_id)s, %(scoring_algorithm_id)s, %(analysis_mode)s, %(status)s, %(total_runs)s, %(successful_runs)s, %(research_notes)s, %(publication_status)s, %(tags)s::JSON, now(), now()) RETURNING experiment.id, experiment.created_at, experiment.updated_at]
[parameters: {'creator_id': None, 'name': 'Pipeline Test - mft_persuasive_force', 'hypothesis': None, 'description': 'End-to-end pipeline validation test', 'research_context': None, 'prompt_template_id': 'hierarchical_v1', 'framework_config_id': 'mft_persuasive_force', 'scoring_algorithm_id': 'standard', 'analysis_mode': 'single_model', 'status': 'draft', 'total_runs': 0, 'successful_runs': 0, 'research_notes': None, 'publication_status': 'unpublished', 'tags': '[]'}]
(Background on this error at: https://sqlalche.me/e/20/gkpj), using mock storage
   *Manual Intervention Required*: Yes

⚠️ **WARNING**: Real database storage failed: (psycopg2.errors.NotNullViolation) null value in column "selected_models" of relation "experiment" violates not-null constraint
DETAIL:  Failing row contains (25, null, Pipeline Test - moral_rhetorical_posture, null, End-to-end pipeline validation test, null, hierarchical_v1, moral_rhetorical_posture, standard, single_model, null, draft, 0, 0, null, unpublished, [], 2025-06-13 07:21:50.076557, 2025-06-13 07:21:50.076557, null, null, null).

[SQL: INSERT INTO experiment (creator_id, name, hypothesis, description, research_context, prompt_template_id, framework_config_id, scoring_algorithm_id, analysis_mode, status, total_runs, successful_runs, research_notes, publication_status, tags, created_at, updated_at) VALUES (%(creator_id)s, %(name)s, %(hypothesis)s, %(description)s, %(research_context)s, %(prompt_template_id)s, %(framework_config_id)s, %(scoring_algorithm_id)s, %(analysis_mode)s, %(status)s, %(total_runs)s, %(successful_runs)s, %(research_notes)s, %(publication_status)s, %(tags)s::JSON, now(), now()) RETURNING experiment.id, experiment.created_at, experiment.updated_at]
[parameters: {'creator_id': None, 'name': 'Pipeline Test - moral_rhetorical_posture', 'hypothesis': None, 'description': 'End-to-end pipeline validation test', 'research_context': None, 'prompt_template_id': 'hierarchical_v1', 'framework_config_id': 'moral_rhetorical_posture', 'scoring_algorithm_id': 'standard', 'analysis_mode': 'single_model', 'status': 'draft', 'total_runs': 0, 'successful_runs': 0, 'research_notes': None, 'publication_status': 'unpublished', 'tags': '[]'}]
(Background on this error at: https://sqlalche.me/e/20/gkpj), using mock storage
   *Manual Intervention Required*: Yes

⚠️ **WARNING**: Real database storage failed: (psycopg2.errors.NotNullViolation) null value in column "selected_models" of relation "experiment" violates not-null constraint
DETAIL:  Failing row contains (26, null, Pipeline Test - moral_rhetorical_posture, null, End-to-end pipeline validation test, null, hierarchical_v1, moral_rhetorical_posture, standard, single_model, null, draft, 0, 0, null, unpublished, [], 2025-06-13 07:21:56.017411, 2025-06-13 07:21:56.017411, null, null, null).

[SQL: INSERT INTO experiment (creator_id, name, hypothesis, description, research_context, prompt_template_id, framework_config_id, scoring_algorithm_id, analysis_mode, status, total_runs, successful_runs, research_notes, publication_status, tags, created_at, updated_at) VALUES (%(creator_id)s, %(name)s, %(hypothesis)s, %(description)s, %(research_context)s, %(prompt_template_id)s, %(framework_config_id)s, %(scoring_algorithm_id)s, %(analysis_mode)s, %(status)s, %(total_runs)s, %(successful_runs)s, %(research_notes)s, %(publication_status)s, %(tags)s::JSON, now(), now()) RETURNING experiment.id, experiment.created_at, experiment.updated_at]
[parameters: {'creator_id': None, 'name': 'Pipeline Test - moral_rhetorical_posture', 'hypothesis': None, 'description': 'End-to-end pipeline validation test', 'research_context': None, 'prompt_template_id': 'hierarchical_v1', 'framework_config_id': 'moral_rhetorical_posture', 'scoring_algorithm_id': 'standard', 'analysis_mode': 'single_model', 'status': 'draft', 'total_runs': 0, 'successful_runs': 0, 'research_notes': None, 'publication_status': 'unpublished', 'tags': '[]'}]
(Background on this error at: https://sqlalche.me/e/20/gkpj), using mock storage
   *Manual Intervention Required*: Yes

### Visualization

❌ **ERROR**: Visualization creation failed: Invalid format 'html'.
    Supported formats: ['png', 'jpg', 'jpeg', 'webp', 'svg', 'pdf', 'eps', 'json']
   *Manual Intervention Required*: Yes

❌ **ERROR**: Visualization creation failed: Invalid format 'html'.
    Supported formats: ['png', 'jpg', 'jpeg', 'webp', 'svg', 'pdf', 'eps', 'json']
   *Manual Intervention Required*: Yes

❌ **ERROR**: Visualization creation failed: Invalid format 'html'.
    Supported formats: ['png', 'jpg', 'jpeg', 'webp', 'svg', 'pdf', 'eps', 'json']
   *Manual Intervention Required*: Yes

❌ **ERROR**: Visualization creation failed: Invalid format 'html'.
    Supported formats: ['png', 'jpg', 'jpeg', 'webp', 'svg', 'pdf', 'eps', 'json']
   *Manual Intervention Required*: Yes

❌ **ERROR**: Visualization creation failed: Invalid format 'html'.
    Supported formats: ['png', 'jpg', 'jpeg', 'webp', 'svg', 'pdf', 'eps', 'json']
   *Manual Intervention Required*: Yes

❌ **ERROR**: Visualization creation failed: Invalid format 'html'.
    Supported formats: ['png', 'jpg', 'jpeg', 'webp', 'svg', 'pdf', 'eps', 'json']
   *Manual Intervention Required*: Yes

❌ **ERROR**: Visualization creation failed: Invalid format 'html'.
    Supported formats: ['png', 'jpg', 'jpeg', 'webp', 'svg', 'pdf', 'eps', 'json']
   *Manual Intervention Required*: Yes

❌ **ERROR**: Visualization creation failed: Invalid format 'html'.
    Supported formats: ['png', 'jpg', 'jpeg', 'webp', 'svg', 'pdf', 'eps', 'json']
   *Manual Intervention Required*: Yes

❌ **ERROR**: Visualization creation failed: Invalid format 'html'.
    Supported formats: ['png', 'jpg', 'jpeg', 'webp', 'svg', 'pdf', 'eps', 'json']
   *Manual Intervention Required*: Yes

❌ **ERROR**: Visualization creation failed: Invalid format 'html'.
    Supported formats: ['png', 'jpg', 'jpeg', 'webp', 'svg', 'pdf', 'eps', 'json']
   *Manual Intervention Required*: Yes

## Recommended Actions

1. **Address Manual Intervention Points**: Focus on automating components requiring manual intervention
2. **Fix Critical and Error Gaps**: Resolve gaps preventing functionality
3. **Implement Real LLM Analysis**: Replace mock analysis with actual LLM integration
4. **Complete Database Integration**: Implement real database storage operations
5. **Test Full Pipeline**: Re-run tests after implementing fixes

## Next Steps

- [ ] Implement real LLM analysis service integration
- [ ] Complete database storage implementation
- [ ] Automate all manual intervention points
- [ ] Re-run comprehensive pipeline tests
- [ ] Achieve 100% success rate with zero manual interventions

## Implementation Priority

1. **HIGH**: Replace mock LLM analysis with real implementation
2. **MEDIUM**: Complete database storage operations
3. **LOW**: Optimize academic export and visualization components
