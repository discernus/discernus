#!/usr/bin/env python3
"""
Systematic CLI Command Testing Framework
=======================================

Tests all CLI commands with various scenarios to ensure they work correctly.
This script provides comprehensive testing coverage for the Discernus CLI.
"""

import subprocess
import sys
import tempfile
import shutil
from pathlib import Path
import json
import time
from typing import Dict, List, Tuple, Optional
import click

class CLITestResult:
    """Result of a CLI command test."""
    def __init__(self, command: str, success: bool, output: str, error: str, duration: float):
        self.command = command
        self.success = success
        self.output = output
        self.error = error
        self.duration = duration

class CLITester:
    """Systematic CLI testing framework."""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.results: List[CLITestResult] = []
        self.test_experiment_path = None
        self.temp_dir = None
        
    def log(self, message: str, level: str = "INFO"):
        """Log a message with timestamp."""
        timestamp = time.strftime("%H:%M:%S")
        if self.verbose or level == "ERROR":
            print(f"[{timestamp}] {level}: {message}")
    
    def run_command(self, command: List[str], timeout: int = 30) -> CLITestResult:
        """Run a CLI command and capture results."""
        start_time = time.time()
        full_command = ["discernus"] + command
        
        self.log(f"Running: {' '.join(full_command)}")
        
        try:
            result = subprocess.run(
                full_command,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd="/Volumes/code/discernus"
            )
            
            duration = time.time() - start_time
            success = result.returncode == 0
            
            test_result = CLITestResult(
                command=" ".join(command),
                success=success,
                output=result.stdout,
                error=result.stderr,
                duration=duration
            )
            
            if success:
                self.log(f"✅ SUCCESS ({duration:.2f}s)")
            else:
                self.log(f"❌ FAILED ({duration:.2f}s) - Exit code: {result.returncode}", "ERROR")
                if result.stderr:
                    self.log(f"Error: {result.stderr}", "ERROR")
            
            self.results.append(test_result)
            return test_result
            
        except subprocess.TimeoutExpired:
            duration = time.time() - start_time
            self.log(f"⏰ TIMEOUT ({duration:.2f}s)", "ERROR")
            
            test_result = CLITestResult(
                command=" ".join(command),
                success=False,
                output="",
                error=f"Command timed out after {timeout} seconds",
                duration=duration
            )
            self.results.append(test_result)
            return test_result
            
        except Exception as e:
            duration = time.time() - start_time
            self.log(f"💥 EXCEPTION ({duration:.2f}s): {e}", "ERROR")
            
            test_result = CLITestResult(
                command=" ".join(command),
                success=False,
                output="",
                error=str(e),
                duration=duration
            )
            self.results.append(test_result)
            return test_result
    
    def setup_test_environment(self):
        """Set up a test environment with sample experiment."""
        self.log("Setting up test environment...")
        
        # Create temporary directory
        self.temp_dir = tempfile.mkdtemp(prefix="discernus_test_")
        self.log(f"Test directory: {self.temp_dir}")
        
        # Create a minimal test experiment
        self.test_experiment_path = Path(self.temp_dir) / "test_experiment"
        self.test_experiment_path.mkdir()
        
        # Create proper experiment.md following v10 spec
        experiment_md = """# CLI Test Experiment

## Abstract
Test experiment for CLI validation and testing.

## Research Questions
- How does the CLI testing framework perform?

## Expected Outcomes
Successful CLI command execution and validation.

---

```yaml
# --- Start of Machine-Readable Appendix ---

# 5.1: Metadata (Required)
metadata:
  experiment_name: "cli_test_experiment"
  author: "CLI Test Suite"
  spec_version: "10.0"

# 5.2: Components (Required)
components:
  framework: "framework.md"
  corpus: "test_corpus.md"

# 5.3: Hypotheses (Optional but Recommended)
hypotheses:
  - id: "H1"
    description: "CLI commands execute successfully"
    falsifiable: true
    mutually_exclusive: true
    collective_exhaustive: true

# --- End of Machine-Readable Appendix ---
```"""
        (self.test_experiment_path / "experiment.md").write_text(experiment_md)
        
        # Create proper framework following v10 spec
        framework_md = """# Test Framework v1.0

## Abstract & Raison d'être

**What is this framework?**
A minimal framework for CLI testing validation.

**What problem does it solve?**
Provides a framework that passes validation for CLI testing.

**Who is it for?**
CLI test suite developers.

## Theoretical Foundations

Basic testing framework for CLI validation.

## Analytical Methodology

**Dimensions:**
- Test Dimension (0.0-1.0): A test dimension for CLI validation

## Intended Application & Corpus Fit

**Target Corpus Description**: Simple test documents for CLI validation.

---

```yaml
# --- Start of Machine-Readable Appendix ---

# 5.1: Metadata (Required)
metadata:
  framework_name: "test_framework"
  version: "1.0"
  spec_version: "10.0"
  author: "CLI Test Suite"

# 5.2: Dimensions (Required)
dimensions:
  - name: "test_dimension"
    description: "A test dimension for CLI validation"
    type: "continuous"
    scale: [0.0, 1.0]
    interpretation: "Higher values indicate more test content"

# --- End of Machine-Readable Appendix ---
```"""
        (self.test_experiment_path / "framework.md").write_text(framework_md)
        
        # Create proper corpus following v10 spec
        corpus_md = """# CLI Test Corpus

Simple test documents for CLI validation.

## Document Overview

- **Test Document 1**: Basic test document for CLI validation

---

## Document Manifest

```yaml
name: "CLI Test Corpus"
version: "1.0"
spec_version: "10.0"
total_documents: 1
date_range: "2024"

documents:
  - filename: "test_document.txt"
    document_id: "test_doc_1"
    metadata:
      type: "test"
      author: "CLI_Test_Suite"
      year: 2024
      title: "Test Document for CLI Validation"
      description: "A simple test document for CLI validation"
```"""
        (self.test_experiment_path / "test_corpus.md").write_text(corpus_md)
        
        # Create test document
        test_doc = "This is a test document for CLI validation. It contains some sample text for analysis and testing purposes."
        (self.test_experiment_path / "test_document.txt").write_text(test_doc)
        
        self.log("✅ Test environment setup complete")
    
    def cleanup_test_environment(self):
        """Clean up test environment."""
        if self.temp_dir and Path(self.temp_dir).exists():
            self.log("Cleaning up test environment...")
            shutil.rmtree(self.temp_dir)
            self.log("✅ Cleanup complete")
    
    def test_basic_commands(self):
        """Test basic commands that don't require experiments."""
        self.log("🧪 Testing basic commands...")
        
        # Test help
        self.run_command(["--help"])
        
        # Test version
        self.run_command(["--version"])
        
        # Test status
        self.run_command(["status"])
        
        # Test list (should work even with no experiments)
        self.run_command(["list"])
    
    def test_validation_commands(self):
        """Test validation-related commands."""
        self.log("🧪 Testing validation commands...")
        
        if not self.test_experiment_path:
            self.log("❌ No test experiment available", "ERROR")
            return
        
        exp_path = str(self.test_experiment_path)
        
        # Test validate with dry-run
        self.run_command(["validate", exp_path, "--dry-run"])
        
        # Test validate (actual validation)
        self.run_command(["validate", exp_path])
        
        # Test artifacts (should work even with no runs)
        self.run_command(["artifacts", exp_path])
        
        # Test cache stats
        self.run_command(["cache", exp_path, "--stats"])
    
    def test_management_commands(self):
        """Test management commands."""
        self.log("🧪 Testing management commands...")
        
        if not self.test_experiment_path:
            self.log("❌ No test experiment available", "ERROR")
            return
        
        exp_path = str(self.test_experiment_path)
        
        # Test promote with dry-run
        self.run_command(["promote", exp_path, "--dry-run"])
        
        # Test promote (actual promotion)
        self.run_command(["promote", exp_path, "--force"])
    
    def test_debug_commands(self):
        """Test debug commands."""
        self.log("🧪 Testing debug commands...")
        
        if not self.test_experiment_path:
            self.log("❌ No test experiment available", "ERROR")
            return
        
        exp_path = str(self.test_experiment_path)
        
        # Test debug with different agents
        agents = ["analysis", "synthesis", "statistical", "fact-checker", "validation"]
        
        for agent in agents:
            self.run_command(["debug", exp_path, "--agent", agent, "--test-mode"], timeout=60)
        
        # Test debug with verbose
        self.run_command(["debug", exp_path, "--verbose", "--test-mode"], timeout=60)
    
    def test_archive_commands(self):
        """Test archive commands (requires a run)."""
        self.log("🧪 Testing archive commands...")
        
        if not self.test_experiment_path:
            self.log("❌ No test experiment available", "ERROR")
            return
        
        exp_path = str(self.test_experiment_path)
        
        # First, try to run a minimal experiment to create a run
        self.log("Creating test run for archive testing...")
        run_result = self.run_command(["run", exp_path, "--dry-run"], timeout=60)
        
        if run_result.success:
            # Look for runs directory
            runs_dir = Path(exp_path) / "runs"
            if runs_dir.exists():
                # Find the most recent run
                run_dirs = [d for d in runs_dir.iterdir() if d.is_dir()]
                if run_dirs:
                    latest_run = max(run_dirs, key=lambda x: x.name)
                    self.log(f"Testing archive with run: {latest_run}")
                    
                    # Test archive command
                    self.run_command(["archive", str(latest_run)], timeout=60)
                else:
                    self.log("No runs found for archive testing", "ERROR")
            else:
                self.log("No runs directory found for archive testing", "ERROR")
        else:
            self.log("Failed to create test run for archive testing", "ERROR")
    
    def test_error_conditions(self):
        """Test error conditions and edge cases."""
        self.log("🧪 Testing error conditions...")
        
        # Test with non-existent experiment
        self.run_command(["validate", "/nonexistent/path"])
        
        # Test with invalid arguments
        self.run_command(["debug", "--agent", "invalid_agent"])
        
        # Test with missing required arguments
        self.run_command(["archive"])
    
    def run_all_tests(self):
        """Run all CLI tests systematically."""
        self.log("🚀 Starting systematic CLI testing...")
        
        try:
            # Setup
            self.setup_test_environment()
            
            # Run test suites
            self.test_basic_commands()
            self.test_validation_commands()
            self.test_management_commands()
            self.test_debug_commands()
            self.test_archive_commands()
            self.test_error_conditions()
            
        finally:
            # Cleanup
            self.cleanup_test_environment()
        
        # Generate report
        self.generate_report()
    
    def generate_report(self):
        """Generate a comprehensive test report."""
        self.log("📊 Generating test report...")
        
        total_tests = len(self.results)
        successful_tests = sum(1 for r in self.results if r.success)
        failed_tests = total_tests - successful_tests
        
        print("\n" + "="*60)
        print("CLI TESTING REPORT")
        print("="*60)
        print(f"Total Tests: {total_tests}")
        print(f"Successful: {successful_tests} ✅")
        print(f"Failed: {failed_tests} ❌")
        print(f"Success Rate: {(successful_tests/total_tests)*100:.1f}%")
        print("="*60)
        
        if failed_tests > 0:
            print("\nFAILED TESTS:")
            print("-" * 40)
            for result in self.results:
                if not result.success:
                    print(f"❌ {result.command}")
                    print(f"   Error: {result.error}")
                    print(f"   Duration: {result.duration:.2f}s")
                    print()
        
        print("\nALL TEST RESULTS:")
        print("-" * 40)
        for result in self.results:
            status = "✅" if result.success else "❌"
            print(f"{status} {result.command} ({result.duration:.2f}s)")
        
        # Save detailed report
        report_file = Path("/Volumes/code/discernus/cli_test_report.json")
        report_data = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "summary": {
                "total_tests": total_tests,
                "successful_tests": successful_tests,
                "failed_tests": failed_tests,
                "success_rate": (successful_tests/total_tests)*100
            },
            "results": [
                {
                    "command": r.command,
                    "success": r.success,
                    "output": r.output,
                    "error": r.error,
                    "duration": r.duration
                }
                for r in self.results
            ]
        }
        
        report_file.write_text(json.dumps(report_data, indent=2))
        self.log(f"📄 Detailed report saved to: {report_file}")

@click.command()
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
@click.option('--quick', '-q', is_flag=True, help='Run quick tests only (skip expensive operations)')
def main(verbose: bool, quick: bool):
    """Systematic CLI testing framework for Discernus."""
    tester = CLITester(verbose=verbose)
    
    if quick:
        tester.log("Running quick tests only...")
        tester.setup_test_environment()
        try:
            tester.test_basic_commands()
            tester.test_validation_commands()
        finally:
            tester.cleanup_test_environment()
        tester.generate_report()
    else:
        tester.run_all_tests()

if __name__ == "__main__":
    main()
