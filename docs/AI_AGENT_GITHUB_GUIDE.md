# AI Agent Guide: GitHub Issues Management
## Proven Methods for AI Agents Working with GitHub

**Status**: ✅ **VERIFIED WORKING** - July 18, 2025  
**Evidence**: Successfully created and managed issues #9-#12 in discernus/discernus repo  
**Agent Tested**: Claude Sonnet 3.5 via Cursor

---

## 🎯 **For AI Agents: YES, YOU CAN DO THIS!**

If another agent told you "I can't create GitHub Issues," they were wrong. Here's exactly how to do it.

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

# View specific issue
gh issue view 12

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

## 🛠️ **Method 3: Programmatic Creation (FALLBACK)**

If GitHub CLI fails, use the web interface approach:

### **Guide User to Web Interface**
```
Please create an issue manually:

1. Go to: https://github.com/[owner]/[repo]/issues/new
2. Select appropriate template
3. Fill in required fields
4. Submit issue

Then tell me the issue number and I'll reference it in our work.
```

---

## 📋 **Complete Working Example**

Here's exactly what we did in discernus project:

```bash
# 1. Fix authentication
unset GITHUB_TOKEN
gh auth status  # Confirmed working

# 2. Create labels
gh label create "bug" --color "d73a4a" --description "System defects"
gh label create "enhancement" --color "a2eeef" --description "New capabilities"
gh label create "research" --color "0075ca" --description "Academic/methodological concerns"
gh label create "release-blocker" --color "b60205" --description "Critical for 1.0 release"
gh label create "orchestration" --color "f9d0c4" --description "Workflow system issues"
gh label create "synthesis" --color "c2e0c6" --description "Report generation issues"

# 3. Create issue templates (files shown above)

# 4. Create actual issues
gh issue create --title "Resume functionality creates duplicate sessions instead of continuing" --body "CRITICAL BUG: Financial Impact..." --label "bug,release-blocker"

# 5. Test functionality
gh issue create --title "Test Issue: Verify GitHub CLI Integration" --body "Test description" --label "enhancement"
gh issue close 12 --comment "Test completed successfully"
```

**Result**: Created issues #9, #10, #11, #12 - all successful!

---

## ⚠️ **Common Issues & Solutions**

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

**Last Updated**: July 18, 2025  
**Verified Working**: discernus/discernus repository  
**Issues Created**: #9, #10, #11, #12 (all successful) 