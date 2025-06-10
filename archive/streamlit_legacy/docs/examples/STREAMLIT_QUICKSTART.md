# 🎯 Streamlit Interface Quick Start Guide

## 🚀 Launch the App

### Option 1: Simple Launch
```bash
python launch_app.py
```

### Option 2: Direct Streamlit Command  
```bash
streamlit run moral_gravity_app.py
```

The app will open automatically in your browser at `http://localhost:8501`

## 📱 Interface Overview

### 🔧 Sidebar - Framework Management
- **Current Framework Display** - Shows which framework is active
- **Framework Switcher** - Change frameworks with dropdown + button
- **Framework Info** - View detailed framework configuration

### 📝 Main Tabs

#### 1. Text Analysis Tab
- **📝 Paste Text** - Direct text input for analysis
- **📁 Upload File** - Upload .txt or .md files
- **📂 Load Existing JSON** - Continue work on previous analyses
- **📋 Generate Prompt** - Create prompts for LLM analysis
- **🎯 Generate Visualization** - Create charts from JSON results

#### 2. Batch Processing Tab  
- **📁 Multi-file Upload** - Process multiple texts at once
- **📋 Batch Prompt Generator** - Create batch analysis prompts
- **💾 Analysis Package Creator** - Organize files for batch processing

#### 3. Framework Creator Tab
- **🏗️ Guided Framework Creation** - Step-by-step wizard
- **🔄 Dipole Definition** - Visual interface for creating moral dipoles
- **📝 Language Cues** - Easy input for positive/negative language patterns

#### 4. Visualizations Tab
- **🖼️ Gallery View** - Browse all your visualizations
- **🔍 Analysis Comparison** - Side-by-side comparison tool
- **📊 Interactive Charts** - Detailed metrics and comparisons

## 🔄 Typical Workflow

### For Single Text Analysis:
1. **Select Framework** - Use sidebar to choose or switch frameworks
2. **Input Text** - Paste, upload, or load existing analysis
3. **Generate Prompt** - Click "Generate Analysis Prompt" 
4. **Copy to LLM** - Use the generated prompt in ChatGPT/Claude
5. **Paste Results** - Return JSON response to the app
6. **Create Visualization** - Click "Generate Visualization"
7. **Download Results** - Save JSON and PNG files

### For Creating Custom Framework:
1. **Go to Framework Creator Tab**
2. **Fill Framework Info** - Name, description, number of dipoles
3. **Define Each Dipole** - Positive/negative poles + language cues
4. **Create Framework** - Submit form to generate configuration files
5. **Switch to New Framework** - Use sidebar to activate it
6. **Test with Sample Text** - Validate your framework works

### For Batch Processing:
1. **Go to Batch Processing Tab**
2. **Upload Multiple Files** - Select all texts to analyze
3. **Generate Batch Prompt** - Get specialized prompt for multiple texts
4. **Prepare Analysis Package** - Organize files for processing
5. **Process with LLM** - Use batch prompt for efficient analysis
6. **Return for Visualization** - Process results through Text Analysis tab

## 💡 Tips for Reducing Cursor Dependency

### ✅ What You Can Do in the GUI:
- Switch frameworks without command line
- Generate prompts without manual file editing
- Create visualizations with point-and-click
- Compare analyses side-by-side
- Create new frameworks through wizard
- Organize and view all your results

### 🔧 When You Still Need Terminal/Cursor:
- Complex framework modifications (angles, weights)
- Advanced statistical analysis
- Custom visualization modifications
- Git operations and version control

## 🚨 Troubleshooting

### App Won't Start
```bash
# Check if you're in the right directory
ls narrative_gravity_elliptical.py

# Install dependencies manually
pip install -r requirements.txt

# Try direct streamlit command
streamlit run moral_gravity_app.py
```

### Framework Switching Issues
- Use sidebar framework switcher
- Check that frameworks exist in `frameworks/` directory
- Refresh browser if interface doesn't update

### Visualization Generation Fails
- Verify JSON format is valid
- Check that `model_output/` directory exists
- Ensure all required fields are present in JSON

### Upload Issues
- Only .txt and .md files supported
- File size limits apply (usually < 200MB)
- Check file encoding (UTF-8 recommended)

## 🎯 Next Steps

Once comfortable with the interface:
1. **Create Your Custom Framework** using the wizard
2. **Test Framework** with sample texts
3. **Batch Process** your research corpus  
4. **Generate Comparisons** between different frameworks
5. **Export Results** for your academic paper

This interface should handle 80% of your daily workflow without needing Cursor assistance! 🎉 