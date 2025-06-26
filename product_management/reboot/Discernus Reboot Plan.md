# Discernus Reboot Plan
#discernus/reboot

## Situation Analysis
**BLUF — Discernus possesses a rare union of theory-driven IP and a compelling moral-cartography vision, but its home-grown infrastructure is dragging velocity, reliability, and team energy. A decisive architectural reset—keeping the distinctive frameworks while replacing bespoke plumbing—will unlock an MVP in weeks and position the project for planetary scale.**

### Opening Framework — Situation at a Glance
* **Strategic Edge** – Original analytic frameworks, coordinate geometry, and narrative visualizer form an IP moat; few competitors mingle moral theory with LLMs so rigorously.
* **Operational Drag** – A monolithic orchestrator duplicates commodity functions (LLM routing, task queueing) and fails frequently, stalling research momentum.
* **Market Timing** – Open-source stacks (LiteLLM, LangGraph, Celery, Supabase) now deliver turnkey reliability; academic demand for transparent, replicable LLM studies is surging.
* **Leadership Imperative** – Pivot from “builder of every gear” to “composer of higher-order meaning”—freeing talent to craft insights, not battle infrastructure.
⠀
### 1. Context & Background
Like a cartographer charting new continents, Discernus set out to map the moral foundations of modern discourse. The journey produced **ten richly annotated YAML frameworks**, an interactive Plotly coordinate visualizer, and a proof-of-concept orchestrator that could, in theory, run thousands of text evaluations. Reality proved harsher: recursive registry errors, version-skew, and spaghetti async loops turned each expedition into a slog.
Meanwhile, the tooling ecosystem sprinted ahead. What took Discernus months to prototype—multi-provider LLM gateways, durable DAG engines, horizontal task queues—now ships in single-line Docker commands. The world changed around the project; the mapmaker can now charter railroads instead of hacking through jungle.

### 2. Internal Assessment
| **Asset** | **Strength** | **Weakness** |
|:-:|:-:|:-:|
| Framework YAMLs | Unique theory, peer-review ready; declarative and portable | Version drift across copies; no automated validation |
| Visualizer | Engaging, story-telling plots; zero failures in logs | Hard-wired to bespoke JSON schema; needs API shim |
| Orchestrator | Early proof that concept works | Monolithic, brittle, duplicates open-source features |
| Team Expertise | Deep social-science insight; product vision | Limited bandwidth for low-level DevOps |

### 3. External Landscape
* **Tools Explosion** – LiteLLM, LangGraph, Temporal.io, Ray, and Supabase reduce infrastructure effort by 80-90 %.
* **Competitive Noise** – Dozens of RAG start-ups compete on plumbing; few articulate *why* language matters.
* **Scholarly Demand** – Journals and funders now insist on transparent replication bundles—Discernus’ declarative specs are a perfect match.

⠀
### 4. Opportunity & Threat Matrix
|  | **Opportunity** | **Threat** |
|:-:|:-:|:-:|
| **Technology** | Bolt reliable OSS components onto Discernus theories and sprint to MVP | Continue maintaining custom code; burnout and stalled releases |
| **Market** | Offer “moral cartography as a service” for think tanks, journalists, educators | Competitors adopt same OSS stack and outpace without unique theory |
| **Reputation** | Publish early replication packages; build academic goodwill | Frequent orchestrator crashes erode credibility |

### 5. Strategic Implications
**1** **Refactor, don’t rewrite IP** – Move frameworks and visualizer into a clean branch; delete, outsource, or wrap everything else.
**2** **Shift talent up the stack** – Direct scarce coding hours to theory validation, UX polish, and replication tooling.
**3** **Adopt English-first UX** – Let researchers write “recipes,” not YAML; an agent translates to specs behind the scenes.
**4** **Institute provenance hygiene** – Single canonical copy of every framework; automated schema linting in CI.
**5** **Time-box MVP** – Six-week sprint to run two frameworks, one model, Celery queue, LiteLLM proxy, and live HTML plot.

