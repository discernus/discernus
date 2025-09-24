# Troubleshooting Guide - Trump Populism Evolution Study

## 🚨 Critical Issues

### **Framework Configuration Errors**
```
Error: PDAF v10.0 framework not found
```
**Root Cause**: Framework not properly loaded or configured
**Solution**:
```bash
# Validate framework availability
discernus validate framework pdaf_v10

# Reinitialize if needed
discernus framework reload pdaf_v10

# Check framework directory
ls -la /discernus/core/frameworks/pdaf_v10/
```

### **Model Authentication Failures**
```
Error: Gemini model authentication failed
```
**Root Cause**: API keys expired or misconfigured
**Solution**:
```bash
# Check model health
discernus health check --models gemini-2.0-flash-exp

# Validate API configuration
discernus config validate --api-keys

# Refresh authentication if needed
discernus auth refresh --provider google
```

### **Corpus Access Issues**
```
Error: Cannot access corpus directory
```
**Root Cause**: File permissions or path issues
**Solution**:
```bash
# Verify corpus structure
ls -la /corpus/analysis_ready/

# Check permissions
chmod -R 755 /corpus/analysis_ready/

# Validate document integrity
find /corpus/analysis_ready/ -name "*.txt" -exec file {} \;
```

## ⚠️ Common Execution Issues

### **Memory/Resource Constraints**
**Symptoms**: Process crashes during large phase execution
**Solutions**:
```bash
# Reduce batch size
discernus run experiment --batch-size 5 ...

# Process sequentially
discernus run experiment --phase-by-phase ...

# Monitor resources
discernus run experiment --monitor-resources ...
```

### **Rate Limiting**
**Symptoms**: API quota exceeded errors
**Solutions**:
```bash
# Add delays between requests
discernus run experiment --delay 30 ...

# Use exponential backoff
discernus run experiment --retry-strategy exponential ...

# Monitor API usage
discernus monitor usage --real-time
```

### **Document Processing Failures**
**Symptoms**: Individual documents fail analysis
**Solutions**:
```bash
# Check document formatting
file /corpus/analysis_ready/01_campaign_2015_2016/problematic_doc.txt

# Validate text encoding
discernus validate documents /corpus/analysis_ready/

# Skip problematic documents
discernus run experiment --skip-errors --log-failures ...
```

## 🔍 Diagnostic Commands

### **System Health Check**
```bash
# Comprehensive health assessment
discernus health check --full

# Framework validation
discernus validate framework pdaf_v10 --verbose

# Corpus integrity check
discernus validate corpus /corpus/analysis_ready/ --detailed
```

### **Performance Monitoring**
```bash
# Monitor execution progress
discernus monitor execution --real-time

# Track resource usage
discernus monitor resources --log-to-file

# API usage analytics
discernus monitor usage --breakdown-by-phase
```

### **Log Analysis**
```bash
# View recent logs
tail -f /logs/discernus.log

# Search for specific errors
grep "ERROR" /logs/discernus.log | tail -20

# Phase-specific logs
discernus logs show --phase campaign_2015_2016 --level ERROR
```

## 🛠️ Recovery Procedures

### **Interrupted Execution Recovery**
```bash
# Check execution state
discernus status execution

# Resume from last checkpoint
discernus run experiment --resume-from-checkpoint

# Validate partial results
discernus validate results /runs/partial_results/
```

### **Corrupted Results Recovery**
```bash
# Identify corrupted files
find /runs/ -name "*.json" -exec jq . {} \; 2>/dev/null | grep -v "^{" | wc -l

# Re-run specific phases
discernus run experiment --phases 2,3 --overwrite

# Backup and restore
cp -r /runs /runs_backup
discernus run experiment --clean-restart
```

### **Configuration Reset**
```bash
# Reset framework configuration
discernus config reset pdaf_v10

# Clear cache and temporary files
discernus cache clear --all

# Reinitialize experiment environment
discernus experiment init --template pdaf_v10_execution.yaml
```

## 📊 Quality Assurance

### **Result Validation**
```bash
# Validate analysis completeness
discernus validate results /runs/*_results/ --completeness

# Check consistency across phases
discernus validate results /runs/*_results/ --consistency

# Verify metadata integrity
discernus validate metadata /corpus/metadata/
```

### **Performance Benchmarks**
- **Expected Runtime**: 20-30 hours total
- **Normal Memory Usage**: < 8GB per phase
- **API Rate**: < 60 requests/minute
- **Success Rate**: > 95% document processing

### **Quality Metrics**
- **Analysis Depth**: PDAF dimensions fully populated
- **Consistency**: < 5% variation between similar documents
- **Completeness**: All required fields present in results
- **Accuracy**: Manual spot-check validation

## 🚨 Emergency Procedures

### **Complete System Reset**
```bash
# Stop all processes
discernus stop --all

# Backup critical data
cp -r /runs /runs_emergency_backup
cp -r /corpus/analysis_ready /corpus_emergency_backup

# Reset environment
discernus reset --full

# Reinitialize from template
discernus project init --template trump_populism_reorganized
```

### **Data Recovery**
```bash
# Restore from backup
cp -r /runs_emergency_backup/* /runs/

# Verify data integrity
discernus validate corpus /corpus/analysis_ready/
discernus validate results /runs/

# Resume execution
discernus run experiment --resume
```

## 📞 Support Resources

### **Documentation**
- **Execution Guide**: `/docs/execution_guides/pdaf_execution_guide.md`
- **Framework Documentation**: `/docs/specifications/pdaf_v10_specification.md`
- **API Reference**: `/docs/developer/api_reference.md`

### **Logs and Diagnostics**
- **System Logs**: `/logs/discernus.log`
- **Execution Logs**: `/runs/*/execution.log`
- **Debug Information**: `discernus debug info --full`

### **Community Resources**
- **GitHub Issues**: Report bugs and request features
- **Documentation Wiki**: Extended troubleshooting guides
- **User Forum**: Community-driven solutions and workarounds

---

**Last Updated**: January 30, 2025
**Version**: 1.0
**Status**: Production Ready
