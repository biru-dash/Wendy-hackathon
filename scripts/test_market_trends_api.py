import json
import time

import requests

ADK_BASE_URL = "http://127.0.0.1:8000"
AGENT = "market_trends_analyst"
USER = "streamlit-user"


def main():
    print("=== Market Trends Analyst API smoke test ===")

    create_url = f"{ADK_BASE_URL}/apps/{AGENT}/users/{USER}/sessions"
    print(f"Creating session via {create_url}")
    create_resp = requests.post(create_url, json={}, timeout=30)
    print("create status", create_resp.status_code)
    print("body", create_resp.text)
    create_resp.raise_for_status()

    data = create_resp.json()
    session_id = data.get("id") or data.get("name", "").split("/")[-1]
    if not session_id:
        raise RuntimeError("No session_id returned")

    print("session_id", session_id)

    run_url = f"{ADK_BASE_URL}/apps/{AGENT}/users/{USER}/sessions/{session_id}:run"
    payloads = [
        {"query": "Test query about Gen Z breakfast trends"},
        {"message": {"text": "Test query about Gen Z breakfast trends"}},
        {"new_message": {"parts": [{"text": "Test query about Gen Z breakfast trends"}]}},
    ]

    run_status = None
    for payload in payloads:
        print("Attempting", run_url, "payload", json.dumps(payload))
        run_resp = requests.post(run_url, json=payload, timeout=60)
        print(" -> status", run_resp.status_code)
        print(" -> body", run_resp.text)
        if run_resp.status_code in (200, 201, 202):
            run_status = run_resp
            break

    if run_status is None or run_status.status_code not in (200, 201, 202):
        print("No successful run invocation.")
        return

    poll_url = f"{ADK_BASE_URL}/apps/{AGENT}/users/{USER}/sessions/{session_id}"
    print("Polling", poll_url)
    for i in range(10):
        time.sleep(2)
        poll_resp = requests.get(poll_url, timeout=30)
        print(f"poll {i}: status {poll_resp.status_code}")
        if poll_resp.status_code != 200:
            print(" ->", poll_resp.text)
            continue
        poll_data = poll_resp.json()
        events = poll_data.get("events", [])
        print(" -> events", len(events))
        if events:
            print(json.dumps(events[-1], indent=2))
            break
    else:
        print("No events observed after polling window.")


if __name__ == "__main__":
    main()
