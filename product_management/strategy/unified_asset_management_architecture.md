# Unified Asset Management Architecture Strategy

**Document Version**: 1.0  
**Created**: June 19, 2025  
**Status**: Strategic Implementation Plan  
**Implementation Timeline**: Weeks 1-4 of Current Iteration

---

## **Executive Summary**

This strategy document outlines the comprehensive redesign of Discernus asset management infrastructure to achieve **disciplined, defensible, replicable, and auditable** research capabilities. The current five-dimensional experiment architecture (texts, frameworks, prompt templates, weighting schemes, evaluators) suffers from inconsistent asset management patterns, format inconsistencies, and insufficient auditing capabilities for academic credibility.

**Core Strategic Objectives:**
1. **Unified Asset Format**: Standardize on YAML for all researcher-developed assets
2. **Content-Addressable Storage**: Extend corpus hash-based pattern to all asset types  
3. **Two-Tier Architecture**: Separate development workspace from immutable storage
4. **Academic Audit Trail**: Complete replication packages with human-readable verification
5. **Systematic Version Control**: Comprehensive provenance tracking across all dimensions

---

## **Current State Analysis**

### **Asset Management Maturity Assessment**

| Dimension | Current State | Issues Identified | Target State |
|-----------|---------------|-------------------|--------------|
| **📁 Texts (Corpus)** | ✅ **Well-Architected** | *(none - reference model)* | ✅ **Maintain Excellence** |
| **🏗️ Frameworks** | 🔄 **Partially Architected** | Format inconsistency, sync issues | 🎯 **Unified YAML + Hash Storage** |
| **📝 Prompt Templates** | ❌ **Under-Architected** | No content hashing, minimal organization | 🎯 **Full Asset Management** |
| **⚖️ Weighting Schemes** | 🔄 **Database Only** | No development workspace | 🎯 **Development → Storage Pipeline** |
| **🤖 Evaluators (LLMs)** | ❌ **Ad-hoc Integration** | No systematic versioning | 🎯 **Complete Asset Lifecycle** |

### **Critical Gap: Theoretical Accuracy**
**Immediate Issue Identified**: Current `mft_persuasive_force` framework incorrectly implements Haidt's Moral Foundations Theory as 10 independent wells instead of 5 dipole pairs, compromising academic credibility for expert consultation.

**Resolution**: ✅ **Completed** - Created theoretically accurate `moral_foundations_theory` framework with proper dipole structure.

---

## **Strategic Architecture Design**

### **1. Unified Asset Format Standard**

**Decision**: **YAML for All Researcher-Developed Assets**

**Rationale:**
- **Human Readability**: Comments, multi-line strings, minimal syntax noise
- **Academic Collaboration**: Easier for researchers to read, edit, and understand
- **Version Control Friendly**: Git-compatible, meaningful diffs
- **Consistency**: Matches existing experiment definition format

**Implementation Scope:**
```yaml
# Asset Type Classification
researcher_developed_assets:
  format: YAML
  types:
    - experiments          # ✅ Already YAML
    - frameworks          # 🔄 Convert from JSON
    - prompt_templates    # 🔄 Convert from database-only
    - weighting_schemes   # 🔄 Convert from database-only  
    - evaluator_configs   # 🆕 Create new

system_generated_assets:
  format: JSON/Binary
  types:
    - corpus_metadata     # ✅ Stay JSON
    - experiment_results  # ✅ Stay JSON
    - database_exports    # ✅ Stay JSON
```

### **2. Two-Tier Architecture Pattern**

**Principle**: **Separate Development Workflow from Immutable Storage**

```
Development Workspace              Content-Addressable Storage
(Semantic, Mutable)               (Hash-Based, Immutable)

frameworks/                       asset_storage/
├── moral_foundations_theory/     ├── frameworks/
│   ├── framework.yaml           │   └── a7/f3/a7f3d8e2.../
│   ├── README.md                │       ├── framework.yaml
│   └── iterations/              │       ├── .metadata.yaml
│       ├── v1.0_initial.yaml    │       └── .provenance.yaml
│       └── v2.0_validated.yaml  └── prompt_templates/
                                     └── b2/c4/b2c4f1a9.../
```

### **3. Researcher Development Workspace Structure**

**Principle**: **Project-Focused Asset Development with Clear Asset Type Separation**

