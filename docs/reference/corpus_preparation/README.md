# Corpus Preparation Tools & Reference Prompts

This directory contains reference implementations of tools and prompts to help researchers prepare their corpora for analysis, specifically focusing on mitigating speaker identity bias as demonstrated in the Attesor Study.

**For detailed best practices, please see the [Corpus Specification](../specifications/CORPUS_SPECIFICATION_V2.md).**

---

## Contents

*   `hash_generator.py`: A Python script to replace filenames with unique hashes based on a mapping file.
*   `speaker_mapping.jsonl`: An example mapping file. This links original speaker identifiers or filenames to generated hashes.
*   `reorganize_corpus.py`: A utility script for restructuring corpus files (use as needed).
*   `sanitization_prompt_context_removal.md`: A reference prompt for sanitizing text content to remove identifying linguistic styles.
*   `sanitization_prompt_esperanto_translation.md`: A reference prompt using Esperanto as a "linguistic firewall" for advanced sanitization.

---

## Workflow: De-identifying a Corpus

1.  **Create Your Mapping File**:
    *   Copy `speaker_mapping.jsonl` to your project directory.
    *   For each original document, create a JSON line entry mapping the original identifier (e.g., `"sandra_day_oconnor_speech.txt"`) to a unique, non-identifiable hash (e.g., `"sanitized_speech_a1c5e7d2"`). You can generate hashes using any preferred method.

    ```jsonl
    {"original_name": "speaker_a_doc_1.txt", "hash_name": "text_7f9a2b8c"}
    {"original_name": "speaker_b_doc_1.txt", "hash_name": "text_a4c8e1d9"}
    ```

2.  **Run the Hashing Script**:
    *   Place your original text files in a source directory (e.g., `my_project/corpus_original/`).
    *   Create a destination directory for the sanitized output (e.g., `my_project/corpus_sanitized/`).
    *   Run the script from your terminal:
        ```bash
        python3 docs/reference/corpus_preparation/hash_generator.py \
          --source_dir path/to/your/corpus_original \
          --dest_dir path/to/your/corpus_sanitized \
          --mapping_file path/to/your/speaker_mapping.jsonl
        ```

3.  **Verify**: Your `corpus_sanitized` directory should now contain the same files, but with their names replaced by the hashes from your mapping file. This is the directory you would point to in your `experiment.md`. 