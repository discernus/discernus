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
import uuid
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

# SOAR v2.0 Redis chronolog import
try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    logging.warning("Redis not available - chronolog events will not be published")

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

# Import knowledgenaut research infrastructure
try:
    from discernus.core.knowledgenaut import UltraThinKnowledgenaut
    KNOWLEDGENAUT_AVAILABLE = True
except ImportError:
    KNOWLEDGENAUT_AVAILABLE = False
    logging.warning("Knowledgenaut research infrastructure not available")

# Import corpus inspection infrastructure
try:
    from discernus.core.corpus_inspector import CorpusInspector
    CORPUS_INSPECTOR_AVAILABLE = True
except ImportError:
    CORPUS_INSPECTOR_AVAILABLE = False
    logging.warning("Corpus inspector infrastructure not available")

# Import Discernus components
from discernus.core.conversation_logger import ConversationLogger
from discernus.core.conversation_formatter import format_conversation_to_markdown
from discernus.core.secure_code_executor import process_llm_code_request, extract_code_blocks
from discernus.core.llm_roles import get_expert_prompt, get_simulated_researcher_prompt
from discernus.core.thin_validation import check_thin_compliance



# Configure logging first
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# THIN Architecture: For validation, run: 
# python3 -c "from discernus.core.thin_validation import check_thin_compliance; check_thin_compliance()"


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
    framework_content: str = ""  # Framework specification content
    enable_code_execution: bool = True
    dev_mode: bool = False  # Enable automated human simulation for testing
    simulated_researcher_profile: str = "experienced_computational_social_scientist"  # Profile for AI responses


