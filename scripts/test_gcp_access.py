#!/usr/bin/env python3
"""
Test script to verify GCP project access and permissions.
Tests authentication, project access, and BigQuery API availability.

This script reads project details from the .env file in the project root.
You can override the project ID by providing it as a command line argument.

Usage:
    python scripts/test_gcp_access.py
    python scripts/test_gcp_access.py <project-id>
    python scripts/test_gcp_access.py <project-id> <project-number>
"""

import os
import sys
from pathlib import Path

# Add project root to path to import env_loader
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Load environment variables from .env file
from src.utils.env_loader import load_env
load_env()

from google.cloud import bigquery
from google.cloud.exceptions import NotFound, Forbidden
from google.api_core import exceptions
import json


def test_authentication():
    """Test if we can authenticate with GCP"""
    print("=" * 80)
    print("1. Testing Authentication")
    print("=" * 80)
    
    try:
        # Try to create a client without specifying project to test auth
        client = bigquery.Client()
        print("✓ Authentication successful (using Application Default Credentials)")
        
        # Try to get default project
        try:
            default_project = client.project
            print(f"  Default project from credentials: {default_project}")
        except Exception as e:
            print(f"  Could not determine default project: {e}")
        
        return True, client
    except Exception as e:
        print(f"✗ Authentication failed: {e}")
        print("\n  Troubleshooting:")
        print("  - Run: gcloud auth application-default login")
        print("  - Or set GOOGLE_APPLICATION_CREDENTIALS to a service account key file")
        return False, None


def test_project_access(client: bigquery.Client, project_id: str, project_number: str = None):
    """Test if we can access the specified project"""
    print("\n" + "=" * 80)
    print("2. Testing Project Access")
    print("=" * 80)
    print(f"  Project ID: {project_id}")
    if project_number:
        print(f"  Project Number: {project_number}")
    
    try:
        # Try to create a client with the specific project
        project_client = bigquery.Client(project=project_id)
        
        # Try to list datasets (this requires project access)
        print("\n  Attempting to list datasets...")
        datasets = list(project_client.list_datasets())
        print(f"✓ Successfully accessed project '{project_id}'")
        print(f"  Found {len(datasets)} dataset(s) in project")
        
        if datasets:
            print("\n  Existing datasets:")
            for dataset in datasets[:10]:  # Show first 10
                print(f"    - {dataset.dataset_id}")
            if len(datasets) > 10:
                print(f"    ... and {len(datasets) - 10} more")
        else:
            print("  (No datasets found - this is expected if BigQuery hasn't been set up yet)")
        
        return True, project_client
    except Forbidden as e:
        print(f"✗ Access denied to project '{project_id}'")
        print(f"  Error: {e}")
        print("\n  Troubleshooting:")
        print("  - Verify you have access to this project")
        print("  - Check IAM permissions (BigQuery Data Viewer, BigQuery Job User, etc.)")
        return False, None
    except NotFound as e:
        print(f"✗ Project '{project_id}' not found")
        print(f"  Error: {e}")
        return False, None
    except Exception as e:
        print(f"✗ Error accessing project: {e}")
        return False, None


def test_bigquery_api(project_client: bigquery.Client, project_id: str):
    """Test if BigQuery API is enabled and accessible"""
    print("\n" + "=" * 80)
    print("3. Testing BigQuery API")
    print("=" * 80)
    
    try:
        # Try to run a simple query to test API access
        print("  Testing BigQuery API with a simple query...")
        query = "SELECT 1 as test"
        query_job = project_client.query(query)
        results = query_job.result()
        
        # Check if we got results
        for row in results:
            if row.test == 1:
                print("✓ BigQuery API is enabled and accessible")
                print(f"  Query executed successfully")
                return True
        
        print("✗ Query executed but returned unexpected results")
        return False
    except exceptions.PermissionDenied as e:
        print(f"✗ Permission denied: {e}")
        print("\n  Troubleshooting:")
        print("  - BigQuery API may not be enabled")
        print("  - You may not have BigQuery Job User role")
        print("  - Run: gcloud services enable bigquery.googleapis.com --project={project_id}")
        return False
    except Exception as e:
        print(f"✗ Error testing BigQuery API: {e}")
        return False


def test_dataset_permissions(project_client: bigquery.Client, project_id: str, dataset_id: str = "test_dataset"):
    """Test if we can create/access datasets (permissions check)"""
    print("\n" + "=" * 80)
    print("4. Testing Dataset Permissions")
    print("=" * 80)
    
    # Test if we can list datasets (already done, but let's be explicit)
    try:
        print(f"  Checking if we can list datasets...")
        datasets = list(project_client.list_datasets())
        print(f"✓ Can list datasets (found {len(datasets)} dataset(s))")
    except Exception as e:
        print(f"✗ Cannot list datasets: {e}")
        return False
    
    # Test if we can check for a specific dataset
    try:
        print(f"  Testing dataset access permissions...")
        dataset_ref = bigquery.DatasetReference(project_id, dataset_id)
        
        try:
            dataset = project_client.get_dataset(dataset_ref)
            print(f"✓ Can access dataset '{dataset_id}' (it exists)")
            return True
        except NotFound:
            print(f"  Dataset '{dataset_id}' does not exist (this is OK)")
            print("  Testing if we can create datasets...")
            
            # Try to create a test dataset (we'll delete it immediately)
            try:
                test_dataset = bigquery.Dataset(dataset_ref)
                test_dataset.location = "US"
                test_dataset = project_client.create_dataset(test_dataset, timeout=30)
                print(f"✓ Can create datasets (created test dataset '{dataset_id}')")
                
                # Clean up - delete the test dataset
                print(f"  Cleaning up test dataset...")
                project_client.delete_dataset(dataset_ref, delete_contents=True, not_found_ok=True)
                print(f"✓ Test dataset deleted")
                return True
            except Forbidden as e:
                print(f"✗ Cannot create datasets: {e}")
                print("  You may need 'BigQuery Data Editor' or 'BigQuery Admin' role")
                return False
            except Exception as e:
                print(f"✗ Error testing dataset creation: {e}")
                return False
    except Exception as e:
        print(f"✗ Error testing dataset permissions: {e}")
        return False


