# Experiment Run Manifest: vanderveen_binary_test

**Generated**: 2025-07-23 03:55:32 UTC  
**Total Artifacts**: 4

## Artifact Overview

| SHA256 (12 chars) | Task Type | Original Filename | Timestamp |
|-------------------|-----------|-------------------|-----------|
| `595a2ee6521b...` | framework | framework.md | 2025-07-23 03:55:32 |
| `fd506a89920a...` | corpus | us.2016.Trump.Announcement.6-16.docx | 2025-07-23 03:55:32 |
| `b18912729e9e...` | corpus | us.2016.Sanders.Announcement.5-26.docx | 2025-07-23 03:55:32 |
| `5deca64480ad...` | corpus | us.2016.DemocraticPartyPlatform.pdf | 2025-07-23 03:55:32 |

## Provenance Chain

This manifest provides complete artifact traceability for academic reproducibility:

- **Content-Addressable Storage**: All artifacts stored by SHA256 hash
- **Parent Relationships**: `parent_sha256` tracks derivation chains
- **Task Classification**: `task_type` identifies processing stage
- **Temporal Ordering**: `timestamp` provides execution chronology

## File Reconstruction

Original files can be reconstructed from MinIO storage:

```bash
# Retrieve framework.md
python3 scripts/minio_client.py get 595a2ee6521b49abedde85faa073e0514d8f18c7da108b28b611f9c8de16c2a3 framework.md
# Retrieve us.2016.Trump.Announcement.6-16.docx
python3 scripts/minio_client.py get fd506a89920a9e8e3a9509d02d3c23ebfc0bf70cd4273784fae44d29b2609c33 us.2016.Trump.Announcement.6-16.docx
# Retrieve us.2016.Sanders.Announcement.5-26.docx
python3 scripts/minio_client.py get b18912729e9ec955f9786d384807667f6589c8e3d6003cb7dd144ea5577537d4 us.2016.Sanders.Announcement.5-26.docx
# Retrieve us.2016.DemocraticPartyPlatform.pdf
python3 scripts/minio_client.py get 5deca64480ad04bcd1ff09bbb8aaaef8bd05a2c6084bd7e9289995be42085a0f us.2016.DemocraticPartyPlatform.pdf
```
