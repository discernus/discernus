from typing import Dict, Any


def create_prompt_from_experiment(experiment_def: Dict[str, Any], text_to_analyze: str) -> str:
    """
    Constructs a detailed LLM prompt from a self-contained experiment definition file,
    including a dynamically generated framework summary.
    """
    guidance = experiment_def.get("prompt_guidance", {})
    framework = experiment_def.get("framework", {})

    # Build the dynamic framework description for the prompt
    framework_description_parts = [framework.get("description", "")]
    axes = framework.get("axes", {})
    for axis_name, axis_details in axes.items():
        integrative = axis_details.get("integrative", {})

        # Add axis description, cleaned up for presentation
        axis_desc = axis_details.get("description", axis_name.replace("_", " vs "))
        framework_description_parts.append(f"\n- **{axis_name.replace('_', ' ')}**: {axis_desc}")

        # Add integrative anchor description
        if integrative.get("name"):
            framework_description_parts.append(f"  - **{integrative['name']}**: {integrative.get('description', '')}")
            if integrative.get("language_cues"):
                cues = ", ".join(integrative["language_cues"])
                framework_description_parts.append(f"    *Cues: {cues}*")

    framework_summary = "\n".join(framework_description_parts)

    prompt_parts = [
        guidance.get("role_definition", "Analyze the following text."),
        guidance.get("framework_summary_instructions", "Analyze the text based on the following framework:"),
        "--- FRAMEWORK DEFINITION ---",
        framework_summary,
        "--------------------------",
        guidance.get("analysis_methodology", ""),
        guidance.get("scoring_requirements", ""),
        f"--- TEXT TO ANALYZE ---\n{text_to_analyze}\n-----------------------",
        guidance.get("json_format_instructions", "Provide your response in JSON format."),
    ]

    return "\n\n".join(part for part in prompt_parts if part)
