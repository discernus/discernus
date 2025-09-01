#!/usr/bin/env python3
import yaml

# Read the corpus file
with open('corpus.md', 'r') as f:
    content = f.read()

# Find the YAML section
yaml_start = content.find('```yaml')
yaml_end = content.find('```', yaml_start + 1)

if yaml_start != -1 and yaml_end != -1:
    yaml_content = content[yaml_start + 7:yaml_end].strip()

    try:
        parsed = yaml.safe_load(yaml_content)
        print('✅ YAML syntax is valid')
        print(f'📊 Found {len(parsed["documents"])} documents')

        # Check for required grouping variables
        docs = parsed['documents']
        required_fields = ['pre_post_stabbing', 'electoral_proximity']
        missing_fields = []

        for doc in docs:
            for field in required_fields:
                if field not in doc:
                    missing_fields.append(f'{doc["filename"]} missing {field}')

        if missing_fields:
            print(f'❌ Missing grouping variables: {len(missing_fields)} issues')
            for issue in missing_fields[:5]:  # Show first 5
                print(f'  - {issue}')
        else:
            print('✅ All required grouping variables present')

    except yaml.YAMLError as e:
        print(f'❌ YAML syntax error: {e}')

else:
    print('❌ Could not find YAML section markers')

