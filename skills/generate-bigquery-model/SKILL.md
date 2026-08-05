---
name: generate-bigquery-model
description: Generate reviewable BigQuery GoogleSQL for curated views or scheduled marts that power dashboards. Use after KPI definitions, source metadata, grain, and access policy are approved.
---

# Generate BigQuery Model

Read the approved request, KPI resolution, schema discovery, `governance/source-allowlist.json`, and `references/cost-guardrails.md`.

## Output

Produce:

1. `model.sql` in Standard SQL.
2. An output-schema contract with grain and field descriptions.
3. `validation.sql` for a business-agreed date range.
4. A cost/performance note and deploy recommendation.

## Rules

- Use only fully qualified, allow-listed source tables.
- State the output grain before SQL.
- Filter partition columns directly; never use `SELECT *`.
- Use `SAFE_DIVIDE` for ratios and calculate ratios from additive components.
- Preserve correct distinct-count behavior across the dashboard's selectable date range.
- Use approximate functions only when the catalog explicitly permits them.
- Do not execute DDL, schedule queries, or publish assets. Produce a reviewable pull-request artifact.
