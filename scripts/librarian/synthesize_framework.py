#!/usr/bin/env python3
"""
Framework Synthesis Tool

Automated framework documentation generator using DiscernusLibrarian methodology.

Copyright (C) 2025  Discernus Team

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import argparse
import sys
import os
import json
from pathlib import Path

# Import the main librarian functionality
try:
    from .discernuslibrarian import DiscernusLibrarian
except ImportError:
    # Fallback for direct execution
    sys.path.append(os.path.dirname(__file__))
    from discernuslibrarian import DiscernusLibrarian

def main():
    parser = argparse.ArgumentParser(
        description="Generate framework documentation using DiscernusLibrarian synthesis"
    )
    parser.add_argument(
        "framework_path", 
        help="Path to the framework file to synthesize"
    )
    parser.add_argument(
        "--type", 
        choices=["overview", "validation", "guide", "enhanced-validation"],
        default="overview",
        help="Type of synthesis to generate"
    )
    parser.add_argument(
        "--data", 
        help="Path to reliability/validation data JSON file"
    )
    parser.add_argument(
        "--output", 
        help="Output file for synthesis report"
    )
    parser.add_argument(
        "--format", 
        choices=["markdown", "html", "json"],
        default="markdown",
        help="Output format"
    )
    
    args = parser.parse_args()
    
    if not os.path.exists(args.framework_path):
        print(f"Error: Framework file not found: {args.framework_path}")
        sys.exit(1)
    
    # Load validation data if provided
    validation_data = None
    if args.data:
        if not os.path.exists(args.data):
            print(f"Error: Data file not found: {args.data}")
            sys.exit(1)
        with open(args.data, 'r') as f:
            validation_data = json.load(f)
    
    # Initialize librarian
    librarian = DiscernusLibrarian()
    
    print(f"Synthesizing {args.type} for framework: {args.framework_path}")
    
    try:
        # Perform synthesis using librarian
        if args.type == "overview":
            result = librarian.generate_academic_overview(args.framework_path)
        elif args.type == "validation":
            result = librarian.generate_validation_report(
                args.framework_path, 
                validation_data=validation_data
            )
        elif args.type == "guide":
            result = librarian.generate_usage_guide(args.framework_path)
        elif args.type == "enhanced-validation":
            result = librarian.generate_enhanced_validation_report(
                args.framework_path,
                validation_data=validation_data
            )
        
        # Format output
        if args.format == "json":
            output = json.dumps(result, indent=2)
        elif args.format == "html":
            # Convert markdown to HTML if needed
            output = result.get('html_content', result.get('content', ''))
        else:  # markdown
            output = result.get('content', str(result))
        
        # Save or print output
        if args.output:
            with open(args.output, 'w') as f:
                f.write(output)
            print(f"Synthesis report saved to: {args.output}")
        else:
            print("\n" + "="*60)
            print(f"FRAMEWORK {args.type.upper()} SYNTHESIS")
            print("="*60)
            print(output)
            
    except Exception as e:
        print(f"Error synthesizing framework: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
