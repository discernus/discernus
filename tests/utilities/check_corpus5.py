import requests
response = requests.get('http://localhost:8000/api/corpora/5/documents')
if response.status_code == 200:
    docs = response.json()
    print('Corpus 5 documents:')
    for doc in docs:
        print(f'  - {doc["text_id"]}: {doc["title"]}')
else:
    print(f'No documents in corpus 5: {response.status_code}') 