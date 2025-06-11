#!/usr/bin/env python3
"""
Analysis Template Generator - Priority 3 CLI Tool

Generate Cursor-assisted analysis code for academic research in multiple languages.
Creates Jupyter notebooks, R scripts, and Stata scripts for statistical analysis.

Supports Elena's Week 3 workflow for statistical analysis and visualization.

Usage:
    python generate_analysis_templates.py --study-name week3_validation --templates all
    python generate_analysis_templates.py --study-name framework_study --templates jupyter,r --output-dir analysis_code
    python generate_analysis_templates.py --help
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime

# Add src to path for development mode
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.narrative_gravity.academic.analysis_templates import (
    JupyterTemplateGenerator, 
    RScriptGenerator, 
    StataIntegration
)


def main():
    parser = argparse.ArgumentParser(
        description="Generate AI-powered analysis templates for academic research",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Generate all analysis templates:
    python generate_analysis_templates.py --study-name week3_validation --templates all

  Generate specific templates:
    python generate_analysis_templates.py --study-name framework_study \\
        --templates jupyter,r --output-dir analysis_code

  Generate Jupyter notebook only:
    python generate_analysis_templates.py --study-name validation_study \\
        --templates jupyter --notebook-type exploration

  Generate publication-ready Stata script:
    python generate_analysis_templates.py --study-name publication_study \\
        --templates stata --stata-type publication

  Custom output directories:
    python generate_analysis_templates.py --study-name custom_study \\
        --templates all \\
        --jupyter-dir notebooks \\
        --r-dir r_analysis \\
        --stata-dir stata_scripts

Academic Integration:
  These templates are designed to work with data exported using:
    python export_academic_data.py --study-name [STUDY_NAME]
        """
    )
    
    parser.add_argument(
        "--study-name",
        required=True,
        help="Study name for template customization and file naming"
    )
    
    parser.add_argument(
        "--templates",
        default="all",
        help="Templates to generate: jupyter, r, stata, all (default: all)"
    )
    
    # Jupyter options
    parser.add_argument(
        "--jupyter-dir",
        default="notebooks",
        help="Output directory for Jupyter notebooks (default: notebooks)"
    )
    
    parser.add_argument(
        "--notebook-type",
        choices=["exploration", "analysis", "visualization", "publication"],
        default="exploration",
        help="Type of Jupyter notebook to generate (default: exploration)"
    )
    
    # R script options
    parser.add_argument(
        "--r-dir",
        default="r_scripts",
        help="Output directory for R scripts (default: r_scripts)"
    )
    
    parser.add_argument(
        "--r-type",
        choices=["statistical", "visualization", "mixed-effects", "publication"],
        default="statistical",
        help="Type of R script to generate (default: statistical)"
    )
    
    # Stata options
    parser.add_argument(
        "--stata-dir",
        default="stata_scripts", 
        help="Output directory for Stata scripts (default: stata_scripts)"
    )
    
    parser.add_argument(
        "--stata-type",
        choices=["analysis", "publication", "descriptive", "regression"],
        default="publication",
        help="Type of Stata script to generate (default: publication)"
    )
    
    # General options
    parser.add_argument(
        "--output-dir",
        help="Base output directory (overrides individual directory settings)"
    )
    
    parser.add_argument(
        "--data-path-prefix",
        default="../data",
        help="Relative path prefix to data files in generated code (default: ../data)"
    )
    
    parser.add_argument(
        "--include-visualization",
        action="store_true",
        default=True,
        help="Include visualization code in templates"
    )
    
    parser.add_argument(
        "--include-model-validation",
        action="store_true",
        default=True,
        help="Include model validation and diagnostics code"
    )
    
    parser.add_argument(
        "--academic-style",
        action="store_true",
        default=True,
        help="Generate academic-style code with publication formatting"
    )
    
    args = parser.parse_args()
    
    # Determine which templates to generate
    requested_templates = args.templates.split(',') if args.templates != 'all' else ['jupyter', 'r', 'stata']
    
    # Set up output directories
    if args.output_dir:
        jupyter_dir = str(Path(args.output_dir) / "notebooks")
        r_dir = str(Path(args.output_dir) / "r_scripts")
        stata_dir = str(Path(args.output_dir) / "stata_scripts")
    else:
        jupyter_dir = args.jupyter_dir
        r_dir = args.r_dir
        stata_dir = args.stata_dir
    
    generated_files = []
    
    try:
        print("🎯 Generating AI-powered analysis templates...")
        print(f"📊 Study: {args.study_name}")
        print(f"🔧 Templates: {', '.join(requested_templates)}")
        print()
        
        # Generate Jupyter notebook
        if 'jupyter' in requested_templates or 'all' in requested_templates:
            print("📓 Generating Jupyter notebook template...")
            
            jupyter_generator = JupyterTemplateGenerator()
            
            if args.notebook_type == "exploration":
                notebook_path = jupyter_generator.generate_exploration_notebook(
                    study_name=args.study_name,
                    output_path=jupyter_dir
                )
            else:
                # For other notebook types, use the exploration template as base
                # In a full implementation, we'd have separate methods for each type
                notebook_path = jupyter_generator.generate_exploration_notebook(
                    study_name=args.study_name,
                    output_path=jupyter_dir
                )
            
            generated_files.append(("Jupyter Notebook", notebook_path))
            print(f"   ✅ Created: {notebook_path}")
        
        # Generate R script
        if 'r' in requested_templates or 'all' in requested_templates:
            print("📈 Generating R analysis script...")
            
            r_generator = RScriptGenerator()
            r_script_path = r_generator.generate_statistical_analysis(
                study_name=args.study_name,
                output_path=r_dir
            )
            
            generated_files.append(("R Script", r_script_path))
            print(f"   ✅ Created: {r_script_path}")
        
        # Generate Stata script
        if 'stata' in requested_templates or 'all' in requested_templates:
            print("📊 Generating Stata analysis script...")
            
            stata_integration = StataIntegration()
            stata_script_path = stata_integration.generate_publication_analysis(
                study_name=args.study_name,
                output_path=stata_dir
            )
            
            generated_files.append(("Stata Script", stata_script_path))
            print(f"   ✅ Created: {stata_script_path}")
        
        print()
        print("✅ Analysis template generation completed!")
        print()
        
        # Display generated files
        print("📋 Generated Templates:")
        for template_type, file_path in generated_files:
            print(f"   {template_type}: {file_path}")
        
        print()
        print("🚀 Next Steps:")
        
        # Data preparation reminder
        print("1. Ensure your data is exported in the correct format:")
        print(f"   python export_academic_data.py --study-name {args.study_name} --format all")
        
        print()
        print("2. Start your analysis in your preferred environment:")
        
        if any("Jupyter" in item[0] for item in generated_files):
            jupyter_file = next(item[1] for item in generated_files if "Jupyter" in item[0])
            print(f"   Jupyter: jupyter lab {jupyter_file}")
        
        if any("R Script" in item[0] for item in generated_files):
            r_file = next(item[1] for item in generated_files if "R Script" in item[0])
            print(f"   R: Rscript {r_file}")
        
        if any("Stata" in item[0] for item in generated_files):
            stata_file = next(item[1] for item in generated_files if "Stata" in item[0])
            print(f"   Stata: stata-se do {stata_file}")
        
        print()
        print("3. Customize the generated code for your specific research questions")
        print("4. Generate methodology documentation:")
        print(f"   python generate_documentation.py --study-name {args.study_name}")
        
        print()
        print("💡 Tips:")
        print("   - All templates include comprehensive comments and documentation")
        print("   - Visualization code uses publication-ready styling")
        print("   - Statistical models follow academic best practices")
        print("   - Code is designed for reproducible research")
        
        if args.academic_style:
            print("   - Academic-style formatting enabled for publication")
        
        print()
        
    except Exception as e:
        print(f"❌ Error during template generation: {e}")
        print("\n🔍 Troubleshooting:")
        print("1. Ensure the database connection is working")
        print("2. Check that the study name exists in your experimental data")
        print("3. Verify output directories are writable")
        print("4. Run with --help for usage examples")
        sys.exit(1)


if __name__ == "__main__":
    main() 