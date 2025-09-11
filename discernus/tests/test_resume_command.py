#!/usr/bin/env python3
"""
Test for Issue #130: Resume feature directory structure mismatch
Verifies that resume auto-discovery works with both directory structures.
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

from discernus_cli import _find_latest_state_file


class TestResumeDirectoryFix(unittest.TestCase):
    """Test that resume works with both results/ and experiments/ directory structures"""
    
    def setUp(self):
        """Create temporary directory for testing"""
        self.temp_dir = Path(tempfile.mkdtemp())
        
    def tearDown(self):
        """Clean up temporary directory"""
        import shutil
        shutil.rmtree(self.temp_dir)
        
    def _create_state_file(self, file_path: Path, step_num: int, agent_name: str):
        """Create a mock state file"""
        file_path.parent.mkdir(parents=True, exist_ok=True)
        state_data = {
            "step": step_num,
            "agent": agent_name,
            "timestamp": datetime.now().isoformat(),
            "workflow_state": {"test": "data"}
        }
        with open(file_path, 'w') as f:
            json.dump(state_data, f, indent=2)
        return file_path
        
    def test_legacy_results_structure(self):
        """Test that resume finds state files in results/ directory (legacy MVA structure)"""
        # Create legacy results/ structure like MVA experiments
        session_dir = self.temp_dir / "results" / "2025-01-22_10-30-00"
        state_file = self._create_state_file(
            session_dir / "state_after_step_2_DataExtractionAgent.json",
            2, "DataExtractionAgent"
        )
        
        # Should find the state file
        found_file = _find_latest_state_file(self.temp_dir)
        self.assertEqual(found_file, state_file)
        print(f"✅ Found legacy structure: {found_file}")
        
    def test_current_experiments_structure(self):
        """Test that resume finds state files in experiments/ directory (current WorkflowOrchestrator)"""
        # Create current experiments/ structure like WorkflowOrchestrator
        session_dir = self.temp_dir / "experiments" / "test_experiment" / "sessions" / "session_20250122_103000"
        state_file = self._create_state_file(
            session_dir / "state_after_step_1_AnalysisAgent.json",
            1, "AnalysisAgent"
        )
        
        # Should find the state file
        found_file = _find_latest_state_file(self.temp_dir)
        self.assertEqual(found_file, state_file)
        print(f"✅ Found current structure: {found_file}")
        
    def test_both_structures_returns_most_recent(self):
        """Test that when both structures exist, resume returns the most recent state file"""
        import time
        
        # Create legacy structure file first
        legacy_session = self.temp_dir / "results" / "2025-01-22_10-30-00"
        legacy_file = self._create_state_file(
            legacy_session / "state_after_step_2_DataExtractionAgent.json",
            2, "DataExtractionAgent"
        )
        
        # Wait to ensure different timestamps
        time.sleep(0.1)
        
        # Create current structure file (should be more recent)
        current_session = self.temp_dir / "experiments" / "test_experiment" / "sessions" / "session_20250122_103000"
        current_file = self._create_state_file(
            current_session / "state_after_step_1_AnalysisAgent.json",
            1, "AnalysisAgent"
        )
        
        # Should return the more recent file (current structure)
        found_file = _find_latest_state_file(self.temp_dir)
        self.assertEqual(found_file, current_file)
        print(f"✅ Found most recent: {found_file}")
        
    def test_no_state_files_returns_none(self):
        """Test that when no state files exist, returns None"""
        # Create empty directories
        (self.temp_dir / "results").mkdir(exist_ok=True)
        (self.temp_dir / "experiments").mkdir(exist_ok=True)
        
        # Should return None
        found_file = _find_latest_state_file(self.temp_dir)
        self.assertIsNone(found_file)
        print("✅ Correctly returns None when no state files exist")
        
    def test_partial_state_files(self):
        """Test that partial state files are also found"""
        session_dir = self.temp_dir / "experiments" / "test_experiment" / "sessions" / "session_20250122_103000"
        partial_file = self._create_state_file(
            session_dir / "state_step_1_partial.json",
            1, "AnalysisAgent"
        )
        
        found_file = _find_latest_state_file(self.temp_dir)
        self.assertEqual(found_file, partial_file)
        print(f"✅ Found partial state file: {found_file}")


def run_issue_130_test():
    """Run the Issue #130 test suite"""
    print("🧪 Testing Issue #130 Fix: Resume Directory Structure Mismatch")
    print("=" * 70)
    
    # Run the tests
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestResumeDirectoryFix)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    if result.wasSuccessful():
        print("\n🎉 Issue #130 Fix Verified! Resume works with both directory structures")
        return True
    else:
        print("\n❌ Issue #130 Fix Failed! Check test output for details")
        return False


if __name__ == "__main__":
    # Run the test if called directly
    success = run_issue_130_test()
    sys.exit(0 if success else 1) 