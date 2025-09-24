#!/usr/bin/env python3
"""
Batch Process TMP Directory Audio Files
=======================================

This script processes all audio files in the /tmp directory and generates
high-quality transcripts using Whisper AI. Designed to run in the background
and handle all 10 identified audio files.

Usage:
    python3 batch_process_tmp_audio.py --output-dir /path/to/output --whisper-model base
"""

import argparse
import json
import logging
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

import whisper

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('tmp_audio_processing.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class TMPAudioProcessor:
    def __init__(self, output_dir: Path, whisper_model: str = "base"):
        self.tmp_dir = Path("/Volumes/code/discernus/tmp")
        self.output_dir = Path(output_dir)
        self.whisper_model = whisper_model
        self.model = None
        
        # Create output directories
        self.output_dir.mkdir(parents=True, exist_ok=True)
        (self.output_dir / "transcripts").mkdir(exist_ok=True)
        (self.output_dir / "metadata").mkdir(exist_ok=True)
        (self.output_dir / "logs").mkdir(exist_ok=True)
        
        # Define expected files and their metadata
        self.expected_files = {
            "President Trump full speech January 6th, 2021.opus": {
                "date": "2021-01-06",
                "event_type": "Political Rally",
                "location": "The Ellipse, Washington, DC",
                "context": "January 6th rally preceding Capitol attack",
                "historical_significance": "Critical - Preceded historic events"
            },
            "President Trump CPAC 2021 Full Speech I NewsNOW from FOX.m4a": {
                "date": "2021-03-01",
                "event_type": "CPAC Speech",
                "location": "Conservative Political Action Conference",
                "context": "First major post-presidency speech",
                "historical_significance": "High - First post-presidency appearance"
            },
            "Speech： Donald Trump Holds a Political Rally in Youngstown, Ohio - September 17, 2022.opus": {
                "date": "2022-09-17",
                "event_type": "Campaign Rally",
                "location": "Youngstown, Ohio",
                "context": "2022 midterm election campaign",
                "historical_significance": "Medium - Campaign rally"
            },
            "Speech： Donald Trump Holds a Political Rally in Delaware, Ohio - April 23, 2022.opus": {
                "date": "2022-04-23",
                "event_type": "Campaign Rally",
                "location": "Delaware, Ohio",
                "context": "2022 midterm election campaign",
                "historical_significance": "Medium - Campaign rally"
            },
            "Speech： Donald Trump Delivers a Speech at the 2022 CPAC Convention in Dallas - August 6, 2022.opus": {
                "date": "2022-08-06",
                "event_type": "CPAC Speech",
                "location": "CPAC Convention, Dallas, Texas",
                "context": "2022 CPAC convention speech",
                "historical_significance": "Medium - CPAC appearance"
            },
            "Speech： Donald Trump Holds a Political Rally in Dayton, Ohio - November 7, 2022.opus": {
                "date": "2022-11-07",
                "event_type": "Campaign Rally",
                "location": "Dayton, Ohio",
                "context": "2022 midterm election campaign",
                "historical_significance": "High - Pre-election rally"
            },
            "LIVE： President Donald J. Trump to hold a rally in Hialeah, Florida - 11⧸8⧸23.opus": {
                "date": "2023-11-08",
                "event_type": "Campaign Rally",
                "location": "Hialeah, Florida",
                "context": "2024 presidential campaign rally",
                "historical_significance": "Medium - Campaign rally"
            },
            "FULL SPEECH： Former President Donald Trump speaks at 'Save America' rally in Conroe, Texas.opus": {
                "date": "2024",
                "event_type": "Save America Rally",
                "location": "Conroe, Texas",
                "context": "2024 presidential campaign",
                "historical_significance": "Medium - Campaign rally"
            },
            "LIVE： Trump Delivers Remarks at the 'Save America Rally' in Washington, D.C..opus": {
                "date": "2024",
                "event_type": "Save America Rally",
                "location": "Washington, D.C.",
                "context": "2024 presidential campaign",
                "historical_significance": "Medium - Campaign rally"
            },
            "Full Trump Interview： 'I don't consider us to have much of a democracy right now'.m4a": {
                "date": "2024",
                "event_type": "Interview",
                "location": "Unknown",
                "context": "Media interview",
                "historical_significance": "Medium - Policy interview"
            }
        }
        
    def load_whisper_model(self):
        """Load the specified Whisper model."""
        logger.info(f"Loading Whisper model: {self.whisper_model}")
        try:
            self.model = whisper.load_model(self.whisper_model)
            logger.info(f"✅ Whisper {self.whisper_model} model loaded successfully")
        except Exception as e:
            logger.error(f"❌ Failed to load Whisper model: {e}")
            raise
    
    def get_audio_files(self) -> List[Path]:
        """Get all audio files from tmp directory."""
        audio_extensions = {'.mp3', '.wav', '.m4a', '.flac', '.aac', '.ogg', '.opus'}
        audio_files = []
        
        for file_path in self.tmp_dir.glob('*'):
            if file_path.is_file() and file_path.suffix.lower() in audio_extensions:
                audio_files.append(file_path)
        
        logger.info(f"Found {len(audio_files)} audio files in tmp directory")
        return audio_files
    
    def get_file_metadata(self, filename: str) -> Dict[str, Any]:
        """Get metadata for a specific file."""
        base_metadata = {
            "speaker": "Donald Trump",
            "category": "Political Speech",
            "extraction_method": "whisper",
            "whisper_model_used": self.whisper_model,
            "extracted_at": datetime.now().isoformat(),
            "source_format": "Audio file",
            "processing_notes": "Batch processed from tmp directory"
        }
        
        # Get specific metadata if available
        if filename in self.expected_files:
            base_metadata.update(self.expected_files[filename])
        
        return base_metadata
    
    def process_audio_file(self, audio_file: Path) -> Dict[str, Any]:
        """Process a single audio file with Whisper."""
        logger.info(f"🎙️ Processing: {audio_file.name}")
        
        try:
            # Transcribe with Whisper
            result = self.model.transcribe(str(audio_file))
            
            # Get metadata
            metadata = self.get_file_metadata(audio_file.name)
            metadata.update({
                "filename": audio_file.name,
                "transcript_length_chars": len(result["text"]),
                "language": result.get("language", "en"),
                "confidence_score": result.get("segments", [{}])[0].get("avg_logprob", 0) if result.get("segments") else 0,
                "audio_duration_seconds": result.get("segments", [{}])[-1].get("end", 0) if result.get("segments") else 0
            })
            
            # Generate output filename
            base_name = audio_file.stem.replace("：", "_").replace("：", "_").replace("⧸", "_")
            transcript_file = self.output_dir / "transcripts" / f"{base_name}.txt"
            metadata_file = self.output_dir / "metadata" / f"{base_name}_metadata.json"
            
            # Save transcript
            with open(transcript_file, 'w', encoding='utf-8') as f:
                f.write(f"# {metadata.get('title', audio_file.name)}\n")
                f.write(f"# Date: {metadata.get('date', 'Unknown')}\n")
                f.write(f"# Location: {metadata.get('location', 'Unknown')}\n")
                f.write(f"# Event: {metadata.get('event_type', 'Unknown')}\n")
                f.write(f"# Duration: {metadata.get('audio_duration_seconds', 0):.1f} seconds\n")
                f.write(f"# Source: {audio_file.name}\n")
                f.write(f"# Processed: {metadata['extracted_at']}\n")
                f.write("=" * 80 + "\n\n")
                f.write(result["text"])
            
            # Save metadata
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            
            logger.info(f"✅ Successfully processed: {audio_file.name}")
            logger.info(f"   Transcript: {transcript_file}")
            logger.info(f"   Metadata: {metadata_file}")
            
            return {
                "success": True,
                "transcript_file": str(transcript_file),
                "metadata_file": str(metadata_file),
                "metadata": metadata
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to process {audio_file.name}: {e}")
            return {
                "success": False,
                "error": str(e),
                "file": str(audio_file)
            }
    
    def process_all_files(self) -> Dict[str, Any]:
        """Process all audio files in the tmp directory."""
        if not self.model:
            self.load_whisper_model()
        
        audio_files = self.get_audio_files()
        if not audio_files:
            logger.warning("No audio files found in tmp directory")
            return {"success": False, "error": "No audio files found"}
        
        results = []
        successful = 0
        failed = 0
        
        logger.info(f"🚀 Starting batch processing of {len(audio_files)} files...")
        
        for i, audio_file in enumerate(audio_files, 1):
            logger.info(f"📁 Processing file {i}/{len(audio_files)}: {audio_file.name}")
            
            result = self.process_audio_file(audio_file)
            results.append(result)
            
            if result["success"]:
                successful += 1
            else:
                failed += 1
            
            # Progress update
            logger.info(f"📊 Progress: {successful}/{len(audio_files)} successful, {failed} failed")
            
            # Small delay between files to prevent overwhelming
            if i < len(audio_files):
                time.sleep(2)
        
        # Generate summary
        summary = {
            "total_files": len(audio_files),
            "successful": successful,
            "failed": failed,
            "success_rate": (successful / len(audio_files)) * 100 if audio_files else 0,
            "results": results,
            "processed_at": datetime.now().isoformat(),
            "whisper_model": self.whisper_model
        }
        
        # Save summary
        summary_file = self.output_dir / "logs" / "batch_processing_summary.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        logger.info(f"📊 Batch processing complete: {successful}/{len(audio_files)} successful")
        logger.info(f"📄 Summary saved to: {summary_file}")
        
        return summary

def main():
    parser = argparse.ArgumentParser(description="Batch process all audio files in tmp directory")
    parser.add_argument("--output-dir", required=True, help="Output directory for transcripts and metadata")
    parser.add_argument("--whisper-model", default="base", choices=["tiny", "base", "small", "medium", "large"], 
                       help="Whisper model to use (default: base)")
    
    args = parser.parse_args()
    
    # Create processor and run
    processor = TMPAudioProcessor(args.output_dir, args.whisper_model)
    
    try:
        summary = processor.process_all_files()
        if summary["success"]:
            logger.info("🎉 All files processed successfully!")
        else:
            logger.error(f"❌ Processing failed: {summary.get('error', 'Unknown error')}")
            sys.exit(1)
    except KeyboardInterrupt:
        logger.info("⏹️ Processing interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

