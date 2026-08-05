-- Asset: acme-prod.analytics_curated.vw_sales_completed_orders
-- Grain: one row per completed order. Retaining customer_id preserves correct
-- COUNT_DISTINCT(customer_id) results for arbitrary Looker Studio date ranges.
-- Cost notes:
--   * order_date is the partition column and is filtered directly.
--   * Bind the Looker Studio date-range control to metric_date.
--   * Materialize a partitioned mart if the view's measured refresh cost exceeds
--     the agreed dashboard byte budget.

CREATE OR REPLACE VIEW `acme-prod.analytics_curated.vw_sales_completed_orders` AS
SELECT
  order_id,
  customer_id,
  order_date AS metric_date,
  region,
  channel,
  1 AS completed_orders,
  net_revenue,
  gross_margin
FROM `acme-prod.sales_raw.fct_orders`
WHERE order_date >= DATE_SUB(CURRENT_DATE('Asia/Kolkata'), INTERVAL 730 DAY)
  AND order_status = 'COMPLETED';
