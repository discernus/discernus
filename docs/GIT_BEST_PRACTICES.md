# Git Best Practices for Discernus Research
**Preventing Nested Repository Issues**

## ⚠️ Critical Rule: Never Run `git init` in Project Subdirectories

### Why This Matters
- **GitHub is our persistence layer** for research provenance
- **Chronolog system** requires all files in the main repository
- **Nested repositories break academic integrity** tracking
- **Peer review becomes impossible** without complete audit trail

### ❌ What NOT to Do
```bash
# NEVER do this in experiment directories:
cd projects/my_experiment/
git init  # ❌ This breaks everything!

# NEVER do this in any subdirectory:
cd results/some_analysis/
git init  # ❌ This breaks provenance!
```

### ✅ What TO Do Instead
```bash
# Always work from the main repository:
cd /path/to/discernus/
git add projects/my_experiment/
git commit -m "Add new experiment"

# All experiment files belong in main repo:
git add projects/my_experiment/framework.md
git add projects/my_experiment/experiment.md
git add projects/my_experiment/results/
git commit -m "Complete experiment analysis"
```

### 🔧 If You Accidentally Created Nested Repos
```bash
# Scan for problems:
python3 scripts/prevent_nested_repos.py --scan

# Clean them up:
python3 scripts/prevent_nested_repos.py --clean --confirm

# Add files to main repo:
git add .
git commit -m "Fix nested repository issue"
```

### 🛡️ Prevention System
- **Git hooks** automatically detect nested repos before commit
- **Scanning script** finds existing problems
- **Cleanup script** removes nested repos safely
- **.gitignore patterns** prevent common mistakes

### 📚 Academic Integrity Impact
When nested repositories exist:
- **Chronolog events** get logged but files don't get committed
- **Provenance chain** breaks between logs and actual files
- **Peer reviewers** can't verify complete research record
- **Replication** becomes impossible due to missing files

### 🆘 Emergency Recovery
If you've lost work due to nested repos:
1. **Don't panic** - files are still on disk
2. **Run cleanup script** to remove nested .git directories
3. **Add all files** to main repository: `git add .`
4. **Commit everything** to restore provenance
5. **Verify chronolog** integrity with scanning tools

### 💡 Pro Tips
- **Use git status** regularly to see what's tracked
- **Check for nested repos** before major commits
- **Keep experiments** in projects/ directory structure
- **Let chronolog system** handle all git operations automatically

Remember: The entire academic integrity system depends on having a single, unified git repository with complete provenance tracking.
