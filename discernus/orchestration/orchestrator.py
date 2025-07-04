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
from discernus.core.conversation_formatter import format_conversation_to_markdown
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
    
    def _create_session_folder(self, session_id: str, config: ResearchConfig) -> Path:
        """Create session folder in research_sessions/ with proper structure"""
        session_path = self.project_root / "research_sessions" / session_id
        session_path.mkdir(parents=True, exist_ok=True)
        
        # Create session metadata
        metadata = {
            'session_id': session_id,
            'research_question': config.research_question,
            'started_at': datetime.now().isoformat(),
            'status': 'active',
            'enable_code_execution': config.enable_code_execution
        }
        
        with open(session_path / "metadata.json", 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return session_path
    
    async def start_research_session(self, config: ResearchConfig) -> str:
        """Start new research session with proper session structure"""
        session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Create session folder
        session_path = self._create_session_folder(session_id, config)
        
        self.sessions[session_id] = {
            'config': config,
            'phase': SessionPhase.DESIGN_CONSULTATION,
            'design_history': [],  # Track design iterations
            'approved_design': None,
            'conversation_id': None,
            'session_path': session_path
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
        Execute analysis using approved design with proper session management
        
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
            conversation_id, approved_design, config, session
        )
        
        # Create readable markdown in session folder
        await self._create_session_readable_markdown(session_id, conversation_id)
        
        session['phase'] = SessionPhase.COMPLETED
        
        logger.info("Analysis execution completed")
        return results
    
    async def _create_session_readable_markdown(self, session_id: str, conversation_id: str):
        """Create readable markdown file in the session folder"""
        session = self.sessions[session_id]
        session_path = session['session_path']
        
        # Generate markdown content
        markdown_content = format_conversation_to_markdown(conversation_id, str(self.project_root))
        
        # Save to session folder
        readable_file = session_path / "conversation_readable.md"
        with open(readable_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        # Also copy the JSONL file to session folder for completeness
        jsonl_source = self.project_root / "conversations" / f"{conversation_id}.jsonl"
        jsonl_dest = session_path / "conversation_log.jsonl"
        
        if jsonl_source.exists():
            import shutil
            shutil.copy2(jsonl_source, jsonl_dest)
        
        logger.info(f"Created readable markdown: {readable_file}")
    
    async def _execute_via_moderator(self, 
                                   conversation_id: str,
                                   approved_design: str,
                                   config: ResearchConfig,
                                   session: Dict[str, Any]) -> Dict[str, Any]:
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
4. Each time you want an expert to contribute, clearly request their input
5. Continue until you have sufficient analysis to answer the research question
6. Synthesize findings into a final analysis

IMPORTANT: When you need expert input, format your request as:
REQUEST TO [expert_name]: [your request]

When you're ready to provide final conclusions, format as:
FINAL ANALYSIS: [your conclusions]

Begin by interpreting the design and requesting input from the first expert you need.
If you need code execution for analysis, write Python code in ```python blocks.
"""
        
        # Start moderator conversation
        logger.info("Starting moderator-orchestrated analysis...")
        turn = 1
        max_turns = 20  # Prevent infinite loops
        
        conversation_history = []
        current_prompt = moderator_prompt
        
        while turn <= max_turns:
            logger.info(f"Moderator turn {turn}")
            
            # Get moderator response
            if self.llm_client:
                moderator_response = self.llm_client.call_llm(current_prompt, "moderator_llm")
            else:
                moderator_response = f"[MOCK] Moderator turn {turn}: Would request expert analysis and synthesize results"
            
            # Handle code execution BEFORE logging (to avoid duplicates)
            if config.enable_code_execution and '```python' in moderator_response:
                enhanced_response = process_llm_notebook_request(
                    conversation_id, "moderator_llm", moderator_response
                )
                
                if enhanced_response != moderator_response:
                    moderator_response = enhanced_response
            
            # Log moderator's response (enhanced if code was executed)
            self.conversation_logger.log_llm_message(
                conversation_id, "moderator_llm", moderator_response,
                metadata={'role': 'moderator', 'turn': turn, 'code_executed': '```python' in moderator_response}
            )
            
            # Check if moderator is requesting expert input
            if "REQUEST TO " in moderator_response:
                # Extract expert request
                expert_response = await self._handle_expert_request(
                    conversation_id, moderator_response, config, turn
                )
                
                # Update conversation history
                conversation_history.append(f"Moderator: {moderator_response}")
                conversation_history.append(f"Expert Response: {expert_response}")
                
                # Prepare next prompt for moderator with expert response
                current_prompt = f"""
Continue orchestrating the analysis. Here's what has happened so far:

CONVERSATION HISTORY:
{chr(10).join(conversation_history[-6:])}  # Last 6 entries to keep context manageable

Based on the expert response above, either:
1. Request input from another expert (use "REQUEST TO [expert_name]: [request]")
2. Ask follow-up questions to the same expert
3. Provide your FINAL ANALYSIS if you have sufficient information

Continue the analysis.
"""
            
            elif "FINAL ANALYSIS:" in moderator_response:
                # Moderator has completed the analysis
                logger.info("Moderator completed final analysis")
                break
            
            else:
                # Moderator is continuing without expert requests
                conversation_history.append(f"Moderator: {moderator_response}")
                
                # Prepare continuation prompt
                current_prompt = f"""
Continue your analysis. Current conversation:

{chr(10).join(conversation_history[-4:])}

Either request expert input or provide your FINAL ANALYSIS.
"""
            
            turn += 1
        
        if turn > max_turns:
            logger.warning("Moderator conversation reached maximum turns")
        
        # End conversation
        self.conversation_logger.end_conversation(
            conversation_id, "Multi-LLM analysis orchestrated by moderator LLM"
        )
        
        return {
            'conversation_id': conversation_id,
            'status': 'completed',
            'turns': turn - 1,
            'summary': 'Multi-LLM analysis completed via moderator orchestration'
        }
    
    async def _handle_expert_request(self,
                                   conversation_id: str,
                                   moderator_request: str,
                                   config: ResearchConfig,
                                   turn: int) -> str:
        """
        Handle moderator's request for expert input
        
        THIN Principle: Expert LLMs respond to moderator's specific requests
        """
        # Extract expert name and request from moderator's message
        import re
        
        # Look for "REQUEST TO expert_name: request text"
        match = re.search(r'REQUEST TO ([^:]+):\s*(.+)', moderator_request, re.DOTALL)
        
        if not match:
            return "[ERROR] Could not parse expert request format"
        
        expert_name = match.group(1).strip()
        expert_request = match.group(2).strip()
        
        logger.info(f"Handling request to {expert_name}")
        
        # Build expert prompt
        expert_prompt = f"""
You are {expert_name}, a specialized expert LLM.

RESEARCH QUESTION: {config.research_question}

SOURCE TEXTS:
{config.source_texts}

The moderator_llm has requested your expertise:

MODERATOR REQUEST: {expert_request}

Your Task:
Provide your expert analysis based on your specialization. Be specific and thorough.
If you need to perform calculations or analysis, write Python code in ```python blocks.

Focus on your area of expertise and directly address the moderator's request.
"""
        
        # Get expert response
        if self.llm_client:
            expert_response = self.llm_client.call_llm(expert_prompt, expert_name)
        else:
            expert_response = f"[MOCK] {expert_name} would provide specialized analysis addressing: {expert_request}"
        
        # Handle code execution BEFORE logging (to avoid duplicates)
        if config.enable_code_execution and '```python' in expert_response:
            enhanced_response = process_llm_notebook_request(
                conversation_id, expert_name, expert_response
            )
            
            if enhanced_response != expert_response:
                expert_response = enhanced_response
        
        # Log expert response (enhanced if code was executed)
        self.conversation_logger.log_llm_message(
            conversation_id, expert_name, expert_response,
            metadata={'role': 'expert', 'turn': turn, 'requested_by': 'moderator_llm', 'code_executed': '```python' in expert_response}
        )
        
        return expert_response
    
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