# Wendy's AI Agents Hackathon

**Date**: November 10, 2025  
**Time**: 10:30 AM - 12:00 PM (90 minutes)  

## Overview

Participants will modify and enhance Wendy's multi-agent AI system by updating agent instructions, tools, and models. The system uses Market Trends Analyst and Customer Insights agents to generate offer concepts.

## Hackathon Goal

**"Develop three innovative offers to increase breakfast traffic among Gen Z customers during Q1 (January-March) breakfast hours (6am-11am)"**

**Goal Parameters:**
- Customer Segment: Gen Z customers (ages 18-27)
- Time Period: Q1 (January-March)
- Daypart: Breakfast hours (6am-11am)
- Objective: Increase breakfast traffic and engagement
- Output: Three prioritized offer concepts with rationale

**Rationale:**
- Breakfast is an underperforming daypart for QSRs
- Gen Z is a key growth segment with distinct preferences
- Q1 presents seasonal challenges (post-holiday, winter weather)
- Breakfast requires different strategies than lunch/dinner

**Task**: Modify generic instructions and tools to align with this goal.

## Schedule

| Time | Activity |
|------|----------|
| 10:30 - 10:40 AM | Setup (10 min) |
| 10:40 - 11:15 AM | System Overview and Testing (35 min) |
| 11:15 - 11:45 AM | Agent Modifications (30 min) |
| 11:45 - 12:00 PM | Demos & Evaluation (15 min) |

## Setup (10:30 - 10:40 AM)

### Prerequisites

- Python 3.10+
- Google Cloud SDK (`gcloud`) installed and authenticated
- Access to `gemini-copilot-testing` Google Cloud project
- Git installed

### Clone Repository

Clone the repository to your local machine:

```bash
git clone <repository-url>
cd Wendy-hackathon
```

Replace `<repository-url>` with the actual repository URL provided by organizers.

### Environment Setup

#### Mac/Linux

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install google-adk google-cloud-aiplatform google-cloud-bigquery

# Authenticate with Google Cloud
gcloud auth application-default login

# Set Google Cloud project
gcloud config set project gemini-copilot-testing

# Launch ADK Web Server
adk web src
```

#### Windows

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate

# Install dependencies
pip install google-adk google-cloud-aiplatform google-cloud-bigquery

# Authenticate with Google Cloud
gcloud auth application-default login

# Set Google Cloud project
gcloud config set project gemini-copilot-testing

# Launch ADK Web Server
adk web src
```

### Access ADK Web Interface

1. Open browser to `http://localhost:8000`
2. Select "marketing_orchestrator" from agent dropdown
3. Use the fixed goal query for testing

### System Components

- Multi-Agent System: Market Trends Analyst, Customer Insights, Offer Design
- ADK Web Interface: Testing and debugging interface
- Instruction Files: Text files controlling agent behavior
- Tools: Python functions available to agents
- BigQuery Datasets: Customer data (read-only access)
- Advanced Path: Competitor Intelligence (optional, commented out by default)

## System Overview and Testing (10:40 - 11:15 AM)

### ADK Web Interface Components

**Sessions**: Each conversation creates a session with full conversation history.

**Events**: Individual actions agents take (e.g., "Agent started", "Tool called", "Response generated"). Events show step-by-step execution.

**Trace**: Visual execution flow showing which agents ran, their relationships, timing, and data flow.

### 1. Market Trends Analyst

**Function**: Research market trends and consumer behaviors using web search

**Structure**:

**Root Agent**: `MarketTrendsAnalystRoot` (SequentialAgent)

**Sub-Agents**:

1. **Data Collection Agent**
   - Role: Collects raw data sources
   - Function: Uses Google Search to find URLs and trend data
   - Tools: `google_search`
   - File: `src/market_trends_analyst/sub_agents/data_collection/instruction.txt`

2. **Research Synthesis Agent**
   - Role: Analyzes collected data
   - Function: Reads URLs, extracts insights, synthesizes trend briefs
   - Tools: `web_scraper_tool`
   - File: `src/market_trends_analyst/sub_agents/research_synthesis/instruction.txt`

**Workflow**:
```
Input: Fixed goal query
  ↓
Data Collection Agent: Finds URLs about Gen Z breakfast trends, Q1 QSR campaigns
  ↓
Research Synthesis Agent: Reads articles, identifies breakfast-specific trends
  ↓
Output: Trend briefs focused on breakfast and Gen Z
```

