import json
import time
from contextlib import nullcontext
from typing import Any, Dict, List, Optional, Tuple

import requests
import streamlit as st

# ---------------------------------------------------------------------------
# Constants & Metadata
# ---------------------------------------------------------------------------

ADK_BASE_URL = "http://127.0.0.1:8000"
DEFAULT_USER_ID = "user"
RUN_SSE_ENDPOINT = f"{ADK_BASE_URL}/run_sse"
STATUS_SUCCESS_CODES = {200, 201, 202}
POLL_INTERVAL_SECONDS = 2.0
MAX_POLL_SECONDS = 180

AGENT_METADATA = {
    "market_trends_analyst": {
        "title": "Market Trends Analyst",
        "user_id": DEFAULT_USER_ID,
        "overview_md": """
### What does this agent do?
- Acts like a **Market Research Analyst**.
- Scans articles, blogs, and social channels to surface emerging breakfast trends and consumer signals.
- Supplies these insights to downstream teams (Customer Insights, Offer Design, Orchestrator).
- In real life, market research analysts continuously track consumer behavior, competitor moves, and macro signals, then package the takeaways for marketing and product teams—this agent emulates that end-to-end loop programmatically.

### How does it achieve this?
1. **Data Collection Agent** hunts for URLs using `google_search`.
2. **Research Synthesis Agent** reads those URLs via `web_scraper_tool` and produces a trend brief.
3. Gemini models (`gemini-2.5-flash` for lookup, `gemini-2.5-pro` for synthesis) interpret context and summarize findings.

### Workflow at a glance
```
Input prompt → Data Collection Agent → Research Synthesis Agent → Trend brief output
```
""",
        "technical_md": """
**Structure**
- Root: `MarketTrendsAnalystRoot` (SequentialAgent)
- Sub-agents:
  1. `DataCollectionAgent` (LlmAgent)
     - Tool: `google_search`
     - Instruction: `src/market_trends_analyst/sub_agents/data_collection/instruction.txt`
  2. `ResearchAndSynthesisAgent` (LlmAgent)
     - Tool: `web_scraper_tool`
     - Instruction: `src/market_trends_analyst/sub_agents/research_synthesis/instruction.txt`

**Function focus**
- External market scanning: breakfast trends, Gen Z preferences, Q1 seasonal signals.
""",
        "testing_intro": """
1. Pick a focused breakfast/Gen Z prompt.
2. Run the agent and watch the SSE feed and event timeline.
3. Open the linked session in ADK Web UI to inspect the trace and events.
4. Tweak instructions/tools, rerun, and compare improvements.
""",
        "example_prompts": [
            "What breakfast trends are emerging among Gen Z customers during Q1?",
            "Which competitor breakfast promotions are resonating with younger digital audiences?",
            "How are quick-service restaurants innovating morning offers for Gen Z?",
        ],
        "default_prompt": "What emerging breakfast trends should we watch for Gen Z consumers?",
    },
    "customer_insights": {
        "title": "Customer Insights",
        "user_id": DEFAULT_USER_ID,
        "overview_md": """
### What does this agent do?
- Mirrors a **Customer Insights Analyst / Data Scientist**.
- Mines transactional and feedback data to understand Gen Z breakfast behaviours, sentiment, and segment profiles.
- Provides internal context that complements Market Trends outputs.

### How does it achieve this?
1. **Behavioral Analysis Agent** queries BigQuery (via `crm_database_tool`) for breakfast visit patterns, spend, and redemption metrics.
2. **Sentiment Analysis Agent** pulls review/comment data with `feedback_database_tool` to capture themes and tone.
3. **Profile Synthesizer Agent** merges quantitative + qualitative findings into breakfast-focused customer profiles.

### Workflow at a glance
```
Input prompt → Behavioral Analysis (parallel) → Sentiment Analysis (parallel)
            → Profile Synthesizer → Segment profiles & insights
```
""",
        "technical_md": """
**Structure**
- Root: `CustomerInsightsManagerAgent` (ParallelAgent)
- Sub-agents:
  1. `BehavioralAnalysisAgent`
     - Tool: `crm_database_tool`
     - Instruction: `src/customer_insights/sub_agents/behavioral_analysis/instruction.txt`
  2. `SentimentAnalysisAgent`
     - Tool: `feedback_database_tool`
     - Instruction: `src/customer_insights/sub_agents/sentiment_analysis/instruction.txt`
  3. `ProfileSynthesizerAgent`
     - Synthesizes prior outputs (`profile_synthesizer/instruction.txt`)

**Function focus**
- Internal data mining: Gen Z breakfast visit lift, channel preferences, review sentiment.
""",
        "testing_intro": """
1. Run a query about Gen Z breakfast behaviour or sentiment.
2. Observe the parallel execution (two sub-agents first, profile synthesis after).
3. In ADK Web UI, review the SQL-like tool calls and resulting insights.
4. Adjust instructions to tighten filters (Gen Z age, 6-11am window, Q1 date range) and compare outputs.
""",
        "example_prompts": [
            "What are the behavioral patterns of Gen Z app users during breakfast hours?",
            "Summarize feedback themes from Gen Z customers about breakfast offers.",
            "Profile Gen Z breakfast segments during Q1 across channels and redemption types.",
        ],
        "default_prompt": "Analyze Gen Z breakfast customer behaviour and sentiment for Q1.",
    },
    "offer_design": {
        "title": "Offer Design",
        "user_id": DEFAULT_USER_ID,
        "overview_md": """
### What does this agent do?
- Acts like a **Marketing Strategist / Offer Design Manager**.
- Combines market trends, customer insights, and (optionally) competitor intel to propose breakfast offers aimed at Gen Z.
- Produces prioritized concepts with rationale and feasibility notes.

### How does it achieve this?
- **Simplified Offer Design Agent** ingests the upstream research and generates/prioritizes offer concepts in a single step.
- Leverages LLM reasoning (`gemini-2.5-pro`) for creative idea generation, evidence citation, and scoring.

### Workflow at a glance
```
Input: Trend brief + Customer insights (+ optional competitor insights)
  ↓
Simplified Offer Design Agent → Offer ideas → Rationale / Feasibility / Impact
```
""",
        "technical_md": """
**Structure**
- Root: `SimplifiedOfferDesignAgent` (LlmAgent)
- Instruction file: `src/offer_design/sub_agents/simplified_offer_design/instruction.txt`
- Tools: none (operates on text inputs from other agents)

**Function focus**
- Strategic synthesis: breakfast bundles, app exclusives, value offers with evidence and impact call-outs.
""",
        "testing_intro": """
1. Provide synthesized inputs (or the full goal prompt) describing market/customer insights.
2. Review the generated concepts, rationale, and prioritization.
3. In ADK Web UI, confirm the structure, evidence citations, and feasibility discussion.
4. Strengthen instructions to enforce structure, evidence, and Gen Z breakfast relevance.
""",
        "example_prompts": [
            "Using Gen Z breakfast trends and behaviour insights, propose three breakfast offers for Q1.",
            "Create prioritized breakfast concepts informed by Gen Z app usage and morning preferences.",
        ],
        "default_prompt": "Based on trends and customer insights, propose three prioritized breakfast offers for Gen Z.",
    },
    "marketing_orchestrator": {
        "title": "Marketing Orchestrator",
        "user_id": DEFAULT_USER_ID,
        "overview_md": """
### What does this agent do?
- Plays the role of a **Marketing Director / Campaign Manager**.
- Orchestrates Market Trends, Customer Insights, and Offer Design in sequence to deliver final breakfast offers for Gen Z.
- Represents the full end-to-end workflow described in the hackathon.

### How does it achieve this?
1. **Market Trends Analyst** delivers external context.
2. **Customer Insights** contributes internal behavioural/sentiment data.
3. **Offer Design** synthesizes both into prioritized breakfast concepts with rationale.

### Workflow at a glance
```
User prompt → Market Trends → Customer Insights → Offer Design → Final offer concepts
```
""",
        "technical_md": """
**Structure**
- Root: `MarketingOrchestratorAgent` (SequentialAgent)
- Sub-flows:
  1. Market Trends Analyst (see above)
  2. Customer Insights (parallel sub-agents)
  3. Offer Design (simplified LLM agent)
- Optional: Competitor Intelligence (disabled by default)

**Function focus**
- Cross-team coordination: ensures each specialised agent runs, then passes outputs downstream.
""",
        "testing_intro": """
1. Run the full goal query to watch the orchestrated workflow.
2. Inspect the trace to see sub-agent execution order and data handoffs.
3. Compare orchestrator output before/after instruction tweaks to upstream agents.
4. Use this as the "final demo" once individual agents are tuned.
""",
        "example_prompts": [
            "Develop three innovative offers to increase breakfast traffic among Gen Z customers during Q1 (6am-11am).",
        ],
        "default_prompt": "Develop three innovative offers to increase breakfast traffic among Gen Z customers during Q1 (6am-11am).",
    },
    "competitor_intelligence": {
        "title": "Competitor Intelligence",
        "user_id": DEFAULT_USER_ID,
        "overview_md": """
### What does this agent do?
- Mirrors a **Competitive Intelligence Lead**.
- Researches breakfast-focused campaigns from rival QSR brands targeting Gen Z.
- Surfaces whitespace opportunities that can be fed into Offer Design and the orchestrated workflow.

### How does it achieve this?
1. **Target Identification Agent** selects which competitors to investigate using `google_search`.
2. **Research Orchestrator Agent** coordinates deeper dives with an AgentTool that spins up competitor-specific agents.
3. **Competitor Analysis Agent** compiles detailed findings for each competitor.
4. **Whitespace Synthesizer Agent** distills opportunities where Wendy's can differentiate.

### Workflow at a glance
```
Prompt → Target Identification → Research Orchestrator → Competitor Analysis → Whitespace Synthesis
```
""",
        "technical_md": """
**Structure**
- Root: `CompetitorIntelManagerAgent` (SequentialAgent)
- Sub-agents:
  1. `TargetIdentificationAgent`
     - Tool: `google_search`
     - Instruction: `src/competitor_intelligence/sub_agents/target_identification/instruction.txt`
  2. `ResearchOrchestratorAgent`
     - Tool: `competitor_analysis_tool`
     - Instruction: `src/competitor_intelligence/sub_agents/research_orchestrator/instruction.txt`
  3. `CompetitorAnalysisAgent`
     - Tool: `google_search`
     - Instruction: `src/competitor_intelligence/sub_agents/competitor_analysis/instruction.txt`
  4. `WhitespaceSynthesizerAgent`
     - Instruction: `src/competitor_intelligence/sub_agents/whitespace_synthesizer/instruction.txt`

**Function focus**
- External competitor scan: breakfast offers, Gen Z targeting tactics, pricing moves, Q1 seasonal campaigns.
""",
        "testing_intro": """
1. Enable this agent in ADK Web if it is commented out (see Advanced Path instructions in the agenda).
2. Run a query focused on competitor breakfast strategies for Gen Z.
3. In ADK Web UI, confirm the sequential flow (target identification → competitor dives → whitespace synthesis).
4. Tighten instructions to emphasise Gen Z breakfast insights, pricing comparisons, and concrete promo examples.
""",
        "example_prompts": [
            "Identify competitor breakfast campaigns targeting Gen Z in Q1 and highlight whitespace opportunities.",
            "How are rival QSR brands pricing Gen Z breakfast offers, and where can we differentiate?",
            "Summarize Gen Z-focused breakfast promotions from top three competitors and gaps we can exploit.",
        ],
        "default_prompt": "Research competitor Gen Z breakfast promotions for Q1 and identify whitespace opportunities.",
    },
}

