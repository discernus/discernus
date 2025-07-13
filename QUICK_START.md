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

The system is designed to be simple and self-configuring. No complex bootstrap process needed! 