class ThinOrchestrator:
    """
    Ultra-thin orchestrator implementing pure LLM-to-LLM communication
    
    THIN Principles:
    1. NO parsing or interpretation of LLM responses
    2. Raw text passing between LLMs  
    3. Software provides routing only
    4. LLMs handle ALL intelligence decisions
    """
    
    def __init__(self, project_root: str = ".", custom_session_path: Optional[str] = None):
        self.project_root = Path(project_root)
        self.custom_session_path = Path(custom_session_path) if custom_session_path else None
        
        # Initialize components - if custom session path is provided, log directly there
        if self.custom_session_path:
            self.conversation_logger = ConversationLogger(project_root, str(self.custom_session_path))
        else:
            self.conversation_logger = ConversationLogger(project_root)
        
        # Initialize LLM client
        if LITELLM_AVAILABLE:
            self.llm_client = ThinLiteLLMClient()
        else:
            self.llm_client = None
            logger.warning("Running in mock mode - no actual LLM calls")
        
        # SOAR v2.0: Initialize Redis chronolog client
        if REDIS_AVAILABLE:
            try:
                self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
                self.redis_client.ping()  # Test connection
                logger.info("SOAR v2.0 chronolog connected")
            except Exception as e:
                self.redis_client = None
                logger.warning(f"Redis chronolog unavailable: {e}")
        else:
            self.redis_client = None
        
        # Session state (minimal)
        self.sessions: Dict[str, Dict[str, Any]] = {}
        
        logger.info(f"THIN Orchestrator initialized: {project_root}")
    
    def _publish_soar_event(self, channel: str, session_id: str, event_data: Dict[str, Any]) -> None:
        """
        THIN: Publish SOAR v2.0 chronolog event to Redis
        
        Software provides simple pub-sub routing; chronolog_capture handles persistence
        """
        if not self.redis_client:
            return  # Silently skip if Redis unavailable
        
        try:
            event_message = {
                "timestamp": datetime.utcnow().isoformat() + "Z",  # Zulu time
                "session_id": session_id,
                "event_id": str(uuid.uuid4()),
                **event_data
            }
            
            self.redis_client.publish(channel, json.dumps(event_message))
            logger.debug(f"Published SOAR event: {channel}")
            
        except Exception as e:
            logger.warning(f"Failed to publish SOAR event {channel}: {e}")
    
    def _create_session_folder(self, session_id: str, config: ResearchConfig) -> Path:
        """Create session folder in research_sessions/ with proper structure"""
        # Use custom session path if provided, otherwise use default
        if self.custom_session_path:
            session_path = self.custom_session_path
        else:
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
        
        # SOAR v2.0: Publish session start event
        self._publish_soar_event("soar.session.start", session_id, {
            "message_type": "session_started",
            "research_question": config.research_question,
            "framework_provided": bool(config.framework_content),
            "dev_mode": config.dev_mode,
            "researcher_profile": config.simulated_researcher_profile if config.dev_mode else "human"
        })
        
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
        
        # Start conversation logging directly in session folder
        session_path = session['session_path']
        session_conversation_logger = ConversationLogger(str(self.project_root), str(session_path))
        conversation_id = session_conversation_logger.start_conversation(
            speech_text=config.source_texts,
            research_question=config.research_question,
            participants=["moderator_llm"]  # Moderator will determine actual participants
        )
        
        # Use session-specific logger for this conversation
        session['conversation_logger'] = session_conversation_logger
        
        session['conversation_id'] = conversation_id
        
        # Execute analysis via moderator LLM (no parsing, just text passing)
        results = await self._execute_via_moderator(
            conversation_id, approved_design, config, session, session_id
        )
        
        # Create readable markdown in session folder
        await self._create_session_readable_markdown(session_id, conversation_id)
        
        session['phase'] = SessionPhase.COMPLETED
        
        # SOAR v2.0: Publish session end event
        self._publish_soar_event("soar.session.end", session_id, {
            "message_type": "session_completed",
            "conversation_id": conversation_id,
            "results_summary": results.get('summary', 'Analysis completed'),
            "session_path": str(session['session_path']),
            "framework_used": bool(config.framework_content)
        })
        
        logger.info("Analysis execution completed")
        return results
    
    async def _create_session_readable_markdown(self, session_id: str, conversation_id: str):
        """Create readable markdown file in the session folder with session ID and metadata"""
        session = self.sessions[session_id]
        session_path = session['session_path']
        config = session['config']
        
        # Generate markdown content from session folder
        markdown_content = format_conversation_to_markdown(conversation_id, str(session_path))
        
        # Add metadata header to markdown
        metadata_header = f"""---
session_id: {session_id}
conversation_id: {conversation_id}
research_question: "{config.research_question}"
created_at: {datetime.now().isoformat()}
dev_mode: {config.dev_mode}
researcher_profile: {config.simulated_researcher_profile if config.dev_mode else 'human'}
status: completed
---

"""
        
        # Combine header with content
        full_markdown = metadata_header + markdown_content
        
        # Save with session ID in filename
        readable_file = session_path / f"{session_id}_conversation_readable.md"
        with open(readable_file, 'w', encoding='utf-8') as f:
            f.write(full_markdown)
        
        logger.info(f"Created readable markdown: {readable_file}")
    
    async def _execute_via_moderator(self, 
                                   conversation_id: str,
                                   approved_design: str,
                                   config: ResearchConfig,
                                   session: Dict[str, Any],
                                   session_id: str) -> Dict[str, Any]:
        """
        Execute analysis by passing approved design to moderator LLM
        
        THIN Principle: Moderator LLM interprets design and orchestrates analysis
        """
        # Build moderator prompt with approved design and framework context
        moderator_prompt = f"""
You are the moderator_llm responsible for executing this approved research design.

RESEARCH QUESTION: {config.research_question}

SOURCE TEXTS:
{config.source_texts}

APPROVED DESIGN:
{approved_design}"""

        # Add framework specification if available
        if config.framework_content:
            moderator_prompt += f"""

FRAMEWORK SPECIFICATION:
{config.framework_content}

IMPORTANT: You must use this framework specification to guide your analysis. This is not a general conversation - you are conducting systematic framework-guided analysis."""

        moderator_prompt += """

Your Task:
1. Read and interpret the approved design
2. Apply the framework specification systematically to analyze the source texts
3. Determine what expert LLMs are needed for framework-guided analysis
4. Orchestrate the multi-LLM conversation to answer the research question using the framework
5. Each time you want an expert to contribute, clearly request their input
6. Continue until you have sufficient framework-based analysis to answer the research question
7. Synthesize findings into a final analysis with framework dimensions and scores

IMPORTANT: When you need expert input, format your request as:
REQUEST TO [expert_name]: [your request]

When you're ready to provide final conclusions, format as:
FINAL ANALYSIS: [your conclusions]

Begin by interpreting the design and framework, then request input from the first expert you need for systematic framework application.
If you need code execution for analysis, write Python code in ```python blocks.
"""
        
        # SOAR v2.0: Publish moderator agent spawn event
        moderator_agent_id = f"moderator_llm_{str(uuid.uuid4())[:8]}"
        self._publish_soar_event("soar.agent.spawned", session_id, {
            "message_type": "agent_spawned",
            "agent_id": moderator_agent_id,
            "agent_type": "moderator_llm",
            "agent_role": "Research orchestration and multi-expert coordination",
            "instructions_preview": moderator_prompt[:500] + "..." if len(moderator_prompt) > 500 else moderator_prompt
        })
        
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
            if config.enable_code_execution and moderator_response and '```python' in moderator_response:
                enhanced_response = process_llm_code_request(
                    conversation_id, "moderator_llm", moderator_response
                )
                
                if enhanced_response != moderator_response:
                    moderator_response = enhanced_response
            
            # Log moderator's response (enhanced if code was executed)
            session['conversation_logger'].log_llm_message(
                conversation_id, "moderator_llm", moderator_response,
                metadata={'role': 'moderator', 'turn': turn, 'code_executed': moderator_response and '```python' in moderator_response}
            )
            
            # SOAR v2.0: Publish moderator response event
            self._publish_soar_event("soar.agent.completed", session_id, {
                "message_type": "agent_response",
                "agent_id": moderator_agent_id,
                "agent_type": "moderator_llm", 
                "turn": turn,
                "response_preview": (moderator_response[:500] + "..." if len(moderator_response) > 500 else moderator_response) if moderator_response else "[NO_RESPONSE]",
                "code_executed": moderator_response and '```python' in moderator_response,
                "requesting_expert": "REQUEST TO " in moderator_response if moderator_response else False
            })
            
            # Check if moderator is requesting expert input
            if moderator_response and "REQUEST TO " in moderator_response:
                # Extract expert request
                expert_response = await self._handle_expert_request(
                    conversation_id, moderator_response, config, turn, session, session_id
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
            
            elif moderator_response and "FINAL ANALYSIS:" in moderator_response:
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
        session['conversation_logger'].end_conversation(
            conversation_id, "Multi-LLM analysis orchestrated by moderator LLM"
        )
        
        # SOAR v2.0: Publish analysis completion event
        self._publish_soar_event("soar.synthesis.ready", session_id, {
            "message_type": "analysis_completed",
            "conversation_id": conversation_id,
            "total_turns": turn - 1,
            "moderator_agent_id": moderator_agent_id,
            "final_analysis_reached": "FINAL ANALYSIS:" in moderator_response if moderator_response else False,
            "summary": "Multi-LLM analysis completed via moderator orchestration"
        })
        
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
                                   turn: int,
                                   session: Dict[str, Any],
                                   session_id: str) -> str:
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
        
        # SOAR v2.0: Publish expert agent spawn event
        expert_agent_id = f"{expert_name}_{str(uuid.uuid4())[:8]}"
        self._publish_soar_event("soar.agent.spawned", session_id, {
            "message_type": "agent_spawned",
            "agent_id": expert_agent_id,
            "agent_type": expert_name,
            "agent_role": f"Expert analysis for: {expert_request[:100]}...",
            "requested_by": "moderator_llm",
            "expert_request": expert_request[:300] + "..." if len(expert_request) > 300 else expert_request
        })
        
        # KNOWLEDGENAUT INTEGRATION: Execute actual research infrastructure
        if expert_name == "knowledgenaut_agent":
            return await self._execute_knowledgenaut_research(
                conversation_id, expert_request, config, turn, session
            )
        
        # CORPUS DETECTIVE INTEGRATION: Execute actual file inspection infrastructure
        if expert_name == "corpus_detective_agent":
            return await self._execute_corpus_detective_inspection(
                conversation_id, expert_request, config, turn, session
            )
        
        # Build specialized prompt using THIN expert system
        expert_prompt = get_expert_prompt(
            expert_name=expert_name,
            research_question=config.research_question,
            source_texts=config.source_texts,
            expert_request=expert_request
        )
        
        # THIN Framework Enhancement: Add framework context if available
        if config.framework_content:
            expert_prompt = f"""You are a {expert_name} agent. That means you analyze texts for patterns and insights using systematic frameworks.

The researcher has provided this framework specification:
{config.framework_content}

Apply this framework systematically to analyze the source texts, then provide framework-guided analysis with specific evidence and scores.

Original Task: {expert_prompt}

Begin your framework-guided analysis:"""
        
        # Get expert response
        if self.llm_client:
            expert_response = self.llm_client.call_llm(expert_prompt, expert_name)
        else:
            expert_response = f"[MOCK] {expert_name} would provide specialized analysis addressing: {expert_request}"
        
        # Handle code execution BEFORE logging (to avoid duplicates)
        if config.enable_code_execution and expert_response and '```python' in expert_response:
            enhanced_response = process_llm_code_request(
                conversation_id, expert_name, expert_response
            )
            if enhanced_response:
                expert_response = enhanced_response
                
        # Log the expert response
        session['conversation_logger'].log_llm_message(
            conversation_id, expert_name, expert_response,
            metadata={'role': 'expert', 'turn': turn, 'requested_by': 'moderator_llm', 'code_executed': expert_response and '```python' in expert_response}
        )
        
        # SOAR v2.0: Publish expert completion event
        self._publish_soar_event("soar.agent.completed", session_id, {
            "message_type": "agent_response",
            "agent_id": expert_agent_id,
            "agent_type": expert_name,
            "turn": turn,
            "response_preview": expert_response[:500] + "..." if len(expert_response) > 500 else expert_response,
            "code_executed": expert_response and '```python' in expert_response,
            "requested_by": "moderator_llm"
        })
        
        return expert_response
    
    async def _execute_knowledgenaut_research(self,
                                            conversation_id: str,
                                            expert_request: str,
                                            config: ResearchConfig,
                                            turn: int,
                                            session: Dict[str, Any]) -> str:
        """
        Execute actual knowledgenaut research infrastructure
        
        THIN Principle: Research infrastructure executes, LLM provides intelligence
        """
        logger.info("🧭 Executing knowledgenaut research infrastructure")
        
        # Check if knowledgenaut is available
        if not KNOWLEDGENAUT_AVAILABLE:
            error_msg = "❌ Knowledgenaut research infrastructure not available. Please check knowledgenaut.py import."
            logger.error(error_msg)
            return error_msg
        
        try:
            # Initialize knowledgenaut research engine
            knowledgenaut = UltraThinKnowledgenaut()
            
            # Extract research question from expert request
            research_question = self._extract_research_question(expert_request, config.research_question)
            
            logger.info(f"🔍 Knowledgenaut research question: {research_question}")
            
            # Execute research (this will return the complete research results)
            research_results = knowledgenaut.research_question(research_question, save_results=False)
            
            # Format results for conversation
            formatted_response = self._format_knowledgenaut_response(research_results, expert_request)
            
            # Log the knowledgenaut response
            session['conversation_logger'].log_llm_message(
                conversation_id, "knowledgenaut_agent", formatted_response,
                metadata={
                    'role': 'expert', 
                    'turn': turn, 
                    'requested_by': 'moderator_llm',
                    'research_infrastructure': True,
                    'papers_found': research_results.get('papers_found', 0),
                    'research_question': research_question,
                    'cost_optimization': research_results.get('cost_optimization', 'N/A')
                }
            )
            
            logger.info(f"✅ Knowledgenaut research completed - {research_results.get('papers_found', 0)} papers found")
            return formatted_response
            
        except Exception as e:
            error_msg = f"❌ Knowledgenaut research failed: {str(e)}"
            logger.error(error_msg)
            
            # Log the error
            session['conversation_logger'].log_llm_message(
                conversation_id, "knowledgenaut_agent", error_msg,
                metadata={
                    'role': 'expert', 
                    'turn': turn, 
                    'requested_by': 'moderator_llm',
                    'research_infrastructure': True,
                    'error': True
                }
            )
            
            return error_msg
    
    async def _execute_corpus_detective_inspection(self,
                                                  conversation_id: str,
                                                  expert_request: str,
                                                  config: ResearchConfig,
                                                  turn: int,
                                                  session: Dict[str, Any]) -> str:
        """
        Execute actual corpus inspection infrastructure
        
        THIN Principle: Use CorpusInspector to read files, corpus detective agent to analyze content
        """
        logger.info("🔍 Executing corpus detective inspection infrastructure")
        
        # Check if corpus inspector is available
        if not CORPUS_INSPECTOR_AVAILABLE:
            error_msg = "❌ Corpus inspector infrastructure not available. Please check corpus_inspector.py import."
            logger.error(error_msg)
            return error_msg
        
        try:
            # Initialize corpus inspector
            inspector = CorpusInspector()
            
            # Check if source_texts looks like a directory path
            source_texts = config.source_texts.strip()
            
            if (source_texts.startswith('/') or 
                source_texts.startswith('./') or 
                source_texts.startswith('../') or
                ('/' in source_texts and not source_texts.startswith('FILE:'))):
                
                logger.info(f"🗂️ Detected directory path: {source_texts}")
                
                # Read files from directory
                files, errors = inspector.inspect_directory_corpus(source_texts)
                
                if not files:
                    error_summary = "\n".join(errors) if errors else "No files found in directory"
                    error_msg = f"❌ Could not read corpus from {source_texts}\n\nErrors:\n{error_summary}"
                    logger.error(error_msg)
                    return error_msg
                
                # Use corpus inspector to analyze with detective agent
                analysis = await inspector.analyze_corpus_with_detective(files, config.research_question)
                
                # Add file reading results to analysis
                if errors:
                    analysis += f"\n\n⚠️ **File Reading Issues:**\n" + "\n".join(f"- {error}" for error in errors)
                
                # Add corpus statistics
                stats = inspector.get_corpus_stats(files)
                analysis += f"\n\n📊 **Corpus Statistics:**\n"
                analysis += f"- Files read: {stats['file_count']}\n"
                analysis += f"- Total characters: {stats['total_chars']:,}\n"
                analysis += f"- Estimated tokens: {stats['total_tokens']:,}\n"
                analysis += f"- File types: {', '.join(stats['file_types'])}\n"
                analysis += f"- Average file size: {stats['avg_file_size']:,} characters\n"
                
                logger.info(f"✅ Corpus inspection completed - {stats['file_count']} files analyzed")
                
            else:
                # Source texts are already provided as text content
                logger.info("📄 Source texts provided as content, analyzing directly")
                
                # Create a single-file dict for consistency
                files = {"provided_texts": source_texts}
                
                # Use corpus inspector to analyze with detective agent
                analysis = await inspector.analyze_corpus_with_detective(files, config.research_question)
            
            # Log the corpus detective response
            session['conversation_logger'].log_llm_message(
                conversation_id, "corpus_detective_agent", analysis,
                metadata={
                    'role': 'expert', 
                    'turn': turn, 
                    'requested_by': 'moderator_llm',
                    'corpus_inspection': True,
                    'files_analyzed': len(files) if 'files' in locals() else 1,
                    'inspection_type': 'directory' if '/' in source_texts else 'content'
                }
            )
            
            return analysis
            
        except Exception as e:
            error_msg = f"❌ Corpus detective inspection failed: {str(e)}"
            logger.error(error_msg)
            
            # Log the error
            session['conversation_logger'].log_llm_message(
                conversation_id, "corpus_detective_agent", error_msg,
                metadata={
                    'role': 'expert', 
                    'turn': turn, 
                    'requested_by': 'moderator_llm',
                    'corpus_inspection': True,
                    'error': True
                }
            )
            
            return error_msg
    
    def _extract_research_question(self, expert_request: str, fallback_question: str) -> str:
        """Extract research question from expert request"""
        # Look for explicit research questions in the request
        request_lower = expert_request.lower()
        
        # Common research question patterns
        if "research question:" in request_lower:
            # Extract text after "research question:"
            parts = expert_request.split("research question:", 1)
            if len(parts) > 1:
                return parts[1].strip()
        
        # If expert request seems to be a direct question, use it
        if any(q in request_lower for q in ["what", "how", "why", "when", "where", "which"]):
            return expert_request.strip()
        
        # Otherwise use the main research question
        return fallback_question
    
    def _format_knowledgenaut_response(self, research_results: Dict[str, Any], expert_request: str) -> str:
        """Format knowledgenaut research results for conversation"""
        
        # Extract key information
        papers_found = research_results.get('papers_found', 0)
        final_response = research_results.get('final_response', '')
        synthesis = research_results.get('synthesis', '')
        critique = research_results.get('critique', '')
        papers = research_results.get('papers', [])
        
        # Build formatted response
        response = f"""# 🧭 Knowledgenaut Research Analysis

**Research Request**: {expert_request}

**Research Question**: {research_results.get('question', 'N/A')}

**Papers Found**: {papers_found}

**Cost Optimization**: {research_results.get('cost_optimization', 'N/A')}

---

## 🔬 Research Synthesis

{synthesis}

---

## 🥊 Red Team Critique

{critique}

---

## 🎯 Final Research Analysis

{final_response}

---

## 📚 Key Literature Found

"""
        
        # Add top papers (limit to 5 for readability)
        for i, paper in enumerate(papers[:5], 1):
            response += f"""
### {i}. {paper.get('title', 'No title')}

- **Authors**: {', '.join(paper.get('authors', [])[:3])}
- **Year**: {paper.get('year', 'Unknown')}
- **Source**: {paper.get('source', 'Unknown')}
- **Quality Score**: {paper.get('quality_score', 'N/A')}/5
- **DOI**: {paper.get('doi', 'No DOI')}

"""
        
        if papers_found > 5:
            response += f"\n*({papers_found - 5} additional papers found but not shown for brevity)*\n"
        
        response += f"""
---

**Research Infrastructure**: Ultra-THIN Knowledgenaut with multi-API literature discovery
**Analysis Date**: {research_results.get('timestamp', 'N/A')}
"""
        
        return response
    
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

