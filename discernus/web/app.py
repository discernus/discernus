#!/usr/bin/env python3
"""
Discernus Research Artifact UX - THIN Academic Web Interface
===========================================================

THIN Principle: Pure interface layer, zero intelligence in software
All research intelligence handled by LLMs, web app just displays artifacts
"""

import sys
from pathlib import Path
from flask import Flask, render_template, jsonify, request, send_from_directory
import json
import asyncio
from datetime import datetime
import logging
import threading
import time

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from discernus.core.session_summarizer import summarize_all_sessions
from discernus.core.corpus_library import discover_corpora
from discernus.orchestration.workflow_orchestrator import WorkflowOrchestrator
from discernus.core.spec_loader import SpecLoader

app = Flask(__name__)

# Configure Flask for academic interface
app.config['SECRET_KEY'] = 'discernus-academic-research'

# Initialize orchestrator for research sessions (will be reinitialized per session)
orchestrator = None

# In-memory session state (simple approach)
chat_sessions = {}

@app.route('/')
def index():
    """Main research dashboard showing sessions and corpora"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def api_chat():
    """
    Handle chat messages and coordinate research sessions
    
    THIN Principle: Route messages to orchestrator, handle responses
    """
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        session_id = data.get('session_id')
        
        if not message:
            return jsonify({
                'status': 'error',
                'message': 'Message cannot be empty'
            }), 400
        
        # Save user message if we have a session
        if session_id and session_id in chat_sessions:
            _save_chat_message(session_id, "user", message)
        
        # Process message based on current session state
        if session_id and session_id in chat_sessions:
            # Continue existing session
            response = _handle_existing_session(session_id, message)
        else:
            # Start new session or handle initial message
            response = _handle_new_session(message)
        
        # Save assistant response if we have a session
        if response.get('session_id') and response['session_id'] in chat_sessions:
            _save_chat_message(response['session_id'], "assistant", response['response'])
        elif session_id and session_id in chat_sessions:
            _save_chat_message(session_id, "assistant", response['response'])
        
        return jsonify(response)
        
    except Exception as e:
        # Use Overwatch LLM pattern for error handling
        error_summary = _get_error_summary(str(e))
        return jsonify({
            'status': 'error',
            'message': error_summary
        }), 500

def _handle_new_session(message):
    """Handle new session creation and initial message"""
    # Simple corpus path detection
    corpus_path = _extract_corpus_path(message)
    
    if not corpus_path:
        return {
            'status': 'success',
            'response': """I need a corpus path to start your research session. Please provide:

1. **Corpus Path**: Local path to your text files (e.g., data/inaugural_addresses)
2. **Research Question**: What would you like to investigate?

You can format it like:
```
Corpus Path: data/inaugural_addresses
Research Question: How do Lincoln and Trump's inaugural addresses compare in terms of unity vs division themes?
```

Or just tell me in your own words what you want to research and where your files are located."""
        }
    
    # Verify corpus exists
    if not Path(corpus_path).exists():
        return {
            'status': 'error',
            'message': f'Corpus path not found: {corpus_path}. Please check the path and try again.'
        }
    
    # Extract research question
    research_question = _extract_research_question(message)
    if not research_question:
        research_question = f"Analysis of texts in {corpus_path}"
    
    # Start orchestrator session and get design consultation immediately
    try:
        session_id = f"web_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Create research config
        config = ResearchConfig(
            research_question=research_question,
            source_texts=str(corpus_path),
            enable_code_execution=True
        )
        
        # Initialize session state
        chat_sessions[session_id] = {
            'phase': 'starting',
            'config': config,
            'corpus_path': corpus_path,
            'research_question': research_question,
            'orchestrator_session': None
        }
        
        # Create session folder
        _create_chat_session_folder(session_id, chat_sessions[session_id])
        
        # Save user message
        _save_chat_message(session_id, "user", message)
        
        # Start orchestrator session immediately
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            orchestrator_session_id = loop.run_until_complete(
                orchestrator.start_research_session(config)
            )
            
            # Update session state
            chat_sessions[session_id]['orchestrator_session'] = orchestrator_session_id
            chat_sessions[session_id]['phase'] = 'design_consultation'
            
            # Get design consultation immediately
            design_response = loop.run_until_complete(
                orchestrator.run_design_consultation(orchestrator_session_id)
            )
            
            # Update phase to awaiting approval
            chat_sessions[session_id]['phase'] = 'awaiting_approval'
            
            # Save conversation steps
            _save_chat_message(session_id, "system", "Research session started")
            _save_chat_message(session_id, "design_llm", design_response)
            
            return {
                'status': 'success',
                'response': f"""✅ **Research Session Started!**

**Corpus Path**: {corpus_path}
**Research Question**: {research_question}

