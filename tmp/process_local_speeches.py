#!/usr/bin/env python3
"""
Process local speech files that were blocked on YouTube
"""

import whisper
import json
from pathlib import Path
from datetime import datetime
import re

def clean_title_for_filename(title):
    """Clean title for use in filename"""
    # Remove special characters and replace spaces with underscores
    clean = re.sub(r'[^\w\s-]', '', title)
    clean = re.sub(r'[-\s]+', '_', clean).strip('_')
    return clean

def process_speech_file(file_path, output_dir, speech_info):
    """Process a single speech file and save transcript + metadata"""
    
    print(f"🎯 Processing: {file_path}")
    
    # Load Whisper model
    print("📥 Loading Whisper model...")
    model = whisper.load_model('base')
    
    # Transcribe
    print("🎤 Transcribing with Whisper...")
    result = model.transcribe(str(file_path))
    
    # Extract text
    transcript_text = result['text']
    print(f"✅ Transcription complete: {len(transcript_text)} characters")
    
    # Generate filename
    title_clean = clean_title_for_filename(speech_info['title'])
    date_str = speech_info['date']
    filename = f"{title_clean}_{date_str}_whisper.txt"
    output_path = Path(output_dir) / filename
    
    # Save transcript
    print(f"📝 Saving transcript to: {output_path}")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"# {speech_info['title']}\n")
        f.write(f"# Date: {speech_info['date']}\n")
        f.write(f"# Venue: {speech_info['venue']}\n")
        f.write(f"# Method: Whisper (local file processing)\n")
        f.write(f"# Source: {file_path}\n")
        f.write(f"# Extracted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"# Transcript Length: {len(transcript_text)} characters\n")
        f.write(f"# Word Count: {len(transcript_text.split())}\n")
        f.write("\n" + "="*80 + "\n\n")
        f.write(transcript_text)
    
    # Save metadata
    metadata = {
        "document_id": f"trump_2024_{speech_info['date']}_{speech_info['state']}_local_whisper",
        "title": speech_info['title'],
        "speaker": "Donald Trump",
        "speaker_role": "presidential_candidate",
        "date": speech_info['date'],
        "venue": speech_info['venue'],
        "state": speech_info['state'],
        "category": "campaign_speech",
        "domain": "political",
        "language": "en",
        "country": "US",
        "audience_type": "campaign_rally",
        "formality_level": "informal",
        "rhetorical_style": ["campaign", "populist", "rally"],
        "campaign_phase": "general_election",
        "extraction_method": "whisper_local",
        "source_file": str(file_path),
        "transcript_length": len(transcript_text),
        "word_count": len(transcript_text.split()),
        "extraction_date": datetime.now().isoformat(),
        "notes": "Processed from local file due to YouTube access restrictions"
    }
    
    metadata_filename = f"{title_clean}_{date_str}_whisper_metadata.json"
    metadata_path = Path(output_dir) / metadata_filename
    
    print(f"📊 Saving metadata to: {metadata_path}")
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Successfully processed: {filename}")
    return filename

def main():
    # Speech information for the local files
    speeches = [
        {
            "file_path": "/Volumes/code/discernus/tmp/Donald Trump full speech at campaign rally in Wilkes-Barre PA Aug 17 2024.mp4",
            "title": "Donald Trump full speech at campaign rally in Wilkes-Barre PA",
            "date": "2024-08-17",
            "venue": "Campaign Rally in Wilkes-Barre, PA",
            "state": "PA"
        },
        {
            "file_path": "/Volumes/code/discernus/tmp/Speech 17 - North Carolina August 21 2024.mp4",
            "title": "Donald Trump campaign speech in North Carolina",
            "date": "2024-08-21",
            "venue": "Campaign Event in North Carolina",
            "state": "NC"
        }
    ]
    
    output_dir = "/Volumes/code/discernus/projects/2d_trump_populism/corpus/2024_campaign/primary_campaign"
    
    print(f"🎯 Processing {len(speeches)} local speech files...")
    print(f"📁 Output directory: {output_dir}")
    
    for speech in speeches:
        try:
            filename = process_speech_file(
                speech["file_path"], 
                output_dir, 
                speech
            )
            print(f"✅ Completed: {filename}\n")
        except Exception as e:
            print(f"❌ Failed to process {speech['file_path']}: {e}\n")
    
    print("🎉 All local speech processing complete!")

if __name__ == "__main__":
    main()
