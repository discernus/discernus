# AI Agent Guide: GitHub Issues Management
## Proven Methods for AI Agents Working with GitHub

**Status**: ✅ **VERIFIED WORKING** - January 22, 2025  
**Evidence**: Successfully created and managed issues #9-#12 in discernus/discernus repo  
**Agent Tested**: Claude Sonnet 3.5 via Cursor  
**Critical Update**: Added pager bypass fixes for AI agent terminals

---

## ⚡ **Quick Reference for AI Agents**

```bash
# 🚨 ALWAYS use | cat to prevent hanging!
gh issue view 68 | cat

# Authentication fix if needed
unset GITHUB_TOKEN && gh auth status  

# Create issue
gh issue create --title "Title" --body "Body" --label "bug"

# List issues  
gh issue list
```

---

## 🎯 **For AI Agents: YES, YOU CAN DO THIS!**

If another agent told you "I can't create GitHub Issues," they were wrong. Here's exactly how to do it.

---

## 🚨 **CRITICAL: Complete Authentication Reset (When Basic Fixes Fail)**

**When to Use**: If you're getting persistent HTTP 401 errors, authentication conflicts, or mixed SSH/HTTPS protocol issues after trying basic fixes.

**Root Cause**: Conflicting authentication methods - SSH git remotes with HTTPS GitHub CLI, stale environment variables, or conda-related token conflicts.

### **5-Step Complete Reset Procedure** (VERIFIED WORKING)

#### **Step 1: Diagnose the Problem**
```bash
# Check current authentication state
gh auth status

# Check for protocol conflicts  
echo "Git remote:" && git remote -v
echo "SSH connectivity:" && ssh -T git@github.com -o ConnectTimeout=10 -o BatchMode=yes
echo "Environment variables:" && env | grep -i github
```

**Common Conflict Pattern:**
- Git remote: `git@github.com:user/repo.git` (SSH)
- GitHub CLI: `Git operations protocol: https` (HTTPS)
- Result: HTTP 401 errors and authentication confusion

#### **Step 2: Complete Authentication Reset**
```bash
# Logout from GitHub CLI
gh auth logout --hostname github.com || echo "No session to logout"

# Clear conflicting environment variables
unset GITHUB_TOKEN && unset GH_TOKEN && unset GITHUB_USER && unset GH_USER

# Test SSH connectivity (should work independently)
ssh -T git@github.com -o ConnectTimeout=10 -o BatchMode=yes
```

#### **Step 3: Rebuild with Consistent Protocol**
```bash
# Rebuild GitHub CLI authentication using SSH (matches git remote)
gh auth login --hostname github.com --git-protocol ssh --scopes "repo,gist,read:org,workflow"

# This will:
# 1. Upload SSH key to GitHub account
# 2. Configure CLI to use SSH protocol  
# 3. Match git operations protocol
```

#### **Step 4: Verify Consistent Configuration**
```bash
# Verify authentication is working
gh auth status
# Should show: "Git operations protocol: ssh"

# Test GitHub CLI operations
gh issue list --limit 3
gh issue view 9 | cat  # Should work without HTTP 401 errors
```

#### **Step 5: Create Permanent Prevention**
```bash
# Create GitHub CLI config to prevent future conflicts
mkdir -p ~/.config/gh
cat > ~/.config/gh/config.yml << 'EOF'
version: "1"
git_protocol: ssh
pager: cat
hosts:
  github.com:
    git_protocol: ssh
EOF

# Add shell protection (prevents token conflicts)
echo '
# GitHub Authentication Protection
unset GITHUB_TOKEN 2>/dev/null
unset GH_TOKEN 2>/dev/null  
export GH_PAGER="cat"  # Prevent pager hanging
' >> ~/.zshrc
```

### **Success Verification Checklist**
After reset, these should all work without errors:
- [ ] `gh auth status` shows SSH protocol active
- [ ] `gh issue view 9 | cat` works without HTTP 401 
- [ ] `gh issue list` returns results quickly
- [ ] `git fetch --dry-run` works (SSH git operations)
- [ ] No authentication prompts or hanging

### **When This Reset is Needed**
- ✅ **Persistent HTTP 401 errors** despite token clearing
- ✅ **Conda/virtual environment conflicts** with GitHub tokens
- ✅ **Mixed SSH/HTTPS protocol confusion**
- ✅ **Authentication works sometimes but fails randomly**
- ✅ **SSH keys work but GitHub CLI fails**

---

## 🚨 **CRITICAL: Pager Issue Fix**

**Problem**: `gh issue view` commands hang or truncate due to pager (less/more) issues in AI agent terminals.

