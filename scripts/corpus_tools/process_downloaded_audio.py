#!/usr/bin/env python3
"""
Process Downloaded Audio Files with Whisper Transcription
=======================================================

This script processes manually downloaded YouTube audio files and generates
high-quality transcripts using Whisper AI. Designed to work around YouTube's
anti-scraping measures by processing pre-downloaded audio files.

Usage:
    python3 process_downloaded_audio.py --input-dir /path/to/audio/files --output-dir /path/to/transcripts
"""

import argparse
import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

import whisper

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AudioProcessor:
    def __init__(self, input_dir: Path, output_dir: Path, whisper_model: str = "base"):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.whisper_model = whisper_model
        self.model = None
        
        # Create output directories
        self.output_dir.mkdir(parents=True, exist_ok=True)
        (self.output_dir / "transcripts").mkdir(exist_ok=True)
        (self.output_dir / "metadata").mkdir(exist_ok=True)
        
    def load_whisper_model(self):
        """Load the specified Whisper model."""
        logger.info(f"Loading Whisper model: {self.whisper_model}")
        try:
            self.model = whisper.load_model(self.whisper_model)
            logger.info(f"✅ Whisper {self.whisper_model} model loaded successfully")
        except Exception as e:
            logger.error(f"❌ Failed to load Whisper model: {e}")
            raise
    
    def get_audio_files(self) -> list[Path]:
        """Get all audio files from input directory."""
        audio_extensions = {'.mp3', '.wav', '.m4a', '.flac', '.aac', '.ogg', '.opus'}
        audio_files = []
        
        for file_path in self.input_dir.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in audio_extensions:
                audio_files.append(file_path)
        
        logger.info(f"Found {len(audio_files)} audio files")
        return audio_files
    
    def extract_metadata_from_filename(self, filename: str) -> Dict[str, Any]:
        """Extract metadata from filename patterns."""
        # Common patterns for Trump speech filenames
        filename_lower = filename.lower()
        
        metadata = {
            "speaker": "Donald Trump",
            "category": "Political Speech",
            "extraction_method": "whisper",
            "whisper_model_used": self.whisper_model,
            "extracted_at": datetime.now().isoformat()
        }
        
        # Try to extract date patterns
        if "2021" in filename:
            metadata["date"] = "2021"
        elif "2022" in filename:
            metadata["date"] = "2022"
        elif "2023" in filename:
            metadata["date"] = "2023"
        elif "2024" in filename:
            metadata["date"] = "2024"
        
        # Try to extract event/location patterns
        if "cpac" in filename_lower:
            metadata["event_type"] = "CPAC Speech"
            metadata["location"] = "Conservative Political Action Conference"
        elif "rally" in filename_lower:
            metadata["event_type"] = "Campaign Rally"
        elif "ellipse" in filename_lower or "january 6" in filename_lower:
            metadata["event_type"] = "Political Rally"
            metadata["location"] = "The Ellipse, Washington, DC"
            metadata["date"] = "2021-01-06"
        
        return metadata
    
    def process_audio_file(self, audio_file: Path) -> Dict[str, Any]:
        """Process a single audio file with Whisper."""
        logger.info(f"🎙️ Processing: {audio_file.name}")
        
        try:
            # Transcribe with Whisper
            result = self.model.transcribe(str(audio_file))
            
            # Extract metadata
            metadata = self.extract_metadata_from_filename(audio_file.name)
            metadata.update({
                "filename": audio_file.name,
                "transcript_length_chars": len(result["text"]),
                "language": result.get("language", "en"),
                "confidence_score": result.get("segments", [{}])[0].get("avg_logprob", 0) if result.get("segments") else 0
            })
            
            # Generate output filename
            base_name = audio_file.stem
            transcript_file = self.output_dir / "transcripts" / f"{base_name}.txt"
            metadata_file = self.output_dir / "metadata" / f"{base_name}_metadata.json"
            
            # Save transcript
            with open(transcript_file, 'w', encoding='utf-8') as f:
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
        """Process all audio files in the input directory."""
        if not self.model:
            self.load_whisper_model()
        
        audio_files = self.get_audio_files()
        if not audio_files:
            logger.warning("No audio files found in input directory")
            return {"success": False, "error": "No audio files found"}
        
        results = []
        successful = 0
        failed = 0
        
        for audio_file in audio_files:
            result = self.process_audio_file(audio_file)
            results.append(result)
            
            if result["success"]:
                successful += 1
            else:
                failed += 1
        
        # Generate summary
        summary = {
            "total_files": len(audio_files),
            "successful": successful,
            "failed": failed,
            "success_rate": (successful / len(audio_files)) * 100 if audio_files else 0,
            "results": results,
            "processed_at": datetime.now().isoformat()
        }
        
        # Save summary
        summary_file = self.output_dir / "processing_summary.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        logger.info(f"📊 Processing complete: {successful}/{len(audio_files)} successful")
        logger.info(f"📄 Summary saved to: {summary_file}")
        
        return summary

def main():
    parser = argparse.ArgumentParser(description="Process downloaded audio files with Whisper")
    parser.add_argument("--input-dir", required=True, help="Directory containing audio files")
    parser.add_argument("--output-dir", required=True, help="Output directory for transcripts and metadata")
    parser.add_argument("--whisper-model", default="base", choices=["tiny", "base", "small", "medium", "large"], 
                       help="Whisper model to use (default: base)")
    
    args = parser.parse_args()
    
    # Validate input directory
    input_dir = Path(args.input_dir)
    if not input_dir.exists():
        logger.error(f"Input directory does not exist: {input_dir}")
        sys.exit(1)
    
    # Create processor and run
    processor = AudioProcessor(input_dir, args.output_dir, args.whisper_model)
    
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

