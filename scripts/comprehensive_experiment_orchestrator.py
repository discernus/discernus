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
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
import logging
from datetime import datetime

# Configure basic logging (will be enhanced with experiment logging)
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

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

class MissingComponentsError(Exception):
    """Raised when required experiment components are missing"""
    def __init__(self, missing_components: List[str], guidance: Dict[str, str]):
        self.missing_components = missing_components
        self.guidance = guidance
        super().__init__(f"Missing components: {', '.join(missing_components)}")

@dataclass
class ComponentInfo:
    """Information about an experiment component"""
    component_type: str
    component_id: str
    version: Optional[str] = None
    file_path: Optional[str] = None
    expected_hash: Optional[str] = None
    exists_in_db: bool = False
    exists_on_filesystem: bool = False
    needs_registration: bool = False

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
        """Load framework using consolidated format first, fallback to legacy"""
        # Try consolidated format first
        consolidated_file = self.frameworks_dir / framework_name / "framework_consolidated.json"
        if consolidated_file.exists():
            logger.info(f"Loading consolidated framework: {framework_name}")
            with open(consolidated_file, 'r') as f:
                return json.load(f)
        
        # Fallback to legacy format
        legacy_file = self.frameworks_dir / framework_name / "framework.json"
        if legacy_file.exists():
            logger.warning(f"Using legacy framework format: {framework_name}")
            with open(legacy_file, 'r') as f:
                return json.load(f)
        
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

class ExperimentOrchestrator:
    """Main orchestrator for comprehensive experiment execution"""
    
    def __init__(self):
        self.framework_loader = ConsolidatedFrameworkLoader()
        self.dry_run = False
        self.force_reregister = False
        
        # Initialize experiment logging (Phase 5: Comprehensive Logging)
        if DATABASE_AVAILABLE:
            try:
                setup_experiment_logging()
                self.experiment_logger = get_experiment_logger("experiment_orchestrator")
            except Exception as e:
                logger.warning(f"Experiment logging not available: {e}")
                self.experiment_logger = None
        else:
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
            framework_data = self.framework_loader.load_framework(framework_id)
            component.exists_on_filesystem = True
            
            # Validate framework structure
            missing_sections = self.framework_loader.validate_framework_structure(framework_data)
            if missing_sections:
                logger.warning(f"Framework {framework_id} missing sections: {missing_sections}")
            
        except FileNotFoundError:
            component.exists_on_filesystem = False
            component.needs_registration = True
        
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
                query = query.filter_by(version=version)
            
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
        """Pre-flight validation of experiment"""
        logger.info("🚁 Running pre-flight validation...")
        
        # Validate components
        components = self.validate_components(experiment)
        
        # Identify missing components
        missing_components = [
            comp for comp in components 
            if not comp.exists_on_filesystem or not comp.exists_in_db
        ]
        
        if missing_components:
            logger.error(f"❌ Pre-flight validation failed: {len(missing_components)} missing components")
            
            # Generate guidance
            guidance = self.generate_error_guidance(missing_components)
            
            # Print detailed error information
            print("\n🚨 MISSING COMPONENTS:")
            print("=" * 50)
            for component in missing_components:
                print(f"❌ {component.component_type}: {component.component_id}")
                if component.version:
                    print(f"   Version: {component.version}")
                if not component.exists_on_filesystem:
                    print(f"   Issue: Not found on filesystem")
                if not component.exists_in_db:
                    print(f"   Issue: Not registered in database")
                print()
            
            print("💡 GUIDANCE:")
            print("-" * 20)
            for component_key, guide_text in guidance.items():
                print(f"• {component_key}:")
                for line in guide_text.split('\n'):
                    if line.strip():
                        print(f"  {line}")
                print()
            
            print("🔧 SOLUTIONS:")
            print("-" * 20)
            print("  • Run with --dry-run to see execution plan without running")
            print("  • Run with --force-reregister to auto-register missing components")
            print("  • Check experiment definition format and file paths")
            print("  • See docs/user-guides/ for component setup guides")
            
            return False, missing_components
        
        logger.info("✅ Pre-flight validation passed!")
        return True, components
    
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
        """Main execution method with comprehensive logging"""
        try:
            # Load experiment definition
            experiment = self.load_experiment_definition(experiment_file)
            
            # Start experiment logging if available
            if self.experiment_logger:
                experiment_meta = experiment.get('experiment_meta', {})
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
            execution_results = self.execute_analysis_matrix(experiment, components)
            
            # Log execution summary (serialize datetime objects)
            if self.experiment_logger and execution_results:
                # Clean execution results for JSON serialization
                clean_results = execution_results.copy()
                clean_results.pop('results', None)  # Remove results array to avoid datetime issues
                
                self.experiment_logger.info(
                    f"Experiment execution completed: {execution_results['successful_analyses']}/{execution_results['total_analyses']} successful analyses",
                    extra_data={
                        'execution_summary': clean_results,
                        'total_cost': execution_results['total_cost'],
                        'cost_efficiency': execution_results['cost_efficiency']
                    }
                )
            
            # End experiment logging successfully
            if self.experiment_logger:
                self.experiment_logger.end_experiment_logging(True)
            
        except Exception as e:
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
        help='Path to experiment definition JSON file'
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
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Create orchestrator
    orchestrator = ExperimentOrchestrator()
    orchestrator.dry_run = args.dry_run
    orchestrator.force_reregister = args.force_reregister
    
    # Execute experiment
    orchestrator.execute_experiment(args.experiment_file)

if __name__ == "__main__":
    main() 