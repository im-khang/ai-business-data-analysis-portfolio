---
title: 'Hiring-manager Decision Layer for Olist GitHub Pages Dashboard'
type: 'feature'
created: '2026-05-22'
status: 'done'
context:
  - '.a0proj/_bmad-output/design-thinking-2026-05-22.md'
  - '.a0proj/_bmad-output/implementation-artifacts/spec-static-github-pages-plotly-dashboard-olist-delivery-sla-case-study.md'
baseline_commit: '95476e9cf0cb80da24b4890d03f02ab65aaa7508'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** The current static Olist dashboard has working metrics and charts, but hiring managers still have to infer the decision logic, business judgment, and caveats from scattered page sections. That weakens the scan path for BA/DA credibility and makes operations recommendations feel less explicit than the evidence supports.

**Approach:** Add a hiring-manager decision layer to the existing GitHub Pages dashboard: stronger above-fold business framing, visible caveat chips near claims, chart-level “So what?” captions, risk segment language reframed as investigation candidates, and a concise Decision Logic / Action Priority panel that connects delivery SLA risk → customer review impact → seller/category/region candidates → next actions.

## Boundaries & Constraints

**Always:** Keep the dashboard static-only under `docs/inventory-stockout-overstock-analysis/` using plain HTML/CSS/JS and Plotly. Preserve relative asset and data fetch paths, aggregate JSON only, no raw Olist data, no secrets, and no server/backend dependencies. Preserve proxy-honest language: delivery SLA risk, review-score association, seller/category/region investigation candidates, and fulfillment-planning proxy signals only. Keep the slice focused on hiring-manager depth plus operations realism, not new analytics.

**Ask First:** Halt before changing the data exporter, adding new aggregate JSON fields, adding build tooling, introducing frameworks, vendoring new assets, changing README/case-study docs, adding screenshots, or making any claim that needs row-level data or external validation. Halt before adding a sticky mini-nav if it would require broad page restructuring beyond this single-goal UX slice.

**Never:** Do not push, deploy, change raw-data handling, expose raw rows, add time estimates, claim causality, or claim Olist directly measures stockouts, overstock, inventory-on-hand, replenishment performance, warehouse availability, or backorders. Do not rename the case study or convert the dashboard into a generic sales report.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Static dashboard loads | Existing aggregate JSON files load through relative fetch paths | Above-fold hero, KPI cards, caveat chips, charts, captions, investigation-candidate panel, and decision/action panel render without backend code | Existing visible data-load error remains available if fetch fails |
| Hiring-manager scan path | Viewer opens page and scans top section before charts | Page states business question, strongest proof metrics, caveat/proxy limits, and decision story before deep chart interpretation | Copy avoids unsupported direct inventory or causality claims |
| Chart interpretation | Viewer reviews each Plotly chart panel | Each chart has a concise “So what?” caption tying evidence to decision use and caveat level | Captions do not imply root-cause proof where data only supports association/candidate framing |
| Segment terminology | Existing risk segment chart/data are unchanged | UI labels and explanatory copy say “Investigation Candidates” rather than treating segments as proven risk causes | Existing chart still renders if risk segment JSON shape is unchanged |

</frozen-after-approval>

## Code Map

- `docs/inventory-stockout-overstock-analysis/index.html` -- dashboard shell, hero copy, panel order, chart headings, caveat chips, action-priority content, and optional mini-nav target.
- `docs/inventory-stockout-overstock-analysis/assets/js/app.js` -- KPI card rendering, Plotly chart titles/text, segment label wording, and dynamic build-note/error handling.
- `docs/inventory-stockout-overstock-analysis/assets/css/styles.css` -- responsive layout and visual treatments for hero proof row, caveat chips, captions, decision/action panels, and optional sticky mini-nav.
- `docs/inventory-stockout-overstock-analysis/assets/data/*.json` -- existing aggregate data contract; should remain unchanged unless implementation hits a blocker requiring user approval.
- `.a0proj/_bmad-output/design-thinking-2026-05-22.md` -- audience and trust-path rationale for hiring-manager credibility, operations realism, visible caveats, and decision story.

## Tasks & Acceptance

**Execution:**
- [x] `docs/inventory-stockout-overstock-analysis/index.html` -- revise above-fold hero with business question, decision-story summary, proof/caveat chips, clearer navigation labels, chart captions, renamed Investigation Candidates section, and Decision Logic / Action Priority panel -- makes BA/DA judgment and operational next actions visible without requiring code or artifact inspection.
- [x] `docs/inventory-stockout-overstock-analysis/assets/js/app.js` -- update rendered KPI/card labels, Plotly titles, hover/caption-adjacent wording where JS owns text, and risk segment terminology to “investigation candidates” while keeping relative fetch paths and existing JSON schema -- aligns dynamic content with proxy-honest decision-support language.
- [x] `docs/inventory-stockout-overstock-analysis/assets/css/styles.css` -- add responsive styles for improved hero hierarchy, chip groups, “So what?” captions, decision/action panel, investigation-candidate framing, and optional sticky mini-nav if it stays small -- improves recruiter/hiring-manager scan quality on desktop and mobile.
- [x] `docs/inventory-stockout-overstock-analysis/index.html`, `assets/js/app.js`, and `assets/css/styles.css` -- inspect for unsupported claim wording and static-hosting regressions -- protects existing GitHub Pages, aggregate-only, and proxy-honesty constraints.

