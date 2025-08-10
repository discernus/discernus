#!/usr/bin/env python3
"""
ThinResultsInterpreterAgent
===========================

THIN agent that generates an evidence-grounded report in two LLM calls:
- Call 1: Claims selection (JSON-only) bound to experiment hypotheses
- Call 2: Report generation (Markdown) using retrieved evidence snippets

All prompt content is externalized in YAML under ./prompts/
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple
from pathlib import Path
import json
import logging

from ...txtai_evidence_curator.agent import TxtaiEvidenceCurator  # type: ignore
from ...txtai_evidence_curator.agent import EvidenceQuery  # type: ignore
from discernus.gateway.model_registry import ModelRegistry
from discernus.gateway.llm_gateway import LLMGateway


@dataclass
class ThinInterpretationResponse:
    success: bool
    full_report: str
    scanner_section: str
    collaborator_section: str
    transparency_section: str
    evidence_queries_used: int
    word_count: int
    error_message: str = ""


class ThinResultsInterpreterAgent:
    def __init__(self, model: str, audit_logger=None):
        self.model = model
        self.model_registry = ModelRegistry()
        self.llm_gateway = LLMGateway(self.model_registry)
        self.logger = logging.getLogger(__name__)
        self.audit_logger = audit_logger

        # Prompts directory alongside this file
        self.prompts_dir = Path(__file__).parent / "prompts"

    # -------------------- Public API --------------------
    def interpret_results(self, request) -> ThinInterpretationResponse:
        try:
            claims = self._select_claims(request)
            evidence_map, queries_used, evidence_catalog = self._retrieve_evidence(request.txtai_curator, claims)
            report = self._generate_report(request, claims, evidence_map, evidence_catalog)

            # Basic sections split (first H2 as scanner, rest as collaborator; transparency appended)
            scanner_section, collaborator_section, transparency_section = self._split_sections(report)

            return ThinInterpretationResponse(
                success=True,
                full_report=report,
                scanner_section=scanner_section,
                collaborator_section=collaborator_section,
                transparency_section=transparency_section,
                evidence_queries_used=queries_used,
                word_count=len(report.split()),
            )
        except Exception as e:
            self.logger.error(f"Thin interpreter failed: {e}")
            return ThinInterpretationResponse(
                success=False,
                full_report="",
                scanner_section="",
                collaborator_section="",
                transparency_section="",
                evidence_queries_used=0,
                word_count=0,
                error_message=str(e),
            )

    # -------------------- Internal methods --------------------
    def _select_claims(self, request) -> List[Dict[str, Any]]:
        """LLM call 1: Select interpretive claims bounded to hypotheses; JSON-only."""
        prompt_cfg = self._load_yaml("claims_selector.yaml")
        system_prompt = prompt_cfg.get("system", "You are a careful research assistant.")
        template = prompt_cfg.get("template", "")

        payload = {
            "statistical_results_json": self._safe_json(request.statistical_results),
            "experiment_context": request.experiment_context or "",
            "framework_spec": request.framework_spec or "",
        }
        rendered = self._render_template(template, payload)

        content, meta = self.llm_gateway.execute_call(
            model=self.model,
            system_prompt=system_prompt,
            prompt=rendered,
            temperature=0.2,
        )

        # Expect strict JSON list with robust recovery from fences or extra text
        claims = self._parse_json_list(content)
        if claims is not None:
            return claims

        # Minimal deterministic fallback: derive 1-3 claims from statistical_results
        try:
            sr = json.loads(payload["statistical_results_json"]) or {}
        except Exception:
            sr = {}
        auto_claims: List[Dict[str, Any]] = []
        for i, (k, v) in enumerate(list(sr.items())[:3]):
            auto_claims.append({
                "id": f"auto_{i+1}",
                "hypothesis": None,
                "testable": True,
                "dimension": k.split("_")[0] if isinstance(k, str) else None,
                "speaker": None,
                "result_key": k,
                "rationale": "Auto-selected claim for thin fallback due to JSON parse failure",
                "query_terms": [str(k)],
                "priority": 2,
            })
        return auto_claims

    def _retrieve_evidence(self, txtai_curator: Optional[TxtaiEvidenceCurator], claims: List[Dict[str, Any]]):
        """Deterministic txtai retrieval based on claim-suggested queries.

        Returns: (evidence_map, queries_used, evidence_catalog)
        - evidence_map: {claim_id: [catalog_ids...]}
        - evidence_catalog: {catalog_id: evidence_dict}
        """
        if not txtai_curator or not getattr(txtai_curator, "index_built", False):
            return {}, 0, {}

        evidence_map: Dict[str, List[str]] = {}
        evidence_catalog: Dict[str, Dict[str, Any]] = {}
        queries_used = 0
        next_id = 1

        for idx, claim in enumerate(claims):
            result_key = claim.get("id") or f"claim_{idx+1}"
            terms = claim.get("query_terms") or []
            try:
                # Build two queries: primary terms and a supplemental with dimension/speaker
                query_list: List[EvidenceQuery] = []
                # EvidenceQuery signature: document_name, dimension, speaker, semantic_query, limit
                if isinstance(terms, list) and terms:
                    query_list.append(EvidenceQuery(semantic_query=" ".join(terms), limit=3))
                dim = claim.get("dimension")
                spk = claim.get("speaker")
                if dim or spk:
                    query_list.append(EvidenceQuery(dimension=dim, speaker=spk, limit=2))

                pieces_objs = []
                for q in query_list:
                    res = txtai_curator._query_evidence(q) or []  # List[EvidenceResult]
                    if res:
                        pieces_objs.extend(res)

                # Rank by txtai score (desc), then confidence (desc), then length (desc)
                def _to_dict(ev) -> Dict[str, Any]:
                    # EvidenceResult or dict
                    if hasattr(ev, 'quote_text'):
                        return {
                            "document_id": getattr(ev, 'document_name', None) or getattr(ev, 'document_id', None) or "unknown",
                            "dimension": getattr(ev, 'dimension', None) or "unknown",
                            "quote": getattr(ev, 'quote_text', None) or getattr(ev, 'text', '') or '',
                            "confidence": getattr(ev, 'confidence', 0.0),
                            "score": getattr(ev, 'score', 0.0),
                            "start": getattr(ev, 'metadata', {}).get('start') if getattr(ev, 'metadata', None) else None,
                            "end": getattr(ev, 'metadata', {}).get('end') if getattr(ev, 'metadata', None) else None,
                        }
                    # dict fallback
                    return {
                        "document_id": ev.get("document_id") or ev.get("doc_id") or "unknown",
                        "dimension": ev.get("dimension") or ev.get("label") or "unknown",
                        "quote": ev.get("quote") or ev.get("quote_text") or ev.get("text") or "",
                        "confidence": ev.get("confidence", 0.0),
                        "score": ev.get("score", 0.0),
                        "start": ev.get("start"),
                        "end": ev.get("end"),
                    }

                ranked: List[Dict[str, Any]] = []
                for ev in pieces_objs:
                    ranked.append(_to_dict(ev))
                ranked.sort(key=lambda r: (r.get('score', 0.0), r.get('confidence', 0.0), len(r.get('quote', ''))), reverse=True)

                # Ensure diversity by document_id; select 2–3 per claim
                seen_docs = set()
                selected: List[Dict[str, Any]] = []
                for r in ranked:
                    if not r.get('quote'):
                        continue
                    doc = r.get('document_id')
                    if doc in seen_docs:
                        continue
                    seen_docs.add(doc)
                    selected.append(r)
                    if len(selected) >= 3:
                        break

                # If less than 2, relax diversity constraint
                if len(selected) < 2:
                    for r in ranked:
                        if not r.get('quote'):
                            continue
                        if r not in selected:
                            selected.append(r)
                        if len(selected) >= 2:
                            break

                # Assign catalog IDs and map to claim
                if selected:
                    ids_for_claim: List[str] = []
                    for r in selected:
                        eid = f"E{next_id}"
                        next_id += 1
                        evidence_catalog[eid] = r
                        ids_for_claim.append(eid)
                    evidence_map[result_key] = ids_for_claim
                    queries_used += len(query_list)
            except Exception as e:
                self.logger.warning(f"Evidence retrieval failed for {result_key}: {e}")
        return evidence_map, queries_used, evidence_catalog

    def _generate_report(self, request, claims: List[Dict[str, Any]], evidence_map: Dict[str, List[str]], evidence_catalog: Dict[str, Dict[str, Any]]) -> str:
        prompt_cfg = self._load_yaml("report_generator.yaml")
        system_prompt = prompt_cfg.get("system", "You are a careful research assistant.")
        template = prompt_cfg.get("template", "")

        payload = {
            "statistical_results_json": self._safe_json(request.statistical_results),
            "experiment_context": request.experiment_context or "",
            "framework_spec": request.framework_spec or "",
            "claims_json": self._safe_json(claims),
            "evidence_map_json": self._safe_json(evidence_map),
            "evidence_catalog_json": self._safe_json(evidence_catalog),
        }
        rendered = self._render_template(template, payload)

        content, meta = self.llm_gateway.execute_call(
            model=self.model,
            system_prompt=system_prompt,
            prompt=rendered,
            temperature=0.2,
        )
        return content or ""

    # -------------------- Utilities --------------------
    def _split_sections(self, report_md: str) -> Tuple[str, str, str]:
        # Very light split to satisfy pipeline’s expectations without imposing format
        if not report_md:
            return "", "", ""
        parts = report_md.split("\n## ", 1)
        scanner = parts[0].strip()
        rest = parts[1] if len(parts) > 1 else ""
        collaborator = ("## " + rest).strip() if rest else ""
        # Transparency: try to extract a section; otherwise include a brief appendix
        transp = ""
        if "Evidence References" in report_md:
            transp = report_md.split("Evidence References", 1)[-1]
            transp = ("Evidence References" + transp).strip()
        return scanner, collaborator, transp

    def _load_yaml(self, filename: str) -> Dict[str, Any]:
        import yaml
        path = self.prompts_dir / filename
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def _render_template(self, template: str, payload: Dict[str, Any]) -> str:
        # Simple double-brace replacement to avoid str.format pitfalls
        rendered = template
        for key, value in payload.items():
            token = "{{" + key + "}}"
            rendered = rendered.replace(token, value if isinstance(value, str) else json.dumps(value))
        return rendered

    def _convert_evidence_result(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        out = []
        for r in results:
            out.append(
                {
                    "document_id": r.get("document_id") or r.get("doc_id") or "unknown",
                    "dimension": r.get("dimension") or r.get("label") or "unknown",
                    "quote": r.get("quote_text") or r.get("text") or "",
                    "confidence": r.get("confidence", 0.0),
                    "start": r.get("start", None),
                    "end": r.get("end", None),
                }
            )
        return out

    def _safe_json(self, obj: Any) -> str:
        try:
            return json.dumps(obj, ensure_ascii=False)
        except Exception:
            return json.dumps(str(obj))

    def _parse_json_list(self, content: str) -> Optional[List[Any]]:
        if not content:
            return None
        txt = content.strip()
        # Remove code fences if present
        if txt.startswith("```"):
            try:
                fence_body = txt.strip('`')
                # If fenced like ```json\n...\n```
                start = txt.find('\n')
                end = txt.rfind('```')
                if start != -1 and end != -1 and end > start:
                    txt = txt[start+1:end].strip()
            except Exception:
                pass
        # Direct parse
        try:
            data = json.loads(txt)
            return data if isinstance(data, list) else None
        except Exception:
            pass
        # Extract first JSON array substring
        try:
            first = txt.find('[')
            last = txt.rfind(']')
            if first != -1 and last != -1 and last > first:
                sub = txt[first:last+1]
                data = json.loads(sub)
                return data if isinstance(data, list) else None
        except Exception:
            return None
        return None


