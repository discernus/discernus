"""
Generate a multi-model comparison visualization of moral gravity analyses.
"""

from moral_gravity_map import load_analysis_data, generate_multi_visualization
from pathlib import Path

# Define the model groups and their JSON files
REASONING_LLMS = [
    "model_output/2025_05_20_230558_claude_3.7_sonnet_thinking_jefferson_first_inaugural_address_analyzed_by_claude_3_7_sonnet_thinking_2025_05_20/jefferson_first_inaugural_address_analyzed_by_claude_3_7_sonnet_thinking_2025_05_20_claude_3.7_sonnet_thinking.json",
    "model_output/2025_05_20_230215_perplexity_r1_1776_jefferson_first_inaugural_address_analyzed_by_perplexity_r1_1776_2025_05_20/jefferson_first_inaugural_address_analyzed_by_perplexity_r1_1776_2025_05_20_perplexity_r1_1776.json",
    "model_output/2025_05_20_224124_openai_o4-mini_first_inaugural_address_analysis_2025_05_20/first_inaugural_address_analysis_2025_05_20_openai_o4-mini.json"
]

STANDARD_LLMS = [
    "model_output/2025_05_20_224537_perplexity_sonar_thomas_jefferson_first_inaugural_address_analysis_2025-05-20/thomas_jefferson_first_inaugural_address_analysis_2025-05-20_perplexity_sonar.json",
    "model_output/2025_05_20_225053_claude_3.7_sonnet_jefferson_first_inaugural_analysis_2025/jefferson_first_inaugural_analysis_2025_claude_3.7_sonnet.json",
    "model_output/2025_05_20_225253_openai_gpt-4.1_jefferson_first_inaugural_address_analysis_2025_05_20/jefferson_first_inaugural_address_analysis_2025_05_20_openai_gpt-4.1.json",
    "model_output/2025_05_20_225616_gemini_2.5_pro_thomas_jefferson_first_inaugural_address_analysis_2025_05_20/thomas_jefferson_first_inaugural_address_analysis_2025_05_20_gemini_2.5_pro.json",
    "model_output/2025_05_20_225816_grok_3_beta_jefferson_first_inaugural_address_analyzed_by_grok_3_beta_2025_05_20/jefferson_first_inaugural_address_analyzed_by_grok_3_beta_2025_05_20_grok_3_beta.json",
    "model_output/2025_05_20_231506_le_chat_jefferson_first_inaugural_address_analyzed_by_le_chat_2025_05_20/jefferson_first_inaugural_address_analyzed_by_le_chat_2025_05_20_le_chat.json"
]

def main():
    # Load all analyses
    reasoning_analyses = []
    standard_analyses = []
    
    print("Loading Reasoning LLM analyses...")
    for file_path in REASONING_LLMS:
        try:
            data = load_analysis_data(file_path)
            reasoning_analyses.append(data)
            print(f"✓ Loaded {data['metadata']['model_name']}")
        except Exception as e:
            print(f"✗ Error loading {file_path}: {e}")
    
    print("\nLoading Standard LLM analyses...")
    for file_path in STANDARD_LLMS:
        try:
            data = load_analysis_data(file_path)
            standard_analyses.append(data)
            print(f"✓ Loaded {data['metadata']['model_name']}")
        except Exception as e:
            print(f"✗ Error loading {file_path}: {e}")
    
    # Generate comparison visualizations
    print("\nGenerating visualizations...")
    
    if reasoning_analyses:
        print("\nGenerating Reasoning LLMs comparison...")
        generate_multi_visualization(reasoning_analyses, "reasoning_llms_comparison")
    
    if standard_analyses:
        print("\nGenerating Standard LLMs comparison...")
        generate_multi_visualization(standard_analyses, "standard_llms_comparison")
    
    if reasoning_analyses and standard_analyses:
        print("\nGenerating All Models comparison...")
        generate_multi_visualization(reasoning_analyses + standard_analyses, "all_models_comparison")

if __name__ == "__main__":
    main() 