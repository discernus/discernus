# Research Provenance Quick Reference
**Which file answers which question?**

---

## 🔍 **"I need to know..."** → **"Look here"**

| Question | File Type | Location |
|---|---|---|
| **"How long did this analysis take?"** | Run Chronolog | `results/{timestamp}/RUN_CHRONOLOG_{session}.jsonl` |
| **"What exactly did the LLM say?"** | Conversation | `conversations/conversation_{timestamp}_{id}.jsonl` |
| **"Can I replicate this analysis?"** | Conversation + Run Chronolog | Both files from same session |
| **"What scores did we get?"** | Final Report | `results/{timestamp}/final_report.md` |
| **"How many sessions have we run?"** | Project Chronolog | `PROJECT_CHRONOLOG_{project}.jsonl` |
| **"What evidence supports score X?"** | Conversation | Search for agent responses in conversation file |
| **"Is this model reliable across runs?"** | Multiple Run Chronologs | Compare timing across multiple sessions |
| **"When did we change our methodology?"** | Project Chronolog | Look for configuration changes over time |
| **🚨 "Why can't I find my files?"** | **Nested Repo Check** | **`python3 scripts/prevent_nested_repos.py --scan`** |

## 🚨 **START HERE: Repository Health Check**

**Before analyzing ANY provenance files, run this command:**
```bash
python3 scripts/prevent_nested_repos.py --scan
```

**If you see nested repositories:**
```bash
# Fix the issue immediately
python3 scripts/prevent_nested_repos.py --clean --confirm
git add .
git commit -m "Fix nested repository provenance issue"
```

**Why this matters**: Nested git repositories are the #1 cause of broken provenance. They prevent experiment files from being committed to the main repository, making replication impossible.

---

## 📁 **File Types at a Glance**

### **🌍 Project Chronolog** (Everything, All Time)
```
PROJECT_CHRONOLOG_attesor.jsonl
```
- **Size**: Large (grows over time)
- **Contains**: All events from all sessions
- **Use for**: Project history, methodology evolution

### **🎯 Run Chronolog** (Events, Single Run)  
```
RUN_CHRONOLOG_session_20250113_223231.jsonl
```
- **Size**: Small (8-20 events)
- **Contains**: System events and timing for one session
- **Use for**: Performance analysis, Cronbach's alpha

### **💬 Conversation File** (Content, Single Run)
```
conversation_20250113_223231_abc123.jsonl  
```
- **Size**: Large (100KB+ with full LLM responses)
- **Contains**: All LLM prompts and responses
- **Use for**: Replication, content analysis, scoring validation

### **📊 Final Report** (Results, Single Run)
```
final_report.md
```
- **Size**: Medium (5-15KB)
- **Contains**: Aggregated analysis results
- **Use for**: Publishing, summary statistics

---

## ⚡ **Common Tasks**

### **Find Timing Statistics**
```bash
grep "analysis_duration_seconds" results/*/RUN_CHRONOLOG_*.jsonl
```

### **Extract PDAF Scores**
```bash
grep -A 20 "analysis_agent_" conversations/conversation_*.jsonl
```

### **Verify File Integrity**
```bash
python3 -c "
from discernus.core.project_chronolog import get_project_chronolog
chronolog = get_project_chronolog('projects/attesor')
print(chronolog.verify_integrity())
"
```

### **List All Sessions**
```bash
python3 -c "
from discernus.core.project_chronolog import get_project_chronolog
chronolog = get_project_chronolog('projects/attesor')
sessions = chronolog.list_sessions()
for s in sessions: print(f'{s[\"session_id\"]}: {s[\"event_count\"]} events')
"
```

---

## 🧪 **Research Workflows**

### **Cronbach's Alpha Study**
1. Run analysis 5-10 times: `python3 discernus_cli.py execute project/experiment`
2. Collect run chronologs: `ls results/*/RUN_CHRONOLOG_*.jsonl`
3. Extract timing data: Use grep or Python parsing
4. Calculate alpha across timing consistency

### **Content Replication**
1. Copy framework and experiment files
2. Run analysis: `python3 discernus_cli.py execute project/experiment` 
3. Compare conversation files between runs
4. Verify identical prompts and similar reasoning

### **Performance Debugging**
1. Check run chronolog for errors: `grep "ERROR\|FAILED" RUN_CHRONOLOG_*.jsonl`
2. Check conversation file for LLM errors: `grep "ERROR\|failed" conversation_*.jsonl`
3. Verify project chronolog for system issues: `grep "ERROR" PROJECT_CHRONOLOG_*.jsonl`

---

## 🚨 **Troubleshooting**

| Problem | Solution |
|---|---|
| **No run chronolog created** | Check if session completed successfully in project chronolog |
| **Empty conversation file** | LLM client connection issue - check network/API keys |
| **Missing final report** | Aggregation phase failed - check conversation file for errors |
| **Corrupted chronolog** | Run integrity verification script above |
| **Can't find session** | Use `list_sessions()` script above to see all available sessions |

---

## 📚 **For More Detail**

- **Academic Research**: See `docs/RESEARCH_PROVENANCE_GUIDE.md`
- **Technical Implementation**: See `docs/CHRONOLOG_SYSTEM_SPECIFICATION.md`
- **Getting Started**: See `QUICK_START.md` (provenance section)

---

**💡 Pro Tip**: Each analysis run creates a complete package in `results/{timestamp}/` with all files needed for that specific run. Start there for most questions! 