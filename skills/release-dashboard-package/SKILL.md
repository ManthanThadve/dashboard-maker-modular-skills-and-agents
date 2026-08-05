---
name: release-dashboard-package
description: Assemble the governed release record for a Looker Studio dashboard. Use after data validation, dashboard visual QA, business UAT, and group-based sharing are complete.
---

# Release Dashboard Package

Read every request artifact: request, KPI resolution, model, validation evidence, dashboard spec, Linking API record, and UAT result.

## Output

Return `release.md` with request ID, catalog/template versions, curated source, freshness SLA, report URL, owners, UAT approval, known limitations, and support contact.

## Rules

- Refuse release when open questions, failed validation, missing UAT, or draft template status remains.
- Record group-based sharing and the owning Workspace account.
- Link all artifact paths and preserve versions; do not replace historical records.
- Include any cost, freshness, or metric caveat visible to dashboard users.
