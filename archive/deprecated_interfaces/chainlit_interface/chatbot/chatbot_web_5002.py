#!/usr/bin/env python3
"""
Simple Web Interface for Narrative Gravity Analysis Chatbot (Port 5002)
"""

import sys
from pathlib import Path
from flask import Flask, render_template, request, jsonify
import json

# Add src to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

from narrative_gravity.chatbot import NarrativeGravityBot

app = Flask(__name__)

# Configure for large file uploads (1.5MB limit)
app.config['MAX_CONTENT_LENGTH'] = 1.5 * 1024 * 1024  # 1.5MB

# Initialize chatbot
bot = NarrativeGravityBot()

@app.route('/')
def index():
    """Main chatbot interface"""
    current_framework = bot.framework_interface.get_current_framework()
    display_name = bot.framework_interface._get_display_name(current_framework) if current_framework else "None"
    
    frameworks = bot.framework_interface.get_available_frameworks()
    
    return render_template('chatbot.html', 
                         current_framework=display_name,
                         frameworks=frameworks)

@app.route('/chat', methods=['POST'])
def chat():
    """Process chatbot query"""
    try:
        data = request.get_json()
        user_input = data.get('message', '').strip()
        
        if not user_input:
            return jsonify({'error': 'No message provided'}), 400
        
        # Check message length (1.2MB limit)
        if len(user_input.encode('utf-8')) > 1.2 * 1024 * 1024:
            return jsonify({'error': 'Message too long (max 1.2MB)'}), 400
        
        # Process with chatbot
        response = bot.process_query(user_input)
        
        return jsonify({
            'response': response.content,
            'response_type': response.response_type,
            'metadata': response.metadata
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/switch_framework', methods=['POST'])
def switch_framework():
    """Switch analysis framework"""
    try:
        data = request.get_json()
        framework_name = data.get('framework', '').strip()
        
        if not framework_name:
            return jsonify({'error': 'No framework specified'}), 400
        
        # Switch framework
        success, message = bot.framework_interface.switch_framework(framework_name)
        
        if success:
            bot.context.set_framework(framework_name)
            display_name = bot.framework_interface._get_display_name(framework_name)
            return jsonify({
                'success': True,
                'message': f"Switched to {display_name}",
                'framework': display_name
            })
        else:
            return jsonify({'error': message}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/status')
def status():
    """Get chatbot status"""
    current_framework = bot.framework_interface.get_current_framework()
    display_name = bot.framework_interface._get_display_name(current_framework) if current_framework else "None"
    
    session_summary = bot.get_session_summary()
    
    return jsonify({
        'current_framework': display_name,
        'session': session_summary,
        'llm_available': bot.llm_classifier.llm_available
    })

if __name__ == '__main__':
    print("🚀 Starting Narrative Gravity Analysis Chatbot Web Interface")
    print("🌐 Open your browser to: http://localhost:5002")
    print("📝 Supports text input up to 1.2MB (3x largest corpus file)")
    print("🛠️  Framework Creation: Try 'Create a framework based on...'")
    print()
    
    # Check if templates directory exists
    templates_dir = Path("templates")
    if not templates_dir.exists():
        print("⚠️  Creating templates directory...")
        templates_dir.mkdir()
    
    app.run(debug=True, host='0.0.0.0', port=5002) 