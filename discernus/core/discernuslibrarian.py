#!/usr/bin/env python3
"""
DiscernusLibrarian: Citation-Guided Research Agent
Ultra-THIN implementation with Vertex AI for cost-effective literature discovery
"""
import os
import requests
import json
import urllib.parse
import xml.etree.ElementTree as ET
import time
from typing import Dict, List, Any, Optional
from datetime import datetime
from discernus.gateway.llm_gateway import LLMGateway
from discernus.gateway.model_registry import ModelRegistry

class DiscernusLibrarian:
    """
    DiscernusLibrarian - Multi-stage validation with LLM intelligence
    Specializes in academic literature discovery, validation, and synthesis
    Uses Perplexity for literature search and Claude/Gemini for analysis
    """
    
    def __init__(self):
        # Set up Vertex AI environment for ultra-cheap pricing
        os.environ['VERTEXAI_PROJECT'] = 'gen-lang-client-0199646265'
        os.environ['VERTEXAI_LOCATION'] = 'us-central1'
        
        # Use the working LLM Gateway infrastructure
        self.model_registry = ModelRegistry()
        self.gateway = LLMGateway(self.model_registry)
        
        # Model selection for cost optimization
        self.research_model = "vertex_ai/gemini-2.5-flash"  # Ultra-cheap: $0.13/$0.38 per 1M tokens
        self.synthesis_model = "vertex_ai/gemini-2.5-flash"  # Same model for consistency
        self.critique_model = "vertex_ai/gemini-2.5-pro"     # Smart & cost-effective red team critique
        
        print("📚 DiscernusLibrarian initialized with multi-stage literature validation")
        print(f"🔬 Literature review models: Claude 3.5 Sonnet + Perplexity r1-1776 + Gemini 2.5 Flash")
    
    def research_question(self, question: str, save_results: bool = True) -> Dict[str, Any]:
        """
        Main research workflow: LLM Strategy → Literature Discovery → Synthesis → Critique
        """
        print(f"\n🔍 Research Question: {question}")
        
        # Phase 0: LLM Strategic Intelligence (THIN Philosophy - Use LLM to guide, not replace research)
        print("🧠 Phase 0: LLM Strategic Intelligence...")
        llm_intelligence = self._gather_llm_intelligence(question)
        
        # Phase 1: Research Planning (ultra-cheap model, informed by LLM intelligence)
        print("📋 Phase 1: Research Planning...")
        research_plan = self._plan_research(question, llm_intelligence)
        
        # Phase 2: Multi-Stage Research Discovery & Validation (Perplexity-powered)
        print("📚 Phase 2: Multi-Stage Research Discovery & Validation...")
        research_data = self._multi_stage_research_discovery(question, research_plan)
        
        # Phase 3: Research Synthesis with Validation Data
        print("🔬 Phase 3: Research Synthesis...")
        synthesis = self._synthesize_validated_research(question, research_data, research_plan)
        
        # Phase 4: Enhanced Red Team Validation (Independent fact-checking)
        print("🥊 Phase 4: Enhanced Red Team Validation...")
        critique = self._enhanced_red_team_validation(synthesis, research_data)
        
        # Phase 5: Final Response (ultra-cheap model)
        print("🎯 Phase 5: Final Synthesis...")
        final_response = self._final_synthesis(synthesis, critique, question)
        
        # Calculate process transparency metrics
        process_metrics = self._calculate_process_metrics(research_data)
        
        result = {
            'question': question,
            'llm_intelligence': llm_intelligence,
            'research_plan': research_plan,
            'research_data': research_data,
            'studies_analyzed': process_metrics.get('total_studies_analyzed', 0),
            'synthesis': synthesis,
            'critique': critique,
            'final_response': final_response,
            'process_metrics': process_metrics,
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'validation_method': 'Multi-stage Perplexity validation with enhanced red team fact-checking'
        }
        
        # Save results to file
        if save_results:
            self._save_results(result)
        
        return result
    
    def _save_results(self, result: Dict[str, Any]):
        """Save research results to organized librarian directory structure"""
        import os
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Ensure librarian directories exist
        base_path = "discernus/librarian"
        reports_dir = f"{base_path}/reports"
        data_dir = f"{base_path}/research_data"
        
        os.makedirs(reports_dir, exist_ok=True)
        os.makedirs(data_dir, exist_ok=True)
        
        # Save research data (JSON)
        data_filename = f"{data_dir}/discernus_librarian_data_{timestamp}.json"
        
        try:
            with open(data_filename, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"💾 Research data saved to: {data_filename}")
            
            # Save readable report (Markdown)
            report_filename = f"{reports_dir}/discernus_librarian_report_{timestamp}.md"
            self._create_markdown_report(result, report_filename)
            print(f"📄 Human-readable report saved to: {report_filename}")
            
        except Exception as e:
            print(f"⚠️ Failed to save results: {e}")
    
    def _create_markdown_report(self, result: Dict[str, Any], filename: str):
        """Create a human-readable markdown report with process transparency"""
        process_metrics = result.get('process_metrics', {})
        
        report = f"""# DiscernusLibrarian Literature Review

**Research Question:** {result['question']}
**Timestamp:** {result['timestamp']}
**Studies Analyzed:** {result['studies_analyzed']}
**Validation Method:** {result['validation_method']}

---

## 🔍 Process Summary (Multi-Stage Validation Report)

**Research Methodology Overview:**
- **Phase 0**: LLM Strategic Intelligence → Research direction and terminology guidance
- **Phase 1**: Systematic Research Planning → Search strategy development  
- **Phase 2**: Multi-Stage Research Validation → 3-stage Perplexity validation process
  - **Stage 2.1**: Initial Research Discovery → Comprehensive literature identification
  - **Stage 2.2**: Counter-Evidence Analysis → Contradictory findings and alternative perspectives
  - **Stage 2.3**: Completeness Verification → Systematic gap analysis and missing research
- **Phase 3**: Validated Research Synthesis → Multi-stage evidence integration
- **Phase 4**: Enhanced Red Team Validation → Independent fact-checking and verification
- **Phase 5**: Final Research Report → Academically rigorous conclusions

**Validation Results:**
- **Total Studies Analyzed:** {result['studies_analyzed']}
- **Research Method:** {process_metrics.get('research_method', 'N/A')}
- **Validation Approach:** {process_metrics.get('validation_approach', 'N/A')}

**Quality Indicators:**"""

        # Add quality indicators
        for indicator, description in process_metrics.get('quality_indicators', {}).items():
            report += f"""
- **{indicator.replace('_', ' ').title()}:** {description}"""

        report += f"""

---

## 📊 Multi-Stage Research Validation Breakdown

**Validation Stages:**"""
        
        # Add validation stage breakdown
        for stage, result_desc in process_metrics.get('validation_stages', {}).items():
            report += f"""
- **{stage.replace('_', ' ').title()}:** {result_desc}"""

        report += f"""

---

## 🧠 LLM Strategic Intelligence

**Phase 0 Research Direction (THIN Philosophy - LLM guides strategy, evidence provides answers):**

{result.get('llm_intelligence', 'Strategic intelligence not available')}

---

## 📋 Systematic Research Plan

**Phase 1 Search Strategy (Informed by LLM Intelligence):**

{result['research_plan']}

---

## 🔍 Stage 1: Initial Research Discovery

{result['research_data'].get('initial_research', 'Initial research not available')}

---

## ⚖️ Stage 2: Counter-Evidence & Alternative Perspectives  

{result['research_data'].get('counter_research', 'Counter-research not available')}

---

## 📋 Stage 3: Literature Completeness Check

{result['research_data'].get('completeness_check', 'Completeness check not available')}

"""

        report += f"""
---

## 🔬 Initial Research Synthesis

{result['synthesis']}

---

## 🥊 Red Team Critique

{result['critique']}

---

## 🎯 Final Research Synthesis

{result['final_response']}

---

*Generated by Ultra-THIN DiscernusLibrarian with Vertex AI Gemini 2.5 Flash*
"""
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(report)
        except Exception as e:
            print(f"⚠️ Failed to create markdown report: {e}")

    def _gather_llm_intelligence(self, question: str) -> str:
        """Phase 0: Use LLM intelligence to guide research strategy (THIN Philosophy)"""
        prompt = f"""You are an expert research consultant. I need strategic intelligence to guide a systematic literature search.

Research Question: {question}

Please provide strategic guidance (NOT factual claims, but research direction):

1. **Key Academic Terminology**: What terms and synonyms would academics use to discuss this topic across disciplines?

2. **Research Domains**: Which academic fields would study this question? (e.g., Psychology, Political Science, Communication Studies, Sociology)

3. **Methodological Approaches**: What research methods would scholars likely use to investigate this?

4. **Critical Perspectives**: What debates, limitations, or contradictory views should we look for?

5. **Landmark Studies**: What types of seminal papers or influential researchers might exist in this area?

6. **Cross-Disciplinary Connections**: How might different fields approach this question differently?

IMPORTANT: Do NOT provide factual claims or conclusions. Focus on strategic guidance for WHERE and HOW to search for evidence."""

        response, metadata = self.gateway.execute_call(
            model="anthropic/claude-3-5-sonnet-20240620",  # Best model for strategic intelligence
            prompt=prompt,
            system_prompt="You are providing research strategy guidance, not factual claims. Focus on search methodology and terminology."
        )
        return response

    def _multi_stage_research_discovery(self, question: str, research_plan: str) -> Dict[str, Any]:
        """Multi-stage research validation using Perplexity for comprehensive coverage"""
        
        # Stage 1: Initial Research Discovery
        print("🔍 Stage 1: Initial Research Discovery...")
        initial_research = self._perplexity_research_discovery(question, research_plan)
        
        # Stage 2: Gap Analysis & Counter-Research  
        print("🔍 Stage 2: Gap Analysis & Counter-Research...")
        counter_research = self._perplexity_gap_analysis(question, initial_research)
        
        # Stage 3: Literature Completeness Check
        print("🔍 Stage 3: Literature Completeness Validation...")
        completeness_check = self._perplexity_completeness_check(question, initial_research)
        
        # Combine all research phases
        combined_research = {
            'initial_research': initial_research,
            'counter_research': counter_research, 
            'completeness_check': completeness_check,
            'research_method': 'multi_stage_perplexity_validation'
        }
        
        return combined_research

    def _perplexity_research_discovery(self, question: str, research_plan: str) -> str:
        """Stage 1: Use Perplexity for initial comprehensive research discovery"""
        prompt = f"""I need you to find peer-reviewed academic research on this question: {question}

Research Strategy Context:
{research_plan}

Please identify 8-10 specific published studies from academic journals, including:
1. Full citations with authors, year, journal, and DOI
2. Key methodology used (experimental, longitudinal, survey, computational, etc.)  
3. Sample sizes and populations studied
4. Main findings with specific effect sizes or statistical results where available
5. Any limitations or critiques mentioned in the papers

Focus on high-quality empirical research with robust methodology. Prioritize studies from top-tier journals and recent research (2018+) while including foundational works where relevant.

Include diverse methodological approaches and ensure geographic/cultural diversity where possible."""

        response, metadata = self.gateway.execute_call(
            model="perplexity/r1-1776",
            prompt=prompt,
            system_prompt="You are a research librarian finding peer-reviewed academic literature with precise citations."
        )
        return response

    def _perplexity_gap_analysis(self, question: str, initial_research: str) -> str:
        """Stage 2: Use Perplexity to find contradictory evidence and research gaps"""
        prompt = f"""I conducted initial research on: {question}

Initial Research Found:
{initial_research[:1000]}...

Now I need you to find CONTRADICTORY evidence, alternative explanations, and research gaps:

1. **Counter-Evidence**: Find peer-reviewed studies that challenge or contradict the main findings above
2. **Alternative Explanations**: Research proposing different causal mechanisms or interpretations  
3. **Methodological Critiques**: Studies that critique the research methods or measurement approaches
4. **Null Results**: Studies that found no effects or mixed findings
5. **Missing Perspectives**: Research from underrepresented populations, non-Western contexts, or different disciplines

Be thorough in finding studies that disagree with or complicate the narrative from the initial research. Include full citations and specific findings that challenge the initial conclusions."""

        response, metadata = self.gateway.execute_call(
            model="perplexity/r1-1776", 
            prompt=prompt,
            system_prompt="You are finding contradictory evidence and alternative perspectives to ensure balanced research coverage."
        )
        return response

    def _perplexity_completeness_check(self, question: str, initial_research: str) -> str:
        """Stage 3: Use Perplexity to verify literature completeness and identify missing areas"""
        prompt = f"""Research Question: {question}

Based on this initial research summary:
{initial_research[:800]}...

Please conduct a COMPLETENESS CHECK to identify what might be missing:

1. **Major Research Gaps**: What important aspects of this question haven't been adequately studied?
2. **Methodological Gaps**: What research methods haven't been applied that could provide valuable insights?
3. **Population Gaps**: What demographic groups, cultures, or contexts are underrepresented?
4. **Temporal Gaps**: Are there important time periods or longitudinal aspects missing?
5. **Interdisciplinary Gaps**: What academic fields should be studying this but seem absent?
6. **Recent Developments**: What recent studies (2022-2024) might be missing?

Also identify 3-5 additional high-quality studies that would strengthen the literature base, focusing on filling the identified gaps."""

        response, metadata = self.gateway.execute_call(
            model="perplexity/r1-1776",
            prompt=prompt, 
            system_prompt="You are evaluating research completeness and identifying systematic gaps in the literature."
        )
        return response

    def _enhanced_red_team_validation(self, synthesis: str, research_data: Dict[str, Any]) -> str:
        """Enhanced Red Team with independent research capabilities for fact-checking"""
        prompt = f"""You are a RED TEAM researcher conducting independent fact-checking and validation.

You have been presented with this research synthesis:
{synthesis[:1500]}...

Your job is to VERIFY key claims independently using your own research capabilities:

1. **Citation Verification**: Check specific citations mentioned - verify authors, journals, years, DOIs
2. **Fact-Check Numbers**: Verify any statistical claims, effect sizes, sample sizes, percentages  
3. **Methodology Verification**: Check if study designs are accurately described (experimental vs observational, etc.)
4. **Missing Counter-Evidence**: Find studies that contradict the main conclusions
5. **Source Quality Assessment**: Evaluate if the cited journals are reputable and peer-reviewed
6. **Bias Detection**: Look for selection bias in which studies were included/excluded
7. **Replication Status**: Check if key findings have been replicated in other studies

Be skeptical and thorough. If you find any inaccuracies, misrepresentations, or critical omissions, report them clearly with your own independent evidence.

Focus especially on verifying any quantitative claims (percentages, effect sizes, sample sizes) and ensuring experimental vs correlational studies are properly distinguished."""

        response, metadata = self.gateway.execute_call(
            model="perplexity/r1-1776",
            prompt=prompt,
            system_prompt="You are an independent fact-checker with research capabilities. Be skeptical and verify claims thoroughly."
        )
        return response

    def _plan_research(self, question: str, llm_intelligence: str) -> str:
        """Phase 1: Create focused research plan informed by LLM strategic intelligence"""
        prompt = f"""You are a research librarian creating a systematic literature search plan.

Research Question: {question}

Strategic Intelligence from Expert Consultant:
{llm_intelligence}

Based on this strategic guidance, create a focused research plan that includes:
1. Key concepts and terms to search for (informed by the strategic guidance)
2. Likely academic disciplines to target
3. Important authors or seminal papers to look for
4. Search strategy for maximum literature coverage
5. Critical perspectives and debates to include

Be specific and actionable. Focus on findable, citable academic sources."""

        response, metadata = self.gateway.execute_call(
            model=self.research_model,
            prompt=prompt,
            system_prompt="You are a research librarian creating a systematic literature search plan."
        )
        return response
    
    def _synthesize_validated_research(self, question: str, research_data: Dict[str, Any], research_plan: str) -> str:
        """Phase 3: Synthesize findings from multi-stage validated research"""
        
        initial_research = research_data.get('initial_research', '')
        counter_research = research_data.get('counter_research', '')
        completeness_check = research_data.get('completeness_check', '')
        
        prompt = f"""You are synthesizing academic research with rigorous, evidence-based confidence levels using MULTI-STAGE VALIDATED research.

Research Question: {question}

Research Plan Context: {research_plan}

MULTI-STAGE RESEARCH VALIDATION:

=== STAGE 1: INITIAL RESEARCH DISCOVERY ===
{initial_research}

=== STAGE 2: COUNTER-EVIDENCE & ALTERNATIVE PERSPECTIVES ===
{counter_research}

=== STAGE 3: LITERATURE COMPLETENESS CHECK ===
{completeness_check}

Create a comprehensive research synthesis using this EVIDENCE-BASED CONFIDENCE SYSTEM:

**CONFIDENCE CRITERIA:**
- HIGH (Score 8-10): 
  * Multiple peer-reviewed studies supporting claim across stages
  * Consistent findings even when counter-evidence is considered
  * Well-replicated results with robust methodology
  * Evidence withstands completeness analysis scrutiny

- MEDIUM (Score 5-7):
  * Some supporting studies but notable counter-evidence exists
  * Mixed findings across different methodological approaches
  * Some gaps identified in completeness check
  * Moderate certainty with acknowledged limitations

- LOW (Score 1-4):
  * Limited supporting evidence or strong counter-evidence
  * Significant methodological concerns or gaps
  * High uncertainty due to contradictory findings
  * Major limitations identified in completeness analysis

**REQUIRED SYNTHESIS STRUCTURE:**
For each major claim, provide:
1. The evidence-based claim statement
2. Confidence level (HIGH/MEDIUM/LOW) with numerical score (1-10)
3. Supporting evidence from Stage 1 research
4. Counter-evidence and limitations from Stage 2 analysis
5. Research gaps and missing perspectives from Stage 3 completeness check
6. Overall assessment balancing all three stages

Address these areas:
1. **Convergent Findings**: What conclusions are supported across all research stages?
2. **Contradictory Evidence**: Where do findings conflict and why?
3. **Research Gaps**: What important questions remain unanswered?
4. **Methodological Strengths/Weaknesses**: Quality assessment across the literature
5. **Future Research Priorities**: Based on the completeness analysis

Be especially rigorous - assign lower confidence when counter-evidence is strong or when completeness analysis reveals significant gaps. This multi-stage approach ensures we avoid confirmation bias and selective reporting."""

        response, metadata = self.gateway.execute_call(
            model="anthropic/claude-3-5-sonnet-20240620",  # Best model for nuanced synthesis
            prompt=prompt,
            system_prompt="You are synthesizing multi-stage validated academic research with rigorous confidence assessments."
        )
        return response
    
    def _calculate_process_metrics(self, research_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate transparency metrics for multi-stage Perplexity research validation"""
        initial_research = research_data.get('initial_research', '')
        counter_research = research_data.get('counter_research', '') 
        completeness_check = research_data.get('completeness_check', '')
        
        # Count approximate number of studies mentioned in each stage
        initial_count = len([line for line in initial_research.split('\n') if 'DOI:' in line or 'doi.org' in line])
        counter_count = len([line for line in counter_research.split('\n') if 'DOI:' in line or 'doi.org' in line])
        completeness_count = len([line for line in completeness_check.split('\n') if 'DOI:' in line or 'doi.org' in line])
        
        total_studies = initial_count + counter_count + completeness_count
        
        return {
            "research_method": "multi_stage_perplexity_validation",
            "validation_stages": {
                "initial_discovery": f"{initial_count} studies identified",
                "counter_research": f"{counter_count} contradictory/alternative studies",
                "completeness_check": f"{completeness_count} gap-filling studies"
            },
            "total_studies_analyzed": total_studies,
            "sources_used": ["Perplexity r1-1776 with academic database access"],
            "validation_approach": "3-stage cross-validation with independent fact-checking",
            "quality_indicators": {
                "research_validation": "Multi-stage counter-evidence analysis",
                "fact_checking": "Independent red team verification", 
                "completeness_verification": "Systematic gap analysis conducted",
                "source_quality": "Perplexity academic database integration"
            }
        }
    
    def _discover_literature(self, question: str, research_plan: str) -> List[Dict[str, Any]]:
        """Phase 2: Enhanced multi-API literature discovery with validation"""
        # Extract search terms from research plan using LLM
        search_terms = self._extract_search_terms(research_plan)
        
        papers = []
        sources_tried = []
        
        # Try multiple APIs for better coverage with respectful rate limiting
        for i, term in enumerate(search_terms[:5]):  # Limit to 5 terms for cost control
            term_papers = []
            
            # Add longer delay between search terms to be respectful
            if i > 0:
                print(f"⏱️ Waiting 3 seconds between search terms (respectful API usage)...")
                time.sleep(3)
            
            # 1. Try Semantic Scholar first (often better abstracts, but strict rate limits)
            try:
                print(f"🔍 Searching Semantic Scholar for: '{term}'")
                semantic_papers = self._search_semantic_scholar(term)
                # Tag papers with search term for transparency reporting
                for paper in semantic_papers:
                    paper['search_term'] = term
                term_papers.extend(semantic_papers)
                sources_tried.append(f"Semantic Scholar: {len(semantic_papers)} papers for '{term}'")
                time.sleep(2)  # Longer delay for Semantic Scholar (strict rate limits)
            except Exception as e:
                print(f"⚠️ Semantic Scholar search failed for '{term}': {e}")
            
            # 2. Try CrossRef if we need more papers
            if len(term_papers) < 5:
                try:
                    print(f"🔍 Searching CrossRef for: '{term}'")
                    crossref_papers = self._search_crossref(term)
                    # Tag papers with search term for transparency reporting
                    for paper in crossref_papers:
                        paper['search_term'] = term
                    term_papers.extend(crossref_papers)
                    sources_tried.append(f"CrossRef: {len(crossref_papers)} papers for '{term}'")
                    time.sleep(1)  # Moderate delay for CrossRef
                except Exception as e:
                    print(f"⚠️ CrossRef search failed for '{term}': {e}")
            
            # 3. Try arXiv for cutting-edge research
            try:
                print(f"🔍 Searching arXiv for: '{term}'")
                arxiv_papers = self._search_arxiv(term)
                # Tag papers with search term for transparency reporting
                for paper in arxiv_papers:
                    paper['search_term'] = term
                term_papers.extend(arxiv_papers)
                sources_tried.append(f"arXiv: {len(arxiv_papers)} papers for '{term}'")
                time.sleep(1)  # Moderate delay for arXiv
            except Exception as e:
                print(f"⚠️ arXiv search failed for '{term}': {e}")
            
            # Add to main papers list
            papers.extend(term_papers)
        
        # Remove duplicates based on DOI
        unique_papers = []
        seen_dois = set()
        for paper in papers:
            doi = (paper.get('doi') or '').lower()
            if doi and doi not in seen_dois:
                seen_dois.add(doi)
                unique_papers.append(paper)
            elif not doi:  # Keep papers without DOI but check titles
                title = (paper.get('title') or '').lower()
                if title and title not in {(p.get('title') or '').lower() for p in unique_papers}:
                    unique_papers.append(paper)
        
        # Validate papers (check DOIs, detect low-quality entries)
        validated_papers = self._validate_papers(unique_papers)
        
        # Phase 2.5: Bibliography Mining & Citation Network Crawling (Issue #100 Enhancement)
        if len(validated_papers) > 0:
            print(f"🕸️ Phase 2.5: Citation Network Exploration...")
            try:
                # Crawl citation networks from validated papers
                additional_papers = self._crawl_citation_network(validated_papers, max_additional_papers=5)
                
                if additional_papers:
                    print(f"📚 Found {len(additional_papers)} additional papers via citation networks")
                    # Combine and deduplicate all papers
                    all_papers = validated_papers + additional_papers
                    final_papers = self._deduplicate_papers_by_doi(all_papers)
                    print(f"📚 Total after citation network expansion: {len(final_papers)} papers")
                    validated_papers = final_papers
                else:
                    print(f"📚 No additional papers found via citation networks")
                    
            except Exception as e:
                print(f"⚠️ Citation network crawling failed, continuing with original papers: {e}")
        
        print(f"📚 Literature Discovery Results:")
        for source in sources_tried:
            print(f"  - {source}")
        print(f"📚 Total: {len(papers)} papers found, {len(unique_papers)} unique, {len(validated_papers)} validated")
        
        return validated_papers
    
    def _search_semantic_scholar(self, term: str) -> List[Dict[str, Any]]:
        """Search Semantic Scholar API for papers with rate limit handling"""
        papers = []
        max_retries = 3
        base_delay = 2
        
        for attempt in range(max_retries):
            try:
                url = "https://api.semanticscholar.org/graph/v1/paper/search"
                params = {
                    'query': term,
                    'limit': 5,
                    'fields': 'paperId,title,authors,year,abstract,openAccessPdf,citationCount'
                }
                
                # Add user-agent header for better API compatibility
                headers = {
                    'User-Agent': 'DiscernusLibrarian/1.0 (research tool) - Respectful API usage'
                }
                
                response = requests.get(url, params=params, headers=headers, timeout=15)
                
                if response.status_code == 200:
                    data = response.json()
                    for item in data.get('data', []):
                        papers.append({
                            'doi': f"semantic-scholar:{item.get('paperId', '')}",
                            'title': item.get('title', ''),
                            'authors': [author.get('name', '') for author in item.get('authors', [])],
                            'year': item.get('year'),
                            'abstract': item.get('abstract', ''),
                            'url': item.get('openAccessPdf', {}).get('url', '') if item.get('openAccessPdf') else '',
                            'citation_count': item.get('citationCount', 0),
                            'search_term': term,
                            'source': 'semantic_scholar'
                        })
                    break  # Success, exit retry loop
                    
                elif response.status_code == 429:
                    # Rate limited - exponential backoff
                    delay = base_delay * (2 ** attempt)
                    print(f"⚠️ Rate limited by Semantic Scholar. Waiting {delay} seconds (attempt {attempt + 1}/{max_retries})")
                    time.sleep(delay)
                    if attempt == max_retries - 1:
                        print(f"❌ Semantic Scholar rate limit exceeded after {max_retries} attempts for '{term}'")
                else:
                    print(f"Semantic Scholar API error: {response.status_code} - {response.text}")
                    break  # Don't retry non-rate-limit errors
                    
            except Exception as e:
                print(f"Semantic Scholar error for '{term}' (attempt {attempt + 1}): {e}")
                if attempt == max_retries - 1:
                    break
                time.sleep(base_delay)
        
        return papers

    def _search_crossref(self, term: str) -> List[Dict[str, Any]]:
        """Search CrossRef API for papers"""
        papers = []
        try:
            url = "https://api.crossref.org/works"
            params = {
                'query': term,
                'rows': 5,
                'sort': 'relevance',
                'select': 'DOI,title,author,published-print,abstract,URL'
            }
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                for item in data.get('message', {}).get('items', []):
                    papers.append({
                        'doi': item.get('DOI', ''),
                        'title': item.get('title', [''])[0] if item.get('title') else '',
                        'authors': [author.get('given', '') + ' ' + author.get('family', '') 
                                  for author in item.get('author', [])],
                        'year': item.get('published-print', {}).get('date-parts', [[None]])[0][0],
                        'abstract': item.get('abstract', ''),
                        'url': item.get('URL', ''),
                        'search_term': term,
                        'source': 'crossref'
                    })
        except Exception as e:
            print(f"CrossRef error for '{term}': {e}")
        
        return papers

    def _search_arxiv(self, term: str) -> List[Dict[str, Any]]:
        """Search arXiv API for papers"""
        papers = []
        try:
            # arXiv API expects URL-encoded query
            query = urllib.parse.quote(term)
            url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results=3"
            
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                root = ET.fromstring(response.content)
                
                # Parse arXiv XML response
                for entry in root.findall('.//{http://www.w3.org/2005/Atom}entry'):
                    title = entry.find('.//{http://www.w3.org/2005/Atom}title')
                    authors = entry.findall('.//{http://www.w3.org/2005/Atom}author')
                    published = entry.find('.//{http://www.w3.org/2005/Atom}published')
                    summary = entry.find('.//{http://www.w3.org/2005/Atom}summary')
                    arxiv_id = entry.find('.//{http://www.w3.org/2005/Atom}id')
                    
                    papers.append({
                        'doi': arxiv_id.text if arxiv_id is not None else '',
                        'title': title.text if title is not None else '',
                        'authors': [author.find('.//{http://www.w3.org/2005/Atom}name').text 
                                  for author in authors if author.find('.//{http://www.w3.org/2005/Atom}name') is not None],
                        'year': int(published.text[:4]) if published is not None else None,
                        'abstract': summary.text if summary is not None else '',
                        'url': arxiv_id.text if arxiv_id is not None else '',
                        'search_term': term,
                        'source': 'arxiv'
                    })
        except Exception as e:
            print(f"arXiv error for '{term}': {e}")
        
        return papers

    def _validate_papers(self, papers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Validate and filter papers for quality"""
        validated = []
        
        for paper in papers:
            # Quality checks
            quality_score = 0
            issues = []
            
            # Check for title
            if paper.get('title') and len(paper['title']) > 10:
                quality_score += 1
            else:
                issues.append("missing_or_short_title")
            
            # Check for authors
            if paper.get('authors') and len(paper['authors']) > 0:
                quality_score += 1
            else:
                issues.append("missing_authors")
            
            # Check for year (reasonable range)
            year = paper.get('year')
            if year and isinstance(year, int) and 1950 <= year <= 2025:
                quality_score += 1
            else:
                issues.append("invalid_year")
            
            # Check for abstract
            if paper.get('abstract') and len(paper['abstract']) > 50:
                quality_score += 1
            else:
                issues.append("missing_or_short_abstract")
            
            # Check DOI format (basic validation)
            doi = paper.get('doi', '')
            if doi and ('10.' in doi or 'semantic-scholar:' in doi or 'arxiv.org' in doi):
                quality_score += 1
            else:
                issues.append("invalid_doi")
            
            # Add quality metadata
            paper['quality_score'] = quality_score
            paper['quality_issues'] = issues
            
            # Only include papers with minimum quality (3/5 criteria)
            if quality_score >= 3:
                validated.append(paper)
        
        return validated

    def _extract_search_terms(self, research_plan: str) -> List[str]:
        """Extract diverse search terms including critical perspectives with semantic expansion"""
        prompt = f"""Extract 6-8 specific academic search terms from this research plan that include BOTH supportive and critical perspectives:

{research_plan}

Include terms that would find:
1. Core/supportive research (2-3 terms)
2. Critical perspectives and limitations (2-3 terms) 
3. Failed approaches or negative results (1-2 terms)

Return ONLY a JSON list of search terms, like: ["term 1", "term 2", "term 3", "criticism of term 1", "limitations of term 2", "bias in term 3"]
Use precise academic terminology that would work well in academic database searches."""

        response, metadata = self.gateway.execute_call(
            model=self.research_model,
            prompt=prompt,
            system_prompt="You are a research assistant extracting academic search terms."
        )
        
        try:
            # Clean and parse JSON response
            cleaned_response = response.strip()
            if cleaned_response.startswith('```json'):
                cleaned_response = cleaned_response.replace('```json', '').replace('```', '')
            elif cleaned_response.startswith('```'):
                cleaned_response = cleaned_response.replace('```', '')
            
            terms = json.loads(cleaned_response.strip())
            if isinstance(terms, list):
                # Apply semantic expansion to discovered terms
                expanded_terms = self._apply_semantic_expansion(terms)
                # Add critical search terms if not present
                critical_terms = self._add_critical_search_terms(expanded_terms)
                return critical_terms[:8]  # Limit to 8 terms to control costs
            else:
                raise ValueError("Response is not a list")
        except Exception as e:
            print(f"Warning: JSON parsing failed ({e}), using intelligent fallback")
            # Intelligent fallback: extract key concepts from research plan
            return self._intelligent_fallback_extraction(research_plan)

    def _add_critical_search_terms(self, base_terms: List[str]) -> List[str]:
        """Add critical perspectives to search terms if not already present"""
        critical_keywords = ["criticism", "limitations", "bias", "problems", "challenges", "failures"]
        
        # Check if critical terms already exist
        has_critical = any(keyword in ' '.join(base_terms).lower() for keyword in critical_keywords)
        
        if not has_critical:
            # Add critical terms based on the base terms
            if any("citation" in term.lower() for term in base_terms):
                base_terms.extend(["citation analysis criticism", "citation bias"])
            if any("network" in term.lower() for term in base_terms):
                base_terms.extend(["network analysis limitations"])
        
        return base_terms
    
    def _apply_semantic_expansion(self, base_terms: List[str]) -> List[str]:
        """Apply semantic expansion using domain-specific terminology mapping"""
        # Domain-specific terminology expansions based on Issue #100 requirements
        TERMINOLOGY_EXPANSIONS = {
            # Social Cohesion Research Domain
            "social cohesion": ["social capital", "collective efficacy", "community resilience", "social trust", "social bonds"],
            "social capital": ["social cohesion", "collective efficacy", "community bonds", "social trust"],
            "collective efficacy": ["social cohesion", "community resilience", "neighborhood efficacy"],
            
            # Discourse Analysis Domain
            "hostile discourse": ["divisive language", "hate speech", "incivility", "polarization", "negative partisanship"],
            "cooperative discourse": ["civil discourse", "deliberative democracy", "bridging language", "inclusive language"],
            "civil discourse": ["deliberative democracy", "political civility", "democratic dialogue"],
            
            # Intergroup Relations Domain
            "intergroup relations": ["intergroup contact", "prejudice reduction", "contact hypothesis", "intergroup conflict"],
            "intergroup contact": ["contact hypothesis", "prejudice reduction", "intergroup relations"],
            
            # Political Communication Domain
            "political polarization": ["affective polarization", "negative partisanship", "partisan animosity"],
            "polarization": ["political polarization", "affective polarization", "partisan divide"],
            
            # Community Development Domain
            "community development": ["social capital", "collective efficacy", "community organizing", "civic engagement"],
            "civic engagement": ["political participation", "community involvement", "citizen engagement"]
        }
        
        expanded_terms = base_terms.copy()
        
        for term in base_terms:
            term_lower = term.lower()
            # Find semantic variants for each base term
            for key, variants in TERMINOLOGY_EXPANSIONS.items():
                if key in term_lower:
                    # Add variants that aren't already present
                    for variant in variants[:2]:  # Limit to 2 variants per term
                        if variant.lower() not in [t.lower() for t in expanded_terms]:
                            expanded_terms.append(variant)
        
        return expanded_terms
    
    def _intelligent_fallback_extraction(self, research_plan: str) -> List[str]:
        """Intelligent fallback: extract key concepts from research plan when JSON parsing fails"""
        # Common research keywords by domain (based on Issue #100 analysis)
        DOMAIN_KEYWORDS = {
            'social_cohesion': ['social cohesion', 'community bonds', 'social trust', 'collective efficacy'],
            'discourse_analysis': ['hostile discourse', 'cooperative discourse', 'civil discourse', 'political communication'],
            'intergroup_relations': ['intergroup contact', 'prejudice reduction', 'intergroup conflict', 'contact hypothesis'],
            'political_science': ['political polarization', 'partisan animosity', 'democratic dialogue', 'civic engagement'],
            'communication': ['deliberative democracy', 'political civility', 'inclusive language', 'bridging language']
        }
        
        research_lower = research_plan.lower()
        extracted_terms = []
        
        # Extract domain-specific terms that appear in the research plan
        for domain, keywords in DOMAIN_KEYWORDS.items():
            for keyword in keywords:
                if keyword in research_lower:
                    extracted_terms.append(keyword)
                    # Add semantic variants
                    if keyword == 'social cohesion':
                        extracted_terms.extend(['social capital', 'collective efficacy'])
                    elif keyword == 'hostile discourse':
                        extracted_terms.extend(['divisive language', 'incivility'])
                    elif keyword == 'cooperative discourse':
                        extracted_terms.extend(['civil discourse', 'deliberative democracy'])
        
        # If no domain-specific terms found, extract general academic concepts
        if not extracted_terms:
            academic_concepts = ['social', 'political', 'community', 'discourse', 'communication', 'research', 'analysis']
            for concept in academic_concepts:
                if concept in research_lower:
                    extracted_terms.append(f"{concept} research")
        
        # Add critical perspectives
        critical_terms = []
        for term in extracted_terms[:4]:  # Limit base terms
            critical_terms.extend([f"{term} criticism", f"{term} limitations"])
        
        extracted_terms.extend(critical_terms[:4])  # Limit critical terms
        
        # Ensure we have at least some terms
        if not extracted_terms:
            extracted_terms = ["discourse analysis", "social research", "communication studies", "research methodology"]
        
        return extracted_terms[:8]  # Limit to 8 terms
    
    def _extract_paper_references(self, papers: List[Dict]) -> List[str]:
        """Extract references and citations from discovered papers for network expansion"""
        reference_dois = []
        
        for paper in papers:
            # Extract DOI-based references from paper metadata
            if paper.get('references'):
                for ref in paper['references']:
                    if isinstance(ref, dict) and ref.get('doi'):
                        reference_dois.append(ref['doi'])
            
            # Extract cited-by information if available
            if paper.get('citedBy'):
                for citing_paper in paper['citedBy'][:5]:  # Limit to prevent explosion
                    if isinstance(citing_paper, dict) and citing_paper.get('doi'):
                        reference_dois.append(citing_paper['doi'])
        
        # Remove duplicates and return
        return list(set(reference_dois))
    
    def _crawl_citation_network(self, seed_papers: List[Dict], max_additional_papers: int = 10) -> List[Dict]:
        """Crawl citation networks from seed papers to discover additional relevant literature"""
        additional_papers = []
        processed_dois = {paper.get('doi') for paper in seed_papers if paper.get('doi')}
        
        # Extract reference DOIs from seed papers
        reference_dois = self._extract_paper_references(seed_papers)
        
        print(f"📚 Found {len(reference_dois)} potential references to explore")
        
        # Search for referenced papers (limited to prevent API overload)
        for doi in reference_dois[:max_additional_papers]:
            if doi and doi not in processed_dois:
                try:
                    # Search Semantic Scholar for papers by DOI
                    paper_data = self._search_by_doi(doi)
                    if paper_data and self._validate_paper_quality(paper_data):
                        additional_papers.append(paper_data)
                        processed_dois.add(doi)
                        print(f"📄 Added cited paper: {paper_data.get('title', 'Unknown')[:60]}...")
                    
                    # Rate limiting for citation crawling
                    time.sleep(1)  # Be extra respectful during network crawling
                    
                except Exception as e:
                    print(f"⚠️ Failed to fetch paper with DOI {doi}: {e}")
                    continue
        
        return additional_papers
    
    def _search_by_doi(self, doi: str) -> Optional[Dict]:
        """Search for a specific paper by DOI"""
        try:
            # Try Semantic Scholar first
            base_url = "https://api.semanticscholar.org/graph/v1/paper"
            url = f"{base_url}/{doi}"
            
            headers = {
                'User-Agent': 'Discernus-DiscernusLibrarian/1.0 (Academic Research Tool)',
            }
            
            params = {
                'fields': 'title,authors,year,abstract,doi,citationCount,url,venue'
            }
            
            response = requests.get(url, headers=headers, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'title': data.get('title', ''),
                    'authors': [author.get('name', '') for author in data.get('authors', [])],
                    'year': data.get('year'),
                    'abstract': data.get('abstract', ''),
                    'doi': data.get('doi', ''),
                    'citations': data.get('citationCount', 0),
                    'url': data.get('url', ''),
                    'venue': data.get('venue', {}),
                    'source': 'semantic_scholar_doi'
                }
            elif response.status_code == 429:
                print("⚠️ Rate limited during DOI search, backing off...")
                time.sleep(5)
                return None
            
        except requests.exceptions.RequestException as e:
            print(f"⚠️ DOI search failed: {e}")
        
        return None
    
    def _deduplicate_papers_by_doi(self, papers: List[Dict]) -> List[Dict]:
        """Remove duplicate papers using DOI comparison"""
        seen_dois = set()
        unique_papers = []
        
        for paper in papers:
            doi = paper.get('doi', '')
            title = paper.get('title', '').lower().strip()
            
            # Use DOI as primary identifier
            if doi and doi not in seen_dois:
                seen_dois.add(doi)
                unique_papers.append(paper)
            # Fallback to title-based deduplication if no DOI
            elif not doi and title and title not in seen_dois:
                seen_dois.add(title)
                unique_papers.append(paper)
        
        return unique_papers
    
    def _synthesize_research(self, question: str, papers: List[Dict], research_plan: str) -> str:
        """Phase 3: Synthesize findings with evidence-based confidence levels"""
        # First, analyze the quality and characteristics of the paper corpus
        corpus_analysis = self._analyze_corpus_quality(papers)
        
        # Detect systematic bias in corpus
        bias_analysis = self._detect_corpus_bias(papers, question)
        
        papers_text = "\n\n".join([
            f"**{paper.get('title', 'No title')}** ({paper.get('year', 'No year')}) by {', '.join((paper.get('authors', []) or [])[:3])}\n"
            f"DOI: {paper.get('doi', 'No DOI')}\nSource: {paper.get('source', 'unknown')}\nQuality Score: {paper.get('quality_score', 'N/A')}/5\n"
            f"Citation Count: {paper.get('citation_count', 'N/A')}\n"
            f"Abstract: {(paper.get('abstract') or 'No abstract available')[:300]}..."
            for paper in papers[:10]  # Limit to 10 papers for context size
        ])
        
        prompt = f"""You are synthesizing academic research with rigorous, evidence-based confidence levels.

Research Question: {question}

Research Plan: {research_plan}

CORPUS ANALYSIS:
{corpus_analysis}

BIAS ANALYSIS:
{bias_analysis}

Available Literature:
{papers_text}

Create a comprehensive research synthesis using this EVIDENCE-BASED CONFIDENCE SYSTEM:

**CONFIDENCE CRITERIA:**
- HIGH (Score 7-10): 
  * 5+ peer-reviewed papers supporting claim
  * Consistent findings across multiple studies
  * Large sample sizes (>1000 citations/papers analyzed)
  * Recent research (within 5 years)
  * Replicated findings

- MEDIUM (Score 4-6):
  * 2-4 papers supporting claim
  * Some consistency but minor variations
  * Moderate sample sizes (100-1000)
  * Mix of recent and older research
  * Limited replication

- LOW (Score 1-3):
  * 1-2 papers supporting claim
  * Preliminary findings or single study
  * Small sample sizes (<100)
  * Mostly preprints or older research
  * No replication evidence

**REQUIRED FORMAT:**
For each major claim, provide:
1. The claim statement
2. Confidence level (HIGH/MEDIUM/LOW) with numerical score (1-10)
3. Specific evidence justification including:
   - Number of supporting papers in our corpus
   - Quality of sources (peer-reviewed vs preprints)
   - Sample sizes mentioned in studies
   - Consistency of findings
   - Publication years
   - Limitations affecting confidence

Address these areas:
1. **Key Findings**: What does the literature say about this question?
2. **Methodological Approaches**: What methods are being used?
3. **Consensus Areas**: Where do researchers agree?
4. **Debate Areas**: What are the open questions or disagreements?
5. **Knowledge Gaps**: What's missing from current research?
6. **Methodological Recommendations**: Based on evidence, how should researchers proceed?

Be rigorous - err on the side of lower confidence if evidence is thin. Explicitly cite paper titles and DOIs for claims."""

        response, metadata = self.gateway.execute_call(
            model=self.synthesis_model,
            prompt=prompt,
            system_prompt="You are synthesizing academic research with rigorous, evidence-based confidence levels."
        )
        return response

    def _analyze_corpus_quality(self, papers: List[Dict]) -> str:
        """Analyze the quality and characteristics of the paper corpus"""
        total_papers = len(papers)
        
        # Analyze sources
        source_counts = {}
        for paper in papers:
            source = paper.get('source', 'unknown')
            source_counts[source] = source_counts.get(source, 0) + 1
        
        # Analyze years
        years = [paper.get('year') for paper in papers if paper.get('year')]
        recent_papers = sum(1 for year in years if year and year >= 2020)
        
        # Analyze quality scores
        quality_scores = [paper.get('quality_score', 0) for paper in papers]
        avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0
        high_quality_papers = sum(1 for score in quality_scores if score >= 4)
        
        # Analyze abstracts
        papers_with_abstracts = sum(1 for paper in papers if paper.get('abstract') and len(paper['abstract']) > 100)
        
        # Analyze DOIs (proxy for peer-review status)
        peer_reviewed_likely = sum(1 for paper in papers if paper.get('doi') and '10.' in paper.get('doi', ''))
        
        # Analyze citation counts
        citation_counts = [paper.get('citation_count') for paper in papers if paper.get('citation_count') is not None]
        avg_citations = sum(citation_counts) / len(citation_counts) if citation_counts else 0
        
        analysis = f"""
CORPUS QUALITY ANALYSIS:
- Total papers: {total_papers}
- Sources: {dict(source_counts)}
- Recent papers (2020+): {recent_papers}/{total_papers} ({recent_papers/total_papers*100:.1f}%)
- Average quality score: {avg_quality:.1f}/5
- High quality papers (4+/5): {high_quality_papers}/{total_papers} ({high_quality_papers/total_papers*100:.1f}%)
- Papers with substantial abstracts: {papers_with_abstracts}/{total_papers} ({papers_with_abstracts/total_papers*100:.1f}%)
- Likely peer-reviewed (DOI format): {peer_reviewed_likely}/{total_papers} ({peer_reviewed_likely/total_papers*100:.1f}%)
- Average citation count: {avg_citations:.1f} (from {len(citation_counts)} papers with data)

CONFIDENCE IMPLICATIONS:
- Small corpus size ({total_papers} papers) limits generalizability
- Mixed source quality affects reliability of claims
- {'Strong' if avg_quality >= 4 else 'Moderate' if avg_quality >= 3 else 'Weak'} average quality ({avg_quality:.1f}/5)
- {'Recent' if recent_papers/total_papers > 0.6 else 'Mixed age'} literature base
- {'High' if avg_citations > 50 else 'Moderate' if avg_citations > 10 else 'Low'} impact corpus (avg {avg_citations:.1f} citations)
- Maximum confidence levels should be capped due to corpus limitations
        """
        
        return analysis
    
    def _detect_corpus_bias(self, papers: List[Dict], question: str) -> str:
        """Systematic bias detection in literature corpus"""
        if not papers:
            return "No papers available for bias analysis."
        
        bias_analysis = []
        
        # 1. Publication Bias Analysis
        pub_bias = self._analyze_publication_bias(papers)
        bias_analysis.append(f"**Publication Bias:** {pub_bias}")
        
        # 2. Temporal Bias Analysis
        temporal_bias = self._analyze_temporal_bias(papers)
        bias_analysis.append(f"**Temporal Bias:** {temporal_bias}")
        
        # 3. Geographical/Institutional Bias
        geo_bias = self._analyze_geographical_bias(papers)
        bias_analysis.append(f"**Geographical Bias:** {geo_bias}")
        
        # 4. Citation Bias Analysis
        citation_bias = self._analyze_citation_bias(papers)
        bias_analysis.append(f"**Citation Bias:** {citation_bias}")
        
        # 5. Methodological Bias
        method_bias = self._analyze_methodological_bias(papers)
        bias_analysis.append(f"**Methodological Bias:** {method_bias}")
        
        # 6. Selection Bias in Search Terms
        selection_bias = self._analyze_selection_bias(papers)
        bias_analysis.append(f"**Selection Bias:** {selection_bias}")
        
        # 7. Language/Cultural Bias
        lang_bias = self._analyze_language_bias(papers)
        bias_analysis.append(f"**Language/Cultural Bias:** {lang_bias}")
        
        # 8. Overall Bias Assessment
        overall_bias = self._assess_overall_bias(papers, question)
        bias_analysis.append(f"**Overall Bias Assessment:** {overall_bias}")
        
        return "\n\n".join(bias_analysis)
    
    def _analyze_publication_bias(self, papers: List[Dict]) -> str:
        """Analyze publication bias - skew toward positive results"""
        if not papers:
            return "No papers to analyze."
        
        # Check for positive/negative sentiment in titles and abstracts
        positive_indicators = ['improve', 'benefit', 'success', 'effective', 'advantage', 'positive', 'enhance', 'significant']
        negative_indicators = ['fail', 'negative', 'problem', 'limitation', 'challenge', 'ineffective', 'harmful', 'bias']
        
        positive_count = 0
        negative_count = 0
        
        for paper in papers:
            title = (paper.get('title') or '').lower()
            abstract = (paper.get('abstract') or '').lower()
            text = f"{title} {abstract}"
            
            if any(indicator in text for indicator in positive_indicators):
                positive_count += 1
            if any(indicator in text for indicator in negative_indicators):
                negative_count += 1
        
        if positive_count + negative_count == 0:
            return "Unable to detect clear positive/negative trends in corpus."
        
        positive_ratio = positive_count / (positive_count + negative_count)
        
        if positive_ratio > 0.75:
            return f"HIGH RISK - Strong positive bias detected ({positive_count} positive vs {negative_count} negative papers). May be missing critical studies, negative results, or failure cases."
        elif positive_ratio > 0.6:
            return f"MODERATE RISK - Positive bias detected ({positive_count} positive vs {negative_count} negative papers). Consider seeking more critical perspectives."
        else:
            return f"LOW RISK - Balanced perspective detected ({positive_count} positive vs {negative_count} negative papers)."
    
    def _analyze_temporal_bias(self, papers: List[Dict]) -> str:
        """Analyze temporal bias in publication dates"""
        years = [p.get('year') for p in papers if p.get('year')]
        if len(years) < 3:
            return "Insufficient temporal data for bias analysis."
        
        current_year = datetime.now().year
        recent_papers = sum(1 for year in years if year >= current_year - 5)
        older_papers = len(years) - recent_papers
        
        recent_ratio = recent_papers / len(years)
        
        if recent_ratio > 0.8:
            return f"HIGH RISK - Strong recency bias ({recent_papers} recent vs {older_papers} older papers). May be missing established foundational research or long-term studies."
        elif recent_ratio > 0.6:
            return f"MODERATE RISK - Some recency bias ({recent_papers} recent vs {older_papers} older papers). Consider including more historical context."
        else:
            return f"LOW RISK - Good temporal balance ({recent_papers} recent vs {older_papers} older papers)."
    
    def _analyze_geographical_bias(self, papers: List[Dict]) -> str:
        """Analyze geographical and institutional bias"""
        # Check for geographical indicators in author affiliations, DOIs, or abstracts
        western_indicators = ['university', 'stanford', 'mit', 'harvard', 'oxford', 'cambridge', 'europe', 'usa', 'america']
        global_indicators = ['china', 'japan', 'india', 'brazil', 'africa', 'asia', 'international', 'global']
        
        western_count = 0
        global_count = 0
        
        for paper in papers:
            text = f"{paper.get('title') or ''} {paper.get('abstract') or ''} {paper.get('doi') or ''}".lower()
            
            if any(indicator in text for indicator in western_indicators):
                western_count += 1
            if any(indicator in text for indicator in global_indicators):
                global_count += 1
        
        total_with_geo = western_count + global_count
        if total_with_geo == 0:
            return "Unable to detect geographical patterns in corpus."
        
        western_ratio = western_count / total_with_geo
        
        if western_ratio > 0.8:
            return f"HIGH RISK - Strong Western bias detected ({western_count} Western vs {global_count} global papers). May be missing non-Western perspectives and contexts."
        elif western_ratio > 0.6:
            return f"MODERATE RISK - Some Western bias ({western_count} Western vs {global_count} global papers). Consider seeking more diverse geographical perspectives."
        else:
            return f"LOW RISK - Good geographical balance ({western_count} Western vs {global_count} global papers)."
    
    def _analyze_citation_bias(self, papers: List[Dict]) -> str:
        """Analyze citation patterns for self-reinforcing bias"""
        citations = [p.get('citation_count', 0) for p in papers if p.get('citation_count')]
        if len(citations) < 5:
            return "Insufficient citation data for bias analysis."
        
        # Check for extreme citation concentration
        citations.sort(reverse=True)
        top_20_percent = int(len(citations) * 0.2) or 1
        top_citations = sum(citations[:top_20_percent])
        total_citations = sum(citations)
        
        if total_citations == 0:
            return "No citation data available for bias analysis."
        
        concentration_ratio = top_citations / total_citations
        
        if concentration_ratio > 0.8:
            return f"HIGH RISK - Extreme citation concentration ({concentration_ratio:.1%} of citations in top 20% of papers). May be missing important but less-cited work."
        elif concentration_ratio > 0.6:
            return f"MODERATE RISK - High citation concentration ({concentration_ratio:.1%} of citations in top 20% of papers). Consider including more diverse citation patterns."
        else:
            return f"LOW RISK - Good citation distribution ({concentration_ratio:.1%} of citations in top 20% of papers)."
    
    def _analyze_methodological_bias(self, papers: List[Dict]) -> str:
        """Analyze methodological bias in research approaches"""
        method_indicators = {
            'quantitative': ['survey', 'experiment', 'statistical', 'regression', 'correlation', 'sample', 'n='],
            'qualitative': ['interview', 'ethnography', 'case study', 'narrative', 'phenomenology', 'grounded theory'],
            'theoretical': ['theory', 'framework', 'model', 'conceptual', 'literature review'],
            'computational': ['algorithm', 'machine learning', 'neural network', 'artificial intelligence', 'deep learning']
        }
        
        method_counts = {method: 0 for method in method_indicators}
        
        for paper in papers:
            text = f"{paper.get('title') or ''} {paper.get('abstract') or ''}".lower()
            
            for method, indicators in method_indicators.items():
                if any(indicator in text for indicator in indicators):
                    method_counts[method] += 1
        
        total_methods = sum(method_counts.values())
        if total_methods == 0:
            return "Unable to detect methodological patterns in corpus."
        
        # Check for extreme concentration in one method
        max_method = max(method_counts, key=method_counts.get)
        max_ratio = method_counts[max_method] / total_methods
        
        if max_ratio > 0.8:
            return f"HIGH RISK - Extreme methodological bias toward {max_method} approaches ({method_counts[max_method]}/{total_methods} papers). May be missing important alternative methodologies."
        elif max_ratio > 0.6:
            return f"MODERATE RISK - Some methodological bias toward {max_method} approaches ({method_counts[max_method]}/{total_methods} papers). Consider more methodological diversity."
        else:
            return f"LOW RISK - Good methodological balance across approaches: {dict(method_counts)}"
    
    def _analyze_selection_bias(self, papers: List[Dict]) -> str:
        """Analyze selection bias in search terms and corpus construction"""
        search_terms = set()
        for paper in papers:
            term = paper.get('search_term', '')
            if term:
                search_terms.add(term.lower())
        
        if len(search_terms) < 2:
            return "HIGH RISK - Very limited search terms used. High likelihood of selection bias."
        
        # Check for critical vs supportive search terms
        critical_terms = sum(1 for term in search_terms if any(word in term for word in ['limitation', 'bias', 'problem', 'fail', 'critic']))
        supportive_terms = len(search_terms) - critical_terms
        
        if critical_terms == 0:
            return f"HIGH RISK - No critical search terms used ({len(search_terms)} total terms). Strong selection bias toward supportive literature."
        elif critical_terms < supportive_terms * 0.3:
            return f"MODERATE RISK - Few critical search terms ({critical_terms} critical vs {supportive_terms} supportive). Some selection bias likely."
        else:
            return f"LOW RISK - Good balance of critical and supportive search terms ({critical_terms} critical vs {supportive_terms} supportive)."
    
    def _analyze_language_bias(self, papers: List[Dict]) -> str:
        """Analyze language and cultural bias"""
        # Most academic databases are English-dominant, so this is a known limitation
        non_english_indicators = ['chinese', 'japanese', 'spanish', 'portuguese', 'french', 'german', 'russian', 'arabic']
        
        non_english_count = 0
        for paper in papers:
            text = f"{paper.get('title') or ''} {paper.get('abstract') or ''}".lower()
            if any(indicator in text for indicator in non_english_indicators):
                non_english_count += 1
        
        english_ratio = (len(papers) - non_english_count) / len(papers) if papers else 0
        
        if english_ratio > 0.95:
            return f"HIGH RISK - Strong English-language bias ({english_ratio:.1%} English sources). Missing important non-English research and cultural perspectives."
        elif english_ratio > 0.85:
            return f"MODERATE RISK - Some English-language bias ({english_ratio:.1%} English sources). Consider seeking more diverse linguistic perspectives."
        else:
            return f"LOW RISK - Good linguistic diversity ({english_ratio:.1%} English sources)."
    
    def _assess_overall_bias(self, papers: List[Dict], question: str) -> str:
        """Provide overall bias assessment and recommendations"""
        total_papers = len(papers)
        
        if total_papers < 5:
            return "CRITICAL - Very small corpus size increases all bias risks. Findings should be treated as preliminary exploration only."
        elif total_papers < 15:
            return "HIGH RISK - Small corpus size amplifies bias effects. Results should be interpreted with significant caution and additional research is needed."
        elif total_papers < 30:
            return "MODERATE RISK - Limited corpus size may hide important perspectives. Consider expanding search strategy for more comprehensive coverage."
        else:
            return "LOW RISK - Reasonable corpus size for exploratory research, though larger systematic reviews would strengthen conclusions."
    
    def _red_team_critique(self, synthesis: str, question: str) -> str:
        """Phase 4: Adversarial quality control with premium model"""
        prompt = f"""You are a cranky, adversarial academic reviewer. Your job is to find every flaw, bias, and weakness in this research synthesis.

Original Question: {question}

Research Synthesis to Attack:
{synthesis}

Tear this apart systematically:

1. **Literature Coverage**: What important papers or perspectives are missing?
2. **Methodological Flaws**: Are the confidence levels justified? Are claims overstated?
3. **Citation Bias**: Is this cherry-picking evidence? What about contrary findings?
4. **Logical Gaps**: Where does the reasoning break down?
5. **Assumption Problems**: What unstated assumptions are being made?
6. **Generalizability Issues**: Are conclusions over-generalized from limited evidence?
7. **Research Design Critiques**: Are the methodological recommendations sound?

Be harsh but constructive. Point out specific weaknesses and suggest improvements.
Your goal is to make this research synthesis more robust and honest."""

        response, metadata = self.gateway.execute_call(
            model=self.critique_model,  # Use premium model for sophisticated critique
            prompt=prompt,
            system_prompt="You are a cranky, adversarial academic reviewer."
        )
        return response
    
    def _final_synthesis(self, synthesis: str, critique: str, question: str) -> str:
        """Phase 5: Respond to critique and provide final research guidance"""
        prompt = f"""You are responding to peer review and improving your research synthesis.

Original Question: {question}

Your Original Synthesis:
{synthesis}

Reviewer's Critique:
{critique}

Provide an improved final synthesis that:

1. **Addresses Valid Critiques**: Fix legitimate problems identified by the reviewer
2. **Defends Sound Conclusions**: Explain why some critiques may be unfair or incorrect
3. **Adds Missing Perspectives**: Include important viewpoints that were overlooked
4. **Refines Confidence Levels**: Adjust confidence assessments based on critique
5. **Enhanced Methodology**: Provide better methodological recommendations
6. **Research Agenda**: Suggest specific next steps for researchers
7. **Limitations Acknowledgment**: Be explicit about what this review cannot conclude

Make this a robust, honest assessment that acknowledges uncertainty while providing clear guidance.
Include explicit confidence levels and cite the DOIs of key papers."""

        response, metadata = self.gateway.execute_call(
            model=self.research_model,  # Back to ultra-cheap model for final synthesis
            prompt=prompt,
            system_prompt="You are responding to peer review and improving your research synthesis."
        )
        return response

def main():
    """Test the DiscernusLibrarian with a sample research question"""
    librarian = DiscernusLibrarian()
    
    # Test question about our DiscernusLibrarian system itself!
    test_question = "How do citation networks influence academic research discovery and what are the most effective computational methods for analyzing them?"
    
    print("🧪 Testing DiscernusLibrarian with citation networks research question...")
    result = librarian.research_question(test_question)
    
    print("\n" + "="*80)
    print("DISCERNUSLIBRARIAN RESEARCH REPORT")
    print("="*80)
    print(f"Question: {result['question']}")
    print(f"Papers Found: {result['papers_found']}")
    print(f"Timestamp: {result['timestamp']}")
    print(f"Cost Optimization: {result['cost_optimization']}")
    
    print(f"\n🎯 FINAL RESEARCH SYNTHESIS:")
    print(result['final_response'])
    
    return result

if __name__ == "__main__":
    main() 