```
research_workspaces/
├── {project_name}_research_dev_workspace/
│   ├── README.md                          # Project overview and objectives
│   ├── project_manifest.yaml             # Asset inventory and status
│   │
│   ├── frameworks/                        # Framework development
│   │   ├── {framework_name}/
│   │   │   ├── framework.yaml            # Main framework definition
│   │   │   ├── README.md                 # Framework documentation  
│   │   │   ├── validation_notes.md       # Expert consultation notes
│   │   │   └── iterations/               # Development history
│   │   │       ├── v1.0_initial.yaml
│   │   │       ├── v1.1_expert_feedback.yaml
│   │   │       └── v2.0_validated.yaml
│   │   └── [other_frameworks]/
│   │
│   ├── prompt_templates/                  # Template development
│   │   ├── {template_name}/
│   │   │   ├── template.yaml             # Main template definition
│   │   │   ├── README.md                 # Usage documentation
│   │   │   ├── validation_results.md     # Testing and validation
│   │   │   └── iterations/               # Development history
│   │   │       ├── v1.0_initial.yaml
│   │   │       └── v1.1_optimized.yaml
│   │   └── [other_templates]/
│   │
│   ├── weighting_schemes/                 # Weighting methodology development
│   │   ├── {scheme_name}/
│   │   │   ├── scheme.yaml               # Main scheme definition
│   │   │   ├── README.md                 # Theoretical justification
│   │   │   ├── validation_study.md       # Empirical validation results
│   │   │   └── iterations/               # Development history
│   │   └── [other_schemes]/
│   │
│   ├── evaluator_configs/                 # LLM evaluator configurations
│   │   ├── {evaluator_name}/
│   │   │   ├── config.yaml               # Evaluator configuration
│   │   │   ├── README.md                 # Usage and optimization notes
│   │   │   └── performance_logs/         # Testing and optimization data
│   │   └── [other_evaluators]/
│   │
│   ├── experiments/                       # Experiment definitions and results
│   │   ├── {experiment_name}/
│   │   │   ├── definition.yaml           # Experiment configuration
│   │   │   ├── README.md                 # Experiment objectives and methodology
│   │   │   ├── results/                  # Execution results and analysis
│   │   │   └── replication_package/      # Complete replication materials
│   │   └── [other_experiments]/
│   │
│   ├── validation_studies/                # Academic validation work
│   │   ├── mfq_correlation_study/
│   │   ├── expert_consultation_feedback/
│   │   └── cross_cultural_validation/
│   │
│   └── collaboration/                     # External collaboration materials
│       ├── expert_consultation_packages/
│       ├── academic_partnership_proposals/
│       └── publication_drafts/
```

**Workspace Benefits:**
- **Project Focus**: Clear boundaries for research initiatives
- **Asset Type Separation**: Frameworks, templates, schemes develop independently
- **Iteration Tracking**: Complete development history with validation milestones
- **Collaboration Ready**: Expert consultation and academic partnership materials
- **Academic Standards**: Validation studies and replication package preparation

**Development Tier Benefits:**
- Human-readable organization (`moral_foundations_theory`, not `a7f3d8e2...`)
- Mutable for iteration and experimentation
- Git-friendly structure for version control
- Researcher-focused workflow

**Storage Tier Benefits:**
- Content-addressable deduplication (same content = same hash)
- Immutable integrity protection
- Experiment replication guarantees
- Database references to exact versions

### **4. Content-Addressable Storage Extension**

**Strategy**: **Extend Proven Corpus Pattern to All Asset Types**

The corpus system demonstrates ideal asset management:
```
Content → Hash → Storage → Database Reference → Experiment Integration
```

**Universal Storage Pattern:**
```
{asset_type}/{hash_prefix}/{hash_middle}/{hash_full}/
├── {semantic_name}.yaml          # Main asset definition
├── .metadata.yaml                # Performance metrics, usage stats
├── .provenance.yaml              # Development lineage
└── .validation.yaml              # Compatibility testing results
```

**Hash-Based Benefits:**
- **Deduplication**: Same content stored once regardless of naming
- **Integrity Verification**: Detect corruption or tampering
- **Exact Replication**: Experiments reference specific content versions
- **Audit Trail**: Complete provenance from development to production

---

## **Implementation Architecture**

### **Phase 1: Foundation (Week 1)**

**Objective**: Establish unified format and basic two-tier structure

