"""AgentTools for delegating to sub-agents in Competitor Intelligence"""
from google.adk.tools import AgentTool
from competitor_intelligence.sub_agents.competitor_analysis.agent import competitor_analysis_agent

# Create AgentTool to wrap CompetitorAnalysisAgent
# This allows ResearchOrchestratorAgent to invoke it multiple times (once per competitor)
competitor_analysis_tool = AgentTool(agent=competitor_analysis_agent)

# Export all agent tools for use in orchestrator agent
agent_tools = [
    competitor_analysis_tool,
]

