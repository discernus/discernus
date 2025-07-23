#!/usr/bin/env python3
"""
Redis PEL (Pending Entry List) Cleanup Utility
Addresses the reviewer's concern about orphaned tasks in consumer groups.
"""

import redis
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def cleanup_pending_tasks(redis_client, stream_name='tasks', group_name='discernus', max_idle_ms=30000):
    """
    XPENDING → XCLAIM for orphaned IDs, with log summary of reclaimed count.
    
    Args:
        redis_client: Redis connection
        stream_name: Redis stream name
        group_name: Consumer group name  
        max_idle_ms: Maximum idle time before claiming (default 30 seconds)
    """
    try:
        # Get pending task info
        pending_info = redis_client.xpending_range(stream_name, group_name, min='-', max='+', count=100)
        
        if not pending_info:
            logger.info(f"No pending tasks in {group_name} group")
            return 0
            
        claimed_count = 0
        current_time = int(time.time() * 1000)  # Current time in milliseconds
        
        logger.info(f"Found {len(pending_info)} pending tasks in {group_name} group")
        
        for info in pending_info:
            msg_id, consumer, idle_time, delivery_count = info
            
            # Claim tasks that have been idle too long
            if idle_time > max_idle_ms:
                try:
                    # Claim the orphaned task
                    claimed = redis_client.xclaim(stream_name, group_name, 'cleanup-agent', max_idle_ms, msg_id)
                    
                    if claimed:
                        # Acknowledge the task to remove it from pending
                        redis_client.xack(stream_name, group_name, msg_id) 
                        claimed_count += 1
                        
                        # Log details
                        if isinstance(msg_id, bytes):
                            msg_id_str = msg_id.decode()
                        else:
                            msg_id_str = str(msg_id)
                            
                        logger.info(f"  Cleaned orphaned task: {msg_id_str} (idle: {idle_time}ms, deliveries: {delivery_count})")
                        
                except Exception as e:
                    logger.error(f"Failed to claim task {msg_id}: {e}")
                    
        logger.info(f"✅ PEL cleanup complete: {claimed_count} orphaned tasks reclaimed")
        return claimed_count
        
    except Exception as e:
        logger.error(f"PEL cleanup error: {e}")
        return 0

def main():
    """CLI entry point for PEL cleanup"""
    redis_client = redis.Redis(host='localhost', port=6379, db=0)
    
    try:
        # Test connection
        redis_client.ping()
        logger.info("Connected to Redis")
        
        # Run cleanup
        reclaimed = cleanup_pending_tasks(redis_client)
        
        # Show final status
        pending = redis_client.xpending('tasks', 'discernus')
        logger.info(f"Final PEL status: {pending['pending']} tasks still pending")
        
    except Exception as e:
        logger.error(f"Cleanup failed: {e}")
        return 1
        
    return 0

if __name__ == '__main__':
    exit(main()) 