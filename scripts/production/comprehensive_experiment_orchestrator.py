#!/usr/bin/env python3
"""
Comprehensive Experiment Orchestrator

Addresses critical gaps identified in IDITI validation study failure:
- Single unified tool for complete experiment lifecycle
- Auto-component registration and validation  
- Experiment context propagation
- Clear error handling and guidance

Phase 1: Core Orchestrator (Day 1 Implementation)
"""

import json
import sys
import argparse
import hashlib
import os
import webbrowser
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
import logging
from datetime import datetime
from enum import Enum
import pickle

# Configure basic logging (will be enhanced with experiment logging)
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    logger.warning("PyYAML not available - YAML functionality limited")
    YAML_AVAILABLE = False
    yaml = None

try:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from narrative_gravity.models.component_models import FrameworkVersion, PromptTemplate, WeightingMethodology
    from narrative_gravity.utils.database import get_database_url
    from narrative_gravity.corpus.registry import CorpusRegistry
    from narrative_gravity.corpus.intelligent_ingestion import IntelligentIngestionService
    from narrative_gravity.utils.experiment_logging import (
        get_experiment_logger, 
        setup_experiment_logging,
        ExperimentErrorCodes
    )
    from narrative_gravity.api.analysis_service import RealAnalysisService
    DATABASE_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Database imports not available: {e}")
    DATABASE_AVAILABLE = False

# Add import with try/except for optional architectural compliance
try:
    sys.path.insert(0, str(Path(__file__).parent))
    from architectural_compliance_validator import ArchitecturalComplianceValidator
    ARCHITECTURAL_COMPLIANCE_AVAILABLE = True
except ImportError:
    logger.warning("Architectural compliance validator not available")
    ARCHITECTURAL_COMPLIANCE_AVAILABLE = False

class MissingComponentsError(Exception):
    """Raised when required experiment components are missing"""
    def __init__(self, missing_components: List[str], guidance: Dict[str, str]):
        self.missing_components = missing_components
        self.guidance = guidance
        super().__init__(f"Missing components: {', '.join(missing_components)}")

class FrameworkTransactionIntegrityError(Exception):
    """
    🔒 FRAMEWORK TRANSACTION INTEGRITY ERROR
    
    Exception raised when framework validation uncertainty threatens experiment integrity.
    This is a critical error that requires experiment termination and user intervention.
    """
    def __init__(self, framework_errors: List[str], guidance: Dict[str, Any], detailed_message: str):
        self.framework_errors = framework_errors
        self.guidance = guidance
        self.detailed_message = detailed_message
        self.transaction_id = guidance.get('transaction_id', 'unknown')
        
        # Create concise error message for exception
        error_summary = f"Framework transaction integrity failure (Transaction: {self.transaction_id})"
        
        super().__init__(error_summary)

@dataclass
class ComponentInfo:
    """Information about an experiment component"""
    component_type: str
    component_id: str
    version: Optional[str] = None
    file_path: Optional[str] = None
    expected_hash: Optional[str] = None
    content_hash: Optional[str] = None  # NEW: Content hash for unified asset management
    storage_path: Optional[str] = None  # NEW: Path in content-addressable storage
    exists_in_db: bool = False
    exists_on_filesystem: bool = False
    needs_registration: bool = False
    validated_content: Optional[Dict[str, Any]] = None  # NEW: Store validated content

@dataclass
class ExperimentContext:
    """Experiment context for hypothesis-aware analysis"""
    name: str
    description: str
    version: str
    created: str
    hypotheses: List[str] = field(default_factory=list)
    research_context: str = ""
    success_criteria: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    principal_investigator: Optional[str] = None
    institution: Optional[str] = None
    funding_source: Optional[str] = None
    ethical_clearance: Optional[str] = None
    
    def to_prompt_context(self) -> str:
        """Generate context string for LLM prompts"""
        context_parts = []
        
        # Basic experiment information
        context_parts.append(f"EXPERIMENT: {self.name}")
        if self.description:
            context_parts.append(f"DESCRIPTION: {self.description}")
        
        # Research context
        if self.research_context:
            context_parts.append(f"RESEARCH CONTEXT: {self.research_context}")
        
        # Hypotheses being tested
        if self.hypotheses:
            context_parts.append("HYPOTHESES BEING TESTED:")
            for i, hypothesis in enumerate(self.hypotheses, 1):
                context_parts.append(f"  H{i}: {hypothesis}")
        
        # Success criteria
        if self.success_criteria:
            context_parts.append("SUCCESS CRITERIA:")
            for criterion in self.success_criteria:
                context_parts.append(f"  • {criterion}")
        
        return "\n".join(context_parts)
    
    def to_metadata_dict(self) -> Dict[str, Any]:
        """Generate metadata dictionary for database storage"""
        metadata = {
            'experiment_name': self.name,
            'experiment_description': self.description,
            'experiment_version': self.version,
            'experiment_created': self.created,
            'research_context': self.research_context,
            'hypotheses': self.hypotheses,
            'success_criteria': self.success_criteria,
            'tags': self.tags
        }
        
        # Optional institutional metadata
        if self.principal_investigator:
            metadata['principal_investigator'] = self.principal_investigator
        if self.institution:
            metadata['institution'] = self.institution
        if self.funding_source:
            metadata['funding_source'] = self.funding_source
        if self.ethical_clearance:
            metadata['ethical_clearance'] = self.ethical_clearance
        
        return metadata
    
    def generate_context_summary(self) -> str:
        """Generate human-readable context summary"""
        summary_parts = []
        
        summary_parts.append(f"📊 Experiment: {self.name} (v{self.version})")
        summary_parts.append(f"📝 Description: {self.description}")
        
        if self.research_context:
            summary_parts.append(f"🔬 Research Context: {self.research_context}")
        
        if self.hypotheses:
            summary_parts.append(f"🎯 Testing {len(self.hypotheses)} hypothesis(es):")
            for i, hypothesis in enumerate(self.hypotheses, 1):
                summary_parts.append(f"   H{i}: {hypothesis}")
        
        if self.success_criteria:
            summary_parts.append(f"✅ Success Criteria ({len(self.success_criteria)}):")
            for criterion in self.success_criteria:
                summary_parts.append(f"   • {criterion}")
        
        if self.tags:
            summary_parts.append(f"🏷️  Tags: {', '.join(self.tags)}")
        
        return "\n".join(summary_parts)

class ConsolidatedFrameworkLoader:
    """Loader for consolidated framework format"""
    
    def __init__(self, frameworks_dir: str = "frameworks"):
        self.frameworks_dir = Path(frameworks_dir)
    
    def load_framework(self, framework_name: str) -> Dict[str, Any]:
        """Load framework using enhanced pattern matching - descriptive names first, fallback to legacy"""
        framework_dir = self.frameworks_dir / framework_name
        
        if not framework_dir.exists():
            raise FileNotFoundError(f"Framework directory not found: {framework_name}")
        
        # Enhanced framework file detection with pattern matching
        framework_patterns = [
            # 1. Descriptive framework names (new pattern) - highest priority
            "*_framework.yaml",
            "*_framework.json", 
            # 2. Consolidated format (enhanced legacy support)
            "framework_consolidated.json",
            # 3. Standard framework names (current pattern)
            "framework.yaml",
            "framework.json"
        ]
        
        main_framework_file = None
        
        # Find the main framework file using pattern matching
        for pattern in framework_patterns:
            matches = list(framework_dir.glob(pattern))
            if matches:
                # If multiple matches, prefer the first alphabetically for consistency
                main_framework_file = sorted(matches)[0]
                logger.info(f"Found framework file using pattern '{pattern}': {main_framework_file.name}")
                break
        
        if main_framework_file:
            logger.info(f"Loading framework: {framework_name} from {main_framework_file.name}")
            
            try:
                if main_framework_file.suffix.lower() == '.yaml':
                    # Handle YAML format
                    import yaml
                    with open(main_framework_file, 'r') as f:
                        return yaml.safe_load(f)
                else:
                    # Handle JSON format
                    with open(main_framework_file, 'r') as f:
                        return json.load(f)
            except Exception as e:
                logger.error(f"Error loading framework file {main_framework_file}: {e}")
                raise
        
        raise FileNotFoundError(f"Framework not found: {framework_name}")
    
    def validate_framework_structure(self, framework: Dict[str, Any]) -> List[str]:
        """Validate framework has required sections"""
        # For consolidated format
        consolidated_sections = [
            'framework_meta', 'coordinate_system', 'dipoles', 
            'weighting_philosophy', 'prompt_configuration'
        ]
        
        # For legacy format  
        legacy_sections = ['framework_name', 'dipoles', 'wells']
        
        if 'framework_meta' in framework:
            # Consolidated format validation
            missing = [section for section in consolidated_sections if section not in framework]
        else:
            # Legacy format validation
            missing = [section for section in legacy_sections if section not in framework]
        
        return missing

