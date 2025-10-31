"""BigQuery tools for BehavioralAnalysisAgent"""
from google.adk.tools import FunctionTool
from google.cloud import bigquery
from typing import Dict, Any, Optional
import os
import json


def get_bigquery_client() -> bigquery.Client:
    """Get BigQuery client with credentials"""
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    
    if credentials_path:
        client = bigquery.Client.from_service_account_json(credentials_path, project=project_id)
    else:
        client = bigquery.Client(project=project_id)
    
    return client


def crm_database_tool(
    query: str,
    dataset_id: str,
    table_name: str
) -> Dict[str, Any]:
    """
    Query the Loyalty and CRM database for visits, spend, and segment information.
    
    This tool queries both:
    - crm_data: Comprehensive CRM data with segments, visits, spend (37K+ rows) 
    - customer_transactions_raw: Raw transaction data with offers and channels (2K rows)
    
    The tool auto-selects the best table based on query content, or use table_name parameter.
    
    Args:
        query: SQL query string or natural language query describing what data to retrieve.
               Examples:
               - "SELECT segment_id, AVG(spend) as avg_spend FROM crm_data GROUP BY segment_id"
               - "Find all customers in value-driven-lunch-buyer segment with more than 20 visits"
               - "Get transactions with redeemed offers"
        dataset_id: BigQuery dataset ID (typically: "wendys_hackathon_data")
        table_name: BigQuery table name - 'crm_data' or 'customer_transactions_raw' (typically: "crm_data")
    
    Returns:
        Dictionary containing:
        - rows: List of query results
        - columns: Column names
        - row_count: Number of rows returned
        - query_executed: The SQL query that was executed
    """
    client = get_bigquery_client()
    project_id = client.project
    
    # Determine which table to query based on query content or use specified table
    primary_table = table_name if table_name else "crm_data"
    
    # Auto-select table based on query content if not specified
    if not table_name:
        if "transaction" in query.lower() or "redeemed_offer" in query.lower():
            primary_table = "customer_transactions_raw"
        elif "segment" in query.lower() or "lifetime" in query.lower() or "visit" in query.lower():
            primary_table = "crm_data"
    
    # Set default dataset if not provided
    dataset = dataset_id if dataset_id else "wendys_hackathon_data"
    
    # If query is natural language, try to convert to SQL (simplified)
    if not query.strip().upper().startswith("SELECT"):
        if primary_table == "customer_transactions_raw":
            sql_query = f"""
            SELECT 
                customer_id,
                COUNT(*) as transaction_count,
                AVG(total_spend) as avg_spend,
                COUNT(DISTINCT redeemed_offer) as unique_offers_redeemed,
                channel,
                COUNTIF(redeemed_offer IS NOT NULL) as redemptions_count
            FROM `{project_id}.{dataset}.{primary_table}`
            WHERE customer_id LIKE '%{query}%' OR redeemed_offer LIKE '%{query}%'
            GROUP BY customer_id, channel
            LIMIT 100
            """
        else:
            sql_query = f"""
            SELECT 
                segment_id,
                COUNT(DISTINCT customer_id) as customer_count,
                AVG(spend) as avg_spend,
                COUNT(*) as total_visits,
                AVG(total_lifetime_visits) as avg_lifetime_visits
            FROM `{project_id}.{dataset}.{primary_table}`
            WHERE segment_id LIKE '%{query}%' OR customer_id LIKE '%{query}%'
            GROUP BY segment_id
            LIMIT 100
            """
    else:
        # Replace table name in query if needed
        sql_query = query.replace("{table}", f"`{project_id}.{dataset_id}.{primary_table}`")
        if f"{project_id}.{dataset_id}" not in sql_query:
            # Try to inject table name for common patterns
            sql_query = sql_query.replace("FROM crm_data", f"FROM `{project_id}.{dataset_id}.crm_data`")
            sql_query = sql_query.replace("FROM customer_transactions_raw", f"FROM `{project_id}.{dataset_id}.customer_transactions_raw`")
            sql_query = sql_query.replace("FROM transactions", f"FROM `{project_id}.{dataset_id}.customer_transactions_raw`")
    
    try:
        query_job = client.query(sql_query)
        results = query_job.result()
        
        rows = []
        columns = [field.name for field in results.schema]
        
        for row in results:
            row_dict = {}
            for col in columns:
                row_dict[col] = row[col]
            rows.append(row_dict)
        
        return {
            "rows": rows,
            "columns": columns,
            "row_count": len(rows),
            "query_executed": sql_query,
        }
    except Exception as e:
        return {
            "error": str(e),
            "query_executed": sql_query,
            "rows": [],
            "columns": [],
            "row_count": 0,
        }


