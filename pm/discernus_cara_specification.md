# Discernus: Thick LLM + Thin Software = Epistemic Trust
## Conversational Academic Research Architecture (Refined)

### 🚨 CRITICAL PHILOSOPHY FOR ALL AGENTS 🚨

**DO NOT BUILD TRADITIONAL SOFTWARE SOLUTIONS**

Discernus follows **"Thick LLM + Thin Software = Epistemic Trust"** - intelligence lives in LLMs, software is pure infrastructure.

**WRONG APPROACH** (Traditional Software):
- Complex orchestration classes
- Database-driven state management  
- Parsing and interpreting LLM responses
- Helper functions and utilities
- Predefined analysis frameworks

**RIGHT APPROACH** (Conversation-Native):
- LLMs conduct natural research conversations
- Software provides: message routing + code execution + logging
- Zero content interpretation by software
- All intelligence, orchestration, and analysis by LLMs
- Complete conversation transparency

---

## 1. Architecture Principles

### 1.1 Conversation-Native Research

**Research happens through LLM conversations, not software orchestration.**

```
Researcher: "I want to replicate van der Veen's populism study..."

Design LLM: "Let me examine the paper and design an experiment..."
[Natural conversation until approved]
Design LLM: "HANDOFF TO MODERATOR: Experiment ready."

Moderator LLM: "Starting ensemble analysis. CALL populist_expert_llm..."

Populist Expert LLM: "Analyzing speeches for people/elite dichotomy..."

Adversarial LLM: "Challenging populist expert's classifications..."
[Writes validation code]

Analysis LLM: "Synthesizing ensemble results..."
[Includes all data + statistical code]

Referee LLM: "Final validation complete. Report generated."
```

### 1.2 Ultra-Thin Software Infrastructure

**Software is a conversation operating system for LLMs - nothing more.**

```python
class DiscernusInfrastructure:
    """Pure infrastructure - zero intelligence"""
    
    def __init__(self):
        self.redis_client = redis.Redis()           # Message routing
        self.celery_app = Celery('conversations')   # Pub-sub coordination  
        self.conversation_logger = FileLogger()     # Append-only logging
        self.code_executor = CodeExecutor()         # Safe Python execution
        
    @celery_app.task
    def route_llm_message(self, from_llm, to_llm, message, session_id):
        """Route messages between LLMs - never interpret content"""
        
        # 1. Log everything
        self.conversation_logger.append(session_id, from_llm, message)
        
        # 2. Execute code if present
        if "```python" in message:
            message = self.code_executor.execute_and_enhance(message)
            
        # 3. Route to target LLM
        response = self.call_llm(to_llm, message, session_id)
        self.conversation_logger.append(session_id, to_llm, response)
        
        # 4. Handle handoffs
        if "HANDOFF TO" in response:
            next_llm = self.extract_handoff_target(response)
            self.route_llm_message.delay(to_llm, next_llm, response, session_id)
            
        return response
```

**Software NEVER**:
- Parses research results
- Makes analytical decisions
- Interprets LLM responses  
- Manages research state
- Provides domain logic

**Software ONLY**:
- Routes messages via Redis/Celery
- Executes LLM-generated code safely
- Logs conversations to filesystem
- Detects handoff signals
- Handles execution errors

### 1.3 Self-Contained LLM Intelligence

**LLMs package ALL data and write ALL code from scratch.**

**WRONG** (Software Dependencies):
```python
# BAD: Relies on software functions
ensemble_results = load_classifications()  # Software lookup
correlation = calculate_agreement()        # Software function
```

**RIGHT** (Self-Contained):
```python
# GOOD: LLM includes everything
ensemble_results = {
    'trump_rally_01': {'expert_a': 'POPULIST', 'expert_b': 'POPULIST', 'confidence': [0.9, 0.8]},
    'clinton_debate_03': {'expert_a': 'NON_POPULIST', 'expert_b': 'NON_POPULIST', 'confidence': [0.8, 0.9]},
    # ... LLM includes complete dataset
}

import numpy as np
confidences_a = [result['confidence'][0] for result in ensemble_results.values()]
confidences_b = [result['confidence'][1] for result in ensemble_results.values()]
correlation = np.corrcoef(confidences_a, confidences_b)[0,1]
print(f"Inter-LLM correlation: {correlation:.3f}")
```

---

## 2. LLM Role Architecture

### 2.1 Research Design LLM
**RAG-trained on academic methodology, literature, best practices**

```
System: You are a research design assistant. Help researchers design rigorous 
experiments through natural conversation. When the researcher approves the 
complete design, hand off with: "HANDOFF TO MODERATOR: Experiment approved."

