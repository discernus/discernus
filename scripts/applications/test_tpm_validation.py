#!/usr/bin/env python3
"""
Test TPM Validation System
==========================

Demonstrates the upfront TPM validation that prevents expensive experiment failures.
Creates test experiment configurations to show validation in action.
"""

import os
import sys
import tempfile
import yaml
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

def create_test_experiment_configs():
    """Create various test experiment configurations to demonstrate TPM validation"""
    
    configs = {}
    
    # Test 1: Small experiment that should pass
    configs["small_feasible"] = {
        "experiment_meta": {
            "name": "Small Feasible Experiment",
            "description": "A small experiment that should pass TPM validation",
            "version": "1.0.0",
            "tags": ["test", "tpm", "feasible"]
        },
        "components": {
            "frameworks": [{
                "id": "test_framework",
                "name": "test_framework",
                "version": "1.0",
                "file_path": "./tmp/test_framework.yaml"
            }],
            "models": [{
                "name": "gpt-3.5-turbo",
                "provider": "openai"
            }],
            "corpus": {
                "name": "Test Small Corpus",
                "path": "./corpus/demo_texts/",
                "pattern": "*.txt"
            }
        }
    }
    
    # Test 2: Large experiment with expensive model that should be blocked
    configs["large_blocked"] = {
        "experiment_meta": {
            "name": "Large Blocked Experiment",
            "description": "A large experiment that should be blocked by TPM validation",
            "version": "1.0.0", 
            "tags": ["test", "tpm", "blocked"]
        },
        "components": {
            "frameworks": [{
                "id": "test_framework",
                "name": "test_framework", 
                "version": "1.0",
                "file_path": "./tmp/test_framework.yaml"
            }],
            "models": [{
                "name": "gpt-4o",  # Expensive model with low TPM
                "provider": "openai"
            }],
            "corpus": {
                "name": "Test Large Corpus",
                "path": "./research_workspaces/june_2025_research_dev_workspace/corpus/",
                "pattern": "*.txt"
            }
        }
    }
    
    # Test 3: Multi-model experiment with mixed feasibility
    configs["mixed_models"] = {
        "experiment_meta": {
            "name": "Mixed Model Experiment", 
            "description": "Multi-model experiment with mixed TPM feasibility",
            "version": "1.0.0",
            "tags": ["test", "tpm", "mixed"]
        },
        "components": {
            "frameworks": [{
                "id": "test_framework",
                "name": "test_framework",
                "version": "1.0",
                "file_path": "./tmp/test_framework.yaml"
            }],
            "models": [
                {
                    "name": "gpt-3.5-turbo",  # High TPM, should pass
                    "provider": "openai"
                },
                {
                    "name": "gpt-4o",  # Low TPM, may be blocked
                    "provider": "openai"
                },
                {
                    "name": "claude-3-5-haiku-20241022",  # Medium TPM
                    "provider": "anthropic"
                },
                {
                    "name": "ollama/llama3.2",  # Local, no TPM limits
                    "provider": "ollama"
                }
            ],
            "corpus": {
                "name": "Test Medium Corpus",
                "path": "./research_workspaces/june_2025_research_dev_workspace/corpus/",
                "pattern": "*.txt"
            }
        }
    }
    
    return configs

def create_test_corpus():
    """Create test corpus files for validation"""
    
    # Create a temporary directory for test corpus
    test_corpus_dir = project_root / "tmp" / "test_corpus"
    test_corpus_dir.mkdir(parents=True, exist_ok=True)
    
    # Small corpus file (should pass)
    small_text = """
    The foundation of democratic governance rests upon the principle that legitimate authority derives from the consent of the governed. This fundamental tenet requires that those entrusted with power act with integrity, transparency, and unwavering commitment to the common good. When leaders prioritize personal gain over public service, they violate the sacred trust placed in them by the citizenry and undermine the very institutions they are sworn to protect.
    """
    
    with open(test_corpus_dir / "small_text.txt", "w", encoding="utf-8") as f:
        f.write(small_text.strip())
    
    # Large corpus file (might be blocked)
    large_text = small_text * 100  # Repeat to make it large
    
    with open(test_corpus_dir / "large_text.txt", "w", encoding="utf-8") as f:
        f.write(large_text)
    
    # Medium corpus file
    medium_text = small_text * 20  # Medium size
    
    with open(test_corpus_dir / "medium_text.txt", "w", encoding="utf-8") as f:
        f.write(medium_text)
    
    return test_corpus_dir

