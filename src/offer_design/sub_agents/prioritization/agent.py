"""Prioritization Agent - The Business Analyst"""
from google.adk.agents.llm_agent import LlmAgent
from utils.instruction_loader import load_instruction_from_file
import os

# PrioritizationAgent is model-only - no tools needed
# It ranks and prioritizes the final offer concepts

prioritization_agent = LlmAgent(
    name="PrioritizationAgent",
    model=os.getenv("GEN_ADVANCED_MODEL", "gemini-2.5-pro"),
    instruction=load_instruction_from_file(
        "offer_design/sub_agents/prioritization/instruction.txt"
    ),
    description="Prioritizes final offer concepts by feasibility and expected impact to produce the final ranked list.",
    tools=[],  # Model-only agent - no tools needed
)

