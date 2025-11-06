"""Research Squad Agent - The Data Gatherer (ParallelAgent)"""
from google.adk.agents.parallel_agent import ParallelAgent

# Import the three research specialist agents
# These are the root agents from each specialist module
from market_trends_analyst.agent import market_trends_analyst_root_agent
from customer_insights.agent import customer_insights_manager_agent
from competitor_intelligence.agent import competitor_intel_manager_agent

# -- Research Squad Agent (ParallelAgent) --
# This agent runs all three research specialists simultaneously
# It receives a high-level goal and passes it to all three agents in parallel
research_squad_agent = ParallelAgent(
    name="ResearchSquadAgent",
    sub_agents=[
        market_trends_analyst_root_agent,      # Market Trends research
        customer_insights_manager_agent,         # Customer Insights research
        competitor_intel_manager_agent,          # Competitor Intelligence research
    ],
    description="Coordinates parallel execution of all three research agents (Market Trends, Customer Insights, Competitor Intelligence) to gather comprehensive intelligence simultaneously.",
)

