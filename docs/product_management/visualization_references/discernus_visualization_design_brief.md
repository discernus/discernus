
# Discernus Visualization System — Design Brief

## 🧭 Overview
Discernus visualizations are designed to translate complex rhetorical scoring data into clear, interpretable visual patterns. These tools should aid researchers in theory validation and support civic users in understanding the moral and ideological structure of political texts.

## 🎯 Core Design Goals
- **Clarity**: Make worldview structures immediately legible
- **Theoretical Fidelity**: Every axis, pole, and score must map directly to Discernus frameworks (e.g., MFT, Populism)
- **Comparability**: Ensure consistency across visualizations to enable document-to-document or model-to-model comparisons
- **Diagnostic Value**: Prioritize outputs that help users understand internal contradiction, rhetorical strength, and model confidence

## 👥 Key Audiences
- Academic researchers
- Civic discourse analysts
- Policy watchdogs
- Political communication educators

## 📐 Visual Components (Must-Have)
1. **Gravity Well Ellipse**  
   - 8–10 fixed poles (e.g., Dignity, Fear, Tribalism)  
   - Blue score rays to poles; orange center dot with coordinate  
   - Optional contradiction ribbon if index > 0.5  

2. **Integrative vs. Disintegrative Bar Chart**  
   - Side-by-side grouped bars with error bars per dimension  
   - Green for positive wells; red for disintegrative wells  

3. **Variance/Confidence Bar**  
   - 5-run model scoring with ±σ range per well  

4. **Model-Human Correlation Grid**  
   - Matrix comparing model scores vs human aggregate per well  

5. **Narrative Trajectory Plot**  
   - Line plot showing movement of narrative center across multiple speeches  

## ✨ Optional / High-Delight Features
- Interactive ellipse (hover reveals quotes, references)
- Time slider for narrative evolution
- Model overlays with sonar-style diffusion
- Printable dashboard reports

## 🎨 Style Guide
- Font: Inter or Source Sans
- Color:
  - Green (integrative): #44aa99
  - Red (disintegrative): #dd5566
  - Blue (score rays): #3399ff
  - Orange (center): #ff9933
- Layout: Center visual, summary sidebar, bottom metric strip

## 📦 Outputs
- SVG and PNG for publication
- JSON overlays for interactive embedding
- Summary markdown card with chart and score snapshot
