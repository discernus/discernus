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
        framework_def: Dict,
        scores: Dict,
        coordinates: Tuple[float, float],
        run_id: str
    ) -> str:
        """
        Generates an HTML visualization and returns the file path.
        """
        # Extract the anchors from the framework axes
        anchors = {}
        axes = framework_def.get("framework", {}).get("axes", {})
        for axis in axes.values():
            if 'integrative' in axis:
                anchors[axis['integrative']['name']] = axis['integrative']
            if 'disintegrative' in axis:
                anchors[axis['disintegrative']['name']] = axis['disintegrative']

        output_filename = self.output_dir / f"analysis_report_{run_id}.html"

        self.visualizer.plot(
            anchors=anchors,
            signature_scores=scores,
            output_html=str(output_filename),
            show=False # We don't want to pop up a browser window on the server
        )

        return str(output_filename) 