#!/bin/bash
# Narrative Gravity Auto-Bloat Prevention Startup

# Run on system startup or project activation
cd "/Users/jeffwhatcott/Library/Mobile Documents/com~apple~CloudDocs/Coding Projects/narrative_gravity_analysis"
python3 scripts/production/auto_bloat_prevention.py --startup-check
