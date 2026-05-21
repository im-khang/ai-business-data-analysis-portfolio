-- 03_inventory_proxy_metrics.sql
-- Purpose: demand velocity and inventory-risk proxy patterns.
-- Important limitation: Olist lacks stock-on-hand, replenishment, purchase order, and warehouse availability fields.
-- Therefore this script does NOT claim direct stockout or overstock measurement.

WITH product_monthly_demand AS (
    SELECT
        p.product_category_name,
        oi.product_id,
        oi.seller_id,
        DATE_TRUNC('month', CAST(o.order_purchase_timestamp AS TIMESTAMP)) AS order_month,
        COUNT(DISTINCT o.order_id) AS orders,
        SUM(COALESCE(oi.price, 0)) AS item_revenue,
        AVG(COALESCE(oi.freight_value, 0)) AS avg_freight_value
    FROM olist_orders o
    JOIN olist_order_items oi ON o.order_id = oi.order_id
    JOIN olist_products p ON oi.product_id = p.product_id
    WHERE o.order_purchase_timestamp IS NOT NULL
      AND o.order_status IN ('delivered', 'shipped', 'invoiced', 'processing')
    GROUP BY p.product_category_name, oi.product_id, oi.seller_id, DATE_TRUNC('month', CAST(o.order_purchase_timestamp AS TIMESTAMP))
),
velocity_proxy AS (
    SELECT
        product_category_name,
        product_id,
        seller_id,
        COUNT(*) AS active_months,
        AVG(orders) AS avg_monthly_orders,
        MAX(orders) AS peak_monthly_orders,
        COALESCE(STDDEV(orders), 0) AS monthly_order_volatility,
        SUM(COALESCE(item_revenue, 0)) AS total_item_revenue
    FROM product_monthly_demand
    GROUP BY product_category_name, product_id, seller_id
),
risk_proxy AS (
    SELECT
        *,
        CASE
            WHEN avg_monthly_orders >= 20 AND COALESCE(monthly_order_volatility, 0) >= 10 THEN 'Stockout-risk proxy: high demand and volatile ordering'
            WHEN avg_monthly_orders <= 1 AND active_months >= 6 THEN 'Overstock-risk proxy: persistent low demand candidate'
            WHEN peak_monthly_orders >= 3 * NULLIF(avg_monthly_orders, 0) THEN 'Forecast-risk proxy: demand spike pattern'
            ELSE 'No strong inventory proxy signal'
        END AS inventory_proxy_label
    FROM velocity_proxy
)
SELECT
    product_category_name,
    product_id,
    seller_id,
    active_months,
    avg_monthly_orders,
    peak_monthly_orders,
    monthly_order_volatility,
    total_item_revenue,
    inventory_proxy_label,
    'Proxy only: requires stock-on-hand, replenishment, lead time, and warehouse data for direct inventory decisioning.' AS limitation_note
FROM risk_proxy
ORDER BY total_item_revenue DESC;
