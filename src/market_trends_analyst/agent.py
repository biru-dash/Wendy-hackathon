"""
This module defines the root agent for the Market Trends Analyst team.

This agent is responsible for scanning the internet to find relevant news,
articles, and discussions related to a specific marketing query. It uses a
SequentialAgent architecture to first collect data and then synthesize it.
"""
from google.adk.agents.sequential_agent import SequentialAgent

from .sub_agents.data_collection.agent import data_collection_agent
from .sub_agents.research_synthesis.agent import research_synthesis_agent

# The Market Trends Analyst is a SequentialAgent that first runs the
# data_collection_agent to search for information online, and then passes
# the collected data to the research_synthesis_agent to summarize and extract
# key insights.
market_trends_analyst_root_agent = SequentialAgent(
    name="MarketTrendsAnalystAgent",
    sub_agents=[data_collection_agent, research_synthesis_agent],
    description=(
        "An agent specialized in analyzing market trends. It takes a research"
        " query, finds relevant online information, and synthesizes the findings"
        " into a concise summary."
    ),
)

root_agent = market_trends_analyst_root_agent


