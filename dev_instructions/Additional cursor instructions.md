# A. Schema and Data Model Finalization
**Where to Edit/Add:**
* schemas/
  * Add semantic versioning to filenames (e.g., core_schema_v1.0.0.json) and update the $id and schema_version fields inside each schema file101.
  * Place migration scripts in schemas/migrations/ (create this subfolder if it does not exist)10.
  * Document schema versioning and migration process in schemas/README.md (create if missing)10.
* corpus/golden_set/
  * Ensure test records here cover all schema fields and chunking strategies1.
* /docs/ERD/
  * Store your ER diagram export here10.

⠀
# B. Integration and Monitoring
**Where to Edit/Add:**
* src/api/health.py
  * Implement and extend /api/health and /api/health/history endpoints for system and dependency checks14.
* src/services/cost_tracker.py
  * Add cost-tracking logic, budget thresholds, and alerting hooks1.
* src/api/views/
  * Extend admin UI to display real-time cost meter and health status1.

⠀
# C. Failure-Mode Handling
**Where to Edit/Add:**
* src/tasks/processing.py
  * Implement exponential backoff, retries, and persistent failure handling14.
  * Add admin notification logic for repeated failures.
* src/models/task.py
  * Ensure task state and error logging fields are present.
* src/api/jobs.py
  * Add /api/jobs/{job_id}/resume endpoint for resumability1.
* tests/
  * Add tests for failure modes and job/task resumption (e.g., test_job_lifecycle.py)1.

⠀
# D. Security and Access Control
**Where to Edit/Add:**
* src/api/ (all endpoints)
  * Enforce token-based authentication and role checks111.
* src/utils/validation.py
  * Ensure all input validation and sanitization logic is present and up-to-date111.
* .env
  * Store secrets (DB, API keys, etc.) here; ensure .env is in .gitignore11.
* README.md
  * Document secrets management and rotation policy11.

⠀
# E. Documentation and Developer Experience
**Where to Edit/Add:**
* README.md
  * Keep setup, schema, and migration instructions current13.
* schemas/README.md
  * Document schema evolution, migration, and versioning policy10.
* src/cli/generate_jsonl.py
  * Ensure CLI help text and error messages are clear; add usage examples.
* CONTRIBUTING.md (create at project root if missing)
  * Outline code standards, testing, and schema evolution policy.

⠀
# F. Framework Extensibility
**Where to Edit/Add:**
* schemas/
  * Place new extension schemas here; update registry logic to auto-discover13.
* src/frameworks/ (create if missing)
  * Store framework extension templates and onboarding docs.
* tests/
  * Add test harnesses for framework validation (e.g., test_framework_extension.py).
* docs/development/
  * Add a “Framework Extension Guide” for third-party developers.

⠀
# G. Data Export and Replication
**Where to Edit/Add:**
* src/api/jobs.py or src/api/export.py (create if missing)
  * Implement /api/export endpoints for raw and aggregated results14.
* src/services/
  * Add logic for CSV/JSON export formatting.
* docs/
  * Add “Replication Package Guide” for academic users.

⠀
# H. Hugging Face API Robustness
**Where to Edit/Add:**
* src/services/huggingface_client.py
  * Implement rate limit detection, backoff, and version checks14.
* src/api/health.py
  * Extend health checks to include Hugging Face API version and quota status.

⠀
# I. Admin UI Scalability
**Where to Edit/Add:**
* src/api/views/
  * Modularize dashboard, cost meter, error logs, and job queue components.

⠀
# J. Schema Migration Complexity
**Where to Edit/Add:**
* schemas/migrations/
  * Store all migration scripts here10.
* schemas/README.md
  * Maintain registry of schema versions and migration scripts10.
* tests/
  * Add tests for migration correctness using golden set data.

⠀
# K. Testing and Monitoring
**Where to Edit/Add:**
* tests/
  * Add/expand tests for CI coverage, golden set regression, and performance benchmarks13.
* src/services/ or src/utils/
  * Add structured logging utilities.
* src/api/health.py
  * Integrate alerting for health failures.

⠀
# New Documents to Add
| **Document Name** | **Location** | **Purpose** |
|:-:|:-:|:-:|
| schemas/README.md | schemas/ | Schema versioning, migration, and extension documentation10 |
| schemas/migrations/ | schemas/ | Store all schema migration scripts10 |
| CONTRIBUTING.md | Project root | Code, schema, and testing standards |
| docs/ERD/ | docs/ | Store canonical ER diagrams10 |
| docs/development/frameworks.md | docs/development/ | Guide for adding/extending frameworks |
| docs/replication_package.md | docs/ | Instructions for academic replication and export |


# Summary Table: Where to Put Each Addition
| **Recommendation Area** | **File/Folder(s) to Edit or Create** |
|:-:|:-:|
| Schema versioning/migration | schemas/, schemas/migrations/, schemas/README.md |
| Golden set coverage | corpus/golden_set/ |
| ER diagram | docs/ERD/ |
| Health/cost monitoring | src/api/health.py, src/services/cost_tracker.py, src/api/views/ |
| Failure modes | src/tasks/processing.py, src/models/task.py, src/api/jobs.py, tests/ |
| Security/auth | src/api/, src/utils/validation.py, .env, README.md |
| Documentation | README.md, schemas/README.md, CONTRIBUTING.md |
| Framework extensibility | schemas/, src/frameworks/, tests/, docs/development/frameworks.md |
| Data export/replication | src/api/export.py, src/services/, docs/replication_package.md |
| Hugging Face robustness | src/services/huggingface_client.py, src/api/health.py |
| Admin UI scalability | src/api/views/ |
| Schema migration registry | schemas/migrations/, schemas/README.md, tests/ |
| Testing/monitoring | tests/, src/services/, src/api/health.py |

#personal/writing/narrativegravity