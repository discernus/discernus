# Comprehensive Experiment Orchestrator Specification

**Date:** June 14, 2025  
**Status:** MISSING - Needs Implementation  
**Priority:** CRITICAL for Research Workflow  

## Overview

The Narrative Gravity Analysis platform needs a **single, comprehensive experiment orchestrator** that handles the complete experiment lifecycle from definition to final outputs, with automatic component registration and graceful error handling.

## Current Problem

Researchers currently face a fragmented workflow:
- ❌ Manual component registration required
- ❌ No automatic framework/template ingestion  
- ❌ Experiment context lost during pipeline execution
- ❌ Multiple tools required for single experiment
- ❌ Poor error messages when components missing
- ❌ No validation of corpus file integrity

## Required Solution

### Single Command Interface
```bash
python3 scripts/comprehensive_experiment_orchestrator.py experiment_definition.json [--dry-run] [--force-reregister]
```

## Enhanced Experiment Definition Format

### Complete JSON Schema
```json
{
  "experiment": {
    "name": "IDITI Framework Validation Study",
    "version": "1.0.0",
    "description": "Three-hypothesis validation of IDITI framework",
    "hypotheses": [
      {
        "id": "discriminative_validity", 
        "description": "Framework can distinguish dignity from tribalism rhetoric",
        "success_criteria": {
          "dignity_threshold": 0.6,
          "tribalism_threshold": 0.6,
          "significance_level": 0.05
        }
      },
      {
        "id": "ideological_agnosticism",
        "description": "Framework scores content rather than political orientation", 
        "success_criteria": {
          "similarity_threshold": 0.8,
          "significance_level": 0.05
        }
      },
      {
        "id": "ground_truth_alignment",
        "description": "Pre-labeled texts match expected framework responses",
        "success_criteria": {
          "extreme_controls_threshold": 0.8,
          "alignment_correlation": 0.7
        }
      }
    ],
    "research_context": "Validation study for specialized identity-focused framework",
    "expected_outcomes": {
      "primary": "Framework validation across three hypotheses",
      "secondary": "Reliability metrics and academic publication package"
    }
  },
  
  "components": {
    "frameworks": [
      {
        "id": "iditi",
        "version": "v2025.06.14",
        "type": "file_path",
        "file_path": "frameworks/iditi/framework.json",
        "expected_hash": "sha256:abc123...",
        "required": true
      }
    ],
    
    "prompt_templates": [
      {
        "id": "traditional_analysis", 
        "version": "v2.1.0",
        "type": "file_path",
        "file_path": "prompts/templates/traditional_analysis_v2.1.0.json",
        "expected_hash": "sha256:def456...",
        "required": true
      }
    ],
    
    "weighting_schemes": [
      {
        "id": "linear_traditional",
        "version": "v2.1.0", 
        "type": "file_path",
        "file_path": "weighting/linear_traditional_v2.1.0.json",
        "expected_hash": "sha256:ghi789...",
        "required": true
      }
    ],
    
    "models": [
      {
        "id": "gpt-4o",
        "provider": "openai",
        "parameters": {
          "temperature": 0.1,
          "max_tokens": 4000
        },
        "cost_estimate_per_run": 0.0056
      }
    ]
  },
  
  "corpus": {
    "sources": [
      {
        "id": "validation_set_dignity_texts",
        "type": "file_collection",
        "file_paths": [
          "corpus/validation_set/conservative_dignity/*.txt",
          "corpus/validation_set/progressive_dignity/*.txt"
        ],
        "expected_count": 12,
        "content_hash_manifest": "corpus/validation_set/dignity_texts_manifest.json"
      },
      {
        "id": "validation_set_tribalism_texts", 
        "type": "file_collection",
        "file_paths": [
          "corpus/validation_set/conservative_tribalism/*.txt",
          "corpus/validation_set/progressive_tribalism/*.txt"
        ],
        "expected_count": 12,
        "content_hash_manifest": "corpus/validation_set/tribalism_texts_manifest.json"
      },
      {
        "id": "validation_set_controls",
        "type": "file_collection", 
        "file_paths": [
          "corpus/validation_set/extreme_controls/*.txt",
          "corpus/validation_set/mixed_controls/*.txt"
        ],
        "expected_count": 8,
        "content_hash_manifest": "corpus/validation_set/controls_manifest.json"
      }
    ]
  },
  
  "execution": {
    "design_matrix": {
      "type": "full_factorial",
      "dimensions": ["texts", "frameworks", "models"],
      "replication": {
        "runs_per_combination": 1,
        "randomize_order": false
      }
    },
    "quality_assurance": {
      "enabled": true,
      "confidence_threshold": 0.7,
      "validate_all_runs": true
    },
    "cost_controls": {
      "max_total_cost": 0.50,
      "confirm_before_execution": true
    }
  },
  
  "outputs": {
    "hypothesis_validation": {
      "enabled": true,
      "statistical_tests": ["t_test", "anova", "correlation"],
      "significance_level": 0.05,
      "effect_size_reporting": true
    },
    "academic_export": {
      "formats": ["csv", "feather", "json", "stata_dta"],
      "include_replication_package": true,
      "include_analysis_templates": ["jupyter", "r", "stata"]
    },
    "visualizations": {
      "hypothesis_aware": true,
      "include_validation_plots": true,
      "publication_ready": true
    }
  }
}
```

