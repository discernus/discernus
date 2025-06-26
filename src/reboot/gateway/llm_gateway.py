from src.reboot.gateway.reboot_litellm_client import LiteLLMClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Instantiate a single, reusable client instance
# This is more efficient than creating a new client for every request.
llm_client = LiteLLMClient()

async def get_llm_analysis(text: str, framework: str, model: str) -> dict:
    """
    A simple wrapper to call the existing LiteLLMClient.
    
    This function serves as the clean entry point for the new reboot architecture,
    hiding the implementation details of the underlying client.
    """
    # For now, we are not handling the 'cost' return value, but we can add it later.
    analysis_result, _ = llm_client.analyze_text(
        text=text,
        framework=framework,
        model_name=model
    )
    return analysis_result 