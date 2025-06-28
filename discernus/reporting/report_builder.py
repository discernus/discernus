from pathlib import Path
from typing import Dict, Tuple, List, Any
import jinja2
from .reboot_plotly_circular import RebootPlotlyCircularVisualizer
import uuid
from datetime import datetime
import json


class ReportBuilder:
    """
    Builds the visual report for an analysis.
    Uses the rebooted, glossary-compliant visualizer.
    """

    def __init__(self, output_dir: str = "reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.visualizer = RebootPlotlyCircularVisualizer()
        template_dir = Path(__file__).parent / "templates"
        self.env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))

    def _calculate_group_centroid(self, signatures: List[Dict]) -> Tuple[float, float]:
        if not signatures:
            return (0.0, 0.0)
        all_coords = [s["centroid"] for s in signatures if "centroid" in s]
        if not all_coords:
            return (0.0, 0.0)
        avg_x = sum(c[0] for c in all_coords) / len(all_coords)
        avg_y = sum(c[1] for c in all_coords) / len(all_coords)
        return (avg_x, avg_y)

    def generate_report(self, anchors: Dict, scores: Dict, coordinates: Tuple[float, float], run_id: str) -> str:
        """
        Generates an HTML visualization and returns the file path.
        """
        output_filename = self.output_dir / f"analysis_report_{run_id}.html"

        self.visualizer.plot(
            anchors=anchors,
            signature_scores=scores,
            centroid_coords=coordinates,
            output_html=str(output_filename),
            show=False,
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
        distance: float,
    ) -> str:
        """Generates a side-by-side HTML comparison report."""
        template = self.env.get_template("comparison_template.html")

        # This data structure is used for the scatter plot
        plot_data = [
            {"x": analysis_a["centroid"][0], "y": analysis_a["centroid"][1], "label": label_a},
            {"x": analysis_b["centroid"][0], "y": analysis_b["centroid"][1], "label": label_b},
        ]

        title = f"Comparison: {label_a} vs. {label_b}"
        plot_html = self._generate_comparison_plot(anchors, analysis_a, label_a, analysis_b, label_b, title)

        html_content = template.render(
            report_title=title,
            plot_html=plot_html,
            scores_a=analysis_a["scores"],
            scores_b=analysis_b["scores"],
            label_a=label_a,
            label_b=label_b,
            distance=f"{distance:.4f}",  # Format for display
        )

        report_filename = f"comparison_report_{run_id}.html"
        report_path = self.output_dir / report_filename
        with open(report_path, "w") as f:
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
            show=False,
        )

        # Read the generated plot and return it as an HTML string
        with open(temp_plot_path, "r") as f:
            plot_html = f.read()

        # Clean up the temporary file
        temp_plot_path.unlink()

        return plot_html

    def generate_group_report(self, anchors: Dict, signatures: List[Dict], group_label: str, run_id: str) -> str:
        """Generates a report for a group of signatures, plotting their centroid."""
        if not signatures:
            return "No signatures provided for group report."

        # Calculate the centroid for the group
        all_coords = [s["centroid"] for s in signatures if "centroid" in s]
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
            signature_scores={},  # No individual scores needed for a group plot
            centroid_coords=group_centroid,
            centroid_label=group_label,
            title=f"Group Centroid: {group_label}",
            output_html=str(output_filename),
            show=False,
        )
        return str(output_filename)

    def _generate_group_comparison_plot(self, anchors, group_a_signatures, label_a, group_b_signatures, label_b, title):
        # Create a temporary file for the plot to be saved to
        temp_plot_path = self.output_dir / f"temp_plot_{uuid.uuid4()}.html"

        centroid_a = self._calculate_group_centroid(group_a_signatures)
        centroid_b = self._calculate_group_centroid(group_b_signatures)

        self.visualizer.plot_group_comparison(
            anchors=anchors,
            centroid_a=centroid_a,
            label_a=label_a,
            group_a_signatures=group_a_signatures,
            centroid_b=centroid_b,
            label_b=label_b,
            group_b_signatures=group_b_signatures,
            title=title,
            output_html=str(temp_plot_path),
            show=False,
        )

        # Read the generated plot and return it as an HTML string
        with open(temp_plot_path, "r") as f:
            plot_html = f.read()

        # Clean up the temporary file
        temp_plot_path.unlink()

        return plot_html

    def generate_group_comparison_report(
        self,
        anchors: Dict,
        group_a_signatures: List[Dict],
        label_a: str,
        group_b_signatures: List[Dict],
        label_b: str,
        run_id: str,
        distance: float,
    ) -> str:
        """Generates a report comparing the centroids of two groups."""

        template = self.env.get_template("group_comparison_template.html")
        title = f"Group Comparison: {label_a} vs. {label_b}"

        plot_html = self._generate_group_comparison_plot(
            anchors=anchors,
            group_a_signatures=group_a_signatures,
            label_a=label_a,
            group_b_signatures=group_b_signatures,
            label_b=label_b,
            title=title,
        )

        html_content = template.render(
            report_title=title,
            plot_html=plot_html,
            label_a=label_a,
            label_b=label_b,
            distance=f"{distance:.4f}",  # Format for display
            generation_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )

        report_filename = f"group_comparison_report_{run_id}.html"
        report_path = self.output_dir / report_filename
        with open(report_path, "w") as f:
            f.write(html_content)

        return str(report_path)

    def generate_statistical_comparison_report(
        self,
        anchors: Dict,
        condition_results: List[Dict],
        statistical_metrics: Dict,
        comparison_type: str,
        job_id: str,
        run_id: str,
    ) -> str:
        """Generates a statistical comparison report with visualizations and metrics."""
        
        template = self.env.get_template("enhanced_statistical_comparison_template.html")
        title = f"Statistical Comparison: {comparison_type}"

        # Generate the visualization plot using the existing comparison visualization
        # For now, we'll use a simple plot with multiple centroids
        plot_html = self._generate_statistical_comparison_plot(
            anchors=anchors,
            condition_results=condition_results,
            title=title
        )

        html_content = template.render(
            report_title=title,
            job_id=job_id,
            comparison_type=comparison_type,
            condition_results=condition_results,
            statistical_metrics=statistical_metrics,
            plot_html=plot_html,
            generation_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )

        report_filename = f"statistical_comparison_report_{run_id}.html"
        report_path = self.output_dir / report_filename
        with open(report_path, "w") as f:
            f.write(html_content)

        return str(report_path)

    def _generate_statistical_comparison_plot(self, anchors, condition_results, title):
        """Generate a proper circular coordinate plot showing multiple model centroids."""
        try:
            # Create a temporary file for the plot to be saved to
            temp_plot_path = self.output_dir / f"temp_plot_{uuid.uuid4()}.html"

            # Use the circular visualizer for proper coordinate system display
            if len(condition_results) >= 2:
                analysis_a = {
                    "scores": condition_results[0]["raw_scores"],
                    "centroid": condition_results[0]["centroid"]
                }
                analysis_b = {
                    "scores": condition_results[1]["raw_scores"], 
                    "centroid": condition_results[1]["centroid"]
                }
                
                self.visualizer.plot_comparison(
                    anchors=anchors,
                    analysis_a=analysis_a,
                    label_a=condition_results[0]["condition_identifier"],
                    analysis_b=analysis_b,
                    label_b=condition_results[1]["condition_identifier"],
                    title=f"{title}: {condition_results[0]['condition_identifier']} vs {condition_results[1]['condition_identifier']}",
                    output_html=str(temp_plot_path),
                    show=False,
                )
            elif len(condition_results) == 1:
                # Single model circular plot
                self.visualizer.plot(
                    anchors=anchors,
                    signature_scores=condition_results[0]["raw_scores"],
                    centroid_coords=condition_results[0]["centroid"],
                    title=f"{title} - {condition_results[0]['condition_identifier']}",
                    output_html=str(temp_plot_path),
                    show=False,
                )
            else:
                return "<p>No condition results available for visualization.</p>"

            # Read the generated plot and return it as an HTML string
            with open(temp_plot_path, "r") as f:
                plot_html = f.read()

            # Clean up the temporary file
            temp_plot_path.unlink()

            return plot_html
                
        except Exception as e:
            return f"<p>Error generating circular visualization: {str(e)}</p>"

    def generate_corpus_statistical_comparison_report(
        self,
        anchors: List[Dict],
        model_groups: Dict[str, List],
        statistical_metrics: Dict[str, Any],
        experiment_def: Dict[str, Any],
        job_id: str,
        run_id: str,
    ) -> str:
        """Generate comprehensive corpus-based statistical comparison report"""
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Calculate model averages for visualization
        model_summaries = {}
        for model, results in model_groups.items():
            centroids = [r["centroid"] for r in results]
            scores_list = [r["scores"] for r in results]
            
            avg_centroid = self._calculate_average_centroid(centroids)
            avg_scores = self._calculate_average_scores(scores_list)
            
            model_summaries[model] = {
                "average_centroid": avg_centroid,
                "average_scores": avg_scores,
                "total_texts": len(results),
                "score_variance": self._calculate_score_variance(scores_list)
            }
        
        # Generate similarity indicators
        similarity_indicators = self._generate_similarity_indicators(statistical_metrics, experiment_def)
        
        # Generate innovative statistical summary
        statistical_summary = self._generate_accessible_statistical_summary(statistical_metrics)
        
        # Generate prompt documentation
        prompt_documentation = self._extract_prompt_documentation(experiment_def)
        
        # Create individual model visualizations
        model_charts = {}
        for model, summary in model_summaries.items():
            model_charts[model] = self._create_model_summary_chart(
                model, summary, anchors, model_groups[model]
            )
        
        # Create comparison overview chart
        comparison_chart = self._create_model_comparison_overview_chart(
            model_summaries, anchors
        )
        
        # Generate correlation heatmap
        correlation_heatmap = self._create_correlation_heatmap(statistical_metrics)
        
        # Build comprehensive report
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flagship Model Statistical Comparison: {experiment_def.get('experiment_meta', {}).get('display_name', 'Statistical Analysis')}</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        {self._get_enhanced_statistical_styles()}
    </style>
