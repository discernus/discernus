#!/usr/bin/env python3
"""
Corpus Chunking for Rate Limit Management
========================================

THIN approach to handling large academic corpora within API rate limits.
Pure infrastructure - no content interpretation, just smart chunking.
"""

from typing import Dict, List, Tuple
import asyncio
import time

def estimate_token_count(text: str) -> int:
    """Rough token estimation - Claude uses ~4 chars per token"""
    return len(text) // 4

def chunk_corpus_by_size(files: Dict[str, str], max_tokens_per_chunk: int = 15000) -> List[Dict[str, str]]:
    """
    Chunk corpus into manageable sizes for rate limiting
    
    THIN principle: Just divide by size, no content interpretation
    """
    chunks = []
    current_chunk = {}
    current_tokens = 0
    
    for filename, content in files.items():
        file_tokens = estimate_token_count(content)
        
        # If adding this file would exceed limit, start new chunk
        if current_tokens + file_tokens > max_tokens_per_chunk and current_chunk:
            chunks.append(current_chunk)
            current_chunk = {}
            current_tokens = 0
        
        # If single file is too large, split it
        if file_tokens > max_tokens_per_chunk:
            # Split large file into smaller pieces
            chunk_size = max_tokens_per_chunk * 4  # Convert back to chars
            for i in range(0, len(content), chunk_size):
                chunk_content = content[i:i + chunk_size]
                chunk_filename = f"{filename}_part_{i//chunk_size + 1}"
                
                if current_chunk:
                    chunks.append(current_chunk)
                    current_chunk = {}
                    current_tokens = 0
                
                chunks.append({chunk_filename: chunk_content})
        else:
            current_chunk[filename] = content
            current_tokens += file_tokens
    
    # Add final chunk if not empty
    if current_chunk:
        chunks.append(current_chunk)
    
    return chunks

def create_chunked_detective_prompt(chunk: Dict[str, str], chunk_index: int, total_chunks: int) -> str:
    """Create detective prompt for a specific chunk"""
    
    file_summary = ""
    for filename, content in chunk.items():
        preview = content[:200] + "..." if len(content) > 200 else content
        file_summary += f"\n{filename}:\n{preview}\n{'-' * 40}\n"
    
    return f"""
You are a research corpus detective analyzing CHUNK {chunk_index + 1} of {total_chunks}.

This chunk contains {len(chunk)} files from a larger corpus. Your job is to:

1. Analyze what each file in this chunk contains
2. Identify potential issues (duplicates, corruption, etc.)
3. Determine metadata you can infer from content
4. Note any patterns or themes in this chunk

Here are the files in this chunk:
{file_summary}

Please provide:
1. CHUNK {chunk_index + 1} ANALYSIS: What you think each file contains
2. PATTERNS: Any patterns or themes you notice in this chunk
3. METADATA INFERENCE: What you can determine about these texts
4. ISSUES: Any files that seem problematic

Remember: This is chunk {chunk_index + 1} of {total_chunks}. Focus on this specific chunk.
"""

async def analyze_corpus_in_chunks(files: Dict[str, str], llm_client, max_tokens_per_chunk: int = 15000) -> str:
    """
    Analyze large corpus by chunking with rate limit management
    
    Returns combined analysis from all chunks
    """
    chunks = chunk_corpus_by_size(files, max_tokens_per_chunk)
    
    print(f"📊 Corpus chunked into {len(chunks)} parts for rate limit management")
    
    chunk_analyses = []
    
    for i, chunk in enumerate(chunks):
        print(f"🔍 Analyzing chunk {i + 1}/{len(chunks)}...")
        
        prompt = create_chunked_detective_prompt(chunk, i, len(chunks))
        
        # Add delay between chunks to manage rate limits
        if i > 0:
            print("⏱️ Waiting 10 seconds between chunks for rate limiting...")
            time.sleep(10)
        
        try:
            if llm_client:
                analysis = llm_client.call_llm(prompt, "design_llm")
            else:
                analysis = f"Mock analysis for chunk {i + 1}: Would analyze {list(chunk.keys())}"
            
            chunk_analyses.append(f"## CHUNK {i + 1} ANALYSIS:\n{analysis}\n")
            
        except Exception as e:
            print(f"⚠️ Error analyzing chunk {i + 1}: {e}")
            chunk_analyses.append(f"## CHUNK {i + 1} ANALYSIS:\nError occurred: {e}\n")
    
    # Combine all chunk analyses
    combined_analysis = f"""
CORPUS ANALYSIS (CHUNKED APPROACH):
Total files: {len(files)}
Analyzed in {len(chunks)} chunks for rate limit management

{''.join(chunk_analyses)}

OVERALL SUMMARY:
The corpus has been analyzed in chunks to manage API rate limits. Each chunk provides detailed analysis above. 
Key patterns and themes should be evident across chunks.

CLARIFYING QUESTIONS:
Based on the chunked analysis, what specific research questions would you like to explore with this corpus?
"""
    
    return combined_analysis

def should_use_chunking(files: Dict[str, str], rate_limit_threshold: int = 50000) -> bool:
    """
    Determine if corpus should be chunked based on estimated token count
    
    Args:
        files: Corpus files
        rate_limit_threshold: Token count above which to use chunking
    
    Returns:
        True if chunking is recommended
    """
    total_tokens = sum(estimate_token_count(content) for content in files.values())
    
    return total_tokens > rate_limit_threshold 