🎯 **Design Consultation Complete**

The design LLM has analyzed your research question and corpus. Here's the proposed methodology:

---

{design_response}

---

**Next Steps:**
- Review the proposed methodology above
- Type 'approve' if you agree with this approach
- Type 'reject' or provide specific feedback if you want changes
- You can also ask questions or request clarifications

**Session ID**: {session_id}""",
                'session_id': session_id
            }
        finally:
            loop.close()
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Failed to start research session: {str(e)}'
        }

def _handle_existing_session(session_id, message):
    """Handle messages for existing sessions"""
    session = chat_sessions.get(session_id)
    if not session:
        return {
            'status': 'error',
            'message': 'Session not found. Please start a new session.'
        }
    
    phase = session.get('phase', 'unknown')
    
    if phase == 'design_consultation':
        return _handle_design_consultation(session_id, session, message)
    elif phase == 'awaiting_approval':
        return _handle_design_approval(session_id, session, message)
    elif phase == 'executing':
        return _handle_execution_phase(session_id, session, message)
    elif phase == 'completed':
        return _handle_completed_session(session_id, session, message)
    else:
        return {
            'status': 'success',
            'response': f"""**Session Status**: {phase}

I'm not sure what to do in this phase. Please try:
- Typing 'status' to see current session information
- Typing 'restart' to begin a new session
- Typing 'help' for available commands

**Current Session**: {session_id}"""
        }

def _create_chat_session_folder(session_id, session):
    """Create session folder and metadata for chat sessions"""
    try:
        session_path = project_root / "research_sessions" / session_id
        session_path.mkdir(parents=True, exist_ok=True)
        
        # Create metadata file
        metadata = {
            'session_id': session_id,
            'session_type': 'web_chat',
            'research_question': session['research_question'],
            'corpus_path': session['corpus_path'],
            'started_at': datetime.now().isoformat(),
            'status': 'active',
            'phase': session.get('phase', 'starting'),
            'web_session': True
        }
        
        metadata_file = session_path / "metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        # Create conversation log file
        conversation_file = session_path / "conversation_log.jsonl"
        with open(conversation_file, 'w') as f:
            # Start with session initiation
            initial_log = {
                'timestamp': datetime.now().isoformat(),
                'participant': 'system',
                'message': f'Web chat session started for: {session["research_question"]}',
                'metadata': {
                    'session_id': session_id,
                    'corpus_path': session['corpus_path'],
                    'session_type': 'web_chat'
                }
            }
            f.write(json.dumps(initial_log) + '\n')
        
        # Update session with paths
        chat_sessions[session_id]['session_path'] = str(session_path)
        chat_sessions[session_id]['conversation_file'] = str(conversation_file)
        
    except Exception as e:
        print(f"Failed to create session folder: {str(e)}")

def _save_chat_message(session_id, participant, message, metadata=None):
    """Save chat message to session conversation log with deduplication"""
    try:
        session = chat_sessions.get(session_id)
        if not session:
            return
        
        conversation_file = session.get('conversation_file')
        if not conversation_file:
            return
        
        # Check for recent duplicates (last 5 messages to avoid performance issues)
        if _is_duplicate_message(conversation_file, participant, message):
            return  # Skip duplicate
        
        # Create log entry
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'participant': participant,
            'message': message,
            'metadata': metadata or {}
        }
        
        # Append to conversation log
        with open(conversation_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
            
    except Exception as e:
        print(f"Failed to save chat message: {str(e)}")

def _is_duplicate_message(conversation_file, participant, message):
    """Check if this message is a duplicate of recent messages"""
    try:
        if not Path(conversation_file).exists():
            return False
        
        # Read last 5 lines to check for duplicates
        with open(conversation_file, 'r') as f:
            lines = f.readlines()
        
        # Check last 5 messages
        recent_lines = lines[-5:] if len(lines) >= 5 else lines
        
        for line in recent_lines:
            try:
                entry = json.loads(line.strip())
                if (entry.get('participant') == participant and 
                    entry.get('message') == message):
                    return True  # Duplicate found
            except json.JSONDecodeError:
                continue
        
        return False
        
    except Exception as e:
        print(f"Error checking for duplicates: {e}")
        return False  # If error, allow message to be saved

def _update_session_status(session_id, status, phase=None):
    """Update session status and metadata"""
    try:
        session = chat_sessions.get(session_id)
        if not session:
            return
        
        session_path = session.get('session_path')
        if not session_path:
            return
        
        metadata_file = Path(session_path) / "metadata.json"
        
        # Read existing metadata
        metadata = {}
        if metadata_file.exists():
            with open(metadata_file, 'r') as f:
                metadata = json.load(f)
        
        # Update status
        metadata['status'] = status
        metadata['last_updated'] = datetime.now().isoformat()
        
        if phase:
            metadata['phase'] = phase
            chat_sessions[session_id]['phase'] = phase
        
        # Save updated metadata
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
            
    except Exception as e:
        print(f"Failed to update session status: {str(e)}")

def _finalize_session(session_id, results=None):
    """Finalize session and create readable markdown"""
    try:
        session = chat_sessions.get(session_id)
        if not session:
            return
        
        session_path = Path(session.get('session_path', ''))
        conversation_file = session.get('conversation_file', '')
        
        if not session_path.exists():
            return
        
        # Update final status
        _update_session_status(session_id, 'completed', 'completed')
        
        # Create readable markdown from conversation log
        if Path(conversation_file).exists():
            _create_readable_markdown(session_id, conversation_file, session_path)
        
        # Save results if provided
        if results:
            results_file = session_path / "analysis_results.json"
            with open(results_file, 'w') as f:
                json.dump(results, f, indent=2)
        
        # Create session manifest for dashboard integration
        _create_session_manifest(session_id, session, session_path)
        
    except Exception as e:
        print(f"Failed to finalize session: {str(e)}")

def _create_readable_markdown(session_id, conversation_file, session_path):
    """Create readable markdown from conversation log"""
    try:
        markdown_content = f"""# Research Session: {session_id}

