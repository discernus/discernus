# Release Process Guide

This document outlines the standardized release process for the Narrative Gravity Wells project.

## 🎯 Release Types

### **Patch Release** (X.Y.Z → X.Y.Z+1)
- **Purpose**: Bug fixes, minor improvements, documentation updates
- **Examples**: Fix broken imports, correct typos, update dependencies
- **Breaking Changes**: None
- **Timeline**: As needed

### **Minor Release** (X.Y.Z → X.Y+1.0)
- **Purpose**: New features, non-breaking enhancements
- **Examples**: New analysis frameworks, UI improvements, API endpoints
- **Breaking Changes**: None (backward compatible)
- **Timeline**: Monthly or when significant features are ready

### **Major Release** (X.Y.Z → X+1.0.0)
- **Purpose**: Breaking changes, major architecture updates
- **Examples**: Database schema changes, API redesigns, package restructuring
- **Breaking Changes**: Yes (may require user action)
- **Timeline**: Quarterly or when breaking changes are necessary

## 🚀 Automated Release Process

### Quick Start
```bash
# Test the release process (safe)
python scripts/release.py --dry-run patch --message "Test release process"

# Perform actual releases
python scripts/release.py patch --message "Bug fixes and documentation updates"
python scripts/release.py minor --message "New multi-framework analysis capabilities"
python scripts/release.py major --message "Database architecture restructuring"
```

### What the Script Does

#### 🔍 **Pre-release Checks**
1. **Git Status**: Ensures repository is clean with no uncommitted changes
2. **File Hygiene**: Verifies proper project organization (no files in root)
3. **Test Suite**: Runs complete test suite with coverage
4. **Documentation**: Verifies all required docs exist and are complete

#### 📝 **Version Management**
1. **Current Version**: Extracts from CHANGELOG.md
2. **New Version**: Calculates based on semantic versioning rules
3. **CHANGELOG Update**: Adds new version entry with release date
4. **Git Operations**: Commits, tags, and pushes changes

#### ✅ **Success Verification**
- All tests pass (100% requirement)
- Documentation is complete
- Git operations succeed
- Release summary generated

## 📋 Manual Release Checklist

For manual oversight or when automated script isn't available:

### Pre-Release (Required)
- [ ] **Code Quality**
  - [ ] All tests pass: `pytest -v`
  - [ ] No linting errors: `flake8 src/`
  - [ ] Code coverage acceptable: `pytest --cov=src`
  
- [ ] **File Hygiene**
  - [ ] Root directory clean (only operational files)
  - [ ] No temporary files (*.tmp, *.bak, *~)
  - [ ] Proper directory organization followed
  - [ ] No debug print statements or commented code

- [ ] **Documentation**
  - [ ] README.md up to date
  - [ ] CHANGELOG.md has [Unreleased] section with changes
  - [ ] API documentation current
  - [ ] User guides reflect new features

- [ ] **Git Repository**
  - [ ] All changes committed
  - [ ] Working directory clean
  - [ ] On main/master branch
  - [ ] Pulled latest changes

### Release Execution
- [ ] **Version Planning**
  - [ ] Determine release type (patch/minor/major)
  - [ ] Calculate new version number
  - [ ] Write clear release message

- [ ] **CHANGELOG Update**
  - [ ] Move changes from [Unreleased] to new version
  - [ ] Add release date
  - [ ] Create new [Unreleased] section

- [ ] **Git Operations**
  - [ ] Stage all changes: `git add .`
  - [ ] Commit with version: `git commit -m "Release vX.Y.Z: message"`
  - [ ] Create annotated tag: `git tag -a vX.Y.Z -m "Release vX.Y.Z"`
  - [ ] Push changes: `git push`
  - [ ] Push tags: `git push --tags`

### Post-Release
- [ ] **Verification**
  - [ ] Verify tag appears on GitHub/GitLab
  - [ ] Check CHANGELOG.md rendered correctly
  - [ ] Test that release can be cloned and launched

- [ ] **Communication**
  - [ ] Update team/stakeholders if applicable
  - [ ] Document any deployment steps needed
  - [ ] Monitor for immediate issues

## 🔧 Release Script Configuration

### Environment Setup
```bash
# Ensure script dependencies
pip install -r requirements.txt

# Make script executable
chmod +x scripts/release.py

# Test script works
python scripts/release.py --help
```

### Customization Options

#### **Allowed Root Files** (Modify in script if needed)
```python
allowed_root_files = {
    'README.md', 'CHANGELOG.md', 'LICENSE', 
    'launch.py', 'launch_streamlit.py', 'check_database.py',
    'requirements.txt', 'env.example', 'alembic.ini',
    'pytest.ini', '.gitignore', '.cursorrules'
}
```

#### **Required Documentation**
```python
required_docs = [
    'README.md',
    'CHANGELOG.md', 
    'LAUNCH_GUIDE.md',
    'docs/development/CONTRIBUTING.md',
    'docs/architecture/database_architecture.md'
]
```

## 🚨 Troubleshooting

### Common Issues

#### **"Repository has uncommitted changes"**
```bash
# Check what's uncommitted
git status

# Commit or stash changes
git add .
git commit -m "Prepare for release"
# OR
git stash
```

#### **"Test suite failed"**
```bash
# Run tests to see specific failures
pytest -v

# Fix failing tests before release
# All tests must pass for release
```

#### **"File hygiene check failed"**
```bash
# Check what files are in root
ls -la

# Move files to appropriate directories
mv temp_file.txt tmp/2025_06_09/
mv test_script.py scripts/
```

#### **"Documentation missing"**
```bash
# Check which docs are missing
find docs/ -name "*.md" -type f

# Create missing documentation
# Update existing docs to be current
```

### Recovery Procedures

#### **Undo Last Release** (if just tagged)
```bash
# Remove local tag
git tag -d vX.Y.Z

# Remove remote tag (if already pushed)
git push origin :refs/tags/vX.Y.Z

# Reset to previous commit
git reset --hard HEAD~1
```

#### **Fix Release Issues**
```bash
# For post-release fixes
python scripts/release.py patch --message "Fix release issue: description"
```

## 📊 Release Metrics

### Success Criteria
- **Test Coverage**: > 95%
- **Test Pass Rate**: 100%
- **Documentation Coverage**: All required docs present
- **File Hygiene**: Zero violations
- **Git Cleanliness**: No uncommitted changes

### Release Frequency Guidelines
- **Patch**: As needed (bugs, urgent fixes)
- **Minor**: Monthly or bi-weekly (new features)
- **Major**: Quarterly (breaking changes, major updates)

### Version History Tracking
All releases are tracked in:
- **CHANGELOG.md**: Human-readable change descriptions
- **Git Tags**: Machine-readable version markers
- **Release Summary**: Generated post-release report

## 🎉 Release Announcement Template

```markdown
# Release v{version} - {title}

## 🚀 What's New
- {feature descriptions}

## 🔧 Improvements  
- {improvement descriptions}

## 🐛 Bug Fixes
- {bug fix descriptions}

## 📋 Upgrade Instructions
{any required upgrade steps}

## 🙏 Contributors
{acknowledge contributors}
```

This standardized process ensures consistent, high-quality releases with comprehensive verification and proper documentation. 