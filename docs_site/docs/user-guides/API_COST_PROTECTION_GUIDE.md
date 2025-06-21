# 🛡️ API Cost Protection Guide

## Overview
Your system now has **comprehensive cost protection** built-in to prevent unexpected API charges from OpenAI, Anthropic, and Mistral.

## 🔐 Protection Layers

### **1. Pre-Request Cost Estimation**
- **Automatic estimation** before every API call
- **Real-time limit checking** 
- **Immediate blocking** if limits would be exceeded

### **2. Automatic Cost Tracking**
- **Real-time recording** of actual costs
- **Token usage tracking** for accuracy
- **Historical cost data** for analysis

### **3. Multi-Level Spending Limits**
- **Daily limits**: Prevent daily overspending
- **Weekly limits**: Control weekly research budgets
- **Monthly limits**: Academic budget management
- **Single request limits**: Prevent large single charges

### **4. Early Warning System**
- **80% threshold warnings** when approaching limits
- **Real-time notifications** during analysis
- **Spending summaries** and breakdowns

## 📋 Current Settings

### **Your Default Limits:**
```
Daily: $2.00        # Safe for daily research
Weekly: $10.00      # Reasonable weekly budget
Monthly: $25.00     # Academic-friendly monthly limit
Single Request: $0.50  # Prevent large single charges
```

### **Typical Costs per Analysis:**
```
GPT-4: ~$0.01-0.02          # Most expensive
Claude-3-Sonnet: ~$0.003-0.005  # Mid-range
Claude-3-Haiku: ~$0.0004    # Very cheap
Mistral-Large: ~$0.007      # Mid-range
GPT-3.5-Turbo: ~$0.0005    # Very cheap
```

## 🚀 **How to Use Cost Management**

### **Check Current Status**
```bash
python manage_costs.py status
```

### **Set Your Own Limits**
```bash
# Conservative research limits
python manage_costs.py limits --daily 1 --weekly 5 --monthly 15

# Production/large-scale limits  
python manage_costs.py limits --daily 10 --weekly 50 --monthly 150
```

### **Estimate Costs Before Running**
```bash
python manage_costs.py estimate "Your text to analyze here"
```

### **Export Cost Data for Accounting**
```bash
python manage_costs.py export --filename my_research_costs.csv
```

### **Real-Time Monitoring**
```bash
python manage_costs.py monitor
```

## ⚙️ **Provider-Specific Cost Management**

### **OpenAI (Most Expensive)**
- **GPT-4**: $0.03/1K input + $0.06/1K output tokens
- **GPT-3.5**: $0.0005/1K input + $0.0015/1K output tokens
- **Billing**: Per token, very accurate
- **Cost Control**: ✅ Excellent usage tracking

### **Anthropic (Mid-Range)**
- **Claude-3-Sonnet**: $0.003/1K input + $0.015/1K output tokens
- **Claude-3-Haiku**: $0.00025/1K input + $0.00125/1K output tokens
- **Billing**: Per token, accurate
- **Cost Control**: ✅ Good usage tracking

### **Mistral (Competitive)**
- **Large**: $0.008/1K input + $0.024/1K output tokens
- **Small**: $0.002/1K input + $0.006/1K output tokens
- **Billing**: Per token, estimated if not provided
- **Cost Control**: ✅ Estimated tracking

## 🚨 **Emergency Procedures**

### **If You Hit a Limit**
```bash
# Check current spending
python manage_costs.py status

# Increase limits if needed
python manage_costs.py limits --daily 5

# Or wait for next time period
```

### **If Costs Seem Wrong**
```bash
# Export data for review
python manage_costs.py export

# Reset tracking if needed (with confirmation)
python manage_costs.py reset
```

### **For Large Analysis Projects**
```bash
# Set higher temporary limits
python manage_costs.py limits --weekly 20 --monthly 60

# Run your analysis
python run_flagship_analysis.py --samples

# Reset to conservative limits
python manage_costs.py limits --daily 2 --weekly 10
```

## 📊 **Best Practices for Academic Research**

### **1. Budget Planning**
- **Start conservative**: $25/month typically covers substantial research
- **Track by project**: Export costs for grant reporting
- **Use cheaper models first**: Test with GPT-3.5 and Claude-Haiku

### **2. Model Selection Strategy**
```bash
# Development/testing: Use cheaper models
--model gpt-3.5-turbo
--model claude-3-haiku

# Final analysis: Use premium models
--model gpt-4
--model claude-3-sonnet
```

### **3. Batch Processing**
- **Estimate total costs** before large batches
- **Process in smaller chunks** to stay within daily limits
- **Monitor progress** during long analyses

### **4. Cost Optimization**
- **Shorter prompts** = lower input costs
- **Focused analysis** = lower output costs  
- **Model selection** based on task complexity

## 🔧 **Advanced Configuration**

### **Custom Cost Limits per Provider**
You can modify `src/utils/cost_manager.py` to set different limits for different providers:

```python
# Example: Higher limits for cheaper models
if provider == "anthropic" and "haiku" in model:
    daily_limit *= 2  # Double limit for cheap model
```

### **Project-Specific Tracking**
```python
# Create separate cost managers for different projects
cost_manager = CostManager(
    cost_file="project_a_costs.json",
    limits_file="project_a_limits.json"
)
```

### **Alert Integration**
Add email/Slack alerts when approaching limits by modifying the `_check_and_warn_limits()` method.

## 🎯 **Summary: Your Protection is Active**

✅ **Automatic cost estimation** before every request  
✅ **Hard limits** prevent overspending  
✅ **Real-time tracking** of actual costs  
✅ **Early warnings** at 80% of limits  
✅ **Multi-level protection** (daily/weekly/monthly)  
✅ **Provider-specific tracking** for all three APIs  
✅ **Export capabilities** for accounting/grants  
✅ **Emergency controls** to adjust or reset  

**Your research is protected against runaway costs while maintaining full access to flagship LLMs! 🛡️** 