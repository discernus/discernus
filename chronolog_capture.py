#!/usr/bin/env python3
"""
THIN Chronolog Capture
=====================

Simple Redis subscriber that captures SOAR events and writes to JSONL files.
"""

import redis
import json
from pathlib import Path
from datetime import datetime

def capture_chronolog():
    """THIN: Subscribe to SOAR events and write to JSONL"""
    
    # Connect to Redis
    redis_client = redis.Redis(host='localhost', port=6379, db=0)
    pubsub = redis_client.pubsub()
    
    # Subscribe to all SOAR events
    pubsub.psubscribe('soar.*')
    
    print("📊 Chronolog capture started - listening for SOAR events...")
    
    try:
        for message in pubsub.listen():
            if message['type'] == 'pmessage':
                # Parse event
                channel = message['channel'].decode('utf-8')
                data = json.loads(message['data'].decode('utf-8'))
                
                # Extract session ID for file naming
                session_id = data.get('session_id', 'unknown_session')
                
                # Create chronolog file path
                chronolog_dir = Path("chronolog")
                chronolog_dir.mkdir(exist_ok=True)
                chronolog_file = chronolog_dir / f"{session_id}.jsonl"
                
                # Write event to JSONL
                event_entry = {
                    "channel": channel,
                    "timestamp": data.get('timestamp', datetime.utcnow().isoformat()),
                    "session_id": session_id,
                    "data": data
                }
                
                with open(chronolog_file, 'a') as f:
                    f.write(json.dumps(event_entry) + '\n')
                
                print(f"📝 {channel} → {chronolog_file}")
                
    except KeyboardInterrupt:
        print("\n📊 Chronolog capture stopped")
        pubsub.close()

if __name__ == '__main__':
    capture_chronolog() 