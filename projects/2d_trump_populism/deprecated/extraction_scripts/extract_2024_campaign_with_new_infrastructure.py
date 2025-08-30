#!/usr/bin/env python3
"""
Trump 2024 Campaign Transcript Extraction
Using the new durable TranscriptExtractor infrastructure

This script extracts transcripts for all 74 speeches in the 2024 campaign corpus
using the standardized transcript extraction infrastructure.
"""

import json
import logging
import time
from pathlib import Path
from typing import List, Dict, Any

# Import the new durable infrastructure
from scripts.corpus_tools.transcript_extractor import TranscriptExtractor
from scripts.corpus_tools.extraction_result import ExtractionResult

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('extraction_log_new_infrastructure.txt'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class Trump2024Extractor:
    """Extract transcripts for Trump 2024 campaign speeches using new infrastructure."""
    
    def __init__(self, metadata_path: str, output_base_dir: str):
        self.metadata_path = Path(metadata_path)
        self.output_base_dir = Path(output_base_dir)
        self.metadata = self._load_metadata()
        
        # Initialize the new transcript extractor
        self.extractor = TranscriptExtractor(
            prefer_method="whisper",  # Standardized on Whisper for reliability
            whisper_model="small",    # Best quality/speed balance
            rate_limit=10,           # 10 second delay between requests
            retry_attempts=3,
            output_format="both"     # Both transcript and metadata
        )
        
        # Track progress
        self.success_count = 0
        self.failure_count = 0
        self.skipped_count = 0
        
    def _load_metadata(self) -> List[Dict[str, Any]]:
        """Load the 2024 campaign metadata."""
        try:
            with open(self.metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            logger.info(f"Loaded metadata for {len(metadata)} speeches")
            return metadata
        except Exception as e:
            logger.error(f"Failed to load metadata: {e}")
            raise
    
    def _get_output_dir(self, speech: Dict[str, Any]) -> Path:
        """Determine output directory based on campaign phase."""
        campaign_phase = speech.get('campaign_phase', 'unknown')
        phase_dir = self.output_base_dir / campaign_phase
        phase_dir.mkdir(parents=True, exist_ok=True)
        return phase_dir
    
    def _should_skip_speech(self, speech: Dict[str, Any]) -> bool:
        """Check if speech should be skipped (already processed)."""
        file_path = Path(speech['file_path'])
        if file_path.exists() and file_path.stat().st_size > 1000:  # More than 1KB
            return True
        return False
    
    def extract_single_speech(self, speech: Dict[str, Any]) -> bool:
        """Extract transcript for a single speech."""
        speech_id = speech['document_id']
        youtube_url = speech['youtube_url']
        
        logger.info(f"Processing {speech_id}")
        
        # Check if already processed
        if self._should_skip_speech(speech):
            logger.info(f"Skipping {speech_id} - already processed")
            self.skipped_count += 1
            return True
        
        # Determine output directory
        output_dir = self._get_output_dir(speech)
        
        try:
            # Extract transcript using new infrastructure
            result: ExtractionResult = self.extractor.extract_from_url(
                url=youtube_url,
                output_dir=output_dir,
                languages=["en"],
                experiment_context="trump_2024_campaign"
            )
            
            if result.success:
                logger.info(f"✅ Successfully extracted {speech_id}")
                logger.info(f"   Method: {result.method}")
                logger.info(f"   Confidence: {result.confidence:.1f}%")
                logger.info(f"   Transcript length: {result.transcript_length:,} chars")
                self.success_count += 1
                return True
            else:
                logger.error(f"❌ Failed to extract {speech_id}")
                logger.error(f"   Error: {result.error_message}")
                logger.error(f"   Error type: {result.error_type}")
                self.failure_count += 1
                return False
                
        except Exception as e:
            logger.error(f"❌ Exception processing {speech_id}: {e}")
            self.failure_count += 1
            return False
    
    def extract_all_speeches(self) -> None:
        """Extract transcripts for all speeches."""
        total_speeches = len(self.metadata)
        logger.info(f"🎯 Starting extraction of {total_speeches} speeches")
        logger.info(f"Output directory: {self.output_base_dir}")
        logger.info(f"Using Whisper model: {self.extractor.whisper_model}")
        
        start_time = time.time()
        
        for i, speech in enumerate(self.metadata, 1):
            logger.info(f"Progress: {i}/{total_speeches} ({(i/total_speeches)*100:.1f}%)")
            
            success = self.extract_single_speech(speech)
            
            # Add delay between extractions to be respectful
            if i < total_speeches:  # Don't delay after the last one
                time.sleep(5)  # 5 second delay between extractions
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Log final statistics
        logger.info("=" * 60)
        logger.info("🎉 EXTRACTION COMPLETE")
        logger.info("=" * 60)
        logger.info(f"Total speeches: {total_speeches}")
        logger.info(f"Successful: {self.success_count}")
        logger.info(f"Failed: {self.failure_count}")
        logger.info(f"Skipped (already processed): {self.skipped_count}")
        logger.info(f"Success rate: {(self.success_count/total_speeches)*100:.1f}%")
        logger.info(f"Total time: {total_time/60:.1f} minutes")
        logger.info(f"Average time per speech: {total_time/total_speeches:.1f} seconds")
        
        # Save summary statistics
        summary = {
            "extraction_summary": {
                "total_speeches": total_speeches,
                "successful": self.success_count,
                "failed": self.failure_count,
                "skipped": self.skipped_count,
                "success_rate": (self.success_count/total_speeches)*100,
                "total_time_minutes": total_time/60,
                "average_time_per_speech": total_time/total_speeches
            },
            "extraction_timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "whisper_model": self.extractor.whisper_model,
            "extraction_method": "new_durable_infrastructure"
        }
        
        summary_path = self.output_base_dir / "extraction_summary_new_infrastructure.json"
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Summary saved to: {summary_path}")

def main():
    """Main execution function."""
    # Paths
    metadata_path = "corpus/2024_campaign/2024_campaign_metadata.json"
    output_base_dir = "corpus/2024_campaign"
    
    # Verify paths exist
    if not Path(metadata_path).exists():
        logger.error(f"Metadata file not found: {metadata_path}")
        return
    
    # Create extractor and run extraction
    extractor = Trump2024Extractor(metadata_path, output_base_dir)
    extractor.extract_all_speeches()

if __name__ == "__main__":
    main()