</head>
<body>
    <div class="report-container">
        <!-- Header Section -->
        <header class="report-header">
            <h1>Flagship Model Statistical Comparison</h1>
            <h2>{experiment_def.get('experiment_meta', {}).get('display_name', 'Statistical Analysis')}</h2>
            <div class="report-meta">
                <p><strong>Generated:</strong> {timestamp}</p>
                <p><strong>Job ID:</strong> {job_id}</p>
                <p><strong>Research Question:</strong> Do different flagship cloud LLMs produce statistically similar results for substantive texts?</p>
            </div>
        </header>

        <!-- Executive Summary with Traffic Lights -->
        <section class="executive-summary">
            <h2>Executive Summary</h2>
            <div class="similarity-dashboard">
                {similarity_indicators}
            </div>
            
            <div class="key-findings">
                <h3>Key Findings</h3>
                {statistical_summary['executive_findings']}
            </div>
        </section>

        <!-- Model Comparison Overview -->
        <section class="model-overview">
            <h2>Model Comparison Overview</h2>
            <div class="chart-container">
                <div id="comparison-overview-chart"></div>
            </div>
            
            <div class="model-summary-grid">
                {self._generate_model_summary_cards(model_summaries)}
            </div>
        </section>

        <!-- Individual Model Charts -->
        <section class="individual-models">
            <h2>Individual Model Analysis</h2>
            <div class="model-charts-grid">
                {self._generate_model_charts_html(model_charts)}
            </div>
        </section>

        <!-- Statistical Results -->
        <section class="statistical-results">
            <h2>Statistical Analysis Results</h2>
            
            <!-- Accessible Summary -->
            <div class="accessible-stats">
                {statistical_summary['accessible_summary']}
            </div>
            
            <!-- Correlation Analysis -->
            <div class="correlation-section">
                <h3>Cross-Model Correlation Analysis</h3>
                <div id="correlation-heatmap"></div>
                {statistical_summary['correlation_interpretation']}
            </div>
            
            <!-- Expandable Technical Details -->
            <details class="technical-details">
                <summary>Technical Statistical Details</summary>
                {statistical_summary['technical_details']}
            </details>
        </section>

        <!-- Corpus Characteristics -->
        <section class="corpus-info">
            <h2>Corpus Characteristics</h2>
            {self._generate_corpus_characteristics(model_groups, experiment_def)}
        </section>

        <!-- Prompt Documentation -->
        <section class="prompt-documentation">
            <h2>Methodology: Prompt Documentation</h2>
            {prompt_documentation}
        </section>

        <!-- Technical Appendix -->
        <section class="technical-appendix">
            <h2>Technical Appendix</h2>
            <details>
                <summary>Raw Statistical Metrics</summary>
                <pre class="json-display">{json.dumps(statistical_metrics, indent=2, default=str)}</pre>
            </details>
            
            <details>
                <summary>Experiment Configuration</summary>
                <pre class="json-display">{json.dumps(experiment_def, indent=2)}</pre>
            </details>
        </section>
    </div>

    <script>
        // Render comparison overview chart
        {comparison_chart}
        
        // Render correlation heatmap
        {correlation_heatmap}
        
        // Render individual model charts
        {self._generate_model_charts_scripts(model_charts)}
    </script>
