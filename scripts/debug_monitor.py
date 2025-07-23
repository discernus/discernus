#!/usr/bin/env python3
"""
Development monitoring script for real-time system visibility
Provides immediate status without hanging operations
"""

import redis
import json
import time
import sys
from datetime import datetime

def get_system_status():
    """Get immediate system status - no blocking operations"""
    try:
        r = redis.Redis(host='localhost', port=6379, db=0, socket_timeout=2)
        
        status = {
            'timestamp': datetime.now().strftime('%H:%M:%S.%f')[:-3],
            'orchestrator_queue': r.xlen('orchestrator.tasks'),
            'analysis_queue': r.xlen('tasks'), 
            'completed_tasks': r.xlen('tasks.done'),
            'status': 'CONNECTED'
        }
        
        # Get latest task IDs without blocking
        try:
            latest_orch = r.xrevrange('orchestrator.tasks', count=1)
            if latest_orch:
                status['latest_orchestrator_task'] = latest_orch[0][0].decode()
        except:
            pass
            
        try:
            latest_task = r.xrevrange('tasks', count=1)
            if latest_task:
                status['latest_analysis_task'] = latest_task[0][0].decode()
        except:
            pass
            
        return status
        
    except Exception as e:
        return {
            'timestamp': datetime.now().strftime('%H:%M:%S.%f')[:-3],
            'status': f'ERROR: {e}',
            'orchestrator_queue': '?',
            'analysis_queue': '?', 
            'completed_tasks': '?'
        }

def print_status():
    """Print current status in readable format"""
    status = get_system_status()
    
    print(f"\n=== SYSTEM STATUS [{status['timestamp']}] ===")
    print(f"Orchestrator Queue: {status['orchestrator_queue']}")
    print(f"Analysis Queue: {status['analysis_queue']}")  
    print(f"Completed Tasks: {status['completed_tasks']}")
    print(f"Status: {status['status']}")
    
    if 'latest_orchestrator_task' in status:
        print(f"Latest Orchestrator Task: {status['latest_orchestrator_task']}")
    if 'latest_analysis_task' in status:
        print(f"Latest Analysis Task: {status['latest_analysis_task']}")
    
    return status

def monitor_single_orchestrator_task():
    """Process exactly one orchestrator task with full visibility"""
    try:
        r = redis.Redis(host='localhost', port=6379, db=0, socket_timeout=5)
        
        print("\n=== ATTEMPTING TO PROCESS ONE ORCHESTRATOR TASK ===")
        
        # Check if there are tasks
        task_count = r.xlen('orchestrator.tasks')
        print(f"Tasks in orchestrator queue: {task_count}")
        
        if task_count == 0:
            print("No orchestrator tasks to process")
            return False
            
        # Try to read one message (with timeout)
        try:
            messages = r.xreadgroup('discernus', 'orchestrator', {'orchestrator.tasks': '>'}, count=1, block=5000)
            
            if not messages or not messages[0][1]:
                print("No new messages available (consumer group may be caught up)")
                return False
                
            msg_id, fields = messages[0][1][0]
            print(f"Retrieved task: {msg_id.decode()}")
            
            # Parse the data
            orchestration_data = json.loads(fields[b'data'])
            experiment_name = orchestration_data.get('experiment', {}).get('name', 'unknown')
            print(f"Processing experiment: {experiment_name}")
            
            # Import and create orchestrator
            sys.path.append('agents/OrchestratorAgent')
            from main import OrchestratorAgent
            
            orchestrator = OrchestratorAgent()
            
            print("Calling orchestrator.orchestrate_experiment()...")
            start_time = time.time()
            
            success = orchestrator.orchestrate_experiment(orchestration_data)
            
            end_time = time.time()
            print(f"Orchestration completed in {end_time - start_time:.2f} seconds")
            print(f"Result: {'SUCCESS' if success else 'FAILED'}")
            
            if success:
                r.xack('orchestrator.tasks', 'discernus', msg_id)
                print("Task acknowledged")
                
                # Check if new analysis tasks were created
                new_status = get_system_status()
                print(f"Analysis queue after orchestration: {new_status['analysis_queue']}")
                
            return success
            
        except redis.exceptions.ResponseError as e:
            if "NOGROUP" in str(e):
                print("Consumer group doesn't exist - creating it")
                r.xgroup_create('orchestrator.tasks', 'discernus', '0', mkstream=True)
                return monitor_single_orchestrator_task()  # Retry once
            else:
                print(f"Redis error: {e}")
                return False
                
    except Exception as e:
        print(f"Error processing orchestrator task: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'process':
        monitor_single_orchestrator_task()
    else:
        print_status() 