**Deliverables:**
1. **Framework YAML Conversion**
   ```bash
   # Convert existing frameworks to YAML
   frameworks/
   ├── moral_foundations_theory/framework.yaml  # ✅ Completed
   ├── civic_virtue/framework.yaml              # 🔄 Convert from JSON
   ├── iditi/framework.yaml                     # 🔄 Convert from JSON
   └── three_wells_political/framework.yaml     # ✅ Already consolidated
   ```

2. **Prompt Template Development Workspace**
   ```bash
   prompt_templates/
   ├── hierarchical_analysis/
   │   ├── template.yaml           # Main template
   │   ├── README.md              # Usage documentation
   │   └── iterations/            # Development history
   ├── direct_analysis/
   └── comparative_analysis/
   ```

3. **Asset Ingestion Pipeline Design**
   ```python
   class UnifiedAssetIngestion:
       """Extend corpus pattern to all asset types"""
       
       def ingest_framework(self, development_path: Path) -> AssetStorageResult:
           # Calculate content hash
           content_hash = self._calculate_asset_hash(development_path)
           
           # Check for existing version
           existing = self._check_existing_hash(content_hash)
           if existing:
               return AssetStorageResult(duplicate=True, existing_id=existing)
           
           # Create content-addressable storage
           storage_path = self._create_hash_storage(content_hash, development_path)
           
           # Register in database
           asset_id = self._register_asset(storage_path, content_hash)
           
           return AssetStorageResult(success=True, asset_id=asset_id, storage_path=storage_path)
   ```

### **Phase 2: Hash-Based Storage (Week 2)**

**Objective**: Implement content-addressable storage for all asset types

**Deliverables:**
1. **Universal Asset Storage System**
   ```
   asset_storage/
   ├── frameworks/
   │   ├── a7/f3/a7f3d8e2.../     # MFT framework
   │   ├── b1/c2/b1c2d3e4.../     # Civic Virtue framework
   │   └── c4/d5/c4d5e6f7.../     # IDITI framework
   ├── prompt_templates/
   │   ├── e8/f9/e8f9a0b1.../     # Hierarchical analysis template
   │   └── g2/h3/g2h3i4j5.../     # Direct analysis template
   ├── weighting_schemes/
   │   ├── k6/l7/k6l7m8n9.../     # Winner-take-most methodology
   │   └── o0/p1/o0p1q2r3.../     # Proportional weighting
   └── evaluator_configs/
       ├── s4/t5/s4t5u6v7.../     # GPT-4 configuration
       └── w8/x9/w8x9y0z1.../     # Claude-3.5 configuration
   ```

2. **Database Schema Extensions**
   ```sql
   -- Universal asset versioning table
   CREATE TABLE asset_versions (
       id UUID PRIMARY KEY,
       asset_type VARCHAR(50) NOT NULL,  -- 'framework', 'prompt_template', etc.
       name VARCHAR(100) NOT NULL,
       version VARCHAR(20) NOT NULL,
       content_hash VARCHAR(64) NOT NULL,
       storage_path TEXT NOT NULL,
       development_session_id UUID,
       created_at TIMESTAMP DEFAULT NOW(),
       UNIQUE(asset_type, name, version),
       UNIQUE(content_hash)  -- Enforce deduplication
   );
   
   -- Asset provenance tracking
   CREATE TABLE asset_provenance (
       id UUID PRIMARY KEY,
       asset_version_id UUID REFERENCES asset_versions(id),
       source_type VARCHAR(50),  -- 'development_session', 'migration', 'import'
       source_metadata JSONB,
       created_at TIMESTAMP DEFAULT NOW()
   );
   ```

### **Phase 3: Experiment Integration (Week 3)**

**Objective**: Update experiment orchestration to use unified asset system

**Deliverables:**
1. **Enhanced Experiment Definition Format**
   ```yaml
   experiment_meta:
     name: "MFT Academic Validation Study"
     version: "v1.0"
     
   components:
     framework:
       name: "moral_foundations_theory"
       version: "v2025.06.19"
       # System resolves to content hash: a7f3d8e2bc4a1509...
       
     prompt_template:
       name: "hierarchical_analysis"  
       version: "v2.1"
       # System resolves to content hash: b2c4f1a98e7d3621...
       
     weighting_scheme:
       name: "foundation_pairs"
       version: "v1.0"
       # System resolves to content hash: c5d7e9f2a8b3c014...
       
     evaluator:
       name: "gpt4_academic"
       version: "v2025.06"
       # System resolves to content hash: d8f2a7c5b9e1f634...
   ```

