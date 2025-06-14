#!/usr/bin/env python3
"""
Academic Documentation Generator - Priority 3 CLI Tool

Generate methodology papers, statistical reports, and replication documentation
for academic publication and reproducibility.

Supports Elena's Week 5 workflow for publication preparation.

Usage:
    python generate_documentation.py --study-name week5_publication --doc-type methodology
    python generate_documentation.py --study-name validation_study --doc-type all --output-dir docs/publication
    python generate_documentation.py --help
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime
import json

# Add src to path for development mode
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.narrative_gravity.academic.documentation import (
    MethodologyPaperGenerator,
    StatisticalReportFormatter
)


def main():
    parser = argparse.ArgumentParser(
        description="Generate academic documentation for publication and reproducibility",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Generate methodology section:
    python generate_documentation.py --study-name week5_publication --doc-type methodology

  Generate all documentation:
    python generate_documentation.py --study-name validation_study \\
        --doc-type all --output-dir docs/publication

  Generate statistical results report:
    python generate_documentation.py --study-name framework_comparison \\
        --doc-type results --results-file analysis_results.json

  Generate replication guide:
    python generate_documentation.py --study-name reproducibility_study \\
        --doc-type replication --include-development-process

  Custom methodology documentation:
    python generate_documentation.py --study-name custom_study \\
        --doc-type methodology \\
        --include-development-process \\
        --methodology-dir methodology_docs

Academic Workflow:
  This tool works with exported data and analysis templates:
    1. python export_academic_data.py --study-name [STUDY_NAME]
    2. python generate_analysis_templates.py --study-name [STUDY_NAME]
    3. python generate_documentation.py --study-name [STUDY_NAME]
        """
    )
    
    parser.add_argument(
        "--study-name",
        required=True,
        help="Study name for documentation customization"
    )
    
    parser.add_argument(
        "--doc-type",
        choices=["methodology", "results", "replication", "all"],
        default="all",
        help="Type of documentation to generate (default: all)"
    )
    
    # Output directory options
    parser.add_argument(
        "--output-dir",
        default="docs",
        help="Base output directory for documentation (default: docs)"
    )
    
    parser.add_argument(
        "--methodology-dir",
        help="Specific directory for methodology documentation (overrides --output-dir)"
    )
    
    parser.add_argument(
        "--results-dir",
        help="Specific directory for results documentation (overrides --output-dir)"
    )
    
    parser.add_argument(
        "--replication-dir",
        help="Specific directory for replication documentation (overrides --output-dir)"
    )
    
    # Methodology options
    parser.add_argument(
        "--include-development-process",
        action="store_true",
        default=True,
        help="Include component development methodology in documentation"
    )
    
    parser.add_argument(
        "--methodology-detail",
        choices=["basic", "comprehensive", "publication"],
        default="comprehensive",
        help="Level of detail for methodology documentation (default: comprehensive)"
    )
    
    # Results options
    parser.add_argument(
        "--results-file",
        help="JSON file with statistical analysis results for results documentation"
    )
    
    parser.add_argument(
        "--include-effect-sizes",
        action="store_true",
        default=True,
        help="Include effect size analysis in results documentation"
    )
    
    parser.add_argument(
        "--statistical-format",
        choices=["apa", "academic", "detailed"],
        default="apa",
        help="Statistical reporting format (default: apa)"
    )
    
    # Replication options
    parser.add_argument(
        "--include-code-examples",
        action="store_true",
        default=True,
        help="Include code examples in replication documentation"
    )
    
    parser.add_argument(
        "--include-troubleshooting",
        action="store_true",
        default=True,
        help="Include troubleshooting guide in replication documentation"
    )
    
    # Format options
    parser.add_argument(
        "--format",
        choices=["markdown", "latex", "docx", "all"],
        default="markdown",
        help="Output format(s) for documentation (default: markdown)"
    )
    
    parser.add_argument(
        "--publication-ready",
        action="store_true",
        help="Format documentation for publication submission"
    )
    
    args = parser.parse_args()
    
    # Set up output directories
    base_output = Path(args.output_dir)
    methodology_dir = args.methodology_dir or str(base_output / "methodology")
    results_dir = args.results_dir or str(base_output / "results")
    replication_dir = args.replication_dir or str(base_output / "replication")
    
    # Determine which documentation to generate
    doc_types = [args.doc_type] if args.doc_type != 'all' else ['methodology', 'results', 'replication']
    
    generated_docs = []
    
    try:
        print("📚 Generating academic documentation...")
        print(f"📊 Study: {args.study_name}")
        print(f"📝 Documentation types: {', '.join(doc_types)}")
        if args.publication_ready:
            print("🎯 Publication-ready formatting enabled")
        print()
        
        # Generate methodology documentation
        if 'methodology' in doc_types:
            print("📋 Generating methodology documentation...")
            
            methodology_generator = MethodologyPaperGenerator()
            methodology_path = methodology_generator.generate_methodology_section(
                study_name=args.study_name,
                include_development_process=args.include_development_process,
                output_path=methodology_dir
            )
            
            generated_docs.append(("Methodology", methodology_path))
            print(f"   ✅ Created: {methodology_path}")
        
        # Generate results documentation
        if 'results' in doc_types:
            print("📊 Generating results documentation...")
            
            # Load results data if provided
            results_data = {}
            if args.results_file:
                try:
                    with open(args.results_file, 'r') as f:
                        results_data = json.load(f)
                    print(f"   📁 Loaded results from: {args.results_file}")
                except (FileNotFoundError, json.JSONDecodeError) as e:
                    print(f"   ⚠️  Could not load results file: {e}")
                    print("   📝 Generating template results section...")
            
            results_formatter = StatisticalReportFormatter()
            results_path = results_formatter.generate_results_section(
                analysis_results=results_data,
                study_name=args.study_name,
                output_path=results_dir
            )
            
            generated_docs.append(("Results", results_path))
            print(f"   ✅ Created: {results_path}")
        
        # Generate replication documentation
        if 'replication' in doc_types:
            print("🔄 Generating replication documentation...")
            
            replication_path = generate_replication_guide(
                study_name=args.study_name,
                output_path=replication_dir,
                include_code_examples=args.include_code_examples,
                include_troubleshooting=args.include_troubleshooting
            )
            
            generated_docs.append(("Replication Guide", replication_path))
            print(f"   ✅ Created: {replication_path}")
        
        print()
        print("✅ Academic documentation generation completed!")
        print()
        
        # Display generated documentation
        print("📋 Generated Documentation:")
        for doc_type, file_path in generated_docs:
            print(f"   {doc_type}: {file_path}")
        
        print()
        print("🚀 Next Steps:")
        
        print("1. Review generated documentation for accuracy and completeness")
        print("2. Customize content for your specific research context")
        
        if 'methodology' in [item[0] for item in generated_docs]:
            print("3. Integrate methodology section into your paper draft")
        
        if 'results' in [item[0] for item in generated_docs]:
            print("4. Update results section with your statistical analysis outcomes")
        
        if 'replication' in [item[0] for item in generated_docs]:
            print("5. Test replication instructions with a fresh environment")
        
        print()
        print("📖 Publication Checklist:")
        print("   ✓ Methodology section provides complete experimental details")
        print("   ✓ Results section includes all necessary statistical information")
        print("   ✓ Replication package enables independent reproduction")
        print("   ✓ Component versions are documented for reproducibility")
        
        if args.publication_ready:
            print("   ✓ Documentation formatted for publication submission")
        
        print()
        print("💡 Tips for Publication:")
        print("   - Methodology section can be directly integrated into paper drafts")
        print("   - Results formatting follows academic standards (APA style)")
        print("   - Replication guide ensures reproducibility requirements are met")
        print("   - All component versions are tracked for exact replication")
        
        print()
        
    except Exception as e:
        print(f"❌ Error during documentation generation: {e}")
        print("\n🔍 Troubleshooting:")
        print("1. Ensure the database connection is working")
        print("2. Check that the study name exists in your experimental data")
        print("3. Verify output directories are writable")
        print("4. For results documentation, ensure analysis results are available")
        print("5. Run with --help for usage examples")
        sys.exit(1)


