#!/usr/bin/env python3
"""
Enable Automatic Cost Tracking for Discernus
============================================

This script shows how to enable LiteLLM cost tracking in the audit logs.
The infrastructure is already there - we just need to use it!
"""

def show_current_cost_infrastructure():
    """Show what cost tracking infrastructure already exists."""
    
    print("🔍 Current Cost Tracking Infrastructure:")
    print()
    print("1. LLM Gateway (llm_gateway_enhanced.py) captures:")
    print("   - response_cost_usd from LiteLLM completion_cost()")
    print("   - prompt_tokens, completion_tokens, total_tokens")
    print("   - Returns in metadata['usage'] dictionary")
    print()
    print("2. Audit Logger (audit_logger.py) provides:")
    print("   - log_llm_interaction() method for cost logging")
    print("   - costs.jsonl file for cost data")
    print("   - llm_interactions.jsonl for detailed interaction logs")
    print()
    print("3. Missing piece: Agents don't call audit logging methods")
    print()

def show_cost_logging_example():
    """Show how to add cost logging to an agent."""
    
    print("💡 How to Enable Cost Logging in Agents:")
    print()
    print("Add this after LLM calls in agents:")
    print("""
# After: response = self.gateway.execute_call(...)
if isinstance(response, tuple):
    content, metadata = response
    
    # Log cost data from LiteLLM
    if metadata and 'usage' in metadata:
        usage_data = metadata['usage']
        self.audit.log_llm_interaction(
            model="vertex_ai/gemini-2.5-flash",
            prompt=prompt,
            response=content,
            agent_name=self.agent_name,
            interaction_type="analysis",
            metadata={
                "prompt_tokens": usage_data.get('prompt_tokens', 0),
                "completion_tokens": usage_data.get('completion_tokens', 0), 
                "total_tokens": usage_data.get('total_tokens', 0),
                "response_cost_usd": usage_data.get('response_cost_usd', 0.0)
            }
        )
""")

def show_cost_analysis_query():
    """Show how to query cost data from logs."""
    
    print("📊 How to Analyze Costs from Logs:")
    print()
    print("1. Check LLM interaction logs:")
    print("   cat logs/llm_interactions.jsonl | jq '.metadata.response_cost_usd'")
    print()
    print("2. Sum total costs for an experiment:")
    print("   cat logs/llm_interactions.jsonl | jq -s 'map(.metadata.response_cost_usd) | add'")
    print()
    print("3. Cost breakdown by model:")
    print("   cat logs/llm_interactions.jsonl | jq -r '[.model, .metadata.response_cost_usd] | @csv'")
    print()
    print("4. Token usage analysis:")
    print("   cat logs/llm_interactions.jsonl | jq '.metadata | {tokens: .total_tokens, cost: .response_cost_usd}'")
    print()

def main():
    """Show complete cost tracking setup."""
    
    print("🎯 Discernus Cost Tracking Setup")
    print("=" * 50)
    print()
    
    show_current_cost_infrastructure()
    show_cost_logging_example()
    show_cost_analysis_query()
    
    print("🚀 Next Steps:")
    print("1. Add cost logging to agents (see example above)")
    print("2. Run experiments to generate cost data")
    print("3. Use jq queries to analyze costs from logs/llm_interactions.jsonl")
    print("4. Update cost guide with real data from logs!")
    print()
    print("💰 This will give you exact per-document costs instead of estimates!")

if __name__ == "__main__":
    main()

