# Competitor Intelligence Agent

## Architecture Overview

The Competitor Intelligence agent follows a sequential orchestration pattern with parallel research capabilities, similar to the deep research agent design pattern from the Google ADK blog post.

## Root Agent

**CompetitorIntelManagerAgent** (`agent.py`)
- Type: `SequentialAgent`
- Orchestrates the complete workflow from competitor identification through strategic synthesis

## Sub-Agents (Executed in Order)

### 1. TargetIdentificationAgent (The "Scout")
- **Purpose**: Identifies competitors and their digital assets to research
- **Type**: `LlmAgent`
- **Tools**: `google_search`
- **Location**: `sub_agents/target_identification/`

**Workflow**:
- Receives research goal from user
- Uses Google Search to find Wendy's top QSR competitors
- Extracts clean list of brand names, websites, and app names
- Outputs structured COMPETITOR_LIST

### 2. ResearchOrchestratorAgent (The "Team Lead")
- **Purpose**: Manages parallel research of all identified competitors
- **Type**: `LlmAgent` with `AgentTool` delegation
- **Tools**: `competitor_analysis_tool` (AgentTool wrapping CompetitorAnalysisAgent)
- **Location**: `sub_agents/research_orchestrator/`

**Workflow**:
- Receives COMPETITOR_LIST from TargetIdentificationAgent
- For each competitor, calls CompetitorAnalysisAgent tool
- Collects all structured profiles
- Outputs complete COMPETITIVE_LANDSCAPE

**Parallel Execution Note**: While ADK's ParallelAgent supports running multiple different agents in parallel, ResearchOrchestratorAgent uses an AgentTool pattern to call CompetitorAnalysisAgent multiple times (once per competitor). The ADK framework handles efficient execution of these calls.

### 3. CompetitorAnalysisAgent (The "Specialist")
- **Purpose**: Researches a single competitor's promotions and loyalty programs
- **Type**: `LlmAgent`
- **Tools**: `google_search`, `web_scraper_tool` (when available)
- **Location**: `sub_agents/competitor_analysis/`

**Workflow**:
- Receives one competitor target (name, website, app)
- Uses Google Search to find recent promotions, press releases, loyalty program details
- Uses web scraper to extract content from competitor websites
- Builds structured COMPETITOR_PROFILE for that one competitor

**Note**: This agent is invoked by ResearchOrchestratorAgent via AgentTool, allowing it to be called multiple times for different competitors.

### 4. WhitespaceSynthesizerAgent (The "Strategist")
- **Purpose**: Analyzes competitive landscape and identifies strategic whitespace opportunities
- **Type**: `LlmAgent` (model-only, no tools)
- **Location**: `sub_agents/whitespace_synthesizer/`

**Workflow**:
- Receives complete COMPETITIVE_LANDSCAPE from ResearchOrchestratorAgent
- Compares competitor strategies to Wendy's current offerings
- Identifies gaps and whitespace opportunities
- Outputs structured WHITESPACE_OPPORTUNITIES with recommendations

## Directory Structure

```
competitor_intelligence/
├── __init__.py
├── agent.py                          # Root agent: CompetitorIntelManagerAgent
├── root_agent_instruction.txt        # Root agent instructions
├── README.md                         # This file
├── sub_agents/
│   ├── __init__.py
│   ├── target_identification/
│   │   ├── __init__.py
│   │   ├── agent.py
│   │   └── instruction.txt
│   ├── research_orchestrator/
│   │   ├── __init__.py
│   │   ├── agent.py
│   │   └── instruction.txt
│   ├── competitor_analysis/
│   │   ├── __init__.py
│   │   ├── agent.py
│   │   └── instruction.txt
│   └── whitespace_synthesizer/
│       ├── __init__.py
│       ├── agent.py
│       └── instruction.txt
└── tools/
    ├── __init__.py
    └── agent_tools.py                 # AgentTool for CompetitorAnalysisAgent
```

## Usage

Run the agent using ADK:

```bash
adk web competitor_intelligence
```

Example user prompts:
- "Find gaps in our market"
- "Analyze competitor loyalty programs"
- "Identify whitespace opportunities in QSR promotions"

## Key Design Patterns

1. **Sequential Orchestration**: Root agent uses SequentialAgent to execute sub-agents in order
2. **AgentTool Delegation**: ResearchOrchestratorAgent uses AgentTool to call CompetitorAnalysisAgent multiple times
3. **Specialized Agents**: Each agent has a single, focused responsibility
4. **State Passing**: Agents pass structured outputs between stages via conversation context

## Future Enhancements

- Implement `web_scraper_tool` for CompetitorAnalysisAgent (currently placeholder)
- Add caching mechanism for competitor profiles to avoid redundant research
- Integrate with competitive intelligence databases for more structured data
- Add performance tracking and metrics collection

