#!/usr/bin/env python3
"""
Efficient Trump 2024 Campaign Transcript Extraction
Processes speeches in small batches to avoid resource issues.

This script extracts transcripts for remaining 2024 campaign speeches
using the new durable infrastructure, with batch processing and
robust error handling.
"""

import json
import logging
import time
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional

# Add the scripts directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))

from corpus_tools.transcript_extractor import TranscriptExtractor
from corpus_tools.extraction_result import ExtractionResult

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('extraction_log_efficient.txt'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class EfficientTrump2024Extractor:
    """Extract transcripts for Trump 2024 campaign speeches efficiently."""
    
    def __init__(self, metadata_path: str, output_base_dir: str, batch_size: int = 5):
        self.metadata_path = Path(metadata_path)
        self.output_base_dir = Path(output_base_dir)
        self.batch_size = batch_size
        self.metadata = self._load_metadata()
        
        # Initialize the transcript extractor with small model for efficiency
        self.extractor = TranscriptExtractor(
            prefer_method="whisper",  # Standardized on Whisper for reliability
            whisper_model="tiny",     # Use tiny for speed and stability
            rate_limit=15,           # 15 second delay between requests
            retry_attempts=2,        # Fewer retries for efficiency
            output_format="both"     # Both transcript and metadata
        )
        
        # Track progress
        self.success_count = 0
        self.failure_count = 0
        self.skipped_count = 0
        self.current_batch = 0
        
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
    
    def _get_pending_speeches(self) -> List[Dict[str, Any]]:
        """Get list of speeches that still need processing."""
        pending = []
        for speech in self.metadata:
            if not self._should_skip_speech(speech):
                pending.append(speech)
        return pending
    
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
                experiment_context="trump_2024_campaign_efficient"
            )
            
            if result.success:
                logger.info(f"✅ Successfully extracted {speech_id}")
                logger.info(f"   Method: {result.method}")
                logger.info(f"   Confidence: {result.confidence:.1f}%")
                logger.info(f"   Transcript length: {result.quality_metrics.transcript_length:,} chars")
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
    
    def extract_batch(self, batch: List[Dict[str, Any]]) -> None:
        """Extract transcripts for a batch of speeches."""
        self.current_batch += 1
        logger.info(f"🎯 Processing Batch {self.current_batch} ({len(batch)} speeches)")
        
        batch_start_time = time.time()
        batch_success = 0
        batch_failure = 0
        
        for i, speech in enumerate(batch, 1):
            logger.info(f"   Progress: {i}/{len(batch)} ({(i/len(batch))*100:.1f}%)")
            
            success = self.extract_single_speech(speech)
            if success:
                batch_success += 1
            else:
                batch_failure += 1
            
            # Add delay between extractions to be respectful
            if i < len(batch):  # Don't delay after the last one
                time.sleep(10)  # 10 second delay between extractions
        
        batch_time = time.time() - batch_start_time
        logger.info(f"📊 Batch {self.current_batch} Complete:")
        logger.info(f"   Successful: {batch_success}")
        logger.info(f"   Failed: {batch_failure}")
        logger.info(f"   Time: {batch_time/60:.1f} minutes")
        logger.info(f"   Average: {batch_time/len(batch):.1f} seconds per speech")
        
        # Save batch summary
        self._save_batch_summary(batch, batch_success, batch_failure, batch_time)
    
    def _save_batch_summary(self, batch: List[Dict[str, Any]], success: int, failure: int, time_taken: float):
        """Save summary for the current batch."""
        batch_summary = {
            "batch_number": self.current_batch,
            "batch_size": len(batch),
            "successful": success,
            "failed": failure,
            "time_taken_minutes": time_taken / 60,
            "average_time_per_speech": time_taken / len(batch),
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "speeches": [speech['document_id'] for speech in batch]
        }
        
        summary_path = self.output_base_dir / f"batch_{self.current_batch}_summary.json"
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(batch_summary, f, indent=2, ensure_ascii=False)
        
        logger.info(f"📄 Batch summary saved to: {summary_path}")
    
    def extract_all_speeches(self) -> None:
        """Extract transcripts for all speeches in batches."""
        pending_speeches = self._get_pending_speeches()
        total_speeches = len(pending_speeches)
        
        if total_speeches == 0:
            logger.info("🎉 All speeches have already been processed!")
            return
        
        logger.info(f"🎯 Starting extraction of {total_speeches} pending speeches")
        logger.info(f"Output directory: {self.output_base_dir}")
        logger.info(f"Using Whisper model: {self.extractor.whisper_model}")
        logger.info(f"Batch size: {self.batch_size}")
        
        start_time = time.time()
        
        # Process in batches
        for i in range(0, total_speeches, self.batch_size):
            batch = pending_speeches[i:i + self.batch_size]
            logger.info(f"\n{'='*60}")
            logger.info(f"📦 Processing Batch {self.current_batch + 1} of {(total_speeches + self.batch_size - 1) // self.batch_size}")
            logger.info(f"{'='*60}")
            
            try:
                self.extract_batch(batch)
                
                # Save overall progress after each batch
                self._save_overall_progress()
                
                # Add delay between batches
                if i + self.batch_size < total_speeches:
                    logger.info("⏳ Waiting 30 seconds before next batch...")
                    time.sleep(30)
                    
            except Exception as e:
                logger.error(f"💥 Batch {self.current_batch} failed: {e}")
                logger.error("Continuing with next batch...")
                continue
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Log final statistics
        logger.info("\n" + "=" * 60)
        logger.info("🎉 EXTRACTION COMPLETE")
        logger.info("=" * 60)
        logger.info(f"Total speeches processed: {total_speeches}")
        logger.info(f"Successful: {self.success_count}")
        logger.info(f"Failed: {self.failure_count}")
        logger.info(f"Skipped (already processed): {self.skipped_count}")
        logger.info(f"Success rate: {(self.success_count/total_speeches)*100:.1f}%")
        logger.info(f"Total time: {total_time/60:.1f} minutes")
        logger.info(f"Average time per speech: {total_time/total_speeches:.1f} seconds")
        
        # Save final summary
        self._save_final_summary(total_time)
    
    def _save_overall_progress(self):
        """Save current progress summary."""
        progress = {
            "current_batch": self.current_batch,
            "successful": self.success_count,
            "failed": self.failure_count,
            "skipped": self.skipped_count,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")
        }
        
        progress_path = self.output_base_dir / "extraction_progress.json"
        with open(progress_path, 'w', encoding='utf-8') as f:
            json.dump(progress, f, indent=2, ensure_ascii=False)
    
    def _save_final_summary(self, total_time: float):
        """Save final extraction summary."""
        summary = {
            "extraction_summary": {
                "total_speeches": len(self._get_pending_speeches()) + self.skipped_count,
                "successful": self.success_count,
                "failed": self.failure_count,
                "skipped": self.skipped_count,
                "success_rate": (self.success_count/(self.success_count + self.failure_count))*100 if (self.success_count + self.failure_count) > 0 else 0,
                "total_time_minutes": total_time/60,
                "average_time_per_speech": total_time/(self.success_count + self.failure_count) if (self.success_count + self.failure_count) > 0 else 0
            },
            "extraction_timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "whisper_model": self.extractor.whisper_model,
            "extraction_method": "efficient_batch_processing",
            "batch_size": self.batch_size
        }
        
        summary_path = self.output_base_dir / "extraction_summary_efficient.json"
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        logger.info(f"📄 Final summary saved to: {summary_path}")

def main():
    """Main execution function."""
    # Paths
    metadata_path = "corpus/2024_campaign/2024_campaign_metadata.json"
    output_base_dir = "corpus/2024_campaign"
    
    # Verify paths exist
    if not Path(metadata_path).exists():
        logger.error(f"Metadata file not found: {metadata_path}")
        return
    
    # Create extractor with small batch size for stability
    extractor = EfficientTrump2024Extractor(
        metadata_path=metadata_path, 
        output_base_dir=output_base_dir,
        batch_size=3  # Process only 3 speeches at a time
    )
    
    # Run extraction
    extractor.extract_all_speeches()

if __name__ == "__main__":
    main()
