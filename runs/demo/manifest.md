# Experiment Run Manifest: demo

**Generated**: 2025-07-23 11:07:26 UTC  
**Total Artifacts**: 2

## Artifact Overview

| SHA256 (12 chars) | Task Type | Original Filename | Timestamp |
|-------------------|-----------|-------------------|-----------|
| `1e0d641f0919...` | framework | demo_framework.md | 2025-07-23 11:07:26 |
| `fb57e94e58b0...` | corpus | demo_doc.txt | 2025-07-23 11:07:26 |

## Provenance Chain

This manifest provides complete artifact traceability for academic reproducibility:

- **Content-Addressable Storage**: All artifacts stored by SHA256 hash
- **Parent Relationships**: `parent_sha256` tracks derivation chains
- **Task Classification**: `task_type` identifies processing stage
- **Temporal Ordering**: `timestamp` provides execution chronology

## File Reconstruction

Original files can be reconstructed from MinIO storage:

```bash
# Retrieve demo_framework.md
python3 scripts/minio_client.py get 1e0d641f0919b8ca61f8328e0fbd12b15cdacf67d6916955044190b1c522c70d demo_framework.md
# Retrieve demo_doc.txt
python3 scripts/minio_client.py get fb57e94e58b0323798b5f9b75f9a394f54a7047c3733db6d5548e2de116c3ebb demo_doc.txt
```
