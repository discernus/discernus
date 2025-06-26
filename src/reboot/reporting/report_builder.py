from pathlib import Path
from typing import Dict, Tuple
from src.visualization.plotly_circular import PlotlyCircularVisualizer

class ReportBuilder:
    """
    Builds the visual report for an analysis.
    For the MVP, this is a thin wrapper around the existing PlotlyCircularVisualizer.
    """
    def __init__(self, output_dir: str = "reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.visualizer = PlotlyCircularVisualizer()

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
        # The plot method from the visualizer can recalculate coordinates,
        # but we pass them in if we already have them. For now, let's
        # just pass the scores and let it do its work.
        
        # Extract the wells from the framework definition
        wells = framework_def.get("wells", {})
        if not wells:
            dipoles = framework_def.get("dipoles", [])
            for dipole in dipoles:
                if 'positive' in dipole:
                    wells[dipole['positive']['name']] = dipole['positive']
                if 'negative' in dipole:
                    wells[dipole['negative']['name']] = dipole['negative']

        output_filename = self.output_dir / f"analysis_report_{run_id}.html"

        self.visualizer.plot(
            wells=wells,
            narrative_scores=scores,
            output_html=str(output_filename),
            show=False # We don't want to pop up a browser window on the server
        )

        return str(output_filename) 