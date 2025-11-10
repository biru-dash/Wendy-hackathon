"""BigQuery table schemas for Customer Insights data"""
from google.cloud import bigquery

# Schema definitions for BigQuery tables

CRM_TABLE_SCHEMA = [
    bigquery.SchemaField("customer_id", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("segment_id", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("visit_date", "TIMESTAMP", mode="REQUIRED"),
    bigquery.SchemaField("spend", "FLOAT", mode="REQUIRED"),
    bigquery.SchemaField("channel", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("preferred_time", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("total_lifetime_visits", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("total_lifetime_spend", "FLOAT", mode="NULLABLE"),
    bigquery.SchemaField("birth_year", "INTEGER", mode="REQUIRED"),
    bigquery.SchemaField("age", "INTEGER", mode="REQUIRED"),
    bigquery.SchemaField("generation", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("is_gen_z", "BOOLEAN", mode="REQUIRED"),
    bigquery.SchemaField("time_period", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("visit_daypart", "STRING", mode="REQUIRED"),
]

CUSTOMER_TRANSACTIONS_RAW_SCHEMA = [
    bigquery.SchemaField("transaction_id", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("customer_id", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("segment_id", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("transaction_date", "TIMESTAMP", mode="REQUIRED"),
    bigquery.SchemaField("total_spend", "FLOAT", mode="REQUIRED"),
    bigquery.SchemaField("channel", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("redeemed_offer", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("offer_type", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("payment_method", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("items", "STRING", mode="REPEATED"),
    bigquery.SchemaField("visit_daypart", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("birth_year", "INTEGER", mode="REQUIRED"),
    bigquery.SchemaField("age", "INTEGER", mode="REQUIRED"),
    bigquery.SchemaField("generation", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("is_gen_z", "BOOLEAN", mode="REQUIRED"),
    bigquery.SchemaField("time_period", "STRING", mode="REQUIRED"),
]

REDEMPTION_LOGS_TABLE_SCHEMA = [
    bigquery.SchemaField("redemption_id", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("customer_id", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("segment_id", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("offer_type", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("redemption_date", "TIMESTAMP", mode="REQUIRED"),
    bigquery.SchemaField("channel", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("is_time_boxed", "BOOLEAN", mode="REQUIRED"),
    bigquery.SchemaField("is_app_exclusive", "BOOLEAN", mode="REQUIRED"),
    bigquery.SchemaField("lift_multiplier", "FLOAT", mode="REQUIRED"),
    bigquery.SchemaField("redemption_value", "FLOAT", mode="REQUIRED"),
    bigquery.SchemaField("month", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("day_of_week", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("hour", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("time_period", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("daypart", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("birth_year", "INTEGER", mode="REQUIRED"),
    bigquery.SchemaField("age", "INTEGER", mode="REQUIRED"),
    bigquery.SchemaField("generation", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("is_gen_z", "BOOLEAN", mode="REQUIRED"),
]

FEEDBACK_TABLE_SCHEMA = [
    bigquery.SchemaField("feedback_id", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("customer_id", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("segment_id", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("offer_type", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("feedback_date", "TIMESTAMP", mode="REQUIRED"),
    bigquery.SchemaField("review_text", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("sentiment_score", "FLOAT", mode="REQUIRED"),
    bigquery.SchemaField("key_phrases", "STRING", mode="REPEATED"),  # Array of strings
    bigquery.SchemaField("channel", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("source", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("time_period", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("daypart", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("birth_year", "INTEGER", mode="REQUIRED"),
    bigquery.SchemaField("age", "INTEGER", mode="REQUIRED"),
    bigquery.SchemaField("generation", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("is_gen_z", "BOOLEAN", mode="REQUIRED"),
]

CUSTOMER_FEEDBACK_RAW_SCHEMA = [
    bigquery.SchemaField("feedback_id", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("customer_id", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("segment_id", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("feedback_date", "TIMESTAMP", mode="REQUIRED"),
    bigquery.SchemaField("rating", "INTEGER", mode="REQUIRED"),
    bigquery.SchemaField("feedback_text", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("channel", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("source", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("time_period", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("daypart", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("birth_year", "INTEGER", mode="REQUIRED"),
    bigquery.SchemaField("age", "INTEGER", mode="REQUIRED"),
    bigquery.SchemaField("generation", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("is_gen_z", "BOOLEAN", mode="REQUIRED"),
]

CUSTOMER_SEGMENTS_SCHEMA = [
    bigquery.SchemaField("segment_id", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("description", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("preferred_mechanics", "STRING", mode="REPEATED"),
    bigquery.SchemaField("key_messaging_phrases", "STRING", mode="REPEATED"),
    bigquery.SchemaField("redemption_rate", "FLOAT", mode="NULLABLE"),
    bigquery.SchemaField("lift_estimate", "FLOAT", mode="NULLABLE"),
    bigquery.SchemaField("empirical_metrics", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("created_at", "TIMESTAMP", mode="NULLABLE"),
    bigquery.SchemaField("primary_generation", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("gen_z_share", "FLOAT", mode="NULLABLE"),
    bigquery.SchemaField("top_time_periods", "STRING", mode="REPEATED"),
    bigquery.SchemaField("dominant_dayparts", "STRING", mode="REPEATED"),
]

# Table configuration
TABLE_CONFIGS = {
    "crm_data": {
        "schema": CRM_TABLE_SCHEMA,
        "description": "CRM and loyalty customer visit data",
        "table_id": "crm_data",
    },
    "customer_transactions_raw": {
        "schema": CUSTOMER_TRANSACTIONS_RAW_SCHEMA,
        "description": "Raw transactional records with offer redemptions",
        "table_id": "customer_transactions_raw",
    },
    "redemption_logs": {
        "schema": REDEMPTION_LOGS_TABLE_SCHEMA,
        "description": "Redemption logs and offer history",
        "table_id": "redemption_logs",
    },
    "feedback_data": {
        "schema": FEEDBACK_TABLE_SCHEMA,
        "description": "Customer feedback, reviews, and sentiment data",
        "table_id": "feedback_data",
    },
    "customer_feedback_raw": {
        "schema": CUSTOMER_FEEDBACK_RAW_SCHEMA,
        "description": "Raw customer feedback verbatims with ratings",
        "table_id": "customer_feedback_raw",
    },
    "customer_segments": {
        "schema": CUSTOMER_SEGMENTS_SCHEMA,
        "description": "Synthesized customer segment insights",
        "table_id": "customer_segments",
    },
}
