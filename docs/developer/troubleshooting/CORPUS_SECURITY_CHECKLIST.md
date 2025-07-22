# Corpus Security Checklist
**Preventing the "4,077 Files vs 7 Files" Regression**

## 🚨 **Quick Security Check**

Before running any experiment, verify these basics:

### ✅ **Pre-Flight Checklist**
```bash
# 1. Verify experiment location
ls -la projects/your_experiment/
# Should show: experiment.md, framework.md, corpus/

# 2. Count corpus files (should be reasonable number)
find projects/your_experiment/corpus -type f | wc -l
# Should be: 7-50 files, NOT thousands

# 3. Check for .env exposure risk
find . -name ".env*" -not -path "./pm/ancient_archives/*"
# Should show: ./.env (project root only)

# 4. Verify no nested repositories
python3 scripts/prevent_nested_repos.py --scan
# Should show: ✅ No nested repositories found
```

### ❌ **Red Flags - STOP IMMEDIATELY**
- Corpus count > 1000 files
- `.env` files in multiple locations  
- Nested git repositories detected
- Experiment file outside `projects/` directory

## 🛡️ **Agent Security Validation**

### **For Developers: Agent Code Review**
```python
# ❌ DANGEROUS - Direct path access
corpus_files = [f for f in Path(corpus_path).rglob('*') if f.is_file()]

# ✅ SECURE - Validated path access  
corpus_files = self.secure_glob(corpus_path, "*")
```

### **For Users: Runtime Monitoring**
```bash
# Monitor what files are being processed
tail -f projects/your_experiment/logs/session_*/session_run.log | grep "Processing"

# Should see lines like:
# 🛡️ Security: Processing 7 files within project boundary
# 🛡️ Security: Project root = /path/to/projects/your_experiment
```

## 🔍 **Common Security Violations**

### **1. Corpus Path Confusion**
**Problem**: Agent gets wrong corpus path, scans everything
```python
# Missing corpus_path in workflow_state
corpus_path = Path(workflow_state.get('corpus_path', ''))  # Empty!
# Falls back to scanning project root → 4,077 files
```

**Solution**: Always verify `corpus_path` is explicitly set
```python
corpus_path = workflow_state.get('corpus_path')
if not corpus_path:
    raise ValueError("❌ corpus_path not provided in workflow_state")
```

### **2. Relative Path Confusion**
**Problem**: Relative paths escape project boundaries
```python
# Dangerous relative path
corpus_path = "../../sensitive_data/"  # Escapes project!
```

**Solution**: Always resolve and validate paths
```python
corpus_path = Path(corpus_path).resolve()
if not str(corpus_path).startswith(str(project_root)):
    raise SecurityError("🚨 Corpus path outside project boundary")
```

### **3. Symlink Attacks**
**Problem**: Symlinks can point outside project directory
```bash
# Malicious symlink in corpus
ln -s /etc/passwd projects/experiment/corpus/secrets.txt
```

**Solution**: Resolve symlinks and validate final paths
```python
def validate_path_access(self, requested_path: str) -> bool:
    requested = Path(requested_path).resolve()  # Resolves symlinks
    try:
        requested.relative_to(self.project_root)
        return True
    except ValueError:
        return False
```

## 📋 **Testing Your Security Implementation**

### **Unit Test Template**
```python
def test_corpus_security_boundary():
    """Test that agents respect project boundaries."""
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create project structure
        project = Path(temp_dir) / "test_project"
        (project / "corpus").mkdir(parents=True)
        (project / "corpus" / "safe.txt").write_text("safe")
        
        # Create files outside project
        outside = Path(temp_dir) / "secret.txt"
        outside.write_text("SECRET")
        
        # Test security boundary
        boundary = ProjectSecurityBoundary(str(project / "experiment.md"))
        
        # Should allow project files
        assert boundary.validate_path_access(str(project / "corpus" / "safe.txt"))
        
        # Should block outside files
        assert not boundary.validate_path_access(str(outside))
        
        # Test agent with security
        agent = AnalysisAgent(security_boundary=boundary)
        corpus_files = agent.secure_glob(str(project / "corpus"))
        
        # Should only find project files
        assert len(corpus_files) == 1
        assert corpus_files[0].name == "safe.txt"
```

### **Integration Test**
```python
def test_full_experiment_security():
    """Test complete experiment respects boundaries."""
    
    # Run experiment in isolated directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Set up test project
        setup_test_project(temp_dir)
        
        # Add decoy files outside project
        create_decoy_files(temp_dir)
        
        # Run experiment
        result = run_experiment(temp_dir + "/test_project/experiment.md")
        
        # Verify only project files were processed
        processed_files = extract_processed_files(result)
        assert all(f.startswith(temp_dir + "/test_project/") for f in processed_files)
        assert len(processed_files) < 20  # Reasonable corpus size
```

## 🚨 **Incident Response**

### **If Security Violation Detected**
1. **STOP** the experiment immediately
2. **Check logs** for what files were accessed
3. **Verify** no sensitive data was processed
4. **Fix** the security boundary issue
5. **Re-run** with proper boundaries

### **If .env File Exposed**
1. **Rotate** all API keys immediately
2. **Check** LLM provider logs for suspicious activity  
3. **Audit** session logs for sensitive data
4. **Update** security documentation
5. **Add** prevention measures

## 📚 **Additional Resources**

- [Workflow Security Architecture](WORKFLOW_SECURITY_ARCHITECTURE.md) - Complete security framework
- [Git Best Practices](../workflows/GIT_BEST_PRACTICES.md) - Preventing nested repos
- [Agent Development Guidelines](../workflows/AGENT_DEVELOPMENT_GUIDE.md) - Secure coding practices

## 🎯 **Security Mantras**

1. **"Trust but Verify"** - Always validate paths before access
2. **"Principle of Least Privilege"** - Only access what's needed
3. **"Defense in Depth"** - Multiple security layers
4. **"Fail Securely"** - When in doubt, block access
5. **"Audit Everything"** - Log all file access for review

Remember: The biggest security threat is often the simplest mistake. A missing `corpus_path` parameter turned into a 4,077-file exposure risk. Stay vigilant! 