## Session Overview
- **Session ID**: {session_id}
- **Started**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Type**: Web Chat Session

## Conversation Log

"""
        
        # Read conversation log
        with open(conversation_file, 'r') as f:
            for line in f:
                try:
                    log_entry = json.loads(line.strip())
                    participant = log_entry.get('participant', 'unknown')
                    message = log_entry.get('message', '')
                    timestamp = log_entry.get('timestamp', '')
                    
                    # Format timestamp
                    formatted_time = timestamp.split('T')[1].split('.')[0] if 'T' in timestamp else timestamp
                    
                    markdown_content += f"""### {participant.title()} ({formatted_time})

{message}

---

"""
                except json.JSONDecodeError:
                    continue
        
        # Save markdown file
        markdown_file = session_path / "conversation_readable.md"
        with open(markdown_file, 'w') as f:
            f.write(markdown_content)
            
    except Exception as e:
        print(f"Failed to create readable markdown: {str(e)}")

def _create_session_manifest(session_id, session, session_path):
    """Create session manifest for dashboard integration"""
    try:
        manifest = {
            'session_id': session_id,
            'friendly_name': f"Web Chat: {session['research_question'][:50]}...",
            'summary': f"Interactive web chat session analyzing {session['corpus_path']}",
            'research_question': session['research_question'],
            'timestamp': datetime.now().isoformat(),
            'corpus_description': f"Corpus: {session['corpus_path']}",
            'key_findings': ['Web chat session completed'],
            'session_path': str(session_path),
            'session_type': 'web_chat',
            'phase': session.get('phase', 'completed'),
            'status': 'completed'
        }
        
        manifest_file = session_path / "session_manifest.json"
        with open(manifest_file, 'w') as f:
            json.dump(manifest, f, indent=2)
            
    except Exception as e:
        print(f"Failed to create session manifest: {str(e)}")

def _handle_design_consultation(session_id, session, message):
    """Handle ongoing design consultation"""
    try:
        orchestrator_session_id = session['orchestrator_session']
        
        # Get updated design consultation with user feedback
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            design_response = loop.run_until_complete(
                orchestrator.run_design_consultation(orchestrator_session_id, message)
            )
        finally:
            loop.close()
        
        # Update phase
        chat_sessions[session_id]['phase'] = 'awaiting_approval'
        
        return {
            'status': 'success',
            'response': f"""🎯 **Updated Design Consultation**

Based on your feedback, here's the revised methodology:

---

{design_response}

---

**Your Options:**
- Type 'approve' to proceed with this methodology
- Type 'reject' with specific feedback for further revisions
- Ask questions about any aspect of the proposed approach

