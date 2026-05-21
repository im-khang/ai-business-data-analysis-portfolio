-- 01_delivery_sla_metrics.sql
-- Purpose: delivery SLA KPI patterns using order timestamps and estimated delivery date.
-- Business question: where did delivery miss customer promise, and by how many days?

WITH delivered_orders AS (
    SELECT
        o.order_id,
        o.customer_id,
        o.order_status,
        CAST(o.order_purchase_timestamp AS TIMESTAMP) AS purchased_at,
        CAST(o.order_approved_at AS TIMESTAMP) AS approved_at,
        CAST(o.order_delivered_carrier_date AS TIMESTAMP) AS carrier_delivered_at,
        CAST(o.order_delivered_customer_date AS TIMESTAMP) AS customer_delivered_at,
        CAST(o.order_estimated_delivery_date AS TIMESTAMP) AS estimated_delivery_at
    FROM olist_orders o
    WHERE o.order_status = 'delivered'
      AND o.order_delivered_customer_date IS NOT NULL
      AND o.order_estimated_delivery_date IS NOT NULL
),
delivery_metrics AS (
    SELECT
        order_id,
        customer_id,
        purchased_at,
        approved_at,
        carrier_delivered_at,
        customer_delivered_at,
        estimated_delivery_at,
        -- DATE_DIFF shown in DuckDB style. Postgres example: DATE_PART('day', customer_delivered_at - purchased_at).
        DATE_DIFF('day', purchased_at, customer_delivered_at) AS total_delivery_days,
        DATE_DIFF('day', approved_at, carrier_delivered_at) AS fulfillment_lead_days,
        DATE_DIFF('day', carrier_delivered_at, customer_delivered_at) AS carrier_transit_days,
        DATE_DIFF('day', estimated_delivery_at, customer_delivered_at) AS days_late,
        CASE WHEN customer_delivered_at > estimated_delivery_at THEN 1 ELSE 0 END AS late_delivery_flag
    FROM delivered_orders
)
SELECT
    COUNT(*) AS delivered_orders,
    SUM(late_delivery_flag) AS late_orders,
    ROUND(100.0 * SUM(late_delivery_flag) / NULLIF(COUNT(*), 0), 2) AS late_delivery_rate_pct,
    AVG(total_delivery_days) AS avg_total_delivery_days,
    AVG(fulfillment_lead_days) AS avg_fulfillment_lead_days,
    AVG(carrier_transit_days) AS avg_carrier_transit_days,
    AVG(CASE WHEN late_delivery_flag = 1 THEN days_late END) AS avg_days_late_when_late
FROM delivery_metrics;