**Testing Exercise**:

1. In ADK Web, select `market_trends_analyst`
2. Run test query: "Develop three innovative offers to increase breakfast traffic among Gen Z customers during Q1 (January-March) breakfast hours (6am-11am)"
3. Observe session events appearing in real-time
4. View trace to see execution flow:
   ```
   MarketTrendsAnalystRoot (SequentialAgent)
     ├─ DataCollectionAgent (LlmAgent)
     │   ├─ Event: google_search tool called
     │   └─ Event: URLs collected
     └─ ResearchSynthesisAgent (LlmAgent)
         ├─ Event: web_scraper_tool called (for each URL)
         └─ Event: Trend briefs generated
   ```
5. Review event list to see tool calls and data flow

### 2. Customer Insights

**Function**: Analyze customer behavioral data from BigQuery

**Structure**:

**Root Agent**: `CustomerInsightsManagerAgent` (ParallelAgent)

**Sub-Agents**:

1. **Behavioral Analysis Agent**
   - Role: Analyzes numerical data (redemptions, visits, spend)
   - Function: Queries BigQuery for transaction patterns, calculates metrics
   - Tools: `crm_database_tool`
   - File: `src/customer_insights/sub_agents/behavioral_analysis/instruction.txt`

2. **Sentiment Analysis Agent**
   - Role: Analyzes text feedback (reviews, comments)
   - Function: Queries feedback data, extracts sentiment and key phrases
   - Tools: `feedback_database_tool`
   - File: `src/customer_insights/sub_agents/sentiment_analysis/instruction.txt`

3. **Profile Synthesizer Agent**
   - Role: Combines quantitative and qualitative insights
   - Function: Creates customer profiles from behavioral and sentiment data
   - Tools: None (read-only BigQuery access)
   - File: `src/customer_insights/sub_agents/profile_synthesizer/instruction.txt`

**Workflow**:
```
Input: Fixed goal query
  ↓
Behavioral Analysis: Analyzes breakfast transactions → "12% of Gen Z app users visit for breakfast, 1.8x lift"
Sentiment Analysis: Analyzes breakfast reviews → "Gen Z customers say 'convenient morning', 'quick breakfast'"
  ↓ (Both run in parallel)
Profile Synthesizer: Combines both → "Gen Z breakfast customers prefer quick, convenient, app-exclusive morning offers"
  ↓
Output: Gen Z breakfast segment profiles with metrics and messaging
```

**Testing Exercise**:

1. Select `customer_insights`
2. Run test query: "Develop three innovative offers to increase breakfast traffic among Gen Z customers during Q1 (January-March) breakfast hours (6am-11am)"
3. Observe trace showing Behavioral Analysis and Sentiment Analysis running simultaneously
4. Note Profile Synthesizer runs after both complete
5. Compare with Market Trends sequential execution pattern

### 3. Offer Design

**Function**: Synthesizes research into actionable offer concepts

**Structure**:

**Root Agent**: `SimplifiedOfferDesignAgent` (LlmAgent)

**Input**: Market trends, customer insights, competitor intelligence (if available)

**Output**: 3 prioritized offer concepts

**File**: `src/offer_design/sub_agents/simplified_offer_design/instruction.txt`

**Workflow**:
```
Input: 
  - Market Trends: "Breakfast convenience trending, 35% Gen Z morning engagement"
  - Customer Insights: "Gen Z breakfast users prefer app, 1.8x lift for breakfast offers"
  ↓
Simplified Offer Design Agent:
  - Generates 5-7 breakfast-focused ideas
  - Selects top 3 for Gen Z breakfast in Q1
  - Adds rationale, feasibility, impact
  ↓
Output: 3 prioritized breakfast offer concepts
```

### 4. Marketing Orchestrator

**Function**: Coordinates all teams in sequence

**File**: `src/marketing_orchestrator/agent.py`

**Workflow** (Current Configuration):
```
Input: Fixed goal query
  ↓
Step 1: Market Trends Analyst → breakfast trend_briefs[] (Gen Z, Q1 focused)
  ↓
Step 2: Customer Insights → Gen Z breakfast customer_insights, segment_profiles
  ↓
Step 3: Offer Design → 3 prioritized breakfast offer_concepts[] (final output)
```

**Note**: Competitor Intelligence is commented out by default. See "Advanced Path" section to enable.

**Testing Exercise**:

