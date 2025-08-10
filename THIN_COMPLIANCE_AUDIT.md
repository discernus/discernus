# THIN Architecture Compliance Audit Report
Generated: 2025-08-10 07:35:52

## Executive Summary
- **Total Violations**: 230
- **Critical Violations**: 0
- **High Priority Violations**: 156
- **Agents Audited**: 14
- **Non-Compliant Agents**: 12

## Violation Breakdown

- **INLINE_PROMPTS**: 149 violations
- **EXCESSIVE_PARSING**: 72 violations
- **MISSING_YAML**: 7 violations
- **COMPLEX_PARSING_METHODS**: 2 violations

## Detailed Agent Analysis

### EnhancedAnalysisAgent
**Violations**: 43

🔸 **EXCESSIVE_PARSING**: Regex parsing: from discernus.core.local_artifact_storage import LocalArtifactStorage
   📍 /Volumes/code/discernus/discernus/agents/EnhancedAnalysisAgent/analysis_cache.py:15
🔸 **EXCESSIVE_PARSING**: Regex parsing: from discernus.core.audit_logger import AuditLogger
   📍 /Volumes/code/discernus/discernus/agents/EnhancedAnalysisAgent/analysis_cache.py:16
🔸 **EXCESSIVE_PARSING**: Regex parsing: THIN Principle: Pure software caching infrastructure.
   📍 /Volumes/code/discernus/discernus/agents/EnhancedAnalysisAgent/analysis_cache.py:31
⚠️ **INLINE_PROMPTS**: F-string prompts: batch_content = f'{framework_content}{doc_content_hash}{model}'...
   📍 /Volumes/code/discernus/discernus/agents/EnhancedAnalysisAgent/analysis_cache.py:59
🔸 **EXCESSIVE_PARSING**: JSON parsing: cached_result = json.loads(cached_content.decode('utf-8'))
   📍 /Volumes/code/discernus/discernus/agents/EnhancedAnalysisAgent/analysis_cache.py:87
⚠️ **INLINE_PROMPTS**: F-string prompts: print(f"⚠️ Cache hit but failed to load content: {e}")...
   📍 /Volumes/code/discernus/discernus/agents/EnhancedAnalysisAgent/analysis_cache.py:101
⚠️ **INLINE_PROMPTS**: F-string prompts: print(f"🔍 No cache hit for {batch_id} - will perform analysis...")...
   📍 /Volumes/code/discernus/discernus/agents/EnhancedAnalysisAgent/analysis_cache.py:106
🔸 **EXCESSIVE_PARSING**: Regex parsing: from discernus.core.local_artifact_storage import LocalArtifactStorage
   📍 /Volumes/code/discernus/discernus/agents/EnhancedAnalysisAgent/document_processor.py:15
⚠️ **INLINE_PROMPTS**: F-string prompts: content_for_analysis = f"[Binary content, base64 encoded: {len(doc_content)} chars]"...
   📍 /Volumes/code/discernus/discernus/agents/EnhancedAnalysisAgent/document_processor.py:57
⚠️ **INLINE_PROMPTS**: F-string prompts: formatted_docs.append(f"Document {i+1} ({doc.filename}):\n{doc.content}")...
   📍 /Volumes/code/discernus/discernus/agents/EnhancedAnalysisAgent/document_processor.py:102
⚠️ **INLINE_PROMPTS**: F-string prompts: formatted_docs.append(f"Document {i+1} ({doc.filename}):\n{doc.content}")...
   📍 /Volumes/code/discernus/discernus/agents/EnhancedAnalysisAgent/llm_analyzer.py:95
🔸 **EXCESSIVE_PARSING**: Regex parsing: from discernus.core.security_boundary import ExperimentSecurityBoundary, SecurityError
   📍 /Volumes/code/discernus/discernus/agents/EnhancedAnalysisAgent/main.py:27
🔸 **EXCESSIVE_PARSING**: Regex parsing: from discernus.core.audit_logger import AuditLogger
   📍 /Volumes/code/discernus/discernus/agents/EnhancedAnalysisAgent/main.py:28
🔸 **EXCESSIVE_PARSING**: Regex parsing: from discernus.core.local_artifact_storage import LocalArtifactStorage
   📍 /Volumes/code/discernus/discernus/agents/EnhancedAnalysisAgent/main.py:29
⚠️ **INLINE_PROMPTS**: F-string prompts: print(f"🧠 {self.agent_name} initialized with mathematical validation")...
   📍 /Volumes/code/discernus/discernus/agents/EnhancedAnalysisAgent/main.py:69
🔸 **EXCESSIVE_PARSING**: Regex parsing: json_match = re.search(json_pattern, result_content, re.DOTALL)
   📍 /Volumes/code/discernus/discernus/agents/EnhancedAnalysisAgent/main.py:154
🔸 **EXCESSIVE_PARSING**: JSON parsing: analysis_data = json.loads(json_match.group(1).strip())
   📍 /Volumes/code/discernus/discernus/agents/EnhancedAnalysisAgent/main.py:160
⚠️ **INLINE_PROMPTS**: F-string prompts: # session_base_content = f'{framework_content}{doc_content_hash}{model}'...
   📍 /Volumes/code/discernus/discernus/agents/EnhancedAnalysisAgent/main.py:240
⚠️ **INLINE_PROMPTS**: F-string prompts: # session_id = f"ensemble_session_{hashlib.sha256(session_base_content.encode()).hexdigest()[:12]}"...
   📍 /Volumes/code/discernus/discernus/agents/EnhancedAnalysisAgent/main.py:241
⚠️ **INLINE_PROMPTS**: F-string prompts: #     batch_id = f"batch_{hashlib.sha256(f'{session_base_content}{ensemble_run}'.encode()).hexdigest...
   📍 /Volumes/code/discernus/discernus/agents/EnhancedAnalysisAgent/main.py:245
⚠️ **INLINE_PROMPTS**: F-string prompts: #     batch_id = f"batch_{hashlib.sha256(session_base_content.encode()).hexdigest()[:12]}"...
   📍 /Volumes/code/discernus/discernus/agents/EnhancedAnalysisAgent/main.py:247
⚠️ **INLINE_PROMPTS**: F-string prompts: batch_id = f"batch_{hashlib.sha256(f'{framework_content}{doc_content_hash}{model}'.encode()).hexdige...
   📍 /Volumes/code/discernus/discernus/agents/EnhancedAnalysisAgent/main.py:250
🔸 **EXCESSIVE_PARSING**: JSON parsing: cached_result = json.loads(cached_content.decode('utf-8'))
   📍 /Volumes/code/discernus/discernus/agents/EnhancedAnalysisAgent/main.py:275
⚠️ **INLINE_PROMPTS**: F-string prompts: print(f"🔍 No cache hit for {batch_id} - performing analysis...")...
   📍 /Volumes/code/discernus/discernus/agents/EnhancedAnalysisAgent/main.py:307
⚠️ **INLINE_PROMPTS**: F-string prompts: "original_filename": doc.get('filename', f'doc_{i+1}'),...
   📍 /Volumes/code/discernus/discernus/agents/EnhancedAnalysisAgent/main.py:325
