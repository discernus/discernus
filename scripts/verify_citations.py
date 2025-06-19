#!/usr/bin/env python3
"""
Citation Verification Script
Helps detect AI-generated fake citations by checking multiple verification sources.

Usage:
    python3 scripts/verify_citations.py --title "Paper Title" --authors "Author1, Author2" --year 2024
    python3 scripts/verify_citations.py --bibtex citation.bib
    python3 scripts/verify_citations.py --batch citations.txt
"""

import argparse
import requests
import json
import time
from urllib.parse import quote
import sys
import os

class CitationVerifier:
    def __init__(self):
        self.results = []
        
    def verify_citation(self, title, authors=None, journal=None, year=None):
        """Verify a single citation using multiple methods."""
        print(f"\n🔍 Verifying: {title}")
        
        result = {
            'title': title,
            'authors': authors,
            'journal': journal,
            'year': year,
            'verification_status': 'UNKNOWN',
            'checks': {},
            'confidence': 0,
            'red_flags': [],
            'recommendations': []
        }
        
        # Check 1: Crossref DOI verification
        result['checks']['crossref'] = self._check_crossref(title, authors)
        
        # Check 2: Google Scholar simulation (search pattern analysis)
        result['checks']['scholar_pattern'] = self._check_scholar_pattern(title, authors)
        
        # Check 3: Journal verification
        if journal:
            result['checks']['journal'] = self._check_journal(journal)
            
        # Check 4: Author pattern analysis
        if authors:
            result['checks']['authors'] = self._check_author_patterns(authors)
            
        # Check 5: Timeline consistency
        if year:
            result['checks']['timeline'] = self._check_timeline(year)
            
        # Calculate confidence and flags
        self._analyze_results(result)
        
        return result
    
    def _check_crossref(self, title, authors):
        """Check Crossref API for title existence."""
        try:
            # Crossref API search
            query = quote(title)
            url = f"https://api.crossref.org/works?query={query}&rows=5"
            
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                items = data.get('message', {}).get('items', [])
                
                for item in items:
                    item_title = item.get('title', [''])[0].lower()
                    if title.lower() in item_title or item_title in title.lower():
                        return {
                            'status': 'FOUND',
                            'doi': item.get('DOI'),
                            'publisher': item.get('publisher'),
                            'match_quality': 'HIGH' if title.lower() == item_title else 'PARTIAL'
                        }
                        
                return {'status': 'NOT_FOUND', 'searched': True}
            else:
                return {'status': 'ERROR', 'message': f"API error: {response.status_code}"}
                
        except Exception as e:
            return {'status': 'ERROR', 'message': str(e)}
    
    def _check_scholar_pattern(self, title, authors):
        """Analyze patterns that suggest fake citations."""
        patterns = {
            'title_length': len(title.split()),
            'has_colon': ':' in title,
            'has_subtitle': ':' in title or '–' in title,
            'academic_words': sum(1 for word in ['analysis', 'study', 'research', 'method', 'approach', 'investigation'] 
                                if word.lower() in title.lower())
        }
        
        # Red flags for fake citations
        red_flags = []
        if patterns['title_length'] > 15:
            red_flags.append("Unusually long title")
        if patterns['academic_words'] > 3:
            red_flags.append("Too many academic buzzwords")
            
        return {
            'patterns': patterns,
            'red_flags': red_flags,
            'suspicion_level': 'HIGH' if len(red_flags) > 1 else 'LOW'
        }
    
    def _check_journal(self, journal):
        """Basic journal verification."""
        # Check against known predatory journal patterns
        predatory_patterns = [
            'international journal of',
            'global journal of',
            'world journal of',
            'advances in',
            'research in'
        ]
        
        journal_lower = journal.lower()
        predatory_score = sum(1 for pattern in predatory_patterns if pattern in journal_lower)
        
        return {
            'journal': journal,
            'predatory_score': predatory_score,
            'warning': 'Possible predatory journal pattern' if predatory_score >= 2 else None
        }
    
    def _check_author_patterns(self, authors):
        """Analyze author name patterns for authenticity."""
        author_list = [name.strip() for name in authors.split(',')]
        
        patterns = {
            'author_count': len(author_list),
            'has_initials': any('.' in name for name in author_list),
            'name_lengths': [len(name.split()) for name in author_list]
        }
        
        warnings = []
        if patterns['author_count'] > 10:
            warnings.append("Unusually high author count")
        if not patterns['has_initials']:
            warnings.append("No authors with initials (unusual for academic papers)")
            
        return {
            'patterns': patterns,
            'warnings': warnings
        }
    
    def _check_timeline(self, year):
        """Check if publication year is reasonable."""
        current_year = 2024
        year = int(year)
        
        warnings = []
        if year > current_year:
            warnings.append(f"Future publication date: {year}")
        if year < 1990:
            warnings.append(f"Very old publication: {year}")
            
        return {
            'year': year,
            'warnings': warnings
        }
    
    def _analyze_results(self, result):
        """Analyze all checks to determine overall confidence and recommendations."""
        confidence = 0
        red_flags = []
        recommendations = []
        
        # Crossref analysis
        crossref = result['checks'].get('crossref', {})
        if crossref.get('status') == 'FOUND':
            confidence += 40
            recommendations.append("✅ Found in Crossref - likely legitimate")
        elif crossref.get('status') == 'NOT_FOUND':
            confidence -= 30
            red_flags.append("❌ Not found in Crossref database")
            recommendations.append("🔍 Manual verification required - search Google Scholar")
        
        # Pattern analysis
        scholar = result['checks'].get('scholar_pattern', {})
        if scholar.get('suspicion_level') == 'HIGH':
            confidence -= 20
            red_flags.extend(scholar.get('red_flags', []))
        
        # Journal analysis
        journal_check = result['checks'].get('journal', {})
        if journal_check and journal_check.get('warning'):
            confidence -= 15
            red_flags.append(journal_check['warning'])
        
        # Timeline analysis
        timeline = result['checks'].get('timeline', {})
        if timeline.get('warnings'):
            confidence -= 10
            red_flags.extend(timeline['warnings'])
        
        # Determine status
        if confidence >= 30:
            status = 'LIKELY_LEGITIMATE'
        elif confidence >= 0:
            status = 'REQUIRES_VERIFICATION'
        else:
            status = 'SUSPICIOUS'
            
        result['confidence'] = max(0, min(100, confidence + 50))  # Normalize to 0-100
        result['verification_status'] = status
        result['red_flags'] = red_flags
        result['recommendations'] = recommendations
        
        return result
    
    def print_verification_report(self, result):
        """Print a formatted verification report."""
        print("\n" + "="*60)
        print(f"📋 CITATION VERIFICATION REPORT")
        print("="*60)
        
        print(f"Title: {result['title']}")
        if result['authors']:
            print(f"Authors: {result['authors']}")
        if result['journal']:
            print(f"Journal: {result['journal']}")
        if result['year']:
            print(f"Year: {result['year']}")
            
        print(f"\n🎯 Status: {result['verification_status']}")
        print(f"🔢 Confidence: {result['confidence']}/100")
        
        if result['red_flags']:
            print(f"\n🚨 Red Flags:")
            for flag in result['red_flags']:
                print(f"   • {flag}")
        
        if result['recommendations']:
            print(f"\n💡 Recommendations:")
            for rec in result['recommendations']:
                print(f"   • {rec}")
                
        # Crossref details
        crossref = result['checks'].get('crossref', {})
        if crossref.get('status') == 'FOUND':
            print(f"\n✅ Crossref Verification:")
            print(f"   DOI: {crossref.get('doi', 'Not available')}")
            print(f"   Publisher: {crossref.get('publisher', 'Not available')}")
            print(f"   Match Quality: {crossref.get('match_quality', 'Unknown')}")
        
        print("\n" + "="*60)

def main():
    parser = argparse.ArgumentParser(description='Verify academic citations for AI hallucinations')
    parser.add_argument('--title', help='Paper title to verify')
    parser.add_argument('--authors', help='Authors (comma-separated)')
    parser.add_argument('--journal', help='Journal name')
    parser.add_argument('--year', type=int, help='Publication year')
    parser.add_argument('--batch', help='File with citations to verify (one per line)')
    parser.add_argument('--output', help='Output file for results (JSON format)')
    
    args = parser.parse_args()
    
    if not any([args.title, args.batch]):
        parser.print_help()
        sys.exit(1)
    
    verifier = CitationVerifier()
    
    if args.title:
        # Single citation verification
        result = verifier.verify_citation(args.title, args.authors, args.journal, args.year)
        verifier.print_verification_report(result)
        
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(result, f, indent=2)
                
    elif args.batch:
        # Batch verification
        print("🔄 Batch verification mode not yet implemented")
        print("💡 For now, run single citations individually")
    
    print(f"\n💡 Pro tip: Always verify suspicious citations manually!")
    print(f"🔍 Check: Google Scholar, journal website, author pages")

if __name__ == '__main__':
    main() 