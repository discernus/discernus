#!/usr/bin/env python3
"""
Generate YouTube search URLs for Donald Trump's post-presidency events (2021-2023)
Creates searchable URLs and a manual search guide instead of requiring external search libraries
"""

import json
import logging
from pathlib import Path
from typing import List, Dict, Any
from urllib.parse import quote_plus

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class VideoSearchURLGenerator:
    """Generates YouTube search URLs for post-presidency events"""
    
    def __init__(self, manifest_path: str):
        self.manifest_path = Path(manifest_path)
        self.manifest = self._load_manifest()
        
    def _load_manifest(self) -> Dict[str, Any]:
        """Load the video targets manifest"""
        with open(self.manifest_path, 'r') as f:
            return json.load(f)
    
    def generate_search_urls(self) -> List[Dict[str, Any]]:
        """Generate YouTube search URLs for each event"""
        search_urls = []
        
        for year, events in self.manifest['events_by_year'].items():
            for event in events:
                # Create multiple search variations for each event
                event_name = event['event']
                date = event['date']
                location = event['location']
                
                # Base search query
                base_query = f"Donald Trump {event_name} {location} {date}"
                base_url = f"https://www.youtube.com/results?search_query={quote_plus(base_query)}"
                
                # Rally-specific search
                rally_query = f"Donald Trump rally {location} {date}"
                rally_url = f"https://www.youtube.com/results?search_query={quote_plus(rally_query)}"
                
                # Speech-specific search
                speech_query = f"Donald Trump speech {location} {date}"
                speech_url = f"https://www.youtube.com/results?search_query={quote_plus(speech_query)}"
                
                # Full speech search
                full_speech_query = f"Donald Trump full speech {location} {date}"
                full_speech_url = f"https://www.youtube.com/results?search_query={quote_plus(full_speech_query)}"
                
                search_urls.append({
                    'event': event_name,
                    'date': date,
                    'location': location,
                    'type': event['type'],
                    'notes': event['notes'],
                    'search_urls': {
                        'base': base_url,
                        'rally': rally_url,
                        'speech': speech_url,
                        'full_speech': full_speech_url
                    },
                    'priority': 'high' if 'CPAC' in event_name else 'medium'
                })
        
        return search_urls
    
    def save_search_guide(self, search_urls: List[Dict[str, Any]], output_dir: str) -> str:
        """Save a comprehensive search guide"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Save as JSON
        json_path = output_path / "youtube_search_urls.json"
        with open(json_path, 'w') as f:
            json.dump({
                'metadata': {
                    'total_events': len(search_urls),
                    'description': 'YouTube search URLs for post-presidency events',
                    'usage': 'Copy URLs to browser to search for videos'
                },
                'search_urls': search_urls
            }, f, indent=2)
        
        # Save as HTML for easy clicking
        html_path = output_path / "youtube_search_guide.html"
        with open(html_path, 'w') as f:
            f.write("""
