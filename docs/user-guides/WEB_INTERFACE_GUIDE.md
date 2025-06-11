# Web Interface Usage Guide

## 🌐 Narrative Gravity Analysis Chatbot - Web Interface

### Quick Start

1. **Launch the Web Interface**:
   ```bash
   python3 chatbot_web.py
   ```

2. **Open Your Browser**:
   Go to: http://localhost:5001

3. **Ready to Use**: The interface will load with your current framework displayed.

### Key Features

#### 📝 Large Text Input Support
- **Capacity**: Up to 1.2MB of text (3x largest corpus file)
- **Character Counter**: Live updating with visual feedback
- **Auto-disable**: Submit button disabled if text exceeds limits
- **Keyboard Shortcut**: Ctrl+Enter to submit

#### 🔄 Framework Management
- **Current Framework**: Displayed prominently at top
- **Framework Switching**: Dropdown selector with instant switching
- **Live Updates**: Framework changes reflected immediately

#### 🧠 Intelligent Processing
- **Domain Classification**: LLM-powered content classification
- **Analysis Metadata**: Shows classification confidence and reasoning
- **Response Types**: Framework explanations, analysis results, general responses

#### 🎨 User Experience
- **Modern Design**: Clean, professional interface
- **Responsive Layout**: Works on desktop and mobile
- **Loading States**: Visual feedback during processing
- **Error Handling**: Clear error messages and recovery

### Usage Patterns

#### 1. Framework Questions
```
What is the Fukuyama Identity framework?
Explain Megalothymic Thymos
How does Civic Virtue work?
```

#### 2. Large Text Analysis
- Paste political speeches (up to 1.2MB)
- Presidential addresses
- Political statements
- Campaign materials

#### 3. Framework Switching
- Use dropdown to select framework
- Click "Switch" button
- Confirmation shown with green success message

### Technical Details

#### Endpoints
- **Main Interface**: `GET /` - HTML interface
- **Chat Processing**: `POST /chat` - JSON API for analysis
- **Framework Switching**: `POST /switch_framework` - Framework management
- **Status Check**: `GET /status` - System status

#### Supported Input Types
- **Text Length**: 0 - 1,258,291 characters (~1.2MB)
- **Content Types**: Political discourse, framework questions, general queries
- **Languages**: English (primary), with framework content in various languages

#### Response Metadata
The interface shows helpful metadata including:
- Domain classification (political_discourse, framework_question, etc.)
- Classification confidence scores
- Text analysis metrics
- Processing timestamps

### Integration with Existing System

#### Chatbot Backend
- Uses the same `NarrativeGravityBot` as the command-line version
- All framework management functionality available
- Same intelligent domain classification
- Full conversation context tracking

#### Database Integration
- PostgreSQL for framework storage
- Session tracking and analysis history
- Full compatibility with existing data structures

### Advantages Over Command Line

✅ **Large Text Handling**: No terminal buffer limitations  
✅ **Visual Feedback**: Character counts, loading states, progress indicators  
✅ **Copy-Paste Friendly**: Easy to paste large texts from documents  
✅ **Professional UI**: Clean, modern interface suitable for demonstrations  
✅ **Error Recovery**: Clear error messages and recovery options  
✅ **Framework Management**: Visual framework switching with confirmation  

### Next Steps

This basic web interface provides the foundation for:
- Integration with React frontend
- Advanced visualization features
- Real-time collaboration
- API documentation interface
- Administrative dashboard

The web interface maintains full compatibility with the existing chatbot system while providing a much more user-friendly experience for large text analysis.

### Troubleshooting

#### Server Won't Start
```bash
# Check if port 5001 is available
lsof -i :5001

# Kill existing process if needed
pkill -f chatbot_web.py

# Restart
python3 chatbot_web.py
```

#### Import Errors
```bash
# Ensure you're in the project root
cd /path/to/narrative_gravity_analysis

# Check Python path
python3 -c "import sys; print('\n'.join(sys.path))"
```

#### Framework Issues
- Check that frameworks are properly configured in `frameworks/` directory
- Verify PostgreSQL connection
- Run `python check_database.py` if needed 