**Session ID**: {session_id}"""
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Design consultation failed: {str(e)}'
        }

def _handle_design_approval(session_id, session, message):
    """Handle design approval/rejection"""
    try:
        orchestrator_session_id = session['orchestrator_session']
        message_lower = message.lower().strip()
        
        if any(word in message_lower for word in ['approve', 'yes', 'ok', 'proceed', 'good']):
            # Save approval message
            _save_chat_message(session_id, "user", f"Design approved: {message}")
            
            # Approve the design
            approved = orchestrator.approve_design(orchestrator_session_id, True)
            
            if approved:
                # Update phase and start execution with real-time updates
                _update_session_status(session_id, 'executing', 'executing')
                _save_chat_message(session_id, "system", "Design approved. Starting analysis execution...")
                
                # Execute analysis with step-by-step updates
                return _execute_analysis_with_realtime_updates(session_id, session, orchestrator_session_id)
                    
            else:
                _save_chat_message(session_id, "system", "Design approval failed")
                return {
                    'status': 'error',
                    'message': 'Failed to approve design. Please try again.'
                }
        
        elif any(word in message_lower for word in ['reject', 'no', 'change', 'revise']):
            # Save rejection message
            _save_chat_message(session_id, "user", f"Design rejected: {message}")
            
            # Reject the design and provide feedback
            orchestrator.approve_design(orchestrator_session_id, False, message)
            
            # Go back to design consultation
            _update_session_status(session_id, 'design_consultation', 'design_consultation')
            
            return {
                'status': 'success',
                'response': f"""🔄 **Design Revision Requested**

Your feedback has been noted: "{message}"

I'll work with the design LLM to revise the methodology based on your input.

Please wait while I prepare an updated approach..."""
            }
        
        else:
            return {
                'status': 'success',
                'response': f"""❓ **Approval Status Unclear**

I need a clear approval or rejection. Please respond with:
- **"approve"** or **"yes"** to proceed with the current methodology
- **"reject"** or **"no"** with specific feedback for revisions

Your message: "{message}"

**What would you like to do?**"""
            }
        
    except Exception as e:
        _save_chat_message(session_id, "system", f"Error in design approval: {str(e)}")
        return {
            'status': 'error',
            'message': f'Design approval failed: {str(e)}'
        }

def _execute_analysis_with_realtime_updates(session_id, session, orchestrator_session_id):
    """Execute analysis using real orchestrator with live updates"""
    try:
        # Get corpus path and research question from session
        corpus_path = session.get('corpus_path', '')
        research_question = session.get('research_question', '')
        
        # Validate corpus path exists
        if not corpus_path:
            _save_chat_message(session_id, "system", "❌ **Error**: No corpus path specified")
            return {'status': 'error', 'message': 'No corpus path specified'}
        
        # Convert relative path to absolute if needed
        if not corpus_path.startswith('/'):
            corpus_path = str(project_root / corpus_path)
        
        corpus_path_obj = Path(corpus_path)
        if not corpus_path_obj.exists():
            _save_chat_message(session_id, "system", f"❌ **Error**: Corpus path not found: {corpus_path}")
            return {'status': 'error', 'message': f'Corpus path not found: {corpus_path}'}
        
        # Load corpus content
        corpus_content = _load_corpus_content(corpus_path_obj)
        if not corpus_content:
            _save_chat_message(session_id, "system", f"❌ **Error**: No readable files found in corpus: {corpus_path}")
            return {'status': 'error', 'message': f'No readable files found in corpus: {corpus_path}'}
        
        # Create research config
        config = ResearchConfig(
            research_question=research_question,
            source_texts=corpus_content,
            enable_code_execution=True
        )
        
        # Update session status
        _update_session_status(session_id, 'executing', 'executing')
        
        # Save initial message
        _save_chat_message(session_id, "system", f"""🚀 **Multi-LLM Analysis Starting**

**Research Question**: {research_question}
**Corpus**: {corpus_path}
**Files Found**: {len(corpus_content.split('=== END OF FILE ===')) - 1} files

**Analysis Process**:
1. **Design Consultation** - Getting methodology from design LLM
2. **Design Approval** - Auto-approving for web interface
3. **Multi-LLM Execution** - Real expert LLMs analyzing your corpus
4. **Synthesis** - Combining insights into final analysis

**⚡ Live Updates**: You'll see each expert LLM's actual analysis as it happens
""")
        
        # Run orchestrator in background and monitor progress
        def run_orchestrator():
            try:
                # Create orchestrator with custom session path for direct logging
                session_path = Path(chat_sessions[session_id]['session_path'])
                from discernus.orchestration.orchestrator import ThinOrchestrator
                session_orchestrator = ThinOrchestrator(str(project_root), str(session_path))
                
                # Start orchestrator session
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                # Get design consultation
                design_response = loop.run_until_complete(
                    session_orchestrator.run_design_consultation(orchestrator_session_id, "")
                )
                
                # Auto-approve design for web interface
                session_orchestrator.approve_design(orchestrator_session_id, True)
                
                # Execute analysis
                results = loop.run_until_complete(
                    session_orchestrator.execute_approved_analysis(orchestrator_session_id)
                )
                
                # Update session with results
                _update_session_status(session_id, 'completed', 'completed')
                chat_sessions[session_id]['results'] = results
                
                # Create final message
                final_message = f"""✅ **Analysis Complete!**

