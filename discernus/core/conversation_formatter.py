#!/usr/bin/env python3
"""
Conversation Formatter
=====================

Converts JSONL conversation logs to human-readable markdown format.
Ultra-thin: just formatting, no analysis or intelligence.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any


def format_conversation_to_markdown(conversation_id: str, project_root: str = ".") -> str:
    """
    Convert JSONL conversation to readable markdown format
    
    Args:
        conversation_id: Conversation identifier
        project_root: Project root directory
        
    Returns:
        Formatted markdown conversation log
    """
    project_path = Path(project_root)
    jsonl_file = project_path / "conversations" / f"{conversation_id}.jsonl"
    
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
    
    # Start markdown formatting
    markdown = []
    markdown.append(f"# 🎯 Conversation Log: {conversation_id}")
    markdown.append("=" * 80)
    markdown.append("")
    
    # Add metadata
    if metadata:
        markdown.append("## 📋 Conversation Metadata")
        if 'research_question' in metadata:
            markdown.append(f"**Research Question:** {metadata['research_question']}")
        if 'participants' in metadata:
            participants = ", ".join(metadata['participants'])
            markdown.append(f"**Participants:** {participants}")
        if 'started_at' in metadata:
            started = metadata['started_at'][:19]  # Remove microseconds
            markdown.append(f"**Started:** {started}")
        markdown.append("")
    
    # Format messages
    markdown.append("## 💬 Conversation Flow")
    markdown.append("")
    
    for i, message in enumerate(messages):
        timestamp = message['timestamp'][:19]  # Remove microseconds
        speaker = message['speaker']
        content = message['message']
        
        # Skip system messages for readability
        if speaker == 'system':
            if content == 'CONVERSATION_START':
                continue
            elif content == 'CONVERSATION_END':
                markdown.append("---")
                markdown.append("🎉 **Conversation Completed**")
                markdown.append("")
                continue
        
        # Format speaker name
        speaker_names = {
            'design_llm': '🎨 Design LLM',
            'moderator_llm': '🔄 Moderator LLM',
            'unity_expert': '🤝 Unity Expert',
            'division_expert': '⚡ Division Expert',
            'adversarial_llm': '🥊 Adversarial LLM',
            'analysis_llm': '📊 Analysis LLM',
            'referee_llm': '⚖️ Referee LLM'
        }
        
        display_name = speaker_names.get(speaker, speaker.replace('_', ' ').title())
        
        # Add message
        time_only = timestamp.split()[-1] if ' ' in timestamp else timestamp.split('T')[-1]
        markdown.append(f"### {display_name} *(at {time_only})*")
        markdown.append("")
        markdown.append(content)
        markdown.append("")
        markdown.append("---")
        markdown.append("")
    
    return "\n".join(markdown)


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