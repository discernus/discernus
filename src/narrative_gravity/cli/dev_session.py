#!/usr/bin/env python3
"""
Development Session Tracker (dev_session.py)
Priority 1 CLI Infrastructure Component

Structured session management with hypothesis tracking for systematic component development.
Implements manual development workflow orchestration and outcome tracking.
"""

import argparse
import json
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
import uuid

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, desc

from ..models import DevelopmentSession, PromptTemplate, FrameworkVersion, WeightingMethodology
from ..utils.database import get_database_url


class DevelopmentSessionTracker:
    """Tracks systematic component development sessions with hypothesis management."""
    
    def __init__(self):
        """Initialize database connection."""
        self.engine = create_engine(get_database_url())
        self.Session = sessionmaker(bind=self.engine)
    
    def start_session(self, session_name: str, component_type: str, component_name: str,
                     hypothesis: str = None, base_version: str = None, 
                     target_version: str = None) -> str:
        """Start a new development session."""
        session = self.Session()
        try:
            # Validate component type
            valid_types = ["prompt_template", "framework", "weighting_method"]
            if component_type not in valid_types:
                raise ValueError(f"Invalid component type. Must be one of: {valid_types}")
            
            # Check if session name already exists and is active
            existing = session.query(DevelopmentSession).filter_by(
                session_name=session_name, status="active"
            ).first()
            if existing:
                raise ValueError(f"Active session with name '{session_name}' already exists")
            
            # Validate base version exists if specified
            if base_version:
                self._validate_component_version(session, component_type, component_name, base_version)
            
            # Create new development session
            dev_session = DevelopmentSession(
                session_name=session_name,
                component_type=component_type,
                component_name=component_name,
                hypothesis=hypothesis,
                base_version=base_version,
                target_version=target_version,
                status="active",
                iteration_log=[],
                test_results={},
                success_metrics={}
            )
            
            session.add(dev_session)
            session.commit()
            
            print(f"🚀 Started development session: {session_name}")
            print(f"   Component: {component_type} - {component_name}")
            print(f"   Base Version: {base_version or 'None'}")
            print(f"   Target Version: {target_version or 'TBD'}")
            if hypothesis:
                print(f"   Hypothesis: {hypothesis}")
            
            return dev_session.id
            
        finally:
            session.close()
    
    def log_iteration(self, session_id: str, iteration_notes: str, 
                     test_results: Dict[str, Any] = None, 
                     performance_metrics: Dict[str, float] = None) -> None:
        """Log a development iteration with notes and results."""
        session = self.Session()
        try:
            dev_session = session.query(DevelopmentSession).filter_by(id=session_id).first()
            if not dev_session:
                raise ValueError(f"Development session not found: {session_id}")
            
            if dev_session.status != "active":
                raise ValueError(f"Session is not active: {dev_session.status}")
            
            # Create iteration record
            iteration_record = {
                'timestamp': datetime.now().isoformat(),
                'iteration_number': len(dev_session.iteration_log) + 1,
                'notes': iteration_notes,
                'test_results': test_results or {},
                'performance_metrics': performance_metrics or {}
            }
            
            # Update session
            dev_session.iteration_log.append(iteration_record)
            
            # Merge test results
            if test_results:
                dev_session.test_results.update(test_results)
            
            # Update metrics
            if performance_metrics:
                dev_session.success_metrics.update(performance_metrics)
            
            dev_session.last_activity = datetime.now()
            
            # Mark modified for SQLAlchemy to detect JSON changes
            session.query(DevelopmentSession).filter_by(id=session_id).update({
                'iteration_log': dev_session.iteration_log,
                'test_results': dev_session.test_results,
                'success_metrics': dev_session.success_metrics,
                'last_activity': dev_session.last_activity
            })
            
            session.commit()
            
            print(f"📝 Logged iteration #{iteration_record['iteration_number']} for session {dev_session.session_name}")
            if test_results:
                print(f"   Test Results: {len(test_results)} items")
            if performance_metrics:
                print(f"   Performance Metrics: {performance_metrics}")
            
        finally:
            session.close()
    
    def complete_session(self, session_id: str, created_version_id: str = None,
                        lessons_learned: str = None, success: bool = True) -> None:
        """Complete a development session with outcomes."""
        session = self.Session()
        try:
            dev_session = session.query(DevelopmentSession).filter_by(id=session_id).first()
            if not dev_session:
                raise ValueError(f"Development session not found: {session_id}")
            
            if dev_session.status != "active":
                raise ValueError(f"Session is not active: {dev_session.status}")
            
            # Update session
            dev_session.status = "completed" if success else "abandoned"
            dev_session.completed_at = datetime.now()
            dev_session.created_version_id = created_version_id
            dev_session.lessons_learned = lessons_learned
            
            session.commit()
            
            print(f"✅ Completed development session: {dev_session.session_name}")
            print(f"   Status: {dev_session.status}")
            print(f"   Duration: {dev_session.completed_at - dev_session.started_at}")
            print(f"   Iterations: {len(dev_session.iteration_log)}")
            if created_version_id:
                print(f"   Created Component: {created_version_id}")
            if lessons_learned:
                print(f"   Lessons Learned: {lessons_learned}")
            
        finally:
            session.close()
    
    def list_sessions(self, status: str = None, component_type: str = None) -> None:
        """List development sessions with optional filtering."""
        session = self.Session()
        try:
            query = session.query(DevelopmentSession)
            
            if status:
                query = query.filter_by(status=status)
            if component_type:
                query = query.filter_by(component_type=component_type)
            
            sessions = query.order_by(desc(DevelopmentSession.started_at)).all()
            
            print(f"\n🔬 Development Sessions ({len(sessions)} sessions)")
            if status:
                print(f"   Filtered by status: {status}")
            if component_type:
                print(f"   Filtered by type: {component_type}")
            
            for ds in sessions:
                status_icon = "🟢" if ds.status == "active" else "✅" if ds.status == "completed" else "❌"
                duration = ""
                if ds.status == "completed" and ds.completed_at:
                    duration = f" ({ds.completed_at - ds.started_at})"
                elif ds.status == "active":
                    duration = f" (active {datetime.now() - ds.started_at})"
                
                print(f"   {status_icon} {ds.session_name}")
                print(f"      {ds.component_type}: {ds.component_name}")
                print(f"      Started: {ds.started_at.strftime('%Y-%m-%d %H:%M')}{duration}")
                print(f"      Iterations: {len(ds.iteration_log)}")
                if ds.hypothesis:
                    print(f"      Hypothesis: {ds.hypothesis}")
                
        finally:
            session.close()
    
    def show_session_details(self, session_id: str) -> None:
        """Show detailed information about a development session."""
        session = self.Session()
        try:
            dev_session = session.query(DevelopmentSession).filter_by(id=session_id).first()
            if not dev_session:
                print(f"❌ Development session not found: {session_id}")
                return
            
            print(f"\n🔬 Development Session: {dev_session.session_name}")
            print(f"   ID: {dev_session.id}")
            print(f"   Component: {dev_session.component_type} - {dev_session.component_name}")
            print(f"   Status: {dev_session.status}")
            print(f"   Started: {dev_session.started_at}")
            if dev_session.completed_at:
                print(f"   Completed: {dev_session.completed_at}")
                print(f"   Duration: {dev_session.completed_at - dev_session.started_at}")
            else:
                print(f"   Active Duration: {datetime.now() - dev_session.started_at}")
            
            if dev_session.hypothesis:
                print(f"\n   Hypothesis:")
                print(f"   {dev_session.hypothesis}")
            
            if dev_session.base_version:
                print(f"   Base Version: {dev_session.base_version}")
            if dev_session.target_version:
                print(f"   Target Version: {dev_session.target_version}")
            
            # Show iterations
            print(f"\n   Iterations ({len(dev_session.iteration_log)}):")
            for iteration in dev_session.iteration_log:
                print(f"      #{iteration['iteration_number']} - {iteration['timestamp']}")
                print(f"         {iteration['notes']}")
                if iteration.get('performance_metrics'):
                    print(f"         Metrics: {iteration['performance_metrics']}")
            
            # Show test results
            if dev_session.test_results:
                print(f"\n   Test Results:")
                for test_name, result in dev_session.test_results.items():
                    print(f"      {test_name}: {result}")
            
            # Show success metrics
            if dev_session.success_metrics:
                print(f"\n   Success Metrics:")
                for metric_name, value in dev_session.success_metrics.items():
                    print(f"      {metric_name}: {value}")
            
            if dev_session.lessons_learned:
                print(f"\n   Lessons Learned:")
                print(f"   {dev_session.lessons_learned}")
            
            if dev_session.created_version_id:
                print(f"\n   Created Component Version: {dev_session.created_version_id}")
                
        finally:
            session.close()
    
    def export_session(self, session_id: str, output_file: str) -> None:
        """Export session data to JSON file."""
        session = self.Session()
        try:
            dev_session = session.query(DevelopmentSession).filter_by(id=session_id).first()
            if not dev_session:
                raise ValueError(f"Development session not found: {session_id}")
            
            # Convert to dictionary
            session_data = {
                'id': dev_session.id,
                'session_name': dev_session.session_name,
                'component_type': dev_session.component_type,
                'component_name': dev_session.component_name,
                'hypothesis': dev_session.hypothesis,
                'base_version': dev_session.base_version,
                'target_version': dev_session.target_version,
                'status': dev_session.status,
                'started_at': dev_session.started_at.isoformat() if dev_session.started_at else None,
                'completed_at': dev_session.completed_at.isoformat() if dev_session.completed_at else None,
                'last_activity': dev_session.last_activity.isoformat() if dev_session.last_activity else None,
                'iteration_log': dev_session.iteration_log,
                'test_results': dev_session.test_results,
                'success_metrics': dev_session.success_metrics,
                'created_version_id': dev_session.created_version_id,
                'lessons_learned': dev_session.lessons_learned
            }
            
            # Save to file
            with open(output_file, 'w') as f:
                json.dump(session_data, f, indent=2)
            
            print(f"📁 Exported session to: {output_file}")
            
        finally:
            session.close()
    
    def _validate_component_version(self, session, component_type: str, 
                                  component_name: str, version: str) -> None:
        """Validate that a component version exists."""
        if component_type == "prompt_template":
            component = session.query(PromptTemplate).filter_by(name=component_name, version=version).first()
        elif component_type == "framework":
            component = session.query(FrameworkVersion).filter_by(framework_name=component_name, version=version).first()
        elif component_type == "weighting_method":
            component = session.query(WeightingMethodology).filter_by(name=component_name, version=version).first()
        else:
            raise ValueError(f"Unknown component type: {component_type}")
        
        if not component:
            raise ValueError(f"Component version not found: {component_name}:{version}")


