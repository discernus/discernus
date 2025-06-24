# UNDER CONSIDERATION – Discernus Cloud Centered Distribution Strategy

## Purpose

To summarize strategic distribution options for Discernus and evaluate the potential shift from self-hosted binaries to a cloud-centered, API-first model. This plan outlines licensing, community, reproducibility, and monetization considerations as well as implementation pathways.

---

## 1. Summary of Distribution Models Considered

### A. Traditional OSS Binary Distribution

- **Structure**: Docker images + local CLI/API, source-available for academic use.
- **Licence**: Custom “Academic Use Only” licence or PolyForm Non-Commercial 1.0.0.
- **Pros**:
  - Transparent to academia.
  - Maximum reproducibility.
  - Familiar to IRBs and journals.
- **Cons**:
  - Licensing complexity with GPL/AGPL dependencies.
  - High fork risk without strong trademark control.
  - Friction for non-technical users.

### B. Business Source License (BSL)

- **Structure**: Source-available with delayed open-source conversion (e.g., after 3 years).
- **Pros**:
  - Predictable “open” timeline.
  - Better for attracting commercial partners post-PMF.
- **Cons**:
  - Optics risk: resembles “bait-and-switch” if community grows first.
  - Fork risk rises at each expiration cycle.

### C. API-First Cloud Distribution (Current Focus)

- **Structure**: Centralized cloud service with client SDKs (Apache-2.0), generous academic quota, optional enterprise support.
- **Pros**:
  - Simplifies licensing and dependency compliance.
  - Lower user friction.
  - Easier usage-based monetization.
  - Cloud-native data/network effects (CorpusCloud, extension registry).
- **Cons**:
  - Academic pushback on reproducibility.
  - Data sovereignty concerns (e.g., EU, NIH).
  - Cost and scale risks.
  - AGPL still dangerous if integrated or modified.

---

## 2. Licensing Implications

| Licence Model          | GPL Risk | Reproducibility | Fork Control | Monetization Readiness |
|------------------------|----------|------------------|----------------|--------------------------|
| PolyForm NC            | Low      | Medium           | Moderate (requires CLA + trademark) | Medium (dual-license path) |
| Academic Use Only      | Low      | High             | High (tight scoping) | Low-medium |
| BSL                    | Medium   | High (after expiration) | Medium (pre-change), High (post-change) | High |
| API SaaS Only          | Minimal (except AGPL) | Low-medium | High (no source provided) | High |

---

## 3. Academic Strategy: Cloud + Open Science Commitments

- **Free Tiers**: Auto-approve *.edu for token grants.
- **Reproducibility Kit**: Jupyter export, manifest, DOI corpus snapshot.
- **Trust & Escrow**:
  - Publish stability guarantees (e.g., 5-year endpoint support).
  - Commit to AGPL fallback in case of project sunset.

---

## 4. Network Effects Strategy (Cloud-Native Extension Ecosystem)

- **Extension packaging**: OCI / WASM bundles + manifest.
- **Execution model**: Firecracker/WASM sandboxes with scoped permissions.
- **Registry**: Searchable public marketplace + optional private/premium lanes.
- **Incentives**:
  - Token credits for academic usage.
  - Reputation badges, usage leaderboards.
  - Optional monetization for premium/enterprise extensions.

---

## 5. Implementation Roadmap (Provisional)

| Quarter | Milestone |
|---------|-----------|
| Q3 2025 | Finalize API architecture, licence choice, and CLA framework |
| Q4 2025 | Launch academic access programme + core APIs |
| Q1 2026 | Launch extension SDK + registry alpha |
| Q2 2026 | CorpusCloud Prime & Management APIs live |
| Q3 2026 | Begin monetization layers (paid extensions, enterprise SDKs) |
| Q4 2026 | Governance + reproducibility certification pipeline |

---

## 6. Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Reproducibility skepticism | Exportable experiment artefacts, DOI citation support |
| Academic pushback on lock-in | Publish open roadmap, escrow clause for code release |
| Cost spikes from academic use | Cap free tier, pooled grant credit system |
| Legal exposure from AGPL | Avoid modification or network exposure of AGPL code |

---

## Thought Loop

> Discernus must deliver open science credibility *without* repeating old FOSS compliance fights. By anchoring trust in reproducibility, incentivizing extensibility, and modularizing compliance, a cloud-native Discernus becomes not just a product—but a platform for a new generation of scholarly analysis.

