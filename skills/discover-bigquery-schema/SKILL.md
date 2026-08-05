---
name: discover-bigquery-schema
description: Discover approved BigQuery source schemas, partitions, joins, freshness, and candidate curated assets for dashboard KPIs. Use when a KPI resolution is approved and source metadata is needed without querying raw business data.
---

# Discover BigQuery Schema

Read `governance/source-allowlist.json`, then read `references/metadata-queries.md` when constructing metadata queries.

## Workflow

1. Restrict discovery to allow-listed projects and datasets.
2. Query `INFORMATION_SCHEMA` for tables, columns, partitions, options, and views.
3. Identify source grain, partition column, clustering, update frequency, sensitive columns, and proposed joins.
4. Prefer an existing certified curated asset over new raw-source logic.

## Output

Return `schema-discovery.yaml` with candidate assets, field mappings, join assumptions, freshness, partition plan, restricted fields, and unresolved questions.

## Rules

- Inspect metadata only; do not sample personal or sensitive data.
- Exclude restricted columns listed in the allow-list.
- State uncertainty when primary/foreign-key relationships are undocumented.
- Recommend a mart only after documenting expected reuse and likely scan cost.
