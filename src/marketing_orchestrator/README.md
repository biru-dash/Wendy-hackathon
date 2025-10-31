# Marketing Orchestrator Agent - Simplified Architecture

## Architecture Overview

The Marketing Orchestrator is the **root agent** for the entire system. It is the only agent users interact with directly. The architecture has been **simplified** for easier understanding and debugging during hackathons.

## Simplified Flow (Active)

**MarketingOrchestratorAgent** (SequentialAgent - Root)
- Manages end-to-end workflow in 4 sequential steps
- Each specialist agent runs one after another (easier to follow)

### Sequential Steps:

1. **MarketTrendsAnalystRoot**: Market trends research
   - Output: `trend_briefs[]`

2. **CustomerInsightsManagerAgent**: Customer insights research  
   - Output: `customer_insights`, `segment_profiles`

3. **CompetitorIntelManagerAgent**: Competitor intelligence research
   - Output: `whitespace_opportunities[]`
   - **Can be disabled** by commenting out in `agent.py`

4. **SimplifiedOfferDesignAgent**: Single-step offer design
   - Performs: generation, structuring, rationale, and prioritization in one pass
   - Output: `offer_concepts[]` (ranked, evidence-based)

## Key Simplifications

### ✅ What Changed:
- **Removed ResearchSquadAgent**: Research agents run sequentially instead of in parallel
- **Simplified Offer Design**: Replaced 4-step pipeline (ConceptGeneration → Definition → Rationale → Prioritization) with single `SimplifiedOfferDesignAgent`
- **Direct Agent Calls**: Orchestrator calls specialist agents directly (no intermediate layers)
- **Slower but Clearer**: Sequential execution is easier to debug and understand

### 🔒 What's Disabled (Not Deleted):
- `ResearchSquadAgent`: Commented out but kept in `marketing_orchestrator/sub_agents/research_squad/`
- `OfferDesignManagerAgent`: Still exists with full 4-step pipeline in `offer_design/agent.py`

### 🔄 How to Re-enable Complex Architecture:
1. In `marketing_orchestrator/agent.py`, comment out the simplified imports and uncomment the disabled ones
2. Change `simplified_offer_design_agent` to `offer_design_manager_agent`
3. Change individual agent imports to `research_squad_agent`
4. The full parallel architecture will be active again

## Directory Structure

```
marketing_orchestrator/
├── __init__.py
├── agent.py                          # Root agent: MarketingOrchestratorAgent (SIMPLIFIED)
├── root_agent_instruction.txt        # Root agent instructions
├── README.md                         # This file
├── .env                              # Vertex AI configuration
└── sub_agents/
    └── research_squad/               # DISABLED but kept for future use
        ├── __init__.py
        ├── agent.py                  # ResearchSquadAgent (ParallelAgent)
        └── instruction.txt
```

## Simplified Architecture Flow

```
User Input
    ↓
MarketingOrchestratorAgent (Root SequentialAgent)
    ↓
    ├─ Step 1: MarketTrendsAnalystRoot ──→ trend_briefs[]
    ↓
    ├─ Step 2: CustomerInsightsManagerAgent ──→ customer_insights
    ↓
    ├─ Step 3: CompetitorIntelManagerAgent ──→ whitespace_opportunities[]
    ↓
    └─ Step 4: SimplifiedOfferDesignAgent (Single LlmAgent)
        ├─ Generates ideas
        ├─ Structures offers
        ├─ Adds rationale
        ├─ Prioritizes
        ↓
        FINAL: offer_concepts[] (ranked list)
```

## Usage

**Run the simplified orchestrator**:

```bash
cd C:\Users\birup\Documents\wendy-hack-sprint
.\venv\Scripts\activate
adk web marketing_orchestrator
```

**Example User Prompts**:
- "Analyze weekday lunch offers"
- "Find gaps in our market"
- "Research family-sized meal trends"
- "Design offers for value-driven customers"

## Disabling Agents for Testing

To disable `CompetitorIntelManagerAgent` for simplified testing:

1. Open `marketing_orchestrator/agent.py`
2. Comment out the active line:
   ```python
   # competitor_intel_manager_agent,        # Step 3: Competitor Intelligence research
   ```
3. Update `SimplifiedOfferDesignAgent` instruction to not reference competitor data:
   - Open `offer_design/sub_agents/simplified_offer_design/instruction.txt`
   - Remove mentions of "Competitor Intelligence" in examples

To re-enable: Simply uncomment the line.

## Output Format

Final output includes:
- **Ranked list** of 3 offer concepts (by priority)
- **Full definitions**: mechanic, channel, duration, target segment, structure
- **Strategic rationale**: with explicit citations to Market Trends, Customer Insights, (and Competitor Intelligence if enabled)
- **Feasibility assessment**: Easy/Medium/Hard
- **Expected impact**: High/Medium/Low
- **Implementation recommendations**: Prioritized launch sequence

## Benefits of Simplified Architecture

✅ **Easier to Debug**: Sequential execution shows clear step-by-step progress
✅ **Easier to Understand**: No complex parallel orchestration layers
✅ **Easier to Modify**: Agents can be individually enabled/disabled
✅ **Faster Development**: Less moving parts means faster iteration
✅ **Maintainable**: Clear structure for hackathon timelines

## Notes

- This simplified architecture prioritizes **clarity and maintainability** over maximum speed
- Research runs sequentially (slower but easier to debug)
- Offer design is a single-step process (less precise but faster to iterate)
- All original complex agents are preserved and can be re-enabled easily
- The system is production-ready with this simplified approach
