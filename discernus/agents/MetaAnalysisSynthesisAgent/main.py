#!/usr/bin/env python3
"""
MetaAnalysisSynthesisAgent - Deterministic Statistical Aggregation Agent
==================================================================

THIN Principle: LLM handles statistical reasoning and mathematical computation.
Software provides minimal Redis/MinIO coordination only.

Architecture: Layer 2 agent in deterministic 3-layer synthesis pipeline
- Input: Structured data from multiple AnalyseBatch results
- Process: Deterministic mathematical aggregation
- Output: Statistical report ONLY (no qualitative narrative)
- Model: Gemini 2.5 Pro for reliable statistical computations
"""

import json
import os
import sys
import yaml
from pathlib import Path
from litellm import completion

# This agent synthesizes the outputs of multiple BatchAnalysisAgent runs using an LLM.

def load_prompt_template():
    prompt_path = Path(__file__).parent / "prompt.yaml"
    with open(prompt_path, 'r') as f:
        data = yaml.safe_load(f)
    return data['template']

def format_batch_reports_for_prompt(artifacts):
    """Formats the raw analysis_results from batch artifacts for the synthesis prompt."""
    report_strings = []
    for i, artifact in enumerate(artifacts):
        report_content = artifact.get('analysis_results', 'No content found.')
        report_strings.append(f"--- BATCH {i+1} REPORT ---\n{report_content}\n")
    return "\n".join(report_strings)

def main():
    if not sys.stdin.isatty():
        try:
            task_input = json.load(sys.stdin)
        except json.JSONDecodeError:
            print(json.dumps({"error": "Invalid JSON input from stdin"}), file=sys.stderr)
            sys.exit(1)
    else:
        if len(sys.argv) < 3:
            print(json.dumps({"error": "Usage: <run_id> <artifact_path_1> ..."}), file=sys.stderr)
            sys.exit(1)
        run_id = sys.argv[1]
        analysis_artifact_paths = sys.argv[2:]
        task_input = {"run_id": run_id, "analysis_artifacts": analysis_artifact_paths}

    run_id = task_input.get("run_id")
    analysis_artifact_paths = task_input.get("analysis_artifacts", [])

    if not run_id or not analysis_artifact_paths:
        print(json.dumps({"error": "Missing run_id or analysis_artifacts"}), file=sys.stderr)
        sys.exit(1)

    batch_artifacts = []
    for path in analysis_artifact_paths:
        try:
            with open(path, 'r') as f:
                batch_artifacts.append(json.load(f))
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Skipping artifact {path}: {e}", file=sys.stderr)

    if not batch_artifacts:
        print(json.dumps({"error": "No valid batch artifacts found to process."}), file=sys.stderr)
        sys.exit(1)

    # For now, a placeholder for framework summary. In a real scenario, this would be passed in.
    frameworks_summary = "A set of analytical frameworks focused on constitutional health."

    prompt_template = load_prompt_template()
    prompt = prompt_template.format(
        num_batches=len(batch_artifacts),
        frameworks_summary=frameworks_summary,
        batch_reports=format_batch_reports_for_prompt(batch_artifacts)
    )

    try:
        response = completion(
            model="gemini-2.5-pro",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0 # Deterministic synthesis
        )
        synthesis_content = response.choices[0].message.content
    except Exception as e:
        print(json.dumps({"error": f"LLM completion failed: {e}"}), file=sys.stderr)
        sys.exit(1)

    output_filename = f"synthesis_{run_id}.json"
    output_path = Path(f"synthesis/{output_filename}")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w") as f:
        # The prompt asks for JSON, so we trust but verify.
        try:
            parsed_synthesis = json.loads(synthesis_content)
            json.dump(parsed_synthesis, f, indent=2)
        except json.JSONDecodeError:
            print("Warning: LLM output was not valid JSON. Saving raw text.", file=sys.stderr)
            f.write(synthesis_content)

    print(json.dumps({"status": "success", "artifact_name": output_filename, "artifact_path": str(output_path)}))


if __name__ == "__main__":
    main()