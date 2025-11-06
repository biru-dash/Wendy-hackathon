"""BigQuery tools for SentimentAnalysisAgent"""
# Load environment variables from .env file
import sys
from pathlib import Path
project_root = Path(__file__).parent.parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
from src.utils.env_loader import load_env
load_env()

from google.adk.tools import FunctionTool
from google.cloud import bigquery
from typing import Dict, Any
import os


def get_bigquery_client() -> bigquery.Client:
    """Get BigQuery client with credentials"""
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    
    if credentials_path:
        client = bigquery.Client.from_service_account_json(credentials_path, project=project_id)
    else:
        client = bigquery.Client(project=project_id)
    
    return client


def feedback_database_tool(
    query: str,
    dataset_id: str,
    table_name: str
) -> Dict[str, Any]:
    """
    Query past campaign feedback, reviews, and social comments.
    
    This tool queries both:
    - feedback_data: Structured feedback with sentiment scores, key phrases, segments (2K rows)
    - customer_feedback_raw: Raw feedback text with ratings (1K rows)
    
    The tool auto-selects the best table based on query content, or use table_name parameter.
    
    Args:
        query: SQL query string or natural language query.
               Examples:
               - "SELECT review_text, sentiment_score FROM feedback_data WHERE offer_type='BOGO'"
               - "Find feedback for app-exclusive offers"
               - "Get sentiment for value-driven-lunch-buyer segment"
               - "Extract key phrases from positive reviews"
        dataset_id: BigQuery dataset ID (typically: "wendys_hackathon_data")
        table_name: BigQuery table name - 'feedback_data' or 'customer_feedback_raw' (typically: "feedback_data")
    
    Returns:
        Dictionary containing:
        - rows: List of query results with review_text, sentiment_score, key_phrases
        - columns: Column names
        - row_count: Number of rows returned
        - query_executed: The SQL query that was executed
        - extracted_phrases: Unique key phrases found across results
        - avg_sentiment: Average sentiment score across results
    """
    client = get_bigquery_client()
    project_id = client.project
    
    # Set defaults if not provided
    dataset = dataset_id if dataset_id else "wendys_hackathon_data"
    primary_table = table_name if table_name else "feedback_data"
    
    # Auto-select table based on query content if not specified
    if not table_name:
        if "rating" in query.lower() or "raw" in query.lower():
            primary_table = "customer_feedback_raw"
        elif "sentiment" in query.lower() or "key_phrases" in query.lower() or "segment" in query.lower():
            primary_table = "feedback_data"
    
    # Handle natural language queries
    if not query.strip().upper().startswith("SELECT"):
        if primary_table == "customer_feedback_raw":
            sql_query = f"""
            SELECT 
                feedback_id,
                customer_id,
                feedback_date,
                rating,
                feedback_text
            FROM `{project_id}.{dataset}.{primary_table}`
            WHERE 
                feedback_text LIKE '%{query}%'
            ORDER BY rating DESC, feedback_date DESC
            LIMIT 100
            """
        else:
            sql_query = f"""
            SELECT 
                feedback_id,
                segment_id,
                offer_type,
                review_text,
                sentiment_score,
                key_phrases,
                source,
                channel
            FROM `{project_id}.{dataset}.{primary_table}`
            WHERE 
                review_text LIKE '%{query}%' 
                OR offer_type LIKE '%{query}%'
                OR segment_id LIKE '%{query}%'
            ORDER BY sentiment_score DESC
            LIMIT 100
            """
    else:
        sql_query = query.replace("{table}", f"`{project_id}.{dataset}.{primary_table}`")
        if f"{project_id}.{dataset}" not in sql_query:
            sql_query = sql_query.replace("FROM feedback_data", f"FROM `{project_id}.{dataset}.feedback_data`")
            sql_query = sql_query.replace("FROM customer_feedback_raw", f"FROM `{project_id}.{dataset}.customer_feedback_raw`")
            sql_query = sql_query.replace("FROM reviews", f"FROM `{project_id}.{dataset}.feedback_data`")
    
    try:
        query_job = client.query(sql_query)
        results = query_job.result()
        
        rows = []
        columns = [field.name for field in results.schema]
        all_phrases = set()
        
        for row in results:
            row_dict = {}
            for col in columns:
                value = row[col]
                if col == "key_phrases" and value:
                    # Handle repeated field (array)
                    if isinstance(value, list):
                        all_phrases.update(value)
                    elif isinstance(value, str):
                        # Split if it's a string representation
                        phrases = [p.strip() for p in value.split(",")]
                        all_phrases.update(phrases)
                        value = phrases
                row_dict[col] = value
            rows.append(row_dict)
        
        return {
            "rows": rows,
            "columns": columns,
            "row_count": len(rows),
            "query_executed": sql_query,
            "extracted_phrases": list(all_phrases),
            "avg_sentiment": sum(r.get("sentiment_score", 0) or 0 for r in rows) / len(rows) if rows else 0,
        }
    except Exception as e:
        return {
            "error": str(e),
            "query_executed": sql_query,
            "rows": [],
            "columns": [],
            "row_count": 0,
            "extracted_phrases": [],
            "avg_sentiment": 0,
        }


# Wrap function with FunctionTool for ADK
feedback_database_tool = FunctionTool(feedback_database_tool)