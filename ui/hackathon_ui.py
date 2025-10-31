# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
This module contains the Streamlit user interface for the Wendy's Hackathon.

It provides a user-friendly web interface to interact with the multi-agent system,
allowing participants to input their strategic challenges, adjust parameters, and
view the generated offer concepts.

Key Functions:
- `start_orchestrator_session`: Initiates the agent run by sending a POST request.
- `poll_session_events`: Continuously polls the ADK server to get live updates.
- `process_adk_response_with_data`: Parses the final JSON from the agent.
"""

import json
import random
import time
from typing import Any, Dict, List

import requests
import streamlit as st

# --- 1. CONFIGURATION ---

# This section defines the connection details for the ADK API server.
# For the UI to work, the ADK server MUST be running in a separate terminal.
# See the main README.md for instructions on how to start it.
ADK_BASE_URL = "http://localhost:8000"
USER_ID = "hackathon-user"
SESSION_ID = "hackathon-session"  # Using a fixed session for simplicity and persistence

# This is the primary endpoint for creating and polling the session state.
ADK_API_URL = (
    f"{ADK_BASE_URL}/apps/marketing_orchestrator/users/{USER_ID}/sessions/{SESSION_ID}"
)

# --- 2. BACKEND CONNECTOR FUNCTIONS ---


def start_orchestrator_session(
    query: str, agent_focus: List[str], model: str, instructions: str
) -> Dict[str, Any]:
    """
    Starts an agent run by sending the initial prompt to the ADK server.

    This function constructs a detailed prompt from the user's inputs and sends it
    to the ADK's execution endpoint (`/run`). It handles potential server
    endpoint variations (e.g., falling back to older formats) and returns a
    simple success or error message.

    Args:
        query: The main strategic challenge from the user.
        agent_focus: A list of agents to prioritize.
        model: The LLM model to emulate.
        instructions: Any custom instructions for the agent.

    Returns:
        A dictionary indicating success (`{'ok': True}`) or an error.
    """
    full_prompt = f"""
    --- HACKATHON INSTRUCTIONS ---
    Model to emulate: {model}
    Focus on agents: {', '.join(agent_focus)}
    Custom Instructions: {instructions}

    --- MAIN TASK ---
    {query}
    """

    # The ADK server expects the prompt to be in a specific JSON structure.
    payload = {"new_message": {"parts": [{"text": full_prompt}]}}

    try:
        # The recommended endpoint to trigger an agent run is `/run`.
        # We include the app, user, and session details in the payload.
        run_url = f"{ADK_BASE_URL}/run"
        payload_with_app = {
            **payload,
            "app_name": "marketing_orchestrator",
            "user_id": USER_ID,
            "session_id": SESSION_ID,
        }
        response = requests.post(
            run_url,
            json=payload_with_app,
            timeout=600,
            headers={"Content-Type": "application/json"},
        )

        # Fallback for older ADK versions that might use a different endpoint.
        if response.status_code == 404:
            alt_url = f"{ADK_BASE_URL}/apps/marketing_orchestrator:run"
            response = requests.post(
                alt_url,
                json=payload,
                timeout=600,
                headers={"Content-Type": "application/json"},
            )

        # As a last resort, we try creating the session directly. In some ADK
        # versions, this might also trigger the run.
        if response.status_code == 404:
            response = requests.post(
                ADK_API_URL,
                json=payload,
                timeout=600,
                headers={"Content-Type": "application/json"},
            )

        # A 409 Conflict status means a session with this ID already exists,
        # which is fine. Other success codes (200-204) are also good.
        if response.status_code in (200, 201, 202, 204, 409):
            return {"ok": True}

        # If we receive any other error, raise it.
        response.raise_for_status()
        return {"ok": True}

    except requests.exceptions.RequestException as e:
        # Provide a detailed error message if the connection fails.
        details = {"url": ADK_API_URL, "error": str(e)}
        if hasattr(e, "response") and getattr(e, "response") is not None:
            details["status_code"] = e.response.status_code
            details["response_text"] = e.response.text
        return {"error": "Failed to connect to ADK server", "details": details}


def poll_session_events(max_seconds: int = 600, interval_seconds: float = 2.0):
    """
    Polls the ADK session endpoint to get live updates on the agent's progress.

    This function will continuously make GET requests to the session URL. It
    `yields` data back to the UI, allowing for a real-time stream of events
    and heartbeats.

    Args:
        max_seconds: The maximum time to poll before timing out.
        interval_seconds: The time to wait between each poll.

    Yields:
        A dictionary containing the latest events, raw session data, a
        heartbeat status, and the elapsed time.
    """
    start_time = time.time()
    seen_event_count = 0
    last_data: Dict[str, Any] = {}

    # Yield an initial heartbeat to show the UI that polling has started.
    yield {"events": [], "data": {}, "heartbeat": True, "elapsed": 0.0}

    while (time.time() - start_time) < max_seconds:
        try:
            get_response = requests.get(ADK_API_URL, timeout=15)
            if get_response.status_code == 200:
                data = get_response.json()
                last_data = data
                events = data.get("events", [])

                # If new events have arrived, yield them to the UI.
                if len(events) > seen_event_count:
                    seen_event_count = len(events)
                    yield {
                        "events": events,
                        "data": data,
                        "heartbeat": False,
                        "elapsed": time.time() - start_time,
                    }

                # Check if the agent has returned its final response.
                for event in reversed(events):
                    if event.get("isFinalResponse") or event.get("type") == "agent_response":
                        return data  # Stop polling

            # Yield a heartbeat to let the UI know we're still waiting.
            yield {
                "events": last_data.get("events", []),
                "data": last_data,
                "heartbeat": True,
                "elapsed": time.time() - start_time,
            }
            time.sleep(interval_seconds)

        except requests.exceptions.RequestException:
            # If the server is temporarily unavailable, wait and try again.
            time.sleep(interval_seconds)
            continue

    # If the loop finishes, it means we have timed out.
    return last_data or {"events": []}


def process_adk_response_with_data(response_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parses the final JSON data from the ADK server to extract offer concepts.

    Args:
        response_data: The full JSON response from the session.

    Returns:
        A dictionary containing the extracted offer concepts or an error.
    """
    events = response_data.get("events", [])
    if not events:
        return {
            "error": (
                "Agent processing started but no events were returned. "
                "This might be an issue with the agent's execution."
            ),
            "raw_response": response_data,
        }

    # Find the last event, which should contain the final agent output.
    final_event = None
    for event in reversed(events):
        if event.get("isFinalResponse") or event.get("type") == "agent_response":
            final_event = event
            break
        # Fallback to the last event with any content.
        if "content" in event and not final_event:
            final_event = event

    if not final_event:
        return {"error": "No final response found in events", "raw_response": response_data}

    # Extract the text content from the final event.
    raw_text = ""
    if final_event.get("content", {}).get("parts"):
        raw_text = final_event["content"]["parts"][0].get("text", "")
    elif final_event.get("text"):
        raw_text = final_event["text"]
    elif isinstance(final_event.get("content"), str):
        raw_text = final_event["content"]

    return process_agent_response_text(raw_text)


