#!/usr/bin/env python3
"""
Academic Data Exporter - Priority 3 CLI Tool

Export experimental data in academic-standard formats for statistical analysis
in R, Stata, Python, and other academic tools.

Supports Elena's Week 3 workflow for academic tool integration.

Usage:
    python export_academic_data.py --study-name week3_validation --format all
    python export_academic_data.py --study-name framework_comparison --frameworks civic_virtue,political_spectrum --format csv,feather
    python export_academic_data.py --help
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime

# Add src to path for development mode
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.narrative_gravity.academic.data_export import AcademicDataExporter, ReplicationPackageBuilder


def main():
    parser = argparse.ArgumentParser(
        description="Export experimental data in academic-standard formats",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Export all data in all formats:
    python export_academic_data.py --study-name week3_validation --format all

  Export specific frameworks:
    python export_academic_data.py --study-name framework_comparison \\
        --frameworks civic_virtue,political_spectrum \\
        --format csv,feather

  Export date range:
    python export_academic_data.py --study-name june_analysis \\
        --start-date 2025-06-01 --end-date 2025-06-30 \\
        --format stata,json

  Export component development data:
    python export_academic_data.py --study-name component_evolution \\
        --component-analysis --component-type prompt_template \\
        --format csv

  Build replication package:
    python export_academic_data.py --study-name validation_study \\
        --replication-package \\
        --description "Validation study for LLM narrative analysis"
        """
    )
    
    parser.add_argument(
        "--study-name",
        required=True,
        help="Study name for output file naming"
    )
    
    parser.add_argument(
        "--format",
        default="all",
        help="Export formats: csv, feather, stata, json, all (default: all)"
    )
    
    parser.add_argument(
        "--output-dir",
        default="exports/academic_formats",
        help="Output directory for exported files (default: exports/academic_formats)"
    )
    
    # Data filtering options
    parser.add_argument(
        "--start-date",
        help="Start date for filtering (ISO format: 2025-06-01)"
    )
    
    parser.add_argument(
        "--end-date", 
        help="End date for filtering (ISO format: 2025-06-30)"
    )
    
    parser.add_argument(
        "--frameworks",
        help="Comma-separated list of framework names to include"
    )
    
    # Component analysis options
    parser.add_argument(
        "--component-analysis",
        action="store_true",
        help="Export component development data instead of experimental data"
    )
    
    parser.add_argument(
        "--component-type",
        choices=["prompt_template", "framework", "weighting_methodology", "all"],
        default="all",
        help="Component type for analysis export (default: all)"
    )
    
    parser.add_argument(
        "--include-development-sessions",
        action="store_true",
        help="Include development session data in component analysis"
    )
    
    # Replication package options
    parser.add_argument(
        "--replication-package",
        action="store_true",
        help="Build complete replication package instead of data export"
    )
    
    parser.add_argument(
        "--description",
        help="Study description for replication package documentation"
    )
    
    parser.add_argument(
        "--include-code",
        action="store_true",
        default=True,
        help="Include analysis code templates in replication package"
    )
    
    parser.add_argument(
        "--include-documentation",
        action="store_true", 
        default=True,
        help="Include methodology documentation in replication package"
    )
    
    args = parser.parse_args()
    
    # Initialize exporter
    exporter = AcademicDataExporter()
    
    try:
        if args.replication_package:
            # Build replication package
            if not args.description:
                print("❌ Error: --description is required for replication packages")
                sys.exit(1)
            
            print("📦 Building replication package...")
            
            builder = ReplicationPackageBuilder()
            
            # Build data filters
            data_filters = {}
            if args.start_date:
                data_filters['start_date'] = args.start_date
            if args.end_date:
                data_filters['end_date'] = args.end_date
            if args.frameworks:
                data_filters['frameworks'] = args.frameworks.split(',')
            
            package_path = builder.build_replication_package(
                study_name=args.study_name,
                study_description=args.description,
                data_filters=data_filters if data_filters else None,
                include_code=args.include_code,
                include_documentation=args.include_documentation,
                output_path="exports/replication_packages"
            )
            
            print(f"✅ Replication package created: {package_path}")
            
        elif args.component_analysis:
            # Export component development data
            print("🔧 Exporting component development data...")
            
            output_files = exporter.export_component_analysis_data(
                component_type=args.component_type,
                include_development_sessions=args.include_development_sessions,
                output_dir=args.output_dir
            )
            
            print("✅ Component analysis data exported:")
            for format_name, file_path in output_files.items():
                print(f"   {format_name}: {file_path}")
            
        else:
            # Export experimental data
            print("📊 Exporting experimental data...")
            
            # Parse framework list
            framework_names = None
            if args.frameworks:
                framework_names = [f.strip() for f in args.frameworks.split(',')]
            
            # Determine formats to export
            requested_formats = args.format.split(',') if args.format != 'all' else ['all']
            
            output_files = exporter.export_experiments_data(
                start_date=args.start_date,
                end_date=args.end_date,
                framework_names=framework_names,
                study_name=args.study_name,
                output_dir=args.output_dir
            )
            
            # Filter output files based on requested formats
            if 'all' not in requested_formats:
                filtered_files = {k: v for k, v in output_files.items() if k in requested_formats}
                output_files = filtered_files
            
            print("✅ Academic data export completed:")
            for format_name, file_path in output_files.items():
                print(f"   {format_name}: {file_path}")
        
        # Show usage suggestions
        print()
        print("📋 Next Steps:")
        
        if args.replication_package:
            print("1. Review the replication package contents")
            print("2. Test analysis scripts with your data")
            print("3. Customize documentation as needed")
            print("4. Share package for reproducibility")
        
        elif args.component_analysis:
            print("1. Load component data in your preferred analysis tool")
            print("2. Analyze component evolution and performance patterns")
            print("3. Generate development methodology documentation")
            
        else:
            print("1. Load data in your preferred analysis environment:")
            if 'csv' in output_files:
                print(f"   Python: pd.read_csv('{output_files['csv']}')")
            if 'feather' in output_files:
                print(f"   R: read_feather('{output_files['feather']}')")
            if 'stata' in output_files:
                print(f"   Stata: use \"{output_files['stata']}\", clear")
            
            print("2. Generate analysis templates:")
            print(f"   python generate_analysis_templates.py --study-name {args.study_name}")
            
            print("3. Create methodology documentation:")
            print(f"   python generate_documentation.py --study-name {args.study_name}")
        
        print()
        
    except Exception as e:
        print(f"❌ Error during export: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 