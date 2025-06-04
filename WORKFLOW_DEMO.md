# 🎯 Moral Gravity Wells - Quick Start Workflow

## Step-by-Step Guide

### 1. **Paste Your Text** ✅ (You've done this!)
You can see in your Text Analysis tab that you've already pasted some text. Great start!

### 2. **Generate Analysis Prompt** 📋
- Click the **"📋 Generate Analysis Prompt"** button on the right side
- This creates a specialized prompt for the current framework (`moral_foundations`)
- Copy the entire generated prompt

### 3. **Use with LLM** 🤖
Go to ChatGPT, Claude, or your preferred LLM and:
- Paste the generated prompt
- Add your text at the end
- Ask the LLM to analyze it

### 4. **Get JSON Response** 📊
The LLM will return something like:
```json
{
  "moral_foundations_scores": {
    "care_positive": 0.75,
    "harm_negative": 0.25,
    "fairness_positive": 0.60,
    "cheating_negative": 0.15,
    "loyalty_positive": 0.80,
    "betrayal_negative": 0.10,
    "authority_positive": 0.70,
    "subversion_negative": 0.20,
    "sanctity_positive": 0.45,
    "degradation_negative": 0.30
  },
  "moral_polarity_score": 0.65,
  "directional_purity_score": 0.78,
  "text_analysis": {
    "dominant_moral_foundation": "loyalty_positive",
    "key_moral_language": "nation, country, people, service",
    "moral_intensity": "high"
  }
}
```

### 5. **Paste JSON Back** 📋
- Copy the JSON response from your LLM
- Paste it into the **"🤖 LLM Analysis Results"** text area in the Streamlit app

### 6. **Generate Visualization** 🎯
- Click **"🎯 Generate Visualization"** 
- The app will create a beautiful moral gravity wells chart
- You can download both the JSON data and PNG image

## 🔄 Framework Switching
- Use the sidebar to switch between different frameworks
- Try `moral_foundations`, `political_spectrum`, or `virtue_ethics`
- Each framework analyzes text differently

## 🎨 Other Features
- **Batch Processing**: Upload multiple files at once
- **Framework Creator**: Build your own custom framework
- **Visualizations**: Compare different analyses side-by-side

## 💡 Quick Test
Try this with your current text:
1. Click "Generate Analysis Prompt"
2. Copy the prompt
3. Go to ChatGPT and paste: "Here's the analysis prompt: [PASTE PROMPT HERE]. Please analyze this text: [YOUR TEXT HERE]"
4. Copy the JSON response back to the Streamlit app
5. Click "Generate Visualization"

You should get a beautiful moral gravity wells visualization showing how your text maps to different moral foundations! 