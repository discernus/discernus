#!/usr/bin/env python3
"""
Discernus Ultra-Thin Orchestration Engine
===========================================

Implements the "strategically thin software" philosophy for multi-LLM conversation orchestration.

Core THIN Design Principles:
- LLMs talk to each other, software just orchestrates
- NO parsing or interpretation of LLM responses
- Raw text passing between LLMs
- Software provides minimal routing infrastructure only
- Design LLM → Human approval → Moderator LLM (no software intelligence)
"""

import sys
import os
import json
import asyncio
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import THIN LiteLLM client
try:
    from discernus.core.thin_litellm_client import ThinLiteLLMClient
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


class SessionPhase(Enum):
    """Phases of THIN research session"""
    DESIGN_CONSULTATION = "design_consultation"
    AWAITING_APPROVAL = "awaiting_approval"
    EXECUTING_ANALYSIS = "executing_analysis"
    COMPLETED = "completed"


@dataclass
class ResearchConfig:
    """Minimal research session configuration"""
    research_question: str
    source_texts: str
    enable_code_execution: bool = True


class ThinOrchestrator:
    """
    Ultra-thin orchestrator implementing pure LLM-to-LLM communication
    
    THIN Principles:
    1. NO parsing or interpretation of LLM responses
    2. Raw text passing between LLMs  
    3. Software provides routing only
    4. LLMs handle ALL intelligence decisions
    """
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        
        # Initialize components
        self.conversation_logger = ConversationLogger(project_root)
        
        # Initialize LLM client
        if LITELLM_AVAILABLE:
            self.llm_client = ThinLiteLLMClient()
        else:
            self.llm_client = None
            logger.warning("Running in mock mode - no actual LLM calls")
        
        # Session state (minimal)
        self.sessions: Dict[str, Dict[str, Any]] = {}
        
        logger.info(f"THIN Orchestrator initialized: {project_root}")
    
    async def start_research_session(self, config: ResearchConfig) -> str:
        """Start new research session with design consultation"""
        session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        self.sessions[session_id] = {
            'config': config,
            'phase': SessionPhase.DESIGN_CONSULTATION,
            'design_history': [],  # Track design iterations
            'approved_design': None,
            'conversation_id': None
        }
        
        logger.info(f"Started research session: {session_id}")
        return session_id
    
    async def run_design_consultation(self, session_id: str, human_feedback: str = "") -> str:
        """
        Get design proposal from design LLM
        
        THIN Principle: Pass feedback directly to LLM, no interpretation
        """
        if session_id not in self.sessions:
            raise ValueError(f"Session not found: {session_id}")
        
        session = self.sessions[session_id]
        config = session['config']
        
        # Build design consultation prompt including any feedback
        design_prompt = self._build_design_prompt(config, session['design_history'], human_feedback)
        
        logger.info("Consulting design LLM...")
        
        # Get design LLM response (raw text, no parsing)
        if self.llm_client:
            design_response = self.llm_client.call_llm(design_prompt, "design_llm")
        else:
            design_response = self._mock_design_response()
        
        # Store design response (as raw text)
        session['design_history'].append({
            'response': design_response,
            'feedback': human_feedback,
            'timestamp': datetime.now().isoformat()
        })
        
        session['phase'] = SessionPhase.AWAITING_APPROVAL
        
        logger.info("Design LLM consultation complete")
        return design_response
    
    def approve_design(self, session_id: str, approved: bool, feedback: str = "") -> bool:
        """
        Record human approval/rejection
        
        THIN Principle: Just record decision, no interpretation
        """
        if session_id not in self.sessions:
            raise ValueError(f"Session not found: {session_id}")
        
        session = self.sessions[session_id]
        
        if approved:
            # Store approved design (as raw text)
            session['approved_design'] = session['design_history'][-1]['response']
            session['phase'] = SessionPhase.EXECUTING_ANALYSIS
            logger.info("Design approved")
            return True
        else:
            # Return to design consultation with feedback
            session['phase'] = SessionPhase.DESIGN_CONSULTATION
            logger.info(f"Design rejected, feedback: {feedback}")
            return False
    
    async def execute_approved_analysis(self, session_id: str) -> Dict[str, Any]:
        """
        Execute analysis using approved design
        
        THIN Principle: Pass approved design text directly to moderator LLM
        """
        if session_id not in self.sessions:
            raise ValueError(f"Session not found: {session_id}")
        
        session = self.sessions[session_id]
        
        if session['phase'] != SessionPhase.EXECUTING_ANALYSIS:
            raise ValueError(f"Session not ready for execution")
        
        config = session['config']
        approved_design = session['approved_design']
        
        # Start conversation logging
        conversation_id = self.conversation_logger.start_conversation(
            speech_text=config.source_texts,
            research_question=config.research_question,
            participants=["moderator_llm"]  # Moderator will determine actual participants
        )
        
        session['conversation_id'] = conversation_id
        
        # Execute analysis via moderator LLM (no parsing, just text passing)
        results = await self._execute_via_moderator(
            conversation_id, approved_design, config
        )
        
        session['phase'] = SessionPhase.COMPLETED
        
        logger.info("Analysis execution completed")
        return results
    
    async def _execute_via_moderator(self, 
                                   conversation_id: str,
                                   approved_design: str,
                                   config: ResearchConfig) -> Dict[str, Any]:
        """
        Execute analysis by passing approved design to moderator LLM
        
        THIN Principle: Moderator LLM interprets design and orchestrates analysis
        """
        # Build moderator prompt with approved design
        moderator_prompt = f"""
You are the moderator_llm responsible for executing this approved research design.

RESEARCH QUESTION: {config.research_question}

SOURCE TEXTS:
{config.source_texts}

APPROVED DESIGN:
{approved_design}

Your Task:
1. Read and interpret the approved design
2. Determine what expert LLMs are needed
3. Orchestrate the multi-LLM conversation to answer the research question
4. Each time you want an expert to contribute, request their input
5. Synthesize findings into a final analysis

Begin by interpreting the design and requesting input from the first expert you need.
If you need code execution for analysis, write Python code in ```python blocks.
"""
        
        # Start moderator conversation
        logger.info("Starting moderator-orchestrated analysis...")
        
        if self.llm_client:
            moderator_response = self.llm_client.call_llm(moderator_prompt, "moderator_llm")
        else:
            moderator_response = "[MOCK] Moderator would orchestrate analysis based on approved design"
        
        # Log moderator's initial response
        self.conversation_logger.log_llm_message(
            conversation_id, "moderator_llm", moderator_response,
            metadata={'role': 'moderator', 'stage': 'design_interpretation'}
        )
        
        # Handle code execution if needed
        if config.enable_code_execution and '```python' in moderator_response:
            enhanced_response = process_llm_notebook_request(
                conversation_id, "moderator_llm", moderator_response
            )
            
            if enhanced_response != moderator_response:
                self.conversation_logger.log_llm_message(
                    conversation_id, "moderator_llm", enhanced_response,
                    metadata={'enhanced_with_code': True, 'stage': 'design_interpretation'}
                )
        
        # For now, this is a simplified implementation
        # In full implementation, moderator would continue orchestrating expert conversations
        
        # End conversation
        self.conversation_logger.end_conversation(
            conversation_id, "Analysis orchestrated by moderator LLM"
        )
        
        return {
            'conversation_id': conversation_id,
            'status': 'completed',
            'summary': 'Analysis completed via moderator LLM orchestration'
        }
    
    def _build_design_prompt(self, 
                           config: ResearchConfig,
                           design_history: List[Dict[str, Any]],
                           human_feedback: str) -> str:
        """
        Build design consultation prompt
        
        THIN Principle: Include feedback directly, no interpretation
        """
        base_prompt = f"""
You are a design_llm expert in computational research methodology.

RESEARCH QUESTION: {config.research_question}

SOURCE TEXTS:
{config.source_texts}

Your Task: Design a multi-LLM conversation approach to answer this research question.

Provide a detailed design proposal including:
- Analysis approach and methodology
- What expert perspectives are needed
- How the conversation should be orchestrated
- Any computational analysis required

Focus on rigorous, academically sound analysis.
"""
        
        # Add design history and feedback
        if design_history:
            base_prompt += f"\n\nPREVIOUS DESIGN ITERATIONS:\n"
            for i, iteration in enumerate(design_history):
                base_prompt += f"\nIteration {i+1}:\n{iteration['response']}\n"
                if iteration['feedback']:
                    base_prompt += f"Feedback received: {iteration['feedback']}\n"
        
        if human_feedback:
            base_prompt += f"\n\nHUMAN RESEARCHER FEEDBACK:\n{human_feedback}\n"
            base_prompt += "\nPlease revise your design based on this feedback."
        
        return base_prompt
    
    def _mock_design_response(self) -> str:
        """Mock design response for testing"""
        return """
I propose a multi-perspective analysis approach:

1. Use computational linguistics expert for quantitative text analysis
2. Use political discourse expert for rhetorical analysis  
3. Use social cohesion expert for unity/division assessment
4. Include enmity/amity dipole measurement as requested

The moderator should orchestrate these experts in sequence, building on each other's findings.
"""
    
    def get_session_status(self, session_id: str) -> Dict[str, Any]:
        """Get session status"""
        if session_id not in self.sessions:
            return {'status': 'not_found'}
        
        session = self.sessions[session_id]
        return {
            'status': session['phase'].value,
            'research_question': session['config'].research_question,
            'design_iterations': len(session['design_history']),
            'conversation_id': session.get('conversation_id')
        }
    
    def cleanup_session(self, session_id: str) -> None:
        """Clean up session"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            logger.info(f"Cleaned up session: {session_id}")


# Keep old names for compatibility
ThinDiscernusOrchestrator = ThinOrchestrator
ConversationConfig = ResearchConfig 