#!/usr/bin/env python3
"""
Process the August 14 North Carolina speech from the misnamed file
"""

import whisper
import json
from pathlib import Path
from datetime import datetime

def main():
    # Speech information - this is actually August 14, not August 21
    speech_info = {
        "file_path": "/Volumes/code/discernus/tmp/Speech 17 - North Carolina August 21 2024.mp4",
        "title": "Donald Trump campaign speech in North Carolina",
        "date": "2024-08-14",  # Corrected date
        "venue": "Campaign Event in North Carolina",
        "state": "NC"
    }
    
    output_dir = "/Volumes/code/discernus/projects/2d_trump_populism/corpus/2024_campaign/primary_campaign"
    
    print(f"🎯 Processing: {speech_info['file_path']}")
    print(f"📅 Corrected date: {speech_info['date']}")
    
    # Load Whisper model
    print("📥 Loading Whisper model...")
    model = whisper.load_model('base')
    
    # Transcribe
    print("🎤 Transcribing with Whisper...")
    result = model.transcribe(speech_info['file_path'])
    
    # Extract text
    transcript_text = result['text']
    print(f"✅ Transcription complete: {len(transcript_text)} characters")
    
    # Generate filename with correct date
    title_clean = "Donald_Trump_campaign_speech_in_North_Carolina"
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
        f.write(f"# Source: {speech_info['file_path']}\n")
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
        "source_file": str(speech_info['file_path']),
        "transcript_length": len(transcript_text),
        "word_count": len(transcript_text.split()),
        "extraction_date": datetime.now().isoformat(),
        "notes": "Processed from local file due to YouTube access restrictions. Note: File was misnamed as 'August 21' but is actually August 14 speech."
    }
    
    metadata_filename = f"{title_clean}_{date_str}_whisper_metadata.json"
    metadata_path = Path(output_dir) / metadata_filename
    
    print(f"📊 Saving metadata to: {metadata_path}")
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Successfully processed: {filename}")

if __name__ == "__main__":
    main()