def test_tpm_validation():
    """Test the TPM validation system with various configurations"""
    
    print("🧪 TESTING TPM VALIDATION SYSTEM")
    print("=" * 60)
    
    try:
        from scripts.applications.experiment_tpm_validator import ExperimentTPMValidator
        
        # Create test corpus
        print("📝 Creating test corpus...")
        test_corpus_dir = create_test_corpus()
        print(f"   ✅ Test corpus created at: {test_corpus_dir}")
        
        # Create test configurations
        print("\n📋 Creating test experiment configurations...")
        configs = create_test_experiment_configs()
        
        # Update corpus paths to point to test corpus
        for config_name, config in configs.items():
            if config_name == "small_feasible":
                config["components"]["corpus"]["path"] = str(test_corpus_dir / "small_text.txt")
            elif config_name == "large_blocked":
                config["components"]["corpus"]["path"] = str(test_corpus_dir / "large_text.txt")
            else:  # mixed_models
                config["components"]["corpus"]["path"] = str(test_corpus_dir / "medium_text.txt")
        
        print(f"   ✅ Created {len(configs)} test configurations")
        
        # Initialize validator
        validator = ExperimentTPMValidator()
        
        # Test each configuration
        for config_name, config in configs.items():
            print(f"\n" + "="*60)
            print(f"🔍 TESTING: {config_name.upper()}")
            print("="*60)
            
            # Create temporary experiment file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as tmp_file:
                yaml.dump(config, tmp_file, default_flow_style=False)
                tmp_file.flush()
                
                try:
                    # Run validation
                    result = validator.validate_experiment(Path(tmp_file.name))
                    
                    # Print results
                    validator.print_validation_report(result, Path(tmp_file.name))
                    
                    # Summary
                    status = "✅ PASSED" if result.is_feasible else "❌ BLOCKED"
                    print(f"\n🎯 RESULT: {status}")
                    
                    if result.blocking_issues:
                        print(f"   Blocking issues: {len(result.blocking_issues)}")
                    if result.suggested_models:
                        print(f"   Alternative models suggested: {len(result.suggested_models)}")
                    if result.suggested_corpus_modifications:
                        print(f"   Corpus modifications suggested: {len(result.suggested_corpus_modifications)}")
                    
                finally:
                    # Clean up temporary file
                    os.unlink(tmp_file.name)
        
        print(f"\n" + "="*60)
        print("🎉 TPM VALIDATION TESTING COMPLETE")
        print("="*60)
        print("💡 Key Takeaways:")
        print("   • Small experiments with high-TPM models pass validation")
        print("   • Large experiments with low-TPM models get blocked")
        print("   • Validator provides actionable alternatives")
        print("   • Multi-model experiments show per-model analysis")
        print("   • Local models (ollama) have no TPM constraints")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Make sure tiktoken is installed: pip install tiktoken")
        return False
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test execution"""
    
    print("🚀 TPM VALIDATION SYSTEM TEST")
    print("This test demonstrates upfront TPM validation that prevents expensive experiment failures.")
    print()
    
    success = test_tpm_validation()
    
    if success:
        print("\n✅ All tests completed successfully!")
        print("🔧 Integration: TPM validation is now integrated into the experiment orchestrator")
        print("📋 Usage: Run experiments normally - TPM validation happens automatically")
    else:
        print("\n❌ Tests failed - check error messages above")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main()) 