from pathlib import Path
from typing import Dict, Tuple
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