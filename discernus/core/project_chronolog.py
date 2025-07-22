#!/usr/bin/env python3
"""
Project Chronolog: Comprehensive Research Provenance System
==========================================================

Implements the comprehensive project-level audit trail specified in Discernus.
Captures every action from user initialization through final publication.

Discernus Specification Compliance:
- Project-level scope spanning entire research lifecycle
- Initialization event as first chronolog entry
- All agent actions, user interactions, system events
- Cross-session continuity within projects
- Immutable append-only design for academic integrity
- Blockchain-ready architecture for future commercialization
"""

import json
import hashlib
import hmac
import os
import sys
import redis
import threading
import git
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
import uuid

@dataclass
class ChronologEvent:
    """Single chronolog event with tamper-evident integrity"""
    timestamp: str
    event: str
    session_id: str
    project: str
    data: Dict[str, Any]
    event_id: str = ""
    signature: Optional[str] = None
    
    def __post_init__(self):
        if not self.event_id:
            self.event_id = str(uuid.uuid4())

class ProjectChronolog:
    """
    Comprehensive project-level audit trail for academic research integrity
    
    Implements Discernus chronolog specification:
    - Captures every action from initialization through completion
    - Project-scoped with cross-session continuity 
    - Immutable append-only design with cryptographic integrity
    - Academic publication integration for peer review
    """
    
    def __init__(self, project_path: str, signing_key: Optional[str] = None):
        self.project_path = Path(project_path)
        self.project_name = self.project_path.name
        
        # Ensure project directory exists
        self.project_path.mkdir(parents=True, exist_ok=True)
        
        # Project chronolog location per Discernus specification
        self.chronolog_file = self.project_path / f"PROJECT_CHRONOLOG_{self.project_name}.jsonl"
        
        # Initialize Git repo for automatic commits, but NEVER create a new one.
        try:
            # Search up from the project path to find the true git root.
            # This prevents initializing a new repo in a subdirectory.
            self.git_repo = git.Repo(self.project_path, search_parent_directories=True)
            self.true_project_root = Path(self.git_repo.working_dir)
            print(f"✅ ProjectChronolog Git integration active for project: {self.project_name} at root {self.true_project_root}")
        except git.InvalidGitRepositoryError:
            # This is the expected case when running in a non-git directory.
            print(f"⚠️ ProjectChronolog: Not in a Git repository, chronolog persistence limited.")
            self.git_repo = None
        
        # Cryptographic signing for tamper evidence
        self.signing_key = signing_key or os.getenv('CHRONOLOG_SIGNING_KEY', 'default_dev_key')
        
        # Redis integration for real-time event capture
        self.redis_client = None
        self.redis_subscriber = None
        self.redis_thread = None
        self._active = False
        
        self._init_redis_integration()
        
    def _init_redis_integration(self):
        """Initialize Redis integration for automatic event capture"""
        try:
            self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
            self.redis_client.ping()  # Test connection
            print(f"✅ ProjectChronolog Redis connected for project: {self.project_name}")
        except Exception as e:
            print(f"⚠️ ProjectChronolog Redis unavailable: {e}")
            self.redis_client = None
    
    def _sign_event(self, event: ChronologEvent) -> str:
        """Generate cryptographic signature for event integrity"""
        # Create canonical representation for signing
        canonical_data = {
            'timestamp': event.timestamp,
            'event': event.event, 
            'session_id': event.session_id,
            'project': event.project,
            'event_id': event.event_id,
            'data': event.data
        }
        
        canonical_json = json.dumps(canonical_data, sort_keys=True, separators=(',', ':'))
        signature = hmac.new(
            self.signing_key.encode('utf-8'),
            canonical_json.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        return signature
    
    def log_initialization(self, user: str, command: str, session_id: str, 
                          system_state: Optional[Dict[str, Any]] = None) -> str:
        """
        Log project initialization - first chronolog entry per Discernus
        
        This is the critical entry that starts comprehensive research provenance.
        Everything else in the project builds from this initialization event.
        """
        initialization_data = {
            'user': user,
            'command': command,
            'system_state': system_state or {},
            'git_commit': self._get_git_commit(),
                         'environment': {
                 'python_version': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
                 'working_directory': str(Path.cwd()),
                 'project_path': str(self.project_path),
                 'chronolog_version': '2.0'
             }
        }
        
        event = ChronologEvent(
            timestamp=datetime.utcnow().isoformat() + "Z",
            event="PROJECT_INITIALIZATION",
            session_id=session_id,
            project=self.project_name,
            data=initialization_data
        )
        
        self._append_event(event)
        self._start_redis_capture(session_id)
        
        print(f"📝 PROJECT_INITIALIZATION logged for {self.project_name}")
        return event.event_id
    
    def log_event(self, event_type: str, session_id: str, data: Dict[str, Any]) -> str:
        """Log any project event with automatic timestamping and signing"""
        event = ChronologEvent(
            timestamp=datetime.utcnow().isoformat() + "Z",
            event=event_type,
            session_id=session_id,
            project=self.project_name,
            data=data
        )
        
        self._append_event(event)
        return event.event_id
    
    def _append_event(self, event: ChronologEvent):
        """Append event to chronolog with cryptographic integrity and Git commit"""
        # Generate signature
        event.signature = self._sign_event(event)
        
        # Convert to dict and write to JSONL
        event_dict = asdict(event)
        
        with open(self.chronolog_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(event_dict, separators=(',', ':')) + '\n')
            f.flush()  # Ensure immediate write for crash safety
        
        # Automatically commit to Git for reliable persistence
        self._commit_chronolog_event(event)
    
    def _commit_chronolog_event(self, event: ChronologEvent):
        """Automatically commit chronolog event to Git for reliable persistence"""
        if not self.git_repo:
            return
        
        try:
            # Add chronolog file to Git
            self.git_repo.index.add([str(self.chronolog_file)])
            
            # Create descriptive commit message
            commit_message = f"Chronolog: {event.event} - {self.project_name}"
            if event.event == "PROJECT_INITIALIZATION":
                commit_message += f"\n\nProject initialized by {event.data.get('user', 'unknown')}"
                commit_message += f"\nCommand: {event.data.get('command', 'unknown')}"
            else:
                commit_message += f"\n\nEvent: {event.event}"
                commit_message += f"\nSession: {event.session_id}"
            
            # Commit with tamper-evident signature
            if event.signature:
                commit_message += f"\nChronolog signature: {event.signature[:16]}..."
            
            self.git_repo.index.commit(commit_message)
            print(f"📝 Chronolog event committed to Git: {event.event}")
            
        except Exception as e:
            print(f"⚠️ Failed to commit chronolog event to Git: {e}")
    
    def _start_redis_capture(self, session_id: str):
        """Start automatic Redis event capture for this project"""
        if not self.redis_client or self._active:
            return
            
        self._active = True
        self.redis_subscriber = self.redis_client.pubsub()
        self.redis_subscriber.psubscribe('discernus.*')
        
        # Start background thread for Redis event capture
        self.redis_thread = threading.Thread(
            target=self._redis_event_listener,
            args=(session_id,),
            daemon=True
        )
        self.redis_thread.start()
        
        print(f"📡 Redis event capture started for project: {self.project_name}")
    
    def _redis_event_listener(self, primary_session_id: str):
        """Background thread that captures Redis events to chronolog"""
        if not self.redis_subscriber:
            return
            
        try:
            for message in self.redis_subscriber.listen():
                if message['type'] == 'pmessage':
                    # Parse Redis event
                    channel = message['channel'].decode('utf-8')
                    try:
                        redis_data = json.loads(message['data'].decode('utf-8'))
                    except json.JSONDecodeError:
                        continue
                    
                    # Extract session ID, default to primary if not found
                    event_session_id = redis_data.get('session_id', primary_session_id)
                    
                    # Create chronolog event from Redis event
                    chronolog_data = {
                        'redis_channel': channel,
                        'redis_data': redis_data,
                        'capture_timestamp': datetime.utcnow().isoformat() + "Z"
                    }
                    
                    # Log as chronolog event
                    self.log_event("REDIS_EVENT_CAPTURED", event_session_id, chronolog_data)
                    
                    # Break if we're no longer active
                    if not self._active:
                        break
                        
        except Exception as e:
            print(f"⚠️ Redis event listener error: {e}")
            self._active = False
    
    def stop_capture(self):
        """Stop Redis event capture for this project"""
        self._active = False
        if self.redis_subscriber:
            self.redis_subscriber.close()
        if self.redis_thread and self.redis_thread.is_alive():
            self.redis_thread.join(timeout=1.0)
        
        print(f"📡 Redis event capture stopped for project: {self.project_name}")
    
    def _get_git_commit(self) -> Optional[str]:
        """Get current git commit hash for provenance"""
        try:
            if self.git_repo:
                return self.git_repo.head.commit.hexsha[:10]
            else:
                # Fallback to searching for git repo
                repo = git.Repo(self.project_path, search_parent_directories=True)
                return repo.head.commit.hexsha[:10]
        except:
            return None
    
    def get_chronolog_summary(self) -> Dict[str, Any]:
        """Get summary statistics of project chronolog"""
        if not self.chronolog_file.exists():
            return {'status': 'not_initialized', 'event_count': 0}
        
        event_count = 0
        first_event = None
        last_event = None
        event_types = {}
        
        with open(self.chronolog_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    event = json.loads(line.strip())
                    event_count += 1
                    
                    if first_event is None:
                        first_event = event
                    last_event = event
                    
                    event_type = event.get('event', 'unknown')
                    event_types[event_type] = event_types.get(event_type, 0) + 1
                    
                except json.JSONDecodeError:
                    continue
        
        return {
            'status': 'active',
            'event_count': event_count,
            'first_event': first_event,
            'last_event': last_event,
            'event_types': event_types,
            'project': self.project_name,
            'chronolog_file': str(self.chronolog_file)
        }
    
    def verify_integrity(self) -> Dict[str, Any]:
        """Verify cryptographic integrity of entire chronolog"""
        if not self.chronolog_file.exists():
            return {'status': 'no_chronolog', 'verified': False}
        
        verified_events = 0
        corrupted_events = []
        
        with open(self.chronolog_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                try:
                    event_dict = json.loads(line.strip())
                    
                    # Reconstruct event for signature verification
                    stored_signature = event_dict.pop('signature', None)
                    if not stored_signature:
                        corrupted_events.append({'line': line_num, 'reason': 'missing_signature'})
                        continue
                    
                    # Create event object and verify signature
                    event = ChronologEvent(**event_dict)
                    expected_signature = self._sign_event(event)
                    
                    if hmac.compare_digest(stored_signature, expected_signature):
                        verified_events += 1
                    else:
                        corrupted_events.append({'line': line_num, 'reason': 'signature_mismatch'})
                        
                except json.JSONDecodeError:
                    corrupted_events.append({'line': line_num, 'reason': 'invalid_json'})
                except Exception as e:
                    corrupted_events.append({'line': line_num, 'reason': str(e)})
        
        return {
            'status': 'verification_complete',
            'verified': len(corrupted_events) == 0,
            'verified_events': verified_events,
            'corrupted_events': corrupted_events,
            'total_events': verified_events + len(corrupted_events)
        }
    
    def merge_run_log(self, run_chronolog_file_path: str):
        """
        Merges a run-specific chronolog into the main project chronolog.
        """
        run_log_path = Path(run_chronolog_file_path)
        if not run_log_path.exists():
            print(f"⚠️ Run chronolog file not found for merging: {run_log_path}")
            return

        with open(run_log_path, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    event_dict = json.loads(line.strip())
                    # Re-create the event object to ensure it's correctly structured
                    event = ChronologEvent(**event_dict)
                    # Append to the main project chronolog
                    self._append_event(event)
                except (json.JSONDecodeError, TypeError) as e:
                    print(f"⚠️ Could not parse or merge event from {run_log_path}: {e}")
                    continue
    
    def create_run_chronolog(self, session_id: str, results_directory: str) -> Dict[str, Any]:
        """
        Create run-specific chronolog by filtering project chronolog by session_id
        
        Essential for academic integrity and statistical analysis:
        - Each run has self-contained tamper-evident record
        - Enables Cronbach's alpha calculations across multiple runs
        - Supports debugging and performance analysis per run
        - Maintains cryptographic integrity of original events
        
        Args:
            session_id: The session to extract events for
            results_directory: Directory to save the run chronolog
            
        Returns:
            Dictionary with run chronolog statistics and file path
        """
        if not self.chronolog_file.exists():
            return {'status': 'no_project_chronolog', 'created': False}
        
        # Create results directory if it doesn't exist
        results_path = Path(results_directory)
        results_path.mkdir(parents=True, exist_ok=True)
        
        # Run chronolog filename
        run_chronolog_file = results_path / f"RUN_CHRONOLOG_{session_id}.jsonl"
        
        # Filter project chronolog for this session
        session_events = []
        total_events = 0
        
        with open(self.chronolog_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    event_dict = json.loads(line.strip())
                    total_events += 1
                    
                    # Filter by session_id
                    if event_dict.get('session_id') == session_id:
                        session_events.append(event_dict)
                        
                except json.JSONDecodeError:
                    continue
        
        # Write run-specific chronolog
        with open(run_chronolog_file, 'w', encoding='utf-8') as f:
            for event_dict in session_events:
                f.write(json.dumps(event_dict, separators=(',', ':')) + '\n')
            f.flush()  # Ensure data is written to disk
        
        # Ensure file exists before Git commit
        if not run_chronolog_file.exists():
            print(f"⚠️ Run chronolog file not found after write: {run_chronolog_file}")
            return {'status': 'file_write_failed', 'created': False}
        
        # Calculate timing statistics for academic analysis
        run_stats = self._calculate_run_statistics(session_events)
        
        # Commit run chronolog to Git for academic integrity
        self._commit_run_chronolog(session_id, run_chronolog_file, len(session_events))
        
        return {
            'status': 'run_chronolog_created',
            'created': True,
            'session_id': session_id,
            'run_chronolog_file': str(run_chronolog_file),
            'session_events': len(session_events),
            'total_project_events': total_events,
            'run_statistics': run_stats
        }
    
    def _calculate_run_statistics(self, session_events: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate timing and event statistics for academic analysis
        
        Critical for statistical analysis and Cronbach's alpha calculations
        """
        if not session_events:
            return {'status': 'no_events'}
        
        # Extract timestamps and event types
        timestamps = []
        event_types = {}
        
        for event in session_events:
            try:
                timestamp = datetime.fromisoformat(event['timestamp'].replace('Z', '+00:00'))
                timestamps.append(timestamp)
                
                event_type = event.get('event', 'unknown')
                event_types[event_type] = event_types.get(event_type, 0) + 1
                
            except (ValueError, KeyError):
                continue
        
        if not timestamps:
            return {'status': 'no_valid_timestamps'}
        
        # Calculate timing statistics
        timestamps.sort()
        start_time = timestamps[0]
        end_time = timestamps[-1]
        duration = (end_time - start_time).total_seconds()
        
        # Find analysis phase timing (for performance analysis)
        analysis_start = None
        analysis_end = None
        
        for i, event in enumerate(session_events):
            event_type = event.get('event', '')
            if 'ANALYSIS_AGENTS_SPAWNING' in event_type and analysis_start is None:
                try:
                    analysis_start = datetime.fromisoformat(event['timestamp'].replace('Z', '+00:00'))
                except (ValueError, KeyError):
                    pass
            elif 'ANALYSIS_AGENTS_COMPLETED' in event_type:
                try:
                    analysis_end = datetime.fromisoformat(event['timestamp'].replace('Z', '+00:00'))
                except (ValueError, KeyError):
                    pass
        
        analysis_duration = None
        if analysis_start and analysis_end:
            analysis_duration = (analysis_end - analysis_start).total_seconds()
        
        return {
            'status': 'statistics_calculated',
            'start_time': start_time.isoformat(),
            'end_time': end_time.isoformat(),
            'total_duration_seconds': duration,
            'analysis_duration_seconds': analysis_duration,
            'event_count': len(session_events),
            'event_types': event_types,
            'events_per_minute': (len(session_events) / (duration / 60)) if duration > 0 else 0
        }
    
    def _commit_run_chronolog(self, session_id: str, run_chronolog_file: Path, event_count: int):
        """Commit run chronolog to Git for academic integrity"""
        if not self.git_repo:
            return
        
        try:
            # Ensure file exists before adding to Git
            if not run_chronolog_file.exists():
                print(f"⚠️ Run chronolog file doesn't exist for Git commit: {run_chronolog_file}")
                return
            
            # Get relative path from git repo root for cleaner commits
            try:
                repo_root = Path(self.git_repo.working_dir)
                # Ensure we're working with resolved absolute paths
                absolute_file_path = run_chronolog_file.resolve()
                absolute_repo_root = repo_root.resolve()
                relative_path = absolute_file_path.relative_to(absolute_repo_root)
                file_path_for_git = str(relative_path)
            except ValueError:
                # If relative path fails, use absolute path
                file_path_for_git = str(run_chronolog_file)
            

            
            # Add run chronolog file to Git
            self.git_repo.index.add([file_path_for_git])
            
            # Create descriptive commit message
            commit_message = f"Run Chronolog: {session_id} - {self.project_name}"
            commit_message += f"\n\nRun-specific chronolog created for session: {session_id}"
            commit_message += f"\nEvents captured: {event_count}"
            commit_message += f"\nFile: {run_chronolog_file.name}"
            commit_message += f"\nProject: {self.project_name}"
            
            self.git_repo.index.commit(commit_message)
            print(f"📝 Run chronolog committed to Git: {session_id}")
            
        except Exception as e:
            print(f"⚠️ Failed to commit run chronolog to Git: {e}")
    
    def get_session_events(self, session_id: str) -> List[Dict[str, Any]]:
        """Get all events for a specific session without creating a file"""
        if not self.chronolog_file.exists():
            return []
        
        session_events = []
        
        with open(self.chronolog_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    event_dict = json.loads(line.strip())
                    if event_dict.get('session_id') == session_id:
                        session_events.append(event_dict)
                except json.JSONDecodeError:
                    continue
        
        return session_events
    
    def list_sessions(self) -> List[Dict[str, Any]]:
        """List all sessions in the project chronolog with basic statistics"""
        if not self.chronolog_file.exists():
            return []
        
        sessions = {}
        
        with open(self.chronolog_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    event_dict = json.loads(line.strip())
                    session_id = event_dict.get('session_id')
                    
                    if session_id:
                        if session_id not in sessions:
                            sessions[session_id] = {
                                'session_id': session_id,
                                'first_event': event_dict,
                                'last_event': event_dict,
                                'event_count': 0,
                                'event_types': {}
                            }
                        
                        sessions[session_id]['last_event'] = event_dict
                        sessions[session_id]['event_count'] += 1
                        
                        event_type = event_dict.get('event', 'unknown')
                        sessions[session_id]['event_types'][event_type] = sessions[session_id]['event_types'].get(event_type, 0) + 1
                        
                except json.JSONDecodeError:
                    continue
        
        return list(sessions.values())


# Global registry for active project chronologs
_active_chronologs: Dict[str, ProjectChronolog] = {}

def _detect_project_root(path_str: str) -> Path:
    """
    Detect the actual project root from a file path.
    For Discernus projects, the project root is the first subdirectory under 'projects/'.
    This ensures one chronolog per logical project (e.g., MVA, attesor) regardless of experiment subdirectories.
    """
    original_path = Path(path_str).resolve()
    if original_path.is_file():
        original_path = original_path.parent
        
    parts = original_path.parts
    try:
        projects_index = parts.index('projects')
        if projects_index + 1 < len(parts):
            # Return path up to the first subdirectory under 'projects/'
            # e.g., projects/MVA/experiment_1 → projects/MVA
            return Path(*parts[:projects_index + 2])
    except ValueError:
        pass # 'projects' not in path
        
    # Fallback: search upwards for a .git directory for non-projects paths
    current_path = original_path
    while current_path != current_path.parent:
        if (current_path / ".git").is_dir():
            return current_path
        current_path = current_path.parent
        
    return original_path

def get_project_chronolog(project_path: str) -> ProjectChronolog:
    """Get or create project chronolog instance"""
    # Detect the actual project root
    actual_project_root = _detect_project_root(project_path)
    project_key = str(actual_project_root)
    
    if project_key not in _active_chronologs:
        _active_chronologs[project_key] = ProjectChronolog(str(actual_project_root))
    
    return _active_chronologs[project_key]

def initialize_project_chronolog(project_path: str, user: str, command: str, 
                                session_id: str, system_state: Optional[Dict[str, Any]] = None) -> str:
    """
    Initialize project chronolog with PROJECT_INITIALIZATION event
    
    This is the critical function that starts comprehensive research provenance.
    Should be called by all entry points (CLI, ValidationAgent, etc.)
    """
    chronolog = get_project_chronolog(project_path)
    return chronolog.log_initialization(user, command, session_id, system_state)

def log_project_event(project_path: str, event_type: str, session_id: str, 
                     data: Dict[str, Any]) -> str:
    """Log event to project chronolog"""
    chronolog = get_project_chronolog(project_path)
    return chronolog.log_event(event_type, session_id, data)

def cleanup_project_chronolog(project_path: str):
    """Stop and cleanup project chronolog"""
    project_key = str(Path(project_path).resolve())
    if project_key in _active_chronologs:
        _active_chronologs[project_key].stop_capture()
        del _active_chronologs[project_key] 