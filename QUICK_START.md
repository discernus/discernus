# SOAR Quick Start Guide

## Running Experiments (Simple & Direct)

### Prerequisites
```bash
# Activate venv
source venv/bin/activate

# Install dependencies (if needed)
pip install -r requirements.txt

# Start Redis (if not running)
brew services start redis
```

### Run Any Experiment
```bash
# General pattern (works with descriptive filenames)
python3 -c "
from discernus.agents.validation_agent import ValidationAgent
agent = ValidationAgent()
agent.validate_and_execute_sync('path/to/framework.md', 'path/to/experiment.md', 'path/to/corpus')
"

# Example: Run Attesor smoke test
python3 -c "
from discernus.agents.validation_agent import ValidationAgent
agent = ValidationAgent()
agent.validate_and_execute_sync(
    'projects/attesor/experiments/01_smoketest/pdaf_v1.1_sanitized_framework.md',
    'projects/attesor/experiments/01_smoketest/smoketest_experiment.md', 
    'projects/attesor/experiments/01_smoketest/corpus'
)
"
```

### That's It!

**No bootstrap needed** - components handle their own initialization:
- ✅ LLM clients initialize automatically
- ✅ Redis connects with graceful fallback
- ✅ ConversationLogger handles missing dependencies
- ✅ All error handling built-in

### Troubleshooting

**Redis not running?**
```bash
brew services start redis
```

**Missing dependencies?**
```bash
pip install -r requirements.txt
```

**Wrong directory?**
```bash
cd /Volumes/dev/discernus
```

**Want to check if everything works?**
```bash
# Run Attesor smoke test (5 minutes, ~$0.50)
python3 -c "
from discernus.agents.validation_agent import ValidationAgent
agent = ValidationAgent()
agent.validate_and_execute_sync(
    'projects/attesor/experiments/01_smoketest/pdaf_v1.1_sanitized_framework.md',
    'projects/attesor/experiments/01_smoketest/smoketest_experiment.md', 
    'projects/attesor/experiments/01_smoketest/corpus'
)
"
```

## Research Provenance and Academic Integrity

### Understanding the Three-Tier Audit Trail
Every analysis automatically creates **complete provenance records** for academic integrity:

1. **Project Chronolog** (`PROJECT_CHRONOLOG_attesor.jsonl`): All events across all sessions
2. **Run Chronolog** (`results/{timestamp}/RUN_CHRONOLOG_{session}.jsonl`): Events for single run
3. **Conversation Files** (`conversations/conversation_{timestamp}_{id}.jsonl`): LLM content

### Quick Verification
```bash
# Verify chronolog integrity
python3 -c "
from discernus.core.project_chronolog import get_project_chronolog
chronolog = get_project_chronolog('projects/attesor')
result = chronolog.verify_integrity()
print(f'Verified: {result[\"verified\"]} events: {result[\"verified_events\"]}')
"

# List all analysis sessions
python3 -c "
from discernus.core.project_chronolog import get_project_chronolog
chronolog = get_project_chronolog('projects/attesor')
for session in chronolog.list_sessions():
    print(f'{session[\"session_id\"]}: {session[\"event_count\"]} events')
"
```

### For Academic Publication
- **Results package**: Each run creates complete replication package in `results/{timestamp}/`
- **Integrity verification**: HMAC-SHA256 signatures on all chronolog events
- **Statistical analysis**: Run chronologs enable Cronbach's alpha across multiple runs
- **Complete documentation**: See `docs/RESEARCH_PROVENANCE_GUIDE.md` for full academic workflows

---

The system is designed to be simple and self-configuring. No complex bootstrap process needed! 