#!/usr/bin/env python3
"""
TPM Blocking Demonstration
===========================

Creates an experiment that WILL be blocked by TPM validation to show the system in action.
"""

import os
import sys
import tempfile
import yaml
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

def create_massive_corpus():
    """Create a corpus file that will definitely trigger TPM blocking"""
    
    test_corpus_dir = project_root / "tmp" / "massive_test_corpus"
    test_corpus_dir.mkdir(parents=True, exist_ok=True)
    
    # Create a massive text that will exceed even high TPM limits
    base_text = """
    The foundation of democratic governance rests upon the principle that legitimate authority derives from the consent of the governed. This fundamental tenet requires that those entrusted with power act with integrity, transparency, and unwavering commitment to the common good. When leaders prioritize personal gain over public service, they violate the sacred trust placed in them by the citizenry and undermine the very institutions they are sworn to protect.
    
    Throughout history, societies have grappled with the delicate balance between individual liberty and collective responsibility. The moral foundations that guide our judgments about right and wrong are deeply embedded in our cultural fabric, influencing everything from personal relationships to political discourse. Care for others, fairness in treatment, loyalty to groups, respect for authority, and concerns about purity all play crucial roles in shaping our moral landscape.
    
    In the modern era, these timeless principles face new challenges as technology reshapes human interaction and globalization brings diverse moral systems into contact. The question becomes: how do we maintain our moral bearings while adapting to an ever-changing world? The answer lies not in rigid adherence to tradition nor in wholesale abandonment of proven principles, but in thoughtful engagement with both our inherited wisdom and emerging realities.
    """
    
    # Repeat this text many times to create a massive corpus
    massive_text = base_text * 500  # This should create roughly 50,000+ tokens
    
    with open(test_corpus_dir / "massive_text.txt", "w", encoding="utf-8") as f:
        f.write(massive_text)
    
    return test_corpus_dir

def create_blocked_experiment():
    """Create an experiment that should be blocked by TPM validation"""
    
    return {
        "experiment_meta": {
            "name": "Massive Blocked Experiment",
            "description": "An experiment designed to be blocked by TPM validation",
            "version": "1.0.0",
            "tags": ["test", "tpm", "blocked", "demonstration"]
        },
        "components": {
            "frameworks": [{
                "id": "test_framework",
                "name": "test_framework",
                "version": "1.0",
                "file_path": "./tmp/test_framework.yaml"
            }],
            "models": [{
                "name": "gpt-4o",  # Low TPM model (30K TPM)
                "provider": "openai"
            }],
            "corpus": {
                "name": "Massive Test Corpus",
                "path": "./tmp/massive_test_corpus/massive_text.txt",
                "pattern": "*.txt"
            }
        }
    }

def test_tpm_blocking():
    """Test that TPM validation properly blocks oversized experiments"""
    
    print("🧪 TESTING TPM BLOCKING BEHAVIOR")
    print("This test demonstrates how the system prevents expensive failures.")
    print("=" * 70)
    
    try:
        from scripts.applications.experiment_tpm_validator import ExperimentTPMValidator
        
        # Create massive corpus
        print("📝 Creating massive corpus...")
        test_corpus_dir = create_massive_corpus()
        print(f"   ✅ Massive corpus created at: {test_corpus_dir}")
        
        # Create blocked experiment configuration
        print("\n📋 Creating experiment designed to be blocked...")
        config = create_blocked_experiment()
        
        # Initialize validator
        validator = ExperimentTPMValidator()
        
        print(f"\n🔍 RUNNING TPM VALIDATION ON MASSIVE EXPERIMENT")
        print("=" * 60)
        
        # Create temporary experiment file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as tmp_file:
            yaml.dump(config, tmp_file, default_flow_style=False)
            tmp_file.flush()
            
            try:
                # Run validation
                result = validator.validate_experiment(Path(tmp_file.name))
                
                # Print detailed results
                validator.print_validation_report(result, Path(tmp_file.name))
                
                # Analyze results
                print(f"\n🎯 ANALYSIS:")
                if result.is_feasible:
                    print("   ⚠️ Unexpected: Experiment was NOT blocked")
                    print("   • This might indicate the corpus wasn't large enough")
                    print("   • Or the model's TPM limit is higher than expected")
                else:
                    print("   ✅ Expected: Experiment was BLOCKED by TPM validation")
                    print("   • This prevented an expensive failure")
                    print("   • User gets actionable suggestions instead")
                
                print(f"\n💡 ACTIONABLE ALTERNATIVES PROVIDED:")
                if result.suggested_models:
                    print(f"   • {len(result.suggested_models)} alternative models suggested")
                    for model in result.suggested_models[:3]:
                        tpm = validator.get_model_tpm_limit(model)
                        cost = validator.get_model_cost(model)
                        print(f"     - {model} (TPM: {tpm:,}, Cost: ${cost:.4f}/1K)")
                
                if result.suggested_corpus_modifications:
                    print(f"   • {len(result.suggested_corpus_modifications)} corpus modifications suggested")
                    for mod in result.suggested_corpus_modifications[:2]:
                        print(f"     - {mod}")
                
                if result.suggested_batching_strategy:
                    strategy = result.suggested_batching_strategy
                    print(f"   • Batching strategy suggested:")
                    print(f"     - Split into {strategy['estimated_chunks']} chunks")
                    print(f"     - Use {strategy['aggregation_method']} for results")
                
                return not result.is_feasible  # Return True if blocked (expected)
                
            finally:
                # Clean up temporary file
                os.unlink(tmp_file.name)
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test execution"""
    
    print("🚀 TPM BLOCKING DEMONSTRATION")
    print("This demonstrates how upfront TPM validation prevents expensive failures.")
    print()
    
    blocked_as_expected = test_tpm_blocking()
    
    if blocked_as_expected:
        print("\n" + "=" * 70)
        print("🎉 SUCCESS: TPM validation working as expected!")
        print()
        print("✅ Key Benefits Demonstrated:")
        print("   • Prevents expensive API failures before they happen")
        print("   • Provides actionable alternatives (better models, smaller corpus)")
        print("   • Gives realistic time and cost estimates")
        print("   • Suggests text chunking strategies for large corpora")
        print()
        print("🔧 Integration Status:")
        print("   • TPM validation now runs automatically in experiment orchestrator")
        print("   • Experiments are blocked BEFORE any API calls are made")
        print("   • Users get helpful guidance instead of cryptic rate limit errors")
    else:
        print("\n❌ Unexpected result - check configuration or test corpus size")
    
    return 0 if blocked_as_expected else 1

if __name__ == "__main__":
    sys.exit(main()) 