"""AgentTools for delegating to sub-agents"""
from google.adk.tools import AgentTool
from customer_insights.sub_agents.insight_orchestrator.agent import insight_orchestrator_agent
from customer_insights.sub_agents.profile_synthesizer.agent import profile_synthesizer_agent

# Create AgentTools to wrap sub-agents - allows root agent to invoke them as tools
# This follows the pattern from the Google ADK blog post on deep research agents
insight_orchestrator_tool = AgentTool(agent=insight_orchestrator_agent)
profile_synthesizer_tool = AgentTool(agent=profile_synthesizer_agent)

# Export all agent tools for use in root agent
agent_tools = [
    insight_orchestrator_tool,
    profile_synthesizer_tool,
]
