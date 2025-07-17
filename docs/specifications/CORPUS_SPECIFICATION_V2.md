# Corpus Best Practices Guide (v2.0)

**Version**: 2.0  
**Status**: Active  
**Principle**: The integrity of a computational analysis depends entirely on the integrity of the input corpus. This guide outlines the best practices for corpus preparation to enable rigorous, bias-controlled research. **It is the researcher's responsibility to prepare their corpus according to these principles *before* running an experiment.**

---

### Corpus Preparation Best Practices

1.  **Speaker/Author De-identification**: To mitigate speaker identity bias, all identifying information must be removed from the text and replaced with a unique, non-identifiable hash.
    *   **Tooling**: A reference implementation of a hashing script (`hash_generator.py`) and a speaker mapping file (`speaker_mapping.jsonl`) are available in `docs/reference/corpus_preparation/`.
    *   **Process**:
        1.  Create a `speaker_mapping.jsonl` file that maps original filenames or speaker names to unique, randomly generated hashes.
        2.  Run the `hash_generator.py` script to process the original corpus, replacing filenames with their corresponding hashes.

2.  **Content Sanitization (Optional but Recommended)**: For an even stronger control against bias, the content of the texts can be sanitized to remove subtle linguistic cues that might betray author identity.
    *   **Reference Prompts**: Example sanitization prompts from the Attesor Study are available for review in `docs/reference/corpus_preparation/`:
        *   `attesor_sanitization_supreme.md`: A prompt for general-purpose content sanitization.
        *   `attesor_esperanto_supreme.md`: A more advanced prompt that uses Esperanto as a "linguistic firewall" to neutralize stylistic idiosyncrasies.

3.  **Directory Structure**: The corpus should be a single directory containing one text file per document. The experiment will process all files within this directory.

---

## 1. The "Corpus State" Methodology

For rigorous bias analysis, we recommend preparing your corpus in multiple states, each in a separate directory. A typical project might have:

*   **`/corpus_original/`**: The raw, unmodified source texts with descriptive filenames (e.g., `speaker_name_speech_title.txt`).
*   **`/corpus_sanitized/`**: The bias-reduced versions of the texts, using hashed filenames.
*   **`/corpus_translated/`**: An optional, further sanitized version translated into a neutral language like Esperanto.

An experiment is then run against a specific corpus directory by pointing to it in the `experiment.md` `corpus:` key. For example, `corpus: corpus_sanitized/`.

---

## 2. Best Practice: Sanitization and Hashing

To mitigate the risk of LLMs activating biases based on speaker identity, we strongly recommend a sanitization and hashing process.

### 2.1. Sanitization

*   **Goal**: To remove all **Identity Vectors** (speaker names, specific locations, identifying dates, signature phrases) while preserving the core **Rhetorical Architecture** (argument structure, emotional tone, linguistic patterns).
*   **Process**: This is a methodological step that should be performed with care. We recommend using a powerful LLM guided by a detailed prompt.
*   **Recommendation**: A project SHOULD include a `/sanitization_prompts` directory containing the exact prompts used, ensuring the process is reproducible. An example can be found in `projects/attesor/sanitization_prompts/`.

### 2.2. Hashed Filenames

*   **Purpose**: To prevent the LLM from inferring speaker identity from filenames.
*   **Requirement**: All files within a `sanitized/` or `translated/` corpus directory SHOULD use a hashed filename.
*   **Mechanism**: A salted SHA-256 hash, truncated to 12 characters for manageability.
*   **Tooling**: The project provides a reference implementation script to automate this process at `scripts/hash_generator.py`.

---

## 3. Best Practice: The Secure Lookup Table

To link anonymized files back to their sources for post-analysis interpretation, a secure lookup table is essential.

*   **Filename**: `speaker_mapping.jsonl`
*   **Location**: This file MUST be placed in the project's root directory, **not** inside any `corpus/` directory, to prevent it from being accidentally fed to an LLM.
*   **Format**: A JSONL file where each line is an object mapping a hash to its source metadata.

#### **Schema**
```json
{
  "hash": "9c759f7025a4",
  "speaker": "Mitt Romney",
  "title": "2020 Impeachment Vote Speech",
  "source": "mitt_romney_2020_impeachment.txt"
}
```

---

## 4. Best Practice: The `corpus.md` Manifest

For experiments requiring detailed, file-level metadata (e.g., for testing a hypothesis against pre-categorized data), we recommend creating a `corpus.md` manifest inside the specific corpus directory you are analyzing.

*   **Example Location**: `corpus_sanitized/corpus.md`
*   **Content**: A YAML file listing metadata for each file in that directory. The filenames in the manifest MUST match the filenames in the directory (i.e., hashed names for a sanitized corpus).

#### **Schema**
```yaml
files:
  - name: 9c759f7025a4.txt
    expert_categorization: "statement_of_principle"
    political_party: "Republican"
  - name: cccec508db40.txt
    expert_categorization: "legislative_action"
    political_party: "Democrat"
``` 