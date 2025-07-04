#!/usr/bin/env python3
"""
Discernus Ultra-Thin Orchestration Engine
===========================================

Implements the "strategically thin software" philosophy using Redis/Celery
for multi-LLM conversation orchestration with secure code execution.

Core Design Principles:
- Minimal custom code focused on enabling conversation
- Leverage mature infrastructure (Redis, Celery, Git, Docker)
- Software orchestrates rather than interprets or analyzes
- Maximum functionality with minimum complexity
"""

import sys
import os
import json
import asyncio
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
from dataclasses import dataclass

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import existing LiteLLM client
try:
    from discernus.gateway.reboot_litellm_client import LiteLLMClient
    LITELLM_AVAILABLE = True
except ImportError:
    LITELLM_AVAILABLE = False
    logging.warning("LiteLLM client not available - using mock responses")

# Import Discernus components
from discernus.core.conversation_logger import ConversationLogger
from discernus.core.simple_code_executor import process_llm_notebook_request, extract_code_blocks

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@dataclass
class ConversationConfig:
    """Configuration for a multi-LLM conversation"""
    research_question: str
    participants: List[str]
    speech_text: str
    models: Dict[str, str]  # participant -> model mapping
    max_turns: int = 10
    enable_code_execution: bool = True
    code_review_model: str = "claude-3-5-sonnet"


