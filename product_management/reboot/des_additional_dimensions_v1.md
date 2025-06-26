# DES Extensions — Six Additional Research Dimensions  
*Date: 2025‑06‑25*

## Additional Dimensions Worth Carving into the DES  

| # | Dimension | Research Question Unlocked | Minimal DES Hooks |
|---|-----------|---------------------------|-------------------|
| 6 | **Retrieval‑Augmented Context (RAG)** | “How do scores change with background sources X vs Y?” | `context_enrichment` block with source corpora & top‑k |
| 7 | **Multimodal Inputs** | “Does an image or audio clip shift moral portrayal?” | `multimodal` spec (`modalities`, `preproc_model`) |
| 8 | **Counter‑factual / Synthetic Texts** | “Swap ‘immigrant’ for ‘refugee’ – what shifts?” | `counterfactuals` substitution rules |
| 9 | **Robustness / Perturbation Sweep** | “Stable under typos, paraphrases, adversarial prompts?” | `perturbation_tests` configs |
| 10 | **Privacy & Redaction Modes** | “Run but never store PII.” | `privacy` policy & detector model |
| 11 | **Self‑Explanation Capture** | “Grab model justifications for qualitative coding.” | `explanations.capture` flag |

### Key Implementation Notes  

* Optional blocks keep default pipeline intact.  
* Cost and latency controlled by existing execution caps.  
* Report Builder gains new tabs: perturbation drift, RAG source citations, privacy audit.  

---

*Every new lens—context, modality, counter‑facts—fits cleanly when DES leaves optional doors instead of later renovations.*  