**Acceptance Criteria:**
- Given `cd docs && python -m http.server 8000`, when `/inventory-stockout-overstock-analysis/` is opened, then the page loads with KPI cards and Plotly charts from `./assets/data/*.json` and no backend/server build step is required.
- Given a hiring manager scans above the fold, when they read the hero and first proof elements, then they see the business question, delivery SLA risk framing, review-impact association framing, proxy limitation, and decision story before chart-heavy sections.
- Given any chart panel is visible, when a viewer reads below or near it, then a “So what?” caption explains the decision use without claiming unsupported root cause or direct inventory measurement.
- Given the seller/category/region segment section is visible, when labels/headings/captions are read, then segments are framed as “Investigation Candidates” or candidate queues rather than proven causes.
- Given the Decision Logic / Action Priority panel is visible, when a viewer reads it, then it connects SLA risk, review impact, investigation candidates, and recommended next actions in priority order.
- Given dashboard files are searched, when checking for direct inventory or causality claims, then no copy claims stockout rate, overstock value, inventory-on-hand, replenishment performance, warehouse availability, backorders, or single-cause proof.
- Given `git status --short`, when implementation is complete, then only intended static dashboard files are changed unless user explicitly approved data-pipeline changes.

## Spec Change Log

## Design Notes

Prefer copy changes and small structural additions over new data. Suggested decision panel pattern:

```text
Decision Logic
1. Size SLA exposure: late delivered orders + late rate.
2. Check customer pain: review score association by delay band.
3. Triage candidates: seller/state/category combinations with late volume.
4. Act carefully: audit promise accuracy, carrier routes, seller fulfillment handoffs, and inventory snapshots before production decisions.
```

Use caveat chips near claims, not only in a bottom note. Good chip examples: `Aggregate-only public data`, `Proxy signal, not inventory proof`, `Association, not causality`, `Investigation candidates`. Keep “risk” where it describes delivery SLA exposure; use “candidate” where talking about seller/category/region segments.

## Verification

**Commands:**
- `grep -RniE "stockout rate|overstock value|inventory on hand|stock-on-hand|replenishment performance|warehouse availability|backorder|caused by|proves" docs/inventory-stockout-overstock-analysis || true` -- expected: no unsupported direct-measurement or causality claims.
- `grep -Rni "Investigation Candidates\|So what\?|Decision Logic\|Action Priority" docs/inventory-stockout-overstock-analysis` -- expected: new decision-layer labels and captions are present.
- `python -m py_compile case-studies/inventory-stockout-overstock-analysis/dashboard/export_pages_data.py` -- expected: existing exporter remains syntactically valid if untouched.
- `cd docs && python -m http.server 8000` -- expected: `/inventory-stockout-overstock-analysis/` renders locally through static HTTP with relative asset/data paths.
- `git status --short` -- expected: changed files are limited to intended dashboard HTML/CSS/JS files unless user approved otherwise.

## Suggested Review Order

**Decision story entry point**

- Hero frames hiring-manager question and caveat-first trust path.
  [`index.html:15`](../../../docs/inventory-stockout-overstock-analysis/index.html#L15)

- Decision panel turns evidence into prioritized operations actions.
  [`index.html:51`](../../../docs/inventory-stockout-overstock-analysis/index.html#L51)

**Evidence interpretation**

- KPI cards add decision-use notes without new data fields.
  [`app.js:13`](../../../docs/inventory-stockout-overstock-analysis/assets/js/app.js#L13)

- Chart captions explain “So what?” while avoiding causality claims.
  [`index.html:67`](../../../docs/inventory-stockout-overstock-analysis/index.html#L67)

- Review score chart keeps 0–5 scale to avoid visual exaggeration.
  [`app.js:37`](../../../docs/inventory-stockout-overstock-analysis/assets/js/app.js#L37)

**Investigation candidate framing**

- Segment section labels queues as candidates, not proven causes.
  [`index.html:81`](../../../docs/inventory-stockout-overstock-analysis/index.html#L81)

- Hover text reinforces candidate framing inside Plotly output.
  [`app.js:46`](../../../docs/inventory-stockout-overstock-analysis/assets/js/app.js#L46)

**Static safety and presentation**

- Plotly guard surfaces CDN load failure as visible dashboard error.
  [`app.js:29`](../../../docs/inventory-stockout-overstock-analysis/assets/js/app.js#L29)

- Responsive styles support hero, chips, captions, and action cards.
  [`styles.css:1`](../../../docs/inventory-stockout-overstock-analysis/assets/css/styles.css#L1)
