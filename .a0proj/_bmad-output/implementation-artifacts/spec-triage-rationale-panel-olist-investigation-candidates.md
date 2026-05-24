---
title: 'Triage Rationale Panel for Olist Investigation Candidates'
type: 'feature'
created: '2026-05-23'
status: 'done'
baseline_commit: 'f06af9b5a3c48a7bd135b9070e0c8138f474f39f'
context:
  - '.a0proj/_bmad-output/design-thinking-2026-05-22.md'
  - '.a0proj/_bmad-output/implementation-artifacts/spec-hiring-manager-decision-layer-olist-github-pages-dashboard.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** The current dashboard ranks seller/category/region investigation candidates, but it does not yet explain why those candidates appear, what operations checks they suggest, what evidence limits apply, or where a reviewer can inspect the proof trail. Hiring managers and ecommerce/logistics reviewers may see the ranked bar chart, but still have to infer triage logic and bounded actionability.

**Approach:** Add a static Triage Rationale Panel next to or directly below the Investigation Candidates section. Panel explains candidate-selection rationale, ops checks, evidence limits, and proof-trail links while preserving story: delivery SLA risk → review impact → seller/category/region candidates → next actions.

## Boundaries & Constraints

**Always:** Work inside `/a0/usr/projects/ba`. Keep static GitHub Pages under `docs/inventory-stockout-overstock-analysis/` with plain HTML/CSS/JS, Plotly, relative asset paths, and aggregate JSON only. Use proxy-honest wording and preserve existing charts, KPI cards, caveat chips, decision panel, local HTTP/fetch behavior, and Pages compatibility.

**Ask First:** Halt before changing exporter, aggregate JSON schema, raw-data handling, README/case-study docs, screenshots, chart logic, tooling, dependencies, broad navigation, or claims needing row-level/external operational data.

**Never:** Do not push, deploy, expose raw CSVs, include secrets, add backend code, add time estimates, blame sellers/carriers, claim causality, or claim Olist proves stockouts, overstock, inventory-on-hand, replenishment performance, warehouse availability, or backorders.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Candidate section loads | Existing `risk_segments.json` loads through relative fetch | Ranked candidate chart remains visible and a static Triage Rationale Panel explains selection logic, checks, limits, and proof trail | Existing dashboard error handling remains available if fetch fails |
| Reviewer reads candidate rationale | Viewer reaches Investigation Candidates section | Panel states candidates appear because late-order volume and late-rate context make them worth investigation, not because they prove root cause | Copy avoids seller blame and direct inventory/causality claims |
| Operations user wants next action | Viewer reads suggested checks | Panel lists practical checks such as delivery promises, seller fulfillment handoffs, carrier lanes/routes, and company-owned inventory snapshots before policy action | Checks are phrased as investigation prompts, not conclusions |
| Technical reviewer wants evidence trail | Viewer reads proof-trail links | Panel links to existing case study and SLA/risk artifacts without exposing raw CSV data | Links use existing public repo paths and do not require backend code |

</frozen-after-approval>

## Code Map

- `docs/inventory-stockout-overstock-analysis/index.html` -- dashboard shell and Investigation Candidates section; primary place for static triage rationale copy, proof-trail links, candidate-not-blame wording, and any section-local structure.
- `docs/inventory-stockout-overstock-analysis/assets/js/app.js` -- existing Plotly rendering for `risk-segments`; should stay data-compatible, with only label/hover tweaks if needed to align with new panel wording.
- `docs/inventory-stockout-overstock-analysis/assets/css/styles.css` -- responsive styling for the Triage Rationale Panel, section-local grid/card layout, proof-trail link group, and mobile stacking.
- `docs/inventory-stockout-overstock-analysis/assets/data/risk_segments.json` -- existing aggregate candidate data contract; read-only for this slice unless a blocker is approved by the user.
- `case-studies/inventory-stockout-overstock-analysis/artifacts/seller-category-region-risk.md` -- existing proof-trail target for ranked seller/category/region evidence.
- `case-studies/inventory-stockout-overstock-analysis/artifacts/delivery-sla-summary.md` -- existing proof-trail target for SLA sizing context.
- `.a0proj/_bmad-output/design-thinking-2026-05-22.md` -- rationale for this prototype slice: evidence-confidence and triage explanation layer.

## Tasks & Acceptance

**Execution:**
- [x] `docs/inventory-stockout-overstock-analysis/index.html` -- add static Triage Rationale Panel with four parts: why candidates appear, ops checks, evidence limits, proof-trail links -- makes candidate ranking understandable without new analytics.
- [x] `docs/inventory-stockout-overstock-analysis/assets/css/styles.css` -- add responsive panel/card/link styles -- preserves desktop/mobile scan path.
- [x] `docs/inventory-stockout-overstock-analysis/assets/js/app.js` -- minimally adjust candidate chart wording only if needed -- keeps JSON contract and fetch behavior stable.
- [x] `docs/inventory-stockout-overstock-analysis/index.html`, `assets/js/app.js`, and `assets/css/styles.css` -- run claim-safety and static-hosting checks -- protects Pages compatibility and proxy-honest framing.

