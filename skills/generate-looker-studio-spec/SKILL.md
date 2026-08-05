---
name: generate-looker-studio-spec
description: Generate an exact, template-based Looker Studio assembly specification from an approved curated schema and KPI mapping. Use when a BI analyst needs chart, field, formula, control, and layout instructions for a dashboard.
---

# Generate Looker Studio Specification

Read the request, KPI resolution, output schema, and the selected field contract in `contracts/`.

## Output

Return `dashboard-spec.yaml` containing:

- Template/version, source alias, report name, and source asset.
- Page names and canvas positions using `x`, `y`, `width`, and `height`.
- Every chart's type, title, dimensions, metrics, aggregation, formulas, sorting, range, comparisons, and filter scope.
- Dashboard controls, accessible labels, refresh note, owner note, and release checks.

## Rules

- Bind only contract fields and approved calculated fields.
- Use exact Looker Studio formulas; calculate ratios from summed components.
- Set every chart's filter interaction deliberately.
- Use templates and a human assembly workflow; do not claim autonomous report generation.
- Follow `examples/DB-104/dashboard-spec.yaml` as the expected level of precision.
