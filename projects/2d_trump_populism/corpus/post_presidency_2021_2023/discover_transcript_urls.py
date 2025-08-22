#!/usr/bin/env python3
"""
Transcript URL Discovery Script

This script searches for actual working transcript URLs by testing common patterns
and known sources for Donald Trump's post-presidency speeches.
"""

import requests
import time
import json
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Known working sources to test
KNOWN_SOURCES = [
    "https://www.rev.com/blog/transcripts",
    "https://www.factcheck.org",
    "https://www.politifact.com",
    "https://www.washingtonpost.com",
    "https://www.nytimes.com",
    "https://www.foxnews.com",
    "https://www.cnn.com"
]

# Common URL patterns to test
URL_PATTERNS = [
    "https://www.rev.com/blog/transcripts/donald-trump-{event}-speech-transcript",
    "https://www.rev.com/blog/transcripts/donald-trump-{event}-transcript",
    "https://www.factcheck.org/2021/02/donald-trump-cpac-speech-transcript/",
    "https://www.factcheck.org/2022/02/donald-trump-cpac-speech-transcript/"
]

# Specific events to search for
EVENTS = [
    "cpac-2021",
    "cpac-2022", 
    "cpac-2023",
    "ohio-rally-2021",
    "florida-rally-2021",
    "arizona-rally-2021",
    "georgia-rally-2021",
    "iowa-rally-2021",
    "north-carolina-rally-2021"
]

def test_url(url):
    """Test if a URL is accessible and contains transcript content."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            # Check if page contains transcript-like content
            content = response.text.lower()
            transcript_indicators = ['transcript', 'speech', 'donald trump', 'rally', 'cpac']
            indicator_count = sum(1 for indicator in transcript_indicators if indicator in content)
            
            if indicator_count >= 2:
                return True, response.status_code, len(content)
            else:
                return False, response.status_code, "No transcript indicators found"
        else:
            return False, response.status_code, "HTTP error"
            
    except Exception as e:
        return False, "ERROR", str(e)

def search_rev_com():
    """Search Rev.com for actual Trump speech transcripts."""
    working_urls = []
    
    # Test the CPAC 2021 URL we know works
    test_urls = [
        "https://www.rev.com/blog/transcripts/donald-trump-cpac-2021-speech-transcript",
        "https://www.rev.com/blog/transcripts/donald-trump-cpac-2022-speech-transcript",
        "https://www.rev.com/blog/transcripts/donald-trump-cpac-2023-speech-transcript"
    ]
    
    for url in test_urls:
        logging.info(f"Testing: {url}")
        is_working, status, details = test_url(url)
        
        if is_working:
            working_urls.append({
                'url': url,
                'status': status,
                'content_size': details,
                'source': 'rev.com'
            })
            logging.info(f"✓ Working: {url}")
        else:
            logging.info(f"✗ Failed: {url} - {status}: {details}")
        
        time.sleep(1)  # Be respectful
    
    return working_urls

def search_factcheck_org():
    """Search FactCheck.org for Trump speech transcripts."""
    working_urls = []
    
    # Test known FactCheck URLs
    test_urls = [
        "https://www.factcheck.org/2021/02/donald-trump-cpac-speech-transcript/",
        "https://www.factcheck.org/2022/02/donald-trump-cpac-speech-transcript/",
        "https://www.factcheck.org/2023/03/donald-trump-cpac-speech-transcript/"
    ]
    
    for url in test_urls:
        logging.info(f"Testing: {url}")
        is_working, status, details = test_url(url)
        
        if is_working:
            working_urls.append({
                'url': url,
                'status': status,
                'content_size': details,
                'source': 'factcheck.org'
            })
            logging.info(f"✓ Working: {url}")
        else:
            logging.info(f"✗ Failed: {url} - {status}: {details}")
        
        time.sleep(1)
    
    return working_urls

def main():
    """Main discovery function."""
    logging.info("Starting transcript URL discovery")
    
    all_working_urls = []
    
    # Search Rev.com
    logging.info("Searching Rev.com...")
    rev_urls = search_rev_com()
    all_working_urls.extend(rev_urls)
    
    # Search FactCheck.org
    logging.info("Searching FactCheck.org...")
    factcheck_urls = search_factcheck_org()
    all_working_urls.extend(factcheck_urls)
    
    # Save results
    results_file = "discovered_transcript_urls.json"
    with open(results_file, 'w') as f:
        json.dump(all_working_urls, f, indent=2)
    
    logging.info(f"Discovery complete. Found {len(all_working_urls)} working URLs")
    logging.info(f"Results saved to: {results_file}")
    
    # Print summary
    print(f"\nDiscovery Results:")
    print(f"Total working URLs found: {len(all_working_urls)}")
    for url_info in all_working_urls:
        print(f"✓ {url_info['source']}: {url_info['url']}")

if __name__ == "__main__":
    main()