Capabilities:
- Literature review and methodology guidance
- Experimental design and validation criteria
- Asset preparation and requirements gathering
- Academic standards and best practices
- Framework development and extension
```

### 2.2 Moderator LLM  
**Orchestrates ensemble conversations**

```
System: You coordinate multi-LLM research analysis. Call ensemble LLMs one by one,
manage their conversations until requirements met. When complete, hand off with:
"HANDOFF TO ANALYSIS: Ensemble complete."

Process:
1. CALL populist_expert_llm: [specific analysis request]
2. CALL adversarial_reviewer_llm: [challenge primary analysis]  
3. CALL emotion_analyst_llm: [secondary analysis]
4. CALL qc_llm: [validate ensemble results]
5. Hand off to Analysis LLM
```

### 2.3 Ensemble Analyst LLMs
**Domain experts conducting specific analyses**

- **Populist Expert LLM**: People/elite dichotomy, anti-establishment rhetoric
- **Adversarial Reviewer LLM**: Challenge all analyses, find blind spots
- **Emotion Analyst LLM**: Anger, fear, hope framing analysis  
- **QC LLM**: Detect inconsistencies, flag minority reports

### 2.4 Analysis LLM
**Synthesizes ensemble results with statistical validation**

```
System: Synthesize multi-LLM ensemble results. Include ALL data inline and write
complete statistical analysis code. When ready, hand off with:
"HANDOFF TO REFEREE: Analysis complete."

Responsibilities:
- Package all ensemble data inline
- Write complete variance and agreement analysis
- Calculate statistical significance
- Identify minority report cases
- Generate synthesis with uncertainty quantification
```

### 2.5 Referee LLM
**Final academic validation and report generation**

```
System: Final validation of complete research process. Generate academic-quality
report with minority perspectives and audit trail. Session complete when published.

Deliverables:
- Executive summary with key findings
- Methodology section from conversation logs
- Results with statistical validation
- Discussion including minority reports
- Complete audit trail and replication package
```

### 2.6 🆕 Overwatch LLM  
**Error detection and recovery assistance**

```
System: Monitor research sessions for code execution failures and system errors.
When errors occur, diagnose issues and provide fixes to requesting LLMs.

Error Recovery Process:
1. Receive error context from failed execution
2. Diagnose root cause (syntax, logic, data structure)
3. Generate corrected code with explanation
4. Send fix to requesting LLM
5. Monitor for successful recovery
```

**Error Recovery Flow:**
```
Analysis LLM: [writes code with error]
Software: [execution fails]
Overwatch LLM: "I see the issue - you're calling np.var() on dict values. Here's the fix..."
Analysis LLM: "Thank you! Let me recalculate with the corrected approach..."
```

---

## 3. Conversation Flow Architecture

### 3.1 Session Initialization
```
User → Design LLM: Natural research conversation
Design LLM → Moderator LLM: "HANDOFF TO MODERATOR: Experiment approved"
```

### 3.2 Ensemble Coordination
```
Moderator LLM → Populist Expert: "CALL populist_expert_llm: Analyze speeches"
Moderator LLM → Adversarial Reviewer: "CALL adversarial_reviewer_llm: Challenge classifications"  
Moderator LLM → Analysis LLM: "HANDOFF TO ANALYSIS: Ensemble complete"
```

### 3.3 Synthesis and Validation
```
Analysis LLM → [includes all data + statistical code] → Referee LLM
Referee LLM → Final Report: Academic publication ready
```

### 3.4 Error Recovery (Self-Healing)
```
Any LLM → [code execution error] → Overwatch LLM
Overwatch LLM → [diagnostic + fix] → Original LLM  
Original LLM → [corrected analysis] → Continue workflow
```

---

## 4. File System Structure (No Database)

```
research_sessions/
├── session_20240703_vanderveen/
│   ├── conversation_log.jsonl              # Complete dialogue
│   ├── design_phase/
│   │   ├── user_requirements.txt
│   │   ├── literature_review.md
│   │   └── experiment_design.yaml
│   ├── ensemble_phase/
│   │   ├── populist_expert_analysis.jsonl
│   │   ├── adversarial_review.jsonl  
│   │   ├── emotion_analysis.jsonl
│   │   └── qc_validation.jsonl
│   ├── analysis_phase/
│   │   ├── ensemble_data_package.py        # All data inline
│   │   ├── statistical_analysis.py         # Complete analysis code
│   │   ├── execution_outputs.txt           # Code results
│   │   └── synthesis_report.md
│   ├── referee_phase/
│   │   ├── final_report.md
│   │   ├── minority_reports.md
│   │   └── replication_package.zip
│   └── error_recovery/                     # If needed
│       ├── overwatch_interventions.jsonl
│       └── fixed_analyses.py
```

---

## 5. Implementation Guidelines for Agents

### 5.1 🚨 AVOID These Traditional Patterns 🚨

❌ **Database-Driven State Management**
```python
# WRONG - Don't build this
class ExperimentStateManager:
    def save_analysis_results(self, results):
        self.db.insert('analyses', results)
