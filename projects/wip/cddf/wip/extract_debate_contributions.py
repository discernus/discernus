#!/usr/bin/env python3
"""
Extract individual speaker contributions from debate transcripts for CDDF v10.2 analysis.
"""

import re
import os
from pathlib import Path

def extract_speaker_contributions(input_file, speaker_name, output_file):
    """Extract all contributions by a specific speaker from a debate transcript."""
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split into lines for processing
    lines = content.split('\n')
    
    # Find all lines that start with the speaker name
    speaker_lines = []
    current_contribution = []
    
    for line in lines:
        # Check if this line starts with the speaker name
        if line.strip().startswith(speaker_name):
            # If we have a current contribution, save it
            if current_contribution:
                speaker_lines.append('\n'.join(current_contribution))
                current_contribution = []
            
            # Start new contribution
            current_contribution = [line]
        elif current_contribution and line.strip():
            # Continue current contribution if line is not empty
            current_contribution.append(line)
        elif current_contribution and not line.strip():
            # Empty line - continue current contribution
            current_contribution.append(line)
        elif not current_contribution and line.strip():
            # No current contribution and non-empty line - skip
            continue
    
    # Don't forget the last contribution
    if current_contribution:
        speaker_lines.append('\n'.join(current_contribution))
    
    # Write to output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"# {speaker_name} Contributions from Debate\n\n")
        for i, contribution in enumerate(speaker_lines, 1):
            f.write(f"## Contribution {i}\n\n")
            f.write(contribution)
            f.write("\n\n---\n\n")
    
    print(f"Extracted {len(speaker_lines)} contributions from {speaker_name} to {output_file}")

def main():
    """Extract contributions from all debate files."""
    
    # 2024 Harris vs Trump Debate
    print("Processing 2024 Harris vs Trump Debate...")
    extract_speaker_contributions(
        "Full Debate： Harris vs. Trump in 2024 ABC News Presidential Debate ｜ WSJ.txt",
        "Kamala Harris",
        "harris_2024_debate_responses.txt"
    )
    
    extract_speaker_contributions(
        "Full Debate： Harris vs. Trump in 2024 ABC News Presidential Debate ｜ WSJ.txt",
        "Donald J. Trump",
        "trump_2024_debate_responses.txt"
    )
    
    # 2016 GOP Primary Debate
    print("Processing 2016 GOP Primary Debate...")
    extract_speaker_contributions(
        "FULL SHOW - Presidential GOP Republican Prime Time Debate Part 1 - Presidential Election 2016.txt",
        "Donald J. Trump",
        "trump_2016_primary_debate_responses.txt"
    )
    
    # Democratic Debate
    print("Processing Democratic Debate...")
    extract_speaker_contributions(
        "NBC News-YouTube Democratic Debate (Full).txt",
        "Hillary Clinton",
        "clinton_2016_primary_debate_responses.txt"
    )
    
    print("All extractions complete!")

if __name__ == "__main__":
    main()
