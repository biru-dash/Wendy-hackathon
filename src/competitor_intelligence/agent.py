"""
This module defines the root agent for the Competitor Intelligence team.

This agent is responsible for gathering and analyzing information about
Wendy's competitors. It uses a SequentialAgent to orchestrate a workflow of
identifying targets, conducting research, and synthesizing the findings.
"""
from google.adk.agents.sequential_agent import SequentialAgent

from .sub_agents.competitor_analysis.agent import competitor_analysis_agent
from .sub_agents.research_orchestrator.agent import research_orchestrator_agent
from .sub_agents.target_identification.agent import target_identification_agent
from .sub_agents.whitespace_synthesizer.agent import whitespace_synthesizer_agent

# The Competitor Intelligence Manager is a SequentialAgent that follows a clear
# research process. Participants can modify this workflow by changing the order
# or adding new analytical steps.
competitor_intel_manager_agent = SequentialAgent(
    name="CompetitorIntelAgent",
    sub_agents=[
        target_identification_agent,
        research_orchestrator_agent,
        competitor_analysis_agent,
        whitespace_synthesizer_agent,
    ],
    description=(
        "An agent that performs competitive analysis by identifying targets, "
        "orchestrating research, analyzing competitors, and synthesizing "
        "whitespace opportunities."
    ),
)

root_agent = competitor_intel_manager_agent