def redemption_log_tool(
    query: str,
    dataset_id: str,
    table_name: str
) -> Dict[str, Any]:
    """
    Query Redemption logs and offer history.
    
    This tool executes SQL queries against the BigQuery redemption logs table.
    Supports calculating lift, redemption patterns, and time/channel dependencies.
    
    Args:
        query: SQL query string or natural language query.
               Examples:
               - "CALCULATE lift for 'BOGO' offer WHERE channel='app'"
               - "SELECT offer_type, AVG(lift_multiplier) as avg_lift, COUNT(*) as count FROM redemption_logs WHERE channel='app' GROUP BY offer_type"
               - "Find redemption patterns for value-driven-lunch-buyer segment"
        dataset_id: BigQuery dataset ID (typically: "wendys_hackathon_data")
        table_name: BigQuery table name (typically: "redemption_logs")
    
    Returns:
        Dictionary containing:
        - rows: List of query results
        - columns: Column names
        - row_count: Number of rows returned
        - query_executed: The SQL query that was executed
        - metrics: Calculated metrics if applicable (avg_lift, redemption_rate, etc.)
    """
    client = get_bigquery_client()
    project_id = client.project
    
    # Set defaults if not provided
    dataset = dataset_id if dataset_id else "wendys_hackathon_data"
    table = table_name if table_name else "redemption_logs"
    
    # Handle natural language queries for lift calculation
    if "CALCULATE lift" in query.upper() or "calculate lift" in query.lower():
        # Extract offer type and channel from query
        offer_type = "BOGO"  # default
        channel = None
        
        if "BOGO" in query.upper():
            offer_type = "BOGO"
        elif "time-boxed" in query.lower() or "time_boxed" in query.lower():
            offer_type = "Time-Boxed"
        elif "app" in query.lower():
            offer_type = "App Exclusive"
        
        if "channel='app'" in query or "channel = 'app'" in query:
            channel = "app"
        elif "channel='web'" in query or "channel = 'web'" in query:
            channel = "web"
        
        sql_query = f"""
        SELECT 
            offer_type,
            channel,
            AVG(lift_multiplier) as avg_lift,
            COUNT(*) as redemption_count,
            COUNT(DISTINCT customer_id) as unique_customers,
            AVG(redemption_value) as avg_redemption_value
        FROM `{project_id}.{dataset}.{table}`
        WHERE offer_type = '{offer_type}'
        """
        if channel:
            sql_query += f" AND channel = '{channel}'"
        sql_query += " GROUP BY offer_type, channel"
    elif not query.strip().upper().startswith("SELECT"):
        # Simple natural language conversion
        sql_query = f"""
        SELECT 
            offer_type,
            segment_id,
            channel,
            AVG(lift_multiplier) as avg_lift,
            COUNT(*) as redemption_count
        FROM `{project_id}.{dataset}.{table}`
        WHERE segment_id LIKE '%{query}%' OR offer_type LIKE '%{query}%'
        GROUP BY offer_type, segment_id, channel
        ORDER BY avg_lift DESC
        LIMIT 100
        """
    else:
        sql_query = query.replace("{table}", f"`{project_id}.{dataset}.{table}`")
        if f"{project_id}.{dataset}.{table}" not in sql_query:
            sql_query = sql_query.replace("FROM redemption_logs", f"FROM `{project_id}.{dataset}.{table}`")
    
    try:
        query_job = client.query(sql_query)
        results = query_job.result()
        
        rows = []
        columns = [field.name for field in results.schema]
        
        for row in results:
            row_dict = {}
            for col in columns:
                row_dict[col] = row[col]
            rows.append(row_dict)
        
        # Calculate summary metrics
        metrics = {}
        if rows:
            metrics["avg_lift"] = sum(r.get("avg_lift", 0) or 0 for r in rows) / len(rows)
            metrics["total_redemptions"] = sum(r.get("redemption_count", 0) or 0 for r in rows)
        
        return {
            "rows": rows,
            "columns": columns,
            "row_count": len(rows),
            "query_executed": sql_query,
            "metrics": metrics,
        }
    except Exception as e:
        return {
            "error": str(e),
            "query_executed": sql_query,
            "rows": [],
            "columns": [],
            "row_count": 0,
            "metrics": {},
        }


# Wrap functions with FunctionTool for ADK
crm_database_tool = FunctionTool(crm_database_tool)
redemption_log_tool = FunctionTool(redemption_log_tool)