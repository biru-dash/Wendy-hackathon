"""Offer Design Manager Agent with Sub-Agents Architecture"""
from google.adk.agents.sequential_agent import SequentialAgent

# Import sub-agents for SequentialAgent workflow
from offer_design.sub_agents.concept_generation.agent import concept_generation_agent
from offer_design.sub_agents.offer_definition.agent import offer_definition_agent
from offer_design.sub_agents.rationale.agent import rationale_agent
from offer_design.sub_agents.prioritization.agent import prioritization_agent

# -- Offer Design Manager Agent (Root Orchestrator) --
# This is a SequentialAgent that manages the workflow by executing sub-agents in order
# Each agent builds on the previous one's output in a "virtual assembly line"
offer_design_manager_agent = SequentialAgent(
    name="OfferDesignManagerAgent",
    sub_agents=[
        concept_generation_agent,      # Step 1: Generate raw creative ideas
        offer_definition_agent,        # Step 2: Structure and define the offers
        rationale_agent,              # Step 3: Add strategic rationale with citations
        prioritization_agent,         # Step 4: Rank by feasibility and impact
    ],
    description="Root manager agent that orchestrates offer design workflow through concept generation, definition, rationale development, and prioritization.",
)

# -- Run the root agent for the runner --
root_agent = offer_design_manager_agent

