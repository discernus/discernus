#!/usr/bin/env python3
"""
Identify video targets for Donald Trump's post-presidency period (2021-2023)
Focuses on major events, rallies, and speeches that would have video recordings
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Major events and rallies from 2021-2023 (post-presidency)
POST_PRESIDENCY_EVENTS = {
    "2021": [
        {
            "date": "2021-02-28",
            "event": "CPAC 2021",
            "location": "Orlando, Florida",
            "type": "Conservative Political Action Conference",
            "notes": "First major post-presidency speech, already extracted"
        },
        {
            "date": "2021-06-26",
            "event": "Ohio Rally",
            "location": "Lorain, Ohio",
            "type": "Campaign Rally",
            "notes": "First post-presidency rally"
        },
        {
            "date": "2021-07-03",
            "event": "Florida Rally",
            "location": "Sarasota, Florida",
            "type": "Campaign Rally",
            "notes": "Fourth of July weekend rally"
        },
        {
            "date": "2021-07-24",
            "event": "Arizona Rally",
            "location": "Phoenix, Arizona",
            "type": "Campaign Rally",
            "notes": "Election audit rally"
        },
        {
            "date": "2021-08-21",
            "event": "Alabama Rally",
            "location": "Cullman, Alabama",
            "type": "Campaign Rally",
            "notes": "Large outdoor rally"
        },
        {
            "date": "2021-09-25",
            "event": "Georgia Rally",
            "location": "Perry, Georgia",
            "type": "Campaign Rally",
            "notes": "Supporting GOP candidates"
        },
        {
            "date": "2021-10-09",
            "event": "Iowa Rally",
            "location": "Des Moines, Iowa",
            "type": "Campaign Rally",
            "notes": "Early primary state"
        },
        {
            "date": "2021-11-20",
            "event": "Florida Rally",
            "location": "Tampa, Florida",
            "type": "Campaign Rally",
            "notes": "Thanksgiving weekend"
        }
    ],
    "2022": [
        {
            "date": "2022-01-15",
            "event": "Arizona Rally",
            "location": "Florence, Arizona",
            "type": "Campaign Rally",
            "notes": "Election integrity focus"
        },
        {
            "date": "2022-02-26",
            "event": "CPAC 2022",
            "location": "Orlando, Florida",
            "type": "Conservative Political Action Conference",
            "notes": "Annual CPAC speech"
        },
        {
            "date": "2022-03-26",
            "event": "Georgia Rally",
            "location": "Commerce, Georgia",
            "type": "Campaign Rally",
            "notes": "Primary season"
        },
        {
            "date": "2022-04-09",
            "event": "North Carolina Rally",
            "location": "Selma, North Carolina",
            "type": "Campaign Rally",
            "notes": "Primary support"
        },
        {
            "date": "2022-05-28",
            "event": "Texas Rally",
            "location": "Houston, Texas",
            "type": "Campaign Rally",
            "notes": "NRA convention"
        },
        {
            "date": "2022-06-18",
            "event": "Nashville Rally",
            "location": "Nashville, Tennessee",
            "type": "Campaign Rally",
            "notes": "Faith and Freedom Coalition"
        },
        {
            "date": "2022-07-23",
            "event": "Arizona Rally",
            "location": "Prescott Valley, Arizona",
            "type": "Campaign Rally",
            "notes": "Primary election support"
        },
        {
            "date": "2022-08-06",
            "event": "Wisconsin Rally",
            "location": "Waukesha, Wisconsin",
            "type": "Campaign Rally",
            "notes": "Midterm support"
        },
        {
            "date": "2022-09-03",
            "event": "Pennsylvania Rally",
            "location": "Wilkes-Barre, Pennsylvania",
            "type": "Campaign Rally",
            "notes": "Senate race support"
        },
        {
            "date": "2022-10-22",
            "event": "Texas Rally",
            "location": "Robstown, Texas",
            "type": "Campaign Rally",
            "notes": "Midterm election support"
        },
        {
            "date": "2022-11-05",
            "event": "Florida Rally",
            "location": "Miami, Florida",
            "type": "Campaign Rally",
            "notes": "Election eve rally"
        }
    ],
    "2023": [
        {
            "date": "2023-01-28",
            "event": "New Hampshire Rally",
            "location": "Salem, New Hampshire",
            "type": "Campaign Rally",
            "notes": "Early primary state"
        },
        {
            "date": "2023-02-25",
            "event": "CPAC 2023",
            "location": "National Harbor, Maryland",
            "type": "Conservative Political Action Conference",
            "notes": "Annual CPAC speech"
        },
        {
            "date": "2023-03-04",
            "event": "South Carolina Rally",
            "location": "Columbia, South Carolina",
            "type": "Campaign Rally",
            "notes": "Primary state"
        },
        {
            "date": "2023-04-22",
            "event": "Iowa Rally",
            "location": "Davenport, Iowa",
            "type": "Campaign Rally",
            "notes": "First in the nation caucus"
        },
        {
            "date": "2023-05-13",
            "event": "Ohio Rally",
            "location": "Vandalia, Ohio",
            "type": "Campaign Rally",
            "notes": "Primary support"
        },
        {
            "date": "2023-06-10",
            "event": "Georgia Rally",
            "location": "Columbus, Georgia",
            "type": "Campaign Rally",
            "notes": "Primary season"
        },
        {
            "date": "2023-07-01",
            "event": "South Carolina Rally",
            "location": "Pickens, South Carolina",
            "type": "Campaign Rally",
            "notes": "Fourth of July weekend"
        },
        {
            "date": "2023-08-12",
            "event": "Iowa Rally",
            "location": "Des Moines, Iowa",
            "type": "Campaign Rally",
            "notes": "State fair rally"
        },
        {
            "date": "2023-09-16",
            "event": "South Dakota Rally",
            "location": "Rapid City, South Dakota",
            "type": "Campaign Rally",
            "notes": "Primary support"
        },
        {
            "date": "2023-10-07",
            "event": "New Hampshire Rally",
            "location": "Laconia, New Hampshire",
            "type": "Campaign Rally",
            "notes": "Primary state focus"
        },
        {
            "date": "2023-11-11",
            "event": "Florida Rally",
            "location": "Hialeah, Florida",
            "type": "Campaign Rally",
            "notes": "Veterans Day rally"
        }
    ]
}

def generate_video_search_queries() -> List[Dict[str, str]]:
    """Generate search queries for finding videos of these events"""
    queries = []
    
    for year, events in POST_PRESIDENCY_EVENTS.items():
        for event in events:
            # Create multiple search variations for each event
            base_query = f"Donald Trump {event['event']} {event['location']} {event['date']}"
            
            # Variation 1: Full event name
            queries.append({
                "event": event['event'],
                "date": event['date'],
                "location": event['location'],
                "search_query": base_query,
                "priority": "high" if "CPAC" in event['event'] else "medium"
            })
            
            # Variation 2: Rally focus
            if "Rally" in event['type']:
                rally_query = f"Donald Trump rally {event['location']} {event['date']}"
                queries.append({
                    "event": event['event'],
                    "date": event['date'],
                    "location": event['location'],
                    "search_query": rally_query,
                    "priority": "medium"
                })
            
            # Variation 3: Speech focus
            speech_query = f"Donald Trump speech {event['location']} {event['date']}"
            queries.append({
                "event": event['event'],
                "date": event['date'],
                "location": event['location'],
                "search_query": speech_query,
                "priority": "medium"
            })
    
    return queries

def create_video_target_manifest() -> Dict[str, Any]:
    """Create a comprehensive manifest of video targets"""
    manifest = {
        "metadata": {
            "created_at": datetime.now().isoformat(),
            "description": "Video targets for Donald Trump post-presidency speeches (2021-2023)",
            "total_events": sum(len(events) for events in POST_PRESIDENCY_EVENTS.values()),
            "extraction_status": "pending"
        },
        "events_by_year": POST_PRESIDENCY_EVENTS,
        "search_queries": generate_video_search_queries(),
        "extraction_notes": {
            "strategy": "Targeted YouTube searches for specific events and dates",
            "priority_order": ["CPAC speeches", "Major rallies", "Primary support events"],
            "expected_sources": ["YouTube channels", "News organizations", "Political channels"],
            "challenges": ["Some events may not have public video", "Quality varies by source"]
        }
    }
    
    return manifest

def save_manifest(manifest: Dict[str, Any], output_dir: str) -> str:
    """Save the manifest to the specified directory"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Save as JSON
    json_path = output_path / "post_presidency_video_targets.json"
    with open(json_path, 'w') as f:
        json.dump(manifest, f, indent=2)
    
    # Save as text summary
    txt_path = output_path / "post_presidency_video_targets.txt"
    with open(txt_path, 'w') as f:
        f.write("POST-PRESIDENCY VIDEO TARGETS (2021-2023)\n")
        f.write("=" * 50 + "\n\n")
        
        for year, events in manifest["events_by_year"].items():
            f.write(f"{year} EVENTS:\n")
            f.write("-" * 20 + "\n")
            for event in events:
                f.write(f"• {event['date']}: {event['event']} - {event['location']}\n")
                f.write(f"  Type: {event['type']}\n")
                f.write(f"  Notes: {event['notes']}\n\n")
        
        f.write(f"\nTOTAL EVENTS: {manifest['metadata']['total_events']}\n")
        f.write(f"SEARCH QUERIES: {len(manifest['search_queries'])}\n")
        f.write(f"CREATED: {manifest['metadata']['created_at']}\n")
    
    return str(json_path)

def main():
    """Main function to generate and save the video target manifest"""
    logger.info("Generating post-presidency video target manifest...")
    
    # Create manifest
    manifest = create_video_target_manifest()
    
    # Save to the post-presidency corpus directory
    output_dir = "projects/2d_trump_populism/corpus/post_presidency_2021_2023"
    json_path = save_manifest(manifest, output_dir)
    
    logger.info(f"Manifest saved to: {json_path}")
    logger.info(f"Total events identified: {manifest['metadata']['total_events']}")
    logger.info(f"Search queries generated: {len(manifest['search_queries'])}")
    
    # Print summary
    print(f"\n📋 POST-PRESIDENCY VIDEO TARGETS GENERATED")
    print(f"📁 Saved to: {output_dir}")
    print(f"🎯 Total events: {manifest['metadata']['total_events']}")
    print(f"🔍 Search queries: {len(manifest['search_queries'])}")
    print(f"\nNext steps:")
    print(f"1. Review the manifest in {output_dir}")
    print(f"2. Use search queries to find YouTube videos")
    print(f"3. Extract transcripts using enhanced_transcript_extractor.py")

if __name__ == "__main__":
    main()
