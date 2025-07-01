from typing import Dict, Any


def create_prompt_from_experiment(experiment_def: Dict[str, Any], text_to_analyze: str) -> str:
    """
    Constructs a detailed LLM prompt from a self-contained experiment definition file,
    including a dynamically generated framework summary.
    """
    guidance = experiment_def.get("prompt_guidance", {})
    framework = experiment_def.get("framework", {})
    
    # CRITICAL FIX: Get detailed prompts from framework section (Framework Spec v3.2)
    detailed_prompts = framework.get("detailed_prompts", {})

    # Build the dynamic framework description for the prompt
    framework_description_parts = [framework.get("description", "")]
    
    # Support Framework Specification v3.2 format
    components = framework.get("components", {})
    axes = framework.get("axes", {})
    
    if components and axes:
        # Framework Specification v3.2: Build from components + axes
        for axis_name, axis_details in axes.items():
            axis_desc = axis_details.get("description", axis_name.replace("_", " vs "))
            framework_description_parts.append(f"\n- **{axis_name.replace('_', ' ')}**: {axis_desc}")
            
            # Get anchor components referenced by this axis
            anchor_ids = axis_details.get("anchor_ids", [])
            for anchor_id in anchor_ids:
                if anchor_id in components:
                    component = components[anchor_id]
                    if component.get("type") == "anchor":
                        anchor_name = component.get("component_id", anchor_id).replace("_", " ").title()
                        framework_description_parts.append(f"  - **{anchor_name}**: {component.get('description', '')}")
                        if component.get("language_cues"):
                            cues = ", ".join(component["language_cues"][:5])  # Limit for readability
                            framework_description_parts.append(f"    *Cues: {cues}...*")
    else:
        # Legacy format: Original logic
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
        framework.get("expert_role", "Analyze the following text."),
        framework.get("methodological_approach", "Analyze the text based on the following framework:"),
        "--- FRAMEWORK DEFINITION ---",
        framework_summary,
        "--------------------------",
        detailed_prompts.get("dimensional_analysis_guidance", ""),
        detailed_prompts.get("scoring_methodology", ""),
        f"--- TEXT TO ANALYZE ---\n{text_to_analyze}\n-----------------------",
        detailed_prompts.get("json_output_format", "Provide your response in JSON format."),
    ]

    return "\n\n".join(part for part in prompt_parts if part)