def process_agent_response_text(raw_text: str) -> Dict[str, Any]:
    """
    Processes the raw text from the agent's final response.

    It first tries to parse the text as JSON. If that fails, it assumes the
    agent returned unstructured text and returns it as-is.

    Args:
        raw_text: The string content from the final agent event.

    Returns:
        A dictionary with the parsed data or the raw text.
    """
    if not raw_text:
        return {"error": "Empty response from agent", "raw_response": ""}

    try:
        # The agent is instructed to return JSON, so we try to parse it.
        # We strip markdown fences (```json ... ```) just in case.
        text_to_parse = raw_text.strip()
        if text_to_parse.startswith("```") and text_to_parse.endswith("```"):
            text_to_parse = "\n".join(text_to_parse.splitlines()[1:-1])

        parsed_data = json.loads(text_to_parse)
        if isinstance(parsed_data, dict):
            return parsed_data
        # If the agent returns a list, wrap it in a standard dictionary format.
        return {"offer_concepts": parsed_data if isinstance(parsed_data, list) else [parsed_data]}

    except json.JSONDecodeError:
        # If parsing fails, the agent may have returned plain text.
        # We return this for debugging purposes.
        return {"raw_response": raw_text, "offer_concepts": []}


def mock_image_generation(offer_name: str) -> str:
    """
    Mocks a call to an image generation model (like Imagen).

    For the hackathon, this returns a themed placeholder image based on keywords
    in the offer's name. In a real application, this would be an API call.

    Args:
        offer_name: The name of the offer concept.

    Returns:
        A URL to a placeholder image.
    """
    time.sleep(random.uniform(1, 3))  # Simulate network latency
    placeholders = {
        "breakfast": "https://placehold.co/600x400/FFF0C7/B36A00?text=Breakfast+Ad",
        "lunch": "https://placehold.co/600x400/FFD9D9/DA291C?text=Lunch+Ad",
        "frosty": "https://placehold.co/600x400/D4EBFF/0085C4?text=Frosty+Ad",
        "default": "https://placehold.co/600x400/E0E0E0/505050?text=Wendy's+Offer",
    }
    name_lower = offer_name.lower()
    if "breakfast" in name_lower or "streak" in name_lower:
        return placeholders["breakfast"]
    if "lunch" in name_lower or "baconator" in name_lower:
        return placeholders["lunch"]
    if "frosty" in name_lower:
        return placeholders["frosty"]
    return placeholders["default"]


