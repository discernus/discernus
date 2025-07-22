# Workflow Security Architecture
**Preventing Agent Access Outside Project Boundaries**

## 🎯 **Security Principle**

**Agents must NEVER access files outside the project directory where the experiment.md file is located.**

This prevents:
- ✅ Accidental `.env` file exposure  
- ✅ Cross-project data contamination
- ✅ Massive corpus explosions (4,077 vs 7 files)
- ✅ System file access by malicious experiments

## 🏗️ **Architecture Components**

### 1. Project Boundary Enforcement
```python
class ProjectSecurityBoundary:
    """Enforces strict project directory boundaries for all agent operations."""
    
    def __init__(self, experiment_file_path: str):
        self.project_root = Path(experiment_file_path).parent.resolve()
        self.allowed_paths = [
            self.project_root / "framework.md",
            self.project_root / "experiment.md", 
            self.project_root / "corpus",
            self.project_root / "experiments",
            self.project_root / "results",
            self.project_root / "logs"
        ]
    
    def validate_path_access(self, requested_path: str) -> bool:
        """Returns True only if path is within project boundaries."""
        requested = Path(requested_path).resolve()
        
        # Must be within project root
        try:
            requested.relative_to(self.project_root)
        except ValueError:
            return False
            
        # Must be in allowed subdirectories
        return any(
            str(requested).startswith(str(allowed)) 
            for allowed in self.allowed_paths
        )
```

### 2. Secure Agent Base Class
```python
class SecureAgent:
    """Base class that enforces project boundary security for all agents."""
    
    def __init__(self, project_boundary: ProjectSecurityBoundary):
        self.security_boundary = project_boundary
    
    def secure_path_access(self, path: str) -> Path:
        """Validates path access and returns secure Path object."""
        if not self.security_boundary.validate_path_access(path):
            raise SecurityError(
                f"🚨 SECURITY VIOLATION: Agent attempted to access {path} "
                f"outside project boundary {self.security_boundary.project_root}"
            )
        return Path(path)
    
    def secure_glob(self, base_path: str, pattern: str = "*") -> List[Path]:
        """Secure glob that only returns files within project boundaries."""
        base = self.secure_path_access(base_path)
        files = []
        for file in base.rglob(pattern):
            if self.security_boundary.validate_path_access(str(file)):
                files.append(file)
        return files
```

### 3. Enhanced AnalysisAgent Security
```python
class AnalysisAgent(SecureAgent):
    """Analysis agent with enforced project boundary security."""
    
    def execute(self, workflow_state: Dict[str, Any], step_config: Dict[str, Any]) -> Dict[str, Any]:
        # Initialize security boundary from project path
        project_path = workflow_state.get('project_path', '')
        security_boundary = ProjectSecurityBoundary(project_path + "/experiment.md")
        super().__init__(security_boundary)
        
        # Secure corpus access
        corpus_path = workflow_state.get('corpus_path', '')
        corpus_files = self.secure_glob(corpus_path, "*")
        
        # Only process files within security boundary
        safe_corpus_files = [
            f for f in corpus_files 
            if f.suffix in ['.txt', '.md', '.docx', '.pdf']
        ]
        
        print(f"🛡️ Security: Processing {len(safe_corpus_files)} files within project boundary")
        print(f"🛡️ Security: Project root = {self.security_boundary.project_root}")
```

## 🔒 **Implementation Safeguards**

### 1. CLI-Level Validation
```python
# In discernus_cli.py execute command
def execute(experiment_file: str, dev_mode: bool, researcher_profile: str):
    experiment_path = Path(experiment_file).resolve()
    
    # Validate experiment file is in a reasonable location
    if not _is_safe_experiment_location(experiment_path):
        click.secho("🚨 Security Error: Experiment file in unsafe location", fg='red')
        sys.exit(1)
    
    # Initialize security boundary
    security_boundary = ProjectSecurityBoundary(str(experiment_path))
    
    # Pass security context to analyst
    analyst = ProjectCoherenceAnalyst(security_boundary=security_boundary)
```

### 2. WorkflowOrchestrator Security Integration
```python
class WorkflowOrchestrator:
    def __init__(self, project_path: str, security_boundary: ProjectSecurityBoundary):
        self.project_path = Path(project_path)
        self.security_boundary = security_boundary
        
        # Validate orchestrator project path matches security boundary
        if self.project_path.resolve() != security_boundary.project_root:
            raise SecurityError("Project path mismatch with security boundary")
    
    def _create_agent_instance(self, agent_def: Dict[str, Any]) -> Any:
        # Inject security boundary into all agents
        agent_class = self._load_agent_class(agent_def)
        
        if issubclass(agent_class, SecureAgent):
            return agent_class(security_boundary=self.security_boundary)
        else:
            # Legacy agents get security boundary via workflow state
            return agent_class()
```

## 📚 **Documentation Requirements**

### 1. Agent Development Guidelines
- **All new agents MUST inherit from `SecureAgent`**
- **File access MUST use `secure_path_access()` or `secure_glob()`**
- **NO direct `Path().rglob()` calls outside security framework**

### 2. Security Testing Requirements
```python
def test_agent_security_boundary():
    """Test that agents cannot access files outside project directory."""
    
    # Create test project
    with tempfile.TemporaryDirectory() as temp_dir:
        project_dir = Path(temp_dir) / "test_project"
        project_dir.mkdir()
        
        # Create files inside and outside project
        (project_dir / "experiment.md").write_text("test")
        (project_dir / "corpus" / "safe.txt").write_text("safe content")
        
        outside_file = Path(temp_dir) / "secret.txt"
        outside_file.write_text("SECRET CONTENT")
        
        # Test security boundary
        boundary = ProjectSecurityBoundary(str(project_dir / "experiment.md"))
        
        # Should allow project files
        assert boundary.validate_path_access(str(project_dir / "corpus" / "safe.txt"))
        
        # Should block outside files  
        assert not boundary.validate_path_access(str(outside_file))
```

## 🚨 **Migration Plan**

### Phase 1: Core Security Infrastructure (Immediate)
1. Create `ProjectSecurityBoundary` class
2. Create `SecureAgent` base class  
3. Add security validation to CLI

### Phase 2: Agent Migration (Sprint)
1. Update `AnalysisAgent` to use security boundary
2. Update other file-accessing agents
3. Add security tests for all agents

### Phase 3: Validation & Hardening (Ongoing)
1. Comprehensive security testing
2. Penetration testing with malicious experiments
3. Documentation and training updates

## 🎯 **Success Criteria**

- ✅ **No agent can access files outside project directory**
- ✅ **Security violations throw clear exceptions with helpful messages**
- ✅ **All file access goes through security validation**
- ✅ **Comprehensive test coverage for security boundaries**
- ✅ **Zero regression risk - existing experiments continue working**

This architecture prevents the "biggest regression witnessed" from ever happening again while maintaining the THIN philosophy and research workflow integrity. 