#!/usr/bin/env python3
"""
Perplexity Citation-Source Correlation Analysis
Analyzes whether citations mentioned in text actually correlate with provided source lists.

Usage:
    python3 scripts/analyze_perplexity_citations.py --file response.md
    python3 scripts/analyze_perplexity_citations.py --compare file1.md file2.md
"""

import re
import argparse
import requests
from urllib.parse import urlparse
from typing import Dict, List, Tuple, Set
import json

class PerplexityCitationAnalyzer:
    def __init__(self):
        self.citation_patterns = [
            r'([A-Z][a-z]+ et al\.?,? \d{4})',  # "Smith et al. 2024"
            r'([A-Z][a-z]+ & [A-Z][a-z]+,? \d{4})',  # "Smith & Jones 2024"
            r'([A-Z][a-z]+,? \d{4})',  # "Smith 2024"
            r'"([^"]+)" \([^)]+\d{4}\)',  # Paper titles in quotes
        ]
        
    def extract_citations_from_text(self, text: str) -> Set[str]:
        """Extract academic citations mentioned in the text."""
        citations = set()
        
        # Remove footnote references to focus on inline citations
        text_clean = re.sub(r'\[\^\d+\]', '', text)
        
        for pattern in self.citation_patterns:
            matches = re.findall(pattern, text_clean)
            citations.update(matches)
            
        return citations
    
    def extract_footnote_sources(self, text: str) -> Dict[str, str]:
        """Extract footnote sources from bottom of response."""
        footnote_pattern = r'\[\^(\d+)\]:\s*(.+)'
        footnotes = {}
        
        matches = re.findall(footnote_pattern, text)
        for num, url in matches:
            footnotes[num] = url.strip()
            
        return footnotes
    
    def categorize_source_quality(self, url: str) -> str:
        """Categorize source quality based on domain and URL patterns."""
        if not url.startswith('http'):
            return 'LOCAL_FILE'
            
        domain = urlparse(url).netloc.lower()
        
        # High quality academic sources
        high_quality_domains = [
            'arxiv.org', 'doi.org', 'pubmed.ncbi.nlm.nih.gov', 'pmc.ncbi.nlm.nih.gov',
            'nature.com', 'science.org', 'cell.com', 'springer.com', 'acm.org',
            'ieee.org', 'jstor.org', 'wiley.com', 'sage.com', 'cambridge.org',
            'oxford.edu', 'harvard.edu', 'mit.edu', 'stanford.edu',
            'nationalacademies.org', 'nih.gov', 'nsf.gov'
        ]
        
        # Medium quality institutional/conference sources
        medium_quality_domains = [
            'gesis.org', 'cessda.eu', 'figshare.com', 'osf.io', 'researchgate.net',
            'ssrn.com', 'biorxiv.org', 'socarxiv.org'
        ]
        
        # Conference/workshop sources
        conference_patterns = [
            'workshop', 'conference', 'symposium', '2024', '2025',
            'cfp', 'call-for-papers'
        ]
        
        for hq_domain in high_quality_domains:
            if hq_domain in domain:
                return 'HIGH_QUALITY'
                
        for mq_domain in medium_quality_domains:
            if mq_domain in domain:
                return 'MEDIUM_QUALITY'
                
        if any(pattern in url.lower() for pattern in conference_patterns):
            return 'CONFERENCE_EVENT'
            
        return 'LOW_QUALITY'
    
    def check_source_accessibility(self, url: str) -> str:
        """Check if source URL is accessible."""
        if not url.startswith('http'):
            return 'LOCAL_FILE'
            
        try:
            response = requests.head(url, timeout=10, allow_redirects=True)
            if response.status_code == 200:
                return 'ACCESSIBLE'
            elif response.status_code == 404:
                return 'NOT_FOUND'
            elif response.status_code == 403:
                return 'PAYWALL'
            else:
                return f'HTTP_{response.status_code}'
        except Exception as e:
            return f'ERROR: {str(e)[:50]}'
    
    def analyze_citation_source_correlation(self, citations: Set[str], footnotes: Dict[str, str]) -> Dict:
        """Analyze correlation between mentioned citations and provided sources."""
        correlation_analysis = {
            'total_citations_mentioned': len(citations),
            'total_sources_provided': len(footnotes),
            'source_quality_breakdown': {},
            'accessibility_check': {},
            'citation_verification': {},
            'recommendations': []
        }
        
        # Analyze source quality
        quality_counts = {'HIGH_QUALITY': 0, 'MEDIUM_QUALITY': 0, 'LOW_QUALITY': 0, 
                         'LOCAL_FILE': 0, 'CONFERENCE_EVENT': 0}
        
        for num, url in footnotes.items():
            quality = self.categorize_source_quality(url)
            quality_counts[quality] += 1
            
            # Check accessibility
            accessibility = self.check_source_accessibility(url)
            correlation_analysis['accessibility_check'][num] = {
                'url': url,
                'quality': quality,
                'accessibility': accessibility
            }
        
        correlation_analysis['source_quality_breakdown'] = quality_counts
        
        # Generate recommendations
        if quality_counts['LOCAL_FILE'] > 3:
            correlation_analysis['recommendations'].append(
                f"⚠️ High local file pollution: {quality_counts['LOCAL_FILE']} local files in source list"
            )
            
        if quality_counts['HIGH_QUALITY'] < 3:
            correlation_analysis['recommendations'].append(
                f"⚠️ Low high-quality sources: Only {quality_counts['HIGH_QUALITY']} high-quality academic sources"
            )
            
        high_quality_ratio = quality_counts['HIGH_QUALITY'] / len(footnotes) if footnotes else 0
        correlation_analysis['high_quality_ratio'] = high_quality_ratio
        
        if high_quality_ratio < 0.3:
            correlation_analysis['recommendations'].append(
                f"⚠️ Low quality ratio: Only {high_quality_ratio:.1%} of sources are high quality"
            )
        
        return correlation_analysis
    
    def analyze_file(self, filepath: str) -> Dict:
        """Analyze a single Perplexity response file."""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        citations = self.extract_citations_from_text(content)
        footnotes = self.extract_footnote_sources(content)
        
        analysis = self.analyze_citation_source_correlation(citations, footnotes)
        analysis['file'] = filepath
        analysis['citations_found'] = list(citations)
        
        return analysis
    
    def compare_files(self, file1: str, file2: str) -> Dict:
        """Compare two Perplexity response files."""
        analysis1 = self.analyze_file(file1)
        analysis2 = self.analyze_file(file2)
        
        comparison = {
            'file1': analysis1,
            'file2': analysis2,
            'comparison': {
                'quality_improvement': (
                    analysis2['high_quality_ratio'] - analysis1['high_quality_ratio']
                ),
                'source_count_change': (
                    analysis2['total_sources_provided'] - analysis1['total_sources_provided']
                ),
                'recommendations': []
            }
        }
        
        if comparison['comparison']['quality_improvement'] > 0:
            comparison['comparison']['recommendations'].append(
                f"✅ File 2 has higher quality ratio: {comparison['comparison']['quality_improvement']:.1%} improvement"
            )
        
        if comparison['comparison']['source_count_change'] < 0:
            comparison['comparison']['recommendations'].append(
                f"✅ File 2 has fewer sources: {abs(comparison['comparison']['source_count_change'])} fewer sources (less clutter)"
            )
            
        return comparison
    
    def print_analysis_report(self, analysis: Dict):
        """Print formatted analysis report."""
        print(f"\n📊 PERPLEXITY CITATION ANALYSIS: {analysis['file']}")
        print("=" * 60)
        
        print(f"📝 Citations mentioned in text: {analysis['total_citations_mentioned']}")
        if analysis['citations_found']:
            for citation in analysis['citations_found']:
                print(f"   • {citation}")
        
        print(f"\n🔗 Sources provided: {analysis['total_sources_provided']}")
        
        print(f"\n📈 Source Quality Breakdown:")
        quality = analysis['source_quality_breakdown']
        total = sum(quality.values())
        for category, count in quality.items():
            percentage = (count / total * 100) if total > 0 else 0
            print(f"   {category}: {count} ({percentage:.1f}%)")
        
        print(f"\n🎯 High Quality Ratio: {analysis['high_quality_ratio']:.1%}")
        
        if analysis['recommendations']:
            print(f"\n⚠️ Recommendations:")
            for rec in analysis['recommendations']:
                print(f"   {rec}")
        
        print(f"\n🔍 Accessibility Check:")
        accessible = sum(1 for v in analysis['accessibility_check'].values() 
                        if v['accessibility'] == 'ACCESSIBLE')
        total_external = sum(1 for v in analysis['accessibility_check'].values() 
                           if v['quality'] != 'LOCAL_FILE')
        if total_external > 0:
            print(f"   {accessible}/{total_external} external sources accessible ({accessible/total_external:.1%})")

def main():
    parser = argparse.ArgumentParser(description='Analyze Perplexity citation quality')
    parser.add_argument('--file', help='Single file to analyze')
    parser.add_argument('--compare', nargs=2, help='Compare two files')
    parser.add_argument('--output', help='Output JSON file for detailed results')
    
    args = parser.parse_args()
    analyzer = PerplexityCitationAnalyzer()
    
    if args.compare:
        comparison = analyzer.compare_files(args.compare[0], args.compare[1])
        
        print("🔄 COMPARISON ANALYSIS")
        print("=" * 60)
        analyzer.print_analysis_report(comparison['file1'])
        analyzer.print_analysis_report(comparison['file2'])
        
        print(f"\n📊 COMPARISON SUMMARY:")
        comp = comparison['comparison']
        print(f"Quality improvement: {comp['quality_improvement']:+.1%}")
        print(f"Source count change: {comp['source_count_change']:+d}")
        
        for rec in comp['recommendations']:
            print(f"   {rec}")
            
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(comparison, f, indent=2)
                
    elif args.file:
        analysis = analyzer.analyze_file(args.file)
        analyzer.print_analysis_report(analysis)
        
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(analysis, f, indent=2)
    else:
        parser.print_help()

if __name__ == '__main__':
    main() 