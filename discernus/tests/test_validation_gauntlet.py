#!/usr/bin/env python3
"""
Test for THIN Experiment Lifecycle Validation Gauntlet - Issue #131
===================================================================

Tests the validation gauntlet functionality that detects and fixes Issue #68:
"technically compliant but research useless" experiments missing SynthesisAgent.
"""

# Copyright (C) 2025  Discernus Team

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import unittest
import tempfile
import json
from pathlib import Path
from datetime import datetime
import sys
import os

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from discernus.core.experiment_lifecycle import ExperimentLifecycleManager


class TestValidationGauntlet(unittest.TestCase):
    """Test that the validation gauntlet detects Issue #68 problems and suggests enhancements"""
    
    def setUp(self):
        """Create temporary directory with test experiment"""
        self.temp_dir = Path(tempfile.mkdtemp())
        
        # Create test framework
        self.framework_file = self.temp_dir / "framework.md"
        self.framework_file.write_text("""
# Test Framework

## Analysis Instructions

Please analyze the text for basic sentiment.

# --- Discernus Configuration ---

name: test_framework
version: 1.0

analysis_variants:
  default:
    analysis_prompt: "Analyze this text for sentiment."
""")
        
        # Create test corpus
        self.corpus_dir = self.temp_dir / "corpus"
        self.corpus_dir.mkdir()
        (self.corpus_dir / "test.txt").write_text("This is a test text for analysis.")
        
    def tearDown(self):
        """Clean up temporary directory"""
        import shutil
        shutil.rmtree(self.temp_dir)
        
    def _create_experiment_file(self, workflow: list) -> Path:
        """Create experiment file with specified workflow"""
        experiment_file = self.temp_dir / "experiment.md"
        experiment_content = f"""---
name: test_experiment
description: Test experiment for validation gauntlet
hypothesis: This is a test hypothesis
framework_file: framework.md
corpus: corpus/
models:
  - "vertex_ai/gemini-2.5-pro"
runs_per_model: 1
workflow:
{self._format_workflow_yaml(workflow)}
---

# Test Experiment
"""
        experiment_file.write_text(experiment_content)
        return experiment_file
        
    def _format_workflow_yaml(self, workflow: list) -> str:
        """Format workflow list as YAML"""
        lines = []
        for step in workflow:
            lines.append(f"  - agent: {step['agent']}")
        return "\n".join(lines)
    
    def test_detects_missing_synthesis_agent(self):
        """Test that validation gauntlet detects missing SynthesisAgent (Issue #68 core problem)"""
        print("🧪 Testing Issue #68 detection: Missing SynthesisAgent")
        
        # Create experiment with Issue #68 problem - no SynthesisAgent
        issue_68_workflow = [
            {"agent": "AnalysisAgent"},
            {"agent": "MethodologicalOverwatchAgent"},
            {"agent": "CalculationAgent"}
        ]
        
        experiment_file = self._create_experiment_file(issue_68_workflow)
        
        # Initialize lifecycle manager
        lifecycle_manager = ExperimentLifecycleManager(str(self.temp_dir))
        
        # Test workflow completeness validation (core of Issue #68 fix)
        result = lifecycle_manager._validate_workflow_completeness(issue_68_workflow)
        
        # Should detect the Issue #68 problem
        self.assertFalse(result['complete'], "Should detect incomplete workflow")
        self.assertIn('SynthesisAgent', result['missing_agents'], "Should identify missing SynthesisAgent")
        self.assertTrue(any('SynthesisAgent' in issue for issue in result['issues']), 
                       "Should report SynthesisAgent issue")
        self.assertTrue(any('research deliverables' in rec for rec in result['recommendations']), 
                       "Should recommend adding research deliverables")
        
        print("✅ Successfully detected Issue #68 problem: Missing SynthesisAgent")
        
    def test_accepts_complete_workflow(self):
        """Test that validation gauntlet accepts workflow with SynthesisAgent"""
        print("🧪 Testing complete workflow acceptance")
        
        # Create experiment with complete workflow including SynthesisAgent
        complete_workflow = [
            {"agent": "AnalysisAgent"},
            {"agent": "MethodologicalOverwatchAgent"}, 
            {"agent": "CalculationAgent"},
            {"agent": "SynthesisAgent"}
        ]
        
        experiment_file = self._create_experiment_file(complete_workflow)
        
        # Initialize lifecycle manager
        lifecycle_manager = ExperimentLifecycleManager(str(self.temp_dir))
        
        # Test workflow completeness validation
        result = lifecycle_manager._validate_workflow_completeness(complete_workflow)
        
        # Should accept complete workflow (workflow is complete even if it has validation recommendations)
        self.assertTrue(result['complete'], "Should accept complete workflow")
        self.assertEqual(len(result['missing_agents']), 0, "Should not identify missing agents")
        # Note: validation agents warning is separate from completeness - workflow can be complete but still have recommendations
        
        print("✅ Successfully accepted complete workflow")
    
    def test_generates_enhanced_workflow(self):
        """Test that validation gauntlet generates enhanced workflow with SynthesisAgent"""
        print("🧪 Testing enhanced workflow generation")
        
        # Create experiment with Issue #68 problem
        incomplete_workflow = [
            {"agent": "AnalysisAgent"},
            {"agent": "CalculationAgent"}
        ]
        
        experiment_file = self._create_experiment_file(incomplete_workflow)
        
        # Initialize lifecycle manager
        lifecycle_manager = ExperimentLifecycleManager(str(self.temp_dir))
        
        # Generate enhanced workflow
        enhanced = lifecycle_manager._generate_enhanced_workflow(
            incomplete_workflow, ['SynthesisAgent']
        )
        
        # Should add SynthesisAgent
        self.assertEqual(len(enhanced), 3, "Should add one new agent")
        self.assertEqual(enhanced[2]['agent'], 'SynthesisAgent', "Should add SynthesisAgent")
        self.assertIn('config', enhanced[2], "Should include configuration")
        self.assertIn('output_artifacts', enhanced[2]['config'], "Should specify output artifacts")
        
        print("✅ Successfully generated enhanced workflow")


def run_validation_gauntlet_test():
    """Run the validation gauntlet test suite"""
    print("🧪 Testing THIN Experiment Lifecycle Validation Gauntlet - Issue #131")
    print("=" * 80)
    print("This tests the core Issue #68 detection and enhancement logic.")
    print()
    
    # Run the tests
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestValidationGauntlet)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    if result.wasSuccessful():
        print("\n🎉 Validation Gauntlet Tests PASSED!")
        print("✅ Issue #68 detection logic working correctly")
        print("✅ Workflow enhancement logic working correctly")
        return True
    else:
        print("\n❌ Validation Gauntlet Tests FAILED!")
        return False


if __name__ == "__main__":
    # Run the test if called directly
    success = run_validation_gauntlet_test()
    sys.exit(0 if success else 1) 