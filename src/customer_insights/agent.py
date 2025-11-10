"""
This module defines the root agent for the Customer Insights team.

This agent's primary responsibility is to extract and synthesize insights from
Wendy's internal data sources, which are mocked using a BigQuery database.
It uses a ParallelAgent to conduct different types of analysis simultaneously,
making the research process more efficient.
"""
# Load environment variables from .env file (must be imported early)
from utils.env_loader import load_env
load_env()

from google.adk.agents.parallel_agent import ParallelAgent

from .sub_agents.behavioral_analysis.agent import behavioral_analysis_agent
from .sub_agents.profile_synthesizer.agent import profile_synthesizer_agent
from .sub_agents.sentiment_analysis.agent import sentiment_analysis_agent

# The Customer Insights Manager is a ParallelAgent. This means it runs all the
# specified sub-agents (behavioral_analysis, profile_synthesizer, etc.) at the
# same time. This is useful for running independent analyses concurrently.
customer_insights_manager_agent = ParallelAgent(
    name="CustomerInsightsAgent",
    sub_agents=[
        behavioral_analysis_agent,
        profile_synthesizer_agent,
        # sentiment_analysis_agent,
    ],
    description=(
        "An agent that analyzes customer data to uncover behavioral patterns,"
        " synthesize customer profiles, and perform sentiment analysis. It runs"
        " multiple analyses in parallel to generate comprehensive insights."
    ),
)

root_agent = customer_insights_manager_agent