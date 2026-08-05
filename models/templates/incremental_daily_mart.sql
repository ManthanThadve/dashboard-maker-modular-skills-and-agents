-- Scheduled-query template: replace all UPPERCASE placeholders before review.
-- Use only when profiling shows the order-grain view is too expensive for repeated use.
-- Caveat: do not use this aggregate for unique customers across arbitrary date ranges;
-- retain an order-grain view or use an explicitly designed distinct-count solution.

DECLARE run_date DATE DEFAULT CURRENT_DATE('Asia/Kolkata');
DECLARE backfill_start DATE DEFAULT DATE_SUB(run_date, INTERVAL 14 DAY);

DELETE FROM `PROJECT.analytics_mart.sales_daily`
WHERE metric_date BETWEEN backfill_start AND run_date;

INSERT INTO `PROJECT.analytics_mart.sales_daily` (
  metric_date,
  region,
  channel,
  completed_orders,
  net_revenue,
  gross_margin
)
SELECT
  order_date AS metric_date,
  region,
  channel,
  COUNT(*) AS completed_orders,
  SUM(net_revenue) AS net_revenue,
  SUM(gross_margin) AS gross_margin
FROM `PROJECT.sales_raw.fct_orders`
WHERE order_date BETWEEN backfill_start AND run_date
  AND order_status = 'COMPLETED'
GROUP BY metric_date, region, channel;
