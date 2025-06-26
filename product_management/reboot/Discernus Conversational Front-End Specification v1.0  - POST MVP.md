# Discernus Conversational Front-End Specification v1.0  - POST MVP
*(“English-as-Code” Interface)*  

#discernus/reboot

---

## 1 – Vision  

Enable researchers to design, launch, and retrieve Discernus experiments using **plain-language chat** instead of editing YAML or invoking CLI commands.  
The chat agent acts as a *compiler*: translating natural-language “recipes” into validated experiment YAML, triggering the pipeline, and returning artefacts as clickable links.

---

## 2 – User Personas & Stories  

| Persona | Goal | Sample Utterance |
|---------|------|------------------|
| **Social-Psych Scholar** | Run MFT on 50 speeches | “Analyze these 50 inaugural speeches with Moral Foundations Theory and give me the radar plot.” |
| **Political Journalist** | Compare framing across parties | “Frame 2024 debate transcripts with the PFT anchors and show differences.” |
| **Methodology Reviewer** | Verify replication | “Show me the YAML and corpus hash for the Johnson & Lee 2025 study.” |

---

## 3 – Functional Requirements  

1. **Recipe Parsing** – convert chat request → validated Experiment YAML.  
2. **Dependency Resolution** – auto-attach latest framework, prompt, and corpus slugs unless user overrides.  
3. **Run Orchestration** – enqueue Celery batch, stream status messages (“30 % complete…”).  
4. **Artefact Delivery** – send clickable links for HTML/PDF report, replication ZIP, and raw JSON.  
5. **History & Recall** – “Show my last three runs” returns a summary table.  
6. **Error Handling** – natural-language explanations + suggestions (e.g., missing license).  
7. **Permissions** – OAuth login; user sees only their own runs unless flagged public.  

---

## 4 – Non-Functional Requirements  

| Attribute | Target |
|-----------|--------|
| **Latency** | < 3 s to parse recipe and start job |
| **Uptime** | 99 % SLA (chat service layer) |
| **Scalability** | 100 concurrent users |
| **Cost Awareness** | Bot estimates token cost before confirmation |
| **Security** | OWASP Top-10 compliant; rate-limit 10 req/min/user |

---

## 5 – High-Level Architecture  

```mermaid
sequenceDiagram
  participant U as User
  participant Chat as Chat API (FastAPI+LLM)
  participant Lang as LangGraph Compiler
  participant Orchestrator as Celery Queue
  participant DB as Postgres
  participant FS as Object Storage (reports)

  U->>Chat: Plain-language recipe
  Chat->>Lang: pass recipe text
  Lang->>Lang: parse ➜ Experiment YAML
  Lang-->>Chat: YAML + cost estimate
  Chat->>U: “Confirm run (est. $3.20)?”
  U-->>Chat: Confirm
  Chat->>Orchestrator: enqueue job(id)
  Orchestrator->>DB: insert run record
  Orchestrator->>FS: save artefacts
  Orchestrator-->>Chat: stream progress
  Chat-->>U: Links to report & zip