def main():
    """CLI entry point for development session tracker."""
    parser = argparse.ArgumentParser(description="Development Session Tracker")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Start session
    start_parser = subparsers.add_parser('start', help='Start new development session')
    start_parser.add_argument('--name', required=True, help='Session name')
    start_parser.add_argument('--type', required=True, choices=['prompt_template', 'framework', 'weighting_method'], help='Component type')
    start_parser.add_argument('--component', required=True, help='Component name')
    start_parser.add_argument('--hypothesis', help='Development hypothesis')
    start_parser.add_argument('--base-version', help='Base version for iteration')
    start_parser.add_argument('--target-version', help='Target version to create')
    
    # Log iteration
    log_parser = subparsers.add_parser('log', help='Log development iteration')
    log_parser.add_argument('--session-id', required=True, help='Session ID')
    log_parser.add_argument('--notes', required=True, help='Iteration notes')
    log_parser.add_argument('--test-results', help='JSON file with test results')
    log_parser.add_argument('--metrics', help='JSON string with performance metrics')
    
    # Complete session
    complete_parser = subparsers.add_parser('complete', help='Complete development session')
    complete_parser.add_argument('--session-id', required=True, help='Session ID')
    complete_parser.add_argument('--created-version', help='ID of created component version')
    complete_parser.add_argument('--lessons', help='Lessons learned')
    complete_parser.add_argument('--abandon', action='store_true', help='Mark session as abandoned')
    
    # List sessions
    list_parser = subparsers.add_parser('list', help='List development sessions')
    list_parser.add_argument('--status', choices=['active', 'completed', 'abandoned'], help='Filter by status')
    list_parser.add_argument('--type', choices=['prompt_template', 'framework', 'weighting_method'], help='Filter by component type')
    
    # Show session details
    show_parser = subparsers.add_parser('show', help='Show session details')
    show_parser.add_argument('session_id', help='Session ID')
    
    # Export session
    export_parser = subparsers.add_parser('export', help='Export session data')
    export_parser.add_argument('session_id', help='Session ID')
    export_parser.add_argument('output_file', help='Output JSON file')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        tracker = DevelopmentSessionTracker()
        
        if args.command == 'start':
            session_id = tracker.start_session(
                args.name, args.type, args.component, args.hypothesis,
                args.base_version, args.target_version
            )
            print(f"Session ID: {session_id}")
        
        elif args.command == 'log':
            test_results = None
            if args.test_results:
                with open(args.test_results, 'r') as f:
                    test_results = json.load(f)
            
            metrics = None
            if args.metrics:
                metrics = json.loads(args.metrics)
            
            tracker.log_iteration(args.session_id, args.notes, test_results, metrics)
        
        elif args.command == 'complete':
            tracker.complete_session(
                args.session_id, args.created_version, args.lessons, not args.abandon
            )
        
        elif args.command == 'list':
            tracker.list_sessions(args.status, args.type)
        
        elif args.command == 'show':
            tracker.show_session_details(args.session_id)
        
        elif args.command == 'export':
            tracker.export_session(args.session_id, args.output_file)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main()) 