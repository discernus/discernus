#!/usr/bin/env python3
"""
Model Health Verification Tool
==============================

A developer utility to perform a quick health check on all models defined in the
Model Registry (`discernus/gateway/models.yaml`).

This script iterates through each model, performs a simple, low-cost API call,
and reports on its accessibility and configuration status. This helps diagnose
issues with API keys, model names, or provider access before running
a full experiment.

USAGE:
    python3 -m discernus.dev_tools.verify_model_health
"""

# Copyright (C) 2025  Discernus Team

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import asyncio
import sys
from pathlib import Path
import yaml
import litellm
# Disable LiteLLM verbose output to reduce terminal clutter
litellm.set_verbose = False
from rich.console import Console
from rich.table import Table

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# To see verbose provider-specific errors
# litellm.set_verbose = True

async def check_model(model_name: str, console: Console):
    """Performs a simple completion call to test a single model."""
    try:
        # A simple, low-cost prompt
        messages = [{"role": "user", "content": "Hello, are you there? Respond with just 'yes'."}]
        
        # Add safety settings specifically for Vertex AI models
        # and REMOVE max_tokens which triggers safety filters
        extra_kwargs = {}
        if model_name.startswith("vertex_ai"):
            extra_kwargs['safety_settings'] = [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
            ]
            # DO NOT pass max_tokens for vertex_ai models - it triggers safety filters
        else:
            # For non-vertex_ai models, we can use max_tokens
            extra_kwargs['max_tokens'] = 5

        # Make the API call
        response = await litellm.acompletion(
            model=model_name,
            messages=messages,
            temperature=0.0,
            **extra_kwargs
        )
        
        # Check if the response is valid (basic check)
        if response.choices[0].message.content:
            return {"model": model_name, "status": "✅ SUCCESS", "error": ""}
        else:
            return {"model": model_name, "status": "❌ FAILED", "error": "Empty response received."}
            
    except Exception as e:
        # Capture any exception from litellm
        error_message = str(e).split('\n')[0] # Get the core error message
        return {"model": model_name, "status": "❌ FAILED", "error": error_message}

async def main():
    """Main function to load models and run checks."""
    console = Console()
    console.print("[bold cyan]Discernus Model Registry Health Check[/bold cyan]")
    console.print("="*40)

    # Load the model registry
    models_yaml_path = project_root / "discernus" / "gateway" / "models.yaml"
    try:
        with open(models_yaml_path, 'r') as f:
            model_registry = yaml.safe_load(f)
        model_names = list(model_registry.get('models', {}).keys())
        console.print(f"🔍 Found {len(model_names)} models in the registry.")
    except FileNotFoundError:
        console.print(f"[bold red]❌ Error: Model registry not found at {models_yaml_path}[/bold red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]❌ Error: Failed to parse model registry: {e}[/bold red]")
        sys.exit(1)

    # Create a table for the results
    table = Table(title="Model Health Status")
    table.add_column("Model Name", justify="left", style="cyan", no_wrap=True)
    table.add_column("Status", justify="center", style="magenta")
    table.add_column("Details", justify="left", style="red")

    # Run checks concurrently
    tasks = [check_model(model, console) for model in model_names]
    results = await asyncio.gather(*tasks)
    
    success_count = 0
    # Populate the table
    for result in sorted(results, key=lambda x: x['model']):
        if result['status'] == "✅ SUCCESS":
            table.add_row(result['model'], result['status'], "")
            success_count += 1
        else:
            table.add_row(result['model'], result['status'], result['error'])

    console.print(table)
    
    # Print summary
    total_models = len(model_names)
    failure_count = total_models - success_count
    console.print("\n[bold]Summary:[/bold]")
    console.print(f"  [green]✅ Successful Checks: {success_count}[/green]")
    console.print(f"  [red]❌ Failed Checks: {failure_count}[/red]")
    
    if failure_count > 0:
        console.print("\n[bold yellow]💡 Action Required:[/bold yellow]")
        console.print("   - Verify API keys and provider configurations in your environment.")
        console.print("   - Check model names and availability in the `models.yaml` file.")
        console.print("   - For Vertex AI, ensure the model is available in your configured GCP region.")


if __name__ == "__main__":
    asyncio.run(main()) 