## Step 1: Branch and Purge
Spin off a **clean, history-preserving branch** inside the current repo and treat it as a “green-field” rebuild. You keep the audit trail, avoid the mental tax of a brand-new repo, and gain an easy path to cherry-pick proven modules while ruthlessly deleting anything you no longer want. When the refactor stabilises, open a PR and fast-forward-merge it into main.

1. **1** **Cut the branch** `git checkout -b refactor/discernus_rebuild`

2. **Nuke everything except real assets** (framework YAMLs, visualizer, MVP plan) `git rm -r orchestrator/* old_cli/ docs/  # keep what matters`
   `git commit -m "Start green-field rebuild: preserve core assets only"` 
3. **Introduce your modern stack** – add LiteLLM proxy config, LangGraph workflow skeleton, and slim Celery worker.
4. **Push and open a Draft PR** so progress is visible but isolated.
5. **Wire CI** to run only the new workflow on this branch.
6. **Cherry-pick or copy-paste** any utility modules that prove their worth during rebuild; everything else stays dead.
7. **When tests are green and docs updated**:
   `git checkout main`
   `git checkout main`
8. Tag the merge (v0.9.0-MVP) and archive the legacy orchestrator in a GitHub release for posterity.

### Principles for What to Keep vs Nuke
Preserve the assets that embody Discernus’** ***intellectual edge*** **and proven reliability; ruthlessly delete or replace anything that is generic plumbing, un-validated, or duplicative.**

#### Opening Framework – Seven Sorting Rules
**1** **Keep unique theory & data models** – nuke commodity infrastructure.
**2** **Keep code that** ***already works and is tested*** – nuke anything chronically failing.
**3** **Keep declarative specs (YAML, SQL schemas)** – nuke imperative glue that hard-codes pathways.
**4** **Keep single-responsibility modules** – nuke monolithic multitask files.
**5** **Keep external-facing interfaces & examples** – nuke hidden throw-away prototypes.
**6** **Keep clear provenance history** – nuke version-skewed duplicates.
**7** **Keep small, composable scripts** – nuke “God objects” larger than one screen of logic.

	| **#** | **KEEP When…** | **NUKE When…** | **Rationale & Evidence** |
|:-:|:-:|:-:|:-:|
| **1** | The artefact encodes *original theory* (e.g., the framework YAMLs and coordinate system geometry) | It rebuilds commodity services like an LLM router or task queue | Discernus frameworks are distinctive scholarly IP , while LiteLLM already solves generic model routing more robustly |
| **2** | Unit tests pass and logs show stable runs | Logs show recursive failures or YAML parse bombs | The visualizer runs cleanly ; the orchestrator spews ScannerErrors line after line |
| **3** | The file is a declarative recipe you can hand to any engine (framework YAMLs, DB schema scripts) | It is imperative glue you wrote because no standard existed | Declarative specs travel well; imperative glue will be replaced by LangGraph/Celery anyway |
| **4** | A file owns one well-defined job (e.g., discernus_coordinate_visualizer.py) | A single script tries to be validator, scheduler, and database layer at once | Single-purpose modules are maintainable; monoliths block parallel work |
| **5** | It teaches users how to use Discernus (sample YAML, demo notebooks) | It is an internal spike or half-done prototype no longer referenced | External examples are your on-ramp; dead spikes just confuse newcomers |
| **6** | There is exactly one canonical version and a meaningful git history | Multiple copies with version drift exist (civic_virtue_v1.0.yaml vs DB “v2025.06.14”) | Forked copies cause registry mismatches and endless “which one is truth?” debates |
| **7** | The code fits on one screen, follows SRP, and is easy to unit-test | It sprawls, hides nested loops, or requires a mental stack trace | Short, composable scripts survive refactors; sprawling orchestrator code does not |
#### How to Apply These Rules in Practice
**1** **Run the tests** – anything that fails without a good reason is a nuclear candidate.
**2** **grep for “TODO”, “hack”, “tmp”** – likely cruft.
**3** **Count lines of code** – >300 LOC single files almost always violate Principle #7.
**4** **Ask “Could an off-the-shelf library do this better?”** – if yes, delete and depend.
**5** **Retain only one canonical copy** of every framework, prompt template, and schema.
**6** **Document what survives** in a KEPT_ASSETS.md; everything else heads to the graveyard branch.

## 