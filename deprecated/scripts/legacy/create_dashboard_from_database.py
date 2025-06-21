#!/usr/bin/env python3
"""
Database-First Dashboard Generator
Creates dashboards directly from PostgreSQL database using job IDs
No JSON files required - true single source of truth architecture
"""

import argparse
import sys
import os
from pathlib import Path

# Add the src directory to the Python path
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))
sys.path.insert(0, str(project_root))  # Also add root for direct imports

from create_generic_multi_run_dashboard import create_dashboard_from_database
from src.utils.statistical_logger import logger

def list_recent_jobs(limit: int = 10):
    """List recent jobs for dashboard creation"""
    print(f"📋 Recent {limit} Jobs:")
    print("=" * 80)
    
    jobs = logger.get_recent_jobs(limit)
    
    if not jobs:
        print("❌ No jobs found in database")
        return
    
    for i, job in enumerate(jobs, 1):
        print(f"{i:2d}. Job ID: {job['job_id']}")
        print(f"    Speaker: {job['speaker']}")
        print(f"    Speech: {job['speech_type']}")
        print(f"    Framework: {job['framework']}")
        print(f"    Model: {job['model_name']}")
        print(f"    Runs: {job['total_runs']}")
        # Handle both string and datetime timestamps
        timestamp = job['timestamp']
        if hasattr(timestamp, 'strftime'):
            print(f"    Date: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print(f"    Date: {str(timestamp)[:19]}")
        print()

def create_dashboard_interactive():
    """Interactive dashboard creation"""
    print("🎨 Interactive Database Dashboard Creator")
    print("=" * 50)
    
    # List recent jobs
    list_recent_jobs(20)
    
    # Get job ID from user
    job_id = input("\n📝 Enter Job ID for dashboard creation: ").strip()
    
    if not job_id:
        print("❌ No Job ID provided")
        return
    
    # Get output filename (optional)
    output_file = input("📁 Output filename (optional, press Enter for auto): ").strip()
    if not output_file:
        output_file = None
    
    # Create dashboard
    print(f"\n🎨 Creating dashboard for job: {job_id}")
    result = create_dashboard_from_database(job_id, output_file)
    
    if result:
        print("✅ Dashboard created successfully!")
    else:
        print("❌ Dashboard creation failed")

def main():
    parser = argparse.ArgumentParser(description='Database-First Dashboard Generator')
    parser.add_argument('--job-id', '-j', type=str, help='Job ID for dashboard creation')
    parser.add_argument('--output', '-o', type=str, help='Output filename')
    parser.add_argument('--list', '-l', action='store_true', help='List recent jobs')
    parser.add_argument('--limit', type=int, default=10, help='Number of jobs to list (default: 10)')
    parser.add_argument('--interactive', '-i', action='store_true', help='Interactive mode')
    
    args = parser.parse_args()
    
    if args.list:
        list_recent_jobs(args.limit)
        return
    
    if args.interactive:
        create_dashboard_interactive()
        return
    
    if args.job_id:
        print(f"🎨 Creating database dashboard for job: {args.job_id}")
        result = create_dashboard_from_database(args.job_id, args.output)
        
        if result:
            print("✅ Dashboard created successfully!")
        else:
            print("❌ Dashboard creation failed")
            sys.exit(1)
    else:
        parser.print_help()
        print("\n💡 Examples:")
        print("  python create_dashboard_from_database.py --list")
        print("  python create_dashboard_from_database.py --interactive")
        print("  python create_dashboard_from_database.py --job-id trump_gpt4o_20250106_123456")

if __name__ == "__main__":
    main() 