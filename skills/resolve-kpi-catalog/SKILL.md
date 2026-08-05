---
name: resolve-kpi-catalog
description: Map dashboard KPI requests to certified catalog definitions and identify metric conflicts. Use after request normalization and before schema discovery, SQL generation, or dashboard specification work.
---

# Resolve KPI Catalog

Read `catalog/kpi-catalog.json` and the normalized `request.yaml`.

## Workflow

1. Match requested KPI IDs and aliases to certified records.
2. Verify requested dimensions and filters are allowed by each matched KPI.
3. Compare requested grain and freshness to the KPI semantic contract.
4. Produce one traceability record per KPI.

## Output

Return `kpi-resolution.yaml` with `kpi_id`, catalog version, semantic version, business owner, steward, curated asset, output field, valid controls, and status.

## Rules

- Never select a deprecated KPI without explicit owner approval.
- Treat competing definitions or changed denominators as unresolved, not as aliases.
- Open a KPI-definition task when no certified metric matches.
- Do not choose raw tables; source mapping must terminate at a curated asset.
