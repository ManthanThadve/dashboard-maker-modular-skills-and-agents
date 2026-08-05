-- Run with query parameters @start_date and @end_date of type DATE.
-- This validates a business-agreed period without scanning outside the source partition range.

WITH raw AS (
  SELECT
    COUNT(*) AS completed_orders,
    COUNT(DISTINCT customer_id) AS unique_customers,
    SUM(net_revenue) AS net_revenue,
    SUM(gross_margin) AS gross_margin
  FROM `acme-prod.sales_raw.fct_orders`
  WHERE order_date BETWEEN @start_date AND @end_date
    AND order_status = 'COMPLETED'
),
curated AS (
  SELECT
    SUM(completed_orders) AS completed_orders,
    COUNT(DISTINCT customer_id) AS unique_customers,
    SUM(net_revenue) AS net_revenue,
    SUM(gross_margin) AS gross_margin
  FROM `acme-prod.analytics_curated.vw_sales_completed_orders`
  WHERE metric_date BETWEEN @start_date AND @end_date
)
SELECT
  raw.completed_orders = curated.completed_orders AS completed_orders_match,
  raw.unique_customers = curated.unique_customers AS unique_customers_match,
  ABS(raw.net_revenue - curated.net_revenue) <= 0.01 AS net_revenue_match,
  ABS(raw.gross_margin - curated.gross_margin) <= 0.01 AS gross_margin_match,
  raw.completed_orders,
  curated.completed_orders,
  raw.unique_customers,
  curated.unique_customers,
  raw.net_revenue,
  curated.net_revenue
FROM raw
CROSS JOIN curated;
