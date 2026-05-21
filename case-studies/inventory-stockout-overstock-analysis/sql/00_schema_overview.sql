-- 00_schema_overview.sql
-- Purpose: document Olist table inventory and key joins for delivery-risk analysis.
-- Dialect note: ANSI-style comments and join logic; adapt types/functions for DuckDB, Postgres, or BigQuery.

-- Core tables:
-- olist_orders_dataset.csv
--   Grain: one row per order_id.
--   Key fields: order_id, customer_id, order_status,
--   order_purchase_timestamp, order_approved_at,
--   order_delivered_carrier_date, order_delivered_customer_date,
--   order_estimated_delivery_date.

-- olist_order_items_dataset.csv
--   Grain: one row per order_id + order_item_id.
--   Key fields: order_id, product_id, seller_id, shipping_limit_date, price, freight_value.

-- olist_customers_dataset.csv
--   Grain: one row per customer_id.
--   Key fields: customer_id, customer_unique_id, customer_city, customer_state, customer_zip_code_prefix.

-- olist_sellers_dataset.csv
--   Grain: one row per seller_id.
--   Key fields: seller_id, seller_city, seller_state, seller_zip_code_prefix.

-- olist_products_dataset.csv
--   Grain: one row per product_id.
--   Key fields: product_id, product_category_name, product_weight_g, product_length_cm, product_height_cm, product_width_cm.

-- olist_order_reviews_dataset.csv
--   Grain: one or more rows per order_id.
--   Key fields: review_id, order_id, review_score, review_comment_title, review_comment_message.
--   Optional: delivery metrics must still work when this table is unavailable.

-- olist_order_payments_dataset.csv
--   Grain: one or more rows per order_id/payment sequence.
--   Key fields: order_id, payment_type, payment_installments, payment_value.

-- Key joins:
-- orders.customer_id = customers.customer_id
-- orders.order_id = order_items.order_id
-- order_items.seller_id = sellers.seller_id
-- order_items.product_id = products.product_id
-- orders.order_id = reviews.order_id
-- orders.order_id = payments.order_id

-- Base analytical grain recommendation:
-- Use order-item grain for seller/category risk; aggregate back to order grain for SLA and review impact.
