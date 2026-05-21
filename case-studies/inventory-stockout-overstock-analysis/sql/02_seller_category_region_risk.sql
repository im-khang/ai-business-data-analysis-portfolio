-- 02_seller_category_region_risk.sql
-- Purpose: seller/category/geography aggregation patterns for operational prioritization.
-- Business question: which sellers, categories, and regions concentrate delivery SLA risk?

WITH order_item_risk AS (
    SELECT
        o.order_id,
        oi.order_item_id,
        oi.seller_id,
        s.seller_state,
        s.seller_city,
        c.customer_state,
        c.customer_city,
        p.product_category_name,
        oi.price,
        oi.freight_value,
        CAST(o.order_delivered_customer_date AS TIMESTAMP) AS customer_delivered_at,
        CAST(o.order_estimated_delivery_date AS TIMESTAMP) AS estimated_delivery_at,
        CASE
            WHEN CAST(o.order_delivered_customer_date AS TIMESTAMP) > CAST(o.order_estimated_delivery_date AS TIMESTAMP) THEN 1
            ELSE 0
        END AS late_delivery_flag
    FROM olist_orders o
    JOIN olist_order_items oi ON o.order_id = oi.order_id
    JOIN olist_sellers s ON oi.seller_id = s.seller_id
    JOIN olist_customers c ON o.customer_id = c.customer_id
    JOIN olist_products p ON oi.product_id = p.product_id
    WHERE o.order_status = 'delivered'
      AND o.order_delivered_customer_date IS NOT NULL
      AND o.order_estimated_delivery_date IS NOT NULL
),
segment_risk AS (
    SELECT
        seller_id,
        seller_state,
        customer_state,
        product_category_name,
        COUNT(DISTINCT order_id) AS orders,
        COUNT(*) AS order_items,
        SUM(price + freight_value) AS gross_item_value,
        COUNT(DISTINCT CASE WHEN late_delivery_flag = 1 THEN order_id END) AS late_orders,
        ROUND(100.0 * COUNT(DISTINCT CASE WHEN late_delivery_flag = 1 THEN order_id END) / NULLIF(COUNT(DISTINCT order_id), 0), 2) AS late_order_rate_pct
    FROM order_item_risk
    GROUP BY seller_id, seller_state, customer_state, product_category_name
)
SELECT
    seller_id,
    seller_state,
    customer_state,
    product_category_name,
    orders,
    order_items,
    gross_item_value,
    late_orders,
    late_order_rate_pct,
    CASE
        WHEN orders >= 50 AND late_order_rate_pct >= 20 THEN 'High priority: recurring SLA risk'
        WHEN orders >= 20 AND late_order_rate_pct >= 10 THEN 'Monitor: emerging SLA risk'
        ELSE 'Lower priority'
    END AS prioritization_label
FROM segment_risk
WHERE orders >= 10
ORDER BY late_order_rate_pct DESC, orders DESC;
