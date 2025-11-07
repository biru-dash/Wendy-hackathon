#!/usr/bin/env python3
"""
Simple script to test connectivity to the ADK web server.

This helps verify that the ADK server is running and accessible
before attempting to use the Streamlit UI.

Usage:
    python scripts/test_adk_connectivity.py
"""

import sys
import requests

ADK_BASE_URL = "http://127.0.0.1:8000"


def test_health_endpoint():
    """Test the /health endpoint if it exists."""
    try:
        print(f"Testing {ADK_BASE_URL}/health ...")
        response = requests.get(f"{ADK_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print(f"✅ Health endpoint OK: {response.status_code}")
            return True
        else:
            print(f"⚠️  Health endpoint returned: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Health endpoint failed: {e}")
        return False


def test_base_url():
    """Test the base URL to see if server is responding."""
    try:
        print(f"\nTesting {ADK_BASE_URL} ...")
        response = requests.get(ADK_BASE_URL, timeout=5)
        if response.status_code in (200, 404):
            print(f"✅ Base URL responding: {response.status_code}")
            return True
        else:
            print(f"⚠️  Base URL returned: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot connect to {ADK_BASE_URL}")
        print(f"\n💡 Make sure the ADK server is running:")
        print(f"   Run: adk web")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection failed: {e}")
        return False


def test_run_endpoint():
    """Test if the /run endpoint exists (without actually running anything)."""
    try:
        print(f"\nTesting {ADK_BASE_URL}/run endpoint (OPTIONS request)...")
        response = requests.options(f"{ADK_BASE_URL}/run", timeout=5)
        print(f"✅ /run endpoint exists: {response.status_code}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"⚠️  Could not verify /run endpoint: {e}")
        return False


def main():
    """Run all connectivity tests."""
    print("=" * 60)
    print("ADK Web Server Connectivity Test")
    print("=" * 60)
    
    results = []
    
    # Test health endpoint
    results.append(test_health_endpoint())
    
    # Test base URL
    results.append(test_base_url())
    
    # Test run endpoint
    results.append(test_run_endpoint())
    
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    
    if any(results):
        print("✅ ADK server is reachable!")
        print("\nYou can now start the Streamlit app:")
        print("   streamlit run ui/hackathon_ui.py")
        return 0
    else:
        print("❌ ADK server is not reachable")
        print("\n💡 To start the ADK server, run:")
        print("   adk web")
        print("\n   Then run this test again.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

