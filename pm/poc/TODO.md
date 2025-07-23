# PoC Pending Tasks

- [ ] Implement `discernus results <RUN_ID>` CLI command to fetch and organize results by run ID.
- [ ] Add export/import functionality: `discernus run --from-manifest runs/<RUN_ID>/manifest.json`.
- [ ] Harden cost guard: abort mid-run in live mode when spending exceeds the cap via Lua script.
- [ ] Extend run manifest to capture output artifact hashes and generate a human-readable report.

## Next-Step Wishlist (post-PoC)

- [ ] Implement `discernus export <RUN_ID>` CLI command to materialize run directory (`corpus/`, `analysis/`, `synthesis/`, `logs/`, `manifest.json`).
- [ ] Precision-aware normalizer & framework `precision` field.
- [ ] Support `non_deterministic` averaging and `runs_per_chunk`.
- [ ] Build ValidationAgent for custom schema validation.
- [ ] Build PostHocMathAgent for retro metrics analysis.
- [ ] Composite framework synthesis combining multiple analyses.
- [ ] Complete Security package: static policy enforcement in router and deploy SecuritySentinelAgent. 