AGENT_CHOICES = {meta["title"]: key for key, meta in AGENT_METADATA.items()}
UNCHANGED_POLL_LIMIT = 3

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def _session_endpoints(agent_name: str, user_id: str, session_id: Optional[str] = None):
    base = f"{ADK_BASE_URL}/apps/{agent_name}/users/{user_id}/sessions"
    if session_id is None:
        return base
    return f"{base}/{session_id}"


def create_session(agent_name: str, user_id: str) -> Optional[str]:
    endpoint = _session_endpoints(agent_name, user_id)
    try:
        response = requests.post(
            endpoint,
            json={},
            timeout=30,
            headers={"Content-Type": "application/json"},
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as exc:
        st.error(f"Failed to create session for {agent_name} ({exc})")
        return None

    session_id = None
    try:
        data = response.json()
        session_id = (
            data.get("id")
            or (data.get("name", "").split("/")[-1] if data.get("name") else None)
        )
    except ValueError:
        pass

    if not session_id:
        st.error("Session created but no session_id returned in response body.")
        return None
    return session_id


def run_agent_with_messages(agent_name: str, user_id: str, session_id: str, query: str, status, sse_container):
    payload = {
        "appName": agent_name,
        "userId": user_id,
        "sessionId": session_id,
        "newMessage": {
            "role": "user",
            "parts": [{"text": query}],
        },
        "streaming": False,
        "stateDelta": None,
    }
    headers = {
        "Accept": "text/event-stream",
        "Content-Type": "application/json",
    }

    try:
        status.write("Calling `/run_sse` to start the agent…")
        response = requests.post(
            RUN_SSE_ENDPOINT,
            json=payload,
            headers=headers,
            timeout=300,
            stream=True,
        )
    except requests.exceptions.RequestException as exc:
        st.error(f"Failed to call /run_sse: {exc}")
        return False, [], [f"Network error calling /run_sse: {exc}"]

    if response.status_code not in STATUS_SUCCESS_CODES:
        st.error(
            f"/run_sse returned {response.status_code}: {response.text.strip()}"
        )
        return False, [], [f"/run_sse returned {response.status_code}: {response.text.strip()}"]

    status.write("Streaming live SSE messages…")
    sse_messages: List[Dict] = []
    sse_errors: List[str] = []

    try:
        for _line in response.iter_lines(decode_unicode=True):
            if not _line:
                continue
            if _line.startswith("data:"):
                message = _line[5:].strip()
                parsed, error_text = _parse_sse_payload(message)
                if parsed is not None:
                    sse_messages.append(parsed)
                    with sse_container:
                        st.json(parsed)
                    if error_text:
                        sse_errors.append(error_text)
                else:
                    sse_messages.append({"raw": message})
                    with sse_container:
                        st.code(message, language="json")
    finally:
        response.close()

    return True, sse_messages, sse_errors


def poll_session_for_data(agent_name: str, user_id: str, session_id: str, status):
    session_url = _session_endpoints(agent_name, user_id, session_id)
    start_time = time.time()
    seen_event_ids: set = set()
    collected_events: List[Dict] = []
    final_summary: Optional[str] = None
    raw_session: Optional[Dict] = None
    unchanged_cycles = 0
    previous_event_count = 0

    while True:
        elapsed = time.time() - start_time
        if elapsed > MAX_POLL_SECONDS:
            status.update(
                label="Polling timed out — check the session in ADK Web UI for full details.",
                state="error",
            )
            break

        try:
            response = requests.get(session_url, timeout=30)
        except requests.exceptions.RequestException as exc:
            status.write(f"Polling error: {exc}")
            time.sleep(POLL_INTERVAL_SECONDS)
            continue

        if response.status_code != 200:
            status.write(
                f"Polling failed with status {response.status_code}: {response.text.strip()}"
            )
            time.sleep(POLL_INTERVAL_SECONDS)
            continue

        raw_session = response.json()
        events = raw_session.get("events", [])

        status.write(
            f"Polling session… {int(elapsed)}s elapsed. Events received: {len(events)}"
        )

        for event in events:
            event_id = _event_id(event)
            if event_id not in seen_event_ids:
                seen_event_ids.add(event_id)
                collected_events.append(event)
                extracted_text = _extract_final_model_text([event])
                if extracted_text:
                    final_summary = extracted_text

        if _session_complete(events):
            status.update(
                label="Final response detected — session complete.",
                state="complete",
            )
            break

        if len(events) == previous_event_count:
            unchanged_cycles += 1
        else:
            unchanged_cycles = 0
            previous_event_count = len(events)

        if unchanged_cycles >= UNCHANGED_POLL_LIMIT:
            if not final_summary:
                final_summary = _extract_final_model_text(events)
            status.update(
                label="No new events detected; stopping polling. Review in ADK Web UI for full trace.",
                state="complete",
            )
            break

        time.sleep(POLL_INTERVAL_SECONDS)

    return final_summary, collected_events, raw_session


def _event_id(event: Dict) -> str:
    return str(event.get("id") or event.get("eventId") or hash(str(event)))


def _render_event(event: Dict):
    event_type = event.get("type", "agent_message")
    role = event.get("role", "")
    label = f"**Event:** `{event_type}`"
    if role:
        label += f" · `{role}`"
    st.markdown(label)

    if event.get("text"):
        st.write(event["text"])

    if event.get("parts"):
        for part in event["parts"]:
            if isinstance(part, dict) and part.get("text"):
                st.markdown(part["text"])

    if event.get("content"):
        st.json(event["content"])

    if event.get("payload"):
        st.json(event["payload"])

    st.markdown("---")


def _session_complete(events: List[Dict]) -> bool:
    if not events:
        return False
    for event in reversed(events):
        event_type = event.get("type") or ""
        if event.get("isFinalResponse") or event_type in {
            "agent_response",
            "agent_completed",
            "session_completed",
            "session.complete",
            "session.completed",
            "response_completed",
            "session.result",
        }:
            return True
    return False


def _extract_final_model_text(events: List[Dict]) -> Optional[str]:
    for event in reversed(events):
        if not isinstance(event, dict):
            continue
        if event.get("role") not in (None, "", "model", "assistant"):
            continue
        text_fields: List[str] = []
        if event.get("text"):
            text_fields.append(event["text"])
        parts = event.get("parts") or []
        for part in parts:
            if isinstance(part, dict):
                part_text = part.get("text")
                if part_text:
                    text_fields.append(part_text)
        payload = event.get("payload")
        if isinstance(payload, dict):
            maybe_texts = _extract_text_blocks(payload)
            text_fields.extend(maybe_texts)
        content = event.get("content")
        if isinstance(content, dict):
            maybe_texts = _extract_text_blocks(content)
            text_fields.extend(maybe_texts)
        elif isinstance(content, list):
            for item in content:
                maybe_texts = _extract_text_blocks(item)
                text_fields.extend(maybe_texts)

        for candidate in text_fields:
            normalized = candidate.strip()
            if normalized:
                return normalized
    return None


def _render_market_trends_summary(summary: str):
    intro_text = summary.strip()
    trend_data = None
    remainder = summary.strip()

    if "```json" in summary:
        json_start = summary.index("```json") + len("```json")
        json_end = summary.find("```", json_start)
        if json_end != -1:
            json_payload = summary[json_start:json_end].strip()
            try:
                trend_data = json.loads(json_payload)
            except json.JSONDecodeError:
                trend_data = None
            intro_text = summary[: summary.index("```json")].strip()
            remainder = summary[json_end + len("```") :].strip()

    exec_summary = ""
    if "### Executive Summary" in remainder:
        _, exec_summary = remainder.split("### Executive Summary", 1)
        exec_summary = exec_summary.strip()
    else:
        exec_summary = remainder.strip()

    if intro_text and intro_text != exec_summary:
        st.caption(intro_text)

    if exec_summary:
        st.subheader("Executive Summary")
        st.markdown(exec_summary)

    if trend_data:
        st.subheader("Trend Brief JSON")
        st.json(trend_data)

        if isinstance(trend_data, dict):
            briefs = trend_data.get("trend_briefs") or trend_data.get("trend_brief") or []
            if briefs:
                st.subheader("Market Trends Briefs")
                for idx, brief in enumerate(briefs, start=1):
                    title = brief.get("title") or f"Trend {idx}"
                    summary_text = brief.get("summary", "")
                    evidence = brief.get("evidence_snippets") or []
                    signal = brief.get("signal_strength")
                    velocity = brief.get("velocity")
                    recommendations = brief.get("recommended_directions")

                    with st.expander(f"{idx}. {title}", expanded=(idx == 1)):
                        if summary_text:
                            st.markdown(summary_text)
                        if signal or velocity:
                            st.markdown(
                                f"- **Signal strength:** {signal or 'Unknown'}\n"
                                f"- **Velocity:** {velocity or 'Unknown'}"
                            )
                        if evidence:
                            st.markdown("**Evidence snippets:**")
                            for snippet in evidence:
                                st.write(f"- {snippet}")
                        if recommendations:
                            st.markdown("**Recommended directions:**")
                            st.markdown(recommendations)


def _parse_sse_payload(message: str):
    try:
        payload = json.loads(message)
    except json.JSONDecodeError:
        return None, None

    error_text = None
    if payload.get("errorMessage"):
        error_text = f"SSE error: {payload['errorMessage']}"
    elif payload.get("errorCode"):
        error_text = (
            f"SSE error {payload['errorCode']}: {payload.get('errorMessage', 'Unknown error')}"
        )

    return payload, error_text


def _extract_text_blocks(obj) -> List[str]:
    texts: List[str] = []

    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == "text" and isinstance(value, str):
                texts.append(value)
            else:
                texts.extend(_extract_text_blocks(value))
    elif isinstance(obj, list):
        for item in obj:
            texts.extend(_extract_text_blocks(item))

    return texts


def _collect_generated_outputs(run_state: Dict[str, Any]) -> List[str]:
    outputs: List[str] = []

    summary = run_state.get("final_summary")
    if summary:
        outputs.append(summary)

    for message in run_state.get("sse_messages", []) or []:
        outputs.extend(_extract_text_blocks(message))

    for event in run_state.get("events", []) or []:
        outputs.extend(_extract_text_blocks(event))

    seen: set = set()
    deduped: List[str] = []
    for text in outputs:
        normalized = text.strip()
        if normalized and normalized not in seen:
            seen.add(normalized)
            deduped.append(normalized)

    return deduped


def _parse_offer_concepts(texts: List[str]) -> List[Tuple[str, str]]:
    offers: List[Tuple[str, str]] = []

    for text in texts:
        if "Priority:" not in text:
            continue

        current_name = None
        current_desc: List[str] = []
        lines = [line.strip() for line in text.splitlines() if line.strip()]

        for line in lines:
            if line.startswith("Priority:"):
                if current_name and current_desc:
                    offers.append((current_name, "\n".join(current_desc)))
                    current_desc = []

                parts = line.split("-", 1)
                if len(parts) == 2:
                    current_name = parts[1].strip()
                else:
                    current_name = line.replace("Priority:", "", 1).strip()
            elif current_name:
                current_desc.append(line)

        if current_name and current_desc:
            offers.append((current_name, "\n".join(current_desc)))

    return offers


# ---------------------------------------------------------------------------
# Streamlit UI
# ---------------------------------------------------------------------------

st.set_page_config(page_title="Hackathon Agent Console", layout="wide")

if "agent_runs" not in st.session_state:
    st.session_state.agent_runs = {}

st.sidebar.header("Select agent to explore")
agent_title = st.sidebar.selectbox("Agent", list(AGENT_CHOICES.keys()))
agent_key = AGENT_CHOICES[agent_title]
metadata = AGENT_METADATA[agent_key]
user_id = metadata.get("user_id", DEFAULT_USER_ID)

st.title(f"🧪 {metadata['title']} — Hackathon Testing Console")

run_state = st.session_state.agent_runs.get(agent_key)

overview_tab, testing_tab, results_tab = st.tabs([
    "Overview & Prerequisites",
    "Testing Exercise",
    "Results",
])

with overview_tab:
    left, right = st.columns([1.8, 1])
    with left:
        st.markdown(metadata["overview_md"])
    with right:
        st.markdown(
            """
### Readiness checklist
- ✅ `adk web src` running locally
- ✅ `gcloud auth application-default login`
- ✅ Internet access for API/tool calls
- 🔗 Keep `http://127.0.0.1:8000/dev-ui` open alongside this page
"""
        )
        with st.expander("Technical deep dive", expanded=False):
            st.markdown(metadata["technical_md"])

with st.sidebar:
    st.divider()
    st.subheader("Static Config")
    st.write(f"ADK Base URL: `{ADK_BASE_URL}`")
    st.write(f"Agent: `{agent_key}`")
    st.write(f"User ID: `{user_id}`")
    st.caption("Override in `AGENT_METADATA` if your environment differs.")

with testing_tab:
    st.markdown(metadata["testing_intro"])
    st.caption(
        "Tip: capture both baseline and post-instruction runs for your final demo."
    )

    with st.expander("1. Run the agent", expanded=True):
        st.markdown("**Try prompts such as:**")
        for prompt in metadata["example_prompts"]:
            st.markdown(f"- {prompt}")

        form_key = f"prompt_form_{agent_key}"
        with st.form(form_key, clear_on_submit=False):
            query_text = st.text_area(
                "Enter your prompt",
                metadata["default_prompt"],
                height=120,
            )
            submitted = st.form_submit_button(
                f"Run {metadata['title']}",
                type="primary",
            )

with results_tab:
    if run_state:
        final_summary_text = (
            run_state.get("final_summary")
            or _extract_final_model_text(run_state.get("events", []) or [])
            or _extract_final_model_text(run_state.get("sse_messages", []) or [])
        )

        if agent_key == "market_trends_analyst":
            if final_summary_text:
                _render_market_trends_summary(final_summary_text)
            else:
                st.caption(
                    "Unable to locate the final summary in this session. Open the ADK Web trace for full details."
                )
        else:
            if final_summary_text:
                st.subheader("Executive Summary")
                st.markdown(final_summary_text)

            generated_outputs = _collect_generated_outputs(run_state)
            if final_summary_text:
                generated_outputs = [
                    text
                    for text in generated_outputs
                    if text.strip() != final_summary_text.strip()
                ]

            offer_concepts = _parse_offer_concepts(generated_outputs)

            if offer_concepts:
                st.subheader("Detailed Results")
                for idx, (name, description) in enumerate(offer_concepts, start=1):
                    with st.expander(f"Offer {idx}: {name}", expanded=(idx == 1)):
                        st.markdown(description)
            elif generated_outputs:
                st.subheader("Detailed Results")
                for idx, text in enumerate(generated_outputs, start=1):
                    with st.expander(f"Result Segment {idx}", expanded=(idx == 1)):
                        st.markdown(text)
            else:
                st.caption(
                    "Run completed but no additional structured output was extracted. Check the ADK Web UI for details."
                )

        st.caption(
            f"Latest session: `{run_state['session_id']}` · [Open in ADK Web ↗]({run_state['ui_link']})"
        )
    else:
        st.caption("Run the agent to see generated results here.")

if submitted:
    if not query_text.strip():
        st.warning("Please enter a prompt before running the agent.")
    else:
        status = st.status("Preparing agent run…", expanded=True)
        status.write("Creating session via REST API…")
        session_id = create_session(agent_key, user_id)

        if session_id:
            session_url = _session_endpoints(agent_key, user_id, session_id)
            ui_link = f"{ADK_BASE_URL}/dev-ui/?app={agent_key}&session={session_id}"

            if agent_key == "market_trends_analyst":
                sse_container = nullcontext()
            else:
                sse_container = st.expander("Live SSE messages from /run_sse", expanded=False)
            started, sse_messages, sse_errors = run_agent_with_messages(
                agent_key,
                user_id,
                session_id,
                query_text.strip(),
                status,
                sse_container,
            )

            if started:
                status.update(label="Agent run started — polling for events…", state="running")
                final_summary, events, raw_session = poll_session_for_data(
                    agent_key,
                    user_id,
                    session_id,
                    status,
                )
                status.update(label="Agent run completed.", state="complete")
                st.session_state.agent_runs[agent_key] = {
                    "session_id": session_id,
                    "session_url": session_url,
                    "ui_link": ui_link,
                    "query": query_text.strip(),
                    "sse_messages": sse_messages,
                    "sse_errors": sse_errors,
                    "events": events,
                    "final_summary": final_summary,
                    "raw_session": raw_session,
                }
                run_state = st.session_state.agent_runs[agent_key]
            else:
                status.update(label="Agent run failed to start. See error above.", state="error")
                st.session_state.agent_runs[agent_key] = {
                    "session_id": session_id,
                    "session_url": session_url,
                    "ui_link": ui_link,
                    "query": query_text.strip(),
                    "sse_messages": sse_messages,
                    "sse_errors": sse_errors,
                    "events": [],
                    "final_summary": None,
                    "raw_session": None,
                }
                run_state = st.session_state.agent_runs[agent_key]
        else:
            st.error("Agent run could not be started. See details above.")

if run_state:
    st.divider()

    results_events = run_state.get("events", []) or []
    results_sse = run_state.get("sse_messages", []) or []

    st.subheader("Results Overview")
    st.info(
        f"Session ID: `{run_state['session_id']}`  ·  [Open in ADK Web ↗]({run_state['ui_link']})"
    )

    metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
    metrics_col1.metric("Events captured", len(results_events))
    metrics_col2.metric("SSE messages", len(results_sse))
    metrics_col3.metric(
        "Errors detected",
        len(run_state.get("sse_errors", []) or []),
        help="Errors surfaced while consuming the SSE stream.",
    )

    if agent_key != "market_trends_analyst":
        st.markdown("**Agent Summary**")
        if run_state.get("final_summary"):
            st.success(run_state["final_summary"])
        else:
            st.caption(
                "No final summary detected yet — open the session in ADK Web UI for details."
            )

    if run_state.get("sse_errors"):
        st.warning("\n".join(run_state["sse_errors"]))

    summary_tab, sse_tab, timeline_tab, raw_tab = st.tabs([
        "📝 Run Summary",
        "📡 SSE Stream",
        "🕒 Event Timeline",
        "🧾 Raw Session JSON",
    ])

    with summary_tab:
        st.subheader("What happened")
        st.markdown(
            f"- **Prompt:** `{run_state['query']}`\n"
            f"- **Session ID:** `{run_state['session_id']}`\n"
            f"- **ADK Web UI:** [Open trace ↗]({run_state['ui_link']})"
        )
        st.markdown(
            "**Next steps:**\n"
            "1. Inspect the timeline for intermediate outputs.\n"
            "2. Use the ADK Web UI to study tool calls, traces, and sessions.\n"
            "3. Apply instruction/tool tweaks as suggested in the agenda and rerun."
        )

    with sse_tab:
        st.subheader("Live SSE messages")
        if run_state["sse_messages"]:
            for idx, message in enumerate(run_state["sse_messages"], start=1):
                with st.expander(f"Message {idx}"):
                    st.json(message)
        else:
            st.caption("No SSE payloads were captured.")

    with timeline_tab:
        st.subheader("Session events")
        if run_state["events"]:
            for event in run_state["events"]:
                _render_event(event)
        else:
            st.caption("No events recorded yet—check the ADK Web UI for more details.")

    with raw_tab:
        st.subheader("Raw session payload")
        if run_state.get("raw_session"):
            st.json(run_state["raw_session"])
        else:
            st.caption("Raw session data not available.")

st.caption(
    "For deeper background, consult the internal hackathon agenda and related resources."
)
