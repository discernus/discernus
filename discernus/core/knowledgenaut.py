#!/usr/bin/env python3
"""
Knowledgenaut: Citation-Guided Research Agent
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
from discernus.core.ultra_thin_llm_client import UltraThinLLMClient as ThinLiteLLMClient

class UltraThinKnowledgenaut:
    """
    THIN research agent - LLMs do the thinking, we just route messages
    Cost-optimized with ultra-cheap Vertex AI Gemini 2.5 Flash
    """
    
    def __init__(self):
        # Set up Vertex AI environment for ultra-cheap pricing
        os.environ['VERTEXAI_PROJECT'] = 'gen-lang-client-0199646265'
        os.environ['VERTEXAI_LOCATION'] = 'us-central1'
        
        self.client = ThinLiteLLMClient()
        
        # Model selection for cost optimization
        self.research_model = "vertex_ai/gemini-2.5-flash"  # Ultra-cheap: $0.13/$0.38 per 1M tokens
        self.synthesis_model = "vertex_ai/gemini-2.5-flash"  # Same model for consistency
        self.critique_model = "claude-3-5-sonnet-20241022"   # Premium model for red team critique
        
        print("🧭 Knowledgenaut initialized with ultra-cheap Vertex AI")
        print(f"💰 Research cost: $0.13/$0.38 per 1M tokens (Gemini 2.5 Flash)")
    
    def research_question(self, question: str, save_results: bool = True) -> Dict[str, Any]:
        """
        Main research workflow: Question → Literature Discovery → Synthesis → Critique
        """
        print(f"\n🔍 Research Question: {question}")
        
        # Phase 1: Research Planning (ultra-cheap model)
        print("📋 Phase 1: Research Planning...")
        research_plan = self._plan_research(question)
        
        # Phase 2: Literature Discovery via CrossRef
        print("📚 Phase 2: Literature Discovery...")
        papers = self._discover_literature(question, research_plan)
        
        # Phase 3: Research Synthesis (ultra-cheap model)
        print("🔬 Phase 3: Research Synthesis...")
        synthesis = self._synthesize_research(question, papers, research_plan)
        
        # Phase 4: Red Team Critique (premium model for quality)
        print("🥊 Phase 4: Red Team Critique...")
        critique = self._red_team_critique(synthesis, question)
        
        # Phase 5: Final Response (ultra-cheap model)
        print("🎯 Phase 5: Final Synthesis...")
        final_response = self._final_synthesis(synthesis, critique, question)
        
        result = {
            'question': question,
            'research_plan': research_plan,
            'papers_found': len(papers),
            'papers': papers,
            'synthesis': synthesis,
            'critique': critique,
            'final_response': final_response,
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'cost_optimization': 'Ultra-cheap Vertex AI for research, premium model for critique'
        }
        
        # Save results to file
        if save_results:
            self._save_results(result)
        
        return result
    
    def _save_results(self, result: Dict[str, Any]):
        """Save research results to timestamped file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"knowledgenaut_research_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"💾 Results saved to: {filename}")
            
            # Also create a readable markdown report
            md_filename = f"knowledgenaut_report_{timestamp}.md"
            self._create_markdown_report(result, md_filename)
            print(f"📄 Readable report saved to: {md_filename}")
            
        except Exception as e:
            print(f"⚠️ Failed to save results: {e}")
    
    def _create_markdown_report(self, result: Dict[str, Any], filename: str):
        """Create a human-readable markdown report"""
        report = f"""# Knowledgenaut Research Report

**Research Question:** {result['question']}
**Timestamp:** {result['timestamp']}
**Papers Found:** {result['papers_found']}
**Cost Optimization:** {result['cost_optimization']}

---

## 🧠 Research Plan

{result['research_plan']}

---

## 📚 Literature Found ({result['papers_found']} papers)

"""
        
        for i, paper in enumerate(result.get('papers', [])[:10], 1):
            report += f"""
### {i}. {paper.get('title', 'No title')}

- **Authors:** {', '.join(paper.get('authors', [])[:3])}
- **Year:** {paper.get('year', 'Unknown')}
- **DOI:** {paper.get('doi', 'No DOI')}
- **Search Term:** {paper.get('search_term', 'Unknown')}

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

*Generated by Ultra-THIN Knowledgenaut with Vertex AI Gemini 2.5 Flash*
"""
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(report)
        except Exception as e:
            print(f"⚠️ Failed to create markdown report: {e}")

    def _plan_research(self, question: str) -> str:
        """Phase 1: Let LLM plan the research approach"""
        prompt = f"""You are a research librarian planning a comprehensive literature review.

Research Question: {question}

Create a focused research plan that includes:
1. Key concepts and terms to search for
2. Likely academic disciplines involved  
3. Important authors or seminal papers to look for
4. Search strategy for maximum literature coverage

Be specific and actionable. Focus on findable, citable academic sources."""

        return self.client.call_llm_with_vertex_support(
            model=self.research_model,
            messages=[{"role": "user", "content": prompt}]
        )
    
    def _discover_literature(self, question: str, research_plan: str) -> List[Dict[str, Any]]:
        """Phase 2: Enhanced multi-API literature discovery with validation"""
        # Extract search terms from research plan using LLM
        search_terms = self._extract_search_terms(research_plan)
        
        papers = []
        sources_tried = []
        
        # Try multiple APIs for better coverage - expanded for critical perspectives
        for term in search_terms[:5]:  # Limit to 5 terms for cost control (increased for critical perspectives)
            term_papers = []
            
            # 1. Try Semantic Scholar first (often better abstracts)
            try:
                semantic_papers = self._search_semantic_scholar(term)
                term_papers.extend(semantic_papers)
                sources_tried.append(f"Semantic Scholar: {len(semantic_papers)} papers for '{term}'")
                time.sleep(0.5)  # Be respectful to API rate limits
            except Exception as e:
                print(f"⚠️ Semantic Scholar search failed for '{term}': {e}")
            
            # 2. Try CrossRef if we need more papers
            if len(term_papers) < 5:
                try:
                    crossref_papers = self._search_crossref(term)
                    term_papers.extend(crossref_papers)
                    sources_tried.append(f"CrossRef: {len(crossref_papers)} papers for '{term}'")
                    time.sleep(0.5)  # Be respectful to API rate limits
                except Exception as e:
                    print(f"⚠️ CrossRef search failed for '{term}': {e}")
            
            # 3. Try arXiv for cutting-edge research
            try:
                arxiv_papers = self._search_arxiv(term)
                term_papers.extend(arxiv_papers)
                sources_tried.append(f"arXiv: {len(arxiv_papers)} papers for '{term}'")
                time.sleep(0.5)  # Be respectful to API rate limits
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
        
        print(f"📚 Literature Discovery Results:")
        for source in sources_tried:
            print(f"  - {source}")
        print(f"📚 Total: {len(papers)} papers found, {len(unique_papers)} unique, {len(validated_papers)} validated")
        
        return validated_papers
    
    def _search_semantic_scholar(self, term: str) -> List[Dict[str, Any]]:
        """Search Semantic Scholar API for papers"""
        papers = []
        try:
            url = "https://api.semanticscholar.org/graph/v1/paper/search"
            params = {
                'query': term,
                'limit': 5,
                'fields': 'paperId,title,authors,year,abstract,openAccessPdf,citationCount'
            }
            
            # Add user-agent header for better API compatibility
            headers = {
                'User-Agent': 'Knowledgenaut/1.0 (research tool)'
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=10)
            print(f"Semantic Scholar API response status: {response.status_code}")
            
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
            else:
                print(f"Semantic Scholar API error: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Semantic Scholar error for '{term}': {e}")
        
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
        """Extract diverse search terms including critical perspectives"""
        prompt = f"""Extract 6-8 specific academic search terms from this research plan that include BOTH supportive and critical perspectives:

{research_plan}

Include terms that would find:
1. Core/supportive research (2-3 terms)
2. Critical perspectives and limitations (2-3 terms) 
3. Failed approaches or negative results (1-2 terms)

Return ONLY a JSON list of search terms, like: ["term 1", "term 2", "term 3", "criticism of term 1", "limitations of term 2", "bias in term 3"]
Use precise academic terminology that would work well in academic database searches."""

        response = self.client.call_llm_with_vertex_support(
            model=self.research_model,
            messages=[{"role": "user", "content": prompt}]
        )
        
        try:
            # Parse JSON response
            terms = json.loads(response.strip())
            # Add critical search terms if not present
            critical_terms = self._add_critical_search_terms(terms if isinstance(terms, list) else [])
            return critical_terms[:8]  # Limit to 8 terms to control costs
        except:
            # Fallback with both supportive and critical terms
            return ["citation networks", "bibliometrics", "citation analysis limitations", "citation bias", "academic research"]

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

        return self.client.call_llm_with_vertex_support(
            model=self.synthesis_model,
            messages=[{"role": "user", "content": prompt}]
        )

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

        return self.client.call_llm_with_vertex_support(
            model=self.critique_model,  # Use premium model for sophisticated critique
            messages=[{"role": "user", "content": prompt}]
        )
    
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

        return self.client.call_llm_with_vertex_support(
            model=self.research_model,  # Back to ultra-cheap model for final synthesis
            messages=[{"role": "user", "content": prompt}]
        )

def main():
    """Test the knowledgenaut with a sample research question"""
    knowledgenaut = UltraThinKnowledgenaut()
    
    # Test question about our knowledgenaut system itself!
    test_question = "How do citation networks influence academic research discovery and what are the most effective computational methods for analyzing them?"
    
    print("🧪 Testing knowledgenaut with citation networks research question...")
    result = knowledgenaut.research_question(test_question)
    
    print("\n" + "="*80)
    print("KNOWLEDGENAUT RESEARCH REPORT")
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