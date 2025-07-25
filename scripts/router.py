#!/usr/bin/env python3
"""
Discernus PoC Router - Redis Streams Task Router
Thin router that moves tasks between streams with NO business logic.
"""

import redis
import json
import os
import subprocess
import logging
import time
import sys
from concurrent.futures import ThreadPoolExecutor, Future
from typing import Dict, Any

# Get the current Python executable (works in any environment)
PYTHON_EXECUTABLE = sys.executable

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Redis configuration
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = 6379
REDIS_DB = 0

# Stream names
TASKS_STREAM = 'tasks'
TASKS_DONE_STREAM = 'tasks.done'
ORCHESTRATOR_STREAM = 'orchestrator.tasks'
CONSUMER_GROUP = 'discernus'

# Agent type to script mapping - uses current Python executable automatically
AGENT_SCRIPTS = {
    'analyse': [PYTHON_EXECUTABLE, 'agents/AnalyseChunkAgent/main.py'],
    'orchestrate': [PYTHON_EXECUTABLE, 'agents/OrchestratorAgent/main.py'],
    'synthesize': [PYTHON_EXECUTABLE, 'agents/SynthesisAgent/main.py'],
    # Modern Redis-based agents with YAML prompts
    'analyse_batch': [PYTHON_EXECUTABLE, 'agents/AnalyseBatchAgent/main.py'],
    'meta_synthesis': [PYTHON_EXECUTABLE, 'agents/MetaAnalysisSynthesisAgent/main.py'],
    'synthesis': [PYTHON_EXECUTABLE, 'agents/SynthesisAgent/main.py'],
    'pre_test': [PYTHON_EXECUTABLE, 'agents/PreTestAgent/main.py'],
    # Phase 2 Components
    'execute_plan': [PYTHON_EXECUTABLE, 'scripts/execution_bridge.py'],
    # Phase 3 Quality Assurance agents
    'review': [PYTHON_EXECUTABLE, 'agents/ReviewerAgent/main.py'],
    # Alpha System Components - BaseAgent standardized
    'report': [PYTHON_EXECUTABLE, 'agents/ReportAgent/main.py'],
}

class RouterError(Exception):
    """Router-specific exceptions"""
    pass

