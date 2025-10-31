"""Inspect existing BigQuery dataset to discover available tables"""
from google.cloud import bigquery
import os
import json


def inspect_dataset(project_id: str, dataset_id: str) -> dict:
    """Inspect BigQuery dataset and return information about all tables"""
    client = bigquery.Client(project=project_id)
    dataset_ref = bigquery.DatasetReference(project_id, dataset_id)
    
    print(f"Inspecting dataset: {project_id}.{dataset_id}")
    print("=" * 80)
    
    try:
        # List all tables in the dataset
        tables = list(client.list_tables(dataset_ref))
        
        print(f"\nFound {len(tables)} table(s) in dataset:")
        print("-" * 80)
        
        table_info = {}
        
        for table in tables:
            table_ref = dataset_ref.table(table.table_id)
            full_table = client.get_table(table_ref)
            
            print(f"\nTable: {table.table_id}")
            print(f"  Description: {full_table.description or 'No description'}")
            print(f"  Created: {full_table.created}")
            print(f"  Modified: {full_table.modified}")
            print(f"  Num Rows: {full_table.num_rows:,}")
            print(f"  Num Bytes: {full_table.num_bytes:,}")
            print(f"  Schema Fields: {len(full_table.schema)}")
            
            print("\n  Schema:")
            fields_info = []
            for field in full_table.schema:
                field_info = {
                    "name": field.name,
                    "type": field.field_type,
                    "mode": field.mode,
                    "description": field.description,
                }
                fields_info.append(field_info)
                
                mode_str = f" ({field.mode})" if field.mode != "NULLABLE" else ""
                desc_str = f" - {field.description}" if field.description else ""
                print(f"    - {field.name}: {field.field_type}{mode_str}{desc_str}")
            
            # Sample some data
            print("\n  Sample Data (first 3 rows):")
            try:
                query_job = client.query(f"SELECT * FROM `{project_id}.{dataset_id}.{table.table_id}` LIMIT 3")
                results = query_job.result()
                
                sample_rows = []
                for row in results:
                    row_dict = {}
                    for field in full_table.schema:
                        row_dict[field.name] = row[field.name]
                    sample_rows.append(row_dict)
                
                # Print formatted sample
                if sample_rows:
                    for i, row in enumerate(sample_rows, 1):
                        print(f"    Row {i}:")
                        for key, value in list(row.items())[:5]:  # Show first 5 columns
                            if value is None:
                                print(f"      {key}: None")
                            elif isinstance(value, (list, dict)):
                                print(f"      {key}: {str(value)[:100]}...")
                            else:
                                print(f"      {key}: {str(value)[:100]}")
                        if len(row) > 5:
                            print(f"      ... and {len(row) - 5} more columns")
                else:
                    print("    (Table is empty)")
                    
            except Exception as e:
                print(f"    (Could not fetch sample: {str(e)[:100]})")
                sample_rows = []
            
            table_info[table.table_id] = {
                "description": full_table.description,
                "created": str(full_table.created),
                "modified": str(full_table.modified),
                "num_rows": full_table.num_rows,
                "num_bytes": full_table.num_bytes,
                "schema": fields_info,
                "sample_data": sample_rows,
            }
            
            print()
        
        return {
            "dataset": f"{project_id}.{dataset_id}",
            "tables": table_info,
            "total_tables": len(tables),
        }
        
    except Exception as e:
        print(f"Error inspecting dataset: {e}")
        return {"error": str(e)}


if __name__ == "__main__":
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "483447458116")
    dataset_id = os.getenv("BIGQUERY_DATASET", "wendys_hackathon_data")
    
    print(f"\n{'=' * 80}")
    print("BigQuery Dataset Inspector")
    print(f"{'=' * 80}\n")
    
    result = inspect_dataset(project_id, dataset_id)
    
    print("\n" + "=" * 80)
    print("Summary")
    print("=" * 80)
    print(f"\nDataset: {result.get('dataset', 'N/A')}")
    print(f"Total Tables: {result.get('total_tables', 0)}")
    
    if "tables" in result:
        print("\nTable Names:")
        for table_name in result["tables"].keys():
            num_rows = result["tables"][table_name].get("num_rows", 0)
            print(f"  - {table_name} ({num_rows:,} rows)")
    
    # Save detailed info to JSON file
    output_file = "customer_insights/data/bigquery_tables_info.json"
    with open(output_file, "w") as f:
        json.dump(result, f, indent=2, default=str)
    
    print(f"\nDetailed information saved to: {output_file}")