**Results Summary**:
- **Conversation ID**: {results.get('conversation_id', 'N/A')}
- **Analysis Status**: {results.get('status', 'Unknown')}
- **Total LLM Interactions**: {results.get('turns', 'N/A')}

**📁 Files Generated**:
- Complete multi-LLM conversation
- Academic-formatted analysis
- Session metadata and manifest

**🔍 View Results**: The detailed analysis is now available in the Sessions tab

**💡 Key Insight**: This analysis contains actual expert LLM perspectives on your research question, not just progress summaries!

**Session ID**: {session_id}
**Research Question**: {research_question}
**Corpus**: {corpus_path}
"""
                
                _save_chat_message(session_id, "system", final_message)
                
                # Finalize session
                _finalize_session(session_id, results)
                
                loop.close()
                
            except Exception as e:
                _save_chat_message(session_id, "system", f"❌ **Analysis Error**: {str(e)}")
                _update_session_status(session_id, 'error', 'error')
                logging.error(f"Orchestrator execution failed: {str(e)}")
        
        # Start orchestrator in background thread
        thread = threading.Thread(target=run_orchestrator)
        thread.daemon = True
        thread.start()
        
        return {
            'status': 'success',
            'response': '🚀 **Analysis Started with Real Orchestrator!**\n\nYour Lincoln/Trump inaugural address analysis is now running with actual expert LLMs. You\'ll see real-time updates as each expert contributes their analysis.',
            'orchestrator_session_id': orchestrator_session_id
        }
        
    except Exception as e:
        _save_chat_message(session_id, "system", f"❌ **Execution Error**: {str(e)}")
        return {'status': 'error', 'response': f"❌ **Execution Error**: {str(e)}"}

def _load_corpus_content(corpus_path):
    """Load and concatenate all text files in corpus"""
    content_parts = []
    
    for file_path in corpus_path.glob('**/*.txt'):
        if file_path.is_file():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if content:
                        content_parts.append(f"=== FILE: {file_path.name} ===\n{content}\n=== END OF FILE ===")
            except Exception as e:
                logging.warning(f"Could not read file {file_path}: {e}")
    
    return '\n\n'.join(content_parts)

# Removed redundant monitoring and copying functions - orchestrator now logs directly to session folder

async def _execute_with_step_monitoring(session_id, orchestrator_session_id):
    """Execute with step monitoring - now using real orchestrator"""
    try:
        # This is now handled by the real orchestrator
        # Just wait for completion
        session = chat_sessions.get(session_id)
        while session and session.get('phase') != 'completed':
            await asyncio.sleep(1)
            session = chat_sessions.get(session_id)
        
        results = session.get('results', {}) if session else {}
        return results
        
    except Exception as e:
        logging.error(f"Step monitoring failed: {e}")
        return {'status': 'error', 'message': str(e)}

def _handle_execution_phase(session_id, session, message):
    """Handle messages during execution phase"""
    return {
        'status': 'success',
        'response': f"""⚙️ **Analysis in Progress**

Your research analysis is currently being executed by the multi-LLM system. This process involves:

1. **Corpus Analysis** - Understanding your texts
2. **Expert Consultation** - Specialized LLM perspectives  
3. **Adversarial Review** - Challenging assumptions
4. **Synthesis** - Combining insights

**Current Status**: Executing
**Session ID**: {session_id}

Please wait for the analysis to complete. This may take several minutes depending on your corpus size and research complexity.

*Note: Full real-time execution streaming is coming soon.*"""
    }

def _handle_completed_session(session_id, session, message):
    """Handle messages for completed sessions"""
    results = session.get('results', {})
    
    if 'help' in message.lower():
        return {
            'status': 'success',
            'response': f"""✅ **Completed Session Help**

Your research analysis is complete! Here's what you can do:

**Available Commands:**
- **'summary'** - View analysis summary
- **'results'** - View detailed results
- **'export'** - Get download links
- **'new'** - Start a new research session

**Session Details:**
- Session ID: {session_id}
- Research Question: {session['research_question']}
- Corpus: {session['corpus_path']}
- Status: Completed

**Results Location**: `research_sessions/{session_id}/`"""
        }
    
    elif 'summary' in message.lower():
        return {
            'status': 'success',
            'response': f"""📊 **Analysis Summary**

**Research Question**: {session['research_question']}
**Corpus Analyzed**: {session['corpus_path']}

**Results:**
- Conversation ID: {results.get('conversation_id', 'N/A')}
- Analysis Status: {results.get('status', 'Unknown')}
- Total Turns: {results.get('turns', 'N/A')}

**Files Generated:**
- Complete conversation log
- Readable markdown analysis
- Session metadata

**Location**: `research_sessions/{session_id}/`

Type 'results' for more detailed information."""
        }
    
    else:
        return {
            'status': 'success',
            'response': f"""✅ **Session Completed**

