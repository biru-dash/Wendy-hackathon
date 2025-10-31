# Wendy's AI Agents Hackathon

**Date**: November 10, 2025  
**Time**: 10:30 AM - 12:00 PM (90 minutes)  

## 🎯 Overview

Work with Wendy's AI agent system to analyze customer data and market trends. You'll modify agent instructions and parameters to improve marketing intelligence outputs.

### Schedule

| Time | Activity |
|------|----------|
| 10:30 - 10:40 AM | Intro & Setup (10 min) |
| 10:40 - 11:20 AM | **Level 1**: Core Agents (40 min) |
| 11:20 - 11:50 AM | **Level 2**: Advanced (30 min) |
| 11:50 - 12:00 PM | Demos & Judging (10 min) |

---

## 🚀 Setup (10:30 - 10:40 AM)

### Quick Start

```bash
# Clone and navigate
git clone <REPOSITORY_URL>
cd wendy-hack-sprint

# Activate environment (already set up for you)
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Launch interface (choose one)
.\start_adk_web.bat      # Option A: ADK Web (Recommended)
python hackathon_ui.py   # Option B: Streamlit UI
```

### Agent Structure
Each agent folder has:
- `root_agent_instruction.txt` - Instructions you'll modify
- `tools/agent_tools.py` - Tool functions
- `sub_agents/` - Specialized sub-agents

---

## 📊 Level 1: Core Agents (10:40 - 11:20 AM)

### Goal
Learn how agents work by improving two core agents through instruction tuning.

### Task 1: Customer Insights Agent (20 min)

**What it does**: Analyzes customer data from BigQuery datasets

**Your mission**: Improve the insights by modifying instructions

**Steps**:
1. Open `customer_insights/root_agent_instruction.txt`
2. Test baseline: "What are dining preferences of Gen-Z customers?"
3. Modify instructions to be more specific:
   - Add demographic focus (age groups, regions)
   - Request quantitative metrics
   - Specify output format (bullet points, tables)
4. Re-run and compare results

**Example Enhancement**:
```
Add to instructions: "Always include percentage metrics, compare across age groups, 
and highlight actionable insights for QSR marketing campaigns."
```

### Task 2: Market Trends Analyst (20 min)

**What it does**: Uses Google Search to find market trends and industry insights

**Your mission**: Make it more relevant for Wendy's

**Steps**:
1. Open `market_trends_analyst/root_agent_instruction.txt`
2. Test baseline: "What are emerging food trends in QSR?"
3. Modify instructions to:
   - Focus on specific topics (plant-based, delivery, social media)
   - Prioritize recent trends (last 3 months)
   - Request competitive comparisons
4. Re-run and compare results

**Example Enhancement**:
```
Add to instructions: "Focus on trends relevant to quick-service restaurants. 
Prioritize social media trends and competitor innovations from the past quarter."
```

### Success Criteria
- ✅ More specific, actionable outputs
- ✅ Better data/metrics included
- ✅ Outputs align with Wendy's needs
- ✅ Faster, more focused results

---

## 🚀 Level 2: Advanced (11:20 - 11:50 AM)

### Goal
For teams who finish Level 1 early - add competitive intelligence and multi-agent workflows.

### Task 3: Competitor Intelligence (15 min)

**What it does**: Monitors and analyzes competitor strategies using web search and synthesis

**Your mission**: Configure it to track specific competitors

**Steps**:
1. Open `competitor_intelligence/root_agent_instruction.txt`
2. Add specific competitors: McDonald's, Burger King, Chick-fil-A, Taco Bell
3. Test: "What promotional strategies are competitors using this quarter?"
4. Modify to focus on:
   - Pricing strategies
   - Menu innovations
   - Digital/delivery initiatives
   - Social media campaigns

**Example Enhancement**:
```
Add to instructions: "Focus on McDonald's, Burger King, and Chick-fil-A. 
Prioritize pricing, limited-time offers, and digital ordering innovations. 
Provide actionable competitive insights with specific examples."
```

### Task 4: Multi-Agent Integration (15 min)

**Your mission**: Chain agents together for comprehensive insights

**Ideas**:
- Run Market Trends → then feed insights to Customer Insights
- Run Customer Insights + Competitor Intelligence → identify gaps
- Create a "Campaign Brief" using multiple agent outputs

**Steps**:
1. Run Customer Insights: "What do Gen-Z customers want?"
2. Run Competitor Intelligence: "What are competitors offering to Gen-Z?"
3. Run Market Trends: "What Gen-Z food trends are emerging?"
4. Synthesize results into one recommendation

### Bonus Challenges
- Add custom tools to `tools/agent_tools.py`
- Optimize BigQuery queries in `customer_insights/data/`
- Create chain-of-thought prompts in instructions
- Add few-shot examples to improve accuracy

---

## 🎬 Demos & Judging (11:50 AM - 12:00 PM)

### Quick Demo Format (2 minutes per team)

1. **Show before/after** (30 sec): Run same query with original vs. modified instructions
2. **Highlight changes** (30 sec): What you modified and why
3. **Business impact** (30 sec): How this helps Wendy's
4. **Q&A** (30 sec): Quick judge questions

### Judging Criteria (Total: 50 points)

| Criterion | Points | What Judges Look For |
|-----------|--------|---------------------|
| **Output Quality** | 20 | Better insights, more actionable, specific metrics |
| **Innovation** | 15 | Creative modifications, unique approach |
| **Business Value** | 10 | Clear value to Wendy's marketing |
| **Execution** | 5 | Works properly, clean implementation |

**Winners**: Top 3 teams by total score


---

## 📚 Quick Reference

### Key Files
- `customer_insights/root_agent_instruction.txt` - Customer agent instructions
- `market_trends_analyst/root_agent_instruction.txt` - Trends agent instructions  
- `competitor_intelligence/root_agent_instruction.txt` - Competitor agent instructions
- `customer_insights/data/BIGQUERY_TABLES_SUMMARY.md` - Available datasets

### Commands
```bash
.\start_adk_web.bat           # Launch ADK Web
python hackathon_ui.py        # Launch Streamlit
python test_adk_endpoint.py   # Test GCP connection
```

### Test Queries
- **Customer Insights**: "What are dining preferences of Gen-Z customers?"
- **Market Trends**: "What are emerging food trends in QSR?"
- **Competitor Intelligence**: "What promotional strategies are competitors using?"

### Tips
- ✅ Test before and after each change
- ✅ Focus on clear, measurable improvements
- ✅ Keep modifications simple and purposeful
- ✅ Think about business value for Wendy's

---

## 🚀 Ready? Let's Go!

Focus on making clear improvements, test frequently, and have fun! 🎉

---

*Hackathon Date: November 10, 2025 | 10:30 AM - 12:00 PM*