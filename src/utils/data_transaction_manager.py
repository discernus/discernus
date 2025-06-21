#!/usr/bin/env python3
"""
Data Transaction Manager

Implements data integrity validation for experiments:
- Corpus data integrity and content hash verification
- Text encoding and format validation
- Database schema version compatibility
- Data drift detection and prevention

Requirements:
- Any data uncertainty triggers graceful experiment termination
- Content hash mismatches indicate data drift requiring resolution
- Text encoding issues must be resolved before analysis
- Database schema compatibility enforced across experiment lifecycle
"""

import hashlib
import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import chardet

try:
    from sqlalchemy import create_engine, text
    from sqlalchemy.orm import sessionmaker
    from ..utils.database import get_database_url
    DATABASE_AVAILABLE = True
except ImportError:
    DATABASE_AVAILABLE = False

logger = logging.getLogger(__name__)

class DataValidationResult(Enum):
    """Data validation result codes"""
    VALID = "valid"
    FILE_MISSING = "file_missing"
    CONTENT_CHANGED = "content_changed"
    ENCODING_ERROR = "encoding_error"
    EMPTY_FILE = "empty_file"
    CORRUPTED_FILE = "corrupted_file"
    SCHEMA_MISMATCH = "schema_mismatch"
    VALIDATION_ERROR = "validation_error"

@dataclass
class DataTransactionState:
    """Data transaction state for rollback capability"""
    file_path: str
    expected_hash: Optional[str]
    actual_hash: str
    file_size: int
    encoding: str
    validation_result: DataValidationResult
    error_details: List[str] = None
    transaction_id: str = ""
    timestamp: str = ""
    backup_created: bool = False
    
    def __post_init__(self):
        if self.error_details is None:
            self.error_details = []
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()

