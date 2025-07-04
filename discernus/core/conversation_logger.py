#!/usr/bin/env python3
"""
Discernus Conversation Logger
==============================

Ultra-thin conversation logging system that records LLM dialogues verbatim
without parsing or structured data extraction. All analysis emerges from
conversation flow, not imposed data structures.

Core Discernus Principle: Conversation-Native Processing
- No parsing or data extraction from LLM responses
- Analysis emerges from conversation flow
- Complete transparency through Git logging
"""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
import git
import logging

logger = logging.getLogger(__name__)


class ConversationLogger:
    """
    Ultra-thin conversation logging without parsing
    
    Records all LLM interactions verbatim to Git for complete transparency
    and reproducibility. No structured data extraction or analysis.
    """
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.conversations_dir = self.project_root / "conversations"
        self.conversations_dir.mkdir(exist_ok=True)
        
        # Initialize Git repo if not exists
        try:
            self.git_repo = git.Repo(self.project_root)
        except git.exc.InvalidGitRepositoryError:
            self.git_repo = git.Repo.init(self.project_root)
        
        logger.info(f"ConversationLogger initialized: {self.conversations_dir}")
    
    def start_conversation(self, 
                          speech_text: str, 
                          research_question: str,
                          participants: List[str]) -> str:
        """
        Start a new conversation with specified LLM participants
        
        Args:
            speech_text: The text to analyze
            research_question: The research question driving the analysis
            participants: List of LLM "speakers" (e.g., ['populist_expert', 'pluralist_expert'])
            
        Returns:
            conversation_id: Unique identifier for this conversation
        """
        conversation_id = f"conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
        
        # Create conversation metadata
        metadata = {
            "conversation_id": conversation_id,
            "started_at": datetime.now().isoformat(),
            "research_question": research_question,
            "participants": participants,
            "speech_text": speech_text,
            "status": "active"
        }
        
        # Log conversation start
        self._log_message(conversation_id, "system", "CONVERSATION_START", metadata)
        
        return conversation_id
    
    def log_llm_message(self, 
                       conversation_id: str,
                       speaker: str,
                       message: str,
                       metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Log an LLM message to conversation
        
        Args:
            conversation_id: Conversation identifier
            speaker: LLM speaker name (e.g., 'populist_expert')
            message: Raw LLM response (no parsing)
            metadata: Optional metadata (model used, costs, etc.)
        """
        self._log_message(conversation_id, speaker, message, metadata)
    
    def log_code_execution(self,
                          conversation_id: str,
                          speaker: str,
                          code: str,
                          execution_result: Dict[str, Any]) -> None:
        """
        Log code execution within conversation
        
        Args:
            conversation_id: Conversation identifier
            speaker: LLM speaker who wrote the code
            code: Code that was executed
            execution_result: Results from code execution
        """
        code_log = {
            "type": "code_execution",
            "code": code,
            "execution_result": execution_result,
            "executed_at": datetime.now().isoformat()
        }
        
        self._log_message(conversation_id, f"{speaker}_code", "CODE_EXECUTION", code_log)
    
    def end_conversation(self, conversation_id: str, summary: str = "") -> None:
        """
        End conversation and commit to Git
        
        Args:
            conversation_id: Conversation identifier
            summary: Optional summary for Git commit
        """
        metadata = {
            "ended_at": datetime.now().isoformat(),
            "summary": summary,
            "status": "completed"
        }
        
        self._log_message(conversation_id, "system", "CONVERSATION_END", metadata)
        
        # Commit conversation to Git
        self._commit_conversation(conversation_id, summary)
    
    def _log_message(self, 
                    conversation_id: str,
                    speaker: str,
                    message: str,
                    metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Log a single message to conversation file
        
        Uses JSONL format for streaming and easy reading
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "conversation_id": conversation_id,
            "speaker": speaker,
            "message": message,
            "metadata": metadata or {}
        }
        
        conversation_file = self.conversations_dir / f"{conversation_id}.jsonl"
        
        with open(conversation_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
    
    def _commit_conversation(self, conversation_id: str, summary: str) -> None:
        """
        Commit conversation to Git for transparency
        """
        conversation_file = self.conversations_dir / f"{conversation_id}.jsonl"
        
        if conversation_file.exists():
            # Add to Git
            self.git_repo.index.add([str(conversation_file)])
            
            # Commit with descriptive message
            commit_message = f"Discernus conversation: {conversation_id}"
            if summary:
                commit_message += f"\n\n{summary}"
            
            self.git_repo.index.commit(commit_message)
            logger.info(f"Committed conversation to Git: {conversation_id}")
    
    def read_conversation(self, conversation_id: str) -> List[Dict[str, Any]]:
        """
        Read conversation history
        
        Returns:
            List of conversation messages in chronological order
        """
        conversation_file = self.conversations_dir / f"{conversation_id}.jsonl"
        
        if not conversation_file.exists():
            return []
        
        messages = []
        with open(conversation_file, "r", encoding="utf-8") as f:
            for line in f:
                messages.append(json.loads(line.strip()))
        
        return messages
    
    def list_conversations(self) -> List[Dict[str, Any]]:
        """
        List all conversations with basic metadata
        
        Returns:
            List of conversation summaries
        """
        conversations = []
        
        for conversation_file in self.conversations_dir.glob("*.jsonl"):
            try:
                # Read first and last messages for metadata
                with open(conversation_file, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    
                if lines:
                    first_msg = json.loads(lines[0].strip())
                    last_msg = json.loads(lines[-1].strip())
                    
                    conversations.append({
                        "conversation_id": first_msg["conversation_id"],
                        "started_at": first_msg["timestamp"],
                        "ended_at": last_msg["timestamp"],
                        "message_count": len(lines),
                        "status": last_msg.get("metadata", {}).get("status", "unknown")
                    })
            except Exception as e:
                logger.warning(f"Error reading conversation {conversation_file}: {e}")
        
        return sorted(conversations, key=lambda x: x["started_at"], reverse=True) 