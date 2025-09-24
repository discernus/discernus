#!/usr/bin/env python3
"""
Extract Trump 2024 Campaign Speeches

This script processes the 2024 campaign data from the brownepres/trump-speech-analysis
repository and prepares it for integration into the Trump Populism Corpus.
"""

import pandas as pd
import os
import sys
from pathlib import Path
from datetime import datetime
import json

def load_2024_campaign_data():
    """Load the 2024 campaign data from the Excel file"""
    excel_path = "corpus/github_repositories/trump-speech-analysis/data-source/speeches.xlsx"
    
    if not os.path.exists(excel_path):
        print(f"❌ Excel file not found: {excel_path}")
        return None
    
    try:
        df = pd.read_excel(excel_path)
        print(f"✅ Loaded {len(df)} 2024 campaign speeches")
        return df
    except Exception as e:
        print(f"❌ Error loading Excel file: {e}")
        return None

def create_2024_campaign_structure():
    """Create the directory structure for 2024 campaign speeches"""
    base_dir = Path("projects/2d_trump_populism/corpus/2024_campaign")
    
    # Create subdirectories for different campaign phases
    subdirs = [
        "primary_campaign",      # Early primary positioning
        "general_election",      # General election campaign
        "closing_arguments",     # Final campaign stretch
        "victory_transition"     # Election night and transition
    ]
    
    for subdir in subdirs:
        (base_dir / subdir).mkdir(parents=True, exist_ok=True)
    
    print(f"✅ Created 2024 campaign directory structure")
    return base_dir

def categorize_speeches_by_phase(df):
    """Categorize speeches into campaign phases based on dates"""
    # Convert date strings to datetime objects
    df['date_dt'] = pd.to_datetime(df['date'].str.strip('"'), format='%Y-%m-%d')
    
    # Define phase boundaries
    primary_end = pd.to_datetime('2024-08-01')  # Primary season ends
    general_start = pd.to_datetime('2024-09-01')  # General election begins
    closing_start = pd.to_datetime('2024-10-15')  # Final campaign stretch
    election_day = pd.to_datetime('2024-11-05')   # Election day
    
    def get_phase(row):
        date = row['date_dt']
        if date < primary_end:
            return "primary_campaign"
        elif date < general_start:
            return "general_election"
        elif date < closing_start:
            return "general_election"
        elif date < election_day:
            return "closing_arguments"
        else:
            return "victory_transition"
    
    df['phase'] = df.apply(get_phase, axis=1)
    
    # Print phase distribution
    phase_counts = df['phase'].value_counts()
    print("\n📊 Campaign Phase Distribution:")
    for phase, count in phase_counts.items():
        print(f"  {phase}: {count} speeches")
    
    return df

def generate_metadata(df, base_dir):
    """Generate metadata for each speech"""
    metadata_list = []
    
    for idx, row in df.iterrows():
        # Create filename
        date_str = row['date'].strip('"')
        state = row['state']
        phase = row['phase']
        
        # Clean URL for filename
        url_clean = row['url'].split('watch?v=')[1].split('&')[0]
        filename = f"trump_2024_{date_str}_{state}_{url_clean}.txt"
        
        # Create metadata
        metadata = {
            "document_id": filename,
            "title": f"Trump 2024 Campaign Speech - {state} ({date_str})",
            "speaker": "Donald Trump",
            "speaker_role": "presidential_candidate",
            "date": date_str,
            "venue": f"Campaign Event in {state}",
            "category": "campaign_speech",
            "domain": "political",
            "language": "en",
            "country": "US",
            "audience_type": "campaign_rally",
            "formality_level": "informal",
            "rhetorical_style": ["campaign", "populist", "rally"],
            "campaign_phase": phase,
            "state": state,
            "youtube_url": row['url'],
            "trimming_needed": row['trimming_needed'],
            "file_path": f"corpus/2024_campaign/{phase}/{filename}",
            "file_size": 0,  # Will be updated after transcript extraction
            "word_count": 0,  # Will be updated after transcript extraction
            "transcript_quality": "youtube_auto",  # Will be updated after extraction
            "source": "brownepres/trump-speech-analysis",
            "collected_date": datetime.now().isoformat(),
            "collected_by": "extract_2024_campaign.py"
        }
        
        metadata_list.append(metadata)
    
    # Save metadata
    metadata_path = base_dir / "2024_campaign_metadata.json"
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata_list, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Generated metadata for {len(metadata_list)} speeches")
    return metadata_list

