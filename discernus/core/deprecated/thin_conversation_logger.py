#!/usr/bin/env python3
"""
Ultra-Thin Conversation Logger
=============================

Simple conversation logging following THIN principles.
Just appends messages to files, no parsing or intelligence.
"""

from pathlib import Path
from datetime import datetime


class ThinConversationLogger:
    """Ultra-thin conversation logger - just appends, no intelligence"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
    
    def log_message(self, session_id: str, role: str, message: str):
        """Simple message logging with conversational dialogue format"""
        log_file = self.project_root / "research_sessions" / session_id / "conversation_log.md"
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Full timestamp for precision (UTC for global academic collaboration)
        utc_now = datetime.utcnow()
        full_timestamp = utc_now.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3] + "Z"
        time_only = utc_now.strftime("%H:%M:%S") + "Z"
        
        # Make role names more conversational
        role_names = {
            'user': 'Researcher',
            'user_feedback': 'Researcher', 
            'design': 'Design LLM',
            'moderator': 'Moderator LLM',
            'specialist': 'Specialist LLM',
            'adversarial': 'Adversarial LLM',
            'analysis': 'Analysis LLM',
            'referee': 'Referee LLM'
        }
        
        speaker = role_names.get(role.lower(), role.title())
        
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"\n**{speaker} said** *(at {time_only})*:\n\n{message}\n\n---\n")
    
    def log_code_execution(self, session_id: str, role: str, code: str, result: str):
        """Log code execution results in conversational format"""
        # Log to main conversation
        role_names = {
            'design': 'Design LLM',
            'moderator': 'Moderator LLM', 
            'specialist': 'Specialist LLM',
            'adversarial': 'Adversarial LLM',
            'analysis': 'Analysis LLM',
            'referee': 'Referee LLM'
        }
        
        speaker = role_names.get(role.lower(), role.title())
        time_only = datetime.utcnow().strftime("%H:%M:%S") + "Z"
        
        code_message = f"{speaker} executed code:\n\n```python\n{code}\n```\n\n**Result:**\n```\n{result}\n```"
        
        # Log to main conversation 
        self.log_message(session_id, f"{role}_code", code_message)
        
        # Also save to separate code file for reference
        log_file = self.project_root / "research_sessions" / session_id / "generated_code" / f"{role}_code.md"
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        full_timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3] + "Z"
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"\n**{speaker} executed code** *(at {time_only})*:\n\n```python\n{code}\n```\n")
            f.write(f"**Result:**\n```\n{result}\n```\n\n---\n")
    
    def read_conversation(self, session_id: str) -> str:
        """Read complete conversation log"""
        log_file = self.project_root / "research_sessions" / session_id / "conversation_log.md"
        return log_file.read_text() if log_file.exists() else "" 