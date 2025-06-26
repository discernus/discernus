from pathlib import Path
from typing import Dict, Tuple, List
from src.reboot.reporting.reboot_plotly_circular import RebootPlotlyCircularVisualizer

class ReportBuilder:
    """
    Builds the visual report for an analysis.
    Uses the rebooted, glossary-compliant visualizer.
    """
    def __init__(self, output_dir: str = "reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.visualizer = RebootPlotlyCircularVisualizer()

    def generate_report(
        self,
        anchors: Dict,
        scores: Dict,
        coordinates: Tuple[float, float],
        run_id: str
    ) -> str:
        """
        Generates an HTML visualization and returns the file path.
        """
        output_filename = self.output_dir / f"analysis_report_{run_id}.html"

        self.visualizer.plot(
            anchors=anchors,
            signature_scores=scores,
            centroid_coords=coordinates,
            output_html=str(output_filename),
            show=False
        )

        return str(output_filename)

    def generate_comparison_report(
        self,
        anchors: Dict,
        analysis_a: Dict, label_a: str,
        analysis_b: Dict, label_b: str,
        run_id: str
    ) -> str:
        """Generates a side-by-side HTML comparison report."""
        output_filename = self.output_dir / f"comparison_report_{run_id}.html"

        self.visualizer.plot_comparison(
            anchors=anchors,
            analysis_a=analysis_a,
            label_a=label_a,
            analysis_b=analysis_b,
            label_b=label_b,
            output_html=str(output_filename),
            show=False
        )
        return str(output_filename)

    def generate_group_report(self, anchors: Dict, signatures: List[Dict], group_label: str, run_id: str) -> str:
        """Generates a report for a group of signatures, plotting their centroid."""
        if not signatures:
            return "No signatures provided for group report."

        # Calculate the centroid for the group
        all_coords = [s['centroid'] for s in signatures if 'centroid' in s]
        if not all_coords:
            return "No valid centroids found in signatures."
            
        avg_x = sum(c[0] for c in all_coords) / len(all_coords)
        avg_y = sum(c[1] for c in all_coords) / len(all_coords)
        group_centroid = (avg_x, avg_y)
        
        # We need a way to plot just a single centroid with its anchors.
        # For now, let's reuse the main plot method. We can enhance it later.
        # The 'scores' are not strictly needed here if we pass the centroid coords.
        output_filename = self.output_dir / f"group_report_{group_label}_{run_id}.html"

        self.visualizer.plot(
            anchors=anchors,
            signature_scores={}, # No individual scores needed for a group plot
            centroid_coords=group_centroid,
            centroid_label=group_label,
            title=f"Group Centroid: {group_label}",
            output_html=str(output_filename),
            show=False
        )
        return str(output_filename)

    def generate_group_comparison_report(self, anchors: Dict, 
                                         group_a_signatures: List[Dict], label_a: str,
                                         group_b_signatures: List[Dict], label_b: str,
                                         run_id: str) -> str:
        """Generates a report comparing the centroids of two groups."""
        
        def _calculate_group_centroid(signatures: List[Dict]) -> Tuple[float, float]:
            if not signatures: return (0.0, 0.0)
            all_coords = [s['centroid'] for s in signatures if 'centroid' in s]
            if not all_coords: return (0.0, 0.0)
            avg_x = sum(c[0] for c in all_coords) / len(all_coords)
            avg_y = sum(c[1] for c in all_coords) / len(all_coords)
            return (avg_x, avg_y)

        centroid_a = _calculate_group_centroid(group_a_signatures)
        centroid_b = _calculate_group_centroid(group_b_signatures)

        output_filename = self.output_dir / f"group_comparison_{run_id}.html"

        self.visualizer.plot_group_comparison(
            anchors=anchors,
            centroid_a=centroid_a, label_a=label_a,
            centroid_b=centroid_b, label_b=label_b,
            title=f"Group Comparison: {label_a} vs. {label_b}",
            output_html=str(output_filename),
            show=False
        )
        return str(output_filename) 