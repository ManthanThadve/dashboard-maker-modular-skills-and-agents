# Operating Guide

## Request lifecycle

1. Create `requests/<request-id>/request.yaml` from the business form.
2. Run `$normalize-dashboard-request`, then `$resolve-kpi-catalog`.
3. Use `$discover-bigquery-schema` only against `catalog/source-allowlist.json`.
4. Generate `model.sql`, `validation.sql`, and an output-schema contract.
5. Obtain analytics-engineer approval before creating a view, mart, or scheduled query.
6. Generate `dashboard-spec.yaml` and select an active template version.
7. Use the Linking API URL, copy the template, complete manual assembly, and capture a screenshot.
8. Record UAT, report URL, data source, and ownership in `release.md`.

## Required pull-request evidence

- KPI catalog version and unresolved-definition status.
- Dry-run bytes processed and partition/clustering assessment.
- Reconciliation result for at least one agreed business period.
- Dashboard specification and template compatibility check.
- UAT sign-off and group-based sharing plan.

## Quality gates

| Gate | Owner | Blocks release when |
|---|---|---|
| Intake | Requester | KPI, grain, audience, or acceptance examples are missing |
| Semantic | Steward | Metric has no certified or approved draft definition |
| Data | Analytics engineer | SQL has unbounded scans, failed reconciliation, or unclear source grain |
| Visual | BI analyst | A chart is not bound to expected filters or contract fields |
| UAT | Business owner | KPI values, permissions, or business interpretation fail |
