#!/usr/bin/env python3
import json

# Load the framework encoding test results
with open('/Volumes/code/discernus/test_thin_approach/artifacts/framework_encoding_test.json', 'r') as f:
    data = json.load(f)

plain_text_cost = data['plain_text_test']['metadata']['usage']['response_cost_usd']
base64_cost = data['base64_test']['metadata']['usage']['response_cost_usd']

plain_text_tokens = data['plain_text_test']['metadata']['usage']['total_tokens']
base64_tokens = data['base64_test']['metadata']['usage']['total_tokens']

print('=== COST COMPARISON ===')
print('Plain Text Framework:')
print(f'  Total tokens: {plain_text_tokens:,}')
print(f'  Cost: ${plain_text_cost:.6f}')
print()
print('Base64 Framework:')
print(f'  Total tokens: {base64_tokens:,}')
print(f'  Cost: ${base64_cost:.6f}')
print()
print('Difference:')
print(f'  Token difference: {base64_tokens - plain_text_tokens:,} tokens')
print(f'  Cost difference: ${base64_cost - plain_text_cost:.6f}')
print(f'  Percentage increase: {((base64_cost - plain_text_cost) / plain_text_cost) * 100:.1f}%')
