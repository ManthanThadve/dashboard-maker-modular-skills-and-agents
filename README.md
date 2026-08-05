# Dashboard Maker

Dashboard Maker is a Git-backed, human-approved workflow for turning a business request into a governed BigQuery data product and an exact Looker Studio build specification. It does not attempt unsupported autonomous report publishing.

## Included

- Versioned KPI catalog and source allow-list.
- Eight modular Claude Code skills under `skills/`.
- Looker Studio template registry and field contracts.
- A DB-104 end-to-end package with SQL, validation, and dashboard spec.
- A dependency-free Python CLI for validating manifests and generating Linking API URLs.

Human-facing request and dashboard artifacts are YAML. Machine-validated registry and contract artifacts are JSON so the starter kit has no external package dependency.

## Quick start

Use the bundled Python runtime when Python is not on your PATH:

```powershell
$py = 'C:\Users\manth\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
& $py tools/dashboard_maker.py validate-request --request examples/DB-104/request.json --catalog catalog/kpi-catalog.json --registry templates/template-registry.json
& $py -m unittest discover -s tests -v
```

Set a real report ID in `templates/template-registry.json`, then create a reviewable URL:

```powershell
& $py tools/dashboard_maker.py build-link --registry templates/template-registry.json --template operational-performance@1.0.0 --report-name "Weekly Sales Performance" --project YOUR_PROJECT --dataset analytics_curated --table vw_sales_daily
```

The command refuses placeholder template IDs. Open the resulting URL as the BI analyst, select **Edit and share**, assemble the report from `dashboard-spec.yaml`, and complete UAT.

## Repository map

- `catalog/` — certified KPI definitions and source policy.
- `contracts/` — stable field contracts consumed by templates.
- `examples/` — complete request packages used for testing and onboarding.
- `models/` — reviewable BigQuery Standard SQL and validations.
- `skills/` — modular Claude Code instructions.
- `templates/` — template registry and contract mapping.
- `tools/` — safe local utilities; no cloud credentials or writes.
- `docs/` — operating model, architecture, and rollout checklist.

## Safety model

- Agents inspect only allow-listed metadata and curated source definitions.
- Generated SQL is a pull-request artifact; production deployment requires review.
- Looker Studio reports use only approved curated views or marts.
- The Linking API does not bypass BigQuery, Looker Studio, or sharing permissions.
