"""AgentTools for delegating to sub-agents"""
from google.adk.tools import AgentTool
from market_trends_analyst.sub_agents.data_collection.agent import data_collection_agent
from market_trends_analyst.sub_agents.research_synthesis.agent import research_synthesis_agent

# Create AgentTools to wrap sub-agents - allows root agent to invoke them as tools
# This follows the pattern from the Google ADK blog post on deep research agents
data_collection_tool = AgentTool(agent=data_collection_agent)
research_synthesis_tool = AgentTool(agent=research_synthesis_agent)

# Export all agent tools for use in root agent
agent_tools = [
    data_collection_tool,
    research_synthesis_tool,
]
