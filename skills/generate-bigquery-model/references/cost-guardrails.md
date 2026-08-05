# BigQuery Cost Guardrails

- Use Standard SQL with fully qualified table names and explicit columns.
- Demonstrate direct filtering of each partition column.
- Capture dry-run bytes before approval; set a project-agreed `maximum_bytes_billed` for validation.
- Prefer a scheduled, partitioned, clustered mart when repeated dashboards scan large joins.
- Do not aggregate daily distinct values and later sum them for an arbitrary date range.
- Use `SAFE_DIVIDE`; label any approximation in the KPI catalog and dashboard.