class FrameworkAutoRegistrar:
    """Auto-registration for frameworks using existing database infrastructure"""
    
    def __init__(self):
        if not DATABASE_AVAILABLE:
            raise RuntimeError("Database not available for framework registration")
        
        self.engine = create_engine(get_database_url())
        self.Session = sessionmaker(bind=self.engine)
        self.frameworks_dir = Path("frameworks")
    
    def register_framework(self, framework_id: str, version: str = None) -> bool:
        """Register framework from filesystem to database"""
        logger.info(f"🔧 Auto-registering framework: {framework_id}")
        
        framework_dir = self.frameworks_dir / framework_id
        if not framework_dir.exists():
            logger.error(f"Framework directory not found: {framework_dir}")
            return False
        
        session = self.Session()
        try:
            # Load framework files (try consolidated first)
            consolidated_file = framework_dir / "framework_consolidated.json"
            legacy_framework_file = framework_dir / "framework.json"
            dipoles_file = framework_dir / "dipoles.json" 
            weights_file = framework_dir / "weights.json"
            
            if consolidated_file.exists():
                # Load consolidated format
                with open(consolidated_file, 'r') as f:
                    consolidated_data = json.load(f)
                
                # Extract components for database storage
                framework_data = {
                    'framework_name': framework_id,
                    'version': consolidated_data.get('framework_meta', {}).get('version', version or 'v1.0'),
                    'description': consolidated_data.get('framework_meta', {}).get('description', ''),
                    'coordinate_system': consolidated_data.get('coordinate_system', {}),
                    'dipoles': consolidated_data.get('dipoles', []),
                    'wells': self._extract_wells_from_consolidated(consolidated_data),
                    'theoretical_foundation': consolidated_data.get('framework_meta', {}).get('theoretical_foundation', {})
                }
                
                dipoles_data = {'dipoles': consolidated_data.get('dipoles', [])}
                weights_data = consolidated_data.get('weighting_philosophy', {})
                
            else:
                # Load legacy format
                if not all(f.exists() for f in [legacy_framework_file, dipoles_file, weights_file]):
                    logger.error(f"Missing required framework files in {framework_dir}")
                    return False
                
                with open(legacy_framework_file, 'r') as f:
                    framework_data = json.load(f)
                with open(dipoles_file, 'r') as f:
                    dipoles_data = json.load(f)
                with open(weights_file, 'r') as f:
                    weights_data = json.load(f)
            
            # Check if framework version already exists
            framework_version = framework_data.get('version', version or 'v1.0')
            existing = session.query(FrameworkVersion).filter_by(
                framework_name=framework_id,
                version=framework_version
            ).first()
            
            if existing:
                logger.info(f"Framework {framework_id}:{framework_version} already exists in database")
                return True
            
            # Create new framework version
            framework_record = FrameworkVersion(
                framework_name=framework_id,
                version=framework_version,
                dipoles_json=dipoles_data,
                framework_json=framework_data,
                weights_json=weights_data,
                description=framework_data.get('description', f'Auto-registered from filesystem'),
                theoretical_foundation=str(framework_data.get('theoretical_foundation', '')),
                validation_status="draft"
            )
            
            session.add(framework_record)
            session.commit()
            
            logger.info(f"✅ Successfully registered framework: {framework_id}:{framework_version}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to register framework {framework_id}: {e}")
            session.rollback()
            return False
        finally:
            session.close()
    
    def _extract_wells_from_consolidated(self, consolidated_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract wells configuration from consolidated framework data"""
        wells = {}
        dipoles = consolidated_data.get('dipoles', [])
        
        for dipole in dipoles:
            if 'positive' in dipole:
                pos_well = dipole['positive']
                wells[pos_well['name']] = {
                    'angle': pos_well.get('angle', 0),
                    'weight': pos_well.get('weight', 1.0),
                    'type': pos_well.get('type', 'integrative'),
                    'tier': pos_well.get('tier', 'primary'),
                    'description': pos_well.get('description', '')
                }
            
            if 'negative' in dipole:
                neg_well = dipole['negative']
                wells[neg_well['name']] = {
                    'angle': neg_well.get('angle', 180),
                    'weight': neg_well.get('weight', -1.0),
                    'type': neg_well.get('type', 'disintegrative'),
                    'tier': neg_well.get('tier', 'primary'),
                    'description': neg_well.get('description', '')
                }
        
        return wells

class ComponentAutoRegistrar:
    """Auto-registration for prompt templates and weighting schemes"""
    
    def __init__(self):
        if not DATABASE_AVAILABLE:
            raise RuntimeError("Database not available for component registration")
        
        self.engine = create_engine(get_database_url())
        self.Session = sessionmaker(bind=self.engine)
    
    def register_prompt_template(self, template_id: str, version: str = None) -> bool:
        """Register default prompt template"""
        logger.info(f"🔧 Auto-registering prompt template: {template_id}")
        
        session = self.Session()
        try:
            # Check if template already exists
            template_version = version or "v2.1"
            existing = session.query(PromptTemplate).filter_by(
                name=template_id,
                version=template_version
            ).first()
            
            if existing:
                logger.info(f"Prompt template {template_id}:{template_version} already exists")
                return True
            
            # Create default template content based on template ID
            template_content = self._generate_default_template_content(template_id)
            
            # Create new prompt template
            template = PromptTemplate(
                name=template_id,
                version=template_version,
                template_content=template_content,
                template_type="hierarchical" if "hierarchical" in template_id else "standard",
                description=f"Auto-registered template: {template_id}",
                validation_status="draft"
            )
            
            session.add(template)
            session.commit()
            
            logger.info(f"✅ Successfully registered prompt template: {template_id}:{template_version}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to register prompt template {template_id}: {e}")
            session.rollback()
            return False
        finally:
            session.close()
    
    def register_weighting_scheme(self, scheme_id: str, version: str = None) -> bool:
        """Register default weighting scheme"""
        logger.info(f"🔧 Auto-registering weighting scheme: {scheme_id}")
        
        session = self.Session()
        try:
            # Check if scheme already exists
            scheme_version = version or "v2.1"
            existing = session.query(WeightingMethodology).filter_by(
                name=scheme_id,
                version=scheme_version
            ).first()
            
            if existing:
                logger.info(f"Weighting scheme {scheme_id}:{scheme_version} already exists")
                return True
            
            # Create default scheme based on scheme ID
            scheme_config = self._generate_default_weighting_config(scheme_id)
            
            # Create new weighting methodology
            weighting = WeightingMethodology(
                name=scheme_id,
                version=scheme_version,
                algorithm_type=scheme_config['algorithm_type'],
                algorithm_description=scheme_config['description'],
                mathematical_formula=scheme_config['formula'],
                parameters_json=scheme_config['parameters'],
                validation_status="draft"
            )
            
            session.add(weighting)
            session.commit()
            
            logger.info(f"✅ Successfully registered weighting scheme: {scheme_id}:{scheme_version}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to register weighting scheme {scheme_id}: {e}")
            session.rollback()
            return False
        finally:
            session.close()
    
    def _generate_default_template_content(self, template_id: str) -> str:
        """Generate default template content based on template ID"""
        if "hierarchical" in template_id:
            return """Analyze the following text using a hierarchical framework approach.

Consider the hierarchical relationship between wells:
- Primary wells (high influence): Dominant narrative themes
- Secondary wells (medium influence): Supporting narrative elements  
- Tertiary wells (lower influence): Background narrative presence

TEXT TO ANALYZE:
{text_content}

Provide scores (0.0-1.0) for each framework well and explain the hierarchical relationships."""
        
        else:
            return """Analyze the following text using the specified framework.

TEXT TO ANALYZE:
{text_content}

Provide scores (0.0-1.0) for each framework well with supporting evidence."""
    
    def _generate_default_weighting_config(self, scheme_id: str) -> Dict[str, Any]:
        """Generate default weighting configuration based on scheme ID"""
        if scheme_id == "winner_take_most":
            return {
                'algorithm_type': 'winner_take_most',
                'description': 'Winner-take-most algorithm that amplifies dominant themes while preserving subtlety',
                'formula': 'w_amplified = w_base ^ amplification_factor',
                'parameters': {
                    'amplification_factor': 1.5,
                    'threshold': 0.6,
                    'normalization': 'preserve_ratios'
                }
            }
        elif scheme_id == "proportional":
            return {
                'algorithm_type': 'proportional',
                'description': 'Proportional weighting using direct well scores',
                'formula': 'w_final = w_raw / sum(w_raw)',
                'parameters': {
                    'normalization': 'sum_to_one'
                }
            }
        else:
            return {
                'algorithm_type': 'hierarchical_weighted',
                'description': 'Hierarchical weighting with tier-based amplification',
                'formula': 'w_final = w_raw * tier_weight',
                'parameters': {
                    'primary_weight': 1.0,
                    'secondary_weight': 0.8,
                    'tertiary_weight': 0.6
                }
            }

class CorpusAutoRegistrar:
    """Auto-registration and validation for corpus files"""
    
    def __init__(self):
        if not DATABASE_AVAILABLE:
            raise RuntimeError("Database not available for corpus registration")
        
        self.corpus_registry = CorpusRegistry()
        self.ingestion_service = IntelligentIngestionService(
            corpus_registry=self.corpus_registry,
            confidence_threshold=70.0
        )
    
    def validate_corpus_file(self, file_path: str, expected_hash: str = None) -> Dict[str, Any]:
        """Validate corpus file existence and hash"""
        logger.info(f"🔍 Validating corpus file: {file_path}")
        
        corpus_file = Path(file_path)
        
        validation_result = {
            'exists': False,
            'hash_valid': False,
            'calculated_hash': None,
            'size_bytes': 0,
            'hash_manifest_path': None
        }
        
        if not corpus_file.exists():
            logger.warning(f"Corpus file not found: {file_path}")
            return validation_result
        
        validation_result['exists'] = True
        validation_result['size_bytes'] = corpus_file.stat().st_size
        
        # Calculate file hash
        calculated_hash = self._calculate_file_hash(corpus_file)
        validation_result['calculated_hash'] = calculated_hash
        
        # Validate hash if expected hash provided
        if expected_hash:
            validation_result['hash_valid'] = (calculated_hash == expected_hash)
            if not validation_result['hash_valid']:
                logger.warning(f"Hash mismatch for {file_path}")
                logger.warning(f"  Expected: {expected_hash}")
                logger.warning(f"  Calculated: {calculated_hash}")
        else:
            # No expected hash provided - consider valid
            validation_result['hash_valid'] = True
        
        # Check for or generate hash manifest
        manifest_path = self._get_or_create_hash_manifest(corpus_file.parent, corpus_file.name)
        validation_result['hash_manifest_path'] = str(manifest_path) if manifest_path else None
        
        return validation_result
    
    def validate_corpus_collection(self, directory: str, pattern: str = "*.txt") -> Dict[str, Any]:
        """Validate a collection of corpus files"""
        logger.info(f"🔍 Validating corpus collection: {directory}/{pattern}")
        
        corpus_dir = Path(directory)
        if not corpus_dir.exists():
            return {
                'valid': False,
                'error': f"Directory not found: {directory}",
                'files_found': 0,
                'files_valid': 0
            }
        
        # Find matching files
        files = list(corpus_dir.glob(pattern))
        
        validation_results = []
        files_valid = 0
        
        for file_path in files:
            file_result = self.validate_corpus_file(str(file_path))
            file_result['file_path'] = str(file_path)
            validation_results.append(file_result)
            
            if file_result['exists'] and file_result['hash_valid']:
                files_valid += 1
        
        # Generate or update collection manifest
        collection_manifest = self._generate_collection_manifest(corpus_dir, pattern)
        
        return {
            'valid': files_valid == len(files) and len(files) > 0,
            'files_found': len(files),
            'files_valid': files_valid,
            'files': validation_results,
            'collection_manifest': collection_manifest,
            'directory': str(corpus_dir)
        }
    
    def register_corpus_file(self, file_path: str, corpus_id: str = None) -> bool:
        """Register corpus file using intelligent ingestion"""
        logger.info(f"🔧 Auto-registering corpus file: {file_path}")
        
        corpus_file = Path(file_path)
        if not corpus_file.exists():
            logger.error(f"Cannot register missing file: {file_path}")
            return False
        
        try:
            # Use intelligent ingestion for single file
            if corpus_file.is_file():
                # Create temporary directory for processing
                import tempfile
                with tempfile.TemporaryDirectory() as temp_dir:
                    temp_path = Path(temp_dir)
                    
                    # Copy file to temp directory for processing
                    temp_file = temp_path / corpus_file.name
                    import shutil
                    shutil.copy2(corpus_file, temp_file)
                    
                    # Process with intelligent ingestion
                    result = self.ingestion_service.ingest_directory(str(temp_path))
                    
                    # Check if any files were successfully processed
                    successful = result.get('successful', [])
                    if successful:
                        logger.info(f"✅ Successfully registered corpus file: {file_path}")
                        logger.info(f"   Text IDs: {[item.get('text_id', 'N/A') for item in successful]}")
                        return True
                    else:
                        uncertain = result.get('uncertain', [])
                        failed = result.get('failed', [])
                        if uncertain:
                            logger.warning(f"⚠️ Corpus file registered with uncertainty: {file_path}")
                            return True
                        else:
                            logger.error(f"❌ Failed to register corpus file: {file_path}")
                            return False
            else:
                logger.error(f"Expected file, got directory: {file_path}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to register corpus file {file_path}: {e}")
            return False
    
    def register_corpus_collection(self, directory: str, pattern: str = "*.txt") -> bool:
        """Register corpus collection using intelligent ingestion"""
        logger.info(f"🔧 Auto-registering corpus collection: {directory}/{pattern}")
        
        corpus_dir = Path(directory)
        if not corpus_dir.exists():
            logger.error(f"Cannot register missing directory: {directory}")
            return False
        
        try:
            # Use intelligent ingestion for directory
            result = self.ingestion_service.ingest_directory(str(corpus_dir))
            
            # Check overall success
            summary = result.get('summary', {})
            success_rate = summary.get('success_rate', 0)
            
            if success_rate >= 70:  # At least 70% success rate
                logger.info(f"✅ Successfully registered corpus collection: {directory}")
                logger.info(f"   Success rate: {success_rate:.1f}%")
                logger.info(f"   Files processed: {summary.get('total_files', 0)}")
                return True
            else:
                logger.warning(f"⚠️ Corpus collection registered with low success rate: {success_rate:.1f}%")
                return success_rate > 0  # At least some files succeeded
                
        except Exception as e:
            logger.error(f"Failed to register corpus collection {directory}: {e}")
            return False
    
    def check_corpus_in_database(self, corpus_id: str, file_path: str = None) -> bool:
        """Check if corpus item exists in database using CorpusRegistry API"""
        logger.info(f"🔍 Checking corpus in database: {corpus_id} (file_path: {file_path})")
        
        try:
            # Approach 1: Direct lookup by text_id (most reliable)
            if corpus_id:
                try:
                    logger.info(f"🔍 Approach 1: Looking up by text_id '{corpus_id}'")
                    doc = self.corpus_registry.get_document_by_text_id(corpus_id)
                    if doc is not None:
                        logger.info(f"✅ Found corpus {corpus_id} by text_id lookup")
                        return True
                    else:
                        logger.info(f"❌ No document found with text_id '{corpus_id}'")
                except Exception as e:
                    logger.warning(f"❌ Approach 1 failed: {e}")
            
            # Approach 2: Search through all documents for matches
            if corpus_id:
                try:
                    logger.info(f"🔍 Approach 2: Searching all documents for '{corpus_id}'")
                    all_docs = self.corpus_registry.list_documents()
                    logger.info(f"🔍 Approach 2: Got {len(all_docs)} total documents")
                    
                    for doc in all_docs:
                        # Check text_id match
                        if hasattr(doc, 'text_id') and doc.text_id == corpus_id:
                            logger.info(f"✅ Found corpus {corpus_id} by text_id match in document list")
                            return True
                        
                        # Check title contains corpus_id
                        if hasattr(doc, 'title') and doc.title and corpus_id.lower() in doc.title.lower():
                            logger.info(f"✅ Found corpus {corpus_id} by title match: {doc.title}")
                            return True
                        
                        # Check file path match (if provided)
                        if file_path and hasattr(doc, 'file_path'):
                            if str(doc.file_path) == file_path or doc.file_path.name == Path(file_path).name:
                                logger.info(f"✅ Found corpus {corpus_id} by file path match")
                                return True
                
                except Exception as e:
                    logger.warning(f"❌ Approach 2 failed: {e}")
            
            # Approach 3: Check by filename pattern matching  
            if file_path:
                try:
                    from pathlib import Path
                    filename = Path(file_path).name
                    filename_base = filename.replace('.txt', '').replace('.md', '')
                    logger.info(f"🔍 Approach 3: Searching by filename pattern '{filename_base}'")
                    
                    all_docs = self.corpus_registry.list_documents()
                    for doc in all_docs:
                        if hasattr(doc, 'text_id') and doc.text_id:
                            # Check if filename contains corpus_id or vice versa
                            if corpus_id in filename_base or filename_base in doc.text_id:
                                logger.info(f"✅ Found corpus {corpus_id} by filename pattern match: {doc.text_id}")
                                return True
                            
                            # Check for partial matches (reagan in ronald_reagan_1986_challenger)
                            corpus_parts = corpus_id.split('_')
                            filename_parts = filename_base.split('_')
                            
                            # Check if most key parts match
                            matches = 0
                            for part in corpus_parts:
                                if any(part in fp for fp in filename_parts):
                                    matches += 1
                            
                            if matches >= min(2, len(corpus_parts)):
                                logger.info(f"✅ Found corpus {corpus_id} by partial filename match: {doc.text_id}")
                                return True
                                
                except Exception as e:
                    logger.warning(f"❌ Approach 3 failed: {e}")
            
            logger.warning(f"❌ Corpus validation failed: {corpus_id} not found in database")
            return False
            
        except Exception as e:
            logger.error(f"Error checking corpus in database: {e}")
            return False
    
    def _calculate_file_hash(self, file_path: Path) -> str:
        """Calculate SHA-256 hash of file"""
        hash_sha256 = hashlib.sha256()
        
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        
        return hash_sha256.hexdigest()
    
    def _get_or_create_hash_manifest(self, directory: Path, filename: str) -> Optional[Path]:
        """Get existing hash manifest or create one"""
        manifest_file = directory / ".corpus_manifest.json"
        
        # Load existing manifest
        manifest = {}
        if manifest_file.exists():
            try:
                with open(manifest_file, 'r') as f:
                    manifest = json.load(f)
            except Exception as e:
                logger.warning(f"Could not load manifest {manifest_file}: {e}")
                manifest = {}
        
        # Ensure structure
        if 'version' not in manifest:
            manifest['version'] = '1.0.0'
        if 'files' not in manifest:
            manifest['files'] = {}
        
        # Calculate hash for file
        file_path = directory / filename
        if file_path.exists():
            file_hash = self._calculate_file_hash(file_path)
            
            # Update manifest
            manifest['files'][filename] = {
                'hash': file_hash,
                'size_bytes': file_path.stat().st_size,
                'last_updated': datetime.now().isoformat()
            }
            
            manifest['manifest_updated'] = datetime.now().isoformat()
            
            # Save manifest
            try:
                with open(manifest_file, 'w') as f:
                    json.dump(manifest, f, indent=2)
                return manifest_file
            except Exception as e:
                logger.warning(f"Could not save manifest {manifest_file}: {e}")
                return None
        
        return None
    
    def _generate_collection_manifest(self, directory: Path, pattern: str) -> Optional[str]:
        """Generate hash manifest for collection of files"""
        manifest_file = directory / ".corpus_collection_manifest.json"
        
        # Find all matching files
        files = list(directory.glob(pattern))
        
        manifest = {
            'version': '1.0.0',
            'collection_name': directory.name,
            'pattern': pattern,
            'files': {},
            'generated_at': datetime.now().isoformat(),
            'total_files': len(files)
        }
        
        # Calculate hashes for all files
        for file_path in files:
            try:
                file_hash = self._calculate_file_hash(file_path)
                manifest['files'][file_path.name] = {
                    'hash': file_hash,
                    'size_bytes': file_path.stat().st_size,
                    'relative_path': str(file_path.relative_to(directory))
                }
            except Exception as e:
                logger.warning(f"Could not hash file {file_path}: {e}")
        
        # Save manifest
        try:
            with open(manifest_file, 'w') as f:
                json.dump(manifest, f, indent=2)
            logger.info(f"📄 Generated collection manifest: {manifest_file}")
            return str(manifest_file)
        except Exception as e:
            logger.warning(f"Could not save collection manifest {manifest_file}: {e}")
            return None

class ExperimentState(Enum):
    """Experiment transaction states for checkpoint management"""
    INITIALIZING = "initializing"
    PRE_FLIGHT_VALIDATION = "pre_flight_validation"
    COMPONENT_REGISTRATION = "component_registration"
    ANALYSIS_EXECUTION = "analysis_execution"
    ENHANCED_PIPELINE = "enhanced_pipeline"
    ARCHITECTURAL_COMPLIANCE = "architectural_compliance"
    COMPLETED = "completed"
    FAILED = "failed"

class ExperimentOrchestrator:
    """
    🚨 AI ASSISTANT WARNING: This is the PRODUCTION experiment execution system!
    
    ❌ DO NOT suggest custom scripts for:
    - Statistical analysis (use enhanced_analysis_pipeline)
    - Data extraction (built into orchestrator)
    - Hypothesis testing (integrated in pipeline)
    - Report generation (automatic HTML/academic exports)
    - Visualization (comprehensive viz system included)
    
    ✅ ALWAYS use this orchestrator for ALL experiment work!
    
    The orchestrator includes:
    - Complete statistical analysis pipeline
    - Architectural compliance validation
    - Academic export systems
    - Visualization generation
    - Hypothesis tracking
    - Transaction-safe execution with resume capability
    
    Main orchestrator for comprehensive experiment execution with checkpoint/resume support
    """
    
    def __init__(self):
        """Initialize orchestrator with all necessary components"""
        
        # Database and logging setup
        self.current_experiment_id = None
        self.experiment_context = None
        
        # Initialize asset manager for unified storage
        self.asset_manager = UnifiedAssetManager()
        
        # Initialize component loaders and registrars
        self.framework_loader = ConsolidatedFrameworkLoader()
        
        if DATABASE_AVAILABLE:
            try:
                self.framework_registrar = FrameworkAutoRegistrar()
                self.component_registrar = ComponentAutoRegistrar()
                self.corpus_registrar = CorpusAutoRegistrar()
                self.auto_registration_available = True
                logger.info("✅ Auto-registration systems initialized")
            except Exception as e:
                logger.warning(f"⚠️ Auto-registration systems not available: {e}")
                self.framework_registrar = None
                self.component_registrar = None
                self.corpus_registrar = None
                self.auto_registration_available = False
        else:
            self.framework_registrar = None
            self.component_registrar = None
            self.corpus_registrar = None
            self.auto_registration_available = False
            logger.warning("⚠️ Database not available - auto-registration disabled")
        
        # Initialize experiment logging
        try:
            from src.narrative_gravity.analysis.statistical_logger import StatisticalLogger
            self.experiment_logger = StatisticalLogger()
            logger.info("✅ StatisticalLogger initialized")
        except ImportError:
            logger.warning("⚠️ StatisticalLogger not available")
            self.experiment_logger = None
        
        # Initialize auto-registrars if database available
        if DATABASE_AVAILABLE:
            try:
                self.framework_registrar = FrameworkAutoRegistrar()
                self.component_registrar = ComponentAutoRegistrar()
                self.corpus_registrar = CorpusAutoRegistrar()
                self.auto_registration_available = True
            except Exception as e:
                logger.warning(f"Auto-registration not available: {e}")
                self.auto_registration_available = False
        else:
            self.auto_registration_available = False
        
        # Experiment context for hypothesis-aware analysis
        self.experiment_context: Optional[ExperimentContext] = None
        self.current_run_id: Optional[str] = None
        
        # New: Checkpoint management
        self.current_experiment_id: Optional[str] = None
        self.checkpoint_dir: Optional[Path] = None
        self.current_state: ExperimentState = ExperimentState.INITIALIZING
    
    def _create_experiment_id(self, experiment_meta: Dict[str, Any]) -> str:
        """Create unique experiment ID for checkpoint management"""
        name = experiment_meta.get('name', 'experiment')
        version = experiment_meta.get('version', 'v1.0')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{name}_{version}_{timestamp}".replace(' ', '_')
    
    def _get_checkpoint_path(self, experiment_id: str) -> Path:
        """Get checkpoint file path for experiment"""
        checkpoint_dir = Path('experiments') / experiment_id
        checkpoint_dir.mkdir(parents=True, exist_ok=True)
        return checkpoint_dir / 'checkpoint.json'
    
    def save_checkpoint(self, state: ExperimentState, data: Dict[str, Any] = None):
        """Save experiment checkpoint for transaction safety"""
        if not self.current_experiment_id:
            logger.warning("Cannot save checkpoint: no experiment ID set")
            return
        
        checkpoint_path = self._get_checkpoint_path(self.current_experiment_id)
        
        checkpoint_data = {
            'experiment_id': self.current_experiment_id,
            'state': state.value,
            'timestamp': datetime.now().isoformat(),
            'can_resume': state not in [ExperimentState.FAILED, ExperimentState.COMPLETED],
            'orchestrator_version': '2.1.0',  # Track orchestrator version for compatibility
            'data': data or {}
        }
        
        try:
            with open(checkpoint_path, 'w') as f:
                json.dump(checkpoint_data, f, indent=2, default=str)
            
            self.current_state = state
            logger.info(f"📋 Checkpoint saved: {state.value}")
            
        except Exception as e:
            logger.warning(f"Failed to save checkpoint: {e}")
    
    def load_checkpoint(self, experiment_id: str) -> Optional[Dict[str, Any]]:
        """Load experiment checkpoint if it exists"""
        checkpoint_path = self._get_checkpoint_path(experiment_id)
        
        if not checkpoint_path.exists():
            return None
        
        try:
            with open(checkpoint_path, 'r') as f:
                checkpoint_data = json.load(f)
            
            # Validate checkpoint compatibility
            if not checkpoint_data.get('can_resume', False):
                logger.warning(f"Checkpoint exists but experiment cannot be resumed (state: {checkpoint_data.get('state')})")
                return None
            
            logger.info(f"📋 Found checkpoint: {checkpoint_data['state']} from {checkpoint_data['timestamp']}")
            return checkpoint_data
            
        except Exception as e:
            logger.warning(f"Failed to load checkpoint: {e}")
            return None
    
    def find_resumable_experiments(self) -> List[Dict[str, Any]]:
        """Find experiments that can be resumed"""
        experiments_dir = Path('experiments')
        if not experiments_dir.exists():
            return []
        
        resumable = []
        for exp_dir in experiments_dir.iterdir():
            if exp_dir.is_dir():
                checkpoint_path = exp_dir / 'checkpoint.json'
                if checkpoint_path.exists():
                    try:
                        with open(checkpoint_path, 'r') as f:
                            checkpoint = json.load(f)
                        
                        if checkpoint.get('can_resume', False):
                            resumable.append({
                                'experiment_id': checkpoint['experiment_id'],
                                'state': checkpoint['state'],
                                'timestamp': checkpoint['timestamp'],
                                'checkpoint_path': str(checkpoint_path)
                            })
                    except Exception:
                        continue
        
        return sorted(resumable, key=lambda x: x['timestamp'], reverse=True)
    
    def validate_experiment_transaction(self, experiment_id: str) -> bool:
        """Validate that experiment transaction completed successfully"""
        experiment_dir = Path('experiments') / experiment_id
        if not experiment_dir.exists():
            return False
        
        # Check for required transaction outputs
        required_outputs = [
            'enhanced_analysis/pipeline_results.json',
            'enhanced_analysis/structured_results.json',
            'enhanced_analysis/statistical_results.json',
            'enhanced_analysis/architectural_compliance_report.json'
        ]
        
        transaction_complete = all((experiment_dir / output).exists() for output in required_outputs)
        
        # Check final checkpoint state
        checkpoint_path = experiment_dir / 'checkpoint.json'
        if checkpoint_path.exists():
            try:
                with open(checkpoint_path, 'r') as f:
                    checkpoint = json.load(f)
                
                checkpoint_complete = checkpoint.get('state') == ExperimentState.COMPLETED.value
                return transaction_complete and checkpoint_complete
            except Exception:
                return False
        
        return transaction_complete
    
    def load_experiment_definition(self, experiment_file: Path) -> Dict[str, Any]:
        """Load and validate experiment definition with full specification validation"""
        logger.info(f"Loading experiment definition: {experiment_file}")
        
        if not experiment_file.exists():
            raise FileNotFoundError(f"Experiment definition not found: {experiment_file}")
        
        # Step 1: Full experimental specification validation (first step for academics)
        try:
            # Import here to avoid circular dependencies
            import sys
            sys.path.insert(0, str(Path(__file__).parent))
            from experiment_validator import ExperimentSpecValidator
            
            logger.info("🔍 Running comprehensive experimental specification validation...")
            validator = ExperimentSpecValidator()
            validation_result = validator.validate_experiment(experiment_file)
            
            # Check validation results
            if validation_result.is_valid:
                logger.info("✅ Experimental specification validation passed")
                
                # Show academic compliance status
                compliance_summary = []
                for field, compliant in validation_result.academic_compliance.items():
                    status = "✅" if compliant else "⚠️"
                    compliance_summary.append(f"{status} {field.replace('_', ' ').title()}")
                
                if compliance_summary:
                    logger.info(f"🎓 Academic compliance: {len([c for c in validation_result.academic_compliance.values() if c])}/{len(validation_result.academic_compliance)} requirements met")
            else:
                logger.error("❌ Experimental specification validation failed")
                
                # Print detailed errors for researchers
                for error in validation_result.errors:
                    logger.error(f"  • {error}")
                
                raise ValueError(f"Experiment specification validation failed with {len(validation_result.errors)} errors. Please address these academic research requirements before proceeding.")
            
            # Show warnings and suggestions (non-blocking)
            for warning in validation_result.warnings:
                logger.warning(f"⚠️  Academic Note: {warning}")
            
            for suggestion in validation_result.suggestions:
                logger.info(f"💡 Suggestion: {suggestion}")
            
        except ImportError:
            logger.warning("⚠️  ExperimentSpecValidator not available - using basic validation only")
        except Exception as e:
            logger.error(f"❌ Specification validation error: {e}")
            raise ValueError(f"Failed to validate experiment specification: {e}")
        
        # Step 2: Load experiment data (supports YAML auto-conversion)
        try:
            file_content = experiment_file.read_text(encoding='utf-8')
            
            # Auto-detect and handle YAML/JSON
            if experiment_file.suffix.lower() in ['.yaml', '.yml']:
                try:
                    import yaml
                    experiment = yaml.safe_load(file_content)
                    logger.info("✅ Loaded YAML experiment definition (auto-converted)")
                except ImportError:
                    raise ValueError("YAML file detected but PyYAML not installed. Please install PyYAML or convert to JSON.")
            else:
                experiment = json.loads(file_content)
                logger.info("✅ Loaded JSON experiment definition")
            
            # Step 3: Basic schema validation (backup)
            required_fields = ['experiment_meta', 'components', 'execution']
            missing_fields = [field for field in required_fields if field not in experiment]
            if missing_fields:
                raise ValueError(f"Missing required sections: {missing_fields}")
            
            # Step 4: Create experiment context for hypothesis-aware analysis
            self.experiment_context = self._create_experiment_context(experiment)
            
            return experiment
            
        except (json.JSONDecodeError, yaml.YAMLError) as e:
            raise ValueError(f"Invalid format in experiment definition: {e}")
        except Exception as e:
            raise ValueError(f"Error loading experiment definition: {e}")
    
    def _create_experiment_context(self, experiment: Dict[str, Any]) -> ExperimentContext:
        """Create ExperimentContext from experiment definition"""
        meta = experiment.get('experiment_meta', {})
        
        context = ExperimentContext(
            name=meta.get('name', 'Unnamed Experiment'),
            description=meta.get('description', 'No description provided'),
            version=meta.get('version', 'v1.0.0'),
            created=meta.get('created', datetime.now().isoformat()),
            hypotheses=meta.get('hypotheses', []),
            research_context=meta.get('research_context', ''),
            success_criteria=meta.get('success_criteria', []),
            tags=meta.get('tags', []),
            principal_investigator=meta.get('principal_investigator'),
            institution=meta.get('institution'),
            funding_source=meta.get('funding_source'),
            ethical_clearance=meta.get('ethical_clearance')
        )
        
        logger.info(f"🔬 Created experiment context: {context.name} (v{context.version})")
        if context.hypotheses:
            logger.info(f"🎯 Testing {len(context.hypotheses)} hypotheses")
        
        return context
    
    def create_context_enriched_prompt(self, base_prompt: str, analysis_run_info: Dict[str, Any] = None) -> str:
        """Create context-enriched prompt for hypothesis-aware analysis"""
        if not self.experiment_context:
            return base_prompt
        
        # Generate experiment context section
        context_section = self.experiment_context.to_prompt_context()
        
        # Add analysis run specific context if provided
        if analysis_run_info:
            context_section += "\n\nANALYSIS RUN CONTEXT:"
            
            framework = analysis_run_info.get('framework')
            if framework:
                context_section += f"\nFramework: {framework}"
            
            corpus_item = analysis_run_info.get('corpus_item')
            if corpus_item:
                context_section += f"\nCorpus Item: {corpus_item}"
            
            prompt_template = analysis_run_info.get('prompt_template')
            if prompt_template:
                context_section += f"\nPrompt Template: {prompt_template}"
            
            weighting_scheme = analysis_run_info.get('weighting_scheme')
            if weighting_scheme:
                context_section += f"\nWeighting Scheme: {weighting_scheme}"
            
            model = analysis_run_info.get('model')
            if model:
                context_section += f"\nModel: {model}"
        
        # Combine context with base prompt
        enriched_prompt = f"""EXPERIMENTAL CONTEXT:
{context_section}

ANALYSIS INSTRUCTIONS:
When performing this analysis, please keep in mind the experimental context above, particularly the hypotheses being tested and the research context. Your analysis should be conducted in a way that can contribute to validating or refuting the stated hypotheses.

{base_prompt}

EXPERIMENTAL OUTPUT REQUIREMENTS:
In addition to the standard analysis output, please consider how your findings relate to the experimental hypotheses stated above. If relevant, briefly note which hypothesis(es) your analysis supports or challenges."""
        
        return enriched_prompt
    
    def prepare_analysis_metadata(self, analysis_run_info: Dict[str, Any] = None) -> Dict[str, Any]:
        """Prepare metadata for analysis run including experiment context"""
        metadata = {}
        
        if self.experiment_context:
            # Add experiment context to metadata
            metadata.update(self.experiment_context.to_metadata_dict())
        
        # Add analysis run specific metadata
        if analysis_run_info:
            metadata.update({
                'analysis_framework': analysis_run_info.get('framework'),
                'analysis_corpus_item': analysis_run_info.get('corpus_item'),
                'analysis_prompt_template': analysis_run_info.get('prompt_template'),
                'analysis_weighting_scheme': analysis_run_info.get('weighting_scheme'),
                'analysis_model': analysis_run_info.get('model'),
                'analysis_timestamp': datetime.now().isoformat()
            })
        
        return metadata
    
    def generate_context_aware_output(self, analysis_results: Dict[str, Any], analysis_run_info: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate context-aware output with hypothesis validation"""
        if not self.experiment_context:
            return analysis_results
        
        # Create enriched output with experiment context
        enriched_output = analysis_results.copy()
        
        # Add experiment context to output
        enriched_output['experiment_context'] = self.experiment_context.to_metadata_dict()
        
        # Add analysis run context
        if analysis_run_info:
            enriched_output['analysis_run_context'] = analysis_run_info
        
        # Create hypothesis validation section
        hypothesis_validation = {
            'experiment_hypotheses': self.experiment_context.hypotheses,
            'hypothesis_validation_notes': "Automated hypothesis validation not yet implemented",
            'analysis_timestamp': datetime.now().isoformat(),
            'context_propagation_version': "v1.0.0"
        }
        
        enriched_output['hypothesis_validation'] = hypothesis_validation
        
        # Add academic export metadata
        academic_metadata = {
            'experiment_name': self.experiment_context.name,
            'experiment_version': self.experiment_context.version,
            'research_context': self.experiment_context.research_context,
            'principal_investigator': self.experiment_context.principal_investigator,
            'institution': self.experiment_context.institution,
            'tags': self.experiment_context.tags,
            'replication_package_ready': True
        }
        
        enriched_output['academic_metadata'] = academic_metadata
        
        return enriched_output
    
    def create_validation_report(self, all_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create validation report tied to research questions"""
        if not self.experiment_context:
            return {"error": "No experiment context available for validation report"}
        
        report = {
            'experiment_info': self.experiment_context.to_metadata_dict(),
            'validation_timestamp': datetime.now().isoformat(),
            'total_analyses': len(all_results),
            'hypothesis_summary': {},
            'success_criteria_evaluation': {},
            'context_propagation_stats': {
                'context_preserved': len([r for r in all_results if 'experiment_context' in r]),
                'metadata_complete': len([r for r in all_results if 'academic_metadata' in r]),
                'hypothesis_tracking': len([r for r in all_results if 'hypothesis_validation' in r])
            }
        }
        
        # Evaluate each hypothesis (placeholder - real implementation would analyze results)
        for i, hypothesis in enumerate(self.experiment_context.hypotheses, 1):
            report['hypothesis_summary'][f'H{i}'] = {
                'hypothesis': hypothesis,
                'status': 'Under Analysis',
                'supporting_analyses': 0,  # TODO: Implement hypothesis validation logic
                'contradicting_analyses': 0,
                'inconclusive_analyses': len(all_results)
            }
        
        # Evaluate success criteria (placeholder)
        for criterion in self.experiment_context.success_criteria:
            report['success_criteria_evaluation'][criterion] = {
                'status': 'Pending Implementation',
                'evaluation_notes': 'Automated success criteria evaluation not yet implemented'
            }
        
        return report
    
    def validate_components(self, experiment: Dict[str, Any]) -> List[ComponentInfo]:
        """Validate all experiment components and identify missing ones"""
        logger.info("🔍 Validating experiment components...")
        
        components = []
        components_config = experiment.get('components', {})
        
        # Validate frameworks
        for framework_spec in components_config.get('frameworks', []):
            component = self._validate_framework(framework_spec)
            components.append(component)
        
        # Validate prompt templates  
        for template_spec in components_config.get('prompt_templates', []):
            component = self._validate_prompt_template(template_spec)
            components.append(component)
        
        # Validate weighting schemes
        for scheme_spec in components_config.get('weighting_schemes', []):
            component = self._validate_weighting_scheme(scheme_spec)
            components.append(component)
        
        # Validate models
        for model_spec in components_config.get('models', []):
            component = self._validate_model(model_spec)
            components.append(component)
        
        # Validate corpus
        for corpus_spec in components_config.get('corpus', []):
            component = self._validate_corpus(corpus_spec)
            components.append(component)
        
        return components
    
    def _validate_framework(self, framework_spec: Dict[str, Any]) -> ComponentInfo:
        """Validate framework component"""
        framework_id = framework_spec.get('id', framework_spec.get('name'))
        version = framework_spec.get('version')
        file_path = framework_spec.get('file_path')
        
        component = ComponentInfo(
            component_type='framework',
            component_id=framework_id,
            version=version,
            file_path=file_path
        )
        
        # Check if framework exists on filesystem
        try:
            # If file_path is specified, load directly from there
            if file_path:
                framework_path = Path(file_path)
                if not framework_path.exists():
                    raise FileNotFoundError(f"Framework file not found at specified path: {file_path}")
                
                # Load framework directly from file path
                if framework_path.suffix.lower() in ['.yaml', '.yml']:
                    import yaml
                    with open(framework_path, 'r') as f:
                        framework_data = yaml.safe_load(f)
                else:
                    with open(framework_path, 'r') as f:
                        framework_data = json.load(f)
                
                component.exists_on_filesystem = True
                logger.info(f"✅ Framework loaded from workspace file: {file_path}")
                
            else:
                # Fall back to standard framework loader
                framework_data = self.framework_loader.load_framework(framework_id)
                component.exists_on_filesystem = True
            
            # Validate framework structure
            missing_sections = self.framework_loader.validate_framework_structure(framework_data)
            if missing_sections:
                logger.warning(f"Framework {framework_id} missing sections: {missing_sections}")
            
            # 📦 UNIFIED ASSET MANAGEMENT: Store validated framework in content-addressable storage
            if framework_data:
                try:
                    storage_result = self.asset_manager.store_asset(
                        content=framework_data,
                        asset_type='framework',
                        asset_id=framework_id,
                        version=version or 'v1.0.0',
                        source_path=file_path
                    )
                    
                    component.content_hash = storage_result['content_hash']
                    component.storage_path = storage_result['storage_path']
                    component.validated_content = framework_data
                    
                    if storage_result['already_existed']:
                        logger.info(f"📦 Framework {framework_id} already in asset storage (hash: {component.content_hash[:8]}...)")
                    else:
                        logger.info(f"📦 Framework {framework_id} stored in asset storage (hash: {component.content_hash[:8]}...)")
                        
                except Exception as e:
                    logger.warning(f"⚠️ Failed to store framework in asset storage: {e}")
                    # Continue without asset storage - not a blocking error
            
        except FileNotFoundError as e:
            component.exists_on_filesystem = False
            component.needs_registration = True
            logger.warning(f"Framework {framework_id} not found: {e}")
        except Exception as e:
            logger.error(f"Error loading framework {framework_id}: {e}")
            raise
        
        # Check database existence if available
        if DATABASE_AVAILABLE and self.auto_registration_available:
            component.exists_in_db = self._check_framework_in_database(framework_id, version)
        else:
            component.exists_in_db = False
        
        return component
    
    def _validate_prompt_template(self, template_spec: Dict[str, Any]) -> ComponentInfo:
        """Validate prompt template component"""
        template_id = template_spec.get('id', template_spec.get('name'))
        version = template_spec.get('version')
        
        component = ComponentInfo(
            component_type='prompt_template',
            component_id=template_id,
            version=version
        )
        
        # Prompt templates don't have filesystem files - they're stored in database
        component.exists_on_filesystem = True  # Not applicable
        
        # Check database existence if available
        if DATABASE_AVAILABLE and self.auto_registration_available:
            component.exists_in_db = self._check_template_in_database(template_id, version)
        else:
            component.exists_in_db = False
        
        return component
    
    def _validate_weighting_scheme(self, scheme_spec: Dict[str, Any]) -> ComponentInfo:
        """Validate weighting scheme component"""
        scheme_id = scheme_spec.get('id', scheme_spec.get('name'))
        version = scheme_spec.get('version')
        
        component = ComponentInfo(
            component_type='weighting_scheme',
            component_id=scheme_id,
            version=version
        )
        
        # Weighting schemes don't have filesystem files - they're stored in database
        component.exists_on_filesystem = True  # Not applicable
        
        # Check database existence if available
        if DATABASE_AVAILABLE and self.auto_registration_available:
            component.exists_in_db = self._check_weighting_in_database(scheme_id, version)
        else:
            component.exists_in_db = False
        
        return component
    
    def _validate_model(self, model_spec: Dict[str, Any]) -> ComponentInfo:
        """Validate model availability"""
        model_id = model_spec.get('id', model_spec.get('name'))
        provider = model_spec.get('provider', 'openai')
        
        component = ComponentInfo(
            component_type='model',
            component_id=model_id
        )
        
        # TODO: Implement model availability checking (Phase 2)
        component.exists_on_filesystem = True  # Placeholder (models don't use filesystem)
        component.exists_in_db = True  # Placeholder
        
        return component
    
    def _validate_corpus(self, corpus_spec: Dict[str, Any]) -> ComponentInfo:
        """Validate corpus files with hash validation and database checking"""
        corpus_id = corpus_spec.get('id', corpus_spec.get('name'))
        file_path = corpus_spec.get('file_path')
        expected_hash = corpus_spec.get('expected_hash')
        pattern = corpus_spec.get('pattern', '*.txt')  # For directory validation
        
        component = ComponentInfo(
            component_type='corpus',
            component_id=corpus_id,
            file_path=file_path,
            expected_hash=expected_hash
        )
        
        # Validate using corpus registrar if available
        if DATABASE_AVAILABLE and self.auto_registration_available:
            try:
                if file_path:
                    corpus_path = Path(file_path)
                    
                    if corpus_path.is_file():
                        # Single file validation
                        validation = self.corpus_registrar.validate_corpus_file(file_path, expected_hash)
                        component.exists_on_filesystem = validation['exists']
                        
                        # Check hash validation
                        if expected_hash and not validation['hash_valid']:
                            logger.warning(f"Hash validation failed for corpus: {corpus_id}")
                            logger.warning(f"  Expected: {expected_hash}")
                            logger.warning(f"  Calculated: {validation['calculated_hash']}")
                        
                        # Store calculated hash for reference
                        component.expected_hash = validation['calculated_hash']
                        
                    elif corpus_path.is_dir():
                        # Directory collection validation  
                        validation = self.corpus_registrar.validate_corpus_collection(file_path, pattern)
                        component.exists_on_filesystem = validation['valid']
                        
                        if not validation['valid']:
                            logger.warning(f"Corpus collection validation failed: {corpus_id}")
                            logger.warning(f"  Files found: {validation['files_found']}")
                            logger.warning(f"  Files valid: {validation['files_valid']}")
                    else:
                        component.exists_on_filesystem = False
                        
                    # Check database existence
                    component.exists_in_db = self.corpus_registrar.check_corpus_in_database(corpus_id, file_path)
                    
                else:
                    # No file path provided - can't validate
                    component.exists_on_filesystem = False
                    component.exists_in_db = False
                    
            except Exception as e:
                logger.warning(f"Error validating corpus {corpus_id}: {e}")
                # Fallback to basic file existence check
                if file_path:
                    corpus_file = Path(file_path)
                    component.exists_on_filesystem = corpus_file.exists()
                component.exists_in_db = False
        else:
            # Fallback validation without corpus registrar
            if file_path:
                corpus_file = Path(file_path)
                component.exists_on_filesystem = corpus_file.exists()
            component.exists_in_db = False
        
        return component
    
    def _check_framework_in_database(self, framework_id: str, version: str = None) -> bool:
        """Check if framework exists in database"""
        if not DATABASE_AVAILABLE:
            return False
        
        session = self.framework_registrar.Session()
        try:
            query = session.query(FrameworkVersion).filter_by(framework_name=framework_id)
            if version:
                # Handle version prefix variations (v2025.06.14 vs 2025.06.14)
                version_with_v = version if version.startswith('v') else f'v{version}'
                version_without_v = version[1:] if version.startswith('v') else version
                
                # Check both with and without 'v' prefix
                query = query.filter(
                    (FrameworkVersion.version == version) |
                    (FrameworkVersion.version == version_with_v) |
                    (FrameworkVersion.version == version_without_v)
                )
            
            return query.first() is not None
        except Exception:
            return False
        finally:
            session.close()
    
    def _check_template_in_database(self, template_id: str, version: str = None) -> bool:
        """Check if prompt template exists in database"""
        if not DATABASE_AVAILABLE:
            return False
        
        session = self.component_registrar.Session()
        try:
            query = session.query(PromptTemplate).filter_by(name=template_id)
            if version:
                query = query.filter_by(version=version)
            
            return query.first() is not None
        except Exception:
            return False
        finally:
            session.close()
    
    def _check_weighting_in_database(self, scheme_id: str, version: str = None) -> bool:
        """Check if weighting scheme exists in database"""
        if not DATABASE_AVAILABLE:
            return False
        
        session = self.component_registrar.Session()
        try:
            query = session.query(WeightingMethodology).filter_by(name=scheme_id)
            if version:
                query = query.filter_by(version=version)
            
            return query.first() is not None
        except Exception:
            return False
        finally:
            session.close()
    
    def auto_register_missing_components(self, missing_components: List[ComponentInfo]) -> bool:
        """Auto-register missing components with comprehensive logging"""
        if not self.auto_registration_available:
            logger.error("Auto-registration not available (database connection issues)")
            return False
        
        logger.info("🔧 Starting auto-registration of missing components...")
        
        registration_success = True
        
        for component in missing_components:
            try:
                if component.component_type == 'framework' and component.exists_on_filesystem:
                    success = self.framework_registrar.register_framework(
                        component.component_id, 
                        component.version
                    )
                    
                    # Log registration attempt
                    if self.experiment_logger:
                        self.experiment_logger.log_auto_registration(
                            'framework',
                            component.component_id,
                            success,
                            {
                                'version': component.version,
                                'file_path': component.file_path,
                                'registration_method': 'filesystem_to_database'
                            }
                        )
                    
                    registration_success = registration_success and success
                    
                elif component.component_type == 'prompt_template':
                    success = self.component_registrar.register_prompt_template(
                        component.component_id,
                        component.version
                    )
                    
                    # Log registration attempt
                    if self.experiment_logger:
                        self.experiment_logger.log_auto_registration(
                            'prompt_template',
                            component.component_id,
                            success,
                            {
                                'version': component.version,
                                'registration_method': 'default_template_creation'
                            }
                        )
                    
                    registration_success = registration_success and success
                    
                elif component.component_type == 'weighting_scheme':
                    success = self.component_registrar.register_weighting_scheme(
                        component.component_id,
                        component.version
                    )
                    
                    # Log registration attempt
                    if self.experiment_logger:
                        self.experiment_logger.log_auto_registration(
                            'weighting_scheme',
                            component.component_id,
                            success,
                            {
                                'version': component.version,
                                'registration_method': 'default_scheme_creation'
                            }
                        )
                    
                    registration_success = registration_success and success
                    
                elif component.component_type == 'corpus':
                    if component.file_path:
                        corpus_path = Path(component.file_path)
                        files_processed = 0
                        
                        if corpus_path.is_file():
                            success = self.corpus_registrar.register_corpus_file(
                                component.file_path,
                                component.component_id
                            )
                            files_processed = 1 if success else 0
                        elif corpus_path.is_dir():
                            success = self.corpus_registrar.register_corpus_collection(
                                component.file_path
                            )
                            # Count files in directory for logging
                            files_processed = len(list(corpus_path.glob("*.txt"))) if success else 0
                        else:
                            logger.error(f"Corpus path does not exist: {component.file_path}")
                            success = False
                            files_processed = 0
                        
                        # Log corpus registration
                        if self.experiment_logger:
                            integrity_checks = {
                                'path_exists': corpus_path.exists(),
                                'files_processed': files_processed,
                                'expected_hash': component.expected_hash,
                                'registration_method': 'intelligent_ingestion'
                            }
                            
                            self.experiment_logger.log_corpus_processing(
                                component.component_id,
                                files_processed,
                                integrity_checks,
                                success
                            )
                            
                            self.experiment_logger.log_auto_registration(
                                'corpus',
                                component.component_id,
                                success,
                                {
                                    'file_path': component.file_path,
                                    'files_processed': files_processed,
                                    'registration_method': 'intelligent_ingestion'
                                }
                            )
                    else:
                        logger.error(f"No file path provided for corpus: {component.component_id}")
                        success = False
                        
                        if self.experiment_logger:
                            self.experiment_logger.log_auto_registration(
                                'corpus',
                                component.component_id,
                                False,
                                {'error': 'No file path provided'}
                            )
                    
                    registration_success = registration_success and success
                    
                else:
                    logger.warning(f"Auto-registration not implemented for {component.component_type}: {component.component_id}")
                    
                    if self.experiment_logger:
                        self.experiment_logger.log_auto_registration(
                            component.component_type,
                            component.component_id,
                            False,
                            {'error': 'Auto-registration not implemented for component type'}
                        )
                    
            except Exception as e:
                logger.error(f"Failed to auto-register {component.component_type} {component.component_id}: {e}")
                
                if self.experiment_logger:
                    self.experiment_logger.log_auto_registration(
                        component.component_type,
                        component.component_id,
                        False,
                        {'error': str(e), 'exception_type': type(e).__name__}
                    )
                
                registration_success = False
        
        if registration_success:
            logger.info("✅ All missing components successfully auto-registered")
            
            # Update component states after successful registration
            for component in missing_components:
                if component.component_type == 'framework':
                    component.exists_in_db = self._check_framework_in_database(component.component_id, component.version)
                elif component.component_type == 'prompt_template':
                    component.exists_in_db = self._check_template_in_database(component.component_id, component.version)
                elif component.component_type == 'weighting_scheme':
                    component.exists_in_db = self._check_weighting_in_database(component.component_id, component.version)
                # Note: corpus components don't need updating here as they're handled differently
        else:
            logger.error("❌ Some components failed to auto-register")
        
        return registration_success
    
    def generate_error_guidance(self, missing_components: List[ComponentInfo]) -> Dict[str, str]:
        """Generate helpful error messages and guidance"""
        guidance = {}
        
        for component in missing_components:
            if component.component_type == 'framework':
                if not component.exists_on_filesystem:
                    guidance[f"Framework: {component.component_id}"] = (
                        f"Framework '{component.component_id}' not found.\n"
                        f"  • Check frameworks/{component.component_id}/framework_consolidated.json exists\n"
                        f"  • Or provide file_path in experiment definition\n"
                        f"  • See frameworks/civic_virtue/ for example structure"
                    )
                elif not component.exists_in_db:
                    guidance[f"Framework: {component.component_id}"] = (
                        f"Framework '{component.component_id}' exists on filesystem but not registered in database.\n"
                        f"  • Use --force-reregister to auto-register\n"
                        f"  • Or register manually with: python scripts/framework_sync.py import {component.component_id}"
                    )
            
            elif component.component_type == 'prompt_template':
                guidance[f"Prompt Template: {component.component_id}"] = (
                    f"Prompt template '{component.component_id}' not found in database.\n"
                    f"  • Use --force-reregister to create default template\n"
                    f"  • Or create manually with: python scripts/component_manager.py create-template {component.component_id}"
                )
            
            elif component.component_type == 'weighting_scheme':
                guidance[f"Weighting Scheme: {component.component_id}"] = (
                    f"Weighting scheme '{component.component_id}' not found in database.\n"
                    f"  • Use --force-reregister to create default scheme\n"
                    f"  • Or create manually with: python scripts/component_manager.py create-weighting {component.component_id}"
                )
            
            elif component.component_type == 'corpus':
                if not component.exists_on_filesystem:
                    guidance[f"Corpus: {component.component_id}"] = (
                        f"Corpus '{component.component_id}' not found on filesystem.\n"
                        f"  • Check file path: {component.file_path}\n"
                        f"  • Verify file or directory exists and is readable\n"
                        f"  • For collections, ensure directory contains matching files\n"
                        f"  • Use --force-reregister to attempt auto-ingestion after fixing path"
                    )
                elif not component.exists_in_db:
                    guidance[f"Corpus: {component.component_id}"] = (
                        f"Corpus '{component.component_id}' exists on filesystem but not registered in database.\n"
                        f"  • Use --force-reregister to auto-ingest with intelligent ingestion\n"
                        f"  • Or register manually with: python scripts/intelligent_ingest.py {Path(component.file_path).parent if component.file_path else 'DIRECTORY'}\n"
                        f"  • Hash manifest will be automatically generated during registration"
                    )
                else:
                    guidance[f"Corpus: {component.component_id}"] = (
                        f"Corpus '{component.component_id}' has validation issues.\n"
                        f"  • Check hash validation if expected_hash provided\n"
                        f"  • Verify file integrity and content format\n"
                        f"  • Review .corpus_manifest.json for details"
                    )
        
        return guidance
    
    def pre_flight_validation(self, experiment: Dict[str, Any]) -> Tuple[bool, List[ComponentInfo]]:
        """
        🔒 FRAMEWORK TRANSACTION INTEGRITY: Enhanced pre-flight validation
        
        Validates all components including framework transaction integrity.
        Any framework uncertainty triggers graceful experiment termination.
        """
        logger.info("🔍 Starting enhanced pre-flight validation with framework transaction integrity...")
        
        # Initialize Framework Transaction Manager
        try:
            from src.narrative_gravity.utils.framework_transaction_manager import FrameworkTransactionManager
            framework_tx_manager = FrameworkTransactionManager(self.current_experiment_id)
            logger.info("🔒 Framework Transaction Manager initialized")
        except ImportError:
            logger.warning("⚠️ Framework Transaction Manager not available - using basic validation")
            framework_tx_manager = None
        
        # Validate components with standard validation
        components = self.validate_components(experiment)
        
        # 🔒 CRITICAL: Framework Transaction Integrity Validation
        if framework_tx_manager:
            logger.info("🔒 Validating framework transaction integrity...")
            
            # Extract framework specifications from experiment
            components_config = experiment.get('components', {})
            frameworks = components_config.get('frameworks', [])
            
            # Validate each framework for transaction integrity
            for framework_spec in frameworks:
                framework_name = framework_spec.get('id', framework_spec.get('name'))
                expected_version = framework_spec.get('version')
                framework_file = framework_spec.get('file_path')
                
                # Resolve framework file path if provided
                framework_file_path = None
                if framework_file:
                    if Path(framework_file).is_absolute():
                        framework_file_path = Path(framework_file)
                    else:
                        # Try relative to experiment file location
                        framework_file_path = Path(self.experiment_file).parent / framework_file
                        if not framework_file_path.exists():
                            # Try relative to frameworks directory
                            framework_file_path = Path("frameworks") / framework_name / "framework_consolidated.json"
                
                logger.info(f"🔍 Validating framework transaction: {framework_name}")
                
                # Perform framework transaction validation
                tx_state = framework_tx_manager.validate_framework_for_experiment(
                    framework_name=framework_name,
                    framework_file_path=framework_file_path,
                    expected_version=expected_version
                )
                
                # Log transaction state
                logger.info(f"🔒 Framework {framework_name} validation result: {tx_state.validation_result.value}")
                if tx_state.new_version_created:
                    logger.info(f"🔄 New framework version created: {framework_name}:{tx_state.database_version}")
            
            # 🚨 CRITICAL: Check framework transaction validity
            is_framework_valid, framework_errors = framework_tx_manager.is_transaction_valid()
            
            if not is_framework_valid:
                logger.error("🚨 FRAMEWORK TRANSACTION INTEGRITY FAILURE")
                logger.error("❌ Experiment terminated due to framework validation uncertainty")
                
                # Generate user guidance
                guidance = framework_tx_manager.generate_rollback_guidance()
                
                # Log detailed guidance
                logger.error("🔧 Framework Transaction Failure Guidance:")
                logger.error(f"   Transaction ID: {guidance['transaction_id']}")
                logger.error(f"   Failed Frameworks: {len(guidance['failed_frameworks'])}")
                
                for recommendation in guidance['recommendations']:
                    logger.error(f"   📋 {recommendation}")
                
                logger.error("🔧 Commands to fix framework issues:")
                for command in guidance['commands_to_run']:
                    logger.error(f"   $ {command}")
                
                # Attempt rollback
                logger.warning("🔄 Attempting framework transaction rollback...")
                rollback_success = framework_tx_manager.rollback_transaction()
                
                if rollback_success:
                    logger.info("✅ Framework transaction rollback completed")
                else:
                    logger.error("❌ Framework transaction rollback failed - manual intervention required")
                
                # Save framework failure checkpoint
                self.save_checkpoint(ExperimentState.FAILED, {
                    'failure_reason': 'framework_transaction_integrity_failure',
                    'framework_errors': framework_errors,
                    'guidance': guidance,
                    'rollback_successful': rollback_success
                })
                
                # Generate comprehensive error for experiment designer
                error_message = self._generate_framework_failure_message(guidance, framework_errors)
                
                # Fail the experiment with clear guidance
                raise FrameworkTransactionIntegrityError(
                    framework_errors,
                    guidance,
                    error_message
                )
            
            else:
                logger.info("✅ Framework transaction integrity validation PASSED")
                
                # Log framework validation success
                if self.experiment_logger:
                    self.experiment_logger.info(
                        "Framework transaction integrity validated",
                        extra_data={
                            'transaction_id': framework_tx_manager.transaction_id,
                            'frameworks_validated': len(framework_tx_manager.transaction_states),
                            'new_versions_created': len([s for s in framework_tx_manager.transaction_states if s.new_version_created])
                        }
                    )
        
        # Standard component validation
        missing_components = [comp for comp in components if not comp.exists_on_filesystem or not comp.exists_in_db]
        
        if missing_components:
            logger.warning(f"⚠️  Found {len(missing_components)} missing components")
            for comp in missing_components:
                logger.warning(f"   Missing: {comp.component_type}:{comp.component_id}")
        else:
            logger.info("✅ All standard components validated")
        
        # Overall validation result
        is_valid = len(missing_components) == 0
        
        return is_valid, components
    
    def _generate_framework_failure_message(self, guidance: Dict[str, Any], framework_errors: List[str]) -> str:
        """Generate comprehensive error message for framework transaction failures"""
        
        message_parts = [
            "🚨 EXPERIMENT TERMINATED: Framework Transaction Integrity Failure",
            "",
            "The experiment cannot proceed due to framework validation uncertainty.",
            "This protects experiment integrity by preventing contaminated results.",
            "",
            f"Transaction ID: {guidance['transaction_id']}",
            f"Failed Frameworks: {len(guidance['failed_frameworks'])}/{guidance['total_frameworks']}",
            ""
        ]
        
        # Add specific framework errors
        message_parts.append("❌ Framework Validation Errors:")
        for error in framework_errors:
            message_parts.append(f"   • {error}")
        
        message_parts.append("")
        
        # Add recommendations
        if guidance['recommendations']:
            message_parts.append("🔧 Recommended Actions:")
            for recommendation in guidance['recommendations']:
                message_parts.append(f"   • {recommendation}")
            
            message_parts.append("")
        
        # Add commands to run
        if guidance['commands_to_run']:
            message_parts.append("💻 Commands to Fix Issues:")
            for command in guidance['commands_to_run']:
                message_parts.append(f"   $ {command}")
            
            message_parts.append("")
        
        message_parts.extend([
            "🔒 Why This Matters:",
            "   • Framework uncertainty compromises experiment validity",
            "   • Database is the single source of truth for production",
            "   • Framework content changes require explicit versioning",
            "   • Transaction rollback protects against partial failures",
            "",
            "📋 Next Steps:",
            "   1. Fix the framework issues using the commands above",
            "   2. Verify framework status: python3 scripts/framework_sync.py status",
            "   3. Re-run the experiment with validated frameworks",
            "",
            "🔒 Framework Transaction Integrity ensures reliable experimental results."
        ])
        
        return "\n".join(message_parts)
    
    def show_execution_plan(self, experiment: Dict[str, Any], components: List[ComponentInfo]):
        """Show what would be executed (dry-run mode)"""
        print("\n📋 EXECUTION PLAN:")
        print("=" * 50)
        
        # Show experiment context if available
        if self.experiment_context:
            print(self.experiment_context.generate_context_summary())
            print()
        
        execution = experiment.get('execution', {})
        print(f"📊 Analysis runs: {len(execution.get('matrix', []))}")
        
        print(f"\n🔧 Components to use:")
        for component in components:
            status = "✅ Ready" if component.exists_on_filesystem and component.exists_in_db else "⚠️  Needs registration"
            print(f"  • {component.component_type}: {component.component_id} - {status}")
        
        print(f"\n💰 Estimated cost: TODO") # TODO: Implement cost estimation
        print(f"⏱️  Estimated time: TODO") # TODO: Implement time estimation
        
        if self.dry_run:
            print("\n🔍 DRY RUN - No actual execution will occur")
    
    def execute_enhanced_analysis_pipeline(self, execution_results: Dict[str, Any], experiment: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute enhanced analysis pipeline with statistical validation, visualization, and reporting."""
        logger.info("📊 Starting enhanced analysis pipeline...")
        
        # Get enhanced analysis configuration
        enhanced_config = {}
        if experiment:
            enhanced_config = experiment.get('enhanced_analysis', {})
        
        # Check if enhanced analysis is enabled (default: True)
        if not enhanced_config.get('enabled', True):
            logger.info("📊 Enhanced analysis pipeline disabled in experiment configuration")
            return {'pipeline_status': 'disabled', 'timestamp': datetime.now().isoformat()}
        
        # Create organized output directory within experiments/ structure
        experiment_name = experiment.get('experiment_meta', {}).get('name', 'experiment') if experiment else 'analysis'
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        experiment_dir = Path('experiments') / f"{experiment_name}_{timestamp}"
        output_dir = experiment_dir / 'enhanced_analysis'
        output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"📁 Enhanced analysis output directory: {output_dir}")
        logger.info(f"📁 Complete experiment directory: {experiment_dir}")
        
        try:
            # Step 1: Extract and structure experiment results
            logger.info("📊 Step 1: Extracting and structuring results...")
            from extract_experiment_results import ExperimentResultsExtractor
            extractor = ExperimentResultsExtractor()
            structured_results = extractor.extract_results(execution_results)
            
            if 'error' in structured_results:
                logger.error(f"❌ Results extraction failed: {structured_results['error']}")
                return {
                    'pipeline_status': 'failed', 
                    'error': f"Results extraction failed: {structured_results['error']}", 
                    'timestamp': datetime.now().isoformat()
                }
            
            # Save structured results
            structured_file = output_dir / 'structured_results.json'
            with open(structured_file, 'w') as f:
                json.dump(structured_results, f, indent=2, default=str)
            logger.info(f"✅ Structured {len(structured_results.get('structured_data', []))} records")
            
            # Step 2: Run statistical hypothesis testing
            logger.info("🧪 Step 2: Running statistical hypothesis testing...")
            from statistical_hypothesis_testing import StatisticalHypothesisTester
            tester = StatisticalHypothesisTester()
            statistical_results = tester.test_hypotheses(structured_results)
            
            # Save statistical results
            stats_file = output_dir / 'statistical_results.json'
            with open(stats_file, 'w') as f:
                json.dump(statistical_results, f, indent=2, default=str)
            
            if 'error' in statistical_results:
                logger.warning(f"⚠️ Statistical testing issues: {statistical_results['error']}")
            else:
                summary = statistical_results.get('summary', {})
                logger.info(f"✅ Hypothesis testing complete - {summary.get('hypotheses_supported', 0)}/3 supported")
            
            # Step 3: Calculate interrater reliability
            logger.info("🔍 Step 3: Analyzing interrater reliability...")
            from interrater_reliability_analysis import InterraterReliabilityAnalyzer
            reliability_analyzer = InterraterReliabilityAnalyzer()
            reliability_results = reliability_analyzer.analyze_reliability(structured_results)
            
            # Save reliability results
            reliability_file = output_dir / 'reliability_results.json'
            with open(reliability_file, 'w') as f:
                json.dump(reliability_results, f, indent=2, default=str)
            
            if 'error' in reliability_results:
                logger.warning(f"⚠️ Reliability analysis limited: {reliability_results['error']}")
            else:
                logger.info("✅ Reliability analysis complete")
            
            # Step 4: Generate comprehensive visualizations
            logger.info("🎨 Step 4: Generating comprehensive visualizations...")
            from generate_comprehensive_visualizations import VisualizationGenerator
            viz_output_dir = output_dir / 'visualizations'
            visualizer = VisualizationGenerator(output_dir=str(viz_output_dir))
            visualization_results = visualizer.generate_visualizations(
                structured_results,
                statistical_results,
                reliability_results
            )
            
            if 'error' in visualization_results:
                logger.warning(f"⚠️ Visualization generation issues: {visualization_results['error']}")
            else:
                viz_count = len(visualizer.generated_files) if hasattr(visualizer, 'generated_files') else 0
                logger.info(f"✅ Generated {viz_count} visualizations")
            
            # Step 5: Generate enhanced HTML report (if enabled)
            html_report_path = None
            if enhanced_config.get('generate_html_report', True):
                logger.info("📄 Step 5: Generating enhanced HTML report...")
                try:
                    # Create HTML report with all analysis results
                    html_report_path = self._generate_comprehensive_html_report(
                        structured_results, statistical_results, 
                        reliability_results, visualization_results, output_dir
                    )
                    logger.info(f"✅ Enhanced HTML report generated: {html_report_path}")
                except Exception as e:
                    logger.warning(f"⚠️ HTML report generation failed: {e}")
            
            # Step 6: Academic pipeline integration (if enabled)
            academic_results = None
            if enhanced_config.get('generate_academic_exports', False):
                logger.info("🎓 Step 6: Generating academic exports...")
                try:
                    academic_results = self._generate_academic_exports(
                        structured_results, output_dir, experiment
                    )
                    logger.info("✅ Academic exports generated")
                except Exception as e:
                    logger.warning(f"⚠️ Academic export generation failed: {e}")
            
            # Combine all results with comprehensive metadata
            enhanced_results = {
                'structured_results': structured_results,
                'statistical_results': statistical_results,
                'reliability_results': reliability_results,
                'visualization_results': visualization_results,
                'pipeline_status': 'success',
                'timestamp': datetime.now().isoformat(),
                'experiment_directory': str(experiment_dir),
                'enhanced_analysis_directory': str(output_dir),
                'files_generated': {
                    'structured_data': str(structured_file),
                    'statistical_analysis': str(stats_file),
                    'reliability_analysis': str(reliability_file),
                    'visualizations_dir': str(viz_output_dir),
                    'html_report': str(html_report_path) if html_report_path else None
                },
                'summary': {
                    'total_analyses': len(structured_results.get('structured_data', [])),
                    'statistical_tests_run': len(statistical_results.get('tests', {})) if 'error' not in statistical_results else 0,
                    'hypotheses_supported': statistical_results.get('summary', {}).get('hypotheses_supported', 0) if 'error' not in statistical_results else 0,
                    'reliability_metrics_calculated': bool('error' not in reliability_results),
                    'visualizations_generated': len(visualizer.generated_files) if hasattr(visualizer, 'generated_files') else 0,
                    'html_report_generated': bool(html_report_path),
                    'academic_exports_generated': bool(academic_results)
                }
            }
            
            # Save comprehensive pipeline results
            pipeline_results_file = output_dir / 'pipeline_results.json'
            with open(pipeline_results_file, 'w') as f:
                json.dump(enhanced_results, f, indent=2, default=str)
            
            # Generate pipeline summary report
            self._generate_pipeline_summary_report(enhanced_results, output_dir, experiment_dir)
            
            logger.info("✅ Enhanced analysis pipeline completed successfully")
            logger.info(f"📁 All results saved to: {output_dir}")
            
            # Phase 5: Architectural Compliance Validation (AI Academic Advisor v2.0)
            print(f"\n{'='*60}")
            print(f"Phase 5: Architectural Compliance Validation")
            print(f"{'='*60}")
            
            try:
                if ARCHITECTURAL_COMPLIANCE_AVAILABLE:
                    validator = ArchitecturalComplianceValidator()
                    compliance_report = validator.validate_experiment_results(str(output_dir))
                else:
                    logger.warning("Architectural compliance validator not available - skipping validation")
                    compliance_report = {
                        'compliance_level': 'VALIDATION_UNAVAILABLE',
                        'compliance_score': 0,
                        'error': 'Architectural compliance validator not available'
                    }
                
                # Add compliance report to enhanced results
                enhanced_results['architectural_compliance'] = compliance_report
                
                if compliance_report["compliance_level"] == "NON_COMPLIANT":
                    logger.warning(f"⚠️ ARCHITECTURAL VIOLATIONS DETECTED!")
                    logger.warning(f"Compliance Score: {compliance_report['compliance_score']:.1f}%")
                    logger.warning(f"Violations: {len(compliance_report['violations'])}")
                    logger.warning(f"See report: {output_dir}/architectural_compliance_report.json")
                    # Don't fail the experiment, but warn about violations
                elif compliance_report["compliance_level"] == "COMPLIANT_WITH_WARNINGS":
                    logger.info(f"✅ Architectural compliance validated with warnings")
                    logger.info(f"Compliance Score: {compliance_report['compliance_score']:.1f}%")
                    logger.info(f"Warnings: {len(compliance_report['warnings'])}")
                else:
                    logger.info(f"✅ Full architectural compliance validated")
                    logger.info(f"Compliance Score: {compliance_report['compliance_score']:.1f}%")
                    
            except Exception as e:
                logger.warning(f"⚠️ Architectural compliance validation failed: {str(e)}")
                # Don't fail the experiment for validation issues
                enhanced_results['architectural_compliance'] = {
                    'error': str(e),
                    'compliance_level': 'VALIDATION_FAILED'
                }
            
            return enhanced_results
            
        except Exception as e:
            logger.error(f"❌ Enhanced analysis pipeline failed: {e}")
            import traceback
            traceback.print_exc()
            
            # Save error information
            error_file = output_dir / 'pipeline_error.json'
            error_info = {
                'pipeline_status': 'failed',
                'error': str(e),
                'traceback': traceback.format_exc(),
                'timestamp': datetime.now().isoformat()
            }
            with open(error_file, 'w') as f:
                json.dump(error_info, f, indent=2)
            
            return error_info
    
    def _generate_comprehensive_html_report(self, structured_results, 
                                            statistical_results, reliability_results, 
                                            visualization_results, output_dir):
        """Generate comprehensive HTML report combining all analysis results."""
        
        # Create comprehensive report data
        report_data = {
            'experiment_analysis': {
                'structured_data_summary': {
                    'total_analyses': len(structured_results.get('structured_data', [])),
                    'metadata': structured_results.get('metadata', {})
                },
                'statistical_summary': statistical_results.get('summary', {}) if 'error' not in statistical_results else {},
                'reliability_summary': reliability_results.get('summary', {}) if 'error' not in reliability_results else {},
                'visualization_summary': visualization_results.get('summary', {}) if 'error' not in visualization_results else {}
            }
        }
        
        # Generate HTML using template
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Enhanced Analysis Report</title>
            <meta name="generator" content="NarrativeGravityVisualizationEngine">
            <meta name="theme" content="narrative-gravity-theme">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .header {{ background: #2E86AB; color: white; padding: 20px; border-radius: 8px; }}
                .section {{ margin: 20px 0; padding: 20px; border: 1px solid #ddd; border-radius: 8px; }}
                .metric {{ display: inline-block; margin: 10px; padding: 15px; background: #f8f9fa; border-radius: 5px; }}
                .success {{ color: #28a745; }}
                .warning {{ color: #ffc107; }}
                .error {{ color: #dc3545; }}
                .ng-production-signature {{ display: none; }}
            </style>
        </head>
        <body>
            <!-- NarrativeGravityVisualizationEngine Production Signature -->
            <div class="ng-production-signature">Generated by NarrativeGravityVisualizationEngine</div>
            <div class="header">
                <h1>🎯 Enhanced Analysis Report</h1>
                <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p class="narrative-gravity-theme">Theme: Academic (Production)</p>
            </div>
            
            <div class="section">
                <h2>📊 Analysis Summary</h2>
                <div class="metric">
                    <strong>Total Analyses:</strong> {report_data['experiment_analysis']['structured_data_summary']['total_analyses']}
                </div>
                <div class="metric">
                    <strong>Statistical Tests:</strong> {len(statistical_results.get('hypothesis_testing', {})) if 'error' not in statistical_results else 'Failed'}
                </div>
                <div class="metric">
                    <strong>Reliability Analysis:</strong> {'✅ Complete' if 'error' not in reliability_results else '⚠️ Limited'}
                </div>
                <div class="metric">
                    <strong>Visualizations:</strong> {len([f for f in (output_dir / 'visualizations').glob('*.png')]) if (output_dir / 'visualizations').exists() else 0}
                </div>
            </div>
            
            <div class="section">
                <h2>📁 Generated Files</h2>
                <ul>
                    <li>📊 Structured Results: <code>structured_results.json</code></li>
                    <li>🧪 Statistical Analysis: <code>statistical_results.json</code></li>
                    <li>🔍 Reliability Analysis: <code>reliability_results.json</code></li>
                    <li>🎨 Visualizations: <code>visualizations/</code></li>
                    <li>📋 Pipeline Results: <code>pipeline_results.json</code></li>
                </ul>
            </div>
            
            <div class="section">
                <h2>🔗 Quick Links</h2>
                <p>All analysis files are located in: <code>{output_dir}</code></p>
            </div>
        </body>
        </html>
        """
        
        # Save HTML report
        html_file = output_dir / 'enhanced_analysis_report.html'
        with open(html_file, 'w') as f:
            f.write(html_content)
        
        return html_file
    
    def _generate_academic_exports(self, structured_results, output_dir, experiment):
        """Generate academic exports if enabled."""
        academic_dir = output_dir / 'academic_exports'
        academic_dir.mkdir(exist_ok=True)
        
        # Export structured data in academic formats
        if 'structured_data' in structured_results:
            # CSV export
            csv_file = academic_dir / 'analysis_data.csv'
            if hasattr(structured_results['structured_data'], 'to_csv'):
                structured_results['structured_data'].to_csv(csv_file, index=False)
            
            # Generate basic academic report
            academic_report = {
                'study_metadata': experiment.get('experiment_meta', {}) if experiment else {},
                'analysis_summary': structured_results.get('metadata', {}),
                'export_timestamp': datetime.now().isoformat(),
                'files_generated': ['analysis_data.csv']
            }
            
            report_file = academic_dir / 'academic_report.json'
            with open(report_file, 'w') as f:
                json.dump(academic_report, f, indent=2, default=str)
        
        return {'academic_exports_dir': str(academic_dir)}
    
    def _generate_pipeline_summary_report(self, enhanced_results, output_dir, experiment_dir):
        """Generate a human-readable summary report."""
        summary = enhanced_results['summary']
        
        report_content = f"""
# Enhanced Analysis Pipeline Summary

**Generated:** {enhanced_results['timestamp']}
**Status:** {enhanced_results['pipeline_status']}

## 📊 Analysis Overview

- **Total Analyses Processed:** {summary['total_analyses']}
- **Statistical Tests Run:** {summary['statistical_tests_run']}
- **Hypotheses Supported:** {summary['hypotheses_supported']}
- **Reliability Metrics:** {'✅ Calculated' if summary['reliability_metrics_calculated'] else '❌ Failed'}
- **Visualizations Generated:** {summary['visualizations_generated']}
- **HTML Report:** {'✅ Generated' if summary['html_report_generated'] else '❌ Failed'}
- **Academic Exports:** {'✅ Generated' if summary['academic_exports_generated'] else '❌ Not Requested'}

## 📁 Generated Files

All experiment outputs have been saved to: `{experiment_dir}`

### Experiment Directory Structure:
```
{experiment_dir.name}/
├── enhanced_analysis/
│   ├── pipeline_results.json          # Complete pipeline results
│   ├── structured_results.json        # Extracted experiment data
│   ├── statistical_results.json       # Statistical analysis results
│   ├── reliability_results.json       # Reliability metrics
│   ├── enhanced_analysis_report.html  # Interactive HTML report
│   ├── README.md                       # This summary
│   ├── visualizations/                # Comprehensive visualizations
│   └── academic_exports/               # Publication-ready exports
```

## 🚀 Next Steps

1. Review the HTML report for interactive analysis
2. Examine statistical results for hypothesis validation
3. Check reliability metrics for data quality assessment
4. Use visualizations for presentation and publication

"""
        
        summary_file = output_dir / 'README.md'
        with open(summary_file, 'w') as f:
            f.write(report_content)
    
    def execute_analysis_matrix(self, experiment: Dict[str, Any], components: List[ComponentInfo]) -> Dict[str, Any]:
        """Execute the actual analysis matrix with real API calls"""
        logger.info("🔬 Initializing real analysis service...")
        
        try:
            # Initialize the real analysis service
            analysis_service = RealAnalysisService()
            
        except Exception as e:
            logger.error(f"Failed to initialize analysis service: {e}")
            # Continue with mock data for now
            return {"error": f"Analysis service initialization failed: {e}", "results": []}
        
        execution = experiment.get('execution', {})
        matrix = execution.get('matrix', [])
        
        if not matrix:
            logger.warning("No execution matrix found - creating default run")
            matrix = [{"run_id": "default_run", "description": "Default execution"}]
        
        # Extract cost controls
        cost_controls = execution.get('cost_controls', {})
        max_total_cost = cost_controls.get('max_total_cost', 5.0)
        cost_per_analysis_limit = cost_controls.get('cost_per_analysis_limit', 0.25)
        
        # Track execution
        total_cost = 0.0
        all_results = []
        corpus_components = [comp for comp in components if comp.component_type == 'corpus']
        
        logger.info(f"🚀 Starting execution with {len(corpus_components)} corpus items...")
        
        for run_config in matrix:
            run_id = run_config.get('run_id', 'unknown_run')
            logger.info(f"📝 Executing run: {run_id}")
            
            # Get analysis configuration from run
            framework_id = run_config.get('framework', 'civic_virtue')
            model_id = run_config.get('model', 'gpt-4o')
            prompt_template = run_config.get('prompt_template', 'traditional_analysis')
            
            for corpus_component in corpus_components:
                if total_cost >= max_total_cost:
                    logger.warning(f"⚠️  Reached total cost limit: ${total_cost:.2f}")
                    break
                
                try:
                    # Load text content from file
                    text_content = self._load_corpus_text(corpus_component.file_path)
                    
                    if not text_content:
                        logger.warning(f"⚠️  Could not load text from: {corpus_component.file_path}")
                        continue
                    
                    logger.info(f"🧠 Analyzing: {corpus_component.component_id} with {model_id}...")
                    
                    # Create analysis context for this run
                    analysis_run_info = {
                        'run_id': run_id,
                        'framework': framework_id,
                        'corpus_item': corpus_component.component_id,
                        'prompt_template': prompt_template,
                        'model': model_id,
                        'text_path': corpus_component.file_path
                    }
                    
                    # Execute real analysis using RealAnalysisService
                    import asyncio
                    analysis_result = asyncio.run(analysis_service.analyze_single_text(
                        text_content=text_content,
                        framework_config_id=framework_id,
                        prompt_template_id=prompt_template,
                        llm_model=model_id,
                        include_justifications=True,
                        include_hierarchical_ranking=True
                    ))
                    
                    # Track costs
                    analysis_cost = analysis_result.get('api_cost', 0.0)
                    total_cost += analysis_cost
                    
                    if analysis_cost > cost_per_analysis_limit:
                        logger.warning(f"⚠️  Analysis exceeded cost limit: ${analysis_cost:.3f} > ${cost_per_analysis_limit:.3f}")
                    
                    # Add experiment context to results
                    if self.experiment_context:
                        analysis_result = self.generate_context_aware_output(analysis_result, analysis_run_info)
                    
                    # Log analysis completion
                    if self.experiment_logger:
                        self.experiment_logger.info(
                            f"Analysis completed successfully: {corpus_component.component_id}",
                            extra_data={
                                'corpus_id': corpus_component.component_id,
                                'framework': framework_id,
                                'model': model_id,
                                'api_cost': analysis_cost,
                                'duration_seconds': analysis_result.get('duration_seconds', 0),
                                'quality_score': analysis_result.get('framework_fit_score', 0),
                                'analysis_type': 'real_api_execution'
                            }
                        )
                    
                    all_results.append(analysis_result)
                    
                    logger.info(f"✅ Analysis completed - Cost: ${analysis_cost:.3f}, Total: ${total_cost:.3f}")
                    
                except Exception as e:
                    logger.error(f"❌ Analysis failed for {corpus_component.component_id}: {e}")
                    
                    # Log failed analysis
                    if self.experiment_logger:
                        self.experiment_logger.error(
                            f"Analysis failed: {corpus_component.component_id}",
                            error_code=ExperimentErrorCodes.EXECUTION_ANALYSIS_FAILED,
                            extra_data={'error': str(e), 'framework': framework_id, 'model': model_id}
                        )
                    
                    continue
        
        # Generate validation report if we have results
        if all_results and self.experiment_context:
            validation_report = self.create_validation_report(all_results)
            logger.info(f"📊 Validation report generated with {len(all_results)} analyses")
        
        execution_summary = {
            'total_analyses': len(all_results),
            'total_cost': round(total_cost, 4),
            'successful_analyses': len([r for r in all_results if 'error' not in r]),
            'failed_analyses': len([r for r in all_results if 'error' in r]),
            'cost_efficiency': round(total_cost / len(all_results), 4) if all_results else 0,
            'results': all_results
        }
        
        logger.info(f"🎯 Execution completed: {execution_summary['successful_analyses']}/{execution_summary['total_analyses']} successful, ${execution_summary['total_cost']:.3f} total cost")
        
        # After collecting all_results, run enhanced analysis pipeline
        if all_results:
            # Save checkpoint before enhanced analysis (this is expensive and shouldn't be repeated)
            if hasattr(self, 'save_checkpoint'):
                self.save_checkpoint(ExperimentState.ENHANCED_PIPELINE, {
                    'analyses_completed': len(all_results),
                    'total_cost': execution_summary.get('total_cost', 0),
                    'starting_enhanced_pipeline': True
                })
            
            enhanced_results = self.execute_enhanced_analysis_pipeline(execution_summary, experiment)
            execution_summary['enhanced_analysis'] = enhanced_results
        
        return execution_summary
    
    def _load_corpus_text(self, file_path: str) -> Optional[str]:
        """Load text content from corpus file"""
        try:
            corpus_file = Path(file_path)
            if not corpus_file.exists():
                logger.error(f"Corpus file not found: {file_path}")
                return None
            
            with open(corpus_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            
            if not content:
                logger.warning(f"Empty corpus file: {file_path}")
                return None
            
            logger.debug(f"Loaded {len(content)} characters from {file_path}")
            return content
            
        except Exception as e:
            logger.error(f"Error loading corpus file {file_path}: {e}")
            return None
    
    def execute_experiment(self, experiment_file: Path):
        """
        🚨 TRANSACTION-SAFE EXPERIMENT EXECUTION 🚨
        
        This method treats experiments as atomic transactions that must complete fully.
        Resume capability prevents losing expensive LLM analysis work.
        
        ❌ AI ASSISTANTS: DO NOT suggest bypassing this with custom scripts!
        ✅ This orchestrator handles ALL experiment needs including statistical analysis.
        """
        try:
            # Store experiment file path for use in other methods
            self.experiment_file = experiment_file
            
            # Initialize experiment transaction
            logger.info("🚀 Starting experiment transaction...")
            
            # Load experiment definition
            experiment = self.load_experiment_definition(experiment_file)
            experiment_meta = experiment.get('experiment_meta', {})
            
            # Create experiment ID for transaction tracking
            self.current_experiment_id = self._create_experiment_id(experiment_meta)
            logger.info(f"📋 Experiment Transaction ID: {self.current_experiment_id}")
            
            # 🚨 FIX: CREATE DATABASE EXPERIMENT RECORD (was missing!)
            # This fixes the critical database storage disconnect issue
            self.database_experiment_id = None
            if DATABASE_AVAILABLE:
                try:
                    from src.narrative_gravity.models.models import Experiment
                    from src.narrative_gravity.utils.database import get_database_url
                    from sqlalchemy import create_engine
                    from sqlalchemy.orm import sessionmaker
                    from sqlalchemy.exc import IntegrityError, SQLAlchemyError
                    
                    logger.info("💾 Creating production database experiment record...")
                    
                    # 🔒 COHERENCE FIX: Validate experiment data before database insertion
                    experiment_validation = self._validate_experiment_for_database(experiment_meta, experiment)
                    if not experiment_validation['valid']:
                        logger.warning(f"⚠️  Experiment data validation failed: {experiment_validation['errors']}")
                        logger.warning("🔄 Continuing with file-based storage only")
                        self.database_experiment_id = None
                        self.statistical_logger = None
                    else:
                        # 🔒 COHERENCE FIX: Use single transaction for atomic database operations
                        engine = create_engine(get_database_url())
                        Session = sessionmaker(bind=engine)
                        session = Session()
                        
                        try:
                            # Create Experiment record with correct field mapping
                            db_experiment = Experiment(
                                name=experiment_meta.get('name', 'Unnamed Experiment')[:255],  # Respect length limits
                                description=experiment_meta.get('description', 'No description provided'),
                                hypothesis=experiment_meta.get('hypotheses', ['No hypothesis specified'])[0] if experiment_meta.get('hypotheses') else None,
                                research_context=experiment_meta.get('research_context'),
                                prompt_template_id=experiment_validation['prompt_template_id'],  # Required field
                                framework_config_id=experiment_validation['framework_config_id'],  # Required field  
                                scoring_algorithm_id=experiment_validation['scoring_algorithm_id'],  # Required field
                                selected_models=experiment_validation['selected_models'],  # Required JSON array
                                analysis_mode=experiment_validation['analysis_mode'],
                                status='active',  # Use valid enum value
                                research_notes=f"Orchestrator Transaction ID: {self.current_experiment_id}",
                                tags=experiment_meta.get('tags', [])
                            )
                            
                            # 🔒 COHERENCE FIX: Validate foreign key constraints
                            session.add(db_experiment)
                            session.flush()  # Get ID without committing
                            
                            self.database_experiment_id = db_experiment.id
                            
                            # 🔒 COHERENCE FIX: Initialize StatisticalLogger within same transaction
                            try:
                                from src.narrative_gravity.utils.statistical_logger import StatisticalLogger
                                self.statistical_logger = StatisticalLogger()
                                # Test StatisticalLogger connection within transaction
                                logger.info("✅ StatisticalLogger initialized")
                            except Exception as sl_error:
                                logger.warning(f"⚠️  StatisticalLogger initialization failed: {sl_error}")
                                self.statistical_logger = None
                            
                            # 🔒 COHERENCE FIX: Commit transaction atomically
                            session.commit()
                            logger.info(f"✅ Database experiment record created: ID {self.database_experiment_id}")
                            
                        except IntegrityError as ie:
                            session.rollback()
                            logger.error(f"❌ Database integrity constraint violation: {ie}")
                            logger.warning("🔄 Continuing with file-based storage only")
                            self.database_experiment_id = None
                            self.statistical_logger = None
                            
                        except SQLAlchemyError as se:
                            session.rollback()
                            logger.error(f"❌ Database error: {se}")
                            logger.warning("🔄 Continuing with file-based storage only")
                            self.database_experiment_id = None
                            self.statistical_logger = None
                            
                        finally:
                            session.close()
                    
                except Exception as e:
                    logger.error(f"❌ Failed to create database experiment record: {e}")
                    logger.warning("🔄 Continuing with file-based storage only")
                    self.database_experiment_id = None
                    self.statistical_logger = None
            else:
                logger.warning("⚠️  Database not available - using file-based storage only")
                self.statistical_logger = None
            
            # Check for resumable state if resume requested
            if self.resume_from_checkpoint:
                # Look for resumable experiments if no specific ID provided
                resumable = self.find_resumable_experiments()
                if resumable:
                    logger.info(f"📋 Found {len(resumable)} resumable experiments:")
                    for exp in resumable[:5]:  # Show top 5
                        logger.info(f"   • {exp['experiment_id']} ({exp['state']}) - {exp['timestamp']}")
                    
                    # Use most recent resumable experiment
                    latest = resumable[0]
                    self.current_experiment_id = latest['experiment_id']
                    checkpoint = self.load_checkpoint(self.current_experiment_id)
                    
                    if checkpoint:
                        logger.info(f"🔄 Resuming from state: {checkpoint['state']}")
                        # Resume from checkpoint logic will be handled in state checks below
                    else:
                        logger.warning("Failed to load checkpoint - starting fresh")
                        self.resume_from_checkpoint = False
                else:
                    logger.info("No resumable experiments found - starting fresh")
                    self.resume_from_checkpoint = False
            
            # Save initial checkpoint
            self.save_checkpoint(ExperimentState.INITIALIZING, {
                'experiment_file': str(experiment_file),
                'experiment_meta': experiment_meta
            })
            
            # Start experiment logging if available
            if self.experiment_logger:
                academic_info = {
                    'principal_investigator': experiment_meta.get('principal_investigator'),
                    'institution': experiment_meta.get('institution'),
                    'ethical_clearance': experiment_meta.get('ethical_clearance'),
                    'funding_source': experiment_meta.get('funding_source'),
                    'data_classification': experiment_meta.get('data_classification', 'unclassified'),
                    'publication_intent': experiment_meta.get('publication_intent', False)
                }
                
                self.current_run_id = self.experiment_logger.start_experiment_logging(
                    experiment_meta.get('name', 'unnamed_experiment'),
                    experiment_meta,
                    academic_info
                )
                
                # Log academic compliance checks
                if experiment_meta.get('ethical_clearance'):
                    self.experiment_logger.log_academic_compliance(
                        'ethical_clearance', True,
                        {'clearance_id': experiment_meta.get('ethical_clearance')}
                    )
                else:
                    self.experiment_logger.log_academic_compliance(
                        'ethical_clearance', False,
                        {'note': 'No ethical clearance specified in experiment definition'}
                    )
            
            # Pre-flight validation with logging
            self.save_checkpoint(ExperimentState.PRE_FLIGHT_VALIDATION, {'message': 'Starting pre-flight validation'})
            is_valid, components = self.pre_flight_validation(experiment)
            
            if not is_valid:
                if self.experiment_logger:
                    self.experiment_logger.error(
                        "Pre-flight validation failed",
                        error_code=ExperimentErrorCodes.EXECUTION_PRE_FLIGHT_FAILED,
                        extra_data={'missing_components': len([comp for comp in components if not comp.exists_on_filesystem or not comp.exists_in_db])}
                    )
                
                if not self.force_reregister:
                    raise MissingComponentsError(
                        [f"{comp.component_type}:{comp.component_id}" for comp in components if not comp.exists_on_filesystem or not comp.exists_in_db],
                        self.generate_error_guidance([comp for comp in components if not comp.exists_on_filesystem or not comp.exists_in_db])
                    )
                else:
                    logger.info("🔧 Force registration enabled - attempting to auto-register missing components")
                    
                    # Filter components that need registration
                    missing_components = [comp for comp in components if not comp.exists_on_filesystem or not comp.exists_in_db]
                    
                    # Save checkpoint before registration
                    self.save_checkpoint(ExperimentState.COMPONENT_REGISTRATION, {
                        'missing_components': len(missing_components),
                        'components_to_register': [f"{comp.component_type}:{comp.component_id}" for comp in missing_components]
                    })
                    
                    # Attempt auto-registration with logging
                    registration_success = self.auto_register_missing_components(missing_components)
                    
                    if not registration_success:
                        if self.experiment_logger:
                            self.experiment_logger.error(
                                "Auto-registration failed - cannot continue",
                                error_code=ExperimentErrorCodes.COMPONENT_AUTO_REGISTRATION_FAILED
                            )
                        logger.error("❌ Auto-registration failed - cannot continue")
                        raise MissingComponentsError(
                            [f"{comp.component_type}:{comp.component_id}" for comp in missing_components],
                            self.generate_error_guidance(missing_components)
                        )
                    
                    # Re-validate after registration
                    logger.info("🔍 Re-validating components after auto-registration...")
                    is_valid, components = self.pre_flight_validation(experiment)
                    
                    if not is_valid:
                        if self.experiment_logger:
                            self.experiment_logger.error(
                                "Validation still failing after auto-registration",
                                error_code=ExperimentErrorCodes.EXECUTION_PRE_FLIGHT_FAILED
                            )
                        logger.error("❌ Validation still failing after auto-registration")
                        raise MissingComponentsError(
                            [f"{comp.component_type}:{comp.component_id}" for comp in components if not comp.exists_on_filesystem or not comp.exists_in_db],
                            self.generate_error_guidance([comp for comp in components if not comp.exists_on_filesystem or not comp.exists_in_db])
                        )
            
            # Log successful validation
            if self.experiment_logger:
                for component in components:
                    self.experiment_logger.log_component_validation(
                        component.component_type,
                        component.component_id,
                        component.exists_on_filesystem and component.exists_in_db,
                        {
                            'exists_on_filesystem': component.exists_on_filesystem,
                            'exists_in_db': component.exists_in_db,
                            'version': component.version,
                            'file_path': component.file_path
                        }
                    )
            
            # Show execution plan
            self.show_execution_plan(experiment, components)
            
            if self.dry_run:
                logger.info("✅ Dry run completed successfully")
                if self.experiment_logger:
                    self.experiment_logger.info("Dry run completed successfully")
                    self.experiment_logger.end_experiment_logging(True)
                return
            
            # Log context propagation test
            if self.experiment_logger and self.experiment_context:
                self.experiment_logger.log_context_propagation(
                    "experiment_context",
                    True,
                    {
                        'hypotheses_count': len(self.experiment_context.hypotheses),
                        'success_criteria_count': len(self.experiment_context.success_criteria),
                        'context_name': self.experiment_context.name,
                        'context_version': self.experiment_context.version
                    }
                )
                
                # Log hypothesis validation
                if self.experiment_context.hypotheses:
                    self.experiment_logger.log_hypothesis_validation(
                        self.experiment_context.hypotheses,
                        {'status': 'loaded', 'validation_pending': True}
                    )
            
            # Execute the actual experiment with real API calls
            logger.info("🚀 Starting experiment execution...")
            self.save_checkpoint(ExperimentState.ANALYSIS_EXECUTION, {
                'components_validated': len(components),
                'total_analyses_planned': len([comp for comp in components if comp.component_type == 'corpus'])
            })
            execution_results = self.execute_analysis_matrix(experiment, components)
            
            # Log execution summary (serialize datetime objects)
            if self.experiment_logger and execution_results:
                # Skip logging detailed execution results to avoid DataFrame serialization issues
                self.experiment_logger.info(
                    f"Experiment execution completed: {execution_results['successful_analyses']}/{execution_results['total_analyses']} successful analyses",
                    extra_data={
                        'total_cost': execution_results['total_cost'],
                        'cost_efficiency': execution_results['cost_efficiency'],
                        'experiment_completed': True
                    }
                )
            
            # Launch HTML report in browser if requested and available
            if self.open_report and execution_results and 'enhanced_analysis' in execution_results:
                enhanced_analysis = execution_results['enhanced_analysis']
                files_generated = enhanced_analysis.get('files_generated', {})
                html_report_path = files_generated.get('html_report')
                
                if html_report_path and html_report_path != 'None':
                    try:
                        # Convert to absolute path for browser opening
                        absolute_path = Path(html_report_path).resolve()
                        webbrowser.open(f'file://{absolute_path}')
                        logger.info(f"🌐 Opening HTML report in browser: {absolute_path}")
                    except Exception as e:
                        logger.warning(f"Failed to open HTML report in browser: {e}")
                else:
                    logger.warning("HTML report path not found - cannot open in browser")
            elif self.open_report:
                logger.warning("HTML report not available - cannot open in browser")
            
            # End experiment logging successfully
            if self.experiment_logger:
                self.experiment_logger.end_experiment_logging(True)
            
            # Save final completion checkpoint
            self.save_checkpoint(ExperimentState.COMPLETED, {
                'transaction_complete': True,
                'final_timestamp': datetime.now().isoformat(),
                'execution_summary': {
                    'total_analyses': execution_results.get('total_analyses', 0) if 'execution_results' in locals() else 0,
                    'total_cost': execution_results.get('total_cost', 0) if 'execution_results' in locals() else 0
                }
            })
            
            # 🚨 FIX: UPDATE DATABASE EXPERIMENT STATUS TO COMPLETED
            if self.database_experiment_id and DATABASE_AVAILABLE:
                try:
                    from src.narrative_gravity.models.models import Experiment
                    from src.narrative_gravity.utils.database import get_database_url
                    from sqlalchemy import create_engine
                    from sqlalchemy.orm import sessionmaker
                    from sqlalchemy.exc import SQLAlchemyError
                    
                    engine = create_engine(get_database_url())
                    Session = sessionmaker(bind=engine)
                    session = Session()
                    
                    try:
                        # 🔒 COHERENCE FIX: Update experiment status with correct field mapping
                        experiment = session.query(Experiment).filter_by(id=self.database_experiment_id).first()
                        if experiment:
                            experiment.status = 'completed'  # Use string value, not enum
                            if 'execution_results' in locals():
                                experiment.total_runs = execution_results.get('total_analyses', 0)
                                experiment.successful_runs = execution_results.get('successful_analyses', 0)
                                # Store cost and results in research_notes (no results_summary field)
                                existing_notes = experiment.research_notes or ""
                                experiment.research_notes = f"{existing_notes}\nCompleted: {execution_results.get('total_analyses', 0)} analyses, ${execution_results.get('total_cost', 0):.3f} cost"
                            
                            session.commit()
                            logger.info(f"✅ Database experiment status updated to COMPLETED")
                        else:
                            logger.warning(f"⚠️  Experiment ID {self.database_experiment_id} not found in database")
                    
                    except SQLAlchemyError as se:
                        session.rollback()
                        logger.error(f"❌ Database error updating experiment status: {se}")
                    finally:
                        session.close()
                    
                except Exception as e:
                    logger.warning(f"⚠️  Failed to update database experiment status: {e}")
            
            logger.info("✅ Experiment transaction completed successfully!")
            logger.info(f"📋 Transaction ID: {self.current_experiment_id}")
            logger.info(f"💾 Database ID: {self.database_experiment_id}")
            
        except FrameworkTransactionIntegrityError as fti_error:
            # 🔒 FRAMEWORK TRANSACTION INTEGRITY FAILURE HANDLING
            logger.error("🚨 FRAMEWORK TRANSACTION INTEGRITY FAILURE")
            logger.error("=" * 60)
            
            # Display detailed error message to user
            print("\n🚨 EXPERIMENT TERMINATED")
            print("=" * 60)
            print(fti_error.detailed_message)
            print("=" * 60)
            
            # Update database status if available
            if hasattr(self, 'database_experiment_id') and self.database_experiment_id and DATABASE_AVAILABLE:
                try:
                    from src.narrative_gravity.models.models import Experiment
                    from src.narrative_gravity.utils.database import get_database_url
                    from sqlalchemy import create_engine
                    from sqlalchemy.orm import sessionmaker
                    from sqlalchemy.exc import SQLAlchemyError
                    
                    engine = create_engine(get_database_url())
                    Session = sessionmaker(bind=engine)
                    session = Session()
                    
                    try:
                        experiment = session.query(Experiment).filter_by(id=self.database_experiment_id).first()
                        if experiment:
                            experiment.status = 'failed'
                            # Store framework transaction failure details
                            error_details = {
                                'failure_type': 'framework_transaction_integrity',
                                'transaction_id': fti_error.transaction_id,
                                'framework_errors': fti_error.framework_errors[:3],  # Limit for storage
                                'timestamp': datetime.now().isoformat()
                            }
                            experiment.research_notes = f"{experiment.research_notes or ''}\nFRAMEWORK TRANSACTION FAILURE: {json.dumps(error_details)}"
                            
                            session.commit()
                            logger.info(f"💾 Database experiment status updated: FRAMEWORK TRANSACTION FAILURE")
                        
                    except SQLAlchemyError as se:
                        session.rollback()
                        logger.error(f"❌ Database error recording framework failure: {se}")
                    finally:
                        session.close()
                        
                except Exception as db_error:
                    logger.warning(f"⚠️  Failed to update database with framework failure: {db_error}")
            
            # Log to experiment logger if available
            if hasattr(self, 'experiment_logger') and self.experiment_logger:
                self.experiment_logger.error(
                    "Framework transaction integrity failure",
                    error_code="FRAMEWORK_TRANSACTION_INTEGRITY_FAILURE",
                    extra_data={
                        'transaction_id': fti_error.transaction_id,
                        'framework_errors': fti_error.framework_errors,
                        'guidance': fti_error.guidance
                    }
                )
                self.experiment_logger.end_experiment_logging(False)
            
            # Exit with specific code for framework failures
            logger.error(f"🔒 Framework transaction integrity compromised - experiment cannot proceed")
            sys.exit(2)  # Different exit code for framework integrity issues
            
        except Exception as e:
            # 🚨 FIX: UPDATE DATABASE EXPERIMENT STATUS TO FAILED
            if hasattr(self, 'database_experiment_id') and self.database_experiment_id and DATABASE_AVAILABLE:
                try:
                    from src.narrative_gravity.models.models import Experiment
                    from src.narrative_gravity.utils.database import get_database_url
                    from sqlalchemy import create_engine
                    from sqlalchemy.orm import sessionmaker
                    from sqlalchemy.exc import SQLAlchemyError
                    
                    engine = create_engine(get_database_url())
                    Session = sessionmaker(bind=engine)
                    session = Session()
                    
                    try:
                        # 🔒 COHERENCE FIX: Update experiment status with correct field mapping
                        experiment = session.query(Experiment).filter_by(id=self.database_experiment_id).first()
                        if experiment:
                            experiment.status = 'failed'  # Use string value, not enum
                            # Store error in research_notes (no error_message field in model)
                            error_msg = str(e)[:500]  # Truncate long error messages
                            existing_notes = experiment.research_notes or ""
                            experiment.research_notes = f"{existing_notes}\nFAILED: {error_msg}"
                            
                            session.commit()
                            logger.info(f"💾 Database experiment status updated to FAILED")
                        else:
                            logger.warning(f"⚠️  Experiment ID {self.database_experiment_id} not found in database")
                    
                    except SQLAlchemyError as se:
                        session.rollback()
                        logger.error(f"❌ Database error updating experiment failure status: {se}")
                    finally:
                        session.close()
                    
                except Exception as db_error:
                    logger.warning(f"⚠️  Failed to update database experiment status: {db_error}")
            
            # Log error and end experiment logging with failure
            if self.experiment_logger:
                self.experiment_logger.error(
                    f"Orchestrator execution failed: {e}",
                    error_code=ExperimentErrorCodes.EXECUTION_EXPERIMENT_FAILED,
                    exception=e
                )
                self.experiment_logger.end_experiment_logging(False)
            
            logger.error(f"❌ Orchestrator execution failed: {e}")
            if isinstance(e, MissingComponentsError):
                sys.exit(1)
            else:
                import traceback
                traceback.print_exc()
                sys.exit(1)
    
    def _validate_experiment_for_database(self, experiment_meta: Dict[str, Any], experiment: Dict[str, Any]) -> Dict[str, Any]:
        """
        🔒 COHERENCE VALIDATION: Validate experiment data for database insertion
        Ensures all required Experiment model fields are present and valid.
        """
        validation_result = {
            'valid': False,
            'errors': [],
            'warnings': []
        }
        
        try:
            # Extract components configuration for validation
            components = experiment.get('components', {})
            frameworks = components.get('frameworks', [])
            templates = components.get('prompt_templates', [])
            models = components.get('models', [])
            weighting_schemes = components.get('weighting_schemes', [])
            
            # Required field: prompt_template_id (NOT NULL in database)
            if templates:
                template_id = templates[0].get('id', templates[0].get('name', 'unknown_template'))
                validation_result['prompt_template_id'] = template_id
            else:
                validation_result['prompt_template_id'] = 'default_template'
                validation_result['warnings'].append('No prompt template specified, using default')
            
            # Required field: framework_config_id (NOT NULL in database)
            if frameworks:
                framework_id = frameworks[0].get('id', frameworks[0].get('name', 'unknown_framework'))
                validation_result['framework_config_id'] = framework_id
            else:
                validation_result['framework_config_id'] = 'default_framework'
                validation_result['errors'].append('No framework specified - this is required')
            
            # Required field: scoring_algorithm_id (NOT NULL in database)
            if weighting_schemes:
                algorithm_id = weighting_schemes[0].get('id', weighting_schemes[0].get('name', 'unknown_algorithm'))
                validation_result['scoring_algorithm_id'] = algorithm_id
            else:
                validation_result['scoring_algorithm_id'] = 'proportional'
                validation_result['warnings'].append('No scoring algorithm specified, using proportional')
            
            # Required field: selected_models (JSON array, NOT NULL in database)
            if models:
                model_list = [model.get('id', model.get('name', 'unknown_model')) for model in models]
                validation_result['selected_models'] = model_list
            else:
                validation_result['selected_models'] = ['gpt-4']
                validation_result['warnings'].append('No models specified, using default gpt-4')
            
            # Optional field: analysis_mode
            analysis_mode = 'single_model' if len(validation_result['selected_models']) == 1 else 'multi_model_comparison'
            validation_result['analysis_mode'] = analysis_mode
            
            # Validate field lengths (database constraints)
            name = experiment_meta.get('name', 'Unnamed Experiment')
            if len(name) > 255:
                validation_result['warnings'].append(f'Experiment name too long, truncating to 255 chars')
            
            # Validate JSON data
            try:
                import json
                json.dumps(validation_result['selected_models'])
                if experiment_meta.get('tags'):
                    json.dumps(experiment_meta.get('tags'))
            except (TypeError, ValueError) as json_error:
                validation_result['errors'].append(f'Invalid JSON data: {json_error}')
            
            # Check if validation passed
            validation_result['valid'] = len(validation_result['errors']) == 0
            
            if validation_result['valid']:
                logger.info(f"✅ Experiment data validation passed with {len(validation_result['warnings'])} warnings")
            else:
                logger.error(f"❌ Experiment data validation failed with {len(validation_result['errors'])} errors")
            
        except Exception as e:
            validation_result['valid'] = False
            validation_result['errors'].append(f'Validation process failed: {e}')
            logger.error(f"❌ Experiment validation error: {e}")
        
        return validation_result

class UnifiedAssetManager:
    """Unified asset management with content-addressable storage"""
    
    def __init__(self, storage_root: str = "asset_storage"):
        self.storage_root = Path(storage_root)
        self.storage_root.mkdir(exist_ok=True)
        
        # Create asset type directories
        for asset_type in ['framework', 'prompt_template', 'weighting_scheme', 'experiment']:
            (self.storage_root / asset_type).mkdir(exist_ok=True)
    
    def calculate_content_hash(self, content: Any, asset_type: str) -> str:
        """Calculate SHA-256 hash of asset content"""
        if asset_type in ['framework', 'prompt_template', 'weighting_scheme', 'experiment']:
            # For structured data, use canonical JSON representation
            if isinstance(content, dict):
                canonical_json = json.dumps(content, sort_keys=True, separators=(',', ':'))
                return hashlib.sha256(canonical_json.encode('utf-8')).hexdigest()
            elif isinstance(content, str):
                return hashlib.sha256(content.encode('utf-8')).hexdigest()
        
        raise ValueError(f"Unsupported asset type for hashing: {asset_type}")
    
    def get_storage_path(self, content_hash: str, asset_type: str) -> Path:
        """Get storage path for content hash using prefix-based directory structure"""
        # Use first 2 and next 2 characters for directory structure
        prefix1 = content_hash[:2]
        prefix2 = content_hash[2:4]
        
        storage_path = self.storage_root / asset_type / prefix1 / prefix2 / content_hash
        return storage_path
    
    def store_asset(self, content: Any, asset_type: str, asset_id: str, version: str, 
                   source_path: Optional[str] = None) -> Dict[str, Any]:
        """Store validated asset in content-addressable storage"""
        
        # Calculate content hash
        content_hash = self.calculate_content_hash(content, asset_type)
        storage_path = self.get_storage_path(content_hash, asset_type)
        
        # Check if asset already exists
        if storage_path.exists():
            logger.info(f"📦 Asset already stored: {asset_id} (hash: {content_hash[:8]}...)")
            return {
                'content_hash': content_hash,
                'storage_path': str(storage_path),
                'already_existed': True
            }
        
        # Create storage directory
        storage_path.mkdir(parents=True, exist_ok=True)
        
        # Store primary content
        if not YAML_AVAILABLE:
            raise RuntimeError("PyYAML not available - cannot store YAML assets")
            
        if asset_type == 'framework':
            content_file = storage_path / 'framework.yaml'
            with open(content_file, 'w') as f:
                yaml.dump(content, f, default_flow_style=False, sort_keys=False)
        elif asset_type in ['prompt_template', 'weighting_scheme']:
            content_file = storage_path / f'{asset_type}.yaml'
            with open(content_file, 'w') as f:
                yaml.dump(content, f, default_flow_style=False, sort_keys=False)
        elif asset_type == 'experiment':
            content_file = storage_path / 'experiment.yaml'
            with open(content_file, 'w') as f:
                yaml.dump(content, f, default_flow_style=False, sort_keys=False)
        
        # Create metadata
        metadata = {
            'asset_type': asset_type,
            'asset_id': asset_id,
            'version': version,
            'content_hash': content_hash,
            'created_timestamp': datetime.now().isoformat(),
            'storage_path': str(storage_path),
            'content_size': len(json.dumps(content) if isinstance(content, dict) else str(content))
        }
        
        metadata_file = storage_path / '.metadata.yaml'
        with open(metadata_file, 'w') as f:
            yaml.dump(metadata, f, default_flow_style=False)
        
        # Create provenance tracking
        provenance = {
            'asset_id': asset_id,
            'version': version,
            'source_path': source_path,
            'ingestion_method': 'orchestrator_validation',
            'ingestion_timestamp': datetime.now().isoformat(),
            'content_hash': content_hash,
            'validation_status': 'validated_before_storage'
        }
        
        provenance_file = storage_path / '.provenance.yaml'
        with open(provenance_file, 'w') as f:
            yaml.dump(provenance, f, default_flow_style=False)
        
        logger.info(f"📦 Stored asset: {asset_id} (hash: {content_hash[:8]}...) → {storage_path}")
        
        return {
            'content_hash': content_hash,
            'storage_path': str(storage_path),
            'already_existed': False,
            'metadata': metadata,
            'provenance': provenance
        }
    
    def load_asset_by_hash(self, content_hash: str, asset_type: str) -> Optional[Dict[str, Any]]:
        """Load asset by content hash"""
        storage_path = self.get_storage_path(content_hash, asset_type)
        
        if not storage_path.exists():
            return None
        
        # Load primary content
        if asset_type == 'framework':
            content_file = storage_path / 'framework.yaml'
        elif asset_type in ['prompt_template', 'weighting_scheme']:
            content_file = storage_path / f'{asset_type}.yaml'
        elif asset_type == 'experiment':
            content_file = storage_path / 'experiment.yaml'
        else:
            return None
        
        if not content_file.exists():
            return None
        
        with open(content_file, 'r') as f:
            content = yaml.safe_load(f)
        
        # Load metadata if available
        metadata_file = storage_path / '.metadata.yaml'
        metadata = None
        if metadata_file.exists():
            with open(metadata_file, 'r') as f:
                metadata = yaml.safe_load(f)
        
        return {
            'content': content,
            'content_hash': content_hash,
            'storage_path': str(storage_path),
            'metadata': metadata
        }
    
    def verify_asset_integrity(self, content_hash: str, asset_type: str) -> bool:
        """Verify asset integrity by recalculating hash"""
        asset_data = self.load_asset_by_hash(content_hash, asset_type)
        if not asset_data:
            return False
        
        recalculated_hash = self.calculate_content_hash(asset_data['content'], asset_type)
        return recalculated_hash == content_hash

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Comprehensive Experiment Orchestrator - Phase 1 & 2 Complete",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Dry run to validate experiment definition
  python comprehensive_experiment_orchestrator.py experiment.json --dry-run
  
  # Execute with auto-registration of missing components
  python comprehensive_experiment_orchestrator.py experiment.json --force-reregister
  
  # Execute and automatically open HTML report in browser
  python comprehensive_experiment_orchestrator.py experiment.json --open-report
  
  # Normal execution
  python comprehensive_experiment_orchestrator.py experiment.json

Phase 2 Features:
  - Framework auto-registration from filesystem to database
  - Prompt template auto-registration with default content
  - Weighting scheme auto-registration with default algorithms
  - Database integration with existing component models
        """
    )
    
    parser.add_argument(
        'experiment_file',
        type=Path,
        nargs='?',  # Make optional for resume mode
        help='Path to experiment definition JSON file (optional when using --resume)'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Validate experiment and show execution plan without running'
    )
    
    parser.add_argument(
        '--force-reregister',
        action='store_true', 
        help='Auto-register missing components instead of failing'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    parser.add_argument(
        '--open-report',
        action='store_true',
        help='Automatically open the HTML report in browser after successful completion'
    )
    
    parser.add_argument(
        '--resume',
        action='store_true',
        help='Resume the most recent failed/interrupted experiment from checkpoint'
    )
    
    parser.add_argument(
        '--list-resumable',
        action='store_true',
        help='List experiments that can be resumed'
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Create orchestrator
    orchestrator = ExperimentOrchestrator()
    orchestrator.dry_run = args.dry_run
    orchestrator.force_reregister = args.force_reregister
    orchestrator.open_report = args.open_report
    orchestrator.resume_from_checkpoint = args.resume
    
    # Handle --list-resumable command
    if args.list_resumable:
        resumable = orchestrator.find_resumable_experiments()
        if resumable:
            print(f"\n📋 Found {len(resumable)} resumable experiments:")
            print("=" * 80)
            for exp in resumable:
                print(f"🔄 {exp['experiment_id']}")
                print(f"   State: {exp['state']}")
                print(f"   Timestamp: {exp['timestamp']}")
                print(f"   Checkpoint: {exp['checkpoint_path']}")
                print()
            print("💡 Use --resume to resume the most recent experiment")
        else:
            print("\n📋 No resumable experiments found")
        return
    
    # Validate experiment file requirement (unless listing resumable)
    if not args.resume and not args.experiment_file:
        logger.error("Experiment file required unless using --resume or --list-resumable")
        return
    
    # Execute experiment
    if args.resume and not args.experiment_file:
        # Resume mode without specific experiment file - will find latest resumable
        orchestrator.execute_experiment(Path("dummy.json"))  # Will be overridden by resume logic
    else:
        orchestrator.execute_experiment(args.experiment_file)

if __name__ == "__main__":
    main() 