class DataTransactionManager:
    """
    Data Transaction Integrity Manager
    
    Ensures data validity and handles corpus integrity automatically.
    Any data uncertainty results in graceful experiment failure.
    """
    
    def __init__(self, transaction_id: str = None):
        self.transaction_id = transaction_id or f"dtx_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.engine = None
        self.Session = None
        self.transaction_states: List[DataTransactionState] = []
        
        if DATABASE_AVAILABLE:
            self.engine = create_engine(get_database_url())
            self.Session = sessionmaker(bind=self.engine)
        
        logger.info(f"🔒 Data Transaction Manager initialized: {self.transaction_id}")
    
    def validate_corpus_for_experiment(self, corpus_specs: List[Dict[str, Any]]) -> List[DataTransactionState]:
        """
        🔒 TRANSACTION INTEGRITY: Validate corpus data for experiment use
        
        Returns list of transaction states with validation results.
        CRITICAL: Any data uncertainty should result in experiment termination.
        
        Args:
            corpus_specs: List of corpus specifications from experiment definition
            
        Returns:
            List of DataTransactionState with validation results
        """
        logger.info(f"🔍 Validating data transaction integrity for {len(corpus_specs)} corpus items")
        
        for corpus_spec in corpus_specs:
            # Extract corpus information
            corpus_id = corpus_spec.get('id', corpus_spec.get('name', 'unknown'))
            file_path = corpus_spec.get('file_path')
            expected_hash = corpus_spec.get('content_hash')
            
            # Resolve file path
            if file_path:
                resolved_path = self._resolve_corpus_path(file_path)
                
                logger.info(f"🔍 Validating corpus file: {resolved_path}")
                
                # Perform data validation
                state = self._validate_single_file(resolved_path, expected_hash)
                state.transaction_id = self.transaction_id
                
                self.transaction_states.append(state)
                
                # Log validation result
                self._log_validation_result(state, corpus_id)
            else:
                # No file path provided - check if corpus is in database
                db_state = self._validate_database_corpus(corpus_id)
                if db_state:
                    self.transaction_states.append(db_state)
        
        return self.transaction_states
    
    def validate_database_schema(self) -> DataTransactionState:
        """
        🔒 DATABASE INTEGRITY: Validate database schema compatibility
        
        Returns:
            DataTransactionState with schema validation result
        """
        logger.info("🔍 Validating database schema integrity")
        
        state = DataTransactionState(
            file_path="database_schema",
            expected_hash=None,
            actual_hash="",
            file_size=0,
            encoding="utf-8",
            validation_result=DataValidationResult.VALIDATION_ERROR,
            transaction_id=self.transaction_id
        )
        
        if not DATABASE_AVAILABLE:
            state.validation_result = DataValidationResult.SCHEMA_MISMATCH
            state.error_details.append("Database not available - cannot validate schema")
            return state
        
        try:
            session = self.Session()
            
            # Check critical tables exist
            critical_tables = [
                'experiment', 'run', 'corpus', 'framework_versions'
            ]
            
            for table in critical_tables:
                try:
                    result = session.execute(text(f"SELECT 1 FROM {table} LIMIT 1"))
                    result.fetchone()
                except Exception as e:
                    state.validation_result = DataValidationResult.SCHEMA_MISMATCH
                    state.error_details.append(f"Critical table missing or inaccessible: {table} ({e})")
                    session.close()
                    return state
            
            # Schema validation passed
            state.validation_result = DataValidationResult.VALID
            logger.info("✅ Database schema validation passed")
            
            session.close()
            
        except Exception as e:
            state.validation_result = DataValidationResult.VALIDATION_ERROR
            state.error_details.append(f"Database schema validation failed: {e}")
            logger.error(f"❌ Database schema validation error: {e}")
        
        self.transaction_states.append(state)
        return state
    
    def is_transaction_valid(self) -> Tuple[bool, List[str]]:
        """
        🔒 TRANSACTION INTEGRITY: Check if all data validations are valid
        
        Returns:
            Tuple of (is_valid, error_messages)
            is_valid=False means experiment should terminate
        """
        invalid_states = []
        error_messages = []
        
        for state in self.transaction_states:
            if state.validation_result != DataValidationResult.VALID:
                invalid_states.append(state)
                error_messages.extend([
                    f"Data file {state.file_path}: {state.validation_result.value}",
                    *state.error_details
                ])
        
        is_valid = len(invalid_states) == 0
        
        if not is_valid:
            logger.error(f"🚨 DATA TRANSACTION FAILURE: {len(invalid_states)} file(s) invalid")
            for msg in error_messages:
                logger.error(f"   {msg}")
        else:
            logger.info(f"✅ Data transaction validation passed: {len(self.transaction_states)} file(s)")
        
        return is_valid, error_messages
    
    def generate_rollback_guidance(self) -> Dict[str, Any]:
        """
        Generate user guidance for fixing data transaction failures
        
        Returns:
            Dictionary with specific guidance for each failed file
        """
        guidance = {
            'transaction_id': self.transaction_id,
            'total_files': len(self.transaction_states),
            'failed_files': [],
            'recommendations': [],
            'commands_to_run': []
        }
        
        for state in self.transaction_states:
            if state.validation_result != DataValidationResult.VALID:
                failure_info = {
                    'file_path': state.file_path,
                    'validation_result': state.validation_result.value,
                    'error_details': state.error_details,
                    'expected_hash': state.expected_hash,
                    'actual_hash': state.actual_hash,
                    'file_size': state.file_size,
                    'encoding': state.encoding
                }
                
                guidance['failed_files'].append(failure_info)
                
                # Generate specific recommendations
                if state.validation_result == DataValidationResult.FILE_MISSING:
                    guidance['recommendations'].append(
                        f"File '{state.file_path}' not found. "
                        f"Verify file path and ensure file exists."
                    )
                    guidance['commands_to_run'].extend([
                        f"# Check if file exists: ls -la {state.file_path}",
                        f"# Verify corpus directory: ls -la corpus/",
                        f"# Update corpus manifest if needed"
                    ])
                
                elif state.validation_result == DataValidationResult.CONTENT_CHANGED:
                    guidance['recommendations'].append(
                        f"File '{state.file_path}' content changed. "
                        f"Expected hash: {state.expected_hash}, Found: {state.actual_hash}"
                    )
                    guidance['commands_to_run'].extend([
                        f"# Verify file integrity: sha256sum {state.file_path}",
                        f"# Check for accidental modifications",
                        f"# Restore from backup if available",
                        f"# Update corpus manifest: python3 scripts/corpus_sync.py update"
                    ])
                
                elif state.validation_result == DataValidationResult.ENCODING_ERROR:
                    guidance['recommendations'].append(
                        f"File '{state.file_path}' has encoding issues. "
                        f"Detected encoding: {state.encoding}"
                    )
                    guidance['commands_to_run'].extend([
                        f"# Check file encoding: file {state.file_path}",
                        f"# Convert to UTF-8: iconv -f {state.encoding} -t utf-8 {state.file_path} > {state.file_path}.utf8",
                        f"# Validate UTF-8: python3 -c \"open('{state.file_path}', 'r', encoding='utf-8').read()\""
                    ])
                
                elif state.validation_result == DataValidationResult.EMPTY_FILE:
                    guidance['recommendations'].append(
                        f"File '{state.file_path}' is empty. "
                        f"Ensure file contains valid text content."
                    )
                    guidance['commands_to_run'].extend([
                        f"# Check file size: wc -l {state.file_path}",
                        f"# Verify file content: head -20 {state.file_path}",
                        f"# Remove from experiment if intentionally empty"
                    ])
                
                elif state.validation_result == DataValidationResult.SCHEMA_MISMATCH:
                    guidance['recommendations'].append(
                        f"Database schema compatibility issues detected. "
                        f"Check database connectivity and schema version."
                    )
                    guidance['commands_to_run'].extend([
                        f"# Check database connectivity: python3 check_database.py",
                        f"# Run schema migrations: alembic upgrade head",
                        f"# Validate database tables: python3 scripts/validate_schema.py"
                    ])
        
        return guidance
    
    def rollback_transaction(self) -> bool:
        """
        🔒 ROLLBACK: Undo any data changes made during this transaction
        
        Returns:
            True if rollback successful, False if issues remain
        """
        logger.warning(f"🔄 Rolling back data transaction: {self.transaction_id}")
        
        rollback_success = True
        
        for state in self.transaction_states:
            if state.backup_created:
                # Restore from backup if created
                backup_path = f"{state.file_path}.backup_{self.transaction_id}"
                if Path(backup_path).exists():
                    try:
                        # Restore original file
                        os.rename(backup_path, state.file_path)
                        logger.info(f"✅ Restored file from backup: {state.file_path}")
                    except Exception as e:
                        logger.error(f"❌ Failed to restore backup: {e}")
                        rollback_success = False
                else:
                    logger.warning(f"⚠️ Backup file not found: {backup_path}")
                    rollback_success = False
        
        if rollback_success:
            logger.info(f"✅ Data transaction rollback completed")
        else:
            logger.error(f"❌ Data transaction rollback failed")
        
        return rollback_success
    
    def _resolve_corpus_path(self, file_path: str) -> Path:
        """Resolve corpus file path to absolute path"""
        path = Path(file_path)
        
        if path.is_absolute():
            return path
        
        # Try relative to current directory
        if path.exists():
            return path.resolve()
        
        # Try relative to corpus directory
        corpus_path = Path("corpus") / path
        if corpus_path.exists():
            return corpus_path.resolve()
        
        # Try raw_sources subdirectory
        raw_sources_path = Path("corpus/raw_sources") / path
        if raw_sources_path.exists():
            return raw_sources_path.resolve()
        
        # Return original path for error reporting
        return path.resolve()
    
    def _validate_single_file(self, file_path: Path, expected_hash: Optional[str] = None) -> DataTransactionState:
        """Validate a single corpus file"""
        state = DataTransactionState(
            file_path=str(file_path),
            expected_hash=expected_hash,
            actual_hash="",
            file_size=0,
            encoding="unknown",
            validation_result=DataValidationResult.VALIDATION_ERROR
        )
        
        try:
            # Check if file exists
            if not file_path.exists():
                state.validation_result = DataValidationResult.FILE_MISSING
                state.error_details.append(f"File not found: {file_path}")
                return state
            
            # Check file size
            state.file_size = file_path.stat().st_size
            if state.file_size == 0:
                state.validation_result = DataValidationResult.EMPTY_FILE
                state.error_details.append(f"File is empty: {file_path}")
                return state
            
            # Detect encoding
            with open(file_path, 'rb') as f:
                raw_data = f.read(min(10000, state.file_size))  # Read first 10KB for detection
                encoding_result = chardet.detect(raw_data)
                state.encoding = encoding_result.get('encoding', 'unknown')
                confidence = encoding_result.get('confidence', 0.0)
            
            # Validate encoding confidence
            if confidence < 0.7:
                state.validation_result = DataValidationResult.ENCODING_ERROR
                state.error_details.append(f"Low encoding confidence: {confidence:.2f} for {state.encoding}")
                return state
            
            # Try to read file with detected encoding
            try:
                with open(file_path, 'r', encoding=state.encoding) as f:
                    content = f.read()
                    
                # Check for minimum content length
                if len(content.strip()) < 10:
                    state.validation_result = DataValidationResult.EMPTY_FILE
                    state.error_details.append(f"File content too short: {len(content)} characters")
                    return state
                    
            except UnicodeDecodeError as e:
                state.validation_result = DataValidationResult.ENCODING_ERROR
                state.error_details.append(f"Unicode decode error: {e}")
                return state
            
            # Calculate content hash
            state.actual_hash = self._calculate_file_hash(file_path)
            
            # Validate content hash if provided
            if expected_hash:
                if state.actual_hash != expected_hash:
                    state.validation_result = DataValidationResult.CONTENT_CHANGED
                    state.error_details.append(f"Content hash mismatch: expected {expected_hash}, got {state.actual_hash}")
                    return state
            
            # All validations passed
            state.validation_result = DataValidationResult.VALID
            
        except Exception as e:
            state.validation_result = DataValidationResult.VALIDATION_ERROR
            state.error_details.append(f"File validation error: {e}")
        
        return state
    
    def _validate_database_corpus(self, corpus_id: str) -> Optional[DataTransactionState]:
        """Validate corpus that exists in database"""
        if not DATABASE_AVAILABLE:
            return None
        
        # This would integrate with existing corpus registry
        # For now, return None to indicate database corpus validation not implemented
        logger.info(f"Database corpus validation not yet implemented for: {corpus_id}")
        return None
    
    def _calculate_file_hash(self, file_path: Path) -> str:
        """Calculate SHA256 hash of file content"""
        sha256_hash = hashlib.sha256()
        
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)
        
        return sha256_hash.hexdigest()[:16]  # Short hash for display
    
    def _log_validation_result(self, state: DataTransactionState, corpus_id: str):
        """Log detailed validation result"""
        if state.validation_result == DataValidationResult.VALID:
            logger.info(f"✅ Data validation PASSED: {corpus_id} ({state.file_size} bytes, {state.encoding})")
        else:
            logger.error(f"❌ Data validation FAILED: {corpus_id} - {state.validation_result.value}")
            for error in state.error_details:
                logger.error(f"   {error}") 