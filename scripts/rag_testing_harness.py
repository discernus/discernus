#!/usr/bin/env python3
"""
RAG Testing Harness for Discernus

This script allows interactive testing of RAG indices to diagnose why
fact-checking queries aren't returning useful results.
"""

import sys
import os
import logging
import json
import base64
from pathlib import Path
from typing import Dict, Any, List, Optional
import argparse

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from discernus.core.clean_analysis_orchestrator import CleanAnalysisOrchestrator
from discernus.core.local_artifact_storage import LocalArtifactStorage


class RAGTestingHarness:
    """Interactive RAG index testing and diagnosis tool."""
    
    def __init__(self, experiment_path: str):
        self.experiment_path = Path(experiment_path)
        self.orchestrator = None
        self.artifact_storage = None
        self.rag_index = None
        
        # Setup verbose logging
        self._setup_logging()
        
    def _setup_logging(self):
        """Setup verbose logging for txtai and our operations."""
        # Enable txtai debug logging
        txtai_logger = logging.getLogger("txtai.embeddings")
        txtai_logger.setLevel(logging.DEBUG)
        
        # Setup our own logging
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(sys.stdout),
                logging.FileHandler('rag_testing.log')
            ]
        )
        
        self.logger = logging.getLogger(__name__)
        self.logger.info("RAG Testing Harness initialized with verbose logging")
        
    def load_experiment(self):
        """Load the experiment and its artifacts."""
        try:
            self.logger.info(f"Loading experiment from: {self.experiment_path}")
            
            # Initialize orchestrator
            self.orchestrator = CleanAnalysisOrchestrator(self.experiment_path)
            self.logger.info("✅ Orchestrator initialized")
            
            # Load specifications
            self.orchestrator.config = self.orchestrator._load_specs()
            self.logger.info(f"✅ Config loaded: {list(self.orchestrator.config.keys())}")
            
            # Initialize artifact storage like the orchestrator does
            from discernus.core.security_boundary import ExperimentSecurityBoundary
            security = ExperimentSecurityBoundary(self.experiment_path)
            shared_cache_dir = self.experiment_path / "shared_cache"
            self.artifact_storage = LocalArtifactStorage(
                security_boundary=security,
                run_folder=shared_cache_dir,
                run_name="rag_testing"
            )
            self.logger.info("✅ Artifact storage initialized")
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to load experiment: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def examine_existing_rag_indices(self):
        """Examine what RAG indices exist in the experiment."""
        try:
            self.logger.info("🔍 Examining existing RAG indices...")
            
            # Look for RAG index artifacts
            cache_dir = self.experiment_path / "shared_cache" / "artifacts"
            if not cache_dir.exists():
                self.logger.warning("No shared_cache/artifacts directory found")
                return
            
            rag_files = list(cache_dir.glob("rag_index_cache_*"))
            self.logger.info(f"Found {len(rag_files)} RAG index cache files:")
            
            for rag_file in rag_files:
                size_mb = rag_file.stat().st_size / (1024 * 1024)
                self.logger.info(f"  - {rag_file.name}: {size_mb:.1f} MB")
            
            # Check artifact registry for RAG index metadata
            registry_file = cache_dir / "artifact_registry.json"
            if registry_file.exists():
                with open(registry_file, 'r') as f:
                    registry = json.load(f)
                
                rag_entries = [k for k in registry.keys() if 'rag' in k.lower()]
                self.logger.info(f"RAG-related entries in registry: {rag_entries}")
                
                # Show details for each RAG entry
                for entry in rag_entries:
                    if entry in registry:
                        details = registry[entry]
                        self.logger.info(f"  {entry}: {details}")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to examine RAG indices: {e}")
            import traceback
            traceback.print_exc()
    
    def load_rag_index(self, index_hash: Optional[str] = None):
        """Load a specific RAG index or the most recent one."""
        try:
            if not index_hash:
                # Find the most recent RAG index
                cache_dir = self.experiment_path / "shared_cache" / "artifacts"
                rag_files = list(cache_dir.glob("rag_index_cache_*"))
                if not rag_files:
                    self.logger.error("No RAG index files found")
                    return False
                
                # Use the largest/most recent one
                rag_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
                index_hash = rag_files[0].name.replace("rag_index_cache_", "")
                self.logger.info(f"Using most recent RAG index: {index_hash}")
            
            # Load the RAG index
            self.logger.info(f"🔧 Loading RAG index: {index_hash}")
            
            # Try to load from artifact storage first
            try:
                rag_data = self.artifact_storage.get_artifact(index_hash)
                self.logger.info(f"✅ Loaded RAG index from artifact storage: {len(rag_data)} bytes")
                
                # Import txtai and load the index
                from txtai.embeddings import Embeddings
                self.rag_index = Embeddings()
                
                # Load the cached index
                import tempfile
                with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                    temp_file.write(rag_data)
                    temp_path = temp_file.name
                
                try:
                    self.rag_index.load(temp_path)
                    self.logger.info("✅ RAG index loaded successfully")
                    
                    # Get index info
                    if hasattr(self.rag_index, 'index'):
                        index_info = self.rag_index.index
                        self.logger.info(f"Index info: {index_info}")
                        
                        if hasattr(index_info, 'documents'):
                            doc_count = len(index_info.documents) if index_info.documents else 0
                            self.logger.info(f"Documents in index: {doc_count}")
                    
                    return True
                    
                finally:
                    # Clean up temp file
                    os.unlink(temp_path)
                    
            except Exception as e:
                self.logger.warning(f"Failed to load from artifact storage: {e}")
                
                # Try direct file loading (RAG indices are stored as tar.gz files)
                cache_dir = self.experiment_path / "shared_cache" / "artifacts"
                rag_file = cache_dir / f"rag_index_cache_{index_hash}"
                
                if rag_file.exists():
                    self.logger.info(f"Loading RAG index from compressed file: {rag_file}")
                    
                    # RAG indices are stored as tar.gz files, need to extract first
                    import tempfile
                    import tarfile
                    import shutil
                    
                    temp_dir = Path(tempfile.mkdtemp())
                    try:
                        # Extract the tar.gz file
                        with tarfile.open(rag_file, 'r:gz') as tar:
                            # Use data filter for security (Python 3.12+)
                            try:
                                tar.extractall(temp_dir, filter='data')
                            except TypeError:
                                # Fallback for older Python versions
                                tar.extractall(temp_dir)
                        
                        # Find the extracted index directory
                        index_path = temp_dir / "rag_index"
                        if not index_path.exists():
                            # Look for any directory that might contain the index
                            subdirs = [d for d in temp_dir.iterdir() if d.is_dir()]
                            if subdirs:
                                index_path = subdirs[0]
                        
                        if index_path.exists():
                            self.logger.info(f"Extracted index to: {index_path}")
                            from txtai.embeddings import Embeddings
                            self.rag_index = Embeddings()
                            self.rag_index.load(str(index_path))
                            self.logger.info("✅ RAG index loaded successfully from extracted file")
                            return True
                        else:
                            self.logger.error(f"Could not find extracted index directory in: {temp_dir}")
                            return False
                            
                    finally:
                        # Clean up temp directory
                        if temp_dir.exists():
                            shutil.rmtree(temp_dir)
                else:
                    self.logger.error(f"RAG index file not found: {rag_file}")
                    return False
                    
        except Exception as e:
            self.logger.error(f"❌ Failed to load RAG index: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def test_queries(self, queries: List[str]):
        """Test a list of queries against the loaded RAG index."""
        if not self.rag_index:
            self.logger.error("No RAG index loaded. Use load_rag_index() first.")
            return
        
        self.logger.info(f"🔍 Testing {len(queries)} queries against RAG index...")
        
        for i, query in enumerate(queries, 1):
            self.logger.info(f"\n--- Query {i}: '{query}' ---")
            
            try:
                # Perform search - txtai.search() returns (id, score) tuples
                # We need to use search() to get IDs, then retrieve documents separately
                search_results = self.rag_index.search(query, limit=5)
                self.logger.info(f"Query returned {len(search_results)} results")
                
                # Debug: Show what search_results actually contains
                print(f"DEBUG: search_results type: {type(search_results)}")
                print(f"DEBUG: search_results length: {len(search_results)}")
                if search_results:
                    print(f"DEBUG: first result type: {type(search_results[0])}")
                    print(f"DEBUG: first result: {search_results[0]}")
                    if hasattr(search_results[0], '__len__'):
                        print(f"DEBUG: first result length: {len(search_results[0])}")

                # Get the actual document content for each result
                for j, result in enumerate(search_results, 1):
                    # Handle different result formats
                    if isinstance(result, (list, tuple)) and len(result) >= 2:
                        doc_id, score = result[0], result[1]
                    elif isinstance(result, dict):
                        doc_id = result.get('id', result.get('document', 0))
                        score = result.get('score', 0.0)
                    else:
                        print(f"DEBUG: Unexpected result format: {result} (type: {type(result)})")
                        continue
                    self.logger.info(f"\nResult {j}:")
                    self.logger.info(f"  Document ID: {doc_id}")
                    self.logger.info(f"  Score: {score:.4f}")
                    
                    # Retrieve the actual document content
                    try:
                        # Debug: show what attributes the RAG index has
                        if j == 1:  # Only show this once per query
                            self.logger.info(f"  RAG index attributes: {dir(self.rag_index)}")
                            if hasattr(self.rag_index, 'index'):
                                self.logger.info(f"  Index object attributes: {dir(self.rag_index.index)}")
                            
                            # Try to get document count
                            if hasattr(self.rag_index, 'count'):
                                try:
                                    doc_count = self.rag_index.count()
                                    self.logger.info(f"  Document count: {doc_count}")
                                except Exception as e:
                                    self.logger.info(f"  Error getting count: {e}")
                            
                            # Check database type and content
                            if hasattr(self.rag_index, 'database'):
                                db = self.rag_index.database
                                self.logger.info(f"  Database type: {type(db)}")
                                if hasattr(db, '__len__'):
                                    try:
                                        db_len = len(db)
                                        self.logger.info(f"  Database length: {db_len}")
                                    except Exception as e:
                                        self.logger.info(f"  Error getting database length: {e}")
                        
                        # Try to get document by ID
                        if hasattr(self.rag_index, 'documents') and self.rag_index.documents:
                            if doc_id < len(self.rag_index.documents):
                                doc = self.rag_index.documents[doc_id]
                                if isinstance(doc, dict):
                                    text = doc.get('text', '')
                                    metadata = doc.get('metadata', {})
                                else:
                                    text = str(doc)
                                    metadata = {}
                            else:
                                text = f"Document {doc_id} not found in index"
                                metadata = {}
                        elif hasattr(self.rag_index, 'database') and self.rag_index.database:
                            # Try through the database attribute
                            try:
                                if hasattr(self.rag_index.database, 'get'):
                                    doc = self.rag_index.database.get(doc_id)
                                    if doc:
                                        if isinstance(doc, dict):
                                            text = doc.get('text', '')
                                            metadata = doc.get('metadata', {})
                                        else:
                                            text = str(doc)
                                            metadata = {}
                                    else:
                                        text = f"Document {doc_id} not found in database"
                                        metadata = {}
                                else:
                                    text = f"Database exists but no get method: {type(self.rag_index.database)}"
                                    metadata = {}
                            except Exception as e:
                                text = f"Error accessing database: {e}"
                                metadata = {}
                        elif hasattr(self.rag_index, 'ids') and self.rag_index.ids:
                            # Try through the ids attribute
                            try:
                                # Try to access the ids object directly
                                if hasattr(self.rag_index.ids, '__getitem__'):
                                    doc_id_value = self.rag_index.ids[doc_id]
                                    text = f"Document ID {doc_id} maps to: {doc_id_value}"
                                    metadata = {}
                                else:
                                    text = f"IDs object exists but no __getitem__: {type(self.rag_index.ids)}"
                                    metadata = {}
                            except Exception as e:
                                text = f"Error accessing ids: {e}"
                                metadata = {}
                        elif hasattr(self.rag_index, 'database') and self.rag_index.database:
                            # Try through the database attribute
                            try:
                                if hasattr(self.rag_index.database, 'get'):
                                    doc = self.rag_index.database.get(doc_id)
                                    if doc:
                                        if isinstance(doc, dict):
                                            text = doc.get('text', '')
                                            metadata = doc.get('metadata', {})
                                        else:
                                            text = str(doc)
                                            metadata = {}
                                    else:
                                        text = f"Document {doc_id} not found in database"
                                        metadata = {}
                                else:
                                    text = f"Database exists but no get method: {type(self.rag_index.database)}"
                                    metadata = {}
                            except Exception as e:
                                text = f"Error accessing database: {e}"
                                metadata = {}
                        elif hasattr(self.rag_index, 'query'):
                            # Try using the query method to get document content
                            try:
                                # Try to query for the specific document ID
                                query_result = self.rag_index.query(f"id:{doc_id}")
                                if query_result:
                                    if isinstance(query_result, list) and len(query_result) > 0:
                                        doc = query_result[0]
                                        if isinstance(doc, dict):
                                            text = doc.get('text', '')
                                            metadata = doc.get('metadata', {})
                                        else:
                                            text = str(doc)
                                            metadata = {}
                                    else:
                                        text = f"Query returned: {query_result}"
                                        metadata = {}
                                else:
                                    text = f"Query for id:{doc_id} returned nothing"
                                    metadata = {}
                            except Exception as e:
                                text = f"Error using query method: {e}"
                                metadata = {}
                        else:
                            # Try alternative method to get document content
                            text = f"Document {doc_id} (content not accessible - no documents attribute)"
                            metadata = {}
                        
                        # Show content preview
                        if text and not text.startswith("Document") and not text.startswith("Error"):
                            preview = text[:200] + "..." if len(text) > 200 else text
                            self.logger.info(f"  Content: {preview}")
                        else:
                            self.logger.info(f"  Content: {text}")
                        
                        # Show metadata if available
                        if metadata:
                            self.logger.info(f"  Metadata: {metadata}")
                            
                    except Exception as e:
                        self.logger.warning(f"  Could not retrieve document content: {e}")
                        text = f"Error retrieving document {doc_id}: {e}"
                        metadata = {}
                
            except Exception as e:
                self.logger.error(f"❌ Query failed: {e}")
    
    def build_fresh_fact_checker_rag(self):
        """Build a fresh fact-checker RAG index to see what happens."""
        try:
            self.logger.info("🔧 Building fresh fact-checker RAG index...")
            
            # Mock synthesis and statistical results
            mock_synthesis = {'report_hash': 'mock'}
            mock_stats = {'stats_hash': 'mock'}
            
            # Call the orchestrator's method
            rag_index = self.orchestrator._build_fact_checker_rag_index(mock_synthesis, mock_stats)
            self.logger.info("✅ Fresh fact-checker RAG index built successfully")
            
            # Test it
            self.rag_index = rag_index
            test_queries = [
                "framework dimensions list definition",
                "compersion vs compassion",
                "cohesive flourishing framework"
            ]
            
            self.test_queries(test_queries)
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to build fresh RAG index: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def interactive_mode(self):
        """Run interactive testing mode."""
        print("\n" + "="*60)
        print("RAG TESTING HARNESS - INTERACTIVE MODE")
        print("="*60)
        
        while True:
            print("\nOptions:")
            print("1. Test specific queries")
            print("2. Build fresh fact-checker RAG index")
            print("3. Load different RAG index")
            print("4. Show experiment info")
            print("5. Exit")
            
            choice = input("\nEnter choice (1-5): ").strip()
            
            if choice == "1":
                queries = input("Enter queries (comma-separated): ").strip()
                if queries:
                    query_list = [q.strip() for q in queries.split(",")]
                    self.test_queries(query_list)
            
            elif choice == "2":
                self.build_fresh_fact_checker_rag()
            
            elif choice == "3":
                index_hash = input("Enter RAG index hash (or press Enter for auto-detect): ").strip()
                if index_hash:
                    self.load_rag_index(index_hash)
                else:
                    self.load_rag_index()
            
            elif choice == "4":
                self.examine_existing_rag_indices()
            
            elif choice == "5":
                print("Exiting...")
                break
            
            else:
                print("Invalid choice. Please enter 1-5.")


def main():
    parser = argparse.ArgumentParser(description="RAG Testing Harness for Discernus")
    parser.add_argument("experiment_path", help="Path to experiment directory")
    parser.add_argument("--queries", nargs="+", help="Test specific queries")
    parser.add_argument("--build-fresh", action="store_true", help="Build fresh fact-checker RAG index")
    parser.add_argument("--interactive", action="store_true", help="Run interactive mode")
    
    args = parser.parse_args()
    
    # Initialize harness
    harness = RAGTestingHarness(args.experiment_path)
    
    # Load experiment
    if not harness.load_experiment():
        print("❌ Failed to load experiment. Exiting.")
        return 1
    
    # Examine existing RAG indices
    harness.examine_existing_rag_indices()
    
    # Load most recent RAG index
    if not harness.load_rag_index():
        print("❌ Failed to load RAG index. Exiting.")
        return 1
    
    # Run based on arguments
    if args.build_fresh:
        harness.build_fresh_fact_checker_rag()
    elif args.queries:
        harness.test_queries(args.queries)
    elif args.interactive:
        harness.interactive_mode()
    else:
        # Default: test some common queries
        default_queries = [
            "framework dimensions list definition",
            "compersion vs compassion", 
            "cohesive flourishing framework",
            "analysis results",
            "evidence extraction"
        ]
        harness.test_queries(default_queries)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
