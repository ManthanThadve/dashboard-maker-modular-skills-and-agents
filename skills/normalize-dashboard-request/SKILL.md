---
name: normalize-dashboard-request
description: Convert a business dashboard brief into a complete, reviewable request package. Use when a requester provides KPIs, audience, dimensions, filters, time grain, purpose, acceptance criteria, or a dashboard deadline.
---

# Normalize Dashboard Request

Read `catalog/kpi-catalog.json` and `governance/source-allowlist.json` before producing an artifact.

## Workflow

1. Extract the decision, audience, owner, KPIs, grain, date semantics, filters, freshness, and acceptance examples.
2. Use a canonical KPI ID only for an exact catalog match. Do not create formulas or sources.
3. Mark missing denominator, date field, source-of-truth, grain, owner, or access intent as an open question.
4. Recommend a template family: `executive-pulse`, `operational-performance`, or `funnel-and-cohort`.

## Output

Return `request.yaml` and a short clarification list. Include `open_questions`; set it to an empty list only when the request is ready for catalog resolution.

## Rules

- Keep dashboard-level controls separate from chart-specific filters.
- Require at least one measurable acceptance example per request.
- Do not mark a request ready if a KPI has an ambiguous calculation or grain.
- Follow the field shape in `examples/DB-104/request.yaml`.
