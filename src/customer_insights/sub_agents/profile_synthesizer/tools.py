"""Tools for ProfileSynthesizerAgent to write results back to BigQuery"""
from google.adk.tools import FunctionTool
from google.cloud import bigquery
from typing import Dict, Any, List
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


def save_customer_segments_tool(
    customer_insights: List[Dict[str, Any]],
    dataset_id: str,
    table_name: str
) -> Dict[str, Any]:
    """
    Save synthesized customer insights to BigQuery customer_segments table.
    
    This tool stores the final output from ProfileSynthesizerAgent into BigQuery
    so it can be retrieved later and used by other agents.
    
    Args:
        customer_insights: List of customer insight dictionaries with structure:
            [
                {
                    "segment_id": "value-driven-lunch-buyer",
                    "description": "...",
                    "preferred_mechanics": ["BOGO", "time-boxed"],
                    "key_messaging_phrases": ["time-boxed", "app-exclusive"],
                    "empirical_metrics": {
                        "redemption_rate": "2.3x",
                        "lift_estimate": "2.3x",
                        "segment_size": "15%",
                        "channel_preference": "app"
                    }
                }
            ]
        dataset_id: BigQuery dataset ID (typically: "wendys_hackathon_data")
        table_name: BigQuery table name (typically: "customer_segments")
    
    Returns:
        Dictionary with save results including row count and any errors
    """
    client = get_bigquery_client()
    project_id = client.project
    
    # Set defaults if not provided
    dataset = dataset_id if dataset_id else "wendys_hackathon_data"
    table = table_name if table_name else "customer_segments"
    
    try:
        table_ref = bigquery.TableReference(
            bigquery.DatasetReference(project_id, dataset),
            table
        )
        
        # Prepare rows for insertion
        rows_to_insert = []
        for insight in customer_insights:
            row = {
                "segment_id": insight.get("segment_id", ""),
                "description": insight.get("description", ""),
                "preferred_mechanics": insight.get("preferred_mechanics", []),
                "key_messaging_phrases": insight.get("key_messaging_phrases", []),
            }
            
            # Handle empirical_metrics
            metrics = insight.get("empirical_metrics", {})
            if isinstance(metrics, dict):
                row["redemption_rate"] = _parse_metric(metrics.get("redemption_rate", "0"))
                row["lift_estimate"] = _parse_metric(metrics.get("lift_estimate", "0"))
                row["empirical_metrics"] = json.dumps(metrics)
            else:
                row["redemption_rate"] = None
                row["lift_estimate"] = None
                row["empirical_metrics"] = json.dumps({})
            
            rows_to_insert.append(row)
        
        # Insert rows
        errors = client.insert_rows_json(table_ref, rows_to_insert)
        
        if errors:
            return {
                "success": False,
                "rows_inserted": 0,
                "rows_attempted": len(rows_to_insert),
                "errors": errors,
            }
        else:
            return {
                "success": True,
                "rows_inserted": len(rows_to_insert),
                "rows_attempted": len(rows_to_insert),
                "table": f"{project_id}.{dataset}.{table}",
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "rows_inserted": 0,
        }


def _parse_metric(metric_str: str) -> float:
    """Parse metric string like '2.3x' to float"""
    try:
        if isinstance(metric_str, (int, float)):
            return float(metric_str)
        if "x" in str(metric_str).lower():
            return float(str(metric_str).replace("x", "").replace("X", "").strip())
        return float(metric_str)
    except (ValueError, TypeError):
        return 0.0


# Wrap function with FunctionTool for ADK
save_customer_segments_tool = FunctionTool(save_customer_segments_tool)
