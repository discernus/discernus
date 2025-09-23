#!/usr/bin/env python3
import yaml
import re

with open('projects/2b_cff_cohesive_flourishing/experiment.md', 'r') as f:
    content = f.read()

print("Looking for YAML patterns...")

# Try the first pattern
yaml_match = re.search(r'```yaml\n(.*?)```', content, re.DOTALL)
if yaml_match:
    print("Found ```yaml``` pattern")
    yaml_content = yaml_match.group(1)
else:
    print("No ```yaml``` pattern found")
    # Try the second pattern
    yaml_match = re.search(r'---\n(.*?)\n---', content, re.DOTALL)
    if yaml_match:
        print("Found --- pattern")
        yaml_content = yaml_match.group(1)
    else:
        print("No --- pattern found either")

if yaml_match:
    print('YAML content found:')
    print(repr(yaml_content))
    try:
        config = yaml.safe_load(yaml_content)
        print('Parsed config:')
        print(config)
        components = config.get('components', {})
        print('Components:')
        print(components)
        framework_filename = components.get('framework')
        corpus_filename = components.get('corpus')
        print(f'Framework: {framework_filename}')
        print(f'Corpus: {corpus_filename}')
    except Exception as e:
        print(f'YAML parsing error: {e}')
else:
    print('No YAML match found')
