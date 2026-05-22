---
title: 'Dashboard Preview README Link'
type: 'feature'
created: '2026-05-23T06:30:27+00:00'
status: 'done'
route: 'one-shot'
---

# Dashboard Preview README Link

## Intent

**Problem:** Top-level portfolio README linked the live Olist dashboard but did not show the captured dashboard preview asset, reducing quick-scan usefulness for recruiters and hiring managers.

**Approach:** Add the saved `assets/dashboard-preview.png` asset to git and embed it in `README.md` as a clickable preview that opens the live dashboard, while preserving existing portfolio framing and proxy-honest caveats.

## Suggested Review Order

1. `../../../../README.md:30` -- Confirm Findings Artifacts section keeps existing links and shows clickable dashboard preview without adding unsupported claims.
2. `../../../../assets/dashboard-preview.png` -- Confirm screenshot asset renders and represents the linked dashboard.
3. `../../../../.gitignore` -- Confirm raw Olist CSV protections remain unchanged.
