"""
Centralized logging configuration for Narrative Gravity Analysis.
Implements Epic 1 requirement F: Validation & Logging with structured logs and metrics.
"""

import logging
import logging.config
import json
import traceback
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path

# Error codes for structured logging
class ErrorCodes:
    # API Errors (1000-1999)
    API_VALIDATION_ERROR = "E1001"
    API_AUTHENTICATION_ERROR = "E1002"
    API_AUTHORIZATION_ERROR = "E1003"
    API_NOT_FOUND = "E1004"
    API_INTERNAL_ERROR = "E1005"
    
    # Ingestion Errors (2000-2999)
    INGESTION_JSON_PARSE_ERROR = "E2001"
    INGESTION_SCHEMA_VALIDATION_ERROR = "E2002"
    INGESTION_DUPLICATE_DOCUMENT = "E2003"
    INGESTION_FILE_FORMAT_ERROR = "E2004"
    INGESTION_DATABASE_ERROR = "E2005"
    
    # Task Processing Errors (3000-3999)
    TASK_NOT_FOUND = "E3001"
    TASK_CHUNK_NOT_FOUND = "E3002"
    TASK_FRAMEWORK_UNKNOWN = "E3003"
    TASK_API_RATE_LIMITED = "E3004"
    TASK_API_SERVER_ERROR = "E3005"
    TASK_API_CLIENT_ERROR = "E3006"
    TASK_EXECUTION_TIMEOUT = "E3007"
    
    # Job Management Errors (4000-4999)
    JOB_CREATION_ERROR = "E4001"
    JOB_NOT_FOUND = "E4002"
    JOB_INVALID_CONFIGURATION = "E4003"
    JOB_CORPUS_NOT_FOUND = "E4004"
    
    # Database Errors (5000-5999)
    DATABASE_CONNECTION_ERROR = "E5001"
    DATABASE_QUERY_ERROR = "E5002"
    DATABASE_TRANSACTION_ERROR = "E5003"

