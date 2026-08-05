#!/usr/bin/env python3
"""Validate Dashboard Maker manifests and generate a Looker Studio Linking API URL.

This tool intentionally has no cloud SDK dependency and never executes BigQuery SQL.
It is a pre-review aid, not a deployment tool.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlencode


class DashboardMakerError(ValueError):
    """Raised when a package violates the local governance contract."""


IDENTIFIER = re.compile(r"^[A-Za-z0-9_.-]+$")
REQUIRED_REQUEST_FIELDS = {
    "request_id",
    "title",
    "audience",
    "decision_supported",
    "template_family",
    "time_grain",
    "freshness_sla",
    "dashboard_filters",
    "kpis",
    "acceptance_examples",
}


def load_json(path: str | Path) -> dict:
    try:
        with Path(path).open(encoding="utf-8") as handle:
            return json.load(handle)
    except FileNotFoundError as error:
        raise DashboardMakerError(f"File not found: {path}") from error
    except json.JSONDecodeError as error:
        raise DashboardMakerError(f"Invalid JSON in {path}: {error.msg}") from error


def find_template(registry: dict, reference: str) -> dict:
    if "@" not in reference:
        raise DashboardMakerError("Template reference must be '<template-id>@<version>'.")
    template_id, version = reference.rsplit("@", 1)
    for template in registry.get("templates", []):
        if template.get("id") == template_id and template.get("version") == version:
            return template
    raise DashboardMakerError(f"Template not found: {reference}")


def validate_request(request: dict, catalog: dict, registry: dict) -> list[str]:
    errors: list[str] = []
    missing = sorted(REQUIRED_REQUEST_FIELDS - request.keys())
    if missing:
        errors.append("Missing request fields: " + ", ".join(missing))

    for field in ("dashboard_filters", "kpis", "acceptance_examples"):
        if field in request and not request[field]:
            errors.append(f"'{field}' must not be empty.")

    if request.get("open_questions"):
        errors.append("Request has unresolved open_questions and cannot enter model generation.")

    certified = {
        kpi["kpi_id"]
        for kpi in catalog.get("kpis", [])
        if kpi.get("status") == "certified"
    }
    requested_kpis = request.get("kpis", [])
    unknown = sorted(set(requested_kpis) - certified)
    if unknown:
        errors.append("KPIs are not certified: " + ", ".join(unknown))

    template_family = request.get("template_family")
    if template_family and not any(
        template.get("id") == template_family for template in registry.get("templates", [])
    ):
        errors.append(f"No template family exists for '{template_family}'.")
    return errors


def validate_identifier(label: str, value: str) -> None:
    if not IDENTIFIER.fullmatch(value):
        raise DashboardMakerError(f"Invalid {label}: '{value}'. Use letters, numbers, '.', '_' or '-'.")


def build_link(template: dict, report_name: str, project: str, dataset: str, table: str) -> str:
    for label, value in (("project", project), ("dataset", dataset), ("table", table)):
        validate_identifier(label, value)
    report_id = template.get("report_id", "")
    if not report_id or report_id.startswith("REPLACE_"):
        raise DashboardMakerError("Template has no real report_id. Update the registry before generating a link.")
    if template.get("status") != "active":
        raise DashboardMakerError("Template must be active before generating a production linking URL.")

    alias = template.get("data_source_alias", "ds0_main")
    parameters = [
        ("c.reportId", report_id),
        ("r.reportName", report_name),
        ("c.mode", "edit"),
        (f"ds.{alias}.connector", "bigQuery"),
        (f"ds.{alias}.datasourceName", f"{dataset}.{table}"),
        (f"ds.{alias}.projectId", project),
        (f"ds.{alias}.type", "TABLE"),
        (f"ds.{alias}.datasetId", dataset),
        (f"ds.{alias}.tableId", table),
    ]
    return "https://lookerstudio.google.com/reporting/create?" + urlencode(parameters)


def lint_sql(sql: str, partition_column: str | None) -> list[str]:
    """Return pragmatic SQL review warnings, not a full SQL parser."""
    normalized = re.sub(r"\s+", " ", sql, flags=re.MULTILINE).upper()
    issues: list[str] = []
    if re.search(r"\bSELECT\s+\*(?:\s|$)", normalized):
        issues.append("Avoid SELECT *; enumerate columns in dashboard models.")
    if "#LEGACYSQL" in normalized or "USE LEGACY SQL" in normalized:
        issues.append("Use GoogleSQL/Standard SQL, not Legacy SQL.")
    if partition_column and partition_column.upper() not in normalized:
        issues.append(f"Partition column '{partition_column}' is not referenced.")
    if partition_column and "WHERE" not in normalized:
        issues.append("No WHERE clause found; partition pruning cannot be demonstrated.")
    return issues


def command_validate_request(args: argparse.Namespace) -> int:
    errors = validate_request(load_json(args.request), load_json(args.catalog), load_json(args.registry))
    if errors:
        print("INVALID REQUEST PACKAGE", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("VALID REQUEST PACKAGE")
    return 0


def command_build_link(args: argparse.Namespace) -> int:
    template = find_template(load_json(args.registry), args.template)
    link = build_link(template, args.report_name, args.project, args.dataset, args.table)
    if args.output:
        Path(args.output).write_text(link + "\n", encoding="utf-8")
        print(f"Wrote {args.output}")
    else:
        print(link)
    return 0


def command_lint_sql(args: argparse.Namespace) -> int:
    sql = Path(args.sql).read_text(encoding="utf-8")
    issues = lint_sql(sql, args.partition_column)
    if issues:
        print("SQL REVIEW WARNINGS")
        for issue in issues:
            print(f"- {issue}")
        return 1 if args.strict else 0
    print("SQL REVIEW PASSED")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser("validate-request", help="Validate a JSON request against catalog and registry.")
    validate.add_argument("--request", required=True)
    validate.add_argument("--catalog", required=True)
    validate.add_argument("--registry", required=True)
    validate.set_defaults(handler=command_validate_request)

    link = subparsers.add_parser("build-link", help="Build a configured Looker Studio Linking API URL.")
    link.add_argument("--registry", required=True)
    link.add_argument("--template", required=True, help="template-id@version")
    link.add_argument("--report-name", required=True)
    link.add_argument("--project", required=True)
    link.add_argument("--dataset", required=True)
    link.add_argument("--table", required=True)
    link.add_argument("--output", help="Optional file path for the URL.")
    link.set_defaults(handler=command_build_link)

    lint = subparsers.add_parser("lint-sql", help="Run lightweight dashboard SQL safety checks.")
    lint.add_argument("--sql", required=True)
    lint.add_argument("--partition-column")
    lint.add_argument("--strict", action="store_true", help="Return a non-zero exit code for warnings.")
    lint.set_defaults(handler=command_lint_sql)

    try:
        parsed = parser.parse_args()
        return parsed.handler(parsed)
    except DashboardMakerError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
