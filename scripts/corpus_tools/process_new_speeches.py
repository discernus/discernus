#!/usr/bin/env python3
"""
Process New Speeches - Targeted Processing
=========================================

This script processes the three new speeches added to tmp/new:
1. 1999-2000 campaign speeches (early political period)
2. 2024 campaign announcement (critical transition point)

Usage:
    python3 process_new_speeches.py --whisper-model base
"""

import argparse
import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

import whisper

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('new_speeches_processing.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class NewSpeechesProcessor:
    def __init__(self, whisper_model: str = "base"):
        self.whisper_model = whisper_model
        self.model = None
        
        # Define the new speeches and their metadata
        self.new_speeches = {
            "Donald Trump 2000 Presidential Race ｜ 7 Oct 1999.opus": {
                "period": "early_campaign",
                "date": "1999-10-07",
                "event_type": "Presidential Campaign Speech",
                "location": "Unknown",
                "context": "Trump's first presidential campaign attempt",
                "historical_significance": "Critical - First presidential campaign, early political positioning",
                "political_phase": "Early Political Period (1988-2000)",
                "campaign_cycle": "2000 Presidential Election",
                "speech_purpose": "Campaign announcement and positioning"
            },
            "Trump Campaign Speech 2000.opus": {
                "period": "early_campaign", 
                "date": "2000",
                "event_type": "Presidential Campaign Speech",
                "location": "Unknown",
                "context": "2000 presidential campaign",
                "historical_significance": "High - Early campaign rhetoric and messaging",
                "political_phase": "Early Political Period (1988-2000)",
                "campaign_cycle": "2000 Presidential Election",
                "speech_purpose": "Campaign rally or speech"
            },
            "Former President Donald Trump Announces 2024 Campaign | Election Rally from New Hampshire ｜ Streamed live on Apr 27, 2023.opus": {
                "period": "campaign_launch",
                "date": "2023-04-27",
                "event_type": "Campaign Announcement Rally",
                "location": "New Hampshire",
                "context": "Official announcement of 2024 presidential campaign",
                "historical_significance": "Critical - Campaign launch, transition from post-presidency to active campaigning",
                "political_phase": "Post-Presidency to Campaign (2021-2024)",
                "campaign_cycle": "2024 Presidential Election",
                "speech_purpose": "Campaign announcement and launch"
            }
        }
        
        # Define output directories for each period
        self.output_dirs = {
            "early_campaign": "projects/2d_trump_populism/corpus/first_campaign_1988_2000",
            "campaign_launch": "projects/2d_trump_populism/corpus/post_presidency_2021_2023"
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
    
    def get_file_metadata(self, filename: str) -> Dict[str, Any]:
        """Get comprehensive metadata for a specific file."""
        if filename not in self.new_speeches:
            logger.warning(f"No metadata found for {filename}, using defaults")
            return self._get_default_metadata(filename)
        
        speech_info = self.new_speeches[filename]
        base_metadata = {
            "filename": filename,
            "speaker": "Donald Trump",
            "category": "Political Speech",
            "extraction_method": "whisper",
            "whisper_model_used": self.whisper_model,
            "extracted_at": datetime.now().isoformat(),
            "source_format": "Audio file",
            "processing_notes": "Targeted processing of new speeches",
            "corpus_integration": "New content addition"
        }
        
        # Merge with specific speech metadata
        base_metadata.update(speech_info)
        return base_metadata
    
    def _get_default_metadata(self, filename: str) -> Dict[str, Any]:
        """Fallback metadata for unknown files."""
        return {
            "filename": filename,
            "speaker": "Donald Trump",
            "category": "Political Speech",
            "extraction_method": "whisper",
            "whisper_model_used": self.whisper_model,
            "extracted_at": datetime.now().isoformat(),
            "source_format": "Audio file",
            "processing_notes": "Targeted processing with default metadata",
            "corpus_integration": "New content addition"
        }
    
    def process_speech(self, audio_file: Path) -> Dict[str, Any]:
        """Process a single speech file."""
        logger.info(f"🎙️ Processing: {audio_file.name}")
        
        try:
            # Transcribe with Whisper
            result = self.model.transcribe(str(audio_file))
            
            # Get metadata
            metadata = self.get_file_metadata(audio_file.name)
            metadata.update({
                "transcript_length_chars": len(result["text"]),
                "language": result.get("language", "en"),
                "confidence_score": result.get("segments", [{}])[0].get("avg_logprob", 0) if result.get("segments") else 0,
                "audio_duration_seconds": result.get("segments", [{}])[-1].get("end", 0) if result.get("segments") else 0
            })
            
            # Determine output directory based on period
            period = metadata.get("period", "unknown")
            output_dir = Path(self.output_dirs.get(period, "projects/2d_trump_populism/corpus/unknown"))
            output_dir.mkdir(parents=True, exist_ok=True)
            (output_dir / "transcripts").mkdir(exist_ok=True)
            (output_dir / "metadata").mkdir(exist_ok=True)
            
            # Generate clean filename
            base_name = audio_file.stem.replace("｜", "_").replace("｜", "_").replace("｜", "_")
            base_name = base_name.replace(" ", "_").replace("：", "_")
            transcript_file = output_dir / "transcripts" / f"{base_name}.txt"
            metadata_file = output_dir / "metadata" / f"{base_name}_metadata.json"
            
            # Save transcript with comprehensive header
            with open(transcript_file, 'w', encoding='utf-8') as f:
                f.write(f"# {metadata.get('event_type', 'Political Speech')}\n")
                f.write(f"# Speaker: {metadata.get('speaker', 'Donald Trump')}\n")
                f.write(f"# Date: {metadata.get('date', 'Unknown')}\n")
                f.write(f"# Location: {metadata.get('location', 'Unknown')}\n")
                f.write(f"# Political Phase: {metadata.get('political_phase', 'Unknown')}\n")
                f.write(f"# Campaign Cycle: {metadata.get('campaign_cycle', 'Unknown')}\n")
                f.write(f"# Historical Significance: {metadata.get('historical_significance', 'Unknown')}\n")
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
            logger.info(f"   Output Directory: {output_dir}")
            
            return {
                "success": True,
                "transcript_file": str(transcript_file),
                "metadata_file": str(metadata_file),
                "metadata": metadata,
                "output_directory": str(output_dir)
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to process {audio_file.name}: {e}")
            return {
                "success": False,
                "error": str(e),
                "file": str(audio_file)
            }
    
    def process_all_new_speeches(self) -> Dict[str, Any]:
        """Process all new speeches in the tmp/new directory."""
        if not self.model:
            self.load_whisper_model()
        
        new_dir = Path("/Volumes/code/discernus/tmp/new")
        if not new_dir.exists():
            logger.error("❌ tmp/new directory not found")
            return {"success": False, "error": "tmp/new directory not found"}
        
        audio_files = list(new_dir.glob("*.opus")) + list(new_dir.glob("*.m4a")) + list(new_dir.glob("*.mp3"))
        
        if not audio_files:
            logger.warning("No audio files found in tmp/new directory")
            return {"success": False, "error": "No audio files found"}
        
        logger.info(f"🚀 Starting targeted processing of {len(audio_files)} new speeches...")
        
        results = []
        successful = 0
        failed = 0
        
        for i, audio_file in enumerate(audio_files, 1):
            logger.info(f"📁 Processing file {i}/{len(audio_files)}: {audio_file.name}")
            
            result = self.process_speech(audio_file)
            results.append(result)
            
            if result["success"]:
                successful += 1
            else:
                failed += 1
            
            logger.info(f"📊 Progress: {successful}/{len(audio_files)} successful, {failed} failed")
            
            # Small delay between files
            if i < len(audio_files):
                import time
                time.sleep(1)
        
        # Generate summary
        summary = {
            "total_files": len(audio_files),
            "successful": successful,
            "failed": failed,
            "success_rate": (successful / len(audio_files)) * 100 if audio_files else 0,
            "results": results,
            "processed_at": datetime.now().isoformat(),
            "whisper_model": self.whisper_model,
            "processing_type": "Targeted new speeches"
        }
        
        # Save summary
        summary_file = Path("new_speeches_summary.json")
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        logger.info(f"📊 Targeted processing complete: {successful}/{len(audio_files)} successful")
        logger.info(f"📄 Summary saved to: {summary_file}")
        
        return summary

def main():
    parser = argparse.ArgumentParser(description="Process new speeches from tmp/new directory")
    parser.add_argument("--whisper-model", default="base", choices=["tiny", "base", "small", "medium", "large"], 
                       help="Whisper model to use (default: base)")
    
    args = parser.parse_args()
    
    # Create processor and run
    processor = NewSpeechesProcessor(args.whisper_model)
    
    try:
        summary = processor.process_all_new_speeches()
        if summary["success"]:
            logger.info("🎉 All new speeches processed successfully!")
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

