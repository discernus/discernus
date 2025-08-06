#!/usr/bin/env python3
"""
Systematic validation of all v7.3 frameworks using the coherence agent.
"""

import os
import subprocess
import sys
from pathlib import Path

# All v7.3 frameworks to validate
FRAMEWORKS = [
    "frameworks/reference/core/caf_v7.3.md",
    "frameworks/reference/core/chf_v7.3.md", 
    "frameworks/reference/core/ecf_v7.3.md",
    "frameworks/reference/flagship/cff_v7.3.md",
    "frameworks/reference/flagship/pdaf_v7.3.md",
    "frameworks/seed/communication/entman_v7.3.md",
    "frameworks/seed/communication/lakoff_framing_v7.3.md",
    "frameworks/seed/ethics/business_ethics_v7.3.md",
    "frameworks/seed/ethics/iditi_v7.3.md",
    "frameworks/seed/political/moral_foundations_theory_v7.3.md",
    "frameworks/seed/political/political_discourse_populism_v7.3.md",
    "frameworks/seed/political/political_discourse_v7.3.md",
    "frameworks/seed/political/political_worldview_triad_v7.3.md",
    "frameworks/seed/political/populism_pluralism_v7.3.md",
    "frameworks/seed/temporal/prm_v7.3.md",
    "frameworks/star_wars_bar/exotic_frameworks/nested_nightmare_v7.3.md"
]

def create_test_experiment(framework_path):
    """Create a minimal test experiment for framework validation."""
    experiment_content = f'''---
name: "framework_validation_test"
description: "Testing v7.3 framework validation"
framework: "../{framework_path}"
corpus: "corpus/"
hypotheses:
  H1_Test: "This tests v7.3 framework compliance"
analysis:
  variant: "default"
  models:
    - "vertex_ai/gemini-2.5-flash-lite"
synthesis:
  model: "vertex_ai/gemini-2.5-flash-lite"
expected_outcomes:
  - "Framework validation success"
---

# Framework Validation Test

This experiment tests v7.3 framework compliance.
'''
    
    with open("experiment.md", "w") as f:
        f.write(experiment_content)

def create_test_corpus():
    """Create minimal corpus for validation."""
    os.makedirs("corpus", exist_ok=True)
    
    corpus_content = '''---
corpus_version: "v7.3"
name: "validation_test_corpus"
description: "Minimal test corpus for framework validation"
---

# Test Corpus

```json
{
  "corpus_version": "v7.3",
  "file_manifest": [
    {
      "name": "test.txt",
      "document_type": "test",
      "category": "validation"
    }
  ],
  "field_naming_standards": {
    "required_consistency": ["document_type", "category"]
  }
}
```
'''
    
    with open("corpus/corpus.md", "w") as f:
        f.write(corpus_content)
    
    with open("corpus/test.txt", "w") as f:
        f.write("This is test content for framework validation.")

def validate_framework(framework_path):
    """Validate a single framework."""
    framework_name = Path(framework_path).stem
    print(f"\n🔍 Validating {framework_name}...")
    
    try:
        # Create test experiment
        create_test_experiment(framework_path)
        create_test_corpus()
        
        # Run validation
        result = subprocess.run(
            ["discernus", "validate", "."],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print(f"✅ {framework_name}: PASSED")
            return True
        else:
            print(f"❌ {framework_name}: FAILED")
            print(f"   Error: {result.stderr.strip()}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏰ {framework_name}: TIMEOUT")
        return False
    except Exception as e:
        print(f"💥 {framework_name}: ERROR - {e}")
        return False
    finally:
        # Cleanup
        for file in ["experiment.md"]:
            if os.path.exists(file):
                os.remove(file)
        if os.path.exists("corpus"):
            import shutil
            shutil.rmtree("corpus")

def main():
    """Run validation on all frameworks."""
    print("🚀 Starting systematic validation of all 16 v7.3 frameworks...")
    
    passed = 0
    failed = 0
    
    for framework in FRAMEWORKS:
        if validate_framework(framework):
            passed += 1
        else:
            failed += 1
    
    print(f"\n📊 Validation Results:")
    print(f"   ✅ Passed: {passed}/16")
    print(f"   ❌ Failed: {failed}/16")
    
    if failed == 0:
        print("\n🎉 ALL FRAMEWORKS VALIDATED SUCCESSFULLY!")
        sys.exit(0)
    else:
        print(f"\n⚠️  {failed} frameworks failed validation")
        sys.exit(1)

if __name__ == "__main__":
    main()