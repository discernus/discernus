# Discernus DES Extensions – **Evaluator Abstraction & Hybrid Methods Draft v0.1**
*Date: 2025‑06‑25*

This addendum introduces a **unified “evaluators” layer** so a single DES file can orchestrate any blend of:

1. **Cloud‑hosted LLMs** (OpenAI, Anthropic, Google, etc.)
2. **Locally‑hosted or proprietary fine‑tuned LLMs** (GPU cluster, LM‑studio, vLLM)
3. **Crowdsourced human raters** via API platforms (MTurk, Prolific, Toloka, Swarm)
4. **Offline / archival human ratings** already completed in prior studies

---

## 1 – Top‑Level Hook

Replace (or supersede) the earlier `models:` array with a **single ordered list**:

```yaml
evaluators:
  - type: cloud_llm | local_llm | human_crowd | human_offline
    id: <string>          # slug
    version: <string>     # semantic or git‑hash
    config: {…}           # type‑specific
```

Execution engine fans‑out prompts or tasks to each evaluator and merges their outputs into a consistent signature schema.

---

## 2 – Type‑Specific Required Fields

| Type | Required `config` keys | Notes |
|------|------------------------|-------|
| **cloud_llm** | `provider` (openai/anthropic/…)<br>`model`<br>`api_key_ref` (env var / secret name)<br>`endpoint` (opt) | Reuses existing `execution.model` rules; cost captured via provider metadata. |
| **local_llm** | `engine` (vllm/ollama/transformers)<br>`model_path` or `huggingface_id`<br>`hardware` (gpu‑spec)<br>`max_batch_tokens` | Optional `launch_cmd` for containerised spin‑up if not always running. |
| **human_crowd** | `platform` (mturk/prolific/custom)<br>`task_template_id`<br>`reward_usd`<br>`assignments` (# per text)<br>`aggregation_method` (majority/mean/etc.) | Optional `qualification_tests`, `time_limit_min`. |
| **human_offline** | `data_file` (csv/tsv/jsonl path)<br>`schema` mapping to expected fields (`text_id`, `axis`, `score`) | Must include `provenance` (DOI, citation). |

---

## 3 – Shared Optional Keys

| Key | Purpose |
|-----|---------|
| `cost_cap_usd` | Overrides global cost cap per evaluator |
| `priority` | Integer; lower executes first (helpful if human tasks lag) |
| `weight` | Contribution weight in ensemble averaging (default 1) |

---

## 4 – Signature Merging Rules

1. **Vector Alignment** – axes must match framework; missing axes filled with `null`.  
2. **Aggregation** – default is *simple mean across evaluators*, weighted by `weight`.  
3. **Provenance Stamp** – `lock.evaluators[]` records SHA‑256 (LLM prompts), turk HIT IDs, or dataset checksum.  
4. **Conflict Flagging** – engine flags > 0.3 Euclidean distance between any two evaluator vectors for a text.

---

## 5 – Crowdsourcing Lifecycle

| Step | Responsibility |
|------|----------------|
| 1. Create tasks | Orchestrator via platform API |
| 2. Monitor status | Poll until all assignments completed or timeout |
| 3. Aggregate | Apply `aggregation_method` |
| 4. Persist | Store raw worker IDs & answers under `human_ratings` table |
| 5. Pay bonuses / close HITs | Automatic |

All PII stripped; only anonymised worker IDs stored.

---

## 6 – Local LLM Execution Guidance

- Prefer *vLLM* or *Ollama* with REST interface to match cloud call signature.  
- If `launch_cmd` provided, orchestrator spins container, mounts model, runs health‑check, tears down post‑run.  
- `hardware` key supports:  
  `gpu: "A100-40GB"`, `memory_gb: 80`, `num_gpus: 2`.

---

## 7 – Validation & Cost Accounting

| Dimension | Check |
|-----------|-------|
| Cloud LLM | API response status; token cost matches provider quote |
| Local LLM | Latency < `max_latency_ms` (optional); model hash matches `model_path.sha256` |
| Human Crowd | assignment count == config; inter‑rater reliability (Krippendorff α) ≥ config threshold |
| Human Offline | dataset checksum == declared; schema mapping passes |

---

## 8 – Example Hybrid DES Snippet

```yaml
evaluators:
  - type: cloud_llm
    id: openai_gpt4o_demo
    version: 2025-05-13
    config:
      provider: openai
      model: gpt-4o
      api_key_ref: OPENAI_API_KEY
      cost_cap_usd: 25

  - type: local_llm
    id: local_mistral_ft_v2
    version: git:c1a9e7d
    config:
      engine: vllm
      model_path: /models/mistral_finetune_v2
      hardware: {gpu: "A100-40GB", num_gpus: 1}
      max_batch_tokens: 4096

  - type: human_crowd
    id: prolific_mft_raters
    version: 2025-06-25
    config:
      platform: prolific
      task_template_id: tmpl_9412
      reward_usd: 0.60
      assignments: 5
      aggregation_method: majority
      qualification_tests: qual_334
      cost_cap_usd: 60
```

---

## 9 – Reporting Additions

Report Builder adds:

- **Evaluator Comparison Table** (per‑text and aggregate)  
- **Inter‑rater Reliability Section** for human tasks  
- **Latency & Cost Summary** per evaluator type

---

## 10 – Backward Compatibility

If `evaluators:` absent, engine falls back to previous `model` / `models` semantics (treated as single `cloud_llm`).  

---

*By elevating “who or what produced the score” to a first‑class list, the DES can flex from single GPU boxes to global crowd labs—without fracturing again.*  
