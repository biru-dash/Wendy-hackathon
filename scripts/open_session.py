#!/usr/bin/env python3
"""
Helper script to open a session in ADK Web UI

Usage:
    python scripts/open_session.py streamlit-1762521075-7311
    python scripts/open_session.py streamlit-1762521075-7311 marketing_orchestrator
"""

import sys
import webbrowser

ADK_BASE_URL = "http://localhost:8000"

def open_session(session_id: str, agent_name: str = None):
    """Open a session in the ADK Web UI."""
    
    print("=" * 60)
    print("Opening Session in ADK Web UI")
    print("=" * 60)
    
    if agent_name:
        # Direct URL if agent name is known
        url = f"{ADK_BASE_URL}/apps/{agent_name}/users/streamlit-user/sessions/{session_id}"
        print(f"\nDirect URL:")
        print(f"  {url}")
    else:
        # Try common agents
        print(f"\nSession ID: {session_id}")
        print(f"\nTry these URLs:")
        
        agents = [
            "marketing_orchestrator",
            "market_trends_analyst",
            "customer_insights",
            "offer_design"
        ]
        
        for agent in agents:
            url = f"{ADK_BASE_URL}/apps/{agent}/users/streamlit-user/sessions/{session_id}"
            print(f"\n  {agent}:")
            print(f"    {url}")
    
    print(f"\n" + "=" * 60)
    print("Or browse all sessions at:")
    print(f"  {ADK_BASE_URL}")
    print("=" * 60)
    
    # Try to open in browser
    if agent_name:
        print(f"\nOpening in browser...")
        webbrowser.open(url)
    else:
        print(f"\nOpening ADK Web UI home page...")
        webbrowser.open(ADK_BASE_URL)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/open_session.py <session_id> [agent_name]")
        print("\nExample:")
        print("  python scripts/open_session.py streamlit-1762521075-7311")
        print("  python scripts/open_session.py streamlit-1762521075-7311 marketing_orchestrator")
        sys.exit(1)
    
    session_id = sys.argv[1]
    agent_name = sys.argv[2] if len(sys.argv) > 2 else None
    
    open_session(session_id, agent_name)

