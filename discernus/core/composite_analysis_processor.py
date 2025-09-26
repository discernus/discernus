"""
Composite Analysis Statistical Processor

Extracts statistical data directly from composite_analysis artifacts, bypassing the need for
additional LLM calls to score_extraction and evidence_extraction. This eliminates transcription
entropy and reduces costs while providing richer, more structured data.

The composite analysis contains all the data we need:
- Dimensional scores (raw_score, salience, confidence) 
- Derived metrics (framework-calculated values)
- Evidence quotes (tied to specific dimensions)
- Framework metadata (name, version, confidence)
- Document metadata (names, IDs)
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


class CompositeAnalysisProcessor:
    """
    Statistical processor that works directly with composite_analysis artifacts.
    
    Advantages over score_extraction approach:
    1. No additional LLM calls needed (saves cost)
    2. No transcription entropy (more reliable)
    3. Richer data structure (evidence quotes, metadata)
    4. Single source of truth (composite analysis)
    5. Framework metadata included
    """
    
    def __init__(self):
        self.document_data = None
        self.dimension_data = None
        self.evidence_data = None
        self.framework_metadata = {}
    
    def process_composite_analyses(self, artifact_paths: List[Path]) -> Dict[str, Any]:
        """
        Process composite_analysis artifacts and return comprehensive statistics.
        
        Args:
            artifact_paths: List of paths to composite_analysis_*.json files
            
        Returns:
            Dictionary containing all statistical analysis and metadata
        """
        # Step 1: Ingest and parse all composite analyses
        raw_data = self._ingest_composite_analyses(artifact_paths)
        
        # Step 2: Convert to structured DataFrames
        self.document_data, self.dimension_data, self.evidence_data = self._create_dataframes(raw_data)
        
        # Step 3: Extract framework metadata
        self.framework_metadata = self._extract_framework_metadata(raw_data)
        
        # Step 4: Generate comprehensive statistics
        statistics = self._generate_statistics()
        
        # Step 5: Add processing metadata
        statistics['processing_metadata'] = {
            'processor_version': '1.0.0',
            'processor_type': 'composite_analysis',
            'artifact_count': len(artifact_paths),
            'document_count': len(self.document_data) if self.document_data is not None else 0,
            'dimension_count': len(self.dimension_data) if self.dimension_data is not None else 0,
            'evidence_count': len(self.evidence_data) if self.evidence_data is not None else 0,
            'framework_metadata': self.framework_metadata,
            'content_hash': self._generate_content_hash(statistics)
        }
        
        return statistics
    
    def _ingest_composite_analyses(self, artifact_paths: List[Path]) -> List[Dict[str, Any]]:
        """Ingest and parse composite_analysis artifacts."""
        parsed_data = []
        
        for path in artifact_paths:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    artifact_data = json.load(f)
                
                # Extract the embedded JSON from LLM response
                if 'raw_analysis_response' in artifact_data:
                    raw_response = artifact_data['raw_analysis_response']
                    
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
                        analysis_data = json.loads(raw_response)
                        
                        # Add metadata from artifact wrapper
                        parsed_artifact = {
                            'analysis_id': artifact_data.get('analysis_id'),
                            'model_used': artifact_data.get('model_used'),
                            'document_index': artifact_data.get('document_index'),
                            'timestamp': artifact_data.get('timestamp'),
                            'analysis_metadata': analysis_data.get('analysis_metadata', {}),
                            'document_analyses': analysis_data.get('document_analyses', [])
                        }
                        parsed_data.append(parsed_artifact)
                        
                    except json.JSONDecodeError as e:
                        print(f"Warning: Could not parse JSON from {path.name}: {e}")
                        continue
                        
            except Exception as e:
                print(f"Warning: Could not process {path.name}: {e}")
                continue
        
        return parsed_data
    
    def _create_dataframes(self, raw_data: List[Dict[str, Any]]) -> Tuple[Optional[pd.DataFrame], Optional[pd.DataFrame], Optional[pd.DataFrame]]:
        """Convert raw composite analysis data into structured DataFrames."""
        if not raw_data:
            return None, None, None
        
        doc_rows = []
        dim_rows = []
        evidence_rows = []
        
        for artifact in raw_data:
            for doc_analysis in artifact['document_analyses']:
                doc_id = doc_analysis.get('document_id', 'unknown')
                doc_name = doc_analysis.get('document_name', 'unknown')
                
                # Document-level row with derived metrics
                if 'derived_metrics' in doc_analysis and doc_analysis['derived_metrics']:
                    doc_row = {
                        'document_id': doc_id,
                        'document_name': doc_name,
                        'analysis_id': artifact.get('analysis_id'),
                        'model_used': artifact.get('model_used'),
                        'timestamp': artifact.get('timestamp')
                    }
                    doc_row.update(doc_analysis['derived_metrics'])
                    doc_rows.append(doc_row)
                
                # Dimension-level rows
                if 'dimensional_scores' in doc_analysis:
                    for dim_name, dim_scores in doc_analysis['dimensional_scores'].items():
                        dim_row = {
                            'document_id': doc_id,
                            'document_name': doc_name,
                            'dimension': dim_name,
                            'raw_score': dim_scores.get('raw_score'),
                            'salience': dim_scores.get('salience'),
                            'confidence': dim_scores.get('confidence'),
                            'analysis_id': artifact.get('analysis_id'),
                            'model_used': artifact.get('model_used'),
                            'timestamp': artifact.get('timestamp')
                        }
                        dim_rows.append(dim_row)
                
                # Evidence rows
                if 'evidence_quotes' in doc_analysis:
                    for dim_name, quotes in doc_analysis['evidence_quotes'].items():
                        if isinstance(quotes, list):
                            for quote in quotes:
                                if quote and quote.strip():
                                    evidence_row = {
                                        'document_id': doc_id,
                                        'document_name': doc_name,
                                        'dimension': dim_name,
                                        'evidence_quote': quote.strip(),
                                        'quote_length': len(quote.strip()),
                                        'analysis_id': artifact.get('analysis_id'),
                                        'model_used': artifact.get('model_used'),
                                        'timestamp': artifact.get('timestamp')
                                    }
                                    evidence_rows.append(evidence_row)
        
        document_df = pd.DataFrame(doc_rows) if doc_rows else None
        dimension_df = pd.DataFrame(dim_rows) if dim_rows else None
        evidence_df = pd.DataFrame(evidence_rows) if evidence_rows else None
        
        return document_df, dimension_df, evidence_df
    
    def _extract_framework_metadata(self, raw_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract framework metadata from composite analyses."""
        if not raw_data:
            return {}
        
        # Use the first artifact's metadata as representative
        first_artifact = raw_data[0]
        analysis_metadata = first_artifact.get('analysis_metadata', {})
        
        return {
            'framework_name': analysis_metadata.get('framework_name', 'unknown'),
            'framework_version': analysis_metadata.get('framework_version', 'unknown'),
            'analyst_confidence': analysis_metadata.get('analyst_confidence', 0.0),
            'analysis_notes': analysis_metadata.get('analysis_notes', ''),
            'internal_consistency_approach': analysis_metadata.get('internal_consistency_approach', ''),
            'derived_metrics_calculated': analysis_metadata.get('derived_metrics_calculated', False)
        }
    
    def _generate_statistics(self) -> Dict[str, Any]:
        """Generate comprehensive descriptive statistics."""
        stats_dict = {}
        
        # Document-level statistics (derived metrics)
        if self.document_data is not None and not self.document_data.empty:
            stats_dict['document_level'] = self._analyze_document_data()
        
        # Dimension-level statistics
        if self.dimension_data is not None and not self.dimension_data.empty:
            stats_dict['dimension_level'] = self._analyze_dimension_data()
        
        # Evidence-level statistics
        if self.evidence_data is not None and not self.evidence_data.empty:
            stats_dict['evidence_level'] = self._analyze_evidence_data()
        
        # Cross-level analysis (if both document and dimension data exist)
        if (self.document_data is not None and not self.document_data.empty and 
            self.dimension_data is not None and not self.dimension_data.empty):
            stats_dict['cross_level'] = self._analyze_cross_level()
        
        # Semi-universal statistical tests
        stats_dict['semi_universal_tests'] = self._run_semi_universal_tests()
        
        return stats_dict
    
    def _analyze_document_data(self) -> Dict[str, Any]:
        """Analyze document-level derived metrics."""
        # Get numeric columns (exclude metadata columns)
        metadata_cols = ['document_id', 'document_name', 'analysis_id', 'model_used', 'timestamp']
        numeric_cols = [col for col in self.document_data.columns 
                       if col not in metadata_cols and pd.api.types.is_numeric_dtype(self.document_data[col])]
        
        if not numeric_cols:
            return {'error': 'No numeric derived metrics found'}
        
        numeric_data = self.document_data[numeric_cols]
        
        analysis = {
            'sample_size': len(self.document_data),
            'metric_count': len(numeric_cols),
            'metric_names': numeric_cols,
            
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
    
    def _analyze_evidence_data(self) -> Dict[str, Any]:
        """Analyze evidence quotes and their characteristics."""
        if self.evidence_data is None or self.evidence_data.empty:
            return {'error': 'No evidence data available'}
        
        analysis = {
            'total_quotes': len(self.evidence_data),
            'unique_documents': self.evidence_data['document_id'].nunique(),
            'unique_dimensions': self.evidence_data['dimension'].nunique(),
            'quotes_per_document': float(len(self.evidence_data) / self.evidence_data['document_id'].nunique()),
            'quotes_per_dimension': float(len(self.evidence_data) / self.evidence_data['dimension'].nunique()),
            
            # Quote length statistics
            'quote_length_stats': {
                'mean': float(self.evidence_data['quote_length'].mean()),
                'median': float(self.evidence_data['quote_length'].median()),
                'std': float(self.evidence_data['quote_length'].std()),
                'min': int(self.evidence_data['quote_length'].min()),
                'max': int(self.evidence_data['quote_length'].max())
            },
            
            # Evidence distribution by dimension
            'evidence_by_dimension': self.evidence_data['dimension'].value_counts().to_dict(),
            
            # Evidence distribution by document
            'evidence_by_document': self.evidence_data['document_id'].value_counts().to_dict()
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
                    } for col in score_cols if col in dim_data.columns and pd.api.types.is_numeric_dtype(dim_data[col])
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
        
        # Get numeric columns for correlation (exclude metadata)
        metadata_cols = ['document_id', 'document_name', 'analysis_id', 'model_used', 'timestamp']
        numeric_cols = [col for col in merged.columns 
                       if col not in metadata_cols and pd.api.types.is_numeric_dtype(merged[col])]
        
        analysis = {
            'merged_sample_size': len(merged),
            'cross_correlations': self._safe_correlation_matrix(merged[numeric_cols]),
            'dimension_aggregates': {
                col: {
                    'mean': float(dim_aggregates[col].mean()),
                    'std': float(dim_aggregates[col].std())
                } for col in dim_aggregates.columns if col != 'document_id' and pd.api.types.is_numeric_dtype(dim_aggregates[col])
            }
        }
        
        return analysis
    
    # Include all the semi-universal test methods from the original processor
    def _run_semi_universal_tests(self) -> Dict[str, Any]:
        """Run semi-universal statistical tests."""
        tests = {}
        
        # 1. Multivariate analysis (if we have document-level data)
        if self.document_data is not None and not self.document_data.empty:
            tests['multivariate_analysis'] = self._run_multivariate_tests()
        
        # 2. Distribution tests
        tests['distribution_tests'] = self._run_distribution_tests()
        
        # 3. Outlier detection
        tests['outlier_detection'] = self._detect_outliers()
        
        # 4. Effect size calculations
        tests['effect_sizes'] = self._calculate_effect_sizes()
        
        # 5. Clustering analysis
        tests['clustering'] = self._run_clustering_analysis()
        
        return tests
    
    # Copy all the helper methods from UniversalStatisticsProcessor
    def _safe_correlation_matrix(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Calculate correlation matrix with error handling."""
        try:
            if data.empty or len(data.columns) < 2:
                return {'error': 'Insufficient data for correlation analysis'}
            
            # Remove non-numeric columns
            numeric_data = data.select_dtypes(include=[np.number])
            
            if numeric_data.empty or len(numeric_data.columns) < 2:
                return {'error': 'No numeric columns for correlation'}
            
            # Calculate Pearson correlations
            corr_matrix = numeric_data.corr()
            
            # Convert to nested dict for JSON serialization
            corr_dict = {}
            for col1 in corr_matrix.columns:
                corr_dict[col1] = {}
                for col2 in corr_matrix.columns:
                    value = corr_matrix.loc[col1, col2]
                    corr_dict[col1][col2] = float(value) if not pd.isna(value) else None
            
            return {
                'pearson_correlations': corr_dict,
                'matrix_size': f"{len(corr_matrix)}x{len(corr_matrix)}",
                'variable_count': len(corr_matrix.columns)
            }
            
        except Exception as e:
            return {'error': f'Correlation calculation failed: {str(e)}'}
    
    def _calculate_cronbach_alpha(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Calculate Cronbach's alpha for reliability analysis."""
        try:
            if data.empty or len(data.columns) < 2:
                return {'error': 'Insufficient variables for reliability analysis'}
            
            # Remove any non-numeric data
            numeric_data = data.select_dtypes(include=[np.number])
            
            if len(numeric_data.columns) < 2:
                return {'error': 'Need at least 2 numeric variables for reliability'}
            
            # Calculate Cronbach's alpha
            k = len(numeric_data.columns)
            item_variances = numeric_data.var(axis=0, ddof=1)
            total_variance = numeric_data.sum(axis=1).var(ddof=1)
            
            alpha = (k / (k - 1)) * (1 - (item_variances.sum() / total_variance))
            
            return {
                'cronbach_alpha': float(alpha),
                'item_count': k,
                'interpretation': self._interpret_alpha(alpha)
            }
            
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
    
    # Add all the other semi-universal test methods here (abbreviated for space)
    def _run_multivariate_tests(self) -> Dict[str, Any]:
        """Run multivariate statistical tests on document-level data."""
        try:
            metadata_cols = ['document_id', 'document_name', 'analysis_id', 'model_used', 'timestamp']
            numeric_cols = [col for col in self.document_data.columns 
                           if col not in metadata_cols and pd.api.types.is_numeric_dtype(self.document_data[col])]
            
            if len(numeric_cols) < 2:
                return {'error': 'Need at least 2 metrics for multivariate analysis'}
            
            numeric_data = self.document_data[numeric_cols]
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
                        f'PC{i+1}': dict(zip(numeric_cols, pca.components_[i]))
                        for i in range(min(3, len(pca.components_)))
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
            metadata_cols = ['document_id', 'document_name', 'analysis_id', 'model_used', 'timestamp']
            numeric_cols = [col for col in self.document_data.columns 
                           if col not in metadata_cols and pd.api.types.is_numeric_dtype(self.document_data[col])]
            tests['document_level'] = {}
            
            for col in numeric_cols:
                data = self.document_data[col].dropna()
                if len(data) < 3:
                    continue
                
                try:
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
        
        return tests
    
    def _detect_outliers(self) -> Dict[str, Any]:
        """Detect outliers using multiple methods."""
        outliers = {}
        
        if self.document_data is not None and not self.document_data.empty:
            metadata_cols = ['document_id', 'document_name', 'analysis_id', 'model_used', 'timestamp']
            numeric_cols = [col for col in self.document_data.columns 
                           if col not in metadata_cols and pd.api.types.is_numeric_dtype(self.document_data[col])]
            outliers['document_level'] = {}
            
            for col in numeric_cols:
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
            metadata_cols = ['document_id', 'document_name', 'analysis_id', 'model_used', 'timestamp']
            numeric_cols = [col for col in self.document_data.columns 
                           if col not in metadata_cols and pd.api.types.is_numeric_dtype(self.document_data[col])]
            
            effect_sizes['cohens_d_interpretations'] = {}
            
            for col in numeric_cols:
                data = self.document_data[col].dropna()
                if len(data) < 2:
                    continue
                
                # Calculate effect size relative to theoretical midpoint (if scores are 0-1)
                if data.min() >= 0 and data.max() <= 1:
                    theoretical_midpoint = 0.5
                    cohens_d = (data.mean() - theoretical_midpoint) / data.std()
                    
                    # Interpret Cohen's d
                    if abs(cohens_d) < 0.2:
                        interpretation = 'negligible'
                    elif abs(cohens_d) < 0.5:
                        interpretation = 'small'
                    elif abs(cohens_d) < 0.8:
                        interpretation = 'medium'
                    else:
                        interpretation = 'large'
                    
                    effect_sizes['cohens_d_interpretations'][col] = {
                        'cohens_d': float(cohens_d),
                        'interpretation': interpretation,
                        'direction': 'above_midpoint' if cohens_d > 0 else 'below_midpoint'
                    }
        
        return effect_sizes
    
    def _run_clustering_analysis(self) -> Dict[str, Any]:
        """Run clustering analysis to identify document groups."""
        try:
            if self.document_data is None or self.document_data.empty:
                return {'error': 'No document data for clustering'}
            
            metadata_cols = ['document_id', 'document_name', 'analysis_id', 'model_used', 'timestamp']
            numeric_cols = [col for col in self.document_data.columns 
                           if col not in metadata_cols and pd.api.types.is_numeric_dtype(self.document_data[col])]
            
            if len(numeric_cols) == 0 or len(self.document_data) < 3:
                return {'error': 'Insufficient data for clustering'}
            
            numeric_data = self.document_data[numeric_cols]
            
            # Standardize the data
            scaler = StandardScaler()
            scaled_data = scaler.fit_transform(numeric_data.fillna(0))
            
            results = {}
            max_clusters = min(len(numeric_data) - 1, 5)
            
            for n_clusters in range(2, max_clusters + 1):
                try:
                    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
                    cluster_labels = kmeans.fit_predict(scaled_data)
                    
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
        content_str = json.dumps(statistics, sort_keys=True, default=str)
        return hashlib.sha256(content_str.encode()).hexdigest()[:12]


def process_composite_analyses(artifact_directory: Path, output_path: Optional[Path] = None) -> Dict[str, Any]:
    """
    Convenience function to process all composite_analysis artifacts in a directory.
    
    Args:
        artifact_directory: Path to directory containing composite_analysis_*.json files
        output_path: Optional path to save the statistics JSON file
        
    Returns:
        Dictionary containing comprehensive statistics
    """
    # Find all composite analysis artifacts
    artifact_paths = list(artifact_directory.glob("composite_analysis_*.json"))
    
    if not artifact_paths:
        raise ValueError(f"No composite_analysis_*.json files found in {artifact_directory}")
    
    # Process artifacts
    processor = CompositeAnalysisProcessor()
    statistics = processor.process_composite_analyses(artifact_paths)
    
    # Save to file if requested
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(statistics, f, indent=2, default=str)
        print(f"Statistics saved to {output_path}")
    
    return statistics


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python composite_analysis_processor.py <artifact_directory>")
        sys.exit(1)
    
    artifact_dir = Path(sys.argv[1])
    output_file = artifact_dir.parent / f"composite_statistics_{artifact_dir.name}.json"
    
    try:
        stats = process_composite_analyses(artifact_dir, output_file)
        print(f"Processed {stats['processing_metadata']['artifact_count']} composite analyses")
        print(f"Generated statistics for {stats['processing_metadata']['document_count']} documents")
        print(f"Framework: {stats['processing_metadata']['framework_metadata']['framework_name']}")
        print(f"Content hash: {stats['processing_metadata']['content_hash']}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
