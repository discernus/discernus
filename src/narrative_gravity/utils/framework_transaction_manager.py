#!/usr/bin/env python3
"""
Framework Transaction Manager

Implements framework transaction integrity for experiments:
- Framework uncertainty = experiment failure + rollback
- Automatic version detection for changed frameworks
- Database as single source of truth after ingestion
- Comprehensive logging and user guidance

Requirements:
- Any framework validation uncertainty triggers graceful termination
- Framework content changes auto-increment versions
- Complete audit trail of framework decisions
"""

import hashlib
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

try:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from ..models.component_models import FrameworkVersion
    from ..utils.database import get_database_url
    DATABASE_AVAILABLE = True
except ImportError:
    DATABASE_AVAILABLE = False

logger = logging.getLogger(__name__)

class FrameworkValidationResult(Enum):
    """Framework validation result codes"""
    VALID = "valid"
    VERSION_MISMATCH = "version_mismatch"
    CONTENT_CHANGED = "content_changed"
    NOT_FOUND = "not_found"
    VALIDATION_ERROR = "validation_error"
    TRANSACTION_FAILURE = "transaction_failure"

@dataclass
class FrameworkTransactionState:
    """Framework transaction state for rollback capability"""
    framework_name: str
    requested_version: Optional[str]
    database_version: Optional[str]
    content_hash: str
    validation_result: FrameworkValidationResult
    new_version_created: bool = False
    transaction_id: str = ""
    timestamp: str = ""
    error_details: List[str] = None
    
    def __post_init__(self):
        if self.error_details is None:
            self.error_details = []
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()