1. Select `marketing_orchestrator`
2. Run test query: "Develop three innovative offers to increase breakfast traffic among Gen Z customers during Q1 (January-March) breakfast hours (6am-11am)"
3. Observe trace showing 3 steps (Market Trends → Customer Insights → Offer Design)
4. Analyze events to see data transformation at each step
5. Note differences between sequential and parallel execution patterns

## Agent Modifications (11:15 - 11:45 AM)

### Modifiable Components

#### 1. Instructions
- Location: `src/[agent]/sub_agents/[sub_agent]/instruction.txt`
- Impact: Changes agent behavior, focus, and output quality

#### 2. Tools
- Location: `src/[agent]/sub_agents/[sub_agent]/tools.py`
- Impact: Adds new capabilities or improves existing ones

#### 3. Models
- Location: In agent.py files, `model=os.getenv("GEN_FAST_MODEL", "gemini-2.5-flash")`
- Impact: Changes reasoning quality, speed, cost

### Task 1: Improve Instructions (20 min)

#### Data Collection Agent

1. Open: `src/market_trends_analyst/sub_agents/data_collection/instruction.txt`
2. Review current instruction
3. Run baseline test with `marketing_orchestrator` using fixed goal query
4. Save output
5. Modify instructions to be specific to goal:
   - Add: "Focus on breakfast trends relevant to Gen Z"
   - Add: "Consider Q1 seasonal factors (post-holiday, winter weather)"
   - Add: "Prioritize trends from breakfast daypart (6am-11am)"
6. Save file
7. Test again with same query
8. Compare outputs
9. Review trace to verify behavior changes

#### Behavioral Analysis Agent

1. Open: `src/customer_insights/sub_agents/behavioral_analysis/instruction.txt`
2. Review "Hackathon Challenge" marker
3. Run baseline test with `marketing_orchestrator` using fixed goal query
4. Save output
5. Address Hackathon Challenge:
   - Add: "Focus analysis on Gen Z customer segments (ages 18-27)"
   - Add: "Analyze breakfast-specific behavioral patterns (6am-11am visits)"
   - Add: "Consider Q1 seasonal patterns in customer behavior"
   - Add: "Always include percentage comparisons when analyzing segments"
   - Add: "Compare metrics across at least 3 different Gen Z segments"
6. Test and compare outputs
7. Verify outputs focus on Gen Z and breakfast
8. Confirm cross-segment comparisons and actionable insights

### Advanced Path: Competitor Intelligence (Optional)

To enable Competitor Intelligence:

#### Step 1: Enable

1. Open: `src/marketing_orchestrator/agent.py`
2. Uncomment:
   ```python
   from src.competitor_intelligence.agent import competitor_intel_manager_agent
   ```
3. In sub_agents list, uncomment: `competitor_intel_manager_agent,`
4. Restart ADK Web Server: Stop server (Ctrl+C), run `adk web src` again

#### Step 2: Competitor Intelligence Agents

**Root Agent**: `CompetitorIntelManagerAgent` (SequentialAgent)

**Sub-Agents**:

1. **Target Identification Agent**
   - Role: Identifies competitors to research
   - Tools: `google_search`
   - File: `src/competitor_intelligence/sub_agents/target_identification/instruction.txt`

2. **Research Orchestrator Agent**
   - Role: Coordinates research across multiple competitors using AgentTool
   - Tools: `competitor_analysis_tool` (AgentTool)
   - File: `src/competitor_intelligence/sub_agents/research_orchestrator/instruction.txt`

3. **Competitor Analysis Agent**
   - Role: Researches one specific competitor in detail
   - Tools: `google_search`
   - File: `src/competitor_intelligence/sub_agents/competitor_analysis/instruction.txt`

4. **Whitespace Synthesizer Agent**
   - Role: Identifies opportunities where Wendy's can compete
   - File: `src/competitor_intelligence/sub_agents/whitespace_synthesizer/instruction.txt`

#### Step 3: Improve Competitor Intelligence Instructions

1. Open: `src/competitor_intelligence/sub_agents/competitor_analysis/instruction.txt`
2. Review Hackathon Challenge
3. Add requirements:
   - "Focus on competitor breakfast offerings and promotions"
   - "Research how competitors target Gen Z for breakfast"
   - "Analyze Q1 seasonal breakfast campaigns"
   - "Include breakfast pricing strategies and morning promotions"
   - "Include specific examples with metrics when available"
