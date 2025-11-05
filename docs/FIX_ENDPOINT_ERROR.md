# Fix for ADK Endpoint 404 Error

## Problem
Getting 404 error: `Not Found for url: http://localhost:8000/apps/marketing_orchestrator:run`

## Solution Steps

### Step 1: Find the Correct Endpoint

The ADK API server endpoint format may vary. I've updated `hackathon_ui.py` to try multiple endpoint formats automatically. But first, let's discover the correct one.

**Run this test script while ADK server is running:**

```powershell
# Make sure ADK server is running in another terminal first!
python test_adk_endpoint.py
```

This will test different endpoint formats and tell you which one works.

### Step 2: Updated Code

The updated `hackathon_ui.py` now:
- ✅ Tries multiple endpoint formats automatically
- ✅ Provides better error messages
- ✅ Handles different response formats from ADK

### Step 3: Common ADK Endpoint Formats

The code now tries these formats in order:

1. `/apps/marketing_orchestrator/users/{user_id}/sessions/{session_id}` (most common)
2. `/apps/marketing_orchestrator:run` (original format you tried)
3. `/run` with app_name in payload

### Step 4: Verify ADK Server is Running

Make sure your ADK server is actually running:

```powershell
# Terminal 1 - Start ADK Server
adk api_server marketing_orchestrator
```

You should see something like:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Step 5: Check ADK Documentation

If none of the endpoints work, check:
1. ADK version: `adk --version`
2. ADK API docs: The endpoint format might depend on your ADK version
3. Try: `adk api_server --help` to see available options

### Step 6: Alternative - Use ADK Web Instead

If the API server doesn't work, you can use the web server and modify the UI to connect to it:

```powershell
# Instead of: adk api_server marketing_orchestrator
# Use:
adk web src
# Then select "marketing_orchestrator" from the dropdown in the web interface
```

Then update the endpoint in `hackathon_ui.py` to match the web server format.

## Quick Fix

**If you just want to test quickly:**

1. Make sure ADK server is running: `adk api_server marketing_orchestrator`
2. Run the test script: `python test_adk_endpoint.py`
3. Look for the ✅ SUCCESS message
4. Update `ADK_API_URL` in `hackathon_ui.py` to use the working endpoint

## Most Likely Working Endpoint

Based on ADK patterns, try this format:

```python
ADK_API_URL = "http://localhost:8000/apps/marketing_orchestrator/users/{USER_ID}/sessions/{SESSION_ID}"
```

The code already tries this first!