class FrameworkTransactionManager:
    """
    Framework Transaction Integrity Manager
    
    Ensures framework validity and handles versioning automatically.
    Any uncertainty results in graceful experiment failure.
    """
    
    def __init__(self, transaction_id: str = None):
        self.transaction_id = transaction_id or f"ftx_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.engine = None
        self.Session = None
        self.transaction_states: List[FrameworkTransactionState] = []
        
        if DATABASE_AVAILABLE:
            self.engine = create_engine(get_database_url())
            self.Session = sessionmaker(bind=self.engine)
        
        logger.info(f"🔒 Framework Transaction Manager initialized: {self.transaction_id}")
    
    def validate_framework_for_experiment(self, framework_name: str, 
                                        framework_file_path: Optional[Path] = None,
                                        expected_version: Optional[str] = None) -> FrameworkTransactionState:
        """
        🔒 TRANSACTION INTEGRITY: Validate framework for experiment use
        
        Returns transaction state with validation result.
        CRITICAL: Any uncertainty should result in experiment termination.
        
        Args:
            framework_name: Name of framework to validate
            framework_file_path: Optional path to framework definition file
            expected_version: Optional expected version for validation
            
        Returns:
            FrameworkTransactionState with validation result
        """
        logger.info(f"🔍 Validating framework transaction: {framework_name}")
        
        # Initialize transaction state
        state = FrameworkTransactionState(
            framework_name=framework_name,
            requested_version=expected_version,
            database_version=None,
            content_hash="",
            validation_result=FrameworkValidationResult.VALIDATION_ERROR,
            transaction_id=self.transaction_id
        )
        
        try:
            # Step 1: Check database state (single source of truth)
            db_framework = self._get_database_framework(framework_name, expected_version)
            
            if db_framework:
                state.database_version = db_framework.version
                state.content_hash = self._calculate_framework_hash(db_framework.dipoles_json, db_framework.framework_json)
                logger.info(f"✅ Framework found in database: {framework_name}:{db_framework.version}")
                
                # Step 2: If file provided, validate consistency
                if framework_file_path and framework_file_path.exists():
                    file_consistency = self._validate_file_database_consistency(framework_file_path, db_framework)
                    
                    if file_consistency['consistent']:
                        state.validation_result = FrameworkValidationResult.VALID
                        logger.info(f"✅ Framework file-database consistency validated")
                    else:
                        # Content changed - create new version
                        logger.warning(f"⚠️ Framework content changed - creating new version")
                        state.validation_result = FrameworkValidationResult.CONTENT_CHANGED
                        new_version_state = self._create_new_framework_version(framework_file_path, framework_name, db_framework.version)
                        state.new_version_created = new_version_state['success']
                        if not new_version_state['success']:
                            state.validation_result = FrameworkValidationResult.TRANSACTION_FAILURE
                            state.error_details.extend(new_version_state['errors'])
                else:
                    # No file provided - database is source of truth
                    state.validation_result = FrameworkValidationResult.VALID
                    
            else:
                # Framework not in database
                logger.warning(f"⚠️ Framework not found in database: {framework_name}")
                
                if framework_file_path and framework_file_path.exists():
                    # Import from file to database
                    logger.info(f"📥 Importing framework from file to database")
                    import_result = self._import_framework_to_database(framework_file_path, framework_name)
                    
                    if import_result['success']:
                        state.database_version = import_result['version']
                        state.content_hash = import_result['content_hash']
                        state.validation_result = FrameworkValidationResult.VALID
                        state.new_version_created = True
                        logger.info(f"✅ Framework imported successfully: {framework_name}:{import_result['version']}")
                    else:
                        state.validation_result = FrameworkValidationResult.TRANSACTION_FAILURE
                        state.error_details.extend(import_result['errors'])
                        logger.error(f"❌ Framework import failed: {import_result['errors']}")
                else:
                    # No database record, no file - critical failure
                    state.validation_result = FrameworkValidationResult.NOT_FOUND
                    state.error_details.append(f"Framework {framework_name} not found in database or filesystem")
                    logger.error(f"❌ Framework not found: {framework_name}")
            
        except Exception as e:
            state.validation_result = FrameworkValidationResult.VALIDATION_ERROR
            state.error_details.append(f"Framework validation exception: {e}")
            logger.error(f"❌ Framework validation error: {e}")
        
        # Record transaction state
        self.transaction_states.append(state)
        
        # Log validation result
        self._log_validation_result(state)
        
        return state
    
    def is_transaction_valid(self) -> Tuple[bool, List[str]]:
        """
        🔒 TRANSACTION INTEGRITY: Check if all framework validations are valid
        
        Returns:
            Tuple of (is_valid, error_messages)
            is_valid=False means experiment should terminate
        """
        invalid_states = []
        error_messages = []
        
        for state in self.transaction_states:
            if state.validation_result not in [FrameworkValidationResult.VALID, FrameworkValidationResult.CONTENT_CHANGED]:
                invalid_states.append(state)
                error_messages.extend([
                    f"Framework {state.framework_name}: {state.validation_result.value}",
                    *state.error_details
                ])
        
        is_valid = len(invalid_states) == 0
        
        if not is_valid:
            logger.error(f"🚨 FRAMEWORK TRANSACTION FAILURE: {len(invalid_states)} framework(s) invalid")
            for msg in error_messages:
                logger.error(f"   {msg}")
        else:
            logger.info(f"✅ Framework transaction validation passed: {len(self.transaction_states)} framework(s)")
        
        return is_valid, error_messages
    
    def generate_rollback_guidance(self) -> Dict[str, Any]:
        """
        Generate user guidance for fixing framework transaction failures
        
        Returns:
            Dictionary with specific guidance for each failed framework
        """
        guidance = {
            'transaction_id': self.transaction_id,
            'total_frameworks': len(self.transaction_states),
            'failed_frameworks': [],
            'recommendations': [],
            'commands_to_run': []
        }
        
        for state in self.transaction_states:
            if state.validation_result not in [FrameworkValidationResult.VALID, FrameworkValidationResult.CONTENT_CHANGED]:
                failure_info = {
                    'framework_name': state.framework_name,
                    'validation_result': state.validation_result.value,
                    'error_details': state.error_details,
                    'requested_version': state.requested_version,
                    'database_version': state.database_version
                }
                
                guidance['failed_frameworks'].append(failure_info)
                
                # Generate specific recommendations
                if state.validation_result == FrameworkValidationResult.NOT_FOUND:
                    guidance['recommendations'].append(
                        f"Framework '{state.framework_name}' not found. "
                        f"Create framework definition file and import to database."
                    )
                    guidance['commands_to_run'].extend([
                        f"# Create framework definition file: frameworks/{state.framework_name}/framework_consolidated.json",
                        f"python3 scripts/framework_sync.py import {state.framework_name}",
                        f"python3 scripts/framework_sync.py validate {state.framework_name}"
                    ])
                
                elif state.validation_result == FrameworkValidationResult.VERSION_MISMATCH:
                    guidance['recommendations'].append(
                        f"Framework '{state.framework_name}' version mismatch. "
                        f"Expected: {state.requested_version}, Found: {state.database_version}"
                    )
                    guidance['commands_to_run'].extend([
                        f"python3 scripts/framework_sync.py status",
                        f"python3 scripts/framework_sync.py export {state.framework_name} --version {state.database_version}"
                    ])
                
                elif state.validation_result == FrameworkValidationResult.TRANSACTION_FAILURE:
                    guidance['recommendations'].append(
                        f"Framework '{state.framework_name}' transaction failed. "
                        f"Check database connectivity and framework definition validity."
                    )
                    guidance['commands_to_run'].extend([
                        f"python3 scripts/framework_sync.py validate {state.framework_name}",
                        f"python3 scripts/framework_sync.py status"
                    ])
        
        return guidance
    
    def rollback_transaction(self) -> bool:
        """
        🔒 ROLLBACK: Undo any framework changes made during this transaction
        
        Returns:
            True if rollback successful, False if issues remain
        """
        logger.warning(f"🔄 Rolling back framework transaction: {self.transaction_id}")
        
        rollback_success = True
        
        if not DATABASE_AVAILABLE:
            logger.warning("⚠️ Database not available - cannot rollback framework changes")
            return False
        
        session = self.Session()
        try:
            for state in self.transaction_states:
                if state.new_version_created:
                    # Attempt to remove newly created framework version
                    logger.info(f"🔄 Rolling back framework version: {state.framework_name}:{state.database_version}")
                    
                    framework = session.query(FrameworkVersion).filter_by(
                        framework_name=state.framework_name,
                        version=state.database_version
                    ).first()
                    
                    if framework:
                        session.delete(framework)
                        logger.info(f"✅ Removed framework version: {state.framework_name}:{state.database_version}")
                    else:
                        logger.warning(f"⚠️ Framework version not found for rollback: {state.framework_name}:{state.database_version}")
                        rollback_success = False
            
            if rollback_success:
                session.commit()
                logger.info(f"✅ Framework transaction rollback completed")
            else:
                session.rollback()
                logger.error(f"❌ Framework transaction rollback failed")
                
        except Exception as e:
            session.rollback()
            logger.error(f"❌ Framework transaction rollback error: {e}")
            rollback_success = False
        finally:
            session.close()
        
        return rollback_success
    
    def _get_database_framework(self, framework_name: str, version: Optional[str] = None) -> Optional[FrameworkVersion]:
        """Get framework from database (single source of truth)"""
        if not DATABASE_AVAILABLE:
            return None
        
        session = self.Session()
        try:
            query = session.query(FrameworkVersion).filter_by(framework_name=framework_name)
            
            if version:
                # Handle version prefix variations
                version_variants = [version, f"v{version}", version[1:] if version.startswith('v') else version]
                query = query.filter(FrameworkVersion.version.in_(version_variants))
            else:
                # Get latest version
                query = query.order_by(FrameworkVersion.created_at.desc())
            
            return query.first()
        finally:
            session.close()
    
    def _calculate_framework_hash(self, dipoles_json: Dict, framework_json: Dict) -> str:
        """Calculate hash of framework content for change detection"""
        content = {
            'dipoles': dipoles_json,
            'framework': framework_json
        }
        content_str = json.dumps(content, sort_keys=True)
        return hashlib.sha256(content_str.encode()).hexdigest()[:16]
    
    def _validate_file_database_consistency(self, file_path: Path, db_framework: FrameworkVersion) -> Dict[str, Any]:
        """Validate file content matches database content"""
        try:
            with open(file_path, 'r') as f:
                if file_path.suffix.lower() in ['.yaml', '.yml']:
                    import yaml
                    file_content = yaml.safe_load(f)
                else:
                    file_content = json.load(f)
            
            # Calculate file hash
            file_dipoles = file_content.get('dipoles', [])
            file_framework = file_content.get('framework_meta', {})
            file_hash = self._calculate_framework_hash(file_dipoles, file_framework)
            
            # Calculate database hash
            db_hash = self._calculate_framework_hash(db_framework.dipoles_json, db_framework.framework_json)
            
            return {
                'consistent': file_hash == db_hash,
                'file_hash': file_hash,
                'database_hash': db_hash
            }
            
        except Exception as e:
            return {
                'consistent': False,
                'error': str(e)
            }
    
    def _create_new_framework_version(self, file_path: Path, framework_name: str, current_version: str) -> Dict[str, Any]:
        """Create new framework version for changed content"""
        try:
            # Generate new version number
            new_version = self._generate_next_version(current_version, framework_name)
            
            # Load framework content
            with open(file_path, 'r') as f:
                if file_path.suffix.lower() in ['.yaml', '.yml']:
                    import yaml
                    file_content = yaml.safe_load(f)
                else:
                    file_content = json.load(f)
            
            # Import as new version
            return self._import_framework_to_database(file_path, framework_name, new_version)
            
        except Exception as e:
            return {
                'success': False,
                'errors': [f"Failed to create new framework version: {e}"]
            }
    
    def _import_framework_to_database(self, file_path: Path, framework_name: str, version: str = None) -> Dict[str, Any]:
        """Import framework from file to database"""
        if not DATABASE_AVAILABLE:
            return {
                'success': False,
                'errors': ['Database not available']
            }
        
        session = self.Session()
        try:
            with open(file_path, 'r') as f:
                if file_path.suffix.lower() in ['.yaml', '.yml']:
                    import yaml
                    content = yaml.safe_load(f)
                else:
                    content = json.load(f)
            
            # Extract framework data
            dipoles_data = content.get('dipoles', [])
            framework_data = content.get('framework_meta', {})
            weights_data = content.get('weighting_philosophy', {})
            
            # Generate version if not provided
            if not version:
                version = framework_data.get('version', 'v1.0.0')
            
            # Check if framework version already exists
            existing_framework = session.query(FrameworkVersion).filter_by(
                framework_name=framework_name,
                version=version
            ).first()
            
            if existing_framework:
                # Framework already exists - return existing info
                logger.info(f"✅ Framework already exists in database: {framework_name}:{version}")
                content_hash = self._calculate_framework_hash({'dipoles': dipoles_data}, framework_data)
                return {
                    'success': True,
                    'version': version,
                    'content_hash': content_hash,
                    'already_existed': True
                }
            
            # Create framework version record
            framework_record = FrameworkVersion(
                framework_name=framework_name,
                version=version,
                dipoles_json={'dipoles': dipoles_data},
                framework_json=framework_data,
                weights_json=weights_data,
                description=framework_data.get('description', f'Auto-imported: {self.transaction_id}'),
                validation_status='draft'
            )
            
            session.add(framework_record)
            session.commit()
            
            # Calculate content hash
            content_hash = self._calculate_framework_hash({'dipoles': dipoles_data}, framework_data)
            
            logger.info(f"✅ New framework imported to database: {framework_name}:{version}")
            return {
                'success': True,
                'version': version,
                'content_hash': content_hash,
                'already_existed': False
            }
            
        except Exception as e:
            session.rollback()
            return {
                'success': False,
                'errors': [f"Database import failed: {e}"]
            }
        finally:
            session.close()
    
    def _generate_next_version(self, current_version: str, framework_name: str) -> str:
        """Generate next version number with collision detection for specific framework"""
        if not DATABASE_AVAILABLE:
            # Fallback when no database available
            return f"v{datetime.now().strftime('%Y.%m.%d.%H%M%S')}"
        
        session = self.Session()
        try:
            # Strategy 1: Try to increment patch version
            try:
                if current_version.startswith('v'):
                    version_num = current_version[1:]
                else:
                    version_num = current_version
                
                parts = version_num.split('.')
                if len(parts) >= 3:
                    # Increment patch version
                    parts[2] = str(int(parts[2]) + 1)
                    candidate = f"v{'.'.join(parts)}"
                    
                    # Check if this version exists for this framework
                    if not self._version_exists(session, framework_name, candidate):
                        return candidate
            except (ValueError, IndexError):
                pass
            
            # Strategy 2: Date-based version with collision detection
            today = datetime.now()
            date_base = f"v{today.strftime('%Y.%m.%d')}"
            
            if not self._version_exists(session, framework_name, date_base):
                return date_base
            
            # Strategy 3: Date + time components (collision-resistant)
            time_variants = [
                f"{date_base}.{today.strftime('%H')}",  # Add hour
                f"{date_base}.{today.strftime('%H%M')}",  # Add hour+minute
                f"{date_base}.{today.strftime('%H%M%S')}",  # Add hour+minute+second
            ]
            
            for candidate in time_variants:
                if not self._version_exists(session, framework_name, candidate):
                    return candidate
            
            # Strategy 4: Date + microseconds (virtually collision-proof)
            microsecond_variant = f"{date_base}.{today.strftime('%H%M%S')}.{today.microsecond}"
            return microsecond_variant
            
        except Exception as e:
            # Ultimate fallback - timestamp with transaction ID for uniqueness
            logger.warning(f"Version generation error: {e}, using fallback")
            return f"v{datetime.now().strftime('%Y.%m.%d.%H%M%S')}.{self.transaction_id[-6:]}"
        finally:
            session.close()
    
    def _version_exists(self, session, framework_name: str, version: str) -> bool:
        """Check if a version already exists for the specific framework"""
        try:
            count = session.query(FrameworkVersion).filter_by(
                framework_name=framework_name,
                version=version
            ).count()
            return count > 0
        except Exception:
            return False  # Assume it doesn't exist if we can't check
    
    def _log_validation_result(self, state: FrameworkTransactionState):
        """Log detailed validation result"""
        if state.validation_result == FrameworkValidationResult.VALID:
            logger.info(f"✅ Framework validation PASSED: {state.framework_name}:{state.database_version}")
        elif state.validation_result == FrameworkValidationResult.CONTENT_CHANGED:
            logger.warning(f"🔄 Framework content CHANGED: {state.framework_name} - new version created")
        else:
            logger.error(f"❌ Framework validation FAILED: {state.framework_name} - {state.validation_result.value}")
            for error in state.error_details:
                logger.error(f"   {error}") 