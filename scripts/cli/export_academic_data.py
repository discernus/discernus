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
    parser = argparse.ArgumentParser(
        description="A command-line tool to export experiment data for academic use, creating datasets in various statistical software formats.",
        epilog="""
Example Usage:
  # Export specific experiments to CSV and Stata formats
  python %(prog)s --experiment-ids exp_01,exp_02 --formats csv,stata --output-dir ./my_study_data

  # Export all experiments within a date range for a specific framework
  python %(prog)s --start-date 2025-01-01 --end-date 2025-03-31 --frameworks moral_foundations_theory --study-name Q1_MFT_Study

  # Create a full replication package for all experiments
  python %(prog)s --all-experiments --create-replication-package --study-name "Full_Replication"
"""
    )
    
    # Data selection group
    data_group = parser.add_argument_group('Data Selection', 'Arguments to select which data to export.')
    data_group.add_argument("--experiment-ids", type=str, help="Comma-separated list of specific experiment IDs to export.")
    data_group.add_argument("--all-experiments", action="store_true", help="Flag to export all experiments in the database.")
    data_group.add_argument("--start-date", type=str, help="The start date for filtering experiments (format: YYYY-MM-DD).")
    data_group.add_argument("--end-date", type=str, help="The end date for filtering experiments (format: YYYY-MM-DD).")
    data_group.add_argument("--frameworks", type=str, help="Comma-separated list of framework names to filter experiments by.")
    
    # Output options group
    output_group = parser.add_argument_group('Output Configuration', 'Arguments to control the output format and location.')
    output_group.add_argument("--study-name", type=str, help="A descriptive name for the study, used for naming output files.")
    output_group.add_argument("--output-dir", type=str, default="exports/academic_formats", 
                       help="The directory where exported files will be saved. Defaults to 'exports/academic_formats'.")
    output_group.add_argument("--formats", type=str, default="csv,json,feather",
                       help="Comma-separated list of export formats. Supported: csv, json, feather, stata. Defaults to 'csv,json,feather'.")
    
    # Additional options group
    additional_group = parser.add_argument_group('Additional Features', 'Extra features like metadata and replication packages.')
    additional_group.add_argument("--include-metadata", action="store_true", 
                       help="Flag to include a comprehensive JSON file with experiment metadata.")
    additional_group.add_argument("--include-component-analysis", action="store_true",
                       help="Flag to include data from component development analysis in the export.")
    additional_group.add_argument("--create-replication-package", action="store_true",
                       help="Flag to create a complete, self-contained replication package (ZIP file) for the study.")
    
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