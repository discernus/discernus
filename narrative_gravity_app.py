#!/usr/bin/env python3
"""
Narrative Gravity Maps - Streamlit Interface
A user-friendly GUI for the Narrative Gravity Maps methodology
"""

import streamlit as st
import json
import os
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import subprocess
from datetime import datetime
import importlib
import sys
import re

# Force reload narrative_gravity_elliptical to ensure we get the latest changes
if 'narrative_gravity_elliptical' in sys.modules:
    importlib.reload(sys.modules['narrative_gravity_elliptical'])

# Import our existing modules
from narrative_gravity_elliptical import NarrativeGravityWellsElliptical
from framework_manager import FrameworkManager
from src.prompts.template_manager import PromptTemplateManager

# Configure page
st.set_page_config(
    page_title="Narrative Gravity Maps",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        margin: 1rem 0;
    }
    .warning-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'framework_manager' not in st.session_state:
        st.session_state.framework_manager = FrameworkManager()
    if 'current_framework' not in st.session_state:
        st.session_state.current_framework = st.session_state.framework_manager.get_active_framework()
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = None
    if 'comparative_results' not in st.session_state:
        st.session_state.comparative_results = None

def sidebar_framework_manager():
    """Sidebar for framework management"""
    st.sidebar.markdown("## 🎯 Framework Management")
    
    # Current framework display
    current = st.session_state.current_framework
    st.sidebar.markdown(f"**Default Framework:** `{current}`")
    st.sidebar.markdown("*Individual analyses use their own detected frameworks*")
    
    # Available frameworks
    framework_data = st.session_state.framework_manager.list_frameworks()
    frameworks = [fw['name'] for fw in framework_data]
    
    # Framework switcher for new analyses
    selected_framework = st.sidebar.selectbox(
        "Default for new prompts:",
        frameworks,
        index=frameworks.index(current) if current and current in frameworks else 0,
        key="framework_selector",
        help="This sets the default framework for generating new prompts. Existing analyses will use their original frameworks."
    )
    
    if selected_framework != current:
        if st.sidebar.button("🔄 Set as Default", key="switch_btn"):
            try:
                st.session_state.framework_manager.switch_framework(selected_framework)
                st.session_state.current_framework = selected_framework
                st.sidebar.success(f"Default set to {selected_framework}")
                st.rerun()
            except Exception as e:
                st.sidebar.error(f"Error setting default framework: {e}")
    
    # Framework info
    if st.sidebar.button("ℹ️ Framework Info", key="info_btn"):
        try:
            # Find the framework data
            framework_info = next((fw for fw in framework_data if fw['name'] == current), None)
            if framework_info:
                st.sidebar.markdown("### Framework Details")
                st.sidebar.json({
                    'name': framework_info['name'],
                    'version': framework_info['version'],
                    'description': framework_info['description'],
                    'dipole_count': framework_info['dipole_count'],
                    'well_count': framework_info['well_count']
                })
            else:
                st.sidebar.error("Framework information not found")
        except Exception as e:
            st.sidebar.error(f"Error loading framework info: {e}")

def main_analysis_interface():
    """Main interface for text analysis"""
    st.markdown('<div class="main-header">🎯 Narrative Gravity Maps</div>', unsafe_allow_html=True)
    
    # Create tabs for different functions - updated tab names and added comparison
    tab1, tab2, tab3, tab4 = st.tabs(["📝 Create Analysis", "🔧 Framework Creator", "📈 Visualizations", "🔍 Compare Analysis"])
    
    with tab1:
        single_text_analysis()
    
    with tab2:
        framework_creation_interface()
    
    with tab3:
        visualization_interface()
    
    with tab4:
        comparison_interface()

