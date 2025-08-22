#!/usr/bin/env python3
"""
Simple script to append full librarian reports as appendices to the synthesis report.
"""

import json
from pathlib import Path
import sys

def append_librarian_reports(synthesis_file: str, research_data_file: str, output_file: str = None):
    """
    Append full librarian reports as appendices to the synthesis report.
    
    Args:
        synthesis_file: Path to the synthesis report
        research_data_file: Path to the librarian research data JSON
        output_file: Output file path (defaults to synthesis_file with _with_appendices suffix)
    """
    
    if output_file is None:
        synthesis_path = Path(synthesis_file)
        output_file = synthesis_path.parent / f"{synthesis_path.stem}_with_appendices{synthesis_path.suffix}"
    
    # Read the synthesis report
    with open(synthesis_file, 'r', encoding='utf-8') as f:
        synthesis_content = f.read()
    
    # Read the research data
    with open(research_data_file, 'r', encoding='utf-8') as f:
        research_data = json.load(f)
    
    # Create appendices section
    appendices = []
    appendices.append("\n\n---\n\n# 📚 Detailed Research Reports\n\n")
    
    # Add each research question's detailed report
    # Extract timestamp from the research data file name to find the corresponding report
    import re
    from pathlib import Path as PathLib
    
    research_data_path = PathLib(research_data_file)
    timestamp_match = re.search(r'(\d{8}_\d{6})', research_data_path.name)
    
    if timestamp_match:
        timestamp = timestamp_match.group(1)
        # Look for the corresponding report file
        report_file_pattern = f"discernus_librarian_report_{timestamp}.md"
        
        # Check in the local discernus/librarian/reports directory first
        local_report_path = PathLib("discernus/librarian/reports") / report_file_pattern
        global_report_path = PathLib("/Volumes/code/discernus/discernus/librarian/reports") / report_file_pattern
        
        report_file = None
        if local_report_path.exists():
            report_file = local_report_path
        elif global_report_path.exists():
            report_file = global_report_path
        
        if report_file:
            try:
                # Read the detailed report content from the markdown file
                with open(report_file, 'r', encoding='utf-8') as f:
                    detailed_report = f.read()
                
                appendices.append(f"## Appendix 1: Research Report\n\n")
                appendices.append(f"**Source**: {report_file}\n\n")
                appendices.append("**Complete Research Report**:\n\n")
                appendices.append(f"{detailed_report}\n\n")
                appendices.append("---\n\n")
            except Exception as e:
                appendices.append(f"## Appendix 1: Research Report\n\n")
                appendices.append(f"**Error**: Could not load detailed report from {report_file}: {e}\n\n")
                appendices.append("---\n\n")
        else:
            appendices.append(f"## Appendix 1: Research Report\n\n")
            appendices.append(f"**Error**: Could not find report file {report_file_pattern} in expected locations\n\n")
            appendices.append(f"**Searched**: {local_report_path}, {global_report_path}\n\n")
            appendices.append("---\n\n")
    else:
        appendices.append(f"## Appendix 1: Research Report\n\n")
        appendices.append(f"**Error**: Could not extract timestamp from {research_data_file}\n\n")
        appendices.append("---\n\n")
    
    # Combine content
    full_report = synthesis_content + ''.join(appendices)
    
    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(full_report)
    
    print(f"✅ Full report with appendices saved to: {output_file}")
    return output_file

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 append_librarian_reports.py <synthesis_file> <research_data_file> [output_file]")
        sys.exit(1)
    
    synthesis_file = sys.argv[1]
    research_data_file = sys.argv[2]
    output_file = sys.argv[3] if len(sys.argv) > 3 else None
    
    try:
        result = append_librarian_reports(synthesis_file, research_data_file, output_file)
        print(f"🎯 Successfully created: {result}")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
