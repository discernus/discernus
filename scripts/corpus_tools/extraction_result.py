#!/usr/bin/env python3
"""
Extraction Result Data Structure

This module defines the core data structures for transcript extraction results
that are used across the entire transcript extraction infrastructure.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path


@dataclass
class VideoInfo:
    """Container for video metadata information"""
    video_id: str
    title: Optional[str] = None
    channel: Optional[str] = None
    upload_date: Optional[str] = None
    description: Optional[str] = None
    duration: Optional[int] = None
    view_count: Optional[int] = None
    like_count: Optional[int] = None
    url: Optional[str] = None
    
    def __post_init__(self):
        """Set default URL if not provided"""
        if self.url is None:
            self.url = f"https://www.youtube.com/watch?v={self.video_id}"


@dataclass
class QualityMetrics:
    """Container for transcript quality assessment metrics"""
    transcript_length: int = 0
    word_count: int = 0
    completeness_score: float = 0.0
    confidence_score: float = 0.0
    language_detected: Optional[str] = None
    extraction_method: Optional[str] = None
    whisper_model_used: Optional[str] = None
    
    def __post_init__(self):
        """Validate quality metrics"""
        if not 0.0 <= self.completeness_score <= 1.0:
            raise ValueError("Completeness score must be between 0.0 and 1.0")
        if not 0.0 <= self.confidence_score <= 100.0:
            raise ValueError("Confidence score must be between 0.0 and 100.0")


@dataclass
class ExtractionResult:
    """Container for complete transcript extraction results"""
    
    # Core result information
    success: bool
    url: str
    video_info: VideoInfo
    
    # Transcript content
    transcript_text: Optional[str] = None
    language: Optional[str] = None
    
    # Quality and metadata
    quality_metrics: QualityMetrics = field(default_factory=QualityMetrics)
    
    # Error information (when success=False)
    error_type: Optional[str] = None
    error_message: Optional[str] = None
    retry_after: Optional[int] = None
    
    # Processing information
    extraction_timestamp: datetime = field(default_factory=datetime.now)
    processing_time_seconds: Optional[float] = None
    
    # File output information
    output_filename: Optional[str] = None
    output_directory: Optional[Path] = None
    
    # Fallback information
    fallback_attempted: bool = False
    fallback_success: bool = False
    primary_method_failed: bool = False
    
    def __post_init__(self):
        """Validate and set derived fields"""
        if self.success and not self.transcript_text:
            raise ValueError("Successful extraction must have transcript text")
        
        if not self.success and not self.error_message:
            raise ValueError("Failed extraction must have error message")
        
        # Set quality metrics if not provided
        if self.transcript_text and self.quality_metrics.transcript_length == 0:
            self.quality_metrics.transcript_length = len(self.transcript_text)
        
        if self.transcript_text and self.quality_metrics.word_count == 0:
            self.quality_metrics.word_count = len(self.transcript_text.split())
    
    @property
    def method(self) -> str:
        """Get the extraction method used"""
        return self.quality_metrics.extraction_method or "unknown"
    
    @property
    def confidence(self) -> float:
        """Get the confidence score"""
        return self.quality_metrics.confidence_score
    
    @property
    def filename(self) -> str:
        """Get the output filename"""
        return self.output_filename or "unknown"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary for serialization"""
        return {
            "success": self.success,
            "url": self.url,
            "method": self.method,
            "confidence": self.confidence,
            "transcript_length": self.quality_metrics.transcript_length,
            "word_count": self.quality_metrics.word_count,
            "language": self.language,
            "extraction_timestamp": self.extraction_timestamp.isoformat(),
            "processing_time": self.processing_time_seconds,
            "error_type": self.error_type,
            "error_message": self.error_message,
            "retry_after": self.retry_after,
            "fallback_attempted": self.fallback_attempted,
            "fallback_success": self.fallback_success,
            "video_info": {
                "title": self.video_info.title,
                "channel": self.video_info.channel,
                "duration": self.video_info.duration,
                "upload_date": self.video_info.upload_date,
                "video_id": self.video_info.video_id
            }
        }
    
    def to_json(self) -> str:
        """Convert result to JSON string"""
        import json
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)
    
    def is_high_quality(self, threshold: float = 80.0) -> bool:
        """Check if the result meets high quality standards"""
        return (
            self.success and
            self.quality_metrics.confidence_score >= threshold and
            self.quality_metrics.completeness_score >= 0.9
        )
    
    def can_retry(self) -> bool:
        """Check if this extraction can be retried"""
        if self.success:
            return False
        
        # Don't retry certain error types
        non_retryable_errors = {
            "content_unavailable",
            "private_video",
            "deleted_video",
            "age_restricted"
        }
        
        return self.error_type not in non_retryable_errors
    
    def get_retry_delay(self, base_delay: int = 60) -> int:
        """Get recommended retry delay in seconds"""
        if not self.can_retry():
            return 0
        
        # Use provided retry_after or calculate exponential backoff
        if self.retry_after:
            return self.retry_after
        
        # Simple exponential backoff for now
        # In a real implementation, this would track retry attempts
        return base_delay


class ExtractionError(Exception):
    """Base exception for transcript extraction errors"""
    
    def __init__(self, message: str, error_type: str, retry_after: Optional[int] = None):
        super().__init__(message)
        self.error_type = error_type
        self.retry_after = retry_after


class YouTubeAPIError(ExtractionError):
    """Exception for YouTube API related errors"""
    pass


class WhisperError(ExtractionError):
    """Exception for Whisper transcription errors"""
    pass


class NetworkError(ExtractionError):
    """Exception for network and connection errors"""
    pass


class ContentUnavailableError(ExtractionError):
    """Exception for unavailable or private content"""
    pass
