#!/usr/bin/env python3
"""
Test Result Preservation System

Ensures that valuable test results are preserved while allowing cleanup
of temporary test data and bloat.
"""

import os
import shutil
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Set
import json
import logging

class TestResultPreservationSystem:
    """Manages preservation of important test results"""
    
    def __init__(self, project_root: Path = None):
        self.project_root = project_root or Path.cwd()
        self.logger = logging.getLogger(__name__)
        
        # Define what should be preserved
        self.preserve_patterns = [
            "exports/qa_*_test/",           # QA test result exports
            "tests/test_results/",          # Basic test results
            "exports/academic_formats/",    # Academic result exports
            "exports/analysis_results/",    # Analysis result exports
        ]
        
        # Define important file extensions to preserve
        self.preserve_extensions = [
            ".json",    # Validation reports, test results
            ".csv",     # Data exports for analysis
            ".feather", # Statistical data format
            ".dta",     # Stata format for academic use
        ]
    
    def get_preserved_paths(self) -> Set[Path]:
        """Get all paths that should be preserved"""
        preserved_paths = set()
        
        for pattern in self.preserve_patterns:
            # Convert pattern to Path and find matches
            pattern_path = self.project_root / pattern
            
            if pattern.endswith("/"):
                # Directory pattern
                if pattern_path.exists():
                    preserved_paths.add(pattern_path)
                    # Add all subdirectories and files
                    for item in pattern_path.rglob("*"):
                        preserved_paths.add(item)
            else:
                # File pattern - use glob
                for match in self.project_root.glob(pattern):
                    preserved_paths.add(match)
        
        return preserved_paths
    
    def is_test_result_file(self, file_path: Path) -> bool:
        """Check if a file contains important test results"""
        
        # Check if in preserved directories
        preserved_paths = self.get_preserved_paths()
        if file_path in preserved_paths or any(file_path.is_relative_to(p) for p in preserved_paths if p.is_dir()):
            return True
        
        # Check file extension
        if file_path.suffix.lower() in self.preserve_extensions:
            # Additional checks for test result content
            if any(keyword in file_path.name.lower() for keyword in [
                'qa_validation', 'qa_enhanced', 'test_result', 'validation_report'
            ]):
                return True
        
        return False
    
    def create_test_result_archive(self, archive_name: str = None) -> Path:
        """Create archive of all test results"""
        if not archive_name:
            archive_name = f"test_results_archive_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        archive_dir = self.project_root / "test_archives" / archive_name
        archive_dir.mkdir(parents=True, exist_ok=True)
        
        preserved_paths = self.get_preserved_paths()
        archived_count = 0
        
        for path in preserved_paths:
            if path.is_file():
                # Create relative path structure in archive
                rel_path = path.relative_to(self.project_root)
                archive_file = archive_dir / rel_path
                archive_file.parent.mkdir(parents=True, exist_ok=True)
                
                # Copy file to archive
                shutil.copy2(path, archive_file)
                archived_count += 1
        
        self.logger.info(f"📦 Created test result archive: {archive_dir}")
        self.logger.info(f"   Archived {archived_count} test result files")
        
        return archive_dir
    
    def get_test_result_summary(self) -> Dict:
        """Get summary of all test results"""
        preserved_paths = self.get_preserved_paths()
        
        summary = {
            'total_files': 0,
            'total_size_mb': 0.0,
            'by_category': {},
            'newest_result': None,
            'oldest_result': None
        }
        
        newest_time = None
        oldest_time = None
        
        for path in preserved_paths:
            if path.is_file():
                summary['total_files'] += 1
                size_mb = path.stat().st_size / (1024 * 1024)
                summary['total_size_mb'] += size_mb
                
                # Categorize by parent directory
                category = path.parent.name
                if category not in summary['by_category']:
                    summary['by_category'][category] = {'files': 0, 'size_mb': 0.0}
                summary['by_category'][category]['files'] += 1
                summary['by_category'][category]['size_mb'] += size_mb
                
                # Track newest/oldest
                file_time = datetime.fromtimestamp(path.stat().st_mtime)
                if newest_time is None or file_time > newest_time:
                    newest_time = file_time
                    summary['newest_result'] = str(path)
                if oldest_time is None or file_time < oldest_time:
                    oldest_time = file_time
                    summary['oldest_result'] = str(path)
        
        return summary
    
    def cleanup_old_test_results(self, keep_days: int = 90, dry_run: bool = False) -> Dict:
        """Clean up very old test results while preserving recent ones"""
        cutoff_date = datetime.now() - timedelta(days=keep_days)
        
        cleanup_stats = {
            'files_removed': 0,
            'size_freed_mb': 0.0,
            'preserved_files': 0
        }
        
        preserved_paths = self.get_preserved_paths()
        
        for path in preserved_paths:
            if not path.is_file():
                continue
            
            file_time = datetime.fromtimestamp(path.stat().st_mtime)
            
            if file_time < cutoff_date:
                # Very old test result - consider for cleanup
                size_mb = path.stat().st_size / (1024 * 1024)
                
                # Check if it's a particularly important result
                if self._is_critical_test_result(path):
                    self.logger.info(f"🔒 Preserving critical test result: {path}")
                    cleanup_stats['preserved_files'] += 1
                else:
                    self.logger.info(f"🧹 Cleaning old test result: {path} ({size_mb:.1f}MB)")
                    if not dry_run:
                        path.unlink()
                        cleanup_stats['files_removed'] += 1
                        cleanup_stats['size_freed_mb'] += size_mb
        
        return cleanup_stats
    
    def _is_critical_test_result(self, path: Path) -> bool:
        """Check if a test result is critical and should never be cleaned"""
        critical_indicators = [
            'validation_report',
            'qa_enhanced_data_dictionary',
            'golden_set',
            'academic_validation'
        ]
        
        return any(indicator in path.name.lower() for indicator in critical_indicators)
    
    def integrate_with_bloat_prevention(self) -> str:
        """Generate code to integrate with bloat prevention system"""
        
        integration_code = '''
# Add this to bloat_prevention_system.py cleanup_temp_files method:

def cleanup_temp_files(self, dry_run: bool = False) -> CleanupStats:
    """Clean up temporary files and caches"""
    self.logger.info("🧹 Cleaning up temporary files...")
    
    # Import test result preservation
    try:
        from .test_result_preservation_system import TestResultPreservationSystem
        preservator = TestResultPreservationSystem(self.project_root)
        preserved_paths = preservator.get_preserved_paths()
    except ImportError:
        preserved_paths = set()
        self.logger.warning("Test result preservation not available")
    
    temp_patterns = [
        "tmp/**/*",
        "**/*.tmp", 
        "**/*.cache",
        "**/__pycache__/**/*",
        # REMOVED: "**/test_output/**/*" - now handled selectively
    ]
    
    # Handle test_output selectively
    test_output_dirs = list(self.project_root.glob("**/test_output/"))
    for test_output_dir in test_output_dirs:
        if test_output_dir.is_dir():
            for item in test_output_dir.rglob("*"):
                if item.is_file():
                    # Check if this is a preserved test result
                    if item not in preserved_paths and not preservator.is_test_result_file(item):
                        # Safe to clean up
                        size_mb = item.stat().st_size / (1024 * 1024)
                        if size_mb >= 0.1:  # Skip tiny files
                            self.logger.info(f"  🗑️  {item} ({size_mb:.1f}MB)")
                            if not dry_run:
                                item.unlink()
                                self.stats.files_removed += 1
                                self.stats.size_freed_mb += size_mb
    
    # Continue with other temp patterns...
    for pattern in temp_patterns:
        for temp_file in self.project_root.glob(pattern):
            if temp_file.is_file() and temp_file not in preserved_paths:
                size_mb = temp_file.stat().st_size / (1024 * 1024)
                
                # Skip tiny files and preserved results
                if size_mb < 0.1:
                    continue
                
                self.logger.info(f"  🗑️  {temp_file} ({size_mb:.1f}MB)")
                
                if not dry_run:
                    temp_file.unlink()
                    self.stats.files_removed += 1
                    self.stats.size_freed_mb += size_mb
    
    return self.stats
'''
        
        return integration_code

