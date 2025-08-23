#!/usr/bin/env python3
"""
Comprehensive Corpus Processor
=============================

This script processes all 22 new audio files in the tmp directory, organizing them
by political period and generating rich metadata. This will dramatically improve
our corpus coverage from 1988-2025.

Usage:
    python3 comprehensive_corpus_processor.py --whisper-model base
"""

import argparse
import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

import whisper

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('comprehensive_processing.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ComprehensiveCorpusProcessor:
    def __init__(self, whisper_model: str = "base"):
        self.whisper_model = whisper_model
        self.model = None
        
        # Define comprehensive metadata for all new files
        self.speech_metadata = {
            # Early Political Period (1988-2000)
            "Donald Trump Teases a President Bid During a 1988 Oprah Show ｜ The Oprah Winfrey Show ｜ OWN.m4a": {
                "period": "early_political",
                "date": "1988",
                "event_type": "Television Interview",
                "location": "The Oprah Winfrey Show",
                "context": "First public mention of presidential ambitions",
                "historical_significance": "Critical - First presidential tease, early political positioning",
                "political_phase": "Early Political Period (1988-2000)",
                "speech_purpose": "Political positioning and presidential tease",
                "audience": "National television audience",
                "media_type": "Television interview"
            },
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
            
            # Pre-Campaign Period (2011-2015)
            "Donald Trump  CPAC 2011.opus": {
                "period": "pre_campaign",
                "date": "2011",
                "event_type": "CPAC Speech",
                "location": "Conservative Political Action Conference",
                "context": "Early political positioning before presidential run",
                "historical_significance": "High - Early CPAC appearance, political positioning",
                "political_phase": "Pre-Campaign Period (2011-2015)",
                "speech_purpose": "Political positioning and conservative outreach",
                "audience": "Conservative activists and leaders"
            },
            "CPAC 2013 - Donald Trump.opus": {
                "period": "pre_campaign",
                "date": "2013",
                "event_type": "CPAC Speech",
                "location": "Conservative Political Action Conference",
                "context": "Continued political positioning",
                "historical_significance": "Medium - Continued political positioning",
                "political_phase": "Pre-Campaign Period (2011-2015)",
                "speech_purpose": "Political positioning and conservative outreach"
            },
            "CPAC 2014 - Donald Trump, The Trump Organization.opus": {
                "period": "pre_campaign",
                "date": "2014",
                "event_type": "CPAC Speech",
                "location": "Conservative Political Action Conference",
                "context": "Final pre-campaign positioning",
                "historical_significance": "Medium - Final pre-campaign positioning",
                "political_phase": "Pre-Campaign Period (2011-2015)",
                "speech_purpose": "Political positioning and conservative outreach"
            },
            "Donald Trump CPAC 2015 Full Speech Donald trump president.m4a": {
                "period": "campaign_launch",
                "date": "2015",
                "event_type": "CPAC Speech",
                "location": "Conservative Political Action Conference",
                "context": "Campaign launch period",
                "historical_significance": "High - Campaign launch period CPAC",
                "political_phase": "Campaign Launch Period (2015-2016)",
                "speech_purpose": "Campaign positioning and conservative outreach"
            },
            
            # Presidential Period (2017-2020)
            "Trump's full speech at CPAC 2017.opus": {
                "period": "presidential",
                "date": "2017",
                "event_type": "CPAC Speech",
                "location": "Conservative Political Action Conference",
                "context": "First CPAC as president",
                "historical_significance": "Critical - First CPAC as president, presidential messaging",
                "political_phase": "Presidential Period (2017-2020)",
                "speech_purpose": "Presidential policy and messaging",
                "presidential_context": "First year in office"
            },
            "CPAC 2018 - President Donald Trump.opus": {
                "period": "presidential",
                "date": "2018",
                "event_type": "CPAC Speech",
                "location": "Conservative Political Action Conference",
                "context": "Second CPAC as president",
                "historical_significance": "High - Second CPAC as president",
                "political_phase": "Presidential Period (2017-2020)",
                "speech_purpose": "Presidential policy and messaging",
                "presidential_context": "Second year in office"
            },
            "Speech： Donald Trump Delivers a Speech at the 2020 CPAC Convention in Orlando - February 28, 2021.opus": {
                "period": "presidential",
                "date": "2021-02-28",
                "event_type": "CPAC Speech",
                "location": "CPAC Convention, Orlando, Florida",
                "context": "Final CPAC as president (post-election)",
                "historical_significance": "Critical - Final CPAC as president, post-election messaging",
                "political_phase": "Presidential Period (2017-2020)",
                "speech_purpose": "Post-election messaging and policy",
                "presidential_context": "Post-election period"
            },
            "URGENT 🔴 President Trump EXPLOSIVE Speech at CPAC 2020.m4a": {
                "period": "presidential",
                "date": "2020",
                "event_type": "CPAC Speech",
                "location": "Conservative Political Action Conference",
                "context": "Fourth CPAC as president",
                "historical_significance": "High - Fourth CPAC as president",
                "political_phase": "Presidential Period (2017-2020)",
                "speech_purpose": "Presidential policy and messaging",
                "presidential_context": "Fourth year in office"
            },
            "CPAC 2020 - President Donald J. Trump.m4a": {
                "period": "presidential",
                "date": "2020",
                "event_type": "CPAC Speech",
                "location": "Conservative Political Action Conference",
                "context": "Fourth CPAC as president (alternative source)",
                "historical_significance": "High - Fourth CPAC as president",
                "political_phase": "Presidential Period (2017-2020)",
                "speech_purpose": "Presidential policy and messaging",
                "presidential_context": "Fourth year in office"
            },
            
            # Post-Presidency Period (2021-2024)
            "President Trump CPAC 2021 Full Speech I NewsNOW from FOX.opus": {
                "period": "post_presidency",
                "date": "2021-03-01",
                "event_type": "CPAC Speech",
                "location": "Conservative Political Action Conference",
                "context": "First post-presidency CPAC",
                "historical_significance": "Critical - First post-presidency appearance",
                "political_phase": "Post-Presidency Period (2021-2024)",
                "speech_purpose": "Post-presidency positioning and messaging",
                "post_presidency_context": "First major post-presidency speech"
            },
            "Speech： Donald Trump Delivers a Speech at the 2022 CPAC Convention in Orlando - February 26, 2022.opus": {
                "period": "post_presidency",
                "date": "2022-02-26",
                "event_type": "CPAC Speech",
                "location": "CPAC Convention, Orlando, Florida",
                "context": "Second post-presidency CPAC",
                "historical_significance": "High - Second post-presidency CPAC",
                "political_phase": "Post-Presidency Period (2021-2024)",
                "speech_purpose": "Post-presidency positioning and messaging",
                "post_presidency_context": "Second post-presidency CPAC"
            },
            "PRESIDENT DONALD J. TRUMP DELIVERS REMARKS AT CPAC 2023.opus": {
                "period": "post_presidency",
                "date": "2023",
                "event_type": "CPAC Speech",
                "location": "Conservative Political Action Conference",
                "context": "Third post-presidency CPAC",
                "historical_significance": "High - Third post-presidency CPAC",
                "political_phase": "Post-Presidency Period (2021-2024)",
                "speech_purpose": "Post-presidency positioning and messaging",
                "post_presidency_context": "Third post-presidency CPAC"
            },
            "CPAC 2024 LIVE ｜ Former President Trump Speaks LIVE at CPAC ｜ Donald Trump Speech Live ｜ News18 Live.opus": {
                "period": "post_presidency",
                "date": "2024",
                "event_type": "CPAC Speech",
                "location": "Conservative Political Action Conference",
                "context": "Fourth post-presidency CPAC",
                "historical_significance": "High - Fourth post-presidency CPAC",
                "political_phase": "Post-Presidency Period (2021-2024)",
                "speech_purpose": "Post-presidency positioning and messaging",
                "post_presidency_context": "Fourth post-presidency CPAC"
            },
            "President Donald J. Trump at CPAC DC 2025 – Day 3 (Part 2).m4a": {
                "period": "post_presidency",
                "date": "2025",
                "event_type": "CPAC Speech",
                "location": "Conservative Political Action Conference, Washington DC",
                "context": "Fifth post-presidency CPAC",
                "historical_significance": "High - Fifth post-presidency CPAC",
                "political_phase": "Post-Presidency Period (2021-2024)",
                "speech_purpose": "Post-presidency positioning and messaging",
                "post_presidency_context": "Fifth post-presidency CPAC"
            },
            
            # Recent Campaign Content (2024)
            "FULL SPEECH： President Trump speaks at CPAC  ｜ LiveNOW from FOX.m4a": {
                "period": "recent_campaign",
                "date": "2024",
                "event_type": "CPAC Speech",
                "location": "Conservative Political Action Conference",
                "context": "Recent CPAC appearance",
                "historical_significance": "Medium - Recent CPAC appearance",
                "political_phase": "Recent Campaign Period (2024-2025)",
                "speech_purpose": "Campaign messaging and positioning"
            }
        }
        
        # Define output directories for each period
        self.output_dirs = {
            "early_political": "projects/2d_trump_populism/corpus/first_campaign_1988_2000",
            "early_campaign": "projects/2d_trump_populism/corpus/first_campaign_1988_2000",
            "pre_campaign": "projects/2d_trump_populism/corpus/first_campaign_1988_2000",
            "campaign_launch": "projects/2d_trump_populism/corpus/campaign_2015_2016",
            "presidential": "projects/2d_trump_populism/corpus/presidential_2017_2020",
            "post_presidency": "projects/2d_trump_populism/corpus/post_presidency_2021_2023",
            "recent_campaign": "projects/2d_trump_populism/corpus/post_presidency_2021_2023"
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
        if filename in self.speech_metadata:
            speech_info = self.speech_metadata[filename]
        else:
            logger.warning(f"No metadata found for {filename}, using defaults")
            speech_info = self._get_default_metadata(filename)
        
        base_metadata = {
            "filename": filename,
            "speaker": "Donald Trump",
            "category": "Political Speech",
            "extraction_method": "whisper",
            "whisper_model_used": self.whisper_model,
            "extracted_at": datetime.now().isoformat(),
            "source_format": "Audio file",
            "processing_notes": "Comprehensive corpus processing",
            "corpus_integration": "Major corpus enhancement"
        }
        
        # Merge with specific speech metadata
        base_metadata.update(speech_info)
        return base_metadata
    
    def _get_default_metadata(self, filename: str) -> Dict[str, Any]:
        """Fallback metadata for unknown files."""
        return {
            "period": "unknown",
            "date": "Unknown",
            "event_type": "Political Speech",
            "location": "Unknown",
            "context": "Unknown",
            "historical_significance": "Unknown",
            "political_phase": "Unknown",
            "speech_purpose": "Unknown"
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
            base_name = base_name.replace("：", "_").replace(" ", "_").replace("🔴", "")
            base_name = base_name.replace("(", "").replace(")", "").replace("-", "_")
            transcript_file = output_dir / "transcripts" / f"{base_name}.txt"
            metadata_file = output_dir / "metadata" / f"{base_name}_metadata.json"
            
            # Save transcript with comprehensive header
            with open(transcript_file, 'w', encoding='utf-8') as f:
                f.write(f"# {metadata.get('event_type', 'Political Speech')}\n")
                f.write(f"# Speaker: {metadata.get('speaker', 'Donald Trump')}\n")
                f.write(f"# Date: {metadata.get('date', 'Unknown')}\n")
                f.write(f"# Location: {metadata.get('location', 'Unknown')}\n")
                f.write(f"# Political Phase: {metadata.get('political_phase', 'Unknown')}\n")
                f.write(f"# Historical Significance: {metadata.get('historical_significance', 'Unknown')}\n")
                f.write(f"# Speech Purpose: {metadata.get('speech_purpose', 'Unknown')}\n")
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
    
    def get_unprocessed_files(self) -> List[Path]:
        """Get all unprocessed audio files from tmp directory."""
        tmp_dir = Path("/Volumes/code/discernus/tmp")
        processed_dir = tmp_dir / "processed"
        
        # Get all audio files in tmp
        audio_extensions = {'.mp3', '.wav', '.m4a', '.flac', '.aac', '.ogg', '.opus', '.mp4'}
        all_audio = []
        for ext in audio_extensions:
            all_audio.extend(tmp_dir.glob(f"*{ext}"))
        
        # Get processed files
        processed_files = set()
        if processed_dir.exists():
            for ext in audio_extensions:
                processed_files.update(f.name for f in processed_dir.glob(f"*{ext}"))
        
        # Filter out processed files
        unprocessed = [f for f in all_audio if f.name not in processed_files]
        
        logger.info(f"Found {len(all_audio)} total audio files")
        logger.info(f"Found {len(processed_files)} processed files")
        logger.info(f"Found {len(unprocessed)} unprocessed files")
        
        return unprocessed
    
    def process_all_unprocessed(self) -> Dict[str, Any]:
        """Process all unprocessed audio files."""
        if not self.model:
            self.load_whisper_model()
        
        unprocessed_files = self.get_unprocessed_files()
        if not unprocessed_files:
            logger.warning("No unprocessed files found")
            return {"success": False, "error": "No unprocessed files found"}
        
        logger.info(f"🚀 Starting comprehensive processing of {len(unprocessed_files)} unprocessed files...")
        
        results = []
        successful = 0
        failed = 0
        
        for i, audio_file in enumerate(unprocessed_files, 1):
            logger.info(f"📁 Processing file {i}/{len(unprocessed_files)}: {audio_file.name}")
            
            result = self.process_speech(audio_file)
            results.append(result)
            
            if result["success"]:
                successful += 1
            else:
                failed += 1
            
            logger.info(f"📊 Progress: {successful}/{len(unprocessed_files)} successful, {failed} failed")
            
            # Small delay between files
            if i < len(unprocessed_files):
                import time
                time.sleep(1)
        
        # Generate summary
        summary = {
            "total_files": len(unprocessed_files),
            "successful": successful,
            "failed": failed,
            "success_rate": (successful / len(unprocessed_files)) * 100 if unprocessed_files else 0,
            "results": results,
            "processed_at": datetime.now().isoformat(),
            "whisper_model": self.whisper_model,
            "processing_type": "Comprehensive corpus enhancement"
        }
        
        # Save summary
        summary_file = Path("comprehensive_processing_summary.json")
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        logger.info(f"📊 Comprehensive processing complete: {successful}/{len(unprocessed_files)} successful")
        logger.info(f"📄 Summary saved to: {summary_file}")
        
        return summary

def main():
    parser = argparse.ArgumentParser(description="Comprehensive processing of all unprocessed audio files")
    parser.add_argument("--whisper-model", default="base", choices=["tiny", "base", "small", "medium", "large"], 
                       help="Whisper model to use (default: base)")
    
    args = parser.parse_args()
    
    # Create processor and run
    processor = ComprehensiveCorpusProcessor(args.whisper_model)
    
    try:
        summary = processor.process_all_unprocessed()
        if summary["success"]:
            logger.info("🎉 All unprocessed files processed successfully!")
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

