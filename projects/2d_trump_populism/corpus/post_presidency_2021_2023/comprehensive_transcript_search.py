#!/usr/bin/env python3
"""
Comprehensive Transcript URL Search

This script performs a systematic search for working transcript URLs by:
1. Testing known working patterns
2. Searching through source websites systematically
3. Testing common URL variations
"""

import requests
import time
import json
from pathlib import Path
import logging
from urllib.parse import urljoin, urlparse
import re

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def test_url(url):
    """Test if a URL is accessible and contains transcript content."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            # Check if page contains transcript-like content
            content = response.text.lower()
            transcript_indicators = ['transcript', 'speech', 'donald trump', 'rally', 'cpac', 'remarks']
            indicator_count = sum(1 for indicator in transcript_indicators if indicator in content)
            
            if indicator_count >= 2:
                return True, response.status_code, len(content)
            else:
                return False, response.status_code, "No transcript indicators found"
        else:
            return False, response.status_code, "HTTP error"
            
    except Exception as e:
        return False, "ERROR", str(e)

def search_rev_com_systematically():
    """Search Rev.com systematically for Trump speech transcripts."""
    working_urls = []
    base_url = "https://www.rev.com/blog/transcripts"
    
    # Test known working patterns
    test_patterns = [
        "donald-trump-cpac-2021-speech-transcript",
        "donald-trump-cpac-2022-speech-transcript", 
        "donald-trump-cpac-2023-speech-transcript",
        "donald-trump-ohio-rally-speech-transcript",
        "donald-trump-florida-rally-speech-transcript",
        "donald-trump-arizona-rally-speech-transcript",
        "donald-trump-georgia-rally-speech-transcript",
        "donald-trump-iowa-rally-speech-transcript",
        "donald-trump-north-carolina-rally-speech-transcript",
        "donald-trump-texas-rally-speech-transcript",
        "donald-trump-pennsylvania-rally-speech-transcript",
        "donald-trump-michigan-rally-speech-transcript",
        "donald-trump-wisconsin-rally-speech-transcript",
        "donald-trump-south-carolina-rally-speech-transcript",
        "donald-trump-new-hampshire-rally-speech-transcript"
    ]
    
    for pattern in test_patterns:
        url = f"{base_url}/{pattern}"
        logging.info(f"Testing Rev.com pattern: {url}")
        
        is_working, status, details = test_url(url)
        
        if is_working:
            working_urls.append({
                'url': url,
                'status': status,
                'content_size': details,
                'source': 'rev.com',
                'pattern': pattern
            })
            logging.info(f"✓ Working: {url}")
        else:
            logging.info(f"✗ Failed: {url} - {status}: {details}")
        
        time.sleep(1)  # Be respectful
    
    return working_urls

def search_factcheck_systematically():
    """Search FactCheck.org systematically for Trump speech transcripts."""
    working_urls = []
    
    # Test different date patterns and URL structures
    test_patterns = [
        "https://www.factcheck.org/2021/02/donald-trump-cpac-speech-transcript/",
        "https://www.factcheck.org/2021/06/donald-trump-ohio-rally-transcript/",
        "https://www.factcheck.org/2021/07/donald-trump-florida-rally-transcript/",
        "https://www.factcheck.org/2021/08/donald-trump-alabama-rally-transcript/",
        "https://www.factcheck.org/2021/09/donald-trump-georgia-rally-transcript/",
        "https://www.factcheck.org/2021/10/donald-trump-iowa-rally-transcript/",
        "https://www.factcheck.org/2021/11/donald-trump-florida-rally-transcript/",
        "https://www.factcheck.org/2022/01/donald-trump-texas-rally-transcript/",
        "https://www.factcheck.org/2022/02/donald-trump-cpac-speech-transcript/",
        "https://www.factcheck.org/2022/03/donald-trump-south-carolina-rally-transcript/",
        "https://www.factcheck.org/2022/04/donald-trump-michigan-rally-transcript/",
        "https://www.factcheck.org/2022/05/donald-trump-texas-rally-transcript/",
        "https://www.factcheck.org/2022/06/donald-trump-tennessee-rally-transcript/",
        "https://www.factcheck.org/2022/07/donald-trump-alaska-rally-transcript/",
        "https://www.factcheck.org/2022/08/donald-trump-wisconsin-rally-transcript/",
        "https://www.factcheck.org/2022/09/donald-trump-ohio-rally-transcript/",
        "https://www.factcheck.org/2022/10/donald-trump-michigan-rally-transcript/",
        "https://www.factcheck.org/2022/11/donald-trump-pennsylvania-rally-transcript/",
        "https://www.factcheck.org/2023/01/donald-trump-new-hampshire-rally-transcript/",
        "https://www.factcheck.org/2023/02/donald-trump-south-carolina-rally-transcript/",
        "https://www.factcheck.org/2023/03/donald-trump-cpac-speech-transcript/",
        "https://www.factcheck.org/2023/04/donald-trump-indiana-rally-transcript/",
        "https://www.factcheck.org/2023/05/donald-trump-texas-rally-transcript/",
        "https://www.factcheck.org/2023/06/donald-trump-north-carolina-rally-transcript/",
        "https://www.factcheck.org/2023/07/donald-trump-south-carolina-rally-transcript/",
        "https://www.factcheck.org/2023/08/donald-trump-alabama-rally-transcript/",
        "https://www.factcheck.org/2023/09/donald-trump-iowa-rally-transcript/",
        "https://www.factcheck.org/2023/10/donald-trump-south-carolina-rally-transcript/",
        "https://www.factcheck.org/2023/11/donald-trump-iowa-rally-transcript/",
        "https://www.factcheck.org/2023/12/donald-trump-iowa-rally-transcript/"
    ]
    
    for url in test_patterns:
        logging.info(f"Testing FactCheck.org: {url}")
        
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

def search_news_sources():
    """Search major news sources for Trump speech transcripts."""
    working_urls = []
    
    # Test major news sources
    news_sources = [
        "https://www.washingtonpost.com/politics/2021/02/28/donald-trump-cpac-speech-transcript/",
        "https://www.nytimes.com/2021/02/28/us/politics/donald-trump-cpac-speech-transcript.html",
        "https://www.foxnews.com/politics/donald-trump-cpac-2021-speech-transcript",
        "https://www.cnn.com/2021/02/28/politics/donald-trump-cpac-speech-transcript/index.html"
    ]
    
    for url in news_sources:
        logging.info(f"Testing news source: {url}")
        
        is_working, status, details = test_url(url)
        
        if is_working:
            working_urls.append({
                'url': url,
                'status': status,
                'content_size': details,
                'source': 'news'
            })
            logging.info(f"✓ Working: {url}")
        else:
            logging.info(f"✗ Failed: {url} - {status}: {details}")
        
        time.sleep(1)
    
    return working_urls

def main():
    """Main comprehensive search function."""
    logging.info("Starting comprehensive transcript URL search")
    
    all_working_urls = []
    
    # Search Rev.com systematically
    logging.info("Searching Rev.com systematically...")
    rev_urls = search_rev_com_systematically()
    all_working_urls.extend(rev_urls)
    
    # Search FactCheck.org systematically
    logging.info("Searching FactCheck.org systematically...")
    factcheck_urls = search_factcheck_systematically()
    all_working_urls.extend(factcheck_urls)
    
    # Search news sources
    logging.info("Searching news sources...")
    news_urls = search_news_sources()
    all_working_urls.extend(news_urls)
    
    # Save results
    results_file = "comprehensive_transcript_search_results.json"
    with open(results_file, 'w') as f:
        json.dump(all_working_urls, f, indent=2)
    
    # Create a working manifest file
    manifest_file = "working_transcript_urls.txt"
    with open(manifest_file, 'w') as f:
        f.write("# Working Transcript URLs Found\n")
        f.write("# Format: Date | Location | Event Type | URL\n\n")
        
        for url_info in all_working_urls:
            # Try to extract date and location from URL
            url = url_info['url']
            source = url_info['source']
            
            # Parse URL to extract information
            if 'cpac' in url.lower():
                if '2021' in url:
                    date = "2021-02-28"
                    location = "CPAC"
                    event = "Conservative Political Action Conference"
                elif '2022' in url:
                    date = "2022-02-26"
                    location = "CPAC"
                    event = "Conservative Political Action Conference"
                elif '2023' in url:
                    date = "2023-03-04"
                    location = "CPAC"
                    event = "Conservative Political Action Conference"
                else:
                    date = "Unknown"
                    location = "CPAC"
                    event = "Conservative Political Action Conference"
            else:
                date = "Unknown"
                location = "Unknown"
                event = "Speech/Rally"
            
            f.write(f"{date} | {location} | {event} | {url}\n")
    
    logging.info(f"Comprehensive search complete. Found {len(all_working_urls)} working URLs")
    logging.info(f"Results saved to: {results_file}")
    logging.info(f"Working manifest saved to: {manifest_file}")
    
    # Print summary
    print(f"\nComprehensive Search Results:")
    print(f"Total working URLs found: {len(all_working_urls)}")
    for url_info in all_working_urls:
        print(f"✓ {url_info['source']}: {url_info['url']}")

if __name__ == "__main__":
    main()
