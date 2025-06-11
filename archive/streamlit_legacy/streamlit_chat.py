#!/usr/bin/env python3
"""
Simple Streamlit Chat Interface for Narrative Gravity Analysis
"""

import streamlit as st
import sys
from pathlib import Path
from datetime import datetime

# Add src to path for imports
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

# Import the existing chatbot
from narrative_gravity.chatbot import NarrativeGravityBot

# Configure the page
st.set_page_config(
    page_title="Narrative Gravity Chat",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize the chatbot
@st.cache_resource
def get_chatbot():
    """Initialize chatbot once and cache it"""
    return NarrativeGravityBot()

def initialize_session_state():
    """Initialize session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "chatbot" not in st.session_state:
        st.session_state.chatbot = get_chatbot()

def main():
    """Main Streamlit app"""
    initialize_session_state()
    
    st.title("🎯 Narrative Gravity Analysis Chat")
    st.markdown("**Conversational interface for political discourse analysis**")
    
    # Sidebar with framework information
    with st.sidebar:
        st.header("🛠️ Framework Settings")
        
        bot = st.session_state.chatbot
        current_fw = bot.framework_interface.get_current_framework()
        display_name = bot.framework_interface._get_display_name(current_fw) if current_fw else "None"
        
        st.info(f"**Current Framework:** {display_name}")
        
        # Show available frameworks
        frameworks = bot.framework_interface.get_available_frameworks()
        st.markdown("**Available Frameworks:**")
        for fw in frameworks:
            fw_display = bot.framework_interface._get_display_name(fw)
            if fw == current_fw:
                st.markdown(f"• ✅ {fw_display}")
            else:
                st.markdown(f"• {fw_display}")
        
        st.markdown("---")
        st.markdown("**💡 What you can do:**")
        st.markdown("• Analyze political texts")
        st.markdown("• Switch frameworks mid-conversation")
        st.markdown("• Create new frameworks")
        st.markdown("• Compare analyses")
        
        if st.button("🔄 Clear Chat"):
            st.session_state.messages = []
            st.session_state.chatbot = get_chatbot()
            st.rerun()
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Show metadata if available
            if "metadata" in message and message["metadata"]:
                with st.expander("🔍 Details", expanded=False):
                    st.json(message["metadata"])
    
    # Chat input
    if prompt := st.chat_input("Ask me to analyze a political text, create a framework, or switch frameworks..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get bot response
        with st.chat_message("assistant"):
            with st.spinner("Analyzing..."):
                try:
                    response = st.session_state.chatbot.process_query(prompt)
                    
                    st.markdown(response.content)
                    
                    # Store assistant response
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": response.content,
                        "metadata": response.metadata
                    })
                    
                    # Show response type and confidence if available
                    if response.metadata:
                        info_items = []
                        if 'classification' in response.metadata:
                            info_items.append(f"Type: {response.metadata['classification']}")
                        if 'confidence' in response.metadata:
                            confidence = response.metadata['confidence']
                            info_items.append(f"Confidence: {confidence:.2f}")
                        if 'response_type' in response.metadata:
                            info_items.append(f"Response: {response.metadata['response_type']}")
                        
                        if info_items:
                            st.caption(" | ".join(info_items))
                
                except Exception as e:
                    error_msg = f"❌ Error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": error_msg,
                        "metadata": {"error": True}
                    })

    # Instructions at the bottom
    with st.expander("💡 How to use this chat interface", expanded=False):
        st.markdown("""
        **Basic Commands:**
        • Paste any political text to analyze it
        • "Switch to [framework name]" to change frameworks
        • "Create a framework based on..." to build new frameworks
        • "Compare this analysis with..." to compare results
        
        **Example Queries:**
        • "Analyze this speech: [paste text]"
        • "Switch to Civic Virtue framework"
        • "Create a framework based on John Stuart Mill's concept of liberty"
        • "What frameworks are available?"
        
        **Large Texts:**
        • This interface supports large text inputs (up to 1.2MB)
        • Perfect for analyzing full speeches, documents, or articles
        
        **Framework Creation:**
        • The chat will guide you through creating custom analytical frameworks
        • Same conversational process used to create the Fukuyama Identity Framework
        """)

if __name__ == "__main__":
    main() 