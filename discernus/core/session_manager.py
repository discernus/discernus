#!/usr/bin/env python3
"""
Ultra-Thin Session Manager
=========================

Basic session lifecycle management following THIN principles.
Just creates sessions and manages Git commits.
"""

import git
from pathlib import Path
from datetime import datetime


class SessionManager:
    """Ultra-thin session manager - just lifecycle, no intelligence"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.git_repo = git.Repo(project_root)
    
    def create_session(self, research_question: str) -> str:
        """Create new research session"""
        session_id = f"lincoln_trump_mvp_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
        session_path = self.project_root / "research_sessions" / session_id
        session_path.mkdir(parents=True, exist_ok=True)
        
        # Create session metadata
        with open(session_path / "metadata.txt", 'w') as f:
            f.write(f"Research Question: {research_question}\n")
            f.write(f"Started: {datetime.now().isoformat()}\n")
        
        return session_id
    
    def end_session(self, session_id: str):
        """End session and commit to Git"""
        session_path = self.project_root / "research_sessions" / session_id
        if session_path.exists():
            self.git_repo.index.add([str(session_path)])
            self.git_repo.index.commit(f"Research session: {session_id}") 