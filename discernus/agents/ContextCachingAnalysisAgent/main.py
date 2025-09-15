#!/usr/bin/env python3
"""
Context Caching Analysis Agent
==============================

Uses Vertex AI context caching for efficient sequential tool calls.
This agent makes 3 separate LLM calls with context caching to get
scores, evidence, and computational work for each document.

Key benefits:
- 75% cost reduction on cached content (framework + document)
- More reliable than complex multi-tool calls
- Can process multiple documents in one session
"""

import json
import hashlib
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional
from datetime import datetime, timezone, timedelta

from ...core.security_boundary import ExperimentSecurityBoundary
from ...core.audit_logger import AuditLogger
from ...core.local_artifact_storage import LocalArtifactStorage
from ...gateway.llm_gateway_enhanced import EnhancedLLMGateway
from ...gateway.model_registry import ModelRegistry

# Vertex AI context caching imports
try:
    import vertexai
    from vertexai.generative_models import GenerativeModel, Part
    from vertexai.preview import caching
    VERTEX_AI_AVAILABLE = True
except ImportError:
    VERTEX_AI_AVAILABLE = False


class ContextCachingAnalysisAgent:
    """Analysis agent using Vertex AI context caching for sequential tool calls"""
    
    def __init__(self, security: ExperimentSecurityBoundary, audit: AuditLogger, storage: LocalArtifactStorage):
        self.security = security
        self.audit = audit
        self.storage = storage
        self.gateway = EnhancedLLMGateway(ModelRegistry())
        self.cached_content = None  # Will store the cached content
        self.cache_name = None  # Will store the cache name
        
    def analyze_documents(self, framework: str, documents: List[Dict[str, Any]], 
                         config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze documents using context caching for efficient sequential tool calls.
        
        Args:
            framework: The analysis framework content
            documents: List of documents to analyze
            config: Analysis configuration
            
        Returns:
            Analysis results with scores, evidence, and computational work
        """
        agent_name = "ContextCachingAnalysisAgent"
        
        # Generate analysis ID for this batch
        analysis_id = self._generate_analysis_id(framework, documents, config)
        
        # Log analysis start
        self.audit.log_agent_event(agent_name, "analysis_started", {
            "analysis_id": analysis_id,
            "document_count": len(documents),
            "framework_size": len(framework)
        })
        
        try:
            # Process each document with context caching
            all_results = []
            
            for i, document in enumerate(documents):
                self.audit.log_agent_event(agent_name, "document_analysis_started", {
                    "document_index": i,
                    "document_filename": document.get('filename', 'unknown'),
                    "document_size": len(document.get('content', ''))
                })
                
                # Analyze single document with context caching
                doc_result = self._analyze_single_document(
                    framework, document, config, analysis_id, i
                )
                
                all_results.append(doc_result)
                
                self.audit.log_agent_event(agent_name, "document_analysis_completed", {
                    "document_index": i,
                    "scores_count": len(doc_result.get('dimensional_scores', {})),
                    "evidence_count": len(doc_result.get('evidence', [])),
                    "has_computational_work": bool(doc_result.get('computational_work'))
                })
            
            # Aggregate results
            result = self._aggregate_results(all_results, analysis_id)
            
            self.audit.log_agent_event(agent_name, "analysis_completed", {
                "analysis_id": analysis_id,
                "total_documents": len(documents),
                "successful_analyses": len(all_results)
            })
            
            return result
            
        except Exception as e:
            self.audit.log_agent_event(agent_name, "analysis_failed", {
                "analysis_id": analysis_id,
                "error": str(e)
            })
            raise
    
    def _analyze_single_document(self, framework: str, document: Dict[str, Any], 
                                config: Dict[str, Any], analysis_id: str, 
                                doc_index: int) -> Dict[str, Any]:
        """Analyze a single document using 3 sequential calls with context caching"""
        
        agent_name = "ContextCachingAnalysisAgent"
        document_content = document.get('content', '')
        document_id = document.get('filename', f'doc_{doc_index}')
        
        # Generate document hash for caching
        doc_hash = hashlib.sha256(document_content.encode()).hexdigest()[:16]
        
        try:
            # Call 1: Get dimensional scores
            scores_result = self._get_dimensional_scores(
                framework, document_content, document_id, analysis_id, doc_index
            )
            
            # Call 2: Get evidence quotes (with context caching)
            evidence_result = self._get_evidence_quotes(
                framework, document_content, document_id, analysis_id, doc_index
            )
            
            # Call 3: Get computational work (with context caching)
            work_result = self._get_computational_work(
                framework, document_content, document_id, analysis_id, doc_index
            )
            
            # Combine results
            result = {
                'document_id': document_id,
                'document_hash': doc_hash,
                'dimensional_scores': scores_result.get('scores', {}),
                'evidence': evidence_result.get('evidence', []),
                'computational_work': work_result.get('work', {}),
                'analysis_metadata': {
                    'analysis_id': analysis_id,
                    'document_index': doc_index,
                    'timestamp': datetime.now(timezone.utc).isoformat(),
                    'agent': agent_name
                }
            }
            
            return result
            
        except Exception as e:
            self.audit.log_agent_event(agent_name, "document_analysis_failed", {
                "document_id": document_id,
                "document_index": doc_index,
                "error": str(e)
            })
            raise
    
    def _get_dimensional_scores(self, framework: str, document_content: str, 
                               document_id: str, analysis_id: str, doc_index: int) -> Dict[str, Any]:
        """First call: Get dimensional scores (creates context cache)"""
        
        agent_name = "ContextCachingAnalysisAgent"
        
        # Create context cache if not already created
        if not self.cached_content:
            self._create_context_cache(framework, document_content, document_id)
        
        # Create prompt for dimensional scoring (without framework/doc content since it's cached)
        prompt = self._create_scores_prompt_cached(document_id)
        
        # Create tool definition for scores
        tools = [{
            "type": "function",
            "function": {
                "name": "record_analysis_scores",
                "description": "Record dimensional analysis scores for the document",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "document_id": {"type": "string"},
                        "dimensional_scores": {
                            "type": "object",
                            "description": "Scores for each dimension in the framework"
                        }
                    },
                    "required": ["document_id", "dimensional_scores"]
                }
            }
        }]
        
        # Make LLM call using cached content
        response, metadata = self._make_cached_call(
            prompt=prompt,
            system_prompt="You are an expert discourse analyst. Analyze the document and provide dimensional scores.",
            tools=tools,
            context="Dimensional scoring with context cache"
        )
        
        # Extract tool calls from response
        tool_calls = self._extract_tool_calls(response, metadata)
        
        # Verbose logging: Capture full LLM response and reasoning
        self.audit.log_agent_event(agent_name, "scores_verbose_response", {
            "full_response": response,
            "response_length": len(response),
            "tool_calls_count": len(tool_calls) if tool_calls else 0,
            "metadata_keys": list(metadata.keys()),
            "prompt_preview": prompt[:500] + "..." if len(prompt) > 500 else prompt
        })
        
        # Debug: Log what we got
        self.audit.log_agent_event(agent_name, "scores_debug", {
            "tool_calls_count": len(tool_calls),
            "response_length": len(response),
            "metadata_keys": list(metadata.keys()),
            "tool_calls": [str(tc) for tc in tool_calls[:2]]  # Log first 2 tool calls
        })
        
        # Process the scores
        scores_data = self._process_scores_tool_call(tool_calls, document_id)
        
        # Store the context cache ID for subsequent calls
        if 'cached_content_token_count' in metadata:
            self.cache_id = metadata.get('cached_content_token_count')
        
        self.audit.log_agent_event(agent_name, "scores_call_completed", {
            "document_id": document_id,
            "doc_index": doc_index,
            "scores_count": len(scores_data.get('scores', {})),
            "cache_created": self.cached_content is not None
        })
        
        return scores_data
    
    def _get_evidence_quotes(self, framework: str, document_content: str, 
                            document_id: str, analysis_id: str, doc_index: int) -> Dict[str, Any]:
        """Second call: Get evidence quotes (uses context cache)"""
        
        agent_name = "ContextCachingAnalysisAgent"
        
        # Create prompt for evidence extraction (cached content already has framework/doc)
        prompt = self._create_evidence_prompt_cached(document_id)
        
        # Create tool definition for evidence
        tools = [{
            "type": "function",
            "function": {
                "name": "record_evidence_quotes",
                "description": "Record specific textual evidence for each dimension",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "document_id": {"type": "string"},
                        "evidence_quotes": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "dimension": {"type": "string"},
                                    "quote": {"type": "string"},
                                    "context": {"type": "string"},
                                    "relevance_score": {"type": "number"}
                                    }
                                }
                            }
                        },
                    "required": ["document_id", "evidence_quotes"]
                }
            }
        }]
        
        # Make LLM call using cached content
        response, metadata = self._make_cached_call(
            prompt=prompt,
            system_prompt="You are an expert discourse analyst. Extract specific evidence quotes for each dimension.",
            tools=tools,
            context="Evidence extraction with context cache"
        )
        
        # Extract tool calls from response
        tool_calls = self._extract_tool_calls(response, metadata)
        
        # Process the evidence
        evidence_data = self._process_evidence_tool_call(tool_calls, document_id)
        
        self.audit.log_agent_event(agent_name, "evidence_call_completed", {
            "document_id": document_id,
            "doc_index": doc_index,
            "evidence_count": len(evidence_data.get('evidence', [])),
            "cache_used": self.cached_content is not None
        })
        
        return evidence_data
    
    def _get_computational_work(self, framework: str, document_content: str, 
                               document_id: str, analysis_id: str, doc_index: int) -> Dict[str, Any]:
        """Third call: Get computational work (uses context cache)"""
        
        agent_name = "ContextCachingAnalysisAgent"
        
        # Create prompt for computational work (cached content already has framework/doc)
        prompt = self._create_work_prompt_cached(document_id)
        
        # Create tool definition for computational work
        tools = [{
            "type": "function",
            "function": {
                "name": "record_computational_work",
                "description": "Record computational analysis and derived metrics",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "document_id": {"type": "string"},
                        "computational_work": {
                            "type": "object",
                            "properties": {
                                "python_code": {"type": "string"},
                                "derived_metrics": {"type": "object"},
                                "statistical_analysis": {"type": "object"}
                            }
                        }
                    },
                    "required": ["document_id", "computational_work"]
                }
            }
        }]
        
        # Make LLM call using cached content
        response, metadata = self._make_cached_call(
            prompt=prompt,
            system_prompt="You are an expert discourse analyst. Perform computational analysis and derive metrics.",
            tools=tools,
            context="Computational work with context cache"
        )
        
        # Extract tool calls from response
        tool_calls = self._extract_tool_calls(response, metadata)
        
        # Process the computational work
        work_data = self._process_work_tool_call(tool_calls, document_id)
        
        self.audit.log_agent_event(agent_name, "work_call_completed", {
            "document_id": document_id,
            "doc_index": doc_index,
            "has_python_code": bool(work_data.get('work', {}).get('python_code')),
            "cache_used": self.cached_content is not None
        })
        
        return work_data
    
    def _create_context_cache(self, framework: str, document_content: str, document_id: str):
        """Create Vertex AI context cache with framework and document content"""
        if not VERTEX_AI_AVAILABLE:
            self.audit.log_agent_event("ContextCachingAnalysisAgent", "cache_creation_failed", {
                "error": "Vertex AI not available",
                "document_id": document_id
            })
            return
        
        try:
            # Initialize Vertex AI (assuming project is already set)
            # vertexai.init(project="your-project-id", location="us-central1")
            
            # Create system instruction
            system_instruction = "You are an expert discourse analyst specializing in populist rhetoric analysis using the PDAF framework."
            
            # Create content to cache (framework + document)
            content_text = f"**FRAMEWORK:**\n{framework}\n\n**DOCUMENT:**\nFilename: {document_id}\nContent: {document_content}"
            contents = [Part.from_text(content_text)]
            
            # Create cached content
            self.cached_content = caching.CachedContent.create(
                model_name="gemini-2.5-flash",
                system_instruction=system_instruction,
                contents=contents,
                ttl=timedelta(minutes=60)  # 1 hour TTL
            )
            
            self.cache_name = self.cached_content.name
            
            self.audit.log_agent_event("ContextCachingAnalysisAgent", "cache_created", {
                "cache_name": self.cache_name,
                "document_id": document_id,
                "content_length": len(content_text)
            })
            
        except Exception as e:
            self.audit.log_agent_event("ContextCachingAnalysisAgent", "cache_creation_failed", {
                "error": str(e),
                "document_id": document_id
            })
            # Fall back to regular calls
            self.cached_content = None
    
    def _make_cached_call(self, prompt: str, system_prompt: str, tools: List[Dict[str, Any]], context: str) -> Tuple[str, Dict[str, Any]]:
        """Make LLM call using cached content if available, otherwise fall back to regular call"""
        if self.cached_content and VERTEX_AI_AVAILABLE:
            try:
                # Use cached content
                model = GenerativeModel.from_cached_content(cached_content=self.cached_content)
                response = model.generate_content(
                    prompt,
                    tools=tools,
                    generation_config={
                        "temperature": 0.1,
                        "max_output_tokens": 4000
                    }
                )
                
                # Extract content and tool calls
                content = response.text or ""
                tool_calls = getattr(response, 'candidates', [{}])[0].get('content', {}).get('parts', [])
                
                metadata = {
                    "success": True,
                    "model": "gemini-2.5-flash",
                    "cached_content_used": True,
                    "cache_name": self.cache_name,
                    "tool_calls": tool_calls
                }
                
                self.audit.log_agent_event("ContextCachingAnalysisAgent", "cached_call_made", {
                    "context": context,
                    "cache_name": self.cache_name,
                    "response_length": len(content)
                })
                
                return content, metadata
                
            except Exception as e:
                self.audit.log_agent_event("ContextCachingAnalysisAgent", "cached_call_failed", {
                    "error": str(e),
                    "context": context,
                    "falling_back": True
                })
                # Fall back to regular call
        
        # Fall back to regular LLM call
        return self.gateway.execute_call_with_tools(
            model="vertex_ai/gemini-2.5-flash",
            prompt=prompt,
            system_prompt=system_prompt,
            tools=tools,
            force_function_calling=True,
            temperature=0.1,
            max_tokens=4000
        )
    
    def _create_scores_prompt_cached(self, document_id: str) -> str:
        """Create prompt for dimensional scoring when using cached content"""
        return f"""Analyze the document using the PDAF framework and record dimensional scores for all 9 dimensions.

**REQUIRED DIMENSIONS TO SCORE:**
1. Manichaean People-Elite Framing (0.0-1.0)
2. Crisis-Restoration Temporal Narrative (0.0-1.0) 
3. Popular Sovereignty Claims (0.0-1.0)
4. Anti-Pluralist Exclusion (0.0-1.0)
5. Elite Conspiracy/Systemic Corruption (0.0-1.0)
6. Authenticity vs. Political Class (0.0-1.0)
7. Homogeneous People Construction (0.0-1.0)
8. Nationalist Exclusion (0.0-1.0)
9. Economic Populist Appeals (0.0-1.0)

**INSTRUCTIONS:**
1. Read the document carefully and identify populist discourse patterns
2. For each dimension, provide a score from 0.0-1.0 based on the framework definitions
3. Use the record_analysis_scores tool to save your results
4. Include all 9 dimensions in your response

Begin analysis now."""
    
    def _create_scores_prompt(self, framework: str, document_content: str, document_id: str) -> str:
        """Create prompt for dimensional scoring"""
        return f"""Analyze the following document using the PDAF framework and record dimensional scores for all 9 dimensions.

**FRAMEWORK:**
{framework}

**DOCUMENT:**
Filename: {document_id}
Content: {document_content}

**REQUIRED DIMENSIONS TO SCORE:**
1. Manichaean People-Elite Framing (0.0-1.0)
2. Crisis-Restoration Temporal Narrative (0.0-1.0) 
3. Popular Sovereignty Claims (0.0-1.0)
4. Anti-Pluralist Exclusion (0.0-1.0)
5. Elite Conspiracy/Systemic Corruption (0.0-1.0)
6. Authenticity vs. Political Class (0.0-1.0)
7. Homogeneous People Construction (0.0-1.0)
8. Nationalist Exclusion (0.0-1.0)
9. Economic Populist Appeals (0.0-1.0)

**INSTRUCTIONS:**
1. Read the document carefully and identify populist discourse patterns
2. For each dimension, provide a score from 0.0-1.0 based on the framework definitions
3. Use the record_analysis_scores tool to save your results
4. Include all 9 dimensions in your response

Begin analysis now."""
    
    def _create_evidence_prompt(self, framework: str, document_content: str, document_id: str) -> str:
        """Create prompt for evidence extraction"""
        return f"""Extract specific textual evidence for each dimension from the following document.

**FRAMEWORK:**
{framework}

**DOCUMENT:**
Filename: {document_id}
Content: {document_content}

**INSTRUCTIONS:**
1. Find specific quotes that demonstrate each dimension
2. Provide context for each quote
3. Rate relevance on a 0.0-1.0 scale
4. Use the record_evidence_quotes tool to save your results

Begin evidence extraction now."""
    
    def _create_work_prompt(self, framework: str, document_content: str, document_id: str) -> str:
        """Create prompt for computational work"""
        return f"""Perform computational analysis and derive metrics for the following document.

**FRAMEWORK:**
{framework}

**DOCUMENT:**
Filename: {document_id}
Content: {document_content}

**INSTRUCTIONS:**
1. Write Python code to calculate derived metrics
2. Perform statistical analysis where appropriate
3. Use the record_computational_work tool to save your results

Begin computational analysis now."""
    
    def _create_evidence_prompt_cached(self, document_id: str) -> str:
        """Create prompt for evidence extraction when using cached content"""
        return f"""Extract specific textual evidence for each dimension from the document.

**REQUIRED DIMENSIONS TO EXTRACT EVIDENCE FOR:**
1. Manichaean People-Elite Framing
2. Crisis-Restoration Temporal Narrative
3. Popular Sovereignty Claims
4. Anti-Pluralist Exclusion
5. Elite Conspiracy/Systemic Corruption
6. Authenticity vs. Political Class
7. Homogeneous People Construction
8. Nationalist Exclusion
9. Economic Populist Appeals

**INSTRUCTIONS:**
1. Find specific quotes that demonstrate each dimension
2. Provide context for each quote
3. Rate relevance on a 0.0-1.0 scale
4. Use the record_evidence_quotes tool to save your results

Begin evidence extraction now."""
    
    def _create_work_prompt_cached(self, document_id: str) -> str:
        """Create prompt for computational work when using cached content"""
        return f"""Perform computational analysis and derive metrics for the document.

**INSTRUCTIONS:**
1. Write Python code to calculate derived metrics
2. Perform statistical analysis where appropriate
3. Use the record_computational_work tool to save your results

Begin computational analysis now."""
    
    def _extract_tool_calls(self, response: str, metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract tool calls from LLM response"""
        # The gateway already extracts tool calls and puts them in metadata
        tool_calls = metadata.get('tool_calls', [])
        return tool_calls if tool_calls is not None else []
    
    def _process_scores_tool_call(self, tool_calls: List[Dict[str, Any]], document_id: str) -> Dict[str, Any]:
        """Process scores tool call"""
        for tool_call in tool_calls:
            # Handle both dict format and ChatCompletionMessageToolCall format
            if hasattr(tool_call, 'function'):
                # ChatCompletionMessageToolCall format
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
            else:
                # Dict format
                function_name = tool_call.get('function', {}).get('name')
                function_args = json.loads(tool_call['function']['arguments'])
            
            if function_name == 'record_analysis_scores':
                return {'scores': function_args.get('dimensional_scores', {})}
        
        return {'scores': {}}
    
    def _process_evidence_tool_call(self, tool_calls: List[Dict[str, Any]], document_id: str) -> Dict[str, Any]:
        """Process evidence tool call"""
        for tool_call in tool_calls:
            # Handle both dict format and ChatCompletionMessageToolCall format
            if hasattr(tool_call, 'function'):
                # ChatCompletionMessageToolCall format
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
            else:
                # Dict format
                function_name = tool_call.get('function', {}).get('name')
                function_args = json.loads(tool_call['function']['arguments'])
            
            if function_name == 'record_evidence_quotes':
                return {'evidence': function_args.get('evidence_quotes', [])}
        
        return {'evidence': []}
    
    def _process_work_tool_call(self, tool_calls: List[Dict[str, Any]], document_id: str) -> Dict[str, Any]:
        """Process computational work tool call"""
        for tool_call in tool_calls:
            # Handle both dict format and ChatCompletionMessageToolCall format
            if hasattr(tool_call, 'function'):
                # ChatCompletionMessageToolCall format
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
            else:
                # Dict format
                function_name = tool_call.get('function', {}).get('name')
                function_args = json.loads(tool_call['function']['arguments'])
            
            if function_name == 'record_computational_work':
                return {'work': function_args.get('computational_work', {})}
        
        return {'work': {}}
    
    def _aggregate_results(self, all_results: List[Dict[str, Any]], analysis_id: str) -> Dict[str, Any]:
        """Aggregate results from all documents"""
        return {
            'analysis_id': analysis_id,
            'document_count': len(all_results),
            'results': all_results,
            'aggregated_scores': self._aggregate_scores(all_results),
            'aggregated_evidence': self._aggregate_evidence(all_results),
            'metadata': {
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'agent': 'ContextCachingAnalysisAgent'
            }
        }
    
    def _aggregate_scores(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Aggregate dimensional scores across documents"""
        # Simplified implementation
        return {}
    
    def _aggregate_evidence(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Aggregate evidence across documents"""
        # Simplified implementation
        return []
    
    def _generate_analysis_id(self, framework: str, documents: List[Dict[str, Any]], 
                             config: Dict[str, Any]) -> str:
        """Generate unique analysis ID"""
        content = f"{framework}{len(documents)}{str(config)}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]