</body>
</html>
        """
        
        # Save report
        report_filename = f"corpus_statistical_comparison_{run_id}.html"
        report_path = self.output_dir / report_filename
        
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        return str(report_path)

    def _generate_similarity_indicators(self, statistical_metrics: Dict[str, Any], experiment_def: Dict[str, Any]) -> str:
        """Generate traffic light similarity indicators"""
        
        # Extract key metrics
        geometric = statistical_metrics.get("geometric_similarity", {})
        correlation = statistical_metrics.get("dimensional_correlation", {})
        hypothesis = statistical_metrics.get("hypothesis_testing", {})
        
        mean_distance = geometric.get("mean_distance", 1.0)
        correlation_matrix = correlation.get("correlation_matrix", [[]])
        
        # Calculate overall similarity score
        similarity_classification = self._classify_similarity_level(statistical_metrics, experiment_def)
        
        # Generate traffic light indicators
        indicators = []
        
        # Geometric Similarity Indicator
        if mean_distance <= 0.15:
            geo_status = "green"
            geo_text = "Highly Similar"
            geo_icon = "🟢"
        elif mean_distance <= 0.35:
            geo_status = "yellow"
            geo_text = "Moderately Similar"
            geo_icon = "🟡"
        else:
            geo_status = "red"
            geo_text = "Different"
            geo_icon = "🔴"
        
        indicators.append(f"""
        <div class="indicator-card {geo_status}">
            <div class="indicator-icon">{geo_icon}</div>
            <div class="indicator-content">
                <h4>Geometric Similarity</h4>
                <p class="indicator-value">{mean_distance:.3f}</p>
                <p class="indicator-status">{geo_text}</p>
            </div>
        </div>
        """)
        
        # Correlation Indicator
        if correlation_matrix and len(correlation_matrix) > 1:
            correlations = []
            for i in range(len(correlation_matrix)):
                for j in range(len(correlation_matrix[i])):
                    if i != j:
                        correlations.append(correlation_matrix[i][j])
            avg_correlation = sum(correlations) / len(correlations) if correlations else 0.0
            
            if avg_correlation >= 0.85:
                corr_status = "green"
                corr_text = "High Correlation"
                corr_icon = "🟢"
            elif avg_correlation >= 0.65:
                corr_status = "yellow"
                corr_text = "Moderate Correlation"
                corr_icon = "🟡"
            else:
                corr_status = "red"
                corr_text = "Low Correlation"
                corr_icon = "🔴"
            
            indicators.append(f"""
            <div class="indicator-card {corr_status}">
                <div class="indicator-icon">{corr_icon}</div>
                <div class="indicator-content">
                    <h4>Score Correlation</h4>
                    <p class="indicator-value">{avg_correlation:.3f}</p>
                    <p class="indicator-status">{corr_text}</p>
                </div>
            </div>
            """)
        
        # Hypothesis Testing Indicator
        significant_differences = 0
        total_comparisons = 0
        for comparison, results in hypothesis.items():
            if isinstance(results, dict):
                total_comparisons += 1
                if not results.get("overall_similar", True):
                    significant_differences += 1
        
        if significant_differences == 0:
            hyp_status = "green"
            hyp_text = "No Significant Differences"
            hyp_icon = "🟢"
        elif significant_differences <= total_comparisons * 0.3:
            hyp_status = "yellow"
            hyp_text = "Some Differences"
            hyp_icon = "🟡"
        else:
            hyp_status = "red"
            hyp_text = "Significant Differences"
            hyp_icon = "🔴"
        
        indicators.append(f"""
        <div class="indicator-card {hyp_status}">
            <div class="indicator-icon">{hyp_icon}</div>
            <div class="indicator-content">
                <h4>Statistical Tests</h4>
                <p class="indicator-value">{significant_differences}/{total_comparisons}</p>
                <p class="indicator-status">{hyp_text}</p>
            </div>
        </div>
        """)
        
        # Overall Classification
        if similarity_classification == "HIGHLY_SIMILAR":
            overall_status = "green"
            overall_text = "Models are Highly Similar"
            overall_icon = "🎯"
        elif similarity_classification == "MODERATELY_SIMILAR":
            overall_status = "yellow"
            overall_text = "Models are Moderately Similar"
            overall_icon = "⚖️"
        else:
            overall_status = "red"
            overall_text = "Models are Statistically Different"
            overall_icon = "❗"
        
        indicators.append(f"""
        <div class="indicator-card overall {overall_status}">
            <div class="indicator-icon">{overall_icon}</div>
            <div class="indicator-content">
                <h4>Overall Assessment</h4>
                <p class="indicator-status">{overall_text}</p>
            </div>
        </div>
        """)
        
        return "".join(indicators)

    def _generate_accessible_statistical_summary(self, statistical_metrics: Dict[str, Any]) -> Dict[str, str]:
        """Generate accessible statistical summary for non-experts"""
        
        summary = {}
        
        # Executive findings
        geometric = statistical_metrics.get("geometric_similarity", {})
        correlation = statistical_metrics.get("dimensional_correlation", {})
        hypothesis = statistical_metrics.get("hypothesis_testing", {})
        effect_size = statistical_metrics.get("effect_size_analysis", {})
        
        findings = []
        
        mean_distance = geometric.get("mean_distance", 1.0)
        if mean_distance <= 0.15:
            findings.append("✅ Models show <strong>high geometric similarity</strong> - they place texts in very similar positions on the moral framework.")
        elif mean_distance <= 0.35:
            findings.append("⚠️ Models show <strong>moderate geometric similarity</strong> - they generally agree but have some differences in text positioning.")
        else:
            findings.append("❌ Models show <strong>significant geometric differences</strong> - they place texts in notably different positions.")
        
        # Correlation findings
        if correlation.get("correlation_matrix"):
            avg_corr = self._calculate_average_correlation(correlation["correlation_matrix"])
            if avg_corr >= 0.85:
                findings.append("✅ Models show <strong>high score correlation</strong> - they assign very similar moral foundation scores.")
            elif avg_corr >= 0.65:
                findings.append("⚠️ Models show <strong>moderate score correlation</strong> - they generally agree on moral foundation strengths.")
            else:
                findings.append("❌ Models show <strong>low score correlation</strong> - they disagree on which moral foundations are most important.")
        
        summary["executive_findings"] = "<ul>" + "".join(f"<li>{finding}</li>" for finding in findings) + "</ul>"
        
        # Accessible summary
        accessible_parts = []
        
        accessible_parts.append(f"""
        <div class="stat-card">
            <h4>🎯 Model Agreement</h4>
            <p>Average distance between model results: <strong>{mean_distance:.3f}</strong></p>
            <p class="explanation">Lower numbers mean models agree more. Values below 0.15 indicate high agreement.</p>
        </div>
        """)
        
        if effect_size:
            effect_interpretations = []
            for comparison, results in effect_size.items():
                if isinstance(results, dict):
                    overall_effect = results.get("overall_effect_size", 0.0)
                    if overall_effect < 0.2:
                        effect_interpretations.append(f"{comparison}: negligible difference")
                    elif overall_effect < 0.5:
                        effect_interpretations.append(f"{comparison}: small difference")
                    elif overall_effect < 0.8:
                        effect_interpretations.append(f"{comparison}: medium difference")
                    else:
                        effect_interpretations.append(f"{comparison}: large difference")
            
            if effect_interpretations:
                accessible_parts.append(f"""
                <div class="stat-card">
                    <h4>📏 Effect Sizes</h4>
                    <ul>
                        {''.join(f'<li>{interp}</li>' for interp in effect_interpretations)}
                    </ul>
                    <p class="explanation">Effect sizes measure how meaningful the differences are, beyond just statistical significance.</p>
                </div>
                """)
        
        summary["accessible_summary"] = "".join(accessible_parts)
        
        # Correlation interpretation
        if correlation.get("correlation_matrix"):
            model_names = correlation.get("model_names", [])
            corr_matrix = correlation["correlation_matrix"]
            
            corr_text = f"""
            <p>The correlation matrix shows how similarly each pair of models scored the texts:</p>
            <ul>
            """
            
            for i in range(len(model_names)):
                for j in range(i+1, len(model_names)):
                    if i < len(corr_matrix) and j < len(corr_matrix[i]):
                        corr_value = corr_matrix[i][j]
                        model1, model2 = model_names[i], model_names[j]
                        if corr_value >= 0.8:
                            corr_text += f"<li><strong>{model1}</strong> and <strong>{model2}</strong>: Very high agreement (r = {corr_value:.3f})</li>"
                        elif corr_value >= 0.6:
                            corr_text += f"<li><strong>{model1}</strong> and <strong>{model2}</strong>: Good agreement (r = {corr_value:.3f})</li>"
                        else:
                            corr_text += f"<li><strong>{model1}</strong> and <strong>{model2}</strong>: Moderate agreement (r = {corr_value:.3f})</li>"
            
            corr_text += "</ul>"
            summary["correlation_interpretation"] = corr_text
        else:
            summary["correlation_interpretation"] = "<p>Correlation analysis not available.</p>"
        
        # Technical details (expandable)
        technical_parts = []
        
        for method_name, method_results in statistical_metrics.items():
            if isinstance(method_results, dict) and "error" not in method_results:
                technical_parts.append(f"""
                <div class="technical-section">
                    <h4>{method_name.replace('_', ' ').title()}</h4>
                    <pre class="technical-data">{json.dumps(method_results, indent=2, default=str)}</pre>
                </div>
                """)
        
        summary["technical_details"] = "".join(technical_parts)
        
        return summary

    def _extract_prompt_documentation(self, experiment_def: Dict[str, Any]) -> str:
        """Extract and format prompt documentation"""
        
        prompt_guidance = experiment_def.get("prompt_guidance", {})
        framework = experiment_def.get("framework", {})
        
        doc_parts = []
        
        # Overview
        doc_parts.append("""
        <div class="prompt-overview">
            <h3>Prompt Overview</h3>
            <p>Understanding the prompt used is crucial for interpreting the results. This section documents the exact instructions given to each LLM.</p>
        </div>
        """)
        
        # Role Definition
        if prompt_guidance.get("role_definition"):
            doc_parts.append(f"""
            <div class="prompt-section">
                <h4>🎭 Role Definition</h4>
                <div class="prompt-content">
                    {prompt_guidance["role_definition"].replace('\n', '<br>')}
                </div>
            </div>
            """)
        
        # Framework Instructions
        if prompt_guidance.get("framework_summary_instructions"):
            doc_parts.append(f"""
            <div class="prompt-section">
                <h4>📊 Framework Instructions</h4>
                <div class="prompt-content">
                    {prompt_guidance["framework_summary_instructions"].replace('\n', '<br>')}
                </div>
            </div>
            """)
        
        # Methodology
        if prompt_guidance.get("analysis_methodology"):
            doc_parts.append(f"""
            <div class="prompt-section">
                <h4>🔬 Analysis Methodology</h4>
                <div class="prompt-content">
                    {prompt_guidance["analysis_methodology"].replace('\n', '<br>')}
                </div>
            </div>
            """)
        
        # Scoring Requirements
        if prompt_guidance.get("scoring_requirements"):
            doc_parts.append(f"""
            <div class="prompt-section">
                <h4>📏 Scoring Requirements</h4>
                <div class="prompt-content">
                    {prompt_guidance["scoring_requirements"].replace('\n', '<br>')}
                </div>
            </div>
            """)
        
        # Framework Details
        if framework.get("axes"):
            doc_parts.append("""
            <div class="prompt-section">
                <h4>🗺️ Framework Structure</h4>
                <p>The Moral Foundations Theory framework used includes the following dimensions:</p>
                <div class="framework-grid">
            """)
            
            for axis_name, axis_info in framework["axes"].items():
                integrative = axis_info.get("integrative", {})
                doc_parts.append(f"""
                <div class="framework-card">
                    <h5>{integrative.get('name', axis_name)}</h5>
                    <p>{integrative.get('description', 'No description')}</p>
                </div>
                """)
            
            doc_parts.append("</div></div>")
        
        # JSON Format
        if prompt_guidance.get("json_format_instructions"):
            doc_parts.append(f"""
            <div class="prompt-section">
                <h4>💻 Response Format</h4>
                <div class="prompt-content">
                    {prompt_guidance["json_format_instructions"].replace('\n', '<br>')}
                </div>
            </div>
            """)
        
        return "".join(doc_parts)

    def _get_enhanced_statistical_styles(self) -> str:
        """Return enhanced CSS styles for statistical reports"""
        return """
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f8f9fa;
            margin: 0;
            padding: 20px;
        }
        
        .report-container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .report-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }
        
        .report-header h1 {
            margin: 0 0 10px 0;
            font-size: 2.5em;
            font-weight: 300;
        }
        
        .report-header h2 {
            margin: 0 0 20px 0;
            font-size: 1.3em;
            opacity: 0.9;
        }
        
        .report-meta {
            display: flex;
            justify-content: center;
            gap: 30px;
            flex-wrap: wrap;
            opacity: 0.8;
        }
        
        section {
            padding: 40px;
            border-bottom: 1px solid #eee;
        }
        
        section:last-child {
            border-bottom: none;
        }
        
        .similarity-dashboard {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }
        
        .indicator-card {
            padding: 20px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            gap: 15px;
            border: 2px solid;
            transition: transform 0.2s;
        }
        
        .indicator-card:hover {
            transform: translateY(-2px);
        }
        
        .indicator-card.green {
            background: #f0f9f0;
            border-color: #4caf50;
        }
        
        .indicator-card.yellow {
            background: #fffdf0;
            border-color: #ff9800;
        }
        
        .indicator-card.red {
            background: #fff0f0;
            border-color: #f44336;
        }
        
        .indicator-card.overall {
            grid-column: 1 / -1;
            font-weight: bold;
        }
        
        .indicator-icon {
            font-size: 2em;
        }
        
        .indicator-content h4 {
            margin: 0 0 5px 0;
            font-size: 1.1em;
        }
        
        .indicator-value {
            font-size: 1.5em;
            font-weight: bold;
            margin: 5px 0;
        }
        
        .indicator-status {
            margin: 0;
            font-size: 0.9em;
        }
        
        .stat-card {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin: 15px 0;
            border-left: 4px solid #667eea;
        }
        
        .stat-card h4 {
            margin: 0 0 10px 0;
            color: #667eea;
        }
        
        .explanation {
            font-size: 0.9em;
            color: #666;
            font-style: italic;
        }
        
        .model-summary-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }
        
        .model-card {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 12px;
            border: 1px solid #dee2e6;
        }
        
        .model-card h4 {
            margin: 0 0 15px 0;
            color: #495057;
            border-bottom: 2px solid #667eea;
            padding-bottom: 5px;
        }
        
        .model-charts-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 30px;
            margin: 30px 0;
        }
        
        .chart-container {
            background: white;
            border-radius: 8px;
            padding: 20px;
            border: 1px solid #dee2e6;
            margin: 20px 0;
        }
        
        .technical-details {
            margin: 30px 0;
            border: 1px solid #dee2e6;
            border-radius: 8px;
        }
        
        .technical-details summary {
            padding: 20px;
            background: #f8f9fa;
            cursor: pointer;
            font-weight: bold;
            border-radius: 8px 8px 0 0;
        }
        
        .technical-details[open] summary {
            border-bottom: 1px solid #dee2e6;
        }
        
        .technical-section {
            padding: 20px;
            border-bottom: 1px solid #eee;
        }
        
        .technical-section:last-child {
            border-bottom: none;
        }
        
        .technical-data {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 4px;
            overflow-x: auto;
            font-size: 0.9em;
        }
        
        .prompt-section {
            margin: 25px 0;
            border-left: 4px solid #667eea;
            padding-left: 20px;
        }
        
        .prompt-section h4 {
            color: #667eea;
            margin: 0 0 15px 0;
        }
        
        .prompt-content {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 6px;
            font-family: 'Georgia', serif;
            line-height: 1.8;
        }
        
        .framework-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        
        .framework-card {
            background: #fff;
            padding: 15px;
            border-radius: 8px;
            border: 1px solid #dee2e6;
        }
        
        .framework-card h5 {
            margin: 0 0 10px 0;
            color: #667eea;
        }
        
        .json-display {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 6px;
            overflow-x: auto;
            max-height: 400px;
            overflow-y: auto;
        }
        
        .key-findings ul {
            list-style: none;
            padding: 0;
        }
        
        .key-findings li {
            padding: 10px 0;
            border-bottom: 1px solid #eee;
        }
        
        .key-findings li:last-child {
            border-bottom: none;
        }
        """

    def _calculate_average_centroid(self, centroids):
        """Calculate average centroid from list"""
        if not centroids:
            return (0.0, 0.0)
        
        avg_x = sum(c[0] for c in centroids) / len(centroids)
        avg_y = sum(c[1] for c in centroids) / len(centroids)
        return (avg_x, avg_y)

    def _calculate_average_scores(self, scores_list):
        """Calculate average scores from list of score dictionaries"""
        if not scores_list:
            return {}
        
        all_keys = set()
        for scores in scores_list:
            all_keys.update(scores.keys())
        
        avg_scores = {}
        for key in all_keys:
            values = [scores.get(key, 0.0) for scores in scores_list]
            avg_scores[key] = sum(values) / len(values)
        
        return avg_scores

    def _calculate_score_variance(self, scores_list):
        """Calculate variance in scores across texts"""
        if len(scores_list) < 2:
            return {}
        
        import numpy as np
        
        all_keys = set()
        for scores in scores_list:
            all_keys.update(scores.keys())
        
        variances = {}
        for key in all_keys:
            values = [scores.get(key, 0.0) for scores in scores_list]
            variances[key] = float(np.var(values))
        
        return variances

    def _calculate_average_correlation(self, correlation_matrix):
        """Calculate average correlation excluding diagonal"""
        if not correlation_matrix or len(correlation_matrix) < 2:
            return 0.0
        
        correlations = []
        for i in range(len(correlation_matrix)):
            for j in range(len(correlation_matrix[i])):
                if i != j:
                    correlations.append(correlation_matrix[i][j])
        
        return sum(correlations) / len(correlations) if correlations else 0.0

    def _classify_similarity_level(self, statistical_metrics, experiment_def):
        """Classify similarity level for traffic lights"""
        # This duplicates the logic from the API but ensures consistency
        geometric = statistical_metrics.get("geometric_similarity", {})
        mean_distance = geometric.get("mean_distance", 1.0)
        
        if mean_distance <= 0.15:
            return "HIGHLY_SIMILAR"
        elif mean_distance <= 0.35:
            return "MODERATELY_SIMILAR"
        else:
            return "STATISTICALLY_DIFFERENT"

    def _generate_model_summary_cards(self, model_summaries: Dict[str, Any]) -> str:
        """Generate summary cards for each model"""
        cards = []
        
        for model, summary in model_summaries.items():
            avg_centroid = summary["average_centroid"]
            total_texts = summary["total_texts"]
            avg_scores = summary["average_scores"]
            
            # Find top scoring moral foundation
            if avg_scores:
                top_foundation = max(avg_scores.items(), key=lambda x: x[1])
                top_foundation_text = f"<strong>{top_foundation[0]}</strong>: {top_foundation[1]:.3f}"
            else:
                top_foundation_text = "No data"
            
            # Calculate score range
            if avg_scores:
                min_score = min(avg_scores.values())
                max_score = max(avg_scores.values())
                score_range = max_score - min_score
            else:
                score_range = 0.0
            
            cards.append(f"""
            <div class="model-card">
                <h4>{model.replace('_', ' ').title()}</h4>
                <div class="model-stats">
                    <p><strong>Texts Analyzed:</strong> {total_texts}</p>
                    <p><strong>Average Position:</strong> ({avg_centroid[0]:.3f}, {avg_centroid[1]:.3f})</p>
                    <p><strong>Top Foundation:</strong> {top_foundation_text}</p>
                    <p><strong>Score Range:</strong> {score_range:.3f}</p>
                </div>
            </div>
            """)
        
        return "".join(cards)

    def _generate_model_charts_html(self, model_charts: Dict[str, str]) -> str:
        """Generate HTML containers for individual model charts"""
        charts_html = []
        
        for model, chart_data in model_charts.items():
            charts_html.append(f"""
            <div class="model-chart-container">
                <h4>{model.replace('_', ' ').title()} Analysis</h4>
                <div id="model-chart-{model.replace('-', '_').replace('.', '_')}" class="chart-container"></div>
            </div>
            """)
        
        return "".join(charts_html)

    def _generate_model_charts_scripts(self, model_charts: Dict[str, str]) -> str:
        """Generate JavaScript for rendering individual model charts"""
        scripts = []
        
        for model, chart_script in model_charts.items():
            scripts.append(chart_script)
        
        return "".join(scripts)

    def _create_model_summary_chart(self, model: str, summary: Dict[str, Any], anchors: List[Dict], results: List[Dict]) -> str:
        """Create a summary chart for an individual model"""
        
        try:
            # Create scatter plot showing individual text positions with average centroid highlighted
            avg_centroid = summary["average_centroid"]
            
            # Individual text positions
            x_coords = [r["centroid"][0] for r in results]
            y_coords = [r["centroid"][1] for r in results]
            text_ids = [r["text_id"] for r in results]
            
            # Generate the chart script
            chart_id = f"model-chart-{model.replace('-', '_').replace('.', '_')}"
            
            script = f"""
            Plotly.newPlot('{chart_id}', [
                {{
                    x: {x_coords},
                    y: {y_coords},
                    mode: 'markers',
                    type: 'scatter',
                    name: 'Individual Texts',
                    text: {text_ids},
                    marker: {{
                        size: 8,
                        color: 'rgba(100, 150, 255, 0.6)',
                        line: {{ color: 'rgba(100, 150, 255, 1)', width: 1 }}
                    }},
                    hovertemplate: '<b>%{{text}}</b><br>Position: (%{{x:.3f}}, %{{y:.3f}})<extra></extra>'
                }},
                {{
                    x: [{avg_centroid[0]}],
                    y: [{avg_centroid[1]}],
                    mode: 'markers',
                    type: 'scatter',
                    name: 'Average Position',
                    marker: {{
                        size: 15,
                        color: 'red',
                        symbol: 'star',
                        line: {{ color: 'darkred', width: 2 }}
                    }},
                    hovertemplate: '<b>Average Position</b><br>Centroid: (%{{x:.3f}}, %{{y:.3f}})<extra></extra>'
                }}
            ], {{
                title: {{
                    text: '{model.replace("_", " ").title()} - Text Positioning',
                    font: {{ size: 16 }}
                }},
                xaxis: {{ 
                    title: 'X Coordinate',
                    range: [-1.1, 1.1],
                    zeroline: true,
                    zerolinewidth: 1,
                    zerolinecolor: 'lightgray'
                }},
                yaxis: {{ 
                    title: 'Y Coordinate',
                    range: [-1.1, 1.1],
                    zeroline: true,
                    zerolinewidth: 1,
                    zerolinecolor: 'lightgray'
                }},
                showlegend: true,
                width: 500,
                height: 400,
                margin: {{ t: 40, b: 40, l: 40, r: 40 }}
            }});
            """
            
            return script
            
        except Exception as e:
            return f"console.error('Error creating chart for {model}: {str(e)}');"

    def _create_model_comparison_overview_chart(self, model_summaries: Dict[str, Any], anchors: List[Dict]) -> str:
        """Create overview chart comparing all models"""
        
        try:
            # Extract model data
            models = list(model_summaries.keys())
            x_coords = [summary["average_centroid"][0] for summary in model_summaries.values()]
            y_coords = [summary["average_centroid"][1] for summary in model_summaries.values()]
            
            # Color scheme for different models
            colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD']
            model_colors = {model: colors[i % len(colors)] for i, model in enumerate(models)}
            
            script = f"""
            Plotly.newPlot('comparison-overview-chart', [
                {{
                    x: {x_coords},
                    y: {y_coords},
                    mode: 'markers+text',
                    type: 'scatter',
                    text: {[model.replace('_', ' ').title() for model in models]},
                    textposition: 'top center',
                    marker: {{
                        size: 20,
                        color: {[model_colors[model] for model in models]},
                        line: {{ color: 'white', width: 2 }},
                        symbol: 'circle'
                    }},
                    hovertemplate: '<b>%{{text}}</b><br>Average Position: (%{{x:.3f}}, %{{y:.3f}})<extra></extra>',
                    showlegend: false
                }}
            ], {{
                title: {{
                    text: 'Model Comparison: Average Positions Across Corpus',
                    font: {{ size: 18 }}
                }},
                xaxis: {{ 
                    title: 'X Coordinate',
                    range: [-1.1, 1.1],
                    zeroline: true,
                    zerolinewidth: 2,
                    zerolinecolor: 'lightgray',
                    gridcolor: 'lightgray'
                }},
                yaxis: {{ 
                    title: 'Y Coordinate', 
                    range: [-1.1, 1.1],
                    zeroline: true,
                    zerolinewidth: 2,
                    zerolinecolor: 'lightgray',
                    gridcolor: 'lightgray'
                }},
                plot_bgcolor: 'white',
                width: 600,
                height: 500,
                margin: {{ t: 60, b: 60, l: 60, r: 60 }}
            }});
            """
            
            return script
            
        except Exception as e:
            return f"console.error('Error creating comparison overview chart: {str(e)}');"

    def _create_correlation_heatmap(self, statistical_metrics: Dict[str, Any]) -> str:
        """Create correlation heatmap visualization"""
        
        try:
            correlation_data = statistical_metrics.get("dimensional_correlation", {})
            correlation_matrix = correlation_data.get("correlation_matrix", [])
            model_names = correlation_data.get("model_names", [])
            
            if not correlation_matrix or not model_names:
                return "console.log('No correlation data available for heatmap');"
            
            # Clean model names for display
            display_names = [name.replace('_', ' ').title() for name in model_names]
            
            script = f"""
            Plotly.newPlot('correlation-heatmap', [{{
                z: {correlation_matrix},
                x: {display_names},
                y: {display_names},
                type: 'heatmap',
                colorscale: 'RdYlBu',
                reversescale: true,
                zmin: -1,
                zmax: 1,
                text: {[[f"{val:.3f}" for val in row] for row in correlation_matrix]},
                texttemplate: "%{{text}}",
                textfont: {{ size: 12 }},
                hovertemplate: '<b>%{{y}}</b> vs <b>%{{x}}</b><br>Correlation: %{{z:.3f}}<extra></extra>'
            }}], {{
                title: {{
                    text: 'Cross-Model Score Correlation Matrix',
                    font: {{ size: 16 }}
                }},
                xaxis: {{ 
                    title: 'Model',
                    side: 'bottom'
                }},
                yaxis: {{ 
                    title: 'Model',
                    autorange: 'reversed'
                }},
                width: 500,
                height: 400,
                margin: {{ t: 40, b: 80, l: 80, r: 40 }}
            }});
            """
            
            return script
            
        except Exception as e:
            return f"console.error('Error creating correlation heatmap: {str(e)}');"

    def _generate_corpus_characteristics(self, model_groups: Dict[str, List], experiment_def: Dict[str, Any]) -> str:
        """Generate corpus characteristics section"""
        
        corpus_config = experiment_def.get("corpus", {})
        
        # Calculate corpus statistics
        all_text_ids = set()
        category_counts = {}
        
        for model, results in model_groups.items():
            for result in results:
                text_id = result["text_id"]
                all_text_ids.add(text_id)
                
                # Extract category from text_id or result if available
                category = result.get("category", "unknown")
                if category not in category_counts:
                    category_counts[category] = 0
                category_counts[category] += 1
        
        # Normalize category counts (divide by number of models)
        num_models = len(model_groups)
        for category in category_counts:
            category_counts[category] = category_counts[category] // num_models
        
        corpus_info = f"""
        <div class="corpus-overview">
            <h3>Corpus Overview</h3>
            <div class="corpus-stats">
                <div class="stat-card">
                    <h4>📊 Dataset Statistics</h4>
                    <p><strong>Total Texts:</strong> {len(all_text_ids)}</p>
                    <p><strong>Models Analyzed:</strong> {num_models}</p>
                    <p><strong>Total Analyses:</strong> {sum(len(results) for results in model_groups.values())}</p>
                    <p><strong>Source:</strong> {corpus_config.get('file_path', 'Unknown')}</p>
                </div>
                
                <div class="stat-card">
                    <h4>📁 Category Distribution</h4>
                    <ul>
        """
        
        for category, count in sorted(category_counts.items()):
            corpus_info += f"<li><strong>{category.replace('_', ' ').title()}:</strong> {count} texts</li>"
        
        corpus_info += """
                    </ul>
                </div>
            </div>
        </div>
        
        <div class="methodology-note">
            <h3>Sampling Strategy</h3>
            <p>This analysis used a <strong>stratified sampling</strong> approach across political discourse categories 
            to ensure representative coverage of different rhetorical styles and moral framings. Each text was 
            analyzed by all models using identical prompts and scoring criteria.</p>
        </div>
        """
        
        return corpus_info