def test_query_permissions(project_client: bigquery.Client, project_id: str):
    """Test if we can run queries"""
    print("\n" + "=" * 80)
    print("5. Testing Query Permissions")
    print("=" * 80)
    
    try:
        # Test a simple query
        print("  Testing query execution...")
        query = """
        SELECT 
            CURRENT_TIMESTAMP() as current_time,
            'test' as test_string,
            42 as test_number
        """
        query_job = project_client.query(query)
        results = query_job.result()
        
        for row in results:
            print(f"✓ Can execute queries")
            print(f"  Test query result: {row.test_string} = {row.test_number}")
            print(f"  Current time: {row.current_time}")
            return True
        
        return False
    except Exception as e:
        print(f"✗ Cannot execute queries: {e}")
        return False


def get_project_info(project_client: bigquery.Client, project_id: str):
    """Get information about the project"""
    print("\n" + "=" * 80)
    print("6. Project Information")
    print("=" * 80)
    
    try:
        # List all datasets
        datasets = list(project_client.list_datasets())
        
        print(f"  Project ID: {project_id}")
        print(f"  Number of datasets: {len(datasets)}")
        
        if datasets:
            print("\n  Datasets:")
            for dataset in datasets:
                try:
                    full_dataset = project_client.get_dataset(dataset.dataset_id)
                    print(f"    - {dataset.dataset_id}")
                    print(f"      Location: {full_dataset.location}")
                    print(f"      Created: {full_dataset.created}")
                    
                    # List tables in dataset
                    tables = list(project_client.list_tables(full_dataset))
                    print(f"      Tables: {len(tables)}")
                    if tables:
                        for table in tables[:5]:  # Show first 5 tables
                            print(f"        • {table.table_id}")
                        if len(tables) > 5:
                            print(f"        ... and {len(tables) - 5} more")
                except Exception as e:
                    print(f"    - {dataset.dataset_id} (error getting details: {e})")
        else:
            print("  No datasets found (BigQuery setup may be needed)")
        
        return True
    except Exception as e:
        print(f"✗ Error getting project info: {e}")
        return False


def main():
    """Main test function"""
    print("\n" + "=" * 80)
    print("GCP Project Access Test")
    print("=" * 80)
    print()
    
    # Get project details from environment variables (loaded from .env file)
    # Allow override via command line arguments
    if len(sys.argv) > 1:
        project_id = sys.argv[1]
    else:
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        if not project_id:
            print("✗ Error: GOOGLE_CLOUD_PROJECT not found in environment variables")
            print("\n  Please ensure you have:")
            print("  1. Created a .env file from .env.example")
            print("  2. Set GOOGLE_CLOUD_PROJECT in your .env file")
            print("  3. Or provide project ID as command line argument: python test_gcp_access.py <project-id>")
            sys.exit(1)
    
    if len(sys.argv) > 2:
        project_number = sys.argv[2]
    else:
        project_number = os.getenv("GOOGLE_CLOUD_PROJECT_NUMBER")
        # Project number is optional, so we don't fail if it's not set
    
    print(f"Testing access to:")
    print(f"  Project ID: {project_id}")
    if project_number:
        print(f"  Project Number: {project_number}")
    else:
        print(f"  Project Number: (not specified)")
    print()
    
    # Test 1: Authentication
    auth_success, default_client = test_authentication()
    if not auth_success:
        print("\n" + "=" * 80)
        print("SUMMARY: Authentication failed. Please authenticate first.")
        print("=" * 80)
        print("\nTo authenticate, run:")
        print("  gcloud auth application-default login")
        sys.exit(1)
    
    # Test 2: Project Access
    project_access, project_client = test_project_access(default_client, project_id, project_number)
    if not project_access:
        print("\n" + "=" * 80)
        print("SUMMARY: Cannot access project. Check permissions.")
        print("=" * 80)
        sys.exit(1)
    
    # Test 3: BigQuery API
    api_success = test_bigquery_api(project_client, project_id)
    
    # Test 4: Dataset Permissions
    dataset_perms = test_dataset_permissions(project_client, project_id)
    
    # Test 5: Query Permissions
    query_perms = test_query_permissions(project_client, project_id)
    
    # Test 6: Project Info
    get_project_info(project_client, project_id)
    
    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"✓ Authentication: {'PASS' if auth_success else 'FAIL'}")
    print(f"✓ Project Access: {'PASS' if project_access else 'FAIL'}")
    print(f"✓ BigQuery API: {'PASS' if api_success else 'FAIL'}")
    print(f"✓ Dataset Permissions: {'PASS' if dataset_perms else 'FAIL'}")
    print(f"✓ Query Permissions: {'PASS' if query_perms else 'FAIL'}")
    print()
    
    if all([auth_success, project_access, api_success, dataset_perms, query_perms]):
        print("🎉 All tests passed! You have full access to the GCP project.")
        print(f"\nYou can now set up BigQuery datasets using:")
        print(f"  python -m customer_insights.data.setup_bigquery")
        print(f"  (Project ID will be read from your .env file)")
        return 0
    else:
        print("⚠️  Some tests failed. Review the output above for details.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

