import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
import json
import csv
from typing import Dict, List, Optional, Union, Tuple
from datetime import datetime
from pathlib import Path
from scipy import stats


class RebootPlotlyCircularVisualizer:
    """
    Glossary-Compliant visualizer for circular coordinate system maps.
    Refactored to use 'anchor', 'axis', 'signature', and 'centroid' terminology.
    """

    def __init__(self, circle_radius=1.0, type_to_color=None, figure_size=900):
        self.circle_radius = circle_radius
        self.type_to_color = type_to_color or {"integrative": "#2E7D32", "disintegrative": "#C62828"}
        self.figure_size = figure_size
        self.fallback_palette = px.colors.qualitative.Plotly

        self.style = {
            "font_family": "Arial",
            "title_size": 16,
            "subtitle_size": 12,
            "axis_title_size": 12,
            "label_size": 10,
            "anchor_marker_size": 18,
            "centroid_marker_size": 28,
            "grid_color": "lightgray",
            "grid_width": 1,
            "boundary_color": "black",
            "boundary_width": 2,
        }

    def get_anchor_type_color(self, anchor_type: str, idx: int) -> str:
        """Get color for an anchor type, using config or fallback palette."""
        if anchor_type in self.type_to_color:
            return self.type_to_color[anchor_type]
        return self.fallback_palette[idx % len(self.fallback_palette)]

    def create_base_figure(self, title: str = None) -> go.Figure:
        """Create base figure with circle boundary and styling."""
        fig = go.Figure()

        # Draw unit circle
        theta = np.linspace(0, 2 * np.pi, 361)
        x_circle = self.circle_radius * np.cos(theta)
        y_circle = self.circle_radius * np.sin(theta)
        fig.add_trace(
            go.Scatter(
                x=x_circle,
                y=y_circle,
                mode="lines",
                line=dict(color=self.style["boundary_color"], width=self.style["boundary_width"]),
                name="Boundary",
                showlegend=False,
            )
        )

        # Add coordinate axes
        fig.add_hline(y=0, line_dash="dot", line_color=self.style["grid_color"], opacity=0.7)
        fig.add_vline(x=0, line_dash="dot", line_color=self.style["grid_color"], opacity=0.7)

        # Base layout with locked aspect ratio and responsive sizing
        fig.update_layout(
            # Remove hardcoded width/height for responsive design
            title=dict(
                text=title or "Discernus Coordinate System",
                font=dict(size=self.style["title_size"], family=self.style["font_family"]),
            ),
            xaxis=dict(
                visible=False,
                range=[-1.2, 1.2],
                scaleanchor="y",  # Lock aspect ratio to y-axis
                scaleratio=1,  # 1:1 ratio ensures circle stays circular
            ),
            yaxis=dict(
                visible=False,
                range=[-1.2, 1.2],
            ),
            plot_bgcolor="white",
            paper_bgcolor="white",
            showlegend=False,
            # Add responsive configuration
            autosize=True,
            margin=dict(l=20, r=20, t=60, b=20),
        )

        return fig

    def calculate_centroid(self, anchors: Dict, signature_scores: Dict) -> Tuple[float, float]:
        """Calculate the centroid position based on anchor scores in a signature."""
        weighted_x, weighted_y, total_weight = 0.0, 0.0, 0.0

        for anchor_name, score in signature_scores.items():
            if anchor_name in anchors:
                angle = anchors[anchor_name]["angle"]
                weight = abs(anchors[anchor_name].get("weight", 1.0))
                x = self.circle_radius * np.cos(np.deg2rad(angle))
                y = self.circle_radius * np.sin(np.deg2rad(angle))
                force = score * weight
                weighted_x += x * force
                weighted_y += y * force
                total_weight += force

        if total_weight > 0:
            return weighted_x / total_weight, weighted_y / total_weight
        return 0.0, 0.0

    def plot(
        self,
        anchors: Dict,
        signature_scores: Optional[Dict] = None,
        centroid_coords: Optional[Tuple[float, float]] = None,
        centroid_label: Optional[str] = None,
        title: Optional[str] = None,
        output_html: Optional[str] = None,
        output_png: Optional[str] = None,
        show: bool = True,
    ) -> go.Figure:
        """
        Create a complete circular visualization using the new glossary.

        Args:
            anchors: dict of {anchor_name: {'angle': deg, 'type': str, ...}}
            signature_scores: dict of {anchor_name: score} (the signature)
            centroid_coords: Optional pre-calculated (x, y) tuple for the centroid.
                             If provided, this will be used instead of recalculating.
            centroid_label: str (optional label for the centroid)
            title: str (optional)
            output_html: path to save interactive HTML (optional)
            output_png: path to save static PNG (optional, requires kaleido)
            show: whether to display the figure
        """
        fig = self.create_base_figure(title)

        # Plot anchors
        anchor_xs, anchor_ys, anchor_labels, anchor_colors = [], [], [], []
        for idx, (anchor_name, anchor) in enumerate(anchors.items()):
            angle = anchor["angle"]
            anchor_type = anchor.get("type", "default")
            x = self.circle_radius * np.cos(np.deg2rad(angle))
            y = self.circle_radius * np.sin(np.deg2rad(angle))
            color = self.get_anchor_type_color(anchor_type, idx)

            fig.add_trace(
                go.Scatter(
                    x=[0, x],
                    y=[0, y],
                    mode="lines",
                    line=dict(color=color, width=1, dash="dot"),
                    showlegend=False,
                    hoverinfo="skip",
                )
            )

            anchor_xs.append(x)
            anchor_ys.append(y)
            anchor_labels.append(f"{anchor_name} ({angle}°)")
            anchor_colors.append(color)

        fig.add_trace(
            go.Scatter(
                x=anchor_xs,
                y=anchor_ys,
                mode="markers+text",
                marker=dict(
                    size=self.style["anchor_marker_size"], color=anchor_colors, line=dict(width=2, color="black")
                ),
                text=anchor_labels,
                textposition="top center",
                name="Anchors",
                hovertemplate="<b>%{text}</b><extra></extra>",
            )
        )

        # Plot centroid if a signature or pre-calculated coords are provided
        if signature_scores or centroid_coords:
            if centroid_coords:
                centroid_x, centroid_y = centroid_coords
            else:
                centroid_x, centroid_y = self.calculate_centroid(anchors, signature_scores)

            fig.add_trace(
                go.Scatter(
                    x=[centroid_x],
                    y=[centroid_y],
                    mode="markers+text",
                    marker=dict(
                        size=self.style["centroid_marker_size"], color="orange", line=dict(width=3, color="black")
                    ),
                    text=[centroid_label or "Centroid"],
                    textposition="bottom right",
                    name="Signature Centroid",
                    hovertemplate="<b>%{text}</b><br>x: %{x:.3f}<br>y: %{y:.3f}<extra></extra>",
                )
            )

            fig.add_trace(
                go.Scatter(
                    x=[0, centroid_x],
                    y=[0, centroid_y],
                    mode="lines",
                    line=dict(color="orange", width=2, dash="dash"),
                    showlegend=False,
                    hoverinfo="skip",
                )
            )

            distance = np.sqrt(centroid_x**2 + centroid_y**2)
            angle_rad = np.arctan2(centroid_y, centroid_x)
            angle_deg = np.degrees(angle_rad) % 360

            metrics_text = f"Distance: {distance:.3f}<br>Angle: {angle_deg:.1f}°<br>Position: ({centroid_x:+.3f}, {centroid_y:+.3f})"

            fig.add_annotation(
                x=0.05,
                y=-0.95,
                text=metrics_text,
                showarrow=False,
                font=dict(size=10),
                bgcolor="rgba(173, 216, 230, 0.8)",
                bordercolor="rgba(0, 0, 0, 0.3)",
                borderwidth=1,
                borderpad=4,
                xanchor="left",
                yanchor="bottom",
            )

        if output_html:
            Path(output_html).parent.mkdir(parents=True, exist_ok=True)
            fig.write_html(output_html)

        if output_png:
            Path(output_png).parent.mkdir(parents=True, exist_ok=True)
            fig.write_image(output_png)

        if show:
            fig.show()

        return fig

    def plot_group_comparison(
        self,
        anchors: Dict,
        centroid_a: Tuple[float, float],
        label_a: str,
        centroid_b: Tuple[float, float],
        label_b: str,
        group_a_signatures: Optional[List[Dict]] = None,
        group_b_signatures: Optional[List[Dict]] = None,
        title: Optional[str] = None,
        output_html: Optional[str] = None,
        show: bool = True,
    ) -> go.Figure:
        """Creates a plot comparing the centroids of two groups."""
        fig = self.plot(anchors=anchors, show=False)  # Get the base plot with anchors

        # Plot individual points for Group A
        if group_a_signatures:
            group_a_xs = [s["centroid"][0] for s in group_a_signatures if "centroid" in s]
            group_a_ys = [s["centroid"][1] for s in group_a_signatures if "centroid" in s]
            fig.add_trace(
                go.Scatter(
                    x=group_a_xs,
                    y=group_a_ys,
                    mode="markers",
                    marker=dict(size=10, color="blue", opacity=0.4),
                    name=f"{label_a} points",
                    showlegend=False,
                    hoverinfo="skip",
                )
            )

        # Plot individual points for Group B
        if group_b_signatures:
            group_b_xs = [s["centroid"][0] for s in group_b_signatures if "centroid" in s]
            group_b_ys = [s["centroid"][1] for s in group_b_signatures if "centroid" in s]
            fig.add_trace(
                go.Scatter(
                    x=group_b_xs,
                    y=group_b_ys,
                    mode="markers",
                    marker=dict(size=10, color="red", opacity=0.4),
                    name=f"{label_b} points",
                    showlegend=False,
                    hoverinfo="skip",
                )
            )

        # Plot Centroid A
        fig.add_trace(
            go.Scatter(
                x=[centroid_a[0]],
                y=[centroid_a[1]],
                mode="markers+text",
                marker=dict(
                    size=self.style["centroid_marker_size"], color="blue", line=dict(width=3, color="darkblue")
                ),
                text=[label_a],
                textposition="top center",
                name=label_a,
                hovertemplate="<b>%{text}</b><br>x: %{x:.3f}<br>y: %{y:.3f}<extra></extra>",
            )
        )

        # Plot Centroid B
        fig.add_trace(
            go.Scatter(
                x=[centroid_b[0]],
                y=[centroid_b[1]],
                mode="markers+text",
                marker=dict(size=self.style["centroid_marker_size"], color="red", line=dict(width=3, color="darkred")),
                text=[label_b],
                textposition="bottom center",
                name=label_b,
                hovertemplate="<b>%{text}</b><br>x: %{x:.3f}<br>y: %{y:.3f}<extra></extra>",
            )
        )

        fig.update_layout(title=dict(text=title or "Group Centroid Comparison"), showlegend=True)

        if output_html:
            Path(output_html).parent.mkdir(parents=True, exist_ok=True)
            fig.write_html(output_html)

        if show:
            fig.show()

        return fig

    def plot_comparison(
        self,
        anchors: Dict,
        analysis_a: Dict,
        label_a: str,
        analysis_b: Dict,
        label_b: str,
        title: Optional[str] = None,
        output_html: Optional[str] = None,
        show: bool = True,
    ) -> go.Figure:
        """Creates a side-by-side comparison plot of two signatures."""
        fig = make_subplots(
            rows=1, cols=2, subplot_titles=[label_a, label_b], specs=[[{"type": "scatter"}, {"type": "scatter"}]]
        )

        # Generate each plot individually
        fig_a = self.plot(
            anchors, signature_scores=analysis_a["scores"], centroid_coords=analysis_a["centroid"], show=False
        )
        fig_b = self.plot(
            anchors, signature_scores=analysis_b["scores"], centroid_coords=analysis_b["centroid"], show=False
        )

        # Add traces to the subplots
        for trace in fig_a.data:
            fig.add_trace(trace, row=1, col=1)
        for trace in fig_b.data:
            fig.add_trace(trace, row=1, col=2)

        fig.update_layout(
            title=dict(text=title or "Comparative Analysis"),
            # Remove hardcoded dimensions for responsive design
            showlegend=False,
            autosize=True,
            margin=dict(l=20, r=20, t=60, b=20),
        )

        fig.update_xaxes(scaleanchor="y", scaleratio=1, range=[-1.2, 1.2])
        fig.update_yaxes(range=[-1.2, 1.2])

        if output_html:
            Path(output_html).parent.mkdir(parents=True, exist_ok=True)
            fig.write_html(output_html)

        if show:
            fig.show()

        return fig

    def create_comparison(
        self,
        analyses: List[Dict],
        title: str = "Comparative Analysis",
        output_html: Optional[str] = None,
        output_png: Optional[str] = None,
    ) -> go.Figure:
        """
        Create a comparison visualization with multiple analyses.

        Args:
            analyses: List of analysis results, each containing wells and scores
            title: Title for the comparison visualization
            output_html: Path to save interactive HTML
            output_png: Path to save static PNG
        """
        # Create subplot figure
        fig = make_subplots(
            rows=2,
            cols=2,
            subplot_titles=[analysis.get("title", f"Analysis {i+1}") for i, analysis in enumerate(analyses[:4])],
            specs=[[{"type": "scatter"}, {"type": "scatter"}], [{"type": "scatter"}, {"type": "scatter"}]],
        )

        # Plot each analysis
        for i, analysis in enumerate(analyses[:4]):
            row = (i // 2) + 1
            col = (i % 2) + 1

            wells = analysis.get("wells", {})
            scores = analysis.get("scores", {})

            # Create base visualization for this subplot
            base_fig = self.create_base_figure()

            # Add all traces to the subplot
            for trace in base_fig.data:
                fig.add_trace(trace, row=row, col=col)

            # Add wells and centroid
            subplot_fig = self.plot(wells, scores, show=False)
            for trace in subplot_fig.data[1:]:  # Skip the boundary trace
                fig.add_trace(trace, row=row, col=col)

        # Update layout with aspect ratio locking for all subplots
        fig.update_layout(
            title=dict(text=title, font=dict(size=self.style["title_size"], family=self.style["font_family"])),
            height=self.figure_size * 2,
            width=self.figure_size * 2,
            showlegend=False,
        )

        # Lock aspect ratio for all subplots to keep circles circular
        fig.update_xaxes(scaleanchor="y", scaleratio=1, range=[-1.2, 1.2])
        fig.update_yaxes(range=[-1.2, 1.2])

        # Save outputs
        if output_html:
            Path(output_html).parent.mkdir(parents=True, exist_ok=True)
            fig.write_html(output_html)

        if output_png:
            Path(output_png).parent.mkdir(parents=True, exist_ok=True)
            fig.write_image(output_png)

        return fig

    # =============================================================================
    # ENHANCED ANALYTICS & ACADEMIC OUTPUT FEATURES
    # =============================================================================

    def calculate_multi_run_variance(self, multi_run_data: List[Dict]) -> Dict:
        """
        Calculate variance analysis across multiple LLM runs for reliability assessment.

        Args:
            multi_run_data: List of run dictionaries, each containing:
                - 'scores': Dict of foundation scores
                - 'coordinates': Tuple of (x, y) coordinates
                - 'metadata': Dict with run information

        Returns:
            Dict with comprehensive variance statistics
        """
        if len(multi_run_data) < 2:
            return {"error": "Need at least 2 runs for variance analysis"}

        # Extract scores across runs
        all_scores = {}
        all_coordinates = []

        for run in multi_run_data:
            scores = run.get("scores", {})
            coords = run.get("coordinates", (0.0, 0.0))
            all_coordinates.append(coords)

            for foundation, score in scores.items():
                if foundation not in all_scores:
                    all_scores[foundation] = []
                all_scores[foundation].append(score)

        # Calculate foundation-level statistics
        foundation_stats = {}
        for foundation, score_list in all_scores.items():
            if len(score_list) >= 2:
                foundation_stats[foundation] = {
                    "mean": np.mean(score_list),
                    "std": np.std(score_list),
                    "var": np.var(score_list),
                    "min": np.min(score_list),
                    "max": np.max(score_list),
                    "coefficient_of_variation": (
                        np.std(score_list) / np.mean(score_list) if np.mean(score_list) > 0 else 0
                    ),
                }

        # Calculate coordinate-level statistics
        x_coords = [coord[0] for coord in all_coordinates]
        y_coords = [coord[1] for coord in all_coordinates]
        distances = [np.sqrt(x**2 + y**2) for x, y in all_coordinates]

        coordinate_stats = {
            "x_mean": np.mean(x_coords),
            "x_std": np.std(x_coords),
            "y_mean": np.mean(y_coords),
            "y_std": np.std(y_coords),
            "distance_mean": np.mean(distances),
            "distance_std": np.std(distances),
            "coordinate_variance": np.var(x_coords) + np.var(y_coords),
        }

        # Calculate inter-run correlations
        reliability_metrics = {}
        if len(multi_run_data) >= 3:
            # Pearson correlation between consecutive runs
            correlations = []
            for i in range(len(multi_run_data) - 1):
                run1_scores = list(multi_run_data[i]["scores"].values())
                run2_scores = list(multi_run_data[i + 1]["scores"].values())
                if len(run1_scores) == len(run2_scores) and len(run1_scores) > 1:
                    corr, _ = stats.pearsonr(run1_scores, run2_scores)
                    correlations.append(corr)

            reliability_metrics = {
                "inter_run_correlation": np.mean(correlations) if correlations else 0,
                "correlation_std": np.std(correlations) if correlations else 0,
                "overall_reliability": (
                    1 - np.mean([stats["coefficient_of_variation"] for stats in foundation_stats.values()])
                    if foundation_stats
                    else 0
                ),
            }

        return {
            "foundation_statistics": foundation_stats,
            "coordinate_statistics": coordinate_stats,
            "reliability_metrics": reliability_metrics,
            "run_count": len(multi_run_data),
            "analysis_timestamp": datetime.now().isoformat(),
        }

    def generate_academic_report(self, analysis_data: Dict, output_dir: Path, include_methodology: bool = True) -> Path:
        """
        Generate comprehensive HTML academic report with methodology and results.

        Args:
            analysis_data: Complete analysis data including multi-run variance
            output_dir: Directory to save the report
            include_methodology: Whether to include detailed methodology section

        Returns:
            Path to generated HTML report
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = output_dir / f"discernus_analysis_report_{timestamp}.html"

        # Extract key information
        foundation_stats = analysis_data.get("foundation_statistics", {})
        coordinate_stats = analysis_data.get("coordinate_statistics", {})
        reliability_metrics = analysis_data.get("reliability_metrics", {})
        algorithm_config = analysis_data.get("algorithm_config", {})

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Discernus Analysis Report</title>
            <style>
                body {{ font-family: 'Arial', sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 30px; }}
                .section {{ margin-bottom: 30px; }}
                .metrics-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }}
                .metric-card {{ background: #fff; border: 1px solid #dee2e6; border-radius: 8px; padding: 15px; }}
                .metric-title {{ font-weight: bold; color: #495057; margin-bottom: 10px; }}
                .metric-value {{ font-size: 1.2em; color: #28a745; }}
                table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}
                th, td {{ border: 1px solid #dee2e6; padding: 8px; text-align: left; }}
                th {{ background-color: #f8f9fa; }}
                .methodology {{ background-color: #e9ecef; padding: 20px; border-radius: 8px; }}
                .algorithm-config {{ background-color: #fff3cd; padding: 15px; border-radius: 8px; border: 1px solid #ffeaa7; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Discernus Narrative Gravity Analysis Report</h1>
                <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p><strong>Analysis Type:</strong> Multi-Run Variance Analysis with Algorithm Configuration</p>
            </div>
        """

        # Algorithm Configuration Section
        if algorithm_config:
            html_content += f"""
            <div class="section">
                <h2>Algorithm Configuration</h2>
                <div class="algorithm-config">
                    <h3>Dominance Amplification</h3>
                    <ul>
                        <li><strong>Enabled:</strong> {algorithm_config.get('dominance_amplification', {}).get('enabled', 'N/A')}</li>
                        <li><strong>Threshold:</strong> {algorithm_config.get('dominance_amplification', {}).get('threshold', 'N/A')}</li>
                        <li><strong>Multiplier:</strong> {algorithm_config.get('dominance_amplification', {}).get('multiplier', 'N/A')}</li>
                    </ul>
                    
                    <h3>Adaptive Scaling</h3>
                    <ul>
                        <li><strong>Base Scaling:</strong> {algorithm_config.get('adaptive_scaling', {}).get('base_scaling', 'N/A')}</li>
                        <li><strong>Max Scaling:</strong> {algorithm_config.get('adaptive_scaling', {}).get('max_scaling', 'N/A')}</li>
                        <li><strong>Variance Factor:</strong> {algorithm_config.get('adaptive_scaling', {}).get('variance_factor', 'N/A')}</li>
                    </ul>
                </div>
            </div>
            """

        # Reliability Metrics
        if reliability_metrics:
            html_content += f"""
            <div class="section">
                <h2>Reliability Metrics</h2>
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="metric-title">Overall Reliability Index</div>
                        <div class="metric-value">{reliability_metrics.get('overall_reliability', 0):.3f}</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-title">Inter-Run Correlation</div>
                        <div class="metric-value">{reliability_metrics.get('inter_run_correlation', 0):.3f}</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-title">Run Count</div>
                        <div class="metric-value">{analysis_data.get('run_count', 0)}</div>
                    </div>
                </div>
            </div>
            """

        # Foundation Statistics
        if foundation_stats:
            html_content += """
            <div class="section">
                <h2>Foundation-Level Analysis</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Foundation</th>
                            <th>Mean Score</th>
                            <th>Std Dev</th>
                            <th>Coefficient of Variation</th>
                            <th>Range</th>
                        </tr>
                    </thead>
                    <tbody>
            """

            for foundation, stats in foundation_stats.items():
                html_content += f"""
                        <tr>
                            <td>{foundation}</td>
                            <td>{stats['mean']:.3f}</td>
                            <td>{stats['std']:.3f}</td>
                            <td>{stats['coefficient_of_variation']:.3f}</td>
                            <td>{stats['min']:.3f} - {stats['max']:.3f}</td>
                        </tr>
                """

            html_content += """
                    </tbody>
                </table>
            </div>
            """

        # Coordinate Statistics
        if coordinate_stats:
            html_content += f"""
            <div class="section">
                <h2>Coordinate Space Analysis</h2>
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="metric-title">Mean Position</div>
                        <div class="metric-value">({coordinate_stats.get('x_mean', 0):.3f}, {coordinate_stats.get('y_mean', 0):.3f})</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-title">Position Variance</div>
                        <div class="metric-value">{coordinate_stats.get('coordinate_variance', 0):.4f}</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-title">Mean Distance from Origin</div>
                        <div class="metric-value">{coordinate_stats.get('distance_mean', 0):.3f}</div>
                    </div>
                </div>
            </div>
            """

        # Methodology Section
        if include_methodology:
            html_content += """
            <div class="section">
                <h2>Methodology</h2>
                <div class="methodology">
                    <h3>LLM-Prompting-Amplification Pipeline</h3>
                    <p>This analysis employed the Discernus LLM-prompting-amplification pipeline, which integrates:</p>
                    <ol>
                        <li><strong>LLM Semantic Analysis:</strong> Large Language Models identify nuanced patterns and hierarchical relationships in text</li>
                        <li><strong>Algorithmic Enhancement:</strong> Optional mathematical amplification of computationally-identified dominance patterns</li>
                        <li><strong>Coordinate Positioning:</strong> Integration of enhanced assessments into geometric coordinate space</li>
                    </ol>
                    
                    <h3>Multi-Run Reliability Assessment</h3>
                    <p>Reliability is assessed through multiple independent LLM runs, calculating:</p>
                    <ul>
                        <li>Inter-run correlations for consistency measurement</li>
                        <li>Coefficient of variation for score stability</li>
                        <li>Coordinate variance for positional reliability</li>
                    </ul>
                    
                    <h3>Academic Reporting Standards</h3>
                    <p>Algorithm parameters are fully documented for reproducibility. Enhanced scores reflect the integration of LLM assessment and mathematical amplification, not raw LLM outputs.</p>
                </div>
            </div>
            """

        html_content += """
        </body>
        </html>
        """

        with open(report_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        return report_path

    def export_csv_data(self, analysis_data: Dict, output_dir: Path) -> Dict[str, Path]:
        """
        Export analysis data to CSV files for statistical analysis in R/SPSS/etc.

        Args:
            analysis_data: Complete analysis data
            output_dir: Directory to save CSV files

        Returns:
            Dict mapping data type to file path
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        exported_files = {}

        # Export foundation statistics
        foundation_stats = analysis_data.get("foundation_statistics", {})
        if foundation_stats:
            foundation_df_data = []
            for foundation, stats in foundation_stats.items():
                foundation_df_data.append(
                    {
                        "foundation": foundation,
                        "mean_score": stats["mean"],
                        "std_dev": stats["std"],
                        "variance": stats["var"],
                        "min_score": stats["min"],
                        "max_score": stats["max"],
                        "coefficient_of_variation": stats["coefficient_of_variation"],
                    }
                )

            foundation_df = pd.DataFrame(foundation_df_data)
            foundation_path = output_dir / f"foundation_statistics_{timestamp}.csv"
            foundation_df.to_csv(foundation_path, index=False)
            exported_files["foundation_statistics"] = foundation_path

        # Export coordinate statistics
        coordinate_stats = analysis_data.get("coordinate_statistics", {})
        if coordinate_stats:
            coordinate_df = pd.DataFrame([coordinate_stats])
            coordinate_path = output_dir / f"coordinate_statistics_{timestamp}.csv"
            coordinate_df.to_csv(coordinate_path, index=False)
            exported_files["coordinate_statistics"] = coordinate_path

        # Export reliability metrics
        reliability_metrics = analysis_data.get("reliability_metrics", {})
        if reliability_metrics:
            reliability_df = pd.DataFrame([reliability_metrics])
            reliability_path = output_dir / f"reliability_metrics_{timestamp}.csv"
            reliability_df.to_csv(reliability_path, index=False)
            exported_files["reliability_metrics"] = reliability_path

        # Export algorithm configuration
        algorithm_config = analysis_data.get("algorithm_config", {})
        if algorithm_config:
            # Flatten algorithm config for CSV
            algo_flat = {}
            for section, params in algorithm_config.items():
                if isinstance(params, dict):
                    for param, value in params.items():
                        algo_flat[f"{section}_{param}"] = value
                else:
                    algo_flat[section] = params

            algo_df = pd.DataFrame([algo_flat])
            algo_path = output_dir / f"algorithm_configuration_{timestamp}.csv"
            algo_df.to_csv(algo_path, index=False)
            exported_files["algorithm_configuration"] = algo_path

        return exported_files

    def generate_r_script(self, csv_files: Dict[str, Path], output_dir: Path) -> Path:
        """
        Generate R script for statistical analysis of exported CSV data.

        Args:
            csv_files: Dict mapping data type to CSV file path
            output_dir: Directory to save R script

        Returns:
            Path to generated R script
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        r_script_path = output_dir / f"discernus_analysis_{timestamp}.R"

        r_script = f"""
# Discernus Analysis R Script
# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# 
# This script provides statistical analysis of Discernus narrative gravity data
# with configurable algorithms and multi-run reliability assessment.

library(tidyverse)
library(corrplot)
library(psych)

# Set working directory to script location
setwd(dirname(rstudioapi::getActiveDocumentContext()$path))

# Load data files
"""

        # Add data loading commands
        for data_type, file_path in csv_files.items():
            var_name = data_type.replace("_", ".")
            r_script += f"{var_name} <- read.csv('{file_path.name}')\n"

        r_script += """

# Foundation Analysis
if(exists('foundation.statistics')) {
  cat("\\n=== FOUNDATION ANALYSIS ===\\n")
  
  # Summary statistics
  print(summary(foundation.statistics))
  
  # Reliability assessment
  cat("\\nMean Coefficient of Variation:", mean(foundation.statistics$coefficient_of_variation), "\\n")
  
  # Foundation comparison plot
  ggplot(foundation.statistics, aes(x = foundation, y = mean_score)) +
    geom_col(fill = "steelblue", alpha = 0.7) +
    geom_errorbar(aes(ymin = mean_score - std_dev, ymax = mean_score + std_dev), 
                  width = 0.2) +
    theme_minimal() +
    labs(title = "Foundation Scores with Standard Deviation",
         x = "Foundation", y = "Mean Score") +
    theme(axis.text.x = element_text(angle = 45, hjust = 1))
  
  ggsave("foundation_analysis.png", width = 10, height = 6, dpi = 300)
}

# Coordinate Analysis  
if(exists('coordinate.statistics')) {
  cat("\\n=== COORDINATE ANALYSIS ===\\n")
  print(coordinate.statistics)
  
  # Calculate position metrics
  if('x_mean' %in% names(coordinate.statistics) && 'y_mean' %in% names(coordinate.statistics)) {
    distance_from_origin <- sqrt(coordinate.statistics$x_mean^2 + coordinate.statistics$y_mean^2)
    angle_degrees <- atan2(coordinate.statistics$y_mean, coordinate.statistics$x_mean) * 180 / pi
    
    cat("\\nPosition Metrics:\\n")
    cat("Distance from Origin:", distance_from_origin, "\\n")
    cat("Angle (degrees):", angle_degrees, "\\n")
  }
}

# Reliability Analysis
if(exists('reliability.metrics')) {
  cat("\\n=== RELIABILITY ANALYSIS ===\\n")
  print(reliability.metrics)
  
  if('overall_reliability' %in% names(reliability.metrics)) {
    cat("\\nReliability Assessment:\\n")
    if(reliability.metrics$overall_reliability > 0.8) {
      cat("HIGH reliability (>0.8)\\n")
    } else if(reliability.metrics$overall_reliability > 0.6) {
      cat("MODERATE reliability (0.6-0.8)\\n") 
    } else {
      cat("LOW reliability (<0.6) - consider more runs\\n")
    }
  }
}

# Algorithm Configuration Analysis
if(exists('algorithm.configuration')) {
  cat("\\n=== ALGORITHM CONFIGURATION ===\\n")
  print(algorithm.configuration)
  
  # Check for standard configurations
  if('dominance_amplification_threshold' %in% names(algorithm.configuration)) {
    threshold <- algorithm.configuration$dominance_amplification_threshold
    multiplier <- algorithm.configuration$dominance_amplification_multiplier
    
    cat("\\nAlgorithm Settings:\\n")
    cat("Dominance Threshold:", threshold, "\\n")
    cat("Amplification Multiplier:", multiplier, "\\n")
    
    if(threshold == 0.7 && multiplier == 1.1) {
      cat("Using STANDARD algorithm configuration\\n")
    } else {
      cat("Using CUSTOM algorithm configuration\\n")
    }
  }
}

cat("\\n=== ANALYSIS COMPLETE ===\\n")
cat("Charts saved as PNG files in working directory\\n")
"""

        with open(r_script_path, "w", encoding="utf-8") as f:
            f.write(r_script)

        return r_script_path

    def add_provenance_info(self, fig: go.Figure, algorithm_config: Dict, analysis_metadata: Dict = None) -> go.Figure:
        """
        Add interactive provenance tracking to Plotly charts.

        Args:
            fig: Plotly figure to enhance
            algorithm_config: Algorithm configuration used
            analysis_metadata: Additional metadata about the analysis

        Returns:
            Enhanced figure with provenance information
        """
        # Create provenance annotation
        provenance_text = "Algorithm Provenance:<br>"

        # Dominance amplification info
        dom_config = algorithm_config.get("dominance_amplification", {})
        if dom_config.get("enabled", False):
            provenance_text += f"Dominance: threshold={dom_config.get('threshold', 'N/A')}, multiplier={dom_config.get('multiplier', 'N/A')}<br>"
        else:
            provenance_text += "Dominance: disabled<br>"

        # Adaptive scaling info
        scale_config = algorithm_config.get("adaptive_scaling", {})
        if scale_config.get("enabled", False):
            provenance_text += (
                f"Scaling: {scale_config.get('base_scaling', 'N/A')}-{scale_config.get('max_scaling', 'N/A')}<br>"
            )
        else:
            provenance_text += "Scaling: disabled<br>"

        # Analysis metadata
        if analysis_metadata:
            provenance_text += f"Run Count: {analysis_metadata.get('run_count', 'N/A')}<br>"
            provenance_text += f"Timestamp: {analysis_metadata.get('timestamp', 'N/A')}<br>"

        # Add as annotation in bottom right
        fig.add_annotation(
            x=1.15,
            y=-0.95,
            text=provenance_text,
            showarrow=False,
            font=dict(size=9, color="gray"),
            bgcolor="rgba(255, 255, 255, 0.8)",
            bordercolor="rgba(0, 0, 0, 0.1)",
            borderwidth=1,
            borderpad=4,
            xanchor="left",
            yanchor="bottom",
            xref="paper",
            yref="paper",
        )

        # Add hover info to title
        current_title = fig.layout.title.text if fig.layout.title else "Analysis"
        fig.update_layout(
            title=dict(
                text=f"{current_title}<br><sub>Interactive provenance: hover for details</sub>",
                font=dict(size=self.style["title_size"], family=self.style["font_family"]),
            )
        )

        return fig

    def create_multi_run_visualization(
        self,
        multi_run_data: List[Dict],
        wells: Dict,
        title: str = "Multi-Run Analysis",
        output_dir: Optional[Path] = None,
    ) -> Dict:
        """
        Create comprehensive multi-run visualization with variance analysis.

        Args:
            multi_run_data: List of run data dictionaries
            wells: Wells configuration
            title: Chart title
            output_dir: Directory to save outputs

        Returns:
            Dict containing figure, variance stats, and file paths
        """
        if len(multi_run_data) < 2:
            raise ValueError("Need at least 2 runs for multi-run analysis")

        # Calculate variance statistics
        variance_stats = self.calculate_multi_run_variance(multi_run_data)

        # Create the main comparison figure
        fig = self.create_base_figure(f"{title} - Multi-Run Comparison")

        # Plot all run positions
        colors = px.colors.qualitative.Set1[: len(multi_run_data)]

        for i, run_data in enumerate(multi_run_data):
            coords = run_data.get("coordinates", (0.0, 0.0))
            run_label = f"Run {i+1}"

            # Add run position
            fig.add_trace(
                go.Scatter(
                    x=[coords[0]],
                    y=[coords[1]],
                    mode="markers+text",
                    marker=dict(size=20, color=colors[i], line=dict(width=2, color="black")),
                    text=[run_label],
                    textposition="top center",
                    name=run_label,
                    hovertemplate=f"<b>{run_label}</b><br>x: %{{x:.3f}}<br>y: %{{y:.3f}}<extra></extra>",
                )
            )

            # Add line from center
            fig.add_trace(
                go.Scatter(
                    x=[0, coords[0]],
                    y=[0, coords[1]],
                    mode="lines",
                    line=dict(color=colors[i], width=1, dash="dot"),
                    showlegend=False,
                    hoverinfo="skip",
                )
            )

        # Add mean position
        mean_x = variance_stats["coordinate_statistics"]["x_mean"]
        mean_y = variance_stats["coordinate_statistics"]["y_mean"]

        fig.add_trace(
            go.Scatter(
                x=[mean_x],
                y=[mean_y],
                mode="markers+text",
                marker=dict(size=30, color="red", symbol="star", line=dict(width=3, color="darkred")),
                text=["Mean"],
                textposition="bottom center",
                name="Mean Position",
                hovertemplate="<b>Mean Position</b><br>x: %{x:.3f}<br>y: %{y:.3f}<extra></extra>",
            )
        )

        # Add confidence ellipse if we have enough runs
        if len(multi_run_data) >= 3:
            x_coords = [run["coordinates"][0] for run in multi_run_data]
            y_coords = [run["coordinates"][1] for run in multi_run_data]

            # Calculate 95% confidence ellipse
            cov_matrix = np.cov(x_coords, y_coords)
            eigenvals, eigenvecs = np.linalg.eigh(cov_matrix)

            # 95% confidence
            chi_sq_val = 5.991  # Chi-square value for 95% confidence, 2 DOF
            ellipse_radii = np.sqrt(chi_sq_val * eigenvals)

            # Generate ellipse points
            angles = np.linspace(0, 2 * np.pi, 100)
            ellipse_x = ellipse_radii[0] * np.cos(angles)
            ellipse_y = ellipse_radii[1] * np.sin(angles)

            # Rotate ellipse
            rotation_matrix = eigenvecs
            ellipse_points = np.dot(rotation_matrix, np.array([ellipse_x, ellipse_y]))

            # Translate to mean position
            ellipse_x_final = ellipse_points[0] + mean_x
            ellipse_y_final = ellipse_points[1] + mean_y

            fig.add_trace(
                go.Scatter(
                    x=ellipse_x_final,
                    y=ellipse_y_final,
                    mode="lines",
                    line=dict(color="red", dash="dash", width=2),
                    name="95% Confidence",
                    hovertemplate="95% Confidence Ellipse<extra></extra>",
                )
            )

        # Add variance statistics annotation
        reliability_index = variance_stats["reliability_metrics"].get("overall_reliability", 0)
        coord_variance = variance_stats["coordinate_statistics"]["coordinate_variance"]

        stats_text = f"Runs: {len(multi_run_data)}<br>"
        stats_text += f"Reliability: {reliability_index:.3f}<br>"
        stats_text += f"Coord Variance: {coord_variance:.4f}<br>"
        stats_text += f'Mean Distance: {variance_stats["coordinate_statistics"]["distance_mean"]:.3f}'

        fig.add_annotation(
            x=1.02,
            y=0.98,
            text=stats_text,
            showarrow=False,
            font=dict(size=10),
            bgcolor="rgba(144, 238, 144, 0.8)",
            bordercolor="rgba(0, 100, 0, 0.3)",
            borderwidth=1,
            borderpad=4,
            xanchor="left",
            yanchor="top",
            xref="paper",
            yref="paper",
        )

        fig.update_layout(showlegend=True)

        # Save outputs if directory provided
        saved_files = {}
        if output_dir:
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)

            # Save chart
            chart_path = output_dir / f"multi_run_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
            fig.write_html(chart_path)
            saved_files["chart"] = chart_path

            # Save variance statistics
            stats_path = output_dir / f"variance_statistics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(stats_path, "w") as f:
                json.dump(variance_stats, f, indent=2, default=str)
            saved_files["statistics"] = stats_path

        return {"figure": fig, "variance_statistics": variance_stats, "saved_files": saved_files}


if __name__ == "__main__":
    # Example usage with dummy data
    wells = {
        "Hope": {"angle": 0, "type": "integrative", "weight": 1.0},
        "Justice": {"angle": 72, "type": "integrative", "weight": 0.8},
        "Truth": {"angle": 144, "type": "integrative", "weight": 0.8},
        "Fear": {"angle": 216, "type": "disintegrative", "weight": 0.6},
        "Manipulation": {"angle": 288, "type": "disintegrative", "weight": 0.6},
    }
    scores = {"Hope": 0.9, "Justice": 0.7, "Truth": 0.2, "Fear": 0.1, "Manipulation": 0.5}

    # Single visualization
    viz = RebootPlotlyCircularVisualizer()
    viz.plot(wells, signature_scores=scores, centroid_label="Example", title="Single Analysis Example", show=True)

    # Comparison visualization
    analyses = [
        {"title": "Analysis 1", "wells": wells, "scores": scores},
        {"title": "Analysis 2", "wells": wells, "scores": {k: 1 - v for k, v in scores.items()}},
        {"title": "Analysis 3", "wells": wells, "scores": {k: v * 0.5 for k, v in scores.items()}},
        {"title": "Analysis 4", "wells": wells, "scores": {k: abs(np.sin(v)) for k, v in scores.items()}},
    ]
    viz.create_comparison(analyses, title="Comparison Example", output_html="comparison_example.html")
