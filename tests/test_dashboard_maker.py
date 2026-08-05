import json
import tempfile
import unittest
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from tools.dashboard_maker import DashboardMakerError, build_link, lint_sql, validate_request


ROOT = Path(__file__).resolve().parents[1]


class DashboardMakerTests(unittest.TestCase):
    def setUp(self):
        self.request = json.loads((ROOT / "examples/DB-104/request.json").read_text())
        self.catalog = json.loads((ROOT / "catalog/kpi-catalog.json").read_text())
        self.registry = json.loads((ROOT / "templates/template-registry.json").read_text())

    def test_example_request_is_valid(self):
        self.assertEqual([], validate_request(self.request, self.catalog, self.registry))

    def test_unknown_kpi_is_rejected(self):
        self.request["kpis"].append("invented_metric")
        errors = validate_request(self.request, self.catalog, self.registry)
        self.assertIn("KPIs are not certified: invented_metric", errors)

    def test_link_contains_bigquery_configuration(self):
        template = {
            "id": "operational-performance",
            "version": "1.0.0",
            "status": "active",
            "report_id": "abc123",
            "data_source_alias": "ds0_main",
        }
        link = build_link(template, "Weekly Sales", "acme-prod", "analytics_curated", "vw_sales_daily")
        query = parse_qs(urlparse(link).query)
        self.assertEqual(["abc123"], query["c.reportId"])
        self.assertEqual(["bigQuery"], query["ds.ds0_main.connector"])
        self.assertEqual(["vw_sales_daily"], query["ds.ds0_main.tableId"])

    def test_placeholder_template_is_rejected(self):
        with self.assertRaises(DashboardMakerError):
            build_link(
                {"status": "active", "report_id": "REPLACE_WITH_ID"},
                "Weekly Sales",
                "acme-prod",
                "analytics_curated",
                "vw_sales_daily",
            )

    def test_sql_lint_detects_unbounded_select_star(self):
        issues = lint_sql("SELECT * FROM `acme-prod.sales_raw.fct_orders`", "order_date")
        self.assertIn("Avoid SELECT *; enumerate columns in dashboard models.", issues)
        self.assertIn("Partition column 'order_date' is not referenced.", issues)
        self.assertIn("No WHERE clause found; partition pruning cannot be demonstrated.", issues)


if __name__ == "__main__":
    unittest.main()
