#!/usr/bin/env python3
"""
Framework-Agile Synthesis Orchestrator for Discernus
====================================================

This module provides the SynthesisOrchestrator, a robust, framework-agile
component responsible for creating a compact, structured data manifest from a
large collection of verbose analysis artifacts.

Core Principles:
1.  **Framework-Agile**: The orchestrator is not hardcoded to any specific
    framework. It dynamically discovers the required data schema by inspecting
    the framework file used for the experiment.
2.  **Kryptonite-Immune Parsing**: It is designed to be resilient to malformed
    analysis artifacts. It uses a simple, robust `try/except` block to
    validate the integrity of each artifact's core JSON response, quarantining
    failures rather than crashing.
3.  **Deterministic and THIN**: The logic is purely deterministic Python. It
    performs no complex analysis itself, leaving that to LLM agents. Its sole
    job is data extraction, validation, and aggregation.
"""

import json
import csv
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Tuple, Set

class SynthesisOrchestratorError(Exception):
    """Custom exception for the SynthesisOrchestrator."""
    pass

class SynthesisOrchestrator:
    """
    Orchestrates the creation of a structured data manifest from analysis artifacts.
    """

    def generate_manifest(
        self,
        artifact_paths: List[Path],
    ) -> Tuple[List[Dict[str, Any]], List[str]]:
        """
        Generates a structured data manifest from a list of analysis artifacts.
        It dynamically discovers the schema from the first valid artifact.
        """
        quarantined_artifacts: List[str] = []
        manifest_rows: List[Dict[str, Any]] = []
        header_keys: Set[str] = set()

        for artifact_path in artifact_paths:
            try:
                with open(artifact_path, 'r', encoding='utf-8') as f:
                    outer_json = json.load(f)

                raw_response_str = outer_json.get("raw_analysis_response")
                if not raw_response_str:
                    raise ValueError("Artifact missing 'raw_analysis_response'")

                if raw_response_str.startswith("```json"):
                    raw_response_str = raw_response_str[7:-4]

                inner_json = json.loads(raw_response_str)

                analysis_key = next(iter(inner_json.get("document_analyses", {})), None)
                if not analysis_key:
                    if "scores" in inner_json:
                        analysis_data = inner_json
                    else:
                        raise ValueError("Could not find analysis data block.")
                else:
                    analysis_data = inner_json["document_analyses"][analysis_key]

                if not header_keys:
                    header_keys.add('artifact_hash')
                    header_keys.add('document_name')
                    header_keys.update(analysis_data.get("scores", {}).keys())
                    # Only add a few specific, known top-level metrics if they exist
                    for key in ["mc_sci_score", "PSCI_Score", "Salience_Concentration"]:
                        if key in analysis_data:
                            header_keys.add(key)

                doc_hash = outer_json.get("input_artifacts", {}).get("document_hashes", [None])[0]
                row = {
                    'artifact_hash': artifact_path.name,
                    'document_name': f"doc_{doc_hash[:12]}",
                    '_has_scores': False
                }

                scores_data = analysis_data.get("scores", {})
                if scores_data:
                    row['_has_scores'] = True

                for key in header_keys:
                    if key not in row:
                        if key in scores_data:
                            score_value = scores_data[key]
                            if isinstance(score_value, dict) and "intensity" in score_value:
                                row[key] = score_value.get("intensity")
                            else:
                                row[key] = score_value
                        else:
                            # Only pull top-level values that are numeric
                            value = analysis_data.get(key)
                            if isinstance(value, (int, float)):
                                row[key] = value
                
                manifest_rows.append(row)

            except (IOError, json.JSONDecodeError, ValueError, KeyError):
                quarantined_artifacts.append(artifact_path.name)
        
        final_header = sorted(list(header_keys))
        final_manifest = []
        for row in manifest_rows:
            if row.pop('_has_scores', False):
                standardized_row = {key: row.get(key) for key in final_header}
                final_manifest.append(standardized_row)
            else:
                quarantined_artifacts.append(row['artifact_hash'])
        
        return final_manifest, quarantined_artifacts

    def generate_hash_cross_referenced_csv(
        self, 
        artifact_paths: List[Path], 
        output_dir: Path
    ) -> Tuple[Path, Path, List[str]]:
        """
        Generate hash cross-referenced CSV files via progressive appending.
        
        Process: Opens CSV files once, appends each artifact's data as processed,
        closes files when complete. No in-memory accumulation.
        
        Returns:
            (scores_csv_path, evidence_csv_path, quarantined_files)
        """
        quarantined_artifacts: List[str] = []
        
        # Create temporary CSV files for progressive writing
        scores_temp_path = output_dir / "scores_temp.csv"
        evidence_temp_path = output_dir / "evidence_temp.csv"
        
        # Track headers for dynamic discovery
        header_keys: Set[str] = set()
        scores_rows: List[Dict[str, Any]] = []
        evidence_rows: List[Dict[str, Any]] = []
        
        # First pass: collect all data and discover schema
        for artifact_path in artifact_paths:
            try:
                with open(artifact_path, 'r', encoding='utf-8') as f:
                    outer_json = json.load(f)

                raw_response_str = outer_json.get("raw_analysis_response")
                if not raw_response_str:
                    raise ValueError("Artifact missing 'raw_analysis_response'")

                if raw_response_str.startswith("```json"):
                    raw_response_str = raw_response_str[7:-4]

                inner_json = json.loads(raw_response_str)

                # Extract document analysis data
                analysis_key = next(iter(inner_json.get("document_analyses", {})), None)
                if not analysis_key:
                    if "scores" in inner_json:
                        analysis_data = inner_json
                        document_name = "unknown_doc"
                    else:
                        raise ValueError("Could not find analysis data block.")
                else:
                    analysis_data = inner_json["document_analyses"][analysis_key]
                    document_name = analysis_key

                # Get artifact hash from filename
                artifact_hash = artifact_path.name
                
                # Extract scores data
                scores_data = analysis_data.get("scores", {})
                if not scores_data:
                    raise ValueError("No scores data found")

                # Build scores row
                scores_row = {
                    'artifact_hash': artifact_hash,
                    'document_name': document_name
                }
                
                # Add scores (extract intensity values)
                for dimension, score_data in scores_data.items():
                    if isinstance(score_data, dict) and "intensity" in score_data:
                        scores_row[dimension] = score_data["intensity"]
                        header_keys.add(dimension)
                    else:
                        scores_row[dimension] = score_data
                        header_keys.add(dimension)
                
                # Add any top-level numeric metrics
                for key in ["mc_sci_score", "PSCI_Score", "Salience_Concentration"]:
                    if key in analysis_data and isinstance(analysis_data[key], (int, float)):
                        scores_row[key] = analysis_data[key]
                        header_keys.add(key)

                scores_rows.append(scores_row)

                # Extract evidence data
                evidence_data = analysis_data.get("evidence", {})
                for dimension, quotes in evidence_data.items():
                    if isinstance(quotes, list):
                        for quote_id, quote_text in enumerate(quotes, 1):
                            evidence_rows.append({
                                'artifact_hash': artifact_hash,
                                'dimension': dimension,
                                'quote_id': quote_id,
                                'quote_text': quote_text,
                                'context_type': 'primary'  # Could be enhanced with more context analysis
                            })

            except (IOError, json.JSONDecodeError, ValueError, KeyError) as e:
                quarantined_artifacts.append(artifact_path.name)
                continue

        # Define final headers
        scores_headers = ['artifact_hash', 'document_name'] + sorted(header_keys)
        evidence_headers = ['artifact_hash', 'dimension', 'quote_id', 'quote_text', 'context_type']

        # Write scores CSV
        with open(scores_temp_path, 'w', newline='', encoding='utf-8') as scores_file:
            writer = csv.DictWriter(scores_file, fieldnames=scores_headers)
            writer.writeheader()
            for row in scores_rows:
                # Ensure all headers are present with None for missing values
                standardized_row = {header: row.get(header) for header in scores_headers}
                writer.writerow(standardized_row)

        # Write evidence CSV
        with open(evidence_temp_path, 'w', newline='', encoding='utf-8') as evidence_file:
            writer = csv.DictWriter(evidence_file, fieldnames=evidence_headers)
            writer.writeheader()
            writer.writerows(evidence_rows)

        # Generate hash-based filenames
        scores_hash = self._hash_file_contents(scores_temp_path)[:16]
        evidence_hash = self._hash_file_contents(evidence_temp_path)[:16]
        
        scores_final_path = output_dir / f"{scores_hash}_scores.csv"
        evidence_final_path = output_dir / f"{evidence_hash}_evidence.csv"

        # Move to final hash-based filenames
        scores_temp_path.rename(scores_final_path)
        evidence_temp_path.rename(evidence_final_path)

        return scores_final_path, evidence_final_path, quarantined_artifacts

    def generate_optimized_hash_csv(
        self, 
        artifact_paths: List[Path], 
        output_dir: Path
    ) -> Tuple[Path, Path, Path, List[str]]:
        """
        Generate optimized hash cross-referenced CSV files with maximum token efficiency.
        
        Optimizations:
        - Short artifact IDs (A1, A2, A3) instead of full hashes
        - Abbreviated dimension names (D=Dignity, H=Hope, etc.)
        - Artifact lookup table for hash cross-reference
        
        Returns:
            (scores_csv_path, evidence_csv_path, lookup_csv_path, quarantined_files)
        """
        quarantined_artifacts: List[str] = []
        
        # Create temporary CSV files
        scores_temp_path = output_dir / "scores_temp.csv"
        evidence_temp_path = output_dir / "evidence_temp.csv" 
        lookup_temp_path = output_dir / "lookup_temp.csv"
        
        # Track data for processing
        header_keys: Set[str] = set()
        scores_rows: List[Dict[str, Any]] = []
        evidence_rows: List[Dict[str, Any]] = []
        artifact_lookup: Dict[str, str] = {}  # short_id -> full_hash
        
        # Dimension abbreviations for token efficiency
        dimension_abbrevs = {
            'Dignity': 'DIG', 'Tribalism': 'TRB', 'Truth': 'TRU', 'Manipulation': 'MAN',
            'Justice': 'JUS', 'Resentment': 'RES', 'Hope': 'HOP', 'Fear': 'FEA',
            'Pragmatism': 'PRA', 'Fantasy': 'FAN'
        }
        
        # Process artifacts and assign short IDs
        for i, artifact_path in enumerate(artifact_paths, 1):
            try:
                with open(artifact_path, 'r', encoding='utf-8') as f:
                    outer_json = json.load(f)

                raw_response_str = outer_json.get("raw_analysis_response")
                if not raw_response_str:
                    raise ValueError("Artifact missing 'raw_analysis_response'")

                if raw_response_str.startswith("```json"):
                    raw_response_str = raw_response_str[7:-4]

                inner_json = json.loads(raw_response_str)

                # Extract document analysis data
                analysis_key = next(iter(inner_json.get("document_analyses", {})), None)
                if not analysis_key:
                    if "scores" in inner_json:
                        analysis_data = inner_json
                        document_name = "unknown_doc"
                    else:
                        raise ValueError("Could not find analysis data block.")
                else:
                    analysis_data = inner_json["document_analyses"][analysis_key]
                    document_name = analysis_key

                # Assign short artifact ID
                artifact_hash = artifact_path.name
                short_id = f"A{i}"
                artifact_lookup[short_id] = artifact_hash
                
                # Extract scores data
                scores_data = analysis_data.get("scores", {})
                if not scores_data:
                    raise ValueError("No scores data found")

                # Build optimized scores row
                scores_row = {
                    'aid': short_id,  # Short artifact ID
                    'doc': document_name[:20]  # Truncated document name
                }
                
                # Add scores with abbreviated dimension names
                for dimension, score_data in scores_data.items():
                    abbrev_dim = dimension_abbrevs.get(dimension, dimension[:3])
                    if isinstance(score_data, dict) and "intensity" in score_data:
                        scores_row[abbrev_dim] = score_data["intensity"]
                        header_keys.add(abbrev_dim)
                    else:
                        scores_row[abbrev_dim] = score_data
                        header_keys.add(abbrev_dim)
                
                # Add compact metrics
                for key in ["mc_sci_score", "PSCI_Score"]:
                    if key in analysis_data and isinstance(analysis_data[key], (int, float)):
                        short_key = key.replace("_score", "").replace("_", "")[:4]
                        scores_row[short_key] = analysis_data[key]
                        header_keys.add(short_key)

                scores_rows.append(scores_row)

                # Extract evidence data with optimizations
                evidence_data = analysis_data.get("evidence", {})
                for dimension, quotes in evidence_data.items():
                    abbrev_dim = dimension_abbrevs.get(dimension, dimension[:3])
                    if isinstance(quotes, list):
                        for quote_id, quote_text in enumerate(quotes, 1):
                            # Compress quote while preserving key meaning
                            compressed_quote = quote_text[:100] + "..." if len(quote_text) > 100 else quote_text
                            evidence_rows.append({
                                'aid': short_id,
                                'dim': abbrev_dim,
                                'qid': quote_id,
                                'txt': compressed_quote,
                                'typ': 'P'  # P=Primary, S=Supporting
                            })

            except (IOError, json.JSONDecodeError, ValueError, KeyError) as e:
                quarantined_artifacts.append(artifact_path.name)
                continue

        # Write optimized scores CSV
        scores_headers = ['aid', 'doc'] + sorted(header_keys)
        with open(scores_temp_path, 'w', newline='', encoding='utf-8') as scores_file:
            writer = csv.DictWriter(scores_file, fieldnames=scores_headers)
            writer.writeheader()
            for row in scores_rows:
                standardized_row = {header: row.get(header) for header in scores_headers}
                writer.writerow(standardized_row)

        # Write optimized evidence CSV
        evidence_headers = ['aid', 'dim', 'qid', 'txt', 'typ']
        with open(evidence_temp_path, 'w', newline='', encoding='utf-8') as evidence_file:
            writer = csv.DictWriter(evidence_file, fieldnames=evidence_headers)
            writer.writeheader()
            writer.writerows(evidence_rows)

        # Write artifact lookup table
        with open(lookup_temp_path, 'w', newline='', encoding='utf-8') as lookup_file:
            writer = csv.DictWriter(lookup_file, fieldnames=['short_id', 'artifact_hash', 'document_name'])
            writer.writeheader()
            for short_id, artifact_hash in artifact_lookup.items():
                # Find document name from scores_rows
                doc_name = next((row['doc'] for row in scores_rows if row['aid'] == short_id), 'unknown')
                writer.writerow({
                    'short_id': short_id,
                    'artifact_hash': artifact_hash,
                    'document_name': doc_name
                })

        # Generate hash-based filenames
        scores_hash = self._hash_file_contents(scores_temp_path)[:12]
        evidence_hash = self._hash_file_contents(evidence_temp_path)[:12] 
        lookup_hash = self._hash_file_contents(lookup_temp_path)[:12]
        
        scores_final_path = output_dir / f"{scores_hash}_scores.csv"
        evidence_final_path = output_dir / f"{evidence_hash}_evidence.csv"
        lookup_final_path = output_dir / f"{lookup_hash}_lookup.csv"

        # Move to final hash-based filenames
        scores_temp_path.rename(scores_final_path)
        evidence_temp_path.rename(evidence_final_path)
        lookup_temp_path.rename(lookup_final_path)

        return scores_final_path, evidence_final_path, lookup_final_path, quarantined_artifacts

    def generate_conservative_hash_csv(
        self, 
        artifact_paths: List[Path], 
        output_dir: Path
    ) -> Tuple[Path, Path, Path, List[str]]:
        """
        Generate conservatively optimized hash cross-referenced CSV files.
        
        Conservative optimizations for academic clarity:
        - Short artifact IDs (A1, A2, A3) instead of full hashes [KEEP - big win]
        - Full dimension names (Dignity, Hope, etc.) [RESTORE - for LLM clarity]
        - Full quote text preserved [RESTORE - no truncation]
        - Compact column names (aid, txt) [KEEP - minimal impact]
        
        Returns:
            (scores_csv_path, evidence_csv_path, lookup_csv_path, quarantined_files)
        """
        quarantined_artifacts: List[str] = []
        
        # Create temporary CSV files
        scores_temp_path = output_dir / "scores_temp.csv"
        evidence_temp_path = output_dir / "evidence_temp.csv" 
        lookup_temp_path = output_dir / "lookup_temp.csv"
        
        # Track data for processing
        header_keys: Set[str] = set()
        scores_rows: List[Dict[str, Any]] = []
        evidence_rows: List[Dict[str, Any]] = []
        artifact_lookup: Dict[str, str] = {}  # short_id -> full_hash
        
        # Process artifacts and assign short IDs
        for i, artifact_path in enumerate(artifact_paths, 1):
            try:
                with open(artifact_path, 'r', encoding='utf-8') as f:
                    outer_json = json.load(f)

                raw_response_str = outer_json.get("raw_analysis_response")
                if not raw_response_str:
                    raise ValueError("Artifact missing 'raw_analysis_response'")

                if raw_response_str.startswith("```json"):
                    raw_response_str = raw_response_str[7:-4]

                inner_json = json.loads(raw_response_str)

                # Extract document analysis data
                analysis_key = next(iter(inner_json.get("document_analyses", {})), None)
                if not analysis_key:
                    if "scores" in inner_json:
                        analysis_data = inner_json
                        document_name = "unknown_doc"
                    else:
                        raise ValueError("Could not find analysis data block.")
                else:
                    analysis_data = inner_json["document_analyses"][analysis_key]
                    document_name = analysis_key

                # Assign short artifact ID
                artifact_hash = artifact_path.name
                short_id = f"A{i}"
                artifact_lookup[short_id] = artifact_hash
                
                # Extract scores data
                scores_data = analysis_data.get("scores", {})
                if not scores_data:
                    raise ValueError("No scores data found")

                # Build conservatively optimized scores row
                scores_row = {
                    'aid': short_id,  # Short artifact ID (keep optimization)
                    'doc': document_name[:30]  # Slightly longer document name
                }
                
                # Add scores with FULL dimension names (restore for LLM clarity)
                for dimension, score_data in scores_data.items():
                    if isinstance(score_data, dict) and "intensity" in score_data:
                        scores_row[dimension] = score_data["intensity"]  # Full name: Dignity, Hope, etc.
                        header_keys.add(dimension)
                    else:
                        scores_row[dimension] = score_data
                        header_keys.add(dimension)
                
                # Add compact metrics (keep minor optimization)
                for key in ["mc_sci_score", "PSCI_Score"]:
                    if key in analysis_data and isinstance(analysis_data[key], (int, float)):
                        short_key = key.replace("_score", "").replace("_", "")[:4]
                        scores_row[short_key] = analysis_data[key]
                        header_keys.add(short_key)

                scores_rows.append(scores_row)

                # Extract evidence data with FULL preservation (no compression)
                evidence_data = analysis_data.get("evidence", {})
                for dimension, quotes in evidence_data.items():
                    if isinstance(quotes, list):
                        for quote_id, quote_text in enumerate(quotes, 1):
                            # Preserve FULL quote text (no truncation)
                            evidence_rows.append({
                                'aid': short_id,  # Short ID (keep optimization)
                                'dim': dimension,  # Full dimension name (restore clarity)
                                'qid': quote_id,
                                'txt': quote_text,  # Full quote text (restore academic rigor)
                                'typ': 'primary'  # Full context type name
                            })

            except (IOError, json.JSONDecodeError, ValueError, KeyError) as e:
                quarantined_artifacts.append(artifact_path.name)
                continue

        # Write conservative scores CSV
        scores_headers = ['aid', 'doc'] + sorted(header_keys)
        with open(scores_temp_path, 'w', newline='', encoding='utf-8') as scores_file:
            writer = csv.DictWriter(scores_file, fieldnames=scores_headers)
            writer.writeheader()
            for row in scores_rows:
                standardized_row = {header: row.get(header) for header in scores_headers}
                writer.writerow(standardized_row)

        # Write conservative evidence CSV
        evidence_headers = ['aid', 'dim', 'qid', 'txt', 'typ']
        with open(evidence_temp_path, 'w', newline='', encoding='utf-8') as evidence_file:
            writer = csv.DictWriter(evidence_file, fieldnames=evidence_headers)
            writer.writeheader()
            writer.writerows(evidence_rows)

        # Write artifact lookup table
        with open(lookup_temp_path, 'w', newline='', encoding='utf-8') as lookup_file:
            writer = csv.DictWriter(lookup_file, fieldnames=['short_id', 'artifact_hash', 'document_name'])
            writer.writeheader()
            for short_id, artifact_hash in artifact_lookup.items():
                # Find document name from scores_rows
                doc_name = next((row['doc'] for row in scores_rows if row['aid'] == short_id), 'unknown')
                writer.writerow({
                    'short_id': short_id,
                    'artifact_hash': artifact_hash,
                    'document_name': doc_name
                })

        # Generate hash-based filenames
        scores_hash = self._hash_file_contents(scores_temp_path)[:12]
        evidence_hash = self._hash_file_contents(evidence_temp_path)[:12] 
        lookup_hash = self._hash_file_contents(lookup_temp_path)[:12]
        
        scores_final_path = output_dir / f"{scores_hash}_scores.csv"
        evidence_final_path = output_dir / f"{evidence_hash}_evidence.csv"
        lookup_final_path = output_dir / f"{lookup_hash}_lookup.csv"

        # Move to final hash-based filenames
        scores_temp_path.rename(scores_final_path)
        evidence_temp_path.rename(evidence_final_path)
        lookup_temp_path.rename(lookup_final_path)

        return scores_final_path, evidence_final_path, lookup_final_path, quarantined_artifacts

    def _hash_file_contents(self, file_path: Path) -> str:
        """Generate SHA256 hash of file contents for provenance."""
        with open(file_path, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()

if __name__ == '__main__':
    print("Synthesis Orchestrator Module") 