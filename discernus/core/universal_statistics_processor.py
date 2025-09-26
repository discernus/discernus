"""
Universal Statistics Processor

Framework-agnostic component that ingests score_extraction artifacts from any experiment
and produces comprehensive descriptive statistics without knowledge of experiment, framework, or corpus.

This implements Tier 1 processing: reliable, universal statistical calculations that are
identical regardless of the experimental context.
"""

import json
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional
import hashlib
from scipy import stats
from scipy.stats import pearsonr, spearmanr, ttest_ind, mannwhitneyu, f_oneway, kruskal
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import warnings

# Suppress pandas warnings for cleaner output
warnings.filterwarnings('ignore', category=pd.errors.PerformanceWarning)


class UniversalStatisticsProcessor:
    """
    Framework-agnostic statistical processor that works with any score_extraction artifacts.
    
    Key Design Principles:
    1. No knowledge of experiment, framework, or corpus structure
    2. Dynamically discovers data structure from artifacts
    3. Produces identical calculations regardless of context
    4. Creates CAS-addressable artifacts for downstream processing
    """
    
    def __init__(self):
        self.document_data = None
        self.dimension_data = None
        self.metadata = {}
    
    def process_artifacts(self, artifact_paths: List[Path]) -> Dict[str, Any]:
        """
        Process a list of score_extraction artifact files and return comprehensive statistics.
        
        Args:
            artifact_paths: List of paths to score_extraction_*.json files
            
        Returns:
            Dictionary containing all descriptive statistics and metadata
        """
        # Step 1: Ingest and parse all artifacts
        raw_data = self._ingest_artifacts(artifact_paths)
        
        # Step 2: Convert to structured DataFrames
        self.document_data, self.dimension_data = self._create_dataframes(raw_data)
        
        # Step 3: Generate comprehensive statistics
        statistics = self._generate_statistics()
        
        # Step 4: Add metadata for CAS addressing
        statistics['processing_metadata'] = {
            'processor_version': '1.0.0',
            'artifact_count': len(artifact_paths),
            'document_count': len(self.document_data) if self.document_data is not None else 0,
            'dimension_count': len(self.dimension_data) if self.dimension_data is not None else 0,
            'content_hash': self._generate_content_hash(statistics)
        }
        
        return statistics
    
    def _ingest_artifacts(self, artifact_paths: List[Path]) -> List[Dict[str, Any]]:
        """Ingest and parse score_extraction artifacts with robust JSON handling."""
        parsed_artifacts = []
        
        for path in artifact_paths:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    artifact_data = json.load(f)
                
                # Extract the embedded JSON from LLM response
                if 'score_extraction' in artifact_data:
                    raw_response = artifact_data['score_extraction']
                    
                    # Clean markdown formatting
                    if raw_response.startswith('```json\n'):
                        raw_response = raw_response[7:]
                    elif raw_response.startswith('```json'):
                        raw_response = raw_response[7:]
                    if raw_response.endswith('\n```'):
                        raw_response = raw_response[:-4]
                    elif raw_response.endswith('```'):
                        raw_response = raw_response[:-3]
                    
                    try:
                        scores_data = json.loads(raw_response)
                        
                        # Add metadata from artifact wrapper
                        parsed_artifact = {
                            'document_id': path.stem.replace('score_extraction_', ''),
                            'document_index': artifact_data.get('document_index'),
                            'dimensional_scores': scores_data.get('dimensional_scores', {}),
                            'derived_metrics': scores_data.get('derived_metrics', {}),
                            'timestamp': artifact_data.get('timestamp'),
                            'model_used': artifact_data.get('model_used')
                        }
                        parsed_artifacts.append(parsed_artifact)
                        
                    except json.JSONDecodeError as e:
                        print(f"Warning: Could not parse JSON from {path.name}: {e}")
                        continue
                        
            except Exception as e:
                print(f"Warning: Could not process {path.name}: {e}")
                continue
        
        return parsed_artifacts
    
    def _create_dataframes(self, raw_data: List[Dict[str, Any]]) -> Tuple[Optional[pd.DataFrame], Optional[pd.DataFrame]]:
        """Convert raw artifact data into structured DataFrames."""
        if not raw_data:
            return None, None
        
        # Document-level DataFrame (derived metrics)
        doc_rows = []
        dim_rows = []
        
        for artifact in raw_data:
            doc_id = artifact['document_id']
            
            # Document-level row with derived metrics
            if artifact['derived_metrics']:
                doc_row = {
                    'document_id': doc_id,
                    'document_index': artifact.get('document_index')
                }
                doc_row.update(artifact['derived_metrics'])
                doc_rows.append(doc_row)
            
            # Dimension-level rows
            for dim_name, dim_scores in artifact['dimensional_scores'].items():
                dim_row = {
                    'document_id': doc_id,
                    'document_index': artifact.get('document_index'),
                    'dimension': dim_name,
                    'raw_score': dim_scores.get('raw_score'),
                    'salience': dim_scores.get('salience'),
                    'confidence': dim_scores.get('confidence')
                }
                dim_rows.append(dim_row)
        
        document_df = pd.DataFrame(doc_rows) if doc_rows else None
        dimension_df = pd.DataFrame(dim_rows) if dim_rows else None
        
        return document_df, dimension_df
    
    def _generate_statistics(self) -> Dict[str, Any]:
        """Generate comprehensive descriptive statistics."""
        stats_dict = {}
        
        # Document-level statistics (derived metrics)
        if self.document_data is not None and not self.document_data.empty:
            stats_dict['document_level'] = self._analyze_document_data()
        
        # Dimension-level statistics
        if self.dimension_data is not None and not self.dimension_data.empty:
            stats_dict['dimension_level'] = self._analyze_dimension_data()
        
        # Cross-level analysis (if both exist)
        if (self.document_data is not None and not self.document_data.empty and 
            self.dimension_data is not None and not self.dimension_data.empty):
            stats_dict['cross_level'] = self._analyze_cross_level()
        
        # Semi-universal statistical tests
        stats_dict['semi_universal_tests'] = self._run_semi_universal_tests()
        
        return stats_dict
    
    def _analyze_document_data(self) -> Dict[str, Any]:
        """Analyze document-level derived metrics."""
        # Get numeric columns (exclude document_id, document_index)
        numeric_cols = self.document_data.select_dtypes(include=[np.number]).columns
        numeric_data = self.document_data[numeric_cols]
        
        if numeric_data.empty:
            return {'error': 'No numeric data found in document-level metrics'}
        
        analysis = {
            'sample_size': len(self.document_data),
            'metric_count': len(numeric_cols),
            'metric_names': list(numeric_cols),
            
            # Descriptive statistics
            'descriptives': {
                col: {
                    'mean': float(numeric_data[col].mean()),
                    'median': float(numeric_data[col].median()),
                    'std': float(numeric_data[col].std()),
                    'min': float(numeric_data[col].min()),
                    'max': float(numeric_data[col].max()),
                    'q25': float(numeric_data[col].quantile(0.25)),
                    'q75': float(numeric_data[col].quantile(0.75)),
                    'skewness': float(stats.skew(numeric_data[col])),
                    'kurtosis': float(stats.kurtosis(numeric_data[col]))
                } for col in numeric_cols
            },
            
            # Correlation matrix
            'correlations': self._safe_correlation_matrix(numeric_data),
            
            # Reliability analysis (Cronbach's alpha)
            'reliability': self._calculate_cronbach_alpha(numeric_data)
        }
        
        return analysis
    
    def _analyze_dimension_data(self) -> Dict[str, Any]:
        """Analyze dimension-level scores."""
        # Get numeric score columns
        score_cols = ['raw_score', 'salience', 'confidence']
        available_cols = [col for col in score_cols if col in self.dimension_data.columns]
        
        if not available_cols:
            return {'error': 'No numeric score columns found'}
        
        analysis = {
            'sample_size': len(self.dimension_data),
            'dimension_count': self.dimension_data['dimension'].nunique(),
            'document_count': self.dimension_data['document_id'].nunique(),
            'dimension_names': sorted(self.dimension_data['dimension'].unique().tolist()),
            'score_types': available_cols,
            
            # Overall descriptives across all dimensions
            'overall_descriptives': {
                col: {
                    'mean': float(self.dimension_data[col].mean()),
                    'median': float(self.dimension_data[col].median()),
                    'std': float(self.dimension_data[col].std()),
                    'min': float(self.dimension_data[col].min()),
                    'max': float(self.dimension_data[col].max()),
                    'skewness': float(stats.skew(self.dimension_data[col].dropna())),
                    'kurtosis': float(stats.kurtosis(self.dimension_data[col].dropna()))
                } for col in available_cols
            },
            
            # Per-dimension descriptives
            'by_dimension': self._analyze_by_dimension(available_cols),
            
            # Score type correlations
            'score_correlations': self._safe_correlation_matrix(self.dimension_data[available_cols])
        }
        
        return analysis
    
    def _analyze_by_dimension(self, score_cols: List[str]) -> Dict[str, Dict[str, Any]]:
        """Analyze statistics for each dimension separately."""
        by_dimension = {}
        
        for dimension in self.dimension_data['dimension'].unique():
            dim_data = self.dimension_data[self.dimension_data['dimension'] == dimension]
            
            by_dimension[dimension] = {
                'sample_size': len(dim_data),
                'descriptives': {
                    col: {
                        'mean': float(dim_data[col].mean()),
                        'median': float(dim_data[col].median()),
                        'std': float(dim_data[col].std()),
                        'min': float(dim_data[col].min()),
                        'max': float(dim_data[col].max())
                    } for col in score_cols if col in dim_data.columns
                }
            }
        
        return by_dimension
    
    def _analyze_cross_level(self) -> Dict[str, Any]:
        """Analyze relationships between document-level and dimension-level data."""
        # Calculate document-level aggregates from dimension data
        dim_aggregates = self.dimension_data.groupby('document_id').agg({
            'raw_score': ['mean', 'std', 'min', 'max'],
            'salience': ['mean', 'std', 'min', 'max'],
            'confidence': ['mean', 'std', 'min', 'max']
        }).round(6)
        
        # Flatten column names
        dim_aggregates.columns = [f"{col[1]}_{col[0]}" for col in dim_aggregates.columns]
        dim_aggregates = dim_aggregates.reset_index()
        
        # Merge with document-level data
        if 'document_id' in self.document_data.columns:
            merged = pd.merge(self.document_data, dim_aggregates, on='document_id', how='inner')
        else:
            return {'error': 'Cannot merge: document_id not found in document data'}
        
        # Get numeric columns for correlation
        numeric_cols = merged.select_dtypes(include=[np.number]).columns
        
        analysis = {
            'merged_sample_size': len(merged),
            'cross_correlations': self._safe_correlation_matrix(merged[numeric_cols]),
            'dimension_aggregates': {
                col: {
                    'mean': float(dim_aggregates[col].mean()),
                    'std': float(dim_aggregates[col].std())
                } for col in dim_aggregates.columns if col != 'document_id'
            }
        }
        
        return analysis
    
    def _safe_correlation_matrix(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Calculate correlation matrix with statistical validity checks."""
        try:
            if data.empty or len(data.columns) < 2:
                return {'error': 'Insufficient data for correlation analysis'}
            
            # Remove non-numeric columns
            numeric_data = data.select_dtypes(include=[np.number])
            
            if numeric_data.empty or len(numeric_data.columns) < 2:
                return {'error': 'No numeric columns for correlation'}
            
            # Check sample size for statistical validity
            sample_size = len(numeric_data)
            
            if sample_size < 3:
                return {
                    'error': f'Insufficient sample size for correlation analysis (N={sample_size})',
                    'sample_size': sample_size,
                    'minimum_required': 3,
                    'recommendation': 'Correlations require at least 3 data points to be statistically meaningful'
                }
            
            # Calculate Pearson correlations
            corr_matrix = numeric_data.corr()
            
            # Convert to nested dict for JSON serialization
            corr_dict = {}
            warnings = []
            
            for col1 in corr_matrix.columns:
                corr_dict[col1] = {}
                for col2 in corr_matrix.columns:
                    value = corr_matrix.loc[col1, col2]
                    if not pd.isna(value):
                        corr_dict[col1][col2] = float(value)
                        
                        # Check for perfect correlations with small samples
                        if abs(value) == 1.0 and sample_size < 5:
                            warnings.append(f'Perfect correlation (r={value:.3f}) between {col1} and {col2} with small sample (N={sample_size})')
                    else:
                        corr_dict[col1][col2] = None
            
            result = {
                'pearson_correlations': corr_dict,
                'matrix_size': f"{len(corr_matrix)}x{len(corr_matrix)}",
                'variable_count': len(corr_matrix.columns),
                'sample_size': sample_size,
                'statistical_validity': {
                    'valid': sample_size >= 3,
                    'recommended_minimum': 5,
                    'warnings': warnings if warnings else None
                }
            }
            
            # Add warning for small samples
            if sample_size < 5:
                result['statistical_validity']['warning'] = f'Small sample size (N={sample_size}) - correlations may be unreliable'
            
            return result
            
        except Exception as e:
            return {'error': f'Correlation calculation failed: {str(e)}'}
    
    def _calculate_cronbach_alpha(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Calculate Cronbach's alpha for reliability analysis with statistical validity checks."""
        try:
            if data.empty or len(data.columns) < 2:
                return {'error': 'Insufficient variables for reliability analysis'}
            
            # Remove any non-numeric data
            numeric_data = data.select_dtypes(include=[np.number])
            
            if len(numeric_data.columns) < 2:
                return {'error': 'Need at least 2 numeric variables for reliability'}
            
            # Check sample size for statistical validity
            sample_size = len(numeric_data)
            
            if sample_size < 3:
                return {
                    'error': f'Insufficient sample size for reliability analysis (N={sample_size})',
                    'sample_size': sample_size,
                    'minimum_required': 3,
                    'recommendation': 'Reliability analysis requires at least 3 data points to be statistically meaningful'
                }
            
            # Calculate Cronbach's alpha
            # α = (k / (k-1)) * (1 - (Σσ²ᵢ / σ²ₜ))
            k = len(numeric_data.columns)  # number of items
            item_variances = numeric_data.var(axis=0, ddof=1)  # variance of each item
            total_variance = numeric_data.sum(axis=1).var(ddof=1)  # variance of total scores
            
            alpha = (k / (k - 1)) * (1 - (item_variances.sum() / total_variance))
            
            result = {
                'cronbach_alpha': float(alpha),
                'item_count': k,
                'sample_size': sample_size,
                'interpretation': self._interpret_alpha(alpha),
                'statistical_validity': {
                    'valid': sample_size >= 3,
                    'recommended_minimum': 5
                }
            }
            
            # Add warning for small samples
            if sample_size < 5:
                result['statistical_validity']['warning'] = f'Small sample size (N={sample_size}) - reliability estimates may be unreliable'
            
            return result
            
        except Exception as e:
            return {'error': f'Reliability calculation failed: {str(e)}'}
    
    def _interpret_alpha(self, alpha: float) -> str:
        """Provide interpretation of Cronbach's alpha value."""
        if alpha >= 0.9:
            return 'Excellent reliability'
        elif alpha >= 0.8:
            return 'Good reliability'
        elif alpha >= 0.7:
            return 'Acceptable reliability'
        elif alpha >= 0.6:
            return 'Questionable reliability'
        else:
            return 'Poor reliability'
    
    def _run_semi_universal_tests(self) -> Dict[str, Any]:
        """Run semi-universal statistical tests that are commonly useful across experiments."""
        tests = {}
        
        # 1. Multivariate analysis (if we have document-level data)
        if self.document_data is not None and not self.document_data.empty:
            tests['multivariate_analysis'] = self._run_multivariate_tests()
        
        # 2. Distribution tests (always useful)
        tests['distribution_tests'] = self._run_distribution_tests()
        
        # 3. Outlier detection
        tests['outlier_detection'] = self._detect_outliers()
        
        # 4. Effect size calculations
        tests['effect_sizes'] = self._calculate_effect_sizes()
        
        # 5. Clustering analysis
        tests['clustering'] = self._run_clustering_analysis()
        
        return tests
    
    def _run_multivariate_tests(self) -> Dict[str, Any]:
        """Run multivariate statistical tests on document-level data."""
        try:
            numeric_data = self.document_data.select_dtypes(include=[np.number])
            if numeric_data.empty or len(numeric_data.columns) < 2:
                return {'error': 'Insufficient numeric data for multivariate analysis'}
            
            # Remove document_index if present (not a real metric)
            if 'document_index' in numeric_data.columns:
                numeric_data = numeric_data.drop('document_index', axis=1)
            
            if len(numeric_data.columns) < 2:
                return {'error': 'Need at least 2 metrics for multivariate analysis'}
            
            results = {}
            
            # Principal Component Analysis
            try:
                scaler = StandardScaler()
                scaled_data = scaler.fit_transform(numeric_data.fillna(0))
                
                pca = PCA()
                pca_result = pca.fit_transform(scaled_data)
                
                results['pca'] = {
                    'explained_variance_ratio': pca.explained_variance_ratio_.tolist(),
                    'cumulative_variance': np.cumsum(pca.explained_variance_ratio_).tolist(),
                    'n_components_90_percent': int(np.argmax(np.cumsum(pca.explained_variance_ratio_) >= 0.9) + 1),
                    'component_loadings': {
                        f'PC{i+1}': dict(zip(numeric_data.columns, pca.components_[i]))
                        for i in range(min(3, len(pca.components_)))  # First 3 components
                    }
                }
            except Exception as e:
                results['pca'] = {'error': f'PCA failed: {str(e)}'}
            
            return results
            
        except Exception as e:
            return {'error': f'Multivariate analysis failed: {str(e)}'}
    
    def _run_distribution_tests(self) -> Dict[str, Any]:
        """Test distributions of key variables."""
        tests = {}
        
        # Test document-level metrics
        if self.document_data is not None and not self.document_data.empty:
            numeric_cols = self.document_data.select_dtypes(include=[np.number]).columns
            tests['document_level'] = {}
            
            for col in numeric_cols:
                if col == 'document_index':
                    continue
                    
                data = self.document_data[col].dropna()
                if len(data) < 3:
                    continue
                
                try:
                    # Shapiro-Wilk test for normality
                    shapiro_stat, shapiro_p = stats.shapiro(data)
                    
                    tests['document_level'][col] = {
                        'normality_test': {
                            'shapiro_wilk_statistic': float(shapiro_stat),
                            'shapiro_wilk_p_value': float(shapiro_p),
                            'is_normal': shapiro_p > 0.05
                        }
                    }
                except Exception as e:
                    tests['document_level'][col] = {'error': str(e)}
        
        # Test dimension-level scores
        if self.dimension_data is not None and not self.dimension_data.empty:
            tests['dimension_level'] = {}
            score_cols = ['raw_score', 'salience', 'confidence']
            
            for col in score_cols:
                if col not in self.dimension_data.columns:
                    continue
                    
                data = self.dimension_data[col].dropna()
                if len(data) < 3:
                    continue
                
                try:
                    shapiro_stat, shapiro_p = stats.shapiro(data)
                    tests['dimension_level'][col] = {
                        'normality_test': {
                            'shapiro_wilk_statistic': float(shapiro_stat),
                            'shapiro_wilk_p_value': float(shapiro_p),
                            'is_normal': shapiro_p > 0.05
                        }
                    }
                except Exception as e:
                    tests['dimension_level'][col] = {'error': str(e)}
        
        return tests
    
    def _detect_outliers(self) -> Dict[str, Any]:
        """Detect outliers using multiple methods."""
        outliers = {}
        
        if self.document_data is not None and not self.document_data.empty:
            numeric_cols = self.document_data.select_dtypes(include=[np.number]).columns
            outliers['document_level'] = {}
            
            for col in numeric_cols:
                if col == 'document_index':
                    continue
                    
                data = self.document_data[col].dropna()
                if len(data) < 4:
                    continue
                
                try:
                    # IQR method
                    Q1 = data.quantile(0.25)
                    Q3 = data.quantile(0.75)
                    IQR = Q3 - Q1
                    lower_bound = Q1 - 1.5 * IQR
                    upper_bound = Q3 + 1.5 * IQR
                    
                    iqr_outliers = data[(data < lower_bound) | (data > upper_bound)]
                    
                    # Z-score method
                    z_scores = np.abs(stats.zscore(data))
                    z_outliers = data[z_scores > 2]
                    
                    outliers['document_level'][col] = {
                        'iqr_method': {
                            'outlier_count': len(iqr_outliers),
                            'outlier_percentage': float(len(iqr_outliers) / len(data) * 100),
                            'bounds': {'lower': float(lower_bound), 'upper': float(upper_bound)}
                        },
                        'zscore_method': {
                            'outlier_count': len(z_outliers),
                            'outlier_percentage': float(len(z_outliers) / len(data) * 100)
                        }
                    }
                except Exception as e:
                    outliers['document_level'][col] = {'error': str(e)}
        
        return outliers
    
    def _calculate_effect_sizes(self) -> Dict[str, Any]:
        """Calculate effect sizes for common comparisons."""
        effect_sizes = {}
        
        if self.document_data is not None and not self.document_data.empty:
            numeric_cols = self.document_data.select_dtypes(include=[np.number]).columns
            
            # Calculate Hedge's g effect sizes for all numeric variables
            effect_sizes['hedges_g_interpretations'] = {}
            
            for col in numeric_cols:
                if col == 'document_index':
                    continue
                    
                data = self.document_data[col].dropna()
                if len(data) < 2:
                    continue
                
                # Calculate effect size relative to theoretical midpoint (if scores are 0-1)
                if data.min() >= 0 and data.max() <= 1:
                    theoretical_midpoint = 0.5
                    cohens_d = (data.mean() - theoretical_midpoint) / data.std()
                    
                    # Calculate Hedge's g (corrected for small sample bias)
                    n = len(data)
                    df = n - 1
                    correction_factor = 1 - (3 / (4 * df - 1)) if df > 1 else 1
                    hedges_g = cohens_d * correction_factor
                    
                    # Interpret effect size using Hedge's g
                    if abs(hedges_g) < 0.2:
                        interpretation = 'negligible'
                    elif abs(hedges_g) < 0.5:
                        interpretation = 'small'
                    elif abs(hedges_g) < 0.8:
                        interpretation = 'medium'
                    else:
                        interpretation = 'large'
                    
                    effect_sizes['hedges_g_interpretations'][col] = {
                        'hedges_g': float(hedges_g),
                        'interpretation': interpretation,
                        'direction': 'above_midpoint' if hedges_g > 0 else 'below_midpoint',
                        'sample_size': n,
                        'bias_corrected': True,
                        'correction_factor': float(correction_factor)
                    }
        
        return effect_sizes
    
    def _run_clustering_analysis(self) -> Dict[str, Any]:
        """Run clustering analysis to identify document groups."""
        try:
            if self.document_data is None or self.document_data.empty:
                return {'error': 'No document data for clustering'}
            
            numeric_data = self.document_data.select_dtypes(include=[np.number])
            if 'document_index' in numeric_data.columns:
                numeric_data = numeric_data.drop('document_index', axis=1)
            
            if numeric_data.empty or len(numeric_data) < 3:
                return {'error': 'Insufficient data for clustering'}
            
            # Standardize the data
            scaler = StandardScaler()
            scaled_data = scaler.fit_transform(numeric_data.fillna(0))
            
            results = {}
            
            # Try different numbers of clusters
            max_clusters = min(len(numeric_data) - 1, 5)
            
            for n_clusters in range(2, max_clusters + 1):
                try:
                    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
                    cluster_labels = kmeans.fit_predict(scaled_data)
                    
                    # Calculate silhouette score would require sklearn.metrics
                    # For now, just store basic cluster info
                    results[f'{n_clusters}_clusters'] = {
                        'cluster_centers': kmeans.cluster_centers_.tolist(),
                        'inertia': float(kmeans.inertia_),
                        'cluster_sizes': [int(np.sum(cluster_labels == i)) for i in range(n_clusters)]
                    }
                except Exception as e:
                    results[f'{n_clusters}_clusters'] = {'error': str(e)}
            
            return results
            
        except Exception as e:
            return {'error': f'Clustering analysis failed: {str(e)}'}

    def _generate_content_hash(self, statistics: Dict[str, Any]) -> str:
        """Generate content hash for CAS addressing."""
        # Create a stable string representation for hashing
        content_str = json.dumps(statistics, sort_keys=True, default=str)
        return hashlib.sha256(content_str.encode()).hexdigest()[:12]


def process_score_extractions(artifact_directory: Path, output_path: Optional[Path] = None) -> Dict[str, Any]:
    """
    Convenience function to process all score_extraction artifacts in a directory.
    
    Args:
        artifact_directory: Path to directory containing score_extraction_*.json files
        output_path: Optional path to save the statistics JSON file
        
    Returns:
        Dictionary containing comprehensive statistics
    """
    # Find all score extraction artifacts
    artifact_paths = list(artifact_directory.glob("score_extraction_*.json"))
    
    if not artifact_paths:
        raise ValueError(f"No score_extraction_*.json files found in {artifact_directory}")
    
    # Process artifacts
    processor = UniversalStatisticsProcessor()
    statistics = processor.process_artifacts(artifact_paths)
    
    # Save to file if requested
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(statistics, f, indent=2, default=str)
        print(f"Statistics saved to {output_path}")
    
    return statistics


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python universal_statistics_processor.py <artifact_directory>")
        sys.exit(1)
    
    artifact_dir = Path(sys.argv[1])
    output_file = artifact_dir.parent / f"universal_statistics_{artifact_dir.name}.json"
    
    try:
        stats = process_score_extractions(artifact_dir, output_file)
        print(f"Processed {stats['processing_metadata']['artifact_count']} artifacts")
        print(f"Generated statistics for {stats['processing_metadata']['document_count']} documents")
        print(f"Content hash: {stats['processing_metadata']['content_hash']}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
