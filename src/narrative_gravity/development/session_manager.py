"""
Development Session Manager for Structured Component Development

Provides systematic session management for iterative development of:
- Prompt templates with performance tracking
- Framework architectures with coherence validation
- Weighting methodologies with mathematical verification

Integrates with Priority 1 CLI infrastructure and database tracking.
"""

import json
import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from src.narrative_gravity.utils.database import get_database_url
from src.narrative_gravity.models.component_models import DevelopmentSession
from .seed_prompts import SeedPromptLibrary, ComponentType


@dataclass
class SessionMetrics:
    """Performance metrics for a development session."""
    coefficient_variation: Optional[float] = None
    hierarchy_clarity_score: Optional[float] = None
    framework_fit_average: Optional[float] = None
    evidence_quality_score: Optional[float] = None
    mathematical_validity: Optional[bool] = None
    custom_metrics: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.custom_metrics is None:
            self.custom_metrics = {}


@dataclass
class SessionIteration:
    """Individual iteration within a development session."""
    iteration_number: int
    timestamp: datetime
    hypothesis: str
    changes_made: str
    test_results: Dict[str, Any]
    performance_metrics: SessionMetrics
    notes: str
    version_created: Optional[str] = None


class DevelopmentSessionManager:
    """
    Manages structured development sessions with systematic tracking.
    
    Provides tools for:
    - Starting sessions with proper initialization
    - Tracking iterations with performance metrics
    - Creating component versions from session outcomes
    - Analyzing development patterns and success factors
    """
    
    def __init__(self, database_url: Optional[str] = None):
        """Initialize session manager with database connection."""
        self.database_url = database_url or get_database_url()
        self.engine = create_engine(self.database_url)
        self.Session = sessionmaker(bind=self.engine)
        self.seed_library = SeedPromptLibrary()
    
    def start_session(self,
                     session_name: str,
                     component_type: str,
                     component_name: str,
                     hypothesis: str,
                     base_version: Optional[str] = None,
                     target_version: Optional[str] = None,
                     researcher_id: Optional[int] = None) -> str:
        """
        Start a new development session with structured initialization.
        
        Args:
            session_name: Descriptive name for the session
            component_type: Type of component (prompt_template, framework, weighting_method)
            component_name: Name of the component being developed
            hypothesis: Initial development hypothesis
            base_version: Starting version for iteration
            target_version: Intended new version
            researcher_id: ID of researcher conducting session
            
        Returns:
            Session ID for tracking
        """
        session = DevelopmentSession(
            session_name=session_name,
            component_type=component_type,
            component_name=component_name,
            hypothesis=hypothesis,
            base_version=base_version,
            target_version=target_version,
            researcher=researcher_id,
            status="active",
            development_notes="",
            iteration_log=[],
            test_results={},
            success_metrics={}
        )
        
        with self.Session() as db_session:
            db_session.add(session)
            db_session.commit()
            db_session.refresh(session)
            
        print(f"✅ Started development session: {session.id}")
        print(f"   Session: {session_name}")
        print(f"   Component: {component_type}/{component_name}")
        print(f"   Hypothesis: {hypothesis}")
        
        return str(session.id)
    
    def log_iteration(self,
                     session_id: str,
                     iteration_hypothesis: str,
                     changes_made: str,
                     test_results: Dict[str, Any],
                     performance_metrics: Optional[SessionMetrics] = None,
                     notes: str = "",
                     version_created: Optional[str] = None) -> int:
        """
        Log an iteration within a development session.
        
        Args:
            session_id: ID of the development session
            iteration_hypothesis: Hypothesis for this iteration
            changes_made: Description of changes made
            test_results: Testing outcomes and data
            performance_metrics: Quantitative performance metrics
            notes: Additional notes and observations
            version_created: New version ID if component was created
            
        Returns:
            Iteration number
        """
        with self.Session() as db_session:
            session = db_session.query(DevelopmentSession).filter_by(id=session_id).first()
            if not session:
                raise ValueError(f"Development session {session_id} not found")
            
            iteration_number = len(session.iteration_log) + 1
            
            iteration = SessionIteration(
                iteration_number=iteration_number,
                timestamp=datetime.now(timezone.utc),
                hypothesis=iteration_hypothesis,
                changes_made=changes_made,
                test_results=test_results,
                performance_metrics=performance_metrics or SessionMetrics(),
                notes=notes,
                version_created=version_created
            )
            
            # Convert iteration to dict for JSON storage
            iteration_dict = {
                "iteration": iteration.iteration_number,
                "timestamp": iteration.timestamp.isoformat(),
                "hypothesis": iteration.hypothesis,
                "changes_made": iteration.changes_made,
                "test_results": iteration.test_results,
                "performance_metrics": asdict(iteration.performance_metrics),
                "notes": iteration.notes,
                "version_created": iteration.version_created
            }
            
            # Update session with new iteration
            session.iteration_log.append(iteration_dict)
            session.last_activity = datetime.now(timezone.utc)
            
            # Update session success metrics with latest performance
            if performance_metrics:
                metrics_dict = asdict(performance_metrics)
                for key, value in metrics_dict.items():
                    if value is not None and key != 'custom_metrics':
                        session.success_metrics[key] = value
                if metrics_dict.get('custom_metrics'):
                    session.success_metrics.update(metrics_dict['custom_metrics'])
            
            # Update test results
            session.test_results.update(test_results)
            
            db_session.commit()
            
        print(f"✅ Logged iteration {iteration_number} for session {session_id}")
        if version_created:
            print(f"   Created version: {version_created}")
        
        return iteration_number
    
    def complete_session(self,
                        session_id: str,
                        lessons_learned: str,
                        final_version_created: Optional[str] = None,
                        success: bool = True) -> Dict[str, Any]:
        """
        Complete a development session with final documentation.
        
        Args:
            session_id: ID of the development session
            lessons_learned: Key learnings and insights from session
            final_version_created: Final component version ID if created
            success: Whether session achieved its goals
            
        Returns:
            Session summary with metrics and outcomes
        """
        with self.Session() as db_session:
            session = db_session.query(DevelopmentSession).filter_by(id=session_id).first()
            if not session:
                raise ValueError(f"Development session {session_id} not found")
            
            session.status = "completed" if success else "abandoned"
            session.lessons_learned = lessons_learned
            session.completed_at = datetime.now(timezone.utc)
            
            if final_version_created:
                session.created_version_id = final_version_created
            
            db_session.commit()
            
            # Generate session summary
            summary = {
                "session_id": session_id,
                "session_name": session.session_name,
                "component_type": session.component_type,
                "component_name": session.component_name,
                "status": session.status,
                "iterations": len(session.iteration_log),
                "duration_hours": self._calculate_duration(session),
                "final_metrics": session.success_metrics,
                "lessons_learned": lessons_learned,
                "version_created": final_version_created
            }
            
        print(f"✅ Completed development session: {session_id}")
        print(f"   Status: {session.status}")
        print(f"   Iterations: {len(session.iteration_log)}")
        if final_version_created:
            print(f"   Final version: {final_version_created}")
        
        return summary
    
    def get_session_status(self, session_id: str) -> Dict[str, Any]:
        """Get current status and metrics for a development session."""
        with self.Session() as db_session:
            session = db_session.query(DevelopmentSession).filter_by(id=session_id).first()
            if not session:
                raise ValueError(f"Development session {session_id} not found")
            
            return {
                "session_id": session_id,
                "session_name": session.session_name,
                "component_type": session.component_type,
                "component_name": session.component_name,
                "status": session.status,
                "hypothesis": session.hypothesis,
                "iterations": len(session.iteration_log),
                "started_at": session.started_at.isoformat(),
                "last_activity": session.last_activity.isoformat() if session.last_activity else None,
                "current_metrics": session.success_metrics,
                "latest_test_results": session.test_results
            }
    
    def list_active_sessions(self) -> List[Dict[str, Any]]:
        """List all currently active development sessions."""
        with self.Session() as db_session:
            active_sessions = db_session.query(DevelopmentSession).filter_by(status="active").all()
            
            return [
                {
                    "session_id": str(session.id),
                    "session_name": session.session_name,
                    "component_type": session.component_type,
                    "component_name": session.component_name,
                    "started_at": session.started_at.isoformat(),
                    "iterations": len(session.iteration_log),
                    "hypothesis": session.hypothesis
                }
                for session in active_sessions
            ]
    
    def get_session_analytics(self, component_type: Optional[str] = None) -> Dict[str, Any]:
        """Generate analytics across development sessions."""
        with self.Session() as db_session:
            query = db_session.query(DevelopmentSession)
            if component_type:
                query = query.filter_by(component_type=component_type)
            
            sessions = query.all()
            
            analytics = {
                "total_sessions": len(sessions),
                "completed_sessions": len([s for s in sessions if s.status == "completed"]),
                "active_sessions": len([s for s in sessions if s.status == "active"]),
                "abandoned_sessions": len([s for s in sessions if s.status == "abandoned"]),
                "average_iterations": sum(len(s.iteration_log) for s in sessions) / len(sessions) if sessions else 0,
                "component_type_breakdown": self._component_type_breakdown(sessions),
                "success_patterns": self._analyze_success_patterns(sessions),
                "performance_trends": self._analyze_performance_trends(sessions)
            }
            
        return analytics
    
    def get_seed_prompt(self, component_type: str, context: Optional[Dict] = None) -> str:
        """Get a structured seed prompt for starting development conversation."""
        try:
            comp_type = ComponentType(component_type)
            return self.seed_library.get_prompt(comp_type, context)
        except ValueError:
            raise ValueError(f"Unknown component type: {component_type}")
    
    def export_session_data(self, session_id: str, export_path: Optional[str] = None) -> str:
        """Export complete session data for external analysis."""
        with self.Session() as db_session:
            session = db_session.query(DevelopmentSession).filter_by(id=session_id).first()
            if not session:
                raise ValueError(f"Development session {session_id} not found")
            
            export_data = {
                "session_metadata": {
                    "id": str(session.id),
                    "name": session.session_name,
                    "component_type": session.component_type,
                    "component_name": session.component_name,
                    "hypothesis": session.hypothesis,
                    "status": session.status,
                    "started_at": session.started_at.isoformat(),
                    "completed_at": session.completed_at.isoformat() if session.completed_at else None
                },
                "iteration_log": session.iteration_log,
                "final_metrics": session.success_metrics,
                "test_results": session.test_results,
                "lessons_learned": session.lessons_learned,
                "created_version_id": session.created_version_id
            }
            
            if not export_path:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                export_path = f"exports/session_{session.session_name}_{timestamp}.json"
            
            Path(export_path).parent.mkdir(parents=True, exist_ok=True)
            with open(export_path, 'w') as f:
                json.dump(export_data, f, indent=2)
                
        return export_path
    
    def _calculate_duration(self, session: DevelopmentSession) -> float:
        """Calculate session duration in hours."""
        if not session.completed_at:
            end_time = datetime.now(timezone.utc)
        else:
            end_time = session.completed_at
            
        duration = end_time - session.started_at
        return duration.total_seconds() / 3600
    
    def _component_type_breakdown(self, sessions: List[DevelopmentSession]) -> Dict[str, int]:
        """Analyze component type distribution."""
        breakdown = {}
        for session in sessions:
            breakdown[session.component_type] = breakdown.get(session.component_type, 0) + 1
        return breakdown
    
    def _analyze_success_patterns(self, sessions: List[DevelopmentSession]) -> Dict[str, Any]:
        """Analyze patterns in successful sessions."""
        completed = [s for s in sessions if s.status == "completed"]
        
        if not completed:
            return {"no_completed_sessions": True}
        
        return {
            "average_iterations_successful": sum(len(s.iteration_log) for s in completed) / len(completed),
            "average_duration_hours": sum(self._calculate_duration(s) for s in completed) / len(completed),
            "common_hypotheses": self._extract_common_patterns([s.hypothesis for s in completed]),
            "version_creation_rate": len([s for s in completed if s.created_version_id]) / len(completed)
        }
    
    def _analyze_performance_trends(self, sessions: List[DevelopmentSession]) -> Dict[str, Any]:
        """Analyze performance metric trends across sessions."""
        metrics = []
        for session in sessions:
            if session.success_metrics:
                metrics.append(session.success_metrics)
        
        if not metrics:
            return {"no_metrics_available": True}
        
        # Calculate averages for common metrics
        common_metrics = ['coefficient_variation', 'hierarchy_clarity_score', 'framework_fit_average']
        trends = {}
        
        for metric in common_metrics:
            values = [m.get(metric) for m in metrics if m.get(metric) is not None]
            if values:
                trends[metric] = {
                    "average": sum(values) / len(values),
                    "trend": "improving" if len(values) > 1 and values[-1] > values[0] else "stable"
                }
        
        return trends
    
    def _extract_common_patterns(self, text_list: List[str]) -> List[str]:
        """Extract common patterns from text data."""
        # Simple pattern extraction - can be enhanced with NLP
        words = []
        for text in text_list:
            words.extend(text.lower().split())
        
        word_counts = {}
        for word in words:
            word_counts[word] = word_counts.get(word, 0) + 1
        
        # Return most common non-trivial words
        common_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
        return [word for word, count in common_words[:5] if len(word) > 3]


# Convenience functions for CLI integration
def start_dev_session(session_name: str, component_type: str, component_name: str, hypothesis: str) -> str:
    """Quick session startup for CLI tools."""
    manager = DevelopmentSessionManager()
    return manager.start_session(session_name, component_type, component_name, hypothesis)


def log_session_iteration(session_id: str, hypothesis: str, changes: str, results: Dict) -> int:
    """Quick iteration logging for CLI tools."""
    manager = DevelopmentSessionManager()
    return manager.log_iteration(session_id, hypothesis, changes, results) 