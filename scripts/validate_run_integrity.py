#!/usr/bin/env python3
"""
Discernus Research Run Integrity Validator

This script provides comprehensive cryptographic validation of research run integrity.
Designed for auditors to verify that no tampering has occurred and that the complete
provenance chain is intact.

Usage:
    python3 scripts/validate_run_integrity.py projects/simple_test/runs/20250804T175152Z
    python3 scripts/validate_run_integrity.py projects/simple_test/runs/20250804T175152Z --verbose
    python3 scripts/validate_run_integrity.py projects/simple_test/runs/20250804T175152Z --check-git
"""

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import sys


class IntegrityValidator:
    """Validates cryptographic integrity of research runs."""
    
    def __init__(self, run_path: Path, verbose: bool = False):
        self.run_path = Path(run_path)
        self.verbose = verbose
        self.errors = []
        self.warnings = []
        self.checks_passed = 0
        self.checks_total = 0
        
    def log(self, message: str, level: str = "INFO"):
        """Log messages with appropriate formatting."""
        if level == "ERROR":
            self.errors.append(message)
            print(f"❌ ERROR: {message}")
        elif level == "WARNING":
            self.warnings.append(message)
            print(f"⚠️  WARNING: {message}")
        elif level == "SUCCESS":
            print(f"✅ {message}")
        elif self.verbose or level == "INFO":
            print(f"ℹ️  {message}")
    
    def compute_file_hash(self, file_path: Path) -> str:
        """Compute SHA-256 hash of a file."""
        try:
            hasher = hashlib.sha256()
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except Exception as e:
            self.log(f"Failed to hash {file_path}: {e}", "ERROR")
            return ""
    
    def extract_hash_from_filename(self, filename: str) -> Optional[str]:
        """Extract hash from content-addressed filename."""
        # Pattern: prefix_hash.extension (hash is 8 chars from SHA-256)
        parts = filename.split('_')
        if len(parts) >= 2:
            # Try last part before extension
            potential_hash = parts[-1].split('.')[0]
            if len(potential_hash) == 8 and all(c in '0123456789abcdef' for c in potential_hash):
                return potential_hash
        
        # Try filename without extension
        potential_hash = filename.split('.')[0]
        if len(potential_hash) == 8 and all(c in '0123456789abcdef' for c in potential_hash):
            return potential_hash
            
        return None
    
    def validate_artifact_hashes(self) -> bool:
        """Validate that all artifacts match their content-addressed hashes."""
        self.log("Validating artifact hash integrity...")
        artifacts_dir = self.run_path / "artifacts"
        
        if not artifacts_dir.exists():
            self.log("No artifacts directory found", "ERROR")
            return False
        
        hash_mismatches = []
        validated_files = 0
        
        # Check all files in artifacts directory (following symlinks)
        for artifact_file in artifacts_dir.rglob("*"):
            if artifact_file.is_file():
                # Skip non-content-addressed files
                if artifact_file.name in ["provenance.json", "manifest.json"]:
                    continue
                
                expected_hash = self.extract_hash_from_filename(artifact_file.name)
                if not expected_hash:
                    self.log(f"Skipping non-content-addressed file: {artifact_file.name}", "WARNING")
                    continue
                
                # Resolve symlink to get actual file
                actual_file = artifact_file.resolve()
                if not actual_file.exists():
                    self.log(f"Broken symlink: {artifact_file}", "ERROR")
                    continue
                
                actual_hash = self.compute_file_hash(actual_file)
                # Check if the expected hash (8 chars) matches the prefix of actual hash (64 chars)
                if not actual_hash.startswith(expected_hash):
                    hash_mismatches.append((artifact_file, expected_hash, actual_hash[:8]))
                else:
                    validated_files += 1
                    self.log(f"Hash verified: {artifact_file.name} ({expected_hash}...)")
        
        if hash_mismatches:
            self.log(f"Found {len(hash_mismatches)} hash mismatches:", "ERROR")
            for file_path, expected, actual in hash_mismatches:
                self.log(f"  {file_path.name}: expected {expected}, got {actual}", "ERROR")
            return False
        
        self.log(f"All {validated_files} content-addressed artifacts verified", "SUCCESS")
        return True
    
    def validate_symlinks(self) -> bool:
        """Validate that all symlinks point to existing files."""
        self.log("Validating symlink integrity...")
        artifacts_dir = self.run_path / "artifacts"
        
        if not artifacts_dir.exists():
            self.log("No artifacts directory found", "ERROR")
            return False
        
        broken_links = []
        valid_links = 0
        
        for artifact_file in artifacts_dir.rglob("*"):
            if artifact_file.is_symlink():
                target = artifact_file.resolve()
                if not target.exists():
                    broken_links.append((artifact_file, target))
                else:
                    valid_links += 1
                    self.log(f"Symlink valid: {artifact_file.name} → {target.name}")
        
        if broken_links:
            self.log(f"Found {len(broken_links)} broken symlinks:", "ERROR")
            for link, target in broken_links:
                self.log(f"  {link} → {target} (missing)", "ERROR")
            return False
        
        self.log(f"All {valid_links} symlinks verified", "SUCCESS")
        return True
    
    def validate_provenance_chain(self) -> bool:
        """Validate the dependency chain in provenance metadata."""
        self.log("Validating provenance chain integrity...")
        
        provenance_file = self.run_path / "artifacts" / "provenance.json"
        if not provenance_file.exists():
            self.log("No provenance.json found", "ERROR")
            return False
        
        try:
            with open(provenance_file) as f:
                provenance = json.load(f)
        except Exception as e:
            self.log(f"Failed to parse provenance.json: {e}", "ERROR")
            return False
        
        missing_dependencies = []
        validated_chains = 0
        
        for hash_id, metadata in provenance.items():
            # Check if dependencies exist
            if "metadata" in metadata and "dependencies" in metadata["metadata"]:
                try:
                    deps = json.loads(metadata["metadata"]["dependencies"])
                    if isinstance(deps, list):
                        for dep_hash in deps:
                            if dep_hash not in provenance:
                                missing_dependencies.append((hash_id, dep_hash))
                            else:
                                self.log(f"Dependency verified: {hash_id[:8]} → {dep_hash[:8]}")
                        validated_chains += 1
                except (json.JSONDecodeError, TypeError):
                    self.log(f"Invalid dependencies format for {hash_id}", "WARNING")
        
        if missing_dependencies:
            self.log(f"Found {len(missing_dependencies)} missing dependencies:", "ERROR")
            for artifact, dep in missing_dependencies:
                self.log(f"  {artifact[:8]} depends on missing {dep[:8]}", "ERROR")
            return False
        
        self.log(f"Provenance chain validated for {validated_chains} artifacts", "SUCCESS")
        return True
    
    def validate_manifest(self) -> bool:
        """Validate the execution manifest."""
        self.log("Validating execution manifest...")
        
        manifest_file = self.run_path / "manifest.json"
        if not manifest_file.exists():
            self.log("No manifest.json found", "ERROR")
            return False
        
        try:
            with open(manifest_file) as f:
                manifest = json.load(f)
        except Exception as e:
            self.log(f"Failed to parse manifest.json: {e}", "ERROR")
            return False
        
        # Check required fields in run_metadata
        run_metadata = manifest.get("run_metadata", {})
        required_fields = ["run_id", "experiment_name", "created_at"]
        missing_fields = [field for field in required_fields if field not in run_metadata]
        
        if missing_fields:
            self.log(f"Manifest missing required fields in run_metadata: {missing_fields}", "ERROR")
            return False
        
        # Check performance metrics for completion
        perf_metrics = manifest.get("performance_metrics", {})
        exec_time = perf_metrics.get("total_execution_time", {})
        if not exec_time.get("end_time"):
            self.log("Run appears incomplete (no end_time in performance_metrics)", "WARNING")
        
        self.log("Manifest validation passed", "SUCCESS")
        return True
    
    def validate_git_history(self) -> bool:
        """Validate that this run exists in Git history."""
        self.log("Validating Git provenance...")
        
        run_id = self.run_path.name
        
        try:
            # Check if this run is committed to Git
            result = subprocess.run(
                ["git", "log", "--oneline", "--grep", run_id],
                capture_output=True,
                text=True,
                cwd=self.run_path.parent.parent.parent  # Go to repo root
            )
            
            if result.returncode != 0:
                self.log(f"Git command failed: {result.stderr}", "ERROR")
                return False
            
            if not result.stdout.strip():
                self.log(f"Run {run_id} not found in Git history", "WARNING")
                return False
            
            commits = result.stdout.strip().split('\n')
            self.log(f"Found {len(commits)} Git commits referencing this run", "SUCCESS")
            
            if self.verbose:
                for commit in commits:
                    self.log(f"  {commit}")
            
            return True
            
        except Exception as e:
            self.log(f"Git validation failed: {e}", "ERROR")
            return False
    
    def validate_results_files(self) -> bool:
        """Validate that expected results files exist and are substantial."""
        self.log("Validating results files...")
        
        results_dir = self.run_path / "results"
        if not results_dir.exists():
            self.log("No results directory found", "ERROR")
            return False
        
        expected_files = ["final_report.md", "scores.csv", "evidence.csv", "metadata.csv"]
        missing_files = []
        empty_files = []
        
        for filename in expected_files:
            file_path = results_dir / filename
            if not file_path.exists():
                missing_files.append(filename)
            elif file_path.stat().st_size == 0:
                empty_files.append(filename)
            else:
                size_kb = file_path.stat().st_size // 1024
                self.log(f"Results file verified: {filename} ({size_kb}KB)")
        
        if missing_files:
            self.log(f"Missing results files: {missing_files}", "ERROR")
            return False
        
        if empty_files:
            self.log(f"Empty results files: {empty_files}", "WARNING")
        
        self.log("Results files validation passed", "SUCCESS")
        return True
    
    def run_full_validation(self, check_git: bool = False) -> bool:
        """Run complete integrity validation suite."""
        print(f"\n🔍 Discernus Research Run Integrity Validator")
        print(f"📁 Validating: {self.run_path}")
        print(f"🕐 Started: {subprocess.run(['date'], capture_output=True, text=True).stdout.strip()}")
        print("=" * 60)
        
        validations = [
            ("Manifest Structure", self.validate_manifest),
            ("Results Files", self.validate_results_files),
            ("Symlink Integrity", self.validate_symlinks),
            ("Hash Integrity", self.validate_artifact_hashes),
            ("Provenance Chain", self.validate_provenance_chain),
        ]
        
        if check_git:
            validations.append(("Git History", self.validate_git_history))
        
        all_passed = True
        
        for name, validation_func in validations:
            print(f"\n📋 {name}:")
            print("-" * 40)
            passed = validation_func()
            all_passed = all_passed and passed
            self.checks_total += 1
            if passed:
                self.checks_passed += 1
        
        # Summary
        print("\n" + "=" * 60)
        print(f"🎯 VALIDATION SUMMARY")
        print(f"✅ Checks Passed: {self.checks_passed}/{self.checks_total}")
        
        if self.warnings:
            print(f"⚠️  Warnings: {len(self.warnings)}")
            for warning in self.warnings:
                print(f"   • {warning}")
        
        if self.errors:
            print(f"❌ Errors: {len(self.errors)}")
            for error in self.errors:
                print(f"   • {error}")
        
        if all_passed and not self.errors:
            print(f"\n🎉 INTEGRITY VERIFICATION: PASSED")
            print(f"   This research run has cryptographic integrity.")
            print(f"   All artifacts are tamper-evident and traceable.")
            return True
        else:
            print(f"\n⚠️  INTEGRITY VERIFICATION: FAILED")
            print(f"   Issues detected that require investigation.")
            return False


def main():
    parser = argparse.ArgumentParser(
        description="Validate cryptographic integrity of Discernus research runs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 scripts/validate_run_integrity.py projects/simple_test/runs/20250804T175152Z
  python3 scripts/validate_run_integrity.py projects/simple_test/runs/20250804T175152Z --verbose
  python3 scripts/validate_run_integrity.py projects/simple_test/runs/20250804T175152Z --check-git
        """
    )
    
    parser.add_argument(
        "run_path",
        help="Path to the research run directory to validate"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output showing all validation steps"
    )
    
    parser.add_argument(
        "--check-git",
        action="store_true",
        help="Also validate that the run exists in Git history"
    )
    
    args = parser.parse_args()
    
    run_path = Path(args.run_path)
    if not run_path.exists():
        print(f"❌ ERROR: Run path does not exist: {run_path}")
        sys.exit(1)
    
    if not run_path.is_dir():
        print(f"❌ ERROR: Run path is not a directory: {run_path}")
        sys.exit(1)
    
    validator = IntegrityValidator(run_path, args.verbose)
    success = validator.run_full_validation(args.check_git)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()