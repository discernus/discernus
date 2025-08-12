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
    rich_log_context: List[str] = None  # Enhanced context from log files
    
    def __post_init__(self):
        if self.rich_log_context is None:
            self.rich_log_context = []
    
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
        
    def collect_metrics_from_project(self, project_path: Path, rolling_window: int = 3) -> Dict[str, ComponentMetrics]:
        """
        Collect telemetry metrics from the last N runs in a project (rolling window).
        
        Args:
            project_path: Path to specific project directory
            rolling_window: Number of most recent runs to analyze (default: 3)
            
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
            'last_execution': None,
            'rich_log_context': []  # Enhanced context from log files
        })
        
        # Get sorted list of run directories (newest first)
        run_dirs = []
        for run_dir in runs_dir.iterdir():
            if run_dir.is_dir() and run_dir.name.replace('T', '').replace('Z', '').isdigit():
                # Extract timestamp from directory name (format: YYYYMMDDTHHMMSSZ)
                try:
                    timestamp = run_dir.name.replace('T', '').replace('Z', '')
                    run_dirs.append((timestamp, run_dir))
                except ValueError:
                    continue
        
        # Sort by timestamp (newest first) and take only the last N runs
        run_dirs.sort(key=lambda x: x[0], reverse=True)
        recent_runs = run_dirs[:rolling_window]
        
        # Process only the recent run directories
        for timestamp, run_dir in recent_runs:
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
            
            # Process LLM interaction logs
            llm_log = logs_dir / "llm_interactions.jsonl"
            if llm_log.exists():
                self._process_llm_interactions_log(llm_log, component_data)
            
            # Enhanced: Process rich log files for detailed failure context
            self._process_rich_log_files(logs_dir, component_data, timestamp)
        
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
                    last_execution=data['last_execution'] or "unknown",
                    rich_log_context=data['rich_log_context'] # Pass the collected context
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
    
    def _process_llm_interactions_log(self, log_file: Path, component_data: Dict) -> None:
        """Process LLM interaction log file for telemetry data."""
        try:
            with open(log_file, 'r') as f:
                for line in f:
                    try:
                        entry = json.loads(line.strip())
                        self._extract_llm_interaction_metrics(entry, component_data)
                    except json.JSONDecodeError:
                        continue
        except Exception:
            pass  # Skip problematic log files
    
    def _extract_llm_interaction_metrics(self, entry: Dict, component_data: Dict) -> None:
        """Extract metrics from LLM interaction log entry."""
        if entry.get('log_type') != 'llm_interaction':
            return
        
        agent_name = entry.get('agent_name', 'unknown_agent')
        model = entry.get('model', 'unknown_model')
        timestamp = entry.get('timestamp', '')
        metadata = entry.get('metadata', {})
        
        # Create component key that includes LLM context
        llm_component = f"{agent_name}_llm_interactions"
        
        # Track LLM interaction metrics
        component_data[llm_component]['total'] += 1
        component_data[llm_component]['last_execution'] = timestamp
        
        # Determine success/failure based on metadata
        success = metadata.get('success', True)  # Default to success if not specified
        
        if success:
            component_data[llm_component]['successful'] += 1
        else:
            component_data[llm_component]['failed'] += 1
            error_msg = metadata.get('error', 'llm_interaction_failure')
            component_data[llm_component]['errors'].append(f"llm_call:{error_msg[:100]}")
        
        # Add rich context for LLM interactions
        interaction_context = [
            f"Model: {model}",
            f"Interaction: {entry.get('interaction_type', 'unknown')}",
            f"Prompt length: {entry.get('prompt_length', 0)} chars",
            f"Response length: {entry.get('response_length', 0)} chars"
        ]
        
        # Add cost and token information if available
        if 'cost_usd' in metadata:
            interaction_context.append(f"Cost: ${metadata['cost_usd']:.4f}")
        if 'total_tokens' in metadata:
            interaction_context.append(f"Tokens: {metadata['total_tokens']}")
        
        component_data[llm_component]['rich_log_context'].extend(interaction_context)
        
        # Track model-specific metrics
        model_component = f"llm_model_{model.replace('/', '_').replace('-', '_')}"
        component_data[model_component]['total'] += 1
        component_data[model_component]['last_execution'] = timestamp
        
        if success:
            component_data[model_component]['successful'] += 1
        else:
            component_data[model_component]['failed'] += 1
            component_data[model_component]['errors'].append(f"model_call:{model}")
    
    def _process_rich_log_files(self, logs_dir: Path, component_data: Dict, timestamp: str) -> None:
        """
        Process rich log files (application.log, errors.log, performance.log) for enhanced context.
        
        Args:
            logs_dir: Path to logs directory
            component_data: Component data dictionary to update
            timestamp: Timestamp of the run
        """
        # Process errors.log first for concise error information
        errors_log = logs_dir / "errors.log"
        if errors_log.exists() and errors_log.stat().st_size > 0:
            self._process_errors_log(errors_log, component_data, timestamp)
        
        # Process application.log for detailed execution context
        application_log = logs_dir / "application.log"
        if application_log.exists():
            self._process_application_log(application_log, component_data, timestamp)
        
        # Process performance.log for timing and resource information
        performance_log = logs_dir / "performance.log"
        if performance_log.exists() and performance_log.stat().st_size > 0:
            self._process_performance_log(performance_log, component_data, timestamp)
    
    def _process_errors_log(self, errors_log: Path, component_data: Dict, timestamp: str) -> None:
        """Process errors.log for specific error context."""
        try:
            with open(errors_log, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    
                    # Look for error patterns that indicate component failures
                    if "statistical_validation" in line.lower():
                        component_data['statistical_validation']['errors'].append(f"errors_log:{line}")
                        component_data['statistical_validation']['rich_log_context'].append(f"ERROR: {line}")
                    
                    if "dimension_validation" in line.lower():
                        component_data['dimension_validation']['errors'].append(f"errors_log:{line}")
                        component_data['dimension_validation']['rich_log_context'].append(f"ERROR: {line}")
                    
                    if "synthesis" in line.lower() and ("error" in line.lower() or "failed" in line.lower()):
                        component_data['SequentialSynthesisAgent']['errors'].append(f"errors_log:{line}")
                        component_data['SequentialSynthesisAgent']['rich_log_context'].append(f"ERROR: {line}")
                    
                    if "analysis" in line.lower() and ("error" in line.lower() or "failed" in line.lower()):
                        component_data['EnhancedAnalysisAgent']['errors'].append(f"errors_log:{line}")
                        component_data['EnhancedAnalysisAgent']['rich_log_context'].append(f"ERROR: {line}")
                        
        except Exception:
            pass  # Skip problematic log files
    
    def _process_application_log(self, application_log: Path, component_data: Dict, timestamp: str) -> None:
        """Process application.log for detailed execution context."""
        try:
            with open(application_log, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    
                    # Look for specific failure patterns in application logs
                    if "statistical_validation" in line.lower():
                        if "failed" in line.lower() or "error" in line.lower():
                            component_data['statistical_validation']['errors'].append(f"application_log:{line}")
                            component_data['statistical_validation']['rich_log_context'].append(f"CONTEXT: {line}")
                    
                    if "synthesis" in line.lower() and "failed" in line.lower():
                        component_data['SequentialSynthesisAgent']['errors'].append(f"application_log:{line}")
                        component_data['SequentialSynthesisAgent']['rich_log_context'].append(f"CONTEXT: {line}")
                    
                    if "analysis" in line.lower() and "failed" in line.lower():
                        component_data['EnhancedAnalysisAgent']['errors'].append(f"application_log:{line}")
                        component_data['EnhancedAnalysisAgent']['rich_log_context'].append(f"CONTEXT: {line}")
                    
                    # Look for stage transitions that might indicate where failures occur
                    if "stage set to" in line.lower():
                        stage_name = line.split("stage set to")[-1].split("with")[0].strip().strip("'")
                        if stage_name:
                            # Track stage progression to identify failure points
                            for component in component_data.values():
                                component['rich_log_context'].append(f"STAGE: {stage_name}")
                        
        except Exception:
            pass  # Skip problematic log files
    
    def _process_performance_log(self, performance_log: Path, component_data: Dict, timestamp: str) -> None:
        """Process performance.log for timing and resource information."""
        try:
            with open(performance_log, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    
                    # Look for performance issues that might indicate component problems
                    if "timeout" in line.lower() or "slow" in line.lower():
                        # Performance issues can affect any component
                        for component in component_data.values():
                            component['rich_log_context'].append(f"PERFORMANCE: {line}")
                        
        except Exception:
            pass  # Skip problematic log files
    
    def assess_pipeline_health(self, project_path: Path, rolling_window: int = 3) -> PipelineHealth:
        """
        Assess overall pipeline health for a project.
        
        Args:
            project_path: Path to specific project directory
            rolling_window: Number of most recent runs to analyze (default: 3)
            
        Returns:
            PipelineHealth assessment with categorized components
        """
        metrics = self.collect_metrics_from_project(project_path, rolling_window)
        
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
    
    def generate_reliability_report(self, project_path: Path, rolling_window: int = 3) -> str:
        """
        Generate a comprehensive reliability report for developers.
        
        Args:
            project_path: Path to specific project directory
            rolling_window: Number of most recent runs to analyze (default: 3)
            
        Returns:
            Formatted reliability report as string
        """
        metrics = self.collect_metrics_from_project(project_path, rolling_window)
        health = self.assess_pipeline_health(project_path, rolling_window)
        
        report_lines = [
            "# Infrastructure Reliability Report",
            f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}",
            f"Project: {project_path.name}",
            f"Rolling Window: Last {rolling_window} runs",
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
                
                if m.rich_log_context:
                    report_lines.extend([
                        "**Rich Log Context:**",
                        ""
                    ])
                    for context_line in m.rich_log_context:
                        report_lines.append(f"- {context_line}")
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
