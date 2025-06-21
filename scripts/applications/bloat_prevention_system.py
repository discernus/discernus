#!/usr/bin/env python3
"""
Bloat Prevention System

Comprehensive system to prevent storage, logging, and database bloat
from testing and development activities.
"""

import os
import shutil
import sqlite3
import json
import time
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import logging
import argparse

@dataclass
class CleanupStats:
    """Statistics from cleanup operations"""
    files_removed: int = 0
    directories_removed: int = 0
    size_freed_mb: float = 0.0
    database_records_removed: int = 0
    log_lines_truncated: int = 0

class BloatPreventionSystem:
    """Comprehensive bloat prevention and cleanup system"""
    
    def __init__(self, project_root: Path = None):
        self.project_root = project_root or Path.cwd()
        self.stats = CleanupStats()
        
        # Configure logging for cleanup operations
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    # ========================================================================
    # EXPERIMENT DIRECTORY CLEANUP
    # ========================================================================
    
    def cleanup_test_experiments(self, dry_run: bool = False, 
                               days_old: int = 7) -> CleanupStats:
        """Clean up test experiment directories"""
        experiments_dir = self.project_root / "experiments"
        if not experiments_dir.exists():
            return self.stats
        
        self.logger.info(f"🧹 Cleaning up test experiments older than {days_old} days...")
        
        cutoff_date = datetime.now() - timedelta(days=days_old)
        test_patterns = [
            "MFT_Academic_Validation_Study_",
            "MFT_Simple_Test_",
            "IDITI_",
            "_Test_",
            "_Demo_",
            "_validation_"
        ]
        
        for experiment_dir in experiments_dir.iterdir():
            if not experiment_dir.is_dir():
                continue
            
            # Check if it's a test experiment
            is_test = any(pattern in experiment_dir.name for pattern in test_patterns)
            if not is_test:
                continue
            
            # Check age
            created_time = datetime.fromtimestamp(experiment_dir.stat().st_ctime)
            if created_time > cutoff_date:
                continue
            
            # Calculate size
            size_mb = self._get_directory_size_mb(experiment_dir)
            
            self.logger.info(f"  🗑️  {experiment_dir.name} ({size_mb:.1f}MB, {created_time.strftime('%Y-%m-%d')})")
            
            if not dry_run:
                shutil.rmtree(experiment_dir)
                self.stats.directories_removed += 1
                self.stats.size_freed_mb += size_mb
        
        return self.stats
    
    def cleanup_duplicate_experiments(self, dry_run: bool = False) -> CleanupStats:
        """Remove duplicate experiment directories (keep latest)"""
        experiments_dir = self.project_root / "experiments"
        if not experiments_dir.exists():
            return self.stats
        
        self.logger.info("🧹 Cleaning up duplicate experiment directories...")
        
        # Group by base name (without timestamp)
        experiment_groups = {}
        for experiment_dir in experiments_dir.iterdir():
            if not experiment_dir.is_dir():
                continue
            
            # Extract base name (remove timestamp)
            base_name = self._extract_experiment_base_name(experiment_dir.name)
            if base_name not in experiment_groups:
                experiment_groups[base_name] = []
            experiment_groups[base_name].append(experiment_dir)
        
        # For each group, keep only the newest
        for base_name, directories in experiment_groups.items():
            if len(directories) <= 1:
                continue
            
            # Sort by creation time, keep newest
            directories.sort(key=lambda d: d.stat().st_ctime, reverse=True)
            keep = directories[0]
            remove = directories[1:]
            
            self.logger.info(f"  📁 {base_name}: keeping {keep.name}, removing {len(remove)} duplicates")
            
            for old_dir in remove:
                size_mb = self._get_directory_size_mb(old_dir)
                self.logger.info(f"    🗑️  {old_dir.name} ({size_mb:.1f}MB)")
                
                if not dry_run:
                    shutil.rmtree(old_dir)
                    self.stats.directories_removed += 1
                    self.stats.size_freed_mb += size_mb
        
        return self.stats
    
    # ========================================================================
    # LOG FILE MANAGEMENT
    # ========================================================================
    
    def rotate_logs(self, dry_run: bool = False, 
                   max_size_mb: float = 10.0, 
                   keep_lines: int = 1000) -> CleanupStats:
        """Rotate large log files"""
        logs_dir = self.project_root / "logs"
        if not logs_dir.exists():
            return self.stats
        
        self.logger.info(f"🧹 Rotating log files larger than {max_size_mb}MB...")
        
        for log_file in logs_dir.glob("*.log"):
            size_mb = log_file.stat().st_size / (1024 * 1024)
            
            if size_mb <= max_size_mb:
                continue
            
            self.logger.info(f"  📝 {log_file.name} ({size_mb:.1f}MB)")
            
            if not dry_run:
                # Read last N lines
                with open(log_file, 'r') as f:
                    lines = f.readlines()
                
                if len(lines) > keep_lines:
                    # Keep only last N lines
                    kept_lines = lines[-keep_lines:]
                    
                    # Archive old content
                    archive_name = f"{log_file.stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.archive.log"
                    archive_path = logs_dir / archive_name
                    
                    # Write archive
                    with open(archive_path, 'w') as f:
                        f.writelines(lines[:-keep_lines])
                    
                    # Write truncated log
                    with open(log_file, 'w') as f:
                        f.write(f"# Log rotated on {datetime.now()}\n")
                        f.write(f"# Archived {len(lines) - keep_lines} lines to {archive_name}\n\n")
                        f.writelines(kept_lines)
                    
                    self.stats.log_lines_truncated += len(lines) - keep_lines
                    self.stats.size_freed_mb += size_mb * 0.8  # Estimate
        
        return self.stats
    
    def cleanup_old_log_archives(self, dry_run: bool = False, 
                                days_old: int = 30) -> CleanupStats:
        """Remove old log archives"""
        logs_dir = self.project_root / "logs"
        if not logs_dir.exists():
            return self.stats
        
        self.logger.info(f"🧹 Cleaning up log archives older than {days_old} days...")
        
        cutoff_date = datetime.now() - timedelta(days=days_old)
        
        for archive_file in logs_dir.glob("*.archive.log"):
            created_time = datetime.fromtimestamp(archive_file.stat().st_ctime)
            if created_time <= cutoff_date:
                size_mb = archive_file.stat().st_size / (1024 * 1024)
                self.logger.info(f"  🗑️  {archive_file.name} ({size_mb:.1f}MB)")
                
                if not dry_run:
                    archive_file.unlink()
                    self.stats.files_removed += 1
                    self.stats.size_freed_mb += size_mb
        
        return self.stats
    
    # ========================================================================
    # DATABASE CLEANUP
    # ========================================================================
    
    def cleanup_test_database_records(self, dry_run: bool = False) -> CleanupStats:
        """Clean up test records from database"""
        self.logger.info("🧹 Cleaning up test database records...")
        
        # This would connect to your actual database
        # For now, we'll handle the local SQLite files
        
        # Clean up local database files
        for db_file in self.project_root.rglob("*.db"):
            if "test" in db_file.name.lower() or db_file.stat().st_size == 0:
                size_mb = db_file.stat().st_size / (1024 * 1024)
                self.logger.info(f"  🗑️  {db_file} ({size_mb:.1f}MB)")
                
                if not dry_run and size_mb > 0:
                    db_file.unlink()
                    self.stats.files_removed += 1
                    self.stats.size_freed_mb += size_mb
        
        return self.stats
    
    # ========================================================================
    # ASSET STORAGE CLEANUP
    # ========================================================================
    
    def cleanup_orphaned_assets(self, dry_run: bool = False) -> CleanupStats:
        """Clean up orphaned assets in content-addressable storage"""
        asset_storage_dir = self.project_root / "asset_storage"
        if not asset_storage_dir.exists():
            return self.stats
        
        self.logger.info("🧹 Cleaning up orphaned assets...")
        
        # This is a simplified version - in production you'd check database references
        # For now, just clean up empty directories
        
        for asset_type_dir in asset_storage_dir.iterdir():
            if not asset_type_dir.is_dir():
                continue
            
            for hash_prefix_dir in asset_type_dir.iterdir():
                if not hash_prefix_dir.is_dir():
                    continue
                
                # Check if directory is empty or contains only empty subdirs
                if self._is_empty_recursive(hash_prefix_dir):
                    self.logger.info(f"  🗑️  Empty directory: {hash_prefix_dir}")
                    
                    if not dry_run:
                        shutil.rmtree(hash_prefix_dir)
                        self.stats.directories_removed += 1
        
        return self.stats
    
    # ========================================================================
    # TEMPORARY FILE CLEANUP
    # ========================================================================
    
    def cleanup_temp_files(self, dry_run: bool = False) -> CleanupStats:
        """Clean up temporary files and caches"""
        self.logger.info("🧹 Cleaning up temporary files...")
        
        # Import test result preservation
        try:
            import sys
            sys.path.append(str(Path(__file__).parent))
            from test_result_preservation_system import TestResultPreservationSystem
            preservator = TestResultPreservationSystem(self.project_root)
            preserved_paths = preservator.get_preserved_paths()
            self.logger.info(f"🔒 Protecting {len([p for p in preserved_paths if p.is_file()])} test result files")
        except ImportError:
            preserved_paths = set()
            self.logger.warning("Test result preservation not available")
        
        temp_patterns = [
            "tmp/**/*",
            "**/*.tmp", 
            "**/*.cache",
            "**/__pycache__/**/*",
            # REMOVED: "**/test_output/**/*" - now handled selectively below
        ]
        
        # Handle test_output selectively to preserve test results
        test_output_dirs = list(self.project_root.glob("**/test_output/"))
        for test_output_dir in test_output_dirs:
            if test_output_dir.is_dir():
                for item in test_output_dir.rglob("*"):
                    if item.is_file():
                        # Check if this is a preserved test result
                        is_preserved = (item in preserved_paths or 
                                      (hasattr(preservator, 'is_test_result_file') and 
                                       preservator.is_test_result_file(item)))
                        
                        if not is_preserved:
                            # Safe to clean up
                            size_mb = item.stat().st_size / (1024 * 1024)
                            if size_mb >= 0.1:  # Skip tiny files
                                self.logger.info(f"  🗑️  {item} ({size_mb:.1f}MB)")
                                if not dry_run:
                                    item.unlink()
                                    self.stats.files_removed += 1
                                    self.stats.size_freed_mb += size_mb
                        else:
                            self.logger.debug(f"  🔒 Preserving test result: {item}")
        
        # Continue with other temp patterns
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
    
    # ========================================================================
    # UTILITY METHODS
    # ========================================================================
    
    def _get_directory_size_mb(self, directory: Path) -> float:
        """Get directory size in MB"""
        total_size = 0
        try:
            for dirpath, dirnames, filenames in os.walk(directory):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    if os.path.exists(filepath):
                        total_size += os.path.getsize(filepath)
        except (OSError, FileNotFoundError):
            pass
        return total_size / (1024 * 1024)
    
    def _extract_experiment_base_name(self, name: str) -> str:
        """Extract base experiment name without timestamp"""
        # Remove common timestamp patterns
        import re
        patterns = [
            r'_\d{8}_\d{6}$',  # _20250619_123456
            r'_v?\d+\.\d+\.\d+_\d{8}_\d{6}$',  # _v1.0.0_20250619_123456
            r'_\d{4}-\d{2}-\d{2}$',  # _2025-06-19
        ]
        
        base_name = name
        for pattern in patterns:
            base_name = re.sub(pattern, '', base_name)
        
        return base_name
    
    def _is_empty_recursive(self, directory: Path) -> bool:
        """Check if directory is empty recursively"""
        try:
            for item in directory.rglob("*"):
                if item.is_file():
                    return False
            return True
        except (OSError, PermissionError):
            return False
    
    # ========================================================================
    # MAIN CLEANUP ORCHESTRATION
    # ========================================================================
    
    def run_full_cleanup(self, dry_run: bool = False, 
                        aggressive: bool = False) -> CleanupStats:
        """Run comprehensive cleanup"""
        self.logger.info("🧹 Starting comprehensive bloat prevention cleanup...")
        self.logger.info(f"Mode: {'DRY RUN' if dry_run else 'LIVE CLEANUP'}")
        
        # Reset stats
        self.stats = CleanupStats()
        
        # Run cleanup operations
        self.cleanup_test_experiments(dry_run, days_old=3 if aggressive else 7)
        self.cleanup_duplicate_experiments(dry_run)
        self.rotate_logs(dry_run, max_size_mb=5.0 if aggressive else 10.0)
        self.cleanup_old_log_archives(dry_run, days_old=7 if aggressive else 30)
        self.cleanup_test_database_records(dry_run)
        self.cleanup_orphaned_assets(dry_run)
        self.cleanup_temp_files(dry_run)
        
        # Print summary
        self.logger.info("=" * 60)
        self.logger.info("🎯 CLEANUP SUMMARY:")
        self.logger.info(f"  📁 Directories removed: {self.stats.directories_removed}")
        self.logger.info(f"  📄 Files removed: {self.stats.files_removed}")
        self.logger.info(f"  💾 Space freed: {self.stats.size_freed_mb:.1f} MB")
        self.logger.info(f"  🗃️  Database records removed: {self.stats.database_records_removed}")
        self.logger.info(f"  📝 Log lines truncated: {self.stats.log_lines_truncated}")
        
        return self.stats
    
    def setup_automated_cleanup(self):
        """Set up automated cleanup (cron job, etc.)"""
        # This would set up automated cleanup scheduling
        script_content = f"""#!/bin/bash
# Auto-generated bloat prevention cleanup
cd {self.project_root}
python3 scripts/production/bloat_prevention_system.py --auto-cleanup
"""
        
        script_path = self.project_root / "scripts" / "auto_cleanup.sh"
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        script_path.chmod(0o755)
        
        self.logger.info(f"✅ Automated cleanup script created: {script_path}")
        self.logger.info("To schedule daily cleanup, add to crontab:")
        self.logger.info(f"0 2 * * * {script_path}")

def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(description="Bloat Prevention System")
    parser.add_argument("--dry-run", action="store_true", 
                       help="Show what would be cleaned without actually doing it")
    parser.add_argument("--aggressive", action="store_true",
                       help="More aggressive cleanup (shorter retention periods)")
    parser.add_argument("--auto-cleanup", action="store_true",
                       help="Run automated daily cleanup")
    parser.add_argument("--setup-automation", action="store_true",
                       help="Set up automated cleanup scheduling")
    
    args = parser.parse_args()
    
    cleaner = BloatPreventionSystem()
    
    if args.setup_automation:
        cleaner.setup_automated_cleanup()
        return 0
    
    if args.auto_cleanup:
        # Automated mode - less verbose, moderate cleanup
        cleaner.run_full_cleanup(dry_run=False, aggressive=False)
    else:
        # Interactive mode
        cleaner.run_full_cleanup(dry_run=args.dry_run, aggressive=args.aggressive)
    
    return 0

if __name__ == "__main__":
    exit(main()) 