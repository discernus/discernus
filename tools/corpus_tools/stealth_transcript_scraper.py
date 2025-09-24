#!/usr/bin/env python3
"""
Stealth Transcript Scraper for APDES Corpus Collection

Uses browser automation to bypass access restrictions and collect official transcripts 
from government websites, news sources, and academic repositories.

Combines multiple bypass techniques:
1. Undetected ChromeDriver (Selenium-based)
2. Playwright with stealth plugins
3. Intelligent request headers and delays
4. User agent rotation and proxy support

Usage:
    python3 scripts/stealth_transcript_scraper.py <url> [options]
"""

import argparse
import json
import os
import time
import random
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
import re
from urllib.parse import urlparse

# Browser automation imports
try:
    import undetected_chromedriver as uc
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


@dataclass
class TranscriptScrapingResult:
    """Result container for transcript scraping"""
    success: bool
    url: str
    title: Optional[str]
    content: Optional[str]
    method_used: Optional[str] = None
    word_count: Optional[int] = None
    confidence_score: Optional[float] = None
    error_message: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class StealthTranscriptScraper:
    """Advanced transcript scraper that bypasses access restrictions"""
    
    def __init__(self):
        self.user_agents = [
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36", 
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0"
        ]
        
        # Common selectors for transcript content
        self.transcript_selectors = [
            # Government/Official sites
            '.transcript-content', '.speech-content', '.remarks-content',
            '.full-text', '.speech-text', '.transcript-text',
            # News sites
            '.article-content', '.story-content', '.entry-content',
            '.post-content', '.body-copy', '.article-body',
            # Generic content selectors
            '[class*="transcript"]', '[class*="speech"]', '[class*="content"]',
            'main article', '.main-content', '#main-content',
            # Fallback selectors
            'article', 'main', '.content', '#content'
        ]
        
        # Patterns to identify transcript content
        self.transcript_patterns = [
            r'remarks?\s+by\s+president',
            r'speech\s+by\s+president',  
            r'transcript\s+of',
            r'full\s+text\s+of',
            r'prepared\s+remarks',
            r'as\s+delivered',
            r'thank\s+you\s+(very\s+much|all)',
            r'(ladies\s+and\s+)?gentlemen',
            r'my\s+fellow\s+americans'
        ]
        
    def scrape_transcript(self, url: str, method: str = "auto") -> TranscriptScrapingResult:
        """
        Scrape transcript using specified method with intelligent fallback
        
        Methods:
        - "selenium": Use undetected ChromeDriver
        - "playwright": Use Playwright with stealth
        - "requests": Use enhanced requests with headers
        - "auto": Try all methods in order of effectiveness
        """
        
        print(f"🔍 Stealth Transcript Scraper")
        print(f"📋 URL: {url}")
        print(f"🎭 Method: {method}")
        print("-" * 60)
        
        if method == "auto":
            # Try methods in order of effectiveness for transcript content
            methods = []
            if SELENIUM_AVAILABLE:
                methods.append("selenium")
            if PLAYWRIGHT_AVAILABLE:
                methods.append("playwright") 
            methods.append("requests")
            
            for attempt_method in methods:
                print(f"🔄 Attempting {attempt_method} method...")
                result = self._scrape_with_method(url, attempt_method)
                
                if result.success:
                    print(f"✅ Success with {attempt_method}!")
                    return result
                else:
                    print(f"❌ {attempt_method} failed: {result.error_message}")
            
            return TranscriptScrapingResult(
                success=False,
                url=url,
                title=None,
                content=None,
                error_message="All extraction methods failed"
            )
        
        else:
            return self._scrape_with_method(url, method)
    
    def _scrape_with_method(self, url: str, method: str) -> TranscriptScrapingResult:
        """Scrape using a specific method"""
        
        if method == "selenium" and SELENIUM_AVAILABLE:
            return self._scrape_with_selenium(url)
        elif method == "playwright" and PLAYWRIGHT_AVAILABLE:
            return self._scrape_with_playwright(url)
        elif method == "requests":
            return self._scrape_with_requests(url)
        else:
            return TranscriptScrapingResult(
                success=False,
                url=url,
                title=None,
                content=None,
                error_message=f"Method {method} not available or unsupported"
            )
    
    def _scrape_with_selenium(self, url: str) -> TranscriptScrapingResult:
        """Scrape using undetected ChromeDriver"""
        
        if not SELENIUM_AVAILABLE:
            return TranscriptScrapingResult(
                success=False, url=url, title=None, content=None,
                error_message="Selenium not available"
            )
        
        driver = None
        try:
            # Configure undetected ChromeDriver
            options = uc.ChromeOptions()
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            # Random user agent
            user_agent = random.choice(self.user_agents)
            options.add_argument(f"--user-agent={user_agent}")
            
            # Initialize driver
            driver = uc.Chrome(options=options, version_main=None)
            
            # Additional stealth measures
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            print(f"🌐 Loading page with Selenium...")
            driver.get(url)
            
            # Wait for page load and add random delay
            time.sleep(random.uniform(2, 5))
            
            # Get page title
            title = driver.title
            
            # Extract content using multiple selectors
            content = self._extract_content_selenium(driver)
            
            if content:
                confidence = self._assess_transcript_confidence(content, title)
                word_count = len(content.split())
                
                return TranscriptScrapingResult(
                    success=True,
                    url=url,
                    title=title,
                    content=content,
                    method_used="selenium",
                    word_count=word_count,
                    confidence_score=confidence,
                    metadata={
                        "user_agent": user_agent,
                        "extraction_date": datetime.now().isoformat(),
                        "page_title": title
                    }
                )
            else:
                return TranscriptScrapingResult(
                    success=False, url=url, title=title, content=None,
                    method_used="selenium", error_message="No transcript content found"
                )
                
        except Exception as e:
            return TranscriptScrapingResult(
                success=False, url=url, title=None, content=None,
                method_used="selenium", error_message=f"Selenium error: {str(e)}"
            )
        finally:
            if driver:
                driver.quit()
    
    def _scrape_with_playwright(self, url: str) -> TranscriptScrapingResult:
        """Scrape using Playwright with stealth techniques"""
        
        if not PLAYWRIGHT_AVAILABLE:
            return TranscriptScrapingResult(
                success=False, url=url, title=None, content=None,
                error_message="Playwright not available"
            )
        
        try:
            with sync_playwright() as p:
                # Launch browser with stealth options
                browser = p.chromium.launch(
                    headless=True,
                    args=[
                        "--no-sandbox",
                        "--disable-dev-shm-usage", 
                        "--disable-blink-features=AutomationControlled"
                    ]
                )
                
                context = browser.new_context(
                    user_agent=random.choice(self.user_agents),
                    viewport={"width": 1920, "height": 1080}
                )
                
                page = context.new_page()
                
                # Add stealth script
                page.add_init_script("""
                    Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                    delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
                    delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
                    delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
                """)
                
                print(f"🌐 Loading page with Playwright...")
                response = page.goto(url, timeout=30000)
                
                if response.status >= 400:
                    return TranscriptScrapingResult(
                        success=False, url=url, title=None, content=None,
                        method_used="playwright", 
                        error_message=f"HTTP {response.status} error"
                    )
                
                # Wait for content to load
                page.wait_for_load_state("domcontentloaded")
                time.sleep(random.uniform(1, 3))
                
                title = page.title()
                content = self._extract_content_playwright(page)
                
                browser.close()
                
                if content:
                    confidence = self._assess_transcript_confidence(content, title)
                    word_count = len(content.split())
                    
                    return TranscriptScrapingResult(
                        success=True,
                        url=url,
                        title=title,
                        content=content,
                        method_used="playwright",
                        word_count=word_count,
                        confidence_score=confidence,
                        metadata={
                            "extraction_date": datetime.now().isoformat(),
                            "page_title": title,
                            "http_status": response.status
                        }
                    )
                else:
                    return TranscriptScrapingResult(
                        success=False, url=url, title=title, content=None,
                        method_used="playwright", error_message="No transcript content found"
                    )
                    
        except Exception as e:
            return TranscriptScrapingResult(
                success=False, url=url, title=None, content=None,
                method_used="playwright", error_message=f"Playwright error: {str(e)}"
            )
    
    def _scrape_with_requests(self, url: str) -> TranscriptScrapingResult:
        """Scrape using enhanced requests with stealth headers"""
        
        try:
            session = requests.Session()
            
            # Configure retry strategy
            retry_strategy = Retry(
                total=3,
                backoff_factor=1,
                status_forcelist=[429, 500, 502, 503, 504],
            )
            adapter = HTTPAdapter(max_retries=retry_strategy)
            session.mount("http://", adapter)
            session.mount("https://", adapter)
            
            # Stealth headers
            headers = {
                'User-Agent': random.choice(self.user_agents),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Cache-Control': 'max-age=0'
            }
            
            print(f"🌐 Loading page with enhanced requests...")
            response = session.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            # Parse content
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            
            title = soup.title.get_text(strip=True) if soup.title else "Unknown"
            content = self._extract_content_beautifulsoup(soup)
            
            if content:
                confidence = self._assess_transcript_confidence(content, title)
                word_count = len(content.split())
                
                return TranscriptScrapingResult(
                    success=True,
                    url=url,
                    title=title,
                    content=content,
                    method_used="requests",
                    word_count=word_count,
                    confidence_score=confidence,
                    metadata={
                        "extraction_date": datetime.now().isoformat(),
                        "page_title": title,
                        "http_status": response.status_code,
                        "content_type": response.headers.get('content-type', '')
                    }
                )
            else:
                return TranscriptScrapingResult(
                    success=False, url=url, title=title, content=None,
                    method_used="requests", error_message="No transcript content found"
                )
                
        except ImportError:
            return TranscriptScrapingResult(
                success=False, url=url, title=None, content=None,
                method_used="requests", error_message="BeautifulSoup not available (pip install beautifulsoup4)"
            )
        except Exception as e:
            return TranscriptScrapingResult(
                success=False, url=url, title=None, content=None,
                method_used="requests", error_message=f"Requests error: {str(e)}"
            )
    
    def _extract_content_selenium(self, driver) -> Optional[str]:
        """Extract transcript content using Selenium"""
        
        for selector in self.transcript_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    text = element.get_attribute('innerText') or element.text
                    if self._is_likely_transcript(text):
                        return self._clean_transcript_text(text)
            except:
                continue
                
        # Fallback: get body text and filter
        try:
            body_text = driver.find_element(By.TAG_NAME, 'body').text
            if self._is_likely_transcript(body_text):
                return self._clean_transcript_text(body_text)
        except:
            pass
            
        return None
    
    def _extract_content_playwright(self, page) -> Optional[str]:
        """Extract transcript content using Playwright"""
        
        for selector in self.transcript_selectors:
            try:
                elements = page.query_selector_all(selector)
                for element in elements:
                    text = element.inner_text()
                    if self._is_likely_transcript(text):
                        return self._clean_transcript_text(text)
            except:
                continue
                
        # Fallback: get body text
        try:
            body_text = page.inner_text('body')
            if self._is_likely_transcript(body_text):
                return self._clean_transcript_text(body_text)
        except:
            pass
            
        return None
    
    def _extract_content_beautifulsoup(self, soup) -> Optional[str]:
        """Extract transcript content using BeautifulSoup"""
        
        for selector in self.transcript_selectors:
            try:
                elements = soup.select(selector)
                for element in elements:
                    text = element.get_text(separator=' ', strip=True)
                    if self._is_likely_transcript(text):
                        return self._clean_transcript_text(text)
            except:
                continue
                
        # Fallback: get body text
        try:
            body = soup.find('body')
            if body:
                text = body.get_text(separator=' ', strip=True)
                if self._is_likely_transcript(text):
                    return self._clean_transcript_text(text)
        except:
            pass
            
        return None
    
    def _is_likely_transcript(self, text: str) -> bool:
        """Determine if text is likely a transcript"""
        
        if not text or len(text) < 500:  # Too short
            return False
            
        if len(text) > 200000:  # Too long (likely includes navigation/ads)
            return False
            
        # Check for transcript patterns
        text_lower = text.lower()
        pattern_matches = sum(1 for pattern in self.transcript_patterns 
                            if re.search(pattern, text_lower))
        
        if pattern_matches >= 2:  # Multiple transcript indicators
            return True
            
        # Check for speech-like characteristics
        speech_indicators = [
            'thank you', 'ladies and gentlemen', 'my fellow', 
            'president', 'remarks', 'speech', 'transcript'
        ]
        
        indicator_count = sum(1 for indicator in speech_indicators 
                            if indicator in text_lower)
        
        return indicator_count >= 3
    
    def _clean_transcript_text(self, text: str) -> str:
        """Clean and format transcript text"""
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\n\s*\n', '\n\n', text)
        
        # Remove common navigation/footer text
        cleanup_patterns = [
            r'skip to main content',
            r'accessibility statement',
            r'privacy policy',
            r'terms of use',
            r'cookie policy',
            r'share this page',
            r'print this page',
            r'email this page'
        ]
        
        for pattern in cleanup_patterns:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)
        
        return text.strip()
    
    def _assess_transcript_confidence(self, content: str, title: str) -> float:
        """Assess confidence that this is a quality transcript"""
        
        confidence = 50.0  # Base confidence
        
        # Length indicators
        word_count = len(content.split())
        if 1000 <= word_count <= 10000:  # Reasonable speech length
            confidence += 20
        elif word_count > 500:
            confidence += 10
        
        # Pattern matching
        content_lower = content.lower()
        title_lower = title.lower()
        
        # Positive indicators
        if any(word in title_lower for word in ['transcript', 'speech', 'remarks']):
            confidence += 15
        
        if any(word in title_lower for word in ['president', 'biden', 'trump']):
            confidence += 10
            
        pattern_matches = sum(1 for pattern in self.transcript_patterns 
                            if re.search(pattern, content_lower))
        confidence += pattern_matches * 5
        
        # Quality indicators
        if re.search(r'[.!?]', content):  # Has punctuation
            confidence += 10
            
        if len(content.split('\n')) > 10:  # Reasonable paragraph structure
            confidence += 5
        
        return min(confidence, 100.0)