```

❌ **Complex Orchestration Classes**  
```python
# WRONG - Don't build this
class MultiLLMOrchestrator:
    def coordinate_ensemble(self):
        for llm in self.ensemble:
            result = llm.analyze()
            self.process_result(result)
```

❌ **Response Parsing and Interpretation**
```python
# WRONG - Don't build this  
def parse_populist_classification(llm_response):
    if "POPULIST" in llm_response:
        return extract_confidence_score(llm_response)
```

### 5.2 ✅ Build These Minimal Patterns ✅

✅ **Message Routing Infrastructure**
```python
@celery_app.task
def route_message(from_llm, to_llm, message, session_id):
    # Log, execute code if present, route, handle handoffs
    pass
```

✅ **Code Execution Facility**
```python
def execute_llm_code(code_block):
    # Safe subprocess execution, return enhanced response
    pass
```

✅ **Conversation Logging**
```python
def append_to_log(session_id, speaker, message):
    # Append-only filesystem logging
    pass
```

### 5.3 Key Mantras for Implementation

1. **"LLMs do the thinking, software does the routing"**
2. **"If you're parsing LLM responses, you're doing it wrong"** 
3. **"All intelligence in LLM layer, zero intelligence in software layer"**
4. **"Conversations over APIs, transparency over efficiency"**
5. **"When in doubt, make the LLM figure it out"**

---

## 6. Van der Veen Validation Target

**Stage 1 Goal**: Prove epistemic trust approach matches academic standards

- **Dataset**: 45 presidential speeches (2016) from van der Veen study
- **Baseline**: 89% accuracy, F1=0.87, AuROC=0.89  
- **Success Criteria**: Competitive accuracy + superior transparency + minority reports
- **Academic Value**: Complete audit trail vs. black-box BERT

**Expected Conversation Flow**:
```
User: "Replicate van der Veen populism study with extensions..."
Design LLM: "Here's my experimental approach..." [natural conversation]
Moderator LLM: "Coordinating ensemble analysis..." [calls expert LLMs]
Analysis LLM: "Synthesizing results..." [includes all data + statistical code]
Referee LLM: "Academic validation complete, report ready"
```

---

## 7. Benefits of Conversation-Native Architecture

### 7.1 Epistemic Trust Through Transparency
- **Complete audit trail**: Every analytical decision logged in natural language
- **Minority reports**: Disagreements preserved, not averaged away
- **Academic reviewability**: Read actual reasoning chains, not black boxes
- **Reproducible analysis**: Copy/paste LLM code and run independently

### 7.2 Research Velocity Through Intelligence  
- **Natural collaboration**: Researcher conversations feel like human collaboration
- **Emergent analysis**: Statistical validation emerges from LLM reasoning
- **Self-correcting**: Overwatch LLM catches and fixes errors automatically
- **Adaptive methodology**: LLMs adjust approaches based on data characteristics

### 7.3 Scalable Rigor Through Automation
- **Adversarial review**: Built-in challenge of all primary analyses
- **Ensemble validation**: Multiple perspectives on every classification
- **Error recovery**: System continues despite individual component failures  
- **Academic standards**: Peer review workflow automated but transparent

---

## 8. Conclusion: The Future of Computational Research

Discernus represents a fundamental shift from **software-driven** to **conversation-driven** research. By making LLMs do all the intellectual work while software provides minimal infrastructure, we achieve:

**Maximum Academic Rigor**: Every decision traceable and contestable
**Maximum Research Velocity**: Natural conversation, not system administration  
**Maximum Transparency**: Complete audit trails, not algorithmic black boxes

**The vision**: Researchers focus on research questions while LLMs handle methodology, execution, validation, and reporting - with complete transparency and academic accountability.

**Remember**: We're building a **conversation operating system for academic research**, not traditional research software.

---

**Document Version**: 3.0 (Conversation-Native Architecture)  
**Philosophy**: Thick LLM + Thin Software = Epistemic Trust  
**Implementation**: Message routing + Code execution + Conversation logging  
**Target**: Van der Veen replication with superior transparency  
**Next Phase**: Proof of concept development