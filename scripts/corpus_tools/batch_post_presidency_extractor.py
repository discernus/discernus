#!/usr/bin/env python3
"""
Batch transcript extractor for Donald Trump's post-presidency videos (2021-2023)
Processes multiple video URLs and extracts transcripts with metadata
"""

import argparse
import json
import logging
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BatchPostPresidencyExtractor:
    """Batch extractor for post-presidency video transcripts"""
    
    def __init__(self, output_dir: str, whisper_model: str = "base"):
        self.output_dir = Path(output_dir)
        self.whisper_model = whisper_model
        self.extractor_script = "scripts/corpus_tools/enhanced_transcript_extractor.py"
        self.results = []
        self.failed_urls = []
        
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories for organization
        (self.output_dir / "transcripts").mkdir(exist_ok=True)
        (self.output_dir / "metadata").mkdir(exist_ok=True)
        (self.output_dir / "logs").mkdir(exist_ok=True)
    
    def load_video_urls(self, urls_file: str) -> List[str]:
        """Load video URLs from a file"""
        urls = []
        
        if urls_file.endswith('.json'):
            # Load from JSON file
            with open(urls_file, 'r') as f:
                data = json.load(f)
                if 'videos' in data:
                    # Extract URLs from search results
                    for video in data['videos']:
                        if 'url' in video:
                            urls.append(video['url'])
                elif 'search_urls' in data:
                    # Extract URLs from search URLs file
                    for item in data['search_urls']:
                        # This would be populated after manual searching
                        pass
        elif urls_file.endswith('.txt'):
            # Load from text file (one URL per line)
            with open(urls_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and line.startswith('http'):
                        urls.append(line)
        
        return urls
    
    def extract_single_video(self, url: str, event_info: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Extract transcript from a single video URL"""
        logger.info(f"Extracting transcript from: {url}")
        
        # Generate filename based on event info or URL
        if event_info:
            filename = f"{event_info['date']}_{event_info['event'].replace(' ', '_')}_{event_info['location'].replace(' ', '_')}"
        else:
            # Fallback to video ID
            import re
            video_id_match = re.search(r'v=([a-zA-Z0-9_-]{11})', url)
            if video_id_match:
                filename = f"video_{video_id_match.group(1)}"
            else:
                filename = f"video_{int(time.time())}"
        
        # Clean filename
        filename = "".join(c for c in filename if c.isalnum() or c in ('_', '-')).rstrip('_')
        
        # Run the enhanced transcript extractor
        command = [
            "python3",
            self.extractor_script,
            url,
            "--output-dir",
            str(self.output_dir / "transcripts"),
            "--whisper-model",
            self.whisper_model
        ]
        
        try:
            logger.info(f"Running command: {' '.join(command)}")
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            
            # Check if transcript was created
            transcript_files = list((self.output_dir / "transcripts").glob(f"{filename}*"))
            
            if transcript_files:
                transcript_file = transcript_files[0]
                logger.info(f"Successfully extracted transcript: {transcript_file.name}")
                
                return {
                    'url': url,
                    'success': True,
                    'transcript_file': str(transcript_file),
                    'filename': transcript_file.name,
                    'event_info': event_info,
                    'stdout': result.stdout,
                    'stderr': result.stderr
                }
            else:
                logger.warning(f"No transcript file created for: {url}")
                return {
                    'url': url,
                    'success': False,
                    'error': 'No transcript file created',
                    'event_info': event_info,
                    'stdout': result.stdout,
                    'stderr': result.stderr
                }
                
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to extract transcript from {url}: {e}")
            return {
                'url': url,
                'success': False,
                'error': str(e),
                'event_info': event_info,
                'stdout': e.stdout,
                'stderr': e.stderr
            }
    
    def extract_batch(self, urls: List[str], event_mapping: Optional[Dict[str, Dict[str, str]]] = None, 
                     delay: float = 2.0) -> List[Dict[str, Any]]:
        """Extract transcripts from a batch of video URLs"""
        logger.info(f"Starting batch extraction of {len(urls)} videos...")
        
        results = []
        
        for i, url in enumerate(urls, 1):
            logger.info(f"Processing video {i}/{len(urls)}: {url}")
            
            # Get event info if available
            event_info = None
            if event_mapping and url in event_mapping:
                event_info = event_mapping[url]
            
            # Extract transcript
            result = self.extract_single_video(url, event_info)
            results.append(result)
            
            # Track success/failure
            if result['success']:
                self.results.append(result)
            else:
                self.failed_urls.append(url)
            
            # Add delay between extractions
            if i < len(urls):
                logger.info(f"Waiting {delay} seconds before next extraction...")
                time.sleep(delay)
        
        return results
    
    def save_batch_results(self) -> str:
        """Save batch extraction results"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save results summary
        results_file = self.output_dir / "logs" / f"batch_extraction_results_{timestamp}.json"
        with open(results_file, 'w') as f:
            json.dump({
                'metadata': {
                    'extraction_date': datetime.now().isoformat(),
                    'total_urls': len(self.results) + len(self.failed_urls),
                    'successful_extractions': len(self.results),
                    'failed_extractions': len(self.failed_urls),
                    'whisper_model': self.whisper_model
                },
                'successful_extractions': self.results,
                'failed_urls': self.failed_urls
            }, f, indent=2)
        
        # Save summary report
        summary_file = self.output_dir / "logs" / f"batch_extraction_summary_{timestamp}.txt"
        with open(summary_file, 'w') as f:
            f.write("BATCH TRANSCRIPT EXTRACTION SUMMARY\n")
            f.write("=" * 40 + "\n\n")
            f.write(f"Extraction Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total URLs Processed: {len(self.results) + len(self.failed_urls)}\n")
            f.write(f"Successful Extractions: {len(self.results)}\n")
            f.write(f"Failed Extractions: {len(self.failed_urls)}\n")
            f.write(f"Whisper Model: {self.whisper_model}\n\n")
            
            if self.results:
                f.write("SUCCESSFUL EXTRACTIONS:\n")
                f.write("-" * 25 + "\n")
                for result in self.results:
                    f.write(f"• {result['filename']}\n")
                    f.write(f"  URL: {result['url']}\n")
                    if result.get('event_info'):
                        f.write(f"  Event: {result['event_info'].get('event', 'Unknown')}\n")
                    f.write(f"  File: {result['transcript_file']}\n\n")
            
            if self.failed_urls:
                f.write("FAILED EXTRACTIONS:\n")
                f.write("-" * 20 + "\n")
                for url in self.failed_urls:
                    f.write(f"• {url}\n")
        
        return str(results_file)
    
    def print_summary(self):
        """Print extraction summary"""
        total = len(self.results) + len(self.failed_urls)
        success_rate = (len(self.results) / total * 100) if total > 0 else 0
        
        print(f"\n📊 BATCH EXTRACTION SUMMARY")
        print(f"=" * 35)
        print(f"Total URLs processed: {total}")
        print(f"Successful extractions: {len(self.results)}")
        print(f"Failed extractions: {len(self.failed_urls)}")
        print(f"Success rate: {success_rate:.1f}%")
        
        if self.results:
            print(f"\n✅ SUCCESSFUL EXTRACTIONS:")
            for result in self.results[:5]:  # Show first 5
                print(f"• {result['filename']}")
                if result.get('event_info'):
                    print(f"  Event: {result['event_info'].get('event', 'Unknown')}")
        
        if self.failed_urls:
            print(f"\n❌ FAILED EXTRACTIONS:")
            for url in self.failed_urls[:5]:  # Show first 5
                print(f"• {url}")
        
        print(f"\n📁 Results saved to: {self.output_dir}")
        print(f"📄 Logs: {self.output_dir}/logs/")

def main():
    """Main function for batch extraction"""
    parser = argparse.ArgumentParser(description="Batch extract transcripts from post-presidency videos")
    parser.add_argument("--output-dir", default="projects/2d_trump_populism/corpus/post_presidency_2021_2023",
                       help="Output directory for transcripts")
    parser.add_argument("--url-file", help="Specific URL file to use")
    parser.add_argument("--auto-confirm", action="store_true", help="Automatically confirm extraction")
    parser.add_argument("--whisper-model", default="base", help="Whisper model to use")
    
    args = parser.parse_args()
    
    output_dir = args.output_dir
    
    # Initialize extractor
    extractor = BatchPostPresidencyExtractor(output_dir, whisper_model=args.whisper_model)
    
    print("🔍 BATCH POST-PRESIDENCY TRANSCRIPT EXTRACTOR")
    print("=" * 50)
    print("This script processes video URLs to extract transcripts.")
    print("You can provide URLs in several ways:")
    print("1. Create a text file with one URL per line")
    print("2. Create a JSON file with video data")
    print("3. Manually input URLs")
    
    # Check for existing URL files
    url_files = list(Path(output_dir).glob("*urls*.txt")) + list(Path(output_dir).glob("*urls*.json"))
    
    if args.url_file:
        # Use specified URL file
        selected_file = Path(args.url_file)
        if not selected_file.exists():
            print(f"❌ Specified URL file not found: {args.url_file}")
            return
        url_files = [selected_file]
        choice = "1"
    elif url_files:
        print(f"\n📁 Found existing URL files:")
        for i, file in enumerate(url_files, 1):
            print(f"{i}. {file.name}")
        
        if args.auto_confirm:
            choice = "1"  # Use first file automatically
            print("Auto-confirm enabled, using first file")
        else:
            choice = input(f"\nSelect file number (1-{len(url_files)}) or press Enter to input URLs manually: ").strip()
    else:
        print(f"\n❌ No URL files found in {output_dir}")
        print("Please create a file with video URLs first, or use the search guide to find videos.")
        return
    
    if choice.isdigit() and 1 <= int(choice) <= len(url_files):
        selected_file = url_files[int(choice) - 1]
        print(f"Using file: {selected_file.name}")
        
        # Load URLs from file
        urls = extractor.load_video_urls(str(selected_file))
        
        if urls:
            print(f"Loaded {len(urls)} URLs from {selected_file.name}")
            
            # Confirm before proceeding
            if args.auto_confirm:
                proceed = "y"
                print("Auto-confirm enabled, proceeding with extraction")
            else:
                proceed = input(f"Proceed with extraction of {len(urls)} videos? (y/N): ").strip().lower()
            
            if proceed == 'y':
                # Run batch extraction
                results = extractor.extract_batch(urls, delay=2.0)
                
                # Save results
                results_file = extractor.save_batch_results()
                
                # Print summary
                extractor.print_summary()
                
                print(f"\n✅ Batch extraction complete! Results saved to: {results_file}")
            else:
                print("Extraction cancelled.")
        else:
            print(f"No URLs found in {selected_file.name}")
    else:
        print("Manual URL input not implemented yet. Please create a URL file first.")

if __name__ == "__main__":
    main()
