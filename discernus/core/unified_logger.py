#!/usr/bin/env python3
"""
Unified Logger - Consolidates All Fragmented Logging Systems
===========================================================

THIN Principle: Single source of truth for all logging with dual-track output.
Solves the fragmented logging crisis that caused critical failures in MVA Experiment 2.

CRITICAL PROBLEMS SOLVED:
1. Fragmented provenance with duplicate conversation logs having different contents
2. Session logs only written at end so crashes leave no debugging record
3. Multiple logging systems that don't work together coherently

UNIFIED SOLUTION:
- Dual-track logging: Human-readable + Machine-readable
- Real-time append-only logging (no end-of-session writes)
- Single source of truth for all logging
- Complete audit trail with tamper-evident hashing
- Forensic validation integration
"""

import json
import hashlib
import threading
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List, Union
import git
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UnifiedLogger:
    """
    Single source of truth for all logging in the Discernus system.
    Consolidates ConversationLogger, ProjectChronolog, and agent-specific logging.
    """

    def __init__(self, project_path: Union[str, Path]):
        self.project_path = Path(project_path)
        self.project_name = self.project_path.name
        
        # Create logging directories
        self.logs_dir = self.project_path / "logs"
        self.logs_dir.mkdir(exist_ok=True)
        
        # Initialize session-specific logging
        self.session_id = None
        self.session_logs_dir = None
        self.conversation_id = None
        
        # Thread lock for safe concurrent logging
        self.log_lock = threading.Lock()
        
        # Initialize Git repo for tamper-evident logging
        try:
            self.git_repo = git.Repo(self.project_path, search_parent_directories=True)
            logger.info(f"✅ UnifiedLogger Git integration active for {self.project_name}")
        except git.InvalidGitRepositoryError:
            logger.warning(f"⚠️ UnifiedLogger: Not in Git repository, tamper evidence limited")
            self.git_repo = None
        
        # Forensic validation integration
        self.forensic_enabled = True
        self.content_hashes = {}
        
        logger.info(f"✅ UnifiedLogger initialized for project: {self.project_name}")

    def start_session(self, session_id: str, research_question: str, participants: List[str],
                     experiment_metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Start a new logging session with dual-track output and comprehensive header.
        
        Args:
            session_id: Unique session identifier
            research_question: The research question being investigated
            participants: List of agents/participants in the session
            experiment_metadata: Optional experiment details for self-contained logs
            
        Returns:
            conversation_id: Unique identifier for this conversation
        """
        self.session_id = session_id
        self.conversation_id = f"conversation_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{session_id}"
        
        # Create session-specific directory
        self.session_logs_dir = self.logs_dir / session_id
        self.session_logs_dir.mkdir(exist_ok=True)
        
        # Initialize session metadata
        session_metadata = {
            'session_id': session_id,
            'conversation_id': self.conversation_id,
            'research_question': research_question,
            'participants': participants,
            'started_at': datetime.utcnow().isoformat() + "Z",
            'project_name': self.project_name,
            'experiment_metadata': experiment_metadata or {}
        }
        
        # Log session start in both tracks
        self.log_event("SESSION_START", "system", session_metadata)
        
        # Create comprehensive research session header
        header = self._create_research_session_header(session_id, research_question, participants, experiment_metadata)
        self.log_human_readable(header)
        
        return self.conversation_id

    def _create_research_session_header(self, session_id: str, research_question: str, 
                                       participants: List[str], experiment_metadata: Optional[Dict[str, Any]]) -> str:
        """Create a comprehensive research session header for self-contained logs."""
        
        header = f"""# Research Session Log
========================================

## Session Information
**Session ID:** {session_id}
**Project:** {self.project_name}
**Started:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}Z
**Research Question:** {research_question}
**Participants:** {', '.join(participants)}