# --- 3. STREAMLIT APP UI ---

st.set_page_config(page_title="Wendy's Offer AI", layout="wide")

# --- Sidebar for Levers (Inputs) ---
with st.sidebar:
    st.image(
        "https://placehold.co/400x150/DA291C/FFFFFF?text=Wendy's+Logo",
        use_container_width=True,
    )
    st.title("🚀 Mission Control")
    st.markdown("Adjust the levers for your AI agent team.")

    # Lever 1: The User Query
    user_query = st.text_input(
        "Enter your Strategic Challenge:",
        "Develop offers to increase breakfast traffic among Gen Z.",
    )

    # Lever 2: The Model (for emulation purposes)
    model_choice = st.selectbox(
        "Select Model (For Emulation):", ["Gemini 1.5 Pro", "Gemini 1.5 Flash"]
    )

    # Lever 3: Agent Focus
    tools_enabled = st.multiselect(
        "Agent Focus (What to prioritize):",
        ["MarketTrendsAgent", "CustomerInsightsAgent", "CompetitorIntelAgent"],
        default=["MarketTrendsAgent", "CustomerInsightsAgent", "CompetitorIntelAgent"],
    )

    # Lever 4: Custom Instructions
    model_instructions = st.text_area(
        "Custom Instructions (Optional):",
        "Focus on app-exclusive offers. Be creative and bold.",
        height=100,
    )

    # The "Run" button that triggers the agent workflow.
    run_button = st.button("Generate Offers", type="primary", use_container_width=True)

# --- Main Area for Results (Outputs) ---
st.title("🤖 Wendy's Agentic AI Offer Generator")

if run_button:
    # --- Live Polling and Event Streaming ---
    status_placeholder = st.empty()
    trace_box = st.container()
    raw_expander = st.expander("Live raw session snapshots (for debugging)")

    with status_placeholder.container():
        st.info("Attempting to start agent run...")

    start_result = start_orchestrator_session(
        user_query, tools_enabled, model_choice, model_instructions
    )

    if "error" in start_result:
        st.error(f"Error starting session: {start_result['error']}")
        st.json(start_result.get("details", "No details available."))
    else:
        # --- Stream events as they arrive from the polling function ---
        displayed_event_count = 0
        final_data: Dict[str, Any] = {}
        last_update = None

        for update in poll_session_events():
            last_update = update
            events = update.get("events", [])
            elapsed = update.get("elapsed", 0.0)
            is_heartbeat = update.get("heartbeat", False)

            # Update the main status line.
            with status_placeholder.container():
                st.info(
                    f"Session running... Polling for events. "
                    f"Count: {len(events)} | Elapsed: {int(elapsed)}s"
                )

            # If new events have arrived, display them in the trace log.
            if len(events) > displayed_event_count:
                with trace_box:
                    for event in events[displayed_event_count:]:
                        st.text(f"[{event.get('type', 'event')}] {event.get('text', '(No text)')}")
                displayed_event_count = len(events)

            # Periodically show the raw session data for debugging.
            if is_heartbeat and int(elapsed) % 10 == 0:
                with raw_expander:
                    st.caption(f"Snapshot at t={int(elapsed)}s")
                    st.json(update.get("data", {}))

        # --- Process and Display Final Results ---
        status_placeholder.empty()  # Clear the "polling" status
        final_data = last_update.get("data") if last_update else {}

        if not final_data or not final_data.get("events"):
            st.warning(
                "Polling timed out, but no events were found. "
                "Check the ADK server logs for errors."
            )
            st.json(final_data)
        else:
            results = process_adk_response_with_data(final_data)

            st.success("Your new offer concepts are ready!")

            if "error" in results:
                st.error(f"Error processing final response: {results['error']}")

            final_offers = results.get("offer_concepts", [])
            if not final_offers:
                st.warning(
                    "The agent ran but did not return any offer concepts. "
                    "Check the raw output below."
                )

            for i, offer in enumerate(final_offers):
                st.header(f"Concept {i+1}: {offer.get('name', 'Unnamed Offer')}")
                col1, col2 = st.columns([1, 1.5])

                with col1:
                    with st.spinner(f"Generating ad mockup for '{offer.get('name')}'..."):
                        image_url = mock_image_generation(offer.get("name", "default"))
                        st.image(
                            image_url, caption=f"AI-generated mockup for {offer.get('name')}"
                        )
                with col2:
                    st.subheader("Mechanic:")
                    st.markdown(f"> {offer.get('mechanic', 'No mechanic defined.')}")
                    st.subheader("Data-Driven Rationale:")
                    st.info(offer.get("rationale", "No rationale provided."))

            with st.expander("Show Full Raw Output from Orchestrator"):
                st.json(final_data)
else:
    st.info("Adjust the levers in the sidebar and click 'Generate Offers' to start.")

