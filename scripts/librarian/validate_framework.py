#!/usr/bin/env python3
"""
Framework Validation Tool

Comprehensive framework validation tool using the DiscernusLibrarian methodology.

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
        description="Validate analytical frameworks using DiscernusLibrarian methodology"
    )
    parser.add_argument(
        "framework_path", 
        help="Path to the framework file to validate"
    )
    parser.add_argument(
        "--detailed", 
        action="store_true", 
        help="Generate detailed validation report"
    )
    parser.add_argument(
        "--output", 
        help="Output file for validation report"
    )
    parser.add_argument(
        "--summary", 
        action="store_true", 
        help="Generate summary report for batch validation"
    )
    parser.add_argument(
        "--level", 
        type=int, 
        choices=[1, 2, 3, 4], 
        default=2,
        help="Validation level (1=basic, 2=academic, 3=measurement, 4=production)"
    )
    
    args = parser.parse_args()
    
    # Initialize librarian
    librarian = DiscernusLibrarian()
    
    # Handle multiple files for batch processing
    framework_paths = []
    if "*" in args.framework_path:
        # Handle glob patterns
        from glob import glob
        framework_paths = glob(args.framework_path)
    else:
        framework_paths = [args.framework_path]
    
    results = []
    for framework_path in framework_paths:
        if not os.path.exists(framework_path):
            print(f"Error: Framework file not found: {framework_path}")
            continue
            
        print(f"Validating framework: {framework_path}")
        
        # Perform validation using librarian
        try:
            # This would use the existing librarian validation functionality
            result = librarian.validate_framework(
                framework_path, 
                level=args.level,
                detailed=args.detailed
            )
            results.append(result)
            
            if args.detailed and args.output:
                # Save detailed report
                with open(args.output, 'w') as f:
                    f.write(result.get('detailed_report', ''))
                print(f"Detailed report saved to: {args.output}")
            else:
                # Print summary
                print(f"Validation result: {'PASSED' if result.get('valid', False) else 'FAILED'}")
                if result.get('errors'):
                    print("Errors:")
                    for error in result['errors']:
                        print(f"  - {error}")
                if result.get('warnings'):
                    print("Warnings:")
                    for warning in result['warnings']:
                        print(f"  - {warning}")
                        
        except Exception as e:
            print(f"Error validating {framework_path}: {e}")
            results.append({'valid': False, 'error': str(e)})
    
    # Generate summary for batch processing
    if args.summary and len(results) > 1:
        passed = sum(1 for r in results if r.get('valid', False))
        total = len(results)
        print(f"\nBatch validation summary: {passed}/{total} frameworks passed")
    
    # Exit with appropriate code
    if all(r.get('valid', False) for r in results):
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