Your research analysis has been successfully completed and saved.

**Quick Actions:**
- Type 'summary' for analysis overview
- Type 'help' for available commands
- Visit the Sessions tab to view the full conversation

**Session ID**: {session_id}"""
        }

def _extract_corpus_path(message):
    """Extract corpus path from user message"""
    import re
    
    # Look for explicit corpus path patterns with better handling of natural language
    patterns = [
        r'corpus path:?\s*([^\n]+)',
        r'corpus is (?:here|located|at):?\s*([^\n]+)',
        r'corpus:?\s*([/][^\s\n]+)',  # Absolute paths starting with /
        r'path:?\s*([^\n]+)',
        r'files in:?\s*([^\n]+)',
        r'directory:?\s*([^\n]+)',
        r'corpus is:?\s*([^\n]+)',
        r'my corpus is (?:here|located|at):?\s*([^\n]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, message.lower())
        if match:
            path = match.group(1).strip()
            # Clean up common path formats
            path = path.replace('"', '').replace("'", '')
            
            # If path doesn't start with / or contain recognizable path separators, skip
            if not ('/' in path or '\\' in path):
                continue
                
            return path
    
    # Look for absolute path patterns anywhere in the message
    path_patterns = [
        r'(/[A-Za-z0-9_/.-]+)',  # Absolute paths starting with /
        r'(data/[^\s]+)',
        r'(projects/[^\s]+)',
        r'([^\s]+/[^\s]+\.txt)',
        r'([^\s]*[/\\][^\s]*)'  # Any path with separators
    ]
    
    for pattern in path_patterns:
        matches = re.findall(pattern, message)
        for match in matches:
            # Filter out very short or obviously wrong matches
            if len(match) > 3 and ('/' in match or '\\' in match):
                return match.strip()
    
    return None

def _extract_research_question(message):
    """Extract research question from user message"""
    import re
    
    # Look for explicit research question patterns
    patterns = [
        r'research question:?\s*([^\n]+)',
        r'question:?\s*([^\n]+)',
        r'investigate:?\s*([^\n]+)',
        r'analyze:?\s*([^\n]+)',
        r'study:?\s*([^\n]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, message.lower())
        if match:
            return match.group(1).strip()
    
    # If no explicit question, try to infer from the message
    # Look for question-like sentences
    sentences = message.split('.')
    for sentence in sentences:
        if any(word in sentence.lower() for word in ['how', 'what', 'why', 'compare', 'analyze', 'difference']):
            return sentence.strip()
    
    return None

def _get_error_summary(error_message):
    """Generate user-friendly error summary using Overwatch LLM pattern"""
    
    # Try to get intelligent error analysis from Overwatch LLM
    try:
        overwatch_response = _call_overwatch_llm(error_message)
        return overwatch_response
    except Exception as overwatch_error:
        # Fallback to simple error categorization
        return _simple_error_categorization(error_message)

def _call_overwatch_llm(error_message):
    """Call Overwatch LLM for intelligent error diagnosis"""
    
    overwatch_prompt = f"""You are an Overwatch LLM specialized in diagnosing research system errors and providing user-friendly explanations.

ERROR CONTEXT:
{error_message}

Your task:
1. Diagnose the root cause of this error
2. Provide a clear, user-friendly explanation
3. Suggest specific steps to resolve the issue
4. Use appropriate emojis and formatting for academic users

Format your response as:
**Error Type**: [Category]
**Issue**: [Clear explanation]
**Solution**: [Specific steps]

Keep the tone professional but approachable for academic researchers."""

    try:
        # Use the existing LLM client through orchestrator
        from discernus.core.thin_litellm_client import ThinLiteLLMClient
        
        llm_client = ThinLiteLLMClient()
        if llm_client.available:
            overwatch_response = llm_client.call_llm(overwatch_prompt, "overwatch_llm")
            return f"🔍 **Overwatch Analysis**\n\n{overwatch_response}"
        else:
            raise Exception("LLM client not available")
            
    except Exception as e:
        # If Overwatch LLM fails, use simple categorization
        raise Exception(f"Overwatch LLM failed: {str(e)}")

def _simple_error_categorization(error_message):
    """Simple error categorization fallback"""
    
    error_lower = error_message.lower()
    
    if any(word in error_lower for word in ['path', 'file', 'directory', 'not found', 'does not exist']):
        return f"""📁 **File Access Issue**

**Problem**: {error_message}

**Likely Cause**: The corpus path you specified cannot be found or accessed.

**Solutions**:
1. **Check the path**: Verify the corpus directory exists
2. **Use absolute paths**: Try the full path (e.g., `/full/path/to/corpus`)
3. **Check permissions**: Ensure you have read access to the directory
4. **Available corpora**: Use one of the corpus paths listed below