## Experiment Details"""
        
        if experiment_metadata:
            if 'framework_name' in experiment_metadata:
                header += f"\n**Framework:** {experiment_metadata['framework_name']}"
            if 'framework_version' in experiment_metadata:
                header += f" (v{experiment_metadata['framework_version']})"
            if 'experiment_name' in experiment_metadata:
                header += f"\n**Experiment:** {experiment_metadata['experiment_name']}"
            if 'models' in experiment_metadata:
                header += f"\n**Models:** {', '.join(experiment_metadata['models'])}"
            if 'runs_per_model' in experiment_metadata:
                header += f"\n**Runs per Model:** {experiment_metadata['runs_per_model']}"
            if 'corpus_files' in experiment_metadata:
                header += f"\n**Corpus Files:** {len(experiment_metadata['corpus_files'])} files"
                # Show first few corpus files as examples
                if experiment_metadata['corpus_files']:
                    header += f"\n**Sample Corpus:** {', '.join(experiment_metadata['corpus_files'][:3])}"
                    if len(experiment_metadata['corpus_files']) > 3:
                        header += f" (and {len(experiment_metadata['corpus_files']) - 3} more)"
        
        header += f"\n\n## Analysis Log\n{'='*50}\n"
        
        return header

    def log_event(self, event_type: str, speaker: str, data: Dict[str, Any], 
                  metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Log a structured event to the machine-readable track.
        
        Args:
            event_type: Type of event (e.g., "ANALYSIS_COMPLETE", "FORENSIC_VALIDATION")
            speaker: Who/what generated this event
            data: Event data
            metadata: Optional metadata
            
        Returns:
            event_id: Unique identifier for this event
        """
        if not self.session_id:
            raise ValueError("Session not started. Call start_session() first.")
        
        timestamp = datetime.utcnow().isoformat() + "Z"
        event_id = hashlib.sha256(f"{timestamp}{event_type}{speaker}".encode()).hexdigest()[:12]
        
        # Create forensic content hash
        content_hash = self._create_content_hash(data)
        
        log_entry = {
            "event_id": event_id,
            "timestamp": timestamp,
            "session_id": self.session_id,
            "conversation_id": self.conversation_id,
            "event_type": event_type,
            "speaker": speaker,
            "data": data,
            "metadata": metadata or {},
            "content_hash": content_hash
        }
        
        # Write to machine-readable log (JSONL format)
        if self.session_logs_dir is None:
            raise ValueError("Session logs directory not initialized")
        machine_log_file = self.session_logs_dir / f"{self.session_id}_machine.jsonl"
        with self.log_lock:
            with open(machine_log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
        
        # Store content hash for forensic validation
        self.content_hashes[event_id] = content_hash
        
        return event_id

    def log_human_readable(self, message: str, speaker: str = "system", 
                          event_type: str = "INFO") -> None:
        """
        Log a human-readable message to the human track.
        
        Args:
            message: Human-readable message
            speaker: Who/what generated this message
            event_type: Type of event for context
        """
        if not self.session_id:
            raise ValueError("Session not started. Call start_session() first.")
        
        timestamp = datetime.utcnow().strftime('%H:%M:%S')
        
        # Format message for human consumption
        formatted_message = f"\n**{speaker.replace('_', ' ').title()}** *(at {timestamp}Z)*:\n\n{message}\n\n---\n"
        
        # Write to human-readable log (Markdown format)
        if self.session_logs_dir is None:
            raise ValueError("Session logs directory not initialized")
        human_log_file = self.session_logs_dir / f"{self.session_id}_human.md"
        with self.log_lock:
            with open(human_log_file, 'a', encoding='utf-8') as f:
                f.write(formatted_message)

    def log_analysis_result(self, agent_id: str, corpus_file: str, model_name: str, 
                           content: str, run_num: int, provenance_validated: bool = False,
                           forensic_validated: bool = False, metadata: Optional[Dict[str, Any]] = None,
                           corpus_text: Optional[str] = None) -> str:
        """
        Log an analysis result with research narrative format.
        
        Args:
            agent_id: Identifier for the agent
            corpus_file: Path to the corpus file analyzed
            model_name: Name of the model used
            content: Analysis content
            run_num: Run number for multi-run experiments
            provenance_validated: Whether provenance validation passed
            forensic_validated: Whether forensic validation passed
            metadata: Optional metadata
            corpus_text: Optional corpus text for narrative context
            
        Returns:
            event_id: Unique identifier for this event
        """
        # Structure the analysis data
        analysis_data = {
            'agent_id': agent_id,
            'corpus_file': corpus_file,
            'model_name': model_name,
            'content': content,
            'run_num': run_num,
            'provenance_validated': provenance_validated,
            'forensic_validated': forensic_validated,
            'content_length': len(content)
        }
        
        # Log to machine-readable track
        event_id = self.log_event("ANALYSIS_RESULT", agent_id, analysis_data, metadata)
        
        # Create research narrative for human-readable track
        validation_status = "✅ VALIDATED" if provenance_validated else "❌ VALIDATION FAILED"
        if provenance_validated and not forensic_validated:
            validation_status = "✅ PROVENANCE VALIDATED (forensic disabled)"
        
        narrative = f"""📊 **Analysis Complete - Run {run_num}**
**Model:** {model_name}
**Corpus File:** {Path(corpus_file).name}
**Validation:** {validation_status}
"""
        
        # Add corpus snippet for context
        if corpus_text:
            corpus_snippet = corpus_text[:200] + "..." if len(corpus_text) > 200 else corpus_text
            narrative += f"\n**Text Being Analyzed:**\n*\"{corpus_snippet}\"*\n"
        
        # Add LLM response snippet  
        response_snippet = content[:300] + "..." if len(content) > 300 else content
        narrative += f"\n**LLM Analysis:**\n*\"{response_snippet}\"*\n"
        
        # Add technical details
        narrative += f"\n**Technical Details:**\n"
        narrative += f"- Content Length: {len(content)} characters\n"
        narrative += f"- Agent ID: {agent_id}\n"
        
        if metadata and 'provenance_stamp' in metadata:
            narrative += f"- Provenance Stamp: {metadata['provenance_stamp'][:16]}...\n"
        
        self.log_human_readable(narrative, agent_id, "ANALYSIS_RESULT")
        
        return event_id

    def log_forensic_validation(self, corpus_file: str, validation_result: Dict[str, Any]) -> str:
        """
        Log forensic validation results.
        
        Args:
            corpus_file: Path to the corpus file
            validation_result: Result from ForensicQAAgent
            
        Returns:
            event_id: Unique identifier for this event
        """
        event_id = self.log_event("FORENSIC_VALIDATION", "forensic_qa_agent", validation_result)
        
        status = "✅ PASSED" if validation_result.get('valid', False) else "❌ FAILED"
        error_msg = validation_result.get('error', 'No error')
        
        self.log_human_readable(
            f"🔍 **Forensic Validation Result**\n"
            f"**File:** {Path(corpus_file).name}\n"
            f"**Status:** {status}\n"
            f"**Content Hash:** {validation_result.get('content_hash', 'N/A')}\n"
            f"**Error:** {error_msg if not validation_result.get('valid', False) else 'None'}\n",
            "forensic_qa_agent",
            "FORENSIC_VALIDATION"
        )
        
        return event_id

    def log_system_event(self, event_type: str, event_data: Dict[str, Any]) -> str:
        """
        Log a system event (workflow, orchestrator, etc.).
        
        Args:
            event_type: Type of system event
            event_data: Event data
            
        Returns:
            event_id: Unique identifier for this event
        """
        event_id = self.log_event(event_type, "system", event_data)
        
        self.log_human_readable(
            f"⚙️ **System Event: {event_type}**\n"
            f"**Details:** {json.dumps(event_data, indent=2)}\n",
            "system",
            event_type
        )
        
        return event_id

    def log_error(self, error_type: str, error_message: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Log an error with full context.
        
        Args:
            error_type: Type of error
            error_message: Error message
            context: Optional context data
            
        Returns:
            event_id: Unique identifier for this event
        """
        error_data = {
            'error_type': error_type,
            'error_message': error_message,
            'context': context if context is not None else {}
        }
        
        event_id = self.log_event("ERROR", "system", error_data)
        
        self.log_human_readable(
            f"❌ **Error: {error_type}**\n"
            f"**Message:** {error_message}\n"
            f"**Context:** {json.dumps(context, indent=2) if context is not None else 'None'}\n",
            "system",
            "ERROR"
        )
        
        return event_id

    def end_session(self, summary: str = "") -> None:
        """
        End the current session and commit to Git for tamper evidence.
        
        Args:
            summary: Optional summary of the session
        """
        if not self.session_id:
            return
        
        # Log session end
        end_data = {
            'session_id': self.session_id,
            'ended_at': datetime.utcnow().isoformat() + "Z",
            'summary': summary,
            'total_events': len(self.content_hashes)
        }
        
        self.log_event("SESSION_END", "system", end_data)
        self.log_human_readable(
            f"🏁 **Session Ended**\n"
            f"**Summary:** {summary}\n"
            f"**Total Events:** {len(self.content_hashes)}\n"
            f"**Ended:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}Z\n"
        )
        
        # Commit to Git for tamper evidence
        self._commit_to_git()
        
        # Reset session state
        self.session_id = None
        self.session_logs_dir = None
        self.conversation_id = None
        self.content_hashes = {}

    def get_session_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the current session.
        
        Returns:
            Dictionary containing session summary
        """
        if not self.session_id:
            return {}
        
        return {
            'session_id': self.session_id,
            'conversation_id': self.conversation_id,
            'total_events': len(self.content_hashes),
            'logs_directory': str(self.session_logs_dir) if self.session_logs_dir else None,
            'machine_log': str(self.session_logs_dir / f"{self.session_id}_machine.jsonl") if self.session_logs_dir else None,
            'human_log': str(self.session_logs_dir / f"{self.session_id}_human.md") if self.session_logs_dir else None
        }

    def _create_content_hash(self, data: Dict[str, Any]) -> str:
        """
        Create a tamper-evident hash of the content.
        
        Args:
            data: Data to hash
            
        Returns:
            SHA-256 hash of the data
        """
        content_str = json.dumps(data, sort_keys=True)
        return hashlib.sha256(content_str.encode()).hexdigest()[:12]

    def _commit_to_git(self) -> None:
        """
        Commit session logs to Git for tamper evidence.
        """
        if not self.git_repo or not self.session_logs_dir:
            return
        
        try:
            # Add all session files to Git
            for log_file in self.session_logs_dir.glob("*"):
                self.git_repo.index.add([str(log_file)])
            
            # Commit with descriptive message
            commit_message = f"UnifiedLogger session: {self.session_id}\n\nDual-track logging with forensic validation"
            self.git_repo.index.commit(commit_message)
            
            logger.info(f"📝 Session logs committed to Git: {self.session_id}")
            
        except Exception as e:
            logger.error(f"❌ Git commit failed: {e}") 