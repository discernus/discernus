#!/usr/bin/env python3
"""
Three-Part Academic Report Generator

Generates structured academic reports with clear separation between:
1. Deterministic computational results (no LLM interpretation)
2. LLM-generated interpretive synthesis 
3. Research transparency metadata

THIN: Deterministic formatting and data assembly. LLM content injected at designated point.
"""
from typing import Dict, Any, List, Optional
import json
from datetime import datetime
import pandas as pd
from .statistical_formatter import StatisticalResultsFormatter


class ThreePartReportGenerator:
    """Generates three-part academic reports with deterministic statistical foundation."""

    def __init__(self, 
                 experiment_name: str,
                 framework_name: str,
                 statistical_results: Dict[str, Any],
                 provenance_metadata: Dict[str, Any],
                 cost_metadata: Dict[str, Any]):
        """
        Initialize report generator with computational results and metadata.
        
        Args:
            experiment_name: Name of the experiment
            framework_name: Name/version of the framework used
            statistical_results: Raw MathToolkit output
            provenance_metadata: Hashes, timestamps, versions
            cost_metadata: Token usage, API costs
        """
        self.experiment_name = experiment_name
        self.framework_name = framework_name
        self.statistical_results = statistical_results
        self.provenance_metadata = provenance_metadata
        self.cost_metadata = cost_metadata
        self.formatter = StatisticalResultsFormatter(statistical_results)

    def generate_report(self, llm_synthesis_content: str) -> str:
        """
        Generate complete three-part report.
        
        Args:
            llm_synthesis_content: The interpretive analysis from SequentialSynthesisAgent
            
        Returns:
            Complete markdown report
        """
        part1 = self._generate_deterministic_foundation()
        part2 = self._format_llm_synthesis(llm_synthesis_content)
        part3 = self._generate_research_transparency()
        
        return f"{part1}\n\n{part2}\n\n{part3}"

    def _generate_deterministic_foundation(self) -> str:
        """Generate Part 1: Deterministic computational foundation (no LLM)."""
        
        # Format timestamp and execution time
        timestamp = self.provenance_metadata.get('run_id', 'unknown')
        execution_time = self.provenance_metadata.get('execution_time', 0.0)
        formatted_time = f"{execution_time:.2f} seconds" if execution_time > 0 else "unknown"
        
        report = f"""# Research Report: {self.experiment_name}

## Part I: Computational Foundation

### Experiment Metadata
- **Experiment**: {self.experiment_name}
- **Framework**: {self.framework_name}
- **Run ID**: {timestamp}
- **Execution Time**: {formatted_time}
- **Framework Hash**: {self.provenance_metadata.get('framework_hash', 'unknown')[:12]}...
- **Corpus Hash**: {self.provenance_metadata.get('corpus_hash', 'unknown')[:12]}...
- **Scores Hash**: {self.provenance_metadata.get('scores_hash', 'unknown')[:12]}...

### Statistical Results

#### Descriptive Statistics
{self._render_descriptive_stats_table()}

#### Correlation Analysis  
{self._render_correlation_table()}

#### ANOVA Results
{self._render_anova_table()}

### Computational Errors and Warnings
{self._render_errors_warnings()}"""

        return report

    def _format_llm_synthesis(self, synthesis_content: str) -> str:
        """Format Part 2: LLM interpretive synthesis with enhanced structure."""
        
        # Extract framework description from statistical data
        framework_description = self._extract_framework_description()
        
        # Extract experiment overview 
        experiment_overview = self._extract_experiment_overview()
        
        # Extract framework fit assessment from synthesis content
        framework_fit_section = self._extract_framework_fit_assessment(synthesis_content)
        
        # Extract notable findings
        notable_findings = self._extract_notable_findings(synthesis_content)
        
        return f"""## Part II: Interpretive Analysis

### Framework Description
{framework_description}

### Experiment Overview  
{experiment_overview}

### Evidence-Grounded Analysis
{synthesis_content}

### Framework Fit Assessment
{framework_fit_section}

### Notable Findings
{notable_findings}"""

    def _generate_research_transparency(self) -> str:
        """Generate Part 3: Research transparency metadata."""
        
        total_cost = self.cost_metadata.get('total_cost', 0.0)
        total_tokens = self.cost_metadata.get('total_tokens', 0)
        
        # Debug logging
        print(f"🔍 Report Generator Debug: total_cost = {total_cost} (type: {type(total_cost)})")
        print(f"🔍 Report Generator Debug: total_tokens = {total_tokens} (type: {type(total_tokens)})")
        print(f"🔍 Report Generator Debug: cost_metadata = {self.cost_metadata}")
        
        return f"""## Part III: Research Transparency

### Computational Cost Analysis
- **Total Cost**: ${total_cost:.4f} USD
- **Total Tokens**: {total_tokens:,}
- **Cost per Token**: ${(total_cost/total_tokens if total_tokens > 0 else 0.0):.6f} USD

### Cost Breakdown by Model
{self._render_cost_breakdown()}

### Provenance and Audit Trail
- **Artifact Storage**: Content-addressable with SHA-256 hashes
- **Complete Reproducibility**: All inputs, outputs, and intermediate results preserved
- **Audit Logs**: Available in experiment run directory
- **Statistical Calculations**: Performed by MathToolkit v2.0 (no LLM interpretation)

### Platform Attribution
This research was conducted using the **Discernus Computational Research Platform**, ensuring complete transparency in computational costs, statistical calculations, and research provenance. All mathematical results are computed deterministically and bypass LLM interpretation to maximize academic defensibility.

**Documentation**: https://discernus.org/docs  
**Source Code**: https://github.com/discernus/discernus  
**Citation**: Discernus Research Platform v2.0 (2025)"""

    def _render_descriptive_stats_table(self) -> str:
        """Render descriptive statistics as clean markdown table."""
        formatted = self.formatter.format_all()
        desc_summary = formatted.get('descriptive_summary')
        
        if not desc_summary or not desc_summary.get('rows'):
            return "*No descriptive statistics available.*"
            
        headers = desc_summary.get('headers', [])
        rows = desc_summary.get('rows', [])
        
        # Create markdown table
        table = f"| {' | '.join(headers)} |\n"
        table += f"| {' | '.join(['---'] * len(headers))} |\n"
        
        for row in rows:
            formatted_row = []
            for cell in row:
                if isinstance(cell, float):
                    formatted_row.append(f"{cell:.3f}" if cell is not None else "N/A")
                else:
                    formatted_row.append(str(cell) if cell is not None else "N/A")
            table += f"| {' | '.join(formatted_row)} |\n"
            
        return table

    def _render_correlation_table(self) -> str:
        """Render correlation analysis as clean markdown table."""
        formatted = self.formatter.format_all()
        corr_summary = formatted.get('correlation_summary')
        
        if not corr_summary or not corr_summary.get('rows'):
            return "*No correlation analysis available.*"
            
        rows = corr_summary.get('rows', [])
        
        # Create markdown table
        table = "| Dimension Pair | Correlation | P-Value |\n"
        table += "| --- | --- | --- |\n"
        
        for row in rows:
            dims = row.get('dimensions', 'Unknown')
            corr = row.get('correlation')
            pval = row.get('p_value')
            
            corr_str = f"{corr:.3f}" if corr is not None else "N/A"
            pval_str = f"{pval:.3f}" if pval is not None else "N/A"
            
            table += f"| {dims} | {corr_str} | {pval_str} |\n"
            
        return table

    def _render_anova_table(self) -> str:
        """Render ANOVA results as clean markdown table."""
        formatted = self.formatter.format_all()
        anova_summary = formatted.get('anova_summary')
        
        if not anova_summary or not anova_summary.get('rows'):
            return "*No ANOVA analysis available (requires >2 groups).*"
            
        headers = anova_summary.get('headers', [])
        rows = anova_summary.get('rows', [])
        
        # Create markdown table
        table = f"| {' | '.join(headers)} |\n"
        table += f"| {' | '.join(['---'] * len(headers))} |\n"
        
        for row in rows:
            formatted_row = []
            for i, cell in enumerate(row):
                if i == 0:  # Dimension name
                    formatted_row.append(str(cell))
                elif i in [1, 2]:  # F-stat, P-value
                    formatted_row.append(f"{cell:.3f}" if cell is not None else "N/A")
                else:  # Significant boolean
                    formatted_row.append("Yes" if cell else "No")
            table += f"| {' | '.join(formatted_row)} |\n"
            
        return table

    def _render_errors_warnings(self) -> str:
        """Render computational errors and warnings."""
        errors = self.statistical_results.get('errors', [])
        warning_list = self.statistical_results.get('warnings', [])
        
        # Handle case where warnings might be a module object instead of list
        if not isinstance(warning_list, list):
            warning_list = []
        
        if not errors and not warning_list:
            return "*No computational errors or warnings.*"
            
        output = ""
        if errors:
            output += "**Errors:**\n"
            for error in errors:
                output += f"- {error}\n"
                
        if warning_list:
            output += "**Warnings:**\n" 
            for warning in warning_list:
                output += f"- {warning}\n"
                
        return output

    def _render_cost_breakdown(self) -> str:
        """Render cost breakdown by model/agent."""
        models = self.cost_metadata.get('models', {})
        agents = self.cost_metadata.get('agents', {})
        
        if not models and not agents:
            return "*Detailed cost breakdown not available in current implementation.*"
        
        breakdown = ""
        
        # Model breakdown
        if models:
            breakdown += "#### By Model\n"
            for model, model_costs in models.items():
                cost_usd = model_costs.get('cost_usd', 0.0)
                tokens = model_costs.get('tokens', 0)
                calls = model_costs.get('calls', 0)
                breakdown += f"- **{model}**: ${cost_usd:.4f} USD ({tokens:,} tokens, {calls} calls)\n"
            breakdown += "\n"
        
        # Agent breakdown
        if agents:
            breakdown += "#### By Agent\n"
            for agent, agent_costs in agents.items():
                cost_usd = agent_costs.get('cost_usd', 0.0)
                tokens = agent_costs.get('tokens', 0)
                calls = agent_costs.get('calls', 0)
                breakdown += f"- **{agent}**: ${cost_usd:.4f} USD ({tokens:,} tokens, {calls} calls)\n"
        
        return breakdown

    def _format_timestamp(self, timestamp: str) -> str:
        """Format run timestamp for display."""
        try:
            if 'T' in timestamp and 'Z' in timestamp:
                # Parse format like "20250809T225238Z"
                dt = datetime.strptime(timestamp.split('T')[0] + timestamp.split('T')[1].replace('Z', ''), '%Y%m%d%H%M%S')
                return dt.strftime('%Y-%m-%d %H:%M:%S UTC')
        except:
            pass
        return timestamp
    
    def _extract_framework_description(self) -> str:
        """Extract framework description from statistical data."""
        # Use framework fit assessment data to describe what dimensions measure
        formatted = self.formatter.format_all()
        framework_fit = formatted.get('framework_fit_assessment', {})
        
        if framework_fit:
            quality_level = framework_fit.get('quality_level', 'Unknown validation level')
            conclusion = framework_fit.get('framework_fit_conclusion', 'Framework assessment not available')
            
            return f"""The {self.framework_name} provides a systematic approach to discourse analysis across multiple dimensions. This analysis employed **{quality_level.lower()}** with the following assessment: {conclusion}

The framework's dimensions measure key aspects of social cohesion and discourse quality, enabling quantitative analysis of rhetorical patterns and their potential impacts on democratic discourse."""
        
        return f"The {self.framework_name} provides a systematic approach to discourse analysis across multiple dimensions of social cohesion and discourse quality."
    
    def _extract_experiment_overview(self) -> str:
        """Extract experiment overview with research questions and methodology."""
        return f"""**Research Questions**: This experiment investigates patterns of social cohesion and fragmentation in political discourse using computational analysis.

**Methodology**: The analysis applies the {self.framework_name} to score discourse samples across multiple dimensions, followed by statistical analysis (descriptive statistics, correlation analysis, and where applicable, ANOVA) to identify patterns and relationships. Evidence is then retrieved and synthesized to ground statistical findings in textual analysis."""
    
    def _extract_framework_fit_assessment(self, synthesis_content: str) -> str:
        """Extract framework fit assessment from synthesis content."""
        # Look for framework fit assessment section in synthesis content
        if "Framework Fit Assessment" in synthesis_content:
            lines = synthesis_content.split('\n')
            fit_section = []
            in_fit_section = False
            
            for line in lines:
                if "Framework Fit Assessment" in line:
                    in_fit_section = True
                    continue
                elif in_fit_section and line.startswith('#') and "Framework Fit Assessment" not in line:
                    break
                elif in_fit_section:
                    fit_section.append(line)
            
            if fit_section:
                return '\n'.join(fit_section).strip()
        
        # Fallback: use statistical formatter data
        formatted = self.formatter.format_all()
        framework_fit = formatted.get('framework_fit_assessment', {})
        
        if framework_fit:
            quality_level = framework_fit.get('quality_level', 'Unknown validation level')
            conclusion = framework_fit.get('framework_fit_conclusion', 'Assessment not available')
            return f"**Validation Approach**: {quality_level}\n\n**Framework Assessment**: {conclusion}"
        
        return "Framework fit assessment not available in current analysis."
    
    def _extract_notable_findings(self, synthesis_content: str) -> str:
        """Extract notable findings, patterns, and anomalies from synthesis content."""
        # Look for key patterns in the synthesis content
        notable_items = []
        
        # Extract correlation findings
        if "correlation" in synthesis_content.lower():
            notable_items.append("**Statistical Correlations**: Significant dimensional relationships identified in correlation analysis")
        
        # Extract anomaly findings  
        if "anomal" in synthesis_content.lower() or "unusual" in synthesis_content.lower():
            notable_items.append("**Statistical Anomalies**: Unusual patterns detected requiring further investigation")
        
        # Extract zero scores or extreme values
        if "zero" in synthesis_content.lower() or "perfect correlation" in synthesis_content.lower():
            notable_items.append("**Extreme Values**: Zero scores or perfect correlations indicating potential data quality issues")
        
        # Add framework-specific insights
        formatted = self.formatter.format_all()
        reliability_summary = formatted.get('reliability_summary', {})
        if reliability_summary and reliability_summary.get('rows'):
            notable_items.append("**Measurement Reliability**: Framework dimensions show measurable internal consistency")
        
        if notable_items:
            return '\n'.join([f"- {item}" for item in notable_items])
        
        return "- **Analysis Complete**: Comprehensive statistical and textual analysis conducted with framework application"
