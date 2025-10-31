# Offer Design Agent

## Architecture Overview

The Offer Design agent follows a sequential pipeline pattern, unlike the research-oriented agents. It takes synthesized inputs from other agents (Market Trends, Customer Insights, Competitor Intelligence) and transforms them into actionable offer concepts through a "virtual assembly line" of specialist agents.

## Root Agent

**OfferDesignManagerAgent** (`agent.py`)
- Type: `SequentialAgent`
- Orchestrates a 4-stage synthesis pipeline from raw ideas to prioritized concepts

## Sub-Agents (Executed in Sequential Order)

### 1. ConceptGenerationAgent (The "Creative Brainstormer")
- **Purpose**: Generates a wide list of raw creative offer ideas
- **Type**: `LlmAgent` (model-only, no tools)
- **Location**: `sub_agents/concept_generation/`

**Workflow**:
- Receives market trends, customer insights, and whitespace opportunities
- Combines signals creatively to generate 10-15 candidate concepts
- Outputs structured RAW_CONCEPTS list

### 2. OfferDefinitionAgent (The "Structurer")
- **Purpose**: Takes raw ideas and structures them into defined offers
- **Type**: `LlmAgent` (model-only, no tools)
- **Location**: `sub_agents/offer_definition/`

**Workflow**:
- Receives RAW_CONCEPTS from ConceptGenerationAgent
- Selects top 3-5 strongest concepts
- Defines full structure: mechanic, channel, duration, target segment, offer structure
- Outputs DEFINED_OFFERS

### 3. RationaleAgent (The "Strategist")
- **Purpose**: Provides strategic rationale and cites evidence for each offer
- **Type**: `LlmAgent` (model-only, no tools)
- **Location**: `sub_agents/rationale/`

**Workflow**:
- Receives DEFINED_OFFERS and original input briefs
- Maps each design decision to supporting evidence
- Cites specific sources: Market Trends agent, Customer Insights agent, Competitor Intel agent
- Outputs OFFERS_WITH_RATIONALE

### 4. PrioritizationAgent (The "Business Analyst")
- **Purpose**: Ranks offers by feasibility and expected impact
- **Type**: `LlmAgent` (model-only, no tools)
- **Location**: `sub_agents/prioritization/`

**Workflow**:
- Receives OFFERS_WITH_RATIONALE
- Evaluates feasibility (Easy/Medium/Hard) and expected impact (High/Medium/Low)
- Ranks offers by priority
- Outputs FINAL_OFFER_CONCEPTS (ranked list)

## Directory Structure

```
offer_design/
├── __init__.py
├── agent.py                          # Root agent: OfferDesignManagerAgent
├── root_agent_instruction.txt        # Root agent instructions
├── README.md                         # This file
├── .env                              # Vertex AI configuration
└── sub_agents/
    ├── __init__.py
    ├── concept_generation/
    │   ├── __init__.py
    │   ├── agent.py
    │   └── instruction.txt
    ├── offer_definition/
    │   ├── __init__.py
    │   ├── agent.py
    │   └── instruction.txt
    ├── rationale/
    │   ├── __init__.py
    │   ├── agent.py
    │   └── instruction.txt
    └── prioritization/
        ├── __init__.py
        ├── agent.py
        └── instruction.txt
```

## Usage

Run the agent using ADK:

```bash
cd C:\Users\birup\Documents\wendy-hack-sprint
.\venv\Scripts\activate
adk web offer_design
```

**Input Requirements**:
This agent expects to receive outputs from upstream agents:
- Market Trends Analyst: `trend_briefs`
- Customer Insights: `customer_insights`, `segment_profiles`
- Competitor Intelligence: `whitespace_opportunities`

**Example User Prompts**:
- "Generate offer concepts based on recent market trends and customer insights"
- "Design offers that address competitor gaps and align with our customer segments"
- "Create prioritized offer concepts combining all intelligence inputs"

## Key Design Patterns

1. **Sequential Pipeline**: Each agent builds on the previous one's output
2. **Model-Only Agents**: All sub-agents are pure LLM agents with no tools
3. **Evidence-Based Design**: RationaleAgent explicitly cites supporting evidence
4. **Business Prioritization**: Final agent ranks concepts by feasibility and impact

## Pipeline Flow

```
Input Signals (Market Trends + Customer Insights + Competitor Intel)
    ↓
[ConceptGenerationAgent] → RAW_CONCEPTS (10-15 ideas)
    ↓
[OfferDefinitionAgent] → DEFINED_OFFERS (3-5 structured offers)
    ↓
[RationaleAgent] → OFFERS_WITH_RATIONALE (with evidence citations)
    ↓
[PrioritizationAgent] → FINAL_OFFER_CONCEPTS (ranked list)
    ↓
Output: Prioritized, evidence-based offer concepts
```

## Output Format

The final output includes:
- Ranked list of offer concepts
- Full definitions (mechanic, channel, duration, segment, structure)
- Strategic rationale with evidence citations
- Feasibility assessment (Easy/Medium/Hard)
- Expected impact assessment (High/Medium/Low)
- Implementation recommendations

## Notes

- All agents are model-only (no tools required)
- Each agent specializes in one aspect of the synthesis process
- The pipeline ensures quality through sequential refinement
- Evidence citations link design decisions back to source intelligence

