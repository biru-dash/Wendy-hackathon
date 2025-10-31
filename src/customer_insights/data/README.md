# Customer Insights Synthetic Data & BigQuery Setup

This directory contains utilities for generating synthetic customer data and loading it into BigQuery.

## Files

- `synthetic_data_generator.py`: Generates synthetic CRM, redemption, and feedback data
- `bigquery_schemas.py`: Defines BigQuery table schemas
- `bigquery_loader.py`: Loads synthetic data into BigQuery tables

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Google Cloud Credentials

You need Google Cloud credentials to access BigQuery. Choose one:

**Option A: Service Account Key (Recommended for local dev)**
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"
export GOOGLE_CLOUD_PROJECT="your-project-id"
```

**Option B: Application Default Credentials**
```bash
gcloud auth application-default login
export GOOGLE_CLOUD_PROJECT="your-project-id"
```

### 3. Generate and Load Data

```bash
# From project root
python -m customer_insights.data.bigquery_loader
```

Or set environment variables and run:
```bash
export GOOGLE_CLOUD_PROJECT="your-project-id"
export BIGQUERY_DATASET="customer_insights_data"  # Optional, defaults to customer_insights_data
python -m customer_insights.data.bigquery_loader
```

## Generated Tables

The script creates three BigQuery tables in the `customer_insights_data` dataset:

1. **crm_data**: Customer visit and loyalty data
   - customer_id, segment_id, visit_date, spend, channel, etc.

2. **redemption_logs**: Offer redemption history
   - redemption_id, offer_type, lift_multiplier, channel, etc.

3. **feedback_data**: Customer feedback and reviews
   - feedback_id, review_text, sentiment_score, key_phrases, etc.

## Usage in Agents

The database tools automatically use these tables:
- `crm_database_tool` queries `crm_data`
- `redemption_log_tool` queries `redemption_logs`
- `feedback_database_tool` queries `feedback_data`

## Customizing Data

Edit `synthetic_data_generator.py` to:
- Adjust number of records
- Modify segment definitions
- Change offer types or channels
- Customize synthetic patterns

## Query Examples

The tools support both SQL and natural language queries:

```python
# SQL queries
"SELECT segment_id, AVG(spend) FROM crm_data GROUP BY segment_id"

# Natural language (simplified conversion)
"Find all value-driven-lunch-buyer customers"
"Calculate lift for BOGO offers in app channel"
"Get sentiment for time-boxed offers"
```
