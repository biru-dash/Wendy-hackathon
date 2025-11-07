#!/usr/bin/env python3
"""
Test ways to execute an agent after session creation
"""

import requests
import json
import time

ADK_BASE_URL = "http://127.0.0.1:8000"
AGENT_NAME = "market_trends_analyst"
USER_ID = "test-user"
SESSION_ID = f"test-{int(time.time())}"

query = "What breakfast trends are emerging?"

print("=" * 60)
print("Testing Agent Execution Methods")
print("=" * 60)
print(f"\nAgent: {AGENT_NAME}")
print(f"Session ID: {SESSION_ID}")
print()

# Create session first
session_url = f"{ADK_BASE_URL}/apps/{AGENT_NAME}/users/{USER_ID}/sessions/{SESSION_ID}"
payload = {"new_message": {"parts": [{"text": query}]}}

print("Step 1: Creating session...")
response = requests.post(session_url, json=payload, timeout=10)
print(f"Status: {response.status_code}")

if response.status_code in (200, 201):
    print("✅ Session created\n")
    
    # Try different execution methods
    methods = [
        ("POST {session}/execute", f"{session_url}/execute", {}),
        ("POST {session}/run", f"{session_url}/run", {}),
        ("POST {session}:execute", f"{session_url}:execute", {}),
        ("POST {session}:run", f"{session_url}:run", {}),
        ("PUT {session}", session_url, payload),
        ("PATCH {session}", session_url, payload),
        ("POST {session} (again)", session_url, payload),
    ]
    
    for desc, url, body in methods:
        print(f"Trying: {desc}")
        try:
            if "PUT" in desc:
                resp = requests.put(url, json=body, timeout=10)
            elif "PATCH" in desc:
                resp = requests.patch(url, json=body, timeout=10)
            else:
                resp = requests.post(url, json=body, timeout=10)
            
            print(f"  Status: {resp.status_code}")
            if resp.status_code in (200, 201, 202):
                print(f"  ✅ Might work! Response: {resp.text[:100]}")
            elif resp.status_code == 404:
                print(f"  ❌ Not Found")
            else:
                print(f"  ⚠️  {resp.text[:80]}")
        except Exception as e:
            print(f"  ❌ Error: {e}")
        print()
    
    # Check if anything worked
    print("Checking for events...")
    time.sleep(3)
    check_resp = requests.get(session_url, timeout=10)
    if check_resp.status_code == 200:
        data = check_resp.json()
        events = data.get("events", [])
        print(f"Events: {len(events)}")
        if events:
            print(f"✅✅✅ SUCCESS! Agent executed!")
            for event in events[:3]:
                print(f"  - {event.get('type', 'unknown')}")
        else:
            print(f"❌ No events - none of the methods worked")
else:
    print(f"❌ Failed to create session: {response.text[:200]}")

print("\n" + "=" * 60)