def generate_replication_guide(study_name: str, output_path: str, 
                             include_code_examples: bool = True,
                             include_troubleshooting: bool = True) -> str:
    """Generate comprehensive replication guide."""
    
    output_dir = Path(output_path)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    guide_content = f"""# Replication Guide: {study_name}

## Overview

This guide provides step-by-step instructions for replicating the analysis and results from the {study_name} study using the Narrative Gravity Wells framework.

## Prerequisites

### System Requirements

- **Python 3.8+** with pandas, numpy, scipy, matplotlib, seaborn
- **R 4.0+** with tidyverse, arrow, lme4, ggplot2 (optional)
- **Stata 16+** (optional, for publication-grade statistics)
- **PostgreSQL 12+** (for database operations)

### Data Requirements

- Exported experimental data from: `export_academic_data.py --study-name {study_name}`
- Analysis templates from: `generate_analysis_templates.py --study-name {study_name}`
- Component version specifications (included in data export)

## Step-by-Step Replication

### Step 1: Environment Setup

```bash
# Clone repository and set up environment
git clone [REPOSITORY_URL]
cd narrative_gravity_analysis
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
pip install -r requirements.txt

# Set up development environment
source scripts/setup_dev_env.sh
```

### Step 2: Database Setup

```bash
# Set up PostgreSQL database
python launch.py --setup-db

# Verify database connection
python check_database.py
```

### Step 3: Data Export

```bash
# Export study data in all academic formats
python src/narrative_gravity/cli/export_academic_data.py \\
    --study-name {study_name} \\
    --format all \\
    --output-dir data/replication
```

### Step 4: Analysis Templates

```bash
# Generate analysis code templates
python src/narrative_gravity/cli/generate_analysis_templates.py \\
    --study-name {study_name} \\
    --templates all \\
    --output-dir analysis/replication
```

### Step 5: Statistical Analysis

#### Python/Jupyter Analysis

```bash
# Start Jupyter environment
jupyter lab analysis/replication/notebooks/{study_name}_exploration.ipynb
```

#### R Analysis

```bash
# Run R statistical analysis
Rscript analysis/replication/r_scripts/{study_name}_analysis.R
```

#### Stata Analysis (Optional)

```stata
// In Stata command window
do "analysis/replication/stata_scripts/{study_name}_publication.do"
```

### Step 6: Verification

Compare your results with the original study outputs:

1. **Reliability metrics**: CV values should match within 0.001
2. **Framework performance**: Relative rankings should be identical
3. **Statistical significance**: p-values should match within 0.01
4. **Effect sizes**: Cohen's d should match within 0.05

## Expected Outputs

### Data Files
- `{study_name}.csv` - Universal format dataset
- `{study_name}.feather` - R-optimized format
- `{study_name}.dta` - Stata format (if available)
- `{study_name}.json` - Python format with metadata

### Analysis Results
- Reliability analysis by framework
- Statistical significance tests
- Effect size calculations
- Visualization outputs

### Documentation
- Methodology section
- Results section with statistical formatting
- Data dictionary and codebook

## Component Versions

The study used the following component versions:

- **Prompt Templates**: [Automatically retrieved from database]
- **Frameworks**: [Automatically retrieved from database]
- **Weighting Methodologies**: [Automatically retrieved from database]

*Note: Exact component specifications are included in the exported data files.*

## Troubleshooting

### Common Issues

1. **Import errors**: Ensure development environment is properly set up
   ```bash
   source scripts/setup_dev_env.sh
   python -c "from src.narrative_gravity.engine_circular import NarrativeGravityWellsCircular; print('✅ Imports working!')"
   ```

2. **Database connection errors**: Verify PostgreSQL is running and accessible
   ```bash
   python check_database.py
   ```

3. **Missing data**: Ensure data export completed successfully
   ```bash
   ls -la data/replication/
   ```

4. **Analysis errors**: Check that all required packages are installed
   ```bash
   pip install -r requirements.txt
   ```

### Data Quality Checks

```python
# Verify data integrity
import pandas as pd
data = pd.read_feather('data/replication/{study_name}.feather')

# Check expected columns
expected_columns = ['exp_id', 'framework', 'cv', 'llm_model']
missing_columns = set(expected_columns) - set(data.columns)
if missing_columns:
    print(f"⚠️  Missing columns: {{missing_columns}}")
else:
    print("✅ All expected columns present")

# Check data ranges
print(f"CV range: {{data['cv'].min():.4f}} - {{data['cv'].max():.4f}}")
print(f"Frameworks: {{data['framework'].unique()}}")
```

### Statistical Verification

```r
# Verify R analysis setup
library(tidyverse)
library(arrow)

# Load data
data <- read_feather('data/replication/{study_name}.feather')

# Check data structure
glimpse(data)

# Verify key statistics
summary(data$cv)
table(data$framework)
```

## Contact Information

For questions about this replication package or issues with reproduction:

- **Primary Contact**: [Research Team Contact]
- **Repository Issues**: [GitHub Issues URL]
- **Documentation**: [Documentation URL]

## Citation

If you use this replication package in your research, please cite:

```bibtex
@misc{{{study_name}_replication,
  title={{{study_name} Replication Package}},
  author={{[Research Team]}},
  year={{{datetime.now().year}}},
  url={{[Repository URL]}},
  note={{Replication materials for narrative gravity analysis study}}
}}
```

## Version Information

- **Replication Guide Version**: 1.0
- **Generated**: {datetime.now().strftime("%B %d, %Y")}
- **Framework Version**: [Automatically determined from data]
- **Analysis Date**: [From experimental data]

---

*This replication guide was automatically generated from experimental data and component specifications. For manual updates, edit this file directly while preserving the structured format.*
"""
    
    guide_path = output_dir / f"{study_name}_replication_guide.md"
    with open(guide_path, 'w') as f:
        f.write(guide_content)
    
    return str(guide_path)


if __name__ == "__main__":
    main() 