def save_transcript(result: TranscriptScrapingResult, output_dir: Path, 
                   save_metadata: bool = True):
    """Save transcript scraping results"""
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if not result.success:
        print(f"❌ Cannot save results: {result.error_message}")
        return
    
    # Generate filename from URL and title
    domain = urlparse(result.url).netloc.replace('www.', '')
    safe_title = re.sub(r'[^\w\s-]', '', result.title or 'transcript')
    safe_title = re.sub(r'[-\s]+', '_', safe_title)[:50]
    filename = f"{domain}_{safe_title}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    # Save transcript
    transcript_file = output_dir / filename
    with open(transcript_file, 'w', encoding='utf-8') as f:
        # Write header
        f.write(f"# {result.title or 'Web Transcript'}\\n")
        f.write(f"# Source URL: {result.url}\\n")
        f.write(f"# Extraction Method: {result.method_used}\\n")
        f.write(f"# Word Count: {result.word_count or 0}\\n")
        f.write(f"# Confidence: {result.confidence_score:.1f}%\\n")
        f.write(f"# Extracted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n")
        f.write("\\n" + "="*80 + "\\n\\n")
        f.write(result.content)
    
    print(f"📄 Transcript saved: {transcript_file}")
    
    # Save metadata if requested
    if save_metadata:
        metadata_file = output_dir / f"{filename.replace('.txt', '_metadata.json')}"
        
        full_metadata = {
            "url": result.url,
            "title": result.title,
            "method_used": result.method_used,
            "word_count": result.word_count,
            "confidence_score": result.confidence_score,
            "success": result.success,
            "extraction_metadata": result.metadata or {}
        }
        
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(full_metadata, f, indent=2, ensure_ascii=False)
        
        print(f"📊 Metadata saved: {metadata_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Stealth Transcript Scraper for bypassing web access restrictions",
        epilog="Example: python3 scripts/stealth_transcript_scraper.py 'https://example.com/speech' -o ./output"
    )
    
    parser.add_argument("url", help="URL to scrape transcript from")
    
    parser.add_argument(
        "--output-dir", "-o",
        type=Path,
        help="Output directory (default: ./stealth_extractions_TIMESTAMP)"
    )
    
    parser.add_argument(
        "--method", "-m",
        choices=["auto", "selenium", "playwright", "requests"],
        default="auto",
        help="Scraping method (default: auto)"
    )
    
    parser.add_argument(
        "--no-metadata",
        action="store_true",
        help="Skip saving metadata JSON file"
    )
    
    args = parser.parse_args()
    
    # Set default output directory
    if not args.output_dir:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        args.output_dir = Path(f"./stealth_extractions_{timestamp}")
    
    print(f"🎭 Stealth Transcript Scraper")
    print(f"📋 URL: {args.url}")
    print(f"📁 Output: {args.output_dir}")
    print(f"🔧 Method: {args.method}")
    print("=" * 60)
    
    # Check dependencies
    if not SELENIUM_AVAILABLE and not PLAYWRIGHT_AVAILABLE:
        print("⚠️  No browser automation libraries available")
        print("📦 Install with: pip install undetected-chromedriver playwright")
    
    # Initialize scraper
    scraper = StealthTranscriptScraper()
    
    # Scrape transcript
    result = scraper.scrape_transcript(args.url, args.method)
    
    if result.success:
        # Save results
        save_transcript(result, args.output_dir, save_metadata=not args.no_metadata)
        
        print("=" * 60)
        print("✅ Stealth extraction completed successfully!")
        print(f"📊 Stats:")
        print(f"  - Method: {result.method_used}")
        print(f"  - Word count: {result.word_count:,}")
        print(f"  - Confidence: {result.confidence_score:.1f}%")
        print(f"  - Title: {result.title}")
        
        return 0
    else:
        print(f"❌ Stealth extraction failed: {result.error_message}")
        return 1


if __name__ == "__main__":
    exit(main())