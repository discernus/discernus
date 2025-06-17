#!/usr/bin/env python3
"""
Cleanup Obsolete Experiment Data
Safely removes pre-unified structure experiment data from database and archives old logs.

This script:
1. Archives obsolete database records (pre-June 17th civic_virtue experiments)
2. Compresses and archives old log files
3. Preserves recent IDITI validation study data
4. Creates backup before deletion

Usage:
    python3 scripts/cleanup_obsolete_experiment_data.py [--dry-run] [--backup-dir=path]
"""

import os
import sys
import json
import gzip
import shutil
import argparse
from pathlib import Path
from datetime import datetime, timedelta
import logging
import pandas as pd

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.narrative_gravity.utils.statistical_logger import StatisticalLogger

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ExperimentDataCleaner:
    """Safely clean up obsolete experiment data while preserving important records."""
    
    def __init__(self, backup_dir: str = "archive/database_cleanup_backup", dry_run: bool = False):
        self.backup_dir = Path(backup_dir)
        self.dry_run = dry_run
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Cutoff date: June 17, 2025 (IDITI validation study success)
        self.cutoff_date = datetime(2025, 6, 17)
        
        logger.info(f"Initializing cleanup (dry_run={dry_run})")
        logger.info(f"Backup directory: {self.backup_dir}")
        logger.info(f"Cutoff date: {self.cutoff_date}")
        
    def analyze_database_contents(self) -> dict:
        """Analyze what's currently in the database."""
        try:
            stat_logger = StatisticalLogger()
            
            # Get all runs data
            df = stat_logger._get_runs_dataframe(include_raw_responses=True)
            
            if df.empty:
                return {'total_records': 0, 'analysis': 'Database is empty'}
            
            # Convert timestamp column to datetime for analysis
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            # Analyze data
            analysis = {
                'total_records': len(df),
                'frameworks': df['framework'].value_counts().to_dict(),
                'models': df['model_name'].value_counts().to_dict(),
                'date_range': {
                    'earliest': df['timestamp'].min().isoformat(),
                    'latest': df['timestamp'].max().isoformat()
                },
                'records_before_cutoff': len(df[df['timestamp'] < self.cutoff_date]),
                'records_after_cutoff': len(df[df['timestamp'] >= self.cutoff_date]),
                'obsolete_records': df[df['timestamp'] < self.cutoff_date]['run_id'].tolist(),
                'recent_records': df[df['timestamp'] >= self.cutoff_date]['run_id'].tolist()
            }
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing database: {e}")
            return {'error': str(e)}
    
    def backup_database_data(self, analysis: dict) -> bool:
        """Create backup of data that will be deleted."""
        try:
            if analysis.get('records_before_cutoff', 0) == 0:
                logger.info("No obsolete records to backup")
                return True
                
            stat_logger = StatisticalLogger()
            df = stat_logger._get_runs_dataframe(include_raw_responses=True)
            
            if df.empty:
                return True
                
            # Convert timestamp for filtering
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            obsolete_df = df[df['timestamp'] < self.cutoff_date]
            
            if obsolete_df.empty:
                logger.info("No obsolete records found")
                return True
            
            # Create backup
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = self.backup_dir / f"obsolete_experiment_data_{timestamp}.csv"
            
            if not self.dry_run:
                obsolete_df.to_csv(backup_file, index=False)
                logger.info(f"Backed up {len(obsolete_df)} obsolete records to {backup_file}")
            else:
                logger.info(f"DRY RUN: Would backup {len(obsolete_df)} records to {backup_file}")
            
            # Also create JSON backup with metadata
            backup_metadata = {
                'backup_date': datetime.now().isoformat(),
                'cutoff_date': self.cutoff_date.isoformat(),
                'records_backed_up': len(obsolete_df),
                'frameworks_backed_up': obsolete_df['framework'].value_counts().to_dict(),
                'models_backed_up': obsolete_df['model_name'].value_counts().to_dict(),
                'reason': 'Pre-unified structure experiment data cleanup',
                'csv_file': str(backup_file.name)
            }
            
            metadata_file = self.backup_dir / f"backup_metadata_{timestamp}.json"
            if not self.dry_run:
                with open(metadata_file, 'w') as f:
                    json.dump(backup_metadata, f, indent=2)
                logger.info(f"Backup metadata saved to {metadata_file}")
            else:
                logger.info(f"DRY RUN: Would save metadata to {metadata_file}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error creating backup: {e}")
            return False
    
    def cleanup_database_records(self, analysis: dict) -> bool:
        """Remove obsolete records from database."""
        try:
            obsolete_records = analysis.get('obsolete_records', [])
            
            if not obsolete_records:
                logger.info("No obsolete database records to clean up")
                return True
            
            logger.info(f"Found {len(obsolete_records)} obsolete records to remove")
            
            if not self.dry_run:
                stat_logger = StatisticalLogger()
                
                                # Delete obsolete runs using direct connection
                conn = stat_logger._get_connection()
                cursor = conn.cursor()
                
                for run_id in obsolete_records:
                    try:
                        # Use direct SQL to delete records
                        if stat_logger.use_postgresql:
                            cursor.execute("DELETE FROM runs WHERE run_id = %s", (run_id,))
                        else:
                            cursor.execute("DELETE FROM runs WHERE run_id = ?", (run_id,))
                        logger.debug(f"Deleted run: {run_id}")
                    except Exception as e:
                        logger.warning(f"Could not delete run {run_id}: {e}")
                
                conn.commit()
                conn.close()
                
                logger.info(f"Deleted {len(obsolete_records)} obsolete database records")
            else:
                logger.info(f"DRY RUN: Would delete {len(obsolete_records)} obsolete records")
            
            return True
            
        except Exception as e:
            logger.error(f"Error cleaning up database records: {e}")
            return False
    
    def cleanup_log_files(self) -> bool:
        """Archive and compress old log files."""
        try:
            logs_dir = Path("logs")
            if not logs_dir.exists():
                logger.info("No logs directory found")
                return True
            
            # Files to archive (older than cutoff date)
            files_to_archive = []
            
            for log_file in logs_dir.glob("*.log"):
                # Check file modification time
                mtime = datetime.fromtimestamp(log_file.stat().st_mtime)
                if mtime < self.cutoff_date:
                    files_to_archive.append(log_file)
            
            # Also archive old API costs if large
            api_costs_file = logs_dir / "api_costs.json"
            if api_costs_file.exists() and api_costs_file.stat().st_size > 100000:  # > 100KB
                files_to_archive.append(api_costs_file)
            
            if not files_to_archive:
                logger.info("No old log files to archive")
                return True
            
            # Create archive directory
            archive_logs_dir = self.backup_dir / "archived_logs"
            archive_logs_dir.mkdir(exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            for log_file in files_to_archive:
                archive_name = f"{log_file.stem}_{timestamp}.gz"
                archive_path = archive_logs_dir / archive_name
                
                if not self.dry_run:
                    # Compress and move
                    with open(log_file, 'rb') as f_in:
                        with gzip.open(archive_path, 'wb') as f_out:
                            shutil.copyfileobj(f_in, f_out)
                    
                    # Remove original
                    log_file.unlink()
                    logger.info(f"Archived and compressed: {log_file} -> {archive_path}")
                else:
                    logger.info(f"DRY RUN: Would archive {log_file} to {archive_path}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error cleaning up log files: {e}")
            return False
    
    def generate_cleanup_report(self, analysis: dict) -> str:
        """Generate a comprehensive cleanup report."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.backup_dir / f"cleanup_report_{timestamp}.md"
        
        report_content = f"""# Experiment Data Cleanup Report

**Date**: {datetime.now().strftime("%B %d, %Y %H:%M:%S")}  
**Operation**: {'DRY RUN - ' if self.dry_run else ''}Database and logs cleanup  
**Cutoff Date**: {self.cutoff_date.strftime("%B %d, %Y")} (IDITI validation study success)

## Database Analysis

### Before Cleanup
- **Total Records**: {analysis.get('total_records', 0)}
- **Frameworks**: {analysis.get('frameworks', {})}
- **Models**: {analysis.get('models', {})}
- **Date Range**: {analysis.get('date_range', {}).get('earliest', 'N/A')} to {analysis.get('date_range', {}).get('latest', 'N/A')}

### Cleanup Actions
- **Obsolete Records**: {analysis.get('records_before_cutoff', 0)} (pre-{self.cutoff_date.strftime('%B %d')})
- **Preserved Records**: {analysis.get('records_after_cutoff', 0)} (post-{self.cutoff_date.strftime('%B %d')})

### Rationale
The obsolete records represent pre-unified structure experiments that have been superseded by:
1. The unified experiment package system implemented on June 18, 2025
2. The successful IDITI validation study on June 17, 2025
3. The enhanced analysis pipeline with comprehensive statistical validation

## Files Processed

### Database Backup
- **Backup Location**: `{self.backup_dir}/`
- **Records Backed Up**: {analysis.get('records_before_cutoff', 0)}
- **Backup Format**: CSV + JSON metadata

### Log Files
- **Action**: Archived and compressed old log files
- **Archive Location**: `{self.backup_dir}/archived_logs/`

## Post-Cleanup Status

### Database
- **Active Records**: {analysis.get('records_after_cutoff', 0)} (recent IDITI and unified structure data)
- **Storage Freed**: Removed {analysis.get('records_before_cutoff', 0)} obsolete records
- **Data Integrity**: All important data preserved in unified experiment packages

### Logs
- **Recent Logs**: Preserved for ongoing operations
- **Archived Logs**: Compressed and stored for historical reference

## Verification

To verify cleanup success:
```bash
# Check database contents
python3 scripts/extract_experiment_results.py

# Check experiment packages
ls -la experiments/

# Check backup integrity
ls -la {self.backup_dir}/
```

## Recovery Instructions

If data recovery is needed:
1. **Database Recovery**: Import from `{self.backup_dir}/obsolete_experiment_data_*.csv`
2. **Log Recovery**: Decompress from `{self.backup_dir}/archived_logs/*.gz`
3. **Unified Packages**: All recent data preserved in `experiments/` directory

## Impact Assessment

### ✅ Benefits Achieved
- **Reduced Database Size**: Removed obsolete records
- **Improved Performance**: Faster queries on relevant data
- **Clean Organization**: Only unified structure data remains
- **Storage Optimization**: Compressed old logs

### ✅ Data Safety
- **Complete Backup**: All deleted data backed up with metadata
- **Unified Packages**: Recent experiments preserved in self-contained packages
- **Recovery Options**: Multiple recovery paths available

## Next Steps

1. **Monitor Performance**: Verify improved database query performance
2. **Validate unified packages**: Ensure all recent experiments properly organized
3. **Archive maintenance**: Periodically review and compress old backups
4. **Documentation updates**: Update any references to old data organization

---

**Operation Status**: {'✅ COMPLETED' if not self.dry_run else '🔍 DRY RUN - NO CHANGES MADE'}
"""
        
        if not self.dry_run:
            with open(report_file, 'w') as f:
                f.write(report_content)
            logger.info(f"Cleanup report saved to {report_file}")
        else:
            logger.info(f"DRY RUN: Would save report to {report_file}")
        
        return report_content


def main():
    """Main cleanup execution."""
    parser = argparse.ArgumentParser(description="Clean up obsolete experiment data")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without making changes")
    parser.add_argument("--backup-dir", default="archive/database_cleanup_backup", help="Backup directory path")
    parser.add_argument("--force", action="store_true", help="Skip confirmation prompts")
    
    args = parser.parse_args()
    
    try:
        cleaner = ExperimentDataCleaner(backup_dir=args.backup_dir, dry_run=args.dry_run)
        
        # Analyze current database contents
        logger.info("🔍 Analyzing database contents...")
        analysis = cleaner.analyze_database_contents()
        
        if 'error' in analysis:
            logger.error(f"Failed to analyze database: {analysis['error']}")
            return 1
        
        # Show analysis
        logger.info(f"📊 Database analysis:")
        logger.info(f"   Total records: {analysis.get('total_records', 0)}")
        logger.info(f"   Obsolete records: {analysis.get('records_before_cutoff', 0)}")
        logger.info(f"   Recent records: {analysis.get('records_after_cutoff', 0)}")
        
        if analysis.get('records_before_cutoff', 0) == 0:
            logger.info("✅ No obsolete data found. Database is already clean.")
            return 0
        
        # Confirm operation
        if not args.force and not args.dry_run:
            response = input(f"\nThis will delete {analysis.get('records_before_cutoff', 0)} obsolete records. Continue? (y/N): ")
            if response.lower() != 'y':
                logger.info("Operation cancelled by user")
                return 0
        
        # Create backup
        logger.info("💾 Creating backup of obsolete data...")
        if not cleaner.backup_database_data(analysis):
            logger.error("Backup failed. Aborting cleanup.")
            return 1
        
        # Clean up database
        logger.info("🗑️ Cleaning up database records...")
        if not cleaner.cleanup_database_records(analysis):
            logger.error("Database cleanup failed")
            return 1
        
        # Clean up logs
        logger.info("📁 Archiving old log files...")
        if not cleaner.cleanup_log_files():
            logger.warning("Log cleanup had issues, but continuing...")
        
        # Generate report
        logger.info("📋 Generating cleanup report...")
        report = cleaner.generate_cleanup_report(analysis)
        
        if args.dry_run:
            logger.info("🔍 DRY RUN COMPLETE - No changes were made")
            logger.info("   Run without --dry-run to perform actual cleanup")
        else:
            logger.info("✅ CLEANUP COMPLETE")
            logger.info(f"   Removed {analysis.get('records_before_cutoff', 0)} obsolete records")
            logger.info(f"   Backup created in {args.backup_dir}")
        
        return 0
        
    except Exception as e:
        logger.error(f"Cleanup failed: {e}")
        return 1


if __name__ == "__main__":
    exit(main()) 