---
name: validate-dashboard-data
description: Create and interpret reconciliation checks for a dashboard's curated BigQuery model. Use after SQL generation and before a dashboard enters UAT or production.
---

# Validate Dashboard Data

Read the KPI resolution, model SQL, validation SQL, and business acceptance examples.

## Workflow

1. Select an agreed closed reporting period with stable source data.
2. Compare raw source controls with the curated asset at the same filters and grain.
3. Reconcile each KPI; calculate variance where exact equality is not appropriate.
4. Produce pass/fail evidence for the pull request.

## Rules

- Filter both source and curated queries to the same date range and business filters.
- Never validate a ratio by averaging row-level percentages.
- Distinct-count KPIs must be compared as `COUNT(DISTINCT key)` over the full selected period.
- Flag failed, missing, or stale evidence; do not rationalize it away.
