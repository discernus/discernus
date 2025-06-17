#!/usr/bin/env python3
"""
🎯 ORCHESTRATOR MONITORING & LOG MANAGEMENT SYSTEM

Enhances the existing cleanup system with specific support for:
- Orchestrator checkpoint management
- Transaction log monitoring  
- Experiment storage tracking
- Automated pruning with safety controls

This enhances scripts/cleanup_obsolete_experiment_data.py for the new orchestrator features.

🚨 AI ASSISTANTS: This extends existing production systems, doesn't replace them!
✅ Integrates with comprehensive_experiment_orchestrator.py monitoring needs
"""

import json
import gzip
import shutil
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class OrchestratorMonitoringSystem:
    """
    Enhanced monitoring for the orchestrator's comprehensive logging and checkpoint system.
    
    Monitors:
    - Experiment transaction logs and checkpoints
    - Storage utilization and growth trends
    - Failed/incomplete experiments needing cleanup
    - API cost accumulation and alerts
    - Log rotation and archival requirements
    """
    
    def __init__(self, 
                 logs_dir: str = "logs",
                 experiments_dir: str = "experiments", 
                 max_log_age_days: int = 30,
                 max_checkpoint_age_days: int = 7,
                 storage_warning_gb: float = 1.0):
        """
        Initialize monitoring system.
        
        Args:
            logs_dir: Directory containing log files
            experiments_dir: Directory containing experiment transactions
            max_log_age_days: Days to keep detailed logs before archiving
            max_checkpoint_age_days: Days to keep old checkpoints for incomplete experiments
            storage_warning_gb: GB threshold for storage warnings
        """
        self.logs_dir = Path(logs_dir)
        self.experiments_dir = Path(experiments_dir)
        self.max_log_age = timedelta(days=max_log_age_days)
        self.max_checkpoint_age = timedelta(days=max_checkpoint_age_days)
        self.storage_warning_threshold = storage_warning_gb * 1024 * 1024 * 1024  # Convert to bytes
        
        # Create monitoring state file
        self.state_file = self.logs_dir / "monitoring_state.json"
        self.load_monitoring_state()
    
    def load_monitoring_state(self) -> Dict:
        """Load previous monitoring state for trend analysis."""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r') as f:
                    self.monitoring_state = json.load(f)
            except Exception as e:
                logger.warning(f"Could not load monitoring state: {e}")
                self.monitoring_state = {}
        else:
            self.monitoring_state = {}
        return self.monitoring_state
    
    def save_monitoring_state(self, new_state: Dict):
        """Save monitoring state for trend tracking."""
        self.monitoring_state = new_state
        try:
            with open(self.state_file, 'w') as f:
                json.dump(self.monitoring_state, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Could not save monitoring state: {e}")
    
    def analyze_storage_usage(self) -> Dict:
        """Analyze storage usage across logs and experiments."""
        analysis = {
            'timestamp': datetime.now().isoformat(),
            'logs': {},
            'experiments': {},
            'total_size_bytes': 0,
            'warnings': [],
            'growth_trend': {}
        }
        
        # Analyze logs directory
        if self.logs_dir.exists():
            log_files = {}
            total_log_size = 0
            
            for log_file in self.logs_dir.glob("*"):
                if log_file.is_file():
                    size = log_file.stat().st_size
                    mtime = datetime.fromtimestamp(log_file.stat().st_mtime)
                    log_files[str(log_file.name)] = {
                        'size_bytes': size,
                        'size_mb': round(size / 1024 / 1024, 2),
                        'modified': mtime.isoformat(),
                        'age_days': (datetime.now() - mtime).days
                    }
                    total_log_size += size
            
            analysis['logs'] = {
                'total_size_bytes': total_log_size,
                'total_size_mb': round(total_log_size / 1024 / 1024, 2),
                'file_count': len(log_files),
                'files': log_files
            }
            analysis['total_size_bytes'] += total_log_size
        
        # Analyze experiments directory
        if self.experiments_dir.exists():
            experiment_dirs = {}
            total_exp_size = 0
            completed_experiments = 0
            failed_experiments = 0
            resumable_experiments = 0
            
            for exp_dir in self.experiments_dir.iterdir():
                if exp_dir.is_dir():
                    size = sum(f.stat().st_size for f in exp_dir.rglob('*') if f.is_file())
                    mtime = datetime.fromtimestamp(exp_dir.stat().st_mtime)
                    
                    # Check experiment status
                    checkpoint_file = exp_dir / "checkpoint.json"
                    status = "unknown"
                    if checkpoint_file.exists():
                        try:
                            with open(checkpoint_file, 'r') as f:
                                checkpoint = json.load(f)
                            status = checkpoint.get('state', 'unknown')
                            if checkpoint.get('can_resume', False):
                                resumable_experiments += 1
                            if status == "completed":
                                completed_experiments += 1
                            elif status == "failed":
                                failed_experiments += 1
                        except Exception:
                            status = "checkpoint_error"
                    
                    experiment_dirs[str(exp_dir.name)] = {
                        'size_bytes': size,
                        'size_mb': round(size / 1024 / 1024, 2),
                        'modified': mtime.isoformat(),
                        'age_days': (datetime.now() - mtime).days,
                        'status': status,
                        'has_checkpoint': checkpoint_file.exists()
                    }
                    total_exp_size += size
            
            analysis['experiments'] = {
                'total_size_bytes': total_exp_size,
                'total_size_mb': round(total_exp_size / 1024 / 1024, 2),
                'directory_count': len(experiment_dirs),
                'completed_experiments': completed_experiments,
                'failed_experiments': failed_experiments,
                'resumable_experiments': resumable_experiments,
                'directories': experiment_dirs
            }
            analysis['total_size_bytes'] += total_exp_size
        
        # Calculate total size and warnings
        total_size_gb = analysis['total_size_bytes'] / 1024 / 1024 / 1024
        analysis['total_size_gb'] = round(total_size_gb, 3)
        
        if analysis['total_size_bytes'] > self.storage_warning_threshold:
            analysis['warnings'].append(f"Storage usage ({total_size_gb:.2f} GB) exceeds warning threshold")
        
        # Calculate growth trend if we have previous data
        previous_state = self.monitoring_state.get('storage_analysis')
        if previous_state:
            try:
                prev_size = previous_state.get('total_size_bytes', 0)
                growth_bytes = analysis['total_size_bytes'] - prev_size
                
                prev_time = datetime.fromisoformat(previous_state.get('timestamp'))
                time_diff = datetime.now() - prev_time
                
                if time_diff.total_seconds() > 0:
                    growth_per_day = growth_bytes / (time_diff.total_seconds() / 86400)
                    analysis['growth_trend'] = {
                        'growth_bytes': growth_bytes,
                        'growth_mb': round(growth_bytes / 1024 / 1024, 2),
                        'growth_per_day_mb': round(growth_per_day / 1024 / 1024, 2),
                        'days_since_last_check': round(time_diff.total_seconds() / 86400, 1)
                    }
            except Exception as e:
                logger.warning(f"Could not calculate growth trend: {e}")
        
        return analysis
    
    def find_cleanup_candidates(self) -> Dict:
        """Find files and experiments that are candidates for cleanup."""
        candidates = {
            'old_logs': [],
            'failed_experiments': [],
            'old_checkpoints': [],
            'large_experiments': [],
            'recommendations': []
        }
        
        cutoff_date = datetime.now() - self.max_log_age
        checkpoint_cutoff = datetime.now() - self.max_checkpoint_age
        
        # Find old log files
        if self.logs_dir.exists():
            for log_file in self.logs_dir.glob("*.log"):
                mtime = datetime.fromtimestamp(log_file.stat().st_mtime)
                if mtime < cutoff_date:
                    candidates['old_logs'].append({
                        'file': str(log_file),
                        'size_mb': round(log_file.stat().st_size / 1024 / 1024, 2),
                        'age_days': (datetime.now() - mtime).days
                    })
        
        # Find experiment cleanup candidates
        if self.experiments_dir.exists():
            for exp_dir in self.experiments_dir.iterdir():
                if exp_dir.is_dir():
                    mtime = datetime.fromtimestamp(exp_dir.stat().st_mtime)
                    size_mb = sum(f.stat().st_size for f in exp_dir.rglob('*') if f.is_file()) / 1024 / 1024
                    
                    checkpoint_file = exp_dir / "checkpoint.json"
                    if checkpoint_file.exists():
                        try:
                            with open(checkpoint_file, 'r') as f:
                                checkpoint = json.load(f)
                            
                            status = checkpoint.get('state', 'unknown')
                            can_resume = checkpoint.get('can_resume', False)
                            
                            # Old failed experiments
                            if status == "failed" and mtime < checkpoint_cutoff:
                                candidates['failed_experiments'].append({
                                    'directory': str(exp_dir.name),
                                    'status': status,
                                    'size_mb': round(size_mb, 2),
                                    'age_days': (datetime.now() - mtime).days
                                })
                            
                            # Old incomplete experiments that can't be resumed
                            elif not can_resume and status != "completed" and mtime < checkpoint_cutoff:
                                candidates['old_checkpoints'].append({
                                    'directory': str(exp_dir.name),
                                    'status': status,
                                    'size_mb': round(size_mb, 2),
                                    'age_days': (datetime.now() - mtime).days
                                })
                            
                        except Exception:
                            # Corrupted checkpoint - candidate for cleanup
                            if mtime < checkpoint_cutoff:
                                candidates['old_checkpoints'].append({
                                    'directory': str(exp_dir.name),
                                    'status': 'corrupted_checkpoint',
                                    'size_mb': round(size_mb, 2),
                                    'age_days': (datetime.now() - mtime).days
                                })
                    
                    # Large completed experiments (for archival consideration)
                    if size_mb > 50:  # > 50MB
                        candidates['large_experiments'].append({
                            'directory': str(exp_dir.name),
                            'size_mb': round(size_mb, 2),
                            'age_days': (datetime.now() - mtime).days
                        })
        
        # Generate recommendations
        if candidates['old_logs']:
            total_log_mb = sum(item['size_mb'] for item in candidates['old_logs'])
            candidates['recommendations'].append(f"Archive {len(candidates['old_logs'])} old log files ({total_log_mb:.1f} MB)")
        
        if candidates['failed_experiments']:
            total_failed_mb = sum(item['size_mb'] for item in candidates['failed_experiments'])
            candidates['recommendations'].append(f"Clean up {len(candidates['failed_experiments'])} failed experiments ({total_failed_mb:.1f} MB)")
        
        if candidates['old_checkpoints']:
            total_checkpoint_mb = sum(item['size_mb'] for item in candidates['old_checkpoints'])
            candidates['recommendations'].append(f"Remove {len(candidates['old_checkpoints'])} old incomplete experiments ({total_checkpoint_mb:.1f} MB)")
        
        if candidates['large_experiments']:
            candidates['recommendations'].append(f"Consider archiving {len(candidates['large_experiments'])} large experiments")
        
        return candidates
    
    def monitor_api_costs(self) -> Dict:
        """Monitor API cost accumulation and trends."""
        api_costs_file = self.logs_dir / "api_costs.json"
        
        cost_analysis = {
            'file_exists': False,
            'total_cost': 0.0,
            'recent_cost': 0.0,
            'daily_average': 0.0,
            'warnings': []
        }
        
        if api_costs_file.exists():
            try:
                with open(api_costs_file, 'r') as f:
                    costs_data = json.load(f)
                
                cost_analysis['file_exists'] = True
                cost_analysis['file_size_mb'] = round(api_costs_file.stat().st_size / 1024 / 1024, 3)
                
                # Calculate cost metrics if data is available
                if isinstance(costs_data, dict) and 'total_cost' in costs_data:
                    cost_analysis['total_cost'] = costs_data.get('total_cost', 0.0)
                    
                    # Get recent costs (last 7 days)
                    recent_costs = []
                    cutoff_date = datetime.now() - timedelta(days=7)
                    
                    for entry in costs_data.get('cost_history', []):
                        if 'timestamp' in entry:
                            entry_date = datetime.fromisoformat(entry['timestamp'])
                            if entry_date > cutoff_date:
                                recent_costs.append(entry.get('cost', 0.0))
                    
                    cost_analysis['recent_cost'] = sum(recent_costs)
                    cost_analysis['daily_average'] = cost_analysis['recent_cost'] / 7 if recent_costs else 0.0
                
                # Check for cost warnings
                if cost_analysis['daily_average'] > 5.0:  # > $5/day average
                    cost_analysis['warnings'].append(f"High daily cost average: ${cost_analysis['daily_average']:.2f}")
                
                if cost_analysis['total_cost'] > 100.0:  # > $100 total
                    cost_analysis['warnings'].append(f"High total cost: ${cost_analysis['total_cost']:.2f}")
                
            except Exception as e:
                cost_analysis['error'] = str(e)
        
        return cost_analysis
    
    def generate_monitoring_report(self) -> Dict:
        """Generate comprehensive monitoring report."""
        report = {
            'timestamp': datetime.now().isoformat(),
            'storage_analysis': self.analyze_storage_usage(),
            'cleanup_candidates': self.find_cleanup_candidates(),
            'api_costs': self.monitor_api_costs(),
            'system_health': {
                'orchestrator_log_size_mb': 0,
                'active_experiments': 0,
                'resumable_experiments': 0,
                'storage_warnings': []
            }
        }
        
        # System health summary
        orchestrator_log = self.logs_dir / "experiment_orchestrator.log"
        if orchestrator_log.exists():
            report['system_health']['orchestrator_log_size_mb'] = round(
                orchestrator_log.stat().st_size / 1024 / 1024, 2
            )
        
        exp_analysis = report['storage_analysis']['experiments']
        report['system_health']['active_experiments'] = exp_analysis.get('directory_count', 0)
        report['system_health']['resumable_experiments'] = exp_analysis.get('resumable_experiments', 0)
        
        # Aggregate warnings
        all_warnings = []
        all_warnings.extend(report['storage_analysis'].get('warnings', []))
        all_warnings.extend(report['api_costs'].get('warnings', []))
        report['system_health']['storage_warnings'] = all_warnings
        
        # Save state for trend analysis
        self.save_monitoring_state(report)
        
        return report
    
    def create_cleanup_script(self, report: Dict, output_file: str = None) -> str:
        """Generate a safe cleanup script based on monitoring report."""
        if output_file is None:
            output_file = f"experimental/prototypes/auto_cleanup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sh"
        
        cleanup_candidates = report['cleanup_candidates']
        
        script_content = f"""#!/bin/bash
# Auto-generated cleanup script from orchestrator monitoring
# Generated: {datetime.now().isoformat()}
# 
# ⚠️  REVIEW BEFORE RUNNING - This affects experiment data!
# ✅ Safe to run: Archives data rather than deleting
#
# Usage: bash {output_file} [--dry-run]

set -e  # Exit on error

DRY_RUN=false
if [[ "$1" == "--dry-run" ]]; then
    DRY_RUN=true
    echo "🔍 DRY RUN MODE - No changes will be made"
fi

echo "🧹 Starting orchestrator data cleanup..."
echo "📊 Based on monitoring report from {report['timestamp']}"

# Create archive directory
ARCHIVE_DIR="archive/monitoring_cleanup_$(date +%Y%m%d_%H%M%S)"
if [[ "$DRY_RUN" == "false" ]]; then
    mkdir -p "$ARCHIVE_DIR/logs"
    mkdir -p "$ARCHIVE_DIR/experiments"
fi

"""
        
        # Add log file archival
        if cleanup_candidates['old_logs']:
            script_content += "\n# Archive old log files\n"
            for log_item in cleanup_candidates['old_logs']:
                log_file = log_item['file']
                script_content += f"""
if [[ "$DRY_RUN" == "false" ]]; then
    gzip -c "{log_file}" > "$ARCHIVE_DIR/logs/$(basename {log_file}).gz"
    rm "{log_file}"
    echo "✅ Archived: {log_file} ({log_item['size_mb']} MB)"
else
    echo "📋 Would archive: {log_file} ({log_item['size_mb']} MB)"
fi"""
        
        # Add failed experiment cleanup
        if cleanup_candidates['failed_experiments']:
            script_content += "\n\n# Archive failed experiments\n"
            for exp_item in cleanup_candidates['failed_experiments']:
                exp_dir = f"experiments/{exp_item['directory']}"
                script_content += f"""
if [[ "$DRY_RUN" == "false" ]]; then
    tar -czf "$ARCHIVE_DIR/experiments/{exp_item['directory']}.tar.gz" "{exp_dir}"
    rm -rf "{exp_dir}"
    echo "✅ Archived failed experiment: {exp_item['directory']} ({exp_item['size_mb']} MB)"
else
    echo "📋 Would archive failed experiment: {exp_item['directory']} ({exp_item['size_mb']} MB)"
fi"""
        
        script_content += f"""

echo ""
echo "🎯 Cleanup Summary:"
echo "   Old logs: {len(cleanup_candidates['old_logs'])} files"
echo "   Failed experiments: {len(cleanup_candidates['failed_experiments'])} directories" 
echo "   Archive location: $ARCHIVE_DIR"
echo ""
echo "✅ Cleanup complete!"
"""
        
        # Write script file
        script_path = Path(output_file)
        script_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        # Make executable
        script_path.chmod(0o755)
        
        return str(script_path)


def main():
    """Demonstrate the monitoring system."""
    print("🎯 ORCHESTRATOR MONITORING SYSTEM DEMONSTRATION")
    print("=" * 60)
    
    monitor = OrchestratorMonitoringSystem()
    
    print("\n📊 Generating monitoring report...")
    report = monitor.generate_monitoring_report()
    
    # Display summary
    storage = report['storage_analysis']
    print(f"\n📁 Storage Analysis:")
    print(f"   Total Size: {storage['total_size_gb']:.2f} GB")
    print(f"   Logs: {storage['logs']['total_size_mb']:.1f} MB ({storage['logs']['file_count']} files)")
    print(f"   Experiments: {storage['experiments']['total_size_mb']:.1f} MB ({storage['experiments']['directory_count']} dirs)")
    
    if storage.get('growth_trend'):
        growth = storage['growth_trend']
        print(f"   Growth Rate: {growth['growth_per_day_mb']:.1f} MB/day")
    
    # Display system health
    health = report['system_health']
    print(f"\n🏥 System Health:")
    print(f"   Orchestrator Log: {health['orchestrator_log_size_mb']:.1f} MB")
    print(f"   Active Experiments: {health['active_experiments']}")
    print(f"   Resumable Experiments: {health['resumable_experiments']}")
    
    # Display warnings
    if health['storage_warnings']:
        print(f"\n⚠️  Warnings:")
        for warning in health['storage_warnings']:
            print(f"   • {warning}")
    else:
        print(f"\n✅ No storage warnings")
    
    # Display cleanup recommendations
    cleanup = report['cleanup_candidates']
    if cleanup['recommendations']:
        print(f"\n🧹 Cleanup Recommendations:")
        for recommendation in cleanup['recommendations']:
            print(f"   • {recommendation}")
        
        # Generate cleanup script
        script_path = monitor.create_cleanup_script(report)
        print(f"\n🔧 Generated cleanup script: {script_path}")
        print(f"   Usage: bash {script_path} --dry-run")
    else:
        print(f"\n✅ No cleanup needed at this time")
    
    # API costs
    costs = report['api_costs']
    if costs['file_exists']:
        print(f"\n💰 API Costs:")
        print(f"   Total: ${costs['total_cost']:.2f}")
        print(f"   Recent (7 days): ${costs['recent_cost']:.2f}")
        print(f"   Daily Average: ${costs['daily_average']:.2f}")
    
    # Save detailed report
    report_file = f"experimental/prototypes/monitoring_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    print(f"\n📋 Detailed report saved: {report_file}")
    print(f"\n🎯 INTEGRATION WITH EXISTING SYSTEMS:")
    print(f"   • Enhances scripts/cleanup_obsolete_experiment_data.py")
    print(f"   • Monitors comprehensive_experiment_orchestrator.py output")
    print(f"   • Provides automated cleanup recommendations")
    print(f"   • Tracks storage growth and API cost trends")


if __name__ == "__main__":
    main() 