#!/usr/bin/env python3
"""
Academic Data Export CLI - Simple wrapper for existing functionality

Uses the existing AcademicDataExporter to export PostgreSQL data to academic formats.
This is a thin CLI layer over the existing academic module functionality.

Usage:
    python export_academic_data.py --experiment-ids exp1,exp2 --output-dir exports/study2025 --formats csv,stata,r,json
    python export_academic_data.py --study-name my_study --all-experiments --include-metadata
"""

import argparse
import sys
from pathlib import Path

# Setup path for imports
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from src.academic import AcademicDataExporter, ReplicationPackageBuilder


def export_data_cli():
    """CLI interface for academic data export."""
    parser = argparse.ArgumentParser(description="Export academic data from PostgreSQL")
    
    # Data selection
    parser.add_argument("--experiment-ids", type=str, help="Comma-separated experiment IDs")
    parser.add_argument("--all-experiments", action="store_true", help="Export all experiments")
    parser.add_argument("--start-date", type=str, help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end-date", type=str, help="End date (YYYY-MM-DD)")
    parser.add_argument("--frameworks", type=str, help="Comma-separated framework names")
    
    # Output options
    parser.add_argument("--study-name", type=str, help="Study name for output files")
    parser.add_argument("--output-dir", type=str, default="exports/academic_formats", 
                       help="Output directory")
    parser.add_argument("--formats", type=str, default="csv,json,feather",
                       help="Export formats (csv,json,feather,stata)")
    
    # Additional options
    parser.add_argument("--include-metadata", action="store_true", 
                       help="Include comprehensive metadata")
    parser.add_argument("--include-component-analysis", action="store_true",
                       help="Include component development analysis")
    parser.add_argument("--create-replication-package", action="store_true",
                       help="Create complete replication package")
    
    args = parser.parse_args()
    
    try:
        # Initialize exporter using existing functionality
        exporter = AcademicDataExporter()
        
        # Prepare parameters
        framework_names = args.frameworks.split(',') if args.frameworks else None
        
        print("📊 Exporting academic data using existing infrastructure...")
        
        # Use existing export functionality
        export_files = exporter.export_experiments_data(
            start_date=args.start_date,
            end_date=args.end_date,
            framework_names=framework_names,
            study_name=args.study_name,
            output_dir=args.output_dir
        )
        
        print("✅ Data export completed successfully!")
        print("\n📁 Generated files:")
        for format_name, file_path in export_files.items():
            print(f"  • {format_name}: {file_path}")
        
        # Create replication package if requested
        if args.create_replication_package:
            print("\n📦 Creating replication package...")
            
            builder = ReplicationPackageBuilder()
            package_path = builder.build_replication_package(
                study_name=args.study_name or "academic_study",
                study_description="Academic analysis export",
                include_code=True,
                include_documentation=True
            )
            
            print(f"✅ Replication package created: {package_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ Export failed: {e}")
        return False


if __name__ == "__main__":
    success = export_data_cli()
    sys.exit(0 if success else 1) 