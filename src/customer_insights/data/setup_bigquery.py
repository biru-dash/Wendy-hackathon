#!/usr/bin/env python3
"""
Setup script to generate and load synthetic customer insights data into BigQuery.

Usage:
    python -m customer_insights.data.setup_bigquery
    # Or with environment variables:
    GOOGLE_CLOUD_PROJECT=your-project-id python -m customer_insights.data.setup_bigquery
"""

import os
import sys
from bigquery_loader import load_all_synthetic_data


def main():
    """Main setup function"""
    print("=" * 60)
    print("Customer Insights BigQuery Data Setup")
    print("=" * 60)
    print()
    
    # Get project ID
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        project_id = input("Enter your Google Cloud Project ID: ").strip()
        if not project_id:
            print("Error: Project ID is required")
            sys.exit(1)
    
    # Get dataset ID
    dataset_id = os.getenv("BIGQUERY_DATASET", "customer_insights_data")
    
    # Get credentials path (optional)
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    
    print(f"Project ID: {project_id}")
    print(f"Dataset ID: {dataset_id}")
    if credentials_path:
        print(f"Credentials: {credentials_path}")
    else:
        print("Credentials: Using Application Default Credentials")
    print()
    
    confirm = input("Proceed with data generation and loading? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Cancelled.")
        sys.exit(0)
    
    try:
        load_all_synthetic_data(
            project_id=project_id,
            dataset_id=dataset_id,
            credentials_path=credentials_path,
        )
        print()
        print("=" * 60)
        print("✓ Setup Complete!")
        print("=" * 60)
        print(f"\nYour data is now available in BigQuery:")
        print(f"  Project: {project_id}")
        print(f"  Dataset: {dataset_id}")
        print(f"  Tables:")
        print(f"    - crm_data")
        print(f"    - redemption_logs")
        print(f"    - feedback_data")
        print()
        print("You can now use the Customer Insights agent!")
    except Exception as e:
        print(f"\nError: {e}")
        print("\nTroubleshooting:")
        print("1. Verify GOOGLE_CLOUD_PROJECT is set correctly")
        print("2. Check GOOGLE_APPLICATION_CREDENTIALS points to valid service account key")
        print("3. Or run: gcloud auth application-default login")
        print("4. Ensure BigQuery API is enabled in your project")
        sys.exit(1)


if __name__ == "__main__":
    main()