## Orchestrator Implementation Requirements

### 1. Pre-Flight Validation
```python
class ComprehensiveExperimentOrchestrator:
    def validate_experiment_definition(self, experiment_def):
        """Comprehensive validation before execution."""
        
        # Validate JSON schema
        self.validate_schema(experiment_def)
        
        # Check all components
        missing_components = []
        
        # Frameworks
        for framework in experiment_def['components']['frameworks']:
            if not self.framework_exists(framework['id'], framework['version']):
                if framework['type'] == 'file_path':
                    if not self.validate_file_hash(framework['file_path'], framework['expected_hash']):
                        missing_components.append(f"Framework file hash mismatch: {framework['file_path']}")
                    else:
                        self.register_framework(framework)
                else:
                    missing_components.append(f"Framework not found: {framework['id']} v{framework['version']}")
        
        # Prompt Templates
        for template in experiment_def['components']['prompt_templates']:
            if not self.template_exists(template['id'], template['version']):
                if template['type'] == 'file_path':
                    if not self.validate_file_hash(template['file_path'], template['expected_hash']):
                        missing_components.append(f"Template file hash mismatch: {template['file_path']}")
                    else:
                        self.register_template(template)
                else:
                    missing_components.append(f"Prompt template not found: {template['id']} v{template['version']}")
        
        # Weighting Schemes  
        for scheme in experiment_def['components']['weighting_schemes']:
            if not self.scheme_exists(scheme['id'], scheme['version']):
                if scheme['type'] == 'file_path':
                    if not self.validate_file_hash(scheme['file_path'], scheme['expected_hash']):
                        missing_components.append(f"Weighting scheme file hash mismatch: {scheme['file_path']}")
                    else:
                        self.register_scheme(scheme)
                else:
                    missing_components.append(f"Weighting scheme not found: {scheme['id']} v{scheme['version']}")
        
        # Corpus Texts with Hash Validation
        for corpus_source in experiment_def['corpus']['sources']:
            manifest_path = corpus_source['content_hash_manifest']
            if not self.validate_corpus_integrity(corpus_source, manifest_path):
                missing_components.append(f"Corpus integrity check failed: {corpus_source['id']}")
            else:
                self.ingest_corpus_source(corpus_source)
        
        # Models (check availability)
        for model in experiment_def['components']['models']:
            if not self.model_available(model['id'], model['provider']):
                missing_components.append(f"Model not available: {model['id']} from {model['provider']}")
        
        if missing_components:
            self.generate_helpful_error_message(missing_components)
            raise MissingComponentsError(missing_components)
```

