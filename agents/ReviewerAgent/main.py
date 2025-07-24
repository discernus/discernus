#!/usr/bin/env python3
"""
ReviewerAgent - Phase 3 Quality Assurance Agent
Provides adversarial critique of corpus synthesis reports from specific analytical perspectives.

Supports two review modes:
1. Ideological Review: Analyzes through Progressive/Conservative/Populist lens
2. Statistical Review: Examines methodology, framework fit, statistical rigor

Follows THIN architecture: LLM intelligence, minimal software coordination.
"""

import json
import sys
import os
import redis
import logging
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

class ReviewerAgentError(Exception):
    """Agent-specific exceptions"""
    pass

class ReviewerAgent:
    def __init__(self):
        self.redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

    def process_review_task(self, task_id: str) -> bool:
        """Process a review task and generate critical analysis"""
        try:
            logger.info(f"Processing Review task: {task_id}")
            
            # Get task data from Redis
            task_data = self._get_task_data(task_id)
            if not task_data:
                raise ReviewerAgentError(f"Could not retrieve task data for {task_id}")

            review_type = task_data.get('review_type', 'ideological')  # ideological or statistical
            ideology = task_data.get('ideology', 'progressive')  # progressive, conservative, populist, centrist
            synthesis_hash = task_data.get('synthesis_hash')
            conversation_context = task_data.get('conversation_context', {})  # Previous review if responding
            
            if not synthesis_hash:
                raise ReviewerAgentError("Missing synthesis_hash in task data")

            logger.info(f"Review type: {review_type}, Ideology: {ideology}")
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
                raise ReviewerAgentError("No framework_hashes found in synthesis report - cannot provide framework context")
            
            # Retrieve frameworks for review context
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
                logger.info(f"Retrieved framework {i+1} for review context: {clean_hash[:12]}...")
            
            logger.info(f"Retrieved {len(frameworks)} frameworks for review context")

            # Generate review based on type
            if review_type == 'ideological':
                review_content = self._generate_ideological_review(
                    synthesis_report, frameworks, ideology, conversation_context
                )
            elif review_type == 'statistical':
                review_content = self._generate_statistical_review(
                    synthesis_report, frameworks, conversation_context
                )
            else:
                raise ReviewerAgentError(f"Unknown review type: {review_type}")

            # Store review result
            review_result = {
                "task_id": task_id,
                "review_type": review_type,
                "ideology": ideology if review_type == 'ideological' else None,
                "synthesis_hash": synthesis_hash,
                "review_content": review_content,
                "model_used": "gemini-2.5-pro",
                "review_timestamp": "2025-07-23T21:00:00.000000Z"
            }
            
            result_hash = put_artifact(json.dumps(review_result).encode('utf-8'))
            logger.info(f"Stored review result: {result_hash} ({len(json.dumps(review_result))} bytes)")

            # Mark task as completed
            completion_data = {
                "original_task_id": task_id,
                "result_hash": result_hash,
                "status": "completed",
                "task_type": "Review",
                "model_used": "gemini-2.5-flash"
            }

            self.redis_client.xadd('tasks.done', {
                'original_task_id': task_id,
                'data': json.dumps(completion_data)
            })

            logger.info(f"Review task completed: {task_id}")
            return True

        except Exception as e:
            logger.error(f"Review task failed: {e}", exc_info=True)
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

    def _generate_ideological_review(self, synthesis_report: Dict, frameworks: List[Dict], ideology: str, conversation_context: Dict) -> str:
        """Generate ideological critique of synthesis report"""
        
        # Get the raw statistical report content
        raw_report = synthesis_report.get('raw_llm_statistical_report', '')
        if not raw_report:
            raw_report = str(synthesis_report)

        # Determine if this is an opening statement or response
        is_response = bool(conversation_context.get('previous_reviews'))
        turn_type = "response" if is_response else "opening_statement"
        
        context_prompt = ""
        if is_response:
            context_prompt = f"""
CONVERSATION CONTEXT: You are responding to a previous reviewer's analysis. 
Previous review key points: {conversation_context.get('previous_reviews', [])}
Your task is to provide a counter-perspective that addresses their points while maintaining your ideological viewpoint.
"""

        ideology_perspectives = {
            'progressive': """
You are reviewing this analysis from a PROGRESSIVE CONSTITUTIONAL perspective. Focus on:
- Whether the analysis adequately captures progressive constitutional priorities (voting rights, economic justice, institutional reform)
- Whether conservative constitutional rhetoric is properly contextualized within broader power structures
- Whether the framework captures threats to democratic participation and representation
- Whether the analysis identifies constitutional barriers to social and economic justice
- Whether populist constitutional critique is distinguished from progressive constitutional reform
""",
            'conservative': """
You are reviewing this analysis from a CONSERVATIVE CONSTITUTIONAL perspective. Focus on:
- Whether the analysis adequately captures conservative constitutional priorities (institutional respect, procedural legitimacy, constitutional stability)
- Whether progressive constitutional rhetoric is properly distinguished from constitutional activism  
- Whether the framework captures threats to constitutional tradition and institutional authority
- Whether the analysis identifies constitutional overreach and judicial activism
- Whether populist constitutional critique is distinguished from principled conservative constitutionalism
""",
            'populist': """
You are reviewing this analysis from a POPULIST CONSTITUTIONAL perspective. Focus on:
- Whether the analysis adequately captures populist constitutional priorities (anti-establishment sentiment, democratic representation vs elite capture)
- Whether establishment constitutional rhetoric (both progressive and conservative) is properly understood as maintaining existing power structures
- Whether the framework captures the constitutional crisis of institutional capture by special interests
- Whether the analysis identifies the gap between constitutional theory and constitutional reality for ordinary Americans
""",
            'centrist': """
You are reviewing this analysis from a CENTRIST CONSTITUTIONAL perspective. Focus on:
- Whether the analysis adequately balances different constitutional perspectives without ideological bias
- Whether the framework captures pragmatic constitutional solutions that transcend partisan divisions
- Whether extreme constitutional positions (both left and right) are properly identified as threats to constitutional stability
- Whether the analysis identifies opportunities for constitutional reform that builds broad consensus
"""
        }

        perspective_prompt = ideology_perspectives.get(ideology, ideology_perspectives['progressive'])
        
        # Format frameworks for review context
        frameworks_text = "\n".join([
            f"=== FRAMEWORK {fw['index']} (base64 encoded) ===\n{fw['content']}\n"
            for fw in frameworks
        ])

        prompt = f"""You are an expert constitutional scholar providing {turn_type} critical review of a corpus synthesis report from a {ideology.upper()} constitutional perspective.

{context_prompt}

{perspective_prompt}

ANALYTICAL FRAMEWORKS USED:
{frameworks_text}

SYNTHESIS REPORT TO REVIEW:
{raw_report}

CRITICAL REVIEW REQUIREMENTS:
1. Provide sharp, substantive critique from your ideological perspective
2. Identify specific analytical gaps or biases in the constitutional assessment
3. Challenge assumptions about constitutional health/pathology patterns
4. Question whether the framework adequately captures your constitutional priorities
5. Raise concerns about methodology, interpretation, or conclusions that reflect ideological blind spots

Your review should be rigorous academic critique that:
- Points to specific evidence in the report
- Challenges the analysis from your constitutional perspective  
- Identifies what the analysis missed or misunderstood
- Suggests alternative interpretations of the constitutional patterns
- Maintains scholarly tone while making strong critical points

Provide approximately 400-600 words of substantive constitutional critique."""

        try:
            logger.info(f"Calling LLM (gemini-2.5-pro) for {ideology} ideological review...")
            
            response = completion(
                model="gemini-2.5-pro",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            
            review_content = response.choices[0].message.content.strip()
            logger.info(f"Generated {ideology} ideological review: {len(review_content)} characters")
            
            return review_content
            
        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            raise ReviewerAgentError(f"Failed to generate ideological review: {e}")

    def _generate_statistical_review(self, synthesis_report: Dict, frameworks: List[Dict], conversation_context: Dict) -> str:
        """Generate statistical/methodological critique of synthesis report"""
        
        # Get the raw statistical report content  
        raw_report = synthesis_report.get('raw_llm_statistical_report', '')
        batch_hashes = synthesis_report.get('batch_result_hashes', [])
        metadata = synthesis_report.get('aggregation_metadata', {})
        
        if not raw_report:
            raw_report = str(synthesis_report)

        # Determine if this is an opening statement or response
        is_response = bool(conversation_context.get('previous_reviews'))
        turn_type = "response" if is_response else "opening_statement"
        
        context_prompt = ""
        if is_response:
            context_prompt = f"""
CONVERSATION CONTEXT: You are responding to a previous reviewer's ideological analysis.
Previous review key points: {conversation_context.get('previous_reviews', [])}
Your task is to provide methodological critique that addresses their ideological concerns from a statistical rigor perspective.
"""

        # Format frameworks for review context
        frameworks_text = "\n".join([
            f"=== FRAMEWORK {fw['index']} (base64 encoded) ===\n{fw['content']}\n"
            for fw in frameworks
        ])

        prompt = f"""You are an expert quantitative researcher providing {turn_type} critical review of a corpus synthesis report from a STATISTICAL METHODOLOGY perspective.

{context_prompt}

You specialize in:
- Framework validation and construct validity
- Statistical significance and effect size analysis  
- Methodological rigor and replication concerns
- Measurement reliability and validity assessment
- Research design and analytical approach evaluation

ANALYTICAL FRAMEWORKS USED:
{frameworks_text}

SYNTHESIS REPORT TO REVIEW:
{raw_report}

METADATA:
- Number of batches: {len(batch_hashes)}
- Analysis metadata: {metadata}

STATISTICAL REVIEW REQUIREMENTS:
1. Evaluate the framework's construct validity for the analyzed content
2. Assess whether the statistical patterns reported are methodologically sound
3. Identify potential confounding variables or analytical limitations
4. Question the reliability and validity of the measurement approach
5. Examine whether conclusions are supported by the statistical evidence

Your review should focus on:
- Framework fit: Does CHF adequately capture the constitutional patterns in these texts?
- Statistical rigor: Are the quantitative findings reliable and valid?
- Methodological concerns: What are the limitations of this analytical approach?
- Replication issues: Would this analysis produce consistent results across runs?
- Measurement validity: Do the scores accurately reflect constitutional health/pathology?

Provide approximately 400-600 words of substantive methodological critique that challenges the statistical foundations and analytical approach."""

        try:
            logger.info("Calling LLM (gemini-2.5-pro) for statistical review...")
            
            response = completion(
                model="gemini-2.5-pro", 
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            
            review_content = response.choices[0].message.content.strip()
            logger.info(f"Generated statistical review: {len(review_content)} characters")
            
            return review_content
            
        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            raise ReviewerAgentError(f"Failed to generate statistical review: {e}")

def main():
    """ReviewerAgent entry point"""
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <task_id>")
        sys.exit(1)
    
    task_id = sys.argv[1]
    agent = ReviewerAgent()
    
    success = agent.process_review_task(task_id)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main() 