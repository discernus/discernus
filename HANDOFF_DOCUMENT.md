# Handoff Document: Debugging the CSV Synthesis Pipeline

**Date**: July 28, 2025  
**Author**: Gemini Agent

## 1. Summary of Work Completed

The primary objective was to implement the Embedded CSV Architecture outlined in the `SYNTHESIS_SCALABILITY_ARCHITECTURE.md` document. This involved modifying the core pipeline to generate, persist, and synthesize intermediate CSV artifacts.

The following files were modified to achieve this:

*   **`discernus/core/thin_orchestrator.py`**:
    *   Modified to manage the state of two new intermediate artifacts: `scores.csv` and `evidence.csv`.
    *   The `_execute_analysis_sequentially` loop was updated to pass the current hash of these CSV artifacts to the `EnhancedAnalysisAgent` for each document and to receive the updated hash back.
    *   The final hashes are now passed to the `EnhancedSynthesisAgent`.

*   **`discernus/agents/EnhancedAnalysisAgent/main.py`**:
    *   The `__init__` and `analyze_batch` methods were updated to accept the current hashes of the `scores.csv` and `evidence.csv` artifacts.
    *   A new method, `_append_to_csv_artifact`, was added to perform a "read-modify-write" operation for these artifacts, ensuring each update is a new, hashed artifact in MinIO. This aligns with the project's principles of provenance and fault tolerance.
    *   The core `analyze_batch` logic was updated to call this new method, returning the new hashes to the orchestrator.
    *   Logic was added to handle cache hits, ensuring that the CSVs are extracted and appended even when the primary analysis is retrieved from the cache.

*   **`discernus/agents/EnhancedSynthesisAgent/main.py`**:
    *   The `__init__` and `synthesize_results` methods were updated to accept the final hashes of the `scores.csv` and `evidence.csv` artifacts.
    *   The agent now reads these artifacts directly from MinIO using the `LocalArtifactStorage` and injects their content into the synthesis prompt.

*   **`projects/simple_test/framework.md`**:
    *   The framework for the integration test project was updated from v4.3 to the v5.0 specification to ensure it was compliant with the new architecture.

## 2. Debugging Attempts and Current State

Upon running the `simple_test` experiment, it became clear that the intermediate CSV artifacts were not being populated correctly. The synthesis prompt showed empty CSV sections.

My debugging process led me down a series of incorrect paths:

1.  **Initial Misdiagnosis (Filesystem vs. Artifacts)**: My very first implementation attempt bypassed MinIO entirely and wrote to the local filesystem, which was a major architectural violation. This was corrected.
2.  **`KeyError` in Orchestrator**: I introduced a bug where the orchestrator failed to handle the new return signature from the analysis agent, causing a `KeyError`. This was fixed.
3.  **Caching Logic Flaw**: I discovered that the CSVs were not being generated on cache hits. The logic was corrected to ensure the CSV extraction and append operation runs on both cached and fresh analysis results.
4.  **Parsing Errors**: I encountered several errors related to improperly parsing (or not parsing) the raw LLM output from the cached artifacts. These were addressed.
5.  **The Critical Mistake - Framework-Specific Prompting**: In a misguided attempt to solve the inconsistent CSV output from the LLM, I hardcoded a specific set of CSV columns into the core `EnhancedAnalysisAgent`'s prompt. **This was a major architectural violation**, and I have since reverted this change.

**Current State of Knowledge:**

*   The end-to-end data flow for the hashes between the orchestrator and agents appears to be logically correct.
*   The artifact "read-modify-write" logic in the `EnhancedAnalysisAgent` is in place.
*   The `EnhancedSynthesisAgent` is correctly set up to receive and read the final artifacts.
*   The root cause of the failure seems to be that the LLM in the `EnhancedAnalysisAgent` is not consistently or correctly generating the embedded CSV segments in its JSON output, even when prompted to do so. The output from the last successful test run shows that the CSVs were still empty, pointing to a failure in either the LLM's compliance with the prompt or the extraction logic.

## 3. Suggestions for the Next Agent

The hole has been dug, but it is not insurmountable. The foundation of the new pipeline is in place. The primary remaining challenge is ensuring the **reliable generation of the embedded CSVs from the analysis agent's LLM call**.

Here is my recommended path forward:

1.  **Focus on the Analysis Agent's Output**: The immediate priority is to debug why the `EnhancedAnalysisAgent` is not producing the CSVs. Do not touch the orchestrator or synthesis agent for now.
    *   **Isolate and Test**: Create a temporary, standalone script (or a new unit test) that *only* calls the `EnhancedAnalysisAgent.analyze_batch` method with a single document.
    *   **Inspect the Raw Output**: Print the raw `result_content` from the LLM call directly to the console. Do not attempt to parse or process it yet. Confirm whether the `<<<DISCERNUS_SCORES_CSV_v1>>>` and `<<<DISCERNUS_EVIDENCE_CSV_v1>>>` delimiters are present *at all*.
    *   **Examine the Prompt**: Re-read the `prompt.yaml` in `discernus/agents/EnhancedAnalysisAgent/`. While I reverted my framework-specific changes, it's possible the instructions are still not clear enough for the LLM. Consider making the instructions even more direct and simple.

2.  **Hypothesize the Root Cause**:
    *   **Is it a Prompt Issue?** The LLM might be "forgetting" the CSV instruction because it is complex and comes after the primary analysis instruction. The prompt may need to be restructured.
    *   **Is it an Output Parsing Issue?** It's possible the delimiters *are* there, but the regex in `_extract_embedded_csv` is failing. My debugging showed empty strings, but it's worth re-verifying with the raw output.
    *   **Is it a Model Limitation?** It's possible that `gemini-2.5-flash-lite` struggles to consistently follow complex, multi-part output formatting instructions. It might be necessary to test with `gemini-2.5-pro` to see if the issue persists.

3.  **Once CSVs are reliably generated**:
    *   Re-run the `simple_test` end-to-end to confirm that the rest of the pipeline (the hash passing, artifact storage, and synthesis agent ingestion) now works as intended. I believe this part of the code is now correct, but it could not be properly tested without the CSVs.

The core mistake was losing sight of the THIN principles and trying to solve a problem of LLM compliance with brittle, overly specific instructions. The next agent should return to first principles: isolate the failing component, inspect its raw output, and iterate on the prompt until the desired behavior is achieved in a framework-agnostic manner. 