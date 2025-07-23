#!/usr/bin/env python3
"""
OrchestratorAgent - LLM-powered experiment orchestration
Receives orchestration requests, uses LLM to plan task queues, enqueues tasks.
"""

import redis
import json
import yaml
import sys
import os
import logging
from typing import Dict, Any, List
from litellm import completion

# Add scripts directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))
from minio_client import put_artifact

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - OrchestratorAgent - %(message)s')
logger = logging.getLogger(__name__)

# Redis configuration
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = 6379
REDIS_DB = 0
CONSUMER_GROUP = 'discernus'

class OrchestratorAgentError(Exception):
    """Agent-specific exceptions"""
    pass

class OrchestratorAgent:
    """LLM-powered orchestration agent"""
    
    def __init__(self):
        self.redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
        self.prompt_template = self._load_prompt_template()
        
    def _load_prompt_template(self) -> str:
        """Load external prompt template - NO PARSING, just string formatting"""
        try:
            prompt_path = os.path.join(os.path.dirname(__file__), 'prompt.yaml')
            with open(prompt_path, 'r') as f:
                prompt_data = yaml.safe_load(f)
            return prompt_data['template']
        except Exception as e:
            logger.error(f"Failed to load prompt template: {e}")
            raise OrchestratorAgentError(f"Prompt loading failed: {e}")
    
    def orchestrate_experiment(self, orchestration_data: Dict[str, Any]) -> bool:
        """Use LLM to plan and enqueue experiment tasks"""
        try:
            experiment = orchestration_data['experiment']
            framework_hash = orchestration_data['framework_hash']
            corpus_hashes = orchestration_data['corpus_hashes']
            
            logger.info(f"Orchestrating experiment: {experiment.get('name', 'unnamed')}")
            logger.info(f"Framework: {framework_hash[:12]}..., Corpus files: {len(corpus_hashes)}")
            
            # Format orchestrator prompt (THIN - just string substitution)
            prompt_text = self.prompt_template.format(
                experiment=json.dumps(experiment, indent=2),
                framework_hash=framework_hash,
                corpus_hashes=json.dumps(corpus_hashes, indent=2)
            )
            
            # Ask LLM what tasks to create (LLM intelligence, not software parsing)
            logger.info("Asking LLM to plan experiment tasks...")
            # Use Gemini Flash for orchestration planning with safety settings for political content
            planning_response = completion(
                model="gemini-2.5-flash",
                messages=[{"role": "user", "content": prompt_text}],
                temperature=0.0,
                safety_settings=[
                    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
                ]
            )
            
            # THIN approach: Store raw LLM response and let another LLM execute it
            llm_content = planning_response.choices[0].message.content
            if not llm_content or llm_content.strip() == "":
                logger.error(f"LLM returned empty response. Full response: {planning_response}")
                return False
            
            logger.info(f"LLM generated {len(llm_content)} character plan")
            
            # Store raw orchestration plan (THIN - no parsing, just storage)
            import time
            raw_plan_content = {
                'experiment': experiment,
                'framework_hash': framework_hash,
                'corpus_hashes': corpus_hashes,
                'raw_llm_plan': llm_content,
                'orchestration_timestamp': time.time()
            }
            plan_hash = put_artifact(json.dumps(raw_plan_content, indent=2).encode('utf-8'))
            logger.info(f"Raw orchestration plan stored: {plan_hash}")
            
            # Create single execution task - let downstream LLM interpret the plan
            message_id = self.redis_client.xadd('tasks', {
                'type': 'execute_plan',
                'data': json.dumps({
                    'plan_hash': plan_hash,
                    'experiment_name': experiment.get('name', 'unknown')
                })
            })
            logger.info(f"Plan execution task enqueued: {message_id}")
            
            logger.info("Orchestration complete: Raw plan stored and execution task created")
            return True
            
        except json.JSONDecodeError as e:
            logger.error(f"LLM returned invalid JSON: {e}")
            return False
        except Exception as e:
            logger.error(f"Orchestration error: {e}")
            return False
    
    def listen_for_orchestration_requests(self):
        """Listen for orchestration requests on orchestrator.tasks stream"""
        logger.info("OrchestratorAgent listening for requests...")
        
        try:
            while True:
                # Read orchestration requests (blocking)
                messages = self.redis_client.xreadgroup(
                    CONSUMER_GROUP, 'orchestrator',
                    {'orchestrator.tasks': '>'},
                    count=1, block=0  # Block until message available
                )
                
                for stream, msgs in messages:
                    for msg_id, fields in msgs:
                        try:
                            orchestration_data = json.loads(fields[b'data'])
                            
                            # Process orchestration request
                            success = self.orchestrate_experiment(orchestration_data)
                            
                            if success:
                                logger.info(f"Orchestration request completed: {msg_id}")
                            else:
                                logger.error(f"Orchestration request failed: {msg_id}")
                            
                            # Acknowledge message
                            self.redis_client.xack('orchestrator.tasks', CONSUMER_GROUP, msg_id)
                            
                        except Exception as e:
                            logger.error(f"Error processing orchestration request: {e}")
                            continue
                            
        except KeyboardInterrupt:
            logger.info("OrchestratorAgent shutdown requested")
        except Exception as e:
            logger.error(f"Orchestrator listening error: {e}")
            raise

def main():
    """Agent entry point"""
    agent = OrchestratorAgent()
    
    try:
        # Start listening for orchestration requests
        agent.listen_for_orchestration_requests()
    except Exception as e:
        logger.error(f"OrchestratorAgent failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 