4. Test with fixed goal query
5. Verify improved focus on breakfast and Gen Z competitive strategies

#### Step 4: Test Full Workflow

With Competitor Intelligence enabled, workflow becomes:
```
Step 1: Market Trends Analyst → trend_briefs[]
Step 2: Customer Insights → customer_insights, segment_profiles
Step 3: Competitor Intelligence → whitespace_opportunities[]
Step 4: Offer Design → 3 prioritized offer_concepts[]
```

**Note**: This adds an additional step, increasing execution time. Only enable if time permits and competitive intelligence is required for final output.

### Task 2: Modify Tools (Optional, 10 min)

#### Add Redemption Log Tool

1. Open: `src/customer_insights/sub_agents/behavioral_analysis/tools.py`
2. Review existing `crm_database_tool`
3. Add `redemption_log_tool`:
   - Function exists in `tools.py`
   - Wrapped as `redemption_log_tool = FunctionTool(redemption_log_tool)` at bottom
   - In `agent.py`, import: `from .tools import redemption_log_tool`
   - In `get_behavioral_tools()`, add: `return [crm_database_tool, redemption_log_tool]`
4. Modify tool to focus on breakfast redemption patterns:
   - Add filters for Gen Z segments
   - Add filters for breakfast time periods
5. Test with fixed goal query

## Demos & Evaluation (11:45 AM - 12:00 PM)

### Demo Format (2 minutes per team)

1. **System Understanding** (30 sec):
   - Explain one agent workflow using trace/session
   - Demonstrate ADK Web debugging usage

2. **Before/After Comparison** (30 sec):
   - Run same query with original vs. modified instructions
   - Highlight key differences

3. **Modifications** (30 sec):
   - What was modified and rationale
   - How trace/events verified changes

4. **Business Impact** (30 sec):
   - Value to Wendy's marketing
   - Actionable insights generated

### Evaluation Criteria (Total: 50 points)

| Criterion | Points | Focus |
|-----------|--------|-------|
| **Understanding** | 15 | Demonstrates understanding of multi-agent system, effective use of trace/events |
| **Output Quality** | 20 | Better insights, more actionable, specific metrics, improved structure |
| **Innovation** | 10 | Creative modifications, unique approach, experimentation |
| **Business Value** | 5 | Clear value to Wendy's marketing, actionable recommendations |

**Winners**: Top 3 teams by total score

## Reference

### Key Files to Modify

**Instructions**:
- `src/market_trends_analyst/sub_agents/data_collection/instruction.txt`
- `src/market_trends_analyst/sub_agents/research_synthesis/instruction.txt`
- `src/customer_insights/sub_agents/behavioral_analysis/instruction.txt`
- `src/customer_insights/sub_agents/sentiment_analysis/instruction.txt`
- `src/competitor_intelligence/sub_agents/competitor_analysis/instruction.txt`
- `src/offer_design/sub_agents/simplified_offer_design/instruction.txt`

**Tools**:
- `src/customer_insights/sub_agents/behavioral_analysis/tools.py`
- `src/market_trends_analyst/sub_agents/data_collection/tools.py`

### ADK Web Features

- **Sessions**: Each conversation is a session
- **Events**: Step-by-step agent actions
- **Trace**: Visual execution flow
- **Select Agent**: Choose individual agents or orchestrator
- **View Details**: Click on events to see data

### Fixed Test Query

All participants use this query:
```
Develop three innovative offers to increase breakfast traffic among Gen Z customers during Q1 (January-March) breakfast hours (6am-11am)
```

**Rationale**:
- Enables fair comparison across participants
- Allows objective evaluation of improvements
- Focuses effort on agent improvements, not goal variation

### Available Data

See `src/customer_insights/data/BIGQUERY_TABLES_SUMMARY.md`:
- CRM data (visits, spend, segments)
- Redemption logs (offer history, lift metrics)
- Feedback data (sentiment, reviews)
- **Note**: Read-only access

### Agent Focus

**Core Agents**:
1. Market Trends Analyst - Research online trends
2. Customer Insights - Analyze customer data
3. Offer Design - Create offer concepts

**Advanced Path**:
- Competitor Intelligence - Research competitors (commented out by default)

**Recommendation**: Start with Market Trends and Customer Insights. These provide the foundation for offer design. Enable Competitor Intelligence only if time permits and competitive gaps are required in final output.

---

*Hackathon Date: November 10, 2025 | 10:30 AM - 12:00 PM*
