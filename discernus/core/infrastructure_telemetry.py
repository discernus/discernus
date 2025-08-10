#!/usr/bin/env python3
"""
Infrastructure Telemetry System for Discernus THIN v2.0
=======================================================

Provides developer-focused telemetry collection and analysis for infrastructure
reliability monitoring. Integrates with existing AuditLogger to track:
- Component success/failure rates
- Dependency validation results  
- Performance metrics and trends
- Infrastructure health indicators

Enables data-driven reliability improvements and proactive issue detection.
"""

import json
import statistics
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from collections import defaultdict, Counter

from .audit_logger import AuditLogger


@dataclass
class ComponentMetrics:
    """Metrics for a specific infrastructure component."""
    component_name: str
    total_executions: int
    successful_executions: int
    failed_executions: int
    success_rate: float
    average_duration: float
    error_patterns: List[str]
    last_execution: str
    
    @property
    def failure_rate(self) -> float:
        """Calculate failure rate as percentage."""
        return (self.failed_executions / max(self.total_executions, 1)) * 100


@dataclass
class PipelineHealth:
    """Overall pipeline health assessment."""
    overall_success_rate: float
    critical_components: List[str]  # Components with high failure rates
    warning_components: List[str]   # Components with moderate issues
    healthy_components: List[str]   # Components performing well
    total_experiments: int
    total_failures: int
    common_failure_patterns: List[Tuple[str, int]]  # (pattern, count)
    reliability_trend: str  # "improving", "stable", "degrading"