**Example**: `data/inaugural_addresses` or `projects/vanderveen`"""
    
    elif any(word in error_lower for word in ['network', 'connection', 'timeout', 'api', 'http']):
        return f"""🌐 **Network/API Issue**

**Problem**: {error_message}

**Likely Cause**: Network connectivity or API service issue.

**Solutions**:
1. **Check internet connection**: Ensure you're connected to the internet
2. **Try again**: Temporary API issues often resolve quickly
3. **Check API keys**: Verify your LLM API credentials are configured
4. **Wait and retry**: If services are overloaded, try again in a few minutes

**Note**: The system will fall back to mock responses if APIs are unavailable."""
    
    elif any(word in error_lower for word in ['llm', 'model', 'ai', 'anthropic', 'openai']):
        return f"""🤖 **LLM Service Issue**

**Problem**: {error_message}

**Likely Cause**: Issue with the AI language model services.

**Solutions**:
1. **Check API status**: AI services occasionally have outages
2. **Verify credentials**: Ensure your API keys are valid
3. **Try different model**: System can use multiple AI providers
4. **Mock mode**: System will use mock responses if needed

**Available Models**: Claude, GPT-4, and local models if configured."""
    
    elif any(word in error_lower for word in ['async', 'await', 'coroutine', 'thread']):
        return f"""⚙️ **System Processing Issue**

**Problem**: {error_message}

**Likely Cause**: Internal system processing error.

**Solutions**:
1. **Try again**: The system may recover automatically
2. **Simplify request**: Try with a smaller corpus or simpler question
3. **Check system resources**: Ensure adequate memory and processing power
4. **Restart session**: Clear the chat and start a new session

**Note**: Complex multi-LLM analyses require significant processing time."""
    
    elif any(word in error_lower for word in ['json', 'parse', 'format', 'syntax']):
        return f"""📄 **Data Format Issue**

**Problem**: {error_message}

**Likely Cause**: Data parsing or format error.

**Solutions**:
1. **Check file formats**: Ensure corpus files are plain text (.txt)
2. **Verify encoding**: Files should be UTF-8 encoded
3. **Remove special characters**: Avoid unusual characters in filenames
4. **Try different corpus**: Test with a known working corpus

**Supported Formats**: Plain text files (.txt) in UTF-8 encoding."""
    
    else:
        return f"""⚠️ **Unknown System Error**

**Problem**: {error_message}

**Likely Cause**: An unexpected error occurred in the system.

**Solutions**:
1. **Try again**: Many issues resolve on retry
2. **Restart session**: Clear the chat and start fresh
3. **Check logs**: Look for additional error details
4. **Contact support**: If the issue persists, report the error

**Error Details**: {error_message}