class DiscernusOrchestrator:
    """
    Ultra-thin orchestration engine for multi-LLM conversations
    
    Implements Discernus's "strategically thin software" philosophy:
    - Minimal custom orchestration logic
    - Conversation-native processing (no parsing)
    - Complete transparency through Git logging
    - Secure code execution integration
    """
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        
        # Initialize Discernus components
        self.conversation_logger = ConversationLogger(project_root)
        
        # Initialize LLM client
        if LITELLM_AVAILABLE:
            self.llm_client = LiteLLMClient()
        else:
            self.llm_client = None
        
        # Conversation state
        self.active_conversations: Dict[str, ConversationConfig] = {}
        
        logger.info(f"Discernus Orchestrator initialized: {project_root}")
    
    async def start_conversation(self, config: ConversationConfig) -> str:
        """
        Start a new multi-LLM conversation
        
        Args:
            config: Conversation configuration
            
        Returns:
            conversation_id: Unique identifier for this conversation
        """
        # Start conversation logging
        conversation_id = self.conversation_logger.start_conversation(
            speech_text=config.speech_text,
            research_question=config.research_question,
            participants=config.participants
        )
        
        # Store conversation config
        self.active_conversations[conversation_id] = config
        
        logger.info(f"Started conversation: {conversation_id}")
        logger.info(f"Participants: {config.participants}")
        logger.info(f"Code execution: {'enabled' if config.enable_code_execution else 'disabled'}")
        
        return conversation_id
    
    async def run_conversation(self, conversation_id: str) -> Dict[str, Any]:
        """
        Run the complete conversation flow
        
        Args:
            conversation_id: Conversation identifier
            
        Returns:
            Conversation results and metadata
        """
        if conversation_id not in self.active_conversations:
            raise ValueError(f"Conversation not found: {conversation_id}")
        
        config = self.active_conversations[conversation_id]
        
        # Initialize conversation with research question
        context = self._build_initial_context(config)
        
        # Run conversation turns
        for turn in range(config.max_turns):
            logger.info(f"Starting turn {turn + 1}/{config.max_turns}")
            
            # Each participant speaks
            for participant in config.participants:
                model = config.models.get(participant, "claude-3-5-sonnet")
                
                # Get participant's response
                response = await self._get_participant_response(
                    conversation_id, participant, model, context
                )
                
                # Log the response
                self.conversation_logger.log_llm_message(
                    conversation_id, participant, response['message'],
                    metadata={'model': model, 'turn': turn + 1}
                )
                
                # Handle code execution if requested
                if config.enable_code_execution and response.get('code_requested'):
                    # Ultra-thin: just process code blocks and enhance response
                    enhanced_response = process_llm_notebook_request(
                        conversation_id, participant, response['message']
                    )
                    
                    # Log the enhanced response (with code results)
                    if enhanced_response != response['message']:
                        self.conversation_logger.log_llm_message(
                            conversation_id, f"{participant}_code_results", enhanced_response,
                            metadata={'enhanced_with_code': True}
                        )
                
                # Update context for next participant
                context = self._update_context(context, participant, response)
            
            # Check for conversation completion
            if self._is_conversation_complete(context):
                logger.info(f"Conversation completed at turn {turn + 1}")
                break
        
        # End conversation
        summary = self._generate_summary(conversation_id, context)
        self.conversation_logger.end_conversation(conversation_id, summary)
        
        # Clean up
        del self.active_conversations[conversation_id]
        
        return {
            'conversation_id': conversation_id,
            'turns_completed': turn + 1,
            'summary': summary,
            'participants': config.participants
        }
    
    async def _get_participant_response(self, 
                                      conversation_id: str,
                                      participant: str,
                                      model: str,
                                      context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get response from a specific participant
        
        Args:
            conversation_id: Conversation identifier
            participant: Participant name
            model: LLM model to use
            context: Current conversation context
            
        Returns:
            Dictionary with participant response
        """
        # Build participant-specific prompt
        prompt = self._build_participant_prompt(participant, context)
        
        # Get LLM response
        if self.llm_client:
            try:
                response_text, cost = await self.llm_client._litellm_call_basic(prompt, model)
                if isinstance(response_text, dict) and 'raw_response' in response_text:
                    response_text = response_text['raw_response']
                
                # Parse response for code execution requests
                code_request = self._parse_code_request(response_text)
                
                return {
                    'message': response_text,
                    'code_requested': code_request['requested'],
                    'code': code_request.get('code', ''),
                    'cost': cost,
                    'model': model
                }
            except Exception as e:
                logger.error(f"LLM call failed for {participant}: {e}")
                return {
                    'message': f"[ERROR] LLM call failed: {str(e)}",
                    'code_requested': False,
                    'code': '',
                    'cost': 0,
                    'model': model
                }
        else:
            # Mock response for testing
            return {
                'message': f"[MOCK] {participant} response to: {context['research_question']}",
                'code_requested': False,
                'code': '',
                'cost': 0,
                'model': model
            }
    
    def _build_participant_prompt(self, 
                                 participant: str,
                                 context: Dict[str, Any]) -> str:
        """
        Build prompt for specific participant
        
        Args:
            participant: Participant name
            context: Current conversation context
            
        Returns:
            Formatted prompt string
        """
        base_prompt = f"""
You are {participant}, an expert in political discourse analysis.

Research Question: {context['research_question']}

Text to Analyze:
{context['speech_text']}

Previous Discussion:
{context.get('previous_discussion', 'None yet.')}

Your Task:
Provide your expert analysis of this text. If you need to perform calculations, 
statistical analysis, or create visualizations to support your analysis, 
you can write Python code by starting a code block with ```python and ending with ```.

Focus on your area of expertise and engage with any previous analyses from other experts.
"""
        
        # Add participant-specific instructions
        if participant == 'populist_expert':
            base_prompt += """
As a populist discourse expert, focus on:
- People vs. elite framing
- Anti-establishment rhetoric
- Appeals to ordinary citizens
- Moral boundary drawing
- Claims of representation
"""
        elif participant == 'pluralist_expert':
            base_prompt += """
As a pluralist discourse expert, focus on:
- Democratic cooperation
- Institutional respect
- Compromise and consensus
- Diverse stakeholder inclusion
- Procedural fairness
"""
        elif participant == 'code_reviewer':
            base_prompt += """
As a code reviewer, focus on:
- Academic appropriateness of proposed code
- Security concerns
- Resource usage
- Compliance with research standards
"""
        
        return base_prompt
    
    def _parse_code_request(self, response_text: str) -> Dict[str, Any]:
        """
        Check if response contains code blocks
        
        Args:
            response_text: Raw LLM response
            
        Returns:
            Dictionary with code request information
        """
        code_blocks = extract_code_blocks(response_text)
        
        return {
            'requested': len(code_blocks) > 0,
            'code_blocks': code_blocks
        }
    
    def _build_initial_context(self, config: ConversationConfig) -> Dict[str, Any]:
        """
        Build initial conversation context
        
        Args:
            config: Conversation configuration
            
        Returns:
            Initial context dictionary
        """
        return {
            'research_question': config.research_question,
            'speech_text': config.speech_text,
            'participants': config.participants,
            'previous_discussion': '',
            'turn': 0
        }
    
    def _update_context(self, 
                       context: Dict[str, Any],
                       participant: str,
                       response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update conversation context with new response
        
        Args:
            context: Current context
            participant: Participant who responded
            response: Response dictionary
            
        Returns:
            Updated context
        """
        # Simple context update - just append to discussion
        context['previous_discussion'] += f"\n\n{participant}: {response['message']}"
        context['turn'] += 1
        
        return context
    
    def _is_conversation_complete(self, context: Dict[str, Any]) -> bool:
        """
        Check if conversation is complete
        
        Args:
            context: Current conversation context
            
        Returns:
            True if conversation should end
        """
        # Simple completion check - could be enhanced
        return context['turn'] >= len(context['participants']) * 2
    
    def _generate_summary(self, 
                         conversation_id: str,
                         context: Dict[str, Any]) -> str:
        """
        Generate conversation summary
        
        Args:
            conversation_id: Conversation identifier
            context: Final conversation context
            
        Returns:
            Summary string
        """
        return f"Multi-LLM conversation completed with {len(context['participants'])} participants"
    
    def get_conversation_status(self, conversation_id: str) -> Dict[str, Any]:
        """
        Get status of active conversation
        
        Args:
            conversation_id: Conversation identifier
            
        Returns:
            Status dictionary
        """
        if conversation_id in self.active_conversations:
            config = self.active_conversations[conversation_id]
            return {
                'status': 'active',
                'participants': config.participants,
                'research_question': config.research_question,
                'code_execution_enabled': config.enable_code_execution
            }
        else:
            return {
                'status': 'not_found'
            }
    
    def list_conversations(self) -> List[Dict[str, Any]]:
        """
        List all conversations (active and completed)
        
        Returns:
            List of conversation summaries
        """
        return self.conversation_logger.list_conversations()
    
    def cleanup_resources(self) -> None:
        """
        Clean up resources for completed conversations
        """
        # Could implement cleanup logic here
        pass 