"""
Quick test script to find the correct ADK API endpoint
Run this while ADK server is running to discover the correct endpoint format
"""
import requests
import json

BASE_URL = "http://localhost:8000"
USER_ID = "test-user"
SESSION_ID = "test-session"
APP_NAME = "marketing_orchestrator"

# Test different endpoint formats
endpoints_to_test = [
    f"/apps/{APP_NAME}/users/{USER_ID}/sessions/{SESSION_ID}",
    f"/apps/{APP_NAME}:run",
    f"/apps/{APP_NAME}/run",
    f"/run",
    f"/api/v1/apps/{APP_NAME}/run",
    f"/{APP_NAME}/run",
]

payload = {
    "new_message": {
        "parts": [{"text": "Test query"}]
    }
}

print("Testing ADK API endpoint formats...")
print("=" * 60)

for endpoint in endpoints_to_test:
    url = f"{BASE_URL}{endpoint}"
    try:
        print(f"\nTesting: {url}")
        response = requests.post(url, json=payload, timeout=5)
        print(f"  Status: {response.status_code}")
        if response.status_code == 200:
            print(f"  ✅ SUCCESS! This endpoint works!")
            print(f"  Response: {response.text[:200]}")
            break
        elif response.status_code == 404:
            print(f"  ❌ Not Found (404)")
        elif response.status_code == 405:
            print(f"  ⚠️  Method Not Allowed (405) - try GET")
            try:
                get_response = requests.get(url, timeout=5)
                print(f"     GET Status: {get_response.status_code}")
            except:
                pass
        else:
            print(f"  ⚠️  Status: {response.status_code}")
            print(f"  Response: {response.text[:200]}")
    except requests.exceptions.ConnectionError:
        print(f"  ❌ Connection Error - Is ADK server running?")
    except Exception as e:
        print(f"  ❌ Error: {e}")

print("\n" + "=" * 60)
print("\nIf none worked, check ADK documentation or run:")
print(f"  curl -X POST {BASE_URL}/apps/{APP_NAME}/users/{USER_ID}/sessions/{SESSION_ID} -H 'Content-Type: application/json' -d '{json.dumps(payload)}'")

