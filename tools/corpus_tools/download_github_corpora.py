#!/usr/bin/env python3
"""
Download and integrate GitHub corpora for APDES experiment

This script downloads political speech corpora from GitHub repositories
and integrates them into the APDES corpus structure.
"""

import requests
import json
import os
from pathlib import Path
from typing import Dict, List, Optional
import time

class GitHubCorpusDownloader:
    """Download political speech corpora from GitHub repositories"""
    
    def __init__(self, output_dir: str = "corpus_sources/github"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # High-priority repositories for APDES
        self.high_priority_repos = [
            {
                'name': 'kaydenjordan/nlp_congress',
                'description': 'U.S Congressional Speech 1995-2023',
                'apdes_value': 'Very High - Comprehensive congressional speech data',
                'target_era': 'Era 1-4 (Legislative baseline)'
            },
            {
                'name': 'brownepres/trump-speech-analysis',
                'description': 'Trump 2024 campaign rhetoric analysis',
                'apdes_value': 'Very High - Era 4 populist consolidation',
                'target_era': 'Era 4 (2024)'
            },
            {
                'name': 'mlinegar/politicalRhetoric',
                'description': '2016 campaign speech analysis',
                'apdes_value': 'Very High - Era 2 populist emergence',
                'target_era': 'Era 2 (2016)'
            },
            {
                'name': 'Aiecco/Binary-Classification-of-Populist-Discourse',
                'description': 'Populist discourse classification models',
                'apdes_value': 'Very High - Pre-trained classification tools',
                'target_era': 'All Eras (Analysis tool)'
            }
        ]
        
        # Medium-priority repositories
        self.medium_priority_repos = [
            {
                'name': 'kfogel/presidential-speeches',
                'description': 'Raw presidential speech texts',
                'apdes_value': 'High - Presidential rhetoric baseline',
                'target_era': 'Era 1 (1992-2016)'
            },
            {
                'name': 'ui-libraries/congressional-speech',
                'description': 'Congressional Speech API',
                'apdes_value': 'High - API access to congressional rhetoric',
                'target_era': 'All Eras (API access)'
            }
        ]
    
    def get_repo_contents(self, repo_name: str) -> Optional[List[Dict]]:
        """Get contents of a GitHub repository"""
        api_url = f"https://api.github.com/repos/{repo_name}/contents"
        
        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Failed to access {repo_name}: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error accessing {repo_name}: {e}")
            return None
    
    def download_file(self, file_url: str, target_path: Path) -> bool:
        """Download a file from GitHub"""
        try:
            response = requests.get(file_url)
            if response.status_code == 200:
                target_path.parent.mkdir(parents=True, exist_ok=True)
                
                with open(target_path, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                
                print(f"✅ Downloaded: {target_path.name}")
                return True
            else:
                print(f"❌ Failed to download {file_url}: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Error downloading {file_url}: {e}")
            return False
    
    def is_relevant_file(self, filename: str) -> bool:
        """Check if file is relevant for corpus collection"""
        relevant_extensions = ['.txt', '.json', '.csv', '.md', '.py', '.ipynb']
        relevant_keywords = ['speech', 'transcript', 'corpus', 'data', 'analysis']
        
        # Check file extension
        if any(filename.endswith(ext) for ext in relevant_extensions):
            return True
        
        # Check filename for relevant keywords
        filename_lower = filename.lower()
        if any(keyword in filename_lower for keyword in relevant_keywords):
            return True
        
        return False
    
    def download_repo(self, repo_info: Dict) -> Dict:
        """Download relevant files from a repository"""
        repo_name = repo_info['name']
        repo_dir = self.output_dir / repo_name.split('/')[1]
        
        print(f"\n📥 Downloading {repo_name}: {repo_info['description']}")
        print(f"🎯 APDES Value: {repo_info['apdes_value']}")
        print(f"📅 Target Era: {repo_info['target_era']}")
        
        contents = self.get_repo_contents(repo_name)
        if not contents:
            return {'success': False, 'files_downloaded': 0}
        
        files_downloaded = 0
        total_files = 0
        
        for item in contents:
            if item['type'] == 'file' and self.is_relevant_file(item['name']):
                total_files += 1
                file_path = repo_dir / item['name']
                
                if self.download_file(item['download_url'], file_path):
                    files_downloaded += 1
                
                # Rate limiting
                time.sleep(0.1)
        
        print(f"📊 Downloaded {files_downloaded}/{total_files} relevant files")
        
        return {
            'success': files_downloaded > 0,
            'files_downloaded': files_downloaded,
            'total_files': total_files,
            'repo_dir': str(repo_dir)
        }
    
    def download_all_corpora(self) -> Dict:
        """Download all high-priority and medium-priority corpora"""
        results = {
            'high_priority': [],
            'medium_priority': [],
            'summary': {}
        }
        
        print("🚀 Starting GitHub corpus download for APDES experiment")
        print("=" * 60)
        
        # Download high-priority repositories
        print("\n🔥 HIGH PRIORITY REPOSITORIES")
        print("-" * 40)
        
        for repo in self.high_priority_repos:
            result = self.download_repo(repo)
            result['repo_info'] = repo
            results['high_priority'].append(result)
        
        # Download medium-priority repositories
        print("\n📚 MEDIUM PRIORITY REPOSITORIES")
        print("-" * 40)
        
        for repo in self.medium_priority_repos:
            result = self.download_repo(repo)
            result['repo_info'] = repo
            results['medium_priority'].append(result)
        
        # Generate summary
        total_downloaded = sum(r['files_downloaded'] for r in results['high_priority'] + results['medium_priority'])
        successful_repos = sum(1 for r in results['high_priority'] + results['medium_priority'] if r['success'])
        
        results['summary'] = {
            'total_repos_attempted': len(self.high_priority_repos) + len(self.medium_priority_repos),
            'successful_repos': successful_repos,
            'total_files_downloaded': total_downloaded,
            'output_directory': str(self.output_dir)
        }
        
        print("\n📈 DOWNLOAD SUMMARY")
        print("-" * 40)
        print(f"📁 Output Directory: {self.output_dir}")
        print(f"📦 Repositories Attempted: {results['summary']['total_repos_attempted']}")
        print(f"✅ Successful Downloads: {results['summary']['successful_repos']}")
        print(f"📄 Total Files Downloaded: {results['summary']['total_files_downloaded']}")
        
        return results
    
    def generate_integration_report(self, results: Dict) -> str:
        """Generate a report for APDES integration"""
        report = []
        report.append("# GitHub Corpus Download Report")
        report.append("")
        report.append(f"**Download Date**: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"**Output Directory**: {results['summary']['output_directory']}")
        report.append("")
        
        report.append("## High Priority Repositories")
        report.append("")
        for result in results['high_priority']:
            repo_info = result['repo_info']
            status = "✅" if result['success'] else "❌"
            report.append(f"- {status} **{repo_info['name']}**: {repo_info['description']}")
            report.append(f"  - APDES Value: {repo_info['apdes_value']}")
            report.append(f"  - Target Era: {repo_info['target_era']}")
            report.append(f"  - Files Downloaded: {result['files_downloaded']}/{result['total_files']}")
            report.append("")
        
        report.append("## Medium Priority Repositories")
        report.append("")
        for result in results['medium_priority']:
            repo_info = result['repo_info']
            status = "✅" if result['success'] else "❌"
            report.append(f"- {status} **{repo_info['name']}**: {repo_info['description']}")
            report.append(f"  - APDES Value: {repo_info['apdes_value']}")
            report.append(f"  - Target Era: {repo_info['target_era']}")
            report.append(f"  - Files Downloaded: {result['files_downloaded']}/{result['total_files']}")
            report.append("")
        
        report.append("## Next Steps for APDES Integration")
        report.append("")
        report.append("1. **Review Downloaded Files**: Examine the downloaded corpora for quality and relevance")
        report.append("2. **Standardize Metadata**: Apply APDES metadata standards to downloaded documents")
        report.append("3. **Validate Content**: Ensure temporal coverage matches APDES requirements")
        report.append("4. **Integrate with Pipeline**: Add downloaded sources to corpus collection workflow")
        report.append("5. **Update Documentation**: Add GitHub sources to comprehensive resource guide")
        
        return "\n".join(report)

def main():
    """Main function to download GitHub corpora"""
    downloader = GitHubCorpusDownloader()
    
    # Download all corpora
    results = downloader.download_all_corpora()
    
    # Generate and save report
    report = downloader.generate_integration_report(results)
    report_path = Path("corpus_sources/github/download_report.md")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(report_path, 'w') as f:
        f.write(report)
    
    print(f"\n📋 Report saved to: {report_path}")
    print("\n🎯 Next steps:")
    print("1. Review downloaded corpora in corpus_sources/github/")
    print("2. Check download_report.md for integration guidance")
    print("3. Update APDES corpus strategy with new sources")

if __name__ == "__main__":
    main() 