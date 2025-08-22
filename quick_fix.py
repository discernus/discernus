#!/usr/bin/env python3

# Read the file
with open('../../frameworks/reference/flagship/pdaf_v10.md', 'r') as f:
    content = f.read()

# Fix all remaining scoring calibrations
replacements = [
    ('high: "0.8-1.0"', 'high: "0.8-1.0: Strong opposition rejection, clear legitimacy denial, exclusionary language"'),
    ('medium: "0.5-0.7"', 'medium: "0.5-0.7: Moderate opposition rejection, some legitimacy denial, limited exclusion"'),
    ('low: "0.1-0.4"', 'low: "0.1-0.4: Weak opposition rejection hints, minimal exclusionary language"'),
    ('absent: "0.0"', 'absent: "0.0: No opposition rejection, legitimacy denial, or exclusionary language"'),
]

# Apply replacements
for old, new in replacements:
    content = content.replace(old, new)

# Write back
with open('../../frameworks/reference/flagship/pdaf_v10.md', 'w') as f:
    f.write(content)

print("✅ Quick fix applied!")