⚠️ **INLINE_PROMPTS**: F-string prompts: "original_filename": doc.get('filename', f'doc_{i+1}'),...
   📍 /Volumes/code/discernus/discernus/agents/EnhancedAnalysisAgent/main.py:333
⚠️ **INLINE_PROMPTS**: F-string prompts: frameworks=f"=== FRAMEWORK 1 (base64 encoded) ===\n{framework_b64}\n",...
   📍 /Volumes/code/discernus/discernus/agents/EnhancedAnalysisAgent/main.py:354
⚠️ **INLINE_PROMPTS**: F-string prompts: #     print(f"    🔄 Using session-based caching: {session_id} (run {ensemble_run}/{total_ensemble_ru...
   📍 /Volumes/code/discernus/discernus/agents/EnhancedAnalysisAgent/main.py:387
⚠️ **INLINE_PROMPTS**: F-string prompts: #             print(f"    💾 Vertex AI cache hit: {cached_tokens} tokens reused")...
   📍 /Volumes/code/discernus/discernus/agents/EnhancedAnalysisAgent/main.py:408
⚠️ **INLINE_PROMPTS**: F-string prompts: print(f"💰 Document analysis cost: ${response_cost:.6f} ({total_tokens:,} tokens)")...
   📍 /Volumes/code/discernus/discernus/agents/EnhancedAnalysisAgent/main.py:457
⚠️ **INLINE_PROMPTS**: F-string prompts: print(f"⚠️ Error extracting cost information: {e}")...
   📍 /Volumes/code/discernus/discernus/agents/EnhancedAnalysisAgent/main.py:460
🔸 **EXCESSIVE_PARSING**: String splitting: "tokens_input": len(prompt_text.split()),
   📍 /Volumes/code/discernus/discernus/agents/EnhancedAnalysisAgent/main.py:486
🔸 **EXCESSIVE_PARSING**: String splitting: "tokens_output": len(result_content.split())
   📍 /Volumes/code/discernus/discernus/agents/EnhancedAnalysisAgent/main.py:487
🔸 **EXCESSIVE_PARSING**: Content parsing: "tokens_output": len(result_content.split())
   📍 /Volumes/code/discernus/discernus/agents/EnhancedAnalysisAgent/main.py:487
⚠️ **INLINE_PROMPTS**: F-string prompts: print(f"✅ Enhanced analysis complete: {batch_id} ({duration:.1f}s)")...
   📍 /Volumes/code/discernus/discernus/agents/EnhancedAnalysisAgent/main.py:548
⚠️ **INLINE_PROMPTS**: F-string prompts: raise EnhancedAnalysisAgentError(f"Enhanced analysis failed: {e}")...
   📍 /Volumes/code/discernus/discernus/agents/EnhancedAnalysisAgent/main.py:569
⚠️ **INLINE_PROMPTS**: F-string prompts: f"=== DOCUMENT {document['index']} (base64 encoded) ===\n"...
   📍 /Volumes/code/discernus/discernus/agents/EnhancedAnalysisAgent/main.py:584
⚠️ **INLINE_PROMPTS**: F-string prompts: f"Filename: {document.get('filename', 'unknown')}\n"...
   📍 /Volumes/code/discernus/discernus/agents/EnhancedAnalysisAgent/main.py:585
🔸 **EXCESSIVE_PARSING**: Regex parsing: json_match = re.search(json_pattern, framework_content, re.DOTALL)
   📍 /Volumes/code/discernus/discernus/agents/EnhancedAnalysisAgent/framework_parser.py:46
🔸 **EXCESSIVE_PARSING**: JSON parsing: framework_config = json.loads(json_match.group(1))
   📍 /Volumes/code/discernus/discernus/agents/EnhancedAnalysisAgent/framework_parser.py:51
⚠️ **INLINE_PROMPTS**: F-string prompts: raise ValueError(f"Invalid JSON in framework appendix: {e}")...
   📍 /Volumes/code/discernus/discernus/agents/EnhancedAnalysisAgent/framework_parser.py:53
⚠️ **INLINE_PROMPTS**: F-string prompts: print(f"Warning: Dimension group '{group_name}' is not a list, skipping")...
   📍 /Volumes/code/discernus/discernus/agents/EnhancedAnalysisAgent/framework_parser.py:64
🔸 **COMPLEX_PARSING_METHODS**: Contains parse_* or extract_* methods
   📍 /Volumes/code/discernus/discernus/agents/EnhancedAnalysisAgent/framework_parser.py

### classification_agent
**Violations**: 3

⚠️ **MISSING_YAML**: No YAML prompt files found
   📍 /Volumes/code/discernus/discernus/agents/classification_agent
⚠️ **INLINE_PROMPTS**: F-string prompts: classifications[f"{metric_name}_classification"] = category...
   📍 /Volumes/code/discernus/discernus/agents/classification_agent/agent.py:44
⚠️ **INLINE_PROMPTS**: F-string prompts: classifications[f"{metric_name}_classification"] = "Unclassified"...
   📍 /Volumes/code/discernus/discernus/agents/classification_agent/agent.py:48

### comprehensive_knowledge_curator
**Violations**: 24

⚠️ **MISSING_YAML**: No YAML prompt files found
   📍 /Volumes/code/discernus/discernus/agents/comprehensive_knowledge_curator
🔸 **EXCESSIVE_PARSING**: Regex parsing: from discernus.core.local_artifact_storage import LocalArtifactStorage
   📍 /Volumes/code/discernus/discernus/agents/comprehensive_knowledge_curator/agent.py:41
⚠️ **INLINE_PROMPTS**: F-string prompts: self.logger.info(f"📚 Loaded cached comprehensive knowledge index: {index_hash[:12]}...")...
   📍 /Volumes/code/discernus/discernus/agents/comprehensive_knowledge_curator/agent.py:166
