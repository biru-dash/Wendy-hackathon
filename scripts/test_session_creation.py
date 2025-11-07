#!/usr/bin/env python3
"""
Test different ways to create and execute agents in ADK
"""

import requests
import json
import time

ADK_BASE_URL = "http://127.0.0.1:8000"
AGENT_NAME = "market_trends_analyst"
USER_ID = "test-user"
SESSION_ID = f"test-{int(time.time())}"

query = "What breakfast trends are emerging?"
payload = {"new_message": {"parts": [{"text": query}]}}

print("=" * 60)
print("Testing ADK Session Creation Methods")
print("=" * 60)
print(f"\nAgent: {AGENT_NAME}")
print(f"Session ID: {SESSION_ID}")
print(f"Query: {query}")
print()

# Method 1: Create session, then send message
print("Method 1: Create session + send message")
print("-" * 60)

session_url = f"{ADK_BASE_URL}/apps/{AGENT_NAME}/users/{USER_ID}/sessions/{SESSION_ID}"
print(f"1a. Creating session at: {session_url}")

try:
    # Create empty session
    response = requests.post(session_url, json={}, timeout=10)
    print(f"    Status: {response.status_code}")
    if response.status_code in (200, 201, 409):
        print(f"    ✅ Session created")
        
        # Try sending message to /messages
        message_url = f"{session_url}/messages"
        print(f"\n1b. Sending message to: {message_url}")
        response2 = requests.post(message_url, json=payload, timeout=10)
        print(f"    Status: {response2.status_code}")
        if response2.status_code in (200, 201, 202):
            print(f"    ✅ Message sent via /messages")
            print(f"    Response: {response2.json()}")
        else:
            print(f"    ❌ Failed: {response2.text[:200]}")
    else:
        print(f"    ❌ Failed: {response.text[:200]}")
except Exception as e:
    print(f"    ❌ Error: {e}")

# Method 2: Create session with message in one call
print("\n\nMethod 2: Create session with message")
print("-" * 60)

SESSION_ID2 = f"test-{int(time.time())}-2"
session_url2 = f"{ADK_BASE_URL}/apps/{AGENT_NAME}/users/{USER_ID}/sessions/{SESSION_ID2}"
print(f"2. Creating session with message at: {session_url2}")

try:
    response = requests.post(session_url2, json=payload, timeout=10)
    print(f"   Status: {response.status_code}")
    if response.status_code in (200, 201):
        print(f"   ✅ Session created with message")
        print(f"   Response: {response.json()}")
    else:
        print(f"   ❌ Failed: {response.text[:200]}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Method 3: Check session to see if it has events
print("\n\nMethod 3: Check if agent executed")
print("-" * 60)

for sid in [SESSION_ID, SESSION_ID2]:
    url = f"{ADK_BASE_URL}/apps/{AGENT_NAME}/users/{USER_ID}/sessions/{sid}"
    print(f"Checking: {sid}")
    try:
        time.sleep(2)  # Wait a moment for processing
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            events = data.get("events", [])
            print(f"   Status: 200, Events: {len(events)}")
            if events:
                print(f"   ✅ Agent executed! {len(events)} events")
                print(f"   Latest event: {events[-1].get('type', 'unknown')}")
            else:
                print(f"   ⚠️  No events - agent didn't execute")
        else:
            print(f"   Status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    print()

print("=" * 60)
print("Summary")
print("=" * 60)
print("\nRecommendation:")
print("Check which method created events (agent execution)")
print("That's the method we should use in Streamlit!")

