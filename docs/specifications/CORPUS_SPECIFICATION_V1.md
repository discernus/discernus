# Corpus Specification (v1.0)

**Version**: 1.0  
**Status**: Active

To ensure MECE (Mutually Exclusive, Collectively Exhaustive) completeness and to support more rigorous hypothesis testing, the system supports an optional `corpus.md` manifest file.

---

## 1. File Structure

If present, the `corpus.md` file MUST be a YAML file located in the root of the corpus directory.

---

## 2. Schema

The purpose of this file is to allow researchers to provide metadata for the files in their corpus. This is particularly useful for pre-categorizing texts to test a hypothesis or for tracking ground truth data.

```yaml
# A list of files in the corpus and any associated metadata.
# The `name` field is required. All other fields are user-defined.
files:
  - name: cory_booker_2018_first_step_act.txt
    # Example user-defined metadata fields
    expert_categorization: "legislative_action"
    speaker_id: "cb_01"
    political_party: "Democrat"
    year: 2018

  - name: mitt_romney_2020_impeachment.txt
    expert_categorization: "statement_of_principle"
    speaker_id: "mr_01"
    political_party: "Republican"
    year: 2020
```

---

## 3. Usage

The data from this file will be made available to the orchestration workflow. For example, the `SynthesisAgent` can use this metadata to perform more sophisticated post-analysis filtering and grouping of results, such as comparing average scores between different political parties or time periods. 