# Infrastructure Troubleshooting Guide
*Prevents the $0.50 debugging dance that wastes Cursor agent cycles*

## **Quick Resolution Commands**

```bash
# Start everything (most common solution)
make start-infra

# Test infrastructure status
make check
lsof -i :9000    # MinIO should be running
lsof -i :9001    # MinIO console
pgrep redis      # Redis (optional)

# Run experiment correctly
make run-direct EXPERIMENT=projects/your_experiment
```

## **Common Issues & Solutions**

### **❌ "MinIO connection failed: HTTPConnectionPool"**

**Symptom**: 
```
❌ Artifact storage error: MinIO connection failed: 
HTTPConnectionPool(host='localhost', port=9000): Max retries exceeded
```

**Root Cause**: MinIO server not running

**Solution**:
```bash
# Automatic fix
make start-infra

# Manual fix (if needed)
mkdir -p ~/minio-data
MINIO_ROOT_USER=minio MINIO_ROOT_PASSWORD=minio123 \
minio server ~/minio-data --console-address ":9001" &
```

**Prevention**: Always run `make start-infra` before development

---

### **❌ "Experiment hangs in orchestrator queue"**

**Symptom**:
```
📊 Infrastructure Status:
   📥 Orchestrator queue: 1 tasks
   ⚙️  Worker queue: 0 tasks
   ✅ Completed: 0 tasks
```

**Root Cause**: Using legacy CLI that requires Redis workers

**Solution**:
```bash
# Use THIN v2.0 direct orchestration instead
make run-direct EXPERIMENT=projects/your_experiment

# Or manually:
python3 -c "
from discernus.core.thin_orchestrator import ThinOrchestrator
from pathlib import Path
ThinOrchestrator(Path('projects/your_experiment')).run_experiment()
"
```

**Prevention**: Use direct orchestration, not `discernus/cli.py run`

---

### **❌ "Input token count exceeds maximum"**

**Symptom**:
```
"The input token count (1409470) exceeds the maximum number of tokens allowed (1048576)."
```

**Root Cause**: Context window limits, NOT rate limiting

**Analysis**:
- **Gemini 2.5 Flash**: 1M token limit (~47 presidential speeches)
- **Gemini 2.5 Pro**: 2M token limit (use for larger batches)

**Solutions**:
1. **Reduce batch size**: Use fewer documents
2. **Switch to Pro model**: Edit model string in orchestrator
3. **Implement batching**: Break large corpus into smaller chunks

**Key Insight**: This is a context management issue, not a rate limiting issue

---

### **❌ "Redis connection errors"**

**Symptom**: Redis connection failures when using CLI

**Root Cause**: Redis not running or CLI using deprecated orchestration

**Solution**:
```bash
# Option 1: Start Redis (for legacy CLI)
redis-server --daemonize yes

# Option 2: Use direct orchestration (recommended)
make run-direct EXPERIMENT=projects/your_experiment
```

**Prevention**: Migrate to THIN v2.0 direct orchestration

---

## **Architecture Understanding**

### **THIN v2.0 vs Legacy CLI**

| Approach | Method | Status | Use Case |
|----------|--------|--------|----------|
| **THIN v2.0** | Direct function calls | ✅ Current | Development & Production |
| **Legacy CLI** | Redis orchestration | ⚠️ Deprecated | Legacy compatibility only |

### **Required Services**

| Service | Port | Required | Purpose |
|---------|------|----------|---------|
| **MinIO** | 9000 | ✅ Always | Artifact storage & provenance |
| **MinIO Console** | 9001 | ℹ️ Optional | Web UI for storage management |
| **Redis** | 6379 | ⚠️ Legacy CLI only | Deprecated orchestration |

### **Storage Architecture**

```
Experiment Files → MinIO (localhost:9000) → Content-addressable hashes
                                          ↓
                  Provenance & Audit Trails → Run folders
```

## **Debugging Workflow**

### **1. Environment Check**
```bash
make check                    # Verify Python environment
source venv/bin/activate      # Ensure venv active
python3 --version            # Should be 3.13.5
```

### **2. Infrastructure Check**
```bash
make start-infra             # Start all services
lsof -i :9000               # MinIO running?
curl -s http://localhost:9000/minio/health/live  # MinIO responding?
```

### **3. Test Connection**
```bash
python3 -c "
from discernus.storage.minio_client import get_default_client
client = get_default_client()
print('✅ MinIO connection successful!')
"
```

### **4. Test Orchestration**
```bash
make run-direct EXPERIMENT=projects/simple_test
```

## **Performance Considerations**

### **Context Window Management**
- **Small batches** (1-10 docs): Any model works
- **Medium batches** (10-25 docs): Use Flash with monitoring
- **Large batches** (25+ docs): Use Pro or implement chunking

### **Cost Optimization**
- **Development/Testing**: Gemini 2.5 Flash ($0.075/1M tokens)
- **Production/Research**: Gemini 2.5 Pro ($1.25/1M tokens)
- **Rate limiting**: LiteLLM handles automatically - no custom logic needed

## **Emergency Recovery**

### **Complete Infrastructure Reset**
```bash
# Stop everything
make stop-infra

# Clean up
rm -rf ~/minio-data
pkill -f minio
pkill redis-server

# Restart
make start-infra
make check
```

### **Test Infrastructure**
```bash
# Quick infrastructure test
make run-direct EXPERIMENT=projects/simple_test
```

## **Key Lessons Learned**

1. **MinIO is required** - never try to bypass it
2. **CLI is deprecated** - use direct orchestration
3. **Context limits ≠ rate limits** - different problems, different solutions
4. **LiteLLM retries work** - no custom batching needed for 429 errors
5. **Infrastructure automation prevents debugging cycles** - always use scripts

## **References**

- **Quick Start**: `CURSOR_AGENT_QUICK_START.md`
- **Architecture**: `docs/architecture/DISCERNUS_SYSTEM_ARCHITECTURE.md`
- **Testing Strategy**: `docs/developer/workflows/TESTING_STRATEGY.md`
- **Makefile**: Root-level automation commands 