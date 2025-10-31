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
]

# Table configuration
TABLE_CONFIGS = {
    "crm_data": {
        "schema": CRM_TABLE_SCHEMA,
        "description": "CRM and loyalty customer visit data",
        "table_id": "crm_data",
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
}
