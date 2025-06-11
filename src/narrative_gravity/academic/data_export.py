"""
Academic Data Export Pipeline

Converts experimental data from PostgreSQL into publication-ready formats
for statistical analysis in R, Stata, Python, and other academic tools.

Supports Elena's Week 3 workflow for academic tool integration.
"""

import json
import pandas as pd
import numpy as np
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
import zipfile
import tempfile
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text

from src.narrative_gravity.utils.database import get_database_url


class AcademicDataExporter:
    """
    Export experimental data in academic-standard formats.
    
    Supports Elena's statistical analysis workflow with proper
    variable naming, data dictionaries, and metadata preservation.
    """
    
    def __init__(self, database_url: Optional[str] = None):
        """Initialize exporter with database connection."""
        self.database_url = database_url or get_database_url()
        self.engine = create_engine(self.database_url)
        self.Session = sessionmaker(bind=self.engine)
    
    def export_experiments_data(self, 
                               start_date: Optional[str] = None,
                               end_date: Optional[str] = None,
                               framework_names: Optional[List[str]] = None,
                               study_name: Optional[str] = None,
                               output_dir: str = "exports/academic_formats") -> Dict[str, str]:
        """
        Export comprehensive experimental data for academic analysis.
        
        Args:
            start_date: ISO date string for filtering (e.g., '2025-06-01')
            end_date: ISO date string for filtering
            framework_names: List of framework names to include
            study_name: Study identifier for output naming
            output_dir: Directory for output files
            
        Returns:
            Dict mapping format names to output file paths
        """
        # Generate study identifier
        if not study_name:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            study_name = f"narrative_gravity_study_{timestamp}"
        
        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Build comprehensive query
        query = self._build_comprehensive_query(start_date, end_date, framework_names)
        
        # Execute query and get data
        with self.Session() as session:
            df = pd.read_sql(query, session.bind)
        
        # Clean and standardize data for academic analysis
        df_clean = self._prepare_academic_dataframe(df)
        
        # Generate data dictionary
        data_dict = self._generate_data_dictionary(df_clean)
        
        # Export in multiple formats
        output_files = {}
        
        # 1. CSV (universal compatibility)
        csv_path = output_path / f"{study_name}.csv"
        df_clean.to_csv(csv_path, index=False)
        output_files['csv'] = str(csv_path)
        
        # 2. Feather (R-optimized)
        feather_path = output_path / f"{study_name}.feather"
        df_clean.to_feather(feather_path)
        output_files['feather'] = str(feather_path)
        
        # 3. Stata DTA (if pyreadstat available)
        try:
            import pyreadstat
            dta_path = output_path / f"{study_name}.dta"
            pyreadstat.write_dta(df_clean, str(dta_path), 
                               variable_labels=data_dict['variable_labels'])
            output_files['stata'] = str(dta_path)
        except ImportError:
            print("⚠️  pyreadstat not available - skipping Stata .dta export")
        
        # 4. JSON (Python-optimized with metadata)
        json_path = output_path / f"{study_name}.json"
        export_data = {
            'metadata': {
                'study_name': study_name,
                'export_date': datetime.now().isoformat(),
                'record_count': len(df_clean),
                'date_range': {
                    'start': start_date,
                    'end': end_date
                },
                'frameworks_included': framework_names,
                'data_dictionary': data_dict
            },
            'data': df_clean.to_dict('records')
        }
        
        with open(json_path, 'w') as f:
            json.dump(export_data, f, indent=2, default=str)
        output_files['json'] = str(json_path)
        
        # 5. Data dictionary (separate file)
        dict_path = output_path / f"{study_name}_data_dictionary.json"
        with open(dict_path, 'w') as f:
            json.dump(data_dict, f, indent=2)
        output_files['data_dictionary'] = str(dict_path)
        
        return output_files
    
    def export_component_analysis_data(self,
                                     component_type: str = "all",
                                     include_development_sessions: bool = True,
                                     output_dir: str = "exports/academic_formats") -> Dict[str, str]:
        """
        Export component development and performance data.
        
        Supports analysis of prompt engineering, framework development,
        and weighting methodology evolution for methodology papers.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        study_name = f"component_analysis_{component_type}_{timestamp}"
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Query component performance data
        component_query = self._build_component_query(component_type, include_development_sessions)
        
        with self.Session() as session:
            df = pd.read_sql(component_query, session.bind)
        
        # Process for academic analysis
        df_clean = self._prepare_component_dataframe(df)
        
        # Generate component-specific data dictionary
        data_dict = self._generate_component_dictionary(df_clean, component_type)
        
        # Export formats
        output_files = {}
        
        # CSV export
        csv_path = output_path / f"{study_name}.csv"
        df_clean.to_csv(csv_path, index=False)
        output_files['csv'] = str(csv_path)
        
        # JSON with metadata
        json_path = output_path / f"{study_name}.json"
        export_data = {
            'metadata': {
                'study_name': study_name,
                'component_type': component_type,
                'export_date': datetime.now().isoformat(),
                'record_count': len(df_clean),
                'includes_development_sessions': include_development_sessions,
                'data_dictionary': data_dict
            },
            'data': df_clean.to_dict('records')
        }
        
        with open(json_path, 'w') as f:
            json.dump(export_data, f, indent=2, default=str)
        output_files['json'] = str(json_path)
        
        return output_files
    
    def _build_comprehensive_query(self, start_date: Optional[str], 
                                 end_date: Optional[str], 
                                 framework_names: Optional[List[str]]) -> str:
        """Build comprehensive SQL query for experimental data."""
        
        base_query = """
        SELECT 
            -- Experiment identifiers
            e.id as experiment_id,
            e.name as experiment_name,
            e.created_at as experiment_date,
            e.description as experiment_description,
            
            -- Framework information
            f.name as framework_name,
            fv.version as framework_version,
            fv.dipoles_json,
            fv.framework_json,
            
            -- Prompt template information
            COALESCE(pt.name, 'legacy') as prompt_template_name,
            COALESCE(pt.version, 'v1.0') as prompt_template_version,
            COALESCE(pt.template_type, 'standard') as template_type,
            
            -- Weighting methodology information
            COALESCE(wm.name, 'linear') as weighting_method_name,
            COALESCE(wm.version, 'v1.0') as weighting_method_version,
            COALESCE(wm.algorithm_type, 'linear') as weighting_algorithm,
            
            -- Run results
            r.id as run_id,
            r.text_title,
            r.model_name,
            r.analysis_result,
            r.cost,
            r.processing_time,
            r.created_at as run_date,
            
            -- Calculated metrics
            r.coefficient_variation,
            r.icc_score,
            r.confidence_intervals,
            r.statistical_summary,
            
            -- Narrative positioning
            r.narrative_position,
            r.relative_position,
            r.framework_fit
            
        FROM experiments e
        JOIN frameworks f ON e.framework_id = f.id
        JOIN framework_versions fv ON e.framework_version_id = fv.id  
        JOIN runs r ON e.id = r.experiment_id
        LEFT JOIN prompt_templates pt ON e.prompt_template_id = pt.id
        LEFT JOIN weighting_methodologies wm ON e.weighting_method_id = wm.id
        """
        
        conditions = []
        if start_date:
            conditions.append(f"e.created_at >= '{start_date}'")
        if end_date:
            conditions.append(f"e.created_at <= '{end_date}'")
        if framework_names:
            framework_list = "', '".join(framework_names)
            conditions.append(f"f.name IN ('{framework_list}')")
        
        if conditions:
            base_query += " WHERE " + " AND ".join(conditions)
        
        base_query += " ORDER BY e.created_at DESC, r.created_at DESC"
        
        return base_query
    
    def _build_component_query(self, component_type: str, 
                             include_sessions: bool) -> str:
        """Build query for component development analysis."""
        
        if component_type == "prompt_template" or component_type == "all":
            query = """
            SELECT 
                'prompt_template' as component_type,
                pt.name as component_name,
                pt.version,
                pt.template_type,
                pt.created_at,
                pt.validation_status,
                pt.usage_count,
                pt.performance_metrics,
                pt.development_notes
            FROM prompt_templates pt
            """
        elif component_type == "framework" or component_type == "all":
            query = """
            SELECT 
                'framework' as component_type,
                fv.framework_name as component_name,
                fv.version,
                fv.theoretical_foundation,
                fv.created_at,
                fv.validation_status,
                fv.usage_count,
                fv.performance_metrics,
                fv.development_notes
            FROM framework_versions fv
            """
        else:
            # Default to all components union
            query = """
            SELECT * FROM (
                SELECT 
                    'prompt_template' as component_type,
                    pt.name as component_name,
                    pt.version,
                    pt.template_type as subtype,
                    pt.created_at,
                    pt.validation_status,
                    pt.usage_count,
                    pt.performance_metrics,
                    pt.development_notes
                FROM prompt_templates pt
                
                UNION ALL
                
                SELECT 
                    'framework' as component_type,
                    fv.framework_name as component_name,
                    fv.version,
                    'framework' as subtype,
                    fv.created_at,
                    fv.validation_status,
                    fv.usage_count,
                    fv.performance_metrics,
                    fv.development_notes
                FROM framework_versions fv
                
                UNION ALL
                
                SELECT 
                    'weighting_methodology' as component_type,
                    wm.name as component_name,
                    wm.version,
                    wm.algorithm_type as subtype,
                    wm.created_at,
                    wm.validation_status,
                    wm.usage_count,
                    wm.performance_metrics,
                    wm.implementation_notes as development_notes
                FROM weighting_methodologies wm
            ) component_data
            """
        
        query += " ORDER BY created_at DESC"
        return query
    
    def _prepare_academic_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Prepare dataframe for academic analysis with proper variable naming."""
        
        # Create academic-friendly variable names
        df_clean = df.copy()
        
        # Rename columns to academic standards (lowercase, underscores)
        column_mapping = {
            'experiment_id': 'exp_id',
            'experiment_name': 'exp_name', 
            'experiment_date': 'exp_date',
            'framework_name': 'framework',
            'framework_version': 'framework_ver',
            'prompt_template_name': 'prompt_template',
            'prompt_template_version': 'prompt_ver',
            'weighting_method_name': 'weighting_method',
            'weighting_method_version': 'weight_ver',
            'model_name': 'llm_model',
            'text_title': 'text_id',
            'coefficient_variation': 'cv',
            'icc_score': 'icc',
            'processing_time': 'process_time_sec',
            'run_date': 'analysis_date'
        }
        
        df_clean = df_clean.rename(columns=column_mapping)
        
        # Parse JSON fields into numeric columns
        if 'analysis_result' in df_clean.columns:
            df_clean = self._expand_analysis_results(df_clean)
        
        # Convert dates to proper datetime
        date_columns = ['exp_date', 'analysis_date']
        for col in date_columns:
            if col in df_clean.columns:
                df_clean[col] = pd.to_datetime(df_clean[col])
        
        # Create categorical variables
        categorical_columns = ['framework', 'prompt_template', 'weighting_method', 'llm_model']
        for col in categorical_columns:
            if col in df_clean.columns:
                df_clean[col] = df_clean[col].astype('category')
        
        # Handle missing values appropriately
        df_clean = df_clean.fillna({
            'cv': np.nan,
            'icc': np.nan,
            'cost': 0.0,
            'process_time_sec': 0.0
        })
        
        return df_clean
    
    def _prepare_component_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Prepare component development data for academic analysis."""
        
        df_clean = df.copy()
        
        # Convert dates
        if 'created_at' in df_clean.columns:
            df_clean['created_at'] = pd.to_datetime(df_clean['created_at'])
            df_clean['creation_date'] = df_clean['created_at'].dt.date
            df_clean['creation_week'] = df_clean['created_at'].dt.isocalendar().week
        
        # Parse performance metrics if present
        if 'performance_metrics' in df_clean.columns:
            df_clean = self._expand_performance_metrics(df_clean)
        
        # Create version numbering for analysis
        if 'version' in df_clean.columns:
            df_clean['version_major'] = df_clean['version'].str.extract(r'v?(\d+)').astype(float)
            df_clean['version_minor'] = df_clean['version'].str.extract(r'v?\d+\.(\d+)').astype(float)
        
        return df_clean
    
    def _expand_analysis_results(self, df: pd.DataFrame) -> pd.DataFrame:
        """Expand JSON analysis results into individual columns."""
        
        if 'analysis_result' not in df.columns:
            return df
        
        # Parse JSON analysis results
        analysis_data = []
        for idx, row in df.iterrows():
            try:
                if pd.notna(row['analysis_result']):
                    result = json.loads(row['analysis_result']) if isinstance(row['analysis_result'], str) else row['analysis_result']
                    
                    # Extract well scores
                    well_scores = {}
                    if isinstance(result, dict):
                        for key, value in result.items():
                            if isinstance(value, dict) and 'score' in value:
                                well_scores[f'well_{key}'] = value['score']
                            elif isinstance(value, (int, float)):
                                well_scores[f'well_{key}'] = value
                    
                    analysis_data.append(well_scores)
                else:
                    analysis_data.append({})
            except (json.JSONDecodeError, TypeError):
                analysis_data.append({})
        
        # Convert to DataFrame and merge
        if analysis_data:
            analysis_df = pd.DataFrame(analysis_data)
            df = pd.concat([df, analysis_df], axis=1)
        
        return df
    
    def _expand_performance_metrics(self, df: pd.DataFrame) -> pd.DataFrame:
        """Expand JSON performance metrics into individual columns."""
        
        if 'performance_metrics' not in df.columns:
            return df
        
        metrics_data = []
        for idx, row in df.iterrows():
            try:
                if pd.notna(row['performance_metrics']):
                    metrics = json.loads(row['performance_metrics']) if isinstance(row['performance_metrics'], str) else row['performance_metrics']
                    
                    if isinstance(metrics, dict):
                        # Flatten performance metrics
                        flattened = {}
                        for key, value in metrics.items():
                            if isinstance(value, (int, float)):
                                flattened[f'metric_{key}'] = value
                        metrics_data.append(flattened)
                    else:
                        metrics_data.append({})
                else:
                    metrics_data.append({})
            except (json.JSONDecodeError, TypeError):
                metrics_data.append({})
        
        # Convert to DataFrame and merge
        if metrics_data:
            metrics_df = pd.DataFrame(metrics_data)
            df = pd.concat([df, metrics_df], axis=1)
        
        return df
    
    def _generate_data_dictionary(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Generate comprehensive data dictionary for academic documentation."""
        
        data_dict = {
            'study_info': {
                'title': 'Narrative Gravity Wells Analysis Dataset',
                'description': 'Experimental data from LLM-based narrative analysis',
                'creation_date': datetime.now().isoformat(),
                'n_observations': len(df),
                'n_variables': len(df.columns)
            },
            'variables': {},
            'variable_labels': {},
            'value_labels': {}
        }
        
        # Define variable descriptions
        variable_descriptions = {
            'exp_id': 'Unique experiment identifier (UUID)',
            'exp_name': 'Descriptive name of experiment',
            'exp_date': 'Date experiment was created',
            'framework': 'Moral framework used for analysis',
            'framework_ver': 'Version of framework',
            'prompt_template': 'Prompt template used for LLM instruction',
            'prompt_ver': 'Version of prompt template',
            'weighting_method': 'Algorithm for score weighting',
            'weight_ver': 'Version of weighting methodology',
            'llm_model': 'Large language model used for analysis',
            'text_id': 'Identifier for analyzed text',
            'cv': 'Coefficient of variation (reliability measure)',
            'icc': 'Intraclass correlation coefficient',
            'cost': 'API cost for analysis (USD)',
            'process_time_sec': 'Processing time in seconds',
            'analysis_date': 'Date analysis was performed'
        }
        
        # Add well score descriptions
        well_columns = [col for col in df.columns if col.startswith('well_')]
        for col in well_columns:
            well_name = col.replace('well_', '').replace('_', ' ').title()
            variable_descriptions[col] = f'Score for {well_name} well (0.0-1.0)'
        
        # Generate variable info
        for col in df.columns:
            var_info = {
                'description': variable_descriptions.get(col, f'Variable: {col}'),
                'type': str(df[col].dtype),
                'missing_count': df[col].isna().sum(),
                'missing_percent': (df[col].isna().sum() / len(df)) * 100
            }
            
            # Add statistics for numeric variables
            if df[col].dtype in ['int64', 'float64']:
                var_info.update({
                    'min': float(df[col].min()) if df[col].notna().any() else None,
                    'max': float(df[col].max()) if df[col].notna().any() else None,
                    'mean': float(df[col].mean()) if df[col].notna().any() else None,
                    'std': float(df[col].std()) if df[col].notna().any() else None
                })
            
            # Add value counts for categorical variables
            elif df[col].dtype == 'category' or df[col].dtype == 'object':
                if df[col].notna().any():
                    value_counts = df[col].value_counts().to_dict()
                    var_info['value_counts'] = {str(k): int(v) for k, v in value_counts.items()}
            
            data_dict['variables'][col] = var_info
            data_dict['variable_labels'][col] = variable_descriptions.get(col, col)
        
        return data_dict
    
    def _generate_component_dictionary(self, df: pd.DataFrame, 
                                     component_type: str) -> Dict[str, Any]:
        """Generate data dictionary for component development data."""
        
        data_dict = {
            'study_info': {
                'title': f'Component Development Analysis: {component_type}',
                'description': 'Development tracking for narrative analysis components',
                'component_type': component_type,
                'creation_date': datetime.now().isoformat(),
                'n_observations': len(df),
                'n_variables': len(df.columns)
            },
            'variables': {},
            'variable_labels': {}
        }
        
        # Component-specific variable descriptions
        descriptions = {
            'component_type': 'Type of component (prompt_template, framework, weighting_methodology)',
            'component_name': 'Name of the component',
            'version': 'Version identifier',
            'subtype': 'Component subtype or algorithm type',
            'created_at': 'Date component was created',
            'validation_status': 'Current validation status',
            'usage_count': 'Number of times component has been used',
            'development_notes': 'Development process notes',
            'creation_date': 'Date of creation (date only)',
            'creation_week': 'ISO week number of creation',
            'version_major': 'Major version number',
            'version_minor': 'Minor version number'
        }
        
        # Generate variable information
        for col in df.columns:
            var_info = {
                'description': descriptions.get(col, f'Variable: {col}'),
                'type': str(df[col].dtype),
                'missing_count': df[col].isna().sum(),
                'missing_percent': (df[col].isna().sum() / len(df)) * 100
            }
            
            if df[col].dtype in ['int64', 'float64']:
                if df[col].notna().any():
                    var_info.update({
                        'min': float(df[col].min()),
                        'max': float(df[col].max()),
                        'mean': float(df[col].mean()),
                        'std': float(df[col].std())
                    })
            
            data_dict['variables'][col] = var_info
            data_dict['variable_labels'][col] = descriptions.get(col, col)
        
        return data_dict


