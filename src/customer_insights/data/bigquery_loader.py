"""Load synthetic data into BigQuery"""
# Load environment variables from .env file
import sys
from pathlib import Path
project_root = Path(__file__).parent.parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
from src.utils.env_loader import load_env
load_env()

from google.cloud import bigquery
from google.cloud.exceptions import NotFound
import pandas as pd
from typing import Dict, Optional
from .bigquery_schemas import TABLE_CONFIGS
from .synthetic_data_generator import export_to_dataframes
import os


def get_or_create_dataset(client: bigquery.Client, dataset_id: str, project_id: str) -> bigquery.Dataset:
    """Get existing dataset or create a new one"""
    dataset_ref = bigquery.DatasetReference(project_id, dataset_id)
    
    try:
        dataset = client.get_dataset(dataset_ref)
        print(f"Dataset {dataset_id} already exists.")
        return dataset
    except NotFound:
        print(f"Creating dataset {dataset_id}...")
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = "US"  # Change to your preferred location
        dataset = client.create_dataset(dataset, timeout=30)
        print(f"Dataset {dataset_id} created successfully.")
        return dataset


def create_table_if_not_exists(
    client: bigquery.Client,
    project_id: str,
    dataset_id: str,
    table_name: str,
    schema: list,
    description: str = "",
) -> bigquery.Table:
    """Create a BigQuery table if it doesn't exist"""
    table_ref = bigquery.TableReference(
        bigquery.DatasetReference(project_id, dataset_id),
        table_name
    )
    table = bigquery.Table(table_ref, schema=schema)
    
    try:
        table = client.get_table(table_ref)
        print(f"Table {table_name} already exists.")
        
        # Option to delete and recreate (uncomment if needed)
        # print(f"Deleting existing table {table_name}...")
        # client.delete_table(table_ref)
        # table = client.create_table(table)
        # print(f"Table {table_name} recreated.")
        
        return table
    except NotFound:
        print(f"Creating table {table_name}...")
        table.description = description
        table = client.create_table(table)
        print(f"Table {table_name} created successfully.")
        return table


def load_dataframe_to_bigquery(
    client: bigquery.Client,
    df: pd.DataFrame,
    project_id: str,
    dataset_id: str,
    table_name: str,
    write_disposition: str = "WRITE_TRUNCATE",  # or "WRITE_APPEND"
) -> None:
    """Load a pandas DataFrame into BigQuery"""
    table_ref = bigquery.TableReference(
        bigquery.DatasetReference(project_id, dataset_id),
        table_name
    )
    
    print(f"Loading data into {project_id}.{dataset_id}.{table_name}...")
    print(f"  Rows: {len(df)}")
    print(f"  Write mode: {write_disposition}")
    
    job_config = bigquery.LoadJobConfig(
        write_disposition=write_disposition,
    )
    
    # Convert dataframe to BigQuery format
    # Handle repeated fields (arrays) specially
    if table_name == "feedback_data" and "key_phrases" in df.columns:
        # Convert list column to proper format
        df = df.copy()
        df["key_phrases"] = df["key_phrases"].apply(
            lambda x: x if isinstance(x, list) else [x] if pd.notna(x) else []
        )
    
    job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
    job.result()  # Wait for the job to complete
    
    print(f"Successfully loaded {len(df)} rows into {project_id}.{dataset_id}.{table_name}")


def load_all_synthetic_data(
    project_id: str,
    dataset_id: str = "wendys_hackathon_data",
    credentials_path: Optional[str] = None,
) -> None:
    """Generate synthetic data and load it into BigQuery"""
    
    # Initialize BigQuery client
    if credentials_path:
        client = bigquery.Client.from_service_account_json(credentials_path, project=project_id)
    else:
        # Use default credentials from environment
        client = bigquery.Client(project=project_id)
    
    # Create dataset
    get_or_create_dataset(client, dataset_id, project_id)
    
    # Generate synthetic data
    print("\n=== Generating Synthetic Data ===")
    dataframes = export_to_dataframes()
    
    # Load each table
    print("\n=== Loading Data into BigQuery ===")
    
    for table_name, config in TABLE_CONFIGS.items():
        if table_name in dataframes:
            df = dataframes[table_name]

            # Normalize datetime columns
            datetime_columns = {
                "crm_data": ["visit_date"],
                "customer_transactions_raw": ["transaction_date"],
                "redemption_logs": ["redemption_date"],
                "feedback_data": ["feedback_date"],
                "customer_feedback_raw": ["feedback_date"],
                "customer_segments": ["created_at"],
            }.get(table_name, [])

            for column in datetime_columns:
                if column in df.columns:
                    df[column] = pd.to_datetime(df[column])

            # Normalize repeated field columns
            repeated_columns = {
                "customer_transactions_raw": ["items"],
                "feedback_data": ["key_phrases"],
                "customer_feedback_raw": [],
                "customer_segments": [
                    "preferred_mechanics",
                    "key_messaging_phrases",
                    "top_time_periods",
                    "dominant_dayparts",
                ],
            }.get(table_name, [])

            if repeated_columns:
                df = df.copy()
                for column in repeated_columns:
                    if column in df.columns:
                        df[column] = df[column].apply(
                            lambda value: value if isinstance(value, list) else ([] if pd.isna(value) else [value])
                        )

            # Create or update table
            create_table_if_not_exists(
                client,
                project_id,
                dataset_id,
                table_name,
                config["schema"],
                config["description"],
            )

            # Load data
            load_dataframe_to_bigquery(
                client,
                df,
                project_id,
                dataset_id,
                table_name,
                write_disposition="WRITE_TRUNCATE",  # Change to "WRITE_APPEND" to add more data
            )
    
    print("\n=== Data Loading Complete ===")
    print(f"All tables are available at: {project_id}.{dataset_id}")


if __name__ == "__main__":
    # Example usage
    import sys
    
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT") or input("Enter your Google Cloud Project ID: ")
    dataset_id = os.getenv("BIGQUERY_DATASET", "wendys_hackathon_data")
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    
    if not project_id:
        print("Error: Please set GOOGLE_CLOUD_PROJECT environment variable or enter project ID")
        sys.exit(1)
    
    load_all_synthetic_data(
        project_id=project_id,
        dataset_id=dataset_id,
        credentials_path=credentials_path,
    )
