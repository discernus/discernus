# 🚀 Quick Start: AI Citation Safeguards

**IMMEDIATE ACTION ITEMS** - Implement these safeguards today!

---

## ⚡ **5-Minute Setup**

### 1. **Update Your AI Prompts** (1 minute)
Add this to every AI interaction that might involve citations:

```
IMPORTANT: If you suggest any academic citations, include:
- Web verification links (Google Scholar, DOI, journal site)
- Your confidence level (High/Medium/Low/Uncertain)  
- Flag any citations you're not certain about
- Do NOT invent citations - say "I don't know" instead
```

### 2. **Install Verification Tool** (2 minutes)
```bash
cd /path/to/your/project
python3 scripts/verify_citations.py --title "Test Citation" --authors "Test Author"
```

### 3. **Set Browser Bookmarks** (2 minutes)
Create bookmark folder "Citation Verification":
- [Google Scholar](https://scholar.google.com)
- [DOI Resolver](https://dx.doi.org/)  
- [Crossref Search](https://search.crossref.org/)
- [Retraction Watch](http://retractionwatch.com)

---

## 🔍 **Daily Workflow Changes**

### **When AI Suggests Citations:**

#### ❌ **OLD WAY:**
```
AI: "Here are some relevant papers: Smith et al. 2024..."
You: *copies directly to bibliography*
```

#### ✅ **NEW WAY:**
```
AI: "Here are some relevant papers: Smith et al. 2024..."
You: "Provide verification links for each citation"
AI: "I should note that I'm not certain about these citations..."
You: *verifies each citation before use*
```

### **3-Step Verification** (2-3 minutes per citation):
1. **Google Scholar Search**: `title + author names`
2. **DOI Check**: Does the DOI resolve to the actual paper?
3. **Journal Verification**: Does the paper exist in that journal/volume?

---

## 📋 **Documentation Template**

Keep a simple verification log:

```markdown
## Citation Verification Log - [Date]

| Citation | AI Source | Status | Verification Method | Notes |
|----------|-----------|---------|---------------------|--------|
| Smith 2024 | Claude | ✅ VERIFIED | DOI + Scholar | Found in Nature |
| Jones 2023 | ChatGPT | ❌ FAKE | No results | Hallucination |
```

---

## 🚨 **Red Flag Checklist**

**STOP and verify immediately if citation has:**
- [ ] Perfect fit for your exact research need (too convenient)
- [ ] Recent date but can't find online
- [ ] Authors you can't find at claimed institutions  
- [ ] Journal you haven't heard of
- [ ] DOI that doesn't resolve
- [ ] Multiple "recent" papers from same obscure journal

---

## 💡 **Browser Extensions** (Optional but helpful)

- **DOI resolver plugins** - Instantly check DOI validity
- **Google Scholar Button** - Quick searches from any page
- **Zotero Connector** - Auto-fetch verified bibliographic data

---

## ⚠️ **Emergency Protocol** 

**If you discover a fake citation in your work:**

1. **Immediate Action**:
   - Remove from all drafts immediately
   - Search for replacement citations
   - Document the hallucination

2. **Team Notification**:
   - Alert collaborators about the fake citation
   - Check if it appears in other team work
   - Update shared bibliography databases

3. **Prevention**:
   - Review AI interaction that produced the fake
   - Improve prompting to reduce future hallucinations
   - Share experience with research community

---

## 🎯 **Success Indicators**

You're doing it right when:
- ✅ Every AI-suggested citation is verified before use
- ✅ You catch suspicious citations during AI conversation
- ✅ Your bibliography has verification status for each entry
- ✅ You find legitimate alternatives to replace fakes
- ✅ Team members know the verification protocol

---

## 📞 **Get Help**

If you discover fake citations or need verification help:
1. **Check this project's safeguard guide**: `AI_BIBLIOGRAPHY_SAFEGUARDS.md`
2. **Use verification tool**: `scripts/verify_citations.py`
3. **Ask colleagues for second opinions**
4. **Contact library for institutional verification services**

---

**Remember**: The goal is safe, effective AI use - not avoiding AI entirely!

**Start today**: Add verification prompts to your next AI interaction. 