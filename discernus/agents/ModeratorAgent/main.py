#!/usr/bin/env python3
"""
ModeratorAgent - Phase 3 Conversation Orchestrator
Manages the review conversation protocol and produces final synthesis with audit trail.

Conversation Flow:
1. Welcome + ground rules
2. IdeologicalReviewer: Opening statement  
3. StatisticalReviewer: Opening statement
4. IdeologicalReviewer: Response 
5. StatisticalReviewer: Response  
6. Final synthesis + conclusion

Produces dual audit trail: JSONL conversation log + Markdown transcript
"""

import json
import sys
import os
import redis
import logging
import time
import base64
from typing import Dict, Any, Optional, List
from litellm import completion

# Add scripts directory to path for minio_client
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'scripts'))
from minio_client import get_artifact, put_artifact, ArtifactStorageError

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Redis configuration
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = 6379
REDIS_DB = 0

class ModeratorAgentError(Exception):
    """Agent-specific exceptions"""
    pass

class ModeratorAgent:
    def __init__(self):
        self.redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
        self.conversation_log = []  # JSONL conversation record

    def process_moderation_task(self, task_id: str) -> bool:
        """Process moderation task and orchestrate review conversation"""
        try:
            logger.info(f"Processing Moderation task: {task_id}")
            
            # Get task data from Redis
            task_data = self._get_task_data(task_id)
            if not task_data:
                raise ModeratorAgentError(f"Could not retrieve task data for {task_id}")

            synthesis_hash = task_data.get('synthesis_hash')
            experiment_name = task_data.get('experiment_name', 'phase3_review_test')
            
            if not synthesis_hash:
                raise ModeratorAgentError("Missing synthesis_hash in task data")

            logger.info(f"Moderating review for experiment: {experiment_name}")
            logger.info(f"Synthesis report: {synthesis_hash}")

            # Connect to artifact store
            logger.info("Connected to artifact store at localhost:9000")

            # Retrieve synthesis report
            synthesis_bytes = get_artifact(synthesis_hash)
            synthesis_report = json.loads(synthesis_bytes.decode('utf-8'))
            
            logger.info(f"Retrieved synthesis report: {len(synthesis_bytes)} bytes")
            
            # Extract framework hashes from synthesis report for context
            framework_hashes = synthesis_report.get('framework_hashes', [])
            if not framework_hashes:
                raise ModeratorAgentError("No framework_hashes found in synthesis report - cannot provide framework context")
            
            # Retrieve frameworks for moderation context
            frameworks = []
            for i, framework_hash in enumerate(framework_hashes):
                # Strip sha256: prefix if present
                clean_hash = framework_hash[7:] if framework_hash.startswith('sha256:') else framework_hash
                framework_bytes = get_artifact(clean_hash)
                # Binary-First Principle: Frameworks as base64
                framework_content = base64.b64encode(framework_bytes).decode('utf-8')
                frameworks.append({
                    'index': i + 1,
                    'hash': clean_hash,
                    'content': framework_content
                })
                logger.info(f"Retrieved framework {i+1} for moderation context: {clean_hash[:12]}...")
            
            logger.info(f"Retrieved {len(frameworks)} frameworks for moderation context")

            # Start conversation with welcome message
            self._add_conversation_entry("moderator", "welcome", self._generate_welcome_message())

            # Create review tasks
            review_task_ids = self._create_review_tasks(synthesis_hash, experiment_name)
            logger.info(f"Created review tasks: {review_task_ids}")

            # Wait for review completion and orchestrate conversation
            conversation_successful = self._orchestrate_conversation(review_task_ids, synthesis_report, frameworks)

            if conversation_successful:
                # Generate final synthesis
                final_synthesis = self._generate_final_synthesis(synthesis_report, frameworks)
                self._add_conversation_entry("moderator", "final_synthesis", final_synthesis)

                # Create audit trail artifacts
                audit_trail_hash = self._create_audit_trail(experiment_name)
                
                # Store moderation result
                moderation_result = {
                    "task_id": task_id,
                    "experiment_name": experiment_name,
                    "synthesis_hash": synthesis_hash,
                    "conversation_log": self.conversation_log,
                    "audit_trail_hash": audit_trail_hash,
                    "model_used": "gemini-2.5-pro",
                    "moderation_timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                }
                
                result_hash = put_artifact(json.dumps(moderation_result).encode('utf-8'))
                logger.info(f"Stored moderation result: {result_hash}")

                # Mark task as completed
                completion_data = {
                    "original_task_id": task_id,
                    "result_hash": result_hash,
                    "audit_trail_hash": audit_trail_hash,
                    "status": "completed",
                    "task_type": "Moderation",
                    "model_used": "gemini-2.5-pro"
                }

                self.redis_client.xadd('tasks.done', {
                    'original_task_id': task_id,
                    'data': json.dumps(completion_data)
                })

                logger.info(f"Moderation task completed: {task_id}")
                return True
            else:
                logger.error("Conversation orchestration failed")
                return False

        except Exception as e:
            logger.error(f"Moderation task failed: {e}", exc_info=True)
            return False

    def _get_task_data(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve task data from Redis tasks stream"""
        try:
            # Get task from stream
            messages = self.redis_client.xrange('tasks', task_id, task_id)
            if not messages:
                return None
            
            _, fields = messages[0]
            task_data = json.loads(fields[b'data'])
            return task_data
            
        except Exception as e:
            logger.error(f"Failed to retrieve task data: {e}")
            return None

    def _add_conversation_entry(self, speaker: str, turn_type: str, content: str):
        """Add entry to conversation log"""
        entry = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "speaker": speaker,
            "turn_type": turn_type,
            "content": content,
            "turn_number": len(self.conversation_log) + 1
        }
        self.conversation_log.append(entry)
        logger.info(f"Added conversation entry: {speaker} - {turn_type}")

    def _generate_welcome_message(self) -> str:
        """Generate moderator welcome message and ground rules"""
        return """Welcome to the Phase 3 Constitutional Health Framework Review Session.

GROUND RULES FOR THIS ACADEMIC REVIEW:
1. **Scholarly Discourse**: Maintain rigorous academic standards while engaging in substantive critique
2. **Turn Management**: Each reviewer will provide one opening statement and one response - wait to be invited to speak
3. **Evidence-Based Argument**: Ground all critiques in specific evidence from the synthesis report
4. **Time Constraint**: This review session has a 10-minute limit for focused, productive debate
5. **Mutual Respect**: Challenge ideas rigorously while respecting the scholarly contributions of your colleague

REVIEW PARTICIPANTS:
- Ideological Reviewer: Will examine the constitutional analysis through a specific political lens
- Statistical Reviewer: Will examine the methodological rigor and framework validity

CONVERSATION PROTOCOL:
The moderator will facilitate orderly exchange of ideas to ensure both perspectives receive fair hearing and substantive engagement. Each reviewer will have the opportunity for both initial analysis and response to their colleague's perspective.

Let us begin with opening statements from each reviewer.
"""

    def _create_review_tasks(self, synthesis_hash: str, experiment_name: str) -> List[str]:
        """Create review tasks for both reviewers"""
        task_ids = []

        # Create ideological review task (progressive perspective)
        ideological_task_data = {
            'review_type': 'ideological',
            'ideology': 'progressive',  # Could be randomized or specified
            'synthesis_hash': synthesis_hash,
            'conversation_context': {},
            'experiment_name': experiment_name,
            'model': 'gemini-2.5-pro'
        }

        ideological_task_id = self.redis_client.xadd('tasks', {
            'type': 'review',
            'data': json.dumps(ideological_task_data)
        }).decode()
        task_ids.append(ideological_task_id)

        # Create statistical review task
        statistical_task_data = {
            'review_type': 'statistical',
            'synthesis_hash': synthesis_hash,
            'conversation_context': {},
            'experiment_name': experiment_name,
            'model': 'gemini-2.5-pro'
        }

        statistical_task_id = self.redis_client.xadd('tasks', {
            'type': 'review',
            'data': json.dumps(statistical_task_data)
        }).decode()
        task_ids.append(statistical_task_id)

        return task_ids

    def _orchestrate_conversation(self, review_task_ids: List[str], synthesis_report: Dict, frameworks: List[Dict]) -> bool:
        """Orchestrate the review conversation protocol"""
        try:
            # Wait for initial reviews to complete
            logger.info("Waiting for opening statements...")
            initial_reviews = self._wait_for_reviews(review_task_ids, timeout=300)
            
            if len(initial_reviews) != 2:
                logger.error(f"Expected 2 initial reviews, got {len(initial_reviews)}")
                return False

            # Add opening statements to conversation
            for review in initial_reviews:
                reviewer_type = "Ideological Reviewer" if review['review_type'] == 'ideological' else "Statistical Reviewer"
                self._add_conversation_entry(reviewer_type, "opening_statement", review['review_content'])

            # Create response tasks with conversation context
            response_task_ids = self._create_response_tasks(initial_reviews, synthesis_report, frameworks)
            
            # Wait for responses to complete
            logger.info("Waiting for response statements...")
            response_reviews = self._wait_for_reviews(response_task_ids, timeout=300)
            
            if len(response_reviews) != 2:
                logger.error(f"Expected 2 response reviews, got {len(response_reviews)}")
                return False

            # Add response statements to conversation
            for review in response_reviews:
                reviewer_type = "Ideological Reviewer" if review['review_type'] == 'ideological' else "Statistical Reviewer"
                self._add_conversation_entry(reviewer_type, "response", review['review_content'])

            logger.info("Conversation orchestration completed successfully")
            return True

        except Exception as e:
            logger.error(f"Conversation orchestration failed: {e}")
            return False

    def _wait_for_reviews(self, task_ids: List[str], timeout: int = 300) -> List[Dict]:
        """Wait for review tasks to complete and return results"""
        completed_reviews = []
        start_time = time.time()
        completed_task_ids = set()

        while len(completed_reviews) < len(task_ids) and time.time() - start_time < timeout:
            # Check for completed tasks
            try:
                done_messages = self.redis_client.xread({'tasks.done': '0-0'}, block=1000)
                if not done_messages:
                    continue

                for stream, msgs in done_messages:
                    for msg_id, fields in msgs:
                        completion_data = json.loads(fields[b'data'])
                        original_task_id = completion_data.get('original_task_id')
                        
                        if original_task_id in task_ids and original_task_id not in completed_task_ids:
                            # Retrieve the review result
                            result_hash = completion_data.get('result_hash')
                            if result_hash:
                                review_bytes = get_artifact(result_hash)
                                review_data = json.loads(review_bytes.decode('utf-8'))
                                completed_reviews.append(review_data)
                                completed_task_ids.add(original_task_id)
                                logger.info(f"Collected review from task {original_task_id}")

            except Exception as e:
                logger.error(f"Error waiting for reviews: {e}")
                continue

        if len(completed_reviews) < len(task_ids):
            logger.warning(f"Timeout waiting for reviews. Got {len(completed_reviews)}/{len(task_ids)}")

        return completed_reviews

    def _create_response_tasks(self, initial_reviews: List[Dict], synthesis_report: Dict, frameworks: List[Dict]) -> List[str]:
        """Create response tasks with conversation context"""
        task_ids = []

        # Prepare conversation context for responses
        previous_reviews = [
            {
                'reviewer_type': review['review_type'],
                'key_points': review['review_content'][:500] + "..."  # Summary for context
            }
            for review in initial_reviews
        ]

        for review in initial_reviews:
            # Create response task for the same reviewer
            if review['review_type'] == 'ideological':
                response_task_data = {
                    'review_type': 'ideological',
                    'ideology': review.get('ideology', 'progressive'),
                    'synthesis_hash': review['synthesis_hash'],
                    'conversation_context': {'previous_reviews': previous_reviews},
                    'experiment_name': review.get('experiment_name', 'phase3_review_test'),
                    'model': 'gemini-2.5-pro'
                }
            else:  # statistical
                response_task_data = {
                    'review_type': 'statistical',
                    'synthesis_hash': review['synthesis_hash'],
                    'conversation_context': {'previous_reviews': previous_reviews},
                    'experiment_name': review.get('experiment_name', 'phase3_review_test'),
                    'model': 'gemini-2.5-pro'
                }

            response_task_id = self.redis_client.xadd('tasks', {
                'type': 'review',
                'data': json.dumps(response_task_data)
            }).decode()
            task_ids.append(response_task_id)

        return task_ids

    def _generate_final_synthesis(self, synthesis_report: Dict, frameworks: List[Dict]) -> str:
        """Generate final moderated synthesis after review conversation"""
        
        # Extract conversation content for synthesis
        conversation_content = "\n\n".join([
            f"**{entry['speaker']} ({entry['turn_type']})**:\n{entry['content']}"
            for entry in self.conversation_log[1:]  # Skip welcome message
        ])

        raw_report = synthesis_report.get('raw_llm_statistical_report', str(synthesis_report))
        
        # Format frameworks for final synthesis context
        frameworks_text = "\n".join([
            f"=== FRAMEWORK {fw['index']} (base64 encoded) ===\n{fw['content']}\n"
            for fw in frameworks
        ])

        prompt = f"""You are the moderator of an academic review session. After facilitating a structured debate between an ideological reviewer and a statistical reviewer, you must now provide the final synthesis that incorporates their perspectives and produces a balanced academic conclusion.

ANALYTICAL FRAMEWORKS USED:
{frameworks_text}

ORIGINAL SYNTHESIS REPORT:
{raw_report}

REVIEW CONVERSATION:
{conversation_content}

FINAL SYNTHESIS REQUIREMENTS:
1. **Framework Context**: Reference the original analytical frameworks to ground the discussion
2. **Acknowledge Both Perspectives**: Fairly represent the key insights from both ideological and statistical reviews
3. **Reconcile Disagreements**: Address points of tension between the reviewers with scholarly balance
4. **Enhance Original Analysis**: Identify how the review process has improved understanding of the constitutional patterns
5. **Academic Conclusion**: Provide a final assessment that integrates the original analysis with reviewer insights
6. **Future Research Directions**: Suggest how future framework applications could address reviewer concerns

Your final synthesis should:
- Ground all conclusions in the original analytical frameworks provided
- Maintain scholarly objectivity while acknowledging the value of different analytical perspectives
- Demonstrate how peer review has strengthened the framework-based analysis
- Provide clear conclusions about the patterns identified using the specified analytical frameworks
- Address methodological limitations raised by the statistical reviewer about framework application
- Incorporate ideological insights about framework interpretation and constitutional analysis
- Suggest improvements for future applications of these analytical frameworks

Provide approximately 600-800 words of final synthesis that demonstrates the value of the peer review process for constitutional health analysis."""

        try:
            logger.info("Calling LLM for final moderated synthesis...")
            
            response = completion(
                model="gemini-2.5-pro",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            
            final_synthesis = response.choices[0].message.content.strip()
            logger.info(f"Generated final synthesis: {len(final_synthesis)} characters")
            
            return final_synthesis
            
        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            raise ModeratorAgentError(f"Failed to generate final synthesis: {e}")

    def _create_audit_trail(self, experiment_name: str) -> str:
        """Create dual audit trail: JSONL + Markdown"""
        
        # Create JSONL conversation log
        jsonl_content = "\n".join([
            json.dumps(entry) for entry in self.conversation_log
        ])

        # Create Markdown transcript
        markdown_content = f"""# Constitutional Health Framework Review Session
## Experiment: {experiment_name}
## Date: {time.strftime("%Y-%m-%d %H:%M:%S")}

---

"""

        for entry in self.conversation_log:
            markdown_content += f"### {entry['speaker']} - {entry['turn_type'].replace('_', ' ').title()}\n"
            markdown_content += f"**Time**: {entry['timestamp']}\n\n"
            markdown_content += f"{entry['content']}\n\n---\n\n"

        # Store both formats
        jsonl_hash = put_artifact(jsonl_content.encode('utf-8'))
        markdown_hash = put_artifact(markdown_content.encode('utf-8'))

        # Create combined audit trail metadata
        audit_trail_metadata = {
            "experiment_name": experiment_name,
            "conversation_jsonl_hash": jsonl_hash,
            "conversation_markdown_hash": markdown_hash,
            "total_turns": len(self.conversation_log),
            "participants": ["moderator", "ideological_reviewer", "statistical_reviewer"],
            "created_timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        }

        audit_trail_hash = put_artifact(json.dumps(audit_trail_metadata).encode('utf-8'))
        
        logger.info(f"Created audit trail: JSONL={jsonl_hash}, Markdown={markdown_hash}, Metadata={audit_trail_hash}")
        return audit_trail_hash

def main():
    """ModeratorAgent entry point"""
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <task_id>")
        sys.exit(1)
    
    task_id = sys.argv[1]
    agent = ModeratorAgent()
    
    success = agent.process_moderation_task(task_id)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main() 