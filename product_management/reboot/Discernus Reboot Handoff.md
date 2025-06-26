# Discernus Reboot Handoff
#discernus/reboot
### Opening Framework — Key Points Before the Handoff
* **Unified DES direction is clear.** We’ve drafted the core requirements (v0.3), evaluator extensions, temporal/comparative hooks, five & six extra dimensions, and analysis/visualisation guidance.
* **Artifacts are saved in** /mnt/data/ with explicit filenames; links have been tested.
* **MVP environment, architecture diagram, and BOM are locked.**

⠀
# 1 – Artifact Index (filenames in sandbox)
| **Theme** | **Filename** |
|:-:|:-:|
| **DES core requirements** | discernus_des_requirements_v0.3.md |
| Evaluator abstraction | des_evaluator_extensions_v0.1.md |
| Temporal & comparative hooks | des_temporal_comparative_extension.md |
| Five next-obvious axes | des_next_axes_v1.md |
| Six additional dimensions | des_additional_dimensions_v1.md |
| Analysis / visual guidance | des_analysis_visual_guidance_v0.1.md |
| MVP spec & env/BOM | discernus_mvp_spec_v1.1.md, discernus_mvp_env_bom_v1.0.md |
| Architecture diagram (PNG) | discernus_mvp_arch.png |
| Corpus spec | corpus_schema_v1.0.md |

# 2 – Suggested Handoff Packet
**1** **README-handoff.md**
	* Purpose, current branch names, open tasks.
**2** **/specs/** folder
	* Move all *_v*.md spec docs here.
**3** **/diagrams/** folder
	* Place discernus_mvp_arch.png.
**4** **/examples/**
	* Include sample DES YAML illustrating one temporal + evaluator mix.
**5** **Issue board refresh**
	* Create GitHub issues: Schema finalization, JSON-Schema drafting, migration script, notebook auto-generator.

⠀
# 3 – Next Collaborator’s Immediate To-Dos
| **Priority** | **Task** |
|:-:|:-:|
| **P0** | Convert discernus_des_requirements_v0.3.md into formal JSON Schema draft. |
| **P1** | Prototype des migrate script on mft_multi_llm_comprehensive_v2.yaml. |
| **P1** | Draft auto-notebook template, confirm runs with sample raw output. |
| **P2** | Evaluate evaluator extension feasibility in orchestrator (Celery fan-out). |
| **P2** | Align analysis recipe DSL ops with pandas/plotly API. |

# 4 – Context-Keeper Tips
* **Reference lockfiles**: all specs assume SHA-256 locking; emphasise in schema.
* **Backward compatibility**: orchestrator must treat missing new blocks as defaults.
* **Cost guardrails**: ensure execution.cost_cap_usd bubbles up through evaluator list.

⠀
### Thought-Provoking Takeaway
*We’ve mapped the territory; now it’s engineering carpentry.* With specs frozen and deliverables indexed, the next collaborator can move from blueprint to code without losing the narrative thread.

#discernus/reboot