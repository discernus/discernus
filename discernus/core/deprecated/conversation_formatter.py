#!/usr/bin/env python3
"""
Conversation Formatter
=====================

Converts JSONL conversation logs to human-readable markdown format.
Ultra-thin: uses LLM intelligence for formatting instead of brittle parsing.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
from .agent_roles import get_expert_prompt


def format_conversation_to_markdown(conversation_id: str, project_root: str = ".") -> str:
    """
    Convert JSONL conversation to readable markdown format using LLM
    
    Args:
        conversation_id: Conversation identifier
        project_root: Project root directory (should be session folder path)
        
    Returns:
        Formatted markdown conversation log
    """
    project_path = Path(project_root)
    jsonl_file = project_path / f"{conversation_id}.jsonl"
    
    if not jsonl_file.exists():
        return f"❌ Conversation file not found: {jsonl_file}"
    
    # Read JSONL messages
    messages = []
    with open(jsonl_file, 'r', encoding='utf-8') as f:
        for line in f:
            messages.append(json.loads(line.strip()))
    
    if not messages:
        return "❌ No messages found in conversation file"
    
    # Extract metadata from first message
    first_msg = messages[0]
    metadata = first_msg.get('metadata', {})
    
    # Prepare data for LLM formatting
    conversation_data = {
        "conversation_id": conversation_id,
        "metadata": metadata,
        "messages": messages,
        "total_messages": len(messages)
    }
    
    # Create formatting prompt
    prompt = _create_formatting_prompt(conversation_data)
    
    # Get LLM formatted version
    try:
        from .thin_litellm_client import ThinLiteLLMClient
        client = ThinLiteLLMClient()
        
        formatted_markdown = client.get_completion(
            prompt, 
            model="claude-3-haiku-20240307",
            max_tokens=8000
        )
        
        # THIN integrity check
        if _passes_integrity_check(messages, formatted_markdown):
            return formatted_markdown
        else:
            # Fallback to basic format if integrity check fails
            return _create_basic_fallback(conversation_data)
            
    except Exception as e:
        # Fallback on any error
        return _create_basic_fallback(conversation_data)


def _create_formatting_prompt(conversation_data: Dict) -> str:
    """Create the LLM formatting prompt."""
    return f"""Convert this conversation log to clean, readable markdown format.

CONVERSATION DATA:
{json.dumps(conversation_data, indent=2)}

REQUIREMENTS:
1. Start with conversation metadata header including ID, research question, participants, timestamps
2. Format each message with readable speaker names:
   - design_llm -> 🎨 Design LLM
   - moderator_llm -> 🔄 Moderator LLM
   - unity_expert -> 🤝 Unity Expert
   - division_expert -> ⚡ Division Expert
   - adversarial_llm -> 🥊 Adversarial LLM
   - analysis_llm -> 📊 Analysis LLM
   - referee_llm -> ⚖️ Referee LLM
   - discernuslibrarian_agent -> 🧠 DiscernusLibrarian Agent
   - Rhetoric_Analyst_LLM -> 📝 Rhetoric Analyst
   - Political_Comms_LLM -> 🗳️ Political Communications Expert
3. Include timestamps (time only) for each message
4. Skip system messages like 'CONVERSATION_START' for readability
5. For 'CONVERSATION_END', show "🎉 Conversation Completed"
6. Preserve ALL original content exactly - do not summarize, paraphrase, or modify any content
7. Use professional markdown formatting with headers and separators
8. Handle null/empty content gracefully

Return only the formatted markdown, no additional commentary."""


def _passes_integrity_check(original_messages: List[Dict], formatted_markdown: str) -> bool:
    """THIN integrity check - just basic sanity checks."""
    try:
        # Count non-system messages in original
        original_count = len([msg for msg in original_messages 
                            if msg.get('speaker') != 'system' and msg.get('message')])
        
        # Count headers in formatted (rough proxy for messages)
        formatted_count = formatted_markdown.count('###')
        
        # Check approximate length
        original_length = sum(len(str(msg.get('message', ''))) for msg in original_messages)
        formatted_length = len(formatted_markdown)
        
        # Very loose checks - just make sure we're in the right ballpark
        count_reasonable = abs(original_count - formatted_count) <= 3
        length_reasonable = formatted_length > original_length * 0.5
        
        return count_reasonable and length_reasonable
        
    except Exception:
        return False


def _create_basic_fallback(conversation_data: Dict) -> str:
    """Create basic fallback markdown if LLM formatting fails."""
    conversation_id = conversation_data['conversation_id']
    metadata = conversation_data['metadata']
    messages = conversation_data['messages']
    
    lines = [
        f"# 🎯 Conversation Log: {conversation_id}",
        "=" * 80,
        "",
        "## 📋 Conversation Metadata"
    ]
    
    if metadata:
        if 'research_question' in metadata:
            lines.append(f"**Research Question:** {metadata['research_question']}")
        if 'participants' in metadata:
            participants = ", ".join(metadata['participants'])
            lines.append(f"**Participants:** {participants}")
        if 'started_at' in metadata:
            started = metadata['started_at'][:19]
            lines.append(f"**Started:** {started}")
    
    lines.extend([
        "",
        "## 💬 Conversation Flow",
        ""
    ])
    
    for message in messages:
        if not message or 'message' not in message:
            continue
            
        timestamp = message.get('timestamp', 'unknown')[:19]
        speaker = message.get('speaker', 'unknown')
        content = message.get('message', '')
        
        if not content or speaker == 'system':
            continue
            
        time_only = timestamp.split()[-1] if ' ' in timestamp else timestamp.split('T')[-1]
        lines.extend([
            f"### {speaker.replace('_', ' ').title()} *(at {time_only})*",
            "",
            str(content),
            "",
            "---",
            ""
        ])
    
    return "\n".join(lines)


def save_formatted_conversation(conversation_id: str, project_root: str = ".") -> str:
    """
    Save formatted conversation to markdown file
    
    Args:
        conversation_id: Conversation identifier
        project_root: Project root directory
        
    Returns:
        Path to saved markdown file
    """
    project_path = Path(project_root)
    conversations_dir = project_path / "conversations"
    
    # Generate markdown
    markdown_content = format_conversation_to_markdown(conversation_id, project_root)
    
    # Save to file
    markdown_file = conversations_dir / f"{conversation_id}_readable.md"
    with open(markdown_file, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    return str(markdown_file)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python conversation_formatter.py <conversation_id>")
        sys.exit(1)
    
    conversation_id = sys.argv[1]
    
    try:
        markdown_file = save_formatted_conversation(conversation_id)
        print(f"✅ Conversation formatted and saved to: {markdown_file}")
    except Exception as e:
        print(f"❌ Error formatting conversation: {e}")
        sys.exit(1) 