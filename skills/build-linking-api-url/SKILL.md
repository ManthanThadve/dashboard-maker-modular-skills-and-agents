---
name: build-linking-api-url
description: Generate and validate a Looker Studio Linking API URL for an approved template and curated BigQuery asset. Use after template selection and before the BI analyst creates a controlled report copy.
---

# Build Linking API URL

Read `templates/template-registry.json` and the approved dashboard specification.

## Workflow

1. Verify the requested template version is `active`, has a real report ID, and has the expected source alias.
2. Verify the requested BigQuery project, dataset, and table/view are approved curated assets.
3. Build the URL with report ID, report name, edit mode, BigQuery connector, alias, project, dataset, and table/view.
4. Record the URL in `linking-url.txt` without credentials or tokens.

## Command

Use `tools/dashboard_maker.py build-link`. The command refuses draft templates and placeholder IDs.

## Rules

- Do not add credentials, service-account keys, or user tokens to the URL or repository.
- Explain that the BI analyst must open the URL, select **Edit and share**, verify credentials, and complete manual assembly.
- A valid link does not grant access; document required template, source, and group permissions.