**Acceptance Criteria:**
- Given `cd docs && python -m http.server 8000`, when `/inventory-stockout-overstock-analysis/` is opened, then KPI cards, Plotly charts, and the Investigation Candidates section load through static HTTP/fetch with no backend or build step.
- Given a viewer reaches Investigation Candidates, when they read the new panel, then they can identify why candidates appear: meaningful late-order volume plus late-rate context creates an investigation queue, not proof of root cause.
- Given an operations-minded viewer reads suggested checks, when they choose next actions, then they see delivery promise review, seller fulfillment handoff review, carrier lane/route review, and company-owned inventory snapshot validation framed as checks before policy decisions.
- Given a skeptical reviewer reads evidence limits, when they inspect candidate claims, then the panel states aggregate public data, association not causality, candidate not blame, and proxy signal not inventory proof.
- Given a technical reviewer wants proof trail, when they use links in the panel, then they can reach existing case-study/SLA/risk artifacts or portfolio repo pages without exposing raw CSVs or requiring secrets.
- Given dashboard files are searched, when checking claim wording, then no copy claims stockout rate, overstock value, inventory-on-hand, replenishment performance, warehouse availability, backorders, seller fault, carrier fault, or single-cause proof.
- Given `git status --short`, when implementation is complete, then only intended dashboard HTML/CSS/JS files and this spec are changed unless the user explicitly approved another file.

## Spec Change Log

## Design Notes

Do not duplicate the existing hero, KPI proof strip, sticky navigation, or general chart “So what?” captions. This slice should deepen the candidate section only.

Suggested panel structure:

```text
Triage rationale
Why these candidates appear: late-order volume + late-rate context.
Checks to run: promise accuracy, fulfillment handoffs, carrier lanes, company inventory snapshots.
Evidence limits: aggregate data, association not causality, candidates not blame.
Proof trail: case study, SLA summary, seller/category/region risk artifact.
```

Use short labels that support scanning: `Why this candidate queue`, `Operations checks`, `Evidence limits`, `Proof trail`. Link text should describe reviewer value, not implementation detail.

## Verification

**Commands:**
- `node --check docs/inventory-stockout-overstock-analysis/assets/js/app.js` -- expected: JavaScript syntax passes.
- `cd docs && python -m http.server 8000` -- expected: `/inventory-stockout-overstock-analysis/` renders locally through static HTTP with relative asset/data paths.
- `python - <<'PY'\nimport urllib.request\nbase='http://127.0.0.1:8000/inventory-stockout-overstock-analysis/'\nfor path in ['', 'assets/data/risk_segments.json', 'assets/js/app.js', 'assets/css/styles.css']:\n    r=urllib.request.urlopen(base+path, timeout=5)\n    print(path or 'index.html', r.status)\nPY` -- expected: all responses print `200` while local server is running.
- `grep -RniE "stockout rate|overstock value|inventory[- ]?on[- ]?hand|replenishment performance|warehouse availability|backorder|seller fault|carrier fault|caused by|proves|proof of root cause" docs/inventory-stockout-overstock-analysis || true` -- expected: no unsupported direct-measurement, blame, or causality claims.
- `grep -RniE "Triage Rationale|Why these candidates|Operations checks|Evidence limits|Proof trail|candidate.*not blame|association not causality" docs/inventory-stockout-overstock-analysis` -- expected: new panel labels and caveat wording are present.
- `git status --short --ignored case-studies/inventory-stockout-overstock-analysis/data/raw` -- expected: raw Olist CSVs remain ignored/untracked and no raw CSV is staged.
- `git status --short` -- expected: only intended dashboard files and this spec are changed unless user approved otherwise.


## Suggested Review Order

**Candidate rationale entry**

- Main panel explains why candidate queue exists and stays bounded.
  [`index.html:86`](../../../docs/inventory-stockout-overstock-analysis/index.html#L86)

- Operations checks turn candidate ranking into safe investigation prompts.
  [`index.html:96`](../../../docs/inventory-stockout-overstock-analysis/index.html#L96)

**Evidence limits and proof trail**

- Limits separate aggregate signals from causality, blame, and inventory proof.
  [`index.html:105`](../../../docs/inventory-stockout-overstock-analysis/index.html#L105)

- Proof links connect reviewers to public case-study artifacts.
  [`index.html:115`](../../../docs/inventory-stockout-overstock-analysis/index.html#L115)

**Responsive presentation**

- Triage styles keep panel scannable across desktop and mobile.
  [`styles.css:2`](../../../docs/inventory-stockout-overstock-analysis/assets/css/styles.css#L2)
