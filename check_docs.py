import requests

API_BASE = 'http://localhost:8000/api'

# Check all corpora
print('=== All Corpora ===')
response = requests.get(f'{API_BASE}/corpora')
if response.status_code == 200:
    corpora = response.json()
    for corpus in corpora:
        print(f"Corpus {corpus['id']}: {corpus['name']} (records: {corpus['record_count']})")
        
        # Check documents for each corpus
        doc_response = requests.get(f'{API_BASE}/corpora/{corpus["id"]}/documents')
        if doc_response.status_code == 200:
            docs = doc_response.json()
            print(f"  Documents ({len(docs)}):")
            for doc in docs:
                print(f"    - {doc['text_id']}: {doc['title']}")
        else:
            print(f"  No documents (status: {doc_response.status_code})")
        print()
else:
    print(f'❌ Failed to get corpora: {response.status_code}') 