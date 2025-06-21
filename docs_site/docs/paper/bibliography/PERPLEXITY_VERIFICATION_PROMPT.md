# Perplexity AI Verification Prompt for Custom Instructions

**For Discernus Research and Academic Work**

---

## 📋 **Copy-Paste Ready Prompt**

```
CRITICAL: CITATION VERIFICATION PROTOCOL

For ALL academic citations you provide:

1. VERIFICATION REQUIREMENTS:
   - Include direct links to: Google Scholar result, DOI resolver, journal page
   - Mark confidence level: HIGH/MEDIUM/LOW/UNCERTAIN for each citation
   - If you cannot find a working link to the actual paper, explicitly state "LINK NOT VERIFIED"
   - Flag any citation you're not 100% certain exists with ⚠️

2. PROHIBITED ACTIONS:
   - NEVER create or suggest citations without verified web sources
   - NEVER assume a paper exists based on logical reasoning
   - NEVER cite papers you cannot directly link to

3. REQUIRED FORMAT for each citation:
   [Author, Year] - "Title" - Journal
   🔗 Verification: [Google Scholar link] | [DOI link] | [Journal link]
   📊 Confidence: HIGH/MEDIUM/LOW/UNCERTAIN
   ⚠️ [Flag if uncertain]

4. WHEN UNCERTAIN:
   Say "I found references to this topic but cannot verify specific citations" rather than providing unverified citations.

5. SEARCH STRATEGY:
   Use multiple search approaches and cross-reference sources before citing.

This is for academic research where citation accuracy is critical.
```

---

## 🎯 **Why This Prompt Works for Perplexity**

### **Leverages Perplexity's Strengths:**
- **Web search integration** - Forces use of Perplexity's search capabilities
- **Link generation** - Requires actual verification links
- **Source cross-referencing** - Encourages multiple search strategies

### **Addresses Perplexity's Risks:**
- **False confidence** - Requires explicit confidence rating
- **Link hallucination** - Demands working verification links
- **Citation fabrication** - Prohibits unverified citations

### **Provides Clear Structure:**
- **Verification requirements** - Specific, actionable steps
- **Prohibited actions** - Clear boundaries
- **Required format** - Consistent output structure
- **Fallback strategy** - What to do when uncertain

---

## 🔧 **Implementation Tips**

### **Custom Instructions Setup:**
1. **Copy the prompt** from the box above
2. **Paste into Perplexity Pro** custom instructions
3. **Test with known citations** to verify it's working
4. **Adjust if needed** based on Perplexity's response patterns

### **Testing the Prompt:**
Ask Perplexity to find citations for a topic you know well and check if:
- ✅ All links actually work
- ✅ Confidence levels are provided
- ✅ Uncertain citations are flagged
- ✅ Format is consistent

### **Optimization:**
If the prompt is too long for custom instructions, use this **condensed version**:

```
CITATION PROTOCOL: For all academic citations provide: (1) Working verification links (Google Scholar + DOI + Journal), (2) Confidence level (HIGH/MEDIUM/LOW), (3) ⚠️ flag if uncertain, (4) Say "cannot verify citations" instead of guessing. Academic research requires verified citations only.
```

---

## 📊 **Expected Results**

### **Before Safeguard Prompt:**
```
Perplexity: "Recent studies show this trend (Smith et al., 2024; Jones, 2023)"
User: *copies citations without verification*
Result: Potential hallucinations in bibliography
```

### **After Safeguard Prompt:**
```
Perplexity: "I found references to this trend but cannot verify specific recent citations. Here are verified sources I can confirm:
[Author, 2022] - 'Verified Title' - Real Journal
🔗 Verification: [working Scholar link] | [working DOI] | [working journal link]  
📊 Confidence: HIGH
```

---

## ⚠️ **Monitoring and Adjustment**

### **Weekly Review:**
- Check if Perplexity is following the verification protocol
- Note any citations that slip through without proper verification
- Adjust prompt language if needed

### **Red Flags to Watch:**
- Citations without working verification links
- Missing confidence ratings
- "Perfect" citations that seem too convenient
- Recent papers (2023-2024) without DOIs

### **Continuous Improvement:**
Based on your experience, you might need to:
- Add specific instructions for your research domain
- Include examples of acceptable vs. unacceptable citations
- Adjust confidence level requirements
- Add domain-specific verification sources

---

## 🚀 **Advanced Integration**

### **Workflow Integration:**
1. **Perplexity search** with verification prompt
2. **Immediate verification** of provided links
3. **Documentation** in your verification log
4. **Bibliography addition** only after verification

### **Team Coordination:**
If sharing Perplexity results with team members:
- Include the verification status in shared documents
- Copy the verification links for team review
- Flag any citations that need additional human verification

---

## 📝 **Success Metrics**

You'll know the prompt is working when:
- ✅ Every Perplexity citation comes with working verification links
- ✅ Confidence levels help you prioritize verification efforts
- ✅ Uncertain citations are clearly flagged
- ✅ You catch potential issues before they enter your bibliography
- ✅ Perplexity says "I cannot verify" instead of guessing

---

**Start today**: Copy the prompt into your Perplexity custom instructions and test it with your next research query! 