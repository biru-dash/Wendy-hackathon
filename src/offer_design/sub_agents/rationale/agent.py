"""Rationale Agent - The Strategist"""
from google.adk.agents.llm_agent import LlmAgent
from utils.instruction_loader import load_instruction_from_file
import os

# RationaleAgent is model-only - no tools needed
# It provides strategic rationale and cites evidence for each offer

rationale_agent = LlmAgent(
    name="RationaleAgent",
    model=os.getenv("GEN_ADVANCED_MODEL", "gemini-2.5-pro"),
    description="Provides concise rationale for each offer concept and explicitly cites which input signals supported each design decision.",
    instruction=load_instruction_from_file(
        "offer_design/sub_agents/rationale/instruction.txt"
    ),
    tools=[],  # Model-only agent - no tools needed
)

