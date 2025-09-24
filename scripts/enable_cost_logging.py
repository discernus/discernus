#!/usr/bin/env python3
"""
Enable Automatic Cost Logging for Discernus Agents
==================================================

This script adds LiteLLM cost tracking to all agent LLM interactions.
The system already captures cost data from LiteLLM but doesn't log it to audit.
"""

import os
import re
from pathlib import Path

def add_cost_logging_to_agent(agent_file: Path):
    """Add cost logging to an agent file."""
    
    with open(agent_file, 'r') as f:
        content = f.read()
    
    # Pattern to find LLM calls that return metadata
    llm_call_pattern = r'(\s+)(response = self\.gateway\.execute_call\(\s*\n\s*model="[^"]+",\s*\n\s*prompt=prompt\s*\n\s*\)\s*\n\s*)\n\s*if isinstance\(response, tuple\):\s*\n\s*content, metadata = response\s*\n\s*else:\s*\n\s*content = response\.get\(\'content\', \'\'\)\s*\n\s*metadata = response\.get\(\'metadata\', \{\}\)'
    
    # Replacement with cost logging
    cost_logging_replacement = r'\1\2\n\1\n\1# Log LLM interaction with cost data\n\1if metadata and \'usage\' in metadata:\n\1    usage_data = metadata[\'usage\']\n\1    self.audit.log_llm_interaction(\n\1        model="vertex_ai/gemini-2.5-flash-lite",\n\1        prompt=prompt,\n\1        response=content,\n\1        agent_name=self.agent_name,\n\1        interaction_type="analysis_step",\n\1        metadata={\n\1            "prompt_tokens": usage_data.get(\'prompt_tokens\', 0),\n\1            "completion_tokens": usage_data.get(\'completion_tokens\', 0),\n\1            "total_tokens": usage_data.get(\'total_tokens\', 0),\n\1            "response_cost_usd": usage_data.get(\'response_cost_usd\', 0.0),\n\1            "step": "analysis_step"\n\1        }\n\1    )\n\1\n\1if isinstance(response, tuple):\n\1    content, metadata = response\n\1else:\n\1    content = response.get(\'content\', \'\')\n\1    metadata = response.get(\'metadata\', {})'
    
    # Apply the replacement
    new_content = re.sub(llm_call_pattern, cost_logging_replacement, content, flags=re.MULTILINE | re.DOTALL)
    
    if new_content != content:
        with open(agent_file, 'w') as f:
            f.write(new_content)
        print(f"✅ Added cost logging to {agent_file}")
        return True
    else:
        print(f"⚠️  No LLM calls found in {agent_file}")
        return False

def main():
    """Enable cost logging for all agents."""
    
    # Find all agent files
    agents_dir = Path("discernus/agents")
    agent_files = []
    
    for agent_dir in agents_dir.iterdir():
        if agent_dir.is_dir() and not agent_dir.name.startswith('_'):
            for py_file in agent_dir.glob("*.py"):
                if not py_file.name.startswith('_'):
                    agent_files.append(py_file)
    
    print(f"Found {len(agent_files)} agent files to process...")
    
    updated_count = 0
    for agent_file in agent_files:
        try:
            if add_cost_logging_to_agent(agent_file):
                updated_count += 1
        except Exception as e:
            print(f"❌ Error processing {agent_file}: {e}")
    
    print(f"\n✅ Updated {updated_count} agent files with cost logging")
    print("\nNow all LLM interactions will be logged with:")
    print("- Token usage (prompt_tokens, completion_tokens, total_tokens)")
    print("- Cost data (response_cost_usd)")
    print("- Model and interaction details")
    print("\nCheck logs/llm_interactions.jsonl for cost data!")

if __name__ == "__main__":
    main()