class InfrastructureTelemetry:
    """
    Infrastructure telemetry collection and analysis system.
    
    Analyzes audit logs to provide developer insights into component reliability,
    failure patterns, and infrastructure health trends.
    """
    
    def __init__(self, project_root: Path):
        """
        Initialize telemetry system for a project.
        
        Args:
            project_root: Root path of the Discernus project
        """
        self.project_root = project_root
        self.runs_dir = project_root / "runs"
        
        # Component reliability thresholds
        self.CRITICAL_THRESHOLD = 0.5   # <50% success rate = critical
        self.WARNING_THRESHOLD = 0.8    # <80% success rate = warning
        
    def collect_metrics_from_project(self, project_path: Path) -> Dict[str, ComponentMetrics]:
        """
        Collect telemetry metrics from all runs in a project.
        
        Args:
            project_path: Path to specific project directory
            
        Returns:
            Dictionary mapping component names to their metrics
        """
        runs_dir = project_path / "runs"
        if not runs_dir.exists():
            return {}
        
        component_data = defaultdict(lambda: {
            'total': 0,
            'successful': 0,
            'failed': 0,
            'durations': [],
            'errors': [],
            'last_execution': None
        })
        
        # Process all run directories
        for run_dir in runs_dir.iterdir():
            if not run_dir.is_dir():
                continue
                
            logs_dir = run_dir / "logs"
            if not logs_dir.exists():
                continue
            
            # Process orchestrator logs
            orchestrator_log = logs_dir / "orchestrator.jsonl"
            if orchestrator_log.exists():
                self._process_orchestrator_log(orchestrator_log, component_data)
            
            # Process agent logs
            agent_log = logs_dir / "agents.jsonl"
            if agent_log.exists():
                self._process_agent_log(agent_log, component_data)
        
        # Convert to ComponentMetrics objects
        metrics = {}
        for component_name, data in component_data.items():
            if data['total'] > 0:
                success_rate = data['successful'] / data['total']
                avg_duration = statistics.mean(data['durations']) if data['durations'] else 0.0
                
                metrics[component_name] = ComponentMetrics(
                    component_name=component_name,
                    total_executions=data['total'],
                    successful_executions=data['successful'],
                    failed_executions=data['failed'],
                    success_rate=success_rate,
                    average_duration=avg_duration,
                    error_patterns=list(set(data['errors'])),
                    last_execution=data['last_execution'] or "unknown"
                )
        
        return metrics
    
    def _process_orchestrator_log(self, log_file: Path, component_data: Dict) -> None:
        """Process orchestrator log file for telemetry data."""
        try:
            with open(log_file, 'r') as f:
                for line in f:
                    try:
                        entry = json.loads(line.strip())
                        self._extract_orchestrator_metrics(entry, component_data)
                    except json.JSONDecodeError:
                        continue
        except Exception:
            pass  # Skip problematic log files
    
    def _process_agent_log(self, log_file: Path, component_data: Dict) -> None:
        """Process agent log file for telemetry data."""
        try:
            with open(log_file, 'r') as f:
                for line in f:
                    try:
                        entry = json.loads(line.strip())
                        self._extract_agent_metrics(entry, component_data)
                    except json.JSONDecodeError:
                        continue
        except Exception:
            pass  # Skip problematic log files
    
    def _extract_orchestrator_metrics(self, entry: Dict, component_data: Dict) -> None:
        """Extract metrics from orchestrator log entry."""
        event_type = entry.get('event_type', '')
        timestamp = entry.get('timestamp', '')
        
        # Track dimension validation
        if event_type == 'framework_dimension_validation':
            component = 'dimension_validation'
            component_data[component]['total'] += 1
            component_data[component]['last_execution'] = timestamp
            
            validation_passed = entry.get('event_data', {}).get('validation_passed', False)
            if validation_passed:
                component_data[component]['successful'] += 1
            else:
                component_data[component]['failed'] += 1
                # Extract error pattern
                recommended_action = entry.get('event_data', {}).get('recommended_action', '')
                if recommended_action:
                    component_data[component]['errors'].append(f"dimension_validation:{recommended_action}")
        
        # Track overall experiment success/failure
        elif event_type == 'experiment_start':
            component = 'experiment_execution'
            component_data[component]['total'] += 1
            component_data[component]['last_execution'] = timestamp
        
        elif event_type == 'experiment_complete':
            component = 'experiment_execution'
            component_data[component]['successful'] += 1
        
        elif event_type == 'experiment_failed':
            component = 'experiment_execution'
            component_data[component]['failed'] += 1
            error_msg = entry.get('event_data', {}).get('error_message', 'unknown_error')
            component_data[component]['errors'].append(f"experiment:{error_msg[:100]}")
    
    def _extract_agent_metrics(self, entry: Dict, component_data: Dict) -> None:
        """Extract metrics from agent log entry."""
        agent_name = entry.get('agent_name', 'unknown_agent')
        event_type = entry.get('event_type', '')
        timestamp = entry.get('timestamp', '')
        
        # Track agent-specific events
        if event_type in ['analysis_complete', 'synthesis_complete', 'validation_complete', 'extraction_complete']:
            component_data[agent_name]['total'] += 1
            component_data[agent_name]['last_execution'] = timestamp
            
            # Check for success indicators
            event_data = entry.get('event_data', {})
            success = event_data.get('success', True)  # Default to success if not specified
            
            if success:
                component_data[agent_name]['successful'] += 1
            else:
                component_data[agent_name]['failed'] += 1
                error_msg = event_data.get('error_message', 'agent_failure')
                component_data[agent_name]['errors'].append(f"{agent_name}:{error_msg[:100]}")
            
            # Track duration if available
            duration = event_data.get('duration', event_data.get('execution_time', 0))
            if duration and isinstance(duration, (int, float)):
                component_data[agent_name]['durations'].append(float(duration))
        
        # Track statistical health validation specifically
        elif event_type == 'statistical_health_validation':
            component = 'statistical_validation'
            component_data[component]['total'] += 1
            component_data[component]['last_execution'] = timestamp
            
            validation_passed = entry.get('event_data', {}).get('validation_passed', False)
            if validation_passed:
                component_data[component]['successful'] += 1
            else:
                component_data[component]['failed'] += 1
                recommended_action = entry.get('event_data', {}).get('recommended_action', '')
                component_data[component]['errors'].append(f"statistical_validation:{recommended_action}")
    
    def assess_pipeline_health(self, project_path: Path) -> PipelineHealth:
        """
        Assess overall pipeline health for a project.
        
        Args:
            project_path: Path to specific project directory
            
        Returns:
            PipelineHealth assessment with categorized components
        """
        metrics = self.collect_metrics_from_project(project_path)
        
        if not metrics:
            return PipelineHealth(
                overall_success_rate=0.0,
                critical_components=[],
                warning_components=[],
                healthy_components=[],
                total_experiments=0,
                total_failures=0,
                common_failure_patterns=[],
                reliability_trend="unknown"
            )
        
        # Categorize components by health
        critical_components = []
        warning_components = []
        healthy_components = []
        
        total_executions = 0
        total_successes = 0
        all_errors = []
        
        for component_name, component_metrics in metrics.items():
            total_executions += component_metrics.total_executions
            total_successes += component_metrics.successful_executions
            all_errors.extend(component_metrics.error_patterns)
            
            if component_metrics.success_rate < self.CRITICAL_THRESHOLD:
                critical_components.append(component_name)
            elif component_metrics.success_rate < self.WARNING_THRESHOLD:
                warning_components.append(component_name)
            else:
                healthy_components.append(component_name)
        
        # Calculate overall success rate
        overall_success_rate = total_successes / max(total_executions, 1)
        
        # Analyze common failure patterns
        error_counter = Counter(all_errors)
        common_failure_patterns = error_counter.most_common(5)
        
        # Simple trend analysis (could be enhanced with historical data)
        if overall_success_rate >= 0.9:
            reliability_trend = "stable"
        elif overall_success_rate >= 0.7:
            reliability_trend = "stable"
        else:
            reliability_trend = "degrading"
        
        return PipelineHealth(
            overall_success_rate=overall_success_rate,
            critical_components=critical_components,
            warning_components=warning_components,
            healthy_components=healthy_components,
            total_experiments=total_executions,
            total_failures=total_executions - total_successes,
            common_failure_patterns=common_failure_patterns,
            reliability_trend=reliability_trend
        )
    
    def generate_reliability_report(self, project_path: Path) -> str:
        """
        Generate a comprehensive reliability report for developers.
        
        Args:
            project_path: Path to specific project directory
            
        Returns:
            Formatted reliability report as string
        """
        metrics = self.collect_metrics_from_project(project_path)
        health = self.assess_pipeline_health(project_path)
        
        report_lines = [
            "# Infrastructure Reliability Report",
            f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}",
            f"Project: {project_path.name}",
            "",
            "## Overall Health",
            f"- Success Rate: {health.overall_success_rate:.1%}",
            f"- Total Experiments: {health.total_experiments}",
            f"- Total Failures: {health.total_failures}",
            f"- Reliability Trend: {health.reliability_trend.title()}",
            ""
        ]
        
        # Component health summary
        if health.critical_components:
            report_lines.extend([
                "## 🚨 Critical Components (< 50% success rate)",
                ""
            ])
            for component in health.critical_components:
                if component in metrics:
                    m = metrics[component]
                    report_lines.append(f"- **{component}**: {m.success_rate:.1%} success ({m.failed_executions}/{m.total_executions} failures)")
            report_lines.append("")
        
        if health.warning_components:
            report_lines.extend([
                "## ⚠️ Warning Components (< 80% success rate)",
                ""
            ])
            for component in health.warning_components:
                if component in metrics:
                    m = metrics[component]
                    report_lines.append(f"- **{component}**: {m.success_rate:.1%} success ({m.failed_executions}/{m.total_executions} failures)")
            report_lines.append("")
        
        if health.healthy_components:
            report_lines.extend([
                "## ✅ Healthy Components (≥ 80% success rate)",
                ""
            ])
            for component in health.healthy_components:
                if component in metrics:
                    m = metrics[component]
                    report_lines.append(f"- **{component}**: {m.success_rate:.1%} success ({m.total_executions} executions)")
            report_lines.append("")
        
        # Common failure patterns
        if health.common_failure_patterns:
            report_lines.extend([
                "## 🔍 Common Failure Patterns",
                ""
            ])
            for pattern, count in health.common_failure_patterns:
                report_lines.append(f"- `{pattern}` ({count} occurrences)")
            report_lines.append("")
        
        # Detailed component metrics
        if metrics:
            report_lines.extend([
                "## 📊 Detailed Component Metrics",
                ""
            ])
            
            for component_name, m in sorted(metrics.items()):
                report_lines.extend([
                    f"### {component_name}",
                    f"- Executions: {m.total_executions} total, {m.successful_executions} successful, {m.failed_executions} failed",
                    f"- Success Rate: {m.success_rate:.1%}",
                    f"- Average Duration: {m.average_duration:.2f}s" if m.average_duration > 0 else "- Average Duration: N/A",
                    f"- Last Execution: {m.last_execution}",
                    ""
                ])
                
                if m.error_patterns:
                    report_lines.append("**Recent Error Patterns:**")
                    for error in m.error_patterns[-5:]:  # Show last 5 error patterns
                        report_lines.append(f"- `{error}`")
                    report_lines.append("")
        
        return "\n".join(report_lines)
    
    def get_component_alerts(self, project_path: Path) -> List[str]:
        """
        Get list of alerts for components requiring attention.
        
        Args:
            project_path: Path to specific project directory
            
        Returns:
            List of alert messages for developers
        """
        health = self.assess_pipeline_health(project_path)
        alerts = []
        
        # Critical component alerts
        for component in health.critical_components:
            alerts.append(f"CRITICAL: {component} has < 50% success rate - immediate attention required")
        
        # Warning component alerts  
        for component in health.warning_components:
            alerts.append(f"WARNING: {component} has < 80% success rate - investigation recommended")
        
        # Overall health alerts
        if health.overall_success_rate < 0.5:
            alerts.append(f"CRITICAL: Overall pipeline success rate is {health.overall_success_rate:.1%} - system reliability severely degraded")
        elif health.overall_success_rate < 0.8:
            alerts.append(f"WARNING: Overall pipeline success rate is {health.overall_success_rate:.1%} - reliability improvements needed")
        
        return alerts