<!DOCTYPE html>
<html>
<head>
    <title>YouTube Search Guide - Trump Post-Presidency Events</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .event { border: 1px solid #ddd; margin: 10px 0; padding: 15px; border-radius: 5px; }
        .event h3 { margin-top: 0; color: #333; }
        .search-links { margin: 10px 0; }
        .search-links a { display: inline-block; margin: 5px; padding: 8px 15px; 
                          background: #007bff; color: white; text-decoration: none; 
                          border-radius: 3px; }
        .search-links a:hover { background: #0056b3; }
        .priority-high { border-left: 4px solid #dc3545; }
        .priority-medium { border-left: 4px solid #ffc107; }
        .metadata { font-size: 0.9em; color: #666; margin: 5px 0; }
    </style>
</head>
<body>
    <h1>YouTube Search Guide - Trump Post-Presidency Events (2021-2023)</h1>
            """)
            
            # Group by year
            events_by_year = {}
            for item in search_urls:
                year = item['date'][:4]
                if year not in events_by_year:
                    events_by_year[year] = []
                events_by_year[year].append(item)
            
            for year in sorted(events_by_year.keys()):
                f.write(f"<h2>{year} Events</h2>")
                
                for item in events_by_year[year]:
                    priority_class = f"priority-{item['priority']}"
                    f.write(f'<div class="event {priority_class}">')
                    f.write(f"<h3>{item['event']} - {item['date']}</h3>")
                    f.write(f"<div class='metadata'>")
                    f.write(f"<strong>Location:</strong> {item['location']}<br>")
                    f.write(f"<strong>Type:</strong> {item['type']}<br>")
                    f.write(f"<strong>Notes:</strong> {item['notes']}<br>")
                    f.write(f"<strong>Priority:</strong> {item['priority'].title()}")
                    f.write(f"</div>")
                    
                    f.write(f"<div class='search-links'>")
                    f.write(f"<a href='{item['search_urls']['base']}' target='_blank'>Base Search</a>")
                    f.write(f"<a href='{item['search_urls']['rally']}' target='_blank'>Rally Search</a>")
                    f.write(f"<a href='{item['search_urls']['speech']}' target='_blank'>Speech Search</a>")
                    f.write(f"<a href='{item['search_urls']['full_speech']}' target='_blank'>Full Speech Search</a>")
                    f.write(f"</div>")
                    f.write(f"</div>")
            
            f.write("""
    <div style="margin-top: 30px; padding: 20px; background: #f8f9fa; border-radius: 5px;">
        <h3>Instructions:</h3>
        <ol>
            <li>Click any search link to open YouTube search results</li>
            <li>Look for videos with relevant titles and reasonable duration (10+ minutes for speeches)</li>
            <li>Copy the video URL for transcript extraction</li>
            <li>Focus on high-priority events first (CPAC speeches)</li>
        </ol>
    </div>
</body>
</html>
            """)
        
        # Save as text guide
        txt_path = output_path / "youtube_search_guide.txt"
        with open(txt_path, 'w') as f:
            f.write("YOUTUBE SEARCH GUIDE - TRUMP POST-PRESIDENCY EVENTS (2021-2023)\n")
            f.write("=" * 70 + "\n\n")
            f.write("INSTRUCTIONS:\n")
            f.write("1. Copy any search URL below to your browser\n")
            f.write("2. Look for videos with relevant titles and reasonable duration\n")
            f.write("3. Copy the video URL for transcript extraction\n")
            f.write("4. Focus on high-priority events first (CPAC speeches)\n\n")
            
            # Group by year
            events_by_year = {}
            for item in search_urls:
                year = item['date'][:4]
                if year not in events_by_year:
                    events_by_year[year] = []
                events_by_year[year].append(item)
            
            for year in sorted(events_by_year.keys()):
                f.write(f"{year} EVENTS:\n")
                f.write("-" * 20 + "\n")
                
                for item in events_by_year[year]:
                    f.write(f"• {item['event']} - {item['date']}\n")
                    f.write(f"  Location: {item['location']}\n")
                    f.write(f"  Type: {item['type']}\n")
                    f.write(f"  Priority: {item['priority'].title()}\n")
                    f.write(f"  Notes: {item['notes']}\n")
                    f.write(f"  Search URLs:\n")
                    f.write(f"    Base: {item['search_urls']['base']}\n")
                    f.write(f"    Rally: {item['search_urls']['rally']}\n")
                    f.write(f"    Speech: {item['search_urls']['speech']}\n")
                    f.write(f"    Full Speech: {item['search_urls']['full_speech']}\n\n")
            
            f.write(f"\nTOTAL EVENTS: {len(search_urls)}\n")
            f.write("Generated search URLs for manual YouTube searching\n")
        
        return str(json_path)
    
    def print_summary(self, search_urls: List[Dict[str, Any]]):
        """Print a summary of generated search URLs"""
        print(f"\n🔍 YOUTUBE SEARCH URLS GENERATED")
        print(f"=" * 40)
        print(f"Total events: {len(search_urls)}")
        
        # Count by priority
        high_priority = len([u for u in search_urls if u['priority'] == 'high'])
        medium_priority = len([u for u in search_urls if u['priority'] == 'medium'])
        
        print(f"High priority (CPAC): {high_priority}")
        print(f"Medium priority (rallies): {medium_priority}")
        
        print(f"\n📋 OUTPUT FILES:")
        print(f"• youtube_search_urls.json - Machine-readable format")
        print(f"• youtube_search_guide.html - Interactive HTML guide")
        print(f"• youtube_search_guide.txt - Text format for reference")
        
        print(f"\n🎯 NEXT STEPS:")
        print(f"1. Open youtube_search_guide.html in your browser")
        print(f"2. Click search links to find videos")
        print(f"3. Copy video URLs for transcript extraction")
        print(f"4. Start with high-priority CPAC events")

def main():
    """Main function to generate YouTube search URLs"""
    manifest_path = "projects/2d_trump_populism/corpus/post_presidency_2021_2023/post_presidency_video_targets.json"
    
    if not Path(manifest_path).exists():
        logger.error(f"Manifest not found: {manifest_path}")
        print("Please run identify_post_presidency_videos.py first to generate the manifest.")
        return
    
    logger.info("Generating YouTube search URLs...")
    
    # Initialize generator
    generator = VideoSearchURLGenerator(manifest_path)
    
    # Generate search URLs
    search_urls = generator.generate_search_urls()
    
    # Save search guide
    output_dir = "projects/2d_trump_populism/corpus/post_presidency_2021_2023"
    json_path = generator.save_search_guide(search_urls, output_dir)
    
    # Print summary
    generator.print_summary(search_urls)
    
    print(f"\n✅ Search guide generated! Files saved to: {output_dir}")

if __name__ == "__main__":
    main()