**Solutions** (use ONE of these):
```bash
# Solution 1: Bypass pager with cat (RECOMMENDED)
gh issue view 68 | cat

# Solution 2: JSON output for parsing
gh issue view 68 --json title,body,state,labels --jq '{title: .title, body: (.body | .[0:200] + "...")}'

# Solution 3: Disable pager globally (if persistent issues)
export PAGER=""
gh issue view 68
```

**Why This Matters**: Without these fixes, issue viewing commands will hang indefinitely, wasting tool calls.

---

## 🔧 **Method 1: GitHub CLI (RECOMMENDED)**

### **Step 1: Check Authentication**
```bash
gh auth status
```

**Expected Success Output:**
```
✓ Logged in to github.com account [username] (keyring)
- Active account: true
```

**Common Problem - Invalid Token Override:**
```
X Failed to log in to github.com using token (GITHUB_TOKEN)
- Active account: true
- The token in GITHUB_TOKEN is invalid.
```

**Fix:**
```bash
unset GITHUB_TOKEN  # Clear invalid environment variable
gh auth status      # Should now show keyring auth working
```

### **Step 2: Create Issues**
```bash
# Basic issue
gh issue create --title "Issue Title" --body "Description text"

# Issue with label
gh issue create --title "Bug Report" --body "Description" --label "bug"

# Issue with multiple labels  
gh issue create --title "Enhancement" --body "Description" --label "enhancement,release-blocker"
```

### **Step 3: Manage Issues**
```bash
# List issues
gh issue list

# View specific issue (CRITICAL: Use | cat to bypass pager!)
gh issue view 12 | cat

# Alternative: JSON output (recommended for parsing)
gh issue view 12 --json title,body,state,labels | jq '.'

# Close issue
gh issue close 12 --comment "Fixed in PR #15"

# Reopen issue
gh issue reopen 12
```

### **Step 4: Create Labels**
```bash
gh label create "bug" --color "d73a4a" --description "System defects"
gh label create "enhancement" --color "a2eeef" --description "New capabilities"
gh label create "research" --color "0075ca" --description "Academic/methodological concerns"
```

---

## 🏗️ **Method 2: Issue Templates (RECOMMENDED FOR PROJECTS)**

### **Create Template Directory**
```bash
mkdir -p .github/ISSUE_TEMPLATE
```

### **Bug Report Template**
**File**: `.github/ISSUE_TEMPLATE/bug_report.yml`
```yaml
name: Bug Report
description: Report a system defect or unexpected behavior
title: "[BUG]: "
labels: ["bug"]
body:
  - type: markdown
    attributes:
      value: |
        Thanks for taking the time to fill out this bug report!
  
  - type: input
    id: summary
    attributes:
      label: Summary
      description: Brief description of the issue
      placeholder: ex. Resume functionality creates duplicate sessions
    validations:
      required: true

  - type: textarea
    id: expected-behavior
    attributes:
      label: Expected Behavior
      description: What should happen?
      placeholder: Resume should continue from existing session
    validations:
      required: true

  - type: textarea
    id: actual-behavior  
    attributes:
      label: Actual Behavior
      description: What actually happens?
      placeholder: Creates new session and duplicates work
    validations:
      required: true

  - type: textarea
    id: reproduction
    attributes:
      label: Steps to Reproduce
      description: How can this be reproduced?
      placeholder: |
        1. Start experiment with `discernus_cli.py`
        2. Interrupt mid-analysis
        3. Run `discernus_cli.py resume`
        4. Observe duplicate session creation
    validations:
      required: true

  - type: textarea
    id: impact
    attributes:
      label: Impact Assessment
      description: What's the business/technical impact?
      placeholder: Financial - wastes LLM API costs on duplicate analyses
    validations:
      required: false
```

### **Enhancement Template**  
**File**: `.github/ISSUE_TEMPLATE/enhancement.yml`
```yaml
name: Enhancement Request
description: Suggest a new feature or improvement
title: "[ENHANCEMENT]: "
labels: ["enhancement"]
body:
  - type: textarea
    id: problem
    attributes:
      label: Problem Statement
      description: What problem does this solve?
      placeholder: Describe the current limitation or need
    validations:
      required: true

  - type: textarea
    id: solution
    attributes:
      label: Proposed Solution
      description: How should this be implemented?
      placeholder: Describe your suggested approach
    validations:
      required: true

  - type: textarea
    id: alternatives
    attributes:
      label: Alternative Approaches
      description: What other approaches were considered?
      placeholder: List and briefly evaluate alternatives
    validations:
      required: false
```

### **Configuration File**
**File**: `.github/ISSUE_TEMPLATE/config.yml`
```yaml
blank_issues_enabled: true
contact_links:
  - name: 🤔 Questions & Discussion
    url: https://github.com/discernus/discernus/discussions
    about: Ask questions and discuss ideas with the community
```

---

