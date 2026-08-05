# Looker Studio Template Governance

Maintain three template families in the registry:

| Family | Intended use | Required contract |
|---|---|---|
| Executive Pulse | Leadership weekly review | Executive contract when activated |
| Operational Performance | Team performance and drill-down | `operational-performance-1.0.0.json` |
| Funnel and Cohort | Conversion and retention analysis | Funnel contract when activated |

For every template release:

1. Create the report under the dedicated Workspace template owner.
2. Add the BigQuery source as alias `ds0_main` and verify the documented field contract.
3. Capture a screenshot and report ID in `template-registry.json`.
4. Change the record from `draft` to `active` only after a synthetic-data compatibility test.
5. Create a new semantic version for any breaking field-contract change; never mutate an active contract in place.

Use `tools/dashboard_maker.py build-link` only for active records with real report IDs.
