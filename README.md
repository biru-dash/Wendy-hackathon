# Wendy's AI Agents Hackathon

Multi-agent AI system for generating data-driven promotional offers at Wendy's. This system uses specialized AI agents that collaborate to research market trends, analyze customer data, and design offer concepts.

## Table of Contents

- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [Multi-Agent System Overview](#multi-agent-system-overview)
- [System Architecture](#system-architecture)
- [Key Files](#key-files)

## Getting Started

### Prerequisites

- Python 3.10+
- Google Cloud SDK (`gcloud`) installed and authenticated
- Access to `cdp-tst-5fba` Google Cloud project
- Git installed

### Clone Repository

Clone the repository to your local machine:

```bash
git clone <repository-url>
cd Wendy-hackathon
```

Replace `<repository-url>` with the actual repository URL provided by organizers.

### Setup Instructions

**Important**: Use the commands for your operating system. Windows uses PowerShell commands, while Mac/Linux use bash commands.

#### Windows (PowerShell)

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# If you get an execution policy error, run this first:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Install dependencies
pip install google-adk google-cloud-aiplatform google-cloud-bigquery

# Authenticate with Google Cloud
# This will open a browser window - use your Wendy's email to sign in
gcloud auth application-default login

# (Optional) Set Google Cloud project for gcloud commands
# Note: This is optional - your .env file will set the project for the agents
# If you get a password prompt, you can skip this step
# gcloud config set project cdp-tst-5fba

# Configure environment variables
Copy-Item .env.example .env
# Edit .env file with your GCP project details

# Launch ADK Web Server
adk web src
```

**Windows Alternative** (if PowerShell activation doesn't work):
```cmd
# Use Command Prompt (cmd.exe) instead
venv\Scripts\activate.bat
```

#### Mac/Linux

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install google-adk google-cloud-aiplatform google-cloud-bigquery

# Authenticate with Google Cloud
# This will open a browser window - use your Wendy's email to sign in
gcloud auth application-default login

# (Optional) Set Google Cloud project for gcloud commands
# Note: This is optional - your .env file will set the project for the agents
# If you get a password prompt, you can skip this step
# gcloud config set project cdp-tst-5fba

# Configure environment variables
cp .env.example .env
# Edit .env file with your GCP project details

# Launch ADK Web Server
adk web src
```

### Access ADK Web Interface

1. Open browser to `http://localhost:8000`
2. Select "marketing_orchestrator" from agent dropdown menu
3. Enter your query in the chat interface

**Example Query**: "Develop three innovative offers to increase breakfast traffic among Gen Z customers during Q1 (January-March) breakfast hours (6am-11am)"

### Next Steps

For complete hackathon instructions, testing exercises, and modification guidelines, see:
- **[Hackathon Agenda](docs/hackathon_agenda.md)** - Complete guide with system overview, testing exercises, and modification tasks

## Project Structure

```
Wendy-hackathon/
├── src/                          # Agent source code
│   ├── marketing_orchestrator/   # Root orchestrator agent
│   │   ├── agent.py             # Main orchestrator (SequentialAgent)
│   │   └── README.md
│   │
│   ├── market_trends_analyst/   # Market research team
│   │   ├── agent.py             # Root agent (SequentialAgent)
│   │   └── sub_agents/
│   │       ├── data_collection/
│   │       │   ├── agent.py
│   │       │   ├── instruction.txt
│   │       │   └── tools.py
│   │       └── research_synthesis/
│   │           ├── agent.py
│   │           ├── instruction.txt
│   │           └── tools.py
│   │
│   ├── customer_insights/       # Customer analytics team
│   │   ├── agent.py             # Root agent (ParallelAgent)
│   │   ├── data/                # BigQuery data schemas and utilities
│   │   └── sub_agents/
│   │       ├── behavioral_analysis/
│   │       │   ├── agent.py
│   │       │   ├── instruction.txt
│   │       │   └── tools.py     # BigQuery tools (crm_database_tool)
│   │       ├── sentiment_analysis/
│   │       │   ├── agent.py
│   │       │   ├── instruction.txt
│   │       │   └── tools.py     # BigQuery tools (feedback_database_tool)
│   │       └── profile_synthesizer/
│   │           ├── agent.py
│   │           └── instruction.txt
│   │
│   ├── competitor_intelligence/ # Competitive analysis (optional)
│   │   ├── agent.py
│   │   └── sub_agents/
│   │       ├── target_identification/
│   │       ├── research_orchestrator/
│   │       ├── competitor_analysis/
│   │       └── whitespace_synthesizer/
│   │
│   ├── offer_design/            # Offer concept generation
│   │   ├── agent.py
│   │   └── sub_agents/
│   │       └── simplified_offer_design/
│   │           ├── agent.py
│   │           └── instruction.txt
│   │
│   └── utils/                   # Shared utilities
│       └── instruction_loader.py
│
├── docs/                        # Documentation
│   └── hackathon_agenda.md     # Complete hackathon guide
│
├── .gitignore                   # Git ignore rules
└── README.md                    # This file
```

## Multi-Agent System Overview

The system consists of specialized agent teams working together:

### 1. Market Trends Analyst

**Function**: Research market trends and consumer behaviors using web search

**Structure**:
- **Root Agent**: `MarketTrendsAnalystRoot` (SequentialAgent)
- **Sub-Agents**:
  1. **Data Collection Agent** - Uses Google Search to find URLs and trend data
  2. **Research Synthesis Agent** - Reads URLs, extracts insights, synthesizes trend briefs

**Workflow**:
```
Input Query → Data Collection (finds URLs) → Research Synthesis (analyzes content) → Trend Briefs
```

### 2. Customer Insights

**Function**: Analyze customer behavioral data from BigQuery

**Structure**:
- **Root Agent**: `CustomerInsightsManagerAgent` (ParallelAgent)
- **Sub-Agents**:
  1. **Behavioral Analysis Agent** - Analyzes numerical data (redemptions, visits, spend)
  2. **Sentiment Analysis Agent** - Analyzes text feedback (reviews, comments)
  3. **Profile Synthesizer Agent** - Combines quantitative and qualitative insights

**Workflow**:
```
Input Query → Behavioral Analysis (parallel) → Profile Synthesizer → Customer Profiles
              Sentiment Analysis (parallel)
```

### 3. Offer Design

**Function**: Synthesizes research into actionable offer concepts

**Structure**:
- **Root Agent**: `SimplifiedOfferDesignAgent` (LlmAgent)
- **Input**: Market trends, customer insights
- **Output**: 3 prioritized offer concepts

### 4. Marketing Orchestrator (Root Agent)

**Function**: Coordinates all teams in sequence

**Workflow**:
```
User Query
  ↓
Step 1: Market Trends Analyst → trend_briefs[]
  ↓
Step 2: Customer Insights → customer_insights, segment_profiles
  ↓
Step 3: Offer Design → 3 prioritized offer_concepts[] (final output)
```

**Note**: Competitor Intelligence is commented out by default. See hackathon agenda for advanced path.

## System Architecture

### Agent Types

- **SequentialAgent**: Executes sub-agents in order, passing results sequentially
- **ParallelAgent**: Executes sub-agents simultaneously for independent tasks
- **LlmAgent**: Single agent using Large Language Model with tools

### Data Flow

1. **Market Trends Analyst** (SequentialAgent)
   - Data Collection → Research Synthesis
   - Output: Trend briefs

2. **Customer Insights** (ParallelAgent)
   - Behavioral Analysis (parallel) → Profile Synthesizer
   - Sentiment Analysis (parallel)
   - Output: Customer profiles with metrics

3. **Offer Design** (LlmAgent)
   - Input: Trend briefs + Customer profiles
   - Output: 3 prioritized offer concepts

### ADK Web Features

- **Sessions**: Each conversation creates a session with full history
- **Events**: Step-by-step agent actions (tool calls, responses)
- **Trace**: Visual execution flow showing agent relationships and data flow

## Key Files

### Agent Configuration

- `src/marketing_orchestrator/agent.py` - Main orchestrator workflow
- `src/market_trends_analyst/agent.py` - Market trends root agent
- `src/customer_insights/agent.py` - Customer insights root agent
- `src/offer_design/sub_agents/simplified_offer_design/agent.py` - Offer design agent

### Instructions (Modify These)

- `src/market_trends_analyst/sub_agents/data_collection/instruction.txt`
- `src/market_trends_analyst/sub_agents/research_synthesis/instruction.txt`
- `src/customer_insights/sub_agents/behavioral_analysis/instruction.txt`
- `src/customer_insights/sub_agents/sentiment_analysis/instruction.txt`
- `src/customer_insights/sub_agents/profile_synthesizer/instruction.txt`
- `src/offer_design/sub_agents/simplified_offer_design/instruction.txt`

### Tools (Add/Modify These)

- `src/customer_insights/sub_agents/behavioral_analysis/tools.py` - BigQuery CRM tools
- `src/customer_insights/sub_agents/sentiment_analysis/tools.py` - BigQuery feedback tools
- `src/market_trends_analyst/sub_agents/data_collection/tools.py` - Search tools

### Data

- `src/customer_insights/data/BIGQUERY_TABLES_SUMMARY.md` - BigQuery schema documentation
- BigQuery datasets: CRM data, redemption logs, feedback data (read-only access)

## Documentation

- **[Hackathon Agenda](docs/hackathon_agenda.md)** - Complete hackathon guide with:
  - System overview and testing exercises
  - Agent modification instructions
  - Evaluation criteria
  - Quick reference

---

*For hackathon participants: See `docs/hackathon_agenda.md` for detailed instructions, testing exercises, and modification tasks.*