class DiscernusRouter:
    def __init__(self):
        self.redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
        self.running = True
        self.active_processes = {}
        # ThreadPoolExecutor for reliable agent spawning
        self.executor = ThreadPoolExecutor(max_workers=10, thread_name_prefix="agent-")
        self.active_futures = {}  # task_id -> Future mapping
        
    def setup_streams(self):
        """Initialize Redis streams and consumer groups"""
        try:
            # Create consumer groups (idempotent)
            streams_to_setup = [TASKS_STREAM, TASKS_DONE_STREAM, ORCHESTRATOR_STREAM]
            
            for stream in streams_to_setup:
                try:
                    self.redis_client.xgroup_create(stream, CONSUMER_GROUP, id='0-0', mkstream=True)
                    logger.info(f"Created consumer group '{CONSUMER_GROUP}' for stream '{stream}'")
                except redis.exceptions.ResponseError as e:
                    if "BUSYGROUP" in str(e):
                        logger.info(f"Consumer group '{CONSUMER_GROUP}' already exists for stream '{stream}'")
                    else:
                        raise
                        
        except Exception as e:
            logger.error(f"Failed to setup streams: {e}")
            raise RouterError(f"Stream setup failed: {e}")

    def enqueue_task(self, task_type: str, task_data: Dict[str, Any]) -> str:
        """Simple task publisher - called by CLI or agents"""
        try:
            message_data = {
                'type': task_type,
                'data': json.dumps(task_data),
                'timestamp': time.time()
            }
            
            message_id = self.redis_client.xadd(TASKS_STREAM, message_data)
            logger.info(f"Enqueued task {task_type}: {message_id}")
            return message_id.decode()
            
        except Exception as e:
            logger.error(f"Failed to enqueue task: {e}")
            raise RouterError(f"Task enqueue failed: {e}")

    def complete_task(self, task_id: str, result_data: Dict[str, Any]) -> str:
        """Called by agents when done"""
        try:
            completion_data = {
                'original_task_id': task_id,
                'data': json.dumps(result_data),
                'timestamp': time.time()
            }
            
            message_id = self.redis_client.xadd(TASKS_DONE_STREAM, completion_data)
            logger.info(f"Task completed: {task_id} -> {message_id}")
            return message_id.decode()
            
        except Exception as e:
            logger.error(f"Failed to complete task: {e}")
            raise RouterError(f"Task completion failed: {e}")

    def _run_agent_process(self, task_type: str, task_id: str, script_cmd: list) -> bool:
        """Run agent process with comprehensive error handling and logging."""
        try:
            logger.info(f"Starting {task_type} agent for task {task_id}: {' '.join(script_cmd)}")
            logger.info(f"Working directory: {os.getcwd()}")
            logger.info(f"Full command: {script_cmd}")
            
            # Run the agent process with full error capture
            result = subprocess.run(
                script_cmd,
                cwd='.',
                capture_output=True,
                text=True,
                timeout=1800  # 30 minute timeout
            )
            
            # Log stdout/stderr for debugging
            if result.stdout:
                logger.info(f"Agent {task_id} stdout: {result.stdout[:500]}...")
            if result.stderr:
                logger.warning(f"Agent {task_id} stderr: {result.stderr[:500]}...")
            
            if result.returncode == 0:
                logger.info(f"Agent {task_type} completed successfully for task {task_id}")
                return True
            else:
                logger.error(f"Agent {task_type} failed for task {task_id} with return code {result.returncode}")
                return False
                
        except subprocess.TimeoutExpired:
            logger.error(f"Agent {task_type} timed out for task {task_id}")
            return False
        except FileNotFoundError as e:
            logger.error(f"Agent script not found for {task_type}: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error running {task_type} agent for task {task_id}: {e}")
            return False

    def route_task(self, task_type: str, task_id: str, task_info: Dict[str, Any] = None) -> bool:
        """Route task to appropriate agent using ThreadPoolExecutor - NO BUSINESS LOGIC"""
        try:
            if task_type not in AGENT_SCRIPTS:
                logger.error(f"Unknown task type: {task_type}")
                return False
            
            # Store task data in Redis for agent retrieval (if provided)
            if task_info:
                task_data_key = f"task:{task_id}:data"
                self.redis_client.set(task_data_key, json.dumps(task_info), ex=3600)  # 1 hour TTL
                logger.info(f"Stored task data in Redis key: {task_data_key}")
                
            # Get agent script command
            script_cmd = AGENT_SCRIPTS[task_type] + [task_id]
            
            # Submit to thread pool for reliable execution
            future = self.executor.submit(self._run_agent_process, task_type, task_id, script_cmd)
            self.active_futures[task_id] = future
            
            logger.info(f"Submitted {task_type} agent for task {task_id} to thread pool")
            return True
            
        except Exception as e:
            logger.error(f"Failed to route task {task_id}: {e}")
            return False

    def handle_completed_tasks(self):
        """Process completed tasks and clean up finished futures"""
        try:
            # Clean up completed futures
            completed_tasks = []
            for task_id, future in list(self.active_futures.items()):
                if future.done():
                    try:
                        success = future.result()  # This will raise exception if agent failed
                        if success:
                            logger.info(f"Agent completed successfully for task {task_id}")
                        else:
                            logger.error(f"Agent failed for task {task_id}")
                    except Exception as e:
                        logger.error(f"Agent exception for task {task_id}: {e}")
                    
                    completed_tasks.append(task_id)
            
            # Clean up completed futures
            for task_id in completed_tasks:
                self.active_futures.pop(task_id, None)
                        
        except Exception as e:
            logger.error(f"Error in completion handler: {e}")

    def route_pending_tasks(self):
        """Route new tasks to agents using BRPOP list pattern (per architecture spec 4.2)"""
        try:
            logger.info(f"Checking for pending tasks in list 'tasks' with BRPOP")
            
            # Use BRPOP instead of XREADGROUP (no consumer groups, no races)
            result = self.redis_client.brpop('tasks', timeout=1)
            
            if result:
                list_name, task_data = result
                logger.info(f"Got task from list '{list_name}'")
                
                try:
                    # Parse task data (type is now embedded in the data)
                    task_info = json.loads(task_data)
                    task_type = task_info.get('type')
                    
                    if not task_type:
                        logger.error(f"Task missing 'type' field: {task_data}")
                        return
                    
                    logger.info(f"Processing task type: {task_type}")
                    
                    # Generate task ID for tracking
                    task_id = task_info.get('run_id', 'unknown') + f"_{task_type}"
                    
                    # Route task (THIN - no logic, just dispatch)
                    if self.route_task(task_type, task_id, task_info):
                        logger.info(f"Routed {task_type} task: {task_id}")
                    else:
                        logger.error(f"Failed to route {task_type} task: {task_id}")
                        
                except Exception as e:
                    logger.error(f"Error processing task: {e}")
            else:
                logger.info("No tasks available (BRPOP timeout)")
                        
        except Exception as e:
            logger.error(f"Error in task router: {e}")

    def main_loop(self):
        """Main router loop - just moves tasks between streams"""
        logger.info("Starting Discernus Router...")
        
        try:
            while self.running:
                logger.info("Router main loop iteration starting")
                
                # Handle completed tasks
                self.handle_completed_tasks()
                logger.info("Completed task handling")
                
                # Route new tasks
                self.route_pending_tasks()
                logger.info("Completed task routing")
                
                # Brief sleep to prevent busy loop
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            logger.info("Router shutdown requested")
            self.shutdown()
        except Exception as e:
            logger.error(f"Router main loop error: {e}")
            raise

    def shutdown(self):
        """Graceful shutdown"""
        logger.info("Shutting down router...")
        self.running = False
        
        # Shutdown thread pool executor
        logger.info(f"Waiting for {len(self.active_futures)} active tasks to complete...")
        self.executor.shutdown(wait=True, timeout=60)
        
        # Clean up any remaining tracking
        self.active_processes.clear()
        self.active_futures.clear()
                
        logger.info("Router shutdown complete")

def main():
    """Router entry point"""
    router = DiscernusRouter()
    
    try:
        # No longer need streams setup - using Redis lists per architecture spec 4.2
        # router.setup_streams()
        
        # Start main loop
        router.main_loop()
        
    except Exception as e:
        logger.error(f"Router failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 