2. **Asset Resolution System**
   ```python
   class ExperimentAssetResolver:
       """Resolve semantic asset references to hash-based storage"""
       
       def resolve_experiment_assets(self, experiment_config: Dict) -> ResolvedAssets:
           resolved = {}
           
           for component_type, component_spec in experiment_config['components'].items():
               # Look up asset by name + version
               asset_record = self.db.get_asset_version(
                   asset_type=component_type,
                   name=component_spec['name'],
                   version=component_spec['version']
               )
               
               if not asset_record:
                   raise AssetNotFoundError(f"{component_type}:{component_spec['name']}:{component_spec['version']}")
               
               # Verify hash integrity
               if not self._verify_hash_integrity(asset_record):
                   raise AssetIntegrityError(f"Content hash mismatch: {asset_record.content_hash}")
               
               resolved[component_type] = {
                   'asset_id': asset_record.id,
                   'content_hash': asset_record.content_hash,
                   'storage_path': asset_record.storage_path,
                   'resolved_content': self._load_asset_content(asset_record.storage_path)
               }
           
           return ResolvedAssets(resolved)
   ```

### **Phase 4: Replication Packages (Week 4)**

**Objective**: Create comprehensive audit-ready replication packages

**Deliverables:**
1. **Replication Package Generator**
   ```python
   class ReplicationPackageGenerator:
       """Generate comprehensive, auditor-friendly experiment packages"""
       
       def create_replication_package(self, experiment_id: str) -> ReplicationPackage:
           package_dir = f"replication_packages/{experiment_id}_{timestamp}"
           
           # Human-readable summary
           self._create_rosetta_stone(experiment_id, package_dir)
           
           # Asset copies in both formats
           self._copy_human_readable_assets(experiment_id, package_dir)
           self._copy_hash_verified_assets(experiment_id, package_dir)
           
           # Complete execution logs
           self._export_execution_logs(experiment_id, package_dir)
           
           # Verification tools
           self._create_verification_tools(experiment_id, package_dir)
           
           # Academic documentation
           self._generate_methodology_docs(experiment_id, package_dir)
           
           return ReplicationPackage(package_dir)
   ```

2. **"Rosetta Stone" Manifest**
   ```yaml
   # EXPERIMENT_MANIFEST.yaml - The human auditor's guide
   experiment_metadata:
     name: "MFT Academic Validation Study"
     experiment_id: "mft_validation_20250619_143025"
     executed_at: "2025-06-19T14:30:25Z"
     total_cost: "$47.23"
     
   human_readable_summary: |
     This experiment validated Haidt's Moral Foundations Theory framework
     using hierarchical analysis prompts on 125 political texts, evaluated
     by GPT-4 and Claude-3.5, using foundation-pairs weighting methodology.
     
   asset_manifest:
     framework:
       name: "Moral Foundations Theory (Haidt)"
       version: "v2025.06.19"
       human_file: "assets/human_readable/framework_mft.yaml"
       hash_file: "assets/hash_verified/a7/f3/a7f3d8e2.../framework.yaml"
       content_hash: "a7f3d8e2bc4a1509..."
       theoretical_basis: "Haidt (2012), Graham et al. (2013)"
       
   execution_summary:
     total_llm_calls: 250
     success_rate: "98.4%"
     qa_validation_passes: 246
     statistical_significance: "p < 0.001"
     
   verification_instructions: |
     1. Run `python verification_tools/verify_integrity.py`
     2. Compare human_readable with hash_verified assets
     3. Review execution_logs/ for complete audit trail
     4. Use `python replay_experiment.py` to replicate results
   ```

---

## **Academic Credibility Benefits**

### **1. Complete Transparency**
- **Asset Provenance**: Full development lineage from initial creation to experiment use
- **Content Integrity**: Hash verification proves no post-experiment tampering
- **Human Audit Trail**: Persnickety auditors can examine everything without using our system

### **2. Replication Guarantees**
- **Exact Asset Versions**: Content-addressable storage ensures experiments use identical assets
- **Independent Verification**: Replication packages work outside our infrastructure
- **Academic Standards**: Publication-ready with proper documentation and verification tools

