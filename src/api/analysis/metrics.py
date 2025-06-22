from typing import Dict, Any, List
import math


def generate_hierarchical_ranking(raw_scores: Dict[str, float]) -> Dict[str, Any]:
    """Generate hierarchical ranking from well scores."""
    sorted_wells = sorted(raw_scores.items(), key=lambda x: x[1], reverse=True)
    top_3_scores = [score for _, score in sorted_wells[:3]]
    total_top_3 = sum(top_3_scores)

    if total_top_3 > 0:
        weights = [score / total_top_3 * 100 for score in top_3_scores]
    else:
        weights = [33.3, 33.3, 33.3]

    primary_wells = []
    for i, (well, score) in enumerate(sorted_wells[:3]):
        primary_wells.append({
            "well": well,
            "score": round(score, 3),
            "relative_weight": round(weights[i], 1),
        })

    return {
        "primary_wells": primary_wells,
        "secondary_wells": [],
        "total_weight": 100.0,
    }


def calculate_circular_metrics(x: float, y: float, raw_scores: Dict[str, float]) -> Dict[str, float]:
    """Calculate metrics compatible with circular coordinate system."""
    radius = math.sqrt(x * x + y * y)
    angle = math.atan2(y, x) if x != 0 or y != 0 else 0

    scores = list(raw_scores.values())
    positive_scores = [s for s in scores if s > 0.5]
    negative_scores = [s for s in scores if s <= 0.5]

    metrics = {
        "narrative_elevation": radius,
        "polarity": (sum(positive_scores) - sum(negative_scores)) / len(scores) if scores else 0.0,
        "coherence": 1.0 - (max(scores) - min(scores)) if scores else 0.8,
        "directional_purity": abs(math.cos(angle)) + abs(math.sin(angle)),
    }

    return metrics