class ReplicationPackageBuilder:
    """
    Generate comprehensive replication packages for academic publication.
    
    Supports Elena's Week 5 workflow for academic documentation and reproducibility.
    """
    
    def __init__(self, database_url: Optional[str] = None):
        """Initialize package builder."""
        self.database_url = database_url or get_database_url()
        self.exporter = AcademicDataExporter(database_url)
    
    def build_replication_package(self,
                                 study_name: str,
                                 study_description: str,
                                 data_filters: Optional[Dict] = None,
                                 include_code: bool = True,
                                 include_documentation: bool = True,
                                 output_path: str = "exports/replication_packages") -> str:
        """
        Build complete replication package for academic publication.
        
        Args:
            study_name: Name of the study for package identification
            study_description: Description for documentation
            data_filters: Filters for data export (start_date, end_date, frameworks)
            include_code: Include analysis code and templates
            include_documentation: Include methodology documentation
            output_path: Directory for output package
            
        Returns:
            Path to generated replication package ZIP file
        """
        
        # Create temporary directory for package assembly
        with tempfile.TemporaryDirectory() as temp_dir:
            package_dir = Path(temp_dir) / study_name
            package_dir.mkdir(parents=True)
            
            # 1. Export data in multiple formats
            print("📊 Exporting experimental data...")
            data_files = self.exporter.export_experiments_data(
                start_date=data_filters.get('start_date') if data_filters else None,
                end_date=data_filters.get('end_date') if data_filters else None,
                framework_names=data_filters.get('frameworks') if data_filters else None,
                study_name=study_name,
                output_dir=str(package_dir / "data")
            )
            
            # 2. Export component development data
            print("🔧 Exporting component development data...")
            component_files = self.exporter.export_component_analysis_data(
                output_dir=str(package_dir / "components")
            )
            
            # 3. Generate README
            print("📝 Generating documentation...")
            self._generate_readme(package_dir, study_name, study_description, data_files)
            
            # 4. Generate data documentation
            self._generate_data_documentation(package_dir, data_files)
            
            # 5. Include code templates if requested
            if include_code:
                print("💻 Including analysis code templates...")
                self._include_analysis_templates(package_dir)
            
            # 6. Include methodology documentation if requested
            if include_documentation:
                print("📋 Including methodology documentation...")
                self._include_methodology_docs(package_dir)
            
            # 7. Create ZIP package
            print("📦 Creating replication package...")
            output_dir = Path(output_path)
            output_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            zip_path = output_dir / f"{study_name}_replication_package_{timestamp}.zip"
            
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_path in package_dir.rglob('*'):
                    if file_path.is_file():
                        arcname = file_path.relative_to(package_dir)
                        zipf.write(file_path, arcname)
            
            print(f"✅ Replication package created: {zip_path}")
            return str(zip_path)
    
    def _generate_readme(self, package_dir: Path, study_name: str, 
                        description: str, data_files: Dict[str, str]):
        """Generate comprehensive README for replication package."""
        
        readme_content = f"""# {study_name} - Replication Package

## Study Description

{description}

## Package Contents

This replication package contains all data, code, and documentation necessary to reproduce the analysis results from this study.

### Data Files (`data/` directory)

- **{study_name}.csv** - Main dataset in CSV format (universal compatibility)
- **{study_name}.feather** - Dataset in Feather format (optimized for R/Python)
- **{study_name}.dta** - Dataset in Stata format (if available)
- **{study_name}.json** - Dataset with complete metadata (Python-optimized)
- **{study_name}_data_dictionary.json** - Complete variable documentation

### Component Development Data (`components/` directory)

- Component development tracking and performance metrics
- Version evolution and quality assessment data

### Analysis Code (`code/` directory)

- **jupyter_analysis.ipynb** - Jupyter notebook for statistical analysis
- **analysis.R** - R script for statistical modeling and visualization
- **analysis.do** - Stata script for publication-grade statistics
- **python_analysis.py** - Python script for data processing

### Documentation (`docs/` directory)

- **methodology.md** - Complete methodology description
- **variable_codebook.md** - Detailed variable descriptions
- **replication_instructions.md** - Step-by-step replication guide

## Quick Start

### Python/Jupyter
```python
import pandas as pd
data = pd.read_feather('data/{study_name}.feather')
# See jupyter_analysis.ipynb for complete analysis
```

### R
```r
library(arrow)
data <- read_feather('data/{study_name}.feather')
# See analysis.R for complete analysis
```

### Stata
```stata
use "data/{study_name}.dta", clear
// See analysis.do for complete analysis
```

## System Requirements

- Python 3.8+ with pandas, numpy, scipy, matplotlib, seaborn
- R 4.0+ with tidyverse, arrow, lme4, ggplot2
- Stata 16+ (optional)

## Replication Instructions

1. Load the dataset using your preferred tool (Python/R/Stata)
2. Follow the analysis scripts in the `code/` directory
3. Refer to `docs/methodology.md` for methodological details
4. Check `docs/variable_codebook.md` for variable definitions

## Contact Information

For questions about this replication package, please contact the research team.

## Data Collection Period

Data collected from experimental database spanning the analysis period defined in the study.

## Last Updated

{datetime.now().strftime("%B %d, %Y")}
"""
        
        readme_path = package_dir / "README.md"
        with open(readme_path, 'w') as f:
            f.write(readme_content)
    
    def _generate_data_documentation(self, package_dir: Path, data_files: Dict[str, str]):
        """Generate detailed data documentation."""
        
        docs_dir = package_dir / "docs"
        docs_dir.mkdir(exist_ok=True)
        
        # Variable codebook
        codebook_content = """# Variable Codebook

## Dataset Overview

This dataset contains experimental results from narrative analysis using Large Language Models (LLMs) with systematic moral framework application.

## Variable Descriptions

### Experimental Identifiers
- **exp_id**: Unique experiment identifier (UUID format)
- **exp_name**: Descriptive name assigned to experiment
- **exp_date**: Date when experiment was created (ISO format)

### Component Specifications
- **framework**: Name of moral framework used for analysis
- **framework_ver**: Version of framework (semantic versioning)
- **prompt_template**: Name of prompt template used for LLM instruction
- **prompt_ver**: Version of prompt template
- **weighting_method**: Algorithm used for score weighting and narrative positioning
- **weight_ver**: Version of weighting methodology

### Analysis Context
- **llm_model**: Large language model used for analysis (e.g., gpt-4o, claude-3.5-sonnet)
- **text_id**: Identifier for text that was analyzed
- **analysis_date**: Date when individual analysis was performed

### Performance Metrics
- **cv**: Coefficient of variation (measure of consistency across runs)
- **icc**: Intraclass correlation coefficient (reliability measure)
- **cost**: API cost for analysis in USD
- **process_time_sec**: Processing time in seconds

### Well Scores
Well scores represent the degree to which specific moral dimensions are present in the analyzed text.
All well scores range from 0.0 (completely absent) to 1.0 (strongly present).

- **well_[name]**: Score for specific moral dimension defined by framework

## Data Quality Notes

- Missing values in CV and ICC indicate single-run analyses
- Cost values may be $0.00 for cached or test analyses
- Well scores sum to varying totals depending on weighting methodology

## Statistical Considerations

- CV values < 0.20 indicate acceptable reliability
- ICC values > 0.75 indicate good inter-rater reliability
- Framework fit scores indicate how well the framework applies to specific texts
"""
        
        codebook_path = docs_dir / "variable_codebook.md"
        with open(codebook_path, 'w') as f:
            f.write(codebook_content)
    
    def _include_analysis_templates(self, package_dir: Path):
        """Include analysis code templates in multiple languages."""
        
        code_dir = package_dir / "code"
        code_dir.mkdir(exist_ok=True)
        
        # Python analysis template
        python_template = '''"""
Narrative Gravity Wells Analysis - Python Template

This script provides template analysis code for the experimental dataset.
Adapt as needed for your specific research questions.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import json

# Load data
print("Loading dataset...")
data = pd.read_feather('../data/[STUDY_NAME].feather')
print(f"Loaded {len(data)} observations with {len(data.columns)} variables")

# Basic descriptive statistics
print("\\nDescriptive Statistics:")
print(data.describe())

# Framework reliability analysis
print("\\nFramework Reliability Analysis:")
reliability_stats = data.groupby('framework')['cv'].agg(['mean', 'std', 'count'])
print(reliability_stats)

# Model comparison
print("\\nModel Performance Comparison:")
model_stats = data.groupby('llm_model')['cv'].agg(['mean', 'std'])
print(model_stats)

# Visualization
plt.figure(figsize=(12, 8))

# Reliability by framework
plt.subplot(2, 2, 1)
sns.boxplot(data=data, x='framework', y='cv')
plt.title('Reliability by Framework')
plt.xticks(rotation=45)

# Processing time by model
plt.subplot(2, 2, 2)
sns.boxplot(data=data, x='llm_model', y='process_time_sec')
plt.title('Processing Time by Model')
plt.xticks(rotation=45)

# Well scores distribution (example for first well)
well_columns = [col for col in data.columns if col.startswith('well_')]
if well_columns:
    plt.subplot(2, 2, 3)
    sns.histplot(data=data, x=well_columns[0], bins=20)
    plt.title(f'Distribution of {well_columns[0]}')

# Cost analysis
plt.subplot(2, 2, 4)
sns.scatterplot(data=data, x='process_time_sec', y='cost', hue='llm_model')
plt.title('Cost vs Processing Time')

plt.tight_layout()
plt.savefig('../output/exploratory_analysis.png', dpi=300, bbox_inches='tight')
plt.show()

print("\\nAnalysis complete! Check the output directory for visualizations.")
'''
        
        python_path = code_dir / "python_analysis.py"
        with open(python_path, 'w') as f:
            f.write(python_template)
        
        # R analysis template
        r_template = '''# Narrative Gravity Wells Analysis - R Template
# Statistical analysis and visualization for experimental dataset

library(tidyverse)
library(arrow)
library(lme4)
library(ggplot2)
library(corrplot)

# Load data
cat("Loading dataset...\\n")
data <- read_feather("../data/[STUDY_NAME].feather")
cat("Loaded", nrow(data), "observations with", ncol(data), "variables\\n")

# Basic descriptive statistics
cat("\\nDescriptive Statistics:\\n")
summary(data)

# Framework reliability analysis
cat("\\nFramework Reliability Analysis:\\n")
reliability_stats <- data %>%
  group_by(framework) %>%
  summarise(
    mean_cv = mean(cv, na.rm = TRUE),
    sd_cv = sd(cv, na.rm = TRUE),
    n = n(),
    .groups = 'drop'
  )
print(reliability_stats)

# Mixed-effects model for CV prediction
if ("cv" %in% names(data)) {
  cat("\\nMixed-effects model for reliability prediction:\\n")
  cv_model <- lmer(cv ~ framework + llm_model + (1|text_id), data = data)
  print(summary(cv_model))
}

# Visualization
cat("\\nGenerating visualizations...\\n")

# Reliability by framework
p1 <- ggplot(data, aes(x = framework, y = cv)) +
  geom_boxplot() +
  theme_minimal() +
  labs(title = "Reliability by Framework", y = "Coefficient of Variation") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

# Model performance comparison
p2 <- ggplot(data, aes(x = llm_model, y = cv, fill = llm_model)) +
  geom_violin() +
  theme_minimal() +
  labs(title = "Model Performance Comparison", y = "Coefficient of Variation") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

# Well scores correlation matrix
well_columns <- names(data)[grepl("^well_", names(data))]
if (length(well_columns) > 1) {
  well_correlations <- cor(data[well_columns], use = "complete.obs")
  
  png("../output/well_correlations.png", width = 800, height = 600)
  corrplot(well_correlations, method = "color", type = "upper", 
           order = "hclust", tl.cex = 0.8, tl.col = "black")
  dev.off()
}

# Save plots
ggsave("../output/reliability_by_framework.png", p1, width = 10, height = 6)
ggsave("../output/model_performance.png", p2, width = 10, height = 6)

cat("\\nAnalysis complete! Check the output directory for visualizations.\\n")
'''
        
        r_path = code_dir / "analysis.R"
        with open(r_path, 'w') as f:
            f.write(r_template)
        
        # Stata analysis template
        stata_template = '''* Narrative Gravity Wells Analysis - Stata Template
* Statistical analysis for experimental dataset

clear all
set more off

* Load data
use "../data/[STUDY_NAME].dta", clear

* Describe dataset
describe
summarize

* Framework reliability analysis
display "Framework Reliability Analysis:"
bysort framework: summarize cv

* Model performance by LLM
display "Model Performance by LLM:"
bysort llm_model: summarize cv

* Mixed-effects regression for CV prediction
display "Mixed-effects model for reliability:"
mixed cv i.framework i.llm_model || text_id:, reml

* Generate summary statistics table
estpost tabstat cv, by(framework) statistics(mean sd n) columns(statistics)
esttab using "../output/reliability_by_framework.tex", ///
    cells("mean(fmt(3)) sd(fmt(3)) count(fmt(0))") ///
    replace booktabs title("Reliability by Framework")

* Cost analysis
if !missing(cost) {
    regress cost process_time_sec i.llm_model
    estimates store cost_model
    
    esttab cost_model using "../output/cost_analysis.tex", ///
        replace booktabs title("Cost Analysis Model")
}

* Export dataset summary
estpost summarize
esttab using "../output/dataset_summary.tex", ///
    cells("mean(fmt(3)) sd(fmt(3)) min(fmt(3)) max(fmt(3)) count(fmt(0))") ///
    replace booktabs title("Dataset Summary Statistics")

display "Analysis complete! Check the output directory for results."
'''
        
        stata_path = code_dir / "analysis.do"
        with open(stata_path, 'w') as f:
            f.write(stata_template)
    
    def _include_methodology_docs(self, package_dir: Path):
        """Include methodology documentation."""
        
        docs_dir = package_dir / "docs"
        docs_dir.mkdir(exist_ok=True)
        
        methodology_content = """# Methodology Documentation

## Overview

This study employs Large Language Models (LLMs) for systematic narrative analysis using moral framework application. The methodology combines structured prompt engineering, framework versioning, and statistical validation to achieve reliable thematic assessment.

## Analytical Framework

### Component Architecture

The analysis system consists of three main components:

1. **Prompt Templates**: Structured instructions that guide LLM analysis
2. **Moral Frameworks**: Theoretical structures defining analytical dimensions  
3. **Weighting Methodologies**: Mathematical approaches for score integration

### Framework Application Process

1. **Text Preprocessing**: Standardization and formatting of narrative texts
2. **LLM Analysis**: Application of prompt templates with moral frameworks
3. **Score Extraction**: Structured extraction of dimensional scores
4. **Weighting Application**: Mathematical transformation using weighting methodology
5. **Statistical Validation**: Reliability assessment through multiple runs

## Quality Assurance

### Reliability Measures

- **Coefficient of Variation (CV)**: Consistency across multiple runs (target: <0.20)
- **Intraclass Correlation (ICC)**: Inter-rater reliability equivalent (target: >0.75)
- **Framework Fit**: Appropriateness assessment for specific texts

### Component Validation

Each component undergoes systematic quality assessment:
- Prompt templates validated for clarity and consistency
- Frameworks assessed for theoretical grounding and operational clarity
- Weighting methodologies tested for mathematical soundness

## Statistical Considerations

### Experimental Design

- Multiple runs per text-framework combination
- Cross-model validation using different LLMs
- Systematic component version tracking

### Data Analysis Approach

- Mixed-effects modeling for nested data structure
- Reliability analysis using variance decomposition
- Effect size calculation for practical significance

## Limitations and Assumptions

### LLM Limitations
- Analysis quality depends on model capabilities
- Potential bias in model training data
- Variability in model responses

### Framework Limitations  
- Domain-specific applicability
- Theoretical assumptions embedded in framework design
- Cultural and contextual considerations

## Replication Notes

For exact replication:
1. Use identical component versions as specified in dataset
2. Apply same LLM models with consistent parameters
3. Follow statistical analysis procedures in provided code
4. Consider temporal variations in LLM model performance

## References

[Include relevant academic references for theoretical frameworks and methodological approaches]
"""
        
        methodology_path = docs_dir / "methodology.md"
        with open(methodology_path, 'w') as f:
            f.write(methodology_content)


# Convenience functions for CLI integration
def export_academic_data(study_name: str, **kwargs) -> Dict[str, str]:
    """Quick export function for CLI tools."""
    exporter = AcademicDataExporter()
    return exporter.export_experiments_data(study_name=study_name, **kwargs)


def build_replication_package(study_name: str, description: str, **kwargs) -> str:
    """Quick replication package builder for CLI tools."""
    builder = ReplicationPackageBuilder()
    return builder.build_replication_package(study_name, description, **kwargs) 