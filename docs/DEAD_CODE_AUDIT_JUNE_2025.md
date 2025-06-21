# Dead Code Audit Report - June 20, 2025 (Revised)
*Systematic analysis of unused src/ components after architectural breakthrough*

## 🎯 **Executive Summary - REVISED**

Following the **unified framework architecture breakthrough**, a systematic audit was conducted to identify obsolete code. Initial findings suggested 57.6% of modules were dead. However, a deeper strategic review revealed that many of these modules are **critical supporting utilities** for the project's immediate goal of academic validation and publication.

This revised audit re-categorizes these modules, providing a more accurate picture of the codebase. The new focus is on archiving components related to a deprecated web-interface architecture, while promoting essential academic and utility modules for integration.

---

## 📊 **Audit Statistics - REVISED**

| Metric | Count | Percentage |
|--------|-------|------------|
| **Total `src/` modules** | 59 | 100% |
| **Production-critical modules** | 17 | 28.8% |
| **Supporting Tools to Integrate** | 12 | 20.3% |
| **Modules to Archive/Remove** | 30 | 50.8% |

**Revised Action**: Archive/remove **50.8%** of modules, integrate **20.3%** into the production pipeline.

---

## ✅ **Modules to Keep & Integrate**

### **Production Core (17 modules)**
*(This list remains unchanged)*

### **Supporting Research & Publication Tools (8 modules) - TO INTEGRATE**
These modules are essential for the academic validation and publication workflow.

- `corpus.discovery`: Corpus exploration and search.
- `corpus.exporter`: Creation of replication packages and academic datasets.
- `corpus.validator`: Corpus integrity and FAIR compliance validation.
- `corpus.youtube_ingestion`: Specialized ingestion for video-based corpora.
- `academic.analysis_templates`: Automated generation of R/Python/Stata analysis scripts.
- `academic.documentation`: Automated generation of methodology and results sections for papers.

### **Core Project Utilities (4 modules) - TO INTEGRATE**
These modules provide critical, cross-cutting functionality for finance, security, and presentation.

- `utils.cost_manager`: Essential cost-control and financial safety management.
- `utils.manage_costs`: CLI for the cost management utility.
- `utils.api_retry_handler`: Critical resilience component for all API calls.
- `visualization.themes`: Centralized styling for professional, publication-ready plots.

---

## 🗑️ **Modules to Archive or Remove (30 modules)**

### **1. Entire CLI System** ❌ **TO REMOVE (15 modules)**
The legacy CLI system is fully superseded by the `comprehensive_experiment_orchestrator.py`.
*(List of 15 modules remains the same)*
```
cli.academic_analysis_pipeline
cli.academic_pipeline
cli.analyze_batch
cli.component_manager
cli.dev_session
cli.export_academic_data
cli.generate_analysis_templates
cli.generate_documentation
cli.jsonl_generator
cli.log_iteration
cli.manage_components
cli.schema_generator
cli.start_dev_session
cli.validate_component
```

### **2. Abandoned Web Application Components** 🗄️ **TO ARCHIVE (8 modules)**
This code is well-designed for a web front-end but is not used by the current synchronous pipeline. It should be **archived** for potential future use.

- `api.auth`, `api.crud`, `api.main`, `api.services`: The core web server.
- `utils.auth`: User authentication and JWT token handling.
- `utils.sanitization`: Security module for web inputs.
- `celery_app`: Asynchronous task queue application.
- `tasks/` directory (2 modules): Background job definitions.

### **3. Deprecated Development & Utility Tools** ❌ **TO REMOVE (7 modules)**
These tools have been replaced by functionality within the production core or the modules listed above.
```
development.quality_assurance
development.seed_prompts
development.session_manager
prompts.template_manager
```

---

## 🎯 **Revised Cleanup Recommendations**

### **Immediate Actions (High Confidence)**
1.  **Archive Web Application Components**: Move the 8 modules related to the web interface and task queue system to `deprecated/by-system/`. This preserves their value while cleaning the `src/` directory.
    - `git mv src/narrative_gravity/api/auth.py deprecated/by-system/web_app/`
    - `git mv src/narrative_gravity/celery_app.py deprecated/by-system/web_app/`
    - etc.
2.  **Remove Legacy CLI System**: Delete the 15 modules in `src/narrative_gravity/cli/`, as they are fully replaced.
3.  **Remove Deprecated Dev Tools**: Delete the remaining development and utility tools that are no longer needed.

### **Integration Work (Next Steps)**
1.  **Integrate Utilities**: Explicitly call the `cost_manager`, `validator`, and `exporter` from the main orchestrator script at the appropriate stages.
2.  **Formalize Dependencies**: Ensure that `api_retry_handler` is correctly treated as a production dependency for the `direct_api_client`.
3.  **Enhance Reporting**: Use the `academic.documentation` and `visualization.themes` modules in the post-processing phase to automate the creation of publication-ready reports.

---

## 🚀 **Post-Cleanup Architecture**

### **Target: ~29 Core & Supporting Modules** (from 59)
The new architecture will consist of the 17 production-critical modules plus the 12 supporting tools, creating a lean but powerful, academically-focused codebase.

**Benefits:**
- **51% code reduction** in the active `src/` directory.
- **Clearer Architecture**: Production core is distinct from supporting tools.
- **Preserved Value**: Code for a potential web front-end is safely archived.
- **Accelerated Research**: Integrated tools for validation, publication, and cost management.

---

*This document was revised on June 20, 2025, to reflect a deeper strategic analysis of module utility in service of the project's academic validation goals.* 