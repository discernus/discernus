from typing import Dict, Any

def create_prompt_from_experiment(experiment_def: Dict[str, Any], text_to_analyze: str) -> str:
    """
    Constructs a detailed LLM prompt from a self-contained experiment definition file.
    """
    guidance = experiment_def.get("prompt_guidance", {})
    
    prompt_parts = [
        guidance.get("role_definition", "Analyze the following text."),
        guidance.get("scoring_requirements", ""),
        guidance.get("analysis_methodology", ""),
        f"TEXT TO ANALYZE:\n---\n{text_to_analyze}\n---",
        guidance.get("json_format_instructions", "Provide your response in JSON format.")
    ]
    
    return "\n\n".join(part for part in prompt_parts if part) 