⚠️ **INLINE_PROMPTS**: F-string prompts: self.logger.info(f"✅ Built comprehensive knowledge graph: {len(documents)} items across {len(request...
   📍 /Volumes/code/discernus/discernus/agents/comprehensive_knowledge_curator/agent.py:233
⚠️ **INLINE_PROMPTS**: F-string prompts: self.logger.error(f"Comprehensive indexing failed: {str(e)}")...
   📍 /Volumes/code/discernus/discernus/agents/comprehensive_knowledge_curator/agent.py:244
⚠️ **INLINE_PROMPTS**: F-string prompts: types_str = ", ".join(f"'{t}'" for t in query.content_types)...
   📍 /Volumes/code/discernus/discernus/agents/comprehensive_knowledge_curator/agent.py:272
⚠️ **INLINE_PROMPTS**: F-string prompts: where_clauses.append(f"content_type IN ({types_str})")...
   📍 /Volumes/code/discernus/discernus/agents/comprehensive_knowledge_curator/agent.py:273
⚠️ **INLINE_PROMPTS**: F-string prompts: where_clauses.append(f"speaker = '{query.speaker_filter}'")...
   📍 /Volumes/code/discernus/discernus/agents/comprehensive_knowledge_curator/agent.py:275
⚠️ **INLINE_PROMPTS**: F-string prompts: where_clauses.append(f"document_id = '{query.document_filter}'")...
   📍 /Volumes/code/discernus/discernus/agents/comprehensive_knowledge_curator/agent.py:277
⚠️ **INLINE_PROMPTS**: F-string prompts: search_results = self.embeddings.search(f"select id, text, score, content_type, source_artifact, spe...
   📍 /Volumes/code/discernus/discernus/agents/comprehensive_knowledge_curator/agent.py:282
⚠️ **INLINE_PROMPTS**: F-string prompts: self.logger.info(f"🔍 Knowledge query '{query.semantic_query}' with filter '{where_sql}' → {len(knowl...
   📍 /Volumes/code/discernus/discernus/agents/comprehensive_knowledge_curator/agent.py:316
⚠️ **INLINE_PROMPTS**: F-string prompts: self.logger.error(f"Knowledge query failed: {str(e)}")...
   📍 /Volumes/code/discernus/discernus/agents/comprehensive_knowledge_curator/agent.py:320
🔸 **EXCESSIVE_PARSING**: JSON parsing: evidence_json = json.loads(evidence_data.decode('utf-8'))
   📍 /Volumes/code/discernus/discernus/agents/comprehensive_knowledge_curator/agent.py:327
⚠️ **INLINE_PROMPTS**: F-string prompts: searchable_text = f"Evidence from {doc_name} for {dimension}: {quote_text}"...
   📍 /Volumes/code/discernus/discernus/agents/comprehensive_knowledge_curator/agent.py:337
⚠️ **INLINE_PROMPTS**: F-string prompts: self.logger.error(f"Failed to process evidence data: {e}")...
   📍 /Volumes/code/discernus/discernus/agents/comprehensive_knowledge_curator/agent.py:358
🔸 **EXCESSIVE_PARSING**: JSON parsing: scores_json = json.loads(scores_data.decode('utf-8'))
   📍 /Volumes/code/discernus/discernus/agents/comprehensive_knowledge_curator/agent.py:364
⚠️ **INLINE_PROMPTS**: F-string prompts: searchable_text = f"Score for {dimension} in {document_name} by {speaker}: {value}"...
   📍 /Volumes/code/discernus/discernus/agents/comprehensive_knowledge_curator/agent.py:381
⚠️ **INLINE_PROMPTS**: F-string prompts: 'confidence': record.get(f'{dimension}_confidence', 1.0),...
   📍 /Volumes/code/discernus/discernus/agents/comprehensive_knowledge_curator/agent.py:393
⚠️ **INLINE_PROMPTS**: F-string prompts: 'salience': record.get(f'{dimension}_salience', 1.0)...
   📍 /Volumes/code/discernus/discernus/agents/comprehensive_knowledge_curator/agent.py:394
⚠️ **INLINE_PROMPTS**: F-string prompts: self.logger.error(f"Failed to process scores data: {e}")...
   📍 /Volumes/code/discernus/discernus/agents/comprehensive_knowledge_curator/agent.py:402
🔸 **EXCESSIVE_PARSING**: JSON parsing: metrics_json = json.loads(metrics_data.decode('utf-8'))
   📍 /Volumes/code/discernus/discernus/agents/comprehensive_knowledge_curator/agent.py:408
⚠️ **INLINE_PROMPTS**: F-string prompts: description = metric_data.get('description', f'Calculated metric: {metric_name}')...
   📍 /Volumes/code/discernus/discernus/agents/comprehensive_knowledge_curator/agent.py:417
⚠️ **INLINE_PROMPTS**: F-string prompts: searchable_text = f"Calculated metric {metric_name}: {description} = {value}"...
   📍 /Volumes/code/discernus/discernus/agents/comprehensive_knowledge_curator/agent.py:419
⚠️ **INLINE_PROMPTS**: F-string prompts: self.logger.error(f"Failed to process calculated metrics data: {e}")...
   📍 /Volumes/code/discernus/discernus/agents/comprehensive_knowledge_curator/agent.py:438

### csv_export_agent
**Violations**: 17

⚠️ **MISSING_YAML**: No YAML prompt files found
   📍 /Volumes/code/discernus/discernus/agents/csv_export_agent
🔸 **EXCESSIVE_PARSING**: Regex parsing: framework's output structure.
   📍 /Volumes/code/discernus/discernus/agents/csv_export_agent/agent.py:8
🔸 **EXCESSIVE_PARSING**: Regex parsing: from discernus.core.audit_logger import AuditLogger
   📍 /Volumes/code/discernus/discernus/agents/csv_export_agent/agent.py:33
🔸 **EXCESSIVE_PARSING**: JSON parsing: return json.loads(artifact_content.decode('utf-8'))
   📍 /Volumes/code/discernus/discernus/agents/csv_export_agent/agent.py:222
⚠️ **INLINE_PROMPTS**: F-string prompts: raise FileNotFoundError(f"Artifact not found: {artifact_hash}")...
   📍 /Volumes/code/discernus/discernus/agents/csv_export_agent/agent.py:228
🔸 **EXCESSIVE_PARSING**: JSON parsing: return json.loads(artifact_content.decode('utf-8'))
   📍 /Volumes/code/discernus/discernus/agents/csv_export_agent/agent.py:233
⚠️ **INLINE_PROMPTS**: F-string prompts: raise CSVExportError(f"Failed to load artifact {artifact_hash}: {str(e)}")...
   📍 /Volumes/code/discernus/discernus/agents/csv_export_agent/agent.py:235
⚠️ **INLINE_PROMPTS**: F-string prompts: self.logger.info(f"Generated {filename} with {len(document_analyses)} records")...
   📍 /Volumes/code/discernus/discernus/agents/csv_export_agent/agent.py:290
⚠️ **INLINE_PROMPTS**: F-string prompts: reasoning = f"Confidence: {confidence}, Context: {context_type}"...
   📍 /Volumes/code/discernus/discernus/agents/csv_export_agent/agent.py:323
⚠️ **INLINE_PROMPTS**: F-string prompts: reasoning = f"Analysis reasoning for {dimension} score: {score}"...
   📍 /Volumes/code/discernus/discernus/agents/csv_export_agent/agent.py:346
⚠️ **INLINE_PROMPTS**: F-string prompts: hash_content = f"{document_id}:{json.dumps(analysis_scores, sort_keys=True)}"...
   📍 /Volumes/code/discernus/discernus/agents/csv_export_agent/agent.py:429
⚠️ **INLINE_PROMPTS**: F-string prompts: self.logger.warning(f"Could not load statistical results: {e}")...
   📍 /Volumes/code/discernus/discernus/agents/csv_export_agent/agent.py:521
⚠️ **INLINE_PROMPTS**: F-string prompts: self.logger.warning(f"Could not load curated evidence: {e}")...
   📍 /Volumes/code/discernus/discernus/agents/csv_export_agent/agent.py:527
⚠️ **INLINE_PROMPTS**: F-string prompts: self.logger.error(f"Final synthesis CSV export failed: {str(e)}")...
   📍 /Volumes/code/discernus/discernus/agents/csv_export_agent/agent.py:585
⚠️ **INLINE_PROMPTS**: F-string prompts: f"Structure: {list(results.keys()) if isinstance(results, dict) else type(results)}")...
   📍 /Volumes/code/discernus/discernus/agents/csv_export_agent/agent.py:640
⚠️ **INLINE_PROMPTS**: F-string prompts: f"{test_name}_{var1}_{var2}", test_type, 'correlation_coefficient',...
   📍 /Volumes/code/discernus/discernus/agents/csv_export_agent/agent.py:705
⚠️ **INLINE_PROMPTS**: F-string prompts: self.logger.info(f"Generated statistical_results.csv with {len(results)} test results")...
   📍 /Volumes/code/discernus/discernus/agents/csv_export_agent/agent.py:732

### evidence_indexer_agent
**Violations**: 7

⚠️ **MISSING_YAML**: No YAML prompt files found
   📍 /Volumes/code/discernus/discernus/agents/evidence_indexer_agent
🔸 **EXCESSIVE_PARSING**: JSON parsing: evidence_json = json.loads(request.evidence_data.decode('utf-8'))
   📍 /Volumes/code/discernus/discernus/agents/evidence_indexer_agent/agent.py:38
⚠️ **INLINE_PROMPTS**: F-string prompts: "id": f"evd_{hashlib.sha1(str(evidence_item).encode()).hexdigest()[:10]}",...
   📍 /Volumes/code/discernus/discernus/agents/evidence_indexer_agent/agent.py:50
⚠️ **INLINE_PROMPTS**: F-string prompts: "original_quote_hash": f"sha256:{hashlib.sha256(evidence_item.get('quote_text', '').encode()).hexdig...
   📍 /Volumes/code/discernus/discernus/agents/evidence_indexer_agent/agent.py:55
⚠️ **INLINE_PROMPTS**: F-string prompts: quotes_section += f"\nQuote {i+1}: \"{quote_text}\"\n"...
   📍 /Volumes/code/discernus/discernus/agents/evidence_indexer_agent/agent.py:86
🔸 **EXCESSIVE_PARSING**: JSON parsing: response_array = json.loads(response_content)
   📍 /Volumes/code/discernus/discernus/agents/evidence_indexer_agent/agent.py:108
⚠️ **INLINE_PROMPTS**: F-string prompts: self.logger.warning(f"Batch processing failed: {e}. Using fallback.")...
   📍 /Volumes/code/discernus/discernus/agents/evidence_indexer_agent/agent.py:128

### evidence_quality_measurement
**Violations**: 28

⚠️ **MISSING_YAML**: No YAML prompt files found
   📍 /Volumes/code/discernus/discernus/agents/evidence_quality_measurement
⚠️ **INLINE_PROMPTS**: F-string prompts: self.logger.error(f"Evidence quality measurement failed: {str(e)}")...
   📍 /Volumes/code/discernus/discernus/agents/evidence_quality_measurement/agent.py:209
🔸 **EXCESSIVE_PARSING**: String splitting: queries = [q.strip() for q in response.split('\n') if q.strip()]
   📍 /Volumes/code/discernus/discernus/agents/evidence_quality_measurement/agent.py:239
🔸 **EXCESSIVE_PARSING**: Response parsing: queries = [q.strip() for q in response.split('\n') if q.strip()]
   📍 /Volumes/code/discernus/discernus/agents/evidence_quality_measurement/agent.py:239
⚠️ **INLINE_PROMPTS**: F-string prompts: self.logger.debug(f"LLM query generation failed: {e}")...
   📍 /Volumes/code/discernus/discernus/agents/evidence_quality_measurement/agent.py:242
⚠️ **INLINE_PROMPTS**: F-string prompts: self.logger.debug(f"Query failed for '{query}': {e}")...
   📍 /Volumes/code/discernus/discernus/agents/evidence_quality_measurement/agent.py:288
⚠️ **INLINE_PROMPTS**: F-string prompts: self.logger.debug(f"Failed to get total evidence count: {e}")...
   📍 /Volumes/code/discernus/discernus/agents/evidence_quality_measurement/agent.py:304
🔸 **EXCESSIVE_PARSING**: Regex parsing: matches = re.findall(ref_pattern, synthesis_report)
   📍 /Volumes/code/discernus/discernus/agents/evidence_quality_measurement/agent.py:322
⚠️ **INLINE_PROMPTS**: F-string prompts: self.logger.debug(f"Claim query failed for '{result_key}': {e}")...
   📍 /Volumes/code/discernus/discernus/agents/evidence_quality_measurement/agent.py:370
⚠️ **INLINE_PROMPTS**: F-string prompts: self.logger.debug(f"Synthesis claim query failed for '{claim}': {e}")...
   📍 /Volumes/code/discernus/discernus/agents/evidence_quality_measurement/agent.py:394
🔸 **EXCESSIVE_PARSING**: String splitting: query_terms.extend(result_key.split('_'))
   📍 /Volumes/code/discernus/discernus/agents/evidence_quality_measurement/agent.py:414
🔸 **EXCESSIVE_PARSING**: String splitting: query_terms.extend(value.split()[:5])  # First 5 words
   📍 /Volumes/code/discernus/discernus/agents/evidence_quality_measurement/agent.py:420
🔸 **EXCESSIVE_PARSING**: String splitting: claims = [c.strip() for c in response.split('\n') if c.strip()]
   📍 /Volumes/code/discernus/discernus/agents/evidence_quality_measurement/agent.py:448
🔸 **EXCESSIVE_PARSING**: Response parsing: claims = [c.strip() for c in response.split('\n') if c.strip()]
   📍 /Volumes/code/discernus/discernus/agents/evidence_quality_measurement/agent.py:448
⚠️ **INLINE_PROMPTS**: F-string prompts: self.logger.debug(f"LLM claim extraction failed: {e}")...
   📍 /Volumes/code/discernus/discernus/agents/evidence_quality_measurement/agent.py:451
🔸 **EXCESSIVE_PARSING**: Regex parsing: match = re.search(r'0\.\d+|1\.0', response)
   📍 /Volumes/code/discernus/discernus/agents/evidence_quality_measurement/agent.py:482
⚠️ **INLINE_PROMPTS**: F-string prompts: self.logger.debug(f"LLM alignment assessment failed: {e}")...
   📍 /Volumes/code/discernus/discernus/agents/evidence_quality_measurement/agent.py:487
⚠️ **INLINE_PROMPTS**: F-string prompts: self.logger.debug(f"Alignment query failed for '{query}': {e}")...
   📍 /Volumes/code/discernus/discernus/agents/evidence_quality_measurement/agent.py:542
⚠️ **INLINE_PROMPTS**: F-string prompts: self.logger.debug(f"Relevance query failed for '{query}': {e}")...
   📍 /Volumes/code/discernus/discernus/agents/evidence_quality_measurement/agent.py:611
⚠️ **INLINE_PROMPTS**: F-string prompts: self.logger.debug(f"Quality query failed for '{query}': {e}")...
   📍 /Volumes/code/discernus/discernus/agents/evidence_quality_measurement/agent.py:674
🔸 **EXCESSIVE_PARSING**: String splitting: if evidence_quote and any(word in claim_text for word in evidence_quote.split()[:5]):
   📍 /Volumes/code/discernus/discernus/agents/evidence_quality_measurement/agent.py:711
⚠️ **INLINE_PROMPTS**: F-string prompts: self.logger.debug(f"Evidence is not a list: {type(evidence)}")...
   📍 /Volumes/code/discernus/discernus/agents/evidence_quality_measurement/agent.py:731
⚠️ **INLINE_PROMPTS**: F-string prompts: self.logger.debug(f"Invalid evidence object {i}: {type(ev)}")...
   📍 /Volumes/code/discernus/discernus/agents/evidence_quality_measurement/agent.py:744
🔸 **EXCESSIVE_PARSING**: Regex parsing: citations = re.findall(citation_pattern, synthesis_report)
   📍 /Volumes/code/discernus/discernus/agents/evidence_quality_measurement/agent.py:1012
🔸 **EXCESSIVE_PARSING**: Regex parsing: has_evidence_section = bool(re.search(evidence_section_pattern, synthesis_report))
   📍 /Volumes/code/discernus/discernus/agents/evidence_quality_measurement/agent.py:1014
🔸 **EXCESSIVE_PARSING**: Regex parsing: inline_citations = re.findall(r'\[(\d+)\]', synthesis_report)
   📍 /Volumes/code/discernus/discernus/agents/evidence_quality_measurement/agent.py:1062
🔸 **EXCESSIVE_PARSING**: Regex parsing: evidence_section_match = re.search(r'## Evidence References\s*\n(.*?)(?=\n##|\Z)', synthesis_report, re.DOTALL)
   📍 /Volumes/code/discernus/discernus/agents/evidence_quality_measurement/agent.py:1066
🔸 **EXCESSIVE_PARSING**: Regex parsing: references = re.findall(r'\[(\d+)\]', evidence_section)
   📍 /Volumes/code/discernus/discernus/agents/evidence_quality_measurement/agent.py:1074

### experiment_coherence_agent
**Violations**: 19

🔸 **EXCESSIVE_PARSING**: Regex parsing: from discernus.core.audit_logger import AuditLogger
   📍 /Volumes/code/discernus/discernus/agents/experiment_coherence_agent/agent.py:21
⚠️ **INLINE_PROMPTS**: F-string prompts: raise FileNotFoundError(f"Prompt file not found: {prompt_path}")...
   📍 /Volumes/code/discernus/discernus/agents/experiment_coherence_agent/agent.py:96
⚠️ **INLINE_PROMPTS**: F-string prompts: raise ValueError(f"Prompt file missing 'template' key: {prompt_path}")...
   📍 /Volumes/code/discernus/discernus/agents/experiment_coherence_agent/agent.py:104
⚠️ **INLINE_PROMPTS**: F-string prompts: description=f"Failed to load experiment artifacts: {str(e)}",...
   📍 /Volumes/code/discernus/discernus/agents/experiment_coherence_agent/agent.py:232
⚠️ **INLINE_PROMPTS**: F-string prompts: raise FileNotFoundError(f"experiment.md not found in {experiment_path}")...
   📍 /Volumes/code/discernus/discernus/agents/experiment_coherence_agent/agent.py:243
🔸 **EXCESSIVE_PARSING**: String splitting: parts = content.split('---', 2)
   📍 /Volumes/code/discernus/discernus/agents/experiment_coherence_agent/agent.py:250
🔸 **EXCESSIVE_PARSING**: Content parsing: parts = content.split('---', 2)
   📍 /Volumes/code/discernus/discernus/agents/experiment_coherence_agent/agent.py:250
⚠️ **INLINE_PROMPTS**: F-string prompts: raise FileNotFoundError(f"Framework file not found: {framework_file}")...
   📍 /Volumes/code/discernus/discernus/agents/experiment_coherence_agent/agent.py:262
⚠️ **INLINE_PROMPTS**: F-string prompts: raise FileNotFoundError(f"corpus.md not found in {corpus_path}")...
   📍 /Volumes/code/discernus/discernus/agents/experiment_coherence_agent/agent.py:273
🔸 **EXCESSIVE_PARSING**: JSON parsing: return json.loads(json_content)
   📍 /Volumes/code/discernus/discernus/agents/experiment_coherence_agent/agent.py:284
⚠️ **INLINE_PROMPTS**: F-string prompts: description=f"Insufficient corpus size: {corpus_size} documents",...
   📍 /Volumes/code/discernus/discernus/agents/experiment_coherence_agent/agent.py:311
⚠️ **INLINE_PROMPTS**: F-string prompts: fix=f"Add {3 - corpus_size} more documents to corpus directory",...
   📍 /Volumes/code/discernus/discernus/agents/experiment_coherence_agent/agent.py:313
⚠️ **INLINE_PROMPTS**: F-string prompts: description=f"Minimal corpus size: {corpus_size} documents",...
   📍 /Volumes/code/discernus/discernus/agents/experiment_coherence_agent/agent.py:320
⚠️ **INLINE_PROMPTS**: F-string prompts: description=f"Complex framework ({dimension_count} dimension indicators) with small corpus ({corpus_...
   📍 /Volumes/code/discernus/discernus/agents/experiment_coherence_agent/agent.py:342
⚠️ **INLINE_PROMPTS**: F-string prompts: description=f"Could not analyze framework complexity: {str(e)}",...
   📍 /Volumes/code/discernus/discernus/agents/experiment_coherence_agent/agent.py:351
🔸 **EXCESSIVE_PARSING**: JSON parsing: data = json.loads(json_content)
   📍 /Volumes/code/discernus/discernus/agents/experiment_coherence_agent/agent.py:380
🔸 **EXCESSIVE_PARSING**: JSON parsing: data = json.loads(response)
   📍 /Volumes/code/discernus/discernus/agents/experiment_coherence_agent/agent.py:382
🔸 **EXCESSIVE_PARSING**: JSON parsing: data = json.loads(response)
   📍 /Volumes/code/discernus/discernus/agents/experiment_coherence_agent/agent.py:384
⚠️ **INLINE_PROMPTS**: F-string prompts: description=f"Failed to parse validation response: {str(e)}",...
   📍 /Volumes/code/discernus/discernus/agents/experiment_coherence_agent/agent.py:410

### intelligent_extractor_agent
**Violations**: 18

🔸 **EXCESSIVE_PARSING**: Regex parsing: from discernus.core.audit_logger import AuditLogger
   📍 /Volumes/code/discernus/discernus/agents/intelligent_extractor_agent/agent.py:32
⚠️ **INLINE_PROMPTS**: F-string prompts: error_message=f"Unsupported gasket_schema version: {gasket_schema.get('version')}. Supported version...
   📍 /Volumes/code/discernus/discernus/agents/intelligent_extractor_agent/agent.py:160
⚠️ **INLINE_PROMPTS**: F-string prompts: self.logger.warning(f"Extraction attempt {attempt} failed: {str(e)}")...
   📍 /Volumes/code/discernus/discernus/agents/intelligent_extractor_agent/agent.py:236
🔸 **EXCESSIVE_PARSING**: Regex parsing: Load external YAML prompt template following THIN architecture.
   📍 /Volumes/code/discernus/discernus/agents/intelligent_extractor_agent/agent.py:269
⚠️ **INLINE_PROMPTS**: F-string prompts: raise FileNotFoundError(f"Prompt file not found: {prompt_path}")...
   📍 /Volumes/code/discernus/discernus/agents/intelligent_extractor_agent/agent.py:279
⚠️ **INLINE_PROMPTS**: F-string prompts: raise ValueError(f"Prompt file missing 'template' key: {prompt_path}")...
   📍 /Volumes/code/discernus/discernus/agents/intelligent_extractor_agent/agent.py:287
⚠️ **INLINE_PROMPTS**: F-string prompts: keys_text = "\n".join(f"- {key}" for key in target_keys)...
   📍 /Volumes/code/discernus/discernus/agents/intelligent_extractor_agent/agent.py:310
⚠️ **INLINE_PROMPTS**: F-string prompts: pattern_hints.append(f"- {key}: Look for patterns like '{patterns[0]}'")...
   📍 /Volumes/code/discernus/discernus/agents/intelligent_extractor_agent/agent.py:317
⚠️ **INLINE_PROMPTS**: F-string prompts: example_json_content = ",\n      ".join(f'"{k}": {v}' for k, v in example_mapping.items())...
   📍 /Volumes/code/discernus/discernus/agents/intelligent_extractor_agent/agent.py:324
🔸 **EXCESSIVE_PARSING**: JSON parsing: parsed_data = json.loads(cleaned_response)
   📍 /Volumes/code/discernus/discernus/agents/intelligent_extractor_agent/agent.py:360
⚠️ **INLINE_PROMPTS**: F-string prompts: self.logger.warning(f"Invalid score for {key} in {document_name}: {value} (must be {min_score}-{max_...
   📍 /Volumes/code/discernus/discernus/agents/intelligent_extractor_agent/agent.py:393
⚠️ **INLINE_PROMPTS**: F-string prompts: self.logger.warning(f"Invalid score type for {key} in {document_name}: {value} (must be numeric)")...
   📍 /Volumes/code/discernus/discernus/agents/intelligent_extractor_agent/agent.py:395
⚠️ **INLINE_PROMPTS**: F-string prompts: self.logger.error(f"Failed to parse extraction response as JSON: {e}")...
   📍 /Volumes/code/discernus/discernus/agents/intelligent_extractor_agent/agent.py:405
⚠️ **INLINE_PROMPTS**: F-string prompts: self.logger.error(f"Response was: {response[:200]}...")...
   📍 /Volumes/code/discernus/discernus/agents/intelligent_extractor_agent/agent.py:406
⚠️ **INLINE_PROMPTS**: F-string prompts: raise IntelligentExtractorError(f"Invalid JSON response from LLM: {e}")...
   📍 /Volumes/code/discernus/discernus/agents/intelligent_extractor_agent/agent.py:407
⚠️ **INLINE_PROMPTS**: F-string prompts: self.logger.error(f"Unexpected error parsing extraction response: {e}")...
   📍 /Volumes/code/discernus/discernus/agents/intelligent_extractor_agent/agent.py:410
⚠️ **INLINE_PROMPTS**: F-string prompts: raise IntelligentExtractorError(f"Failed to parse extraction response: {e}")...
   📍 /Volumes/code/discernus/discernus/agents/intelligent_extractor_agent/agent.py:411
🔸 **COMPLEX_PARSING_METHODS**: Contains parse_* or extract_* methods
   📍 /Volumes/code/discernus/discernus/agents/intelligent_extractor_agent/agent.py

### reliability_analysis_agent
**Violations**: 15

🔸 **EXCESSIVE_PARSING**: Regex parsing: from discernus.core.audit_logger import AuditLogger
   📍 /Volumes/code/discernus/discernus/agents/reliability_analysis_agent/agent.py:21
⚠️ **INLINE_PROMPTS**: F-string prompts: print(f"Warning: Failed to load prompts for {self.agent_name}: {e}")...
   📍 /Volumes/code/discernus/discernus/agents/reliability_analysis_agent/agent.py:101
⚠️ **INLINE_PROMPTS**: F-string prompts: error_msg = f"Framework dimension validation failed: {str(e)}"...
   📍 /Volumes/code/discernus/discernus/agents/reliability_analysis_agent/agent.py:179
⚠️ **INLINE_PROMPTS**: F-string prompts: error_msg = f"Statistical health validation failed: {str(e)}"...
   📍 /Volumes/code/discernus/discernus/agents/reliability_analysis_agent/agent.py:266
⚠️ **INLINE_PROMPTS**: F-string prompts: error_msg = f"Pipeline health assessment failed: {str(e)}"...
   📍 /Volumes/code/discernus/discernus/agents/reliability_analysis_agent/agent.py:359
🔸 **EXCESSIVE_PARSING**: Regex parsing: json_match = re.search(r'\{.*\}', response, re.DOTALL)
   📍 /Volumes/code/discernus/discernus/agents/reliability_analysis_agent/agent.py:381
🔸 **EXCESSIVE_PARSING**: JSON parsing: result_data = json.loads(json_match.group(0))
   📍 /Volumes/code/discernus/discernus/agents/reliability_analysis_agent/agent.py:383
🔸 **EXCESSIVE_PARSING**: JSON parsing: result_data = json.loads(response)
   📍 /Volumes/code/discernus/discernus/agents/reliability_analysis_agent/agent.py:385
⚠️ **INLINE_PROMPTS**: F-string prompts: impact_assessment=f"Failed to parse validation response: {str(e)}",...
   📍 /Volumes/code/discernus/discernus/agents/reliability_analysis_agent/agent.py:403
🔸 **EXCESSIVE_PARSING**: Regex parsing: json_match = re.search(r'\{.*\}', response, re.DOTALL)
   📍 /Volumes/code/discernus/discernus/agents/reliability_analysis_agent/agent.py:413
🔸 **EXCESSIVE_PARSING**: JSON parsing: result_data = json.loads(json_match.group(0))
   📍 /Volumes/code/discernus/discernus/agents/reliability_analysis_agent/agent.py:415
🔸 **EXCESSIVE_PARSING**: JSON parsing: result_data = json.loads(response)
   📍 /Volumes/code/discernus/discernus/agents/reliability_analysis_agent/agent.py:417
🔸 **EXCESSIVE_PARSING**: Regex parsing: json_match = re.search(r'\{.*\}', response, re.DOTALL)
   📍 /Volumes/code/discernus/discernus/agents/reliability_analysis_agent/agent.py:445
🔸 **EXCESSIVE_PARSING**: JSON parsing: result_data = json.loads(json_match.group(0))
   📍 /Volumes/code/discernus/discernus/agents/reliability_analysis_agent/agent.py:447
🔸 **EXCESSIVE_PARSING**: JSON parsing: result_data = json.loads(response)
   📍 /Volumes/code/discernus/discernus/agents/reliability_analysis_agent/agent.py:449

### score_grounding
**Violations**: 18

🔸 **EXCESSIVE_PARSING**: Regex parsing: Provides automatic grounding evidence generation for every numerical score.
   📍 /Volumes/code/discernus/discernus/agents/score_grounding/__init__.py:5
🔸 **EXCESSIVE_PARSING**: Regex parsing: from discernus.core.audit_logger import AuditLogger
   📍 /Volumes/code/discernus/discernus/agents/score_grounding/grounding_evidence_generator.py:29
🔸 **EXCESSIVE_PARSING**: Regex parsing: from discernus.core.evidence_confidence_calibrator import EvidenceConfidenceCalibrator, ConfidenceCalibrationRequest
   📍 /Volumes/code/discernus/discernus/agents/score_grounding/grounding_evidence_generator.py:30
⚠️ **INLINE_PROMPTS**: F-string prompts: raise ValueError(f"Prompt file missing 'template' key: {prompt_path}")...
   📍 /Volumes/code/discernus/discernus/agents/score_grounding/grounding_evidence_generator.py:127
⚠️ **INLINE_PROMPTS**: F-string prompts: self.logger.error(f"LLM returned empty response for grounding evidence. Reason: {reason}")...
   📍 /Volumes/code/discernus/discernus/agents/score_grounding/grounding_evidence_generator.py:203
⚠️ **INLINE_PROMPTS**: F-string prompts: raise ValueError(f"LLM returned empty response. Reason: {reason}")...
   📍 /Volumes/code/discernus/discernus/agents/score_grounding/grounding_evidence_generator.py:204
🔸 **EXCESSIVE_PARSING**: JSON parsing: grounding_data = json.loads(json_content)
   📍 /Volumes/code/discernus/discernus/agents/score_grounding/grounding_evidence_generator.py:271
🔸 **EXCESSIVE_PARSING**: JSON parsing: grounding_data = json.loads(response_content)
   📍 /Volumes/code/discernus/discernus/agents/score_grounding/grounding_evidence_generator.py:273
🔸 **EXCESSIVE_PARSING**: JSON parsing: grounding_data = json.loads(response_content)
   📍 /Volumes/code/discernus/discernus/agents/score_grounding/grounding_evidence_generator.py:275
⚠️ **INLINE_PROMPTS**: F-string prompts: logging.error(f"Failed to parse grounding response: {str(e)}")...
   📍 /Volumes/code/discernus/discernus/agents/score_grounding/grounding_evidence_generator.py:303
⚠️ **INLINE_PROMPTS**: F-string prompts: content = f"{document_name}:{dimension}:{evidence_text}"...
   📍 /Volumes/code/discernus/discernus/agents/score_grounding/grounding_evidence_generator.py:309
⚠️ **INLINE_PROMPTS**: F-string prompts: self.logger.warning(f"Missing calibration for evidence {i}, using original confidence")...
   📍 /Volumes/code/discernus/discernus/agents/score_grounding/grounding_evidence_generator.py:333
⚠️ **INLINE_PROMPTS**: F-string prompts: self.logger.warning(f"Batch calibration failed: {reason}. Using fallback individual calibration.")...
   📍 /Volumes/code/discernus/discernus/agents/score_grounding/grounding_evidence_generator.py:392
🔸 **EXCESSIVE_PARSING**: JSON parsing: calibrations = json.loads(response_content)
   📍 /Volumes/code/discernus/discernus/agents/score_grounding/grounding_evidence_generator.py:397
⚠️ **INLINE_PROMPTS**: F-string prompts: self.logger.warning(f"Batch calibration returned {len(calibrations) if isinstance(calibrations, list...
   📍 /Volumes/code/discernus/discernus/agents/score_grounding/grounding_evidence_generator.py:399
⚠️ **INLINE_PROMPTS**: F-string prompts: self.logger.info(f"Batch calibration successful: processed {len(calibrations)} evidence pieces in 1 ...
   📍 /Volumes/code/discernus/discernus/agents/score_grounding/grounding_evidence_generator.py:402
⚠️ **INLINE_PROMPTS**: F-string prompts: self.logger.warning(f"Batch calibration JSON parsing failed: {str(e)}. Using fallback.")...
   📍 /Volumes/code/discernus/discernus/agents/score_grounding/grounding_evidence_generator.py:406
⚠️ **INLINE_PROMPTS**: F-string prompts: self.logger.error(f"Batch calibration failed: {str(e)}. Using fallback individual calibration.")...
   📍 /Volumes/code/discernus/discernus/agents/score_grounding/grounding_evidence_generator.py:410

### sequential_synthesis
**Violations**: 7

⚠️ **MISSING_YAML**: No YAML prompt files found
   📍 /Volumes/code/discernus/discernus/agents/sequential_synthesis
🔸 **EXCESSIVE_PARSING**: Regex parsing: Implements the THIN, framework-agnostic, sequential synthesis architecture.
   📍 /Volumes/code/discernus/discernus/agents/sequential_synthesis/agent.py:5
⚠️ **INLINE_PROMPTS**: F-string prompts: self.logger.error(f"Sequential synthesis pipeline failed: {e}", exc_info=True)...
   📍 /Volumes/code/discernus/discernus/agents/sequential_synthesis/agent.py:96
🔸 **EXCESSIVE_PARSING**: String splitting: llm_response = llm_response.split("```json")[1].split("```")[0]
   📍 /Volumes/code/discernus/discernus/agents/sequential_synthesis/agent.py:155
🔸 **EXCESSIVE_PARSING**: Response parsing: llm_response = llm_response.split("```json")[1].split("```")[0]
   📍 /Volumes/code/discernus/discernus/agents/sequential_synthesis/agent.py:155
🔸 **EXCESSIVE_PARSING**: JSON parsing: return json.loads(llm_response)
   📍 /Volumes/code/discernus/discernus/agents/sequential_synthesis/agent.py:156
⚠️ **INLINE_PROMPTS**: F-string prompts: self.logger.warning(f"Failed to parse JSON list from LLM response: {llm_response}")...
   📍 /Volumes/code/discernus/discernus/agents/sequential_synthesis/agent.py:158

### txtai_evidence_curator
**Violations**: 31

⚠️ **MISSING_YAML**: No YAML prompt files found
   📍 /Volumes/code/discernus/discernus/agents/txtai_evidence_curator
⚠️ **INLINE_PROMPTS**: F-string prompts: self.logger.warning(f"Skipping task '{task_name}' - no provenance information")...
   📍 /Volumes/code/discernus/discernus/agents/txtai_evidence_curator/agent.py:142
⚠️ **INLINE_PROMPTS**: F-string prompts: self.logger.debug(f"Skipping task '{task_name}' - mathematical operation, needs transparency not evi...
   📍 /Volumes/code/discernus/discernus/agents/txtai_evidence_curator/agent.py:149
⚠️ **INLINE_PROMPTS**: F-string prompts: self.logger.info(f"Evidence linking applied to {len(valid_tasks)}/{len(all_results)} tasks (Epic 280...
   📍 /Volumes/code/discernus/discernus/agents/txtai_evidence_curator/agent.py:151
⚠️ **INLINE_PROMPTS**: F-string prompts: self.logger.error(f"txtai evidence curation failed: {str(e)}")...
   📍 /Volumes/code/discernus/discernus/agents/txtai_evidence_curator/agent.py:167
⚠️ **INLINE_PROMPTS**: F-string prompts: self.logger.debug(f"Task '{task_name}' (type: {task_type}) defaulting to evidence linking")...
   📍 /Volumes/code/discernus/discernus/agents/txtai_evidence_curator/agent.py:229
🔸 **EXCESSIVE_PARSING**: JSON parsing: evidence_json = json.loads(evidence_data.decode('utf-8'))
   📍 /Volumes/code/discernus/discernus/agents/txtai_evidence_curator/agent.py:244
⚠️ **INLINE_PROMPTS**: F-string prompts: search_text = f"{evidence.get('document_name', '')} {evidence.get('dimension', '')} evidence: {evide...
   📍 /Volumes/code/discernus/discernus/agents/txtai_evidence_curator/agent.py:258
⚠️ **INLINE_PROMPTS**: F-string prompts: self.logger.info(f"Built txtai index with {len(documents)} evidence pieces")...
   📍 /Volumes/code/discernus/discernus/agents/txtai_evidence_curator/agent.py:279
⚠️ **INLINE_PROMPTS**: F-string prompts: self.logger.info(f"Sample doc {i}: {doc.get('document_name', 'N/A')} - {doc.get('dimension', 'N/A')}...
   📍 /Volumes/code/discernus/discernus/agents/txtai_evidence_curator/agent.py:284
⚠️ **INLINE_PROMPTS**: F-string prompts: self.logger.error(f"Failed to build evidence index: {str(e)}")...
   📍 /Volumes/code/discernus/discernus/agents/txtai_evidence_curator/agent.py:289
⚠️ **INLINE_PROMPTS**: F-string prompts: self.logger.debug(f"No dimensional scores found for task '{task_name}'")...
   📍 /Volumes/code/discernus/discernus/agents/txtai_evidence_curator/agent.py:324
⚠️ **INLINE_PROMPTS**: F-string prompts: self.logger.info(f"Batch evidence synthesis successful: processed {len(valid_tasks)} tasks in 1 LLM ...
   📍 /Volumes/code/discernus/discernus/agents/txtai_evidence_curator/agent.py:355
⚠️ **INLINE_PROMPTS**: F-string prompts: self.logger.warning(f"Batch synthesis failed: {reason}. Using fallback individual processing.")...
   📍 /Volumes/code/discernus/discernus/agents/txtai_evidence_curator/agent.py:359
⚠️ **INLINE_PROMPTS**: F-string prompts: self.logger.error(f"Batch evidence synthesis failed: {str(e)}. Using fallback individual processing....
   📍 /Volumes/code/discernus/discernus/agents/txtai_evidence_curator/agent.py:363
⚠️ **INLINE_PROMPTS**: F-string prompts: f"  - Document: {ev.document_name}, Dimension: {ev.dimension}, Quote: \"{ev.quote_text}\", Confidenc...
   📍 /Volumes/code/discernus/discernus/agents/txtai_evidence_curator/agent.py:379
⚠️ **INLINE_PROMPTS**: F-string prompts: finding_summary = f"Type: {finding_type}, Results: {json.dumps(task_result.get('results', {}), inden...
   📍 /Volumes/code/discernus/discernus/agents/txtai_evidence_curator/agent.py:385
⚠️ **INLINE_PROMPTS**: F-string prompts: self.logger.debug(f"No dimensional scores found for task '{task_name}'")...
   📍 /Volumes/code/discernus/discernus/agents/txtai_evidence_curator/agent.py:456
⚠️ **INLINE_PROMPTS**: F-string prompts: self.logger.warning(f"No evidence found for task '{task_name}' - checked {len(input_document_ids)} d...
   📍 /Volumes/code/discernus/discernus/agents/txtai_evidence_curator/agent.py:472
⚠️ **INLINE_PROMPTS**: F-string prompts: self.logger.warning(f"Documents: {input_document_ids}")...
   📍 /Volumes/code/discernus/discernus/agents/txtai_evidence_curator/agent.py:473
⚠️ **INLINE_PROMPTS**: F-string prompts: self.logger.warning(f"Dimensions: {relevant_dimensions}")...
   📍 /Volumes/code/discernus/discernus/agents/txtai_evidence_curator/agent.py:474
⚠️ **INLINE_PROMPTS**: F-string prompts: self.logger.error(f"Failed to generate narrative for task '{task_name}': {str(e)}")...
   📍 /Volumes/code/discernus/discernus/agents/txtai_evidence_curator/agent.py:483
⚠️ **INLINE_PROMPTS**: F-string prompts: self.logger.warning(f"Unknown txtai result format: {type(result)}")...
   📍 /Volumes/code/discernus/discernus/agents/txtai_evidence_curator/agent.py:534
⚠️ **INLINE_PROMPTS**: F-string prompts: self.logger.warning(f"Failed to retrieve document for result {result}: {e}")...
   📍 /Volumes/code/discernus/discernus/agents/txtai_evidence_curator/agent.py:538
⚠️ **INLINE_PROMPTS**: F-string prompts: self.logger.error(f"Evidence query failed: {str(e)}")...
   📍 /Volumes/code/discernus/discernus/agents/txtai_evidence_curator/agent.py:562
⚠️ **INLINE_PROMPTS**: F-string prompts: f"Document: {ev.document_name}\nDimension: {ev.dimension}\nQuote: \"{ev.quote_text}\"\nConfidence: {...
   📍 /Volumes/code/discernus/discernus/agents/txtai_evidence_curator/agent.py:585
⚠️ **INLINE_PROMPTS**: F-string prompts: finding_summary = f"Task: {task_name}\nType: {finding_type}\nResults: {json.dumps(task_result.get('r...
   📍 /Volumes/code/discernus/discernus/agents/txtai_evidence_curator/agent.py:591
⚠️ **INLINE_PROMPTS**: F-string prompts: self.logger.warning(f"Empty synthesis for task '{task_name}'. Reason: {reason}")...
   📍 /Volumes/code/discernus/discernus/agents/txtai_evidence_curator/agent.py:626
⚠️ **INLINE_PROMPTS**: F-string prompts: return f"// No synthesis generated for {task_name}. Reason: {reason}"...
   📍 /Volumes/code/discernus/discernus/agents/txtai_evidence_curator/agent.py:627
⚠️ **INLINE_PROMPTS**: F-string prompts: self.logger.error(f"Evidence synthesis failed for task '{task_name}': {str(e)}")...
   📍 /Volumes/code/discernus/discernus/agents/txtai_evidence_curator/agent.py:630
⚠️ **INLINE_PROMPTS**: F-string prompts: return f"// Error during synthesis for {task_name}: {str(e)}"...
   📍 /Volumes/code/discernus/discernus/agents/txtai_evidence_curator/agent.py:631

## Redundant Agent Analysis

### Evidence System
**Issue**: Multiple evidence agents
**Agents**: evidence_quality_measurement, txtai_evidence_curator, evidence_indexer_agent