**System Status**: The core system is designed to be resilient and should recover automatically."""

@app.route('/api/sessions')
def api_sessions():
    """
    API endpoint for research sessions
    
    THIN Principle: Just call session summarizer and return results
    """
    try:
        sessions = summarize_all_sessions()
        
        # Convert to list format for frontend
        session_list = []
        for session_id, manifest in sessions.items():
            session_list.append({
                'id': session_id,
                'friendly_name': manifest['friendly_name'],
                'summary': manifest['summary'],
                'research_question': manifest['research_question'],
                'timestamp': manifest['timestamp'],
                'corpus_description': manifest.get('corpus_description', 'Unknown corpus'),
                'key_findings': manifest.get('key_findings', []),
                'session_path': manifest['session_path']
            })
        
        # Sort by timestamp (newest first)
        session_list.sort(key=lambda x: x['timestamp'], reverse=True)
        
        # Check if we should limit to recent items (for dashboard)
        limit = request.args.get('limit', type=int)
        if limit:
            session_list = session_list[:limit]
        
        return jsonify({
            'status': 'success',
            'sessions': session_list
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error loading sessions: {str(e)}'
        }), 500


@app.route('/api/corpora')
def api_corpora():
    """
    API endpoint for available corpora
    
    THIN Principle: Just call corpus library and return results
    """
    try:
        corpora = discover_corpora()
        
        # Convert to list format for frontend
        corpus_list = []
        for corpus_path, info in corpora.items():
            corpus_list.append({
                'path': corpus_path,
                'friendly_name': info['friendly_name'],
                'description': info['description'],
                'file_count': info['file_count'],
                'total_size': info['total_size'],
                'language': info['language'],
                'time_period': info['time_period'],
                'research_themes': info['research_themes'],
                'sample_files': info['sample_files']
            })
        
        # Check if we should limit to recent items (for dashboard)
        limit = request.args.get('limit', type=int)
        if limit:
            corpus_list = corpus_list[:limit]
        
        return jsonify({
            'status': 'success',
            'corpora': corpus_list
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error loading corpora: {str(e)}'
        }), 500


@app.route('/session/<session_id>')
def view_session(session_id):
    """
    Display full conversation for a research session
    
    THIN Principle: Just read and display conversation file
    """
    session_path = project_root / "research_sessions" / session_id
    conversation_file = session_path / "conversation_readable.md"
    
    if not conversation_file.exists():
        return f"Session {session_id} not found", 404
    
    try:
        with open(conversation_file, 'r', encoding='utf-8') as f:
            conversation_content = f.read()
        
        # Read metadata if available
        metadata_file = session_path / "metadata.json"
        metadata = {}
        if metadata_file.exists():
            with open(metadata_file, 'r') as f:
                metadata = json.load(f)
        
        return render_template('session.html', 
                             session_id=session_id,
                             conversation_content=conversation_content,
                             metadata=metadata)
    
    except Exception as e:
        return f"Error reading session: {str(e)}", 500


@app.route('/api/session/<session_id>/conversation')
def api_session_conversation(session_id):
    """
    API endpoint for session conversation content
    
    THIN Principle: Raw file serving, no processing
    """
    session_path = project_root / "research_sessions" / session_id
    conversation_file = session_path / "conversation_readable.md"
    
    if not conversation_file.exists():
        return jsonify({'status': 'error', 'message': 'Session not found'}), 404
    
    try:
        with open(conversation_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return jsonify({
            'status': 'success',
            'content': content,
            'session_id': session_id
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error reading conversation: {str(e)}'
        }), 500


@app.route('/sessions')
def sessions_page():
    """
    Dedicated sessions browsing page
    
    THIN Principle: Pure interface to session library
    """
    return render_template('sessions.html')


@app.route('/corpora')
def corpora_page():
    """
    Dedicated corpora browsing page
    
    THIN Principle: Pure interface to corpus library
    """
    return render_template('corpora.html')


@app.route('/new-session')
def new_session():
    """
    New research session interface
    
    THIN Principle: Pure form interface to start new research
    """
    return render_template('new_session.html')


@app.route('/api/start-session', methods=['POST'])
def api_start_session():
    """
    API endpoint to start new research session
    
    THIN Principle: Just collect parameters and redirect to natural corpus demo
    """
    try:
        data = request.get_json()
        corpus_path = data.get('corpus_path', '')
        research_observation = data.get('research_observation', '')
        
        # For now, return instructions to use CLI
        # In future, integrate with orchestrator directly
        return jsonify({
            'status': 'success',
            'message': f'To start this research session, run:\npython3 discernus/demo/natural_corpus_demo.py\nCorpus: {corpus_path}\nObservation: {research_observation}',
            'next_steps': 'CLI integration coming soon'
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error starting session: {str(e)}'
        }), 500


@app.route('/api/session/<session_id>/updates')
def api_session_updates(session_id):
    """
    Get live updates for a session - returns new messages since last check
    
    THIN Principle: Just read conversation log and return new entries
    """
    try:
        session = chat_sessions.get(session_id)
        if not session:
            return jsonify({
                'status': 'error',
                'message': 'Session not found'
            }), 404
        
        conversation_file = session.get('conversation_file')
        if not conversation_file or not Path(conversation_file).exists():
            return jsonify({
                'status': 'success',
                'updates': []
            })
        
        # Get last_seen parameter to return only new messages
        last_seen = request.args.get('last_seen', type=int, default=0)
        
        # Read conversation log and return entries after last_seen
        updates = []
        try:
            with open(conversation_file, 'r') as f:
                lines = f.readlines()
                
                for i, line in enumerate(lines):
                    if i <= last_seen:
                        continue
                        
                    try:
                        log_entry = json.loads(line.strip())
                        participant = log_entry.get('participant', 'unknown')
                        message = log_entry.get('message', '')
                        timestamp = log_entry.get('timestamp', '')
                        
                        updates.append({
                            'index': i,
                            'participant': participant,
                            'message': message,
                            'timestamp': timestamp,
                            'is_llm': participant.endswith('_llm')
                        })
                    except json.JSONDecodeError:
                        continue
        
        except Exception as e:
            print(f"Error reading conversation file: {e}")
        
        return jsonify({
            'status': 'success',
            'updates': updates,
            'session_phase': session.get('phase', 'unknown'),
            'session_status': session.get('phase', 'unknown')
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error getting updates: {str(e)}'
        }), 500


if __name__ == '__main__':
    print("🌐 Starting Discernus Research Artifact UX...")
    print("📚 Access at: http://localhost:5001")
    print("🔬 Discover sessions and corpora through academic interface")
    
    app.run(debug=True, port=5001) 