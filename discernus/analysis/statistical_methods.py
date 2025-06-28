import json
import numpy as np
from typing import List, Dict, Any
from ..database.models import AnalysisResultV2

# Placeholder for the actual AnalysisResultV2 model
# We'll need to import this properly once we integrate it.
class AnalysisResultV2:
    pass

class BaseAnalyzer:
    """Base class for all statistical analyzers."""
    def analyze(self, data: List[AnalysisResultV2]) -> Dict[str, Any]:
        raise NotImplementedError("Each analyzer must implement the 'analyze' method.")

class GeometricSimilarityAnalyzer(BaseAnalyzer):
    """Analyzes the geometric similarity (centroid distance) between results."""
    def analyze(self, data: List[AnalysisResultV2]) -> Dict[str, Any]:
        if len(data) < 2:
            return {
                "error": "Geometric similarity requires at least two data points.",
                "distances": [],
                "mean_distance": 0,
                "max_distance": 0,
                "variance": 0
            }

        distances = []
        points = np.array([[d.centroid_x, d.centroid_y] for d in data])
        
        # Calculate pairwise distances
        for i in range(len(points)):
            for j in range(i + 1, len(points)):
                distance = np.linalg.norm(points[i] - points[j])
                distances.append(distance)
        
        if not distances:
            return {
                "error": "Could not calculate any distances.",
                "distances": [],
                "mean_distance": 0,
                "max_distance": 0,
                "variance": 0
            }

        mean_distance = np.mean(distances)
        max_distance = np.max(distances)
        variance = np.var(distances)

        return {
            "distances": distances,
            "mean_distance": float(mean_distance),
            "max_distance": float(max_distance),
            "variance": float(variance)
        }

class DimensionalCorrelationAnalyzer(BaseAnalyzer):
    """Analyzes the dimensional correlation (score-based) between results."""
    def analyze(self, data: List[AnalysisResultV2]) -> Dict[str, Any]:
        if len(data) < 2:
            return {"error": "Dimensional correlation requires at least two data points."}

        # Step 1: Parse JSON scores and align them by dimension
        parsed_scores = []
        all_dimensions = set()
        for d in data:
            try:
                scores = json.loads(d.raw_scores)
                parsed_scores.append(scores)
                all_dimensions.update(scores.keys())
            except (json.JSONDecodeError, AttributeError):
                return {"error": f"Could not parse raw_scores for result {d.id}."}

        if not all_dimensions:
            return {"error": "No dimensions found in the provided data."}

        # Step 2: Create a matrix of scores (dimensions x models)
        # Models are columns, dimensions are rows. Default to NaN if a model is missing a dimension.
        score_matrix = []
        sorted_dims = sorted(list(all_dimensions))
        for dim in sorted_dims:
            row = [scores.get(dim, np.nan) for scores in parsed_scores]
            score_matrix.append(row)
        
        score_matrix = np.array(score_matrix, dtype=float)

        # Step 3: Calculate Pearson correlation matrix
        # The result is a model-vs-model correlation matrix
        with np.errstate(divide='ignore', invalid='ignore'):
            # np.corrcoef with rowvar=True (default) expects variables (dimensions) as rows
            # and observations (models) as columns. The output is a (models x models) matrix.
            correlation_matrix = np.corrcoef(score_matrix)

            # If the number of dimensions is 1, corrcoef returns a single float, not a matrix.
            # We need to handle this to avoid errors.
            if score_matrix.shape[0] == 1:
                # When there's only one dimension, the concept of correlation is tricky.
                # If that one row has no variance, it will result in NaN.
                # Let's treat no variance as perfect correlation (1.0)
                if np.all(np.isnan(correlation_matrix)):
                    num_models = score_matrix.shape[1]
                    correlation_matrix = np.ones((num_models, num_models))
                else: # It's a single value, make it a 2x2 matrix
                    correlation_matrix = np.array([[1.0, correlation_matrix], [correlation_matrix, 1.0]])

            # If variance is zero for any row, corrcoef returns NaN. For our purpose,
            # zero variance between two sets of scores means they are identical,
            # so their correlation should be 1.0. We will replace NaNs that arise
            # from zero variance with 1.0. Other NaNs (from missing data) should be 0.
            # A simpler approach that fits the use case is to replace all NaNs with 0,
            # but that fails the "identical input" case.
            # Let's manually compute and build the matrix to be explicit.
            
            num_models = score_matrix.shape[1]
            correlation_matrix = np.identity(num_models) # Diagonals are always 1

            for i in range(num_models):
                for j in range(i + 1, num_models):
                    col1 = score_matrix[:, i]
                    col2 = score_matrix[:, j]
                    
                    # Find common, non-NaN values
                    valid_indices = ~np.isnan(col1) & ~np.isnan(col2)
                    
                    if np.sum(valid_indices) < 2: # Need at least 2 points to correlate
                        corr = 0.0
                    else:
                        v_col1 = col1[valid_indices]
                        v_col2 = col2[valid_indices]
                        
                        # Check for zero variance
                        if np.all(v_col1 == v_col2):
                            corr = 1.0
                        else:
                            # Use np.corrcoef for just these two columns
                            c = np.corrcoef(v_col1, v_col2)
                            corr = c[0, 1] if not np.isnan(c[0, 1]) else 0.0

                    correlation_matrix[i, j] = correlation_matrix[j, i] = corr

        # Handle the case of a single model, where corrcoef might not work as expected
        if not isinstance(correlation_matrix, np.ndarray) or correlation_matrix.ndim < 2:
             correlation_matrix = np.array([[1.0]])

        return {
            "dimensions": sorted_dims,
            "correlation_matrix": correlation_matrix.tolist(),
            "model_count": len(data)
        }