### **3. Expert Consultation Ready**
- **Theoretical Accuracy**: MFT framework now correctly implements Haidt's dipole structure
- **Professional Presentation**: Clean YAML format for academic review
- **Complete Documentation**: Theoretical foundations, implementation rationale, validation results

---

## **Implementation Timeline**

### **Week 1: Foundation & Framework Conversion**
**Days 1-2**: MFT framework validation and testing
**Days 3-4**: Convert remaining frameworks to YAML format  
**Day 5**: Create prompt template development workspace

### **Week 2: Hash-Based Storage System**
**Days 1-2**: Implement universal asset ingestion pipeline
**Days 3-4**: Create content-addressable storage for all asset types
**Day 5**: Database schema updates and migration scripts

### **Week 3: Experiment Integration**
**Days 1-2**: Update experiment orchestrator for unified asset resolution
**Days 3-4**: Test end-to-end workflow with all asset types
**Day 5**: Performance optimization and error handling

### **Week 4: Replication & Audit Infrastructure** 
**Days 1-2**: Build replication package generator
**Days 3-4**: Create verification tools and human audit workflows
**Day 5**: Documentation and academic compliance validation

---

## **Success Metrics**

### **Technical Metrics**
- ✅ **Asset Deduplication**: Same content stored once across all asset types
- ✅ **Integrity Verification**: 100% hash-verified asset loading
- ✅ **Format Consistency**: All researcher assets in YAML format
- ✅ **Development Workflow**: Semantic workspace → hash storage pipeline

### **Academic Metrics**
- ✅ **Expert Review Ready**: MFT framework suitable for Haidt lab consultation
- ✅ **Audit Compliance**: Human auditor can independently verify all experiments
- ✅ **Replication Success**: Independent reproduction using replication packages
- ✅ **Publication Quality**: Academic-standard documentation and provenance

### **Research Impact Metrics**
- ✅ **Researcher Adoption**: YAML format increases researcher engagement
- ✅ **Collaboration Facilitation**: Clear asset structure enables academic partnerships
- ✅ **Scientific Credibility**: Hash-verified integrity supports peer review process
- ✅ **Long-term Preservation**: BagIt-ready packages for institutional repositories

---

## **Risk Mitigation**

### **Technical Risks**
**Risk**: Asset migration corruption during format conversion
**Mitigation**: Complete backups + hash verification of all conversions

**Risk**: Performance degradation from hash-based lookups  
**Mitigation**: Database indexing on content hashes + caching layer

### **Academic Risks**
**Risk**: Framework theoretical accuracy questioned by experts
**Mitigation**: ✅ **Resolved** - MFT framework now theoretically accurate per Haidt literature

**Risk**: Audit trail insufficient for peer review
**Mitigation**: Comprehensive replication packages with human-readable verification

### **Operational Risks**
**Risk**: Development workflow disruption during transition
**Mitigation**: Maintain existing system during parallel implementation + phased cutover

---

## **Future Evolution: Digital Preservation (Phase 2)**

### **Long-Term Preservation Strategy**
**Timeline**: 6-12 months post-implementation

**BagIt Integration:**
```python
# Preservation-grade packaging
def create_bagit_archive(replication_package_path):
    bag = bagit.make_bag(replication_package_path, {
        'Contact-Name': 'Discernus Research Team',
        'Experiment-Type': 'Computational Discourse Analysis',
        'Software-Agent': 'Discernus v2025.06',
        'Digital-Preservation-Standard': 'BagIt-1.0'
    })
    return bag
```

**Academic Integration:**
- DOI assignment for experiments
- Research Data Alliance metadata compliance  
- Institutional repository integration
- Citation standard development

---

## **Conclusion**

This unified asset management architecture establishes Discernus as a **disciplined, defensible, replicable, and auditable** research platform. By extending the proven corpus pattern to all asset types, standardizing on YAML for researcher workflows, and implementing comprehensive audit trails, we create the foundation for credible academic adoption and expert collaboration.

The immediate focus on MFT framework theoretical accuracy and expert consultation readiness positions us for successful academic validation while building long-term infrastructure for scientific excellence.

**Next Steps**: Await approval to proceed with Phase 1 implementation as outlined in updated iteration plans and daily TODO items.

---

*This strategy document supersedes previous asset management approaches and establishes the architectural foundation for academic credibility and scientific reproducibility.* 