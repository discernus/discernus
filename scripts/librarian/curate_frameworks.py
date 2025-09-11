#!/usr/bin/env python3
"""
Framework Curation Tool

Framework collection management and organization using DiscernusLibrarian methodology.

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
import shutil
from pathlib import Path
from collections import defaultdict

# Import the main librarian functionality
try:
    from .discernuslibrarian import DiscernusLibrarian
except ImportError:
    # Fallback for direct execution
    sys.path.append(os.path.dirname(__file__))
    from discernuslibrarian import DiscernusLibrarian

def main():
    parser = argparse.ArgumentParser(
        description="Curate and organize framework collections"
    )
    parser.add_argument(
        "frameworks_dir", 
        help="Directory containing frameworks to curate"
    )
    parser.add_argument(
        "--by-category", 
        action="store_true",
        help="Organize frameworks by category"
    )
    parser.add_argument(
        "--update-metadata", 
        action="store_true",
        help="Update framework metadata"
    )
    parser.add_argument(
        "--index", 
        action="store_true",
        help="Generate collection index"
    )
    parser.add_argument(
        "--output", 
        help="Output directory for curated frameworks"
    )
    parser.add_argument(
        "--source", 
        help="Source metadata file for updates"
    )
    
    args = parser.parse_args()
    
    if not os.path.exists(args.frameworks_dir):
        print(f"Error: Frameworks directory not found: {args.frameworks_dir}")
        sys.exit(1)
    
    # Initialize librarian
    librarian = DiscernusLibrarian()
    
    # Find all framework files
    framework_files = []
    for root, dirs, files in os.walk(args.frameworks_dir):
        for file in files:
            if file.endswith('.md') and 'framework' in file.lower():
                framework_files.append(os.path.join(root, file))
    
    print(f"Found {len(framework_files)} framework files")
    
    try:
        if args.by_category:
            print("Organizing frameworks by category...")
            categories = defaultdict(list)
            
            for framework_file in framework_files:
                # Extract category from framework
                category = librarian.extract_framework_category(framework_file)
                categories[category].append(framework_file)
            
            if args.output:
                # Create organized directory structure
                for category, files in categories.items():
                    category_dir = os.path.join(args.output, category)
                    os.makedirs(category_dir, exist_ok=True)
                    
                    for file in files:
                        filename = os.path.basename(file)
                        shutil.copy2(file, os.path.join(category_dir, filename))
                
                print(f"Organized frameworks saved to: {args.output}")
            else:
                # Print organization
                for category, files in categories.items():
                    print(f"\n{category}:")
                    for file in files:
                        print(f"  - {os.path.basename(file)}")
        
        if args.update_metadata:
            print("Updating framework metadata...")
            
            source_metadata = {}
            if args.source and os.path.exists(args.source):
                with open(args.source, 'r') as f:
                    source_metadata = json.load(f)
            
            for framework_file in framework_files:
                librarian.update_framework_metadata(
                    framework_file, 
                    source_metadata=source_metadata
                )
            
            print("Metadata updates completed")
        
        if args.index:
            print("Generating collection index...")
            
            index_content = librarian.generate_collection_index(framework_files)
            
            if args.output:
                index_file = os.path.join(args.output, "index.md")
                with open(index_file, 'w') as f:
                    f.write(index_content)
                print(f"Collection index saved to: {index_file}")
            else:
                print("\n" + "="*60)
                print("FRAMEWORK COLLECTION INDEX")
                print("="*60)
                print(index_content)
                
    except Exception as e:
        print(f"Error during curation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