class MetricsCollector:
    """
    Centralized metrics collection for Epic 1 requirement F.
    Tracks success/failure rates, API costs, processing times.
    """
    
    def __init__(self):
        self.metrics = {
            "ingestion": {
                "total_attempts": 0,
                "successful_corpora": 0,
                "failed_corpora": 0,
                "validation_errors": 0,
                "documents_processed": 0,
                "chunks_created": 0
            },
            "job_processing": {
                "total_jobs": 0,
                "completed_jobs": 0,
                "failed_jobs": 0,
                "active_jobs": 0,
                "total_tasks": 0,
                "completed_tasks": 0,
                "failed_tasks": 0,
                "retried_tasks": 0
            },
            "api_usage": {
                "total_requests": 0,
                "successful_requests": 0,
                "failed_requests": 0,
                "total_cost": 0.0,
                "rate_limit_hits": 0
            },
            "system_health": {
                "uptime_start": datetime.utcnow().isoformat(),
                "last_health_check": None,
                "database_status": "unknown",
                "redis_status": "unknown"
            }
        }
    
    def record_ingestion_attempt(self, success: bool, documents: int = 0, chunks: int = 0, validation_errors: int = 0):
        """Record corpus ingestion metrics."""
        self.metrics["ingestion"]["total_attempts"] += 1
        if success:
            self.metrics["ingestion"]["successful_corpora"] += 1
            self.metrics["ingestion"]["documents_processed"] += documents
            self.metrics["ingestion"]["chunks_created"] += chunks
        else:
            self.metrics["ingestion"]["failed_corpora"] += 1
        self.metrics["ingestion"]["validation_errors"] += validation_errors
    
    def record_job_event(self, event_type: str, job_id: int = None):
        """Record job processing events."""
        if event_type == "created":
            self.metrics["job_processing"]["total_jobs"] += 1
            self.metrics["job_processing"]["active_jobs"] += 1
        elif event_type == "completed":
            self.metrics["job_processing"]["completed_jobs"] += 1
            self.metrics["job_processing"]["active_jobs"] -= 1
        elif event_type == "failed":
            self.metrics["job_processing"]["failed_jobs"] += 1
            self.metrics["job_processing"]["active_jobs"] -= 1
    
    def record_task_event(self, event_type: str, task_id: int = None, api_cost: float = 0.0):
        """Record task processing events."""
        if event_type == "created":
            self.metrics["job_processing"]["total_tasks"] += 1
        elif event_type == "completed":
            self.metrics["job_processing"]["completed_tasks"] += 1
            self.metrics["api_usage"]["total_cost"] += api_cost
        elif event_type == "failed":
            self.metrics["job_processing"]["failed_tasks"] += 1
        elif event_type == "retried":
            self.metrics["job_processing"]["retried_tasks"] += 1
    
    def record_api_request(self, success: bool, cost: float = 0.0, rate_limited: bool = False):
        """Record API usage metrics."""
        self.metrics["api_usage"]["total_requests"] += 1
        if success:
            self.metrics["api_usage"]["successful_requests"] += 1
            self.metrics["api_usage"]["total_cost"] += cost
        else:
            self.metrics["api_usage"]["failed_requests"] += 1
        
        if rate_limited:
            self.metrics["api_usage"]["rate_limit_hits"] += 1
    
    def update_system_health(self, database_status: str, redis_status: str = None):
        """Update system health metrics."""
        self.metrics["system_health"]["last_health_check"] = datetime.utcnow().isoformat()
        self.metrics["system_health"]["database_status"] = database_status
        if redis_status:
            self.metrics["system_health"]["redis_status"] = redis_status
    
    def increment_metric(self, metric_name: str, tags: Dict[str, Any] = None):
        """Increment a metric by 1. Added for backward compatibility with auth system."""
        if metric_name == "users_registered_total":
            self.metrics["ingestion"]["total_attempts"] += 1
        elif metric_name == "user_logins_total":
            self.metrics["api_usage"]["total_requests"] += 1
        # Note: This is a compatibility method. Full metrics should use specific record_* methods.
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary metrics for monitoring."""
        return {
            **self.metrics,
            "summary": {
                "ingestion_success_rate": (
                    self.metrics["ingestion"]["successful_corpora"] / 
                    max(1, self.metrics["ingestion"]["total_attempts"])
                ) * 100,
                "job_success_rate": (
                    self.metrics["job_processing"]["completed_jobs"] / 
                    max(1, self.metrics["job_processing"]["total_jobs"])
                ) * 100,
                "task_success_rate": (
                    self.metrics["job_processing"]["completed_tasks"] / 
                    max(1, self.metrics["job_processing"]["total_tasks"])
                ) * 100,
                "api_success_rate": (
                    self.metrics["api_usage"]["successful_requests"] / 
                    max(1, self.metrics["api_usage"]["total_requests"])
                ) * 100,
                "average_cost_per_task": (
                    self.metrics["api_usage"]["total_cost"] / 
                    max(1, self.metrics["job_processing"]["completed_tasks"])
                )
            }
        }

# Global metrics collector instance
metrics_collector = MetricsCollector()

class StructuredLogger:
    """
    Structured logger with error codes and stack traces.
    Implements Epic 1 requirement F: Validation & Logging.
    """
    
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
    
    def _log_structured(self, level: str, message: str, error_code: str = None, 
                       extra_data: Dict[str, Any] = None, exception: Exception = None):
        """Log with structured format including error codes and stack traces."""
        
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": level,
            "message": message,
            "service": "discernus",
            "version": "1.0.0"
        }
        
        if error_code:
            log_data["error_code"] = error_code
        
        if extra_data:
            log_data["extra"] = extra_data
        
        if exception:
            log_data["exception"] = {
                "type": type(exception).__name__,
                "message": str(exception),
                "stack_trace": traceback.format_exc()
            }
        
        # Log as structured JSON
        structured_message = json.dumps(log_data, indent=None, separators=(',', ':'))
        
        getattr(self.logger, level.lower())(structured_message)
    
    def info(self, message: str, extra_data: Dict[str, Any] = None):
        """Log info message with structured format."""
        self._log_structured("INFO", message, extra_data=extra_data)
    
    def warning(self, message: str, error_code: str = None, extra_data: Dict[str, Any] = None):
        """Log warning with optional error code."""
        self._log_structured("WARNING", message, error_code=error_code, extra_data=extra_data)
    
    def error(self, message: str, error_code: str = None, extra_data: Dict[str, Any] = None, 
              exception: Exception = None):
        """Log error with error code and optional exception details."""
        self._log_structured("ERROR", message, error_code=error_code, 
                           extra_data=extra_data, exception=exception)
    
    def critical(self, message: str, error_code: str = None, extra_data: Dict[str, Any] = None, 
                 exception: Exception = None):
        """Log critical error with error code and exception details."""
        self._log_structured("CRITICAL", message, error_code=error_code, 
                           extra_data=extra_data, exception=exception)

def setup_logging(log_level: str = "INFO", log_file: str = None):
    """
    Configure centralized logging for the entire application.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file path for log output
    """
    
    # Create logs directory if logging to file
    if log_file:
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
    
    # Logging configuration
    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "structured": {
                "format": "%(message)s"  # Messages are already JSON formatted
            },
            "simple": {
                "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": log_level,
                "formatter": "simple",
                "stream": "ext://sys.stdout"
            }
        },
        "loggers": {
            "discernus": {
                "level": log_level,
                "handlers": ["console"],
                "propagate": False
            },
            "src": {
                "level": log_level,
                "handlers": ["console"],
                "propagate": False
            },
            "celery": {
                "level": "INFO",
                "handlers": ["console"],
                "propagate": False
            },
            "uvicorn": {
                "level": "INFO",
                "handlers": ["console"],
                "propagate": False
            }
        },
        "root": {
            "level": log_level,
            "handlers": ["console"]
        }
    }
    
    # Add file handler if specified
    if log_file:
        config["handlers"]["file"] = {
            "class": "logging.FileHandler",
            "level": log_level,
            "formatter": "structured",
            "filename": log_file
        }
        # Add file handler to all loggers
        for logger_name in config["loggers"]:
            config["loggers"][logger_name]["handlers"].append("file")
        config["root"]["handlers"].append("file")
    
    logging.config.dictConfig(config)

def get_logger(name: str) -> StructuredLogger:
    """Get a structured logger instance for a module."""
    return StructuredLogger(name) 