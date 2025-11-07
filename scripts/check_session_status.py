#!/usr/bin/env python3
"""
Check the status of a session in ADK
"""

import sys
import requests

if len(sys.argv) < 2:
    print("Usage: python scripts/check_session_status.py <session_id> [agent_name]")
    sys.exit(1)

session_id = sys.argv[1]
agent_name = sys.argv[2] if len(sys.argv) > 2 else "marketing_orchestrator"

url = f"http://127.0.0.1:8000/apps/{agent_name}/users/streamlit-user/sessions/{session_id}"

print(f"Checking session: {session_id}")
print(f"Agent: {agent_name}")
print(f"URL: {url}")
print("=" * 60)

try:
    response = requests.get(url, timeout=10)
    print(f"\nStatus Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        events = data.get("events", [])
        print(f"Events: {len(events)} total")
        
        if events:
            print("\nRecent events:")
            for event in events[-5:]:
                event_type = event.get("type", "unknown")
                text = event.get("text", "(no text)")[:60]
                print(f"  - {event_type}: {text}")
        else:
            print("\n⚠️ No events yet - agent may not have started")
        
        # Check for final response
        has_final = any(e.get("isFinalResponse") or e.get("type") == "agent_response" 
                       for e in events)
        if has_final:
            print("\n✅ Session has completed!")
        else:
            print("\n⏳ Session still in progress...")
            
    elif response.status_code == 404:
        print("\n❌ Session not found!")
        print("Possible reasons:")
        print("  - Session ID is incorrect")
        print("  - Agent name is wrong")
        print("  - Session wasn't created successfully")
    else:
        print(f"\n❌ Error: {response.text[:200]}")
        
except requests.exceptions.ConnectionError:
    print("\n❌ Cannot connect to ADK server")
    print("Make sure 'adk web src' is running")
except Exception as e:
    print(f"\n❌ Error: {e}")