def create_extraction_script(df, base_dir):
    """Create a script to extract transcripts from YouTube URLs"""
    script_content = f'''#!/usr/bin/env python3
"""
Extract 2024 Campaign Speech Transcripts

This script uses the enhanced_transcript_extractor.py to extract transcripts
from the 74 Trump 2024 campaign speeches identified in the brownepres repository.
"""

import subprocess
import json
import os
from pathlib import Path

def extract_transcript(url, output_file):
    """Extract transcript from YouTube URL"""
    # Change to the project root directory to ensure correct paths
    project_root = Path(__file__).parent.parent.parent
    
    cmd = [
        "python3", "scripts/corpus_tools/enhanced_transcript_extractor.py",
        url,  # URL is positional argument
        "--output-dir", str(output_file.parent)
    ]
    
    try:
        # Run from project root directory
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300, cwd=project_root)
        if result.returncode == 0:
            print(f"✅ Extracted: {{output_file.name}}")
            return True
        else:
            print(f"❌ Failed: {{output_file.name}} - {{result.stderr}}")
            return False
    except subprocess.TimeoutExpired:
        print(f"⏰ Timeout: {{output_file.name}}")
        return False
    except Exception as e:
        print(f"❌ Error: {{output_file.name}} - {{e}}")
        return False

def main():
    # Load metadata
    metadata_path = Path("{base_dir}/2024_campaign_metadata.json")
    with open(metadata_path, 'r', encoding='utf-8') as f:
        metadata = json.load(f)
    
    print(f"🎯 Starting transcript extraction for {{len(metadata)}} speeches...")
    
    success_count = 0
    for speech in metadata:
        url = speech['youtube_url']
        output_file = Path(speech['file_path'])
        
        # Ensure output directory exists
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        if extract_transcript(url, output_file):
            success_count += 1
        
        # Rate limiting - wait between extractions
        import time
        time.sleep(2)
    
    print(f"\\n🎉 Extraction complete: {{success_count}}/{{len(metadata)}} successful")

if __name__ == "__main__":
    main()
'''
    
    script_path = base_dir / "extract_transcripts.py"
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    # Make executable
    os.chmod(script_path, 0o755)
    
    print(f"✅ Created transcript extraction script: {script_path}")

def main():
    """Main execution function"""
    print("🚀 Trump 2024 Campaign Speech Extraction")
    print("=" * 50)
    
    # Load data
    df = load_2024_campaign_data()
    if df is None:
        return
    
    # Create directory structure
    base_dir = create_2024_campaign_structure()
    
    # Categorize speeches by phase
    df = categorize_speeches_by_phase(df)
    
    # Generate metadata
    metadata = generate_metadata(df, base_dir)
    
    # Create extraction script
    create_extraction_script(df, base_dir)
    
    print("\n🎯 Next Steps:")
    print("1. Review the generated metadata in 2024_campaign_metadata.json")
    print("2. Run the extraction script: python3 extract_transcripts.py")
    print("3. Monitor extraction progress and handle any failures")
    print("4. Integrate successful transcripts into the main corpus")
    
    print(f"\n📊 Summary:")
    print(f"  Total speeches: {len(df)}")
    print(f"  Date range: {df['date_dt'].min().strftime('%Y-%m-%d')} to {df['date_dt'].max().strftime('%Y-%m-%d')}")
    print(f"  States covered: {len(df['state'].unique())}")
    print(f"  Campaign phases: {len(df['phase'].unique())}")

if __name__ == "__main__":
    main()
