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
import threading
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
import git
import logging

# Import Redis for event capture
try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

logger = logging.getLogger(__name__)


class ConversationLogger:
    """
    Ultra-thin conversation logging without parsing
    
    Records all LLM interactions verbatim to Git for complete transparency
    and reproducibility. No structured data extraction or analysis.
    
    Enhanced with Redis event capture for complete chronological logging.
    """
    
    def __init__(self, project_root: str = ".", custom_conversations_dir: Optional[str] = None):
        self.project_root = Path(project_root)
        
        # Use custom conversations directory if provided, otherwise use default
        if custom_conversations_dir:
            self.conversations_dir = Path(custom_conversations_dir)
        else:
            self.conversations_dir = self.project_root / "conversations"
        
        self.conversations_dir.mkdir(exist_ok=True)
        
        # Initialize Git repo by searching parent directories (NEVER create a new one)
        try:
            self.git_repo = git.Repo(self.project_root, search_parent_directories=True)
        except git.InvalidGitRepositoryError:
            # This is the expected case when running in a non-git directory.
            # NEVER create a new git repository - this prevents nested repos.
            self.git_repo = None
        
        # Initialize Redis client for event capture
        self.redis_client = None
        self.redis_pubsub = None
        self.redis_thread = None
        self.active_conversations = set()
        
        if REDIS_AVAILABLE:
            try:
                self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
                self.redis_client.ping()  # Test connection
                logger.info("Redis connected for event capture")
            except Exception as e:
                logger.warning(f"Redis unavailable for event capture: {e}")
                self.redis_client = None
        
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
        conversation_id = f"conversation_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
        
        # Create conversation metadata
        metadata = {
            "conversation_id": conversation_id,
            "started_at": datetime.utcnow().isoformat() + "Z",
            "research_question": research_question,
            "participants": participants,
            "speech_text": speech_text,
            "status": "active"
        }
        
        # Log conversation start
        self._log_message(conversation_id, "system", "CONVERSATION_START", metadata)
        
        # Start Redis event capture for this conversation
        self._start_redis_capture(conversation_id)
        
        return conversation_id
    
    def _start_redis_capture(self, conversation_id: str) -> None:
        """
        Start Redis event capture for a conversation
        
        Captures Discernus events (agent spawning, completions, etc.) and logs them
        alongside LLM messages for complete chronological record.
        """
        if not self.redis_client:
            return
        
        # Add to active conversations
        self.active_conversations.add(conversation_id)
        
        # Start Redis subscriber thread if not already running
        if not self.redis_thread or not self.redis_thread.is_alive():
            self.redis_pubsub = self.redis_client.pubsub()
            self.redis_pubsub.psubscribe('discernus.*')
            self.redis_thread = threading.Thread(target=self._redis_event_listener, daemon=True)
            self.redis_thread.start()
            logger.info(f"Started Redis event capture for conversation: {conversation_id}")
    
    def _redis_event_listener(self) -> None:
        """
        Listen for Redis events and log them to active conversations
        """
        if not self.redis_pubsub:
            return
        
        try:
            for message in self.redis_pubsub.listen():
                if message['type'] == 'pmessage':
                    # Parse Redis event
                    channel = message['channel'].decode('utf-8')
                    try:
                        event_data = json.loads(message['data'].decode('utf-8'))
                        session_id = event_data.get('session_id', 'unknown_session')
                        
                        # Log event to all active conversations
                        # (In practice, there's usually only one active conversation)
                        for conversation_id in list(self.active_conversations):
                            self._log_redis_event(conversation_id, channel, event_data)
                            
                    except json.JSONDecodeError as e:
                        logger.warning(f"Failed to parse Redis event: {e}")
                        
        except Exception as e:
            logger.warning(f"Redis event listener error: {e}")
    
    def _log_redis_event(self, conversation_id: str, channel: str, event_data: Dict[str, Any]) -> None:
        """
        Log a Redis event to the conversation log
        """
        # Create a formatted message for the Redis event
        event_message = self._format_redis_event(channel, event_data)
        
        # Log as a system message with Redis metadata
        redis_metadata = {
            "type": "redis_event",
            "channel": channel,
            "event_data": event_data,
            "timestamp": event_data.get('timestamp', datetime.utcnow().isoformat() + "Z")
        }
        
        self._log_message(conversation_id, "system", event_message, redis_metadata)
    
    def _format_redis_event(self, channel: str, event_data: Dict[str, Any]) -> str:
        """
        Format Redis event for human-readable logging
        """
        message_type = event_data.get('message_type', 'unknown')
        
        if channel == 'discernus.agent.spawned':
            agent_type = event_data.get('agent_type', 'unknown_agent')
            agent_role = event_data.get('agent_role', 'unknown_role')
            return f"AGENT_SPAWNED: {agent_type} ({agent_role})"
        
        elif channel == 'discernus.agent.completed':
            agent_type = event_data.get('agent_type', 'unknown_agent')
            turn = event_data.get('turn', 'unknown')
            return f"AGENT_COMPLETED: {agent_type} (turn {turn})"
        
        elif channel == 'discernus.session.start':
            research_question = event_data.get('research_question', 'unknown')
            return f"SESSION_START: {research_question}"
        
        elif channel == 'discernus.validation.started':
            return f"VALIDATION_STARTED"
        
        elif channel == 'discernus.framework.validated':
            return f"FRAMEWORK_VALIDATED"
        
        else:
            return f"DISCERNUS_EVENT: {channel} - {message_type}"

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
            "executed_at": datetime.utcnow().isoformat() + "Z"
        }
        
        self._log_message(conversation_id, f"{speaker}_code", "CODE_EXECUTION", code_log)
    
    def end_conversation(self, conversation_id: str, summary: str = "") -> None:
        """
        End conversation and commit to Git
        
        Args:
            conversation_id: Conversation identifier
            summary: Optional summary for Git commit
        """
        # Remove from active conversations (stops Redis event capture)
        self.active_conversations.discard(conversation_id)
        
        metadata = {
            "ended_at": datetime.utcnow().isoformat() + "Z",
            "summary": summary,
            "status": "completed"
        }
        
        self._log_message(conversation_id, "system", "CONVERSATION_END", metadata)
        
        # Commit conversation to Git
        self._commit_conversation(conversation_id, summary)
        
        # Stop Redis listener if no active conversations
        if not self.active_conversations and self.redis_pubsub:
            self.redis_pubsub.close()
            self.redis_pubsub = None
            logger.info("Stopped Redis event capture - no active conversations")

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
            "timestamp": datetime.utcnow().isoformat() + "Z",
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
            # Add to Git (only if git repo is available)
            if self.git_repo is not None:
                self.git_repo.index.add([str(conversation_file)])
                
                # Commit with descriptive message
                commit_message = f"Discernus conversation: {conversation_id}"
                if summary:
                    commit_message += f"\n\n{summary}"
                
                self.git_repo.index.commit(commit_message)
                logger.info(f"Committed conversation to Git: {conversation_id}")
            else:
                logger.info(f"Git unavailable, conversation saved to file: {conversation_id}")
    
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