### 2. Graceful Error Handling
```python
def generate_helpful_error_message(self, missing_components):
    """Generate helpful error message with specific guidance."""
    
    print("🚨 EXPERIMENT VALIDATION FAILED")
    print("=" * 60)
    print("The following components are missing or invalid:")
    print()
    
    for component in missing_components:
        print(f"❌ {component}")
        
        # Provide specific guidance
        if "Framework" in component:
            print("   💡 To add framework:")
            print("      1. Place framework.json in frameworks/{framework_id}/")
            print("      2. Update expected_hash in experiment definition")
            print("      3. See examples/frameworks/ for format")
            
        elif "Template" in component:
            print("   💡 To add prompt template:")
            print("      1. Place template.json in prompts/templates/")
            print("      2. Update expected_hash in experiment definition") 
            print("      3. See prompts/templates/examples/ for format")
            
        elif "Weighting" in component:
            print("   💡 To add weighting scheme:")
            print("      1. Place scheme.json in weighting/")
            print("      2. Update expected_hash in experiment definition")
            print("      3. See weighting/examples/ for format")
            
        elif "Corpus" in component:
            print("   💡 To fix corpus integrity:")
            print("      1. Verify all files exist at specified paths")
            print("      2. Regenerate content hash manifest")
            print("      3. Update expected_count if files added/removed")
            
        print()
    
    print("📚 Documentation: docs/experiment-definitions/")
    print("🔧 Examples: examples/experiments/")
    print("❓ Support: See TROUBLESHOOTING.md")
```

### 3. Context Propagation
```python
class ExperimentContext:
    """Maintains experiment context throughout pipeline."""
    
    def __init__(self, experiment_def):
        self.experiment_name = experiment_def['experiment']['name']
        self.hypotheses = experiment_def['experiment']['hypotheses']
        self.expected_outcomes = experiment_def['experiment']['expected_outcomes']
        self.research_context = experiment_def['experiment']['research_context']
        
    def enrich_analysis_request(self, analysis_request):
        """Add experiment context to analysis requests."""
        analysis_request['experiment_context'] = {
            'experiment_name': self.experiment_name,
            'hypotheses': self.hypotheses,
            'research_context': self.research_context
        }
        return analysis_request
        
    def enrich_output_generation(self, output_config):
        """Add experiment context to output generation."""
        output_config['experiment_context'] = {
            'hypotheses': self.hypotheses,
            'expected_outcomes': self.expected_outcomes,
            'validation_criteria': self.get_validation_criteria()
        }
        return output_config
```

## Implementation Priority

### Phase 1: Core Orchestrator (CRITICAL)
- [ ] Basic experiment definition validation
- [ ] Component existence checking
- [ ] Graceful error messages
- [ ] Single-command execution

### Phase 2: Auto-Registration (HIGH)
- [ ] Framework auto-registration from files
- [ ] Prompt template auto-registration
- [ ] Weighting scheme auto-registration
- [ ] Hash validation for all components

### Phase 3: Corpus Management (HIGH)  
- [ ] Corpus integrity checking
- [ ] Hash manifest validation
- [ ] Auto-ingestion with metadata
- [ ] File collection handling

### Phase 4: Context Propagation (MEDIUM)
- [ ] Experiment context tracking
- [ ] Hypothesis-aware analysis
- [ ] Research context in outputs
- [ ] Validation criteria propagation

### Phase 5: Advanced Features (LOW)
- [ ] Dependency resolution
- [ ] Component versioning
- [ ] Rollback capabilities
- [ ] Experiment templates

## Success Criteria

The orchestrator is successful when:
- ✅ Single command executes complete experiment
- ✅ Clear error messages for missing components  
- ✅ Automatic component registration works
- ✅ Experiment context preserved throughout
- ✅ Hypothesis validation in final outputs
- ✅ Zero manual intervention required for valid experiments

---

**This specification addresses the critical gap identified in the failure analysis and provides a roadmap for implementing the missing comprehensive orchestrator.** 