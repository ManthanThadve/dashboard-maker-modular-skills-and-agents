# Dashboard Request Form

Submit one request per dashboard. A request is ready for the data team only when every required field is complete.

| Field | Required input |
|---|---|
| Request title | Clear business name; avoid implementation wording |
| Decision supported | What action will this dashboard change? |
| Audience and owner | Viewer group and accountable business owner |
| KPIs | Canonical KPI name if known, business definition, desired comparison |
| Dimensions and filters | Breakdowns, default filters, and who needs them |
| Time semantics | Event date, reporting grain, period, timezone, and comparison range |
| Freshness | Required availability and tolerated latency |
| Acceptance examples | At least one expected value or source-of-truth comparison |
| Security | Any restricted audience, row-level access, or export limitation |

The data team converts this form into `request.yaml`; it does not infer missing business definitions.