def single_text_analysis():
    """Interface for analyzing a single text"""
    st.markdown('<div class="section-header">Create New Analysis</div>', unsafe_allow_html=True)
    
    # Add explanation of the workflow
    st.info("""
    **📋 Workflow:** Generate Prompt → Use with External LLM → Paste JSON Response → Create Visualization
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Main workflow - Generate prompt
        st.markdown("### Step 1: Generate Prompt")
        if st.button("📋 Generate Analysis Prompt", type="primary"):
            try:
                current_framework = st.session_state.current_framework
                template_manager = PromptTemplateManager()
                prompt = template_manager.generate_interactive_prompt(current_framework)
                
                # Store prompt in session state so it persists
                st.session_state.generated_prompt = prompt
                st.session_state.prompt_timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                
                st.success("✅ Step 1 Complete! Copy this prompt to ChatGPT/Claude along with your text.")
                
            except Exception as e:
                st.error(f"Error generating prompt: {e}")
        
        # Show prompt and buttons if one has been generated
        if 'generated_prompt' in st.session_state:
            prompt = st.session_state.generated_prompt
            timestamp = st.session_state.prompt_timestamp
            
            st.markdown("### 📋 Generated Prompt")
            st.text_area(
                "Copy this prompt to your LLM:",
                prompt,
                height=300,
                key="generated_prompt_display"
            )
            
            # Download and copy buttons
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                st.download_button(
                    label="💾 Download Prompt",
                    data=prompt,
                    file_name=f"narrative_gravity_prompt_{timestamp}.txt",
                    mime="text/plain"
                )
            
            with col_btn2:
                # Simple copy button using Streamlit components
                import streamlit.components.v1 as components
                
                # Create a simple JavaScript copy function
                copy_script = f"""
                <script>
                function copyToClipboard() {{
                    const text = {json.dumps(prompt)};
                    navigator.clipboard.writeText(text).then(function() {{
                        document.getElementById('copy-msg').innerHTML = '✅ Copied!';
                        setTimeout(() => {{
                            document.getElementById('copy-msg').innerHTML = '';
                        }}, 2000);
                    }}).catch(function() {{
                        document.getElementById('copy-msg').innerHTML = '❌ Copy failed';
                        setTimeout(() => {{
                            document.getElementById('copy-msg').innerHTML = '';
                        }}, 3000);
                    }});
                }}
                </script>
                <button onclick="copyToClipboard()" style="
                    background-color: #ff4b4b; 
                    color: white; 
                    border: none; 
                    padding: 0.5rem 1rem; 
                    border-radius: 0.25rem; 
                    cursor: pointer;
                    font-size: 0.875rem;
                    margin: 0.5rem 0;
                ">📋 Copy to Clipboard</button>
                <div id="copy-msg" style="font-size: 0.8rem; margin-top: 0.5rem;"></div>
                """
                
                components.html(copy_script, height=80)
    
    with col2:
        # Framework info
        current_framework = st.session_state.current_framework
        st.markdown("### Current Framework")
        st.markdown(f"**Active:** `{current_framework}`")
        
        # Quick framework switch
        framework_data = st.session_state.framework_manager.list_frameworks()
        frameworks = [fw['name'] for fw in framework_data]
        if len(frameworks) > 1:
            quick_switch = st.selectbox(
                "Switch for this analysis:",
                frameworks,
                index=frameworks.index(current_framework) if current_framework in frameworks else 0,
                key="quick_framework_switch"
            )
            if quick_switch != current_framework:
                if st.button("🔄 Switch & Generate", key="quick_switch_btn"):
                    st.session_state.framework_manager.switch_framework(quick_switch)
                    st.session_state.current_framework = quick_switch
                    st.rerun()
        
        # Load existing analysis option
        st.markdown("### Or Load Existing Analysis")
        output_dir = Path("model_output")
        if output_dir.exists():
            json_files = list(output_dir.glob("*.json"))
            if json_files:
                selected_file = st.selectbox(
                    "Select existing analysis:",
                    [""] + [f.name for f in json_files],
                    help="Load a previously saved analysis"
                )
                if selected_file:
                    if st.button("📂 Load Analysis"):
                        with open(output_dir / selected_file, 'r') as f:
                            json_data = json.load(f)
                        # Store the loaded JSON data to populate the input field
                        st.session_state.loaded_json_content = json.dumps(json_data, indent=2)
                        st.session_state.loaded_analysis = json_data
                        st.success(f"Loaded: {selected_file}")
                        st.rerun()
            else:
                st.info("No existing analyses found")
        else:
            st.info("No model_output directory found")

    # Step 2: JSON input - this is the main required input
    st.markdown("### Step 2: Paste LLM Response (Required)")
    st.markdown("**After using the prompt with ChatGPT/Claude, paste the JSON response here:**")
    
    # Optional title input
    col_title1, col_title2 = st.columns([1, 2])
    with col_title1:
        custom_title = st.text_input(
            "Optional: Custom Title",
            placeholder="e.g., 'Churchill 1940 Speech'",
            help="Provide a descriptive name for this analysis"
        )
    
    # Determine what to show in the JSON input field
    default_json_content = ""
    if 'loaded_json_content' in st.session_state:
        default_json_content = st.session_state.loaded_json_content
        # Clear it after using it once
        del st.session_state.loaded_json_content
    
    json_input = st.text_area(
        "Paste the JSON response from your LLM:",
        value=default_json_content,
        height=150,
        placeholder='{"metadata": {...}, "scores": {...}, ...}',
        help="This is the main input needed for visualization. Get this from ChatGPT/Claude after using the generated prompt.",
        key="json_input_field"
    )
    
    # Quick test buttons
    col_test1, col_test2 = st.columns([1, 1])
    with col_test1:
        if st.button("🧪 Load Test JSON", help="Load sample JSON to test the visualization"):
            sample_json = """{
  "metadata": {
    "title": "Sample Political Analysis (analyzed by ChatGPT)",
    "model_name": "ChatGPT",
    "model_version": "gpt-4",
    "prompt_version": "2025.06.04.18.30",
    "framework_name": "moral_foundations",
    "summary": "This sample demonstrates high dignity and hope themes with strong justice orientation, typical of constructive political rhetoric."
  },
  "scores": {
    "Dignity": 0.8,
    "Tribalism": 0.1,
    "Truth": 0.7,
    "Manipulation": 0.1,
    "Justice": 0.8,
    "Resentment": 0.2,
    "Hope": 0.9,
    "Fantasy": 0.2,
    "Pragmatism": 0.8,
    "Fear": 0.1
  },
  "text_analysis": {
    "dominant_moral_foundation": "Hope",
    "key_moral_language": "better future, work together, equal dignity, evidence-based",
    "moral_intensity": "high"
  }
}"""
            st.session_state.loaded_json_content = sample_json
            st.rerun()
    
    with col_test2:
        if st.button("🏛️ Load CLI Format Test", help="Load sample CLI-format JSON (like Herbert Hoover)"):
            cli_sample_json = """{
  "metadata": {
    "title": "Test CLI Analysis (Herbert Hoover Style)",
    "model_name": "Gravity Wells Analyzer",
    "model_version": "2025.06.04",
    "framework_name": "moral_foundations",
    "summary": "This is a test analysis showing how CLI-format JSON with metadata and summary works properly in the interface."
  },
  "scores": {
    "Dignity": 0.8,
    "Tribalism": 0.1,
    "Truth": 0.7,
    "Manipulation": 0.1,
    "Justice": 0.8,
    "Resentment": 0.2,
    "Hope": 0.9,
    "Fantasy": 0.2,
    "Pragmatism": 0.8,
    "Fear": 0.2
  }
}"""
            st.session_state.loaded_json_content = cli_sample_json
            st.rerun()
    
    # Handle loaded data
    json_data = None
    if 'test_json' in st.session_state:
        st.success("✅ Test JSON loaded! Click 'Generate Visualization' below.")
        json_input = st.session_state.test_json
    elif 'loaded_analysis' in st.session_state:
        json_data = st.session_state.loaded_analysis
        st.success("✅ Analysis loaded! Click 'Generate Visualization' below.")
    
    # Step 3: Generate visualization
    st.markdown("### Step 3: Generate Visualization")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🎯 Generate Visualization", type="primary"):
            if json_input.strip():
                try:
                    # Parse JSON from the input field
                    data = json.loads(json_input)
                    
                    # Clear any test data from session state since we're using the input field
                    if 'test_json' in st.session_state:
                        del st.session_state.test_json
                    if 'loaded_analysis' in st.session_state:
                        del st.session_state.loaded_analysis
                    
                    # Detect and load the correct framework for this analysis
                    detected_framework = detect_framework_from_json(data)
                    st.info(f"🔍 Detected framework: {detected_framework}")
                    
                    # Load the framework for this specific analysis
                    analysis_framework_manager = load_framework_for_analysis(detected_framework)
                    
                    # Get timestamp for this analysis
                    timestamp = datetime.now().strftime("%Y_%m_%d_%H%M%S")
                    
                    # Check if this is already processed format (has metadata and scores)
                    if 'metadata' in data and 'scores' in data:
                        # Already processed format - use as-is but update title if custom title provided
                        visualization_data = data.copy()
                        if custom_title.strip():
                            visualization_data['metadata']['title'] = f'{custom_title} ({timestamp})'
                    else:
                        # Raw LLM format - needs transformation
                        # Extract scores from various possible keys
                        scores = {}
                        if 'moral_foundations_scores' in data:
                            scores = data['moral_foundations_scores']
                        elif 'scores' in data:
                            scores = data['scores']
                        else:
                            # Try to find scores in other keys
                            for key, value in data.items():
                                if isinstance(value, dict) and all(isinstance(v, (int, float)) for v in value.values()):
                                    scores = value
                                    break
                        
                        # Create metadata from available information
                        if custom_title.strip():
                            title = f'{custom_title} ({timestamp})'
                        else:
                            title = f'Analysis of Political Text ({timestamp})'
                        
                        # Preserve model info from LLM if provided, otherwise use defaults
                        model_name = data.get('metadata', {}).get('model_name') or data.get('model_name', 'User LLM')
                        model_version = data.get('metadata', {}).get('model_version') or data.get('model_version', 'unknown')
                        
                        metadata = {
                            'title': title,
                            'model_name': model_name,
                            'model_version': model_version,
                            'summary': ''
                        }
                        
                        # Preserve additional metadata fields if provided by LLM
                        if 'metadata' in data:
                            llm_metadata = data['metadata']
                            for key in ['prompt_version', 'dipoles_version', 'framework_version', 'framework_name']:
                                if key in llm_metadata:
                                    metadata[key] = llm_metadata[key]
                        
                        # Try to extract summary from text_analysis
                        if 'text_analysis' in data:
                            text_analysis = data['text_analysis']
                            summary_parts = []
                            if 'dominant_moral_foundation' in text_analysis:
                                summary_parts.append(f"Dominant foundation: {text_analysis['dominant_moral_foundation']}")
                            if 'key_moral_language' in text_analysis:
                                summary_parts.append(f"Key language: {text_analysis['key_moral_language']}")
                            if 'moral_intensity' in text_analysis:
                                summary_parts.append(f"Intensity: {text_analysis['moral_intensity']}")
                            metadata['summary'] = '. '.join(summary_parts) + '.'
                            
                            # Use dominant foundation for a more descriptive title if no custom title
                            if not custom_title.strip() and 'dominant_moral_foundation' in text_analysis:
                                foundation = text_analysis['dominant_moral_foundation'].replace('_', ' ').title()
                                metadata['title'] = f'Analysis: {foundation} Narrative ({timestamp})'
                        
                        visualization_data = {
                            'metadata': metadata,
                            'scores': scores,
                            'text_analysis': data.get('text_analysis', {})
                        }
                    
                    # Generate descriptive filename like CLI tools
                    analyzer = NarrativeGravityWellsElliptical()
                    model_part = analyzer.generate_model_filename_part(visualization_data['metadata'])
                    content_part = analyzer.generate_content_identifier(visualization_data['metadata']['title'])
                    filename = f"{timestamp}_{model_part}_{content_part}.json"
                    
                    filepath = Path("model_output") / filename
                    
                    # Ensure output directory exists
                    filepath.parent.mkdir(exist_ok=True)
                    
                    # Generate visualization (this will also use descriptive naming)
                    png_path = analyzer.create_visualization(visualization_data)
                    
                    # Calculate the same metrics that are shown in the visualization
                    well_scores = visualization_data.get('scores', {})
                    
                    # Calculate narrative position and metrics like the visualizer does
                    narrative_x, narrative_y = analyzer.calculate_narrative_position(well_scores)
                    calculated_metrics = analyzer.calculate_elliptical_metrics(narrative_x, narrative_y, well_scores)
                    
                    # Store the calculated metrics in our data
                    visualization_data['calculated_metrics'] = calculated_metrics
                    
                    # Re-save with the calculated metrics
                    with open(filepath, 'w') as f:
                        json.dump(visualization_data, f, indent=2)
                    
                    st.session_state.analysis_results = {
                        'json_path': str(filepath),
                        'png_path': png_path,
                        'data': visualization_data
                    }
                    
                    st.success(f"✅ Analysis saved as: {filename}")
                    
                except json.JSONDecodeError:
                    st.error("❌ Invalid JSON format. Please check your input.")
                except Exception as e:
                    st.error(f"❌ Error processing analysis: {e}")
            else:
                st.warning("⚠️ Please provide JSON data or load an existing analysis.")
    
    with col2:
        if st.session_state.analysis_results:
            # Download JSON
            with open(st.session_state.analysis_results['json_path'], 'r') as f:
                json_content = f.read()
            
            st.download_button(
                label="💾 Download JSON",
                data=json_content,
                file_name=Path(st.session_state.analysis_results['json_path']).name,
                mime="application/json"
            )
    
    with col3:
        if st.session_state.analysis_results and Path(st.session_state.analysis_results['png_path']).exists():
            # Download PNG
            with open(st.session_state.analysis_results['png_path'], 'rb') as f:
                png_content = f.read()
            
            st.download_button(
                label="🖼️ Download PNG",
                data=png_content,
                file_name=Path(st.session_state.analysis_results['png_path']).name,
                mime="image/png"
            )
    
    # Display results
    if st.session_state.analysis_results:
        display_analysis_results()

def display_analysis_results():
    """Display the analysis results"""
    st.markdown("### 📊 Analysis Results")
    
    results = st.session_state.analysis_results
    
    # Display visualization
    if Path(results['png_path']).exists():
                    st.image(results['png_path'], caption="Narrative Gravity Map Visualization", use_container_width=True)
    
    # Display metrics
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📈 Key Metrics")
        data = results['data']
        
        # Get the calculated metrics from the visualization if available
        if 'calculated_metrics' in data:
            metrics = data['calculated_metrics']
            st.metric("Narrative Elevation", f"{metrics.get('narrative_elevation', 0):.3f}")
            st.metric("Narrative Polarity", f"{metrics.get('narrative_polarity', 0):.3f}")
            st.metric("Coherence", f"{metrics.get('coherence', 0):.3f}")
            st.metric("Directional Purity", f"{metrics.get('directional_purity', 0):.3f}")
        else:
            # Fallback to original values if calculated metrics not available
            if 'moral_polarity_score' in data:
                st.metric("Moral Polarity Score", f"{data['moral_polarity_score']:.3f}")
            if 'directional_purity_score' in data:
                st.metric("Directional Purity Score", f"{data['directional_purity_score']:.3f}")
        
        # Individual well scores
        if 'moral_foundations_scores' in data:
            st.markdown("#### 🎯 Well Scores")
            scores_df = pd.DataFrame([
                {"Well": well, "Score": score}
                for well, score in data['moral_foundations_scores'].items()
            ])
            st.dataframe(scores_df, hide_index=True)
        elif 'scores' in data:
            st.markdown("#### 🎯 Well Scores")
            scores_df = pd.DataFrame([
                {"Well": well, "Score": score}
                for well, score in data['scores'].items()
            ])
            st.dataframe(scores_df, hide_index=True)
        elif 'wells' in data:
            st.markdown("#### 🎯 Well Scores")
            scores_df = pd.DataFrame([
                {"Well": well['name'], "Score": well['score']}
                for well in data['wells']
            ])
            st.dataframe(scores_df, hide_index=True)
    
    with col2:
        st.markdown("#### 📋 Analysis Summary")
        if 'text_analysis' in data:
            text_analysis = data['text_analysis']
            if 'dominant_moral_foundation' in text_analysis:
                st.write(f"**Dominant Foundation:** {text_analysis['dominant_moral_foundation']}")
            if 'key_moral_language' in text_analysis:
                st.write(f"**Key Language:** {text_analysis['key_moral_language']}")
            if 'moral_intensity' in text_analysis:
                st.write(f"**Intensity:** {text_analysis['moral_intensity']}")

def normalize_framework_name(name: str) -> str:
    """Convert framework name to consistent lowercase_underscore format"""
    # Convert to lowercase
    normalized = name.lower()
    # Replace spaces and hyphens with underscores
    normalized = normalized.replace(' ', '_').replace('-', '_')
    # Remove any other special characters except underscores and alphanumeric
    normalized = re.sub(r'[^a-z0-9_]', '', normalized)
    # Remove duplicate underscores
    normalized = re.sub(r'_+', '_', normalized)
    # Remove leading/trailing underscores
    normalized = normalized.strip('_')
    return normalized

def framework_creation_interface():
    """Interface for creating custom frameworks"""
    st.markdown('<div class="section-header">Framework Creation Wizard</div>', unsafe_allow_html=True)
    
    # Framework creation form
    with st.form("framework_creator"):
        st.markdown("### 🏗️ Create New Framework")
        
        # Basic info
        framework_name = st.text_input(
            "Framework Name",
            placeholder="e.g., environmental_ethics",
            help="Use lowercase with underscores"
        )
        
        framework_description = st.text_area(
            "Framework Description",
            placeholder="Brief description of your framework's purpose and theoretical foundation"
        )
        
        # Number of dipoles
        num_dipoles = st.number_input(
            "Number of Dipoles",
            min_value=3,
            max_value=8,
            value=5,
            help="How many dipoles will your framework include?"
        )
        
        # Weighting system option
        st.markdown("### ⚖️ Weighting System")
        use_differential_weighting = st.checkbox(
            "Use Differential Weighting",
            value=True,
            help="Assign different weights to wells based on theoretical importance"
        )
        
        weighting_philosophy = ""
        tier_system = {}
        
        if use_differential_weighting:
            weighting_philosophy = st.text_area(
                "Weighting Philosophy",
                placeholder="Explain the theoretical basis for your weighting system (e.g., 'Based on moral psychology research showing identity concerns override fairness...')",
                help="Describe why certain dimensions should have more gravitational pull than others"
            )
            
            # Tier system
            st.markdown("**Define Weight Tiers:**")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                primary_weight = st.number_input("Primary Tier Weight", min_value=0.1, max_value=2.0, value=1.0, step=0.1)
                primary_desc = st.text_input("Primary Tier Description", placeholder="Most powerful motivators")
                
            with col2:
                secondary_weight = st.number_input("Secondary Tier Weight", min_value=0.1, max_value=2.0, value=0.8, step=0.1)
                secondary_desc = st.text_input("Secondary Tier Description", placeholder="Important but secondary")
                
            with col3:
                tertiary_weight = st.number_input("Tertiary Tier Weight", min_value=0.1, max_value=2.0, value=0.6, step=0.1)
                tertiary_desc = st.text_input("Tertiary Tier Description", placeholder="Moderating factors")
            
            tier_system = {
                "primary_tier": {
                    "weight": primary_weight,
                    "description": primary_desc,
                    "wells": []
                },
                "secondary_tier": {
                    "weight": secondary_weight,
                    "description": secondary_desc,
                    "wells": []
                },
                "tertiary_tier": {
                    "weight": tertiary_weight,
                    "description": tertiary_desc,
                    "wells": []
                }
            }
        
        st.markdown("### 🔄 Define Your Dipoles")
        
        dipoles = []
        for i in range(num_dipoles):
            st.markdown(f"**Dipole {i+1}:**")
            col1, col2 = st.columns(2)
            
            with col1:
                positive = st.text_input(f"Positive Pole", key=f"pos_{i}", placeholder="e.g., Stewardship")
                pos_cues = st.text_area(f"Positive Language Cues", key=f"pos_cues_{i}", height=80, placeholder="protection, care, responsibility...")
            
            with col2:
                negative = st.text_input(f"Negative Pole", key=f"neg_{i}", placeholder="e.g., Exploitation")
                neg_cues = st.text_area(f"Negative Language Cues", key=f"neg_cues_{i}", height=80, placeholder="profit, extraction, dominance...")
            
            # Weight tier selection
            weight_tier = "primary"
            if use_differential_weighting:
                weight_tier = st.selectbox(
                    f"Weight Tier for Dipole {i+1}",
                    options=["primary", "secondary", "tertiary"],
                    key=f"tier_{i}",
                    help="Select the theoretical importance tier for this dipole"
                )
            
            if positive and negative:
                dipoles.append({
                    "name": f"{positive}/{negative}",
                    "positive_pole": positive,
                    "negative_pole": negative,
                    "positive_cues": [cue.strip() for cue in pos_cues.split(',') if cue.strip()],
                    "negative_cues": [cue.strip() for cue in neg_cues.split(',') if cue.strip()],
                    "weight_tier": weight_tier
                })
        
        # Submit button
        submitted = st.form_submit_button("🏗️ Create Framework", type="primary")
        
        if submitted and framework_name and len(dipoles) == num_dipoles:
            try:
                # Normalize the framework name for directory/file naming
                normalized_name = normalize_framework_name(framework_name)
                
                # Create framework directory using normalized name
                framework_dir = Path("frameworks") / normalized_name
                framework_dir.mkdir(parents=True, exist_ok=True)
                
                # Create dipoles.json
                dipoles_config = {
                    "framework_name": normalized_name,
                    "display_name": framework_name,  # Preserve original for display
                    "description": framework_description,
                    "version": "v1.0.0",
                    "created_date": datetime.now().isoformat(),
                    "dipoles": []
                }
                
                # Add weighting philosophy if differential weighting is used
                if use_differential_weighting and weighting_philosophy:
                    dipoles_config["weighting_philosophy"] = {
                        "description": weighting_philosophy,
                        **tier_system
                    }
                
                for i, dipole in enumerate(dipoles):
                    dipoles_config["dipoles"].append({
                        "name": dipole["name"],
                        "description": f"{dipole['positive_pole']} vs {dipole['negative_pole']} dynamics",
                        "positive": {
                            "name": dipole["positive_pole"],
                            "description": f"Represents {dipole['positive_pole'].lower()} orientation",
                            "language_cues": dipole["positive_cues"]
                        },
                        "negative": {
                            "name": dipole["negative_pole"],
                            "description": f"Represents {dipole['negative_pole'].lower()} orientation",
                            "language_cues": dipole["negative_cues"]
                        }
                    })
                
                # Create framework.json with default mathematical settings
                framework_config = {
                    "framework_name": normalized_name,
                    "display_name": framework_name,  # Preserve original for display
                    "version": "v1.0.0",
                    "description": f"{framework_name} Mathematical Framework - Implementation Parameters",
                    "ellipse": {
                        "description": "Coordinate system parameters",
                        "semi_major_axis": 1.0,
                        "semi_minor_axis": 0.7,
                        "orientation": "vertical"
                    },
                    "wells": {},
                    "scaling_factor": 0.8
                }
                
                # Add weighting philosophy to framework config if used
                if use_differential_weighting and weighting_philosophy:
                    framework_config["weighting_philosophy"] = {
                        "description": weighting_philosophy,
                        **tier_system
                    }
                
                # Generate default angles and weights
                num_wells = num_dipoles * 2
                angle_step = 360 / num_wells
                
                # Get tier weights for assignment
                tier_weights = {
                    "primary": tier_system.get("primary_tier", {}).get("weight", 1.0) if use_differential_weighting else 1.0,
                    "secondary": tier_system.get("secondary_tier", {}).get("weight", 0.8) if use_differential_weighting else 1.0,
                    "tertiary": tier_system.get("tertiary_tier", {}).get("weight", 0.6) if use_differential_weighting else 1.0
                }
                
                for i, dipole in enumerate(dipoles):
                    # Positive pole (integrative - upper half)
                    pos_angle = (i * angle_step * 2) % 360
                    if pos_angle > 180:
                        pos_angle = pos_angle - 180
                    
                    # Negative pole (disintegrative - lower half) 
                    neg_angle = pos_angle + 180
                    
                    # Get weight for this dipole's tier
                    tier = dipole.get('weight_tier', 'primary')
                    tier_weight = tier_weights[tier]
                    
                    framework_config["wells"][dipole['positive_pole']] = {
                        "angle": pos_angle,
                        "weight": tier_weight,
                        "type": "integrative",
                        "tier": tier
                    }
                    framework_config["wells"][dipole['negative_pole']] = {
                        "angle": neg_angle,
                        "weight": -tier_weight,
                        "type": "disintegrative",
                        "tier": tier
                    }
                    
                    # Update tier_system with well names for tracking
                    if use_differential_weighting:
                        tier_key = f"{tier}_tier"
                        if tier_key in tier_system:
                            tier_system[tier_key]["wells"].extend([dipole['positive_pole'], dipole['negative_pole']])
                
                # Save files
                with open(framework_dir / "dipoles.json", 'w') as f:
                    json.dump(dipoles_config, f, indent=2)
                
                with open(framework_dir / "framework.json", 'w') as f:
                    json.dump(framework_config, f, indent=2)
                
                # Create README
                readme_content = f"""# {framework_name} Framework

{framework_description}

## Dipoles

"""
                for dipole in dipoles:
                    readme_content += f"- **{dipole['name']}**: {dipole['positive_pole']} vs {dipole['negative_pole']}\n"
                
                with open(framework_dir / "README.md", 'w') as f:
                    f.write(readme_content)
                
                st.success(f"✅ Framework '{framework_name}' created successfully!")
                st.info(f"📁 Directory: `frameworks/{normalized_name}/`")
                st.info("You can now switch to your new framework and generate prompts for testing.")
                
                # Refresh framework manager
                st.session_state.framework_manager = FrameworkManager()
                
            except Exception as e:
                st.error(f"❌ Error creating framework: {e}")
        
        elif submitted:
            st.warning("⚠️ Please fill in all required fields and define all dipoles.")

def visualization_interface():
    """Interface for viewing and comparing visualizations"""
    st.markdown('<div class="section-header">Visualization Gallery</div>', unsafe_allow_html=True)
    
    # Load existing visualizations
    output_dir = Path("model_output")
    if output_dir.exists():
        png_files = list(output_dir.glob("*.png"))
        json_files = list(output_dir.glob("*.json"))
        
        if png_files:
            st.markdown("### 🖼️ Recent Visualizations")
            
            # Create thumbnail grid
            cols = st.columns(3)
            for i, png_file in enumerate(sorted(png_files, reverse=True)[:9]):  # Show last 9
                with cols[i % 3]:
                    st.image(str(png_file), caption=png_file.stem, use_container_width=True)
                    
                    # Check if this is a comparative visualization
                    is_comparative = "_comparative_analysis" in png_file.stem
                    
                    if is_comparative:
                        # For comparative visualizations, show a different View Details button
                        if st.button(f"📊 View Details", key=f"details_{i}"):
                            # Store comparative visualization info 
                            st.session_state.comparative_results = {
                                'png_path': str(png_file),
                                'is_comparative': True,
                                'filename': png_file.stem
                            }
                            st.rerun()
                    else:
                        # Original logic for individual analyses
                        # Find corresponding JSON
                        json_pattern = png_file.stem.replace("openai_gpt_4_", "").replace("_", "*") + ".json"
                        matching_jsons = list(output_dir.glob(f"*{json_pattern}*"))
                        
                        if matching_jsons:
                            if st.button(f"📊 View Details", key=f"details_{i}"):
                                with open(matching_jsons[0], 'r') as f:
                                    data = json.load(f)
                                
                                st.session_state.analysis_results = {
                                    'json_path': str(matching_jsons[0]),
                                    'png_path': str(png_file),
                                    'data': data
                                }
                                st.rerun()
        else:
            st.info("📊 No visualizations found. Create some analyses first!")
    else:
        st.info("📁 model_output directory not found.")
    
    # Display results if View Details was clicked
    if st.session_state.analysis_results:
        display_analysis_results()
    
    # Display comparative results if comparative View Details was clicked
    if hasattr(st.session_state, 'comparative_results') and st.session_state.comparative_results:
        display_comparative_results()

def display_comparative_results():
    """Display the comparative results"""
    st.markdown("### 📊 Comparative Analysis Results")
    
    results = st.session_state.comparative_results
    
    # Display visualization
    if Path(results['png_path']).exists():
                        st.image(results['png_path'], caption="Narrative Distance Analysis", use_container_width=True)
    
    # Display comparative analysis information
    st.markdown("#### 📈 Comparative Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📊 Analysis Type:** Comparative Visualization")
        st.markdown("**🎯 Purpose:** Shows narrative distance between two narratives")
        st.markdown("**📏 Key Metric:** Distance between narrative centers")
        st.markdown("**🔗 Visual Elements:**")
        st.markdown("- Two narrative centers positioned within the ellipse")
        st.markdown("- Dotted line connecting the narrative centers") 
        st.markdown("- Narrative labels positioned over each center")
    
    with col2:
        st.markdown("**🎨 Visualization Features:**")
        st.markdown("- Wells positioned on ellipse boundary")
        st.markdown("- Comparative metrics on left side")
        st.markdown("- Complete metadata at bottom of image")
        st.markdown("- No legend (labels are directly on chart)")
        
        # Extract timestamp from filename if possible
        filename = results['filename']
        if filename.startswith(tuple('0123456789')):
            # Extract timestamp from beginning of filename
            timestamp_part = filename.split('_')[:3]  # YYYY_MM_DD
            if len(timestamp_part) == 3:
                try:
                    year, month, day = timestamp_part
                    st.markdown(f"**📅 Created:** {year}-{month}-{day}")
                except:
                    pass
    
    # Provide guidance for creating new comparisons
    st.markdown("#### 🔍 Create New Comparisons")
    st.info("To create new comparative analyses, go to the 'Compare Analysis' tab and select two analyses from the same framework.")
    
    # Add button to go to comparison interface
    if st.button("🔍 Go to Compare Analysis Tab"):
        # Clear the current results and redirect focus
        st.session_state.comparative_results = None
        st.info("💡 Click on the 'Compare Analysis' tab above to create new comparisons.")

def comparison_interface():
    """Interface for comparing analyses from the same framework"""
    st.markdown('<div class="section-header">Compare Analyses</div>', unsafe_allow_html=True)
    
    # Framework selection
    framework_data = st.session_state.framework_manager.list_frameworks()
    frameworks = [fw['name'] for fw in framework_data]
    
    selected_framework = st.selectbox(
        "Select framework to compare:",
        frameworks,
        help="Only analyses created with this framework will be shown for comparison"
    )
    
    # Load analyses for the selected framework
    output_dir = Path("model_output")
    if output_dir.exists():
        json_files = list(output_dir.glob("*.json"))
        
        # Filter analyses by framework
        framework_analyses = []
        for json_file in json_files:
            try:
                with open(json_file, 'r') as f:
                    data = json.load(f)
                detected_framework = detect_framework_from_json(data)
                if detected_framework == selected_framework:
                    framework_analyses.append(json_file)
            except Exception:
                continue
        
        if len(framework_analyses) >= 2:
            st.markdown(f"### 🔍 Compare Analyses ({selected_framework} framework)")
            st.info(f"Found {len(framework_analyses)} analyses using the {selected_framework} framework")
            
            col1, col2 = st.columns(2)
            
            with col1:
                analysis1 = st.selectbox(
                    "Select first analysis:",
                    [""] + [f.name for f in framework_analyses],
                    key="compare1"
                )
            
            with col2:
                analysis2 = st.selectbox(
                    "Select second analysis:",
                    [""] + [f.name for f in framework_analyses],
                    key="compare2"
                )
            
            if analysis1 and analysis2 and analysis1 != analysis2:
                if st.button("🔍 Compare Analyses", type="primary"):
                    try:
                        # Load both analyses
                        with open(output_dir / analysis1, 'r') as f:
                            data1 = json.load(f)
                        with open(output_dir / analysis2, 'r') as f:
                            data2 = json.load(f)
                        
                        # Create comparison visualization
                        create_comparison_chart(data1, data2, analysis1, analysis2, selected_framework)
                        
                    except Exception as e:
                        st.error(f"Error creating comparison: {e}")
        elif len(framework_analyses) == 1:
            st.info(f"Only 1 analysis found for {selected_framework} framework. Need at least 2 analyses to compare.")
        else:
            st.info(f"No analyses found for {selected_framework} framework. Create some analyses first!")
    else:
        st.info("📁 model_output directory not found.")

def create_comparison_chart(data1, data2, name1, name2, selected_framework_name: str):
    """Create a comparison chart between two analyses"""
    st.markdown("### 📊 Analysis Comparison")

    # Ensure the correct framework is active for the visualizer
    try:
        st.session_state.framework_manager.switch_framework(selected_framework_name)
        st.info(f"Switched to {selected_framework_name} for comparison visualization.")
    except Exception as e:
        st.error(f"Error switching framework to {selected_framework_name}: {e}")
        return
    
    # Extract scores from current format
    scores1 = data1.get('scores')
    scores2 = data2.get('scores')
    
    if scores1 and scores2:
        # Common wells
        common_wells = set(scores1.keys()) & set(scores2.keys())
        
        if common_wells:
            # Create comparative visualization
            try:
                analyzer = NarrativeGravityWellsElliptical()
                
                # Convert data to the format expected by create_comparative_visualization
                analyses = [data1, data2]
                
                # Generate comparative visualization
                output_path = analyzer.create_comparative_visualization(analyses)
                
                # Display the comparative visualization
                if Path(output_path).exists():
                    st.image(output_path, caption="Comparative Analysis", use_container_width=True)
                    
                    # Calculate and display narrative distance
                    well_scores1 = scores1
                    well_scores2 = scores2
                    
                    pos1 = analyzer.calculate_narrative_position(well_scores1)
                    pos2 = analyzer.calculate_narrative_position(well_scores2)
                    
                    distance = analyzer.calculate_elliptical_distance(pos1, pos2)
                    
                    st.metric("Narrative Distance", f"{distance:.3f}", 
                             help="Distance between the two narrative centers")
                    
                    # Add the improved score differences table below the visualization
                    st.markdown("### 📊 Score Differences")
                    
                    # Extract actual narrative titles from metadata
                    title1 = data1.get('metadata', {}).get('title', name1)
                    title2 = data2.get('metadata', {}).get('title', name2)
                    
                    # Shorten titles if they're too long
                    if len(title1) > 40:
                        title1 = title1[:37] + "..."
                    if len(title2) > 40:
                        title2 = title2[:37] + "..."
                    
                    # Create comparison DataFrame
                    comparison_data = []
                    for well in sorted(common_wells):
                        comparison_data.append({
                            'Well': well,
                            title1: scores1[well],
                            title2: scores2[well],
                            'Difference': scores2[well] - scores1[well]
                        })
                    
                    df = pd.DataFrame(comparison_data)
                    
                    # Round numerical values for cleaner display
                    for col in [title1, title2, 'Difference']:
                        if col in df.columns:
                            df[col] = df[col].round(3)
                    
                    # Use Streamlit's column configuration for better responsive display
                    column_config = {
                        "Well": st.column_config.TextColumn(
                            "Well",
                            width="medium",
                            help="The foundation being compared"
                        ),
                        title1: st.column_config.NumberColumn(
                            title1,
                            width="medium",
                            format="%.3f",
                            help=f"Scores for {title1}"
                        ),
                        title2: st.column_config.NumberColumn(
                            title2,
                            width="medium", 
                            format="%.3f",
                            help=f"Scores for {title2}"
                        ),
                        "Difference": st.column_config.NumberColumn(
                            "Difference",
                            width="small",
                            format="%.3f",
                            help=f"Difference ({title2} - {title1})"
                        )
                    }
                    
                    st.dataframe(
                        df, 
                        hide_index=True, 
                        use_container_width=True,
                        column_config=column_config
                    )
                    
                else:
                    st.error("Failed to generate comparative visualization")
                    
            except Exception as e:
                st.error(f"Error creating comparison: {e}")
                # Fallback to bar chart if visualization fails
                create_fallback_bar_chart(data1, data2, name1, name2, scores1, scores2, common_wells)
        else:
            st.error("No common wells found between the analyses.")
    else:
        st.error("Could not extract scores from one or both analyses. Please ensure both analyses use the current JSON format with 'scores' key.")

def create_fallback_bar_chart(data1, data2, name1, name2, scores1, scores2, common_wells):
    """Create fallback bar chart if visualization fails"""
    # Extract actual narrative titles from metadata
    title1 = data1.get('metadata', {}).get('title', name1)
    title2 = data2.get('metadata', {}).get('title', name2)
    
    # Shorten titles if they're too long
    if len(title1) > 40:
        title1 = title1[:37] + "..."
    if len(title2) > 40:
        title2 = title2[:37] + "..."
    
    # Create comparison DataFrame
    comparison_data = []
    for well in sorted(common_wells):
        comparison_data.append({
            'Well': well,
            title1: scores1[well],
            title2: scores2[well],
            'Difference': scores2[well] - scores1[well]
        })
    
    df = pd.DataFrame(comparison_data)
    
    # Bar chart comparison
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name=title1,
        x=df['Well'],
        y=df[title1],
        marker_color='lightblue'
    ))
    
    fig.add_trace(go.Bar(
        name=title2,
        x=df['Well'],
        y=df[title2],
        marker_color='lightcoral'
    ))
    
    fig.update_layout(
        title="Wells Scores Comparison (Fallback)",
        xaxis_title="Wells",
        yaxis_title="Scores",
        barmode='group',
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Metrics comparison using calculated_metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Narrative Elevation
        if ('calculated_metrics' in data1 and 'narrative_elevation' in data1['calculated_metrics'] and
            'calculated_metrics' in data2 and 'narrative_elevation' in data2['calculated_metrics']):
            val1 = data1['calculated_metrics']['narrative_elevation']
            val2 = data2['calculated_metrics']['narrative_elevation']
            delta = val2 - val1
            st.metric("Narrative Elevation", f"{val2:.3f}", delta=f"{delta:+.3f}")
    
    with col2:
        # Narrative Polarity
        if ('calculated_metrics' in data1 and 'narrative_polarity' in data1['calculated_metrics'] and
            'calculated_metrics' in data2 and 'narrative_polarity' in data2['calculated_metrics']):
            val1 = data1['calculated_metrics']['narrative_polarity']
            val2 = data2['calculated_metrics']['narrative_polarity']
            delta = val2 - val1
            st.metric("Narrative Polarity", f"{val2:.3f}", delta=f"{delta:+.3f}")
    
    with col3:
        # Coherence
        if ('calculated_metrics' in data1 and 'coherence' in data1['calculated_metrics'] and
            'calculated_metrics' in data2 and 'coherence' in data2['calculated_metrics']):
            val1 = data1['calculated_metrics']['coherence']
            val2 = data2['calculated_metrics']['coherence']
            delta = val2 - val1
            st.metric("Coherence", f"{val2:.3f}", delta=f"{delta:+.3f}")
    
    with col4:
        # Directional Purity
        if ('calculated_metrics' in data1 and 'directional_purity' in data1['calculated_metrics'] and
            'calculated_metrics' in data2 and 'directional_purity' in data2['calculated_metrics']):
            val1 = data1['calculated_metrics']['directional_purity']
            val2 = data2['calculated_metrics']['directional_purity']
            delta = val2 - val1
            st.metric("Directional Purity", f"{val2:.3f}", delta=f"{delta:+.3f}")
    
    # Analysis metadata comparison (simplified since metadata is now in visualization)
    st.markdown("### 📋 Analysis Summaries")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**{title1}**")
        if 'metadata' in data1 and 'summary' in data1['metadata']:
            st.write(data1['metadata']['summary'])
    
    with col2:
        st.markdown(f"**{title2}**")
        if 'metadata' in data2 and 'summary' in data2['metadata']:
            st.write(data2['metadata']['summary'])

def detect_framework_from_json(data):
    """Detect which framework a JSON analysis was created with"""
    # Check for direct framework_name field first
    if 'framework_name' in data:
        return data['framework_name']
    
    if 'metadata' in data:
        # Check for explicit framework info
        if 'framework_name' in data['metadata']:
            return data['metadata']['framework_name']
        if 'framework' in data['metadata']:
            return data['metadata']['framework']
        
        # Try to infer from prompt version or other clues
        if 'prompt_version' in data['metadata']:
            # Could map prompt versions to frameworks if needed
            pass
    
    # Check well names to infer framework
    if 'wells' in data:
        well_names = {well['name'] for well in data['wells']}
    elif 'scores' in data:
        well_names = set(data['scores'].keys())
    else:
        well_names = set()
    
    # Current framework wells
    current_wells = {"Dignity", "Tribalism", "Truth", "Manipulation", "Justice", "Resentment", "Hope", "Fantasy", "Pragmatism", "Fear"}
    
    # Check if it matches current framework
    if well_names.issubset(current_wells) or current_wells.issubset(well_names):
        return "moral_foundations"  # Default current framework
    
    # Could add other framework detection logic here
    # For now, default to moral_foundations
    return "moral_foundations"

def load_framework_for_analysis(framework_name):
    """Load a specific framework for analysis"""
    try:
        framework_manager = FrameworkManager()
        available_frameworks = [fw['name'] for fw in framework_manager.list_frameworks()]
        
        if framework_name in available_frameworks:
            framework_manager.switch_framework(framework_name)
            return framework_manager
        else:
            st.warning(f"Framework '{framework_name}' not found. Using default.")
            return framework_manager
    except Exception as e:
        st.error(f"Error loading framework: {e}")
        return FrameworkManager()  # Return default

def main():
    """Main application function"""
    initialize_session_state()
    sidebar_framework_manager()
    main_analysis_interface()
    
    # Footer
    st.markdown("---")
    st.markdown(
        '<div style="text-align: center; color: #666; font-size: 0.8em;">'
        'Narrative Gravity Maps v2025.06.04 | Built with Streamlit'
        '</div>',
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main() 