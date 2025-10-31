# Hackathon UI - Streamlit Frontend

A Streamlit web application that acts as a "mission control" interface for the Wendy's multi-agent marketing system.

## Overview

The Hackathon UI provides a user-friendly interface to interact with the Marketing Orchestrator agents. It includes:
- **Input Levers**: Configure the AI team's focus and instructions
- **Visual Results**: Display generated offer concepts with mock ad images
- **Real-time Status**: Monitor agent execution progress

## Architecture

```
┌─────────────────┐         HTTP POST         ┌──────────────────┐
│  Streamlit UI   │ ────────────────────────> │   ADK API Server │
│  (Frontend)     │                           │   (Backend)      │
│  Port 8501      │ <──────────────────────── │   Port 8000      │
└─────────────────┘      JSON Response        └──────────────────┘
```

## Setup

### 1. Install Dependencies

```powershell
.\venv\Scripts\activate
pip install streamlit requests
```

Or use the requirements file:
```powershell
pip install -r requirements-ui.txt
```

### 2. Run the System

You need **two terminals** running simultaneously:

#### Option A: Manual Setup

**Terminal 1 - ADK API Server:**
```powershell
cd C:\Users\birup\Documents\wendy-hack-sprint
.\venv\Scripts\activate
adk api_server marketing_orchestrator
```

**Terminal 2 - Streamlit UI:**
```powershell
cd C:\Users\birup\Documents\wendy-hack-sprint
.\venv\Scripts\activate
streamlit run hackathon_ui.py
```

#### Option B: Use Launch Scripts (Recommended)

**Windows (PowerShell):**
```powershell
.\run_hackathon.ps1
```

**Windows (Batch):**
```cmd
.\run_hackathon.bat
```

These scripts automatically open two separate windows for each server.

### 3. Access the UI

Once both servers are running:
- **Streamlit UI**: http://localhost:8501 (opens automatically)
- **ADK API Server**: http://localhost:8000 (backend, no direct access needed)

## Features

### Input Levers (Sidebar)

1. **Strategic Challenge**: Enter your marketing goal or question
2. **Model Selection**: Choose which Gemini model style to emulate
3. **Agent Focus**: Select which research agents to prioritize
   - MarketTrendsAgent
   - CustomerInsightsAgent
   - CompetitorIntelAgent
4. **Custom Instructions**: Add specific guidance for the AI team

### Output Display

1. **Offer Concepts**: Visual cards showing:
   - Concept name and priority
   - AI-generated ad mockup (placeholder)
   - Detailed mechanic
   - Data-driven rationale
   - Implementation details

2. **Debug View**: Full raw JSON output for judges/developers

3. **Summary Metrics**: Counts of concepts, priorities, and agents used

## Usage Workflow

1. **Configure Levers** in the sidebar
2. **Click "🚀 Generate Offers"**
3. **Watch Progress** as agents execute
4. **Review Results** with offer concepts displayed
5. **Use Mock Ads** for presentations (Nano Banana integration ready)

## Example Queries

- "Develop offers to increase breakfast traffic among Gen Z"
- "Find gaps in our market positioning vs competitors"
- "Design app-exclusive offers for value-driven customers"
- "Create gamified promotions to boost app engagement"
- "Identify opportunities for family-sized meal offers"

## Troubleshooting

### "Failed to connect to ADK server"

**Problem**: Streamlit can't reach the ADK API server

**Solutions**:
1. Ensure ADK server is running: `adk api_server marketing_orchestrator`
2. Check port 8000 is not in use
3. Verify URL: `http://localhost:8000/apps/marketing_orchestrator:run`

### "Request timed out"

**Problem**: Agent execution takes too long

**Solutions**:
1. Increase timeout in `hackathon_ui.py` (currently 600 seconds)
2. Simplify your query
3. Disable some agents (e.g., CompetitorIntelAgent)

### "No offer concepts returned"

**Problem**: Agent runs but doesn't return structured data

**Solutions**:
1. Check "Show Full Raw Output" expander to see actual response
2. Verify SimplifiedOfferDesignAgent is outputting proper format
3. The UI will attempt to parse text output if JSON isn't available

## Integration with Nano Banana

The UI includes a `mock_nano_banana()` function that simulates image generation. To integrate with actual Nano Banana API:

1. Replace `mock_nano_banana()` function
2. Add API key configuration
3. Call the actual image generation endpoint

```python
def call_nano_banana(offer_name: str, offer_details: dict) -> str:
    """Call actual Nano Banana API for image generation"""
    # Implementation here
    pass
```

## Customization

### Styling

Edit `st.set_page_config()` to customize:
- Page title
- Layout (wide/narrow)
- Sidebar state

### Colors

Streamlit uses theme configuration. Create `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#DA291C"  # Wendy's Red
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
```

### Ad Placeholders

Modify `mock_nano_banana()` to use different placeholder images or integrate real image generation.

## Development

### File Structure

```
wendy-hack-sprint/
├── hackathon_ui.py          # Main Streamlit app
├── run_hackathon.ps1        # PowerShell launcher
├── run_hackathon.bat        # Batch launcher
├── requirements-ui.txt      # UI dependencies
└── marketing_orchestrator/  # Agent system
```

### Adding Features

1. **New Input Levers**: Add to sidebar section
2. **Enhanced Display**: Modify `format_offer_card()` function
3. **Status Monitoring**: Expand progress tracking section

## Notes

- The UI expects the SimplifiedOfferDesignAgent to output structured offer concepts
- Mock image generation uses themed placeholders (replace with real API)
- Session state is used minimally (can be expanded for multi-session support)
- All agent communication happens via HTTP POST to ADK API

## Production Considerations

For production deployment:

1. **Security**:
   - Add authentication
   - Secure ADK API endpoint
   - Validate inputs

2. **Performance**:
   - Add caching for repeated queries
   - Implement async requests
   - Add loading states

3. **Monitoring**:
   - Log all queries
   - Track agent performance
   - Monitor API response times