def main():
    """CLI entry point for test result preservation"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test Result Preservation System")
    parser.add_argument("--summary", action="store_true", help="Show test result summary")
    parser.add_argument("--archive", action="store_true", help="Create test result archive")
    parser.add_argument("--cleanup-old", type=int, metavar="DAYS", 
                       help="Clean up test results older than N days")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done")
    parser.add_argument("--show-integration", action="store_true", 
                       help="Show bloat prevention integration code")
    
    args = parser.parse_args()
    
    preservator = TestResultPreservationSystem()
    
    if args.summary:
        summary = preservator.get_test_result_summary()
        print("📊 TEST RESULT SUMMARY")
        print("=" * 50)
        print(f"Total files: {summary['total_files']}")
        print(f"Total size: {summary['total_size_mb']:.1f} MB")
        print(f"Newest result: {summary['newest_result']}")
        print(f"Oldest result: {summary['oldest_result']}")
        print("\nBy category:")
        for category, stats in summary['by_category'].items():
            print(f"  {category}: {stats['files']} files, {stats['size_mb']:.1f} MB")
    
    elif args.archive:
        archive_dir = preservator.create_test_result_archive()
        print(f"✅ Test results archived to: {archive_dir}")
    
    elif args.cleanup_old:
        cleanup_stats = preservator.cleanup_old_test_results(
            keep_days=args.cleanup_old, 
            dry_run=args.dry_run
        )
        print(f"Cleanup results:")
        print(f"  Files removed: {cleanup_stats['files_removed']}")
        print(f"  Size freed: {cleanup_stats['size_freed_mb']:.1f} MB")
        print(f"  Files preserved: {cleanup_stats['preserved_files']}")
    
    elif args.show_integration:
        print("Add this to your bloat prevention system:")
        print(preservator.integrate_with_bloat_prevention())
    
    else:
        print("Test Result Preservation System")
        print("✅ Protects valuable test results")
        print("✅ Allows safe cleanup of temporary data")
        print("✅ Maintains test result archives")
        
        summary = preservator.get_test_result_summary()
        print(f"\nCurrently preserving {summary['total_files']} test result files ({summary['total_size_mb']:.1f} MB)")

if __name__ == "__main__":
    main() 