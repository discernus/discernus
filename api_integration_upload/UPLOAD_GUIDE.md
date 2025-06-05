# API Integration Upload Files - Guide

## 🎯 Purpose
These files provide complete context for developing API integration specifications for the Narrative Gravity Maps framework (v2025.06.04.2).

## 📋 File Descriptions

### **📚 Documentation Files**
1. **`COMPREHENSIVE_PROJECT_DOCUMENTATION.md`** (68KB)
   - **MAIN CONTEXT** - Complete project overview, architecture, and API integration requirements
   - Strategic roadmap and technical specifications
   - **START HERE** for understanding the project

2. **`SOURCE_CODE_SUMMARY.md`** (2KB)
   - Quick reference guide to critical files
   - Highlights main bottlenecks and priorities

### **🔥 Critical Source Code (Python → .txt)**
3. **`generate_prompt.py` → `generate_prompt.txt`** (351 lines)
   - **HIGHEST PRIORITY** - This is the manual workflow bottleneck
   - Currently generates prompts for copy/paste to LLMs
   - **MAIN TARGET** for API automation

4. **`narrative_gravity_elliptical.py` → `narrative_gravity_elliptical.txt`** (1,136 lines)
   - Core mathematical analysis engine
   - Handles JSON processing and visualization generation
   - Ready for batch processing automation

5. **`framework_manager.py` → `framework_manager.txt`** (257 lines)
   - Multi-framework switching system
   - Critical for API routing to different analysis types

6. **`narrative_gravity_app.py` → `narrative_gravity_app.txt`** (1,372 lines)
   - Streamlit web interface
   - Shows workflow patterns ready for API automation

### **⚙️ Configuration Files**
7. **`config/dipoles.json` → `dipoles.txt`** (78 lines)
   - Framework definitions used for prompt generation
   - Critical for understanding data structures

8. **`config/framework.json` → `framework.txt`** (107 lines)
   - Mathematical parameters for calculations
   - Shows elliptical coordinate system configuration

### **📦 Dependencies**
9. **`requirements.txt`**
   - Python package dependencies
   - Technical reference for implementation

## 🚀 **API Integration Objective**

Transform this **manual workflow**:
```
generate_prompt.py → Manual Copy/Paste → LLM Interface → Manual JSON Copy → Save File → Visualization
```

Into this **automated workflow**:
```
text_input → api_client.analyze() → automated_validation → batch_processing → enhanced_visualization
```

## 🎯 **Key Focus Areas**

1. **Replace Manual Prompt Workflow** (`generate_prompt.txt`)
   - Current bottleneck requiring manual LLM interaction
   - Target: Direct API calls to Hugging Face, OpenAI, Anthropic

2. **Multi-Run Statistical Analysis** 
   - Enable variance quantification across multiple runs
   - Add confidence intervals and cross-model validation

3. **Batch Processing Enhancement**
   - Scale from single analysis to corpus-level processing
   - Implement progress tracking and result caching

4. **Framework-Agnostic Architecture**
   - Support civic virtue, political spectrum, rhetorical posture frameworks
   - Dynamic framework switching for different analysis types

## 📊 **Current System Status**
- **Version**: v2025.06.04.2 (production-ready)
- **Code Base**: 4,084 lines Python (2,572 core, 606 tools, 906 tests)
- **Test Coverage**: 31 tests passing
- **Architecture**: Modular framework system with symlink-based configuration

**Ready for API integration to become a scalable research platform.** 