class TemporalStabilityAnalyzer(BaseAnalyzer):
    """Analyzes the stability of results over time."""
    def analyze(self, data: List[AnalysisResultV2]) -> Dict[str, Any]:
        raise NotImplementedError("TemporalStabilityAnalyzer is not yet implemented.")

class FrameworkVarianceAnalyzer(BaseAnalyzer):
    """Analyzes the variance between different frameworks."""
    def analyze(self, data: List[AnalysisResultV2]) -> Dict[str, Any]:
        raise NotImplementedError("FrameworkVarianceAnalyzer is not yet implemented.")

class RunConsistencyAnalyzer(BaseAnalyzer):
    """Analyzes the consistency between multiple runs of the same experiment."""
    def analyze(self, data: List[AnalysisResultV2]) -> Dict[str, Any]:
        raise NotImplementedError("RunConsistencyAnalyzer is not yet implemented.")


class HypothesisTestingAnalyzer(BaseAnalyzer):
    """Performs statistical hypothesis testing between models."""
    def analyze(self, data: List[AnalysisResultV2]) -> Dict[str, Any]:
        # Group data by model for comparison
        model_groups = {}
        for result in data:
            model = result.model
            if model not in model_groups:
                model_groups[model] = []
            model_groups[model].append({
                "centroid": (result.centroid_x, result.centroid_y),
                "scores": json.loads(result.raw_scores) if result.raw_scores else {},
                "text_id": getattr(result, 'text_identifier', 'unknown')
            })
        
        # Import and use the API's hypothesis testing function
        from ..api.main import _perform_hypothesis_testing
        return _perform_hypothesis_testing(model_groups)


class EffectSizeAnalyzer(BaseAnalyzer):
    """Calculates effect sizes (Cohen's d) for model comparisons."""
    def analyze(self, data: List[AnalysisResultV2]) -> Dict[str, Any]:
        # Group data by model for comparison
        model_groups = {}
        for result in data:
            model = result.model
            if model not in model_groups:
                model_groups[model] = []
            model_groups[model].append({
                "centroid": (result.centroid_x, result.centroid_y),
                "scores": json.loads(result.raw_scores) if result.raw_scores else {},
                "text_id": getattr(result, 'text_identifier', 'unknown')
            })
        
        # Import and use the API's effect size calculation function
        from ..api.main import _calculate_effect_sizes
        return _calculate_effect_sizes(model_groups)


class ConfidenceIntervalsAnalyzer(BaseAnalyzer):
    """Calculates confidence intervals for model centroids."""
    def analyze(self, data: List[AnalysisResultV2]) -> Dict[str, Any]:
        # Group data by model for comparison  
        model_groups = {}
        for result in data:
            model = result.model
            if model not in model_groups:
                model_groups[model] = []
            model_groups[model].append({
                "centroid": (result.centroid_x, result.centroid_y),
                "scores": json.loads(result.raw_scores) if result.raw_scores else {},
                "text_id": getattr(result, 'text_identifier', 'unknown')
            })
        
        # Import and use the API's confidence interval calculation function
        from ..api.main import _calculate_confidence_intervals
        return _calculate_confidence_intervals(model_groups)


class StatisticalMethodRegistry:
    """
    Registry of statistical comparison methods.
    This allows adding new methods without changing core infrastructure.
    """
    
    methods = {
        "geometric_similarity": GeometricSimilarityAnalyzer,
        "dimensional_correlation": DimensionalCorrelationAnalyzer, 
        "temporal_stability": TemporalStabilityAnalyzer,
        "framework_variance": FrameworkVarianceAnalyzer,
        "run_consistency": RunConsistencyAnalyzer,
        "hypothesis_testing": HypothesisTestingAnalyzer,
        "effect_size_analysis": EffectSizeAnalyzer,
        "confidence_intervals": ConfidenceIntervalsAnalyzer
    }
    
    def get_analyzer(self, method_name: str) -> BaseAnalyzer:
        """
        Retrieves an analyzer instance from the registry.
        """
        analyzer_class = self.methods.get(method_name)
        if not analyzer_class:
            raise ValueError(f"Unknown statistical method: {method_name}")
        return analyzer_class()

    def analyze(self, method: str, data: List[AnalysisResultV2]) -> Dict[str, Any]:
        """
        Executes a specific statistical analysis method on the given data.
        """
        analyzer = self.get_analyzer(method)
        return analyzer.analyze(data)

# Example usage (will be removed later)
if __name__ == '__main__':
    registry = StatisticalMethodRegistry()
    try:
        analyzer = registry.get_analyzer("geometric_similarity")
        print(f"Successfully retrieved analyzer: {analyzer.__class__.__name__}")
        # result = registry.analyze("geometric_similarity", data=[])
        # print(f"Analysis result: {result}")
    except ValueError as e:
        print(e) 