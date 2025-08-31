# Inbox - Raw Backlog Items

**Purpose**: Raw capture of backlog items without organization or sprint planning. Items here will be groomed into organized sprints later.

**Usage**:

- "inbox this" → append new items here with minimal formatting
- "groom our sprints" → move all items from here to sprints.md with proper organization

---

## Capability Matrix Architecture for Model Selection

**Problem**: Current fallback system uses linear utility tier cascades that can select unsafe models (experimental, deprecated) as fallbacks.

**Proposed Solution**: Replace linear fallback chains with capability matrices:

### Production Matrix (Capability-Based)
```
                    | Analysis | Synthesis | Validation | Coordination |
--------------------|----------|-----------|------------|--------------|
Top Tier            | G2.5-Pro | G2.5-Pro  | G2.5-Pro   | G2.5-Pro     |
Standard            | G2.5-Flash| G2.5-Flash| G2.5-Flash | G2.5-Flash   |
Cost Optimized      | G2.5-Lite| G2.5-Lite | G2.5-Lite  | G2.5-Lite    |
Cross-Provider      | Claude-Haiku| Claude-Sonnet| Claude-Sonnet| Claude-Sonnet|
```

### Development Matrix (Includes Experimental)
```
                    | Analysis | Synthesis | Validation | Coordination |
--------------------|----------|-----------|------------|--------------|
Experimental        | G2.0-Exp | G2.0-Exp  | G2.0-Exp   | G2.0-Exp     |
Production          | G2.5-Flash| G2.5-Flash| G2.5-Flash | G2.5-Flash   |
```

**Key Principles**:
- Experimental models are opt-in only, never automatic fallbacks
- Every capability has at least 3 production-ready options
- Horizontal fallback (same capability tier) before vertical fallback (different tier)
- Safety gates prevent unsafe model selection

**Integration Considerations**:
- Replace utility_tier system with capability classifications
- Update CLI to support matrix-based model selection
- Maintain backward compatibility during transition
- Consider environment-specific matrices (prod vs dev)