## ⚠️ **Common Issues & Solutions**

### **Pager Hanging/Truncation** (MOST COMMON)
```
gh issue view 68
# Command hangs indefinitely or shows partial output
```

**Solution:**
```bash
# Use pipe to cat (RECOMMENDED)
gh issue view 68 | cat

# OR use JSON output  
gh issue view 68 --json title,body,state | jq '.'
```

### **"Bad Credentials" Error**
```
HTTP 401: Bad credentials (https://api.github.com/graphql)
```

**Solution:**
```bash
unset GITHUB_TOKEN  # Clear invalid token
gh auth status      # Verify keyring auth works
```

### **"Permission Denied" Error**
**Solution**: User needs to run `gh auth login` with proper scopes:
```bash
gh auth login --scopes "repo,gist,read:org,workflow"
```

### **"Command Not Found" Error**
**Solution**: GitHub CLI not installed. User needs to install:
```bash
# macOS
brew install gh

# Or download from: https://github.com/cli/cli/releases
```

---

## 🎯 **Why Other Agents Think They "Can't" Do This**

### **Common Misconceptions:**
1. **"I don't have API access"** - Wrong! GitHub CLI uses terminal commands, not direct API calls
2. **"I can't authenticate"** - Wrong! CLI handles auth via keyring/token
3. **"Too complex"** - Wrong! It's just terminal commands with clear syntax
4. **"Not safe"** - Wrong! Read-only until explicitly creating issues

### **The Reality:**
- ✅ **Any agent with terminal access can do this**
- ✅ **GitHub CLI is designed for automation** 
- ✅ **Authentication persists across sessions** (keyring)
- ✅ **Clear error messages guide troubleshooting**

---

## 📊 **Verification Checklist**

For any agent implementing GitHub Issues:

**Basic Functionality:**
- [ ] `gh auth status` shows active authentication
- [ ] Can create issue: `gh issue create --title "Test" --body "Test"`
- [ ] Can list issues: `gh issue list`  
- [ ] Can view issues without hanging: `gh issue view [number] | cat`
- [ ] Can close issues: `gh issue close [number]`

**Advanced Features:**
- [ ] Can create labels: `gh label create "test" --color "ffffff"`
- [ ] Can apply labels to issues: `--label "bug,enhancement"`
- [ ] Issue templates work in `.github/ISSUE_TEMPLATE/`
- [ ] Can reference issues in commits: `git commit -m "Fix issue #12"`

**Integration:**
- [ ] Issues appear properly on GitHub web interface
- [ ] Labels and templates render correctly
- [ ] Comments and closures work as expected

---

## 🚀 **Success Metrics**

**You've successfully implemented GitHub Issues when:**

1. ✅ **Issues created programmatically** appear in repository
2. ✅ **Labels and templates** provide structured input
3. ✅ **Integration works** with project workflow  
4. ✅ **Team can manage** issues through web interface
5. ✅ **Automation connects** issues to commits/PRs

---

## 📞 **For Future Agents**

**If you're told you "can't" create GitHub Issues:**

1. **Reference this guide** - Proven working approach
2. **Try the terminal commands** - GitHub CLI is your friend
3. **Check authentication** - `unset GITHUB_TOKEN` if needed  
4. **Start simple** - Basic issue creation first
5. **Build incrementally** - Add labels, templates, automation

**Remember**: The capability exists. Other agents might be overly cautious or lack specific knowledge. This guide provides the exact steps that work.

---

## 🔗 **Related Issues & Cross-References**

### **Python/Virtual Environment Problems?**
If you're having Python import errors, virtual environment issues, or project setup problems, see:
📖 **[CURSOR_AGENT_ENVIRONMENT_GUIDE.md](CURSOR_AGENT_ENVIRONMENT_GUIDE.md)**

**When Both Guides Apply:**
- Creating GitHub issues from Python scripts ➜ Use both environment activation AND GitHub auth
- GitHub CLI hanging in development environment ➜ Check both shell config AND virtual environment
- Project setup failing with GitHub operations ➜ Fix environment first, then GitHub auth

### **Command Integration Pattern**
```bash
# For GitHub operations requiring project context:
source venv/bin/activate && python3 script_that_uses_gh_cli.py

# For standalone GitHub CLI operations:
gh auth status  # No virtual environment needed
gh issue view 9 | cat  # No virtual environment needed
```

---

**Last Updated**: January 22, 2025  
**Verified Working**: discernus/discernus repository  
**Issues Created**: #9, #10, #11, #12 (all successful)  
**Critical Fix**: Pager bypass with `| cat` prevents hanging/truncation  
**Major Update**: Complete authentication reset procedure added (verified working July 22, 2025)  
**Authentication Issues**: SSH/HTTPS protocol conflicts now have comprehensive solution