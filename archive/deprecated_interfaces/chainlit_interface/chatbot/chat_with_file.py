#!/usr/bin/env python3
"""
Simple File-Based Chatbot - Avoids terminal input buffer issues completely
"""

import sys
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

def main():
    print("🤖 Narrative Gravity Analysis Chatbot")
    print("=" * 50)
    print("📝 Create a file called 'input.txt' and paste your political text there")
    print("💬 Or type short queries directly")
    print("🚪 Type 'quit' to exit")
    print("=" * 50)
    
    from narrative_gravity.chatbot import NarrativeGravityBot
    
    bot = NarrativeGravityBot()
    current_framework = bot.framework_interface.get_current_framework()
    display_name = bot.framework_interface._get_display_name(current_framework) if current_framework else "None"
    print(f"🎯 Current Framework: {display_name}")
    
    while True:
        try:
            print(f"\n{'-'*50}")
            
            # Check if input.txt exists
            input_file = Path("input.txt")
            if input_file.exists():
                print("📄 Found input.txt - processing file content...")
                
                with open(input_file, 'r') as f:
                    file_content = f.read().strip()
                
                if file_content:
                    print(f"📊 File content: {len(file_content)} characters")
                    
                    # Process the file content
                    response = bot.process_query(file_content)
                    
                    print(f"\n🤖 Bot ({response.response_type}):")
                    print("-" * 40)
                    print(response.content)
                    
                    if response.metadata:
                        interesting = {k: v for k, v in response.metadata.items() 
                                     if k in ['classification', 'confidence', 'auto_analyzed']}
                        if interesting:
                            print(f"\n📊 Debug: {interesting}")
                    
                    # Remove the file after processing
                    input_file.unlink()
                    print(f"\n✅ Processed and removed input.txt")
                    print("💡 Create a new input.txt for more analysis")
                    continue
            
            # Regular terminal input for short queries
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if not user_input:
                continue
            
            # Process query
            response = bot.process_query(user_input)
            
            print(f"\n🤖 Bot ({response.response_type}):")
            print("-" * 40)
            print(response.content)
            
            if response.metadata:
                interesting = {k: v for k, v in response.metadata.items() 
                             if k in ['classification', 'confidence']}
                if interesting:
                    print(f"\n📊 Debug: {interesting}")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def create_sample_file():
    """Create a sample input.txt with the political text"""
    
    sample_text = """Do you remember when we're talking about people coming in? They're trying to deny it. People are flowing and they said, "No, I don't see any people." It's like, what's wrong? But then we saw airplanes going overhead. We said, what the hell are those airplanes doing? Big Boeing 757s were traveling right overhead, loaded up with people. I say, "Where the hell are those planes going?" They were loaded up with migrants coming in illegally flying in by plane paid for by the US government. I'll tell you, they are sick. Remember that day? That was the day we found out that not only do we have to defend it here, we have to defend it not only in the water, but we have to defend it in the air. The planes were going over us. I said, "What the hell is that?" I banned all welfare to illegals and I signed an order that will end automatic citizenship for the children of illegal aliens, no citizenship. For years, Joe Biden and the media told us that stopping the flood of illegal immigration was absolutely impossible."""
    
    with open("input.txt", "w") as f:
        f.write(sample_text)
    
    print("✅ Created input.txt with sample political text")
    print("🚀 Now run: python3 chat_with_file.py")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "sample":
        create_sample_file()
    else:
        main() 