AVAILABLE EXPERT AGENTS:
- knowledgenaut_agent: Research agent for literature discovery, citation validation, framework interrogation, and bias detection
- Any other specialized expert LLMs you deem necessary

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
            'conversation_id': session.get('conversation_id'),
            'session_path': session.get('session_path')
        }
    
    def cleanup_session(self, session_id: str) -> None:
        """Clean up session"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            logger.info(f"Cleaned up session: {session_id}")

    # Development Mode: Simulated Human Researcher
    def _simulate_human_researcher_response(self, context: str, config: ResearchConfig) -> str:
        """Simulate a human researcher's response for development mode"""
        if not config.dev_mode:
            raise ValueError("Simulated responses only available in dev_mode")
        
        # Use externalized THIN prompt system
        researcher_prompt = get_simulated_researcher_prompt(
            prompt_type='feedback',
            researcher_profile=config.simulated_researcher_profile,
            research_question=config.research_question,
            context=context
        )
        
        if self.llm_client:
            response = self.llm_client.call_llm(researcher_prompt, "simulated_researcher")
        else:
            response = "The design looks reasonable. I'd like to see more emphasis on quantitative validation of qualitative findings, but overall the multi-expert approach should work well for this research question."
        
        return response

    def _simulate_approval_decision(self, design_response: str, feedback: str, config: ResearchConfig) -> bool:
        """Simulate human approval decision for development mode"""
        if not config.dev_mode:
            raise ValueError("Simulated approval only available in dev_mode")
        
        # Use externalized THIN prompt system
        decision_prompt = get_simulated_researcher_prompt(
            prompt_type='decision',
            researcher_profile=config.simulated_researcher_profile,
            research_question=config.research_question,
            design_response=design_response,
            feedback=feedback
        )
        
        if self.llm_client:
            decision_response = self.llm_client.call_llm(decision_prompt, "simulated_researcher_decision")
        else:
            decision_response = "APPROVE"
        
        # Parse the decision
        decision_response = decision_response.strip().upper()
        if decision_response.startswith("APPROVE"):
            return True
        else:
            return False

    async def run_automated_session(self, config: ResearchConfig) -> Dict[str, Any]:
        """Run a complete automated session for development/testing
        
        This simulates the full research workflow:
        1. Design consultation
        2. Simulated human feedback  
        3. Design iteration (if needed)
        4. Simulated approval
        5. Execution
        
        Returns complete session results.
        """
        if not config.dev_mode:
            raise ValueError("Automated sessions require dev_mode=True")
        
        logger.info("🤖 Starting automated development session")
        
        # Start session
        session_id = await self.start_research_session(config)
        
        # Design consultation loop with simulated feedback
        max_design_iterations = 3
        for iteration in range(max_design_iterations):
            logger.info(f"🎨 Design iteration {iteration + 1}")
            
            # Get design proposal
            if iteration == 0:
                design_response = await self.run_design_consultation(session_id, "")
            else:
                # Use previous simulated feedback
                design_response = await self.run_design_consultation(session_id, feedback)
            
            # Simulate human researcher feedback
            feedback = self._simulate_human_researcher_response(design_response, config)
            logger.info(f"🧑‍🔬 Simulated researcher feedback: {feedback[:100]}...")
            
            # Simulate approval decision
            approved = self._simulate_approval_decision(design_response, feedback, config)
            
            if approved:
                logger.info("✅ Design approved by simulated researcher")
                self.approve_design(session_id, True, feedback)
                break
            else:
                logger.info("🔄 Design needs revision, iterating...")
                self.approve_design(session_id, False, feedback)
                if iteration == max_design_iterations - 1:
                    logger.warning("⚠️  Max design iterations reached, proceeding anyway")
                    self.approve_design(session_id, True, "Proceeding after max iterations")
        
        # Execute the approved analysis
        logger.info("🚀 Executing approved analysis")
        results = await self.execute_approved_analysis(session_id)
        
        # Add session metadata to results
        results.update({
            'session_id': session_id,
            'dev_mode': True,
            'researcher_profile': config.simulated_researcher_profile,
            'design_iterations': iteration + 1,
            'session_path': str(self.sessions[session_id]['session_path'])
        })
        
        logger.info(f"✅ Automated session completed: {session_id}")
        return results

    @classmethod
    async def quick_analysis(cls, research_question: str, corpus_path: str, 
                           researcher_profile: str = "experienced_computational_social_scientist") -> Dict[str, Any]:
        """Convenience method for quick automated analysis
        
        Example:
            results = await ThinOrchestrator.quick_analysis(
                research_question="How does rhetoric differ between Lincoln and Trump?",
                corpus_path="data/inaugural_addresses/",
                researcher_profile="political_discourse_expert"
            )
        """
        from pathlib import Path
        
        # Read corpus files
        corpus_path = Path(corpus_path)
        if corpus_path.is_file():
            source_texts = corpus_path.read_text()
        elif corpus_path.is_dir():
            # Combine all text files in directory
            texts = []
            for file_path in corpus_path.glob("*.txt"):
                texts.append(f"=== {file_path.name} ===\n{file_path.read_text()}\n")
            source_texts = "\n".join(texts)
        else:
            raise ValueError(f"Corpus path not found: {corpus_path}")
        
        # Create config
        config = ResearchConfig(
            research_question=research_question,
            source_texts=source_texts,
            enable_code_execution=True,
            dev_mode=True,
            simulated_researcher_profile=researcher_profile
        )
        
        # Run automated session
        orchestrator = cls()
        return await orchestrator.run_automated_session(config)


# Keep old names for compatibility
ThinDiscernusOrchestrator = ThinOrchestrator
ConversationConfig = ResearchConfig 