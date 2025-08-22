#!/usr/bin/env python3
"""
Batch Transcript Extractor for Post-Presidency Trump Speeches

This script reads a manifest file containing URLs to web transcripts and processes
each one using the existing html_transcript_extractor.py tool. It provides batch
processing with error handling and progress tracking.
"""

import os
import sys
import subprocess
import logging
from pathlib import Path
from datetime import datetime
import time

# Configuration
MANIFEST_FILE = "test_manifest.txt"  # Use test manifest first
EXTRACTOR_SCRIPT = "/Volumes/code/discernus/corpus/tools/html_transcript_extractor.py"
OUTPUT_DIR = "/Volumes/code/discernus/projects/2d_trump_populism/corpus/post_presidency_2021_2023"
LOG_FILE = "batch_extraction.log"

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)

def parse_manifest_line(line):
    """Parse a line from the manifest file to extract date, location, and URL."""
    line = line.strip()
    
    # Skip comments and empty lines
    if not line or line.startswith('#'):
        return None
    
    # Parse format: Date | Location | Event Type | URL
    try:
        parts = [part.strip() for part in line.split('|')]
        if len(parts) >= 4:
            date = parts[0]
            location = parts[1]
            event_type = parts[2]
            url = parts[3]
            return {
                'date': date,
                'location': location,
                'event_type': event_type,
                'url': url
            }
    except Exception as e:
        logging.warning(f"Failed to parse line: {line}. Error: {e}")
    
    return None

def extract_transcript(url, date, location, event_type):
    """Extract transcript using the html_transcript_extractor.py tool."""
    
    # Create a descriptive filename
    safe_location = location.replace(' ', '_').replace(',', '').replace(' ', '_')
    safe_event = event_type.replace(' ', '_').replace(',', '')
    filename = f"trump_{date}_{safe_location}_{safe_event}"
    
    logging.info(f"Processing: {filename}")
    logging.info(f"URL: {url}")
    
    try:
        # Call the html_transcript_extractor.py script
        cmd = [
            "python3",
            EXTRACTOR_SCRIPT,
            url,
            "--output-dir",
            OUTPUT_DIR
        ]
        
        logging.info(f"Running command: {' '.join(cmd)}")
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300,  # 5 minute timeout per URL
            cwd=OUTPUT_DIR
        )
        
        if result.returncode == 0:
            logging.info(f"SUCCESS: {filename}")
            if result.stdout:
                logging.info(f"Output: {result.stdout.strip()}")
            return True
        else:
            logging.error(f"FAILED: {filename}")
            if result.stderr:
                logging.error(f"Error: {result.stderr.strip()}")
            return False
            
    except subprocess.TimeoutExpired:
        logging.error(f"TIMEOUT: {filename} - exceeded 5 minute limit")
        return False
    except Exception as e:
        logging.error(f"EXCEPTION: {filename} - {str(e)}")
        return False

def main():
    """Main batch processing function."""
    
    # Ensure output directory exists
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    
    # Check if extractor script exists
    if not os.path.exists(EXTRACTOR_SCRIPT):
        logging.error(f"Extractor script not found: {EXTRACTOR_SCRIPT}")
        return
    
    # Check if manifest file exists
    manifest_path = os.path.join(OUTPUT_DIR, MANIFEST_FILE)
    if not os.path.exists(manifest_path):
        logging.error(f"Manifest file not found: {manifest_path}")
        return
    
    logging.info("Starting batch transcript extraction")
    logging.info(f"Manifest: {manifest_path}")
    logging.info(f"Output directory: {OUTPUT_DIR}")
    logging.info(f"Extractor script: {EXTRACTOR_SCRIPT}")
    
    # Read and process manifest
    successful = 0
    failed = 0
    skipped = 0
    
    with open(manifest_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            parsed = parse_manifest_line(line)
            
            if not parsed:
                skipped += 1
                continue
            
            logging.info(f"Line {line_num}: Processing {parsed['date']} - {parsed['location']}")
            
            success = extract_transcript(
                parsed['url'],
                parsed['date'],
                parsed['location'],
                parsed['event_type']
            )
            
            if success:
                successful += 1
            else:
                failed += 1
            
            # Add delay between requests to be respectful
            time.sleep(2)
    
    # Summary
    logging.info("=" * 50)
    logging.info("BATCH EXTRACTION COMPLETE")
    logging.info(f"Successful: {successful}")
    logging.info(f"Failed: {failed}")
    logging.info(f"Skipped: {skipped}")
    logging.info(f"Total processed: {successful + failed}")
    logging.info("=" * 50)

if __name__ == "__main__":
    main()
