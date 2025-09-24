#!/usr/bin/env python3
"""
Analyze how frameworks are provided in show work vs production
"""

def analyze_framework_provision():
    """Compare how frameworks are provided in both approaches."""
    
    print("=== FRAMEWORK PROVISION ANALYSIS ===")
    print()
    
    print("1. SHOW WORK APPROACH:")
    print("   - Uses custom prompt template")
    print("   - Framework provided as: f\"=== FRAMEWORK ===\\n{self.framework_content}\\n\"")
    print("   - Framework is provided as PLAIN TEXT")
    print("   - No base64 encoding")
    print("   - No specific instructions about framework usage")
    print()
    
    print("2. PRODUCTION APPROACH:")
    print("   - Uses standard prompt_3run.yaml template")
    print("   - Framework provided via create_analysis_prompt() function")
    print("   - Framework is BASE64 ENCODED")
    print("   - Framework provided as: \"=== FRAMEWORK 1 (base64 encoded) ===\\n{framework_b64}\"")
    print("   - Includes specific instructions: \"Apply the framework's dimensional definitions precisely\"")
    print()
    
    print("3. KEY DIFFERENCES:")
    print()
    print("   A. ENCODING:")
    print("      - Show Work: Plain text framework")
    print("      - Production: Base64 encoded framework")
    print("      - This could affect how the LLM processes the framework")
    print()
    
    print("   B. INSTRUCTIONS:")
    print("      - Show Work: Generic \"Apply the framework's dimensional definitions precisely\"")
    print("      - Production: Same instruction but in structured template")
    print("      - Both have the same instruction, so this shouldn't matter")
    print()
    
    print("   C. FRAMEWORK FORMAT:")
    print("      - Show Work: \"=== FRAMEWORK ===\"")
    print("      - Production: \"=== FRAMEWORK 1 (base64 encoded) ===\"")
    print("      - The \"(base64 encoded)\" label might confuse the LLM")
    print()
    
    print("   D. PROMPT STRUCTURE:")
    print("      - Show Work: Custom prompt with direct framework inclusion")
    print("      - Production: Uses prompt_builder.py with placeholders")
    print("      - Production has more structured approach")
    print()
    
    print("4. HYPOTHESIS:")
    print("   The LLM might be ignoring the framework because:")
    print("   - Base64 encoding makes it harder to parse")
    print("   - The \"(base64 encoded)\" label suggests it needs decoding")
    print("   - The LLM might not understand it should use the provided framework")
    print("   - The framework content might be too long or complex")
    print()
    
    print("5. RECOMMENDATIONS:")
    print("   A. Test with plain text framework in production")
    print("   B. Add explicit instructions to use the provided framework")
    print("   C. Make framework usage more prominent in the prompt")
    print("   D. Test with shorter, simpler framework descriptions")

if __name__ == "__main__":
    analyze_framework_provision()
