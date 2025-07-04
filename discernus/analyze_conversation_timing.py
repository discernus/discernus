#!/usr/bin/env python3
"""
Conversation Timing Analyzer
============================

Analyze conversation flow timing from timestamped logs.
Shows elapsed time between messages for performance analysis.
"""

import re
import sys
from pathlib import Path
from datetime import datetime

def analyze_conversation_timing(session_id: str):
    """Analyze timing patterns in a conversation session"""
    
    log_file = Path(f"research_sessions/{session_id}/conversation_log.md")
    if not log_file.exists():
        print(f"❌ Session not found: {session_id}")
        return
    
    print(f"🕒 Conversation Timing Analysis: {session_id}")
    print("=" * 60)
    print("📅 All timestamps in UTC (Zulu time)")
    print("")
    
    # Parse conversation log for timestamps
    content = log_file.read_text()
    
    # Extract timestamp and role pairs from conversational format
    # Pattern: **Speaker Name said** *(at HH:MM:SSZ)*:
    pattern = r'\*\*(.*?) said\*\* \*\(at (\d{2}:\d{2}:\d{2}Z)\)\*:'
    matches = re.findall(pattern, content)
    
    if not matches:
        print("❌ No timestamped entries found. Run with updated logger.")
        return
    
    print(f"📊 Found {len(matches)} timestamped interactions\n")
    
    previous_time = None
    total_elapsed = 0
    session_date = datetime.now().date()  # Assume same day for time-only timestamps
    
    for i, (speaker, time_str) in enumerate(matches):
        # Parse UTC time-only format (remove 'Z' suffix) and add today's date
        time_str_clean = time_str.rstrip('Z')
        time_obj = datetime.strptime(time_str_clean, "%H:%M:%S").time()
        current_time = datetime.combine(session_date, time_obj)
        
        if previous_time:
            elapsed = (current_time - previous_time).total_seconds()
            # Handle day rollover (negative elapsed means crossed midnight)
            if elapsed < 0:
                elapsed += 24 * 60 * 60  # Add 24 hours
            total_elapsed += elapsed
            
            print(f"{i:2d}. {speaker:<15} ({time_str}) - +{elapsed:6.2f}s")
        else:
            print(f"{i:2d}. {speaker:<15} ({time_str}) - START")
            session_start = current_time
        
        previous_time = current_time
    
    print("\n" + "=" * 60)
    print(f"📈 Summary:")
    print(f"   Total messages: {len(matches)}")
    print(f"   Total elapsed: {total_elapsed:.2f} seconds")
    print(f"   Average per message: {total_elapsed/(len(matches)-1):.2f} seconds")
    
    if len(matches) > 1:
        session_duration = (previous_time - session_start).total_seconds()
        print(f"   Session duration: {session_duration:.2f} seconds")

def list_recent_sessions():
    """List recent conversation sessions for analysis"""
    sessions_dir = Path("research_sessions")
    if not sessions_dir.exists():
        print("❌ No research sessions found")
        return []
    
    sessions = [d.name for d in sessions_dir.iterdir() if d.is_dir()]
    sessions.sort(reverse=True)  # Most recent first
    
    print("📋 Recent Sessions:")
    for i, session in enumerate(sessions[:5]):  # Show last 5
        print(f"   {i+1}. {session}")
    
    return sessions

if __name__ == "__main__":
    if len(sys.argv) > 1:
        session_id = sys.argv[1]
        analyze_conversation_timing(session_id)
    else:
        print("🕒 Conversation Timing Analyzer")
        print("=" * 40)
        sessions = list_recent_sessions()
        
        if sessions:
            print(f"\nUsage: python3 {sys.argv[0]} <session_id>")
            print(f"Example: python3 {sys.argv[0]} {sessions[0]}")
        else:
            print("\nNo sessions found. Run a conversation first.") 