# Chainlit Interface Usage Guide

## 🎯 Overview

The Chainlit interface provides the most advanced conversational experience for the Narrative Gravity Analysis platform. It replicates the sophisticated academic discussion style demonstrated in the Fukuyama framework development process, offering a rich, interactive environment for political discourse analysis.

## 🚀 Quick Start

### Launch the Interface

```bash
# Option 1: Dedicated launcher (recommended)
python launch_chainlit.py

# Option 2: Through main launcher
python launch.py --chainlit-only

# Option 3: Direct chainlit command
chainlit run chainlit_chat.py --host 0.0.0.0 --port 8002
```

The interface will be available at: **http://localhost:8002**

### System Requirements

- Python 3.9+ with all project requirements installed
- Working PostgreSQL database (see `LAUNCH_GUIDE.md`)
- Chainlit 1.3.1+ (automatically installed with `pip install -r requirements.txt`)

## 💡 Core Features

### 1. **Multi-Framework Analysis**
- Switch between frameworks mid-conversation
- Compare analyses across different theoretical lenses
- Create custom frameworks through guided conversation

### 2. **Advanced Text Processing**
- Supports texts up to 1.2MB (approximately 600,000 words)
- YouTube transcript analysis via URL
- Batch file processing
- Real-time analysis with confidence indicators

### 3. **Interactive Experience**
- Action buttons for common follow-up tasks
- Rich markdown rendering with mathematical expressions
- Professional styling with custom CSS
- Conversation context preservation

### 4. **Academic Integration**
- Replicates scholarly conversation patterns
- Evidence-based analysis justification
- Theoretical framework development processes
- Comparative methodology support

## 🛠️ Usage Examples

### Basic Text Analysis

```
You: Analyze this speech: "My fellow Americans, we stand at a crossroads between two fundamentally different visions of our future..." 