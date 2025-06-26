from pathlib import Path
from typing import Dict, Tuple, List
import jinja2
from src.reboot.reporting.reboot_plotly_circular import RebootPlotlyCircularVisualizer
import uuid
from datetime import datetime

class ReportBuilder:
    """
    Builds the visual report for an analysis.
    Uses the rebooted, glossary-compliant visualizer.
    """
    def __init__(self, output_dir: str = "reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.visualizer = RebootPlotlyCircularVisualizer()
        template_dir = Path(__file__).parent / 'templates'
        self.env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))

    def _calculate_group_centroid(self, signatures: List[Dict]) -> Tuple[float, float]:
        if not signatures: return (0.0, 0.0)
        all_coords = [s['centroid'] for s in signatures if 'centroid' in s]
        if not all_coords: return (0.0, 0.0)
        avg_x = sum(c[0] for c in all_coords) / len(all_coords)
        avg_y = sum(c[1] for c in all_coords) / len(all_coords)
        return (avg_x, avg_y)

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
        anchors: Dict[str, Tuple[float, float]],
        analysis_a: Dict,
        label_a: str,
        analysis_b: Dict,
        label_b: str,
        run_id: str,
        distance: float
    ) -> str:
        """Generates a side-by-side HTML comparison report."""
        template = self.env.get_template('comparison_template.html')
        
        # This data structure is used for the scatter plot
        plot_data = [
            {'x': analysis_a['centroid'][0], 'y': analysis_a['centroid'][1], 'label': label_a},
            {'x': analysis_b['centroid'][0], 'y': analysis_b['centroid'][1], 'label': label_b}
        ]
        
        title = f"Comparison: {label_a} vs. {label_b}"
        plot_html = self._generate_comparison_plot(anchors, analysis_a, label_a, analysis_b, label_b, title)
        
        html_content = template.render(
            report_title=title,
            plot_html=plot_html,
            scores_a=analysis_a['scores'],
            scores_b=analysis_b['scores'],
            label_a=label_a,
            label_b=label_b,
            distance=f"{distance:.4f}" # Format for display
        )
        
        report_filename = f"comparison_report_{run_id}.html"
        report_path = self.output_dir / report_filename
        with open(report_path, 'w') as f:
            f.write(html_content)
            
        return str(report_path)

    def _generate_comparison_plot(self, anchors, analysis_a, label_a, analysis_b, label_b, title):
        # Create a temporary file for the plot to be saved to
        temp_plot_path = self.output_dir / f"temp_plot_{uuid.uuid4()}.html"
        
        self.visualizer.plot_comparison(
            anchors=anchors,
            analysis_a=analysis_a,
            label_a=label_a,
            analysis_b=analysis_b,
            label_b=label_b,
            title=title,
            output_html=str(temp_plot_path),
            show=False
        )
        
        # Read the generated plot and return it as an HTML string
        with open(temp_plot_path, 'r') as f:
            plot_html = f.read()
        
        # Clean up the temporary file
        temp_plot_path.unlink()
        
        return plot_html

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

    def _generate_group_comparison_plot(self, anchors,
                                        group_a_signatures, label_a,
                                        group_b_signatures, label_b,
                                        title):
        # Create a temporary file for the plot to be saved to
        temp_plot_path = self.output_dir / f"temp_plot_{uuid.uuid4()}.html"

        centroid_a = self._calculate_group_centroid(group_a_signatures)
        centroid_b = self._calculate_group_centroid(group_b_signatures)

        self.visualizer.plot_group_comparison(
            anchors=anchors,
            centroid_a=centroid_a, label_a=label_a, group_a_signatures=group_a_signatures,
            centroid_b=centroid_b, label_b=label_b, group_b_signatures=group_b_signatures,
            title=title,
            output_html=str(temp_plot_path),
            show=False
        )

        # Read the generated plot and return it as an HTML string
        with open(temp_plot_path, 'r') as f:
            plot_html = f.read()

        # Clean up the temporary file
        temp_plot_path.unlink()

        return plot_html

    def generate_group_comparison_report(self, anchors: Dict,
                                         group_a_signatures: List[Dict], label_a: str,
                                         group_b_signatures: List[Dict], label_b: str,
                                         run_id: str, distance: float) -> str:
        """Generates a report comparing the centroids of two groups."""

        template = self.env.get_template('group_comparison_template.html')
        title = f"Group Comparison: {label_a} vs. {label_b}"

        plot_html = self._generate_group_comparison_plot(
            anchors=anchors,
            group_a_signatures=group_a_signatures,
            label_a=label_a,
            group_b_signatures=group_b_signatures,
            label_b=label_b,
            title=title
        )

        html_content = template.render(
            report_title=title,
            plot_html=plot_html,
            label_a=label_a,
            label_b=label_b,
            distance=f"{distance:.4f}",  # Format for display
            generation_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

        report_filename = f"group_comparison_report_{run_id}.html"
        report_path = self.output_dir / report_filename
        with open(report_path, 'w') as f:
            f.write(html_content)

        return str(report_path) 