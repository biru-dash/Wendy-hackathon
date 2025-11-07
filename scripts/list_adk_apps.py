#!/usr/bin/env python3
"""
Script to list available ADK apps/agents from the web server.
"""

import requests
import json

ADK_BASE_URL = "http://127.0.0.1:8000"


def test_endpoints():
    """Test various ADK endpoints to find available apps."""
    
    print("=" * 60)
    print("ADK Web Server - Available Apps/Endpoints")
    print("=" * 60)
    
    # Test 1: Root endpoint
    print("\n1. Testing root endpoint (GET /)...")
    try:
        response = requests.get(ADK_BASE_URL, timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"   Response: {json.dumps(data, indent=2)}")
            except:
                print(f"   Response (text): {response.text[:200]}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 2: Apps endpoint
    print("\n2. Testing /apps endpoint...")
    try:
        response = requests.get(f"{ADK_BASE_URL}/apps", timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"   Response: {json.dumps(data, indent=2)}")
            except:
                print(f"   Response (text): {response.text[:200]}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 3: Docs endpoint
    print("\n3. Testing /docs endpoint (OpenAPI)...")
    try:
        response = requests.get(f"{ADK_BASE_URL}/docs", timeout=5)
        print(f"   Status: {response.status_code}")
        print(f"   Visit: {ADK_BASE_URL}/docs to see available endpoints")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 4: Try specific agent paths
    print("\n4. Testing known agent paths...")
    agents = [
        "market_trends_analyst",
        "customer_insights",
        "offer_design",
        "marketing_orchestrator"
    ]
    
    for agent in agents:
        try:
            url = f"{ADK_BASE_URL}/apps/{agent}"
            response = requests.get(url, timeout=5)
            print(f"   {agent}: {response.status_code}")
        except Exception as e:
            print(f"   {agent}: Error - {e}")
    
    print("\n" + "=" * 60)
    print("Recommendation:")
    print("=" * 60)
    print(f"Visit {ADK_BASE_URL}/docs in your browser to see")
    print("the full list of available endpoints and their usage.")


if __name__ == "__main__":
    test_endpoints()

